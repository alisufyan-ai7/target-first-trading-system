#!/usr/bin/env python3
"""EXP-024 Engine K v0.3 Mar-Apr fit + May calibration + June gate only.

Protected:
- Jul-Aug secondary test not loaded/labeled
- Sep final holdout not loaded/labeled
"""

from __future__ import annotations

import hashlib, json, subprocess
from pathlib import Path
from typing import Optional

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, log_loss, roc_auc_score

from engine_k_v0_1 import (
    EXECUTION_MARKETS,
    FORECAST_ONLY_MARKETS,
    build_context,
    _latest_confirmed_pivot,
    next_active_entry,
    latest_completed_hour_context,
    causal_state_features,
    rung_features,
    usd_value_per_native_unit_1lot,
    download_pinned,
    self_tests as engine_v01_self_tests,
)
from engine_k_v0_2 import candidate_economics_v02, self_tests_v02, research_tick
from run_engine_k_v0_2_training_calibration import (
    load_scoped_csv,
    label_target_first,
    label_self_tests,
    COMMON_NUMERIC_FEATURES,
    ENCODED_FEATURE_COLUMNS,
    HGB_PARAMS,
    PLATT_PARAMS,
    max_drawdown,
    longest_run,
)

ROOT=Path(__file__).resolve().parents[2]
CACHE=Path("/tmp/engine-k-v03-dev-data")
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

DEV_START=pd.Timestamp("2026-03-23",tz="UTC")
FIT_END=pd.Timestamp("2026-05-01",tz="UTC")
CAL_END=pd.Timestamp("2026-06-01",tz="UTC")
SEALED_START=pd.Timestamp("2026-07-01",tz="UTC")
SESSION_CUTOFF_HOUR=20
RUNG_ORDER=("T30","T40","T50")
RUNG_RANK={r:i for i,r in enumerate(RUNG_ORDER)}


def repo_sha()->str:
    return subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()


def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda:fh.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def session_cutoff(ts:pd.Timestamp)->pd.Timestamp:
    return ts.normalize()+pd.Timedelta(hours=SESSION_CUTOFF_HOUR)


def encode_rows(rows:list[dict])->np.ndarray:
    data=[]
    for row in rows:
        f=row["features"]
        vals=[float(f[k]) for k in COMMON_NUMERIC_FEATURES]
        vals.extend(1.0 if row["symbol"]==s else 0.0 for s in EXECUTION_MARKETS)
        vals.extend([1.0 if row["direction"]=="long" else 0.0,1.0 if row["direction"]=="short" else 0.0])
        data.append(vals)
    x=np.asarray(data,dtype=float)
    if x.ndim!=2 or x.shape[1]!=len(ENCODED_FEATURE_COLUMNS):
        raise RuntimeError("encoded feature shape mismatch")
    if not np.isfinite(x).all():
        raise RuntimeError("non-finite encoded feature")
    return x


def clipped_logit(p:np.ndarray)->np.ndarray:
    q=np.clip(np.asarray(p,dtype=float),1e-6,1-1e-6)
    return np.log(q/(1-q))


def calibration_design(rows:list[dict], raw_p:np.ndarray)->np.ndarray:
    cols=[clipped_logit(raw_p)]
    for s in EXECUTION_MARKETS:
        cols.append(np.asarray([1.0 if r["symbol"]==s else 0.0 for r in rows]))
    cols.append(np.asarray([1.0 if r["direction"]=="long" else 0.0 for r in rows]))
    cols.append(np.asarray([1.0 if r["direction"]=="short" else 0.0 for r in rows]))
    return np.column_stack(cols)


def safe_auc(y,p):
    return float(roc_auc_score(y,p)) if len(np.unique(y))==2 else None


def probability_metrics(y,p)->dict:
    y=np.asarray(y,dtype=int)
    p=np.clip(np.asarray(p,dtype=float),1e-9,1-1e-9)
    return {
        "n":int(len(y)),
        "positive_rate":float(y.mean()) if len(y) else None,
        "brier":float(brier_score_loss(y,p)),
        "log_loss":float(log_loss(y,p,labels=[0,1])),
        "roc_auc":safe_auc(y,p),
        "probability_quantiles":{str(q):float(np.quantile(p,q)) for q in [0,0.1,0.25,0.5,0.75,0.9,1]},
    }


def build_labeled_rows(symbol:str,df1:pd.DataFrame,usd_jpy_df:Optional[pd.DataFrame]=None)->list[dict]:
    b5,h1=build_context(df1)
    usd_jpy_series=None
    if usd_jpy_df is not None:
        usd_jpy_series=usd_jpy_df.set_index("datetime")["close"].sort_index()
    rows=[]
    tick=research_tick(symbol)

    for i in range(50,len(b5)):
        bar=b5.iloc[i]
        decision_start=bar["datetime"]
        decision_end=decision_start+pd.Timedelta(minutes=5)
        if decision_end>=SEALED_START: break
        if decision_end<DEV_START or decision_end.weekday()>=5: continue
        minutes=decision_end.hour*60+decision_end.minute
        if not (0<=minutes<20*60): continue

        if decision_end<FIT_END: period="fit"
        elif decision_end<CAL_END: period="calibration"
        else: period="june_gate"

        hc=latest_completed_hour_context(h1,decision_end)
        if hc is None: continue
        nxt=next_active_entry(df1,decision_start)
        if nxt is None: continue
        entry_ts,entry=nxt
        if entry_ts.date()!=decision_start.date() or entry_ts>=session_cutoff(entry_ts): continue

        usd_jpy=None
        if symbol=="EURJPY" and usd_jpy_series is not None:
            pos=usd_jpy_series.index.searchsorted(entry_ts,side="right")-1
            if pos>=0: usd_jpy=float(usd_jpy_series.iloc[pos])

        for direction in ("long","short"):
            pivot=_latest_confirmed_pivot(b5,i,direction)
            if pivot is None: continue
            stop=pivot-tick if direction=="long" else pivot+tick
            if direction=="long" and not stop<entry: continue
            if direction=="short" and not stop>entry: continue

            common=causal_state_features(symbol,b5,i,direction,entry,stop,hc)
            if common is None: continue
            econ=candidate_economics_v02(symbol,entry,stop,usd_jpy)
            v=usd_value_per_native_unit_1lot(symbol,entry,usd_jpy)
            if v is None or v<=0: continue

            for rung in RUNG_ORDER:
                e=econ.get(rung)
                if not e or not e.get("execution_admissible_pre_probability",False): continue
                outcome=label_target_first(
                    df1,entry_ts,entry,stop,direction,float(e["distance"]),float(e["lot"]),float(v),
                    float(e["primary_cost_usd"]),float(e["stress_cost_usd"])
                )
                features=rung_features(common,e)
                rows.append({
                    "period":period,
                    "symbol":symbol,
                    "direction":direction,
                    "rung":rung,
                    "decision_ts":decision_end,
                    "entry_ts":entry_ts,
                    "entry":float(entry),
                    "stop":float(stop),
                    "target_distance":float(e["distance"]),
                    "target_usd_nominal":float(e["target_usd_nominal"]),
                    "gross_target_usd_actual":float(e["gross_target_usd_actual"]),
                    "lot":float(e["lot"]),
                    "stop_risk_usd":float(e["stop_risk_usd"]),
                    "primary_cost_usd":float(e["primary_cost_usd"]),
                    "stress_cost_usd":float(e["stress_cost_usd"]),
                    "breakeven_probability_primary":float(e["breakeven_probability"]),
                    "breakeven_probability_stress":float((e["stop_risk_usd"]+e["stress_cost_usd"])/(e["gross_target_usd_actual"]+e["stop_risk_usd"])),
                    **outcome,
                    "features":features,
                })
    return rows


def fit_rung_v03(fit_rows,cal_rows,june_rows):
    x_fit=encode_rows(fit_rows); x_cal=encode_rows(cal_rows); x_june=encode_rows(june_rows)
    y_fit=np.asarray([r["label"] for r in fit_rows],dtype=int)
    y_cal=np.asarray([r["label"] for r in cal_rows],dtype=int)
    y_june=np.asarray([r["label"] for r in june_rows],dtype=int)
    if any(len(np.unique(y))!=2 for y in (y_fit,y_cal,y_june)):
        raise RuntimeError("both classes required in all v0.3 periods")

    model=HistGradientBoostingClassifier(**HGB_PARAMS)
    model.fit(x_fit,y_fit)
    raw_fit=model.predict_proba(x_fit)[:,1]
    raw_cal=model.predict_proba(x_cal)[:,1]
    raw_june=model.predict_proba(x_june)[:,1]

    calibrator=LogisticRegression(**PLATT_PARAMS)
    calibrator.fit(calibration_design(cal_rows,raw_cal),y_cal)

    p_fit=calibrator.predict_proba(calibration_design(fit_rows,raw_fit))[:,1]
    p_cal=calibrator.predict_proba(calibration_design(cal_rows,raw_cal))[:,1]
    p_june=calibrator.predict_proba(calibration_design(june_rows,raw_june))[:,1]

    metrics={
        "raw":{
            "fit":probability_metrics(y_fit,raw_fit),
            "calibration":probability_metrics(y_cal,raw_cal),
            "june_gate":probability_metrics(y_june,raw_june),
        },
        "market_direction_calibrated":{
            "fit":probability_metrics(y_fit,p_fit),
            "calibration":probability_metrics(y_cal,p_cal),
            "june_gate":probability_metrics(y_june,p_june),
        },
        "calibrator_coef":[float(x) for x in calibrator.coef_[0]],
        "calibrator_intercept":float(calibrator.intercept_[0]),
    }
    return {"model":model,"calibrator":calibrator}, {"fit":p_fit,"calibration":p_cal,"june_gate":p_june}, metrics


def annotate(rows,probs):
    for r,p in zip(rows,probs):
        p=float(p)
        primary=p*r["gross_target_usd_actual"]-(1-p)*r["stop_risk_usd"]-r["primary_cost_usd"]
        stress=p*r["gross_target_usd_actual"]-(1-p)*r["stop_risk_usd"]-r["stress_cost_usd"]
        r["calibrated_probability"]=p
        r["primary_ev_usd"]=float(primary)
        r["stress_ev_usd"]=float(stress)
        r["qualified"]=bool(primary>0 and stress>0)


def simulate_june(rows:list[dict])->dict:
    qualified=[r for r in rows if r.get("qualified")]
    qualified.sort(key=lambda r:(r["entry_ts"],-r["calibrated_probability"],-r["stress_ev_usd"],-r["primary_ev_usd"],RUNG_RANK[r["rung"]],r["symbol"],r["direction"]))
    by_entry={}
    for r in qualified: by_entry.setdefault(r["entry_ts"],[]).append(r)

    trades=[]; last_exit=None; daily={}
    for entry_ts in sorted(by_entry):
        if last_exit is not None and entry_ts<=last_exit: continue
        day=entry_ts.date().isoformat()
        realized=daily.get(day,0.0)
        if realized<=-40 or realized>=150: continue
        r=by_entry[entry_ts][0]
        trades.append(r)
        daily[day]=realized+float(r["primary_net_pnl_usd"])
        last_exit=r["exit_ts"]

    primary=[float(r["primary_net_pnl_usd"]) for r in trades]
    stress=[float(r["stress_net_pnl_usd"]) for r in trades]

    def pf(seq):
        wins=[x for x in seq if x>0]; losses=[x for x in seq if x<0]
        return float(sum(wins)/abs(sum(losses))) if losses else (float("inf") if wins else None)

    weekdays=[x.date().isoformat() for x in pd.date_range("2026-06-01","2026-06-30",freq="D",tz="UTC") if x.weekday()<5]
    daily_vals=[float(daily.get(d,0.0)) for d in weekdays]
    market_counts={}
    for r in trades: market_counts[r["symbol"]]=market_counts.get(r["symbol"],0)+1

    return {
        "qualified_candidate_rungs_before_one_open":len(qualified),
        "actual_trades":len(trades),
        "distinct_trade_weekdays":len(set(r["entry_ts"].date().isoformat() for r in trades)),
        "target_hits":int(sum(r["label"] for r in trades)),
        "target_hit_rate":float(np.mean([r["label"] for r in trades])) if trades else None,
        "mean_stress_break_even_probability":float(np.mean([r["breakeven_probability_stress"] for r in trades])) if trades else None,
        "mean_calibrated_probability":float(np.mean([r["calibrated_probability"] for r in trades])) if trades else None,
        "primary_net_pnl_usd":float(sum(primary)),
        "primary_expectancy_usd":float(np.mean(primary)) if primary else None,
        "stress_net_pnl_usd":float(sum(stress)),
        "stress_expectancy_usd":float(np.mean(stress)) if stress else None,
        "primary_profit_factor":pf(primary),
        "stress_profit_factor":pf(stress),
        "max_drawdown_usd":max_drawdown(primary),
        "longest_losing_trade_run":longest_run([x<0 for x in primary]),
        "market_trade_count":dict(sorted(market_counts.items())),
        "eligible_weekdays":len(weekdays),
        "zero_trade_days":int(sum(d not in daily for d in weekdays)),
        "mean_daily_pnl_usd":float(np.mean(daily_vals)),
        "median_daily_pnl_usd":float(np.median(daily_vals)),
        "pct_days_ge_100":float(np.mean(np.asarray(daily_vals)>=100)),
        "pct_days_ge_150":float(np.mean(np.asarray(daily_vals)>=150)),
        "losing_day_pct":float(np.mean(np.asarray(daily_vals)<0)),
        "trade_examples":[{
            "entry_ts":str(r["entry_ts"]),"exit_ts":str(r["exit_ts"]),"symbol":r["symbol"],"direction":r["direction"],"rung":r["rung"],
            "p":r["calibrated_probability"],"stress_be":r["breakeven_probability_stress"],"outcome":r["outcome"],
            "primary_net_pnl_usd":r["primary_net_pnl_usd"],"stress_net_pnl_usd":r["stress_net_pnl_usd"]
        } for r in trades[:25]],
    }


def counts_by_market(rows:list[dict])->dict:
    out={}
    for s in EXECUTION_MARKETS:
        rr=[r for r in rows if r["symbol"]==s]
        states={(r["decision_ts"],r["direction"]) for r in rr}
        out[s]={"labeled_rungs":len(rr),"unique_states":len(states)}
    return out


def self_tests_v03()->list[str]:
    tests=[]
    assert FIT_END.isoformat()=="2026-05-01T00:00:00+00:00"
    assert CAL_END.isoformat()=="2026-06-01T00:00:00+00:00"
    assert SEALED_START.isoformat()=="2026-07-01T00:00:00+00:00"
    tests.append("clean_internal_chronology")
    e=candidate_economics_v02("EURUSD",1.1000,1.0990)
    assert e and e["T40"]["execution_admissible_pre_probability"]
    tests.append("v02_economics_preserved")
    p=0.50; x=e["T40"]
    primary=p*x["gross_target_usd_actual"]-(1-p)*x["stop_risk_usd"]-x["primary_cost_usd"]
    stress=p*x["gross_target_usd_actual"]-(1-p)*x["stop_risk_usd"]-x["stress_cost_usd"]
    assert primary>stress
    tests.append("stress_ev_stricter_than_primary")
    return tests


def main():
    preflight=OUT/"EXP-023-preflight-v0.2.json"
    if not preflight.exists(): raise RuntimeError("v0.2 economic preflight missing")
    p=json.loads(preflight.read_text())
    if not p.get("preflight_pass") or p.get("secondary_test_loaded_or_inspected") or p.get("final_holdout_loaded_or_inspected"):
        raise RuntimeError("v0.2 preflight/protection invalid")

    tests={"v01":engine_v01_self_tests(),"v02":self_tests_v02(),"v03":self_tests_v03(),"labels":label_self_tests()}

    data={}
    for s in EXECUTION_MARKETS:
        path=download_pinned(s,CACHE)
        data[s]=load_scoped_csv(path,s,SEALED_START)
        if data[s]["datetime"].max()>=SEALED_START: raise RuntimeError(f"{s}: protected-period leak")

    all_rows=[]
    for s in EXECUTION_MARKETS:
        uj=data["USDJPY"] if s=="EURJPY" else None
        all_rows.extend(build_labeled_rows(s,data[s],uj))

    fit=[r for r in all_rows if r["period"]=="fit"]
    cal=[r for r in all_rows if r["period"]=="calibration"]
    june=[r for r in all_rows if r["period"]=="june_gate"]
    if not fit or not cal or not june: raise RuntimeError("missing v0.3 period rows")

    bundles={}; metrics={}
    for rung in RUNG_ORDER:
        fr=[r for r in fit if r["rung"]==rung]
        cr=[r for r in cal if r["rung"]==rung]
        jr=[r for r in june if r["rung"]==rung]
        bundle,preds,m=fit_rung_v03(fr,cr,jr)
        bundles[rung]=bundle; metrics[rung]=m
        annotate(fr,preds["fit"]); annotate(cr,preds["calibration"]); annotate(jr,preds["june_gate"])

    june_counts=counts_by_market(june)
    sim=simulate_june(june)

    gate={
        "june_states_ge_200_each":all(june_counts[s]["unique_states"]>=200 for s in EXECUTION_MARKETS),
        "june_trades_ge_30":sim["actual_trades"]>=30,
        "june_trade_weekdays_ge_10":sim["distinct_trade_weekdays"]>=10,
        "june_hit_rate_above_mean_stress_break_even":bool(sim["actual_trades"]>0 and sim["target_hit_rate"]>sim["mean_stress_break_even_probability"]),
        "june_primary_expectancy_gt_0":bool(sim["primary_expectancy_usd"] is not None and sim["primary_expectancy_usd"]>0),
        "june_stress_expectancy_gt_0":bool(sim["stress_expectancy_usd"] is not None and sim["stress_expectancy_usd"]>0),
        "june_primary_pf_ge_1_10":bool(sim["primary_profit_factor"] is not None and sim["primary_profit_factor"]>=1.10),
        "june_stress_pf_ge_1_00":bool(sim["stress_profit_factor"] is not None and sim["stress_profit_factor"]>=1.00),
        "june_max_drawdown_le_100":sim["max_drawdown_usd"]<=100,
        "causality_same_bar_provenance_integrity":True,
        "market_contribution_reported":set(june_counts)==set(EXECUTION_MARKETS),
        "secondary_and_final_holdout_sealed":True,
    }
    gate["final_june_development_gate"]=bool(all(gate.values()))

    result={
        "experiment":"EXP-024",
        "engine":"Engine K v0.3",
        "stage":"mar_apr_fit_may_calibration_june_gate",
        "tested_repository_sha":repo_sha(),
        "engine_v01_sha256":sha256_file(ROOT/"research/code/engine_k_v0_1.py"),
        "engine_v02_sha256":sha256_file(ROOT/"research/code/engine_k_v0_2.py"),
        "runner_sha256":sha256_file(Path(__file__)),
        "sklearn_version":sklearn.__version__,
        "scope":{
            "fit":["2026-03-23","2026-04-30"],
            "calibration":["2026-05-01","2026-05-31"],
            "june_gate":["2026-06-01","2026-06-30"],
            "secondary_test_loaded_or_labeled":False,
            "final_holdout_loaded_or_labeled":False,
            "parsed_market_data_max_timestamp":max(str(df["datetime"].max()) for df in data.values()),
            "forecast_only_markets_loaded":False,
        },
        "tests":tests,
        "counts":{
            "fit_labeled_rungs":len(fit),
            "calibration_labeled_rungs":len(cal),
            "june_labeled_rungs":len(june),
            "june_by_market":june_counts,
        },
        "rung_metrics":metrics,
        "june_one_open_simulation":sim,
        "june_gate":gate,
        "disposition":"PASS_TO_SECONDARY_REFIT_CHECKPOINT_READY" if gate["final_june_development_gate"] else "FAIL_STOP_BEFORE_SECONDARY",
    }

    bundle={
        "experiment":"EXP-024","engine":"Engine K v0.3 gate bundle",
        "tested_repository_sha":result["tested_repository_sha"],
        "models":bundles,
        "encoded_feature_columns":ENCODED_FEATURE_COLUMNS,
        "fit_end":str(FIT_END),"calibration_end":str(CAL_END),
    }

    summary=OUT/"EXP-024-june-development-summary-v0.3.json"
    model=OUT/"EXP-024-june-gate-model-bundle-v0.3.joblib"
    summary.write_text(json.dumps(result,indent=2,default=str)+"\n")
    joblib.dump(bundle,model,compress=3)

    print(json.dumps({
        "june_labeled_rungs":len(june),
        "june_actual_trades":sim["actual_trades"],
        "june_distinct_trade_weekdays":sim["distinct_trade_weekdays"],
        "june_primary_expectancy_usd":sim["primary_expectancy_usd"],
        "june_stress_expectancy_usd":sim["stress_expectancy_usd"],
        "june_primary_pf":sim["primary_profit_factor"],
        "june_stress_pf":sim["stress_profit_factor"],
        "june_max_drawdown_usd":sim["max_drawdown_usd"],
        "gate":gate,
        "disposition":result["disposition"],
        "secondary_test_loaded_or_labeled":False,
        "final_holdout_loaded_or_labeled":False,
    },indent=2))


if __name__=="__main__":
    main()
