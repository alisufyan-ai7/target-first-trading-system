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
