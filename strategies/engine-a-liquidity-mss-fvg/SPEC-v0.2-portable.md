# Engine A v0.2 Portable Specification — Liquidity Sweep / MSS / FVG

**Status:** FROZEN FOR EXP-007 CROSS-MARKET SCREEN  
**Version:** 0.2-portable  
**Frozen:** 2026-09-22

## Purpose

Create a fully mechanical, prospective version of the retained Engine A family that can be applied unchanged to XAUUSD, EURUSD, GBPUSD, and USDJPY.

This is **not** claimed to reproduce the exact unpublished implementation used in EXP-002. The repository only preserved approximate Engine A parameters. Version 0.2 therefore freezes missing mechanics prospectively before cross-market outcome inspection.

## Input

- one-minute OHLC data in UTC;
- 5m bars resampled on UTC 5-minute boundaries;
- active setup/entry window: 06:00 <= UTC < 18:00.

## 5m liquidity swing

A 5m swing high at bar `t` is confirmed only after two later 5m bars exist and:

- `high[t] > high[t-1]`;
- `high[t] > high[t-2]`;
- `high[t] >= high[t+1]`;
- `high[t] >= high[t+2]`.

A swing low is the mirror image.

The swing becomes eligible only when confirmed at `t+2`, avoiding future-looking use.

For each side, use the most recent confirmed swing no older than 24 completed 5m bars (2 hours).

## Sweep

Bearish candidate:

- a completed 5m bar trades above the eligible swing high; and
- that 5m bar closes back below the swing high.

Bullish candidate:

- a completed 5m bar trades below the eligible swing low; and
- that 5m bar closes back above the swing low.

The sweep extreme is the high/low of the sweeping 5m bar.

## 1m internal structure / MSS

At the close of the sweeping 5m bar, identify the most recent **confirmed** 1m swing on the opposite side using the same 2-left / 2-right pivot rule.

The internal swing must:

- already be confirmed by sweep close;
- have occurred within the prior 15 minutes.

Bearish MSS:

- within the next 10 completed 1m bars, a 1m candle must close below the internal swing low.

Bullish MSS:

- within the next 10 completed 1m bars, a 1m candle must close above the internal swing high.

## Displacement

The MSS candle must be directional and have absolute real body:

`>= 1.6 x mean absolute real body of the prior 20 completed 1m candles`.

The signal candle itself is excluded from the baseline.

## FVG

Use a standard three-candle imbalance.

Bullish FVG at bar `j`:

`low[j] > high[j-2]`

Bearish FVG at bar `j`:

`high[j] < low[j-2]`

After a valid MSS/displacement candle, accept the **first** same-direction FVG whose third candle is:

- the MSS candle itself; or
- one of the next two completed 1m candles.

No asset-specific minimum gap size is used in EXP-007.

## Entry

Entry price = midpoint of the FVG.

After the FVG is confirmed, wait at most 10 completed 1m bars for price to retrace to the midpoint.

If not filled within 10 bars, the setup expires.

Only one open Engine A trade per instrument is allowed. New candidates while an Engine A trade is open are ignored.

## Structural stop

Bearish trade stop = sweep 5m high.

Bullish trade stop = sweep 5m low.

The stop must remain on the invalidation side of the entry. Otherwise reject the setup.

No arbitrary stop compression is allowed.

## Risk and target normalization

Reference starting equity remains USD 500.

For EXP-007:

- gross risk at structural stop = USD 20 per trade;
- gross profit target = USD 50;
- therefore required favorable move = 2.5 x structural stop distance.

Position size is derived from the structural stop distance and instrument economics.

This rule is frozen before cross-market outcome inspection.

### FX sizing

For EURUSD and GBPUSD (USD quote):

`base units ~= 20 / stop_price_distance`.

For USDJPY:

`USD base units ~= 20 x entry_USDJPY / stop_price_distance`.

Exact broker-specific conversion will be required later.

### XAUUSD sizing

`ounces ~= 20 / stop_USD_per_oz`.

Broker lot conversion is not assumed in this screen.

## Outcome handling

For each filled trade:

- target-first win if +2.5R is reached before stop;
- stop loss if stop is reached first;
- if target and stop are both touched in the same 1m bar after entry, count the stop first;
- if entry and stop are both touched on the fill bar, count the stop;
- unresolved trades are closed at 20:00 UTC on the entry day, or at the last available bar of that day if earlier;
- timeout P&L is marked to the 20:00/last-bar close and capped between -1R and +2.5R.

For XAUUSD only, also report the legacy diagnostic:

- does a fixed USD 5 favorable move occur before structural stop?

## Data split for EXP-007

Common public-sample window:

- development: 2026-03-12 through 2026-05-31;
- holdout: 2026-06-01 through 2026-08-20.

No parameters may be changed after holdout results are inspected.

## Metrics

Per market and split:

- signals/candidates;
- filled trades;
- target-first win rate at 2.5R;
- mean R/trade;
- median R/trade;
- timeout rate;
- median structural stop distance;
- median position units / ounces;
- median notional/equity ratio where calculable;
- trades/day including zero-signal weekdays;
- losing-day percentage;
- <= USD 50 day percentage;
- >= USD 100 day percentage;
- >= USD 150 day percentage;
- max drawdown in USD under fixed USD 20 risk;
- max consecutive losing days;
- max consecutive <= USD 50 days.

No portfolio combination is allowed until per-market holdout evidence is reviewed.
