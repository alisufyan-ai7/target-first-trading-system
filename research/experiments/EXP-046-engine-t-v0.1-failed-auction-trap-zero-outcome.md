# EXP-046 — Engine T v0.1 Failed-Auction Trap Reversal — Zero-Outcome Preflight

**Status:** FROZEN BEFORE ANY ENGINE-T TARGET/PATH/P&L OUTCOME  
**Market:** XAUUSD only  
**Data:** free pinned `kevingtlin/Market-Data-Lab` XAUUSD BID M1  
**Source commit:** `922f83a60cc574e7395fb27397077288055a1ef6`

## Why this is a new family

EXP-045 / Engine S is closed after its prospectively frozen structural-target development test returned `ENGINE_S_FAIL_CLOSE_BEFORE_VALIDATION`.

Engine T is **not** a threshold change, density repair, branch rescue, or acceptance-only continuation variant of Engine S.

The decision-process hypothesis is different:

`established breakout acceptance -> later failed auction back inside -> boundary retest -> reversal`

The human-style information being tested is whether the market first establishes apparent acceptance beyond meaningful external liquidity, attracts/commits breakout participation, and then **fails that acceptance**. The reversal is considered only after that multi-bar failure has become causal and observable.

## Research-ordering rule

The first Engine-T run is zero-outcome only.

It may calculate:

- setup counts;
- terminal-state counts;
- filled-candidate counts;
- direction/level/day balance;
- timing geometry;
- structural-stop distance;
- causal-integrity assertions.

It must **not** calculate:

- target labels;
- MFE/MAE;
- win rate;
- post-entry path;
- R expectancy;
- dollar P&L;
- profit factor;
- drawdown;
- validation/holdout outcomes.

If the zero-outcome gate fails, Engine T v0.1 closes at preflight. Do not lower the gate after seeing density.

## Protected-data policy

Warm-up only:

- 2021-12-01 through 2021-12-31.

Zero-outcome development preflight:

- 2022-01-01 through 2025-02-28.

Protected and not loaded:

- validation: 2025-03-01 through 2025-08-31;
- fresh holdout: 2025-09-01 through 2026-02-28.

## Causal external-liquidity map

Use the same causal level classes already proven reproducible in EXP-045, because the **decision process** rather than the level source is the experimental change:

1. prior-day high / low;
2. Asia 00:00-06:00 UTC high / low;
3. 06:00-09:00 UTC opening-range high / low.

Knowledge times:

- prior-day levels: known at current UTC day start;
- Asia levels: known from 06:00 UTC;
- opening-range levels: known from 09:00 UTC.

A level is fresh until its first completed active-M5 attack. First attack consumes it whether or not a trade setup follows.

If one M5 bar attacks both a fresh high-side and low-side level, mark the event dual-sided ambiguous and create no setup.

When multiple same-side fresh levels are attacked on the same M5 bar, priority is:

1. prior-day;
2. Asia;
3. opening range.

## Setup window

A first attack may create Engine-T state only when its completed M5 close is:

- weekday;
- at or after 06:00 UTC;
- before 17:00 UTC;
- inside zero-outcome development.

All fills must occur before 18:00 UTC.

## State 1 — breakout attack

For a HIGH-side level:

- M5 high must trade strictly above the level;
- M5 close must finish strictly above the level.

For a LOW-side level:

- M5 low must trade strictly below the level;
- M5 close must finish strictly below the level.

An attack that immediately closes back inside is **not** Engine T. It is consumed and ignored rather than reclassified as Engine-S rejection.

## State 2 — established acceptance

The **next active M5 bar** after the breakout attack must also close beyond the same level in the breakout direction.

This second beyond-level close is the frozen definition of established acceptance.

If the next active M5 closes back inside or exactly on the level, terminate:

`ACCEPTANCE_CONFIRM_FAILED`.

No trade is created.

## State 3 — failed auction

After established acceptance, inspect at most the next **6 active M5 bars**.

The first qualifying failure bar must:

For a prior HIGH breakout:

- close strictly back below the level;
- be bearish (`close < open`);
- have body >= 50% of its full range.

For a prior LOW breakout:

- close strictly back above the level;
- be bullish (`close > open`);
- have body >= 50% of its full range.

If no qualifying failure occurs within 6 active M5 bars:

`FAILED_AUCTION_TIMEOUT_6`.

The structural excursion extreme is the furthest price beyond the level from the breakout attack through the qualifying failure bar inclusive.

## State 4 — non-chasing boundary retest entry

A failed HIGH auction creates a SHORT idea.

A failed LOW auction creates a LONG idea.

Entry is the exact attacked boundary price, only on a later active-M1 retest after the failure M5 close.

Entry window:

- maximum 15 active M1 bars after failure;
- fill must be before 18:00 UTC.

Structural stop:

- SHORT: one source tick above the failed-auction excursion high;
- LONG: one source tick below the failed-auction excursion low.

The entry is invalid unless stop is strictly beyond entry in the correct direction.

Gold structural-risk feasibility at the 0.10-lot anchor:

- one 0.001 source tick = USD0.01 at 0.10 lot;
- stop distance must be <= 4000 ticks, corresponding to <=USD40 gross structural stop at 0.10 lot.

No lot-sizing or profitability outcome is calculated in this preflight.

### Conservative pre-entry ordering

On any M1 after failure:

1. test structural-stop invalidation first;
2. only then test boundary-limit fill.

Therefore a bar that touches both stop and entry before an accepted fill is rejected as pre-entry invalidation.

## Zero-outcome adequacy gate

PASS requires all of:

- >=100 accepted filled candidates total;
- >=25 LONG;
- >=25 SHORT;
- >=50 distinct active signal days;
- median <=4 accepted candidates per active signal day;
- every accepted candidate passes causal ordering;
- validation/holdout not loaded;
- no target/P&L/post-entry outcome computation.

No target/path rule may be frozen or evaluated unless this gate passes naturally.

## Pre-committed branch

If PASS:

1. freeze Engine-T structural target and management prospectively;
2. only then calculate development outcomes;
3. validation remains sealed until the frozen development gate passes.

If FAIL:

- close Engine T v0.1;
- do not create a density-repair v0.2 by widening the 6-M5 failure window, 15-M1 retest window, body threshold, hours, level set, or risk cap after seeing the result;
- choose a genuinely different human-style process.
