# Current Status

**Date:** 2026-09-22  
**Phase:** Strategy research / multi-asset expansion

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

### Engine A

Badar-inspired liquidity/MSS/FVG setup.

Result:

- simplified expectancy remained positive in the later holdout;
- USD 5 target-first hit rate was only about 27% in holdout;
- typical favorable excursion was closer to USD 3;
- daily USD 0–50 outcomes remained far too frequent.

Status: **retain as a research lead / candidate generator only.**

### Engine B / C

- Engine B: momentum breakout -> retest -> continuation.
- Engine C: trend pullback -> continuation.

Status: **first formulations rejected**.

Strict rules were too sparse; loosening them did not justify promotion on holdout.

### Engine D

Session/opening-range momentum.

Result:

- balanced version weakly positive but sparse and far below the daily-output target;
- loose version turned negative on holdout;
- strict version showed an attractive tiny holdout sample but essentially flat development;
- NY-only result did not generalize.

Status: **current formulations not promoted**.

See EXP-004.

### Engine E

Volatility compression -> expansion.

Result:

- strict formulations were too sparse;
- balanced formulation turned approximately flat/negative in holdout;
- loose high-frequency version eliminated zero-signal days but produced about 59% losing days and about 88% <= USD 50 days on holdout.

Status: **current formulations not promoted**.

See EXP-005.

## Current conclusion

More XAUUSD signals do not automatically improve the objective.

The evidence so far suggests that the next useful direction is **multi-asset opportunity expansion**, not progressively looser XAU-only rules.

## Next action

1. identify reliable intraday data for additional liquid markets;
2. prioritize markets where a USD 50 profit unit can be normalized cleanly;
3. freeze one or more existing strategy families before applying them cross-market;
4. test each market on development/holdout splits;
5. combine only positive-expectancy, sufficiently independent streams;
6. evaluate portfolio daily distribution under the USD 40 / USD 60 loss framework and USD 150–200 profit stop;
7. cross-validate finalists on an independent data feed.

## Candidate market universe

Initial candidates from this chat:

- XAUUSD;
- XAGUSD;
- EURUSD;
- GBPUSD;
- USDJPY;
- GBPJPY;
- NAS100 / USTEC;
- US30;
- US500 / SPX500;
- BTCUSD / BTCUSDT where appropriate.

## Key unresolved question

Can multiple independent engines and markets reduce <= USD 50 days toward roughly 20% **without** unacceptable loss frequency, leverage, drawdown, or forced trades?
