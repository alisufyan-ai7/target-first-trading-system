# Target-First Trading System

This repository is the durable source of truth for the **trading system being built in the originating ChatGPT project conversation**.

Research and backtesting are validation layers. The end objective is an operating multi-strategy, multi-market system.

## Strict context isolation

Only two context sources are authorized:

1. the originating/current project chat; and
2. this repository.

Do not import assumptions, code, decisions, strategy definitions, or project memory from any other ChatGPT chat/project, GitHub repository, or account-level context unless the user explicitly introduces that material here.

See docs/SOURCE-OF-TRUTH.md.

## System objective

Build a scanner/execution system that:

- scans multiple liquid markets continuously;
- consumes candidates from validated strategy engines;
- estimates target-first probability and expected value;
- uses XAUUSD 0.10 lot as the economic anchor;
- calculates symbol-specific equivalent sizing for non-Gold markets;
- controls structural risk, margin, leverage, correlation, and daily loss;
- normally seeks about USD 50 per successful trade, with validated USD 30–40 nearer targets and USD 70–100+ continuations;
- works toward roughly USD 150–200 net on days with sufficient qualified opportunity;
- never forces trades, martingales, or increases size to recover losses.

These are design objectives, not guaranteed returns.

## Current gate

The original Badar-inspired Gold Engine A in EXP-002 showed positive simplified expectancy, but its exact implementation was not fully preserved before later portable rewrites.

Before broad ranker/scanner development resumes:

1. recover/reconstruct original Engine A;
2. reproduce EXP-002 behavior within reasonable tolerance;
3. freeze P&L-equivalent non-Gold sizing with feasibility gates;
4. route validated strategy-engine candidates through the target-first ranker.

## Start here

- PROJECT.md
- docs/SYSTEM-BLUEPRINT.md
- docs/ORIGINAL-PROJECT-CONTEXT.md
- docs/BADAR-VIDEO-EVIDENCE.md
- docs/TIMEFRAME-AND-MARKET-CONTEXT.md
- docs/SUPERSEDED-ASSUMPTIONS.md
- docs/BUILD-AND-DEPLOYMENT-ROADMAP.md
- docs/current-status.md
- docs/objectives.md
- docs/risk-framework.md
- strategies/STATUS.md
- research/experiments/
