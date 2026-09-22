# Project Brief

_Last updated: 2026-09-22_

## Goal

Build and validate a **multi-strategy, multi-asset target-first trading system** whose operational purpose is to identify and execute the best qualified opportunities across supported markets and work toward a relatively consistent **USD 150–200 daily net P&L zone**.

Research/backtesting is the validation layer for building that system, not the end objective.

Badar Tanveer's public trading examples supplied in this project were the source for the first Engine A hypothesis. Those original Gold findings remain part of the active knowledge base and must not be overwritten by later portable rewrites.

## User's working economic objective

Reference starting balance: **about USD 500**.

### Gold anchor

XAUUSD reference execution size: **0.10 lot**.

Under the common 100-oz-per-lot convention:

- 0.10 lot ≈ 10 oz;
- USD 3 favorable Gold move ≈ USD 30 gross;
- USD 4 ≈ USD 40;
- USD 5 ≈ USD 50;
- USD 7 ≈ USD 70;
- USD 10 ≈ USD 100.

Broker contract specifications must be verified before execution.

### Other markets — equivalent sizing, not identical lot size

The project must **not** assume 0.10 lot for every market.

For each non-Gold symbol, calculate an **economically equivalent lot size** from:

1. the frozen/native target distance for that symbol;
2. its contract size, pip/tick value, and quote-currency conversion;
3. the objective that the normal successful trade should gross approximately **USD 50**.

Generic sizing rule:

`lot_size ~= 50 / (target_move_in_native_units × USD_value_per_native_unit_per_1_lot)`.

The normal target is approximately USD 50, with two explicit flexibilities:

- if the most reliable attainable move supports only about USD 30–40, the trade may still qualify;
- if continuation evidence supports more, part or all of the trade may be held toward USD 70–100+.

Equivalent sizing is always subject to structural-stop risk, margin, leverage, and daily-risk feasibility. If the size required to make USD 50 is unsafe or infeasible, the system must reduce the dollar objective for that trade or reject it; it must not hide the risk.

## Engine A / Gold clarification

The original Badar-inspired Gold Engine A screen in EXP-002 showed **positive simplified expectancy in both development and holdout**.

Later Engine A v0.2-portable was a prospective mechanical rewrite created because the exact original implementation had not been fully preserved. The repository explicitly states that v0.2 is **not claimed to reproduce the exact EXP-002 implementation**.

Therefore:

- poor XAUUSD results from v0.2 do **not** invalidate the original EXP-002 Gold lead;
- the original Gold Engine A must be treated as a separate retained research lead;
- before further scanner development, the project should recover/reconstruct the original Engine A mechanics as faithfully as possible and verify that the recovered implementation reproduces EXP-002 behavior within reasonable tolerance.

## Operating behavior

- scan all supported liquid markets for the best current long/short opportunities;
- normal successful-trade objective: about USD 50;
- USD 30–40 is acceptable when confidence is materially better at the nearer target;
- USD 70–100+ is allowed when validated continuation evidence supports it;
- trade count is opportunity-driven rather than a fixed quota;
- never force trades merely to reach the daily target;
- desired daily net zone: about USD 150–200 when sufficient validated opportunity exists;
- normal daily loss stop: about USD 40;
- rare absolute hard stop: about USD 60;
- no martingale;
- no increasing size after losses;
- no revenge/recovery trading.

These are system objectives, not guaranteed outcomes.

## Core decision problem

For every candidate setup the system should ask:

> From this exact entry and structural invalidation, what favorable move is likely to occur first, what lot size makes that move economically useful, and is this opportunity better than the alternatives currently available across the market universe?

The scanner should estimate a target ladder:

- approximately USD 30;
- USD 40;
- USD 50;
- USD 70;
- USD 100+;

all evaluated **before structural invalidation**.

No market move is certain. "Sure" in the operating design means the setup has passed a validated probability/expected-value threshold, not guaranteed price movement.

## Intended architecture

```text
multi-market data feeds
    ->
multiple independent setup engines
    ->
candidate native target distances + structural invalidation
    ->
target-first probability model
    ->
equivalent lot-size conversion for ~USD 50 normal target
    ->
risk / margin / correlation feasibility gate
    ->
cross-market opportunity ranking
    ->
entry + target management / partials / runners
    ->
daily P&L state machine
    ->
paper/forward validation
    ->
optional automated execution only after evidence
```

## Current priority

1. preserve the original EXP-002 Gold Engine A as a positive-expectancy research lead;
2. recover/reconstruct its mechanics before treating later v0.2 results as representative;
3. revisit EXP-006 P&L-equivalent cross-market sizing rather than assuming 0.10 lot on FX;
4. freeze the sizing/equivalence rule before any new holdout inspection;
5. only then resume broad scanner/ranker development.

## Important principle

Increase the **opportunity universe**, not the willingness to accept poor trades.

The system may take more qualified trades when several independent opportunities exist, but it must not lower quality thresholds just to reach USD 150–200.
