# EXP-015 — Target-First Opportunity Ranker v0.1

**Status:** PAUSED — DESIGN MUST BE REBASED AFTER EXP-014  
**Date:** 2026-09-22

## Why this file exists

This experiment was originally created under the duplicate ID EXP-014.

It has been renumbered to preserve unique experiment IDs and to restore the correct project sequence:

1. EXP-014 — recover/reproduce original Engine A and freeze equivalent sizing;
2. EXP-015 — target-first ranker, only after EXP-014 passes.

## Design correction

The original EXP-015 draft generated a very broad candidate universe from recent one-minute pivots every five minutes and allowed the statistical model to decide which raw structural candidates were attractive.

That is **not the current default system architecture**.

Current architecture:

~~~text
validated strategy engine
        ->
meaningful candidate
        ->
target-first probability / EV model
        ->
cross-market ranker
~~~

A broad generic structural/statistical candidate generator may be tested later, but it must be explicitly versioned and validated as its own engine before bypassing validated setup engines.

## Sizing correction

The original ranker draft also assumed:

- XAUUSD at 0.10 lot;
- FX at 0.10 standard lot.

The FX assumption is superseded.

Current rule:

- XAUUSD 0.10 lot is the anchor;
- non-Gold markets require symbol-specific P&L-equivalent sizing from a frozen native target distance;
- proposed size must pass structural risk, margin, notional/leverage, daily-budget, and correlation gates.

## Preserved Stage-1 XAU diagnostic

Before the design correction, the broad-pivot XAU candidate enumeration was run on development + May calibration only.

This result is retained as a **diagnostic dataset finding**, not as validation of the final scanner architecture.

Data:

- public external XAUUSD one-minute sample;
- 2026-03-12 through 2026-05-31 only;
- 76,855 one-minute rows;
- 15,378 resampled 5m bars.

Corrected cooldown/risk-gate funnel across training + May:

- structurally eligible long observations before cooldown: 7,779;
- structurally eligible short observations before cooldown: 7,804;
- long suppressed by 15-minute cooldown: 5,120;
- short suppressed by cooldown: 5,148;
- rejected by fixed 0.10-lot stop risk > USD 40: 2,300;
- invalid-side pivot rejects: 831;
- final broad labeled candidates: 2,184.

### Training — 2026-03-12 through 2026-04-30

- candidates: 1,225;
- long: 617;
- short: 608;
- median stop risk: USD 21.70;
- T30: 38.04%;
- T40: 32.33%;
- T50: 28.00%;
- T70: 20.65%;
- T100: 15.27%.

### May calibration — 2026-05-01 through 2026-05-31

- candidates: 959;
- long: 473;
- short: 486;
- median stop risk: USD 21.10;
- T30: 38.89%;
- T40: 33.79%;
- T50: 29.61%;
- T70: 24.19%;
- T100: 18.25%.

Interpretation:

- the broad structural candidate set had stable target-label prevalence across training/May;
- this does **not** establish a profitable scanner;
- it does **not** establish that generic pivots should replace strategy engines;
- June–September EXP-015 outcomes were not required to make the current architecture correction.

## Re-entry conditions

Do not resume EXP-015 until all are true:

1. EXP-014 original Engine A recovery is complete or honestly declared unrecoverable;
2. the recovered/retained engines emit the common candidate contract in docs/STRATEGY-ENGINE-CONTRACT.md;
3. equivalent sizing for non-Gold markets is frozen prospectively;
4. the ranker feature set is rebuilt around engine-generated candidates;
5. training/calibration/holdout dates are re-declared before further outcome inspection.

## Future ranker purpose

Once resumed, EXP-015 should estimate target-first probabilities / expected value for **validated-engine candidates**, compare them across markets, and reject candidates that fail probability, structural-risk, margin, exposure, or daily-state gates.

It is a selection layer, not the default entry-strategy generator.
