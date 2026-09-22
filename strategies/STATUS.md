# Strategy Status

_Last updated: 2026-09-23_

| Strategy | Concept | Current status |
|---|---|---|
| Original Engine A / EXP-002 | Liquidity sweep -> internal MSS -> displacement/FVG -> retracement | **Historical exploratory positive result; implementation unrecoverable; not validated for execution** |
| Engine A recovery A6 | Closest causal mechanical reconstruction | Diagnostic only; frequency/risk near benchmark, target-first edge not reproduced; not promoted |
| Engine A recovery A8/A9 | Forensic timing / fill-order diagnostics | Non-deployable forensic tests; not promoted |
| Engine A v0.2-portable | Prospective portable rewrite | Separate historical rewrite; not a substitute for EXP-002; not promoted |
| Engine B | Momentum breakout -> retest -> continuation | First formulation rejected |
| Engine C | Trend regime -> pullback -> continuation | First formulation rejected |
| Engine D | Session/opening-range momentum | Current formulations not promoted |
| Engine E | Volatility compression -> expansion | Current formulations not promoted |
| Engine F v0.1 | Statistical extension -> re-entry -> mean reversion | Historical research evidence only; not a current execution lead |

## Current promotion state

**No strategy engine is currently promoted as a validated execution lead.**

That is an important system state: the architecture, research discipline, candidate contract, and equivalent-sizing method exist, but the production ranker does not yet have a validated reproducible engine stream to score.

## Original EXP-002 preservation

EXP-002 recorded:

- ~372 signals overall;
- overall USD 5 target-first ~29.6%;
- holdout USD 5 ~27.3%;
- holdout simplified expectancy ~+USD 0.72 Gold/trade before costs;
- holdout target sensitivity: USD 2 48.7%, USD 3 41.7%, USD 4 31.6%, USD 5 27.3%.

EXP-014 froze a numerical recovery protocol and tested A1–A9.

The original implementation could not be reproduced honestly and no source implementation survives.

Therefore these EXP-002 metrics remain historical evidence only; they are not current executable-strategy metrics.

## Closest causal recovery: A6

A6 is preserved because it came closest on frequency, split balance, and average risk:

- 333 trades;
- 164 development / 169 holdout;
- average structural risk ~1.053 Gold;
- overall T5 ~15.0%;
- holdout T5 ~13.6%;
- holdout expectancy ~+0.01 Gold/trade.

That is insufficient for promotion and materially below EXP-002 target-first behavior.

Do not tune A6 post hoc to force the old benchmark.

## Architecture rule

The target-first ranker should normally receive candidates from validated strategy engines.

Do not let a generic broad-pivot candidate universe silently replace validated engines.

## Next strategy action

1. define a **new prospective causal engine** rather than continuing EXP-002 recovery;
2. freeze its exact versioned rules and candidate schema before outcome inspection;
3. validate development / validation / holdout behavior and realistic economics;
4. only after at least one reproducible engine passes should EXP-015 be redesigned/resumed.

A future Badar-derived engine may reuse evidence-supported concepts, but it must have a new identity/version and must not be called the recovered original Engine A.
