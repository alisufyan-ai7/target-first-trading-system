# EXP-014 — Target-First Opportunity Ranker v0.1

**Status:** IN PROGRESS — CANDIDATE, FEATURE, MODEL, AND SPLIT RULES FROZEN BEFORE OUTCOME INSPECTION  
**Date:** 2026-09-22

## Purpose

Build the first actual cross-market opportunity-ranking layer for the intended trading system.

Rather than forcing one fixed strategy/target, EXP-014 will:

1. enumerate structurally valid long and short candidates across the frozen scanner universe;
2. calculate fixed-size structural-stop dollar risk;
3. reject candidates that do not fit the fixed-size risk framework;
4. estimate the probability of reaching each useful dollar-profit rung before structural invalidation;
5. rank candidates across markets by conservative expected dollar value.

This is a first research implementation of the intended live scanner architecture.

## Frozen first scanner universe

Selected in EXP-013 from development-only movement economics:

1. XAUUSD;
2. GBPUSD;
3. USDCHF;
4. EURUSD;
5. AUDUSD.

Fixed execution sizes:

- XAUUSD: 0.10 lot / 10 oz research convention;
- FX: 0.10 standard lot / 10,000 base units.

Broker-specific contract verification remains required before execution.

## Candidate enumeration

Candidates are generated every 5 minutes during:

- 06:00 <= UTC < 18:00.

Entry time:

- open of the first 1m bar immediately after the completed 5m decision bar.

### Structural long candidate

At decision time:

1. identify the most recent confirmed 1m swing low using a non-future-looking 2-left / 2-right pivot;
2. pivot must already be confirmed;
3. pivot bar must be no older than 15 completed minutes;
4. entry = next 1m open;
5. structural stop = pivot low;
6. stop must be below entry.

### Structural short candidate

Mirror image using the most recent confirmed 1m swing high:

- stop = pivot high;
- stop must be above entry.

No stop compression is permitted.

### Candidate cooldown

To reduce nearly duplicate overlapping observations:

- maximum one new candidate per direction per instrument every 15 minutes.

Long and short candidates may both exist when their independent structural conditions are valid.

The model, not a hard-coded directional rule, will determine which candidate is attractive.

## Fixed-size structural-risk gate

Before labeling/modeling a candidate, calculate full stop loss at the fixed execution size.

Candidate is admissible only if:

- stop-dollar risk > 0; and
- stop-dollar risk <= USD 40.

No lot reduction is used to rescue a wider stop.

This implements the existing normal daily loss framework at the individual-opportunity gate.

## Target ladder

For each admissible candidate label whether the following gross-profit level occurs before structural stop:

- T30 = +USD 30;
- T40 = +USD 40;
- T50 = +USD 50;
- T70 = +USD 70;
- T100 = +USD 100.

Outcome horizon:

- earliest of structural stop, target hit, 120 minutes after entry, or 20:00 UTC.

Same-bar target and stop ambiguity:

- count stop first.

Each target label is binary.

Also record:

- maximum favorable excursion;
- maximum adverse excursion;
- time to target/stop;
- horizon-end marked P&L.

## Fixed-size P&L translation

### XAUUSD

Using 10 oz:

- USD P&L = 10 x favorable/adverse XAU price move.

### GBPUSD / EURUSD / AUDUSD

At 10,000 base units and USD quote:

- approximately USD 1 per pip.

### USDCHF

At 10,000 USD base units:

- pip P&L is approximately 1 CHF/pip;
- convert to USD at the contemporaneous USDCHF price.

Exact per-candidate conversion is used rather than a fixed development median.

## Frozen feature set

Only information available at or before entry may be used.

Continuous features:

1. structural stop risk in USD;
2. 5m ATR(14) translated to fixed-size USD movement capacity;
3. 60m high-low range translated to fixed-size USD capacity;
4. current 5m real-body / ATR ratio;
5. signed 15m return in the candidate direction, normalized by 5m ATR;
6. signed 60m return in the candidate direction, normalized by 5m ATR;
7. distance from entry to 60m high, normalized by ATR;
8. distance from entry to 60m low, normalized by ATR.

Categorical/encoded features:

9. candidate direction;
10. market identity;
11. UTC hour represented by sine/cosine transformation.

No volume, news, future bars, post-entry excursion, or holdout-derived feature is permitted.

## Model

For each target rung independently:

- logistic regression;
- L2 regularization;
- regularization coefficient fixed at 1.0;
- continuous features standardized using training-set mean/std only;
- market identity one-hot encoded;
- no feature selection after seeing outcomes.

Probability monotonicity post-processing:

- enforce P(T30) >= P(T40) >= P(T50) >= P(T70) >= P(T100)
  by cumulative minimum from lower to higher targets.

## Conservative target value

For each target rung D, calculate a conservative gross expected value:

`EV_D = P(TD) * D - (1 - P(TD)) * stop_risk_USD`

This assumes every non-target outcome loses the full structural stop, making the ranking intentionally conservative.

For each candidate:

- choose the target rung with the highest positive conservative EV;
- if no rung has positive conservative EV, candidate is not qualified;
- ties prefer the lower target rung.

This rule is frozen before holdout testing.

## Time split

Because prior experiments have already inspected June–August aggregate outcomes on several markets, EXP-014 creates a new split.

### Training

- 2026-03-12 through 2026-04-30.

### Calibration / development check

- 2026-05-01 through 2026-05-31.

No model hyperparameter tuning is permitted. Calibration is used to check probability quality and gross EV behavior.

### Historical secondary test

- 2026-06-01 through 2026-08-20.

This period is **not considered pristine** because prior project experiments inspected market outcomes here.

### Fresh final holdout

- 2026-08-21 through the last common available sample date, expected around 2026-09-11.

No EXP-014 model coefficient, feature, threshold, or target rule may be changed after fresh-holdout outcomes are inspected.

## Model diagnostics

For each target rung and split:

- candidate count;
- base target-first hit rate;
- logistic coefficient stability;
- Brier score;
- log loss;
- calibration by probability bucket where sample permits;
- ROC AUC as a secondary discrimination metric;
- predicted-vs-realized target rate.

## Scanner simulation

After model coefficients are frozen from training/calibration:

At every candidate timestamp:

1. score all admissible market/direction candidates;
2. calculate best positive conservative EV target;
3. rank candidates by conservative EV;
4. accept candidates subject to:
   - maximum one open position per instrument;
   - aggregate nominal structural stop-risk <= USD 40;
   - no new entry after realized daily P&L <= -USD 40;
   - emergency hard-loss tracking at -USD 60;
   - normally stop adding new positions after realized daily P&L >= +USD 150;
5. no fixed daily trade-count cap;
6. no forced minimum trades.

Correlation control is deferred to a later version; EXP-014 will report simultaneous market clustering rather than invent a correlation threshold.

## Required portfolio metrics

- trades/day including zero days;
- mean/median daily P&L;
- losing-day percentage;
- <= USD 50 days;
- >= USD 100 days;
- >= USD 150 days;
- >= USD 200 days;
- maximum daily loss;
- maximum drawdown;
- consecutive losing days;
- consecutive <= USD 50 days;
- contribution by market;
- contribution by target rung;
- average predicted probability and realized hit rate;
- maximum simultaneous stop risk.

## Checkpoint discipline

Run in small stages:

1. verify XAUUSD candidate enumeration and label prevalence on training/calibration only;
2. checkpoint;
3. verify the four FX candidate streams on training/calibration only;
4. checkpoint;
5. fit and freeze model coefficients;
6. checkpoint;
7. run historical secondary test;
8. checkpoint;
9. run fresh final holdout once;
10. checkpoint before any further model revision.

## Promotion rule

EXP-014 is not execution-ready merely for positive historical P&L.

A useful result must show:

- calibrated target probabilities;
- positive gross expectancy in training/calibration;
- no collapse in the secondary test;
- encouraging fresh-holdout evidence;
- fixed-size risk compatibility;
- useful daily distribution;
- no hidden dependence on one isolated market/regime.

Independent-feed and broker-cost validation remain mandatory before paper/live execution.

## Immediate next action

Run Stage 1 only:

- enumerate XAUUSD candidates;
- apply <= USD 40 stop-risk gate;
- calculate T30/T40/T50/T70/T100 prevalence;
- use training + May calibration only;
- do not inspect June–September EXP-014 outcomes yet.

## Stage 1 checkpoint — XAUUSD candidate enumeration and label prevalence

**Status:** COMPLETE — TRAINING + MAY CALIBRATION ONLY; JUNE–SEPTEMBER EXP-014 OUTCOMES NOT INSPECTED

### Implementation correction before checkpoint

An initial scratch pass applied the 15-minute per-direction cooldown only after the USD 40 risk gate.

That was inconsistent with the frozen specification, which defines the cooldown at **candidate enumeration**.

The result below is from the corrected implementation:

1. structural candidate is identified;
2. 15-minute per-direction cooldown is applied immediately;
3. fixed-size stop-dollar risk is calculated;
4. candidate is retained only if 0 < stop risk <= USD 40.

No result from the incorrect scratch pass is used.

### Data

- XAUUSD external public 1m research sample;
- source: `getdata-finance/xauusd-1m-ohlcv-metals-historical-data`;
- used only 2026-03-12 through 2026-05-31 for Stage 1;
- one-minute rows: 76,855;
- resampled 5m bars: 15,378.

### Structural/cooldown funnel

Across training + May calibration:

- structurally eligible long observations before cooldown: 7,779;
- structurally eligible short observations before cooldown: 7,804;
- long observations suppressed by 15-minute cooldown: 5,120;
- short observations suppressed by 15-minute cooldown: 5,148;
- candidates rejected by fixed 0.10-lot stop risk > USD 40: 2,300;
- candidates rejected because pivot stop was not on the invalidation side of entry: 831;
- final admissible labeled candidates: **2,184**.

This candidate set is intentionally broad. It is a training universe for probability ranking, not a trade list.

### Training — 2026-03-12 through 2026-04-30

- candidates: **1,225**;
- long: 617;
- short: 608;
- candidate days: 35;
- candidates per candidate day: 35.00;
- median stop risk: **USD 21.70**;
- mean stop risk: USD 21.40;
- 75th percentile stop risk: USD 30.70;
- 90th percentile stop risk: USD 36.30.

Target-first base rates:

| Target | Hits | Hit rate | Median time to hit |
|---|---:|---:|---:|
| T30 | 466 | **38.04%** | 2 min |
| T40 | 396 | **32.33%** | 3 min |
| T50 | 343 | **28.00%** | 5 min |
| T70 | 253 | **20.65%** | 8 min |
| T100 | 187 | **15.27%** | 12 min |

### May calibration — 2026-05-01 through 2026-05-31

- candidates: **959**;
- long: 473;
- short: 486;
- candidate days: 21;
- candidates per candidate day: 45.67;
- median stop risk: **USD 21.10**;
- mean stop risk: USD 20.95;
- 75th percentile stop risk: USD 30.40;
- 90th percentile stop risk: USD 36.02.

Target-first base rates:

| Target | Hits | Hit rate | Median time to hit |
|---|---:|---:|---:|
| T30 | 373 | **38.89%** | 3 min |
| T40 | 324 | **33.79%** | 5 min |
| T50 | 284 | **29.61%** | 6 min |
| T70 | 232 | **24.19%** | 12 min |
| T100 | 175 | **18.25%** | 22 min |

### Training-to-calibration stability observation

The broad XAU structural candidate base rates did **not** collapse from training into May calibration:

- T30: 38.04% -> 38.89%;
- T40: 32.33% -> 33.79%;
- T50: 28.00% -> 29.61%;
- T70: 20.65% -> 24.19%;
- T100: 15.27% -> 18.25%.

This is not evidence that the frozen feature model will discriminate profitable opportunities. It only establishes that:

1. there is ample candidate volume for model fitting;
2. direction is balanced;
3. stop-risk distribution is similar across training/calibration;
4. target-label prevalence is reasonably stable over the pre-holdout development period.

### Important interpretation

The candidate frequency is intentionally much higher than the desired trade frequency.

EXP-014 does **not** intend to trade every structural candidate. The ranker must reject most candidates unless their predicted target-first probability creates positive conservative EV after the fixed-size structural risk is considered.

### Next stage

Proceed to Stage 2 only:

- enumerate GBPUSD, USDCHF, EURUSD, and AUDUSD candidates;
- use the same frozen structural/cooldown/risk/label rules;
- inspect training + May calibration only;
- checkpoint the four FX streams before model fitting.

