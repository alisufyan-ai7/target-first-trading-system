# EXP-041 Official Release-Time Reconciliation v0.3

**Frozen:** 2026-09-27  
**Supersedes:** v0.2 source-mapping implementation only  
**Input:** exact frozen `research/data/EXP-041-free-macro-consensus-v0.3.json`  
**Type:** zero-outcome BEA schedule parser repair  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed

## 1. Triggering v0.2 result

Durable v0.2 result: `83b12d3673fb770854f12e93b3c479d7a3f79743`.

Resolved completely:

- EMPLOYMENT 11/11;
- CPI 11/11;
- PPI 11/11;
- RETAIL 12/12;
- FOMC 8/8.

Only 14 BEA 2026 blocks remained unresolved:

- GDP + PCE on 2026-01-22;
- GDP + PCE on 2026-02-20;
- GDP + PCE on 2026-03-13;
- GDP + PCE on 2026-04-09;
- GDP + PCE on 2026-04-30;
- GDP + PCE on 2026-05-28;
- GDP + PCE on 2026-06-25.

The official BEA 2026 schedule visibly contains these rows. Therefore the remaining failure is the HTML schedule parser, not missing source data.

## 2. Frozen v0.3 repair

All non-BEA mappings remain byte-for-byte logic-equivalent to v0.2.

For BEA only:

1. fetch the official full-year schedule page;
2. inspect schedule-row containers and linked release anchors;
3. for each row extract:
   - displayed date;
   - displayed time;
   - release title;
   - linked first-party release URL when available;
4. normalize split text such as `N ews`;
5. match exact frozen event date;
6. classify release title:
   - GDP if title contains `Gross Domestic Product` or begins/contains `GDP`;
   - PCE if title contains `Personal Income and Outlays`;
7. require exactly one row for each frozen date + release kind;
8. use that exact row's local time;
9. preserve separate GDP/PCE official blocks even when they share a date;
10. convert America/New_York to UTC with zoneinfo.

Do not hard-code 8:30 AM for BEA.

## 3. First-party corroboration

Where the schedule row exposes a first-party release link, save it as:

`official_release_page_url`

The schedule page remains the timestamp authority for Phase A; the direct release page will be used in Phase B actual-as-released parsing.

## 4. Frozen gate

Same as v0.2, plus:

- exactly 11 GDP blocks;
- exactly 11 PCE blocks;
- all 22 BEA sub-blocks have matched schedule rows;
- all 2026 BEA sub-blocks expose release links where available;
- no unresolved official block remains.

PASS disposition:

`OFFICIAL_RELEASE_TIME_RECONCILIATION_V03_PASS_ACTUAL_VALUES_REQUIRED`

No market data/outcomes are loaded.
