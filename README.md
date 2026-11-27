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

No strategy engine is currently promoted as a validated execution lead.

The latest Badar human-decision mechanization study used a prospectively fresh 43-case v0.2 tranche and failed its predeclared independent reproducibility gates before behavioral-fidelity reveal:

`V0_2_REPRODUCIBILITY_FAIL_CLOSE_BEFORE_BEHAVIORAL_FIDELITY`

Badar's actual TRADE/WAIT/NO_TRADE decisions and all P&L/outcome fields remain sealed.

The project must not rescue the failed v0.2 tranche by adjudication, post-hoc threshold changes, or reuse as fresh validation. If this research path continues, it requires a prospectively new version and fresh evidence.

See `docs/current-status.md` and the v0.2 reproducibility result for the latest checkpoint.

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
- docs/PNL-EQUIVALENT-SIZING.md
- strategies/STATUS.md
- research/experiments/
