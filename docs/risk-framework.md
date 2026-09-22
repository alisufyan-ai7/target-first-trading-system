# Working Risk Framework

_Last updated: 2026-09-22_

This framework governs system construction and validation. It may change only through an explicit project decision.

## Daily limits

- normal daily loss stop: approximately **-USD 40**;
- rare absolute hard stop: **-USD 60**;
- desired daily profit zone / stop-additional-risk zone: approximately **+USD 150 to +USD 200**.

The USD 60 level is an emergency ceiling, not a routine loss allowance.

## Fixed-size execution principle

The project no longer assumes that every trade will be dynamically sized to exactly USD 20 risk / USD 50 profit.

### XAUUSD reference

Reference execution size: **0.10 lot**.

Under the common illustrative convention of 1 lot = 100 oz:

- 0.10 lot = 10 oz;
- USD 1 Gold move ≈ USD 10 gross P&L.

Therefore:

- USD 3 favorable move ≈ +USD 30;
- USD 4 ≈ +USD 40;
- USD 5 ≈ +USD 50;
- USD 7 ≈ +USD 70;
- USD 10 ≈ +USD 100.

The same fixed 0.10-lot position loses approximately USD 10 for each USD 1 adverse Gold move. Actual broker contract specifications must be verified.

### FX and other instruments

Use a fixed execution-size tier derived from actual contract/tick specifications.

For major FX, 0.10 standard lot is the initial research anchor unless the eventual broker specification requires another fixed equivalent.

Do **not** enlarge the lot size merely because a market's normal move is small.

## Structural stop still comes first

Every trade must have a structural/statistical invalidation level.

Because size is fixed, stop distance determines the actual dollar risk.

The scanner must calculate before entry:

- dollar loss at structural stop;
- remaining daily loss budget;
- total open stop-risk;
- margin required;
- correlated exposure.

Reject the trade if its fixed-size structural risk cannot fit inside the remaining daily framework.

Do not compress a structural stop merely to fit an arbitrary dollar loss.

## Aggregate risk gate

Working portfolio rules:

1. no new entry if realized daily P&L is already <= approximately -USD 40;
2. aggregate realized loss plus credible open-stop exposure must be monitored against the -USD 60 emergency ceiling;
3. no new correlated exposure if simultaneous stop-risk would make the hard ceiling easy to breach;
4. once the daily profit state reaches approximately +USD 150, normally stop adding new positions; existing runners may be managed only under a predeclared rule;
5. reaching +USD 200 is the upper daily objective zone, not a reason to increase risk further.

Exact simultaneous-open-risk rules will be validated in later portfolio experiments.

## Flexible profit capture

The system may use multiple target rungs rather than one universal take-profit:

- approximately USD 30;
- USD 40;
- USD 50;
- USD 70;
- USD 100+.

A trade may be closed at a lower rung when evidence favors only a modest move. A runner or larger target is allowed only when the predeclared continuation logic supports it.

Backtests must measure both:

- whether each target rung is hit before invalidation;
- how much favorable excursion was available after entry.

## Prohibited behavior

- martingale;
- doubling after losses;
- increasing size to recover the day;
- revenge trading;
- moving stops farther solely to avoid a loss;
- forcing a trade because the daily target has not been reached;
- increasing lot size merely to manufacture a USD 30/40/50 target on a low-volatility instrument;
- presenting probabilistic signals as certain.

## Small-account implication

At a USD 500 reference balance:

- USD 40 daily loss is 8% of starting equity;
- USD 60 hard loss is 12%.

This remains aggressive.

Any candidate system must explicitly track:

- drawdown;
- risk of ruin;
- margin usage;
- stop-gap / slippage risk;
- consecutive bad days;
- simultaneous correlated exposure;
- broker liquidation / margin-call thresholds.

No live deployment is justified until those risks are validated with actual broker specifications and forward evidence.
