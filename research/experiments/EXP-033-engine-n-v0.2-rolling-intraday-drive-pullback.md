# EXP-033 — Engine N v0.2 Rolling Intraday Drive Pullback

**Status:** DEVELOPMENT RUNNER FROZEN — DEVELOPMENT OUTCOMES NEXT  
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


## Zero-outcome preflight — PASS

**Trigger SHA:** `256929b292c5e9c0e2ded3bd78f3ceee0a5583ee`  
**Durable result commit:** `2b8c781`

Protection:

- target outcomes: **NO**;
- P&L outcomes: **NO**;
- parsed source max timestamp: **2026-06-30 23:59:00 UTC**;
- Jul-Aug secondary: unopened;
- Sep final holdout: unopened.

Frozen-gate result:

- filled valid signals: **626**;
- safely deployable: **624**;
- every market >=25: PASS;
- LONG and SHORT every market: PASS;
- total >=300: PASS;
- safety overlay: PASS.

Per-market filled signals:

- XAUUSD 57;
- EURUSD 81;
- GBPUSD 89;
- USDJPY 78;
- EURJPY 65;
- AUDUSD 79;
- USDCAD 86;
- USDCHF 91.

Utility:

- GE40 32;
- GE30 474;
- LT30 118;
- NONDEPLOYABLE 2.

**Disposition:** PASS. Engine N v0.2 may proceed to development while Jul-Aug and Sep remain sealed.


## Development implementation checkpoint — zero outcomes

Frozen before any EXP-033 development outcome:

- same six chronological development slices used by EXP-028/031;
- same audited target-first labeler;
- T40 vs frozen stop, same-bar stop first;
- maximum 120 active M1 bars counting entry;
- 20:00 UTC hard session cutoff;
- same normalized-R signal metrics;
- same safe-lot USD500 one-open portfolio;
- same daily stop-adding-risk logic;
- same >+0.20R pooled gross hurdle;
- same post-cost expectancy / PF / drawdown / weekday / concentration gates;
- hourly-anchor cohorts reported diagnostically only;
- matched immediate control = first active M1 open after each qualified 30m drive, independent of later pullback fill;
- no post-outcome hour selection;
- Jul1 hard source seal.

Implementation commits:

- development runner: `48d527d0c0359c231ffb0f4d193c0d4c1495e5e0`;
- development workflow: `bb4e70614a83a89086b276a9287fbbbf6996224a`.

At this checkpoint:

- EXP-033 target outcomes: **NO**;
- EXP-033 P&L outcomes: **NO**;
- Jul-Aug loaded/labeled: **NO**;
- Sep loaded/labeled: **NO**.

### Next

Trigger EXP-033 development only. Any failed mandatory gate stops before secondary testing.
