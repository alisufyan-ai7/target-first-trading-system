# EXP-041 Full Free Macro Consensus Acquisition / Gate-A Coverage Audit v0.1

**Frozen:** 2026-09-27  
**Type:** development-only macro data acquisition / coverage audit  
**Requires:** free-source preflight PASS at `bdaaa023879a01e2620a0b9260265a98e7d9e4bd`  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed  
**Market data / target labels / P&L:** not loaded or calculated

## 1. Objective

Acquire the full allowed historical public-calendar consensus layer for EXP-041 and determine whether the free source supplies enough independent macro event blocks for the already-frozen Gate A.

This stage is **not** the final official-release reconciliation.

It establishes:

- event-family coverage;
- historical Forecast consensus availability;
- Actual/Previous availability for later cross-checking;
- independent-event counts;
- source-page provenance/hashes;
- whether the free consensus layer is large enough to justify official reconciliation.

## 2. Consensus source

Forex Factory historical calendar.

Frozen role:

- `Forecast` = `PUBLIC_CALENDAR_CONSENSUS_FF`;
- `Actual` and `Previous` = diagnostic values only until reconciled against official releases;
- Forex Factory event time = diagnostic only, not final release-time authority.

No event-specific substitution with another consensus vendor is allowed after outcomes.

## 3. Allowed acquisition interval

Normalized event date must satisfy:

`2025-07-01 <= event date <= 2026-06-29`

Historical page acquisition:

- weekly pages from week of 2025-06-30 through week of 2026-06-22;
- one day-only page for 2026-06-29.

Do **not** request the week of 2026-06-29 because that weekly page would also contain July 2026 protected dates.

Do not request any page containing Jul-Aug-Sep 2026.

## 4. Frozen target families

### EMPLOYMENT

- Non-Farm / Nonfarm Payrolls;
- Unemployment Rate;
- Average Hourly Earnings.

### CPI

- CPI;
- Core CPI / Core Inflation;
- Inflation Rate when clearly CPI-family.

### PPI

- PPI;
- Producer Price.

### RETAIL

- Retail Sales;
- Core / ex-auto retail where present.

### GDP_PCE

- GDP;
- GDP Price;
- PCE / Core PCE;
- Personal Income;
- Personal Spending.

### FOMC

- FOMC statement/minutes where explicitly policy-event relevant;
- Federal Funds / Fed Interest Rate decision.

FOMC is permitted to remain timing-only if the frozen six-event minimum is not met.

## 5. Normalized record schema

For every targeted USD row store:

- source = `ForexFactory`;
- source_page_url;
- source_page_sha256;
- event_id when exposed;
- event_date;
- displayed_time;
- currency;
- family;
- event_name;
- actual_text;
- forecast_text;
- previous_text;
- has_actual;
- has_forecast;
- has_previous.

No raw HTML is committed.

## 6. Independent event-block rule

Rows belong to the same independent event block when they share:

1. normalized event date;
2. family;
3. displayed release time when available.

If displayed time is unavailable, same-date + same-family rows are one provisional block.

This grouping is **provisional** until official release-time reconciliation.

Multiple components at the same release timestamp are never counted as separate independent economic events.

## 7. Surprise-bearing block

A provisional event block is surprise-bearing when at least one component contains:

- non-empty Forecast; and
- non-empty Actual.

Forex Factory Actual is diagnostic at this stage. Final surprise computation later uses official actual-as-released.

## 8. Frozen acquisition/coverage gate

Consensus-layer PASS requires:

1. every requested historical page returns HTTP 200;
2. every page exposes Actual / Forecast / Previous columns;
3. no requested or retained row is after 2026-06-29;
4. at least one targeted USD row is found in every primary numeric family;
5. >=40 provisional independent event blocks total across target families;
6. >=30 surprise-bearing provisional blocks;
7. >=8 provisional blocks each for:
   - EMPLOYMENT;
   - CPI;
   - PPI;
   - RETAIL;
   - GDP_PCE;
8. FOMC count is reported; if <6, FOMC is marked timing-only rather than failing the numeric-family gate;
9. normalized rows contain no duplicate `event_id` + component identity where event_id exists;
10. no market data, target labels, P&L or protected periods are loaded.

PASS disposition:

`FREE_CONSENSUS_LAYER_GATE_A_COVERAGE_PASS_OFFICIAL_RECONCILIATION_REQUIRED`

Failure disposition:

`FREE_CONSENSUS_LAYER_INSUFFICIENT_OR_PARSER_REPAIR_REQUIRED`

## 9. Raw-page provenance

For every requested public page record:

- requested URL;
- HTTP status;
- response byte count;
- SHA-256;
- week/day label;
- parsed targeted-row count.

Raw HTML is not committed.

## 10. Next stage after PASS

Freeze official-release reconciliation for the exact provisional event blocks:

- BLS Employment/CPI/PPI archives;
- Census Monthly Retail Trade releases;
- BEA GDP/PCE archives;
- Federal Reserve FOMC archives.

For every block verify:

- official release date/time;
- official actual-as-released component values;
- revision notes/previous-as-released where available;
- family/package identity.

The final causal surprise layer becomes:

`official actual-as-released - frozen FF historical Forecast consensus`

Only after official reconciliation and the full Gate-A audit pass may EXP-041 Gate B load the canonical Dukascopy snapshot and calculate target/path labels.
