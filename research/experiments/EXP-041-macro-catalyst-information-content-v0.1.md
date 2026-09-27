# EXP-041 — Macro / Catalyst Information-Content Study v0.1

**Status:** PROSPECTIVELY FROZEN — DATA-ADEQUACY FIRST  
**Date:** 2026-09-25  
**Type:** INFORMATION-CONTENT RESEARCH, NOT A STRATEGY ENGINE  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed

## 1. Objective

Test whether scheduled U.S. macro catalysts add stable predictive information beyond the price-only baseline.

The experiment is intentionally split into two gates:

### Gate A — data adequacy

Do **not** fit an outcome model unless the macro history contains enough independent event blocks.

### Gate B — information content

Only if Gate A passes, compare:

1. `LOCAL_M5` baseline;
2. `PLUS_CATALYST_TIMING`;
3. `PLUS_SURPRISE_MAGNITUDE`.

This prevents thousands of candidate rows around a handful of releases from creating false confidence.

## 2. Candidate universe

If Gate B is eventually permitted, reuse the broad EXP-040 structural candidate universe and target-path labels.

Primary rungs remain:

- T40eq = 2R;
- T50eq = 2.5R.

No strategy entry filter is introduced.

## 3. Macro event families

Primary recurring families:

- EMPLOYMENT: Employment Situation / NFP package;
- CPI: CPI headline/core package;
- PPI: PPI headline/core package;
- RETAIL: retail sales/control-group/ex-auto package;
- GDP_PCE: GDP + PCE package when jointly released;
- FOMC: policy statement/projections.

A single timestamp containing several reported components is one independent **event block**.

## 4. Causal catalyst features

### Timing layer

For candidate time t:

- minutes to next event, clipped to 60m;
- minutes since last event, clipped to 180m;
- pre-event 0-60m;
- post 0-15m;
- post 15-60m;
- post 60-180m;
- event family;
- surprise-known flag.

### Surprise layer

Only after the release timestamp.

For each numeric component:

`scaled surprise = (actual - consensus) / frozen component scale`.

The first version uses fixed ex-ante unit scales reflecting the reporting granularity / typical market discussion, not outcome tuning:

- NFP: 50K;
- unemployment rate: 0.1 percentage point;
- average hourly earnings MoM/YoY: 0.1pp;
- CPI/PPI/PCE rates: 0.1pp;
- retail headline/control/ex-auto: 0.5pp;
- GDP annualized growth / GDP price index: 0.5pp.

Package features:

- mean absolute scaled surprise;
- maximum absolute scaled surprise;
- number of available components;
- conflict flag when package components have both positive and negative signed surprises.

The macro study does **not** hard-code “hawkish = buy USD” into the target label.

Direction/market interpretation is reserved for the later rates/USD-reaction layer.

## 5. Current-source event seed

The current March-June research window contains a curated primary-event seed covering:

- 3 Employment Situation releases;
- 3 CPI releases;
- 3 PPI releases;
- 3 Retail Sales releases;
- 3 GDP/PCE releases;
- 2 FOMC statements.

That is 17 independent event blocks.

This seed is enough to validate data plumbing, but **not enough for a serious recurring-family surprise model**.

## 6. Frozen data-adequacy gate

Before any macro outcome model is fitted require:

1. at least **12 months** of development market history ending no later than 2026-06-30;
2. at least **8 releases per recurring numeric family**: EMPLOYMENT, CPI, PPI, RETAIL, GDP_PCE;
3. at least **40 independent macro event blocks** total;
4. at least **30 surprise-bearing event blocks**;
5. at least **6 distinct FOMC policy events** or FOMC is timing-only/descriptive;
6. every chronological evaluation fold contains at least 4 independent event blocks;
7. at least two event families are represented in every evaluation fold;
8. consensus provenance is point-in-time / pre-release, not a post-hoc model forecast;
9. official release timestamps are independently verified;
10. Jul-Aug/Sep 2026 remain unloaded/unlabeled.

If this gate fails, disposition is:

`DATA_INSUFFICIENT_EXTEND_EARLIER_HISTORY`.

Do not compensate by loosening the gate or consuming protected future periods.

## 7. Future information-content gate

Only after data adequacy passes.

Evaluate only candidate rows in [-60m,+180m] around macro event blocks.

Primary comparison is event-block aware:

- pooled log loss and Brier;
- 6+ chronological event folds;
- per-event-block log loss delta;
- per-market stability;
- calibration.

An enriched set must improve both T40eq and T50eq with:

- >=1% relative pooled log-loss improvement;
- lower Brier;
- >=4/6 chronological fold wins;
- >=60% independent event-block wins;
- non-worse log loss in >=5/8 markets;
- ECE not worse by >0.01.

Select the smallest passing set.

## 8. Current decision

Do **not** run Gate B on the current 17-event / ~3-month source.

The next project action is to acquire and pin **earlier development market history plus matching macro calendar/consensus history**, while leaving July-September 2026 sealed.

This is not a delay; it is the anti-overfitting/data-sufficiency gate required to make the macro research meaningful.


## Gate-A final result and Gate-B implementation checkpoint — 2026-09-27

Final Gate-A durable result:

- commit: `4208af07c148a5d37c61cbbbeb004b83fec14af5`;
- disposition: `EXP041_GATE_A_PASS_AUTHORIZE_GATE_B_INFORMATION_CONTENT`;
- independent event timestamps: 65;
- surprise-bearing independent timestamps: 57;
- family counts: EMPLOYMENT 11, CPI 11, PPI 11, RETAIL 12, GDP_PCE 16, FOMC 8;
- all six frozen folds passed >=4 blocks and >=2 families;
- canonical Dukascopy v2, consensus provenance, official Actual/timestamp provenance and protected-period seal all passed.

Gate B is now prospectively implemented before market outcomes:

- spec commit: `5980e34433de38b17a64e31a260b5beeefa1a054`;
- runner commit: `015eb7b5cf50a86159614b43f331120991322fae`;
- workflow commit: `55ebbedde6bdcdc083d71d6f6a6676d68bbb4b0a`.

Gate B reuses the exact EXP-040 structural candidate/target mechanics on the immutable Dukascopy v2 snapshot and compares:

`LOCAL_M5 -> PLUS_CATALYST_TIMING -> PLUS_SURPRISE_MAGNITUDE`.

The six Gate-A event folds are fixed outer holdouts. Calibration is built from inner fold-wise out-of-fold probabilities; no event timestamp can leak into its own outer fit/calibration.

The original T40eq/T50eq information-advantage thresholds remain unchanged, with the additional already-frozen event-block win requirement from this EXP-041 spec.

No protected-period rows, Engine R outcomes, EXP-015 outcomes, position sizing or P&L are used.


## Final scientific disposition — 2026-09-27

Gate-B integrity corrigendum durable result:

- commit: `57a622a1bcd9abf812e3d8baf07f444be7824ff0`;
- corrected integrity: PASS;
- geometrically eligible Gate-A events: 63/65;
- only ineligible events: 2025-12-10 19:00 UTC FOMC and 2026-01-28 19:00 UTC FOMC;
- no model, metric, threshold, feature, fold, candidate grid or event window was changed;
- recovered scientific disposition: `NO_STABLE_MACRO_INFORMATION_ADVANTAGE`.

Decisive frozen Gate-B comparisons:

- +CATALYST_TIMING T40eq: relative log-loss improvement +0.219%, fold wins 3/6, event-block win rate 60.3%, markets non-worse 5/8 — FAIL;
- +CATALYST_TIMING T50eq: relative log-loss improvement +0.347%, fold wins 4/6, event-block win rate 63.5%, markets non-worse 4/8 — FAIL;
- +SURPRISE_MAGNITUDE T40eq: relative log-loss improvement +0.073%, Brier worsened, fold wins 3/6, event-block win rate 55.6%, markets non-worse 4/8 — FAIL;
- +SURPRISE_MAGNITUDE T50eq: relative log-loss improvement +0.178%, Brier worsened, fold wins 3/6, event-block win rate 57.1%, markets non-worse 4/8 — FAIL.

No enriched macro feature set passed both T40eq and T50eq.

**Decision:** close EXP-041. Do not tune macro thresholds or add macro variants on the same development sample. Move to the next orthogonal information family: rates/USD market interpretation, followed by execution-grade order flow.

Engine R and EXP-015 remain paused. Jul-Aug/Sep remain sealed.
