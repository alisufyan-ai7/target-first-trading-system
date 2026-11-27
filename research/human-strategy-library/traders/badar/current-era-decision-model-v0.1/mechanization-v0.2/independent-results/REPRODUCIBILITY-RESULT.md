# Badar Mechanization v0.2 — Independent Reproducibility Result

## Disposition

`V0_2_REPRODUCIBILITY_FAIL_CLOSE_BEFORE_BEHAVIORAL_FIDELITY`

The two fresh independent annotator returns are complete and structurally valid. The frozen v0.2 gates were applied without adjudication or label repair.

Badar's actual TRADE / WAIT / NO_TRADE decisions were **not** revealed. P&L, result-R, MFE/MAE and skipped-trade outcomes remain sealed.

## Frozen study boundary

- v0.2 external evidence boundary: `bd0037e06a881a066e0cd8070b635cace59240d1`
- fresh live streams: 8
- fresh candidate events: 43
- v0.1 cases reused: 0
- A pack SHA-256: `8a3673345c3f35ffbfb8acc7ed7b6ede9e83210d48c563eb238dccdcac026a67`
- B pack SHA-256: `1561b0a9ea61b22b7968247ae39e4c18420a402479adc93513ba754dade2bca8`
- sealed crosswalk commitment: `8c8fd102539a2099b271a22d93733f9838c46a4cb73965d784abbf93b5dd3096`

## Submission / provenance integrity

- retrieved A pack hash: `8a3673345c3f35ffbfb8acc7ed7b6ede9e83210d48c563eb238dccdcac026a67` — PASS
- retrieved B pack hash: `1561b0a9ea61b22b7968247ae39e4c18420a402479adc93513ba754dade2bca8` — PASS
- recovered sealed crosswalk CSV hash: `8c8fd102539a2099b271a22d93733f9838c46a4cb73965d784abbf93b5dd3096` — PASS
- completed A CSV SHA-256: `3b90fc82dabd64edba8567a3db7a6b761ce681bbb2a777a3ba0f46c457b6c9fd`
- completed B CSV SHA-256: `5a2702817795395755420b324abcddfdd8e091000256fcceefa7529a1e194c07`
- A rows: 43; duplicate IDs: 0; missing IDs: 0; unexpected IDs: 0
- B rows: 43; duplicate IDs: 0; missing IDs: 0; unexpected IDs: 0
- prior_exposure=YES: A 0, B 0
- A/B paired-case prospective metadata matches through the sealed crosswalk: 43/43
- automatic confirmation states preserved: 26/26 for A and 26/26 for B
- automatic HTF states preserved: 43/43 for A and 43/43 for B
- completed required-HTF-close human cases: 0
- human CLOSED-confirmation cases: 17 (predeclared minimum 15 satisfied)

## Frozen reproducibility gates

| Field | Scored N | Raw agreement | Cohen's κ | A unresolved | B unresolved | Frozen requirement | Result |
|---|---:|---:|---:|---:|---:|---|---|
| location_state | 43 | 51.2% | 0.260 | 0.0% | 2.3% | raw ≥ 85%; κ ≥ 0.70; unresolved ≤ 10% each | **FAIL** |
| structural_stop_visibility | 43 | 74.4% | 0.532 | 9.3% | 2.3% | raw ≥ 85%; κ ≥ 0.70; unresolved ≤ 10% each | **FAIL** |
| late_state (both not NOT_APPLICABLE) | 26 | 73.1% | 0.450 | 3.8% | 3.8% | raw ≥ 85%; κ ≥ 0.70; unresolved ≤ 10% each | **FAIL** |
| confirmation_state (17 human CLOSED cases) | 17 | 76.5% | 0.595 | 0.0% | 5.9% | raw ≥ 80%; κ ≥ 0.60; unresolved ≤ 15% each | **FAIL** |
| target_path_state | 43 | 95.3% | 0.482 | 2.3% | 4.7% | raw ≥ 80%; κ ≥ 0.60; unresolved ≤ 15% each | **FAIL** |
| HTF packet applicability | 43 | 100.0% automatic consistency | n/a | 0.0% | 0.0% | 100% packet consistency; no standalone human gate because completed applicable N=0 | **PASS** |

`late_state` including `NOT_APPLICABLE` across all 43 events: raw agreement **44.2%**, κ **0.177**. The formal late gate uses the frozen 26-case subset where both annotators did not mark `NOT_APPLICABLE`.

## Overall gate

Required human fields failing the frozen gate:

- `location_state` — FAIL
- `structural_stop_visibility` — FAIL
- `late_state` — FAIL
- `confirmation_state` — FAIL
- `target_path_state` — FAIL

HTF automatic applicability passes, and the prior-exposure exclusion rate is 0%, but the overall promotion rule requires every required human field to pass.

Therefore the formal disposition is:

`V0_2_REPRODUCIBILITY_FAIL_CLOSE_BEFORE_BEHAVIORAL_FIDELITY`

## Confusion matrices

### location_state

| A \\ B | VALID | APPROACHING | MIDDLE | ABSENT | UNRESOLVED |
|---|---:|---:|---:|---:|---:|
| VALID | 13 | 7 | 0 | 5 | 0 |
| APPROACHING | 2 | 8 | 0 | 3 | 0 |
| MIDDLE | 0 | 0 | 0 | 2 | 0 |
| ABSENT | 1 | 0 | 0 | 1 | 1 |
| UNRESOLVED | 0 | 0 | 0 | 0 | 0 |

### structural_stop_visibility

| A \\ B | VISIBLE | INFERABLE | UNRESOLVED |
|---|---:|---:|---:|
| VISIBLE | 13 | 4 | 0 |
| INFERABLE | 4 | 18 | 0 |
| UNRESOLVED | 1 | 2 | 1 |

### late_state — formal applicable subset

| A \\ B | ON_TIME | CHASING | UNRESOLVED |
|---|---:|---:|---:|
| ON_TIME | 13 | 4 | 0 |
| CHASING | 3 | 5 | 0 |
| UNRESOLVED | 0 | 0 | 1 |

### confirmation_state — 17 human CLOSED cases

| A \\ B | FAILED | WEAK | ADEQUATE | STRONG | UNRESOLVED |
|---|---:|---:|---:|---:|---:|
| FAILED | 0 | 1 | 0 | 0 | 0 |
| WEAK | 0 | 0 | 0 | 0 | 0 |
| ADEQUATE | 0 | 0 | 7 | 1 | 1 |
| STRONG | 0 | 0 | 1 | 6 | 0 |
| UNRESOLVED | 0 | 0 | 0 | 0 | 0 |

### target_path_state

| A \\ B | FEASIBLE | INFEASIBLE | UNRESOLVED |
|---|---:|---:|---:|
| FEASIBLE | 40 | 0 | 1 |
| INFEASIBLE | 1 | 0 | 0 |
| UNRESOLVED | 0 | 0 | 1 |

## Derived direct-branch agreement — diagnostic only

The frozen contract derives direct-branch eligibility after A/B labels are frozen. Only packet branches with a source-supported direct/resting reference can be positive.

- Annotator A derived eligible: 0/43
- Annotator B derived eligible: 1/43
- raw derived-branch agreement: 97.7% (42/43)

| A \\ B | NOT_ELIGIBLE | ELIGIBLE |
|---|---:|---:|
| NOT_ELIGIBLE | 42 | 1 |
| ELIGIBLE | 0 | 0 |

This diagnostic does not override any failed manually scored gate.

## Diagnostic interpretation — not a rescue

- `location_state` remains the clearest unresolved representation problem: only 22/43 pairs agree.
- `structural_stop_visibility` now has acceptable unresolved rates, but VISIBLE vs INFERABLE is still not reproducible enough: raw 74.4%, κ 0.532.
- `late_state` fails even on the predeclared applicable subset. Annotator A used `ON_TIME` on all 13 of its `APPROACHING` location calls, whereas the frozen contract says an `APPROACHING` candidate should be `NOT_APPLICABLE`; Annotator B followed that rule on its APPROACHING calls. This is recorded as a contract-application diagnostic only; no labels are repaired.
- `confirmation_state` is close but still fails exactly as frozen: 76.5% raw < 80%, and κ 0.595 < 0.60. Rounding does not convert it to a pass.
- `target_path_state` has 95.3% raw agreement but κ 0.482 because both annotators overwhelmingly use FEASIBLE. The predeclared kappa gate still applies; prevalence is not waived after seeing the result.
- HTF applicability ambiguity is mechanically resolved in this tranche (41 NOT_RELEVANT + 2 REQUIRED_PENDING, preserved 100%), but there are no completed required-close human cases, so human HTF interpretation remains untested here.

## Scientific action

The protocol closes v0.2 before behavioral fidelity. Do **not**:

- reveal Badar's actual TRADE/WAIT/NO_TRADE labels for these 43 cases;
- adjudicate or repair A/B labels and recalculate the same tranche as if it were independent;
- open P&L/outcomes;
- tune v0.2 on these disagreements and reuse these 43 cases as fresh validation.

If mechanization research continues, it must be a prospectively new version/tranche. The present result can be used only as disagreement diagnostics for that future design.
