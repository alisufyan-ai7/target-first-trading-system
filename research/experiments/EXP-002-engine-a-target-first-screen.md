# EXP-002 — Engine A XAUUSD Target-First Screen

**Status:** COMPLETED EXPLORATORY SCREEN  
**Date:** 2026-09-22

## Question

Can a mechanical Badar-inspired XAUUSD setup produce frequent enough USD 5 favorable moves to support the desired daily-income distribution?

## Dataset

- XAUUSD one-minute historical OHLC;
- baseline source: Dukascopy public minute archive;
- period: 2026-03-01 through 2026-08-20;
- approximately 230,813 one-minute bars processed;
- 5m and 15m bars resampled mechanically;
- broker-specific spread/commission/slippage excluded from this Phase-1 screen.

## Mechanical variant

Practical high-frequency version:

1. recent 5m swing liquidity;
2. 5m wick beyond level and close back inside;
3. 1m internal MSS requiring a close beyond a recent internal pivot;
4. displacement around >= 1.6x recent one-minute average candle body;
5. FVG after the shift;
6. entry around 50% of FVG;
7. tight FVG/structural stop;
8. primary session window about 06:00–18:00 UTC;
9. fixed USD 5 favorable target for target-first label.

## Overall result

Approximately:

- trades/signals: 372;
- USD 5 target-first hit rate: 29.6%;
- average structural risk distance: USD 1.02 Gold;
- median favorable excursion: USD 3.30 Gold;
- average simplified price expectancy: +USD 0.79 Gold/trade before costs.

## Development / holdout

### March–May 2026

- trades: about 185;
- USD 5 target-first: 31.9%;
- average risk: about USD 1.16;
- median favorable excursion: about USD 3.46;
- average simplified price expectancy: about +USD 0.85 Gold/trade.

### June–August 20, 2026

- trades: about 187;
- USD 5 target-first: 27.3%;
- average risk: about USD 0.89;
- median favorable excursion: about USD 2.98;
- average simplified price expectancy: about +USD 0.72 Gold/trade.

## Target-distance sensitivity on later holdout

Using approximately the same entries/stops:

| Favorable target | Target-first rate |
|---|---:|
| USD 2 | 48.7% |
| USD 3 | 41.7% |
| USD 4 | 31.6% |
| USD 5 | 27.3% |

## Liquidity-source observation

Major levels such as previous-day, Asian-session, and London-session highs/lows produced too few fully confirmed setups to satisfy the desired trade frequency.

Broader 5m swing liquidity produced the most usable sample.

## Daily-distribution conclusion

The strategy did not approach the desired daily P&L distribution.

Low-output days dominated and USD 100+ / USD 150+ days were too rare.

## Disposition

**Retain Engine A only as one candidate generator.**

Do not treat it as the complete trading system.

## Limitations

- no execution costs;
- no broker-specific bid/ask modeling;
- common 0.10-lot Gold P&L translation is illustrative only;
- six-month window is insufficient for promotion;
- exact Badar proprietary implementation is not known.
