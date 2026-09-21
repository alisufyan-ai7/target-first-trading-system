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

The evidence so far supports **multi-asset opportunity expansion**, not progressively looser XAU-only rules.

EXP-006 completed the first cross-market data/economics checkpoint using an independent public 1m sample feed for XAUUSD, EURUSD, GBPUSD, and USDJPY. The data are usable for a provisional common-window screen, but matching Gold's USD 5 target as the same fraction of median hourly volatility implied only about 3–4 pip FX targets and roughly 1.2–2.1 standard lots to gross about USD 50. That sizing is too aggressive for the reference USD 500 account and will not be used as the portfolio-economic rule.

## EXP-007 partial result

Engine A v0.2-portable has been frozen prospectively. Its XAUUSD checkpoint failed under the USD 20 structural-risk / USD 50 target rule: holdout produced 133 trades, an 18.8% 2.5R target-first rate, about -0.305R/trade, 66.1% losing days, and 96.6% <= USD 50 days. EURUSD showed +0.167R/trade and a 31.25% holdout hit rate, but development expectancy was negative, 88.1% of holdout days remained <= USD 50, and median notional/equity was about 139x. Neither arm is promoted and the frozen rules will not be retuned. GBPUSD then showed the reverse instability: +0.139R/trade in development but -0.111R/trade in holdout, with 94.9% <= USD 50 days and median notional/equity about 118x. GBPUSD is also not promoted.

## Next action

1. continue the frozen Engine A v0.2 rules unchanged on EURUSD, GBPUSD, and USDJPY;
2. checkpoint each market before testing the next;
3. test each market on the common March 12–August 20 window with development/holdout separation;
4. report notional/equity and margin-feasibility diagnostics alongside target-first statistics;
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
