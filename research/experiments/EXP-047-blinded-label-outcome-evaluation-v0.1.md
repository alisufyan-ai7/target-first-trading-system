# EXP-047 — Frozen Blinded-Label Outcome Evaluation v0.1

**Status:** FROZEN BEFORE ANY EXP-047 POST-DECISION PATH IS LOADED  
**Date:** 2026-09-28  
**Parent replay protocol:** `e5792f4d5980d288d339a82dc1271981534b7867`  
**Reviewer rubric:** `688f90e8d81eed9dd6098b11f377e4f88e423564`  
**Complete blinded-label checkpoint:** `92837503784151a0596618e36700cdc593068233`

## 1. Authorization

The complete 126-case blinded review was frozen before any post-decision path was opened.

Frozen label result:

- 126 total decisions;
- 77 NO_TRADE;
- 20 LONG;
- 29 SHORT;
- 49 total trade labels;
- 9 confidence A;
- 40 confidence B;
- 38 LEVEL_RETEST;
- 11 MARKET_NEXT_OPEN;
- feasibility gate PASS;
- validation / holdout not loaded;
- post-decision path not loaded;
- target outcomes not evaluated.

Frozen label JSONL SHA-256:

`1bc3ef6cc2491d9a1afcd57512ae6aac78b99f74355948c64ba2808bcd0c9298`.

## 2. Scientific question

EXP-047 is not testing whether the reviewer can explain historical winners after seeing them.

The labels are already sealed.

The question now is:

> Do the 49 outcome-blinded human-style trade selections have positive and reasonably stable post-cost economic value when executed under a prospectively frozen causal simulator?

NO_TRADE cases are not converted into trades after outcomes are revealed.

## 3. Pinned artifacts

The evaluator must abort if any of these Git blobs changes:

- blinded replay packets JSONL blob:
  `e6eeeed45a0e0181b23d0d3ba3497b5521677c41`;
- complete blinded labels JSONL blob:
  `e9bb8b70593e52653adfbfc47606b5b6a1c0e82e`;
- blinded label summary blob:
  `8be2b77c183b7221695c02bc4a6d3c5c237d1c9b`.

The complete label set is immutable for v0.1.

## 4. Data boundary

Outcome-development source:

- warm-up: 2021-12-01 through 2021-12-31;
- evaluated development: 2022-01-01 through 2025-02-28.

Remain sealed and must not be downloaded:

- validation: 2025-03-01 through 2025-08-31;
- fresh holdout: 2025-09-01 through 2026-02-28.

Source remains pinned to:

`kevingtlin/Market-Data-Lab@922f83a60cc574e7395fb27397077288055a1ef6`.

## 5. Execution semantics

All orders become eligible only after the frozen replay decision timestamp.

### MARKET_NEXT_OPEN

- fill at the open of the first market-active M1 bar whose start timestamp is at or after the decision timestamp;
- fill must occur before 18:00 UTC;
- if the actual fill is not strictly between the frozen stop and TP1 in the correct directional order, mark `NO_FILL_MARKET_INVALID_GEOMETRY`.

The label's stored `entryPrice` remains the review-time reference; actual simulated entry is the next-active-M1 open.

### LEVEL_RETEST

- place a limit order at the frozen `entryPrice`;
- activate on the first market-active M1 bar starting at or after decision timestamp;
- order lives for at most **60 market-active M1 bars**;
- order expires at 18:00 UTC even if fewer than 60 active bars elapsed.

Conservative pre-entry ordering:

1. if a bar reaches the frozen structural stop before an accepted fill can be resolved, invalidate the setup;
2. otherwise, if the bar touches the entry, fill at the frozen entry price.

Therefore a bar that touches both stop and entry before fill becomes:

`NO_FILL_PREENTRY_INVALIDATION`.

After a LEVEL_RETEST fill, no TP1 is credited on the fill M1 bar. Post-entry target/stop outcome scanning starts on the next market-active M1 bar. This avoids favorable same-bar ordering assumptions.

No trade label uses FVG_RETRACE or OTHER_CAUSAL_LIMIT in v0.1.

## 6. Frozen stop and target

Use exactly the stop and TP1 frozen in the blinded label.

Do not:

- move the stop;
- substitute a nearer/farther structural level;
- add a trailing stop;
- alter TP1 after observing future candles;
- add TP2 post hoc.

Every filled trade is full-size to one frozen TP1.

## 7. Post-entry same-bar ordering

For MARKET_NEXT_OPEN, the entry occurs at M1 open, so that bar is part of the outcome path.

For any post-entry M1 bar:

- if stop and TP1 are both touched, **stop wins**;
- otherwise exit at the touched stop or TP1.

For LEVEL_RETEST, the fill bar itself cannot credit TP1; the next active M1 begins outcome evaluation.

## 8. Intraday horizon

A filled trade exits at the earliest of:

1. structural stop;
2. frozen TP1;
3. 120 market-active M1 bars after fill;
4. 20:00 UTC on the fill UTC date.

Timeout exit uses the close of the last market-active M1 bar at or before the cutoff.

No overnight positions.

## 9. Costs

Retain the established Gold research convention.

At 0.10 lot:

- primary round-trip friction: USD5;
- stress round-trip friction: USD10.

Scale linearly with actual lot.

These are conservative research assumptions, not claimed broker quotes.

## 10. Reference-account sizing

Reference equity remains USD500.

Gold lot:

- maximum 0.10;
- step 0.01;
- no sizing above 0.10.

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
2. smaller structural risk in USD at 0.10 lot;
3. replay ID lexical order.

A later fill while a position is already open is blocked.

No post-result cohort or direction filtering is permitted in the primary promotion result.

## 12. Daily state

Using primary realized P&L:

- if UTC-day realized P&L <= -USD40, no new position that day;
- if UTC-day realized P&L >= +USD150, no new position that day;
- otherwise later eligible fills may trade if no position is open.

No recovery sizing.

## 13. Predeclared eras

Use the same three replay eras:

- ERA1: 2022-01-01 through 2022-12-31;
- ERA2: 2023-01-01 through 2023-12-31;
- ERA3: 2024-01-01 through 2025-02-28.

No era may be removed after outcomes.

## 14. Primary metrics

Report for the **complete frozen 49-trade-label stream**:

- trade labels;
- filled signals;
- no-fill reasons;
- LONG / SHORT filled counts;
- A / B filled counts;
- stop / TP1 / timeout outcomes;
- gross R expectancy;
- primary R expectancy;
- stress R expectancy;
- primary / stress R profit factor;
- stress expectancy by era;
- stress expectancy by direction as a predeclared stability diagnostic.

Reference-account metrics:

- actual trades;
- blocked one-open;
- blocked daily state;
- lot distribution;
- primary / stress USD expectancy;
- primary / stress PF;
- total primary / stress P&L;
- max primary / stress drawdown;
- distinct trade weekdays;
- daily P&L distribution including zero-trade weekdays;
- >=USD100 / >=USD150 / >=USD200 day percentages;
- losing-day percentage;
- rolling five-day P&L;
- consecutive losing days.

Confidence A and B subgroups may be reported **descriptively only**. They may not rescue a failed pooled result.

## 15. Frozen development gate

EXP-047 advances to sealed validation only if **all** of these pass:

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
16. stress max drawdown <=USD150;
17. validation / holdout remain sealed.

The sample floors are frozen from the already sealed 49 blinded trade labels, not from outcomes.

## 16. Disposition

If all gates pass:

`EXP047_BLINDED_HUMAN_SELECTION_READY_FOR_SEALED_VALIDATION`.

Otherwise:

`EXP047_BLINDED_HUMAN_SELECTION_FAIL_CLOSE_BEFORE_VALIDATION`.

A development PASS authorizes a separately frozen validation protocol only. It does not authorize live trading.

## 17. Anti-mining rule

After the outcome run:

- do not keep only LONG or only SHORT;
- do not keep only confidence A;
- do not change the 60-M1 retest life;
- do not change costs;
- do not change stop/target prices;
- do not remove unfavorable eras;
- do not relabel any of the 126 cases.

If the pooled blinded selection fails, EXP-047 v0.1 is closed as a negative result.

If it passes, the labels/rationales may later be studied to formalize an Engine U, but Engine U must then be frozen and tested independently.
