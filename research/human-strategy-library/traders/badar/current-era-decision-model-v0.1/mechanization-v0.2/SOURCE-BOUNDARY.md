# Source Boundary — Badar Mechanization v0.2

## Frozen external evidence commit

`bd0037e06a881a066e0cd8070b635cace59240d1`

Repository:

`alisufyan-ai7/unpack-human-trading-strategies-claude`

This commit is frozen for the v0.2 reproducibility study.

Later external-repo commits are evidence deltas for a future version and may not silently alter v0.2.

## Relation to v0.1

v0.1 was pinned to:

`d19a43da80ae0e3ab4207a73a35f317120d37c84`

The v0.2 test tranche uses **only live streams not present in the frozen v0.1 42-stream corpus**.

No v0.1 annotation case is recycled into the v0.2 reproducibility test.

## Fresh live-stream tranche

Eight post-v0.1 live sessions are present at the v0.2 cutoff:

1. `PYPzCJV-YXE` — 2026-10-01
2. `PxDGTxs-Cvc` — 2026-10-02
3. `EsAa5_T_kbQ` — 2026-10-06
4. `D85FC79tI6w` — 2026-10-08
5. `6wwmBYPvmPQ` — 2026-10-14
6. `_9vCesQpBtM` — 2026-10-15
7. `of0Pv8JP4eE` — 2026-10-23
8. `wXbKuO5lVGg` — 2026-10-26

## Allowed source layer

Only Badar source-layer material under the pinned commit:

- `traders/badar-tanveer/notes/streams/`
- `traders/badar-tanveer/transcripts/streams/`
- `traders/badar-tanveer/evidence/stream_frames/`
- source-linked visual/contact-sheet evidence where needed

## Excluded

- all `derived/**` material;
- Claude AI-rule interpretations;
- Badar decision outcomes when constructing blind packet state;
- trade P&L;
- result R;
- MFE/MAE;
- future candles after the frozen event timestamp;
- any post-cutoff live stream.

## Visual representation

v0.2 uses the full-resolution single-frame source assets added to the Claude evidence workflow.

Across the eight fresh streams there are **201 full-resolution source frames** with timestamped filenames.

This avoids the 2×2 contact-sheet future-panel ambiguity present in v0.1.

## Decision-label handling

The public v0.2 candidate manifest intentionally contains **no TRADE / WAIT / NO_TRADE label**.

Behavioral labels remain recoverable from the pinned source notes only after the reproducibility gate passes.

No behavioral-fidelity reveal is authorized before that gate.

## Freeze

`BADAR_MECHANIZATION_V0_2_SOURCE_BOUNDARY_FROZEN`
