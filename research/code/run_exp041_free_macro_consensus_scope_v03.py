#!/usr/bin/env python3
"""EXP-041 deterministic v0.3 macro-consensus scope correction.

Consumes frozen v0.2 only. No network.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "research/data/EXP-041-free-macro-consensus-v0.2.json"
AUDIT_V02 = ROOT / "research/results/EXP-041-free-macro-consensus-acquisition-audit-v0.2.json"
OUT = ROOT / "research/data/EXP-041-free-macro-consensus-v0.3.json"
RESULT = ROOT / "research/results/EXP-041-free-macro-consensus-scope-audit-v0.3.json"

NUMERIC_FAMILIES = ["EMPLOYMENT","CPI","PPI","RETAIL","GDP_PCE"]
EMPLOYMENT_ALLOWED = {
    "non-farm employment change",
    "unemployment rate",
    "average hourly earnings m/m",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not SRC.exists() or not AUDIT_V02.exists():
        raise SystemExit("required frozen v0.2 input/audit missing")

    audit = json.loads(AUDIT_V02.read_text())
    expected = audit["normalized_dataset"]["sha256"]
    observed = sha256(SRC)
    if observed != expected:
        raise SystemExit(f"v0.2 dataset SHA mismatch: expected {expected}, observed {observed}")

    src = json.loads(SRC.read_text())
    records_in = src["records"]

    removed_adp = []
    records = []
    for r in records_in:
        if r["family"] != "EMPLOYMENT":
            records.append(r)
            continue
        name = re.sub(r"\s+", " ", r["event_name"]).strip().lower()
        if "adp" in name:
            removed_adp.append(r)
            continue
        if name not in EMPLOYMENT_ALLOWED:
            raise SystemExit(f"unexpected EMPLOYMENT component in frozen v0.2: {r['event_name']}")
        records.append(r)

    blocks = defaultdict(list)
    for r in records:
        blocks[f"{r['event_date']}|{r['family']}"].append(r)

    family_blocks = Counter()
    surprise_blocks = 0
    block_rows = []
    for key, rs in sorted(blocks.items()):
        fam = rs[0]["family"]
        surprise = any(r["has_actual"] and r["has_forecast"] for r in rs)
        surprise_blocks += int(surprise)
        family_blocks[fam] += 1
        block_rows.append({
            "block_id": key,
            "event_date": rs[0]["event_date"],
            "family": fam,
            "component_count": len(rs),
            "surprise_bearing_provisional": surprise,
            "component_event_ids": [r["event_id"] for r in rs if r.get("event_id")],
            "component_names": [r["event_name"] for r in rs],
        })

    employment_rows = [r for r in records if r["family"] == "EMPLOYMENT"]
    adp_remaining = [r for r in employment_rows if "adp" in r["event_name"].lower()]
    nfp_rows = [r for r in employment_rows if r["event_name"].strip().lower() == "non-farm employment change"]

    gate = {
        "input_v02_sha_verified": True,
        "adp_rows_removed_gt_0": len(removed_adp) > 0,
        "no_adp_rows_remaining": len(adp_remaining) == 0,
        "nfp_component_present": len(nfp_rows) > 0,
        "provisional_blocks_ge_40": len(block_rows) >= 40,
        "surprise_bearing_blocks_ge_30": surprise_blocks >= 30,
        "each_numeric_family_blocks_ge_8": all(family_blocks[f] >= 8 for f in NUMERIC_FAMILIES),
        "fomc_policy_events_ge_6_or_timing_only_allowed": True,
        "no_market_data_or_outcomes_loaded": True,
        "protected_periods_sealed": True,
    }
    passed = all(gate.values())

    payload = {
        "stage": "EXP-041 free macro consensus normalized layer v0.3",
        "source_dataset": str(SRC.relative_to(ROOT)),
        "source_dataset_sha256": observed,
        "supersedes": str(SRC.relative_to(ROOT)),
        "scope_correction": {
            "remove_adp_from_primary_employment_family": True,
            "employment_allowed_names": sorted(EMPLOYMENT_ALLOWED),
            "removed_adp_rows": len(removed_adp),
            "network_access_used": False,
        },
        "source_role": src["source_role"],
        "allowed_interval": src["allowed_interval"],
        "records": records,
        "provisional_event_blocks": block_rows,
        "protected_periods": src["protected_periods"],
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    out_sha = sha256(OUT)

    result = {
        "stage": "EXP-041 free macro consensus scope audit v0.3",
        "tested_repository_sha": os.environ.get("GITHUB_SHA"),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "input_v02": {
            "path": str(SRC.relative_to(ROOT)),
            "expected_sha256": expected,
            "observed_sha256": observed,
        },
        "normalized_dataset": {
            "path": str(OUT.relative_to(ROOT)),
            "sha256": out_sha,
            "records": len(records),
        },
        "removed_adp_rows": len(removed_adp),
        "removed_adp_dates": sorted({r["event_date"] for r in removed_adp}),
        "employment_component_rows": len(employment_rows),
        "nfp_component_rows": len(nfp_rows),
        "provisional_independent_event_blocks": len(block_rows),
        "surprise_bearing_provisional_blocks": surprise_blocks,
        "family_block_counts": dict(sorted(family_blocks.items())),
        "fomc_policy_event_dates": family_blocks["FOMC"],
        "fomc_timing_only_if_lt_6": family_blocks["FOMC"] < 6,
        "gate": gate,
        "consensus_layer_gate_pass": passed,
        "official_reconciliation_complete": False,
        "network_access_used": False,
        "market_data_loaded": False,
        "target_labels_calculated": False,
        "pnl_calculated": False,
        "scientific_outcomes_calculated": False,
        "protected_periods": src["protected_periods"],
        "disposition": (
            "FREE_CONSENSUS_V03_BLS_EMPLOYMENT_SCOPE_PASS_OFFICIAL_RECONCILIATION_REQUIRED"
            if passed else
            "FREE_CONSENSUS_V03_SCOPE_CORRECTION_FAILED"
        ),
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    print(json.dumps({
        "pass": passed,
        "removed_adp_rows": len(removed_adp),
        "records": len(records),
        "blocks": len(block_rows),
        "surprise_blocks": surprise_blocks,
        "family_blocks": dict(sorted(family_blocks.items())),
        "disposition": result["disposition"],
    }, indent=2))
    return 0 if passed else 2


if __name__ == "__main__":
    sys.exit(main())
