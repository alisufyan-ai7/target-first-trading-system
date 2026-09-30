# Pass A Summary — Outcome-Blind Decision Trace Corpus

## Scope

10 newest current-era live streams, 2026-09-16 through 2026-09-30.

No future outcome fields were included in the decision corpus.

## Pre-entry decisions

Total: **107**

| Decision | Count | Share |
|---|---:|---:|
| NO_TRADE | 42 | 39.3% |
| WAIT | 39 | 36.4% |
| TRADE_SHORT | 18 | 16.8% |
| TRADE_LONG | 8 | 7.5% |
| **All TRADE** | **26** | **24.3%** |
| **WAIT + NO_TRADE** | **81** | **75.7%** |

This does not estimate trade frequency in the market. It describes the salient decisions recorded in the source notes.

The key point is that the source evidence contains substantially more **filtering / waiting decisions** than entries.

## Most common WAIT reasons

| Reason | Count |
|---|---:|
| WAIT_CONFIRMATION_CLOSE | 10 |
| WAIT_SWEEP | 7 |
| WAIT_HTF_CLOSE | 5 |
| WAIT_RETRACE | 4 |
| WAIT_CONFIRMATION | 3 |
| WAIT_SWEEP_CONFIRM | 2 |
| Other individual wait reasons | 8 |

A large part of the live decision process is therefore temporal: a location may already be known, but Badar frequently waits for an additional event or close.

## Most common NO_TRADE reasons

| Reason | Count |
|---|---:|
| NO_TRADE_WRONG_EXTREME | 7 |
| NO_TRADE_HTF_CLOSE_CONFLICT | 2 |
| NO_TRADE_CHASE | 2 |
| NO_TRADE_NO_LOCATION | 2 |
| NO_TRADE_AGAINST_ACTIVE_DIRECTION | 2 |
| NO_TRADE_STRUCTURE_MISSING | 2 |
| NO_TRADE_DISCRETION_UNCLEAR | 2 |
| Other individual skip reasons | 23 |

The single most repeated explicit rejection is being at the **wrong extreme**: selling after price is already low/extended or buying at/near the top.

## Trade decisions

26 trade decisions were captured.

### Direction

- SHORT: 18
- LONG: 8

This is source-sample composition only, not a directional recommendation.

### Alignment

- ALIGNED: 14
- COUNTERTREND: 3
- UNKNOWN / mixed not safely classifiable: 9

### Risk class

- NORMAL: 12
- REDUCED: 14

More than half of captured entries were explicitly represented as reduced-risk / conditional-quality trades.

### Location and stop feasibility

For all 26 captured trade decisions:

- `location_present = YES`
- `logical_stop_present = YES`

This is a strong descriptive feature of Pass A, but it must not yet be treated as proof that those fields predict profitability.

### Confirmation families among trade decisions

| Confirmation | Count |
|---|---:|
| INVERSE_CLOSE | 8 |
| MOMENTUM_CLOSE | 7 |
| OB_RETRACE | 3 |
| CLOSE_BACK_INSIDE | 2 |
| DEMAND_REACTION | 2 |
| NONE / direct zone entry | 2 |
| REJECTION | 1 |
| combined inverse/2CR/MSS | 1 |

The presence of **two direct-location entries with no separate confirmation family** is important counterevidence to making MSS/sweep/candlestick confirmation a universal hard gate.

## Management decisions

Total: **36**

| Action | Count |
|---|---:|
| BREAK_EVEN | 11 |
| PARTIAL | 10 |
| TIGHTEN_STOP | 7 |
| MANUAL_EXIT | 4 |
| HOLD | 2 |
| STRUCTURAL_PROTECTION | 1 |
| EXTEND_TARGET | 1 |

Management is therefore a substantial part of the observable decision process rather than an afterthought.

### Common management reasons

- favorable move: 8
- TP1 reached: 8
- opposing close: 4
- new structure: 3
- failed confirmation: 2

Four explicit manual exits were driven by opposing candle-close evidence rather than waiting mechanically for the original stop.

## Pass-A interpretation

The first 10 streams support five descriptive propositions strongly enough to continue investigating them:

1. **Selection dominates execution count.** WAIT + NO_TRADE decisions substantially outnumber entries in the annotated evidence.
2. **Location is a prerequisite in observed entries.** No captured trade in Pass A is an arbitrary mid-range signal.
3. **Closes are a timing gate.** Waiting for a confirmation close or HTF close is the most common WAIT family.
4. **Sweep is important but not universal.** Direct continuation/retrace/zone entries exist.
5. **Risk and management are state-dependent.** Badar frequently reduces size/risk, tightens, takes partials, or manually exits as the premise changes.

## What Pass A does NOT establish

It does not establish:

- profitability;
- which decision gate has positive expectancy;
- whether skipped trades would have lost;
- an optimal threshold;
- a deployable rule set;
- that every Badar trade fits the hierarchy perfectly.

## Unresolved cases worth preserving

A particularly valuable example is `fkZjFHTg3GY` on 2026-09-18:

Badar identifies a sell POI, rejection, liquidity sweep and momentum shift, yet says he saw the sell sign and **did not take it**.

That decision currently remains `NO_TRADE_DISCRETION_UNCLEAR`.

This kind of unexplained skip should not be erased merely because it makes automation harder. It may identify a missing human variable.

## Status

Pass A validates that the schema can represent current-era live behavior without using outcomes.

**Next:** apply the same schema to the remaining 32 pinned live streams (Pass B), then re-evaluate which gates are genuinely stable before any strategy formalization.
