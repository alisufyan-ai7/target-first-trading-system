# Engine M v0.5 — Recent-H1 Range Sweep/Reclaim Limit Entry

**Engine ID:** engine-m-mtf-reclaim-limit-entry  
**Version:** 0.5  
**Experiment:** EXP-031  
**Status:** FROZEN PROSPECTIVELY — ZERO V0.5 OUTCOMES — 2026-09-24

## 1. Purpose

Engine M v0.4 recovered opportunity density versus v0.3 but still failed its zero-outcome frequency gate:

- v0.3: 106 filled signals;
- v0.4: 237 filled signals;
- v0.4 requirement: >=300 total and >=25 per market;
- only GBPUSD missed the per-market count (19).

v0.5 does **not** lower the frozen opportunity-density gate after seeing those counts.

Instead it makes one prospective structural broadening:

> use the most recent qualifying completed H1 range among H1_0 and H1_1, with deterministic preference for H1_0.

Execution, target, costs, sizing and safety remain unchanged.

## 2. Markets and evidence

Execution markets unchanged:

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

Reusable development evidence: Mar23-Jun30 2026.

Protected:

- Jul-Aug secondary: unopened;
- Sep final holdout: unopened.

No v0.5 target/P&L outcome exists at freeze.

## 3. Higher-timeframe direction

Unchanged.

LONG context:

- H4_0.close > H4_1.close;
- H1_0.close > H1_1.close.

SHORT: mirror.

## 4. Candidate H1 range objects

At each completed M15 decision time, define:

- H1_0 = latest completed H1 bar;
- H1_1 = immediately preceding completed H1 bar.

Evaluate candidate range objects in this fixed order:

1. H1_0;
2. H1_1.

Use the **first** range object that satisfies the complete v0.5 setup + T40 room rules below.

If H1_0 qualifies, H1_1 is not considered.

This deterministic recency preference prevents duplicate setups or post-hoc choice.

## 5. M15 sweep/reclaim of candidate H1 range

For candidate H1_j:

LONG:

1. LONG context;
2. S15.low < H1_j.low;
3. S15.close > H1_j.low.

SHORT:

1. SHORT context;
2. S15.high > H1_j.high;
3. S15.close < H1_j.high.

Strict inequality is required.

No H1 midpoint rule.
No rolling PREV4-M15 rule.

## 6. M5 arm

Unchanged from v0.2-v0.4.

LONG:

- A5 close > open;
- A5 close > previous M5 close;
- A5 closes in upper 25%.

SHORT mirror.

## 7. Entry / stop / lifetime

Unchanged:

- LIMIT = 50% midpoint of A5;
- stop one research tick beyond A5 extreme;
- 10 active-M1 order life;
- no later than 18:00 UTC;
- conservative gap-through-stop and fill-bar stop-first semantics.

## 8. T40 target-room tied to selected H1 range

Using unchanged T40 geometry:

LONG:

- TARGET_PRICE <= selected H1_j.high.

SHORT:

- TARGET_PRICE >= selected H1_j.low.

The same H1 range that supplied the swept boundary must also supply the opposite target-room boundary.

No mixing H1_0 entry boundary with H1_1 destination or vice versa.

## 9. Signal-first deployability

Unchanged:

- every valid filled signal retained for strategy-edge research;
- safe lot under USD20 risk, USD50k notional, USD100 margin, 0.01 lot step;
- XAUUSD <=0.10 lot;
- report GE40 / GE30 / LT30.

## 10. Zero-outcome preflight

Before outcomes require:

1. H1_0/H1_1 recency-order unit tests;
2. no duplicate arm when both ranges qualify;
3. strict sweep/reclaim tests;
4. target room tied to same selected H1 range;
5. unchanged M5/limit/stop/lifetime tests;
6. safe overlay never violates caps;
7. each market >=25 filled valid signals;
8. both LONG and SHORT on every market;
9. >=300 total filled valid signals;
10. no target/P&L outcomes;
11. Jul-Aug and Sep remain unloaded.

The frequency gate is **unchanged from v0.4**.

## 11. Development gate if preflight passes

Same six frozen development slices and same v0.4 economic standard:

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

## 12. Anti-mining

Do not after outcomes change inside v0.5:

- H1_0 then H1_1 recency order;
- strict sweep/reclaim;
- same-range target room;
- M5 arm;
- 50% limit;
- T40;
- stop/lifetime;
- costs/safety caps.

Any redesign requires a new experiment.
