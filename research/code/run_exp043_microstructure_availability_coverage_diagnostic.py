#!/usr/bin/env python3
from __future__ import annotations

import hashlib, json, os
from collections import defaultdict
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
DATA=Path(os.environ.get("EXP043_MICRO_DIR","/tmp/exp043-microstructure"))
AUDIT=ROOT/"research/results/EXP-043-development-microstructure-snapshot-v0.1.json"
OUT=ROOT/"research/results/EXP-043-microstructure-availability-coverage-diagnostic-v0.1.json"

EXPECTED_ARCHIVE="f95edf1f7762271941a1d24b3204c4640485d9e7b9b01440fbef86f521f52ca5"
MARKETS=["XAUUSD","EURUSD","GBPUSD","USDJPY","EURJPY","AUDUSD","USDCAD","USDCHF"]
START=pd.Timestamp("2026-03-23T00:00:00Z")
END=pd.Timestamp("2026-06-30T00:00:00Z")

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()

def decision_grid():
    out=[]
    for day in pd.date_range(START.normalize(),(END-pd.Timedelta(days=1)).normalize(),freq="D",tz="UTC"):
        if day.weekday()>=5: continue
        out.extend(pd.date_range(day+pd.Timedelta(hours=6,minutes=5),
                                 day+pd.Timedelta(hours=17,minutes=55),
                                 freq="5min",tz="UTC").tolist())
    return out

def longest_false_streak(flags):
    best=cur=0
    for x in flags:
        if x: cur=0
        else:
            cur+=1
            best=max(best,cur)
    return best

def main():
    audit=json.loads(AUDIT.read_text())
    if not audit["snapshot_integrity_pass"] or not audit["release"]["created_or_verified_existing"]:
        raise SystemExit("micro snapshot not frozen")
    if audit["release"]["archive_sha256"]!=EXPECTED_ARCHIVE:
        raise SystemExit("archive SHA mismatch")

    grid=decision_grid()
    results={}

    for s in MARKETS:
        p=DATA/f"{s}.csv"
        expected=audit["markets"][s]["aggregate"]["sha256"]
        if sha256(p)!=expected:
            raise SystemExit(f"{s}: aggregate SHA mismatch")
        x=pd.read_csv(p,usecols=["minute_start_utc"])
        x["minute_start_utc"]=pd.to_datetime(x["minute_start_utc"],utc=True)
        observed=set(x.loc[(x["minute_start_utc"]>=START-pd.Timedelta(minutes=60))&
                           (x["minute_start_utc"]<END),"minute_start_utc"])

        eligible=[]
        by_hour=defaultdict(lambda:[0,0])
        by_date=defaultdict(lambda:[0,0])
        ineligible_ts=[]

        for t in grid:
            c5=sum((t-pd.Timedelta(minutes=i)) in observed for i in range(1,6))
            c30=sum((t-pd.Timedelta(minutes=i)) in observed for i in range(1,31))
            c60=sum((t-pd.Timedelta(minutes=i)) in observed for i in range(1,61))
            ok=(c5>=4 and c30>=24 and c60>=48)
            eligible.append(ok)
            by_hour[str(t.hour)][0]+=int(ok); by_hour[str(t.hour)][1]+=1
            by_date[t.date().isoformat()][0]+=int(ok); by_date[t.date().isoformat()][1]+=1
            if not ok: ineligible_ts.append(t.isoformat())

        coverage=sum(eligible)/len(eligible)
        date_ratios={d:a/b for d,(a,b) in by_date.items()}
        hour_ratios={h:{"eligible":a,"total":b,"coverage_ratio":a/b} for h,(a,b) in sorted(by_hour.items(),key=lambda z:int(z[0]))}

        results[s]={
            "theoretical_decision_times":len(grid),
            "source_eligible_decision_times":int(sum(eligible)),
            "source_only_coverage_ratio":coverage,
            "coverage_ge_90pct":coverage>=0.90,
            "coverage_by_utc_hour":hour_ratios,
            "dates_lt_90pct":sum(v<0.90 for v in date_ratios.values()),
            "dates_lt_75pct":sum(v<0.75 for v in date_ratios.values()),
            "dates_lt_50pct":sum(v<0.50 for v in date_ratios.values()),
            "coverage_by_date":date_ratios,
            "longest_consecutive_ineligible_decisions":longest_false_streak(eligible),
            "first_ineligible_decision":ineligible_ts[0] if ineligible_ts else None,
            "last_ineligible_decision":ineligible_ts[-1] if ineligible_ts else None,
        }

    low={s for s in MARKETS if results[s]["source_only_coverage_ratio"]<0.90}
    if low=={"AUDUSD","USDCHF"}:
        disp="SOURCE_AVAILABILITY_EXPLAINS_EXP043_COVERAGE_FAILURE"
    elif low & {"AUDUSD","USDCHF"}:
        disp="SOURCE_AVAILABILITY_PARTIALLY_EXPLAINS_EXP043_COVERAGE_FAILURE"
    else:
        disp="SOURCE_AVAILABILITY_DOES_NOT_EXPLAIN_EXP043_COVERAGE_FAILURE"

    out={
        "experiment":"EXP-043",
        "stage":"microstructure_availability_coverage_diagnostic_v0.1",
        "tested_repository_sha":os.environ.get("GITHUB_SHA"),
        "micro_archive_sha256":audit["release"]["archive_sha256"],
        "decision_interval":["2026-03-23T00:00:00Z","2026-06-30T00:00:00Z"],
        "decision_grid":"weekdays 06:05-17:55 UTC every 5 minutes",
        "availability_rule":{"recent_5m_min_rows":4,"medium_30m_min_rows":24,"baseline_60m_min_rows":48},
        "markets":results,
        "markets_below_90pct":sorted(low),
        "target_market_ohlc_loaded":False,
        "target_labels_loaded":False,
        "model_predictions_loaded":False,
        "pnl_loaded":False,
        "protected_periods":{"jul_aug_2026_loaded":False,"sep_2026_loaded":False},
        "exp043_v01_reinterpreted":False,
        "disposition":disp,
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({
        "coverage":{s:results[s]["source_only_coverage_ratio"] for s in MARKETS},
        "markets_below_90pct":sorted(low),
        "disposition":disp
    },indent=2))

if __name__=="__main__":
    main()
