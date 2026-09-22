# Strategy Engine Candidate Contract

_Last updated: 2026-09-22_

Every validated strategy engine should eventually emit candidates in a common schema so probability/ranking and execution layers remain strategy-agnostic.

## Required candidate fields

- engine_id;
- engine_version;
- symbol;
- venue/data source;
- direction;
- signal timestamp;
- intended entry type;
- intended entry price/rule;
- structural stop/invalidation price;
- native stop distance;
- setup/context fields;
- source timeframe(s);
- session;
- target candidates in native units;
- feature snapshot available at signal time;
- data provenance/version.

## Derived economic fields

Before ranking/execution:

- USD value per native unit at proposed lot;
- P&L-equivalent proposed lot;
- structural stop dollar risk;
- margin requirement;
- notional exposure;
- T30/T40/T50/T70/T100 native target distances;
- target-first probabilities;
- expected value after estimated costs;
- correlation/common-factor exposure.

## Rule

The ranker compares **candidates**, not raw market bars, unless a separately validated statistical candidate-generator engine explicitly creates those candidates.

## Auditability

Every rejected candidate should keep a rejection reason, such as:

- probability below threshold;
- no positive-EV target rung;
- structural risk too high;
- margin infeasible;
- correlated exposure too high;
- daily loss state;
- daily profit state;
- stale entry;
- spread/news regime gate.

This is necessary to diagnose whether low-output days come from lack of opportunity, poor setup quality, or risk constraints.
