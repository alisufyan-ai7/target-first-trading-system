# New Chat Handoff — Target-First Trading System

_Last updated: 2026-09-24 after Engine K v0.2 / EXP-023 freeze and pipeline-policy checkpoint_

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
4. `docs/PIPELINE-WORKFLOW-POLICY.md`
5. `docs/SYSTEM-BLUEPRINT.md`
6. `docs/ORIGINAL-PROJECT-CONTEXT.md`
7. `docs/objectives.md`
8. `docs/risk-framework.md`
9. `docs/PNL-EQUIVALENT-SIZING.md`
10. `docs/current-status.md`
11. `docs/decision-log.md`
12. `docs/STRATEGY-ENGINE-CONTRACT.md`
13. `strategies/STATUS.md`
14. `research/experiments/EXP-014-original-engine-a-recovery-equivalent-sizing.md`
15. `research/experiments/EXP-015-target-first-opportunity-ranker-v0.1.md`
16. `research/experiments/EXP-016-engine-g-contextual-liquidity-reversal-v0.1.md`
17. `research/experiments/EXP-017-engine-h-range-raid-preexisting-fvg-reversal-v0.1.md`
18. `research/experiments/EXP-018-engine-h-v0.2-simplified-mss-confirmation.md`
19. `research/experiments/EXP-019-engine-h-v0.3-postraid-stop-t40.md`
20. `research/experiments/EXP-020-engine-i-session-expansion-continuation-v0.1.md`
21. `strategies/engine-i-session-expansion-continuation/SPEC-v0.1.md`
22. `research/experiments/EXP-021-engine-j-volatility-compression-breakout-v0.1.md`
23. `strategies/engine-k-direct-target-move-scanner/SPEC-v0.1.md`
24. `research/experiments/EXP-022-engine-k-multimarket-direct-target-move-scanner-v0.1.md`
25. `strategies/engine-k-direct-target-move-scanner/SPEC-v0.2.md`
26. `research/experiments/EXP-023-engine-k-v0.2-risk-normalized-target-scanner.md`
27. `research/provenance/EXP-022-wave1-data-manifest.md`
28. `research/provenance/EXP-022-symbol-admission-policy.md`

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



## Engine K / EXP-022 — CURRENT PRIMARY PATH

The user explicitly redirected the project away from sequential one-pattern XAU discovery toward the actual operating requirement:

> continuously scan all supported markets and identify where an economically useful move is most likely next.

Engine K v0.1 is now prospectively frozen as a **multi-market direct target-move forecasting engine**.

Wave-1 execution-research universe:

- XAUUSD;
- EURUSD;
- GBPUSD;
- USDJPY;
- EURJPY;
- AUDUSD;
- USDCAD;
- USDCHF.

Forecast-only until contract economics are frozen:

- XAGUSD;
- NAS100;
- US30;
- SPX500.

These four markets cannot influence primary executable model fitting, calibration, ranking or P&L simulation.

Engine K:

- scores long and short every 5 minutes;
- uses a confirmed structural pivot stop;
- asks Gold directly about +3/+4/+5 XAU moves;
- uses frozen non-Gold movement-equivalence distances;
- calculates P&L-equivalent size;
- requires primary structural risk <= USD20;
- uses a pooled multi-market probability model;
- requires calibrated p >= max(0.60, break-even probability + 0.05) and positive primary-cost EV;
- trades nothing if no candidate qualifies.

Frozen rolling-source provenance:

- `research/provenance/EXP-022-wave1-data-manifest.md`.

Frozen split:

- training: 2026-03-23 through 2026-05-31;
- calibration: 2026-06-01 through 2026-06-30;
- secondary test: 2026-07-01 through 2026-08-31;
- final common-sample holdout: 2026-09-01 through 2026-09-22.

At the checkpoint when this handoff was updated:

- Engine-K target outcomes calculated: NO;
- Engine-K model outcomes calculated: NO;
- data provenance: COMPLETE;
- pre-outcome universe/economic/feature cleanup: COMPLETE;
- primary execution universe: 8 markets;
- forecast-only universe: 4 markets;
- final cleanup preflight: PASSED; result commit `48aa0af80b7fc2fff1dab56d3fb617b1c2140f3f`.

Files:

- `strategies/engine-k-direct-target-move-scanner/SPEC-v0.1.md`;
- `research/experiments/EXP-022-engine-k-multimarket-direct-target-move-scanner-v0.1.md`;
- `research/provenance/EXP-022-wave1-data-manifest.md`;
- `research/code/engine_k_v0_1.py`;
- `research/code/run_engine_k_preflight.py`;
- `.github/workflows/exp022-engine-k-preflight.yml`.

Do not return to G/H/I/J tuning while Engine K is being evaluated.

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


## Engine I / EXP-020 development outcome

Engine I v0.1 has now completed development and failed decisively.

Frozen Jan-2023 through Feb-2025 development result:

- accepted trades: 197;
- T40 hit rate: 24.37%;
- gross expectancy: approximately -USD0.15/trade;
- primary-cost expectancy: approximately -USD5.15/trade;
- primary-cost PF: 0.631;
- total primary-cost P&L: -USD1,015.49;
- max drawdown: USD1,060.90;
- DEV-A expectancy: approximately -USD6.20/trade;
- DEV-B expectancy: approximately -USD4.09/trade;
- 95% block-bootstrap expectancy interval: approximately -USD8.38 to -USD1.94.

Only the >=100 trade-count gate passed. Combined expectancy, both subperiod expectancy gates, PF, drawdown and recovery factor failed.

Development workflow run: `35844194955`.

Durable result commit: `a891dc1aa956151df1b87f6c9e03daae2dabf29b`.

Validation Mar-Aug 2025 and fresh holdout Sep-2025 through Feb-2026 were not loaded or inspected.

Do not:

- run Engine-I validation/holdout;
- create a post-hoc Engine-I sensitivity grid;
- switch T40 to another target because the diagnostic ladder looks different;
- create H v0.4 or reopen G/H reversal tuning.

Current strategy action: move to a genuinely different prospectively frozen engine family. EXP-015 remains paused until one reproducible engine validates.


## Engine J / EXP-021 prospective freeze

After Engine I failed development, Engine J v0.1 — Volatility Compression Breakout — was prospectively frozen before any Engine-J outcome.

Center rule:

```text
same-day 5m volatility baseline
    -> 30m compression / compact box
    -> strong 5m direct breakout
    -> next-active-M1-open
    -> breakout-bar structural stop
    -> fixed T40
```

Key rules:

- baseline = older 24 of previous 30 same-day active 5m bars;
- compression = latest six active 5m bars;
- compression average range <=80% of baseline median;
- compression box width <=3.0x baseline median;
- breakout range >=1.25x baseline median;
- breakout body >=60%;
- breakout close in outer 25%;
- first qualifying breakout per side/day;
- structural stop one tick beyond breakout-bar opposite extreme;
- gross stop <=USD40-equivalent / 4000 ticks;
- primary cost USD5;
- T40 actual target;
- same Jan-2023–Feb-2025 development and sealed validation/holdout;
- same development/validation promotion gates;
- no parameter grid.

Files:

- `strategies/engine-j-volatility-compression-breakout/SPEC-v0.1.md`;
- `research/experiments/EXP-021-engine-j-volatility-compression-breakout-v0.1.md`.

At this checkpoint:

- Engine-J outcomes calculated: NO;
- Engine-J implementation started: NO;
- Engine-J development launched: NO.

Next: review spec, implement/preflight, then development only.


## Engine J / EXP-021 implementation checkpoint

Engine J v0.1 is now implemented and preflight-verified with **zero Engine-J outcomes calculated**.

Reference implementation:

- `research/code/engine-j-v0.1.js`;
- final preflight-ready implementation commit: `a59cc2cf1a48b49c6e76a7da99aa7ed51dd56064`.

Harnesses:

- `research/code/run-engine-j-preflight.js`;
- `research/code/run-engine-j-development.js`;
- `.github/workflows/exp021-engine-j-preflight.yml`;
- `.github/workflows/exp021-engine-j-development.yml`.

Final preflight:

- run ID `35869719236`;
- tested SHA `88717bb88993f2cbbffe1f7174e6d49e3201695f`;
- result commit `1473aa343c7d0ea746c4ff643571fb729329f687`;
- engine SHA-256 `21f60faee3263d5a33b7b5448a79e1355e30562bb4f5dcc677b09e7e3b6ac1ce`;
- 27 frozen warm-up/development files verified;
- 1,182,240 rows / 59,108,737 bytes;
- all 16 Engine-J self/causality tests passed;
- validation/holdout loaded: NO;
- development run: NO.

The only permitted next outcome computation is EXP-021 combined development Jan-2023 through Feb-2025. If any frozen development gate fails, stop before validation and preserve Mar-Aug 2025 validation plus Sep-2025–Feb-2026 fresh holdout.


## Engine J / EXP-021 development outcome

Engine J v0.1 completed frozen Jan-2023 through Feb-2025 development and failed decisively.

Result:

- accepted trades: 307;
- qualifying breakouts: 349;
- T40 hit rate: 27.04%;
- gross expectancy: approximately -USD0.15/trade;
- primary-cost expectancy: approximately -USD5.15/trade;
- primary-cost PF: 0.671;
- total primary-cost P&L: -USD1,581.53;
- max drawdown: USD1,659.93;
- DEV-A primary-cost expectancy: approximately -USD6.95/trade;
- DEV-B primary-cost expectancy: approximately -USD3.48/trade;
- 95% block-bootstrap primary-cost expectancy interval: approximately -USD7.93 to -USD2.27.

DEV-B gross expectancy improved to approximately +USD1.52/trade before cost, but remained negative under the prospectively frozen USD5 primary cost.

Development workflow run: `35870120388`.

Durable result commit: `f9034af1c8f86fb43561d51383e5b4164774dc09`.

Validation Mar-Aug 2025 and fresh holdout Sep-2025 through Feb-2026 were not loaded or inspected.

Do not:

- run Engine-J validation/holdout;
- run a post-hoc Engine-J compression/breakout parameter grid;
- switch T40 to T30/T50/etc. after seeing diagnostics;
- reopen G/H/I tuning.

Current strategy action: move to a genuinely different prospectively frozen engine family. EXP-015 remains paused until one reproducible engine validates.



### Final zero-outcome cleanup preflight

Authoritative tested SHA:

`2c319cd45cbae6cdb1934540f6933890886c1812`

Durable result commit:

`48aa0af80b7fc2fff1dab56d3fb617b1c2140f3f`

Result:

- 11/11 cleanup self-tests passed;
- 205,196 execution structural states through June 30;
- 7,098 execution target rungs passed pre-probability economic feasibility;
- 103,041 forecast-only structural states;
- target outcomes calculated: NO;
- model outcomes calculated: NO;
- July-August state/outcome distributions inspected by authoritative preflight: NO;
- September final-holdout outcomes inspected: NO.

The next permitted stage is training Mar23-May31 + June calibration only. Checkpoint before opening July-August.

## Engine K pre-outcome cleanup — authoritative current rules

This section supersedes any older “exact next strategy direction” wording elsewhere in this historical handoff.

Engine K is the current primary path.

Execution-research markets:

- XAUUSD;
- EURUSD;
- GBPUSD;
- USDJPY;
- EURJPY;
- AUDUSD;
- USDCAD;
- USDCHF.

Forecast-only:

- XAGUSD;
- NAS100;
- US30;
- SPX500.

Research-only feasibility gates before broker-native economics:

- reference equity USD500;
- stop risk <=USD20;
- primary cost = 10% of gross target;
- stress cost = 20% of gross target;
- notional/equity <=100x;
- research margin <=USD100 at 1:500;
- p_required = max(0.60, p_break-even + 0.05);
- primary-cost EV >0.

Causality:

- complete 5m bars only;
- complete 1h MTR bars only;
- next-open entry gap <=5 minutes;
- 29 causal features frozen in code/spec;
- forecast-only markets excluded from executable model fit.

Split:

- train: Mar-23–May-31 2026;
- calibration: June;
- secondary test: July-August;
- final common holdout: Sep-1–Sep-22;
- Sep-23 excluded.

The final September holdout is an initial OOS test only. Live promotion additionally requires longer-history/independent-feed and forward/demo evidence.

BTCUSD/BTCUSDT, GBPJPY and additional liquid markets are desired expansion candidates, but they are not admitted to Engine-K v0.1 until pinned data and exact executable contract/cost/margin conventions are frozen.

**Next:** final zero-outcome cleanup preflight. Only after it passes may the primary eight-market training period be labeled/fitted.


## Engine K v0.2 / EXP-023 authoritative current state

EXP-022 Engine K v0.1 is closed before secondary testing.

v0.1 durable training/calibration result:

- run `35901103493`;
- result/model commit `d24e05ca513777d63a5d0f6762dfdb35bc42cfc3`;
- 7,098 executable labeled rungs, all XAUUSD;
- seven FX execution markets: zero executable rungs;
- zero qualified trades under frozen v0.1 threshold;
- July-August and Sep final holdout unopened.

EXP-023 Engine K v0.2 is now the current path and is prospectively frozen with zero v0.2 outcomes.

v0.2 keeps the dense scanner, structural stops, feature contract, HGB/Platt model, risk framework and protected evidence split.

Prospective economic redesign:

- Gold: unchanged +3/+4/+5 XAU, 0.10 lot;
- non-Gold T30/T40/T50 target distance: 1.5R / 2.0R / 2.5R from unchanged structural stop;
- define target first, then downward P&L-equivalent size;
- p_required = max(0.50, p_break-even +0.10);
- positive primary EV and all USD20/notional/margin gates still required.

Files to read:

- `strategies/engine-k-direct-target-move-scanner/SPEC-v0.2.md`;
- `research/experiments/EXP-023-engine-k-v0.2-risk-normalized-target-scanner.md`;
- `research/code/engine_k_v0_2.py`;
- `research/code/run_engine_k_v0_2_preflight.py`.

**Next action:** run zero-outcome EXP-023 preflight through June only. Require >=200 economically admissible states in every execution market. Do not calculate v0.2 target labels until that passes.


## Long-running pipeline operating rule

Read and follow `docs/PIPELINE-WORKFLOW-POLICY.md`.

Default behavior after triggering a long GitHub Actions research run:

- confirm the intended workflow once;
- do not repeatedly poll while waiting;
- do only work that is independent of the pending result and cannot mutate the running experiment;
- if no independent work remains, end the turn;
- on the next user message, inspect GitHub's durable result first and continue from there;
- workflows that commit generated results should `git pull --rebase origin main` before push.

This is part of project reproducibility, not merely a conversational preference.


### EXP-023 v0.2 preflight PASS

Durable result commit:

`02a2ab0b1ea7f21092b06165a0ca8f0638d4c41b`

All 8 execution markets passed the >=200 unique admissible-state gate through June:

- XAUUSD 2,366;
- EURUSD 13,098;
- GBPUSD 14,466;
- USDJPY 10,503;
- EURJPY 10,869;
- AUDUSD 18,336;
- USDCAD 9,397;
- USDCHF 15,203.

Total: 94,238 unique admissible states / 281,955 admissible rungs.

No v0.2 target/model outcomes, July-August outcomes, or September holdout outcomes were inspected at preflight.

**Current next action:** trigger only EXP-023 v0.2 Mar23-May31 training + June calibration. Apply the frozen pre-secondary gate before opening July-August.


### EXP-023 v0.2 training/June outcome — FAIL

Durable result/model commit:

`763aefadbe56ee7012b475dcb677f6f78d8036ec`

Result:

- 281,955 labeled rungs across all 8 execution markets;
- June AUC T30/T40/T50 about 0.674 / 0.710 / 0.743;
- 2 qualified combined trades;
- 0 qualified June trades;
- >=100 combined frequency gate FAIL;
- >=20 June gate FAIL;
- June hit-rate/expectancy/PF gates FAIL/unavailable;
- June DD/integrity gates PASS;
- July-August secondary-test loaded/labeled: NO;
- September final holdout loaded/labeled: NO.

Engine K v0.2 is closed before secondary testing.

Do not lower its threshold or open protected periods. Any continuation requires a newly frozen version using only the already-inspected Mar-Jun development evidence.


## Engine K v0.3 / EXP-024 authoritative current state

Engine K v0.2 is closed before secondary testing.

v0.3 is the active path.

Frozen design:

- HGB fit Mar23-Apr30;
- market-direction-aware Platt calibration May;
- June true development gate;
- same v0.2 targets/economics;
- qualification = positive primary EV and positive stress EV;
- no fixed probability floor;
- same one-open/daily-risk state machine.

June mandatory gate:

- >=200 states per market;
- >=30 one-open trades;
- >=10 trade weekdays;
- observed hit rate > mean stress break-even;
- primary expectancy >0;
- stress expectancy >0;
- primary PF >=1.10;
- stress PF >=1.00;
- max DD <=USD100;
- integrity/provenance pass.

Protected:

- Jul-Aug secondary outcomes: unopened;
- Sep final holdout: unopened.

Files:

- `strategies/engine-k-direct-target-move-scanner/SPEC-v0.3.md`;
- `research/experiments/EXP-024-engine-k-v0.3-market-aware-stress-ev.md`;
- `research/code/run_engine_k_v0_3_june_gate.py`;
- `.github/workflows/exp024-engine-k-v0.3-june-gate.yml`.

**Next:** trigger June gate only.


### EXP-024 v0.3 June outcome — FAIL

Durable result/model commit:

`db53f3a96fbbb6ed7b1b01f25e931e4140bec215`

June:

- 39 trades;
- 19 distinct trade weekdays;
- hit rate 38.46%;
- mean stress break-even 46.79%;
- primary expectancy -USD0.22/trade;
- stress expectancy -USD3.89/trade;
- primary PF 0.983;
- stress PF 0.742;
- MDD USD212.34;
- calibrated June AUC T30/T40/T50 ~0.672/0.708/0.740.

Trade density passed; economics failed.

Jul-Aug and Sep remain sealed.

Current methodological conclusion: the scanner has broad economic coverage and measurable rank signal, but manual threshold/calibration versions are not converting it into reliable positive expectancy. Next work should use bounded chronological model/configuration selection on Mar-Jun development only, then freeze one configuration before opening Jul-Aug.


## Engine K v0.4 / EXP-025 authoritative current state

Engine K v0.3 / EXP-024 is closed before secondary testing.

EXP-025 is now the active path.

Frozen before EXP-025 metrics:

- Mar-Jun = reusable development pool;
- Jul-Aug secondary = unopened;
- Sep final holdout = unopened;
- 12 configurations exactly;
- 6 chronological expanding walk-forward folds;
- unchanged targets/stops/features/sizing/cost/risk architecture;
- bounded model/calibration/qualification search only;
- stability-first pass and winner criteria;
- no July-Aug access unless one configuration passes.

Read:

- `strategies/engine-k-direct-target-move-scanner/SPEC-v0.4.md`;
- `research/experiments/EXP-025-engine-k-v0.4-walk-forward-selection.md`;
- `research/code/run_engine_k_v0_4_walkforward_selection.py`;
- `.github/workflows/exp025-engine-k-v0.4-walkforward.yml`.

**Next:** trigger EXP-025 development-only walk-forward selection. If none of the 12 configurations passes, stop Engine K tuning on this development pool.


### EXP-025 v0.4 walk-forward outcome — NO PASS

Durable result commit:

`24ce35448cb93158aadeb843dce928199c0c5385`

Result:

- 12 frozen configurations evaluated;
- 6 chronological forward folds;
- passing configs: 0;
- selected winner: NONE;
- Jul-Aug secondary loaded/labeled: NO;
- Sep final holdout loaded/labeled: NO.

Representative near-misses:

- M1-C1-Q3: 75 trades, primary +USD2.15/trade, stress -USD1.67/trade, primary/stress PF 1.185/0.879, stress MDD USD301.54;
- M2-C2-Q3: 124 trades, primary +USD0.86/trade, stress -USD2.62/trade, primary/stress PF 1.079/0.799, stress MDD USD505.51.

Frozen conclusion:

Engine K tuning on the Mar-Jun development pool is closed. Do not add configurations, weaken gates, pick a near-miss, or open Jul-Aug.

Next research must broaden evidence or use a genuinely different prediction/target design.


## Engine L v0.1 / EXP-026 authoritative current state

Engine K tuning on Mar-Jun is closed after EXP-025 no-pass walk-forward.

The current active path is a materially different entry architecture.

Engine L flow:

`5m forecast -> arm -> favorable pullback -> M1 resumption -> next-open entry -> fresh execution stop`.

Frozen center config:

- fixed M2 raw T40 forecast;
- 15 active-M1 arm;
- 0.20*V5 pullback;
- M1 break/resumption + outer-quartile close;
- fresh pullback-extreme stop;
- Gold target 4 XAU;
- non-Gold 2R target-before-size;
- same risk/notional/margin/cost framework;
- matched immediate-entry control.

Current outcome status:

- Engine-L target/P&L outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.

**Next:** run zero-outcome EXP-026 mechanics preflight. Do not run development unless every market has >=100 admissible trigger paths and both directions.


### Engine L mechanics preflight PASS + MTF guidance

Durable preflight result:

`b19d4ef6c3a689117fc5b8237167322bd64a2aa7`

- 12,532 admissible Engine-L entry paths;
- all 8 markets >=100;
- both directions on every market;
- Engine-L target/P&L outcomes at checkpoint: NO;
- Jul-Aug: unopened;
- Sep: unopened.

Also read:

`research/notes/MULTI-TIMEFRAME-INTRADAY-GUIDANCE.md`

Guidance only:

`4H/1H context -> 15m setup/location -> 5m arm -> 1m execution`.

Do not silently add MTF gates to Engine L v0.1. First run the frozen Engine-L development experiment versus its matched immediate-entry control.


### Engine L development launch checkpoint

EXP-026 mechanics preflight passed and the exact development runner/workflow are frozen.

Development compares, on identical forecast arms:

- Engine L: pullback -> M1 resumption -> next-open -> fresh stop;
- Control: immediate next-open -> old 5m pivot stop.

Six chronological forward folds; fixed M2 T40 model; no threshold grid.

At launch checkpoint:

- development outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.

**Next:** trigger EXP-026 development and apply the frozen gate.


### EXP-026 Engine L development outcome — FAIL

Durable result:

`7cacd739f80ab37a2f6465924937bd6489b1b966`

Engine L pooled:

- 303 trades;
- hit 26.40%;
- primary expectancy -USD5.82/trade;
- stress expectancy -USD9.77/trade;
- PF 0.628 / 0.469;
- stress MDD USD3,141.88;
- positive stress folds 0/6.

Matched immediate control:

- stress expectancy -USD8.49/trade.

Engine L underperformed by ~USD1.28/trade.

Critical lesson:

- pullback occurred;
- M1 resumption confirmation occurred;
- but next-open entry was median ~0.516 V5 worse than original decision close;
- confirmation became chase.

Do not add a probability threshold or tune v0.1.

Jul-Aug and Sep remain unopened.

Next prospective architecture should use:

`4H/1H context -> 15m setup/location -> 5m tactical decision -> lower-timeframe entry`

with an entry design that preserves favorable price rather than waiting for a completed breakout.


## Engine M v0.1 / EXP-027 authoritative current state

Engine L v0.1 / EXP-026 is closed. Its decisive lesson: waiting for M1 breakout/resumption then entering next-open chased price and worsened stress expectancy.

Current active family:

**Engine M v0.1 — Multi-Timeframe Reclaim Limit Entry**

Frozen flow:

`H4/H1 direction -> M15 H1-midpoint reclaim -> M5 rejection arm -> 50% M5 retracement limit -> M5 structural stop -> T40 economics`.

Important:

- no ML probability model;
- entry is precomputed before future M1 path;
- no trade if retracement never fills;
- one pending order per symbol;
- matched immediate-entry control reserved for development;
- Mar-Jun reusable;
- Jul-Aug unopened;
- Sep unopened.

Current outcome state:

- Engine-M target/P&L outcomes: NO;
- matched-control outcomes: NO.

**Next:** trigger EXP-027 zero-outcome mechanics preflight. Development is forbidden unless every market has >=50 admissible filled paths, both directions, and >=600 total.


## Engine M v0.2 / EXP-028 authoritative current state

EXP-027 v0.1 is closed before outcomes.

Audited v0.1 preflight:

- 1,581 mechanical MTF retracement-limit fills;
- 126 old USD40-equivalent admissions;
- FX rejects mostly notional+margin;
- target/P&L outcomes: NO;
- Jul-Aug/Sep: unopened.

Conclusion: the preflight conflated signal validity with whether the USD500 reference account could size each trade to ~USD40 gross.

EXP-028 / v0.2 fixes research ordering without changing trade mechanics:

`signal validity first -> separate safe-lot/account utility overlay`.

Frozen safety overlay:

- stop risk <=USD20;
- notional <=USD50k;
- margin <=USD100 at 1:500;
- 0.01 lot step;
- Gold <=0.10 lot.

Utility bands:

- GE40;
- GE30;
- LT30.

**Next:** run zero-outcome EXP-028 preflight. Require >=50 filled valid signals per market, both directions, >=600 total, and no safety-cap violation.


### EXP-028 zero-outcome preflight PASS

Durable result:

`68e52188de8abb2c708cacb611e347afb22a086d`

- 1,581 filled valid signals;
- all eight markets >=50;
- both directions every market;
- all 1,581 safe-lot deployable;
- GE40 66 / GE30 160 / LT30 1,355;
- target/P&L outcomes: NO;
- Jul-Aug/Sep: unopened.

**Next:** Engine M v0.2 development: report normalized-R signal edge separately from safe-lot USD500 portfolio economics.


### EXP-028 development launch checkpoint

v0.2 zero-outcome preflight passed.

Development runner/workflow are frozen.

It will report separately:

- all-signal normalized-R edge;
- safe-lot USD500 one-open portfolio;
- matched immediate-entry control.

At launch:

- target/P&L outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.

**Next:** trigger EXP-028 development and apply the frozen gate.


### EXP-028 Engine M v0.2 development outcome — FAIL

Durable result:

`bd0ae3f18509c8e4e19fbe570766c961b1f4e3fb`

Signal layer:

- 1,249 signals;
- hit 35.07%;
- gross +0.0367R;
- primary -0.1625R;
- stress -0.3616R;
- 0/6 positive-stress folds.

Immediate control:

- gross -0.0146R;
- primary -0.2032R;
- stress -0.3918R.

Safe-lot USD500 portfolio:

- 593 trades / 57 weekdays;
- primary -USD1.69/trade;
- stress -USD3.42/trade;
- PF 0.756 / 0.575;
- stress MDD USD2,065.82;
- 1 day >=USD100;
- 0 days >=USD150.

Conclusion:

The non-chasing MTF limit entry improved raw edge but the current setup/context is not selective enough to overcome costs.

Do not open Jul-Aug or Sep. Do not weaken costs. Any next version must materially improve pre-cost selectivity.


## Engine M v0.3 / EXP-029 authoritative current state

Engine M v0.2 / EXP-028 is closed before secondary testing.

Key v0.2 lesson:

- non-chasing MTF limit entry improved gross edge to +0.0367R versus -0.0146R immediate control;
- edge remained too small for frozen costs;
- Jul-Aug and Sep remain unopened.

Current frozen version:

**Engine M v0.3 — Liquidity Reclaim + HTF Target-Room Limit Entry**

Flow:

`H4/H1 direction -> strict prior-4-M15 liquidity sweep/reclaim -> H1 midpoint reclaim -> unchanged M5 arm -> unchanged 50% retracement limit`.

Additional requirement:

T40 must lie no farther than a recent completed H1 directional liquidity extreme from the latest two H1 bars.

No ML model. No parameter grid. Execution/cost/sizing mechanics unchanged.

Outcome state:

- v0.3 target/P&L outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.

**Next:** trigger EXP-029 zero-outcome preflight. Require >=35 signals per market, both directions, >=400 total.


## Engine M v0.4 / EXP-030 authoritative current state

EXP-029 / v0.3 is closed before outcomes:

- 106 filled signals;
- frequency gate failed;
- target/P&L outcomes NO;
- Jul-Aug/Sep unopened.

Current version:

**Engine M v0.4 — Prior-H1 Range Sweep/Reclaim Limit Entry**

Flow:

`H4/H1 direction -> M15 sweep/reclaim latest completed H1 boundary -> unchanged M5 arm -> unchanged 50% retracement limit`.

Target-room:

- LONG target <= H1_0.high;
- SHORT target >= H1_0.low.

Outcome state:

- v0.4 outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.

**Next:** trigger EXP-030 zero-outcome preflight. Require >=25 signals per market, both directions, >=300 total.


## Engine M v0.5 / EXP-031 authoritative current state

EXP-030 / v0.4 closed before outcomes:

- 237 filled valid signals;
- 7/8 markets passed per-market frequency;
- total >=300 failed;
- GBPUSD 19 <25;
- target/P&L outcomes NO;
- Jul-Aug/Sep unopened.

Current frozen version:

**Engine M v0.5 — Recent-H1 Range Sweep/Reclaim Limit Entry**

At each M15 decision:

- try H1_0 first;
- if H1_0 fails, try H1_1;
- first qualifying range only;
- same selected range supplies sweep boundary + opposite target-room boundary.

Execution and economics remain unchanged.

**Next:** trigger EXP-031 zero-outcome preflight with the same >=25-per-market / >=300-total gate.


### EXP-031 zero-outcome preflight PASS

Durable result: `e0c7566`.

- 417 filled valid signals;
- all 8 markets pass >=25 and both directions;
- all 417 safely deployable;
- GE40 16 / GE30 35 / LT30 366;
- target/P&L outcomes: NO;
- Jul-Aug/Sep: unopened.

**Next:** EXP-031 six-slice development. Report H1_0 and H1_1 outcome cohorts separately without post-outcome tuning.


### EXP-031 development launch checkpoint

v0.5 zero-outcome preflight passed.

Development runner/workflow are frozen:

- six fixed slices;
- normalized-R signal layer;
- H1_0/H1_1 cohort diagnostics;
- safe-lot USD500 portfolio;
- >+0.20R pooled gross hurdle;
- all post-cost gates unchanged.

At launch:

- target/P&L outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.

**Next:** trigger EXP-031 development and stop before secondary on any failed mandatory gate.


## Engine M family final outcome

Engine M is CLOSED after v0.5 / EXP-031 development failure at `d10e0e9`.

v0.5:

- 329 signals;
- gross -0.0099R;
- primary -0.2063R;
- stress -0.4027R;
- 0/6 positive-stress folds;
- safe-account primary/stress -USD1.29 / -USD3.05 per trade;
- stress MDD USD856.89.

H1_0 cohort gross +0.0259R; H1_1 -0.0628R. Do not post-hoc rescue H1_0 or selected symbols.

Family conclusion:

- retain non-chasing execution insight;
- reject H1/midpoint/range sweep-reclaim as sufficient standalone predictor;
- no Engine M v0.6 minor variant.

Jul-Aug and Sep remain unopened.

**Next:** genuinely different prospectively frozen engine family.


## Engine N v0.1 / EXP-032 authoritative current state

Engine M family is closed.

Current prospectively frozen family:

**Engine N v0.1 — Session Opening Drive Pullback Continuation**

Mechanics:

- London anchor 07:00 UTC;
- New York anchor 13:30 UTC;
- first exact 30 minutes = drive;
- prior eight exact M15 bars = volatility baseline;
- drive >=1.50x median baseline range;
- body >=60%;
- close in directional outer 25%;
- enter first 50% pullback;
- stop beyond drive extreme;
- order life 45 active M1 / max anchor+90m;
- unchanged T40 + safe-lot overlay.

Outcome state:

- Engine-N target/P&L outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.

**Next:** trigger EXP-032 zero-outcome preflight. Require >=25 signals per market, both directions, >=300 total.


## Engine N v0.2 / EXP-033 authoritative current state

EXP-032 / Engine N v0.1 closed before outcomes:

- 123 filled signals;
- frequency gate failed;
- both directions everywhere;
- safe overlay passed;
- Jul-Aug/Sep unopened.

Current prospectively frozen version:

**Engine N v0.2 — Rolling Intraday Drive Pullback Scanner**

Every eligible weekday and market scans:

`06:00, 07:00, ..., 17:00 UTC`.

For each anchor:

- 30m drive;
- prior-eight-M15 baseline;
- 1.50x expansion;
- 60% body;
- outer-25% close;
- 50% pullback limit;
- drive-extreme stop;
- 45-M1 / anchor+90m horizon.

Adjacent cycles are non-overlapping.

Outcome state:

- target/P&L outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.

**Next:** trigger EXP-033 zero-outcome preflight with unchanged >=25-per-market / >=300-total gate.


### EXP-033 zero-outcome preflight PASS

Durable result: `2b8c781`.

- 626 filled valid signals;
- all 8 markets pass >=25 and both directions;
- 624 safely deployable;
- GE40 32 / GE30 474 / LT30 118;
- target/P&L outcomes: NO;
- Jul-Aug/Sep: unopened.

**Next:** EXP-033 six-slice development. Report hourly-anchor cohorts diagnostically without post-outcome hour selection.


### EXP-033 development launch checkpoint

Engine N v0.2 zero-outcome preflight passed:

- 626 filled valid signals;
- all eight markets passed >=25 and both directions;
- 624 safely deployable;
- GE40 32 / GE30 474 / LT30 118.

Development runner/workflow are frozen:

- six fixed slices;
- normalized-R signal edge;
- safe-lot USD500 one-open portfolio;
- hourly-anchor diagnostics only;
- matched immediate control = first active M1 open after each qualified 30m drive;
- T40 vs frozen stop;
- same-bar stop first;
- max 120 active M1 bars;
- 20:00 UTC cutoff;
- >+0.20R gross hurdle and all post-cost gates unchanged.

At launch:

- target/P&L outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.

**Next:** trigger EXP-033 development and stop before secondary on any failed mandatory gate.


## Engine O v0.1 / EXP-034 authoritative current state

Engine N family is CLOSED after EXP-033 development failure:

- 505 signals;
- gross +0.0411R;
- primary -0.1450R;
- stress -0.3312R;
- 1/6 positive-stress folds;
- safe-account primary/stress -USD2.82 / -USD6.07.

Do not post-hoc select positive hours/symbols from EXP-033.

Current prospectively frozen family:

**Engine O v0.1 — Rolling Statistical Stretch Reversion**

Flow:

`15m decision grid -> prior-24-M5 robust center/MAD -> stretched rejection M5 -> 50% limit -> T40 reversion toward center`.

Frozen:

- decisions 06:15-17:45 UTC every 15m;
- stretch >=2.50 MAD;
- trigger range >=1.25x baseline median;
- body >=50%;
- favorable outer-35% close;
- 10-active-M1 / 30m limit life;
- stop beyond trigger;
- T40 must fit before CENTER;
- unchanged safe-lot overlay.

Outcome state:

- Engine-O outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.

Implementation:

- `research/code/engine_o_v0_1.py`;
- `research/code/run_engine_o_v0_1_preflight.py`;
- `.github/workflows/exp034-engine-o-v0.1-preflight.yml`.

**Next:** trigger EXP-034 zero-outcome preflight with unchanged >=25-per-market / >=300-total scanner gate.


## Engine O v0.2 / EXP-035 authoritative current state

EXP-034 / Engine O v0.1 closed before outcomes:

- 209 filled valid signals;
- 209 safely deployable;
- six of eight markets passed >=25 + both directions;
- USDJPY 18;
- AUDUSD 22;
- target/P&L outcomes NO;
- Jul-Aug/Sep unopened.

Current prospectively frozen version:

**Engine O v0.2 — Continuous M5 Statistical Stretch Reversion**

Change from v0.1:

- decision grid only: every completed M5 from 06:05 through 17:55 UTC.

Everything else unchanged:

- prior 24 M5 CENTER/MAD state;
- 2.50 MAD stretch;
- 1.25x range;
- 50% body;
- favorable outer-35% close;
- 50% limit;
- trigger-extreme stop;
- 10-M1 / 30m lifetime;
- T40 before CENTER;
- unchanged safe-lot overlay.

Outcome state:

- v0.2 outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.

**Next:** trigger EXP-035 zero-outcome preflight with unchanged >=25-per-market / >=300-total gate.


### EXP-035 development launch checkpoint

Engine O v0.2 zero-outcome preflight PASS:

- 574 filled valid signals;
- all 8 markets >=25 and both directions;
- all 574 safely deployable;
- GE40 7 / GE30 140 / LT30 427;
- outcomes NO;
- Jul-Aug/Sep unopened.

Development runner/workflow frozen:

- six fixed slices;
- normalized-R signal edge;
- safe-lot USD500 one-open portfolio;
- hour cohorts descriptive only;
- matched immediate control on same non-suppressed qualified arms;
- T40 vs trigger-extreme stop;
- stop first on same bar;
- max 120 active M1;
- 20:00 UTC cutoff;
- >+0.20R gross hurdle and all post-cost gates unchanged.

**Next:** trigger EXP-035 development and stop before secondary on any mandatory failure.


## Engine O family final outcome

Engine O is CLOSED after v0.2 / EXP-035 development failure at `f37a757`.

- 430 signals;
- gross -0.0719R;
- primary -0.2611R;
- stress -0.4504R;
- 0/6 positive-stress folds;
- safe-account primary/stress -USD3.11 / -USD5.38;
- stress MDD about USD1,394.

Immediate-entry control was also negative.

Do not post-hoc select EURJPY or favorable time cohorts.

Jul-Aug and Sep remain unopened.

**Next:** genuinely different cross-market relative-strength / factor-divergence family.


## Engine P v0.1 / EXP-036 authoritative current state

Engine O family is CLOSED after EXP-035 development failure.

Current prospectively frozen family:

**Engine P v0.1 — Cross-Market Relative-Strength Pullback**

Mechanics:

- decisions every completed M5 from 06:05-17:55 UTC;
- own 30m MOM normalized by prior-24-M5 median range;
- |own MOM| >=1.50;
- USD_SCORE from other USD-linked FX majors, self-excluded, threshold 0.50;
- EURJPY requires EURUSD and USDJPY leg agreement;
- >=35% trigger body;
- favorable outer-40% close;
- 50% non-chasing limit;
- trigger-extreme stop;
- 10-M1 / 30m order life;
- unchanged T40 + safe-lot overlay.

Outcome state:

- Engine-P outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.

Implementation:

- `research/code/engine_p_v0_1.py`;
- `research/code/run_engine_p_v0_1_preflight.py`;
- `.github/workflows/exp036-engine-p-v0.1-preflight.yml`.

**Next:** trigger EXP-036 zero-outcome preflight with unchanged >=25-per-market / >=300-total gate.


### EXP-036 development launch checkpoint

Engine P v0.1 zero-outcome preflight PASS:

- 6,063 filled valid signals;
- all 8 markets >=25 and both directions;
- 6,059 safely deployable;
- GE40 105 / GE30 1,253 / LT30 4,701;
- outcomes NO;
- Jul-Aug/Sep unopened.

Development runner/workflow frozen:

- six fixed slices;
- normalized-R signal edge;
- safe-lot USD500 one-open portfolio;
- own-MOM / USD_SCORE / EURJPY-leg / time diagnostics descriptive only;
- matched immediate control on same non-suppressed qualified arms;
- T40 vs trigger structural stop;
- stop first on same bar;
- max 120 active M1;
- 20:00 UTC cutoff;
- >+0.20R gross hurdle and all post-cost gates unchanged.

**Next:** trigger EXP-036 development and stop before secondary on any mandatory failure.


## Engine P / EXP-036 authoritative final outcome

Engine P v0.1 is **CLOSED** after failing frozen development at durable result `52e9003f351eb7f5abdf9b38f74c279c88d33906`.

Verified from `research/results/EXP-036-development-summary-v0.1.json`:

- 4,804 development signals;
- gross normalized expectancy -0.0406469R;
- primary -0.2356814R;
- stress -0.4307159R;
- 0/6 positive-stress folds;
- 836 reference-account trades;
- primary/stress expectancy -USD2.0238 / -USD4.1458;
- primary/stress PF 0.7611 / 0.5800;
- stress MDD USD3,526.25;
- final disposition `FAIL_STOP_BEFORE_SECONDARY`.

Protected periods were not loaded/labeled:

- Jul-Aug secondary: NO;
- Sep final holdout: NO.

Do not create Engine P v0.2 as a threshold/hour/symbol/direction rescue. The next engine must be prospectively frozen from a genuinely different information source/family.


## Engine Q v0.1 / EXP-037 authoritative current state

Engine P is closed. The current primary path is prospectively frozen **Engine Q v0.1 — Cross-Market Volatility Spillover Breakout**.

Different information source:

- peer **volatility breadth**, not peer directional consensus;
- candidate must still be locally lagging/compressed;
- trade direction is determined only by the candidate's first later local breakout.

Frozen center mechanics:

- decisions 06:05-17:25 UTC;
- peer VR from current M5 range / prior-24-M5 median range;
- candidate excluded;
- >=4 shocked peers at VR>=1.75, >=6 valid peers;
- candidate VR<=1.00 and inside fixed prior-six-M5 box;
- next-six-M5 arm;
- first breakout VR>=1.25, body>=50%, outer-25% close;
- 50% retracement limit, stop beyond breakout extreme;
- 10-M1/30m order life;
- T40;
- primary/stress costs =10%/20% gross target;
- unchanged USD500 safe-lot overlay.

Source/split is frozen in `research/provenance/EXP-037-engine-q-v0.1-source-manifest.md`. Jun30 is a hard source seal; Jul-Aug and Sep remain sealed.

Outcome state: **zero Engine-Q target/P&L outcomes**.

**Exact next action:** implement and run EXP-037 zero-outcome preflight only. Development is forbidden until that durable preflight passes the unchanged >=25-per-market / both-directions / >=300-total gate.


### EXP-037 implementation checkpoint

Engine Q v0.1 implementation is frozen before outcomes:

- main SHA: `c51c8f9566a6ccfddaf8117c2b0a80c45fbeb10b`;
- engine commit: `9a2a2c7`;
- preflight runner: `2bfb0c5`;
- workflow: `c51c8f9`;
- target/P&L outcomes: NO;
- Jul-Aug/Sep: sealed.

**Exact next action:** trigger exactly one EXP-037 zero-outcome preflight, confirm it starts once, then do not poll repeatedly.


## Engine Q v0.1 / EXP-037 final state

Engine Q v0.1 is CLOSED at zero-outcome preflight `b05efb3`.

- 56 fills total;
- all 56 safely deployable;
- all markets failed >=25 + both-directions;
- total >=300 failed;
- target/P&L outcomes zero;
- Jul-Aug/Sep sealed.

The dominant bottleneck was simultaneous same-M5 four-peer VR>=1.75 shock breadth. Do not lower the opportunity gate. A subsequent version may alter peer-shock temporal sampling only if frozen before new results.


## Engine Q v0.2 / EXP-038 authoritative current state

Current path: **Engine Q v0.2 — Rolling Cross-Market Volatility Spillover**.

The change from v0.1 is only temporal peer-shock memory:

- same VR>=1.75 shock threshold;
- same >=4 unique peers;
- peer may qualify at current M5, 5 minutes ago or 10 minutes ago;
- candidate excluded and each peer counted once.

Candidate lag, six-M5 breakout arm, breakout confirmation, 50% limit, stop, T40, costs, account caps and gates are unchanged.

No v0.2 outcomes exist. Jul-Aug and Sep remain sealed.

**Exact next action:** implement and run EXP-038 zero-outcome preflight only.


### EXP-038 implementation checkpoint

Engine Q v0.2 is implemented and frozen before outcomes at main SHA `850fe44fa426b2ee4f235d3af140fa981ff26ae2`.

- target/P&L outcomes: NO;
- Jul-Aug/Sep: sealed.

**Exact next action:** trigger exactly one EXP-038 zero-outcome preflight, confirm it starts once, then follow the long-running pipeline policy.
