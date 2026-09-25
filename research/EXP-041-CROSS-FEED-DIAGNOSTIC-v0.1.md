# EXP-041 Cross-Feed Diagnostic v0.1

**Date:** 2026-09-25  
**Status:** PROSPECTIVELY FROZEN — ZERO OUTCOME  
**Purpose:** diagnose why the frozen twelve-month Dukascopy acquisition failed cross-feed sanity  
**Scientific target labels:** NONE  
**P&L:** NONE

## Question

The v0.1 acquisition has ~99.7% timestamp overlap with the existing pinned feed but material price/return disagreement for most markets.

Before changing any gate, determine whether the disagreement is primarily:

- timestamp alignment;
- stable quote/basis difference;
- high-frequency feed construction;
- symbol/feed mismatch;
- or broader material path mismatch.

## Data scope

Only the existing development-overlap interval:

`2026-03-23 00:00 UTC <= t < 2026-07-01 00:00 UTC`.

No Jul-Aug or Sep 2026 data.

## Frozen diagnostics

For each of 8 markets report:

1. M1 timestamp overlap ratio;
2. exact-timestamp close ratio `duka/current`:
   - median;
   - p05/p95;
   - daily-median ratio dispersion;
3. return correlation at:
   - 1m;
   - 5m;
   - 15m;
   - 1h;
   - 4h;
   - 1d;
4. directional-sign agreement at 5m and 1h;
5. best 5m lag in [-60m,+60m];
6. best 1h lag in [-3h,+3h];
7. volatility ratio on common hourly returns;
8. first/last timestamps and missing final-day status.

## Frozen diagnostic interpretation

- `TIME_ALIGNMENT_SUSPECT`: non-zero lag improves 5m or 1h correlation by >=0.05 and reaches >=0.95;
- `STABLE_PRICE_BASIS`: 1h correlation >=0.95 and daily-median price ratio standard deviation <=0.1%, even if level basis exceeds 0.5%;
- `HIGH_FREQUENCY_FEED_CONSTRUCTION`: daily correlation >=0.95, 1h correlation <0.95, and no time-shift diagnosis;
- `MATERIAL_PATH_MISMATCH`: none of the above;
- `SOURCE_COVERAGE_GAP`: added when the overlap feed does not cover Jun30.

These classifications are descriptive only.

## Decision rule

This diagnostic does **not** pass/fail the old acquisition gate.

After the result:

- do not retroactively change v0.1;
- if a clear mechanical cause exists, freeze an acquisition v0.2 before rerunning;
- if material path mismatch remains, obtain/compare a third independent source or intended-broker feed before macro outcome modeling.

## Protection

- target labels: NO;
- P&L: NO;
- Jul-Aug: NO;
- Sep: NO.


## Durable diagnostic result — MATERIAL PATH MISMATCH

**Result commit:** `bdd3b7f6786e6cc9752436b808ac2ae1af6f99cf`  
**Workflow:** PASS  
**Target labels / P&L:** NONE

Key findings on Mar23-Jun30 overlap:

- exact-M1 timestamp overlap: ~99.79%-99.86% across markets;
- best 5m lag: **0** for all 8 markets;
- best 1h lag: **0** for all 8 markets;
- therefore no evidence that a simple timezone/clock shift explains the disagreement;
- XAUUSD was relatively close in returns (5m 0.9856, 1h 0.9795, 1d 0.9778) but failed the frozen stable-basis criterion because daily-median price ratio varied too much;
- EURUSD 1h correlation 0.9140;
- GBPUSD 1h 0.8421;
- USDJPY 1h 0.9406;
- EURJPY 1h 0.7977;
- AUDUSD 1h 0.7799;
- USDCAD 1h 0.9740 but narrowly missed the frozen daily-ratio-stability criterion;
- USDCHF 1h 0.9220 and also had a Jun30 source-coverage gap.

All eight markets were therefore tagged `MATERIAL_PATH_MISMATCH`; USDCHF additionally `SOURCE_COVERAGE_GAP`.

**Interpretation:** do not weaken the acquisition-v0.1 thresholds. The disagreement is not explained by a simple lag and needs independent adjudication.

**Next:** compare both feeds to a third independent M1 source before choosing an expanded macro-development feed.
