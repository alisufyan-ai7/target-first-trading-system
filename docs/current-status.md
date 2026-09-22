# Current Status

**Date:** 2026-09-22  
**Phase:** System build / fixed-size multi-market scanner

## Source of truth

Only this repository and the originating chat are authorized project context.

## End objective

Build a multi-strategy, multi-asset scanner/execution system that:

- scans all supported liquid markets;
- ranks the best current long/short opportunities;
- uses fixed execution-size tiers rather than enlarging size to manufacture a USD 50 target;
- treats approximately USD 30–50 as useful ordinary captures;
- can hold toward USD 70–100+ when validated continuation evidence supports it;
- may take more than 3–4 trades/day when several independent qualified opportunities exist;
- never forces trades;
- works toward a USD 150–200 daily net P&L zone when sufficient validated opportunity exists;
- respects approximately -USD 40 normal / -USD 60 hard daily-loss controls.

These are operating objectives, not guaranteed outcomes.

## Fixed-size anchor

### XAUUSD

Reference size: **0.10 lot**.

Research convention pending broker verification:

- 0.10 lot = 10 oz;
- USD 1 Gold move ≈ USD 10 gross P&L;
- USD 3 / 4 / 5 / 7 / 10 move ≈ USD 30 / 40 / 50 / 70 / 100.

### Major FX

Initial research anchor: **0.10 standard lot**, pending broker-specific verification.

USD-quote majors are approximately USD 1/pip at 0.10 lot. JPY-quote pairs require contemporaneous JPY/USD conversion.

## Superseded framework

The prior dynamic USD 20 risk / USD 50 target model is no longer the forward execution model.

EXP-011 was superseded before results because the user changed the operating assumptions to fixed-size execution, flexible USD 30–100+ target capture, and opportunity-driven trade count.

## EXP-012 fixed-size results

### USDJPY / Engine A v0.2

At fixed 0.10 standard lot, holdout reconstruction showed:

- median structural-stop risk: about USD 2.24;
- median maximum favorable excursion: about USD 2.94;
- T30 hit: 7.14%;
- T50 hit: 4.08%;
- T100 hit: 3.06%.

Conclusion: the old USDJPY lead is not useful as a primary USD 30–100 fixed-size income stream.

### GBPUSD / Engine F v0.1

At fixed 0.10 standard lot, holdout reconstruction showed:

- median structural-stop risk: about USD 2.94;
- median maximum favorable excursion: about USD 3.70;
- T30 hit: 11.11%;
- T40 hit: 2.78%;
- T50/T70/T100: 0%.

Conclusion: the old GBPUSD lead is not useful as a primary USD 30–100 fixed-size income stream.

### XAUUSD / Engine A v0.2 — raw fixed-size economics

At fixed 0.10 lot, holdout reconstruction showed:

- median structural-stop risk: about USD 51.90;
- T30 hit: 57.14%;
- T40 hit: 41.35%;
- T50 hit: 36.84%;
- T70 hit: 29.32%;
- T100 hit: 22.56%.

Conclusion: Gold has the correct movement scale for the user's fixed-size objective, but the inherited Engine A structural stop is often too wide.

### XAUUSD / Engine A v0.2 — predeclared USD 40 stop-risk gate

Only setups whose unchanged structural stop costs <= USD 40 at 0.10 lot were admissible.

Holdout:

- 50 of 133 trades passed;
- 35 of 59 weekdays had at least one surviving trade;
- median stop risk: USD 29.82;
- T30 hit: 48%;
- T40 hit: 34%;
- T50 hit: 30%;
- T70 hit: 28%;
- T100 hit: 20%.

Fixed-target expectancy in holdout:

- T30: about **+USD 0.02/trade before costs**;
- T40: -USD 4.93/trade;
- T50: -USD 4.85/trade;
- T70: -USD 0.85/trade;
- T100: -USD 2.70/trade.

Conclusion: the risk-gated Gold subset is economically aligned with the desired lot/target structure, but the current Engine A entry logic does **not** provide a robust positive fixed-target edge. T30 is essentially break-even before costs.

## Current system conclusion

The project now separates two questions:

1. **Does the market naturally have enough fixed-size movement to produce USD 30–100?**
2. **Can the scanner identify entries where those moves are likely before structural invalidation?**

For the tested markets:

- USDJPY/GBPUSD fixed 0.10-lot movement from the retained entries is too small;
- XAUUSD has enough movement;
- the current Gold entry engine is not selective enough.

No existing engine is promoted to execution.

## Active next phase

Open a small checkpointed **market-universe economic feasibility map** before building the next target-first ranker.

The purpose is to identify which liquid markets naturally support the USD 30–100 target ladder at the fixed execution-size tier, using development-only volatility/economic data rather than strategy outcomes.

After that map is frozen, build the cross-market target-first opportunity-ranking layer on the economically suitable universe.

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

Which markets, at fixed economically sensible size, naturally provide enough intraday movement for USD 30–100 targets, and can a validated target-first ranker select those opportunities frequently enough to approach the USD 150–200 daily objective without unacceptable risk, margin use, or forced trading?

## EXP-013 market-economics update

Development-only fixed-size movement ranking has now been expanded.

First scanner universe frozen from economic suitability:

1. XAUUSD;
2. GBPUSD;
3. USDCHF;
4. EURUSD;
5. AUDUSD.

Supporting development-only observations:

- XAUUSD: T50 move is only about 0.233x median hourly TR at 0.10 lot.
- GBPUSD: T50 = 50 pips ≈ 2.703x median hourly TR / 0.708x median active-session range.
- USDCHF: T50 ≈ 38.9 pips ≈ 3.475x median hourly TR / 0.907x median session range.
- EURUSD: T50 = 50 pips ≈ 3.663x median hourly TR / 0.943x median session range.
- AUDUSD: T50 = 50 pips ≈ 3.968x median hourly TR / 0.973x median session range.

Lower-priority 0.10-lot markets:

- EURJPY;
- USDJPY;
- USDCAD.

XAGUSD remains unranked until a fixed contract/quantity convention is frozen. GBPJPY remains deferred because a matching clean sample was unavailable.

## Next experiment

Freeze and test the first target-first opportunity-ranking layer on the five-market scanner universe.

The ranker must:

- consume unchanged mechanical candidate setups;
- calculate fixed-size stop-dollar risk before entry;
- reject candidates above the USD 40 structural-risk gate;
- estimate T30/T40/T50/T70/T100 probability before stop;
- rank candidates across markets;
- use development data for model fitting/calibration;
- preserve a fresh later-period holdout for the new ranker;
- never represent probability as certainty.
