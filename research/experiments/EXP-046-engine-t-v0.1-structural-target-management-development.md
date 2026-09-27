# EXP-046 — Engine T v0.1 Structural Target / Management Development Protocol

**Frozen:** 2026-09-28  
**Status:** PROSPECTIVE — BEFORE ANY ENGINE-T POST-ENTRY OUTCOME  
**Candidate engine:** Engine T v0.1  
**Zero-outcome adequacy PASS:** `3f257487ac32b73bcf605e9cc442678bce9ef662`

## 1. Authorization

Engine T v0.1 passed its frozen zero-outcome gate on Jan-2022 through Feb-2025:

- 185 filled candidates;
- 103 SHORT / 82 LONG;
- 167 signal days;
- median 1 candidate per active signal day;
- causality PASS;
- no target, MFE/MAE, win-rate, P&L or post-entry path exposed;
- validation / fresh holdout not loaded.

Post-entry development outcomes are authorized only under this prospectively frozen protocol.

## 2. Scientific isolation

EXP-046 changes the **selection / decision process**, not the Gold outcome economics.

To isolate the failed-auction hypothesis, this protocol deliberately reuses the already prospectively frozen Gold structural-target, cost, sizing, conservative OHLC-ordering, horizon, one-open, and daily-state conventions from EXP-045 wherever applicable.

The experimental question is therefore:

> Does selecting a causal failed auction after established acceptance create enough edge under the same realistic Gold economics?

Do not change target or cost mechanics after seeing Engine-T outcomes.

## 3. Development / protected periods

Outcome development:

- 2022-01-01 through 2025-02-28.

Warm-up:

- 2021-12-01 through 2021-12-31.

Remain sealed:

- validation: 2025-03-01 through 2025-08-31;
- fresh holdout: 2025-09-01 through 2026-02-28.

No Mar-2025+ source file may be loaded by the development evaluator.

## 4. Structural target map at entry

Reconstruct the same causally known daily external-liquidity instances:

- prior active-day high / low;
- Asia 00:00-06:00 UTC high / low, known from 06:00;
- opening range 06:00-09:00 UTC high / low, known from 09:00.

A target level is **fresh at entry** only if:

1. it was known strictly before the candidate fill signal; and
2. no completed active M5 bar strictly attacked it before or exactly at the fill signal.

Attack semantics:

- high-side: M5 high > level;
- low-side: M5 low < level.

The Engine-T attacked entry boundary is already consumed and cannot be a target.

If multiple causally known fresh level classes have the exact same source-tick price, retain one instance using priority:

1. prior-day;
2. Asia;
3. opening range.

The same price cannot serve as both TP1 and TP2.

## 5. Directional target ladder

For LONG:

- eligible targets are fresh external levels strictly above entry.

For SHORT:

- eligible targets are fresh external levels strictly below entry.

Sort by absolute distance from entry, then priority.

### TP1

TP1 = nearest fresh eligible external-liquidity level.

If none exists:

`REJECT_NO_FRESH_STRUCTURAL_TARGET`.

Let:

- `R = abs(entry - stop)`;
- `room1 = abs(TP1-entry) / R`.

Require:

`room1 >= 1.50R`.

Otherwise:

`REJECT_STRUCTURAL_ROOM_LT_1_50R`.

### TP2 / runner

TP2 = next distinct fresh eligible external-liquidity level farther in the trade direction.

Runner is enabled only if:

- TP2 exists; and
- `abs(TP2-entry) / R >= 3.00R`.

Otherwise the whole position exits at TP1.

## 6. Position management

If runner is not enabled:

- 100% exits at TP1.

If runner is enabled:

- 50% exits at TP1;
- 50% remains for TP2;
- on the TP1-hit M1, runner stop remains at original structural stop;
- from the **next market-active M1**, runner stop becomes entry / breakeven;
- runner exits at TP2, breakeven, or timeout.

No discretionary trailing stop, target extension, third target, or recovery behavior.

## 7. Conservative same-bar ordering

Outcome path starts on the first market-active M1 bar strictly after the accepted fill bar. No favorable excursion from the fill M1 is credited.

Before TP1:

- if structural stop and TP1 are both touched in one M1, stop wins.

On TP1-hit M1:

- only TP1 may be credited;
- TP2 cannot be credited until a later active M1.

After TP1, beginning next active M1:

- if breakeven and TP2 are both touched, breakeven wins.

These are conservative OHLC ordering assumptions.

## 8. Intraday horizon

Force exit at the earlier of:

1. 120 market-active M1 bars after entry; or
2. 20:00 UTC on the entry UTC date.

Use the close of the last market-active M1 available at or before the hard cutoff.

No overnight position.

## 9. Research friction

At 0.10 Gold lot:

- primary round-trip friction: USD5;
- stress round-trip friction: USD10.

Scale linearly with actual lot.

Splitting an exit does not reduce total friction.

These remain research assumptions, not broker specifications.

## 10. Reference-account sizing

Reference equity: USD500.

Gold:

- max 0.10 lot;
- lot step 0.01;
- never size above 0.10.

Choose the largest legal lot <=0.10 such that:

`gross structural stop loss + stress friction <= USD40`.

For lot `L`:

- Gold P&L per USD1 move = `100 * L` USD;
- stress friction = `USD100 * L`;
- primary friction = `USD50 * L`.

If safe lot <0.01:

`REJECT_SAFE_LOT_BELOW_MINIMUM`.

Never shrink the structural stop.

## 11. One-open / simultaneous-candidate rule

Permit one open Gold trade at a time.

Candidates are considered by fill-signal timestamp.

If multiple outcome-tradeable candidates have the exact same fill timestamp:

1. higher TP1 room-R wins;
2. then smaller structural-stop distance;
3. then candidate ID lexical order.

Any later candidate whose fill signal occurs before the current trade exits is blocked.

## 12. Daily state machine

Use primary net realized P&L:

- if realized UTC-day P&L <= -USD40, add no new risk that day;
- if realized UTC-day P&L >= +USD150, add no new risk that day;
- otherwise later qualified candidates may trade if no position is open.

No recovery sizing, martingale, or risk increase to hit the strong-day zone.

## 13. Metrics

Report:

### Signal level

- pre-target candidates;
- target-admitted / rejected counts and reasons;
- TP1 room-R distribution;
- runner-eligible count;
- STOP / TP1 / TP2 / breakeven / timeout outcomes;
- TP1 hit rate;
- TP2 hits;
- gross R expectancy;
- primary net R expectancy;
- stress net R expectancy;
- primary / stress R profit factor;
- three-era stability.

### Reference account

- actual trades;
- blocked due one-open;
- blocked due daily state;
- lot distribution;
- primary / stress USD expectancy per trade;
- primary / stress PF;
- total primary / stress P&L;
- primary / stress max drawdown;
- distinct trade weekdays;
- trades per all development weekday including zero-trade days;
- mean / median daily P&L;
- losing-day percentage;
- <=USD50 day percentage;
- >=USD100 / >=USD150 / >=USD200 day percentages;
- rolling 5-day distribution;
- consecutive losing days;
- consecutive <=USD50 days.

## 14. Stability eras

Predeclare:

- ERA1: 2022-01-01 through 2022-12-31;
- ERA2: 2023-01-01 through 2023-12-31;
- ERA3: 2024-01-01 through 2025-02-28.

No era may be removed after outcomes.

## 15. Development promotion gate

Because zero-outcome preflight produced 185 candidates across 167 days, Engine T advances to sealed validation only if **all** conditions pass:

1. >=80 target-admitted signal trades;
2. >=60 reference-account actual trades;
3. >=50 distinct reference trade weekdays;
4. pooled gross normalized-R expectancy > +0.20R;
5. pooled primary normalized-R expectancy > 0;
6. pooled stress normalized-R expectancy > 0;
7. primary R PF >=1.10;
8. stress R PF >=1.05;
9. stress normalized-R expectancy >0 in at least 2 of 3 eras;
10. reference-account primary expectancy >0 USD/trade;
11. reference-account stress expectancy >0 USD/trade;
12. reference primary PF >=1.10;
13. reference stress PF >=1.05;
14. stress maximum drawdown <=USD150;
15. protected periods remain sealed.

The sample floors are frozen from zero-outcome density only, before any Engine-T post-entry result is inspected.

## 16. Disposition

If every gate passes:

`ENGINE_T_READY_FOR_SEALED_VALIDATION`.

Otherwise:

`ENGINE_T_FAIL_CLOSE_BEFORE_VALIDATION`.

A development PASS authorizes validation design/execution only, not live trading.

## 17. Pinned zero-outcome artifacts

The evaluator must abort if either changes:

- preflight JSON Git blob: `47cb4fb8b28f96469ead35e5332789e618fd9291`;
- immutable candidate JSONL Git blob: `975cf5ca15c532db44857a94bbb3baabf2d26919`.

## 18. Governance

This protocol is frozen before any Engine-T post-entry outcome is inspected.

Do not change after outcomes:

- target freshness;
- 1.50R TP1 room;
- 3.00R runner threshold;
- 50/50 partial;
- breakeven timing;
- same-bar ordering;
- 120-active-M1 / 20:00 exit;
- costs;
- sizing;
- one-open rule;
- daily state;
- development gate.

If development fails, close Engine T rather than tuning it on the same sample.
