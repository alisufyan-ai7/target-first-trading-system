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
