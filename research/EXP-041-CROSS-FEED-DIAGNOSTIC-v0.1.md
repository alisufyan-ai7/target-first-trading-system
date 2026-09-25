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
