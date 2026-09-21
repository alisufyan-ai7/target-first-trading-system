# EXP-008 — Engine A v0.2 XAGUSD Second-Wave Transfer Test

**Status:** IN PROGRESS — RULES ALREADY FROZEN IN EXP-007  
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
