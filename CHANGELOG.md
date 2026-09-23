# Changelog

## 2026-09-23

- Froze Engine H v0.3 / EXP-019 prospectively with post-raid confirmed 1m structural stops, fixed actual T40 target, and T30/T50 target-ladder diagnostics.
- Expanded v0.3 development backward into complete previously unused 2023 data instead of lowering the >=100 evidence threshold; froze DEV-A (2023) and DEV-B (Jan-2024-Feb-2025) stability checks.
- EXP-019 development produced 58 accepted trades, primary-cost expectancy about -USD4.52/trade, PF about 0.703, and 95% bootstrap expectancy interval about -USD11.60 to +USD2.69.
- Both development subperiods were negative (DEV-A about -USD7.18/trade; DEV-B about -USD1.24/trade). Stopped H v0.3 before validation and paused further immediate iteration of the H thesis family.

- Froze Engine H v0.2 / EXP-018 prospectively with simplified confirmation: MSS within 20 active M1 bars followed by next-active-M1-open entry; removed v0.1 displacement/new-FVG/retracement requirements.
- Ran EXP-018 development only. Of 180 in-window raids, 69 reached next-open economic admission, but only 6 passed all frozen geometry/risk gates versus the >=100 minimum.
- H v0.2 primary-cost expectancy was approximately +USD0.08/trade with PF about 1.004 and 95% bootstrap expectancy interval about -USD32.65 to +USD40.00; classified INSUFFICIENT EVIDENCE.
- Stopped H v0.2 before validation and preserved validation/fresh holdout untouched. The next bottleneck is target/stop/economic geometry rather than lower-timeframe confirmation.

- Froze Engine H — Range Raid into Pre-existing FVG Reversal v0.1 prospectively from the two user-provided video motifs before any outcomes.
- Ran EXP-017 development only: 341 qualifying raids, 180 in-window raids, but only 2 accepted filled trades versus the frozen >=100 minimum.
- Classified Engine H v0.1 as INSUFFICIENT EVIDENCE despite a positive two-trade point expectancy; the 95% bootstrap expectancy interval spanned about -USD 34.66 to +USD 53.36.
- Stopped EXP-017 before validation and preserved validation/fresh holdout untouched. No H v0.1 retuning performed.

- Froze Engine G — Contextual Liquidity Reversal v0.1 prospectively before any Engine G outcome calculation.
- Added the complete mechanical specification at `strategies/engine-g-contextual-liquidity-reversal/SPEC-v0.1.md`, including integer-tick price normalization, dynamic liquidity-instance/cluster lifecycle, always-on liquidity consumption, explicit FVG/target logic, gross USD 40 structural-risk admission, independent counterfactual target labels, provenance manifest, bootstrap evidence, and delayed sensitivity rules.
- Opened `EXP-016-engine-g-contextual-liquidity-reversal-v0.1` with checkpoint 0 marked frozen/not-yet-run.
- Froze the same-feed primary split: development Jan 2024–Feb 2025, validation Mar–Aug 2025, fresh holdout Sep 2025–Feb 2026; quarantined Mar–Aug 20 2026 from the primary decision.
- Froze the external Dukascopy-derived source snapshot to `kevingtlin/Market-Data-Lab` commit `922f83a60cc574e7395fb27397077288055a1ef6` plus the per-file BID blob manifest.
- Kept EXP-015 paused pending a reproducible validated strategy engine.
- Ran the frozen EXP-016 Engine G v0.1 development split only after the spec/provenance/implementation checkpoints were committed.
- Engine G v0.1 development produced 71 accepted trades, about 16.9% S1 hits, -USD 9.27/trade at the primary 0.50-XAU cost stress, profit factor about 0.496, and a 95% block-bootstrap expectancy interval entirely below zero (-USD 15.14 to -USD 2.52).
- Stopped EXP-016 v0.1 before validation because the >=100 development minimum was not reached and the mandatory positive development-expectancy criterion failed. Preserved validation and fresh holdout untouched; no sensitivity diagnostics were run.

- Froze a numerical multi-dimensional EXP-014 reproduction-acceptance protocol before new recovery outcomes.
- Audited the March 1–August 20, 2026 Dukascopy-derived XAUUSD BID M1 research series: 230,813 rows, matching EXP-002's recorded row count; zero duplicate timestamps and zero invalid OHLC rows.
- Systematically checkpointed original Engine A recovery variants A1–A9, changing identifiable ambiguities rather than tuning multiple parameters together.
- Identified A6 as the closest causal recovery diagnostic: 333 trades, 164/169 development/holdout split, average structural risk about 1.053 Gold, but only about 15.0% overall T5 and near-flat holdout expectancy.
- Tested A8 forensic intrabar 5m-sweep timing leakage; it did not reproduce EXP-002 and remains non-deployable.
- Tested A9 forensic optimistic fill-bar ordering; it improved target-first results but still remained materially below the EXP-002 ladder/expectancy and remains non-deployable.
- Closed EXP-014 Part A: the original EXP-002 implementation is honestly **unrecoverable from the surviving evidence**. Preserved EXP-002 as historical exploratory evidence rather than relabeling a failed reconstruction as the original.
- Froze EXP-014 Part B in `docs/PNL-EQUIVALENT-SIZING.md`: engine-conditioned native target logic is the forward target-distance method; volatility-burden equivalence is diagnostic only.
- Clarified that the USD 60 emergency hard-loss ceiling is not a normal sizing budget.
- Completed EXP-014 overall.
- Kept EXP-015 paused because no reproducible validated strategy engine currently exists to emit production candidate streams.
- Advanced the project to Phase 2: prospectively define and validate a new causal reproducible strategy engine before ranker work resumes.
- Updated README, project/system blueprint, roadmap, handoff, current status, objectives, risk framework, strategy status, superseded assumptions, Engine A recovery spec, and EXP-015 to reflect the post-EXP-014 state.

## 2026-09-22

- Initialized isolated project repository.
- Declared this repository + originating chat as the only authorized project context.
- Recorded target-first objective and daily consistency criteria.
- Recorded working risk framework.
- Recorded data-source policy.
- Recorded Badar-inspired Engine A findings.
- Recorded rejection of first Engine B/C formulations.
- Completed Engine D session/opening-range momentum screen; current formulations not promoted.
- Completed Engine E volatility-compression/expansion screen; current formulations not promoted.
- Changed next research phase from more XAU-only tuning to multi-asset opportunity expansion.

- Completed EXP-006 multi-asset data/target-normalization checkpoint using a public independent 1m sample feed for XAUUSD, EURUSD, GBPUSD, and USDJPY.
- Found that equalizing the Gold USD 5 target by median-hourly-volatility burden implies roughly 3–4 pip FX targets but about 1.2–2.1 standard lots for a USD 50 gross target; rejected that sizing rule for portfolio economics.
- Set the next step to freeze a fully mechanical portable Engine A variant and a structural-stop/fixed-risk target framework before cross-market performance testing.

- Froze Engine A v0.2-portable before cross-market outcome inspection and opened EXP-007.
- Checkpointed EXP-007 XAUUSD arm: holdout 133 trades, 18.8% 2.5R target-first wins, -0.305R/trade, 66.1% losing days, and 96.6% <= USD 50 days; XAU arm rejected without retuning.
- Checkpointed EXP-007 EURUSD arm: holdout improved to 31.25% 2.5R wins and +0.167R/trade, but development was negative, <= USD 50 days remained 88.1%, and median notional/equity was about 139x; not promoted.
- Checkpointed EXP-007 GBPUSD arm: development +0.139R/trade deteriorated to -0.111R/trade in holdout; 94.9% of holdout days were <= USD 50 and median notional/equity was about 118x; not promoted.
- Completed EXP-007 portable Engine A cross-market screen.
- USDJPY was the only arm with positive mean R in both development (+0.075R) and holdout (+0.263R), but 86.4% of holdout days remained <= USD 50 and median notional/equity was about 178x; retained only as a statistical research lead.
- No EXP-007 arm promoted or combined into a portfolio.

- Completed EXP-008 XAGUSD second-wave Engine A test: holdout 23.53% 2.5R wins, -0.161R/trade, 55.9% losing days, and 93.2% <= USD 50 days; rejected.
- Paused further Engine A market expansion/loosening and moved next research step to a genuinely independent strategy family.

- Froze Engine F v0.1 statistical extension/re-entry/mean-reversion rules prospectively and opened EXP-009.
- Checkpointed EXP-009 XAUUSD arm: development 13 trades at -0.192R/trade; holdout 24 trades at +0.021R/trade; <= USD 50 days were 100% in both splits. XAUUSD arm not promoted and rules not retuned.
- Checkpointed EXP-009 USDJPY arm: development +0.016R/trade on 31 trades, holdout -0.222R/trade on 18 trades, 98.31% holdout <= USD 50 days, and about 258x median notional/equity; not promoted and not retuned.
- Checkpointed EXP-009 EURUSD arm: development -0.125R/trade on 24 trades, holdout +0.242R/trade on 31 trades, 98.31% holdout <= USD 50 days, and about 204x median notional/equity; not promoted because the splits changed sign.
- Completed EXP-009 Engine F screen. GBPUSD was the only arm positive in both splits (+0.138R development, +0.080R holdout), but holdout hit rate was only 28.57%, <= USD 50 days were 100%, and median notional/equity was about 181x; retained as research lead only.
- Closed Engine F v0.1 without retuning. The project now has two frozen research leads: USDJPY / Engine A v0.2 and GBPUSD / Engine F v0.1.
- Set the next step to a prospective two-lead portfolio daily-distribution screen under the USD 40 / USD 60 loss framework and +USD 150 profit stop.
- Completed EXP-010 two-lead portfolio screen. Holdout lead correlation was about +0.03, but 86.44% of days remained <= USD 50, 0% reached >= USD 150, losing days were 44.07%, and max drawdown was about USD 200.53.
- The loss state machine limited the worst holdout day to -USD 40, but peak simultaneous notional/equity exceeded 1,200x.
- No portfolio promotion. Shifted next step to a mathematical feasibility frontier for the current daily-distribution objective before searching for another engine or changing targets.
- Clarified that the project end objective is to build a working multi-market trading system; research remains the validation layer.
- Replaced the forward fixed USD 20 risk / USD 50 target assumption with a fixed-size target-ladder framework anchored at 0.10 lot XAUUSD and initially 0.10 standard lot for major FX pending broker verification.
- Expanded successful-trade capture targets to approximately USD 30 / 40 / 50 / 70 / 100+ and removed the hard 3–4 trades/day assumption in favor of opportunity-driven trade count subject to risk, margin, correlation, and quality gates.
- Superseded EXP-011 before results because its fixed-payoff/max-4-trades assumptions no longer matched the user’s operating objective.
- Opened EXP-012 to rebuild scanner economics and re-evaluate retained USDJPY Engine A / GBPUSD Engine F leads under fixed-size target ladders.
- Re-evaluated USDJPY / Engine A v0.2 at fixed 0.10 lot: holdout T30 about 7.1%, T50 about 4.1%; no longer a priority fixed-size income lead.
- Re-evaluated GBPUSD / Engine F v0.1 at fixed 0.10 lot: holdout T30 about 11.1%, T50+ 0%; no longer a priority fixed-size income lead.
- Re-evaluated XAUUSD / Engine A v0.2 at fixed 0.10 lot: Gold naturally supports USD 30–100 movement, but median holdout structural-stop risk was about USD 51.90.
- Applied the predeclared <= USD 40 fixed-size structural-risk gate to Gold; 50 holdout trades survived, with T30/T40/T50/T70/T100 hit rates of roughly 48%/34%/30%/28%/20%.
- Tested fixed-target expectancy on the risk-gated Gold subset: T30 fell from about +USD 7.13/trade in development to about +USD 0.02/trade in holdout before costs; higher target rungs were negative.
- No existing engine promoted. Next phase is a fixed-size market-universe economic feasibility map followed by a cross-market target-first opportunity ranker.
- Opened EXP-013 fixed-size market-universe economic feasibility map.
- Development-only map confirmed XAUUSD as the dominant fixed-size economic fit and ranked GBPUSD, USDCHF, EURUSD, and AUDUSD as the strongest documented FX complements.
- EURJPY, USDJPY, and USDCAD ranked lower for USD 30–50 at 0.10 lot; GBPJPY matching sample unavailable; XAGUSD left unranked pending fixed contract economics.
- Froze first scanner universe: XAUUSD, GBPUSD, USDCHF, EURUSD, AUDUSD.
- Next phase: prospectively frozen target-first opportunity ranker across the five-market universe.
- Corrected the user's cross-market sizing intent: XAUUSD remains 0.10 lot, while other symbols require P&L-equivalent lot sizes aimed at an approximately USD 50 normal target rather than identical 0.10-lot sizing.
- Reclassified EXP-012/013 same-0.10-lot FX conclusions as diagnostic only; preserved their volatility/Gold findings.
- Restored the original EXP-002 XAUUSD Engine A as an active positive-expectancy research lead distinct from the later v0.2-portable rewrite.
- Opened EXP-014 as a plan-only checkpoint to recover/reproduce original Engine A and freeze the equivalent-lot rule before any further outcome testing.

- Reframed repository identity from research project to **Target-First Trading System**; research remains the validation layer.
- Added authoritative system blueprint, original project context, detailed Badar video evidence, timeframe/context model, superseded-assumptions registry, strategy-engine candidate contract, and staged build/deployment roadmap.
- Restored the architecture rule that validated strategy engines generate candidates and the target-first model ranks/selects them.
- Corrected strategy status so original EXP-002 XAUUSD Engine A is the active recovery lead; v0.2-portable is a separate historical rewrite.
- Activated EXP-014 as the required original Engine A recovery + equivalent-sizing gate.
- Renumbered the duplicate target-first ranker experiment from EXP-014 to EXP-015 and paused it pending EXP-014.
- Preserved EXP-015 Stage-1 broad XAU candidate statistics as diagnostics only.
- Reclassified EXP-013 same-0.10-lot FX market ranking as a historical diagnostic, not the forward scanner-universe rule.
- Strengthened daily-distribution metrics to include median daily P&L and 5-day rolling consistency.
- Added explicit common-factor/correlation exposure controls to the system risk framework.
