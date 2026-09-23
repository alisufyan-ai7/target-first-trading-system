# Engine K — Multi-Market Direct Target-Move Scanner v0.1

**Status:** FROZEN PROSPECTIVELY — PRE-OUTCOME CLEANUP AMENDED — 2026-09-23  
**Engine ID:** `engine-k-direct-target-move-scanner`  
**Version:** `0.1`  
**Experiment:** `EXP-022 — Multi-Market Direct Target-Move Scanner v0.1`  
**Outcome status at freeze:** ZERO ENGINE-K OUTCOMES CALCULATED

## 1. Purpose

Engine K directly implements the user's central requirement:

> Continuously scan supported markets and identify where price has the highest validated probability of making an economically useful move in one direction before structural invalidation.

Engine K is intentionally different from Engines G–J.

It does **not** require a named discretionary pattern such as:

- liquidity sweep;
- FVG;
- session-boundary breakout;
- pullback;
- opening range;
- compression box;
- order block;
- Badar-specific setup.

Those may still be useful features or separate engines later.

Engine K itself is a **direct probabilistic market-state engine**.

## 2. Core live logic

Every completed five-minute observation:

1. scan every supported market;
2. construct a long candidate and short candidate where a causal structural stop exists;
3. calculate the candidate's current market-state features;
4. estimate target-first probability for the useful target ladder;
5. calculate economically equivalent position size;
6. reject unsafe candidates;
7. rank all remaining market/direction/target opportunities;
8. take only the highest-quality qualified opportunity or opportunities allowed by portfolio state.

Conceptually:

~~~text
all supported markets
        ->
every 5 minutes
        ->
LONG + SHORT candidate state
        ->
probability of useful move before stop
        ->
economic sizing / risk gate
        ->
cross-market ranking
        ->
trade best qualified opportunity
~~~

This directly replaces the previous habit of testing one handcrafted XAU-only pattern at a time as the primary discovery path.

## 3. Initial supported market universe

Wave 1 uses markets for which clean public one-minute research samples have already been documented in this repository:

- XAUUSD;
- EURUSD;
- GBPUSD;
- USDJPY;
- EURJPY;
- AUDUSD;
- USDCAD;
- USDCHF.

Forecast-only markets with clean pinned one-minute data, pending executable contract economics:

- XAGUSD;
- NAS100;
- US30;
- SPX500.

Wave 2 should add as soon as clean data and economics are documented:

- GBPJPY;
- XAGUSD execution economics;
- NAS100 / US30 / SPX500 execution economics;
- BTCUSD / BTCUSDT;
- other liquid markets with reliable data and executable contract economics.

“Scan all markets” means all markets admitted to the supported universe, not literally every listed instrument regardless of data quality/liquidity.

## 4. Observation frequency and active windows

### FX / metals

Score every completed UTC-aligned active 5m bar.

Initial research window:

`00:00 <= decision time < 20:00 UTC`

on eligible weekdays.

The model receives time-of-day features, so it may learn that certain sessions are better or worse.

No candidate is entered after the market-specific safe-entry cutoff once broker/session mechanics are known.

### Crypto later

24/7 scoring may be used after BTC/crypto is added with its own calendar and cost model.

## 5. Candidate generation

Engine K deliberately generates a broad but causal state universe.

At each 5m decision timestamp, construct at most:

- one long state per market;
- one short state per market.

A direction is structurally admissible only when an opposite-side confirmed 5m pivot exists.

### Pivot definition

Use a non-future-looking 2-left / 2-right 5m pivot.

The pivot is eligible only after both right-side bars are complete.

Maximum pivot age:

- 12 completed active 5m bars = 60 active minutes.

Long:

- stop = latest eligible confirmed 5m swing low - one instrument tick;
- require stop < next-entry price.

Short:

- stop = latest eligible confirmed 5m swing high + one instrument tick;
- require stop > next-entry price.

This is not claimed to be a trading edge. It provides a causal structural invalidation so target-first labels are economically meaningful.

## 6. Entry

Research entry = open of the next active 1m bar after the completed 5m decision bar.

No same-bar entry.

If the next active 1m open is unavailable or outside the permitted market session:

reject.

Pre-outcome cleanup clarification:

- the next-active 1m entry may be at most **5 chronological minutes** after the completed 5m decision bar;
- a candidate may not jump across a long feed/session closure into a later session.

## 7. Gold target ladder

For XAUUSD at the 0.10-lot research anchor:

- G3 = +3.000 XAU favorable move ~= USD30 gross;
- G4 = +4.000 XAU ~= USD40;
- G5 = +5.000 XAU ~= USD50.

Long:

- target = entry + D.

Short:

- target = entry - D.

These are the user's direct 3/4/5-dollar Gold questions.

## 8. Non-Gold movement ladder

Engine K needs a causal equivalent of the Gold 3/4/5-dollar movement burden without copying Gold's lot number.

For v0.1, freeze a **movement-distance ladder**, not a universal lot size.

For each non-Gold market, before each candidate:

1. build completed 1h bars from prior data only;
2. calculate true range for the most recent 20 completed active 1h bars;
3. let `MTR20` = median of those 20 hourly true ranges.

Freeze movement fractions derived from the approximate burden of Gold USD3/USD4/USD5 versus the documented Gold median active hourly range:

- D30 = 0.14 × MTR20;
- D40 = 0.19 × MTR20;
- D50 = 0.23 × MTR20.

These are native price distances.

No holdout-derived target optimization is allowed in v0.1.

This target-distance formula is only for Engine K v0.1.

**Important pre-outcome clarification:** the 0.14 / 0.19 / 0.23 x MTR20 ladder is a prospectively frozen **forecast-label grid**, not a replacement portfolio-sizing doctrine. It is permitted here so the direct scanner can ask the same target-first question across non-Gold markets. A non-Gold rung becomes execution-research eligible only if its P&L-equivalent size passes every stop-risk, notional, margin and cost gate below. Final paper/live promotion still requires a market/engine native target and broker economics consistent with `docs/PNL-EQUIVALENT-SIZING.md`.

## 9. Equivalent position sizing

### XAUUSD

Use fixed research anchor:

- 0.10 lot.

### Non-Gold markets

For each target rung:

- calculate the lot size that makes the target gross approximately USD30 / USD40 / USD50 respectively;
- round downward to the legal research lot step where a convention is documented;
- calculate structural-stop dollar risk at that size.

A target rung is economically admissible only when:

- proposed size is finite/positive;
- structural stop risk <= USD20 for the primary Engine-K v0.1 screen;
- notional/margin diagnostics are available;
- proposed size does not exceed the configured research leverage/notional safety gate.

Why USD20:

- the normal daily loss-stop zone is about USD40;
- a USD20 primary per-trade cap permits two normal full-stop losses without intentionally consuming the entire daily budget in one trade.

The USD60 emergency ceiling is never a sizing allowance.

For XAUUSD at 0.10 lot, the same primary risk gate means structural stop distance <= approximately USD2.00 Gold.

If no target rung is economically admissible, the market-direction state is not execution-eligible, although raw model diagnostics may still be recorded.

### Research transaction-cost convention

Broker-specific spreads/commission are not yet frozen in the repository for all eight execution markets. Engine K therefore uses a **uniform research stress convention**, not a claim about broker pricing:

- primary round-trip cost = **10% of gross target**;
- stress round-trip cost = **20% of gross target**.

Therefore:

| Rung | Gross target | Primary research cost | Stress research cost |
|---|---:|---:|---:|
| T30 | USD30 | USD3 | USD6 |
| T40 | USD40 | USD4 | USD8 |
| T50 | USD50 | USD5 | USD10 |

The primary cost convention preserves the project's established approximately USD5 cost stress at a USD50 objective while applying the same proportional friction standard across markets. Broker-specific cost modeling is mandatory before paper/live promotion.

### Research notional / margin convention

Before broker-specific verification, execution-research rungs must also satisfy:

- reference equity = **USD500**;
- research leverage reference = **1:500**;
- maximum research margin use = **20% of reference equity = USD100**;
- maximum notional/equity = **100x**, therefore maximum notional = **USD50,000**.

These two leverage/notional gates are deliberately equivalent at the frozen 1:500 research reference.

This is a research feasibility screen only. It prevents the small-target / huge-position problem already identified in EXP-006. It does not assert that 1:500 leverage will be available or appropriate live.

### Probability economics

For each execution-research rung define:

`p_BE = (stop_risk_USD + primary_cost_USD) / (target_USD + stop_risk_USD)`.

The required calibrated probability is:

`p_required = max(0.60, p_BE + 0.05)`.

Thus the old 60% floor remains, but a candidate with unfavorable stop/target economics must clear a higher probability threshold rather than qualifying merely because `p >= 0.60`.

## 10. Outcome label

For every direction/target candidate:

**success = target reached before structural stop**

within the frozen horizon.

Horizon:

- maximum 120 active 1m bars after entry;
- or market/session cutoff;
- whichever occurs first.

Same-bar target + stop ambiguity:

- stop wins.

If neither target nor stop is reached by horizon:

- label = no-target;
- horizon-end marked P&L recorded separately.

Independent labels are kept for each target rung.

## 11. Market-state features

Only information known at decision time may be used.

### Directional momentum

For the candidate direction:

1. signed 5m return;
2. signed 15m return;
3. signed 30m return;
4. signed 60m return;
5. signed 120m return.

Normalize by current volatility scale.

### Trend / structure

6. 5m EMA10 minus EMA30, normalized;
7. EMA10 slope;
8. EMA30 slope;
9. distance from entry to 60m high;
10. distance from entry to 60m low;
11. position inside 60m range;
12. position inside 240m range.

### Volatility / regime

13. current 5m true range / recent median 5m TR;
14. last 15m range / last 60m range;
15. last 30m range / last 120m range;
16. current hourly-range percentile versus prior 20 active hours;
17. compression/expansion ratio.

### Candle shape

18. current 5m body/range;
19. upper-wick/range;
20. lower-wick/range;
21. prior three-bar directional body balance.

### Structural risk

22. native stop distance;
23. stop distance / MTR20;
24. dollar stop risk at target-equivalent size.

### Time / identity

25. market identity;
26. direction;
27. UTC hour sine;
28. UTC hour cosine;
29. weekday.

No future bars, post-entry excursion, news result, or holdout outcome may enter features.

### Exact v0.1 feature formulas frozen before outcomes

The implementation in `research/code/engine_k_v0_1.py` freezes the previously qualitative feature descriptions as follows:

- directional moves = signed price change over 5/15/30/60/120m divided by the rolling median of the latest 20 complete 5m true ranges;
- EMA gap = direction-signed EMA10 minus EMA30 divided by the same 5m volatility scale;
- EMA slopes = direction-signed 15m change in EMA10 / EMA30 divided by that scale;
- 60m/240m range-position features use only complete 5m bars through the decision bar;
- 15m/60m and 30m/120m range ratios use completed windows ending at the decision bar;
- hourly-range percentile compares the latest fully completed 1h true range with the **prior** 20 complete 1h true ranges;
- compression/expansion ratio = mean true range of the latest three complete 5m bars divided by median true range of the preceding 12 complete 5m bars;
- candle body/wicks are divided by current complete 5m range;
- prior-three directional body balance = direction-signed sum of candle bodies divided by total range of the same three bars;
- structural stop distance is recorded in native units and divided by causal MTR20;
- target-rung-specific dollar stop risk is the 29th model feature;
- UTC time uses sine/cosine of the completed decision time;
- market identity and direction are explicit categorical inputs.

All 5m feature bars require exactly five 1m observations. All 1h MTR bars require exactly 60 1m observations. Incomplete resample bins are excluded.

## 12. Model

Primary v0.1 execution model:

- pooled multi-market HistGradientBoostingClassifier from scikit-learn;
- fit only on the eight **execution-research markets**: XAUUSD, EURUSD, GBPUSD, USDJPY, EURJPY, AUDUSD, USDCAD and USDCHF;
- XAGUSD, NAS100, US30 and SPX500 are excluded from fitting, calibration, trade ranking and P&L simulation while they remain forecast-only;
- one binary model per target rung;
- market identity and direction encoded prospectively;
- fixed hyperparameters before outcome inspection:

  - learning_rate = 0.05;
  - max_iter = 150;
  - max_leaf_nodes = 15;
  - min_samples_leaf = 100;
  - l2_regularization = 1.0;
  - random_state = 20260923.

Diagnostic baseline:

- L2 logistic regression.

The diagnostic baseline cannot replace the primary model after seeing final holdout merely because it performs better.

A separate 12-market **forecast diagnostic** model may be reported for research, but forecast-only markets may not influence the primary executable model or execution ranking until their contract economics are prospectively frozen.

## 13. Probability calibration

Exact pinned data provenance:

- `research/provenance/EXP-022-wave1-data-manifest.md`.

Training model fit:

- 2026-03-23 through 2026-05-31.

Probability calibration:

- 2026-06-01 through 2026-06-30;
- sigmoid/Platt calibration only.

No threshold tuning on later periods.

## 14. Evaluation periods

The currently pinned rolling public samples share coverage beginning 2026-03-23 and extending through 2026-09-23.

2026-09-23 is excluded because it is a potentially incomplete current UTC day.

### Training

- 2026-03-23 through 2026-05-31.

### Calibration

- 2026-06-01 through 2026-06-30.

### Historical secondary test

- 2026-07-01 through 2026-08-31.

This is not treated as pristine because prior project work touched related 2026 periods.

### Fresh final common-sample holdout

- 2026-09-01 through 2026-09-22.

Do not change model features, model hyperparameters, target fractions, structural stop, or qualification logic after final-holdout inspection.

The Sep-1 through Sep-22 holdout is an **initial common-sample out-of-sample test**, not sufficient evidence by itself for live promotion. Any successful Engine-K v0.1 result must subsequently survive longer-history and/or independent-feed validation plus forward/demo evidence before execution promotion.

## 15. Cross-market ranking

At each timestamp:

1. score every admissible market/direction/target rung;
2. estimate calibrated target-first probability `p`;
3. calculate conservative net EV:

`EV = p * target_USD - (1-p) * stop_risk_USD - estimated_cost_USD`;

4. reject if EV <= 0;
5. rank primarily by calibrated probability, then conservative EV.

Primary qualification:

- calibrated `p >= p_required = max(0.60, p_BE + 0.05)`;
- primary-cost EV > 0;
- structural risk <= USD20;
- notional/equity <=100x;
- research margin at 1:500 <=USD100;
- all other economic/session/data gates pass.

Stress-cost EV under the 20%-of-target friction schedule must also be reported, but is diagnostic rather than an additional v0.1 hard gate.

If no candidate qualifies:

- take no trade.

The 0.60 floor and +5 percentage-point break-even buffer are prospectively frozen for v0.1 and must not be lowered after seeing low trade frequency.

## 16. Portfolio rule for v0.1

For the first test:

- maximum one open Engine-K trade at a time across all markets;
- no forced minimum trades;
- once flat, resume scanning the entire universe immediately;
- stop adding new risk after realized daily P&L <= -USD40;
- normally stop adding new risk after realized daily P&L >= +USD150.

This isolates signal quality before adding simultaneous-position/correlation complexity.

Later versions may admit concurrent independent candidates if v0.1 validates.

## 17. Primary development questions

Engine K v0.1 must answer directly:

1. Across all supported markets, how often does at least one p>=0.60 opportunity exist?
2. What is realized target-first hit rate of qualified trades?
3. Are probabilities calibrated?
4. What is net expectancy after frozen cost assumptions?
5. Which markets contribute qualified opportunities?
6. How many trading days have zero qualified opportunities?
7. How many qualified trades/day occur?
8. Can the multi-market scanner materially reduce low-output days compared with one-market engines?

## 18. Development gate

Before secondary/final test:

- at least 200 economically admissible labeled states per market where possible;
- at least 100 actual qualified simulated trades across the combined training/calibration period OR classify insufficient frequency;
- calibrated qualified-trade hit rate must exceed the break-even requirement under actual stop/target economics;
- combined net expectancy > 0;
- no single market contributes >70% of qualified-trade P&L without being reported as concentration;
- no leakage/optimistic same-bar handling.

Do not invent a parameter grid if the frozen center configuration fails decisively.

## 19. Why this engine exists

The project spent too long asking whether one handcrafted Gold pattern could be made profitable.

Engine K asks the user's actual question directly:

> Right now, across all supported markets, which direction has the highest validated probability of making a useful move before invalidation?

This is the primary new discovery path.


## 27. Pre-outcome cleanup checkpoint

Before any Engine-K target labels or model performance were calculated, v0.1 was cleaned up to remove ambiguities:

1. execution universe fixed at 8 markets;
2. forecast-only universe fixed at XAGUSD, NAS100, US30 and SPX500;
3. forecast-only markets prohibited from influencing the executable pooled model;
4. one authoritative train/calibration/secondary/final-holdout split retained;
5. incomplete 5m/1h resample bins excluded;
6. next-entry gap capped at five chronological minutes;
7. all 29 causal model features defined explicitly;
8. research primary/stress transaction-cost conventions frozen;
9. stop-risk, notional and research-margin gates frozen;
10. probability qualification tied to both the 60% floor and break-even economics;
11. final September holdout classified as an initial OOS test, not sufficient live-promotion evidence.

**Engine-K target outcomes calculated at this checkpoint: NO.**  
**Engine-K model outcomes calculated at this checkpoint: NO.**
