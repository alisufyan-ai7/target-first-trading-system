# Human-Trader Edge Decomposition v0.1

**Date:** 2026-09-25  
**Status:** GOVERNING RESEARCH FRAMEWORK — NOT A STRATEGY

## Purpose

The project must stop treating profitable day trading as a search for the next chart formula.

A skilled human trader typically combines several information layers and, critically, **skips** many technically valid-looking setups.

The system should therefore be built by proving each information layer before turning it into a strategy.

## Expert-process decomposition

The working causal sequence is:

`catalyst/regime -> structural location -> participation/market interpretation -> trigger -> non-chasing execution -> structural stop -> target path -> EV/ranking -> equity-adaptive sizing`.

### Layer 1 — Catalyst / regime

Questions:

- Is a major release imminent or just released?
- Was the release a meaningful surprise versus consensus?
- Is the market repricing growth, inflation, labor, or monetary policy?
- Is this a normal-liquidity period or a news regime?

Potential data:

- scheduled release timestamp;
- actual;
- consensus;
- prior/revision;
- release family;
- event importance.

### Layer 2 — Structural location

Questions:

- Is price at a meaningful prior high/low, session range, or confirmed swing?
- Is there room to a plausible opposing liquidity target?
- Is the market in the middle of noise?

EXP-040 found that **generic** MTF OHLC context by itself did not add stable information. That does not authorize discarding structure; it means structure should be used when tied to a stronger economic/participation mechanism.

### Layer 3 — Participation / interpretation

Questions:

- Did rates and USD react consistently with the macro surprise?
- Is Gold/FX order flow confirming or rejecting the initial repricing?
- Is there absorption or liquidity depletion?
- Is spread/depth deteriorating?

This is where professional information may exist that is absent from OHLC.

### Layer 4 — Trigger / execution

Use local price behavior only after the information/context layer has earned attention.

Examples:

- sweep and failure;
- displacement and retracement;
- failed breakout;
- pullback/retest;
- non-chasing limit.

Engine Q showed that execution quality can materially improve expectancy, but cannot create a predictor edge.

### Layer 5 — Target path / monetization

Estimate:

- T30/T40/T50/T70/T100 probability;
- MFE/MAE;
- time to target;
- structural room;
- partial/runner continuation probability;
- expected value after realistic costs.

### Layer 6 — Risk / compounding

Risk comes last.

- current equity;
- validated edge;
- stop distance;
- lot step;
- margin/notional;
- daily loss state;
- correlated exposure;
- withdrawal/retained-profit policy.

Do not increase risk to manufacture profitability.

## Research discipline

A new information layer is allowed into a future engine only if it adds stable out-of-sample information beyond the simpler baseline.

A failed information layer is documented and left behind.

Do not iterate tiny thresholds until something passes.

## Immediate implication after EXP-040

Generic 15M/1H/4H/prior-day/session OHLC context did not pass.

The next useful question is therefore **macro/catalyst information**, followed by rates/market interpretation and then execution-grade order flow.

## Anti-loop rule

Before every new experiment ask:

1. Is this genuinely new information, or just another transform of the same prices?
2. Is there enough independent history to test it?
3. Is the economic mechanism explicit?
4. Is the result useful even if negative?
5. Will a negative result tell us where to go next?

If any answer is no, do not run the experiment.
