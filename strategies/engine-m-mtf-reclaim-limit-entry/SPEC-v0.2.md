# Engine M v0.2 — Signal-First MTF Reclaim Limit Entry

**Engine ID:** engine-m-mtf-reclaim-limit-entry  
**Version:** 0.2  
**Experiment:** EXP-028  
**Status:** FROZEN PROSPECTIVELY — ZERO V0.2 OUTCOMES — 2026-09-24

## 1. Why v0.2 exists

Engine M v0.1 zero-outcome preflight produced:

- 1,581 mechanical retracement-limit fills;
- only 126 fills admitted by the USD40-equivalent account-sizing gates;
- XAUUSD 61 admissible;
- seven FX markets mostly rejected by the duplicated notional/margin envelope.

The rejection audit showed that rejected FX fills generally had stop risk already near the intended USD20 level, while USD40-equivalent lot sizing created excessive notional/margin.

Example median rejected economics:

- EURUSD: stop risk ~USD19.69, notional ~USD149k, margin ~USD298;
- GBPUSD: ~USD19.60, ~USD129k, ~USD258;
- USDJPY: ~USD19.88, ~USD190k, ~USD380;
- EURJPY: ~USD19.86, ~USD145k, ~USD290;
- AUDUSD: ~USD19.95, ~USD93k, ~USD186;
- USDCAD: ~USD19.76, ~USD177k, ~USD354;
- USDCHF: ~USD19.92, ~USD119k, ~USD238.

Under the frozen 1:500 research reference, the USD100 margin cap implies the same USD50k notional ceiling. Those two gates are therefore intentionally redundant expressions of the same effective-leverage envelope.

The methodological error was applying the USD30/40/50 deployment objective as a prerequisite for **strategy-signal validation**.

The project architecture is:

`validated strategy candidate -> sizing -> risk/margin/notional gates -> portfolio ranking/execution`.

Engine M v0.2 restores that order.

## 2. Strategy mechanics unchanged

All Engine M v0.1 trading mechanics remain unchanged:

- 8 execution markets;
- complete UTC H4/H1/M15/M5 bars;
- H4 + H1 aligned close-direction context;
- M15 interaction with and reclaim of latest completed H1 midpoint;
- final M5 directional rejection / outer-quartile close;
- precomputed entry at 50% of completed M5 arm range;
- stop one research tick beyond M5 arm extreme;
- 10 active-M1 order life;
- no later than 18:00 UTC;
- conservative gap-through-stop / fill-bar stop-first semantics;
- T40 geometry only;
- no ML probability model.

No setup, entry, stop or target parameter is changed in v0.2.

## 3. Signal layer versus deployability layer

### Signal layer

A filled Engine-M setup is a research signal if:

- causal MTF setup/arm passed;
- precomputed limit filled;
- valid entry/stop geometry exists;
- T40 target geometry exists.

It is **not rejected merely because USD40-equivalent sizing would exceed the USD500-account deployment envelope**.

### Deployability overlay

For every signal, independently calculate the largest safe research lot under the existing frozen account gates:

- structural stop risk <=USD20;
- notional <=USD50,000;
- margin <=USD100 at 1:500;
- legal research lot step 0.01.

Do not loosen those gates.

Let:

- `L_risk = 20 / stop_loss_per_1lot`;
- `L_notional = 50000 / notional_per_1lot`;
- `L_margin = 100*500 / notional_per_1lot`.

`L_safe_raw = min(L_risk, L_notional, L_margin)`.

Round **down** to the 0.01 research lot step.

If rounded safe lot <0.01, signal is non-deployable at the reference account.

Otherwise report:

- safe lot;
- stop risk;
- notional;
- margin;
- achievable gross target USD;
- primary/stress research costs;
- economic utility band:
  - `GE40`: gross target >=USD40;
  - `GE30`: >=USD30 and <USD40;
  - `LT30`: <USD30.

A signal may be statistically valid even if its reference-account utility is LT30. Such a signal cannot be promoted as a normal USD30–50 opportunity without a separate sizing/account solution.

## 4. Size-invariant signal economics

For strategy validation, report returns in structural-risk units as well as safe-account USD.

Let:

`R = abs(entry-stop)`.

Reward multiple:

- non-Gold: approximately 2R by frozen T40 construction;
- Gold: `4 XAU / R`.

Gross normalized outcome:

- target hit: `+reward_multiple R`;
- stop: `-1R`;
- timeout/session exit: mark-to-market normalized by initial R.

Because research cost is frozen as a fraction of gross target, normalized costs are size-invariant:

- primary cost = 10% of target reward multiple;
- stress cost = 20% of target reward multiple.

Thus strategy edge can be evaluated without forcing every signal to manufacture USD40 gross on a USD500 account.

## 5. v0.2 zero-outcome preflight

Before any target/P&L outcome:

1. all Engine-M v0.1 causality/unit tests pass;
2. every execution market has >=50 mechanically filled valid-geometry signals;
3. LONG and SHORT represented on every market;
4. >=600 total signals;
5. every signal receives a safe-lot/deployability annotation;
6. safe lot never violates USD20 risk, USD50k notional or USD100 margin;
7. utility-band counts are reported per market;
8. target/P&L outcomes remain zero;
9. Jul-Aug and Sep remain unloaded.

This preflight no longer requires every signal to be USD40-equivalent deployable.

## 6. Development portfolio if preflight passes

Use the same six chronological development evaluation slices.

Every filled valid signal is eligible for **signal-edge reporting**.

For the reference-account portfolio:

- only signals with safe lot >=0.01 are executable;
- simultaneous fills rank by:
  1. highest achievable gross target USD;
  2. lower stop risk USD;
  3. symbol;
  4. LONG before SHORT;
- one open Engine-M position;
- same daily stop-adding-risk rules.

Report both:

### Signal-edge metrics
- target hit rate;
- gross normalized R expectancy;
- primary normalized R expectancy;
- stress normalized R expectancy;
- per-market results;
- fold stability.

### Reference-account metrics
- actual one-open trades;
- GE40 / GE30 / LT30 trade counts;
- primary/stress USD expectancy;
- PF;
- daily P&L;
- MDD;
- percentage of days reaching USD100 / USD150;
- market contribution.

## 7. Development gate

No July-Aug access unless both **edge** and **deployability** are adequate.

Mandatory:

1. >=120 pooled signal-layer trades;
2. every fold >=8 signals;
3. pooled primary normalized-R expectancy >0;
4. pooled stress normalized-R expectancy >0;
5. at least 4/6 folds positive stress normalized-R expectancy;
6. reference-account executable trades >=90;
7. >=35 distinct executable trade weekdays;
8. reference-account primary USD expectancy >0;
9. reference-account stress USD expectancy >0;
10. primary PF >=1.10;
11. stress PF >=1.05;
12. stress MDD <=USD150;
13. no market >60% of executable trades;
14. integrity/provenance pass;
15. Jul-Aug and Sep sealed.

The daily USD150–200 goal remains an opportunity-dependent portfolio objective, not a gate requiring forced trades.

## 8. Matched immediate-entry control

Same MTF arms and same signal/deployability separation.

Control:

- immediate next-active-M1-open entry;
- same M5 structural stop;
- same T40 target geometry;
- safe-lot overlay calculated from control entry/stop.

Report control diagnostics, but Engine M v0.2 promotion is based on the frozen development gate above.

## 9. Anti-mining

Do not after outcomes:

- loosen account safety gates;
- change H4/H1/M15/M5 rules;
- change 50% limit;
- change stop;
- change T40;
- change order life;
- exclude low-utility signals from signal-edge reporting merely because their USD target is small.

Any redesign requires a new experiment.

## 10. Outcome state at freeze

At freeze:

- v0.2 signal outcomes: NO;
- v0.2 safe-account P&L outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.
