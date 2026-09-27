# EXP-045 — Engine S Human-Style Liquidity Decision Tree v0.1

**Status:** PROSPECTIVE FREEZE — ZERO OUTCOMES  
**Frozen:** 2026-09-27  
**Paid data required:** NO  
**Market:** XAUUSD first

## 1. Purpose

Test a selective human-style intraday decision process rather than another broad predictive feature layer.

Core idea:

`meaningful liquidity -> attack -> rejection OR acceptance -> lower-timeframe trigger -> non-chasing entry -> structural invalidation`.

This experiment is not an EXP-002 reconstruction.

## 2. Free source / split

Reuse the pinned free XAUUSD BID M1 source already verified in EXP-016:

- source repository: `kevingtlin/Market-Data-Lab`;
- pinned commit: `922f83a60cc574e7395fb27397077288055a1ef6`.

Warm-up:

- December 2023.

Development / zero-outcome preflight:

- 2024-01-01 through 2025-02-28.

Remain sealed for Engine S outcomes:

- validation: 2025-03-01 through 2025-08-31;
- fresh holdout: 2025-09-01 through 2026-02-28;
- 2026-03 onward is not needed for initial Engine-S research.

## 3. Meaningful liquidity map

Only levels known before the setup event may be used.

Frozen level classes:

1. prior market-active UTC-day high;
2. prior market-active UTC-day low;
3. current-day Asia range high after 06:00 UTC;
4. current-day Asia range low after 06:00 UTC;
5. current-day 06:00-09:00 opening-range high after 09:00 UTC;
6. current-day 06:00-09:00 opening-range low after 09:00 UTC.

Asia range is frozen as:

`00:00 <= t < 06:00 UTC`.

Opening range is frozen as:

`06:00 <= t < 09:00 UTC`.

No equal-high clustering, discretionary trendline, or manually selected level is allowed in v0.1.

## 4. Active decision window

Potential setup events:

`06:00 <= completed 5m bar close time < 17:00 UTC`.

A level must already be fully known before the 5m bar begins.

One level-attack event can produce at most one Engine-S candidate.

## 5. Branch A — rejection / reclaim reversal

A completed 5m bar attacks an external level and closes back on the original side of that level.

For high-side liquidity:

- 5m high > level;
- 5m close < level.

For low-side liquidity:

- 5m low < level;
- 5m close > level.

After that completed bar:

1. search max 10 active M1 bars for opposite-direction internal MSS using causal 2L2R pivot;
2. require displacement body >=1.50x prior-20 active-M1 mean body;
3. displacement must create a same-direction 1m FVG;
4. first such FVG only;
5. entry = directional 50% FVG midpoint;
6. entry wait max 10 active M1 bars;
7. entry must occur before 18:00 UTC;
8. stop = one source tick beyond the completed 5m attack extreme.

## 6. Branch B — acceptance / hold continuation

A completed 5m bar closes beyond an external level.

Acceptance is confirmed only if the **next completed active 5m bar** also closes on the breakout side of the level.

Then:

1. wait for the first pullback within max 30 active M1 bars that touches/crosses the level from the breakout side;
2. the pullback must not produce a completed 5m close back through the level before entry;
3. after the pullback touch, search max 10 active M1 bars for same-direction causal 2L2R MSS/continuation break;
4. require same 1.50x displacement rule;
5. require same-direction 1m FVG;
6. entry = directional 50% FVG midpoint;
7. entry wait max 10 active M1 bars;
8. entry before 18:00 UTC;
9. stop = one source tick beyond the pullback extreme.

## 7. Mutual exclusivity

A first 5m interaction cannot be both branches.

- close back through attacked level => rejection branch;
- close beyond level => possible acceptance branch;
- acceptance is cancelled if the next completed active 5m bar closes back through the level.

If two eligible level classes are attacked by the same 5m bar in the same direction, priority is:

1. prior-day high/low;
2. Asia high/low;
3. 06:00-09:00 opening-range high/low.

No duplicate candidate from one market move.

## 8. Non-chasing rule

No market entry on the initial attack, MSS candle, or breakout candle.

Every accepted candidate requires retracement into a post-trigger 1m FVG midpoint.

This preserves the non-chasing lesson from EXP-038.

## 9. Zero-outcome preflight only

The first Engine-S run must not calculate:

- T30/T40/T50/T70/T100;
- target-first labels;
- MFE/MAE after entry;
- trade P&L;
- win rate;
- profit factor;
- daily profit.

It may calculate only:

- level-attack counts;
- branch counts;
- MSS/displacement/FVG funnel;
- retracement-fill counts;
- long/short counts;
- branch/location attribution;
- signal timestamps;
- entry/stop geometry;
- structural stop distribution;
- active setup days;
- one-open conflict counts.

## 10. Preflight adequacy gate

Development preflight PASS requires:

- >=100 accepted filled candidates total;
- >=25 rejection candidates;
- >=25 acceptance candidates;
- both long and short candidates in each branch;
- >=50 distinct development weekdays with at least one accepted candidate;
- median accepted candidates per active signal day <=4;
- no causal leakage;
- all level timestamps known before attack;
- all entry triggers strictly after the completed level interaction;
- no validation/holdout file loaded;
- zero target/P&L outcome computation.

If the gate fails, do not loosen rules inside v0.1.

## 11. Target-path freeze after preflight PASS

Only after a zero-outcome PASS may Engine S freeze its actual outcome logic.

The future target must be structural, not a fixed R imposed first.

Candidate target classes to choose prospectively from the setup map include:

- opposing session/range liquidity;
- prior-day opposite extreme when causally available;
- next meaningful external liquidity;
- first partial at a structural path milestone plus runner.

The exact target/partial rule must be frozen **before** any Engine-S target outcome is calculated.

## 12. Why this is different from recent failed research

This experiment does not ask a universal model to predict every broad pivot.

It encodes the human decision sequence:

- meaningful location;
- observe behavior at the location;
- branch on rejection versus acceptance;
- wait for causal lower-timeframe confirmation;
- avoid chasing;
- use structural invalidation;
- later require structural target room.

## 13. Governance

EXP-044 paid true-flow source work is paused under the user's no-paid-data constraint.

Engine R and EXP-015 remain paused.

No protected Jul-Aug/Sep 2026 data are required for EXP-045.


## Pre-outcome mechanical clarifications — 2026-09-27

These rules are frozen before any Engine-S outcome or preflight result exists.

1. **Level consumption:** each concrete daily level instance may create at most one attack event. Its first qualifying completed-5m attack consumes it for the rest of that UTC day, regardless of whether the downstream setup fills.

2. **Dual-sided ambiguity:** if the same completed 5m bar simultaneously attacks eligible high-side and low-side liquidity, the event is classified `dual_sided_attack_ambiguous` and no setup is created.

3. **Priority within one side:** if one completed 5m bar attacks multiple eligible levels on the same side, use only the frozen priority PDH/PDL -> Asia -> opening-range.

4. **Internal pivot selection:** use the most recent causally confirmed 2-left/2-right M1 pivot of the required break type within the prior 15 market-active M1 bars at the branch trigger anchor.
   - rejection SHORT breaks an internal pivot LOW;
   - rejection LONG breaks an internal pivot HIGH;
   - acceptance LONG breaks an internal pivot HIGH after the pullback touch;
   - acceptance SHORT breaks an internal pivot LOW after the pullback touch.
   The pivot must already be confirmed before the M1 trigger bar closes.

5. **Trigger bar:** within the frozen 10-active-M1 trigger search, the first bar that closes through the selected pivot is accepted as a trigger only if that same bar:
   - has directional body;
   - has body >=1.50x the prior-20 active-M1 mean body using exact integer arithmetic;
   - creates the same-direction 3-bar M1 FVG.
   A close-through that does not satisfy all three conditions does not trigger; search continues until the 10-bar window expires.

6. **Non-chasing fill:** the FVG midpoint cannot fill on the trigger/FVG-creation bar. Fill search starts with the next market-active M1 bar and lasts at most 10 active M1 bars.

7. **Acceptance pivot anchor:** the acceptance branch selects its internal pivot at the first pullback-touch bar close, after the pullback has occurred. The pivot center must be later than the initial breakout attack bar start and already confirmed by pullback-touch close.

8. **Acceptance pullback extreme:** structural stop uses the most adverse M1 extreme from the first level-touch pullback bar through the trigger/FVG bar, plus one source tick.

9. **Economic admission:** accepted filled candidates must have valid stop geometry and gross structural risk <= USD40 under the XAUUSD 0.10-lot / 10-oz convention, i.e. stop distance <=4.000 XAU / 4,000 source ticks.

10. **Zero-outcome one-open handling:** because no post-entry exit/target path may be computed in preflight, the preflight does not impose a synthetic one-open-trade duration. It reports overlapping pending setup pipelines as a diagnostic only. A true one-open rule is frozen later together with target/horizon management if the preflight passes.

11. **Active-bar convention:** market-active M1 follows the already audited Engine-G/H convention: an M1 row identical OHLC to the previous close is carry-forward/inactive. A 5m bar is active if at least one constituent M1 row is active.

No target, MFE/MAE, trade P&L or post-entry path is inspected by these clarifications.


12. **Pre-entry invalidation:** after a valid trigger/FVG exists but before midpoint fill, touching/breaching the frozen structural stop cancels the setup. For the acceptance branch, any completed active 5m close back through the attacked level before entry also cancels the setup, as already required by Section 6.

13. **No post-entry inspection:** once a midpoint fill is registered as an accepted preflight candidate, Engine-S preflight immediately stops evaluating that candidate. No later bar is read for that candidate's MFE, MAE, stop, target, timeout, P&L, or win/loss status.


14. **Liquidity freshness across the day:** level attack/consumption is tracked from the moment a level becomes causally known, even outside the 06:00-17:00 setup-creation window. Thus a PDH/PDL attacked before 06:00 is no longer fresh for a later Engine-S setup. Asia levels begin consumption eligibility at 06:00; opening-range levels at 09:00. Only attacks whose completed 5m close satisfies the frozen setup window may create a setup.
