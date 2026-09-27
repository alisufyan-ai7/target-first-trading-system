# EXP-041 Official Release-Time Reconciliation v0.4 — Direct BEA Release Pages

**Frozen:** 2026-09-27  
**Base map:** `research/data/EXP-041-official-release-time-map-v0.2.json`  
**Base map SHA-256:** `691c09da1829695821ead84647bb87b2b1b4c1a4cdc4d727cb33042e991edd1a`  
**Type:** zero-outcome targeted first-party mapping repair  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed

## 1. Why v0.4 exists

v0.3 durable result `b340e2878cf442196e5c5d6d640451c2f93a99e5` confirmed that schedule-HTML parsing remains brittle:

- 2026 BEA schedule rows parsed as zero;
- 2025 BEA rows were duplicated by overlapping parser strategies;
- all non-BEA mappings already worked.

The individual BEA news-release pages are first-party and preserve the exact embargo timestamp and original release content. They are also the source required for Phase B actual-as-released reconciliation.

Therefore v0.4 stops scraping BEA schedule layouts entirely.

## 2. Frozen recovery strategy

Start from the exact v0.2 official-time map.

Preserve every already-resolved block unchanged:

- EMPLOYMENT 11;
- CPI 11;
- PPI 11;
- RETAIL 12;
- FOMC 8;
- 2025 BEA GDP/PCE 8 blocks.

Replace only these 14 unresolved 2026 BEA blocks using direct first-party release pages.

## 3. Frozen 2026 BEA direct-page manifest

| Official block | First-party BEA release page | Expected local time |
|---|---|---:|
| 2026-01-22 GDP | `https://www.bea.gov/news/2026/gross-domestic-product-3rd-quarter-2025-updated-estimate-gdp-industry-and-corporate` | 08:30 EST |
| 2026-01-22 PCE | `https://www.bea.gov/news/2026/personal-income-and-outlays-october-and-november-2025` | 10:00 EST |
| 2026-02-20 GDP | `https://www.bea.gov/news/2026/gdp-advance-estimate-4th-quarter-and-year-2025` | 08:30 EST |
| 2026-02-20 PCE | `https://www.bea.gov/news/2026/personal-income-and-outlays-december-2025` | 08:30 EST |
| 2026-03-13 GDP | `https://www.bea.gov/news/2026/gdp-second-estimate-4th-quarter-and-year-2025` | 08:30 EDT |
| 2026-03-13 PCE | `https://www.bea.gov/news/2026/personal-income-and-outlays-january-2026` | 08:30 EDT |
| 2026-04-09 GDP | `https://www.bea.gov/news/2026/gdp-third-estimate-industries-corporate-profits-state-gdp-and-state-personal-income-4th` | 08:30 EDT |
| 2026-04-09 PCE | `https://www.bea.gov/news/2026/personal-income-and-outlays-february-2026` | 08:30 EDT |
| 2026-04-30 GDP | `https://www.bea.gov/news/2026/gdp-advance-estimate-1st-quarter-2026` | 08:30 EDT |
| 2026-04-30 PCE | `https://www.bea.gov/news/2026/personal-income-and-outlays-march-2026` | 08:30 EDT |
| 2026-05-28 GDP | `https://www.bea.gov/news/2026/gdp-second-estimate-and-corporate-profits-1st-quarter-2026` | 08:30 EDT |
| 2026-05-28 PCE | `https://www.bea.gov/news/2026/personal-income-and-outlays-april-2026` | 08:30 EDT |
| 2026-06-25 GDP | `https://www.bea.gov/news/2026/gdp-third-estimate-industries-corporate-profits-state-gdp-and-state-personal-income-1st` | 08:30 EDT |
| 2026-06-25 PCE | `https://www.bea.gov/news/2026/personal-income-and-outlays-may-2026` | 08:30 EDT |

This manifest is frozen before the CI result.

## 4. Verification rule for each direct page

Require all of:

1. HTTP 200;
2. exact expected release date appears;
3. `EMBARGOED UNTIL RELEASE AT` appears;
4. exact expected local time appears;
5. timezone abbreviation is consistent with America/New_York for the date;
6. GDP pages contain GDP / Gross Domestic Product release identity;
7. PCE pages contain `Personal Income and Outlays`;
8. source SHA-256 recorded;
9. UTC timestamp calculated with `America/New_York` and must agree with the stated EST/EDT abbreviation.

No schedule-page fallback is permitted.

## 5. Protected-period rule

Do not fetch:

- BEA full-year 2026 schedule pages;
- July-Aug-Sep 2026 release pages;
- any market data.

Only the 14 explicitly frozen 2026 BEA pages above may be newly fetched.

## 6. Frozen pass gate

PASS requires:

- base v0.2 map SHA verified;
- exactly 14 unresolved 2026 BEA blocks found before repair;
- all 14 direct pages verify;
- after repair, all 75 official blocks have source URL/hash/date/time/UTC timestamp;
- all original component-record memberships remain unchanged;
- no non-BEA or 2025-BEA block changed;
- no protected-period or market-outcome use.

PASS disposition:

`OFFICIAL_RELEASE_TIME_RECONCILIATION_V04_PASS_ACTUAL_VALUES_REQUIRED`

## 7. Next stage

Freeze Phase B official actual-as-released reconciliation using:

- frozen consensus v0.3;
- frozen official-time map v0.4;
- the direct release pages already recorded in the v0.4 map.

No further timing-source work is authorized after v0.4 PASS unless a direct source itself fails validation.
