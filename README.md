# Target-First Trading Research

This repository is the durable source of truth for the trading-system research originating in the current ChatGPT conversation.

## Project isolation rule

Only two context sources are authorized:

1. the originating ChatGPT conversation for this project; and
2. this repository.

Do **not** import assumptions, results, code, decisions, memory, or strategy definitions from any other ChatGPT chat, project, GitHub repository, or account-level context unless the user explicitly introduces that material into this project.

## Research objective

Investigate whether a multi-strategy, multi-asset trading system can produce a relatively consistent daily profit distribution from a small starting account without forcing trades or using martingale-style recovery.

Current working targets:

- reference starting equity: about USD 500;
- desired daily profit stop: about USD 150–200;
- desired successful-trade profit unit: about USD 50;
- intended normal maximum: about 3–4 qualified trades/day;
- low-output day: net daily P&L <= USD 50;
- research preference: low-output days ideally no more than about 20% of trading days;
- normal daily loss stop: about USD 40;
- rare absolute hard stop: about USD 60;
- no martingale;
- no increasing size after losses;
- no forced recovery trades.

These are research objectives, not promised performance.

## Research principle

A setup is evaluated using a **target-first** question:

> Does price reach the required favorable target before structural invalidation?

For XAUUSD, the initial reference target is a USD 5 favorable price move. For other instruments, target size should be normalized to the desired dollar-profit unit using instrument-specific contract/tick value.

## Current status

The first Badar-inspired XAUUSD strategy screen has been completed on a broker-neutral one-minute dataset. It showed positive simplified expectancy but failed the desired daily-income consistency profile. Initial breakout/retest and trend-pullback alternatives were not strong enough in their first formulations.

See:

- `PROJECT.md`
- `docs/SOURCE-OF-TRUTH.md`
- `docs/current-status.md`
- `research/experiments/`
