#!/usr/bin/env python3
from __future__ import annotations

import csv, hashlib, json, math, os, statistics
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT=Path(__file__).resolve().parents[2]
A=Path(os.environ.get("EXP043_TICK_A","/tmp/exp043-ticks-a"))
B=Path(os.environ.get("EXP043_TICK_B","/tmp/exp043-ticks-b"))
OUT=ROOT/"research/results"
OUT.mkdir(parents=True,exist_ok=True)

MARKETS=["XAUUSD","EURUSD","GBPUSD","USDJPY","EURJPY","AUDUSD","USDCAD","USDCHF"]
DATES=["2025-07-09","2025-09-10","2025-11-12","2026-01-14","2026-03-11","2026-05-13"]
HEADER=["timestamp_ms","ask_price","bid_price","ask_volume","bid_volume"]

def sha(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def pct(vals,p):
    if not vals:return None
    x=sorted(vals)
    if len(x)==1:return float(x[0])
    k=(len(x)-1)*p
    lo=int(math.floor(k)); hi=int(math.ceil(k))
    if lo==hi:return float(x[lo])
    return float(x[lo]*(hi-k)+x[hi]*(k-lo))

def inspect(path:Path,date_str:str):
    if not path.exists():
        return {"exists":False,"integrity_pass":False,"error":"missing"}
    start=int(datetime.fromisoformat(date_str+"T00:00:00+00:00").timestamp()*1000)
    end=start+24*60*60*1000
    rows=0; prev=None; nondec=True; inside=True
    prices_ok=True; spread_ok=True; vols_ok=True
    pos_av=False;pos_bv=False
    timestamps=set(); spreads=[]; intervals=[]; avs=[]; bvs=[]; imbs=[]
    first=last=None
    with path.open("r",encoding="utf-8",newline="") as f:
        r=csv.reader(f)
        header=next(r,None)
        if header!=HEADER:
            return {"exists":True,"sha256":sha(path),"integrity_pass":False,"error":f"header {header!r}"}
        for line in r:
            if len(line)!=5:
                return {"exists":True,"sha256":sha(path),"integrity_pass":False,"error":"malformed row"}
            ts=int(line[0]); ask=float(line[1]); bid=float(line[2]); av=float(line[3]); bv=float(line[4])
            if not all(math.isfinite(v) for v in [ask,bid,av,bv]):
                return {"exists":True,"sha256":sha(path),"integrity_pass":False,"error":"nonfinite"}
            rows+=1; timestamps.add(ts)
            if first is None:first=ts
            last=ts
            if prev is not None:
                if ts<prev: nondec=False
                intervals.append(ts-prev)
            prev=ts
            inside &= start<=ts<end
            prices_ok &= ask>0 and bid>0
            spread=ask-bid
            spread_ok &= spread>=0
            vols_ok &= av>=0 and bv>=0
            pos_av |= av>0; pos_bv |= bv>0
            spreads.append(spread); avs.append(av); bvs.append(bv)
            den=av+bv
            if den>0: imbs.append(abs(av-bv)/den)

    pos_spread_obs=sum(s>0 for s in spreads)
    distinct_pos_spreads=len({s for s in spreads if s>0})
    checks={
        "ticks_ge_500":rows>=500,
        "timestamps_nondecreasing":nondec,
        "inside_requested_day":inside,
        "positive_prices":prices_ok,
        "ask_ge_bid_every_row":spread_ok,
        "volumes_nonnegative":vols_ok,
        "positive_ask_volume_exists":pos_av,
        "positive_bid_volume_exists":pos_bv,
        "distinct_millisecond_timestamps_ge_50":len(timestamps)>=50,
        "spread_variation_or_positive_observations":distinct_pos_spreads>=10 or pos_spread_obs>=10,
    }
    return {
        "exists":True,
        "sha256":sha(path),
        "bytes":path.stat().st_size,
        "rows":rows,
        "distinct_timestamps":len(timestamps),
        "first_timestamp_ms":first,
        "last_timestamp_ms":last,
        "checks":checks,
        "integrity_pass":all(checks.values()),
        "diagnostics":{
            "median_tick_interval_ms":statistics.median(intervals) if intervals else None,
            "median_spread":statistics.median(spreads) if spreads else None,
            "p95_spread":pct(spreads,0.95),
            "zero_spread_fraction":(sum(s==0 for s in spreads)/len(spreads)) if spreads else None,
            "median_ask_volume":statistics.median(avs) if avs else None,
            "median_bid_volume":statistics.median(bvs) if bvs else None,
            "median_abs_quote_side_imbalance":statistics.median(imbs) if imbs else None,
            "distinct_positive_spreads":distinct_pos_spreads,
            "positive_spread_observations":pos_spread_obs,
        }
    }

def main():
    pairs={}
    passed=True
    for sym in MARKETS:
        pairs[sym]={}
        for d in DATES:
            a=inspect(A/sym/f"{d}.csv",d)
            b=inspect(B/sym/f"{d}.csv",d)
            same_sha=a.get("sha256") is not None and a.get("sha256")==b.get("sha256")
            same_rows=a.get("rows") is not None and a.get("rows")==b.get("rows")
            ok=bool(a.get("integrity_pass") and b.get("integrity_pass") and same_sha and same_rows)
            passed &= ok
            pairs[sym][d]={
                "copy_a":a,"copy_b":b,
                "same_sha256":same_sha,
                "same_rows":same_rows,
                "repeatability_pass":ok,
            }

    result={
        "experiment":"EXP-043",
        "stage":"dukascopy_tick_microstructure_source_preflight_v0.1",
        "tested_repository_sha":os.environ.get("GITHUB_SHA"),
        "github_run_id":os.environ.get("GITHUB_RUN_ID"),
        "transport":{"package":"dukascopy-node","version":"1.50.0","timeframe":"tick"},
        "markets":MARKETS,
        "pilot_dates":DATES,
        "pair_count":len(MARKETS)*len(DATES),
        "pairs":pairs,
        "repeatability_gate_pass":passed,
        "target_labels_calculated":False,
        "pnl_calculated":False,
        "scientific_outcomes_calculated":False,
        "protected_periods":{"jul_aug_2026_loaded":False,"sep_2026_loaded":False},
        "disposition":(
            "EXP043_DUKASCOPY_TICK_MICROSTRUCTURE_SOURCE_REPEATABLE"
            if passed else
            "EXP043_DUKASCOPY_TICK_MICROSTRUCTURE_SOURCE_NOT_REPEATABLE"
        ),
    }
    p=OUT/"EXP-043-dukascopy-tick-microstructure-source-preflight-v0.1.json"
    p.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({
        "pass":passed,
        "pairs":48,
        "market_pass":{
            s:all(pairs[s][d]["repeatability_pass"] for d in DATES)
            for s in MARKETS
        },
        "disposition":result["disposition"],
    },indent=2))
    return 0 if passed else 2

if __name__=="__main__":
    raise SystemExit(main())
