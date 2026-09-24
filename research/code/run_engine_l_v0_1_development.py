#!/usr/bin/env python3
"""EXP-026 Engine L v0.1 six-fold development versus matched immediate-entry control.

Development only:
- Mar23-Jun30 reusable evidence
- Jul-Aug secondary never loaded/labeled
- Sep final holdout never loaded/labeled
"""

from __future__ import annotations

import hashlib
import json
import math
import statistics
import subprocess
from collections import Counter
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score

from engine_k_v0_1 import (
    EXECUTION_MARKETS,
    build_context,
    _latest_confirmed_pivot,
    next_active_entry,
    latest_completed_hour_context,
    causal_state_features,
    rung_features,
    usd_value_per_native_unit_1lot,
    download_pinned,
)
from engine_k_v0_2 import candidate_economics_v02, research_tick
from engine_l_v0_1 import find_micro_entry, self_tests_engine_l
from run_engine_k_v0_2_training_calibration import (
    load_scoped_csv,
    label_target_first,
    label_self_tests,
    encode_rows,
    max_drawdown,
)
from run_engine_k_v0_4_walkforward_selection import MODEL_VARIANTS

ROOT=Path(__file__).resolve().parents[2]
CACHE=Path("/tmp/engine-l-v01-development")
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

DEV_START=pd.Timestamp("2026-03-23",tz="UTC")
SEALED_START=pd.Timestamp("2026-07-01",tz="UTC")
M2_PARAMS=MODEL_VARIANTS["M2"]
T40="T40"

FOLDS=(
    {"id":"WF1","fit_start":"2026-03-23","fit_end":"2026-04-06","eval_start":"2026-04-13","eval_end":"2026-04-27"},
    {"id":"WF2","fit_start":"2026-03-23","fit_end":"2026-04-20","eval_start":"2026-04-27","eval_end":"2026-05-11"},
    {"id":"WF3","fit_start":"2026-03-23","fit_end":"2026-05-04","eval_start":"2026-05-11","eval_end":"2026-05-25"},
    {"id":"WF4","fit_start":"2026-03-23","fit_end":"2026-05-18","eval_start":"2026-05-25","eval_end":"2026-06-08"},
    {"id":"WF5","fit_start":"2026-03-23","fit_end":"2026-06-01","eval_start":"2026-06-08","eval_end":"2026-06-22"},
    {"id":"WF6","fit_start":"2026-03-23","fit_end":"2026-06-15","eval_start":"2026-06-22","eval_end":"2026-07-01"},
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
    # Finite JSON-safe representation of an effectively infinite no-loss PF.
    return 1_000_000_000.0 if wins else None


def stress_be(gross:float,risk:float,stress_cost:float)->float:
    return float((risk+stress_cost)/(gross+risk))


def build_t40_rows(
    symbol:str,
    df1:pd.DataFrame,
    usd_jpy_df:Optional[pd.DataFrame]=None,
)->list[dict]:
    """Matched forecast/control domain: old T40 pre-probability economic admission."""
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
        if decision_end>=SEALED_START:
            break
        if decision_end<DEV_START or decision_end.weekday()>=5:
            continue
        if decision_end.hour>=20:
            continue
        v5=float(bar["median_tr20_5m"]) if pd.notna(bar["median_tr20_5m"]) else math.nan
        if not math.isfinite(v5) or v5<=0:
            continue

        hc=latest_completed_hour_context(h1,decision_end)
        if hc is None:
            continue
        nxt=next_active_entry(df1,decision_start)
        if nxt is None:
            continue
        entry_ts,entry=nxt
        if entry_ts.date()!=decision_start.date() or entry_ts>=decision_end.normalize()+pd.Timedelta(hours=20):
            continue

        usd_jpy=None
        if symbol=="EURJPY" and usd_jpy_series is not None:
            k=int(usd_jpy_series.index.searchsorted(entry_ts,side="right"))-1
            if k>=0:
                usd_jpy=float(usd_jpy_series.iloc[k])

        for direction in ("long","short"):
            pivot=_latest_confirmed_pivot(b5,i,direction)
            if pivot is None:
                continue
            old_stop=pivot-tick if direction=="long" else pivot+tick
            if direction=="long" and not old_stop<entry:
                continue
            if direction=="short" and not old_stop>entry:
                continue

            common=causal_state_features(symbol,b5,i,direction,entry,old_stop,hc)
            if common is None:
                continue
            econ=candidate_economics_v02(symbol,entry,old_stop,usd_jpy)
            e=econ.get(T40)
            if not e or not e.get("execution_admissible_pre_probability",False):
                continue

            v=usd_value_per_native_unit_1lot(symbol,entry,usd_jpy)
            if v is None or v<=0:
                continue

            outcome=label_target_first(
                df1=df1,
                entry_ts=entry_ts,
                entry=entry,
                stop=old_stop,
                direction=direction,
                target_distance=float(e["distance"]),
                lot=float(e["lot"]),
                usd_value_per_native_unit=float(v),
                primary_cost_usd=float(e["primary_cost_usd"]),
                stress_cost_usd=float(e["stress_cost_usd"]),
            )
            features=rung_features(common,e)
            rows.append({
                "symbol":symbol,
                "direction":direction,
                "rung":T40,
                "decision_ts":decision_end,
                "decision_close":float(bar["close"]),
                "v5":v5,
                "entry_ts":entry_ts,
                "entry":float(entry),
                "stop":float(old_stop),
                "target_distance":float(e["distance"]),
                "gross_target_usd_actual":float(e["gross_target_usd_actual"]),
                "lot":float(e["lot"]),
                "stop_risk_usd":float(e["stop_risk_usd"]),
                "primary_cost_usd":float(e["primary_cost_usd"]),
                "stress_cost_usd":float(e["stress_cost_usd"]),
                "stress_break_even_probability":stress_be(
                    float(e["gross_target_usd_actual"]),
                    float(e["stop_risk_usd"]),
                    float(e["stress_cost_usd"]),
                ),
                **outcome,
                "features":features,
            })
    return rows


def choose_arms_for_fold(
    model,
    eval_rows:list[dict],
    data:dict[str,pd.DataFrame],
)->tuple[list[dict],dict]:
    """Create causal one-pending-arm-per-symbol forecast arms and both entry candidates."""
    x=encode_rows(eval_rows)
    probs=model.predict_proba(x)[:,1]
    scored=[]
    for r,p in zip(eval_rows,probs):
        z=dict(r)
        z["raw_forecast_probability"]=float(p)
        scored.append(z)

    grouped={}
    for r in scored:
        grouped.setdefault((r["symbol"],r["decision_ts"]),[]).append(r)

    usd_jpy_series=data["USDJPY"].set_index("datetime")["close"].sort_index()
    pending_until={s:pd.Timestamp.min.tz_localize("UTC") for s in EXECUTION_MARKETS}
    arms=[]
    statuses=Counter()
    blocked_decisions=0

    for symbol in EXECUTION_MARKETS:
        keys=sorted(k for k in grouped if k[0]==symbol)
        for key in keys:
            decision_ts=key[1]
            if decision_ts<pending_until[symbol]:
                blocked_decisions+=1
                continue

            sides=grouped[key]
            # Raw probability, then lower old stop risk, then LONG before SHORT.
            sides=sorted(
                sides,
                key=lambda r:(
                    -r["raw_forecast_probability"],
                    r["stop_risk_usd"],
                    0 if r["direction"]=="long" else 1,
                ),
            )
            chosen=sides[0]
            micro=find_micro_entry(
                df1=data[symbol],
                decision_end=chosen["decision_ts"],
                decision_close=chosen["decision_close"],
                v5=chosen["v5"],
                direction=chosen["direction"],
                old_invalidation=chosen["stop"],
                symbol=symbol,
                usd_jpy_series=usd_jpy_series if symbol=="EURJPY" else None,
            )
            if "resolved_ts" not in micro:
                raise RuntimeError("Engine L arm result missing resolved_ts")
            pending_until[symbol]=micro["resolved_ts"]
            statuses[micro["status"]]+=1

            control=dict(chosen)
            control["candidate_type"]="control"
            control["forecast_arm_id"]=f'{symbol}|{decision_ts.isoformat()}'
            control["forecast_probability"]=chosen["raw_forecast_probability"]

            micro_candidate=None
            if micro["status"]=="admissible_entry":
                entry_ts=micro["entry_ts"]
                entry=float(micro["entry"])
                stop=float(micro["stop"])
                entry_usd_jpy=None
                if symbol=="EURJPY":
                    k=int(usd_jpy_series.index.searchsorted(entry_ts,side="right"))-1
                    if k>=0:
                        entry_usd_jpy=float(usd_jpy_series.iloc[k])
                v=usd_value_per_native_unit_1lot(symbol,entry,entry_usd_jpy)
                if v is None or v<=0:
                    raise RuntimeError("entry-time value conversion unavailable")
                e=micro["t40"]
                outcome=label_target_first(
                    df1=data[symbol],
                    entry_ts=entry_ts,
                    entry=entry,
                    stop=stop,
                    direction=chosen["direction"],
                    target_distance=float(e["distance"]),
                    lot=float(e["lot"]),
                    usd_value_per_native_unit=float(v),
                    primary_cost_usd=float(e["primary_cost_usd"]),
                    stress_cost_usd=float(e["stress_cost_usd"]),
                )
                micro_candidate={
                    "candidate_type":"engine_l",
                    "forecast_arm_id":control["forecast_arm_id"],
                    "symbol":symbol,
                    "direction":chosen["direction"],
                    "decision_ts":chosen["decision_ts"],
                    "forecast_probability":chosen["raw_forecast_probability"],
                    "entry_ts":entry_ts,
                    "entry":entry,
                    "stop":stop,
                    "target_distance":float(e["distance"]),
                    "gross_target_usd_actual":float(e["gross_target_usd_actual"]),
                    "lot":float(e["lot"]),
                    "stop_risk_usd":float(e["stop_risk_usd"]),
                    "primary_cost_usd":float(e["primary_cost_usd"]),
                    "stress_cost_usd":float(e["stress_cost_usd"]),
                    "stress_break_even_probability":stress_be(
                        float(e["gross_target_usd_actual"]),
                        float(e["stop_risk_usd"]),
                        float(e["stress_cost_usd"]),
                    ),
                    **outcome,
                    "wait_active_m1_bars":int(micro["wait_active_m1_bars"]),
                    "pullback_depth_v5":float(micro["pullback_depth_v5"]),
                    "entry_directional_displacement_native":float(micro["entry_directional_displacement_from_decision"]),
                    "entry_directional_displacement_v5":float(micro["entry_directional_displacement_v5"]),
                    "entry_price_improvement_native":float(-micro["entry_directional_displacement_from_decision"]),
                    "entry_price_improvement_v5":float(-micro["entry_directional_displacement_v5"]),
                    "fresh_stop_distance_native":float(micro["fresh_stop_distance_native"]),
                    "old_stop_distance_native":abs(float(chosen["entry"])-float(chosen["stop"])),
                }

            arms.append({
                "arm_id":control["forecast_arm_id"],
                "symbol":symbol,
                "decision_ts":decision_ts,
                "direction":chosen["direction"],
                "forecast_probability":chosen["raw_forecast_probability"],
                "old_stop_risk_usd":chosen["stop_risk_usd"],
                "micro_status":micro["status"],
                "resolved_ts":micro["resolved_ts"],
                "pulled_back":bool(micro.get("pulled_back",False)),
                "resumption_confirmed":bool(micro.get("resumption_confirmed",False)),
                "micro_candidate":micro_candidate,
                "control_candidate":control,
            })

    diag={
        "forecast_arms":len(arms),
        "blocked_decisions_due_pending_arm":blocked_decisions,
        "arms_with_required_pullback":sum(a["pulled_back"] for a in arms),
        "arms_with_m1_resumption":sum(a["resumption_confirmed"] for a in arms),
        "micro_status_counts":dict(sorted(statuses.items())),
        "micro_admissible_entries":sum(a["micro_candidate"] is not None for a in arms),
        "control_candidates":len(arms),
    }
    return arms,diag


def portfolio_sim(candidates:list[dict],eval_start:pd.Timestamp,eval_end:pd.Timestamp)->dict:
    candidates=sorted(
        candidates,
        key=lambda r:(
            r["entry_ts"],
            -r["forecast_probability"],
            r["stop_risk_usd"],
            r["symbol"],
            0 if r["direction"]=="long" else 1,
        ),
    )
    by_entry={}
    for r in candidates:
        by_entry.setdefault(r["entry_ts"],[]).append(r)

    trades=[]
    daily={}
    last_exit=None
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
    weekdays=[
        d.date().isoformat()
        for d in pd.date_range(eval_start.normalize(),eval_end-pd.Timedelta(days=1),freq="D",tz="UTC")
        if d.weekday()<5
    ]
    market_counts={}
    for r in trades:
        market_counts[r["symbol"]]=market_counts.get(r["symbol"],0)+1
    max_share=max(market_counts.values())/len(trades) if trades else None

    return {
        "actual_trades":len(trades),
        "distinct_trade_weekdays":len(set(r["entry_ts"].date().isoformat() for r in trades)),
        "target_hits":int(sum(int(r["label"]) for r in trades)),
        "target_hit_rate":float(np.mean([r["label"] for r in trades])) if trades else None,
        "mean_stress_break_even_probability":float(np.mean([r["stress_break_even_probability"] for r in trades])) if trades else None,
        "primary_net_pnl_usd":float(sum(primary)),
        "stress_net_pnl_usd":float(sum(stress)),
        "primary_expectancy_usd":float(np.mean(primary)) if primary else None,
        "stress_expectancy_usd":float(np.mean(stress)) if stress else None,
        "primary_profit_factor":pf(primary),
        "stress_profit_factor":pf(stress),
        "primary_max_drawdown_usd":max_drawdown(primary),
        "stress_max_drawdown_usd":max_drawdown(stress),
        "market_trade_count":dict(sorted(market_counts.items())),
        "max_market_trade_share":float(max_share) if max_share is not None else None,
        "eligible_weekdays":len(weekdays),
        "zero_trade_weekdays":int(sum(d not in daily for d in weekdays)),
        "daily_primary_pnl":[{"date":d,"pnl":float(daily.get(d,0.0))} for d in weekdays],
        "trades":[{
            "arm_id":r["forecast_arm_id"],
            "entry_ts":str(r["entry_ts"]),
            "exit_ts":str(r["exit_ts"]),
            "symbol":r["symbol"],
            "direction":r["direction"],
            "forecast_probability":float(r["forecast_probability"]),
            "outcome":r["outcome"],
            "label":int(r["label"]),
            "primary_net_pnl_usd":float(r["primary_net_pnl_usd"]),
            "stress_net_pnl_usd":float(r["stress_net_pnl_usd"]),
            "stress_break_even_probability":float(r["stress_break_even_probability"]),
        } for r in trades],
    }


def aggregate_fold_sims(fold_results:list[dict],key:str)->dict:
    trades=[]
    for fr in fold_results:
        for t in fr[key]["trades"]:
            z=dict(t); z["fold"]=fr["fold"]; trades.append(z)
    trades.sort(key=lambda r:r["entry_ts"])
    primary=[t["primary_net_pnl_usd"] for t in trades]
    stress=[t["stress_net_pnl_usd"] for t in trades]
    market_counts={}
    for t in trades:
        market_counts[t["symbol"]]=market_counts.get(t["symbol"],0)+1
    max_share=max(market_counts.values())/len(trades) if trades else None
    fold_stress=[fr[key]["stress_expectancy_usd"] for fr in fold_results]

    return {
        "actual_trades":len(trades),
        "distinct_trade_weekdays":len(set(t["entry_ts"][:10] for t in trades)),
        "target_hits":int(sum(t["label"] for t in trades)),
        "target_hit_rate":float(np.mean([t["label"] for t in trades])) if trades else None,
        "mean_stress_break_even_probability":float(np.mean([t["stress_break_even_probability"] for t in trades])) if trades else None,
        "primary_net_pnl_usd":float(sum(primary)),
        "stress_net_pnl_usd":float(sum(stress)),
        "primary_expectancy_usd":float(np.mean(primary)) if primary else None,
        "stress_expectancy_usd":float(np.mean(stress)) if stress else None,
        "primary_profit_factor":pf(primary),
        "stress_profit_factor":pf(stress),
        "primary_max_drawdown_usd":max_drawdown(primary),
        "stress_max_drawdown_usd":max_drawdown(stress),
        "market_trade_count":dict(sorted(market_counts.items())),
        "max_market_trade_share":float(max_share) if max_share is not None else None,
        "positive_stress_expectancy_folds":sum(x is not None and x>0 for x in fold_stress),
        "fold_stress_expectancies":fold_stress,
        "fold_trade_counts":[fr[key]["actual_trades"] for fr in fold_results],
        "trades":trades,
    }


def self_tests_development()->list[str]:
    tests=[]
    assert len(FOLDS)==6
    for i,f in enumerate(FOLDS):
        fs,fe,es,ee=map(ts,[f["fit_start"],f["fit_end"],f["eval_start"],f["eval_end"]])
        assert fs==DEV_START and fs<fe<es<ee<=SEALED_START
        if i:
            assert ts(FOLDS[i-1]["eval_end"])==es
    tests.append("six_frozen_forward_folds")
    assert M2_PARAMS["max_leaf_nodes"]==7 and M2_PARAMS["min_samples_leaf"]==250
    tests.append("fixed_m2_forecast")
    assert ts(FOLDS[-1]["eval_end"])==SEALED_START
    tests.append("july_seal")
    return tests


def main():
    preflight_path=OUT/"EXP-026-entry-mechanics-preflight-v0.1.json"
    if not preflight_path.exists():
        raise RuntimeError("EXP-026 preflight missing")
    pre=json.loads(preflight_path.read_text())
    if not pre.get("preflight_pass"):
        raise RuntimeError("EXP-026 preflight did not pass")
    if pre.get("target_outcomes_calculated") or pre.get("pnl_outcomes_calculated"):
        raise RuntimeError("preflight was not zero-outcome")
    if pre.get("secondary_test_loaded_or_inspected") or pre.get("final_holdout_loaded_or_inspected"):
        raise RuntimeError("protected-period preflight seal failed")

    tests={
        "engine_l":self_tests_engine_l(),
        "label":label_self_tests(),
        "development":self_tests_development(),
    }

    data={}
    for symbol in EXECUTION_MARKETS:
        path=download_pinned(symbol,CACHE)
        df=load_scoped_csv(path,symbol,SEALED_START)
        if df.empty or df["datetime"].max()>=SEALED_START:
            raise RuntimeError(f"{symbol}: protected-period leak")
        data[symbol]=df

    rows=[]
    for symbol in EXECUTION_MARKETS:
        uj=data["USDJPY"] if symbol=="EURJPY" else None
        rows.extend(build_t40_rows(symbol,data[symbol],uj))
    if not rows:
        raise RuntimeError("no T40 forecast rows")

    fold_results=[]
    pooled_entry_records=[]
    for fold in FOLDS:
        fit_start,fit_end=ts(fold["fit_start"]),ts(fold["fit_end"])
        eval_start,eval_end=ts(fold["eval_start"]),ts(fold["eval_end"])

        fit_rows=[r for r in rows if fit_start<=r["decision_ts"]<fit_end]
        eval_rows=[r for r in rows if eval_start<=r["decision_ts"]<eval_end]
        if not fit_rows or not eval_rows:
            raise RuntimeError(f'{fold["id"]}: empty fit/eval')

        y_fit=np.asarray([r["label"] for r in fit_rows],dtype=int)
        y_eval=np.asarray([r["label"] for r in eval_rows],dtype=int)
        if len(np.unique(y_fit))!=2 or len(np.unique(y_eval))!=2:
            raise RuntimeError(f'{fold["id"]}: both classes required')

        model=HistGradientBoostingClassifier(**M2_PARAMS)
        model.fit(encode_rows(fit_rows),y_fit)
        eval_prob=model.predict_proba(encode_rows(eval_rows))[:,1]
        auc=safe_auc(y_eval,eval_prob)

        # choose_arms_for_fold predicts internally from the same frozen model.
        arms,arm_diag=choose_arms_for_fold(model,eval_rows,data)
        engine_candidates=[a["micro_candidate"] for a in arms if a["micro_candidate"] is not None]
        control_candidates=[a["control_candidate"] for a in arms]

        eng=portfolio_sim(engine_candidates,eval_start,eval_end)
        ctrl=portfolio_sim(control_candidates,eval_start,eval_end)

        micro_entries=[a["micro_candidate"] for a in arms if a["micro_candidate"] is not None]
        pooled_entry_records.extend(micro_entries)
        entry_diag={
            "admissible_micro_entries":len(micro_entries),
            "median_wait_active_m1_bars":statistics.median([x["wait_active_m1_bars"] for x in micro_entries]) if micro_entries else None,
            "median_entry_price_improvement_native":statistics.median([x["entry_price_improvement_native"] for x in micro_entries]) if micro_entries else None,
            "median_entry_price_improvement_v5":statistics.median([x["entry_price_improvement_v5"] for x in micro_entries]) if micro_entries else None,
            "median_fresh_stop_distance_native":statistics.median([x["fresh_stop_distance_native"] for x in micro_entries]) if micro_entries else None,
            "median_old_stop_distance_native":statistics.median([x["old_stop_distance_native"] for x in micro_entries]) if micro_entries else None,
        }

        fold_results.append({
            "fold":fold["id"],
            "fit":[fold["fit_start"],fold["fit_end"]],
            "evaluation":[fold["eval_start"],fold["eval_end"]],
            "fit_rows":len(fit_rows),
            "evaluation_rows":len(eval_rows),
            "raw_t40_evaluation_auc":auc,
            "arm_diagnostics":arm_diag,
            "entry_diagnostics":entry_diag,
            "engine_l":eng,
            "immediate_control":ctrl,
            "stress_expectancy_improvement_vs_control_usd":(
                eng["stress_expectancy_usd"]-ctrl["stress_expectancy_usd"]
                if eng["stress_expectancy_usd"] is not None and ctrl["stress_expectancy_usd"] is not None
                else None
            ),
        })

    pooled_engine=aggregate_fold_sims(fold_results,"engine_l")
    pooled_control=aggregate_fold_sims(fold_results,"immediate_control")

    pooled_status=Counter()
    for fr in fold_results:
        pooled_status.update(fr["arm_diagnostics"]["micro_status_counts"])
    pooled_arm_diagnostics={
        "forecast_arms":sum(fr["arm_diagnostics"]["forecast_arms"] for fr in fold_results),
        "blocked_decisions_due_pending_arm":sum(fr["arm_diagnostics"]["blocked_decisions_due_pending_arm"] for fr in fold_results),
        "arms_with_required_pullback":sum(fr["arm_diagnostics"]["arms_with_required_pullback"] for fr in fold_results),
        "arms_with_m1_resumption":sum(fr["arm_diagnostics"]["arms_with_m1_resumption"] for fr in fold_results),
        "micro_admissible_entries":sum(fr["arm_diagnostics"]["micro_admissible_entries"] for fr in fold_results),
        "control_candidates":sum(fr["arm_diagnostics"]["control_candidates"] for fr in fold_results),
        "micro_status_counts":dict(sorted(pooled_status.items())),
    }
    pooled_entry_diagnostics={
        "admissible_micro_entries":len(pooled_entry_records),
        "median_wait_active_m1_bars":statistics.median([x["wait_active_m1_bars"] for x in pooled_entry_records]) if pooled_entry_records else None,
        "median_entry_price_improvement_native":statistics.median([x["entry_price_improvement_native"] for x in pooled_entry_records]) if pooled_entry_records else None,
        "median_entry_price_improvement_v5":statistics.median([x["entry_price_improvement_v5"] for x in pooled_entry_records]) if pooled_entry_records else None,
        "median_fresh_stop_distance_native":statistics.median([x["fresh_stop_distance_native"] for x in pooled_entry_records]) if pooled_entry_records else None,
        "median_old_stop_distance_native":statistics.median([x["old_stop_distance_native"] for x in pooled_entry_records]) if pooled_entry_records else None,
    }
    improvement=(
        pooled_engine["stress_expectancy_usd"]-pooled_control["stress_expectancy_usd"]
        if pooled_engine["stress_expectancy_usd"] is not None and pooled_control["stress_expectancy_usd"] is not None
        else None
    )
    better_folds=sum(
        fr["stress_expectancy_improvement_vs_control_usd"] is not None
        and fr["stress_expectancy_improvement_vs_control_usd"]>0
        for fr in fold_results
    )

    gate={
        "pooled_actual_trades_ge_90":pooled_engine["actual_trades"]>=90,
        "every_fold_trades_ge_6":all(x>=6 for x in pooled_engine["fold_trade_counts"]),
        "distinct_trade_weekdays_ge_35":pooled_engine["distinct_trade_weekdays"]>=35,
        "pooled_primary_expectancy_gt_0":pooled_engine["primary_expectancy_usd"] is not None and pooled_engine["primary_expectancy_usd"]>0,
        "pooled_stress_expectancy_gt_0":pooled_engine["stress_expectancy_usd"] is not None and pooled_engine["stress_expectancy_usd"]>0,
        "primary_pf_ge_1_10":pooled_engine["primary_profit_factor"] is not None and pooled_engine["primary_profit_factor"]>=1.10,
        "stress_pf_ge_1_05":pooled_engine["stress_profit_factor"] is not None and pooled_engine["stress_profit_factor"]>=1.05,
        "hit_rate_above_mean_stress_break_even":bool(
            pooled_engine["target_hit_rate"] is not None
            and pooled_engine["mean_stress_break_even_probability"] is not None
            and pooled_engine["target_hit_rate"]>pooled_engine["mean_stress_break_even_probability"]
        ),
        "positive_stress_expectancy_folds_ge_4":pooled_engine["positive_stress_expectancy_folds"]>=4,
        "pooled_stress_max_drawdown_le_150":pooled_engine["stress_max_drawdown_usd"]<=150,
        "max_market_share_le_60pct":pooled_engine["max_market_trade_share"] is not None and pooled_engine["max_market_trade_share"]<=0.60,
        "stress_expectancy_beats_control_by_ge_2":improvement is not None and improvement>=2.0,
        "stress_expectancy_better_than_control_in_ge_4_folds":better_folds>=4,
        "causality_same_bar_provenance_integrity":True,
        "secondary_and_final_holdout_sealed":True,
    }
    gate["final_development_gate"]=bool(all(gate.values()))

    result={
        "experiment":"EXP-026",
        "engine":"Engine L v0.1",
        "stage":"six_fold_development_vs_matched_immediate_control",
        "tested_repository_sha":repo_sha(),
        "engine_l_sha256":sha256_file(ROOT/"research/code/engine_l_v0_1.py"),
        "runner_sha256":sha256_file(Path(__file__)),
        "sklearn_version":sklearn.__version__,
        "scope":{
            "development":["2026-03-23","2026-06-30"],
            "secondary_test_loaded_or_labeled":False,
            "final_holdout_loaded_or_labeled":False,
            "parsed_market_data_max_timestamp":max(str(df["datetime"].max()) for df in data.values()),
            "forecast_only_markets_loaded":False,
        },
        "tests":tests,
        "forecast_domain":"matched Engine-K-v0.2/v0.3 pre-probability T40 economic domain",
        "fixed_model_params":M2_PARAMS,
        "development_t40_rows":len(rows),
        "folds":fold_results,
        "pooled_arm_diagnostics":pooled_arm_diagnostics,
        "pooled_entry_diagnostics":pooled_entry_diagnostics,
        "pooled_engine_l":pooled_engine,
        "pooled_immediate_control":pooled_control,
        "pooled_stress_expectancy_improvement_vs_control_usd":improvement,
        "folds_engine_l_stress_better_than_control":better_folds,
        "development_gate":gate,
        "disposition":"PASS_READY_FOR_SECONDARY_DESIGN" if gate["final_development_gate"] else "FAIL_STOP_BEFORE_SECONDARY",
    }

    out=OUT/"EXP-026-development-summary-v0.1.json"
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")
    print(json.dumps({
        "development_t40_rows":len(rows),
        "pooled_engine_l":{
            k:pooled_engine[k] for k in [
                "actual_trades","distinct_trade_weekdays","target_hit_rate",
                "primary_expectancy_usd","stress_expectancy_usd",
                "primary_profit_factor","stress_profit_factor",
                "stress_max_drawdown_usd","positive_stress_expectancy_folds"
            ]
        },
        "pooled_control":{
            k:pooled_control[k] for k in [
                "actual_trades","target_hit_rate","primary_expectancy_usd",
                "stress_expectancy_usd","primary_profit_factor","stress_profit_factor"
            ]
        },
        "stress_expectancy_improvement_vs_control_usd":improvement,
        "folds_better_than_control":better_folds,
        "gate":gate,
        "disposition":result["disposition"],
        "secondary_test_loaded_or_labeled":False,
        "final_holdout_loaded_or_labeled":False,
    },indent=2))


if __name__=="__main__":
    main()
