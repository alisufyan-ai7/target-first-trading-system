#!/usr/bin/env python3
"""EXP-041 Trading Economics PIT access/provenance preflight.

Zero market labels, zero P&L, zero protected-period data.
Only non-value schema/coverage metadata are checkpointed.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research/results"
OUT.mkdir(parents=True, exist_ok=True)
RESULT_PATH = OUT / "EXP-041-macro-pit-access-preflight-v0.1.json"

START = "2026-03-01"
END = "2026-06-29"
BASE = (
    "https://api.tradingeconomics.com/calendar/country/"
    "united%20states/2026-03-01/2026-06-29"
)

FAMILY_PATTERNS = {
    "EMPLOYMENT": [
        r"non\s*farm\s*payroll",
        r"nonfarm\s*payroll",
        r"unemployment\s*rate",
        r"average\s*hourly\s*earnings",
    ],
    "CPI": [
        r"\bcpi\b",
        r"core\s+inflation\s+rate",
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
        r"gdp\s+growth",
        r"gdp\s+price",
        r"\bpce\b",
        r"personal\s+income",
        r"personal\s+spending",
    ],
    "FOMC": [
        r"\bfomc\b",
        r"fed\s+interest\s+rate",
        r"federal\s+reserve.*(?:rate|policy)",
    ],
}
NUMERIC_FAMILIES = ["EMPLOYMENT", "CPI", "PPI", "RETAIL", "GDP_PCE"]
REQUIRED_KEYS = ["CalendarId", "Date", "Country", "Category", "Event", "LastUpdate"]


def nonempty(v) -> bool:
    return v is not None and str(v).strip() != ""


def classify(row: dict) -> set[str]:
    text = " ".join(
        str(row.get(k, "") or "")
        for k in ("Category", "Event", "Ticker", "Symbol")
    ).lower()
    found = set()
    for family, patterns in FAMILY_PATTERNS.items():
        if any(re.search(p, text, flags=re.I) for p in patterns):
            found.add(family)
    return found


def sanitized_http_error(exc: urllib.error.HTTPError) -> dict:
    body = ""
    try:
        body = exc.read(2048).decode("utf-8", "replace")
    except Exception:
        pass
    # Do not retain URLs or arbitrary long vendor payloads.
    return {
        "http_status": int(exc.code),
        "body_hint": re.sub(r"(?i)(api[_ -]?key|token|secret)[^,}\n]*", r"\1=[REDACTED]", body)[:500],
    }


def write_result(result: dict) -> None:
    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def base_result() -> dict:
    return {
        "stage": "EXP-041 macro PIT access/provenance preflight v0.1",
        "tested_repository_sha": os.environ.get("GITHUB_SHA"),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "source": "Trading Economics Economic Calendar API",
        "query_scope": {
            "country": "United States",
            "start": START,
            "end": END,
        },
        "credential_present": False,
        "http_success": False,
        "response_rows": 0,
        "response_sha256": None,
        "raw_vendor_payload_committed": False,
        "target_labels_calculated": False,
        "pnl_calculated": False,
        "scientific_outcomes_calculated": False,
        "market_data_loaded": False,
        "protected_periods": {
            "jul_aug_2026_loaded": False,
            "sep_2026_loaded": False,
        },
        "families": {},
        "gate": {},
        "preflight_pass": False,
        "disposition": None,
    }


def main() -> int:
    result = base_result()
    key = os.environ.get("TRADING_ECONOMICS_API_KEY", "").strip()

    if not key:
        result["disposition"] = "CREDENTIAL_REQUIRED"
        result["gate"] = {"credential_present": False}
        write_result(result)
        print(json.dumps({"preflight_pass": False, "disposition": result["disposition"]}, indent=2))
        return 2

    result["credential_present"] = True
    query = urllib.parse.urlencode({"c": key, "f": "json"})
    request = urllib.request.Request(
        BASE + "?" + query,
        headers={"User-Agent": "target-first-trading-system-exp041/0.1"},
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            status = int(response.status)
            raw = response.read()
    except urllib.error.HTTPError as exc:
        result["api_error"] = sanitized_http_error(exc)
        result["disposition"] = (
            "PIT_OR_HISTORICAL_ACCESS_REQUIRED"
            if exc.code in (401, 402, 403, 404, 429)
            else "TRADING_ECONOMICS_API_REQUEST_FAILED"
        )
        result["gate"] = {"credential_present": True, "http_success": False}
        write_result(result)
        print(json.dumps({"preflight_pass": False, "disposition": result["disposition"]}, indent=2))
        return 3
    except Exception as exc:
        result["api_error"] = {"type": type(exc).__name__}
        result["disposition"] = "TRADING_ECONOMICS_API_REQUEST_FAILED"
        result["gate"] = {"credential_present": True, "http_success": False}
        write_result(result)
        print(json.dumps({"preflight_pass": False, "disposition": result["disposition"]}, indent=2))
        return 4

    result["http_status"] = status
    result["http_success"] = 200 <= status < 300
    result["response_sha256"] = hashlib.sha256(raw).hexdigest()

    try:
        rows = json.loads(raw)
    except json.JSONDecodeError:
        result["disposition"] = "TRADING_ECONOMICS_NON_JSON_RESPONSE"
        result["gate"] = {"credential_present": True, "http_success": result["http_success"], "json_list": False}
        write_result(result)
        return 5

    if isinstance(rows, dict) and any(k in rows for k in ("error", "Error", "message", "Message")):
        result["api_error"] = {"response_object_keys": sorted(str(k) for k in rows.keys())[:20]}
        result["disposition"] = "PIT_OR_HISTORICAL_ACCESS_REQUIRED"
        result["gate"] = {"credential_present": True, "http_success": result["http_success"], "json_list": False}
        write_result(result)
        return 6

    if not isinstance(rows, list):
        result["disposition"] = "TRADING_ECONOMICS_UNEXPECTED_SCHEMA"
        result["gate"] = {"credential_present": True, "http_success": result["http_success"], "json_list": False}
        write_result(result)
        return 7

    result["response_rows"] = len(rows)

    family_rows = defaultdict(list)
    max_date = None
    out_of_scope = 0

    for row in rows:
        if not isinstance(row, dict):
            continue
        date_text = str(row.get("Date", "") or "")
        if date_text:
            try:
                dt = datetime.fromisoformat(date_text.replace("Z", "+00:00"))
                day = dt.date().isoformat()
                max_date = max(max_date, day) if max_date else day
                if day > END:
                    out_of_scope += 1
            except ValueError:
                pass
        for family in classify(row):
            family_rows[family].append(row)

    families = {}
    for family in FAMILY_PATTERNS:
        rs = family_rows.get(family, [])
        required_schema_rows = sum(
            all(nonempty(r.get(k)) for k in REQUIRED_KEYS)
            for r in rs
        )
        actual_forecast_rows = sum(
            nonempty(r.get("Actual")) and nonempty(r.get("Forecast"))
            for r in rs
        )
        source_rows = sum(
            nonempty(r.get("Source")) or nonempty(r.get("SourceURL"))
            for r in rs
        )

        # No Actual/Forecast/Previous numeric values are persisted.
        samples = [
            {
                "CalendarId": str(r.get("CalendarId", "")),
                "Date": str(r.get("Date", "")),
                "Category": str(r.get("Category", "")),
                "Event": str(r.get("Event", "")),
                "has_actual": nonempty(r.get("Actual")),
                "has_forecast_consensus": nonempty(r.get("Forecast")),
                "has_previous": nonempty(r.get("Previous")),
                "has_revised_field": "Revised" in r,
                "has_source_provenance": nonempty(r.get("Source")) or nonempty(r.get("SourceURL")),
            }
            for r in rs[:5]
        ]

        families[family] = {
            "matched_rows": len(rs),
            "rows_with_required_schema": required_schema_rows,
            "rows_with_actual_and_forecast": actual_forecast_rows,
            "rows_with_source_provenance": source_rows,
            "samples_without_numeric_values": samples,
        }

    result["families"] = families
    result["max_returned_event_date"] = max_date
    result["out_of_scope_rows_after_end"] = out_of_scope

    targeted = [r for fam in family_rows.values() for r in fam]
    targeted_schema_ok = bool(targeted) and all(
        all(nonempty(r.get(k)) for k in REQUIRED_KEYS)
        for r in targeted
    )
    source_provenance_any = any(
        nonempty(r.get("Source")) or nonempty(r.get("SourceURL"))
        for r in targeted
    )

    gate = {
        "credential_present": True,
        "http_success": result["http_success"],
        "json_nonempty_list": len(rows) > 0,
        "no_rows_after_frozen_end": out_of_scope == 0,
        "all_targeted_rows_have_required_schema": targeted_schema_ok,
        "all_numeric_families_present": all(len(family_rows.get(f, [])) > 0 for f in NUMERIC_FAMILIES),
        "all_numeric_families_have_actual_and_consensus": all(
            any(nonempty(r.get("Actual")) and nonempty(r.get("Forecast")) for r in family_rows.get(f, []))
            for f in NUMERIC_FAMILIES
        ),
        "fomc_timing_row_present": len(family_rows.get("FOMC", [])) > 0,
        "source_provenance_present": source_provenance_any,
        "raw_vendor_payload_not_committed": True,
        "no_market_outcomes_or_protected_data": True,
    }
    result["gate"] = gate
    result["preflight_pass"] = all(gate.values())
    result["disposition"] = (
        "TRADING_ECONOMICS_PIT_ACCESS_PREFLIGHT_PASS"
        if result["preflight_pass"]
        else "TRADING_ECONOMICS_PIT_ACCESS_OR_SCHEMA_INSUFFICIENT"
    )

    write_result(result)

    print(json.dumps({
        "preflight_pass": result["preflight_pass"],
        "response_rows": len(rows),
        "family_rows": {k: v["matched_rows"] for k, v in families.items()},
        "actual_and_consensus_rows": {k: v["rows_with_actual_and_forecast"] for k, v in families.items()},
        "disposition": result["disposition"],
        "protected_periods": result["protected_periods"],
    }, indent=2))

    return 0 if result["preflight_pass"] else 8


if __name__ == "__main__":
    sys.exit(main())
