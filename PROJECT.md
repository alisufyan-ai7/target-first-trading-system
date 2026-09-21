# Project Brief

_Last updated: 2026-09-22_

## Goal

Research and eventually prototype a multi-strategy, multi-asset trading system optimized for **target-first opportunity selection** and a relatively consistent daily P&L distribution.

The project is not limited to copying any one trader or strategy. Badar Tanveer's public trading examples were used as an initial strategy-research input, but the final system may use multiple independently validated strategy engines.

## User's working economic objective

Reference starting balance: **about USD 500**.

Desired behavior:

- seek approximately USD 150–200 net profit on strong days;
- treat roughly USD 50 as a useful profit unit per successful trade;
- normally take no more than about 3–4 qualified trades/day;
- do not force trades to satisfy a daily quota;
- low-output day = net P&L <= USD 50;
- research preference: low-output days ideally <= about 20% of trading days;
- normal daily loss stop: about USD 40;
- rare absolute hard stop: about USD 60;
- no martingale;
- no increasing position size after losses;
- no revenge/recovery trading.

These are research targets, not guaranteed outcomes.

## Core decision problem

The system should not merely ask:

> Is price likely to move up or down?

It should ask:

> From this exact entry, is the required favorable move likely to occur before structural invalidation?

For XAUUSD, the initial reference label is a **USD 5 favorable Gold move before the stop**.

For other instruments, the favorable move must be normalized to the intended dollar-profit unit using contract size, tick value, and position size.

## Intended architecture

```text
market data
    ->
multiple independent setup engines
    ->
common feature extraction
    ->
target-first outcome model / ranking
    ->
correlation and exposure controls
    ->
position sizing
    ->
daily P&L state machine
    ->
paper/forward validation
    ->
optional automated execution only after evidence
```

## Current research status

- Badar/video reverse engineering: **completed sufficiently to define first mechanical hypothesis**.
- Engine A, liquidity sweep -> MSS -> displacement/FVG -> retracement: **screened; positive simplified expectancy, insufficient daily consistency**.
- Engine B, breakout -> retest -> continuation: **first formulations rejected**.
- Engine C, trend pullback -> continuation: **first formulations rejected**.
- Next strategy families to test: **session/opening-range momentum** and **volatility compression -> expansion**, using checkpointed experiments.
- Data-source expansion: keep Dukascopy as a baseline and validate finalists on an independent broker/API feed.

## Important principle

A strategy that looks profitable but produces too many USD 0–50 days fails the user's consistency objective.

A strategy that produces frequent trades only by lowering quality thresholds also fails.

Increase the **opportunity universe**, not the willingness to accept poor trades.
