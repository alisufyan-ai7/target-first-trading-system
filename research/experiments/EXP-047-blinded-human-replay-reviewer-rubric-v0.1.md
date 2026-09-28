# EXP-047 — Blinded Human Replay Reviewer Rubric v0.1

**Status:** FROZEN BEFORE ANY REPLAY LABEL  
**Date:** 2026-09-28  
**Parent protocol:** `e5792f4d5980d288d339a82dc1271981534b7867`  
**Packet checkpoint:** `58ed6163c925b9081b35e53fd46dfa1043653bf6`

## Purpose

This rubric makes the human-style review consistent without turning EXP-047 into another deterministic signal engine.

The reviewer is allowed to synthesize context qualitatively. The reviewer is not allowed to inspect any candle or outcome after the frozen decision timestamp.

## Default posture

Default decision is:

`NO_TRADE`.

A trade is taken only when the causal context forms a coherent idea with a clear invalidation and meaningful target path.

Do not force a direction merely because a meaningful liquidity level was attacked.

## Context dimensions to inspect

The reviewer considers all of the following together.

### 1. Higher-timeframe state

From causal H1 / M15 history:

- directional trend versus balance/range;
- recent expansion versus compression;
- whether the attacked level sits with or against the prevailing directional auction;
- whether price is extended or still has room.

No single moving-average-style slope is sufficient by itself.

### 2. Location quality

Assess whether the attacked PDH/PDL/Asia/opening level is meaningful in the current structure:

- isolated external liquidity versus crowded nearby levels;
- edge of a broader range versus middle of congestion;
- confluence or conflict with recent higher-timeframe swing structure;
- clean room toward a plausible opposing liquidity objective.

### 3. Reaction after attack

Use only the 15 active M1 bars included before the decision timestamp.

Distinguish qualitatively among:

- rejection/reclaim;
- acceptance/hold;
- failed acceptance;
- indecision/chop;
- exhaustion after extension.

Look for persistence, displacement, inability to progress, reclaim/hold behavior, and structure change rather than one candle pattern.

### 4. Lower-timeframe execution quality

A trade requires a plausible non-chasing execution:

- clear causal entry or limit area;
- structural invalidation;
- no entry that depends on future retracement;
- no excessively distant stop with poor path quality;
- no need to "hope" through unresolved chop.

### 5. Target path / asymmetry

The target must be identified from causal structure already visible in the packet.

Avoid trades when:

- nearest meaningful opposing structure is too close;
- path is crowded;
- trade requires an exceptional extension merely to justify risk;
- entry/stop geometry creates poor asymmetry.

No later target hit information may influence the decision.

## Decision rules

### NO_TRADE

Choose NO_TRADE when the context is mixed, late, crowded, structurally unclear, or lacks clean entry/invalidation/target geometry.

NO_TRADE is a positive research decision, not a failure to classify.

### LONG / SHORT

Choose a direction only when the overall auction story, reaction, execution geometry, and target path agree sufficiently to justify risk.

The direction need not agree with the initial attack direction.

## Confidence

### A

Exceptionally coherent context:

- higher-timeframe state and location support the idea;
- post-attack reaction is clear rather than ambiguous;
- execution/invalidation are clean;
- target path is credible;
- little important contradictory evidence.

### B

Tradeable, but with one meaningful imperfection or conflict.

### C

A plausible trade idea with multiple weaknesses.

C trades are still recorded if genuinely tradeable, but they must not be upgraded later after outcomes are known.

## Frozen trade label fields

Every LONG/SHORT label must include:

- `decision`: LONG or SHORT;
- `confidence`: A/B/C;
- `entryStyle`: MARKET_NEXT_OPEN / LEVEL_RETEST / FVG_RETRACE / OTHER_CAUSAL_LIMIT;
- `entryPrice` or deterministic causal entry description;
- `stopPrice` or structural stop anchor;
- `tp1Price` or causal TP1 level;
- optional TP2;
- concise rationale using:
  - HTF state;
  - location;
  - attack/reaction;
  - execution;
  - target path;
- one concise `counterEvidence` field.

NO_TRADE must include:

- concise reason;
- the dominant conflict or missing condition.

## Anti-hindsight controls

During labeling:

- do not query source data after packet decision timestamps;
- do not open development outcome files for these replay IDs;
- do not inspect validation/holdout;
- do not search dates on external charting sites;
- do not change this rubric based on any label outcome;
- complete and checkpoint all 126 labels before any reveal.

## Feasibility gate

The parent protocol remains governing:

- all 126 labeled;
- >=30 LONG+SHORT total;
- >=10 LONG;
- >=10 SHORT;
- >=20 A/B trade labels;
- every trade has causal entry, stop, and target intent.

If these are not achieved naturally, do not manufacture trades to pass the gate.

## Reviewer identity

For v0.1, the reviewer is the project ChatGPT research agent acting as a blinded discretionary analyst under this rubric.

This does not imply real-money trading competence. The scientific question is whether the frozen causal judgments later show reproducible economic information.
