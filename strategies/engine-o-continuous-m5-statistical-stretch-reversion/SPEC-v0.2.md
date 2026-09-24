# Engine O v0.2 — Continuous M5 Statistical Stretch Reversion

**Engine ID:** engine-o-continuous-m5-statistical-stretch-reversion  
**Version:** 0.2  
**Experiment:** EXP-035  
**Status:** FROZEN PROSPECTIVELY — ZERO OUTCOMES — 2026-09-24

## 1. Purpose

Engine O v0.1 produced 209 filled signals with zero target/P&L inspection.

Six of eight markets passed the per-market opportunity gate, but the 15-minute sampling grid missed the frozen >=300 total requirement.

v0.2 preserves the complete statistical-reversion thesis and changes **only sampling frequency**:

> evaluate every completed M5 trigger bar across the active intraday window.

No threshold, target, stop, cost, sizing or market-selection parameter changes.

## 2. Markets / data protection

Same eight execution markets.

Reusable source:

- 2026-03-23 through 2026-06-30.

Protected:

- Jul-Aug secondary;
- Sep final holdout.

## 3. Continuous M5 decision grid

Evaluate every completed UTC-aligned M5 trigger bar whose completion time is:

`06:05, 06:10, 06:15, ..., 17:55 UTC`.

Exactly one decision every five clock minutes.

No entry may occur at or after 18:00 UTC.

A symbol may have only one pending Engine-O limit order at a time. A qualified setup while an earlier Engine-O order remains pending is suppressed, not queued.

## 4. Rolling baseline

Unchanged from v0.1:

- prior 24 contiguous completed M5 bars;
- trigger excluded;
- CENTER = even median close;
- MAD = even median absolute close deviation from CENTER;
- RANGE_MEDIAN = even median M5 range;
- MAD >0;
- RANGE_MEDIAN >0.

## 5. Statistical stretch and rejection

Unchanged:

- abs(trigger close - CENTER) >= 2.50 * MAD;
- trigger range >=1.25 * RANGE_MEDIAN;
- body >=50% of trigger range.

LONG:

- trigger close < CENTER;
- bullish trigger;
- close in upper 35%.

SHORT mirror:

- trigger close > CENTER;
- bearish trigger;
- close in lower 35%.

## 6. Entry / stop / room

Unchanged:

- LIMIT = trigger 50% midpoint;
- stop one research tick beyond trigger extreme;
- 10 active-M1 order life;
- hard expiry decision+30m and no later than 18:00 UTC;
- gap through stop cancels;
- T40 must fit before CENTER;
- conservative stop-first semantics later at outcome stage.

## 7. Safe-lot overlay

Unchanged:

- stop risk <=USD20;
- notional <=USD50,000;
- margin <=USD100 at 1:500;
- 0.01 lot step;
- XAUUSD <=0.10 lot;
- report GE40 / GE30 / LT30.

## 8. Zero-outcome preflight

Keep the **same** scanner opportunity-density gate:

1. exact five-minute decision-grid tests;
2. exact 24xM5 baseline / trigger exclusion tests;
3. all v0.1 threshold and mirror tests;
4. pending-order suppression tests;
5. entry/expiry/gap/center-room tests;
6. safe overlay cap tests;
7. each market >=25 filled valid signals;
8. LONG + SHORT every market;
9. >=300 total filled valid signals;
10. target/P&L outcomes zero;
11. Jul-Aug / Sep unloaded.

The gate is unchanged from v0.1.

## 9. Development gate if preflight passes

Same six fixed chronological slices and audited target-first portfolio framework.

Report:

- pooled normalized-R edge;
- per-market diagnostics;
- per-fold diagnostics;
- time-of-day diagnostics descriptively only;
- safe-lot USD500 one-open portfolio;
- matched immediate-entry control.

Mandatory:

1. >=120 pooled signals;
2. every fold >=8;
3. pooled gross normalized expectancy >+0.20R;
4. pooled primary normalized expectancy >0;
5. pooled stress normalized expectancy >0;
6. >=4/6 positive-stress folds;
7. reference-account trades >=90;
8. >=35 distinct trade weekdays;
9. reference primary/stress expectancy >0;
10. primary PF >=1.10;
11. stress PF >=1.05;
12. stress MDD <=USD150;
13. no market >60%;
14. integrity/provenance pass;
15. protected periods sealed.

## 10. Anti-mining

Do not after outcomes change inside v0.2:

- continuous 06:05-17:55 M5 grid;
- 24xM5 baseline;
- 2.50 MAD stretch;
- 1.25 range expansion;
- 50% body;
- outer-35% close;
- 50% limit;
- 10-M1 / 30m lifetime;
- center-room T40;
- stop;
- costs/safety.

Any redesign requires a new experiment.

## 11. Outcome state at freeze

- target outcomes: NO;
- P&L outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.
