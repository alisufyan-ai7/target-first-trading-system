# Engine L v0.1 — Forecast-Armed Micro Pullback Entry

**Engine ID:** engine-l-forecast-armed-micro-entry  
**Version:** 0.1  
**Experiment:** EXP-026  
**Status:** FROZEN PROSPECTIVELY BEFORE ENGINE-L OUTCOMES — 2026-09-24

## 1. Purpose

Engine K established that multi-market state ranking contains non-random directional information, but its execution assumption was weak:

- complete a 5m state;
- enter almost immediately at the next active M1 open;
- use an older confirmed 5m pivot as the execution stop.

Engine L tests a different architecture:

`5m directional forecast -> arm one side -> wait for a favorable M1 pullback -> require M1 resumption confirmation -> enter next M1 open -> use fresh pullback structure as stop`.

The research question is whether **entry quality**, rather than more probability-threshold tuning, is the missing layer.

## 2. Evidence status

Development-only pool:

- Mar23-Jun30 2026 is reusable inspected development evidence.

Protected:

- Jul1-Aug31 2026 remains sealed;
- Sep1-Sep22 2026 remains sealed.

Engine L v0.1 may not load/label Jul-Sep.

## 3. Markets

Execution-research universe unchanged:

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

Forecast-only markets remain excluded.

## 4. Forecast layer

Engine L uses one fixed development forecast configuration only. There is no model grid.

Per market, every completed causal 5m state is scored in both directions when valid.

Forecast model:

- target rung used for directional learning: **T40 only**;
- HistGradientBoostingClassifier;
- learning_rate=0.035;
- max_iter=180;
- max_leaf_nodes=7;
- min_samples_leaf=250;
- l2_regularization=3.0;
- random_state=20260923.

These are the previously defined regularized M2 parameters.

No probability calibration is used for entry arming in v0.1.

At a decision timestamp for a symbol:

- score LONG and SHORT using information known at decision time;
- arm the direction with the higher raw T40 probability;
- no absolute probability threshold;
- if only one side has valid causal state geometry, that side may be armed;
- if neither side is valid, no arm.

### Direction tie-break

If LONG and SHORT raw T40 probabilities are exactly equal:

1. lower old-reference stop risk;
2. LONG before SHORT.

This tie-break is deterministic and frozen before outcomes.

Raw probability is used only to rank simultaneous entry triggers; it is not itself an entry trigger.

### Forecastable side domain

To isolate **entry quality** rather than simultaneously change candidate admission, the v0.1 forecast model and arm population use the same pre-probability T40 domain as the Engine-K v0.2/v0.3 model:

- complete 29-feature T40 state;
- old next-active-M1-open reference entry;
- old confirmed 5m-pivot stop;
- v0.2 pre-probability T40 economic admission passes.

This old entry/stop geometry is used only to define the forecast/control domain.

After an arm is created, the Engine-L trade itself ignores the old execution geometry except that the old pivot remains the pre-entry invalidation boundary. Engine-L economics are recomputed from the later micro-entry and fresh M1 stop.

Thus EXP-026 compares entry methods on the **same forecastable decisions** rather than giving Engine L a larger candidate universe.

## 5. Arm lifecycle

Maximum one pending arm per symbol.

When no arm is pending:

- a completed 5m decision may create an arm.

An arm:

- begins at the completed 5m decision time;
- is valid for the next **15 active M1 bars**;
- expires no later than 20:00 UTC;
- is cancelled if its pre-entry structural invalidation is breached;
- is cancelled if the market data/session cannot support a causal next-open fill;
- while an arm is pending, later 5m decisions for that symbol do not replace it.

After expiry/cancellation/entry, the next completed 5m decision may create a fresh arm.

This prevents overlapping same-symbol forecast spam.

### Arm resolution time

For enforcing one pending arm per symbol, an arm resolves causally at the first of:

- invalidation/cancellation timestamp;
- actual Engine-L entry timestamp;
- expiry after the 15th active M1 bar;
- 20:00 UTC session cutoff.

A later completed 5m decision may create a fresh arm only when its decision time is at or after the prior arm's resolved timestamp.

## 6. Required favorable pullback

Let:

- `C0` = completed 5m decision close;
- `V5` = causal median true range of the latest 20 complete 5m bars.

LONG arm requires, before entry:

- price trades to at least `C0 - 0.20*V5`;
- the old causal 5m structural invalidation is not breached.

SHORT mirror:

- price trades to at least `C0 + 0.20*V5`;
- structural invalidation not breached.

The 0.20*V5 pullback requirement is one prospectively frozen center value. No depth grid is permitted in EXP-026.

## 7. M1 resumption confirmation

After the required pullback has occurred, wait for a completed M1 resumption bar.

LONG resumption bar:

1. close > previous active M1 high;
2. close > open;
3. bar range >0;
4. close lies in the upper 25% of its own range:
   `4*(high-close) <= high-low`.

SHORT mirror:

1. close < previous active M1 low;
2. close < open;
3. range >0;
4. close lies in the lower 25%:
   `4*(close-low) <= high-low`.

Entry:

- exact next active M1 open after the resumption bar completes;
- entry must still occur inside the 15-active-M1 arm lifetime;
- entry must not jump more than 5 chronological minutes across a feed/session gap.

No intrabar breakout fill is assumed.

## 8. Fresh execution stop

The execution stop is no longer the older 5m pivot.

LONG:

- lowest M1 low from arm start through the completed resumption bar minus one research tick.

SHORT:

- highest M1 high over the same interval plus one research tick.

The old 5m pivot is only an **arm invalidation boundary before entry**.

The fresh M1 pullback extreme is the actual trade stop.

The stop is never shrunk after entry to meet a dollar budget.

## 9. Target and sizing — one center objective

Engine L v0.1 uses **T40 only** to isolate entry quality.

Gold:

- target distance = +4.000 / -4.000 XAU from actual entry;
- 0.10 lot anchor subject to risk feasibility.

Non-Gold:

- target distance = **2.0R** from the fresh M1 execution stop;
- target is defined before size;
- size is rounded down toward approximately USD40 gross.

Economics:

- reference equity USD500;
- structural stop risk <=USD20;
- notional <=USD50,000;
- research margin <=USD100 at 1:500;
- primary round-trip cost = 10% actual gross target;
- stress cost = 20% actual gross target.

If the new entry/stop cannot support safe T40 economics, reject.

No T30/T50 ladder in v0.1.

## 10. Trade exit

After actual entry:

- target-first versus fresh execution stop;
- entry M1 counts as active minute 1;
- max 120 active M1 bars;
- 20:00 UTC same-date cutoff;
- stop wins same-bar stop+target ambiguity;
- no overnight carry.

## 11. Cross-market execution

All eight markets continue to scan.

If multiple armed markets trigger an entry at the same M1 timestamp:

1. higher raw forecast probability;
2. lower stop risk;
3. symbol;
4. direction.

Portfolio:

- maximum one open Engine-L trade;
- no forced trade;
- stop adding new risk after realized daily P&L <= -USD40;
- normally stop adding after realized daily P&L >= +USD150.

## 12. Immediate-entry control

EXP-026 must evaluate a matched **control** using the same forecast arms:

- enter at the first eligible M1 open immediately after arm creation;
- use the old causal 5m pivot stop;
- T40 target/economics under the same rules.

The control is diagnostic only and cannot be promoted.

Purpose:

determine whether the new pullback/resumption entry layer materially improves entry economics versus the old Engine-K-style immediate entry on the **same forecast decisions**.

## 13. Development evaluation

Use the same six chronological walk-forward evaluation folds already frozen for EXP-025.

For each fold:

- train the fixed T40 M2 forecast model only on the fold fit window;
- evaluate both Engine-L entry and matched immediate control on the fold evaluation window;
- calibration window is not needed for v0.1 raw-score arming and remains unused by the forecast model;
- all evaluation decisions are strictly forward of fit data.

No model/configuration selection occurs.

## 14. Mandatory reporting

Per fold and pooled:

- forecast arms;
- arms with required pullback;
- arms with M1 resumption;
- expired/cancelled arms and reasons;
- actual entries;
- median wait-to-entry;
- entry improvement versus decision close in native units and V5 units;
- old-pivot stop distance versus fresh stop distance;
- T40 target hit rate;
- primary/stress expectancy;
- primary/stress PF;
- primary/stress net P&L;
- max drawdown;
- market trade counts;
- daily P&L including zero-trade weekdays;
- immediate-entry control metrics on matched forecast arms.

## 15. Zero-outcome entry-mechanics preflight

Before any Engine-L target/P&L outcome is calculated, run a mechanics-only preflight through Jun30.

For every market and direction independently, verify the causal arm/pullback/resumption/fresh-stop path without using future target labels.

Mandatory preflight gates:

1. all eight markets parse only through Jun30;
2. no Jul-Aug/Sep data loaded;
3. exact 0.20*V5 pullback boundary tests pass;
4. 15-active-M1 expiry tests pass;
5. pre-entry old-pivot invalidation tests pass;
6. resumption-bar mirror tests pass;
7. next-open gap tests pass;
8. fresh-stop geometry tests pass;
9. T40 economics use the fresh stop;
10. each market has >=100 mechanically triggerable + economically admissible T40 entry paths across both directions through Jun30;
11. each market has at least one long and one short admissible trigger.

If preflight fails, correct mechanics before outcomes.

## 16. Engine-L development gate

Engine L passes development only if **all** hold across the six forward folds:

1. pooled actual trades >=90;
2. every fold has >=6 actual trades;
3. >=35 distinct trade weekdays;
4. pooled primary expectancy >0;
5. pooled stress expectancy >0;
6. primary PF >=1.10;
7. stress PF >=1.05;
8. pooled target-hit rate > pooled mean stress break-even probability;
9. at least 4/6 folds have positive stress expectancy;
10. pooled stress max drawdown <=USD150;
11. no market >60% of trades;
12. Engine-L pooled stress expectancy exceeds matched immediate-entry control by **at least USD2/trade**;
13. Engine-L stress expectancy is better than control in at least 4/6 folds;
14. causality/provenance/same-bar integrity passes;
15. Jul-Aug and Sep remain unopened.

Fail any -> stop before secondary.

## 17. Anti-mining

Do not after EXP-026 outcomes:

- change 0.20*V5 pullback depth;
- change 15-M1 arm life;
- change M1 resumption rule;
- change T40;
- add T30/T50;
- change fresh-stop definition;
- change M2 forecast parameters;
- add probability thresholds;
- open Jul-Aug after a failed development gate.

A redesign requires a new experiment.

## 18. Outcome status at freeze

At freeze:

- Engine-L outcomes calculated: NO;
- immediate-control outcomes calculated under EXP-026: NO;
- Jul-Aug inspected: NO;
- Sep inspected: NO.
