# EXP-023 — Engine K v0.2 Risk-Normalized Multi-Market Target Scanner

**Status:** ZERO-OUTCOME PREFLIGHT PASSED — TRAINING + JUNE CALIBRATION NEXT  
**Date:** 2026-09-24  
**Strategy:** strategies/engine-k-direct-target-move-scanner/SPEC-v0.2.md

## Motivation

EXP-022 / Engine K v0.1 proved that the direct target-first scanner pipeline works mechanically but failed before secondary testing.

Observed v0.1 training+June calibration facts:

- 7,098 economically admissible labeled rungs;
- all 7,098 were XAUUSD;
- all seven FX execution markets produced zero economically admissible rungs under the frozen 0.14/0.19/0.23 x MTR20 + equivalent-size construction;
- June raw HGB ROC-AUC was approximately 0.62–0.63 by rung, but Platt-calibrated probabilities remained below the frozen 60% qualification floor;
- zero actual qualified trades;
- July-August secondary-test outcomes were not loaded/labeled;
- Sep-1–Sep-22 final holdout was not loaded/labeled.

EXP-023 is a prospective redesign using only those inspected training/calibration facts.

## What stays unchanged

- dense 5m long/short scanning;
- same 8 execution markets;
- same 4 forecast-only markets;
- same pinned data;
- same training/calibration/secondary/final split;
- same structural pivot stop;
- same entry rule;
- same 29 causal features;
- same HGB model/hyperparameters;
- same June Platt calibration;
- same conservative label horizon;
- same USD500 reference equity;
- same USD20 stop-risk cap;
- same notional/margin gates;
- same primary/stress cost fractions;
- same one-open portfolio state machine.

## What changes prospectively

### Non-Gold target function

Replace the infeasible generic MTR20 target-distance ladder with candidate-specific structural reward/risk targets:

- T30 = 1.5R;
- T40 = 2.0R;
- T50 = 2.5R;

where `R = abs(entry - unchanged structural stop)`.

Target is defined before size.

### Equivalent sizing

After target distance is frozen, compute the downward-rounded lot required for USD30/USD40/USD50 nominal gross target, then rerun risk/notional/margin gates.

### Probability qualification

Replace the universal v0.1 60% floor with:

`p_required = max(0.50, p_break_even + 0.10)`.

This is frozen before any v0.2 target/model outcome.

## Protected evidence

Still unopened for v0.2 design:

- July-August 2026 secondary test;
- Sep-1–Sep-22 2026 final holdout.

No v0.2 result may be calculated from those periods before the required earlier checkpoints pass.

## Required sequence

1. freeze v0.2 spec + EXP-023 — DONE;
2. implement separate v0.2 economics/reference module;
3. zero-outcome tests and preflight through June only;
4. require economically admissible coverage on every execution market;
5. durable checkpoint;
6. only then run Mar23-May31 training + June calibration;
7. apply frozen pre-secondary gate;
8. stop on failure;
9. only on pass may July-August be opened;
10. Sep final holdout remains last.

## Pre-secondary gate

Mandatory:

- >=200 unique economically admissible labeled states per market;
- >=100 qualified one-open trades combined train+cal;
- >=20 qualified one-open June trades;
- June hit rate > June mean break-even;
- June primary expectancy >0;
- June PF >=1.10;
- June max DD <=USD100;
- integrity/provenance pass.

Concentration is reported and cannot be hidden by dropping markets.

## Outcome status

At EXP-023 freeze:

- v0.2 target outcomes calculated: **NO**;
- v0.2 model outcomes calculated: **NO**;
- July-August outcomes inspected: **NO**;
- September outcomes inspected: **NO**.


## Preflight attempt 1 — operational self-test defect

GitHub Actions run `35956306829` failed before data preflight.

Failure location:

- step: `Syntax and v0.2 zero-outcome tests`;
- assertion: exact EURUSD T30 1.5R tick boundary;
- no data-state preflight executed;
- no v0.2 target labels calculated;
- no v0.2 model outcomes calculated;
- no July-August or September evidence inspected.

Cause:

binary floating-point representation made an exact 0.001 structural distance slightly larger than 0.001, so upward tick rounding incorrectly converted the intended exact 0.00150 target to 0.00151.

Correction:

- replaced floating tick-boundary arithmetic with Decimal-based exact structural-distance / tick rounding;
- added an exact-boundary unit test;
- correction commit: `d4983a061b86230d2f92b7fae80608a48c000a48`.

This is an implementation-preflight defect, **not** an Engine-K v0.2 economic or predictive result.


## Preflight attempt 2 — PASS

**Workflow run:** `35956921023`  
**Durable result commit:** `02a2ab0b1ea7f21092b06165a0ca8f0638d4c41b`  
**Result file:** `research/results/EXP-023-preflight-v0.2.json`

Outcome status at this checkpoint:

- v0.2 target outcomes calculated: **NO**;
- v0.2 model outcomes calculated: **NO**;
- July-August secondary test loaded/inspected: **NO**;
- September final holdout loaded/inspected: **NO**.

All seven v0.2 zero-outcome self-tests passed.

Economic coverage through June:

- XAUUSD: 2,366 unique admissible states;
- EURUSD: 13,098;
- GBPUSD: 14,466;
- USDJPY: 10,503;
- EURJPY: 10,869;
- AUDUSD: 18,336;
- USDCAD: 9,397;
- USDCHF: 15,203.

Totals:

- structural states: 205,196;
- unique economically admissible states: 94,238;
- economically admissible rungs: 281,955.

Every execution market exceeded the frozen >=200-state preflight threshold.

**Disposition:** PASS. The v0.2 economic redesign fixed the v0.1 cross-market admission failure without using target/model outcomes.

### Next permitted stage

Run only:

- training: Mar-23 through May-31;
- calibration: June.

Use the frozen HGB/Platt model, feature contract, v0.2 target/economic rules and pre-secondary gate.

Do not inspect July-August or September unless the training/June gate passes and is durably checkpointed.
