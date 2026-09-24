# EXP-026 — Engine L v0.1 Forecast-Armed Micro Pullback Entry

**Status:** FROZEN PROSPECTIVELY — ZERO ENGINE-L OUTCOMES  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-l-forecast-armed-micro-entry/SPEC-v0.1.md`

## Why this experiment exists

The Engine-K series revealed a structural problem in the research architecture:

the probability layer was being asked to do the job of **entry timing**.

Engine K converted a completed 5m state almost directly into a next-M1-open entry. It did not wait for a favorable execution price or fresh M1 confirmation.

EXP-026 isolates that issue.

## Thesis

A useful directional forecast should **arm** a market, not force an immediate trade.

A trade occurs only after:

1. a causal favorable pullback;
2. a causal M1 resumption confirmation;
3. a fresh execution-level stop is available;
4. safe T40 economics pass.

## Frozen configuration

One center configuration only:

- fixed M2 HGB raw T40 forecast;
- higher-scoring direction armed per market;
- 15 active-M1 arm lifetime;
- 0.20*V5 required pullback;
- M1 break/resumption bar with outer-quartile close;
- next-M1-open entry;
- fresh pullback-extreme stop;
- Gold T40 = 4 XAU;
- non-Gold T40 = 2R;
- same USD20 risk/notional/margin/cost framework.

No parameter grid.

## Matched control

Use the same forecast arms but enter immediately at the next M1 open with the old 5m pivot stop.

This directly tests whether execution timing/stop freshness improves economics.

## Evidence

Development:

- Mar23-Jun30 reusable.

Protected:

- Jul-Aug unopened;
- Sep unopened.

Use the same six forward folds as EXP-025.

## Gate

Engine L must independently be profitable/stable and materially beat the matched immediate-entry control.

See SPEC-v0.1 for exact frozen criteria.

## Outcome status

At freeze:

- Engine-L outcomes: NO;
- matched-control outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.

## Next

Implement exact causal entry engine + six-fold development runner. Preflight it before outcomes, then run development only if entry mechanics pass.
