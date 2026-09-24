#!/usr/bin/env python3
"""EXP-037 Engine Q v0.1 zero-outcome cross-market volatility-spillover preflight."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pandas as pd

from engine_k_v0_1 import EXECUTION_MARKETS, download_pinned
from engine_m_v0_1 import build_mtf_bars
from engine_m_v0_2 import safe_deployability_overlay, self_tests_engine_m_v02
from engine_q_v0_1 import (
    metric_at_time,
    peer_breadth,
    arm_from_snapshot,
    find_breakout_trigger,
    find_limit_fill,
    self_tests_engine_q_v01,
)
from run_engine_k_v0_2_training_calibration import load_scoped_csv

ROOT=Path(__file__).resolve().parents[2]
CACHE=Path("/tmp/engine-q-v01-preflight")
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

START=pd.Timestamp("2026-03-23",tz="UTC")
SEALED_START=pd.Timestamp("2026-07-01",tz="UTC")


def synthetic_spillover_tests()->list[str]:
    tests=[]
    dt=pd.Timestamp("2026-04-06T10:05:00Z")

    def s(vr,close=100.0,lo=99.0,hi=101.0):
        return {
            "status":"ok","decision_ts":dt,"vr":vr,
            "close":close,"box_low":lo,"box_high":hi,
        }

    snap={
        "XAUUSD":s(0.8),
        "EURUSD":s(1.8),
        "GBPUSD":s(1.9),
        "USDJPY":s(2.0),
        "EURJPY":s(0.7),
        "AUDUSD":s(1.75),
        "USDCAD":s(0.9),
        "USDCHF":s(1.0),
    }
    b=peer_breadth(snap,"XAUUSD")
    assert b["valid_peer_count"]==7 and b["shock_count"]==4
    tests.append("four_of_seven_peer_shock")

    a=arm_from_snapshot("XAUUSD",snap)
    assert a["status"]=="armed"
    tests.append("lagging_candidate_arms")

    snap_bad={k:dict(v) for k,v in snap.items()}
    snap_bad["XAUUSD"]["close"]=101.0
    assert arm_from_snapshot("XAUUSD",snap_bad)["status"]=="candidate_outside_box"
    tests.append("candidate_must_remain_inside_fixed_box")

    snap_self={k:dict(v) for k,v in snap.items()}
    snap_self["EURUSD"]["vr"]=0.2
    snap_self["XAUUSD"]["vr"]=10.0
    b2=peer_breadth(snap_self,"XAUUSD")
    assert b2["shock_count"]==3
    tests.append("candidate_cannot_supply_own_peer_shock")

    return tests


def entry_usd_jpy_at(series:pd.Series|None,entry_ts:pd.Timestamp):
    if series is None:
        return None
    k=int(series.index.searchsorted(entry_ts,side="right"))-1
    if k<0:
        return None
    return float(series.iloc[k])


def main():
    tests={
        "engine_q_v01":self_tests_engine_q_v01(),
        "engine_m_v02_safe_overlay":self_tests_engine_m_v02(),
        "synthetic_spillover":synthetic_spillover_tests(),
    }

    data={}
    bars5={}
    for symbol in EXECUTION_MARKETS:
        path=download_pinned(symbol,CACHE)
        df=load_scoped_csv(path,symbol,SEALED_START)
        if df.empty or df["datetime"].max()>=SEALED_START:
            raise RuntimeError(f"{symbol}: protected-period leak")
        data[symbol]=df
        bars5[symbol]=build_mtf_bars(df)["m5"]

    usd_jpy_series=data["USDJPY"].set_index("datetime")["close"].sort_index()

    arm_status={s:Counter() for s in EXECUTION_MARKETS}
    trigger_status={s:Counter() for s in EXECUTION_MARKETS}
    fill_status={s:Counter() for s in EXECUTION_MARKETS}
    blocked={s:0 for s in EXECUTION_MARKETS}
    busy_until={s:pd.Timestamp.min.tz_localize("UTC") for s in EXECUTION_MARKETS}
    signals={s:0 for s in EXECUTION_MARKETS}
    deployable={s:0 for s in EXECUTION_MARKETS}
    by_dir={s:{"long":0,"short":0} for s in EXECUTION_MARKETS}
    utility={s:Counter() for s in EXECUTION_MARKETS}
    safe_max={s:{"risk":None,"notional":None,"margin":None} for s in EXECUTION_MARKETS}
    examples={s:[] for s in EXECUTION_MARKETS}

    days=pd.date_range(START.normalize(),SEALED_START-pd.Timedelta(days=1),freq="D",tz="UTC")
    for day in days:
        if day.weekday()>=5:
            continue
        for mins in range(6*60+5,17*60+25+1,5):
            decision_ts=day+pd.Timedelta(minutes=mins)
            snapshot={s:metric_at_time(bars5[s],decision_ts) for s in EXECUTION_MARKETS}

            for symbol in EXECUTION_MARKETS:
                if decision_ts<busy_until[symbol]:
                    blocked[symbol]+=1
                    continue

                arm=arm_from_snapshot(symbol,snapshot)
                arm_status[symbol][arm["status"]]+=1
                if arm["status"]!="armed":
                    continue

                trigger=find_breakout_trigger(bars5[symbol],symbol,arm)
                trigger_status[symbol][trigger["status"]]+=1
                if not trigger.get("triggered"):
                    busy_until[symbol]=trigger["resolved_ts"]
                    continue

                fill=find_limit_fill(data[symbol],trigger)
                busy_until[symbol]=fill["resolved_ts"]
                fill_status[symbol][fill["status"]]+=1
                if not fill.get("filled"):
                    continue

                entry=float(fill["entry"])
                stop=float(fill["stop"])
                uj=entry_usd_jpy_at(usd_jpy_series,fill["entry_ts"]) if symbol=="EURJPY" else None
                overlay=safe_deployability_overlay(symbol,entry,stop,uj)
                if overlay.get("reason") in (
                    "invalid_geometry","value_or_notional_unavailable",
                    "target_geometry_unavailable","invalid_stop_loss_per_lot"
                ):
                    continue

                signals[symbol]+=1
                by_dir[symbol][trigger["direction"]]+=1
                utility[symbol][overlay["utility_band"]]+=1

                if overlay["deployable"]:
                    deployable[symbol]+=1
                    for key,field in (
                        ("risk","stop_risk_usd"),
                        ("notional","notional_usd"),
                        ("margin","margin_usd"),
                    ):
                        val=float(overlay[field])
                        prev=safe_max[symbol][key]
                        safe_max[symbol][key]=val if prev is None else max(prev,val)

                if len(examples[symbol])<5:
                    examples[symbol].append({
                        "arm_decision_ts":str(arm["decision_ts"]),
                        "trigger_decision_ts":str(trigger["decision_ts"]),
                        "direction":trigger["direction"],
                        "peer_shock_count":trigger["peer_shock_count_at_arm"],
                        "candidate_vr_at_arm":trigger["candidate_vr_at_arm"],
                        "trigger_vr":trigger["trigger_vr"],
                        "arm_wait_m5_bars":trigger["arm_wait_m5_bars"],
                        "entry_ts":str(fill["entry_ts"]),
                        "entry":entry,
                        "stop":stop,
                        "safe_overlay":overlay,
                    })

    markets={}
    per_market_gate={}
    total=0
    total_deployable=0
    total_utility=Counter()
    safety_ok=True

    for s in EXECUTION_MARKETS:
        markets[s]={
            "arm_status_counts":dict(sorted(arm_status[s].items())),
            "trigger_status_counts":dict(sorted(trigger_status[s].items())),
            "blocked_due_active_arm_or_order":blocked[s],
            "fill_status_counts":dict(sorted(fill_status[s].items())),
            "filled_signal_paths":signals[s],
            "filled_by_direction":by_dir[s],
            "deployable_paths_safe_lot_ge_0_01":deployable[s],
            "utility_band_counts":dict(sorted(utility[s].items())),
            "safe_overlay_maxima":safe_max[s],
            "examples":examples[s],
        }
        per_market_gate[s]=signals[s]>=25 and by_dir[s]["long"]>0 and by_dir[s]["short"]>0
        total+=signals[s]
        total_deployable+=deployable[s]
        total_utility.update(utility[s])

        mx=safe_max[s]
        if mx["risk"] is not None and mx["risk"]>20.0+1e-9:
            safety_ok=False
        if mx["notional"] is not None and mx["notional"]>50000.0+1e-9:
            safety_ok=False
        if mx["margin"] is not None and mx["margin"]>100.0+1e-9:
            safety_ok=False

    gate={
        "each_market_ge_25_and_both_directions":all(per_market_gate.values()),
        "total_signal_paths_ge_300":total>=300,
        "safe_overlay_never_violates_caps":safety_ok,
        "protected_periods_sealed":True,
        "target_outcomes_calculated":False,
        "pnl_outcomes_calculated":False,
    }
    passed=bool(
        gate["each_market_ge_25_and_both_directions"]
        and gate["total_signal_paths_ge_300"]
        and gate["safe_overlay_never_violates_caps"]
        and gate["protected_periods_sealed"]
    )

    result={
        "experiment":"EXP-037",
        "engine":"Engine Q v0.1",
        "stage":"zero_outcome_cross_market_volatility_spillover_preflight",
        "target_outcomes_calculated":False,
        "pnl_outcomes_calculated":False,
        "secondary_test_loaded_or_inspected":False,
        "final_holdout_loaded_or_inspected":False,
        "parsed_market_data_max_timestamp":str(max(df["datetime"].max() for df in data.values())),
        "tests":tests,
        "markets":markets,
        "per_market_gate":per_market_gate,
        "gate":gate,
        "totals":{
            "filled_signal_paths":total,
            "deployable_paths_safe_lot_ge_0_01":total_deployable,
            "utility_band_counts":dict(sorted(total_utility.items())),
        },
        "preflight_pass":passed,
    }

    out=OUT/"EXP-037-cross-market-volatility-spillover-preflight-v0.1.json"
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")
    print(json.dumps({
        "preflight_pass":passed,
        "per_market_gate":per_market_gate,
        "totals":result["totals"],
        "target_outcomes_calculated":False,
        "pnl_outcomes_calculated":False,
        "secondary_test_loaded_or_inspected":False,
        "final_holdout_loaded_or_inspected":False,
    },indent=2))


if __name__=="__main__":
    main()
