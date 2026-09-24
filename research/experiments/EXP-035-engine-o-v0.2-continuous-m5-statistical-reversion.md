# EXP-035 — Engine O v0.2 Continuous M5 Statistical Reversion

**Status:** FROZEN PROSPECTIVELY — ZERO OUTCOMES  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-o-continuous-m5-statistical-stretch-reversion/SPEC-v0.2.md`

## Purpose

Test the same statistical-stretch mean-reversion thesis under continuous five-minute scanning after v0.1 failed only the zero-outcome opportunity-density gate.

## Frozen change from v0.1

Replace the 15-minute decision grid with every completed M5 bar:

`06:05 through 17:55 UTC`.

Everything else is unchanged:

- prior 24 M5 CENTER/MAD state;
- 2.50 MAD stretch;
- 1.25x trigger range;
- 50% body;
- outer-35% rejection close;
- 50% pullback limit;
- trigger-extreme stop;
- 10-active-M1 / 30m order life;
- T40 must fit before CENTER;
- unchanged safe-lot overlay.

## Preflight

Keep the same gate:

- >=25 filled signals per market;
- both directions;
- >=300 total;
- no outcomes;
- protected periods sealed.

## Outcome state

No v0.2 outcomes exist at freeze.

## Next

Implement and run zero-outcome preflight only.
