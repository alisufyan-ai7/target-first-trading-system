# EXP-022 — Engine K Multi-Market Direct Target-Move Scanner v0.1

**Status:** FROZEN PROSPECTIVELY — PRE-OUTCOME CLEANUP + FINAL ZERO-OUTCOME PREFLIGHT COMPLETE; TRAINING/CALIBRATION NEXT  
**Date:** 2026-09-23  
**Strategy:** strategies/engine-k-direct-target-move-scanner/SPEC-v0.1.md  
**Outcome status at freeze:** ZERO ENGINE-K OUTCOMES CALCULATED

## Motivation

The user explicitly corrected the project direction.

The system should not keep testing one handcrafted XAUUSD pattern after another as the primary discovery loop.

The actual operating problem is:

> Continuously scan all supported markets and identify where a USD30–50-equivalent favorable move has the highest probability before invalidation.

EXP-022 directly tests that problem.

## Key difference from G/H/I/J

Engines G–J each required a named setup motif before a candidate existed.

Engine K creates causal long/short market-state candidates every five minutes across the supported universe and lets a frozen probability model learn which market states precede target-first moves.

Engine K is therefore a new **direct forecasting/statistical engine family**, not a tuned variant of G–J.

## Initial universe

Execution-research eligible:

- XAUUSD;
- EURUSD;
- GBPUSD;
- USDJPY;
- EURJPY;
- AUDUSD;
- USDCAD;
- USDCHF.

Forecast-only until economics are frozen:

- XAGUSD;
- NAS100;
- US30;
- SPX500.

These four forecast-only markets may be preflighted and researched, but they may not fit/calibrate the primary executable model or enter trade/P&L ranking.

Wave 2 target additions:

- GBPJPY;
- BTCUSD/BTCUSDT;
- additional liquid markets only after pinned data and contract economics are documented.

## Frozen split

The currently pinned rolling public samples share coverage beginning 2026-03-23. The exact frozen source manifest is in `research/provenance/EXP-022-wave1-data-manifest.md`.

Additional-market admission is governed prospectively by `research/provenance/EXP-022-symbol-admission-policy.md`.

Frozen split:

- training: 2026-03-23 through 2026-05-31;
- calibration: 2026-06-01 through 2026-06-30;
- historical secondary test: 2026-07-01 through 2026-08-31;
- final common-sample holdout: 2026-09-01 through 2026-09-22.

2026-09-23 is excluded as a potentially incomplete current UTC day.

The secondary period is not pristine because prior project work inspected related 2026 periods. The September final holdout must remain untouched until implementation, features, model, and qualification logic are frozen and preflight passes.

## Target logic

### Gold

- +3 / +4 / +5 XAU before structural stop.

### Non-Gold

Use the prospectively frozen dynamic native target ladder from the Engine-K spec:

- 0.14 / 0.19 / 0.23 x median true range of prior 20 completed active 1h bars.

Then size each target rung economically to approximately USD30 / USD40 / USD50 gross.

The MTR20 fractions are a frozen **forecast-label grid**, not a global replacement for the engine-conditioned sizing doctrine. Execution eligibility additionally requires:

- structural stop risk <=USD20;
- notional/equity <=100x;
- research margin <=USD100 at the frozen 1:500 research reference;
- primary research round-trip cost = 10% of gross target;
- stress research round-trip cost = 20% of gross target.

## Structural invalidation

Latest confirmed causal 5m 2-left/2-right pivot within 60 active minutes.

Long stop below latest eligible swing low; short stop above latest eligible swing high.

## Primary model

Frozen pooled HistGradientBoostingClassifier with fixed hyperparameters from the spec.

Qualification:

- `p_BE = (stop_risk + primary_cost) / (target + stop_risk)`;
- calibrated target-first probability >= `max(0.60, p_BE + 0.05)`;
- primary-cost net EV > 0;
- structural stop risk <= USD20;
- notional/equity <=100x;
- research margin <=USD100 at 1:500;
- all other economic/session/data gates pass.

## Required outputs

Per market and combined:

- state count;
- economically admissible state count;
- probability distribution;
- calibration/Brier/log-loss/AUC;
- qualified-trade count;
- target-first hit rate;
- gross/net expectancy;
- market contribution;
- trades/day;
- zero-qualified-opportunity days;
- <=USD50 / >=USD100 / >=USD150 daily percentages under one-open simulation;
- max drawdown;
- longest losing/low-output streak.

## Checkpoint sequence

1. data/provenance inventory for all Wave-1 markets;
2. pre-outcome cleanup of universe, economics, causal bars and feature formulas;
3. exact target/economic conversion verification;
4. 29-feature / pivot / entry-gap self-tests with zero target/model outcomes;
5. durable zero-outcome cleanup preflight checkpoint;
6. fit primary execution model on **training Mar-23 through May-31 only**;
7. calibrate probabilities on **June only**;
8. checkpoint training/calibration outputs and freeze qualification outputs;
9. run historical secondary test on **July through August**;
10. checkpoint;
11. run final common-sample holdout **Sep-1 through Sep-22 once**;
12. checkpoint before any revision.

The September holdout is an initial out-of-sample test, not sufficient by itself for live promotion.

## Prohibited

- lowering the 0.60 floor or the +0.05 break-even buffer after seeing low trade frequency;
- choosing a different target burden after seeing results;
- market-specific feature hand-tuning after outcome inspection;
- using final holdout to select model hyperparameters;
- dropping bad markets from reported combined results without documenting the exclusion rule;
- replacing structural stops after outcome inspection.

## Pre-outcome cleanup checkpoint

Completed before target labels/model outcomes:

- exact execution universe: 8 markets;
- exact forecast-only universe: 4 markets;
- forecast-only isolation from primary executable model;
- authoritative train/calibration/secondary/final split reconciled;
- complete-bar-only 5m/1h construction;
- <=5-minute next-entry gap rule;
- complete 29-feature causal contract;
- target-relative research cost stress;
- USD20 stop-risk gate;
- 100x notional/equity cap;
- USD100 research-margin cap at 1:500;
- qualification probability = max(0.60, break-even + 0.05);
- September final holdout explicitly not sufficient alone for live promotion;
- final raw-file integrity may cover the full pinned file, but state/feature preflight is restricted to training+calibration through June 30.

Implementation commits:

- Engine-K economics/causality hardening: `ae8bf29f0d6c083120f851616b4220dc80448d43`;
- complete 29-feature contract: `4269d95a3483f97630ecbc5c87aee6025d713e39`;
- strengthened cleanup preflight runner: `4b0df1ebfd10b243bd8fe769f6196fd9c8f12a88`;
- durable preflight workflow: `16be981d83594829a52399c10de28052c2bb1b4b`.

**Engine-K target outcomes calculated: NO.**  
**Engine-K model outcomes calculated: NO.**

## Immediate next action

Run the final zero-outcome cleanup preflight against all 12 pinned datasets. Full files may be checked for raw integrity, but structural-state/feature diagnostics must stop at June 30.

Only after that passes may the primary model be fit on the eight execution-research markets using the frozen training period.


## Checkpoint 2 — final zero-outcome cleanup preflight passed

**Authoritative tested repository SHA:** `2c319cd45cbae6cdb1934540f6933890886c1812`  
**Durable preflight result commit:** `48aa0af80b7fc2fff1dab56d3fb617b1c2140f3f`  
**Result:** `research/results/EXP-022-preflight-cleanup-v0.1.json`

Final preflight status:

- Engine-K target outcomes calculated: **NO**;
- Engine-K model outcomes calculated: **NO**;
- training run: **NO**;
- calibration run: **NO**;
- secondary test run: **NO**;
- final holdout outcomes loaded: **NO**;
- July-August / September state-feature distributions inspected by final preflight: **NO**.

Verified universe:

- execution-research markets: **8**;
- forecast-only markets: **4**.

Zero-outcome preflight self-tests passed: **11 / 11**.

Training+calibration-scope state diagnostics through June 30 only:

- execution structural states: **205,196**;
- economically admissible execution target rungs before probability qualification: **7,098**;
- forecast-only structural states: **103,041**.

The cleanup therefore does not create an artificially empty scanner. It leaves thousands of economically admissible rungs before any fitted probability or outcome-based selection.

### Next permitted stage

Implement/freeze the outcome-label + primary-model training/calibration runner if not already present, then:

1. calculate target labels only as needed for **training Mar-23 through May-31** and **calibration June**;
2. fit the primary model only on the eight execution-research markets;
3. calibrate probabilities only on June;
4. checkpoint all training/calibration outputs and qualification behavior;
5. keep July-August secondary test unopened until that checkpoint;
6. keep Sep-1 through Sep-22 final holdout unopened until the later secondary-test checkpoint.

No model/threshold/feature/universe changes may be made using later-period outcomes.


### Final pre-outcome label mechanics clarification

Before any Engine-K target outcome was calculated, the label horizon was made explicit:

- entry M1 bar counts as active bar 1;
- maximum 120 active M1 bars;
- 20:00 UTC same-entry-date session cutoff;
- only bars starting before 20:00 are eligible;
- stop wins target/stop same-bar ambiguity, including on the entry bar;
- if neither stop nor target is reached, mark to the close of the last eligible processed M1 bar;
- no overnight carry.

The diagnostic L2 logistic baseline is also frozen to StandardScaler + LogisticRegression(C=1.0, solver=lbfgs, max_iter=1000). It remains diagnostic and may not replace the primary HistGradientBoosting model based on observed performance.

These are implementation clarifications, not outcome-driven revisions. Engine-K target/model outcomes remained zero when frozen.
