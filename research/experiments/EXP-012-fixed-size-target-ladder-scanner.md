# EXP-012 — Fixed-Size Target-Ladder and Multi-Market Scanner Economics

**Status:** IN PROGRESS — ECONOMIC RULES FROZEN BEFORE NEW OUTCOME TESTING  
**Date:** 2026-09-22

## Purpose

Replace the superseded fixed USD 20 risk / USD 50 target / maximum-4-trades framework with the user's clarified operating objective:

- fixed reference execution size;
- flexible USD 30–100+ profit capture;
- opportunity-driven trade count;
- broad cross-market scanning;
- target-first ranking of where the best current move is most likely to occur before invalidation.

This experiment defines the economic labels and scanner decision structure **before** any new strategy/market outcome inspection under the revised objective.

## System objective

The intended system should scan every supported liquid market, identify candidate long/short setups, estimate attainable dollar-profit rungs before structural invalidation, and rank opportunities across markets.

Desired daily net P&L zone: approximately USD 150–200 when sufficient qualified opportunity exists.

There is no forced daily trade quota.

## Fixed execution-size anchor

### XAUUSD

Reference size: **0.10 lot**.

Research convention until broker-specific verification:

- 1.00 lot = 100 oz;
- 0.10 lot = 10 oz;
- USD 1 XAUUSD move = approximately USD 10 gross P&L.

Therefore the XAUUSD target ladder is:

| Favorable XAU move | Approx gross P&L at 0.10 lot |
|---:|---:|
| USD 3 | USD 30 |
| USD 4 | USD 40 |
| USD 5 | USD 50 |
| USD 7 | USD 70 |
| USD 10 | USD 100 |

The structural stop is not resized to fit a fixed dollar-risk amount. Fixed size + structural stop determines actual risk.

### Major FX

Initial research execution anchor: **0.10 standard lot = 10,000 base units**, pending broker verification.

For USD-quote majors such as EURUSD and GBPUSD, the common convention gives approximately USD 1 per pip at 0.10 lot.

Illustrative target ladder:

| Favorable move | Approx gross P&L at 0.10 lot |
|---:|---:|
| 30 pips | USD 30 |
| 40 pips | USD 40 |
| 50 pips | USD 50 |
| 70 pips | USD 70 |
| 100 pips | USD 100 |

For JPY-quote pairs, pip value must be converted from JPY to USD at the contemporaneous USDJPY conversion rate. Do not assume a fixed USD pip value.

### Other markets

For XAGUSD, indices, crypto, and other CFDs/futures-like instruments:

- do not guess that 0.10 lot has comparable economics;
- record the actual contract size, tick size, tick value, quote currency, and margin rules;
- define a fixed execution-size tier that is economically sensible relative to the XAUUSD 0.10-lot anchor;
- freeze that tier before testing target outcomes.

## Target-first labels

For every filled candidate, calculate whether the position reaches each fixed-size dollar-profit rung before structural invalidation:

- T30: approximately +USD 30;
- T40: approximately +USD 40;
- T50: approximately +USD 50;
- T70: approximately +USD 70;
- T100: approximately +USD 100.

Also record:

- maximum favorable excursion in native price and USD;
- maximum adverse excursion;
- time to each target;
- whether structural stop is reached first;
- end-of-session marked P&L if neither target nor stop is reached.

Same-bar target/stop ambiguity remains conservative: stop first.

## Opportunity ranking design

A future scanner should not output only BUY/SELL.

For each candidate it should output a target ladder such as:

- direction;
- entry;
- structural invalidation;
- fixed position size;
- estimated probability of T30 before stop;
- estimated probability of T40 before stop;
- estimated probability of T50 before stop;
- estimated probability of T70 before stop;
- estimated probability of T100 before stop;
- expected net dollar value after estimated costs;
- margin required;
- open-risk impact;
- correlation/exposure impact;
- confidence/calibration diagnostics.

"Sure" is operationalized as a validated probability/expected-value gate. No target is guaranteed.

## Trade-selection rule to develop

The final decision rule should compare opportunities across markets, not trade each market independently.

Conceptually:

1. generate candidates from all validated engines and supported markets;
2. estimate target-ladder probabilities;
3. reject candidates whose fixed-size structural risk breaches the remaining daily/open-risk budget;
4. reject margin-infeasible or excessively correlated exposure;
5. rank survivors by validated expected dollar value and probability of useful profit capture;
6. execute only candidates above a threshold frozen on development/validation data;
7. stop adding new exposure near the +USD 150–200 daily state or after the daily loss gate.

The exact probability/EV threshold is **not** chosen in this checkpoint. It must be learned on development data and frozen before holdout testing.

## Trade count

No hard maximum of 3–4 trades/day is assumed in EXP-012.

More than four entries may be acceptable if:

- all entries independently pass the frozen quality gate;
- simultaneous exposure is feasible;
- correlated positions are controlled;
- aggregate stop-risk remains within the daily framework;
- no trading is forced to reach the daily target.

The experiment must still report trade count distributions and zero-signal days.

## Daily risk gate

Reference balance: approximately USD 500.

Existing daily framework remains:

- normal stop adding risk around -USD 40 realized daily P&L;
- rare absolute hard-loss ceiling around -USD 60;
- desired profit-state zone around +USD 150–200.

With fixed size, dollar loss at structural invalidation varies by trade.

Therefore every candidate must calculate its actual structural-stop dollar loss before entry.

A candidate is rejected when its fixed-size stop exposure cannot fit the remaining daily/open-risk budget.

## Initial supported research universe

Existing repository/data coverage:

- XAUUSD;
- XAGUSD;
- EURUSD;
- GBPUSD;
- USDJPY.

Priority additions for the scanner as clean data/contract economics become available:

- GBPJPY;
- EURJPY;
- AUDUSD;
- USDCAD;
- USDCHF;
- NAS100 / USTEC;
- US30;
- US500 / SPX500;
- BTCUSD / BTCUSDT where venue economics are explicitly defined.

The long-term scanner should support all liquid markets available through the eventual broker/data feed, but markets are added only after data and contract specifications are documented.

## First quantitative tasks

Before testing another new strategy family:

1. build the fixed-size economic map for the existing five-market universe;
2. calculate native price/pip distances corresponding to T30/T40/T50/T70/T100;
3. calculate the historical frequency with which those favorable moves occur from candidate entries before structural invalidation for the two retained leads:
   - USDJPY / Engine A v0.2;
   - GBPUSD / Engine F v0.1;
4. re-evaluate those leads under fixed 0.10-lot economics instead of dynamic USD 20 risk sizing;
5. report actual structural-stop dollar risk distributions at fixed size;
6. determine whether either lead remains economically useful;
7. only then decide whether to add another engine or expand the market universe.

## Required metrics

Per market/engine/split:

- fixed execution size;
- median/mean structural stop in native units;
- median/mean dollar risk at fixed size;
- T30/T40/T50/T70/T100 hit rates before stop;
- mean/median maximum favorable excursion in USD;
- mean/median trade P&L under predeclared exit rules;
- expectancy after estimated costs when cost data are available;
- trades/day including zero-signal days;
- losing-day percentage;
- <= USD 50 day percentage;
- >= USD 100 / 150 / 200 day percentages;
- maximum daily loss;
- maximum drawdown;
- consecutive losing/low-output days;
- margin/notional diagnostics;
- target-hit time distributions.

## Holdout discipline

Use existing development/holdout separation when reconstructing retained leads:

- development: 2026-03-12 through 2026-05-31;
- holdout: 2026-06-01 through 2026-08-20.

No new signal parameter may be tuned using the holdout.

Fixed-size economics and target ladders in this file are frozen before re-reading outcomes under the revised economic framing.

## Promotion rule

No strategy is promoted merely because it shows some T30/T40/T50 hits.

A candidate must demonstrate:

- positive net expectancy;
- acceptable fixed-size structural risk;
- robust development/holdout behavior;
- feasible margin;
- useful daily contribution;
- stability after realistic costs;
- independent-feed validation;
- forward/paper evidence.

## Immediate next action

Reconstruct the two retained lead trade streams and recalculate them under the fixed-size target ladder, starting with:

1. USDJPY / Engine A v0.2 at 0.10 standard lot;
2. GBPUSD / Engine F v0.1 at 0.10 standard lot.

Checkpoint each result separately before any new engine is introduced.

## Checkpoint 1 — USDJPY / Engine A v0.2 at fixed 0.10 standard lot

**Status:** FIXED-SIZE ECONOMICS NOT SUFFICIENT FOR USD 30–100 TARGET LADDER

### Reconstruction note

The frozen Engine A v0.2 logic was reconstructed from the repository specification and the same public USDJPY 1m research sample used in EXP-007/010.

This reconstruction produced:

- raw retracement fills: 263;
- accepted trades after sweep-time/one-open filtering: 209;
- development trades: 111;
- holdout trades: 98.

EXP-010's prior reconstruction recorded 208 accepted trades / 111 development / 97 holdout, while EXP-007 originally recorded 209 / 112 / 97.

The current run therefore differs by one holdout trade from the prior reconstruction. This discrepancy is preserved transparently. No parameters were changed to force the counts to match.

The old 2.5R diagnostic remains close enough to confirm the reconstruction is broadly consistent:

- development mean old-model R: about +0.084R;
- holdout mean old-model R: about +0.250R;
- EXP-010 reference holdout mean: about +0.263R.

### Fixed-size economics

Execution size:

- 0.10 standard lot = 10,000 USD base units.

Structural-stop dollar loss is calculated from the actual stop distance and JPY/USD conversion implied by USDJPY.

#### Development — 111 reconstructed trades

- median fixed-size structural-stop risk: **USD 3.00**;
- mean structural-stop risk: **USD 3.41**;
- 90th-percentile structural-stop risk: **USD 5.77**;
- median maximum favorable excursion before stop/session end: **USD 3.82**;
- mean maximum favorable excursion: **USD 8.40**.

Target-first hit rates before structural invalidation:

| Target rung | Hit rate |
|---|---:|
| T30 | 3.60% |
| T40 | 3.60% |
| T50 | 2.70% |
| T70 | 2.70% |
| T100 | 0.90% |

#### Holdout — 98 reconstructed trades

- median fixed-size structural-stop risk: **USD 2.24**;
- mean structural-stop risk: **USD 3.15**;
- 90th-percentile structural-stop risk: **USD 6.83**;
- median maximum favorable excursion before stop/session end: **USD 2.94**;
- mean maximum favorable excursion: **USD 12.48**.

Target-first hit rates before structural invalidation:

| Target rung | Hit rate |
|---|---:|
| T30 | 7.14% |
| T40 | 6.12% |
| T50 | 4.08% |
| T70 | 4.08% |
| T100 | 3.06% |

### Interpretation

The fixed 0.10-lot model solves the earlier excessive-notional problem but creates the opposite economic problem:

- ordinary structural risk is only a few dollars;
- the typical favorable excursion is also only a few dollars;
- USD 30–50 outcomes are rare;
- USD 70–100 outcomes are rarer still.

So USDJPY / Engine A v0.2 is **not suitable as a primary USD 30–100 fixed-size income stream at 0.10 lot** under the current setup definition.

This does not prove USDJPY is useless to the future scanner. It means this specific Engine A entry family at this fixed size does not generate the dollar-move distribution required by the revised system objective.

### Disposition

- Preserve the historical Engine A lead record.
- Do not enlarge position size merely to manufacture USD 30–50.
- Do not retune Engine A after this result.
- Continue EXP-012 to GBPUSD / Engine F v0.1 at fixed 0.10 standard lot.

## Checkpoint 2 — GBPUSD / Engine F v0.1 at fixed 0.10 standard lot

**Status:** FIXED-SIZE ECONOMICS NOT SUFFICIENT FOR USD 30–100 TARGET LADDER

### Reconstruction note

The frozen Engine F v0.1 rules were reconstructed from the repository specification and the same public GBPUSD 1m research sample used in EXP-009.

The current reconstruction produced the exact same full-window accepted-trade total as EXP-009:

- accepted trades: 75.

Split assignment differs by one trade:

- current reconstruction: 39 development / 36 holdout;
- EXP-009 record: 40 development / 35 holdout.

The old-model mean-R diagnostics remain close but not identical:

- current development: about +0.167R vs repository +0.138R;
- current holdout: about +0.050R vs repository +0.080R.

The one-trade split discrepancy is preserved transparently; no parameters were changed to force-fit the old summary.

### Fixed-size economics

Execution size:

- 0.10 standard lot = 10,000 GBP;
- for GBPUSD, approximately USD 1 per pip under the common standard-lot convention.

#### Development — 39 reconstructed trades

- median fixed-size structural-stop risk: **USD 4.19**;
- mean structural-stop risk: **USD 4.15**;
- 90th-percentile structural-stop risk: **USD 5.32**;
- median maximum favorable excursion before stop/session end: **USD 4.50**;
- mean maximum favorable excursion: **USD 13.63**.

Target-first hit rates before structural invalidation:

| Target rung | Hit rate |
|---|---:|
| T30 | 15.38% |
| T40 | 7.69% |
| T50 | 7.69% |
| T70 | 7.69% |
| T100 | 0.00% |

#### Holdout — 36 reconstructed trades

- median fixed-size structural-stop risk: **USD 2.94**;
- mean structural-stop risk: **USD 3.80**;
- 90th-percentile structural-stop risk: **USD 5.28**;
- median maximum favorable excursion before stop/session end: **USD 3.70**;
- mean maximum favorable excursion: **USD 9.22**.

Target-first hit rates before structural invalidation:

| Target rung | Hit rate |
|---|---:|
| T30 | 11.11% |
| T40 | 2.78% |
| T50 | 0.00% |
| T70 | 0.00% |
| T100 | 0.00% |

### Interpretation

GBPUSD / Engine F v0.1 does not convert into a useful fixed-size USD 30–100 income stream at 0.10 lot.

The setup's typical structural stop and favorable excursion are only a few pips/dollars at this size. A USD 30–50 target requires approximately 30–50 pips, which occurs too rarely from these entries before invalidation.

### Disposition

- Preserve Engine F v0.1 as historical research evidence only.
- Do not increase lot size merely to force USD 30–50.
- Do not retune Engine F after this result.
- The two previously retained leads are no longer priority execution candidates under the clarified fixed-size objective.

## Interim EXP-012 conclusion

The revised economic framing changes the interpretation of prior work:

- dynamic USD 20 risk sizing made the old leads look capable of USD 50 targets only by creating extreme notional exposure;
- fixed 0.10-lot sizing removes that leverage problem;
- but the same leads then produce typical favorable excursions of only a few dollars.

Therefore the scanner needs setups and/or markets whose **native fixed-size movement** is large enough to support USD 30–100 captures without artificial leverage.

### Immediate next action

Return to XAUUSD first, because the user's fixed-size economics are naturally aligned there:

- 0.10 lot;
- USD 3 move -> about USD 30;
- USD 4 -> about USD 40;
- USD 5 -> about USD 50;
- USD 7 -> about USD 70;
- USD 10 -> about USD 100.

Re-evaluate existing XAUUSD candidate streams under this target ladder before defining a new Gold-specific engine.

