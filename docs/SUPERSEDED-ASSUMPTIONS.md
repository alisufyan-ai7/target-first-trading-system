# Superseded Assumptions

_Last updated: 2026-09-22_

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

Original EXP-002 Gold Engine A remains a separate active research lead until faithfully recovered/reproduced.

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
