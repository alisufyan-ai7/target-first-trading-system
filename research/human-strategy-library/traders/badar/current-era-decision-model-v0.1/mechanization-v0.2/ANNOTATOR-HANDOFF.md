# Independent Annotator Handoff — Badar Mechanization v0.2

## Active packs

### Annotator A

File:

`annotator-A-badar-v0.2.zip`

SHA-256:

`8a3673345c3f35ffbfb8acc7ed7b6ede9e83210d48c563eb238dccdcac026a67`

### Annotator B

File:

`annotator-B-badar-v0.2.zip`

SHA-256:

`1561b0a9ea61b22b7968247ae39e4c18420a402479adc93513ba754dade2bca8`

## Sealed mapping

Crosswalk SHA-256 commitment:

`8c8fd102539a2099b271a22d93733f9838c46a4cb73965d784abbf93b5dd3096`

Do not give the crosswalk to either annotator.

## Required isolation

Create two fresh chats **outside this project context**.

Do not give either chat:

- Target-First repository link;
- Claude evidence repository link;
- Badar source notes/transcripts;
- this research conversation;
- the other annotator pack;
- the crosswalk;
- Badar decision labels;
- P&L/outcomes.

## Prompt for Annotator A

Upload only the A ZIP and say:

> Act only as Independent Annotator A for this blinded chart-state study. Follow the bundled INSTRUCTIONS.md exactly. Use only the supplied files and images. Do not browse the web, GitHub, YouTube, Badar material, prior chats, or external sources. Do not try to infer profitability or what the trader eventually did. Complete annotation-template.csv for all cases, preserve any prefilled automatic states, use UNRESOLVED rather than guessing, and return the completed CSV plus only the short summary requested by the instructions.

## Prompt for Annotator B

Upload only the B ZIP and use the same prompt, replacing `Annotator A` with `Annotator B`.

## Expected return

Two completed CSV files:

- Annotator A completed `annotation-template.csv`
- Annotator B completed `annotation-template.csv`

Bring both back to the governing Target-First research chat.

## Formal scoring after return

The governing chat will:

1. hash/integrity-check both returns;
2. retrieve the sealed mapping;
3. verify the crosswalk commitment;
4. pair A/B blind IDs;
5. exclude any prior-exposure cases;
6. apply `REPRODUCIBILITY-GATES.md`;
7. compute raw agreement, kappa, confusion matrices and unresolved rates;
8. derive direct-branch eligibility independently from A/B labels;
9. close before behavior reveal if a required gate fails;
10. only on full reproducibility pass reveal Badar TRADE/WAIT/NO_TRADE for behavior fidelity.

P&L remains sealed.
