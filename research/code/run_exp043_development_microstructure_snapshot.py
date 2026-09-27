#!/usr/bin/env python3
from __future__ import annotations

import csv, hashlib, json, math, os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DATA=Path(os.environ.get("EXP043_OUTDIR","/tmp/exp043-microstructure"))
OUT=ROOT/"research/results"; OUT.mkdir(parents=True,exist_ok=True)
RESULT=OUT/"EXP-043-development-microstructure-snapshot-v0.1.json"

MARKETS=["XAUUSD","EURUSD","GBPUSD","USDJPY","EURJPY","AUDUSD","USDCAD","USDCHF"]
START=date(2025,7,1); END=date(2026,6,30)
TAG="exp043-quote-microstructure-1m-2025-07-01_2026-06-30-v1"
ASSET="exp043-quote-microstructure-1m-2025-07-01_2026-06-30-v1.tar.gz"
HEADER=[
 "minute_start_utc","tick_count","distinct_timestamp_count",
 "median_interarrival_ms","p90_interarrival_ms",
 "spread_bps_median","spread_bps_p90","spread_bps_last","last_quote_age_ms",
 "bid_update_count","ask_update_count","both_price_update_count",
 "bid_volume_median","ask_volume_median",
 "signed_quote_imbalance_mean","signed_quote_imbalance_median",
 "bid_heavy_fraction","ask_heavy_fraction"
]

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def weekdays():
    out=[]; d=START
    while d<END:
        if d.weekday()<5: out.append(d.isoformat())
        d+=timedelta(days=1)
    return out

def fnum(s,allow_blank=False):
    if s=="" and allow_blank:return None
    x=float(s)
    if not math.isfinite(x):raise ValueError("nonfinite")
    return x

def inspect_market(path:Path):
    if not path.exists():
        return {"exists":False,"integrity_pass":False,"error":"missing"}
    rows=0; prev=None; dates=set()
    checks={
      "timestamps_strictly_increasing":True,
      "all_weekdays":True,
      "all_rows_session_05_18":True,
      "tick_count_valid":True,
      "distinct_timestamp_count_valid":True,
      "interarrival_values_valid":True,
      "spread_metrics_nonnegative":True,
      "last_quote_age_valid":True,
      "update_counts_valid":True,
      "quote_volumes_nonnegative":True,
      "imbalance_values_valid":True,
      "heavy_fractions_valid":True,
      "protected_period_absent":True,
    }
    first=last=None

    with path.open("r",encoding="utf-8",newline="") as f:
        r=csv.reader(f); header=next(r,None)
        if header!=HEADER:
            return {"exists":True,"sha256":sha256(path),"integrity_pass":False,"error":f"header {header!r}"}
        for z in r:
            if len(z)!=len(HEADER):
                return {"exists":True,"sha256":sha256(path),"integrity_pass":False,"error":"malformed row"}
            t=datetime.fromisoformat(z[0].replace("Z","+00:00")).astimezone(timezone.utc)
            if first is None:first=t
            last=t; rows+=1; dates.add(t.date().isoformat())
            if prev is not None and not (t>prev): checks["timestamps_strictly_increasing"]=False
            prev=t
            checks["all_weekdays"] &= t.weekday()<5
            minute=t.hour*60+t.minute
            checks["all_rows_session_05_18"] &= (5*60)<=minute<(18*60)
            protected=(date(2026,7,1)<=t.date()<=date(2026,9,30))
            checks["protected_period_absent"] &= not protected

            tick=int(z[1]); distinct=int(z[2])
            checks["tick_count_valid"] &= tick>=1
            checks["distinct_timestamp_count_valid"] &= 1<=distinct<=tick

            med_i=fnum(z[3],True); p90_i=fnum(z[4],True)
            if med_i is not None: checks["interarrival_values_valid"] &= med_i>=0
            if p90_i is not None: checks["interarrival_values_valid"] &= p90_i>=0
            if tick>=3:
                checks["interarrival_values_valid"] &= med_i is not None and p90_i is not None

            sm=fnum(z[5]); sp=fnum(z[6]); sl=fnum(z[7])
            checks["spread_metrics_nonnegative"] &= sm>=0 and sp>=0 and sl>=0

            age=fnum(z[8])
            checks["last_quote_age_valid"] &= 0<=age<=60000

            bu=int(z[9]); au=int(z[10]); both=int(z[11])
            checks["update_counts_valid"] &= all(0<=v<=max(0,tick-1) for v in [bu,au,both])

            bv=fnum(z[12]); av=fnum(z[13])
            checks["quote_volumes_nonnegative"] &= bv>=0 and av>=0

            im=fnum(z[14],True); imed=fnum(z[15],True)
            if im is not None: checks["imbalance_values_valid"] &= -1<=im<=1
            if imed is not None: checks["imbalance_values_valid"] &= -1<=imed<=1

            bhf=fnum(z[16],True); ahf=fnum(z[17],True)
            if bhf is not None: checks["heavy_fractions_valid"] &= 0<=bhf<=1
            if ahf is not None: checks["heavy_fractions_valid"] &= 0<=ahf<=1

    checks["aggregate_rows_ge_120k"]=rows>=120_000
    checks["represented_dates_ge_230"]=len(dates)>=230
    return {
      "exists":True,"sha256":sha256(path),"bytes":path.stat().st_size,
      "rows":rows,"represented_dates":len(dates),
      "first_timestamp":first.isoformat() if first else None,
      "last_timestamp":last.isoformat() if last else None,
      "checks":checks,"integrity_pass":all(checks.values())
    }

def main():
    mp=DATA/"SOURCE-MANIFEST.json"
    if not mp.exists(): raise SystemExit("SOURCE-MANIFEST missing")
    manifest=json.loads(mp.read_text())
    expected=weekdays()

    global_checks={
      "manifest_requested_weekdays_exact":manifest.get("requested_weekdays")==expected,
      "manifest_interval_exact":manifest.get("interval")==["2025-07-01T00:00:00Z","2026-06-30T00:00:00Z"],
      "manifest_session_exact":manifest.get("session_utc")==["05:00:00","18:00:00"],
      "manifest_market_set_exact":set(manifest.get("markets",{}))==set(MARKETS),
    }

    markets={}; overall=True
    for s in MARKETS:
        m=manifest["markets"][s]
        days=m.get("days",[])
        day_dates=[d.get("date") for d in days]
        positive=sum(int(d.get("tick_count",0))>0 for d in days)
        total_ticks=sum(int(d.get("tick_count",0)) for d in days)
        raw_hashes_valid=all(
            isinstance(d.get("raw_canonical_sha256"),str) and len(d["raw_canonical_sha256"])==64
            for d in days
        )
        day_checks={
          "manifest_day_set_exact":day_dates==expected,
          "positive_source_days_ge_230":positive>=230,
          "total_source_ticks_ge_2m":total_ticks>=2_000_000,
          "raw_day_hashes_present":raw_hashes_valid,
          "manifest_tick_sum_matches":total_ticks==int(m.get("total_source_ticks",-1)),
        }
        agg=inspect_market(DATA/f"{s}.csv")
        if agg.get("rows") is not None:
            day_checks["manifest_aggregate_rows_match"]=agg["rows"]==int(m.get("aggregate_rows",-1))
        else:
            day_checks["manifest_aggregate_rows_match"]=False
        ok=all(day_checks.values()) and bool(agg.get("integrity_pass"))
        overall &= ok
        markets[s]={
          "source_positive_days":positive,
          "source_total_ticks":total_ticks,
          "source_day_checks":day_checks,
          "aggregate":agg,
          "market_pass":ok,
        }

    passed=all(global_checks.values()) and overall
    result={
      "experiment":"EXP-043",
      "stage":"development_microstructure_snapshot_v0.1",
      "tested_repository_sha":os.environ.get("GITHUB_SHA"),
      "github_run_id":os.environ.get("GITHUB_RUN_ID"),
      "source_manifest":{
        "path":"SOURCE-MANIFEST.json",
        "sha256":sha256(mp),
        "requested_weekdays":len(expected),
      },
      "global_checks":global_checks,
      "markets":markets,
      "snapshot_integrity_pass":passed,
      "release":{
        "tag":TAG,"archive_asset":ASSET,
        "archive_sha256":None,"created_or_verified_existing":False
      },
      "target_labels_calculated":False,
      "scientific_outcomes_calculated":False,
      "pnl_calculated":False,
      "protected_periods":{"jul_aug_2026_loaded":False,"sep_2026_loaded":False},
      "disposition":(
        "EXP043_DEVELOPMENT_MICROSTRUCTURE_ELIGIBLE_TO_FREEZE"
        if passed else "EXP043_DEVELOPMENT_MICROSTRUCTURE_SNAPSHOT_FAILED"
      )
    }
    RESULT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({
      "pass":passed,
      "requested_weekdays":len(expected),
      "markets":{s:{
          "days":markets[s]["source_positive_days"],
          "ticks":markets[s]["source_total_ticks"],
          "rows":markets[s]["aggregate"].get("rows"),
          "pass":markets[s]["market_pass"]
      } for s in MARKETS},
      "disposition":result["disposition"],
    },indent=2))
    return 0 if passed else 2

if __name__=="__main__":
    raise SystemExit(main())
