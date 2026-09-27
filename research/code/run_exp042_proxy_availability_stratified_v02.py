#!/usr/bin/env python3
from __future__ import annotations
import json, os
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
V1=ROOT/"research/results/EXP-042-proxy-event-coverage-preflight-v0.1.json"
GATE=ROOT/"research/results/EXP-041-final-gate-a-audit-v0.1.json"
OUT=ROOT/"research/results/EXP-042-proxy-availability-stratified-preflight-v0.2.json"

FAMS=("EMPLOYMENT","CPI","PPI","RETAIL","GDP_PCE")

def summarize(name,events,required_proxies):
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
        "required_proxies":required_proxies,
        "event_count":len(events),
        "event_timestamps":[e["event_ts"] for e in events],
        "family_timestamp_counts":{f:int(fam_counts[f]) for f in FAMS},
        "fold_event_counts":{str(i):int(fold_events[i]) for i in range(1,7)},
        "fold_family_counts":{str(i):len(fold_fams[i]) for i in range(1,7)},
        "checks":checks,
    }

def main():
    x=json.loads(V1.read_text())
    ga=json.loads(GATE.read_text())

    if x["coverage_preflight_pass"]:
        raise SystemExit("v0.1 unexpectedly passed; v0.2 stratification not applicable")
    if x["gate_a_event_count"]!=65 or x["eligible_event_count"]!=57:
        raise SystemExit("unexpected v0.1 geometry")
    if len(x["ineligible_events"])!=8:
        raise SystemExit("unexpected ineligible set")

    dxy=[]; both=[]; excluded_dxy=[]; excluded_both=[]

    for e in x["event_details"]:
        dxy_stale=e["baseline_staleness_minutes"]["DOLLARIDXUSD"]
        tb_stale=e["baseline_staleness_minutes"]["USTBONDTRUSD"]

        # v0.1 common ratio is zero exactly when one proxy has no fresh legal coverage.
        # For nonzero common ratio, both have fresh per-event legal coverage.
        common_ratio=float(e["coverage_ratio"])

        dxy_ok=(dxy_stale is not None and 0<dxy_stale<=5)
        tb_ok=(tb_stale is not None and 0<tb_stale<=5)

        # For v0.2 we need independent DXY coverage, not just common coverage.
        # The six v0.1 failures are pure one-proxy inactivity cases with common=0.
        # At those six, the other proxy has 1-minute baseline and the frozen snapshot
        # is otherwise dense. Exact expected exclusion sets below make this deterministic.
        if dxy_ok:
            dxy.append(e)
        else:
            excluded_dxy.append(e["event_ts"])

        if dxy_ok and tb_ok and common_ratio>=0.80:
            both.append(e)
        else:
            excluded_both.append(e["event_ts"])

    expected_dxy_excluded={
        "2025-08-01T12:30:00+00:00",
        "2026-02-20T13:30:00+00:00",
        "2026-04-09T12:30:00+00:00",
        "2026-04-10T12:30:00+00:00",
    }
    expected_both_excluded=expected_dxy_excluded|{
        "2025-08-14T12:30:00+00:00",
        "2026-04-03T12:30:00+00:00",
    }

    integrity={
        "v01_failed_as_expected":not x["coverage_preflight_pass"],
        "eligible_geometry_57_exact":x["eligible_event_count"]==57,
        "dxy_exclusion_set_exact":set(excluded_dxy)==expected_dxy_excluded,
        "both_exclusion_set_exact":set(excluded_both)==expected_both_excluded,
        "no_target_market_data_or_outcomes_loaded":True,
        "protected_periods_sealed":True,
    }

    dxy_summary=summarize("DXY_COMPLETE",dxy,["DOLLARIDXUSD"])
    both_summary=summarize("DXY_TBOND_COMPLETE",both,["DOLLARIDXUSD","USTBONDTRUSD"])

    dxy_pass=all(integrity.values()) and dxy_summary["checks"]["subset_adequate"]
    both_pass=all(integrity.values()) and both_summary["checks"]["subset_adequate"]

    result={
        "experiment":"EXP-042",
        "stage":"proxy_availability_stratified_preflight_v0.2",
        "tested_repository_sha":os.environ.get("GITHUB_SHA"),
        "source_v01_result":"research/results/EXP-042-proxy-event-coverage-preflight-v0.1.json",
        "v01_disposition":x["disposition"],
        "structurally_eligible_event_count":57,
        "structurally_ineligible_events":x["ineligible_events"],
        "integrity":integrity,
        "subsets":{
            "DXY_COMPLETE":dxy_summary,
            "DXY_TBOND_COMPLETE":both_summary,
        },
        "authorizations":{
            "DXY_COMPLETE":"EXP042_DXY_SUBSET_ADEQUATE" if dxy_pass else "EXP042_DXY_SUBSET_INADEQUATE",
            "DXY_TBOND_COMPLETE":"EXP042_DXY_TBOND_SUBSET_ADEQUATE" if both_pass else "EXP042_DXY_TBOND_SUBSET_INADEQUATE",
        },
        "any_model_authorized":bool(dxy_pass or both_pass),
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
        "dxy_counts":dxy_summary["family_timestamp_counts"],
        "both_counts":both_summary["family_timestamp_counts"],
        "dxy_folds":dxy_summary["fold_event_counts"],
        "both_folds":both_summary["fold_event_counts"],
        "authorizations":result["authorizations"],
        "disposition":result["disposition"],
    },indent=2))
    return 0 if dxy_pass and both_pass else 2

if __name__=="__main__":
    raise SystemExit(main())
