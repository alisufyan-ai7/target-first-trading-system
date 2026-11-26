# Badar Mechanization v0.2 — Prospective Outcome-Blind Redesign

**Status:** DESIGN AUTHORIZED — TEST NOT YET RUN  
**Parent failure:** `PHASE2_V0_1_INDEPENDENT_REPRODUCIBILITY_FAIL_CLOSE_BEFORE_BEHAVIORAL_FIDELITY`  
**Badar decision labels available to design process:** NO  
**P&L/outcomes available:** NO

## Why v0.2 exists

Mechanization v0.1 failed independent reproducibility across all seven frozen promotion fields.

The failure is not treated as a reason to reveal Badar's decisions or tune against profitability.

v0.2 may use only:

- aggregate A/B disagreement structure;
- frozen source-derived definitions already available before outcomes;
- packet/representation deficiencies exposed by the blind study.

It may not use:

- Badar's actual TRADE/WAIT/NO_TRADE labels from the 254 core events;
- result R;
- P&L;
- MFE/MAE;
- skipped-trade hindsight;
- outcome-conditioned threshold selection.

## v0.2 design priorities

### 1. Candidate-side metadata

The blind packet must include a prospectively identifiable candidate direction when it exists.

If no side can be identified before the decision timestamp, mark:

`NO_CANDIDATE_SIDE`

Do not infer direction from Badar's eventual action.

### 2. Intended POI / entry-area anchor

Before asking:

- VALID vs MIDDLE vs WRONG_EXTREME;
- ON_TIME vs CHASING;

the packet must freeze the candidate POI / intended entry area visible before the decision.

Without an entry anchor, chasing is too subjective.

### 3. Candle-status metadata

For the active confirmation timeframe include:

- timeframe;
- current candle open/closed;
- exact cutoff timestamp relative to candle close.

This addresses NOT_YET vs ADEQUATE/STRONG disagreement.

### 4. HTF-close semantics

Separate these mechanically:

- `NOT_RELEVANT`: the branch does not require an HTF close;
- `REQUIRED_PENDING`: the required candle has not closed;
- `NEUTRAL`: the relevant completed close neither confirms nor invalidates;
- `CONFIRMS`;
- `INVALIDATES`;
- `FLIPS_BIAS`;
- `UNRESOLVED`: evidence needed to classify the relevant close is absent.

Do not use NEUTRAL as a generic default for missing information.

### 5. Structural-stop observability

Separate:

- `DEFINED_VISIBLE`
- `DEFINED_INFERABLE`
- `UNDEFINED`
- `UNRESOLVED`

v0.1 showed near-perfect agreement when both annotators resolved the stop, but large disagreement over whether it was inferable from the packet.

### 6. Target-path contract

Freeze before annotation:

- candidate entry;
- first objective;
- next opposing liquidity;
- blocking-POI definition.

Then classify:

- `FEASIBLE`
- `FEASIBLE_WITH_EARLY_OBJECTIVE`
- `INFEASIBLE`
- `UNRESOLVED`

### 7. Confirmation reference

Each candidate must name the prospective reference boundary/family before annotation.

Then the annotator judges whether the completed candle evidence is:

- FAILED
- NOT_YET
- WEAK
- ADEQUATE
- STRONG
- NONE
- UNRESOLVED

Do not ask the annotator to infer both the intended confirmation family and its quality from the same sparse frame set.

## Fresh-test rule

Do not tune this contract on the 254 v0.1 cases and then call rescoring those same cases independent validation.

The next formal reproducibility test must use a prospectively separate evidence tranche.

Preferred source:

post-v0.1 Badar live sessions already arriving in the external evidence repository, beginning after the frozen source boundary `d19a43d...`.

Any new v0.2 evidence boundary must be frozen before blind labels are collected.

## Promotion gate

v0.2 must declare its agreement/kappa/unresolved thresholds before annotation begins.

No development P&L study is authorized unless the new reproducibility gate passes prospectively.

## Exact next action

1. audit post-freeze source-layer live streams available after `d19a43d...`;
2. define a fresh v0.2 evidence cutoff;
3. extract decision timestamps outcome-blind;
4. build the enriched v0.2 pre-decision packet;
5. freeze the v0.2 annotation contract and agreement gate;
6. run fresh independent annotators;
7. score reproducibility;
8. only if reproducibility passes, proceed to behavior-fidelity reveal;
9. keep P&L sealed until the later explicit promotion gate.
