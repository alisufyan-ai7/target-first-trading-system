# Current Status

**Date:** 2026-09-22  
**Phase:** Strategy research / objective-feasibility analysis

## Source of truth

Only this repository and the originating chat are authorized project context.

## Retained research leads

### USDJPY / Engine A v0.2

- development mean R: about +0.075R/trade;
- holdout mean R: about +0.263R/trade;
- holdout <= USD 50 days: 86.44%;
- holdout median notional/equity: about 177.8x.

Status: **research lead only; not deployable**.

### GBPUSD / Engine F v0.1

- development mean R: +0.138R/trade;
- holdout mean R: +0.080R/trade;
- holdout <= USD 50 days: 100%;
- holdout median notional/equity: about 180.6x.

Status: **research lead only; not deployable**.

## EXP-010 portfolio result

The two frozen leads were combined under:

- USD 20 risk/trade;
- max 4 entries/day;
- max 2 open positions;
- no new entries after realized daily P&L <= -USD 40;
- no new entries after realized daily P&L >= +USD 150.

### Holdout

- standalone daily P&L correlation: about +0.03;
- both leads traded on 35.6% of weekdays;
- accepted trades: 114;
- trades/day: 1.93;
- zero-trade days: 3.39%;
- mean daily P&L: +USD 10.51;
- median daily P&L: +USD 10;
- losing days: 44.07%;
- <= USD 50 days: 86.44%;
- >= USD 100 days: 6.78%;
- >= USD 150 days: 0%;
- worst day: -USD 40;
- maximum drawdown: about USD 200.53;
- maximum consecutive <= USD 50 days: 14;
- maximum simultaneous notional/equity: about 1,285x.

Conclusion: **independence exists, but the portfolio still fails the daily-distribution and economic-feasibility objectives.**

## Current conclusion

The research problem is no longer simply "find more signals."

Under the present economic framing, qualified opportunities are too sparse and target-first hit rates are too low to make high-output days common. The small account also creates severe notional/margin pressure when structural stops are only a few pips.

No existing engine or portfolio is promoted.

## Next action

Run an objective-feasibility experiment before inventing another strategy family.

Quantify, for 1–4 trades/day with approximately -USD 20 losses and +USD 50 wins:

- the win probability required for P(daily P&L <= USD 50) <= 20%;
- the win probability required for >= USD 100 days near 75–80%;
- how zero-signal / low-trade days worsen those requirements;
- how the USD 40 daily loss stop changes the distribution.

This should establish whether the current distribution objective is statistically compatible with the current payoff/trade-count framework.

Do not change project targets until that feasibility evidence is recorded and explicitly reviewed.

## Key unresolved question

Is the desired <=20% low-output-day profile mathematically plausible with only 3–4 qualified trades/day and a roughly +USD 50 / -USD 20 trade payoff, even before real-world execution costs?
