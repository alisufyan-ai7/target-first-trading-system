# Engine K v0.2 — Multi-Market Direct Target-Move Scanner

**Engine ID:** engine-k-direct-target-move-scanner  
**Version:** 0.2  
**Experiment:** EXP-023  
**Status:** FROZEN PROSPECTIVELY BEFORE V0.2 OUTCOMES — 2026-09-24

## 1. Why v0.2 exists

Engine K v0.1 correctly changed the project from one-pattern-at-a-time discovery to dense multi-market target-first scanning, but its first training/calibration stage exposed two implementation-level design failures:

1. all 7,098 economically admissible v0.1 labeled rungs came from XAUUSD;
2. every FX execution market produced zero admissible rungs because the generic 0.14/0.19/0.23 x MTR20 target distances were too small to support USD30–50 P&L-equivalent sizing under the frozen USD500-account notional/margin limits;
3. the universal 60% probability floor was stricter than the actual reward/risk economics and produced zero qualified v0.1 trades.

July-August 2026 secondary-test outcomes and Sep-1–Sep-22 final-holdout outcomes remain unopened.

v0.2 keeps the direct causal scanner, features, structural stops, model family and evidence split, while prospectively replacing the non-Gold target/economic construction and probability qualification rule.

## 2. Governing principle

At every eligible completed 5m state, for each execution market and direction:

1. define the unchanged causal structural stop;
2. define a native target distance from the frozen v0.2 target function;
3. only then calculate the downward-rounded P&L-equivalent lot;
4. reject unsafe/notional-heavy candidates;
5. estimate target-before-stop probability;
6. qualify only when calibrated probability exceeds a conservative break-even margin and EV is positive;
7. rank qualified opportunities cross-market.

This preserves the governing order in `docs/PNL-EQUIVALENT-SIZING.md`:

`target distance -> equivalent lot -> risk/margin/notional gates`.

## 3. Universe

Primary execution-research markets remain unchanged:

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

Forecast-only markets remain unchanged and may not influence primary fitting/calibration/ranking/P&L:

- XAGUSD
- NAS100
- US30
- SPX500

No BTC/ETH/extra symbol is added in v0.2. New symbols follow `research/provenance/EXP-022-symbol-admission-policy.md`.

## 4. Evidence split

Reuse the still-protected EXP-022 split:

- training: 2026-03-23 through 2026-05-31;
- calibration: 2026-06-01 through 2026-06-30;
- secondary test: 2026-07-01 through 2026-08-31;
- final common holdout: 2026-09-01 through 2026-09-22;
- 2026-09-23 excluded.

v0.2 may use training/calibration only until its pre-secondary gate passes.

## 5. Candidate clock and structural stop

Unchanged from v0.1:

- completed, complete UTC-aligned 5m bars;
- weekday decisions;
- decision completion before 20:00 UTC;
- entry = next available M1 open, maximum 5 chronological minutes after decision completion;
- no cross-session delayed entry;
- long stop = latest causally confirmed strict 2-left/2-right 5m pivot low within 60 active minutes minus one research tick;
- short stop = mirror pivot high plus one research tick;
- invalid entry/stop geometry rejected;
- structural stop is never shrunk to fit risk.

## 6. Gold target ladder

XAUUSD remains unchanged from v0.1:

- T30: +3.000 / -3.000 XAU from entry;
- T40: +4.000 / -4.000 XAU;
- T50: +5.000 / -5.000 XAU;
- research size anchor = 0.10 lot;
- each rung must independently pass the frozen stop-risk, notional and margin gates.

No Gold target is re-selected using the inspected v0.1 training/calibration outcomes.

## 7. Non-Gold v0.2 native target function

For every non-Gold candidate, first calculate the unchanged structural stop distance:

`R_native = abs(entry - structural_stop)`.

Target distances are then frozen as:

- T30: `1.5 x R_native`;
- T40: `2.0 x R_native`;
- T50: `2.5 x R_native`.

Each target distance is rounded **upward** to the market's research tick so the frozen reward/risk multiple is not weakened by tick alignment.

This is an engine-defined candidate-specific target function. It is not a volatility-burden conversion and does not reverse the target/size order.

## 8. P&L-equivalent size after target definition

For each rung after the native target distance is fixed:

- `V1` = contemporaneous USD P&L per one native price unit at 1.00 lot;
- raw lot = nominal rung objective / (`D_native x V1`);
- nominal objectives: T30=USD30, T40=USD40, T50=USD50;
- round the lot **down** to the 0.01 research lot step;
- actual gross target = `D_native x V1 x rounded_lot`.

No upward lot rounding.

If rounded lot <0.01, reject the rung.

## 9. Economic safety gates

Unchanged research-only feasibility framework:

- reference equity = USD500;
- structural stop risk <=USD20;
- notional/equity <=100x;
- notional <=USD50,000;
- research margin at 1:500 <=USD100;
- primary cost = 10% of actual gross target;
- stress cost = 20% of actual gross target.

These remain research screens, not broker specifications.

Because the non-Gold target multiples are 1.5R/2R/2.5R and size is calculated after the target, the theoretical stop-risk burden before lot rounding is approximately:

- T30: USD20;
- T40: USD20;
- T50: USD20.

The explicit USD20 risk gate remains authoritative.

## 10. Label horizon and conservative ordering

Unchanged from the final v0.1 pre-outcome clarification:

- entry M1 counts as active minute 1;
- maximum 120 active M1 bars;
- same-date 20:00 UTC cutoff;
- only bars starting before 20:00 are eligible;
- stop wins any target/stop same-bar tie, including entry bar;
- no overnight carry;
- if neither stop nor target fires, label=0 and mark P&L to the last eligible processed M1 close.

## 11. Causal feature contract

The same 29-feature v0.1 contract is retained unchanged:

- multi-horizon signed momentum;
- EMA gap/slopes;
- 60m/240m range location;
- volatility/regime;
- candle shape;
- structural-stop geometry;
- stop risk;
- market identity;
- direction;
- UTC cyclic time;
- weekday.

No target outcome, later-bar information, July-August state distribution, or September information enters features.

## 12. Primary model and calibration

Keep the v0.1 primary model unchanged to isolate the economic redesign:

Primary per-rung model:

- pooled eight-market `HistGradientBoostingClassifier`;
- learning_rate=0.05;
- max_iter=150;
- max_leaf_nodes=15;
- min_samples_leaf=100;
- l2_regularization=1.0;
- random_state=20260923.

Market and direction use the same frozen one-hot encoding.

Calibration:

- June only;
- Platt/sigmoid on clipped logit(raw primary probability);
- LogisticRegression(C=1,000,000, solver=lbfgs, max_iter=1000).

Diagnostic baseline remains StandardScaler + L2 LogisticRegression(C=1.0, solver=lbfgs, max_iter=1000). It cannot replace the primary model based on observed performance.

## 13. v0.2 probability qualification

Replace the v0.1 universal 60% floor with an economic-confidence rule.

For each rung:

`p_BE = (stop_risk_USD + primary_cost_USD) / (actual_gross_target_USD + stop_risk_USD)`.

Frozen v0.2 required probability:

`p_required = max(0.50, p_BE + 0.10)`.

A candidate qualifies only if:

- calibrated `p >= p_required`;
- primary-cost EV >0;
- all economic/session/data gates pass.

Primary-cost EV:

`EV = p x actual_gross_target - (1-p) x stop_risk - primary_cost`.

Stress-cost EV must be reported but is diagnostic for v0.2.

Rationale frozen before v0.2 outcomes:

- require the move to be at least more-likely-than-not;
- require at least ten percentage points of probability headroom above economic break-even;
- allow better reward/risk rungs to qualify at lower absolute probability than worse reward/risk rungs;
- do not lower this rule based on later trade frequency.

## 14. One-open portfolio simulation

Unchanged:

- max one Engine-K trade open across all execution markets;
- rank same-entry-time qualified candidates by calibrated probability, then primary EV;
- deterministic rung/symbol/direction tie-break;
- no same-minute re-entry if the previous trade's intrabar exit was not known at that minute open;
- stop adding new risk after realized daily P&L <= -USD40;
- normally stop adding new risk after realized daily P&L >= +USD150;
- no forced trade.

## 15. Zero-outcome v0.2 preflight gate

Before any v0.2 target labels/model outcomes:

- all 8 execution markets must produce >0 economically admissible rungs through June;
- each market should produce at least 200 unique economically admissible states through June; if not, stop and revise before labels;
- complete-bar, pivot, entry-gap, rounded-lot, target-multiple and economic-gate unit tests must pass;
- forecast-only markets remain unloaded from primary execution modeling;
- July-August and September state distributions remain unopened.

The preflight may inspect candidate/economic counts through June because they contain no target outcomes.

## 16. Training + June calibration gate before secondary test

After v0.2 preflight passes:

- fit only on Mar23-May31;
- calibrate only on June.

Mandatory pre-secondary gates:

1. >=200 unique economically admissible labeled states per execution market combined train+cal;
2. >=100 qualified one-open simulated trades combined train+cal;
3. >=20 qualified one-open simulated trades in June calibration alone;
4. June target-hit rate > June mean actual break-even probability;
5. June primary-cost expectancy >0;
6. June primary-cost profit factor >=1.10;
7. June max drawdown <=USD100 on the USD500 reference curve;
8. causality/same-bar/provenance integrity passes;
9. market contribution/concentration is reported; no market may be silently removed;
10. July-August and September remain unopened until this gate is frozen.

If any mandatory gate fails, stop v0.2 before July-August.

## 17. Anti-mining rules

Do not, after v0.2 outcomes:

- alter 1.5R/2R/2.5R;
- lower `max(0.50, p_BE+0.10)`;
- change HGB hyperparameters;
- replace HGB with the diagnostic logistic model because it looks better;
- drop weak markets from combined reporting;
- change structural-stop logic;
- open July-August after a failed training/calibration gate;
- add BTC or other new symbols to rescue v0.2.

Any such redesign requires a new prospectively frozen version/experiment.

## 18. Promotion meaning

Even if v0.2 passes training/calibration, July-August, and September, it is not automatically live-ready.

Longer-history / independent-feed validation and forward/demo evidence remain required before paper/live promotion.
