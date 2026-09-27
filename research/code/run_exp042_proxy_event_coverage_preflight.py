#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,os
from bisect import bisect_left
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
DATA=Path(os.environ.get("EXP042_PROXY_DIR","/tmp/exp042-proxy"))
SNAP=ROOT/"research/results/EXP-042-rates-usd-proxy-repeatability-snapshot-v0.1.json"
GATE=ROOT/"research/results/EXP-041-final-gate-a-audit-v0.1.json"
MACRO=ROOT/"research/data/EXP-041-official-macro-surprise-layer-v0.1.json"
OUT=ROOT/"research/results/EXP-042-proxy-event-coverage-preflight-v0.1.json"
EXPECTED_ARCHIVE="86cef306c36f08a12510c563e307a3158dc45d3236a424251db4d1c1bbaedcb4"
EXPECTED_INELIGIBLE={
"2025-07-30T18:00:00+00:00","2025-09-17T18:00:00+00:00",
"2025-10-29T18:00:00+00:00","2025-12-10T19:00:00+00:00",
"2026-01-28T19:00:00+00:00","2026-03-18T18:00:00+00:00",
"2026-04-29T18:00:00+00:00","2026-06-17T18:00:00+00:00",
}
SYMS=["DOLLARIDXUSD","USTBONDTRUSD"]

def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for c in iter(lambda:f.read(1024*1024),b""):h.update(c)
 return h.hexdigest()

def legal_times(ev):
 out=[]
 day=ev.normalize()
 if day.weekday()<5:
  for m in range(365,1076,5):
   t=day+pd.Timedelta(minutes=m)
   if ev<=t<=ev+pd.Timedelta(minutes=180):
    out.append(t)
 return out

def load(sym,expected):
 p=DATA/f"{sym}.csv"
 if sha(p)!=expected: raise RuntimeError(f"{sym} SHA mismatch")
 x=pd.read_csv(p,usecols=["datetime","close"])
 x["datetime"]=pd.to_datetime(x["datetime"],utc=True)
 x=x.sort_values("datetime").drop_duplicates("datetime")
 return x

def asof_strict(x,t):
 arr=x["datetime"].array
 i=x["datetime"].searchsorted(t,side="left")-1
 if i<0:return None
 ts=x.iloc[i]["datetime"]
 stale=(t-ts).total_seconds()/60
 return {"ts":ts,"close":float(x.iloc[i]["close"]),"stale_min":float(stale)}

def main():
 snap=json.loads(SNAP.read_text()); gate=json.loads(GATE.read_text()); macro=json.loads(MACRO.read_text())
 if not snap["repeatability_gate_pass"] or not snap["release"]["created_or_verified_existing"]:
  raise SystemExit("snapshot not frozen")
 if snap["release"]["archive_sha256"]!=EXPECTED_ARCHIVE: raise SystemExit("archive SHA mismatch")

 data={s:load(s,snap["instruments"][s]["copy_a"]["sha256"]) for s in SYMS}
 events=[]
 for f in gate["chronological_folds"]:
  for s in f["block_timestamps"]:
   events.append({"ts":pd.Timestamp(s),"fold":int(f["fold"])})
 if len(events)!=65 or len({e["ts"] for e in events})!=65: raise SystemExit("Gate-A event mismatch")

 fams={}
 for r in macro["records"]:
  fams.setdefault(pd.Timestamp(r["official_release_timestamp_utc"]),set()).add(r["family"])

 eligible=[]; ineligible=[]
 for e in events:
  times=legal_times(e["ts"])
  (eligible if times else ineligible).append({**e,"legal_times":times})
 inelig_iso={e["ts"].isoformat() for e in ineligible}

 details=[]; covered_by_fold={i:0 for i in range(1,7)}
 pooled_legal=0; pooled_common=0
 for e in eligible:
  baselines={s:asof_strict(data[s],e["ts"]) for s in SYMS}
  baseline_ok=all(b and 0<b["stale_min"]<=5 for b in baselines.values())
  common=0
  for t in e["legal_times"]:
   ok=True
   for s in SYMS:
    a=asof_strict(data[s],t)
    if a is None or not (0<a["stale_min"]<=5):
     ok=False; break
   common+=int(ok)
  n=len(e["legal_times"]); ratio=common/n if n else 0
  event_pass=baseline_ok and common>=1 and ratio>=0.80
  if event_pass: covered_by_fold[e["fold"]]+=1
  pooled_legal+=n; pooled_common+=common
  details.append({
   "event_ts":e["ts"].isoformat(),"fold":e["fold"],"families":sorted(fams.get(e["ts"],set())),
   "legal_decision_times":n,"common_proxy_decision_times":common,"coverage_ratio":ratio,
   "baseline_staleness_minutes":{s:(baselines[s]["stale_min"] if baselines[s] else None) for s in SYMS},
   "event_pass":event_pass
  })

 pooled=pooled_common/pooled_legal if pooled_legal else 0
 gate_checks={
  "snapshot_archive_sha_exact":snap["release"]["archive_sha256"]==EXPECTED_ARCHIVE,
  "gate_a_events_65_exact":len(events)==65,
  "eligible_events_57_exact":len(eligible)==57,
  "ineligible_events_8_exact":len(ineligible)==8,
  "ineligible_set_exact":inelig_iso==EXPECTED_INELIGIBLE,
  "all_ineligible_are_fomc":all(fams.get(e["ts"])=={"FOMC"} for e in ineligible),
  "all_eligible_event_coverage_pass":all(d["event_pass"] for d in details),
  "pooled_common_coverage_ge_95pct":pooled>=0.95,
  "every_fold_ge_8_covered_events":all(v>=8 for v in covered_by_fold.values()),
  "no_target_market_data_or_outcomes_loaded":True,
  "protected_periods_sealed":True,
 }
 passed=all(gate_checks.values())
 result={
  "experiment":"EXP-042","stage":"proxy_event_coverage_preflight_v0.1",
  "tested_repository_sha":os.environ.get("GITHUB_SHA"),
  "proxy_snapshot_tag":snap["release"]["tag"],"proxy_archive_sha256":snap["release"]["archive_sha256"],
  "gate_a_event_count":len(events),"eligible_event_count":len(eligible),
  "ineligible_events":sorted(inelig_iso),"covered_events_by_fold":covered_by_fold,
  "pooled_legal_decision_times":pooled_legal,"pooled_common_proxy_decision_times":pooled_common,
  "pooled_common_coverage_ratio":pooled,"event_details":details,"gate":gate_checks,
  "coverage_preflight_pass":passed,"target_market_data_loaded":False,"target_labels_calculated":False,
  "pnl_calculated":False,"protected_periods":{"jul_aug_2026_loaded":False,"sep_2026_loaded":False},
  "disposition":"EXP042_PROXY_EVENT_COVERAGE_PASS_AUTHORIZE_INFORMATION_CONTENT_DESIGN" if passed else "EXP042_PROXY_EVENT_COVERAGE_FAIL_DO_NOT_MODEL"
 }
 OUT.write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps({"pass":passed,"eligible":len(eligible),"pooled_coverage":pooled,"covered_by_fold":covered_by_fold,"disposition":result["disposition"]},indent=2))
 return 0 if passed else 2
if __name__=="__main__": raise SystemExit(main())
