# Badar Current-Era Decision Model v0.1

**Status:** EVIDENCE SYNTHESIS ONLY  
**Created:** 2026-10-01  
**P&L / outcome test:** NOT RUN  
**Engine status:** NOT AN ENGINE  
**Deployable:** NO

## Purpose

This artifact reconstructs the current-era decision process used by Badar Tanveer from the separate evidence repository:

`alisufyan-ai7/unpack-human-trading-strategies-claude`

The model is intentionally a **decision hierarchy**, not a list of chart patterns.

It asks:

> At a live Gold decision point, what sequence of questions appears to make Badar choose TRADE, WAIT, NO_TRADE, REDUCE_RISK, HOLD, PARTIAL, or EXIT?

## Frozen evidence snapshot

External evidence repository:

`alisufyan-ai7/unpack-human-trading-strategies-claude`

Pinned source commit for v0.1:

`d19a43da80ae0e3ab4207a73a35f317120d37c84`

Latest live session included:

`EOBnMz2Y_9k` — 2026-09-30 NY-session Gold live stream.

At this snapshot the external repository records:

- 143 long videos;
- 114 Shorts;
- 42 live streams;
- 113 live-trade rows.

Only the repository's **source layer** is evidence for this model. `derived/**` is explicitly excluded.

## Current-era priority

Evidence is weighted by recency and directness:

1. **Highest weight:** 2026 live-stream actions and explicit skip/wait explanations.
2. **High weight:** 2024–2026 Liquidity Concept teaching that agrees with live behavior.
3. **Supporting weight:** older SMC/ICT material when it remains consistent with current behavior.
4. **Background only:** older course rules that conflict with later behavior.

## Core finding

The current-era method is best represented as:

```text
ENVIRONMENT / EVENT RISK
        ↓
HTF DIRECTIONAL CONTEXT
        ↓
MEANINGFUL LOCATION
        ↓
LIQUIDITY / TRAP / RETRACEMENT EVENT
        ↓
CANDLE-CLOSE / STRUCTURE CONFIRMATION
        ↓
EXECUTION FEASIBILITY
        ↓
RISK CLASSIFICATION
        ↓
TRADE / WAIT / NO_TRADE
        ↓
ACTIVE PREMISE MANAGEMENT
```

The entry pattern is therefore **not the strategy by itself**.

Engulfing, inverse closing, two-candle rejection, momentum shift, FVG, OB and session sweeps are lower-level components inside a larger selection process.

## Most important v0.1 conclusion

The strongest recurring discriminator is:

> **location and context decide whether a confirmation matters.**

Repeated live behavior shows that Badar will ignore or delay otherwise recognizable patterns when:

- price is in the middle;
- price is at the wrong extreme;
- the relevant higher-timeframe candle has not closed;
- the move has already left and entry would be chasing;
- a logical structural stop cannot be placed;
- the stop would be too large for the intended trade;
- confirmation is weak or contradicted by the next close;
- the broader direction makes the idea lower probability.

This makes `NO_TRADE` and `WAIT` first-class outputs of the model.

## Model outputs

### Pre-entry

- `NO_TRADE`
- `WAIT`
- `TRADE_NORMAL_RISK`
- `TRADE_REDUCED_RISK`

### Post-entry

- `HOLD`
- `REDUCE_RISK`
- `PARTIAL`
- `MOVE_PROTECTION`
- `EXIT_INVALIDATED`
- `RUNNER_TO_LIQUIDITY`

These are descriptive states reconstructed from source behavior. They are **not yet executable rules**.

## Files

- `SOURCE-BOUNDARY.md` — exact external evidence boundary and versioning policy.
- `DECISION-MODEL.md` — hierarchical decision model.
- `EVIDENCE-MATRIX.md` — source support and contradiction map.
- `DECISION-EVENT-SCHEMA.md` — outcome-blind schema for extracting trade and no-trade decisions.
- `NEXT-STUDY.md` — next research stage before any P&L test.

## Explicit non-goals

v0.1 does **not**:

- claim Badar is profitable;
- treat social-media/live-stream performance as verified;
- calculate expectancy, win rate, profit factor or drawdown;
- select a new target/stop parameter;
- create Engine U or any other engine;
- choose between contradictory source rules by looking at historical P&L;
- use Claude's `derived/**` automation rules as Badar evidence.

## Promotion rule

The model can advance toward formalization only after an outcome-blind decision-event corpus contains both:

- accepted trades; and
- comparable `WAIT` / `NO_TRADE` decisions.

Only then may the stable decision gates be translated into a frozen development hypothesis.
