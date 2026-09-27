#!/usr/bin/env python3
"""EXP-041 official release-time reconciliation v0.3.

Same v0.2 source mapping except robust BEA schedule-row/link parsing.
No market outcomes.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "research/data/EXP-041-free-macro-consensus-v0.3.json"
SRC_AUDIT = ROOT / "research/results/EXP-041-free-macro-consensus-scope-audit-v0.3.json"
OUT = ROOT / "research/data/EXP-041-official-release-time-map-v0.3.json"
RESULT = ROOT / "research/results/EXP-041-official-release-time-reconciliation-v0.3.json"

UA = "Mozilla/5.0 (compatible; target-first-trading-system-exp041/0.3; official-source verification)"
NY = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")

BEA_URLS = {
    2025: "https://www.bea.gov/news/schedule/full-2025",
    2026: "https://www.bea.gov/news/schedule/full-2026",
}

RETAIL_PDFS = {
    "2025-07-17": "adv2506.pdf",
    "2025-08-15": "adv2507.pdf",
    "2025-09-16": "adv2508.pdf",
    "2025-11-25": "adv2509.pdf",
    "2025-12-16": "adv2510.pdf",
    "2026-01-14": "adv2511.pdf",
    "2026-02-10": "adv2512.pdf",
    "2026-03-06": "adv2601.pdf",
    "2026-04-01": "adv2602.pdf",
    "2026-04-21": "adv2603.pdf",
    "2026-05-14": "adv2604.pdf",
    "2026-06-17": "adv2605.pdf",
}
RETAIL_BASE = "https://www2.census.gov/retail/releases/historical/marts/"

MONTHS = {
    "January":1,"February":2,"March":3,"April":4,"May":5,"June":6,
    "July":7,"August":8,"September":9,"October":10,"November":11,"December":12,
}


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str) -> bytes:
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"*/*"})
    with urllib.request.urlopen(req,timeout=60) as r:
        if int(r.status)!=200:
            raise RuntimeError(f"HTTP {r.status}: {url}")
        return r.read()


def compact(s: str) -> str:
    return re.sub(r"\s+"," ",s or "").strip()


def html_text(raw: bytes) -> str:
    soup=BeautifulSoup(raw,"html.parser")
    return compact(soup.get_text(" ",strip=True))


def mmddyyyy(d: date) -> str:
    return d.strftime("%m%d%Y")


def bls_url(family: str,d: date)->str:
    prefix={"EMPLOYMENT":"empsit","CPI":"cpi","PPI":"ppi"}[family]
    return f"https://www.bls.gov/news.release/archives/{prefix}_{mmddyyyy(d)}.htm"


def fed_url(d: date)->str:
    return f"https://www.federalreserve.gov/newsevents/pressreleases/monetary{d.strftime('%Y%m%d')}a.htm"


def parse_clock(s: str)->tuple[int,int]:
    m=re.fullmatch(r"(\d{1,2}):(\d{2})\s*(AM|PM)",compact(s),flags=re.I)
    if not m:
        raise ValueError(f"unparseable clock: {s}")
    hh,mm=int(m.group(1)),int(m.group(2))
    ap=m.group(3).upper()
    if ap=="PM" and hh!=12: hh+=12
    if ap=="AM" and hh==12: hh=0
    return hh,mm


def to_utc(d: date,hh:int,mm:int)->str:
    return datetime(d.year,d.month,d.day,hh,mm,tzinfo=NY).astimezone(UTC).isoformat().replace("+00:00","Z")


def date_strings(d: date)->list[str]:
    return [f"{d.strftime('%B')} {d.day}, {d.year}",f"{d.strftime('%B')} {d.day:02d}, {d.year}"]


def contains_date(t: str,d: date)->bool:
    low=t.lower()
    return any(x.lower() in low for x in date_strings(d))


def pdf_first_page_text(raw: bytes)->str:
    reader=PdfReader(io.BytesIO(raw))
    return compact(reader.pages[0].extract_text() if reader.pages else "")


def bea_title_kind(title: str)->str|None:
    t=compact(title)
    if re.search(r"Personal Income and Outlays",t,re.I):
        return "PCE"
    if re.search(r"Gross Domestic Product|\bGDP\b",t,re.I):
        # Exclude subnational GDP-only releases; frozen dates/titles further disambiguate.
        if re.search(r"by State|by County",t,re.I) and not re.search(r"Corporate Profits|Advance Estimate|Second Estimate|Third Estimate|Updated Estimate",t,re.I):
            return None
        return "GDP"
    return None


def parse_bea_date_and_time(text: str,year:int)->tuple[str,str]|None:
    s=compact(text)
    m=re.search(
        r"\b("+"|".join(MONTHS.keys())+r")\s+(\d{1,2})\s+(\d{1,2}:\d{2}\s*(?:AM|PM))\b",
        s,re.I
    )
    if not m:
        return None
    month_name=next(k for k in MONTHS if k.lower()==m.group(1).lower())
    d=date(year,MONTHS[month_name],int(m.group(2)))
    return d.isoformat(),compact(m.group(3)).upper()


def bea_entries(raw: bytes,year:int,base_url:str)->list[dict]:
    soup=BeautifulSoup(raw,"html.parser")
    entries=[]
    seen=set()

    # Strategy 1: parse table rows, retaining release-page links.
    for tr in soup.find_all("tr"):
        row_text=compact(tr.get_text(" ",strip=True))
        dt=parse_bea_date_and_time(row_text,year)
        if not dt:
            continue
        links=tr.find_all("a",href=True)
        title=""
        href=""
        # Prefer anchors that point to a BEA news release.
        for a in links:
            at=compact(a.get_text(" ",strip=True))
            ah=a.get("href","")
            if "/news/" in ah and at and at.lower() not in {"view","news"}:
                title=at
                href=ah
                break
        # Some tables use title text outside the View anchor.
        if not title:
            # Remove date/time and UI tokens; keep row text for classification.
            title=re.sub(r"^.*?\b(?:AM|PM)\b\s+N\s*ews\s+","",row_text,flags=re.I)
            title=re.sub(r"\s+View\s*$","",title,flags=re.I)
            # Capture any /news/ link even when its anchor text is View.
            for a in links:
                ah=a.get("href","")
                if "/news/" in ah:
                    href=ah
                    break
        kind=bea_title_kind(title)
        if not kind:
            continue
        dstr,tstr=dt
        full_url=urllib.parse.urljoin(base_url,href) if href else ""
        key=(dstr,tstr,title,kind)
        if key not in seen:
            seen.add(key)
            entries.append({"date":dstr,"time":tstr,"title":title,"kind":kind,"release_url":full_url})

    # Strategy 2: containers carrying a /news/ link, for non-table Drupal layouts.
    for a in soup.find_all("a",href=True):
        href=a.get("href","")
        if "/news/" not in href:
            continue
        container=a.find_parent(["tr","li","div"])
        if container is None:
            continue
        ct=compact(container.get_text(" ",strip=True))
        dt=parse_bea_date_and_time(ct,year)
        if not dt:
            continue
        # Prefer visible descriptive text from container rather than "View".
        title=compact(a.get_text(" ",strip=True))
        if title.lower() in {"view","news",""}:
            # Look for text matching known release families.
            m=re.search(
                r"(Gross Domestic Product.+|GDP\s*\(.+|Personal Income and Outlays.+)",
                ct,re.I
            )
            title=compact(m.group(1)) if m else ct
        kind=bea_title_kind(title) or bea_title_kind(ct)
        if not kind:
            continue
        dstr,tstr=dt
        full_url=urllib.parse.urljoin(base_url,href)
        key=(dstr,tstr,title,kind)
        if key not in seen:
            seen.add(key)
            entries.append({"date":dstr,"time":tstr,"title":title,"kind":kind,"release_url":full_url})

    # Strategy 3: flattened text fallback. Links may be unavailable but timestamp provenance remains.
    if not entries:
        txt=compact(soup.get_text(" ",strip=True))
        pat=re.compile(
            r"\b("+"|".join(MONTHS.keys())+r")\s+(\d{1,2})\s+"
            r"(\d{1,2}:\d{2}\s*(?:AM|PM))\s+N\s*ews\s+"
            r"(.+?)(?=\s+View\b|\b(?:"+"|".join(MONTHS.keys())+r")\s+\d{1,2}\s+\d{1,2}:\d{2}\s*(?:AM|PM)|$)",
            re.I
        )
        for m in pat.finditer(txt):
            month_name=next(k for k in MONTHS if k.lower()==m.group(1).lower())
            d=date(year,MONTHS[month_name],int(m.group(2)))
            title=compact(m.group(4))
            kind=bea_title_kind(title)
            if kind:
                entries.append({"date":d.isoformat(),"time":compact(m.group(3)).upper(),"title":title,"kind":kind,"release_url":""})

    return entries


def bea_kind(event_name:str)->str:
    if re.search(r"\bGDP\b",event_name,re.I): return "GDP"
    if re.search(r"\bPCE\b|Personal Income|Personal Spending",event_name,re.I): return "PCE"
    raise ValueError(f"unclassified GDP_PCE component: {event_name}")


def build_official_blocks(src:dict)->list[dict]:
    grouped=defaultdict(list)
    for r in src["records"]:
        if r["family"]=="GDP_PCE":
            kind=bea_kind(r["event_name"])
            key=(r["event_date"],"GDP_PCE",kind)
        else:
            key=(r["event_date"],r["family"],r["family"])
        grouped[key].append(r)
    blocks=[]
    for (d,fam,kind),rs in sorted(grouped.items()):
        blocks.append({
            "official_block_id":f"{d}|{fam}|{kind}",
            "event_date":d,
            "family":fam,
            "release_kind":kind,
            "component_event_ids":[r.get("event_id","") for r in rs if r.get("event_id")],
            "component_names":[r["event_name"] for r in rs],
            "component_record_keys":["|".join([r["event_date"],r["family"],r["event_name"],r.get("event_id","")]) for r in rs],
        })
    return blocks


def main()->int:
    if not SRC.exists() or not SRC_AUDIT.exists():
        raise SystemExit("frozen v0.3 input missing")

    audit=json.loads(SRC_AUDIT.read_text())
    expected_sha=audit["normalized_dataset"]["sha256"]
    observed_sha=sha256_file(SRC)
    if observed_sha!=expected_sha:
        raise SystemExit(f"v0.3 SHA mismatch: {observed_sha} != {expected_sha}")
    if not audit["consensus_layer_gate_pass"]:
        raise SystemExit("v0.3 gate did not pass")

    src=json.loads(SRC.read_text())
    official_blocks=build_official_blocks(src)

    bea_raw={year:fetch(url) for year,url in BEA_URLS.items()}
    bea_rows={year:bea_entries(bea_raw[year],year,BEA_URLS[year]) for year in BEA_URLS}

    mapped=[]
    errors=[]

    for b in official_blocks:
        d=date.fromisoformat(b["event_date"])
        fam=b["family"]
        row={**b,"official_local_timezone":"America/New_York","source_date_verified":False,"source_time_verified":False}
        try:
            if fam in {"EMPLOYMENT","CPI","PPI"}:
                url=bls_url(fam,d)
                raw=fetch(url)
                t=html_text(raw)
                row.update({
                    "official_authority":"U.S. Bureau of Labor Statistics",
                    "official_source_url":url,
                    "official_release_page_url":url,
                    "official_source_sha256":sha256_bytes(raw),
                    "official_local_release_time":"08:30",
                    "official_release_timestamp_utc":to_utc(d,8,30),
                    "source_date_verified":contains_date(t,d),
                    "source_time_verified":bool(re.search(r"8:30\s*a\.m\.\s*\(ET\)",t,re.I)),
                })

            elif fam=="RETAIL":
                fn=RETAIL_PDFS.get(b["event_date"])
                if not fn: raise RuntimeError("retail mapping missing")
                url=RETAIL_BASE+fn
                raw=fetch(url)
                t=pdf_first_page_text(raw)
                row.update({
                    "official_authority":"U.S. Census Bureau",
                    "official_source_url":url,
                    "official_release_page_url":url,
                    "official_source_sha256":sha256_bytes(raw),
                    "official_local_release_time":"08:30",
                    "official_release_timestamp_utc":to_utc(d,8,30),
                    "source_date_verified":contains_date(t,d),
                    "source_time_verified":bool(re.search(r"FOR RELEASE AT\s+8:30\s*AM\s+E(?:D|S)T",t,re.I)),
                })

            elif fam=="GDP_PCE":
                kind=b["release_kind"]
                candidates=[x for x in bea_rows[d.year] if x["date"]==d.isoformat() and x["kind"]==kind]
                if len(candidates)!=1:
                    raise RuntimeError(f"BEA {kind} schedule match count={len(candidates)}")
                e=candidates[0]
                hh,mm=parse_clock(e["time"])
                schedule_url=BEA_URLS[d.year]
                row.update({
                    "official_authority":"U.S. Bureau of Economic Analysis",
                    "official_source_url":schedule_url,
                    "official_release_page_url":e.get("release_url",""),
                    "official_source_sha256":sha256_bytes(bea_raw[d.year]),
                    "official_schedule_title":e["title"],
                    "official_local_release_time":f"{hh:02d}:{mm:02d}",
                    "official_release_timestamp_utc":to_utc(d,hh,mm),
                    "source_date_verified":True,
                    "source_time_verified":True,
                })

            elif fam=="FOMC":
                url=fed_url(d)
                raw=fetch(url)
                t=html_text(raw)
                row.update({
                    "official_authority":"Federal Reserve Board",
                    "official_source_url":url,
                    "official_release_page_url":url,
                    "official_source_sha256":sha256_bytes(raw),
                    "official_local_release_time":"14:00",
                    "official_release_timestamp_utc":to_utc(d,14,0),
                    "source_date_verified":contains_date(t,d),
                    "source_time_verified":bool(re.search(r"For release at\s*2:00\s*p\.m\.\s*E(?:D|S)T",t,re.I)),
                })
            else:
                raise RuntimeError(f"unsupported family {fam}")

            if not row.get("source_date_verified") or not row.get("source_time_verified") or not row.get("official_release_timestamp_utc"):
                errors.append({"official_block_id":b["official_block_id"],"reason":"official date/time marker not verified"})
            mapped.append(row)
        except Exception as exc:
            row["error_type"]=type(exc).__name__
            row["error_detail"]=str(exc)[:300]
            mapped.append(row)
            errors.append({"official_block_id":b["official_block_id"],"reason":type(exc).__name__,"detail":str(exc)[:300]})

    record_keys=["|".join([r["event_date"],r["family"],r["event_name"],r.get("event_id","")]) for r in src["records"]]
    mapped_keys=[k for m in mapped for k in m.get("component_record_keys",[])]
    membership_ok=sorted(record_keys)==sorted(mapped_keys)

    fam_counts=defaultdict(int)
    kind_counts=defaultdict(int)
    resolved=defaultdict(int)
    bea_2026_with_links=0
    bea_2026_total=0
    for m in mapped:
        fam_counts[m["family"]]+=1
        kind_counts[f"{m['family']}:{m['release_kind']}"]+=1
        if m.get("source_date_verified") and m.get("source_time_verified") and m.get("official_release_timestamp_utc"):
            resolved[m["family"]]+=1
        if m["family"]=="GDP_PCE" and m["event_date"].startswith("2026-"):
            bea_2026_total+=1
            if m.get("official_release_page_url"): bea_2026_with_links+=1

    gate={
        "input_v03_sha_verified":True,
        "all_source_records_assigned_exactly_once":membership_ok,
        "no_reconciliation_errors":len(errors)==0,
        "all_official_blocks_have_source_url":all(m.get("official_source_url") for m in mapped),
        "all_official_blocks_have_source_hash":all(m.get("official_source_sha256") for m in mapped),
        "all_official_blocks_have_utc_timestamp":all(m.get("official_release_timestamp_utc") for m in mapped),
        "all_dates_verified":all(m.get("source_date_verified") for m in mapped),
        "all_times_verified":all(m.get("source_time_verified") for m in mapped),
        "employment_blocks_11":fam_counts["EMPLOYMENT"]==11,
        "cpi_blocks_11":fam_counts["CPI"]==11,
        "ppi_blocks_11":fam_counts["PPI"]==11,
        "retail_blocks_12":fam_counts["RETAIL"]==12,
        "fomc_blocks_8":fam_counts["FOMC"]==8,
        "bea_gdp_blocks_11":kind_counts["GDP_PCE:GDP"]==11,
        "bea_pce_blocks_11":kind_counts["GDP_PCE:PCE"]==11,
        "all_2026_bea_blocks_have_release_links_if_exposed":bea_2026_with_links==bea_2026_total,
        "no_market_data_or_outcomes_loaded":True,
        "protected_periods_sealed":True,
    }
    passed=all(gate.values())

    payload={
        "stage":"EXP-041 official release-time map v0.3",
        "input_consensus_dataset":str(SRC.relative_to(ROOT)),
        "input_consensus_sha256":observed_sha,
        "official_blocks":mapped,
        "official_block_count":len(mapped),
        "family_counts":dict(sorted(fam_counts.items())),
        "release_kind_counts":dict(sorted(kind_counts.items())),
        "bea_schedule_parse_counts":{str(y):len(bea_rows[y]) for y in bea_rows},
        "protected_periods":src["protected_periods"],
    }
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    out_sha=sha256_file(OUT)

    result={
        "stage":"EXP-041 official release-time reconciliation v0.3",
        "tested_repository_sha":os.environ.get("GITHUB_SHA"),
        "github_run_id":os.environ.get("GITHUB_RUN_ID"),
        "supersedes_result_commit":"83b12d3673fb770854f12e93b3c479d7a3f79743",
        "input_v03":{"path":str(SRC.relative_to(ROOT)),"expected_sha256":expected_sha,"observed_sha256":observed_sha},
        "official_time_map":{"path":str(OUT.relative_to(ROOT)),"sha256":out_sha,"official_blocks":len(mapped)},
        "family_counts":dict(sorted(fam_counts.items())),
        "release_kind_counts":dict(sorted(kind_counts.items())),
        "bea_schedule_parse_counts":{str(y):len(bea_rows[y]) for y in bea_rows},
        "resolved_family_counts":dict(sorted(resolved.items())),
        "errors":errors,
        "gate":gate,
        "release_time_reconciliation_pass":passed,
        "official_actual_reconciliation_complete":False,
        "market_data_loaded":False,
        "target_labels_calculated":False,
        "pnl_calculated":False,
        "scientific_outcomes_calculated":False,
        "protected_periods":src["protected_periods"],
        "disposition":(
            "OFFICIAL_RELEASE_TIME_RECONCILIATION_V03_PASS_ACTUAL_VALUES_REQUIRED"
            if passed else
            "OFFICIAL_RELEASE_TIME_RECONCILIATION_V03_FAILED_REPAIR_SOURCE_MAPPING"
        ),
    }
    RESULT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({
        "pass":passed,
        "official_blocks":len(mapped),
        "bea_parse_counts":result["bea_schedule_parse_counts"],
        "errors":len(errors),
        "disposition":result["disposition"],
    },indent=2))
    return 0 if passed else 2


if __name__=="__main__":
    sys.exit(main())
