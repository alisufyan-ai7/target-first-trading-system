#!/usr/bin/env python3
"""EXP-041 final Gate-A adequacy/provenance audit v0.1.

Zero market outcomes. Freezes six chronological independent-event folds.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

DUKA=ROOT/"research/results/EXP-041-dukas-repeatability-snapshot-recovery-v0.1.json"
CONS=ROOT/"research/data/EXP-041-free-macro-consensus-v0.3.json"
CONS_AUDIT=ROOT/"research/results/EXP-041-free-macro-consensus-scope-audit-v0.3.json"
ACTUAL=ROOT/"research/data/EXP-041-official-macro-surprise-layer-v0.1.json"
ACTUAL_AUDIT=ROOT/"research/results/EXP-041-official-actual-reconciliation-v0.1.json"

OUT=ROOT/"research/results/EXP-041-final-gate-a-audit-v0.1.json"

EXPECTED_DUKA_TAG="exp041-data-dukas-m1-2025-07-01_2026-06-30-v2"
EXPECTED_DUKA_SHA="90bc7301e459062e8e35cd89a1a9aac23332ca3472014dd2cc5045ba34794272"
EXPECTED_INTERVAL=["2025-07-01T00:00:00Z","2026-06-30T00:00:00Z"]

NUMERIC_FAMILIES=["EMPLOYMENT","CPI","PPI","RETAIL","GDP_PCE"]


def sha256_file(p:Path)->str:
    h=hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda:fh.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()


def split_six(items:list[dict])->list[list[dict]]:
    n=len(items)
    base=n//6
    rem=n%6
    out=[]
    i=0
    for k in range(6):
        size=base+(1 if k<rem else 0)
        out.append(items[i:i+size])
        i+=size
    assert i==n
    return out


def main()->int:
    duka=json.loads(DUKA.read_text())
    cons=json.loads(CONS.read_text())
    cons_audit=json.loads(CONS_AUDIT.read_text())
    actual=json.loads(ACTUAL.read_text())
    actual_audit=json.loads(ACTUAL_AUDIT.read_text())

    actual_sha=sha256_file(ACTUAL)
    cons_sha=sha256_file(CONS)

    # Input integrity / prior gates.
    inputs={
        "dukas_repeatability_pass":bool(duka.get("repeatability_gate_pass")),
        "dukas_release_created_or_verified":bool(duka["release"].get("created_or_verified_existing")),
        "dukas_release_tag_exact":duka["release"].get("tag")==EXPECTED_DUKA_TAG,
        "dukas_archive_sha_exact":duka["release"].get("archive_sha256")==EXPECTED_DUKA_SHA,
        "dukas_effective_interval_exact":duka["source"].get("effective_common_model_interval")==EXPECTED_INTERVAL,
        "all_8_market_integrity_pass":len(duka["markets"])==8 and all(x["copy_a"]["integrity_pass"] for x in duka["markets"].values()),
        "consensus_v03_sha_matches_audit":cons_sha==cons_audit["normalized_dataset"]["sha256"],
        "consensus_v03_gate_pass":bool(cons_audit.get("consensus_layer_gate_pass")),
        "official_actual_sha_matches_audit":actual_sha==actual_audit["output"]["sha256"],
        "official_actual_reconciliation_pass":bool(actual_audit.get("official_actual_reconciliation_pass")),
    }

    records=actual["records"]

    # Provenance checks.
    numeric=[r for r in records if not r.get("timing_only")]
    fomc=[r for r in records if r.get("timing_only")]

    provenance={
        "numeric_records_67":len(numeric)==67,
        "fomc_records_8":len(fomc)==8,
        "all_numeric_have_forecast":all(r.get("forecast_text") not in (None,"") for r in numeric),
        "all_numeric_official_context_verified":all(r.get("official_context_verified") is True for r in numeric),
        "all_numeric_have_official_actual":all(r.get("official_actual_numeric") is not None for r in numeric),
        "all_numeric_have_source_sha":all(bool(r.get("official_actual_source_sha256")) for r in numeric),
        "all_numeric_have_utc_timestamp":all(bool(r.get("official_release_timestamp_utc")) for r in numeric),
        "all_fomc_timing_only":all(r.get("timing_only") is True and r.get("surprise_component") is None for r in fomc),
        "all_fomc_have_utc_timestamp":all(bool(r.get("official_release_timestamp_utc")) for r in fomc),
        "all_fomc_have_source_url":all(bool(r.get("official_source_url")) for r in fomc),
        "consensus_source_role_frozen":cons.get("source_role",{}).get("ForexFactory_Forecast")=="PUBLIC_CALENDAR_CONSENSUS_FF",
        "protected_periods_sealed":(
            not actual["protected_periods"]["jul_aug_2026_loaded"]
            and not actual["protected_periods"]["sep_2026_loaded"]
            and not duka["protected_periods"]["jul_aug_2026_loaded"]
            and not duka["protected_periods"]["sep_2026_loaded"]
        ),
    }

    # Collapse by exact official timestamp to respect original independent-block rule.
    by_ts=defaultdict(list)
    for r in records:
        ts=r["official_release_timestamp_utc"]
        by_ts[ts].append(r)

    independent=[]
    family_timestamp_sets=defaultdict(set)

    for ts,rs in sorted(by_ts.items()):
        families=set()
        surprise=False
        official_block_ids=[]
        for r in rs:
            fam=r["family"]
            families.add(fam)
            official_block_ids.append(r["official_block_id"])
            family_timestamp_sets[fam].add(ts)
            if fam=="GDP_PCE":
                family_timestamp_sets["GDP_PCE"].add(ts)
            if not r.get("timing_only") and r.get("forecast_numeric") is not None and r.get("official_actual_numeric") is not None:
                surprise=True

        independent.append({
            "timestamp_utc":ts,
            "families":sorted(families),
            "official_block_ids":sorted(official_block_ids),
            "surprise_bearing":surprise,
        })

    family_counts={
        "EMPLOYMENT":len(family_timestamp_sets["EMPLOYMENT"]),
        "CPI":len(family_timestamp_sets["CPI"]),
        "PPI":len(family_timestamp_sets["PPI"]),
        "RETAIL":len(family_timestamp_sets["RETAIL"]),
        "GDP_PCE":len(family_timestamp_sets["GDP_PCE"]),
        "FOMC":len(family_timestamp_sets["FOMC"]),
    }

    surprise_blocks=sum(1 for b in independent if b["surprise_bearing"])

    # Freeze six deterministic chronological folds.
    folds=[]
    fold_pass=True
    for i,chunk in enumerate(split_six(independent),start=1):
        fams=sorted({f for b in chunk for f in b["families"]})
        fp=len(chunk)>=4 and len(fams)>=2
        fold_pass=fold_pass and fp
        folds.append({
            "fold":i,
            "start_timestamp_utc":chunk[0]["timestamp_utc"] if chunk else None,
            "end_timestamp_utc":chunk[-1]["timestamp_utc"] if chunk else None,
            "independent_blocks":len(chunk),
            "families":fams,
            "family_count":len(fams),
            "pass":fp,
            "block_timestamps":[b["timestamp_utc"] for b in chunk],
        })

    gate={
        # 1 market history
        "market_history_12m_frozen_interval":(
            inputs["dukas_repeatability_pass"]
            and inputs["dukas_release_created_or_verified"]
            and inputs["dukas_release_tag_exact"]
            and inputs["dukas_archive_sha_exact"]
            and inputs["dukas_effective_interval_exact"]
            and inputs["all_8_market_integrity_pass"]
        ),
        # 2 family minimums
        "numeric_families_ge_8":all(family_counts[f]>=8 for f in NUMERIC_FAMILIES),
        # 3 total independent blocks
        "independent_blocks_ge_40":len(independent)>=40,
        # 4 surprise blocks
        "surprise_bearing_blocks_ge_30":surprise_blocks>=30,
        # 5 FOMC
        "fomc_events_ge_6_or_timing_only":family_counts["FOMC"]>=6 and all(r.get("timing_only") for r in fomc),
        # 6 folds >=4
        "all_6_folds_ge_4_blocks":len(folds)==6 and all(f["independent_blocks"]>=4 for f in folds),
        # 7 folds >=2 families
        "all_6_folds_ge_2_families":len(folds)==6 and all(f["family_count"]>=2 for f in folds),
        # 8 consensus point-in-time provenance
        "consensus_pre_release_provenance_frozen":(
            inputs["consensus_v03_sha_matches_audit"]
            and inputs["consensus_v03_gate_pass"]
            and provenance["consensus_source_role_frozen"]
            and provenance["all_numeric_have_forecast"]
        ),
        # 9 official timestamps independently verified
        "official_release_provenance_complete":(
            inputs["official_actual_sha_matches_audit"]
            and inputs["official_actual_reconciliation_pass"]
            and provenance["all_numeric_official_context_verified"]
            and provenance["all_numeric_have_utc_timestamp"]
            and provenance["all_fomc_have_utc_timestamp"]
        ),
        # 10 protected seal
        "protected_periods_unloaded_unlabeled":provenance["protected_periods_sealed"],
        # integrity extras
        "macro_record_counts_exact":provenance["numeric_records_67"] and provenance["fomc_records_8"],
        "official_actuals_have_source_hashes":provenance["all_numeric_have_source_sha"],
        "fomc_first_party_sources_present":provenance["all_fomc_have_source_url"],
        "no_market_outcomes_calculated":True,
    }

    passed=all(gate.values())

    result={
        "stage":"EXP-041 final Gate-A adequacy/provenance audit v0.1",
        "tested_repository_sha":os.environ.get("GITHUB_SHA"),
        "github_run_id":os.environ.get("GITHUB_RUN_ID"),
        "inputs":{
            "dukas_snapshot_tag":duka["release"]["tag"],
            "dukas_archive_sha256":duka["release"]["archive_sha256"],
            "consensus_v03_sha256":cons_sha,
            "official_surprise_layer_sha256":actual_sha,
        },
        "independent_event_block_rule":"collapse exact official_release_timestamp_utc",
        "official_records":len(records),
        "independent_event_blocks":len(independent),
        "surprise_bearing_independent_blocks":surprise_blocks,
        "family_independent_timestamp_counts":family_counts,
        "chronological_folds":folds,
        "input_integrity":inputs,
        "provenance":provenance,
        "gate":gate,
        "gate_a_pass":passed,
        "market_data_loaded":False,
        "target_labels_calculated":False,
        "pnl_calculated":False,
        "scientific_market_outcomes_calculated":False,
        "protected_periods":{
            "jul_aug_2026_loaded":False,
            "sep_2026_loaded":False,
        },
        "disposition":(
            "EXP041_GATE_A_PASS_AUTHORIZE_GATE_B_INFORMATION_CONTENT"
            if passed else
            "EXP041_GATE_A_FAIL_DO_NOT_MODEL"
        ),
    }

    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({
        "gate_a_pass":passed,
        "independent_event_blocks":len(independent),
        "surprise_bearing_independent_blocks":surprise_blocks,
        "family_counts":family_counts,
        "folds":[{"fold":f["fold"],"blocks":f["independent_blocks"],"families":f["family_count"],"pass":f["pass"]} for f in folds],
        "disposition":result["disposition"],
    },indent=2))
    return 0 if passed else 2


if __name__=="__main__":
    sys.exit(main())
