# EXP-025 — Engine K v0.4 Bounded Walk-Forward Selection

**Status:** CLOSED — NO CONFIGURATION PASSED; STOP BEFORE SECONDARY  
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


## Walk-forward outcome — NO PASSING CONFIGURATION

**Tested repository SHA:** `5f887ecbd3fec1016a3f00ca4ab5e6d0464725d5`  
**Durable result commit:** `24ce35448cb93158aadeb843dce928199c0c5385`  
**Result:** `research/results/EXP-025-walkforward-selection-summary-v0.4.json`

Protection:

- development labeled through Jun30 only;
- Jul-Aug secondary test loaded/labeled: **NO**;
- Sep final holdout loaded/labeled: **NO**;
- forecast-only markets loaded: **NO**.

Outcome:

- 12/12 frozen configurations evaluated;
- 6/6 frozen chronological folds evaluated;
- passing configurations: **0**;
- selected configuration: **NONE**;
- final disposition: `NO_PASSING_CONFIGURATION_STOP_BEFORE_SECONDARY`.

Representative near-misses:

### M1-C1-Q3
- 75 pooled trades;
- 28 trade weekdays;
- primary expectancy **+USD2.15/trade**;
- stress expectancy **-USD1.67/trade**;
- primary PF **1.185**;
- stress PF **0.879**;
- stress MDD **USD301.54**;
- only 1/6 folds positive on stress expectancy;
- zero trades in WF3 and WF6.

### M2-C2-Q3
- 124 pooled trades;
- 28 trade weekdays;
- primary expectancy **+USD0.86/trade**;
- stress expectancy **-USD2.62/trade**;
- primary PF **1.079**;
- stress PF **0.799**;
- stress MDD **USD505.51**;
- 0/6 folds positive on stress expectancy;
- zero trades in WF3 and WF6.

No configuration satisfied the predeclared combination of trade density, cross-fold stability, positive stress expectancy, PF, hit-rate-vs-break-even, drawdown and concentration criteria.

Interpretation:

The persistent AUC/ranking signal does not translate into a robust economically positive Engine-K trading policy under this fixed target/stop/cost architecture. A few configurations can become slightly positive before stress cost, but the advantage is not stable across forward folds and disappears under the frozen stress-cost assumption.

Per the predeclared anti-mining rule:

- do **not** add configurations to EXP-025;
- do **not** change fold dates;
- do **not** weaken pass criteria;
- do **not** select a near-miss;
- do **not** open Jul-Aug.

Engine K tuning on the Mar-Jun development pool is closed.

The next research move must broaden the evidence or prediction design rather than manufacture another threshold.
