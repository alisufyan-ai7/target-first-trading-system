# Fresh Independent Annotator Instructions — Badar Phase 2 Core 254

## Role

You are an independent chart-state annotator.

You are **not** testing profitability and you are **not** trying to guess what Badar eventually did.

Use only the supplied blind event packet.

## Forbidden information

Do not access:

- Badar stream notes or transcripts;
- live-trades datasets;
- TRADE / WAIT / NO_TRADE labels;
- later management actions;
- future chart panels;
- P&L;
- result R;
- MFE / MAE;
- another annotator's labels.

If you recognize a stream from prior work, mark the event `PRIOR_EXPOSURE` and exclude it from formal agreement scoring.

## Required output

Fill:

`phase2-core-254-annotation-template.csv`

For every event, label the frozen state from the supplied pre-decision panels.

Primary fields:

- `location_state`
- `confirmation_state`
- `structural_stop_state`
- `target_path_state`
- `htf_close_state`

Secondary fields:

- `directional_context`
- `location_family`
- `interaction_family`
- `confirmation_family`
- `late_state`
- `direct_branch_eligible`
- `annotation_confidence`
- `unresolved_notes`

## Allowed labels

Follow the frozen derivation contract:

`STATE-DERIVATION-CONTRACT.md`

Do not invent a new numeric rule.

When visual evidence is insufficient, use `UNRESOLVED`.

## Critical rules

- A candle pattern alone does not create a VALID location.
- Do not infer a swing/OB/FVG because price later reacts.
- Do not infer target-path feasibility from later TP success.
- Do not infer confirmation from a panel after the frozen event.
- A structural stop is DEFINED only if an invalidation basis is visible before the decision.
- Preserve uncertainty.

## Submission

Return only the completed annotation CSV plus a short count of:

- completed events;
- UNRESOLVED events by primary field;
- PRIOR_EXPOSURE events.

Do not include profitability commentary.
