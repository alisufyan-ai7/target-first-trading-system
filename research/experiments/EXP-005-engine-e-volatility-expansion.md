# EXP-005 — Engine E Volatility Compression -> Expansion

**Status:** CURRENT FORMULATIONS NOT PROMOTED  
**Date:** 2026-09-22

## Question

Can volatility compression followed by directional expansion provide an independent, sufficiently frequent XAUUSD opportunity stream with better USD 5 target-first behavior?

## Dataset

Same Phase-1 baseline as EXP-002 and EXP-004:

- XAUUSD 1-minute Dukascopy data;
- 2026-03-01 through 2026-08-20;
- approximately 230,813 one-minute bars;
- March–May development;
- June–August 20 holdout;
- no broker-specific spread/commission/slippage.

## Strategy family

Core concept:

1. detect a low-volatility 5m compression window;
2. compare recent true range against a longer baseline;
3. optionally restrict total compression-range width relative to ATR;
4. require a directional breakout close;
5. require breakout candle expansion/body strength;
6. enter at breakout close;
7. use a breakout-failure / range-boundary stop;
8. evaluate fixed USD 5 favorable target before stop.

## Results

### E1 balanced

Development:

- trades: 19;
- target-first: 36.8%;
- average simplified price P&L: +0.73 XAU/trade;
- average risk: 1.80 XAU;
- median favorable excursion: 3.14 XAU.

Holdout:

- trades: 25;
- target-first: 24.0%;
- average simplified price P&L: -0.08 XAU/trade;
- average risk: 1.71 XAU;
- median favorable excursion: 2.07 XAU;
- zero-trade days: 64.4%;
- <= USD 50 days: 100%.

### E2 strict

Development:

- trades: 4;
- target-first: 25.0%;
- average simplified price P&L: +0.04 XAU/trade.

Holdout:

- trades: 6;
- target-first: 50.0%;
- average simplified price P&L: +1.65 XAU/trade.

Interpretation: too few observations for meaningful promotion.

### E3 loose

Development:

- trades: 135;
- target-first: 25.9%;
- average simplified price P&L: +0.02 XAU/trade;
- exploratory trades/day: 1.91;
- <= USD 50 days: 89.2%.

Holdout:

- trades: 170;
- target-first: 27.1%;
- average simplified price P&L: +0.15 XAU/trade;
- exploratory trades/day: 2.41;
- zero-trade days: 0%;
- <= USD 50 days: 88.1%;
- >= USD 100 days: 6.8%;
- >= USD 150 days: 1.7%;
- losing days: 59.3%;
- average daily P&L in the exploratory 0.10-lot-style simulator: about -USD 2.36.

This is an important result: removing zero-signal days by increasing opportunity frequency did **not** solve the project objective. It increased losing-day frequency and did not improve the low-output-day distribution enough.

### E4 breakout-candle stop

Development: 1 trade.  
Holdout: 4 trades.

Too sparse to interpret.

## Conclusion

**Do not promote current Engine E formulations.**

The high-frequency loose version demonstrates the difference between:

- reducing zero-trade days; and
- producing robust profitable days.

The project needs independent positive-expectancy opportunity streams, not merely more signals.

## Next action

Stop hand-tuning additional XAU-only variants for now.

Move to **multi-asset opportunity expansion** and test whether the project objective improves by scanning several liquid markets while keeping quality thresholds intact.

Finalist strategies should later be cross-validated on an independent data source.
