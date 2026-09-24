# EXP-026 — Engine L v0.1 Forecast-Armed Micro Pullback Entry

**Status:** CLOSED — DEVELOPMENT GATE FAILED; SECONDARY SEALED  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-l-forecast-armed-micro-entry/SPEC-v0.1.md`

## Why this experiment exists

The Engine-K series revealed a structural problem in the research architecture:

the probability layer was being asked to do the job of **entry timing**.

Engine K converted a completed 5m state almost directly into a next-M1-open entry. It did not wait for a favorable execution price or fresh M1 confirmation.

EXP-026 isolates that issue.

## Thesis

A useful directional forecast should **arm** a market, not force an immediate trade.

A trade occurs only after:

1. a causal favorable pullback;
2. a causal M1 resumption confirmation;
3. a fresh execution-level stop is available;
4. safe T40 economics pass.

## Frozen configuration

One center configuration only:

- fixed M2 HGB raw T40 forecast;
- higher-scoring direction armed per market;
- 15 active-M1 arm lifetime;
- 0.20*V5 required pullback;
- M1 break/resumption bar with outer-quartile close;
- next-M1-open entry;
- fresh pullback-extreme stop;
- Gold T40 = 4 XAU;
- non-Gold T40 = 2R;
- same USD20 risk/notional/margin/cost framework.

No parameter grid.

## Matched control

Use the same forecast arms but enter immediately at the next M1 open with the old 5m pivot stop.

This directly tests whether execution timing/stop freshness improves economics.

## Evidence

Development:

- Mar23-Jun30 reusable.

Protected:

- Jul-Aug unopened;
- Sep unopened.

Use the same six forward folds as EXP-025.

## Zero-outcome preflight gate

Before any Engine-L outcome:

- mechanics/unit tests must pass;
- each execution market must produce >=100 mechanically triggerable and economically admissible T40 entry paths through Jun30;
- both directions must be represented on every market;
- Jul-Aug and Sep remain unloaded.

## Gate

Engine L must independently be profitable/stable and materially beat the matched immediate-entry control.

See SPEC-v0.1 for exact frozen criteria.

## Outcome status

At freeze:

- Engine-L outcomes: NO;
- matched-control outcomes: NO;
- Jul-Aug: unopened;
- Sep: unopened.

## Next

Implement exact causal entry engine + six-fold development runner. Preflight it before outcomes, then run development only if entry mechanics pass.


## Zero-outcome mechanics preflight — PASS

**Workflow run:** `35986445374`  
**Durable result commit:** `b19d4ef6c3a689117fc5b8237167322bd64a2aa7`  
**Result:** `research/results/EXP-026-entry-mechanics-preflight-v0.1.json`

Protection at checkpoint:

- Engine-L target outcomes calculated: **NO**;
- Engine-L P&L outcomes calculated: **NO**;
- forecast model fitted: **NO**;
- Jul-Aug secondary loaded/inspected: **NO**;
- Sep final holdout loaded/inspected: **NO**.

Mechanics result:

- total examined decision-direction paths: 274,666;
- total admissible micro-entry paths: 12,532;
- every execution market exceeded the frozen >=100-path minimum;
- every market produced both long and short admissible triggers;
- median wait-to-entry was about 6-7 active M1 bars across markets.

Per-market admissible paths:

- XAUUSD 1,748;
- EURUSD 1,129;
- GBPUSD 1,665;
- USDJPY 906;
- EURJPY 705;
- AUDUSD 3,938;
- USDCAD 435;
- USDCHF 2,006.

**Disposition:** PASS. Engine-L mechanics are sufficiently abundant and balanced to justify the prospectively frozen development test.

No profitability conclusion is implied by this preflight.


## Final pre-outcome matched-domain clarification

Before Engine-L development outcomes:

- forecast fit/evaluation sides are restricted to the same complete, pre-probability economically admitted T40 state domain used by the Engine-K v0.2/v0.3 forecast model;
- this restriction is intentional so EXP-026 isolates **entry timing + execution stop** rather than candidate-universe expansion;
- Engine-L recomputes T40 economics at its later micro-entry using the fresh M1 stop;
- exact LONG/SHORT raw-score ties use lower old-reference stop risk, then LONG;
- pending-arm resolution is tracked causally so later 5m decisions cannot overlap an unresolved same-symbol arm.

No Engine-L target/P&L outcome had been calculated when these mechanics were frozen.


## Development implementation checkpoint — zero Engine-L outcomes

Frozen before development outcomes:

- matched forecast domain clarification committed;
- one-pending-arm causal resolution timestamps implemented;
- exact six-fold T40/M2 development runner implemented;
- Engine-L pullback/resumption/fresh-stop entry compared with matched immediate-entry control;
- one-open portfolio and daily stop-adding-risk rules implemented separately for Engine L and control;
- pooled arm, pullback, resumption, wait-time, entry-price-improvement and fresh-vs-old-stop diagnostics included;
- strict Jul1 seal asserted in runner/workflow.

Implementation commits:

- matched-domain clarification: `1e595d8ce4ae248cff2551d33a4da8d220ba54a6`;
- arm-resolution metadata: `a1f62169edc282e3965eb4a1729d37976021929b`;
- development runner: `7aefb3d5b19b0144bb474596c78669ca1316b161`;
- development workflow: `dd5f34f507c7e0d96d412112780394ab92256853`;
- final reporting hardening: `467cf9f05e6ee67731605f5dd8af3083729b4ef9`.

At this checkpoint:

- Engine-L development outcomes: **NO**;
- matched-control EXP-026 development outcomes: **NO**;
- Jul-Aug loaded/labeled: **NO**;
- Sep loaded/labeled: **NO**.

### Next

Trigger EXP-026 development only. Apply the frozen development gate; fail any mandatory condition -> stop before secondary.


## Development outcome — FAIL

**Workflow run:** `35991120871`  
**Tested repository SHA:** `ca05b65200a66fd2ff39f4b902a3deed53894ef0`  
**Durable result commit:** `7cacd739f80ab37a2f6465924937bd6489b1b966`

Protection:

- development only through Jun30;
- Jul-Aug secondary loaded/labeled: **NO**;
- Sep final holdout loaded/labeled: **NO**.

Engine L pooled result:

- 303 actual trades;
- 57 distinct trade weekdays;
- target hits: 80;
- hit rate: **26.40%**;
- mean stress break-even probability: **46.42%**;
- primary expectancy: **-USD5.82/trade**;
- stress expectancy: **-USD9.77/trade**;
- primary PF: **0.628**;
- stress PF: **0.469**;
- stress max drawdown: **USD3,141.88**;
- positive-stress folds: **0/6**.

Matched immediate-entry control:

- 438 actual trades;
- hit rate: **18.49%**;
- primary expectancy: **-USD4.55/trade**;
- stress expectancy: **-USD8.49/trade**;
- primary PF: **0.645**;
- stress PF: **0.452**.

Engine L increased hit rate substantially but **reduced** pooled stress expectancy versus the matched control by about **USD1.28/trade**. It beat the control on stress expectancy in only 3/6 folds.

Entry-quality diagnostics:

- 35,211 forecast arms;
- 28,976 reached the required pullback;
- 23,457 reached M1 resumption;
- only 2,643 became economically admissible micro entries;
- 20,178 resumption triggers were economically rejected;
- median wait to micro entry: 7 active M1 bars;
- median fresh-stop distance: about 0.00051 native units;
- median old-stop distance: about 0.00106;
- median "entry price improvement" was **negative ~0.516 V5**.

Interpretation of the last point:

the pullback occurred, but waiting for the frozen previous-M1-break + outer-quartile resumption and then entering next-open caused the system to re-enter after price had already moved back in the forecast direction. The typical executed entry was therefore **worse than the original decision close by about half a recent 5m median range**, not better.

This is the central entry lesson from EXP-026: confirmation as implemented became **chasing**, even though it tightened the stop and improved raw hit rate.

Forecast-score development diagnostic:

- lowest quartile hit rate ~25.3%, stress expectancy ~-USD10.52/trade;
- second quartile ~25.0%, ~-USD10.79/trade;
- third quartile ~28.9%, ~-USD6.68/trade;
- highest quartile ~26.3%, ~-USD11.10/trade.

Thus a simple absolute probability threshold is not the justified next fix.

Frozen gate result:

- frequency / weekday / market-concentration gates: PASS;
- primary expectancy: FAIL;
- stress expectancy: FAIL;
- primary PF: FAIL;
- stress PF: FAIL;
- hit-rate vs stress break-even: FAIL;
- positive-stress folds: FAIL;
- stress drawdown: FAIL;
- >=USD2/trade improvement over control: FAIL;
- better than control in >=4 folds: FAIL;
- integrity/protection: PASS.

**Final disposition:** FAIL. Do not open Jul-Aug.

### Methodological conclusion

Engine L demonstrated that lower-timeframe entry mechanics matter, but the specific "pullback -> breakout/resumption -> next-open" rule enters too late. The next design should not add a probability threshold or tune the same resumption rule.

The strongest prospective direction is the already documented multi-timeframe hierarchy:

`4H/1H context -> 15m setup/location -> 5m tactical decision -> lower-timeframe entry`

with an entry mechanism that preserves the favorable pullback price rather than requiring a chase after a full short-term breakout.
