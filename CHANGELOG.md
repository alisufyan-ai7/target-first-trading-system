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

- Frozen Engine I v0.1 / EXP-020 prospectively before any Engine-I outcome calculation.
- Engine I changes causal family to session expansion/continuation: 15m direction -> Asian boundary expansion -> controlled pullback -> 1m continuation -> structural pullback stop -> T40.
- Frozen Jan-2023–Feb-2025 development with DEV-A/DEV-B stability, Mar-Aug 2025 validation, Sep-2025–Feb-2026 fresh holdout, USD5 primary round-trip cost, and >=100-trade / expectancy / PF / drawdown gates.
- Explicitly prohibited an Engine-I v0.1 parameter grid or post-failure sensitivity rescue; next checkpoint is user approval plus implementation/provenance verification, not a backtest.

- Completed Engine I v0.1 pre-outcome implementation/preflight with zero strategy outcomes calculated.
- Added exact-arithmetic Engine-I implementation, preflight verifier, development runner, and separate preflight/development GitHub Actions workflows.
- Final preflight verified 27 Dec-2022–Feb-2025 warm-up/development files (1,182,240 rows) against frozen blob/byte/month/chronology/OHLC rules and passed all 11 self/causality tests.
- Confirmed validation/holdout were not loaded; development workflow remains untriggered. Next permitted outcome is EXP-020 development only.

- Engine I v0.1 completed development with 197 accepted trades, satisfying the frozen >=100 frequency requirement.
- Engine I failed economics decisively: T40 24.37%, gross expectancy about -USD0.15/trade, primary-cost expectancy about -USD5.15/trade, PF 0.631, total net -USD1,015.49, max drawdown USD1,060.90.
- Both predeclared development subperiods failed at primary cost: DEV-A about -USD6.20/trade and DEV-B about -USD4.09/trade; 95% bootstrap expectancy interval was entirely negative at about -USD8.38 to -USD1.94.
- Stopped EXP-020 before validation. Mar-Aug 2025 validation and Sep-2025–Feb-2026 fresh holdout remain untouched.
- Prohibited post-hoc Engine-I target switching/parameter rescue; next action is a genuinely different engine family.

- Frozen Engine J v0.1 / EXP-021 prospectively after Engine I's decisive development failure.
- Engine J tests a new volatility-compression/direct-breakout family: 24-bar same-day baseline -> 6-bar compression -> strong 5m breakout -> next-open -> breakout-bar stop -> T40.
- Removed Engine-I-specific dependencies: no Asian boundary, trend context, pullback, or continuation confirmation.
- Preserved the same sealed validation/holdout, USD5 primary cost, >=100-trade development minimum, subperiod expectancy, PF, drawdown and recovery gates.
- Zero Engine-J outcomes calculated; implementation/backtest not started.

- Completed Engine J v0.1 pre-outcome implementation/preflight with zero strategy outcomes calculated.
- Added exact-arithmetic Engine-J implementation, preflight verifier, development runner, and separate preflight/development GitHub Actions workflows.
- Implemented frozen same-day 24+6 active-5m compression logic using exact integer inequalities, direct breakout entry, breakout-bar structural stop, conservative same-bar handling, and chronological 20:00 close.
- Final preflight verified 27 Dec-2022–Feb-2025 warm-up/development files (1,182,240 rows / 59,108,737 bytes) against frozen blob/byte/month/chronology/OHLC rules and passed all 16 Engine-J self/causality tests.
- Confirmed validation/holdout were not loaded; Engine-J development workflow remains untriggered. Next permitted outcome is EXP-021 development only.

- Engine J v0.1 completed development with 307 accepted trades, comfortably satisfying the frozen >=100 frequency requirement.
- Engine J failed economics decisively: T40 27.04%, gross expectancy about -USD0.15/trade, primary-cost expectancy about -USD5.15/trade, PF 0.671, total net -USD1,581.53, max drawdown USD1,659.93.
- Both predeclared development subperiods failed at primary cost: DEV-A about -USD6.95/trade and DEV-B about -USD3.48/trade; 95% bootstrap expectancy interval was entirely negative at about -USD7.93 to -USD2.27.
- DEV-B was gross-positive at about +USD1.52/trade before cost, but not enough to survive the frozen USD5 round-trip primary cost.
- Stopped EXP-021 before validation. Mar-Aug 2025 validation and Sep-2025–Feb-2026 fresh holdout remain untouched.
- Prohibited post-hoc compression/breakout threshold tuning and target switching; next action is a genuinely different engine family.

- Course-corrected the primary discovery path after user review: stop relying on sequential single-pattern XAU engines as the main approach.
- Froze Engine K v0.1 / EXP-022 — Multi-Market Direct Target-Move Scanner — with zero outcomes calculated.
- Engine K scans both long and short states every five minutes across XAUUSD, EURUSD, GBPUSD, USDJPY, EURJPY, AUDUSD, USDCAD, and USDCHF; XAGUSD is forecast-only pending execution economics.
- Frozen Gold movement targets at +3/+4/+5 XAU and a prospectively fixed non-Gold movement-equivalence ladder, followed by P&L-equivalent sizing and a USD20 primary structural-risk gate.
- Frozen pooled multi-market probability model, p>=0.60 qualification, positive conservative-EV requirement, and one-open-position v0.1 portfolio rule.
- Completed EXP-022 Checkpoint 1: pinned exact rolling GetData repositories, commit SHAs, CSV blob SHAs, sample row counts, research contract conventions, and common dates.
- Corrected Engine-K split to the currently pinned sample: training Mar23-May31, calibration Jun, secondary Jul-Aug, fresh common-sample holdout Sep1-Sep22; excluded Sep23 as potentially incomplete.
- Next: Engine-K causal implementation/preflight with zero target/model outcomes, then training+calibration across all Wave-1 markets together.

- Pre-outcome cleanup pass for Engine K / EXP-022 completed before any target/model outcomes.
- Reconciled the universe to 8 execution-research markets plus 4 forecast-only markets (XAGUSD, NAS100, US30, SPX500) and prohibited forecast-only markets from influencing executable model fit/calibration/ranking.
- Clarified the non-Gold MTR20 ladder as a forecast-label grid, not a replacement for the frozen P&L-equivalent sizing doctrine.
- Frozen research-only friction at 10% of gross target primary / 20% stress, USD20 stop-risk cap, 100x notional/equity cap, and USD100 margin cap at the 1:500 research reference.
- Strengthened qualification to calibrated p >= max(0.60, break-even probability + 0.05) plus positive primary-cost EV.
- Hardened data causality: complete 5m/1h bins only, <=5-minute next-entry gap, and explicit 29-feature causal contract.
- Reconciled EXP-022 dates to train Mar23-May31, calibrate June, secondary Jul-Aug, final Sep1-Sep22; Sep23 excluded.
- Recorded BTC/GBPJPY and other liquid markets as expansion candidates only after pinned data and executable contract economics are documented.

- Final Engine-K zero-outcome cleanup preflight passed on reconciled SHA `2c319cd45cbae6cdb1934540f6933890886c1812`; durable result commit `48aa0af80b7fc2fff1dab56d3fb617b1c2140f3f`.
- All 11 cleanup self-tests passed; no target/model outcomes were calculated.
- Through June 30 only, 8 execution markets produced 205,196 causal structural states and 7,098 economically admissible target rungs before probability qualification; 4 forecast-only markets remained isolated from executable economics.
- July-August secondary-test and September final-holdout state/outcome distributions remained unopened by the authoritative preflight.
- Next permitted stage: train on Mar23-May31 and calibrate on June only, then checkpoint before secondary testing.

- Closed Engine K v0.1 / EXP-022 before secondary testing: 7,098 admissible labeled rungs were all XAUUSD, all seven FX markets had zero executable rungs, and zero trades cleared the frozen 60% qualification floor.
- Preserved July-August 2026 secondary-test and Sep1-Sep22 final-holdout outcomes unopened.
- Opened EXP-023 / Engine K v0.2 prospectively with zero v0.2 outcomes.
- Kept Gold +3/+4/+5 unchanged; replaced non-Gold generic volatility-burden targets with target-before-size 1.5R/2R/2.5R structural target functions.
- Frozen v0.2 qualification at max(0.50, break-even+0.10), with existing positive-EV, USD20 stop-risk, notional and margin gates.
- Added separate v0.2 economics module and zero-outcome preflight requiring >=200 admissible states in every execution market before labeling.

- Added a formal long-running pipeline workflow policy at `docs/PIPELINE-WORKFLOW-POLICY.md`.
- Project default is now: confirm a long GitHub Actions run once, avoid repeated polling, use runtime only for independent non-contaminating work, otherwise end the turn and resume from the durable result later.
- Added explicit protection against mid-run experiment mutation, duplicate triggers, and result-commit races; result-committing workflows should rebase from current `main` before push.

- EXP-023 first preflight attempt failed before data preflight because binary floating-point tick rounding turned an exact EURUSD 1.5R boundary into one extra tick.
- No v0.2 target/model outcomes or protected-period evidence were inspected.
- Replaced v0.2 structural-distance/tick rounding with Decimal-based exact arithmetic and added an exact-boundary self-test; correction commit `d4983a061b86230d2f92b7fae80608a48c000a48`.

- EXP-023 v0.2 zero-outcome preflight passed; durable result commit `02a2ab0b1ea7f21092b06165a0ca8f0638d4c41b`.
- All 8 execution markets exceeded the frozen >=200 admissible-state threshold; total 94,238 unique admissible states and 281,955 admissible rungs through June.
- No v0.2 target/model outcomes or protected July-September outcomes were inspected.
- Added sealed v0.2 training + June calibration runner and workflow; July-August remains blocked behind the frozen pre-secondary gate.

- Engine K v0.2 training + June calibration completed and failed the frozen pre-secondary gate; durable result/model commit `763aefadbe56ee7012b475dcb677f6f78d8036ec`.
- v0.2 labeled 281,955 rungs across all 8 execution markets; June AUC about 0.674/0.710/0.743 for T30/T40/T50.
- Only 2 combined trades qualified and 0 June trades qualified, so the >=100 combined and >=20 June gates failed; June expectancy/PF/hit-rate gates were unavailable/failed.
- July-August secondary-test and September final-holdout outcomes remain unopened.
- v0.2 is closed; no post-hoc threshold relaxation permitted.

- Opened EXP-024 / Engine K v0.3 after v0.2 failed trade-density gates.
- v0.3 keeps v0.2 targets/economics/features/HGB but separates Mar-Apr fit, May calibration and June development gate.
- Added market-direction-aware Platt calibration and replaced arbitrary probability floors with positive primary-EV + positive stress-EV qualification.
- Added separate June-gate runner/workflow; July-Aug secondary test and September final holdout remain sealed.

- Engine K v0.3 June gate failed at durable result/model commit `db53f3a96fbbb6ed7b1b01f25e931e4140bec215`.
- June produced 39 one-open trades across 19 weekdays, solving the prior trade-density problem, but economics failed: -USD0.22/trade primary, -USD3.89/trade stress, PF 0.983/0.742, MDD USD212.34.
- Calibrated June AUC remained about 0.672/0.708/0.740 for T30/T40/T50, indicating rank signal without sufficient economic conversion.
- July-Aug secondary-test and September final-holdout remain unopened.
- Next methodology shifts from hand-picked threshold/version changes to bounded chronological development model/configuration selection on the reusable Mar-Jun pool.

- Opened EXP-025 / Engine K v0.4 bounded walk-forward selection after v0.3 failed June economics.
- Frozen exactly 12 configurations across two HGB variants, two Platt calibration methods, and three stress-EV qualification policies.
- Frozen six expanding chronological development folds through Jun30; Jul-Aug and Sep remain sealed.
- Added stability-first configuration gate/winner rule and a hard stop if no configuration passes.
- Added development-only EXP-025 walk-forward runner and workflow.

- EXP-025 bounded walk-forward completed with zero passing configurations; durable result commit `24ce35448cb93158aadeb843dce928199c0c5385`.
- All 12 frozen configurations were evaluated across all 6 chronological folds; no winner was selected.
- Best-looking primary-cost near-misses still failed stress expectancy/stability/drawdown gates.
- Jul-Aug secondary test and Sep final holdout remain unopened.
- Applied the prospectively frozen hard stop: no further Engine-K threshold/configuration tuning on the Mar-Jun development pool.
- Next research must broaden evidence or materially change the prediction/target design.

- Opened EXP-026 / Engine L v0.1 forecast-armed micro-entry after identifying immediate next-M1-open execution as a fundamental weakness in Engine K.
- Frozen one center entry architecture: 15-M1 arm, 0.20*V5 pullback, causal M1 resumption, next-open fill, fresh pullback-extreme stop, T40-only economics.
- Added matched immediate-entry control to isolate whether entry quality materially improves economics.
- Added separate Engine-L causal mechanics module and zero-outcome preflight requiring >=100 admissible trigger paths per market before P&L outcomes.
- Jul-Aug and Sep remain sealed.

- Engine L zero-outcome mechanics preflight passed at result commit `b19d4ef6c3a689117fc5b8237167322bd64a2aa7`: 12,532 admissible paths, all 8 markets >=100 and both directions represented.
- No Engine-L target/P&L outcomes were calculated; Jul-Aug and Sep remain sealed.
- Added `research/notes/MULTI-TIMEFRAME-INTRADAY-GUIDANCE.md` from user-supplied top-down timeframe examples.
- Guidance separates 4H/1H context, 15m setup/location, 5m arm, and 1m execution without treating any social-media timeframe claim as a hard rule.

- Frozen Engine L six-fold development runner before outcomes, including matched immediate-entry control, causal pending-arm resolution, and pooled entry-quality diagnostics.
- EXP-026 still has zero development P&L outcomes at the implementation checkpoint; Jul-Aug and Sep remain sealed.

- Engine L v0.1 development failed at durable result commit `7cacd739f80ab37a2f6465924937bd6489b1b966`.
- 303 trades across 57 weekdays; primary/stress expectancy -USD5.82 / -USD9.77 per trade; stress PF 0.469; zero positive-stress folds.
- Matched immediate control stress expectancy was -USD8.49/trade, so Engine L was worse by ~USD1.28/trade.
- Entry diagnostics showed median executed entry ~0.516 V5 worse than decision close after the pullback/resumption sequence: confirmation became chase.
- Raw forecast-score quartiles remained negative; no probability-threshold rescue is justified.
- Jul-Aug secondary and Sep final holdout remain unopened.

- Opened EXP-027 / Engine M v0.1 after Engine L showed breakout/resumption confirmation was chasing price.
- Frozen rule-based MTF hierarchy: H4/H1 context -> M15 H1-midpoint reclaim -> M5 rejection arm -> M1 precomputed retracement limit.
- Entry is fixed at 50% of the completed M5 arm range before future M1 prices are seen; stop is beyond the M5 arm extreme.
- Removed ML probability scoring from the v0.1 center design.
- Added matched immediate-entry control for later development and a zero-outcome preflight requiring >=50 admissible paths per market, both directions, >=600 total.
- Jul-Aug and Sep remain sealed.

- EXP-027 audit confirmed 1,581 mechanical Engine-M fills but only 126 old USD40-equivalent admissions; FX rejections were overwhelmingly notional+margin with stop risk already near USD20.
- Closed EXP-027 before outcomes because sizing/deployment feasibility was incorrectly filtering strategy validity.
- Opened EXP-028 / Engine M v0.2 signal-first validation with unchanged MTF/limit trading mechanics.
- Added maximum-safe-lot overlay under unchanged USD20 risk / USD50k notional / USD100 margin caps; Gold remains capped at 0.10 lot.
- Added GE40 / GE30 / LT30 utility reporting while retaining all filled valid signals for strategy-edge research.

- EXP-028 signal-first preflight passed at `68e52188de8abb2c708cacb611e347afb22a086d`: 1,581 filled valid signals, all eight markets passing, all safely deployable under unchanged caps.
- Reference-account utility: 66 GE40, 160 GE30, 1,355 LT30.
- No target/P&L outcomes yet; Jul-Aug and Sep remain sealed.

- Frozen EXP-028 development runner before outcomes: normalized-R signal edge, safe-lot USD500 portfolio, matched immediate-entry control, per-market diagnostics and daily-target reporting.
- Jul-Aug and Sep remain sealed at launch checkpoint.

- Engine M v0.2 development failed at `bd0ae3f18509c8e4e19fbe570766c961b1f4e3fb`.
- MTF limit entry improved raw signal versus immediate control: +0.0367R gross vs -0.0146R, hit 35.07% vs 32.55%.
- Frozen costs erased that edge: primary/stress -0.1625R / -0.3616R, zero positive-stress folds.
- Safe-lot portfolio: 593 trades, primary/stress expectancy -USD1.69 / -USD3.42, stress MDD USD2,065.82.
- Jul-Aug and Sep remain unopened.

- Opened EXP-029 / Engine M v0.3 after v0.2 established a small gross edge that failed costs.
- Preserved non-chasing 50% M5 limit entry, structural stop, T40, signal-first sizing, safety caps and costs.
- Added strict prior-4-M15 liquidity sweep/reclaim plus H1 midpoint reclaim.
- Added recent-two-H1 target-destination gate requiring T40 to point toward a completed H1 liquidity extreme.
- Frozen preflight at >=35 filled signals per market, both directions, >=400 total, zero outcomes.
- Frozen future development gross-edge requirement >+0.20R.

- Closed EXP-029 at zero-outcome preflight after only 106 filled signals; no P&L outcomes were calculated.
- Opened EXP-030 / Engine M v0.4 with a single prior-H1 range sweep/reclaim setup.
- Preserved non-chasing 50% M5 limit entry, structural stop, T40, signal-first sizing, safety caps and costs.
- Replaced rolling prior-4-M15 sweep + H1 midpoint conjunction with sweep/reclaim of the latest completed H1 boundary.
- Added opposite H1 boundary T40 room check.
- Frozen zero-outcome preflight at >=25 signals per market, both directions, >=300 total.

- Closed EXP-030 at zero-outcome preflight with 237 filled signals; no P&L outcomes were calculated.
- Opened EXP-031 / Engine M v0.5 with deterministic H1_0 -> H1_1 recent-range fallback.
- Kept the same >=300 total / >=25-per-market frequency gate rather than lowering it post hoc.
- Preserved non-chasing limit entry, structural stop, T40, sizing, safety and cost assumptions.

- EXP-031 recent-H1 zero-outcome preflight passed at `e0c7566`: 417 filled valid signals, all eight markets passing, both directions, all safely deployable.
- Kept the unchanged v0.4 frequency gate; no post-hoc threshold relaxation.
- v0.5 may proceed to development; Jul-Aug and Sep remain sealed.

- Frozen EXP-031 development runner before outcomes using audited target/portfolio machinery.
- Added separate H1_0/H1_1 cohort diagnostics without allowing post-outcome cohort selection.
- Preserved >+0.20R gross-edge gate and all post-cost economic gates.
- Jul-Aug and Sep remain sealed.

- Closed Engine M family after EXP-031 development failed: gross -0.0099R, primary -0.2063R, stress -0.4027R, 0/6 positive-stress folds.
- H1_1 fallback added frequency but reduced edge versus H1_0.
- Safe-account portfolio remained negative; Jul-Aug and Sep remain unopened.
- Preserved non-chasing execution as an architectural lesson; prohibited Engine M v0.6 minor-filter rescue.

- Closed Engine M family after EXP-031 development failure.
- Opened EXP-032 / Engine N v0.1 as a genuinely different session opening-drive continuation family.
- Frozen London 07:00 UTC and New York 13:30 UTC 30-minute opening drives.
- Added prior-eight-M15 volatility baseline, 1.50x expansion, 60% body and outer-25% close qualification.
- Preserved non-chasing execution via 50% pullback limit while removing H1 sweep/reclaim logic.
- Frozen zero-outcome preflight at >=25 signals per market, both directions, >=300 total.

- Closed EXP-032 at zero-outcome preflight after 123 filled signals; no P&L outcomes were calculated.
- Opened EXP-033 / Engine N v0.2 with continuous hourly scanning from 06:00 through 17:00 UTC.
- Kept the same >=300 total / >=25-per-market frequency gate.
- Preserved all drive qualification, pullback entry, stop, T40, sizing, safety and cost assumptions.
- Corrected the descriptive max-timestamp reporting bug in the new preflight runner.

- EXP-033 rolling-drive zero-outcome preflight passed at `2b8c781`: 626 filled signals, all eight markets passing, both directions.
- 624 signals were safely deployable; GE40 32 / GE30 474 / LT30 118.
- The unchanged opportunity-density gate passed without post-hoc relaxation.
- Jul-Aug and Sep remain sealed.

- Frozen EXP-033 development runner before outcomes after rolling scanner preflight PASS.
- Froze T40/stop-first outcome handling, 120-active-M1 maximum horizon, 20:00 UTC cutoff and matched immediate-entry control.
- Hourly-anchor cohorts are diagnostic only; no post-outcome hour whitelist is allowed.
- Jul-Aug and Sep remain sealed.

- Closed Engine N family after EXP-033 development failed: gross +0.0411R, primary -0.1450R, stress -0.3312R, 1/6 positive-stress folds.
- Continuous hourly scanning solved opportunity density but the opening-drive continuation thesis failed economics.
- Opened EXP-034 / Engine O v0.1 as a rolling statistical-stretch mean-reversion family.
- Frozen 24xM5 robust center/MAD baseline, 2.50-MAD stretch, 1.25x range expansion, 50% body, outer-35% rejection close, 50% limit entry and center-room T40 gate.
- Jul-Aug and Sep remain sealed.

- Closed EXP-034 at zero-outcome preflight with 209 filled signals; no P&L outcomes were calculated.
- Opened EXP-035 / Engine O v0.2 with continuous five-minute decision sampling from 06:05 through 17:55 UTC.
- Kept the same >=300 total / >=25-per-market opportunity-density gate.
- Preserved all statistical-stretch, rejection, 50% limit, stop, T40-to-center, safety and cost rules.
- Tightened v0.2-local synthetic and pending-order suppression verification before launch.

- EXP-035 continuous-M5 zero-outcome preflight passed with 574 filled/deployable signals across all eight markets.
- Frozen EXP-035 development runner before outcomes using audited target/portfolio machinery.
- Froze T40/trigger-stop outcome convention, 120-active-M1 maximum horizon, 20:00 UTC cutoff and matched immediate-entry control.
- Time-of-day diagnostics are descriptive only; no post-outcome hour/minute/symbol whitelist is allowed.
- Jul-Aug and Sep remain sealed.

- Closed Engine O family after EXP-035 development failed: gross -0.0719R, primary -0.2611R, stress -0.4504R, 0/6 positive-stress folds.
- Matched immediate-entry control was also negative, confirming the weakness was the isolated-symbol mean-reversion predictor rather than only the 50% entry.
- Preserved Jul-Aug and Sep.
- Next research family will use cross-market relative-strength information rather than another isolated-symbol pattern.

- Opened EXP-036 / Engine P v0.1 after closing Engine O.
- Added synchronized cross-market 30m normalized-momentum state and candidate-excluded USD factor confirmation.
- Added EURJPY EURUSD+USDJPY leg confirmation.
- Preserved continuous M5 scanning, non-chasing 50% entry, frozen T40 and reference-account safety caps.
- Kept the same >=300 total / >=25-per-market zero-outcome preflight gate.

- EXP-036 cross-market zero-outcome preflight passed with 6,063 filled signals across all eight markets.
- Frozen EXP-036 development runner before outcomes using audited target/portfolio machinery.
- Froze T40/trigger-stop outcome convention, 120-active-M1 maximum horizon, 20:00 UTC cutoff and matched immediate-entry control.
- Cross-market factor/time/market diagnostics are descriptive only; no post-outcome threshold or whitelist rescue is allowed.
- Jul-Aug and Sep remain sealed.

- Closed Engine P v0.1 / EXP-036 after frozen development failed at durable result commit `52e9003f351eb7f5abdf9b38f74c279c88d33906`.
- Development: 4,804 signals; gross -0.04065R; primary -0.23568R; stress -0.43072R; 0/6 positive-stress folds.
- Reference-account: 836 trades; primary/stress expectancy -USD2.02 / -USD4.15; primary/stress PF 0.761 / 0.580; stress MDD USD3,526.25.
- Durable result confirms Jul-Aug and Sep remained sealed.
- Prohibited post-hoc MOM/USD_SCORE/hour/symbol/direction rescue; next engine must use a genuinely different prospectively frozen information source/family.

- Opened EXP-037 / Engine Q v0.1 after closing Engine P.
- Changed information source from directional factor consensus to directionless cross-market volatility-spillover breadth.
- Frozen candidate-self exclusion, >=4 peer shocks at VR>=1.75, candidate lag VR<=1.00 inside a fixed six-M5 box, first breakout within six M5 bars, breakout VR>=1.25/body>=50%/outer-25% close, 50% retracement limit and structural stop.
- Frozen same six Apr13-Jun30 development slices, Jun30 hard source seal, T40, 10%/20% target-cost stresses and unchanged USD500 safe-lot caps.
- Jul-Aug and Sep remain sealed; Engine-Q outcomes are zero at freeze.

- Implemented Engine Q v0.1 and EXP-037 zero-outcome preflight/workflow before any outcomes.
- Frozen implementation checkpoint at main SHA `c51c8f9566a6ccfddaf8117c2b0a80c45fbeb10b`; engine/runner/workflow commits `9a2a2c7` / `2bfb0c5` / `c51c8f9`.
- Protected Jul-Aug and Sep remain sealed; next computation is one zero-outcome EXP-037 preflight only.

- Closed Engine Q v0.1 / EXP-037 at zero-outcome preflight result `b05efb3`: only 56 filled signals, all safely deployable, but all eight markets and total >=300 frequency gates failed.
- No target/P&L outcomes were calculated; Jun30 hard source seal held and Jul-Aug/Sep remained unopened.
- Same-bar >=4-peer VR>=1.75 synchronization was identified as the dominant frequency bottleneck.
- Frequency gate remains unchanged; any next version must redesign peer-shock sampling prospectively rather than lower the gate.

- Opened EXP-038 / Engine Q v0.2 after v0.1 failed only zero-outcome frequency.
- Preserved peer shock VR>=1.75 and >=4 unique-peer breadth; changed same-bar synchronization to causal rolling 15-minute peer-shock memory across t/t-5/t-10.
- Candidate lag, breakout, 50% retracement entry, structural stop, T40, 10%/20% costs, USD500 safety caps and preflight/development gates remain unchanged.
- Jun30 hard source seal preserved; Jul-Aug and Sep remain sealed; v0.2 outcomes zero at freeze.

- Implemented Engine Q v0.2 rolling peer-shock memory plus EXP-038 zero-outcome preflight/workflow.
- Frozen implementation checkpoint at main SHA `850fe44fa426b2ee4f235d3af140fa981ff26ae2` before any target/P&L outcome.
- Jul-Aug and Sep remain sealed; next computation is exactly one EXP-038 preflight.

- EXP-038 Engine Q v0.2 zero-outcome preflight passed at `3d9ca37`: 467 filled signals, all eight markets >=25 with both directions, 466 safely deployable.
- Rolling 15-minute peer-shock memory solved v0.1's opportunity-density failure without lowering VR>=1.75, four-peer breadth, or the frequency gate.
- Target/P&L outcomes remain zero; Jun30 source seal held and Jul-Aug/Sep remain unopened.
- Next permitted stage is frozen six-slice development only.

- Frozen EXP-038 Engine Q v0.2 six-slice development runner/workflow before outcomes.
- Development fold membership and matched immediate control are keyed to breakout completion time, the first directional candidate decision.
- Preserved T40/stop-first/120-active-M1/20:00 UTC outcome convention, >+0.20R gross hurdle, all post-cost gates and protected-period seals.
- Jul-Aug and Sep remain sealed at launch checkpoint.

- Closed Engine Q v0.2 / EXP-038 after frozen development failed at `6f25b08`: 363 signals, gross +0.09479R, primary -0.09022R, stress -0.27524R, 1/6 positive-stress folds.
- Reference-account: 251 trades; primary/stress expectancy -USD1.53 / -USD3.89; PF 0.836 / 0.640; stress MDD USD1,102.23.
- Matched immediate entry was worse, preserving non-chasing entry as an architectural lesson but not validating the spillover predictor.
- Prohibited post-hoc peer-shock/lag/trigger/time/market/direction rescue; Jul-Aug and Sep remain sealed.

- Opened EXP-039 / Engine R v0.1 after closing Engine Q.
- Changed information source to dynamic candidate-peer co-movement and normalized relative-value residual displacement.
- Frozen prior-48 Pearson peer selection, |rho|>=0.60, peer |NM15|>=1.00, |residual|>=1.50, same-bar rejection confirmation, 50% limit, structural stop and T40.
- Preserved Jun30 hard source seal, 10%/20% costs, USD500 safety caps and unchanged preflight/development gates.
- Jul-Aug and Sep remain sealed; Engine-R outcomes are zero at freeze.

- Implemented Engine R v0.1 dynamic peer-residual mechanics and EXP-039 zero-outcome preflight/workflow before outcomes.
- Frozen implementation checkpoint at main SHA `db879da22f4ec6ab3a7ca497f110f847b7ff373f`.
- Protected Jul-Aug and Sep remain sealed; next computation is exactly one EXP-039 preflight.

- Added `research/ROOT-CAUSE-EDGE-SOURCE-AUDIT-v0.1.md` at `b170bef2` and paused the strategy-family iteration loop.
- Root cause: repeated recent engines mostly transform OHLC state and do not clear the raw-edge hurdle required to survive costs; Q demonstrated that non-chasing execution helps but is insufficient by itself.
- Added research priority for microstructure/order flow, macro surprise, rates/cross-asset context, execution-grade spread/tick data, and target-ladder path modeling before another outcome engine.
- Recorded the economic constraint that USD150-200 on USD500 is a 30%-40% daily return; per-trade risk will not be increased merely to force the objective before stable post-cost edge exists.
- Engine R / EXP-039 paused before development during the audit; Jul-Aug and Sep remain sealed.

- Added `research/ECONOMIC-FEASIBILITY-FRONTIER-v0.1.md` (`73e75b5`) with exact simplified daily-state arithmetic under current cost/loss-gate conventions.
- Added `research/EDGE-SOURCE-RESEARCH-MATRIX-v0.1.md` (`fac6c1b`) prioritizing Gold/FX macro + microstructure/order-flow + rates/execution data over another OHLC-only family.
- Confirmed that risk scaling is deferred until positive post-cost edge exists; Engine R remains paused before development and protected periods remain sealed.

- Added governing `docs/BRAINSTORMING-AND-KNOWLEDGE-CAPTURE-POLICY.md` so material brainstorming is durably synthesized into the repository.
- Added `research/BRAINSTORMING-SYNTHESIS-2026-09-25.md` covering information advantage, human multi-timeframe process, specialization, lot-size caution, compounding, target ladder, non-chasing execution and meta-overfitting lessons.
- Frozen EXP-040 Multi-Timeframe Structural Context Information-Content Study plus source manifest.
- Implemented nested LOCAL_M5 / +15M / +1H / +4H-prior-day / +session feature sets, structural-risk target ladder, six purged chronological folds and fixed logistic+Platt comparison.
- Frozen EXP-040 implementation at workflow SHA `d5e41a0`; no protected-period data authorized and Engine R remains paused.

- Recorded EXP-040 run `36135418584` as an operational GitHub Actions startup block after two attempts failed before any step/log/result existed.
- Explicitly preserved frozen EXP-040 research mechanics; no scientific conclusion or protected-period computation occurred.

- EXP-040 completed at durable result `46049f7` after correcting a non-scientific integrity-boolean implementation issue and rerunning the unchanged frozen study.
- 123,724 development candidates; 99,622 pooled evaluation predictions per primary rung; integrity passed; Jun30 source seal held; Jul-Aug/Sep remained sealed.
- No MTF context set (+15M / +1H / +4H-prior-day / +session) passed the frozen T40eq/T50eq incremental-information gate versus LOCAL_M5.
- Scientific disposition: `NO_STABLE_MTF_INFORMATION_ADVANTAGE`.
- Next research family is macro/catalyst information content, not another MTF-OHLC strategy.

- Added `research/HUMAN-TRADER-EDGE-DECOMPOSITION-v0.1.md`, formalizing the expert-trader research sequence and anti-loop rule.
- Frozen EXP-041 macro/catalyst information-content study with a data-adequacy gate before any outcome model.
- Added EXP-041 data-adequacy audit: current source has only 17 independent primary macro blocks, so disposition is `DATA_INSUFFICIENT_EXTEND_EARLIER_HISTORY` rather than fitting a pseudo-replicated model.
- Added a 17-event macro plumbing seed, explicitly not valid for final promotion.
- Frozen a separate twelve-month Dukascopy M1 development feed (Jul2025-Jun2026) with hash/coverage/cross-feed audit and no labels/P&L; added downloader, audit runner and CI workflow.
- Jul-Aug/Sep 2026 remain sealed; Engine R remains paused.

- EXP-041 extended-history run `36153466140` downloaded all eight 12-month Dukascopy feeds successfully but failed before audit output because the audit imported a modeling module that required missing `joblib`.
- Fixed the audit operational dependency at `105eb2e` by using a local overlap-only parser; no frozen data range, source, integrity threshold or scientific rule changed.
- No labels/P&L/protected-period computation occurred in the failed attempt.

- EXP-041 extended-market-history audit produced durable result `1cf168d`: acquisition integrity largely passed, but the frozen cross-feed sanity gate failed for 7/8 markets; USDCHF also ended one day early.
- Market-history gate remains FAIL. No macro model, target labels or P&L were run.
- Next action changed to a zero-outcome cross-feed diagnostic before any acquisition-v0.2 redesign; frozen v0.1 thresholds will not be relaxed post hoc.

- EXP-041 cross-feed diagnostic completed successfully at `bdd3b7f`: zero lag is best for all markets, so timezone alignment does not explain the feed disagreement.
- All eight markets classified `MATERIAL_PATH_MISMATCH`; USDCHF also has a source-coverage gap.
- No thresholds were relaxed. Next step is prospectively frozen three-feed adjudication before any macro outcome modeling.

- EXP-041 third-source feed adjudication completed successfully at durable result `3e5ed20`.
- Frozen feed-selection gate failed: CURRENT_PINNED 2/8 supported markets, DUKASCOPY 2/8, HISTDATA 0/8; six markets had no two-source consensus and no source was eligible.
- XAUUSD and USDCAD were the only passing CURRENT_PINNED↔Dukascopy pairs; HistData was the outlier there.
- No target labels/P&L/protected-period data were used.
- No feed was selected and no threshold was relaxed.
- Authorized one zero-outcome HistData timestamp-semantics diagnostic before moving to an intended-broker/institutional fourth source, because HistData's daily-vs-intraday correlation pattern may indicate a common mechanical timestamp issue.

- Frozen EXP-041 HistData timestamp-semantics diagnostic at main SHA `2791376846eff374c708f0346da29432ab77f1bd`.
- Added a zero-outcome common whole-hour shift test (-6h..+6h) that replays the original third-source pairwise/feed-selection gates unchanged.
- Prohibited per-market shift fitting and preserved Jul-Aug/Sep protection.
- Next step is one workflow run only; failure to restore the frozen gate requires a fourth/intended-broker source.



- EXP-041 HistData timestamp-semantics diagnostic completed at durable result `f98eba5`; no common -6h..+6h shift restored the frozen three-feed selection gate, so HistData remediation is closed.
- Added `research/EXP-041-DATA-SOURCE-GOVERNANCE-v0.2.md`: prospectively adopts Dukascopy as the canonical EXP-041 development price feed without pretending the earlier consensus gate passed.
- Frozen exact normalized SHA-256 values from audit `1cf168d`; future EXP-041 development data will be an immutable GitHub Release snapshot rather than repeated live downloads.
- Added snapshot verifier and snapshot workflow; common eight-market modeling cutoff is 2026-06-30 00:00 UTC because USDCHF ends Jun29 23:59.
- Broker/institutional execution-feed validation remains required before deployment; Jul-Aug/Sep remain sealed and no strategy outcomes were computed.


- Recorded EXP-041 canonical Dukascopy snapshot attempt 1 trigger `0e685e1` as a red Actions check with no durable result; this is not yet a scientific/data-drift conclusion.
- Hardened the snapshot verifier/workflow at `a20206c` / `3aaed83`: failed hash reproduction is now durably checkpointed, and run-specific metadata was removed from the archive-internal manifest so identical data yield a deterministic archive.
- Frozen data hashes/date boundaries/protected-period rules were unchanged.


- EXP-041 snapshot v1 retrigger produced durable result `2dc6a9c` from run `36264975005`: all eight live Dukascopy files differed from Sep25 hashes/row counts; release creation was skipped and final integrity failed closed.
- The failure does not yet distinguish upstream history revision from acquisition nondeterminism.
- Frozen `EXP-041-DUKASCOPY-REPEATABILITY-SNAPSHOT-RECOVERY-v0.1` with two independent same-run downloads, exact byte/hash equality, and integrity checks across all eight markets.
- If repeatable, the same workflow freezes the current copy as immutable snapshot v2; if not, no release is created and acquisition engineering becomes the blocker.
- No labels/P&L/protected-period data are involved.
