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
| Engine I v0.1 | Established 15m direction -> Asian boundary expansion -> controlled 25%-60% pullback -> 1m continuation break -> next-open -> structural pullback stop -> T40 | **Development failed: 197 trades, -$5.15/trade at primary cost, PF 0.631, DEV-A -$6.20, DEV-B -$4.09, MDD $1,060.90; validation/holdout untouched; not promoted** |
| Engine K v0.1 | Multi-market direct target-move probability scanner | **Training/June-calibration gate failed: 7,098 labeled rungs all XAUUSD, 0 executable FX rungs, 0 qualified trades after frozen >=60% calibrated-probability gate; July-August/September untouched; stopped before secondary test** |
| Engine J v0.1 | Same-day 5m baseline -> 30m compression box -> strong 5m breakout -> next-open -> breakout-bar stop -> T40 | **Development failed: 307 trades, -$5.15/trade at primary cost, PF 0.671, DEV-A -$6.95, DEV-B -$3.48, MDD $1,659.93; validation/holdout untouched; not promoted** |

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

## Engine I v0.1 / EXP-020

Engine I v0.1 is stopped before validation.

- 197 accepted development trades;
- T40 hit rate 24.37%;
- gross expectancy about -USD0.15/trade;
- primary-cost expectancy about -USD5.15/trade;
- primary-cost PF 0.631;
- DEV-A about -USD6.20/trade;
- DEV-B about -USD4.09/trade;
- max drawdown about USD1,060.90;
- 95% bootstrap expectancy interval about -USD8.38 to -USD1.94;
- validation and fresh holdout remain untouched.

The sample-size goal was achieved, so this is not an insufficient-frequency result. The economics failed decisively. Do not tune Engine I v0.1 post hoc.

**Current next step:** prospectively freeze the next genuinely different engine family. EXP-015 remains paused.


## Engine J v0.1 / EXP-021

Engine J v0.1 is stopped before validation.

- 307 accepted development trades;
- T40 hit rate 27.04%;
- gross expectancy about -USD0.15/trade;
- primary-cost expectancy about -USD5.15/trade;
- primary-cost PF 0.671;
- DEV-A about -USD6.95/trade;
- DEV-B about -USD3.48/trade;
- max drawdown about USD1,659.93;
- 95% bootstrap expectancy interval about -USD7.93 to -USD2.27;
- validation and fresh holdout remain untouched.

The sample-size goal was exceeded. The economics failed decisively. Do not tune Engine J v0.1 post hoc.

**Current next step:** prospectively freeze the next genuinely different engine family. EXP-015 remains paused.


## Engine K v0.1 — current primary discovery engine

Engine K changes the project from sequential XAU-only motif testing to direct multi-market target forecasting.

It scans Wave-1 markets every five minutes, creates causal long/short states, estimates target-first probability, applies equivalent sizing and risk gates, and ranks the best qualified opportunity.

Wave-1:

- XAUUSD;
- EURUSD;
- GBPUSD;
- USDJPY;
- EURJPY;
- AUDUSD;
- USDCAD;
- USDCHF.

Forecast-only:

- XAGUSD;
- NAS100;
- US30;
- SPX500.

Status:

- specification frozen prospectively and amended before outcomes;
- EXP-022 opened and split reconciled;
- exact data provenance frozen;
- 29-feature causal contract frozen;
- cost/notional/margin/probability gates frozen;
- forecast-only markets isolated from executable model fitting/ranking;
- zero Engine-K target outcomes calculated;
- zero Engine-K model outcomes calculated;
- final zero-outcome cleanup preflight PASSED at result commit `48aa0af80b7fc2fff1dab56d3fb617b1c2140f3f`;
- training + June calibration completed and FAILED the frozen pre-secondary gate; July-August and September remain sealed.

Do not retune G/H/I/J while Engine K is being evaluated.


## Engine K v0.2 / EXP-023 — current primary path

v0.1 is closed before secondary testing.

v0.2 is prospectively frozen with zero outcomes:

- same 8 execution markets / 4 forecast-only markets;
- same dense 5m long/short scanner;
- same structural stop and 29 causal features;
- Gold remains +3/+4/+5 at 0.10 lot;
- non-Gold target-first ladder = 1.5R / 2.0R / 2.5R, target defined before size;
- downward P&L-equivalent sizing to USD30/40/50;
- unchanged USD20 risk, USD50k notional, USD100 research-margin gates;
- p_required = max(0.50, break-even +0.10);
- July-August and September remain sealed.

**Preflight:** PASSED at result commit `02a2ab0b1ea7f21092b06165a0ca8f0638d4c41b`.

**Training/June result:** FAILED at result/model commit `763aefadbe56ee7012b475dcb677f6f78d8036ec`. 281,955 labeled rungs, but only 2 combined qualified trades and 0 June trades. T30/T40/T50 June AUC about 0.674/0.710/0.743. July-August and September remain sealed.

**Status:** v0.2 closed before secondary testing.


## Engine K v0.3 / EXP-024 — current primary path

v0.2 is closed before secondary testing.

v0.3 is frozen prospectively:

- same 8 execution markets;
- same v0.2 target/economic construction;
- Mar-Apr model fit;
- May market-direction-aware calibration;
- June true development gate;
- qualification requires both positive primary EV and positive stress EV;
- no fixed probability floor;
- July-Aug and September sealed.

**June result:** FAILED at commit `db53f3a96fbbb6ed7b1b01f25e931e4140bec215`.

- 39 trades / 19 weekdays;
- primary expectancy -USD0.22/trade;
- stress expectancy -USD3.89/trade;
- primary PF 0.983;
- stress PF 0.742;
- max DD USD212.34;
- calibrated June AUC 0.672/0.708/0.740.

v0.3 is closed before secondary testing. July-Aug and September remain sealed.


## Engine K v0.4 / EXP-025 — current primary path

v0.3 is closed before secondary testing.

v0.4 prospectively freezes a bounded walk-forward development selection:

- 12 configurations only;
- 6 chronological folds;
- unchanged scanner/economics/risk architecture;
- July-Aug and September sealed;
- stability-first frozen winner rule;
- hard stop before secondary if no configuration passes.

**Next:** run EXP-025 development-only walk-forward selection.


## Engine K v0.4 / EXP-025 — closed

Walk-forward result commit:

`24ce35448cb93158aadeb843dce928199c0c5385`

- 12 frozen configs;
- 6 chronological folds;
- 0 passing configs;
- no selected winner;
- Jul-Aug unopened;
- Sep unopened.

Engine K tuning on the current Mar-Jun development pool is stopped by the frozen anti-mining rule.

Do not create v0.5 as another threshold/configuration extension of this search. Future work must broaden evidence or materially change the prediction design.
