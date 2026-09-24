#!/usr/bin/env python3
"""Engine O v0.1 — rolling statistical stretch reversion mechanics."""

from __future__ import annotations

import math
import pandas as pd

from engine_k_v0_1 import MAX_NEXT_ENTRY_GAP_MINUTES
from engine_k_v0_2 import native_target_distances_v02, research_tick

BASELINE_M5_BARS=24
STRETCH_MAD_MULTIPLE=2.50
TRIGGER_RANGE_MULTIPLE=1.25
BODY_FRACTION=0.50
CLOSE_OUTER_FRACTION=0.35
ORDER_ACTIVE_M1_BARS=10
ORDER_HARD_MINUTES=30
ENTRY_CUTOFF_HOUR=18


def even_median(values:list[float])->float:
    if len(values)==0 or len(values)%2!=0:
        raise ValueError("even_median requires a non-empty even-length list")
    xs=sorted(float(x) for x in values)
    n=len(xs)
    return (xs[n//2-1]+xs[n//2])/2.0


def decision_allowed(ts:pd.Timestamp)->bool:
    minutes=ts.hour*60+ts.minute
    return (
        ts.weekday()<5
        and 6*60+15<=minutes<=17*60+45
        and ts.minute in (0,15,30,45)
    )


def setup_at(
    bars5:pd.DataFrame,
    index:int,
    symbol:str,
)->dict:
    t=bars5.iloc[index]
    decision_ts=t["available_ts"]

    if not decision_allowed(decision_ts):
        return {"status":"outside_decision_grid","decision_ts":decision_ts}

    if index<BASELINE_M5_BARS:
        return {"status":"baseline_24x5_unavailable","decision_ts":decision_ts}

    prev=bars5.iloc[index-BASELINE_M5_BARS:index]
    trigger_start=t["datetime"]
    expected=[
        trigger_start-pd.Timedelta(minutes=5*(BASELINE_M5_BARS-i))
        for i in range(BASELINE_M5_BARS)
    ]
    if list(prev["datetime"])!=expected:
        return {"status":"baseline_24x5_not_contiguous","decision_ts":decision_ts}

    closes=[float(x) for x in prev["close"]]
    ranges=[float(r.high-r.low) for r in prev.itertuples()]
    center=even_median(closes)
    mad=even_median([abs(x-center) for x in closes])
    range_median=even_median(ranges)

    if not math.isfinite(mad) or mad<=0:
        return {
            "status":"baseline_mad_zero",
            "decision_ts":decision_ts,
            "center":center,
        }
    if not math.isfinite(range_median) or range_median<=0:
        return {
            "status":"baseline_range_zero",
            "decision_ts":decision_ts,
            "center":center,
            "mad":mad,
        }

    op=float(t["open"]); hi=float(t["high"]); lo=float(t["low"]); cl=float(t["close"])
    rng=hi-lo
    if not math.isfinite(rng) or rng<=0:
        return {
            "status":"trigger_zero_range",
            "decision_ts":decision_ts,
            "center":center,
            "mad":mad,
            "range_median":range_median,
        }

    stretch=abs(cl-center)
    if stretch+1e-12 < STRETCH_MAD_MULTIPLE*mad:
        return {
            "status":"stretch_failed",
            "decision_ts":decision_ts,
            "center":center,
            "mad":mad,
            "stretch":stretch,
        }

    if rng+1e-12 < TRIGGER_RANGE_MULTIPLE*range_median:
        return {
            "status":"trigger_range_failed",
            "decision_ts":decision_ts,
            "center":center,
            "mad":mad,
            "range_median":range_median,
            "trigger_range":rng,
        }

    body=abs(cl-op)
    if body+1e-12 < BODY_FRACTION*rng:
        return {
            "status":"trigger_body_failed",
            "decision_ts":decision_ts,
            "center":center,
            "trigger_range":rng,
            "trigger_body":body,
        }

    if cl<center:
        direction="long"
        if not cl>op:
            return {"status":"rejection_direction_failed","decision_ts":decision_ts,"direction":direction}
        if hi-cl > CLOSE_OUTER_FRACTION*rng+1e-12:
            return {"status":"rejection_close_location_failed","decision_ts":decision_ts,"direction":direction}
    elif cl>center:
        direction="short"
        if not cl<op:
            return {"status":"rejection_direction_failed","decision_ts":decision_ts,"direction":direction}
        if cl-lo > CLOSE_OUTER_FRACTION*rng+1e-12:
            return {"status":"rejection_close_location_failed","decision_ts":decision_ts,"direction":direction}
    else:
        return {"status":"trigger_at_center","decision_ts":decision_ts}

    limit=(hi+lo)/2.0
    tick=research_tick(symbol)
    stop=lo-tick if direction=="long" else hi+tick

    if direction=="long" and not limit<cl:
        return {"status":"non_chasing_geometry_failed","decision_ts":decision_ts,"direction":direction}
    if direction=="short" and not limit>cl:
        return {"status":"non_chasing_geometry_failed","decision_ts":decision_ts,"direction":direction}

    distances=native_target_distances_v02(symbol,limit,stop)
    d=distances.get("T40")
    if d is None or not math.isfinite(d) or d<=0:
        return {"status":"t40_geometry_unavailable","decision_ts":decision_ts,"direction":direction}

    target_price=limit+d if direction=="long" else limit-d
    room_ok=target_price<=center if direction=="long" else target_price>=center
    if not room_ok:
        return {
            "status":"center_target_room_failed",
            "decision_ts":decision_ts,
            "direction":direction,
            "center":center,
            "limit":limit,
            "stop":stop,
            "target_distance":float(d),
            "target_price":float(target_price),
        }

    return {
        "status":"armed",
        "decision_ts":decision_ts,
        "direction":direction,
        "trigger_start":t["datetime"],
        "center":float(center),
        "mad":float(mad),
        "range_median":float(range_median),
        "stretch":float(stretch),
        "stretch_mad_multiple":float(stretch/mad),
        "trigger_open":op,
        "trigger_high":hi,
        "trigger_low":lo,
        "trigger_close":cl,
        "trigger_range":float(rng),
        "trigger_body_fraction":float(body/rng),
        "limit":float(limit),
        "stop":float(stop),
        "target_distance":float(d),
        "target_price":float(target_price),
        "limit_improvement_native":float(cl-limit if direction=="long" else limit-cl),
        "limit_improvement_trigger_range":float((cl-limit)/rng if direction=="long" else (limit-cl)/rng),
    }


def find_limit_fill(df1:pd.DataFrame,setup:dict)->dict:
    if setup.get("status")!="armed":
        raise ValueError("find_limit_fill requires armed setup")

    decision_ts=setup["decision_ts"]
    direction=setup["direction"]
    limit=float(setup["limit"])
    stop=float(setup["stop"])
    hard_cutoff=min(
        decision_ts+pd.Timedelta(minutes=ORDER_HARD_MINUTES),
        decision_ts.normalize()+pd.Timedelta(hours=ENTRY_CUTOFF_HOUR),
    )

    start=int(df1["datetime"].searchsorted(decision_ts,side="left"))
    if start>=len(df1):
        return {"status":"no_m1_after_decision","resolved_ts":decision_ts,"filled":False}

    end=min(start+ORDER_ACTIVE_M1_BARS,len(df1))
    prev_ts=decision_ts
    last_ts=decision_ts

    for pos in range(start,end):
        row=df1.iloc[pos]
        ts=row["datetime"]
        last_ts=ts
        if ts>=hard_cutoff:
            return {"status":"expired_hard_cutoff","resolved_ts":hard_cutoff,"filled":False}
        if ts-prev_ts>pd.Timedelta(minutes=MAX_NEXT_ENTRY_GAP_MINUTES):
            return {"status":"cancel_gap","resolved_ts":ts,"filled":False}
        prev_ts=ts

        op=float(row["open"]); hi=float(row["high"]); lo=float(row["low"])

        if direction=="long":
            if op<=stop:
                return {"status":"gap_through_stop","resolved_ts":ts,"filled":False}
            touched=lo<=limit
            stop_touched=lo<=stop
        else:
            if op>=stop:
                return {"status":"gap_through_stop","resolved_ts":ts,"filled":False}
            touched=hi>=limit
            stop_touched=hi>=stop

        if not touched:
            continue

        return {
            "status":"filled",
            "resolved_ts":ts,
            "filled":True,
            "entry_ts":ts,
            "entry":limit,
            "stop":stop,
            "fill_bar_stop_touched":bool(stop_touched),
            "wait_active_m1_bars":pos-start+1,
            "entry_improvement_native":float(setup["limit_improvement_native"]),
            "entry_improvement_trigger_range":float(setup["limit_improvement_trigger_range"]),
            "stop_distance_native":abs(limit-stop),
        }

    return {
        "status":"expired_unfilled",
        "resolved_ts":last_ts+pd.Timedelta(minutes=1),
        "filled":False,
    }


def self_tests_engine_o_v01()->list[str]:
    tests=[]

    assert even_median([1,2,3,4])==2.5
    assert even_median(list(range(1,25)))==12.5
    tests.append("even_median_exact")

    vals=[10.0]*12+[12.0]*12
    c=even_median(vals)
    assert c==11.0
    mad=even_median([abs(x-c) for x in vals])
    assert mad==1.0
    tests.append("mad_exact")

    assert 2.5+1e-12>=STRETCH_MAD_MULTIPLE*1.0
    assert 1.25+1e-12>=TRIGGER_RANGE_MULTIPLE*1.0
    assert 0.5+1e-12>=BODY_FRACTION*1.0
    assert 0.35<=CLOSE_OUTER_FRACTION+1e-12
    tests.append("frozen_threshold_boundaries")

    base=pd.Timestamp("2026-04-06T06:15:00Z")
    assert decision_allowed(base)
    assert decision_allowed(pd.Timestamp("2026-04-06T17:45:00Z"))
    assert not decision_allowed(pd.Timestamp("2026-04-06T18:00:00Z"))
    tests.append("decision_grid")

    return tests
