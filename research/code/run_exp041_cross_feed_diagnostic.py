#!/usr/bin/env python3
"""EXP-041 zero-outcome cross-feed diagnostic."""

from __future__ import annotations

import json, math, os
from pathlib import Path

import numpy as np
import pandas as pd

from engine_k_v0_1 import EXECUTION_MARKETS, download_pinned

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"research/results"; OUT.mkdir(parents=True,exist_ok=True)
DATA=Path(os.environ.get("EXP041_DIAG_DIR","/tmp/exp041-cross-feed"))
CACHE=Path("/tmp/exp041-cross-feed-current")
START=pd.Timestamp("2026-03-23T00:00:00Z")
END=pd.Timestamp("2026-07-01T00:00:00Z")


def load_norm(path:Path)->pd.DataFrame:
    x=pd.read_csv(path)
    x["datetime"]=pd.to_datetime(x["datetime"],utc=True,errors="raise")
    for c in ["open","high","low","close","volume"]:
        x[c]=pd.to_numeric(x[c],errors="raise")
    return x[(x["datetime"]>=START)&(x["datetime"]<END)].reset_index(drop=True)


def load_current(path:Path)->pd.DataFrame:
    parts=[]
    for chunk in pd.read_csv(path,chunksize=50000):
        chunk["datetime"]=pd.to_datetime(chunk["datetime"],utc=True,errors="raise")
        z=chunk[(chunk["datetime"]>=START)&(chunk["datetime"]<END)].copy()
        if len(z): parts.append(z[["datetime","open","high","low","close","volume"]])
        if (chunk["datetime"]>=END).any(): break
    if not parts: raise RuntimeError("no current overlap")
    return pd.concat(parts,ignore_index=True)


def resampled_returns(x:pd.DataFrame,rule:str)->pd.Series:
    c=x.set_index("datetime")["close"].resample(rule).last().dropna()
    return np.log(c).diff().dropna()


def corr_join(a:pd.Series,b:pd.Series)->tuple[float|None,int]:
    z=pd.concat([a.rename("a"),b.rename("b")],axis=1).dropna()
    if len(z)<10: return None,len(z)
    c=float(z["a"].corr(z["b"]))
    return (c if math.isfinite(c) else None),len(z)


def sign_agreement(a:pd.Series,b:pd.Series)->tuple[float|None,int]:
    z=pd.concat([a.rename("a"),b.rename("b")],axis=1).dropna()
    z=z[(z["a"]!=0)|(z["b"]!=0)]
    if not len(z): return None,0
    return float((np.sign(z["a"])==np.sign(z["b"])).mean()),len(z)


def best_lag(a:pd.Series,b:pd.Series,lags:list[int])->dict:
    best=None
    for lag in lags:
        shifted=b.copy()
        shifted.index=shifted.index+lag*(b.index[1]-b.index[0])
        c,n=corr_join(a,shifted)
        if c is None: continue
        if best is None or c>best["correlation"]:
            best={"lag_steps":lag,"correlation":c,"common_rows":n}
    return best or {"lag_steps":None,"correlation":None,"common_rows":0}


def classify(zero5,zero1h,best5,best1h,daily_corr,ratio_daily_std,coverage_gap):
    tags=[]
    shift=False
    if best5["lag_steps"] not in (None,0) and best5["correlation"]>=0.95 and zero5 is not None and best5["correlation"]-zero5>=0.05:
        shift=True
    if best1h["lag_steps"] not in (None,0) and best1h["correlation"]>=0.95 and zero1h is not None and best1h["correlation"]-zero1h>=0.05:
        shift=True
    if shift:
        tags.append("TIME_ALIGNMENT_SUSPECT")
    elif zero1h is not None and zero1h>=0.95 and ratio_daily_std is not None and ratio_daily_std<=0.001:
        tags.append("STABLE_PRICE_BASIS")
    elif daily_corr is not None and daily_corr>=0.95 and zero1h is not None and zero1h<0.95:
        tags.append("HIGH_FREQUENCY_FEED_CONSTRUCTION")
    else:
        tags.append("MATERIAL_PATH_MISMATCH")
    if coverage_gap:
        tags.append("SOURCE_COVERAGE_GAP")
    return tags


def main():
    markets={}
    for symbol in EXECUTION_MARKETS:
        d=load_norm(DATA/f"{symbol}.csv")
        c=load_current(download_pinned(symbol,CACHE))

        exact=d[["datetime","close"]].merge(c[["datetime","close"]],on="datetime",suffixes=("_duka","_current"))
        ratio=exact["close_duka"]/exact["close_current"]
        exact["date"]=exact["datetime"].dt.date.astype(str)
        daily_ratio=exact.groupby("date").apply(lambda q:float(np.median(q["close_duka"]/q["close_current"])),include_groups=False)

        ret={}
        series={}
        for label,rule in [("1m","1min"),("5m","5min"),("15m","15min"),("1h","1h"),("4h","4h"),("1d","1D")]:
            rd=resampled_returns(d,rule); rc=resampled_returns(c,rule)
            co,n=corr_join(rd,rc)
            ret[label]={"correlation":co,"common_rows":n}
            series[label]=(rd,rc)

        s5,n5=sign_agreement(*series["5m"])
        s1,n1=sign_agreement(*series["1h"])
        b5=best_lag(series["5m"][0],series["5m"][1],list(range(-12,13)))
        b1=best_lag(series["1h"][0],series["1h"][1],list(range(-3,4)))

        zh=pd.concat([series["1h"][0].rename("d"),series["1h"][1].rename("c")],axis=1).dropna()
        vol_ratio=float(zh["d"].std()/zh["c"].std()) if len(zh)>10 and zh["c"].std()>0 else None

        denom=max(1,min(len(d),len(c)))
        overlap=len(exact)/denom
        coverage_gap=bool(d["datetime"].max()<pd.Timestamp("2026-06-30T18:00:00Z"))
        drstd=float(np.std(daily_ratio)) if len(daily_ratio) else None

        markets[symbol]={
            "coverage":{
                "duka_rows":len(d),"current_rows":len(c),
                "exact_overlap_rows":len(exact),
                "exact_overlap_ratio_smaller":float(overlap),
                "duka_first":str(d["datetime"].min()),"duka_last":str(d["datetime"].max()),
                "current_first":str(c["datetime"].min()),"current_last":str(c["datetime"].max()),
                "missing_final_day_flag":coverage_gap,
            },
            "price_ratio_duka_over_current":{
                "median":float(np.median(ratio)),
                "p05":float(np.quantile(ratio,0.05)),
                "p95":float(np.quantile(ratio,0.95)),
                "daily_median_std":drstd,
            },
            "return_correlations":ret,
            "direction_agreement":{
                "5m":{"fraction":s5,"n":n5},
                "1h":{"fraction":s1,"n":n1},
            },
            "best_lag":{
                "5m":b5,
                "1h":b1,
            },
            "hourly_return_volatility_ratio_duka_over_current":vol_ratio,
            "diagnostic_tags":classify(
                ret["5m"]["correlation"],ret["1h"]["correlation"],b5,b1,
                ret["1d"]["correlation"],drstd,coverage_gap
            ),
        }

    result={
        "stage":"EXP-041 cross-feed diagnostic v0.1",
        "target_labels_calculated":False,
        "pnl_calculated":False,
        "protected_periods":{"jul_aug_2026_loaded":False,"sep_2026_loaded":False},
        "interval":[str(START),str(END)],
        "markets":markets,
        "summary_tags":{s:v["diagnostic_tags"] for s,v in markets.items()},
        "scientific_disposition":"DIAGNOSTIC_ONLY_DO_NOT_CHANGE_ACQUISITION_V01",
    }
    p=OUT/"EXP-041-cross-feed-diagnostic-v0.1.json"
    p.write_text(json.dumps(result,indent=2,default=str)+"\n")
    print(json.dumps({
        "summary_tags":result["summary_tags"],
        "protected_periods":result["protected_periods"],
        "target_labels_calculated":False,
        "pnl_calculated":False,
    },indent=2))


if __name__=="__main__":
    main()
