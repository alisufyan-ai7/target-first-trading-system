# EXP-028 — Engine M v0.2 Signal-First Validation

**Status:** CLOSED — DEVELOPMENT GATE FAILED; SECONDARY SEALED  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-m-mtf-reclaim-limit-entry/SPEC-v0.2.md`

## Purpose

Correct the research-layer ordering exposed by EXP-027.

EXP-027 showed that Engine-M mechanics generated 1,581 limit fills but the USD40-equivalent sizing gate rejected most FX fills because target-size lots exceeded the USD50k / USD100-margin reference-account envelope.

This does not prove the signals lack edge.

EXP-028 separates:

1. **signal validity** — does the MTF/limit setup have target-first edge?
2. **reference-account deployability** — what P&L can the frozen USD500 risk/margin envelope actually support?

## Strategy rules

Unchanged from Engine M v0.1.

No parameter is altered.

## Preflight

Zero-outcome only:

- >=50 mechanically filled valid signals per market;
- both directions every market;
- >=600 total;
- safe-lot overlay for each signal;
- Gold remains capped at 0.10 lot;
- no safety-cap violations;
- utility bands GE40 / GE30 / LT30 reported;
- Jul-Aug/Sep sealed.

## Development

If preflight passes:

- six fixed chronological development slices;
- size-invariant normalized-R signal metrics;
- separate USD500 safe-lot portfolio metrics;
- matched immediate-entry control.

## Protection

At freeze:

- v0.2 outcomes: none;
- Jul-Aug: unopened;
- Sep: unopened.

## Next

Implement the zero-outcome safe-lot/deployability preflight only.


## Zero-outcome preflight — PASS

**Workflow run:** `35997920091`  
**Trigger SHA:** `057871a772d384faa5af67b7e73089d3c2c9d730`  
**Durable result commit:** `68e52188de8abb2c708cacb611e347afb22a086d`

Protection:

- target outcomes: **NO**;
- P&L outcomes: **NO**;
- Jul-Aug secondary: **unopened**;
- Sep final holdout: **unopened**.

Result:

- total filled valid signal paths: **1,581**;
- safe-lot deployable paths >=0.01: **1,581**;
- every market >=50 signals: PASS;
- LONG and SHORT on every market: PASS;
- total >=600: PASS;
- safe overlay never violated USD20 risk / USD50k notional / USD100 margin: PASS.

Utility under the frozen USD500 reference account:

- GE40: **66**;
- GE30: **160**;
- LT30: **1,355**.

Per-market signal counts:

- XAUUSD 196;
- EURUSD 176;
- GBPUSD 212;
- USDJPY 193;
- EURJPY 193;
- AUDUSD 198;
- USDCAD 212;
- USDCHF 201.

All 1,581 are mechanically filled valid signals and all remain safely deployable at some >=0.01 lot size.

**Disposition:** PASS. EXP-028 may proceed to development outcomes while Jul-Aug and Sep remain sealed.


## Final pre-development reporting clarification

Daily USD100/USD150 reporting uses final realized UTC-day primary P&L, with all eligible weekdays including zero-trade days in the denominator. These are descriptive metrics, not pass gates.

No EXP-028 target/P&L outcome existed when this clarification was frozen.


## Development implementation checkpoint — zero outcomes

Frozen before EXP-028 development outcomes:

- six fixed evaluation slices;
- size-invariant normalized-R signal layer;
- separate safe-lot USD500 reference-account portfolio;
- matched immediate-entry control on the same MTF arms;
- one-open portfolio ranking by achievable gross target, then lower stop risk;
- daily stop-adding-risk rules;
- end-of-day USD100/USD150 reporting definition;
- per-market normalized-R diagnostics;
- strict Jul1 seal.

Implementation commits:

- development runner: `033c870660e7a1d58ac7905cc78e107dd4f1aec0`;
- development workflow: `526cdb2234da7f07e23196b60ee0c82b4118a792`;
- per-market reporting hardening: `619e3d3d02bd80ed7182a3ee68b96f18887c64d5`.

At this checkpoint:

- EXP-028 target outcomes: **NO**;
- EXP-028 P&L outcomes: **NO**;
- Jul-Aug loaded/labeled: **NO**;
- Sep loaded/labeled: **NO**.

### Next

Trigger EXP-028 development only. Fail any mandatory development gate -> stop before secondary.


## Development attempt 1 — reporting runtime failure

**Workflow run:** `35999223397`  
**Trigger SHA:** `45a742a2d7d21bb78996e5ebd9cacbb0dba9da07`

The frozen verification step passed, and the development simulation started, but the runner crashed during pooled reporting before writing the durable JSON result.

Root cause:

- pooled distinct-trade-weekday reporting attempted to slice a pandas `Timestamp` as if it were a string.

This was a **reporting implementation defect**, not a strategy-rule or development-gate failure.

Evidence status:

- no development result JSON was committed;
- no development metrics were durably recorded or inspected;
- no Jul-Aug secondary data was loaded/labeled;
- no Sep final holdout data was loaded/labeled.

Correction:

- replace timestamp slicing with `entry_ts.date().isoformat()`;
- no Engine-M mechanics, sizing, costs, development slices or gates changed.

Fix commit:

`57be12953b917c66b269800cb00889e7f707405b`

### Next

Rerun the identical frozen EXP-028 development workflow.


## Development outcome — FAIL

**Retry workflow run:** `35999708390`  
**Tested SHA:** `0312884e3ff251036f6cd71754a2f470f0988fc6`  
**Durable result commit:** `bd0ae3f18509c8e4e19fbe570766c961b1f4e3fb`  
**Result:** `research/results/EXP-028-development-summary-v0.2.json`

Protection:

- development source parsed only through Jun30;
- Jul-Aug secondary loaded/labeled: **NO**;
- Sep final holdout loaded/labeled: **NO**.

### Signal-layer result

Across the six frozen development slices:

- 1,249 Engine-M limit-entry signals;
- target hit rate: **35.07%**;
- gross normalized expectancy: **+0.0367R/signal**;
- primary-cost expectancy: **-0.1625R/signal**;
- stress-cost expectancy: **-0.3616R/signal**;
- primary normalized PF: **0.791**;
- stress normalized PF: **0.601**;
- positive stress folds: **0/6**.

Matched immediate-entry control:

- 1,917 signals;
- hit rate: 32.55%;
- gross expectancy: **-0.0146R/signal**;
- primary expectancy: **-0.2032R/signal**;
- stress expectancy: **-0.3918R/signal**.

Interpretation:

The MTF retracement-limit entry **did improve the raw signal** relative to immediate entry:

- hit rate improved by about 2.5 percentage points;
- gross expectancy improved from slightly negative to slightly positive;
- primary/stress normalized expectancy also improved.

However, the gross edge is too small to overcome the prospectively frozen cost assumptions.

Per-market primary normalized expectancy remained negative on every market. The least negative were approximately:

- USDJPY -0.109R;
- USDCAD -0.111R;
- XAUUSD -0.114R.

### Reference-account result

Safe-lot USD500 one-open portfolio:

- 593 trades;
- 57 distinct trade weekdays;
- hit rate: **34.06%**;
- primary net P&L: **-USD999.84**;
- stress net P&L: **-USD2,028.71**;
- primary expectancy: **-USD1.69/trade**;
- stress expectancy: **-USD3.42/trade**;
- primary PF: **0.756**;
- stress PF: **0.575**;
- primary MDD: **USD1,062.68**;
- stress MDD: **USD2,065.82**;
- GE40 trades: 34;
- GE30 trades: 45;
- LT30 trades: 514;
- final-day P&L >=USD100: 1/57 weekdays;
- final-day P&L >=USD150: 0/57 weekdays.

Matched immediate-control portfolio was also negative:

- primary expectancy about -USD2.08/trade;
- stress expectancy about -USD4.67/trade.

Thus the limit-entry design improved economics versus immediate entry but remained decisively unprofitable after costs.

### Fold stability

Primary normalized R was positive in only one fold (WF5, about +0.017R). Stress normalized R was negative in **all six** folds.

### Frozen gate failures

Failed:

- pooled primary normalized-R expectancy >0;
- pooled stress normalized-R expectancy >0;
- >=4 positive-stress folds;
- reference-account primary expectancy >0;
- reference-account stress expectancy >0;
- primary PF >=1.10;
- stress PF >=1.05;
- stress MDD <=USD150.

Passed:

- signal/trade frequency;
- executable weekdays;
- market concentration;
- integrity/provenance;
- protected-period seal.

**Final disposition:** FAIL. Do not open Jul-Aug.

### Methodological conclusion

Engine M v0.2 established a small raw edge from the user-guided MTF + non-chasing entry architecture, but not enough edge to cover the frozen transaction-cost model.

Do not rescue v0.2 by weakening costs, gates or protected-period discipline.

Any next version must increase **pre-cost signal quality/selectivity** materially while preserving the non-chasing entry principle.
