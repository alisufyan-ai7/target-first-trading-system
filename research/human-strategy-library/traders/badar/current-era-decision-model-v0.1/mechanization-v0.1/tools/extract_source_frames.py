#!/usr/bin/env python3
"""Extract blinded pre-decision frames from Badar source-stream media.

This script intentionally NEVER downloads media. It consumes the existing
Claude-side media cache (badartrader-research/media/) and the frozen
source-frame-request.csv manifest.

No P&L, result-R, MFE/MAE, future candles, or Badar decision labels are used.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_MANIFEST = (
    Path(__file__).resolve().parents[1] / "source-frame-request.csv"
)
OFFSETS = (
    ("t_minus_120_seconds", "m120"),
    ("t_minus_60_seconds", "m060"),
    ("t_minus_30_seconds", "m030"),
    ("t_minus_5_seconds", "m005"),
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def media_for(media_dir: Path, stream_id: str) -> Path | None:
    bad_suffixes = {".part", ".ytdl", ".txt", ".json", ".csv", ".jpg", ".jpeg", ".png", ".webp"}
    candidates = []
    for p in sorted(media_dir.glob(f"{stream_id}.*")):
        if not p.is_file():
            continue
        if p.suffix.lower() in bad_suffixes:
            continue
        candidates.append(p)
    return candidates[0] if candidates else None


def extract_frame(ffmpeg: str, src: Path, t: float, dst: Path, width: int) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    # -ss before -i gives fast seeking. The requested frame is always <= event cutoff.
    cmd = [
        ffmpeg,
        "-v", "error",
        "-y",
        "-ss", f"{t:.3f}",
        "-i", str(src),
        "-frames:v", "1",
        "-vf", f"scale={width}:-2",
        "-q:v", "2",
        str(dst),
    ]
    subprocess.run(cmd, check=True)


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--media-dir", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--ffmpeg", default="ffmpeg")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--limit", type=int, default=0, help="0 = all READY events")
    args = ap.parse_args()

    if not shutil.which(args.ffmpeg):
        raise SystemExit(f"ffmpeg not found: {args.ffmpeg}")
    if not args.manifest.exists():
        raise SystemExit(f"manifest missing: {args.manifest}")
    if not args.media_dir.exists():
        raise SystemExit(f"media directory missing: {args.media_dir}")

    rows = load_manifest(args.manifest)
    ready = [r for r in rows if r.get("extraction_status") == "READY"]
    if args.limit > 0:
        ready = ready[: args.limit]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    index_rows: list[dict[str, str]] = []
    missing_media: set[str] = set()
    failures: list[dict[str, str]] = []

    for n, row in enumerate(ready, 1):
        event_id = row["decision_event_id"]
        stream_id = row["stream_id"]
        src = media_for(args.media_dir, stream_id)
        if src is None:
            missing_media.add(stream_id)
            continue

        event_dir = args.out_dir / "events" / event_id
        for field, label in OFFSETS:
            raw = row.get(field, "")
            if raw == "":
                continue
            t = float(raw)
            dst = event_dir / f"{event_id}__{label}.jpg"
            try:
                extract_frame(args.ffmpeg, src, t, dst, args.width)
                index_rows.append({
                    "decision_event_id": event_id,
                    "stream_id": stream_id,
                    "stream_date": row["stream_date"],
                    "source_stream_timestamp": row["source_stream_timestamp"],
                    "frame_label": label,
                    "frame_seconds": f"{t:.3f}",
                    "relative_path": str(dst.relative_to(args.out_dir)),
                    "sha256": sha256(dst),
                    "source_media_file": src.name,
                    "future_bars_intentionally_excluded": "YES",
                    "badar_decision_label_in_packet": "NO",
                    "outcome_fields_in_packet": "NO",
                })
            except subprocess.CalledProcessError as exc:
                failures.append({
                    "decision_event_id": event_id,
                    "stream_id": stream_id,
                    "frame_label": label,
                    "frame_seconds": str(t),
                    "error": f"ffmpeg_exit_{exc.returncode}",
                })

        if n % 25 == 0:
            print(f"processed {n}/{len(ready)} events", file=sys.stderr)

    index_path = args.out_dir / "frame-index.csv"
    cols = [
        "decision_event_id",
        "stream_id",
        "stream_date",
        "source_stream_timestamp",
        "frame_label",
        "frame_seconds",
        "relative_path",
        "sha256",
        "source_media_file",
        "future_bars_intentionally_excluded",
        "badar_decision_label_in_packet",
        "outcome_fields_in_packet",
    ]
    with index_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(index_rows)

    report = {
        "manifest": str(args.manifest),
        "media_dir": str(args.media_dir),
        "out_dir": str(args.out_dir),
        "ready_events_requested": len(ready),
        "events_with_any_frame": len({r["decision_event_id"] for r in index_rows}),
        "frames_written": len(index_rows),
        "missing_media_streams": sorted(missing_media),
        "missing_media_stream_count": len(missing_media),
        "failures": failures,
        "future_bars_intentionally_excluded": True,
        "decision_labels_exported": False,
        "outcomes_exported": False,
        "downloads_performed": False,
    }
    (args.out_dir / "extraction-report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )

    print(json.dumps(report, indent=2))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
