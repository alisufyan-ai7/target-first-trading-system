#!/usr/bin/env python3
from __future__ import annotations

import csv, hashlib, io, json, os, random, secrets, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[7]
V02 = ROOT / "research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.2"
EVENTS = V02 / "candidate-events-v0.2.csv"
FRAME_SELECTION = V02 / "frame-selection-v0.2.csv"
INSTRUCTIONS = V02 / "INDEPENDENT-ANNOTATOR-INSTRUCTIONS-v0.2.md"
OUT = ROOT / "_badar_v02_blind_build"
SOURCE_ROOT = Path(os.environ.get("BADAR_V02_SOURCE_ROOT", ROOT / "_badar_v02_source_frames"))

SOURCE_COMMIT = "bd0037e06a881a066e0cd8070b635cace59240d1"
SAFETY_SECONDS = 10
MAX_GAP_SECONDS = 240

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
    selection=read_csv(FRAME_SELECTION)
    selection_by_event={r["event_id"]:r for r in selection}
    instructions=INSTRUCTIONS.read_bytes()
    cases=[]; excluded=[]

    if not SOURCE_ROOT.exists():
        raise SystemExit(f"source frame root missing: {SOURCE_ROOT}")

    for row in events:
        event_id=row["event_id"]; sid=row["stream_id"]; evs=int(row["event_seconds"])
        sel=selection_by_event.get(event_id)
        if not sel:
            excluded.append({"event_id":event_id,"reason":"NO_FROZEN_SELECTION"}); continue
        if sel.get("eligible")!="YES":
            excluded.append({"event_id":event_id,"reason":"FROZEN_SELECTION_INELIGIBLE"}); continue
        latest_gap=int(float(sel["latest_gap_seconds"]))
        if latest_gap>MAX_GAP_SECONDS:
            excluded.append({"event_id":event_id,"reason":f"LATEST_GAP_{latest_gap}"}); continue

        paths=[p for p in sel["source_frame_paths"].split("|") if p]
        times=[int(float(x)) for x in sel["source_frame_times"].split("|") if x]
        if len(paths)!=len(times) or not paths:
            excluded.append({"event_id":event_id,"reason":"FRAME_SELECTION_MALFORMED"}); continue

        frames=[]
        for source_path,t in zip(paths,times):
            a=source_path.split("/")
            source_sid=a[-2]; fn=a[-1]
            if source_sid!=sid:
                raise SystemExit(f"stream mismatch {event_id}: {source_sid} != {sid}")
            local=SOURCE_ROOT/sid/fn
            if not local.exists():
                raise SystemExit(f"missing staged frame: {local}")
            if t>evs-SAFETY_SECONDS:
                raise SystemExit(f"unsafe frame for {event_id}: {t} > {evs-SAFETY_SECONDS}")
            frames.append(({"frame_file":fn,"stream_time_s":t},local.read_bytes()))

        conf=norm_confirmation_status(row)
        req=norm_required_close_status(row)
        cases.append({
            "row":row,"frames":frames,"latest_gap":latest_gap,
            "confirmation_candle_status":conf,"required_htf_close_status":req
        })

    if len(cases)!=len(events):
        raise SystemExit(f"eligible case mismatch: {len(cases)} of {len(events)}; excluded={excluded}")

    # Random blind mappings are created before annotation.
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
                "max_gap_seconds":MAX_GAP_SECONDS,
                "candidate_event_ids_exposed":False,"source_stream_ids_exposed":False,
                "badar_decision_labels_exposed":False,"outcomes_exposed":False
            },indent=2).encode())
        zip_paths[ann]=zpath

    cross_fields=["event_id","stream_id","event_seconds","annotator_A_id","annotator_B_id","latest_frame_gap_seconds"]
    cross=csv_bytes(map_rows,cross_fields)
    (OUT/"SEALED-v0.2-crosswalk.csv").write_bytes(cross)
    (OUT/"excluded-events.csv").write_bytes(b"event_id,reason\n")

    summary={
        "source_commit":SOURCE_COMMIT,
        "candidate_events":len(events),"eligible_cases":len(cases),"excluded":[],
        "A_sha256":sha256_file(zip_paths["A"]),
        "B_sha256":sha256_file(zip_paths["B"]),
        "crosswalk_sha256":sha256_bytes(cross),
        "A_file":zip_paths["A"].name,"B_file":zip_paths["B"].name,
        "frames_total":sum(len(c["frames"]) for c in cases),
        "unique_source_frames":len({fr["frame_file"] for c in cases for fr,_ in c["frames"]}),
        "latest_gap_max":max(c["latest_gap"] for c in cases),
        "latest_gap_median":sorted(c["latest_gap"] for c in cases)[len(cases)//2],
        "packet_metadata_complete":True,
        "decision_labels_exposed":False,"outcomes_exposed":False
    }
    (OUT/"BUILD-SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":
    main()
