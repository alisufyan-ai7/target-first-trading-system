# Strategy Status

_Last updated: 2026-09-22_

| Strategy label | Concept | Status |
|---|---|---|
| Engine A | Liquidity sweep -> MSS -> displacement/FVG -> retracement | USDJPY v0.2 RETAINED AS RESEARCH LEAD; expansion paused |
| Engine B | Momentum breakout -> retest -> continuation | FIRST FORMULATION REJECTED |
| Engine C | Trend regime -> pullback -> continuation | FIRST FORMULATION REJECTED |
| Engine D | Session/opening-range momentum | CURRENT FORMULATIONS NOT PROMOTED |
| Engine E | Volatility compression -> expansion | CURRENT FORMULATIONS NOT PROMOTED |
| Engine F | Statistical extension -> re-entry -> mean reversion | GBPUSD v0.1 RETAINED AS RESEARCH LEAD; other arms not promoted |

## Current research leads

### USDJPY / Engine A v0.2

Positive mean R in both EXP-007 splits, but daily-output and leverage/notional requirements remain unacceptable.

### GBPUSD / Engine F v0.1

Positive mean R in both EXP-009 splits:

- development +0.138R/trade;
- holdout +0.080R/trade.

However, holdout target-first hit rate is only 28.57%, <= USD 50 days are 100%, median stop is about 2.98 pips, and median notional/equity is about 181x.

## Research implication

Neither lead is deployable.

Do not retune or expand these engines now. The next experiment should combine the two frozen leads under the daily risk state machine and test whether their independence materially improves the project-level daily distribution.

## EXP-010 portfolio implication

USDJPY / Engine A and GBPUSD / Engine F are low-correlated, but their frozen combination still produced 86.44% <= USD 50 holdout days and no >= USD 150 holdout days.

**Decision:** neither lead nor their combination is promoted. Do not retune them. Active work moves to an objective-feasibility analysis before another engine is introduced.

## Fixed-size re-evaluation phase — EXP-012

The user clarified the intended execution model:

- XAUUSD reference size: 0.10 lot;
- major FX initial research size: 0.10 standard lot pending broker verification;
- useful profit captures may be USD 30–50, with USD 70–100+ runners when justified;
- trade count is opportunity-driven rather than capped at 3–4/day.

**Immediate action:** re-evaluate the two retained leads under fixed-size target ladders before adding another strategy family:

1. USDJPY / Engine A v0.2;
2. GBPUSD / Engine F v0.1.

The old dynamic USD 20 risk sizing results remain valid historical evidence but are no longer the forward execution model.
