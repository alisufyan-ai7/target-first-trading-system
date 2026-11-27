# Reproducibility Gates — Badar Mechanization v0.2

## Freeze timing

These gates are frozen **before any v0.2 independent annotation is collected**.

Evidence tranche:

- 8 fresh post-v0.1 streams;
- 43 candidate events;
- 0 reused v0.1 cases.

## Promotion principle

v0.2 may advance to behavioral-fidelity reveal only if every required human-labeled field passes.

Packet-derived automatic fields do not require inter-annotator kappa.

## Core fields

### location_state

Applicable N: all events unless the visual packet is corrupt.

Pass requires:

- raw agreement >= **85%**
- Cohen's kappa >= **0.70**
- A unresolved rate <= **10%**
- B unresolved rate <= **10%**

### structural_stop_visibility

Pass requires:

- raw agreement >= **85%**
- Cohen's kappa >= **0.70**
- A unresolved rate <= **10%**
- B unresolved rate <= **10%**

### late_state

Evaluate on cases where both annotators do not mark `NOT_APPLICABLE`.

Pass requires:

- raw agreement >= **85%**
- Cohen's kappa >= **0.70**
- unresolved rate <= **10%** for each annotator on applicable cases

Also report agreement including `NOT_APPLICABLE`.

## Quality fields

### confirmation_state

Automatic NONE / NOT_YET cases are checked for packet consistency but excluded from human kappa.

On genuinely human-judged CLOSED-confirmation cases:

- raw agreement >= **80%**
- Cohen's kappa >= **0.60**
- unresolved rate <= **15%** for each annotator

If fewer than 15 human-judged cases exist, the field cannot independently pass; extend the fresh tranche before promotion.

### target_path_state

Pass requires:

- raw agreement >= **80%**
- Cohen's kappa >= **0.60**
- unresolved rate <= **15%** for each annotator

## HTF-close interpretation

Automatic:

- NONE -> NOT_RELEVANT
- PENDING -> REQUIRED_PENDING

Only COMPLETED required-close cases need human interpretation.

If >=15 completed applicable cases exist:

- raw agreement >= **85%**
- kappa >= **0.70**
- unresolved <= **10%** each

If <15 exist:

- report descriptively;
- do not treat the field as a standalone promotion gate;
- the automatic applicability logic must still have 100% packet consistency.

## Packet-metadata quality gate

Before annotator packs are released:

Required non-empty for **100%** of the 43 events:

- candidate_direction
- intended_poi_anchor
- entry_area_anchor
- confirmation_reference
- confirmation_candle_status
- required_htf_close_tf
- required_htf_close_status
- first_objective_anchor
- source frame list

A packet failing metadata completeness is excluded before annotation; it may not be silently repaired after seeing labels.

## Prior exposure

Any event marked `prior_exposure = YES` by either annotator is excluded from formal scoring.

If more than 10% of the 43 cases are excluded for exposure/corruption, the test is insufficient and must be extended prospectively.

## Derived direct-branch agreement

After A/B labels are frozen, derive direct-branch eligibility separately from each annotator's labels.

Report:

- raw derived-branch agreement
- confusion matrix

This is diagnostic; it is not an independent manually scored field.

## Overall promotion gate

Advance to Badar behavioral-fidelity reveal only if:

1. location_state PASS
2. structural_stop_visibility PASS
3. late_state PASS
4. confirmation_state PASS or has sufficient prospective extension and then PASS
5. target_path_state PASS
6. HTF packet applicability consistency = 100%
7. any statistically gated HTF interpretation field PASS
8. prior-exposure/corruption exclusion <=10%

If any required field fails:

`V0_2_REPRODUCIBILITY_FAIL_CLOSE_BEFORE_BEHAVIORAL_FIDELITY`

No P&L access is authorized in either case.
