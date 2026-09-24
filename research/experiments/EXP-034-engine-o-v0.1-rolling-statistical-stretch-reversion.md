# EXP-034 — Engine O v0.1 Rolling Statistical Stretch Reversion

**Status:** FROZEN PROSPECTIVELY — ZERO OUTCOMES  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-o-rolling-statistical-stretch-reversion/SPEC-v0.1.md`

## Purpose

Test a genuinely different continuous-scanning mean-reversion family after Engine N continuation failed development.

## Frozen center design

Every 15 minutes from 06:15 through 17:45 UTC:

- use prior 24 completed M5 bars;
- robust center = median close;
- dispersion = median absolute deviation of close;
- trigger close stretched >=2.50 MAD from center;
- trigger range >=1.25x prior median M5 range;
- body >=50%;
- bullish rejection below center / bearish rejection above center;
- close in favorable outer 35%;
- enter 50% retracement of trigger M5;
- stop beyond trigger extreme;
- order life 10 active M1 / decision+30m;
- unchanged T40 must fit before CENTER;
- unchanged signal-first safe-lot overlay.

## Zero-outcome preflight

Keep the scanner opportunity-density gate:

- >=25 filled signals per market;
- both directions;
- >=300 total;
- safety/causality tests pass;
- no target/P&L outcomes;
- Jul-Aug/Sep sealed.

## Outcome state

No Engine-O outcomes exist at freeze.

## Next

Implement Engine O v0.1 mechanics and run zero-outcome preflight only.
