# EXP-024 — Engine K v0.3 Market-Aware Stress-EV Scanner

**Status:** FROZEN PROSPECTIVELY BEFORE V0.3 METRICS  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-k-direct-target-move-scanner/SPEC-v0.3.md`

## Purpose

Test whether Engine K's observed target-ranking signal can produce a sufficiently dense, cost-robust trading stream when probability calibration and gating are separated chronologically and qualification is based on positive stress EV instead of an arbitrary absolute probability floor.

## Evidence motivating the redesign

EXP-023 / v0.2:

- solved cross-market economic admission;
- 281,955 labeled rungs across all eight execution markets;
- June AUC ~0.674 / 0.710 / 0.743 for T30/T40/T50;
- only 2 qualified combined trades and 0 June trades under the frozen v0.2 threshold;
- July-Aug and September remained unopened.

These facts may guide v0.3 because Mar-Jun is now reusable development evidence.

## Frozen v0.3 chronology

- HGB fit: Mar23-Apr30;
- market-direction-aware Platt calibration: May;
- development gate: June;
- secondary test if gate passes: Jul-Aug;
- final holdout if secondary passes: Sep1-Sep22.

## Frozen economics

Unchanged from v0.2.

Gold:

- +3/+4/+5 XAU;
- 0.10 lot anchor.

Non-Gold:

- T30 1.5R;
- T40 2.0R;
- T50 2.5R;
- target first, then downward USD30/40/50-equivalent size.

Risk/cost:

- stop risk <=USD20;
- notional <=USD50k;
- research margin <=USD100;
- primary cost 10% of actual gross target;
- stress cost 20%.

## Frozen calibration redesign

Per rung, calibration on May only uses logistic regression with:

- clipped logit(raw HGB probability);
- market one-hot;
- direction one-hot.

This is a market-direction-aware Platt transform.

## Frozen qualification

Candidate qualifies only if:

- primary EV >0;
- stress EV >0;
- all other economic/session/data gates pass.

No universal probability floor.

## June mandatory gate

- >=200 admissible states per market;
- >=30 one-open trades;
- >=10 distinct trade weekdays;
- observed hit rate > mean stress break-even;
- primary expectancy >0;
- stress expectancy >0;
- primary PF >=1.10;
- stress PF >=1.00;
- max DD <=USD100;
- integrity/provenance pass;
- market contribution reported;
- protected periods sealed.

Fail any -> stop before July-Aug.

## Protected evidence

At EXP-024 freeze:

- July-Aug outcomes inspected for v0.3: NO;
- Sep holdout inspected: NO.

## Next step

Implement a separate v0.3 development-gate runner/workflow. It may parse only through June 30 and must not load July-Aug or September.
