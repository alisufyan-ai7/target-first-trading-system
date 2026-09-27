# EXP-041 Final Gate-A Adequacy / Provenance Audit v0.1

**Frozen:** 2026-09-27  
**Type:** zero-outcome final data-adequacy audit  
**Market outcomes:** NOT LOADED  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed

## 1. Objective

Make the final yes/no decision on whether EXP-041 Gate B may begin.

Inputs are already frozen:

- canonical Dukascopy development snapshot v2;
- free/public historical consensus layer v0.3;
- official release-time map v0.4;
- official macro surprise layer v0.1.

This audit computes no target/path labels and no P&L.

## 2. Governing frozen Gate-A requirements

From `research/experiments/EXP-041-macro-catalyst-information-content-v0.1.md`:

1. at least 12 months of development market history ending no later than 2026-06-30;
2. at least 8 releases per recurring numeric family: EMPLOYMENT, CPI, PPI, RETAIL, GDP_PCE;
3. at least 40 independent macro event blocks total;
4. at least 30 surprise-bearing event blocks;
5. at least 6 distinct FOMC policy events or FOMC is timing-only/descriptive;
6. every chronological evaluation fold contains at least 4 independent event blocks;
7. at least two event families are represented in every evaluation fold;
8. consensus provenance is point-in-time / pre-release, not a post-hoc model forecast;
9. official release timestamps are independently verified;
10. Jul-Aug/Sep 2026 remain unloaded/unlabeled.

No requirement may be weakened in this audit.

## 3. Independent event-block rule

The original EXP-041 definition governs:

> A single timestamp containing several reported components is one independent event block.

Therefore the final audit groups the reconciled macro layer by exact:

`official_release_timestamp_utc`

All records sharing that timestamp are one independent event block, even if they came from different first-party release pages.

An independent timestamp block is surprise-bearing when at least one numeric record at that timestamp has an official verified Actual and a frozen pre-release Forecast.

## 4. Family counting

For the recurring-family minimum:

- EMPLOYMENT = distinct timestamps containing EMPLOYMENT;
- CPI = distinct timestamps containing CPI;
- PPI = distinct timestamps containing PPI;
- RETAIL = distinct timestamps containing RETAIL;
- GDP_PCE = distinct timestamps containing either GDP or PCE release-kind records;
- FOMC = distinct timestamps containing FOMC.

A timestamp can count toward more than one family if genuinely simultaneous official releases occur, but it counts only once toward the total independent-block count.

## 5. Frozen six chronological evaluation folds

Before any outcome model is fitted:

1. sort independent timestamp blocks ascending;
2. split into exactly six contiguous folds as evenly as possible by block count;
3. earlier folds receive one extra block when division has a remainder;
4. record exact start/end UTC boundaries and block IDs durably.

These six audit folds become the default EXP-041 Gate-B evaluation folds. Gate B may not redraw them after seeing market outcomes.

Each fold must contain:

- >=4 independent blocks;
- >=2 represented event families.

## 6. Market-history check

Read metadata only from the durable Dukascopy snapshot-recovery result.

Require:

- repeatability gate PASS;
- release created/verified;
- release tag `exp041-data-dukas-m1-2025-07-01_2026-06-30-v2`;
- archive SHA-256 `90bc7301e459062e8e35cd89a1a9aac23332ca3472014dd2cc5045ba34794272`;
- effective common model interval exactly:
  `[2025-07-01T00:00:00Z, 2026-06-30T00:00:00Z)`;
- all eight markets integrity PASS.

The price archive itself is not loaded in this Gate-A audit.

## 7. Macro provenance check

Require official actual reconciliation PASS and exact surprise-layer SHA from its durable result.

For every numeric record require:

- non-empty Forecast;
- `official_context_verified=true`;
- official actual numeric present;
- official actual source SHA present;
- official UTC release timestamp present.

For every FOMC record require:

- timing-only true;
- official UTC release timestamp;
- first-party source URL.

Consensus source role must remain the frozen public historical Forex Factory Forecast proxy from the v0.3 consensus input.

## 8. PASS disposition

If all frozen requirements pass:

`EXP041_GATE_A_PASS_AUTHORIZE_GATE_B_INFORMATION_CONTENT`

This authorizes only the information-content study.

It does **not** authorize:

- strategy-engine construction;
- Engine R targets/P&L;
- protected-period use;
- risk scaling;
- live trading.

## 9. FAIL disposition

If any frozen requirement fails:

`EXP041_GATE_A_FAIL_DO_NOT_MODEL`

Do not weaken thresholds or consume protected future data.
