# EXP-044 True Order-Flow Source Feasibility v0.1

Frozen 2026-09-27. Zero-outcome source gate only.

EXP-043 v0.2 passed integrity but found no stable incremental information advantage from Dukascopy broker quote/tick microstructure.

## Priority

Gold first: COMEX Gold trades plus depth / Market-by-Order or equivalent.

FX second: representative institutional signed flow and/or order-book state such as EBS/CME-quality data.

## What counts

At least one genuinely new flow family is required:

- actual executed trades with native or reproducibly inferred side; and/or
- real order-book state/change: depth, add/cancel/modify, depletion/replenishment.

Required provenance before use:

- source/vendor/venue;
- exact dataset/product;
- instrument and contract mapping;
- timestamp precision/timezone;
- trade/depth schema;
- native vs inferred trade side;
- session/calendar rules;
- date range;
- retrieval method;
- immutable checksum/vendor file ID;
- licensing constraints affecting reproducibility.

## What does not count

Do not substitute:

- Dukascopy quote updates;
- retail tick volume;
- candle volume;
- OHLC transforms;
- quote-side size without true book/trade semantics;
- DXY/T-Bond reactions.

## Coverage gate

Gold-first source must cover at least 2026-03-23 through 2026-06-29, or a prospectively frozen earlier development interval of comparable duration, with at least 50 independent trading days and broad London/New York intraday coverage.

Protected Jul-Aug/Sep 2026 cannot be used to choose the source.

## Before modeling

A source-specific zero-outcome preflight must verify:

- schema/timestamp integrity;
- instrument/session continuity;
- duplicate/message-order policy;
- immutable vendor checksums or two independent retrievals;
- deterministic normalization;
- requested-day coverage;
- no protected-period leakage.

No target labels, probabilities, strategy rules or P&L may be computed during preflight.

## Current disposition

`NO_REPRODUCIBLE_TRUE_FLOW_SOURCE_ATTACHED_YET`.

Exact next action: obtain or attach a provenance-preserving true trade/depth source, preferably COMEX Gold first, then freeze and run its zero-outcome source preflight.

Do not weaken this requirement by relabeling another free quote/tick proxy as true order flow.
