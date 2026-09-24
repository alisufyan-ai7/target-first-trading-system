# EXP-026 — Engine L v0.1 Forecast-Armed Micro Pullback Entry

**Status:** ZERO-OUTCOME ENTRY-MECHANICS PREFLIGHT PASSED — DEVELOPMENT NEXT  
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

## Zero-outcome preflight gate

Before any Engine-L outcome:

- mechanics/unit tests must pass;
- each execution market must produce >=100 mechanically triggerable and economically admissible T40 entry paths through Jun30;
- both directions must be represented on every market;
- Jul-Aug and Sep remain unloaded.

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


## Zero-outcome mechanics preflight — PASS

**Workflow run:** `35986445374`  
**Durable result commit:** `b19d4ef6c3a689117fc5b8237167322bd64a2aa7`  
**Result:** `research/results/EXP-026-entry-mechanics-preflight-v0.1.json`

Protection at checkpoint:

- Engine-L target outcomes calculated: **NO**;
- Engine-L P&L outcomes calculated: **NO**;
- forecast model fitted: **NO**;
- Jul-Aug secondary loaded/inspected: **NO**;
- Sep final holdout loaded/inspected: **NO**.

Mechanics result:

- total examined decision-direction paths: 274,666;
- total admissible micro-entry paths: 12,532;
- every execution market exceeded the frozen >=100-path minimum;
- every market produced both long and short admissible triggers;
- median wait-to-entry was about 6-7 active M1 bars across markets.

Per-market admissible paths:

- XAUUSD 1,748;
- EURUSD 1,129;
- GBPUSD 1,665;
- USDJPY 906;
- EURJPY 705;
- AUDUSD 3,938;
- USDCAD 435;
- USDCHF 2,006.

**Disposition:** PASS. Engine-L mechanics are sufficiently abundant and balanced to justify the prospectively frozen development test.

No profitability conclusion is implied by this preflight.


## Final pre-outcome matched-domain clarification

Before Engine-L development outcomes:

- forecast fit/evaluation sides are restricted to the same complete, pre-probability economically admitted T40 state domain used by the Engine-K v0.2/v0.3 forecast model;
- this restriction is intentional so EXP-026 isolates **entry timing + execution stop** rather than candidate-universe expansion;
- Engine-L recomputes T40 economics at its later micro-entry using the fresh M1 stop;
- exact LONG/SHORT raw-score ties use lower old-reference stop risk, then LONG;
- pending-arm resolution is tracked causally so later 5m decisions cannot overlap an unresolved same-symbol arm.

No Engine-L target/P&L outcome had been calculated when these mechanics were frozen.
