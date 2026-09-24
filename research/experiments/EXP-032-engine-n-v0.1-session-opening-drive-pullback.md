# EXP-032 — Engine N v0.1 Session Opening Drive Pullback

**Status:** CLOSED — ZERO-OUTCOME PREFLIGHT FREQUENCY FAIL  
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


## Zero-outcome preflight outcome — FAIL

**Workflow run:** `36011937435`  
**Trigger SHA:** `ca3f020c8228e646290623db5b8d23fa0c94c20a`  
**Durable result commit:** `2c97f71`

Protection:

- target outcomes: **NO**;
- P&L outcomes: **NO**;
- Jul-Aug: unopened;
- Sep: unopened.

Result:

- filled valid signals: **123**;
- safely deployable: **122**;
- required total: >=300;
- every market failed the >=25-per-market gate;
- LONG + SHORT existed on every market;
- safe overlay passed.

Per-market filled signals:

- XAUUSD 11;
- EURUSD 14;
- GBPUSD 23;
- USDJPY 19;
- EURJPY 12;
- AUDUSD 16;
- USDCAD 15;
- USDCHF 13.

Utility:

- GE40 5;
- GE30 99;
- LT30 18;
- NONDEPLOYABLE 1.

The opening-drive qualification itself was not pathologically rare, but only two fixed session anchors per weekday limited the candidate stream too severely for the project's desired multi-market daily opportunity density.

### Metadata note

The durable result's `parsed_market_data_max_timestamp` string contains a generator representation because of a reporting-parentheses bug in the preflight runner.

This field is descriptive metadata only. The actual loader hard-sealed every market at `SEALED_START = 2026-07-01`, and the protected-period flags are false. The defect does not change the research gate or signal counts.

**Disposition:** insufficient frequency. Do not calculate v0.1 outcomes.

### Next design implication

Do not lower the >=300 / >=25-per-market gate.

Prospectively broaden the same displacement-pullback thesis from two named sessions to **continuous non-overlapping hourly scanning during the active intraday window**.

That becomes Engine N v0.2 / EXP-033.
