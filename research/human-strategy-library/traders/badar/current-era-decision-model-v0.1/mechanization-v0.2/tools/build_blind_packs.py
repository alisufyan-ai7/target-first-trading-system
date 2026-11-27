#!/usr/bin/env python3
from __future__ import annotations

import csv, hashlib, io, json, random, secrets, urllib.request, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
V02 = ROOT / "research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.2"
EVENTS = V02 / "candidate-events-v0.2.csv"
INSTRUCTIONS = V02 / "INDEPENDENT-ANNOTATOR-INSTRUCTIONS-v0.2.md"
OUT = ROOT / "_badar_v02_blind_build"

SOURCE_REPO = "alisufyan-ai7/unpack-human-trading-strategies-claude"
SOURCE_COMMIT = "bd0037e06a881a066e0cd8070b635cace59240d1"
SOURCE_BASE = "traders/badar-tanveer/evidence/stream_frames"
SAFETY_SECONDS = 10
MAX_GAP_SECONDS = 240
MAX_FRAMES = 5

def get(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()

def raw(path: str) -> bytes:
    return get(f"https://raw.githubusercontent.com/{SOURCE_REPO}/{SOURCE_COMMIT}/{path}")

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_file(p: Path) -> str:
    h=hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def read_csv(path: Path):
    with path.open(newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def norm_confirmation_status(row):
    rawv=(row["candle_status_at_cutoff"] or "").upper()
    ref=(row["confirmation_reference"] or "").upper()
    if "DIRECT" in ref or rawv=="NOT_REQUIRED":
        return "NOT_REQUIRED"
    if "PENDING" in rawv or rawv=="NONE":
        return "PENDING"
    if "CLOSED" in rawv or "WEAK_OR_UNCLEAR" in rawv:
        return "CLOSED"
    return "UNKNOWN"

def norm_required_close_status(row):
    if row["required_htf_close_tf"]=="NONE":
        return "NOT_REQUIRED"
    if row["event_id"] in {"V02-PYP-003","V02-6W-001"}:
        return "PENDING"
    return "UNKNOWN"

def automatic_confirmation(status):
    if status=="NOT_REQUIRED": return "NONE"
    if status=="PENDING": return "NOT_YET"
    return ""

def automatic_htf(required_status):
    if required_status=="NOT_REQUIRED": return "NOT_RELEVANT"
    if required_status=="PENDING": return "REQUIRED_PENDING"
    return ""

def load_stream_index(stream_id):
    path=f"{SOURCE_BASE}/{stream_id}/index.csv"
    rows=list(csv.DictReader(io.StringIO(raw(path).decode("utf-8-sig"))))
    for r in rows: r["stream_time_s"]=int(float(r["stream_time_s"]))
    return rows

def select_frames(index_rows, event_s):
    cutoff=event_s-SAFETY_SECONDS
    safe=[r for r in index_rows if r["stream_time_s"]<=cutoff]
    if not safe: return []
    tail=safe[-4:]
    context=[r for r in safe if r["stream_time_s"]<=event_s-300]
    if context:
        tail=[context[-1]]+tail
    seen=set(); out=[]
    for r in tail:
        if r["frame_file"] not in seen:
            seen.add(r["frame_file"]); out.append(r)
    out=sorted(out,key=lambda r:r["stream_time_s"])
    return out[-MAX_FRAMES:]

def blind_id(prefix):
    return prefix + "-" + secrets.token_hex(6).upper()

def csv_bytes(rows, fields):
    s=io.StringIO(); w=csv.DictWriter(s,fieldnames=fields,lineterminator="\n")
    w.writeheader(); w.writerows(rows)
    return s.getvalue().encode("utf-8")

def case_md(blind,row,conf_status,req_status,frames):
    return f"""# Blind case {blind}

## Frozen prospective candidate metadata

- Candidate direction: {row['candidate_direction']}
- Directional context: {row['directional_context']}
- Intended POI anchor: {row['intended_poi_anchor']}
- POI family: {row['poi_family']}
- Entry-area anchor: {row['entry_area_anchor']}
- Relevant context timeframe: {row['relevant_context_tf']}
- Confirmation timeframe: {row['confirmation_tf']}
- Confirmation reference: {row['confirmation_reference']}
- Confirmation-candle status: {conf_status}
- Required HTF-close timeframe: {row['required_htf_close_tf']}
- Required HTF-close status: {req_status}
- Structural-stop anchor: {row['structural_stop_anchor']}
- First-objective anchor: {row['first_objective_anchor']}
- Blocking-POI anchor: {row['blocking_poi_anchor']}

## Frames

{len(frames)} frames are supplied in chronological order.

Judge only the supplied candidate and anchors.

Do not infer what the trader eventually did.
"""

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    events=read_csv(EVENTS)
    instructions=INSTRUCTIONS.read_bytes()
    idx_cache={}
    cases=[]
    excluded=[]
    for row in events:
        sid=row["stream_id"]; evs=int(row["event_seconds"])
        idx_cache.setdefault(sid,load_stream_index(sid))
        frames=select_frames(idx_cache[sid],evs)
        if not frames:
            excluded.append({"event_id":row["event_id"],"reason":"NO_SAFE_FRAME"}); continue
        latest_gap=evs-frames[-1]["stream_time_s"]
        if latest_gap>MAX_GAP_SECONDS:
            excluded.append({"event_id":row["event_id"],"reason":f"LATEST_GAP_{latest_gap}"}); continue
        conf=norm_confirmation_status(row)
        req=norm_required_close_status(row)
        downloaded=[]
        for fr in frames:
            p=f"{SOURCE_BASE}/{sid}/{fr['frame_file']}"
            b=raw(p)
            downloaded.append((fr,b))
        cases.append({
            "row":row,"frames":downloaded,"latest_gap":latest_gap,
            "confirmation_candle_status":conf,"required_htf_close_status":req
        })

    if len(cases)<35:
        raise SystemExit(f"too few eligible cases: {len(cases)}")

    # mappings are random and created before annotation.
    map_rows=[]
    for c in cases:
        map_rows.append({
            "event_id":c["row"]["event_id"],
            "stream_id":c["row"]["stream_id"],
            "event_seconds":c["row"]["event_seconds"],
            "annotator_A_id":blind_id("A"),
            "annotator_B_id":blind_id("B"),
            "latest_frame_gap_seconds":c["latest_gap"],
        })

    # independent order
    orderA=map_rows[:]; orderB=map_rows[:]
    random.SystemRandom().shuffle(orderA); random.SystemRandom().shuffle(orderB)
    by_event={c["row"]["event_id"]:c for c in cases}

    template_fields=[
        "blind_case_id","location_state","late_state","structural_stop_visibility",
        "confirmation_state","htf_close_state","target_path_state",
        "annotation_confidence","unresolved_notes","prior_exposure"
    ]

    zip_paths={}
    for ann,ordered,idcol in [("A",orderA,"annotator_A_id"),("B",orderB,"annotator_B_id")]:
        zpath=OUT/f"annotator-{ann}-badar-v0.2.zip"
        template=[]
        with zipfile.ZipFile(zpath,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            z.writestr("INSTRUCTIONS.md",instructions)
            for m in ordered:
                c=by_event[m["event_id"]]; row=c["row"]; blind=m[idcol]
                conf=c["confirmation_candle_status"]; req=c["required_htf_close_status"]
                auto_conf=automatic_confirmation(conf); auto_htf=automatic_htf(req)
                template.append({
                    "blind_case_id":blind,"location_state":"","late_state":"",
                    "structural_stop_visibility":"","confirmation_state":auto_conf,
                    "htf_close_state":auto_htf,"target_path_state":"",
                    "annotation_confidence":"","unresolved_notes":"","prior_exposure":"NO"
                })
                root=f"cases/{blind}"
                z.writestr(f"{root}/CASE.md",case_md(blind,row,conf,req,c["frames"]).encode("utf-8"))
                for i,(fr,b) in enumerate(c["frames"],1):
                    z.writestr(f"{root}/frame_{i:02d}.jpg",b)
            z.writestr("annotation-template.csv",csv_bytes(template,template_fields))
            z.writestr("PACK.json",json.dumps({
                "version":"0.2","annotator":ann,"cases":len(ordered),
                "source_commit":SOURCE_COMMIT,"safety_seconds":SAFETY_SECONDS,
                "max_gap_seconds":MAX_GAP_SECONDS,"badar_decision_labels_exposed":False,
                "outcomes_exposed":False
            },indent=2).encode())
        zip_paths[ann]=zpath

    cross_fields=["event_id","stream_id","event_seconds","annotator_A_id","annotator_B_id","latest_frame_gap_seconds"]
    cross=csv_bytes(map_rows,cross_fields)
    (OUT/"SEALED-v0.2-crosswalk.csv").write_bytes(cross)
    excluded_fields=["event_id","reason"]
    (OUT/"excluded-events.csv").write_bytes(csv_bytes(excluded,excluded_fields) if excluded else b"event_id,reason\n")

    summary={
        "source_commit":SOURCE_COMMIT,
        "candidate_events":len(events),"eligible_cases":len(cases),"excluded":excluded,
        "A_sha256":sha256_file(zip_paths["A"]),
        "B_sha256":sha256_file(zip_paths["B"]),
        "crosswalk_sha256":sha256_bytes(cross),
        "A_file":zip_paths["A"].name,"B_file":zip_paths["B"].name,
        "frames_total":sum(len(c["frames"]) for c in cases),
        "latest_gap_max":max(c["latest_gap"] for c in cases),
        "latest_gap_median":sorted(c["latest_gap"] for c in cases)[len(cases)//2],
    }
    (OUT/"BUILD-SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
