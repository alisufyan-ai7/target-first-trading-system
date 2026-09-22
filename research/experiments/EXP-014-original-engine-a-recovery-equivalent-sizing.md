# EXP-014 — Original Engine A Recovery + P&L-Equivalent Sizing Plan

**Status:** PLANNED — NO NEW OUTCOME TESTING UNTIL PLAN REVIEW  
**Date:** 2026-09-22

## Why this experiment exists

The user clarified two important points before further development:

1. XAUUSD 0.10 lot is the economic anchor, but other markets require **symbol-specific equivalent lot sizes** rather than identical 0.10-lot sizing.
2. The original Badar-inspired Gold Engine A from EXP-002 showed positive simplified expectancy and must not be conflated with the later Engine A v0.2-portable rewrite.

This experiment is therefore a recovery/normalization checkpoint, not a new strategy invention.

## Part A — Recover the original Engine A Gold implementation

Use only project-authorized evidence:

- EXP-001 video reverse-engineering record;
- EXP-002 original XAUUSD screen;
- strategies/engine-a-liquidity-mss-fvg/SPEC.md;
- any explicit mechanics durably recorded from the prior project chat;
- no unrelated repositories/chats.

Recorded original sequence:

liquidity -> sweep -> internal MSS -> displacement -> FVG -> retracement entry -> structural/FVG stop -> target expansion.

Recorded practical screen parameters:

- recent 5m swing liquidity;
- 5m sweep wick beyond level and close back inside;
- 1m internal MSS close beyond recent pivot;
- displacement about >=1.6x recent 1m average body;
- FVG after shift;
- entry near 50% FVG;
- tight FVG/structural stop;
- active window about 06:00–18:00 UTC;
- XAUUSD USD 5 target-first label.

## Reproduction gate

Do not transfer or optimize the recovered implementation until it approximately reproduces EXP-002 on the original baseline.

Reference metrics:

### Overall

- ~372 trades/signals;
- USD 5 target-first: ~29.6%;
- average structural risk: ~USD 1.02 Gold;
- median favorable excursion: ~USD 3.30;
- simplified expectancy: ~+USD 0.79 Gold/trade before costs.

### Development — March–May 2026

- ~185 trades;
- USD 5 hit: ~31.9%;
- simplified expectancy: ~+USD 0.85 Gold/trade.

### Holdout — June–August 20, 2026

- ~187 trades;
- USD 5 hit: ~27.3%;
- simplified expectancy: ~+USD 0.72 Gold/trade;
- USD 2 target-first: 48.7%;
- USD 3: 41.7%;
- USD 4: 31.6%;
- USD 5: 27.3%.

If a recovered implementation materially misses these benchmarks, document the discrepancy rather than pretending it is the same engine.

## Part B — Define the correct equivalent-lot rule

### Gold anchor

- XAUUSD size: 0.10 lot;
- normal target: USD 5 Gold move ≈ USD 50 gross under the 10-oz convention;
- USD 3–4 moves correspond to approximately USD 30–40 fallback capture;
- stronger moves may support USD 70–100+.

### Non-Gold symbols

The symbol's lot size is **not** copied from Gold.

First freeze a native target distance D for the symbol/setup.

Then calculate:

equivalent_lot = 50 / (D × USD P&L per native price unit at 1 lot)

Examples for USD-quote FX under the common USD 10/pip per 1 standard lot convention:

- D = 5 pips -> 1.00 lot for ~USD 50;
- D = 10 pips -> 0.50 lot;
- D = 20 pips -> 0.25 lot;
- D = 50 pips -> 0.10 lot.

JPY-quote and non-FX symbols require contemporaneous quote conversion and actual contract specifications.

## How native target distance will be frozen

Do not choose target distance after seeing holdout P&L.

Two candidate methods may be compared on development data only:

1. **volatility-burden equivalence** — reuse the EXP-006 concept that maps Gold's USD 5 target to a comparable fraction of intraday volatility;
2. **engine-conditioned target distance** — use the development distribution of favorable excursion before invalidation for that engine/market.

The method must be selected and frozen before holdout testing.

EXP-006 is relevant evidence: its volatility-burden method implied approximately 1.608 lots EURUSD, 1.163 lots GBPUSD, and 2.146 lots USDJPY for a ~USD 50 gross target. Those values were previously rejected for leverage pressure; under the corrected plan they become sizing diagnostics that must be tested against feasibility gates.

## Feasibility gate

The USD-50-equivalent lot is only a proposed size.

Before accepting a trade calculate:

- structural-stop dollar loss;
- required margin;
- notional/equity;
- remaining daily loss budget;
- simultaneous correlated exposure.

Decision:

- if USD-50-equivalent size is feasible -> normal target around USD 50;
- if not, but a smaller safe size still offers a validated USD 30–40 opportunity -> allow the smaller trade;
- otherwise reject.

No stop compression, martingale, or post-loss size increase.

## Part C — Scanner design after recovery

Only after Parts A/B pass:

1. run original/recovered Engine A on Gold;
2. test transfer to selected markets under equivalent sizing;
3. preserve other independent engines as separate candidate generators;
4. for each live candidate estimate probability of reaching USD 30 / 40 / 50 / 70 / 100 before invalidation;
5. rank candidates across markets by calibrated target-first probability, expected net USD value, and feasibility;
6. take only opportunities above a frozen quality threshold;
7. use daily risk/profit state controls.

## No work to do before review

This file intentionally stops at the plan.

No new strategy tuning, holdout inspection, or scanner-universe selection should proceed until this corrected plan has been reviewed with the user.
