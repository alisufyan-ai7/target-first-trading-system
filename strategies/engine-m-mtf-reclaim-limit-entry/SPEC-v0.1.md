# Engine M v0.1 — Multi-Timeframe Reclaim Limit Entry

**Engine ID:** engine-m-mtf-reclaim-limit-entry  
**Version:** 0.1  
**Experiment:** EXP-027  
**Status:** FROZEN PROSPECTIVELY — ZERO ENGINE-M OUTCOMES — 2026-09-24

## 1. Purpose

Engine M is a genuinely different family from Engine K/L.

It implements the top-down intraday workflow:

`4H/1H context -> 15m setup/location -> 5m tactical arm -> M1 limit execution`.

The design addresses two findings from EXP-026:

1. the previous M1 resumption confirmation chased price;
2. raw forecast probability did not monotonically separate profitable trades.

Engine M therefore uses **no ML probability model** in v0.1.

The entry price is fixed before the retrace occurs. If price does not return to that favorable price, there is no trade.

## 2. Evidence status

Reusable development evidence:

- Mar23-Jun30 2026.

Protected:

- Jul1-Aug31 secondary test: unopened;
- Sep1-Sep22 final holdout: unopened.

Engine M v0.1 preflight/development may not load or label Jul-Sep.

## 3. Markets

Execution-research universe:

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

Forecast-only markets remain excluded.

## 4. Bar construction

From the pinned M1 feed construct only complete UTC-aligned bars:

- M5: exactly 5 active one-minute rows;
- M15: exactly 15;
- H1: exactly 60;
- H4: exactly 240.

Incomplete bins around closures are excluded.

At any decision timestamp, only bars whose full interval has completed may be used.

## 5. 4H / 1H context — direction only

At a completed M15 decision timestamp, define:

- `H4_0` = latest completed H4 bar;
- `H4_1` = immediately preceding completed H4 bar;
- `H1_0` = latest completed H1 bar;
- `H1_1` = immediately preceding completed H1 bar.

LONG context requires:

- `H4_0.close > H4_1.close`;
- `H1_0.close > H1_1.close`.

SHORT context requires both mirror inequalities.

If H4 and H1 disagree or either pair is unavailable, context is neutral and no setup is armed.

No moving-average grid, no probability model and no daily-direction override are used.

## 6. 15m setup/location — reclaim of completed H1 midpoint

Let:

`H1_MID = (H1_0.high + H1_0.low) / 2`.

For a just-completed M15 bar `S15`:

LONG setup requires:

1. LONG higher-timeframe context;
2. `S15.low <= H1_MID`;
3. `S15.close > H1_MID`.

SHORT setup mirror:

1. SHORT context;
2. `S15.high >= H1_MID`;
3. `S15.close < H1_MID`.

This layer answers whether price pulled into a higher-timeframe intraday location and reclaimed it.

There is no setup if the M15 bar merely remains on one side of H1_MID without interacting with it.

## 7. 5m tactical arm — directional rejection, not entry

Let `A5` be the completed M5 bar ending at the same timestamp as `S15`; let `P5` be the immediately preceding complete M5 bar.

A5 range must be >0.

LONG arm requires:

1. LONG M15 setup;
2. `A5.close > A5.open`;
3. `A5.close > P5.close`;
4. close in upper 25% of A5 range:
   `4*(A5.high-A5.close) <= A5.high-A5.low`.

SHORT mirror:

1. SHORT M15 setup;
2. `A5.close < A5.open`;
3. `A5.close < P5.close`;
4. close in lower 25%:
   `4*(A5.close-A5.low) <= A5.high-A5.low`.

The arm does **not** cause an immediate market entry.

## 8. Precomputed non-chasing entry

At the instant A5 completes, place a conceptual limit order at exactly the midpoint of A5:

`LIMIT = (A5.high + A5.low) / 2`.

LONG:

- buy limit at LIMIT.

SHORT:

- sell limit at LIMIT.

Because the arm closes in its outer quartile, LIMIT is necessarily a retracement from the completed arm close.

The limit price is frozen before any subsequent M1 price path is inspected.

No post-arm breakout/resumption confirmation is required.

## 9. Structural stop

The trade stop is known at arm creation:

LONG:

`STOP = A5.low - 1 research tick`.

SHORT:

`STOP = A5.high + 1 research tick`.

The stop is never moved or compressed to satisfy the risk budget.

## 10. Limit-order lifetime and causal fill

Maximum one pending Engine-M order per symbol.

Order lifetime:

- next **10 active M1 bars** after the arm completes;
- expires no later than 18:00 UTC;
- no overnight carry.

While pending, later same-symbol setups are ignored.

Cancel if a feed gap between consecutive active M1 bars exceeds the existing 5-minute research gap limit.

### Long fill

On a post-arm M1 bar:

- if the bar opens at/below STOP, cancel as `gap_through_stop`;
- otherwise if `low <= LIMIT`, the order fills at LIMIT.

### Short mirror

- if bar opens at/above STOP, cancel as `gap_through_stop`;
- otherwise if `high >= LIMIT`, fill at LIMIT.

A limit order that gaps favorably through LIMIT is still recorded at LIMIT, not at a better price. This is conservative relative to true price improvement.

## 11. Fill-bar ambiguity

Because only M1 OHLC is available:

- if the fill bar also touches the structural stop, treat the trade as filled and stopped on the entry bar;
- if fill bar touches both stop and target, stop wins;
- no intrabar rescue is permitted.

This conservative rule prevents an optimistic limit-fill artifact.

## 12. Target and sizing

Engine M v0.1 uses T40 only.

Gold:

- target distance = 4.000 XAU from actual limit entry;
- 0.10 lot anchor, subject to all safety gates.

Non-Gold:

- target distance = 2.0R from actual limit entry to the frozen A5 stop;
- target defined before lot sizing;
- lot rounded downward toward approximately USD40 gross.

Economics remain:

- reference equity USD500;
- structural stop risk <=USD20;
- notional <=USD50,000;
- research margin <=USD100 at 1:500;
- primary cost = 10% actual gross target;
- stress cost = 20% actual gross target.

If T40 economics fail after limit entry + A5 stop are known, reject.

## 13. Cross-market portfolio

All eight markets scan continuously.

If multiple limit fills occur at the same M1 timestamp:

1. lower stop risk;
2. symbol;
3. LONG before SHORT.

Portfolio:

- maximum one open Engine-M trade;
- no queue;
- stop adding new risk after realized daily P&L <= -USD40;
- normally stop adding after realized daily P&L >= +USD150;
- no forced trades.

## 14. Matched immediate-entry control

Development must also report a matched control on the **same MTF arms**:

- enter at the first active M1 open after A5 completes;
- use the same A5 structural stop;
- use the same T40 economics.

Purpose:

isolate whether the precomputed retracement limit preserves enough price quality to improve economics versus taking the same top-down setup immediately.

The control is diagnostic only.

## 15. Zero-outcome mechanics preflight

Before any target/P&L outcome:

verify exact causal MTF construction and limit mechanics through Jun30 only.

Mandatory:

1. complete-bar H4/H1/M15/M5 construction tests pass;
2. HTF context mirror tests pass;
3. H1-midpoint reclaim tests pass;
4. M5 outer-quartile arm tests pass;
5. limit midpoint is always a favorable retracement from arm close;
6. 10-active-M1 expiry tests pass;
7. gap-through-stop cancellation tests pass;
8. fill-bar stop-first semantics test passes;
9. T40 economics use LIMIT + A5 stop;
10. each market has >=50 mechanically filled + economically admissible limit paths;
11. every market has at least one LONG and one SHORT admissible path;
12. total admissible paths >=600;
13. Jul-Aug and Sep remain unloaded.

Fail preflight -> correct mechanics before outcomes.

## 16. Development evaluation

If preflight passes, use the same six chronological forward evaluation slices as EXP-025/026.

Engine M itself has no fitted model, so each fold simply evaluates setups occurring in that fold's forward interval.

Report per fold and pooled:

- context counts long/short/neutral;
- M15 reclaim setups;
- M5 arms;
- pending orders;
- fills;
- expiries/cancellations;
- economically admitted entries;
- wait-to-fill;
- favorable entry improvement versus A5 close in native units and A5-range units;
- A5 stop distance;
- hit rate;
- primary/stress expectancy;
- PF;
- P&L;
- drawdown;
- daily P&L;
- market contribution;
- matched immediate-control metrics.

## 17. Frozen development gate

Engine M passes only if all hold:

1. >=90 pooled actual portfolio trades;
2. every fold >=6 trades;
3. >=35 distinct trade weekdays;
4. pooled primary expectancy >0;
5. pooled stress expectancy >0;
6. primary PF >=1.10;
7. stress PF >=1.05;
8. hit rate > mean stress break-even probability;
9. at least 4/6 folds positive stress expectancy;
10. stress max drawdown <=USD150;
11. no market >60% pooled trades;
12. Engine-M stress expectancy exceeds matched immediate control by >=USD2/trade;
13. Engine-M stress expectancy beats control in >=4/6 folds;
14. integrity/provenance/same-bar checks pass;
15. Jul-Aug and Sep remain unopened.

Fail any -> stop before secondary.

## 18. Anti-mining

After outcomes do not change inside v0.1:

- H4/H1 direction rule;
- H1 midpoint location;
- M15 reclaim rule;
- M5 arm rule;
- 50% A5 limit;
- 10-M1 order life;
- A5 stop;
- T40;
- risk/cost assumptions.

Any redesign requires a new experiment.

## 19. Outcome status at freeze

At freeze:

- Engine-M target/P&L outcomes: **NO**;
- matched-control outcomes: **NO**;
- Jul-Aug: unopened;
- Sep: unopened.
