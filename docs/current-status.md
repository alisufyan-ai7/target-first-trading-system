# Current Status

**Date:** 2026-09-23  
**Phase:** Phase 2 — Engine G v0.1 frozen; EXP-016 prospective validation

## Authorized context

Only:

1. the originating/current project chat; and
2. this repository.

No other chats, projects, account memories, or GitHub repositories are authorized project context.

## System identity

We are building a **multi-strategy, multi-market trading system**.

Research/backtesting is the evidence layer, not the end objective.

The governing architecture remains:

~~~text
validated strategy engine
    -> standardized meaningful candidate
    -> target-first probability / EV layer
    -> P&L-equivalent sizing
    -> risk / margin / leverage / daily-budget / correlation gates
    -> cross-market ranking
    -> execution / management
    -> daily P&L state machine
    -> journal / performance database
~~~

The ranker is primarily a selector of validated-engine candidates, not a default trade inventor from every bar/pivot.

## User objective

Reference starting balance: about USD 500.

- Gold anchor: 0.10 lot;
- normal successful-trade objective: about USD 50;
- USD 30–40 acceptable when independently validated;
- USD 70–100+ allowed under validated continuation/runner logic;
- desired strong-day net zone: about USD 150–200 when sufficient qualified opportunity exists;
- normal daily loss stop / stop-adding-risk zone: about USD 40;
- emergency hard ceiling: about USD 60, not a normal sizing allowance;
- roughly 3–4 qualified trades/day is a desirable normal range, not a quota;
- low-output day = <= USD 50;
- aspirational low-output-day frequency: around 20% or less if evidence/risk permit;
- no forced trades, martingale, recovery sizing, or revenge trading.

## EXP-014 status

**EXP-014 is COMPLETE.**

### Part A — original EXP-002 Engine A recovery

A numerical reproduction-acceptance protocol was frozen before new recovery outcomes.

Recovery variants A1–A9 were then checkpointed one ambiguity at a time.

Final conclusion:

**The original EXP-002 implementation is not honestly recoverable from the surviving evidence.**

Important evidence:

- the audited March 1–August 20, 2026 one-minute XAUUSD research series contained exactly 230,813 rows, matching EXP-002's recorded row count;
- no original EXP-002 detector/backtest source code survives in repository history;
- A6 was the closest causal reconstruction on frequency/split balance and average structural risk:
  - 333 accepted trades;
  - 164 development / 169 holdout;
  - average risk about 1.053 Gold;
  - but overall T5 only about 15.0%;
  - holdout T5 about 13.6%;
  - holdout expectancy about +0.01 Gold/trade;
- A8 tested possible intrabar 5m-sweep timing leakage and failed;
- A9 tested optimistic fill-bar ordering and improved results, but holdout T5 reached only about 17.9% and holdout expectancy about +0.25 Gold/trade, still materially below EXP-002.

Therefore:

- EXP-002 remains preserved as a **historical exploratory positive result**;
- it is **not** a validated/reproducible execution engine;
- A6 is a diagnostic reconstruction only and is not promoted;
- A8/A9 are forensic/non-deployable;
- Engine A v0.2-portable remains a separate historical rewrite and is not a substitute;
- further post-hoc parameter hunting to force the old benchmark is closed.

See `research/experiments/EXP-014-original-engine-a-recovery-equivalent-sizing.md`.

### Part B — P&L-equivalent sizing

The forward methodology is frozen in:

- `docs/PNL-EQUIVALENT-SIZING.md`.

Current rule:

1. freeze/use the validated engine/market's native target or target function;
2. calculate the lot size that makes the normal target approximately USD 50 gross;
3. round to legal broker sizing without increasing risk;
4. apply unchanged structural-stop risk, margin, notional/leverage, remaining daily budget, aggregate open-stop risk, and correlation/common-factor gates;
5. if USD 50 economics are unsafe, use only a separately validated USD 40/30 fallback or reject.

Volatility-burden equivalence remains diagnostic only; it is not the governing target-distance method.

Same-0.10-lot FX work from EXP-012/013 also remains diagnostic only.

## Current strategy status

There is currently **no strategy engine promoted as a validated execution lead**.

- Engine G v0.1: **prospectively frozen on 2026-09-23; EXP-016 opened; zero outcomes at freeze; not yet validated or promoted.**
- Original Engine A / EXP-002: historical positive exploratory result; implementation unrecoverable.
- A6 recovery variant: closest causal diagnostic reconstruction; not promoted.
- Engine A v0.2-portable: historical rewrite; not promoted.
- Engine B first formulation: rejected.
- Engine C first formulation: rejected.
- Engine D formulations: not promoted.
- Engine E formulations: not promoted.
- Engine F v0.1: historical research evidence only; not a current execution lead.

This means the system has a validated architecture and sizing method, but still lacks the first reproducible strategy engine required to feed the production ranker.

## EXP-015 status

**EXP-015 remains PAUSED.**

Two former prerequisites are resolved:

- EXP-014 Part A is complete via the explicitly allowed unrecoverable conclusion;
- equivalent sizing is frozen.

The remaining blocker is substantive: EXP-015 needs at least one **prospectively specified, reproducible, validated strategy engine** emitting the common candidate contract.

Its historical broad-pivot Stage-1 XAU statistics remain diagnostics only.

## Engine G / EXP-016 status

**Engine G v0.1 is now frozen prospectively before outcomes.**

Frozen files:

- `strategies/engine-g-contextual-liquidity-reversal/SPEC-v0.1.md`;
- `research/experiments/EXP-016-engine-g-contextual-liquidity-reversal-v0.1.md`.

Checkpoint-0 state:

- rules frozen: YES;
- source snapshot and per-file manifest frozen: YES;
- development / validation / fresh-holdout split frozen: YES;
- delayed sensitivity sequence frozen: YES;
- Engine G outcomes calculated at freeze: NO.

Primary split:

- development: 2024-01-01 through 2025-02-28;
- validation: 2025-03-01 through 2025-08-31;
- fresh holdout: 2025-09-01 through 2026-02-28;
- March 1–August 20, 2026 remains quarantined from the primary decision.

EXP-015 remains paused until at least one reproducible engine validates.

## Exact next action

1. verify the immutable EXP-016 data manifest;
2. implement Engine G v0.1 exactly, including integer-tick price logic and causal liquidity lifecycle;
3. run implementation/unit/causality checks without changing the frozen rules;
4. run **development only**;
5. checkpoint the development result to GitHub before inspecting validation;
6. proceed to validation and holdout only in the frozen sequence.

Do **not** run sensitivity variants before the complete 48-bar / 1.60 center-rule development, validation, holdout, and primary conclusion have been checkpointed.

## Key unresolved question

Can one or more new reproducible engines, combined with the frozen equivalent-sizing method and cross-market ranking architecture, generate enough safe USD 30–100 opportunities to materially reduce low-output days without unacceptable leverage, drawdown, or loss frequency?
