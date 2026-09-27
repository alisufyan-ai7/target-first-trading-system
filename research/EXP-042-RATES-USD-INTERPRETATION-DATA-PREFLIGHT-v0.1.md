# EXP-042 Rates / USD Interpretation Proxy Data Preflight v0.1

**Frozen:** 2026-09-27  
**Type:** zero-outcome data-source repeatability + immutable snapshot preflight  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed

## 1. Purpose

EXP-041 closed with `NO_STABLE_MACRO_INFORMATION_ADVANTAGE`.

The next governing information family is **market interpretation**:

> after a macro event, does the USD/rates complex confirm or reject the initial repricing?

Before any outcome model is allowed, freeze reproducible intraday proxy data for:

- Dukascopy US Dollar Index CFD: `dollaridxusd`;
- Dukascopy US T-Bond instrument: `ustbondtrusd`.

These are proxy instruments only.

The US T-Bond proxy is not equivalent to 2Y/5Y Treasury futures, SOFR/Fed-funds expectations, or true order flow. A negative future result cannot reject richer rates information.

## 2. Allowed interval

Request and retain only:

`2025-07-01T00:00:00Z <= t < 2026-06-30T00:00:00Z`

Timeframe:

`M1`.

Do not request Jul-Aug-Sep 2026.

## 3. Transport

Use the same pinned transport family already proven in EXP-041:

`dukascopy-node@1.50.0`.

Frozen instrument IDs:

- `dollaridxusd`;
- `ustbondtrusd`.

Normalize each file to:

`datetime,open,high,low,close,volume`.

Volume is retained for provenance only and is **not** authorized as true centralized traded volume.

## 4. Repeatability test

Perform two independent downloads A and B of the identical request.

For each instrument require:

- schema exact;
- rows > 100,000;
- >= 220 distinct UTC dates;
- first timestamp no later than 2025-07-02 23:59 UTC;
- last timestamp at least 2026-06-29 18:00 UTC;
- all rows inside the frozen interval;
- timestamps strictly increasing;
- no duplicates;
- positive prices;
- valid OHLC geometry;
- copy A SHA-256 == copy B SHA-256;
- copy A row count == copy B row count.

Do not loosen thresholds after seeing results.

## 5. Immutable release

If and only if both instruments pass, build deterministic archive:

Tag:

`exp042-rates-usd-proxy-m1-2025-07-01_2026-06-30-v1`

Asset:

`exp042-rates-usd-proxy-m1-2025-07-01_2026-06-30-v1.tar.gz`

Store source manifest with per-file SHA-256, row count, first/last timestamp and bytes.

Future EXP-042 modeling must consume the immutable release, not live Dukascopy.

## 6. Scientific restrictions

This preflight must not compute:

- structural candidates;
- target/path labels;
- T40/T50 outcomes;
- model probabilities;
- P&L;
- strategy rules.

Engine R and EXP-015 remain paused.

## 7. PASS disposition

`EXP042_RATES_USD_PROXY_REPEATABLE_SNAPSHOT_FROZEN`

## 8. FAIL disposition

`EXP042_RATES_USD_PROXY_DATA_NOT_REPEATABLE_FIX_OR_CHANGE_SOURCE`

Do not start a model if repeatability fails.

## 9. Next step after PASS

Freeze EXP-042 information-content design around the already-frozen macro event timestamps.

Candidate next comparison:

`LOCAL_M5 -> +DXY_REACTION -> +DXY_AND_TBOND_INTERPRETATION`.

The test must remain event-time causal and must not turn into generic cross-market OHLC consensus.
