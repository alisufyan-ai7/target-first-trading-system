# EXP-041 Data-Source Governance v0.2

**Frozen:** 2026-09-25  
**Scope:** EXP-041 development market-history provenance only  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed  
**Scientific outcomes:** none

## 1. Why v0.2 exists

### OBSERVED

The prospectively frozen v0.1 cross-feed program did not identify a broad public-feed consensus:

- three-source adjudication durable result: `3e5ed20a733bf80fc72c155c756edf7c115c566e`;
- CURRENT_PINNED supported by a passing pair in 2/8 markets;
- DUKASCOPY supported in 2/8;
- HISTDATA supported in 0/8;
- six markets had no two-source consensus.

The final allowed HistData mechanical diagnostic also failed:

- durable result: `f98eba568e1aad440873443eaec4e7ed7480b20e`;
- no common whole-hour shift from -6h through +6h restored the original frozen feed-selection gate;
- best descriptive shift was -1h, but it still produced no eligible consensus source;
- disposition: `TIMESTAMP_SHIFT_DOES_NOT_EXPLAIN_FAILURE_REQUIRE_FOURTH_OR_BROKER_SOURCE`.

No target labels, P&L, Jul-Aug data, or Sep data were used.

## 2. Decision

### DECISION

Stop public-feed adjudication/remediation for EXP-041. Do not spend additional research cycles forcing CURRENT_PINNED, Dukascopy and HistData to agree.

For EXP-041 development research:

1. **Dukascopy Bank historical data becomes the canonical market-history source.**
2. This is a prospective governance choice, **not** a claim that the failed v0.1 consensus gate passed.
3. The exact normalized Dukascopy files already audited in v0.1 must be frozen as an immutable, hash-addressed snapshot before Gate-B modeling.
4. Every later EXP-041 development workflow must consume that frozen snapshot, not re-download live Dukascopy history.
5. If the live Dukascopy archive no longer reproduces the already-recorded normalized SHA-256 hashes during snapshot creation, stop and investigate source drift rather than silently accepting revised history.
6. The existing pinned source and HistData remain diagnostic references only.
7. Intended-broker or institutional-quality bid/ask/tick/spread data remains mandatory for independent execution validation before deployment.

## 3. Frozen source and transport

Authority: Dukascopy Bank historical data.  
Transport: `dukascopy-node@1.50.0`, exact version.

Frozen downloaded interval:

`[2025-07-01 00:00:00 UTC, 2026-07-01 00:00:00 UTC)`

Symbols: XAUUSD, EURUSD, GBPUSD, USDJPY, EURJPY, AUDUSD, USDCAD, USDCHF.

Normalized schema:

`datetime,open,high,low,close,volume`

## 4. Exact normalized-file hashes to preserve

These hashes come from durable v0.1 acquisition audit `1cf168d6b3b639cfcc856ffae7aeb66db880dc47` and are frozen before snapshot creation:

| Market | SHA-256 | Rows |
|---|---|---:|
| XAUUSD | `1afa576b5492b4965b6ca19fe613ae8e5a7e520b2dc8f8b16fff32eb37b6b197` | 344,537 |
| EURUSD | `22d3efa1d303f4e4a80bf41f89fd296e9128e699718798624195d13ca87b7b0f` | 367,667 |
| GBPUSD | `3b4a5bdd8fb02508596ec64dca1ffdd92adfde72cc0039cb1c22de913dda68b2` | 338,380 |
| USDJPY | `05296feddaacc8c5c0d9778be9a7612693bbbe3f9f66f0f716838ad0f51fe5f4` | 368,988 |
| EURJPY | `4514cdbe82e4aa2c73d5c30c8ecf1b14c95d49bbd09e568ebd510b8fe49a36d3` | 353,514 |
| AUDUSD | `f275920579feb1fe5f3c9d14bffed7cf61bc140d5181a14480e9d3b03a31d4ab` | 364,256 |
| USDCAD | `00ddb2cde3a7a96539a750747f8c76993aa755f5a4fc94169875959b1e62a568` | 364,120 |
| USDCHF | `1b066ffe16a9cbfe18f1c25ece76390a3d6ca3ef3b6f1fd74bd816f7c14b98da` | 354,708 |

## 5. USDCHF common-window rule

### OBSERVED

The frozen USDCHF Dukascopy file ends at 2026-06-29 23:59 UTC while the other seven markets contain Jun30 data.

### DECISION

Preserve the full eight downloaded files unchanged in the immutable snapshot, but use a common EXP-041 modeling interval ending **2026-06-30 00:00 UTC exclusive** across all eight markets:

`[2025-07-01 00:00:00 UTC, 2026-06-30 00:00:00 UTC)`

This avoids market-specific availability on Jun30 and does not consume protected data.

## 6. Immutable snapshot storage

Do not store a mutable file named “latest”.

Create one immutable GitHub Release:

- tag: `exp041-data-dukas-m1-2025-07-01_2026-06-30-v1`;
- asset: deterministic compressed archive of the eight normalized CSVs plus internal manifest;
- asset: external JSON snapshot manifest;
- record archive SHA-256 and per-file SHA-256 in repository result.

The release must never be overwritten. A future refreshed dataset receives a new version/tag.

## 7. Reproducibility rule

After the immutable snapshot exists, later EXP-041 workflows must:

1. download the exact release asset;
2. verify archive SHA-256;
3. verify all eight normalized-file SHA-256 values;
4. enforce the common modeling cutoff;
5. fail closed on any mismatch.

Live Dukascopy re-download is then unnecessary for the frozen EXP-041 development study.

## 8. What this decision does not authorize

This v0.2 governance decision does **not** calculate target labels or P&L, approve a strategy, claim Dukascopy equals the eventual broker feed, open Jul-Aug/Sep 2026, resume Engine R, or bypass macro-event Gate-A sample/provenance requirements.

## 9. Next action

Create exactly one immutable Dukascopy snapshot from the already-audited normalized bytes. If all eight hashes reproduce exactly, checkpoint the release tag/archive hash and move immediately to the remaining EXP-041 Gate-A task: acquiring enough point-in-time macro event timestamps, pre-release consensus and actual-as-released history.

If the hashes do not reproduce, stop and investigate source drift before macro modeling.
