# EXP-041 Free Macro Consensus / Official-Release Source Preflight v0.1

**Frozen:** 2026-09-27  
**Type:** zero-outcome public-data access/provenance preflight  
**Supersedes active dependence on:** Trading Economics credentialed PIT preflight for the next acquisition attempt  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed

## 1. Triggering result

Trading Economics preflight durable result:

- commit: `6eeb4e93f937fb51e6b2db39d7d57aeb11cf4023`;
- disposition: `CREDENTIAL_REQUIRED`;
- no market data, labels, P&L or protected-period data were loaded.

The project will not purchase or require a paid API merely to continue EXP-041 while a defensible free-source architecture is available.

## 2. Free-source architecture

### 2.1 Consensus / expectation source

Primary public consensus proxy:

- **Forex Factory historical calendar**
- historical week URL form: `https://www.forexfactory.com/calendar?week=<monDD.YYYY>`
- public historical pages expose `Actual / Forecast / Previous` and event identity.

Use only the historical page for the requested development week. Never request Jul-Aug-Sep 2026 pages in EXP-041 development.

The `Forecast` field is frozen as:

`PUBLIC_CALENDAR_CONSENSUS_FF`

It is a vendor consensus proxy, not a claim to represent every economist or every terminal.

Important limitation:

Forex Factory states that calendar times are approximate and the calendar can change as information is updated. Therefore Forex Factory is **not** the authority for release time or actual-as-released values.

### 2.2 Official release-time / actual authorities

- EMPLOYMENT: U.S. Bureau of Labor Statistics Employment Situation archive.
- CPI: U.S. Bureau of Labor Statistics CPI archive.
- PPI: U.S. Bureau of Labor Statistics PPI archive.
- RETAIL: U.S. Census Bureau Monthly Retail Trade historical releases.
- GDP/PCE: U.S. Bureau of Economic Analysis news-release archive / data archive.
- FOMC: Federal Reserve Board archived FOMC statements / meeting materials.

The official archive is authoritative for:

- release date/time;
- actual-as-released value;
- package composition;
- revision disclosure where present.

## 3. Why this combination is scientifically preferable to a single free calendar

The free calendar supplies the one field official statistical agencies generally do not publish:

- pre-release market consensus / forecast.

The official agency supplies the fields most vulnerable to later revision or calendar ambiguity:

- exact release timing;
- original released actual;
- revision notes.

Therefore the causal record becomes:

`official release time + official actual-as-released + frozen public-calendar forecast consensus`

rather than trusting one third-party calendar for everything.

## 4. Preflight scope

Use development dates only.

Forex Factory historical pages to request:

- week of 2026-06-01 — Employment sample;
- week of 2026-06-08 — CPI/PPI sample;
- week of 2026-06-15 — Retail/FOMC sample;
- week of 2026-06-22 — GDP/PCE sample.

Official pages to verify:

- BLS Employment archive for 2026-06-05;
- BLS CPI archive for 2026-06-10;
- BLS PPI archive for 2026-06-11;
- Census Retail historical releases index;
- BEA GDP/PCE June 25 releases or archive;
- Federal Reserve June 17 FOMC statement.

No request may target a date after 2026-06-29.

## 5. Frozen access/provenance gate

PASS requires:

1. all four Forex Factory historical week pages return HTTP 200;
2. historical page content contains the calendar columns `Actual`, `Forecast`, `Previous`;
3. USD rows can be detected;
4. representative targeted families are found:
   - Employment;
   - CPI;
   - PPI;
   - Retail;
   - GDP/PCE;
   - FOMC;
5. at least Employment/CPI/PPI/Retail/GDP-PCE representative rows contain non-empty Forecast values;
6. official BLS Employment/CPI/PPI pages return successfully and expose the expected release date/time text;
7. Census retail historical-release index is reachable;
8. BEA GDP/PCE archive/release pages are reachable;
9. Federal Reserve FOMC archive/statement is reachable;
10. no protected-period page is requested;
11. no market target labels, market prices, P&L or strategy outcomes are computed.

PASS disposition:

`FREE_MACRO_SOURCE_ARCHITECTURE_PREFLIGHT_PASS`

## 6. Full acquisition after PASS

The next stage will prospectively freeze one full development-only acquisition for:

`2025-07-01 <= release time < 2026-06-30 00:00 UTC`

For every macro component store:

- event block id;
- family;
- component;
- official release timestamp UTC;
- official actual-as-released;
- Forex Factory historical Forecast consensus;
- Forex Factory Previous for diagnostics only;
- official revision notes / previous-as-released where available;
- source URLs;
- retrieval timestamp;
- raw-page SHA-256 or normalized-record SHA-256.

Simultaneous components remain one independent event block.

## 7. Consensus-quality rule

Before any Gate-B outcome modeling:

- consensus source is frozen prospectively as Forex Factory historical `Forecast`;
- no event-specific source shopping is allowed;
- missing Forecast => that component cannot contribute a surprise value;
- official actual vs FF actual disagreement => use official actual, record discrepancy;
- ambiguous/missing official release time => event cannot enter surprise modeling until resolved;
- no post-hoc replacement with another vendor because a surprise looks more favorable.

## 8. Optional free corroboration

Investing.com and Myfxbook public historical pages may be used only for **descriptive spot-checks** on development events, not as outcome-dependent replacement consensus sources.

They are not required for Gate A and must not cause Jul-Aug/Sep 2026 rows to be loaded into the acquisition pipeline.

## 9. Scientific boundary

This preflight and subsequent acquisition are data infrastructure.

No:

- target/path labels;
- P&L;
- strategy filtering;
- protected future periods;
- Engine R development.

Only after the full macro dataset passes the already-frozen independent-event Gate A may EXP-041 Gate B begin.
