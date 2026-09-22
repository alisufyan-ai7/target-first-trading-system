# Engine G — Contextual Liquidity Reversal v0.1

**Status:** FROZEN — APPROVED 2026-09-23  
**GitHub status:** COMMITTED BEFORE ANY ENGINE-G OUTCOME CALCULATION  
**Outcome status at freeze:** ZERO ENGINE-G OUTCOMES CALCULATED  
**Engine ID:** `engine-g-contextual-liquidity-reversal`  
**Version:** `0.1`  
**Experiment:** `EXP-016 — Engine G Contextual Liquidity Reversal v0.1 Prospective Validation`

---

# 1. Identity and purpose

Engine G is a new prospective causal strategy engine.

It is **not recovered Engine A**, is not a reconstruction of EXP-002, and must not be described as such.

The hypothesis is:

```text
15m context/location
    ->
known meaningful liquidity
    ->
completed 5m liquidity sweep/rejection
    ->
causal internal 1m MSS
    ->
directional displacement
    ->
valid FVG
    ->
retracement entry
    ->
sweep-based structural invalidation
    ->
pre-existing opposing-liquidity target
```

EXP-016 tests whether this prospectively specified mechanism produces a reproducible XAUUSD candidate stream with positive, cost-robust historical expectancy across development, validation, and an untouched same-feed holdout.

---

# 2. Market and primary Phase-2 price path

Initial market:

`XAUUSD`

Primary Phase-2 data:

- Dukascopy-derived XAUUSD BID M1 OHLC;
- UTC timestamps;
- public transport repository `kevingtlin/Market-Data-Lab`;
- immutable external snapshot defined in Section 41.

Phase 2 uses:

```text
unchanged BID OHLC price path
+
explicit round-trip transaction-cost stress
```

It does not alter price paths using ASK data.

Full bid/ask execution modelling is reserved for later independent execution validation.

Frozen source-grid increment:

```text
τ = 0.001 XAU
```

This is a research-source price grid, not a claim about the eventual broker's tradable tick specification.

---

# 3. Exact integer price normalization

All Engine-G structural price logic uses **integer source-grid ticks**.

For any source price represented in the CSV as decimal text `P`:

```text
price_tick = exact_decimal(P) / 0.001
```

Implementation requirement:

1. parse the CSV price as decimal text, not binary floating point;
2. require the price to be exactly representable on the `0.001` grid;
3. convert it to an integer number of thousandths.

Equivalent representation:

```text
price_tick = integer(P * 1000)
```

where multiplication is exact decimal arithmetic.

Examples:

```text
2062.688 XAU -> 2,062,688 ticks
5277.419 XAU -> 5,277,419 ticks
3.000 XAU    -> 3,000 ticks
```

A source price containing non-zero precision beyond three decimal places is invalid for EXP-016 unless it is exactly equivalent to a three-decimal-grid price.

Display conversion only:

```text
normalized_price_XAU = price_tick / 1000
```

### Mandatory rule

All of the following use integer ticks or exact integer/rational arithmetic:

- price equality;
- liquidity clustering;
- level ties;
- high/low comparisons;
- sweep detection;
- target ordering;
- entry prices;
- stop prices;
- distances;
- T-rungs;
- P&L before final display conversion.

Binary floating-point equality must never determine whether two levels belong to the same cluster.

---

# 4. Source-row validity

A source M1 row is valid only if:

1. timestamp exists exactly once;
2. timestamp is an integer Unix-millisecond UTC timestamp;
3. timestamp lies on an exact whole-minute boundary;
4. OHLC values parse exactly to valid integer source-grid ticks;
5. all prices are positive;
6. `high_tick >= open_tick`;
7. `high_tick >= close_tick`;
8. `low_tick <= open_tick`;
9. `low_tick <= close_tick`;
10. `high_tick >= low_tick`.

No interpolation or price imputation is permitted.

If a required interval fails its completeness rule, the dependent liquidity class or derived bar is unavailable.

---

# 5. Carry-forward and market-active M1 bars

## Carry-forward M1 minute

A valid M1 row at timestamp `t` is a **carry-forward minute** when:

```text
open_tick[t]
=
high_tick[t]
=
low_tick[t]
=
close_tick[t]
```

and:

```text
close_tick[t] = close_tick[t - 1 chronological minute]
```

where the immediately preceding chronological source minute exists and is valid.

## Market-active M1 bar

A **market-active M1 bar** is exactly:

```text
a valid M1 bar that is NOT a carry-forward minute
```

Every valid M1 bar therefore has one of two classifications:

```text
market-active M1
carry-forward M1
```

Invalid/missing rows are neither.

## Market-active ordinal

Market-active M1 bars receive a monotonically increasing ordinal:

```text
active_m1_ordinal = 0, 1, 2, ...
```

Carry-forward minutes do not receive an active ordinal and do not increment active-M1 counters.

---

# 6. Exact 1m windows that exclude carry-forward minutes

Every bar-counted one-minute rule below counts **market-active M1 bars only**:

- 1m 2-left/2-right internal pivots;
- prior-15-M1 internal-pivot search universe;
- MSS 10-bar search window;
- displacement MSS+1 / MSS+2 offsets;
- displacement prior-20 body baseline;
- FVG candle ordinals;
- FVG displacement+1 / displacement+2 offsets;
- 10-bar limit-entry window;
- 120-bar trade/label horizon;
- actual MFE/MAE path;
- counterfactual potential MFE/MAE path.

Carry-forward minutes do not increment any of these counters.

UTC wall-clock cutoffs remain independent of the active-bar counters.

For example:

```text
entry expires at the earlier of:
10 market-active M1 bars
or
18:00 UTC
```

---

# 7. “Contiguous market-active M1 candles”

Whenever this specification refers to:

```text
contiguous market-active M1 candles
```

it means consecutive **market-active M1 ordinals**.

If active ordinals are:

```text
n
n+1
n+2
```

they are contiguous for Engine-G structural logic even if one or more carry-forward calendar minutes occurred between their wall-clock timestamps.

Thus an M1 FVG uses three consecutive active ordinals, not necessarily three consecutive wall-clock timestamps.

No invalid or missing source minute may be skipped this way.

Only valid carry-forward minutes are excluded.

---

# 8. Derived 5m and 15m bars

## 5m bar

A UTC-aligned 5m bar requires exactly five valid expected chronological M1 timestamps.

Aggregation:

```text
open_tick  = first M1 open_tick
high_tick  = maximum M1 high_tick
low_tick   = minimum M1 low_tick
close_tick = final M1 close_tick
```

A complete 5m bar is **market-active** if at least one constituent M1 bar is market-active.

An all-carry-forward 5m bar:

- is not used for 5m pivots;
- is not used for ATR;
- does not increment 5m active-bar age;
- cannot create a sweep/setup.

## 15m bar

A UTC-aligned 15m bar requires exactly fifteen valid expected M1 timestamps.

Aggregation is identical.

It is market-active if at least one constituent M1 bar is market-active.

An all-carry-forward 15m bar:

- is not used for 15m pivots;
- does not increment 15m active-bar age;
- is not included in the 48-bar context window.

---

# 9. Setup window versus liquidity monitoring

These are different processes.

## Setup-generation window

New Engine-G sweep setups may be created only from qualifying sweeps completed during:

```text
06:00 <= sweep completion timestamp < 18:00 UTC
```

FVG confirmation and entry must also occur before 18:00.

## Liquidity-consumption monitoring

Active liquidity is monitored on **every market-active completed 5m bar whenever the source market is trading**, regardless of UTC hour.

Liquidity therefore may be consumed:

- before 06:00;
- after 18:00;
- overnight;
- during any other active trading period.

Example:

A valid PDH breached at 02:00 is consumed at that 5m close and cannot appear as fresh liquidity at 09:00.

The same applies to active 15m and 5m swing liquidity.

---

# 10. 15m context

For a possible sweep bar `B`, context is frozen before `B` opens.

Use the latest:

```text
48 market-active completed 15m bars
```

Define in integer ticks:

```text
CTX_HIGH_TICK = maximum high_tick
CTX_LOW_TICK  = minimum low_tick
```

Require:

```text
CTX_HIGH_TICK > CTX_LOW_TICK
```

The midpoint may lie between grid ticks, so retain it exactly as a rational:

```text
2 * CTX_MID = CTX_HIGH_TICK + CTX_LOW_TICK
```

No floating midpoint is required for comparisons.

For anchor tick `L`:

Bearish location test:

```text
2 * L > CTX_HIGH_TICK + CTX_LOW_TICK
```

Bullish location test:

```text
2 * L < CTX_HIGH_TICK + CTX_LOW_TICK
```

Equality is ineligible.

Context percentile may be reported as:

```text
(L - CTX_LOW_TICK)
/
(CTX_HIGH_TICK - CTX_LOW_TICK)
```

for diagnostics only.

The frozen center context is 48 bars.

---

# 11. ATR(14)

For market-active completed 5m bar `k`:

```text
TR_tick[k] =
max(
    high_tick[k] - low_tick[k],
    abs(high_tick[k] - close_tick[k-1]),
    abs(low_tick[k] - close_tick[k-1])
)
```

where `k-1` is the preceding market-active 5m bar.

Define:

```text
ATR14_tick =
sum(TR_tick over latest 14 active 5m bars) / 14
```

The stored ATR may be rational.

No Wilder recursive smoothing is used.

---

# 12. 2-left / 2-right swing definition

All pivot bars are market-active bars.

Swing high centered on active ordinal `t`:

```text
high[t] >  high[t-1]
high[t] >  high[t-2]
high[t] >= high[t+1]
high[t] >= high[t+2]
```

Swing low:

```text
low[t] <  low[t-1]
low[t] <  low[t-2]
low[t] <= low[t+1]
low[t] <= low[t+2]
```

The swing becomes causally known only after active bar `t+2` has closed.

---

# 13. Exact 5m prominence rule

For 5m swing high:

```text
LEFT_TROUGH_TICK =
min(low[t-2], low[t-1])

RIGHT_TROUGH_TICK =
min(low[t+1], low[t+2])

PROM_HIGH_TICK =
high[t] - max(LEFT_TROUGH_TICK, RIGHT_TROUGH_TICK)
```

For 5m swing low:

```text
LEFT_PEAK_TICK =
max(high[t-2], high[t-1])

RIGHT_PEAK_TICK =
max(high[t+1], high[t+2])

PROM_LOW_TICK =
min(LEFT_PEAK_TICK, RIGHT_PEAK_TICK) - low[t]
```

At confirmation use the latest ATR14 through bar `t+2`.

Instead of floating-point arithmetic:

```text
prominence >= 0.50 * ATR14
```

is implemented exactly as:

```text
28 * PROM_TICK >= SUM_OF_14_TR_TICKS
```

because:

```text
ATR14 = SUM_TR / 14
0.50 * ATR14 = SUM_TR / 28
```

The 15m swing class has no prominence threshold in v0.1.

---

# 14. Individual liquidity instances

Every liquidity level exists as an independent instance.

Each instance stores:

- unique instance ID;
- side;
- class;
- `price_tick`;
- display XAU price;
- source center/session/day;
- creation timestamp;
- first eligible timestamp;
- expiry rule;
- consumed state;
- consumed timestamp if applicable.

Classes:

```text
PDH
PDL
ASIA_HIGH
ASIA_LOW
SWING_15M_HIGH
SWING_15M_LOW
SWING_5M_HIGH
SWING_5M_LOW
```

High classes are buy-side liquidity.

Low classes are sell-side liquidity.

Instances retain their own lifecycle regardless of coincident prices.

---

# 15. Dynamic liquidity clusters

A cluster is a dynamic view, not a durable independent level.

Exact cluster key:

```text
(side, price_tick)
```

Cluster membership at time `T` consists of all individual instances sharing that key that are simultaneously:

- created;
- eligible;
- unexpired;
- unconsumed.

If one constituent expires, only that constituent disappears.

The cluster remains active while at least one constituent remains active.

If every constituent is consumed or expired:

```text
cluster inactive
```

A strict breach of the cluster price consumes **every active constituent instance in that cluster**.

A later newly confirmed swing at the same `price_tick` may create a new active cluster after all prior constituents have disappeared.

The cluster's class labels are the union of its currently active constituent classes.

HIGH and LOW instances at the same numerical price are separate clusters because side is part of the key.

---

# 16. PDH / PDL lifecycle

For setup date `D`, locate the preceding trading day.

Starting from the immediately preceding UTC date:

1. skip Saturdays and Sundays;
2. a source-complete weekday with zero active 5m bars and zero range is treated as a non-trading holiday and skipped;
3. if the first relevant preceding weekday is incomplete, PDH/PDL are unavailable for `D`;
4. do not jump over an incomplete relevant weekday to use an older trading date.

## Exact day completeness

A usable previous trading day requires:

- all 1,440 expected M1 timestamps;
- no duplicates;
- exact one-minute chronology;
- every row valid;
- at least one market-active 5m bar;
- `daily_high_tick > daily_low_tick`.

Then:

```text
PDH_tick = max M1 high_tick
PDL_tick = min M1 low_tick
```

## Creation

Valid PDH/PDL instances activate at:

```text
00:00 UTC on D
```

## Expiry

They expire at:

```text
00:00 UTC on D+1
```

unless consumed first.

A target already frozen into an entered trade remains unchanged.

## Consumption

On every market-active completed 5m bar:

```text
HIGH cluster consumed if high_tick > cluster_price_tick
LOW cluster consumed if low_tick  < cluster_price_tick
```

Equality does not consume.

---

# 17. Asian H/L lifecycle

Asian interval:

```text
00:00 through 05:59 UTC
```

## Completeness

Require:

- exactly 360 expected M1 timestamps;
- no duplicates;
- exact chronological spacing;
- all rows valid;
- at least one market-active 5m bar;
- `ASIA_HIGH_tick > ASIA_LOW_tick`.

Then:

```text
ASIA_HIGH_tick = maximum M1 high_tick
ASIA_LOW_tick  = minimum M1 low_tick
```

If incomplete, neither level is created.

## Creation

At:

```text
06:00 UTC
```

## Expiry

At:

```text
00:00 UTC next calendar date
```

unless consumed first.

## Consumption

The same always-on completed-5m strict-breach rule applies.

---

# 18. 15m swing lifecycle

A 15m swing becomes known after its second right-side active 15m bar closes.

The instance is created then.

Its first breach/sweep eligibility is:

```text
first subsequent market-active 5m bar
```

If the center has active 15m ordinal `i`:

```text
age15 = current active 15m ordinal - i
```

It remains active while:

```text
age15 <= 48
```

It expires before processing a bar for which:

```text
age15 > 48
```

or when consumed.

---

# 19. 5m swing lifecycle

A 5m instance requires:

- valid 2L2R swing;
- frozen prominence test.

It is created after the second right-side market-active 5m bar closes.

Its first breach eligibility is the next market-active 5m bar.

If center ordinal is `i`:

```text
age5 =
current active 5m ordinal - i
```

Active while:

```text
age5 <= 48
```

Expired before:

```text
age5 > 48
```

or when consumed.

Consumed instances never reactivate.

---

# 20. Exact 5m event-processing order

## At each 5m bar open

Before using liquidity:

1. apply calendar expiries effective at the timestamp;
2. activate valid PDH/PDL if applicable;
3. activate valid Asian H/L at 06:00;
4. expire swing instances already beyond their age limit;
5. construct active side/price-tick clusters.

No information from the still-open bar may enter this state.

## At each completed 5m bar close

If incomplete or invalid:

```text
no structure
no consumption
no setup
```

If complete but entirely carry-forward:

```text
no structure
no consumption
no setup
```

For a market-active completed 5m bar:

### Step 1
Snapshot all clusters that existed before the bar's price path.

### Step 2
Evaluate strict price breaches of those pre-existing clusters and consume all active constituent instances at every breached `(side, price_tick)`.

This runs at all UTC hours.

### Step 3
Using the same pre-breach snapshot, determine whether a breach also satisfies sweep/rejection rules.

### Step 4
Evaluate setup eligibility:

- time window;
- dual-sided ambiguity;
- 48-bar context;
- context-half rule;
- one-open suppression.

### Step 5
After all breach/setup decisions for this bar, activate newly confirmed 5m and 15m swing instances.

Those new instances cannot be breached by the bar that confirmed them.

### Step 6
Persist the new state.

---

# 21. Qualifying 5m sweep

## Bearish sweep

For pre-existing HIGH cluster `L`:

```text
high_tick > L
AND
close_tick < L
```

## Bullish sweep

For pre-existing LOW cluster `L`:

```text
low_tick < L
AND
close_tick > L
```

No minimum sweep-depth parameter.

## Multiple same-side levels

Bearish anchor:

```text
maximum qualifying HIGH price_tick
```

Bullish anchor:

```text
minimum qualifying LOW price_tick
```

All breached clusters are consumed.

## Dual-sided sweep

If the same bar qualifies in both directions:

```text
no setup
terminal reason = dual_sided_sweep_ambiguous
```

All valid breaches remain consumed.

---

# 22. Context eligibility

Context is frozen before the sweep bar opens.

Bearish:

```text
2 * anchor_tick >
CTX_HIGH_TICK + CTX_LOW_TICK
```

Bullish:

```text
2 * anchor_tick <
CTX_HIGH_TICK + CTX_LOW_TICK
```

Failure reasons:

```text
context_unavailable_48
context_zero_range
anchor_wrong_context_half
```

---

# 23. Internal M1 pivot

At sweep completion, freeze the most recent already-confirmed opposite-side M1 2L2R pivot from the:

```text
previous 15 market-active M1 ordinals
```

The pivot center must occur before the 5m sweep bar opened.

Its right-side confirmation may complete by the sweep close.

Bearish:

```text
most recent internal swing low
```

Bullish:

```text
most recent internal swing high
```

If absent:

```text
no_internal_mss_pivot
```

---

# 24. MSS

Search begins with the first market-active M1 bar after sweep completion.

Maximum:

```text
10 market-active M1 bars
```

Bearish:

```text
close_tick < frozen_internal_swing_low_tick
```

Bullish:

```text
close_tick > frozen_internal_swing_high_tick
```

Use the first qualifying bar.

Failures:

```text
mss_timeout_10
setup_window_closed_before_mss
```

---

# 25. Displacement

Candidate bars:

```text
MSS active ordinal
MSS+1 active ordinal
MSS+2 active ordinal
```

For bar `j`:

```text
BODY_TICK[j] =
abs(close_tick[j] - open_tick[j])
```

Baseline:

```text
SUM_BODY20 =
sum of BODY_TICK over previous
20 market-active completed M1 bars
```

The frozen test:

```text
BODY >= 1.60 * mean(previous 20 bodies)
```

is implemented exactly without floating point as:

```text
25 * BODY_TICK[j] >= 2 * SUM_BODY20
```

because:

```text
1.60 / 20 = 2 / 25
```

Bearish additionally requires:

```text
close_tick < open_tick
close_tick < frozen_internal_swing_low_tick
```

Bullish:

```text
close_tick > open_tick
close_tick > frozen_internal_swing_high_tick
```

Use first qualifying candidate.

Failures:

```text
displacement_baseline_unavailable_20
displacement_timeout_mss_plus_2
setup_window_closed_before_displacement
```

---

# 26. FVG

Use three consecutive **market-active M1 ordinals**:

```text
j-2
j-1
j
```

## Bullish

```text
low_tick[j] > high_tick[j-2]
```

Zone:

```text
lower_FVG_tick = high_tick[j-2]
upper_FVG_tick = low_tick[j]
```

## Bearish

```text
high_tick[j] < low_tick[j-2]
```

Zone:

```text
lower_FVG_tick = high_tick[j]
upper_FVG_tick = low_tick[j-2]
```

Require:

```text
upper_FVG_tick > lower_FVG_tick
```

The FVG's third candle may be active ordinal:

```text
displacement
displacement+1
displacement+2
```

Use first qualifying same-direction FVG.

Failures:

```text
fvg_timeout_displacement_plus_2
setup_window_closed_before_fvg
```

---

# 27. Entry

The exact mathematical midpoint is:

```text
MID_NUMERATOR =
lower_FVG_tick + upper_FVG_tick
```

over denominator `2`.

No floating point is needed.

Long entry:

```text
entry_tick =
ceil(MID_NUMERATOR / 2)
```

Short entry:

```text
entry_tick =
floor(MID_NUMERATOR / 2)
```

If the sum is even, both equal the exact midpoint tick.

The limit starts after FVG confirmation.

Maximum wait:

```text
10 market-active M1 bars
```

Long fill:

```text
low_tick <= entry_tick
```

Short fill:

```text
high_tick >= entry_tick
```

Entry must occur before 18:00 UTC.

Failures:

```text
entry_timeout_10
entry_window_closed_1800
```

No market substitution.

---

# 28. Structural stop

Bearish:

```text
stop_tick =
sweep_high_tick + 1
```

Bullish:

```text
stop_tick =
sweep_low_tick - 1
```

Require:

Long:

```text
stop_tick < entry_tick
```

Short:

```text
stop_tick > entry_tick
```

Otherwise:

```text
invalid_stop_geometry
```

Stop distance:

```text
STOP_DISTANCE_TICKS =
abs(entry_tick - stop_tick)
```

Display distance:

```text
STOP_DISTANCE_XAU =
STOP_DISTANCE_TICKS / 1000
```

At the project's XAU 0.10-lot / 10-oz research convention:

```text
gross_stop_USD =
STOP_DISTANCE_TICKS * $0.01
```

because one `0.001` tick over 10 oz is `$0.01`.

---

# 29. Gross structural-risk admission gate

Engine-G economic admission requires:

```text
gross_stop_USD <= $40
```

Equivalent tick rule:

```text
STOP_DISTANCE_TICKS <= 4000
```

This is explicitly a **gross structural-risk gate before transaction-cost stress**.

It is **not** cost-inclusive.

Therefore, under the primary `0.50 XAU` round-trip stress:

```text
primary_cost_USD = $5
```

a trade admitted at exactly the maximum gross stop:

```text
gross stop = -$40
```

would produce approximately:

```text
net stopped-trade P&L = -$45
```

after the frozen transaction-cost deduction.

This is intentional and prospective.

The `$40` Engine-G gate means:

> the unchanged structural stop itself may not represent more than approximately $40 gross risk at 0.10 lot.

It does **not** mean:

> every fully cost-adjusted trade loss must be capped at $40.

It is also distinct from the downstream system daily-risk state machine.

The project's approximately `$40` normal / approximately `$60` emergency daily-loss framework remains a later aggregate execution-control layer.

Multiple simultaneously or sequentially admitted trades cannot simply consume that downstream budget without the later daily-state/risk gates.

If:

```text
gross_stop_USD > $40
```

reason:

```text
structural_risk_above_40
```

No stop compression is permitted.

---

# 30. S1 / S2 / S3 structural targets

Targets are frozen at FVG confirmation.

Only already-known, eligible, unexpired, unconsumed opposing liquidity may be used.

All target ordering uses integer `price_tick`.

## Eligible target classes

Long:

```text
PDH
ASIA_HIGH
SWING_15M_HIGH
SWING_5M_HIGH
```

Short:

```text
PDL
ASIA_LOW
SWING_15M_LOW
SWING_5M_LOW
```

## Causal freshness

A target cluster must not already have been strictly passed by any completed market-active M1 bar between the latest completed 5m liquidity-processing event and FVG confirmation.

## S1

Long:

```text
S1_tick =
minimum eligible HIGH cluster tick
strictly greater than entry_tick
```

Short:

```text
S1_tick =
maximum eligible LOW cluster tick
strictly less than entry_tick
```

Distance:

```text
D1_TICKS =
abs(S1_tick - entry_tick)
```

Require:

```text
D1_TICKS >= 3000
```

equivalent to:

```text
D1 >= 3.000 XAU
```

If no opposing target exists:

```text
no_opposing_liquidity_target
```

If nearest target exists but is under 3,000 ticks away:

```text
insufficient_structural_room
```

The nearest obstacle cannot be skipped.

## S2

Next farther distinct target `price_tick`.

If absent:

```text
S2 = null
```

## S3

Next farther distinct target `price_tick`.

If absent:

```text
S3 = null
```

Multiple classes sharing the same `(side, price_tick)` form one target rung.

---

# 31. Pre-entry thesis invalidation

After target freeze but before fill:

If structural stop is reached first:

```text
preentry_structural_invalidation
```

If S1 is reached first:

```text
preentry_s1_reached
```

If entry and S1 occur within the same fill bar:

- fill allowed;
- S1 receives no fill-bar credit.

If entry and stop occur within the same fill bar:

```text
entry occurs
stop wins
```

This becomes an actual filled losing trade.

---

# 32. Actual v0.1 exit

The actual Engine-G trade exits:

```text
100% at S1
```

No:

- partial;
- S2 exit;
- S3 exit;
- runner;
- dynamic target extension

is allowed.

Actual trade terminates at the earliest of:

1. S1;
2. structural stop;
3. 120 active-M1 horizon;
4. 20:00 UTC;
5. data-end fail-safe.

---

# 33. Counterfactual T30/T40/T50/T70/T100 labels

These are not actual trade exits.

Distances in integer ticks:

```text
T30  = 3000 ticks
T40  = 4000 ticks
T50  = 5000 ticks
T70  = 7000 ticks
T100 = 10000 ticks
```

Long target:

```text
entry_tick + rung_ticks
```

Short target:

```text
entry_tick - rung_ticks
```

Each label is evaluated independently using:

- original entry;
- unchanged structural stop;
- same 120-active-M1 horizon;
- same 20:00 cutoff;
- same conservative ambiguity rule.

**The actual S1 exit is ignored when constructing these labels.**

Thus a real trade may exit at S1 while T50 or T100 continues counterfactually along the recorded path.

Each rung receives one state:

```text
target_before_stop
stop_before_target
horizon_without_target_or_stop
```

A lower rung succeeding does not terminate a higher rung.

Actual Engine-G P&L never uses these counterfactual exits.

---

# 34. Actual and counterfactual excursion metrics

## Actual-trade MFE / MAE

Measured from entry through actual:

```text
S1
stop
or timeout
```

## Counterfactual potential MFE / MAE

Measured from entry through:

```text
structural stop
or
full target-label horizon
```

Actual S1 does not terminate this second excursion path.

## Fill bar

If stop is touched on the fill bar:

```text
stop wins
MFE = 0
```

Otherwise fill-bar high/low excursion is excluded because pre-fill versus post-fill path is unknown.

Excursion measurement begins on the next market-active M1 bar.

## Ambiguous later stop bar

If stop and favorable excursion both occur on the same later M1 bar:

- stop ordering wins;
- favorable movement on that ambiguous bar is not credited beyond the previously established MFE;
- MAE terminates at stop distance.

---

# 35. Trade horizon

The fill bar counts as active horizon bar 1.

Maximum:

```text
120 market-active M1 bars
```

subject also to:

```text
20:00 UTC on entry date
```

No overnight carry.

Timeout exit is the final eligible market-active M1 close.

Exit reasons:

```text
exit_timeout_120
exit_session_2000
exit_data_end
```

Counterfactual labels use the same temporal horizon independently of actual S1.

---

# 36. Same-bar ordering

## Fill bar

```text
entry + stop -> stop
entry + S1   -> no S1 credit on fill bar
entry + T-rung -> no T-rung credit on fill bar
```

## Later active M1 bars

```text
stop + S1 -> stop
stop + counterfactual target -> stop for that label
```

No A9-style optimism.

---

# 37. One-open-trade rule

Maximum:

```text
one economically accepted Engine-G XAUUSD trade open
```

A later qualifying setup while an accepted trade is open receives:

```text
suppressed_one_open
```

It is not queued.

Its breached liquidity is nevertheless consumed.

Rejected or expired candidates that never enter do not occupy the position slot.

---

# 38. Transaction-cost stress

First calculate actual S1-strategy gross P&L in integer ticks.

Long:

```text
gross_pnl_ticks =
actual_exit_tick - entry_tick
```

Short:

```text
gross_pnl_ticks =
entry_tick - actual_exit_tick
```

Cost stresses:

```text
0.00 XAU =   0 ticks
0.25 XAU = 250 ticks
0.50 XAU = 500 ticks
```

Net:

```text
net_pnl_ticks(c) =
gross_pnl_ticks - cost_ticks(c)
```

At 10 oz:

```text
net_USD =
net_pnl_ticks * $0.01
```

Therefore:

```text
0.00 stress -> $0.00 deduction/trade
0.25 stress -> $2.50 deduction/trade
0.50 stress -> $5.00 deduction/trade
```

Cost is applied once per actual filled trade.

It applies to:

- S1 winners;
- stop losses;
- timeouts.

Unfilled/rejected setups incur no cost.

Primary promotion economics use:

```text
0.50 XAU / 500-tick / $5 round-trip stress
```

Counterfactual target labels remain non-P&L labels.

---

# 39. Deterministic reason codes

Every candidate receives the first applicable terminal code in causal stage order.

## Data/liquidity availability

```text
source_bar_incomplete_or_invalid
pdh_pdl_unavailable_incomplete_previous_day
pdh_pdl_unavailable_no_previous_trading_day
asian_unavailable_incomplete_interval
asian_unavailable_inactive_or_zero_range
```

## Breach/sweep stage

```text
outside_setup_window
breach_without_rejection_close
dual_sided_sweep_ambiguous
context_unavailable_48
context_zero_range
anchor_wrong_context_half
suppressed_one_open
```

## Construction stage

```text
no_internal_mss_pivot
mss_timeout_10
setup_window_closed_before_mss
displacement_baseline_unavailable_20
displacement_timeout_mss_plus_2
setup_window_closed_before_displacement
fvg_timeout_displacement_plus_2
setup_window_closed_before_fvg
no_opposing_liquidity_target
insufficient_structural_room
invalid_stop_geometry
structural_risk_above_40
```

## Pre-entry cancellation

```text
preentry_structural_invalidation
preentry_s1_reached
entry_timeout_10
entry_window_closed_1800
```

## Filled-trade exit

```text
exit_s1
exit_stop
exit_stop_fill_bar
exit_timeout_120
exit_session_2000
exit_data_end
```

No candidate gets more than one terminal reason code.

---

# 40. Candidate ledger

Required fields include:

- engine ID/version;
- immutable source snapshot ID;
- symbol;
- direction;
- active-M1 ordinal;
- sweep timestamp;
- sweep 5m OHLC ticks;
- breached instance IDs;
- consumed instance IDs;
- anchor `price_tick`;
- anchor constituent classes;
- constituent creation timestamps;
- context high/low ticks;
- exact context-mid numerator;
- context percentile;
- ATR numerator/denominator;
- swing prominence ticks;
- internal MSS pivot tick;
- MSS timestamp;
- displacement timestamp;
- body ticks;
- prior-20 body sum;
- displacement ratio;
- FVG tick bounds;
- FVG timestamp;
- midpoint numerator;
- entry tick;
- fill timestamp;
- sweep extreme tick;
- stop tick;
- stop-distance ticks;
- gross structural stop USD;
- S1/S2/S3 ticks;
- target class sets;
- target distances;
- actual exit tick/time/reason;
- gross P&L ticks/USD;
- net P&L at all stresses;
- actual MFE/MAE;
- potential counterfactual MFE/MAE;
- T30/T40/T50/T70/T100 labels;
- target times;
- terminal reason;
- one-open suppression;
- source provenance identifiers.

All rejected, cancelled, and suppressed events remain in the ledger.

---

# 41. Immutable external data snapshot

Primary external repository:

```text
kevingtlin/Market-Data-Lab
```

Frozen repository commit:

```text
922f83a60cc574e7395fb27397077288055a1ef6
```

Frozen root tree:

```text
6596cd229c736f96bab7d1496656397b31326ca6
```

Frozen XAUUSD BID M1 subtree:

```text
86dd3acd141ffe4b5eb8ad86a04ca42398d0b558
```

Frozen XAUUSD ASK M1 subtree:

```text
bf346b8c4c79bd6a0eee33e3b1114d4d855e646f
```

Dataset README blob:

```text
0ff0a9a2649f664c233b31acb2f1427db2cc03af
```

BID audit CSV blob:

```text
2463651d7bdfc4bc9778b6a63a52e5ddc3ac65f3
```

ASK audit CSV blob:

```text
ce55b4788660794b2db102f78abb7d06273d3baa
```

The source README identifies:

- XAUUSD spot gold;
- Dukascopy historical data;
- downloaded through `dukascopy-node`;
- M1;
- UTC;
- separate BID/ASK OHLC.

The same immutable snapshot contains March 2026 BID blob:

```text
68e025d16d184b12a78505a30efc05564f6b5d2b
```

matching the March file recorded in EXP-014.

---

# 42. Frozen BID file manifest

`2023_12` is warm-up only.

| Role | BID monthly file | Git blob SHA | Bytes | Audit |
|---|---|---|---:|---|
| Warm-up | `xauusd_bid_m1_2023_12.csv` | `56dbf8a5316c48f4ec3300126c0decda03f8325f` | 2,231,969 | ok |
| Development | `xauusd_bid_m1_2024_01.csv` | `f439cc6e17e39addc1a464eb0ccf8fe2eb71de99` | 2,231,993 | ok |
| Development | `xauusd_bid_m1_2024_02.csv` | `b3ad49d5e784fb8c879f8e12095640f454f8f5fb` | 2,087,847 | ok |
| Development | `xauusd_bid_m1_2024_03.csv` | `cdd53e37cc41773cc0d5c9210daefbf5ef6c3535` | 2,231,983 | ok |
| Development | `xauusd_bid_m1_2024_04.csv` | `f2e7801f91829e9aeeebbd88f9177350cc6ba043` | 2,159,936 | ok |
| Development | `xauusd_bid_m1_2024_05.csv` | `b49cd640075396bf656578c52e7dac0d9e472a22` | 2,232,006 | ok |
| Development | `xauusd_bid_m1_2024_06.csv` | `6c4dc31818a7e04d90f165df0930489cdf5e7121` | 2,159,852 | ok |
| Development | `xauusd_bid_m1_2024_07.csv` | `1a9877d863a7cadcfb47388a2d7b6657b57873ed` | 2,231,718 | ok |
| Development | `xauusd_bid_m1_2024_08.csv` | `29c3275f68b15d33325a7a989e322565fca4a64e` | 2,231,775 | ok |
| Development | `xauusd_bid_m1_2024_09.csv` | `075fc0b3c4f01bfebdbdb21af82c66595c2fd6cc` | 2,159,940 | ok |
| Development | `xauusd_bid_m1_2024_10.csv` | `ab734d9cea86c2441b2592e6aa0537829bd093f5` | 2,231,815 | ok |
| Development | `xauusd_bid_m1_2024_11.csv` | `4fe07a39a96512d4264202d4817fafedb3b97e79` | 2,159,626 | ok |
| Development | `xauusd_bid_m1_2024_12.csv` | `a5a219ccee1e3808593f349a56274d6242fe31dd` | 2,231,444 | ok |
| Development | `xauusd_bid_m1_2025_01.csv` | `f0211e901b6f8b26996ba1a48aeba73f599bd5fe` | 2,231,746 | ok |
| Development | `xauusd_bid_m1_2025_02.csv` | `e3beb3def6e2502975046d07f43db777604110b2` | 2,015,844 | ok |
| Validation | `xauusd_bid_m1_2025_03.csv` | `fefe437f1f5b7565ca3cf10c10c60a63edf527ef` | 2,231,490 | ok |
| Validation | `xauusd_bid_m1_2025_04.csv` | `aff4975ce8522f28951940db2daff3f36d5b3155` | 2,159,648 | ok |
| Validation | `xauusd_bid_m1_2025_05.csv` | `6470db6ad153edb9bffd41660d0ae9b4370e4662` | 2,231,564 | ok |
| Validation | `xauusd_bid_m1_2025_06.csv` | `b21e4764f19340da04b524f228264ff907d818f0` | 2,159,802 | ok |
| Validation | `xauusd_bid_m1_2025_07.csv` | `f832021fb3a42d7299830d5420c241d75977293d` | 2,231,995 | ok |
| Validation | `xauusd_bid_m1_2025_08.csv` | `57eb33cd0e3216612f20bdd24ffcb380a8950fb6` | 2,231,992 | ok |
| Holdout | `xauusd_bid_m1_2025_09.csv` | `d9d02b8459d59e624fb10eaf5ee8eed3c8e71a32` | 2,159,764 | ok |
| Holdout | `xauusd_bid_m1_2025_10.csv` | `2abab9482acf9a1612d2270a8c154ef29d7cfa76` | 2,231,779 | ok |
| Holdout | `xauusd_bid_m1_2025_11.csv` | `d352855e8e795e8b63bd0061fe49bf36976bbe14` | 2,159,800 | ok |
| Holdout | `xauusd_bid_m1_2025_12.csv` | `48b6a35faefba150cc05b7bf9ae849e90af2b3d5` | 2,231,857 | ok |
| Holdout | `xauusd_bid_m1_2026_01.csv` | `e94768e8723896c4564085d308bff773384b0b0d` | 2,231,894 | ok |
| Holdout | `xauusd_bid_m1_2026_02.csv` | `7a4190c519c665e9b0381a72e1ce2763a7759c11` | 2,015,873 | ok |

Before any outcome computation:

```text
repository commit matches
AND
file path matches
AND
Git blob SHA matches
AND
byte size matches
AND
expected row count matches
```

Otherwise EXP-016 stops.

---

# 43. Monthly and interval completeness

For complete monthly files:

```text
expected_lines =
days_in_month * 1440 + 1 CSV header
```

Thus:

```text
31 days -> 44,641
30 days -> 43,201
29 days -> 41,761
28 days -> 40,321
```

Timestamp coverage must run exactly:

```text
month-start 00:00 UTC
through
month-end 23:59 UTC
```

in one-minute chronological increments.

No primary split may run on a partial month.

PDH/PDL and Asian classes additionally apply their own interval-level completeness tests.

---

# 44. Primary data split

## Development

```text
2024-01-01 00:00 UTC
through
2025-02-28 23:59 UTC
```

14 months.

December 2023 is warm-up only.

## Validation

```text
2025-03-01 00:00 UTC
through
2025-08-31 23:59 UTC
```

6 months.

## Fresh holdout

```text
2025-09-01 00:00 UTC
through
2026-02-28 23:59 UTC
```

6 months.

All three evaluation segments come from one contiguous immutable provider snapshot.

---

# 45. Contamination/provenance audit

| EXP-016 period | Role | Earlier Target-First strategy-development/result use? |
|---|---|---|
| Jan 2024–Feb 2025 | Development | No recorded earlier strategy-result use |
| Mar 2025–Aug 2025 | Validation | No recorded earlier strategy-development/result use |
| Sep 2025–Feb 2026 | Fresh holdout | No recorded earlier strategy-development/result use |
| Mar 2026–Aug 20 2026 | Quarantined diagnostic | Yes — extensively inspected by earlier project research |

Earlier project strategy-result windows begin in March 2026:

- EXP-002: March 1–August 20, 2026;
- EXP-004/005: March–August 20, 2026;
- EXP-006 through EXP-010: March 12–August 20, 2026;
- EXP-012/013: 2026 windows;
- EXP-014: March–August 20, 2026;
- pre-pause EXP-015 diagnostics: March–May 2026.

The EXP-016 validation and fresh-holdout intervals are therefore outside all previously recorded project strategy-result windows.

---

# 46. Quarantined 2026 period

```text
2026-03-01 through 2026-08-20
```

is excluded from primary Engine-G development, validation, and holdout.

It may be evaluated only after:

```text
center-rule development
+
center-rule validation
+
center-rule holdout
+
primary conclusion
```

have all been durably checkpointed.

Its role is historical/regime diagnosis only.

---

# 47. Independent-feed validation

Any later:

- MT5/broker;
- GetData;
- OANDA;
- Twelve Data;
- other feed

test is a separate independent-feed validation.

A second provider cannot be appended to the Dukascopy primary sequence.

No feed shopping.

---

# 48. Primary execution sequence

After approval and GitHub freeze:

```text
1. immutable manifest verification
2. implementation/unit/causality tests
3. development run
4. GitHub development checkpoint
5. validation run
6. GitHub validation checkpoint
7. fresh holdout run
8. GitHub holdout checkpoint
9. primary v0.1 conclusion
10. only then sensitivity diagnostics
11. sensitivity checkpoint
12. only then optional quarantined-2026 diagnostic
13. later independent-feed validation
```

Validation is not inspected before the development checkpoint.

Holdout is not inspected before the validation checkpoint.

---

# 49. Required metrics

Report separately for development, validation, and fresh holdout:

- data-quality checks;
- setup funnel;
- qualifying sweep count;
- candidate count;
- accepted filled trades;
- rejection/cancellation counts by deterministic reason;
- trades per eligible weekday including zero-trade days;
- S1 hit rate;
- stop rate;
- timeout rate;
- independent T30 hit rate;
- independent T40 hit rate;
- independent T50 hit rate;
- independent T70 hit rate;
- independent T100 hit rate;
- gross actual-strategy expectancy/trade;
- net expectancy/trade at 0.00 cost;
- net expectancy/trade at 0.25 cost;
- net expectancy/trade at 0.50 cost;
- profit factor at all cost levels;
- total net P&L;
- mean daily P&L;
- median daily P&L;
- losing-weekday percentage;
- percentage of weekdays with P&L `<= $50`;
- percentage of weekdays with P&L `>= $100`;
- percentage of weekdays with P&L `>= $150`;
- percentage of weekdays with P&L `>= $200`;
- maximum drawdown;
- maximum consecutive losing trades;
- cumulative loss of worst losing-trade streak;
- maximum consecutive losing weekdays;
- maximum consecutive `<= $50` weekdays;
- actual MFE distribution;
- actual MAE distribution;
- counterfactual potential MFE distribution;
- counterfactual potential MAE distribution;
- S1 distance distribution;
- structural-stop distance distribution;
- gross structural stop-risk distribution;
- time-to-S1 distribution;
- time-to-counterfactual-target distributions;
- long/short contribution;
- anchor-liquidity-class contribution;
- S1 target-class contribution;
- cost sensitivity;
- bootstrap uncertainty.

---

# 50. Daily metrics

Eligible evaluation weekdays include zero-trade weekdays.

Daily P&L is the sum of actual S1-strategy trade P&L.

Counterfactual T-labels do not contribute.

EXP-016 does not impose the downstream:

```text
+$150–$200 daily success state
```

or:

```text
~$40 / ~$60 aggregate daily loss state
```

Those belong to later portfolio/execution control.

---

# 51. Bootstrap uncertainty

Use deterministic moving-block bootstrap over eligible evaluation weekdays.

Frozen parameters:

```text
block length = 5 eligible weekdays
replications = 10,000
random seed = 16016
interval = percentile 95%
```

Procedure:

1. preserve each day's original accepted trades;
2. include zero-trade weekdays;
3. construct every possible contiguous 5-eligible-weekday block;
4. resample blocks with replacement;
5. concatenate to at least original weekday count;
6. truncate to original length;
7. recompute statistics.

Primary bootstrap statistics:

```text
mean net USD expectancy per accepted trade
at 0.50-XAU cost

mean net USD per eligible weekday
at 0.50-XAU cost
```

Report:

- point estimate;
- 2.5th percentile;
- 97.5th percentile.

Zero-trade resamples are excluded only from per-trade expectancy and separately counted.

---

# 52. Maximum drawdown

Use actual chronological S1-strategy net P&L at the primary:

```text
0.50 XAU cost stress
```

Reference equity:

```text
$500
```

Report:

```text
maximum_drawdown_USD
maximum_drawdown_percent_of_500
```

No newly invented numeric MDD veto is imposed in EXP-016.

---

# 53. Consecutive-loss evidence

A losing trade means:

```text
net_USD(0.50) < 0
```

Report:

- maximum consecutive losing trades;
- cumulative net loss during worst losing-trade run;
- maximum consecutive losing weekdays;
- maximum consecutive low-output weekdays.

These are mandatory promotion evidence.

No arbitrary new hard streak threshold is introduced at this engine-validation stage.

If statistical edge validates but observed drawdown/streak behavior is not compatible with the project's later risk framework, classification may be:

```text
EDGE_VALIDATED / RISK_NOT_CLEARED
```

rather than changing rules after seeing outcomes.

---

# 54. Minimum evidence

Required accepted trades:

```text
development >= 100
validation  >= 50
holdout     >= 50
```

Otherwise:

```text
INSUFFICIENT_EVIDENCE
```

not automatic pass or rejection.

---

# 55. Historical-edge promotion criteria

To become a validated historical engine candidate source, all must hold using actual S1-strategy P&L under the frozen `0.50 XAU` stress:

1. development expectancy/trade > 0;
2. validation expectancy/trade > 0;
3. fresh-holdout expectancy/trade > 0;
4. validation profit factor >= 1.10;
5. fresh-holdout profit factor >= 1.10;
6. validation 95% block-bootstrap expectancy lower bound > 0;
7. holdout 95% block-bootstrap expectancy lower bound > 0;
8. no development/validation/holdout expectancy sign reversal;
9. minimum evidence counts satisfied;
10. no causal leakage;
11. no optimistic same-bar treatment;
12. no provenance/manifest violation.

MDD and losing-streak evidence must accompany the decision but have no newly invented EXP-016 numeric cutoff.

Passing does not authorize live trading.

---

# 56. Failure discipline

If validation or holdout expectancy is non-positive under the frozen center specification:

```text
Engine G v0.1 is not promoted
```

Do not change afterward:

- 48-bar context;
- 0.50 prominence threshold;
- liquidity lifecycle;
- setup session;
- MSS window;
- 1.60 displacement;
- FVG logic;
- midpoint entry;
- sweep stop;
- gross `$40` structural-risk gate;
- 3.000-XAU room;
- S1 target logic;
- 120-active-M1 horizon;
- cost stress;
- split.

Material change requires Engine G v0.2 or a new experiment.

---

# 57. Delayed sensitivity diagnostics

Primary center:

```text
context = 48 active 15m bars
displacement = 1.60x
```

Predeclared diagnostics:

```text
context32 / displacement1.60
context64 / displacement1.60
context48 / displacement1.40
context48 / displacement1.80
```

No cross-product search.

No sensitivity outcome may be calculated or inspected until the entire:

```text
48/1.60 development
48/1.60 validation
48/1.60 holdout
```

sequence and primary conclusion have been checkpointed.

Sensitivity assesses parameter-cliff risk only.

It may never select a replacement rule based on superior observed performance.

---

# 58. Anti-leakage / anti-overfitting rules

Prohibited:

- binary-floating equality for price identity;
- future-looking pivots;
- unfinished 5m sweep information;
- A8-style eventual-close leakage;
- A9-style fill-bar optimism;
- retroactive use of newly confirmed swing levels;
- incomplete PDH/PDL construction;
- incomplete Asian-range construction;
- counting carry-forward M1 bars inside active-M1 structural windows;
- silently skipping invalid/missing minutes as though they were carry-forward;
- post-FVG target discovery;
- skipping nearer opposing liquidity;
- censoring higher T-labels at actual S1;
- changing parameters after development begins;
- inspecting sensitivity before center-rule holdout completion;
- choosing best-performing neighboring parameter;
- switching feeds because outcomes improve;
- concatenating independent providers into the primary sequence;
- tuning to EXP-002;
- treating counterfactual target-label profit as actual Engine-G P&L.

---

# 59. Relationship to EXP-015

EXP-015 remains paused.

If Engine G passes historical validation, its persisted standardized candidate stream may later feed the redesigned ranker:

```text
validated Engine G candidate
    ->
target-first probability / EV
    ->
P&L-equivalent/risk gates
    ->
cross-market ranking
```

The ranker may rank Engine-G candidates.

It may not redefine Engine-G entry mechanics retrospectively.

---

# 60. Interpretation of EXP-016

EXP-016 does not test whether Engine G alone guarantees `$150–$200/day`.

It asks whether Engine G produces a:

```text
causal
reproducible
cost-robust
economically admissible
historically validated
candidate stream
```

surviving:

```text
development
+
validation
+
untouched same-feed holdout
+
uncertainty analysis
```

Only after that should the project move to:

- independent-feed validation;
- broker-specific execution modelling;
- forward/demo validation;
- additional validated engines;
- EXP-015 ranking;
- portfolio and daily-risk state-machine validation.
