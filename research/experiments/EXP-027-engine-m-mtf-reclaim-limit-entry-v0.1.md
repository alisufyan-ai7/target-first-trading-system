# EXP-027 — Engine M v0.1 Multi-Timeframe Reclaim Limit Entry

**Status:** FROZEN PROSPECTIVELY — ZERO ENGINE-M OUTCOMES  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-m-mtf-reclaim-limit-entry/SPEC-v0.1.md`

## Purpose

Test the user-guided top-down intraday architecture directly:

`4H/1H context -> 15m setup/location -> 5m tactical arm -> non-chasing lower-timeframe entry`.

Engine M removes the Engine-K/L ML probability model and uses interpretable causal timeframe roles.

## Prior evidence allowed

Mar-Jun is reusable development evidence.

Known before freeze:

- Engine K ranking signal did not convert robustly to economic edge;
- Engine L pullback/resumption raised hit rate but chased price;
- Engine L median executed entry was ~0.516 V5 worse than decision close;
- raw score quartiles were not monotonically profitable.

Protected Jul-Aug and Sep remain unopened.

## Frozen center mechanics

- H4 and H1 close direction must align;
- M15 must interact with and reclaim the last completed H1 midpoint;
- final M5 bar must reject in context direction with outer-quartile close;
- no market entry;
- pre-place 50% M5-range retracement limit;
- stop beyond M5 arm extreme;
- order lives 10 active M1 bars, no later than 18:00 UTC;
- T40 only;
- same USD20 risk/notional/margin/cost framework.

No parameter grid.

## Matched control

Same MTF arms:

- immediate next-M1-open entry;
- same M5 structural stop;
- same T40 economics.

This isolates the value of the non-chasing limit entry.

## Zero-outcome preflight

Before any P&L:

- exact timeframe/causality/unit tests;
- >=50 admissible filled paths per execution market;
- both directions on every market;
- >=600 total paths;
- no protected-period access.

## Outcome status

At freeze:

- Engine-M outcomes: NO;
- control outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.

## Next

Implement causal MTF/limit mechanics and run zero-outcome preflight only.


## Preflight attempt 1 — infrastructure verification failure

**Workflow run:** `35995612463`  
**Trigger SHA:** `83751ee054de59418f93a5426c348ed7090f6cb5`

The run failed in the deterministic verification step **before** the actual market preflight executed.

Root cause:

- the synthetic Engine-M self-test constructed integer-typed H4/H1 OHLC columns;
- the short-context mirror test then assigned `0.5` into the integer `close` column;
- the current pandas runtime rejected that incompatible dtype mutation.

This was a **test-fixture implementation defect**, not a strategy/preflight research failure.

Evidence status from attempt 1:

- market preflight executed: **NO**;
- Engine-M target outcomes: **NO**;
- Engine-M P&L outcomes: **NO**;
- Jul-Aug loaded/inspected: **NO**;
- Sep loaded/inspected: **NO**.

Correction:

- synthetic H4/H1 OHLC fixtures now use floating-point values from construction;
- strategy mechanics, thresholds, timeframe rules, entry price, stop, target, risk/cost assumptions and preflight gates are unchanged.

Fix commit:

`569cc707571f063fb5b9b939cfba08555273086a`

### Next

Rerun the identical frozen zero-outcome EXP-027 preflight.
