# Current Status

**Date:** 2026-09-23  
**Phase:** Phase 2 — Engine K v0.1 pre-outcome cleanup frozen; zero target/model outcomes; final cleanup preflight next

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

## Engine K / EXP-022 — current primary path

**Engine K v0.1 is prospectively frozen with zero Engine-K outcomes calculated.**

This is a deliberate course correction from sequential single-pattern XAU development.

Engine K directly scans all supported markets every five minutes and asks:

> Which market/direction currently has the highest validated probability of reaching an economically useful target before structural invalidation?

Wave-1 execution-research universe:

- XAUUSD;
- EURUSD;
- GBPUSD;
- USDJPY;
- EURJPY;
- AUDUSD;
- USDCAD;
- USDCHF.

XAGUSD is forecast-only until its contract/quantity economics are frozen.

Core Engine-K design:

- broad causal long/short state every 5m;
- latest confirmed 5m swing provides structural invalidation;
- Gold target ladder = +3 / +4 / +5 XAU;
- non-Gold target distances = prospectively frozen volatility-burden equivalents;
- P&L-equivalent sizing;
- primary per-trade structural risk <= USD20;
- pooled multi-market probability model;
- p >= 0.60 plus positive conservative EV required;
- maximum one open Engine-K trade across the portfolio for v0.1;
- no forced trade.

Checkpoint 1 is complete:

- exact rolling public repositories, commits, CSV blobs, research contract conventions, and dates are pinned in `research/provenance/EXP-022-wave1-data-manifest.md`;
- all pinned public samples currently share approximately 2026-03-23 through 2026-09-23 coverage;
- 2026-09-23 is excluded as potentially incomplete;
- final common-sample holdout is frozen at 2026-09-01 through 2026-09-22;
- zero Engine-K target/model outcomes have been inspected.

**Next action:** implement Engine-K causal feature/candidate code and preflight it against the pinned Wave-1 data with zero target/model outcomes, checkpoint the implementation, then run training + calibration only.

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
- Engine H v0.3: **post-raid 1m stop + fixed T40 target, with expanded Jan-2023–Feb-2025 development. 58 accepted trades (<100), primary-cost expectancy -USD4.52/trade; DEV-A -USD7.18, DEV-B -USD1.24. Validation/holdout untouched; not promoted.**
- Engine I v0.1: **development failed under EXP-020: 197 trades, T40 24.37%, primary-cost expectancy -USD5.15/trade, PF 0.631, DEV-A -USD6.20, DEV-B -USD4.09, max drawdown USD1,060.90; validation/holdout untouched; not promoted.**
- Engine J v0.1: **development failed under EXP-021: 307 trades, T40 27.04%, primary-cost expectancy -USD5.15/trade, PF 0.671, DEV-A -USD6.95, DEV-B -USD3.48, max drawdown USD1,659.93; validation/holdout untouched; not promoted.**
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

## Engine I / EXP-020 status

**Engine I v0.1 failed development and is stopped before validation.**

Development result:

- accepted trades: 197;
- T40 hit rate: 24.37%;
- gross expectancy before cost: about -USD0.15/trade;
- primary-cost expectancy: about -USD5.15/trade;
- primary-cost PF: about 0.631;
- total primary-cost P&L: -USD1,015.49;
- DEV-A expectancy: about -USD6.20/trade;
- DEV-B expectancy: about -USD4.09/trade;
- max drawdown: about USD1,060.90;
- bootstrap expectancy 95% interval: about -USD8.38 to -USD1.94;
- validation outcomes inspected: NO;
- fresh-holdout outcomes inspected: NO.

Interpretation: Engine I solved the sample-size problem but did not produce economic edge. Gross expectancy was approximately flat-to-negative before costs and both predeclared development subperiods were negative at the primary cost. This is a decisive failure, not a borderline result.

Do not create an Engine-I parameter grid or switch targets post hoc. Validation and holdout remain sealed.

## Engine J / EXP-021 status

**Engine J v0.1 failed development and is stopped before validation.**

Development result:

- 307 accepted trades;
- 349 qualifying compression breakouts;
- T40 hit rate: 27.04%;
- gross expectancy: about -USD0.15/trade;
- primary-cost expectancy: about -USD5.15/trade;
- primary-cost PF: about 0.671;
- total primary-cost P&L: -USD1,581.53;
- DEV-A expectancy: about -USD6.95/trade;
- DEV-B expectancy: about -USD3.48/trade;
- max drawdown: about USD1,659.93;
- bootstrap expectancy 95% interval: about -USD7.93 to -USD2.27;
- validation outcomes inspected: NO;
- fresh-holdout outcomes inspected: NO.

Interpretation: Engine J had ample frequency, but the direct compression-breakout thesis did not establish cost-adjusted edge. DEV-B improved and was gross-positive before cost, but both predeclared subperiods remained negative at the frozen primary cost. The combined bootstrap interval is entirely negative.

Do not tune the compression/breakout thresholds or switch targets post hoc. Validation and holdout remain sealed.

## Engine K / EXP-022 status

**Engine K v0.1 is the current primary discovery path.**

Purpose: scan supported markets every five minutes, evaluate long/short target-first states directly, apply economic/risk feasibility, and rank the best qualified opportunity rather than waiting for one named chart pattern.

Frozen primary execution-research universe:

- XAUUSD;
- EURUSD;
- GBPUSD;
- USDJPY;
- EURJPY;
- AUDUSD;
- USDCAD;
- USDCHF.

Frozen forecast-only universe:

- XAGUSD;
- NAS100;
- US30;
- SPX500.

Forecast-only markets are isolated from primary executable model fitting, calibration, ranking and P&L until their contract economics are prospectively frozen.

Pre-outcome cleanup completed before any Engine-K target/model outcomes:

- complete 5m bars require 5 M1 observations;
- complete 1h MTR bars require 60 M1 observations;
- delayed next entry cannot cross more than 5 chronological minutes;
- all 29 causal features are now explicitly defined;
- primary cost stress = 10% of gross target;
- stress cost = 20% of gross target;
- stop-risk cap = USD20;
- research leverage reference = 1:500;
- max research margin = USD100;
- max notional/equity = 100x / USD50,000;
- probability qualification = max(0.60, break-even probability + 0.05);
- Sep-1 through Sep-22 is an initial OOS holdout, not sufficient alone for live promotion.

Authoritative split:

- train: Mar-23 through May-31 2026;
- calibration: June 2026;
- historical secondary test: July-August 2026;
- final common-sample holdout: Sep-1 through Sep-22 2026;
- Sep-23 excluded as potentially incomplete.

Engine-K target outcomes calculated: **NO**.  
Engine-K model outcomes calculated: **NO**.

## Exact next action

Run the **final Engine-K zero-outcome cleanup preflight** across all 12 pinned datasets.

If it passes:

1. checkpoint the durable preflight result;
2. fit the primary model only on the 8 execution-research markets and only on Mar-23 through May-31;
3. calibrate only on June;
4. checkpoint before opening July-August secondary test;
5. do not inspect Sep-1 through Sep-22 final holdout until the earlier checkpoint is frozen.

Do not retune G/H/I/J. Do not add BTC or other new executable symbols to Engine-K v0.1 without first pinning data and freezing their contract/cost/margin economics under `research/provenance/EXP-022-symbol-admission-policy.md`.
