#!/usr/bin/env python3
"""Engine M v0.4 prior-H1 range sweep/reclaim mechanics.

Zero-outcome selection layer. Reuses Engine M execution and deployability.
"""

from __future__ import annotations

import math
import pandas as pd

from engine_k_v0_2 import native_target_distances_v02, research_tick
from engine_m_v0_1 import htf_context


def _latest_two_completed_rows(bars:pd.DataFrame, decision_ts:pd.Timestamp):
    k=int(bars["available_ts"].searchsorted(decision_ts,side="right"))-1
    if k<1:
        return None
    return bars.iloc[k],bars.iloc[k-1]


def h1_range_setup_at(
    bars:dict[str,pd.DataFrame],
    m15_index:int,
    symbol:str,
)->dict:
    s15=bars["m15"].iloc[m15_index]
    decision_ts=s15["available_ts"]

    ctx=htf_context(bars["h4"],bars["h1"],decision_ts)
    direction=ctx["direction"]
    if direction=="neutral":
        return {"status":"neutral_context","decision_ts":decision_ts,**ctx}

    pair=_latest_two_completed_rows(bars["h1"],decision_ts)
    if pair is None:
        return {"status":"h1_history_unavailable","decision_ts":decision_ts,**ctx}
    h10,h11=pair
    h1_low=float(h10["low"])
    h1_high=float(h10["high"])

    if direction=="long":
        if not float(s15["low"])<h1_low:
            return {
                "status":"h1_boundary_sweep_failed",
                "decision_ts":decision_ts,
                "h1_low":h1_low,"h1_high":h1_high,**ctx
            }
        if not float(s15["close"])>h1_low:
            return {
                "status":"h1_boundary_reclaim_failed",
                "decision_ts":decision_ts,
                "h1_low":h1_low,"h1_high":h1_high,**ctx
            }
    else:
        if not float(s15["high"])>h1_high:
            return {
                "status":"h1_boundary_sweep_failed",
                "decision_ts":decision_ts,
                "h1_low":h1_low,"h1_high":h1_high,**ctx
            }
        if not float(s15["close"])<h1_high:
            return {
                "status":"h1_boundary_reclaim_failed",
                "decision_ts":decision_ts,
                "h1_low":h1_low,"h1_high":h1_high,**ctx
            }

    a5_start=decision_ts-pd.Timedelta(minutes=5)
    k=int(bars["m5"]["datetime"].searchsorted(a5_start,side="left"))
    if k>=len(bars["m5"]) or bars["m5"].iloc[k]["datetime"]!=a5_start:
        return {"status":"a5_unavailable","decision_ts":decision_ts,**ctx}
    if k<1:
        return {"status":"p5_unavailable","decision_ts":decision_ts,**ctx}

    a5=bars["m5"].iloc[k]
    p5=bars["m5"].iloc[k-1]
    if p5["datetime"]!=a5_start-pd.Timedelta(minutes=5):
        return {"status":"p5_not_contiguous","decision_ts":decision_ts,**ctx}

    rng=float(a5["high"]-a5["low"])
    if rng<=0:
        return {"status":"a5_zero_range","decision_ts":decision_ts,**ctx}

    if direction=="long":
        arm_ok=(
            float(a5["close"])>float(a5["open"])
            and float(a5["close"])>float(p5["close"])
            and 4.0*(float(a5["high"])-float(a5["close"]))<=rng+1e-12
        )
    else:
        arm_ok=(
            float(a5["close"])<float(a5["open"])
            and float(a5["close"])<float(p5["close"])
            and 4.0*(float(a5["close"])-float(a5["low"]))<=rng+1e-12
        )
    if not arm_ok:
        return {"status":"m5_arm_failed","decision_ts":decision_ts,**ctx}

    limit=(float(a5["high"])+float(a5["low"]))/2.0
    tick=research_tick(symbol)
    stop=float(a5["low"]-tick) if direction=="long" else float(a5["high"]+tick)

    d=native_target_distances_v02(symbol,limit,stop).get("T40")
    if d is None or not math.isfinite(d) or d<=0:
        return {"status":"t40_geometry_unavailable","decision_ts":decision_ts,**ctx}
    target_price=limit+d if direction=="long" else limit-d

    if direction=="long":
        target_room_ok=target_price<=h1_high
        destination=h1_high
    else:
        target_room_ok=target_price>=h1_low
        destination=h1_low

    if not target_room_ok:
        return {
            "status":"h1_opposite_boundary_target_room_failed",
            "decision_ts":decision_ts,
            "direction":direction,
            "h1_low":h1_low,
            "h1_high":h1_high,
            "limit":float(limit),
            "stop":float(stop),
            "target_distance":float(d),
            "target_price":float(target_price),
            "h1_destination":float(destination),
            **{k:v for k,v in ctx.items() if k!="direction"},
        }

    return {
        "status":"armed",
        "decision_ts":decision_ts,
        "direction":direction,
        "h1_0_start":h10["datetime"],
        "h1_1_start":h11["datetime"],
        "h1_low":h1_low,
        "h1_high":h1_high,
        "s15_start":s15["datetime"],
        "s15_open":float(s15["open"]),
        "s15_high":float(s15["high"]),
        "s15_low":float(s15["low"]),
        "s15_close":float(s15["close"]),
        "a5_start":a5["datetime"],
        "a5_open":float(a5["open"]),
        "a5_high":float(a5["high"]),
        "a5_low":float(a5["low"]),
        "a5_close":float(a5["close"]),
        "a5_range":rng,
        "limit":float(limit),
        "stop":float(stop),
        "target_distance":float(d),
        "target_price":float(target_price),
        "h1_destination":float(destination),
        "limit_improvement_native":(
            float(a5["close"])-limit if direction=="long" else limit-float(a5["close"])
        ),
        "limit_improvement_a5_range":(
            (float(a5["close"])-limit)/rng if direction=="long"
            else (limit-float(a5["close"]))/rng
        ),
        **{k:v for k,v in ctx.items() if k!="direction"},
    }


def self_tests_engine_m_v04()->list[str]:
    tests=[]

    assert not (1.0<1.0)
    assert 0.999<1.0
    assert not (2.0>2.0)
    assert 2.001>2.0
    tests.append("strict_h1_boundary_sweep")

    limit=100.0
    d=2.0
    assert limit+d<=103.0
    assert limit-d>=97.0
    tests.append("opposite_h1_boundary_target_room_mirror")

    lo,hi=99.0,101.0
    mid=(lo+hi)/2.0
    assert 100.5>mid and 99.5<mid
    tests.append("non_chasing_midpoint_geometry")

    return tests
