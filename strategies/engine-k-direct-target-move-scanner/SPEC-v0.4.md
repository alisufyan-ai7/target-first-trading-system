# Engine K v0.4 — Bounded Walk-Forward Configuration Selection

**Engine ID:** engine-k-direct-target-move-scanner  
**Version:** 0.4  
**Experiment:** EXP-025  
**Status:** FROZEN PROSPECTIVELY BEFORE EXP-025 METRICS — 2026-09-24

## 1. Purpose

Engine K v0.1-v0.3 established four facts on the reusable Mar-Jun 2026 development pool:

1. dense multi-market target-first candidate generation is feasible;
2. v0.2 fixed cross-market economic admission;
3. v0.3 fixed trade-density scarcity;
4. ranking discrimination remained non-random, but hand-picked calibration/qualification rules did not produce robust positive economic expectancy.

EXP-025 therefore stops one-threshold-at-a-time redesign.

It prospectively freezes a **small bounded walk-forward configuration search** on Mar-Jun only, chooses at most one configuration by predeclared stability/economic criteria, and keeps July-August and September sealed.

## 2. What remains unchanged

The scanner/economics are inherited unchanged from Engine K v0.3:

- execution universe: XAUUSD, EURUSD, GBPUSD, USDJPY, EURJPY, AUDUSD, USDCAD, USDCHF;
- forecast-only markets excluded from executable fitting/ranking;
- complete causal 5m state construction;
- next-active M1 entry <=5 chronological minutes;
- strict causal structural pivot stop;
- same 29 causal features;
- Gold targets +3/+4/+5 XAU at 0.10 lot;
- non-Gold target-before-size ladder 1.5R / 2.0R / 2.5R;
- downward P&L-equivalent lot sizing;
- USD20 stop-risk cap;
- USD50,000 notional / 100x equity cap;
- USD100 research margin cap;
- primary cost = 10% actual gross target;
- stress cost = 20% actual gross target;
- 120-active-M1 / 20:00 UTC label horizon;
- stop-first same-bar ordering;
- one-open portfolio state;
- stop adding risk after realized <=-USD40 or normally >=+USD150;
- no forced trades.

No target, stop, cost, sizing, feature, market-universe, or daily-risk parameter participates in the search.

## 3. Development evidence status

Mar23-Jun30 2026 is fully reusable **development** evidence.

Still sealed:

- Jul1-Aug31 2026 secondary test;
- Sep1-Sep22 2026 final holdout.

EXP-025 may parse/label only timestamps <2026-07-01.

## 4. Six frozen chronological walk-forward folds

All intervals are half-open [start, end).

### Fold WF1
- fit: Mar23-Apr05
- calibration: Apr06-Apr12
- evaluation: Apr13-Apr26

### Fold WF2
- fit: Mar23-Apr19
- calibration: Apr20-Apr26
- evaluation: Apr27-May10

### Fold WF3
- fit: Mar23-May03
- calibration: May04-May10
- evaluation: May11-May24

### Fold WF4
- fit: Mar23-May17
- calibration: May18-May24
- evaluation: May25-Jun07

### Fold WF5
- fit: Mar23-May31
- calibration: Jun01-Jun07
- evaluation: Jun08-Jun21

### Fold WF6
- fit: Mar23-Jun14
- calibration: Jun15-Jun21
- evaluation: Jun22-Jul01

Earlier evaluation periods are allowed to become later training/calibration history because this is an expanding-window walk-forward design. The **configuration set itself is frozen before all fold results**.

## 5. Frozen model variants

Per target rung T30/T40/T50.

### M1 — current HGB
- learning_rate=0.05
- max_iter=150
- max_leaf_nodes=15
- min_samples_leaf=100
- l2_regularization=1.0
- random_state=20260923

### M2 — stronger regularization / shallower tree HGB
- learning_rate=0.035
- max_iter=180
- max_leaf_nodes=7
- min_samples_leaf=250
- l2_regularization=3.0
- random_state=20260923

No other HGB configuration is permitted in EXP-025.

## 6. Frozen calibration variants

Each is fit separately per rung on that fold's calibration window only.

### C1 — pooled Platt
LogisticRegression:
- input = clipped logit(raw HGB probability) only;
- C=1_000_000;
- solver=lbfgs;
- max_iter=1000.

### C2 — market-direction-aware Platt
Same logistic model, inputs:
- clipped logit(raw HGB probability);
- market one-hot for all 8 execution markets;
- direction one-hot long/short.

No isotonic, beta calibration, per-market separate model, or post-hoc calibrator is allowed.

## 7. Frozen qualification policies

All policies require:
- primary EV >0;
- stress EV >0;
- all unchanged economic/session/data gates pass.

### Q1 — Stress-EV only
No extra probability threshold.

### Q2 — Stress-EV + calibration top decile
Additionally:
- evaluation calibrated probability >= the **90th percentile** of calibrated probabilities for all economically admissible rows of the same rung in that fold's calibration window.

### Q3 — Stress-EV + calibration top 5%
Additionally:
- evaluation calibrated probability >= the **95th percentile** of calibrated probabilities for all economically admissible rows of the same rung in that fold's calibration window.

Percentile thresholds are learned from calibration predictions only and separately per rung.

## 8. Frozen 12-configuration grid

Cartesian product:

- M1/M2;
- C1/C2;
- Q1/Q2/Q3.

Exactly 12 configuration IDs:

M1-C1-Q1, M1-C1-Q2, M1-C1-Q3,
M1-C2-Q1, M1-C2-Q2, M1-C2-Q3,
M2-C1-Q1, M2-C1-Q2, M2-C1-Q3,
M2-C2-Q1, M2-C2-Q2, M2-C2-Q3.

No configuration may be added after EXP-025 metrics begin.

## 9. Frozen cross-market ranking

Among qualified candidates sharing an entry timestamp:

1. highest calibrated target-first probability;
2. highest stress EV;
3. highest primary EV;
4. rung order T30, T40, T50;
5. symbol;
6. direction.

Maximum one open Engine-K trade.

## 10. Per-fold reporting

For every configuration and fold report:

- admissible candidate count;
- qualified candidate count;
- actual one-open trades;
- distinct trade weekdays;
- target-hit rate;
- mean stress break-even probability;
- primary expectancy;
- stress expectancy;
- primary PF;
- stress PF;
- primary/stress net P&L;
- primary/stress max drawdown;
- market trade counts;
- max market concentration;
- daily P&L including zero-trade weekdays.

Also report per-rung raw/calibrated AUC as diagnostics.

## 11. Frozen configuration pass gate

A configuration is eligible for selection only if **all** hold across the six evaluation folds:

1. total actual trades >=120;
2. every fold has >=8 actual trades;
3. total distinct evaluation trade weekdays >=35;
4. pooled primary expectancy >0;
5. pooled stress expectancy >0;
6. pooled primary PF >=1.10;
7. pooled stress PF >=1.05;
8. at least 4 of 6 folds have positive stress expectancy;
9. worst-fold stress expectancy > -USD5/trade;
10. pooled observed target-hit rate > pooled mean stress break-even probability;
11. chronological pooled stress max drawdown <=USD150;
12. no single market contributes >60% of pooled trades;
13. causality/same-bar/provenance integrity passes;
14. July-August and September remain unopened.

If **no** configuration passes, EXP-025 stops and Engine K is not exposed to July-August.

## 12. Frozen winner selection

Among passing configurations, choose one by this exact lexicographic ordering:

1. highest worst-fold stress expectancy;
2. highest pooled stress PF;
3. lowest pooled stress max drawdown;
4. highest total actual trades;
5. lexicographically smallest configuration ID.

Do **not** choose by total P&L, best AUC, or best single fold.

The selected configuration and all fold metrics must be durably checkpointed before July-August is opened.

## 13. Frozen refit rule if a winner exists

Only after a durable EXP-025 PASS/winner checkpoint:

- fit the selected HGB variant on Mar23-May31;
- fit the selected calibration variant on June;
- if selected policy is Q2/Q3, learn its per-rung percentile threshold from June only;
- freeze model/calibrator/threshold fingerprints;
- evaluate Jul1-Aug31 exactly once.

No fit/calibration on July-Aug before or during secondary testing.

## 14. Secondary-test gate

Jul-Aug may be opened only for the one frozen winner.

Mandatory secondary gates:

1. >=60 one-open trades;
2. >=25 distinct trade weekdays;
3. target-hit rate > mean stress break-even;
4. primary expectancy >0;
5. stress expectancy >0;
6. primary PF >=1.10;
7. stress PF >=1.00;
8. 5-weekday moving-block bootstrap 95% lower bound for **primary expectancy >0**;
9. max drawdown <=USD150;
10. no market >60% of trades;
11. causality/provenance pass.

Fail any -> stop before September.

## 15. Final holdout

Sep1-Sep22 remains untouched until a durable secondary PASS.

The same frozen secondary bundle is used on September:
- no refit using Jul-Aug;
- no threshold change;
- no market removal.

Historical success still requires longer-history/independent-feed and forward/demo evidence before live promotion.

## 16. Anti-mining / stopping rule

After EXP-025 walk-forward metrics:

Do not:
- add configurations;
- change fold dates;
- change pass criteria;
- change winner ordering;
- change model/qualification parameters;
- open July-Aug if no configuration passes.

If no configuration passes, stop Engine K tuning on this Mar-Jun pool. The next research move must broaden evidence or prediction design rather than manufacture another threshold.

## 17. Outcome status at freeze

At v0.4 / EXP-025 freeze:
- EXP-025 walk-forward metrics: **NOT CALCULATED**;
- selected configuration: **NONE**;
- July-Aug outcomes inspected: **NO**;
- September outcomes inspected: **NO**.
