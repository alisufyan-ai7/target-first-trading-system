# Badar Mechanization v0.2 — Prospective Outcome-Blind Redesign

**Status:** BLIND PACKS FROZEN — INDEPENDENT ANNOTATION PENDING  
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


## Execution checkpoint — 2026-11-27

The prospective v0.2 redesign has now advanced through pack freeze.

Completed:

- audited all 8 live streams after the v0.1 cutoff;
- froze external evidence commit `bd0037e06a881a066e0cd8070b635cace59240d1`;
- froze 43 fresh candidate events;
- reused 0 v0.1 cases;
- froze the richer annotation contract before labeling;
- froze the new agreement/kappa gates before labeling;
- froze 102 full-resolution pre-decision source frames;
- all 43 events pass the visual-gap requirement;
- built independently randomized A/B blind packs;
- verified no source/event ID leakage in filenames/text metadata;
- verified no Badar decision labels or outcomes are exposed.

Active pack freeze:

`PACK-FREEZE.md`

Active pack manifest:

`active-pack-manifest-v0.2.csv`

Annotator handoff:

`ANNOTATOR-HANDOFF.md`

### Pack statistics

- candidate events: 43
- eligible: 43
- excluded: 0
- total packet images per annotator: 164
- unique source frames: 102
- max latest-frame gap: 182 sec
- median latest-frame gap: 67 sec
- confirmation cases requiring human judgment: 17
- confirmation automatic NOT_YET: 24
- confirmation automatic NONE: 2
- HTF automatic NOT_RELEVANT: 41
- HTF automatic REQUIRED_PENDING: 2

### Active hashes

Annotator A:

`8a3673345c3f35ffbfb8acc7ed7b6ede9e83210d48c563eb238dccdcac026a67`

Annotator B:

`1561b0a9ea61b22b7968247ae39e4c18420a402479adc93513ba754dade2bca8`

Sealed crosswalk commitment:

`8c8fd102539a2099b271a22d93733f9838c46a4cb73965d784abbf93b5dd3096`

### Current disposition

`BADAR_MECHANIZATION_V0_2_BLIND_PACKS_FROZEN — INDEPENDENT_ANNOTATION_PENDING`

The current Chat #09 may not annotate these packs.

The next formal operation requires two fresh isolated annotator chats.

Badar behavioral labels remain sealed.

P&L remains sealed.


## Chat #10 annotation-return intake checkpoint — 2026-11-27

The user reports both independent v0.2 annotators completed all 43 cases with prior exposure YES = 0.

Aggregate unresolved counts reported:

| Field | Annotator A | Annotator B |
|---|---:|---:|
| location_state | 0 | 1 |
| late_state | 1 | 1 |
| structural_stop_visibility | 4 | 1 |
| confirmation_state | 0 | 1 |
| htf_close_state | 0 | 0 |
| target_path_state | 1 | 2 |

These marginal counts are **not** a reproducibility result.

The governing Chat #10 has not yet ingested the completed row-level CSVs, so no A/B pairing, agreement, kappa, confusion matrix, applicable-case filtering, or direct-branch derivation has been performed.

Current disposition:

`BADAR_MECHANIZATION_V0_2_ANNOTATION_RETURNS_REPORTED — FORMAL_CSV_INGESTION_AND_SCORING_PENDING`

Behavior labels and P&L remain sealed.
