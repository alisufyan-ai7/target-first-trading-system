#!/usr/bin/env python3
"""EXP-028 Engine M v0.2 development.

Evaluates:
1) size-invariant signal edge on all causal filled Engine-M signals; and
2) separate safe-lot USD500 reference-account portfolio.

Development only through 2026-06-30. Jul-Aug and Sep remain sealed.
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

from engine_k_v0_1 import (
    EXECUTION_MARKETS,
    MAX_NEXT_ENTRY_GAP_MINUTES,
    PRIMARY_COST_FRACTION_OF_GROSS_TARGET,
    STRESS_COST_FRACTION_OF_GROSS_TARGET,
    download_pinned,
    usd_value_per_native_unit_1lot,
)
from engine_k_v0_2 import native_target_distances_v02, research_costs_v02, research_tick
from engine_m_v0_1 import build_mtf_bars, mtf_setup_at, find_limit_fill, self_tests_engine_m
from engine_m_v0_2 import safe_deployability_overlay, self_tests_engine_m_v02
from run_engine_k_v0_2_training_calibration import (
    load_scoped_csv,
    label_target_first,
    label_self_tests,
    max_drawdown,
)
from run_engine_m_v0_1_preflight import synthetic_setup_tests, synthetic_fill_tests

ROOT=Path(__file__).resolve().parents[2]
CACHE=Path("/tmp/engine-m-v02-development")
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

START=pd.Timestamp("2026-03-23",tz="UTC")
SEALED_START=pd.Timestamp("2026-07-01",tz="UTC")

FOLDS=(
    {"id":"WF1","eval_start":"2026-04-13","eval_end":"2026-04-27"},
    {"id":"WF2","eval_start":"2026-04-27","eval_end":"2026-05-11"},
    {"id":"WF3","eval_start":"2026-05-11","eval_end":"2026-05-25"},
    {"id":"WF4","eval_start":"2026-05-25","eval_end":"2026-06-08"},
    {"id":"WF5","eval_start":"2026-06-08","eval_end":"2026-06-22"},
    {"id":"WF6","eval_start":"2026-06-22","eval_end":"2026-07-01"},
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


def pf(seq):
    wins=[float(x) for x in seq if x>0]
    losses=[float(x) for x in seq if x<0]
    if losses:
        return float(sum(wins)/abs(sum(losses)))
    return 1_000_000_000.0 if wins else None


def first_active_open(df1:pd.DataFrame,decision_ts:pd.Timestamp):
    k=int(df1["datetime"].searchsorted(decision_ts,side="left"))
    if k>=len(df1):
        return None
    row=df1.iloc[k]
    entry_ts=row["datetime"]
    if entry_ts-decision_ts>pd.Timedelta(minutes=MAX_NEXT_ENTRY_GAP_MINUTES):
        return None
    return entry_ts,float(row["open"])


def entry_usd_jpy_at(series:Optional[pd.Series],entry_ts:pd.Timestamp)->Optional[float]:
    if series is None:
        return None
    k=int(series.index.searchsorted(entry_ts,side="right"))-1
    if k<0:
        return None
    return float(series.iloc[k])


def signal_and_account_labels(
    symbol:str,
    df1:pd.DataFrame,
    direction:str,
    entry_ts:pd.Timestamp,
    entry:float,
    stop:float,
    usd_jpy:Optional[float],
    overlay:dict,
)->dict:
    distances=native_target_distances_v02(symbol,entry,stop)
    if "T40" not in distances:
        raise RuntimeError("T40 target geometry unavailable")
    target_distance=float(distances["T40"])

    v=usd_value_per_native_unit_1lot(symbol,entry,usd_jpy)
    if v is None or v<=0:
        raise RuntimeError("USD value unavailable")

    # Size-invariant label: use 1 lot and normalize all P&L by 1-lot initial risk.
    gross_target_1lot=target_distance*v
    c1=research_costs_v02(gross_target_1lot)
    unit=label_target_first(
        df1=df1,
        entry_ts=entry_ts,
        entry=entry,
        stop=stop,
        direction=direction,
        target_distance=target_distance,
        lot=1.0,
        usd_value_per_native_unit=v,
        primary_cost_usd=float(c1["primary_cost_usd"]),
        stress_cost_usd=float(c1["stress_cost_usd"]),
    )
    unit_risk=abs(entry-stop)*v
    if unit_risk<=0:
        raise RuntimeError("zero unit risk")

    normalized={
        "label":int(unit["label"]),
        "outcome":unit["outcome"],
        "exit_ts":unit["exit_ts"],
        "active_m1_bars":int(unit["active_m1_bars"]),
        "gross_r":float(unit["gross_pnl_usd"]/unit_risk),
        "primary_r":float(unit["primary_net_pnl_usd"]/unit_risk),
        "stress_r":float(unit["stress_net_pnl_usd"]/unit_risk),
        "reward_multiple":float(target_distance/abs(entry-stop)),
    }

    account=None
    if overlay.get("deployable") and float(overlay.get("safe_lot",0.0))>=0.01:
        lot=float(overlay["safe_lot"])
        account=label_target_first(
            df1=df1,
            entry_ts=entry_ts,
            entry=entry,
            stop=stop,
            direction=direction,
            target_distance=target_distance,
            lot=lot,
            usd_value_per_native_unit=v,
            primary_cost_usd=float(overlay["primary_cost_usd"]),
            stress_cost_usd=float(overlay["stress_cost_usd"]),
        )
    return {
        "target_distance":target_distance,
        "normalized":normalized,
        "account":account,
    }


def scan_market(
    symbol:str,
    df1:pd.DataFrame,
    usd_jpy_df:Optional[pd.DataFrame]=None,
)->dict:
    bars=build_mtf_bars(df1)
    usd_jpy_series=None
    if usd_jpy_df is not None:
        usd_jpy_series=usd_jpy_df.set_index("datetime")["close"].sort_index()

    pending_until=pd.Timestamp.min.tz_localize("UTC")
    status=Counter()
    blocked=0
    arms=[]
    signals=[]
    controls=[]

    for i in range(len(bars["m15"])):
        decision_ts=bars["m15"].iloc[i]["available_ts"]
        if decision_ts<START or decision_ts>=SEALED_START:
            continue
        if decision_ts.weekday()>=5 or decision_ts.hour>=18:
            continue

        setup=mtf_setup_at(bars,i)
        status[setup["status"]]+=1
        if setup["status"]!="armed":
            continue
        if decision_ts<pending_until:
            blocked+=1
            continue

        # Same MTF arm drives both Engine-M limit entry and matched immediate control.
        fill=find_limit_fill(df1,setup,symbol,usd_jpy_series)
        pending_until=fill["resolved_ts"]

        direction=setup["direction"]
        stop=float(setup["a5_low"]-research_tick(symbol)) if direction=="long" else float(setup["a5_high"]+research_tick(symbol))
        arm_id=f"{symbol}|{decision_ts.isoformat()}|{direction}"

        arm={
            "arm_id":arm_id,
            "symbol":symbol,
            "direction":direction,
            "decision_ts":decision_ts,
            "stop":stop,
            "limit_status":fill["status"],
            "limit_filled":bool(fill.get("filled",False)),
        }

        # Engine-M signal if the precomputed limit actually filled.
        if fill.get("filled"):
            entry_ts=fill["entry_ts"]
            entry=float(fill["entry"])
            uj=entry_usd_jpy_at(usd_jpy_series,entry_ts) if symbol=="EURJPY" else None
            overlay=safe_deployability_overlay(symbol,entry,stop,uj)
            if overlay.get("reason") not in (
                "invalid_geometry","value_or_notional_unavailable",
                "target_geometry_unavailable","invalid_stop_loss_per_lot"
            ):
                labels=signal_and_account_labels(
                    symbol,df1,direction,entry_ts,entry,stop,uj,overlay
                )
                signals.append({
                    "arm_id":arm_id,
                    "symbol":symbol,
                    "direction":direction,
                    "decision_ts":decision_ts,
                    "entry_ts":entry_ts,
                    "entry":entry,
                    "stop":stop,
                    "wait_active_m1_bars":int(fill["wait_active_m1_bars"]),
                    "entry_improvement_a5_range":float(fill["entry_improvement_a5_range"]),
                    "safe_overlay":overlay,
                    **labels,
                })

        # Matched immediate-entry control on the same accepted MTF arm.
        nxt=first_active_open(df1,decision_ts)
        if nxt is not None:
            ctrl_ts,ctrl_entry=nxt
            valid=(stop<ctrl_entry) if direction=="long" else (stop>ctrl_entry)
            if valid:
                uj=entry_usd_jpy_at(usd_jpy_series,ctrl_ts) if symbol=="EURJPY" else None
                ctrl_overlay=safe_deployability_overlay(symbol,ctrl_entry,stop,uj)
                if ctrl_overlay.get("reason") not in (
                    "invalid_geometry","value_or_notional_unavailable",
                    "target_geometry_unavailable","invalid_stop_loss_per_lot"
                ):
                    labels=signal_and_account_labels(
                        symbol,df1,direction,ctrl_ts,ctrl_entry,stop,uj,ctrl_overlay
                    )
                    controls.append({
                        "arm_id":arm_id,
                        "symbol":symbol,
                        "direction":direction,
                        "decision_ts":decision_ts,
                        "entry_ts":ctrl_ts,
                        "entry":ctrl_entry,
                        "stop":stop,
                        "safe_overlay":ctrl_overlay,
                        **labels,
                    })

        arms.append(arm)

    return {
        "setup_status_counts":dict(sorted(status.items())),
        "blocked_due_pending_order":blocked,
        "arms":arms,
        "signals":signals,
        "controls":controls,
    }


def signal_metrics(rows:list[dict])->dict:
    primary=[float(r["normalized"]["primary_r"]) for r in rows]
    stress=[float(r["normalized"]["stress_r"]) for r in rows]
    gross=[float(r["normalized"]["gross_r"]) for r in rows]
    markets=Counter(r["symbol"] for r in rows)
    directions=Counter(r["direction"] for r in rows)

    per_market={}
    for symbol in sorted(markets):
        rr=[r for r in rows if r["symbol"]==symbol]
        pg=[float(r["normalized"]["gross_r"]) for r in rr]
        pp=[float(r["normalized"]["primary_r"]) for r in rr]
        ps=[float(r["normalized"]["stress_r"]) for r in rr]
        per_market[symbol]={
            "signals":len(rr),
            "target_hit_rate":float(np.mean([r["normalized"]["label"] for r in rr])) if rr else None,
            "gross_r_expectancy":float(np.mean(pg)) if pg else None,
            "primary_r_expectancy":float(np.mean(pp)) if pp else None,
            "stress_r_expectancy":float(np.mean(ps)) if ps else None,
            "primary_r_profit_factor":pf(pp),
            "stress_r_profit_factor":pf(ps),
            "long":int(sum(r["direction"]=="long" for r in rr)),
            "short":int(sum(r["direction"]=="short" for r in rr)),
        }

    return {
        "signals":len(rows),
        "target_hits":int(sum(r["normalized"]["label"] for r in rows)),
        "target_hit_rate":float(np.mean([r["normalized"]["label"] for r in rows])) if rows else None,
        "gross_r_expectancy":float(np.mean(gross)) if gross else None,
        "primary_r_expectancy":float(np.mean(primary)) if primary else None,
        "stress_r_expectancy":float(np.mean(stress)) if stress else None,
        "primary_r_profit_factor":pf(primary),
        "stress_r_profit_factor":pf(stress),
        "market_counts":dict(sorted(markets.items())),
        "per_market":per_market,
        "direction_counts":dict(sorted(directions.items())),
        "max_market_share":float(max(markets.values())/len(rows)) if rows else None,
        "median_wait_active_m1_bars":statistics.median([r.get("wait_active_m1_bars",0) for r in rows]) if rows and "wait_active_m1_bars" in rows[0] else None,
        "median_entry_improvement_a5_range":statistics.median([r.get("entry_improvement_a5_range",0.0) for r in rows]) if rows and "entry_improvement_a5_range" in rows[0] else None,
    }


def portfolio_sim(candidates:list[dict],eval_start:pd.Timestamp,eval_end:pd.Timestamp)->dict:
    rows=[]
    for r in candidates:
        acc=r.get("account")
        ov=r["safe_overlay"]
        if acc is None or not ov.get("deployable") or float(ov.get("safe_lot",0.0))<0.01:
            continue
        x=dict(r)
        x["_account"]=acc
        rows.append(x)

    rows.sort(key=lambda r:(
        r["entry_ts"],
        -float(r["safe_overlay"]["gross_target_usd"]),
        float(r["safe_overlay"]["stop_risk_usd"]),
        r["symbol"],
        0 if r["direction"]=="long" else 1,
    ))

    by_entry={}
    for r in rows:
        by_entry.setdefault(r["entry_ts"],[]).append(r)

    trades=[]
    daily={}
    last_exit=None
    for entry_ts in sorted(by_entry):
        if last_exit is not None and entry_ts<=last_exit:
            continue
        day=entry_ts.date().isoformat()
        realized=daily.get(day,0.0)
        if realized<=-40.0 or realized>=150.0:
            continue
        r=by_entry[entry_ts][0]
        acc=r["_account"]
        trade={
            "arm_id":r["arm_id"],
            "symbol":r["symbol"],
            "direction":r["direction"],
            "entry_ts":r["entry_ts"],
            "exit_ts":acc["exit_ts"],
            "label":int(acc["label"]),
            "outcome":acc["outcome"],
            "primary_net_pnl_usd":float(acc["primary_net_pnl_usd"]),
            "stress_net_pnl_usd":float(acc["stress_net_pnl_usd"]),
            "gross_target_usd":float(r["safe_overlay"]["gross_target_usd"]),
            "stop_risk_usd":float(r["safe_overlay"]["stop_risk_usd"]),
            "safe_lot":float(r["safe_overlay"]["safe_lot"]),
            "utility_band":r["safe_overlay"]["utility_band"],
        }
        trades.append(trade)
        daily[day]=realized+trade["primary_net_pnl_usd"]
        last_exit=acc["exit_ts"]

    primary=[t["primary_net_pnl_usd"] for t in trades]
    stress=[t["stress_net_pnl_usd"] for t in trades]
    eligible=[
        d.date().isoformat()
        for d in pd.date_range(
            eval_start.normalize(),
            eval_end-pd.Timedelta(days=1),
            freq="D",tz="UTC"
        )
        if d.weekday()<5
    ]
    market_counts=Counter(t["symbol"] for t in trades)
    bands=Counter(t["utility_band"] for t in trades)
    final_daily=[float(daily.get(d,0.0)) for d in eligible]
    return {
        "actual_trades":len(trades),
        "distinct_trade_weekdays":len(set(t["entry_ts"].date().isoformat() for t in trades)),
        "target_hits":int(sum(t["label"] for t in trades)),
        "target_hit_rate":float(np.mean([t["label"] for t in trades])) if trades else None,
        "primary_net_pnl_usd":float(sum(primary)),
        "stress_net_pnl_usd":float(sum(stress)),
        "primary_expectancy_usd":float(np.mean(primary)) if primary else None,
        "stress_expectancy_usd":float(np.mean(stress)) if stress else None,
        "primary_profit_factor":pf(primary),
        "stress_profit_factor":pf(stress),
        "primary_max_drawdown_usd":max_drawdown(primary),
        "stress_max_drawdown_usd":max_drawdown(stress),
        "market_trade_count":dict(sorted(market_counts.items())),
        "max_market_trade_share":float(max(market_counts.values())/len(trades)) if trades else None,
        "utility_band_trade_count":dict(sorted(bands.items())),
        "eligible_weekdays":len(eligible),
        "zero_trade_weekdays":int(sum(v==0.0 for v in final_daily)),
        "weekdays_final_pnl_ge_100":int(sum(v>=100.0 for v in final_daily)),
        "weekdays_final_pnl_ge_150":int(sum(v>=150.0 for v in final_daily)),
        "pct_weekdays_final_pnl_ge_100":float(np.mean([v>=100.0 for v in final_daily])) if final_daily else None,
        "pct_weekdays_final_pnl_ge_150":float(np.mean([v>=150.0 for v in final_daily])) if final_daily else None,
        "daily_primary_pnl":[{"date":d,"pnl":float(daily.get(d,0.0))} for d in eligible],
        "trades":trades,
    }


def aggregate_portfolios(folds:list[dict],key:str)->dict:
    trades=[]
    daily=[]
    for fr in folds:
        trades.extend(fr[key]["trades"])
        daily.extend(fr[key]["daily_primary_pnl"])
    trades.sort(key=lambda x:x["entry_ts"])
    primary=[t["primary_net_pnl_usd"] for t in trades]
    stress=[t["stress_net_pnl_usd"] for t in trades]
    market_counts=Counter(t["symbol"] for t in trades)
    bands=Counter(t["utility_band"] for t in trades)
    vals=[float(x["pnl"]) for x in daily]
    return {
        "actual_trades":len(trades),
        "distinct_trade_weekdays":len(set(t["entry_ts"][:10] for t in trades)),
        "target_hits":int(sum(t["label"] for t in trades)),
        "target_hit_rate":float(np.mean([t["label"] for t in trades])) if trades else None,
        "primary_net_pnl_usd":float(sum(primary)),
        "stress_net_pnl_usd":float(sum(stress)),
        "primary_expectancy_usd":float(np.mean(primary)) if primary else None,
        "stress_expectancy_usd":float(np.mean(stress)) if stress else None,
        "primary_profit_factor":pf(primary),
        "stress_profit_factor":pf(stress),
        "primary_max_drawdown_usd":max_drawdown(primary),
        "stress_max_drawdown_usd":max_drawdown(stress),
        "market_trade_count":dict(sorted(market_counts.items())),
        "max_market_trade_share":float(max(market_counts.values())/len(trades)) if trades else None,
        "utility_band_trade_count":dict(sorted(bands.items())),
        "eligible_weekdays":len(daily),
        "zero_trade_weekdays":int(sum(v==0.0 for v in vals)),
        "weekdays_final_pnl_ge_100":int(sum(v>=100.0 for v in vals)),
        "weekdays_final_pnl_ge_150":int(sum(v>=150.0 for v in vals)),
        "pct_weekdays_final_pnl_ge_100":float(np.mean([v>=100.0 for v in vals])) if vals else None,
        "pct_weekdays_final_pnl_ge_150":float(np.mean([v>=150.0 for v in vals])) if vals else None,
        "fold_trade_counts":[fr[key]["actual_trades"] for fr in folds],
        "trades":trades,
    }


def self_tests_development()->list[str]:
    tests=[]
    assert len(FOLDS)==6
    for i,f in enumerate(FOLDS):
        s,e=ts(f["eval_start"]),ts(f["eval_end"])
        assert START<s<e<=SEALED_START
        if i:
            assert ts(FOLDS[i-1]["eval_end"])==s
    assert ts(FOLDS[-1]["eval_end"])==SEALED_START
    tests.append("six_fixed_development_slices")
    tests.append("july_seal")
    return tests


def main():
    pre_path=OUT/"EXP-028-signal-first-preflight-v0.2.json"
    if not pre_path.exists():
        raise RuntimeError("EXP-028 preflight result missing")
    pre=json.loads(pre_path.read_text())
    if pre.get("preflight_pass") is not True:
        raise RuntimeError("EXP-028 preflight did not pass")
    if pre.get("target_outcomes_calculated") or pre.get("pnl_outcomes_calculated"):
        raise RuntimeError("preflight was not zero-outcome")
    if pre.get("secondary_test_loaded_or_inspected") or pre.get("final_holdout_loaded_or_inspected"):
        raise RuntimeError("preflight protected-period seal failed")

    tests={
        "engine_m_v01":self_tests_engine_m(),
        "engine_m_v02":self_tests_engine_m_v02(),
        "synthetic_setup":synthetic_setup_tests(),
        "synthetic_fill":synthetic_fill_tests(),
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

    market_scans={}
    all_signals=[]
    all_controls=[]
    for symbol in EXECUTION_MARKETS:
        uj=data["USDJPY"] if symbol=="EURJPY" else None
        scan=scan_market(symbol,data[symbol],uj)
        market_scans[symbol]={
            "setup_status_counts":scan["setup_status_counts"],
            "blocked_due_pending_order":scan["blocked_due_pending_order"],
            "arms":len(scan["arms"]),
            "limit_signals":len(scan["signals"]),
            "control_signals":len(scan["controls"]),
        }
        all_signals.extend(scan["signals"])
        all_controls.extend(scan["controls"])

    fold_results=[]
    for fold in FOLDS:
        s,e=ts(fold["eval_start"]),ts(fold["eval_end"])
        sig=[r for r in all_signals if s<=r["decision_ts"]<e]
        ctrl=[r for r in all_controls if s<=r["decision_ts"]<e]

        sm=signal_metrics(sig)
        cm=signal_metrics(ctrl)
        p=portfolio_sim(sig,s,e)
        cp=portfolio_sim(ctrl,s,e)

        fold_results.append({
            "fold":fold["id"],
            "evaluation":[fold["eval_start"],fold["eval_end"]],
            "signal_edge":sm,
            "control_signal_edge":cm,
            "reference_account":p,
            "control_reference_account":cp,
        })

    dev_signals=[
        r for r in all_signals
        if ts(FOLDS[0]["eval_start"])<=r["decision_ts"]<SEALED_START
    ]
    dev_controls=[
        r for r in all_controls
        if ts(FOLDS[0]["eval_start"])<=r["decision_ts"]<SEALED_START
    ]
    pooled_signal=signal_metrics(dev_signals)
    pooled_control_signal=signal_metrics(dev_controls)
    pooled_account=aggregate_portfolios(fold_results,"reference_account")
    pooled_control_account=aggregate_portfolios(fold_results,"control_reference_account")

    fold_stress=[fr["signal_edge"]["stress_r_expectancy"] for fr in fold_results]
    positive_stress_folds=sum(x is not None and x>0 for x in fold_stress)

    gate={
        "signal_trades_ge_120":pooled_signal["signals"]>=120,
        "every_fold_signals_ge_8":all(fr["signal_edge"]["signals"]>=8 for fr in fold_results),
        "pooled_primary_normalized_r_expectancy_gt_0":pooled_signal["primary_r_expectancy"] is not None and pooled_signal["primary_r_expectancy"]>0,
        "pooled_stress_normalized_r_expectancy_gt_0":pooled_signal["stress_r_expectancy"] is not None and pooled_signal["stress_r_expectancy"]>0,
        "positive_stress_normalized_r_folds_ge_4":positive_stress_folds>=4,
        "reference_account_trades_ge_90":pooled_account["actual_trades"]>=90,
        "distinct_executable_trade_weekdays_ge_35":pooled_account["distinct_trade_weekdays"]>=35,
        "reference_account_primary_expectancy_gt_0":pooled_account["primary_expectancy_usd"] is not None and pooled_account["primary_expectancy_usd"]>0,
        "reference_account_stress_expectancy_gt_0":pooled_account["stress_expectancy_usd"] is not None and pooled_account["stress_expectancy_usd"]>0,
        "primary_pf_ge_1_10":pooled_account["primary_profit_factor"] is not None and pooled_account["primary_profit_factor"]>=1.10,
        "stress_pf_ge_1_05":pooled_account["stress_profit_factor"] is not None and pooled_account["stress_profit_factor"]>=1.05,
        "stress_mdd_le_150":pooled_account["stress_max_drawdown_usd"]<=150.0,
        "max_market_share_le_60pct":pooled_account["max_market_trade_share"] is not None and pooled_account["max_market_trade_share"]<=0.60,
        "integrity_provenance_pass":True,
        "secondary_and_final_holdout_sealed":True,
    }
    gate["final_development_gate"]=bool(all(gate.values()))

    result={
        "experiment":"EXP-028",
        "engine":"Engine M v0.2",
        "stage":"six_slice_signal_edge_and_safe_account_development",
        "tested_repository_sha":repo_sha(),
        "engine_m_v01_sha256":sha256_file(ROOT/"research/code/engine_m_v0_1.py"),
        "engine_m_v02_sha256":sha256_file(ROOT/"research/code/engine_m_v0_2.py"),
        "runner_sha256":sha256_file(Path(__file__)),
        "scope":{
            "development":["2026-04-13","2026-06-30"],
            "source_parsed_through":"2026-06-30",
            "secondary_test_loaded_or_labeled":False,
            "final_holdout_loaded_or_labeled":False,
            "parsed_market_data_max_timestamp":max(str(df["datetime"].max()) for df in data.values()),
        },
        "tests":tests,
        "market_scan_summary":market_scans,
        "folds":fold_results,
        "pooled_signal_edge":pooled_signal,
        "pooled_control_signal_edge":pooled_control_signal,
        "positive_stress_normalized_r_folds":positive_stress_folds,
        "pooled_reference_account":pooled_account,
        "pooled_control_reference_account":pooled_control_account,
        "development_gate":gate,
        "disposition":"PASS_READY_FOR_SECONDARY_DESIGN" if gate["final_development_gate"] else "FAIL_STOP_BEFORE_SECONDARY",
    }

    out=OUT/"EXP-028-development-summary-v0.2.json"
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")

    print(json.dumps({
        "pooled_signal_edge":pooled_signal,
        "positive_stress_normalized_r_folds":positive_stress_folds,
        "pooled_reference_account":{
            k:pooled_account[k] for k in [
                "actual_trades","distinct_trade_weekdays",
                "primary_expectancy_usd","stress_expectancy_usd",
                "primary_profit_factor","stress_profit_factor",
                "stress_max_drawdown_usd","utility_band_trade_count",
                "pct_weekdays_final_pnl_ge_100","pct_weekdays_final_pnl_ge_150"
            ]
        },
        "development_gate":gate,
        "disposition":result["disposition"],
        "secondary_test_loaded_or_labeled":False,
        "final_holdout_loaded_or_labeled":False,
    },indent=2))


if __name__=="__main__":
    main()
