#!/usr/bin/env python3
from __future__ import annotations

import hashlib, json, os
from collections import Counter, defaultdict
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
DATA=Path(os.environ.get("EXP042_PROXY_DIR","/tmp/exp042-proxy"))
SNAP=ROOT/"research/results/EXP-042-rates-usd-proxy-repeatability-snapshot-v0.1.json"
GATE=ROOT/"research/results/EXP-041-final-gate-a-audit-v0.1.json"
MACRO=ROOT/"research/data/EXP-041-official-macro-surprise-layer-v0.1.json"
V1=ROOT/"research/results/EXP-042-proxy-event-coverage-preflight-v0.1.json"
OUT=ROOT/"research/results/EXP-042-proxy-availability-stratified-preflight-v0.3.json"

EXPECTED_ARCHIVE="86cef306c36f08a12510c563e307a3158dc45d3236a424251db4d1c1bbaedcb4"
EXPECTED_FILE_SHA={
    "DOLLARIDXUSD":"2f070a99784a60f15e9afe5cb1c906f1ded22aedaa74205cd3a286adefb839d2",
    "USTBONDTRUSD":"e1ff7bea80f40b1529e046a7b0f7b4c6265cc147ee8c6c324ddef05cc7c5acf7",
}
FAMS=("EMPLOYMENT","CPI","PPI","RETAIL","GDP_PCE")

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""):
            h.update(c)
    return h.hexdigest()

def load_proxy(sym:str)->pd.DataFrame:
    p=DATA/f"{sym}.csv"
    if not p.exists():
        raise RuntimeError(f"{sym}: file missing")
    if sha256(p)!=EXPECTED_FILE_SHA[sym]:
        raise RuntimeError(f"{sym}: SHA mismatch")
    x=pd.read_csv(p,usecols=["datetime","close"])
    x["datetime"]=pd.to_datetime(x["datetime"],utc=True)
    x["close"]=pd.to_numeric(x["close"],errors="raise")
    x=x.sort_values("datetime").drop_duplicates("datetime",keep="last").reset_index(drop=True)
    return x

def legal_times(ev:pd.Timestamp)->list[pd.Timestamp]:
    if ev.weekday()>=5:
        return []
    out=[]
    day=ev.normalize()
    for minute in range(6*60+5,17*60+56,5):
        t=day+pd.Timedelta(minutes=minute)
        if ev<=t<=ev+pd.Timedelta(minutes=180):
            out.append(t)
    return out

def strict_asof(x:pd.DataFrame,t:pd.Timestamp):
    i=int(x["datetime"].searchsorted(t,side="left"))-1
    if i<0:
        return None
    ts=x.iloc[i]["datetime"]
    return {
        "ts":ts,
        "close":float(x.iloc[i]["close"]),
        "stale_min":float((t-ts).total_seconds()/60.0)
    }

def proxy_event_availability(x:pd.DataFrame,ev:pd.Timestamp,decision_times:list[pd.Timestamp])->dict:
    b=strict_asof(x,ev)
    baseline_ok=bool(b is not None and 0<b["stale_min"]<=5)
    covered=0
    max_stale=None
    for t in decision_times:
        a=strict_asof(x,t)
        ok=bool(a is not None and 0<a["stale_min"]<=5)
        covered+=int(ok)
        if a is not None:
            max_stale=a["stale_min"] if max_stale is None else max(max_stale,a["stale_min"])
    total=len(decision_times)
    ratio=covered/total if total else 0.0
    passed=baseline_ok and covered>=1 and ratio>=0.80
    return {
        "baseline_staleness_minutes":None if b is None else b["stale_min"],
        "legal_decision_times":total,
        "covered_decision_times":covered,
        "coverage_ratio":ratio,
        "max_observed_staleness_minutes":max_stale,
        "availability_pass":passed,
    }

def subset_summary(name:str,events:list[dict],required:list[str])->dict:
    fam_counts=Counter()
    fold_events=Counter()
    fold_fams=defaultdict(set)
    for e in events:
        fold=int(e["fold"])
        fold_events[fold]+=1
        for fam in e["families"]:
            fam_counts[fam]+=1
            fold_fams[fold].add(fam)
    checks={
        "events_ge_40":len(events)>=40,
        "numeric_families_ge_8":all(fam_counts[f]>=8 for f in FAMS),
        "all_6_folds_ge_4_events":all(fold_events[i]>=4 for i in range(1,7)),
        "all_6_folds_ge_2_families":all(len(fold_fams[i])>=2 for i in range(1,7)),
    }
    checks["subset_adequate"]=all(checks.values())
    return {
        "name":name,
        "required_proxies":required,
        "event_count":len(events),
        "event_timestamps":[e["event_ts"] for e in events],
        "family_timestamp_counts":{f:int(fam_counts[f]) for f in FAMS},
        "fold_event_counts":{str(i):int(fold_events[i]) for i in range(1,7)},
        "fold_family_counts":{str(i):int(len(fold_fams[i])) for i in range(1,7)},
        "checks":checks,
    }

def main()->int:
    snap=json.loads(SNAP.read_text())
    gate=json.loads(GATE.read_text())
    macro=json.loads(MACRO.read_text())
    v1=json.loads(V1.read_text())

    if not snap["repeatability_gate_pass"] or not snap["release"]["created_or_verified_existing"]:
        raise SystemExit("proxy snapshot not frozen")
    if snap["release"]["archive_sha256"]!=EXPECTED_ARCHIVE:
        raise SystemExit("proxy archive SHA mismatch")
    if v1["coverage_preflight_pass"]:
        raise SystemExit("v0.1 unexpectedly passed")

    data={s:load_proxy(s) for s in EXPECTED_FILE_SHA}

    fam_by_ts=defaultdict(set)
    for r in macro["records"]:
        fam_by_ts[pd.Timestamp(r["official_release_timestamp_utc"])].add(r["family"])

    all_events=[]
    for f in gate["chronological_folds"]:
        for s in f["block_timestamps"]:
            t=pd.Timestamp(s)
            all_events.append({"ts":t,"fold":int(f["fold"]),"families":sorted(fam_by_ts[t])})

    if len(all_events)!=65 or len({e["ts"] for e in all_events})!=65:
        raise SystemExit("Gate-A event set mismatch")

    structural_eligible=[]
    structural_ineligible=[]
    for e in all_events:
        times=legal_times(e["ts"])
        q={**e,"decision_times":times}
        (structural_eligible if times else structural_ineligible).append(q)

    if len(structural_eligible)!=57 or len(structural_ineligible)!=8:
        raise SystemExit("unexpected post-release geometry")

    if {e["ts"].isoformat() for e in structural_ineligible}!=set(v1["ineligible_events"]):
        raise SystemExit("structural ineligible set differs from v0.1")

    details=[]
    dxy_complete=[]
    both_complete=[]

    for e in structural_eligible:
        per={}
        for sym in EXPECTED_FILE_SHA:
            per[sym]=proxy_event_availability(data[sym],e["ts"],e["decision_times"])
        dxy_ok=per["DOLLARIDXUSD"]["availability_pass"]
        both_ok=dxy_ok and per["USTBONDTRUSD"]["availability_pass"]
        row={
            "event_ts":e["ts"].isoformat(),
            "fold":e["fold"],
            "families":e["families"],
            "proxy_availability":per,
            "DXY_COMPLETE":bool(dxy_ok),
            "DXY_TBOND_COMPLETE":bool(both_ok),
        }
        details.append(row)
        if dxy_ok:
            dxy_complete.append(row)
        if both_ok:
            both_complete.append(row)

    dxy_summary=subset_summary("DXY_COMPLETE",dxy_complete,["DOLLARIDXUSD"])
    both_summary=subset_summary("DXY_TBOND_COMPLETE",both_complete,["DOLLARIDXUSD","USTBONDTRUSD"])

    integrity={
        "snapshot_archive_sha_exact":snap["release"]["archive_sha256"]==EXPECTED_ARCHIVE,
        "proxy_file_shas_exact":all(snap["instruments"][s]["copy_a"]["sha256"]==EXPECTED_FILE_SHA[s] for s in EXPECTED_FILE_SHA),
        "gate_a_events_65_exact":len(all_events)==65,
        "structurally_eligible_57_exact":len(structural_eligible)==57,
        "structurally_ineligible_8_exact":len(structural_ineligible)==8,
        "v01_ineligible_geometry_reproduced":{e["ts"].isoformat() for e in structural_ineligible}==set(v1["ineligible_events"]),
        "all_structurally_ineligible_are_fomc":all(e["families"]==["FOMC"] for e in structural_ineligible),
        "no_target_market_data_or_outcomes_loaded":True,
        "protected_periods_sealed":True,
    }

    dxy_pass=all(integrity.values()) and dxy_summary["checks"]["subset_adequate"]
    both_pass=all(integrity.values()) and both_summary["checks"]["subset_adequate"]

    result={
        "experiment":"EXP-042",
        "stage":"proxy_availability_stratified_preflight_v0.3",
        "tested_repository_sha":os.environ.get("GITHUB_SHA"),
        "supersedes_unexecuted_v02":True,
        "proxy_snapshot_tag":snap["release"]["tag"],
        "proxy_archive_sha256":snap["release"]["archive_sha256"],
        "structurally_eligible_event_count":57,
        "structurally_ineligible_events":[e["ts"].isoformat() for e in structural_ineligible],
        "event_details":details,
        "subsets":{
            "DXY_COMPLETE":dxy_summary,
            "DXY_TBOND_COMPLETE":both_summary,
        },
        "integrity":integrity,
        "authorizations":{
            "DXY_COMPLETE":"EXP042_DXY_SUBSET_ADEQUATE" if dxy_pass else "EXP042_DXY_SUBSET_INADEQUATE",
            "DXY_TBOND_COMPLETE":"EXP042_DXY_TBOND_SUBSET_ADEQUATE" if both_pass else "EXP042_DXY_TBOND_SUBSET_INADEQUATE",
        },
        "target_market_data_loaded":False,
        "target_labels_calculated":False,
        "pnl_calculated":False,
        "protected_periods":{"jul_aug_2026_loaded":False,"sep_2026_loaded":False},
        "disposition":(
            "EXP042_AVAILABILITY_SUBSETS_FROZEN_AUTHORIZE_NESTED_STUDIES"
            if dxy_pass and both_pass else
            "EXP042_AVAILABILITY_SUBSETS_PARTIAL_OR_INADEQUATE"
        ),
    }
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({
        "dxy_events":dxy_summary["event_count"],
        "both_events":both_summary["event_count"],
        "dxy_family_counts":dxy_summary["family_timestamp_counts"],
        "both_family_counts":both_summary["family_timestamp_counts"],
        "dxy_fold_counts":dxy_summary["fold_event_counts"],
        "both_fold_counts":both_summary["fold_event_counts"],
        "authorizations":result["authorizations"],
        "disposition":result["disposition"],
    },indent=2))
    return 0 if dxy_pass and both_pass else 2

if __name__=="__main__":
    raise SystemExit(main())
