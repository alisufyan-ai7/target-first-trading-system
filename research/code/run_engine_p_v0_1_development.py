#!/usr/bin/env python3
"""EXP-036 Engine P v0.1 six-slice development.

Evaluates:
1) normalized-R edge for filled cross-market relative-strength pullback signals;
2) safe-lot USD500 one-open portfolio;
3) descriptive own-MOM / factor / time / market diagnostics;
4) matched immediate-entry control on the same non-suppressed qualified arms.

Development source is hard-sealed before 2026-07-01.
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
from engine_p_v0_1 import (
    metric_at_time,
    setup_from_snapshot,
    find_limit_fill,
    self_tests_engine_p_v01,
)
from run_engine_k_v0_2_training_calibration import load_scoped_csv, label_self_tests
from run_engine_p_v0_1_preflight import synthetic_factor_tests
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

CACHE=Path("/tmp/engine-p-v01-development")


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


def factor_summary(rows:list[dict])->dict:
    own=[abs(float(r["own_mom"])) for r in rows if r.get("own_mom") is not None]
    usd=[abs(float(r["usd_score"])) for r in rows if r.get("usd_score") is not None]
    eu=[abs(float(r["eurusd_mom"])) for r in rows if r.get("eurusd_mom") is not None]
    uj=[abs(float(r["usdjpy_mom"])) for r in rows if r.get("usdjpy_mom") is not None]

    def d(x):
        return {
            "n":len(x),
            "median":statistics.median(x) if x else None,
            "p25":pct(x,0.25),
            "p75":pct(x,0.75),
            "p90":pct(x,0.90),
        }

    return {
        "abs_own_mom":d(own),
        "abs_usd_score":d(usd),
        "abs_eurusd_leg_mom":d(eu),
        "abs_usdjpy_leg_mom":d(uj),
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

    pending_until={s:pd.Timestamp.min.tz_localize("UTC") for s in EXECUTION_MARKETS}
    status={s:Counter() for s in EXECUTION_MARKETS}
    fill_status={s:Counter() for s in EXECUTION_MARKETS}
    blocked={s:0 for s in EXECUTION_MARKETS}
    arms={s:[] for s in EXECUTION_MARKETS}
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

        for mins in range(6*60+5,17*60+55+1,5):
            decision_ts=day+pd.Timedelta(minutes=mins)
            snapshot={s:metric_at_time(bars5[s],decision_ts) for s in EXECUTION_MARKETS}

            for symbol in EXECUTION_MARKETS:
                setup=setup_from_snapshot(symbol,snapshot)
                status[symbol][setup["status"]]+=1
                if setup["status"]!="armed":
                    continue

                if decision_ts<pending_until[symbol]:
                    blocked[symbol]+=1
                    continue

                direction=setup["direction"]
                stop=float(setup["stop"])
                arm_id=f"{symbol}|{decision_ts.isoformat()}|{direction}"

                fill=find_limit_fill(data[symbol],setup)
                pending_until[symbol]=fill["resolved_ts"]
                fill_status[symbol][fill["status"]]+=1

                arm={
                    "arm_id":arm_id,
                    "symbol":symbol,
                    "direction":direction,
                    "decision_ts":decision_ts,
                    "own_mom":float(setup["own_mom"]),
                    "usd_score":float(setup["usd_score"]) if setup.get("usd_score") is not None else None,
                    "eurusd_mom":float(setup["eurusd_mom"]) if setup.get("eurusd_mom") is not None else None,
                    "usdjpy_mom":float(setup["usdjpy_mom"]) if setup.get("usdjpy_mom") is not None else None,
                    "trigger_range":float(setup["trigger_range"]),
                    "trigger_body_fraction":float(setup["trigger_body_fraction"]),
                    "limit":float(setup["limit"]),
                    "stop":stop,
                    "limit_status":fill["status"],
                    "limit_filled":bool(fill.get("filled",False)),
                }
                arms[symbol].append(arm)

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
                            **arm,
                            "entry_ts":entry_ts,
                            "entry":entry,
                            "wait_active_m1_bars":int(fill["wait_active_m1_bars"]),
                            "entry_improvement_trigger_range":float(fill["entry_improvement_trigger_range"]),
                            "safe_overlay":overlay,
                            **labels,
                        })

                # Matched immediate control on the same non-suppressed arm,
                # independent of whether the 50% limit later fills.
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
                                **arm,
                                "entry_ts":ctrl_ts,
                                "entry":float(ctrl_entry),
                                "safe_overlay":overlay,
                                **labels,
                            })

    market_summary={}
    for s in EXECUTION_MARKETS:
        market_summary[s]={
            "setup_status_counts":dict(sorted(status[s].items())),
            "blocked_due_pending_order":blocked[s],
            "fill_status_counts":dict(sorted(fill_status[s].items())),
            "arms":len(arms[s]),
            "signals":sum(1 for r in signals if r["symbol"]==s),
            "controls":sum(1 for r in controls if r["symbol"]==s),
        }

    return {
        "market_summary":market_summary,
        "signals":signals,
        "controls":controls,
    }


def main():
    pre_path=OUT/"EXP-036-cross-market-relative-strength-preflight-v0.1.json"
    if not pre_path.exists():
        raise RuntimeError("EXP-036 preflight result missing")

    pre=json.loads(pre_path.read_text())
    if pre.get("preflight_pass") is not True:
        raise RuntimeError("EXP-036 preflight did not pass")
    if pre.get("target_outcomes_calculated") or pre.get("pnl_outcomes_calculated"):
        raise RuntimeError("EXP-036 preflight was not zero-outcome")
    if pre.get("secondary_test_loaded_or_inspected") or pre.get("final_holdout_loaded_or_inspected"):
        raise RuntimeError("EXP-036 protected-period seal failed")

    tests={
        "engine_p_v01":self_tests_engine_p_v01(),
        "engine_m_v02_safe_overlay":self_tests_engine_m_v02(),
        "synthetic_factor":synthetic_factor_tests(),
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
            "factor_summary":factor_summary(sig),
            "hour_cohorts":hour_cohort_metrics(sig),
            "control_signal_edge":signal_metrics(ctrl),
            "control_factor_summary":factor_summary(ctrl),
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
        "experiment":"EXP-036",
        "engine":"Engine P v0.1",
        "stage":"six_slice_cross_market_relative_strength_development",
        "tested_repository_sha":repo_sha(),
        "engine_p_v01_sha256":sha256_file(ROOT/"research/code/engine_p_v0_1.py"),
        "runner_sha256":sha256_file(Path(__file__)),
        "outcome_convention":{
            "target":"frozen T40",
            "stop":"trigger-bar structural stop",
            "same_bar":"stop_first",
            "max_active_m1":120,
            "session_cutoff_utc":"20:00",
        },
        "immediate_control_definition":
            "same non-suppressed qualified Engine-P arm at first active M1 open after decision; independent of later 50% pullback fill",
        "diagnostic_policy":
            "MOM/USD_SCORE/EURJPY-leg/hour/market cohorts descriptive only; no post-outcome threshold or whitelist rescue",
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
        "pooled_factor_summary":factor_summary(dev_signals),
        "pooled_hour_cohorts":hour_cohort_metrics(dev_signals),
        "pooled_control_signal_edge":pooled_control,
        "pooled_control_factor_summary":factor_summary(dev_controls),
        "positive_stress_normalized_r_folds":positive_stress_folds,
        "pooled_reference_account":pooled_account,
        "pooled_control_reference_account":pooled_control_account,
        "development_gate":gate,
        "disposition":
            "PASS_READY_FOR_SECONDARY_DESIGN"
            if gate["final_development_gate"]
            else "FAIL_STOP_BEFORE_SECONDARY",
    }

    out=OUT/"EXP-036-development-summary-v0.1.json"
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")

    print(json.dumps({
        "pooled_signal_edge":pooled_signal,
        "pooled_control_signal_edge":pooled_control,
        "pooled_factor_summary":result["pooled_factor_summary"],
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
