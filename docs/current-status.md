# Current Status

**Date:** 2026-09-23  
**Phase:** Phase 2 — Engine K v0.1 failed training/June-calibration gate; July-August and September preserved; prospective scanner revision required

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

## Engine K v0.1 / EXP-022 outcome

**Engine K v0.1 failed the frozen training + June calibration gate and is stopped before secondary testing.**

Durable result:

- workflow run: `35901103493`;
- tested SHA: `69a95393f0072d4a4a84668f0a300eb97cf49336`;
- result/model commit: `d24e05ca513777d63a5d0f6762dfdb35bc42cfc3`.

Key result:

- 7,098 economically admissible labeled rungs;
- all 7,098 were XAUUSD;
- each of the seven FX execution markets produced zero executable rungs under v0.1 economics;
- June HGB raw ROC-AUC was roughly 0.62-0.63;
- June Platt-calibrated maximum probabilities were about 0.499 / 0.420 / 0.347 for T30/T40/T50;
- zero candidates passed the frozen v0.1 probability gate;
- zero simulated trades;
- causality/provenance integrity passed.

**Protection:** July-August secondary-test and Sep-1 through Sep-22 final-holdout outcomes remain unopened.

Do not reopen v0.1 by lowering its threshold or tuning the inspected XAU model.

## Engine K v0.2 / EXP-023 outcome

**Engine K v0.2 is CLOSED before secondary testing.**

Durable result/model commit:

`763aefadbe56ee7012b475dcb677f6f78d8036ec`

Training/calibration facts:

- 281,955 labeled rungs across all 8 execution markets;
- T30 June AUC about 0.674;
- T40 June AUC about 0.710;
- T50 June AUC about 0.743;
- only 2 qualified combined trades;
- 0 qualified June trades;
- frozen >=100 combined / >=20 June frequency gates failed;
- June expectancy/PF/hit-rate gates unavailable/failed;
- June DD gate passed;
- causality/provenance passed.

July-August secondary-test and Sep final-holdout outcomes remain unopened.

Interpretation: the v0.2 target/economic redesign solved market admission, but the fixed `max(0.50, break-even+0.10)` qualification rule did not yield a testable trading stream. Do not lower that threshold inside v0.2.



## Engine K v0.4 / EXP-025 — CURRENT PRIMARY PATH

This section supersedes older Engine-K “next action” text above.

Engine K v0.3 / EXP-024 is closed before secondary testing. Durable failure result: `db53f3a96fbbb6ed7b1b01f25e931e4140bec215`.

Engine K v0.4 / EXP-025 is prospectively frozen **before walk-forward metrics**.

Methodology:

- Mar-Jun 2026 is reusable development evidence;
- Jul-Aug secondary test remains sealed;
- Sep final holdout remains sealed;
- exact bounded search = 12 configurations only;
- 2 HGB variants x 2 Platt calibration variants x 3 stress-EV qualification policies;
- exact six expanding chronological walk-forward folds;
- targets, structural stop, features, sizing, costs, risk/notional/margin gates and daily state machine are unchanged.

Configuration pass requires all frozen multi-fold trade-count, expectancy, PF, drawdown, hit-rate, market-concentration and integrity conditions.

If no configuration passes, Engine K tuning on this Mar-Jun pool stops before July-Aug.

If one or more pass, choose exactly one by frozen stability-first ordering:

1. highest worst-fold stress expectancy;
2. highest pooled stress PF;
3. lowest pooled stress max drawdown;
4. highest trade count;
5. configuration ID.

Files:

- `strategies/engine-k-direct-target-move-scanner/SPEC-v0.4.md`;
- `research/experiments/EXP-025-engine-k-v0.4-walk-forward-selection.md`;
- `research/code/run_engine_k_v0_4_walkforward_selection.py`;
- `.github/workflows/exp025-engine-k-v0.4-walkforward.yml`.

### Exact next action

Run EXP-025 bounded walk-forward development selection only.

Do not create or run a July-Aug secondary-test workflow unless EXP-025 durably selects a passing winner.


## Engine K v0.4 / EXP-025 outcome

**Engine K v0.4 is CLOSED before secondary testing.**

Durable result commit:

`24ce35448cb93158aadeb843dce928199c0c5385`

Walk-forward result:

- exact 12 frozen configurations evaluated;
- exact 6 frozen chronological folds evaluated;
- development labeled through Jun30 only;
- passing configurations: **0**;
- selected configuration: **NONE**;
- Jul-Aug secondary test: unopened;
- Sep final holdout: unopened.

Best-looking development near-misses were still not robust:

- M1-C1-Q3: +USD2.15/trade primary but -USD1.67/trade stress, PF 1.185/0.879, stress MDD USD301.54, only 75 trades and only 1 positive-stress fold;
- M2-C2-Q3: +USD0.86/trade primary but -USD2.62/trade stress, PF 1.079/0.799, stress MDD USD505.51, 124 trades but 0 positive-stress folds.

The frozen hard-stop rule applies: **stop Engine K tuning on this Mar-Jun pool and do not open Jul-Aug**.

Current blocker has changed from candidate scarcity to economic robustness. The scanner repeatedly shows rank discrimination, but no tested configuration converts that signal into stable stress-cost-adjusted expectancy.

### Exact next research direction

Do not create Engine K v0.5 by adding thresholds/configurations to this search.

The next work must broaden either:

1. **evidence** — materially longer and more diverse historical data / additional properly specified executable asset classes; or
2. **prediction design** — a genuinely different target/outcome formulation rather than another qualification threshold.

Protected Jul-Aug and Sep data remain available for a future prospectively frozen system that earns access.


## Engine L v0.1 / EXP-026 — CURRENT PRIMARY PATH

This section supersedes older “next research direction” text.

Engine K tuning on the Mar-Jun pool is closed after EXP-025 produced zero passing walk-forward configurations.

The current hypothesis is now **entry architecture**, not more threshold tuning or longer-history expansion.

Concrete defect identified in Engine K:

- a completed 5m forecast was converted almost directly into a next-active-M1-open market entry;
- there was no favorable pullback requirement;
- no M1 resumption confirmation;
- the trade stop reused an older 5m pivot rather than fresh execution structure.

Engine L changes the architecture to:

`5m forecast -> arm direction -> wait for 0.20*V5 pullback -> require causal M1 resumption -> enter next M1 open -> fresh pullback-extreme stop -> T40 economics`.

Frozen Engine-L v0.1:

- 8 execution markets;
- fixed M2 raw T40 forecast model;
- no probability threshold;
- 15 active-M1 arm life;
- one pending arm per symbol;
- required 0.20*V5 favorable pullback;
- M1 break/resumption with outer-quartile close;
- fresh M1 pullback-extreme stop;
- Gold T40 = 4 XAU;
- non-Gold T40 = 2R;
- same USD20 risk / notional / margin / cost framework;
- matched immediate-entry control on the same forecast arms;
- six chronological development folds;
- Jul-Aug and Sep remain sealed.

### Immediate next action

Run EXP-026 **zero-outcome entry-mechanics preflight only**.

Before any Engine-L P&L outcome, every market must produce >=100 mechanically triggerable and economically admissible T40 entry paths through Jun30, with both long and short represented.

Files:

- `strategies/engine-l-forecast-armed-micro-entry/SPEC-v0.1.md`;
- `research/experiments/EXP-026-engine-l-forecast-armed-micro-entry-v0.1.md`;
- `research/code/engine_l_v0_1.py`;
- `research/code/run_engine_l_v0_1_preflight.py`;
- `.github/workflows/exp026-engine-l-v0.1-preflight.yml`.


### Engine L zero-outcome preflight result

EXP-026 mechanics preflight passed at durable result commit:

`b19d4ef6c3a689117fc5b8237167322bd64a2aa7`

- 12,532 admissible micro-entry paths through Jun30;
- all 8 markets passed >=100-path gate;
- long + short represented on every market;
- target/P&L outcomes still zero at checkpoint;
- Jul-Aug and Sep remain sealed.

Engine-L v0.1 is therefore mechanically viable for development.

Separately, `research/notes/MULTI-TIMEFRAME-INTRADAY-GUIDANCE.md` records the user-provided top-down guidance:

`4H/1H context -> 15m setup/location -> 5m arm -> 1m execution`.

This is design guidance, not a silent modification of v0.1. Engine-L v0.1 should first isolate whether improved execution alone beats the matched immediate-entry control.


### Engine L development runner checkpoint

EXP-026 development code/workflow are frozen before outcomes.

The development test uses:

- fixed M2 raw T40 forecast;
- same matched forecastable T40 domain as the old immediate-entry control;
- one pending arm per symbol;
- Engine-L 0.20*V5 pullback + M1 resumption + fresh stop;
- matched immediate next-open/old-pivot control;
- exact six forward folds;
- independent one-open portfolio simulations;
- frozen daily risk state;
- Jul-Aug and Sep sealed.

**Exact next action:** run EXP-026 development. Do not open secondary evidence on a failed gate.


## Engine L v0.1 / EXP-026 outcome

**Engine L v0.1 is CLOSED before secondary testing.**

Durable result commit:

`7cacd739f80ab37a2f6465924937bd6489b1b966`

Pooled six-fold development:

- 303 trades / 57 trade weekdays;
- hit rate 26.40% vs stress break-even 46.42%;
- primary expectancy -USD5.82/trade;
- stress expectancy -USD9.77/trade;
- primary/stress PF 0.628 / 0.469;
- stress MDD USD3,141.88;
- positive stress folds 0/6.

Matched immediate-entry control:

- stress expectancy -USD8.49/trade.

Engine L therefore **lost about USD1.28/trade more under stress cost** than the immediate-entry control.

The important execution diagnostic is that the median Engine-L entry was about **0.516 recent-5m-median-range worse than the original decision close** after waiting for the pullback/resumption sequence. The frozen confirmation rule improved hit rate but chased price and did not improve economics.

Simple forecast-score thresholding is also not supported: the highest raw-score quartile remained strongly negative.

Jul-Aug and Sep remain unopened.

### Current next research direction

Do not tune Engine L v0.1 or add a probability threshold.

The next prospectively frozen architecture should implement the user-supplied multi-timeframe hierarchy as an actual causal trading design:

`4H/1H context -> 15m setup/location -> 5m tactical decision -> lower-timeframe execution`.

The lower-timeframe entry should be designed to **preserve favorable pullback price**, not wait for a full breakout/resumption that creates a chase entry.


## Engine M v0.1 / EXP-027 — CURRENT PRIMARY PATH

Engine L v0.1 / EXP-026 is closed after development failure. Its main lesson was that pullback + breakout/resumption + next-open confirmation **chased price**: the median executed entry was about 0.516 V5 worse than the original decision close.

The active path is now Engine M v0.1, a genuinely different **rule-based multi-timeframe location + non-chasing limit-entry engine**.

Architecture:

`4H / 1H context -> 15m setup/location -> 5m tactical arm -> M1 retracement limit entry`.

Frozen v0.1 center mechanics:

- H4 and H1 must agree by completed-bar close direction;
- completed M15 must interact with and reclaim the latest completed H1 midpoint;
- the final completed M5 bar must reject in context direction and close in its outer quartile;
- no immediate market entry;
- precomputed entry = 50% of the completed M5 arm range;
- stop = beyond the M5 arm extreme by one research tick;
- limit lives 10 active M1 bars and no later than 18:00 UTC;
- T40 only;
- same USD20 stop-risk / notional / margin / cost framework;
- no ML probability model;
- matched immediate-entry control will later use the same MTF arms and same M5 stop.

### Immediate next action

Run EXP-027 **zero-outcome MTF/limit mechanics preflight only**.

Frozen preflight gates:

- exact causal multi-timeframe construction tests pass;
- every execution market has >=50 mechanically filled + economically admissible limit paths;
- LONG and SHORT represented on every market;
- >=600 total admissible paths;
- no target/P&L outcomes;
- Jul-Aug and Sep remain unloaded.

Files:

- `strategies/engine-m-mtf-reclaim-limit-entry/SPEC-v0.1.md`;
- `research/experiments/EXP-027-engine-m-mtf-reclaim-limit-entry-v0.1.md`;
- `research/code/engine_m_v0_1.py`;
- `research/code/run_engine_m_v0_1_preflight.py`;
- `.github/workflows/exp027-engine-m-v0.1-preflight.yml`.


### EXP-027 preflight attempt 1 infrastructure note

Run `35995612463` failed before the real preflight because of a synthetic-test pandas dtype mutation. No market preflight, target outcome, P&L outcome or protected-period inspection occurred.

The test fixture was corrected at `569cc707571f063fb5b9b939cfba08555273086a` with **no Engine-M rule change**.

**Next remains:** rerun the identical zero-outcome EXP-027 preflight.


### EXP-027 preflight attempt 2 research result

The complete Engine-M zero-outcome preflight ran and failed its frozen frequency/economic-admission gate.

Durable checkpoint: `89279ad`.

- mechanical limit fills: 1,581;
- economically admissible T40 paths: 126;
- required: >=600 total and >=50 per market with both directions;
- XAUUSD passed with 61;
- all seven FX markets failed on economic admission;
- no target/P&L outcomes;
- Jul-Aug and Sep remain sealed.

This indicates that the immediate blocker is **post-fill economic feasibility**, not a shortage of MTF setups or retracement fills.

**Next:** zero-outcome rejection audit of lot/risk/notional/margin gates. Do not alter MTF entry mechanics yet.


## Engine M v0.2 / EXP-028 — CURRENT PRIMARY PATH

EXP-027 / Engine M v0.1 is closed before outcomes because its preflight incorrectly used USD40-equivalent deployment feasibility as a prerequisite for strategy-signal validity.

Audited EXP-027 result:

- 1,581 mechanical MTF limit fills;
- 126 old-style economically admitted paths;
- FX rejections overwhelmingly caused by the USD50k-notional / USD100-margin envelope, not by excessive stop risk;
- target/P&L outcomes remained zero;
- Jul-Aug / Sep remain unopened.

Engine M v0.2 keeps **all trading mechanics unchanged** and restores the intended research order:

`signal validity -> safe sizing/deployability -> portfolio economics`.

### v0.2 zero-outcome preflight

Every mechanically filled valid signal is retained for signal-layer research.

Separately calculate the largest safe lot under the unchanged:

- stop risk <=USD20;
- notional <=USD50k;
- margin <=USD100 at 1:500;
- 0.01 lot step;
- XAUUSD capped at 0.10 lot.

Report utility:

- GE40;
- GE30;
- LT30.

Mandatory preflight:

- >=50 filled valid signals per market;
- both directions per market;
- >=600 total;
- safe overlay never violates frozen safety caps;
- no target/P&L outcomes;
- Jul-Aug/Sep sealed.

Files:

- `strategies/engine-m-mtf-reclaim-limit-entry/SPEC-v0.2.md`;
- `research/experiments/EXP-028-engine-m-v0.2-signal-first-validation.md`;
- `research/code/engine_m_v0_2.py`;
- `research/code/run_engine_m_v0_2_preflight.py`;
- `.github/workflows/exp028-engine-m-v0.2-preflight.yml`.

**Exact next action:** run EXP-028 zero-outcome preflight only.


### EXP-028 zero-outcome preflight PASS

Durable checkpoint:

`68e52188de8abb2c708cacb611e347afb22a086d`

- 1,581 filled valid MTF/limit signals;
- all eight markets >=50 and both directions;
- all 1,581 safe-lot deployable;
- GE40 66;
- GE30 160;
- LT30 1,355;
- no safety-cap violations;
- no target/P&L outcomes;
- Jul-Aug / Sep sealed.

This confirms the signal-first correction solved the false FX rejection problem.

**Next permitted stage:** EXP-028 six-slice development outcomes: normalized-R signal edge + separate safe-lot USD500 portfolio.


### EXP-028 development launch checkpoint

The Engine-M v0.2 development runner/workflow are frozen before outcomes.

Development will separately evaluate:

1. **signal edge** across every filled valid MTF/limit signal in normalized R;
2. **reference-account economics** using the maximum safe lot under unchanged USD20 risk / USD50k notional / USD100 margin / 0.10 Gold cap.

It also reports the matched immediate-entry control on the same MTF arms.

Six fixed development slices only; Jul-Aug and Sep remain sealed.

**Exact next action:** run EXP-028 development. Do not open secondary evidence on a failed gate.


### EXP-028 development attempt 1 runtime note

Run `35999223397` failed during pooled reporting after verification passed.

Cause: a pandas `Timestamp` was sliced as a string when counting distinct trade weekdays.

No durable development JSON or inspected metrics resulted. Jul-Aug and Sep remain sealed.

Reporting-only fix: `57be12953b917c66b269800cb00889e7f707405b`.

**Next remains:** rerun the identical frozen EXP-028 development logic.


## Engine M v0.2 / EXP-028 outcome

**Engine M v0.2 is CLOSED before secondary testing.**

Durable result commit:

`bd0ae3f18509c8e4e19fbe570766c961b1f4e3fb`

Signal layer:

- 1,249 development signals;
- hit rate 35.07%;
- gross expectancy **+0.0367R**;
- primary expectancy **-0.1625R**;
- stress expectancy **-0.3616R**;
- stress-positive folds: 0/6.

Matched immediate-entry control gross expectancy was -0.0146R, so the MTF limit entry improved raw edge but not enough to survive frozen costs.

Reference USD500 portfolio:

- 593 trades / 57 weekdays;
- primary expectancy -USD1.69/trade;
- stress expectancy -USD3.42/trade;
- primary/stress PF 0.756 / 0.575;
- stress MDD USD2,065.82;
- >=USD100 final-day P&L on 1/57 weekdays;
- >=USD150 on 0/57.

Jul-Aug and Sep remain unopened.

### Current blocker

The problem is now narrower:

**MTF context + non-chasing limit entry creates a small pre-cost edge, but signal selectivity is not strong enough to cover costs.**

Do not weaken cost assumptions or reuse protected periods.

A future engine/version must improve pre-cost signal quality/selectivity while preserving the non-chasing execution insight.


## Engine M v0.3 / EXP-029 — CURRENT PRIMARY PATH

Engine M v0.2 / EXP-028 is closed before secondary testing.

Its key evidence is important:

- the non-chasing MTF limit architecture improved gross normalized expectancy versus immediate entry;
- v0.2 gross expectancy was +0.0367R versus -0.0146R control;
- but primary/stress expectancy remained negative and all six stress folds failed.

Therefore the next version preserves execution and changes **selectivity only**.

### Frozen v0.3 thesis

`H4/H1 directional context -> M15 strict liquidity sweep/reclaim -> H1 midpoint reclaim -> unchanged M5 arm -> unchanged 50% M5 retracement limit -> unchanged structural stop`.

Additional structural destination gate:

- LONG T40 target price must be no farther than the highest high of the latest two completed H1 bars;
- SHORT target price must be no farther than the lowest low of the latest two completed H1 bars.

Purpose:

- replace the broad v0.2 midpoint touch/reclaim with an actual local liquidity event;
- require a concrete recent H1 directional destination at or beyond T40;
- materially raise **pre-cost signal quality** without chasing entry.

Unchanged:

- eight markets;
- T40;
- 50% M5 limit;
- 10-active-M1 order life;
- structural stop;
- signal-first research ordering;
- safe-lot overlay;
- USD20 risk / USD50k notional / USD100 margin caps;
- 0.10 Gold cap;
- frozen cost assumptions.

### EXP-029 zero-outcome preflight gate

Before any v0.3 target/P&L outcome:

- >=35 filled valid signals per market;
- LONG + SHORT on every market;
- >=400 total signals;
- all causality / sweep / target-destination / limit / safety tests pass;
- Jul-Aug and Sep remain unloaded.

**Exact next action:** run EXP-029 zero-outcome preflight only.

Files:

- `strategies/engine-m-mtf-reclaim-limit-entry/SPEC-v0.3.md`;
- `research/experiments/EXP-029-engine-m-v0.3-liquidity-reclaim-target-room.md`;
- `research/code/engine_m_v0_3.py`;
- `research/code/run_engine_m_v0_3_preflight.py`;
- `.github/workflows/exp029-engine-m-v0.3-preflight.yml`.


## Engine M v0.4 / EXP-030 — CURRENT PRIMARY PATH

Engine M v0.3 / EXP-029 is closed before outcomes after its zero-outcome preflight failed frequency:

- 106 filled valid signals total;
- all eight markets below the frozen >=35-per-market gate;
- target/P&L outcomes remained zero;
- Jul-Aug / Sep remained unopened.

Diagnosis:

The recent-H1 target-destination gate was not the main bottleneck. The main frequency collapse came from stacking:

- prior-4-M15 local sweep/reclaim;
- H1 midpoint reclaim;
- M5 arm.

v0.4 therefore does not relax those same rules one threshold at a time. It replaces them with one coherent completed-H1 range object.

Frozen flow:

`H4/H1 direction -> M15 strict sweep/reclaim of latest completed H1 boundary -> unchanged M5 arm -> unchanged 50% M5 retracement limit -> unchanged structural stop`.

Target-room:

- LONG T40 must fit before H1_0.high;
- SHORT T40 must fit before H1_0.low.

Unchanged:

- eight markets;
- non-chasing execution;
- T40;
- 10-active-M1 order life;
- signal-first research ordering;
- safe-lot overlay;
- USD20 risk / USD50k notional / USD100 margin;
- XAUUSD <=0.10 lot;
- frozen costs.

### EXP-030 zero-outcome preflight

Require:

- >=25 filled valid signals per market;
- LONG + SHORT on every market;
- >=300 total;
- all H1 sweep/reclaim / target-room / limit / safety tests pass;
- no target/P&L outcomes;
- Jul-Aug and Sep unloaded.

**Exact next action:** run EXP-030 preflight only.

Files:

- `strategies/engine-m-mtf-reclaim-limit-entry/SPEC-v0.4.md`;
- `research/experiments/EXP-030-engine-m-v0.4-prior-h1-range-reclaim.md`;
- `research/code/engine_m_v0_4.py`;
- `research/code/run_engine_m_v0_4_preflight.py`;
- `.github/workflows/exp030-engine-m-v0.4-preflight.yml`.


## Engine M v0.5 / EXP-031 — CURRENT PRIMARY PATH

Engine M v0.4 / EXP-030 is closed before outcomes after its zero-outcome preflight failed frequency:

- 237 filled valid signals;
- 7/8 markets passed the >=25 + both-directions gate;
- GBPUSD had 19;
- total requirement >=300 was missed;
- target/P&L outcomes remained zero;
- Jul-Aug / Sep remained unopened.

v0.4 materially improved opportunity density versus v0.3, so the H1-range concept is retained.

v0.5 does **not** lower the failed v0.4 preflight gate. Instead it prospectively broadens the same coherent H1-range logic:

- evaluate H1_0 first;
- if H1_0 does not fully qualify, evaluate H1_1;
- first qualifying range supplies both swept boundary and opposite target-room boundary;
- one M15 bar can create at most one arm.

Everything else remains unchanged:

- H4/H1 directional alignment;
- unchanged M5 rejection arm;
- unchanged 50% M5 retracement limit;
- unchanged structural stop;
- unchanged T40;
- signal-first sizing;
- USD20 risk / USD50k notional / USD100 margin;
- XAUUSD <=0.10 lot;
- frozen costs.

### EXP-031 zero-outcome preflight

The frequency gate is intentionally unchanged from v0.4:

- >=25 filled valid signals per market;
- LONG + SHORT on every market;
- >=300 total;
- safe overlay passes;
- no target/P&L outcomes;
- Jul-Aug/Sep sealed.

**Exact next action:** run EXP-031 preflight only.

Files:

- `strategies/engine-m-mtf-reclaim-limit-entry/SPEC-v0.5.md`;
- `research/experiments/EXP-031-engine-m-v0.5-recent-h1-range-reclaim.md`;
- `research/code/engine_m_v0_5.py`;
- `research/code/run_engine_m_v0_5_preflight.py`;
- `.github/workflows/exp031-engine-m-v0.5-preflight.yml`.


### EXP-031 preflight attempt 1 verification note

Run `36009869842` failed before the market preflight because a helper `status="ok"` field overwrote both the qualifying and non-qualifying v0.5 setup statuses.

No market preflight or target/P&L outcome resulted. Jul-Aug and Sep remain sealed.

Implementation-only fixes:

- `5335a440edc0ad3a58995dfa0bb16b08fb91713b`;
- `a50cf398e57fd13fb1ac1e8b26fbe701df1e1cf9`.

**Next remains:** rerun the identical frozen EXP-031 zero-outcome preflight.


### EXP-031 zero-outcome preflight PASS

Durable checkpoint: `e0c7566`.

- 417 filled valid signals;
- all 8 markets >=25 and both directions;
- all 417 safely deployable;
- GE40 16 / GE30 35 / LT30 366;
- zero target/P&L outcomes;
- Jul-Aug and Sep sealed.

The unchanged v0.4 frequency gate was passed without moving the goalposts.

**Next permitted stage:** six-slice EXP-031 development using the already frozen >+0.20R gross-edge and post-cost economic gates.


### EXP-031 development launch checkpoint

Engine M v0.5 passed zero-outcome preflight and its six-slice development runner is now frozen.

Development will test:

1. pooled normalized-R signal edge;
2. H1_0 and H1_1 cohorts separately;
3. safe-lot USD500 one-open portfolio economics.

Mandatory gross-edge hurdle remains **>+0.20R**. Post-cost primary/stress expectancy, PF, drawdown, weekday and concentration gates remain unchanged.

Jul-Aug and Sep remain sealed.

**Exact next action:** run EXP-031 development only.


## Engine M family — CLOSED

Engine M v0.5 / EXP-031 failed development at durable result `d10e0e9`.

Key result:

- 329 signals;
- gross -0.0099R;
- primary -0.2063R;
- stress -0.4027R;
- 0/6 positive-stress folds;
- safe-account primary/stress expectancy -USD1.29 / -USD3.05;
- stress MDD USD856.89;
- no >=USD100 or >=USD150 final-P&L weekdays.

H1_1 fallback added frequency but worsened edge versus H1_0.

### Engine-M family conclusion

The family has been tested sufficiently.

Useful retained insight:

**non-chasing retracement/limit execution is preferable to chase-style confirmation when a setup is otherwise valid.**

Rejected thesis:

**H4/H1 close-direction + H1/midpoint/range sweep-reclaim location is not a strong enough standalone predictor of the required move across the eight-market universe.**

Do not create Engine M v0.6 by another small location/lookback/filter change.

Jul-Aug and Sep remain sealed.

**Next:** open a genuinely different engine family prospectively.


## Engine N v0.1 / EXP-032 — CURRENT PRIMARY PATH

Engine M is closed at the family level after EXP-031 failed development.

Retained lesson:

- non-chasing retracement/limit execution can improve entry quality.

Rejected family thesis:

- H4/H1 close-direction plus midpoint/H1-range sweep-reclaim did not create robust enough predictive edge.

The current path is a genuinely different family:

**Engine N v0.1 — Session Opening Drive Pullback Continuation**

Flow:

`fixed session anchor -> 30m opening displacement -> first 50% pullback -> continuation`.

Frozen sessions:

- London 07:00 UTC;
- New York 13:30 UTC.

Qualification:

- exact 30-minute drive;
- eight preceding exact M15 bars as volatility baseline;
- drive range >=1.50x baseline median;
- body >=60%;
- close in directional outer 25%.

Execution:

- limit at 50% of drive range;
- stop beyond drive extreme by one research tick;
- 45 active-M1 order life;
- maximum anchor+90m;
- unchanged T40 and safe-lot overlay.

No H1 sweep/reclaim.
No ML probability threshold.

### EXP-032 zero-outcome preflight

Require:

- >=25 filled valid signals per market;
- LONG + SHORT on every market;
- >=300 total;
- chronology/qualification/entry/safety tests pass;
- no target/P&L outcomes;
- Jul-Aug and Sep unloaded.

**Exact next action:** run EXP-032 zero-outcome preflight only.

Files:

- `strategies/engine-n-session-opening-drive-pullback/SPEC-v0.1.md`;
- `research/experiments/EXP-032-engine-n-v0.1-session-opening-drive-pullback.md`;
- `research/code/engine_n_v0_1.py`;
- `research/code/run_engine_n_v0_1_preflight.py`;
- `.github/workflows/exp032-engine-n-v0.1-preflight.yml`.


## Engine N v0.2 / EXP-033 — CURRENT PRIMARY PATH

Engine N v0.1 / EXP-032 is closed before outcomes after its zero-outcome preflight failed opportunity density:

- 123 filled valid signals;
- every market below the frozen >=25-per-market gate;
- LONG + SHORT existed on every market;
- safe overlay passed;
- target/P&L outcomes remained zero;
- Jul-Aug / Sep remained unopened.

v0.1's fixed two-session sampling was the bottleneck.

v0.2 keeps the same displacement-pullback thesis and all qualification/entry thresholds, but changes sampling architecture to continuous **non-overlapping hourly intraday scanning**.

Frozen anchors:

`06:00 through 17:00 UTC inclusive` — 12 anchors per market per eligible weekday.

Each anchor:

- exact 30m drive;
- prior-eight-M15 volatility baseline;
- >=1.50x expansion;
- >=60% body;
- directional outer-25% close;
- 50% pullback limit;
- drive-extreme stop;
- 45 active-M1 order life;
- hard horizon anchor+90m.

Adjacent anchor cycles do not overlap: prior horizon equals next anchor decision.

Unchanged:

- eight markets;
- T40;
- signal-first safe-lot overlay;
- USD20 risk / USD50k notional / USD100 margin;
- XAUUSD <=0.10 lot;
- frozen costs.

### EXP-033 zero-outcome preflight

Keep the same gate as v0.1:

- >=25 filled valid signals per market;
- LONG + SHORT every market;
- >=300 total;
- chronology/entry/safety tests pass;
- no target/P&L outcomes;
- Jul-Aug and Sep unloaded.

**Exact next action:** run EXP-033 zero-outcome preflight only.

Files:

- `strategies/engine-n-rolling-drive-pullback/SPEC-v0.2.md`;
- `research/experiments/EXP-033-engine-n-v0.2-rolling-intraday-drive-pullback.md`;
- `research/code/engine_n_v0_2.py`;
- `research/code/run_engine_n_v0_2_preflight.py`;
- `.github/workflows/exp033-engine-n-v0.2-preflight.yml`.


### EXP-033 zero-outcome preflight PASS

Durable checkpoint: `2b8c781`.

- 626 filled valid signals;
- all eight markets pass >=25 and both directions;
- 624 safely deployable;
- GE40 32 / GE30 474 / LT30 118 / NONDEPLOYABLE 2;
- parsed source max timestamp 2026-06-30 23:59 UTC;
- zero target/P&L outcomes;
- Jul-Aug and Sep sealed.

The rolling hourly scanner solved the v0.1 opportunity-density failure without lowering the gate.

**Next permitted stage:** six-slice EXP-033 development using the already frozen >+0.20R gross-edge and post-cost economic gates.


### EXP-033 development launch checkpoint

Engine N v0.2 passed zero-outcome preflight and its six-slice development runner is frozen.

Development will test:

1. pooled normalized-R signal edge;
2. hourly-anchor cohorts descriptively;
3. safe-lot USD500 one-open portfolio;
4. matched immediate-entry control on the same qualified drives.

Mandatory gross hurdle remains **>+0.20R** and all post-cost economic gates remain unchanged.

Outcome horizon is frozen at T40/stop first within 120 active M1 bars and before 20:00 UTC.

Jul-Aug and Sep remain sealed.

**Exact next action:** run EXP-033 development only.


## Engine N family — CLOSED

Engine N v0.2 / EXP-033 failed development at `78fc698522916ce24a48d718cf948399c902e945`.

- 505 development signals;
- gross +0.0411R;
- primary -0.1450R;
- stress -0.3312R;
- only 1/6 positive-stress folds;
- safe-account primary/stress -USD2.82 / -USD6.07 per trade;
- stress MDD about USD1,244.

Continuous hourly scanning solved opportunity density but the directional-drive continuation thesis did not create robust edge.

Do not post-hoc whitelist H14/H15 or XAUUSD.

## Engine O v0.1 / EXP-034 — CURRENT PRIMARY PATH

Genuinely different family:

**rolling statistical stretch mean reversion**.

Every 15 minutes from 06:15 through 17:45 UTC, compare the latest completed M5 rejection bar to the prior 24-M5 robust center/MAD state, then use a non-chasing 50% limit with T40 required to fit before the recent center.

**Next:** zero-outcome EXP-034 preflight only.


### EXP-034 preflight attempt 1 verification note

Run `36014965193` failed before the real market preflight because the baseline-exclusion synthetic fixture changed the trigger close to a value that violated the already-frozen outer-35% rejection-location rule.

No market preflight or target/P&L outcome resulted. Jul-Aug and Sep remain sealed.

Fixture-only correction:

- `99344d6656070d79aa8d562c56869f8e24ca8f7a`.

**Next remains:** rerun the identical frozen EXP-034 zero-outcome preflight.


## Engine O v0.2 / EXP-035 — CURRENT PRIMARY PATH

Engine O v0.1 / EXP-034 is closed before outcomes after its real zero-outcome preflight failed only opportunity density:

- 209 filled valid signals;
- 209 safely deployable;
- six of eight markets passed >=25 + both directions;
- USDJPY 18;
- AUDUSD 22;
- all markets had both LONG and SHORT;
- target/P&L outcomes remained zero;
- Jul-Aug / Sep remained unopened.

The target-room rule was not the bottleneck. The frozen 15-minute decision grid was too sparse.

v0.2 changes **only the sampling grid**:

- every completed UTC-aligned M5 bar from 06:05 through 17:55 UTC;
- one decision every five minutes;
- one pending Engine-O order per symbol at a time;
- new qualified setup while pending is suppressed, not queued.

Unchanged:

- prior 24 contiguous M5 baseline;
- median CENTER / MAD / median range;
- >=2.50 MAD stretch;
- >=1.25x trigger range;
- >=50% body;
- favorable outer-35% rejection close;
- 50% non-chasing limit;
- stop beyond trigger extreme;
- 10-active-M1 / 30m order life;
- T40 must fit before CENTER;
- safe-lot caps and costs.

### EXP-035 zero-outcome preflight

Keep the same scanner gate:

- >=25 filled valid signals per market;
- LONG + SHORT every market;
- >=300 total;
- safety/causality tests pass;
- no target/P&L outcomes;
- Jul-Aug and Sep unloaded.

**Exact next action:** run EXP-035 zero-outcome preflight only.


### EXP-035 zero-outcome preflight PASS

Durable checkpoint: `6b637af`.

- 574 filled valid signals;
- all eight markets pass >=25 and both directions;
- all 574 safely deployable;
- GE40 7 / GE30 140 / LT30 427;
- parsed source max timestamp 2026-06-30 23:59 UTC;
- zero target/P&L outcomes;
- Jul-Aug and Sep sealed.

Continuous M5 scanning solved the v0.1 opportunity-density failure without changing any statistical threshold.

Development outcome convention is frozen:

- T40 vs trigger-extreme stop;
- same-bar stop first;
- max 120 active M1 bars;
- 20:00 UTC cutoff;
- same six slices;
- matched immediate-entry control;
- >+0.20R gross hurdle and all post-cost gates unchanged.

**Next:** implement and trigger EXP-035 development only.


### EXP-035 development launch checkpoint

Engine O v0.2 passed zero-outcome preflight and its six-slice development runner/workflow are frozen.

Development will evaluate:

1. pooled normalized-R signal edge;
2. per-market and six-fold stability;
3. descriptive hour-of-day cohorts only;
4. safe-lot USD500 one-open portfolio;
5. matched immediate-entry control on the same non-suppressed qualified arms.

Mandatory gross hurdle remains **>+0.20R**. All post-cost economic gates remain unchanged.

No post-outcome hour/minute/symbol whitelist is permitted inside v0.2.

Jul-Aug and Sep remain sealed.

**Exact next action:** run EXP-035 development only.


## Engine O family — CLOSED

Engine O v0.2 / EXP-035 failed development at durable result `f37a757`.

- 430 signals;
- gross -0.0719R;
- primary -0.2611R;
- stress -0.4504R;
- 0/6 positive-stress folds;
- reference primary/stress -USD3.11 / -USD5.38 per trade;
- stress MDD about USD1,394.

Continuous M5 scanning solved opportunity density, but isolated-symbol statistical-stretch mean reversion did not create robust predictive edge.

Do not post-hoc whitelist EURJPY, H16, or other retrospective cohorts.

Jul-Aug and Sep remain sealed.

**Next:** move to a genuinely different information source: cross-market relative strength / factor divergence.


## Engine P v0.1 / EXP-036 — CURRENT PRIMARY PATH

Engine O is closed at the family level after EXP-035 failed development despite adequate frequency.

The current prospectively frozen family changes the information source:

**Engine P v0.1 — Cross-Market Relative-Strength Pullback**

Every completed M5 bar from 06:05-17:55 UTC:

- compute each symbol's 30m normalized momentum from a prior-24-M5 range-vol baseline;
- require |own MOM| >=1.50;
- require contemporaneous cross-market factor confirmation;
- USD-linked pairs use a median USD_SCORE built from the other USD FX majors;
- EURJPY requires aligned EURUSD and USDJPY legs;
- current M5 must confirm direction with >=35% body and favorable outer-40% close;
- enter a non-chasing 50% M5 pullback;
- stop beyond trigger extreme;
- 10-active-M1 / 30m order life;
- unchanged T40 and safe-lot overlay.

This is the first current-family engine whose entry decision directly uses other markets' completed bars at the same timestamp.

### EXP-036 zero-outcome preflight

Require:

- exact synchronized cross-market snapshots;
- candidate-self exclusion from USD_SCORE;
- EURJPY leg-identity checks;
- all entry/safety tests;
- >=25 filled signals per market;
- both directions every market;
- >=300 total;
- zero target/P&L outcomes;
- Jul-Aug and Sep unloaded.

**Exact next action:** run EXP-036 zero-outcome preflight only.


### EXP-036 zero-outcome preflight PASS

Durable checkpoint: `12c6f5d`.

- 6,063 filled valid signals;
- all eight markets pass >=25 and both directions;
- 6,059 safely deployable;
- GE40 105 / GE30 1,253 / LT30 4,701 / NONDEPLOYABLE 4;
- parsed source max timestamp 2026-06-30 23:59 UTC;
- zero target/P&L outcomes;
- Jul-Aug and Sep sealed.

Cross-market factor confirmation easily clears opportunity density.

Development convention is frozen:

- audited T40/structural-stop labeler;
- same-bar stop first;
- max 120 active M1;
- 20:00 UTC cutoff;
- six fixed slices;
- matched immediate-entry control;
- descriptive MOM/USD_SCORE/leg/time diagnostics only;
- >+0.20R gross hurdle and all post-cost gates unchanged.

**Next:** implement and trigger EXP-036 development only.


### EXP-036 development launch checkpoint

Engine P v0.1 passed zero-outcome preflight and its six-slice development runner/workflow are frozen.

Development will evaluate:

1. pooled normalized-R signal edge;
2. per-market and six-fold stability;
3. descriptive own-MOM / USD_SCORE / EURJPY-leg / time diagnostics;
4. safe-lot USD500 one-open portfolio;
5. matched immediate-entry control on the same non-suppressed qualified arms.

Mandatory gross hurdle remains **>+0.20R**. All post-cost economic gates remain unchanged.

No post-outcome factor-threshold, hour, symbol or direction whitelist is permitted inside v0.1.

Jul-Aug and Sep remain sealed.

**Exact next action:** run EXP-036 development only.


## Engine P family — CLOSED after EXP-036 development

Engine P v0.1 / EXP-036 failed its frozen development gate at durable result commit `52e9003f351eb7f5abdf9b38f74c279c88d33906`.

Authoritative development result:

- 4,804 pooled signals;
- gross expectancy **-0.0406469R**;
- primary expectancy **-0.2356814R**;
- stress expectancy **-0.4307159R**;
- **0/6** positive-stress folds;
- 836 reference-account trades;
- reference primary/stress expectancy **-USD2.02 / -USD4.15 per trade**;
- primary/stress PF **0.761 / 0.580**;
- stress MDD **USD3,526.25**;
- final disposition **FAIL_STOP_BEFORE_SECONDARY**.

The durable result confirms Jul-Aug secondary and Sep final holdout were not loaded or labeled.

Do not rescue Engine P by changing MOM/USD_SCORE thresholds, hours, symbols, directions, target, costs or entry rules from inspected development diagnostics.

**Exact next strategy action:** open a genuinely different prospectively frozen engine family. Protected Jul-Aug and Sep remain sealed.


## Engine Q v0.1 / EXP-037 — CURRENT PRIMARY PATH

Engine P is closed after EXP-036 development failure.

The new prospectively frozen family uses a genuinely different information source:

**Cross-Market Volatility Spillover Breakout**.

Flow:

`directionless peer volatility breadth -> candidate lag/compression -> first local breakout -> non-chasing 50% pullback -> T40`.

Frozen center mechanics:

- completed M5 arm decisions 06:05-17:25 UTC;
- prior-24-M5 median range per market;
- candidate excluded from peer breadth;
- >=4 shocked peers with VR>=1.75 and >=6 valid peers;
- candidate VR<=1.00 and close inside fixed prior-six-M5 box;
- next-six-M5 breakout arm;
- first breakout VR>=1.25, body>=50%, outer-25% close;
- 50% breakout-bar retracement limit;
- stop beyond breakout extreme;
- 10-active-M1 / 30m order life;
- unchanged T40;
- primary/stress costs 10%/20% of gross target;
- unchanged USD500 safe-lot caps.

Protection/split:

- source hard-sealed at 2026-06-30 23:59 UTC;
- same six development slices from Apr13 through Jun30;
- Jul-Aug secondary sealed;
- Sep final holdout sealed.

No Engine-Q outcomes exist.

**Exact next action:** implement Engine Q v0.1 and run zero-outcome EXP-037 preflight only. Frequency gate remains >=25 filled signals per market, both directions, >=300 total.

Files:

- `strategies/engine-q-cross-market-volatility-spillover-breakout/SPEC-v0.1.md`;
- `research/experiments/EXP-037-engine-q-v0.1-cross-market-volatility-spillover-breakout.md`;
- `research/provenance/EXP-037-engine-q-v0.1-source-manifest.md`.


### EXP-037 zero-outcome implementation checkpoint

Engine-Q implementation/preflight/workflow are frozen at main SHA `c51c8f9566a6ccfddaf8117c2b0a80c45fbeb10b` before outcomes.

- engine commit `9a2a2c7`;
- runner commit `2bfb0c5`;
- workflow commit `c51c8f9`;
- target/P&L outcomes: NO;
- Jul-Aug/Sep: sealed.

**Next:** trigger one EXP-037 zero-outcome preflight and follow the long-running pipeline policy.


## Engine Q v0.1 / EXP-037 — CLOSED AT ZERO-OUTCOME PREFLIGHT

Durable result: `b05efb3038d6f3531a0def07ff6df09f0a25622b`.

- 56 filled signals total;
- all 56 safely deployable;
- all eight markets failed the >=25 + both-directions gate;
- total >=300 failed;
- no target/P&L outcomes were calculated;
- Jun30 source seal held;
- Jul-Aug and Sep remained unopened.

Main bottleneck: simultaneous same-M5 >=4 peer shocks at VR>=1.75 was too sparse, especially for FX.

Do not lower the frequency gate. Any next version must alter the zero-outcome sampling architecture prospectively rather than relax the failed gate.


## Engine Q v0.2 / EXP-038 — CURRENT PRIMARY PATH

EXP-037 / Engine Q v0.1 is closed before outcomes after the same-bar four-peer shock condition produced only 56 fills.

v0.2 preserves the volatility-spillover thesis but changes the temporal sampling architecture:

- peer shock threshold stays VR>=1.75;
- breadth stays >=4 unique peers;
- candidate remains excluded;
- a peer may contribute if it shocked on t, t-5m or t-10m;
- each peer counts once at most.

Everything downstream remains unchanged:

- candidate VR<=1.00 inside fixed prior-six-M5 box;
- next-six-M5 first breakout;
- breakout VR>=1.25, body>=50%, outer-25% close;
- 50% retracement limit;
- trigger-extreme stop;
- T40;
- 10%/20% cost stresses;
- USD500 safe-lot caps;
- unchanged >=25-per-market / both-directions / >=300-total preflight gate.

Jun30 remains the hard source seal. Jul-Aug and Sep remain sealed.

No Engine-Q v0.2 outcomes exist.

**Exact next action:** implement and run EXP-038 zero-outcome preflight only.


### EXP-038 zero-outcome implementation checkpoint

Engine Q v0.2 implementation, runner and workflow are frozen at main SHA `850fe44fa426b2ee4f235d3af140fa981ff26ae2` before outcomes.

Target/P&L outcomes remain zero; Jul-Aug/Sep remain sealed.

**Next:** trigger one EXP-038 zero-outcome preflight only.


### EXP-038 zero-outcome preflight PASS

Durable checkpoint: `3d9ca37fc733542f1ed2554e26a2989b1b578f2d`.

- 467 filled valid signals;
- all 8 markets pass >=25 and both directions;
- 466 safely deployable;
- GE40 6 / GE30 134 / LT30 326 / NONDEPLOYABLE 1;
- source max Jun30 23:59 UTC;
- target/P&L outcomes still zero;
- Jul-Aug and Sep remain sealed.

**Next permitted stage:** six-slice EXP-038 development using the already-frozen >+0.20R gross hurdle and post-cost/stability/reference-account gates.


### EXP-038 development launch checkpoint

Engine Q v0.2 passed zero-outcome preflight and its six-slice development runner/workflow are frozen at main SHA `be6c986d6ec887b202372a912444cbf7b73b9669` before outcomes.

Development evaluates:

1. pooled normalized-R signal edge;
2. per-market and six-fold stability;
3. descriptive rolling peer-shock/lag/breakout/time diagnostics;
4. safe-lot USD500 one-open portfolio;
5. matched immediate-entry control on the same qualified breakout triggers.

Mandatory gross hurdle remains >+0.20R and all post-cost economic gates remain unchanged.

Fold membership is keyed to breakout completion time. Jul-Aug and Sep remain sealed.

**Exact next action:** run EXP-038 development only.


## Engine Q family — CLOSED after EXP-038 development

Engine Q v0.2 / EXP-038 failed its frozen development gate at durable result `6f25b089d6d7eea01d37d293c48bd51bf1e84d9e`.

- 363 development signals;
- gross **+0.09479R**;
- primary **-0.09022R**;
- stress **-0.27524R**;
- **1/6** positive-stress folds;
- 251 reference-account trades;
- reference primary/stress **-USD1.53 / -USD3.89 per trade**;
- primary/stress PF **0.836 / 0.640**;
- stress MDD **USD1,102.23**.

The 50% pullback entry materially beat matched immediate entry, but the underlying spillover/breakout predictor still did not clear the frozen +0.20R gross hurdle or post-cost gates.

Do not post-hoc select peer-shock ages, lag VR, trigger VR, hours, symbols or directions. Jul-Aug and Sep remain sealed.

**Exact next strategy action:** open a genuinely different prospectively frozen information-source family.


## Engine R v0.1 / EXP-039 — CURRENT PRIMARY PATH

Engine Q is closed after EXP-038 development failure.

The new prospectively frozen family is **Dynamic Peer-Residual Reversion**.

Flow:

`causal strongest peer -> sign-adjusted normalized 15m expectation -> candidate residual dislocation -> same-bar reversion rejection -> 50% non-chasing limit -> T40`.

Frozen center mechanics:

- continuous M5 decisions 06:05-17:55 UTC;
- prior 48 M5 returns estimate candidate-peer Pearson correlation;
- candidate excluded from peer search;
- strongest absolute-correlation peer selected deterministically;
- require |rho|>=0.60;
- current 15m moves normalized by prior-48 median absolute 15m move;
- selected peer |NM15|>=1.00;
- candidate residual vs sign-adjusted peer >=1.50 in absolute value;
- trade candidate toward peer-implied relationship;
- current M5 must reject in reversion direction with >=35% body and outer-40% close;
- 50% retracement limit;
- rejection-bar structural stop;
- T40;
- unchanged 10%/20% costs and USD500 safe-lot caps.

Jun30 remains the hard source seal. Jul-Aug and Sep remain sealed.

No Engine-R outcomes exist.

**Exact next action:** implement Engine R v0.1 and run zero-outcome EXP-039 preflight only. Frequency gate remains >=25 per market, both directions, >=300 total.


### EXP-039 zero-outcome implementation checkpoint

Engine R v0.1 implementation, preflight runner and workflow are frozen at main SHA `db879da22f4ec6ab3a7ca497f110f847b7ff373f` before outcomes.

Target/P&L outcomes remain zero; Jul-Aug/Sep remain sealed.

**Next:** trigger one EXP-039 zero-outcome preflight only.


## 2026-09-25 — ROOT-CAUSE / EDGE-SOURCE RESEARCH PAUSE

The strategy-family iteration loop is paused before any further outcome development.

Authoritative audit:

- `research/ROOT-CAUSE-EDGE-SOURCE-AUDIT-v0.1.md`;
- audit commit: `b170bef290827c0c6d3c46b8d62873131c675085`.

Core finding:

- recent reproducible engines largely transform the same OHLC information source;
- their gross expectancy clusters near zero and does not clear the approximately +0.20R raw-edge hurdle needed to survive the frozen cost model;
- non-chasing execution helps materially but does not create enough predictor edge;
- the next research phase must test genuinely new information sources (microstructure/order flow, macro surprise, rates/cross-asset context, execution-grade spread/tick data) before another strategy family is advanced.

Economic finding:

- USD150-200 is a 30%-40% daily return on the USD500 reference equity;
- increasing per-trade risk can make the arithmetic easier but quickly conflicts with the -USD40 normal / -USD60 emergency loss framework;
- risk is therefore not to be increased merely to force the daily objective before a stable positive post-cost edge exists.

Engine R / EXP-039 is **PAUSED BEFORE DEVELOPMENT** for this audit. Its frozen artifact may remain in the repository, but no Engine-R target/P&L development should be launched merely from a successful frequency preflight.

Jul-Aug secondary and Sep final holdout remain sealed.

**Next project action:** complete the economic-feasibility and edge-source information-content program described in the audit before selecting the next engine for outcome development.


### Root-cause research deliverables completed

Additional durable research checkpoints:

- `research/ECONOMIC-FEASIBILITY-FRONTIER-v0.1.md` at `73e75b5d34e97d10a04d72176314363121a93d77`;
- `research/EDGE-SOURCE-RESEARCH-MATRIX-v0.1.md` at `fac6c1bb4849789aa761a2d41d46ac6df40c00f3`.

The economic frontier confirms that increasing risk is not a valid substitute for edge: under the current primary-cost convention, routine USD150 strong days require exceptionally strong hit-rate/payoff combinations, while USD30-40 structural risk per trade rapidly conflicts with the -USD40 normal / -USD60 emergency daily loss architecture.

The edge-source matrix prioritizes **macro surprise + execution-grade microstructure/order flow + rates/cross-asset interpretation**, especially COMEX Gold and representative/centralized FX flow, before another OHLC-derived strategy family.

No new strategy outcome was calculated. Engine R remains paused before development. Jul-Aug and Sep remain sealed.


## EXP-040 — ACTIVE INFORMATION-ADVANTAGE STUDY

The agreed immediate project action is now frozen and implemented:

**Multi-Timeframe Structural Context Information-Content Study v0.1**.

This is not a strategy engine. It compares the same broad structural candidate universe under nested information sets:

`LOCAL_M5 -> +15M -> +1H -> +4H/prior-day -> +session location`.

Primary question:

> Does higher-timeframe structural/location information improve out-of-sample T40eq/T50eq target-before-stop probability beyond local M5 state?

Frozen details:

- development source only through Jun30;
- six chronological folds;
- 120-minute purge before calibration/evaluation boundaries;
- fixed logistic learner + Platt calibration;
- diagnostic structural-risk ladder 1.5R / 2R / 2.5R / 3.5R / 5R;
- no hyperparameter search;
- smallest passing nested feature set selected by a predeclared parsimony rule;
- Jul-Aug and Sep remain sealed;
- Engine R remains paused.

Governance addition:

- `docs/BRAINSTORMING-AND-KNOWLEDGE-CAPTURE-POLICY.md` is now governing;
- material brainstorming must be synthesized into GitHub rather than left only in chat;
- current brainstorming synthesis is `research/BRAINSTORMING-SYNTHESIS-2026-09-25.md`.

**Exact next action:** run one EXP-040 information-content workflow and resume from its durable bot result.


### 2026-09-25 — EXP-040 operational startup block (no scientific result)

GitHub Actions run `36135418584` failed twice before any workflow step started:

- trigger SHA: `8b94aa585a737ac18f3876c3b7f8352fa164a7cb`;
- attempt 1: completed failure in ~3-4 seconds;
- attempt 2: completed failure in ~4-7 seconds;
- both attempts exposed zero job steps and no downloadable job log;
- no EXP-040 durable result file was created;
- no model, target/path label, development outcome or protected-period computation ran.

**Interpretation:** operational GitHub Actions startup/account/runner block, not an EXP-040 scientific failure and not evidence against the frozen code/mechanics.

Do not modify EXP-040 research mechanics in response to this red check. Exact next action is to resolve the GitHub Actions pre-run failure from the workflow Details/account Actions status, then rerun the same frozen experiment. Jul-Aug and Sep remain sealed; Engine R remains paused.


## EXP-040 result — COMPLETE / NO STABLE MTF INFORMATION ADVANTAGE

Durable result: `46049f7d94131db50e7d9cbb13a3fa82dcafb810`.

The corrected rerun completed successfully and passed integrity.

Result:

- 123,724 labeled development candidates;
- 99,622 pooled evaluation predictions per primary rung;
- no enriched MTF feature set passed the frozen T40eq/T50eq gate;
- +15M, +1H, +4H/prior-day and +session context all failed to improve stable out-of-sample prediction versus LOCAL_M5;
- Jul-Aug and Sep remained sealed;
- Engine R remained paused and its target/P&L outcomes were not used.

**Interpretation:** generic multi-timeframe OHLC context is not the information advantage the project needs.

**Exact next research action:** macro/catalyst information-content study, beginning with historical event timestamps + actual/consensus surprise and testing incremental value over the price-only baseline before any strategy rules are built.


## EXP-041 — MACRO/CATALYST INFORMATION RESEARCH / DATA-ADEQUACY PHASE

The project is deliberately **not** fitting another news/price model yet.

A new governing expert-process decomposition is frozen in:

- `research/HUMAN-TRADER-EDGE-DECOMPOSITION-v0.1.md`.

Working sequence:

`catalyst/regime -> structural location -> participation/market interpretation -> trigger -> non-chasing execution -> structural stop -> target path -> EV/ranking -> equity-adaptive sizing`.

### EXP-041 Gate A finding

The current Mar-Jun development window contains only **17 independent primary macro event blocks**:

- 3 Employment;
- 3 CPI;
- 3 PPI;
- 3 Retail Sales;
- 3 GDP/PCE;
- 2 FOMC.

This is **not enough independent event history** for a trustworthy macro-surprise model. Hundreds of candidate rows around one CPI release are still one economic event.

Therefore Gate A disposition is:

`DATA_INSUFFICIENT_EXTEND_EARLIER_HISTORY`.

No macro outcome model has been run. No protected period has been used.

Durable artifacts:

- `research/experiments/EXP-041-macro-catalyst-information-content-v0.1.md`;
- `research/EXP-041-DATA-ADEQUACY-AUDIT-v0.1.md`;
- `research/provenance/EXP-041-macro-catalyst-source-manifest.md`;
- `research/data/EXP-041-macro-catalyst-seed-v0.1.json` (17-event plumbing seed only; not final promotion data).

### Extended development market history

The market-history half of Gate A is now prospectively frozen:

- source authority: Dukascopy Bank historical data;
- transport helper: exact `dukascopy-node@1.50.0`;
- interval: **2025-07-01 through 2026-06-30 only**;
- eight existing execution markets;
- use one consistent Dukascopy M1 feed for the full expanded EXP-041 development interval;
- do **not** splice the old and new feeds;
- existing pinned source is overlap sanity only;
- raw files are not committed; hashes/coverage/overlap are durably checkpointed;
- zero target labels / zero P&L in this acquisition stage.

Implementation checkpoint:

- downloader commit `df925e3`, blob `93032b2`;
- acquisition-audit commit `208de49`, blob `16f20f0`;
- workflow commit `2ad8174`, blob `2caabe6`.

Jul-Aug and Sep 2026 remain sealed. Engine R remains paused.

**Exact next action:** trigger one EXP-041 extended-market-history acquisition/audit. If it passes, continue the macro Gate-A work by acquiring enough point-in-time event history; do not run Gate B until sample-independence requirements pass.


### EXP-041 extended-history attempt 1 — operational failure only

Run `36153466140` completed **failure**, but this was not a data/scientific gate result.

Verified job sequence:

- setup/install: PASS;
- acquisition code verification: PASS;
- full frozen 12-month Dukascopy download: **PASS for all 8 markets**;
- downloaded normalized-row counts ranged from 338,380 to 368,988 per market;
- audit crashed immediately on an unnecessary import dependency: `ModuleNotFoundError: joblib`;
- no audit JSON was produced;
- no target labels, P&L, strategy outcomes, Jul-Aug data, or Sep data were computed.

Operational fix commit: `105eb2e290c06a76fcd0cee9d0faeee656113f3f` removes the modeling-module dependency and locally parses only the overlap rows needed for source sanity. Frozen acquisition interval, source, integrity thresholds and scientific rules are unchanged.

**Next:** rerun the same EXP-041 acquisition/audit once.


## EXP-041 extended-history acquisition v0.1 — DURABLE GATE FAIL / DIAGNOSTIC REQUIRED

Durable audit commit: `1cf168d6b3b639cfcc856ffae7aeb66db880dc47`.

The second run completed acquisition and produced a valid audit result. This is now a genuine data-quality checkpoint, not an operational error.

What passed:

- all 8 Dukascopy M1 feeds downloaded for the frozen Jul2025-Jun2026 interval;
- 338,380 to 368,988 normalized rows per market;
- all files begin 2025-07-01;
- Jun30 hard source seal held;
- no duplicate timestamps;
- OHLC geometry/positivity/monotonicity passed;
- exact-M1 overlap versus the existing pinned source was ~99.66%-99.86% for all markets;
- no target labels / no P&L / no Jul-Aug / no Sep.

What failed:

- cross-feed sanity failed for 7/8 markets;
- only USDCAD passed all frozen cross-feed checks;
- hourly-return correlation versus the existing pinned source ranged from ~0.779 to 0.974, with several markets below the frozen 0.95 threshold;
- median absolute relative close difference exceeded 0.5% for XAUUSD, EURUSD, AUDUSD and USDCHF;
- USDCHF Dukascopy coverage ended 2026-06-29 23:59 UTC, failing the frozen final-day coverage check.

Therefore:

`market_history_gate_pass = FALSE`.

Do **not** weaken the frozen v0.1 sanity thresholds post hoc and do not proceed to macro outcome modeling yet.

**Exact next action:** run a zero-outcome cross-feed diagnostic on the Mar23-Jun30 overlap to determine whether the discrepancy is a time alignment, stable price-basis, symbol/feed-construction, or material path mismatch. Only after that diagnosis may a prospectively frozen acquisition v0.2 be considered.


## EXP-041 cross-feed diagnostic — COMPLETE / THIRD SOURCE REQUIRED

Durable diagnostic: `bdd3b7f`.

The discrepancy between the existing pinned feed and Dukascopy is **not** a simple timestamp alignment problem. Best 5m and 1h lag is zero across all eight markets, while several FX markets still have materially sub-0.95 1h return correlation.

Frozen diagnostic classification:

- all 8 markets: `MATERIAL_PATH_MISMATCH`;
- USDCHF also: `SOURCE_COVERAGE_GAP`.

No target labels or P&L were calculated; Jul-Aug/Sep remain sealed.

**Exact next action:** third-source adjudication using HistData.com M1 bid bars on the same Mar23-Jun30 overlap. Do not choose a feed or run macro outcomes until the three-feed comparison is complete.

## 2026-09-25 — EXP-041 THIRD-SOURCE ADJUDICATION COMPLETE / NO SOURCE SELECTED

Durable result commit: `3e5ed20a733bf80fc72c155c756edf7c115c566e`.  
Workflow run `36156982409` completed successfully.

Frozen three-feed result:

- CURRENT_PINNED supported in 2/8 markets;
- DUKASCOPY supported in 2/8 markets;
- HISTDATA supported in 0/8 markets;
- XAUUSD and USDCAD = `HISTDATA_OUTLIER`;
- six markets = `NO_TWO_SOURCE_CONSENSUS`;
- eligible consensus sources = none;
- feed-selection gate = FAIL;
- disposition = `NO_CLEAR_CONSENSUS_REQUIRE_FOURTH_OR_BROKER_SOURCE`.

No target labels or P&L were calculated. Jul-Aug and Sep remain sealed.

Do not accept CURRENT_PINNED, Dukascopy, or HistData by preference and do not relax the frozen adjudication criteria.

A data-engineering anomaly remains worth one zero-outcome check: HistData has poor intraday correlation but materially stronger daily correlation versus Dukascopy on several markets. This can be consistent with a timestamp-semantics problem even though minute-grid overlap is high.

**Exact next action:** prospectively freeze and run one HistData timestamp-semantics diagnostic on the same Mar23-Jun30 overlap only. Test common mechanical hour shifts across all markets; no per-market shift fitting, no target labels/P&L, no protected data, no threshold relaxation. If no common correction restores broad agreement under the original pairwise gates, require an intended-broker or another institutional-quality fourth source before EXP-041 macro modeling.

### EXP-041 HistData timestamp diagnostic — implementation frozen

The zero-outcome timestamp-semantics diagnostic is prospectively frozen at main SHA `2791376846eff374c708f0346da29432ab77f1bd`.

Frozen artifacts:

- `research/EXP-041-HISTDATA-TIMESTAMP-SEMANTICS-DIAGNOSTIC-v0.1.md`;
- `research/code/run_exp041_histdata_timestamp_diagnostic.py`;
- `.github/workflows/exp041-histdata-timestamp-diagnostic.yml`.

It tests only one common whole-hour HistData shift from -6h through +6h across all eight markets and replays the original third-source pairwise/feed-selection gates unchanged.

No per-market shift fitting, target labels, P&L, Jul-Aug or Sep data are authorized.

**Exact next action:** trigger exactly one EXP-041 HistData timestamp-semantics diagnostic workflow. Confirm launch once, then resume from the durable bot result rather than polling.



## 2026-09-25 — EXP-041 HISTDATA TIMESTAMP DIAGNOSTIC COMPLETE / PUBLIC-FEED REMEDIATION CLOSED

Durable result commit: `f98eba568e1aad440873443eaec4e7ed7480b20e`.

Frozen result:

- tested one common HistData shift from -6h through +6h;
- no common shift restored the original third-source feed-selection gate;
- passing common shifts: none;
- best descriptive shift: -1h, but still no eligible consensus source and five markets without two-source consensus;
- target labels/P&L: none;
- Jul-Aug/Sep: not loaded;
- disposition: `TIMESTAMP_SHIFT_DOES_NOT_EXPLAIN_FAILURE_REQUIRE_FOURTH_OR_BROKER_SOURCE`.

Do not continue HistData timestamp fitting or relax the old gate.

### Prospective v0.2 data-governance decision

The project is closing the public-feed-consensus loop rather than spending additional cycles forcing free feeds to agree.

For EXP-041 development, Dukascopy is now the **canonical research market-history source** under `research/EXP-041-DATA-SOURCE-GOVERNANCE-v0.2.md`.

This does not rewrite the v0.1 failure and does not claim Dukascopy equals broker execution truth. The old consensus gate remains failed and documented.

Before macro Gate B:

- freeze the exact already-audited Dukascopy normalized bytes as an immutable GitHub Release snapshot;
- require exact reproduction of the v0.1 SHA-256 hashes;
- fail closed if Dukascopy history has drifted;
- use common modeling interval 2025-07-01 through 2026-06-30 00:00 UTC exclusive because USDCHF stops at Jun29 23:59;
- after snapshot creation, all EXP-041 development workflows consume the immutable release, not live Dukascopy;
- intended-broker/institutional bid/ask/tick/spread validation remains mandatory before deployment.

Snapshot governance commit: `4e4e499f90e897bfb7d12a63c7372b8afb510969`.  
Snapshot verifier commit: `3cd2b1914a14aaeb5449ab78c39c62707b2bcb93`.  
Snapshot workflow commit: `ddd2537af351ec67d4ab7ba2c3356d40bd31ca10`.

**Exact next action:** trigger exactly one canonical Dukascopy snapshot workflow. If exact hashes reproduce, checkpoint the immutable release and move to point-in-time macro consensus/actual history acquisition. If hashes drift, stop for source-drift investigation.


### EXP-041 canonical Dukascopy snapshot — attempt 1 red check / diagnostic hardening

Trigger commit `0e685e11dc709ac62d1caa931f500a6486fa508d` finished with a red 0/1 check and produced no durable snapshot result commit.

The connector did not expose the push-run/job logs for that attempt, so the red check alone is **not classified as source drift or a scientific gate result**.

A reproducibility/observability weakness was identified in the first snapshot workflow:

- exact-hash mismatch could terminate before the JSON diagnostic was committed;
- the archive-internal manifest contained run-specific metadata, so otherwise identical data could produce different archive hashes on rerun.

Operational hardening only:

- snapshot verifier commit `a20206c36fecd3cb7358c0bec024914fc741fe7a`;
- workflow commit `3aaed8391b28966eebe8483954107b88d1e5c06b`.

The frozen source, eight expected SHA-256 hashes, transport version, development interval, common modeling cutoff, protected-period rules, and no-label/no-P&L boundary are unchanged.

The hardened workflow now:

- always writes a durable exact-hash diagnostic after a successful download;
- creates a release only when all eight frozen hashes/row counts match;
- commits the diagnostic even when hash reproduction fails;
- keeps run-specific metadata outside the archive-internal manifest;
- treats an already-existing matching release as idempotent recovery rather than overwriting it.

**Exact next action:** update the snapshot trigger once and inspect the next durable bot checkpoint. Do not infer source drift unless the durable diagnostic says so.


## 2026-09-27 — EXP-041 canonical snapshot v1 hash reproduction FAILED / SAME-RUN REPEATABILITY NEXT

Durable result commit: `2dc6a9c0cc1c588fa01179bcc644d5fb6e9fd578`.  
Workflow run: `36264975005`.

Observed:

- live Dukascopy download completed successfully;
- all eight markets differed from Sep25 frozen reference hashes and row counts;
- release/archive creation was correctly skipped;
- final integrity step failed by design;
- no labels/P&L/scientific outcomes;
- Jul-Aug/Sep remained sealed;
- disposition: `LIVE_DUKASCOPY_NO_LONGER_REPRODUCES_FROZEN_AUDITED_BYTES_STOP_FOR_SOURCE_DRIFT`.

This proves current acquisition output differs from the earlier observed output, but it does not yet distinguish genuine upstream revision from nondeterministic/incomplete transport.

Prospectively frozen next diagnostic:

- spec: `research/EXP-041-DUKASCOPY-REPEATABILITY-SNAPSHOT-RECOVERY-v0.1.md`;
- runner commit: `31460148e3cafd2528f707b513663f3e5adffcdc`;
- workflow commit: `743411b0105d097afb48e47e6dea1be0eb85ec8d`.

It performs two independent same-run Dukascopy downloads with identical frozen request semantics and requires exact SHA-256 equality plus integrity across all eight markets.

If repeatability FAILS: fix acquisition transport before any snapshot/modeling.

If repeatability PASSES: freeze copy A immediately as immutable snapshot v2 in the same workflow run. Because no EXP-041 outcomes were ever computed on the unrecoverable Sep25 bytes, adopting the prospectively validated repeatable current snapshot does not contaminate outcome research.

**Exact next action:** trigger the repeatability/snapshot-recovery workflow once, then resume from its durable bot result.


## 2026-09-27 — EXP-041 DUKASCOPY SNAPSHOT V2 FROZEN / PRICE-DATA BLOCKER CLOSED

Durable result commit: `b69e6cb9376c4f57622d042d19de41041a60dca7`.  
Workflow run: `36265569383`.

Result:

- two independent same-run Dukascopy downloads completed;
- all 8 markets matched byte-for-byte between A/B;
- all 8 passed schema, coverage, monotonicity, duplicate, positivity and OHLC-geometry checks;
- repeatability gate = PASS;
- immutable release v2 created/verified;
- release tag: `exp041-data-dukas-m1-2025-07-01_2026-06-30-v2`;
- archive SHA-256: `90bc7301e459062e8e35cd89a1a9aac23332ca3472014dd2cc5045ba34794272`;
- no labels/P&L/scientific outcomes;
- Jul-Aug/Sep remained sealed;
- disposition: `CURRENT_DUKASCOPY_REPEATABLE_IMMUTABLE_SNAPSHOT_V2_FROZEN`.

Active governance is now `research/EXP-041-DATA-SOURCE-GOVERNANCE-v0.3.md`.

**Price-data acquisition is no longer the EXP-041 blocker.** Do not re-download live Dukascopy for EXP-041 modeling. Downstream work must consume and verify the exact immutable v2 release.

**Exact next action:** acquire enough point-in-time macro event history (official release timestamps + pre-release consensus + actual-as-released) to pass EXP-041 Gate A. Preferred consensus source remains Trading Economics historical point-in-time data; Econoday is an acceptable alternative.


## 2026-09-27 — EXP-041 MACRO PIT ACCESS/PROVENANCE PREFLIGHT FROZEN

Price-data acquisition is closed via canonical Dukascopy snapshot v2. The remaining Gate-A blocker is now point-in-time macro consensus/actual-as-released history.

Frozen preflight:

- spec commit: `5bf095c9ae0ce0af94d1a98c906a65331758bb31`;
- runner commit: `12075b89367e3af2ef98a6ae0cb373656f3306e5`;
- workflow commit: `57c42fac9c872ddf733c6c00f3e84246f06b1cc7`.

The preflight uses Trading Economics only on 2026-03-01..2026-06-29 development dates and verifies technical access to Date/CalendarId/Event/Category, Actual, survey Forecast consensus, Previous/Revised and source provenance across the frozen macro families.

Security/licensing boundary:

- API key is read only from GitHub secret `TRADING_ECONOMICS_API_KEY`;
- secret is never printed/committed;
- raw vendor payload is not committed;
- only response hash, schema/coverage counts and non-value sample identifiers/timestamps are checkpointed.

No market data, target labels, P&L, Jul-Aug or Sep are loaded.

PASS => freeze separate full-history acquisition/audit for 2025-07-01..2026-06-29.

CREDENTIAL/PIT ACCESS FAIL => obtain the required Trading Economics entitlement or move to Econoday historical point-in-time data; do not weaken causality requirements.

**Exact next action:** trigger one macro PIT access/provenance preflight and resume from its durable diagnostic.


## 2026-09-27 — TRADING ECONOMICS CREDENTIAL BLOCKER BYPASSED PROSPECTIVELY WITH FREE-SOURCE PREFLIGHT

Trading Economics preflight durable result: `6eeb4e93f937fb51e6b2db39d7d57aeb11cf4023`.

Result:

- credential present = false;
- disposition = `CREDENTIAL_REQUIRED`;
- no market data/outcomes/protected periods used.

The project will not require a paid API before testing a free, causally defensible alternative.

Frozen free-source architecture:

- Forex Factory historical calendar = public historical `Forecast` consensus proxy;
- BLS/Census/BEA/Federal Reserve archives = official release-time and actual-as-released authority.

Implementation:

- spec commit: `9c63a1f2f8cbc7eee2b83d2e404d23725cccbf9d`;
- runner commit: `afc31da851cd0b9932d7bbdba966188162439d36`;
- workflow commit: `c33598dc663273762e0f1563fff516aade1f3412`.

The preflight queries only four Jun-2026 development weeks plus official Jun-2026 release pages. It computes no labels/P&L and touches no Jul-Aug/Sep data.

PASS => freeze full Jul2025-Jun29 2026 public-calendar consensus + official-release acquisition/audit.

FAIL => repair only public-source access/parser mechanics or choose another free consensus archive; do not return to paid API by default and do not weaken causality.

**Exact next action:** trigger one free macro source preflight and resume from its durable checkpoint.


## 2026-09-27 — FREE MACRO SOURCE PREFLIGHT PASSED / FULL CONSENSUS ACQUISITION FROZEN

Free-source preflight durable result: `bdaaa023879a01e2620a0b9260265a98e7d9e4bd`.

Result:

- disposition = `FREE_MACRO_SOURCE_ARCHITECTURE_PREFLIGHT_PASS`;
- all four historical Forex Factory Jun-2026 development pages returned HTTP 200;
- Actual / Forecast / Previous columns present on every tested page;
- all six target families detected;
- official BLS Employment/CPI/PPI pages passed date/time markers;
- Census retail archive reachable;
- BEA GDP/PCE release pages passed date/time markers;
- Federal Reserve FOMC statement passed date/time markers;
- no market data, labels/P&L or protected-period data used.

The paid Trading Economics path is no longer the active blocker.

Full consensus-layer acquisition is prospectively frozen:

- spec: `research/EXP-041-FULL-FREE-MACRO-CONSENSUS-ACQUISITION-v0.1.md`;
- spec commit: `f51f6cece8ba7703854806e3a952398f75bd375e`;
- runner commit: `78e388ba705b101a407e9dd61eba5740f3bcdb24`;
- workflow commit: `cdd373db282345c03b578a0e1dad37595f20e179`.

Scope:

- Forex Factory historical development pages only;
- retained event dates 2025-07-01..2026-06-29;
- week pages through 2026-06-22 plus a day-only 2026-06-29 request, so no July page is loaded;
- normalize only USD target-family rows;
- freeze Forecast as `PUBLIC_CALENDAR_CONSENSUS_FF`;
- Actual/time remain diagnostic pending first-party reconciliation;
- no raw HTML committed;
- no market data/labels/P&L.

Coverage gate requires >=40 provisional blocks, >=30 surprise-bearing blocks and >=8 blocks in each recurring numeric family. FOMC is reported separately and may remain timing-only.

**Exact next action:** trigger one full free macro consensus acquisition/audit. PASS => freeze official-release reconciliation. FAIL => repair only public parser/access or free-source coverage.


## 2026-09-27 — FREE CONSENSUS v0.1 COVERAGE PASSED / ZERO-OUTCOME SCOPE CORRECTION REQUIRED

Durable v0.1 acquisition result: `48291dc19916616ade0852faa067194ebfb6172e`.

Coverage evidence:

- 597 normalized target-family rows;
- 483 provisional blocks;
- 94 surprise-bearing provisional blocks;
- family provisional blocks: EMPLOYMENT 16, CPI 17, PPI 19, RETAIL 15, GDP_PCE 22;
- every recurring numeric family exceeded the frozen >=8 minimum;
- all pages HTTP 200;
- no protected-period or market-outcome use.

Record inspection found two parser-scope defects before official reconciliation:

1. Forex Factory's `Non-Farm Employment Change` label was not included, so the primary NFP component was omitted.
2. FOMC matching included speeches/minutes/press conferences, inflating FOMC to hundreds of non-policy rows.
3. FF displayed time is often blank/repeated, so it should not determine provisional independent-event counting before official timing reconciliation.

These are zero-outcome data-cleaning corrections, not scientific tuning.

Frozen corrected v0.2:

- spec commit: `3489490742d4a5d7bae9cca3d6585d1451aba8a4`;
- runner commit: `977ac996086ef3686177bb11f1426c0ab8c324da`;
- workflow commit: `3e30ce61e387af3e3588c3fb01c2a6e5e966cce4`.

v0.2 adds NFP aliases, restricts FOMC to Statement/Federal Funds Rate/Economic Projections, and groups provisional event blocks by date+family only.

**Exact next action:** run one corrected full consensus v0.2 acquisition. Only v0.2 may feed official BLS/Census/BEA/Fed reconciliation.


## 2026-09-27 — CORRECTED CONSENSUS v0.2 PASSED / ADP REMOVAL v0.3 REQUIRED

Corrected v0.2 durable result: `308ee5c6e1d5f0edb17ab3d6420e97384516f44c`.

Result:

- consensus layer gate = PASS;
- 215 normalized rows;
- 80 provisional independent event blocks;
- 80 surprise-bearing provisional blocks;
- family block counts:
  - EMPLOYMENT 23;
  - CPI 11;
  - PPI 11;
  - RETAIL 12;
  - GDP_PCE 15;
  - FOMC 8;
- NFP component present;
- FOMC reduced to 8 policy-event dates;
- no market data/outcomes/protected-period use.

Identity inspection found one remaining source-scope issue:

- EMPLOYMENT still includes `ADP Non-Farm Employment Change`, a private ADP release rather than the BLS Employment Situation.

Therefore v0.2 proves coverage but is not the final official-reconciliation input.

Frozen deterministic v0.3:

- spec commit: `7a85aeafba0427b12912d183e3686e07804ddc9e`;
- runner commit: `64f35f7281c14425d2f0500c6ff79fc0b213a356`;
- workflow commit: `59aebbb56fe827414a5d37435402bea0e51b4091`.

v0.3 uses no network. It consumes the exact frozen v0.2 dataset SHA `17e93b760a7511688db110ca6e02f2892d485fad7321f6a9a21ef76d02d42811`, removes ADP from the primary EMPLOYMENT family, retains only BLS-style NFP/Unemployment/Average-Hourly-Earnings components, rebuilds date+family blocks, and reruns the same coverage gate.

**Exact next action:** trigger one v0.3 deterministic scope correction. PASS => freeze official BLS/Census/BEA/Fed reconciliation.


## 2026-09-27 — FREE CONSENSUS v0.3 PASSED / OFFICIAL RELEASE-TIME RECONCILIATION FROZEN

Durable v0.3 result: `81e6f6f44a6acf906e46af056c58362b03bf0709`.

Result:

- v0.2 source SHA verified exactly;
- 12 ADP rows removed;
- no ADP rows remain;
- 203 normalized rows;
- 68 provisional independent event blocks;
- 68 surprise-bearing blocks;
- family block counts:
  - EMPLOYMENT 11;
  - CPI 11;
  - PPI 11;
  - RETAIL 12;
  - GDP_PCE 15;
  - FOMC 8;
- every required numeric family remains >=8;
- no network, market data, target labels, P&L or protected-period use;
- disposition: `FREE_CONSENSUS_V03_BLS_EMPLOYMENT_SCOPE_PASS_OFFICIAL_RECONCILIATION_REQUIRED`.

Official reconciliation is now split prospectively into two zero-outcome phases:

1. **Phase A:** first-party source identity + official release timestamp UTC for all 68 blocks;
2. **Phase B:** component-level official actual-as-released numeric reconciliation.

This prevents timestamp/source failures from being mixed with component parsing failures.

Frozen Phase-A implementation:

- spec commit: `3ff0aef8c0c36697370dce1253bbcffb1872a5bb`;
- runner commit: `ad4dc21b80a13076a3f7c3009ca104f6d700eec5`;
- workflow commit: `87cf69dcdfe91779d572d971ae294892d4cb6f23`.

Authorities:

- BLS archived Employment/CPI/PPI pages;
- Census Monthly Retail Trade official release schedule;
- BEA 2025/2026 official release schedules;
- Federal Reserve archived FOMC statement pages.

Release times are converted with `America/New_York` -> UTC using `zoneinfo`.

**Exact next action:** trigger one official release-time reconciliation. PASS => freeze component-level official actual-as-released reconciliation.


## 2026-09-27 — OFFICIAL RELEASE-TIME RECONCILIATION v0.1 FAILED ON SOURCE MAPPING / v0.2 FROZEN

Durable v0.1 result: `a8bceb64027d48de9d2533d852a41d86f9c11e54`.

The failure was operational/source-mapping, not a macro-information result:

- EMPLOYMENT resolved 11/11;
- CPI resolved 11/11;
- PPI resolved 11/11;
- RETAIL resolved 9/12;
- FOMC resolved 1/8;
- GDP_PCE resolved 0/15;
- input v0.3 SHA verified;
- no market data/outcomes/protected periods used.

Root causes:

1. Fed runner used an incorrect FOMC statement URL pattern for most meetings.
2. Retail used a generic schedule page instead of direct historical MARTS release PDFs.
3. BEA schedule parsing assumed one 8:30 release per GDP_PCE date and did not parse the actual schedule structure.
4. Official BEA schedules show that GDP and Personal Income & Outlays can occur on the same date at different times; those provisional same-date GDP_PCE blocks must be split by official release identity.

Frozen v0.2:

- spec commit: `949382b7d5bdf5d712c13b69fad6d91cc305f303`;
- runner commit: `2f7aa1d5521bc4b9efb41616b1598db295f56cae`;
- workflow commit: `f3bea537c8fd9c8b387a4a011fef726436f9f9d1`.

v0.2:

- keeps working BLS direct archive mappings;
- maps all 12 Retail dates to direct official Census MARTS historical PDFs;
- parses official BEA 2025/2026 schedule rows and splits GDP vs PCE sub-blocks when required;
- uses the correct Fed press-release URL `/newsevents/pressreleases/monetaryYYYYMMDDa.htm`;
- preserves the exact frozen v0.3 Forex Factory consensus records unchanged;
- computes no market outcomes.

**Exact next action:** trigger exactly one official release-time reconciliation v0.2. PASS => freeze Phase B official actual-as-released reconciliation.


## 2026-09-27 — OFFICIAL RELEASE-TIME v0.2 ISOLATED TO 2026 BEA PARSER / v0.3 FROZEN

Durable v0.2 result: `83b12d3673fb770854f12e93b3c479d7a3f79743`.

v0.2 successfully resolved:

- EMPLOYMENT 11/11;
- CPI 11/11;
- PPI 11/11;
- RETAIL 12/12;
- FOMC 8/8;
- 2025 BEA GDP/PCE blocks.

Only 14 BEA 2026 sub-blocks remained unresolved: GDP + PCE on Jan22, Feb20, Mar13, Apr9, Apr30, May28 and Jun25.

The official BEA 2026 release schedule contains these rows, including Jan22 GDP at 8:30 AM and Personal Income and Outlays at 10:00 AM, and later 2026 paired GDP/PCE releases. The remaining failure is therefore the HTML schedule-row parser.

Frozen v0.3:

- spec commit: `cc7efa0fdbd6ec75fd6d9b84c3ef64ebf3b95c0a`;
- runner commit: `232ee1f809c4a2002f2a830c645d8fff11abd9ce`;
- workflow commit: `8a002c2dc82dc9786932511cf921c90150a5cd21`.

v0.3 changes BEA parsing only:

- parse schedule rows/containers rather than relying on one flattened-text regex;
- retain linked first-party BEA release URL when exposed;
- classify exact date + GDP/PCE release identity;
- preserve each row's actual official local time;
- keep all BLS/Census/Fed mappings and frozen consensus values unchanged.

**Exact next action:** trigger one official release-time v0.3 reconciliation. PASS => freeze Phase B official actual-as-released reconciliation.


## 2026-09-27 — OFFICIAL RELEASE-TIME v0.3 FAILED ON BEA HTML LAYOUT / v0.4 DIRECT-PAGE REPAIR FROZEN

Durable v0.3 result: `b340e2878cf442196e5c5d6d640451c2f93a99e5`.

v0.3 confirmed the remaining issue is BEA schedule-layout parsing:

- 2026 BEA schedule rows parsed as 0;
- 2025 BEA parser produced duplicate matches;
- all non-BEA mappings remain resolved;
- no market data/outcomes/protected periods used.

To avoid further brittle schedule scraping, v0.4 prospectively switches the unresolved 2026 BEA blocks to direct first-party BEA news-release pages.

Frozen v0.4:

- spec commit: `8f2415adddbaa602285636b17cfda195690328d8`;
- runner commit: `3c25b1a43f0fb10ef7e2ac5b31952f19e5d08fe9`;
- workflow commit: `d4e2ff11887832b67bc7d9e14c50f5f24b80db22`.

Recovery base:

- exact v0.2 official-time map SHA-256: `691c09da1829695821ead84647bb87b2b1b4c1a4cdc4d727cb33042e991edd1a`;
- 75 official blocks total;
- preserve every resolved non-BEA and 2025-BEA block unchanged;
- replace only the 14 unresolved 2026 BEA GDP/PCE blocks.

Each direct BEA page must verify exact date, embargo marker, local time, EST/EDT consistency, release identity and source hash. No BEA full-year 2026 schedule page is fetched in v0.4.

**Exact next action:** trigger exactly one official release-time v0.4 repair. PASS => freeze Phase B official actual-as-released reconciliation.


## 2026-09-27 — OFFICIAL RELEASE-TIME v0.4 PASSED / PHASE-B ACTUAL RECONCILIATION FROZEN

Durable v0.4 result: `9a853a0ba2ab32a537e096fff45e57747f85eb8f`.

Result:

- exact v0.2 base-map SHA verified;
- all 14 direct 2026 BEA pages verified;
- all 75 official blocks complete;
- untouched non-repair blocks remained identical to v0.2;
- no market data/outcomes/protected periods used;
- official-time map v0.4 SHA: `ced4a536b5c99db9ac9ad3ed29c49b13ba1058770ed3eaa4d65250220d60d28e`;
- disposition: `OFFICIAL_RELEASE_TIME_RECONCILIATION_V04_PASS_ACTUAL_VALUES_REQUIRED`.

The release-time blocker is CLOSED.

Phase B is now prospectively frozen:

- spec commit: `0040f86ee3bfe4acd59af5852da7209a253d00c3`;
- runner commit: `5b6247322cc017c9efdd13564f148b82d61749c4`;
- workflow commit: `0e5d45c4c657f64efa76ff127be1f5da91dbab5c`.

Canonical-component audit before freezing Phase B found:

- exactly 67 numeric official blocks;
- all 67 have exactly one forecast-bearing canonical component under the frozen hierarchy;
- no missing or ambiguous selections;
- 8 FOMC policy blocks remain timing-only.

Phase B does not parse every secondary statistic. It verifies one canonical surprise-bearing component per numeric official block against the first-party release context and retains the frozen Forex Factory historical Forecast.

PASS => one final zero-outcome Gate-A audit.

**Exact next action:** trigger exactly one official actual-as-released reconciliation Phase B.


## 2026-09-27 — PHASE B PASSED / FINAL GATE-A AUDIT FROZEN

Official actual-as-released reconciliation durable result: `fe8e180551741d205b2eb620bfa46330aee73c4e`.

Result:

- 67/67 numeric official blocks reconciled;
- 8/8 FOMC blocks retained timing-only;
- zero reconciliation errors;
- all numeric records have frozen Forecast, first-party-verified Actual, official source hash and UTC timestamp;
- surprise layer SHA-256: `ec267643940733db4647d5d1dc5537099e3fc149ee7e0e9257b1b8786017c362`;
- no market data, target labels, P&L or protected-period use;
- disposition: `OFFICIAL_ACTUAL_RECONCILIATION_PASS_FINAL_GATE_A_REQUIRED`.

Final Gate-A is prospectively frozen:

- spec commit: `d9b6dce6366a200fd92f942e1319a44f708fe503`;
- runner commit: `02200aa0a1b472055208ab3022d44cfff682f99a`;
- workflow commit: `1520b4120312a134be7425ef6a58c2a3387742c0`.

Important anti-pseudoreplication rule:

- exact same `official_release_timestamp_utc` records collapse to one independent event block;
- a simultaneous timestamp can contain multiple families but counts once toward total independent blocks.

Six chronological evaluation folds are frozen before outcomes by sorting independent timestamps and splitting them contiguously/as evenly as possible. These fold boundaries become the default Gate-B folds and cannot be redrawn after seeing market outcomes.

The audit checks the original frozen Gate-A requirements unchanged, including >=40 independent blocks, >=30 surprise-bearing blocks, >=8 timestamps per recurring numeric family, >=6 FOMC events or timing-only, >=4 blocks/fold, >=2 families/fold, point-in-time Forecast provenance, official release timestamps, 12-month canonical market history, and protected-period seal.

**Exact next action:** trigger one final Gate-A adequacy/provenance audit. PASS => Gate B information-content study becomes authorized.


## 2026-09-27 — EXP-041 GATE A PASSED / GATE B FROZEN

Final Gate-A durable result: `4208af07c148a5d37c61cbbbeb004b83fec14af5`.

Gate A PASS:

- 65 independent macro timestamps after exact-time collapse;
- 57 surprise-bearing independent blocks;
- EMPLOYMENT 11, CPI 11, PPI 11, RETAIL 12, GDP_PCE 16, FOMC 8;
- all six frozen chronological folds passed;
- 12-month canonical Dukascopy v2 history verified;
- point-in-time Forecast provenance verified;
- official Actual and release-time provenance verified;
- Jul-Aug/Sep protected periods sealed.

Disposition:

`EXP041_GATE_A_PASS_AUTHORIZE_GATE_B_INFORMATION_CONTENT`.

Gate-B implementation is frozen before outcomes:

- spec: `research/EXP-041-GATE-B-MACRO-INFORMATION-CONTENT-v0.1.md`;
- spec commit: `5980e34433de38b17a64e31a260b5beeefa1a054`;
- runner commit: `015eb7b5cf50a86159614b43f331120991322fae`;
- workflow commit: `55ebbedde6bdcdc083d71d6f6a6676d68bbb4b0a`.

Gate B:

- consumes immutable Dukascopy snapshot v2, never live Dukascopy;
- reuses EXP-040 broad structural candidate and target-path mechanics;
- evaluates only [-60m,+180m] around frozen macro timestamps;
- compares LOCAL_M5 vs +CATALYST_TIMING vs +SURPRISE_MAGNITUDE;
- uses the six frozen event folds as grouped outer holdouts with inner fold OOF Platt calibration;
- tests T40eq/T50eq only for promotion;
- preserves original >=1% pooled log-loss / Brier / 4-of-6 fold / >=60% event-block / >=5-of-8 market / ECE gates.

Engine R and EXP-015 remain paused.

**Exact next action:** trigger exactly one EXP-041 Gate-B macro information-content run and resume from its durable result.


## 2026-09-27 — EXP-041 Gate-B run completed; integrity-only corrigendum required

Gate-B durable result commit: `13dc8bb2d93010ab30cc967e66df534a06a02f7c`.

The scientific model run completed, but v0.1 disposition is `INTEGRITY_FAIL_DO_NOT_INTERPRET` because one frozen integrity assertion required all 65 Gate-A events to have candidates.

Exact diagnosis:

- 63/65 Gate-A timestamps have structural candidates;
- missing timestamps are exactly 2025-12-10 19:00 UTC and 2026-01-28 19:00 UTC;
- both are FOMC;
- frozen decision grid ends 17:55 UTC;
- frozen pre-event window begins only 60 minutes before release, so a 19:00 FOMC cannot have any legal candidate without changing the frozen candidate grid;
- every other integrity condition passed.

This is a mechanical design contradiction, not a scientific model failure.

Frozen integrity-only corrigendum:

- spec checkpoint `2a583ac243ff649f069c320030dff2610182d5d9`;
- runner `8c22f18128f1738eb1cc2a54bb43215e549f7562`;
- workflow `996be120f13f538d05f20dcb945f93739871b639`.

The corrigendum does not rerun or alter Gate-B metrics. It only replaces the impossible 65/65 coverage assertion with coverage of every geometrically eligible frozen event, while requiring the two ineligible FOMC timestamps to match exactly.

**Exact next action:** trigger one Gate-B integrity corrigendum and resume from its durable result.


## 2026-09-27 — EXP-041 CLOSED: NO STABLE MACRO INFORMATION ADVANTAGE

Integrity corrigendum durable result: `57a622a1bcd9abf812e3d8baf07f444be7824ff0`.

Corrected integrity PASS:

- 63 geometrically eligible frozen events;
- exactly two ineligible events, both 19:00 UTC FOMC releases outside the unchanged EXP-040 decision grid;
- all 63 eligible events covered;
- all other original integrity checks passed;
- no scientific metric or model was recomputed.

Recovered scientific disposition:

`NO_STABLE_MACRO_INFORMATION_ADVANTAGE`.

Timing produced small pooled improvements but failed the predeclared stability gates. Surprise magnitude did not improve robustness and worsened Brier on both primary rungs.

EXP-041 is CLOSED. No macro-threshold tuning is authorized.

The governing next information family is **rates/USD market interpretation**, followed by execution-grade order flow.

A free source-feasibility path is now allowed for a prospectively frozen next experiment using new cross-asset instruments only; protected target-market periods remain sealed and Engine R/EXP-015 remain paused.


## 2026-09-27 — EXP-042 RATES/USD INTERPRETATION PROXY PREFLIGHT FROZEN

EXP-041 is closed with `NO_STABLE_MACRO_INFORMATION_ADVANTAGE`.

The next orthogonal information family is rates/USD market interpretation.

A zero-outcome EXP-042 data preflight is frozen before any model:

- spec commit: `8f2f63fcb40d3a84f18c48d87c5cbd183702baa6`;
- downloader commit: `82bc00a8244826fa9aaca5703a3c45c75bbb148c`;
- verifier commit: `10533a17bf7c4f35b318ce406edf09db40684c37`;
- workflow commit: `ffb80922dcd65a201ab420020e7b2d00aa0a7c3c`.

Frozen instruments:

- Dukascopy US Dollar Index CFD `dollaridxusd`;
- Dukascopy US T-Bond instrument `ustbondtrusd`.

These are proxies only. The T-Bond proxy is not treated as equivalent to 2Y/5Y Treasury futures, Fed-funds/SOFR expectations or order flow.

The workflow performs two independent full-development M1 downloads, requires byte-for-byte repeatability and integrity, then freezes an immutable GitHub Release only if both pass.

No target labels, model outcomes, P&L or protected Jul-Aug/Sep 2026 data are used.

**Exact next action:** trigger one EXP-042 rates/USD proxy repeatability snapshot. PASS => freeze the information-content study using the immutable proxy snapshot.


## 2026-09-27 — EXP-042 PROXY SNAPSHOT PASSED / EVENT-COVERAGE PREFLIGHT FROZEN

Durable proxy snapshot result: `16766ebbff9b9636a87f0236c209fb4028233773`.

Snapshot PASS:

- DOLLARIDXUSD: 273,175 rows, two copies byte-for-byte identical;
- USTBONDTRUSD: 144,445 rows, two copies byte-for-byte identical;
- both passed schema/coverage/monotonicity/OHLC integrity;
- immutable archive SHA-256: `86cef306c36f08a12510c563e307a3158dc45d3236a424251db4d1c1bbaedcb4`;
- release tag: `exp042-rates-usd-proxy-m1-2025-07-01_2026-06-30-v1`;
- no target labels/P&L/protected-period use.

Before outcome modeling, a zero-outcome proxy-event coverage audit is frozen:

- spec `9ea69bdd6f2cfd90cb7403ee70b098c3be69cc0b`;
- runner `9eb3c32fe81d8e77851642c6e9c63b0579262cd3`;
- workflow `03763015b3d45cd85df1670e5298dcee97681bb9`.

Frozen post-release geometry:

- Gate-A events: 65;
- post-release structurally eligible: 57;
- ineligible: exactly eight FOMC timestamps at 18:00/19:00 UTC outside the unchanged 06:05-17:55 decision grid;
- eligible counts by frozen fold: 10, 9, 10, 10, 9, 9.

The coverage audit requires causal pre-event baselines and fresh (<5m) proxy observations at legal structural decision timestamps, >=80% common coverage per eligible event, >=95% pooled common coverage and >=8 covered events per fold.

**Exact next action:** trigger one zero-outcome EXP-042 proxy-event coverage preflight. PASS => freeze EXP-042 rates/USD information-content study.


## 2026-09-27 — EXP-042 COVERAGE v0.1 FAILED / SOURCE-DRIVEN AVAILABILITY v0.3 FROZEN

Proxy-event coverage v0.1 durable result: `e9ddeb68c5a4b6fa2da2b1892892bafdb72b0d32`.

v0.1 FAIL was caused by real proxy availability gaps, not snapshot corruption:

- 57 post-release structurally eligible macro events;
- 51 events with strict common DXY+US-TBond coverage;
- pooled common decision-time coverage 89.18%;
- six eligible events fail common coverage because one proxy is inactive around release;
- no target-market bars, labels, P&L or protected periods were loaded.

v0.1 remains failed; its thresholds are not weakened.

An unexecuted v0.2 draft was superseded before run because it inferred single-proxy coverage from common coverage.

Final source-driven v0.3 is frozen:

- spec `c751ca2d4c27f2eb8ef584d75e1e18ed68eeadba`;
- runner `c45d17dcf9a77aef5e632bd95a1ae6c2134c2a4d`;
- workflow `5d3f81e93e5ca3a53fc134f9033ed28ed7857a05`.

v0.3 downloads the immutable proxy release, verifies file hashes, and independently recomputes causal <=5-minute baseline/decision-time freshness for each proxy.

It freezes two outcome-blind event universes:

- DXY_COMPLETE;
- DXY_TBOND_COMPLETE.

Each must satisfy the original Gate-A adequacy minima before modeling is authorized.

**Exact next action:** trigger one EXP-042 proxy availability v0.3 preflight.


## 2026-09-27 — EXP-042 AVAILABILITY v0.3 PASSED / INFORMATION-CONTENT STUDY FROZEN

Durable availability result: `2b322158e75d4c1d4722a3ac48f52e8ce5cddd20`.

Outcome-blind subsets passed the original adequacy minima:

- DXY_COMPLETE: 53 events;
  - CPI 10, Employment 10, GDP/PCE 14, PPI 11, Retail 12;
  - fold counts 9/9/10/9/7/9.
- DXY_TBOND_COMPLETE: 51 events;
  - CPI 10, Employment 9, GDP/PCE 14, PPI 10, Retail 12;
  - fold counts 8/9/10/9/6/9.

No target-market bars or labels were loaded by the availability audit.

EXP-042 information-content study is now frozen before outcomes:

- spec commit: `0ade215c8d373b4735d1d22c9400e3d50b98206f`;
- final runner commit: `6efb6902400cbaf058d0b0b12bc04a9d218e6692`;
- workflow commit: `5769360701745312b546ddb90e60ec45848719d0`.

Study A on DXY_COMPLETE:

`LOCAL_M5 + EVENT_TIME_CONTROL -> +DXY_REACTION`.

Study B on DXY_TBOND_COMPLETE:

`CONTROL -> +DXY -> +DXY+TBOND`.

A T-Bond layer passes only if the full DXY+T-Bond model passes the frozen information gate versus both DXY-only and control.

All proxy features use the last M1 close strictly before the structural decision timestamp. Focal event is the most recent prior frozen macro release within +180 minutes.

Primary rungs remain T40eq/T50eq and the original information-advantage thresholds are unchanged.

**Exact next action:** trigger one EXP-042 rates/USD information-content run and resume from its durable result.


## 2026-09-27 — EXP-042 CLOSED: NO STABLE DXY / TBOND INTERPRETATION ADVANTAGE

Durable information-content result: `1e4520b65af1de5cf2bccf6ee807700a349c9a40`.

Integrity PASS:

- immutable target and proxy archives verified;
- all target/proxy file hashes verified;
- frozen availability universes unchanged;
- all subset events had structural candidates;
- all outer/inner primary splits had both classes;
- all 8 markets had both primary classes;
- proxy features were strictly causal;
- Jul-Aug/Sep protected periods remained sealed;
- Engine R/EXP-015 outcomes were unused.

Scientific dispositions:

- Study A DXY: `NO_STABLE_DXY_REACTION_INFORMATION_ADVANTAGE`;
- Study B DXY+T-Bond: `NO_STABLE_DXY_TBOND_INTERPRETATION_ADVANTAGE`.

DXY Study A:

- T40eq relative log-loss change: -0.3606%;
- T50eq relative log-loss change: -0.2793%;
- Brier worsened on both;
- fold wins: 0/6 and 1/6;
- event-block win rates: 32.1% and 35.8%;
- market non-worse count: 1/8 on both.

DXY+T-Bond Study B versus DXY-only:

- T40eq relative log-loss change: -0.1346%;
- T50eq relative log-loss change: -0.1446%;
- Brier worsened on both;
- fold wins: 1/6 and 1/6;
- event-block win rates: 33.3% and 43.1%;
- market non-worse counts: 0/8 and 1/8.

DXY+T-Bond versus control was also negative on both primary rungs.

**Decision:** close EXP-042. Do not tune DXY/T-Bond reaction thresholds or windows on this development sample.

Next governing information family: execution-grade information / order-flow-like observables. Any next step must distinguish true bid/ask/tick participation information from another OHLC transform.


## 2026-09-27 — EXP-043 TICK/QUOTE MICROSTRUCTURE SOURCE PREFLIGHT FROZEN

EXP-042 is closed with no stable DXY or DXY+T-Bond information advantage.

The next orthogonal information family is execution-grade broker quote/tick microstructure.

Frozen EXP-043 zero-outcome source preflight:

- spec `afd3362ba22e1672ec2a76585004869ac05ea3d6`;
- downloader `aa9c05510172cfeec8f0ef8dea701b502d7be233`;
- verifier `62ce3de6548ab5059cd273521dcdbd987560893a`;
- workflow `eb3e9b60493d283af4e3d75f5c82ac6a8ea32cea`.

The pinned Dukascopy tick transport exposes timestamp, ask price, bid price, ask volume and bid volume. EXP-043 treats these only as broker quote/tick microstructure:

- spread;
- quote-update intensity;
- quote-side size/imbalance.

It does **not** label them centralized trade aggressor flow or exchange order-book depth.

The pilot uses six fixed development dates spanning Jul-2025 to May-2026 across all eight target markets, performs two independent downloads, and requires exact canonical SHA equality for all 48 symbol/date pairs.

No target labels, models, P&L or protected Jul-Aug/Sep 2026 data are used.

**Exact next action:** trigger one EXP-043 tick microstructure source preflight. PASS => freeze a development-only acquisition design before any predictive study.


## 2026-09-27 — EXP-043 TICK SOURCE PREFLIGHT PASSED

Durable preflight result: `babcfa8178ebf9288cefc420dab916674a59b55b`.

Result:

- 48/48 symbol/date pairs passed semantic integrity;
- 48/48 independent copy pairs had identical row counts;
- 48/48 independent copy pairs had identical canonical SHA-256;
- all bid/ask prices positive;
- ask >= bid throughout;
- quote-side volumes nonnegative with positive observations;
- millisecond timestamps valid and nondecreasing;
- no target labels/P&L/protected periods used;
- disposition: `EXP043_DUKASCOPY_TICK_MICROSTRUCTURE_SOURCE_REPEATABLE`.

The six-date pilot contained ~4.99 million ticks per copy. XAUUSD alone ranged from ~164k to ~401k ticks/day in the frozen pilot.

**Decision:** do not store a full year of raw tick CSVs. Freeze a deterministic minute-level microstructure snapshot while retaining per-day raw canonical hashes and tick counts for provenance.

The snapshot must preserve execution/participation observables unavailable in OHLC: spread state, quote-update intensity, inter-arrival activity, quote freshness and quote-side imbalance. It must not introduce another generic price-return feature family.


## 2026-09-27 — EXP-043 FULL DEVELOPMENT MICROSTRUCTURE SNAPSHOT FROZEN

Following the exact source-repeatability PASS, the full development snapshot is frozen:

- snapshot spec: `8b0d5e506643c730891d15e42e332048ba7c97fd`;
- acquisition/aggregation code: `3910048bccc142afcf61184d34492538c897d4f1`;
- integrity verifier: `372607f7b6fb0acdb57b3c5ba50742f401634e72`;
- workflow: `fe9111c402a02f34e834e74c0d66762766c5c969`.

Frozen acquisition:

- all 8 target markets;
- weekdays only;
- 2025-07-01 <= date < 2026-06-30;
- 05:00-18:00 UTC tick window;
- pinned `dukascopy-node@1.50.0`.

Raw ticks remain transient. Every source day retains canonical raw tick SHA/count/timestamps in the manifest.

Frozen minute-level data deliberately excludes mid-price OHLC/return fields and preserves only genuinely new execution/participation observables:

- spread bps state;
- tick count and distinct update timestamps;
- inter-arrival timing;
- quote freshness;
- bid/ask price update counts;
- bid/ask quote-side volume medians;
- signed quote-side imbalance and persistence fractions.

PASS freezes immutable release tag:

`exp043-quote-microstructure-1m-2025-07-01_2026-06-30-v1`.

No EXP-043 target/path outcomes are computed during acquisition.

**Exact next action:** trigger exactly one EXP-043 development microstructure snapshot acquisition and resume from its durable checkpoint.


## 2026-09-27 — EXP-043 DEVELOPMENT MICROSTRUCTURE SNAPSHOT PASSED

Durable snapshot result: `ba908a721a131b6062ebcc107ddab5a3e4c01285`.

Snapshot PASS:

- immutable release tag: `exp043-quote-microstructure-1m-2025-07-01_2026-06-30-v1`;
- archive SHA-256: `f95edf1f7762271941a1d24b3204c4640485d9e7b9b01440fbef86f521f52ca5`;
- manifest SHA-256: `887a41cb90b5350764eed5cb69399bc9e146d13fb12a3f9d194d4ad3abfbc2ef`;
- all 8 market aggregate files passed integrity;
- requested weekdays: 260;
- 257-259 positive source days per market;
- no target labels, scientific outcomes, P&L or protected periods were used.

The stored minute layer contains only execution/participation observables: spread, tick/update intensity, inter-arrival timing, quote freshness and quote-side imbalance. No mid-price OHLC/return fields were stored.

The project is now authorized to freeze one development-only EXP-043 information-content study on the immutable microstructure snapshot.
