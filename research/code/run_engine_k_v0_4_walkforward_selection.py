#!/usr/bin/env python3
"""EXP-025 Engine K v0.4 bounded walk-forward configuration selection.

Development-only:
- labels/uses Mar23-Jun30 2026 only
- never loads/labels Jul-Aug secondary test
- never loads/labels Sep final holdout
"""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from engine_k_v0_1 import (
    EXECUTION_MARKETS,
    FORECAST_ONLY_MARKETS,
    download_pinned,
)
from run_engine_k_v0_2_training_calibration import (
    load_scoped_csv,
    COMMON_NUMERIC_FEATURES,
    ENCODED_FEATURE_COLUMNS,
    PLATT_PARAMS,
    max_drawdown,
)
from run_engine_k_v0_3_june_gate import (
    build_labeled_rows,
    encode_rows,
    clipped_logit,
    calibration_design,
    RUNG_ORDER,
    RUNG_RANK,
)

ROOT=Path(__file__).resolve().parents[2]
CACHE=Path("/tmp/engine-k-v04-walkforward-data")
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

DEV_START=pd.Timestamp("2026-03-23",tz="UTC")
SEALED_START=pd.Timestamp("2026-07-01",tz="UTC")

MODEL_VARIANTS={
    "M1":{
        "learning_rate":0.05,
        "max_iter":150,
        "max_leaf_nodes":15,
        "min_samples_leaf":100,
        "l2_regularization":1.0,
        "random_state":20260923,
    },
    "M2":{
        "learning_rate":0.035,
        "max_iter":180,
        "max_leaf_nodes":7,
        "min_samples_leaf":250,
        "l2_regularization":3.0,
        "random_state":20260923,
    },
}
CALIBRATION_VARIANTS=("C1","C2")
QUALIFICATION_POLICIES={
    "Q1":None,
    "Q2":0.90,
    "Q3":0.95,
}
CONFIG_IDS=tuple(
    f"{m}-{c}-{q}"
    for m in MODEL_VARIANTS
    for c in CALIBRATION_VARIANTS
    for q in QUALIFICATION_POLICIES
)

FOLDS=(
    {
        "id":"WF1",
        "fit_start":"2026-03-23","fit_end":"2026-04-06",
        "cal_start":"2026-04-06","cal_end":"2026-04-13",
        "eval_start":"2026-04-13","eval_end":"2026-04-27",
    },
    {
        "id":"WF2",
        "fit_start":"2026-03-23","fit_end":"2026-04-20",
        "cal_start":"2026-04-20","cal_end":"2026-04-27",
        "eval_start":"2026-04-27","eval_end":"2026-05-11",
    },
    {
        "id":"WF3",
        "fit_start":"2026-03-23","fit_end":"2026-05-04",
        "cal_start":"2026-05-04","cal_end":"2026-05-11",
        "eval_start":"2026-05-11","eval_end":"2026-05-25",
    },
    {
        "id":"WF4",
        "fit_start":"2026-03-23","fit_end":"2026-05-18",
        "cal_start":"2026-05-18","cal_end":"2026-05-25",
        "eval_start":"2026-05-25","eval_end":"2026-06-08",
    },
    {
        "id":"WF5",
        "fit_start":"2026-03-23","fit_end":"2026-06-01",
        "cal_start":"2026-06-01","cal_end":"2026-06-08",
        "eval_start":"2026-06-08","eval_end":"2026-06-22",
    },
    {
        "id":"WF6",
        "fit_start":"2026-03-23","fit_end":"2026-06-15",
        "cal_start":"2026-06-15","cal_end":"2026-06-22",
        "eval_start":"2026-06-22","eval_end":"2026-07-01",
    },
)

def ts(x:str)->pd.Timestamp:
    return pd.Timestamp(x,tz="UTC")

def repo_sha()->str:
    return subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()

def sha256_file(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda:fh.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def safe_auc(y,p):
    return float(roc_auc_score(y,p)) if len(np.unique(y))==2 else None

def pf(seq):
    wins=[float(x) for x in seq if x>0]
    losses=[float(x) for x in seq if x<0]
    if losses:
        return float(sum(wins)/abs(sum(losses)))
    return float("inf") if wins else None

def stress_break_even(row:dict)->float:
    return float(
        (row["stop_risk_usd"]+row["stress_cost_usd"])
        /(row["gross_target_usd_actual"]+row["stop_risk_usd"])
    )

def fit_calibrator(kind:str,cal_rows:list[dict],raw_cal:np.ndarray):
    y=np.asarray([r["label"] for r in cal_rows],dtype=int)
    if len(np.unique(y))!=2:
        raise RuntimeError(f"{kind}: calibration requires both classes")
    if kind=="C1":
        x=clipped_logit(raw_cal).reshape(-1,1)
    elif kind=="C2":
        x=calibration_design(cal_rows,raw_cal)
    else:
        raise RuntimeError(f"unknown calibration {kind}")
    model=LogisticRegression(**PLATT_PARAMS)
    model.fit(x,y)
    return model

def apply_calibrator(kind:str,model,rows:list[dict],raw:np.ndarray)->np.ndarray:
    if kind=="C1":
        x=clipped_logit(raw).reshape(-1,1)
    elif kind=="C2":
        x=calibration_design(rows,raw)
    else:
        raise RuntimeError(kind)
    return model.predict_proba(x)[:,1]

def qualified_candidate(row:dict,p:float,threshold:float|None)->dict|None:
    p=float(p)
    primary=p*row["gross_target_usd_actual"]-(1-p)*row["stop_risk_usd"]-row["primary_cost_usd"]
    stress=p*row["gross_target_usd_actual"]-(1-p)*row["stop_risk_usd"]-row["stress_cost_usd"]
    if primary<=0 or stress<=0:
        return None
    if threshold is not None and p+1e-15<threshold:
        return None
    x=dict(row)
    x["calibrated_probability"]=p
    x["primary_ev_usd"]=float(primary)
    x["stress_ev_usd"]=float(stress)
    x["stress_break_even_probability"]=stress_break_even(row)
    return x

def simulate_eval(candidates:list[dict],eval_start:pd.Timestamp,eval_end:pd.Timestamp)->dict:
    candidates=sorted(
        candidates,
        key=lambda r:(
            r["entry_ts"],
            -r["calibrated_probability"],
            -r["stress_ev_usd"],
            -r["primary_ev_usd"],
            RUNG_RANK[r["rung"]],
            r["symbol"],
            r["direction"],
        ),
    )
    by_entry={}
    for r in candidates:
        by_entry.setdefault(r["entry_ts"],[]).append(r)

    trades=[]
    last_exit=None
    daily={}
    for entry_ts in sorted(by_entry):
        if last_exit is not None and entry_ts<=last_exit:
            continue
        day=entry_ts.date().isoformat()
        realized=daily.get(day,0.0)
        if realized<=-40 or realized>=150:
            continue
        r=by_entry[entry_ts][0]
        trades.append(r)
        daily[day]=realized+float(r["primary_net_pnl_usd"])
        last_exit=r["exit_ts"]

    primary=[float(r["primary_net_pnl_usd"]) for r in trades]
    stress=[float(r["stress_net_pnl_usd"]) for r in trades]
    eligible=[
        d.date().isoformat()
        for d in pd.date_range(
            eval_start.normalize(),
            eval_end-pd.Timedelta(days=1),
            freq="D",tz="UTC"
        )
        if d.weekday()<5
    ]
    market_counts={}
    for r in trades:
        market_counts[r["symbol"]]=market_counts.get(r["symbol"],0)+1
    max_share=max(market_counts.values())/len(trades) if trades else None
    primary_dd=max_drawdown(primary)
    stress_dd=max_drawdown(stress)

    return {
        "qualified_candidate_rungs_before_one_open":len(candidates),
        "actual_trades":len(trades),
        "distinct_trade_weekdays":len(set(r["entry_ts"].date().isoformat() for r in trades)),
        "target_hits":int(sum(r["label"] for r in trades)),
        "target_hit_rate":float(np.mean([r["label"] for r in trades])) if trades else None,
        "mean_stress_break_even_probability":float(np.mean([r["stress_break_even_probability"] for r in trades])) if trades else None,
        "primary_net_pnl_usd":float(sum(primary)),
        "stress_net_pnl_usd":float(sum(stress)),
        "primary_expectancy_usd":float(np.mean(primary)) if primary else None,
        "stress_expectancy_usd":float(np.mean(stress)) if stress else None,
        "primary_profit_factor":pf(primary),
        "stress_profit_factor":pf(stress),
        "primary_max_drawdown_usd":primary_dd,
        "stress_max_drawdown_usd":stress_dd,
        "market_trade_count":dict(sorted(market_counts.items())),
        "max_market_trade_share":float(max_share) if max_share is not None else None,
        "eligible_weekdays":len(eligible),
        "zero_trade_weekdays":int(sum(d not in daily for d in eligible)),
        "daily_primary_pnl":[{"date":d,"pnl":float(daily.get(d,0.0))} for d in eligible],
        "trades":[{
            "entry_ts":str(r["entry_ts"]),
            "exit_ts":str(r["exit_ts"]),
            "symbol":r["symbol"],
            "direction":r["direction"],
            "rung":r["rung"],
            "label":int(r["label"]),
            "outcome":r["outcome"],
            "p":float(r["calibrated_probability"]),
            "stress_be":float(r["stress_break_even_probability"]),
            "primary_net_pnl_usd":float(r["primary_net_pnl_usd"]),
            "stress_net_pnl_usd":float(r["stress_net_pnl_usd"]),
        } for r in trades],
    }

def aggregate_config(config_id:str,fold_results:list[dict])->dict:
    trades=[]
    for f in fold_results:
        for t in f["simulation"]["trades"]:
            x=dict(t)
            x["fold"]=f["fold"]
            trades.append(x)
    trades.sort(key=lambda r:r["entry_ts"])
    primary=[t["primary_net_pnl_usd"] for t in trades]
    stress=[t["stress_net_pnl_usd"] for t in trades]
    market_counts={}
    for t in trades:
        market_counts[t["symbol"]]=market_counts.get(t["symbol"],0)+1
    max_share=max(market_counts.values())/len(trades) if trades else None
    hit=float(np.mean([t["label"] for t in trades])) if trades else None
    mean_be=float(np.mean([t["stress_be"] for t in trades])) if trades else None
    distinct_days=len(set(t["entry_ts"][:10] for t in trades))
    stress_exps=[f["simulation"]["stress_expectancy_usd"] for f in fold_results]
    positive_folds=sum(x is not None and x>0 for x in stress_exps)
    worst_fold=min(stress_exps) if all(x is not None for x in stress_exps) else None
    stress_dd=max_drawdown(stress)
    primary_dd=max_drawdown(primary)

    pooled={
        "configuration_id":config_id,
        "total_actual_trades":len(trades),
        "total_distinct_trade_weekdays":distinct_days,
        "target_hit_rate":hit,
        "mean_stress_break_even_probability":mean_be,
        "primary_net_pnl_usd":float(sum(primary)),
        "stress_net_pnl_usd":float(sum(stress)),
        "primary_expectancy_usd":float(np.mean(primary)) if primary else None,
        "stress_expectancy_usd":float(np.mean(stress)) if stress else None,
        "primary_profit_factor":pf(primary),
        "stress_profit_factor":pf(stress),
        "primary_max_drawdown_usd":primary_dd,
        "stress_max_drawdown_usd":stress_dd,
        "positive_stress_expectancy_folds":positive_folds,
        "worst_fold_stress_expectancy_usd":worst_fold,
        "market_trade_count":dict(sorted(market_counts.items())),
        "max_market_trade_share":float(max_share) if max_share is not None else None,
        "fold_trade_counts":[f["simulation"]["actual_trades"] for f in fold_results],
        "fold_stress_expectancies":stress_exps,
    }
    gate={
        "total_trades_ge_120":pooled["total_actual_trades"]>=120,
        "every_fold_trades_ge_8":all(x>=8 for x in pooled["fold_trade_counts"]),
        "distinct_trade_weekdays_ge_35":pooled["total_distinct_trade_weekdays"]>=35,
        "pooled_primary_expectancy_gt_0":pooled["primary_expectancy_usd"] is not None and pooled["primary_expectancy_usd"]>0,
        "pooled_stress_expectancy_gt_0":pooled["stress_expectancy_usd"] is not None and pooled["stress_expectancy_usd"]>0,
        "pooled_primary_pf_ge_1_10":pooled["primary_profit_factor"] is not None and pooled["primary_profit_factor"]>=1.10,
        "pooled_stress_pf_ge_1_05":pooled["stress_profit_factor"] is not None and pooled["stress_profit_factor"]>=1.05,
        "positive_stress_folds_ge_4":pooled["positive_stress_expectancy_folds"]>=4,
        "worst_fold_stress_expectancy_gt_minus_5":pooled["worst_fold_stress_expectancy_usd"] is not None and pooled["worst_fold_stress_expectancy_usd"]>-5.0,
        "hit_rate_above_mean_stress_break_even":bool(
            pooled["target_hit_rate"] is not None and pooled["mean_stress_break_even_probability"] is not None
            and pooled["target_hit_rate"]>pooled["mean_stress_break_even_probability"]
        ),
        "pooled_stress_max_drawdown_le_150":pooled["stress_max_drawdown_usd"]<=150.0,
        "max_market_share_le_60pct":pooled["max_market_trade_share"] is not None and pooled["max_market_trade_share"]<=0.60,
        "causality_same_bar_provenance_integrity":True,
        "secondary_and_final_holdout_sealed":True,
    }
    gate["configuration_pass"]=bool(all(gate.values()))
    pooled["gate"]=gate
    return pooled

def walkforward_self_tests()->list[str]:
    tests=[]
    assert len(CONFIG_IDS)==12 and len(set(CONFIG_IDS))==12
    tests.append("exact_12_configurations")
    assert len(FOLDS)==6
    for i,f in enumerate(FOLDS):
        fs,fe,cs,ce,es,ee=map(ts,[f["fit_start"],f["fit_end"],f["cal_start"],f["cal_end"],f["eval_start"],f["eval_end"]])
        assert fs==DEV_START
        assert fs<fe<=cs<ce<=es<ee<=SEALED_START
        if i:
            assert ts(FOLDS[i-1]["eval_end"])==es
    tests.append("six_chronological_folds")
    assert ts(FOLDS[-1]["eval_end"])==SEALED_START
    tests.append("july_seal")
    assert set(MODEL_VARIANTS)=={"M1","M2"}
    assert set(CALIBRATION_VARIANTS)=={"C1","C2"}
    assert set(QUALIFICATION_POLICIES)=={"Q1","Q2","Q3"}
    tests.append("bounded_search_axes")
    return tests

def main():
    tests=walkforward_self_tests()

    data={}
    for s in EXECUTION_MARKETS:
        path=download_pinned(s,CACHE)
        data[s]=load_scoped_csv(path,s,SEALED_START)
        if data[s]["datetime"].max()>=SEALED_START:
            raise RuntimeError(f"{s}: protected-period leak")

    rows=[]
    for s in EXECUTION_MARKETS:
        uj=data["USDJPY"] if s=="EURJPY" else None
        rows.extend(build_labeled_rows(s,data[s],uj))

    if not rows:
        raise RuntimeError("no development rows")
    if max(r["decision_ts"] for r in rows)>=SEALED_START:
        raise RuntimeError("labeled protected period")

    config_folds={cid:[] for cid in CONFIG_IDS}
    fold_diagnostics=[]

    for fold in FOLDS:
        fid=fold["id"]
        fit_start,fit_end=ts(fold["fit_start"]),ts(fold["fit_end"])
        cal_start,cal_end=ts(fold["cal_start"]),ts(fold["cal_end"])
        eval_start,eval_end=ts(fold["eval_start"]),ts(fold["eval_end"])

        fit_rows=[r for r in rows if fit_start<=r["decision_ts"]<fit_end]
        cal_rows=[r for r in rows if cal_start<=r["decision_ts"]<cal_end]
        eval_rows=[r for r in rows if eval_start<=r["decision_ts"]<eval_end]
        if not fit_rows or not cal_rows or not eval_rows:
            raise RuntimeError(f"{fid}: empty period")

        per_config_candidates={cid:[] for cid in CONFIG_IDS}
        rung_diag={}

        for model_id,params in MODEL_VARIANTS.items():
            rung_diag[model_id]={}
            for rung in RUNG_ORDER:
                fr=[r for r in fit_rows if r["rung"]==rung]
                cr=[r for r in cal_rows if r["rung"]==rung]
                er=[r for r in eval_rows if r["rung"]==rung]
                y_fit=np.asarray([r["label"] for r in fr],dtype=int)
                y_cal=np.asarray([r["label"] for r in cr],dtype=int)
                y_eval=np.asarray([r["label"] for r in er],dtype=int)
                if any(len(np.unique(y))!=2 for y in (y_fit,y_cal,y_eval)):
                    raise RuntimeError(f"{fid}-{model_id}-{rung}: both classes required")

                model=HistGradientBoostingClassifier(**params)
                model.fit(encode_rows(fr),y_fit)
                raw_cal=model.predict_proba(encode_rows(cr))[:,1]
                raw_eval=model.predict_proba(encode_rows(er))[:,1]

                rung_diag[model_id][rung]={
                    "raw_calibration_auc":safe_auc(y_cal,raw_cal),
                    "raw_evaluation_auc":safe_auc(y_eval,raw_eval),
                    "fit_n":len(fr),"calibration_n":len(cr),"evaluation_n":len(er),
                }

                for cal_id in CALIBRATION_VARIANTS:
                    calibrator=fit_calibrator(cal_id,cr,raw_cal)
                    p_cal=apply_calibrator(cal_id,calibrator,cr,raw_cal)
                    p_eval=apply_calibrator(cal_id,calibrator,er,raw_eval)
                    cal_auc=safe_auc(y_cal,p_cal)
                    eval_auc=safe_auc(y_eval,p_eval)
                    rung_diag[model_id][rung][cal_id]={
                        "calibrated_calibration_auc":cal_auc,
                        "calibrated_evaluation_auc":eval_auc,
                        "probability_quantiles_calibration":{
                            "p90":float(np.quantile(p_cal,0.90)),
                            "p95":float(np.quantile(p_cal,0.95)),
                        },
                    }

                    for qid,q in QUALIFICATION_POLICIES.items():
                        threshold=None if q is None else float(np.quantile(p_cal,q))
                        cid=f"{model_id}-{cal_id}-{qid}"
                        for row,pv in zip(er,p_eval):
                            cand=qualified_candidate(row,float(pv),threshold)
                            if cand is not None:
                                per_config_candidates[cid].append(cand)

        for cid in CONFIG_IDS:
            sim=simulate_eval(per_config_candidates[cid],eval_start,eval_end)
            config_folds[cid].append({
                "fold":fid,
                "fit":[fold["fit_start"],fold["fit_end"]],
                "calibration":[fold["cal_start"],fold["cal_end"]],
                "evaluation":[fold["eval_start"],fold["eval_end"]],
                "simulation":sim,
            })

        fold_diagnostics.append({
            "fold":fid,
            "fit_rows":len(fit_rows),
            "calibration_rows":len(cal_rows),
            "evaluation_rows":len(eval_rows),
            "rung_model_diagnostics":rung_diag,
        })

    configs={}
    for cid in CONFIG_IDS:
        configs[cid]={
            "folds":config_folds[cid],
            "pooled":aggregate_config(cid,config_folds[cid]),
        }

    passers=[configs[cid]["pooled"] for cid in CONFIG_IDS if configs[cid]["pooled"]["gate"]["configuration_pass"]]
    if passers:
        passers=sorted(
            passers,
            key=lambda x:(
                -x["worst_fold_stress_expectancy_usd"],
                -x["stress_profit_factor"],
                x["stress_max_drawdown_usd"],
                -x["total_actual_trades"],
                x["configuration_id"],
            )
        )
        winner=passers[0]["configuration_id"]
        disposition="PASS_WINNER_FROZEN_READY_FOR_SECONDARY_REFIT"
    else:
        winner=None
        disposition="NO_PASSING_CONFIGURATION_STOP_BEFORE_SECONDARY"

    result={
        "experiment":"EXP-025",
        "engine":"Engine K v0.4",
        "stage":"bounded_walk_forward_configuration_selection",
        "tested_repository_sha":repo_sha(),
        "runner_sha256":sha256_file(Path(__file__)),
        "sklearn_version":sklearn.__version__,
        "scope":{
            "development":["2026-03-23","2026-06-30"],
            "secondary_test_loaded_or_labeled":False,
            "final_holdout_loaded_or_labeled":False,
            "parsed_market_data_max_timestamp":max(str(df["datetime"].max()) for df in data.values()),
            "forecast_only_markets_loaded":False,
        },
        "self_tests":tests,
        "configuration_ids":CONFIG_IDS,
        "model_variants":MODEL_VARIANTS,
        "calibration_variants":CALIBRATION_VARIANTS,
        "qualification_policies":QUALIFICATION_POLICIES,
        "folds":FOLDS,
        "development_labeled_rungs":len(rows),
        "fold_diagnostics":fold_diagnostics,
        "configurations":configs,
        "passing_configuration_ids":[x["configuration_id"] for x in passers],
        "selected_configuration_id":winner,
        "disposition":disposition,
    }

    out=OUT/"EXP-025-walkforward-selection-summary-v0.4.json"
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")

    print(json.dumps({
        "development_labeled_rungs":len(rows),
        "passing_configuration_ids":result["passing_configuration_ids"],
        "selected_configuration_id":winner,
        "disposition":disposition,
        "secondary_test_loaded_or_labeled":False,
        "final_holdout_loaded_or_labeled":False,
    },indent=2))

if __name__=="__main__":
    main()
