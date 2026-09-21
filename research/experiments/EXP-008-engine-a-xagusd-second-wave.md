# EXP-008 — Engine A v0.2 XAGUSD Second-Wave Transfer Test

**Status:** COMPLETE — XAGUSD ARM REJECTED  
**Date:** 2026-09-22

## Purpose

Run one small second-wave market test before deciding whether further Engine A market expansion is justified.

This experiment does not modify Engine A v0.2.

## Question

Does the frozen Engine A v0.2 liquidity-sweep / MSS / displacement / FVG / retracement logic show robust positive target-first expectancy on XAGUSD under the same USD 20 structural-risk / USD 50 target framework?

## Strategy

Use unchanged:

- `strategies/engine-a-liquidity-mss-fvg/SPEC-v0.2-portable.md`.

No XAG-specific signal parameters are permitted.

## Data

External public research feed:

- repository: `getdata-finance/xagusd-1m-ohlcv-metals-historical-data`;
- file: `XAGUSD_1m.csv`;
- UTC one-minute OHLCV sample.

The public sample covers the same useful 2026 window as the other GetData feeds.

Common experiment split:

- development: 2026-03-12 through 2026-05-31;
- holdout: 2026-06-01 through 2026-08-20.

## Economics

Silver is quoted in USD per ounce in this research feed.

For each trade:

- structural stop is the frozen sweep invalidation;
- gross stop risk = USD 20;
- target = USD 50 = +2.5R;
- position ounces = `20 / stop_USD_per_oz`;
- notional = `ounces x entry_price`;
- no broker-specific lot conversion, spread, commission, slippage, or margin specification is assumed.

## Metrics

Report the same EXP-007 metrics:

- signal funnel;
- trades and trades/day;
- 2.5R target-first rate;
- mean/median R;
- timeout rate;
- median structural stop;
- median ounces;
- median notional/equity;
- mean daily P&L;
- losing days;
- <= USD 50 days;
- >= USD 100 and >= USD 150 days;
- max drawdown;
- consecutive losing and low-output days.

All eligible UTC weekdays are counted, including zero-signal days.

## Promotion rule

XAGUSD is not promoted merely for a positive holdout.

A research lead requires at minimum:

- non-negative/positive mean R in both development and holdout;
- no obvious split collapse;
- sufficient observations;
- daily distribution that adds material value;
- economics that are not obviously incompatible with the USD 500 reference account.

## Deferred market

GBPJPY remains in the candidate universe, but the matching GetData public sample was not available during this checkpoint. No substitute feed will be introduced mid-experiment merely to force an additional market.

## Next action

Run XAGUSD once under the frozen rules, checkpoint the result, and then decide whether additional Engine A market expansion is justified or whether research should shift to an independent engine family.


## Result

**Status:** COMPLETE — XAGUSD ARM REJECTED

### Full-window signal funnel

- eligible 5m sweep events examined: 2,537;
- sweep events reaching valid MSS + displacement: 687;
- events reaching a qualifying FVG: 516;
- raw retracement fills before one-open filtering: 342;
- accepted trades after one-open filtering: 256.

### Development — 2026-03-12 through 2026-05-31

- eligible weekdays: 57;
- trades: 120;
- trades/day including zero-signal weekdays: 2.11;
- 2.5R target-first win rate: 20.83%;
- mean R/trade: -0.179R;
- median R/trade: -1.00R;
- timeout rate: 5.83%;
- median structural stop distance: USD 0.276/oz;
- median position size at USD 20 structural risk: 72.47 oz;
- median notional/equity ratio: 11.9x;
- mean daily P&L: -USD 7.53;
- losing days: 63.16%;
- <= USD 50 days: 92.98%;
- >= USD 100 days: 1.75%;
- >= USD 150 days: 0%;
- maximum drawdown: approximately USD 619.85;
- maximum consecutive losing days: 9;
- maximum consecutive <= USD 50 days: 22;
- total simulated P&L: approximately -USD 429.41.

### Holdout — 2026-06-01 through 2026-08-20

- eligible weekdays: 59;
- trades: 136;
- trades/day including zero-signal weekdays: 2.31;
- 2.5R target-first win rate: 23.53%;
- mean R/trade: -0.161R;
- median R/trade: -1.00R;
- timeout rate: 1.47%;
- median structural stop distance: USD 0.16875/oz;
- median position size at USD 20 structural risk: 118.52 oz;
- median notional/equity ratio: 15.2x;
- mean daily P&L: -USD 7.41;
- losing days: 55.93%;
- <= USD 50 days: 93.22%;
- >= USD 100 days: 3.39%;
- >= USD 150 days: 1.69%;
- maximum drawdown: approximately USD 637.08;
- maximum consecutive losing days: 6;
- maximum consecutive <= USD 50 days: 22;
- total simulated P&L: approximately -USD 437.08.

## Interpretation

XAGUSD fails in both development and holdout under the unchanged Engine A v0.2 rules.

The holdout target-first rate is below the simple no-cost 28.57% break-even rate for the -1R/+2.5R payoff and mean R remains negative.

Although XAGUSD's median notional/equity burden is materially lower than the FX arms in EXP-007, the expectancy and daily-output distributions are unacceptable.

## Conclusion

**Reject the XAGUSD Engine A v0.2 arm.**

Do not tune XAG-specific signal parameters after this result.

The small second-wave test did not produce an additional robust Engine A stream. Combined with EXP-007, this is enough evidence to stop expanding or loosening Engine A for now.

## Next action

Shift the next strategy experiment to a **genuinely independent setup family** rather than continuing Engine A market hunting.

USDJPY / Engine A v0.2 remains preserved as a statistical research lead for later independent-feed and execution-cost validation, but it is not promoted.
