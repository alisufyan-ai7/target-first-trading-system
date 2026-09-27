# EXP-042 Rates/USD Proxy Event-Coverage Preflight v0.1

**Frozen:** 2026-09-27  
**Type:** zero-outcome causal availability audit  
**Proxy snapshot:** `exp042-rates-usd-proxy-m1-2025-07-01_2026-06-30-v1`  
**Archive SHA-256:** `86cef306c36f08a12510c563e307a3158dc45d3236a424251db4d1c1bbaedcb4`

## Purpose

Before any EXP-042 target/path labels or model are loaded, verify that the immutable DXY and US T-Bond proxies are causally available around the frozen Gate-A macro timestamps.

## Frozen event geometry

Reuse the EXP-040 structural decision grid:

- weekdays;
- 06:05 through 17:55 UTC;
- every five minutes.

EXP-042 is a post-release interpretation study, so allowed decision timestamps are:

`event_ts <= decision_ts <= event_ts + 180 minutes`.

Frozen Gate-A event count: 65.

Pure time-grid geometry yields exactly 57 eligible events. The eight ineligible events must be exactly the eight FOMC timestamps:

- 2025-07-30T18:00:00Z;
- 2025-09-17T18:00:00Z;
- 2025-10-29T18:00:00Z;
- 2025-12-10T19:00:00Z;
- 2026-01-28T19:00:00Z;
- 2026-03-18T18:00:00Z;
- 2026-04-29T18:00:00Z;
- 2026-06-17T18:00:00Z.

All eight must be FOMC.

## Causal proxy availability

For each of the 57 eligible events and for each proxy:

1. pre-event baseline = last M1 close strictly before event timestamp;
2. baseline staleness must be <=5 minutes;
3. at every legal structural decision timestamp, causal current price = last M1 close strictly before decision timestamp;
4. current-price staleness must be <=5 minutes.

No bar timestamp equal to the structural decision timestamp may be used in a feature.

## Frozen coverage gate

Require:

- immutable archive SHA exact;
- per-file SHA exact to the durable snapshot result;
- 65 Gate-A timestamps exact;
- 57 geometrically eligible exact;
- eight ineligible timestamps exact and all FOMC;
- both proxy baselines available for every eligible event;
- each eligible event has at least one common legal decision timestamp with both proxies available;
- each eligible event has common both-proxy coverage >=80% of its legal decision timestamps;
- pooled common both-proxy coverage >=95%;
- every frozen fold retains >=8 proxy-covered eligible events;
- no target-market data, target labels, P&L or protected Jul-Aug/Sep 2026 data.

PASS disposition:

`EXP042_PROXY_EVENT_COVERAGE_PASS_AUTHORIZE_INFORMATION_CONTENT_DESIGN`

FAIL disposition:

`EXP042_PROXY_EVENT_COVERAGE_FAIL_DO_NOT_MODEL`.

This audit does not inspect target outcomes.
