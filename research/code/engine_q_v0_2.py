#!/usr/bin/env python3
"""Engine Q v0.2 — rolling cross-market volatility-spillover mechanics."""

from __future__ import annotations

import pandas as pd

from engine_q_v0_1 import (
    PEER_SHOCK_VR,
    PEER_SHOCK_COUNT,
    MIN_VALID_PEERS,
    CANDIDATE_LAG_VR_MAX,
    metric_at_time,
    decision_allowed,
    find_breakout_trigger,
    find_limit_fill,
    breakout_from_state,
    even_median,
)

ROLLING_SHOCK_OFFSETS_MIN=(0,5,10)


def rolling_peer_breadth(history_snapshots:list[dict[str,dict]],exclude_symbol:str)->dict:
    """Count unique peers shocked at t/t-5/t-10; each peer counts once."""
    if len(history_snapshots)!=3:
        raise ValueError("rolling_peer_breadth requires exactly three snapshots")

    all_symbols=set()
    for snap in history_snapshots:
        all_symbols.update(snap.keys())

    valid_peers=[]
    shocked=[]
    for symbol in sorted(all_symbols):
        if symbol==exclude_symbol:
            continue

        states=[snap.get(symbol) for snap in history_snapshots]
        if any((not st) or st.get("status")!="ok" for st in states):
            continue

        valid_peers.append(symbol)
        shock_age=None
        shock_vr=None
        for age,st in zip(ROLLING_SHOCK_OFFSETS_MIN,states):
            vr=float(st["vr"])
            if vr+1e-12>=PEER_SHOCK_VR:
                shock_age=age
                shock_vr=vr
                break

        if shock_age is not None:
            shocked.append({
                "symbol":symbol,
                "shock_age_minutes":int(shock_age),
                "shock_vr":float(shock_vr),
            })

    return {
        "valid_peer_count":len(valid_peers),
        "shock_count":len(shocked),
        "valid_peers":valid_peers,
        "shocked_peers":shocked,
    }


def arm_from_history(symbol:str,history_snapshots:list[dict[str,dict]])->dict:
    """Arm candidate using current candidate state + rolling peer shock memory."""
    if len(history_snapshots)!=3:
        raise ValueError("arm_from_history requires [t,t-5,t-10] snapshots")

    current=history_snapshots[0]
    own=current.get(symbol)
    if not own or own.get("status")!="ok":
        return {"status":"candidate_metric_unavailable"}

    decision_ts=own["decision_ts"]
    if not decision_allowed(decision_ts):
        return {"status":"outside_decision_grid","decision_ts":decision_ts}

    breadth=rolling_peer_breadth(history_snapshots,symbol)
    if breadth["valid_peer_count"]<MIN_VALID_PEERS:
        return {
            "status":"peer_breadth_unavailable",
            "decision_ts":decision_ts,
            **breadth,
        }
    if breadth["shock_count"]<PEER_SHOCK_COUNT:
        return {
            "status":"peer_shock_failed",
            "decision_ts":decision_ts,
            **breadth,
        }

    vr=float(own["vr"])
    if vr>CANDIDATE_LAG_VR_MAX+1e-12:
        return {
            "status":"candidate_not_lagging",
            "decision_ts":decision_ts,
            "candidate_vr":vr,
            **breadth,
        }

    cl=float(own["close"])
    box_lo=float(own["box_low"])
    box_hi=float(own["box_high"])
    if not box_lo<cl<box_hi:
        return {
            "status":"candidate_outside_box",
            "decision_ts":decision_ts,
            "candidate_vr":vr,
            "box_low":box_lo,
            "box_high":box_hi,
            **breadth,
        }

    return {
        "status":"armed",
        "decision_ts":decision_ts,
        "candidate_vr":vr,
        "box_low":box_lo,
        "box_high":box_hi,
        "valid_peer_count":breadth["valid_peer_count"],
        "shock_count":breadth["shock_count"],
        "shocked_peers":[x["symbol"] for x in breadth["shocked_peers"]],
        "shock_ages_minutes":{
            x["symbol"]:x["shock_age_minutes"] for x in breadth["shocked_peers"]
        },
        "shocked_peer_vrs":{
            x["symbol"]:x["shock_vr"] for x in breadth["shocked_peers"]
        },
    }


def self_tests_engine_q_v02()->list[str]:
    tests=[]
    dt=pd.Timestamp("2026-04-06T10:05:00Z")
    symbols=["XAUUSD","EURUSD","GBPUSD","USDJPY","EURJPY","AUDUSD","USDCAD","USDCHF"]

    def base(vr=0.8):
        return {
            "status":"ok",
            "decision_ts":dt,
            "vr":vr,
            "close":100.0,
            "box_low":99.0,
            "box_high":101.0,
        }

    current={s:base() for s in symbols}
    prev5={s:base() for s in symbols}
    prev10={s:base() for s in symbols}

    current["EURUSD"]["vr"]=1.75
    prev5["GBPUSD"]["vr"]=1.80
    prev10["USDJPY"]["vr"]=1.90
    prev5["AUDUSD"]["vr"]=2.00

    breadth=rolling_peer_breadth([current,prev5,prev10],"XAUUSD")
    assert breadth["valid_peer_count"]==7
    assert breadth["shock_count"]==4
    ages={x["symbol"]:x["shock_age_minutes"] for x in breadth["shocked_peers"]}
    assert ages["EURUSD"]==0
    assert ages["GBPUSD"]==5
    assert ages["USDJPY"]==10
    assert ages["AUDUSD"]==5
    tests.append("rolling_three_bar_unique_peer_memory")

    current["XAUUSD"]["vr"]=10.0
    breadth2=rolling_peer_breadth([current,prev5,prev10],"XAUUSD")
    assert breadth2["shock_count"]==4
    tests.append("candidate_self_excluded")

    # Same peer shocked multiple times still counts once, using most recent age.
    current["EURUSD"]["vr"]=2.0
    prev5["EURUSD"]["vr"]=2.2
    prev10["EURUSD"]["vr"]=2.4
    breadth3=rolling_peer_breadth([current,prev5,prev10],"XAUUSD")
    eur=[x for x in breadth3["shocked_peers"] if x["symbol"]=="EURUSD"][0]
    assert eur["shock_age_minutes"]==0
    assert breadth3["shock_count"]==4
    tests.append("peer_counts_once_most_recent_shock")

    current["XAUUSD"]["vr"]=0.8
    arm=arm_from_history("XAUUSD",[current,prev5,prev10])
    assert arm["status"]=="armed" and arm["shock_count"]==4
    tests.append("rolling_breadth_arms_lagging_candidate")

    bad_prev10={k:dict(v) for k,v in prev10.items()}
    bad_prev10["USDCHF"]={"status":"m5_snapshot_unavailable"}
    # Still six complete peers besides XAUUSD, so breadth remains available.
    a2=arm_from_history("XAUUSD",[current,prev5,bad_prev10])
    assert a2["status"] in ("armed","peer_shock_failed")
    tests.append("minimum_six_complete_peer_histories")

    return tests
