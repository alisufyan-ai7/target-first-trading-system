# Engine H — Range Raid into Pre-existing FVG Reversal v0.1

**Status:** FROZEN PROSPECTIVELY — 2026-09-23  
**Engine ID:** `engine-h-range-raid-preexisting-fvg-reversal`  
**Version:** `0.1`  
**Experiment:** `EXP-017 — Engine H Range Raid into Pre-existing FVG Reversal v0.1`  
**Outcome status at freeze:** ZERO ENGINE-H OUTCOMES CALCULATED

## 1. Identity

Engine H is a new prospective engine.

It is not Engine G v0.2, not a retuned Engine G, and not recovered Engine A.

It formalizes the two user-provided video motifs as:

```text
compact recent 5m dealing range
    ->
older unmitigated 5m FVG outside the range
    ->
range-boundary liquidity raid into that pre-existing FVG
    ->
close back inside the range
    ->
causal 1m internal MSS
    ->
directional 1m displacement that creates a new entry FVG
    ->
midpoint retracement entry
    ->
stop beyond the raid extreme
    ->
opposite side of the frozen pre-sweep range
```

Video-supported observations and prospective formalization are deliberately separated:

- Video 1 visibly supports liquidity sweep -> lower-timeframe MSS -> strong displacement/FVG -> reversal entry.
- Video 2 visibly supports a defined range high/low plus a pre-existing FVG beyond the range boundary and a raid toward/into that FVG before reversal.
- The exact bar counts, timeframes, age limits, numerical displacement threshold, and execution rules below are prospective project formalizations frozen before Engine-H outcomes. They are not attributed to the video creator unless visibly demonstrated.

## 2. Market, source and price representation

Initial market: `XAUUSD`.

Primary data: frozen Dukascopy-derived XAUUSD BID M1 OHLC, UTC, public transport `kevingtlin/Market-Data-Lab`.

Pinned external repository commit:

`922f83a60cc574e7395fb27397077288055a1ef6`

Pinned root tree:

`6596cd229c736f96bab7d1496656397b31326ca6`

Pinned XAUUSD BID M1 subtree:

`86dd3acd141ffe4b5eb8ad86a04ca42398d0b558`

Source grid:

`τ = 0.001 XAU`

All structural prices use exact integer source-grid ticks. Parse CSV decimal text exactly; `price_tick = exact_decimal(price) * 1000`. Binary floating-point equality must never define price identity, FVG boundaries, range ties, entries, stops, targets or hit tests.

At the project XAU 0.10-lot / 10-oz research convention, one source tick = USD 0.01.

## 3. Source validity, carry-forward and active bars

Use the same deterministic source-row validity rules frozen for Engine G:

- exact whole-minute UTC timestamp;
- no duplicate timestamp;
- exact three-decimal source grid;
- finite positive OHLC;
- high >= open/close/low;
- low <= open/close.

A carry-forward M1 minute is valid but has `O=H=L=C` equal to the immediately preceding chronological valid M1 close.

A market-active M1 bar is a valid non-carry-forward minute.

Market-active M1 bars receive consecutive active ordinals. Carry-forward bars do not increment active-M1 counters.

UTC-aligned 5m bars require all five chronological constituent M1 rows. A 5m bar is market-active if at least one constituent M1 bar is market-active. Entirely carry-forward 5m bars do not increment active-5m ordinals and cannot create structure or setups.

Whenever this spec says consecutive active M1/5m bars, it means consecutive market-active ordinals; valid carry-forward rows may lie between them in wall-clock time, but missing/invalid data may never be skipped.

## 4. Trading dates and setup window

New setups may be created only Monday-Friday.

Sweep completion must satisfy:

`06:00 <= UTC completion time < 18:00`.

MSS, entry-FVG confirmation and entry fill must also complete before 18:00.

Once filled, a trade may continue until the frozen exit horizon in Section 18.

## 5. Frozen recent dealing range

For every candidate market-active 5m sweep bar `B`, freeze the range before `B` opens.

Use exactly the previous:

`12 market-active completed 5m bars`.

Define:

`RANGE_HIGH = max(high_tick over those 12 bars)`

`RANGE_LOW = min(low_tick over those 12 bars)`

Require `RANGE_HIGH > RANGE_LOW`.

No range is available until 12 active 5m bars exist.

The range remains frozen throughout the setup and any resulting trade.

No ATR compression filter is part of v0.1.

## 6. Pre-existing 5m location FVG

Use three consecutive market-active 5m ordinals `j-2,j-1,j`.

Bullish 5m FVG:

`low[j] > high[j-2]`

Zone:

`lower = high[j-2]`  
`upper = low[j]`

Bearish 5m FVG:

`high[j] < low[j-2]`

Zone:

`lower = high[j]`  
`upper = low[j-2]`

Require `upper > lower`.

The FVG is created only after bar `j` closes and becomes eligible from the next market-active 5m bar.

Each FVG is an individual instance with:

- unique ID;
- direction/class;
- lower/upper integer ticks;
- creation active-5m ordinal;
- creation timestamp;
- mitigated state;
- expiry state.

## 7. Location-FVG age and mitigation

A location FVG is eligible while:

`1 <= age_in_active_5m_bars <= 48`

where age is current candidate 5m ordinal minus the FVG creation ordinal.

It expires before a bar whose age exceeds 48.

Before a candidate sweep bar begins, an FVG must still be unmitigated.

A subsequent market-active completed 5m bar overlaps an FVG when:

`bar_high >= FVG.lower AND bar_low <= FVG.upper`.

Any such overlap mitigates that FVG after that bar's event decision.

Thus the candidate sweep bar itself may be the **first** mitigating touch and can use the pre-bar active FVG snapshot. After the sweep bar closes, the touched FVG is mitigated whether or not a setup is accepted.

A mitigated or expired FVG never reactivates.

## 8. External-location relationship

For a bearish reversal candidate:

- use only an unmitigated **bearish** 5m FVG;
- its entire zone must be above the frozen recent range:

`FVG.lower > RANGE_HIGH`.

For a bullish reversal candidate:

- use only an unmitigated **bullish** 5m FVG;
- its entire zone must be below the frozen recent range:

`FVG.upper < RANGE_LOW`.

If more than one eligible FVG exists on the same side, select the FVG nearest to the swept range boundary:

Bearish: minimum `FVG.lower - RANGE_HIGH`.

Bullish: minimum `RANGE_LOW - FVG.upper`.

Tie-breaker: more recently created FVG; then lower unique FVG ID.

## 9. Raid/rejection sweep

Bearish setup requires the same completed active 5m bar to:

1. trade strictly above the frozen range high:
   `high > RANGE_HIGH`;
2. enter the selected pre-existing bearish FVG:
   `high >= FVG.lower`;
3. close back strictly inside the range:
   `RANGE_LOW < close < RANGE_HIGH`.

Bullish setup requires:

1. `low < RANGE_LOW`;
2. `low <= FVG.upper`;
3. close back strictly inside the range:
   `RANGE_LOW < close < RANGE_HIGH`.

Equality with the range boundary alone is not a raid.

The sweep bar need not traverse the whole FVG; first overlap is enough.

A bar qualifying both bullish and bearish is rejected as:

`dual_sided_raid_ambiguous`.

All FVGs touched by the completed sweep bar become mitigated after the decision.

## 10. Internal M1 pivot for MSS

At qualifying sweep completion, freeze the most recent already-confirmed opposite-side M1 2-left/2-right pivot from the previous 15 market-active M1 ordinals.

Swing high centered at active M1 ordinal `t`:

- high[t] > high[t-1]
- high[t] > high[t-2]
- high[t] >= high[t+1]
- high[t] >= high[t+2]

Swing low is the exact mirror.

The center must occur before the 5m sweep bar begins. Its two right-side confirmation bars may complete by sweep close.

Bearish setup freezes the most recent confirmed internal swing low.

Bullish setup freezes the most recent confirmed internal swing high.

If none exists:

`no_internal_mss_pivot`.

## 11. MSS

Search from the first market-active M1 bar after sweep completion for at most 10 active M1 bars.

Bearish MSS:

`close < frozen_internal_swing_low`.

Bullish MSS:

`close > frozen_internal_swing_high`.

Use the first qualifying close.

Failure:

`mss_timeout_10`.

If 18:00 is reached first:

`setup_window_closed_before_mss`.

## 12. 1m displacement

The displacement candle must be one of:

- MSS bar;
- MSS+1 active M1;
- MSS+2 active M1.

For candidate bar `k`:

`BODY = abs(close-open)`.

Baseline:

mean absolute body of the previous 20 market-active M1 bars.

Frozen threshold:

`BODY >= 1.50 * baseline`.

Implement exactly as:

`40 * BODY_TICKS >= 3 * SUM_PREVIOUS_20_BODY_TICKS`.

Bearish displacement also requires `close < open` and `close < frozen_internal_swing_low`.

Bullish displacement requires `close > open` and `close > frozen_internal_swing_high`.

Use the first qualifying candle.

If none by MSS+2:

`displacement_timeout_mss_plus_2`.

## 13. New 1m entry FVG

The displacement candle itself must be the third candle of a same-direction 1m FVG.

Use three consecutive active M1 ordinals `k-2,k-1,k`.

Bullish:

`low[k] > high[k-2]`.

Zone: `[high[k-2], low[k]]`.

Bearish:

`high[k] < low[k-2]`.

Zone: `[high[k], low[k-2]]`.

There is no minimum entry-FVG width.

If a qualifying displacement bar does not itself form the corresponding FVG, continue to MSS+1/MSS+2 only if those bars independently satisfy both the displacement and FVG rules.

If no qualifying displacement+FVG candle exists by MSS+2:

`no_entry_fvg_by_mss_plus_2`.

## 14. Entry

Entry is the 50% midpoint of the new 1m entry FVG.

If the midpoint lies between source ticks:

- long entry rounds upward to the next tick;
- short entry rounds downward to the next tick.

Search at most 10 market-active M1 bars after entry-FVG confirmation.

Long fills when `low <= entry`.

Short fills when `high >= entry`.

Entry must fill before 18:00.

Failures:

- `entry_timeout_10`;
- `entry_window_closed_1800`.

No market-order substitution.

## 15. Structural stop

Bearish:

`stop = sweep_5m_high + 1 tick`.

Bullish:

`stop = sweep_5m_low - 1 tick`.

Require correct geometry beyond the entry.

Gross structural stop risk at 0.10 lot:

`gross_stop_USD = stop_distance_ticks * 0.01`.

Admission requires:

`gross_stop_USD <= USD 40`.

This remains a gross structural-risk gate before transaction-cost stress. A maximum-admitted stopped trade can therefore net approximately -USD 45 under the primary USD 5 round-trip cost stress.

No stop compression.

## 16. Actual H target

The target is the **opposite side of the frozen pre-sweep 12-active-5m dealing range**.

Bearish trade:

`TARGET = RANGE_LOW`.

Bullish trade:

`TARGET = RANGE_HIGH`.

The target is frozen at sweep creation and never moves.

Require profitable geometry:

Bearish: `TARGET < entry < stop`.

Bullish: `stop < entry < TARGET`.

Otherwise:

`invalid_target_geometry`.

Minimum target distance:

`abs(TARGET-entry) >= 3.000 XAU = 3000 ticks`.

Otherwise:

`insufficient_target_room_3xau`.

Minimum reward/risk:

`target_distance_ticks >= 2 * stop_distance_ticks`.

Otherwise:

`reward_risk_below_2`.

These two thresholds are frozen prospectively before Engine-H outcomes and reflect the visibly asymmetric reward/risk boxes in the videos plus the project's economically meaningful Gold-move objective.

## 17. Pre-entry cancellation

After entry-FVG confirmation but before fill:

- if structural stop is touched first: `preentry_structural_invalidation`;
- if the frozen opposite-range target is touched first: `preentry_target_reached`.

If entry and stop are both touched on the fill bar: entry occurs and stop wins.

If entry and target are both touched on the fill bar: entry occurs but the target receives no fill-bar credit.

## 18. Actual trade exit and horizon

Actual v0.1 trade exits 100% at the frozen opposite-range target.

No partials, runners, dynamic targets or target substitution.

Trade terminates at the earliest of:

1. target;
2. structural stop;
3. close of the 120th market-active M1 bar counting fill bar as bar 1;
4. 20:00 UTC on entry date;
5. final available data bar.

No overnight carry.

## 19. Same-bar ordering and excursions

Conservative ordering:

- fill bar stop wins if touched;
- fill-bar target receives no credit;
- on later bars, if stop and target both touch, stop wins.

Actual MFE/MAE run only until actual target/stop/timeout.

Fill-bar excursions are excluded unless stop is hit; if fill-bar stop occurs, MFE starts at zero.

## 20. Counterfactual target ladder

Independently evaluate from the original entry with unchanged structural stop and unchanged 120-active-M1/20:00 horizon, ignoring the actual opposite-range target exit:

- T30 = +3.000 XAU;
- T40 = +4.000 XAU;
- T50 = +5.000 XAU;
- T70 = +7.000 XAU;
- T100 = +10.000 XAU.

Each rung receives:

- `target_before_stop`;
- `stop_before_target`;
- `horizon_without_target_or_stop`.

Higher rungs continue counterfactually after lower rungs or the actual Engine-H target.

Counterfactual potential MFE/MAE are stored separately from actual-trade MFE/MAE.

## 21. One-open rule

Maximum one economically accepted Engine-H XAUUSD trade open at once.

A new qualifying raid while one Engine-H trade is open receives:

`suppressed_one_open`.

It is not queued.

Pre-existing FVG mitigation caused by the bar still occurs.

## 22. Cost stress

Keep BID price paths unchanged.

Round-trip cost stresses:

- 0.00 XAU = 0 ticks = USD 0/trade;
- 0.25 XAU = 250 ticks = USD 2.50/trade;
- 0.50 XAU = 500 ticks = USD 5/trade.

Primary historical-edge economics use 0.50 XAU.

Cost is deducted once per filled trade, including winners, stops and timeouts.

## 23. Deterministic terminal reason codes

Setup/location:

- `range_unavailable_12`
- `range_zero_width`
- `no_external_preexisting_fvg`
- `outside_setup_window`
- `raid_without_rejection_close`
- `dual_sided_raid_ambiguous`
- `suppressed_one_open`

Confirmation/construction:

- `no_internal_mss_pivot`
- `mss_timeout_10`
- `setup_window_closed_before_mss`
- `displacement_baseline_unavailable_20`
- `displacement_timeout_mss_plus_2`
- `no_entry_fvg_by_mss_plus_2`
- `setup_window_closed_before_entry_fvg`
- `invalid_stop_geometry`
- `structural_risk_above_40`
- `invalid_target_geometry`
- `insufficient_target_room_3xau`
- `reward_risk_below_2`

Pre-entry:

- `preentry_structural_invalidation`
- `preentry_target_reached`
- `entry_timeout_10`
- `entry_window_closed_1800`

Filled exits:

- `exit_target`
- `exit_stop`
- `exit_stop_fill_bar`
- `exit_timeout_120`
- `exit_session_2000`
- `exit_data_end`

## 24. Frozen primary source manifest

The BID monthly manifest is identical to the already-audited immutable source files used by EXP-016:

| Role | File | Git blob SHA | Bytes |
|---|---|---|---:|
| Warm-up | `xauusd_bid_m1_2023_12.csv` | `56dbf8a5316c48f4ec3300126c0decda03f8325f` | 2231969 |
| Dev | `xauusd_bid_m1_2024_01.csv` | `f439cc6e17e39addc1a464eb0ccf8fe2eb71de99` | 2231993 |
| Dev | `xauusd_bid_m1_2024_02.csv` | `b3ad49d5e784fb8c879f8e12095640f454f8f5fb` | 2087847 |
| Dev | `xauusd_bid_m1_2024_03.csv` | `cdd53e37cc41773cc0d5c9210daefbf5ef6c3535` | 2231983 |
| Dev | `xauusd_bid_m1_2024_04.csv` | `f2e7801f91829e9aeeebbd88f9177350cc6ba043` | 2159936 |
| Dev | `xauusd_bid_m1_2024_05.csv` | `b49cd640075396bf656578c52e7dac0d9e472a22` | 2232006 |
| Dev | `xauusd_bid_m1_2024_06.csv` | `6c4dc31818a7e04d90f165df0930489cdf5e7121` | 2159852 |
| Dev | `xauusd_bid_m1_2024_07.csv` | `1a9877d863a7cadcfb47388a2d7b6657b57873ed` | 2231718 |
| Dev | `xauusd_bid_m1_2024_08.csv` | `29c3275f68b15d33325a7a989e322565fca4a64e` | 2231775 |
| Dev | `xauusd_bid_m1_2024_09.csv` | `075fc0b3c4f01bfebdbdb21af82c66595c2fd6cc` | 2159940 |
| Dev | `xauusd_bid_m1_2024_10.csv` | `ab734d9cea86c2441b2592e6aa0537829bd093f5` | 2231815 |
| Dev | `xauusd_bid_m1_2024_11.csv` | `4fe07a39a96512d4264202d4817fafedb3b97e79` | 2159626 |
| Dev | `xauusd_bid_m1_2024_12.csv` | `a5a219ccee1e3808593f349a56274d6242fe31dd` | 2231444 |
| Dev | `xauusd_bid_m1_2025_01.csv` | `f0211e901b6f8b26996ba1a48aeba73f599bd5fe` | 2231746 |
| Dev | `xauusd_bid_m1_2025_02.csv` | `e3beb3def6e2502975046d07f43db777604110b2` | 2015844 |
| Validation | `xauusd_bid_m1_2025_03.csv` | `fefe437f1f5b7565ca3cf10c10c60a63edf527ef` | 2231490 |
| Validation | `xauusd_bid_m1_2025_04.csv` | `aff4975ce8522f28951940db2daff3f36d5b3155` | 2159648 |
| Validation | `xauusd_bid_m1_2025_05.csv` | `6470db6ad153edb9bffd41660d0ae9b4370e4662` | 2231564 |
| Validation | `xauusd_bid_m1_2025_06.csv` | `b21e4764f19340da04b524f228264ff907d818f0` | 2159802 |
| Validation | `xauusd_bid_m1_2025_07.csv` | `f832021fb3a42d7299830d5420c241d75977293d` | 2231995 |
| Validation | `xauusd_bid_m1_2025_08.csv` | `57eb33cd0e3216612f20bdd24ffcb380a8950fb6` | 2231992 |
| Holdout | `xauusd_bid_m1_2025_09.csv` | `d9d02b8459d59e624fb10eaf5ee8eed3c8e71a32` | 2159764 |
| Holdout | `xauusd_bid_m1_2025_10.csv` | `2abab9482acf9a1612d2270a8c154ef29d7cfa76` | 2231779 |
| Holdout | `xauusd_bid_m1_2025_11.csv` | `d352855e8e795e8b63bd0061fe49bf36976bbe14` | 2159800 |
| Holdout | `xauusd_bid_m1_2025_12.csv` | `48b6a35faefba150cc05b7bf9ae849e90af2b3d5` | 2231857 |
| Holdout | `xauusd_bid_m1_2026_01.csv` | `e94768e8723896c4564085d308bff773384b0b0d` | 2231894 |
| Holdout | `xauusd_bid_m1_2026_02.csv` | `7a4190c519c665e9b0381a72e1ce2763a7759c11` | 2015873 |

Before any split outcome is produced, every loaded file must match path, frozen blob SHA, byte count, expected full-calendar row count and exact minute chronology.

## 25. Primary split

Warm-up only:

`2023-12-01 through 2023-12-31 UTC`.

Development:

`2024-01-01 through 2025-02-28 UTC`.

Validation:

`2025-03-01 through 2025-08-31 UTC`.

Fresh holdout:

`2025-09-01 through 2026-02-28 UTC`.

March 1-August 20, 2026 remains quarantined from the primary decision because earlier project research inspected it extensively.

Engine G never inspected the Engine-H validation or holdout periods for Engine-H outcomes; EXP-016 stopped after its development split.

## 26. Required metrics

For each permitted split report:

- raid/setup funnel and all terminal reasons;
- accepted filled trades;
- target/stop/timeout rates;
- independent T30/T40/T50/T70/T100 rates;
- gross expectancy;
- net expectancy at 0/0.25/0.50 XAU cost;
- profit factor;
- total net P&L;
- mean/median eligible-weekday P&L including zero-trade weekdays;
- losing weekday %, <=USD50 %, >=USD100/150/200 %;
- maximum drawdown from USD500 reference;
- maximum consecutive losing trades and cumulative loss of worst run;
- consecutive losing/low-output weekdays;
- target, stop, MFE/MAE and potential-MFE/MAE distributions;
- direction contribution;
- location-FVG age/distance contribution;
- bootstrap uncertainty.

## 27. Bootstrap

Use the same frozen deterministic moving-block bootstrap discipline:

- 5 consecutive eligible weekdays per block;
- 10,000 replications;
- seed `17017`;
- percentile 95% interval.

Primary statistics:

- mean net USD expectancy/trade at 0.50-XAU cost;
- mean net USD per eligible weekday at 0.50-XAU cost.

## 28. Minimum evidence

Development accepted filled trades >=100.

Validation >=50.

Fresh holdout >=50.

A segment below its threshold is `INSUFFICIENT_EVIDENCE`.

## 29. Historical-edge promotion criteria

At primary 0.50-XAU cost, all must hold:

1. development expectancy/trade >0;
2. validation expectancy/trade >0;
3. holdout expectancy/trade >0;
4. validation PF >=1.10;
5. holdout PF >=1.10;
6. validation bootstrap expectancy lower bound >0;
7. holdout bootstrap expectancy lower bound >0;
8. no expectancy sign reversal;
9. minimum evidence counts satisfied;
10. no causal/data defect;
11. no optimistic same-bar dependency.

MDD/streak evidence is mandatory but no arbitrary new hard cutoff is invented in EXP-017.

Passing means historical engine candidate source only, not live authorization.

## 30. Execution sequence and stop discipline

1. freeze this spec and EXP-017 in GitHub;
2. implement and unit-test without outcomes;
3. run development only;
4. checkpoint development;
5. proceed to validation only if development remains eligible for promotion;
6. checkpoint validation;
7. proceed to fresh holdout only if still eligible;
8. checkpoint holdout;
9. only then consider sensitivity/independent-feed work.

If development fails a mandatory promotion criterion decisively or is below minimum evidence, stop before validation and preserve untouched data.

No post-outcome retuning of v0.1. Any change to range window, location-FVG age/relationship, raid logic, MSS, displacement, entry-FVG, target, RR, risk gate, sessions or horizon requires Engine H v0.2/new experiment.

## 31. Relationship to system objective

Engine H is one candidate engine, not the entire USD150-200 strong-day system.

If validated, it can later feed EXP-015 alongside other independently validated engines. The target-first layer ranks validated candidates; it does not invent or retroactively redefine Engine-H trades.
