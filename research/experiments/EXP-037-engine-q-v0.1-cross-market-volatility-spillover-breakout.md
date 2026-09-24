# EXP-037 — Engine Q v0.1 Cross-Market Volatility Spillover Breakout

**Status:** PROSPECTIVE FREEZE — ZERO OUTCOMES  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-q-cross-market-volatility-spillover-breakout/SPEC-v0.1.md`  
**Provenance:** `research/provenance/EXP-037-engine-q-v0.1-source-manifest.md`

## Purpose

Test a genuinely different information source after Engine P's contemporaneous directional factor-confirmation family failed development.

Engine Q uses **directionless cross-market volatility breadth** as an exogenous arm signal, then waits for a lagging candidate's own first local breakout.

## Why this is not Engine P v0.2

Engine P used:

`own directional MOM + directional USD/cross confirmation -> pullback continuation`.

Engine Q uses:

`peer volatility shock breadth + candidate local lag/compression -> later candidate breakout -> pullback continuation`.

No Engine-P MOM/USD_SCORE threshold is retained or tuned.

## Frozen mechanics

Authoritative mechanics are in the strategy spec.

Center design:

1. completed M5 decisions 06:05-17:25 UTC;
2. candidate-excluded peer volatility ratios from prior-24-M5 median range;
3. >=4 shocked peers with VR>=1.75 and >=6 valid peers;
4. candidate VR<=1.00 and close inside a fixed prior-six-M5 box;
5. arm for next six completed M5 bars;
6. first breakout beyond fixed box with VR>=1.25, body>=50%, outer-25% close;
7. 50% breakout-bar retracement limit;
8. stop beyond breakout-bar opposite extreme;
9. 10-active-M1 / 30m order life;
10. unchanged T40 target and safe-lot overlay.

## Frozen provenance / split

Only source through 2026-06-30 may be loaded.

Warm-up/state source starts 2026-03-23.

Development folds:

- WF1 2026-04-13 to 2026-04-27
- WF2 2026-04-27 to 2026-05-11
- WF3 2026-05-11 to 2026-05-25
- WF4 2026-05-25 to 2026-06-08
- WF5 2026-06-08 to 2026-06-22
- WF6 2026-06-22 to 2026-07-01, with hard Jul-01 source seal

Protected:

- Jul-Aug secondary;
- Sep final holdout.

## Frozen costs / risk

Research costs:

- primary = 10% of gross target USD;
- stress = 20% of gross target USD.

Reference-account overlay:

- equity USD500;
- stop risk <=USD20;
- notional <=USD50k;
- margin <=USD100 at 1:500 research leverage;
- 0.01 lot step;
- XAUUSD <=0.10 lot.

Project daily limits remain approximately -USD40 normal stop-adding-risk and -USD60 emergency ceiling.

## Zero-outcome preflight

Preflight only. No labels/P&L.

Mandatory frequency/integrity:

- all causality/self-exclusion/arm/breakout/entry/safety tests pass;
- each market >=25 filled valid signals;
- both directions every market;
- >=300 total;
- source max <=Jun30;
- Jul-Aug and Sep unloaded;
- target/P&L outcomes zero.

If preflight fails frequency, stop before outcomes and do not lower the gate.

## Development gate if preflight passes

Use the frozen six slices and audited target-first outcome/portfolio conventions.

Mandatory:

- >=120 pooled signals;
- every fold >=8;
- gross normalized expectancy >+0.20R;
- primary/stress normalized expectancy >0;
- >=4/6 positive-stress folds;
- reference-account trades >=90;
- >=35 trade weekdays;
- reference primary/stress expectancy >0;
- primary PF >=1.10;
- stress PF >=1.05;
- stress MDD <=USD150;
- max market share <=60%;
- provenance/integrity pass;
- protected periods sealed.

## Anti-mining

Peer breadth, VR thresholds, lag rule, box, horizons, breakout confirmation, entry, stop, target, costs and gates are frozen before outcomes.

Any redesign requires a new version/experiment.

## Outcome state

At EXP-037 freeze:

- target outcomes: **NO**;
- P&L outcomes: **NO**;
- Jul-Aug: **unopened**;
- Sep: **unopened**.

## Exact next action

Implement Engine Q v0.1 mechanics and run a **zero-outcome preflight only**. Do not launch development until the durable preflight passes.


## Zero-outcome implementation checkpoint

Frozen before any Engine-Q target/P&L outcome:

- engine implementation commit: `9a2a2c797e7d526a42ab36399c82bec18c05540c`;
- preflight runner commit: `2bfb0c576167dd9b7f895e00d0b7ed68ccfe2453`;
- workflow commit: `c51c8f9566a6ccfddaf8117c2b0a80c45fbeb10b`;
- engine blob: `d1d95cc14a04ee700ae3709c1b7872941ebdac70`;
- runner blob: `239ca6ba52693cbaf6ce0ad0f928fcfb24a385c2`;
- workflow blob: `4235154e3a091a1caed67e943e0d6f14f6c0bab6`.

Implementation reuses only generic audited infrastructure for bar construction, safe-lot overlay, and limit-fill gap semantics. Engine-Q selection mechanics are new and follow the frozen spec.

At this checkpoint:

- target outcomes: **NO**;
- P&L outcomes: **NO**;
- Jul-Aug loaded/labeled: **NO**;
- Sep loaded/labeled: **NO**.

**Next:** trigger exactly one EXP-037 zero-outcome preflight run. Do not modify frozen inputs while it runs.


## Zero-outcome preflight result — FAIL / CLOSED BEFORE OUTCOMES

**Durable result commit:** `b05efb3038d6f3531a0def07ff6df09f0a25622b`  
**Result file:** `research/results/EXP-037-cross-market-volatility-spillover-preflight-v0.1.json`

Result:

- total filled signal paths: **56**;
- safely deployable: **56**;
- utility: GE40 **1** / GE30 **11** / LT30 **44**;
- per-market >=25 + both directions: **FAIL on all 8 markets**;
- total >=300: **FAIL**;
- safety overlay: PASS;
- target outcomes calculated: **NO**;
- P&L outcomes calculated: **NO**;
- parsed source max: **2026-06-30 23:59 UTC**;
- Jul-Aug secondary loaded/inspected: **NO**;
- Sep final holdout loaded/inspected: **NO**.

Per-market fills:

- XAUUSD 23;
- EURUSD 1;
- GBPUSD 0;
- USDJPY 6;
- EURJPY 11;
- AUDUSD 3;
- USDCAD 9;
- USDCHF 3.

Zero-outcome diagnosis:

- the dominant rejection was `peer_shock_failed` on every market;
- same-bar four-peer VR>=1.75 synchronization was too sparse for the eight-market scanner;
- candidate-lag and later breakout/fill mechanics were not the primary bottleneck.

**Disposition:** close Engine Q v0.1 / EXP-037 before any target/P&L outcome. Do not lower the unchanged >=25-per-market / both-directions / >=300-total gate.

A subsequent version may redesign the peer-shock sampling architecture because no outcome was inspected, but must be prospectively frozen before any new preflight/outcome.
