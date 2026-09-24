# Engine Q v0.2 — Rolling Cross-Market Volatility Spillover Breakout

**Engine ID:** engine-q-cross-market-volatility-spillover-breakout  
**Version:** 0.2  
**Experiment:** EXP-038  
**Status:** PROSPECTIVELY FROZEN — ZERO OUTCOMES — 2026-09-24

## 1. Why v0.2 exists

Engine Q v0.1 / EXP-037 stopped at zero-outcome preflight after only 56 filled signals.

The dominant bottleneck was not safety, candidate lag, or target/P&L economics. It was the requirement that at least four peer markets all exceed VR>=1.75 on the **same completed M5 bar**.

No target/P&L outcome was inspected.

v0.2 therefore changes only the temporal representation of peer shock evidence:

- v0.1: simultaneous same-bar peer shock breadth;
- v0.2: rolling 15-minute unique-peer shock memory.

The peer shock threshold and peer-count requirement are unchanged.

## 2. Markets

Execution-research universe:

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

Candidate symbol is always excluded from its own peer breadth.

## 3. Protected data / split

Reusable source:

- state source begins 2026-03-23;
- hard source seal at 2026-06-30 23:59 UTC.

Development evaluation folds remain:

- WF1 [2026-04-13, 2026-04-27)
- WF2 [2026-04-27, 2026-05-11)
- WF3 [2026-05-11, 2026-05-25)
- WF4 [2026-05-25, 2026-06-08)
- WF5 [2026-06-08, 2026-06-22)
- WF6 [2026-06-22, 2026-07-01)

Protected:

- Jul-Aug secondary;
- Sep final holdout.

## 4. Decision grid

Evaluate completed UTC-aligned M5 bars from:

`06:05, 06:10, ..., 17:25 UTC`.

One active Engine-Q arm/order per symbol at a time. New same-symbol opportunities while active are suppressed.

## 5. Per-market volatility state

For every market at every completed M5 time t:

- current range `R(t)=high-low`;
- baseline = prior 24 contiguous completed M5 bars, excluding current;
- `V(t)=even median(prior 24 ranges)`;
- `VR(t)=R(t)/V(t)`.

Completed bars only.

## 6. Rolling 15-minute peer-shock memory

For candidate S at decision time t:

For every other peer market P, inspect exactly:

- P at t;
- P at t-5m;
- P at t-10m.

A peer is counted as shocked if **any one** of those three completed bars has:

`VR >= 1.75`.

A peer counts at most once, regardless of how many of the three bars exceed threshold.

Require:

- candidate S excluded;
- at least 6 peers have complete valid rolling state;
- at least **4 unique shocked peers**.

Frozen peer-shock threshold remains **1.75**.
Frozen breadth count remains **4**.

Record each shocked peer's most recent qualifying shock age: 0, 5 or 10 minutes. Shock age is diagnostic only.

## 7. Candidate lag/compression

At current decision t, candidate must still be unexpanded:

- current candidate VR <=1.00;
- current close strictly inside fixed prior-six-M5 box.

Box:

- latest six completed candidate M5 bars immediately preceding current decision bar;
- `BOX_HI=max(high)`;
- `BOX_LO=min(low)`;
- box is frozen at arm creation.

## 8. Subsequent breakout trigger

After arm creation, observe at most next six completed candidate M5 bars.

First bar qualifies if:

- VR>=1.25;
- body>=50% of bar range.

LONG:

- close > frozen BOX_HI;
- close>open;
- high-close <=25% of range.

SHORT:

- close < frozen BOX_LO;
- close<open;
- close-low <=25% of range.

First qualifying breakout only.

Direction comes only from candidate breakout, never peer direction.

## 9. Execution

After breakout:

`LIMIT=(high+low)/2`.

LONG stop = trigger low - one research tick.
SHORT stop = trigger high + one research tick.

Order:

- next 10 active M1 bars;
- hard expiry trigger+30m;
- no entry at/after 18:00 UTC;
- gap through stop before limit cancels.

## 10. Target / costs / reference overlay

Unchanged:

- T40 target;
- primary cost = 10% gross target USD;
- stress cost = 20% gross target USD;
- reference equity USD500;
- structural stop risk <=USD20;
- notional <=USD50,000;
- margin <=USD100 at 1:500;
- 0.01 lot step;
- XAUUSD <=0.10 lot.

## 11. Zero-outcome preflight

Before any target/P&L calculation require:

1. exact decision grid;
2. causal prior-24 range baseline;
3. current bar excluded;
4. candidate-self exclusion;
5. exact rolling peer window t/t-5/t-10;
6. each peer counted at most once;
7. shock threshold VR>=1.75 unchanged;
8. >=4 unique shocked peers;
9. >=6 valid peers;
10. candidate current VR<=1.00;
11. fixed prior-six-M5 box;
12. current close inside box;
13. six-M5 arm horizon;
14. first qualifying breakout only;
15. breakout VR>=1.25;
16. body>=50%;
17. outer-25% close;
18. 50% limit;
19. trigger-extreme stop;
20. active-arm/order suppression;
21. 10-M1 / 30m expiry;
22. safe-overlay caps;
23. each market >=25 filled valid signals;
24. both directions every market;
25. >=300 total;
26. target/P&L outcomes zero;
27. parsed source max <=Jun30;
28. Jul-Aug/Sep unloaded.

The v0.1 opportunity-density gate is deliberately unchanged.

## 12. Development convention if preflight passes

Same six chronological slices.

Outcome:

- T40 vs frozen trigger stop;
- stop first on same-bar target+stop;
- max 120 active M1 bars counting entry;
- 20:00 UTC cutoff;
- timeout marked to last eligible M1 close.

Matched immediate-entry control:

- first active M1 open after same qualified breakout;
- same stop;
- descriptive only.

Diagnostics only:

- unique peer shock count;
- shock ages;
- candidate lag VR;
- trigger VR;
- hour;
- market;
- direction.

No post-outcome cohort whitelist.

## 13. Development gate

Mandatory and unchanged:

- >=120 pooled signals;
- every fold >=8;
- pooled gross normalized expectancy >+0.20R;
- primary normalized expectancy >0;
- stress normalized expectancy >0;
- >=4/6 positive-stress folds;
- reference trades >=90;
- >=35 distinct trade weekdays;
- reference primary/stress expectancy >0;
- primary PF >=1.10;
- stress PF >=1.05;
- stress MDD <=USD150;
- max market share <=60%;
- integrity/provenance pass;
- Jul-Aug/Sep sealed.

## 14. Anti-mining

After outcomes do not alter inside v0.2:

- 15-minute rolling memory length;
- peer shock VR threshold 1.75;
- 4-peer breadth;
- candidate lag VR 1.00;
- six-M5 box;
- six-M5 breakout arm;
- breakout VR 1.25;
- body 50%;
- outer-25%;
- 50% limit;
- stop;
- target;
- costs;
- safety caps;
- gates.

## 15. Outcome state at freeze

- target outcomes: NO;
- P&L outcomes: NO;
- Jul-Aug loaded/labeled: NO;
- Sep loaded/labeled: NO.
