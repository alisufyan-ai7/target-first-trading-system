# New Chat Handoff — Target-First Trading System

_Last updated: 2026-09-22_

Use this file as the **first document to read whenever a new ChatGPT conversation is started for this project**.

## Strict context rule

For this project, use only:

1. the current/new chat;
2. this repository: `alisufyan-ai7/target-first-trading-system`.

Do not use any other GitHub repository, other ChatGPT chat/project, or unrelated account memory/context unless the user explicitly introduces that material into this project.

## Project identity

We are **building a trading system**, not merely conducting research.

Research, backtesting, video analysis, statistics, and machine learning are validation layers used to build the system.

## Read in this order before doing any new work

1. `README.md`
2. `PROJECT.md`
3. `docs/SOURCE-OF-TRUTH.md`
4. `docs/SYSTEM-BLUEPRINT.md`
5. `docs/ORIGINAL-PROJECT-CONTEXT.md`
6. `docs/BADAR-VIDEO-EVIDENCE.md`
7. `docs/TIMEFRAME-AND-MARKET-CONTEXT.md`
8. `docs/SUPERSEDED-ASSUMPTIONS.md`
9. `docs/objectives.md`
10. `docs/risk-framework.md`
11. `docs/current-status.md`
12. `docs/decision-log.md`
13. `docs/STRATEGY-ENGINE-CONTRACT.md`
14. `docs/BUILD-AND-DEPLOYMENT-ROADMAP.md`
15. `strategies/STATUS.md`
16. `research/experiments/EXP-001-badar-video-reverse-engineering.md`
17. `research/experiments/EXP-002-engine-a-target-first-screen.md`
18. `research/experiments/EXP-014-original-engine-a-recovery-equivalent-sizing.md`
19. `research/experiments/EXP-015-target-first-opportunity-ranker-v0.1.md`

Then inspect other experiment records only as needed for historical evidence.

## Non-negotiable operating context

Reference starting equity: about USD 500.

Economic anchor:

- XAUUSD reference size: 0.10 lot;
- normal successful-trade objective: about USD 50;
- USD 30–40 may be accepted when the nearer target has materially stronger validated probability;
- USD 70–100+ may be pursued under validated continuation/runner logic.

Daily framework:

- desired strong-day zone: about USD 150–200;
- normal daily loss stop: about USD 40;
- emergency hard ceiling: about USD 60;
- roughly 3–4 qualified trades/day is a desirable normal range, not a quota;
- no forced minimum;
- no martingale;
- no size increase after losses;
- no revenge/recovery trading.

Low-output day:

- net P&L <= USD 50.

Consistency objective:

- reduce low-output days materially, ideally toward ~20% if evidence and risk permit;
- judge the distribution of daily outcomes, not only aggregate profit.

## Core system architecture

Default architecture:

```text
validated strategy engines
        ->
meaningful trade candidates
        ->
target-first probability / expected-value layer
        ->
P&L-equivalent position sizing
        ->
risk / margin / leverage / correlation gates
        ->
cross-market ranking
        ->
execution + management
        ->
daily P&L state machine
        ->
journal / performance database
```

Do not silently replace this with a broad raw-pivot ML scanner.

The target-first model is normally a **selector/ranker after validated engines**, not an unrestricted trade inventor.

## Original Badar / Engine A context that must not be lost

Badar's supplied/public examples produced the first Engine A hypothesis:

liquidity -> sweep -> internal MSS -> displacement -> FVG -> retracement -> structural stop -> partials / target expansion.

Important direct evidence is preserved in `docs/BADAR-VIDEO-EVIDENCE.md`.

Original EXP-002 Gold Engine A recorded positive simplified expectancy and remains the current active recovery lead.

Later Engine A v0.2-portable is a different rewrite and must not be used to invalidate EXP-002.

## Current technical gate

The next technical work is **EXP-014**:

1. recover/reconstruct the original EXP-002 Engine A implementation;
2. reproduce its recorded Gold metrics within reasonable tolerance or honestly declare it unrecoverable;
3. freeze correct P&L-equivalent sizing for non-Gold markets;
4. route recovered/validated engine candidates through the common candidate contract.

Only after that should **EXP-015 target-first ranker** resume.

EXP-015 is currently PAUSED. Its earlier broad-pivot XAU Stage-1 statistics are diagnostic only.

## What a new chat must do first

Before executing tools or proposing a new strategy:

1. read the ordered documents above;
2. summarize the project state in no more than ~10 bullets;
3. state the exact current gate/next experiment;
4. confirm that EXP-014 precedes EXP-015;
5. do not restart prior research or invent a new project direction.

## GitHub checkpoint discipline

Before a substantial experiment:

- create/confirm the experiment record;
- freeze the rules to be tested.

After every material result:

- record data source/date range;
- parameters;
- split;
- result;
- limitation;
- conclusion;
- status;
- next action.

Update `docs/current-status.md`, `docs/decision-log.md`, `strategies/STATUS.md`, and `CHANGELOG.md` when materially appropriate.

## If chat and repository appear to conflict

Use the latest explicit user instruction, then immediately update the repository to reflect the correction.

Do not rely on vague memory from another chat.
