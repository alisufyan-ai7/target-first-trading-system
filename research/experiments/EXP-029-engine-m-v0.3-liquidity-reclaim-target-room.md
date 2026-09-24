# EXP-029 — Engine M v0.3 Liquidity Reclaim + HTF Target-Room

**Status:** CLOSED — ZERO-OUTCOME PREFLIGHT FREQUENCY FAIL  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-m-mtf-reclaim-limit-entry/SPEC-v0.3.md`

## Purpose

Increase pre-cost signal selectivity after EXP-028 showed a small positive gross edge that failed costs.

## Prior evidence used

EXP-028 development:

- v0.2 gross +0.0367R;
- primary -0.1625R;
- stress -0.3616R;
- immediate-control gross -0.0146R;
- 0/6 positive-stress folds.

This supports preserving the non-chasing limit entry while strengthening setup/context selectivity.

## Frozen v0.3 changes

Trading execution remains unchanged.

New selection gates:

1. M15 must strictly sweep the prior four contiguous M15-bar local extreme and reclaim it;
2. S15 must also reclaim the latest completed H1 midpoint;
3. frozen T40 target price must lie no farther than a recent completed H1 directional liquidity extreme from the latest two H1 bars.

No ML model. No parameter grid.

## Zero-outcome preflight

Require before outcomes:

- exact causality/unit tests;
- >=35 filled valid signals per market;
- both directions every market;
- >=400 total signals;
- safe overlay remains valid;
- zero target/P&L outcomes;
- Jul-Aug and Sep sealed.

## Development gate if preflight passes

Same six frozen development slices.

In addition to positive primary/stress economics, v0.3 must demonstrate **gross normalized expectancy > +0.20R** so the new selectivity creates materially more raw edge than v0.2.

## Outcome state

At freeze:

- v0.3 outcomes: none;
- Jul-Aug: unopened;
- Sep: unopened.

## Next

Implement v0.3 mechanics and run zero-outcome preflight only.


## Zero-outcome preflight outcome — FAIL

**Workflow run:** `36002890180`  
**Trigger SHA:** `9a8179a43a41b4bcc67584f17a175764157ef8bd`  
**Durable result commit:** `c078179`

Protection:

- target outcomes: **NO**;
- P&L outcomes: **NO**;
- Jul-Aug: unopened;
- Sep: unopened.

Result:

- filled valid signals: **106**;
- deployable signals: **106**;
- required total: >=400;
- every market failed the >=35-per-market gate;
- both directions existed on every market;
- safety overlay passed.

Per-market filled signals:

- XAUUSD 19;
- EURUSD 10;
- GBPUSD 13;
- USDJPY 14;
- EURJPY 15;
- AUDUSD 9;
- USDCAD 12;
- USDCHF 14.

Utility:

- GE40 5;
- GE30 11;
- LT30 90.

Structural diagnosis:

- the recent-H1 target-destination filter rejected only a modest number of otherwise qualified setups;
- the dominant frequency collapse occurred earlier from combining strict prior-4-M15 sweep/reclaim, H1-midpoint reclaim, and M5 arm.

**Disposition:** insufficient frequency. Do not calculate v0.3 outcomes.

### Next design implication

Do not relax the same conjunction one threshold at a time.

Use one coherent higher-timeframe location object instead:

`latest completed H1 range -> M15 sweep/reclaim of directional boundary -> unchanged M5 arm -> unchanged non-chasing limit -> opposite H1 boundary as target-room check`.

This becomes Engine M v0.4 / EXP-030.
