#!/usr/bin/env python3
"""Download HistData.com M1 bars for EXP-041 third-source adjudication."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from histdata_fetcher import fetch_data

SYMBOLS=("XAUUSD","EURUSD","GBPUSD","USDJPY","EURJPY","AUDUSD","USDCAD","USDCHF")
OUT=Path(os.environ.get("EXP041_HISTDATA_DIR","/tmp/exp041-histdata"))
START=pd.Timestamp("2026-03-23T00:00:00Z")
END=pd.Timestamp("2026-07-01T00:00:00Z")


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for symbol in SYMBOLS:
        # Fetch one local-EST day earlier so the UTC window starts cleanly.
        r=fetch_data(
            pair=symbol,
            start_date="2026-03-22",
            end_date="2026-06-30",
            timeframe="1min",
            output_format=None,
            max_workers=2,
        )
        if not r.ok or r.data.empty:
            raise RuntimeError(f"{symbol}: HistData download failed: {r.failed_periods}")
        x=r.data.copy()
        # HistData M1 timestamps are fixed EST = UTC-5, no DST.
        dt=pd.to_datetime(x["datetime"],errors="raise")
        dt=dt.dt.tz_localize("Etc/GMT+5").dt.tz_convert("UTC")
        x["datetime"]=dt
        x=x[(x["datetime"]>=START)&(x["datetime"]<END)].copy()
        cols=["datetime","open","high","low","close","volume"]
        x=x[cols].sort_values("datetime").drop_duplicates("datetime",keep="last")
        if x.empty:
            raise RuntimeError(f"{symbol}: no rows after UTC scoping")
        p=OUT/f"{symbol}.csv"
        x.to_csv(p,index=False)
        print(symbol,len(x),x["datetime"].min(),x["datetime"].max(),list(r.fetched_periods),len(r.failed_periods))


if __name__=="__main__":
    main()
