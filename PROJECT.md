# Project Brief

_Last updated: 2026-09-23_

## Goal

Build and validate a **multi-strategy, multi-asset target-first trading system** whose operational purpose is to identify, rank, size, manage, and eventually execute the best qualified opportunities across supported markets.

The desired daily operating zone is approximately **USD 150–200 net when sufficient validated opportunity exists**.

Research/backtesting is the validation layer for building the system, not the end objective.

See docs/SYSTEM-BLUEPRINT.md for the authoritative architecture.

## Economic objective

Reference starting balance: about USD 500.

### Gold anchor

XAUUSD reference execution size: **0.10 lot**.

Under the common 100-oz-per-lot convention:

- 0.10 lot ~= 10 oz;
- USD 3 favorable Gold move ~= USD 30 gross;
- USD 4 ~= USD 40;
- USD 5 ~= USD 50;
- USD 7 ~= USD 70;
- USD 10 ~= USD 100.

Broker contract specifications must be verified before execution.

### Other markets

Do **not** assume 0.10 lot for every market.

For each non-Gold symbol:

1. freeze a native target distance from the validated engine/market behavior;
2. calculate the lot size that makes the normal successful target approximately USD 50 gross;
3. verify structural stop risk, margin, leverage/notional, correlation, and remaining daily budget;
4. use a smaller justified USD 30–40 opportunity or reject the trade if the full equivalent size is unsafe.

Generic economic conversion:

lot size ~= 50 / (native target distance x USD value per native unit at 1 lot).

## Profit flexibility

Normal successful-trade objective: about USD 50.

Allowed when validated:

- USD 30–40 for a nearer target with materially stronger target-first probability;
- USD 70–100+ for predeclared continuation/runner logic.

Reward/risk is normally an output of entry + structural stop + available target path, not a fixed number imposed first.

## Operating behavior

- scan all supported liquid markets;
- take only qualified opportunities;
- trade count is opportunity-driven, with roughly 3–4/day a desirable normal range rather than a quota;
- never lower quality merely because the daily target has not been reached;
- normal daily loss stop: about USD 40;
- rare absolute hard loss: about USD 60;
- no martingale;
- no size increase after losses;
- no revenge/recovery trading.

## Core decision problem

For every validated-engine candidate ask:

> From this exact entry and structural invalidation, what favorable move is likely to happen first, what economically useful target/size is feasible, and is this opportunity better than the alternatives currently available?

The eventual target ladder is approximately:

- T30;
- T40;
- T50;
- T70;
- T100+;

all evaluated before structural invalidation.

“Sure” means passing validated probability/EV and risk gates. It never means certainty.

## Candidate-generation architecture

The default architecture is:

~~~text
validated strategy engine
        ->
meaningful candidate
        ->
target-first probability / EV layer
        ->
cross-market ranking
~~~

The ranker is a **selector**, not an unrestricted trade inventor.

A broad statistical candidate generator may be researched separately, but it must itself be versioned and validated as an engine before it bypasses this contract.

See docs/STRATEGY-ENGINE-CONTRACT.md.

## Original Engine A preservation rule

Badar Tanveer's supplied/public trading examples were the source for the first Engine A hypothesis.

EXP-002 recorded positive simplified expectancy in both development and holdout. That historical result remains preserved.

EXP-014 then froze a numerical reproduction protocol and systematically tested recovery variants A1–A9. No causal variant reproduced the complete EXP-002 benchmark; the original implementation/code was not preserved. Therefore:

- EXP-002 is a **historical exploratory positive result**, not a reproducible validated engine;
- Engine A v0.2-portable remains a separate later rewrite and does not invalidate or reproduce EXP-002;
- A6 is the closest causal recovery diagnostic but is not promoted;
- A8/A9 are forensic/non-deployable;
- further benchmark-fitting to recover the lost implementation is closed.

Equivalent sizing is now frozen in `docs/PNL-EQUIVALENT-SIZING.md`.

Before EXP-015 resumes, the project must prospectively define and validate at least one causal, reproducible strategy engine that emits the common candidate contract.

## Consistency objective

The project optimizes the distribution of daily outcomes, not only total return.

Key metrics include median daily P&L, low-output-day frequency, 5-day rolling consistency, losing days, drawdown, consecutive low-output days, and target-rung capture.

A few huge days do not compensate for a system dominated by zero/low-output days if that distribution fails the user's objective.

## System-development path

Historical/reproducible engines -> out-of-sample validation -> independent-feed validation -> portfolio simulation -> paper/demo live scanner -> signal-only -> human approval/semi-auto -> fully automatic execution only after evidence.

See docs/BUILD-AND-DEPLOYMENT-ROADMAP.md.
