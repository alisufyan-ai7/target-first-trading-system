# EXP-041 Official Actual-as-Released Reconciliation v0.1

**Frozen:** 2026-09-27  
**Inputs:**
- `research/data/EXP-041-free-macro-consensus-v0.3.json`
- `research/data/EXP-041-official-release-time-map-v0.4.json`

**Type:** zero-market-outcome macro actual/consensus reconciliation  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed

## 1. Objective

Create one causally defensible surprise-bearing macro component for every numeric official event block without turning the project into an open-ended parser of every statistic in every release.

There are 75 official blocks:

- 67 numeric blocks;
- 8 FOMC policy blocks.

FOMC remains timing-only in EXP-041 v0.1.

For each of the 67 numeric blocks, select exactly one forecast-bearing canonical component, verify its published Actual against the first-party release page, and retain the already-frozen Forex Factory historical Forecast consensus.

## 2. Frozen canonical component hierarchy

Selection is deterministic and frozen before results.

### EMPLOYMENT

1. `Non-Farm Employment Change`
2. `Unemployment Rate`
3. `Average Hourly Earnings m/m`

### CPI

1. `CPI m/m`
2. `Core CPI m/m`
3. `CPI y/y`
4. `Core CPI y/y`

### PPI

1. `PPI m/m`
2. `Core PPI m/m`

### RETAIL

1. `Retail Sales m/m`
2. `Core Retail Sales m/m`

### GDP

1. `Advance GDP q/q`
2. `Prelim GDP q/q`
3. `Final GDP q/q`

### PCE

1. `Core PCE Price Index m/m`
2. `Personal Income m/m`
3. `Personal Spending m/m`

A component is eligible only when its frozen Forex Factory `Forecast` is non-empty.

The input audit already shows every one of the 67 numeric official blocks has exactly one selected forecast-bearing component under this hierarchy.

## 3. Official actual reconciliation method

The first-party page is authoritative.

Forex Factory `Actual` is treated only as a frozen candidate value.

For the selected canonical component:

1. parse the frozen candidate Actual into native numeric units;
2. fetch the exact first-party release page/PDF;
3. require component-specific context on that first-party source;
4. require the same candidate numeric value in that component context;
5. only then mark the Actual as:
   `OFFICIAL_CONTEXT_VERIFIED_ACTUAL_AS_RELEASED`.

If the official page does not verify the candidate value in the correct context, the block remains unresolved and the gate fails.

This is intentionally stricter than accepting Forex Factory Actual directly and simpler/safer than parsing every table cell in every agency format.

## 4. Component-specific official context

### EMPLOYMENT / NFP

Official BLS Employment Situation archive.

Require:

- `nonfarm payroll employment` context;
- candidate employment count, converting `K` to persons;
- negative candidates require decline/decrease/loss context or an explicit negative signed number.

### CPI

Official BLS CPI archive.

For `CPI m/m` require CPI-U/all-items context with candidate monthly percent.

For `Core CPI m/m` require all-items-less-food-and-energy/core context with candidate monthly percent.

For year-over-year fallbacks require 12-month context.

### PPI

Official BLS PPI archive.

For headline require final-demand context with candidate monthly percent.

For Core PPI require final-demand-less-food-and-energy/core context.

### RETAIL

Official Census MARTS historical PDF.

Require retail-and-food-services-sales context with the candidate month-over-month percent.

### GDP

Official BEA GDP release page.

Require real-gross-domestic-product/GDP context with the candidate annualized quarterly percent.

### PCE

Official BEA Personal Income and Outlays release page.

For Core PCE require `excluding food and energy` PCE-price-index context.

Fallback Personal Income/Spending components use their named first-party context.

## 5. 2025 BEA direct release-page manifest

The official-time v0.4 map contains direct release pages for 2026 BEA blocks. For the eight 2025 BEA blocks, freeze these first-party pages for Phase B:

- 2025-07-30 GDP:
  `https://www.bea.gov/news/2025/gross-domestic-product-2nd-quarter-2025-advance-estimate`
- 2025-07-31 PCE:
  `https://www.bea.gov/news/2025/personal-income-and-outlays-june-2025`
- 2025-08-28 GDP:
  `https://www.bea.gov/news/2025/gross-domestic-product-2nd-quarter-2025-second-estimate-and-corporate-profits-preliminary`
- 2025-08-29 PCE:
  `https://www.bea.gov/news/2025/personal-income-and-outlays-july-2025`
- 2025-09-25 GDP:
  `https://www.bea.gov/news/2025/gross-domestic-product-2nd-quarter-2025-third-estimate-gdp-industry-corporate-profits`
- 2025-09-26 PCE:
  `https://www.bea.gov/news/2025/personal-income-and-outlays-august-2025`
- 2025-12-05 PCE:
  `https://www.bea.gov/news/2025/personal-income-and-outlays-september-2025`
- 2025-12-23 GDP:
  `https://www.bea.gov/news/2025/gross-domestic-product-3rd-quarter-2025-initial-estimate-and-corporate-profits`

No other BEA URL discovery is allowed inside the run.

## 6. Input integrity

Require exact SHA-256:

- consensus v0.3: read from its durable v0.3 scope audit;
- official time map v0.4: read from durable v0.4 timing result.

Fail closed on mismatch.

## 7. Output schema

For each numeric official block:

- official_block_id;
- family;
- release_kind;
- official_release_timestamp_utc;
- selected_component;
- event_id;
- forecast_text;
- forecast_numeric;
- candidate_actual_text;
- candidate_actual_numeric;
- native_unit;
- official_actual_verification_source_url;
- official_actual_source_sha256;
- official_context_verified;
- official_actual_numeric;
- surprise_native = official_actual_numeric - forecast_numeric.

For FOMC:

- retain timing/provenance;
- `surprise_component = null`;
- `timing_only = true`.

## 8. Frozen gate

PASS requires:

1. exact consensus and official-time-map hashes verified;
2. exactly 67 numeric official blocks selected;
3. exactly 8 FOMC timing-only blocks retained;
4. no numeric block has missing Forecast;
5. no numeric block has ambiguous canonical selection;
6. all 67 first-party pages/PDFs return HTTP 200;
7. all 67 candidate Actual values verify in component-specific official context;
8. all official source URLs/hashes retained;
9. no market data, target labels, P&L or protected periods loaded.

PASS disposition:

`OFFICIAL_ACTUAL_RECONCILIATION_PASS_FINAL_GATE_A_REQUIRED`

## 9. Next step after PASS

Run one final zero-outcome Gate-A audit on the reconciled macro layer.

That audit must verify:

- independent numeric block counts;
- surprise-bearing counts;
- family minimums;
- FOMC timing-only treatment;
- point-in-time Forecast provenance;
- official Actual + timestamp provenance;
- immutable hashes.

Only after that final Gate-A PASS may EXP-041 load canonical Dukascopy snapshot v2 and begin information-content modeling.
