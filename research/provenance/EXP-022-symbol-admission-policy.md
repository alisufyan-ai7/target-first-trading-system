# EXP-022 Symbol Admission Policy

**Frozen:** 2026-09-23 before Engine-K target/model outcomes  
**Purpose:** define how additional markets enter the direct target-move scanner without post-hoc universe mining.

## Principle

The scanner should become broad enough to find opportunity across genuinely different market regimes, but symbol count is not itself an objective.

Prefer incremental **diversification of opportunity sources** over adding many highly correlated instruments.

A symbol may be observed only after clean pinned data exist. A symbol may become execution-research eligible only after its economic and session mechanics are prospectively frozen.

## Admission stages

### Stage A — planned

Named expansion candidate only.

No model fitting, ranking or P&L contribution.

### Stage B — forecast-only

Requirements:

- exact symbol/venue definition;
- pinned immutable historical data source/version;
- documented timestamp timezone and trading calendar;
- audited schema, duplicates, OHLC geometry and material gaps;
- causal 1m -> 5m / 1h construction rules;
- enough overlapping history for the frozen Engine-K split or a separately frozen split.

Forecast-only symbols may receive feature/label diagnostics in a separately declared diagnostic model. They may not affect the primary executable model.

### Stage C — execution-research

Additional requirements:

- exact contract/quantity convention;
- tick size and tick value;
- P&L currency/conversion;
- minimum quantity/lot and step;
- target-equivalent sizing function;
- spread/commission/slippage research convention;
- margin/leverage/notional convention;
- financing/funding rule if relevant;
- session/market-close handling;
- structural-stop dollar-risk calculation.

Only Stage-C symbols may fit/calibrate the primary executable model, enter cross-market ranking, or contribute simulated P&L.

### Stage D — paper/live eligible

Additional requirements:

- broker/venue-native contract specification;
- broker/venue-native spread/commission/funding;
- longer-history and independent-feed validation;
- forward/demo evidence;
- operational execution checks.

Engine-K historical success alone does not create Stage-D eligibility.

## Current Engine-K v0.1 classification

### Execution-research

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

### Forecast-only

- XAGUSD
- NAS100
- US30
- SPX500

### Planned expansion

Priority should be given to markets that add regime diversification rather than another near-duplicate USD FX exposure:

1. BTCUSD or BTCUSDT — exact venue must be selected first;
2. GBPJPY if compatible one-minute data and economics are pinned;
3. executable XAGUSD;
4. executable NAS100 / US30 / SPX500;
5. ETHUSD/ETHUSDT after BTC mechanics are solved;
6. a liquid energy market such as WTI/USOIL only after exact broker/data mechanics are documented;
7. additional liquid indices/crosses only when they add useful independent opportunity.

## Why BTC is not in v0.1

BTC was deliberately not admitted yet because the repository does not currently freeze:

- whether the instrument is BTCUSD CFD, spot BTCUSD, or BTCUSDT perpetual;
- the venue/feed;
- immutable one-minute provenance;
- contract/quantity convention;
- fee schedule;
- spread/slippage convention;
- leverage/margin;
- perpetual funding if applicable;
- 24/7 horizon/day-boundary handling.

Guessing these after seeing BTC outcomes would contaminate the economic test.

BTC is therefore a **high-priority Wave-2 candidate**, not an excluded market.

## Universe-size policy

Eight execution markets / twelve observed markets are sufficient for the first Engine-K architecture test because the experiment already produces dense five-minute long/short states.

They are **not** considered sufficient as the intended final production universe because the eight execution markets are concentrated in Gold + USD-linked FX.

After v0.1 proves the pipeline, expansion should prioritize distinct asset classes: indices, silver, crypto, and possibly energy.

A practical production target is not a fixed count. The preferred direction is roughly **12–20 executable, liquid, economically documented markets across several asset classes**, stopping expansion when new symbols add little incremental opportunity or mostly duplicate existing factor exposure.

## Anti-mining rule

Do not add or remove a symbol from an already-inspected test/holdout merely because its observed performance is attractive or poor.

Universe changes create a new prospectively frozen engine/version or evaluation wave.
