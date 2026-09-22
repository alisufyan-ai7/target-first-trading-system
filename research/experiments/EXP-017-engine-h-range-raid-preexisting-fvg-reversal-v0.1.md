# EXP-017 — Engine H Range Raid into Pre-existing FVG Reversal v0.1

**Status:** FROZEN / NOT YET RUN  
**Frozen:** 2026-09-23  
**Engine:** Engine H v0.1  
**Spec:** `strategies/engine-h-range-raid-preexisting-fvg-reversal/SPEC-v0.1.md`  
**Engine-H outcomes at freeze:** ZERO

## Hypothesis

Test whether a recent 12-active-5m dealing-range boundary raid into an older, still-unmitigated external 5m FVG, followed by causal lower-timeframe MSS and displacement-created 1m entry FVG, can produce a cost-robust reversal stream whose actual target is the opposite frozen range boundary.

This is a prospective formalization inspired by the two user-provided videos. It is not a claim to reproduce the creator's complete strategy.

## Frozen center rules

- XAUUSD;
- integer 0.001-XAU source ticks;
- setup window 06:00-18:00 UTC;
- recent range = previous 12 active 5m bars;
- location FVG = pre-existing unmitigated external 5m FVG, age <=48 active 5m bars;
- raid bar must sweep range boundary, overlap the selected external FVG and close back inside the range;
- causal 1m opposite pivot from prior 15 active M1;
- MSS <=10 active M1;
- first MSS/MSS+1/MSS+2 candle satisfying 1.50x prior-20 body displacement AND creating same-direction 1m FVG;
- entry at directional midpoint of that new 1m FVG;
- stop one tick beyond sweep extreme;
- gross structural stop <=USD40 at 0.10 lot;
- actual target = opposite side of frozen pre-sweep range;
- target distance >=3 XAU;
- reward/risk >=2.0;
- entry wait <=10 active M1 and before 18:00;
- actual horizon <=120 active M1 and <=20:00 UTC;
- one Engine-H trade open;
- conservative same-bar ordering;
- primary cost = 0.50 XAU/USD5 per filled trade.

## Primary split

- warm-up: Dec 2023 only;
- development: Jan 2024-Feb 2025;
- validation: Mar-Aug 2025;
- fresh holdout: Sep 2025-Feb 2026;
- Mar-Aug 20 2026 quarantined.

## Frozen evidence gates

- accepted trades: dev >=100, validation >=50, holdout >=50;
- net expectancy at primary cost >0 in all three;
- validation and holdout PF >=1.10;
- validation and holdout 95% moving-block-bootstrap expectancy lower bound >0;
- no sign reversal or causal/provenance defect.

## Development-first discipline

Development is the only permitted first outcome run.

If development is not eligible for eventual promotion, stop EXP-017 v0.1 before validation. No v0.1 retuning.

## Checkpoint 0

- spec frozen before outcomes: YES;
- source/split frozen: YES;
- outcome definitions frozen: YES;
- Engine-H outcomes calculated: NO;
- development run started: NO.
