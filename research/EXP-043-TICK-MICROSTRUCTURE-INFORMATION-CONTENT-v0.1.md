# EXP-043 Quote/Tick Microstructure Information-Content Study v0.1

**Frozen:** 2026-09-27, before EXP-043 target outcomes  
**Type:** development-only information-content research, not a strategy engine  
**Snapshot prerequisite:** durable PASS at `ba908a721a131b6062ebcc107ddab5a3e4c01285`

## 1. Objective

Test whether broker quote/tick microstructure adds stable target-before-stop information beyond the existing local M5 structural state.

The nested question is:

`LOCAL_M5 -> +EXECUTION_COST_STATE -> +PARTICIPATION_STATE -> +QUOTE_IMBALANCE_STATE`.

This experiment deliberately excludes mid-price OHLC/return features from the new information layer.

## 2. Immutable inputs

### Target-market price/label source

Canonical Dukascopy development release:

- tag: `exp041-data-dukas-m1-2025-07-01_2026-06-30-v2`;
- archive SHA-256: `90bc7301e459062e8e35cd89a1a9aac23332ca3472014dd2cc5045ba34794272`.

### Microstructure source

Immutable EXP-043 release:

- tag: `exp043-quote-microstructure-1m-2025-07-01_2026-06-30-v1`;
- archive SHA-256: `f95edf1f7762271941a1d24b3204c4640485d9e7b9b01440fbef86f521f52ca5`;
- snapshot-result Git blob: `f1bc941e88ee809bf9810fe34d780e41e4530fe7`.

Per-market aggregate file SHA-256 values must match the durable snapshot result.

## 3. Candidate / target mechanics

Reuse `research/code/mtf_information_v0_1.py` exactly for the broad structural candidate universe and target/path labels.

Markets:

- XAUUSD;
- EURUSD;
- GBPUSD;
- USDJPY;
- EURJPY;
- AUDUSD;
- USDCAD;
- USDCHF.

Candidate mechanics:

- completed M5 decisions;
- weekdays;
- 06:05-17:55 UTC;
- long and short independently;
- latest causally confirmed 2-left/2-right M5 pivot within prior 12 M5 bars;
- one research tick beyond pivot;
- first active M1 open at/after decision;
- same UTC date and entry before 18:00;
- no strategy-pattern filter.

Primary target rungs:

- T40eq = 2.0R;
- T50eq = 2.5R.

Path rules remain the existing 120-active-M1-bar / 20:00 UTC hard-cutoff rules.

No position sizing or P&L is used.

## 4. Frozen chronological evaluation

Reuse the original EXP-040 fold boundaries:

- WF1 eval [2026-04-13, 2026-04-27);
- WF2 eval [2026-04-27, 2026-05-11);
- WF3 eval [2026-05-11, 2026-05-25);
- WF4 eval [2026-05-25, 2026-06-08);
- WF5 eval [2026-06-08, 2026-06-22);
- WF6 eval [2026-06-22, 2026-07-01).

For each fold:

- calibration = seven calendar days immediately before evaluation;
- fit = all eligible development rows from 2025-07-01 before calibration;
- apply the same 120-minute purge before calibration start and evaluation start.

Protected Jul-Aug/Sep 2026 remain sealed.

## 5. Causal microstructure windowing

A minute row with `minute_start_utc = m` represents only ticks in:

`m <= tick < m + 1 minute`.

For structural decision timestamp `t`, EXP-043 may use only minute rows with:

`minute_start_utc + 1 minute <= t`.

Thus the 06:05 decision can use 06:04 and earlier, never the 06:05 minute.

Frozen windows:

- recent = [t-5m, t);
- medium = [t-30m, t);
- baseline = [t-60m, t).

Availability requirements:

- recent: >=4 observed minute rows;
- medium: >=24 observed minute rows;
- baseline: >=48 observed minute rows.

No forward filling.

A candidate enters EXP-043 only if all three windows satisfy these availability minima. The **same eligible candidate rows** are used by LOCAL_M5 and every enriched feature set.

## 6. Fixed feature construction

All ratio denominators use `epsilon = 1e-9`.

All log-ratios are natural log.

### A — LOCAL_M5

Exact existing `FEATURE_SETS["LOCAL_M5"]` plus market identity and direction as in EXP-040.

### B — PLUS_EXECUTION_COST_STATE

A plus four direction-independent features:

1. `spread_bps_recent`
   - median of minute `spread_bps_median` over recent 5m;

2. `spread_bps_p90_recent`
   - median of minute `spread_bps_p90` over recent 5m;

3. `log_spread_ratio_5_to_60`
   - log((recent median spread + eps)/(baseline median spread + eps));

4. `quote_age_recent_fraction`
   - median `last_quote_age_ms` over recent 5m divided by 60000.

### C — PLUS_PARTICIPATION_STATE

B plus five direction-independent features:

5. `log_tick_activity_ratio_5_to_60`
   - log((sum recent tick_count / observed recent minutes + eps) /
         (sum baseline tick_count / observed baseline minutes + eps));

6. `log_interarrival_ratio_5_to_60`
   - log((median recent median_interarrival_ms + eps) /
         (median baseline median_interarrival_ms + eps));

7. `price_update_fraction_recent`
   - over recent rows:
     sum(bid_update_count + ask_update_count - both_price_update_count) /
     max(1, sum(tick_count - 1));

8. `log_quote_size_ratio_5_to_60`
   - quote-size minute value = bid_volume_median + ask_volume_median;
   - log((recent median quote-size + eps)/(baseline median quote-size + eps));

9. `distinct_timestamp_fraction_recent`
   - sum(distinct_timestamp_count) / sum(tick_count) over recent rows.

### D — PLUS_QUOTE_IMBALANCE_STATE

C plus four direction-aligned features.

Let direction sign = +1 for long, -1 for short.

10. `directional_imbalance_recent`
    - direction sign * tick-count-weighted mean of minute
      `signed_quote_imbalance_mean` over recent 5m;

11. `directional_imbalance_medium`
    - direction sign * tick-count-weighted mean over medium 30m;

12. `directional_heavy_balance_recent`
    - direction sign * tick-count-weighted mean of
      (`bid_heavy_fraction - ask_heavy_fraction`) over recent 5m;

13. `directional_imbalance_change_5_vs_30`
    - directional_imbalance_recent - directional_imbalance_medium.

No market-specific sign rules or thresholds are allowed.

## 7. Learner

Same fixed learner family:

Base model:

- StandardScaler;
- LogisticRegression;
- C=0.25;
- L2;
- lbfgs;
- max_iter=1000;
- random_state=20260925.

Calibration:

- one-dimensional Platt logistic regression;
- C=1,000,000;
- lbfgs;
- max_iter=1000.

No hyperparameter search.

## 8. Metrics

For each feature set / rung:

- pooled log loss;
- Brier;
- ROC AUC diagnostic;
- 10-bin ECE;
- fold metrics;
- per-market metrics.

Also compute paired UTC-day mean log loss for each evaluation day.

## 9. Frozen information-advantage gate

For **both T40eq and T50eq**, an enriched set must satisfy versus LOCAL_M5:

1. >=1.0% relative pooled log-loss improvement;
2. pooled Brier lower;
3. log-loss win in >=4 of 6 folds;
4. pooled ECE not worse by >0.01;
5. per-market pooled log loss non-worse in >=5 of 8 markets;
6. paired day-level log-loss win fraction >=55%.

If multiple nested sets pass, select the smallest:

`PLUS_EXECUTION_COST_STATE -> PLUS_PARTICIPATION_STATE -> PLUS_QUOTE_IMBALANCE_STATE`.

T30/T70/T100 cannot rescue failure.

## 10. Integrity / sample gate

Before interpretation require:

- target archive SHA exact;
- all 8 target-market file SHAs exact;
- microstructure archive SHA exact;
- microstructure snapshot-result blob unchanged;
- all 8 microstructure aggregate file SHAs exact;
- no microstructure minute ending after a decision contributes to that decision;
- same eligible candidate rows across all feature sets;
- microstructure-eligible candidates >=90% of broad candidates in each market;
- every market-direction >=500 eligible labeled candidates;
- every evaluation fold has both classes for T40eq/T50eq;
- every market has both classes in pooled evaluation;
- at least 45 distinct paired evaluation UTC days;
- no protected-period row loaded/labeled;
- Engine R / EXP-015 outcomes unused.

Integrity failure => `INTEGRITY_FAIL_DO_NOT_INTERPRET`.

## 11. Scientific dispositions

If no enriched set passes:

`NO_STABLE_TICK_MICROSTRUCTURE_INFORMATION_ADVANTAGE`.

If execution-cost set is smallest passing:

`STABLE_EXECUTION_COST_INFORMATION_ADVANTAGE_FOUND`.

If participation set is smallest passing:

`STABLE_PARTICIPATION_INFORMATION_ADVANTAGE_FOUND`.

If quote-imbalance set is smallest passing:

`STABLE_QUOTE_IMBALANCE_INFORMATION_ADVANTAGE_FOUND`.

A PASS validates an information layer only. It does not itself authorize a strategy engine or protected-period use.

## 12. Next step

- PASS: preserve the smallest passing layer, then evaluate whether it improves a validated specialized engine candidate/ranking architecture.
- FAIL: do not tune tick windows/thresholds on the same development sample. The next materially richer source class is true exchange/broker order-book or aggressor-flow data, which likely requires broker/institutional access.

Engine R and EXP-015 remain paused.
