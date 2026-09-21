# Engine A Specification — Liquidity Sweep / MSS / FVG

**Status:** RESEARCH LEAD  
**Version:** 0.1-chat-screen

## Purpose

Generate reversal/expansion candidates from liquidity sweeps followed by lower-timeframe structural confirmation.

## Initial bearish logic

1. identify a recent 5m swing high acting as candidate buy-side liquidity;
2. require price to trade above it and close back below;
3. after the sweep, identify recent internal 1m swing low;
4. require a 1m candle close below the internal low;
5. require directional displacement relative to recent candle bodies;
6. require a bearish three-candle FVG;
7. wait for retracement toward the FVG;
8. enter short using the selected FVG entry rule;
9. stop at structural/FVG invalidation;
10. evaluate whether the favorable target is reached before the stop.

Bullish logic is mirrored.

## Current research parameters

The first useful screen used approximately:

- 5m liquidity swings;
- 1m execution;
- MSS close required;
- displacement threshold about 1.6x recent average 1m candle body;
- FVG minimum/filtering;
- entry near FVG midpoint;
- active session approximately 06:00–18:00 UTC;
- USD 5 favorable XAU target.

These are not final production parameters.

## Status

Positive simplified expectancy in the first six-month screen, but insufficient daily consistency.

Do not promote to live trading.
