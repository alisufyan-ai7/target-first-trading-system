# Engine M v0.3 — Liquidity Reclaim + HTF Target-Room Limit Entry

**Engine ID:** engine-m-mtf-reclaim-limit-entry  
**Version:** 0.3  
**Experiment:** EXP-029  
**Status:** FROZEN PROSPECTIVELY — ZERO V0.3 OUTCOMES — 2026-09-24

## 1. Purpose

Engine M v0.2 showed that the top-down, non-chasing limit architecture improved raw signal quality versus immediate entry:

- v0.2 gross normalized expectancy: +0.0367R/signal;
- matched immediate control: -0.0146R/signal.

But the edge was too weak to survive frozen costs.

v0.3 therefore changes **selectivity only**.

It does not change:

- markets;
- bar construction;
- 50% M5 retracement-limit entry;
- M5 structural stop;
- 10-active-M1 order life;
- T40 target geometry;
- signal-first research ordering;
- safe-lot overlay;
- account safety gates;
- cost assumptions.

The new thesis is:

> Trade only when the higher-timeframe direction is aligned, the 15m setup contains an actual local liquidity sweep/reclaim, and the frozen target points toward a recent completed H1 liquidity level rather than into empty/ambiguous space.

## 2. Evidence status

Reusable development evidence:

- Mar23-Jun30 2026;
- EXP-028 outcomes are inspected development evidence.

Protected:

- Jul1-Aug31 secondary test: unopened;
- Sep1-Sep22 final holdout: unopened.

v0.3 preflight may inspect only mechanics/frequency through Jun30 and may not calculate target/P&L outcomes.

## 3. Markets

Unchanged execution-research universe:

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

## 4. Higher-timeframe context

Use the same completed-bar H4/H1 directional alignment as v0.2.

LONG:

- latest completed H4 close > preceding completed H4 close;
- latest completed H1 close > preceding completed H1 close.

SHORT: mirror.

Neutral/disagreement => no setup.

No moving averages, probability model or parameter grid.

## 5. 15m liquidity sweep/reclaim

At a completed M15 decision bar `S15`, use the **four immediately preceding contiguous completed M15 bars** only.

Define:

- `PREV4_LOW = min(low)`;
- `PREV4_HIGH = max(high)`.

The four reference bars must be exactly contiguous 15-minute bars ending immediately before S15.

LONG setup requires:

1. LONG H4/H1 context;
2. `S15.low < PREV4_LOW`;
3. `S15.close > PREV4_LOW`;
4. `S15.close > H1_MID`, where H1_MID is the midpoint of the latest completed H1 bar.

SHORT mirror:

1. SHORT context;
2. `S15.high > PREV4_HIGH`;
3. `S15.close < PREV4_HIGH`;
4. `S15.close < H1_MID`.

This replaces v0.2's broad "touch H1 midpoint and close back across it" admission with a concrete local liquidity event.

Strict inequality is intentional: merely equal lows/highs do not count as a sweep.

## 6. 5m tactical arm

Unchanged from v0.2.

Let A5 be the completed M5 bar ending with S15 and P5 the immediately preceding contiguous M5 bar.

LONG arm:

- A5 close > open;
- A5 close > P5 close;
- A5 closes in upper 25% of its range.

SHORT: mirror.

A5 range must be >0.

## 7. Non-chasing limit entry and stop

Unchanged:

`LIMIT = (A5.high + A5.low) / 2`.

LONG stop:

`A5.low - 1 research tick`.

SHORT stop:

`A5.high + 1 research tick`.

The order lives for the next 10 active M1 bars, no later than 18:00 UTC.

No post-arm breakout confirmation. No chasing.

## 8. T40 target and recent-H1 liquidity destination

Use unchanged v0.2 T40 geometry from LIMIT + structural stop.

After LIMIT and STOP are known, compute the frozen T40 price:

LONG:

`TARGET_PRICE = LIMIT + T40_DISTANCE`.

SHORT:

`TARGET_PRICE = LIMIT - T40_DISTANCE`.

Use only the latest two completed H1 bars known at decision time.

LONG requires:

`max(H1_0.high, H1_1.high) >= TARGET_PRICE`.

SHORT requires:

`min(H1_0.low, H1_1.low) <= TARGET_PRICE`.

Interpretation:

the target must be no farther than a recent completed H1 liquidity extreme in the intended direction.

This is a **pre-entry structural destination gate**, not an outcome label.

No alternative H1 lookback, room ratio or target-distance variant is tested inside v0.3.

## 9. Signal-first deployability overlay

Unchanged from v0.2.

Every mechanically filled valid signal remains a strategy-research signal regardless of whether it can produce USD30-40 on the USD500 reference account.

Separately compute maximum safe lot under:

- stop risk <=USD20;
- notional <=USD50,000;
- margin <=USD100 at 1:500;
- 0.01 lot step;
- XAUUSD <=0.10 lot.

Report GE40 / GE30 / LT30.

## 10. Zero-outcome preflight

Before any v0.3 target/P&L outcome, verify:

1. H4/H1 causality unchanged and tests pass;
2. exact contiguous PREV4 M15 construction;
3. strict liquidity-sweep boundary tests;
4. H1-midpoint reclaim tests;
5. unchanged M5 arm tests;
6. target-destination gate uses only completed H1 bars;
7. 50% M5 limit remains favorable versus A5 close;
8. 10-M1 expiry / gap-through-stop / stop-first mechanics unchanged;
9. safe-lot overlay never violates safety caps;
10. each market has >=35 filled valid v0.3 signal paths;
11. each market has at least one LONG and one SHORT;
12. total filled valid signals >=400;
13. no target/P&L outcomes;
14. Jul-Aug and Sep remain unloaded.

Why >=400:

Across roughly the reusable development window this is enough to preserve a multi-market daily-opportunity stream while allowing v0.3 to be materially more selective than v0.2.

Fail preflight -> do not calculate outcomes.

## 11. Development design if preflight passes

Use the same six frozen chronological evaluation slices as EXP-028.

Report:

- context counts;
- liquidity-sweep counts;
- midpoint-reclaim counts;
- M5 arm counts;
- H1-target-destination passes/fails;
- fills;
- signal counts;
- normalized-R gross/primary/stress expectancy;
- per-market and per-fold results;
- safe-account USD portfolio;
- GE40/GE30/LT30 composition;
- matched v0.2-style control diagnostic.

### Matched selectivity control

For the same H4/H1 context and unchanged execution mechanics, report a diagnostic control that uses the old v0.2 broad midpoint-reclaim setup without the new PREV4 liquidity sweep + H1 target-destination filters.

This control is descriptive only and does not alter the frozen v0.3 gate.

## 12. Development gate

v0.3 passes only if all hold:

1. >=120 pooled v0.3 signal-layer trades;
2. every fold >=8 signals;
3. pooled gross normalized-R expectancy > **+0.20R**;
4. pooled primary normalized-R expectancy >0;
5. pooled stress normalized-R expectancy >0;
6. at least 4/6 folds positive stress normalized-R expectancy;
7. reference-account executable trades >=90;
8. >=35 distinct executable trade weekdays;
9. reference-account primary expectancy >0;
10. reference-account stress expectancy >0;
11. primary PF >=1.10;
12. stress PF >=1.05;
13. stress MDD <=USD150;
14. no market >60% of executable trades;
15. integrity/provenance pass;
16. Jul-Aug and Sep remain sealed.

The explicit +0.20R gross gate is prospectively added because v0.2's +0.0367R gross edge was demonstrably too small to survive the frozen cost model. v0.3 must create a **materially larger pre-cost edge**, not merely a statistical improvement.

## 13. Anti-mining

After outcomes do not change inside v0.3:

- PREV4 lookback;
- strict sweep inequalities;
- H1 midpoint reclaim;
- latest-two-H1 target destination;
- M5 arm;
- 50% limit;
- 10-M1 lifetime;
- stop;
- T40;
- cost assumptions;
- safety gates.

No threshold grid or symbol-specific exception.

Any redesign requires a new experiment.

## 14. Outcome state at freeze

At freeze:

- v0.3 target outcomes: NO;
- v0.3 P&L outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.
