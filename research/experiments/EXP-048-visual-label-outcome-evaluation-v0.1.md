# EXP-048 — Frozen Visual-Label Outcome Evaluation v0.1

**Status:** FROZEN BEFORE ANY EXP-048 POST-DECISION PATH IS LOADED  
**Date:** 2026-09-28  
**Parent replay protocol:** `59d426bd56c82a7d48a6081bc695a7a8eaa657e7`  
**Visual reviewer rubric:** `b667bb565abfed562044b42fd3e779a4c7a6af18`  
**Complete visual-label checkpoint:** `8ad19cccdf061afa02c878c0a88dde4700ad95ad`

## 1. Authorization

The complete 126-case visual review was frozen before any post-decision path was opened.

Frozen labels:

- 126 decisions;
- 75 NO_TRADE;
- 26 LONG;
- 25 SHORT;
- 51 total trade labels;
- 14 confidence A;
- 37 confidence B;
- all 51 trade labels use LEVEL_RETEST;
- feasibility gate PASS;
- EXP-047 overlap = zero;
- validation / holdout not loaded;
- no EXP-048 post-decision outcome exposed.

The scientific variable under test is the **representation method**:

- EXP-047: compressed numeric/text causal cards;
- EXP-048: rendered H1/M15/M5/M1 candlestick geometry.

Execution economics remain deliberately aligned with EXP-047.

## 2. Scientific question

> Do the 51 outcome-blinded selections made from actual rendered chart geometry show positive and reasonably stable post-cost value under the same causal Gold execution assumptions used for EXP-047?

No EXP-048 NO_TRADE case may be converted to a trade after outcome reveal.

## 3. Pinned artifacts

The evaluator must abort if any of these Git blobs changes:

- EXP-048 replay packets JSONL blob:
  `7ad151791071f86737c31315ae55e8fdfc4800c8`;
- complete visual labels JSONL blob:
  `c40a4bb56298d4206ce08ddab2ba9199a45a5732`;
- visual label summary blob:
  `df5254b4f3b542a4595c2a2247de50685f4c2b89`.

The 126 decisions are immutable for EXP-048 v0.1.

## 4. Data boundary

Outcome development source:

- warm-up: 2021-12-01 through 2021-12-31;
- evaluated development: 2022-01-01 through 2025-02-28.

Remain sealed and must not be downloaded:

- validation: 2025-03-01 through 2025-08-31;
- fresh holdout: 2025-09-01 through 2026-02-28.

Pinned free source:

`kevingtlin/Market-Data-Lab@922f83a60cc574e7395fb27397077288055a1ef6`.

## 5. Execution semantics

Every EXP-048 trade label is a frozen LEVEL_RETEST order.

- place a limit at frozen `entryPrice`;
- activate on the first market-active M1 bar starting at or after the frozen replay decision timestamp;
- order lives for at most 60 market-active M1 bars;
- order expires at 18:00 UTC even if fewer than 60 active bars elapsed.

Conservative pre-entry ordering:

1. if a bar reaches the frozen structural stop before an accepted fill can be resolved, invalidate the setup;
2. otherwise, if the bar touches entry, fill at the frozen entry price.

A bar touching both stop and entry before fill is:

`NO_FILL_PREENTRY_INVALIDATION`.

After fill, no TP1 is credited on the fill M1 bar. Outcome scanning starts on the next market-active M1 bar.

## 6. Frozen stop and target

Use exactly the stop and TP1 frozen in the visual label.

Do not:

- move the stop;
- substitute another structural level;
- change a fixed-2R target;
- trail the stop;
- add TP2;
- alter target after future candles are visible.

All filled trades are full-size to one TP1.

## 7. Post-entry same-bar ordering

On each evaluated M1 bar:

- if stop and TP1 are both touched, stop wins;
- otherwise exit at whichever frozen boundary is touched.

This preserves conservative OHLC ambiguity handling.

## 8. Intraday horizon

A filled trade exits at the earliest of:

1. frozen structural stop;
2. frozen TP1;
3. 120 market-active M1 bars after fill;
4. 20:00 UTC on the fill UTC date.

Timeout exit uses the close of the last market-active M1 bar at or before the cutoff.

No overnight positions.

## 9. Costs

Keep the same Gold research convention as EXP-047.

At 0.10 lot:

- primary round-trip friction: USD5;
- stress round-trip friction: USD10.

Scale friction linearly with actual lot.

These remain conservative research assumptions rather than claimed broker quotes.

## 10. Reference-account sizing

Reference equity: USD500.

Gold lot:

- maximum 0.10;
- step 0.01;
- never above 0.10.

Choose the largest legal lot <=0.10 such that:

`gross structural stop loss + stress friction <= USD40`.

For lot `L`:

- Gold P&L per USD1 move = `100 * L` USD;
- stress friction = `100 * L` USD;
- primary friction = `50 * L` USD.

If safe lot <0.01:

`NO_FILL_SAFE_LOT_BELOW_MINIMUM`.

Never shrink the frozen stop.

## 11. One-open reference simulation

Permit one open Gold position at a time.

Filled candidates are ordered by actual fill timestamp.

If simultaneous fills occur:

1. confidence A before B before C;
2. smaller structural risk at 0.10 lot;
3. replay ID lexical order.

A later fill while one Gold position is already open is blocked.

No post-result cohort/direction filtering may alter the primary result.

## 12. Daily state

Using primary realized P&L:

- if UTC-day realized P&L <= -USD40, add no new position that day;
- if UTC-day realized P&L >= +USD150, add no new position that day;
- otherwise later eligible fills may trade if no position is open.

No recovery sizing.

## 13. Predeclared eras

- ERA1: 2022-01-01 through 2022-12-31;
- ERA2: 2023-01-01 through 2023-12-31;
- ERA3: 2024-01-01 through 2025-02-28.

No era may be removed after outcomes.

## 14. Primary metrics

Report for the complete frozen 51-trade-label stream:

- trade labels;
- filled signals;
- no-fill reasons;
- LONG / SHORT filled counts;
- A / B filled counts;
- STOP / TP1 / TIMEOUT outcomes;
- gross R expectancy;
- primary R expectancy;
- stress R expectancy;
- primary / stress R profit factor;
- stress expectancy by era;
- stress expectancy by direction.

Reference account:

- actual trades;
- blocked one-open;
- blocked daily state;
- lot distribution;
- primary / stress USD expectancy;
- primary / stress PF;
- total primary / stress P&L;
- max primary / stress drawdown;
- distinct trade weekdays;
- daily P&L including zero-trade weekdays;
- >=USD100 / >=USD150 / >=USD200 day percentages;
- losing-day percentage;
- rolling five-day P&L;
- consecutive losing days.

A/B subgroup diagnostics may be reported descriptively only and cannot rescue a failed pooled result.

## 15. Frozen development gate

To isolate representation from EXP-047, use the same promotion gate:

1. >=30 filled signal trades;
2. >=25 reference-account actual trades;
3. >=20 distinct reference trade weekdays;
4. pooled gross R expectancy > +0.20R;
5. pooled primary R expectancy > 0;
6. pooled stress R expectancy > 0;
7. primary R PF >=1.10;
8. stress R PF >=1.05;
9. stress R expectancy >0 in at least 2 of 3 eras;
10. LONG stress R expectancy >0;
11. SHORT stress R expectancy >0;
12. reference primary expectancy >0 USD/trade;
13. reference stress expectancy >0 USD/trade;
14. reference primary PF >=1.10;
15. reference stress PF >=1.05;
16. stress maximum drawdown <=USD150;
17. validation / holdout remain sealed.

These thresholds are frozen before any EXP-048 post-decision candle is loaded.

## 16. Disposition

If all conditions pass:

`EXP048_VISUAL_BLINDED_SELECTION_READY_FOR_SEALED_VALIDATION`.

Otherwise:

`EXP048_VISUAL_BLINDED_SELECTION_FAIL_CLOSE_BEFORE_VALIDATION`.

A PASS authorizes only a separately frozen validation protocol, not live trading.

## 17. Anti-rescue rule

After outcome reveal:

- do not keep only LONG or SHORT;
- do not keep only A or B;
- do not change retest lifetime;
- do not modify stop/TP1 values;
- do not alter costs;
- do not remove unfavorable eras;
- do not relabel cases;
- do not create another replay-interface/visual-format variant from the same question.

EXP-048 is the one permitted disjoint visual-representation replication. If pooled blinded selection fails, close this research path and move to a genuinely different information/process hypothesis.
