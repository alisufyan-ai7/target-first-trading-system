# Engine Q v0.1 — Cross-Market Volatility Spillover Breakout

**Engine ID:** engine-q-cross-market-volatility-spillover-breakout  
**Version:** 0.1  
**Experiment:** EXP-037  
**Status:** PROSPECTIVELY FROZEN — ZERO OUTCOMES — 2026-09-24

## 1. Thesis

Engine P showed that contemporaneous cross-market **directional** consensus did not create enough pre-cost edge.

Engine Q changes the information source and causal question.

It asks:

> When several other liquid markets experience a synchronized volatility impulse while one candidate market is still locally compressed/lagging, does the candidate's first subsequent local breakout contain a repeatable target-first continuation edge?

Peer information is **directionless volatility breadth**, not directional factor confirmation.

This is not Engine P v0.2:

- no MOM threshold;
- no USD_SCORE;
- no shared directional factor;
- no EURJPY leg-direction confirmation;
- no post-hoc P diagnostics used for parameter selection.

## 2. Markets

Execution-research universe remains:

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

Every candidate uses the other seven markets as possible volatility peers. The candidate itself is always excluded from peer breadth.

## 3. Data protection / split

Reusable development source only:

- source rows no later than **2026-06-30 23:59 UTC**;
- reusable source begins **2026-03-23** for warm-up/state construction;
- development evaluation uses the same six fixed chronological slices:
  - WF1: 2026-04-13 to 2026-04-27
  - WF2: 2026-04-27 to 2026-05-11
  - WF3: 2026-05-11 to 2026-05-25
  - WF4: 2026-05-25 to 2026-06-08
  - WF5: 2026-06-08 to 2026-06-22
  - WF6: 2026-06-22 to 2026-07-01 (hard source seal before Jul-01)

Protected and unavailable to v0.1 preflight/development:

- Jul-Aug secondary test;
- Sep final holdout.

No protected row may be loaded, labeled, summarized, or used for threshold selection before the complete development gate passes.

## 4. Decision grid

Candidate-arm decisions are evaluated on every completed UTC-aligned M5 bar with completion time:

`06:05, 06:10, ..., 17:25 UTC`.

The earlier 17:25 final arm time leaves a full 30-minute breakout-arm window before the no-new-entry 18:00 cutoff.

One active Engine-Q arm/order per symbol at a time. New same-symbol opportunities while an arm/order is active are suppressed, not queued.

## 5. Per-market range-vol state

For every market i at decision time t:

- current completed M5 range: `R_i(t) = high-low`;
- baseline = the **prior 24 contiguous completed M5 bars**, excluding the current bar;
- `V_i(t) = even median(prior 24 M5 ranges)`;
- require `V_i(t) > 0`;
- `VR_i(t) = R_i(t) / V_i(t)`.

All calculations use completed bars only.

## 6. Cross-market volatility breadth arm

For candidate S:

- exclude S from the peer set;
- require at least **6 valid peers** among the other seven;
- a peer is in shock when `VR_peer >= 1.75`;
- require at least **4 shocked peers**.

This is directionless. Peer up/down direction is ignored.

Frozen breadth rule:

`PEER_SHOCK_COUNT >= 4 of 7, with >=6 valid peers`.

## 7. Candidate lag/compression requirement

At the same decision time t, candidate S must still be lagging the cross-market volatility impulse.

Define from the six completed candidate M5 bars immediately preceding the current decision bar:

- `BOX_HI = max(high)`;
- `BOX_LO = min(low)`.

Require:

- candidate current-bar `VR_S <= 1.00`;
- current candidate close strictly inside `(BOX_LO, BOX_HI)`.

The fixed `BOX_HI/BOX_LO` are frozen at arm creation and are not rolled forward while the arm is active.

## 8. Breakout trigger after arm

After a valid breadth+lag arm, observe at most the **next six completed candidate M5 bars** (30 minutes).

The first bar that satisfies either side becomes the trigger.

For trigger bar B:

- use the candidate's same frozen 24-M5 baseline convention available causally at B;
- `VR_B >= 1.25`;
- `BODY = abs(close-open) >= 50% of range`.

LONG breakout:

- close > frozen `BOX_HI`;
- close > open;
- `high-close <= 25% of range`.

SHORT breakout:

- close < frozen `BOX_LO`;
- close < open;
- `close-low <= 25% of range`.

If no trigger appears inside six completed M5 bars, the arm expires with no trade.

Peer direction is never used to choose LONG or SHORT; direction comes only from the candidate's own breakout.

## 9. Non-chasing execution

After the qualifying breakout trigger:

`LIMIT = (trigger high + trigger low)/2`.

LONG:

- require LIMIT < trigger close;
- stop = trigger low - one research tick.

SHORT:

- require LIMIT > trigger close;
- stop = trigger high + one research tick.

Limit order life:

- next 10 active M1 bars;
- hard expiry = trigger decision +30 minutes;
- no entry at/after 18:00 UTC;
- gap through stop before limit cancels;
- same-bar target/stop ambiguity at outcome stage is stop first.

## 10. Target, costs and reference-account overlay

Target:

- unchanged project **T40** target geometry;
- no post-outcome target switching.

Frozen research costs:

- primary transaction-cost stress = **10% of gross target USD**;
- stress transaction-cost stress = **20% of gross target USD**.

Signal-first safe-lot overlay remains unchanged:

- reference equity: USD500;
- structural stop risk <=USD20;
- notional <=USD50,000;
- margin <=USD100 at research 1:500;
- 0.01 lot step;
- XAUUSD <=0.10 lot.

Report utility bands GE40 / GE30 / LT30 / NONDEPLOYABLE.

The USD40 normal daily stop and USD60 emergency ceiling remain portfolio/daily-state rules, not per-trade risk allowances.

## 11. Zero-outcome preflight gate

Before any target/P&L outcome, verify:

1. exact M5 decision grid;
2. current bar excluded from every 24-M5 baseline;
3. even-median range state;
4. candidate-self exclusion from peer breadth;
5. >=6 valid peers;
6. peer shock boundary `VR>=1.75`;
7. shock breadth boundary >=4 peers;
8. candidate lag `VR<=1.00`;
9. fixed prior-six-M5 box;
10. current close inside fixed box;
11. arm horizon exactly next six completed M5 bars;
12. first qualifying breakout only;
13. breakout `VR>=1.25`;
14. breakout body >=50%;
15. outer-25% close;
16. 50% retracement limit;
17. stop beyond trigger extreme;
18. pending/arm suppression;
19. 10-active-M1 / 30m expiry;
20. safe-overlay caps;
21. each market >=25 filled valid signals;
22. LONG + SHORT on every market;
23. >=300 total filled valid signals;
24. target/P&L outcomes remain zero;
25. source max timestamp <=2026-06-30 23:59 UTC;
26. Jul-Aug and Sep remain unloaded/unlabeled.

If the frequency gate fails, stop before outcomes. Do not lower it post hoc.

## 12. Frozen development convention if preflight passes

Use exactly the six fixed slices in section 3.

Outcome:

- target = T40;
- stop = frozen breakout-bar structural stop;
- same-bar target+stop = stop first;
- max outcome horizon = 120 active M1 bars counting entry bar;
- hard session cutoff = 20:00 UTC;
- timeout marked to last eligible M1 close.

Matched immediate-entry control:

- same non-suppressed qualified breakout trigger;
- entry = first active M1 open at/after trigger completion;
- same structural stop;
- descriptive only.

Diagnostics are descriptive only:

- peer shock count;
- peer VR distribution;
- candidate lag VR;
- breakout VR;
- hour;
- market;
- direction.

No post-outcome shock-count, VR, hour, market or direction whitelist is permitted inside v0.1.

## 13. Frozen development gate

Mandatory:

1. >=120 pooled signals;
2. every fold >=8 signals;
3. pooled gross normalized expectancy >+0.20R;
4. pooled primary normalized expectancy >0;
5. pooled stress normalized expectancy >0;
6. >=4/6 positive-stress folds;
7. reference-account trades >=90;
8. >=35 distinct trade weekdays;
9. reference primary expectancy >0;
10. reference stress expectancy >0;
11. primary PF >=1.10;
12. stress PF >=1.05;
13. stress MDD <=USD150;
14. no market >60% of reference-account trades;
15. integrity/provenance pass;
16. Jul-Aug and Sep sealed.

Any mandatory failure stops before secondary testing.

## 14. Anti-mining

Do not change after outcomes inside v0.1:

- eight-market universe;
- peer set / self-exclusion;
- 24-M5 baseline;
- peer VR threshold 1.75;
- breadth count 4;
- candidate VR ceiling 1.00;
- fixed six-M5 box;
- six-M5 arm horizon;
- breakout VR 1.25;
- body 50%;
- outer-25% close;
- 50% limit;
- order life;
- stop;
- T40;
- costs;
- safety caps;
- development gates.

A redesign requires a new experiment/version.

## 15. Outcome state at freeze

- Engine-Q target outcomes: **NO**;
- Engine-Q P&L outcomes: **NO**;
- Jul-Aug loaded/labeled: **NO**;
- Sep loaded/labeled: **NO**.
