# EXP-031 — Engine M v0.5 Recent-H1 Range Sweep/Reclaim

**Status:** ZERO-OUTCOME PREFLIGHT PASSED — DEVELOPMENT NEXT  
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


## Preflight attempt 1 — verification implementation failure

**Workflow run:** `36009869842`  
**Trigger SHA:** `6df0eb309b60d43a429d26c2bd752ec887f9d656`

The workflow failed in the deterministic verification step before the market preflight ran.

Root cause:

- the v0.5 helper returned an M5 geometry dictionary containing `status="ok"`;
- the qualifying return path set `status="armed"` **before** unpacking that helper dictionary;
- Python therefore overwrote `armed` with `ok`;
- the non-qualifying path had the same collision and could overwrite `no_recent_h1_range_qualified` with `ok`.

This was an implementation-field collision, not a strategy/preflight research failure.

Evidence status from attempt 1:

- market preflight executed: **NO**;
- EXP-031 target outcomes: **NO**;
- EXP-031 P&L outcomes: **NO**;
- Jul-Aug loaded/inspected: **NO**;
- Sep loaded/inspected: **NO**.

Corrections:

- qualifying return now unpacks geometry first and sets `status="armed"` afterward;
- non-qualifying return now unpacks geometry first and sets `status="no_recent_h1_range_qualified"` afterward;
- no strategy mechanics, recency order, target-room rule, frequency gate, sizing, cost or safety rule changed.

Fix commits:

- `5335a440edc0ad3a58995dfa0bb16b08fb91713b`;
- `a50cf398e57fd13fb1ac1e8b26fbe701df1e1cf9`.

### Next

Rerun the identical frozen EXP-031 zero-outcome preflight.


## Zero-outcome preflight — PASS

**Retry workflow run:** `36010384519`  
**Retry trigger SHA:** `7ff211f748245ed744a4dfea2563dd02032fded2`  
**Durable result commit:** `e0c7566`

Protection:

- target outcomes: **NO**;
- P&L outcomes: **NO**;
- Jul-Aug: unopened;
- Sep: unopened.

Frozen-gate result:

- filled valid signals: **417**;
- deployable signals: **417**;
- every market >=25: PASS;
- LONG and SHORT every market: PASS;
- total >=300: PASS;
- safety overlay: PASS.

Per-market signals:

- XAUUSD 64;
- EURUSD 50;
- GBPUSD 51;
- USDJPY 44;
- EURJPY 55;
- AUDUSD 53;
- USDCAD 52;
- USDCHF 48.

Selected H1 range counts among armed setups:

- H1_0: 340;
- H1_1: 268.

Reference-account utility across filled signals:

- GE40: 16;
- GE30: 35;
- LT30: 366.

**Disposition:** PASS. v0.5 may proceed to development while Jul-Aug and Sep remain sealed.
