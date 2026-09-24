# EXP-033 — Engine N v0.2 Rolling Intraday Drive Pullback

**Status:** FROZEN PROSPECTIVELY — ZERO OUTCOMES  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-n-rolling-drive-pullback/SPEC-v0.2.md`

## Purpose

Test the same displacement-pullback thesis under continuous hourly multi-market scanning after v0.1 failed only its zero-outcome opportunity-density gate.

## Frozen change from v0.1

Replace two named session anchors with 12 fixed hourly anchors:

`06:00 through 17:00 UTC inclusive`.

Each anchor keeps:

- 30m drive;
- prior-eight-M15 baseline;
- 1.50x expansion;
- 60% body;
- outer-25% close;
- 50% pullback limit;
- drive-extreme stop;
- 45-M1 / anchor+90m horizon.

One anchor's order horizon ends exactly when the next hourly anchor decision occurs.

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
