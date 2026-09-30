# Badar Current-Era Formal Decision Policy v0.1

**Status:** OUTCOME-BLIND FORMAL POLICY — FROZEN AFTER COMMIT  
**Evidence snapshot:** `d19a43da80ae0e3ab4207a73a35f317120d37c84`  
**Decision corpus:** 42 live streams, 347 pre-entry decisions, 136 management decisions  
**P&L / outcome access:** NOT USED  
**Engine:** NO  
**Deployable:** NO  
**Backtest authorized:** NO

## Purpose

Translate the completed Badar current-era decision corpus into an explicit decision policy without inventing unsupported raw-price thresholds.

This policy operates on normalized, outcome-blind chart-state annotations. It is deterministic **given those annotations**.

It is not yet a raw-OHLC algorithm.

## Canonical hierarchy

```text
ENVIRONMENT
-> DIRECTIONAL CONTEXT
-> LOCATION
-> INTERACTION / PRICE EVENT
-> DECISION EVIDENCE
      -> CONFIRMATION BRANCH
      -> DIRECT / AGGRESSIVE BRANCH
-> EXECUTION FEASIBILITY
-> RISK CLASS
-> TRADE / WAIT / NO_TRADE
-> POST-ENTRY PREMISE MONITORING
-> MANAGEMENT ACTION
```

## Files

- `FORMAL-DECISION-POLICY.md` — ordered decision rules and management state machine.
- `ANNOTATION-CONTRACT.md` — normalized inputs required by the policy and the boundary between observation and unresolved mechanization.
- `FREEZE.md` — freeze statement and scientific restrictions.

## Core scientific constraint

The policy may formalize only distinctions already supported by the outcome-blind corpus.

It must **not** invent:

- a numeric MSS threshold;
- a fixed candle-body percentage;
- a universal stop-size ceiling;
- a universal RR minimum;
- a universal news blackout window;
- a universal BE distance;
- a fixed maximum trade count;
- a profit-optimized direct-entry exception.

Those require separate mechanization work before any P&L test.

## Output space

Pre-entry:

- `TRADE_LONG_NORMAL`
- `TRADE_LONG_REDUCED`
- `TRADE_SHORT_NORMAL`
- `TRADE_SHORT_REDUCED`
- `WAIT`
- `NO_TRADE`

Post-entry:

- `HOLD`
- `TIGHTEN_STOP`
- `BREAK_EVEN_OR_STRUCTURAL_PROTECTION`
- `PARTIAL_AND_PROTECT`
- `MANUAL_EXIT_INVALIDATED`
- `RUNNER_TO_LIQUIDITY`

The actual account lot size remains outside this policy and will later be constrained by Target-First account-risk rules.
