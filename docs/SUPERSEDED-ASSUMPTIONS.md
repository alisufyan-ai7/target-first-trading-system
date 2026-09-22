# Superseded Assumptions

_Last updated: 2026-09-23_

This file prevents historical experiments from being mistaken for current system requirements.

## Same 0.10 lot on every market

**SUPERSEDED**

Current:

- XAUUSD uses 0.10 lot as the economic anchor;
- other markets use symbol-specific P&L-equivalent lot sizing based on a frozen native target distance;
- equivalent size must pass structural-risk, margin, notional/leverage, daily-budget, and correlation gates.

EXP-012/013 same-0.10-lot FX calculations remain diagnostics only.

## Dynamic USD 20 risk / USD 50 target as universal economics

**SUPERSEDED AS THE FORWARD MODEL**

This was useful for earlier normalized comparisons but produced excessive notional exposure on tight FX stops.

Current system economics use the Gold 0.10-lot anchor, flexible target ladder, equivalent sizing for non-Gold markets, and actual structural stop risk as a feasibility constraint.

Historical EXP-007/009/010 results remain valid for the model they tested.

## Hard maximum four trades/day

**SUPERSEDED AS A HARD RULE**

Current:

- 3–4 qualified trades/day is a desirable normal range;
- no forced minimum;
- more may be acceptable when independent validated opportunities exist and aggregate risk is safe;
- never increase trade count merely to reach the daily target.

## Every winning trade must equal USD 50

**SUPERSEDED**

Current:

- approximately USD 50 is the normal economic unit;
- USD 30–40 is acceptable when target-first confidence is materially stronger;
- USD 70–100+ may be captured under validated continuation logic.

## 1:9 means 90% probability

**REJECTED**

Reward/risk does not imply probability.

## Portable Engine A v0.2 equals original EXP-002 Engine A

**REJECTED**

Engine A v0.2 is a later prospective rewrite.

Original EXP-002 Gold Engine A remains a separate **historical exploratory result**, but EXP-014 has now closed exact recovery as unrecoverable from the surviving evidence. It is not a validated/reproducible execution lead.

## Broad generic pivot candidates automatically replace strategy engines

**PAUSED / NOT CURRENT ARCHITECTURE**

Current architecture is:

~~~text
validated strategy engine
    -> candidate
    -> target-first probability/ranking layer
~~~

A generic statistical candidate generator may bypass this only after being explicitly defined and independently validated as an engine.

## Research as the end product

**SUPERSEDED**

The end product is a working trading system.

Research is its validation layer.


## Original EXP-002 remains an active executable lead

**SUPERSEDED**

EXP-014 froze a multi-dimensional recovery protocol and tested A1–A9.

No causal reconstruction reproduced the complete EXP-002 benchmark, and no original detector/backtest code survives.

Current treatment:

- preserve EXP-002's recorded historical metrics;
- do not relabel A6, v0.2-portable, or any forensic variant as the original;
- do not continue post-hoc benchmark fitting;
- build the next causal engine prospectively.

## Volatility-burden equivalence defines the forward non-Gold target

**REJECTED AS THE GOVERNING SIZING METHOD**

EXP-006's volatility-burden mapping remains a diagnostic.

Current forward method is engine-conditioned native target logic / engine-conditioned favorable-excursion calibration frozen in `docs/PNL-EQUIVALENT-SIZING.md`.
