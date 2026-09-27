#!/usr/bin/env python3
import json, subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ORIG=ROOT/"research/results/EXP-041-macro-catalyst-information-content-v0.1.json"
GATE=ROOT/"research/results/EXP-041-final-gate-a-audit-v0.1.json"
MACRO=ROOT/"research/data/EXP-041-official-macro-surprise-layer-v0.1.json"
OUT=ROOT/"research/results/EXP-041-gate-b-integrity-corrigendum-v0.1.json"

EXPECTED_BLOB="d5789f32f7c0e239d7efd4e45dc14e205763b5fd"
EXPECTED_TESTED="815de2639e650bfb3d7ee846860a20a8582b8202"
EXPECTED_INELIGIBLE={
 "2025-12-10T19:00:00+00:00",
 "2026-01-28T19:00:00+00:00",
}
START=datetime(2025,7,1,tzinfo=timezone.utc)
END=datetime(2026,6,30,tzinfo=timezone.utc)

def iso(s):
    return datetime.fromisoformat(s.replace("Z","+00:00"))

def blob(path):
    return subprocess.check_output(
        ["git","hash-object",str(path.relative_to(ROOT))],
        cwd=ROOT,text=True
    ).strip()

def eligible(ev):
    lo,hi=ev-timedelta(minutes=60),ev+timedelta(minutes=180)
    day=(lo-timedelta(days=1)).date()
    stop=(hi+timedelta(days=1)).date()
    while day<=stop:
        base=datetime(day.year,day.month,day.day,tzinfo=timezone.utc)
        if base.weekday()<5:
            for minute in range(365,1076,5):
                t=base+timedelta(minutes=minute)
                if START<=t<END and lo<=t<=hi:
                    return True
        day+=timedelta(days=1)
    return False

def main():
    if blob(ORIG)!=EXPECTED_BLOB:
        raise SystemExit("original Gate-B result blob changed")
    x=json.loads(ORIG.read_text())
    ga=json.loads(GATE.read_text())
    macro=json.loads(MACRO.read_text())

    if x["tested_repository_sha"]!=EXPECTED_TESTED:
        raise SystemExit("unexpected original tested SHA")
    if x["disposition"]!="INTEGRITY_FAIL_DO_NOT_INTERPRET":
        raise SystemExit("unexpected original disposition")

    gate_ts=[iso(s) for f in ga["chronological_folds"] for s in f["block_timestamps"]]
    if len(gate_ts)!=65 or len(set(gate_ts))!=65:
        raise SystemExit("expected 65 unique Gate-A timestamps")

    covered={iso(s) for s in x["event_candidate_counts"]}
    elig={t for t in gate_ts if eligible(t)}
    inelig=set(gate_ts)-elig
    inelig_iso={t.isoformat() for t in inelig}

    fams={}
    for r in macro["records"]:
        fams.setdefault(iso(r["official_release_timestamp_utc"]),set()).add(r["family"])

    geometry={
      "gate_a_event_count_65":len(gate_ts)==65,
      "eligible_event_count_63":len(elig)==63,
      "ineligible_event_count_2":len(inelig)==2,
      "ineligible_set_exact":inelig_iso==EXPECTED_INELIGIBLE,
      "ineligible_events_both_fomc":all(fams.get(t)=={"FOMC"} for t in inelig),
      "all_eligible_events_covered":covered==elig,
      "no_ineligible_event_has_candidates":covered.isdisjoint(inelig),
    }

    expected={
      "dukas_archive_sha_verified":True,
      "all_8_market_files_verified":True,
      "macro_surprise_layer_sha_verified":True,
      "final_gate_a_pass":True,
      "frozen_65_events_exact":True,
      "frozen_six_fold_assignments_exact":True,
      "primary_outer_and_inner_both_classes":True,
      "all_markets_both_primary_classes":True,
      "candidate_rows_before_2026_06_30":True,
      "protected_periods_sealed":True,
      "engine_r_or_exp015_outcomes_used":False,
    }
    other={k:x["integrity"].get(k)==v for k,v in expected.items()}
    corrected=all(geometry.values()) and all(other.values())

    timing=bool(x["information_advantage_gates"]["PLUS_CATALYST_TIMING"]["feature_set_pass"])
    surprise=bool(x["information_advantage_gates"]["PLUS_SURPRISE_MAGNITUDE"]["feature_set_pass"])
    if not corrected:
        disposition="INTEGRITY_FAIL_DO_NOT_INTERPRET"
    elif timing:
        disposition="STABLE_MACRO_TIMING_INFORMATION_ADVANTAGE_FOUND"
    elif surprise:
        disposition="STABLE_MACRO_SURPRISE_INFORMATION_ADVANTAGE_FOUND"
    else:
        disposition="NO_STABLE_MACRO_INFORMATION_ADVANTAGE"

    out={
      "experiment":"EXP-041",
      "stage":"gate_b_integrity_corrigendum_v0.1",
      "original_result_blob_sha":blob(ORIG),
      "original_tested_repository_sha":x["tested_repository_sha"],
      "repair_scope":"coverage geometry only; no model or metric rerun",
      "frozen_grid":"weekdays 06:05-17:55 UTC every 5m",
      "frozen_event_window_minutes":[-60,180],
      "gate_a_event_count":len(gate_ts),
      "geometrically_eligible_event_count":len(elig),
      "geometrically_ineligible_events":sorted(inelig_iso),
      "covered_event_count_original_result":len(covered),
      "geometry_gate":geometry,
      "original_other_integrity_checks":other,
      "corrected_integrity_pass":corrected,
      "scientific_metrics_recomputed":False,
      "scientific_thresholds_changed":False,
      "feature_sets_changed":False,
      "folds_changed":False,
      "candidate_grid_changed":False,
      "protected_periods_loaded":False,
      "original_scientific_feature_set_pass":{
        "PLUS_CATALYST_TIMING":timing,
        "PLUS_SURPRISE_MAGNITUDE":surprise
      },
      "recovered_scientific_disposition":disposition,
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({
      "corrected_integrity_pass":corrected,
      "eligible_events":len(elig),
      "ineligible_events":sorted(inelig_iso),
      "timing_pass":timing,
      "surprise_pass":surprise,
      "recovered_scientific_disposition":disposition
    },indent=2))
    return 0 if corrected else 2

if __name__=="__main__":
    raise SystemExit(main())
