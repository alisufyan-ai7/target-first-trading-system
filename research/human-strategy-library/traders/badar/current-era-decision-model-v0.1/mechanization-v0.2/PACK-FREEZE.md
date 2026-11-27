# Pack Freeze — Badar Mechanization v0.2

## Status

`BADAR_MECHANIZATION_V0_2_BLIND_PACKS_FROZEN — INDEPENDENT_ANNOTATION_PENDING`

The v0.2 annotation contract and reproducibility gates were frozen before pack generation.

No Badar TRADE/WAIT/NO_TRADE labels or outcomes were used to build these packs.

## Source/evidence boundary

External source repository:

`alisufyan-ai7/unpack-human-trading-strategies-claude`

Frozen evidence commit:

`bd0037e06a881a066e0cd8070b635cace59240d1`

Fresh streams:

- PYPzCJV-YXE — 2026-10-01
- PxDGTxs-Cvc — 2026-10-02
- EsAa5_T_kbQ — 2026-10-06
- D85FC79tI6w — 2026-10-08
- 6wwmBYPvmPQ — 2026-10-14
- _9vCesQpBtM — 2026-10-15
- of0Pv8JP4eE — 2026-10-23
- wXbKuO5lVGg — 2026-10-26

v0.1 cases reused:

**0**

## Candidate / visual packet

Candidate events:

**43**

Eligible cases:

**43**

Excluded:

**0**

Frozen frame-selection manifest:

`frame-selection-v0.2.csv`

Unique full-resolution source frames:

**102**

Total packet image uses:

**164**

Latest-frame gap:

- maximum: **182 seconds**
- median: **67 seconds**
- frozen maximum allowed: **240 seconds**

Packet metadata completeness:

**100%**

## Pack build

Successful GitHub Actions run:

`45954672567`

Artifacts:

- `badar-v02-annotator-A`
- `badar-v02-annotator-B`
- `badar-v02-sealed-crosswalk`
- `badar-v02-build-summary`

### Annotator A

43 blind cases.

SHA-256:

`8a3673345c3f35ffbfb8acc7ed7b6ede9e83210d48c563eb238dccdcac026a67`

### Annotator B

43 blind cases.

SHA-256:

`1561b0a9ea61b22b7968247ae39e4c18420a402479adc93513ba754dade2bca8`

### Sealed A/B crosswalk

The crosswalk itself is not committed to GitHub and must not be provided to either annotator.

SHA-256 commitment:

`8c8fd102539a2099b271a22d93733f9838c46a4cb73965d784abbf93b5dd3096`

A durable sealed artifact copy is retained outside the public repo for later scoring.

## Leak / integrity audit

Both A and B ZIPs:

- pass ZIP integrity checks;
- contain 43 case metadata files;
- contain 164 full-resolution pre-decision images;
- contain one annotation template;
- expose zero original stream IDs in filenames/text metadata;
- expose zero original v0.2 event IDs in filenames/text metadata;
- expose no actual TRADE / WAIT / NO_TRADE labels;
- expose no P&L, result R, MFE or MAE values.

The instructions mention forbidden terms such as P&L/MFE/MAE/NO_TRADE only to tell annotators what they must not access; those are not study data.

## Automatic vs human annotation fields

Per pack:

### confirmation_state

- 24 prefilled `NOT_YET`
- 2 prefilled `NONE`
- **17 human-judged CLOSED-confirmation cases**

The frozen minimum of 15 human confirmation cases is therefore satisfied.

### htf_close_state

- 41 prefilled `NOT_RELEVANT`
- 2 prefilled `REQUIRED_PENDING`
- 0 completed-required-close human cases

Thus v0.2 has 100% packet-derived HTF applicability and no standalone human HTF interpretation gate for this tranche, exactly as allowed by the frozen gate specification.

## Independent annotation requirement

The current Chat #09 has prior exposure to source evidence and cannot serve as Annotator A or B.

Annotator A and Annotator B must be run in two fresh isolated chats.

They may receive only:

- their own v0.2 pack;
- the bundled instructions.

They must not receive:

- this repository/project context;
- source notes/transcripts;
- the crosswalk;
- the other annotator's labels;
- Badar's eventual decision;
- P&L/outcome data.

## Frozen scoring sequence

After both completed annotation CSVs return:

1. verify A/B pack hash provenance;
2. verify sealed crosswalk hash;
3. map A/B blind IDs;
4. exclude any `prior_exposure=YES`;
5. compute agreement/kappa/unresolved rates using `REPRODUCIBILITY-GATES.md`;
6. derive direct-branch eligibility separately from each annotator's frozen labels;
7. if any required gate fails:
   `V0_2_REPRODUCIBILITY_FAIL_CLOSE_BEFORE_BEHAVIORAL_FIDELITY`;
8. only if all required gates pass may Badar TRADE/WAIT/NO_TRADE labels be revealed for behavior-fidelity analysis;
9. P&L remains sealed in either case.

## Freeze declaration

`BADAR_MECHANIZATION_V0_2_PACK_FREEZE_COMPLETE`
