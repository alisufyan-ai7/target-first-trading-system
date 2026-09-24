#!/usr/bin/env python3
"""Engine L v0.1 causal entry mechanics.

This module contains no future target labeling.
It converts a completed 5m forecast arm into a causal M1 pullback/resumption entry.
"""

from __future__ import annotations

import math
from typing import Optional

import pandas as pd

from engine_k_v0_1 import MAX_NEXT_ENTRY_GAP_MINUTES
from engine_k_v0_2 import candidate_economics_v02, research_tick

ARM_ACTIVE_M1_BARS=15
PULLBACK_V5_FRACTION=0.20
SESSION_CUTOFF_HOUR=20


def session_cutoff(ts:pd.Timestamp)->pd.Timestamp:
    return ts.normalize()+pd.Timedelta(hours=SESSION_CUTOFF_HOUR)


def _outer_quartile_resume(prev:pd.Series, cur:pd.Series, direction:str)->bool:
    rng=float(cur["high"]-cur["low"])
    if rng<=0:
        return False
    if direction=="long":
        return bool(
            float(cur["close"])>float(prev["high"])
            and float(cur["close"])>float(cur["open"])
            and 4.0*(float(cur["high"])-float(cur["close"]))<=rng+1e-12
        )
    if direction=="short":
        return bool(
            float(cur["close"])<float(prev["low"])
            and float(cur["close"])<float(cur["open"])
            and 4.0*(float(cur["close"])-float(cur["low"]))<=rng+1e-12
        )
    raise ValueError(direction)


def find_micro_entry(
    df1:pd.DataFrame,
    decision_end:pd.Timestamp,
    decision_close:float,
    v5:float,
    direction:str,
    old_invalidation:float,
    symbol:str,
    usd_jpy:Optional[float]=None,
    usd_jpy_series:Optional[pd.Series]=None,
)->dict:
    """Find the first causal Engine-L entry after an armed 5m decision.

    No future target outcome is inspected.
    """
    if direction not in ("long","short"):
        raise ValueError(direction)
    if not math.isfinite(v5) or v5<=0:
        return {"status":"invalid_v5"}

    times=df1["datetime"]
    start=int(times.searchsorted(decision_end,side="left"))
    if start>=len(df1):
        return {"status":"no_m1_after_decision"}

    cutoff=session_cutoff(decision_end)
    tick=research_tick(symbol)
    pullback_threshold=decision_close-PULLBACK_V5_FRACTION*v5 if direction=="long" else decision_close+PULLBACK_V5_FRACTION*v5

    pulled=False
    pullback_bar_index=None
    seen_low=math.inf
    seen_high=-math.inf
    prev_ts=None

    # 15 active M1 bars. Entry must itself occur inside this lifetime, so the
    # resumption bar must leave room for one next-active-open fill.
    max_scan=min(start+ARM_ACTIVE_M1_BARS,len(df1))
    for pos in range(start,max_scan):
        row=df1.iloc[pos]
        ts=row["datetime"]
        if ts>=cutoff:
            return {"status":"expired_session"}
        if prev_ts is not None and ts-prev_ts>pd.Timedelta(minutes=MAX_NEXT_ENTRY_GAP_MINUTES):
            return {"status":"cancel_gap"}
        prev_ts=ts

        low=float(row["low"]); high=float(row["high"])
        seen_low=min(seen_low,low)
        seen_high=max(seen_high,high)

        # Old 5m structure is only an arm invalidation boundary.
        if direction=="long" and low<=old_invalidation:
            return {"status":"cancel_old_invalidation"}
        if direction=="short" and high>=old_invalidation:
            return {"status":"cancel_old_invalidation"}

        if not pulled:
            if direction=="long" and low<=pullback_threshold:
                pulled=True; pullback_bar_index=pos
            elif direction=="short" and high>=pullback_threshold:
                pulled=True; pullback_bar_index=pos

        if not pulled or pos<=start:
            continue

        prev=df1.iloc[pos-1]
        if not _outer_quartile_resume(prev,row,direction):
            continue

        entry_pos=pos+1
        if entry_pos>=max_scan or entry_pos>=len(df1):
            return {"status":"expired_before_next_open"}
        entry_row=df1.iloc[entry_pos]
        entry_ts=entry_row["datetime"]
        if entry_ts>=cutoff:
            return {"status":"expired_session"}
        expected=ts+pd.Timedelta(minutes=1)
        if entry_ts-expected>pd.Timedelta(minutes=MAX_NEXT_ENTRY_GAP_MINUTES):
            return {"status":"cancel_entry_gap"}

        entry=float(entry_row["open"])
        stop=(seen_low-tick) if direction=="long" else (seen_high+tick)
        if direction=="long" and not stop<entry:
            return {"status":"invalid_fresh_stop_geometry"}
        if direction=="short" and not stop>entry:
            return {"status":"invalid_fresh_stop_geometry"}

        entry_usd_jpy=usd_jpy
        if symbol=="EURJPY" and usd_jpy_series is not None:
            k=int(usd_jpy_series.index.searchsorted(entry_ts,side="right"))-1
            if k>=0:
                entry_usd_jpy=float(usd_jpy_series.iloc[k])
        econ=candidate_economics_v02(symbol,entry,stop,entry_usd_jpy)
        t40=econ.get("T40")
        if not t40:
            return {"status":"no_t40_economics"}
        if not t40.get("execution_admissible_pre_probability",False):
            return {
                "status":"triggered_but_economically_rejected",
                "entry_ts":entry_ts,
                "entry":entry,
                "stop":stop,
                "pullback_bar_index":pullback_bar_index-start if pullback_bar_index is not None else None,
                "resumption_bar_index":pos-start,
                "wait_active_m1_bars":entry_pos-start+1,
                "t40":t40,
            }

        pullback_depth=(decision_close-seen_low) if direction=="long" else (seen_high-decision_close)
        entry_vs_decision=(entry-decision_close) if direction=="long" else (decision_close-entry)
        return {
            "status":"admissible_entry",
            "entry_ts":entry_ts,
            "entry":entry,
            "stop":stop,
            "pullback_bar_index":pullback_bar_index-start if pullback_bar_index is not None else None,
            "resumption_bar_index":pos-start,
            "wait_active_m1_bars":entry_pos-start+1,
            "pullback_depth_native":pullback_depth,
            "pullback_depth_v5":pullback_depth/v5,
            "entry_directional_displacement_from_decision":entry_vs_decision,
            "entry_directional_displacement_v5":entry_vs_decision/v5,
            "fresh_stop_distance_native":abs(entry-stop),
            "t40":t40,
        }

    return {"status":"expired_no_entry" if pulled else "expired_no_pullback"}


def self_tests_engine_l()->list[str]:
    tests=[]

    # Long resumption.
    prev=pd.Series({"high":100.0,"low":99.0,"open":99.5,"close":99.6})
    cur=pd.Series({"high":101.0,"low":99.5,"open":99.7,"close":100.8})
    assert _outer_quartile_resume(prev,cur,"long")
    tests.append("long_resumption")

    # Short mirror.
    prev=pd.Series({"high":101.0,"low":100.0,"open":100.5,"close":100.4})
    cur=pd.Series({"high":100.5,"low":99.0,"open":100.3,"close":99.2})
    assert _outer_quartile_resume(prev,cur,"short")
    tests.append("short_resumption")

    # Not outer-quartile close.
    bad=pd.Series({"high":101.0,"low":99.0,"open":99.5,"close":100.2})
    assert not _outer_quartile_resume(prev,bad,"long")
    tests.append("weak_close_rejected")

    assert ARM_ACTIVE_M1_BARS==15
    assert abs(PULLBACK_V5_FRACTION-0.20)<1e-12
    tests.append("frozen_constants")

    return tests
