# Current Status

**Date:** 2026-09-22  
**Phase:** System build / fixed-size target-ladder scanner validation

## Source of truth

Only this repository and the originating chat are authorized project context.

## End objective

Build a multi-strategy, multi-asset scanner/execution system that:

- scans all supported liquid markets;
- ranks the best long/short opportunities;
- uses fixed execution-size tiers rather than enlarging size to force a USD 50 target;
- targets approximately USD 30–50 on ordinary successful trades;
- can hold toward USD 70–100+ when validated continuation evidence supports it;
- may take more than 3–4 trades/day when multiple independent qualified opportunities exist;
- never forces trades;
- works toward a USD 150–200 daily net P&L zone when sufficient opportunity exists;
- respects the approximately -USD 40 normal / -USD 60 hard daily-loss framework.

This is an operating objective, not a guaranteed daily outcome.

## Fixed-size anchor

### XAUUSD

Reference size: **0.10 lot**.

Under the common 100-oz-per-lot convention:

- USD 3 favorable move ≈ +USD 30;
- USD 4 ≈ +USD 40;
- USD 5 ≈ +USD 50;
- USD 7 ≈ +USD 70;
- USD 10 ≈ +USD 100.

Broker specifications must be verified before execution.

### Major FX

Initial research anchor: **0.10 standard lot** unless actual broker specifications justify another fixed equivalent.

For USD-quote majors this is approximately USD 1/pip, so roughly 30/40/50/70/100 pips correspond to the same target ladder.

JPY-quote pip values require contemporaneous JPY/USD conversion.

## Retained research leads

### USDJPY / Engine A v0.2

Historical fixed-risk screen:

- development mean R: about +0.075R/trade;
- holdout mean R: about +0.263R/trade;
- holdout <= USD 50 days: 86.44%.

Status: **research lead only; must now be re-evaluated at fixed 0.10-lot economics.**

### GBPUSD / Engine F v0.1

Historical fixed-risk screen:

- development mean R: +0.138R/trade;
- holdout mean R: +0.080R/trade;
- holdout <= USD 50 days: 100%.

Status: **research lead only; must now be re-evaluated at fixed 0.10-lot economics.**

## EXP-010 result under superseded economic framing

The two leads were low-correlated but the fixed USD 20 risk / USD 50 target portfolio still produced:

- 86.44% <= USD 50 holdout days;
- 44.07% losing holdout days;
- no >= USD 150 holdout day;
- extreme notional/margin requirements from dynamic risk sizing.

This is evidence against dynamic sizing to force USD 50, not a final rejection of the leads under the newly clarified fixed-size objective.

## EXP-011

EXP-011 was checkpointed as a fixed +USD 50 / -USD 20, maximum-4-trades analytical feasibility model.

It was **superseded before results** because the user changed the operational assumptions to:

- fixed lot/exposure tiers;
- flexible USD 30–100+ target ladder;
- opportunity-driven trade count.

No EXP-011 result was used.

## Active experiment — EXP-012

**Fixed-Size Target-Ladder and Multi-Market Scanner Economics.**

First tasks:

1. map fixed-size P&L economics for the existing five-market universe;
2. reconstruct USDJPY / Engine A v0.2 at 0.10 standard lot;
3. measure T30/T40/T50/T70/T100 before structural invalidation;
4. measure actual fixed-size stop-dollar risk;
5. checkpoint;
6. repeat for GBPUSD / Engine F v0.1;
7. then decide whether to expand markets or introduce another engine.

## Current market universe

Existing data/records:

- XAUUSD;
- XAGUSD;
- EURUSD;
- GBPUSD;
- USDJPY.

Priority additions as clean data and contract economics become available:

- GBPJPY;
- EURJPY;
- AUDUSD;
- USDCAD;
- USDCHF;
- NAS100 / USTEC;
- US30;
- US500 / SPX500;
- BTCUSD / BTCUSDT where venue economics are explicitly defined.

## Key unresolved question

Can a broad scanner using fixed-size positions and flexible target capture produce enough **qualified** USD 30–100 opportunities across markets to approach the USD 150–200 daily objective without unacceptable stop risk, margin usage, drawdown, or forced trading?
