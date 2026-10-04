# Phase-2 Panel Split and Blind Packet Report

## Status

`PHASE2_BLIND_CORE_PACKET_READY — INDEPENDENT_ANNOTATION_PENDING`

No P&L, result-R, MFE, MAE, later trade outcome, or Badar decision label was used to build the visual packet.

## Evidence boundaries

Frozen v0.1 human-logic source commit:

`d19a43da80ae0e3ab4207a73a35f317120d37c84`

Visual-asset source commit used for the panel export:

`1072f7d5dc477f662436167c25a71566d7e44314`

A later tooling-only commit added the one-shot GitHub Actions export workflow.

Post-freeze streams present in the visual asset repo are not admitted to v0.1.

## Deterministic panel split

GitHub Actions run:

`37230903035`

Artifact:

`11314210584 — badar-phase2-stream-panels`

Input:

- 328 stream contact sheets;
- 44 source stream IDs.

Output:

- **1,312 individual panels**;
- each panel is a direct quadrant crop;
- embedded yellow source timestamp preserved;
- no OCR used during image splitting;
- no image generation;
- no chart reconstruction;
- no decision or outcome field used.

Frozen v0.1 streams remain 42/42 covered.

Two additional visual streams are post-freeze:

- `PYPzCJV-YXE`
- `PxDGTxs-Cvc`

They remain outside v0.1.

## Timestamp indexing

The pushed contact sheets contain the source timestamp only as pixels.

No durable source-side timestamp manifest exists.

A batch numeric timestamp read was therefore used as a **last-resort indexing operation only** after deterministic splitting.

Safeguards:

1. only the embedded yellow `minute:second` label was read;
2. panel order is fixed by source sheet/panel order;
3. the source media pipeline guarantees the first retained panel is time zero;
4. malformed/non-time labels are not promoted;
5. per-stream timestamp anchors are required to form a strictly increasing sequence;
6. packet selection uses a **20-second safety margin** before the frozen decision timestamp;
7. OCR output never supplies a trading-state label;
8. P&L/outcome information remains sealed.

This indexing is provenance metadata, not trading evidence.

## Event packet result

Frozen decision events: **347**

- in-stream events with a safe pre-decision visual packet: **345**
- genuine pre-stream events: **2**

Canonical manifest:

`phase2-event-packet-manifest.csv`

The two pre-stream events remain manual evidence cases; no synthetic timestamp was created.

## First formal annotation tranche

To avoid mixing weak timing evidence into the first agreement study, a core tranche is frozen.

Eligibility:

- in-stream event;
- latest selected panel at least 20 seconds before event;
- latest panel timestamp quality is `HIGH` or `PIPELINE_GUARANTEED`;
- latest visual gap <= 180 seconds.

Result:

**254 events**

Blank scoring sheet:

`phase2-core-254-annotation-template.csv`

The local blind image bundle contains **939 pre-decision panel images** across those 254 events.

## Residual tranche

Residual events: **93**

- 91 in-stream cases need timestamp-quality and/or sparse-frame review;
- 2 are pre-stream cases.

Register:

`phase2-residual-93-review.csv`

Do not mix these into the first kappa calculation.

## Independence boundary

This ChatGPT conversation previously read the source-derived decision corpus.

Therefore annotations made by this same conversation cannot honestly count as an independent blinded annotator.

The earlier visual pilot remains:

`NON_SCORING_SAME_ANALYST`

Formal Phase 2 now requires a fresh annotator context that has not seen:

- Badar's eventual TRADE/WAIT/NO_TRADE labels;
- source paraphrases revealing the action;
- the prior extracted decision corpus;
- this conversation's pilot labels.

## Next exact action

Run **Independent Annotator A** on the 254-event blind core packet.

Then run a separately isolated **Independent Annotator B** on the same packet.

Only after both outputs are frozen:

1. compute raw agreement;
2. compute Cohen's kappa;
3. compute unresolved/conflict rates;
4. adjudicate disagreements outcome-blind;
5. run Formal Decision Policy v0.1;
6. reveal Badar's actual decision labels only for behavioral-fidelity scoring.

P&L remains sealed throughout.
