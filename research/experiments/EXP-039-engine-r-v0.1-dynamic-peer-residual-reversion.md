# EXP-039 — Engine R v0.1 Dynamic Peer-Residual Reversion

**Status:** PROSPECTIVE FREEZE — ZERO OUTCOMES  
**Date:** 2026-09-25  
**Strategy:** `strategies/engine-r-dynamic-peer-residual-reversion/SPEC-v0.1.md`  
**Provenance:** `research/provenance/EXP-039-engine-r-v0.1-source-manifest.md`

## Purpose

Test a genuinely different information source after Engine Q failed development.

Engine R uses **dynamic causal co-movement and relative-value residual displacement**.

Flow:

`rolling strongest peer -> sign-adjusted normalized 15m expectation -> candidate residual extreme -> same-bar reversion rejection -> non-chasing 50% limit -> T40`.

## Distinction from prior families

- not Engine P: no fixed USD factor / directional consensus;
- not Engine Q: no volatility breadth or lag-breakout spillover;
- not Engine O: residual is cross-market relative value, not isolated own-price stretch.

## Frozen center mechanics

- completed M5 decisions 06:05-17:55 UTC;
- prior 48 M5 returns estimate candidate-peer correlation;
- strongest absolute-correlation peer selected causally;
- require |rho|>=0.60;
- normalized current 15m move uses median absolute prior-48 15m moves;
- selected peer |NM15|>=1.00;
- candidate residual vs sign-adjusted peer >=1.50 in absolute value;
- trade candidate toward peer-implied relationship;
- current M5 must reject in reversion direction with >=35% body and outer-40% close;
- enter 50% retracement;
- stop beyond rejection bar;
- unchanged T40 and safe-lot overlay.

## Source / protection

- source begins Mar23 for state;
- hard source seal Jun30 23:59 UTC;
- Jul-Aug secondary sealed;
- Sep final holdout sealed.

## Zero-outcome preflight

Require all causality/correlation/residual/entry/safety tests plus:

- >=25 filled signals per market;
- both directions every market;
- >=300 total;
- target/P&L outcomes zero;
- protected periods unopened.

Do not lower the gate if frequency fails.

## Development if preflight passes

Use the same six fixed folds, audited target-first labeler and one-open USD500 portfolio.

Frozen mandatory development gate remains:

- >+0.20R pooled gross;
- post-cost primary/stress >0;
- >=4/6 stress-positive folds;
- >=90 reference trades;
- >=35 trade weekdays;
- reference expectancy positive;
- PF and MDD hurdles;
- concentration/provenance/protection gates.

## Outcome state

At freeze:

- target outcomes NO;
- P&L outcomes NO;
- Jul-Aug unopened;
- Sep unopened.

## Exact next action

Implement Engine R v0.1 and run zero-outcome EXP-039 preflight only.


## Zero-outcome implementation checkpoint

Frozen before any Engine-R target/P&L outcome:

- engine implementation commit: `8d31d100a747e8c666117b94e825535c7c35cf08`;
- preflight runner commit: `fac8bf178c981ddb5e2f8d45be3b9e6673ca0913`;
- workflow commit: `db879da22f4ec6ab3a7ca497f110f847b7ff373f`;
- engine blob: `d4516a8eb607fca6c26106e1d33b3de3226ccc10`;
- runner blob: `c996834b38a6cf89f41cb57b7ea8264328c0ed1d`;
- workflow blob: `e8bcf489bbd9dffa8a631c2fa6aa95712b06bae1`.

At this checkpoint:

- target outcomes: **NO**;
- P&L outcomes: **NO**;
- Jul-Aug loaded/labeled: **NO**;
- Sep loaded/labeled: **NO**.

**Next:** trigger exactly one EXP-039 zero-outcome preflight and do not mutate frozen inputs while it runs.
