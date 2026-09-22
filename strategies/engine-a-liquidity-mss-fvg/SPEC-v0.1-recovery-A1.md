# Engine A Original Recovery — Variant A1

**Status:** FROZEN BEFORE OUTCOME INSPECTION  
**Version:** 0.1-recovery-A1  
**Frozen:** 2026-09-22  
**Experiment:** EXP-014 Part A

## Purpose

Variant A1 is the first fully mechanical attempt to reconstruct the original EXP-002 XAUUSD Engine A.

It is a recovery hypothesis, not a claim that these missing details were the unpublished original implementation. No A1 parameter may be changed after A1 outcomes are calculated.

The governing sequence remains:

liquidity -> sweep -> internal MSS -> displacement -> FVG -> retracement -> tight FVG/structural invalidation.

## Data and bar construction

- instrument: XAUUSD;
- source: Dukascopy public one-minute OHLC, consistent with EXP-002;
- timestamps: UTC;
- full comparison window: 2026-03-01 through 2026-08-20 inclusive;
- development: 2026-03-01 through 2026-05-31 inclusive;
- holdout: 2026-06-01 through 2026-08-20 inclusive;
- resample 1m bars into UTC-aligned 5m bars using open = first, high = max, low = min, close = last;
- a 5m bar is valid only when all five expected one-minute observations are present;
- 5m bars are treated as known only after their final constituent 1m bar has completed.

## Active session boundaries

- new setup processing begins at 06:00 UTC;
- a 5m sweep bar must complete strictly before 18:00 UTC;
- a retracement entry must fill at a 1m timestamp strictly before 18:00 UTC;
- an already-open trade may remain active after 18:00 subject to the frozen horizon below;
- no new setup or entry is created at or after 18:00 UTC.

## 5m liquidity swing

Use a deliberately local/high-frequency confirmed 5m pivot.

Swing high at completed 5m bar t:

- high[t] > high[t-1];
- high[t] >= high[t+1].

Swing low is mirrored:

- low[t] < low[t-1];
- low[t] <= low[t+1].

The pivot becomes eligible only after t+1 has completed, preventing future-looking use.

For each direction use the **most recent confirmed pivot** no older than 24 completed 5m bars (120 minutes) at the moment a sweep bar completes.

## Liquidity-level reuse

- each confirmed pivot level may generate at most one qualifying sweep event;
- once a bar qualifies as a sweep of that level, the level is retired for future A1 setups on that side, even if later MSS/FVG/entry conditions fail;
- a later newly confirmed pivot may create a new eligible level;
- no additional arbitrary cooldown is applied beyond level retirement and the one-open-trade rule.

## 5m sweep

Bearish candidate:

- sweep-bar high > eligible swing-high level; and
- sweep-bar close < that swing-high level.

Bullish candidate:

- sweep-bar low < eligible swing-low level; and
- sweep-bar close > that swing-low level.

The sweep itself is not an entry.

## 1m internal pivot for MSS

At the completion of the sweep bar, identify the most recent already-confirmed opposite-side 1m pivot from the preceding 12 completed minutes.

A confirmed 1m swing low at minute t requires:

- low[t] < low[t-1];
- low[t] <= low[t+1].

A confirmed 1m swing high is mirrored.

The pivot becomes usable only after t+1 has completed.

Bearish setup uses the most recent confirmed internal swing low.  
Bullish setup uses the most recent confirmed internal swing high.

If none exists in the 12-minute lookback, the setup expires.

## MSS timing and rule

Starting with the first completed 1m candle after the sweep bar completes, allow at most 10 completed 1m bars for MSS.

Bearish MSS:

- 1m close < internal swing low.

Bullish MSS:

- 1m close > internal swing high.

Only the first qualifying MSS is used.

## Displacement

The MSS candle itself must also be the displacement candle.

Requirements:

- real body direction agrees with the MSS direction;
- absolute real body >= **1.6 x** the mean absolute real body of the prior 20 completed 1m candles;
- the MSS/displacement candle is excluded from the 20-bar baseline;
- require all 20 baseline bars to exist.

If the MSS candle fails displacement, the setup expires; A1 does not wait for a later second MSS.

## FVG

Use the standard three-candle imbalance with no additional minimum gap size.

For a third candle j:

Bullish FVG:

- low[j] > high[j-2];
- FVG zone = [high[j-2], low[j]].

Bearish FVG:

- high[j] < low[j-2];
- FVG zone = [high[j], low[j-2]].

After the valid MSS/displacement candle, accept the **first** same-direction FVG whose third candle is:

- the MSS/displacement candle itself; or
- one of the next two completed 1m candles.

The gap width must be strictly positive.

## Entry

- entry price = exact midpoint of the selected FVG;
- entry search starts with the first 1m bar after the FVG third candle has completed;
- allow at most 10 completed 1m bars for midpoint retracement;
- midpoint is filled when that bar's low <= midpoint <= high;
- entry must occur strictly before 18:00 UTC;
- if no fill occurs in the 10-bar window, the setup expires;
- no market-entry substitution is allowed.

## Tight structural/FVG stop

A1 uses FVG invalidation rather than the distant 5m sweep extreme.

Bearish:

- stop = upper edge of bearish FVG + **USD 0.10**.

Bullish:

- stop = lower edge of bullish FVG - **USD 0.10**.

Reject the trade if the stop is not on the correct side of entry or if risk distance is non-positive.

The USD 0.10 buffer is fixed prospectively and is not volatility-scaled.

## Concurrent-trade policy

- maximum one open Engine A A1 trade at a time on XAUUSD;
- a setup whose sweep occurs while an A1 trade is open is ignored and its swept level is still treated as consumed;
- rejected/suppressed setups do not reactivate later;
- no pyramiding.

## Same-bar ambiguity

Conservative handling:

- if entry and stop are both touched in the fill bar, count the stop first;
- after entry, if a target and stop are both touched in the same 1m bar, count the stop first.

## Maximum trade horizon

A trade path is observed until the earliest of:

1. structural stop;
2. **120 completed 1m bars after entry**;
3. 20:00 UTC on the entry date;
4. last available bar of the entry date if data end earlier.

No overnight carry.

## Target-first labels

Using the same entry and stop, independently label whether each favorable XAU move occurs before structural stop:

- T2 = USD 2;
- T3 = USD 3;
- T4 = USD 4;
- T5 = USD 5.

For long trades target = entry + distance.  
For short trades target = entry - distance.

If target and stop occur in the same bar, stop wins.

## MFE

Maximum favorable excursion is measured from entry until the earliest of structural stop or the frozen trade horizon, without truncating MFE at T5.

Long MFE = max(high - entry).  
Short MFE = max(entry - low).

## Simplified expectancy

For the EXP-002 reproduction comparison, A1 simplified T5 P&L in Gold-price units is:

- T5 reached first: +5.00;
- structural stop reached first: -actual structural risk distance;
- neither before horizon: directional mark-to-market at the horizon close, clipped to [-risk distance, +5.00].

Report overall, development, and holdout means.

## Reproduction decision

Compare A1 to the frozen numerical acceptance protocol in:

- research/experiments/EXP-014-original-engine-a-recovery-equivalent-sizing.md.

A1 is a recovered reproduction only if the full frozen PASS definition is satisfied.

If A1 misses, checkpoint the full vector before defining A2. Any A2 change must address one identifiable ambiguity rather than changing several unrelated mechanics simultaneously.
