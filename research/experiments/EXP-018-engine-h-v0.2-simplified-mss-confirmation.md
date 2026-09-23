# EXP-018 — Engine H v0.2 Simplified MSS Confirmation

**Status:** FROZEN / NOT YET RUN  
**Frozen:** 2026-09-23  
**Engine:** Engine H — Range Raid into Pre-existing FVG Reversal v0.2  
**Spec:** `strategies/engine-h-range-raid-preexisting-fvg-reversal/SPEC-v0.2.md`  
**Outcome status at freeze:** ZERO Engine-H-v0.2 outcomes

## Why v0.2 exists

Engine H v0.1 generated 180 in-window qualifying location raids but only 2 accepted filled trades because its post-raid confirmation stack required:

- MSS;
- 1.50x displacement;
- a newly created same-direction 1m FVG on the displacement candle;
- midpoint retracement;
- subsequent limit fill.

v0.2 prospectively tests a simpler causal confirmation:

```text
same frozen range/FVG raid location
    ->
1m MSS within 20 active bars
    ->
entry at next active M1 open
```

The redesign is frozen before v0.2 outcomes.

## Frozen unchanged core

- 12-active-5m recent range;
- unmitigated external 5m FVG, age <=48 active 5m bars;
- first-touch raid into selected external FVG;
- close strictly back inside the range;
- 06:00-18:00 UTC setup window;
- causal internal M1 pivot;
- stop one tick beyond sweep extreme;
- opposite-range actual target;
- minimum 3.000-XAU target room;
- minimum 2.0 reward/risk;
- gross structural stop <=USD40 at 0.10 lot;
- primary 0.50-XAU round-trip cost;
- 120-active-M1/20:00 exit horizon;
- conservative stop-first same-bar ordering;
- one open Engine-H trade.

## Frozen change

- MSS window: 20 active M1 bars;
- no displacement threshold;
- no new 1m FVG requirement;
- no FVG midpoint retracement;
- entry = next market-active M1 open after MSS.

## Data sequence

Warm-up: Dec 2023.

Development: Jan 2024-Feb 2025.

Validation: Mar-Aug 2025.

Fresh holdout: Sep 2025-Feb 2026.

March-Aug 20, 2026 quarantined.

## Evidence gates

Development >=100 accepted filled trades.

Validation >=50.

Holdout >=50.

Development, validation and holdout expectancy >0 at primary cost.

Validation/holdout PF >=1.10.

Validation/holdout bootstrap expectancy lower bound >0.

## Checkpoint 0

- v0.2 frozen before outcomes: YES;
- validation/holdout still untouched: YES;
- Engine-H-v0.2 outcomes calculated: NO;
- next permitted outcome: DEVELOPMENT ONLY.

## Pre-outcome deterministic same-open clarification

Before any v0.2 outcome calculation, simultaneous next-open entries were made deterministic:

1. earlier sweep completion timestamp;
2. then lower setup ID.

At a shared next active M1 open, setups are tested in that order against the already-frozen geometry/risk/room/R:R admission rules. The first passing setup opens the trade; remaining same-open setups become `suppressed_one_open`. A rejected earlier-priority setup does not block a later setup from being tested at that same open.

**Engine-H-v0.2 outcomes calculated at this point: ZERO.**
