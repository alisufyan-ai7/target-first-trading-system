#!/usr/bin/env python3
"""Engine P v0.1 — cross-market relative-strength pullback mechanics."""

from __future__ import annotations

import math
import statistics
import pandas as pd

from engine_k_v0_1 import MAX_NEXT_ENTRY_GAP_MINUTES
from engine_k_v0_2 import research_tick

OWN_MOM_THRESHOLD=1.50
FACTOR_THRESHOLD=0.50
BODY_FRACTION=0.35
CLOSE_OUTER_FRACTION=0.40
BASELINE_M5_BARS=24
MOM_LOOKBACK_BARS=6
ORDER_ACTIVE_M1_BARS=10
ORDER_HARD_MINUTES=30
ENTRY_CUTOFF_HOUR=18

USD_LINKS={
    "EURUSD":-1.0,
    "GBPUSD":-1.0,
    "AUDUSD":-1.0,
    "USDJPY":+1.0,
    "USDCAD":+1.0,
    "USDCHF":+1.0,
}
BASE_USD={"EURUSD","GBPUSD","AUDUSD","XAUUSD"}
USD_QUOTE={"USDJPY","USDCAD","USDCHF"}


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
        and 6*60+5<=minutes<=17*60+55
        and ts.minute in tuple(range(0,60,5))
    )


def metric_at_time(b5:pd.DataFrame,decision_ts:pd.Timestamp)->dict:
    """Causal per-symbol state at one completed-M5 decision time."""
    k=int(b5["available_ts"].searchsorted(decision_ts,side="left"))
    if k>=len(b5) or b5.iloc[k]["available_ts"]!=decision_ts:
        return {"status":"m5_snapshot_unavailable","decision_ts":decision_ts}
    if k<BASELINE_M5_BARS:
        return {"status":"baseline_24x5_unavailable","decision_ts":decision_ts}

    cur=b5.iloc[k]
    prev=b5.iloc[k-BASELINE_M5_BARS:k]
    expected=[
        cur["datetime"]-pd.Timedelta(minutes=5*(BASELINE_M5_BARS-i))
        for i in range(BASELINE_M5_BARS)
    ]
    if list(prev["datetime"])!=expected:
        return {"status":"baseline_24x5_not_contiguous","decision_ts":decision_ts}

    ref=b5.iloc[k-MOM_LOOKBACK_BARS]
    if cur["datetime"]-ref["datetime"]!=pd.Timedelta(minutes=30):
        return {"status":"reference_30m_unavailable","decision_ts":decision_ts}

    ref_close=float(ref["close"])
    close=float(cur["close"])
    if not math.isfinite(ref_close) or ref_close<=0 or not math.isfinite(close) or close<=0:
        return {"status":"invalid_price","decision_ts":decision_ts}

    range_pcts=[]
    for r in prev.itertuples():
        px=float(r.close)
        rng=float(r.high-r.low)
        if px<=0 or rng<0 or not math.isfinite(px) or not math.isfinite(rng):
            return {"status":"invalid_baseline_price","decision_ts":decision_ts}
        range_pcts.append(rng/px)

    vol=even_median(range_pcts)
    if not math.isfinite(vol) or vol<=0:
        return {"status":"baseline_vol_zero","decision_ts":decision_ts}

    move_pct=(close-ref_close)/ref_close
    mom=move_pct/vol

    return {
        "status":"ok",
        "decision_ts":decision_ts,
        "trigger_start":cur["datetime"],
        "open":float(cur["open"]),
        "high":float(cur["high"]),
        "low":float(cur["low"]),
        "close":close,
        "ref_close_30m":ref_close,
        "move_pct_30m":float(move_pct),
        "vol":float(vol),
        "mom":float(mom),
    }


def usd_score(snapshot:dict[str,dict],exclude_symbol:str|None=None)->float|None:
    vals=[]
    for s,sign in USD_LINKS.items():
        if s==exclude_symbol:
            continue
        m=snapshot.get(s)
        if not m or m.get("status")!="ok":
            continue
        vals.append(sign*float(m["mom"]))
    if len(vals)<4:
        return None
    return float(statistics.median(vals))


def factor_direction(symbol:str,snapshot:dict[str,dict])->dict:
    own=snapshot.get(symbol)
    if not own or own.get("status")!="ok":
        return {"status":"candidate_metric_unavailable"}

    mom=float(own["mom"])

    if symbol=="EURJPY":
        eu=snapshot.get("EURUSD")
        uj=snapshot.get("USDJPY")
        if not eu or not uj or eu.get("status")!="ok" or uj.get("status")!="ok":
            return {"status":"eurjpy_leg_snapshot_unavailable"}
        eu_m=float(eu["mom"]); uj_m=float(uj["mom"])
        if mom>=OWN_MOM_THRESHOLD and eu_m>=FACTOR_THRESHOLD and uj_m>=FACTOR_THRESHOLD:
            return {
                "status":"ok","direction":"long","own_mom":mom,
                "eurusd_mom":eu_m,"usdjpy_mom":uj_m,
            }
        if mom<=-OWN_MOM_THRESHOLD and eu_m<=-FACTOR_THRESHOLD and uj_m<=-FACTOR_THRESHOLD:
            return {
                "status":"ok","direction":"short","own_mom":mom,
                "eurusd_mom":eu_m,"usdjpy_mom":uj_m,
            }
        return {
            "status":"cross_factor_failed","own_mom":mom,
            "eurusd_mom":eu_m,"usdjpy_mom":uj_m,
        }

    score=usd_score(snapshot,exclude_symbol=symbol if symbol in USD_LINKS else None)
    if score is None:
        return {"status":"usd_factor_unavailable","own_mom":mom}

    if symbol in BASE_USD:
        if mom>=OWN_MOM_THRESHOLD and score<=-FACTOR_THRESHOLD:
            return {"status":"ok","direction":"long","own_mom":mom,"usd_score":score}
        if mom<=-OWN_MOM_THRESHOLD and score>=FACTOR_THRESHOLD:
            return {"status":"ok","direction":"short","own_mom":mom,"usd_score":score}
    elif symbol in USD_QUOTE:
        if mom>=OWN_MOM_THRESHOLD and score>=FACTOR_THRESHOLD:
            return {"status":"ok","direction":"long","own_mom":mom,"usd_score":score}
        if mom<=-OWN_MOM_THRESHOLD and score<=-FACTOR_THRESHOLD:
            return {"status":"ok","direction":"short","own_mom":mom,"usd_score":score}
    else:
        return {"status":"unsupported_symbol"}

    return {"status":"cross_factor_failed","own_mom":mom,"usd_score":score}


def setup_from_snapshot(symbol:str,snapshot:dict[str,dict])->dict:
    own=snapshot.get(symbol)
    if not own or own.get("status")!="ok":
        return {"status":"candidate_metric_unavailable"}

    decision_ts=own["decision_ts"]
    if not decision_allowed(decision_ts):
        return {"status":"outside_decision_grid","decision_ts":decision_ts}

    fd=factor_direction(symbol,snapshot)
    if fd.get("status")!="ok":
        return {
            "status":fd.get("status","cross_factor_failed"),
            "decision_ts":decision_ts,
            **{k:v for k,v in fd.items() if k!="status"},
        }

    direction=fd["direction"]
    op=float(own["open"]); hi=float(own["high"]); lo=float(own["low"]); cl=float(own["close"])
    rng=hi-lo
    if not math.isfinite(rng) or rng<=0:
        return {"status":"trigger_zero_range","decision_ts":decision_ts,"direction":direction}

    body=abs(cl-op)
    if body+1e-12 < BODY_FRACTION*rng:
        return {"status":"trigger_body_failed","decision_ts":decision_ts,"direction":direction}

    if direction=="long":
        if not cl>op:
            return {"status":"trigger_direction_failed","decision_ts":decision_ts,"direction":direction}
        if hi-cl > CLOSE_OUTER_FRACTION*rng+1e-12:
            return {"status":"trigger_close_location_failed","decision_ts":decision_ts,"direction":direction}
    else:
        if not cl<op:
            return {"status":"trigger_direction_failed","decision_ts":decision_ts,"direction":direction}
        if cl-lo > CLOSE_OUTER_FRACTION*rng+1e-12:
            return {"status":"trigger_close_location_failed","decision_ts":decision_ts,"direction":direction}

    limit=(hi+lo)/2.0
    tick=research_tick(symbol)
    stop=lo-tick if direction=="long" else hi+tick

    if direction=="long" and not limit<cl:
        return {"status":"non_chasing_geometry_failed","decision_ts":decision_ts,"direction":direction}
    if direction=="short" and not limit>cl:
        return {"status":"non_chasing_geometry_failed","decision_ts":decision_ts,"direction":direction}

    out={
        "status":"armed",
        "decision_ts":decision_ts,
        "direction":direction,
        "trigger_start":own["trigger_start"],
        "own_mom":float(fd["own_mom"]),
        "trigger_open":op,
        "trigger_high":hi,
        "trigger_low":lo,
        "trigger_close":cl,
        "trigger_range":float(rng),
        "trigger_body_fraction":float(body/rng),
        "limit":float(limit),
        "stop":float(stop),
        "limit_improvement_native":float(cl-limit if direction=="long" else limit-cl),
        "limit_improvement_trigger_range":float((cl-limit)/rng if direction=="long" else (limit-cl)/rng),
    }
    if "usd_score" in fd:
        out["usd_score"]=float(fd["usd_score"])
    if "eurusd_mom" in fd:
        out["eurusd_mom"]=float(fd["eurusd_mom"])
    if "usdjpy_mom" in fd:
        out["usdjpy_mom"]=float(fd["usdjpy_mom"])
    return out


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


def self_tests_engine_p_v01()->list[str]:
    tests=[]

    assert even_median([1,2,3,4])==2.5
    assert even_median(list(range(1,25)))==12.5
    tests.append("even_median_exact")

    assert decision_allowed(pd.Timestamp("2026-04-06T06:05:00Z"))
    assert decision_allowed(pd.Timestamp("2026-04-06T17:55:00Z"))
    assert not decision_allowed(pd.Timestamp("2026-04-06T18:00:00Z"))
    tests.append("continuous_m5_decision_grid")

    snap={
        "EURUSD":{"status":"ok","mom":2.0},
        "GBPUSD":{"status":"ok","mom":1.0},
        "AUDUSD":{"status":"ok","mom":1.0},
        "USDJPY":{"status":"ok","mom":-1.0},
        "USDCAD":{"status":"ok","mom":-1.0},
        "USDCHF":{"status":"ok","mom":-1.0},
    }
    s=usd_score(snap,exclude_symbol="EURUSD")
    assert s is not None and s<=-0.5
    tests.append("usd_factor_sign_and_self_exclusion")

    snap2={
        "EURUSD":{"status":"ok","mom":-1.0},
        "GBPUSD":{"status":"ok","mom":-1.0},
        "AUDUSD":{"status":"ok","mom":-1.0},
        "USDJPY":{"status":"ok","mom":2.0},
        "USDCAD":{"status":"ok","mom":1.0},
        "USDCHF":{"status":"ok","mom":1.0},
    }
    s2=usd_score(snap2,exclude_symbol="USDJPY")
    assert s2 is not None and s2>=0.5
    tests.append("usd_factor_strong_positive")

    return tests
