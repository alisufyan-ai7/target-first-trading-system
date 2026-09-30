# Badar Strategy Evidence

This directory is the canonical evidence base for material attributed to Badar.

## Objective

Reconstruct Badar's actual decision process from primary-source material rather than from our previous assumptions about his strategy.

The working questions include:

- what context he checks before considering a trade;
- what levels matter and why;
- what makes an otherwise valid setup low quality;
- what confirms direction;
- how he chooses entry timing;
- how he places invalidation;
- how he chooses targets;
- whether he scales, trails, waits, or exits early;
- how session and time influence decisions;
- which chart details he treats visually rather than mechanically;
- which cases he explicitly avoids.

## Source IDs

Use sequential IDs:

- `BADAR-VID-001`
- `BADAR-VID-002`
- ...
- `BADAR-POST-001`
- `BADAR-FB-001`
- etc.

Each source gets its own folder:

`BADAR-VID-001/`

Recommended contents:

- `source.md` — metadata and provenance;
- `analysis.md` — timestamped evidence extraction;
- `frames/` — only necessary research frames;
- `strategy-notes.md` — cumulative implications, clearly separated from direct evidence.

## Important rule

Do not assume that an idea is part of Badar's strategy because it resembles ICT/SMC/liquidity terminology or because our previous engines used it.

It counts as Badar-source evidence only when the uploaded material supports it.


## Source index

| Source ID | Type | Short description | Status |
|---|---|---|---|
| `BADAR-VID-001` | Video | Top 5 entry confirmations: engulfing, two-candles rejection, momentum shift, inverse closing, same-zone confluence | Analyzed; single-source evidence only |

Cumulative synthesis: `CUMULATIVE-SYNTHESIS.md`.


## 2026-10-01 workflow change — external extraction repository

Routine Badar YouTube/video/stream extraction is no longer duplicated in Target-First.

Canonical extraction repository:

`alisufyan-ai7/unpack-human-trading-strategies-claude`

That repository separates Badar-source material from `derived/**` AI interpretation and is updated with new live sessions.

Target-First now consumes the **source layer only** and owns:

- independent synthesis;
- decision-model reconstruction;
- outcome-blind formalization;
- frozen experiments;
- validation.

Historical `BADAR-VID-001/` remains preserved, but future source IDs do not need to be duplicated here unless an independent audit is specifically required.

### Current model

`current-era-decision-model-v0.1/`

Frozen external evidence commit:

`d19a43da80ae0e3ab4207a73a35f317120d37c84`

Latest included live session:

`EOBnMz2Y_9k` — 2026-09-30.

No P&L test has been run from this decision model.
