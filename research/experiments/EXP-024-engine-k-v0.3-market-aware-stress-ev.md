# EXP-024 — Engine K v0.3 Market-Aware Stress-EV Scanner

**Status:** CLOSED — JUNE DEVELOPMENT GATE FAILED  
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


## June development outcome — FAIL

**Workflow run:** `35975630207`  
**Tested repository SHA:** `85b01583cd2ab74fb242e7d0d55fabbbf9b4378d`  
**Durable result/model commit:** `db53f3a96fbbb6ed7b1b01f25e931e4140bec215`

Protected scope:

- Mar23-Apr30 model fit;
- May calibration;
- June development gate;
- July-Aug secondary test loaded/labeled: **NO**;
- Sep final holdout loaded/labeled: **NO**.

June output:

- 81,667 labeled rungs;
- 106 qualified candidate rungs before one-open;
- 39 actual one-open trades;
- 19 distinct June trade weekdays;
- 15 target hits;
- hit rate: **38.46%**;
- mean stress break-even probability: **46.79%**;
- mean calibrated probability: **49.52%**;
- primary net P&L: **-USD8.50**;
- primary expectancy: **-USD0.22/trade**;
- stress net P&L: **-USD151.70**;
- stress expectancy: **-USD3.89/trade**;
- primary PF: **0.983**;
- stress PF: **0.742**;
- max drawdown: **USD212.34**;
- longest losing trade run: 5.

Market trade counts:

- GBPUSD 22;
- AUDUSD 10;
- USDCHF 4;
- XAUUSD 2;
- EURJPY 1.

June discrimination remained non-random:

- T30 calibrated AUC: about **0.672**;
- T40: about **0.708**;
- T50: about **0.740**.

Frozen gate disposition:

- >=200 June states per market: PASS;
- >=30 June trades: PASS;
- >=10 trade weekdays: PASS;
- hit rate > mean stress break-even: FAIL;
- primary expectancy >0: FAIL;
- stress expectancy >0: FAIL;
- primary PF >=1.10: FAIL;
- stress PF >=1.00: FAIL;
- max DD <=USD100: FAIL;
- causality/provenance: PASS;
- market contribution reporting: PASS;
- protected-period seal: PASS.

**Final disposition:** FAIL. Stop before July-Aug.

Interpretation:

v0.3 fixed the trade-density problem and preserved useful rank discrimination, but the selected trades were not economically profitable out of sample in June. The issue is no longer candidate scarcity; it is that the manually frozen model/calibration/qualification configuration is not converting rank signal into positive economic edge.

Do not open July-Aug or retune v0.3 in place.
