# Ready-to-Paste Bootstrap Prompt for Chat #10

You are continuing the **Badar Tanveer Strategies / Target-First Trading System** project. This is **Chat #10**.

## Source of truth

GitHub is canonical. Do not rely on assumed memory from prior chats.

Main governing repository:

`alisufyan-ai7/target-first-trading-system`

External Badar evidence repository:

`alisufyan-ai7/unpack-human-trading-strategies-claude`

Before any new research, fetch the **current main HEADs** and read the current versions of:

1. `docs/PROJECT-GOVERNANCE.md`
2. `docs/current-status.md`
3. `docs/decision-log.md`
4. `docs/NEW-CHAT-HANDOFF.md`
5. `docs/CHAT-LEDGER.md`
6. `CHANGELOG.md`
7. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.1/phase2-independent-results-v2/PHASE2-INDEPENDENT-REPRODUCIBILITY-RESULT.md`
8. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.2/README.md`
9. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.2/SOURCE-BOUNDARY.md`
10. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.2/ANNOTATION-CONTRACT.md`
11. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.2/REPRODUCIBILITY-GATES.md`
12. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.2/PACK-FREEZE.md`
13. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.2/active-pack-manifest-v0.2.csv`
14. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.2/ANNOTATOR-HANDOFF.md`

Also inspect newer commits/docs added after this prompt was written.

## Historical v0.1 result

v0.1 decision-model evidence boundary remains:

`d19a43da80ae0e3ab4207a73a35f317120d37c84`

The v0.1 independent visual mechanization study failed reproducibility before behavioral-fidelity reveal:

`PHASE2_V0_1_INDEPENDENT_REPRODUCIBILITY_FAIL_CLOSE_BEFORE_BEHAVIORAL_FIDELITY`

Do not reopen v0.1 behavior labels or P&L to rescue it.

## Current authorized study — Mechanization v0.2

v0.2 uses a genuinely fresh prospective evidence tranche.

Frozen external evidence commit:

`bd0037e06a881a066e0cd8070b635cace59240d1`

Fresh live streams:

- PYPzCJV-YXE — 2026-10-01
- PxDGTxs-Cvc — 2026-10-02
- EsAa5_T_kbQ — 2026-10-06
- D85FC79tI6w — 2026-10-08
- 6wwmBYPvmPQ — 2026-10-14
- _9vCesQpBtM — 2026-10-15
- of0Pv8JP4eE — 2026-10-23
- wXbKuO5lVGg — 2026-10-26

Fresh candidate events:

**43**

v0.1 cases reused:

**0**

## v0.2 representation changes

The blind packet supplies prospectively frozen:

- candidate direction
- directional context
- intended POI
- entry-area anchor
- relevant context timeframe
- confirmation timeframe/reference
- confirmation-candle status
- required HTF-close applicability
- structural-stop anchor
- first objective
- blocker anchor when prospectively known

Annotators judge those supplied candidates rather than independently inventing the setup.

`direct_branch_eligible` is derived later rather than manually labeled.

## v0.2 visual packet

Frozen frame-selection manifest:

`mechanization-v0.2/frame-selection-v0.2.csv`

Statistics:

- 43/43 eligible
- 102 unique full-resolution source frames
- 164 image uses per annotator
- max latest-frame gap 182 sec
- median latest-frame gap 67 sec
- frozen max allowed 240 sec

## Frozen annotation gates

Read:

`mechanization-v0.2/REPRODUCIBILITY-GATES.md`

Key human-label gates include:

- location_state: raw >=85%, kappa >=0.70, unresolved <=10% each
- structural_stop_visibility: same
- late_state applicable cases: same
- confirmation_state human cases: raw >=80%, kappa >=0.60, unresolved <=15%, minimum 15
- target_path_state: raw >=80%, kappa >=0.60, unresolved <=15%

Confirmation sample composition:

- 24 automatic NOT_YET
- 2 automatic NONE
- 17 human CLOSED-confirmation cases

HTF applicability:

- 41 automatic NOT_RELEVANT
- 2 automatic REQUIRED_PENDING
- no human completed-required-close cases in this tranche

## Active v0.2 independent packs

Current disposition:

`BADAR_MECHANIZATION_V0_2_BLIND_PACKS_FROZEN — INDEPENDENT_ANNOTATION_PENDING`

Annotator A SHA-256:

`8a3673345c3f35ffbfb8acc7ed7b6ede9e83210d48c563eb238dccdcac026a67`

Annotator B SHA-256:

`1561b0a9ea61b22b7968247ae39e4c18420a402479adc93513ba754dade2bca8`

Sealed crosswalk commitment:

`8c8fd102539a2099b271a22d93733f9838c46a4cb73965d784abbf93b5dd3096`

Successful pack build:

`45954672567`

The crosswalk itself is deliberately not in GitHub and must never be shown to either annotator.

## Immediate next action

The user must run two fresh isolated chats:

### Annotator A

Give only the A v0.2 ZIP.

### Annotator B

Give only the B v0.2 ZIP.

Use the exact handoff instructions in:

`mechanization-v0.2/ANNOTATOR-HANDOFF.md`

Do not give annotators:

- project/GitHub context
- source notes/transcripts
- stream IDs/event IDs
- crosswalk
- Badar eventual decisions
- other annotator labels
- P&L/outcomes

## When completed A/B CSVs return

Proceed directly:

1. verify submission rows/schema and pack provenance;
2. retrieve the sealed v0.2 crosswalk from the project/private file surface;
3. verify its SHA-256 equals:
   `8c8fd102539a2099b271a22d93733f9838c46a4cb73965d784abbf93b5dd3096`;
4. pair A/B labels to the 43 frozen events;
5. exclude `prior_exposure=YES`;
6. apply exactly the predeclared v0.2 reproducibility gates;
7. compute raw agreement, Cohen's kappa, confusion matrices and unresolved rates;
8. derive direct-branch eligibility separately from A/B frozen labels;
9. if any required gate fails:
   `V0_2_REPRODUCIBILITY_FAIL_CLOSE_BEFORE_BEHAVIORAL_FIDELITY`;
10. if and only if all required gates pass, reveal Badar's TRADE/WAIT/NO_TRADE labels for behavioral-fidelity analysis;
11. still keep P&L, result R, MFE/MAE and skipped-trade outcomes sealed.

## Do not

- annotate these packs from this governing chat;
- tune the v0.2 contract after seeing A/B disagreement and rescore the same cases as fresh validation;
- reveal Badar decisions early;
- open P&L;
- create another ChatGPT-only OHLC engine;
- use favorable subsets to rescue failed research.

## Mandatory documentation

After every meaningful execution, update GitHub before considering the task complete.

Evaluate/update:

- `docs/current-status.md`
- `docs/decision-log.md`
- `docs/NEW-CHAT-HANDOFF.md`
- `docs/CHAT-LEDGER.md`
- `docs/NEXT-CHAT-PROMPT.md`
- `CHANGELOG.md`
- affected research README/freeze/manifest
- relevant GitHub issue(s)

Always leave:

- exact current disposition;
- exact next action;
- relevant hashes/commit boundaries;
- enough context for another fresh chat to resume from GitHub alone.

At the end of a substantial step, report the current Target-First HEAD and the exact next formal action.
