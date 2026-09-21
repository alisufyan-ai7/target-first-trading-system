# Current Status

**Date:** 2026-09-22  
**Phase:** Strategy research / independent-engine screening

## Source of truth

Only this repository and the originating chat are authorized project context.

## Completed strategy evidence

- **Engine A:** retain USDJPY v0.2 only as a research lead; further expansion paused after EXP-008.
- **Engine B:** first breakout/retest formulation rejected.
- **Engine C:** first trend-pullback formulation rejected.
- **Engine D:** opening-range momentum formulations not promoted.
- **Engine E:** compression/expansion formulations not promoted.
- **Engine F:** statistical mean-reversion portable screen in progress; XAUUSD and USDJPY arms not promoted.

## EXP-006

Multi-asset data/economics checkpoint completed. Public independent 1m samples are usable for provisional screening, but the first volatility-burden sizing translation was economically unsuitable for a ~USD 500 reference account.

## EXP-007 / EXP-008

Engine A v0.2-portable was tested prospectively across XAUUSD, EURUSD, GBPUSD, USDJPY, then XAGUSD.

USDJPY was the only arm positive in both splits (+0.075R development, +0.263R holdout), but 86.4% of holdout days were <= USD 50 and median notional/equity was about 178x. XAGUSD then failed in both splits. Engine A expansion is paused.

## EXP-009 / Engine F

Engine F v0.1 was frozen prospectively before any outcome inspection.

### XAUUSD

- development: 13 trades, -0.192R/trade;
- holdout: 24 trades, +0.021R/trade;
- <= USD 50 days: 100% in both splits;
- holdout median notional/equity: 42.7x.

Status: **not promoted**.

### USDJPY

- development: 31 trades, +0.016R/trade;
- holdout: 18 trades, -0.222R/trade;
- holdout hit rate: 22.22%;
- holdout <= USD 50 days: 98.31%;
- holdout median stop: about 2.50 pips;
- holdout median notional/equity: about 258.3x.

Status: **not promoted**.

### EURUSD

- development: 24 trades, -0.125R/trade;
- holdout: 31 trades, +0.242R/trade;
- holdout hit rate: 35.48%;
- holdout <= USD 50 days: 98.31%;
- holdout median stop: about 2.31 pips;
- holdout median notional/equity: about 203.6x.

Status: **not promoted because development/holdout changed sign**.

## Current conclusion

Engine F has not shown robust evidence in its first three markets. XAUUSD had negative development and marginally positive holdout; USDJPY was nearly flat in development and negative in holdout. Neither materially improves the daily-output objective, and USDJPY is economically impractical under the fixed-risk sizing rule.

The rules remain frozen; no tuning is permitted.

## Next action

1. run Engine F v0.1 unchanged on the final predeclared GBPUSD arm;
2. checkpoint GBPUSD;
3. then decide whether Engine F should be closed or retained;
4. do not combine any Engine F arm with Engine A unless it first demonstrates robust positive evidence;
5. cross-validate only surviving research leads on independent data and realistic costs.

## Key unresolved question

Can multiple independent engines and markets reduce <= USD 50 days toward roughly 20% **without** unacceptable loss frequency, leverage, drawdown, or forced trades?
