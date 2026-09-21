# EXP-006 — Multi-Asset Data and Target-Normalization Checkpoint

**Status:** COMPLETE — DATA FEASIBLE; INITIAL VOLATILITY-BURDEN SIZING NOT SUITABLE FOR PORTFOLIO ECONOMICS  
**Date:** 2026-09-22

## Purpose

Prepare the first multi-asset expansion test without changing strategy quality thresholds or contaminating holdout data.

This experiment is a prerequisite to the first cross-market strategy screen.

## Question

Can we define a small set of liquid non-Gold markets with:

1. reliable one-minute intraday data over a useful overlap with the prior XAUUSD window;
2. clean instrument economics for translating a favorable price move into an approximately USD 50 profit unit;
3. target distances calibrated from development data only, so later holdout testing remains untouched?

## Initial market set

First-wave candidates:

- EURUSD;
- GBPUSD;
- USDJPY.

Reference comparator:

- XAUUSD.

XAGUSD, equity-index CFDs, and crypto remain candidates for later waves.

## Data source

The original preference was Dukascopy, consistent with prior experiments. The current chat environment could not directly retrieve the Dukascopy binary archive, so this checkpoint did **not** fabricate Dukascopy results.

For this feasibility/calibration checkpoint, public one-minute sample files published by GetData were used as an external research feed:

- XAUUSD: `getdata-finance/xauusd-1m-ohlcv-metals-historical-data`;
- EURUSD: `getdata-finance/eurusd-1m-ohlcv-forex-historical-data`;
- GBPUSD: `getdata-finance/gbpusd-1m-ohlcv-forex-historical-data`;
- USDJPY: `getdata-finance/usdjpy-1m-ohlcv-forex-historical-data`.

The samples are UTC one-minute OHLCV files and cover approximately 2026-03-12 through 2026-09-11. This is an **independent external research source**, not durable project context and not a replacement for later Dukascopy/broker validation.

The vendor describes its FX datasets as broker-CFD/mid-quote data. Therefore any finalist must still be cross-validated on another feed.

## Window and split used here

Because the public samples begin on 2026-03-12, the usable window differs slightly from the prior XAU baseline:

- calibration/development: 2026-03-12 through 2026-05-31;
- untouched strategy holdout reserved for later: 2026-06-01 through 2026-08-20.

No cross-market strategy-result inspection was performed in EXP-006.

## Data audit

Rows from 2026-03-12 through 2026-08-20:

| Instrument | Rows | Development rows | Duplicate timestamps | Invalid OHLC rows |
|---|---:|---:|---:|---:|
| XAUUSD | 157,826 | 76,855 | 0 | 0 |
| EURUSD | 166,890 | 81,930 | 0 | 0 |
| GBPUSD | 166,864 | 81,912 | 0 | 0 |
| USDJPY | 166,889 | 81,929 | 0 | 0 |

A simple >10-minute non-weekend gap check found no such gaps for the three FX samples. XAUUSD produced 98 flags, which are consistent with the metals feed's scheduled daily closures/holiday gaps and should not automatically be treated as missing-data errors. A session-aware gap audit should be used before any finalist validation.

## Frozen development-only volatility metric

To avoid looking at strategy outcomes, target calibration used only market volatility.

Metric:

- resample the 1m feed into hourly bars;
- keep hourly bars in the Engine A research window, 06:00 <= UTC < 18:00;
- require at least 45 one-minute observations in an hourly bar;
- calculate hourly true range;
- use the development-period median hourly true range.

Observed medians:

| Instrument | Median hourly true range |
|---|---:|
| XAUUSD | 22.675 USD/oz |
| EURUSD | 0.001410 = 14.10 pips |
| GBPUSD | 0.001950 = 19.50 pips |
| USDJPY | 0.1680 = 16.80 pips |

The XAUUSD USD 5 reference target therefore equals:

`5 / 22.675 = 0.2205`

or about 22.05% of the development-period median hourly true range.

## Initial volatility-burden target mapping

Applying the same 0.2205 hourly-TR burden gives:

| Instrument | Frozen favorable move | Approx pips |
|---|---:|---:|
| XAUUSD | 5.0000 | n/a |
| EURUSD | 0.0003109 | 3.11 |
| GBPUSD | 0.0004300 | 4.30 |
| USDJPY | 0.03705 | 3.70 |

These values were computed **before** inspecting any cross-market Engine A strategy outcomes.

## USD 50 gross-profit translation

Using unit-based FX P&L math:

- for EURUSD/GBPUSD, USD P&L is approximately base units x price move because USD is the quote currency;
- for USDJPY, JPY P&L must be converted back to USD, so the required base-unit quantity depends on USDJPY price.

Using development-period median prices only for an indicative size translation:

| Instrument | Approx units for USD 50 target | Approx standard lots* | Approx USD notional |
|---|---:|---:|---:|
| EURUSD | 160,816 EUR | 1.608 | 189,021 |
| GBPUSD | 116,282 GBP | 1.163 | 156,798 |
| USDJPY | 214,584 USD | 2.146 | 214,584 |

`* standard-lot equivalents assume the common 100,000-base-unit convention; broker specifications must be verified before execution modeling.`

Illustrative margin requirement at 1:500 leverage would still be roughly:

- EURUSD: USD 378;
- GBPUSD: USD 314;
- USDJPY: USD 429.

At 1:100 leverage the corresponding illustrative margin is about USD 1,890, USD 1,568, and USD 2,146 respectively.

## Economic tension discovered

This normalization is mathematically clean but economically unattractive for a USD 500 reference account.

If size were instead limited to 0.10 standard lot (10,000 base units), an approximately USD 50 gross target would require roughly:

| Instrument | Favorable move for ~USD 50 at 0.10 lot | Burden vs median hourly TR |
|---|---:|---:|
| EURUSD | 50.0 pips | 3.55x |
| GBPUSD | 50.0 pips | 2.56x |
| USDJPY | ~79.5 pips | 4.73x |

So there is a direct trade-off:

- small, volatility-comparable targets require very large position size;
- small position size requires much larger favorable moves.

This is a material constraint for the project's small-account consistency objective.

## Conclusion

**Data feasibility: PASS for a provisional cross-market research screen.**

**Initial volatility-burden position-sizing rule: DO NOT USE as the portfolio-economic rule.**

The public samples are sufficient to support a prospective cross-market experiment over the common 2026-03-12 to 2026-08-20 window, but:

1. they are an independent external feed rather than the prior Dukascopy baseline;
2. the common window begins on March 12, not March 1;
3. the volatility-burden mapping produces position sizes that are too aggressive relative to the reference USD 500 account;
4. broker-specific margin, contract, spread, commission, and slippage remain unmodeled.

## Next action

Before running cross-market strategy outcomes, freeze a **portable, fully mechanical Engine A specification** and a risk-consistent USD 50 target framework.

The next experiment should use:

- prospective rules only;
- no tuning to EURUSD/GBPUSD/USDJPY holdout outcomes;
- structural stop first;
- a fixed trade-risk cap consistent with the USD 40 normal daily loss stop;
- USD 50 target translated from the same position size;
- explicit notional/equity and margin-feasibility diagnostics;
- the original XAUUSD USD 5 target retained as a separate Gold diagnostic.
