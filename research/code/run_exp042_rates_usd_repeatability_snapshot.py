#!/usr/bin/env python3
"""EXP-042 DXY / US T-Bond same-run repeatability + snapshot manifest."""

from __future__ import annotations
import csv, hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
A=Path(os.environ.get("EXP042_DATA_A","/tmp/exp042-rates-usd-a"))
B=Path(os.environ.get("EXP042_DATA_B","/tmp/exp042-rates-usd-b"))
OUT=ROOT/"research/results"; OUT.mkdir(parents=True,exist_ok=True)

SYMBOLS=["DOLLARIDXUSD","USTBONDTRUSD"]
HEADER=["datetime","open","high","low","close","volume"]
START=datetime(2025,7,1,tzinfo=timezone.utc)
END=datetime(2026,6,30,tzinfo=timezone.utc)
FIRST_MAX=datetime(2025,7,2,23,59,tzinfo=timezone.utc)
LAST_MIN=datetime(2026,6,29,18,0,tzinfo=timezone.utc)
TAG="exp042-rates-usd-proxy-m1-2025-07-01_2026-06-30-v1"
ASSET="exp042-rates-usd-proxy-m1-2025-07-01_2026-06-30-v1.tar.gz"

def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def ts(s):
    return datetime.fromisoformat(s.replace("Z","+00:00")).astimezone(timezone.utc)

def inspect(path):
    if not path.exists(): return {"exists":False,"integrity_pass":False,"error":"missing"}
    rows=0; dates=set(); first=last=prev=None; dup=0
    mono=True; inside=True; positive=True; geom=True
    with path.open("r",encoding="utf-8",newline="") as f:
        r=csv.reader(f); header=next(r,None)
        if header!=HEADER:
            return {"exists":True,"sha256":sha(path),"integrity_pass":False,"error":f"header {header!r}"}
        for line in r:
            if len(line)!=6:
                return {"exists":True,"sha256":sha(path),"integrity_pass":False,"error":"malformed row"}
            t=ts(line[0]); o,h,l,c,v=map(float,line[1:])
            rows+=1; dates.add(t.date())
            if first is None:first=t
            last=t
            if prev is not None:
                if t==prev:dup+=1
                if t<=prev:mono=False
            prev=t
            inside &= START<=t<END
            positive &= o>0 and h>0 and l>0 and c>0
            geom &= h>=max(o,c,l) and l<=min(o,c,h)
    checks={
      "rows_gt_100k":rows>100_000,
      "distinct_dates_ge_220":len(dates)>=220,
      "first_by_july2":first is not None and first<=FIRST_MAX,
      "last_at_least_jun29_18utc":last is not None and last>=LAST_MIN,
      "inside_interval":inside,
      "strictly_increasing_no_duplicates":mono and dup==0,
      "positive_prices":positive,
      "valid_ohlc_geometry":geom,
    }
    return {
      "exists":True,"sha256":sha(path),"bytes":path.stat().st_size,
      "rows":rows,"distinct_utc_dates":len(dates),
      "first_timestamp":first.isoformat() if first else None,
      "last_timestamp":last.isoformat() if last else None,
      "duplicate_count":dup,"checks":checks,"integrity_pass":all(checks.values())
    }

def main():
    instruments={}; passed=True
    for s in SYMBOLS:
        a=inspect(A/f"{s}.csv"); b=inspect(B/f"{s}.csv")
        same_sha=a.get("sha256")==b.get("sha256") and a.get("sha256") is not None
        same_rows=a.get("rows")==b.get("rows") and a.get("rows") is not None
        ok=bool(a.get("integrity_pass") and b.get("integrity_pass") and same_sha and same_rows)
        passed &= ok
        instruments[s]={
          "copy_a":a,"copy_b":b,"same_sha256":same_sha,
          "same_rows":same_rows,"repeatability_pass":ok
        }

    manifest={
      "snapshot_id":"EXP-042 rates/USD interpretation proxy snapshot v1",
      "release_tag":TAG,
      "source":{
        "authority":"Dukascopy Bank historical data",
        "transport_helper":"dukascopy-node",
        "transport_version":"1.50.0",
        "download_interval":["2025-07-01T00:00:00Z","2026-06-30T00:00:00Z"],
        "timeframe":"m1",
        "instrument_ids":{"DOLLARIDXUSD":"dollaridxusd","USTBONDTRUSD":"ustbondtrusd"},
        "scientific_role":{
          "DOLLARIDXUSD":"USD-index price-reaction proxy",
          "USTBONDTRUSD":"long-duration US Treasury price-reaction proxy"
        },
        "volume_authorized_as_true_centralized_volume":False,
      },
      "instruments":{
        s:{
          "file":f"{s}.csv",
          "sha256":instruments[s]["copy_a"].get("sha256"),
          "rows":instruments[s]["copy_a"].get("rows"),
          "bytes":instruments[s]["copy_a"].get("bytes"),
          "first_timestamp":instruments[s]["copy_a"].get("first_timestamp"),
          "last_timestamp":instruments[s]["copy_a"].get("last_timestamp"),
        } for s in SYMBOLS
      },
      "repeatability_gate_pass":passed,
      "protected_periods":{"jul_aug_2026_loaded":False,"sep_2026_loaded":False},
    }
    (A/"SNAPSHOT-MANIFEST.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")

    result={
      "experiment":"EXP-042",
      "stage":"rates_usd_proxy_repeatability_snapshot_v0.1",
      "tested_repository_sha":os.environ.get("GITHUB_SHA"),
      "github_run_id":os.environ.get("GITHUB_RUN_ID"),
      "source":manifest["source"],
      "instruments":instruments,
      "repeatability_gate_pass":passed,
      "release":{"tag":TAG,"archive_asset":ASSET,"archive_sha256":None,"created_or_verified_existing":False},
      "scientific_outcomes_calculated":False,
      "target_labels_calculated":False,
      "pnl_calculated":False,
      "protected_periods":{"jul_aug_2026_loaded":False,"sep_2026_loaded":False},
      "disposition":(
        "EXP042_RATES_USD_PROXY_REPEATABLE_ELIGIBLE_TO_FREEZE_SNAPSHOT"
        if passed else
        "EXP042_RATES_USD_PROXY_DATA_NOT_REPEATABLE_FIX_OR_CHANGE_SOURCE"
      )
    }
    p=OUT/"EXP-042-rates-usd-proxy-repeatability-snapshot-v0.1.json"
    p.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({
      "repeatability_gate_pass":passed,
      "instrument_pass":{s:instruments[s]["repeatability_pass"] for s in SYMBOLS},
      "rows_a":{s:instruments[s]["copy_a"].get("rows") for s in SYMBOLS},
      "rows_b":{s:instruments[s]["copy_b"].get("rows") for s in SYMBOLS},
      "disposition":result["disposition"],
    },indent=2))

if __name__=="__main__":
    main()
