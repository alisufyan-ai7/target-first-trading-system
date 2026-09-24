# EXP-037 Engine Q v0.1 — Source / Split / Protection Manifest

**Frozen:** 2026-09-24  
**Experiment:** EXP-037  
**Engine:** Engine Q v0.1

## Source-of-truth data scope

Reuse only the synchronized execution-research market data already admitted for the eight-market scanner family:

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

Engine Q requires only completed M5 and M1 OHLC derived/loaded under the repository's existing causal conventions.

No external macro calendar, news label, protected-period statistic, or post-Jun30 row is an Engine-Q input.

## Hard source seal

For zero-outcome preflight and development:

- earliest reusable state source: 2026-03-23;
- maximum permitted source timestamp: **2026-06-30 23:59:00 UTC**;
- any row timestamp >=2026-07-01 00:00 UTC is forbidden.

The implementation/preflight must report its parsed maximum timestamp and fail if the seal is violated.

## Development evaluation slices

Frozen before Engine-Q outcomes:

- WF1: [2026-04-13, 2026-04-27)
- WF2: [2026-04-27, 2026-05-11)
- WF3: [2026-05-11, 2026-05-25)
- WF4: [2026-05-25, 2026-06-08)
- WF5: [2026-06-08, 2026-06-22)
- WF6: [2026-06-22, 2026-07-01)

Warm-up/state may use earlier admitted Mar23-Apr12 rows but they are not a separate favorable outcome-selection pool.

## Protected periods

Remain completely sealed until the full frozen development gate passes:

- secondary: 2026-07-01 through 2026-08-31;
- final holdout: 2026-09-01 through the repository's frozen September common-sample endpoint.

Preflight/development must explicitly record:

- secondary loaded/labeled = false;
- final holdout loaded/labeled = false.

## Causality rules

- completed bars only;
- candidate is excluded from its own peer-volatility breadth;
- all peer bars used for one decision share the same completed timestamp;
- every prior-24 baseline excludes the current bar;
- the lag box is frozen before future breakout bars;
- first qualifying breakout only;
- entry price fixed from completed breakout bar before future M1 path;
- no future target/P&L information in preflight.

## Research economics frozen before outcomes

- target: T40;
- primary cost: 10% of gross target USD;
- stress cost: 20% of gross target USD;
- same signal-first safe-lot overlay:
  - stop risk <=USD20;
  - notional <=USD50,000;
  - margin <=USD100 at 1:500 research leverage;
  - XAUUSD <=0.10 lot;
  - 0.01 lot step.

## Outcome-state declaration

At manifest freeze:

- Engine-Q target outcomes calculated: NO;
- Engine-Q P&L outcomes calculated: NO;
- Jul-Aug inspected by Engine Q: NO;
- September inspected by Engine Q: NO.
