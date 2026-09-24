# Engine N v0.2 — Rolling Intraday Drive Pullback Scanner

**Engine ID:** engine-n-rolling-drive-pullback  
**Version:** 0.2  
**Experiment:** EXP-033  
**Status:** FROZEN PROSPECTIVELY — ZERO OUTCOMES — 2026-09-24

## 1. Purpose

Engine N v0.1 tested only two fixed session anchors per weekday and produced 123 filled signals, below the frozen opportunity-density gate.

No target or P&L outcome was inspected.

v0.2 keeps the same displacement-pullback thesis and qualification thresholds, but changes the sampling architecture from two session snapshots to continuous **non-overlapping hourly intraday scans**.

This directly implements the project requirement to keep scanning the multi-market universe rather than waiting for one named setup window.

## 2. Markets and protection

Same eight execution markets.

Reusable development source:

- 2026-03-23 through 2026-06-30.

Protected:

- Jul-Aug secondary;
- Sep final holdout.

No protected data may be loaded during preflight/development.

## 3. Fixed rolling anchors

For every eligible UTC weekday, evaluate these anchors:

`06:00, 07:00, 08:00, 09:00, 10:00, 11:00, 12:00, 13:00, 14:00, 15:00, 16:00, 17:00 UTC`.

Exactly 12 candidate anchors per market per weekday.

Each anchor uses:

- first 30 exact clock minutes = drive;
- decision at anchor+30m;
- pullback order horizon until anchor+90m.

Because anchors are one hour apart, the prior anchor's order horizon ends exactly when the next anchor decision occurs. This avoids overlapping pending Engine-N orders by construction.

No DST adjustment or symbol-specific anchor selection inside v0.2.

## 4. Baseline and drive qualification

Unchanged from v0.1:

- eight exact contiguous M15 bars immediately preceding anchor;
- median = average of sorted positions 4 and 5;
- baseline median >0;
- exact 30 M1 drive bars;
- drive range >=1.50x baseline median;
- body >=60% of drive range;
- LONG if close>open and closes in upper 25%;
- SHORT mirror in lower 25%.

No H1/H4 filter.
No ML threshold.

## 5. Non-chasing entry

Unchanged from v0.1:

- limit = 50% of drive range;
- LONG stop = drive low -1 research tick;
- SHORT stop = drive high +1 research tick;
- next 45 active M1 bars;
- hard horizon anchor+90m;
- gap-through-stop cancels;
- conservative fill-bar stop-first outcome semantics.

One arm maximum per symbol per anchor.

## 6. Target and sizing

Unchanged project T40 geometry.

Signal-first safe-lot overlay unchanged:

- risk <=USD20;
- notional <=USD50k;
- margin <=USD100 at 1:500;
- 0.01 lot step;
- XAUUSD <=0.10 lot;
- report GE40 / GE30 / LT30.

## 7. Zero-outcome preflight

Keep the same opportunity-density gate as v0.1:

1. exact 12 rolling anchors/day;
2. anchor chronology and non-overlap tests;
3. exact baseline/drive arithmetic;
4. qualification-boundary tests;
5. limit/expiry/gap tests;
6. safe overlay never violates caps;
7. each market >=25 filled valid signals;
8. both LONG and SHORT every market;
9. >=300 total filled valid signals;
10. no target/P&L outcomes;
11. Jul-Aug and Sep unloaded.

The gate is **not lowered** from v0.1.

## 8A. Development outcome convention

Frozen before any v0.2 outcome:

After a valid Engine-N pullback fill:

- target = unchanged project T40;
- stop = frozen drive-extreme stop;
- target-vs-stop on the same M1 bar = **stop first**;
- maximum outcome horizon = **120 active M1 bars counting the entry bar**;
- hard session cutoff = **20:00 UTC** on the entry date;
- timeout is marked to the final eligible M1 close.

Matched immediate-entry control:

- same qualified 30-minute drive;
- entry = first active M1 open at/after the 30-minute decision time;
- uses the same frozen drive-extreme stop;
- control is evaluated whether or not the later 50% pullback would fill;
- descriptive only; it does not alter Engine-N gate rules.

Hourly-anchor cohorts are descriptive diagnostics only. No post-outcome hour whitelist is allowed inside v0.2.

## 8. Development gate if preflight passes

Use the same six frozen chronological slices.

Report:

- hourly-anchor cohort;
- per market;
- per fold;
- pooled normalized-R edge;
- safe-lot USD500 portfolio;
- matched immediate-entry control at the first active M1 open after each 30m drive.

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

## 9. Anti-mining

Do not after outcomes change inside v0.2:

- 06:00-17:00 hourly anchor set;
- 30m drive;
- eight-M15 baseline;
- 1.50 expansion;
- 60% body;
- outer-25% close;
- 50% pullback;
- 45-M1 horizon;
- stop;
- T40;
- costs or safety caps.

Any redesign requires a new experiment.

## 10. Outcome state at freeze

- target outcomes: NO;
- P&L outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.
