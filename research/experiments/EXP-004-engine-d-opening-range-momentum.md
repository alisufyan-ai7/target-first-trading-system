# EXP-004 — Engine D Session / Opening-Range Momentum

**Status:** CURRENT FORMULATIONS NOT PROMOTED  
**Date:** 2026-09-22

## Question

Can a session/opening-range momentum strategy provide an independent stream of XAUUSD opportunities with enough frequency and USD 5 target-first quality to improve daily consistency?

## Dataset

Same baseline as EXP-002:

- XAUUSD 1-minute Dukascopy data;
- 2026-03-01 through 2026-08-20;
- approximately 230,813 one-minute bars;
- March–May development;
- June–August 20 holdout;
- no broker-specific spread/commission/slippage.

## Strategy family

Two fixed UTC opening ranges were screened:

- London-oriented range: 06:00–07:00 UTC, breakout window after 07:00;
- New-York-oriented range: 12:30–13:30 UTC, breakout window after 13:30.

Core logic:

1. define opening range;
2. require breakout close beyond the range;
3. optionally require strong breakout candle body;
4. enter at breakout close;
5. stop just back inside the broken range, subject to max-risk cap;
6. evaluate USD 5 favorable target before stop;
7. maximum one trade per session/day.

## Results

### D1 balanced

Development:

- trades: 39;
- USD 5 target-first: 41.0%;
- average simplified price P&L: +0.74 XAU/trade;
- average risk distance: 2.25 XAU;
- average daily P&L under exploratory 0.10-lot-style simulator: about +USD 4.42;
- zero-trade days: 52.3%;
- <= USD 50 days: 96.9%.

Holdout:

- trades: 44;
- USD 5 target-first: 31.8%;
- average simplified price P&L: +0.23 XAU/trade;
- average risk distance: 1.98 XAU;
- average daily P&L: about +USD 1.69;
- zero-trade days: 35.6%;
- <= USD 50 days: 98.3%.

### D2 strict

Development:

- trades: 10;
- target-first: 30.0%;
- average simplified price P&L: +0.02 XAU/trade.

Holdout:

- trades: 14;
- target-first: 57.1%;
- average simplified price P&L: +2.00 XAU/trade.

Interpretation: holdout result is attractive but the sample is extremely small and development was essentially flat. This is insufficient evidence and likely regime-sensitive.

### D3 loose

Development:

- trades: 68;
- target-first: 33.8%;
- average simplified price P&L: +0.33 XAU/trade.

Holdout:

- trades: 70;
- target-first: 21.4%;
- average simplified price P&L: -0.42 XAU/trade;
- average daily P&L: about -USD 4.96;
- losing days: 59.3%.

Loosening the setup increased frequency but destroyed holdout quality.

### D4 NY-only

Development:

- trades: 14;
- target-first: 50.0%;
- average simplified price P&L: +1.30 XAU/trade.

Holdout:

- trades: 13;
- target-first: 15.4%;
- average simplified price P&L: -1.08 XAU/trade.

The apparent development strength did not generalize.

## Conclusion

The current Engine D formulations are **not promoted**.

Important evidence:

- increasing frequency by loosening the rules worsened holdout expectancy;
- the only attractive holdout result was based on a very small sample and did not have matching development strength;
- daily-output metrics remain nowhere near the project objective.

## Next action

Proceed to Engine E: volatility compression -> expansion.

Do not tune Engine D further at this stage.
