# New Chat Handoff — Target-First Trading System

_Last updated: 2026-09-23_

Use this file as the **first document to read whenever a new ChatGPT conversation is started for this project**.

## Strict context rule

For this project, use only:

1. the current/new chat;
2. this repository: `alisufyan-ai7/target-first-trading-system`.

Do not use any other GitHub repository, other ChatGPT chat/project, or unrelated account memory/context unless the user explicitly introduces that material into this project.

External sources may be used only as documented research data/reference; they do not become durable project context unless the relevant findings are checkpointed here.

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
11. `docs/PNL-EQUIVALENT-SIZING.md`
12. `docs/current-status.md`
13. `docs/decision-log.md`
14. `docs/STRATEGY-ENGINE-CONTRACT.md`
15. `docs/BUILD-AND-DEPLOYMENT-ROADMAP.md`
16. `strategies/STATUS.md`
17. `research/experiments/EXP-001-badar-video-reverse-engineering.md`
18. `research/experiments/EXP-002-engine-a-target-first-screen.md`
19. `research/experiments/EXP-014-original-engine-a-recovery-equivalent-sizing.md`
20. `research/experiments/EXP-015-target-first-opportunity-ranker-v0.1.md`

Inspect the A1–A9 recovery specifications only when the recovery history/mechanics matter.

## Non-negotiable operating context

Reference starting equity: about USD 500.

Economic anchor:

- XAUUSD reference size: 0.10 lot;
- normal successful-trade objective: about USD 50;
- USD 30–40 may be accepted only when independently validated;
- USD 70–100+ may be pursued under validated continuation/runner logic.

Daily framework:

- desired strong-day zone: about USD 150–200 when sufficient qualified opportunity exists;
- normal daily loss stop / stop-adding-risk zone: about USD 40;
- emergency hard ceiling: about USD 60 and **not** a routine sizing allowance;
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
meaningful standardized trade candidates
        ->
target-first probability / expected-value layer
        ->
P&L-equivalent position sizing
        ->
risk / margin / leverage / daily-budget / correlation gates
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

## EXP-014 is complete

### Part A — original Engine A recovery

EXP-002 remains historically important because it recorded positive simplified expectancy.

However, EXP-014 froze a numerical multi-dimensional reproduction protocol and then tested recovery variants A1–A9.

Conclusion:

**The original EXP-002 implementation is not honestly recoverable from the surviving evidence.**

- no original detector/backtest code survives;
- A6 was the closest causal reconstruction on frequency/split balance and average risk but produced target-first rates roughly half the EXP-002 benchmark and near-flat expectancy;
- A8/A9 were forensic/non-deployable tests and did not explain the full discrepancy;
- further post-hoc fitting to force the old benchmark is closed.

Do not call A6, v0.2-portable, A8, or A9 the recovered original.

### Part B — equivalent sizing

The forward sizing methodology is frozen in `docs/PNL-EQUIVALENT-SIZING.md`.

For non-Gold markets:

1. freeze/use an engine-conditioned native target or target function;
2. calculate symbol-specific lot size for approximately USD 50 gross;
3. apply structural-stop, margin, notional/leverage, daily-budget, aggregate-risk, and correlation gates;
4. use a separately validated USD 40/30 fallback only if safe;
5. otherwise reject.

Same-0.10-lot FX and volatility-burden target mappings are historical diagnostics, not forward rules.

## Current strategy/ranker state

There is currently **no strategy engine promoted as a validated execution lead**.

EXP-015 remains **PAUSED**.

Its Part-A recovery and sizing prerequisites are resolved, but it still lacks the essential input: at least one **prospectively specified, causal, reproducible, validated engine** emitting the common candidate contract.

The old broad-pivot Stage-1 EXP-015 statistics remain diagnostic only.

## Current technical gate / exact next direction

Do not restart EXP-002 recovery and do not resume EXP-015 yet.

The next strategy-development step is to define and freeze a **new causal strategy engine prospectively**. It may use Badar-derived evidence-supported concepts, or another independent setup family, but it must:

- have a new version/identity;
- define candidate, context, entry, structural invalidation, target logic, session rules, and outcome handling before outcome inspection;
- emit the common strategy-engine candidate contract;
- preserve development / validation / holdout separation;
- model realistic costs at the appropriate stage;
- avoid future-looking pivots and optimistic same-bar assumptions;
- be checkpointed before long computation.

A future Badar-derived engine is **not** the recovered EXP-002 engine.

## What a new chat must do first

Before executing a new long strategy computation:

1. read the ordered documents above;
2. summarize the post-EXP-014 project state;
3. confirm that EXP-014 is complete and EXP-015 remains paused;
4. identify the proposed new causal engine/specification;
5. freeze that specification and experiment protocol;
6. obtain user confirmation before launching the long computation.

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
