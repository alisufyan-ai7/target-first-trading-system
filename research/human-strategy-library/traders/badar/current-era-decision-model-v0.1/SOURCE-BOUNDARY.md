# Source Boundary — Badar Current-Era Decision Model v0.1

## Canonical external evidence repository

Repository:

`alisufyan-ai7/unpack-human-trading-strategies-claude`

Pinned v0.1 commit:

`d19a43da80ae0e3ab4207a73a35f317120d37c84`

Commit timestamp:

`2026-09-30T19:41:11Z`

Latest included live stream:

- `EOBnMz2Y_9k`
- 2026-09-30
- NY-session Gold live stream
- three logged trade rows, of which the first was a team/VIP signal that Badar explicitly said he did not take.

Latest included daily forecast:

- `Cwu3UcAXLz8`
- 2026-09-30 Gold Daily Forecast.

## Included evidence

Use only the external repository's source layer:

- `PLAYBOOK.md`;
- `LIVE_TRADING_OBSERVATIONS.md`;
- `dataset/live_trades.csv`;
- `notes/videos/**`;
- `notes/shorts/**`;
- `notes/streams/**`;
- `transcripts/**`;
- `INDEX.md`;
- `STREAMS_INDEX.md`;
- `tracker/**`;
- source-layer `README.md`.

At the pinned commit:

- 143 long videos;
- 114 Shorts;
- 42 live streams;
- 113 live-trade rows.

## Explicitly excluded evidence

Do **not** use:

- `derived/**`;
- Claude's grades;
- Claude's pseudo-code;
- Claude's default parameter choices;
- Claude's conflict resolutions;
- Claude's labelled/derived profitability statistics;
- the AI system prompt in the external repository.

Those are researcher/AI interpretations, not Badar-source evidence.

## Relationship to the local BADAR-VID-001 record

The local Target-First folder `BADAR-VID-001/` is preserved as historical direct-ingest research.

It was **not required as evidence for this v0.1 model**.

The separate Claude repository is now the canonical Badar source-extraction repository. Target-First should avoid duplicating per-video extraction unless an independent audit is specifically needed.

## Current-era weighting

### Tier A — direct current behavior

Primary evidence:

- 2026 live streams, especially Jul–Sep;
- explicit `WAIT`, `NO_TRADE`, reduced-risk and early-exit decisions;
- actual timeframe switching and management behavior.

### Tier B — current teaching

Primary teaching era:

- 2024–2026 Liquidity Concept;
- current daily forecasts;
- recent strategy videos/Shorts.

### Tier C — older consistent material

Older SMC/ICT/course material is supporting evidence only when current behavior still agrees.

### Tier D — historical conflicting material

Older rules that later behavior contradicts are preserved as evolution evidence, not promoted into v0.1 as hard rules.

## No-outcome rule

No P&L or outcome analysis is authorized in this evidence-synthesis stage.

Trade outcomes may exist in the external source dataset because they document what occurred live, but v0.1 is **not selected or tuned using those outcomes**.

The next decision-event extraction must omit future outcome fields during classification.

## Daily-update policy

The external repository is a live evidence feed and may receive a new stream or forecast every day.

Therefore:

1. v0.1 remains pinned forever to `d19a43d...`.
2. New commits are reviewed as **evidence deltas**.
3. If a new source only adds examples consistent with v0.1, record it as supporting evidence.
4. If a new source materially changes a decision rule, create a new model version rather than silently rewriting v0.1.
5. Once a future test specification is frozen, no later source may modify that version's rules after outcomes are inspected.
6. New evidence after a test freeze belongs to the next prospective version.

This is the evidence equivalent of a sealed validation boundary.
