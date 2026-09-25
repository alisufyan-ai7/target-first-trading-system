# Brainstorming Synthesis — Information Advantage, Human Process, Timeframes, and Compounding

**Date:** 2026-09-25  
**Status:** DURABLE RESEARCH CONTEXT — NOT A TRADING STRATEGY  
**Protected-period status:** Jul-Aug secondary and Sep final holdout remain sealed

## Why this synthesis exists

This document preserves the material reasoning developed after the Engine Q failure and during the root-cause discussion, including the useful abstractions from user-supplied trading screenshots.

It is deliberately not a new strategy specification.

## 1. Core root-cause conclusion

Recent strategy families changed formulas more often than they changed the underlying information source.

Most relied primarily on:

- recent OHLC price state;
- price-derived momentum/volatility;
- price-derived structure;
- cross-market price relationships.

The repeated near-zero gross edge suggests the main problem is not “we have not found the right candle formula yet.”

The next research question is:

> what information available to a skilled intraday trader is absent from our present dataset, and does it add stable predictive information beyond OHLC?

## 2. What “information advantage” means in this project

Before creating another strategy rule, compare predictive information layers.

Example sequence:

`price-only baseline`
    ->
`+ multi-timeframe structure/location`
    ->
`+ session/liquidity context`
    ->
`+ macro surprise/catalyst`
    ->
`+ rates/USD interpretation`
    ->
`+ order flow / market depth / spread`

The purpose is not to assume the richest layer wins.

The purpose is to measure whether each added layer improves out-of-sample target-before-stop probability, calibration, and economic usefulness.

Only information sources that add stable incremental value should later be wrapped in an execution engine.

## 3. Human trading process hypothesis

A skilled discretionary trader may be doing something closer to:

`market specialization`
    ->
`higher-timeframe regime/location`
    ->
`intraday structure`
    ->
`session/catalyst state`
    ->
`participation/order-flow confirmation`
    ->
`lower-timeframe trigger`
    ->
`non-chasing execution`
    ->
`structural stop`
    ->
`target ladder / partials / runner`

rather than:

`one indicator/pattern -> trade`.

This is a hypothesis to decompose and test causally.

## 4. Useful lesson from the supplied timeframe screenshots

The useful concept is **division of labor across timeframes**, not the claim that any single timeframe is universally “best.”

Working research interpretation:

- Daily / 4H: regime and major location;
- 1H: intraday directional/context state;
- 15M: setup area / structural opportunity;
- 5M: confirmation and local structure;
- 1M: execution refinement only when needed.

This extends the existing repository interpretation in `docs/TIMEFRAME-AND-MARKET-CONTEXT.md`.

Important:

- Monthly/weekly may matter for some instruments, but the current intraday study should not force them into the model without enough history.
- The first information-content experiment should test whether 15M/1H/4H/Daily context adds information beyond local M5 price state.

## 5. Useful lesson from the “master one pair” screenshot

The social-media claims about which pair/session “works” are not accepted as facts.

The useful abstraction is **specialization**.

The final system can remain multi-market while individual engines are mechanism-specific.

Possible future architecture:

- Gold macro/liquidity/COMEX engine;
- FX macro/order-flow engine;
- other specialized engines only when supported by evidence;
- all emit standardized candidates;
- cross-market ranker chooses among validated candidates.

Do not require every engine to work equally on every market.

Do not rescue failed engines by post-hoc symbol selection.

## 6. Useful lesson from the tools/resources screenshot

Most listed tools are operational or educational rather than alpha sources.

The important research clue is the **economic calendar / news layer**.

Human traders commonly know whether a major release is occurring.

Future structured catalyst data should ideally include:

- event type;
- exact timestamp;
- actual;
- consensus;
- prior/revised;
- standardized surprise;
- rates/USD reaction;
- order-flow reaction.

A screenshot mentioning a calendar does not validate a news strategy; it identifies a missing information category.

## 7. Lot-size screenshot: concept useful, numbers not governing

The screenshot mapping account balance directly to lot size is **not** adopted.

Lot size cannot be determined from equity alone.

Correct sizing depends on:

- current equity;
- instrument contract/tick value;
- structural stop distance;
- allowable dollar risk;
- leverage/margin;
- open correlated exposure;
- remaining daily loss budget;
- broker lot step/min/max.

The existing `docs/PNL-EQUIVALENT-SIZING.md` remains governing.

The screenshot is useful only for the broad idea that as account equity changes, safe absolute position size may change.

## 8. Compounding / withdrawals

USD500 is the starting/reference equity, not necessarily permanent equity.

If the system becomes profitable and the user withdraws a portion of weekly profit while retaining the remainder, the account can compound.

Future production sizing should therefore be **equity-adaptive**.

Conceptual flow:

`actual current equity`
    ->
`risk limits as a function of validated edge and drawdown policy`
    ->
`structural stop`
    ->
`safe lot / margin / notional`
    ->
`daily and correlation gates`.

Compounding does not solve an unprofitable strategy.

Sequence remains:

1. establish positive robust post-cost edge;
2. validate risk/drawdown;
3. define equity-adaptive sizing;
4. compound retained profits;
5. withdrawals reduce the equity base used for subsequent sizing.

The strong-day dollar target becomes less demanding as equity grows:

- USD150 on USD500 = 30%;
- USD150 on USD1,000 = 15%;
- USD150 on USD2,000 = 7.5%;
- USD150 on USD5,000 = 3%.

This improves long-term feasibility but does not justify unsafe starting-account risk.

## 9. Risk/reward lesson

Reward/risk is not an edge by itself.

A high R target only helps if target-first probability remains high enough after costs.

Future research should treat reward/risk as an output of:

- entry;
- structural invalidation;
- available structural room;
- target-first probability;
- costs;
- path/runner behavior.

Do not force a fixed R ratio before knowing the target path.

## 10. Target-ladder lesson

Recent development was often reduced to T40.

The final architecture requires richer path information:

- T30;
- T40;
- T50;
- T70;
- T100;
- MFE;
- MAE;
- time to target;
- partial/runner continuation probability;
- opposing-liquidity/structural room.

For the first information-content study, a normalized structural-risk ladder may be used diagnostically so the comparison is target/path focused but independent of arbitrary lot size.

Any mapping from diagnostic R thresholds to production USD targets must remain separate from validated engine-conditioned target/sizing logic.

## 11. Non-chasing execution lesson

Engine Q v0.2 showed a material improvement over matched immediate entry.

Preserve as an architectural clue:

> information/selection first, non-chasing execution second.

Do not conclude that a better limit entry can rescue a weak predictor.

## 12. Meta-overfitting warning

The project has tried many engine families on overlapping development history.

Future work must reduce researcher-level data snooping.

Rules:

- freeze information-content comparisons before outcomes;
- prefer nested feature-family tests over many setup thresholds;
- use chronological fit/calibration/evaluation folds;
- use purge/embargo around label horizons;
- record all attempted feature families;
- do not inspect Jul-Aug or Sep until governing gates permit;
- later obtain independent-feed / forward-demo evidence.

## 13. Immediate research sequence

The current agreed sequence is:

### Step 1 — Multi-Timeframe Structural Context Information-Content Study

Development data only.

Compare:

- A: local M5 price state;
- B: A + 15M context;
- C: B + 1H context;
- D: C + 4H / prior-day location;
- E: D + causal session-location features where available.

Evaluate whether added context improves out-of-sample target/path prediction.

### Step 2 — Catalyst/macro information

Only after Step 1 is checkpointed.

### Step 3 — rates/USD interpretation

### Step 4 — execution-grade microstructure/order flow

COMEX Gold and representative FX flow are highest-priority external sources.

### Step 5 — build a specialized engine only if an information family demonstrates stable incremental value

## 14. Engine R status

Engine R / EXP-039 remains a frozen research artifact.

It is paused before target/P&L development while the information-advantage program is active.

A zero-outcome frequency result does not override this pause.

## Bottom line

The project is moving from:

> strategy-first research

to:

> information-first research -> validated context -> strategy construction.

This is the main conceptual correction from the recent brainstorming.
