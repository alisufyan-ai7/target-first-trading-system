# EXP-041 Free Macro Consensus v0.3 — Employment-Source Correction

**Frozen:** 2026-09-27  
**Input:** frozen v0.2 dataset `research/data/EXP-041-free-macro-consensus-v0.2.json`  
**Input SHA-256:** `17e93b760a7511688db110ca6e02f2892d485fad7321f6a9a21ef76d02d42811` is v0.2 audit's source dataset predecessor?  
**Authoritative v0.2 normalized SHA-256:** read and verify from `research/results/EXP-041-free-macro-consensus-acquisition-audit-v0.2.json` at runtime.  
**Type:** zero-outcome deterministic scope correction  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed

## 1. Observed issue

The corrected v0.2 dataset passed its coverage gate, but an identity audit showed EMPLOYMENT contained:

- `Non-Farm Employment Change` — desired BLS Employment Situation proxy component;
- `Unemployment Rate` — desired;
- `Average Hourly Earnings m/m` — desired;
- `ADP Non-Farm Employment Change` — **not** part of the BLS Employment Situation and must not be in the primary EMPLOYMENT family.

The 23 provisional EMPLOYMENT dates therefore mixed BLS releases with private ADP releases.

No market data, labels, P&L or protected-period outcomes have been used, so this correction is prospective and uncontaminated.

## 2. Frozen correction

Starting from the already-frozen v0.2 normalized dataset:

- remove every EMPLOYMENT record whose event name begins with or contains `ADP`;
- retain only:
  - `Non-Farm Employment Change`;
  - `Unemployment Rate`;
  - `Average Hourly Earnings m/m`;
- do not modify any Forecast / Actual / Previous text values;
- do not re-download Forex Factory pages;
- rebuild provisional event blocks as `event_date + family`;
- recalculate Gate-A coverage counts.

## 3. Integrity rule

The transform must verify that its input file SHA-256 equals the `normalized_dataset.sha256` recorded in the durable v0.2 audit:

`research/results/EXP-041-free-macro-consensus-acquisition-audit-v0.2.json`.

Fail closed on any mismatch.

## 4. Coverage gate

Require after ADP removal:

- >=40 provisional blocks total;
- >=30 surprise-bearing blocks;
- >=8 blocks each for EMPLOYMENT, CPI, PPI, RETAIL, GDP_PCE;
- >=6 FOMC policy-event dates or FOMC becomes timing-only;
- EMPLOYMENT contains no ADP rows;
- at least one Non-Farm Employment Change row remains;
- no market data, labels, P&L or protected periods.

PASS disposition:

`FREE_CONSENSUS_V03_BLS_EMPLOYMENT_SCOPE_PASS_OFFICIAL_RECONCILIATION_REQUIRED`

Only v0.3 may feed official BLS/Census/BEA/Fed reconciliation.
