# Data Sources

## Principle

Do not depend on one feed for final validation.

Use one feed for strategy development/baseline testing and at least one independent feed for finalist validation.

## Baseline used so far

### Dukascopy XAUUSD minute data

Used for the first Engine A strategy-level screen.

Advantages:

- broker-neutral baseline;
- one-minute OHLC;
- long history available;
- suitable for initial mechanical strategy research.

Limitations:

- not the user's eventual broker execution feed;
- Phase-1 test excluded broker-specific spread, commission, slippage, latency, and contract specification;
- price construction may differ from an MT5 broker's XAUUSD CFD.

### EXP-014 recovery transport / mirror

During EXP-014, the execution environment used a public GitHub mirror of Dukascopy-derived XAUUSD BID M1 CSV data as **external research-data transport** because direct binary-archive retrieval was not practical in the tool session.

For the frozen March 1 through August 20, 2026 window:

- rows: 230,813, exactly matching EXP-002's recorded row count;
- duplicate timestamps: 0;
- invalid OHLC rows: 0.

The exact monthly blob SHAs are recorded in EXP-014.

Important limitation: exact row-count agreement does not prove byte-for-byte identity with the original unpublished EXP-002 local download. The mirror is therefore documented as Dukascopy-derived research data, not treated as a substitute for later independent-feed/broker validation.

## Independent validation candidates

### MetaTrader 5

Preferred broker-specific validation path once a terminal is available and logged into the intended broker.

Useful for:

- broker OHLC;
- tick volume;
- spread fields/history where available;
- symbol contract specification;
- realistic position-size and margin modeling.

Constraint: Python access requires an installed MT5 terminal and broker account connection.

### OANDA v20

Candidate independent FX/metals candle source where instrument coverage and API access are appropriate.

### Twelve Data

Candidate independent XAU/USD intraday source for cross-feed validation.

### Binance

Appropriate for crypto markets such as BTCUSDT.

Do **not** treat Binance PAXG or other tokenized-gold markets as interchangeable with broker XAUUSD.

## Validation rule

Do not tune a strategy separately on multiple feeds until one looks best.

Instead:

1. define/freeze the strategy on the baseline feed;
2. run it unchanged on the independent feed;
3. investigate material discrepancies;
4. only then decide whether feed-specific execution rules are justified.

## Raw-data storage

Large raw datasets should generally remain outside Git.

Git should contain:

- source;
- instrument;
- timeframe;
- date range;
- retrieval method;
- checksum if practical;
- transformation/resampling rules;
- experiment ID that used the data.
