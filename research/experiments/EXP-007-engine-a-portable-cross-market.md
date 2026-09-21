# EXP-007 — Engine A v0.2 Portable Cross-Market Screen

**Status:** IN PROGRESS — RULES FROZEN BEFORE OUTCOME INSPECTION  
**Date:** 2026-09-22

## Question

Does a fully mechanical, portable Engine A variant retain positive target-first expectancy when applied unchanged to XAUUSD, EURUSD, GBPUSD, and USDJPY?

## Hypothesis

If Engine A captures a transferable liquidity-sweep / structure-shift mechanism rather than XAU-specific noise, at least one non-Gold market should show non-negative or positive holdout expectancy under unchanged rules.

The experiment is also allowed to falsify transferability.

## Strategy

Frozen specification:

- `strategies/engine-a-liquidity-mss-fvg/SPEC-v0.2-portable.md`.

No parameter may be changed after holdout outcomes are inspected.

## Data

External public one-minute GetData samples identified in EXP-006.

Common test window:

- development: 2026-03-12 through 2026-05-31;
- holdout: 2026-06-01 through 2026-08-20.

Instruments:

- XAUUSD;
- EURUSD;
- GBPUSD;
- USDJPY.

## Economics

- structural stop first;
- USD 20 gross risk at stop;
- USD 50 gross target;
- target distance = 2.5R;
- no martingale;
- no size increase after losses;
- no broker-specific costs in this first transferability screen;
- notional/equity diagnostics must be reported.

## Separation rule

Development and holdout results must be reported separately.

No strategy parameter changes are permitted after holdout inspection.

## Promotion rule

A market is not promoted merely because it has a positive total P&L.

To remain a candidate it should show, on holdout:

- non-negative/positive mean R;
- enough observations to be interpretable;
- no obvious collapse from development;
- daily distribution materially useful relative to prior XAU-only screens;
- economic feasibility not obviously incompatible with the USD 500 reference account.

Any positive result remains provisional until costs and an independent feed are tested.

## Next action

Run the frozen rules market by market in small checkpoints. Record each market result before any portfolio combination.
