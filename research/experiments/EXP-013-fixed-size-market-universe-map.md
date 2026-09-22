# EXP-013 — Fixed-Size Market-Universe Economic Feasibility Map

**Status:** IN PROGRESS — RULES FROZEN BEFORE NEW MARKET RANKING RESULTS  

> **2026-09-22 sizing correction:** This experiment's FX ranking used 0.10 standard lot on each FX symbol. That was based on a misunderstanding of the user's intended "equivalent to 0.10 Gold" concept. The volatility statistics remain useful, but the FX dollar-capacity ranking and scanner-universe implication are **diagnostic only and not the forward selection rule**. Forward sizing must use symbol-specific P&L-equivalent lots for a normal ~USD 50 target, with explicit risk/margin gates.

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

## Checkpoint 1 — Existing five-market development-only economic map

**Status:** COMPLETE FOR XAUUSD / EURUSD / GBPUSD / USDJPY; XAGUSD VOLATILITY MEASURED BUT FIXED-SIZE ECONOMICS UNRANKED

Window:

- development only: 2026-03-12 through 2026-05-31;
- active-session volatility window: 06:00 <= UTC < 18:00;
- no strategy outcomes used for this ranking.

### XAUUSD — 0.10 lot / 10 oz research convention

Development data:

- 76,855 one-minute rows;
- 672 qualifying active-session hourly bars;
- 56 sufficiently covered active-session weekdays.

Hourly true range:

- median: **USD 21.445/oz**;
- 75th percentile: USD 31.720;
- 90th percentile: USD 46.119.

Active-session high-low range:

- median: **USD 86.145/oz**;
- 75th percentile: USD 100.512;
- 90th percentile: USD 143.440.

At 0.10 lot, median active-session gross movement capacity is approximately **USD 861** from session low to high. This is movement capacity, not achievable strategy P&L.

Target burden:

| Target | Required XAU move | / median hourly TR | / median session range |
|---|---:|---:|---:|
| USD 30 | USD 3 | 0.140x | 0.035x |
| USD 40 | USD 4 | 0.187x | 0.046x |
| USD 50 | USD 5 | 0.233x | 0.058x |
| USD 70 | USD 7 | 0.326x | 0.081x |
| USD 100 | USD 10 | 0.466x | 0.116x |

**Economic interpretation:** Gold is naturally compatible with the USD 30–100 fixed-size target ladder. The challenge is entry/stop quality, not insufficient raw movement.

### EURUSD — 0.10 standard lot

Development:

- 81,930 one-minute rows;
- median hourly TR: **13.65 pips**;
- median active-session range: **53.0 pips**;
- 75th / 90th session range: 62.7 / 77.18 pips.

At approximately USD 1/pip, median active-session gross movement capacity is about **USD 53** from low to high.

| Target | Required move | / median hourly TR | / median session range |
|---|---:|---:|---:|
| USD 30 | 30 pips | 2.198x | 0.566x |
| USD 40 | 40 pips | 2.930x | 0.755x |
| USD 50 | 50 pips | 3.663x | 0.943x |
| USD 70 | 70 pips | 5.128x | 1.321x |
| USD 100 | 100 pips | 7.326x | 1.887x |

### GBPUSD — 0.10 standard lot

Development:

- 81,912 one-minute rows;
- median hourly TR: **18.50 pips**;
- median active-session range: **70.60 pips**;
- 75th / 90th session range: 87.0 / 114.26 pips.

At approximately USD 1/pip, median active-session gross movement capacity is about **USD 70.60** from low to high.

| Target | Required move | / median hourly TR | / median session range |
|---|---:|---:|---:|
| USD 30 | 30 pips | 1.622x | 0.425x |
| USD 40 | 40 pips | 2.162x | 0.567x |
| USD 50 | 50 pips | 2.703x | 0.708x |
| USD 70 | 70 pips | 3.784x | 0.992x |
| USD 100 | 100 pips | 5.405x | 1.416x |

### USDJPY — 0.10 standard lot

Development median active price: approximately **159.014**.

At 0.10 lot, pip value is approximately 100 JPY/pip converted to USD at the contemporaneous USDJPY rate.

Development:

- 81,929 one-minute rows;
- median hourly TR: **16.30 pips**;
- median active-session range: **57.70 pips**;
- 75th / 90th session range: 79.0 / 106.62 pips;
- median active-session gross movement capacity: approximately **USD 36.29**.

| Target | Approx required move | / median hourly TR | / median session range |
|---|---:|---:|---:|
| USD 30 | 47.7 pips | 2.927x | 0.827x |
| USD 40 | 63.6 pips | 3.902x | 1.102x |
| USD 50 | 79.5 pips | 4.878x | 1.378x |
| USD 70 | 111.3 pips | 6.829x | 1.929x |
| USD 100 | 159.0 pips | 9.755x | 2.756x |

### XAGUSD — raw volatility only

Development:

- 76,910 one-minute rows;
- median hourly true range: **USD 0.7585/oz**;
- 75th / 90th hourly TR: USD 1.1155 / 1.5329;
- median active-session range: **USD 2.9675/oz**;
- 75th / 90th session range: USD 3.6232 / 4.6315.

**Ranking status:** UNRANKED.

Reason: no broker-specific or prospectively frozen fixed quantity/contract convention has yet been documented for Silver. EXP-013 forbids inventing a 0.10-lot equivalence after seeing volatility.

## Provisional economic ordering among ranked markets

This is a **movement-economics ranking only**, not a strategy ranking:

1. **XAUUSD** — by far the most natural USD 30–100 target ladder at the fixed reference size.
2. **GBPUSD** — strongest of the tested 0.10-lot FX majors.
3. **EURUSD** — USD 30–50 is possible on active days but requires a large fraction of the session move.
4. **USDJPY** — relatively poor fixed-size fit for USD 30–100 at 0.10 lot.

This ordering uses development-period economics only.

## Next checkpoint

Search for clean development-period 1m data for the predeclared priority additions:

- GBPJPY;
- EURJPY;
- AUDUSD;
- USDCAD;
- USDCHF.

Add only markets with documented data provenance. Do not substitute a different feed mid-ranking solely because a preferred pair is unavailable.

## Checkpoint 2 — Priority FX expansion

Matching public GetData 1m samples were located for:

- EURJPY — `getdata-finance/eurjpy-1m-ohlcv-forex-historical-data`;
- AUDUSD — `getdata-finance/audusd-1m-ohlcv-forex-historical-data`;
- USDCAD — `getdata-finance/usdcad-1m-ohlcv-forex-historical-data`;
- USDCHF — `getdata-finance/usdchf-1m-ohlcv-forex-historical-data`.

A matching GBPJPY sample was not found. GBPJPY remains deferred rather than introducing another feed mid-checkpoint.

All metrics below use development data only.

### EURJPY — 0.10 standard lot

JPY-quote P&L is converted using the development median USDJPY rate already frozen in Checkpoint 1 (about 159.014 JPY/USD).

- median hourly TR: **16.80 pips**;
- median active-session range: **61.50 pips**;
- 75th / 90th session range: 90.0 / 117.76 pips;
- approximate median active-session gross movement capacity: **USD 38.68**.

| Target | Approx required move | / median hourly TR | / median session range |
|---|---:|---:|---:|
| USD 30 | 47.7 pips | 2.840x | 0.776x |
| USD 40 | 63.6 pips | 3.786x | 1.034x |
| USD 50 | 79.5 pips | 4.733x | 1.293x |
| USD 70 | 111.3 pips | 6.626x | 1.810x |
| USD 100 | 159.0 pips | 9.465x | 2.586x |

### AUDUSD — 0.10 standard lot

At approximately USD 1/pip:

- median hourly TR: **12.60 pips**;
- median active-session range: **51.40 pips**;
- 75th / 90th session range: 62.7 / 73.42 pips;
- median active-session gross movement capacity: **USD 51.40**.

| Target | Required move | / median hourly TR | / median session range |
|---|---:|---:|---:|
| USD 30 | 30 pips | 2.381x | 0.584x |
| USD 40 | 40 pips | 3.175x | 0.778x |
| USD 50 | 50 pips | 3.968x | 0.973x |
| USD 70 | 70 pips | 5.556x | 1.362x |
| USD 100 | 100 pips | 7.937x | 1.946x |

### USDCAD — 0.10 standard lot

Development median active price: about **1.37031 CAD/USD**.

At 0.10 lot, one pip is approximately 1 CAD, converted to USD at the contemporaneous USDCAD rate.

- median hourly TR: **11.80 pips**;
- median active-session range: **42.50 pips**;
- 75th / 90th session range: 57.2 / 68.8 pips;
- approximate median active-session gross movement capacity: **USD 31.01**.

| Target | Approx required move | / median hourly TR | / median session range |
|---|---:|---:|---:|
| USD 30 | 41.1 pips | 3.484x | 0.967x |
| USD 40 | 54.8 pips | 4.645x | 1.290x |
| USD 50 | 68.5 pips | 5.806x | 1.612x |
| USD 70 | 95.9 pips | 8.129x | 2.257x |
| USD 100 | 137.0 pips | 11.613x | 3.224x |

### USDCHF — 0.10 standard lot

Development median active price: about **0.77843 CHF/USD**.

At 0.10 lot, one pip is approximately 1 CHF, converted to USD at the contemporaneous USDCHF rate.

- median hourly TR: **11.20 pips**;
- median active-session range: **42.90 pips**;
- 75th / 90th session range: 52.2 / 64.72 pips;
- approximate median active-session gross movement capacity: **USD 55.11**.

| Target | Approx required move | / median hourly TR | / median session range |
|---|---:|---:|---:|
| USD 30 | 23.4 pips | 2.085x | 0.544x |
| USD 40 | 31.1 pips | 2.780x | 0.726x |
| USD 50 | 38.9 pips | 3.475x | 0.907x |
| USD 70 | 54.5 pips | 4.865x | 1.270x |
| USD 100 | 77.8 pips | 6.950x | 1.815x |

## Updated development-only movement-economics ordering

This ranking describes **natural fixed-size movement capacity**, not strategy profitability.

Using T30/T50 burden, session capacity, and common data quality:

1. **XAUUSD** — dominant economic fit for USD 30–100 at the reference size.
2. **GBPUSD** — strongest ranked FX market.
3. **USDCHF** — favorable USD pip conversion makes USD 30–50 more natural than its raw pip range alone suggests.
4. **EURUSD** — reasonable USD 30 target; USD 50 consumes almost the full median session range.
5. **AUDUSD** — similar to EURUSD but slightly higher target burden.
6. **EURJPY** — better than USDJPY but USD 50 still exceeds the median session range.
7. **USDJPY** — weak fixed-size fit above USD 30.
8. **USDCAD** — weakest of the ranked 0.10-lot FX markets for the desired ladder.

**XAGUSD remains unranked** pending a frozen quantity/contract convention.

**GBPJPY remains deferred** because the matching source was unavailable.

## Scanner-universe implication

For the first target-first ranking model, the economically strongest currently documented universe is:

- XAUUSD as the core market;
- GBPUSD;
- USDCHF;
- EURUSD;
- AUDUSD.

EURJPY / USDJPY / USDCAD may remain visible to the scanner later, but they are lower priority for USD 30–50 at 0.10 lot.

This is a development-only economic selection. No new strategy outcomes have been inspected for USDCHF/AUDUSD in making this selection.

## Next action

Freeze a first scanner universe and define the target-first opportunity-ranking experiment before inspecting its holdout outcomes.

The first ranking experiment should prioritize:

1. XAUUSD;
2. GBPUSD;
3. USDCHF;
4. EURUSD;
5. AUDUSD.

The model must estimate target-rung probabilities and enforce fixed-size structural-risk gates rather than taking every generated signal.

