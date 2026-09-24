# EXP-034 — Engine O v0.1 Rolling Statistical Stretch Reversion

**Status:** CLOSED — ZERO-OUTCOME PREFLIGHT FREQUENCY FAIL  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-o-rolling-statistical-stretch-reversion/SPEC-v0.1.md`

## Purpose

Test a genuinely different continuous-scanning mean-reversion family after Engine N continuation failed development.

## Frozen center design

Every 15 minutes from 06:15 through 17:45 UTC:

- use prior 24 completed M5 bars;
- robust center = median close;
- dispersion = median absolute deviation of close;
- trigger close stretched >=2.50 MAD from center;
- trigger range >=1.25x prior median M5 range;
- body >=50%;
- bullish rejection below center / bearish rejection above center;
- close in favorable outer 35%;
- enter 50% retracement of trigger M5;
- stop beyond trigger extreme;
- order life 10 active M1 / decision+30m;
- unchanged T40 must fit before CENTER;
- unchanged signal-first safe-lot overlay.

## Zero-outcome preflight

Keep the scanner opportunity-density gate:

- >=25 filled signals per market;
- both directions;
- >=300 total;
- safety/causality tests pass;
- no target/P&L outcomes;
- Jul-Aug/Sep sealed.

## Outcome state

No Engine-O outcomes exist at freeze.

## Next

Implement Engine O v0.1 mechanics and run zero-outcome preflight only.


## Preflight attempt 1 — verification fixture failure

**Workflow run:** `36014965193`  
**Trigger SHA:** `b2c50d9c76c3dace3c14f97a6fb99129fdbfcd02`

The workflow failed in deterministic verification before the real multi-market preflight started.

Root cause:

- the baseline-exclusion synthetic test changed the trigger close from 97.4 to 97.2;
- that new close fell outside the frozen favorable outer-35% rejection-location boundary;
- `setup_at()` therefore correctly returned `rejection_close_location_failed`;
- the test then attempted to access a `center` field that is not present on that rejection result.

Correction:

- synthetic trigger close changed to 97.3;
- this still changes the trigger bar while remaining on the frozen rejection boundary;
- strategy rules, thresholds, decision grid, target-room rule, costs and safety logic are unchanged.

Fix commit:

- `99344d6656070d79aa8d562c56869f8e24ca8f7a`.

Evidence status from attempt 1:

- real market preflight executed: **NO**;
- Engine-O target outcomes: **NO**;
- Engine-O P&L outcomes: **NO**;
- Jul-Aug loaded/inspected: **NO**;
- Sep loaded/inspected: **NO**.

### Next

Rerun the identical frozen EXP-034 zero-outcome preflight.


## Zero-outcome preflight outcome — FAIL

**Retry workflow run:** `36017351416`  
**Retry trigger SHA:** `315be86975a7e1763469c00a726d2da547377972`  
**Durable result commit:** `65f37da`

Protection:

- target outcomes: **NO**;
- P&L outcomes: **NO**;
- parsed source max timestamp: **2026-06-30 23:59:00 UTC**;
- Jul-Aug: unopened;
- Sep: unopened.

Result:

- filled valid signals: **209**;
- safely deployable: **209**;
- required total: >=300;
- six of eight markets passed >=25 + both-directions;
- USDJPY: 18;
- AUDUSD: 22;
- all markets had LONG + SHORT;
- safe overlay passed.

Per-market signals:

- XAUUSD 27;
- EURUSD 34;
- GBPUSD 28;
- USDJPY 18;
- EURJPY 25;
- AUDUSD 22;
- USDCAD 28;
- USDCHF 27.

Utility:

- GE40 3;
- GE30 44;
- LT30 162.

### Diagnosis

The statistical-stretch/rejection mechanics produced a reasonably broad cross-market signal stream, but the frozen **15-minute decision grid** left total opportunity density below the project standard.

The target-room gate was not the primary bottleneck; only a handful of otherwise qualified setups failed it.

**Disposition:** insufficient frequency. Do not calculate v0.1 outcomes.

### Next design implication

Do not lower the >=300 / >=25-per-market gate.

Because zero v0.1 outcomes were inspected, prospectively broaden **only the decision grid** from every 15 minutes to every completed M5 bar during the same active intraday window.

All statistical thresholds, rejection rules, non-chasing entry, target-room, costs and safety rules remain unchanged.

This becomes Engine O v0.2 / EXP-035.
