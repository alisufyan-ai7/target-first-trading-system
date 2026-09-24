# Decision Log

## 2026-09-22 — Context isolation

**Decision:** Only the originating chat and `alisufyan-ai7/target-first-trading-system` may be used as durable project context.

**Reason:** Other GitHub repositories and other chats belong to separate projects and must not contaminate this research.

## 2026-09-22 — GitHub as durable checkpoint

**Decision:** Material experiment conclusions must be written to GitHub before beginning another long-running computation.

**Reason:** Several long ChatGPT streaming runs timed out, making response recovery unreliable.

## 2026-09-22 — Do not force daily trade count

**Decision:** Treat 3–4 trades/day as an upper/typical opportunity objective, not a mandatory quota.

**Reason:** Lowering signal quality to meet a daily count would undermine expectancy and increase drawdown.

## 2026-09-22 — Target-first evaluation

**Decision:** Evaluate setups by whether the desired favorable move occurs before structural invalidation, not simply by directional correctness.

## 2026-09-22 — Engine A retained but not sufficient

**Decision:** Keep the Badar-inspired liquidity/MSS/FVG strategy as one candidate generator.

**Reason:** The first screen showed simplified positive expectancy but far too many low-output days.

## 2026-09-22 — Reject first Engine B/C formulations

**Decision:** Do not continue hand-tuning the initial breakout/retest and trend-pullback formulations merely to make them fit historical data.

**Next:** Test structurally different strategy families.

## 2026-09-22 — Reject volatility-burden sizing as portfolio rule

**Decision:** Do not use the EXP-006 rule that maps Gold's USD 5 target to the same fraction of median hourly volatility and then sizes each FX market to make that move worth USD 50.

**Reason:** On the development-only calibration sample it produced roughly 3–4 pip FX targets but required about 1.2–2.1 standard lots, creating excessive notional/margin demands for the reference USD 500 account.

**Next:** Freeze a structural-stop / fixed-risk normalization before cross-market Engine A performance testing. Keep the EXP-006 mapping only as a diagnostic record.

## 2026-09-22 — Provisional independent feed for multi-asset screening

**Decision:** Public GetData 1m samples may be used as an external research feed for the first cross-market screen over the common 2026-03-12 to 2026-08-20 window.

**Constraint:** This does not replace Dukascopy/broker validation. Any finalist must be cross-validated on another independent feed and with broker-specific execution economics.

## 2026-09-22 — EXP-007 portable Engine A cross-market result

**Decision:** Do not combine or promote the EXP-007 XAUUSD, EURUSD, GBPUSD, and USDJPY arms as a portfolio.

**Evidence:** XAUUSD was negative in both splits; EURUSD and GBPUSD changed sign across development/holdout; USDJPY was positive in both splits but still produced 86.4% <= USD 50 holdout days and required median notional exposure around 178x reference equity under the USD 20 risk / USD 50 target rule.

**Next:** Preserve USDJPY as a research lead without post-hoc tuning. Expand Engine A to a small second wave of markets under the already frozen rules; if that does not add robust positive streams, move to a genuinely independent strategy family.

## 2026-09-22 — Pause Engine A expansion after EXP-008

**Decision:** Stop adding markets or loosening Engine A v0.2 for now.

**Evidence:** XAGUSD, the second-wave unchanged transfer test, was negative in both development (-0.179R/trade) and holdout (-0.161R/trade), with 93.2% <= USD 50 holdout days. Across EXP-007/008, USDJPY was the only market positive in both splits, and it still failed the project's daily-distribution and economic-feasibility objectives.

**Next:** Preserve USDJPY as a research lead for later independent validation and move active strategy research to a genuinely independent setup family.

## 2026-09-22 — Freeze Engine F before outcome inspection

**Decision:** Freeze Engine F v0.1 as a price-only statistical extension -> re-entry -> mean-reversion family before testing any market outcome.

**Reason:** The project needs a genuinely independent stream rather than further Engine A variants or post-hoc filters.

## 2026-09-22 — EXP-009 XAUUSD checkpoint not promoted

**Decision:** Do not promote or retune the XAUUSD Engine F v0.1 arm.

**Evidence:** Development produced 13 trades at -0.192R/trade; holdout produced 24 trades at only +0.021R/trade; every eligible day in both splits remained <= USD 50.

**Next:** Continue unchanged to the predeclared USDJPY checkpoint before judging the portable Engine F family more broadly.

## 2026-09-22 — EXP-009 USDJPY checkpoint not promoted

**Decision:** Do not promote or retune the USDJPY Engine F v0.1 arm.

**Evidence:** Development was approximately flat at +0.016R/trade on 31 trades, while holdout fell to -0.222R/trade on 18 trades. Holdout <= USD 50 days were 98.31%, and the median 2.50-pip stop implied about 258x notional/equity under the USD 20 risk rule.

**Next:** Continue unchanged to the predeclared EURUSD checkpoint before testing GBPUSD.

## 2026-09-22 — EXP-009 EURUSD checkpoint not promoted

**Decision:** Do not promote or retune the EURUSD Engine F v0.1 arm.

**Evidence:** Development was negative at -0.125R/trade on 24 trades while holdout flipped to +0.242R/trade on 31 trades. Holdout <= USD 50 days were 98.31%, and median notional/equity was about 204x.

**Next:** Run the final predeclared GBPUSD arm unchanged, then judge Engine F on the complete four-market screen.

## 2026-09-22 — Complete EXP-009; retain only GBPUSD Engine F as a lead

**Decision:** Close Engine F v0.1 cross-market screening without retuning. Preserve GBPUSD as a statistical research lead only; do not promote any Engine F arm to execution.

**Evidence:** GBPUSD was the only Engine F arm positive in both splits (+0.138R development, +0.080R holdout), but holdout target-first hit rate was only 28.57%, every holdout day remained <= USD 50, median stop was about 2.98 pips, and median notional/equity was about 181x. The other three markets showed sign instability or negative holdout.

**Next:** Test the frozen GBPUSD Engine F lead together with the frozen USDJPY Engine A lead under the project daily risk state machine before inventing or tuning more strategies.

## 2026-09-22 — EXP-010 two-lead portfolio fails the distribution objective

**Decision:** Do not promote or tune the combined USDJPY Engine A / GBPUSD Engine F portfolio.

**Evidence:** Holdout daily P&L correlation between the leads was only about +0.03, confirming useful independence, but 86.44% of holdout days still finished <= USD 50, no holdout day reached USD 150, losing days were 44.07%, and maximum drawdown was about USD 200.53. Maximum simultaneous notional/equity exceeded 1,200x under fixed USD 20 structural risk.

**Next:** Quantify the mathematical feasibility frontier of the user's daily-distribution objective under the current +USD 50 / -USD 20 payoff and 1–4 trade/day constraints before searching for another engine or changing any objective.

## 2026-09-22 — Revise operating objective to fixed-size target-ladder scanner

**Decision:** The project end objective is explicitly system construction, not research as an end in itself. Research remains the evidence/validation layer.

**Execution anchor:**

- XAUUSD reference size = 0.10 lot;
- major FX initial research anchor = 0.10 standard lot, pending broker-specific verification;
- do not dynamically enlarge size merely to force every winning trade to equal USD 50.

**Profit objective:**

- ordinary successful trades may capture approximately USD 30–50;
- stronger validated moves may be held toward USD 70–100+;
- the scanner should estimate and rank multiple target rungs rather than one universal +2.5R target.

**Trade count:** No hard 3–4 trades/day assumption. Trade count is opportunity-driven and may be higher when several independent qualified smaller-target opportunities exist. There is still no forced minimum trade count.

**Daily objective:** Work toward approximately USD 150–200 net on days with sufficient opportunity while preserving the approximately -USD 40 normal / -USD 60 hard daily-loss framework.

**Reason:** Prior fixed-risk tests distorted cross-market economics by using very large notional exposure to manufacture USD 50 targets from narrow structural stops. The user's intended system is fixed-size and should seek the best attainable dollar move across markets.

## 2026-09-22 — Supersede EXP-011 before results

**Decision:** Do not calculate EXP-011 under its old fixed +USD 50 / -USD 20 / maximum-4-trades model.

**Reason:** The user revised the economic and trade-count assumptions before EXP-011 results were produced.

**Next:** EXP-012 will evaluate fixed-size target ladders and rebuild the opportunity-ranking framework around T30/T40/T50/T70/T100 before structural invalidation.

## 2026-09-22 — Re-evaluate retained leads before inventing another engine

**Decision:** Before adding Engine G or further market-specific strategy variants, reconstruct:

1. USDJPY / Engine A v0.2 at fixed 0.10 standard lot;
2. GBPUSD / Engine F v0.1 at fixed 0.10 standard lot.

Measure actual fixed-size stop risk plus T30/T40/T50/T70/T100 hit rates.

**Reason:** A lead that looked impractical under dynamic USD 20 risk sizing may have different economics under the user's intended fixed-size execution model, and that should be tested before discarding it.

## 2026-09-22 — EXP-012 fixed-size reinterpretation of prior leads

**Decision:** The prior USDJPY / Engine A and GBPUSD / Engine F leads are not priority execution candidates under the user's fixed-size objective.

**Evidence:**

- USDJPY at 0.10 standard lot produced only about 7.14% T30 and 4.08% T50 holdout hits from the reconstructed Engine A stream; median favorable excursion was only about USD 2.94.
- GBPUSD at 0.10 standard lot produced about 11.11% T30, 2.78% T40, and 0% T50+ holdout hits from Engine F; median favorable excursion was about USD 3.70.

**Reason:** Their prior apparent USD 50 feasibility depended on dynamic risk sizing that created excessive notional exposure. Fixed 0.10-lot economics reveal that the same entries usually move only a few dollars.

## 2026-09-22 — Gold remains the primary economic anchor

**Decision:** Continue system-building around XAUUSD as a core market because 0.10-lot Gold naturally maps a USD 3–10 price move to approximately USD 30–100 gross P&L.

**Evidence:** XAUUSD / Engine A v0.2 holdout reconstruction at fixed 0.10 lot produced approximate target-first hit rates of 57.14% (T30), 41.35% (T40), 36.84% (T50), 29.32% (T70), and 22.56% (T100).

**Constraint:** Raw structural stops were too wide: median holdout stop risk was about USD 51.90 and the 90th percentile about USD 114.70.

## 2026-09-22 — Apply fixed-size Gold structural-risk gate

**Decision:** For the fixed-size Gold diagnostic, reject any setup whose unchanged structural stop would lose more than USD 40 at 0.10 lot. Do not compress the stop and do not reduce the lot for this diagnostic.

**Evidence:** The gate preserved 50 holdout trades. Target-first hit rates remained meaningful, but fixed-target expectancy showed only T30 near break-even.

## 2026-09-22 — Do not adopt T30 from Engine A

**Decision:** Do not promote a universal USD 30 Gold take-profit from the current Engine A subset.

**Evidence:** Development T30 expectancy was about +USD 7.13/trade, but holdout fell to approximately +USD 0.02/trade before costs. Higher target rungs were negative in holdout.

**Next:** Separate market-economic feasibility from entry-quality prediction. First map which markets naturally support USD 30–100 fixed-size moves; then build a prospectively frozen target-first opportunity-ranking layer across that economically suitable universe.

## 2026-09-22 — Freeze first scanner universe from EXP-013

**Decision:** Use the following first-wave market universe for the target-first opportunity ranker:

1. XAUUSD;
2. GBPUSD;
3. USDCHF;
4. EURUSD;
5. AUDUSD.

**Basis:** development-only fixed-size movement economics, not holdout strategy outcomes.

**Deferred/lower priority:** EURJPY, USDJPY, USDCAD; GBPJPY unavailable on the matching sample source; XAGUSD unranked pending fixed contract/quantity convention.

**Next:** Build a prospectively frozen target-first ranking layer across the five markets rather than selecting a universal take-profit or hand-tuning Engine A filters.

## 2026-09-22 — Correct cross-market lot-size interpretation

**Decision:** XAUUSD uses 0.10 lot as the anchor, but other markets do not automatically use 0.10 lot.

For a frozen native target distance, calculate the lot size that makes the normal successful target approximately USD 50, then apply structural-stop risk, margin, leverage/notional, and daily-risk gates.

USD 30–40 is an acceptable fallback when the full USD-50-equivalent size/target is not safely feasible. USD 70–100+ is allowed under validated continuation logic.

**Reason:** The user clarified that "equivalent to 0.10 Gold" means equivalent earning economics, not identical lot number.

## 2026-09-22 — Restore original EXP-002 Gold Engine A as an active lead

**Decision:** Do not treat later Engine A v0.2-portable results as invalidating the original Badar-inspired Gold screen.

**Evidence:** EXP-002 recorded positive simplified expectancy in both development (~+0.85 Gold/trade) and holdout (~+0.72 Gold/trade), with holdout target-first rates of 41.7% at USD 3, 31.6% at USD 4, and 27.3% at USD 5.

**Reason:** SPEC-v0.2-portable explicitly states that v0.2 was a prospective reconstruction and was not claimed to reproduce the exact EXP-002 implementation.

**Next:** Recover/reconstruct the original Engine A mechanics and require reproduction of the EXP-002 Gold behavior before cross-market transfer.

## 2026-09-22 — Reclassify same-0.10-lot FX work as diagnostic only

**Decision:** Preserve EXP-012/013 calculations but do not use their fixed-0.10-lot FX ranking as the forward sizing rule.

**Reason:** Those calculations were produced under a misunderstanding of the user's intended equivalent-lot concept.

**Next:** Revisit EXP-006-style P&L-equivalent sizing with explicit feasibility gates.


## 2026-09-22 — Reassert system-first identity

**Decision:** This repository represents a trading-system build. Research/backtesting is the validation layer, not the end product.

**Reason:** The original conversation defined an operating multi-market scanner/execution system, and later repository work had become too research-centric.

## 2026-09-22 — Preserve full original conversation architecture

**Decision:** Add authoritative system/context documents covering the full system blueprint, original economic objective, Badar video evidence, timeframe/context model, superseded assumptions, strategy-engine candidate contract, and staged deployment roadmap.

**Reason:** Quantitative experiment files alone did not preserve enough of the original design reasoning for reliable context recovery.

## 2026-09-22 — Restore engine-first ranker architecture

**Decision:** The target-first probability/ranking layer should normally score candidates emitted by validated/versioned strategy engines.

A broad generic pivot/statistical candidate generator may be researched, but it must itself be explicitly defined and validated as an engine before bypassing this contract.

**Reason:** The earlier broad-pivot ranker draft represented architecture drift from the system originally agreed in the chat.

## 2026-09-22 — Resolve duplicate EXP-014 IDs

**Decision:** Keep EXP-014 as Original Engine A Recovery + P&L-Equivalent Sizing. Renumber the previous broad target-first ranker to EXP-015.

**Status:** EXP-015 is PAUSED until EXP-014 passes.

## 2026-09-22 — Original Engine A recovery is the immediate technical gate

**Decision:** Do not resume broad ranker optimization or new scanner-universe outcome testing until the original EXP-002 Gold Engine A is recovered/reproduced within reasonable tolerance or honestly declared unrecoverable.

**Reason:** Later Engine A v0.2 was a different prospective rewrite and cannot substitute for the original positive EXP-002 lead.

## 2026-09-22 — Historical same-lot FX work is diagnostic only

**Decision:** Reclassify EXP-013's same-0.10-lot FX universe ranking as a historical diagnostic, not a current scanner-selection rule.

**Reason:** The user's intended cross-market economics require P&L-equivalent lot sizing, not identical lot numbers.

## 2026-09-23 — Freeze EXP-014 reproduction acceptance before recovery outcomes

**Decision:** Judge original EXP-002 recovery against a multi-dimensional frozen protocol rather than tuning to one headline metric.

**Frozen dimensions:** trade count and split balance, T2/T3/T4/T5 target-first rates, average structural risk, median MFE, and simplified expectancy in development and holdout.

**Reason:** A recovered strategy must resemble the recorded EXP-002 behavior as a whole. One matching hit rate cannot compensate for materially wrong frequency, risk, excursion, or expectancy.

## 2026-09-23 — Close EXP-014 Part A as unrecoverable

**Decision:** The original EXP-002 Engine A implementation is **not honestly recoverable from the surviving evidence**.

**Evidence:**

- the audited March 1–August 20, 2026 XAUUSD one-minute research series contained 230,813 rows, exactly matching the recorded EXP-002 row count;
- no original EXP-002 detector/backtest code survives in repository history;
- recovery variants A1–A9 were frozen/checkpointed one ambiguity at a time;
- A6 came closest to the original frequency/split balance and average-risk dimensions but produced only about 15.0% overall T5, about 13.6% holdout T5, and about +0.01 Gold/trade holdout expectancy;
- A8 forensic intrabar-sweep timing did not recover the edge;
- A9 optimistic fill-bar handling improved holdout T5 to about 17.9% and expectancy to about +0.25 Gold/trade but still materially missed EXP-002.

**Treatment:** Preserve EXP-002 as a historical exploratory positive result. Do not treat it, A6, v0.2-portable, A8, or A9 as a validated reproduction.

**Reason:** Continuing to vary mechanics solely until the old summary fits would become post-hoc overfitting rather than honest recovery.

## 2026-09-23 — Freeze engine-conditioned P&L-equivalent sizing

**Decision:** Use **engine-conditioned native target logic / engine-conditioned favorable-excursion calibration** as the forward non-Gold target-distance method.

**Rejected as governing method:** generic volatility-burden equivalence from EXP-006. Retain it only as a diagnostic.

**Forward order:**

1. freeze/use the validated engine/market native target or target function;
2. calculate the lot that makes that normal target approximately USD 50 gross;
3. round to legal broker size without increasing risk;
4. apply structural-stop risk, margin, notional/leverage, remaining daily budget, aggregate open-stop risk, and correlation gates;
5. if unsafe, use only a separately validated USD 40/30 fallback or reject.

**Constraint:** the approximately USD 60 emergency hard ceiling is not a normal per-trade sizing allowance.

**Specification:** `docs/PNL-EQUIVALENT-SIZING.md`.

## 2026-09-23 — EXP-015 remains paused after EXP-014

**Decision:** Completing EXP-014 does not automatically resume the target-first ranker.

**Reason:** The system currently has no strategy engine promoted as a reproducible validated candidate source. The ranker is a selector after validated engines, not a substitute for them.

**Next:** prospectively define and validate a new causal strategy engine, map its output to the common candidate contract, and only then redesign/resume EXP-015.

A future Badar-derived engine may use evidence-supported concepts, but it must be a new version/identity rather than a claim to have recovered EXP-002.

## 2026-09-23 — Freeze Engine G v0.1 and EXP-016 before outcomes

**Decision:** Freeze Engine G — Contextual Liquidity Reversal v0.1 as a new prospective causal engine and open EXP-016 before calculating any Engine G development, validation, or holdout outcome.

**Frozen mechanics include:** integer 0.001-XAU tick price logic; dynamic side-aware liquidity clusters over individual PDH/PDL, Asian, 15m-swing and prominent-5m-swing instances; 24-hour market-active 5m liquidity consumption; 06:00–18:00 UTC setup generation; 48-active-15m context; causal 1m MSS; 1.60x displacement; explicit FVG rules; midpoint entry; sweep-extreme structural stop; gross <=USD 40 structural-risk admission; nearest opposing-liquidity S1; independent counterfactual T30/T40/T50/T70/T100 labels; conservative same-bar handling; and delayed sensitivity diagnostics.

**Frozen primary split:** development 2024-01-01–2025-02-28; validation 2025-03-01–2025-08-31; fresh holdout 2025-09-01–2026-02-28. March 1–August 20, 2026 is quarantined from the primary decision because it was heavily inspected by earlier project research.

**Frozen source snapshot:** public Dukascopy-derived XAUUSD M1 transport `kevingtlin/Market-Data-Lab` at commit `922f83a60cc574e7395fb27397077288055a1ef6`, with the monthly BID blob manifest recorded in the strategy spec.

**Reason:** The project needs a genuinely reproducible strategy-engine candidate before EXP-015 can resume. Freezing the complete mechanics, provenance, split, uncertainty rules, and promotion criteria before outcomes prevents outcome-driven reconstruction or parameter selection.

**Next:** verify implementation/data integrity, then run development only and checkpoint it before inspecting validation.

## 2026-09-23 — Stop Engine G v0.1 before validation

**Decision:** Do not run Engine G v0.1 on its frozen validation or fresh-holdout periods.

**Development evidence:** 71 accepted trades versus the frozen >=100 minimum; S1 hit rate about 16.9%; primary 0.50-XAU-cost expectancy about -USD 9.27/trade; profit factor about 0.496; 95% moving-block-bootstrap expectancy interval about -USD 15.14 to -USD 2.52; maximum drawdown about USD 826.29 on the USD 500 reference-equity curve.

**Reason:** The frozen promotion protocol requires positive development expectancy and the frozen evidence protocol requires at least 100 accepted development trades. v0.1 satisfies neither. Later validation/holdout performance therefore cannot make v0.1 eligible for promotion. Preserving those periods untouched provides more value than contaminating them with a version that has already failed its development gate.

**Treatment:** Engine G v0.1 is not promoted. Do not retune it and do not run its delayed sensitivity variants. Any revised contextual-liquidity hypothesis must be a prospectively frozen Engine G v0.2 or a new engine.

## 2026-09-23 — Freeze and stop Engine H v0.1 at development

**Decision:** Freeze Engine H v0.1 prospectively from the two uploaded video motifs, run development only, then stop before validation because the frozen minimum evidence gate was not met.

**Development funnel:** 341 qualifying range/FVG raids, 180 inside the setup window, but only 2 accepted filled trades after causal MSS, displacement-created entry FVG and economic gates.

**Evidence:** 2 accepted trades versus >=100 required. Primary-cost point expectancy was +USD 9.35/trade, but the 95% moving-block-bootstrap expectancy interval was approximately -USD 34.66 to +USD 53.36 with 1,264 zero-trade resamples.

**Interpretation:** Do not interpret two positive/ mixed trades as edge. H v0.1 is insufficient evidence, not validated.

**Next:** preserve validation/holdout untouched. Any simplified confirmation architecture must be a prospectively frozen H v0.2/new experiment rather than a post-hoc rewrite of v0.1.

## 2026-09-23 — Stop Engine H v0.2 before validation

**Decision:** Engine H v0.2 is not promoted and will not inspect validation or holdout.

**Development evidence:** 180 in-window qualifying raids; 69 reached an MSS/next-open economic-admission decision; only 6 passed all frozen geometry/risk gates versus >=100 required. Primary-cost expectancy was approximately +USD0.08/trade, profit factor approximately 1.004, total net approximately +USD0.49, and the 95% block-bootstrap expectancy interval approximately -USD32.65 to +USD40.00.

**Interpretation:** Simplifying confirmation from H v0.1 increased accepted trades from 2 to 6 but did not solve evidence scarcity. The dominant bottleneck moved to the target/stop/economic geometry: 24 candidates failed 3-XAU target room, 21 exceeded USD40 gross structural risk, 15 failed 2R, and 3 failed next-open geometry.

**Next:** preserve validation/holdout untouched. Any revised target/stop architecture must be a new prospectively frozen H v0.3 or different engine; do not reinterpret the six-trade positive point estimate as edge.

## 2026-09-23 — Stop Engine H v0.3 and pause the H thesis family

**Decision:** Stop Engine H v0.3 before validation and do not continue immediate post-hoc revisions of the same range-raid/pre-existing-FVG reversal thesis.

**Development design:** expanded prospectively to Jan-2023 through Feb-2025 rather than lowering the >=100 evidence standard; DEV-A=2023 and DEV-B=Jan-2024 through Feb-2025 were frozen as separate stability checks.

**Evidence:** 58 accepted trades; primary-cost expectancy about -USD4.52/trade; PF about 0.703; T40 hit rate about 29.31%; DEV-A expectancy about -USD7.18/trade; DEV-B expectancy about -USD1.24/trade; 95% block-bootstrap expectancy interval about -USD11.60 to +USD2.69.

**Interpretation:** The post-raid structural stop solved much of the previous economic-admission scarcity, but the fixed T40 execution still failed cost-adjusted development expectancy in both subperiods. Together with H v0.1 and v0.2, this is enough evidence to pause this location thesis rather than keep redesigning exits on the same development data.

**Next:** preserve validation/holdout untouched and move to a genuinely different prospectively specified strategy-engine family. EXP-015 remains paused.

## 2026-09-23 — Freeze Engine I v0.1 / EXP-020 before outcomes

**Decision:** Freeze Engine I — Session Expansion / Continuation v0.1 and EXP-020 before calculating any Engine-I outcome.

**Causal family:** established 15m direction -> Asian-session boundary breakout/acceptance -> strong 5m expansion -> controlled 25%-60% pullback -> 1m continuation break -> next-active-M1-open -> structural pullback stop -> fixed T40 actual target.

**Why materially different from G/H:** Engine I is a continuation engine. It removes reversal raid/rejection logic, pre-existing-FVG location, reversal MSS, displacement-created entry FVG, opposing-range target geometry, and the separate 2R admission gate.

**Frozen split:** warm-up Dec-2022; development Jan-2023 through Feb-2025; DEV-A calendar 2023; DEV-B Jan-2024 through Feb-2025; validation Mar-Aug 2025; fresh holdout Sep-2025 through Feb-2026; Mar-Aug 20 2026 quarantined.

**Contamination treatment:** 2023-Feb-2025 is reusable development data but is not pristine at the project level because G/H development results were inspected there. No Engine-I outcomes exist. Validation and fresh holdout remain uninspected by G/H outcomes and stay closed until prospective gates permit them.

**Primary cost:** 0.50 XAU / USD5 round trip from the first development run.

**Frozen development gate:** >=100 accepted trades; positive primary-cost expectancy overall, DEV-A and DEV-B; PF >=1.10; max drawdown <=USD200; net-profit/max-drawdown recovery factor >=1.0; no causal, same-bar or provenance defect.

**Promotion sequence:** validation and holdout remain unopened unless each preceding split passes its frozen gate. No v0.1 parameter grid is authorized.

**Next:** user review/approval, then implementation/provenance verification with zero outcomes; only afterward may development run.


## 2026-09-23 — Engine I preflight passed; authorize development-only next

**Decision:** Accept the Engine-I v0.1 implementation/provenance checkpoint with zero Engine-I outcomes calculated.

**Implementation:** `research/code/engine-i-v0.1.js`; final pre-outcome amendment commit `060ee9848575516ae06e16c1b17b921b525942f8`.

**Verification:** final preflight GitHub Actions run `35842855789`, result commit `61e2e81e95bb01b2ae891b3cb7814cb03efdea60`.

**Evidence:** 27 frozen Dec-2022 through Feb-2025 files matched blob SHA, byte size, row count, exact month boundaries, minute chronology and exact-grid/OHLC checks; 11 exact-arithmetic/causality tests passed. Validation and holdout files were absent and not loaded.

**Clarification before outcomes:** reporting counters were completed for valid Asian weekdays and aligned long/short context events, and the 20-bar unarmed timeout uses `pullback_timeout_20`. No frozen threshold or causal rule changed.

**Next:** the only permitted outcome run is combined development Jan-2023 through Feb-2025. Validation/holdout remain sealed. The development workflow is implemented but untriggered at this checkpoint.


## 2026-09-23 — Stop Engine I v0.1 after decisive development failure

**Decision:** Stop Engine I v0.1 before validation. Do not tune the same session-expansion/controlled-pullback continuation center rule on the inspected development pool.

**Evidence:** 197 accepted trades; T40 hit rate 24.37%; gross expectancy about -USD0.15/trade; primary-cost expectancy about -USD5.15/trade; PF 0.631; total net -USD1,015.49; max drawdown USD1,060.90. DEV-A expectancy about -USD6.20/trade and DEV-B about -USD4.09/trade. The 95% moving-block bootstrap expectancy interval was approximately -USD8.38 to -USD1.94.

**Gate:** only the >=100 trade-count requirement passed. Combined expectancy, both subperiod expectancy tests, PF, drawdown and recovery factor all failed.

**Interpretation:** Engine I fixed the prior H-family sparsity problem but did not establish a cost-adjusted continuation edge. Because gross expectancy itself was approximately flat-to-negative and the primary-cost bootstrap interval was entirely negative, the failure is decisive rather than a case for threshold tuning.

**Protection:** Mar-Aug 2025 validation and Sep-2025 through Feb-2026 fresh holdout were not loaded or inspected.

**Next:** move to a genuinely different prospectively specified engine family. Do not create a rescue parameter grid, switch the actual target after seeing diagnostics, or reopen G/H tuning. EXP-015 remains paused.


## 2026-09-23 — Freeze Engine J v0.1 / EXP-021 before outcomes

**Decision:** After Engine I's decisive development failure, move immediately to a different causal family and freeze Engine J — Volatility Compression Breakout v0.1 before outcomes.

**Causal family:** same-day 5m volatility baseline -> 30m realized-range compression / compact box -> strong 5m breakout expansion -> next-active-M1-open -> breakout-bar structural stop -> fixed T40.

**Why different:** Engine J has no Asian/session boundary, established-direction filter, sweep/rejection, MSS/FVG, pullback, retest, or continuation confirmation. It tests direct expansion out of a low-volatility regime.

**Frozen compression rule:** older 24 same-day active 5m bars define exact median range; latest six active 5m bars must average <=80% of that median and occupy a box <=3x the median range.

**Frozen breakout rule:** candidate 5m bar opens from inside the relevant box boundary, closes outside it, has range >=1.25x baseline median, body >=60%, and closes in its directional outer 25%.

**Entry/stop/target:** next-active-M1-open before 18:00 UTC; one tick beyond breakout-bar opposite extreme; <=4000-tick structural risk; T40 actual target; conservative stop-first same-bar handling.

**Evidence design:** same reusable Jan-2023–Feb-2025 development pool with DEV-A/DEV-B; validation Mar-Aug 2025 and fresh holdout Sep-2025–Feb-2026 remain sealed; USD5 primary cost from run one; same >=100/expectancy/PF/drawdown/recovery gates.

**Anti-mining:** one center configuration, no parameter grid. Zero Engine-J outcomes exist at freeze.

**Next:** user review, implementation/preflight, then development only.


## 2026-09-23 — Engine J preflight passed; authorize development-only next

**Decision:** Accept the Engine-J v0.1 implementation/provenance checkpoint with zero Engine-J outcomes calculated.

**Implementation:** `research/code/engine-j-v0.1.js`; final preflight-ready implementation commit `a59cc2cf1a48b49c6e76a7da99aa7ed51dd56064`.

**Verification:** GitHub Actions run `35869719236`, result commit `1473aa343c7d0ea746c4ff643571fb729329f687`.

**Evidence:** 27 frozen Dec-2022 through Feb-2025 files matched blob SHA, byte size, row count, exact month boundaries, minute chronology and exact-grid/OHLC checks. All 16 Engine-J exact-arithmetic/causality tests passed. Validation and holdout files were absent and not loaded.

**Mechanical clarification before outcomes:** the 20:00 UTC horizon closes on the final chronological M1 close even when that minute is carry-forward. This is an implementation of the already-frozen final-permitted-M1-close rule, not a strategy change.

**Next:** the only permitted outcome run is combined development Jan-2023 through Feb-2025. Validation/holdout remain sealed. The development workflow is implemented but untriggered.


## 2026-09-23 — Stop Engine J v0.1 after decisive development failure

**Decision:** Stop Engine J v0.1 before validation. Do not tune the same 24+6 volatility-compression/direct-breakout center rule on the inspected development pool.

**Evidence:** 307 accepted trades from 349 qualifying breakouts; T40 hit rate 27.04%; gross expectancy about -USD0.15/trade; primary-cost expectancy about -USD5.15/trade; PF 0.671; total net -USD1,581.53; max drawdown USD1,659.93. DEV-A expectancy was about -USD6.95/trade and DEV-B about -USD3.48/trade. The 95% moving-block bootstrap primary-cost expectancy interval was approximately -USD7.93 to -USD2.27.

**Gate:** the >=100 trade-count requirement and implementation integrity checks passed. Combined expectancy, both subperiod expectancy tests, PF, drawdown and recovery factor failed.

**Interpretation:** Engine J solved frequency easily but did not create enough gross edge. DEV-B showed improvement and gross expectancy around +USD1.52/trade, but this remained materially below the frozen USD5 round-trip cost and did not justify post-hoc tuning.

**Protection:** Mar-Aug 2025 validation and Sep-2025 through Feb-2026 fresh holdout were not loaded or inspected.

**Next:** move to a genuinely different prospectively specified engine family. Do not run a compression/breakout parameter grid or change the frozen T40 target after seeing diagnostics. EXP-015 remains paused.


## 2026-09-23 — Shift primary discovery from sequential pattern engines to direct multi-market scanning

**Decision:** Stop using one handcrafted XAUUSD pattern family at a time as the primary discovery loop.

Freeze Engine K v0.1 as a direct multi-market target-move forecasting engine.

**Reason:** The user's operating requirement is to continuously scan all supported markets and identify where an economically useful move is most likely next. Engines G–J showed that a sequence of isolated handcrafted XAU theses can consume time without addressing that cross-market selection problem directly.

Engine K therefore:

- scores both directions every five minutes;
- scans the full supported Wave-1 universe simultaneously;
- predicts target-first probability directly from causal market-state features;
- ranks by probability and conservative EV;
- trades nothing when no candidate qualifies.

This is not permission to claim certainty. “Maximum probability” means calibrated out-of-sample probability and positive expected value.

## 2026-09-23 — Freeze Engine K Wave-1 universe and rolling-sample provenance

**Decision:** Initial Engine-K execution-research universe is XAUUSD, EURUSD, GBPUSD, USDJPY, EURJPY, AUDUSD, USDCAD, and USDCHF.

XAGUSD is forecast-only pending contract economics.

Pinned GetData GitHub sample commits/blob SHAs are recorded in `research/provenance/EXP-022-wave1-data-manifest.md`.

Because those public samples roll weekly, Engine K must fetch pinned commits rather than `main`.

Frozen Engine-K split:

- training 2026-03-23 through 2026-05-31;
- calibration 2026-06-01 through 2026-06-30;
- secondary test 2026-07-01 through 2026-08-31;
- final holdout 2026-09-01 through 2026-09-22;
- 2026-09-23 excluded as potentially incomplete.


## 2026-09-23 — Pre-outcome cleanup Engine K before first target/model outcomes

**Decision:** Keep Engine K / EXP-022 as the primary discovery path, but remove implementation/spec ambiguities before any target label, fitted probability, calibration result, or trading outcome is inspected.

**Universe:** primary executable model is frozen to XAUUSD, EURUSD, GBPUSD, USDJPY, EURJPY, AUDUSD, USDCAD and USDCHF. XAGUSD, NAS100, US30 and SPX500 remain forecast-only and may not influence primary fitting/calibration/ranking/P&L until contract economics are frozen.

**Target clarification:** the non-Gold 0.14/0.19/0.23 x MTR20 ladder remains a prospectively frozen forecast-label grid only. It does not replace the engine-conditioned target doctrine in PNL-EQUIVALENT-SIZING. Any non-Gold rung must independently pass execution feasibility.

**Research economics:** before broker-native specifications are available, freeze primary round-trip cost = 10% of gross target and stress cost = 20% of gross target. Freeze USD20 structural-stop risk, <=100x notional/equity, and <=USD100 research margin at a 1:500 research reference. These are research screens, not broker claims.

**Probability gate:** require calibrated p >= max(0.60, p_break_even + 0.05), with p_break_even = (stop risk + primary cost)/(target + stop risk), plus primary-cost EV >0.

**Causality/data cleanup:** complete 5m bars require 5 M1 rows, complete 1h context bars require 60 M1 rows, next-open entry gap <=5 chronological minutes, and all 29 model features are now explicitly defined from information available by decision time.

**Evidence split:** training Mar-23–May-31; calibration June; secondary July-August; final common holdout Sep-1–Sep-22; Sep-23 excluded. The September holdout is an initial OOS check and cannot by itself authorize live deployment.

**Outcome status:** ZERO Engine-K target outcomes and ZERO model outcomes at this decision.

**BTC / universe policy:** BTCUSD/BTCUSDT and further markets remain planned expansion candidates, but are not admitted to v0.1 until exact pinned data plus venue/contract/cost/margin economics are prospectively documented. The 8-execution/12-observed universe is sufficient for the first architecture/economic proof, not the intended final production universe.


## 2026-09-23 — Engine K final cleanup preflight passed with zero outcomes

**Decision:** Accept the reconciled Engine-K v0.1 pre-outcome implementation/economics/provenance checkpoint.

**Tested repository SHA:** `2c319cd45cbae6cdb1934540f6933890886c1812`.

**Durable result commit:** `48aa0af80b7fc2fff1dab56d3fb617b1c2140f3f`.

**Evidence:** all 11 frozen cleanup self-tests passed. Across training+calibration scope through June 30, the 8 execution markets produced 205,196 causal structural states and 7,098 target rungs that already pass frozen stop-risk/notional/margin feasibility before any probability qualification. The 4 forecast-only markets produced 103,041 structural states but zero executable economic rungs by design.

**Protection:** no target outcomes, fitted model outcomes, training result, calibration result, July-August state/outcome diagnostics, or September final-holdout outcomes were inspected by the authoritative preflight.

**Next:** training Mar-23 through May-31 and probability calibration on June only. Checkpoint before any July-August secondary-test outcome.


## 2026-09-23 — Stop Engine K v0.1 before secondary test

**Decision:** EXP-022 Engine K v0.1 fails the frozen training/June-calibration gate. Do not inspect July-August secondary-test outcomes or September final holdout.

**Result commit:** `d24e05ca513777d63a5d0f6762dfdb35bc42cfc3`.

**Economic-universe evidence:** 7,098 admissible labeled rungs were generated, but all were XAUUSD. EURUSD, GBPUSD, USDJPY, EURJPY, AUDUSD, USDCAD and USDCHF each produced zero rungs after the frozen stop-risk/notional/margin gates. Their target outcomes were therefore not labeled.

**Model evidence on XAU:** June raw AUC was about 0.627 / 0.618 / 0.626 for T30/T40/T50. Frozen Platt-calibrated probabilities never reached 0.60: June maxima were about 0.499 / 0.420 / 0.347. Therefore zero candidate rungs qualified and the one-open simulation placed zero trades.

**Gate:** market coverage FAIL; >=100 qualified trades FAIL; hit-rate/expectancy gates unavailable/FAIL because zero trades; causality/provenance PASS.

**Protection:** July-August and September remain sealed.

**Interpretation:** v0.1 failed both its multi-market economic admission design and its XAU qualification-frequency requirement. Do not lower the probability floor or tune the inspected XAU model. Non-Gold target economics may be prospectively redesigned in a new version because their target outcomes were never inspected.


## 2026-09-24 — Freeze Engine K v0.2 / EXP-023 after v0.1 economic-admission failure

**Decision:** Stop EXP-022 v0.1 before July-August and freeze Engine K v0.2 prospectively using only inspected training/June-calibration facts.

**v0.1 evidence used:** all 7,098 executable labeled rungs were XAUUSD; all seven FX markets had zero economic admission; zero trades qualified under the 60% floor; June raw HGB discrimination was non-zero but modest; protected later periods remain unopened.

**v0.2 design:** preserve candidate clock, structural stop, features, primary HGB, Platt calibration, risk/notional/margin rules and evidence split. Keep Gold +3/+4/+5. For non-Gold define target first as 1.5R/2.0R/2.5R from unchanged structural stop, then calculate downward-rounded USD30/USD40/USD50-equivalent size. Qualification becomes max(50%, break-even +10pp) plus positive primary EV.

**Methodology:** this preserves `docs/PNL-EQUIVALENT-SIZING.md` because native target is still defined before lot size.

**Outcome status:** zero v0.2 target/model outcomes at freeze.

**Next:** zero-outcome preflight through June. Require >=200 economically admissible states in every execution market before labels.


## 2026-09-24 — Adopt asynchronous long-running pipeline discipline

**Decision:** Treat efficient handling of long GitHub Actions runs as a formal project operating rule.

After a long-running pipeline is triggered, confirm the intended run once. While it executes, do only independent work that cannot alter the running experiment. If no independent work remains, end the turn rather than repeatedly polling GitHub.

When the user returns, resume by reading the durable GitHub result and applying the frozen gate.

**Repository safety:** do not mutate frozen inputs of a running experiment. Result-committing workflows should rebase from current `main` before pushing so safe unrelated commits do not create avoidable push races.

**Policy:** `docs/PIPELINE-WORKFLOW-POLICY.md`.


## 2026-09-24 — Engine K v0.2 zero-outcome preflight passed

**Decision:** Accept EXP-023 v0.2 economic admission design and permit training + June calibration.

**Result commit:** `02a2ab0b1ea7f21092b06165a0ca8f0638d4c41b`.

**Evidence:** all 8 execution markets exceeded the frozen >=200 unique admissible-state threshold through June. Total coverage was 94,238 unique admissible states / 281,955 admissible rungs. The weakest market, XAUUSD, still produced 2,366 admissible states.

**Integrity:** all v0.2 zero-outcome self-tests passed. No target/model outcomes were calculated; July-August and September remain unopened.

**Next:** run only Mar23-May31 training + June calibration under the frozen v0.2 model/economic gates. Stop before secondary testing if any mandatory gate fails.


## 2026-09-24 — Stop Engine K v0.2 before secondary test

**Decision:** EXP-023 fails its frozen training/June gate. Do not inspect July-August or September.

**Result/model commit:** `763aefadbe56ee7012b475dcb677f6f78d8036ec`.

**Evidence:** 281,955 labeled rungs across all eight execution markets; June AUC approximately 0.674 / 0.710 / 0.743 for T30/T40/T50. Despite this rank discrimination, the frozen qualification rule yielded only 2 combined trades and 0 June trades.

**Gate:** market coverage PASS; combined >=100 trades FAIL; June >=20 trades FAIL; June hit-rate/expectancy/PF gates FAIL/unavailable; DD/integrity/protection PASS.

**Interpretation:** v0.2 solved cross-market economic admission but not trade qualification density. The two combined trades both won but are statistically meaningless and cannot justify secondary testing.

**Protection:** July-August secondary test and September final holdout remain sealed.

**Next:** new prospectively frozen version only; no threshold relaxation inside v0.2.


## 2026-09-24 — Freeze Engine K v0.3 / EXP-024

**Decision:** After v0.2 failed trade-density gates, freeze a new version rather than lowering the v0.2 threshold.

**Why:** v0.2 showed meaningful June rank discrimination (AUC about 0.674/0.710/0.743) but only 2 combined qualified trades and 0 June trades. July-Aug and September remained sealed.

**v0.3 changes prospectively:**

- fit HGB on Mar23-Apr30;
- calibrate on May only;
- gate on June only;
- use market-direction-aware Platt calibration;
- qualify by positive primary EV and positive stress EV;
- no universal probability floor.

**What stays unchanged:** target ladders, equivalent sizing, costs, structural stop, 29 causal features, HGB hyperparameters, one-open logic, daily budget rules.

**Protection:** Mar-Jun is reusable inspected development data. Jul-Aug and Sep remain pristine for later stages.

**Next:** run the June gate only. Fail -> stop before secondary.


## 2026-09-24 — Stop Engine K v0.3 after failed June economics

**Decision:** EXP-024 fails the June development gate. Do not inspect July-Aug or September.

**Result commit:** `db53f3a96fbbb6ed7b1b01f25e931e4140bec215`.

**Evidence:** 39 June trades across 19 weekdays; hit rate 38.46% vs 46.79% mean stress break-even; primary expectancy -USD0.22/trade; stress expectancy -USD3.89/trade; primary PF 0.983; stress PF 0.742; max drawdown USD212.34.

**Positive diagnostic:** calibrated June AUC remained ~0.672 / 0.708 / 0.740 for T30/T40/T50. Candidate/trade density is no longer the blocker.

**Interpretation:** the scanner appears to contain ranking information, but the manually selected model/calibration/qualification configuration does not convert that information into positive economic expectancy.

**Next methodology change:** stop manual version-by-version threshold selection. Use the reusable Mar-Jun development pool for a prospectively bounded chronological model/configuration search, freeze the selected configuration, then expose Jul-Aug exactly once. September remains final holdout.


## 2026-09-24 — Freeze Engine K v0.4 / EXP-025 bounded walk-forward selection

**Decision:** stop manual Engine-K threshold/version iteration and use a small prospectively bounded configuration search on the already-inspected Mar-Jun development pool.

**Search space:** exactly 12 configurations = 2 HGB variants x 2 Platt calibration variants x 3 stress-EV qualification policies.

**Evaluation:** six expanding chronological walk-forward folds. Each configuration is judged only on forward evaluation slices, with July-Aug and September sealed.

**Pass philosophy:** sufficient trade count, positive pooled primary/stress expectancy, PF thresholds, multi-fold stress stability, hit rate above stress break-even, stress MDD <=USD150, and <=60% market concentration.

**Winner philosophy:** choose stability first, not total P&L or AUC. Lexicographic order = worst-fold stress expectancy, pooled stress PF, lower stress DD, trade count, config ID.

**Stopping rule:** if no configuration passes, stop Engine K tuning on this Mar-Jun pool and do not inspect July-Aug.

**Outcome status at freeze:** EXP-025 metrics not calculated; no selected config; Jul-Aug unopened; Sep unopened.


## 2026-09-24 — Stop Engine K tuning after EXP-025 no-pass walk-forward

**Decision:** No EXP-025 configuration passed the frozen walk-forward gate. No winner is selected and Jul-Aug remains sealed.

**Result commit:** `24ce35448cb93158aadeb843dce928199c0c5385`.

**Evidence:** all 12 frozen configurations were evaluated across all six frozen chronological forward folds. None satisfied the combined trade-density, multi-fold stability, stress expectancy, PF, hit-rate-vs-break-even, drawdown and concentration requirements.

Some configurations became mildly positive at primary cost, but none remained economically robust under the frozen stress cost or across folds. M1-C1-Q3 reached +USD2.15/trade primary but -USD1.67/trade stress with stress MDD ~USD301.54. M2-C2-Q3 reached +USD0.86/trade primary but -USD2.62/trade stress with stress MDD ~USD505.51.

**Protection:** Jul-Aug secondary test and Sep final holdout were not loaded/labeled.

**Methodological conclusion:** stop adding Engine-K configurations or thresholds on the Mar-Jun pool. The next research step must broaden evidence or materially change the prediction/target design.

**Anti-mining:** do not weaken EXP-025 gates, select a near-miss, or open protected periods.


## 2026-09-24 — Freeze Engine L v0.1 / EXP-026 entry architecture

**Decision:** respond to the persistent Engine-K economic failure by changing the entry architecture rather than adding more history or tuning probability thresholds.

**Observed architectural problem:** Engine K treated a completed 5m forecast as an immediate trade instruction. Entry was the next active M1 open and the stop remained an older 5m pivot. There was no favorable execution-price requirement or microstructure confirmation.

**Engine L thesis:** forecast should arm a market, not force a trade.

Frozen flow:

- fixed raw T40 forecast;
- higher-scoring direction armed;
- 15 active-M1 lifetime;
- 0.20*V5 favorable pullback;
- causal M1 resumption confirmation;
- next-M1-open entry;
- fresh M1 pullback-extreme stop;
- T40 only;
- matched immediate-entry control.

**Protection:** Mar-Jun development reusable; Jul-Aug and Sep sealed.

**Next:** zero-outcome mechanics preflight. Require >=100 admissible trigger paths per market and both directions before any Engine-L target/P&L outcome.


## 2026-09-24 — Treat multi-timeframe top-down analysis as design guidance

**Decision:** preserve the user-supplied discretionary principle that different timeframes should have different jobs, without adopting social-media claims such as “15m is best” as evidence.

Research guidance:

- 4H / 1H: context, direction, major location;
- 15m: intraday setup/location;
- 5m: tactical forecast/arm;
- 1m: execution and fresh stop.

**Current experiment discipline:** do not mutate Engine L v0.1 with new MTF gates after its zero-outcome preflight. First test whether its entry redesign materially beats the matched immediate-entry control. If execution helps but economics remain insufficient, a future prospective version may add the explicit MTF context layer.

Guidance file: `research/notes/MULTI-TIMEFRAME-INTRADAY-GUIDANCE.md`.


## 2026-09-24 — Engine L v0.1 mechanics preflight passed

**Result commit:** `b19d4ef6c3a689117fc5b8237167322bd64a2aa7`.

All eight execution markets passed the frozen zero-outcome entry-mechanics gate. Total admissible micro-entry paths through Jun30: 12,532. Both directions were represented on every market.

No Engine-L target or P&L outcomes were calculated. Jul-Aug and Sep remain sealed.

**Next permitted stage:** Engine-L development against the matched immediate-entry control.
