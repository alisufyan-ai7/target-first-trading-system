# EXP-013 — Fixed-Size Market-Universe Economic Feasibility Map

**Status:** IN PROGRESS — RULES FROZEN BEFORE NEW MARKET RANKING RESULTS  
**Date:** 2026-09-22

## Purpose

Identify which liquid markets naturally provide enough intraday movement at a fixed, economically sensible execution size to support the user's target ladder:

- approximately USD 30;
- USD 40;
- USD 50;
- USD 70;
- USD 100+.

This experiment is **not** a strategy backtest. It is an economic/volatility screen used to decide which markets deserve inclusion in the first cross-market opportunity scanner.

## Why this experiment is necessary

EXP-012 established that:

- Gold at 0.10 lot has the correct dollar-movement scale;
- USDJPY and GBPUSD at 0.10 lot usually produced only a few dollars of favorable movement from the retained entry families;
- dynamically increasing position size to manufacture USD 50 created unacceptable notional/margin exposure.

Therefore the scanner should prioritize markets where useful dollar moves are natural at fixed size rather than compensating for small moves with leverage.

## Data discipline

Use development-period data only for market-economic ranking.

Target common development window where available:

- 2026-03-12 through 2026-05-31.

Holdout strategy outcomes must not be used to decide which markets are economically attractive.

External public data may be used only as documented research data and does not become project context unless findings are checkpointed here.

## Fixed execution-size conventions

### XAUUSD

- reference size: 0.10 lot;
- research convention: 10 oz until broker verification.

### Major FX

- initial research size: 0.10 standard lot = 10,000 base units;
- USD-quote pip value ≈ USD 1/pip;
- JPY-quote pip value must be converted through contemporaneous USDJPY.

### XAGUSD / indices / crypto / other CFDs

Do not assume that 0.10 lot has comparable economics.

Before ranking, record:

- contract size;
- tick size;
- tick value;
- quote currency;
- fixed research size;
- approximate notional;
- margin implications where known.

If reliable contract economics are not available, keep the market unranked rather than inventing a lot equivalence.

## Initial universe

Already documented / available in project research:

- XAUUSD;
- XAGUSD;
- EURUSD;
- GBPUSD;
- USDJPY.

Priority expansion candidates:

- GBPJPY;
- EURJPY;
- AUDUSD;
- USDCAD;
- USDCHF.

Second wave after venue/contract specification is documented:

- NAS100 / USTEC;
- US30;
- US500 / SPX500;
- BTCUSD / BTCUSDT.

## Development-only volatility metrics

For each market:

1. resample 1m data to 1h bars;
2. restrict to 06:00 <= UTC < 18:00 for comparability with prior research;
3. require sufficient 1m coverage for the hour;
4. calculate hourly true range;
5. record:
   - median hourly true range;
   - 75th percentile;
   - 90th percentile;
   - median active-session high-low range per weekday;
   - 75th and 90th percentile active-session range.

## Dollar-movement translation

At the fixed research size, translate each volatility metric into gross USD P&L.

Also calculate the native move required for:

- T30;
- T40;
- T50;
- T70;
- T100.

For each target rung calculate a **movement burden**:

`required target move / development median hourly true range`.

Also calculate the same burden relative to median active-session range.

Lower burden means the target is more natural at the fixed-size tier.

## Ranking rule

Do not create an arbitrary pass/fail cutoff after seeing results.

Rank markets descriptively on:

1. T30 movement burden;
2. T50 movement burden;
3. T100 movement burden;
4. median active-session USD range;
5. liquidity/data quality;
6. fixed-size notional/margin practicality.

The first scanner universe will be chosen prospectively from this development-only ranking and documented before any new strategy outcome test.

## Important limitation

High natural volatility does **not** imply a profitable trade.

This experiment only answers:

> Is the market economically capable of producing the desired fixed-size dollar movement often enough to justify scanning?

Entry quality and target-first probability are a separate problem for the next experiment.

## Deliverables

Checkpoint:

- data source per instrument;
- date coverage;
- fixed-size convention;
- target price/pip distances;
- hourly/session volatility statistics;
- target burdens;
- provisional scanner-priority ordering;
- markets excluded due missing/unsafe contract economics.

## Immediate next action

1. compute the existing five-market map first;
2. checkpoint it;
3. add the priority FX crosses/majors only where clean 1m data are available;
4. checkpoint again;
5. freeze the first scanner universe before building the target-first ranker.
