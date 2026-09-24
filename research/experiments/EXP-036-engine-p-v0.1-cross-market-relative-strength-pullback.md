# EXP-036 — Engine P v0.1 Cross-Market Relative-Strength Pullback

**Status:** DEVELOPMENT RUNNER FROZEN — DEVELOPMENT OUTCOMES NEXT  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-p-cross-market-relative-strength-pullback/SPEC-v0.1.md`

## Purpose

Test a genuinely different information source after isolated-symbol M/N/O families failed development.

Engine P uses contemporaneous cross-market factor confirmation.

## Frozen center design

Every completed M5 bar from 06:05-17:55 UTC:

- own 30m normalized momentum from prior 24-M5 range-vol baseline;
- own |MOM| >=1.50;
- USD_SCORE from other USD-linked FX markets, threshold 0.50;
- EURJPY uses EURUSD + USDJPY leg confirmation;
- current M5 bar confirms direction with >=35% body and outer-40% close;
- enter 50% M5 pullback;
- stop beyond trigger extreme;
- 10-active-M1 / 30m order life;
- unchanged T40 and safe-lot overlay.

## Preflight

Require:

- >=25 filled signals per market;
- both directions;
- >=300 total;
- all cross-market alignment / causality / execution / safety tests pass;
- no target/P&L outcomes;
- Jul-Aug/Sep sealed.

## Outcome state

No Engine-P outcomes exist at freeze.

## Next

Implement Engine P v0.1 and run zero-outcome preflight only.


## Zero-outcome preflight — PASS

**Durable result commit:** `12c6f5d`  
**Result file blob:** `b2816dce94507e9d75153d62002196a42a1284df`

Protection:

- target outcomes: **NO**;
- P&L outcomes: **NO**;
- parsed source max timestamp: **2026-06-30 23:59:00 UTC**;
- Jul-Aug secondary: unopened;
- Sep final holdout: unopened.

Frozen-gate result:

- filled valid signals: **6,063**;
- safely deployable: **6,059**;
- every market >=25: PASS;
- LONG + SHORT every market: PASS;
- total >=300: PASS;
- safety overlay: PASS.

Per-market filled signals:

- XAUUSD 576;
- EURUSD 943;
- GBPUSD 913;
- USDJPY 773;
- EURJPY 227;
- AUDUSD 878;
- USDCAD 800;
- USDCHF 953.

Utility:

- GE40 105;
- GE30 1,253;
- LT30 4,701;
- NONDEPLOYABLE 4.

**Disposition:** PASS. Engine P may proceed to development while Jul-Aug and Sep remain sealed.

## Development outcome convention freeze

Before any development label:

- same six chronological slices as EXP-028/031/033/035;
- same audited target-first labeler;
- T40 vs trigger-bar structural stop;
- same-bar stop first;
- max 120 active M1 bars;
- 20:00 UTC hard cutoff;
- same normalized-R signal metrics;
- same safe-lot USD500 one-open portfolio;
- same >+0.20R pooled gross hurdle;
- same post-cost expectancy / PF / drawdown / weekday / concentration gates;
- matched immediate-entry control on the same non-suppressed qualified arm;
- MOM/USD_SCORE/EURJPY-leg/time-of-day diagnostics descriptive only;
- no post-outcome threshold/hour/symbol rescue;
- Jul1 hard source seal.

No Engine-P development outcome existed at this freeze.


## Development implementation checkpoint — zero outcomes

Frozen before any EXP-036 development outcome:

- same six chronological development slices used by EXP-028/031/033/035;
- same audited target-first labeler;
- T40 vs frozen trigger-bar structural stop;
- same-bar stop first;
- max 120 active M1 bars;
- 20:00 UTC hard cutoff;
- same normalized-R signal metrics;
- same safe-lot USD500 one-open portfolio;
- same >+0.20R pooled gross hurdle;
- same post-cost expectancy / PF / drawdown / weekday / concentration gates;
- matched immediate-entry control on the same non-suppressed qualified arm;
- own-MOM / USD_SCORE / EURJPY-leg / hour / market diagnostics are descriptive only;
- no post-outcome factor-threshold, hour, symbol or direction whitelist;
- Jul1 hard source seal.

Implementation commits:

- development runner: `82335c86c4e82d6bd5f17eb822ed83aeb8e9d41b`;
- development workflow: `2c2e84f4f92529f629c67a9738e36c411ed71c65`.

At this checkpoint:

- EXP-036 target outcomes: **NO**;
- EXP-036 P&L outcomes: **NO**;
- Jul-Aug loaded/labeled: **NO**;
- Sep loaded/labeled: **NO**.

### Next

Trigger EXP-036 development only. Any failed mandatory gate stops before secondary testing.
