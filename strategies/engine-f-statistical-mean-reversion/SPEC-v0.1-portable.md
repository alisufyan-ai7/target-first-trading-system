# Engine F v0.1 Portable Specification — Statistical Extension / Re-entry / Mean Reversion

**Status:** FROZEN FOR EXP-009 BEFORE OUTCOME INSPECTION  
**Version:** 0.1-portable  
**Frozen:** 2026-09-22

## Purpose

Test a genuinely independent intraday strategy family after pausing Engine A expansion.

Engine F does **not** use:

- liquidity sweeps;
- MSS/FVG logic;
- breakout-retest continuation;
- trend-pullback continuation;
- opening-range momentum;
- volatility-compression breakout.

It is a price-only statistical mean-reversion engine.

## Input

- one-minute OHLC data in UTC;
- 5m bars resampled on UTC 5-minute boundaries;
- active signal/entry window: 06:00 <= UTC < 18:00;
- no volume input.

## Rolling reference

On completed 5m bars calculate, using only prior/current completed bars:

- rolling mean of close over the latest 12 completed 5m bars (60 minutes);
- rolling population standard deviation of close over the same 12 bars;
- z-score = (close - rolling mean) / rolling standard deviation;
- ATR(14) on completed 5m bars using standard true range.

Require at least 14 completed 5m bars before a signal is eligible.

## Extension event

Upper extension:

- a completed 5m close has z-score >= +2.0.

Lower extension:

- a completed 5m close has z-score <= -2.0.

Once an extension begins, track the most extreme 5m high/low reached before re-entry.

## Re-entry confirmation

After an extension event, allow at most the next 6 completed 5m bars (30 minutes) for re-entry.

Short candidate after upper extension:

- first completed 5m bar whose z-score is <= +1.5.

Long candidate after lower extension:

- first completed 5m bar whose z-score is >= -1.5.

If no qualifying re-entry occurs within 30 minutes, expire the setup.

A new extension in the same direction while the setup is active updates the tracked excursion extreme but does not create a second setup.

## Entry

Enter at the open of the first 1m bar immediately after the confirming 5m re-entry bar.

Only one Engine F trade per instrument may be open at a time.

After an Engine F trade closes or times out, no new Engine F setup is allowed until either:

- the 5m z-score crosses 0; or
- 60 minutes have elapsed,

whichever occurs first.

## Structural/statistical invalidation stop

Short trade:

- stop = highest 5m high observed from the first upper-extension bar through the re-entry bar
  + 0.25 x ATR(14) measured at the re-entry close.

Long trade:

- stop = lowest 5m low observed from the first lower-extension bar through the re-entry bar
  - 0.25 x ATR(14) measured at the re-entry close.

Reject the setup if the stop is not on the invalidation side of entry.

No stop compression is allowed.

## Risk and target normalization

Reference starting equity: USD 500.

For EXP-009:

- gross risk at structural stop = USD 20 per trade;
- gross profit target = USD 50;
- required favorable move = +2.5R.

A setup is eligible only if the rolling 60-minute mean at the re-entry close lies at least +2.5R from entry in the reversion direction. This prevents a nominal mean-reversion trade from requiring a target beyond its statistical reference mean.

Position size is derived from the structural stop distance and instrument economics.

No martingale, loss-recovery sizing, or size increase after losses.

## Outcome handling

For each filled trade:

- win if +2.5R is reached before stop;
- loss if stop is reached first;
- if stop and target are both touched in the same 1m bar, count stop first;
- if entry and stop are both touched on the entry bar, count stop;
- unresolved trades are marked to the 20:00 UTC close/last available bar of the day;
- timeout P&L is capped between -1R and +2.5R.

## Development / holdout

Use the same common public-sample split already documented for EXP-006/007/008:

- development: 2026-03-12 through 2026-05-31;
- holdout: 2026-06-01 through 2026-08-20.

No parameter may be changed after any EXP-009 outcome is inspected.

## Market test order

To preserve small checkpoints:

1. XAUUSD first;
2. USDJPY second only after the XAUUSD checkpoint is recorded;
3. EURUSD and GBPUSD only after the prior checkpoints are recorded.

The rules stay unchanged across markets.

## Metrics

Per market and split record:

- extension events;
- qualifying re-entries;
- filled/accepted trades;
- 2.5R target-first win rate;
- mean and median R/trade;
- timeout rate;
- median stop distance;
- median position size;
- median notional/equity where calculable;
- trades/day including zero-signal weekdays;
- losing-day percentage;
- <= USD 50 day percentage;
- >= USD 100 day percentage;
- >= USD 150 day percentage;
- maximum drawdown;
- maximum consecutive losing days;
- maximum consecutive <= USD 50 days.

No portfolio combination is permitted until the market-level holdout evidence is reviewed.
