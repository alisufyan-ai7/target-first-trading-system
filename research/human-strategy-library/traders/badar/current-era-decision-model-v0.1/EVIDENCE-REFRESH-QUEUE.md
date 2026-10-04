# Badar Evidence Refresh Queue

## Purpose

Track new source evidence arriving after the v0.1 evidence boundary without contaminating the frozen v0.1 corpus or mechanization study.

## Frozen v0.1 source boundary

`d19a43da80ae0e3ab4207a73a35f317120d37c84`

This remains the source commit for:

- Current-Era Decision Model v0.1;
- 42-stream decision corpus;
- Formal Decision Policy v0.1;
- Mechanization v0.1 Phase 1;
- Phase-2 347-event frame manifest.

Do not silently append new sessions to those artifacts.

## Current external evidence HEAD checked 2026-10-05

`e77a73c739927d41e90e42b05a522a80b8fcabaf`

Ahead of v0.1 boundary by one commit.

### New stream queued

**PYPzCJV-YXE — 2026-10-01**

Source-layer note:

`notes/streams/PYPzCJV-YXE.md`

Observed source-only points relevant to a future v0.2 refresh:

- sell-side structural bias;
- main live short entered directly from an M15 inverse close after high sweep / sell-zone context;
- no lower-timeframe retrace was required for that main entry;
- Badar explicitly explains he chose the M15 entry because he expected no retracement;
- he distinguishes an early “hunting” entry from a higher-probability post-momentum-shift entry;
- lower-timeframe scalp idea described around 0.5% risk while main trade described around 1–1.5%;
- repeated refusal to sell lower after the move extended;
- multiple planned retrace entries were not chased when retracement did not occur;
- active management included partial closing area and stop reduction;
- exact main-trade stop was large in pips but accepted through risk sizing.

### Implications to test later, not apply to v0.1

This session appears directionally consistent with existing v0.1 findings:

1. explicit LTF confirmation is not universally required;
2. higher-timeframe close can itself be the decision evidence;
3. location/structure and invalidation geometry remain primary;
4. risk class depends on setup quality / timeframe / stop geometry;
5. no-chase behavior remains strong;
6. management remains adaptive.

It also suggests a future v0.2 formalization may need to distinguish:

- `HTF_CLOSE_DIRECT` as a first-class direct-entry branch;
- `SWEEP_HUNT_EARLY` versus `POST_MSS_CONFIRMED` risk classes.

Do not add those branches to frozen v0.1 until the v0.2 refresh is explicitly opened.

## Refresh rule

After v0.1 Phase-2 reproducibility is complete:

1. fetch the latest external source HEAD;
2. list all new source-layer streams since `d19a43d...`;
3. extract decision events outcome-blind;
4. compare against v0.1 policy;
5. classify each new event as:
   - supported by existing policy;
   - contradiction;
   - genuinely new branch;
   - unresolved;
6. only then create Decision Model / Formal Policy v0.2 if justified.

No P&L may be used to decide whether a new source behavior is admitted.


### New stream queued — PxDGTxs-Cvc — 2026-10-02

External evidence commit:

`1072f7d5dc477f662436167c25a71566d7e44314`

This daily catch-up commit adds the October 2 NFP live stream plus later forecast/video material.

For v0.1 governance:

- `PxDGTxs-Cvc` is **post-freeze**;
- its contact sheets may exist in the Phase-2 visual export artifact;
- it is excluded from the 42-stream v0.1 decision corpus;
- it is excluded from the 254-event v0.1 blind annotation tranche;
- it must be evaluated only in the future v0.2 evidence refresh.

Do not use its behavior to amend v0.1 mechanization before Phase-2 reproducibility is complete.
