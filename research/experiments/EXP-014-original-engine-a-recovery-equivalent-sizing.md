# EXP-014 — Original Engine A Recovery + P&L-Equivalent Sizing

**Status:** READY TO EXECUTE — REQUIRED GATE BEFORE RANKER RESUMES  
**Date:** 2026-09-22

## Why this experiment exists

Two corrections govern the next phase:

1. XAUUSD 0.10 lot is the economic anchor, while other markets require symbol-specific equivalent lot sizes.
2. Original Badar-inspired Gold Engine A from EXP-002 must not be conflated with Engine A v0.2-portable.

EXP-014 is therefore a recovery/reproduction and sizing-normalization gate.

## Part A — recover original Engine A

Authorized evidence:

- EXP-001;
- EXP-002;
- strategies/engine-a-liquidity-mss-fvg/SPEC.md;
- docs/BADAR-VIDEO-EVIDENCE.md;
- docs/TIMEFRAME-AND-MARKET-CONTEXT.md;
- originating/current chat context;
- no unrelated repository/chat/project context.

Recorded sequence:

liquidity -> sweep -> internal MSS -> displacement -> FVG -> retracement -> tight structural/FVG stop -> target expansion.

Starting recovery parameters:

- recent 5m swing liquidity;
- 5m wick sweep and close back inside;
- 1m internal MSS close;
- displacement >= approximately 1.6x recent 1m average body;
- FVG after shift;
- entry near 50% FVG;
- active window about 06:00–18:00 UTC;
- XAU USD 5 target-first label.

## Reproduction benchmark

Overall target:

- ~372 trades/signals;
- USD 5 hit ~29.6%;
- average structural risk ~USD 1.02 Gold;
- median favorable excursion ~USD 3.30;
- simplified expectancy ~+USD 0.79 Gold/trade before costs.

Development March–May:

- ~185 trades;
- USD 5 ~31.9%;
- expectancy ~+USD 0.85.

Holdout June–Aug 20:

- ~187 trades;
- USD 2 48.7%;
- USD 3 41.7%;
- USD 4 31.6%;
- USD 5 27.3%;
- expectancy ~+USD 0.72.

## Frozen reproduction-acceptance protocol

**Frozen before any new EXP-014 reconstruction outcome is calculated.**

A reconstruction is compared to the complete EXP-002 benchmark vector. No single attractive metric can compensate for broad failure elsewhere.

### Hard benchmark bands

- overall trade count: **335–409** (approximately ±10% around 372);
- development trade count: **163–207** (approximately ±12% around 185);
- holdout trade count: **165–209** (approximately ±12% around 187);
- overall USD 5 target-first rate: **26.6%–32.6%** (29.6% ±3 percentage points);
- holdout USD 5 target-first rate: **24.3%–30.3%** (27.3% ±3 percentage points);
- holdout USD 2 target-first rate: **44.7%–52.7%** (48.7% ±4 percentage points);
- holdout USD 3 target-first rate: **37.7%–45.7%** (41.7% ±4 percentage points);
- holdout USD 4 target-first rate: **27.6%–35.6%** (31.6% ±4 percentage points);
- average structural risk distance: **USD 0.867–1.173 Gold** (USD 1.02 ±15%);
- median favorable excursion: **USD 2.805–3.795 Gold** (USD 3.30 ±15%).

### Simplified-expectancy bands

Because simplified expectancy is particularly sensitive to small differences in timeout and stop mechanics, use a wider but still numerical tolerance while requiring the sign to remain positive in every split:

- overall: **+USD 0.514 to +USD 1.067 Gold/trade** (0.79 ±35%);
- development: **+USD 0.553 to +USD 1.148 Gold/trade** (0.85 ±35%);
- holdout: **+USD 0.468 to +USD 0.972 Gold/trade** (0.72 ±35%).

### Acceptance classification

- **PASS / recovered reproduction:** all hard benchmark bands and all three expectancy bands pass simultaneously.
- **NEAR MATCH / not yet recovered:** most dimensions are close, but at least one frozen band fails. This is diagnostic only and may motivate one ambiguity-specific next variant; it is not allowed to be called the recovered original.
- **FAIL:** material multi-dimensional mismatch, wrong expectancy sign in either split, or a miss larger than twice the stated tolerance on any core dimension.

A future variant may change only a mechanically identifiable ambiguity that was frozen in the prior variant. It may not change several unrelated parameters simultaneously to chase the benchmark.

## A1 freeze checkpoint

The first mechanical recovery attempt is frozen at:

- `strategies/engine-a-liquidity-mss-fvg/SPEC-v0.1-recovery-A1.md`;
- acceptance-protocol commit: `24505683baeb326b53b0ff1dc76a71593a0a72c5`;
- initial A1-spec commit: `72dc26d813c4fd1ef9455f97547908346b501930`;
- intermediate A1 clarification commit: `78339e9cb168c9ce0425f19749b4fdaac2f9a819`;
- **final pre-outcome A1-spec commit:** `448aef86af7e7d5227c4e4b9405f9d0c1f8cae03` (adds explicit T5 trade closure/MFE lifecycle).

No A1 outcome was calculated before these freezes.

## Reproduction procedure

1. define all missing mechanical details before comparing a variant to the benchmark;
2. run the complete original date window;
3. compare trade count, hit rates, stop distribution, MFE, and expectancy;
4. checkpoint each materially different reconstruction;
5. do not tune directly to one metric while degrading the others;
6. if no honest reconstruction matches reasonably, record that the original code is unrecoverable rather than inventing certainty.

## Part A checkpoint — A1 result

**Status:** FAIL — MATERIAL MULTI-DIMENSIONAL MISMATCH; DO NOT RELABEL AS ORIGINAL ENGINE A

### Data provenance and audit

The execution environment could not retrieve Dukascopy's binary endpoint directly. For A1, the same Dukascopy XAUUSD M1 bid history was accessed through a public external research mirror generated from Dukascopy data. This external repository is used **only as research-data transport**, not as project context.

Files/blobs used:

- 2026-03: `68e025d16d184b12a78505a30efc05564f6b5d2b`;
- 2026-04: `ffe75abc4fda834b9368c7b25687e4e0f2e1baec`;
- 2026-05: `7adc7eb29dff4fef02784d16c670a7ca5ddfb52f`;
- 2026-06: `3ffcf63c7fe50aa0eb20830f70316231d71b8c8a`;
- 2026-07: `0c992d59888d6ba032793570b7ccb2ded0d0407d`;
- 2026-08: `eac2cab31176755f93109dff6127c5aa92090319`.

Audit over 2026-03-01 through 2026-08-20 inclusive:

- one-minute rows: **230,813**;
- first timestamp: 2026-03-01 00:00 UTC;
- last timestamp: 2026-08-20 23:58 UTC;
- duplicate timestamps: 0;
- invalid OHLC rows: 0;
- non-minute timestamp steps: 0;
- valid complete UTC-aligned 5m bars: 46,157.

The **230,813 row count exactly matches the row count recorded in EXP-002**, materially reducing the likelihood that A1's large discrepancy is explained by simple date-window/data-coverage drift. Direct Dukascopy retrieval should still be preferred for later execution-grade verification.

### A1 signal funnel

- qualifying 5m sweeps: 2,332;
- sweeps with eligible internal pivot: 2,326;
- first MSS found: 1,198;
- MSS candle also passing 1.6x displacement: 523;
- qualifying FVG: 417;
- midpoint fills before one-open suppression: 257;
- sweep-while-open suppressions: 2;
- fill-while-open suppressions: 0;
- accepted trades: **255**.

### Benchmark comparison

| Metric | EXP-002 benchmark | A1 | Frozen band | Pass? |
|---|---:|---:|---:|---|
| Overall trades | ~372 | **255** | 335–409 | No |
| Development trades | ~185 | **128** | 163–207 | No |
| Holdout trades | ~187 | **127** | 165–209 | No |
| Overall T5 | 29.6% | **11.76%** | 26.6–32.6% | No |
| Holdout T5 | 27.3% | **11.02%** | 24.3–30.3% | No |
| Holdout T2 | 48.7% | **22.83%** | 44.7–52.7% | No |
| Holdout T3 | 41.7% | **18.90%** | 37.7–45.7% | No |
| Holdout T4 | 31.6% | **14.17%** | 27.6–35.6% | No |
| Avg structural risk | ~1.02 | **0.827** | 0.867–1.173 | No |
| Median MFE | ~3.30 | **0.00** | 2.805–3.795 | No |
| Overall expectancy | +0.79 | **-0.102** | +0.514 to +1.067 | No |
| Development expectancy | +0.85 | **-0.092** | +0.553 to +1.148 | No |
| Holdout expectancy | +0.72 | **-0.111** | +0.468 to +0.972 | No |

Additional A1 diagnostics:

- development T5: 12.50%;
- development average risk: 0.917 Gold;
- holdout average risk: 0.735 Gold;
- overall median risk: 0.640 Gold;
- T5 wins / stops / timeouts: 30 / 225 / 0;
- overall average MFE: 1.036 Gold;
- holdout average MFE: 1.091 Gold.

### Interpretation

A1 is a clear **FAIL**, not a near match.

Two mismatches stand out:

1. the candidate count is materially too low before outcome evaluation (257 raw fills versus the ~372 final EXP-002 signals);
2. the frozen tight FVG-edge stop produces far too many rapid invalidations, with target-first rates and expectancy far below EXP-002.

The exact row-count match means it is more useful to investigate the frozen implementation ambiguities than to blame the result on a broad data-window mismatch.

### Next ambiguity to test

For A2, change **one mechanics ambiguity only**: the coupling between MSS and displacement.

A1 required the **first MSS candle itself** to satisfy the 1.6x displacement threshold and expired the setup otherwise. The preserved EXP-002 wording and Badar evidence describe the causal sequence as **MSS -> displacement -> FVG**, which does not prove that MSS and displacement must be the same candle.

A2 should therefore keep every other A1 rule unchanged while allowing the first MSS to be followed by a qualifying displacement candle in a short, prospectively frozen window. No stop, liquidity, FVG-entry, session, horizon, or target rule should change in A2.

## Part A checkpoint — A2 result

**Status:** FAIL — FREQUENCY IMPROVED, OUTCOME GEOMETRY STILL FAR FROM EXP-002

A2 changed only the frozen MSS/displacement coupling. All other A1 rules remained unchanged.

### A2 signal funnel

- qualifying 5m sweeps: 2,332;
- sweeps with eligible internal pivot: 2,326;
- first MSS found: 1,198;
- displacement found on MSS / next-two-candle window: 639;
- qualifying FVG: 497;
- midpoint fills before one-open suppression: 302;
- sweep-while-open suppressions: 3;
- fill-while-open suppressions: 1;
- accepted trades: **298**.

### Benchmark comparison

| Metric | EXP-002 benchmark | A2 | Frozen band | Pass? |
|---|---:|---:|---:|---|
| Overall trades | ~372 | **298** | 335–409 | No |
| Development trades | ~185 | **146** | 163–207 | No |
| Holdout trades | ~187 | **152** | 165–209 | No |
| Overall T5 | 29.6% | **11.41%** | 26.6–32.6% | No |
| Holdout T5 | 27.3% | **10.53%** | 24.3–30.3% | No |
| Holdout T2 | 48.7% | **21.71%** | 44.7–52.7% | No |
| Holdout T3 | 41.7% | **18.42%** | 37.7–45.7% | No |
| Holdout T4 | 31.6% | **13.16%** | 27.6–35.6% | No |
| Avg structural risk | ~1.02 | **0.791** | 0.867–1.173 | No |
| Median MFE | ~3.30 | **0.00** | 2.805–3.795 | No |
| Overall expectancy | +0.79 | **-0.089** | +0.514 to +1.067 | No |
| Development expectancy | +0.85 | **-0.076** | +0.553 to +1.148 | No |
| Holdout expectancy | +0.72 | **-0.102** | +0.468 to +0.972 | No |

Additional diagnostics:

- development T5: 12.33%;
- development average risk: 0.872 Gold;
- holdout average risk: 0.713 Gold;
- T5 wins / stops / timeouts: 34 / 264 / 0;
- overall average MFE: 1.021 Gold;
- holdout average MFE: 1.037 Gold.

### A2 interpretation

The A2 single change increased accepted trades by 43, from 255 to 298, confirming that forcing MSS and displacement onto the same candle was too restrictive for recovery purposes.

However, target-first rates, MFE, and expectancy remain far from EXP-002. The preserved FVG-edge + USD 0.10 stop is still substantially tighter than the EXP-002 average-risk benchmark and appears to create rapid invalidation behavior.

A2 is therefore a clear **FAIL**, although the MSS -> displacement sequencing change is more consistent with the preserved causal wording and should be retained as a plausible recovery mechanic unless later evidence argues otherwise.

### A2 stop-geometry diagnostic (no rule change)

Before freezing A3, A2 was diagnosed without changing or rescoring any alternative strategy outcome.

Observed A2 exit timing:

- fill-bar stops: **170 / 298** accepted trades;
- stop on first full bar after fill: 43;
- stop on bars 2–3: 23;
- stop on bars 4–10: 22;
- stop after bar 10: 6;
- T5 exits: 34;
- timeouts: 0.

A2 FVG-width distribution:

- mean: 1.382 Gold;
- median: 1.010;
- 75th percentile: 1.818;
- 90th percentile: 2.693.

Structural-risk geometry measured **without calculating alternative target outcomes**:

| Candidate stop geometry | Mean risk | Median risk | Interpretation |
|---|---:|---:|---|
| A2 FVG far edge + fixed 0.10 | 0.791 | 0.605 | Too tight vs EXP-002 mean-risk benchmark |
| FVG far edge only | 0.691 | 0.505 | Even tighter |
| FVG far edge + 25% of FVG width | **1.037** | 0.758 | Mechanically plausible and close to ~1.02 benchmark |
| FVG far edge + 50% of FVG width | 1.382 | 1.010 | Mean risk materially high |
| Displacement-candle open + 0.10 | 1.862* | 1.513* | Too wide; invalid-side cases excluded |
| Displacement wick extreme + 0.10 | 2.152* | 1.715* | Too wide |
| 5m sweep extreme + 0.10 | 5.633* | 4.582* | Incompatible with EXP-002 tight-risk profile |

`* only geometrically valid cases included.`

This diagnostic supports testing a proportional FVG invalidation before any wider structural stop. It does **not** establish that the 25% buffer is the unpublished original rule.

### Next diagnostic before A3

Before changing another rule, measure where A2 stops occur (fill bar vs later bars) and the risk/FVG-width distribution. This is diagnostic only and does not modify A2. Then freeze one stop-placement ambiguity for A3; do not change candidate-generation rules simultaneously.

## A2 freeze checkpoint

A2 changes exactly one A1 ambiguity: displacement may occur on the MSS candle or either of the next two completed 1m candles while the same internal structure break remains valid.

Frozen specification:

- `strategies/engine-a-liquidity-mss-fvg/SPEC-v0.1-recovery-A2.md`;
- pre-outcome A2-spec commit: `ef409b51461b212f39048133b6dd1d86b5230ec5`.

All other A1 mechanics and the frozen acceptance protocol remain unchanged. No A2 outcome was calculated before this freeze.

## Part A checkpoint — A3 result

**Status:** FAIL — STRUCTURAL-RISK BAND RECOVERED, BUT TARGET-FIRST EDGE NOT RECOVERED

A3 changed only the A2 FVG-stop buffer.

### A3 signal funnel

Candidate-generation funnel is unchanged from A2 through midpoint fill:

- sweeps: 2,332;
- internal-pivot eligible: 2,326;
- MSS: 1,198;
- displacement: 639;
- FVG: 497;
- raw midpoint fills: 302.

Longer A3 trade life from the wider stop caused:

- sweep-while-open suppressions: 6;
- fill-while-open suppressions: 2;
- accepted trades: **294**.

### Benchmark comparison

| Metric | EXP-002 benchmark | A3 | Frozen band | Pass? |
|---|---:|---:|---:|---|
| Overall trades | ~372 | **294** | 335–409 | No |
| Development trades | ~185 | **145** | 163–207 | No |
| Holdout trades | ~187 | **149** | 165–209 | No |
| Overall T5 | 29.6% | **14.97%** | 26.6–32.6% | No |
| Holdout T5 | 27.3% | **13.42%** | 24.3–30.3% | No |
| Holdout T2 | 48.7% | **23.49%** | 44.7–52.7% | No |
| Holdout T3 | 41.7% | **21.48%** | 37.7–45.7% | No |
| Holdout T4 | 31.6% | **16.78%** | 27.6–35.6% | No |
| Avg structural risk | ~1.02 | **1.040** | 0.867–1.173 | **Yes** |
| Median MFE | ~3.30 | **0.00** | 2.805–3.795 | No |
| Overall expectancy | +0.79 | **-0.013** | +0.514 to +1.067 | No |
| Development expectancy | +0.85 | **-0.017** | +0.553 to +1.148 | No |
| Holdout expectancy | +0.72 | **-0.009** | +0.468 to +0.972 | No |

Additional A3 diagnostics:

- development T5: 16.55%;
- development average risk: 1.165 Gold;
- holdout average risk: 0.919 Gold;
- overall median risk: 0.761 Gold;
- fill-bar stops: **148 / 294**;
- T5 wins / total stops / timeouts: 44 / 250 / 0;
- overall average MFE: 1.235 Gold;
- holdout average MFE: 1.178 Gold.

### A3 interpretation

The A3 proportional FVG stop recovers the aggregate **average-risk** dimension almost exactly, but the target ladder, MFE, expectancy, and trade count remain materially wrong.

This demonstrates that matching the stop-risk benchmark alone is insufficient and prevents falsely declaring recovery based on one successful statistic.

### Next ambiguity to test

A4 should change only the **5m liquidity-swing confirmation rule**, from A3's local 1-left/1-right pivot to a more selective 2-left/2-right confirmed 5m swing.

Reason:

- liquidity quality remains a documented recovery unknown;
- the current candidate stream appears too weak even after risk geometry is aligned;
- stronger 5m liquidity is a mechanically distinct hypothesis that can improve setup quality without changing MSS, displacement, FVG, entry, stop, session, or outcome rules.

Trade count may fall; that is acceptable for the diagnostic. Do not compensate by changing fill expiry or level reuse in the same variant.

## A3 freeze checkpoint

A3 inherits A2 candidate generation unchanged and changes exactly one stop-placement ambiguity:

- replace the fixed USD 0.10 FVG-edge buffer with a buffer equal to **25% of the selected FVG width**.

Frozen specification:

- `strategies/engine-a-liquidity-mss-fvg/SPEC-v0.1-recovery-A3.md`;
- pre-outcome A3-spec commit: `75d6885ccb29bc68255a2ef2f80eb85aeea52e94`.

No A3 target/expectancy outcome was calculated before this freeze.

## Part A checkpoint — A4 result

**Status:** FAIL — STRONGER 5m LIQUIDITY PIVOT REDUCED FREQUENCY AND WORSENED HOLDOUT

A4 changed only the 5m swing confirmation rule from A3's 1-left/1-right pivot to 2-left/2-right.

### A4 funnel and results

- sweeps: 1,719;
- internal-pivot eligible: 1,702;
- MSS: 885;
- displacement: 436;
- FVG: 338;
- raw midpoint fills: 212;
- accepted trades: **209**.

| Metric | EXP-002 benchmark | A4 | Frozen band | Pass? |
|---|---:|---:|---:|---|
| Overall trades | ~372 | **209** | 335–409 | No |
| Development trades | ~185 | **103** | 163–207 | No |
| Holdout trades | ~187 | **106** | 165–209 | No |
| Overall T5 | 29.6% | **13.40%** | 26.6–32.6% | No |
| Holdout T5 | 27.3% | **8.49%** | 24.3–30.3% | No |
| Holdout T2 | 48.7% | **20.75%** | 44.7–52.7% | No |
| Holdout T3 | 41.7% | **16.04%** | 37.7–45.7% | No |
| Holdout T4 | 31.6% | **10.38%** | 27.6–35.6% | No |
| Avg structural risk | ~1.02 | **0.966** | 0.867–1.173 | Yes |
| Median MFE | ~3.30 | **0.00** | 2.805–3.795 | No |
| Overall expectancy | +0.79 | **-0.041** | +0.514 to +1.067 | No |
| Development expectancy | +0.85 | **+0.145** | +0.553 to +1.148 | No |
| Holdout expectancy | +0.72 | **-0.221** | +0.468 to +0.972 | No |

Additional diagnostics:

- holdout average risk: 0.875 Gold;
- fill-bar stops: 103 / 209 overall;
- T5 wins / total stops / timeouts: 28 / 181 / 0.

### A4 interpretation

The stronger 2-left/2-right 5m liquidity definition reduces both frequency and holdout quality. It does not explain the original EXP-002 edge.

Therefore do **not** carry the A4 5m-pivot change forward as the default recovery branch.

The next variant should return to the A3 baseline and test a different single ambiguity rather than stacking another rule on top of the failed A4 branch.

## A4 freeze checkpoint

A4 inherits A3 unchanged except for one liquidity-quality ambiguity:

- 5m swing confirmation changes from 1-left/1-right to a **2-left/2-right** confirmed pivot;
- the same 24-bar age limit and liquidity-level retirement rules remain unchanged.

Frozen specification:

- `strategies/engine-a-liquidity-mss-fvg/SPEC-v0.1-recovery-A4.md`;
- pre-outcome A4-spec commit: `cbe731f019767e07720a75441ff6e4ddb56f2650`.

No A4 outcome was calculated before this freeze.

## Part A checkpoint — A5 result

**Status:** FAIL — STRONGER INTERNAL MSS PIVOT REDUCED FREQUENCY WITHOUT RECOVERING TARGET-FIRST QUALITY

A5 branched from A3 and changed only the 1m internal pivot confirmation from 1-left/1-right to 2-left/2-right.

### A5 funnel and results

- sweeps: 2,332;
- eligible stronger internal pivot: 2,155;
- MSS: 831;
- displacement: 486;
- FVG: 391;
- raw midpoint fills: 221;
- accepted trades: **217**.

| Metric | EXP-002 benchmark | A5 | Frozen band | Pass? |
|---|---:|---:|---:|---|
| Overall trades | ~372 | **217** | 335–409 | No |
| Development trades | ~185 | **98** | 163–207 | No |
| Holdout trades | ~187 | **119** | 165–209 | No |
| Overall T5 | 29.6% | **15.67%** | 26.6–32.6% | No |
| Holdout T5 | 27.3% | **13.45%** | 24.3–30.3% | No |
| Holdout T2 | 48.7% | **24.37%** | 44.7–52.7% | No |
| Holdout T3 | 41.7% | **22.69%** | 37.7–45.7% | No |
| Holdout T4 | 31.6% | **17.65%** | 27.6–35.6% | No |
| Avg structural risk | ~1.02 | **1.188** | 0.867–1.173 | No |
| Median MFE | ~3.30 | **0.00** | 2.805–3.795 | No |
| Overall expectancy | +0.79 | **-0.026** | +0.514 to +1.067 | No |
| Development expectancy | +0.85 | **-0.020** | +0.553 to +1.148 | No |
| Holdout expectancy | +0.72 | **-0.031** | +0.468 to +0.972 | No |

Additional diagnostics:

- fill-bar stops: 101 / 217;
- T5 wins / stops / timeouts: 34 / 183 / 0;
- holdout average risk: 1.064 Gold.

### A5 interpretation

A stronger internal pivot does not explain EXP-002. It materially reduces the sample while leaving target-first quality far below the benchmark.

Do not carry the A5 internal-pivot change forward.

### Next ambiguity

Return to A3 and test only **liquidity-level reuse**.

A3 retired a recent 5m swing level after its first qualifying sweep even if no trade ultimately formed. A plausible simpler original implementation may instead have kept using the most recent eligible swing until a newer swing replaced it or it aged out.

A6 should therefore:

- preserve A3's 1-left/1-right 5m pivot;
- preserve A3's 1-left/1-right internal pivot;
- preserve A3 MSS/displacement/FVG/entry/stop/outcome mechanics;
- remove only the one-sweep permanent-consumption rule.

## A5 freeze checkpoint

A5 returns to the A3 baseline after A4 failed and changes exactly one different ambiguity:

- 1m internal MSS pivot confirmation changes from 1-left/1-right to **2-left/2-right**;
- the 12-minute internal-pivot lookback remains unchanged;
- 5m liquidity, displacement, FVG, entry, A3 stop, session, horizon, and outcome rules remain unchanged.

Frozen specification:

- `strategies/engine-a-liquidity-mss-fvg/SPEC-v0.1-recovery-A5.md`;
- pre-outcome A5-spec commit: `f4720ed0dc73439b64c4280a07429d7225073f89`.

No A5 outcome was calculated before this freeze.

## Part A checkpoint — A6 result

**Status:** FAIL — FREQUENCY/BALANCE AND AVERAGE RISK NEAR RECOVERY, TARGET-FIRST EDGE STILL NOT RECOVERED

A6 branched from A3 and changed only liquidity-level reuse.

### A6 funnel

- qualifying reusable-level sweeps: 2,757;
- eligible internal pivot: 2,747;
- MSS: 1,474;
- displacement: 787;
- FVG: 607;
- raw midpoint fills: 358;
- sweep-while-open suppressions: 6;
- fill-while-open suppressions: 19;
- accepted trades: **333**.

### Benchmark comparison

| Metric | EXP-002 benchmark | A6 | Frozen band | Pass? |
|---|---:|---:|---:|---|
| Overall trades | ~372 | **333** | 335–409 | No — short by 2 |
| Development trades | ~185 | **164** | 163–207 | **Yes** |
| Holdout trades | ~187 | **169** | 165–209 | **Yes** |
| Overall T5 | 29.6% | **15.02%** | 26.6–32.6% | No |
| Holdout T5 | 27.3% | **13.61%** | 24.3–30.3% | No |
| Holdout T2 | 48.7% | **23.08%** | 44.7–52.7% | No |
| Holdout T3 | 41.7% | **21.30%** | 37.7–45.7% | No |
| Holdout T4 | 31.6% | **16.57%** | 27.6–35.6% | No |
| Avg structural risk | ~1.02 | **1.053** | 0.867–1.173 | **Yes** |
| Median MFE | ~3.30 | **0.00** | 2.805–3.795 | No |
| Overall expectancy | +0.79 | **-0.023** | +0.514 to +1.067 | No |
| Development expectancy | +0.85 | **-0.057** | +0.553 to +1.148 | No |
| Holdout expectancy | +0.72 | **+0.010** | +0.468 to +0.972 | No |

Additional A6 diagnostics:

- overall median structural risk: 0.7725 Gold;
- fill-bar stops: **163 / 333**;
- T5 wins / total stops / timeouts: 50 / 283 / 0;
- overall average MFE: 1.236 Gold;
- holdout average MFE: 1.155 Gold.

### A6 interpretation

A6 is the closest recovery variant so far on **signal frequency, development/holdout balance, and average structural risk**:

- development and holdout trade-count bands both pass;
- overall count misses the frozen lower bound by only two trades;
- average structural risk passes.

However, the complete benchmark vector still fails decisively because target-first rates and MFE remain roughly half the EXP-002 levels and expectancy is nowhere near the recorded positive values.

This is important evidence: the missing original mechanics are no longer primarily a frequency problem. A6 suggests that liquidity-level reuse plausibly belongs in the recovered implementation, but candidate **quality / entry-path / invalidation geometry** remains materially wrong.

A6 must not be called the recovered original.

## A6 freeze checkpoint

A6 returns to the A3 baseline after A4/A5 pivot-strength branches failed and changes exactly one implementation ambiguity:

- the latest eligible 5m liquidity pivot is **not permanently consumed by its first qualifying sweep**;
- it remains reusable for later qualifying sweep bars until replaced by a newer same-side confirmed pivot or until the unchanged 24-bar age limit expires;
- the A3 5m/1m pivot definitions, MSS -> displacement sequencing, FVG, midpoint entry, proportional FVG stop, session, one-open policy, horizon, same-bar handling, and target labels remain unchanged.

Frozen specification:

- `strategies/engine-a-liquidity-mss-fvg/SPEC-v0.1-recovery-A6.md`;
- pre-outcome A6-spec commit: `71c87644456d858aa807b6bcfcc7434bece2725d`.

No A6 outcome was calculated before this freeze.

## Part A checkpoint — A7 result

**Status:** FAIL — DISPLACEMENT-CANDLE-ONLY FVG IS TOO STRICT AND COLLAPSES HOLDOUT QUALITY

A7 inherited A6 and changed only FVG timing.

### A7 funnel

- reusable-level sweeps: 2,757;
- eligible internal pivot: 2,747;
- MSS: 1,474;
- displacement: 787;
- displacement-candle FVG: 241;
- raw midpoint fills: 113;
- accepted trades: **107**.

### Benchmark comparison

| Metric | EXP-002 benchmark | A7 | Frozen band | Pass? |
|---|---:|---:|---:|---|
| Overall trades | ~372 | **107** | 335–409 | No |
| Development trades | ~185 | **52** | 163–207 | No |
| Holdout trades | ~187 | **55** | 165–209 | No |
| Overall T5 | 29.6% | **11.21%** | 26.6–32.6% | No |
| Holdout T5 | 27.3% | **3.64%** | 24.3–30.3% | No |
| Holdout T2 | 48.7% | **12.73%** | 44.7–52.7% | No |
| Holdout T3 | 41.7% | **12.73%** | 37.7–45.7% | No |
| Holdout T4 | 31.6% | **10.91%** | 27.6–35.6% | No |
| Avg structural risk | ~1.02 | **0.782** | 0.867–1.173 | No |
| Median MFE | ~3.30 | **0.00** | 2.805–3.795 | No |
| Overall expectancy | +0.79 | **-0.043** | +0.514 to +1.067 | No |
| Development expectancy | +0.85 | **+0.334** | +0.553 to +1.148 | No |
| Holdout expectancy | +0.72 | **-0.400** | +0.468 to +0.972 | No |

Additional diagnostics:

- fill-bar stops: 65 / 107;
- T5 wins / total stops / timeouts: 12 / 95 / 0.

### A7 interpretation

Requiring the FVG to be formed by the displacement candle itself is inconsistent with the EXP-002 benchmark under the otherwise preserved A6 mechanics.

Do not carry A7 forward.

Return to A6 as the current best recovery baseline because it is closest on trade frequency/split balance and average structural risk.

## A7 freeze checkpoint

A7 inherits A6 and changes exactly one FVG-selection ambiguity:

- the same-direction FVG must be formed **by the displacement candle itself**;
- A7 no longer accepts an FVG first appearing one or two candles after displacement;
- no minimum gap-size filter is introduced;
- liquidity reuse, pivots, MSS/displacement, midpoint entry, proportional FVG stop, session, one-open policy, horizon, and conservative outcome handling remain unchanged.

Frozen specification:

- `strategies/engine-a-liquidity-mss-fvg/SPEC-v0.1-recovery-A7.md`;
- pre-outcome A7-spec commit: `75c290d7d0189e50d4cb4f4728c073e77f00b2e7`.

No A7 outcome was calculated before this freeze.

## A8 forensic freeze checkpoint

Repository-history audit found no surviving EXP-002 strategy implementation: the original EXP-002 commit `ef131e4c2b13f58dedfeb9782200e62761253017` added only the experiment-summary Markdown, and its parent added EXP-001 narrative evidence. No original detector/backtest code is available in that file history.

A8 therefore tests one particularly consequential unresolved implementation ambiguity from the A6 baseline: **MSS timing relative to the completed 5m sweep bar**.

A8 deliberately allows the 1m MSS/displacement/FVG sequence to begin after the actual intrabar liquidity breach but before the containing 5m bar has completed, while still using that bar's eventual close to classify it as a valid sweep/rejection.

This is explicitly **forensic and non-causal**:

- it may reveal timing leakage capable of explaining EXP-002;
- it is not deployable and cannot become the production recovered Engine A even if it reproduces the historical benchmark;
- all non-timing A6 rules remain unchanged.

Frozen specification:

- `strategies/engine-a-liquidity-mss-fvg/SPEC-v0.1-recovery-A8-forensic.md`;
- initial pre-outcome A8-spec commit: `5d25985f005edfbf114181a3a627cc6c078d052f`;
- final pre-outcome A8 event-time clarification commit: `5f3e820cd7fd2157e4c9ef549a9d16b34ca9ede3`.

No A8 outcome was calculated before this freeze.

## Part B — correct equivalent-lot rule

### Gold

- reference size 0.10 lot;
- normal target about USD 5 Gold move ~= USD 50 gross;
- USD 3–4 ~= USD 30–40 fallback;
- stronger validated continuation may support USD 70–100+.

### Non-Gold

First freeze a native target distance D for the engine/market.

Then propose:

equivalent lot = 50 / (D x USD P&L per native unit at 1 lot).

The proposed size must pass:

- structural-stop dollar loss;
- required margin;
- notional/equity;
- remaining daily loss budget;
- correlated open exposure.

If full USD-50-equivalent size is unsafe but a smaller size still provides a validated USD 30–40 opportunity, allow the smaller objective. Otherwise reject.

No stop compression, martingale, or post-loss size increase.

## Target-distance methods to compare on development data only

1. volatility-burden equivalence;
2. engine-conditioned favorable-excursion distribution.

Select/freeze the method before new holdout use.

EXP-006 remains a sizing diagnostic; its large FX lot estimates are evidence of feasibility pressure, not a reason to switch to same-lot sizing.

## Architecture gate

Only after Part A reproduction and Part B sizing freeze:

1. route recovered Engine A candidates into the common strategy-engine contract;
2. evaluate transfer to selected markets under equivalent sizing;
3. add other independently validated engines;
4. resume target-first ranker work.

## Relationship to EXP-015

EXP-015 is the renumbered target-first ranker experiment.

It is **PAUSED** until EXP-014 passes.

Its earlier broad-pivot XAU candidate statistics are retained as diagnostics only and do not supersede the engine-first architecture.
