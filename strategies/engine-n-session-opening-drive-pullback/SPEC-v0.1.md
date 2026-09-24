# Engine N v0.1 — Session Opening Drive Pullback Continuation

**Engine ID:** engine-n-session-opening-drive-pullback  
**Version:** 0.1  
**Experiment:** EXP-032  
**Status:** FROZEN PROSPECTIVELY — ZERO OUTCOMES — 2026-09-24

## 1. Thesis

Engine M established that non-chasing retracement entry can improve execution quality, but its H1/midpoint/sweep-reclaim predictor was not robust enough.

Engine N is a genuinely different family.

It asks:

> When a major intraday session opens with a strong directional displacement relative to the immediately preceding volatility regime, does the first 50% pullback offer a repeatable continuation entry?

This is a session-opening continuation thesis, not an H1-liquidity-reclaim thesis.

## 2. Markets

Execution universe unchanged:

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

## 3. Source and protection

Use the same pinned minute data and source-integrity conventions already audited in the project.

Reusable development source:

- 2026-03-23 through 2026-06-30.

Protected:

- Jul-Aug secondary;
- Sep final holdout.

No protected data may be loaded during preflight/development.

## 4. Fixed session anchors

Two fixed UTC session anchors per eligible weekday:

- **London drive:** 07:00 UTC;
- **New York drive:** 13:30 UTC.

No DST adjustment is introduced inside v0.1.

Each candidate uses the first **30 exact clock minutes** beginning at the anchor:

- London: 07:00:00 through 07:29:59;
- New York: 13:30:00 through 13:59:59.

Decision time is anchor +30 minutes.

The 30 one-minute bars must all exist and be exactly contiguous. Otherwise reject `drive_30m_incomplete`.

## 5. Pre-drive volatility baseline

Use the eight exact contiguous UTC-aligned M15 bars immediately preceding the session anchor.

Their starts are:

`anchor-120m, anchor-105m, ..., anchor-15m`.

For each bar:

`R_i = high-low`.

Sort the eight ranges.

Exact baseline median:

`BASE_MEDIAN = (R_4 + R_5)/2`

using one-based sorted positions 4 and 5.

Require BASE_MEDIAN >0.

The 30-minute opening drive is excluded from the baseline.

## 6. Opening-drive qualification

Let:

- `O` = first M1 open at anchor;
- `H` = max high of the 30 drive minutes;
- `L` = min low;
- `C` = final M1 close before decision;
- `R = H-L`;
- `BODY = abs(C-O)`.

Require R>0.

### Expansion

`R >= 1.50 * BASE_MEDIAN`.

### Body strength

`BODY >= 0.60 * R`.

### LONG drive

- C > O;
- close in upper 25% of drive range:
  `H-C <= 0.25*R`.

### SHORT drive

- C < O;
- close in lower 25%:
  `C-L <= 0.25*R`.

No H4/H1 direction filter.
No H1 sweep/reclaim.
No ML probability gate.

## 7. Non-chasing pullback entry

For a qualified drive:

`LIMIT = (H+L)/2`.

LONG:

- limit must be below C;
- stop = L -1 research tick.

SHORT:

- limit must be above C;
- stop = H +1 research tick.

The limit becomes active at decision time (anchor +30m).

Order life:

- next **45 active M1 bars**;
- never later than anchor +90m.

If the market gaps through the stop before touching the limit, cancel the setup.

If the fill bar touches both entry and stop, preserve the existing conservative stop-first execution semantics at outcome stage.

At most one Engine-N setup per symbol per session anchor.

## 8. Target and safe-lot overlay

Target geometry is unchanged project T40:

- XAUUSD: fixed +/−4 XAU from entry;
- non-Gold: frozen v0.2 T40 geometry (approximately 2R).

Signal-first research ordering remains:

1. determine valid filled signal;
2. separately calculate maximum safe lot.

Safe-lot caps unchanged:

- stop risk <=USD20;
- notional <=USD50,000;
- margin <=USD100 at 1:500;
- 0.01 lot step;
- XAUUSD <=0.10 lot.

Report GE40 / GE30 / LT30.

## 9. Zero-outcome preflight

Before any target/P&L outcome require:

1. exact London and New York UTC anchors;
2. exact 30-minute drive chronology;
3. exact preceding eight M15 baseline bars;
4. drive excluded from baseline;
5. median-of-eight arithmetic tests;
6. 1.50x expansion boundary tests;
7. 60% body boundary tests;
8. outer-25% close tests;
9. 50% non-chasing limit tests;
10. 45-active-M1 expiry tests;
11. gap-through-stop cancellation tests;
12. safe overlay never violates account caps;
13. each market >=25 filled valid signals;
14. LONG and SHORT represented on every market;
15. >=300 total filled valid signals;
16. no target/P&L outcomes;
17. Jul-Aug and Sep remain unloaded.

The opportunity-density gate matches the recently frozen multi-market standard and is not to be relaxed after observing counts.

## 10. Development gate if preflight passes

Use the same six fixed development slices.

Report separately:

- London cohort;
- New York cohort;
- per market;
- per fold;
- pooled normalized-R edge;
- safe-lot USD500 portfolio;
- matched immediate-entry control at the first active M1 open after the 30m drive.

Mandatory:

1. >=120 pooled Engine-N signals;
2. every fold >=8;
3. pooled gross normalized expectancy > +0.20R;
4. pooled primary normalized expectancy >0;
5. pooled stress normalized expectancy >0;
6. >=4/6 positive-stress folds;
7. reference-account trades >=90;
8. >=35 distinct trade weekdays;
9. reference primary/stress expectancy >0;
10. primary PF >=1.10;
11. stress PF >=1.05;
12. stress MDD <=USD150;
13. no market >60% of executable trades;
14. integrity/provenance pass;
15. protected periods sealed.

## 11. Anti-mining

Do not after outcomes change inside v0.1:

- session anchors;
- 30-minute drive length;
- eight-M15 baseline;
- 1.50 expansion ratio;
- 60% body;
- outer 25% close;
- 50% pullback entry;
- 45-M1 order life;
- structural stop;
- T40;
- costs or safety caps.

Any redesign requires a new experiment.

## 12. Outcome state at freeze

At freeze:

- Engine-N target outcomes: NO;
- Engine-N P&L outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.
