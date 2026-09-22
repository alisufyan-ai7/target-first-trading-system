# Project Brief

_Last updated: 2026-09-22_

## Goal

Build and validate a **multi-strategy, multi-asset target-first trading system** whose operational purpose is to identify and execute high-quality opportunities across supported markets and work toward a relatively consistent **USD 150–200 daily net P&L zone**.

Research/backtesting is the validation layer for building that system, not the end objective.

The project is not limited to copying any one trader or strategy. Badar Tanveer's public trading examples were used as an initial strategy-research input, but the final system may use multiple independently validated strategy engines.

## User's working economic objective

Reference starting balance: **about USD 500**.

Desired behavior:

- XAUUSD reference execution size: **0.10 lot**;
- under the common 100-oz-per-lot convention, 0.10 lot is approximately 10 oz, so a USD 3 / 4 / 5 / 7 / 10 Gold move corresponds approximately to USD 30 / 40 / 50 / 70 / 100 gross P&L;
- for FX and other markets, use a fixed-size tier that is economically comparable and explicitly derived from contract/tick specifications rather than risk-sizing every trade to force a USD 50 outcome;
- treat roughly USD 30–50 as a useful normal successful-trade capture zone;
- allow larger USD 70–100+ captures when the validated move/continuation evidence supports them;
- do not require every trade to make USD 50;
- scan all supported liquid markets for the best current opportunities;
- trade count is **opportunity-driven**, not fixed at 3–4/day: more trades are acceptable when individual opportunities are smaller, provided quality, exposure, margin, correlation, and daily risk gates remain satisfied;
- never force trades merely to meet the daily target;
- desired daily net P&L zone: about USD 150–200 when sufficient validated opportunity exists;
- retain low-output-day and daily-distribution statistics as diagnostic measures;
- normal daily loss stop: about USD 40;
- rare absolute hard stop: about USD 60;
- no martingale;
- no increasing position size after losses;
- no revenge/recovery trading.

These are system objectives, not guaranteed outcomes.

## Core decision problem

The system should not merely ask:

> Is price likely to move up or down?

It should ask:

> From this exact entry and fixed execution size, what favorable dollar-profit levels are likely to be reached before structural invalidation, and is this opportunity better than the alternatives currently available across the market universe?

For XAUUSD, the reference target ladder is based on approximately:

- USD 3 favorable Gold move -> USD 30 gross;
- USD 4 -> USD 40;
- USD 5 -> USD 50;
- USD 7 -> USD 70;
- USD 10 -> USD 100;

assuming the reference 0.10-lot / 10-oz convention. Broker contract specifications must be verified.

For other instruments, favorable price distances and P&L must be translated using actual contract size, tick/pip value, quote-currency conversion, and the fixed execution-size tier.

No market move is certain. "Sure" in the operational design means a setup has passed a validated probability/expected-value threshold, not guaranteed price movement.

## Intended architecture

```text
multi-market data feeds
    ->
multiple independent setup engines
    ->
common feature extraction
    ->
target-ladder model:
P(hit $30), P(hit $40), P(hit $50), P(hit $70), P(hit $100)
before structural invalidation
    ->
cross-market opportunity ranking
    ->
correlation / margin / exposure / daily-risk gates
    ->
fixed-size execution tier by instrument
    ->
trade management / partials / runner logic
    ->
daily P&L state machine
    ->
paper/forward validation
    ->
optional automated execution only after evidence
```

## Current research status

- Engine A / USDJPY v0.2 remains a research lead, not deployable.
- Engine F / GBPUSD v0.1 remains a research lead, not deployable.
- EXP-010 showed the two leads are low-correlated but still fail the previous fixed USD 20 risk / USD 50 target daily-distribution framing.
- EXP-011 was checkpointed under the old fixed-payoff / max-4-trades assumptions but was superseded before results by the user's fixed-size, flexible-target, opportunity-driven clarification.
- The next work is to formalize fixed-size economics and target ladders across the market universe, then rebuild the scanner around ranking attainable dollar moves rather than forcing every setup into +2.5R.

## Important principle

Increase the **opportunity universe**, not the willingness to accept poor trades.

The scanner may take more trades when several independently qualified opportunities exist, but it must not lower quality thresholds just to reach USD 150–200.
