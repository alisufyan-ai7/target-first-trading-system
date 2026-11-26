# Phase-2 Independent Reproducibility Result

## Disposition

`PHASE2_V0_1_INDEPENDENT_REPRODUCIBILITY_FAIL_CLOSE_BEFORE_BEHAVIORAL_FIDELITY`

The two independent annotator returns are complete and structurally valid.

No Badar decision label or trading outcome was revealed before this result.

## Submission integrity

Annotator A:

- Batch 1: 64
- Batch 2: 64
- Batch 3: 63
- Batch 4: 63
- total: 254
- duplicate blind IDs: 0
- unexpected blind IDs: 0
- prior exposure YES: 0

Annotator B:

- Batch 1: 64
- Batch 2: 64
- Batch 3: 63
- Batch 4: 63
- total: 254
- duplicate blind IDs: 0
- unexpected blind IDs: 0
- prior exposure YES: 0

A and B map to the same 254 frozen underlying events.

The rebuilt sealed crosswalk hash verified exactly:

`474572c2e21d6d8f5a770f27ce0b9d5d837bd2c147691bb15b652334672ddbc1`

## Frozen reproducibility gates

### Core hard-gate fields

Required:

- raw agreement >= 85%
- Cohen's kappa >= 0.70
- unresolved rate <= 10%

| Field | Raw agreement | Kappa | A unresolved | B unresolved | Result |
|---|---:|---:|---:|---:|---|
| location_state | 45.3% | 0.285 | 12.6% | 14.6% | FAIL |
| structural_stop_state | 78.0% | 0.448 | 34.6% | 15.4% | FAIL |
| htf_close_state | 18.5% | -0.002 | 53.5% | 3.9% | FAIL |
| late_state | 59.1% | 0.315 | 18.5% | 16.1% | FAIL |

### Quality fields

Required:

- raw agreement >= 80%
- Cohen's kappa >= 0.60
- unresolved rate <= 15%

| Field | Raw agreement | Kappa | A unresolved | B unresolved | Result |
|---|---:|---:|---:|---:|---|
| confirmation_state | 41.3% | 0.265 | 10.2% | 15.7% | FAIL |
| target_path_state | 68.5% | 0.310 | 30.3% | 19.7% | FAIL |
| direct_branch_eligible | 52.4% | 0.278 | 31.5% | 15.0% | FAIL |

**All seven frozen fields fail.**

## Important nuance: some failures are representation/availability failures, not pure semantic contradictions

### Structural stop

Overall:

- raw agreement: 78.0%
- kappa: 0.448
- A unresolved: 34.6%
- B unresolved: 15.4%

But when both annotators made a resolved call:

- resolved pairs: 163
- resolved agreement: **99.4%**

The dominant disagreement is:

- A = UNRESOLVED
- B = DEFINED
- count = **51**

This suggests the structural-stop concept itself may be stable when visible, but the v0.1 packet/contract did not make the invalidation basis equally inferable to both annotators.

### Target path

Overall:

- raw agreement: 68.5%
- kappa: 0.310

When both annotators were resolved:

- resolved pairs: 162
- resolved agreement: **85.8%**

Main disagreement:

- A = UNRESOLVED
- B = FEASIBLE
- count = **38**

A second material disagreement is:

- A = FEASIBLE
- B = INFEASIBLE
- count = **22**

This field needs a stricter definition of the first objective and what counts as a blocking POI.

### HTF close state

This is the clearest contract failure.

A frequently used:

- UNRESOLVED
- NOT_RELEVANT
- CONFIRMS

B overwhelmingly used:

- NEUTRAL

Largest disagreement:

- A = UNRESOLVED
- B = NEUTRAL
- count = **120**

Other large cells:

- A = NOT_RELEVANT / B = NEUTRAL: **49**
- A = CONFIRMS / B = NEUTRAL: **22**

The v0.1 contract does not distinguish these states reproducibly enough from visual frames alone.

### Location state

Largest disagreement:

- A = VALID
- B = MIDDLE
- count = **27**

Other material disagreements:

- A = VALID / B = APPROACHING: **12**
- A = VALID / B = WRONG_EXTREME: **11**
- A = MIDDLE / B = VALID: **9**

The active-boundary / candidate-side definition is not sufficiently explicit.

### Confirmation state

Largest disagreement families:

- A = NOT_YET / B = ADEQUATE: **24**
- A = NOT_YET / B = STRONG: **17**
- A = ADEQUATE / B = STRONG: **16**
- A = WEAK / B = NOT_YET: **12**
- A = WEAK / B = STRONG: **12**
- A = WEAK / B = UNRESOLVED: **12**

This points to missing shared rules for:

- which candle is the active confirmation candle;
- whether that candle is closed;
- which reference boundary/family is being tested;
- whether one completed pattern is adequate versus strong.

### Late / chasing

Largest disagreement:

- A = ON_TIME
- B = CHASING
- count = **51**

Without a prospectively frozen intended entry area, chart-only annotation leaves too much room for interpretation.

## Binary hard-gate reductions

These do not rescue the failed full-state gates, but they help diagnose where signal exists.

### Structural stop defined

Among 163 resolved pairs:

- positive agreement: **99.7%**
- raw agreement: **99.4%**

Negative agreement is not meaningful because only one resolved negative call exists across the pairwise sample.

### Confirmation failed

Among 207 resolved pairs:

- raw binary agreement: **94.2%**
- positive agreement on FAILED: **50.0%**
- negative agreement: **96.9%**

The easy case is agreeing that confirmation has *not* failed; identifying actual failure remains weak.

### Location hard veto

Among 201 resolved pairs:

- raw agreement: 64.2%
- positive agreement: 54.4%
- negative agreement: 70.5%

### Chasing

Among 191 resolved pairs:

- raw agreement: 65.4%
- positive agreement: 45.0%
- negative agreement: 74.8%

## Secondary-field agreement

These are diagnostic only:

- directional_context: 51.2%, kappa 0.358
- location_family: 27.6%, kappa 0.181
- interaction_family: 29.5%, kappa 0.157
- confirmation_family: 31.9%, kappa 0.165

The low agreement supports the same conclusion: the v0.1 visual representation and qualitative contract leave too much interpretation to the annotator.

## Why the study closes here

The frozen protocol states that a field failing its reproducibility gate remains human/discretionary and may not be treated as mechanically resolved.

Because **all seven promotion fields fail**, v0.1 mechanization cannot be promoted to automated policy replay for scientific promotion.

Badar decision labels remain sealed.

P&L remains sealed.

A subjective adjudication after seeing this failure would not be allowed to convert the failed fields into passing automated fields.

Additionally, the current research chat has prior exposure to the source-derived Badar corpus, so it should not become a subjective tie-break adjudicator for the failed v0.1 fields.

## Next research direction — outcome blind

Create **Mechanization v0.2** as a new version, not a silent rewrite of v0.1.

The v0.2 design should address the disagreement structure without using Badar decisions or P&L.

Priority fixes:

1. include prospectively identifiable candidate direction when available;
2. include session/timeframe/current-candle-open-or-closed metadata;
3. freeze the intended entry/POI area before asking ON_TIME vs CHASING;
4. separate `NOT_RELEVANT`, `NEUTRAL`, and `UNRESOLVED` HTF-close logic more sharply;
5. separate “structural stop visible” from “structural stop inferable”;
6. define target path around a predeclared first objective and explicit blocker ordering;
7. give confirmation state a frozen reference boundary and active confirmation candle;
8. test v0.2 on a prospectively separate evidence tranche rather than tuning and re-scoring these same 254 cases.

Do not reveal v0.1 Badar decision labels merely to diagnose this reproducibility failure.
