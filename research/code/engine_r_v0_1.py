#!/usr/bin/env python3
"""Engine R v0.1 — dynamic peer-residual reversion mechanics."""

from __future__ import annotations

import math
import pandas as pd

from engine_k_v0_1 import MAX_NEXT_ENTRY_GAP_MINUTES
from engine_k_v0_2 import research_tick

CORR_RETURNS=48
SCALE_MOVES=48
MIN_HISTORY_BARS=51
CORR_THRESHOLD=0.60
PEER_NM15_THRESHOLD=1.00
RESIDUAL_THRESHOLD=1.50
BODY_FRACTION=0.35
CLOSE_OUTER_FRACTION=0.40
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
    mins=ts.hour*60+ts.minute
    return (
        ts.weekday()<5
        and 6*60+5<=mins<=17*60+55
        and ts.minute in tuple(range(0,60,5))
    )


def pearson(a:list[float],b:list[float])->float|None:
    if len(a)!=len(b) or len(a)<2:
        return None
    ma=sum(a)/len(a)
    mb=sum(b)/len(b)
    da=[float(x)-ma for x in a]
    db=[float(x)-mb for x in b]
    va=sum(x*x for x in da)
    vb=sum(x*x for x in db)
    if va<=0 or vb<=0:
        return None
    cov=sum(x*y for x,y in zip(da,db))
    r=cov/math.sqrt(va*vb)
    if not math.isfinite(r):
        return None
    return max(-1.0,min(1.0,float(r)))


def metric_at_time(b5:pd.DataFrame,decision_ts:pd.Timestamp)->dict:
    """Causal state with current normalized 15m move and prior return history."""
    k=int(b5["available_ts"].searchsorted(decision_ts,side="left"))
    if k>=len(b5) or b5.iloc[k]["available_ts"]!=decision_ts:
        return {"status":"m5_snapshot_unavailable","decision_ts":decision_ts}
    if k<MIN_HISTORY_BARS:
        return {"status":"history_unavailable","decision_ts":decision_ts}

    seg=b5.iloc[k-MIN_HISTORY_BARS:k+1]
    cur=b5.iloc[k]
    expected=[
        cur["datetime"]-pd.Timedelta(minutes=5*(MIN_HISTORY_BARS-i))
        for i in range(MIN_HISTORY_BARS+1)
    ]
    if list(seg["datetime"])!=expected:
        return {"status":"history_not_contiguous","decision_ts":decision_ts}

    closes=[float(x) for x in seg["close"]]
    if any((not math.isfinite(x)) or x<=0 for x in closes):
        return {"status":"invalid_close","decision_ts":decision_ts}

    # Local indices 3..50 correspond to global k-48..k-1.
    ret_hist=[]
    move15_hist=[]
    for j in range(3,51):
        r=closes[j]/closes[j-1]-1.0
        m=closes[j]/closes[j-3]-1.0
        if not math.isfinite(r) or not math.isfinite(m):
            return {"status":"invalid_history_return","decision_ts":decision_ts}
        ret_hist.append(float(r))
        move15_hist.append(float(m))

    if len(ret_hist)!=CORR_RETURNS or len(move15_hist)!=SCALE_MOVES:
        raise AssertionError("frozen history length mismatch")

    scale15=even_median([abs(x) for x in move15_hist])
    if not math.isfinite(scale15) or scale15<=0:
        return {"status":"scale15_zero","decision_ts":decision_ts}

    move15_now=closes[51]/closes[48]-1.0
    nm15=move15_now/scale15

    op=float(cur["open"]); hi=float(cur["high"]); lo=float(cur["low"]); cl=float(cur["close"])
    rng=hi-lo
    if not all(math.isfinite(x) for x in (op,hi,lo,cl,rng)) or rng<=0:
        return {"status":"current_bar_invalid","decision_ts":decision_ts}

    return {
        "status":"ok",
        "decision_ts":decision_ts,
        "trigger_start":cur["datetime"],
        "open":op,
        "high":hi,
        "low":lo,
        "close":cl,
        "range":float(rng),
        "ret_history":ret_hist,
        "scale15":float(scale15),
        "move15_now":float(move15_now),
        "nm15":float(nm15),
    }


def strongest_peer(symbol:str,snapshot:dict[str,dict])->dict:
    own=snapshot.get(symbol)
    if not own or own.get("status")!="ok":
        return {"status":"candidate_metric_unavailable"}

    best_symbol=None
    best_rho=None

    for peer in sorted(snapshot):
        if peer==symbol:
            continue
        st=snapshot.get(peer)
        if not st or st.get("status")!="ok":
            continue
        rho=pearson(own["ret_history"],st["ret_history"])
        if rho is None:
            continue
        if (
            best_rho is None
            or abs(rho)>abs(best_rho)+1e-12
            or (
                abs(abs(rho)-abs(best_rho))<=1e-12
                and peer<best_symbol
            )
        ):
            best_symbol=peer
            best_rho=float(rho)

    if best_symbol is None:
        return {"status":"peer_unavailable"}

    return {
        "status":"ok",
        "peer":best_symbol,
        "rho":float(best_rho),
        "abs_rho":abs(float(best_rho)),
    }


def setup_from_snapshot(symbol:str,snapshot:dict[str,dict])->dict:
    own=snapshot.get(symbol)
    if not own or own.get("status")!="ok":
        return {"status":"candidate_metric_unavailable"}

    decision_ts=own["decision_ts"]
    if not decision_allowed(decision_ts):
        return {"status":"outside_decision_grid","decision_ts":decision_ts}

    sp=strongest_peer(symbol,snapshot)
    if sp.get("status")!="ok":
        return {"status":sp.get("status","peer_unavailable"),"decision_ts":decision_ts}

    peer_symbol=sp["peer"]
    rho=float(sp["rho"])
    if abs(rho)+1e-12<CORR_THRESHOLD:
        return {
            "status":"correlation_failed",
            "decision_ts":decision_ts,
            "peer":peer_symbol,
            "rho":rho,
        }

    peer=snapshot[peer_symbol]
    peer_nm=float(peer["nm15"])
    own_nm=float(own["nm15"])
    if abs(peer_nm)+1e-12<PEER_NM15_THRESHOLD:
        return {
            "status":"peer_move_failed",
            "decision_ts":decision_ts,
            "peer":peer_symbol,
            "rho":rho,
            "candidate_nm15":own_nm,
            "peer_nm15":peer_nm,
        }

    expected=(1.0 if rho>=0 else -1.0)*peer_nm
    residual=own_nm-expected
    if abs(residual)+1e-12<RESIDUAL_THRESHOLD:
        return {
            "status":"residual_failed",
            "decision_ts":decision_ts,
            "peer":peer_symbol,
            "rho":rho,
            "candidate_nm15":own_nm,
            "peer_nm15":peer_nm,
            "peer_expected_nm15":expected,
            "residual":float(residual),
        }

    direction="short" if residual>0 else "long"
    op=float(own["open"]); hi=float(own["high"]); lo=float(own["low"]); cl=float(own["close"])
    rng=float(own["range"])
    body=abs(cl-op)

    if body+1e-12<BODY_FRACTION*rng:
        return {
            "status":"trigger_body_failed","decision_ts":decision_ts,"direction":direction,
            "peer":peer_symbol,"rho":rho,"residual":float(residual),
        }

    if direction=="long":
        if not cl>op:
            return {
                "status":"trigger_direction_failed","decision_ts":decision_ts,
                "direction":direction,"peer":peer_symbol,"rho":rho,"residual":float(residual),
            }
        if hi-cl>CLOSE_OUTER_FRACTION*rng+1e-12:
            return {
                "status":"trigger_close_location_failed","decision_ts":decision_ts,
                "direction":direction,"peer":peer_symbol,"rho":rho,"residual":float(residual),
            }
    else:
        if not cl<op:
            return {
                "status":"trigger_direction_failed","decision_ts":decision_ts,
                "direction":direction,"peer":peer_symbol,"rho":rho,"residual":float(residual),
            }
        if cl-lo>CLOSE_OUTER_FRACTION*rng+1e-12:
            return {
                "status":"trigger_close_location_failed","decision_ts":decision_ts,
                "direction":direction,"peer":peer_symbol,"rho":rho,"residual":float(residual),
            }

    limit=(hi+lo)/2.0
    tick=research_tick(symbol)
    stop=lo-tick if direction=="long" else hi+tick

    if direction=="long" and not limit<cl:
        return {"status":"non_chasing_geometry_failed","decision_ts":decision_ts}
    if direction=="short" and not limit>cl:
        return {"status":"non_chasing_geometry_failed","decision_ts":decision_ts}

    return {
        "status":"armed",
        "decision_ts":decision_ts,
        "direction":direction,
        "trigger_start":own["trigger_start"],
        "peer":peer_symbol,
        "rho":rho,
        "abs_rho":abs(rho),
        "candidate_nm15":own_nm,
        "peer_nm15":peer_nm,
        "peer_expected_nm15":float(expected),
        "residual":float(residual),
        "trigger_open":op,
        "trigger_high":hi,
        "trigger_low":lo,
        "trigger_close":cl,
        "trigger_range":rng,
        "trigger_body_fraction":float(body/rng),
        "limit":float(limit),
        "stop":float(stop),
        "limit_improvement_native":float(cl-limit if direction=="long" else limit-cl),
        "limit_improvement_trigger_range":float(
            (cl-limit)/rng if direction=="long" else (limit-cl)/rng
        ),
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


def self_tests_engine_r_v01()->list[str]:
    tests=[]

    assert even_median([1,2,3,4])==2.5
    tests.append("even_median_exact")

    a=[-2,-1,0,1,2]
    b=[-4,-2,0,2,4]
    c=[4,2,0,-2,-4]
    assert abs(pearson(a,b)-1.0)<1e-12
    assert abs(pearson(a,c)+1.0)<1e-12
    tests.append("pearson_sign_exact")

    assert decision_allowed(pd.Timestamp("2026-04-06T06:05:00Z"))
    assert decision_allowed(pd.Timestamp("2026-04-06T17:55:00Z"))
    assert not decision_allowed(pd.Timestamp("2026-04-06T18:00:00Z"))
    tests.append("continuous_m5_decision_grid")

    dt=pd.Timestamp("2026-04-06T10:05:00Z")
    hist=[(-1.0 if i%2 else 1.0)*(0.001+i*1e-6) for i in range(48)]

    def st(nm,o,h,l,cl,ret=None):
        return {
            "status":"ok","decision_ts":dt,"trigger_start":dt-pd.Timedelta(minutes=5),
            "ret_history":list(hist if ret is None else ret),
            "nm15":float(nm),"open":o,"high":h,"low":l,"close":cl,
            "range":float(h-l),
        }

    # Candidate is +3 normalized vs positively correlated peer +1 -> residual +2 -> short.
    snap={
        "XAUUSD":st(3.0,101.5,102.0,100.0,100.4),
        "AUDUSD":st(1.0,1,2,0,1),
        "EURJPY":st(0.2,1,2,0,1,ret=[x*0.2 for x in hist]),
        "EURUSD":st(0.1,1,2,0,1,ret=[x*0.1 for x in hist]),
        "GBPUSD":st(0.1,1,2,0,1,ret=[x*0.1 for x in hist]),
        "USDCAD":st(0.1,1,2,0,1,ret=[x*0.1 for x in hist]),
        "USDCHF":st(0.1,1,2,0,1,ret=[x*0.1 for x in hist]),
        "USDJPY":st(0.1,1,2,0,1,ret=[x*0.1 for x in hist]),
    }
    sp=strongest_peer("XAUUSD",snap)
    # Multiple peers can tie at |rho|=1; lexicographic tie break must be deterministic.
    assert sp["peer"]=="AUDUSD"
    tests.append("strongest_peer_lexicographic_tie_break")

    x=setup_from_snapshot("XAUUSD",snap)
    assert x["status"]=="armed" and x["direction"]=="short"
    assert x["residual"]>=RESIDUAL_THRESHOLD
    tests.append("positive_residual_maps_to_short")

    # Negative correlation: peer +1 implies candidate expected -1.
    neg=[-x for x in hist]
    snap2=dict(snap)
    snap2["XAUUSD"]=st(-3.0,100.2,102.0,100.0,101.6,ret=hist)
    snap2["AUDUSD"]=st(1.0,1,2,0,1,ret=neg)
    # Make other peers weakly/non-correlated deterministic fixtures.
    for s in ["EURJPY","EURUSD","GBPUSD","USDCAD","USDCHF","USDJPY"]:
        snap2[s]={
            **snap2[s],
            "ret_history":[(i%3-1)*0.0001 + i*1e-8 for i in range(48)],
        }
    x2=setup_from_snapshot("XAUUSD",snap2)
    assert x2["status"]=="armed" and x2["direction"]=="long"
    tests.append("negative_correlation_residual_maps_to_long")

    return tests
