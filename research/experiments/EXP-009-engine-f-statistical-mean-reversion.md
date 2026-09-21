# EXP-009 — Engine F Statistical Mean-Reversion Screen

**Status:** IN PROGRESS — ENGINE F v0.1 RULES FROZEN BEFORE OUTCOME INSPECTION  
**Date:** 2026-09-22

## Purpose

Test a genuinely independent opportunity stream after EXP-008 paused further Engine A market expansion.

## Question

Can a simple price-only statistical extension -> re-entry -> mean-reversion engine produce positive target-first expectancy in both development and holdout while adding an opportunity stream structurally independent from Engines A-E?

## Frozen strategy

Use `strategies/engine-f-statistical-mean-reversion/SPEC-v0.1-portable.md` unchanged.

Core logic:

1. 60-minute rolling mean/std from completed 5m closes;
2. detect |z| >= 2.0 extension;
3. require re-entry to |z| <= 1.5 on the relevant side within 30 minutes;
4. enter at the next 1m open;
5. stop beyond the excursion extreme by 0.25 x 5m ATR(14);
6. accept only if the rolling mean is at least 2.5R away in the reversion direction;
7. risk USD 20 to target USD 50 (+2.5R);
8. conservative same-bar handling and 20:00 UTC timeout;
9. one open Engine F trade per instrument plus reset/cooldown rule.

## Data

Use the already documented provisional external GetData one-minute samples from EXP-006.

Common split:

- development: 2026-03-12 through 2026-05-31;
- holdout: 2026-06-01 through 2026-08-20.

This feed remains provisional research data. Any finalist still requires independent-feed and broker-specific cost validation.

## Checkpoint sequence

Run and write back one market at a time:

1. XAUUSD;
2. USDJPY;
3. EURUSD;
4. GBPUSD.

Do not alter parameters between markets.

## Promotion discipline

A single positive holdout is not sufficient.

A market arm can remain a research lead only if:

- development and holdout mean R are both positive or at minimum do not show a clear sign-instability pattern;
- the result is not driven by a tiny sample;
- daily-distribution and economic-feasibility diagnostics are explicitly reported.

Do not tune failed arms after seeing holdout.

## Next action

Run the XAUUSD checkpoint under the frozen Engine F rules, record the complete result, then decide only whether to continue unchanged to USDJPY.
