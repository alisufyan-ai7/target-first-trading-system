# EXP-041 Extended Market-History Acquisition Manifest v0.1

**Frozen:** 2026-09-25  
**Purpose:** satisfy the market-history half of EXP-041 Gate A without consuming protected future data  
**Type:** data acquisition / provenance, not a strategy experiment

## 1. Source

Authoritative price-data source:

- **Dukascopy Bank Historical Data**
- official historical export: https://www.dukascopy.com/swiss/english/marketwatch/historical/
- official historical-data documentation: https://www.dukascopy.com/wiki/en/development/strategy-api/historical-data/
- official export page states that historical Forex/commodity data are available at multiple granularities.

Transport helper:

- `dukascopy-node@1.50.0`
- npm: https://www.npmjs.com/package/dukascopy-node
- helper only; Dukascopy remains the data authority.

The helper is frozen to an exact version. CI records the installed npm package version and package integrity metadata where available.

## 2. Instruments

Acquire M1 data for the existing eight research markets:

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

Dukascopy instrument identifiers are the lowercase forms of these symbols.

## 3. Frozen development interval

`[2025-07-01 00:00:00 UTC, 2026-07-01 00:00:00 UTC)`

This provides approximately twelve months of development history ending at the existing Jun30 protection boundary.

Absolutely do not download Jul-Aug-Sep 2026 for EXP-041.

## 4. Price side / representation

The transport helper's minute-candle endpoint is used consistently for the entire twelve-month EXP-041 development feed.

No splice with the existing pinned March-June source is allowed inside EXP-041.

The existing source is used only for an overlap sanity audit.

This feed is an **information-content research feed**, not final broker-execution truth.

Final deployability still requires intended-broker bid/ask/tick/spread validation.

## 5. Normalized schema

Each acquired file is normalized to:

`datetime,open,high,low,close,volume`

with:

- UTC timestamps;
- one row per available minute;
- monotonic increasing timestamps;
- no duplicate timestamps;
- positive OHLC;
- valid high/low geometry.

## 6. Integrity gates

Per symbol require:

1. >=300,000 M1 rows in the frozen interval;
2. >=240 distinct UTC dates containing data;
3. first timestamp no later than 2025-07-02 23:59 UTC;
4. last timestamp no earlier than 2026-06-30 18:00 UTC;
5. no row >=2026-07-01;
6. no duplicate timestamp;
7. monotonic timestamps;
8. valid OHLC geometry;
9. SHA-256 of normalized file recorded durably.

## 7. Cross-feed overlap sanity audit

For 2026-03-23 through 2026-06-30:

- compare Dukascopy to the existing repository-pinned research source;
- do not require identical ticks/quotes;
- require substantial timestamp overlap;
- report level difference and hourly-return correlation.

Frozen sanity thresholds:

- exact-M1 overlap >=70% of the smaller feed in the overlap interval;
- hourly close-to-close return correlation >=0.95;
- median absolute relative close difference <=0.5%.

A failure means investigate the feed before macro modeling; it does not authorize threshold tuning or use of protected periods.

## 8. Storage / reproducibility

Raw twelve-month CSVs are **not committed to GitHub**.

The durable audit result records:

- source/version;
- date range;
- row counts;
- first/last timestamps;
- SHA-256 hashes;
- overlap statistics;
- integrity status.

Later EXP-041 workflows must re-download the same frozen source/range and verify the recorded hashes before using the data.

If hashes change, stop and investigate source drift.

## 9. Scientific boundary

This acquisition computes:

- **NO target labels**;
- **NO strategy outcomes**;
- **NO P&L**;
- **NO protected-period result**.

It is data infrastructure only.

## 10. Next action after acquisition

If the market-history gate passes, the remaining Gate-A blocker is sufficient point-in-time macro actual/consensus history.

Do not run EXP-041 Gate B until the full macro data-adequacy gate passes.
