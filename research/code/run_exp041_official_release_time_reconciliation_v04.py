#!/usr/bin/env python3
"""EXP-041 official release-time reconciliation v0.4.

Targeted repair of the 14 unresolved 2026 BEA blocks in the frozen v0.2 map.
No schedule scraping. No market outcomes.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import urllib.request
from copy import deepcopy
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "research/data/EXP-041-official-release-time-map-v0.2.json"
BASE_AUDIT = ROOT / "research/results/EXP-041-official-release-time-reconciliation-v0.2.json"
OUT = ROOT / "research/data/EXP-041-official-release-time-map-v0.4.json"
RESULT = ROOT / "research/results/EXP-041-official-release-time-reconciliation-v0.4.json"

EXPECTED_BASE_SHA = "691c09da1829695821ead84647bb87b2b1b4c1a4cdc4d727cb33042e991edd1a"
UA = "Mozilla/5.0 (compatible; target-first-trading-system-exp041/0.4; official-source verification)"
NY = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")

BEA_2026 = {
    "2026-01-22|GDP_PCE|GDP": {
        "url": "https://www.bea.gov/news/2026/gross-domestic-product-3rd-quarter-2025-updated-estimate-gdp-industry-and-corporate",
        "time": "08:30",
        "tz_abbr": "EST",
        "kind": "GDP",
    },
    "2026-01-22|GDP_PCE|PCE": {
        "url": "https://www.bea.gov/news/2026/personal-income-and-outlays-october-and-november-2025",
        "time": "10:00",
        "tz_abbr": "EST",
        "kind": "PCE",
    },
    "2026-02-20|GDP_PCE|GDP": {
        "url": "https://www.bea.gov/news/2026/gdp-advance-estimate-4th-quarter-and-year-2025",
        "time": "08:30",
        "tz_abbr": "EST",
        "kind": "GDP",
    },
    "2026-02-20|GDP_PCE|PCE": {
        "url": "https://www.bea.gov/news/2026/personal-income-and-outlays-december-2025",
        "time": "08:30",
        "tz_abbr": "EST",
        "kind": "PCE",
    },
    "2026-03-13|GDP_PCE|GDP": {
        "url": "https://www.bea.gov/news/2026/gdp-second-estimate-4th-quarter-and-year-2025",
        "time": "08:30",
        "tz_abbr": "EDT",
        "kind": "GDP",
    },
    "2026-03-13|GDP_PCE|PCE": {
        "url": "https://www.bea.gov/news/2026/personal-income-and-outlays-january-2026",
        "time": "08:30",
        "tz_abbr": "EDT",
        "kind": "PCE",
    },
    "2026-04-09|GDP_PCE|GDP": {
        "url": "https://www.bea.gov/news/2026/gdp-third-estimate-industries-corporate-profits-state-gdp-and-state-personal-income-4th",
        "time": "08:30",
        "tz_abbr": "EDT",
        "kind": "GDP",
    },
    "2026-04-09|GDP_PCE|PCE": {
        "url": "https://www.bea.gov/news/2026/personal-income-and-outlays-february-2026",
        "time": "08:30",
        "tz_abbr": "EDT",
        "kind": "PCE",
    },
    "2026-04-30|GDP_PCE|GDP": {
        "url": "https://www.bea.gov/news/2026/gdp-advance-estimate-1st-quarter-2026",
        "time": "08:30",
        "tz_abbr": "EDT",
        "kind": "GDP",
    },
    "2026-04-30|GDP_PCE|PCE": {
        "url": "https://www.bea.gov/news/2026/personal-income-and-outlays-march-2026",
        "time": "08:30",
        "tz_abbr": "EDT",
        "kind": "PCE",
    },
    "2026-05-28|GDP_PCE|GDP": {
        "url": "https://www.bea.gov/news/2026/gdp-second-estimate-and-corporate-profits-1st-quarter-2026",
        "time": "08:30",
        "tz_abbr": "EDT",
        "kind": "GDP",
    },
    "2026-05-28|GDP_PCE|PCE": {
        "url": "https://www.bea.gov/news/2026/personal-income-and-outlays-april-2026",
        "time": "08:30",
        "tz_abbr": "EDT",
        "kind": "PCE",
    },
    "2026-06-25|GDP_PCE|GDP": {
        "url": "https://www.bea.gov/news/2026/gdp-third-estimate-industries-corporate-profits-state-gdp-and-state-personal-income-1st",
        "time": "08:30",
        "tz_abbr": "EDT",
        "kind": "GDP",
    },
    "2026-06-25|GDP_PCE|PCE": {
        "url": "https://www.bea.gov/news/2026/personal-income-and-outlays-may-2026",
        "time": "08:30",
        "tz_abbr": "EDT",
        "kind": "PCE",
    },
}


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        if int(r.status) != 200:
            raise RuntimeError(f"HTTP {r.status}: {url}")
        return r.read()


def compact_html(raw: bytes) -> str:
    s = raw.decode("utf-8", "replace")
    s = re.sub(r"<script\b[^>]*>.*?</script>", " ", s, flags=re.I | re.S)
    s = re.sub(r"<style\b[^>]*>.*?</style>", " ", s, flags=re.I | re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"&nbsp;|&#160;", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def date_text(d: date) -> str:
    return f"{d.strftime('%B')} {d.day}, {d.year}"


def expected_zone_abbr(d: date, hh: int, mm: int) -> str:
    return datetime(d.year, d.month, d.day, hh, mm, tzinfo=NY).tzname()


def utc_timestamp(d: date, hh: int, mm: int) -> str:
    return datetime(d.year, d.month, d.day, hh, mm, tzinfo=NY).astimezone(UTC).isoformat().replace("+00:00", "Z")


def main() -> int:
    if not BASE.exists() or not BASE_AUDIT.exists():
        raise SystemExit("frozen v0.2 official-time map/audit missing")

    audit = json.loads(BASE_AUDIT.read_text())
    audit_sha = audit["official_time_map"]["sha256"]
    observed_sha = sha256_file(BASE)
    if audit_sha != EXPECTED_BASE_SHA or observed_sha != EXPECTED_BASE_SHA:
        raise SystemExit(f"base v0.2 map SHA mismatch: audit={audit_sha}, observed={observed_sha}")

    base = json.loads(BASE.read_text())
    blocks = deepcopy(base["official_blocks"])

    unresolved_before = [
        b["official_block_id"]
        for b in blocks
        if b["family"] == "GDP_PCE"
        and b["event_date"].startswith("2026-")
        and not b.get("official_release_timestamp_utc")
    ]
    if sorted(unresolved_before) != sorted(BEA_2026):
        raise SystemExit(f"unexpected unresolved 2026 BEA set: {unresolved_before}")

    # Snapshot all unaffected blocks before repair and ensure they remain identical.
    untouched_before = {
        b["official_block_id"]: deepcopy(b)
        for b in blocks
        if b["official_block_id"] not in BEA_2026
    }

    errors = []
    page_meta = {}

    for b in blocks:
        bid = b["official_block_id"]
        if bid not in BEA_2026:
            continue

        cfg = BEA_2026[bid]
        d = date.fromisoformat(b["event_date"])
        hh, mm = map(int, cfg["time"].split(":"))

        try:
            raw = fetch(cfg["url"])
            t = compact_html(raw)
            date_ok = date_text(d).lower() in t.lower()
            embargo_ok = "EMBARGOED UNTIL RELEASE AT".lower() in t.lower()
            time_pattern = rf"{hh if hh <= 12 else hh-12}:{mm:02d}\s*a\.m\.\s*{cfg['tz_abbr']}"
            time_ok = bool(re.search(time_pattern, t, flags=re.I))
            zone_ok = expected_zone_abbr(d, hh, mm) == cfg["tz_abbr"]

            if cfg["kind"] == "GDP":
                identity_ok = bool(re.search(r"Gross Domestic Product|\bGDP\b", t, flags=re.I))
            else:
                identity_ok = bool(re.search(r"Personal Income and Outlays", t, flags=re.I))

            page_meta[bid] = {
                "url": cfg["url"],
                "sha256": sha256_bytes(raw),
                "bytes": len(raw),
                "date_ok": date_ok,
                "embargo_marker_ok": embargo_ok,
                "time_ok": time_ok,
                "zone_ok": zone_ok,
                "identity_ok": identity_ok,
            }

            if not all([date_ok, embargo_ok, time_ok, zone_ok, identity_ok]):
                raise RuntimeError(f"direct BEA page verification failed: {page_meta[bid]}")

            b.update({
                "official_authority": "U.S. Bureau of Economic Analysis",
                "official_source_url": cfg["url"],
                "official_release_page_url": cfg["url"],
                "official_source_sha256": sha256_bytes(raw),
                "official_local_timezone": "America/New_York",
                "official_local_release_time": cfg["time"],
                "official_release_timestamp_utc": utc_timestamp(d, hh, mm),
                "source_date_verified": True,
                "source_time_verified": True,
            })
            for k in ["error_type", "error_detail"]:
                b.pop(k, None)

        except Exception as exc:
            errors.append({
                "official_block_id": bid,
                "reason": type(exc).__name__,
                "detail": str(exc)[:500],
            })

    untouched_after = {
        b["official_block_id"]: b
        for b in blocks
        if b["official_block_id"] not in BEA_2026
    }
    untouched_ok = untouched_before == untouched_after

    all_complete = all(
        b.get("official_source_url")
        and b.get("official_source_sha256")
        and b.get("official_release_timestamp_utc")
        and b.get("source_date_verified")
        and b.get("source_time_verified")
        for b in blocks
    )

    repaired = [
        b["official_block_id"]
        for b in blocks
        if b["official_block_id"] in BEA_2026
        and b.get("official_release_timestamp_utc")
    ]

    gate = {
        "base_v02_sha_verified": True,
        "exactly_14_unresolved_2026_bea_before_repair": len(unresolved_before) == 14,
        "all_14_direct_bea_pages_verified": len(repaired) == 14 and len(errors) == 0,
        "all_75_official_blocks_complete_after_repair": len(blocks) == 75 and all_complete,
        "untouched_blocks_identical_to_v02": untouched_ok,
        "no_market_data_or_outcomes_loaded": True,
        "protected_periods_sealed": True,
    }
    passed = all(gate.values())

    payload = {
        "stage": "EXP-041 official release-time map v0.4",
        "base_map": str(BASE.relative_to(ROOT)),
        "base_map_sha256": observed_sha,
        "repair_scope": "14 unresolved 2026 BEA GDP/PCE blocks only",
        "official_blocks": blocks,
        "official_block_count": len(blocks),
        "protected_periods": base["protected_periods"],
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    out_sha = sha256_file(OUT)

    result = {
        "stage": "EXP-041 official release-time reconciliation v0.4",
        "tested_repository_sha": os.environ.get("GITHUB_SHA"),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "base_v02": {
            "path": str(BASE.relative_to(ROOT)),
            "expected_sha256": EXPECTED_BASE_SHA,
            "observed_sha256": observed_sha,
        },
        "direct_bea_manifest_blocks": len(BEA_2026),
        "unresolved_before": unresolved_before,
        "repaired_blocks": repaired,
        "page_meta": page_meta,
        "errors": errors,
        "official_time_map": {
            "path": str(OUT.relative_to(ROOT)),
            "sha256": out_sha,
            "official_blocks": len(blocks),
        },
        "gate": gate,
        "release_time_reconciliation_pass": passed,
        "official_actual_reconciliation_complete": False,
        "market_data_loaded": False,
        "target_labels_calculated": False,
        "pnl_calculated": False,
        "scientific_outcomes_calculated": False,
        "protected_periods": base["protected_periods"],
        "disposition": (
            "OFFICIAL_RELEASE_TIME_RECONCILIATION_V04_PASS_ACTUAL_VALUES_REQUIRED"
            if passed else
            "OFFICIAL_RELEASE_TIME_RECONCILIATION_V04_FAILED_DIRECT_BEA_VERIFICATION"
        ),
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    print(json.dumps({
        "pass": passed,
        "unresolved_before": len(unresolved_before),
        "repaired": len(repaired),
        "errors": len(errors),
        "all_75_complete": all_complete,
        "disposition": result["disposition"],
    }, indent=2))
    return 0 if passed else 2


if __name__ == "__main__":
    sys.exit(main())
