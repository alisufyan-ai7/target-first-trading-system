# Blind Packet Schema — Badar Mechanization v0.2

## Goal

Give independent annotators enough prospective context to judge the supplied candidate consistently without revealing what Badar eventually did.

## Per-event directory

```text
<blind_case_id>/
  CASE.md
  frame_01.jpg
  frame_02.jpg
  frame_03.jpg
  ...
```

Frames are full-resolution source frames from the frozen external commit and must satisfy:

`frame_timestamp <= event_timestamp`

No future frame is allowed.

## CASE.md — allowed content

Only normalized prospective metadata:

- blind case ID
- candidate direction
- directional context
- intended POI anchor
- POI family
- entry-area anchor
- relevant context TF
- confirmation TF
- confirmation reference
- confirmation-candle status
- required HTF-close TF
- required HTF-close status
- structural-stop anchor
- first-objective anchor
- blocking-POI anchor
- number/order of supplied frames

## CASE.md — forbidden

- source stream ID
- date if it materially enables source lookup
- Badar's final action
- TRADE / WAIT / NO_TRADE
- entry fill confirmation
- management after the decision
- result
- P&L
- MFE/MAE
- source quote that reveals the action
- transcript text
- source-note path
- outcome-oriented terms

## Frame selection

For each event:

1. enumerate full-resolution source frames for the event's stream;
2. include the latest frame at/before event;
3. include up to four earlier frames to provide structural context;
4. prefer at least one context frame >=5 minutes earlier where available;
5. never include a frame after the event timestamp;
6. do not edit/generate chart content;
7. do not crop away chart structure solely to hide an inconvenient cue;
8. if the latest frame visibly contains a post-action position box that itself reveals the action, step back to the prior safe frame and record the gap.

## Timestamp gap

Record internally:

- event timestamp
- latest frame timestamp
- gap seconds

The blinded packet does not expose source IDs.

A case is eligible when latest visual gap <= **240 seconds**.

If >240 seconds:

exclude before annotation and document it.

## Annotation template

Columns:

- blind_case_id
- location_state
- late_state
- structural_stop_visibility
- confirmation_state
- htf_close_state
- target_path_state
- annotation_confidence
- unresolved_notes
- prior_exposure

Packet-derived automatic states may be prefilled:

- confirmation_state NONE / NOT_YET
- htf_close_state NOT_RELEVANT / REQUIRED_PENDING

Annotators must not overwrite a prefilled automatic state unless the packet metadata and image visibly conflict; if so, set `unresolved_notes` with `PACKET_CONFLICT`.

## A/B anonymization

Annotator A and B must receive:

- different blind IDs;
- different case order;
- identical underlying images/metadata for the same event;
- no shared crosswalk.

The mapping must be sealed before annotation returns.

GitHub stores only the crosswalk SHA-256 commitment until scoring is complete.
