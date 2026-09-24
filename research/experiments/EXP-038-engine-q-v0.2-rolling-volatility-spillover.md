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


## Zero-outcome implementation checkpoint

Frozen before any Engine-Q v0.2 outcome:

- engine implementation commit: `3738577057ad15e057bcd54e4cb3b847af245af5`;
- preflight runner commit: `0219ad3084bfdb8b9d0155b668825134f715cbeb`;
- workflow commit: `850fe44fa426b2ee4f235d3af140fa981ff26ae2`;
- engine blob: `ea4642a7e6e92c6b7cd1a85390b3e29cbc47ba40`;
- runner blob: `e709a84e78f3bd0adaf9620a03dee9b431e5683d`;
- workflow blob: `83792f3e41db89ecd663522abbbb54c417c92f9f`.

At this checkpoint:

- target outcomes: NO;
- P&L outcomes: NO;
- Jul-Aug loaded/labeled: NO;
- Sep loaded/labeled: NO.

**Next:** trigger exactly one EXP-038 zero-outcome preflight run and do not mutate frozen inputs while it runs.


## Zero-outcome preflight — PASS

**Durable result commit:** `3d9ca37fc733542f1ed2554e26a2989b1b578f2d`  
**Result file:** `research/results/EXP-038-rolling-volatility-spillover-preflight-v0.2.json`  
**Result blob:** `83061d6ff47f2ddccc36cdb2f75be30df6d1ce37`

Frozen-gate result:

- filled valid signals: **467**;
- safely deployable: **466**;
- every market >=25 and both directions: **PASS**;
- total >=300: **PASS**;
- safe overlay caps: **PASS**;
- utility: GE40 **6** / GE30 **134** / LT30 **326** / NONDEPLOYABLE **1**;
- parsed source max: **2026-06-30 23:59 UTC**;
- target outcomes calculated: **NO**;
- P&L outcomes calculated: **NO**;
- Jul-Aug secondary loaded/inspected: **NO**;
- Sep final holdout loaded/inspected: **NO**.

Per-market filled signals:

- XAUUSD 69;
- EURUSD 53;
- GBPUSD 50;
- USDJPY 55;
- EURJPY 50;
- AUDUSD 64;
- USDCAD 72;
- USDCHF 54.

**Disposition:** PASS. Engine Q v0.2 may proceed to the already-frozen six-slice development stage while protected periods remain sealed.


## Development implementation checkpoint — zero outcomes

Frozen before any EXP-038 development outcome:

- development runner commit: `9f131006140ccb88709a72682760a5c6db66255b`;
- development workflow commit: `be6c986d6ec887b202372a912444cbf7b73b9669`;
- runner blob: `ae610dc3e138a4aabe3bcb3009ac2cd426f22c7b`;
- workflow blob: `34d6158b2aa8b5767ea9b6a8b3ef420cc5b9b545`.

Development convention is now explicit:

- fold membership uses **breakout completion time**, not earlier spillover-arm time;
- matched immediate control enters at first active M1 open after the same qualified breakout completion;
- T40 vs breakout-bar structural stop;
- same-bar stop first;
- max 120 active M1 bars;
- 20:00 UTC cutoff;
- peer-shock count/age, candidate lag VR, breakout VR, hour, market and direction diagnostics are descriptive only;
- >+0.20R gross hurdle and all post-cost/stability/reference-account gates unchanged.

At this checkpoint:

- EXP-038 target outcomes: **NO**;
- EXP-038 P&L outcomes: **NO**;
- Jul-Aug loaded/labeled: **NO**;
- Sep loaded/labeled: **NO**.

**Next:** trigger exactly one EXP-038 development run. Any failed mandatory gate stops before secondary testing.


## Development result — FAIL / STOP BEFORE SECONDARY

**Durable result commit:** `6f25b089d6d7eea01d37d293c48bd51bf1e84d9e`  
**Tested repository SHA:** `e5f18258d8bc559e09f14f89b0276feb048c084f`  
**Result file:** `research/results/EXP-038-development-summary-v0.2.json`

Frozen development result:

- pooled development signals: **363**;
- target hits: **142** / hit rate **39.1185%**;
- gross normalized expectancy: **+0.0947930R**;
- primary normalized expectancy: **-0.0902225R**;
- stress normalized expectancy: **-0.2752379R**;
- positive-stress folds: **1/6**;
- reference-account trades: **251** across **57** trade weekdays;
- reference primary expectancy: **-USD1.5256/trade**;
- reference stress expectancy: **-USD3.8859/trade**;
- reference primary PF: **0.8362**;
- reference stress PF: **0.6403**;
- stress max drawdown: **USD1,102.23**;
- development gate: **FAIL**;
- disposition: **FAIL_STOP_BEFORE_SECONDARY**.

Matched immediate-entry control:

- 651 signals;
- gross expectancy **-0.0190R**;
- primary expectancy **-0.1956R**;
- stress expectancy **-0.3721R**.

Interpretation:

- the 50% non-chasing entry materially improved Engine-Q economics versus immediate entry;
- nevertheless the actual Engine-Q signal layer achieved only +0.0948R gross, below the frozen >+0.20R hurdle, and remained negative after costs;
- only one of six folds was stress-positive;
- no peer-shock-age, lag-VR, breakout-VR, hour, market or direction rescue is permitted inside v0.2.

Protection verified by the durable result:

- parsed source max **2026-06-30 23:59 UTC**;
- Jul-Aug secondary loaded/labeled: **NO**;
- Sep final holdout loaded/labeled: **NO**.

**Final disposition:** Engine Q v0.2 / EXP-038 is closed before secondary testing. Do not inspect protected periods. Retain non-chasing execution as an architectural lesson, but move to a genuinely different information source/family rather than another Engine-Q temporal/threshold variant.
