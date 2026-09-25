#!/usr/bin/env python3
"""EXP-041 three-feed adjudication. No strategy labels or P&L."""

from __future__ import annotations

import json, math, os
from pathlib import Path

import numpy as np
import pandas as pd

from engine_k_v0_1 import EXECUTION_MARKETS, download_pinned

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"research/results"; OUT.mkdir(parents=True,exist_ok=True)
DUKA=Path(os.environ.get("EXP041_DIAG_DIR","/tmp/exp041-cross-feed"))
HIST=Path(os.environ.get("EXP041_HISTDATA_DIR","/tmp/exp041-histdata"))
CACHE=Path("/tmp/exp041-third-current")
START=pd.Timestamp("2026-03-23T00:00:00Z")
END=pd.Timestamp("2026-07-01T00:00:00Z")


def load_csv(path:Path)->pd.DataFrame:
    x=pd.read_csv(path)
    x["datetime"]=pd.to_datetime(x["datetime"],utc=True,errors="raise")
    for c in ["open","high","low","close","volume"]:
        x[c]=pd.to_numeric(x[c],errors="raise")
    x=x[(x["datetime"]>=START)&(x["datetime"]<END)].copy()
    return x.sort_values("datetime").drop_duplicates("datetime").reset_index(drop=True)


def load_current(path:Path)->pd.DataFrame:
    parts=[]
    for chunk in pd.read_csv(path,chunksize=50000):
        chunk["datetime"]=pd.to_datetime(chunk["datetime"],utc=True,errors="raise")
        z=chunk[(chunk["datetime"]>=START)&(chunk["datetime"]<END)].copy()
        if len(z):
            for c in ["open","high","low","close","volume"]:
                z[c]=pd.to_numeric(z[c],errors="raise")
            parts.append(z[["datetime","open","high","low","close","volume"]])
        if (chunk["datetime"]>=END).any():
            break
    if not parts: raise RuntimeError("no current rows")
    return pd.concat(parts,ignore_index=True).sort_values("datetime").drop_duplicates("datetime")


def returns(x:pd.DataFrame,rule:str)->pd.Series:
    c=x.set_index("datetime")["close"].resample(rule).last().dropna()
    return np.log(c).diff().dropna()


def joined_corr(a:pd.Series,b:pd.Series):
    z=pd.concat([a.rename("a"),b.rename("b")],axis=1).dropna()
    if len(z)<10: return None,0,None
    corr=float(z["a"].corr(z["b"]))
    sign=float((np.sign(z["a"])==np.sign(z["b"])).mean())
    return (corr if math.isfinite(corr) else None),int(len(z)),sign


def pair_stats(a:pd.DataFrame,b:pd.DataFrame)->dict:
    common=a[["datetime","close"]].merge(b[["datetime","close"]],on="datetime",suffixes=("_a","_b"))
    denom=max(1,min(len(a),len(b)))
    overlap=len(common)/denom
    ratio=common["close_a"]/common["close_b"] if len(common) else pd.Series(dtype=float)

    out={
        "m1_overlap_ratio_smaller":float(overlap),
        "common_m1_rows":int(len(common)),
        "median_price_ratio_a_over_b":float(np.median(ratio)) if len(ratio) else None,
        "p05_price_ratio":float(np.quantile(ratio,0.05)) if len(ratio) else None,
        "p95_price_ratio":float(np.quantile(ratio,0.95)) if len(ratio) else None,
        "returns":{},
    }
    for label,rule in (("5m","5min"),("1h","1h"),("1d","1D")):
        c,n,s=joined_corr(returns(a,rule),returns(b,rule))
        out["returns"][label]={"correlation":c,"common_rows":n,"sign_agreement":s}

    r5=out["returns"]["5m"]; r1=out["returns"]["1h"]; rd=out["returns"]["1d"]
    checks={
        "m1_overlap_ge_70pct":overlap>=0.70,
        "corr_5m_ge_0_90":r5["correlation"] is not None and r5["correlation"]>=0.90,
        "corr_1h_ge_0_95":r1["correlation"] is not None and r1["correlation"]>=0.95,
        "corr_1d_ge_0_95":rd["correlation"] is not None and rd["correlation"]>=0.95,
        "sign_agreement_1h_ge_0_95":r1["sign_agreement"] is not None and r1["sign_agreement"]>=0.95,
    }
    out["checks"]=checks
    out["pair_agreement_pass"]=bool(all(checks.values()))
    return out


def adjudicate(cd:bool,ch:bool,dh:bool)->str:
    if dh and not cd and not ch:
        return "CURRENT_PINNED_OUTLIER"
    if ch and not cd and not dh:
        return "DUKASCOPY_OUTLIER"
    if cd and not ch and not dh:
        return "HISTDATA_OUTLIER"
    if sum((cd,ch,dh))>=2:
        return "BROAD_THREE_SOURCE_CONSENSUS"
    return "NO_TWO_SOURCE_CONSENSUS"


def main():
    markets={}
    source_support={"CURRENT_PINNED":0,"DUKASCOPY":0,"HISTDATA":0}
    no_consensus=0

    for symbol in EXECUTION_MARKETS:
        src={
            "CURRENT_PINNED":load_current(download_pinned(symbol,CACHE)),
            "DUKASCOPY":load_csv(DUKA/f"{symbol}.csv"),
            "HISTDATA":load_csv(HIST/f"{symbol}.csv"),
        }
        cd=pair_stats(src["CURRENT_PINNED"],src["DUKASCOPY"])
        ch=pair_stats(src["CURRENT_PINNED"],src["HISTDATA"])
        dh=pair_stats(src["DUKASCOPY"],src["HISTDATA"])
        tag=adjudicate(cd["pair_agreement_pass"],ch["pair_agreement_pass"],dh["pair_agreement_pass"])
        if cd["pair_agreement_pass"]:
            source_support["CURRENT_PINNED"]+=1; source_support["DUKASCOPY"]+=1
        if ch["pair_agreement_pass"]:
            source_support["CURRENT_PINNED"]+=1; source_support["HISTDATA"]+=1
        if dh["pair_agreement_pass"]:
            source_support["DUKASCOPY"]+=1; source_support["HISTDATA"]+=1
        no_consensus+=int(tag=="NO_TWO_SOURCE_CONSENSUS")

        markets[symbol]={
            "rows":{k:int(len(v)) for k,v in src.items()},
            "first_last":{k:[str(v["datetime"].min()),str(v["datetime"].max())] for k,v in src.items()},
            "pairwise":{
                "CURRENT_PINNED__DUKASCOPY":cd,
                "CURRENT_PINNED__HISTDATA":ch,
                "DUKASCOPY__HISTDATA":dh,
            },
            "adjudication":tag,
        }

    # Source supported in a market if at least one passing pair includes it.
    supported_markets={s:0 for s in source_support}
    for symbol,m in markets.items():
        p=m["pairwise"]
        if p["CURRENT_PINNED__DUKASCOPY"]["pair_agreement_pass"] or p["CURRENT_PINNED__HISTDATA"]["pair_agreement_pass"]:
            supported_markets["CURRENT_PINNED"]+=1
        if p["CURRENT_PINNED__DUKASCOPY"]["pair_agreement_pass"] or p["DUKASCOPY__HISTDATA"]["pair_agreement_pass"]:
            supported_markets["DUKASCOPY"]+=1
        if p["CURRENT_PINNED__HISTDATA"]["pair_agreement_pass"] or p["DUKASCOPY__HISTDATA"]["pair_agreement_pass"]:
            supported_markets["HISTDATA"]+=1

    eligible=[s for s,n in supported_markets.items() if n>=7]
    gate_pass=bool(eligible and no_consensus<=1)
    result={
        "stage":"EXP-041 third-source feed adjudication v0.1",
        "target_labels_calculated":False,
        "pnl_calculated":False,
        "protected_periods":{"jul_aug_2026_loaded":False,"sep_2026_loaded":False},
        "interval":[str(START),str(END)],
        "sources":{
            "CURRENT_PINNED":"repository-pinned research source",
            "DUKASCOPY":"Dukascopy historical M1",
            "HISTDATA":"HistData.com Generic ASCII M1 bid bars, fixed EST converted to UTC",
        },
        "pairwise_gate":{
            "m1_overlap_ratio":0.70,
            "corr_5m":0.90,
            "corr_1h":0.95,
            "corr_1d":0.95,
            "sign_agreement_1h":0.95,
        },
        "markets":markets,
        "supported_markets_by_source":supported_markets,
        "no_two_source_consensus_markets":int(no_consensus),
        "eligible_consensus_sources":eligible,
        "feed_selection_gate_pass":gate_pass,
        "disposition":"CLEAR_CONSENSUS_FREEZE_ACQUISITION_V02" if gate_pass else "NO_CLEAR_CONSENSUS_REQUIRE_FOURTH_OR_BROKER_SOURCE",
    }
    p=OUT/"EXP-041-third-source-feed-adjudication-v0.1.json"
    p.write_text(json.dumps(result,indent=2,default=str)+"\n")
    print(json.dumps({
        "adjudication":{s:m["adjudication"] for s,m in markets.items()},
        "supported_markets_by_source":supported_markets,
        "eligible_consensus_sources":eligible,
        "feed_selection_gate_pass":gate_pass,
        "disposition":result["disposition"],
        "protected_periods":result["protected_periods"],
    },indent=2))


if __name__=="__main__":
    main()
