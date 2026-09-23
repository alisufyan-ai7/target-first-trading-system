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
| Engine G v0.1 | Contextual liquidity reversal: HTF location -> liquidity sweep -> MSS -> displacement/FVG -> S1 | **Development gate failed: 71 accepted trades (<100 minimum), -$9.27/trade at primary cost, bootstrap CI entirely negative; validation/holdout preserved untouched; not promoted** |
| Engine H v0.1 | Recent range raid into pre-existing external 5m FVG -> 1m MSS/displacement/FVG -> opposite range target | **Development insufficient evidence: only 2 accepted trades vs >=100 minimum; validation/holdout preserved untouched; not promoted** |
| Engine H v0.2 | Same range/FVG raid -> 1m MSS within 20 active bars -> next-active-M1-open entry -> opposite range target | **Development insufficient evidence: 6 accepted trades vs >=100 minimum; +$0.08/trade at primary cost is statistically meaningless; validation/holdout preserved untouched; not promoted** |
| Engine H v0.3 | Same range/FVG raid + MSS/next-open -> post-raid 1m structural stop -> fixed T40 target | **Development failed: 58 trades (<100), -$4.52/trade at primary cost; DEV-A -$7.18 and DEV-B -$1.24; validation/holdout untouched; not promoted** |

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

Engine G v0.1 failed its development gate and is not promoted.

Engine H v0.1 and v0.2 were insufficient-evidence development results.

Engine H v0.3 prospectively replaced the sweep-extreme/opposite-range geometry with a post-raid 1m structural stop and fixed T40 target, and expanded development backward into unused 2023 data rather than lowering the evidence standard. It produced 58 accepted trades, still below the >=100 minimum, with primary-cost expectancy about -USD4.52/trade. Both predeclared development subperiods were negative: DEV-A about -USD7.18/trade and DEV-B about -USD1.24/trade.

Do not retune any frozen H version. Validation and fresh holdout remain untouched.

EXP-015 remains paused until at least one reproducible engine validates.
