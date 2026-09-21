# Working Risk Framework

_Last updated: 2026-09-22_

This is an initial research framework and may change after portfolio-level testing.

## Daily limits

- normal daily loss stop: approximately **-USD 40**;
- rare absolute hard stop: **-USD 60**;
- desired daily profit stop: approximately **+USD 150 to +USD 200**.

The USD 60 level is an emergency ceiling, not a routine loss allowance.

## Trade-level behavior

A structurally valid stop comes first. If the stop is too wide for the desired loss budget:

1. reduce position size; or
2. reject the trade.

Do not compress a stop to an arbitrary dollar amount if that makes the trade structurally invalid.

## Prohibited behavior

- martingale;
- doubling after losses;
- increasing size to recover the day;
- moving the stop farther solely to avoid a loss;
- forcing a trade because the daily target has not been reached.

## Small-account implication

At a USD 500 reference balance:

- USD 40 daily loss is 8% of starting equity;
- USD 60 hard loss is 12%.

That is aggressive. The research must explicitly track risk of ruin, drawdowns, and consecutive bad days before any live deployment.

## Gold reference economics

The conversation used a common illustrative convention in which 0.10 lot XAUUSD produces about USD 10 P&L per USD 1 move in Gold, so a USD 5 favorable move is about USD 50 gross P&L.

This is **not universal**. Broker contract specifications must be verified before broker-specific P&L simulation.
