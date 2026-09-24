# EXP-035 — Engine O v0.2 Continuous M5 Statistical Reversion

**Status:** DEVELOPMENT RUNNER FROZEN — DEVELOPMENT OUTCOMES NEXT  
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


## Zero-outcome preflight — PASS

**Trigger SHA:** `0b91627ad0f216c8395ebaa5907b6173bf122526`  
**Durable result commit:** `6b637af`

Protection:

- target outcomes: **NO**;
- P&L outcomes: **NO**;
- parsed source max timestamp: **2026-06-30 23:59:00 UTC**;
- Jul-Aug secondary: unopened;
- Sep final holdout: unopened.

Frozen-gate result:

- filled valid signals: **574**;
- safely deployable: **574**;
- every market >=25: PASS;
- LONG and SHORT every market: PASS;
- total >=300: PASS;
- safety overlay: PASS.

Per-market signals:

- XAUUSD 68;
- EURUSD 82;
- GBPUSD 84;
- USDJPY 55;
- EURJPY 68;
- AUDUSD 73;
- USDCAD 70;
- USDCHF 74.

Utility:

- GE40 7;
- GE30 140;
- LT30 427.

**Disposition:** PASS. Engine O v0.2 may proceed to development while Jul-Aug and Sep remain sealed.

## Development outcome convention freeze

Before any development label:

- same six chronological slices as EXP-028/031/033;
- same audited target-first labeler;
- T40 vs trigger-extreme stop;
- same-bar stop first;
- max 120 active M1 bars;
- hard 20:00 UTC cutoff;
- normalized-R signal metrics;
- safe-lot USD500 one-open portfolio;
- matched immediate-entry control on the same non-suppressed qualified arm;
- time-of-day diagnostics descriptive only;
- >+0.20R pooled gross hurdle and all post-cost gates unchanged.

No v0.2 outcome existed at this freeze.


## Development implementation checkpoint — zero outcomes

Frozen before any EXP-035 development outcome:

- same six chronological development slices used by EXP-028/031/033;
- same audited target-first outcome labeler;
- T40 vs frozen trigger-extreme stop;
- same-bar stop first;
- max 120 active M1 bars;
- 20:00 UTC hard cutoff;
- same normalized-R signal metrics;
- same safe-lot USD500 one-open portfolio;
- same daily stop-adding-risk logic;
- same >+0.20R pooled gross hurdle;
- same post-cost expectancy / PF / drawdown / weekday / concentration gates;
- hour-of-day cohorts descriptive only;
- matched immediate-entry control descriptive only;
- no post-outcome hour/minute/symbol whitelist;
- Jul1 hard source seal.

Implementation commits:

- development runner: `152413d7b4a080a2ad3cf471da34c04a5188441c`;
- development workflow: `f9d2082c670853c753068c38d9c827deaa0d8a71`.

At this checkpoint:

- EXP-035 target outcomes: **NO**;
- EXP-035 P&L outcomes: **NO**;
- Jul-Aug loaded/labeled: **NO**;
- Sep loaded/labeled: **NO**.

### Next

Trigger EXP-035 development only. Any failed mandatory gate stops before secondary testing.
