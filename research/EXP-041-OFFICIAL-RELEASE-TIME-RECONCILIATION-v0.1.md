# EXP-041 Official Release-Time Reconciliation v0.1

**Frozen:** 2026-09-27  
**Input:** `research/data/EXP-041-free-macro-consensus-v0.3.json`  
**Input SHA-256:** must equal the durable v0.3 scope audit value at runtime  
**Type:** zero-outcome first-party provenance/timestamp reconciliation  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed

## 1. Objective

Map every cleaned v0.3 provisional event block to a first-party U.S. government source and assign an authoritative release timestamp in UTC.

This stage does **not** yet reconcile every component's actual-as-released numeric value. That is the next separately frozen stage.

The split is deliberate:

1. Phase A — source identity + official release time;
2. Phase B — component-level official actual-as-released extraction/reconciliation.

No market data or outcomes are loaded in either phase.

## 2. First-party authorities

### EMPLOYMENT

U.S. Bureau of Labor Statistics Employment Situation archive.

Direct archive pattern:

`https://www.bls.gov/news.release/archives/empsit_MMDDYYYY.htm`

Expected release time: 8:30 a.m. U.S. Eastern, verified on each archived release page.

### CPI

U.S. Bureau of Labor Statistics CPI archive:

`https://www.bls.gov/news.release/archives/cpi_MMDDYYYY.htm`

Expected release time: 8:30 a.m. U.S. Eastern.

### PPI

U.S. Bureau of Labor Statistics PPI archive:

`https://www.bls.gov/news.release/archives/ppi_MMDDYYYY.htm`

Expected release time: 8:30 a.m. U.S. Eastern.

### RETAIL

U.S. Census Bureau Monthly Retail Trade release schedule / historical releases.

Primary timing authority:

`https://www.census.gov/retail/release_schedule.html`

The Advance Monthly Retail Trade release time is 8:30 a.m. U.S. Eastern. Every retained v0.3 RETAIL date must be present in the official schedule.

### GDP_PCE

U.S. Bureau of Economic Analysis release schedules:

- `https://www.bea.gov/news/schedule/full-2025`
- `https://www.bea.gov/news/schedule/full-2026`

Every retained v0.3 GDP/PCE date must occur as an 8:30 a.m. BEA News release relevant to GDP or Personal Income and Outlays.

### FOMC

Federal Reserve Board archived policy statement:

`https://www.federalreserve.gov/monetarypolicy/monetaryYYYYMMDDa.htm`

Every retained FOMC date must resolve to a policy statement page released at 2:00 p.m. U.S. Eastern.

## 3. Timestamp conversion

Use IANA timezone:

`America/New_York`

Convert the authoritative local release time on the event date to UTC using Python `zoneinfo`.

This automatically handles EDT/EST without hard-coded month offsets.

## 4. Input integrity

Before network access:

1. read durable v0.3 scope audit;
2. verify input dataset SHA-256 exactly;
3. require v0.3 consensus gate PASS;
4. require no protected-period flags.

Fail closed on mismatch.

## 5. Frozen reconciliation gate

For every v0.3 provisional event block require:

- a recognized first-party authority;
- official source URL or official schedule URL;
- HTTP 200 for required direct pages;
- date present in official schedule/page;
- expected official release-time marker present;
- computed UTC release timestamp;
- timestamp date remains within allowed development interval;
- no block remains unresolved.

Additional family requirements:

- all 11 EMPLOYMENT dates resolve to BLS Employment Situation archives;
- all 11 CPI dates resolve to BLS CPI archives;
- all 11 PPI dates resolve to BLS PPI archives;
- all 12 RETAIL dates appear in Census official schedule;
- all 15 GDP_PCE dates appear in BEA official schedules at 8:30 AM;
- all 8 FOMC dates resolve to Federal Reserve policy statement pages at 2:00 PM.

PASS disposition:

`OFFICIAL_RELEASE_TIME_RECONCILIATION_PASS_ACTUAL_VALUES_REQUIRED`

## 6. Output

Create:

`research/data/EXP-041-official-release-time-map-v0.1.json`

For each block:

- block_id;
- family;
- event_date;
- official_authority;
- official_source_url;
- official_source_sha256 when direct page was fetched;
- official_local_timezone = America/New_York;
- official_local_release_time;
- official_release_timestamp_utc;
- source_date_verified;
- source_time_verified.

Do not store market outcomes.

## 7. Next stage after PASS

Freeze component-level official actual-as-released reconciliation using the exact v0.3 Forecast consensus records and the exact release-time map.

That next stage will parse:

- BLS NFP / unemployment / average hourly earnings;
- BLS CPI headline/core;
- BLS PPI headline/core;
- Census Retail headline/ex-auto;
- BEA GDP/GDP-price and PCE/income/spending;
- Federal Reserve target-rate decision.

The final surprise layer is not authorized until that component-level reconciliation passes.
