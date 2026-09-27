#!/usr/bin/env python3
"""EXP-041 full free macro consensus acquisition v0.2.

Zero-outcome scope correction:
- include Non-Farm Employment Change/NFP aliases;
- restrict FOMC to genuine policy rows;
- provisional event block key = date + family only.
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
from datetime import date, timedelta
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research/results"
DATA_OUT = ROOT / "research/data"
OUT.mkdir(parents=True, exist_ok=True)
DATA_OUT.mkdir(parents=True, exist_ok=True)

RESULT = OUT / "EXP-041-free-macro-consensus-acquisition-audit-v0.2.json"
NORMALIZED = DATA_OUT / "EXP-041-free-macro-consensus-v0.2.json"

START = date(2025, 7, 1)
END = date(2026, 6, 29)
UA = "Mozilla/5.0 (compatible; target-first-trading-system-exp041/0.2; public-data research)"
MONTHS = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]

FAMILY_PATTERNS = {
    "EMPLOYMENT": [
        r"non.?farm.*employment.*change",
        r"nonfarm.*employment.*change",
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
}
NUMERIC_FAMILIES = ["EMPLOYMENT","CPI","PPI","RETAIL","GDP_PCE"]
FOMC_POLICY_NAMES = {
    "fomc statement",
    "federal funds rate",
    "fomc economic projections",
}


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
    e = clean_text(event).lower()
    if e in FOMC_POLICY_NAMES:
        return "FOMC"
    for fam in ["PPI","CPI","RETAIL","EMPLOYMENT","GDP_PCE"]:
        if any(re.search(p, e, re.I) for p in FAMILY_PATTERNS[fam]):
            return fam
    return None


def parse_date_text(raw: str, current: date | None) -> date | None:
    raw = clean_text(raw)
    if not raw:
        return current
    m = re.search(r"(?i)\b(" + "|".join(MONTHS) + r")[a-z]*\s*(\d{1,2})\b", raw)
    if not m:
        return current
    month = MONTHS.index(m.group(1)[:3].lower()) + 1
    day = int(m.group(2))
    year = 2025 if month >= 7 else 2026
    return date(year, month, day)


def cell_text(row, keywords: list[str]) -> str:
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
    el = row.find(attrs={"data-event-id": True})
    if el:
        return str(el.get("data-event-id"))
    return ""


def candidate_rows(soup: BeautifulSoup):
    rows = soup.select("tr.calendar__row, tr.calendar_row, tr[data-event-id], .calendar__row, .calendar_row")
    return rows if rows else soup.find_all("tr")


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

        if not event or currency.upper() != "USD":
            continue

        family = classify(event)
        if family is None or current_date is None or not (START <= current_date <= END):
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


def main() -> int:
    pages_meta, records, page_errors = [], [], []
    columns_all = True

    for page in build_pages():
        try:
            raw = fetch(page["url"])
            sha = hashlib.sha256(raw).hexdigest()
            soup = BeautifulSoup(raw, "html.parser")
            page_text = clean_text(soup.get_text(" ", strip=True))
            cols = {c: (c.lower() in page_text.lower()) for c in ("Actual","Forecast","Previous")}
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
            page_errors.append({**page, "error_type": type(exc).__name__})
            pages_meta.append({**page, "http_status": None, "targeted_rows": 0, "error_type": type(exc).__name__})

    unique = {}
    for r in records:
        key = (
            r["event_id"], r["event_date"], r["family"], r["event_name"],
            r["actual_text"], r["forecast_text"], r["previous_text"]
        )
        unique[key] = r
    records = sorted(unique.values(), key=lambda r: (r["event_date"], r["family"], r["event_name"]))

    blocks = defaultdict(list)
    for r in records:
        blocks[f'{r["event_date"]}|{r["family"]}'].append(r)

    block_rows = []
    family_blocks = Counter()
    surprise_blocks = 0
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
            "component_event_ids": [r["event_id"] for r in rs if r["event_id"]],
            "component_names": [r["event_name"] for r in rs],
        })

    nfp_rows = [
        r for r in records
        if r["family"] == "EMPLOYMENT" and re.search(r"(?i)non.?farm.*(?:employment|payroll)", r["event_name"])
    ]

    normalized_payload = {
        "stage": "EXP-041 free macro consensus normalized layer v0.2",
        "supersedes": "research/data/EXP-041-free-macro-consensus-v0.1.json",
        "source_role": {
            "ForexFactory_Forecast": "PUBLIC_CALENDAR_CONSENSUS_FF",
            "ForexFactory_Actual": "DIAGNOSTIC_PENDING_OFFICIAL_RECONCILIATION",
            "ForexFactory_Time": "DIAGNOSTIC_PENDING_OFFICIAL_RECONCILIATION",
        },
        "allowed_interval": [START.isoformat(), END.isoformat()],
        "scope_corrections": {
            "nfp_alias_added": True,
            "fomc_policy_only": True,
            "provisional_block_key": "event_date+family",
        },
        "records": records,
        "provisional_event_blocks": block_rows,
        "protected_periods": {"jul_aug_2026_loaded": False, "sep_2026_loaded": False},
    }
    NORMALIZED.write_text(json.dumps(normalized_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    normalized_sha = hashlib.sha256(NORMALIZED.read_bytes()).hexdigest()

    gate = {
        "all_requested_pages_http_200": len(page_errors) == 0,
        "all_pages_show_actual_forecast_previous_columns": columns_all,
        "no_retained_rows_after_2026_06_29": all(START <= date.fromisoformat(r["event_date"]) <= END for r in records),
        "nfp_component_present": len(nfp_rows) > 0,
        "all_numeric_families_present": all(family_blocks[f] > 0 for f in NUMERIC_FAMILIES),
        "provisional_blocks_ge_40": len(block_rows) >= 40,
        "surprise_bearing_blocks_ge_30": surprise_blocks >= 30,
        "each_numeric_family_blocks_ge_8": all(family_blocks[f] >= 8 for f in NUMERIC_FAMILIES),
        "no_market_data_or_outcomes_loaded": True,
        "protected_periods_sealed": True,
    }
    consensus_pass = all(gate.values())

    result = {
        "stage": "EXP-041 full free macro consensus acquisition / Gate-A coverage audit v0.2",
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
        "nfp_component_rows": len(nfp_rows),
        "fomc_policy_event_dates": family_blocks["FOMC"],
        "fomc_timing_only_if_lt_6": family_blocks["FOMC"] < 6,
        "gate": gate,
        "consensus_layer_gate_pass": consensus_pass,
        "official_reconciliation_complete": False,
        "target_labels_calculated": False,
        "pnl_calculated": False,
        "scientific_outcomes_calculated": False,
        "market_data_loaded": False,
        "protected_periods": {"jul_aug_2026_loaded": False, "sep_2026_loaded": False},
        "disposition": (
            "FREE_CONSENSUS_V02_SCOPE_CORRECTED_GATE_PASS_OFFICIAL_RECONCILIATION_REQUIRED"
            if consensus_pass else
            "FREE_CONSENSUS_V02_SCOPE_CORRECTION_FAILED"
        ),
    }

    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "consensus_layer_gate_pass": consensus_pass,
        "records": len(records),
        "provisional_blocks": len(block_rows),
        "surprise_blocks": surprise_blocks,
        "family_blocks": dict(sorted(family_blocks.items())),
        "nfp_component_rows": len(nfp_rows),
        "fomc_policy_event_dates": family_blocks["FOMC"],
        "disposition": result["disposition"],
    }, indent=2))
    return 0 if consensus_pass else 2


if __name__ == "__main__":
    sys.exit(main())
