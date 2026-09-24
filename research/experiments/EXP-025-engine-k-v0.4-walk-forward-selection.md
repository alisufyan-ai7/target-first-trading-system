# EXP-025 — Engine K v0.4 Bounded Walk-Forward Selection

**Status:** FROZEN PROSPECTIVELY BEFORE WALK-FORWARD METRICS  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-k-direct-target-move-scanner/SPEC-v0.4.md`

## Objective

Determine whether Engine K's persistent target-ranking signal can be converted into stable positive economic expectancy using a **small predeclared configuration set** evaluated only by chronological walk-forward development folds.

This replaces manual version-by-version threshold tuning.

## Prior evidence allowed

Mar-Jun 2026 is reusable inspected development evidence.

Known before freeze:
- v0.2 solved multi-market economic admission;
- v0.3 produced 39 June trades across 19 weekdays;
- v0.3 June calibrated AUC ~0.672/0.708/0.740 for T30/T40/T50;
- v0.3 June economics failed;
- Jul-Aug and Sep remain unopened.

## Fixed search space

12 configurations only:
- 2 HGB variants;
- 2 Platt calibration variants;
- 3 stress-EV qualification policies.

See SPEC-v0.4 for exact parameters.

## Fixed folds

Six expanding-window chronological folds spanning Apr13-Jun30 evaluation periods. All data >=Jul1 remains sealed.

## Configuration gate

A configuration must satisfy all frozen trade-count, multi-fold stability, expectancy, PF, drawdown, hit-rate, concentration, and integrity criteria.

## Winner rule

Choose among passers by:
1. highest worst-fold stress expectancy;
2. highest pooled stress PF;
3. lowest pooled stress MDD;
4. highest total trades;
5. configuration ID.

If none pass, stop before July-Aug.

## Protected evidence

At freeze:
- Jul-Aug secondary outcomes inspected: NO;
- Sep final holdout inspected: NO.

## Next

Implement one development-only runner/workflow for the exact 12 configs and six folds, checkpoint results, and do not create a secondary-test workflow unless one configuration passes.
