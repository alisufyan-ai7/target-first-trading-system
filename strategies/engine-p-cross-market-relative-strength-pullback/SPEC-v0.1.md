# Engine P v0.1 — Cross-Market Relative-Strength Pullback

**Engine ID:** engine-p-cross-market-relative-strength-pullback  
**Version:** 0.1  
**Experiment:** EXP-036  
**Status:** FROZEN PROSPECTIVELY — ZERO OUTCOMES — 2026-09-24

## 1. Thesis

Engines M, N and O all used primarily single-symbol information and failed to create robust pre-cost edge even when opportunity density was adequate.

Engine P changes the information source.

It asks:

> When a symbol has a meaningful 30-minute directional move **and the other markets sharing its currencies confirm the same factor direction**, does a non-chasing M5 pullback provide a repeatable target-first continuation entry?

This is a cross-market relative-strength / factor-consensus family.

No H1/H4 pattern filter.
No isolated-symbol statistical-reversion rule.
No session-opening rule.
No ML probability threshold.

## 2. Markets

Same eight execution-research markets:

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

## 3. Protected data

Reusable development source:

- 2026-03-23 through 2026-06-30.

Protected:

- Jul-Aug secondary;
- Sep final holdout.

No protected rows may be loaded in preflight/development.

## 4. Decision grid

Evaluate every completed UTC-aligned M5 bar with completion time:

`06:05, 06:10, ..., 17:55 UTC`.

No entry at or after 18:00 UTC.

One pending Engine-P order per symbol at a time. New same-symbol setup while pending is suppressed, not queued.

## 5. Per-symbol 30-minute normalized momentum

For candidate symbol S at decision time t:

Use the current completed M5 bar and the prior 24 contiguous completed M5 bars.

The current trigger bar is excluded from the volatility baseline.

Define:

- `REF_CLOSE` = close exactly six completed M5 bars before current trigger close;
- `MOVE_PCT = (TRIGGER_CLOSE - REF_CLOSE) / REF_CLOSE`;
- for each prior baseline bar i:
  `RANGE_PCT_i = (high_i-low_i)/close_i`;
- `VOL = even median(RANGE_PCT_i)` over the prior 24 bars;
- `MOM = MOVE_PCT / VOL`.

Require VOL >0.

Frozen own-momentum threshold:

`abs(MOM) >= 1.50`.

## 6. USD factor consensus

Use these six liquid USD-linked FX markets only:

- EURUSD
- GBPUSD
- AUDUSD
- USDJPY
- USDCAD
- USDCHF

For each at the same decision time calculate MOM identically.

Convert to a USD-strength contribution:

- EURUSD: `-MOM`;
- GBPUSD: `-MOM`;
- AUDUSD: `-MOM`;
- USDJPY: `+MOM`;
- USDCAD: `+MOM`;
- USDCHF: `+MOM`.

For a candidate that is one of those six, exclude its own contribution.

`USD_SCORE` = median of the remaining contributions.

Require at least four valid contributions.

Frozen factor threshold:

`abs(USD_SCORE) >= 0.50` in the required direction.

### BASE/USD candidates

EURUSD, GBPUSD, AUDUSD and XAUUSD:

LONG requires:

- own MOM >= +1.50;
- USD_SCORE <= -0.50.

SHORT requires:

- own MOM <= -1.50;
- USD_SCORE >= +0.50.

### USD/QUOTE candidates

USDJPY, USDCAD, USDCHF:

LONG requires:

- own MOM >= +1.50;
- USD_SCORE >= +0.50.

SHORT requires:

- own MOM <= -1.50;
- USD_SCORE <= -0.50.

## 7. EURJPY cross confirmation

EURJPY is handled from its two directly related USD legs.

LONG requires:

- EURJPY MOM >= +1.50;
- EURUSD MOM >= +0.50;
- USDJPY MOM >= +0.50.

SHORT requires:

- EURJPY MOM <= -1.50;
- EURUSD MOM <= -0.50;
- USDJPY MOM <= -0.50.

This is the identity-consistent direction because EURJPY ≈ EURUSD × USDJPY.

## 8. Local trigger-bar confirmation

After cross-market direction is determined, current M5 trigger bar must confirm it.

Let:

- `R = high-low`;
- `BODY = abs(close-open)`.

Require:

- R >0;
- BODY >=35% of R.

LONG:

- close > open;
- high-close <=40% of R.

SHORT:

- close < open;
- close-low <=40% of R.

## 9. Non-chasing entry

Frozen entry:

`LIMIT = (trigger high + trigger low)/2`.

LONG:

- LIMIT < trigger close;
- stop = trigger low -1 research tick.

SHORT:

- LIMIT > trigger close;
- stop = trigger high +1 research tick.

Order life:

- next 10 active M1 bars;
- hard expiry decision+30m;
- no entry at/after 18:00 UTC;
- gap through stop before limit cancels;
- conservative stop-first same-bar semantics at outcome stage.

## 10. Target and safe-lot overlay

Use unchanged project T40 geometry.

No post-hoc target switching.

Signal-first safe-lot overlay unchanged:

- stop risk <=USD20;
- notional <=USD50,000;
- margin <=USD100 at 1:500;
- 0.01 lot step;
- XAUUSD <=0.10 lot.

Report GE40 / GE30 / LT30.

## 11. Zero-outcome preflight

Before target/P&L outcomes require:

1. exact continuous M5 decision grid;
2. exact prior-24-M5 baseline and trigger exclusion;
3. exact 30-minute reference close;
4. even-median range-vol calculation;
5. own MOM 1.50 boundary tests;
6. USD contribution sign tests;
7. candidate-self exclusion from USD_SCORE;
8. USD_SCORE 0.50 boundary tests;
9. EURJPY two-leg confirmation tests;
10. trigger body/close-location tests;
11. 50% non-chasing entry tests;
12. pending-order suppression;
13. 10-active-M1 / 30m expiry and gap cancellation;
14. safe overlay caps;
15. each market >=25 filled valid signals;
16. LONG + SHORT every market;
17. >=300 total filled valid signals;
18. target/P&L outcomes zero;
19. Jul-Aug and Sep unloaded.

The opportunity-density gate is unchanged from recent scanner research.

## 12. Development gate if preflight passes

Use the same six frozen chronological slices and audited target-first portfolio framework.

Report:

- pooled normalized-R signal edge;
- per market;
- per fold;
- descriptive time-of-day cohorts;
- USD_SCORE / MOM distributions;
- safe-lot USD500 one-open portfolio;
- matched immediate-entry control on the same non-suppressed qualified arm.

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

## 13. Anti-mining

Do not after outcomes change inside v0.1:

- eight-market universe;
- continuous 06:05-17:55 M5 grid;
- 24-M5 VOL baseline;
- 30m MOM definition;
- own threshold 1.50;
- USD_SCORE definition or 0.50 threshold;
- EURJPY leg thresholds;
- 35% body;
- outer-40% close;
- 50% pullback;
- 10-M1 / 30m lifetime;
- stop;
- T40;
- costs or safety caps.

Any redesign requires a new experiment.

## 14. Outcome state at freeze

- target outcomes: NO;
- P&L outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.
