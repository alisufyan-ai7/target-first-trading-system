#!/usr/bin/env python3
"""EXP-041 full free macro consensus acquisition / Gate-A coverage audit.

Development only. No market data, target labels, P&L or protected periods.
"""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research/results"
DATA_OUT = ROOT / "research/data"
OUT.mkdir(parents=True, exist_ok=True)
DATA_OUT.mkdir(parents=True, exist_ok=True)

RESULT = OUT / "EXP-041-free-macro-consensus-acquisition-audit-v0.1.json"
NORMALIZED = DATA_OUT / "EXP-041-free-macro-consensus-v0.1.json"

START = date(2025, 7, 1)
END = date(2026, 6, 29)
UA = "Mozilla/5.0 (compatible; target-first-trading-system-exp041/0.1; public-data research)"

MONTHS = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]

FAMILY_PATTERNS = {
    "EMPLOYMENT": [
        r"non.?farm.*payroll",
        r"nonfarm.*payroll",
        r"unemployment\s+rate",
        r"average\s+hourly\s+earnings",
    ],
    "CPI": [
        r"\bcpi\b",
        r"core\s+cpi",
        r"core\s+inflation",
        r"\binflation\s+rate\b",
    ],
    "PPI": [
        r"\bppi\b",
        r"producer\s+price",
    ],
    "RETAIL": [
        r"retail\s+sales",
    ],
    "GDP_PCE": [
        r"\bgdp\b",
        r"gdp\s+price",
        r"\bpce\b",
        r"personal\s+income",
        r"personal\s+spending",
    ],
    "FOMC": [
        r"\bfomc\b",
        r"fed\s+funds",
        r"federal\s+funds",
        r"fed\s+interest\s+rate",
    ],
}
NUMERIC_FAMILIES = ["EMPLOYMENT","CPI","PPI","RETAIL","GDP_PCE"]


def ff_token(d: date) -> str:
    return f"{MONTHS[d.month-1]}{d.day:02d}.{d.year}"


def monday_on_or_before(d: date) -> date:
    return d - timedelta(days=d.weekday())


def build_pages() -> list[dict]:
    pages = []
    d = monday_on_or_before(START)
    last_week = date(2026, 6, 22)
    while d <= last_week:
        pages.append({
            "kind": "week",
            "label": d.isoformat(),
            "url": f"https://www.forexfactory.com/calendar?week={ff_token(d)}",
        })
        d += timedelta(days=7)
    pages.append({
        "kind": "day",
        "label": "2026-06-29",
        "url": "https://www.forexfactory.com/calendar?day=jun29.2026",
    })
    return pages


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        if int(r.status) != 200:
            raise RuntimeError(f"HTTP {r.status}")
        return r.read()


def clean_text(s: str | None) -> str:
    if not s:
        return ""
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def classify(event: str) -> str | None:
    text = event.lower()
    # Resolve overlap conservatively: PPI before CPI; FOMC explicit; GDP/PCE explicit.
    order = ["FOMC","PPI","CPI","RETAIL","EMPLOYMENT","GDP_PCE"]
    for fam in order:
        if any(re.search(p, text, re.I) for p in FAMILY_PATTERNS[fam]):
            return fam
    return None


def parse_date_text(raw: str, current: date | None) -> date | None:
    raw = clean_text(raw)
    if not raw:
        return current
    # Common FF renderings: "Tue Jul 1", "Jul 1", "TueJul 1"
    m = re.search(r"(?i)\b(" + "|".join(MONTHS) + r")[a-z]*\s*(\d{1,2})\b", raw)
    if not m:
        return current
    month = MONTHS.index(m.group(1)[:3].lower()) + 1
    day = int(m.group(2))
    # Acquisition spans Jul2025-Jun2026.
    year = 2025 if month >= 7 else 2026
    return date(year, month, day)


def cell_text(row, keywords: list[str]) -> str:
    # Search class names first.
    for el in row.find_all(["td","div","span"]):
        classes = " ".join(el.get("class", []))
        data_title = str(el.get("data-title", ""))
        aria = str(el.get("aria-label", ""))
        hay = " ".join([classes, data_title, aria]).lower()
        if any(k in hay for k in keywords):
            txt = clean_text(el.get_text(" ", strip=True))
            if txt:
                return txt
    return ""


def row_event_id(row) -> str:
    for key in ("data-event-id","data-eventid","data-id","id"):
        v = row.get(key)
        if v:
            s = str(v)
            m = re.search(r"(\d{4,})", s)
            return m.group(1) if m else s[:100]
    # Search descendants.
    el = row.find(attrs={"data-event-id": True})
    if el:
        return str(el.get("data-event-id"))
    return ""


def candidate_rows(soup: BeautifulSoup):
    rows = soup.select("tr.calendar__row, tr.calendar_row, tr[data-event-id], .calendar__row, .calendar_row")
    # Fallback: any tr containing recognizable actual/forecast/previous/event cells.
    if not rows:
        rows = soup.find_all("tr")
    return rows


def parse_page(raw: bytes, url: str, page_sha: str) -> list[dict]:
    soup = BeautifulSoup(raw, "html.parser")
    out = []
    current_date = None

    for row in candidate_rows(soup):
        date_txt = cell_text(row, ["date"])
        current_date = parse_date_text(date_txt, current_date)

        currency = cell_text(row, ["currency"])
        event = cell_text(row, ["event"])
        time_txt = cell_text(row, ["time"])
        actual = cell_text(row, ["actual"])
        forecast = cell_text(row, ["forecast"])
        previous = cell_text(row, ["previous"])

        # Fallback based on structured text if event class changed.
        full = clean_text(row.get_text(" ", strip=True))
        if not event:
            # Avoid guessing if no event-specific cell is available.
            continue

        if currency.upper() != "USD":
            continue

        family = classify(event)
        if family is None or current_date is None:
            continue
        if not (START <= current_date <= END):
            continue

        out.append({
            "source": "ForexFactory",
            "source_page_url": url,
            "source_page_sha256": page_sha,
            "event_id": row_event_id(row),
            "event_date": current_date.isoformat(),
            "displayed_time": time_txt,
            "currency": "USD",
            "family": family,
            "event_name": event,
            "actual_text": actual,
            "forecast_text": forecast,
            "previous_text": previous,
            "has_actual": bool(actual),
            "has_forecast": bool(forecast),
            "has_previous": bool(previous),
        })
    return out


def block_key(row: dict) -> str:
    t = row["displayed_time"].lower().strip()
    if not t:
        t = "TIME_UNRESOLVED"
    return "|".join([row["event_date"], row["family"], t])


def main() -> int:
    pages_meta = []
    records = []
    page_errors = []
    columns_all = True

    for page in build_pages():
        try:
            raw = fetch(page["url"])
            sha = hashlib.sha256(raw).hexdigest()
            text = clean_text(BeautifulSoup(raw, "html.parser").get_text(" ", strip=True))
            cols = {c: (c.lower() in text.lower()) for c in ("Actual","Forecast","Previous")}
            columns_all = columns_all and all(cols.values())
            parsed = parse_page(raw, page["url"], sha)
            pages_meta.append({
                **page,
                "http_status": 200,
                "bytes": len(raw),
                "sha256": sha,
                "columns_present": cols,
                "targeted_rows": len(parsed),
            })
            records.extend(parsed)
        except Exception as exc:
            page_errors.append({
                **page,
                "error_type": type(exc).__name__,
            })
            pages_meta.append({
                **page,
                "http_status": None,
                "targeted_rows": 0,
                "error_type": type(exc).__name__,
            })

    # Deduplicate exact repeated rows caused by flexible selectors.
    unique = {}
    for r in records:
        key = (
            r["event_id"],
            r["event_date"],
            r["displayed_time"],
            r["family"],
            r["event_name"],
            r["actual_text"],
            r["forecast_text"],
            r["previous_text"],
        )
        unique[key] = r
    records = sorted(unique.values(), key=lambda r: (r["event_date"], r["displayed_time"], r["family"], r["event_name"]))

    blocks = defaultdict(list)
    for r in records:
        blocks[block_key(r)].append(r)

    block_rows = []
    family_blocks = Counter()
    surprise_blocks = 0
    for key, rs in sorted(blocks.items()):
        fam = rs[0]["family"]
        surprise = any(r["has_actual"] and r["has_forecast"] for r in rs)
        if surprise:
            surprise_blocks += 1
        family_blocks[fam] += 1
        block_rows.append({
            "block_id": key,
            "event_date": rs[0]["event_date"],
            "displayed_time": rs[0]["displayed_time"],
            "family": fam,
            "component_count": len(rs),
            "surprise_bearing_provisional": surprise,
            "component_event_ids": [r["event_id"] for r in rs if r["event_id"]],
            "component_names": [r["event_name"] for r in rs],
        })

    duplicate_event_ids = []
    id_counter = Counter(r["event_id"] for r in records if r["event_id"])
    for eid, n in id_counter.items():
        if n > 1:
            # Same FF event id may still repeat due to component/rendering quirks; report, do not silently ignore.
            duplicate_event_ids.append({"event_id": eid, "count": n})

    normalized_payload = {
        "stage": "EXP-041 free macro consensus normalized layer v0.1",
        "source_role": {
            "ForexFactory_Forecast": "PUBLIC_CALENDAR_CONSENSUS_FF",
            "ForexFactory_Actual": "DIAGNOSTIC_PENDING_OFFICIAL_RECONCILIATION",
            "ForexFactory_Time": "DIAGNOSTIC_PENDING_OFFICIAL_RECONCILIATION",
        },
        "allowed_interval": [START.isoformat(), END.isoformat()],
        "records": records,
        "provisional_event_blocks": block_rows,
        "protected_periods": {
            "jul_aug_2026_loaded": False,
            "sep_2026_loaded": False,
        },
    }
    NORMALIZED.write_text(json.dumps(normalized_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    normalized_sha = hashlib.sha256(NORMALIZED.read_bytes()).hexdigest()

    no_future = all(START <= date.fromisoformat(r["event_date"]) <= END for r in records)
    numeric_counts_ok = all(family_blocks[f] >= 8 for f in NUMERIC_FAMILIES)

    gate = {
        "all_requested_pages_http_200": len(page_errors) == 0,
        "all_pages_show_actual_forecast_previous_columns": columns_all,
        "no_retained_rows_after_2026_06_29": no_future,
        "all_numeric_families_present": all(family_blocks[f] > 0 for f in NUMERIC_FAMILIES),
        "provisional_blocks_ge_40": len(block_rows) >= 40,
        "surprise_bearing_blocks_ge_30": surprise_blocks >= 30,
        "each_numeric_family_blocks_ge_8": numeric_counts_ok,
        "no_market_data_or_outcomes_loaded": True,
        "protected_periods_sealed": True,
    }
    pre_reconciliation_pass = all(gate.values())

    result = {
        "stage": "EXP-041 full free macro consensus acquisition / Gate-A coverage audit v0.1",
        "tested_repository_sha": os.environ.get("GITHUB_SHA"),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "source": "Forex Factory historical calendar",
        "allowed_interval": [START.isoformat(), END.isoformat()],
        "requested_pages": pages_meta,
        "page_errors": page_errors,
        "normalized_dataset": {
            "path": str(NORMALIZED.relative_to(ROOT)),
            "sha256": normalized_sha,
            "records": len(records),
        },
        "provisional_independent_event_blocks": len(block_rows),
        "surprise_bearing_provisional_blocks": surprise_blocks,
        "family_block_counts": dict(sorted(family_blocks.items())),
        "fomc_timing_only_if_lt_6": family_blocks["FOMC"] < 6,
        "duplicate_event_ids_reported": duplicate_event_ids,
        "gate": gate,
        "consensus_layer_gate_pass": pre_reconciliation_pass,
        "official_reconciliation_complete": False,
        "target_labels_calculated": False,
        "pnl_calculated": False,
        "scientific_outcomes_calculated": False,
        "market_data_loaded": False,
        "protected_periods": {
            "jul_aug_2026_loaded": False,
            "sep_2026_loaded": False,
        },
        "disposition": (
            "FREE_CONSENSUS_LAYER_GATE_A_COVERAGE_PASS_OFFICIAL_RECONCILIATION_REQUIRED"
            if pre_reconciliation_pass
            else "FREE_CONSENSUS_LAYER_INSUFFICIENT_OR_PARSER_REPAIR_REQUIRED"
        ),
    }

    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({
        "consensus_layer_gate_pass": pre_reconciliation_pass,
        "records": len(records),
        "provisional_blocks": len(block_rows),
        "surprise_blocks": surprise_blocks,
        "family_blocks": dict(sorted(family_blocks.items())),
        "pages_failed": len(page_errors),
        "disposition": result["disposition"],
    }, indent=2))

    return 0 if pre_reconciliation_pass else 2


if __name__ == "__main__":
    sys.exit(main())
