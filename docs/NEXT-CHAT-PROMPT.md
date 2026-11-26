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
7. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.1/phase2-independent-results-v2/PHASE2-INDEPENDENT-REPRODUCIBILITY-RESULT.md`
8. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.1/phase2-independent-results-v2/AGREEMENT-METRICS.csv`
9. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.2/README.md`

Also inspect any newer commits/docs added after this prompt was written.

## Critical frozen boundary

Badar Current-Era Decision Model v0.1 remains pinned to external source-evidence commit:

`d19a43da80ae0e3ab4207a73a35f317120d37c84`

Do not silently move that boundary.

Post-freeze evidence belongs to the evidence-refresh queue / future version unless explicitly admitted prospectively.

## Completed v0.1 Phase-2 result

The two independent fresh annotators completed all four batches each.

Submission integrity:

- Annotator A: 254/254
- Annotator B: 254/254
- duplicate blind IDs: 0
- unexpected blind IDs: 0
- prior exposure YES: 0

The rebuilt sealed A/B crosswalk commitment verified:

`474572c2e21d6d8f5a770f27ce0b9d5d837bd2c147691bb15b652334672ddbc1`

Final v0.1 disposition:

`PHASE2_V0_1_INDEPENDENT_REPRODUCIBILITY_FAIL_CLOSE_BEFORE_BEHAVIORAL_FIDELITY`

All seven frozen fields failed their gate.

Core fields:

- location_state: 45.3% raw agreement, kappa 0.285
- structural_stop_state: 78.0%, kappa 0.448
- htf_close_state: 18.5%, kappa -0.002
- late_state: 59.1%, kappa 0.315

Quality fields:

- confirmation_state: 41.3%, kappa 0.265
- target_path_state: 68.5%, kappa 0.310
- direct_branch_eligible: 52.4%, kappa 0.278

Important diagnostic nuance:

- structural-stop agreement is 99.4% among the 163 pairs where both annotators made a resolved call;
- target-path agreement is 85.8% among 162 resolved pairs;
- the largest systemic contract failure is HTF-close semantics;
- location, confirmation and chasing remain materially ambiguous.

## What must remain sealed

Do **not** reveal Badar's actual TRADE/WAIT/NO_TRADE labels merely to diagnose the v0.1 reproducibility failure.

Do **not** open:

- P&L
- result R
- MFE/MAE
- skipped-trade outcome

Do not perform a behavior-fidelity reveal for v0.1 unless a later explicit governance decision justifies a descriptive-only analysis.

Do not adjudicate v0.1 disagreements merely to manufacture a passing automated set.

## Current authorized research object

Mechanization v0.1 is closed.

Current next object:

**Badar Mechanization v0.2 — prospective outcome-blind representation/annotation redesign.**

Canonical brief:

`research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.2/README.md`

Tracking:

GitHub issue #2.

v0.2 may use only:

- aggregate v0.1 A/B disagreement structure;
- source-derived definitions already available before outcomes;
- representation/contract deficiencies exposed by the blind study.

It may not use:

- v0.1 Badar actual decisions;
- any P&L/outcome information;
- outcome-conditioned threshold selection.

## v0.2 priorities

1. prospectively identifiable candidate direction;
2. frozen intended POI / entry-area anchor;
3. active timeframe + candle open/closed metadata;
4. precise HTF-close semantics:
   - NOT_RELEVANT
   - REQUIRED_PENDING
   - NEUTRAL
   - CONFIRMS
   - INVALIDATES
   - FLIPS_BIAS
   - UNRESOLVED
5. structural-stop visible vs inferable distinction;
6. explicit first-objective / blocker target-path contract;
7. frozen confirmation reference boundary/family;
8. explicit chasing anchor.

## Fresh-test rule

Do not redesign on the 254 v0.1 cases and then rescore those same cases as if they were fresh validation.

The next reproducibility test must use a prospectively separate evidence tranche.

Preferred source:

post-freeze Badar live sessions after `d19a43d...`.

## Next exact action

Proceed directly with:

1. fetch the latest external Badar evidence repo HEAD;
2. identify all source-layer live streams after the v0.1 cutoff;
3. audit enough post-freeze streams to define a fresh v0.2 evidence boundary;
4. freeze that boundary before any blind labels;
5. design the enriched v0.2 packet/annotation contract;
6. predeclare reproducibility gates;
7. build fresh blinded packets;
8. run new independent annotators;
9. score reproducibility;
10. only if v0.2 reproducibility passes may behavior-fidelity reveal be considered;
11. P&L remains sealed until a later explicit promotion gate.

## Mandatory documentation behavior

After every meaningful execution, update GitHub before considering the task complete.

At minimum evaluate/update:

- `docs/current-status.md`
- `docs/decision-log.md`
- `docs/NEW-CHAT-HANDOFF.md`
- `docs/CHAT-LEDGER.md`
- `docs/NEXT-CHAT-PROMPT.md`
- `CHANGELOG.md`
- affected research README/freeze/manifest
- relevant GitHub issue(s)

Always leave the repository with:

- exact disposition;
- exact next action;
- current hashes/commits;
- enough context for another fresh chat to resume from GitHub alone.

## Working style

Act rather than repeatedly asking for confirmation.

Do not create another ChatGPT-only OHLC strategy/replay variant.

Do not rescue failed experiments with favorable subsets.

Do not open protected validation periods or P&L early.

Use the external Claude repo as source evidence and Target-First as the governing strategy/research repository.

At the end of a substantial step, report the new Target-First HEAD and the exact next formal action.
