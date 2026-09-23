# New Chat Handoff — Target-First Trading System

_Last updated: 2026-09-23 after EXP-019_

Use this file as the **first document to read whenever a new ChatGPT conversation is started for this project**.

## Strict context rule

For this project, use only:

1. the current/new chat;
2. this repository: `alisufyan-ai7/target-first-trading-system`.

Do not use any other GitHub repository, other ChatGPT chat/project, or unrelated account memory/context unless the user explicitly introduces that material into this project.

External sources may be used only as documented research data/reference; they do not become durable project context unless relevant findings are checkpointed here.

## Project identity

We are **building a trading system**, not merely conducting research.

Research/backtesting is the evidence layer used to build a profitable, reproducible multi-strategy, multi-market system.

## Read in this order before new work

1. `README.md`
2. `PROJECT.md`
3. `docs/SOURCE-OF-TRUTH.md`
4. `docs/SYSTEM-BLUEPRINT.md`
5. `docs/ORIGINAL-PROJECT-CONTEXT.md`
6. `docs/objectives.md`
7. `docs/risk-framework.md`
8. `docs/PNL-EQUIVALENT-SIZING.md`
9. `docs/current-status.md`
10. `docs/decision-log.md`
11. `docs/STRATEGY-ENGINE-CONTRACT.md`
12. `strategies/STATUS.md`
13. `research/experiments/EXP-014-original-engine-a-recovery-equivalent-sizing.md`
14. `research/experiments/EXP-015-target-first-opportunity-ranker-v0.1.md`
15. `research/experiments/EXP-016-engine-g-contextual-liquidity-reversal-v0.1.md`
16. `research/experiments/EXP-017-engine-h-range-raid-preexisting-fvg-reversal-v0.1.md`
17. `research/experiments/EXP-018-engine-h-v0.2-simplified-mss-confirmation.md`
18. `research/experiments/EXP-019-engine-h-v0.3-postraid-stop-t40.md`
19. `research/experiments/EXP-020-engine-i-session-expansion-continuation-v0.1.md`
20. `strategies/engine-i-session-expansion-continuation/SPEC-v0.1.md`

Read the Badar/video and timeframe documents only when needed for historical context; do not use them as justification to keep retuning reversal engines.

## Non-negotiable operating objective

Reference starting equity: about USD 500.

- XAUUSD economic anchor: 0.10 lot;
- normal successful-trade objective: about USD 50;
- USD 30–40 allowed only when independently validated;
- USD 70–100+ allowed only under validated continuation/runner logic;
- desired strong-day net zone: about USD 150–200 when sufficient opportunity exists;
- normal daily stop-adding-risk zone: about -USD 40;
- emergency hard ceiling: about -USD 60;
- roughly 3–4 qualified trades/day is desirable, not a quota;
- low-output day = <= USD 50;
- aspirational low-output-day frequency: toward ~20% if evidence and risk permit;
- no forced trades, martingale, recovery sizing, or revenge trading.

## Core architecture

```text
validated strategy engines
    ->
standardized meaningful candidates
    ->
target-first probability / EV selector
    ->
P&L-equivalent sizing
    ->
risk / margin / leverage / daily-budget / correlation gates
    ->
cross-market ranking
    ->
execution / management
    ->
daily P&L state machine
```

EXP-015 remains paused until a reproducible engine validates.

## EXP-014 conclusion

The original EXP-002 positive Engine A result is historical but not reproducible from surviving evidence.

A1–A9 did not honestly recover it.

Do not restart EXP-002 recovery.

Equivalent non-Gold sizing is frozen in `docs/PNL-EQUIVALENT-SIZING.md`.

## Engine G / EXP-016

Engine G v0.1 was prospectively frozen and failed development:

- accepted trades: 71 vs >=100 required;
- primary-cost expectancy: about -USD 9.27/trade;
- primary-cost PF: about 0.496;
- 95% bootstrap expectancy interval entirely negative;
- validation and holdout untouched.

Do not retune or validate Engine G v0.1.

## Engine H family / EXP-017–019

### H v0.1

- 180 in-window raids;
- only 2 accepted trades;
- insufficient evidence;
- validation/holdout untouched.

### H v0.2

- simplified to MSS-within-20 + next-open;
- 69 setups reached economic admission;
- only 6 accepted trades;
- primary-cost expectancy +USD 0.08/trade but statistically meaningless;
- validation/holdout untouched.

### H v0.3 / EXP-019

Prospectively changed to:

- post-raid 1m structural stop;
- fixed T40 = +4.000 XAU actual target;
- expanded unused development Jan-2023 through Feb-2025;
- validation Mar-Aug 2025 untouched;
- fresh holdout Sep 2025-Feb 2026 untouched.

Development result:

- accepted trades: 58 vs >=100 required;
- T30 hit: 36.21%;
- T40 hit: 29.31%;
- T50 hit: 20.69%;
- T70 hit: 18.97%;
- T100 hit: 8.62%;
- primary-cost expectancy: -USD 4.52/trade;
- PF: 0.703;
- net P&L: -USD 261.98;
- 95% bootstrap expectancy interval: [-USD 11.60, +USD 2.69];
- DEV-A 2023 expectancy: -USD 7.18/trade;
- DEV-B Jan-2024–Feb-2025 expectancy: -USD 1.24/trade;
- max drawdown: USD 336.05;
- worst losing run: 7 trades / -USD 163.45.

Frozen development gate failed on trade count and all expectancy-sign requirements.

**Engine H thesis family is paused. Do not create H v0.4 by tuning the same reversal thesis on the same development evidence.**

## Engine I / EXP-020 freeze checkpoint

Engine I v0.1 — Session Expansion / Continuation is now prospectively frozen before outcomes.

Center rule:

```text
established 15m direction
    -> Asian-session boundary breakout/acceptance
    -> strong 5m expansion
    -> 25%-60% controlled pullback holding the boundary
    -> 1m continuation break
    -> next-active-M1-open
    -> structural pullback stop
    -> fixed T40 actual target
```

Frozen evidence design:

- warm-up Dec-2022;
- development Jan-2023 through Feb-2025;
- DEV-A=2023;
- DEV-B=Jan-2024 through Feb-2025;
- validation Mar-Aug 2025 remains closed;
- fresh holdout Sep-2025 through Feb-2026 remains closed;
- primary round-trip cost USD5 / 0.50 XAU;
- development requires >=100 accepted trades, positive combined/DEV-A/DEV-B expectancy, PF >=1.10, max drawdown <=USD200 and recovery factor >=1.0;
- no Engine-I v0.1 sensitivity grid is authorized.

At this checkpoint zero Engine-I outcomes have been calculated. Do not backtest until the user reviews/approves the frozen specification and the implementation/provenance checkpoint is complete.

## Current promotion state

**No strategy engine is currently promoted as a validated execution lead.**

This is the system's main blocker.

EXP-015 remains paused.

## Exact next strategy direction

The next engine must be a genuinely different causal family, not another liquidity-reversal variation.

Preferred next family:

### Engine I — Session Expansion / Continuation

Concept:

```text
established intraday direction
    ->
liquidity / session boundary cleared
    ->
strong session displacement
    ->
controlled pullback
    ->
continuation confirmation
    ->
structural pullback stop
    ->
T30 / T40 / T50 ladder
```

Why this is preferred:

- G/H repeatedly tested reversal logic and failed development;
- continuation is structurally different and can diversify the future engine portfolio;
- the desired system needs several independent profitable engines, not one over-tuned motif;
- continuation can naturally use tighter pullback stops and target-first ladder economics.

## Rapid engine-development discipline

The goal is to find a profitable engine **quickly without overfitting**.

For Engine I:

1. use only development data first;
2. prospectively freeze a simple center configuration;
3. avoid a huge parameter grid;
4. target >=100 development trades if feasible;
5. use realistic primary transaction cost from the start;
6. require positive expectancy and positive subperiod expectancy before validation;
7. keep validation and fresh holdout untouched until the development gate passes;
8. if the center rule fails decisively, stop quickly and move to the next genuinely different family rather than creating endless I v0.x variants.

## Recommended Engine-I split

Reuse untouched periods only if the new chat confirms they remain uncontaminated for Engine I:

- development: Jan-2023 through Feb-2025;
- validation: Mar-Aug 2025;
- fresh holdout: Sep 2025-Feb 2026;
- previously heavily researched 2026 Mar-Aug period remains quarantined.

Before freezing Engine I, explicitly verify data-provenance and contamination status.

## First task in the new chat

Do **not** immediately backtest.

Current state is already past the initial Engine-I design freeze. The next steps are:

1. read this handoff and the ordered source-of-truth files including EXP-020 and Engine-I v0.1 spec;
2. confirm that zero Engine-I outcomes have been calculated;
3. present/review the frozen Engine-I v0.1 mechanics and rationale with the user;
4. obtain user approval before launching development;
5. implement exact-arithmetic Engine-I code and a development-only harness;
6. re-verify frozen source manifest, unit checks and causal sequencing with zero outcomes;
7. checkpoint the pre-outcome implementation/provenance state;
8. only then run combined development Jan-2023 through Feb-2025;
9. stop before validation if any frozen development gate fails.

## Required development gate for Engine I

Do not invent a favorable threshold after seeing results.

Recommended predeclared minimum:

- accepted development trades >=100;
- primary-cost expectancy >0;
- DEV-A expectancy >0;
- DEV-B expectancy >0;
- primary-cost PF materially >1.0;
- no causal leakage or optimistic same-bar handling.

Validation/holdout promotion gates should be frozen before development.

## GitHub checkpoint discipline

Before any substantial experiment:

- create/freeze the strategy specification;
- create the experiment record;
- freeze source provenance, split, costs, and evidence gates.

After each material result, update:

- experiment file;
- `docs/current-status.md`;
- `docs/decision-log.md`;
- `strategies/STATUS.md`;
- `CHANGELOG.md`.

## Principle for speed

“Build a profitable engine quickly” means:

- test **distinct hypotheses** quickly;
- reject weak development results quickly;
- preserve validation/holdout;
- do not spend many versions tuning one failed thesis;
- favor simple causal engines with enough candidate frequency and realistic transaction-cost headroom.

Do not trade statistical certainty for speed.
