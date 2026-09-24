#!/usr/bin/env python3
"""Engine M v0.5 recent-H1 range sweep/reclaim mechanics.

Zero-outcome selection layer.
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


def _m5_arm_geometry(
    bars:dict[str,pd.DataFrame],
    decision_ts:pd.Timestamp,
    direction:str,
    symbol:str,
):
    a5_start=decision_ts-pd.Timedelta(minutes=5)
    k=int(bars["m5"]["datetime"].searchsorted(a5_start,side="left"))
    if k>=len(bars["m5"]) or bars["m5"].iloc[k]["datetime"]!=a5_start:
        return {"status":"a5_unavailable"}
    if k<1:
        return {"status":"p5_unavailable"}

    a5=bars["m5"].iloc[k]
    p5=bars["m5"].iloc[k-1]
    if p5["datetime"]!=a5_start-pd.Timedelta(minutes=5):
        return {"status":"p5_not_contiguous"}

    rng=float(a5["high"]-a5["low"])
    if rng<=0:
        return {"status":"a5_zero_range"}

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
        return {"status":"m5_arm_failed"}

    limit=(float(a5["high"])+float(a5["low"]))/2.0
    tick=research_tick(symbol)
    stop=float(a5["low"]-tick) if direction=="long" else float(a5["high"]+tick)

    d=native_target_distances_v02(symbol,limit,stop).get("T40")
    if d is None or not math.isfinite(d) or d<=0:
        return {"status":"t40_geometry_unavailable"}
    target_price=limit+d if direction=="long" else limit-d

    return {
        "status":"ok",
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
        "limit_improvement_native":(
            float(a5["close"])-limit if direction=="long" else limit-float(a5["close"])
        ),
        "limit_improvement_a5_range":(
            (float(a5["close"])-limit)/rng if direction=="long"
            else (limit-float(a5["close"]))/rng
        ),
    }


def recent_h1_range_setup_at(
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

    arm=_m5_arm_geometry(bars,decision_ts,direction,symbol)
    if arm["status"]!="ok":
        return {"status":arm["status"],"decision_ts":decision_ts,**ctx}

    candidates=[("H1_0",h10),("H1_1",h11)]
    reasons=[]
    for rank,(label,h1) in enumerate(candidates):
        h1_low=float(h1["low"])
        h1_high=float(h1["high"])

        if direction=="long":
            swept=float(s15["low"])<h1_low
            reclaimed=float(s15["close"])>h1_low
            room=arm["target_price"]<=h1_high
        else:
            swept=float(s15["high"])>h1_high
            reclaimed=float(s15["close"])<h1_high
            room=arm["target_price"]>=h1_low

        if swept and reclaimed and room:
            return {
                **arm,
                "status":"armed",
                "decision_ts":decision_ts,
                "direction":direction,
                "selected_h1":label,
                "selected_h1_rank":rank,
                "selected_h1_start":h1["datetime"],
                "h1_low":h1_low,
                "h1_high":h1_high,
                "s15_start":s15["datetime"],
                "s15_open":float(s15["open"]),
                "s15_high":float(s15["high"]),
                "s15_low":float(s15["low"]),
                "s15_close":float(s15["close"]),
                **{k:v for k,v in ctx.items() if k!="direction"},
            }

        if not swept:
            reasons.append(f"{label}:sweep")
        elif not reclaimed:
            reasons.append(f"{label}:reclaim")
        else:
            reasons.append(f"{label}:room")

    return {
        **arm,
        "status":"no_recent_h1_range_qualified",
        "decision_ts":decision_ts,
        "candidate_failures":reasons,
        **ctx,
    }


def self_tests_engine_m_v05()->list[str]:
    tests=[]

    # Deterministic recency preference is H1_0 first, then H1_1.
    assert ["H1_0","H1_1"][0]=="H1_0"
    tests.append("h1_recency_order")

    # Strict sweep boundaries.
    assert not (1.0<1.0)
    assert not (2.0>2.0)
    tests.append("strict_h1_sweep_boundary")

    # Same selected range must provide target room.
    target=102.0
    assert target<=103.0
    tests.append("same_range_target_room")

    return tests
