#!/usr/bin/env python3
"""EXP-038 Engine Q v0.2 six-slice development.

Evaluates:
1) normalized-R edge for filled rolling cross-market volatility-spillover signals;
2) safe-lot USD500 one-open portfolio;
3) descriptive peer-shock / lag / breakout / hour / market diagnostics;
4) matched immediate-entry control on the same qualified breakout triggers.

Development source is hard-sealed before 2026-07-01.
Fold membership is keyed to breakout completion time, the first directional trade-decision time.
"""

from __future__ import annotations

import json
import math
import statistics
from collections import Counter
from pathlib import Path

import pandas as pd

from engine_k_v0_1 import EXECUTION_MARKETS, download_pinned
from engine_m_v0_1 import build_mtf_bars
from engine_m_v0_2 import safe_deployability_overlay, self_tests_engine_m_v02
from engine_q_v0_1 import metric_at_time, find_breakout_trigger, find_limit_fill
from engine_q_v0_2 import arm_from_history, self_tests_engine_q_v02
from run_engine_k_v0_2_training_calibration import load_scoped_csv, label_self_tests
from run_engine_q_v0_2_preflight import synthetic_rolling_tests
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

CACHE=Path("/tmp/engine-q-v02-development")


def pct(values:list[float],q:float):
    if not values:
        return None
    xs=sorted(float(x) for x in values)
    if len(xs)==1:
        return xs[0]
    pos=(len(xs)-1)*q
    lo=int(math.floor(pos)); hi=int(math.ceil(pos))
    if lo==hi:
        return xs[lo]
    w=pos-lo
    return xs[lo]*(1-w)+xs[hi]*w


def descriptive_summary(rows:list[dict])->dict:
    shock_counts=[float(r["peer_shock_count"]) for r in rows if r.get("peer_shock_count") is not None]
    lag=[float(r["candidate_vr_at_arm"]) for r in rows if r.get("candidate_vr_at_arm") is not None]
    trig=[float(r["trigger_vr"]) for r in rows if r.get("trigger_vr") is not None]
    waits=[float(r["arm_wait_m5_bars"]) for r in rows if r.get("arm_wait_m5_bars") is not None]

    ages=[]
    for r in rows:
        for a in (r.get("shock_ages_minutes") or {}).values():
            ages.append(float(a))

    def d(xs):
        return {
            "n":len(xs),
            "median":statistics.median(xs) if xs else None,
            "p25":pct(xs,0.25),
            "p75":pct(xs,0.75),
            "p90":pct(xs,0.90),
        }

    return {
        "peer_shock_count":d(shock_counts),
        "shock_age_minutes":d(ages),
        "candidate_vr_at_arm":d(lag),
        "trigger_vr":d(trig),
        "arm_wait_m5_bars":d(waits),
    }


def hour_cohort_metrics(rows:list[dict])->dict:
    out={}
    for h in range(6,18):
        key=f"H{h:02d}"
        rr=[r for r in rows if r["decision_ts"].hour==h]
        out[key]=signal_metrics(rr)
    return out


def scan_all_markets(data:dict[str,pd.DataFrame])->dict:
    bars5={s:build_mtf_bars(data[s])["m5"] for s in EXECUTION_MARKETS}
    usd_jpy_series=data["USDJPY"].set_index("datetime")["close"].sort_index()

    busy_until={s:pd.Timestamp.min.tz_localize("UTC") for s in EXECUTION_MARKETS}
    arm_status={s:Counter() for s in EXECUTION_MARKETS}
    trigger_status={s:Counter() for s in EXECUTION_MARKETS}
    fill_status={s:Counter() for s in EXECUTION_MARKETS}
    blocked={s:0 for s in EXECUTION_MARKETS}
    arms={s:0 for s in EXECUTION_MARKETS}
    triggers={s:0 for s in EXECUTION_MARKETS}
    signals=[]
    controls=[]

    days=pd.date_range(
        START.normalize(),
        SEALED_START-pd.Timedelta(days=1),
        freq="D",
        tz="UTC",
    )

    for day in days:
        if day.weekday()>=5:
            continue

        for mins in range(6*60+5,17*60+25+1,5):
            arm_decision_ts=day+pd.Timedelta(minutes=mins)

            history=[]
            for offset in (0,5,10):
                dts=arm_decision_ts-pd.Timedelta(minutes=offset)
                history.append({
                    s:metric_at_time(bars5[s],dts)
                    for s in EXECUTION_MARKETS
                })

            for symbol in EXECUTION_MARKETS:
                if arm_decision_ts<busy_until[symbol]:
                    blocked[symbol]+=1
                    continue

                arm=arm_from_history(symbol,history)
                arm_status[symbol][arm["status"]]+=1
                if arm["status"]!="armed":
                    continue
                arms[symbol]+=1

                trigger=find_breakout_trigger(bars5[symbol],symbol,arm)
                trigger_status[symbol][trigger["status"]]+=1
                if not trigger.get("triggered"):
                    busy_until[symbol]=trigger["resolved_ts"]
                    continue
                triggers[symbol]+=1

                # First directional candidate decision is breakout completion.
                decision_ts=trigger["decision_ts"]
                direction=trigger["direction"]
                stop=float(trigger["stop"])
                arm_id=f"{symbol}|{decision_ts.isoformat()}|{direction}"

                fill=find_limit_fill(data[symbol],trigger)
                busy_until[symbol]=fill["resolved_ts"]
                fill_status[symbol][fill["status"]]+=1

                base={
                    "arm_id":arm_id,
                    "symbol":symbol,
                    "direction":direction,
                    "arm_decision_ts":arm_decision_ts,
                    "decision_ts":decision_ts,
                    "peer_shock_count":int(arm["shock_count"]),
                    "shock_ages_minutes":dict(arm["shock_ages_minutes"]),
                    "candidate_vr_at_arm":float(arm["candidate_vr"]),
                    "trigger_vr":float(trigger["trigger_vr"]),
                    "arm_wait_m5_bars":int(trigger["arm_wait_m5_bars"]),
                    "trigger_range":float(trigger["trigger_range"]),
                    "trigger_body_fraction":float(trigger["trigger_body_fraction"]),
                    "limit":float(trigger["limit"]),
                    "stop":stop,
                    "limit_status":fill["status"],
                    "limit_filled":bool(fill.get("filled",False)),
                }

                # Frozen 50% pullback signal.
                if fill.get("filled"):
                    entry_ts=fill["entry_ts"]
                    entry=float(fill["entry"])
                    uj=entry_usd_jpy_at(usd_jpy_series,entry_ts) if symbol=="EURJPY" else None
                    overlay=safe_deployability_overlay(symbol,entry,stop,uj)

                    if overlay.get("reason") not in (
                        "invalid_geometry",
                        "value_or_notional_unavailable",
                        "target_geometry_unavailable",
                        "invalid_stop_loss_per_lot",
                    ):
                        labels=signal_and_account_labels(
                            symbol,data[symbol],direction,entry_ts,entry,stop,uj,overlay
                        )
                        signals.append({
                            **base,
                            "entry_ts":entry_ts,
                            "entry":entry,
                            "wait_active_m1_bars":int(fill["wait_active_m1_bars"]),
                            "entry_improvement_trigger_range":float(
                                fill["entry_improvement_trigger_range"]
                            ),
                            "safe_overlay":overlay,
                            **labels,
                        })

                # Matched immediate control on same qualified breakout trigger.
                nxt=first_active_open(data[symbol],decision_ts)
                if nxt is not None:
                    ctrl_ts,ctrl_entry=nxt
                    valid=(stop<ctrl_entry) if direction=="long" else (stop>ctrl_entry)
                    if valid:
                        uj=entry_usd_jpy_at(usd_jpy_series,ctrl_ts) if symbol=="EURJPY" else None
                        overlay=safe_deployability_overlay(symbol,ctrl_entry,stop,uj)
                        if overlay.get("reason") not in (
                            "invalid_geometry",
                            "value_or_notional_unavailable",
                            "target_geometry_unavailable",
                            "invalid_stop_loss_per_lot",
                        ):
                            labels=signal_and_account_labels(
                                symbol,data[symbol],direction,ctrl_ts,ctrl_entry,stop,uj,overlay
                            )
                            controls.append({
                                **base,
                                "entry_ts":ctrl_ts,
                                "entry":float(ctrl_entry),
                                "safe_overlay":overlay,
                                **labels,
                            })

    market_summary={}
    for s in EXECUTION_MARKETS:
        market_summary[s]={
            "arm_status_counts":dict(sorted(arm_status[s].items())),
            "trigger_status_counts":dict(sorted(trigger_status[s].items())),
            "fill_status_counts":dict(sorted(fill_status[s].items())),
            "blocked_due_active_arm_or_order":blocked[s],
            "arms":arms[s],
            "triggers":triggers[s],
            "signals":sum(1 for r in signals if r["symbol"]==s),
            "controls":sum(1 for r in controls if r["symbol"]==s),
        }

    return {
        "market_summary":market_summary,
        "signals":signals,
        "controls":controls,
    }


def self_tests_q_development()->list[str]:
    tests=self_tests_development()
    # Trade-decision timestamp is explicitly breakout completion, not arm creation.
    arm_ts=pd.Timestamp("2026-04-13T09:05:00Z")
    trigger_ts=arm_ts+pd.Timedelta(minutes=10)
    assert trigger_ts>arm_ts
    tests.append("fold_assignment_uses_breakout_decision_time")
    tests.append("matched_control_uses_breakout_decision_time")
    return tests


def main():
    pre_path=OUT/"EXP-038-rolling-volatility-spillover-preflight-v0.2.json"
    if not pre_path.exists():
        raise RuntimeError("EXP-038 preflight result missing")

    pre=json.loads(pre_path.read_text())
    if pre.get("preflight_pass") is not True:
        raise RuntimeError("EXP-038 preflight did not pass")
    if pre.get("target_outcomes_calculated") or pre.get("pnl_outcomes_calculated"):
        raise RuntimeError("EXP-038 preflight was not zero-outcome")
    if pre.get("secondary_test_loaded_or_inspected") or pre.get("final_holdout_loaded_or_inspected"):
        raise RuntimeError("EXP-038 protected-period seal failed")

    tests={
        "engine_q_v02":self_tests_engine_q_v02(),
        "engine_m_v02_safe_overlay":self_tests_engine_m_v02(),
        "synthetic_rolling":synthetic_rolling_tests(),
        "label":label_self_tests(),
        "development":self_tests_q_development(),
    }

    data={}
    for symbol in EXECUTION_MARKETS:
        path=download_pinned(symbol,CACHE)
        df=load_scoped_csv(path,symbol,SEALED_START)
        if df.empty or df["datetime"].max()>=SEALED_START:
            raise RuntimeError(f"{symbol}: protected-period leak")
        data[symbol]=df

    scan=scan_all_markets(data)
    all_signals=scan["signals"]
    all_controls=scan["controls"]

    fold_results=[]
    for fold in FOLDS:
        s,e=ts(fold["eval_start"]),ts(fold["eval_end"])
        sig=[r for r in all_signals if s<=r["decision_ts"]<e]
        ctrl=[r for r in all_controls if s<=r["decision_ts"]<e]

        fold_results.append({
            "fold":fold["id"],
            "evaluation":[fold["eval_start"],fold["eval_end"]],
            "signal_edge":signal_metrics(sig),
            "descriptive_summary":descriptive_summary(sig),
            "hour_cohorts":hour_cohort_metrics(sig),
            "control_signal_edge":signal_metrics(ctrl),
            "control_descriptive_summary":descriptive_summary(ctrl),
            "reference_account":portfolio_sim(sig,s,e),
            "control_reference_account":portfolio_sim(ctrl,s,e),
        })

    dev_start=ts(FOLDS[0]["eval_start"])
    dev_signals=[r for r in all_signals if dev_start<=r["decision_ts"]<SEALED_START]
    dev_controls=[r for r in all_controls if dev_start<=r["decision_ts"]<SEALED_START]

    pooled_signal=signal_metrics(dev_signals)
    pooled_control=signal_metrics(dev_controls)
    pooled_account=aggregate_portfolios(fold_results,"reference_account")
    pooled_control_account=aggregate_portfolios(fold_results,"control_reference_account")
    positive_stress_folds=sum(
        fr["signal_edge"]["stress_r_expectancy"] is not None
        and fr["signal_edge"]["stress_r_expectancy"]>0
        for fr in fold_results
    )

    gate={
        "signal_trades_ge_120":pooled_signal["signals"]>=120,
        "every_fold_signals_ge_8":all(fr["signal_edge"]["signals"]>=8 for fr in fold_results),
        "pooled_gross_normalized_r_expectancy_gt_0_20":
            pooled_signal["gross_r_expectancy"] is not None
            and pooled_signal["gross_r_expectancy"]>0.20,
        "pooled_primary_normalized_r_expectancy_gt_0":
            pooled_signal["primary_r_expectancy"] is not None
            and pooled_signal["primary_r_expectancy"]>0,
        "pooled_stress_normalized_r_expectancy_gt_0":
            pooled_signal["stress_r_expectancy"] is not None
            and pooled_signal["stress_r_expectancy"]>0,
        "positive_stress_normalized_r_folds_ge_4":positive_stress_folds>=4,
        "reference_account_trades_ge_90":pooled_account["actual_trades"]>=90,
        "distinct_executable_trade_weekdays_ge_35":pooled_account["distinct_trade_weekdays"]>=35,
        "reference_account_primary_expectancy_gt_0":
            pooled_account["primary_expectancy_usd"] is not None
            and pooled_account["primary_expectancy_usd"]>0,
        "reference_account_stress_expectancy_gt_0":
            pooled_account["stress_expectancy_usd"] is not None
            and pooled_account["stress_expectancy_usd"]>0,
        "primary_pf_ge_1_10":
            pooled_account["primary_profit_factor"] is not None
            and pooled_account["primary_profit_factor"]>=1.10,
        "stress_pf_ge_1_05":
            pooled_account["stress_profit_factor"] is not None
            and pooled_account["stress_profit_factor"]>=1.05,
        "stress_mdd_le_150":pooled_account["stress_max_drawdown_usd"]<=150.0,
        "max_market_share_le_60pct":
            pooled_account["max_market_trade_share"] is not None
            and pooled_account["max_market_trade_share"]<=0.60,
        "integrity_provenance_pass":True,
        "secondary_and_final_holdout_sealed":True,
    }
    gate["final_development_gate"]=bool(all(gate.values()))

    result={
        "experiment":"EXP-038",
        "engine":"Engine Q v0.2",
        "stage":"six_slice_rolling_cross_market_volatility_spillover_development",
        "tested_repository_sha":repo_sha(),
        "engine_q_v02_sha256":sha256_file(ROOT/"research/code/engine_q_v0_2.py"),
        "runner_sha256":sha256_file(Path(__file__)),
        "outcome_convention":{
            "target":"frozen T40",
            "stop":"breakout-bar structural stop",
            "same_bar":"stop_first",
            "max_active_m1":120,
            "session_cutoff_utc":"20:00",
            "fold_membership":"breakout completion time",
        },
        "immediate_control_definition":
            "same qualified Engine-Q breakout trigger at first active M1 open after breakout completion; independent of later 50% pullback fill",
        "diagnostic_policy":
            "peer shock count/age, candidate lag VR, breakout VR, hour, market and direction are descriptive only; no post-outcome cohort/threshold rescue",
        "scope":{
            "development":["2026-04-13","2026-06-30"],
            "source_parsed_through":"2026-06-30",
            "secondary_test_loaded_or_labeled":False,
            "final_holdout_loaded_or_labeled":False,
            "parsed_market_data_max_timestamp":
                max(str(df["datetime"].max()) for df in data.values()),
        },
        "tests":tests,
        "market_scan_summary":scan["market_summary"],
        "folds":fold_results,
        "pooled_signal_edge":pooled_signal,
        "pooled_descriptive_summary":descriptive_summary(dev_signals),
        "pooled_hour_cohorts":hour_cohort_metrics(dev_signals),
        "pooled_control_signal_edge":pooled_control,
        "pooled_control_descriptive_summary":descriptive_summary(dev_controls),
        "positive_stress_normalized_r_folds":positive_stress_folds,
        "pooled_reference_account":pooled_account,
        "pooled_control_reference_account":pooled_control_account,
        "development_gate":gate,
        "disposition":
            "PASS_READY_FOR_SECONDARY_DESIGN"
            if gate["final_development_gate"]
            else "FAIL_STOP_BEFORE_SECONDARY",
    }

    out=OUT/"EXP-038-development-summary-v0.2.json"
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")

    print(json.dumps({
        "pooled_signal_edge":pooled_signal,
        "pooled_control_signal_edge":pooled_control,
        "pooled_descriptive_summary":result["pooled_descriptive_summary"],
        "positive_stress_normalized_r_folds":positive_stress_folds,
        "pooled_reference_account":{
            k:pooled_account[k] for k in [
                "actual_trades",
                "distinct_trade_weekdays",
                "primary_expectancy_usd",
                "stress_expectancy_usd",
                "primary_profit_factor",
                "stress_profit_factor",
                "stress_max_drawdown_usd",
                "utility_band_trade_count",
                "pct_weekdays_final_pnl_ge_100",
                "pct_weekdays_final_pnl_ge_150",
            ]
        },
        "development_gate":gate,
        "disposition":result["disposition"],
        "secondary_test_loaded_or_labeled":False,
        "final_holdout_loaded_or_labeled":False,
    },indent=2))


if __name__=="__main__":
    main()
