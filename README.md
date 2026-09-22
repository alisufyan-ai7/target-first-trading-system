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

**EXP-014 is complete.**

- Part A systematically tested recovery variants A1–A9 under a frozen multi-dimensional acceptance protocol.
- The original EXP-002 implementation could not be honestly reproduced from the surviving evidence and is now classified as a **historical exploratory positive result, not a validated/reproducible engine**.
- Part B froze the forward non-Gold P&L-equivalent sizing method in `docs/PNL-EQUIVALENT-SIZING.md`.
- EXP-015 remains **PAUSED** because the ranker still needs at least one prospectively specified, reproducible, validated strategy engine that emits the common candidate contract.

The next build gate is therefore to define and validate a new **causal, reproducible strategy engine** prospectively. Do not continue post-hoc fitting to the lost EXP-002 implementation and do not resume the broad-pivot ranker.

## Start here

- **docs/NEW-CHAT-HANDOFF.md** — read this first when starting a new chat

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
