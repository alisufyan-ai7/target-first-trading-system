# System Objectives

_Last updated: 2026-09-22_

## Primary objective

Build and validate a multi-market trading system that continuously scans supported liquid markets, ranks the best target-first opportunities, and works toward a relatively consistent **USD 150–200 daily net P&L zone** without forcing trades, martingale, or loss-recovery sizing.

Historical research, holdout testing, independent-feed validation, and forward/paper evidence are required because the purpose is eventually to build a system that can operate, not merely to publish research results.

## Fixed-size economic anchor

### XAUUSD

Reference execution size: **0.10 lot**.

Under the common illustrative convention of 1 XAUUSD lot = 100 oz:

- 0.10 lot = 10 oz;
- USD 1 Gold move ≈ USD 10 gross P&L;
- USD 3 move ≈ USD 30;
- USD 4 move ≈ USD 40;
- USD 5 move ≈ USD 50;
- USD 7 move ≈ USD 70;
- USD 10 move ≈ USD 100.

Broker-specific contract size must be verified before execution.

### Other markets

Do not dynamically enlarge position size merely to make every target equal USD 50.

Instead:

1. define a fixed execution-size tier per instrument from actual contract/tick specifications;
2. compute the native price/pip move needed for approximately USD 30, 40, 50, 70, and 100 gross P&L;
3. test whether those moves occur before structural invalidation;
4. reject economically unreasonable sizes or margin burdens.

For major FX, 0.10 standard lot is the initial research reference unless broker specifications justify a different fixed equivalent.

## Target ladder

The scanner should estimate and rank the probability that a setup reaches each profit rung **before structural invalidation**:

- approximately USD 30;
- USD 40;
- USD 50;
- USD 70;
- USD 100+.

A trade does not fail merely because it cannot reasonably reach USD 50. A validated USD 30–40 opportunity may be useful if its probability, expectancy, costs, and portfolio contribution justify taking it.

Likewise, if continuation evidence supports more than USD 50, the system should be able to hold part or all of the position toward USD 70–100+ rather than using a universal fixed take-profit.

## Opportunity-driven trade count

There is no longer a hard research assumption that the system should normally stop at 3–4 trades/day.

The system may take more qualified trades when:

- several independent opportunities exist;
- individual opportunities target smaller USD 30–40 captures;
- aggregate open risk remains within the daily framework;
- margin/notional exposure is feasible;
- correlated positions are controlled;
- the signal-quality threshold is unchanged.

There is still **no minimum trade quota** and no forced trading.

## Daily objective

Working operating target:

- desired net daily zone: approximately USD 150–200 when sufficient opportunity exists;
- stop adding new exposure once the daily profit-state rule is satisfied, subject to explicit runner/open-position rules;
- normal daily loss stop: approximately -USD 40;
- rare hard ceiling: approximately -USD 60.

No historical experiment can guarantee a USD 150–200 result every day. The system must quantify how often that zone is actually reached.

## Acceptance dimensions

The system must evaluate all of the following:

- target-first probability for each profit rung;
- expectancy after realistic costs;
- calibration of predicted probabilities;
- mean and median daily P&L;
- percentage of days <= USD 50;
- percentage of days >= USD 100;
- percentage of days >= USD 150;
- percentage of days >= USD 200;
- losing-day percentage;
- maximum daily loss;
- maximum drawdown;
- consecutive low-output days;
- consecutive losing days;
- trades/day including zero-signal days;
- opportunity concentration by market/session;
- cross-market signal correlation;
- simultaneous open risk;
- margin usage;
- fixed-size notional/equity;
- spread/slippage sensitivity;
- realized profit captured versus maximum favorable excursion.

## Non-goals

The system must not be optimized to:

- show an artificially high win rate;
- force a fixed number of trades;
- force every trade to make exactly USD 50;
- increase size after losses;
- hide losing or zero days;
- use martingale or recovery sizing;
- assume a high reward/risk ratio implies a high win probability;
- claim certainty when only a probability estimate is available.
