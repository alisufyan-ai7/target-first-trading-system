#!/usr/bin/env python3
"""Split Claude's pushed 2x2 stream contact sheets into source-faithful panels.

No OCR, no generative editing, no chart reconstruction, no future-data logic.
The embedded yellow timestamp is preserved because each quadrant is cropped intact.

Run against a local checkout of unpack-human-trading-strategies-claude.
"""

from __future__ import annotations
import argparse
import csv
import hashlib
from pathlib import Path
from PIL import Image


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-dir", type=Path, required=True,
                    help="Path to evidence/frames/streams in Claude repo checkout")
    ap.add_argument("--out-dir", type=Path, required=True)
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    rows = []

    for sheet in sorted(args.source_dir.glob("*.jpg")):
        with Image.open(sheet) as im:
            w, h = im.size
            # Claude media_pipeline creates 2 columns and up to 2 rows.
            xmid = w // 2
            ymid = h // 2
            boxes = [
                ("p0_tl", (0, 0, xmid, ymid)),
                ("p1_tr", (xmid, 0, w, ymid)),
                ("p2_bl", (0, ymid, xmid, h)),
                ("p3_br", (xmid, ymid, w, h)),
            ]
            # Last sheet can contain fewer than 4 source frames, leaving white/blank quadrants.
            # We preserve every quadrant first; blank filtering is a separate deterministic step.
            for label, box in boxes:
                crop = im.crop(box)
                dst = args.out_dir / f"{sheet.stem}__{label}.jpg"
                crop.save(dst, quality=95)
                rows.append({
                    "source_sheet": sheet.name,
                    "source_sheet_sha256": digest(sheet),
                    "panel": label,
                    "panel_file": dst.name,
                    "panel_sha256": digest(dst),
                    "width": crop.width,
                    "height": crop.height,
                })

    idx = args.out_dir / "panel-index.csv"
    cols = ["source_sheet","source_sheet_sha256","panel","panel_file",
            "panel_sha256","width","height"]
    with idx.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    print(f"sheets={len(list(args.source_dir.glob('*.jpg')))} panels={len(rows)}")
    print(idx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
