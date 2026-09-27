# EXP-045 — Engine S Human-Style Liquidity Decision Tree v0.2

**Status:** PROSPECTIVE ZERO-OUTCOME FREEZE  
**Frozen:** 2026-09-27  
**Parent:** EXP-045 / Engine S v0.1  
**Paid data required:** NO  
**Market:** XAUUSD

## 1. Why v0.2 exists

Engine-S v0.1 failed only its zero-outcome opportunity-density gate.

No target label, MFE/MAE, win rate, P&L or post-entry path was calculated.

v0.1 generated abundant level interactions but compressed human confirmation into one M1 bar:

`MSS close-through + 1.50x displacement + same-direction FVG`.

The v0.2 correction is temporal, not outcome-driven:

`MSS -> displacement -> FVG -> midpoint retracement`.

Each stage may occur on a later active M1 bar within a frozen short window.

## 2. Immutable source / split

Exactly unchanged from v0.1:

- source repo: `kevingtlin/Market-Data-Lab`;
- source commit: `922f83a60cc574e7395fb27397077288055a1ef6`;
- Dec-2023 warm-up;
- development 2024-01-01 through 2025-02-28;
- validation 2025-03-01 through 2025-08-31 sealed;
- fresh holdout 2025-09-01 through 2026-02-28 sealed.

## 3. Unchanged location / branch rules

All v0.1 rules remain unchanged unless explicitly replaced below:

- PDH/PDL;
- Asia 00:00-06:00 UTC;
- opening range 06:00-09:00 UTC;
- setup window 06:00-17:00 UTC;
- first attack consumes a level;
- dual-sided 5m attacks are skipped;
- same-side level priority PDH/PDL -> Asia -> opening range;
- rejection/reclaim branch;
- acceptance/hold branch;
- next active 5m acceptance confirmation;
- acceptance cancelled by later completed 5m close back through level before entry;
- causal 2L2R internal pivots;
- 1.50x prior-20 active-M1 body displacement threshold;
- same-direction 3-bar M1 FVG;
- FVG midpoint entry;
- structural stop;
- gross stop risk <= USD40 at Gold 0.10-lot convention;
- conservative same-bar pre-entry invalidation;
- no target/path/P&L computation.

## 4. Rejection confirmation sequence

After a completed 5m rejection/reclaim attack:

### Stage R1 — MSS

Search at most **15 market-active M1 bars** after the completed attack bar.

Use the same frozen internal pivot type:

- rejection SHORT breaks a pivot LOW;
- rejection LONG breaks a pivot HIGH.

The first active M1 close through the selected pivot freezes the MSS bar.

If no close-through occurs within 15 active M1 bars:

`mss_timeout_15`.

### Stage R2 — displacement

Starting with the MSS bar and ending at MSS +2 active M1 bars, accept the first same-direction M1 bar whose body is >=1.50x the prior-20 active-M1 mean body.

If none:

`displacement_timeout_mss_plus_2`.

### Stage R3 — FVG

Starting with the displacement bar and ending at displacement +2 active M1 bars, accept the first same-direction 3-bar M1 FVG.

If none:

`fvg_timeout_displacement_plus_2`.

The entry midpoint is frozen from that first qualifying FVG.

### Stage R4 — retracement fill

Midpoint fill search begins with the **next** market-active M1 bar after FVG creation and lasts at most **15 active M1 bars**, still requiring entry before 18:00 UTC.

Structural invalidation remains stop-first on same-bar ambiguity.

## 5. Acceptance confirmation sequence

The initial breakout and next-active-5m acceptance confirmation are unchanged.

### Stage A1 — pullback

After acceptance confirmation, wait at most **60 market-active M1 bars** for the first pullback touching/crossing the attacked level from the breakout side.

Any completed active 5m close back through the level cancels the setup before entry.

If no pullback within 60 active M1 bars:

`pullback_timeout_60`.

### Stage A2 — MSS

At first pullback touch, freeze the same causal pivot rule as v0.1.

Search at most **15 active M1 bars** after the touch for same-direction close-through.

If none:

`mss_timeout_15`.

### Stage A3 — displacement

MSS bar through MSS +2 active M1 bars, same unchanged 1.50x displacement requirement.

### Stage A4 — FVG

Displacement bar through displacement +2 active M1 bars, same-direction FVG.

### Stage A5 — retracement fill

Next active M1 bar after FVG creation through +15 active M1 bars, before 18:00 UTC.

Structural stop uses the most adverse M1 extreme from first pullback touch through the accepted FVG bar, plus one source tick.

## 6. Why these timeboxes are frozen

The timeboxes are simple human-process units, not selected from target outcomes:

- 15 active M1 bars = up to three 5m bars for lower-timeframe confirmation;
- +2 active M1 bars = immediate follow-through after MSS/displacement;
- 60 active M1 bars = up to one hour for a genuine breakout retest;
- 15 active M1 bars = a non-chasing entry window after confirmation.

No target or profitability outcome informed these choices.

## 7. v0.2 zero-outcome preflight gate

Exactly the same adequacy gate as v0.1:

- >=100 accepted filled candidates total;
- >=25 rejection candidates;
- >=25 acceptance candidates;
- both long and short in each branch;
- >=50 distinct development weekdays with >=1 accepted candidate;
- median accepted candidates per active signal day <=4;
- no causal leakage;
- no validation/holdout file loaded;
- zero target/P&L outcome computation.

If v0.2 fails, do not loosen v0.2 after the fact.

## 8. Zero-outcome reporting

Report:

- full branch/stage funnel;
- terminal reason counts;
- level/side/direction attribution;
- time-to-MSS distribution;
- MSS-to-displacement bars;
- displacement-to-FVG bars;
- FVG-to-fill bars;
- pullback wait distribution for acceptance;
- stop geometry;
- active setup days;
- pending-pipeline overlap diagnostics.

Do not report any post-entry market path.

## 9. Governance after PASS

Only if v0.2 passes naturally may the project freeze Engine-S structural target and trade-management rules before inspecting any target/path result.

No validation/holdout data are authorized by preflight PASS alone.


## Pre-run same-timestamp acceptance ordering clarification

If an active M1 bar closes at the exact timestamp of a completed active 5m bar, and that 5m bar closes back through the acceptance level, the 5m cancellation is applied **before** using that M1 close for acceptance pullback/MSS/displacement/FVG/entry processing.

This conservative rule prevents same-timestamp intrabar ordering from creating an acceptance candidate.


## Zero-outcome implementation checkpoint

Frozen before any v0.2 target/path/P&L outcome:

- final spec including conservative same-timestamp ordering: `a83afb25c543c1772a3ded5fb00ad281a6a3d6db`;
- final Engine-S v0.2 state machine: `262e3ca7b1322adce2a35b7bcba14d0369d31e51`;
- source-verifying runner: `b109793b390538e5051f2e2058d936f85d9139f3`;
- workflow: `47fd28a697b25f08781e267cb22321afa1bf584c`.

Static pre-run audit confirmed:

- source manifest exactly matches the already verified 15-file Engine-H manifest;
- v0.2 runner uses EngineSv02 and v0.2 result paths;
- no target-before-stop labels exist in engine code;
- no MFE/MAE logic exists;
- no P&L/profit-factor/win-rate logic exists;
- validation/holdout files are not downloaded.

**Exact next action:** trigger one EXP-045 Engine-S v0.2 zero-outcome preflight.


## v0.2 zero-outcome result and final sample-adequacy confirmation — 2026-09-27

Durable v0.2 result commit:

`fa21229d80ba5ae0b4b57dbfa3f392722cacb040`

v0.2 remained fully zero-outcome and causally valid.

Observed:

- 57 accepted filled candidates;
- 45 rejection;
- 12 acceptance;
- 55 distinct active signal days;
- median 1 candidate per active signal day;
- both directions present in both branches.

The unchanged adequacy gate still failed only on:

- total >=100;
- acceptance >=25.

The sequential process materially improved v0.1 density (22 -> 57 fills; 21 -> 55 signal days) without exposing profitability.

### Final zero-outcome sample extension

No Engine-S target/P&L outcome has yet been exposed.

Therefore one final **sample-size** confirmation is authorized with the exact same Engine-S v0.2 rules and the exact same adequacy gate.

Frozen source:

- same `kevingtlin/Market-Data-Lab` repository;
- same pinned source commit `922f83a60cc574e7395fb27397077288055a1ef6`;
- same XAUUSD BID M1 schema.

Frozen interval:

- warm-up: 2021-12-01 through 2021-12-31;
- zero-outcome development: 2022-01-01 through 2025-02-28;
- validation remains sealed from 2025-03-01;
- fresh holdout remains sealed from 2025-09-01.

No setup rule, level, timebox, pivot, displacement threshold, FVG rule, entry rule, stop rule or USD40 risk cap changes.

The preflight adequacy gate remains exactly:

- >=100 accepted filled candidates total;
- >=25 rejection;
- >=25 acceptance;
- both long and short in each branch;
- >=50 active signal days;
- median <=4 accepted candidates per active signal day;
- causality pass;
- no validation/holdout;
- zero target/P&L outcomes.

This extension is for statistical sample adequacy only. It does **not** claim or manufacture higher daily opportunity frequency.

### Anti-loop stop

This is the final zero-outcome density attempt for Engine S v0.2.

- PASS => freeze target/path and management rules before any Engine-S outcome is calculated.
- FAIL => close Engine S; do not alter density rules again.
