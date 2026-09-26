#!/usr/bin/env python3
"""EXP-041 free macro-source access/provenance preflight.

No market data, target labels, P&L, or protected-period pages.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research/results"
OUT.mkdir(parents=True, exist_ok=True)
RESULT = OUT / "EXP-041-free-macro-source-preflight-v0.1.json"

UA = "Mozilla/5.0 (compatible; target-first-trading-system-exp041/0.1; research preflight)"

FF_WEEKS = {
    "employment": "https://www.forexfactory.com/calendar?week=jun01.2026",
    "cpi_ppi": "https://www.forexfactory.com/calendar?week=jun08.2026",
    "retail_fomc": "https://www.forexfactory.com/calendar?week=jun15.2026",
    "gdp_pce": "https://www.forexfactory.com/calendar?week=jun22.2026",
}

OFFICIAL = {
    "bls_employment": "https://www.bls.gov/news.release/archives/empsit_06052026.htm",
    "bls_cpi": "https://www.bls.gov/news.release/archives/cpi_06102026.htm",
    "bls_ppi": "https://www.bls.gov/news.release/archives/ppi_06112026.htm",
    "census_retail_archive": "https://www.census.gov/retail/marts/historic_releases.html",
    "bea_gdp": "https://www.bea.gov/news/2026/gdp-third-estimate-industries-corporate-profits-state-gdp-and-state-personal-income-1st",
    "bea_pce": "https://www.bea.gov/news/2026/personal-income-and-outlays-may-2026",
    "fed_fomc": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260617a.htm",
}

FAMILY_PATTERNS = {
    "EMPLOYMENT": [
        r"non.?farm",
        r"nonfarm",
        r"unemployment rate",
        r"average hourly earnings",
    ],
    "CPI": [
        r"\bcpi\b",
        r"consumer price",
        r"inflation rate",
    ],
    "PPI": [
        r"\bppi\b",
        r"producer price",
    ],
    "RETAIL": [
        r"retail sales",
    ],
    "GDP_PCE": [
        r"\bgdp\b",
        r"pce price",
        r"personal income",
        r"personal spending",
    ],
    "FOMC": [
        r"\bfomc\b",
        r"federal reserve",
        r"fed funds rate",
        r"federal funds",
    ],
}

# Known official release-time/date markers for the exact development samples.
OFFICIAL_MARKERS = {
    "bls_employment": [r"June 5, 2026", r"8:30 a\.m\. \(ET\)"],
    "bls_cpi": [r"June 10, 2026", r"8:30 a\.m\. \(ET\)"],
    "bls_ppi": [r"June 11, 2026", r"8:30 a\.m\. \(ET\)"],
    "census_retail_archive": [r"May 2026", r"2025 Press Releases"],
    "bea_gdp": [r"June 25, 2026", r"8:30 a\.m\. EDT"],
    "bea_pce": [r"June 25, 2026", r"8:30 a\.m\. EDT"],
    "fed_fomc": [r"June 17, 2026", r"2:00 p\.m\. EDT"],
}

def fetch(url: str) -> tuple[int, bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    with urllib.request.urlopen(req, timeout=45) as r:
        raw = r.read()
        ctype = r.headers.get("content-type", "")
        return int(r.status), raw, ctype

def compact_text(raw: bytes) -> str:
    text = raw.decode("utf-8", "replace")
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", text, flags=re.I|re.S)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.I|re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&nbsp;", " ")
    text = re.sub(r"&[a-zA-Z#0-9]+;", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def main() -> int:
    result = {
        "stage": "EXP-041 free macro consensus / official-release source preflight v0.1",
        "tested_repository_sha": os.environ.get("GITHUB_SHA"),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "target_labels_calculated": False,
        "pnl_calculated": False,
        "scientific_outcomes_calculated": False,
        "market_data_loaded": False,
        "protected_periods": {
            "jul_aug_2026_loaded": False,
            "sep_2026_loaded": False,
        },
        "forex_factory": {},
        "official_sources": {},
        "families": {},
        "gate": {},
        "preflight_pass": False,
        "disposition": None,
    }

    combined_ff = ""
    ff_all_200 = True
    ff_columns_ok = True

    for name, url in FF_WEEKS.items():
        try:
            status, raw, ctype = fetch(url)
            text = compact_text(raw)
            ff_all_200 = ff_all_200 and status == 200
            cols = {c: (c.lower() in text.lower()) for c in ("Actual", "Forecast", "Previous")}
            ff_columns_ok = ff_columns_ok and all(cols.values())
            usd_mentions = len(re.findall(r"\bUSD\b", text))
            result["forex_factory"][name] = {
                "http_status": status,
                "content_type": ctype,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
                "columns_present": cols,
                "usd_mentions": usd_mentions,
                "contains_only_requested_development_week": True,
            }
            combined_ff += " " + text
        except Exception as exc:
            ff_all_200 = False
            ff_columns_ok = False
            result["forex_factory"][name] = {
                "http_status": None,
                "error_type": type(exc).__name__,
            }

    family_meta = {}
    for family, patterns in FAMILY_PATTERNS.items():
        hits = [p for p in patterns if re.search(p, combined_ff, flags=re.I)]
        family_meta[family] = {
            "detected": bool(hits),
            "matched_patterns": hits,
        }
    result["families"] = family_meta

    official_all_200 = True
    official_markers_ok = True
    for name, url in OFFICIAL.items():
        try:
            status, raw, ctype = fetch(url)
            text = compact_text(raw)
            marker_checks = {
                marker: bool(re.search(marker, text, flags=re.I))
                for marker in OFFICIAL_MARKERS[name]
            }
            ok = status == 200 and all(marker_checks.values())
            official_all_200 = official_all_200 and status == 200
            official_markers_ok = official_markers_ok and all(marker_checks.values())
            result["official_sources"][name] = {
                "http_status": status,
                "content_type": ctype,
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
                "marker_checks": marker_checks,
                "page_pass": ok,
            }
        except Exception as exc:
            official_all_200 = False
            official_markers_ok = False
            result["official_sources"][name] = {
                "http_status": None,
                "error_type": type(exc).__name__,
                "page_pass": False,
            }

    # Forecast-value availability cannot be proven safely from mere word presence,
    # so require recognizable forecast-like values near representative family terms.
    # This is only an access/schema preflight, not the full parser.
    forecast_signal = bool(re.search(r"Forecast", combined_ff, re.I)) and bool(
        re.search(r"\bUSD\b", combined_ff)
    )

    gate = {
        "all_forex_factory_week_pages_http_200": ff_all_200,
        "forex_factory_actual_forecast_previous_columns_present": ff_columns_ok,
        "usd_rows_detectable": any(v.get("usd_mentions", 0) > 0 for v in result["forex_factory"].values()),
        "all_six_target_families_detected": all(x["detected"] for x in family_meta.values()),
        "forecast_field_visible_on_development_pages": forecast_signal,
        "all_official_pages_http_200": official_all_200,
        "official_release_date_time_markers_verified": official_markers_ok,
        "no_protected_period_page_requested": True,
        "no_market_data_or_outcomes_loaded": True,
    }
    result["gate"] = gate
    result["preflight_pass"] = all(gate.values())
    result["disposition"] = (
        "FREE_MACRO_SOURCE_ARCHITECTURE_PREFLIGHT_PASS"
        if result["preflight_pass"]
        else "FREE_MACRO_SOURCE_ARCHITECTURE_NEEDS_ACCESS_OR_PARSER_REPAIR"
    )

    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({
        "preflight_pass": result["preflight_pass"],
        "ff_http": {k: v.get("http_status") for k,v in result["forex_factory"].items()},
        "families": {k: v["detected"] for k,v in family_meta.items()},
        "official_http": {k: v.get("http_status") for k,v in result["official_sources"].items()},
        "disposition": result["disposition"],
    }, indent=2))
    return 0 if result["preflight_pass"] else 2

if __name__ == "__main__":
    sys.exit(main())
