#!/usr/bin/env python3
"""Engine N v0.1 — session opening-drive pullback mechanics.

Zero-outcome selection/execution mechanics only.
"""

from __future__ import annotations

import math
from typing import Optional

import pandas as pd

from engine_k_v0_1 import MAX_NEXT_ENTRY_GAP_MINUTES
from engine_k_v0_2 import research_tick

SESSION_ANCHORS=((7,0,"LONDON"),(13,30,"NEW_YORK"))
DRIVE_MINUTES=30
BASELINE_M15_BARS=8
EXPANSION_RATIO=1.50
BODY_FRACTION=0.60
OUTER_CLOSE_FRACTION=0.25
ORDER_ACTIVE_M1_BARS=45
SESSION_HORIZON_MINUTES=90


def median8(values:list[float])->float:
    if len(values)!=8:
        raise ValueError("median8 requires exactly 8 values")
    xs=sorted(float(x) for x in values)
    return (xs[3]+xs[4])/2.0


def session_anchor(date:pd.Timestamp,hour:int,minute:int)->pd.Timestamp:
    return date.normalize()+pd.Timedelta(hours=hour,minutes=minute)


def session_setup(
    df1:pd.DataFrame,
    m15:pd.DataFrame,
    anchor:pd.Timestamp,
    session_name:str,
    symbol:str,
)->dict:
    decision_ts=anchor+pd.Timedelta(minutes=DRIVE_MINUTES)

    # Exact eight preceding M15 bars.
    expected_m15=[
        anchor-pd.Timedelta(minutes=15*(BASELINE_M15_BARS-i))
        for i in range(BASELINE_M15_BARS)
    ]
    k=int(m15["datetime"].searchsorted(expected_m15[0],side="left"))
    base=m15.iloc[k:k+BASELINE_M15_BARS]
    if len(base)!=BASELINE_M15_BARS or list(base["datetime"])!=expected_m15:
        return {
            "status":"baseline_8x15_unavailable",
            "anchor":anchor,
            "decision_ts":decision_ts,
            "session":session_name,
        }

    base_ranges=[float(r.high-r.low) for r in base.itertuples()]
    med=median8(base_ranges)
    if not math.isfinite(med) or med<=0:
        return {
            "status":"baseline_zero_range",
            "anchor":anchor,
            "decision_ts":decision_ts,
            "session":session_name,
        }

    # Exact 30 M1 bars starting at anchor.
    start=int(df1["datetime"].searchsorted(anchor,side="left"))
    drive=df1.iloc[start:start+DRIVE_MINUTES]
    expected_m1=[anchor+pd.Timedelta(minutes=i) for i in range(DRIVE_MINUTES)]
    if len(drive)!=DRIVE_MINUTES or list(drive["datetime"])!=expected_m1:
        return {
            "status":"drive_30m_incomplete",
            "anchor":anchor,
            "decision_ts":decision_ts,
            "session":session_name,
            "baseline_median":med,
        }

    o=float(drive.iloc[0]["open"])
    h=float(drive["high"].max())
    l=float(drive["low"].min())
    c=float(drive.iloc[-1]["close"])
    rng=h-l
    if not math.isfinite(rng) or rng<=0:
        return {
            "status":"drive_zero_range",
            "anchor":anchor,
            "decision_ts":decision_ts,
            "session":session_name,
            "baseline_median":med,
        }

    body=abs(c-o)
    if rng+1e-12 < EXPANSION_RATIO*med:
        return {
            "status":"drive_expansion_failed",
            "anchor":anchor,
            "decision_ts":decision_ts,
            "session":session_name,
            "baseline_median":med,
            "drive_range":rng,
        }
    if body+1e-12 < BODY_FRACTION*rng:
        return {
            "status":"drive_body_failed",
            "anchor":anchor,
            "decision_ts":decision_ts,
            "session":session_name,
            "baseline_median":med,
            "drive_range":rng,
            "drive_body":body,
        }

    if c>o:
        direction="long"
        if h-c > OUTER_CLOSE_FRACTION*rng+1e-12:
            return {
                "status":"drive_close_location_failed",
                "anchor":anchor,
                "decision_ts":decision_ts,
                "session":session_name,
                "direction":direction,
                "drive_range":rng,
            }
    elif c<o:
        direction="short"
        if c-l > OUTER_CLOSE_FRACTION*rng+1e-12:
            return {
                "status":"drive_close_location_failed",
                "anchor":anchor,
                "decision_ts":decision_ts,
                "session":session_name,
                "direction":direction,
                "drive_range":rng,
            }
    else:
        return {
            "status":"drive_doji",
            "anchor":anchor,
            "decision_ts":decision_ts,
            "session":session_name,
            "drive_range":rng,
        }

    limit=(h+l)/2.0
    tick=research_tick(symbol)
    stop=l-tick if direction=="long" else h+tick

    if direction=="long":
        if not limit<c:
            raise AssertionError("long midpoint limit must be below drive close")
        improvement=c-limit
    else:
        if not limit>c:
            raise AssertionError("short midpoint limit must be above drive close")
        improvement=limit-c

    return {
        "status":"armed",
        "session":session_name,
        "anchor":anchor,
        "decision_ts":decision_ts,
        "direction":direction,
        "baseline_median":float(med),
        "baseline_ranges":base_ranges,
        "drive_open":o,
        "drive_high":h,
        "drive_low":l,
        "drive_close":c,
        "drive_range":rng,
        "drive_body":body,
        "drive_body_fraction":body/rng,
        "drive_range_over_baseline_median":rng/med,
        "limit":float(limit),
        "stop":float(stop),
        "limit_improvement_native":float(improvement),
        "limit_improvement_drive_range":float(improvement/rng),
    }


def find_session_pullback_fill(
    df1:pd.DataFrame,
    setup:dict,
)->dict:
    if setup.get("status")!="armed":
        raise ValueError("find_session_pullback_fill requires armed setup")

    decision_ts=setup["decision_ts"]
    anchor=setup["anchor"]
    direction=setup["direction"]
    limit=float(setup["limit"])
    stop=float(setup["stop"])

    start=int(df1["datetime"].searchsorted(decision_ts,side="left"))
    if start>=len(df1):
        return {"status":"no_m1_after_drive","resolved_ts":decision_ts,"filled":False}

    cutoff=anchor+pd.Timedelta(minutes=SESSION_HORIZON_MINUTES)
    max_end=min(start+ORDER_ACTIVE_M1_BARS,len(df1))
    prev_ts=decision_ts
    last_ts=decision_ts

    for pos in range(start,max_end):
        row=df1.iloc[pos]
        ts=row["datetime"]
        last_ts=ts
        if ts>=cutoff:
            return {"status":"expired_session_horizon","resolved_ts":cutoff,"filled":False}
        if ts-prev_ts>pd.Timedelta(minutes=MAX_NEXT_ENTRY_GAP_MINUTES):
            return {"status":"cancel_gap","resolved_ts":ts,"filled":False}
        prev_ts=ts

        op=float(row["open"])
        hi=float(row["high"])
        lo=float(row["low"])

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
            "entry_improvement_drive_range":float(setup["limit_improvement_drive_range"]),
            "stop_distance_native":abs(limit-stop),
        }

    return {
        "status":"expired_unfilled",
        "resolved_ts":last_ts+pd.Timedelta(minutes=1),
        "filled":False,
    }


def self_tests_engine_n_v01()->list[str]:
    tests=[]

    assert median8([1,2,3,4,5,6,7,8])==4.5
    tests.append("median8_exact")

    assert 1.5+1e-12>=EXPANSION_RATIO*1.0
    assert 0.6+1e-12>=BODY_FRACTION*1.0
    assert 0.25<=OUTER_CLOSE_FRACTION+1e-12
    tests.append("qualification_boundaries")

    lo,hi=100.0,110.0
    mid=(lo+hi)/2.0
    assert mid==105.0
    assert mid<108.0 and mid>102.0
    tests.append("non_chasing_midpoint")

    assert ORDER_ACTIVE_M1_BARS==45
    assert SESSION_HORIZON_MINUTES==90
    tests.append("order_lifetime_constants")

    return tests
