#!/usr/bin/env python3
"""Engine M v0.1 causal multi-timeframe + non-chasing limit-entry mechanics.

No future target/P&L labeling is performed in this module.
"""

from __future__ import annotations

import math
from typing import Optional

import pandas as pd

from engine_k_v0_1 import MAX_NEXT_ENTRY_GAP_MINUTES, resample_ohlc
from engine_k_v0_2 import candidate_economics_v02, research_tick

ORDER_ACTIVE_M1_BARS=10
ORDER_CUTOFF_HOUR=18


def build_mtf_bars(df1:pd.DataFrame)->dict[str,pd.DataFrame]:
    specs={
        "m5":("5min",5,pd.Timedelta(minutes=5)),
        "m15":("15min",15,pd.Timedelta(minutes=15)),
        "h1":("1h",60,pd.Timedelta(hours=1)),
        "h4":("4h",240,pd.Timedelta(hours=4)),
    }
    out={}
    for key,(rule,n,dur) in specs.items():
        x=resample_ohlc(df1,rule,required_count=n).copy()
        x["available_ts"]=x["datetime"]+dur
        out[key]=x
    return out


def _latest_two_completed(bars:pd.DataFrame,decision_ts:pd.Timestamp):
    k=int(bars["available_ts"].searchsorted(decision_ts,side="right"))-1
    if k<1:
        return None
    return bars.iloc[k],bars.iloc[k-1]


def htf_context(h4:pd.DataFrame,h1:pd.DataFrame,decision_ts:pd.Timestamp)->dict:
    p4=_latest_two_completed(h4,decision_ts)
    p1=_latest_two_completed(h1,decision_ts)
    if p4 is None or p1 is None:
        return {"direction":"neutral","reason":"htf_history_unavailable"}
    h40,h41=p4
    h10,h11=p1
    if float(h40["close"])>float(h41["close"]) and float(h10["close"])>float(h11["close"]):
        direction="long"
    elif float(h40["close"])<float(h41["close"]) and float(h10["close"])<float(h11["close"]):
        direction="short"
    else:
        direction="neutral"
    return {
        "direction":direction,
        "h4_0_start":h40["datetime"],
        "h4_1_start":h41["datetime"],
        "h1_0_start":h10["datetime"],
        "h1_1_start":h11["datetime"],
        "h1_mid":(float(h10["high"])+float(h10["low"]))/2.0,
    }


def mtf_setup_at(
    bars:dict[str,pd.DataFrame],
    m15_index:int,
)->dict:
    s15=bars["m15"].iloc[m15_index]
    decision_ts=s15["available_ts"]
    ctx=htf_context(bars["h4"],bars["h1"],decision_ts)
    direction=ctx["direction"]
    if direction=="neutral":
        return {"status":"neutral_context","decision_ts":decision_ts,**ctx}

    mid=float(ctx["h1_mid"])
    if direction=="long":
        if not (float(s15["low"])<=mid and float(s15["close"])>mid):
            return {"status":"m15_reclaim_failed","decision_ts":decision_ts,**ctx}
    else:
        if not (float(s15["high"])>=mid and float(s15["close"])<mid):
            return {"status":"m15_reclaim_failed","decision_ts":decision_ts,**ctx}

    # A5 must be the complete M5 bar ending exactly at the M15 decision time.
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
        ok=(
            float(a5["close"])>float(a5["open"])
            and float(a5["close"])>float(p5["close"])
            and 4.0*(float(a5["high"])-float(a5["close"]))<=rng+1e-12
        )
    else:
        ok=(
            float(a5["close"])<float(a5["open"])
            and float(a5["close"])<float(p5["close"])
            and 4.0*(float(a5["close"])-float(a5["low"]))<=rng+1e-12
        )
    if not ok:
        return {"status":"m5_arm_failed","decision_ts":decision_ts,**ctx}

    limit=(float(a5["high"])+float(a5["low"]))/2.0
    return {
        "status":"armed",
        "decision_ts":decision_ts,
        "direction":direction,
        "h1_mid":mid,
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
        "limit":limit,
        "limit_improvement_native":(
            float(a5["close"])-limit if direction=="long" else limit-float(a5["close"])
        ),
        "limit_improvement_a5_range":(
            (float(a5["close"])-limit)/rng if direction=="long"
            else (limit-float(a5["close"]))/rng
        ),
        **{k:v for k,v in ctx.items() if k!="direction"},
    }


def find_limit_fill(
    df1:pd.DataFrame,
    arm:dict,
    symbol:str,
    usd_jpy_series:Optional[pd.Series]=None,
)->dict:
    if arm.get("status")!="armed":
        raise ValueError("find_limit_fill requires armed setup")
    direction=arm["direction"]
    decision_ts=arm["decision_ts"]
    if decision_ts.hour>=ORDER_CUTOFF_HOUR:
        return {
            "status":"order_window_closed",
            "resolved_ts":decision_ts,
            "filled":False,
        }

    tick=research_tick(symbol)
    limit=float(arm["limit"])
    stop=float(arm["a5_low"]-tick) if direction=="long" else float(arm["a5_high"]+tick)

    if direction=="long":
        assert limit<float(arm["a5_close"])+1e-12
        assert stop<limit
    else:
        assert limit>float(arm["a5_close"])-1e-12
        assert stop>limit

    times=df1["datetime"]
    start=int(times.searchsorted(decision_ts,side="left"))
    if start>=len(df1):
        return {"status":"no_m1_after_arm","resolved_ts":decision_ts,"filled":False}

    cutoff=decision_ts.normalize()+pd.Timedelta(hours=ORDER_CUTOFF_HOUR)
    max_end=min(start+ORDER_ACTIVE_M1_BARS,len(df1))
    prev_ts=decision_ts
    last_ts=decision_ts

    for pos in range(start,max_end):
        row=df1.iloc[pos]
        ts=row["datetime"]
        last_ts=ts
        if ts>=cutoff:
            return {"status":"expired_1800","resolved_ts":cutoff,"filled":False}
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

        entry=limit
        entry_usd_jpy=None
        if symbol=="EURJPY" and usd_jpy_series is not None:
            k=int(usd_jpy_series.index.searchsorted(ts,side="right"))-1
            if k>=0:
                entry_usd_jpy=float(usd_jpy_series.iloc[k])
        econ=candidate_economics_v02(symbol,entry,stop,entry_usd_jpy)
        t40=econ.get("T40") if econ else None

        base={
            "resolved_ts":ts,
            "filled":True,
            "entry_ts":ts,
            "entry":entry,
            "stop":stop,
            "fill_bar_stop_touched":bool(stop_touched),
            "wait_active_m1_bars":pos-start+1,
            "entry_improvement_native":float(arm["limit_improvement_native"]),
            "entry_improvement_a5_range":float(arm["limit_improvement_a5_range"]),
            "stop_distance_native":abs(entry-stop),
            "t40":t40,
        }
        if not t40 or not t40.get("execution_admissible_pre_probability",False):
            return {"status":"filled_economically_rejected",**base}
        return {"status":"admissible_fill",**base}

    return {
        "status":"expired_unfilled",
        "resolved_ts":last_ts+pd.Timedelta(minutes=1),
        "filled":False,
    }


def self_tests_engine_m()->list[str]:
    tests=[]
    # Context mirror.
    h4=pd.DataFrame({
        "datetime":pd.to_datetime(["2026-01-01T00:00Z","2026-01-01T04:00Z"]),
        "available_ts":pd.to_datetime(["2026-01-01T04:00Z","2026-01-01T08:00Z"]),
        "open":[1,1],"high":[2,3],"low":[0,0],"close":[1,2],
    })
    h1=pd.DataFrame({
        "datetime":pd.to_datetime(["2026-01-01T06:00Z","2026-01-01T07:00Z"]),
        "available_ts":pd.to_datetime(["2026-01-01T07:00Z","2026-01-01T08:00Z"]),
        "open":[1,1],"high":[2,3],"low":[0,0],"close":[1,2],
    })
    x=htf_context(h4,h1,pd.Timestamp("2026-01-01T08:00Z"))
    assert x["direction"]=="long"
    tests.append("htf_long_context")

    h4.loc[1,"close"]=0.5
    h1.loc[1,"close"]=0.5
    x=htf_context(h4,h1,pd.Timestamp("2026-01-01T08:00Z"))
    assert x["direction"]=="short"
    tests.append("htf_short_context")

    assert ORDER_ACTIVE_M1_BARS==10 and ORDER_CUTOFF_HOUR==18
    tests.append("frozen_order_constants")
    return tests
