#!/usr/bin/env python3
import json
from pathlib import Path

from engine_k_v0_1 import (
    SOURCES,
    download_pinned,
    load_csv,
    preflight_states,
    self_tests,
)

CACHE=Path("/tmp/engine-k-data")
OUT=Path("research/results/exp022")
OUT.mkdir(parents=True, exist_ok=True)

def main():
    result={"self_tests":self_tests(),"markets":{},"target_outcomes_calculated":False}
    data={}
    for symbol in SOURCES:
        path=download_pinned(symbol,CACHE)
        df=load_csv(path,symbol)
        data[symbol]=df
        result["markets"][symbol]={
            "downloaded":True,
            "raw_rows_expected":SOURCES[symbol]["rows"],
            "rows_after_sep23_cut":len(df),
            "first_ts":str(df["datetime"].iloc[0]),
            "last_ts":str(df["datetime"].iloc[-1]),
        }

    for symbol,df in data.items():
        uj=data.get("USDJPY") if symbol=="EURJPY" else None
        result["markets"][symbol]["state_preflight"]=preflight_states(symbol,df,uj)

    out=OUT/"preflight.json"
    out.write_text(json.dumps(result,indent=2,default=str))
    print(json.dumps(result,indent=2,default=str))
    print(f"WROTE {out}")
    print("ENGINE_K_TARGET_OUTCOMES_CALCULATED=NO")

if __name__=="__main__":
    main()
