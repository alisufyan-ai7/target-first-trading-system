# EXP-011 — Daily-Distribution Feasibility Frontier

**Status:** IN PROGRESS — ANALYTICAL MODEL FROZEN BEFORE RESULTS  
**Date:** 2026-09-22

## Purpose

Determine whether the project's desired daily P&L distribution is mathematically compatible with the current trade payoff and opportunity-count framework, before inventing another strategy or changing any project objective.

## Question

With approximately:

- USD 20 loss at structural invalidation;
- USD 50 profit on a successful trade;
- normally no more than 1–4 qualified trades/day;
- low-output day defined as net P&L <= USD 50;
- normal daily loss stop at -USD 40;
- strong-day profit stop at +USD 150;

what per-trade target-first win probability and opportunity frequency would be required to approach:

- <= USD 50 days <= 20%;
- >= USD 100 days around 75–80%;
- frequent >= USD 150 strong days?

## Model A — Fixed number of completed trades, no intraday state stops

For each N in {1,2,3,4}, assume exactly N independent trades are completed.

Each trade is:

- win: +USD 50 with probability p;
- loss: -USD 20 with probability 1-p.

Daily P&L after N completed trades is:

`P&L = 50W - 20(N-W) = 70W - 20N`

where W is the number of wins.

For each N, calculate exactly:

- P(daily P&L <= USD 50);
- P(daily P&L >= USD 100);
- P(daily P&L >= USD 150);
- P(losing day);
- expected daily P&L.

Find the minimum p, if it exists, required for:

1. low-output days <= 20%;
2. >= USD 100 days >= 75%;
3. >= USD 100 days >= 80%.

## Model B — Idealized sequential daily state machine

For each N in {1,2,3,4}, assume up to N independent opportunities arrive sequentially.

After each completed trade:

- stop accepting new trades if realized daily P&L <= -USD 40;
- stop accepting new trades if realized daily P&L >= +USD 150;
- otherwise continue until N opportunities have been used.

Each trade remains +USD 50 / -USD 20.

This model is intentionally optimistic:

- no spread, commission, slippage, or latency;
- no simultaneous-open-trade overshoot beyond -USD 40;
- no correlation between trade outcomes;
- no signal clustering or regime dependence.

Therefore, if the project objective is difficult even under this model, real execution would be harder.

Calculate the same daily-distribution metrics and p thresholds as Model A.

## Opportunity-scarcity bounds

Let q_N be the fraction of eligible weekdays with exactly N qualified opportunities before state-machine suppression.

The overall low-output probability is:

`sum(q_N * P_low(N,p))`.

Important structural bounds to quantify:

- with 0 or 1 trade, a day can never finish above USD 50;
- with fewer than 2 trades, a day can never reach USD 100;
- with fewer than 3 trades, a day can never reach USD 150 under the +USD 50 unit.

Thus the fraction of 0–1 opportunity days creates a hard floor under the low-output-day rate, independent of strategy skill.

No arbitrary opportunity-count mixture will be invented. Instead, report generic bounds and show how fixed N=1–4 behave.

## Interpretation rules

This is not a strategy backtest and has no development/holdout split.

Do not alter the project's objectives based on the result automatically.

The experiment should answer:

1. what win rates would theoretically be required;
2. whether those win rates are materially above the ~28.57% per-trade break-even probability for a +USD 50 / -USD 20 payoff;
3. whether 3–4 trades/day can plausibly satisfy both the low-output and >=USD 100 preferences at the same time;
4. how the -USD 40 loss stop changes the frontier;
5. what opportunity-frequency floor is required regardless of p.

## Next action

Compute the exact distributions and thresholds, checkpoint the result, and then use that evidence to decide whether the next research phase should:

- seek another independent engine;
- alter the payoff/risk unit;
- alter the daily-distribution objective;
- or alter the reference-account economic assumptions.

Do not silently change any target.
