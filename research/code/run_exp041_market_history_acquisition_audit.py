#!/usr/bin/env python3
"""Audit EXP-041 twelve-month Dukascopy M1 acquisition.

No labels, no P&L, no protected-period data.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path

import numpy as np
import pandas as pd

from engine_k_v0_1 import EXECUTION_MARKETS, download_pinned
from run_engine_k_v0_2_training_calibration import load_scoped_csv

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

DATA=Path(os.environ.get("EXP041_DATA_DIR","/tmp/exp041-dukas-m1"))
CURRENT_CACHE=Path("/tmp/exp041-current-pinned")

START=pd.Timestamp("2025-07-01T00:00:00Z")
END=pd.Timestamp("2026-07-01T00:00:00Z")
OVERLAP_START=pd.Timestamp("2026-03-23T00:00:00Z")
SEALED_START=END

MIN_ROWS=300_000
MIN_DATES=240
MIN_EXACT_OVERLAP_RATIO=0.70
MIN_HOURLY_RETURN_CORR=0.95
MAX_MEDIAN_RELATIVE_CLOSE_DIFF=0.005


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda:fh.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def load_duka(path:Path,symbol:str)->pd.DataFrame:
    x=pd.read_csv(path)
    required=["datetime","open","high","low","close","volume"]
    if list(x.columns)!=required:
        raise RuntimeError(f"{symbol}: unexpected normalized columns {list(x.columns)}")
    x["datetime"]=pd.to_datetime(x["datetime"],utc=True,errors="raise")
    for c in required[1:]:
        x[c]=pd.to_numeric(x[c],errors="raise")
    return x


def integrity(symbol:str,x:pd.DataFrame)->dict:
    duplicate_count=int(x["datetime"].duplicated().sum())
    monotonic=bool(x["datetime"].is_monotonic_increasing)
    in_range=bool((x["datetime"]>=START).all() and (x["datetime"]<END).all())
    positive=bool((x[["open","high","low","close"]]>0).all().all())
    geometry=bool(
        (x["high"]>=x[["open","close","low"]].max(axis=1)).all()
        and (x["low"]<=x[["open","close","high"]].min(axis=1)).all()
    )
    first=x["datetime"].min()
    last=x["datetime"].max()
    distinct_dates=int(x["datetime"].dt.date.nunique())
    checks={
        "rows_ge_300k":len(x)>=MIN_ROWS,
        "distinct_dates_ge_240":distinct_dates>=MIN_DATES,
        "first_timestamp_by_july2":bool(first<=pd.Timestamp("2025-07-02T23:59:00Z")),
        "last_timestamp_after_jun30_18utc":bool(last>=pd.Timestamp("2026-06-30T18:00:00Z")),
        "all_rows_inside_frozen_interval":in_range,
        "no_duplicates":duplicate_count==0,
        "timestamps_monotonic":monotonic,
        "positive_prices":positive,
        "valid_ohlc_geometry":geometry,
    }
    return {
        "rows":int(len(x)),
        "distinct_utc_dates":distinct_dates,
        "first_timestamp":str(first),
        "last_timestamp":str(last),
        "duplicate_count":duplicate_count,
        "checks":checks,
        "integrity_pass":bool(all(checks.values())),
    }


def overlap_audit(symbol:str,duka:pd.DataFrame,current:pd.DataFrame)->dict:
    d=duka[(duka["datetime"]>=OVERLAP_START)&(duka["datetime"]<END)][["datetime","close"]].copy()
    c=current[(current["datetime"]>=OVERLAP_START)&(current["datetime"]<END)][["datetime","close"]].copy()

    m=d.merge(c,on="datetime",how="inner",suffixes=("_duka","_current"))
    denom=max(1,min(len(d),len(c)))
    overlap_ratio=len(m)/denom

    if len(m):
        rel=np.abs(m["close_duka"]/m["close_current"]-1.0)
        med_rel=float(np.median(rel))
        p95_rel=float(np.quantile(rel,0.95))
    else:
        med_rel=None
        p95_rel=None

    def hret(x:pd.DataFrame)->pd.Series:
        z=x.set_index("datetime")["close"].resample("1h").last().dropna()
        return np.log(z).diff()

    hd=hret(d).rename("duka")
    hc=hret(c).rename("current")
    hm=pd.concat([hd,hc],axis=1).dropna()
    corr=float(hm["duka"].corr(hm["current"])) if len(hm)>=10 else float("nan")

    checks={
        "exact_m1_overlap_ge_70pct":overlap_ratio>=MIN_EXACT_OVERLAP_RATIO,
        "hourly_return_corr_ge_0_95":math.isfinite(corr) and corr>=MIN_HOURLY_RETURN_CORR,
        "median_relative_close_diff_le_0_5pct":med_rel is not None and med_rel<=MAX_MEDIAN_RELATIVE_CLOSE_DIFF,
    }
    return {
        "duka_overlap_rows":int(len(d)),
        "current_overlap_rows":int(len(c)),
        "exact_timestamp_overlap_rows":int(len(m)),
        "exact_overlap_ratio_of_smaller_feed":float(overlap_ratio),
        "median_abs_relative_close_difference":med_rel,
        "p95_abs_relative_close_difference":p95_rel,
        "hourly_return_common_rows":int(len(hm)),
        "hourly_return_correlation":corr if math.isfinite(corr) else None,
        "checks":checks,
        "sanity_pass":bool(all(checks.values())),
    }


def main():
    npm_meta={}
    meta_path=Path("/tmp/exp041_npm_meta.json")
    if meta_path.exists():
        npm_meta=json.loads(meta_path.read_text())

    markets={}
    max_ts=None

    for symbol in EXECUTION_MARKETS:
        path=DATA/f"{symbol}.csv"
        if not path.exists():
            raise RuntimeError(f"{symbol}: acquired file missing")
        duka=load_duka(path,symbol)
        integ=integrity(symbol,duka)

        current_path=download_pinned(symbol,CURRENT_CACHE)
        current=load_scoped_csv(current_path,symbol,SEALED_START)
        ov=overlap_audit(symbol,duka,current)

        markets[symbol]={
            "normalized_file_sha256":sha256(path),
            "file_bytes":int(path.stat().st_size),
            "integrity":integ,
            "overlap_sanity_vs_existing_pinned_source":ov,
        }
        tsmax=duka["datetime"].max()
        max_ts=tsmax if max_ts is None else max(max_ts,tsmax)

    result={
        "stage":"EXP-041 extended market-history acquisition audit",
        "scientific_outcomes_calculated":False,
        "target_labels_calculated":False,
        "pnl_calculated":False,
        "source":{
            "authority":"Dukascopy Bank historical data",
            "transport_helper":"dukascopy-node",
            "transport_version":"1.50.0",
            "transport_metadata":npm_meta,
            "timeframe":"m1",
            "interval":[str(START),str(END)],
            "normalized_schema":["datetime","open","high","low","close","volume"],
            "raw_files_committed_to_repo":False,
        },
        "markets":markets,
        "parsed_market_data_max_timestamp":str(max_ts),
        "protected_periods":{
            "jul_aug_2026_loaded":False,
            "sep_2026_loaded":False,
        },
        "gate":{
            "all_market_integrity_pass":all(v["integrity"]["integrity_pass"] for v in markets.values()),
            "all_cross_feed_sanity_pass":all(v["overlap_sanity_vs_existing_pinned_source"]["sanity_pass"] for v in markets.values()),
            "hard_source_seal_pass":max_ts<END,
        },
    }
    result["market_history_gate_pass"]=bool(all(result["gate"].values()))

    out=OUT/"EXP-041-extended-market-history-acquisition-audit-v0.1.json"
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")

    print(json.dumps({
        "market_history_gate_pass":result["market_history_gate_pass"],
        "gate":result["gate"],
        "rows":{s:v["integrity"]["rows"] for s,v in markets.items()},
        "overlap_corr":{s:v["overlap_sanity_vs_existing_pinned_source"]["hourly_return_correlation"] for s,v in markets.items()},
        "protected_periods":result["protected_periods"],
        "scientific_outcomes_calculated":False,
    },indent=2))


if __name__=="__main__":
    main()
