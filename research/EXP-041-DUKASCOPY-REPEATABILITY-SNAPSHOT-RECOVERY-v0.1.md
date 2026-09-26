# EXP-041 Dukascopy Same-Run Repeatability + Snapshot Recovery v0.1

**Frozen:** 2026-09-27  
**Type:** zero-outcome data-infrastructure diagnostic with conditional immutable snapshot creation  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed

## 1. Triggering observation

Durable snapshot diagnostic `2dc6a9c0cc1c588fa01179bcc644d5fb6e9fd578` showed that a fresh Dukascopy download on run `36264975005` did not reproduce the normalized hashes recorded by acquisition audit `1cf168d6b3b639cfcc856ffae7aeb66db880dc47`.

All eight markets differed in both SHA-256 and row count. The workflow correctly skipped immutable release creation and failed closed.

This proves that the **current live acquisition output differs from the previously observed output**. It does not by itself distinguish:

1. genuine upstream historical revisions; from
2. nondeterministic/incomplete transport behavior.

No labels, P&L, strategy outcomes, Jul-Aug data, or Sep data were involved.

## 2. Scientific question

Can the exact same frozen Dukascopy request reproduce byte-for-byte within the same workflow run?

## 3. Frozen acquisition

Run the existing downloader twice independently:

- transport: `dukascopy-node@1.50.0`;
- symbols: XAUUSD, EURUSD, GBPUSD, USDJPY, EURJPY, AUDUSD, USDCAD, USDCHF;
- timeframe: M1;
- request interval: `[2025-07-01 00:00 UTC, 2026-07-01 00:00 UTC)`;
- independent output directories A and B.

No source/range/normalization changes are allowed inside the diagnostic.

## 4. Frozen per-copy integrity gate

For every market in both A and B require:

- normalized schema exactly `datetime,open,high,low,close,volume`;
- >=300,000 rows;
- >=240 distinct UTC dates;
- first timestamp <= 2025-07-02 23:59 UTC;
- last timestamp >= 2026-06-29 23:00 UTC;
- every timestamp inside the frozen request interval;
- strictly increasing timestamps;
- no duplicates;
- positive OHLC;
- valid OHLC high/low geometry.

The common future modeling interval remains:

`[2025-07-01 00:00 UTC, 2026-06-30 00:00 UTC)`

regardless of whether a full Jun30 file is present.

## 5. Frozen repeatability gate

For all eight markets require simultaneously:

- A SHA-256 == B SHA-256;
- A row count == B row count;
- A integrity PASS;
- B integrity PASS.

No approximate matching is allowed.

## 6. Conditional action frozen before result

### If the repeatability gate FAILS

Disposition:

`CURRENT_DUKASCOPY_TRANSPORT_NONDETERMINISTIC_FIX_ACQUISITION_BEFORE_SNAPSHOT`

Do not create a release and do not proceed to macro Gate B.

The next task becomes acquisition engineering: direct/retryable day-level retrieval or another deterministic transport, still with no outcomes.

### If the repeatability gate PASSES

The previous Sep25 bytes are treated as an unrecoverable earlier observation, not as a required canonical dataset, because:

- they were never frozen as raw bytes;
- no EXP-041 target/P&L/macro outcome modeling was run on them;
- all protected periods remained sealed.

Freeze copy A **in the same workflow run** as the new canonical immutable snapshot v2.

Release tag:

`exp041-data-dukas-m1-2025-07-01_2026-06-30-v2`

Archive:

`exp041-dukas-m1-2025-07-01_2026-06-30-v2.tar.gz`

The archive must include the eight normalized CSVs and a deterministic internal manifest. Record the archive SHA-256 durably.

Disposition after successful release creation/verification:

`CURRENT_DUKASCOPY_REPEATABLE_IMMUTABLE_SNAPSHOT_V2_FROZEN`

No further live Dukascopy re-download is then permitted for EXP-041 development modeling; later workflows consume the exact release asset and verify hashes.

## 7. Scientific boundary

This diagnostic/snapshot process computes:

- NO target labels;
- NO P&L;
- NO strategy outcomes;
- NO macro outcome model;
- NO Jul-Aug 2026 data;
- NO Sep 2026 data.

Engine R remains paused.

## 8. Next action after a successful snapshot

Proceed directly to the remaining EXP-041 Gate-A blocker:

- acquire enough historical macro event blocks;
- official release timestamps;
- point-in-time pre-release consensus;
- actual-as-released values;
- preserve the existing independent-event requirements.

Do not return to generic OHLC strategy research.
