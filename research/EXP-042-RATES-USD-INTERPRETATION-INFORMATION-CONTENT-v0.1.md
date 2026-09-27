# EXP-042 Rates/USD Interpretation Information-Content Study v0.1

**Frozen:** 2026-09-27, before EXP-042 target outcomes  
**Authorized by:** proxy availability v0.3 durable result `2b322158e75d4c1d4722a3ac48f52e8ce5cddd20`  
**Availability result Git blob:** `d6fe91ff1136b57fa4a7e92a5ddf1bfc7608d0a1`

## 1. Objective

Test whether **post-release market interpretation** in the USD index and US T-Bond proxy adds stable predictive information beyond the local structural baseline and event-time controls.

This is not a strategy engine.

## 2. Frozen inputs

Target-market development data:

- immutable Dukascopy v2 release;
- tag `exp041-data-dukas-m1-2025-07-01_2026-06-30-v2`;
- archive SHA-256 `90bc7301e459062e8e35cd89a1a9aac23332ca3472014dd2cc5045ba34794272`.

Proxy data:

- tag `exp042-rates-usd-proxy-m1-2025-07-01_2026-06-30-v1`;
- archive SHA-256 `86cef306c36f08a12510c563e307a3158dc45d3236a424251db4d1c1bbaedcb4`;
- DOLLARIDXUSD file SHA-256 `2f070a99784a60f15e9afe5cb1c906f1ded22aedaa74205cd3a286adefb839d2`;
- USTBONDTRUSD file SHA-256 `e1ff7bea80f40b1529e046a7b0f7b4c6265cc147ee8c6c324ddef05cc7c5acf7`.

Availability universes come only from:

`research/results/EXP-042-proxy-availability-stratified-preflight-v0.3.json`.

Frozen sizes:

- DXY_COMPLETE = 53 events;
- DXY_TBOND_COMPLETE = 51 events.

## 3. Structural candidate and target mechanics

Reuse the exact EXP-040 machinery from `mtf_information_v0_1.py`:

- same 8 target markets;
- completed M5 decision grid;
- weekdays;
- 06:05-17:55 UTC;
- long and short independently;
- latest confirmed 2-left/2-right M5 pivot within prior 12 M5 bars;
- one research tick beyond pivot for stop;
- first active M1 open at/after decision;
- same-date entry before 18:00 UTC;
- 120 active-M1-bar target horizon;
- hard 20:00 UTC cutoff;
- same-bar stop+target = stop first.

Primary rungs only:

- T40eq = 2.0R;
- T50eq = 2.5R.

## 4. Focal-event assignment

EXP-042 is strictly post-release.

For every structural candidate, choose the **most recent frozen structurally eligible macro event** satisfying:

`event_ts <= decision_ts <= event_ts + 180 minutes`.

If no such event exists, exclude the candidate.

A later event always supersedes an earlier overlapping event.

Only after this focal event is assigned may availability-subset membership be tested.

This prevents a candidate after an unavailable newer release from being assigned to an older release.

## 5. Causal proxy feature timing

For each proxy:

- event baseline = last M1 close strictly before focal event timestamp;
- current proxy value = last M1 close strictly before structural decision timestamp.

A proxy bar timestamp equal to the structural decision timestamp is prohibited.

Availability must independently satisfy the v0.3 <=5-minute freshness rule.

## 6. Event-time control features

Every study baseline contains:

- LOCAL_M5 features;
- minutes since event, clipped to [0,180];
- event-family multi-hot:
  - EMPLOYMENT;
  - CPI;
  - PPI;
  - RETAIL;
  - GDP_PCE.

FOMC is absent from these post-release universes because all eight FOMC events are outside the frozen structural decision geometry.

No macro surprise feature from EXP-041 is used.

## 7. Proxy reaction features

### DXY reaction

Using baseline and causal current close:

`dxy_log_return_bps = 10000 * log(current / baseline)`

Also include:

`dxy_abs_log_return_bps = abs(dxy_log_return_bps)`.

No thresholding and no sign hand-coding by target market.

### US T-Bond reaction

Analogously:

- `tbond_log_return_bps`;
- `tbond_abs_log_return_bps`.

No proxy volume feature is authorized.

## 8. Study A — DXY information

Universe: exact DXY_COMPLETE 53-event list.

Paired feature sets:

1. `A_CONTROL = LOCAL_M5 + EVENT_TIME_CONTROL`;
2. `A_PLUS_DXY = A_CONTROL + DXY_REACTION`.

Both feature sets use exactly the same candidate rows.

## 9. Study B — DXY + T-Bond interpretation

Universe: exact DXY_TBOND_COMPLETE 51-event list.

Nested feature sets:

1. `B_CONTROL = LOCAL_M5 + EVENT_TIME_CONTROL`;
2. `B_PLUS_DXY = B_CONTROL + DXY_REACTION`;
3. `B_PLUS_DXY_TBOND = B_PLUS_DXY + TBOND_REACTION`.

All three use exactly the same candidate rows.

A T-Bond interpretation layer is considered validated only if the full set passes the frozen information gate:

- versus `B_PLUS_DXY`; and
- versus `B_CONTROL`.

This prevents a claim of rates value merely by repairing a harmful DXY baseline.

## 10. Learner and calibration

Same fixed learner family as EXP-040/041:

Base:

- StandardScaler;
- LogisticRegression;
- C=0.25;
- L2;
- lbfgs;
- max_iter=1000;
- random_state=20260925.

Platt calibration:

- LogisticRegression;
- C=1,000,000;
- lbfgs;
- max_iter=1000.

No hyperparameter search.

## 11. Frozen folds

Use the original Gate-A fold number attached to each event.

For each study, outer evaluation uses the six frozen fold numbers after availability filtering.

For each outer fold:

1. evaluation = study rows whose focal event is in that fold;
2. training = rows from the other five fold numbers;
3. build raw inner OOF probabilities by holding out each of those five training folds in turn;
4. fit Platt only on inner OOF predictions;
5. refit base learner on all five outer-training folds;
6. predict untouched outer fold;
7. apply prefit Platt.

No event timestamp appears in its own training/calibration data.

## 12. Metrics

For each feature set / T40eq / T50eq:

- pooled log loss;
- Brier;
- ROC AUC diagnostic;
- 10-bin ECE;
- six fold metrics;
- per-market metrics;
- per-event mean log loss.

## 13. Frozen information-advantage gate

For both T40eq and T50eq, enriched must satisfy versus its baseline:

1. >=1.0% relative pooled log-loss improvement;
2. lower pooled Brier;
3. log-loss win in >=4/6 frozen fold numbers;
4. win on >=60% evaluated event blocks;
5. per-market pooled log loss non-worse in >=5/8 markets;
6. ECE not worse by >0.01.

Study A passes only if A_PLUS_DXY passes both primary rungs versus A_CONTROL.

Study B passes only if B_PLUS_DXY_TBOND passes both primary rungs versus BOTH:
- B_PLUS_DXY;
- B_CONTROL.

No secondary target rung may rescue failure.

## 14. Integrity gate

Require:

- exact immutable target archive SHA;
- all eight target-market file SHAs verified;
- exact immutable proxy archive SHA;
- exact DXY/T-Bond file SHAs;
- availability v0.3 Git blob unchanged;
- exact DXY_COMPLETE event list size 53;
- exact DXY_TBOND_COMPLETE size 51;
- every study event has at least one broad structural candidate;
- every outer evaluation fold has both classes for T40 and T50;
- every inner calibration split has both classes;
- every market has both classes in pooled OOF evaluation;
- all proxy features use timestamps strictly before decision;
- no target/proxy data at or after 2026-06-30;
- Jul-Aug/Sep 2026 sealed;
- Engine R / EXP-015 outcomes unused.

If integrity fails, disposition is `INTEGRITY_FAIL_DO_NOT_INTERPRET`.

## 15. Scientific dispositions

Possible independent study results:

- `STABLE_DXY_REACTION_INFORMATION_ADVANTAGE_FOUND`;
- `NO_STABLE_DXY_REACTION_INFORMATION_ADVANTAGE`;
- `STABLE_DXY_TBOND_INTERPRETATION_ADVANTAGE_FOUND`;
- `NO_STABLE_DXY_TBOND_INTERPRETATION_ADVANTAGE`.

No result by itself authorizes strategy construction.

If neither study passes, close this free rates/USD proxy layer and proceed to execution-grade order flow or a higher-quality institutional rates source rather than tuning proxy thresholds.
