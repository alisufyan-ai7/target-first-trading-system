# Decision Model — Badar Current-Era v0.1

## Status labels

- **CORE** — repeatedly supported by recent live behavior and current teaching.
- **STRONG** — recurring and useful, but not universal.
- **VARIABLE** — implementation changes by context or across eras.
- **UNRESOLVED** — evidence is contradictory or insufficient for a mechanical rule.

The objective is not to force human discretion into false precision.

## State 0 — Environment and event risk

Questions:

- Which session is active?
- Is this near a major session open?
- Is important news imminent or just released?
- Is this month-end / Friday / unusually low-volume or manipulated trading?
- Is the market moving normally enough to interpret lower-timeframe confirmation?

**Status: STRONG, but not a universal hard filter.**

Environment modifies waiting, confirmation standard, risk size and willingness to trade. Exact session and news rules are variable.

## State 1 — Higher-timeframe directional context

Questions:

- What is D1/H4/H1 structure?
- Where did the relevant BOS originate?
- Is the trade aligned, mixed, or counter to H1/daily context?
- Has an HTF close changed the bias?

**Status: CORE.**

Recent anchors:

- `1E65DgTFxe0` — H1 defines sell areas and target; LTF executes.
- `WUblCihXgPU` — counter-trend long receives lower risk; later sell aligns with bearish structure.
- `EOBnMz2Y_9k` — active bias changes after the H1 close, then the retracement is sold.

Direction alone does not trigger a trade.

## State 2 — Meaningful location

Common locations:

- prior session high/low;
- previous-day high/low;
- H4/H1 swing extreme;
- equal highs/lows;
- range extreme;
- unmitigated OB;
- FVG / imbalance;
- breaker;
- BOS origin / continuation base;
- premium/discount area;
- stacked POIs.

**Status: CORE — probably the most important gate.**

Badar repeatedly rejects entries in the middle:

- `mGJ4dtVjlxE` — “It is in the middle, so we let it stay.”
- `wQ5uxbmLlM4` — “This is the center... we will not trade from here.”
- `WUblCihXgPU` — “No sell area, no buy area.”
- `1E65DgTFxe0` — refuses to sell after the move is already extended down; waits for a retracement.
- `CPGcMydNbbQ` — reasons from being at the top/high rather than buying there.

If location is absent: `NO_TRADE`.

If location is approaching: `WAIT`.

## State 3 — Interaction / liquidity event

Common events:

- sweep / stop hunt;
- fake breakout and close back;
- trap candle;
- rejection;
- retracement into OB/FVG;
- range-extreme test;
- repeated test / second confirmation;
- continuation retest into the BOS base.

**Status: STRONG, not universally mandatory.**

The flagship sequence favors `liquidity -> sweep/trap -> confirmation`, but live continuation/retracement entries sometimes occur without a textbook sweep.

Therefore “sweep present” must not be a universal Boolean gate.

## State 4 — Higher-timeframe close gate

Questions:

- Is M15, M30, H1 or H4 close pending?
- Did the close confirm, invalidate or flip the case?
- Was the apparent break only a wick/transient move?

**Status: CORE as a behavioral principle; VARIABLE in exact timeframe.**

`EOBnMz2Y_9k` is especially clear: H1/M30/M15 closes drive the case and M30 close is explicitly emphasized.

Stable principle: **closes matter**.

Unstable detail: exact number of closes / exact timeframe.

## State 5 — Confirmation / trigger

Recurring families:

- momentum / MSS;
- inverse closing / close-back-inside;
- two-candle rejection;
- engulfing / strong opposing close;
- mini-range momentum break;
- strong wickless close;
- FVG/OB retracement after confirming move;
- second confirmation at same zone.

**Status: STRONG that explicit confirmation is common; NOT universal. Decision evidence is CORE, but 20/107 captured trades have no separately coded confirmation family.**

A practical current-era live hierarchy often looks like:

```text
H1 context / area
    -> optional M15/M30 close gate
        -> either:
             M1/M3/M5 execution confirmation
             OR a narrow direct/aggressive structural-location branch
```

M1 is used frequently in recent live execution even though older course material sometimes calls M1 MSS unreliable.

The direct/aggressive branch is legal only when the location is structurally meaningful, the interaction is a sweep or retrace-to-POI, invalidation is defined, the entry is not chasing and no relevant HTF close invalidates the case.

Confirmation quality states:

- STRONG
- ADEQUATE
- WEAK
- FAILED
- NOT_YET

`NOT_YET` generally maps to `WAIT`.

`FAILED` generally maps to `NO_TRADE` or, after entry, `REDUCE_RISK / EXIT_INVALIDATED`.

## State 6 — Execution feasibility

Questions:

- Has price already run away?
- Would entry be chasing?
- Is there a logical structural stop?
- Is the required stop too large for the intended trade?
- Is there enough room before opposing liquidity?
- Is entry at the correct side of the move?
- Can risk be sized appropriately?

**Status: CORE.**

Observed repeatedly:

- skip if stop is too large;
- skip if there is no logical stop;
- do not enter late;
- wait for retracement instead of chasing;
- do not sell lows / buy highs merely because momentum continues.

Hard outputs:

- no logical stop -> `NO_TRADE`
- move already left -> `NO_TRADE` or `WAIT_FOR_RETRACE`

## State 7 — Risk classification

Normal-risk context generally has:

- HTF alignment;
- good location;
- clear confirmation;
- reasonable structural stop;
- normal conditions.

Reduced-risk modifiers repeatedly include:

- countertrend;
- large stop;
- news/event uncertainty;
- weak/low-probability confirmation;
- later/re-entry trade;
- protecting a profitable day;
- choppy market.

**Status: CORE that risk changes with quality; VARIABLE exact percentage.**

v0.1 outputs:

- `NORMAL_RISK`
- `REDUCED_RISK`
- `NO_RISK / SKIP`

Target-First will ultimately impose its own independent account-risk constraints.

## State 8 — Entry decision

### TRADE_NORMAL_RISK

Requires meaningful context, location, feasible structural invalidation and no major unresolved contradiction.

Execution can come from either:

- a strong/adequate confirmation branch; or
- the narrow direct/aggressive branch with aligned context, acceptable stop geometry and no downgrade modifier.

### TRADE_REDUCED_RISK

Still logically valid but with negative modifiers such as countertrend, news, larger stop, weak confirmation, direct/aggressive execution, re-entry/test status or lower confidence.

### WAIT

Use when:

- location not reached;
- sweep/retracement still desired;
- HTF close pending;
- confirmation not closed;
- retracement entry not arrived;
- second confirmation desired;
- market temporarily unclear.

### NO_TRADE

Use when:

- price is in the middle;
- location is not meaningful;
- move has already left and entry would chase;
- structural stop is not definable;
- risk is unacceptable;
- confirmation failed;
- idea is at the wrong extreme;
- relevant HTF close invalidates it;
- there is no clear trade reason.

# Post-entry state machine

## State 9 — Premise monitoring

Monitor:

- M1/M3/M5 reaction;
- relevant M15/M30/H1 closes;
- opposing strong/engulfing/wickless candles;
- expected follow-through;
- new OB/FVG/structure;
- arrival at target liquidity.

## State 10 — Management outputs

### HOLD
Premise remains valid.

### REDUCE_RISK
Used when confirmation disappoints, expected close fails, market becomes abnormal, or enough favorable movement exists to protect.

### PARTIAL
Often at TP1 or nearby opposing liquidity.

### MOVE_PROTECTION
Can be BE, BE+buffer, or structural protection behind a new OB. Exact rule is variable.

### EXIT_INVALIDATED
Manual exits on new candle evidence are common. The original stop is not the only definition of “wrong.”

### RUNNER_TO_LIQUIDITY
Remaining size may target next session extreme, equal highs/lows, HTF swing, imbalance or other opposing liquidity.

# Stable enough to carry forward

## CORE

1. Context before trigger.
2. Meaningful location before confirmation.
3. No trade in the middle.
4. HTF/H1 context matters.
5. Higher-timeframe closes matter.
6. Decision evidence matters; explicit confirmation is common but not universal.
7. When confirmation is used, candle-close behavior matters more than wick alone.
8. Do not chase.
9. A logical structural stop must exist.
10. Reduce risk when quality/confidence is lower.
11. `WAIT` and `NO_TRADE` are first-class decisions.
12. Re-evaluate the premise after entry.
13. Cut/reduce when new price behavior shows the premise is wrong.

## STRONG but not universal

1. Sweep / stop hunt before reversal.
2. Session extremes as liquidity.
3. OB/FVG at or beyond the liquidity location.
4. MSS after sweep.
5. Second confirmation at same zone.
6. Partial + runner structure.

## VARIABLE / unresolved

1. Exact session preference.
2. Exact BOS threshold / close count.
3. Exact ICC body-percentage threshold.
4. Exact MSS timeframe.
5. Exact 2CR timeframe.
6. Exact order type.
7. Exact stop buffer / width.
8. Exact RR minimum.
9. Exact percentage risk.
10. Universal news policy.
11. Whether stop may ever be widened.
12. Maximum trades/day.
13. Exact BE timing.

None of these VARIABLE items should become a frozen machine rule solely from v0.1.

# Forbidden simplifications

Do **not** build:

- `sweep -> trade`;
- `MSS -> trade`;
- `FVG touch -> trade`;
- `engulfing -> trade`;
- `every OB -> trade`;
- `every session high/low sweep -> reverse`;
- `M1 signal -> trade regardless of H1`;
- one global fixed stop/target copied from a selected video.

A faithful formalization must preserve:

`context -> location -> event -> decision evidence (confirmation OR controlled direct branch) -> feasibility -> risk -> decision -> management`.


# Post-corpus formalization

The completed 42-stream decision corpus supersedes any earlier implication that explicit confirmation is universal.

Canonical frozen formal policy:

`formal-policy-v0.1/FORMAL-DECISION-POLICY.md`

Scientific status:

`FORMAL_DECISION_POLICY_V0_1_FROZEN_OUTCOME_BLIND`

No P&L test is authorized until the remaining human-classified inputs are mechanized prospectively.
