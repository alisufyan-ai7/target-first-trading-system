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


## Checkpoint 1 — implementation and preflight verified before outcomes

**Outcome status:** ZERO ENGINE-J OUTCOMES CALCULATED.

Reference implementation:

- `research/code/engine-j-v0.1.js`;
- initial implementation commit: `e9953da73357e546bc0e72d0c9d8079a7ee84544`;
- final preflight-ready implementation commit: `a59cc2cf1a48b49c6e76a7da99aa7ed51dd56064`.

Execution harnesses:

- preflight verifier: `research/code/run-engine-j-preflight.js`;
- development runner: `research/code/run-engine-j-development.js`;
- preflight workflow: `.github/workflows/exp021-engine-j-preflight.yml`;
- development workflow: `.github/workflows/exp021-engine-j-development.yml`.

The development workflow exists but has **not** been triggered.

### Final preflight

Successful GitHub Actions run:

- run ID: `35869719236`;
- tested repository SHA: `88717bb88993f2cbbffe1f7174e6d49e3201695f`;
- result commit: `1473aa343c7d0ea746c4ff643571fb729329f687`;
- engine file SHA-256: `21f60faee3263d5a33b7b5448a79e1355e30562bb4f5dcc677b09e7e3b6ac1ce`;
- durable result: `research/results/EXP-021-preflight-v0.1.json`.

Preflight verified:

- 27 frozen warm-up/development files only;
- 1,182,240 total M1 rows;
- 59,108,737 total bytes;
- every file matched frozen Git blob SHA and byte size;
- every file matched exact full-month row count;
- every first/last timestamp matched exact calendar-month boundaries;
- one-minute chronology passed;
- exact 0.001-XAU grid and OHLC validity passed;
- validation/holdout filenames were absent from the development runner and workflow;
- validation/holdout data were not loaded;
- exact integer compression comparisons are present;
- exact integer breakout-expansion comparison is present;
- the breakout bar is excluded from the previous-30 window;
- same-day history enforcement is present;
- conservative stop-first same-bar handling is present;
- first-qualifying-breakout-per-side/day consumption is present;
- chronological 20:00 session close is present, including carry-forward final minute handling.

### Self/causality tests

All 16 frozen tests passed:

1. exact tick parsing;
2. off-grid rejection;
3. exact baseline median numerator;
4. compression equality boundary;
5. compression-average failure boundary;
6. compact-box arithmetic;
7. box-width failure boundary;
8. long breakout geometry;
9. short breakout geometry;
10. open-already-outside rejection;
11. close-inside rejection;
12. previous-30 candidate exclusion;
13. same-day history enforcement;
14. structural stop geometry;
15. 4000-tick risk-cap boundary;
16. stop-first same-bar handling.

### Pre-outcome implementation clarification

Before any Engine-J outcome, the implementation made one mechanical interpretation explicit: the 20:00 UTC horizon closes on the final chronological M1 close even when that minute is classified carry-forward. This implements the frozen “final permitted M1 close” rule and changes no strategy threshold.

### Permission to begin next stage

Checkpoint-1 requirements are satisfied.

The **next and only permitted outcome computation** is combined development:

`2023-01-01 through 2025-02-28`

with Dec-2022 warm-up, DEV-A=2023 and DEV-B=Jan-2024 through Feb-2025.

Validation Mar-Aug 2025 and fresh holdout Sep-2025 through Feb-2026 remain sealed and must not be downloaded or run.

**Engine-J development backtest started at this checkpoint: NO.**
