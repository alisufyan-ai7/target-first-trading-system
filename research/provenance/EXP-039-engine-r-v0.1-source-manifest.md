# EXP-039 Engine R v0.1 — Source / Split / Protection Manifest

**Frozen:** 2026-09-25

## Markets

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

Use only repository-admitted synchronized M1/M5 source conventions.

## Hard source seal

For preflight/development:

- source may begin 2026-03-23 for warm-up/state;
- no row at or after 2026-07-01 00:00 UTC may be loaded;
- parsed maximum timestamp must be reported and must be <=2026-06-30 23:59 UTC.

## Development folds if permitted

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

At decision t:

- peer relationship uses only prior completed M5 returns;
- current bar is excluded from correlation and scale estimation;
- current 15m candidate/peer moves use completed bars only;
- candidate excluded from peer search;
- deterministic strongest-peer selection;
- rejection bar is completed before limit is fixed;
- no future target/P&L data in preflight.

## Economics frozen before outcomes

- T40;
- primary cost 10% gross target;
- stress cost 20% gross target;
- stop risk <=USD20;
- notional <=USD50,000;
- margin <=USD100 at research 1:500;
- XAUUSD <=0.10 lot;
- 0.01 lot step.

## Outcome state

At freeze:

- Engine-R target outcomes: NO;
- Engine-R P&L outcomes: NO;
- Jul-Aug inspected: NO;
- Sep inspected: NO.
