# Current Status

**Date:** 2026-09-23  
**Phase:** Phase 2 — Engine G failed; Engine H v0.1/v0.2 insufficient evidence; validation/holdout preserved

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

- Engine G v0.1: **prospectively frozen, then failed the EXP-016 development gate: 71 accepted trades (<100 minimum), -USD 9.27/trade at primary cost, bootstrap expectancy CI entirely below zero. Validation/holdout remain untouched; not promoted.**
- Engine H v0.1: **prospectively frozen from the two video motifs, then produced only 2 accepted development trades from 180 in-window raids versus the >=100 minimum. Formally insufficient evidence; validation/holdout untouched; not promoted.**
- Engine H v0.2: **simplified confirmation to MSS-within-20 + next-active-M1-open entry. 69 setups reached economic admission, but only 6 passed target/stop/room/R:R/risk geometry. Primary-cost expectancy +USD0.08/trade with bootstrap CI -USD32.65 to +USD40.00; insufficient evidence; validation/holdout untouched.**
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

**Engine G v0.1 is frozen and its development gate is complete.**

Development result:

- accepted trades: 71 versus frozen >=100 minimum;
- S1 hit rate: about 16.9%;
- primary-cost net expectancy: about -USD 9.27/trade;
- primary-cost profit factor: about 0.496;
- 95% moving-block-bootstrap expectancy interval: about -USD 15.14 to -USD 2.52;
- max drawdown: about USD 826.29 on the USD 500 reference-equity curve;
- validation outcomes inspected: NO;
- fresh-holdout outcomes inspected: NO;
- sensitivity diagnostics run: NO.

Because the mandatory development expectancy criterion already failed and the minimum development trade count was not reached, EXP-016 v0.1 is stopped before validation. The untouched validation and holdout periods remain available for a genuinely prospective future engine/version.

EXP-015 remains paused until at least one reproducible engine validates.

## Exact next action

Do not inspect validation/holdout for Engine G v0.1, Engine H v0.1, or Engine H v0.2, and do not retune any frozen version.

The key new evidence is architectural: H v0.2's simplified confirmation produced **69 causal MSS/next-open admission candidates**, but only **6** survived the economic geometry. The remaining bottleneck is therefore not primarily confirmation anymore; it is the combination of:

- opposite-range target;
- sweep-extreme structural stop;
- >=3.000-XAU target room;
- >=2.0 reward/risk;
- <=USD40 gross structural risk.

A next experiment should prospectively test a different target/stop architecture while preserving the useful range-raid-into-pre-existing-FVG location concept. It must be versioned as Engine H v0.3 or a new engine before any outcome calculation.

EXP-015 remains paused until at least one reproducible engine validates.
