# EXP-048 — Visual Replay Reviewer Rubric v0.1

**Status:** FROZEN BEFORE ANY EXP-048 CASE IS REVIEWED  
**Date:** 2026-09-28  
**Parent protocol:** `59d426bd56c82a7d48a6081bc695a7a8eaa657e7`

## Purpose

EXP-048 tests whether reviewing actual multi-timeframe chart geometry changes the quality of outcome-blind discretionary selection relative to EXP-047's compressed numeric/text cards.

The visual reviewer must judge only what is visible in the frozen chart packet. No post-decision data may be consulted.

## Default posture

Default:

`NO_TRADE`.

Take a trade only when the visual chart presents a coherent location + reaction + execution + target story.

## Visual dimensions

### Higher-timeframe auction

Use H1 and M15 to judge:

- trend, balance or transition;
- expansion versus compression;
- whether price is extended;
- whether the attacked level is at an outer edge or buried inside congestion;
- whether the proposed direction fights or aligns with the dominant auction.

### Location

Judge:

- significance of the attacked PDH/PDL/Asia/opening level;
- clustering of known levels;
- distance to the next opposing liquidity;
- whether price is trading at a clean edge or in the middle of a range.

### Attack and reaction

Use M5 and M1 visually to distinguish:

- clean rejection/reclaim;
- clean acceptance/hold;
- failed acceptance;
- compression/indecision;
- exhaustion after a large extension.

Do not convert one candlestick into a trade without surrounding structure.

### Execution

Prefer non-chasing entries.

A trade requires:

- identifiable causal entry;
- structural stop;
- target path visible before the decision boundary;
- no need for future confirmation to make the idea valid.

### Target path

TP1 must be either:

- a causally visible fresh external-liquidity level; or
- an explicitly frozen fixed-R objective when no external target is suitable but the chart geometry supports the trade.

Avoid trades with poor room or crowded path.

## Confidence

### A

Visually coherent across location, reaction, execution and target path with little important contradiction.

### B

Tradeable but with one meaningful conflict.

### C

Plausible but materially weaker. C is allowed but must not be upgraded later.

## Frozen label fields

LONG / SHORT:

- decision;
- confidence A/B/C;
- entryStyle;
- entryPrice or deterministic causal rule;
- stopPrice;
- tp1Price or explicit fixed-R intent;
- concise visual rationale;
- concise counterEvidence.

NO_TRADE:

- reason;
- dominant visual conflict.

## Anti-hindsight

The reviewer must not:

- open source data after decision timestamps;
- look up the date externally;
- search EXP-047 outcomes for analogous cases;
- infer outcomes from later repository result files;
- alter labels after any EXP-048 outcome is exposed.

All 126 labels must be frozen first.

## Feasibility gate

Before any outcome reveal:

- 126/126 labeled;
- >=30 trades;
- >=10 LONG;
- >=10 SHORT;
- >=20 A/B;
- every trade has causal entry, stop and TP1 intent;
- no overlap with EXP-047;
- protected periods sealed.

## Reviewer

The reviewer is the project ChatGPT research agent using the rendered chart images.

This is a test of visual information representation, not a claim that the reviewer is equivalent to a proven profitable human trader.
