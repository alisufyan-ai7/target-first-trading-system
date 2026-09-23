# EXP-022 Wave-1 Data Provenance Manifest

**Frozen:** 2026-09-23  
**Purpose:** Engine K v0.1 multi-market direct target-move scanner  
**External role:** research-data transport only; these repositories are not project context

## Important rolling-sample rule

The GetData GitHub samples update weekly and their six-month window rolls forward.

Engine K v0.1 must therefore fetch the exact **pinned commits below**, never `main`, so later weekly updates cannot alter the experiment.

Current common sample coverage reported by the pinned repositories:

- approximately 2026-03-23 through 2026-09-23;
- 2026-09-23 is potentially a partial current UTC day and is excluded from all model evaluation.

## Frozen Wave-1 sources

| Symbol | External repository | Frozen commit | CSV blob SHA | Reported sample rows | Reported coverage |
|---|---|---|---|---:|---|
| XAUUSD | getdata-finance/xauusd-1m-ohlcv-metals-historical-data | 8b1cea156045bda7aefa2245d202cf0a8fd04bb1 | 8ff56a9776ab68d2aad4f2ef5d039874603a06e2 | 179,921 | 2026-03-23 -> 2026-09-23 |
| EURUSD | getdata-finance/eurusd-1m-ohlcv-forex-historical-data | d7c7be3ebabea6829ac0828ff0fe14c2e567e1e3 | a3b314549440faabf0f6ef3051087a6ba72582b5 | 189,940 | 2026-03-23 -> 2026-09-23 |
| GBPUSD | getdata-finance/gbpusd-1m-ohlcv-forex-historical-data | 2ff10e3bfd0160a93afe6c867158083e07d966d6 | c08632a8c65e358efcb0146a2ab27084ef12b75a | 189,876 | 2026-03-23 -> 2026-09-23 |
| USDJPY | getdata-finance/usdjpy-1m-ohlcv-forex-historical-data | ff31183928d89096d08cd3cf32316d3b42397bcb | acd5f7e96c69a69f1193ae9c95fbfc6cdbfb777d | 189,765 | 2026-03-23 -> 2026-09-23 |
| EURJPY | getdata-finance/eurjpy-1m-ohlcv-forex-historical-data | eb85398a913fb6304b1ea17c661f9ec58891ce31 | f79f4acc7fd140a63a2c120f08516fb239b489f5 | 189,916 | 2026-03-23 -> 2026-09-23 |
| AUDUSD | getdata-finance/audusd-1m-ohlcv-forex-historical-data | 97b572279e9f4cf83d8e40e69afb8d9a3b05d39f | d1604b891bbd4fb65cc4c06b8ec7b6d5813eeff3 | 189,815 | 2026-03-23 -> 2026-09-23 |
| USDCAD | getdata-finance/usdcad-1m-ohlcv-forex-historical-data | 108c13fa875437fde58c11d89d987b1c64ee1e5d | 901411b8fdc223ec14ce473429e15ff58b62e83d | 189,719 | 2026-03-23 -> 2026-09-23 |
| USDCHF | getdata-finance/usdchf-1m-ohlcv-forex-historical-data | 545c371fd14537cff8cf52ca4ac8c67cae46f80f | 6ebec50b4c26380526b25f3d6ad3c65c0de11918 | 189,553 | 2026-03-23 -> 2026-09-23 |
| XAGUSD | getdata-finance/xagusd-1m-ohlcv-metals-historical-data | 5e3f6bdee52b79ce0006d459fce7d324bb1fe36a | ef933e44d0430195d0d477f83ad5b8b7d690b900 | 180,106 | 2026-03-23 -> 2026-09-23 |
| NAS100 | getdata-finance/nas100-1m-ohlcv-index-historical-data | 5260d251ecc38918fa3d464c4a2988f7dec25f0d | 204a04ca70579a0ea89953e9bd4dc1f35b30a336 | 180,750 | 2026-03-23 -> 2026-09-23 |
| US30 | getdata-finance/us30-1m-ohlcv-index-historical-data | 66841c6540c1d7b6a22b908c5977cf738f8737e8 | 28e9d0c5b00bface9117f393b2184b2c87319806 | 180,658 | 2026-03-23 -> 2026-09-23 |
| SPX500 | getdata-finance/spx500-1m-ohlcv-index-historical-data | 71f7399603f3ba6ee931668dad58c4b323f83f81 | 1fd0ae9813edc333da5c2b831555c791b7310d6f | 180,576 | 2026-03-23 -> 2026-09-23 |

## Frozen evaluation split

Because the currently pinned public sample begins on 2026-03-23, the earlier draft split beginning 2026-03-12 is superseded before any Engine-K outcome calculation.

Freeze:

### Training
- 2026-03-23 00:00 UTC through 2026-05-31 23:59 UTC.

### Calibration
- 2026-06-01 through 2026-06-30.

### Historical secondary test
- 2026-07-01 through 2026-08-31.

This is not considered pristine because prior project work has examined related 2026 market periods.

### Final common-sample holdout
- 2026-09-01 through 2026-09-22 inclusive.

2026-09-23 is excluded because the external samples were refreshed during the current UTC day and may be incomplete.

No Engine-K feature, target, model hyperparameter, probability threshold, risk gate, or market-exclusion rule may be changed after the final holdout is inspected.

## Research contract conventions for Wave 1

These are research translation conventions pending broker-specific verification.

### XAUUSD
- 1 standard lot research convention = 100 oz;
- Engine-K reference size = 0.10 lot = 10 oz.

### EURUSD / GBPUSD / AUDUSD
- 1 standard lot = 100,000 base units;
- pip = 0.0001;
- pip value at 1 lot ~= USD10.

### USDJPY
- 1 lot = 100,000 USD;
- pip = 0.01 JPY;
- 1-lot pip P&L = JPY1,000;
- convert to USD using contemporaneous USDJPY.

### EURJPY
- 1 lot = 100,000 EUR;
- pip = 0.01 JPY;
- 1-lot pip P&L = JPY1,000;
- convert to USD using contemporaneous USDJPY.

### USDCAD
- 1 lot = 100,000 USD;
- pip = 0.0001 CAD;
- 1-lot pip P&L = CAD10;
- convert to USD using contemporaneous USDCAD.

### USDCHF
- 1 lot = 100,000 USD;
- pip = 0.0001 CHF;
- 1-lot pip P&L = CHF10;
- convert to USD using contemporaneous USDCHF.

### XAGUSD
Forecast-only in v0.1 until the project freezes a research contract/quantity convention.

### NAS100 / US30 / SPX500
Forecast-only in Engine K v0.1 until the intended broker/CFD contract size, point value, tick value, and margin convention are frozen.

Their price-move labels/features may be tested now; they may not enter the dollar-P&L execution simulation yet.

## Preflight requirements

Before Engine-K training outcomes:

1. download only pinned commit URLs;
2. verify CSV schema;
3. verify timestamp monotonicity and duplicates;
4. verify OHLC geometry;
5. verify first/last timestamps are compatible with the manifest;
6. exclude 2026-09-23;
7. build causal 1m/5m/1h bars;
8. run feature-causality and pivot-confirmation self-tests;
9. do not calculate target labels or model metrics in preflight.

After preflight passes, development/training may run.


## Pre-outcome universe classification

Primary **execution-research** model/trade universe:

- XAUUSD;
- EURUSD;
- GBPUSD;
- USDJPY;
- EURJPY;
- AUDUSD;
- USDCAD;
- USDCHF.

**Forecast-only** datasets:

- XAGUSD;
- NAS100;
- US30;
- SPX500.

Forecast-only datasets are pinned and may be used for data/feature diagnostics, but they must not influence the primary executable model fit, probability calibration, cross-market execution ranking, or P&L simulation until contract economics are prospectively frozen.

## Pre-outcome research feasibility conventions

Because broker-specific costs and leverage specifications are not yet available uniformly in the repository, EXP-022 v0.1 freezes the following **research-only** conventions before any target/model outcome:

- reference equity: USD500;
- primary stop-risk cap: USD20;
- primary round-trip cost: 10% of gross target;
- stress round-trip cost: 20% of gross target;
- research leverage reference: 1:500;
- max margin at that reference: USD100 / 20% of equity;
- max notional/equity: 100x / USD50,000;
- next-active-M1 entry gap: maximum five chronological minutes;
- calibrated probability qualification: `max(0.60, break-even probability + 0.05)`.

These conventions are screening assumptions, not claims about broker pricing or available leverage. Broker-native spread, commission, tick value, contract size and margin rules must replace them before paper/live promotion.

## Bar-integrity cleanup

Engine K v0.1 now requires:

- complete 5m feature bars: exactly five one-minute observations;
- complete 1h MTR bars: exactly sixty one-minute observations;
- incomplete resample bins are excluded;
- long session/feed gaps may not be crossed by a delayed next-open entry.

No target labels or model outcomes were used to make these cleanup amendments.
