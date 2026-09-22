# Timeframe and Market Context

_Last updated: 2026-09-22_

## What “context” means

“15-minute context” or “5-minute context” does **not** mean looking at one previous candle.

Context is a rolling structural map plus persistent important levels.

## Working multi-timeframe interpretation

~~~text
15m:
Where are we in the larger market?

5m:
What is price doing at that important location?

3m / 1m:
Has the actual execution trigger occurred?
~~~

The final timeframe combination must be selected by evidence, not assumption.

## Initial research lookbacks

Conversation-level starting ranges, not final production parameters:

- 15m context: roughly 32–64 recent candles;
- 5m structure: roughly 36–72 recent candles;
- 3m / 1m execution: enough recent bars to establish internal swings, MSS, displacement, and entry refinement.

Important market levels may remain relevant even when older than the rolling window.

## Persistent levels

Examples:

- previous-day high/low;
- Asian session high/low;
- London session high/low;
- New York session high/low;
- major confirmed swing highs/lows;
- equal highs/lows / liquidity clusters;
- important unfilled FVGs;
- relevant order blocks / POIs.

## Example short workflow

~~~text
15m:
price approaches important buy-side liquidity / premium location

5m:
liquidity is attacked or swept

3m / 1m:
internal MSS
    ->
bearish displacement
    ->
bearish FVG
    ->
retracement / entry
~~~

The 15m chart does not itself force a short. It provides location/context.

## Target-path use

Even if a 1m entry trigger is valid, larger context can reject the trade.

Example:

- XAU sell entry around 4505;
- desired normal target around 4500;
- major 15m support at 4502.

The setup may be technically valid, but the system should recognize that a full USD 5 move has poor structural room and either use a justified nearer target or reject the trade.

## Timeframe experiments

Possible combinations should be tested rather than assumed:

- 15m -> 5m -> 1m;
- 15m -> 5m -> 3m;
- 15m -> 3m -> 1m;
- 5m -> 1m.

Evaluation should include signal frequency, target-first hit rate, false MSS rate, stop width, MFE/MAE, daily P&L distribution, and low-output days.

## Higher-timeframe BOS versus lower-timeframe MSS

Working interpretation:

- BOS can characterize higher-timeframe directional/structural context;
- MSS is the lower-timeframe reversal/entry confirmation after the liquidity event.

Do not collapse both into the same generic structure break without testing.
