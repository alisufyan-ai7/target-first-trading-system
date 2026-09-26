# EXP-041 Macro Point-in-Time Access / Provenance Preflight v0.1

**Frozen:** 2026-09-27  
**Type:** zero-outcome external-data access/provenance preflight  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed  
**Market data:** canonical immutable Dukascopy snapshot v2; not loaded in this preflight

## 1. Objective

Before acquiring a full year of macro/catalyst history, verify that the preferred historical calendar source can supply the causal fields required by EXP-041:

- scheduled event timestamp;
- event/category identity;
- Actual as released;
- Forecast = survey consensus;
- Previous;
- Revised where applicable;
- source/provenance;
- point-in-time historical access.

This stage computes no market labels, no strategy outcomes and no P&L.

## 2. Preferred source

Trading Economics Economic Calendar API.

Current public API documentation states:

- historical calendar queries support country + date range;
- `Forecast` is consensus from a representative group of economists;
- `Actual`, `Previous`, `Revised`, `Date`, `Source`, `SourceURL`, `LastUpdate`, `CalendarId` and related fields are exposed;
- point-in-time calendar data is intended to preserve the historical information state for backtesting/audit use.

Documentation references:

- https://docs.tradingeconomics.com/economic_calendar/point-in-time/
- https://docs.tradingeconomics.com/economic_calendar/schema/
- https://api.tradingeconomics.com/swagger/index.html

Alternative source if PIT access is unavailable under the available Trading Economics entitlement:

- Econoday historical consensus + actual-as-released archive.

## 3. Credential handling

GitHub Actions secret:

`TRADING_ECONOMICS_API_KEY`

Rules:

- never print or commit the key;
- never commit a request URL containing the key;
- never store the key in artifacts;
- sanitize any API error payload before durable checkpointing.

If the secret is missing, the workflow must still create a durable result with:

`CREDENTIAL_REQUIRED`

and fail closed.

If credentials exist but the subscription does not permit the required historical calendar access, checkpoint:

`PIT_OR_HISTORICAL_ACCESS_REQUIRED`

and fail closed.

## 4. Frozen preflight interval

Query United States calendar data only for:

`2026-03-01 <= event date <= 2026-06-29`

This interval is already within development and contains the existing 17-event plumbing seed. It does not consume Jul-Aug or Sep 2026.

The preflight intentionally does not acquire July-September 2026 calendar data.

## 5. Required event-family detection

Classify returned U.S. calendar rows descriptively using event/category text only:

### EMPLOYMENT

- non farm payroll / nonfarm payroll;
- unemployment rate;
- average hourly earnings.

### CPI

- CPI;
- inflation rate;
- core inflation rate.

### PPI

- PPI;
- producer price.

### RETAIL

- retail sales.

### GDP_PCE

- GDP growth;
- GDP price;
- PCE price;
- core PCE;
- personal income;
- personal spending.

### FOMC

- FOMC;
- Fed interest rate;
- Federal Reserve policy/rate decision.

These aliases are access/schema plumbing only. They do not create trading features or outcome rules.

## 6. Frozen access gate

Preflight PASS requires all of:

1. API credential present;
2. HTTP request succeeds;
3. JSON response is a non-empty list;
4. no returned event is later than 2026-06-29;
5. every targeted row has `CalendarId`, `Date`, `Country`, `Category`, `Event`, `LastUpdate`;
6. each of EMPLOYMENT, CPI, PPI, RETAIL, GDP_PCE is represented;
7. each of those five numeric families has at least one row with non-empty `Actual` and non-empty `Forecast`;
8. at least one FOMC-related row is found; FOMC consensus is not required because v0.1 permits timing-only FOMC;
9. at least one targeted row exposes `Source` or `SourceURL`;
10. no raw vendor payload is committed; only response SHA-256, counts, schema availability and non-value sample identifiers/timestamps are checkpointed.

Pass disposition:

`TRADING_ECONOMICS_PIT_ACCESS_PREFLIGHT_PASS`

Failure dispositions are descriptive and must not trigger strategy fitting.

## 7. What the preflight does NOT prove

A pass does not yet prove full-year Gate-A sufficiency.

It only establishes that the preferred interface is technically available and contains the required causal fields on known development history.

After a pass, freeze and run a separate full-history acquisition/audit for 2025-07-01 through 2026-06-29.

## 8. Full-history stage after PASS

The subsequent acquisition must:

- retrieve the full allowed development interval;
- retain point-in-time consensus / Actual / Previous / Revised with source provenance;
- independently verify official release timestamps using BLS/Census/BEA/Fed sources;
- group simultaneous components into one event block;
- count independent events before any outcome modeling;
- require >=40 independent blocks, >=30 surprise-bearing blocks, >=8 releases per recurring numeric family;
- require >=6 FOMC events or retain FOMC as timing-only;
- freeze a reproducible macro data snapshot subject to vendor licensing constraints;
- keep Jul-Aug/Sep sealed.

Only after Gate A passes may EXP-041 Gate B compute market target/path labels.
