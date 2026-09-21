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
