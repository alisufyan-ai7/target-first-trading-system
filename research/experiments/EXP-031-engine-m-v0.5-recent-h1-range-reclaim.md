# EXP-031 — Engine M v0.5 Recent-H1 Range Sweep/Reclaim

**Status:** FROZEN PROSPECTIVELY — ZERO V0.5 OUTCOMES  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-m-mtf-reclaim-limit-entry/SPEC-v0.5.md`

## Purpose

Increase opportunity density without weakening the v0.4 frequency gate or changing the non-chasing execution architecture.

## Frozen change

At each M15 decision:

- test H1_0 range first;
- if it does not fully qualify, test H1_1;
- first qualifying range supplies both swept boundary and opposite target-room boundary;
- never create two setups from one M15 bar.

Everything else unchanged from v0.4.

## Zero-outcome preflight

Keep the **same** frozen v0.4 gate:

- >=25 filled valid signals per market;
- both directions every market;
- >=300 total;
- safety caps intact;
- no target/P&L outcomes;
- Jul-Aug/Sep sealed.

## Outcome state

- v0.5 outcomes: none;
- Jul-Aug: unopened;
- Sep: unopened.

## Next

Implement and run zero-outcome preflight only.
