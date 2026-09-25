# EXP-041 Third-Source Feed Adjudication v0.1

**Date:** 2026-09-25  
**Status:** PROSPECTIVELY FROZEN — ZERO OUTCOME  
**Purpose:** adjudicate the existing pinned feed vs Dukascopy using an independent third M1 source  
**Target labels / P&L:** NONE

## Third source

**HistData.com Generic ASCII M1 bid bars**.

HistData documents:

- M1 historical data;
- all eight required pairs/instruments, including XAUUSD;
- Generic ASCII M1 bars are bid-quote OHLC;
- timestamps are EST (UTC-5) with no daylight-saving adjustment.

Transport helper:

- `histdata-fetcher==0.1.0`;
- transport only; HistData.com remains the data authority;
- helper timestamps are localized from fixed UTC-5 to UTC before comparison.

## Scope

Overlap only:

`2026-03-23 00:00 UTC <= t < 2026-07-01 00:00 UTC`.

No Jul-Aug/Sep 2026.

Sources:

1. CURRENT_PINNED — repository-pinned research source;
2. DUKASCOPY — official historical export transported by frozen helper;
3. HISTDATA — independent M1 bid source.

## Frozen pairwise agreement test

For each source pair and market require all:

1. exact/common M1 overlap ratio of smaller feed >=70%;
2. 5m log-return correlation >=0.90;
3. 1h log-return correlation >=0.95;
4. 1d log-return correlation >=0.95;
5. 1h direction-sign agreement >=0.95.

Level-price ratio is reported descriptively but is **not** part of third-source agreement because venue/bid/CFD basis can differ while return path remains usable.

## Frozen adjudication

For each market:

- DUKASCOPY-HISTDATA passes while both pairs involving CURRENT_PINNED fail -> `CURRENT_PINNED_OUTLIER`;
- CURRENT_PINNED-HISTDATA passes while both pairs involving DUKASCOPY fail -> `DUKASCOPY_OUTLIER`;
- CURRENT_PINNED-DUKASCOPY passes while both HistData pairs fail -> `HISTDATA_OUTLIER`;
- at least two of three pairs pass -> `BROAD_THREE_SOURCE_CONSENSUS`;
- otherwise -> `NO_TWO_SOURCE_CONSENSUS`.

## Feed-selection gate

A development feed is not accepted from this test unless:

- one source is supported by at least one passing pair in >=7/8 markets; and
- no more than 1 market is `NO_TWO_SOURCE_CONSENSUS`.

If a clear source consensus exists, freeze a separate acquisition v0.2 before downloading twelve-month history.

If not, require intended-broker/another institutional source.

## Protection

- target labels: NO;
- P&L: NO;
- strategy selection: NO;
- Jul-Aug: NO;
- Sep: NO.
