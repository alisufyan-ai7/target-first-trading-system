# EXP-010 — Two-Lead Portfolio Daily-Distribution Screen

**Status:** IN PROGRESS — PORTFOLIO RULES FROZEN BEFORE COMBINATION RESULTS  
**Date:** 2026-09-22

## Purpose

Test whether the two existing, structurally independent research leads materially improve the project-level daily P&L distribution when combined without changing either strategy.

## Frozen input leads

1. **USDJPY / Engine A v0.2**
   - exact rules from `strategies/engine-a-liquidity-mss-fvg/SPEC-v0.2-portable.md`;
   - research-lead status from EXP-007.

2. **GBPUSD / Engine F v0.1**
   - exact rules from `strategies/engine-f-statistical-mean-reversion/SPEC-v0.1-portable.md`;
   - research-lead status from EXP-009.

No signal, stop, target, session, or sizing parameter may be changed in EXP-010.

## Data and split

Use the same provisional GetData one-minute feed and common split used by EXP-007/009:

- development: 2026-03-12 through 2026-05-31;
- holdout: 2026-06-01 through 2026-08-20.

This remains a same-feed portfolio screen, not independent validation.

## Stream reconstruction rule

Regenerate each lead from its frozen specification and verify that its standalone counts/summary agree with the recorded experiment closely enough to establish implementation consistency.

The portfolio consumes the **standalone accepted trade streams**.

If the portfolio rejects a precomputed trade because of a portfolio risk/state rule, suppressed alternative signals are **not reactivated**. This keeps the experiment deterministic and avoids branch-dependent post-hoc opportunity creation.

## Portfolio state machine

Reference equity: USD 500.

Per accepted trade:

- gross stop risk: USD 20;
- target: USD 50 / +2.5R.

Portfolio controls:

1. maximum 4 new entries per eligible weekday;
2. maximum 2 simultaneously open positions;
3. therefore maximum nominal open stop-risk is about USD 40;
4. once realized daily P&L is <= -USD 40, accept no further new entries that day;
5. once realized daily P&L is >= +USD 150, accept no further new entries that day;
6. pre-existing open positions are allowed to finish under their original strategy exits;
7. with at most two open USD 20-risk trades, the loss-stop design allows a rare realized day near -USD 60 if a remaining open position stops after the -USD 40 gate is reached;
8. no martingale, recovery sizing, or size increase after losses.

If two new trades have the same entry timestamp and capacity is constrained, use deterministic priority:

- Engine A first;
- Engine F second.

No performance-based ranking is allowed.

## Metrics

For development and holdout report:

- standalone lead daily-P&L correlation;
- percentage of weekdays with signals/trades from both leads;
- candidate trades by lead;
- portfolio-accepted trades by lead;
- rejections by open-position cap, daily entry cap, loss stop, and profit stop;
- trades/day including zero-signal days;
- zero-trade days;
- mean and median daily P&L;
- losing-day percentage;
- <= USD 50 day percentage;
- >= USD 100 day percentage;
- >= USD 150 day percentage;
- maximum daily loss;
- maximum drawdown;
- maximum consecutive losing days;
- maximum consecutive <= USD 50 days;
- maximum simultaneous notional/equity where calculable;
- contribution by lead.

## Interpretation discipline

Do not call the portfolio successful merely because total P&L is positive.

The main question is whether combining two independently generated positive-expectancy leads materially reduces low-output days without unacceptable drawdown or economic exposure.

No live promotion is possible from EXP-010.

## Next action

Reconstruct and validate the USDJPY Engine A and GBPUSD Engine F streams, then run the frozen portfolio state machine and checkpoint the result.
