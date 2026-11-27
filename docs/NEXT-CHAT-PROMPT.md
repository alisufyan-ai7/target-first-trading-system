# Ready-to-Paste Bootstrap Prompt for Chat #11

You are continuing the **Badar Tanveer Strategies / Target-First Trading System** project. This is **Chat #11**.

## Source of truth

GitHub is canonical. Do not rely on assumed memory from prior chats.

Main governing repository:

`alisufyan-ai7/target-first-trading-system`

External Badar evidence repository:

`alisufyan-ai7/unpack-human-trading-strategies-claude`

Before new research, fetch current main HEADs and read:

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

Also inspect commits/docs newer than this prompt.

## Historical result

v0.1 failed independent reproducibility and closed before behavior reveal:

`PHASE2_V0_1_INDEPENDENT_REPRODUCIBILITY_FAIL_CLOSE_BEFORE_BEHAVIORAL_FIDELITY`

Badar behavior labels and P&L remained sealed.

## Active v0.2 study

Frozen evidence boundary:

`bd0037e06a881a066e0cd8070b635cace59240d1`

Fresh tranche:

- 8 post-v0.1 live streams
- 43 candidate events
- 0 reused v0.1 cases
- 102 unique full-resolution pre-decision frames
- 43/43 packet eligible

Frozen pack identities:

- A: `8a3673345c3f35ffbfb8acc7ed7b6ede9e83210d48c563eb238dccdcac026a67`
- B: `1561b0a9ea61b22b7968247ae39e4c18420a402479adc93513ba754dade2bca8`
- crosswalk commitment: `8c8fd102539a2099b271a22d93733f9838c46a4cb73965d784abbf93b5dd3096`

## Latest intake checkpoint from Chat #10

The user reported both isolated annotators completed all 43 rows and prior exposure YES = 0.

Reported unresolved counts:

- A: location 0; late 1; structural stop 4; confirmation 0; HTF close 0; target path 1
- B: location 1; late 1; structural stop 1; confirmation 1; HTF close 0; target path 2

These are only marginal summaries. They are not enough to calculate agreement or kappa.

Current disposition:

`BADAR_MECHANIZATION_V0_2_ANNOTATION_RETURNS_REPORTED — FORMAL_CSV_INGESTION_AND_SCORING_PENDING`

## Exact next formal action

When the completed A and B CSVs are available:

1. verify both files contain exactly 43 expected rows and valid schema;
2. verify prior exposure/corruption exclusions;
3. verify pack provenance;
4. recover the sealed crosswalk and verify SHA-256 commitment `8c8fd102539a2099b271a22d93733f9838c46a4cb73965d784abbf93b5dd3096`;
5. pair A/B blind IDs;
6. compute raw agreement, Cohen's kappa, confusion matrices and unresolved rates exactly under `REPRODUCIBILITY-GATES.md`;
7. derive direct-branch eligibility independently from A/B labels;
8. if any required gate fails, close with `V0_2_REPRODUCIBILITY_FAIL_CLOSE_BEFORE_BEHAVIORAL_FIDELITY`;
9. only on full reproducibility PASS reveal Badar TRADE/WAIT/NO_TRADE for behavior fidelity;
10. keep P&L, result R, MFE/MAE and skipped-trade outcomes sealed.

Do not score from the aggregate unresolved summaries alone.

## Mandatory documentation

After every meaningful execution, update GitHub before treating the task as complete:

- `docs/current-status.md`
- `docs/decision-log.md`
- `docs/NEW-CHAT-HANDOFF.md`
- `docs/CHAT-LEDGER.md`
- `docs/NEXT-CHAT-PROMPT.md`
- `CHANGELOG.md`
- affected research README/freeze/manifest
- relevant GitHub issue(s)

Always leave exact disposition, next action, hashes/boundaries, and current Target-First HEAD.
