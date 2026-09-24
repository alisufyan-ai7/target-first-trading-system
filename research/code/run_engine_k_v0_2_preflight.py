#!/usr/bin/env python3
"""EXP-023 Engine K v0.2 zero-outcome preflight.

No target labels or model outcomes are calculated.
Only execution-research markets through 2026-06-30 are parsed into state/economic diagnostics.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from engine_k_v0_1 import (
    EXECUTION_MARKETS,
    SOURCES,
    build_context,
    _latest_confirmed_pivot,
    next_active_entry,
    latest_completed_hour_context,
    causal_state_features,
    rung_features,
    download_pinned,
)
from engine_k_v0_2 import (
    candidate_economics_v02,
    research_tick,
    self_tests_v02,
)

ROOT=Path(__file__).resolve().parents[2]
CACHE=Path("/tmp/engine-k-v02-preflight-data")
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

START=pd.Timestamp("2026-03-23",tz="UTC")
CUTOFF=pd.Timestamp("2026-07-01",tz="UTC")
SESSION_CUTOFF_HOUR=20


def load_scoped(path:Path,symbol:str)->pd.DataFrame:
    required=["datetime","open","high","low","close","volume"]
    parts=[]
    reached=False
    for chunk in pd.read_csv(path,chunksize=50000):
        if list(chunk.columns[:6])!=required:
            raise RuntimeError(f"{symbol}: unexpected columns")
        chunk=chunk[required].copy()
        chunk["datetime"]=pd.to_datetime(chunk["datetime"],utc=True,errors="raise")
        mask=chunk["datetime"]<CUTOFF
        if mask.any():
            x=chunk.loc[mask].copy()
            for col in ["open","high","low","close","volume"]:
                x[col]=pd.to_numeric(x[col],errors="raise")
            parts.append(x)
        if (~mask).any():
            reached=True
            break
    if not reached:
        raise RuntimeError(f"{symbol}: July seal sentinel not reached")
    df=pd.concat(parts,ignore_index=True)
    df=df[df["datetime"]>=START].reset_index(drop=True)
    if df.empty or not (df["datetime"]<CUTOFF).all():
        raise RuntimeError(f"{symbol}: scope failure")
    if df["datetime"].duplicated().any() or not df["datetime"].is_monotonic_increasing:
        raise RuntimeError(f"{symbol}: timestamp integrity")
    if (df[["open","high","low","close"]]<=0).any().any():
        raise RuntimeError(f"{symbol}: nonpositive price")
    if (df["high"]<df[["open","close","low"]].max(axis=1)).any():
        raise RuntimeError(f"{symbol}: invalid high")
    if (df["low"]>df[["open","close","high"]].min(axis=1)).any():
        raise RuntimeError(f"{symbol}: invalid low")
    return df


def market_preflight(symbol:str,df1:pd.DataFrame,usd_jpy_df:pd.DataFrame|None=None)->dict:
    b5,h1=build_context(df1)
    usd_jpy_series=None
    if usd_jpy_df is not None:
        usd_jpy_series=usd_jpy_df.set_index("datetime")["close"].sort_index()

    structural=0
    admissible_states=0
    admissible_rungs=0
    feature_complete_admissible_rungs=0
    by_rung={"T30":0,"T40":0,"T50":0}
    by_direction={"long":0,"short":0}
    examples=[]

    tick=research_tick(symbol)

    for i in range(50,len(b5)):
        bar=b5.iloc[i]
        decision_start=bar["datetime"]
        decision_end=decision_start+pd.Timedelta(minutes=5)
        if decision_end>=CUTOFF:
            break
        if decision_end.weekday()>=5:
            continue
        minutes=decision_end.hour*60+decision_end.minute
        if not (0<=minutes<SESSION_CUTOFF_HOUR*60):
            continue

        hc=latest_completed_hour_context(h1,decision_end)
        if hc is None:
            continue
        nxt=next_active_entry(df1,decision_start)
        if nxt is None:
            continue
        entry_ts,entry=nxt
        if entry_ts.date()!=decision_start.date():
            continue

        usd_jpy=None
        if symbol=="EURJPY" and usd_jpy_series is not None:
            pos=usd_jpy_series.index.searchsorted(entry_ts,side="right")-1
            if pos>=0:
                usd_jpy=float(usd_jpy_series.iloc[pos])

        for direction in ("long","short"):
            pivot=_latest_confirmed_pivot(b5,i,direction)
            if pivot is None:
                continue
            stop=pivot-tick if direction=="long" else pivot+tick
            if direction=="long" and not stop<entry:
                continue
            if direction=="short" and not stop>entry:
                continue
            structural+=1

            common=causal_state_features(symbol,b5,i,direction,entry,stop,hc)
            if common is None:
                continue

            econ=candidate_economics_v02(symbol,entry,stop,usd_jpy)
            admitted=[r for r,e in econ.items() if e.get("execution_admissible_pre_probability",False)]
            if not admitted:
                continue

            admissible_states+=1
            by_direction[direction]+=1
            admissible_rungs+=len(admitted)

            for rung in admitted:
                by_rung[rung]+=1
                rf=rung_features(common,econ[rung])
                if len(rf)!=29:
                    raise RuntimeError(f"{symbol}: feature contract mismatch")
                feature_complete_admissible_rungs+=1

            if len(examples)<3:
                examples.append({
                    "decision_ts":str(decision_end),
                    "direction":direction,
                    "entry":entry,
                    "stop":stop,
                    "admitted_rungs":admitted,
                    "economics":{r:econ[r] for r in admitted},
                })

    return {
        "m1_rows":len(df1),
        "bars_5m":len(b5),
        "bars_1h":len(h1),
        "structural_states":structural,
        "unique_economically_admissible_states":admissible_states,
        "economically_admissible_rungs":admissible_rungs,
        "feature_complete_admissible_rungs":feature_complete_admissible_rungs,
        "admissible_by_rung":by_rung,
        "admissible_by_direction":by_direction,
        "examples":examples,
    }


def main():
    tests=self_tests_v02()
    data={}
    for symbol in EXECUTION_MARKETS:
        p=download_pinned(symbol,CACHE)
        data[symbol]=load_scoped(p,symbol)

    markets={}
    for symbol in EXECUTION_MARKETS:
        uj=data["USDJPY"] if symbol=="EURJPY" else None
        markets[symbol]=market_preflight(symbol,data[symbol],uj)

    gate={
        s:markets[s]["unique_economically_admissible_states"]>=200
        for s in EXECUTION_MARKETS
    }
    passed=all(gate.values())

    result={
        "experiment":"EXP-023",
        "engine":"Engine K v0.2",
        "stage":"zero_outcome_preflight",
        "target_outcomes_calculated":False,
        "model_outcomes_calculated":False,
        "secondary_test_loaded_or_inspected":False,
        "final_holdout_loaded_or_inspected":False,
        "parsed_market_data_max_timestamp":str(max(df["datetime"].max() for df in data.values())),
        "execution_markets":list(EXECUTION_MARKETS),
        "self_tests_v02":tests,
        "markets":markets,
        "preflight_gate_ge_200_admissible_states_each":gate,
        "preflight_pass":passed,
        "totals":{
            "structural_states":sum(x["structural_states"] for x in markets.values()),
            "unique_economically_admissible_states":sum(x["unique_economically_admissible_states"] for x in markets.values()),
            "economically_admissible_rungs":sum(x["economically_admissible_rungs"] for x in markets.values()),
        },
    }

    out=OUT/"EXP-023-preflight-v0.2.json"
    out.write_text(json.dumps(result,indent=2,default=str)+"\n")
    print(json.dumps({
        "preflight_pass":passed,
        "gate":gate,
        "totals":result["totals"],
        "target_outcomes_calculated":False,
        "model_outcomes_calculated":False,
    },indent=2))
    print(f"WROTE {out}")
    if not passed:
        raise SystemExit("EXP-023 zero-outcome economic coverage gate failed")


if __name__=="__main__":
    main()
