# Phase-2 Independent Annotator Pack Freeze

## Status

`INDEPENDENT_ANNOTATOR_PACKS_FROZEN — FRESH_CONTEXT_EXECUTION_REQUIRED`

The 254-event core tranche has been converted into two independently anonymized annotation sets.

## Independence hardening

The prior core packet exposed original stream/event identifiers.

The formal annotator packs do not.

For both Annotator A and Annotator B:

- original stream IDs removed from paths and text metadata;
- original decision-event IDs removed;
- case folders use random blind IDs;
- image filenames use only sequential frame numbers;
- cases are independently shuffled;
- A and B use different blind IDs and different within-batch order;
- decision labels are absent;
- outcomes/P&L/MFE/MAE are absent;
- source notes/transcripts are absent.

Images themselves are unchanged source-derived pre-decision panels.

## Workload split

The same 254 underlying events are divided into four paired folds:

- Batch 1: 64 events
- Batch 2: 64 events
- Batch 3: 63 events
- Batch 4: 63 events

Annotator A and B receive the same underlying events per batch, but with independent blind IDs/order.

This permits fold-by-fold agreement calculations while reducing context pressure.

## Public pack hashes

See:

`phase2-independent-pack-manifest.csv`

## Sealed crosswalk

The blind-ID crosswalk is **not committed to GitHub**.

Only its SHA-256 commitment is frozen here:

`4752dbd7cee71e4185da38da762778bc7bb4c913a9b0d6a516ec2b1062d1f990`

This allows later verification that the mapping used for scoring is the same mapping created before annotation results were seen.

## Leak scan

All 8 packs were scanned for:

- representative original stream IDs;
- original event-ID field names;
- stream-ID field names.

No such identifier leaks were found in pack filenames or text metadata.

Forbidden terms such as P&L/TRADE/NO_TRADE can appear only in the instructions as explicit things the annotator must not access; no actual labels are supplied.

## Formal execution requirement

A fresh context that has not read the source-derived Badar decision corpus is required for Annotator A.

A separately isolated fresh context is required for Annotator B.

The current research chat is ineligible because it has prior source-decision exposure.

## Submission contract

Each annotator returns one completed CSV per batch using the bundled `annotation-template.csv`.

Do not merge or transform the returned labels before all 8 batch outputs are frozen.

After all outputs are received:

1. verify pack hashes;
2. verify blind-ID mapping commitment;
3. map A/B labels to original frozen event IDs;
4. exclude `prior_exposure=YES`;
5. compute raw agreement, kappa, confusion matrices, unresolved rates;
6. adjudicate outcome-blind;
7. freeze final state labels;
8. replay Formal Decision Policy v0.1;
9. only then reveal Badar decision labels for behavioral fidelity.

P&L remains sealed.
