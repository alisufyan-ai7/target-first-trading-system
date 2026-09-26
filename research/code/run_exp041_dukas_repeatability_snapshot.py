#!/usr/bin/env python3
"""EXP-041 Dukascopy same-run repeatability + snapshot manifest.

Zero-outcome data infrastructure only.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
A_DIR = Path(os.environ.get("EXP041_DATA_A", "/tmp/exp041-dukas-repeat-a"))
B_DIR = Path(os.environ.get("EXP041_DATA_B", "/tmp/exp041-dukas-repeat-b"))
OUT = ROOT / "research/results"
OUT.mkdir(parents=True, exist_ok=True)

SYMBOLS = ["XAUUSD","EURUSD","GBPUSD","USDJPY","EURJPY","AUDUSD","USDCAD","USDCHF"]
HEADER = ["datetime","open","high","low","close","volume"]
START = datetime(2025,7,1,tzinfo=timezone.utc)
END = datetime(2026,7,1,tzinfo=timezone.utc)
FIRST_MAX = datetime(2025,7,2,23,59,tzinfo=timezone.utc)
LAST_MIN = datetime(2026,6,29,23,0,tzinfo=timezone.utc)
TAG = "exp041-data-dukas-m1-2025-07-01_2026-06-30-v2"
ASSET = "exp041-dukas-m1-2025-07-01_2026-06-30-v2.tar.gz"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z","+00:00")).astimezone(timezone.utc)


def inspect(path: Path) -> dict:
    if not path.exists():
        return {"exists": False, "integrity_pass": False, "error": "missing"}

    rows = 0
    dates = set()
    first = None
    last = None
    prev = None
    duplicate_count = 0
    monotonic = True
    all_in_range = True
    positive = True
    geometry = True

    with path.open("r", encoding="utf-8", newline="") as fh:
        r = csv.reader(fh)
        header = next(r, None)
        if header != HEADER:
            return {
                "exists": True,
                "sha256": sha256(path),
                "integrity_pass": False,
                "error": f"unexpected header {header!r}",
            }

        for line in r:
            if len(line) != 6:
                return {
                    "exists": True,
                    "sha256": sha256(path),
                    "integrity_pass": False,
                    "error": f"malformed row length {len(line)}",
                }
            ts = parse_ts(line[0])
            o,h,l,c,v = map(float, line[1:])
            rows += 1
            dates.add(ts.date())
            first = ts if first is None else first
            last = ts

            if prev is not None:
                if ts == prev:
                    duplicate_count += 1
                if ts <= prev:
                    monotonic = False
            prev = ts

            all_in_range = all_in_range and START <= ts < END
            positive = positive and o > 0 and h > 0 and l > 0 and c > 0
            geometry = geometry and h >= max(o,c,l) and l <= min(o,c,h)

    checks = {
        "rows_ge_300k": rows >= 300_000,
        "distinct_dates_ge_240": len(dates) >= 240,
        "first_timestamp_by_july2": first is not None and first <= FIRST_MAX,
        "last_timestamp_at_least_jun29_23utc": last is not None and last >= LAST_MIN,
        "all_rows_inside_frozen_interval": all_in_range,
        "strictly_increasing_no_duplicates": monotonic and duplicate_count == 0,
        "positive_prices": positive,
        "valid_ohlc_geometry": geometry,
    }

    return {
        "exists": True,
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "rows": rows,
        "distinct_utc_dates": len(dates),
        "first_timestamp": first.isoformat() if first else None,
        "last_timestamp": last.isoformat() if last else None,
        "duplicate_count": duplicate_count,
        "checks": checks,
        "integrity_pass": all(checks.values()),
    }


def main() -> None:
    markets = {}
    repeatability_pass = True

    for symbol in SYMBOLS:
        a = inspect(A_DIR / f"{symbol}.csv")
        b = inspect(B_DIR / f"{symbol}.csv")
        same_hash = a.get("sha256") == b.get("sha256") and a.get("sha256") is not None
        same_rows = a.get("rows") == b.get("rows") and a.get("rows") is not None
        market_pass = bool(a.get("integrity_pass") and b.get("integrity_pass") and same_hash and same_rows)
        repeatability_pass = repeatability_pass and market_pass
        markets[symbol] = {
            "copy_a": a,
            "copy_b": b,
            "same_sha256": same_hash,
            "same_rows": same_rows,
            "repeatability_pass": market_pass,
        }

    stable_manifest = {
        "snapshot_id": "EXP-041 canonical Dukascopy immutable snapshot v2",
        "release_tag": TAG,
        "source": {
            "authority": "Dukascopy Bank historical data",
            "transport_helper": "dukascopy-node",
            "transport_version": "1.50.0",
            "download_interval": ["2025-07-01T00:00:00Z","2026-07-01T00:00:00Z"],
            "effective_common_model_interval": ["2025-07-01T00:00:00Z","2026-06-30T00:00:00Z"],
        },
        "markets": {
            s: {
                "file": f"{s}.csv",
                "sha256": markets[s]["copy_a"].get("sha256"),
                "rows": markets[s]["copy_a"].get("rows"),
                "bytes": markets[s]["copy_a"].get("bytes"),
                "first_timestamp": markets[s]["copy_a"].get("first_timestamp"),
                "last_timestamp": markets[s]["copy_a"].get("last_timestamp"),
            }
            for s in SYMBOLS
        },
        "repeatability_gate_pass": repeatability_pass,
        "protected_periods": {"jul_aug_2026_loaded": False, "sep_2026_loaded": False},
    }
    (A_DIR / "SNAPSHOT-MANIFEST.json").write_text(
        json.dumps(stable_manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    result = {
        "stage": "EXP-041 Dukascopy same-run repeatability + immutable snapshot recovery v0.1",
        "tested_repository_sha": os.environ.get("GITHUB_SHA"),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "source": stable_manifest["source"],
        "markets": markets,
        "repeatability_gate_pass": repeatability_pass,
        "release": {
            "tag": TAG,
            "archive_asset": ASSET,
            "archive_sha256": None,
            "created_or_verified_existing": False,
        },
        "scientific_outcomes_calculated": False,
        "target_labels_calculated": False,
        "pnl_calculated": False,
        "protected_periods": {"jul_aug_2026_loaded": False, "sep_2026_loaded": False},
        "disposition": (
            "CURRENT_DUKASCOPY_REPEATABLE_ELIGIBLE_TO_FREEZE_SNAPSHOT_V2"
            if repeatability_pass
            else "CURRENT_DUKASCOPY_TRANSPORT_NONDETERMINISTIC_FIX_ACQUISITION_BEFORE_SNAPSHOT"
        ),
    }

    p = OUT / "EXP-041-dukas-repeatability-snapshot-recovery-v0.1.json"
    p.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "repeatability_gate_pass": repeatability_pass,
        "market_pass": {s: markets[s]["repeatability_pass"] for s in SYMBOLS},
        "copy_a_rows": {s: markets[s]["copy_a"].get("rows") for s in SYMBOLS},
        "copy_b_rows": {s: markets[s]["copy_b"].get("rows") for s in SYMBOLS},
        "disposition": result["disposition"],
    }, indent=2))


if __name__ == "__main__":
    main()
