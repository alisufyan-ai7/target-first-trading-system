# EXP-040 — Multi-Timeframe Structural Context Information-Content Study v0.1

**Status:** PROSPECTIVELY FROZEN — BEFORE EXP-040 OUTCOMES  
**Date:** 2026-09-25  
**Type:** INFORMATION-CONTENT RESEARCH, NOT A STRATEGY ENGINE  
**Provenance:** `research/provenance/EXP-040-mtf-context-source-manifest.md`

## 1. Purpose

Test whether higher-timeframe structural/location context adds stable predictive information beyond local M5 price state.

This experiment does **not** ask which entry setup makes money.

It asks:

> for the same broad causal structural candidate universe, do 15M / 1H / 4H / prior-day / session-location features improve out-of-sample target-before-stop probability relative to M5-local information alone?

No strategy family is promoted by this experiment.

## 2. Candidate universe

Markets:

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

Decision grid:

- completed M5 bars;
- weekdays;
- 06:05 through 17:55 UTC;
- every five minutes.

For each market and each direction independently:

1. use latest causally confirmed 2-left/2-right M5 pivot within the prior 12 M5 bars as structural invalidation;
2. one research tick beyond the pivot;
3. entry = first active M1 open at/after the completed M5 decision;
4. require same UTC date and entry before 18:00 UTC;
5. no strategy-pattern filter is applied.

This is a broad structural candidate universe, not an execution engine.

## 3. Diagnostic target/path ladder

This study intentionally separates **information content** from production lot sizing.

For structural stop distance `R = abs(entry-stop)`, label target-first events at:

- T30eq = 1.5R;
- T40eq = 2.0R;
- T50eq = 2.5R;
- T70eq = 3.5R;
- T100eq = 5.0R.

The names are reference-risk diagnostics only: if structural risk were normalized to USD20, these gross multiples correspond to USD30/40/50/70/100.

They are **not** production target-distance rules and do not override `docs/PNL-EQUIVALENT-SIZING.md`.

Outcome path:

- max 120 active M1 bars counting entry bar;
- hard 20:00 UTC session cutoff;
- same-bar stop + target = stop first;
- once a stop occurs, no target touched on that same M1 bar is credited;
- MFE/MAE in structural-R units are recorded descriptively.

No position sizing or account P&L is used to choose feature families.

## 4. Protected source / split

Hard source seal:

- reusable source begins 2026-03-23;
- no row at or after 2026-07-01 00:00 UTC may be parsed into EXP-040;
- Jul-Aug secondary remains sealed;
- Sep final holdout remains sealed.

Six chronological evaluation folds:

- WF1 eval [2026-04-13, 2026-04-27)
- WF2 eval [2026-04-27, 2026-05-11)
- WF3 eval [2026-05-11, 2026-05-25)
- WF4 eval [2026-05-25, 2026-06-08)
- WF5 eval [2026-06-08, 2026-06-22)
- WF6 eval [2026-06-22, 2026-07-01)

For every fold:

- fit uses all available development rows from 2026-03-23 up to the fold's seven-day calibration window;
- calibration uses the seven calendar days immediately before evaluation;
- a **120-minute purge** is applied before calibration start and before evaluation start so labels from the preceding segment cannot cross the boundary.

## 5. Frozen nested information sets

All models receive market identity, direction, weekday and cyclic UTC time.

### A — LOCAL_M5

Only local M5 state:

- directional 5m / 15m / 30m moves;
- local EMA relationship/slope;
- current M5 range versus local median range;
- short-window compression/expansion;
- current body / directional close location;
- recent directional body balance;
- structural stop distance normalized by M5 volatility.

No completed 15M/1H/4H/Daily bar features.

### B — PLUS_M15

A plus causal completed-15M context:

- directional 15m / 30m / 60m moves;
- 15M EMA relationship/slope;
- 15M range state;
- directional position inside recent completed-15M structure.

### C — PLUS_H1

B plus causal completed-1H context:

- directional 1h / 3h / 6h moves;
- 1H EMA relationship;
- 1H range state;
- directional position inside recent 6h / 12h structure.

### D — PLUS_H4_D1

C plus causal completed-4H and previous-trading-day location:

- directional 4h / 8h / 12h moves;
- 4H EMA relationship;
- directional position inside recent completed-4H structure;
- distance/position relative to previous completed UTC trading-day high/low and close.

### E — PLUS_SESSION

D plus session-location state:

- completed Asia-proxy range 00:00-06:00 UTC, when available;
- completed London-proxy range 07:00-12:00 UTC, when available;
- directional distance/position relative to those completed ranges;
- explicit availability indicators.

These fixed UTC ranges are research proxies, not claims about optimal local-session definitions.

## 6. Frozen learner

Primary learner for information comparison:

- StandardScaler;
- LogisticRegression;
- C = 0.25;
- L2 penalty;
- lbfgs;
- max_iter = 1000;
- random_state = 20260925.

For each fold / feature set / target rung:

1. fit base logistic model on fit rows;
2. obtain fit/calibration probabilities;
3. fit one-dimensional Platt calibrator on the calibration window using clipped logit(base probability);
4. evaluate calibrated probability on the untouched chronological evaluation slice.

No hyperparameter search.

## 7. Primary metrics

For every feature set / target / fold:

- Brier score;
- log loss;
- ROC AUC (secondary);
- calibration bins / expected calibration error;
- sample count / positive rate.

Also pool all untouched evaluation predictions across the six folds and report:

- pooled metrics;
- per-market metrics;
- fold-by-fold metric differences versus LOCAL_M5.

## 8. Frozen information-advantage gate

Primary rungs:

- T40eq = 2.0R;
- T50eq = 2.5R.

An enriched feature set B/C/D/E is considered to show **stable incremental MTF information** only if, for **both** primary rungs:

1. pooled log loss improves by at least **1.0% relative** versus LOCAL_M5;
2. pooled Brier score is lower than LOCAL_M5;
3. log loss beats LOCAL_M5 in at least **4 of 6 folds**;
4. pooled expected calibration error is not worse than LOCAL_M5 by more than 0.01;
5. pooled per-market log loss is no worse than LOCAL_M5 in at least **5 of 8 markets**.

If multiple nested sets pass, select the **smallest/earliest** passing set:

`PLUS_M15 -> PLUS_H1 -> PLUS_H4_D1 -> PLUS_SESSION`.

This parsimony rule is frozen before results.

T30eq/T70eq/T100eq are secondary diagnostics and cannot rescue failure on T40eq/T50eq.

## 9. Integrity / sample gate

Before interpreting information metrics require:

- every market-direction combination >=500 labeled development candidates;
- every evaluation fold contains both classes for T40eq and T50eq;
- no protected-period row is loaded/labeled;
- exact feature-set nesting passes tests;
- all higher-timeframe features are based on bars completed before the decision;
- previous-day/session levels are causal;
- no target/P&L result from Engine R is used.

## 10. Disposition rules

If no enriched set passes:

`NO_STABLE_MTF_INFORMATION_ADVANTAGE`.

Consequence:

- do not build a strategy merely from MTF context;
- proceed to the next information family: macro/catalyst.

If one or more enriched sets pass:

`STABLE_MTF_INFORMATION_ADVANTAGE_FOUND`.

Consequence:

- preserve the smallest passing context set as a future candidate information layer;
- **do not** yet build/promote a strategy;
- proceed to macro/catalyst information testing and ask whether it adds further incremental value.

## 11. Anti-mining

After EXP-040 outcomes do not alter inside v0.1:

- candidate grid;
- structural stop convention;
- target-R ladder;
- 120m horizon;
- feature definitions;
- model C;
- fold boundaries;
- purge duration;
- gate thresholds;
- primary rungs.

Any redesign requires a new experiment/version.

## 12. Engine R / protected periods

Engine R / EXP-039 remains paused before target/P&L development.

EXP-040 must not load July-August or September.

## Exact next action

Implement the frozen feature/label pipeline and run one development-only EXP-040 workflow.


## Implementation checkpoint — frozen before EXP-040 outcomes

Implementation is now frozen before any EXP-040 target/path labels are produced by CI:

- feature/label module commit: `3e44de11d1b0386fd4abf005c34757f9498e4c68`;
- runner commit: `107cf3091d67dd708e227c25b37d036d9fd24566`;
- workflow commit: `d5e41a009f03bc8100cf40f281f73890c6fc3752`;
- feature module blob: `70ecae5eb94bf5fdc4325cdf1a29e33d20bf0cd4`;
- runner blob: `3d062de2cb6f7e21680bf3fd6253242ae55f4fd6`;
- workflow blob: `c1be21397ebd3dda168d143c8f8300011885fe54`.

The workflow will treat either scientific disposition as a valid research result. CI fails only on operational/integrity failure or protected-period leakage; `NO_STABLE_MTF_INFORMATION_ADVANTAGE` is not a pipeline failure.

At this checkpoint:

- EXP-040 outcome labels generated by the workflow: **NO**;
- Jul-Aug loaded/labeled: **NO**;
- September loaded/labeled: **NO**;
- Engine R target/P&L development: **PAUSED**.

**Next:** trigger exactly one EXP-040 development-only information-content run.


## Final EXP-040 result — NO STABLE MTF INFORMATION ADVANTAGE

**Durable result commit:** `46049f7d94131db50e7d9cbb13a3fa82dcafb810`  
**Tested repository SHA:** `cea178f42cb94a1311a65c2d56ea8667ca05e340`  
**Result file:** `research/results/EXP-040-mtf-structural-context-information-content-v0.1.json`

Operational note:

- the original workflow run encountered an integrity-boolean implementation issue after producing a result;
- the integrity logic was corrected prospectively without changing the frozen scientific feature sets, targets, folds, model, or gates;
- rerun workflow `36149076144` completed **SUCCESS** and produced the durable result above.

Scientific result:

- candidate rows: **123,724**;
- pooled evaluation predictions per primary rung: **99,622**;
- integrity gate: **PASS**;
- Jun30 source seal: **PASS**;
- Jul-Aug loaded/labeled: **NO**;
- Sep loaded/labeled: **NO**;
- Engine-R target/P&L development used: **NO**;
- passing enriched feature sets: **NONE**;
- disposition: `NO_STABLE_MTF_INFORMATION_ADVANTAGE`.

Primary pooled baseline:

- LOCAL_M5 T40eq log loss **0.493874**, Brier **0.161613**, AUC **0.6634**;
- LOCAL_M5 T50eq log loss **0.412801**, Brier **0.129229**, AUC **0.6929**.

Every richer nested context set failed the frozen T40eq/T50eq information-advantage gate:

- +15M slightly worsened pooled log loss/Brier and won only 1/6 folds on T40eq and 2/6 on T50eq;
- +1H worsened pooled log loss/Brier and won only 2/6 and 3/6 folds;
- +4H/prior-day worsened pooled metrics further;
- +session context worsened pooled metrics most and was not non-worse in any of 8 markets on the primary pooled market comparison.

Interpretation:

- generic higher-timeframe OHLC context, as frozen here, does **not** provide stable incremental predictive information beyond the local-M5 baseline for the broad structural candidate universe;
- this does not prove that all discretionary higher-timeframe context is useless;
- it does show that simply adding generic 15M/1H/4H/prior-day/session OHLC features is not the missing information advantage we are seeking;
- therefore do not build/promote another MTF-OHLC strategy from this result.

**Next research action:** proceed to the next genuinely new information family: macro/catalyst information-content research. Protected periods remain sealed.
