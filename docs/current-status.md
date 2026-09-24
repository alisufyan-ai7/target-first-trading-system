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
