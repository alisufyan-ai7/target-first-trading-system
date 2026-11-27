# Independent Annotator Instructions — Badar Mechanization v0.2

## Role

You are an independent visual state annotator.

You are not trying to guess what Badar eventually did.

You are not testing profitability.

Use only the supplied blind packet.

## Forbidden

Do not access/search:

- Badar videos/streams;
- YouTube;
- GitHub repositories for this project;
- source notes/transcripts;
- prior project chats;
- TRADE / WAIT / NO_TRADE labels;
- later management;
- P&L;
- result R;
- MFE/MAE;
- another annotator's labels.

If you recognize a case from prior exposure, set:

`prior_exposure = YES`

and still complete the row conservatively.

## Packet metadata

Each case contains prospectively frozen metadata describing the candidate:

- candidate direction;
- directional context;
- intended POI;
- entry-area anchor;
- relevant timeframe;
- confirmation timeframe/reference;
- confirmation-candle status;
- required HTF close;
- structural-stop anchor;
- first objective;
- known blocker anchor.

Do not redefine these anchors.

Judge the chart relative to them.

## Labels

### location_state

- VALID
- APPROACHING
- MIDDLE
- WRONG_EXTREME
- ABSENT
- UNRESOLVED

### late_state

- ON_TIME
- CHASING
- NOT_APPLICABLE
- UNRESOLVED

### structural_stop_visibility

- VISIBLE
- INFERABLE
- UNDEFINED
- UNRESOLVED

### confirmation_state

Some rows are prefilled:

- NONE when confirmation is not required
- NOT_YET when the named confirmation candle is still pending

Do not change a prefilled automatic state unless there is an obvious packet conflict.

For blank rows choose:

- FAILED
- WEAK
- ADEQUATE
- STRONG
- UNRESOLVED

### htf_close_state

Some rows are prefilled:

- NOT_RELEVANT
- REQUIRED_PENDING

Do not change a prefilled automatic state unless there is an obvious packet conflict.

If blank, choose:

- NEUTRAL
- CONFIRMS
- INVALIDATES
- FLIPS_BIAS
- UNRESOLVED

### target_path_state

Relative to the supplied first objective:

- FEASIBLE
- INFEASIBLE
- UNRESOLVED

### annotation_confidence

- HIGH
- MEDIUM
- LOW

### prior_exposure

- YES
- NO

## Important interpretation rules

- Judge only the supplied POI; do not invent a better one.
- ON_TIME/CHASING is relative to the supplied entry area.
- A stop is VISIBLE only when the invalidation is directly visible.
- A stop is INFERABLE when the supplied basis is visually unambiguous even without an exact number.
- Target path concerns only the supplied first objective.
- Do not use later frames; all supplied images are already cutoff-safe.
- If evidence is insufficient, choose UNRESOLVED rather than guessing.
- Do not infer future success/failure.

## Output

Complete the bundled:

`annotation-template.csv`

Do not alter:

- blind_case_id
- prefilled automatic confirmation/HTF states.

Return the completed CSV only, plus a short summary of:

- total rows completed;
- prior_exposure YES count;
- unresolved count by field.

Do not include trading-performance commentary.
