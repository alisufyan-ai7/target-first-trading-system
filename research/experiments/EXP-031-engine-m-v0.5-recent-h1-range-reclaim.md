# EXP-031 — Engine M v0.5 Recent-H1 Range Sweep/Reclaim

**Status:** CLOSED — DEVELOPMENT GATE FAILED; SECONDARY SEALED  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-m-mtf-reclaim-limit-entry/SPEC-v0.5.md`

## Purpose

Increase opportunity density without weakening the v0.4 frequency gate or changing the non-chasing execution architecture.

## Frozen change

At each M15 decision:

- test H1_0 range first;
- if it does not fully qualify, test H1_1;
- first qualifying range supplies both swept boundary and opposite target-room boundary;
- never create two setups from one M15 bar.

Everything else unchanged from v0.4.

## Zero-outcome preflight

Keep the **same** frozen v0.4 gate:

- >=25 filled valid signals per market;
- both directions every market;
- >=300 total;
- safety caps intact;
- no target/P&L outcomes;
- Jul-Aug/Sep sealed.

## Outcome state

- v0.5 outcomes: none;
- Jul-Aug: unopened;
- Sep: unopened.

## Next

Implement and run zero-outcome preflight only.


## Preflight attempt 1 — verification implementation failure

**Workflow run:** `36009869842`  
**Trigger SHA:** `6df0eb309b60d43a429d26c2bd752ec887f9d656`

The workflow failed in the deterministic verification step before the market preflight ran.

Root cause:

- the v0.5 helper returned an M5 geometry dictionary containing `status="ok"`;
- the qualifying return path set `status="armed"` **before** unpacking that helper dictionary;
- Python therefore overwrote `armed` with `ok`;
- the non-qualifying path had the same collision and could overwrite `no_recent_h1_range_qualified` with `ok`.

This was an implementation-field collision, not a strategy/preflight research failure.

Evidence status from attempt 1:

- market preflight executed: **NO**;
- EXP-031 target outcomes: **NO**;
- EXP-031 P&L outcomes: **NO**;
- Jul-Aug loaded/inspected: **NO**;
- Sep loaded/inspected: **NO**.

Corrections:

- qualifying return now unpacks geometry first and sets `status="armed"` afterward;
- non-qualifying return now unpacks geometry first and sets `status="no_recent_h1_range_qualified"` afterward;
- no strategy mechanics, recency order, target-room rule, frequency gate, sizing, cost or safety rule changed.

Fix commits:

- `5335a440edc0ad3a58995dfa0bb16b08fb91713b`;
- `a50cf398e57fd13fb1ac1e8b26fbe701df1e1cf9`.

### Next

Rerun the identical frozen EXP-031 zero-outcome preflight.


## Zero-outcome preflight — PASS

**Retry workflow run:** `36010384519`  
**Retry trigger SHA:** `7ff211f748245ed744a4dfea2563dd02032fded2`  
**Durable result commit:** `e0c7566`

Protection:

- target outcomes: **NO**;
- P&L outcomes: **NO**;
- Jul-Aug: unopened;
- Sep: unopened.

Frozen-gate result:

- filled valid signals: **417**;
- deployable signals: **417**;
- every market >=25: PASS;
- LONG and SHORT every market: PASS;
- total >=300: PASS;
- safety overlay: PASS.

Per-market signals:

- XAUUSD 64;
- EURUSD 50;
- GBPUSD 51;
- USDJPY 44;
- EURJPY 55;
- AUDUSD 53;
- USDCAD 52;
- USDCHF 48.

Selected H1 range counts among armed setups:

- H1_0: 340;
- H1_1: 268.

Reference-account utility across filled signals:

- GE40: 16;
- GE30: 35;
- LT30: 366.

**Disposition:** PASS. v0.5 may proceed to development while Jul-Aug and Sep remain sealed.


## Development implementation checkpoint — zero outcomes

Frozen before any EXP-031 development outcome:

- same six chronological slices as EXP-028;
- same audited target-first labeler;
- same stop-first / timeout semantics;
- same normalized-R signal metrics;
- same safe-lot USD500 one-open portfolio;
- same daily stop-adding-risk rules;
- same >+0.20R pooled gross gate;
- same positive primary/stress gates;
- same PF / MDD / weekday / market-share gates;
- H1_0 and H1_1 cohorts reported separately;
- cohort reporting is diagnostic only and may not be used to tune v0.5 after outcomes;
- Jul1 hard seal.

Implementation:

- development runner `f3e508d5a7fa4f5d282959951640a264bb51995d`;
- development workflow `29fe4dc6f95074cfe0401b48ee678b00f5d2c861`.

At this checkpoint:

- EXP-031 target outcomes: **NO**;
- EXP-031 P&L outcomes: **NO**;
- Jul-Aug loaded/labeled: **NO**;
- Sep loaded/labeled: **NO**.

### Next

Trigger EXP-031 development only. Any mandatory gate failure stops before secondary testing.


## Development outcome — FAIL

**Workflow run:** `36010973242`  
**Trigger SHA:** `10456a42163eec1a89ba6cebcddda8e088979844`  
**Durable result commit:** `d10e0e9`  
**Result:** `research/results/EXP-031-development-summary-v0.5.json`

Protection:

- source parsed only through 2026-06-30;
- Jul-Aug secondary loaded/labeled: **NO**;
- Sep final holdout loaded/labeled: **NO**.

### Pooled signal layer

- 329 development signals;
- target hit rate: **33.74%**;
- gross normalized expectancy: **-0.00994R**;
- primary expectancy: **-0.2063R**;
- stress expectancy: **-0.4027R**;
- primary PF: **0.740**;
- stress PF: **0.565**;
- positive stress folds: **0/6**.

### H1 recency cohorts

H1_0:

- 196 signals;
- hit rate 34.18%;
- gross expectancy **+0.0259R**;
- primary **-0.1718R**;
- stress **-0.3696R**.

H1_1:

- 133 signals;
- hit rate 33.08%;
- gross expectancy **-0.0628R**;
- primary **-0.2571R**;
- stress **-0.4514R**.

Interpretation:

The H1_1 fallback added frequency but did **not** add edge. H1_0 remained slightly better, but still far below the prospectively frozen >+0.20R gross hurdle and negative after costs.

### Per-market development diagnostic

No symbol-level result is eligible for promotion or selective rescue after observing development.

Descriptive results:

- GBPUSD gross +0.416R, primary +0.214R, stress +0.011R;
- AUDUSD gross +0.203R, primary +0.003R, stress -0.198R;
- XAUUSD gross +0.126R, primary -0.038R, stress -0.202R;
- EURUSD gross +0.088R, primary -0.117R, stress -0.322R;
- remaining markets gross and post-cost expectancy negative.

These are retrospective diagnostics only. Do not create a post-hoc symbol whitelist.

### Reference-account portfolio

- 261 trades;
- 57 distinct trade weekdays;
- hit rate 35.63%;
- primary P&L **-USD337.34**;
- stress P&L **-USD797.31**;
- primary expectancy **-USD1.29/trade**;
- stress expectancy **-USD3.05/trade**;
- primary PF **0.817**;
- stress PF **0.626**;
- primary MDD **USD408.93**;
- stress MDD **USD856.89**;
- final-day >=USD100: **0**;
- final-day >=USD150: **0**.

### Failed mandatory gates

- pooled gross expectancy >+0.20R;
- pooled primary expectancy >0;
- pooled stress expectancy >0;
- >=4/6 positive-stress folds;
- reference primary expectancy >0;
- reference stress expectancy >0;
- primary PF >=1.10;
- stress PF >=1.05;
- stress MDD <=USD150.

Frequency, weekday count, diversification and provenance gates passed.

### Final disposition

**FAIL.** Do not open Jul-Aug.

### Family-level conclusion

Engine M has now supplied enough development evidence across v0.2-v0.5:

- non-chasing limit execution can improve entry quality versus immediate/chasing entry;
- broad MTF midpoint logic produced only a tiny gross edge;
- progressively stronger H1/liquidity selectivity either collapsed frequency or failed to create robust pre-cost edge;
- v0.5 recovered frequency but pooled gross edge reverted slightly negative.

Do not create Engine M v0.6 by another small H1/lookback/filter variation.

Preserve the useful execution lesson and move to a genuinely different strategy family.
