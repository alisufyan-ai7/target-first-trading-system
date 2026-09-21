# EXP-009 — Engine F Statistical Mean-Reversion Screen

**Status:** IN PROGRESS — XAUUSD CHECKPOINT COMPLETE; RULES REMAIN FROZEN  
**Date:** 2026-09-22

## Purpose

Test a genuinely independent opportunity stream after EXP-008 paused further Engine A market expansion.

## Question

Can a simple price-only statistical extension -> re-entry -> mean-reversion engine produce positive target-first expectancy in both development and holdout while adding an opportunity stream structurally independent from Engines A-E?

## Frozen strategy

Use `strategies/engine-f-statistical-mean-reversion/SPEC-v0.1-portable.md` unchanged.

Core logic:

1. 60-minute rolling mean/std from completed 5m closes;
2. detect |z| >= 2.0 extension;
3. require re-entry to |z| <= 1.5 on the relevant side within 30 minutes;
4. enter at the next 1m open;
5. stop beyond the excursion extreme by 0.25 x 5m ATR(14);
6. accept only if the rolling mean is at least 2.5R away in the reversion direction;
7. risk USD 20 to target USD 50 (+2.5R);
8. conservative same-bar handling and 20:00 UTC timeout;
9. one open Engine F trade per instrument plus reset/cooldown rule.

## Data

Use the already documented provisional external GetData one-minute samples from EXP-006.

Common split:

- development: 2026-03-12 through 2026-05-31;
- holdout: 2026-06-01 through 2026-08-20.

This feed remains provisional research data. Any finalist still requires independent-feed and broker-specific cost validation.

## Checkpoint sequence

Run and write back one market at a time:

1. XAUUSD;
2. USDJPY;
3. EURUSD;
4. GBPUSD.

Do not alter parameters between markets.

## Promotion discipline

A single positive holdout is not sufficient.

A market arm can remain a research lead only if:

- development and holdout mean R are both positive or at minimum do not show a clear sign-instability pattern;
- the result is not driven by a tiny sample;
- daily-distribution and economic-feasibility diagnostics are explicitly reported.

Do not tune failed arms after seeing holdout.

## Market checkpoint 1 — XAUUSD

**Status:** NOT PROMOTED

### Data processed

- one-minute rows in the EXP-009 window: 157,826;
- resampled 5m bars: 31,575;
- full-window extension events after sequencing/cooldown logic: 1,001;
- qualifying re-entry confirmations: 971;
- accepted trades after the 2.5R-to-mean feasibility gate and one-open/cooldown rules: 37.

The large drop from re-entry confirmations to accepted trades is expected because Engine F only accepts a setup when the current 60-minute mean is at least 2.5R away from the actual entry.

### Development — 2026-03-12 through 2026-05-31

- eligible weekdays: 57;
- trades: 13;
- trades/day including zero-signal weekdays: 0.23;
- 2.5R target-first hit rate: 23.08%;
- mean R/trade: -0.192R;
- median R/trade: -1.00R;
- timeout rate: 0%;
- median structural/statistical stop distance: USD 3.054/oz;
- median position size at USD 20 risk: 6.55 oz;
- median notional/equity ratio: 65.36x;
- mean daily P&L: about -USD 0.88;
- losing days: 14.04%;
- <= USD 50 days: 100%;
- >= USD 100 days: 0%;
- >= USD 150 days: 0%;
- maximum drawdown: about USD 140;
- maximum consecutive losing days: 2;
- maximum consecutive <= USD 50 days: 57;
- total simulated P&L: about -USD 50.

### Holdout — 2026-06-01 through 2026-08-20

- eligible weekdays: 59;
- trades: 24;
- trades/day including zero-signal weekdays: 0.41;
- 2.5R target-first hit rate: 29.17%;
- mean R/trade: +0.021R;
- median R/trade: -1.00R;
- timeout rate: 0%;
- median structural/statistical stop distance: USD 3.980/oz;
- median position size at USD 20 risk: 5.03 oz;
- median notional/equity ratio: 42.74x;
- mean daily P&L: about +USD 0.17;
- losing days: 22.03%;
- <= USD 50 days: 100%;
- >= USD 100 days: 0%;
- >= USD 150 days: 0%;
- maximum drawdown: about USD 100;
- maximum consecutive losing days: 2;
- maximum consecutive <= USD 50 days: 59;
- total simulated P&L: about +USD 10.

### Interpretation

The XAUUSD Engine F arm is not robust enough to retain as a lead.

Development expectancy is negative, while holdout is only marginally positive on 24 trades. The 29.17% holdout hit rate is only slightly above the simple no-cost 28.57% break-even rate for a -1R/+2.5R payoff, and the sample is small.

Most importantly for the project objective, every eligible development and holdout weekday remained <= USD 50. The arm therefore adds neither robust expectancy nor useful daily-output coverage.

The notional/equity burden also remains aggressive even though it is lower than the EXP-007 FX arms.

### Disposition

- Do not promote XAUUSD / Engine F v0.1.
- Do not tune the frozen Engine F parameters after this result.
- Continue unchanged to USDJPY as the second predeclared market checkpoint so the engine family is not judged from one instrument only.

## Next action

Run USDJPY under the already frozen Engine F v0.1 rules and write the result back before testing any third market.
