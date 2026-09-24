#!/usr/bin/env python3
"""EXP-035 Engine O v0.2 six-slice development.

Evaluates:
1) normalized-R edge for filled continuous-M5 statistical-reversion signals;
2) safe-lot USD500 one-open portfolio;
3) descriptive time-of-day cohorts;
4) matched immediate-entry control on the same non-suppressed qualified arms.

Development source hard-sealed before 2026-07-01.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Optional

import pandas as pd

from engine_k_v0_1 import EXECUTION_MARKETS, download_pinned
from engine_m_v0_1 import build_mtf_bars
from engine_m_v0_2 import safe_deployability_overlay, self_tests_engine_m_v02
from engine_o_v0_2 import setup_at, find_limit_fill, self_tests_engine_o_v02
from run_engine_k_v0_2_training_calibration import load_scoped_csv, label_self_tests
from run_engine_o_v0_2_preflight import (
    synthetic_engine_o_v02_tests,
    pending_suppression_tests,
    continuous_grid_tests,
)
from run_engine_m_v0_2_development import (
    ROOT,
    OUT,
    START,
    SEALED_START,
    FOLDS,
    ts,
    repo_sha,
    sha256_file,
    first_active_open,
    entry_usd_jpy_at,
    signal_and_account_labels,
    signal_metrics,
    portfolio_sim,
    aggregate_portfolios,
    self_tests_development,
)

CACHE=Path("/tmp/engine-o-v02-development")


def scan_market_o(
    symbol:str,
    df1:pd.DataFrame,
    usd_jpy_df:Optional[pd.DataFrame]=None,
)->dict:
    bars=build_mtf_bars(df1)
    b5=bars["m5"]

    usd_jpy_series=None
    if usd_jpy_df is not None:
        usd_jpy_series=usd_jpy_df.set_index("datetime")["close"].sort_index()

    pending_until=pd.Timestamp.min.tz_localize("UTC")
    status=Counter()
    fill_status=Counter()
    blocked=0
    arms=[]
    signals=[]
    controls=[]

    for i in range(len(b5)):
        decision_ts=b5.iloc[i]["available_ts"]
        if decision_ts<START or decision_ts>=SEALED_START:
            continue

        setup=setup_at(b5,i,symbol)
        status[setup["status"]]+=1
        if setup["status"]!="armed":
            continue

        # Match the preflight architecture: a qualified setup while a prior
        # Engine-O limit is still pending is suppressed, not queued.
        if decision_ts<pending_until:
            blocked+=1
            continue

        direction=setup["direction"]
        stop=float(setup["stop"])
        arm_id=f"{symbol}|{decision_ts.isoformat()}|{direction}"

        fill=find_limit_fill(df1,setup)
        pending_until=fill["resolved_ts"]
        fill_status[fill["status"]]+=1

        arms.append({
            "arm_id":arm_id,
            "symbol":symbol,
            "direction":direction,
            "decision_ts":decision_ts,
            "center":float(setup["center"]),
            "stretch_mad_multiple":float(setup["stretch_mad_multiple"]),
            "trigger_range":float(setup["trigger_range"]),
            "trigger_body_fraction":float(setup["trigger_body_fraction"]),
            "stop":stop,
            "limit":float(setup["limit"]),
            "limit_status":fill["status"],
            "limit_filled":bool(fill.get("filled",False)),
        })

        # Engine-O pullback signal only if the frozen midpoint limit fills.
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
                    "center":float(setup["center"]),
                    "stretch_mad_multiple":float(setup["stretch_mad_multiple"]),
                    "trigger_range":float(setup["trigger_range"]),
                    "trigger_body_fraction":float(setup["trigger_body_fraction"]),
                    "wait_active_m1_bars":int(fill["wait_active_m1_bars"]),
                    "entry_improvement_trigger_range":float(fill["entry_improvement_trigger_range"]),
                    "safe_overlay":overlay,
                    **labels,
                })

        # Matched immediate-entry control on the same non-suppressed qualified arm.
        # It is descriptive and independent of whether the 50% pullback later fills.
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
                        "center":float(setup["center"]),
                        "stretch_mad_multiple":float(setup["stretch_mad_multiple"]),
                        "trigger_range":float(setup["trigger_range"]),
                        "trigger_body_fraction":float(setup["trigger_body_fraction"]),
                        "safe_overlay":ctrl_overlay,
                        **labels,
                    })

    return {
        "setup_status_counts":dict(sorted(status.items())),
        "blocked_due_pending_order":blocked,
        "fill_status_counts":dict(sorted(fill_status.items())),
        "arms":arms,
        "signals":signals,
        "controls":controls,
    }


def hour_cohort_metrics(rows:list[dict])->dict:
    out={}
    for h in range(6,18):
        key=f"H{h:02d}"
        rr=[r for r in rows if r["decision_ts"].hour==h]
        out[key]=signal_metrics(rr)
    return out


def main():
    pre_path=OUT/"EXP-035-continuous-m5-reversion-preflight-v0.2.json"
    if not pre_path.exists():
        raise RuntimeError("EXP-035 preflight result missing")
    pre=json.loads(pre_path.read_text())
    if pre.get("preflight_pass") is not True:
        raise RuntimeError("EXP-035 preflight did not pass")
    if pre.get("target_outcomes_calculated") or pre.get("pnl_outcomes_calculated"):
        raise RuntimeError("EXP-035 preflight was not zero-outcome")
    if pre.get("secondary_test_loaded_or_inspected") or pre.get("final_holdout_loaded_or_inspected"):
        raise RuntimeError("EXP-035 protected-period seal failed")

    tests={
        "engine_o_v02":self_tests_engine_o_v02(),
        "engine_m_v02_safe_overlay":self_tests_engine_m_v02(),
        "synthetic_engine_o_v02":synthetic_engine_o_v02_tests(),
        "pending_suppression":pending_suppression_tests(),
        "continuous_grid":continuous_grid_tests(),
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
        scan=scan_market_o(symbol,data[symbol],uj)
        market_scans[symbol]={
            "setup_status_counts":scan["setup_status_counts"],
            "blocked_due_pending_order":scan["blocked_due_pending_order"],
            "fill_status_counts":scan["fill_status_counts"],
            "arms":len(scan["arms"]),
            "signals":len(scan["signals"]),
            "controls":len(scan["controls"]),
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
            "hour_cohorts":hour_cohort_metrics(sig),
            "control_signal_edge":cm,
            "control_hour_cohorts":hour_cohort_metrics(ctrl),
            "reference_account":p,
            "control_reference_account":cp,
        })

    dev_start=ts(FOLDS[0]["eval_start"])
    dev_signals=[r for r in all_signals if dev_start<=r["decision_ts"]<SEALED_START]
    dev_controls=[r for r in all_controls if dev_start<=r["decision_ts"]<SEALED_START]

    pooled_signal=signal_metrics(dev_signals)
    pooled_control=signal_metrics(dev_controls)
    pooled_hours=hour_cohort_metrics(dev_signals)
    pooled_control_hours=hour_cohort_metrics(dev_controls)
    pooled_account=aggregate_portfolios(fold_results,"reference_account")
    pooled_control_account=aggregate_portfolios(fold_results,"control_reference_account")

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
        "experiment":"EXP-035",
        "engine":"Engine O v0.2",
        "stage":"six_slice_continuous_m5_statistical_reversion_development",
        "tested_repository_sha":repo_sha(),
        "engine_o_v02_sha256":sha256_file(ROOT/"research/code/engine_o_v0_2.py"),
        "runner_sha256":sha256_file(Path(__file__)),
        "outcome_convention":{
            "target":"frozen T40",
            "stop":"trigger extreme plus/minus one research tick",
            "same_bar":"stop_first",
            "max_active_m1":120,
            "session_cutoff_utc":"20:00",
        },
        "immediate_control_definition":"same non-suppressed qualified Engine-O arm at first active M1 open after decision; independent of later 50% pullback fill",
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
        "pooled_hour_cohorts":pooled_hours,
        "pooled_control_signal_edge":pooled_control,
        "pooled_control_hour_cohorts":pooled_control_hours,
        "positive_stress_normalized_r_folds":positive_stress_folds,
        "pooled_reference_account":pooled_account,
        "pooled_control_reference_account":pooled_control_account,
        "development_gate":gate,
        "disposition":"PASS_READY_FOR_SECONDARY_DESIGN" if gate["final_development_gate"] else "FAIL_STOP_BEFORE_SECONDARY",
    }

    out=OUT/"EXP-035-development-summary-v0.2.json"
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")

    print(json.dumps({
        "pooled_signal_edge":pooled_signal,
        "pooled_control_signal_edge":pooled_control,
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
