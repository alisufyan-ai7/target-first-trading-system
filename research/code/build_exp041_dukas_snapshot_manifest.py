#!/usr/bin/env python3
"""Verify and manifest the frozen EXP-041 Dukascopy development snapshot.

Data infrastructure only: no labels, no P&L, no protected periods.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(os.environ.get("EXP041_DATA_DIR", "/tmp/exp041-dukas-m1"))
OUT = ROOT / "research/results"
OUT.mkdir(parents=True, exist_ok=True)

EXPECTED = {
    "XAUUSD": {"sha256": "1afa576b5492b4965b6ca19fe613ae8e5a7e520b2dc8f8b16fff32eb37b6b197", "rows": 344537},
    "EURUSD": {"sha256": "22d3efa1d303f4e4a80bf41f89fd296e9128e699718798624195d13ca87b7b0f", "rows": 367667},
    "GBPUSD": {"sha256": "3b4a5bdd8fb02508596ec64dca1ffdd92adfde72cc0039cb1c22de913dda68b2", "rows": 338380},
    "USDJPY": {"sha256": "05296feddaacc8c5c0d9778be9a7612693bbbe3f9f66f0f716838ad0f51fe5f4", "rows": 368988},
    "EURJPY": {"sha256": "4514cdbe82e4aa2c73d5c30c8ecf1b14c95d49bbd09e568ebd510b8fe49a36d3", "rows": 353514},
    "AUDUSD": {"sha256": "f275920579feb1fe5f3c9d14bffed7cf61bc140d5181a14480e9d3b03a31d4ab", "rows": 364256},
    "USDCAD": {"sha256": "00ddb2cde3a7a96539a750747f8c76993aa755f5a4fc94169875959b1e62a568", "rows": 364120},
    "USDCHF": {"sha256": "1b066ffe16a9cbfe18f1c25ece76390a3d6ca3ef3b6f1fd74bd816f7c14b98da", "rows": 354708},
}
HEADER = "datetime,open,high,low,close,volume"
TAG = "exp041-data-dukas-m1-2025-07-01_2026-06-30-v1"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def line_count(path: Path) -> int:
    with path.open("rb") as fh:
        return sum(1 for _ in fh) - 1


def first_last(path: Path) -> tuple[str, str]:
    with path.open("r", encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n\r")
        if header != HEADER:
            raise RuntimeError(f"{path.name}: unexpected header {header!r}")
        first = fh.readline().split(",", 1)[0]
        last = first
        for line in fh:
            if line.strip():
                last = line.split(",", 1)[0]
    if not first:
        raise RuntimeError(f"{path.name}: no data rows")
    return first, last


def main() -> None:
    markets = {}
    all_match = True

    for symbol, exp in EXPECTED.items():
        path = DATA / f"{symbol}.csv"
        if not path.exists():
            raise RuntimeError(f"{symbol}: normalized file missing")
        observed_hash = sha256(path)
        observed_rows = line_count(path)
        first, last = first_last(path)
        hash_match = observed_hash == exp["sha256"]
        rows_match = observed_rows == exp["rows"]
        match = hash_match and rows_match
        all_match = all_match and match
        markets[symbol] = {
            "file": path.name,
            "expected_sha256": exp["sha256"],
            "observed_sha256": observed_hash,
            "hash_match": hash_match,
            "expected_rows": exp["rows"],
            "observed_rows": observed_rows,
            "rows_match": rows_match,
            "first_timestamp": first,
            "last_timestamp": last,
            "bytes": path.stat().st_size,
            "snapshot_match": match,
        }

    result = {
        "stage": "EXP-041 canonical Dukascopy immutable snapshot v1",
        "governance_version": "v0.2",
        "tested_repository_sha": os.environ.get("GITHUB_SHA"),
        "source": {
            "authority": "Dukascopy Bank historical data",
            "transport_helper": "dukascopy-node",
            "transport_version": "1.50.0",
            "download_interval": ["2025-07-01T00:00:00Z", "2026-07-01T00:00:00Z"],
            "effective_common_model_interval": ["2025-07-01T00:00:00Z", "2026-06-30T00:00:00Z"],
        },
        "release": {
            "tag": TAG,
            "archive_asset": "exp041-dukas-m1-2025-07-01_2026-06-30-v1.tar.gz",
            "archive_sha256": None,
            "created": False,
        },
        "frozen_reference_audit_commit": "1cf168d6b3b639cfcc856ffae7aeb66db880dc47",
        "markets": markets,
        "all_expected_hashes_and_rows_match": all_match,
        "target_labels_calculated": False,
        "pnl_calculated": False,
        "scientific_outcomes_calculated": False,
        "protected_periods": {"jul_aug_2026_loaded": False, "sep_2026_loaded": False},
        "snapshot_eligible": all_match,
    }

    out = OUT / "EXP-041-canonical-dukas-snapshot-v1.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (DATA / "SNAPSHOT-MANIFEST.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "snapshot_eligible": all_match,
        "hash_match": {s: v["hash_match"] for s, v in markets.items()},
        "rows_match": {s: v["rows_match"] for s, v in markets.items()},
        "protected_periods": result["protected_periods"],
    }, indent=2))

    if not all_match:
        raise SystemExit("Frozen Dukascopy bytes no longer reproduce the audited hashes; investigate source drift.")


if __name__ == "__main__":
    main()
