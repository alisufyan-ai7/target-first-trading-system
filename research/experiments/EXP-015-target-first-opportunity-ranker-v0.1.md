# EXP-015 — Target-First Opportunity Ranker v0.1

**Status:** PAUSED — WAITING FOR VALIDATED REPRODUCIBLE ENGINE CANDIDATES  
**Date:** 2026-09-23

## Why this file exists

This experiment was originally created under the duplicate ID EXP-014.

It has been renumbered to preserve unique experiment IDs and to restore the correct project sequence.

EXP-014 is now complete:

- Part A systematically investigated original Engine A recovery and honestly closed it as unrecoverable from the surviving evidence;
- Part B froze the forward P&L-equivalent sizing methodology.

EXP-015 does **not** resume automatically. It still requires at least one validated reproducible engine candidate stream.

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

Current status of the prerequisites:

1. **SATISFIED** — EXP-014 Part A is complete via the explicitly allowed honest-unrecoverable conclusion.
2. **NOT SATISFIED** — there is currently no promoted reproducible validated engine emitting the common candidate contract.
3. **SATISFIED** — equivalent-sizing methodology is frozen in `docs/PNL-EQUIVALENT-SIZING.md`.
4. **NOT YET EXECUTED** — ranker features must be rebuilt around the eventual engine-generated candidate stream.
5. **NOT YET EXECUTED** — training/calibration/holdout dates must be re-declared prospectively before ranker outcome inspection.

Therefore EXP-015 remains **PAUSED**.

Do not use A6, A8/A9, v0.2-portable, Engine F v0.1, or the broad raw-pivot candidate set merely to satisfy condition 2. A strategy engine must independently earn validated status first.

## Future ranker purpose

Once resumed, EXP-015 should estimate target-first probabilities / expected value for **validated-engine candidates**, compare them across markets, and reject candidates that fail probability, structural-risk, margin, exposure, or daily-state gates.

It is a selection layer, not the default entry-strategy generator.


## Post-EXP-014 note

The next project experiment is **not** an EXP-015 model run.

The immediate missing system component is a prospectively specified causal strategy engine with deterministic candidate generation, structural invalidation, native target logic, data provenance, and development/validation/holdout evidence.

Once such an engine passes, EXP-015 should be redesigned around that engine's standardized candidates and the frozen equivalent-sizing methodology.
