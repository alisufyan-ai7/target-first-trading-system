# EXP-042 Proxy Availability-Stratified Preflight v0.3

Frozen 2026-09-27. Zero-outcome. Supersedes the unexecuted v0.2 draft.

v0.1 failed because both proxy CFDs were not fresh around every one of the 57 post-release-eligible macro timestamps. The immutable proxy snapshot itself passed repeatability.

v0.3 independently reads the immutable proxy files and freezes two availability-defined event universes before any target outcome is loaded.

## Immutable inputs

- release tag: exp042-rates-usd-proxy-m1-2025-07-01_2026-06-30-v1
- archive SHA-256: 86cef306c36f08a12510c563e307a3158dc45d3236a424251db4d1c1bbaedcb4
- DOLLARIDXUSD SHA-256: 2f070a99784a60f15e9afe5cb1c906f1ded22aedaa74205cd3a286adefb839d2
- USTBONDTRUSD SHA-256: e1ff7bea80f40b1529e046a7b0f7b4c6265cc147ee8c6c324ddef05cc7c5acf7
- exact Gate-A macro timestamps/folds

## Frozen geometry

Structural decision grid remains weekdays 06:05-17:55 UTC every 5 minutes.

Post-release decision eligibility:
event_ts <= decision_ts <= event_ts + 180 minutes.

The pure time grid must reproduce 65 total Gate-A timestamps, 57 structurally eligible timestamps, and the same eight late FOMC timestamps as structurally ineligible.

## Causal availability rule

For each structurally eligible event and each proxy independently:

- baseline is the last M1 close strictly before release;
- baseline staleness must be >0 and <=5 minutes;
- at each legal decision timestamp, current proxy value is the last M1 close strictly before decision;
- decision-time observation staleness must be >0 and <=5 minutes;
- at least one legal decision timestamp must be covered;
- per-event decision-time coverage must be >=80%.

No imputation or stale carry-forward beyond five minutes.

## Frozen subsets

DXY_COMPLETE:
events where DOLLARIDXUSD passes the independent rule.

DXY_TBOND_COMPLETE:
events where both DOLLARIDXUSD and USTBONDTRUSD independently pass.

The exact event timestamp lists emitted by this run become immutable modeling universes.

## Adequacy gate for each subset

Reuse original Gate-A minima:

- >=40 independent event timestamps;
- EMPLOYMENT, CPI, PPI, RETAIL, GDP_PCE each >=8 timestamps;
- every frozen fold >=4 subset events;
- every frozen fold >=2 represented families.

If DXY_COMPLETE passes, future Study A may test:
LOCAL_M5 + EVENT_TIME_CONTROL -> +DXY_REACTION.

If DXY_TBOND_COMPLETE passes, future Study B may test:
LOCAL_M5 + EVENT_TIME_CONTROL + DXY_REACTION -> +DXY_TBOND_INTERPRETATION.

Within each study baseline and enriched models must use identical rows. Do not compare absolute performance across the two different availability subsets.

This run must not load target-market bars, target/path labels, model outcomes, P&L, Jul-Aug 2026, or Sep 2026.
