# EXP-041 Official Release-Time Reconciliation v0.2

**Frozen:** 2026-09-27  
**Supersedes:** official release-time reconciliation v0.1  
**Input:** `research/data/EXP-041-free-macro-consensus-v0.3.json`  
**Type:** zero-outcome first-party source/timestamp repair  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed

## 1. Why v0.2 exists

v0.1 durable result `a8bceb64027d48de9d2533d852a41d86f9c11e54` failed because the source-mapping implementation was incomplete:

- BLS Employment/CPI/PPI resolved 11/11 each;
- Retail resolved 9/12 using a generic current schedule;
- GDP/PCE resolved 0/15 because the BEA schedule parser assumed one 8:30 release and failed to parse the actual schedule structure;
- FOMC resolved 1/8 because the runner used the wrong Federal Reserve URL family for most statement pages.

The failure is therefore data plumbing, not evidence against the macro information layer.

Official-source inspection also revealed a real timing distinction: on some dates GDP and Personal Income & Outlays occur on the same day at different official times. A provisional `event_date + GDP_PCE` block must therefore be split by official release identity before timestamps are assigned.

No market outcomes have been computed, so this correction is prospective.

## 2. Frozen v0.2 corrections

### BLS

Keep the already-working direct archive mappings:

- Employment: `news.release/archives/empsit_MMDDYYYY.htm`;
- CPI: `news.release/archives/cpi_MMDDYYYY.htm`;
- PPI: `news.release/archives/ppi_MMDDYYYY.htm`.

Require archived date + 8:30 a.m. ET marker.

### Retail

Use direct first-party Census historical MARTS PDFs, not the mutable/current schedule page.

Frozen release-date -> official PDF mapping:

| Release date | Official PDF |
|---|---|
| 2025-07-17 | `adv2506.pdf` |
| 2025-08-15 | `adv2507.pdf` |
| 2025-09-16 | `adv2508.pdf` |
| 2025-11-25 | `adv2509.pdf` |
| 2025-12-16 | `adv2510.pdf` |
| 2026-01-14 | `adv2511.pdf` |
| 2026-02-10 | `adv2512.pdf` |
| 2026-03-06 | `adv2601.pdf` |
| 2026-04-01 | `adv2602.pdf` |
| 2026-04-21 | `adv2603.pdf` |
| 2026-05-14 | `adv2604.pdf` |
| 2026-06-17 | `adv2605.pdf` |

Base URL:

`https://www2.census.gov/retail/releases/historical/marts/`

For each PDF verify first-page release header contains the exact release date and 8:30 AM EST/EDT.

### BEA GDP / PCE

Parse the official BEA 2025 and 2026 release-schedule rows.

Split each frozen `GDP_PCE` provisional date into one or two official sub-blocks:

- `GDP` for component names containing GDP;
- `PCE` for Core PCE / Personal Income / Personal Spending.

For each sub-block:

- match exact event date;
- GDP title must contain `Gross Domestic Product` or begin with `GDP`;
- PCE title must contain `Personal Income and Outlays`;
- take the official time from that exact BEA schedule row;
- convert that time from America/New_York to UTC.

Do not assume all BEA releases are 8:30 AM. If GDP and PCE have different times on the same date, preserve separate official blocks/timestamps.

### FOMC

Use the correct Federal Reserve press-release URL:

`https://www.federalreserve.gov/newsevents/pressreleases/monetaryYYYYMMDDa.htm`

Require exact statement date and `For release at 2:00 p.m. EST/EDT`.

## 3. Official-block construction

For EMPLOYMENT/CPI/PPI/RETAIL/FOMC:

- retain one official block per frozen v0.3 provisional date+family.

For GDP_PCE:

- split by official release identity (`GDP` vs `PCE`) based only on frozen component names.

This may increase the official event-block count relative to provisional v0.3. That is a timestamp/provenance correction, not a sample-threshold change.

## 4. Frozen gate

PASS requires:

1. exact v0.3 input SHA verified;
2. all BLS blocks resolved;
3. all 12 Retail blocks resolved to direct official PDFs;
4. every GDP component group resolves to a matching BEA GDP schedule row;
5. every PCE component group resolves to a matching BEA Personal Income and Outlays schedule row;
6. all 8 FOMC policy dates resolve to official Fed statement pages;
7. every official block has source URL, source hash, local time and UTC timestamp;
8. every frozen v0.3 component record belongs to exactly one official block;
9. no protected-period or market-outcome use.

PASS disposition:

`OFFICIAL_RELEASE_TIME_RECONCILIATION_V02_PASS_ACTUAL_VALUES_REQUIRED`

## 5. Next step after PASS

Freeze Phase B: component-level official actual-as-released reconciliation against:

- frozen v0.3 Forex Factory Forecast consensus;
- frozen v0.2 official release-time map.

Only after Phase B passes may the final Gate-A adequacy audit authorize EXP-041 information-content modeling.
