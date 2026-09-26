# EXP-041 Data-Source Governance v0.3

**Frozen:** 2026-09-27  
**Supersedes:** v0.2 for active EXP-041 development-data use  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed

## 1. Final Dukascopy decision

### OBSERVED

Run `36265569383`, durable result commit `b69e6cb9376c4f57622d042d19de41041a60dca7`, performed two independent downloads of the exact same Dukascopy request.

All eight markets:

- passed schema/coverage/monotonicity/OHLC integrity;
- had zero duplicate timestamps;
- matched byte-for-byte between copy A and copy B;
- had identical row counts between copies.

The immutable release was created or verified successfully.

Release tag:

`exp041-data-dukas-m1-2025-07-01_2026-06-30-v2`

Archive:

`exp041-dukas-m1-2025-07-01_2026-06-30-v2.tar.gz`

Archive SHA-256:

`90bc7301e459062e8e35cd89a1a9aac23332ca3472014dd2cc5045ba34794272`

Disposition:

`CURRENT_DUKASCOPY_REPEATABLE_IMMUTABLE_SNAPSHOT_V2_FROZEN`

No target labels, P&L, macro outcome model, Jul-Aug data, or Sep data were used.

## 2. Canonical EXP-041 market-data rule

### DECISION

EXP-041 development must use the immutable snapshot v2 above.

Do not re-download live Dukascopy for EXP-041 modeling.

Every downstream EXP-041 workflow must:

1. fetch the exact v2 release asset;
2. verify archive SHA-256;
3. verify per-market SHA-256 values from the durable repeatability result;
4. fail closed on mismatch;
5. use only the effective common model interval:
   `2025-07-01 00:00 UTC <= t < 2026-06-30 00:00 UTC`.

The live Dukascopy archive may change over time. Such later changes do not alter EXP-041 v2. Any future data refresh must become a new versioned snapshot.

## 3. Why v2 can supersede the unrecoverable Sep25 observation

The earlier Sep25 Dukascopy download was never stored as an immutable raw snapshot.

No EXP-041 macro/target/P&L outcome modeling was performed on those earlier bytes.

Therefore freezing the current repeatable, integrity-passing v2 snapshot prospectively does not contaminate outcome evidence or rewrite a completed scientific result.

## 4. Macro-data source rule

With market-history acquisition closed, Gate A now requires point-in-time macro/catalyst history.

Release timestamp authorities:

- U.S. Bureau of Labor Statistics — Employment, CPI, PPI;
- U.S. Census Bureau — Retail Sales;
- U.S. Bureau of Economic Analysis — GDP and Personal Income/Outlays;
- Federal Reserve — FOMC.

Preferred consensus / actual-as-released source:

- Trading Economics historical economic-calendar/API/archive data with pre-release Forecast/consensus, Actual, Previous, revision fields and event timestamps.

Acceptable alternative:

- Econoday historical calendar/consensus archive with actual-as-released and revisions.

Causal requirements:

- consensus value must be the value available before release;
- actual is unavailable before the release timestamp;
- later revisions must not overwrite original actual-as-released values;
- every stored event retains source provenance and original timezone;
- Jul-Aug/Sep 2026 remain excluded from sample extension.

## 5. Next action

Acquire enough 2025-07-01 through 2026-06-29 point-in-time macro event history to satisfy the already-frozen EXP-041 Gate-A requirements:

- >=40 independent event blocks total;
- >=30 surprise-bearing blocks;
- >=8 releases each for EMPLOYMENT, CPI, PPI, RETAIL, GDP_PCE;
- >=6 FOMC events or FOMC remains timing-only;
- point-in-time pre-release consensus provenance;
- first-party release-time verification.

Only after Gate A passes may EXP-041 Gate B calculate target-path labels and test incremental macro information content.
