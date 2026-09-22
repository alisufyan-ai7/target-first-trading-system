# Current Status

**Date:** 2026-09-22  
**Phase:** System-context consolidation and original Engine A recovery

## Authorized context

Only:

1. the originating/current project chat; and
2. this repository.

No other chats, projects, account memories, or GitHub repositories are authorized project context.

## System identity

We are building a **multi-strategy, multi-market trading system**.

Research/backtesting is the evidence layer, not the end objective.

See:

- docs/SYSTEM-BLUEPRINT.md;
- docs/ORIGINAL-PROJECT-CONTEXT.md;
- docs/BUILD-AND-DEPLOYMENT-ROADMAP.md.

## User objective

Reference starting balance: about USD 500.

- Gold anchor: 0.10 lot;
- normal successful-trade objective: about USD 50;
- USD 30–40 acceptable when the nearer target is materially more reliable;
- USD 70–100+ allowed when continuation evidence supports it;
- desired strong-day net zone: about USD 150–200;
- normal daily loss stop: about USD 40;
- emergency hard ceiling: about USD 60;
- roughly 3–4 qualified trades/day is a desirable normal range, not a quota;
- low-output day = <= USD 50;
- aspirational low-output-day frequency: around 20% or less if evidence/risk permit.

## Correct sizing interpretation

### XAUUSD

Reference size = 0.10 lot.

### Other markets

Use symbol-specific P&L-equivalent sizing for a frozen native target distance.

Then apply structural-risk, margin, leverage/notional, daily-budget, and correlation gates.

Same-0.10-lot FX work from EXP-012/013 remains diagnostic only.

## Original Engine A / Gold

EXP-002 remains the active original Badar-inspired Gold lead.

Recorded simplified results:

- about 372 signals overall;
- USD 5 target-first ~29.6%;
- average structural risk distance ~USD 1.02 Gold;
- median favorable excursion ~USD 3.30;
- simplified expectancy ~+USD 0.79 Gold/trade before costs.

Holdout:

- ~187 trades;
- USD 2 target-first 48.7%;
- USD 3 41.7%;
- USD 4 31.6%;
- USD 5 27.3%;
- simplified expectancy ~+USD 0.72 Gold/trade before costs.

## Engine A distinction

Engine A v0.2-portable is a different later rewrite.

Its poor Gold results do not invalidate EXP-002.

The next technical gate is to reconstruct the original Engine A and reproduce EXP-002 within reasonable tolerance.

## Other engine status

- Engine B first formulation: rejected;
- Engine C first formulation: rejected;
- Engine D opening-range formulations: not promoted;
- Engine E volatility-expansion formulations: not promoted;
- Engine F v0.1: historically interesting GBPUSD arm but not a current execution lead after economic reinterpretation.

## Target-first ranker status

The previous broad-pivot ranker experiment has been renumbered to **EXP-015** and **paused**.

Reason:

1. it began before original Engine A recovery;
2. it used broad generic structural candidates rather than validated-engine candidates;
3. its initial FX fixed-size assumptions predated the corrected equivalent-sizing rule.

Its Stage-1 XAU candidate statistics are retained as diagnostics, not as the governing system architecture.

## Immediate plan

1. preserve/review detailed Badar/video evidence;
2. execute EXP-014 original Engine A recovery;
3. verify reproduction against EXP-002;
4. freeze equivalent-sizing method for non-Gold markets;
5. persist a standard strategy-engine candidate contract;
6. then redesign/resume EXP-015 so the ranker consumes validated-engine candidates;
7. only after that perform multi-market portfolio daily-distribution testing.

## Key unresolved question

Can the recovered positive Gold Engine A plus additional independently validated engines and economically feasible cross-market sizing generate enough high-quality USD 30–100 opportunities to materially reduce low-output days without unacceptable leverage, drawdown, or loss frequency?
