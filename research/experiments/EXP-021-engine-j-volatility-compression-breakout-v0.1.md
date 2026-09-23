# EXP-021 — Engine J Volatility Compression Breakout v0.1

**Status:** FROZEN / NOT YET RUN  
**Frozen:** 2026-09-23  
**Engine:** Engine J — Volatility Compression Breakout v0.1  
**Spec:** `strategies/engine-j-volatility-compression-breakout/SPEC-v0.1.md`  
**Outcome status at freeze:** ZERO ENGINE-J OUTCOMES CALCULATED

## Why EXP-021 exists

Engine I solved the frequency problem but failed economics decisively:

- 197 accepted development trades;
- primary-cost expectancy about -USD5.15/trade;
- primary-cost PF 0.631;
- DEV-A and DEV-B both negative;
- max drawdown about USD1,060.90;
- bootstrap expectancy interval entirely negative.

Per the frozen fast-turnover rule, Engine I stops before validation and is not tuned.

Engine J changes causal family again.

## Frozen thesis

```text
same-day 5m volatility baseline
    ->
30m realized-range compression / compact price box
    ->
strong 5m expansion closes outside box
    ->
next-active-M1-open entry
    ->
breakout-bar structural stop
    ->
fixed T40 actual target
```

No Asian boundary, pre-established direction, pullback, reversal MSS, FVG, or retest is required.

## Frozen center rule

- XAUUSD first;
- exact 0.001-XAU integer ticks;
- candidate breakout completion 06:00 to before 18:00 UTC;
- previous 30 same-day active 5m bars required;
- older 24 bars define baseline median range;
- latest 6 bars define compression;
- compression average range <=80% of baseline median;
- compression box width <=3.0x baseline median;
- breakout bar opens from inside the relevant box boundary and closes outside it;
- breakout range >=1.25x baseline median;
- body >=60% of bar range;
- close in directional outer 25%;
- first qualifying breakout per side/day only;
- entry = next active M1 open before 18:00;
- stop = one tick beyond breakout-bar opposite extreme;
- structural risk <=4000 ticks / approximately USD40 gross;
- actual target = T40;
- T30/T40/T50/T70/T100 diagnostics;
- horizon = 120 active M1 bars or 20:00 UTC;
- one open Engine-J trade maximum;
- conservative same-bar stop-first handling;
- primary cost USD5 / 0.50 XAU from run one.

## Split

Warm-up:

`2022-12-01 through 2022-12-31`.

Development:

`2023-01-01 through 2025-02-28`.

DEV-A:

`2023-01-01 through 2023-12-31`.

DEV-B:

`2024-01-01 through 2025-02-28`.

Validation:

`2025-03-01 through 2025-08-31`.

Fresh holdout:

`2025-09-01 through 2026-02-28`.

Mar-2026 through Aug-20-2026 remains quarantined.

## Contamination classification

Jan-2023 through Feb-2025 is reusable development data, not pristine project-level data, because G/H/I development outcomes have been inspected there.

At this freeze:

- zero Engine-J outcomes exist;
- no Engine-J sensitivity grid exists;
- the complete center configuration is frozen before Engine-J development.

Validation and fresh holdout remain sealed and were not inspected by Engine-I validation/holdout because Engine I failed development.

## Frequency design

The rule allows up to the first qualifying long and first qualifying short compression breakout per eligible weekday.

There is no pullback/retest/confirmation stack after breakout.

This is designed to produce >=100 accepted development trades naturally.

If accepted trades are below 100, the threshold is not lowered.

## Frozen development gate

Validation forbidden unless all pass:

1. accepted trades >=100;
2. combined primary-cost expectancy >0;
3. DEV-A primary-cost expectancy >0;
4. DEV-B primary-cost expectancy >0;
5. primary-cost PF >=1.10;
6. max drawdown <=USD200;
7. recovery factor >=1.00;
8. no causal leakage;
9. no optimistic same-bar handling;
10. no provenance defect.

## Validation and holdout gate

Each later split requires:

- >=50 accepted trades;
- primary-cost expectancy >0;
- PF >=1.10;
- 95% 5-weekday-block bootstrap expectancy lower bound >0;
- max drawdown <=USD200;
- no causal/provenance/same-bar defect.

## Bootstrap

- block size: 5 eligible weekdays;
- replications: 10,000;
- seed: `21021`;
- percentile 95%.

## No-parameter-mining rule

EXP-021 has one center rule.

Do not rescue failure by trying nearby compression lengths, baseline lengths, thresholds, session windows, stop definitions, or targets.

If Engine J fails decisively, preserve validation/holdout and move to another genuinely different engine family.

## Checkpoint 0 — frozen before outcomes

- spec frozen: YES;
- experiment frozen: YES;
- development/validation/holdout split frozen: YES;
- primary cost frozen: YES;
- promotion gates frozen: YES;
- Engine-J outcomes calculated: NO;
- Engine-J implementation started: NO;
- Engine-J development launched: NO.

## Next

User reviews the frozen specification.

Only after approval:

1. implement exact-arithmetic Engine J;
2. run preflight/provenance with zero outcomes;
3. checkpoint;
4. run development only.
