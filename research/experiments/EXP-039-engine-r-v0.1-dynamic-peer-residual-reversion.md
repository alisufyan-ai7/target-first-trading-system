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
