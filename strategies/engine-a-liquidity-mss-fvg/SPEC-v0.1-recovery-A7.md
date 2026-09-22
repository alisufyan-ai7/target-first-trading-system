# Engine A Original Recovery — Variant A7

**Status:** FROZEN BEFORE OUTCOME INSPECTION  
**Version:** 0.1-recovery-A7  
**Frozen:** 2026-09-22  
**Experiment:** EXP-014 Part A

## Purpose

Variant A7 inherits A6, which brought frequency and average risk close to the EXP-002 benchmark. A7 changes exactly one ambiguity: how tightly the FVG must be associated with the displacement candle.

It is a recovery hypothesis, not a claim that these missing details were the unpublished original implementation. No A7 parameter may be changed after A7 outcomes are calculated. All A6 rules remain unchanged except FVG timing below.

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

## Liquidity-level reuse — A6 single-ambiguity change

The most recent confirmed 5m pivot remains the active liquidity level until either:

- a newer same-side confirmed pivot replaces it; or
- it becomes older than the unchanged 24-completed-5m-bar age limit.

A qualifying sweep does **not** permanently consume or retire that level.

Therefore, while the same pivot remains the latest eligible level, more than one later 5m bar may independently qualify as a sweep if each bar satisfies the unchanged sweep rule.

Each qualifying sweep bar creates at most one setup attempt on that side.

The existing one-open-trade policy still suppresses setups/trades that occur while an A6 trade is open. Suppression does not otherwise retire the liquidity level.

No new cooldown is introduced.

No other A3 rule changes in A6.

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

## Displacement — A2 single-ambiguity change

A2 keeps the **first MSS** rule unchanged, but displacement is allowed to occur on:

- the MSS candle itself; or
- either of the next two completed 1m candles.

For each eligible displacement candle:

- real body direction must agree with the MSS direction;
- absolute real body >= **1.6 x** the mean absolute real body of that candle's prior 20 completed 1m candles;
- the candidate candle is excluded from its 20-bar baseline;
- require all 20 baseline bars to exist;
- bearish: its close must remain below the already-broken internal swing low;
- bullish: its close must remain above the already-broken internal swing high.

Use the **first** candle in this three-candle window that satisfies all displacement conditions.

If none qualifies, the setup expires.

No second MSS is searched for and the internal pivot is not changed.

## FVG — A7 single-ambiguity change

Use the same standard three-candle imbalance with no additional minimum gap size.

For the **displacement candle itself** as third candle j:

Bullish FVG:

- low[j] > high[j-2];
- FVG zone = [high[j-2], low[j]].

Bearish FVG:

- high[j] < low[j-2];
- FVG zone = [high[j], low[j-2]].

A7 requires that the qualifying same-direction FVG be formed **on the displacement candle itself**.

If the displacement candle does not form the FVG, the setup expires. A7 does not search the next one or two candles for a later FVG.

The gap width must be strictly positive.

No FVG minimum-size filter is added.

## Entry

- entry price = exact midpoint of the selected FVG;
- entry search starts with the first 1m bar after the FVG third candle has completed;
- allow at most 10 completed 1m bars for midpoint retracement;
- midpoint is filled when that bar's low <= midpoint <= high;
- entry must occur strictly before 18:00 UTC;
- if no fill occurs in the 10-bar window, the setup expires;
- no market-entry substitution is allowed.

## Tight structural/FVG stop — A3 single-ambiguity change

A3 keeps FVG invalidation as the stop concept but replaces A2's fixed USD 0.10 buffer with a buffer equal to **25% of the selected FVG width**.

Let `W = upper_FVG_edge - lower_FVG_edge`.

Bearish:

- stop = upper edge of bearish FVG + `0.25 x W`.

Bullish:

- stop = lower edge of bullish FVG - `0.25 x W`.

Entry remains the FVG midpoint.

Reject the trade if the stop is not on the correct side of entry or if risk distance is non-positive.

No other A2 rule changes in A3.

## Concurrent-trade policy

- maximum one open Engine A A2 trade at a time on XAUUSD;
- a setup whose sweep occurs while an A1 trade is open is ignored and its swept level is still treated as consumed;
- rejected/suppressed setups do not reactivate later;
- no pyramiding.
- if multiple eligible midpoint fills occur on the same 1m timestamp while flat, priority is: earlier sweep time, then earlier FVG-confirmation time, then bearish before bullish as the final deterministic tie-break.

## Same-bar ambiguity

Conservative handling:

- if entry and stop are both touched in the fill bar, count the stop first;
- a target touched on the fill bar is **not** credited because intrabar ordering relative to the midpoint fill is unknowable; target evaluation begins on the next completed 1m bar;
- after the fill bar, if a target and stop are both touched in the same 1m bar, count the stop first.

## Maximum trade horizon

A trade is considered open, for the one-open-trade rule, until the earliest of:

1. the USD 5 primary target (T5);
2. structural stop;
3. the close of the **120th 1m bar counting the fill bar as bar 1**;
4. 20:00 UTC on the entry date;
5. last available bar of the entry date if data end earlier.

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

Maximum favorable excursion is measured over the **actual A7 trade life**: from entry until T5, structural stop, or the frozen time horizon, whichever occurs first. Because fill-bar ordering is unknowable, A7 records fill-bar MFE as zero and begins MFE accumulation with the next completed 1m bar. For a T5 winner, realized MFE is capped at USD 5 because the trade exits at T5.

Long MFE = max(high - entry) over the active path, capped at 5 on a T5 exit.  
Short MFE = max(entry - low) over the active path, capped at 5 on a T5 exit.

## Simplified expectancy

For the EXP-002 reproduction comparison, A7 simplified T5 P&L in Gold-price units is:

- T5 reached first: +5.00;
- structural stop reached first: -actual structural risk distance;
- neither before horizon: directional mark-to-market at the horizon close, clipped to [-risk distance, +5.00].

Report overall, development, and holdout means.

## Reproduction decision

Compare A7 to the frozen numerical acceptance protocol in:

- research/experiments/EXP-014-original-engine-a-recovery-equivalent-sizing.md.

A7 is a recovered reproduction only if the full frozen PASS definition is satisfied.

If A1 misses, checkpoint the full vector before defining A2. Any A2 change must address one identifiable ambiguity rather than changing several unrelated mechanics simultaneously.
