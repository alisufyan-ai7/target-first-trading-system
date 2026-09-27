# EXP-041 Gate B — Macro / Catalyst Information-Content Study v0.1

**Frozen:** 2026-09-27 — before Gate-B market outcomes  
**Authorized by Gate A:** durable result `4208af07c148a5d37c61cbbbeb004b83fec14af5`  
**Type:** information-content research, not a strategy engine  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed

## 1. Objective

Test whether scheduled U.S. macro catalyst information adds stable predictive information beyond the frozen `LOCAL_M5` structural baseline.

The comparison is:

1. `LOCAL_M5`;
2. `PLUS_CATALYST_TIMING`;
3. `PLUS_SURPRISE_MAGNITUDE`.

No entry filter, target optimization, position sizing, P&L rule, or strategy promotion is introduced.

## 2. Market-data input

Use only the immutable EXP-041 Dukascopy development release:

- tag: `exp041-data-dukas-m1-2025-07-01_2026-06-30-v2`;
- archive SHA-256: `90bc7301e459062e8e35cd89a1a9aac23332ca3472014dd2cc5045ba34794272`;
- effective interval:
  `2025-07-01T00:00:00Z <= t < 2026-06-30T00:00:00Z`.

The runner must verify the archive and every market file against the durable snapshot result before parsing.

No live Dukascopy re-download is permitted.

## 3. Structural candidate / target labels

Reuse the exact EXP-040 mechanics from:

`research/code/mtf_information_v0_1.py`

Candidate universe:

- same eight markets;
- completed M5 bars;
- weekdays;
- 06:05 through 17:55 UTC;
- long and short independently;
- latest confirmed 2-left/2-right M5 pivot within prior 12 M5 bars;
- one research tick beyond pivot for structural stop;
- first active M1 open at/after decision;
- same-date entry before 18:00 UTC;
- no strategy-pattern filter.

Target/path definitions remain:

- T30eq = 1.5R;
- T40eq = 2.0R;
- T50eq = 2.5R;
- T70eq = 3.5R;
- T100eq = 5.0R;
- 120 active-M1-bar horizon;
- hard 20:00 UTC cutoff;
- same-bar stop + target = stop first.

Primary Gate-B rungs remain only:

- T40eq;
- T50eq.

The richer EXP-040 MTF feature sets are **not** used because EXP-040 found no stable incremental MTF advantage.

## 4. Macro input

Use only:

`research/data/EXP-041-official-macro-surprise-layer-v0.1.json`

Expected SHA-256:

`ec267643940733db4647d5d1dc5537099e3fc149ee7e0e9257b1b8786017c362`

The 65 independent timestamp blocks and six chronological fold memberships come only from:

`research/results/EXP-041-final-gate-a-audit-v0.1.json`

Gate-B may not redraw event folds.

## 5. Candidate-event window

Evaluate only structural candidates whose decision timestamp is within:

`[-60 minutes, +180 minutes]`

of at least one frozen independent macro timestamp.

If windows overlap, choose one **focal event** deterministically:

1. smallest absolute time distance;
2. on an exact distance tie, prefer the already-released/past event;
3. then earlier timestamp.

This focal event determines phase, event-family indicators and surprise features.

Every frozen event timestamp remains assigned to its Gate-A fold.

## 6. Timing information set

`PLUS_CATALYST_TIMING` = `LOCAL_M5` plus:

- minutes to next frozen event, clipped to [0,60];
- minutes since last frozen event, clipped to [0,180];
- pre-event 0-60m flag;
- post-event 0-15m flag;
- post-event 15-60m flag;
- post-event 60-180m flag;
- surprise-known flag;
- focal-event family multi-hot:
  - EMPLOYMENT;
  - CPI;
  - PPI;
  - RETAIL;
  - GDP_PCE;
  - FOMC.

When several families share the same official timestamp, all corresponding family indicators are 1.

## 7. Surprise magnitude information set

`PLUS_SURPRISE_MAGNITUDE` = timing set plus the package-level surprise diagnostics frozen in EXP-041:

- mean absolute scaled surprise;
- maximum absolute scaled surprise;
- number of available canonical surprise components;
- conflict flag when available signed surprises contain both positive and negative values.

Before the focal release timestamp all four surprise diagnostics are zero.

FOMC v0.1 remains timing-only, so its surprise component count is zero.

Frozen ex-ante component scales:

- NFP / employment change: 50,000 persons;
- unemployment / earnings / CPI / PPI / PCE / personal income / personal spending rates: 0.1 percentage point;
- Retail Sales: 0.5 percentage point;
- GDP annualized growth: 0.5 percentage point.

For each numeric canonical record:

`scaled_surprise = (official_actual - frozen_forecast) / fixed_scale`.

No outcome-dependent sign interpretation is introduced.

## 8. Learner

To isolate information content, use the same primary learner family as EXP-040:

- StandardScaler;
- LogisticRegression;
- C = 0.25;
- L2;
- lbfgs;
- max_iter = 1000;
- random_state = 20260925.

Platt calibration:

- LogisticRegression;
- C = 1,000,000;
- lbfgs;
- max_iter = 1000.

No hyperparameter search.

## 9. Six grouped out-of-fold evaluations

The six frozen Gate-A event folds are the outer holdouts.

For each outer fold, feature set and primary rung:

1. outer evaluation rows = candidates whose focal event is in that fold;
2. outer training rows = candidates from the other five frozen event folds;
3. create raw out-of-fold probabilities inside those five training folds:
   - hold one training event fold out;
   - fit on the other four;
   - predict the held training fold;
   - repeat for all five;
4. fit the Platt calibrator on those inner out-of-fold raw probabilities only;
5. refit the base model on all five outer-training folds;
6. predict the untouched outer evaluation fold;
7. apply the prefit Platt calibrator.

Thus every pooled Gate-B prediction is out-of-fold with respect to its entire independent event fold.

This is a development-only grouped information-content screen, not a live-forward performance estimate.

## 10. Metrics

For each feature set / rung:

- pooled log loss;
- pooled Brier;
- ROC AUC diagnostic;
- 10-bin ECE;
- six outer-fold metrics;
- per-market metrics.

For every independent event timestamp with evaluation candidates:

- mean candidate log loss for LOCAL_M5;
- mean candidate log loss for each enriched set;
- baseline-minus-enriched event-block delta;
- block win when delta > 0.

Also report evaluated-event coverage by frozen fold and market.

## 11. Frozen information-advantage gate

For **both** T40eq and T50eq, an enriched set must satisfy versus LOCAL_M5:

1. >=1.0% relative pooled log-loss improvement;
2. lower pooled Brier;
3. log-loss win in >=4 of 6 frozen folds;
4. win on >=60% of evaluated independent event blocks;
5. per-market pooled log loss non-worse in >=5 of 8 markets;
6. ECE not worse by >0.01.

If both enriched sets pass, select the smallest:

`PLUS_CATALYST_TIMING -> PLUS_SURPRISE_MAGNITUDE`.

T30eq/T70eq/T100eq cannot rescue failure.

## 12. Integrity gate

Before interpretation require:

- exact Dukascopy release/archive hash;
- all eight market file hashes/integrity verified;
- exact macro surprise-layer hash;
- final Gate-A PASS;
- exact frozen 65 event timestamps and six fold assignments used;
- all 65 frozen event timestamps have at least one structural candidate in the allowed window;
- every primary-rung outer evaluation fold has both classes;
- every primary-rung inner calibration construction has both classes;
- every market has both primary-rung classes in pooled OOF evaluation;
- candidate labels never use data at/after 2026-06-30;
- Jul-Aug/Sep 2026 never loaded/labeled;
- Engine R / EXP-015 outcomes not used.

## 13. Dispositions

If timing passes:

`STABLE_MACRO_TIMING_INFORMATION_ADVANTAGE_FOUND`.

If timing fails but surprise magnitude passes:

`STABLE_MACRO_SURPRISE_INFORMATION_ADVANTAGE_FOUND`.

If neither passes:

`NO_STABLE_MACRO_INFORMATION_ADVANTAGE`.

If integrity fails:

`INTEGRITY_FAIL_DO_NOT_INTERPRET`.

A passing information layer is preserved as future candidate information only. It does not itself authorize a strategy, Engine R, P&L promotion, or protected-period use.

## 14. Scientific next step after result

- If neither macro set passes: do not tune macro thresholds; move to the next genuinely new information family (rates/USD reaction or execution/order-flow).
- If a macro set passes: preserve the smallest passing layer and test the next orthogonal information family before strategy construction.

Engine R remains paused.
