# EXP-014 — Original Engine A Recovery + P&L-Equivalent Sizing

**Status:** READY TO EXECUTE — REQUIRED GATE BEFORE RANKER RESUMES  
**Date:** 2026-09-22

## Why this experiment exists

Two corrections govern the next phase:

1. XAUUSD 0.10 lot is the economic anchor, while other markets require symbol-specific equivalent lot sizes.
2. Original Badar-inspired Gold Engine A from EXP-002 must not be conflated with Engine A v0.2-portable.

EXP-014 is therefore a recovery/reproduction and sizing-normalization gate.

## Part A — recover original Engine A

Authorized evidence:

- EXP-001;
- EXP-002;
- strategies/engine-a-liquidity-mss-fvg/SPEC.md;
- docs/BADAR-VIDEO-EVIDENCE.md;
- docs/TIMEFRAME-AND-MARKET-CONTEXT.md;
- originating/current chat context;
- no unrelated repository/chat/project context.

Recorded sequence:

liquidity -> sweep -> internal MSS -> displacement -> FVG -> retracement -> tight structural/FVG stop -> target expansion.

Starting recovery parameters:

- recent 5m swing liquidity;
- 5m wick sweep and close back inside;
- 1m internal MSS close;
- displacement >= approximately 1.6x recent 1m average body;
- FVG after shift;
- entry near 50% FVG;
- active window about 06:00–18:00 UTC;
- XAU USD 5 target-first label.

## Reproduction benchmark

Overall target:

- ~372 trades/signals;
- USD 5 hit ~29.6%;
- average structural risk ~USD 1.02 Gold;
- median favorable excursion ~USD 3.30;
- simplified expectancy ~+USD 0.79 Gold/trade before costs.

Development March–May:

- ~185 trades;
- USD 5 ~31.9%;
- expectancy ~+USD 0.85.

Holdout June–Aug 20:

- ~187 trades;
- USD 2 48.7%;
- USD 3 41.7%;
- USD 4 31.6%;
- USD 5 27.3%;
- expectancy ~+USD 0.72.

## Frozen reproduction-acceptance protocol

**Frozen before any new EXP-014 reconstruction outcome is calculated.**

A reconstruction is compared to the complete EXP-002 benchmark vector. No single attractive metric can compensate for broad failure elsewhere.

### Hard benchmark bands

- overall trade count: **335–409** (approximately ±10% around 372);
- development trade count: **163–207** (approximately ±12% around 185);
- holdout trade count: **165–209** (approximately ±12% around 187);
- overall USD 5 target-first rate: **26.6%–32.6%** (29.6% ±3 percentage points);
- holdout USD 5 target-first rate: **24.3%–30.3%** (27.3% ±3 percentage points);
- holdout USD 2 target-first rate: **44.7%–52.7%** (48.7% ±4 percentage points);
- holdout USD 3 target-first rate: **37.7%–45.7%** (41.7% ±4 percentage points);
- holdout USD 4 target-first rate: **27.6%–35.6%** (31.6% ±4 percentage points);
- average structural risk distance: **USD 0.867–1.173 Gold** (USD 1.02 ±15%);
- median favorable excursion: **USD 2.805–3.795 Gold** (USD 3.30 ±15%).

### Simplified-expectancy bands

Because simplified expectancy is particularly sensitive to small differences in timeout and stop mechanics, use a wider but still numerical tolerance while requiring the sign to remain positive in every split:

- overall: **+USD 0.514 to +USD 1.067 Gold/trade** (0.79 ±35%);
- development: **+USD 0.553 to +USD 1.148 Gold/trade** (0.85 ±35%);
- holdout: **+USD 0.468 to +USD 0.972 Gold/trade** (0.72 ±35%).

### Acceptance classification

- **PASS / recovered reproduction:** all hard benchmark bands and all three expectancy bands pass simultaneously.
- **NEAR MATCH / not yet recovered:** most dimensions are close, but at least one frozen band fails. This is diagnostic only and may motivate one ambiguity-specific next variant; it is not allowed to be called the recovered original.
- **FAIL:** material multi-dimensional mismatch, wrong expectancy sign in either split, or a miss larger than twice the stated tolerance on any core dimension.

A future variant may change only a mechanically identifiable ambiguity that was frozen in the prior variant. It may not change several unrelated parameters simultaneously to chase the benchmark.

## A1 freeze checkpoint

The first mechanical recovery attempt is frozen at:

- `strategies/engine-a-liquidity-mss-fvg/SPEC-v0.1-recovery-A1.md`;
- acceptance-protocol commit: `24505683baeb326b53b0ff1dc76a71593a0a72c5`;
- A1-spec commit: `72dc26d813c4fd1ef9455f97547908346b501930`.

No A1 outcome was calculated before these freezes.

## Reproduction procedure

1. define all missing mechanical details before comparing a variant to the benchmark;
2. run the complete original date window;
3. compare trade count, hit rates, stop distribution, MFE, and expectancy;
4. checkpoint each materially different reconstruction;
5. do not tune directly to one metric while degrading the others;
6. if no honest reconstruction matches reasonably, record that the original code is unrecoverable rather than inventing certainty.

## Part B — correct equivalent-lot rule

### Gold

- reference size 0.10 lot;
- normal target about USD 5 Gold move ~= USD 50 gross;
- USD 3–4 ~= USD 30–40 fallback;
- stronger validated continuation may support USD 70–100+.

### Non-Gold

First freeze a native target distance D for the engine/market.

Then propose:

equivalent lot = 50 / (D x USD P&L per native unit at 1 lot).

The proposed size must pass:

- structural-stop dollar loss;
- required margin;
- notional/equity;
- remaining daily loss budget;
- correlated open exposure.

If full USD-50-equivalent size is unsafe but a smaller size still provides a validated USD 30–40 opportunity, allow the smaller objective. Otherwise reject.

No stop compression, martingale, or post-loss size increase.

## Target-distance methods to compare on development data only

1. volatility-burden equivalence;
2. engine-conditioned favorable-excursion distribution.

Select/freeze the method before new holdout use.

EXP-006 remains a sizing diagnostic; its large FX lot estimates are evidence of feasibility pressure, not a reason to switch to same-lot sizing.

## Architecture gate

Only after Part A reproduction and Part B sizing freeze:

1. route recovered Engine A candidates into the common strategy-engine contract;
2. evaluate transfer to selected markets under equivalent sizing;
3. add other independently validated engines;
4. resume target-first ranker work.

## Relationship to EXP-015

EXP-015 is the renumbered target-first ranker experiment.

It is **PAUSED** until EXP-014 passes.

Its earlier broad-pivot XAU candidate statistics are retained as diagnostics only and do not supersede the engine-first architecture.
