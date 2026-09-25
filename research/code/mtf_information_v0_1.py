#!/usr/bin/env python3
"""EXP-040 causal multi-timeframe information features and labels.

This module does not implement a trading strategy. It creates a broad structural
candidate universe and nested information sets for information-content testing.
"""

from __future__ import annotations

import math
from collections import defaultdict
from typing import Optional

import numpy as np
import pandas as pd

from engine_k_v0_1 import _latest_confirmed_pivot
from engine_k_v0_2 import research_tick
from engine_m_v0_1 import build_mtf_bars

TARGET_R_MULTIPLES={
    "T30eq":1.5,
    "T40eq":2.0,
    "T50eq":2.5,
    "T70eq":3.5,
    "T100eq":5.0,
}
MAX_ACTIVE_M1=120
SESSION_CUTOFF_HOUR=20
ENTRY_CUTOFF_HOUR=18

BASE_FEATURES=(
    "m5_signed_move_5m",
    "m5_signed_move_15m",
    "m5_signed_move_30m",
    "m5_ema10_minus_ema30_dir",
    "m5_ema10_slope_15m_dir",
    "m5_tr_over_med20",
    "m5_compression_ratio",
    "m5_body_over_range",
    "m5_dir_close_location",
    "m5_prior3_body_balance_dir",
    "stop_distance_over_m5_medtr",
    "utc_hour_sin",
    "utc_hour_cos",
    "weekday",
)
M15_FEATURES=(
    "m15_signed_move_15m",
    "m15_signed_move_30m",
    "m15_signed_move_60m",
    "m15_ema5_minus_ema12_dir",
    "m15_ema5_slope_dir",
    "m15_tr_over_med20",
    "m15_dir_pos_2h",
    "m15_dir_pos_4h",
)
H1_FEATURES=(
    "h1_signed_move_1h",
    "h1_signed_move_3h",
    "h1_signed_move_6h",
    "h1_ema3_minus_ema8_dir",
    "h1_tr_over_med20",
    "h1_dir_pos_6h",
    "h1_dir_pos_12h",
)
H4_D1_FEATURES=(
    "h4_signed_move_4h",
    "h4_signed_move_8h",
    "h4_signed_move_12h",
    "h4_ema3_minus_ema6_dir",
    "h4_tr_over_med6",
    "h4_dir_pos_24h",
    "prev_day_dir_position",
    "prev_day_distance_to_favorable_boundary_vol",
    "prev_day_distance_from_adverse_boundary_vol",
    "prev_day_body_dir",
)
SESSION_FEATURES=(
    "asia_available",
    "asia_dir_position",
    "asia_distance_to_favorable_boundary_vol",
    "asia_distance_from_adverse_boundary_vol",
    "london_available",
    "london_dir_position",
    "london_distance_to_favorable_boundary_vol",
    "london_distance_from_adverse_boundary_vol",
)

FEATURE_SETS={
    "LOCAL_M5":BASE_FEATURES,
    "PLUS_M15":BASE_FEATURES+M15_FEATURES,
    "PLUS_H1":BASE_FEATURES+M15_FEATURES+H1_FEATURES,
    "PLUS_H4_D1":BASE_FEATURES+M15_FEATURES+H1_FEATURES+H4_D1_FEATURES,
    "PLUS_SESSION":BASE_FEATURES+M15_FEATURES+H1_FEATURES+H4_D1_FEATURES+SESSION_FEATURES,
}


def add_state_columns(x:pd.DataFrame,fast:int,slow:int,med_window:int)->pd.DataFrame:
    out=x.copy()
    prev=out["close"].shift(1)
    out["tr"]=np.maximum.reduce([
        (out["high"]-out["low"]).to_numpy(),
        (out["high"]-prev).abs().fillna(0).to_numpy(),
        (out["low"]-prev).abs().fillna(0).to_numpy(),
    ])
    out[f"ema{fast}"]=out["close"].ewm(span=fast,adjust=False).mean()
    out[f"ema{slow}"]=out["close"].ewm(span=slow,adjust=False).mean()
    out["medtr"]=out["tr"].rolling(med_window,min_periods=med_window).median()
    return out


def build_augmented_bars(df1:pd.DataFrame)->dict[str,pd.DataFrame]:
    bars=build_mtf_bars(df1)
    bars["m5"]=add_state_columns(bars["m5"],10,30,20)
    bars["m5"]["pivot_high_raw"]=(
        (bars["m5"]["high"]>bars["m5"]["high"].shift(1))
        & (bars["m5"]["high"]>bars["m5"]["high"].shift(2))
        & (bars["m5"]["high"]>bars["m5"]["high"].shift(-1))
        & (bars["m5"]["high"]>bars["m5"]["high"].shift(-2))
    )
    bars["m5"]["pivot_low_raw"]=(
        (bars["m5"]["low"]<bars["m5"]["low"].shift(1))
        & (bars["m5"]["low"]<bars["m5"]["low"].shift(2))
        & (bars["m5"]["low"]<bars["m5"]["low"].shift(-1))
        & (bars["m5"]["low"]<bars["m5"]["low"].shift(-2))
    )
    bars["m15"]=add_state_columns(bars["m15"],5,12,20)
    bars["h1"]=add_state_columns(bars["h1"],3,8,20)
    bars["h4"]=add_state_columns(bars["h4"],3,6,6)
    return bars


def build_daily_table(df1:pd.DataFrame)->pd.DataFrame:
    x=df1.set_index("datetime")
    d=x.resample("1D",label="left",closed="left").agg(
        open=("open","first"),
        high=("high","max"),
        low=("low","min"),
        close=("close","last"),
        n=("close","count"),
    ).dropna(subset=["open","high","low","close"]).reset_index()
    d=d[d["n"]>=600].copy()
    d["available_ts"]=d["datetime"]+pd.Timedelta(days=1)
    return d.reset_index(drop=True)


def build_session_tables(df1:pd.DataFrame)->dict[str,dict[str,dict]]:
    out={"asia":{},"london":{}}
    z=df1.copy()
    z["date"]=z["datetime"].dt.date.astype(str)
    mins=z["datetime"].dt.hour*60+z["datetime"].dt.minute
    specs={
        "asia":((mins>=0)&(mins<6*60),300),
        "london":((mins>=7*60)&(mins<12*60),250),
    }
    for name,(mask,min_rows) in specs.items():
        g=z.loc[mask].groupby("date",sort=True)
        for day,grp in g:
            if len(grp)<min_rows:
                continue
            out[name][day]={
                "high":float(grp["high"].max()),
                "low":float(grp["low"].min()),
                "close":float(grp.iloc[-1]["close"]),
                "n":int(len(grp)),
            }
    return out


def latest_completed_index(bars:pd.DataFrame,decision_ts:pd.Timestamp)->int:
    k=int(bars["available_ts"].searchsorted(decision_ts,side="right"))-1
    return k


def directional_position(close:float,lo:float,hi:float,d:float)->Optional[float]:
    if not (math.isfinite(close) and math.isfinite(lo) and math.isfinite(hi)) or hi<=lo:
        return None
    p=(close-lo)/(hi-lo)
    return float(p if d>0 else 1.0-p)


def directional_boundary_distances(
    close:float,lo:float,hi:float,d:float,vol:float
)->tuple[Optional[float],Optional[float]]:
    if hi<=lo or vol<=0:
        return None,None
    if d>0:
        fav=(hi-close)/vol
        adverse=(close-lo)/vol
    else:
        fav=(close-lo)/vol
        adverse=(hi-close)/vol
    return float(fav),float(adverse)


def _window_dir_pos(bars:pd.DataFrame,k:int,n:int,d:float)->Optional[float]:
    if k<n-1:
        return None
    w=bars.iloc[k-n+1:k+1]
    return directional_position(
        float(bars.iloc[k]["close"]),
        float(w["low"].min()),
        float(w["high"].max()),
        d,
    )


def base_features(
    b5:pd.DataFrame,
    i:int,
    direction:str,
    entry:float,
    stop:float,
)->Optional[dict]:
    if i<32:
        return None
    r=b5.iloc[i]
    med=float(r["medtr"])
    if not math.isfinite(med) or med<=0:
        return None
    d=1.0 if direction=="long" else -1.0
    close=float(r["close"])
    rng=float(r["high"]-r["low"])
    if rng<=0:
        return None

    prior12=b5.iloc[i-14:i-2]
    last3=b5.iloc[i-2:i+1]
    if len(prior12)!=12 or len(last3)!=3:
        return None
    prior_med=float(prior12["tr"].median())
    last3_mean=float(last3["tr"].mean())
    if not math.isfinite(prior_med) or prior_med<=0:
        return None
    den=float((last3["high"]-last3["low"]).sum())
    if den<=0:
        return None

    decision_ts=r["available_ts"]
    minutes=decision_ts.hour*60+decision_ts.minute
    angle=2.0*math.pi*minutes/(24.0*60.0)
    dir_close=(close-float(r["low"]))/rng if d>0 else (float(r["high"])-close)/rng

    out={
        "m5_signed_move_5m":d*(close-float(b5.iloc[i-1]["close"]))/med,
        "m5_signed_move_15m":d*(close-float(b5.iloc[i-3]["close"]))/med,
        "m5_signed_move_30m":d*(close-float(b5.iloc[i-6]["close"]))/med,
        "m5_ema10_minus_ema30_dir":d*float(r["ema10"]-r["ema30"])/med,
        "m5_ema10_slope_15m_dir":d*float(r["ema10"]-b5.iloc[i-3]["ema10"])/med,
        "m5_tr_over_med20":float(r["tr"])/med,
        "m5_compression_ratio":last3_mean/prior_med,
        "m5_body_over_range":abs(float(r["close"]-r["open"]))/rng,
        "m5_dir_close_location":float(dir_close),
        "m5_prior3_body_balance_dir":d*float((last3["close"]-last3["open"]).sum())/den,
        "stop_distance_over_m5_medtr":abs(entry-stop)/med,
        "utc_hour_sin":math.sin(angle),
        "utc_hour_cos":math.cos(angle),
        "weekday":float(decision_ts.weekday()),
    }
    if not all(math.isfinite(float(v)) for v in out.values()):
        return None
    return out


def m15_features(b:pd.DataFrame,decision_ts:pd.Timestamp,d:float)->Optional[dict]:
    k=latest_completed_index(b,decision_ts)
    if k<20:
        return None
    r=b.iloc[k]
    med=float(r["medtr"])
    if not math.isfinite(med) or med<=0:
        return None
    pos8=_window_dir_pos(b,k,8,d)
    pos16=_window_dir_pos(b,k,16,d)
    if pos8 is None or pos16 is None:
        return None
    close=float(r["close"])
    out={
        "m15_signed_move_15m":d*(close-float(b.iloc[k-1]["close"]))/med,
        "m15_signed_move_30m":d*(close-float(b.iloc[k-2]["close"]))/med,
        "m15_signed_move_60m":d*(close-float(b.iloc[k-4]["close"]))/med,
        "m15_ema5_minus_ema12_dir":d*float(r["ema5"]-r["ema12"])/med,
        "m15_ema5_slope_dir":d*float(r["ema5"]-b.iloc[k-1]["ema5"])/med,
        "m15_tr_over_med20":float(r["tr"])/med,
        "m15_dir_pos_2h":pos8,
        "m15_dir_pos_4h":pos16,
    }
    return out if all(math.isfinite(float(v)) for v in out.values()) else None


def h1_features(b:pd.DataFrame,decision_ts:pd.Timestamp,d:float)->Optional[dict]:
    k=latest_completed_index(b,decision_ts)
    if k<20:
        return None
    r=b.iloc[k]
    med=float(r["medtr"])
    if not math.isfinite(med) or med<=0:
        return None
    pos6=_window_dir_pos(b,k,6,d)
    pos12=_window_dir_pos(b,k,12,d)
    if pos6 is None or pos12 is None:
        return None
    close=float(r["close"])
    out={
        "h1_signed_move_1h":d*(close-float(b.iloc[k-1]["close"]))/med,
        "h1_signed_move_3h":d*(close-float(b.iloc[k-3]["close"]))/med,
        "h1_signed_move_6h":d*(close-float(b.iloc[k-6]["close"]))/med,
        "h1_ema3_minus_ema8_dir":d*float(r["ema3"]-r["ema8"])/med,
        "h1_tr_over_med20":float(r["tr"])/med,
        "h1_dir_pos_6h":pos6,
        "h1_dir_pos_12h":pos12,
    }
    return out if all(math.isfinite(float(v)) for v in out.values()) else None


def h4_d1_features(
    h4:pd.DataFrame,
    daily:pd.DataFrame,
    decision_ts:pd.Timestamp,
    current_close:float,
    d:float,
    m5_medtr:float,
)->Optional[dict]:
    k=latest_completed_index(h4,decision_ts)
    if k<6:
        return None
    r=h4.iloc[k]
    med=float(r["medtr"])
    if not math.isfinite(med) or med<=0 or m5_medtr<=0:
        return None
    pos6=_window_dir_pos(h4,k,6,d)
    if pos6 is None:
        return None
    close=float(r["close"])

    kd=latest_completed_index(daily,decision_ts)
    if kd<0:
        return None
    dr=daily.iloc[kd]
    dlo=float(dr["low"]); dhi=float(dr["high"]); dcl=float(dr["close"]); dop=float(dr["open"])
    dpos=directional_position(current_close,dlo,dhi,d)
    fav,adv=directional_boundary_distances(current_close,dlo,dhi,d,m5_medtr)
    drng=dhi-dlo
    if dpos is None or fav is None or adv is None or drng<=0:
        return None

    out={
        "h4_signed_move_4h":d*(close-float(h4.iloc[k-1]["close"]))/med,
        "h4_signed_move_8h":d*(close-float(h4.iloc[k-2]["close"]))/med,
        "h4_signed_move_12h":d*(close-float(h4.iloc[k-3]["close"]))/med,
        "h4_ema3_minus_ema6_dir":d*float(r["ema3"]-r["ema6"])/med,
        "h4_tr_over_med6":float(r["tr"])/med,
        "h4_dir_pos_24h":pos6,
        "prev_day_dir_position":dpos,
        "prev_day_distance_to_favorable_boundary_vol":fav,
        "prev_day_distance_from_adverse_boundary_vol":adv,
        "prev_day_body_dir":d*(dcl-dop)/drng,
    }
    return out if all(math.isfinite(float(v)) for v in out.values()) else None


def session_features(
    sessions:dict[str,dict[str,dict]],
    decision_ts:pd.Timestamp,
    current_close:float,
    d:float,
    m5_medtr:float,
)->Optional[dict]:
    if m5_medtr<=0:
        return None
    day=decision_ts.date().isoformat()
    out={}
    for name,available_after in (("asia",6),("london",12)):
        available=decision_ts.hour>=available_after and day in sessions[name]
        out[f"{name}_available"]=1.0 if available else 0.0
        if not available:
            out[f"{name}_dir_position"]=0.0
            out[f"{name}_distance_to_favorable_boundary_vol"]=0.0
            out[f"{name}_distance_from_adverse_boundary_vol"]=0.0
            continue
        s=sessions[name][day]
        lo=float(s["low"]); hi=float(s["high"])
        pos=directional_position(current_close,lo,hi,d)
        fav,adv=directional_boundary_distances(current_close,lo,hi,d,m5_medtr)
        if pos is None or fav is None or adv is None:
            return None
        out[f"{name}_dir_position"]=pos
        out[f"{name}_distance_to_favorable_boundary_vol"]=fav
        out[f"{name}_distance_from_adverse_boundary_vol"]=adv
    return out


def extract_features(
    bars:dict[str,pd.DataFrame],
    daily:pd.DataFrame,
    sessions:dict[str,dict[str,dict]],
    m5_index:int,
    direction:str,
    entry:float,
    stop:float,
)->Optional[dict]:
    b5=bars["m5"]
    base=base_features(b5,m5_index,direction,entry,stop)
    if base is None:
        return None
    decision_ts=b5.iloc[m5_index]["available_ts"]
    d=1.0 if direction=="long" else -1.0
    f15=m15_features(bars["m15"],decision_ts,d)
    f1=h1_features(bars["h1"],decision_ts,d)
    m5_med=float(b5.iloc[m5_index]["medtr"])
    f4=h4_d1_features(
        bars["h4"],daily,decision_ts,float(b5.iloc[m5_index]["close"]),d,m5_med
    )
    fs=session_features(
        sessions,decision_ts,float(b5.iloc[m5_index]["close"]),d,m5_med
    )
    if any(x is None for x in (f15,f1,f4,fs)):
        return None
    out={**base,**f15,**f1,**f4,**fs}
    expected=set(FEATURE_SETS["PLUS_SESSION"])
    if set(out)!=expected:
        raise AssertionError(f"feature set mismatch missing={expected-set(out)} extra={set(out)-expected}")
    if not all(math.isfinite(float(v)) for v in out.values()):
        return None
    return out


def first_active_entry(df1:pd.DataFrame,decision_ts:pd.Timestamp):
    k=int(df1["datetime"].searchsorted(decision_ts,side="left"))
    if k>=len(df1):
        return None
    row=df1.iloc[k]
    ts=row["datetime"]
    if ts-decision_ts>pd.Timedelta(minutes=5):
        return None
    if ts.date()!=decision_ts.date() or ts.hour>=ENTRY_CUTOFF_HOUR:
        return None
    return ts,float(row["open"])


def label_structural_path(
    df1:pd.DataFrame,
    entry_ts:pd.Timestamp,
    entry:float,
    stop:float,
    direction:str,
)->dict:
    stop_dist=abs(entry-stop)
    if stop_dist<=0:
        raise ValueError("invalid stop distance")
    targets={
        name:(entry+m*stop_dist if direction=="long" else entry-m*stop_dist)
        for name,m in TARGET_R_MULTIPLES.items()
    }
    hit={name:False for name in TARGET_R_MULTIPLES}
    hit_ts={name:None for name in TARGET_R_MULTIPLES}

    start=int(df1["datetime"].searchsorted(entry_ts,side="left"))
    if start>=len(df1) or df1.iloc[start]["datetime"]!=entry_ts:
        raise RuntimeError("entry timestamp missing")
    cutoff=entry_ts.normalize()+pd.Timedelta(hours=SESSION_CUTOFF_HOUR)
    sign=1.0 if direction=="long" else -1.0
    mfe=0.0
    mae=0.0
    processed=0
    outcome_end="timeout"
    exit_ts=entry_ts

    for k in range(start,min(start+MAX_ACTIVE_M1,len(df1))):
        row=df1.iloc[k]
        ts=row["datetime"]
        if ts>=cutoff or ts.date()!=entry_ts.date():
            break
        processed+=1
        hi=float(row["high"]); lo=float(row["low"])
        fav=(hi-entry)/stop_dist if direction=="long" else (entry-lo)/stop_dist
        adv=(entry-lo)/stop_dist if direction=="long" else (hi-entry)/stop_dist
        mfe=max(mfe,float(fav))
        mae=max(mae,float(adv))
        stop_hit=(lo<=stop) if direction=="long" else (hi>=stop)
        if stop_hit:
            outcome_end="stop"
            exit_ts=ts
            break
        for name,target in targets.items():
            if hit[name]:
                continue
            touched=(hi>=target) if direction=="long" else (lo<=target)
            if touched:
                hit[name]=True
                hit_ts[name]=ts
        exit_ts=ts

    if processed<=0:
        raise RuntimeError("zero active M1 bars")
    return {
        "labels":{k:int(v) for k,v in hit.items()},
        "hit_ts":{k:(str(v) if v is not None else None) for k,v in hit_ts.items()},
        "mfe_r":float(mfe),
        "mae_r":float(mae),
        "path_end":outcome_end,
        "path_exit_ts":exit_ts,
        "active_m1_bars":processed,
    }


def build_candidate_rows(symbol:str,df1:pd.DataFrame)->list[dict]:
    bars=build_augmented_bars(df1)
    daily=build_daily_table(df1)
    sessions=build_session_tables(df1)
    b5=bars["m5"]
    rows=[]
    tick=research_tick(symbol)

    for i in range(40,len(b5)):
        r=b5.iloc[i]
        decision_ts=r["available_ts"]
        if decision_ts.weekday()>=5:
            continue
        minutes=decision_ts.hour*60+decision_ts.minute
        if not (6*60+5<=minutes<=17*60+55):
            continue
        entry_info=first_active_entry(df1,decision_ts)
        if entry_info is None:
            continue
        entry_ts,entry=entry_info

        for direction in ("long","short"):
            pivot=_latest_confirmed_pivot(b5,i,direction,max_age_bars=12)
            if pivot is None:
                continue
            stop=float(pivot-tick) if direction=="long" else float(pivot+tick)
            if direction=="long" and not stop<entry:
                continue
            if direction=="short" and not stop>entry:
                continue
            feats=extract_features(bars,daily,sessions,i,direction,entry,stop)
            if feats is None:
                continue
            lab=label_structural_path(df1,entry_ts,entry,stop,direction)
            rows.append({
                "symbol":symbol,
                "direction":direction,
                "decision_ts":decision_ts,
                "entry_ts":entry_ts,
                "entry":float(entry),
                "stop":float(stop),
                "stop_distance":abs(float(entry-stop)),
                "features":feats,
                **lab,
            })
    return rows


def self_tests_mtf_information()->list[str]:
    tests=[]
    assert TARGET_R_MULTIPLES=={
        "T30eq":1.5,"T40eq":2.0,"T50eq":2.5,"T70eq":3.5,"T100eq":5.0
    }
    tests.append("target_r_ladder_exact")

    assert set(FEATURE_SETS)=={
        "LOCAL_M5","PLUS_M15","PLUS_H1","PLUS_H4_D1","PLUS_SESSION"
    }
    prev=set()
    for name in ("LOCAL_M5","PLUS_M15","PLUS_H1","PLUS_H4_D1","PLUS_SESSION"):
        cur=set(FEATURE_SETS[name])
        assert prev.issubset(cur)
        prev=cur
    tests.append("feature_sets_strictly_nested")

    base=pd.Timestamp("2026-04-06T10:00:00Z")
    df=pd.DataFrame({
        "datetime":[base,base+pd.Timedelta(minutes=1)],
        "open":[100.0,100.0],
        "high":[103.0,100.5],
        "low":[98.0,99.5],
        "close":[101.0,100.0],
        "volume":[1.0,1.0],
    })
    x=label_structural_path(df,base,100.0,99.0,"long")
    assert x["labels"]["T30eq"]==0 and x["path_end"]=="stop"
    tests.append("same_bar_stop_first")

    df2=pd.DataFrame({
        "datetime":[base,base+pd.Timedelta(minutes=1)],
        "open":[100.0,100.0],
        "high":[101.0,105.5],
        "low":[99.5,99.5],
        "close":[100.5,105.0],
        "volume":[1.0,1.0],
    })
    y=label_structural_path(df2,base,100.0,99.0,"long")
    assert y["labels"]["T30eq"]==1
    assert y["labels"]["T40eq"]==1
    assert y["labels"]["T50eq"]==1
    assert y["labels"]["T70eq"]==1
    assert y["labels"]["T100eq"]==1
    tests.append("nested_target_hits")

    return tests
