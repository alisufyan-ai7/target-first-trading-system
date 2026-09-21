# Current Status

**Date:** 2026-09-22  
**Phase:** Strategy research / portfolio lead-combination screening

## Source of truth

Only this repository and the originating chat are authorized project context.

## Strategy state

- **Engine A:** USDJPY v0.2 remains a research lead only; further Engine A expansion is paused.
- **Engine B:** first breakout/retest formulation rejected.
- **Engine C:** first trend-pullback formulation rejected.
- **Engine D:** opening-range momentum formulations not promoted.
- **Engine E:** compression/expansion formulations not promoted.
- **Engine F:** four-market portable screen complete; only GBPUSD v0.1 retained as a research lead.

## Engine A lead — USDJPY

From EXP-007:

- development mean R: +0.075R/trade;
- holdout mean R: +0.263R/trade;
- holdout <= USD 50 days: 86.44%;
- holdout median notional/equity: about 177.8x;
- median holdout stop: about 3.65 pips.

Status: **research lead only; not deployable**.

## Engine F lead — GBPUSD

From EXP-009:

- development: 40 trades, +0.138R/trade;
- holdout: 35 trades, +0.080R/trade;
- holdout target-first hit rate: 28.57%;
- holdout <= USD 50 days: 100%;
- holdout median stop: about 2.98 pips;
- holdout median notional/equity: about 180.6x.

Status: **research lead only; not deployable**.

The other Engine F arms were not promoted:

- XAUUSD: negative development / marginally positive holdout;
- USDJPY: approximately flat development / negative holdout;
- EURUSD: negative development / positive holdout.

## Current conclusion

The project now has two structurally independent leads that were prospectively frozen before their outcome inspection:

1. USDJPY / Engine A v0.2;
2. GBPUSD / Engine F v0.1.

Both are gross-positive in development and holdout, but both have severe small-account economic constraints and neither comes close to the desired daily-output distribution alone.

No further parameter tuning is justified at this point.

## Next action

Prospectively define and run a two-lead portfolio distribution screen using the unchanged Engine A USDJPY and Engine F GBPUSD trade streams.

The portfolio screen should enforce:

- USD 20 risk per accepted trade;
- no more than 4 entries/day;
- no more than 2 simultaneously open trades / about USD 40 open stop-risk;
- stop new entries after realized daily P&L <= -USD 40;
- stop new entries after realized daily P&L >= +USD 150;
- allow pre-existing open risk to create a rare absolute floor near -USD 60;
- count every eligible weekday including zero-signal days;
- report lead correlation/overlap, <= USD 50 days, >= USD 100/150 days, losing days, drawdown, and streaks.

If this two-lead combination still leaves the distribution far from the objective, active research should return to a new independent engine family rather than trying to tune these leads.

## Key unresolved question

Can two independently generated positive-expectancy leads materially improve daily output **without** unacceptable leverage, drawdown, or forced trading?
