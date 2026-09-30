# Freeze — Mechanization v0.1 Phase 1

## Status

`MECHANIZATION_V0_1_PHASE1_FROZEN — VISUAL_REPRODUCIBILITY_PENDING`

## Evidence boundary

External Badar source evidence:

`d19a43da80ae0e3ab4207a73a35f317120d37c84`

Target-First corpus:

- 347 pre-entry decisions;
- 136 management decisions;
- no P&L/outcome/MFE/MAE join.

## Frozen Phase-1 findings

1. Location not reached/absent is a hard/pending gate.
2. Middle is a hard veto.
3. Chasing is a hard veto or WAIT-for-retrace state.
4. Undefined structural stop is a hard veto.
5. Failed confirmation is a hard veto.
6. Required close still pending is a WAIT state.
7. These six structured conditions hit 148/240 WAIT/NO_TRADE events and contradict 0/107 TRADE events in the source-informed corpus.
8. Structural stop existence belongs to strategy logic.
9. Stop sizeability belongs to the independent risk/broker layer.
10. Target-path state must be explicitly annotated; it is missing from all 347 current events.
11. Confirmation strength can be partially mechanized from source family rules but requires blinded chart reproducibility.
12. Required HTF timeframe is machine-ready only when the setup plan/source mapping makes the timeframe explicit.

## Frozen source-derived primitives

Safe/near-safe:

- PDH/PDL;
- session highs/lows;
- 3-candle FVG;
- premium/discount midpoint after BOS-leg freeze;
- sweep close-back;
- high-confidence two-close BOS/MSS state;
- structural invalidation basis.

Partial/unresolved:

- swing-selection width;
- hidden OB;
- equal-high/low tolerance;
- overlapping-POI ranking;
- ambiguous strong-vs-adequate confirmation;
- automatic required-HTF-timeframe selection.

## Forbidden before Phase 2

Do not:

- pick numeric thresholds from profitable trades;
- use future candles;
- infer target-path labels from eventual TP performance;
- choose a stop cutoff from winner/loser separation;
- treat source-informed Phase-1 annotation agreement as independent validation;
- launch an automated P&L backtest using unresolved visual classifiers;
- silently convert `UNRESOLVED` to TRADE.

## Next exact action

Build the **blinded timestamped chart-snapshot pack** for the 347 decision events, then execute the Phase-2 reproducibility protocol.

The snapshot pack must hide future bars and Badar's eventual decision.

Only after Phase 2 passes may a development P&L experiment be specified.


## Protected-data safeguard

A full repo-tree audit confirms Target-First has market-data acquisition infrastructure, but July–August and September 2026 are protected/sealed periods in existing data governance.

Mechanization v0.1 does **not** authorize opening those raw periods to recreate Badar charts.

Phase-2 visual evidence must therefore come from contemporaneous source-stream chart frames/screenshots, not an independent raw-OHLC reconstruction, unless a later explicit governance decision retires those protected periods.
