#!/usr/bin/env python3
"""EXP-031 Engine M v0.5 six-slice development.

Uses the already-audited EXP-028 labeling and portfolio machinery unchanged.
Only the setup selector is Engine M v0.5 recent-H1 range logic.

Development source is sealed at 2026-06-30.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Optional

import pandas as pd

from engine_k_v0_1 import EXECUTION_MARKETS, download_pinned
from engine_m_v0_1 import build_mtf_bars, find_limit_fill, self_tests_engine_m
from engine_m_v0_2 import safe_deployability_overlay, self_tests_engine_m_v02
from engine_m_v0_5 import recent_h1_range_setup_at, self_tests_engine_m_v05
from run_engine_k_v0_2_training_calibration import load_scoped_csv, label_self_tests
from run_engine_m_v0_1_preflight import synthetic_fill_tests
from run_engine_m_v0_5_preflight import synthetic_recent_h1_tests
from run_engine_m_v0_2_development import (
    ROOT,
    OUT,
    START,
    SEALED_START,
    FOLDS,
    ts,
    repo_sha,
    sha256_file,
    entry_usd_jpy_at,
    signal_and_account_labels,
    signal_metrics,
    portfolio_sim,
    aggregate_portfolios,
    self_tests_development,
)

CACHE=Path("/tmp/engine-m-v05-development")


def scan_market_v05(
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
    selected=Counter()
    blocked=0
    arms=[]
    signals=[]

    for i in range(len(bars["m15"])):
        decision_ts=bars["m15"].iloc[i]["available_ts"]
        if decision_ts<START or decision_ts>=SEALED_START:
            continue
        if decision_ts.weekday()>=5 or decision_ts.hour>=18:
            continue

        setup=recent_h1_range_setup_at(bars,i,symbol)
        status[setup["status"]]+=1
        if setup["status"]!="armed":
            continue

        selected[setup["selected_h1"]]+=1
        if decision_ts<pending_until:
            blocked+=1
            continue

        fill=find_limit_fill(df1,setup,symbol,usd_jpy_series)
        pending_until=fill["resolved_ts"]

        direction=setup["direction"]
        stop=float(setup["stop"])
        arm_id=f"{symbol}|{decision_ts.isoformat()}|{direction}|{setup['selected_h1']}"

        arms.append({
            "arm_id":arm_id,
            "symbol":symbol,
            "direction":direction,
            "decision_ts":decision_ts,
            "selected_h1":setup["selected_h1"],
            "selected_h1_start":setup["selected_h1_start"],
            "stop":stop,
            "limit_status":fill["status"],
            "limit_filled":bool(fill.get("filled",False)),
        })

        if not fill.get("filled"):
            continue

        entry_ts=fill["entry_ts"]
        entry=float(fill["entry"])
        uj=entry_usd_jpy_at(usd_jpy_series,entry_ts) if symbol=="EURJPY" else None
        overlay=safe_deployability_overlay(symbol,entry,stop,uj)
        if overlay.get("reason") in (
            "invalid_geometry","value_or_notional_unavailable",
            "target_geometry_unavailable","invalid_stop_loss_per_lot"
        ):
            continue

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
            "selected_h1":setup["selected_h1"],
            "selected_h1_start":setup["selected_h1_start"],
            "h1_low":float(setup["h1_low"]),
            "h1_high":float(setup["h1_high"]),
            "target_price_preentry":float(setup["target_price"]),
            "wait_active_m1_bars":int(fill["wait_active_m1_bars"]),
            "entry_improvement_a5_range":float(fill["entry_improvement_a5_range"]),
            "safe_overlay":overlay,
            **labels,
        })

    return {
        "setup_status_counts":dict(sorted(status.items())),
        "selected_h1_counts":dict(sorted(selected.items())),
        "blocked_due_pending_order":blocked,
        "arms":arms,
        "signals":signals,
    }


def cohort_metrics(rows:list[dict])->dict:
    out={}
    for cohort in ("H1_0","H1_1"):
        rr=[r for r in rows if r["selected_h1"]==cohort]
        out[cohort]=signal_metrics(rr)
    return out


def main():
    pre_path=OUT/"EXP-031-recent-h1-preflight-v0.5.json"
    if not pre_path.exists():
        raise RuntimeError("EXP-031 preflight result missing")
    pre=json.loads(pre_path.read_text())
    if pre.get("preflight_pass") is not True:
        raise RuntimeError("EXP-031 preflight did not pass")
    if pre.get("target_outcomes_calculated") or pre.get("pnl_outcomes_calculated"):
        raise RuntimeError("EXP-031 preflight was not zero-outcome")
    if pre.get("secondary_test_loaded_or_inspected") or pre.get("final_holdout_loaded_or_inspected"):
        raise RuntimeError("EXP-031 protected-period seal failed")

    tests={
        "engine_m_v01":self_tests_engine_m(),
        "engine_m_v02":self_tests_engine_m_v02(),
        "engine_m_v05":self_tests_engine_m_v05(),
        "synthetic_recent_h1":synthetic_recent_h1_tests(),
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
    for symbol in EXECUTION_MARKETS:
        uj=data["USDJPY"] if symbol=="EURJPY" else None
        scan=scan_market_v05(symbol,data[symbol],uj)
        market_scans[symbol]={
            "setup_status_counts":scan["setup_status_counts"],
            "selected_h1_counts":scan["selected_h1_counts"],
            "blocked_due_pending_order":scan["blocked_due_pending_order"],
            "arms":len(scan["arms"]),
            "signals":len(scan["signals"]),
        }
        all_signals.extend(scan["signals"])

    fold_results=[]
    for fold in FOLDS:
        s,e=ts(fold["eval_start"]),ts(fold["eval_end"])
        sig=[r for r in all_signals if s<=r["decision_ts"]<e]
        sm=signal_metrics(sig)
        cohorts=cohort_metrics(sig)
        p=portfolio_sim(sig,s,e)

        fold_results.append({
            "fold":fold["id"],
            "evaluation":[fold["eval_start"],fold["eval_end"]],
            "signal_edge":sm,
            "selected_h1_cohorts":cohorts,
            "reference_account":p,
        })

    dev_signals=[
        r for r in all_signals
        if ts(FOLDS[0]["eval_start"])<=r["decision_ts"]<SEALED_START
    ]

    pooled_signal=signal_metrics(dev_signals)
    pooled_cohorts=cohort_metrics(dev_signals)
    pooled_account=aggregate_portfolios(fold_results,"reference_account")
    fold_stress=[fr["signal_edge"]["stress_r_expectancy"] for fr in fold_results]
    positive_stress_folds=sum(x is not None and x>0 for x in fold_stress)

    gate={
        "signal_trades_ge_120":pooled_signal["signals"]>=120,
        "every_fold_signals_ge_8":all(fr["signal_edge"]["signals"]>=8 for fr in fold_results),
        "pooled_gross_normalized_r_expectancy_gt_0_20":pooled_signal["gross_r_expectancy"] is not None and pooled_signal["gross_r_expectancy"]>0.20,
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
        "experiment":"EXP-031",
        "engine":"Engine M v0.5",
        "stage":"six_slice_recent_h1_development",
        "tested_repository_sha":repo_sha(),
        "engine_m_v05_sha256":sha256_file(ROOT/"research/code/engine_m_v0_5.py"),
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
        "pooled_selected_h1_cohorts":pooled_cohorts,
        "positive_stress_normalized_r_folds":positive_stress_folds,
        "pooled_reference_account":pooled_account,
        "development_gate":gate,
        "disposition":"PASS_READY_FOR_SECONDARY_DESIGN" if gate["final_development_gate"] else "FAIL_STOP_BEFORE_SECONDARY",
    }

    out=OUT/"EXP-031-development-summary-v0.5.json"
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")

    print(json.dumps({
        "pooled_signal_edge":pooled_signal,
        "pooled_selected_h1_cohorts":pooled_cohorts,
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
