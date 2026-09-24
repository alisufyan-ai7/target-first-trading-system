# Engine M v0.4 — Prior-H1 Range Sweep/Reclaim Limit Entry

**Engine ID:** engine-m-mtf-reclaim-limit-entry  
**Version:** 0.4  
**Experiment:** EXP-030  
**Status:** FROZEN PROSPECTIVELY — ZERO V0.4 OUTCOMES — 2026-09-24

## Purpose

Preserve the v0.2 non-chasing execution improvement while replacing v0.3's over-constrained location stack with one coherent H1 range object.

Architecture:

`H4/H1 direction -> M15 sweep/reclaim of latest completed H1 boundary -> unchanged M5 rejection arm -> unchanged 50% M5 limit -> unchanged structural stop`.

The frozen T40 target must fit before the **opposite boundary of that same completed H1 range**.

## Evidence status

Reusable development: Mar23-Jun30 2026.

Protected: Jul-Aug secondary and Sep final holdout remain unopened.

No v0.4 target/P&L outcome exists at freeze.

## Higher-timeframe context

Unchanged directional alignment:

LONG:
- H4_0.close > H4_1.close;
- H1_0.close > H1_1.close.

SHORT: mirror.

H1_0 is the latest completed H1 bar at the M15 decision timestamp.

## M15 H1-range sweep/reclaim

LONG setup:

1. LONG context;
2. S15.low < H1_0.low;
3. S15.close > H1_0.low.

SHORT:

1. SHORT context;
2. S15.high > H1_0.high;
3. S15.close < H1_0.high.

Strict sweep inequality is required.

No H1-midpoint condition.
No rolling PREV4-M15 condition.

## M5 arm

Unchanged from v0.2/v0.3:

LONG:
- A5 close > open;
- A5 close > previous M5 close;
- A5 closes in upper 25%.

SHORT mirror.

## Entry / stop / lifetime

Unchanged:

- limit = 50% midpoint of A5 range;
- stop one research tick beyond A5 extreme;
- order life 10 active M1 bars;
- no later than 18:00 UTC;
- conservative gap/stop-first handling.

## T40 target-room gate

After LIMIT and STOP determine unchanged T40 geometry:

LONG:
- target price <= H1_0.high.

SHORT:
- target price >= H1_0.low.

Thus the intended move is from a reclaimed H1 boundary toward the opposite side of the same completed H1 range.

No alternate room ratio or lookback.

## Signal-first safe-lot overlay

Unchanged from v0.2:

- retain every valid filled signal for strategy research;
- safe lot under USD20 risk, USD50k notional, USD100 margin, 0.01 lot step;
- XAUUSD capped at 0.10 lot;
- report GE40 / GE30 / LT30.

## Zero-outcome preflight

Before outcomes require:

1. exact H1-boundary sweep/reclaim tests;
2. strict equality does not count as sweep;
3. target-room uses only H1_0 known at decision time;
4. unchanged M5/limit/stop/lifetime tests pass;
5. safe overlay never violates caps;
6. each market >=25 filled valid signals;
7. both LONG and SHORT on every market;
8. >=300 total filled valid signals;
9. target/P&L outcomes remain zero;
10. Jul-Aug and Sep unloaded.

The >=300 total threshold corresponds to roughly three filled opportunities per eligible development weekday across the multi-market universe, consistent with the project's desired opportunity density without forcing trades.

## Development gate if preflight passes

Use the same six frozen development slices.

Mandatory:

1. >=120 pooled signals;
2. every fold >=8;
3. pooled gross normalized expectancy > +0.20R;
4. pooled primary normalized expectancy >0;
5. pooled stress normalized expectancy >0;
6. >=4/6 positive-stress folds;
7. reference-account trades >=90;
8. >=35 trade weekdays;
9. reference primary/stress expectancy >0;
10. primary PF >=1.10;
11. stress PF >=1.05;
12. stress MDD <=USD150;
13. no market >60%;
14. integrity/provenance pass;
15. protected periods sealed.

## Anti-mining

No post-outcome changes inside v0.4 to:

- H1 range object;
- strict sweep/reclaim;
- M5 arm;
- 50% limit;
- T40 room check;
- stop/lifetime;
- costs/safety caps.

Any redesign requires a new experiment.
