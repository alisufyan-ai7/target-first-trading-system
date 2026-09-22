# Working Risk Framework

_Last updated: 2026-09-23_

## Daily limits

- normal stop adding risk: approximately **-USD 40**;
- rare absolute hard-loss ceiling: approximately **-USD 60**;
- desired daily profit-state zone: approximately **+USD 150 to +USD 200**.

The USD 60 level is an emergency ceiling, not a routine daily allowance and **not a per-trade sizing budget**.

## Position sizing

### XAUUSD

Reference size: **0.10 lot**, subject to broker verification.

### Other markets

Use **P&L-equivalent sizing**, not identical lot size.

Use the frozen methodology in `docs/PNL-EQUIVALENT-SIZING.md`.

For an engine-conditioned frozen native target distance/target function, calculate the size that would make the normal target approximately USD 50 gross.

The proposed size must pass:

- structural-stop dollar risk;
- margin;
- notional/leverage;
- remaining daily-loss budget;
- aggregate open-stop risk;
- correlated/common-factor exposure.

If unsafe:

1. use a smaller safe size / justified USD 30–40 objective; or
2. reject the trade.

Never enlarge size after a loss.

## Structural stop first

A valid structural/statistical invalidation remains mandatory.

Never compress the stop solely to fit a dollar amount.

For each candidate calculate:

- dollar loss at structural stop;
- target dollar reward;
- actual reward/risk;
- required margin;
- notional exposure;
- aggregate open-stop exposure.

## Daily state machine

The daily target is not a quota.

Illustrative operating behavior:

- around +USD 50: continue only for qualified opportunities;
- around +USD 100: continue only for qualified opportunities;
- around +USD 150–200: normally stop adding new exposure;
- around -USD 30: materially tighten selection;
- around -USD 40: normally stop adding risk;
- -USD 60: emergency hard ceiling.

No recovery trade is permitted because the day is below target.

## Profit management

Normal objective: about USD 50.

Allowed only under predeclared/validated rules:

- USD 30–40 nearer target;
- partial profit;
- USD 70–100+ runner/continuation.

## Correlation/common-factor risk

Per-trade risk is insufficient.

Examples such as long EURUSD + long GBPUSD + short USDJPY + long Gold may all load on USD weakness.

The portfolio gate must eventually measure:

- same-currency factor exposure;
- same-index/macro exposure;
- simultaneous stop loss;
- concentration by strategy and market;
- correlation of candidate outcomes where evidence permits.

## Small-account implication

At USD 500 reference equity, the stated daily limits are aggressive.

Before live deployment verify:

- actual broker leverage/margin;
- liquidation/margin-call thresholds;
- spread/commission;
- slippage/gaps;
- risk of ruin;
- simultaneous exposure;
- drawdown under realistic costs.

No live promotion without independent-feed and forward/demo validation.
