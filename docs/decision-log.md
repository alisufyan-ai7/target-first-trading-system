# Decision Log

## 2026-09-22 — Context isolation

**Decision:** Only the originating chat and `alisufyan-ai7/owner-target-first-trading-research` may be used as durable project context.

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
