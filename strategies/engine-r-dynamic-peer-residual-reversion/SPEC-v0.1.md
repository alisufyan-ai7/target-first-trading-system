# Engine R v0.1 — Dynamic Peer-Residual Reversion

**Engine ID:** engine-r-dynamic-peer-residual-reversion  
**Version:** 0.1  
**Experiment:** EXP-039  
**Status:** PROSPECTIVELY FROZEN — ZERO OUTCOMES — 2026-09-25

## 1. Thesis

Engine P tested directional cross-market factor confirmation and failed development.

Engine Q tested directionless cross-market volatility spillover followed by a lagging-market breakout and failed development.

Engine R changes both the information source and trade thesis.

It asks:

> When one market has a stable recent co-movement relationship with another liquid market, and the candidate becomes materially displaced from the move implied by that strongest peer, does the candidate's first same-bar rejection back toward the peer relationship produce a repeatable target-first mean-reversion entry?

This is a **dynamic cross-market relative-value residual** family.

It is not:

- Engine P factor consensus;
- Engine Q peer-volatility breadth;
- Engine O isolated-symbol statistical stretch;
- a post-hoc symbol/hour whitelist.

## 2. Markets

Same eight execution-research markets:

- XAUUSD
- EURUSD
- GBPUSD
- USDJPY
- EURJPY
- AUDUSD
- USDCAD
- USDCHF

For every candidate, the candidate itself is excluded from its peer set.

## 3. Protected data / split

Reusable source only:

- state source begins 2026-03-23;
- hard source seal: **2026-06-30 23:59 UTC**.

If development is later permitted, use the same six fixed folds:

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

Evaluate every completed UTC-aligned M5 bar:

`06:05, 06:10, ..., 17:55 UTC`.

One active Engine-R pending order per symbol at a time. New same-symbol setup while pending is suppressed, not queued.

## 5. Causal state window

At candidate decision time t, for every market:

- use completed M5 bars only;
- current bar is allowed only for the current dislocation and rejection trigger;
- relationship estimation excludes the current bar.

Require at least 51 contiguous completed M5 bars before the current bar.

### 5.1 Prior 48 one-bar returns

For the 49 completed M5 closes ending immediately before the current bar, form exactly 48 close-to-close returns.

These 48 returns are used only to estimate candidate/peer co-movement.

### 5.2 Prior 48 fifteen-minute moves

For the 48 completed M5 endpoints immediately before the current bar, calculate:

`MOVE15_i = close_i / close_(i-3) - 1`.

Define:

`SCALE15 = even median(abs(MOVE15_i))`.

Require SCALE15 > 0.

### 5.3 Current normalized 15-minute move

At current completed M5 bar t:

`MOVE15_NOW = close_t / close_(t-3) - 1`.

`NM15 = MOVE15_NOW / SCALE15`.

The current bar is excluded from SCALE15.

## 6. Dynamic strongest peer

For candidate S, evaluate every other market P using the prior 48 one-bar returns.

Calculate Pearson correlation:

`RHO(S,P)`.

Require finite nonzero variance for both return series.

Select the peer with maximum absolute correlation.

Tie-break deterministically by lexicographically smaller peer symbol.

Frozen relationship gate:

`abs(RHO) >= 0.60`.

No fixed USD-factor mapping is used.

## 7. Peer-led residual

For selected peer P:

Require:

`abs(NM15_peer) >= 1.00`.

Define sign-adjusted peer move:

`PEER_EXPECTED = sign(RHO) * NM15_peer`.

Define candidate residual:

`RESID = NM15_candidate - PEER_EXPECTED`.

Frozen dislocation threshold:

`abs(RESID) >= 1.50`.

Interpretation:

- RESID >= +1.50: candidate is too strong relative to peer -> seek SHORT reversion;
- RESID <= -1.50: candidate is too weak relative to peer -> seek LONG reversion.

The peer determines relative-value expectation; the candidate determines executable direction.

## 8. Current-bar reversion confirmation

The current completed candidate M5 bar must already reject in the reversion direction.

Let:

- R = high-low;
- BODY = abs(close-open).

Require:

- R > 0;
- BODY >=35% of R.

LONG reversion:

- close > open;
- high-close <=40% of R.

SHORT reversion:

- close < open;
- close-low <=40% of R.

No future breakout arm is used.

## 9. Non-chasing execution

Frozen entry:

`LIMIT = (high+low)/2` of the completed rejection bar.

LONG:

- LIMIT < close;
- stop = bar low - one research tick.

SHORT:

- LIMIT > close;
- stop = bar high + one research tick.

Order life:

- next 10 active M1 bars;
- hard expiry decision+30m;
- no entry at/after 18:00 UTC;
- gap through stop before limit cancels.

## 10. Target / costs / safe-lot overlay

Unchanged project conventions:

- target = T40;
- primary cost = 10% of gross target USD;
- stress cost = 20% of gross target USD;
- reference equity USD500;
- structural stop risk <=USD20;
- notional <=USD50,000;
- margin <=USD100 at research 1:500;
- 0.01 lot step;
- XAUUSD <=0.10 lot.

Report GE40 / GE30 / LT30 / NONDEPLOYABLE.

## 11. Zero-outcome preflight gate

Before any target/P&L outcome, verify:

1. exact decision grid;
2. completed-bar causality;
3. exact 48 prior one-bar returns;
4. exact 48 prior 15m moves;
5. current bar excluded from relationship/scale estimation;
6. even-median SCALE15;
7. exact current 15m reference;
8. candidate excluded from peer search;
9. Pearson correlation calculation;
10. deterministic strongest-peer tie-break;
11. abs correlation boundary >=0.60;
12. peer normalized move boundary >=1.00;
13. residual definition/sign;
14. residual boundary >=1.50;
15. reversion direction mapping;
16. 35% body boundary;
17. outer-40% close boundary;
18. 50% non-chasing limit;
19. structural stop;
20. pending-order suppression;
21. 10-active-M1 / 30m expiry;
22. safe-overlay caps;
23. each market >=25 filled valid signals;
24. LONG + SHORT every market;
25. >=300 total filled valid signals;
26. target outcomes zero;
27. P&L outcomes zero;
28. parsed source max <=2026-06-30 23:59 UTC;
29. Jul-Aug and Sep unloaded/unlabeled.

If opportunity density fails, stop before outcomes. Do not lower the gate post hoc.

## 12. Frozen development convention if preflight passes

Use the same six fixed chronological slices.

Outcome:

- T40 vs frozen rejection-bar structural stop;
- same-bar target+stop = stop first;
- max 120 active M1 bars counting entry;
- hard 20:00 UTC cutoff;
- timeout marked to last eligible M1 close.

Matched immediate-entry control:

- same non-suppressed qualified Engine-R setup;
- first active M1 open after decision;
- same stop;
- descriptive only.

Diagnostics are descriptive only:

- selected peer;
- abs correlation;
- candidate NM15;
- peer NM15;
- residual;
- hour;
- market;
- direction.

No post-outcome peer/correlation/residual/hour/market/direction whitelist is permitted inside v0.1.

## 13. Frozen development gate

Mandatory:

1. >=120 pooled signals;
2. every fold >=8;
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
14. no market >60%;
15. integrity/provenance pass;
16. protected periods sealed.

Any mandatory failure stops before secondary testing.

## 14. Anti-mining

Do not alter after outcomes inside v0.1:

- 48-return relationship window;
- 48-move scale window;
- Pearson peer selection;
- abs correlation threshold 0.60;
- peer NM15 threshold 1.00;
- residual threshold 1.50;
- body 35%;
- outer-40% close;
- 50% limit;
- order life;
- stop;
- T40;
- costs;
- safety caps;
- gates.

A redesign requires a new experiment/version.

## 15. Outcome state at freeze

- Engine-R target outcomes: **NO**;
- Engine-R P&L outcomes: **NO**;
- Jul-Aug loaded/labeled: **NO**;
- Sep loaded/labeled: **NO**.
