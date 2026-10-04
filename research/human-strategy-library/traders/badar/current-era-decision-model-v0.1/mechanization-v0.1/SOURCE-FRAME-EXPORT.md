# Source-Frame Export — Phase 2 Acquisition

## Why this exists

Claude's research workflow already downloaded Badar source streams and generated local frame sheets in:

`badartrader-research/`

The durable GitHub evidence repo intentionally does not contain those binary frame assets.

Target-First therefore must **reuse the existing Claude media cache**, not duplicate video research and not open protected Jul–Sep 2026 raw market data.

## Frozen request manifest

`source-frame-request.csv`

Contains 347 events:

- 345 READY in-stream events;
- 2 MANUAL_PRESTREAM events.

For every READY event, the requested visual evidence is:

- T−120 seconds
- T−60 seconds
- T−30 seconds
- T−5 seconds

All frames are before the frozen event anchor.

The manifest intentionally contains no Badar TRADE/WAIT/NO_TRADE decision label.

## Extractor

`tools/extract_source_frames.py`

The extractor never downloads video.

It requires:

- Python 3
- ffmpeg
- the existing Claude `media/` directory

Example from a checkout of Target-First:

```bash
python3 research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.1/tools/extract_source_frames.py \
  --media-dir "$HOME/Documents/badartrader-research/media" \
  --out-dir "$HOME/Documents/badar-phase2-source-frames"
```

If Claude's workspace is mounted elsewhere, change only `--media-dir`.

## Pilot first

Before exporting all 345 events:

```bash
python3 research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.1/tools/extract_source_frames.py \
  --media-dir "$HOME/Documents/badartrader-research/media" \
  --out-dir "$HOME/Documents/badar-phase2-source-frames-pilot" \
  --limit 10
```

Verify:

- frames are readable;
- no frame is later than the frozen event timestamp;
- no future price path is shown beyond what was visible in the live stream at that time;
- no trade result text has been added by the export;
- extraction report says `downloads_performed: false`.

## Output

The extractor writes:

```text
<out-dir>/
  events/
    <decision_event_id>/
      <event>__m120.jpg
      <event>__m060.jpg
      <event>__m030.jpg
      <event>__m005.jpg
  frame-index.csv
  extraction-report.json
```

`frame-index.csv` includes SHA-256 for every frame.

## Transfer into ChatGPT / Target-First

Do not commit all source-video frames to Git by default.

Preferred transfer:

1. package `events/`, `frame-index.csv`, and `extraction-report.json` as one archive;
2. attach the archive to this Project/conversation or place it in a Project-accessible file surface;
3. verify hashes against `frame-index.csv`;
4. run blinded annotation from the frames.

## Existing contact sheets

If the full `media/` cache is unavailable but Claude's existing `sheets/` directory remains available, preserve it as secondary evidence.

Do not silently substitute sparse contact-sheet frames for the exact T−5/T−30/T−60/T−120 extraction without recording that downgrade.

## Two pre-stream events

The following are intentionally not assigned synthetic stream positions:

- `1E65DgTFxe0-PE-001`
- `aEw6393GE1c-PB5-001`

They require pre-stream source evidence already documented by Badar/Claude and remain separate from the 345 exact in-stream frame cases.

## Scientific status after export

Frame extraction alone does not reveal P&L and does not complete Phase 2.

After transfer, perform:

1. two independent blinded annotations;
2. agreement/kappa calculation;
3. label freeze;
4. formal-policy replay;
5. reveal Badar's decision only for behavioral-fidelity analysis;
6. still keep P&L sealed.
