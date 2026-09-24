# Engine O v0.1 — Rolling Statistical Stretch Reversion

**Engine ID:** engine-o-rolling-statistical-stretch-reversion  
**Version:** 0.1  
**Experiment:** EXP-034  
**Status:** FROZEN PROSPECTIVELY — ZERO OUTCOMES — 2026-09-24

## 1. Thesis

Engine N showed that continuously scanning the market solves opportunity density, but opening-drive continuation did not create robust edge.

Engine O is a genuinely different **mean-reversion** family.

It asks:

> When price becomes statistically stretched away from its recent intraday center and the current 5-minute bar rejects that extension, can a non-chasing entry capture reversion back toward the recent center?

No H1/H4 trend filter.
No session-opening continuation rule.
No post-hoc hour whitelist.
No ML probability threshold.

## 2. Markets and source protection

Same eight execution-research markets:

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

Reusable development source:

- 2026-03-23 through 2026-06-30.

Protected:

- Jul-Aug secondary;
- Sep final holdout.

No protected rows may be loaded during preflight/development.

## 3. Decision grid

Evaluate completed UTC-aligned M5 trigger bars whose **completion time** is every 15 minutes:

`06:15, 06:30, ..., 17:45 UTC`.

The trigger bar is the final completed M5 bar ending at the decision time.

No setup may enter at or after 18:00 UTC.

## 4. Rolling baseline

For each trigger bar T5, use the **24 immediately preceding contiguous completed M5 bars**, excluding T5.

This is exactly two hours of prior M5 state.

Require exact 5-minute contiguity.

For the 24 baseline bars compute:

- `CENTER = median(close)`;
- absolute close deviations `D_i = abs(close_i - CENTER)`;
- `MAD = median(D_i)`;
- `RANGE_MEDIAN = median(high_i-low_i)`.

For an even 24-value median, use the arithmetic mean of sorted one-based positions 12 and 13.

Require:

- MAD > 0;
- RANGE_MEDIAN > 0.

## 5. Statistical stretch

Frozen stretch threshold:

`abs(T5.close - CENTER) >= 2.50 * MAD`.

The trigger bar itself is excluded from CENTER/MAD.

## 6. Rejection bar

Let:

- `R = T5.high - T5.low`;
- `BODY = abs(T5.close - T5.open)`.

Require:

- R > 0;
- `R >= 1.25 * RANGE_MEDIAN`;
- `BODY >= 0.50 * R`.

### LONG reversion

All required:

1. `T5.close < CENTER`;
2. downside stretch threshold passed;
3. bullish trigger: `close > open`;
4. close in upper 35% of trigger range:
   `high-close <= 0.35*R`.

### SHORT reversion

Mirror:

1. `T5.close > CENTER`;
2. upside stretch threshold passed;
3. bearish trigger: `close < open`;
4. close in lower 35%:
   `close-low <= 0.35*R`.

## 7. Non-chasing entry

For a qualified trigger:

`LIMIT = (T5.high + T5.low)/2`.

LONG:

- LIMIT < trigger close;
- stop = T5.low -1 research tick.

SHORT:

- LIMIT > trigger close;
- stop = T5.high +1 research tick.

Order life:

- next **10 active M1 bars**;
- hard expiry decision+30 minutes;
- entry must be before 18:00 UTC;
- gap through stop before limit => cancel;
- conservative fill-bar stop-first semantics later at outcome stage.

A symbol may have only one pending Engine-O limit order at a time. A new qualified trigger while a prior order remains pending is suppressed, not queued.

## 8. Mean-reversion destination gate

Use unchanged project T40 geometry from LIMIT and STOP.

LONG requires:

`TARGET_PRICE <= CENTER`.

SHORT requires:

`TARGET_PRICE >= CENTER`.

Thus the frozen T40 target must fit before the recent statistical center. This is a causal pre-entry room check, not an outcome label.

## 9. Signal-first safe-lot overlay

Every valid filled Engine-O signal remains a strategy-research signal regardless of reference-account utility.

Separately calculate maximum safe lot under unchanged:

- stop risk <=USD20;
- notional <=USD50,000;
- margin <=USD100 at 1:500;
- 0.01 lot step;
- XAUUSD <=0.10 lot.

Report GE40 / GE30 / LT30.

## 10. Zero-outcome preflight

Before target/P&L outcomes require:

1. exact 15-minute decision grid tests;
2. exact contiguous 24xM5 baseline;
3. trigger excluded from baseline;
4. even-24 median arithmetic tests;
5. MAD arithmetic tests;
6. 2.50x stretch boundary tests;
7. 1.25x range-expansion boundary tests;
8. 50% body tests;
9. outer-35% rejection-close tests;
10. 50% non-chasing limit tests;
11. 10-active-M1 / 30-minute expiry tests;
12. gap-through-stop cancellation tests;
13. same-center T40 room tests;
14. safe overlay never violates caps;
15. each market >=25 filled valid signals;
16. LONG + SHORT on every market;
17. >=300 total filled valid signals;
18. no target/P&L outcomes;
19. Jul-Aug and Sep unloaded.

The opportunity-density gate is unchanged from recent scanner research.

## 11. Development gate if preflight passes

Use the same six frozen chronological slices and audited target-first outcome/portfolio framework.

Report:

- pooled signal edge;
- per market;
- per fold;
- 15-minute decision-time cohorts descriptively;
- safe-lot USD500 one-open portfolio;
- matched immediate-entry control using first active M1 open after the trigger decision.

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

## 12. Anti-mining

Do not after outcomes change inside v0.1:

- 15-minute decision grid;
- 24xM5 baseline;
- 2.50 MAD stretch;
- 1.25 range expansion;
- 50% body;
- outer-35% close;
- 50% pullback entry;
- 10-M1 / 30-minute lifetime;
- target-room-to-center gate;
- stop;
- T40;
- costs or safety caps.

Any redesign requires a new experiment.

## 13. Outcome state at freeze

- target outcomes: NO;
- P&L outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.
