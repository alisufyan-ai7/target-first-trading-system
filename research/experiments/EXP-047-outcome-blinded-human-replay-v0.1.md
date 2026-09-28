# EXP-047 — Outcome-Blinded Human-Style Gold Replay v0.1

**Status:** PROSPECTIVE / ZERO-OUTCOME SOURCE-PACKET STAGE  
**Frozen:** 2026-09-28  
**Market:** XAUUSD  
**Source:** free pinned `kevingtlin/Market-Data-Lab` BID M1  
**Source commit:** `922f83a60cc574e7395fb27397077288055a1ef6`

## 1. Why EXP-047 exists

Engine S and Engine T were deliberately designed around human-style liquidity concepts, but both failed their prospectively frozen development economics.

Do not respond by immediately encoding another verbal motif.

The project now tests a different research question:

> Can an outcome-blinded human-style review of causal multi-timeframe context select a coherent A-grade subset before any future path is visible?

This is a research-process experiment, not yet an execution engine.

## 2. Core anti-leak rule

Every replay packet must contain only information available at or before a frozen decision timestamp.

It must contain **no**:

- future candle;
- target label;
- MFE / MAE;
- win/loss flag;
- realized R;
- realized USD P&L;
- post-decision path summary;
- validation / holdout source file.

The complete replay labels must be frozen before any post-decision path may later be evaluated.

## 3. Development-only source interval

Warm-up:

- 2021-12-01 through 2021-12-31.

Replay source-development:

- 2022-01-01 through 2025-02-28.

Protected and not loaded:

- validation: 2025-03-01 through 2025-08-31;
- fresh holdout: 2025-09-01 through 2026-02-28.

## 4. Outcome-blind event universe

The event universe is intentionally broad and causal.

Use the same reproducible meaningful external-liquidity classes already present in project research:

- PDH;
- PDL;
- ASIA_HIGH;
- ASIA_LOW;
- OPEN_HIGH;
- OPEN_LOW.

Definitions:

- prior-day high/low: prior active UTC day;
- Asia high/low: 00:00-06:00 UTC, known from 06:00;
- opening high/low: 06:00-09:00 UTC, known from 09:00.

A level's **first completed active-M5 attack** consumes it.

Attack:

- HIGH level: M5 high > level;
- LOW level: M5 low < level.

Replay events are eligible only when the first attack M5 closes:

- weekday;
- >=06:00 UTC;
- <16:30 UTC;
- in 2022-01-01 through 2025-02-28.

If one attack M5 hits both a fresh high-side and low-side level, consume those levels but create no replay event.

If multiple same-side levels are first-attacked on the same M5, keep one replay event using priority:

1. prior-day;
2. Asia;
3. opening range.

No target/path information participates in event selection.

## 5. Frozen replay decision timestamp

The replay decision point is **15 market-active M1 bars after the attack M5 close**.

The 15-bar reaction window is part of the observable context, not an outcome label.

The event is excluded if:

- 15 later active M1 bars do not exist on the same UTC day;
- the decision timestamp is >=18:00 UTC.

No candle after the decision timestamp may enter the packet.

## 6. Deterministic stratified selection

Predeclare three eras:

- ERA1: 2022-01-01 through 2022-12-31;
- ERA2: 2023-01-01 through 2023-12-31;
- ERA3: 2024-01-01 through 2025-02-28.

For each era and each of the six level classes:

1. build all eligible replay events;
2. compute SHA-256 of the event identity string;
3. sort ascending by hash;
4. select the first **7**.

Required packet count:

`3 eras x 6 classes x 7 = 126 events`.

This selection is outcome-blind and deterministic.

If any era/class cell has <7 eligible events, the packet-generation gate fails closed.

## 7. Causal packet content

Each packet contains:

### Event metadata

- replay event ID;
- era;
- level class / side / price;
- level knowledge timestamp;
- attack M5 start / close;
- frozen decision timestamp.

### Multi-timeframe OHLC windows

Only bars fully completed by decision time:

- H1: up to 96 completed bars;
- M15: up to 96 completed bars;
- M5: up to 144 completed bars;
- M1: up to 180 completed bars.

All prices remain integer source ticks.

### Causal level snapshot

For each external level known by decision time:

- class;
- side;
- price;
- known timestamp;
- whether it had already been attacked by the decision timestamp.

Do not include when a still-fresh level will later be attacked.

## 8. Replay-label contract — frozen before packets are reviewed

The eventual reviewer may choose exactly one primary decision:

- `NO_TRADE`;
- `LONG`;
- `SHORT`.

For LONG / SHORT, the reviewer must freeze before future data is revealed:

- decision rationale in concise structured text;
- entry style from:
  - `MARKET_NEXT_OPEN`;
  - `LEVEL_RETEST`;
  - `FVG_RETRACE`;
  - `OTHER_CAUSAL_LIMIT`;
- intended entry price or deterministic entry rule;
- structural stop price / anchor;
- TP1 target class / price or explicit fixed-R target;
- optional TP2 intent;
- confidence:
  - `A`;
  - `B`;
  - `C`.

No reviewer may inspect post-decision candles before submitting the label.

The labels themselves must be checkpointed durably before outcome evaluation.

## 9. Feasibility gate before any outcome reveal

Before post-decision evaluation is authorized:

- all 126 packets must pass leakage integrity;
- all 126 must receive a frozen primary decision;
- there must be >=30 total LONG+SHORT labels;
- there must be >=10 LONG and >=10 SHORT;
- at least 20 trade labels must be confidence A or B;
- every trade label must have a causal stop and target intent.

If the reviewer produces too few tradeable setups, do not loosen packet selection after seeing outcomes because no outcomes have yet been opened. A separate replay-design decision would be required first.

## 10. Scientific role

EXP-047 does **not** validate a deployable system by itself.

Its purpose is to answer whether outcome-blinded contextual review can isolate a meaningfully smaller candidate stream that deserves formalization.

If later outcome evaluation is promising and stable, the next step is:

1. analyze the frozen contextual rationales;
2. formalize common causal traits into a reproducible Engine U;
3. freeze Engine U prospectively;
4. test it on still-sealed data.

If replay economics fail, do not claim discretionary edge.

## 11. Governance

The source-packet stage is zero-outcome.

Do not:

- inspect post-decision candles;
- use Engine S/T outcome cohorts to select packet events;
- hand-pick dates;
- remove losing-looking contexts after future reveal;
- change the 7-per-era/class deterministic sample after packet generation.

Exact next action after this specification:

> Build one deterministic EXP-047 causal replay-packet checkpoint. Do not label or evaluate outcomes in the same run.
