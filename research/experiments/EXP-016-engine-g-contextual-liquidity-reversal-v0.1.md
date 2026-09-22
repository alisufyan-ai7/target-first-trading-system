# EXP-016 — Engine G Contextual Liquidity Reversal v0.1 Prospective Validation

**Date frozen:** 2026-09-23  
**Status:** FROZEN / NOT YET RUN  
**Engine:** Engine G — Contextual Liquidity Reversal v0.1  
**Frozen specification:** `strategies/engine-g-contextual-liquidity-reversal/SPEC-v0.1.md`  
**Outcome status at experiment creation:** ZERO ENGINE-G OUTCOMES CALCULATED

## Purpose

Prospectively test whether Engine G v0.1 produces a causal, reproducible, cost-robust and economically admissible XAUUSD candidate stream across development, validation and an untouched same-feed holdout.

Engine G is a new engine. It is not recovered Engine A and must not be interpreted as an EXP-002 reproduction.

## Governing rule

The complete mechanical definition is the frozen Engine G v0.1 strategy specification. That file governs all implementation and outcome interpretation. No parameter or lifecycle rule may be changed inside EXP-016 after development begins.

## Frozen center configuration

- market: XAUUSD;
- primary path: frozen Dukascopy-derived BID M1;
- source grid: 0.001 XAU represented as integer ticks;
- 15m context: 48 market-active completed 15m bars;
- 5m swing prominence: >= 0.50 * simple ATR(14), using the exact integer formula in the spec;
- sweep/setup creation: qualifying completed 5m sweeps from 06:00 to <18:00 UTC;
- liquidity consumption: every market-active completed 5m bar regardless of UTC hour;
- internal pivot: causal 1m 2L2R;
- MSS search: 10 market-active M1 bars;
- displacement: MSS/MSS+1/MSS+2, body >=1.60x prior-20 market-active M1 mean body;
- FVG: frozen explicit bullish/bearish inequalities;
- entry: grid-aligned FVG midpoint;
- stop: one source tick beyond completed 5m sweep extreme;
- gross structural-risk admission: <=$40 at XAU 0.10 lot / 10 oz convention;
- actual v0.1 exit: 100% at S1;
- minimum S1 room: 3.000 XAU / 3,000 ticks;
- counterfactual labels: independent T30/T40/T50/T70/T100 from original entry, unchanged stop and unchanged horizon, ignoring actual S1 exit;
- horizon: 120 market-active M1 bars or 20:00 UTC, whichever occurs first;
- one accepted open Engine-G XAUUSD trade at a time;
- primary round-trip cost stress: 0.50 XAU / 500 ticks / $5 per filled trade;
- same-bar ambiguity: conservative stop-first treatment.

## Frozen external source snapshot

Repository:

`kevingtlin/Market-Data-Lab`

Repository commit:

`922f83a60cc574e7395fb27397077288055a1ef6`

Root tree:

`6596cd229c736f96bab7d1496656397b31326ca6`

XAUUSD BID M1 subtree:

`86dd3acd141ffe4b5eb8ad86a04ca42398d0b558`

XAUUSD ASK M1 subtree:

`bf346b8c4c79bd6a0eee33e3b1114d4d855e646f`

The full frozen BID monthly-file manifest and per-file blob SHAs are in Sections 41–43 of the Engine G v0.1 specification.

## Frozen primary split

### Warm-up only

`2023-12-01 through 2023-12-31 UTC`

No evaluation outcome is credited to warm-up.

### Development

`2024-01-01 00:00 UTC through 2025-02-28 23:59 UTC`

### Validation

`2025-03-01 00:00 UTC through 2025-08-31 23:59 UTC`

### Fresh primary holdout

`2025-09-01 00:00 UTC through 2026-02-28 23:59 UTC`

### Quarantined prior-research period

`2026-03-01 through 2026-08-20`

This period was extensively used in earlier project research and is excluded from the primary development/validation/holdout decision. It may be inspected only after the complete center-rule primary experiment is finished and checkpointed.

## Contamination audit

Earlier Target-First strategy-result windows recorded in the repository begin in March 2026. The EXP-016 validation and fresh-holdout periods are therefore outside previously recorded project strategy-development/result windows.

## Required execution order

1. verify immutable source snapshot and file manifest;
2. implement and run unit/causality tests;
3. run development only;
4. checkpoint development result to GitHub;
5. only then run validation;
6. checkpoint validation;
7. only then run fresh holdout;
8. checkpoint holdout;
9. write primary v0.1 conclusion;
10. only then run the predeclared sensitivity diagnostics;
11. checkpoint sensitivity;
12. only then optionally run the quarantined March–August 2026 diagnostic;
13. independent-feed validation remains separate.

## Delayed sensitivity diagnostics

These are predeclared but must not be calculated before the complete 48/1.60 primary development/validation/holdout sequence is checkpointed:

- context32 / displacement1.60;
- context64 / displacement1.60;
- context48 / displacement1.40;
- context48 / displacement1.80.

They are parameter-cliff diagnostics only. They may never replace v0.1 because one neighbor performs better.

## Minimum evidence

Required accepted filled trades:

- development >=100;
- validation >=50;
- holdout >=50.

If a split falls below its minimum, disposition is `INSUFFICIENT_EVIDENCE`, not an automatic pass or rejection.

## Primary historical-edge promotion criteria

Using actual S1-strategy P&L under the frozen 0.50-XAU round-trip stress:

1. development expectancy/trade >0;
2. validation expectancy/trade >0;
3. holdout expectancy/trade >0;
4. validation profit factor >=1.10;
5. holdout profit factor >=1.10;
6. validation 95% moving-block-bootstrap expectancy lower bound >0;
7. holdout 95% moving-block-bootstrap expectancy lower bound >0;
8. no expectancy sign reversal across development/validation/holdout;
9. minimum evidence satisfied;
10. no causal leakage;
11. no optimistic same-bar handling;
12. no source/provenance violation.

Maximum drawdown and consecutive-loss behavior are mandatory promotion evidence but have no newly invented hard EXP-016 cutoff.

Passing EXP-016 does not authorize live execution.

## Mandatory reporting

Each primary split must report the full metric set frozen in Section 49 of the Engine G specification, including:

- setup funnel and deterministic rejection reasons;
- accepted trades;
- S1/stop/timeout rates;
- independent counterfactual T30/T40/T50/T70/T100 labels;
- gross and cost-stressed expectancy;
- profit factor;
- total/mean/median daily P&L;
- low-output and high-output-day proportions;
- maximum drawdown;
- consecutive-loss behavior;
- actual MFE/MAE;
- counterfactual potential MFE/MAE;
- structural-risk and target-distance distributions;
- liquidity/target-class attribution;
- bootstrap uncertainty.

## Failure discipline

No post-outcome retuning is permitted inside v0.1. A material rule change requires Engine G v0.2 or another explicitly versioned experiment.

## Checkpoint 0 — frozen before outcomes

Engine G v0.1 and EXP-016 were frozen in GitHub before any Engine-G development, validation or holdout outcome calculation.

At this checkpoint:

- specification frozen: YES;
- data source/split frozen: YES;
- promotion evidence frozen: YES;
- sensitivity sequence frozen: YES;
- Engine G outcomes calculated: NO;
- development backtest started: NO.
