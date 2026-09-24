# EXP-032 — Engine N v0.1 Session Opening Drive Pullback

**Status:** FROZEN PROSPECTIVELY — ZERO OUTCOMES  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-n-session-opening-drive-pullback/SPEC-v0.1.md`

## Purpose

Test a genuinely different intraday family after closing Engine M.

Thesis:

`major-session opening displacement -> first 50% pullback -> continuation`.

## Frozen center design

- London anchor 07:00 UTC;
- New York anchor 13:30 UTC;
- first 30 exact clock minutes define opening drive;
- eight preceding exact M15 bars define volatility baseline;
- drive range >=1.50x baseline median;
- body >=60%;
- close in directional outer 25%;
- entry at 50% drive range;
- stop one research tick beyond drive extreme;
- order life 45 active M1 bars / max anchor+90m;
- unchanged T40 and safe-lot overlay.

No H1 sweep/reclaim logic. No ML threshold.

## Zero-outcome preflight

Require:

- >=25 filled valid signals per market;
- both directions every market;
- >=300 total;
- exact chronology and boundary tests;
- safety caps pass;
- zero target/P&L outcomes;
- Jul-Aug/Sep sealed.

## Outcome state

- outcomes: none;
- Jul-Aug: unopened;
- Sep: unopened.

## Next

Implement Engine N v0.1 mechanics and run zero-outcome preflight only.
