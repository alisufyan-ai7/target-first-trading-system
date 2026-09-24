# EXP-038 Engine Q v0.2 — Source / Split / Protection Manifest

**Frozen:** 2026-09-24

## Markets

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

Use only repository-admitted synchronized M1/M5 source conventions already used by the current scanner research.

## Hard source seal

Preflight/development may load no row at or after:

`2026-07-01 00:00:00 UTC`.

Report parsed max timestamp and fail on violation.

Warm-up/state source may begin 2026-03-23.

## Development folds

- WF1 [2026-04-13, 2026-04-27)
- WF2 [2026-04-27, 2026-05-11)
- WF3 [2026-05-11, 2026-05-25)
- WF4 [2026-05-25, 2026-06-08)
- WF5 [2026-06-08, 2026-06-22)
- WF6 [2026-06-22, 2026-07-01)

## Protected periods

- Jul-Aug secondary: sealed;
- Sep final holdout: sealed.

## Causality

At candidate decision t:

- all current states use completed M5 bars only;
- rolling peer shock memory may use only t, t-5m, t-10m;
- candidate excluded from peer set;
- each peer counted once;
- lag box frozen before later breakout;
- first qualifying later breakout only;
- entry fixed from completed breakout bar before future M1 path.

## Economics

Frozen before outcomes:

- T40;
- primary cost 10% gross target;
- stress cost 20% gross target;
- stop risk <=USD20;
- notional <=USD50k;
- margin <=USD100 at 1:500 research leverage;
- XAUUSD <=0.10 lot;
- 0.01 lot step.

## Outcome state

At freeze:

- target outcomes NO;
- P&L outcomes NO;
- Jul-Aug inspected NO;
- Sep inspected NO.
