#!/usr/bin/env python3
"""Engine Q v0.1 — cross-market volatility-spillover breakout mechanics."""

from __future__ import annotations

import math
import pandas as pd

from engine_k_v0_1 import MAX_NEXT_ENTRY_GAP_MINUTES
from engine_k_v0_2 import research_tick

PEER_SHOCK_VR=1.75
PEER_SHOCK_COUNT=4
MIN_VALID_PEERS=6
CANDIDATE_LAG_VR_MAX=1.00
BREAKOUT_VR_MIN=1.25
BREAKOUT_BODY_FRACTION=0.50
BREAKOUT_CLOSE_OUTER_FRACTION=0.25
BASELINE_M5_BARS=24
BOX_M5_BARS=6
ARM_M5_BARS=6
ORDER_ACTIVE_M1_BARS=10
ORDER_HARD_MINUTES=30
ENTRY_CUTOFF_HOUR=18


def even_median(values:list[float])->float:
    if len(values)==0 or len(values)%2!=0:
        raise ValueError("even_median requires non-empty even-length values")
    xs=sorted(float(x) for x in values)
    n=len(xs)
    return (xs[n//2-1]+xs[n//2])/2.0


def decision_allowed(ts:pd.Timestamp)->bool:
    minutes=ts.hour*60+ts.minute
    return (
        ts.weekday()<5
        and 6*60+5<=minutes<=17*60+25
        and ts.minute in tuple(range(0,60,5))
    )


def _state_at_index(b5:pd.DataFrame,k:int)->dict:
    if k<BASELINE_M5_BARS:
        return {"status":"baseline_24x5_unavailable"}
    cur=b5.iloc[k]
    prev=b5.iloc[k-BASELINE_M5_BARS:k]
    expected=[
        cur["datetime"]-pd.Timedelta(minutes=5*(BASELINE_M5_BARS-i))
        for i in range(BASELINE_M5_BARS)
    ]
    if list(prev["datetime"])!=expected:
        return {"status":"baseline_24x5_not_contiguous"}

    ranges=[]
    for r in prev.itertuples():
        rng=float(r.high-r.low)
        if not math.isfinite(rng) or rng<0:
            return {"status":"invalid_baseline_range"}
        ranges.append(rng)

    vol=even_median(ranges)
    if not math.isfinite(vol) or vol<=0:
        return {"status":"baseline_vol_zero"}

    op=float(cur["open"]); hi=float(cur["high"]); lo=float(cur["low"]); cl=float(cur["close"])
    rng=hi-lo
    if not all(math.isfinite(x) for x in (op,hi,lo,cl,rng)) or rng<0:
        return {"status":"invalid_price"}

    return {
        "status":"ok",
        "decision_ts":cur["available_ts"],
        "bar_start":cur["datetime"],
        "open":op,
        "high":hi,
        "low":lo,
        "close":cl,
        "range":float(rng),
        "baseline_median_range":float(vol),
        "vr":float(rng/vol),
    }


def metric_at_time(b5:pd.DataFrame,decision_ts:pd.Timestamp)->dict:
    """Causal per-symbol volatility state at one completed-M5 decision time."""
    k=int(b5["available_ts"].searchsorted(decision_ts,side="left"))
    if k>=len(b5) or b5.iloc[k]["available_ts"]!=decision_ts:
        return {"status":"m5_snapshot_unavailable","decision_ts":decision_ts}

    st=_state_at_index(b5,k)
    if st.get("status")!="ok":
        return {"status":st.get("status"),"decision_ts":decision_ts}

    if k<BOX_M5_BARS:
        return {"status":"box_6x5_unavailable","decision_ts":decision_ts}
    box=b5.iloc[k-BOX_M5_BARS:k]
    expected=[
        b5.iloc[k]["datetime"]-pd.Timedelta(minutes=5*(BOX_M5_BARS-i))
        for i in range(BOX_M5_BARS)
    ]
    if list(box["datetime"])!=expected:
        return {"status":"box_6x5_not_contiguous","decision_ts":decision_ts}

    out=dict(st)
    out["box_high"]=float(box["high"].max())
    out["box_low"]=float(box["low"].min())
    return out


def peer_breadth(snapshot:dict[str,dict],exclude_symbol:str)->dict:
    valid=[]
    shocked=[]
    for symbol,state in snapshot.items():
        if symbol==exclude_symbol:
            continue
        if not state or state.get("status")!="ok":
            continue
        vr=float(state["vr"])
        valid.append((symbol,vr))
        if vr+1e-12>=PEER_SHOCK_VR:
            shocked.append((symbol,vr))
    return {
        "valid_peer_count":len(valid),
        "shock_count":len(shocked),
        "valid_peers":valid,
        "shocked_peers":shocked,
    }


def arm_from_snapshot(symbol:str,snapshot:dict[str,dict])->dict:
    own=snapshot.get(symbol)
    if not own or own.get("status")!="ok":
        return {"status":"candidate_metric_unavailable"}

    decision_ts=own["decision_ts"]
    if not decision_allowed(decision_ts):
        return {"status":"outside_decision_grid","decision_ts":decision_ts}

    breadth=peer_breadth(snapshot,symbol)
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
    box_lo=float(own["box_low"]); box_hi=float(own["box_high"])
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
        "shocked_peers":[s for s,_ in breadth["shocked_peers"]],
        "shocked_peer_vrs":[float(v) for _,v in breadth["shocked_peers"]],
    }


def breakout_from_state(symbol:str,arm:dict,state:dict)->dict|None:
    if state.get("status")!="ok":
        return None
    op=float(state["open"]); hi=float(state["high"]); lo=float(state["low"]); cl=float(state["close"])
    rng=float(state["range"])
    if rng<=0:
        return None
    vr=float(state["vr"])
    if vr+1e-12<BREAKOUT_VR_MIN:
        return None
    body=abs(cl-op)
    if body+1e-12<BREAKOUT_BODY_FRACTION*rng:
        return None

    box_hi=float(arm["box_high"]); box_lo=float(arm["box_low"])
    direction=None
    if cl>box_hi and cl>op and hi-cl<=BREAKOUT_CLOSE_OUTER_FRACTION*rng+1e-12:
        direction="long"
    elif cl<box_lo and cl<op and cl-lo<=BREAKOUT_CLOSE_OUTER_FRACTION*rng+1e-12:
        direction="short"
    if direction is None:
        return None

    limit=(hi+lo)/2.0
    tick=research_tick(symbol)
    stop=lo-tick if direction=="long" else hi+tick
    if direction=="long" and not limit<cl:
        return None
    if direction=="short" and not limit>cl:
        return None

    return {
        "status":"triggered",
        "decision_ts":state["decision_ts"],
        "direction":direction,
        "trigger_start":state["bar_start"],
        "trigger_open":op,
        "trigger_high":hi,
        "trigger_low":lo,
        "trigger_close":cl,
        "trigger_range":rng,
        "trigger_vr":vr,
        "trigger_body_fraction":float(body/rng),
        "limit":float(limit),
        "stop":float(stop),
        "limit_improvement_native":float(cl-limit if direction=="long" else limit-cl),
        "limit_improvement_trigger_range":float((cl-limit)/rng if direction=="long" else (limit-cl)/rng),
        "arm_decision_ts":arm["decision_ts"],
        "candidate_vr_at_arm":float(arm["candidate_vr"]),
        "peer_shock_count_at_arm":int(arm["shock_count"]),
        "valid_peer_count_at_arm":int(arm["valid_peer_count"]),
        "shocked_peers_at_arm":list(arm["shocked_peers"]),
    }


def find_breakout_trigger(b5:pd.DataFrame,symbol:str,arm:dict)->dict:
    if arm.get("status")!="armed":
        raise ValueError("find_breakout_trigger requires armed state")

    decision_ts=arm["decision_ts"]
    k=int(b5["available_ts"].searchsorted(decision_ts,side="left"))
    if k>=len(b5) or b5.iloc[k]["available_ts"]!=decision_ts:
        return {"status":"arm_origin_unavailable","resolved_ts":decision_ts,"triggered":False}

    last_ts=decision_ts
    for step in range(1,ARM_M5_BARS+1):
        pos=k+step
        if pos>=len(b5):
            break
        st=_state_at_index(b5,pos)
        if st.get("status")!="ok":
            continue
        ts=st["decision_ts"]
        last_ts=ts
        if ts>=decision_ts.normalize()+pd.Timedelta(hours=ENTRY_CUTOFF_HOUR):
            return {"status":"arm_expired_cutoff","resolved_ts":ts,"triggered":False}
        trig=breakout_from_state(symbol,arm,st)
        if trig is not None:
            trig["resolved_ts"]=ts
            trig["triggered"]=True
            trig["arm_wait_m5_bars"]=step
            return trig

    return {
        "status":"arm_expired_no_breakout",
        "resolved_ts":min(
            decision_ts+pd.Timedelta(minutes=5*ARM_M5_BARS),
            decision_ts.normalize()+pd.Timedelta(hours=ENTRY_CUTOFF_HOUR),
        ),
        "triggered":False,
        "last_checked_ts":last_ts,
    }


def find_limit_fill(df1:pd.DataFrame,setup:dict)->dict:
    if setup.get("status")!="triggered":
        raise ValueError("find_limit_fill requires triggered setup")

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
        return {"status":"no_m1_after_trigger","resolved_ts":decision_ts,"filled":False}

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


def self_tests_engine_q_v01()->list[str]:
    tests=[]

    assert even_median([1,2,3,4])==2.5
    assert even_median(list(range(1,25)))==12.5
    tests.append("even_median_exact")

    assert decision_allowed(pd.Timestamp("2026-04-06T06:05:00Z"))
    assert decision_allowed(pd.Timestamp("2026-04-06T17:25:00Z"))
    assert not decision_allowed(pd.Timestamp("2026-04-06T17:30:00Z"))
    tests.append("arm_decision_grid")

    dt=pd.Timestamp("2026-04-06T10:05:00Z")
    snap={}
    for i,s in enumerate(["XAUUSD","EURUSD","GBPUSD","USDJPY","EURJPY","AUDUSD","USDCAD","USDCHF"]):
        snap[s]={
            "status":"ok","decision_ts":dt,"vr":0.8,
            "close":100.0,"box_low":99.0,"box_high":101.0,
        }
    for s in ["EURUSD","GBPUSD","USDJPY","AUDUSD"]:
        snap[s]["vr"]=1.75
    snap["XAUUSD"]["vr"]=9.0
    breadth=peer_breadth(snap,"XAUUSD")
    assert breadth["shock_count"]==4
    tests.append("candidate_self_excluded_from_peer_breadth")

    snap["XAUUSD"]["vr"]=0.8
    arm=arm_from_snapshot("XAUUSD",snap)
    assert arm["status"]=="armed" and arm["shock_count"]==4
    tests.append("peer_breadth_and_candidate_lag_arm")

    snap2={k:dict(v) for k,v in snap.items()}
    snap2["XAUUSD"]["vr"]=1.01
    assert arm_from_snapshot("XAUUSD",snap2)["status"]=="candidate_not_lagging"
    tests.append("candidate_lag_boundary")

    state={
        "status":"ok","decision_ts":dt+pd.Timedelta(minutes=5),
        "bar_start":dt,"open":100.2,"high":102.0,"low":100.0,"close":101.8,
        "range":2.0,"vr":1.25,
    }
    trig=breakout_from_state("XAUUSD",arm,state)
    assert trig is not None and trig["direction"]=="long"
    tests.append("long_breakout_boundary")

    state2={
        "status":"ok","decision_ts":dt+pd.Timedelta(minutes=5),
        "bar_start":dt,"open":99.8,"high":100.0,"low":98.0,"close":98.2,
        "range":2.0,"vr":1.25,
    }
    trig2=breakout_from_state("XAUUSD",arm,state2)
    assert trig2 is not None and trig2["direction"]=="short"
    tests.append("short_breakout_boundary")

    return tests
