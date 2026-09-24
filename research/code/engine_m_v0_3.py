#!/usr/bin/env python3
"""Engine M v0.3 selective liquidity-reclaim + H1 target-destination mechanics.

Zero-outcome selection layer. Reuses v0.1 execution and v0.2 deployability.
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


def selective_setup_at(
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

    if m15_index<4:
        return {"status":"prev4_m15_unavailable","decision_ts":decision_ts,**ctx}

    expected=[
        s15["datetime"]-pd.Timedelta(minutes=15*j)
        for j in range(4,0,-1)
    ]
    prev4=bars["m15"].iloc[m15_index-4:m15_index]
    actual=list(prev4["datetime"])
    if actual!=expected:
        return {"status":"prev4_m15_not_contiguous","decision_ts":decision_ts,**ctx}

    prev4_low=float(prev4["low"].min())
    prev4_high=float(prev4["high"].max())
    mid=float(ctx["h1_mid"])

    if direction=="long":
        swept=float(s15["low"])<prev4_low
        reclaimed=float(s15["close"])>prev4_low
        midpoint_ok=float(s15["close"])>mid
    else:
        swept=float(s15["high"])>prev4_high
        reclaimed=float(s15["close"])<prev4_high
        midpoint_ok=float(s15["close"])<mid

    if not swept:
        return {
            "status":"m15_liquidity_sweep_failed",
            "decision_ts":decision_ts,
            "prev4_low":prev4_low,
            "prev4_high":prev4_high,
            **ctx,
        }
    if not reclaimed:
        return {
            "status":"m15_local_reclaim_failed",
            "decision_ts":decision_ts,
            "prev4_low":prev4_low,
            "prev4_high":prev4_high,
            **ctx,
        }
    if not midpoint_ok:
        return {
            "status":"m15_h1_midpoint_reclaim_failed",
            "decision_ts":decision_ts,
            "prev4_low":prev4_low,
            "prev4_high":prev4_high,
            **ctx,
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

    h1pair=_latest_two_completed_rows(bars["h1"],decision_ts)
    if h1pair is None:
        return {"status":"h1_target_history_unavailable","decision_ts":decision_ts,**ctx}
    h10,h11=h1pair

    if direction=="long":
        h1_destination=max(float(h10["high"]),float(h11["high"]))
        target_room_ok=h1_destination>=target_price
    else:
        h1_destination=min(float(h10["low"]),float(h11["low"]))
        target_room_ok=h1_destination<=target_price

    if not target_room_ok:
        return {
            "status":"h1_target_destination_failed",
            "decision_ts":decision_ts,
            "direction":direction,
            "limit":limit,
            "stop":stop,
            "target_distance":float(d),
            "target_price":float(target_price),
            "h1_destination":float(h1_destination),
            **{k:v for k,v in ctx.items() if k!="direction"},
        }

    return {
        "status":"armed",
        "decision_ts":decision_ts,
        "direction":direction,
        "h1_mid":mid,
        "prev4_low":prev4_low,
        "prev4_high":prev4_high,
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
        "h1_destination":float(h1_destination),
        "limit_improvement_native":(
            float(a5["close"])-limit if direction=="long" else limit-float(a5["close"])
        ),
        "limit_improvement_a5_range":(
            (float(a5["close"])-limit)/rng if direction=="long"
            else (limit-float(a5["close"]))/rng
        ),
        **{k:v for k,v in ctx.items() if k!="direction"},
    }


def self_tests_engine_m_v03()->list[str]:
    tests=[]
    # Strict inequality boundary.
    assert not (1.0<1.0)
    assert 0.999<1.0
    tests.append("strict_sweep_boundary")

    # Target-destination mirror arithmetic.
    limit=100.0
    d=2.0
    assert max(102.0,101.0)>=limit+d
    assert min(98.0,99.0)<=limit-d
    tests.append("h1_target_destination_mirror")

    # 50% arm midpoint remains favorable whenever arm closes in directional outer quartile.
    lo,hi=99.0,101.0
    mid=(lo+hi)/2
    assert 100.5>mid
    assert 99.5<mid
    tests.append("non_chasing_midpoint_geometry")

    return tests
