# EXP-041 HistData Timestamp-Semantics Diagnostic v0.1

**Date:** 2026-09-25  
**Status:** PROSPECTIVELY FROZEN — ZERO OUTCOME  
**Purpose:** determine whether the failed HistData third-source adjudication is explained by one common mechanical timestamp shift  
**Target labels / P&L:** NONE

## Background

EXP-041 third-source adjudication completed at durable result `3e5ed20a733bf80fc72c155c756edf7c115c566e`.

The frozen feed-selection gate failed:

- CURRENT_PINNED supported in 2/8 markets;
- DUKASCOPY supported in 2/8 markets;
- HISTDATA supported in 0/8 markets;
- six markets had `NO_TWO_SOURCE_CONSENSUS`.

No source was selected.

A specific data-engineering anomaly remains: HistData's 5m/1h return agreement with the other feeds is very weak while daily-return agreement is materially stronger on several markets. A common timestamp-semantics error can create that scale pattern even when both feeds occupy nearly every minute of the same date range.

This diagnostic tests only that mechanical hypothesis. It does not reopen the frozen feed-selection thresholds.

## Scope

Same overlap only:

`2026-03-23 00:00 UTC <= t < 2026-07-01 00:00 UTC`.

Sources:

1. CURRENT_PINNED — repository-pinned source;
2. DUKASCOPY — frozen Dukascopy overlap downloader;
3. HISTDATA — the exact HistData v0.1 transport/conversion output already used in adjudication.

No Jul-Aug/Sep 2026.

## Frozen shift grid

Apply one **common** timestamp shift to HistData after the existing v0.1 fixed-EST-to-UTC conversion.

Test integer-hour shifts only:

`-6, -5, -4, -3, -2, -1, 0, +1, +2, +3, +4, +5, +6 hours`.

The same shift must apply to every market.

Per-market custom shifts are prohibited.

This grid is designed to detect:

- a duplicated fixed-offset conversion;
- a fixed-EST vs daylight-saving interpretation difference;
- another whole-hour timestamp-basis error.

It is not a strategy parameter grid.

## Pairwise criteria

For every candidate common shift, rerun the **unchanged** third-source pairwise gate:

1. exact/common M1 overlap ratio of smaller feed >=70%;
2. 5m log-return correlation >=0.90;
3. 1h log-return correlation >=0.95;
4. 1d log-return correlation >=0.95;
5. 1h direction-sign agreement >=0.95.

CURRENT_PINNED↔DUKASCOPY is not shifted.

Only HistData timestamps move.

## Frozen adjudication replay

For each market and common shift, reuse the original tags:

- DUKASCOPY-HISTDATA passes while both CURRENT_PINNED pairs fail -> `CURRENT_PINNED_OUTLIER`;
- CURRENT_PINNED-HISTDATA passes while both DUKASCOPY pairs fail -> `DUKASCOPY_OUTLIER`;
- CURRENT_PINNED-DUKASCOPY passes while both HistData pairs fail -> `HISTDATA_OUTLIER`;
- at least two pairs pass -> `BROAD_THREE_SOURCE_CONSENSUS`;
- otherwise -> `NO_TWO_SOURCE_CONSENSUS`.

Replay the original feed-selection gate unchanged:

- one source supported by >=1 passing pair in >=7/8 markets; and
- no more than 1 market is `NO_TWO_SOURCE_CONSENSUS`.

## Decision rule

If **no** common shift passes the original feed-selection gate:

`TIMESTAMP_SHIFT_DOES_NOT_EXPLAIN_FAILURE_REQUIRE_FOURTH_OR_BROKER_SOURCE`.

Then stop HistData remediation and require intended-broker or another institutional-quality source before EXP-041 macro modeling.

If one or more common shifts pass:

`COMMON_TIMESTAMP_SHIFT_CAN_RESTORE_FROZEN_GATE_FREEZE_CORRECTED_ADJUDICATION_V02`.

This does **not** itself select HistData or authorize macro modeling.

Before a corrected adjudication v0.2, the winning common shift must be reconciled against source/tool timestamp semantics, then frozen prospectively. The original pairwise thresholds remain unchanged.

## Descriptive best-shift rule

For reporting only, rank common shifts by:

1. feed-selection gate pass (pass first);
2. maximum number of eligible >=7/8 sources;
3. minimum `NO_TWO_SOURCE_CONSENSUS` count;
4. maximum HistData supported-market count;
5. maximum median 1h correlation across the 16 HistData-vs-anchor market pairs;
6. smallest absolute shift;
7. smaller signed shift.

This ordering cannot modify the scientific decision rule above.

## Protection

- target labels: NO;
- P&L: NO;
- strategy selection: NO;
- no market-specific shift fitting;
- original pairwise thresholds unchanged;
- Jul-Aug: NO;
- Sep: NO;
- Engine R remains paused before target/P&L development.
