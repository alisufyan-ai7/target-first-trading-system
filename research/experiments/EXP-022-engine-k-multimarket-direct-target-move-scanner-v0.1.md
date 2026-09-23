# EXP-022 — Engine K Multi-Market Direct Target-Move Scanner v0.1

**Status:** FROZEN PROSPECTIVELY — CHECKPOINT 1 DATA PROVENANCE COMPLETE; PRE-OUTCOME IMPLEMENTATION NEXT  
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

- XAGUSD.

Wave 2 target additions:

- GBPJPY;
- NAS100/USTEC;
- US30;
- US500/SPX500;
- BTCUSD/BTCUSDT.

## Frozen split

The currently pinned rolling public samples share coverage beginning 2026-03-23. The exact frozen source manifest is in `research/provenance/EXP-022-wave1-data-manifest.md`.

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

Then size each target rung economically to approximately USD30 / USD40 / USD50 gross, subject to the primary USD20 structural-risk gate.

## Structural invalidation

Latest confirmed causal 5m 2-left/2-right pivot within 60 active minutes.

Long stop below latest eligible swing low; short stop above latest eligible swing high.

## Primary model

Frozen pooled HistGradientBoostingClassifier with fixed hyperparameters from the spec.

Qualification:

- calibrated target-first probability >= 0.60;
- conservative net EV > 0;
- structural stop risk <= USD20;
- economic/margin gates pass.

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
2. exact target/economic conversion verification;
3. feature/label implementation self-tests with zero model outcomes;
4. checkpoint preflight;
5. training + May calibration only;
6. checkpoint;
7. freeze calibration/qualification outputs;
8. secondary Jun–Aug test;
9. checkpoint;
10. final Aug21–Sep11 holdout once;
11. checkpoint before any revision.

## Prohibited

- changing p>=0.60 after seeing low trade frequency;
- choosing a different target burden after seeing results;
- market-specific feature hand-tuning after outcome inspection;
- using final holdout to select model hyperparameters;
- dropping bad markets from reported combined results without documenting the exclusion rule;
- replacing structural stops after outcome inspection.

## Immediate next action

Checkpoint 1 is complete.

Next:

- implement Engine-K feature/candidate/preflight code against the pinned Wave-1 manifest;
- verify causal feature construction and structural pivots with zero target/model outcomes;
- checkpoint preflight;
- then run training + calibration only.
