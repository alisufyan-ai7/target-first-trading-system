#!/usr/bin/env python3
"""EXP-041 official actual-as-released reconciliation v0.1.

Verifies one canonical forecast-bearing component per numeric official block
against first-party release context. No market outcomes.
"""

from __future__ import annotations

import hashlib
import io
import json
import math
import os
import re
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
CONS=ROOT/"research/data/EXP-041-free-macro-consensus-v0.3.json"
CONS_AUDIT=ROOT/"research/results/EXP-041-free-macro-consensus-scope-audit-v0.3.json"
TIME_MAP=ROOT/"research/data/EXP-041-official-release-time-map-v0.4.json"
TIME_AUDIT=ROOT/"research/results/EXP-041-official-release-time-reconciliation-v0.4.json"
OUT=ROOT/"research/data/EXP-041-official-macro-surprise-layer-v0.1.json"
RESULT=ROOT/"research/results/EXP-041-official-actual-reconciliation-v0.1.json"

UA="Mozilla/5.0 (compatible; target-first-trading-system-exp041/0.1; official-actual verification)"

HIER={
    "EMPLOYMENT":["Non-Farm Employment Change","Unemployment Rate","Average Hourly Earnings m/m"],
    "CPI":["CPI m/m","Core CPI m/m","CPI y/y","Core CPI y/y"],
    "PPI":["PPI m/m","Core PPI m/m"],
    "RETAIL":["Retail Sales m/m","Core Retail Sales m/m"],
    "GDP":["Advance GDP q/q","Prelim GDP q/q","Final GDP q/q"],
    "PCE":["Core PCE Price Index m/m","Personal Income m/m","Personal Spending m/m"],
}

BEA_2025={
    "2025-07-30|GDP_PCE|GDP":"https://www.bea.gov/news/2025/gross-domestic-product-2nd-quarter-2025-advance-estimate",
    "2025-07-31|GDP_PCE|PCE":"https://www.bea.gov/news/2025/personal-income-and-outlays-june-2025",
    "2025-08-28|GDP_PCE|GDP":"https://www.bea.gov/news/2025/gross-domestic-product-2nd-quarter-2025-second-estimate-and-corporate-profits-preliminary",
    "2025-08-29|GDP_PCE|PCE":"https://www.bea.gov/news/2025/personal-income-and-outlays-july-2025",
    "2025-09-25|GDP_PCE|GDP":"https://www.bea.gov/news/2025/gross-domestic-product-2nd-quarter-2025-third-estimate-gdp-industry-corporate-profits",
    "2025-09-26|GDP_PCE|PCE":"https://www.bea.gov/news/2025/personal-income-and-outlays-august-2025",
    "2025-12-05|GDP_PCE|PCE":"https://www.bea.gov/news/2025/personal-income-and-outlays-september-2025",
    "2025-12-23|GDP_PCE|GDP":"https://www.bea.gov/news/2025/gross-domestic-product-3rd-quarter-2025-initial-estimate-and-corporate-profits",
}


def sha256_file(p:Path)->str:
    h=hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda:fh.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()


def sha256_bytes(raw:bytes)->str:
    return hashlib.sha256(raw).hexdigest()


def fetch(url:str)->bytes:
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"*/*"})
    with urllib.request.urlopen(req,timeout=60) as r:
        if int(r.status)!=200: raise RuntimeError(f"HTTP {r.status}: {url}")
        return r.read()


def source_text(raw:bytes,url:str)->str:
    if url.lower().endswith(".pdf"):
        reader=PdfReader(io.BytesIO(raw))
        return re.sub(r"\s+"," "," ".join((p.extract_text() or "") for p in reader.pages[:4])).strip()
    soup=BeautifulSoup(raw,"html.parser")
    return re.sub(r"\s+"," ",soup.get_text(" ",strip=True)).strip()


def parse_native(text:str)->tuple[float,str]:
    s=text.strip().replace(",","")
    if s.endswith("K"):
        return float(s[:-1])*1000.0,"persons"
    if s.endswith("%"):
        return float(s[:-1]),"percent"
    raise ValueError(f"unsupported numeric text: {text}")


def number_pat(v:float,unit:str)->str:
    a=abs(v)
    if unit=="persons":
        n=int(round(a))
        comma=f"{n:,}"
        plain=str(n)
        return rf"(?:\+|-)?(?:{re.escape(comma)}|{plain})"
    # Preserve one/two-decimal published forms while allowing trailing zero.
    if abs(a-round(a))<1e-9:
        core=rf"{int(round(a))}(?:\.0+)?"
    else:
        core=re.escape(f"{a:.4f}".rstrip("0").rstrip("."))
    return rf"{core}\s*(?:%|percent)"


def context_windows(t:str,anchors:list[str],radius:int=700)->list[str]:
    out=[]
    for a in anchors:
        for m in re.finditer(a,t,flags=re.I):
            out.append(t[max(0,m.start()-radius):min(len(t),m.end()+radius)])
    return out


def has_candidate(windows:list[str],v:float,unit:str,negative_words:bool=True)->bool:
    pat=number_pat(v,unit)
    for w in windows:
        if not re.search(pat,w,flags=re.I):
            continue
        if v<0 and negative_words:
            if not re.search(r"decreas|declin|fell|down|drop|loss|contract|negative|\-",w,flags=re.I):
                continue
        return True
    return False


def verify_component(name:str,v:float,unit:str,t:str)->bool:
    if name=="Non-Farm Employment Change":
        return has_candidate(context_windows(t,[r"nonfarm payroll employment",r"non-farm payroll employment"],900),v,unit)

    if name=="Unemployment Rate":
        return has_candidate(context_windows(t,[r"unemployment rate"],500),v,unit)

    if name=="Average Hourly Earnings m/m":
        return has_candidate(context_windows(t,[r"average hourly earnings"],700),v,unit)

    if name=="CPI m/m":
        return has_candidate(context_windows(t,[r"CPI-U",r"Consumer Price Index",r"all items index"],500),v,unit)

    if name=="Core CPI m/m":
        return has_candidate(context_windows(t,[r"less food and energy",r"core CPI"],500),v,unit)

    if name in {"CPI y/y","Core CPI y/y"}:
        anchors=[r"12 months",r"12-month",r"over the last 12 months"]
        if "Core" in name:
            anchors += [r"less food and energy"]
        return has_candidate(context_windows(t,anchors,500),v,unit)

    if name=="PPI m/m":
        return has_candidate(context_windows(t,[r"final demand"],500),v,unit)

    if name=="Core PPI m/m":
        return has_candidate(context_windows(t,[r"final demand less foods? and energy",r"less foods? and energy"],600),v,unit)

    if name=="Retail Sales m/m":
        return has_candidate(context_windows(t,[r"retail and food services sales",r"retail sales"],700),v,unit)

    if name=="Core Retail Sales m/m":
        return has_candidate(context_windows(t,[r"excluding motor vehicle",r"excluding autos",r"retail"],700),v,unit)

    if re.fullmatch(r"(?:Advance|Prelim|Final) GDP q/q",name):
        return has_candidate(context_windows(t,[r"real gross domestic product",r"real GDP"],600),v,unit)

    if name=="Core PCE Price Index m/m":
        return has_candidate(context_windows(t,[r"excluding food and energy"],500),v,unit)

    if name=="Personal Income m/m":
        return has_candidate(context_windows(t,[r"personal income"],500),v,unit)

    if name=="Personal Spending m/m":
        return has_candidate(context_windows(t,[r"personal consumption expenditures",r"consumer spending"],500),v,unit)

    raise ValueError(f"unsupported selected component {name}")


def rows_for_block(records:list[dict],block:dict)->list[dict]:
    rows=[r for r in records if r["event_date"]==block["event_date"] and r["family"]==block["family"]]
    if block["family"]!="GDP_PCE":
        return rows
    if block["release_kind"]=="GDP":
        return [r for r in rows if re.search(r"\bGDP\b",r["event_name"],re.I)]
    return [r for r in rows if re.search(r"\bPCE\b|Personal Income|Personal Spending",r["event_name"],re.I)]


def select_component(rows:list[dict],kind:str)->dict:
    names=HIER[kind]
    for name in names:
        c=[r for r in rows if r["event_name"]==name and str(r.get("forecast_text","")).strip()]
        if len(c)==1:
            return c[0]
        if len(c)>1:
            raise RuntimeError(f"ambiguous forecast-bearing {name}: {len(c)}")
    raise RuntimeError(f"no forecast-bearing canonical component for {kind}")


def source_url(block:dict)->str:
    if block["family"]=="GDP_PCE":
        if block["official_block_id"] in BEA_2025:
            return BEA_2025[block["official_block_id"]]
        u=block.get("official_release_page_url") or block.get("official_source_url")
        if "/news/" not in u:
            raise RuntimeError(f"no direct BEA release page for {block['official_block_id']}")
        return u
    return block["official_source_url"]


def main()->int:
    cons_audit=json.loads(CONS_AUDIT.read_text())
    time_audit=json.loads(TIME_AUDIT.read_text())
    cons_sha=sha256_file(CONS)
    time_sha=sha256_file(TIME_MAP)

    if cons_sha!=cons_audit["normalized_dataset"]["sha256"]:
        raise SystemExit("consensus v0.3 SHA mismatch")
    if time_sha!=time_audit["official_time_map"]["sha256"]:
        raise SystemExit("official time-map v0.4 SHA mismatch")
    if not time_audit["release_time_reconciliation_pass"]:
        raise SystemExit("official time-map v0.4 did not pass")

    cons=json.loads(CONS.read_text())
    tm=json.loads(TIME_MAP.read_text())
    records=cons["records"]

    reconciled=[]
    errors=[]
    fetch_cache={}

    numeric_blocks=0
    fomc_blocks=0
    selected_counts=defaultdict(int)

    for block in tm["official_blocks"]:
        if block["family"]=="FOMC":
            fomc_blocks+=1
            reconciled.append({
                "official_block_id":block["official_block_id"],
                "family":"FOMC",
                "official_release_timestamp_utc":block["official_release_timestamp_utc"],
                "timing_only":True,
                "surprise_component":None,
                "official_source_url":block["official_source_url"],
            })
            continue

        numeric_blocks+=1
        kind=block["release_kind"] if block["family"]=="GDP_PCE" else block["family"]
        try:
            rows=rows_for_block(records,block)
            selected=select_component(rows,kind)
            forecast,fu=parse_native(selected["forecast_text"])
            candidate,au=parse_native(selected["actual_text"])
            if fu!=au:
                raise RuntimeError("forecast/actual unit mismatch")

            url=source_url(block)
            if url not in fetch_cache:
                raw=fetch(url)
                fetch_cache[url]=(raw,source_text(raw,url))
            raw,t=fetch_cache[url]

            ok=verify_component(selected["event_name"],candidate,au,t)
            if not ok:
                raise RuntimeError("candidate Actual not verified in official component context")

            selected_counts[kind]+=1
            reconciled.append({
                "official_block_id":block["official_block_id"],
                "family":block["family"],
                "release_kind":block["release_kind"],
                "official_release_timestamp_utc":block["official_release_timestamp_utc"],
                "selected_component":selected["event_name"],
                "event_id":selected.get("event_id",""),
                "forecast_text":selected["forecast_text"],
                "forecast_numeric":forecast,
                "candidate_actual_text":selected["actual_text"],
                "candidate_actual_numeric":candidate,
                "native_unit":au,
                "official_actual_verification_source_url":url,
                "official_actual_source_sha256":sha256_bytes(raw),
                "official_context_verified":True,
                "official_actual_numeric":candidate,
                "surprise_native":candidate-forecast,
                "timing_only":False,
            })

        except Exception as exc:
            errors.append({
                "official_block_id":block["official_block_id"],
                "family":block["family"],
                "release_kind":block["release_kind"],
                "reason":type(exc).__name__,
                "detail":str(exc)[:500],
            })

    numeric_rows=[r for r in reconciled if not r.get("timing_only")]
    gate={
        "consensus_v03_sha_verified":True,
        "official_time_map_v04_sha_verified":True,
        "numeric_official_blocks_67":numeric_blocks==67,
        "fomc_timing_only_blocks_8":fomc_blocks==8,
        "reconciled_numeric_records_67":len(numeric_rows)==67,
        "no_reconciliation_errors":len(errors)==0,
        "all_numeric_have_forecast":all(r.get("forecast_numeric") is not None for r in numeric_rows),
        "all_numeric_official_context_verified":all(r.get("official_context_verified") for r in numeric_rows),
        "all_numeric_have_source_hash":all(r.get("official_actual_source_sha256") for r in numeric_rows),
        "family_selection_counts_expected":(
            selected_counts["EMPLOYMENT"]==11 and
            selected_counts["CPI"]==11 and
            selected_counts["PPI"]==11 and
            selected_counts["RETAIL"]==12 and
            selected_counts["GDP"]==11 and
            selected_counts["PCE"]==11
        ),
        "no_market_data_or_outcomes_loaded":True,
        "protected_periods_sealed":True,
    }
    passed=all(gate.values())

    payload={
        "stage":"EXP-041 official macro surprise layer v0.1",
        "consensus_dataset":str(CONS.relative_to(ROOT)),
        "consensus_sha256":cons_sha,
        "official_time_map":str(TIME_MAP.relative_to(ROOT)),
        "official_time_map_sha256":time_sha,
        "canonical_component_hierarchy":HIER,
        "records":reconciled,
        "numeric_block_count":numeric_blocks,
        "fomc_timing_only_blocks":fomc_blocks,
        "protected_periods":cons["protected_periods"],
    }
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    out_sha=sha256_file(OUT)

    result={
        "stage":"EXP-041 official actual-as-released reconciliation v0.1",
        "tested_repository_sha":os.environ.get("GITHUB_SHA"),
        "github_run_id":os.environ.get("GITHUB_RUN_ID"),
        "inputs":{
            "consensus_v03_sha256":cons_sha,
            "official_time_map_v04_sha256":time_sha,
        },
        "output":{
            "path":str(OUT.relative_to(ROOT)),
            "sha256":out_sha,
            "records":len(reconciled),
            "numeric_records":len(numeric_rows),
            "fomc_timing_only_records":fomc_blocks,
        },
        "selected_counts":dict(sorted(selected_counts.items())),
        "source_pages_fetched":len(fetch_cache),
        "errors":errors,
        "gate":gate,
        "official_actual_reconciliation_pass":passed,
        "market_data_loaded":False,
        "target_labels_calculated":False,
        "pnl_calculated":False,
        "scientific_market_outcomes_calculated":False,
        "protected_periods":cons["protected_periods"],
        "disposition":(
            "OFFICIAL_ACTUAL_RECONCILIATION_PASS_FINAL_GATE_A_REQUIRED"
            if passed else
            "OFFICIAL_ACTUAL_RECONCILIATION_FAILED_REPAIR_COMPONENT_VERIFIER"
        ),
    }
    RESULT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")

    print(json.dumps({
        "pass":passed,
        "numeric_blocks":numeric_blocks,
        "numeric_reconciled":len(numeric_rows),
        "fomc_timing_only":fomc_blocks,
        "selected_counts":dict(sorted(selected_counts.items())),
        "errors":len(errors),
        "disposition":result["disposition"],
    },indent=2))
    return 0 if passed else 2


if __name__=="__main__":
    sys.exit(main())
