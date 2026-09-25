# EXP-040 — MTF Structural Context Source / Split Manifest

**Frozen:** 2026-09-25  
**Experiment:** EXP-040  
**Type:** information-content study

## Source markets

Use only the repository-pinned M1 research sources for:

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

No external macro/order-flow data are introduced in EXP-040.

## Purpose of this stage

EXP-040 tests the first information layer that can be constructed from already-admitted data:

- 15M;
- 1H;
- 4H;
- previous completed day;
- fixed UTC session-location context.

It is a bridge between the OHLC-only root-cause audit and later genuinely external information families.

## Hard source seal

- earliest reusable source: 2026-03-23;
- latest permitted parsed timestamp: 2026-06-30 23:59 UTC;
- any row >=2026-07-01 00:00 UTC is forbidden.

The durable result must report parsed maximum timestamp.

## Protected periods

Must remain unloaded/unlabeled:

- secondary: 2026-07-01 through 2026-08-31;
- final holdout: September protected sample.

## Causality

At decision time t:

- local M5 decision bar is complete;
- 15M/1H/4H context uses only bars whose `available_ts <= t`;
- previous-day features use only a fully prior UTC trading day;
- Asia proxy is used only after 06:00 UTC;
- London proxy is used only after 12:00 UTC;
- target labels begin at the first active M1 open after the decision;
- target/stop on same M1 bar uses stop-first ordering.

## Split protection

Six evaluation folds are fixed in EXP-040.

A 120-minute purge is applied before each calibration/evaluation boundary.

No outcome-driven fold movement is permitted.

## Outcome declaration at freeze

- EXP-040 labels calculated: NO;
- Jul-Aug loaded/labeled: NO;
- September loaded/labeled: NO;
- Engine-R target/P&L development: PAUSED.
