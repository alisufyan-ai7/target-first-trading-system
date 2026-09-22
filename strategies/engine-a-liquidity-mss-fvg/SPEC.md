# Engine A — Original Gold Recovery Specification

**Status:** ACTIVE RECOVERY LEAD  
**Version:** 0.1-recovery-target

## Purpose

Recover the original Badar-inspired XAUUSD implementation that produced EXP-002 closely enough to create a reproducible, versioned strategy engine.

Do not confuse this with SPEC-v0.2-portable.md.

## Evidence-derived bearish sequence

1. identify meaningful/recent 5m buy-side liquidity;
2. require a 5m sweep beyond the level and rejection/close back inside;
3. after the sweep identify a recent internal 1m swing low;
4. require a 1m candle **close** below that internal low for the first recovery version;
5. require bearish displacement relative to recent 1m candle bodies;
6. require a bearish three-candle FVG associated with the displacement/shift;
7. wait for retracement into the FVG entry area;
8. enter short;
9. use the recovered tight structural/FVG invalidation;
10. evaluate target-first outcomes and available continuation.

Bullish logic is mirrored.

## Recorded practical EXP-002 screen parameters

Approximate starting values:

- 5m swing liquidity;
- 1m execution;
- MSS close required;
- displacement >= about 1.6x recent average 1m body;
- FVG after structure shift;
- entry around 50% of FVG;
- active window about 06:00–18:00 UTC;
- fixed USD 5 favorable XAU target for the original target-first label.

## Recovery unknowns

The exact EXP-002 code was not persisted. The recovery must resolve and document:

- 5m swing confirmation strength/lookback;
- internal 1m pivot definition/lookback;
- FVG minimum size;
- entry fill window;
- stop placement/buffer;
- target/stop same-bar rule;
- one-open-trade handling;
- setup reuse/cooldown;
- horizon/timeout;
- session edge handling.

## Reproduction gate

Recovered code is not allowed to become “original Engine A” merely because the concept looks similar.

It should approximately reproduce EXP-002:

- ~372 overall trades/signals;
- overall USD 5 target-first ~29.6%;
- average structural risk ~USD 1.02 Gold;
- median MFE ~USD 3.30;
- simplified expectancy ~+USD 0.79 Gold/trade.

Development March–May:

- ~185 trades;
- USD 5 ~31.9%;
- expectancy ~+USD 0.85 Gold/trade.

Holdout June–Aug 20:

- ~187 trades;
- USD 5 ~27.3%;
- expectancy ~+USD 0.72 Gold/trade;
- USD 2 48.7%;
- USD 3 41.7%;
- USD 4 31.6%;
- USD 5 27.3%.

Reasonable tolerance should be defined before trying variants. If no reconstruction reproduces the benchmark without post-hoc manipulation, preserve the discrepancy rather than claiming success.

## Timeframe/context note

The first recovered engine is deliberately narrow and mechanical.

Broader 15m context, BOS, volume/VSA, DXY, news, order-block quality, IFVG, and secondary-entry logic are potential later filters/branches, not assumptions to insert while recovering EXP-002.

See:

- docs/BADAR-VIDEO-EVIDENCE.md;
- docs/TIMEFRAME-AND-MARKET-CONTEXT.md.

## Status

Do not deploy live.

The immediate task is reproducibility.
