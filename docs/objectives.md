# System Objectives

_Last updated: 2026-09-22_

## Primary objective

Build and validate a multi-market trading system that continuously scans supported liquid markets, ranks the best target-first opportunities, and works toward a relatively consistent **USD 150–200 daily net P&L zone** without forcing trades, martingale, or loss-recovery sizing.

Research is the validation layer; the end objective is an operating system.

## Economic anchor and normal trade objective

### XAUUSD

Reference execution size: **0.10 lot**.

Under the common illustrative convention of 1 XAUUSD lot = 100 oz:

- USD 3 Gold move ≈ USD 30 gross;
- USD 4 ≈ USD 40;
- USD 5 ≈ USD 50;
- USD 7 ≈ USD 70;
- USD 10 ≈ USD 100.

### Other markets

Do **not** assume the same 0.10-lot size.

For every symbol, freeze a native target distance first, then calculate the lot size required for that move to produce approximately USD 50 gross:

`lot_size ~= 50 / (target_distance × USD value per distance unit at 1 lot)`.

For USD-quote FX, for example:

- 10-pip target -> about 0.50 lot for USD 50;
- 20-pip target -> about 0.25 lot;
- 50-pip target -> about 0.10 lot.

The exact value depends on contract/pip value and quote conversion.

The target-distance rule itself must be frozen on development data before holdout testing.

## Profit flexibility

The system should normally seek about **USD 50** per successful trade.

Permitted deviations:

- accept approximately USD 30–40 when the nearer target has materially stronger target-first probability;
- hold toward USD 70–100+ when continuation evidence is predeclared and validated.

The system must not increase size after a loss or change size to recover the day.

## Risk feasibility

P&L-equivalent sizing is not automatically executable.

Before entry calculate:

- structural-stop dollar risk at the proposed equivalent lot;
- required margin;
- notional exposure;
- remaining daily loss budget;
- correlated open exposure.

If the USD-50-equivalent size is unsafe or infeasible:

1. reduce the trade objective to a justified USD 30–40 level with a smaller safe size; or
2. reject the trade.

Do not compress the stop merely to make the economics fit.

## Engine A preservation rule

EXP-002 original XAUUSD Engine A remains a retained positive-expectancy research lead.

Its later portable v0.2 implementation is a different prospective specification and must not be treated as proof that the EXP-002 implementation failed.

Before new scanner optimization, recover/reconstruct the EXP-002 implementation and test whether the recovered code reproduces the recorded Gold metrics.

## Opportunity-driven trade count

There is no forced daily trade count.

More trades may be taken when multiple independent qualified opportunities exist and aggregate risk/margin remains acceptable.

The system must never lower quality thresholds merely because the USD 150–200 daily zone has not yet been reached.

## Daily objective

- desired net daily zone: approximately USD 150–200 when sufficient qualified opportunity exists;
- normal daily loss stop: approximately -USD 40;
- rare hard ceiling: approximately -USD 60.

No historical result guarantees these values every day. The system must report the actual distribution achieved.

## Acceptance dimensions

Evaluate:

- T30/T40/T50/T70/T100 target-first probability;
- expectancy after realistic costs;
- probability calibration;
- structural-stop dollar risk at equivalent size;
- margin and notional feasibility;
- mean/median daily P&L;
- <= USD 50 day percentage;
- >= USD 100 / 150 / 200 day percentages;
- losing-day percentage;
- drawdown;
- consecutive bad/low-output days;
- trades/day including zero-signal days;
- opportunity concentration;
- simultaneous-signal correlation;
- realized capture versus maximum favorable excursion.

## Non-goals

Do not optimize to:

- force a trade count;
- force exactly USD 50 when the setup only supports USD 30–40;
- manufacture USD 50 with unsafe leverage;
- hide zero/loss days;
- martingale;
- increase size after losses;
- assume reward/risk implies probability;
- present probabilistic signals as certain.
