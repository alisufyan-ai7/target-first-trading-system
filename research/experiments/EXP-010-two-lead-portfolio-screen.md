# EXP-010 — Two-Lead Portfolio Daily-Distribution Screen

**Status:** COMPLETE — COMBINATION DOES NOT SOLVE DAILY-DISTRIBUTION OR ECONOMIC-FEASIBILITY OBJECTIVE  
**Date:** 2026-09-22

## Purpose

Test whether the two existing, structurally independent research leads materially improve the project-level daily P&L distribution when combined without changing either strategy.

## Frozen input leads

1. **USDJPY / Engine A v0.2**
   - exact rules from `strategies/engine-a-liquidity-mss-fvg/SPEC-v0.2-portable.md`;
   - research-lead status from EXP-007.

2. **GBPUSD / Engine F v0.1**
   - exact rules from `strategies/engine-f-statistical-mean-reversion/SPEC-v0.1-portable.md`;
   - research-lead status from EXP-009.

No signal, stop, target, session, or sizing parameter was changed in EXP-010.

## Data and split

Same provisional GetData one-minute feed and common split:

- development: 2026-03-12 through 2026-05-31;
- holdout: 2026-06-01 through 2026-08-20.

This is a same-feed portfolio screen, not independent validation.

## Stream reconstruction check

### USDJPY / Engine A

The reconstruction was checked against EXP-007 before combination.

Recorded EXP-007 full-window funnel:

- sweeps: 2,037;
- MSS + displacement: 557;
- FVG: 416;
- raw fills: 262;
- accepted trades: 209;
- development trades: 112;
- holdout trades: 97.

EXP-010 reconstruction:

- sweeps: 2,037;
- MSS + displacement: 560;
- FVG: 418;
- raw fills: 263;
- accepted trades: 208;
- development trades: 111;
- holdout trades: 97.

The holdout reconstruction reproduces the recorded lead essentially exactly on the key statistics, including approximately +0.263R/trade, 7.22% timeouts, 3.65-pip median stop, and about 177.8x median notional/equity.

There is a one-trade development discrepancy. It is retained transparently rather than forcing the reconstruction to fit. The discrepancy is small enough for this portfolio-distribution screen, but any later execution-grade work must use a persisted trade ledger/test implementation rather than reconstructed chat logic.

### GBPUSD / Engine F

The EXP-009 implementation is reproduced exactly:

- full-window accepted trades: 75;
- development: 40;
- holdout: 35.

## Frozen portfolio state machine

Reference equity: USD 500.

Per accepted trade:

- gross stop risk: USD 20;
- target: USD 50 / +2.5R.

Controls:

1. maximum 4 new entries/day;
2. maximum 2 simultaneously open positions;
3. stop new entries after realized daily P&L <= -USD 40;
4. stop new entries after realized daily P&L >= +USD 150;
5. pre-existing open positions finish under original exits;
6. deterministic same-time priority: Engine A before Engine F;
7. rejected precomputed trades do not reactivate alternative suppressed signals.

## Development result

Standalone relationship:

- eligible weekdays: 57;
- Engine A candidate trades: 111;
- Engine F candidate trades: 40;
- daily P&L correlation: +0.143;
- weekdays with trades from both leads: 52.63%.

Portfolio:

- candidate trades: 151;
- accepted trades: 115;
- trades/day including zero days: 2.02;
- zero-trade days: 5.26%;
- mean daily P&L: +USD 0.65;
- median daily P&L: -USD 40;
- losing days: 59.65%;
- <= USD 50 days: 84.21%;
- >= USD 100 days: 10.53%;
- >= USD 150 days: 5.26%;
- maximum daily loss: -USD 60;
- maximum drawdown: about USD 350;
- maximum consecutive losing days: 7;
- maximum consecutive <= USD 50 days: 11;
- total simulated P&L: about +USD 37.03;
- maximum simultaneous notional/equity: about 716.6x.

Rejections:

- open-position cap: 0;
- 4-entry daily cap: 4;
- daily loss stop: 30;
- daily profit stop: 2.

Contribution:

- Engine A: 84 accepted trades, about -USD 182.97;
- Engine F: 31 accepted trades, +USD 220.

## Holdout result

Standalone relationship:

- eligible weekdays: 59;
- Engine A candidate trades: 97;
- Engine F candidate trades: 35;
- daily P&L correlation: +0.031;
- weekdays with trades from both leads: 35.59%.

The near-zero correlation confirms that the streams are meaningfully independent at the daily P&L level.

Portfolio:

- candidate trades: 132;
- accepted trades: 114;
- trades/day including zero days: 1.93;
- zero-trade days: 3.39%;
- mean daily P&L: +USD 10.51;
- median daily P&L: +USD 10;
- losing days: 44.07%;
- <= USD 50 days: 86.44%;
- >= USD 100 days: 6.78%;
- >= USD 150 days: 0%;
- maximum daily loss: -USD 40;
- maximum drawdown: about USD 200.53;
- maximum consecutive losing days: 7;
- maximum consecutive <= USD 50 days: 14;
- total simulated P&L: about +USD 619.92;
- maximum simultaneous notional/equity: about 1,285.4x.

Rejections:

- open-position cap: 0;
- 4-entry daily cap: 2;
- daily loss stop: 16;
- daily profit stop: 0.

Contribution:

- Engine A: 84 accepted trades, about +USD 589.92;
- Engine F: 30 accepted trades, about +USD 30.

## Interpretation

The two leads are genuinely independent, but independence alone does not solve the objective.

Important findings:

1. holdout <= USD 50 days remain 86.44%, versus the project preference near 20%;
2. there are no >= USD 150 holdout days;
3. losing days remain 44.07%;
4. maximum holdout drawdown is roughly 40% of the USD 500 reference equity;
5. the portfolio's positive holdout P&L is overwhelmingly attributable to USDJPY / Engine A rather than balanced contribution;
6. the Engine F contribution is small;
7. fixed USD 20 risk with very small structural stops creates extreme notional exposure, with a maximum simultaneous notional/equity reading above 1,200x.

The loss state machine successfully limits the worst observed holdout day to -USD 40, but it cannot manufacture high-output days from low hit rates and limited qualified opportunity.

## Conclusion

**Do not promote the two-lead portfolio.**

Do not tune either retained lead to rescue the portfolio distribution.

The project has now demonstrated:

- more XAU signals are not sufficient;
- more markets are not sufficient;
- two low-correlated positive-expectancy research leads are still not sufficient under the current USD 20 risk / USD 50 target / 3–4 trade daily framework.

## Next action

Before spending more effort inventing strategy filters, quantify the **mathematical feasibility frontier** of the daily-distribution objective under the current payoff and trade-count constraints.

Specifically determine the target-first win probability and opportunity frequency required to make <= USD 50 days approach 20% when only 1–4 trades/day are allowed.

Use that feasibility result to decide whether the next phase should:

- search for another independent engine;
- change the payoff/risk unit;
- change the daily distribution objective;
- or change the reference account/economic assumptions.

Any such change requires an explicit project decision; do not silently move the goalposts.
