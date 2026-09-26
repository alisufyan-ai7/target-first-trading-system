# EXP-041 — Macro / Catalyst Source Manifest v0.1

**Frozen:** 2026-09-25

## Market-data rule

Current repository-pinned sources begin effectively in March 2026.

For serious macro information-content research, EXP-041 requires an **earlier development extension** ending at the existing Jun30 hard boundary.

Target minimum:

- at least 12 months of development history;
- preferred window: 2025-07-01 through 2026-06-30.

Do not use Jul-Aug/Sep 2026 to satisfy this requirement.

## Release timestamp authorities

Use first-party release schedules/press releases where available:

- U.S. Bureau of Labor Statistics — Employment, CPI, PPI;
- U.S. Census Bureau — retail sales and other Census indicators;
- U.S. Bureau of Economic Analysis — GDP and Personal Income/Outlays;
- Federal Reserve — FOMC statement/projection release time.

All event timestamps must be stored in UTC with original source timezone noted.

## Consensus / actual-as-released source

Preferred research source:

- Trading Economics Economic Calendar point-in-time data, because its schema exposes timestamp, Actual, Previous, Forecast/consensus, revision fields and event importance.

Alternative acceptable source:

- Econoday historical calendar/consensus data with actual-as-released and revisions.

For the short March-June 2026 seed only, historical Trading Economics calendar pages may be curated manually and cross-checked against official release schedules.

Before model promotion, use point-in-time/API or licensed historical archives rather than relying on manually indexed pages.

## Causality

- consensus must be the value available before release;
- actual/surprise features are unavailable before the release timestamp;
- later revisions may not overwrite the original actual-as-released value used for causal backtesting;
- FOMC statement text/sentiment is not introduced in v0.1;
- speeches/unscheduled geopolitical news are out of scope for v0.1.

## Protection

- current Jul-Aug secondary remains sealed;
- Sep final holdout remains sealed;
- no future macro rows are used to extend sample size.


## 2026-09-27 — Point-in-time access preflight

The preferred Trading Economics path is now prospectively frozen as a zero-outcome access/provenance preflight before full-year acquisition.

Frozen public API contract:

- historical U.S. calendar endpoint by date range;
- `Forecast` = survey consensus;
- `Actual` = released value;
- `Previous` and `Revised` available for prior-value revision state;
- `CalendarId`, `Date`, `Category`, `Event`, `Source`, `SourceURL`, `LastUpdate` retained for provenance;
- point-in-time/historical calendar access is required for causal backtesting.

Credential secret name:

`TRADING_ECONOMICS_API_KEY`

Preflight artifacts:

- `research/EXP-041-MACRO-PIT-ACCESS-PREFLIGHT-v0.1.md`;
- `research/code/run_exp041_macro_pit_access_preflight.py`;
- `.github/workflows/exp041-macro-pit-access-preflight.yml`.

The preflight queries only 2026-03-01 through 2026-06-29 development dates and commits no raw licensed vendor payload or secret. It stores only schema/coverage metadata and a response SHA-256.

If credentials/entitlement are unavailable, fail closed with a durable diagnostic and do not substitute post-hoc web calendar pages for missing point-in-time consensus.
