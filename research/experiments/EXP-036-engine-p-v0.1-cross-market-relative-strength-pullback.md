# EXP-036 — Engine P v0.1 Cross-Market Relative-Strength Pullback

**Status:** FROZEN PROSPECTIVELY — ZERO OUTCOMES  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-p-cross-market-relative-strength-pullback/SPEC-v0.1.md`

## Purpose

Test a genuinely different information source after isolated-symbol M/N/O families failed development.

Engine P uses contemporaneous cross-market factor confirmation.

## Frozen center design

Every completed M5 bar from 06:05-17:55 UTC:

- own 30m normalized momentum from prior 24-M5 range-vol baseline;
- own |MOM| >=1.50;
- USD_SCORE from other USD-linked FX markets, threshold 0.50;
- EURJPY uses EURUSD + USDJPY leg confirmation;
- current M5 bar confirms direction with >=35% body and outer-40% close;
- enter 50% M5 pullback;
- stop beyond trigger extreme;
- 10-active-M1 / 30m order life;
- unchanged T40 and safe-lot overlay.

## Preflight

Require:

- >=25 filled signals per market;
- both directions;
- >=300 total;
- all cross-market alignment / causality / execution / safety tests pass;
- no target/P&L outcomes;
- Jul-Aug/Sep sealed.

## Outcome state

No Engine-P outcomes exist at freeze.

## Next

Implement Engine P v0.1 and run zero-outcome preflight only.
