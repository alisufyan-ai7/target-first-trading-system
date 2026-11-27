# Project Governance — Source of Truth and Chat Continuity

## Canonical source of truth

The durable source of truth for the Target-First Trading System project is GitHub:

`alisufyan-ai7/target-first-trading-system`

Chat conversation context is working memory only. No important research result, methodological decision, freeze boundary, active dependency, or next-step instruction should exist only in chat.

Badar source extraction is maintained separately in:

`alisufyan-ai7/unpack-human-trading-strategies-claude`

That external repository is an evidence feed. Target-First owns strategy synthesis, formalization, experiments, validation governance, project status, decision logs and handoffs.

## Mandatory post-execution checkpoint

After every meaningful research or engineering execution, update GitHub before treating the task as complete.

At minimum check whether each of these needs an update:

1. `docs/current-status.md`
   - current scientific/project state;
   - exact disposition;
   - active dependency;
   - next exact action.

2. `docs/decision-log.md`
   - any methodological, governance, data-boundary, freeze, promotion, rejection or architecture decision.

3. `docs/NEW-CHAT-HANDOFF.md`
   - compact but sufficient latest checkpoint for a fresh chat.

4. `CHANGELOG.md`
   - durable record of new artifacts/results.

5. `docs/CHAT-LEDGER.md`
   - current chat number;
   - next chat number;
   - current handoff state.

6. `docs/NEXT-CHAT-PROMPT.md`
   - always keep a ready-to-paste bootstrap prompt for the next chat.

7. Relevant research directory README / freeze / manifest
   - when the execution changes the scientific object itself.

A task is not fully checkpointed until the relevant docs and exact commit hashes are durable in GitHub.

## HEAD verification

At the end of a substantial execution:

- fetch and record the current Target-First `main` HEAD;
- when external Badar evidence was consulted, fetch the external repo HEAD too;
- keep frozen evidence commits distinct from moving repository HEADs.

Do not silently reinterpret a moving external HEAD as part of an already frozen study.

## Chat numbering

Current working conversation:

`Chat #09`

Next conversation:

`Chat #10`

When Chat #09 approaches its context/conversation limit, do not rely on manual recollection.

Before transition:

1. checkpoint all current work to GitHub;
2. update `docs/NEW-CHAT-HANDOFF.md`;
3. update `docs/NEXT-CHAT-PROMPT.md`;
4. verify repository HEADs;
5. give the user the ready prompt from `docs/NEXT-CHAT-PROMPT.md`.

The new chat must recover project state from GitHub before doing new work.

## Attachment / artifact rule

Conversation-generated downloads and sandbox attachments can expire.

Therefore:

- never use a chat attachment as the only durable record of an important research object;
- record hashes, provenance, composition and regeneration instructions in GitHub;
- when an attachment is rebuilt, create a new active manifest/version rather than silently pretending the expired bytes still exist;
- keep sealed mappings/private crosswalks out of public research packs while committing cryptographic commitments where useful.

## Scientific integrity rule

Documentation must distinguish:

- source evidence;
- researcher/model inference;
- frozen hypotheses/policies;
- development data;
- protected/sealed validation data;
- post-freeze evidence deltas.

Do not update historical frozen rules based on later outcomes.

Do not expose P&L/outcomes before the currently authorized blind-study stage permits it.

## Current Badar study guardrails

Historical v0.1 decision-model evidence boundary:

`d19a43da80ae0e3ab4207a73a35f317120d37c84`

Historical v0.1 disposition:

`PHASE2_V0_1_INDEPENDENT_REPRODUCIBILITY_FAIL_CLOSE_BEFORE_BEHAVIORAL_FIDELITY`

Active v0.2 evidence boundary:

`bd0037e06a881a066e0cd8070b635cace59240d1`

Active v0.2 study:

- 8 fresh post-v0.1 live streams;
- 43 fresh candidate events;
- 0 reused v0.1 cases;
- frozen annotation contract and reproducibility gates;
- frozen A/B blind packs and sealed crosswalk commitment.

User-reported independent-annotation intake on 2026-11-27:

- Annotator A reports 43/43 rows complete and prior exposure YES = 0;
- Annotator B reports 43/43 rows complete and prior exposure YES = 0;
- only aggregate unresolved counts have been provided to the governing Chat #10 so far;
- completed row-level CSVs have not yet been ingested in Chat #10.

Current formal stage:

`BADAR_MECHANIZATION_V0_2_ANNOTATION_RETURNS_REPORTED — FORMAL_CSV_INGESTION_AND_SCORING_PENDING`

No raw agreement, Cohen's kappa, confusion matrix, or promotion decision may be inferred from the marginal unresolved-count summaries alone.

Exact next formal action:

1. ingest the completed Annotator A and Annotator B CSV files;
2. verify schema/provenance and frozen pack identities;
3. recover and verify the sealed crosswalk against commitment `8c8fd102539a2099b271a22d93733f9838c46a4cb73965d784abbf93b5dd3096`;
4. pair A/B labels and apply the predeclared v0.2 reproducibility gates;
5. reveal Badar TRADE/WAIT/NO_TRADE only if every required gate passes;
6. keep P&L/result-R/MFE/MAE sealed in either case.

Current working conversation:

`Chat #10`

Next conversation:

`Chat #11`

The ready bootstrap prompt for the next conversation is maintained in `docs/NEXT-CHAT-PROMPT.md`.
