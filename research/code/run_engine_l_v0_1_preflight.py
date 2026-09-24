#!/usr/bin/env python3
"""EXP-026 Engine L v0.1 zero-outcome entry mechanics preflight."""

from __future__ import annotations

import json
import statistics
from collections import Counter
from pathlib import Path

import pandas as pd

from engine_k_v0_1 import (
    EXECUTION_MARKETS,
    build_context,
    _latest_confirmed_pivot,
    download_pinned,
)
from engine_k_v0_2 import research_tick
from engine_l_v0_1 import (
    ARM_ACTIVE_M1_BARS,
    PULLBACK_V5_FRACTION,
    find_micro_entry,
    self_tests_engine_l,
)
from run_engine_k_v0_2_training_calibration import load_scoped_csv

ROOT=Path(__file__).resolve().parents[2]
CACHE=Path("/tmp/engine-l-v01-preflight")
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

START=pd.Timestamp("2026-03-23",tz="UTC")
SEALED_START=pd.Timestamp("2026-07-01",tz="UTC")


def synthetic_entry_tests()->list[str]:
    tests=[]

    # Long: exact pullback threshold, then causal resumption, then next-open entry.
    t=pd.date_range("2026-04-06T10:00:00Z",periods=8,freq="1min")
    long_df=pd.DataFrame({
        "datetime":t,
        "open":[4000.0,4000.0,3999.85,4000.19,4000.2,4000.2,4000.2,4000.2],
        "high":[4000.1,4000.0,4000.2,4000.3,4000.3,4000.3,4000.3,4000.3],
        "low":[3999.9,3999.8,3999.79,4000.1,4000.1,4000.1,4000.1,4000.1],
        "close":[4000.0,3999.85,4000.18,4000.2,4000.2,4000.2,4000.2,4000.2],
        "volume":[1]*8,
    })
    x=find_micro_entry(
        long_df,t[0],4000.0,1.0,"long",3998.0,"XAUUSD"
    )
    assert x["status"]=="admissible_entry"
    assert x["entry_ts"]==t[3]
    assert abs(x["stop"]-(3999.79-0.001))<1e-9
    tests.append("synthetic_long_exact_pullback_resume")

    # Short mirror.
    short_df=pd.DataFrame({
        "datetime":t,
        "open":[4000.0,4000.0,4000.15,3999.81,3999.8,3999.8,3999.8,3999.8],
        "high":[4000.1,4000.2,4000.21,3999.9,3999.9,3999.9,3999.9,3999.9],
        "low":[3999.9,4000.0,3999.8,3999.7,3999.7,3999.7,3999.7,3999.7],
        "close":[4000.0,4000.15,3999.82,3999.8,3999.8,3999.8,3999.8,3999.8],
        "volume":[1]*8,
    })
    x=find_micro_entry(
        short_df,t[0],4000.0,1.0,"short",4002.0,"XAUUSD"
    )
    assert x["status"]=="admissible_entry"
    assert x["entry_ts"]==t[3]
    assert abs(x["stop"]-(4000.21+0.001))<1e-9
    tests.append("synthetic_short_exact_pullback_resume")

    # Old invalidation cancels before entry.
    bad=long_df.copy()
    bad.loc[1,"low"]=3997.9
    x=find_micro_entry(bad,t[0],4000.0,1.0,"long",3998.0,"XAUUSD")
    assert x["status"]=="cancel_old_invalidation"
    tests.append("old_invalidation_cancels")

    # Frozen constants.
    assert ARM_ACTIVE_M1_BARS==15
    assert abs(PULLBACK_V5_FRACTION-0.20)<1e-12
    tests.append("frozen_entry_constants")

    return tests


def preflight_market(symbol:str,df1:pd.DataFrame,usd_jpy_df:pd.DataFrame|None=None)->dict:
    b5,_=build_context(df1)
    tick=research_tick(symbol)
    usd_jpy_series=None
    if usd_jpy_df is not None:
        usd_jpy_series=usd_jpy_df.set_index("datetime")["close"].sort_index()

    statuses=Counter()
    examined=0
    valid_old_geometry=0
    admissible=0
    by_direction={"long":0,"short":0}
    waits=[]
    pullback_v5=[]
    stop_dist=[]
    displacement_v5=[]
    examples=[]

    for i in range(50,len(b5)):
        row=b5.iloc[i]
        decision_end=row["datetime"]+pd.Timedelta(minutes=5)
        if decision_end>=SEALED_START:
            break
        if decision_end<START or decision_end.weekday()>=5:
            continue
        if decision_end.hour>=20:
            continue
        v5=float(row["median_tr20_5m"])
        if not pd.notna(v5) or v5<=0:
            continue
        c0=float(row["close"])

        for direction in ("long","short"):
            examined+=1
            pivot=_latest_confirmed_pivot(b5,i,direction)
            if pivot is None:
                statuses["no_old_pivot"]+=1
                continue
            old_inv=pivot-tick if direction=="long" else pivot+tick
            if direction=="long" and not old_inv<c0:
                statuses["invalid_old_geometry"]+=1
                continue
            if direction=="short" and not old_inv>c0:
                statuses["invalid_old_geometry"]+=1
                continue
            valid_old_geometry+=1

            x=find_micro_entry(
                df1=df1,
                decision_end=decision_end,
                decision_close=c0,
                v5=v5,
                direction=direction,
                old_invalidation=old_inv,
                symbol=symbol,
                usd_jpy_series=usd_jpy_series,
            )
            statuses[x["status"]]+=1
            if x["status"]!="admissible_entry":
                continue

            admissible+=1
            by_direction[direction]+=1
            waits.append(int(x["wait_active_m1_bars"]))
            pullback_v5.append(float(x["pullback_depth_v5"]))
            stop_dist.append(float(x["fresh_stop_distance_native"]))
            displacement_v5.append(float(x["entry_directional_displacement_v5"]))
            if len(examples)<4:
                examples.append({
                    "decision_end":str(decision_end),
                    "direction":direction,
                    "old_invalidation":old_inv,
                    "decision_close":c0,
                    "v5":v5,
                    "entry":x,
                })

    return {
        "decision_direction_paths_examined":examined,
        "valid_old_geometry_paths":valid_old_geometry,
        "status_counts":dict(sorted(statuses.items())),
        "admissible_entry_paths":admissible,
        "admissible_by_direction":by_direction,
        "median_wait_active_m1_bars":statistics.median(waits) if waits else None,
        "median_pullback_depth_v5":statistics.median(pullback_v5) if pullback_v5 else None,
        "median_fresh_stop_distance_native":statistics.median(stop_dist) if stop_dist else None,
        "median_entry_directional_displacement_v5":statistics.median(displacement_v5) if displacement_v5 else None,
        "examples":examples,
    }


def main():
    tests=self_tests_engine_l()+synthetic_entry_tests()

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
        markets[symbol]=preflight_market(symbol,data[symbol],uj)

    market_gate={
        s:(
            markets[s]["admissible_entry_paths"]>=100
            and markets[s]["admissible_by_direction"]["long"]>0
            and markets[s]["admissible_by_direction"]["short"]>0
        )
        for s in EXECUTION_MARKETS
    }
    passed=all(market_gate.values())

    result={
        "experiment":"EXP-026",
        "engine":"Engine L v0.1",
        "stage":"zero_outcome_entry_mechanics_preflight",
        "target_outcomes_calculated":False,
        "pnl_outcomes_calculated":False,
        "forecast_model_fitted":False,
        "secondary_test_loaded_or_inspected":False,
        "final_holdout_loaded_or_inspected":False,
        "parsed_market_data_max_timestamp":str(max(df["datetime"].max() for df in data.values())),
        "self_tests":tests,
        "markets":markets,
        "market_gate_ge_100_and_both_directions":market_gate,
        "preflight_pass":passed,
        "totals":{
            "admissible_entry_paths":sum(x["admissible_entry_paths"] for x in markets.values()),
            "examined_paths":sum(x["decision_direction_paths_examined"] for x in markets.values()),
        },
    }

    out=OUT/"EXP-026-entry-mechanics-preflight-v0.1.json"
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")
    print(json.dumps({
        "preflight_pass":passed,
        "market_gate":market_gate,
        "totals":result["totals"],
        "target_outcomes_calculated":False,
        "pnl_outcomes_calculated":False,
        "secondary_test_loaded_or_inspected":False,
        "final_holdout_loaded_or_inspected":False,
    },indent=2))
    if not passed:
        raise SystemExit("EXP-026 entry-mechanics preflight gate failed")


if __name__=="__main__":
    main()
