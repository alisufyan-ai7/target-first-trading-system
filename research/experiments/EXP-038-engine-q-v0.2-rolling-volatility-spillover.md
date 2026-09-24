# EXP-038 — Engine Q v0.2 Rolling Cross-Market Volatility Spillover

**Status:** PROSPECTIVE FREEZE — ZERO OUTCOMES  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-q-cross-market-volatility-spillover-breakout/SPEC-v0.2.md`  
**Provenance:** `research/provenance/EXP-038-engine-q-v0.2-source-manifest.md`

## Purpose

Retest the volatility-spillover hypothesis after EXP-037 failed only zero-outcome opportunity density.

EXP-037's same-bar 4-peer shock synchronization was too sparse. No target/P&L outcomes were inspected.

EXP-038 preserves shock severity and breadth, but lets a peer contribute if it shocked within the immediately preceding 15 minutes.

## Frozen change from v0.1

Unchanged:

- peer VR shock threshold 1.75;
- 4 unique peers required;
- candidate excluded;
- candidate VR<=1.00;
- prior-six-M5 frozen box;
- next-six-M5 breakout arm;
- breakout VR>=1.25;
- body>=50%;
- outer-25% close;
- 50% retracement limit;
- structural stop;
- T40;
- costs;
- safety;
- opportunity-density gate;
- development gates.

Changed:

- same-bar peer breadth -> rolling three-completed-M5 peer memory (t, t-5, t-10);
- each peer counted once at most.

## Frozen source / split

Only source through 2026-06-30.

Six development folds unchanged from EXP-037.

Jul-Aug and Sep remain sealed.

## Zero-outcome gate

Require:

- rolling-memory causality and unique-peer counting tests;
- all existing arm/breakout/entry/safety tests;
- >=25 fills per market;
- both directions every market;
- >=300 total;
- zero target/P&L outcomes;
- Jun30 source seal;
- protected periods unopened.

Do not lower the gate if frequency still fails.

## Development gate

If preflight passes, use the same >+0.20R gross hurdle and all post-cost/stability/reference-account gates already frozen in Engine Q v0.2 spec.

## Outcome state

At freeze:

- target outcomes NO;
- P&L outcomes NO;
- Jul-Aug unopened;
- Sep unopened.

## Exact next action

Implement Engine Q v0.2 and run zero-outcome EXP-038 preflight only.
