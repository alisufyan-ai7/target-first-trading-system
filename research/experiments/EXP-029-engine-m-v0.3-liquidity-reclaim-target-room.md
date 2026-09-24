# EXP-029 — Engine M v0.3 Liquidity Reclaim + HTF Target-Room

**Status:** FROZEN PROSPECTIVELY — ZERO V0.3 OUTCOMES  
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
