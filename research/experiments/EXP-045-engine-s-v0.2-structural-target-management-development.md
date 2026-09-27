# EXP-045 — Engine S v0.2 Structural Target / Management Development Protocol

**Frozen:** 2026-09-28  
**Status:** PROSPECTIVE — BEFORE ANY ENGINE-S POST-ENTRY OUTCOME  
**Candidate engine:** Engine S v0.2  
**Zero-outcome adequacy PASS:** `835af4eb6a1b76026cf0f04c46ce06840d2ff287`

## 1. Authorization

The unchanged Engine-S v0.2 rules passed the final zero-outcome sample gate on Jan-2022 through Feb-2025:

- 160 filled candidates;
- 126 rejection;
- 34 acceptance;
- both directions in both branches;
- 151 signal days;
- causality PASS;
- zero target/P&L information exposed.

Post-entry development outcomes are now authorized only under this prospectively frozen protocol.

## 2. Development / protected periods

Outcome-development:

- 2022-01-01 through 2025-02-28.

Warm-up:

- 2021-12-01 through 2021-12-31.

Remain sealed:

- validation: 2025-03-01 through 2025-08-31;
- fresh holdout: 2025-09-01 through 2026-02-28;
- later 2026 periods remain outside this experiment.

## 3. Structural target map at entry

Reconstruct the same causally known daily external-liquidity instances used by Engine S:

- prior active-day high / low;
- Asia 00:00-06:00 UTC high / low, known from 06:00;
- opening-range 06:00-09:00 UTC high / low, known from 09:00.

A target level is **fresh at entry** only if:

1. it was known before the candidate fill signal;
2. no completed active 5m bar strictly attacked it before the candidate fill signal, using the same Engine-S attack semantics:
   - high-side attacked when 5m high > level;
   - low-side attacked when 5m low < level.

The candidate's own attacked source level is therefore already consumed and cannot be a target.

## 4. Directional target ladder

For LONG:

- eligible targets are fresh external levels strictly above entry.

For SHORT:

- eligible targets are fresh external levels strictly below entry.

Sort by absolute distance from entry.

### TP1

TP1 = nearest fresh eligible external-liquidity level.

If none exists:

`REJECT_NO_FRESH_STRUCTURAL_TARGET`.

### Structural-room gate

Let:

- `R = abs(entry - stop)`;
- `reward1 = abs(TP1 - entry)`;
- `room_R = reward1 / R`.

Candidate is outcome-tradeable only if:

`room_R >= 1.50`.

Otherwise:

`REJECT_STRUCTURAL_ROOM_LT_1_50R`.

The 1.50R floor is frozen before outcomes and is consistent with the observed Badar TP1 example near 1.6R.

### TP2 / runner eligibility

TP2 = next fresh eligible external-liquidity level farther in the trade direction.

Runner is enabled only if:

- TP2 exists; and
- `abs(TP2-entry)/R >= 3.00`.

Otherwise the entire position exits at TP1.

The 3.00R runner threshold is frozen before outcomes and is consistent with the observed staged Gold example reaching roughly 3R after TP1.

## 5. Position management

### No runner

If TP2 is not runner-eligible:

- 100% position exits at TP1.

### Runner enabled

If TP2 is runner-eligible:

- 50% exits at TP1;
- 50% remains for TP2;
- runner stop remains at the original structural stop on the TP1-hit M1 bar;
- from the **next market-active M1 bar**, runner stop becomes entry/breakeven;
- runner exits at TP2, breakeven, or time exit.

No trailing stop, discretionary extension or third target is allowed.

## 6. Same-bar ordering

Before TP1:

- if one M1 bar touches both structural stop and TP1, **stop wins**.

TP1/TP2 same M1 bar:

- only TP1 is credited;
- runner cannot reach TP2 until a later active M1 bar.

After TP1, from the next active M1 bar:

- if runner breakeven and TP2 are both touched in one M1 bar, breakeven wins.

These are conservative OHLC-ordering rules.

## 7. Intraday horizon

A trade is force-closed at the earlier of:

1. 120 market-active M1 bars after entry; or
2. 20:00 UTC of the entry UTC date.

For timeout exit:

- use the close of the last market-active M1 bar available at/before the hard cutoff;
- no position is carried overnight.

## 8. Research friction

Use the repository's existing Gold research convention.

At 0.10 lot:

- primary round-trip friction: USD 5;
- stress round-trip friction: USD 10.

Scale friction linearly with actual lot.

For partial/runner management, total friction is charged once on total round-trip traded volume; splitting the exit does not reduce friction.

These are research assumptions, not broker specifications.

## 9. Reference-account sizing

Reference equity remains USD 500.

Gold lot:

- maximum 0.10 lot;
- research lot step 0.01;
- never size above the Gold anchor.

Choose the largest legal lot <=0.10 such that:

`gross structural stop loss + stress friction <= USD 40`.

For lot `L`:

- Gold P&L per USD1 move = `100 * L` USD;
- stress friction = `USD 100 * L`;
- primary friction = `USD 50 * L`.

If safe lot <0.01:

`REJECT_SAFE_LOT_BELOW_MINIMUM`.

Do not shrink the structural stop.

## 10. One-open / simultaneous candidate rule

Engine-S reference-account simulation permits one open Gold trade at a time.

Candidates are considered by fill-signal timestamp.

For multiple outcome-tradeable candidates with the exact same fill timestamp:

1. higher TP1 structural room in R wins;
2. then smaller structural-stop distance;
3. then candidate ID lexical order.

Any later candidate whose fill signal occurs before the current trade exits is blocked.

## 11. Daily state machine

Use primary net realized P&L for the reference-account daily state:

- if realized day P&L <= -USD 40, add no new risk that UTC day;
- if realized day P&L >= +USD 150, add no new risk that UTC day;
- otherwise later qualified Engine-S candidates may trade if no position is open.

No recovery sizing.

## 12. Metrics

Report for combined Engine S and separately for REJECTION / ACCEPTANCE:

### Signal-level

- pre-target candidates;
- structural-target admitted / rejected counts;
- TP1 room-R distribution;
- runner-eligible count;
- stop-first / TP1 / TP2 / breakeven / timeout outcomes;
- TP1 hit rate;
- TP2 hit rate among runner-eligible;
- gross R expectancy;
- primary net R expectancy;
- stress net R expectancy;
- primary and stress R profit factor.

### Reference account

- actual trades;
- blocked due one-open;
- blocked due daily state;
- lot distribution;
- primary/stress expectancy USD per trade;
- primary/stress profit factor;
- total primary/stress P&L;
- maximum primary/stress drawdown;
- distinct trade weekdays;
- trades per all development weekday including zero-trade days;
- mean/median daily P&L;
- losing-day percentage;
- <=USD50 day percentage;
- >=USD100 / >=USD150 / >=USD200 day percentages;
- 5-day rolling P&L distribution;
- consecutive losing days;
- consecutive <=USD50 days.

## 13. Stability eras

Development stability is reported on three predeclared eras:

- ERA1: 2022-01-01 through 2022-12-31;
- ERA2: 2023-01-01 through 2023-12-31;
- ERA3: 2024-01-01 through 2025-02-28.

No year/era may be removed after seeing outcomes.

## 14. Branch-specific promotion

Engine S is a family with two predeclared specialized branches:

- Engine S-R = REJECTION;
- Engine S-A = ACCEPTANCE.

Each branch is evaluated independently for promotion.

### Rejection minimum sample

After structural-room admission:

- >=60 signal trades;
- >=40 reference-account actual trades;
- >=35 distinct reference trade weekdays.

### Acceptance minimum sample

After structural-room admission:

- >=25 signal trades;
- >=20 reference-account actual trades;
- >=18 distinct reference trade weekdays.

These floors were frozen using zero-outcome counts only.

## 15. Development edge gate per branch

A branch advances to sealed validation only if **all** applicable conditions pass:

1. branch sample floor passes;
2. pooled gross normalized-R expectancy > +0.20R;
3. pooled primary normalized-R expectancy > 0;
4. pooled stress normalized-R expectancy > 0;
5. primary R profit factor >=1.10;
6. stress R profit factor >=1.05;
7. stress normalized-R expectancy >0 in at least 2 of 3 eras;
8. reference-account primary expectancy >0 USD/trade;
9. reference-account stress expectancy >0 USD/trade;
10. reference-account primary profit factor >=1.10;
11. reference-account stress profit factor >=1.05;
12. stress maximum drawdown <=USD150;
13. no validation/holdout data loaded.

No single combined-family result may rescue a branch that fails its own gate.

## 16. Combined family

Combined Engine-S metrics are descriptive.

Only branches passing their own frozen development gate are eligible to enter the later candidate/ranking architecture.

If neither branch passes:

`ENGINE_S_FAIL_CLOSE_BEFORE_VALIDATION`.

If exactly one branch passes:

`ENGINE_S_ONE_BRANCH_READY_FOR_VALIDATION`.

If both pass:

`ENGINE_S_BOTH_BRANCHES_READY_FOR_VALIDATION`.

## 17. Governance

This specification was frozen before any Engine-S post-entry path was inspected.

Do not change:

- target freshness;
- 1.50R TP1 room;
- 3.00R runner threshold;
- 50/50 partial;
- breakeven timing;
- 120-active-M1 / 20:00 horizon;
- cost assumptions;
- sizing rule;
- branch gates

after development outcomes are produced.

A development PASS authorizes **validation design/execution only**, not live trading.


## Pre-run target-map clarifications

These are frozen before any Engine-S post-entry outcome is calculated.

1. **Same-timestamp freshness:** a target level is fresh only if its first completed-active-5m attack close is strictly **after** the candidate fill-signal timestamp. Therefore a level attacked by a 5m bar closing exactly at the fill-signal timestamp is not fresh.

2. **Exact-price duplicates:** if multiple causally known fresh level classes have the exact same source-tick price, keep one target instance using priority:
   - prior-day high/low;
   - Asia high/low;
   - opening-range high/low.
   The same price cannot serve as both TP1 and TP2.

3. **Outcome path start:** post-entry outcome scanning begins with the first market-active M1 bar strictly after the accepted fill bar. No favorable excursion from the fill M1 bar is credited.

Pinned zero-outcome artifacts:

- extended preflight result Git blob: `717b3f99edd58d47d3e7088b845ddb8a4d0a4583`;
- immutable accepted-candidate JSONL Git blob: `e49f13b7b558ccd4b35130596ec103eedc800b55`.

The development evaluator must abort if either blob changes.
