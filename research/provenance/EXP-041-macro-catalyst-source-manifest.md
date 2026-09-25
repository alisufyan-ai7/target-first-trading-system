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
