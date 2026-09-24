# Root-Cause / Edge-Source Audit v0.1

**Date:** 2026-09-25  
**Status:** RESEARCH CHECKPOINT — NO NEW STRATEGY OUTCOME  
**Scope:** repository evidence through Engine Q / EXP-038 plus public market-microstructure/day-trading research  
**Protected-period policy:** Jul-Aug secondary and Sep final holdout remain sealed  
**Engine-R policy:** EXP-039 is not advanced to development during this audit; no EXP-039 target/P&L result is used to select or tune the audit conclusions

## Executive conclusion

The project should pause the loop of inventing another OHLC-derived engine whenever the prior one fails.

The repeated failures are not primarily caused by insufficient trade frequency, position size, or the choice between trend and mean reversion. The dominant evidence points to a more fundamental problem:

> the system has been asking low-information OHLC-derived states to support high-selectivity, high-economic-output intraday decisions.

Recent engines differ mathematically, but most are transformations of the same underlying information source: recent price bars. The best recent reproducible result, Engine Q v0.2, improved execution materially but still produced only +0.09479R gross expectancy, below the frozen >+0.20R hurdle and negative after costs.

The next research objective is therefore **not another setup family**. It is to establish which information sources contain stable incremental intraday predictive information before designing the next execution engine.

## 1. What the repository evidence says

### 1.1 Recent reproducible price-derived engines do not contain enough raw edge

Representative frozen development results:

| Experiment | Engine | Signals | Gross R expectancy | Primary R | Stress R | Stress-positive folds |
|---|---|---:|---:|---:|---:|---:|
| EXP-028 | M v0.2 | 1,249 | +0.03668R | -0.16248R | -0.36164R | 0 |
| EXP-031 | M v0.5 | 329 | -0.00994R | -0.20629R | -0.40265R | 0 |
| EXP-033 | N v0.2 | 505 | +0.04112R | -0.14504R | -0.33120R | 1 |
| EXP-035 | O v0.2 | 430 | -0.07187R | -0.26113R | -0.45039R | 0 |
| EXP-036 | P v0.1 | 4,804 | -0.04065R | -0.23568R | -0.43072R | 0 |
| EXP-038 | Q v0.2 | 363 | **+0.09479R** | -0.09022R | -0.27524R | 1 |

The pattern matters more than any one failure:

- very high opportunity density did not help P;
- changing trend/reversion/spillover hypotheses did not create a stable edge;
- the primary cost drag has generally been roughly 0.18-0.20R/trade;
- therefore the project's >+0.20R gross hurdle is economically meaningful rather than arbitrary;
- no recent reproducible price-derived engine has reached it.

### 1.2 Q isolated an execution lesson

EXP-038's matched immediate-entry control had approximately:

- gross -0.01903R;
- primary -0.19558R;
- stress -0.37213R.

The actual 50% non-chasing entry had:

- gross +0.09479R;
- primary -0.09022R;
- stress -0.27524R.

So non-chasing execution improved gross expectancy by roughly **+0.114R** versus the matched immediate control.

This is valuable. Entry quality is real.

But execution did not manufacture enough predictive edge. The predictor still failed the +0.20R raw-edge hurdle.

**Research consequence:** preserve non-chasing execution as an architectural component, but stop treating execution refinement as a substitute for an information advantage.

### 1.3 Frequency and edge are different problems

Engine Q v0.1 generated only 56 zero-outcome fills because same-bar four-peer volatility synchronization was too sparse.

Q v0.2 changed the causal temporal sampling to a 15-minute rolling shock memory and produced 467 zero-outcome fills. It solved opportunity density.

Development still failed.

Engine P generated 4,804 signals and was negative gross.

Therefore:

> opportunity density can be engineered, but density does not create predictive edge.

Future preflight gates should continue to protect against tiny samples, but strategy design must be driven by an economic information mechanism first, not by the desire to reach a signal quota.

## 2. What happened to the historical positive Engine A clue

EXP-002 remains important but must be interpreted correctly.

The exploratory Gold screen reported roughly:

- 372 signals;
- T5 target-first hit rate 29.6%;
- average structural risk about USD 1.02 Gold;
- median MFE about USD 3.30 Gold;
- simplified pre-cost price expectancy about +USD 0.79 Gold/trade.

The recorded sequence was:

`liquidity -> sweep -> internal MSS -> displacement -> FVG -> retracement -> tight structural stop -> target expansion`.

However, EXP-014's frozen A1-A9 reconstruction program could not reproduce the result honestly.

A6 recovered approximately the frequency and average-risk dimensions:

- 333 trades;
- development/holdout counts inside or very near frozen bands;
- average structural risk 1.053 Gold.

But quality remained far below the EXP-002 record:

- overall T5 15.02%;
- holdout T5 13.61%;
- holdout T2/T3/T4 23.08% / 21.30% / 16.57%;
- overall expectancy -0.023 Gold/trade.

Even the deliberately optimistic/non-deployable A9 assumption improved holdout expectancy only to about +0.251 Gold/trade and still failed the frozen benchmark.

This gives two plausible explanations, neither of which permits blindly restoring EXP-002:

1. the original exploratory implementation contained important contextual/selection/path mechanics that were not preserved; and/or
2. the original exploratory result benefited from implementation/path-ordering artifacts that cannot be reproduced causally.

The strongest useful clue is not the exact historical performance number. It is the **rich decision sequence** and the surviving human evidence: meaningful location, liquidity event, internal shift, displacement, FVG/retracement, structural stop, staged target/runner management, plus session/news/DXY context.

## 3. The missing-information diagnosis

### 3.1 Current engines mostly observe price observing price

The generic causal feature stack in the repository uses:

- recent returns;
- EMAs/slopes;
- range location;
- true-range/compression measures;
- wick/body geometry;
- recent pivots;
- time/day/market identity;
- structural stop distance.

The source CSVs contain a volume column, but the current generic feature stack does not use execution-grade signed order flow, bid/ask spread, order-book imbalance, depth, trades-at-bid/ask, macro surprise, rates reaction, or broker execution state.

Engines P/Q add cross-market price transforms, but still use price-derived information.

This is consistent with the external evidence:

- Evans & Lyons show that order flow can contain exchange-rate information missing from conventional macro-only models.
- Federal Reserve EBS research documents a substantial association between high-frequency FX returns and interdealer order flow from one minute upward, with important intraday variation.
- Petrova, Vilhelmsson & Nordén (International Journal of Forecasting, 2026) find generally low short-horizon FX predictability and limited incremental value from cross-currency variables, while some microstructure variables such as order flow retain short-term predictive power.
- Love & Payne show that macro news is transmitted both directly and indirectly through order flow.

That is unusually aligned with our internal evidence:

- cross-market directional price consensus P: failed;
- cross-market volatility-price spillover Q: improved but insufficient;
- execution quality mattered;
- the missing layer may be **who is actually trading, with what urgency, around what information event and liquidity condition**.

### 3.2 A skilled human's visible candle pattern is probably not the entire edge

The Badar evidence preserved in the repository repeatedly points to:

- larger-timeframe context/location;
- meaningful liquidity;
- lower-timeframe execution;
- London/New York timing;
- news awareness;
- sometimes DXY/fundamental context;
- later material discussing volume/VSA/open interest;
- partial targets and runners.

A mechanical system that copies only `sweep -> MSS -> FVG` but lacks the trader's **skip logic** can trade many visually similar but economically different events.

The missing question is often not "did an FVG occur?"

It is:

> why is this location/event worth trading now, and is real participation confirming it?

## 4. Daily-economic feasibility: $150-$200 on $500

The desired strong-day zone is 30%-40% of the reference equity in one day.

That can happen on exceptional leveraged days. It is not a reasonable unconditional daily expectation under a low-drawdown small-account framework.

### 4.1 Current non-Gold research payoff geometry

Current v0.2 non-Gold target geometry is:

- T30 = 1.5R;
- T40 = 2.0R;
- T50 = 2.5R.

Primary research cost is 10% of gross target and is charged in the target-first label economics.

For a target multiple m and structural risk D:

- net winner ~= `0.9 * m * D`;
- full-stop outcome ~= `-(1 + 0.1m) * D`;
- break-even win probability ~= `(1 + 0.1m)/(1+m)`.

Illustrative break-even rates:

| Target | Gross reward/risk | Primary-cost break-even hit rate |
|---|---:|---:|
| T30 | 1.5R | 46.0% |
| T40 | 2.0R | 40.0% |
| T50 | 2.5R | 35.7% |
| 3R | 3.0R | 32.5% |
| 4R | 4.0R | 28.0% |

For XAUUSD the dollar target is fixed by Gold price distance, so its actual R multiple depends on the structural stop and must be evaluated per trade.

### 4.2 Why increasing risk is not the root fix

With USD20 structural risk and a 2R target:

- net target ~= +USD36;
- full stop ~= -USD24;
- four perfect target hits ~= **USD144**.

So four ordinary T40 wins cannot even reach the lower USD150 strong-day bound under the simplified primary-cost model.

At USD20 risk and 2.5R:

- win ~= +USD45;
- stop ~= -USD25;
- four perfect wins = USD180;
- to **average** USD150 from exactly four independent trades would require about an 89.3% hit rate;
- with six trades the required hit rate is still about 71.4%.

At USD20 risk and 3R:

- win ~= +USD54;
- stop ~= -USD26;
- four trades require about 79.4% hit probability to average USD150;
- six require about 63.8%.

Increasing risk makes the daily arithmetic easier but collides with the existing loss framework.

At USD30 risk and 3R:

- win ~= +USD81;
- stop ~= -USD39;
- one stop almost consumes the normal -USD40 daily risk limit;
- four trades require about a 63.8% hit rate to average USD150.

At USD40 risk and 3R:

- win ~= +USD108;
- stop ~= -USD52;
- one full stop exceeds the normal -USD40 stop-adding-risk threshold and approaches the -USD60 emergency ceiling.

Therefore:

> position sizing can scale a positive edge; it cannot create one, and scaling risk enough to force the daily objective would break the current risk architecture.

No risk increase should be researched for live use until a positive, stable post-cost edge exists.

### 4.3 Daily target must remain a conditional state, not a quota

The repo already says this correctly: +USD150-$200 is a desired strong-day zone **when sufficient qualified opportunity exists**.

The audit strengthens that interpretation.

Future validation should report the full distribution:

- expected daily P&L;
- median;
- losing-day probability;
- P(>=50), P(>=100), P(>=150), P(>=200);
- drawdown/risk-of-ruin;
- opportunity count and correlation.

The system should not be designed backward to guarantee USD150 every day.

## 5. The T40-only development abstraction is too narrow

The repository objective requires T30/T40/T50/T70/T100 target-first probabilities.

Recent engine development has mostly reduced validation to one T40 binary outcome.

That is useful for a clean gate, but it can distort strategy design.

The human evidence supports:

- nearer partial capture;
- larger runners when structural room exists;
- opposing liquidity as target context;
- variable reward/risk as an **output** of location, stop and available path.

The correct future abstraction is a conditional target surface:

`P(T30 before stop), P(T40 before stop), P(T50 before stop), P(T70 before stop), P(T100 before stop)`

plus:

- MFE/MAE distribution;
- time-to-target;
- structural room/opposing liquidity;
- realistic cost/slippage;
- expected value by target/management rule.

The strategy should not be forced to make every valid event a T40 trade.

## 6. Universal engine versus specialized engine

The system should remain multi-market, but each engine does not need to be universal.

Requiring one mechanism to produce a balanced sample across Gold, EURUSD, USDJPY, AUDUSD, USDCAD, etc. can force the wrong level of generality.

A better architecture is:

- Gold macro/liquidity/microstructure engine when its mechanism is economically relevant;
- FX macro/order-flow engine where centralized/representative flow is available;
- non-news liquidity/absorption engine for genuinely different conditions;
- all engines emit the same candidate contract;
- the cross-market ranker compares only validated candidates.

This must be prospective.

Do **not** rescue failed engines by selecting the markets/hours/directions that happened to look good after outcomes.

## 7. Data realism is now a gating issue

Current public M1 OHLC research data are sufficient for causal bar-pattern research but are not execution-grade enough for the next phase.

Missing or weakly represented inputs include:

- historical bid/ask spread;
- transaction direction;
- top-of-book/depth;
- order additions/cancellations;
- order-flow imbalance;
- queue/liquidity depletion;
- broker-specific tick path and execution;
- macro actual-vs-consensus surprise;
- rates/futures reaction around macro events.

CME DataMine documents historical Market-by-Order, market-depth and trade data, and EBS Spot FX is available among its cash-market datasets. CME Market Depth files contain messages needed to recreate the futures order book with millisecond timestamps. These are plausible research-data sources for COMEX Gold and CME FX futures, subject to licensing/cost.

For production, broker-specific MT5/tick/spread data remain necessary for final execution validation.

## 8. External evidence on where short-horizon information may exist

### FX microstructure

**Evans & Lyons, Order Flow and Exchange Rate Dynamics (NBER 7317 / JPE 2002)**  
https://www.nber.org/papers/w7317

Order flow is modeled as an information-bearing proximate determinant of price and improved short-horizon forecasting in their historical DM/USD sample.

**Berger et al., Federal Reserve, Order Flow and Exchange Rate Dynamics in Electronic Brokerage System Data**  
https://www.federalreserve.gov/econres/ifdp/order-flow-and-exchange-rate-dynamics-in-electronic-brokerage-system-data.htm

Using six years of one-minute EBS EUR/USD and USD/JPY data, the authors document substantial high-frequency association between interdealer order flow and exchange-rate returns, with intraday variation.

**Petrova, Vilhelmsson & Nordén, International Journal of Forecasting 42(3), 2026**  
DOI: 10.1016/j.ijforecast.2025.12.007

The study finds generally low one-minute-to-one-hour FX predictability and limited extra value from cross-currency variables, but some microstructure/order-flow variables have short-horizon predictive power.

### Macro news and order flow

**Love & Payne, Journal of Financial Economics 88(1), 2008**  
DOI: 10.1016/j.jfineco.2007.06.001

Macro news affects FX both directly and through trading/order flow; order-flow effects become more important around news arrival.

### Gold

**Smales & Yang, International Review of Financial Analysis 41, 2015**  
DOI: 10.1016/j.irfa.2015.01.017

COMEX Gold futures returns, volatility and volume react quickly to macro announcements; unemployment and GDP surprises were among the strongest in their sample, and much of the reaction occurred rapidly.

### Short-horizon order-book evidence beyond FX

**Cont, Kukanov & Stoikov, Journal of Financial Econometrics / order-book-event research**  
https://arxiv.org/abs/1011.6402

For U.S. stocks, short-interval price changes were more robustly related to order-flow imbalance at the best bid/ask than to raw trade volume. This is not direct FX/Gold evidence, but supports testing imbalance/depth rather than candle volume alone.

## 9. Human day trading: existence of skill does not imply easy reproducibility

**Barber, Lee, Liu & Odean, Journal of Financial Markets 18 (2014)** found strong heterogeneity in Taiwan day-trader skill, but less than 1% of the day-trader population could predictably and reliably earn positive abnormal returns net of fees.

**Chague, De-Losso & Giovannetti (Brazilian equity futures)** found that among traders who persisted for at least 300 days, 97% lost money; the very small profitable tail earned returns with substantial risk.

The implication for this project is not "day trading cannot work."

It is:

> the target is to reproduce the information/process advantage of the small skilled tail, not the visible chart behavior of the average trader.

## 10. Meta-overfitting has become a project-level risk

Even though Jul-Aug and September have been protected, the project has now designed many engine families and versions after repeatedly observing the same development environment.

That creates **researcher-level data snooping**.

Sullivan, Timmermann & White show why performance must be interpreted in the context of the full universe of rules tried, not the one rule that eventually looks best.

Bailey et al. similarly warn that ordinary holdout procedures can be unreliable when many backtests are used to select strategies.

Therefore the next research phase must:

- maintain a complete trial ledger;
- count engine/version families as strategy-search trials;
- avoid further OHLC-threshold invention on the same development set;
- preferably broaden **earlier** historical development data rather than consume protected future periods;
- use purged/embargoed walk-forward evaluation for learned models;
- reserve independent-feed and forward/demo evidence for promotion.

## 11. Root-cause ranking

### RC-1 — Insufficient information advantage: HIGH confidence

Most engines transform OHLC price state. Their pooled gross expectancy clusters around zero. This is the strongest repeated internal finding.

### RC-2 — Objective/equity/risk mismatch: HIGH confidence

USD150-$200 is a 30%-40% daily return on USD500. The current safe-risk/payoff framework cannot make that a routine expectation without extremely high hit rates or materially higher loss risk.

### RC-3 — Human context/skip logic not encoded: HIGH confidence

The surviving Badar evidence contains context/location/session/news/target-path concepts that recent generic engines do not fully represent.

### RC-4 — Execution matters but is not sufficient: HIGH confidence

Q's non-chasing entry improved matched immediate execution materially, yet remained below the raw-edge gate.

### RC-5 — T40-only labeling is too restrictive for final architecture: MEDIUM-HIGH confidence

The project objective and human evidence both require target-ladder/runner behavior; T40 should remain a gate diagnostic, not the final trading ontology.

### RC-6 — Universal-engine requirement is probably too broad: MEDIUM confidence

Different markets can require different information mechanisms. Specialization should be prospective and mechanism-based.

### RC-7 — Execution-grade/microstructure data deficiency: HIGH confidence for next research phase

External FX research directly supports order flow as a candidate source of short-horizon information missing from the current feature stack.

### RC-8 — Meta-overfitting from repeated development reuse: HIGH confidence

The number of tried families now makes strategy-search selection bias a material concern even with protected future periods.

## 12. Required research program before another engine family

### Phase A — economic feasibility frontier

Freeze a quantitative frontier across:

- structural risk per trade;
- target multiples / target ladder;
- hit probability;
- qualified opportunities/day;
- outcome correlation;
- transaction costs;
- daily stop;
- maximum tolerable drawdown/risk-of-ruin.

Deliverable: identify combinations that can plausibly yield useful strong days without requiring implausible hit rates or breaking the loss budget.

### Phase B — edge-source data acquisition audit

Prioritize:

1. intended-broker MT5 tick/bid/ask/spread data where available;
2. COMEX Gold futures trades/top-of-book/depth/order flow;
3. CME FX futures and/or EBS Spot FX order-flow/depth data where commercially feasible;
4. macro announcement timestamps, actual, consensus and standardized surprise;
5. U.S. rates/Treasury or rate-futures reaction around macro events;
6. DXY/broad USD factor/context;
7. session/liquidity-state features;
8. volume/open-interest where causally available.

No strategy is selected yet.

### Phase C — information-content study before trade rules

Build a frozen comparison:

- price-only baseline;
- price + session/structural location;
- + macro/catalyst;
- + microstructure/order flow;
- + rates/cross-asset context.

Evaluate incremental out-of-sample information for the target ladder using:

- Brier score / log loss;
- calibration;
- AUC as secondary only;
- conditional MFE/MAE/path distributions;
- economically relevant expected value after realistic costs;
- stability across folds/regimes.

The purpose is to answer:

> does this new information source actually add predictive information beyond OHLC before we wrap it in a trading setup?

### Phase D — human-process decomposition

Future strategy design should follow:

`regime/catalyst -> structural location -> participation/order-flow confirmation -> trigger -> non-chasing execution -> structural stop -> target ladder -> EV/ranking`.

Every layer must be causal and measurable.

### Phase E — specialized engines only after edge-source evidence

If Phase C finds stable incremental information, freeze at most a small number of genuinely distinct engines, for example:

- Gold macro + COMEX participation/liquidity;
- FX macro/order-flow;
- non-news liquidity/absorption if independently supported.

Do not start three because three are desired. Start only the mechanisms supported by the information audit.

## 13. Decision on Engine R / EXP-039

Engine R is not promoted or rejected by this root-cause audit.

Its zero-outcome mechanics may remain preserved as a frozen research artifact.

However:

- do not advance it to target/P&L development merely because its preflight may produce sufficient signals;
- do not use its eventual preflight count to justify another price-only development cycle;
- do not inspect protected Jul-Aug or Sep;
- first complete the edge-source/economic feasibility program.

## 14. Go/no-go rule for the next strategy build

Before another strategy family reaches outcome development, require all of the following:

1. a stated economic mechanism not reducible to another threshold transform of the same OHLC state;
2. evidence that its new information family adds stable out-of-sample predictive content versus a price-only baseline;
3. realistic spread/cost/execution assumptions for that information horizon;
4. target-ladder and structural-room compatibility;
5. a predeclared development/validation plan accounting for the growing number of strategies already tried;
6. protected Jul-Aug and Sep remain sealed until the frozen development gate passes.

## Bottom line

The project should stop asking:

> which chart formula should we try next?

It should ask:

> what information is available to a skilled intraday trader that is not yet present in our dataset, does that information predict target-before-stop outcomes out of sample, and can that edge be monetized safely under a USD500 account?

Until those questions are answered quantitatively, increasing risk or iterating another OHLC family is more likely to magnify noise than produce a trading system.
