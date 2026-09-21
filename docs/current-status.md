# Current Status

**Date:** 2026-09-22  
**Phase:** Strategy research / independent-engine screening

## Source of truth

Only this repository and the originating chat are authorized project context.

## Completed

### Badar Tanveer video analysis

Enough direct video evidence was obtained to define an initial mechanical setup family:

liquidity -> sweep -> internal MSS -> displacement -> FVG -> retracement entry -> structural stop -> liquidity/target expansion.

The videos also support:

- XAUUSD focus;
- lower-timeframe execution;
- variable reward/risk rather than universal 1:9;
- partial profit taking;
- session/news awareness.

### Engine A

Badar-inspired liquidity/MSS/FVG setup.

Result:

- simplified expectancy remained positive in the later EXP-002 holdout;
- USD 5 target-first hit rate was only about 27% in holdout;
- typical favorable excursion was closer to USD 3;
- daily USD 0–50 outcomes remained far too frequent.

Cross-market portable testing in EXP-007/008 then showed that only USDJPY was positive in both splits, while XAGUSD failed both splits and the other FX/Gold arms were unstable or negative.

Status: **retain USDJPY / Engine A v0.2 as a research lead only; pause further Engine A expansion.**

### Engine B / C

- Engine B: momentum breakout -> retest -> continuation.
- Engine C: trend regime -> pullback -> continuation.

Status: **first formulations rejected**.

### Engine D

Session/opening-range momentum.

Status: **current formulations not promoted**.

See EXP-004.

### Engine E

Volatility compression -> expansion.

Status: **current formulations not promoted**.

See EXP-005.

### EXP-006

Multi-asset data/economics checkpoint completed. Public independent 1m samples are usable for provisional screening, but the first volatility-burden sizing translation was economically unsuitable for a ~USD 500 reference account.

### EXP-007 / EXP-008

Engine A v0.2-portable was tested prospectively across XAUUSD, EURUSD, GBPUSD, USDJPY, then XAGUSD.

- XAUUSD: negative in both splits under the 2.5R rule.
- EURUSD: negative development, positive holdout.
- GBPUSD: positive development, negative holdout.
- USDJPY: positive in both splits (+0.075R development, +0.263R holdout), but 86.4% of holdout days were <= USD 50 and median notional/equity was about 178x.
- XAGUSD: negative in both splits.

Conclusion: stop further Engine A market expansion/loosening for now.

### EXP-009 / Engine F

A genuinely independent price-only statistical mean-reversion engine was frozen prospectively before outcome inspection.

XAUUSD first checkpoint:

- development: 13 trades, 23.08% 2.5R hit rate, -0.192R/trade;
- holdout: 24 trades, 29.17% hit rate, +0.021R/trade;
- <= USD 50 days: 100% in both splits;
- holdout median notional/equity: about 42.7x.

Status: **XAUUSD Engine F arm not promoted; rules remain frozen.**

## Current conclusion

Neither more XAUUSD signals nor simply adding markets has solved the daily-distribution objective.

The active research question is now whether a genuinely independent engine can produce a robust second stream without post-hoc tuning.

## Next action

1. run the already-frozen Engine F v0.1 unchanged on USDJPY;
2. checkpoint the USDJPY result before touching EURUSD or GBPUSD;
3. do not retune Engine F after the XAUUSD failure;
4. continue to report notional/equity and margin-feasibility diagnostics;
5. combine streams only after positive development/holdout evidence exists;
6. later cross-validate any surviving lead on an independent feed and with execution costs.

## Key unresolved question

Can multiple independent engines and markets reduce <= USD 50 days toward roughly 20% **without** unacceptable loss frequency, leverage, drawdown, or forced trades?
