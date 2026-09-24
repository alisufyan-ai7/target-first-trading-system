#!/usr/bin/env python3
"""EXP-027 Engine M v0.1 zero-outcome MTF + limit-entry preflight."""

from __future__ import annotations

import json
import statistics
from collections import Counter
from pathlib import Path

import pandas as pd

from engine_k_v0_1 import EXECUTION_MARKETS, download_pinned
from engine_m_v0_1 import (
    build_mtf_bars,
    mtf_setup_at,
    find_limit_fill,
    self_tests_engine_m,
)
from run_engine_k_v0_2_training_calibration import load_scoped_csv

ROOT=Path(__file__).resolve().parents[2]
CACHE=Path("/tmp/engine-m-v01-preflight")
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

START=pd.Timestamp("2026-03-23",tz="UTC")
SEALED_START=pd.Timestamp("2026-07-01",tz="UTC")


def synthetic_setup_tests()->list[str]:
    tests=[]
    # Long aligned context + H1 midpoint reclaim + final M5 rejection.
    h4=pd.DataFrame({
        "datetime":pd.to_datetime(["2026-04-06T00:00Z","2026-04-06T04:00Z"]),
        "available_ts":pd.to_datetime(["2026-04-06T04:00Z","2026-04-06T08:00Z"]),
        "open":[1.0,1.0],"high":[2.0,2.4],"low":[0.5,0.8],"close":[1.0,2.0],"volume":[1,1],"n":[240,240],
    })
    h1=pd.DataFrame({
        "datetime":pd.to_datetime(["2026-04-06T06:00Z","2026-04-06T07:00Z"]),
        "available_ts":pd.to_datetime(["2026-04-06T07:00Z","2026-04-06T08:00Z"]),
        "open":[1.0,1.8],"high":[2.0,2.2],"low":[1.0,1.8],"close":[1.5,2.1],"volume":[1,1],"n":[60,60],
    })
    m15=pd.DataFrame({
        "datetime":pd.to_datetime(["2026-04-06T08:00Z"]),
        "available_ts":pd.to_datetime(["2026-04-06T08:15Z"]),
        "open":[2.05],"high":[2.13],"low":[1.95],"close":[2.10],"volume":[1],"n":[15],
    })
    m5=pd.DataFrame({
        "datetime":pd.to_datetime(["2026-04-06T08:05Z","2026-04-06T08:10Z"]),
        "available_ts":pd.to_datetime(["2026-04-06T08:10Z","2026-04-06T08:15Z"]),
        "open":[2.00,2.00],"high":[2.08,2.12],"low":[1.98,1.98],"close":[2.00,2.10],
        "volume":[1,1],"n":[5,5],
    })
    x=mtf_setup_at({"h4":h4,"h1":h1,"m15":m15,"m5":m5},0)
    assert x["status"]=="armed" and x["direction"]=="long"
    assert x["limit"]<x["a5_close"]
    assert x["limit_improvement_a5_range"]>0
    tests.append("synthetic_long_mtf_arm")

    # Short mirror.
    h4s=h4.copy(); h4s.loc[1,"close"]=0.8
    h1s=h1.copy(); h1s.loc[1,"close"]=1.2
    h1s.loc[1,"high"]=1.4; h1s.loc[1,"low"]=1.0
    m15s=m15.copy(); m15s.loc[0,["open","high","low","close"]]=[1.25,1.25,1.05,1.10]
    m5s=m5.copy()
    m5s.loc[0,["open","high","low","close"]]=[1.20,1.22,1.12,1.18]
    m5s.loc[1,["open","high","low","close"]]=[1.18,1.20,1.04,1.06]
    y=mtf_setup_at({"h4":h4s,"h1":h1s,"m15":m15s,"m5":m5s},0)
    assert y["status"]=="armed" and y["direction"]=="short"
    assert y["limit"]>y["a5_close"]
    assert y["limit_improvement_a5_range"]>0
    tests.append("synthetic_short_mtf_arm")
    return tests


def synthetic_fill_tests()->list[str]:
    tests=[]
    t=pd.date_range("2026-04-06T10:00:00Z",periods=12,freq="1min")
    base=pd.DataFrame({
        "datetime":t,
        "open":[100.7]*12,
        "high":[100.8]*12,
        "low":[100.6]*12,
        "close":[100.7]*12,
        "volume":[1]*12,
    })
    arm={
        "status":"armed","direction":"long","decision_ts":t[0],
        "a5_low":99.5,"a5_high":101.5,"a5_close":101.2,
        "limit":100.5,"limit_improvement_native":0.7,
        "limit_improvement_a5_range":0.35,
    }
    df=base.copy()
    df.loc[2,"low"]=100.4
    x=find_limit_fill(df,arm,"XAUUSD")
    assert x["status"]=="admissible_fill" and x["entry_ts"]==t[2]
    assert abs(x["entry"]-100.5)<1e-12
    assert x["entry_improvement_native"]>0
    tests.append("long_limit_fill_at_precomputed_price")

    # Same fill bar touches stop: mechanics flags it for later stop-first outcome.
    df2=base.copy()
    df2.loc[2,"low"]=99.4
    y=find_limit_fill(df2,arm,"XAUUSD")
    assert y["filled"] and y["fill_bar_stop_touched"] is True
    tests.append("fill_bar_stop_touch_flagged")

    # Opening through stop cancels rather than assuming a favorable fill.
    df3=base.copy()
    df3.loc[1,["open","high","low","close"]]=[99.0,99.2,98.8,99.1]
    z=find_limit_fill(df3,arm,"XAUUSD")
    assert z["status"]=="gap_through_stop" and not z["filled"]
    tests.append("gap_through_stop_cancelled")

    # No retracement within ten active M1 bars => expiry.
    w=find_limit_fill(base,arm,"XAUUSD")
    assert w["status"]=="expired_unfilled" and not w["filled"]
    tests.append("ten_m1_expiry")
    return tests


def market_preflight(symbol:str,df1:pd.DataFrame,usd_jpy_df:pd.DataFrame|None=None)->dict:
    bars=build_mtf_bars(df1)
    usd_jpy_series=None
    if usd_jpy_df is not None:
        usd_jpy_series=usd_jpy_df.set_index("datetime")["close"].sort_index()

    setup_status=Counter()
    fill_status=Counter()
    context_counts=Counter()
    admissible_by_direction={"long":0,"short":0}
    armed_by_direction={"long":0,"short":0}
    pending_until=pd.Timestamp.min.tz_localize("UTC")
    blocked_pending=0
    fills=0
    admissible=0
    waits=[]
    improvements=[]
    stop_dist=[]
    examples=[]

    for i in range(len(bars["m15"])):
        decision_ts=bars["m15"].iloc[i]["available_ts"]
        if decision_ts<START or decision_ts>=SEALED_START:
            continue
        if decision_ts.weekday()>=5 or decision_ts.hour>=18:
            continue

        setup=mtf_setup_at(bars,i)
        direction=setup.get("direction","neutral")
        context_counts[direction]+=1
        setup_status[setup["status"]]+=1
        if setup["status"]!="armed":
            continue
        if decision_ts<pending_until:
            blocked_pending+=1
            continue

        armed_by_direction[direction]+=1
        fill=find_limit_fill(df1,setup,symbol,usd_jpy_series)
        pending_until=fill["resolved_ts"]
        fill_status[fill["status"]]+=1
        if fill.get("filled"):
            fills+=1
        if fill["status"]!="admissible_fill":
            continue

        admissible+=1
        admissible_by_direction[direction]+=1
        waits.append(int(fill["wait_active_m1_bars"]))
        improvements.append(float(fill["entry_improvement_a5_range"]))
        stop_dist.append(float(fill["stop_distance_native"]))
        if len(examples)<4:
            examples.append({
                "decision_ts":str(decision_ts),
                "direction":direction,
                "h1_mid":setup["h1_mid"],
                "a5_close":setup["a5_close"],
                "limit":setup["limit"],
                "entry":fill,
            })

    return {
        "bar_counts":{k:len(v) for k,v in bars.items()},
        "context_counts":dict(sorted(context_counts.items())),
        "setup_status_counts":dict(sorted(setup_status.items())),
        "armed_by_direction":armed_by_direction,
        "blocked_setups_due_pending_order":blocked_pending,
        "fill_status_counts":dict(sorted(fill_status.items())),
        "mechanical_fills":fills,
        "admissible_entry_paths":admissible,
        "admissible_by_direction":admissible_by_direction,
        "median_wait_active_m1_bars":statistics.median(waits) if waits else None,
        "median_entry_improvement_a5_range":statistics.median(improvements) if improvements else None,
        "median_stop_distance_native":statistics.median(stop_dist) if stop_dist else None,
        "examples":examples,
    }


def main():
    tests={
        "engine_m":self_tests_engine_m(),
        "synthetic_setup":synthetic_setup_tests(),
        "synthetic_fill":synthetic_fill_tests(),
    }

    data={}
    for symbol in EXECUTION_MARKETS:
        path=download_pinned(symbol,CACHE)
        df=load_scoped_csv(path,symbol,SEALED_START)
        if df.empty or df["datetime"].max()>=SEALED_START:
            raise RuntimeError(f"{symbol}: protected-period leak")
        data[symbol]=df

    markets={}
    for symbol in EXECUTION_MARKETS:
        uj=data["USDJPY"] if symbol=="EURJPY" else None
        markets[symbol]=market_preflight(symbol,data[symbol],uj)

    per_market_gate={
        s:(
            markets[s]["admissible_entry_paths"]>=50
            and markets[s]["admissible_by_direction"]["long"]>0
            and markets[s]["admissible_by_direction"]["short"]>0
        )
        for s in EXECUTION_MARKETS
    }
    total=sum(x["admissible_entry_paths"] for x in markets.values())
    gate={
        "each_market_ge_50_and_both_directions":all(per_market_gate.values()),
        "total_admissible_paths_ge_600":total>=600,
        "protected_periods_sealed":True,
        "target_outcomes_calculated":False,
        "pnl_outcomes_calculated":False,
    }
    passed=bool(
        gate["each_market_ge_50_and_both_directions"]
        and gate["total_admissible_paths_ge_600"]
        and gate["protected_periods_sealed"]
    )

    result={
        "experiment":"EXP-027",
        "engine":"Engine M v0.1",
        "stage":"zero_outcome_mtf_limit_mechanics_preflight",
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
            "admissible_entry_paths":total,
            "mechanical_fills":sum(x["mechanical_fills"] for x in markets.values()),
        },
        "preflight_pass":passed,
    }
    out=OUT/"EXP-027-entry-mechanics-preflight-v0.1.json"
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
