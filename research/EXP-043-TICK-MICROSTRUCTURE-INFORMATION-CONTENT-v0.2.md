# EXP-043 Tick Microstructure Information-Content Study v0.2

**Frozen:** 2026-09-27, after source-only coverage diagnosis and without reinterpreting v0.1  
**Type:** development-only availability-defined rerun  
**v0.1 status:** `INTEGRITY_FAIL_DO_NOT_INTERPRET`

## 1. Scientific reason for v0.2

EXP-043 v0.1 failed only the prospectively frozen requirement that microstructure eligibility coverage be >=90% in every market.

A separate source-only diagnostic, which loaded no target OHLC, labels, predictions or P&L, proved that the immutable microstructure source itself has <90% theoretical decision-time coverage for exactly:

- AUDUSD: 82.37%;
- USDCHF: 87.30%.

All other markets have >=90% source-only coverage.

Diagnostic durable commit:

`2005a6187a3dec895d68e066d19a018ac25cd290`

Diagnostic Git blob:

`c0f5a33d5a73495922280b241b037e0f81641f33`

Disposition:

`SOURCE_AVAILABILITY_EXPLAINS_EXP043_COVERAGE_FAILURE`.

v0.1 remains non-interpretable.

## 2. Frozen availability-defined market universe

v0.2 uses exactly the six markets with source-only theoretical decision coverage >=90%:

- XAUUSD;
- EURUSD;
- GBPUSD;
- USDJPY;
- EURJPY;
- USDCAD.

AUDUSD and USDCHF are excluded solely because of outcome-blind source availability.

No other market may be added or removed.

## 3. What is unchanged from v0.1

All of the following remain exactly unchanged:

- target-market immutable Dukascopy v2 source;
- immutable EXP-043 microstructure snapshot;
- model interval starting 2026-03-23;
- broad structural candidate mechanics;
- target/path labels;
- T40eq/T50eq primary rungs;
- six EXP-040 chronological folds;
- 120-minute purge;
- 5m / 30m / 60m microstructure windows;
- 4 / 24 / 48 observed-minute availability minima;
- all microstructure feature definitions;
- LOCAL_M5 baseline;
- execution-cost / participation / quote-imbalance nesting;
- fixed logistic learner;
- fixed Platt calibration;
- >=1% pooled relative log-loss improvement;
- lower Brier;
- >=4/6 fold wins;
- ECE not worse by >0.01;
- paired day-level win fraction >=55%;
- no protected-period use.

No feature, window, threshold, learner parameter or fold may change based on v0.1 outputs.

## 4. Market-stability gate

The existing absolute requirement is retained:

> enriched pooled log loss must be non-worse in at least **5 markets**.

Because v0.2 contains six markets, this is stricter proportionally than v0.1's 5-of-8 requirement.

Do not weaken it.

## 5. Integrity gate

Require:

- source diagnostic blob exactly `c0f5a33d5a73495922280b241b037e0f81641f33`;
- diagnostic disposition exactly `SOURCE_AVAILABILITY_EXPLAINS_EXP043_COVERAGE_FAILURE`;
- diagnostic markets below 90% exactly `AUDUSD, USDCHF`;
- active market universe exactly the six markets above;
- immutable target and microstructure source hashes unchanged;
- candidate-level microstructure eligibility >=90% in every active market;
- every active market-direction >=500 eligible labeled candidates;
- every evaluation fold has both T40/T50 classes;
- every active market has both classes in pooled evaluation;
- paired evaluation days >=45;
- same eligible rows across all feature sets;
- microstructure data strictly causal;
- no protected Jul-Aug/Sep 2026 data;
- Engine R / EXP-015 outcomes unused.

Any integrity failure => `INTEGRITY_FAIL_DO_NOT_INTERPRET`.

## 6. Scientific gate and dispositions

Use the exact v0.1 information-advantage gate, except the absolute market-count requirement is still five markets, now out of six.

If no enriched set passes:

`NO_STABLE_TICK_MICROSTRUCTURE_INFORMATION_ADVANTAGE`.

If the smallest passing set is execution-cost:

`STABLE_EXECUTION_COST_INFORMATION_ADVANTAGE_FOUND`.

If participation:

`STABLE_PARTICIPATION_INFORMATION_ADVANTAGE_FOUND`.

If quote imbalance:

`STABLE_QUOTE_IMBALANCE_INFORMATION_ADVANTAGE_FOUND`.

## 7. Governance after result

Because v0.1 outcomes already exist but were non-interpretable, v0.2 may change **only** the market universe using the outcome-blind source diagnostic.

No other design change is permitted.

A v0.2 PASS remains development evidence and does not itself authorize strategy deployment or protected-period use.

A v0.2 FAIL closes the free Dukascopy quote-microstructure information layer. Do not tune microstructure windows/features on this development sample; move to a genuinely richer source class such as true broker/exchange order book or aggressor-flow data.
