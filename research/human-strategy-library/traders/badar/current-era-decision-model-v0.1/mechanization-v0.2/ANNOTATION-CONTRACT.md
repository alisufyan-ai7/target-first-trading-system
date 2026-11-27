# Annotation Contract — Badar Mechanization v0.2

## Status

`V0_2_ANNOTATION_CONTRACT_FROZEN_BEFORE_LABELING`

This contract is outcome-blind.

It is designed specifically to remove the ambiguities exposed by the independent v0.1 A/B study.

## Principle

Annotators no longer have to infer the candidate itself.

Every packet supplies prospectively frozen metadata:

- candidate direction;
- intended POI / entry-area anchor;
- directional context;
- relevant context timeframe;
- active confirmation timeframe;
- confirmation family/reference;
- current confirmation-candle status;
- required HTF-close timeframe;
- structural-stop anchor if prospectively stated;
- first objective;
- known blocker anchor if prospectively stated.

The annotator judges the visual state **relative to those supplied anchors**.

No Badar behavior label is supplied.

No outcome is supplied.

---

# 1. Packet metadata — not annotation targets

These fields are frozen before annotation.

## candidate_direction

- LONG
- SHORT

There is no inference from Badar's eventual action.

## directional_context

- ALIGNED
- COUNTERTREND
- MIXED
- UNKNOWN

This is source-derived prospective context, not an annotator judgment.

## intended_poi_anchor

Human-readable prospectively named area.

Examples:

- H1 sell area / swept high;
- M15 FVG;
- hidden OB/FVG;
- range breakout level;
- 4000 support area.

The packet must also contain the relevant pre-decision frame(s).

## poi_family

Examples:

- H1_SUPPLY_SWEEP
- FVG_RETRACE
- HIDDEN_OB_FVG
- RANGE_BREAK
- FVG_OB
- DAILY_OB_FVG
- ROUND_NUMBER_SUPPORT

## entry_area_anchor

The intended execution area.

This is the reference used for location and chasing.

## confirmation_tf

The timeframe on which the named confirmation is expected.

## confirmation_reference

The specific predeclared family/reference.

Examples:

- M15 inverse close after sweep;
- M1 sell close at FVG;
- M5 reverse close;
- 1m breakout close;
- direct resting limit.

Annotators do not choose the family.

## confirmation_candle_status

Normalized packet metadata:

- PENDING
- CLOSED
- NOT_REQUIRED
- UNKNOWN

This is derived from the source timestamp/candidate plan before annotation.

## required_htf_close_tf

- NONE
- M15
- M30
- H1
- H4

## required_htf_close_status

- NOT_REQUIRED
- PENDING
- COMPLETED
- UNKNOWN

## structural_stop_anchor

Prospectively named invalidation basis when one was stated or already visible.

Examples:

- above swept high;
- above FVG / zone;
- below support;
- signal-candle high;
- UNKNOWN.

The annotator still judges whether that stop is visually visible/inferable.

## first_objective_anchor

The prospectively named first objective.

It is fixed before target-path annotation.

## blocking_poi_anchor

If a blocker was already explicitly identified before the decision, it is supplied.

Otherwise:

`UNKNOWN`

Annotators may identify a clearly visible opposing structural blocker from the packet but may not use later movement.

---

# 2. location_state

Question:

> Relative to the supplied candidate direction and intended entry area, where is current price at the packet cutoff?

Labels:

### VALID

Current price is touching/inside the intended entry area, or the just-completed named confirmation candle closes from that area.

### APPROACHING

Price has not yet reached the intended entry area but is moving toward it.

### MIDDLE

Price is away from the intended entry area and sits between the active structural boundaries without a directionally coherent execution location.

### WRONG_EXTREME

Price is at the structurally wrong side for the candidate direction and the supplied candidate is not a continuation-break/retest branch.

### ABSENT

The supplied intended area is not visible/identifiable in the packet.

### UNRESOLVED

The visual packet is insufficient to distinguish the states above.

Important:

Do not redefine the POI.

Do not choose a better POI.

Judge only the supplied intended area.

---

# 3. late_state

Question:

> Relative to the supplied entry-area anchor, has price already left the intended execution area in the candidate direction?

Labels:

### ON_TIME

Price is at/inside the entry area or the named decision candle has just closed at/from the entry area.

### CHASING

Price has already displaced away from the entry area in the candidate direction and a new entry at current price would no longer be the supplied setup entry.

### NOT_APPLICABLE

The candidate is still APPROACHING the entry area, or it is a resting-limit/direct-entry branch where chasing cannot yet be assessed.

### UNRESOLVED

The entry area/current price relationship cannot be determined from the packet.

This field is no longer asked without a frozen entry-area anchor.

---

# 4. structural_stop_visibility

Question:

> Using the supplied structural-stop anchor, can the invalidation be identified from the packet before the decision?

Labels:

### VISIBLE

The exact invalidation level/line/extreme is directly visible.

### INFERABLE

The exact numerical line is not drawn, but the supplied structural basis is unambiguous from the visible chart.

### UNDEFINED

The packet and supplied setup contain no coherent structural invalidation.

### UNRESOLVED

A stop may exist, but the packet does not allow the annotator to determine it reliably.

This replaces the v0.1 `DEFINED / UNDEFINED / UNRESOLVED` state.

Risk sizeability is still outside this classifier.

---

# 5. confirmation_state

The packet supplies:

- confirmation timeframe;
- confirmation family/reference;
- confirmation-candle status.

The annotator does not invent another confirmation family.

## Automatic states

If `confirmation_candle_status = NOT_REQUIRED`:

`confirmation_state = NONE`

If `confirmation_candle_status = PENDING`:

`confirmation_state = NOT_YET`

These are packet-derived and do not require visual discretion unless the packet contradicts itself.

## For CLOSED confirmation

Labels:

### FAILED

The named completed confirmation visibly fails or closes through the candidate's invalidating side.

### WEAK

The named family is directionally present but incomplete/marginal relative to its frozen definition.

### ADEQUATE

The named family is completed at/from the supplied POI with no visible contradiction.

### STRONG

The named family is completed and has one of the predeclared strengthening conditions:

- two independent confirmations at the same area;
- a confirmed structural break aligned with the candidate;
- a separately required completed HTF close also supports the candidate.

### UNRESOLVED

The relevant candle/reference cannot be read sufficiently.

Do not use future candles to upgrade WEAK/ADEQUATE/STRONG.

---

# 6. HTF close state

v0.2 sharply separates applicability from interpretation.

## Automatic states

If `required_htf_close_tf = NONE`:

`htf_close_state = NOT_RELEVANT`

If `required_htf_close_status = PENDING`:

`htf_close_state = REQUIRED_PENDING`

These are derived from frozen metadata, not annotator opinion.

## Completed required HTF close

Only when:

- a required timeframe is supplied; and
- its required close is marked COMPLETED.

Annotator labels:

### CONFIRMS

The completed required close supports candidate direction/reference.

### INVALIDATES

The completed required close invalidates the candidate.

### FLIPS_BIAS

The close creates a structural reversal requiring the old candidate to be rebuilt.

### NEUTRAL

The close is readable but neither confirms nor invalidates the supplied candidate.

### UNRESOLVED

The required completed candle cannot be interpreted from the packet.

`NEUTRAL` is never a default for missing information.

---

# 7. target_path_state

The packet supplies a first objective before annotation.

Question:

> Is the visual path from the intended entry area to the frozen first objective structurally open?

Labels:

### FEASIBLE

No clear opposing structural blocker exists between entry area and first objective.

### INFEASIBLE

A clear opposing structural POI lies before the frozen first objective and materially blocks the path.

### UNRESOLVED

The relevant path/POIs cannot be read sufficiently.

There is no separate `FEASIBLE_WITH_EARLY_OBJECTIVE` state because the early objective is now frozen as `first_objective_anchor`.

---

# 8. direct_branch_eligible — derived, not annotated

Annotators do **not** label this field.

It is derived after A/B labels are frozen.

A direct branch is eligible only if:

- confirmation_state = NONE;
- location_state = VALID;
- structural_stop_visibility in {VISIBLE, INFERABLE};
- late_state in {ON_TIME, NOT_APPLICABLE};
- htf_close_state not in {INVALIDATES, FLIPS_BIAS};
- packet branch/reference is a source-supported direct/resting/sweep/retrace branch.

This removes an entire subjective v0.1 classifier.

---

# 9. Required annotator outputs

Human-labeled fields:

1. `location_state`
2. `late_state`
3. `structural_stop_visibility`
4. `confirmation_state` only when not automatically NONE/NOT_YET
5. `htf_close_state` only for completed required HTF closes
6. `target_path_state`
7. `annotation_confidence`
8. `unresolved_notes`
9. `prior_exposure`

Packet-derived fields must be copied unchanged.

---

# 10. Blindness

Annotators may not access:

- Badar stream notes/transcripts;
- source repository;
- eventual TRADE/WAIT/NO_TRADE decision;
- later management;
- outcome;
- P&L;
- MFE/MAE;
- other annotator labels;
- v0.1 case identities.

All images are at/before the frozen v0.2 event cutoff.

---

# 11. No post-hoc rescue

If v0.2 fails its frozen reproducibility gate:

- do not reveal Badar decisions to tune the classifier;
- do not adjudicate into a passing score;
- do not change labels and recalculate as if independent;
- create a new prospective version if warranted.
