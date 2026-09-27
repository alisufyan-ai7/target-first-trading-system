# EXP-041 Full Free Macro Consensus Acquisition v0.2 — Scope Correction

**Frozen:** 2026-09-27  
**Supersedes:** v0.1 normalized consensus layer for downstream official reconciliation  
**Reason:** zero-outcome parser-scope correction discovered before any official reconciliation or market outcome modeling

## 1. Observed v0.1 issues

Durable v0.1 acquisition result:

`48291dc19916616ade0852faa067194ebfb6172e`

The coverage gate passed, but record inspection showed:

1. EMPLOYMENT omitted the Forex Factory label **Non-Farm Employment Change**, so the primary NFP component was missing.
2. FOMC matching included speeches, meeting minutes, press conferences and other non-policy rows, inflating the provisional FOMC count to 394 blocks.
3. Forex Factory displayed time is often blank/repeated within simultaneous releases, so using displayed time in the provisional block key can split one release into multiple pseudo-blocks.

No target labels, P&L, market outcomes, Jul-Aug 2026 or Sep 2026 data were used. Therefore this correction is prospective and uncontaminated.

## 2. Frozen corrections

### Employment

Add aliases:

- Non-Farm Employment Change;
- Nonfarm Employment Change;
- Non-Farm Payrolls;
- Nonfarm Payrolls;
- Unemployment Rate;
- Average Hourly Earnings.

### FOMC

Only these rows may enter the FOMC family:

- FOMC Statement;
- Federal Funds Rate;
- FOMC Economic Projections.

Explicitly exclude:

- FOMC Member ... Speaks;
- FOMC Meeting Minutes;
- FOMC Press Conference;
- FOMC Financial Stability Report;
- other speech/minutes/non-policy rows.

### Independent event blocks

For provisional Gate-A counting group by:

`event_date + family`

not Forex Factory displayed time.

This is conservative and appropriate before official release-time reconciliation. Simultaneous components on one release date remain one economic event block.

## 3. Source/date rules unchanged

- consensus source: Forex Factory historical `Forecast`;
- allowed retained dates: 2025-07-01 through 2026-06-29;
- no week page containing July 2026;
- no raw HTML committed;
- official actual/time reconciliation remains a later stage;
- no market data, target labels, P&L, Jul-Aug 2026 or Sep 2026 data.

## 4. Corrected coverage gate

Require:

- all requested pages HTTP 200;
- Actual/Forecast/Previous columns present;
- no retained row after 2026-06-29;
- >=40 provisional independent blocks total;
- >=30 surprise-bearing provisional blocks;
- >=8 blocks each for EMPLOYMENT, CPI, PPI, RETAIL, GDP_PCE;
- >=6 distinct FOMC policy-event dates OR FOMC remains timing-only;
- NFP component appears in the normalized EMPLOYMENT rows;
- no market outcome computation.

PASS disposition:

`FREE_CONSENSUS_V02_SCOPE_CORRECTED_GATE_PASS_OFFICIAL_RECONCILIATION_REQUIRED`

Only a passing v0.2 dataset may feed official reconciliation.
