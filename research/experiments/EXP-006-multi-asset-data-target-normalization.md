# EXP-006 — Multi-Asset Data and Target-Normalization Checkpoint

**Status:** IN PROGRESS  
**Date:** 2026-09-22

## Purpose

Prepare the first multi-asset expansion test without changing strategy quality thresholds or contaminating holdout data.

This experiment is a prerequisite to the first cross-market strategy screen.

## Question

Can we define a small set of liquid non-Gold markets with:

1. reliable one-minute intraday data over the same baseline window used in prior XAUUSD experiments;
2. clean instrument economics for translating a favorable price move into an approximately USD 50 profit unit;
3. target distances calibrated from development data only, so later holdout testing remains untouched?

## Initial market set

First-wave candidates:

- EURUSD;
- GBPUSD;
- USDJPY.

Reference comparator:

- XAUUSD.

XAGUSD, equity-index CFDs, and crypto remain candidates for later waves, but are excluded from this first checkpoint until their contract/tick conventions and data-source mapping are documented cleanly enough for comparable sizing.

## Data window and split

Target baseline window, matching prior experiments where available:

- full range: 2026-03-01 through 2026-08-20;
- development/calibration: 2026-03-01 through 2026-05-31;
- untouched holdout: 2026-06-01 through 2026-08-20.

Preferred baseline source for this checkpoint: Dukascopy one-minute data where available.

No strategy-result inspection on the holdout is permitted during target calibration.

## Normalization method to freeze before strategy testing

The Gold reference remains a USD 5 favorable XAUUSD move.

For each non-Gold instrument:

1. use development data only to estimate intraday volatility in native price/pip units;
2. measure the Gold USD 5 target as a volatility burden on the XAUUSD development sample;
3. map that same burden to each candidate market to obtain a frozen favorable target distance;
4. translate that target distance into a position size that would produce approximately USD 50 gross P&L using the instrument's contract/tick economics;
5. reject or cap any setup whose structurally valid stop would breach the project trade/day risk framework at the required size.

For USDJPY, USD P&L conversion must use the relevant JPY/USD conversion rather than assuming a fixed USD pip value.

## Strategy to be used after this checkpoint

Engine A is the first cross-market transfer candidate because it is the only existing engine retained as a research lead.

The transferable rules will remain frozen from the existing specification:

- recent 5m swing liquidity;
- wick/sweep beyond the level and close back inside;
- 1m internal MSS close;
- displacement threshold approximately 1.6x recent average 1m candle body;
- three-candle FVG;
- entry near FVG midpoint;
- structural/FVG invalidation stop;
- active window approximately 06:00–18:00 UTC.

Only instrument-native target distance and position-size translation may differ.

## Deliverables

Before proceeding to the cross-market holdout screen, record:

- exact data source and retrieval method for each instrument;
- bar count and missing-data checks;
- development-period volatility metrics;
- frozen target distance per instrument;
- assumed contract/tick economics;
- position size corresponding to approximately USD 50 gross target;
- limitations and any markets rejected before testing.

## Promotion rule

EXP-006 does not promote a strategy.

It only authorizes a market for the next experiment if the data and normalization are sufficiently clean to support an unchanged cross-market Engine A test.

## Next action

Collect and audit the first-wave datasets and freeze the target/position-size mapping. Then checkpoint the result before starting the cross-market strategy performance test.
