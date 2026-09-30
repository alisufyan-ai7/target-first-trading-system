# State Derivation Contract — Mechanization v0.1

## Principle

Every state must be derivable from information visible **at or before the candidate timestamp**.

If a raw rule is not supported strongly enough by Badar's source evidence, output `UNRESOLVED`; do not invent a threshold.

---

# 1. Source-supported primitive map

## Machine-ready or near-machine-ready primitives

### Previous-day high / low

- `PDH = previous completed trading-day high`
- `PDL = previous completed trading-day low`

### Session highs / lows

Freeze the completed or currently active session window first, then use its observed high/low.

No future extension of the session range is permitted at the candidate timestamp.

### FVG

Source-supported rule:

- bullish FVG = candle-1 high < candle-3 low;
- bearish FVG = candle-1 low > candle-3 high;
- candle 3 must be closed;
- if candle 3's wick re-enters candle 1's range, the clean-FVG condition fails.

An FVG is invalidated once a candle closes through it.

### Premium / discount

For a frozen BOS/dealing-range leg:

- midpoint = 0.5 of the leg;
- bullish continuation preference = discount;
- bearish continuation preference = premium.

The leg anchor must be frozen before the candidate: origin of the move that produced the BOS to the new extreme.

### Liquidity sweep

High-side sweep:

1. price trades above a pre-existing liquidity level;
2. the next completed candidate-timeframe candle closes back below/inside that level.

Low-side sweep is the mirror.

Same-candle wick-through-and-close-back is recorded as `WEAK_SWEEP` until the next lower-timeframe close is available.

Do **not** use the historical 35-pip teaching cutoff as a universal modern rule; the source itself is contradictory and era-dependent.

### BOS / MSS — high-confidence structural version

A high-confidence break requires:

- a pre-identified swing/base; and
- at least 2 closes beyond that reference on the analysis timeframe or one timeframe lower.

A single close beyond is recorded separately as `SINGLE_CLOSE_BREAK`, not silently upgraded to a confirmed BOS/MSS.

This preserves the source's 2-close teaching while retaining live one-close evidence as a weaker state.

---

# 2. Semi-mechanized primitives

The following can be drawn prospectively but still contain source ambiguity.

## Order block

Minimum source-supported validity:

1. candidate candle/base is the last opposite candle or accepted hidden-OB junction before an impulsive move;
2. the move produces a structural break;
3. the zone has not already been closed through / fully invalidated;
4. first touch is preferred; already mitigated zones are tagged `TESTED`.

Because the source contains several OB shape variants, record:

- `OB_CLASSIC`
- `OB_TWO_CANDLE`
- `OB_HIDDEN`
- `OB_UNRESOLVED`

Do not force them into one candle-shape formula yet.

## Equal highs / lows

Source identifies clustered/double highs/lows as liquidity but provides no stable tolerance.

Until a tolerance is frozen independently of P&L:

- exact/effectively identical chart-marked pairs may be annotated;
- automated price-distance clustering remains `UNRESOLVED`.

## Swing selection

The source distinguishes major/external from minor/internal swings but does not supply one universal fractal width.

Therefore:

- H4/H1 visually established external swing = allowed annotation;
- raw-OHLC fractal lookback parameter = `UNRESOLVED`.

---

# 3. Location state

Inputs:

- candidate direction;
- active structural POIs frozen before candidate;
- current price relative to those POIs;
- active range/dealing-range side;
- interaction family.

## VALID

`VALID` if current price is touching/inside a pre-identified eligible POI or liquidity extreme that is directionally coherent with the candidate.

Directionally coherent includes:

- LONG from lower/range-low/discount/demand/liquidity-below context;
- SHORT from upper/range-high/premium/supply/liquidity-above context;
- continuation retest after a valid structural break in the candidate direction.

A lower-timeframe candle pattern by itself cannot make location VALID.

## APPROACHING

A valid candidate POI is pre-identified but current price has not yet touched/entered it.

## MIDDLE

Price lies between the active lower and upper structural boundaries and is not touching any eligible POI.

## WRONG_EXTREME

Absent a valid continuation-breakout/retest context:

- LONG at the active upper/range-high/premium extreme;
- SHORT at the active lower/range-low/discount extreme.

## ABSENT

No eligible candidate POI has been identified prospectively.

## UNRESOLVED

Use when overlapping/competing POIs make the state non-unique.

### Current reproducibility status

Partially mechanized.

The existing corpus has:

- `location_present` populated on 347/347 events;
- `location_position` non-UNKNOWN on 200/347 events;
- zero TRADE events with `location_present != YES`;
- zero TRADE events labelled MIDDLE.

A blinded chart pass is still required for true reproducibility.

---

# 4. Confirmation state

First freeze a `reference_boundary` and `confirmation_family` before evaluating the completed candle.

## FAILED

Use when the completed confirmation candle:

- closes through the candidate's invalidating side / opposite structural boundary; or
- explicitly fails the family rule and closes in the opposing direction strongly enough to invalidate the candidate.

## NOT_YET

Required confirmation candle is still open or the second required candle has not closed.

## STRONG

At least one of:

1. confirmed BOS/MSS with >=2 closes beyond the frozen reference;
2. two independent source-supported confirmations at the same zone;
3. a valid confirmation family plus an HTF close that independently confirms the same direction.

## ADEQUATE

One completed source-supported confirmation family is valid at a VALID location, with no opposing HTF invalidation.

Examples:

- inverse close meeting its family rule;
- 2CR completed;
- close-back-inside after fake break;
- valid engulf / momentum close;
- completed MSS variant.

## WEAK

Directional evidence exists but does not meet STRONG/ADEQUATE criteria.

Examples:

- single structural close where 2 are required for confirmed BOS/MSS;
- first counter-signal at the zone while the next confirming candle is still desired;
- directional close that does not complete the selected confirmation family.

No candle-body or wick-ratio threshold is invented beyond source-explicit family definitions.

## Family-specific source rules retained

- ICC: minimum source teaching is close back >=30% into trap candle; higher values are stronger but contradictory across sources.
- Engulf: source gives >=20–40% beyond prior extreme; use `ENGULF_MIN_SOURCE` if >=20%, and preserve exact percentage separately.
- 2CR: two consecutive rejection candles at the same zone.
- Sweep close-back: level is exceeded then a completed candle returns inside.
- MSS/BOS: high-confidence version = >=2 closes beyond frozen swing/base.

### Current reproducibility status

Partially mechanized.

Existing corpus quality labels are populated, but they were source-informed rather than independently blinded. Phase 2 is required.

---

# 5. Structural stop / stop sizeability

## 5.1 Strategy-layer structural stop

A trade candidate must have one of:

- sweep extreme;
- outer structural swing;
- outer POI/zone boundary;
- confirmation-candle invalidation;
- active range boundary.

If no source-supported invalidation price exists:

`STRUCTURAL_STOP = UNDEFINED`

Otherwise:

`STRUCTURAL_STOP = DEFINED`

This layer is machine-mechanizable once the corresponding POI/swing primitive is frozen.

## 5.2 Risk-layer sizeability

Do **not** infer `TOO_LARGE` from a universal pip count.

Badar's current live evidence accepts some large stops with reduced size and rejects others.

Therefore sizeability is calculated later from:

- structural stop distance;
- instrument contract value;
- broker minimum lot / size increment;
- Target-First maximum permitted dollar risk for the risk class.

Derived states:

- `DEFINED_ACCEPTABLE`: structural stop can be executed at the intended risk class without violating account/broker constraints.
- `DEFINED_LARGE_BUT_SIZABLE`: requires risk downgrade / smaller position but remains within constraints.
- `TOO_LARGE_FOR_THIS_SETUP`: even the allowed reduced-risk implementation fails the independent risk/sizeability contract.
- `UNDEFINED`: no structural invalidation.

This resolves the previous ambiguity without tuning a Gold-pip cutoff to history.

### Current reproducibility status

Structural-stop existence: strong.

Existing corpus:

- 107/107 TRADE decisions have `logical_stop_present = YES`;
- only 1 non-trade event explicitly has `logical_stop_present = NO`;
- 223 events have `UNCLEAR`, so full prospective chart annotation remains required.

Sizeability cannot be finalized until Target-First broker/instrument sizing inputs are frozen.

---

# 6. Target-path state

Use the source rule: before TP, inspect whether an unmitigated OB/level/imbalance blocks the route to the next opposing liquidity.

At candidate time:

1. identify the nearest source-valid opposing liquidity objective in trade direction;
2. list all pre-existing opposing POIs between entry and that objective;
3. if no blocking POI exists -> `FEASIBLE`;
4. if a blocking POI exists but it is itself a valid first/scalp objective -> `FEASIBLE_WITH_EARLY_OBJECTIVE`, mapped to policy `FEASIBLE`;
5. if a blocking POI exists before any plausible objective and no first objective can be defined -> `INFEASIBLE`;
6. if POI ordering is ambiguous -> `UNRESOLVED`.

No universal RR threshold is introduced here.

### Current reproducibility status

Not previously annotated.

In the existing 347-event corpus:

- `barrier_before_target = UNCLEAR` for 347/347 events.

Therefore target-path feasibility requires a new blinded chart pass before backtesting.

---

# 7. Required HTF-close state

Use branch-specific rules.

## Direct/aggressive pre-planned POI branch

Default:

`HTF_CLOSE = NOT_RELEVANT`

unless:

- the candidate is countertrend against active H1 structure; or
- the active H1/H4 boundary itself is being broken/reclaimed; or
- the plan explicitly depends on confirming a bias flip.

## Confirmation branch at an HTF POI

Source mapping:

- D1 event -> H4/H1 confirmation;
- H1 event -> M30, optionally M15 where the source plan uses it;
- M15 event -> M5 confirmation.

If the mapped confirming candle is open:

`REQUIRED_PENDING`

If it closes against the candidate:

`INVALIDATES`

If it closes in candidate direction without changing the larger bias:

`CONFIRMS`

If it produces a valid structural bias reversal:

`FLIPS_BIAS` and the old candidate must be rebuilt.

## BOS/MSS-specific rule

A high-confidence H1/H4 structural break requires >=2 closes on the analysis timeframe or one lower.

Single-close breaks remain lower-confidence until confirmed.

### Current reproducibility status

Relatively strong for explicit waits.

Existing corpus:

- 44 events have a non-NONE close pending state;
- 42 are WAIT and 2 are NO_TRADE;
- 0 are TRADE.

Selecting **which** HTF close is required still needs Phase-2 chart replay for cases where source commentary is absent.

---

# 8. Environment interpretability

Not one of the five priority classifiers, but retained.

- `NORMAL`: no explicit abnormal condition.
- `CAUTION`: news, low volume, Friday/month-end, chop/manipulation, but readable.
- `UNINTERPRETABLE`: source/chart state cannot support a stable candidate interpretation.

News alone never forces UNINTERPRETABLE.

---

# 9. Machine-ready vs unresolved boundary

## Safe to encode now

- PDH/PDL;
- completed session high/low;
- clean 3-candle FVG;
- premium/discount midpoint once BOS leg is frozen;
- sweep close-back;
- candidate already chasing;
- confirmation candle open vs closed;
- structural stop exists vs absent;
- required close pending when the plan names it;
- barrier ordering once POIs are frozen.

## Still requires prospective visual or separate primitive study

- major vs minor swing selection;
- hidden/subjective OB variants;
- equal-high/low tolerance;
- exact location quality among overlapping POIs;
- exact strong-vs-adequate close in ambiguous cases;
- which HTF close to require when the plan does not explicitly name it;
- any stop-size classification before account/broker sizeability is known.

No unresolved field may be backfilled using later P&L.
