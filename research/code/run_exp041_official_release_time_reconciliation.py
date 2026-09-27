#!/usr/bin/env python3
"""EXP-041 official first-party release-time reconciliation v0.1.

Zero market outcomes. Consumes frozen consensus v0.3 and produces official UTC times.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import urllib.request
from datetime import date, datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "research/data/EXP-041-free-macro-consensus-v0.3.json"
SRC_AUDIT = ROOT / "research/results/EXP-041-free-macro-consensus-scope-audit-v0.3.json"
OUT = ROOT / "research/data/EXP-041-official-release-time-map-v0.1.json"
RESULT = ROOT / "research/results/EXP-041-official-release-time-reconciliation-v0.1.json"

UA = "Mozilla/5.0 (compatible; target-first-trading-system-exp041/0.1; official-source verification)"
NY = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")

CENSUS_SCHEDULE = "https://www.census.gov/retail/release_schedule.html"
BEA_2025 = "https://www.bea.gov/news/schedule/full-2025"
BEA_2026 = "https://www.bea.gov/news/schedule/full-2026"

EXPECTED_COUNTS = {
    "EMPLOYMENT": 11,
    "CPI": 11,
    "PPI": 11,
    "RETAIL": 12,
    "GDP_PCE": 15,
    "FOMC": 8,
}


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        if int(r.status) != 200:
            raise RuntimeError(f"HTTP {r.status} for {url}")
        return r.read()


def text(raw: bytes) -> str:
    s = raw.decode("utf-8", "replace")
    s = re.sub(r"<script\b[^>]*>.*?</script>", " ", s, flags=re.I|re.S)
    s = re.sub(r"<style\b[^>]*>.*?</style>", " ", s, flags=re.I|re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"&nbsp;|&#160;", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def local_to_utc(d: date, hh: int, mm: int) -> str:
    dt = datetime.combine(d, time(hh, mm), tzinfo=NY)
    return dt.astimezone(UTC).isoformat().replace("+00:00", "Z")


def mmddyyyy(d: date) -> str:
    return d.strftime("%m%d%Y")


def date_forms(d: date) -> list[str]:
    return [
        d.strftime("%B %-d, %Y"),
        d.strftime("%B %d, %Y").replace(" 0", " "),
        d.strftime("%b %-d, %Y"),
    ]


def contains_date(t: str, d: date) -> bool:
    low = t.lower()
    return any(x.lower() in low for x in date_forms(d))


def bls_url(family: str, d: date) -> str:
    prefix = {"EMPLOYMENT":"empsit","CPI":"cpi","PPI":"ppi"}[family]
    return f"https://www.bls.gov/news.release/archives/{prefix}_{mmddyyyy(d)}.htm"


def fed_url(d: date) -> str:
    return f"https://www.federalreserve.gov/monetarypolicy/monetary{d.strftime('%Y%m%d')}a.htm"


def main() -> int:
    if not SRC.exists() or not SRC_AUDIT.exists():
        raise SystemExit("frozen v0.3 inputs missing")

    audit = json.loads(SRC_AUDIT.read_text())
    expected_sha = audit["normalized_dataset"]["sha256"]
    observed_sha = sha256_file(SRC)
    if observed_sha != expected_sha:
        raise SystemExit(f"v0.3 SHA mismatch: {observed_sha} != {expected_sha}")
    if not audit["consensus_layer_gate_pass"]:
        raise SystemExit("v0.3 consensus gate did not pass")
    if audit["protected_periods"]["jul_aug_2026_loaded"] or audit["protected_periods"]["sep_2026_loaded"]:
        raise SystemExit("protected-period flag in input audit")

    src = json.loads(SRC.read_text())
    blocks = src["provisional_event_blocks"]

    # Fetch shared official schedules once.
    census_raw = fetch(CENSUS_SCHEDULE)
    census_text = text(census_raw)
    bea25_raw = fetch(BEA_2025)
    bea25_text = text(bea25_raw)
    bea26_raw = fetch(BEA_2026)
    bea26_text = text(bea26_raw)

    schedule_meta = {
        "census_retail": {
            "url": CENSUS_SCHEDULE,
            "sha256": sha256_bytes(census_raw),
            "bytes": len(census_raw),
        },
        "bea_2025": {
            "url": BEA_2025,
            "sha256": sha256_bytes(bea25_raw),
            "bytes": len(bea25_raw),
        },
        "bea_2026": {
            "url": BEA_2026,
            "sha256": sha256_bytes(bea26_raw),
            "bytes": len(bea26_raw),
        },
    }

    mapped = []
    errors = []

    for b in blocks:
        fam = b["family"]
        d = date.fromisoformat(b["event_date"])
        row = {
            "block_id": b["block_id"],
            "family": fam,
            "event_date": b["event_date"],
            "official_local_timezone": "America/New_York",
            "source_date_verified": False,
            "source_time_verified": False,
        }

        try:
            if fam in {"EMPLOYMENT","CPI","PPI"}:
                url = bls_url(fam, d)
                raw = fetch(url)
                t = text(raw)
                date_ok = contains_date(t, d)
                time_ok = bool(re.search(r"8:30\s*a\.m\.\s*\(ET\)", t, flags=re.I))
                row.update({
                    "official_authority": "U.S. Bureau of Labor Statistics",
                    "official_source_url": url,
                    "official_source_sha256": sha256_bytes(raw),
                    "official_local_release_time": "08:30",
                    "official_release_timestamp_utc": local_to_utc(d, 8, 30),
                    "source_date_verified": date_ok,
                    "source_time_verified": time_ok,
                })

            elif fam == "RETAIL":
                date_ok = contains_date(census_text, d)
                # Official schedule states Advance Monthly Retail Trade at 8:30 am.
                time_ok = bool(re.search(r"Advance Monthly Retail Trade Report", census_text, re.I)) and bool(re.search(r"8:30\s*am", census_text, re.I))
                row.update({
                    "official_authority": "U.S. Census Bureau",
                    "official_source_url": CENSUS_SCHEDULE,
                    "official_source_sha256": schedule_meta["census_retail"]["sha256"],
                    "official_local_release_time": "08:30",
                    "official_release_timestamp_utc": local_to_utc(d, 8, 30),
                    "source_date_verified": date_ok,
                    "source_time_verified": time_ok,
                })

            elif fam == "GDP_PCE":
                sched_text = bea25_text if d.year == 2025 else bea26_text
                meta_key = "bea_2025" if d.year == 2025 else "bea_2026"
                date_ok = contains_date(sched_text, d)
                # Require an 8:30 AM News release on that official schedule date.
                # Date+time+News are verified globally from the first-party schedule;
                # component-level release identity is checked in Phase B actual reconciliation.
                pos_candidates = [sched_text.lower().find(x.lower()) for x in date_forms(d)]
                pos_candidates = [p for p in pos_candidates if p >= 0]
                if pos_candidates:
                    p = min(pos_candidates)
                    window = sched_text[max(0,p-200):p+700]
                else:
                    window = ""
                time_ok = bool(re.search(r"8:30\s*AM", window, re.I)) and bool(re.search(r"News", window, re.I))
                row.update({
                    "official_authority": "U.S. Bureau of Economic Analysis",
                    "official_source_url": schedule_meta[meta_key]["url"],
                    "official_source_sha256": schedule_meta[meta_key]["sha256"],
                    "official_local_release_time": "08:30",
                    "official_release_timestamp_utc": local_to_utc(d, 8, 30),
                    "source_date_verified": date_ok,
                    "source_time_verified": time_ok,
                })

            elif fam == "FOMC":
                url = fed_url(d)
                raw = fetch(url)
                t = text(raw)
                date_ok = contains_date(t, d)
                time_ok = bool(re.search(r"(?:For release at\s*)?2:00\s*p\.m\.\s*E(?:D|S)T", t, flags=re.I))
                row.update({
                    "official_authority": "Federal Reserve Board",
                    "official_source_url": url,
                    "official_source_sha256": sha256_bytes(raw),
                    "official_local_release_time": "14:00",
                    "official_release_timestamp_utc": local_to_utc(d, 14, 0),
                    "source_date_verified": date_ok,
                    "source_time_verified": time_ok,
                })
            else:
                raise RuntimeError(f"unsupported family {fam}")

            if not row["source_date_verified"] or not row["source_time_verified"]:
                errors.append({
                    "block_id": b["block_id"],
                    "family": fam,
                    "event_date": b["event_date"],
                    "reason": "official date/time marker not verified",
                })

            mapped.append(row)

        except Exception as exc:
            row["error_type"] = type(exc).__name__
            mapped.append(row)
            errors.append({
                "block_id": b["block_id"],
                "family": fam,
                "event_date": b["event_date"],
                "reason": type(exc).__name__,
            })

    family_counts = {}
    resolved_counts = {}
    for fam in EXPECTED_COUNTS:
        family_counts[fam] = sum(1 for x in mapped if x["family"] == fam)
        resolved_counts[fam] = sum(
            1 for x in mapped
            if x["family"] == fam and x.get("source_date_verified") and x.get("source_time_verified") and x.get("official_release_timestamp_utc")
        )

    gate = {
        "input_v03_sha_verified": True,
        "all_blocks_mapped": len(mapped) == len(blocks),
        "no_reconciliation_errors": len(errors) == 0,
        "all_blocks_have_official_timestamp": all(x.get("official_release_timestamp_utc") for x in mapped),
        "all_dates_verified": all(x.get("source_date_verified") for x in mapped),
        "all_times_verified": all(x.get("source_time_verified") for x in mapped),
        "family_counts_match_frozen_v03": all(family_counts[f] == EXPECTED_COUNTS[f] for f in EXPECTED_COUNTS),
        "all_family_blocks_resolved": all(resolved_counts[f] == EXPECTED_COUNTS[f] for f in EXPECTED_COUNTS),
        "no_market_data_or_outcomes_loaded": True,
        "protected_periods_sealed": True,
    }
    passed = all(gate.values())

    payload = {
        "stage": "EXP-041 official release-time map v0.1",
        "input_consensus_dataset": str(SRC.relative_to(ROOT)),
        "input_consensus_sha256": observed_sha,
        "official_schedule_sources": schedule_meta,
        "blocks": mapped,
        "protected_periods": src["protected_periods"],
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    out_sha = sha256_file(OUT)

    result = {
        "stage": "EXP-041 official release-time reconciliation v0.1",
        "tested_repository_sha": os.environ.get("GITHUB_SHA"),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "input_v03": {
            "path": str(SRC.relative_to(ROOT)),
            "expected_sha256": expected_sha,
            "observed_sha256": observed_sha,
        },
        "official_time_map": {
            "path": str(OUT.relative_to(ROOT)),
            "sha256": out_sha,
            "blocks": len(mapped),
        },
        "family_counts": family_counts,
        "resolved_family_counts": resolved_counts,
        "errors": errors,
        "gate": gate,
        "release_time_reconciliation_pass": passed,
        "official_actual_reconciliation_complete": False,
        "network_access_used": True,
        "market_data_loaded": False,
        "target_labels_calculated": False,
        "pnl_calculated": False,
        "scientific_outcomes_calculated": False,
        "protected_periods": src["protected_periods"],
        "disposition": (
            "OFFICIAL_RELEASE_TIME_RECONCILIATION_PASS_ACTUAL_VALUES_REQUIRED"
            if passed else
            "OFFICIAL_RELEASE_TIME_RECONCILIATION_FAILED_REPAIR_SOURCE_MAPPING"
        ),
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    print(json.dumps({
        "pass": passed,
        "blocks": len(mapped),
        "family_counts": family_counts,
        "resolved_family_counts": resolved_counts,
        "errors": len(errors),
        "disposition": result["disposition"],
    }, indent=2))
    return 0 if passed else 2


if __name__ == "__main__":
    sys.exit(main())
