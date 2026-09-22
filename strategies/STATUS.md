# Strategy Status

_Last updated: 2026-09-22_

| Strategy | Concept | Current status |
|---|---|---|
| Engine A original / EXP-002 | Liquidity sweep -> internal MSS -> displacement/FVG -> retracement | **ACTIVE LEAD; implementation recovery required** |
| Engine A v0.2-portable | Prospective portable rewrite of Engine A | Separate historical rewrite; not a substitute for EXP-002; not promoted |
| Engine B | Momentum breakout -> retest -> continuation | First formulation rejected |
| Engine C | Trend regime -> pullback -> continuation | First formulation rejected |
| Engine D | Session/opening-range momentum | Current formulations not promoted |
| Engine E | Volatility compression -> expansion | Current formulations not promoted |
| Engine F v0.1 | Statistical extension -> re-entry -> mean reversion | Historical GBPUSD research lead only; not a current execution lead |

## Active strategy priority

### Original Engine A / XAUUSD

**Status: ACTIVE RESEARCH/BUILD LEAD — POSITIVE SIMPLIFIED EXPECTANCY; NEEDS REPRODUCTION, COST VALIDATION, AND FORWARD EVIDENCE.**

EXP-002 recorded:

- ~372 signals overall;
- overall USD 5 target-first ~29.6%;
- holdout USD 5 ~27.3%;
- holdout simplified expectancy ~+USD 0.72 Gold/trade before costs;
- holdout target sensitivity: USD 2 48.7%, USD 3 41.7%, USD 4 31.6%, USD 5 27.3%.

Next action: recover implementation and reproduce those metrics within reasonable tolerance.

## Historical but non-governing leads

### Engine A v0.2 / USDJPY

Earlier normalized-risk testing showed positive mean R in both splits, but later economic reinterpretation made it unsuitable as a primary income stream. Preserve as historical evidence only.

### Engine F v0.1 / GBPUSD

Earlier normalized-risk testing was positive in both splits, but later target/economic reinterpretation showed insufficient dollar movement at the then-assumed fixed size. Preserve as historical evidence only.

## Architecture rule

The target-first ranker should normally receive candidates from validated strategy engines.

Do not let a generic broad-pivot candidate universe silently replace Engine A or other validated engines.

## Next strategy action

1. recover original Engine A;
2. reproduce EXP-002;
3. freeze candidate contract and equivalent sizing;
4. only then resume ranker/multi-engine expansion.
