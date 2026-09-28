# EXP-048 — Disjoint Outcome-Blinded Visual Gold Replay v0.1

**Status:** PROSPECTIVE / ZERO-OUTCOME VISUAL-REPLAY REPLICATION  
**Frozen:** 2026-09-28  
**Market:** XAUUSD  
**Parent methodological lesson:** EXP-047 closed negative at `eaf83fdc987aa03ab202d6b6531e0f50a9797b21`.

## 1. Why EXP-048 exists

EXP-047 completed a valid anti-hindsight test, but the reviewer consumed compressed numeric/text cards rather than the spatial multi-timeframe charts a discretionary trader normally sees.

EXP-048 tests one narrowly defined methodological question:

> Does genuinely visual multi-timeframe chart perception produce a materially better outcome-blind selection stream than the compact-card review?

This is **not** a relabeling or threshold rescue of EXP-047.

Every EXP-048 event must be disjoint from all 126 EXP-047 events.

## 2. Source and protected periods

Free source:

`kevingtlin/Market-Data-Lab@922f83a60cc574e7395fb27397077288055a1ef6`.

Warm-up:

- 2021-12-01 through 2021-12-31.

Replay development:

- 2022-01-01 through 2025-02-28.

Remain sealed:

- validation: 2025-03-01 through 2025-08-31;
- fresh holdout: 2025-09-01 through 2026-02-28.

No Mar-2025+ source file may be loaded.

## 3. Event universe

Use exactly the same zero-outcome event-universe mechanics as EXP-047:

- PDH;
- PDL;
- ASIA_HIGH;
- ASIA_LOW;
- OPEN_HIGH;
- OPEN_LOW.

First completed active-M5 attack consumes a level.

Eligible attack close:

- weekday;
- >=06:00 UTC;
- <16:30 UTC;
- development period.

Dual-sided attacks create no event.

Multiple same-side attacked levels use priority:

1. prior day;
2. Asia;
3. opening range.

Decision timestamp remains:

**15 market-active M1 bars after the attack M5 close**.

No candle after that decision timestamp is allowed in the replay packet or visual.

## 4. Deterministic disjoint selection

Use the same three eras:

- ERA1: 2022;
- ERA2: 2023;
- ERA3: 2024-01-01 through 2025-02-28.

Within each era × level-class cell:

1. construct all eligible events;
2. hash the same event identity used by EXP-047;
3. sort ascending by SHA-256;
4. EXP-047 used ranks 1–7;
5. EXP-048 uses **ranks 8–14**.

Required count:

`3 eras × 6 level classes × 7 = 126 events`.

Every cell must contain at least 14 eligible events.

The generator must verify zero event-hash overlap with the pinned EXP-047 packet set:

Git blob:

`e6eeeed45a0e0181b23d0d3ba3497b5521677c41`.

If any overlap exists, fail closed.

## 5. Causal packet content

Retain the causal packet structure:

- H1: up to 96 completed bars;
- M15: up to 96 completed bars;
- M5: up to 144 completed bars;
- M1: up to 180 completed bars;
- known external-liquidity snapshot at decision time;
- attack metadata;
- decision timestamp.

No future candle, MFE/MAE, outcome, target hit, P&L, or validation/holdout field.

## 6. Visual presentation

The review interface must render the frozen causal packet as an actual multi-timeframe chart.

Each case must show:

- H1;
- M15;
- M5;
- M1;
- OHLC candlesticks;
- attacked level visibly identified;
- other causally known external-liquidity levels visible and labeled;
- attack timestamp marker where meaningful;
- no data to the right of the frozen decision timestamp.

The renderer may change only presentation—not underlying packet data.

Charts must not contain:

- future candles;
- outcome markers;
- later targets/stops;
- win/loss annotations.

## 7. Visual reviewer rubric

Default:

`NO_TRADE`.

The visual reviewer must judge the complete causal chart, including:

- higher-timeframe trend / balance / extension;
- spatial location of attacked liquidity;
- nearby opposing liquidity and room;
- acceptance / rejection / failed acceptance;
- displacement, compression and congestion;
- whether execution would chase;
- structural invalidation;
- plausible target path.

A trade label is:

- LONG or SHORT;
- confidence A / B / C;
- entry style;
- causal entry price/rule;
- structural stop;
- TP1 intent;
- concise visual rationale;
- counter-evidence.

The reviewer must not use EXP-047 event outcomes as analog labels.

## 8. Label seal

All 126 EXP-048 labels must be frozen before any EXP-048 post-decision path is loaded.

Feasibility gate before outcome reveal:

- all 126 labeled;
- >=30 LONG+SHORT;
- >=10 LONG;
- >=10 SHORT;
- >=20 A/B trades;
- all trades have causal entry, stop and TP1 intent;
- zero EXP-047 event overlap;
- protected data sealed.

Do not manufacture trades to pass the gate.

## 9. Outcome stage

If the label seal passes, freeze a separate outcome/economic protocol before loading future paths.

No outcome rule is authorized by this source-packet specification itself.

## 10. Anti-rescue rule

EXP-048 is the **one permitted visual-representation replication**.

If its pooled blinded selection later fails its prospectively frozen economic gate:

- do not make EXP-049 as another replay-interface variation;
- do not relabel the cases;
- do not select favorable confidence/direction/era cohorts;
- move away from synthetic/model-generated discretionary selection.

## 11. Exact next action

Build one zero-outcome EXP-048 disjoint packet checkpoint and verify:

- 126 packets;
- 7 per era/class;
- zero overlap with EXP-047;
- causal integrity;
- no protected source;
- no future/outcome fields.
