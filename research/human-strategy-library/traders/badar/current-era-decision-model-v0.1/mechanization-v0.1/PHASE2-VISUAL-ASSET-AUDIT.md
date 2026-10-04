# Phase-2 Visual Asset Audit

**External visual asset commit:** `be4c0463a0dbdf759a3b352ce462c4ed1664fca9`  
**Frozen source-evidence logic commit:** `d19a43da80ae0e3ab4207a73a35f317120d37c84`

## Coverage

The external Badar repo now contains:

- **319** stream contact-sheet JPEGs;
- **43** stream IDs with visual sheets;
- all **42/42** streams in the frozen v0.1 decision corpus;
- one extra post-freeze stream, `PYPzCJV-YXE` (2026-10-01), kept outside v0.1.

There are no raw stream-video files under the pushed `evidence/` tree.

## Contact-sheet format

Stream sheets are 2×2 panels. Each panel contains a contemporaneous source-stream chart frame with a yellow stream-time label.

Example verified visually:

`evidence/frames/streams/CPGcMydNbbQ_00.jpg`

contains panels labelled:

- 0:00
- 3:00
- 5:00
- 6:40

The sheets are therefore genuine source visual evidence, but an individual JPEG can contain both pre-event and post-event panels.

## Blinding consequence

A full contact sheet is formally safe only when **all panels in that sheet occur at or before the frozen decision timestamp**.

If any panel in the same JPEG is after the decision timestamp, using the whole image would expose future chart state.

Therefore:

- current sheets are sufficient for a feasibility pilot;
- current sheets are sufficient for some events whose timestamp is after the final panel of a sheet;
- current sheets are **not sufficient for universal formal blinding** until split into individual panels.

## Visual readability

Manual connector inspection confirms the sheets preserve enough resolution to read:

- chart timeframe in many cases;
- major horizontal levels;
- highs/lows;
- position boxes;
- candle structure;
- range position;
- some volume panels;
- many chart timestamps.

This is sufficient to attempt the v0.1 state labels conservatively.

## Independence limitation

This ChatGPT conversation created/read the source-informed corpus before Phase 2.

Therefore any visual annotation produced here is:

`ANNOTATOR_A_FEASIBILITY / NON_SCORING`

It cannot count as one of the two fully independent blinded annotators required by the frozen protocol.

A future independent pass must be performed without access to:

- Badar's final decision label;
- source-event paraphrase revealing the decision;
- this pilot's labels.

## Required panel-split artifact

The next binary transformation is deterministic and outcome-free:

```text
2×2 contact sheet
    -> top-left panel
    -> top-right panel
    -> bottom-left panel
    -> bottom-right panel
```

No image generation or reconstruction is allowed.

Each panel must retain its embedded yellow source timestamp.

After panel splitting, event packets can include only panels with:

`panel_timestamp <= frozen_event_timestamp`

and exclude every later panel.

## Scientific status

`PHASE2_VISUAL_ASSETS_COVER_42_OF_42 — PANEL_SPLIT_REQUIRED_FOR_FORMAL_BLINDING`
