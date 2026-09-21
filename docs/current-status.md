# Current Status

**Date:** 2026-09-22  
**Phase:** Strategy research / opportunity-engine discovery

## Source of truth

Only this repository and the originating chat are authorized project context.

## Completed

### Badar Tanveer video analysis

Enough direct video evidence was obtained to define an initial mechanical setup family:

liquidity -> sweep -> internal MSS -> displacement -> FVG -> retracement entry -> structural stop -> liquidity/target expansion.

The videos also support:

- XAUUSD focus;
- lower-timeframe execution;
- variable reward/risk rather than universal 1:9;
- partial profit taking;
- session/news awareness.

### Engine A screen

A mechanical Badar-inspired setup was tested on XAUUSD one-minute data from 2026-03-01 through 2026-08-20.

High-level result:

- simplified expectancy remained positive in the later holdout;
- USD 5 favorable target-first hit rate was only about 27% in holdout;
- typical favorable excursion was closer to USD 3;
- daily USD 0–50 outcomes remained far too frequent.

Conclusion: **Engine A is a candidate generator, not a complete daily-income solution.**

### Engine B / C first formulations

- Engine B: momentum breakout -> retest -> continuation.
- Engine C: trend pullback -> continuation.

Strict definitions produced too few trades; looser definitions did not justify promotion on holdout.

Conclusion: **reject these first formulations rather than overfit them.**

## Current next tests

1. session/opening-range momentum;
2. volatility compression -> expansion;
3. compare each strategy on the same development/holdout framework;
4. record results immediately in GitHub;
5. if one survives, combine it with Engine A and test portfolio daily distribution;
6. later expand to additional markets rather than forcing more XAU trades.

## Data work

Dukascopy remains the current baseline.

Independent finalist validation should use at least one of:

- broker/MT5 history;
- OANDA where suitable;
- Twelve Data where suitable.

## Key unresolved question

Can multiple independent engines and markets reduce <= USD 50 days toward roughly 20% **without** unacceptable loss frequency, leverage, drawdown, or forced trades?
