# Edge-Source Research Matrix v0.1

**Date:** 2026-09-25  
**Status:** RESEARCH CHECKPOINT — NO STRATEGY OUTCOME  
**Purpose:** prioritize genuinely new information sources before another engine is advanced

## Research principle

A new engine should not be justified merely because its chart rules are different.

Before strategy construction, ask whether the proposed information family adds stable causal information beyond the existing OHLC-only baseline.

## Priority matrix

| Information source | Direct relevance to our markets/horizon | Evidence from literature | Current repo coverage | Data feasibility | Research priority |
|---|---|---|---|---|---|
| FX signed order flow / order-book imbalance | Very high for 1m-1h FX | Strong historical + recent FX evidence | Missing | EBS/CME/commercial data | **First-tier** |
| COMEX Gold trades/depth/order-flow imbalance | Very high for Gold intraday | Strong microstructure rationale; centralized futures venue | Missing | CME DataMine | **First-tier** |
| Macro actual-vs-consensus surprise | High for Gold/FX around releases | Strong FX and Gold announcement evidence | Missing | Economic calendar/vendor | **First-tier** |
| Rates/Treasury reaction around macro/FOMC | High for USD/Gold macro transmission | Strong economic mechanism | Missing | CME/rates feeds/public series depending horizon | **First-tier** |
| Broker bid/ask/spread/tick path | Essential for executable edge | Execution realism rather than standalone alpha | Missing from current research bars | MT5/intended broker | **First-tier** |
| Session/location/liquidity structure | High for human-style skip logic | Supported by project evidence, less direct causal literature | Partial OHLC only | Already derivable | **Second-tier context** |
| Futures volume/open interest | Potentially useful for participation/regime | Plausible + human evidence; weaker than signed flow | Missing/unused | CME | **Second-tier** |
| Cross-market OHLC momentum/volatility consensus | Already directly tested | Recent FX paper says incremental cross-currency value generally limited | Present/tested | Easy | **Low as standalone alpha** |
| Retail spot tick volume | Possible activity proxy | Feed-specific and not true centralized volume | Column may exist but provenance/meaning uncertain | Broker/feed dependent | **Validation only** |
| Social/news sentiment | Possible slower contextual input | Heterogeneous evidence; latency/licensing issues | Missing | Feasible but noisy | **Defer** |

## 1. FX order flow / limit-order-book state

### Why it is first-tier

The project's P/Q experiments already tested cross-market price relations and did not obtain enough raw edge.

Recent FX research is unusually relevant:

**Petrova, Vilhelmsson & Nordén (2026), International Journal of Forecasting**  
DOI: https://doi.org/10.1016/j.ijforecast.2025.12.007

- forecasts from one minute to one hour;
- generally low predictability;
- cross-currency variables add limited insight;
- certain microstructure variables such as order flow show short-horizon predictive power.

This directly argues against spending the next cycle on another cross-market OHLC transform.

Historical evidence:

**Evans & Lyons, Order Flow and Exchange Rate Dynamics**  
https://www.nber.org/papers/w7317

**Berger et al., Federal Reserve, Order Flow and Exchange Rate Dynamics in Electronic Brokerage System Data**  
https://www.federalreserve.gov/econres/ifdp/order-flow-and-exchange-rate-dynamics-in-electronic-brokerage-system-data.htm

The latter uses one-minute EBS EUR/USD and USD/JPY and documents substantial high-frequency association between order flow and exchange-rate returns.

### Candidate causal variables to research

Before strategy rules:

- signed trade imbalance over 30s / 1m / 5m;
- best-bid/best-ask depth imbalance;
- order additions vs cancellations;
- depletion/replenishment rate;
- aggressive-buy/aggressive-sell persistence;
- spread;
- short-window price impact per unit imbalance;
- flow divergence: price move without confirming order flow;
- absorption: sustained aggressive flow with limited price progress.

These should first be tested as incremental information, not converted immediately into BUY/SELL rules.

## 2. COMEX Gold participation / order flow

Gold is the project's economic anchor and the strongest surviving human evidence is Gold-specific.

A centralized futures venue provides information not available in broker-neutral OHLC:

- actual traded volume;
- trade direction inference / aggressor side where reconstructable;
- depth and book changes;
- liquidity depletion;
- event-time participation.

**CME DataMine**  
https://www.cmegroup.com/datamine.html

Available datasets include futures/options Market-by-Order and historical cash/FX datasets.

**CME Market Depth FAQ**  
https://www.cmegroup.com/market-data/files/cme-group-market-depth-faq.pdf

The documented files contain messages required to recreate the futures order book, with trade data and millisecond timestamps.

### Candidate research questions

- Does a Badar-style sweep/rejection have different target-first probability when COMEX order-flow imbalance reverses after the sweep?
- Is displacement more meaningful when accompanied by depth depletion / aggressive flow?
- Does a failed breakout with absorption predict reversion better than candle geometry alone?
- Does an FVG/retest work only when participation persists after the structural shift?

This would test the **missing participation layer** rather than redesign the visible chart pattern.

## 3. Macro surprise / catalyst state

### FX evidence

**Love & Payne, Journal of Financial Economics (2008)**  
DOI: https://doi.org/10.1016/j.jfineco.2007.06.001

Macro news affects FX directly and indirectly through order flow; the order-flow channel becomes particularly important after news arrival.

### Gold evidence

**Smales & Yang, International Review of Financial Analysis (2015)**  
DOI: https://doi.org/10.1016/j.irfa.2015.01.017

Gold futures returns, volatility and volume react quickly to macroeconomic announcements, with unemployment and GDP surprises among the most important in that study.

### Research representation

For each scheduled release:

- event type;
- exact timestamp;
- actual;
- consensus;
- previous/revised;
- standardized surprise;
- sign relative to USD/Gold economic hypothesis;
- pre-event dispersion where available;
- first 30s/1m/5m rate/futures reaction;
- order-flow response.

Do not encode “CPI high = short Gold” as a fixed rule.

The point is to characterize **information shock + market interpretation**.

## 4. Rates / cross-asset macro transmission

For Gold and USD FX, a skilled discretionary trader often observes whether rates and the dollar complex confirm the initial interpretation.

Potential causal state:

- 2Y / 5Y Treasury futures or yields;
- Fed-funds / SOFR expectations around policy events;
- DXY or broad USD factor;
- Gold futures;
- FX pair.

Research question:

> after a macro surprise, does the candidate market move have better continuation/reversion probability when the relevant rates/USD complex confirms or rejects it?

This is different from Engine P's generic cross-market price consensus because the peer variables have an explicit macroeconomic role.

## 5. Execution feed: bid/ask/spread/ticks

This is mandatory for final validation even if it adds no alpha.

Current one-minute OHLC research cannot faithfully represent:

- spread widening around news;
- executable bid/ask path;
- stop triggering on the relevant side of market;
- slippage/gaps;
- quote bursts;
- exact pullback fill quality.

`docs/data-sources.md` already identifies intended-broker MT5 as the preferred final broker-specific validation path.

Before promoting any short-horizon engine, obtain:

- tick timestamps;
- bid;
- ask;
- spread;
- symbol contract specification;
- commission;
- swap if relevant;
- leverage/margin rules.

## 6. Structural location/session context

This remains useful, but it should be treated as **context**, not assumed alpha.

Prospective features can include:

- previous-day high/low;
- Asian high/low;
- London high/low;
- previous session VWAP/value where real volume is available;
- confirmed swing liquidity;
- distance to opposing structural level;
- session transition;
- pre/post macro event state.

This directly addresses a known gap between the Badar evidence and recent generic price engines.

## 7. Target-path information

The final prediction target should not be one T40 label only.

For a causally frozen candidate, research:

- T30/T40/T50/T70/T100 before stop;
- MFE distribution;
- MAE distribution;
- time to each target;
- probability of partial then stop;
- probability of T30/T40 then extension;
- structural-room / opposing-liquidity distance;
- outcome under staged partial/runner rules frozen before evaluation.

This lets the eventual ranker choose the **best monetizable path**, not merely the setup with the highest binary T40 probability.

## 8. Information-content test design

Before building an execution engine, compare nested feature families on earlier development history:

**Baseline A — price only**
- existing OHLC/range/trend/time state.

**Baseline B — price + structural/session context**
- persistent levels and available room.

**Model C — + macro surprise / catalyst**
- event identity and surprise.

**Model D — + order flow / book**
- imbalance, depth, depletion, aggressor flow, spread.

**Model E — + rates / cross-asset interpretation**
- causally available rates/USD confirmation.

Use the same target-ladder labels and purged chronological folds.

Primary comparison:

- out-of-sample log loss;
- Brier score/calibration;
- conditional economic EV after realistic costs;
- stability across folds/regimes.

AUC is descriptive, not sufficient.

The critical test is **incremental value**:

> Does C/D/E improve out-of-sample target probabilities and economic EV beyond the price-only baseline?

If not, do not create a strategy from that source.

## 9. Data-snooping protection

The project has tried many strategy families on overlapping development data.

For the next information-content study:

- register each feature-family/model comparison before running it;
- keep a complete trial ledger;
- do not tune thresholds by inspecting protected-period outcomes;
- use purged/embargoed chronological validation;
- use earlier historical data to expand development where possible;
- reserve Jul-Aug/Sep under the existing protection policy;
- require independent-feed / forward-demo evidence before promotion.

Relevant methodology:

**Sullivan, Timmermann & White (1999)**  
DOI: https://doi.org/10.1111/0022-1082.00163

**Bailey et al., The Probability of Backtest Overfitting**  
https://www.risk.net/journal-of-computational-finance/2471206/the-probability-of-backtest-overfitting

## 10. Research decision

The highest-value next data/research path is:

**Gold:** macro surprise + COMEX participation/order flow + structural location + non-chasing entry.

**FX:** macro surprise + representative/centralized order flow + rates/USD interpretation + non-chasing entry.

OHLC-only cross-market consensus, residual, momentum, stretch or volatility should not be the next primary family unless new information-content evidence changes this conclusion.

No strategy outcome is authorized by this matrix.
