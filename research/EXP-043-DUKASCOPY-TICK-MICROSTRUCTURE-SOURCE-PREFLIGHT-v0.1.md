# EXP-043 Dukascopy Tick / Quote Microstructure Source Preflight v0.1

**Frozen:** 2026-09-27  
**Type:** zero-outcome source semantics + repeatability pilot  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed

## 1. Scientific purpose

EXP-040, EXP-041 and EXP-042 did not establish a stable information advantage from richer OHLC structure, macro timing/surprise, or free DXY/T-Bond interpretation proxies.

The next orthogonal information family is execution-grade microstructure.

Dukascopy tick data exposes broker quote/tick fields:

- millisecond timestamp;
- ask price;
- bid price;
- ask volume;
- bid volume.

This is genuinely new information versus M1/M5 OHLC because it exposes spread, quote-update intensity and quote-side size.

It is **not** centralized trade aggressor flow, exchange order book, CME market depth, or consolidated FX volume. Any future features must be named broker quote/tick microstructure proxies.

## 2. Frozen transport

Use:

`dukascopy-node@1.50.0`

with:

`timeframe = tick`.

Target markets:

- XAUUSD;
- EURUSD;
- GBPUSD;
- USDJPY;
- EURJPY;
- AUDUSD;
- USDCAD;
- USDCHF.

## 3. Frozen pilot dates

Use exactly six UTC calendar dates, chosen before any tick result:

- 2025-07-09;
- 2025-09-10;
- 2025-11-12;
- 2026-01-14;
- 2026-03-11;
- 2026-05-13.

Each request is:

`00:00:00Z <= timestamp < next-day 00:00:00Z`.

These dates are source-transport probes only; no target labels or P&L are loaded.

## 4. Independent copies

Perform two independent complete downloads:

- copy A;
- copy B.

Canonical per-day CSV schema:

`timestamp_ms,ask_price,bid_price,ask_volume,bid_volume`.

Do not aggregate ticks.

## 5. Semantic integrity checks

For every symbol/date/copy require:

- file exists;
- >=500 ticks;
- timestamps nondecreasing;
- all timestamps inside requested UTC day;
- ask and bid finite and positive;
- ask >= bid on every row;
- spread = ask-bid nonnegative;
- ask_volume and bid_volume finite and >=0;
- at least one positive ask_volume;
- at least one positive bid_volume;
- at least 50 distinct millisecond timestamps;
- at least 10 distinct positive spread values or, if price precision makes that impossible, >=10 distinct spread observations at raw numeric precision.

Duplicate timestamps are allowed because multiple quote records may share a millisecond; source row order must remain unchanged.

## 6. Repeatability gate

For every symbol/date pair require:

- copy A row count == copy B row count;
- copy A canonical SHA-256 == copy B canonical SHA-256.

Global PASS requires all 48 symbol/date pairs to pass.

No tolerance-based reconciliation is allowed in v0.1.

## 7. Descriptive source diagnostics

Record only source diagnostics:

- tick count;
- first/last timestamp;
- median tick interval milliseconds;
- median spread;
- 95th-percentile spread;
- fraction zero spread;
- median ask_volume;
- median bid_volume;
- median absolute quote-side imbalance:
  `abs(ask_volume-bid_volume)/(ask_volume+bid_volume)` when denominator >0.

These diagnostics are not trading outcomes and cannot be used to select dates or markets.

## 8. PASS disposition

`EXP043_DUKASCOPY_TICK_MICROSTRUCTURE_SOURCE_REPEATABLE`

PASS authorizes a separate frozen acquisition-design stage for development-only tick windows.

It does not authorize a predictive model yet.

## 9. FAIL disposition

`EXP043_DUKASCOPY_TICK_MICROSTRUCTURE_SOURCE_NOT_REPEATABLE`

If FAIL, do not relax hash equality after seeing results. Investigate transport/history mutability or change source.

## 10. Restrictions

This preflight must not compute:

- structural target labels;
- T40/T50 outcomes;
- model probabilities;
- P&L;
- strategy filters;
- protected Jul-Aug/Sep 2026 data.

Engine R and EXP-015 remain paused.
