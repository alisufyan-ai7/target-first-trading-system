# Engine K v0.3 — Market-Aware Calibrated Stress-EV Scanner

**Engine ID:** engine-k-direct-target-move-scanner  
**Version:** 0.3  
**Experiment:** EXP-024  
**Status:** FROZEN PROSPECTIVELY BEFORE V0.3 METRICS — 2026-09-24

## 1. Why v0.3 exists

Engine K v0.2 fixed the v0.1 cross-market economic-admission failure: all eight execution markets produced ample admissible states.

However v0.2 failed its frozen pre-secondary gate because its fixed qualification rule `max(0.50, p_break_even + 0.10)` produced only two qualified combined trades and zero June trades.

At the same time, the frozen June discrimination diagnostics were non-random:

- T30 AUC ~0.674;
- T40 AUC ~0.710;
- T50 AUC ~0.743.

July-August and September remain unopened.

v0.3 does **not** lower the v0.2 threshold in place. It freezes a new evaluation/calibration design and replaces arbitrary probability floors with a directly economic stress-EV qualification rule.

## 2. What remains unchanged

From v0.2:

- execution markets: XAUUSD, EURUSD, GBPUSD, USDJPY, EURJPY, AUDUSD, USDCAD, USDCHF;
- forecast-only markets remain excluded;
- complete 5m decision bars;
- next-active M1 entry <=5 chronological minutes;
- strict causal 2-left/2-right structural pivot stop;
- USD20 structural-stop risk cap;
- USD50,000 notional cap / 100x equity;
- USD100 research margin cap at 1:500 reference;
- primary cost = 10% of actual gross target;
- stress cost = 20% of actual gross target;
- Gold +3/+4/+5 XAU target ladder at 0.10 lot;
- non-Gold 1.5R / 2.0R / 2.5R target-before-size ladder;
- downward 0.01-lot equivalent sizing;
- same 29 causal features;
- same HGB hyperparameters;
- same 120-active-M1 / 20:00 UTC label horizon;
- same stop-first ambiguity rule;
- same one-open portfolio state machine;
- no forced trades.

## 3. Development evidence status

Mar23-Jun30 is now a **reusable inspected development pool**, not pristine evidence.

Protected evidence still sealed:

- secondary test: Jul1-Aug31 2026;
- final holdout: Sep1-Sep22 2026.

v0.3 may be redesigned using inspected Mar-Jun evidence, but no July-Sep state/outcome information may enter design or gating.

## 4. Clean internal chronology

v0.3 changes the internal development chronology to avoid using the same month for both probability calibration and strategy gating.

### Model fit

- Mar23-Apr30 2026 only.

### Probability calibration

- May1-May31 2026 only.

### Development gate

- Jun1-Jun30 2026 only.

June is not used to fit HGB or the v0.3 gate-time calibrator.

If and only if the June gate passes, a secondary-test bundle may then be refit prospectively as:

- HGB fit: Mar23-May31;
- calibrator: June;
- secondary evaluation: Jul-Aug.

This refit rule is frozen before v0.3 June metrics.

## 5. Primary model

Per rung T30/T40/T50:

`HistGradientBoostingClassifier`

Frozen parameters unchanged:

- learning_rate=0.05;
- max_iter=150;
- max_leaf_nodes=15;
- min_samples_leaf=100;
- l2_regularization=1.0;
- random_state=20260923.

The same encoded 29-feature + market/direction input contract is used.

## 6. Market-direction-aware probability calibration

v0.2 used a single pooled Platt transform per rung.

v0.3 uses one prospectively frozen **market-direction-aware Platt calibrator per rung**.

Calibration model:

`LogisticRegression(C=1_000_000, solver=lbfgs, max_iter=1000)`

Inputs on May only:

1. clipped logit of raw HGB probability;
2. one-hot market identity for all 8 execution markets;
3. one-hot direction long/short.

This allows base-rate adjustment by market/direction while keeping a single monotonic raw-probability slope.

No target-distance/rung-specific outcome feature beyond the separate per-rung calibrator is added.

## 7. v0.3 qualification rule

No universal 50% or 60% probability floor.

For each candidate/rung:

Primary EV:

`EV_primary = p*G - (1-p)*R - C_primary`

Stress EV:

`EV_stress = p*G - (1-p)*R - C_stress`

where:

- `p` = May-calibrated target-first probability;
- `G` = actual rounded-lot gross target;
- `R` = structural stop risk;
- `C_primary` = 10% of G;
- `C_stress` = 20% of G.

A candidate qualifies only if:

- `EV_primary > 0`;
- `EV_stress > 0`;
- all risk/notional/margin/session/data gates pass.

Equivalent stress break-even probability:

`p_BE_stress = (R + C_stress) / (G + R)`.

Thus qualification is economically grounded and automatically stricter when stop risk is large relative to reward.

No extra absolute probability floor may be introduced after June metrics are seen.

## 8. Cross-market ranking

At a common entry timestamp:

1. highest calibrated target-first probability;
2. highest stress EV;
3. highest primary EV;
4. rung order T30, T40, T50;
5. symbol;
6. direction.

Maximum one open Engine-K position across the portfolio.

Daily stop-adding-risk rules remain unchanged:

- stop adding after realized <= -USD40;
- normally stop adding after realized >= +USD150;
- no forced trades.

## 9. June development gate

June is the first true out-of-sample gate for v0.3's Mar-Apr model + May calibrator.

Mandatory:

1. all 8 markets retain >=200 June economically admissible states;
2. >=30 qualified one-open June trades;
3. trades occur on >=10 distinct June weekdays;
4. observed June target-hit rate > mean **stress** break-even probability;
5. June primary-cost expectancy >0;
6. June stress-cost expectancy >0;
7. June primary PF >=1.10;
8. June stress PF >=1.00;
9. June max drawdown <=USD100;
10. causality/same-bar/provenance integrity passes;
11. market contribution is reported with no silent market dropping;
12. July-August and September remain unopened.

If any mandatory gate fails, stop EXP-024 before secondary test.

## 10. Secondary-test rule if June passes

Only after a durable June PASS checkpoint:

- refit HGB Mar23-May31;
- fit market-direction-aware calibrator on June;
- freeze bundle fingerprints;
- evaluate Jul1-Aug31 exactly once.

Secondary mandatory gates:

- >=60 one-open trades;
- primary expectancy >0;
- stress expectancy >0;
- primary PF >=1.10;
- stress PF >=1.00;
- 5-weekday moving-block bootstrap 95% lower bound for primary expectancy >0;
- max drawdown <=USD150;
- integrity/provenance pass.

If any secondary gate fails, stop before September.

## 11. Final holdout

Sep1-Sep22 remains the final common-sample holdout.

Final-holdout gate will use the same frozen bundle/qualification rules from the secondary checkpoint. No refitting on Jul-Aug before final holdout.

Historical success through September is still insufficient for live promotion; longer-history/independent-feed and forward/demo evidence remain required.

## 12. Anti-mining

After v0.3 June metrics:

Do not:

- add a probability floor or change the stress-EV rule;
- change primary/stress cost fractions;
- change 1.5R/2R/2.5R;
- change HGB hyperparameters;
- switch to diagnostic logistic because it looks better;
- remove markets based on June;
- change May calibration design;
- open July-Aug after a failed June gate.

Any such redesign requires a new version/experiment.

## 13. Outcome status at freeze

At v0.3 freeze:

- v0.3 model fit metrics under the new Mar-Apr split: **NOT CALCULATED**;
- v0.3 May calibration metrics: **NOT CALCULATED**;
- v0.3 June gate metrics: **NOT CALCULATED**;
- Jul-Aug outcomes inspected for v0.3: **NO**;
- September outcomes inspected: **NO**.
