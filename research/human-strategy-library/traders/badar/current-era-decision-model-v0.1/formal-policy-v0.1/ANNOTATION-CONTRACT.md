# Annotation Contract — Formal Decision Policy v0.1

## Purpose

The formal policy is deterministic only if its inputs are normalized consistently.

This file defines the outcome-blind state labels that must be known **before** the policy is evaluated.

It also marks fields that remain human-classified because Badar's source material does not provide a defensible raw-price threshold.

## Unit of evaluation

A policy evaluation is performed for one candidate direction at one timestamp.

Do not label with knowledge of what price does afterward.

## Required normalized inputs

### 1. `candidate_direction`

- LONG
- SHORT

Direction is the side currently being evaluated, not a prediction that it will win.

### 2. `environment_state`

- NORMAL
- CAUTION
- UNINTERPRETABLE

`CAUTION` includes news, low volume, Friday/month-end, chop, manipulation comments or similar source-supported modifiers.

News alone does not imply `UNINTERPRETABLE`.

### 3. `external_risk_lock`

- YES
- NO

This belongs to the account/session risk layer.

### 4. `directional_context`

- ALIGNED
- COUNTERTREND
- MIXED
- UNKNOWN

Use D1/H4/H1 with greatest weight on the active H1/current structural case.

### 5. `htf_close_state`

- CONFIRMS
- NEUTRAL
- REQUIRED_PENDING
- INVALIDATES
- FLIPS_BIAS
- NOT_RELEVANT

### 6. `location_state`

- VALID
- APPROACHING
- ABSENT
- MIDDLE
- WRONG_EXTREME
- UNRESOLVED

A VALID location is a pre-identifiable structural area such as:

- session high/low;
- prior-day high/low;
- swing high/low;
- equal high/low;
- range edge;
- OB/FVG/breaker;
- BOS origin;
- supply/demand;
- premium/discount POI;
- stacked structural POI.

A lower-timeframe candle pattern by itself is not a VALID location.

### 7. `location_family`

One or more of:

- SESSION_EXTREME
- PRIOR_DAY_EXTREME
- SWING_EXTREME
- EQUAL_HIGH_LOW
- RANGE_EXTREME
- OB
- FVG
- BREAKER
- BOS_ORIGIN
- SUPPLY_DEMAND
- PREMIUM_DISCOUNT
- OTHER_STRUCTURAL_POI

### 8. `interaction_family`

- SWEEP
- FAKE_BREAK
- TRAP
- RETRACE_TO_POI
- REJECTION
- CONTINUATION_RETEST
- RANGE_TEST
- SECOND_REACTION
- NONE
- UNRESOLVED

### 9. `required_interaction_state`

- COMPLETE
- NOT_YET
- NOT_REQUIRED
- UNRESOLVED

This prevents hindsight from labeling an interaction as required only after seeing the result.

### 10. `confirmation_family`

- MSS_MOMENTUM
- INVERSE_CLOSE
- CLOSE_BACK_INSIDE
- TWO_CANDLE_REJECTION
- ENGULF_STRONG_CLOSE
- MINI_RANGE_BREAK
- FVG_OB_RETRACE_CONFIRM
- DOUBLE_CONFIRMATION
- NONE
- OTHER

### 11. `confirmation_state`

- STRONG
- ADEQUATE
- WEAK
- FAILED
- NOT_YET
- NONE

### 12. `late_state`

- ON_TIME
- CHASING

### 13. `valid_retrace_path_exists`

- YES
- NO

Used only after a missed/late entry.

### 14. `stop_state`

- DEFINED_ACCEPTABLE
- DEFINED_LARGE_BUT_SIZABLE
- TOO_LARGE_FOR_THIS_SETUP
- UNDEFINED

### 15. `stop_basis`

- SWEEP_EXTREME
- OUTER_SWING
- ZONE
- CONFIRMATION_CANDLE
- RANGE_BOUNDARY
- OTHER

### 16. `target_path_state`

- FEASIBLE
- INFEASIBLE
- UNRESOLVED

This is a structural judgment about room before opposing liquidity, not a hidden P&L label.

### 17. `execution_style`

- MARKET_ON_CLOSE
- LIMIT_RETRACE
- DIRECT_AFTER_SWEEP
- SPLIT_ENTRY
- OTHER

### 18. downgrade modifiers

Boolean flags:

- COUNTERTREND
- NEWS_CAUTION
- LARGE_STOP
- WEAK_CONFIRMATION
- DIRECT_AGGRESSIVE
- RANGE_CHOP
- LOW_VOLUME
- TEST_POSITION
- REENTRY_ADDON
- LOW_CONFIDENCE
- TARGET_PATH_UNRESOLVED
- OTHER_CAUTION

## Human-classified fields that are NOT yet raw-price rules

The following labels are legitimate policy inputs but are not yet mechanically derived from OHLC:

1. `location_state`
2. `confirmation_state` strength
3. `stop_state` size class
4. `target_path_state`
5. `environment_state = UNINTERPRETABLE`
6. whether a specific HTF close is `REQUIRED_PENDING`

This is intentional.

Creating a numeric threshold now would be researcher invention.

## Anti-hindsight labeling rules

1. Freeze the candidate timestamp before annotation.
2. Hide future candles.
3. Do not use trade outcome, MFE, MAE, TP hit, SL hit or later P&L.
4. Do not label a level “strong” because price later reversed from it.
5. Do not label a direct entry “eligible” because it later won.
6. Do not change `required_interaction_state` after the future interaction becomes visible.
7. If a state cannot be determined from information available at the timestamp, use `UNRESOLVED`; do not guess.

## Conflict rule

If two annotators disagree on a human-classified input:

- preserve both labels;
- mark the event `ANNOTATION_CONFLICT`;
- do not use the event to set a new threshold;
- resolve only by a pre-declared adjudication method before outcome access.

## Mechanization boundary

The next mechanization study must turn the unresolved human-classified fields into prospective chart rules **without P&L optimization**.

Until then, this policy is suitable for:

- source-fidelity replay;
- blinded annotation studies;
- deterministic decision reconstruction from normalized labels.

It is not yet suitable for automated OHLC backtesting.
