# Ready-to-Paste Bootstrap Prompt for Chat #10

You are continuing the **Badar Tanveer Strategies / Target-First Trading System** project. This is **Chat #10**.

## Source of truth

GitHub is the canonical source of truth. Do not rely on assumed memory from prior chats.

Main project repository:

`alisufyan-ai7/target-first-trading-system`

External Badar source-evidence repository:

`alisufyan-ai7/unpack-human-trading-strategies-claude`

Before doing new research, use the GitHub connector to fetch the **current main HEADs** and read the latest versions of:

1. `docs/PROJECT-GOVERNANCE.md`
2. `docs/current-status.md`
3. `docs/decision-log.md`
4. `docs/NEW-CHAT-HANDOFF.md`
5. `docs/CHAT-LEDGER.md`
6. `CHANGELOG.md`
7. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.1/PHASE2-PANEL-SPLIT-AND-PACKET-REPORT.md`
8. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.1/INDEPENDENT-ANNOTATOR-INSTRUCTIONS.md`
9. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.1/phase2-independent-pack-manifest-v2.csv`
10. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.1/PHASE2-REBUILT-PACK-HASHES-2026-11-27.md`

Also inspect any newer commits/docs added after this prompt was written.

## Critical frozen boundaries

Badar Current-Era Decision Model v0.1 is pinned to external source-evidence commit:

`d19a43da80ae0e3ab4207a73a35f317120d37c84`

Do not silently move that evidence boundary even if the external evidence repo has newer sessions.

Post-freeze sessions belong to the evidence-refresh queue / future v0.2 unless explicitly admitted prospectively.

Protected P&L/outcomes remain sealed.

No development backtest is currently authorized.

## Current Phase-2 state

The study has:

- 347 frozen pre-entry decision events;
- 254-event conservative independent-annotation core tranche;
- 93-event residual review tranche;
- Formal Decision Policy v0.1 frozen outcome-blind;
- Phase-1 hard-gate mechanization frozen;
- source visual panels already constructed.

The original October A/B attachment bytes expired.

**Use only the active rebuilt v2 packs**, not the historical v1 pack hashes.

Active v2 pack hashes:

- Annotator A:
  `e972eea554b77636021f1a37b9662e47867089bff00960ba33604a52ee883e95`
- Annotator B:
  `285caff6000667a01758bedf5904bfa01f5862054d4908c9cd7179586063a45d`
- rebuilt sealed crosswalk SHA-256 commitment:
  `474572c2e21d6d8f5a770f27ce0b9d5d837bd2c147691bb15b652334672ddbc1`

The user is currently running two separate fresh isolated chats as Independent Annotator A and Independent Annotator B.

Each annotator covers four paired folds:

`64 / 64 / 63 / 63`

A and B use different blind IDs/order.

They must not see:

- original stream IDs/event IDs;
- Badar's TRADE/WAIT/NO_TRADE labels;
- source notes/transcripts;
- later management;
- P&L;
- outcome R;
- MFE/MAE;
- the sealed A/B crosswalk;
- the other annotator's labels.

## Next formal action

If the user returns the 8 completed annotation CSVs, do not ask unnecessary questions.

Proceed directly to:

1. inspect all 8 files;
2. verify expected batch/event counts;
3. verify the active v2 pack provenance/hashes where possible;
4. load the sealed rebuilt crosswalk from the current Project attachment/file surface if available;
5. verify its SHA-256 equals:
   `474572c2e21d6d8f5a770f27ce0b9d5d837bd2c147691bb15b652334672ddbc1`;
6. map Annotator A and B blind IDs to the same frozen original events;
7. exclude `PRIOR_EXPOSURE` cases;
8. compute raw percent agreement for each categorical field;
9. compute Cohen's kappa where class support permits;
10. compute confusion matrices;
11. compute UNRESOLVED rates;
12. compare results to the frozen reproducibility gates;
13. preserve all disagreements;
14. adjudicate disagreements **outcome-blind** using only the frozen derivation contract and pre-decision visual evidence;
15. freeze final state labels;
16. replay Formal Decision Policy v0.1;
17. only after that reveal Badar's actual TRADE/WAIT/NO_TRADE labels for behavioral-fidelity analysis;
18. still do not open P&L unless a later explicit gate authorizes it.

If only some annotator CSVs have returned, verify and checkpoint them but do not compute final A/B kappa prematurely.

## Mandatory documentation behavior

After every meaningful execution, update GitHub before considering the task complete.

At minimum evaluate/update:

- `docs/current-status.md`
- `docs/decision-log.md`
- `docs/NEW-CHAT-HANDOFF.md`
- `docs/CHAT-LEDGER.md`
- `docs/NEXT-CHAT-PROMPT.md`
- `CHANGELOG.md`
- any affected research README/freeze/manifest

Always leave the repository with:

- exact current disposition;
- exact next action;
- current hashes/commits;
- enough context for another fresh chat to resume without reading old chat history.

Do not let important project knowledge exist only in the conversation.

## Working style

Act rather than repeatedly asking for confirmation.

Do not create another ChatGPT-only OHLC strategy/replay variant.

Do not use favorable post-hoc subsets to rescue failed experiments.

Do not open protected validation periods or P&L early.

Use the external Claude repo as source evidence, and Target-First as the governing strategy/research repository.

When finished with a substantial step, report the new Target-First HEAD and the exact next formal action.
