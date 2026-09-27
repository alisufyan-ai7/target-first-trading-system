# EXP-043 Development Microstructure Snapshot v0.1

**Frozen:** 2026-09-27  
**Type:** zero-outcome full-development acquisition + deterministic microstructure aggregation  
**Prerequisite:** source preflight PASS at `babcfa8178ebf9288cefc420dab916674a59b55b`

## 1. Objective

Freeze a compact, immutable development-only broker quote/tick microstructure dataset for the eight target markets.

The scientific purpose is to preserve information unavailable in M1/M5 OHLC:

- spread state;
- quote-update intensity;
- quote inter-arrival activity;
- quote freshness;
- quote-side size/imbalance.

Do not store or derive mid-price OHLC or return features in this snapshot.

## 2. Source

Pinned transport:

`dukascopy-node@1.50.0`

Timeframe:

`tick`

Markets:

- XAUUSD;
- EURUSD;
- GBPUSD;
- USDJPY;
- EURJPY;
- AUDUSD;
- USDCAD;
- USDCHF.

Canonical raw tick fields used for provenance:

`timestamp_ms,ask_price,bid_price,ask_volume,bid_volume`.

Scientific semantics remain broker quote/tick microstructure, not centralized traded order flow.

## 3. Frozen development interval

Calendar interval:

`2025-07-01 <= date < 2026-06-30`

Acquire weekdays only.

Per weekday acquisition window:

`05:00:00 UTC <= tick < 18:00:00 UTC`.

Rationale:

- structural decision grid begins 06:05 UTC;
- acquisition provides 65 minutes of pre-grid warmup;
- structural decision grid ends 17:55 UTC;
- no protected Jul-Aug/Sep 2026 dates are requested.

## 4. Per-day raw provenance

For every market/weekday request, retain in a manifest:

- market;
- date;
- request start/end UTC;
- canonical raw tick count;
- canonical raw SHA-256;
- first raw tick timestamp;
- last raw tick timestamp;
- no-data flag.

Canonical raw SHA is computed over source rows after exact request-window filtering using:

`timestamp_ms,ask_price,bid_price,ask_volume,bid_volume\n`

in source order.

Raw tick CSVs are transient and are not required in the frozen release.

## 5. Minute aggregation

Aggregate ticks by UTC minute bucket.

For a minute `m`, only ticks satisfying:

`m <= tick < m + 1 minute`

belong to that row.

Stored columns:

- `minute_start_utc`;
- `tick_count`;
- `distinct_timestamp_count`;
- `median_interarrival_ms`;
- `p90_interarrival_ms`;
- `spread_bps_median`;
- `spread_bps_p90`;
- `spread_bps_last`;
- `last_quote_age_ms`;
- `bid_update_count`;
- `ask_update_count`;
- `both_price_update_count`;
- `bid_volume_median`;
- `ask_volume_median`;
- `signed_quote_imbalance_mean`;
- `signed_quote_imbalance_median`;
- `bid_heavy_fraction`;
- `ask_heavy_fraction`.

Definitions:

`mid = (ask + bid) / 2`

`spread_bps = 10000 * (ask - bid) / mid`

`signed_quote_imbalance = (bid_volume - ask_volume) / (bid_volume + ask_volume)`

when denominator >0.

`bid_heavy_fraction` = fraction of valid imbalance observations >0.

`ask_heavy_fraction` = fraction <0.

Price update counts compare consecutive ticks **within the same minute**. The first tick of each minute has no predecessor.

`last_quote_age_ms = minute_end_ms - timestamp_of_last_tick_in_minute`.

No cross-minute forward fill occurs.

## 6. Quantiles

Median and p90 use deterministic linear interpolation on sorted finite observations.

If a minute has fewer than two inter-arrival observations, inter-arrival quantiles are stored as null.

## 7. Frozen release

Release tag:

`exp043-quote-microstructure-1m-2025-07-01_2026-06-30-v1`

Asset:

`exp043-quote-microstructure-1m-2025-07-01_2026-06-30-v1.tar.gz`

Release contents:

- one aggregate CSV per market;
- one global provenance manifest;
- one acquisition-result JSON.

The archive must be deterministic.

## 8. Integrity gate

For each market require:

- >=230 source weekdays with positive tick count;
- >=120,000 aggregate minute rows;
- >=2,000,000 raw source ticks across the frozen windows;
- aggregate minute timestamps strictly increasing and unique;
- all aggregate rows on weekdays;
- all aggregate rows between 05:00 and 17:59 UTC;
- tick_count >=1;
- distinct_timestamp_count >=1 and <= tick_count;
- spread metrics finite and nonnegative;
- last_quote_age_ms in [0,60000];
- update counts >=0 and <= tick_count-1;
- quote volumes finite and nonnegative;
- signed imbalance values within [-1,1];
- heavy-side fractions within [0,1];
- no protected-period rows.

Global require:

- all eight markets pass;
- requested weekday set derives only from the frozen development calendar;
- no target/path labels, model probabilities or P&L computed.

## 9. PASS disposition

`EXP043_DEVELOPMENT_MICROSTRUCTURE_SNAPSHOT_FROZEN`

PASS authorizes a prospectively frozen information-content design using the immutable minute-level microstructure snapshot.

## 10. FAIL disposition

`EXP043_DEVELOPMENT_MICROSTRUCTURE_SNAPSHOT_FAILED`

Do not begin predictive modeling on a failed snapshot.

## 11. Next study after PASS

The next study should be nested and minimal:

`LOCAL_M5 -> +EXECUTION_COST_STATE -> +PARTICIPATION_STATE -> +QUOTE_IMBALANCE_STATE`.

Any rolling normalization/window definitions must be frozen before target outcomes from EXP-043 are inspected.

Engine R and EXP-015 remain paused.
