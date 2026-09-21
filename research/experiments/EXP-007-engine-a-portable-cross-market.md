# EXP-007 — Engine A v0.2 Portable Cross-Market Screen

**Status:** IN PROGRESS — RULES FROZEN BEFORE OUTCOME INSPECTION  
**Date:** 2026-09-22

## Question

Does a fully mechanical, portable Engine A variant retain positive target-first expectancy when applied unchanged to XAUUSD, EURUSD, GBPUSD, and USDJPY?

## Hypothesis

If Engine A captures a transferable liquidity-sweep / structure-shift mechanism rather than XAU-specific noise, at least one non-Gold market should show non-negative or positive holdout expectancy under unchanged rules.

The experiment is also allowed to falsify transferability.

## Strategy

Frozen specification:

- `strategies/engine-a-liquidity-mss-fvg/SPEC-v0.2-portable.md`.

No parameter may be changed after holdout outcomes are inspected.

## Data

External public one-minute GetData samples identified in EXP-006.

Common test window:

- development: 2026-03-12 through 2026-05-31;
- holdout: 2026-06-01 through 2026-08-20.

Instruments:

- XAUUSD;
- EURUSD;
- GBPUSD;
- USDJPY.

## Economics

- structural stop first;
- USD 20 gross risk at stop;
- USD 50 gross target;
- target distance = 2.5R;
- no martingale;
- no size increase after losses;
- no broker-specific costs in this first transferability screen;
- notional/equity diagnostics must be reported.

## Separation rule

Development and holdout results must be reported separately.

No strategy parameter changes are permitted after holdout inspection.

## Promotion rule

A market is not promoted merely because it has a positive total P&L.

To remain a candidate it should show, on holdout:

- non-negative/positive mean R;
- enough observations to be interpretable;
- no obvious collapse from development;
- daily distribution materially useful relative to prior XAU-only screens;
- economic feasibility not obviously incompatible with the USD 500 reference account.

Any positive result remains provisional until costs and an independent feed are tested.

## Next action

Run the frozen rules market by market in small checkpoints. Record each market result before any portfolio combination.


## Implementation notes

The first implementation checkpoint uses the frozen v0.2 rules exactly as specified.

Additional deterministic execution details:

- the active setup/entry window is enforced so a sweep must complete before 18:00 UTC and a retracement fill must occur before 18:00 UTC;
- the 2-left/2-right pivot is not eligible until its two right-side bars have completed;
- if several eligible pivots exist, the most recent confirmed pivot within the frozen age window is used;
- the first qualifying same-direction FVG is used;
- retracement entry begins only after the FVG-confirming candle has completed;
- the one-open-trade rule is applied chronologically: a new candidate whose sweep or fill occurs while an existing Engine A trade is open is ignored;
- all UTC weekdays in each split are included in daily-distribution statistics, including zero-signal days;
- raw funnel counts below are for the full common test window unless otherwise stated.

## Market checkpoint 1 — XAUUSD

**Status:** PORTABLE v0.2 XAU ARM REJECTED UNDER THE 2.5R ECONOMIC RULE

### Full-window signal funnel

- eligible 5m sweep events examined: 2,394;
- sweep events reaching valid MSS + displacement: 678;
- events reaching a qualifying FVG: 496;
- raw retracement fills before one-open filtering: 296;
- accepted trades after one-open filtering: 231.

### Development — 2026-03-12 through 2026-05-31

- eligible weekdays: 57;
- trades: 98;
- trades/day including zero-signal weekdays: 1.72;
- 2.5R target-first win rate: 23.47%;
- mean R/trade: -0.163R;
- median R/trade: -1.00R;
- timeout rate: 1.02%;
- median structural stop distance: USD 6.95/oz;
- median position size at USD 20 structural risk: 2.88 oz;
- median notional/equity ratio: 27.0x;
- legacy fixed-USD-5 favorable-move-before-stop diagnostic: 53.06%;
- mean daily P&L under fixed USD 20 risk: -USD 5.60;
- losing days: 50.88%;
- <= USD 50 days: 91.23%;
- >= USD 100 days: 5.26%;
- >= USD 150 days: 1.75%;
- maximum drawdown: approximately USD 789.42;
- maximum consecutive losing days: 8;
- maximum consecutive <= USD 50 days: 32;
- total simulated P&L: approximately -USD 319.42.

### Holdout — 2026-06-01 through 2026-08-20

- eligible weekdays: 59;
- trades: 133;
- trades/day including zero-signal weekdays: 2.25;
- 2.5R target-first win rate: 18.80%;
- mean R/trade: -0.305R;
- median R/trade: -1.00R;
- timeout rate: 2.26%;
- median structural stop distance: USD 5.19/oz;
- median position size at USD 20 structural risk: 3.85 oz;
- median notional/equity ratio: 32.6x;
- legacy fixed-USD-5 favorable-move-before-stop diagnostic: 35.34%;
- mean daily P&L under fixed USD 20 risk: -USD 13.77;
- losing days: 66.10%;
- <= USD 50 days: 96.61%;
- >= USD 100 days: 0%;
- >= USD 150 days: 0%;
- maximum drawdown: approximately USD 852.27;
- maximum consecutive losing days: 7;
- maximum consecutive <= USD 50 days: 24;
- total simulated P&L: approximately -USD 812.27.

### Interpretation

The frozen portable version fails on XAUUSD under the USD 20 risk / USD 50 target rule.

For a simple -1R / +2.5R binary payoff, the no-cost break-even win rate is about 28.57%. The observed 18.80% holdout target-first rate is materially below that threshold, and measured mean R is negative.

The legacy USD 5 diagnostic is **not directly comparable** with EXP-002 because this experiment uses a different public feed, a newly frozen fully mechanical implementation, and a shorter common window.

The large fixed-risk drawdown relative to the USD 500 reference equity also independently fails the project's risk objective.

### Disposition

- Do not promote Engine A v0.2 on XAUUSD.
- Do not alter the frozen rules to rescue the XAU result.
- Continue the same unchanged rules on EURUSD, GBPUSD, and USDJPY solely to test cross-market transferability.


## Market checkpoint 2 — EURUSD

**Status:** NOT PROMOTED

### Full-window signal funnel

- eligible 5m sweep events examined: 2,057;
- sweep events reaching valid MSS + displacement: 609;
- events reaching a qualifying FVG: 483;
- raw retracement fills before one-open filtering: 285;
- accepted trades after one-open filtering: 227.

### Development — 2026-03-12 through 2026-05-31

- eligible weekdays: 57;
- trades: 115;
- trades/day including zero-signal weekdays: 2.02;
- 2.5R target-first win rate: 23.48%;
- mean R/trade: -0.109R;
- median R/trade: -1.00R;
- timeout rate: 3.48%;
- median structural stop distance: 0.0004500 = 4.50 pips;
- median base-unit position size at USD 20 structural risk: 44,444 EUR;
- median notional/equity ratio: 105.2x;
- mean daily P&L under fixed USD 20 risk: -USD 4.38;
- losing days: 52.63%;
- <= USD 50 days: 96.49%;
- >= USD 100 days: 1.75%;
- >= USD 150 days: 0%;
- maximum drawdown: approximately USD 339.30;
- maximum consecutive losing days: 6;
- maximum consecutive <= USD 50 days: 34;
- total simulated P&L: approximately -USD 249.76.

### Holdout — 2026-06-01 through 2026-08-20

- eligible weekdays: 59;
- trades: 112;
- trades/day including zero-signal weekdays: 1.90;
- 2.5R target-first win rate: 31.25%;
- mean R/trade: +0.167R;
- median R/trade: -1.00R;
- timeout rate: 5.36%;
- median structural stop distance: 0.0003350 = 3.35 pips;
- median base-unit position size at USD 20 structural risk: 59,701 EUR;
- median notional/equity ratio: 139.0x;
- mean daily P&L under fixed USD 20 risk: +USD 6.35;
- losing days: 40.68%;
- <= USD 50 days: 88.14%;
- >= USD 100 days: 6.78%;
- >= USD 150 days: 0%;
- maximum drawdown: USD 240.00;
- maximum consecutive losing days: 4;
- maximum consecutive <= USD 50 days: 17;
- total simulated P&L: approximately +USD 374.36.

### Interpretation

EURUSD is the first non-Gold market to show positive holdout mean R under the frozen rules, and its 31.25% holdout target-first rate is above the simple no-cost 28.57% break-even rate for a -1R/+2.5R payoff.

However, it is **not promoted** because:

1. development expectancy was negative at -0.109R/trade, so robustness across the split is not established;
2. 88.14% of holdout weekdays still finished at <= USD 50, far from the project objective;
3. the median USD-20-risk position implies roughly 139x notional/equity on the USD 500 reference account before broker margin/cost constraints;
4. costs have not yet been included, and 3–5 pip structural stops are especially sensitive to spread/slippage.

### Disposition

- Do not promote EURUSD Engine A v0.2.
- Do not tune the rules to preserve the positive holdout result.
- Continue unchanged to GBPUSD and USDJPY to complete the transferability test.


## Market checkpoint 3 — GBPUSD

**Status:** NOT PROMOTED

### Full-window signal funnel

- eligible 5m sweep events examined: 2,139;
- sweep events reaching valid MSS + displacement: 599;
- events reaching a qualifying FVG: 459;
- raw retracement fills before one-open filtering: 280;
- accepted trades after one-open filtering: 224.

### Development — 2026-03-12 through 2026-05-31

- eligible weekdays: 57;
- trades: 109;
- trades/day including zero-signal weekdays: 1.91;
- 2.5R target-first win rate: 30.28%;
- mean R/trade: +0.139R;
- median R/trade: -1.00R;
- timeout rate: 3.67%;
- median structural stop distance: 0.0005750 = 5.75 pips;
- median base-unit position size at USD 20 structural risk: 34,783 GBP;
- median notional/equity ratio: 94.8x;
- mean daily P&L under fixed USD 20 risk: +USD 5.30;
- losing days: 42.11%;
- <= USD 50 days: 91.23%;
- >= USD 100 days: 1.75%;
- >= USD 150 days: 0%;
- maximum drawdown: approximately USD 136.79;
- maximum consecutive losing days: 4;
- maximum consecutive <= USD 50 days: 17;
- total simulated P&L: approximately +USD 302.20.

### Holdout — 2026-06-01 through 2026-08-20

- eligible weekdays: 59;
- trades: 115;
- trades/day including zero-signal weekdays: 1.95;
- 2.5R target-first win rate: 24.35%;
- mean R/trade: -0.111R;
- median R/trade: -1.00R;
- timeout rate: 2.61%;
- median structural stop distance: 0.0004500 = 4.50 pips;
- median base-unit position size at USD 20 structural risk: 44,444 GBP;
- median notional/equity ratio: 118.1x;
- mean daily P&L under fixed USD 20 risk: -USD 4.34;
- losing days: 50.85%;
- <= USD 50 days: 94.92%;
- >= USD 100 days: 3.39%;
- >= USD 150 days: 0%;
- maximum drawdown: approximately USD 585.50;
- maximum consecutive losing days: 4;
- maximum consecutive <= USD 50 days: 41;
- total simulated P&L: approximately -USD 256.22.

### Interpretation

GBPUSD does not generalize across the split. Development was positive, but holdout target-first rate fell below the simple no-cost 28.57% break-even level and mean R turned negative.

The daily-distribution objective also remains far away, and the fixed-risk sizing implies very large notional exposure relative to the USD 500 reference equity.

### Disposition

- Do not promote GBPUSD Engine A v0.2.
- Do not retune after the holdout deterioration.
- Continue unchanged to USDJPY to complete EXP-007.
