# Engine H — Range Raid into Pre-existing FVG Reversal v0.2

**Status:** FROZEN PROSPECTIVELY — 2026-09-23  
**Engine ID:** `engine-h-range-raid-preexisting-fvg-reversal`  
**Version:** `0.2`  
**Experiment:** `EXP-018 — Engine H v0.2 Simplified MSS Confirmation`  
**Outcome status at freeze:** ZERO ENGINE-H-v0.2 OUTCOMES CALCULATED

## 1. Identity and change from v0.1

Engine H v0.2 preserves the v0.1 location thesis:

```text
recent 5m dealing range
    ->
older unmitigated 5m FVG outside the range
    ->
range-boundary raid into that FVG
    ->
close back inside the range
```

The v0.1 development funnel produced 180 in-window qualifying raids but only 2 accepted trades because the lower-timeframe confirmation stack was too restrictive.

v0.2 is a **new prospective version**, not a retune inside EXP-017.

The only conceptual redesign is the confirmation/entry layer:

```text
raid/rejection
    ->
causal 1m MSS within 20 active M1 bars
    ->
enter at next market-active M1 open
```

v0.2 removes:

- the 1.50x displacement threshold;
- the requirement that MSS/MSS+1/MSS+2 create a new 1m FVG;
- the midpoint-retracement entry;
- the 10-bar post-FVG entry wait.

The location logic, sweep logic, stop, target, 3-XAU room, 2R requirement, structural-risk gate, costs and data split remain unchanged unless explicitly restated below.

## 2. Market, source and exact price representation

Market: `XAUUSD`.

Primary source: Dukascopy-derived BID M1 OHLC from public repository `kevingtlin/Market-Data-Lab`.

Pinned external commit:

`922f83a60cc574e7395fb27397077288055a1ef6`

Pinned root tree:

`6596cd229c736f96bab7d1496656397b31326ca6`

Pinned XAUUSD BID M1 subtree:

`86dd3acd141ffe4b5eb8ad86a04ca42398d0b558`

Grid:

`τ = 0.001 XAU`.

All structural prices use exact integer ticks:

`price_tick = exact_decimal(source_price) * 1000`.

No binary-floating equality is allowed in structure, entry, stop, target or hit logic.

At 0.10 lot / 10 oz, one source tick = USD 0.01.

## 3. Source validity and active bars

Use the same frozen source-validity, carry-forward and market-active rules as H v0.1:

- exact whole-minute UTC timestamps;
- no duplicates or missing minutes in loaded monthly files;
- exact source-grid OHLC;
- positive valid OHLC geometry;
- carry-forward M1 = valid O=H=L=C equal to prior chronological close;
- market-active M1 = valid non-carry-forward minute;
- active ordinals exclude carry-forward minutes;
- a 5m bar requires all five chronological M1 rows and is market-active if at least one is active.

Missing/invalid rows may never be silently skipped.

## 4. Setup dates and window

New setups: UTC Monday-Friday only.

Qualifying 5m raid completion:

`06:00 <= close time < 18:00 UTC`.

MSS must complete before 18:00.

The next-active-M1-open entry must occur before 18:00.

Filled trades may continue only to the frozen horizon in Section 16.

## 5. Frozen recent dealing range

Before candidate 5m sweep bar `B` opens, freeze exactly the previous 12 market-active completed 5m bars.

`RANGE_HIGH = max(high)`

`RANGE_LOW = min(low)`

Require `RANGE_HIGH > RANGE_LOW`.

The range stays fixed for the entire setup/trade.

## 6. Pre-existing external 5m FVG

Use three consecutive market-active 5m ordinals.

Bullish FVG:

`low[j] > high[j-2]`

zone `[high[j-2], low[j]]`.

Bearish FVG:

`high[j] < low[j-2]`

zone `[high[j], low[j-2]]`.

An FVG exists only after the third bar closes and becomes eligible from the next market-active 5m bar.

Eligible age:

`1 <= age_active_5m <= 48`.

A subsequent active completed 5m bar overlapping the FVG mitigates it after that bar's event decision:

`bar_high >= FVG.lower AND bar_low <= FVG.upper`.

A mitigated/expired FVG never reactivates.

## 7. External-location relationship

Bearish reversal:

- selected FVG must be bearish;
- entire FVG must lie above range:
  `FVG.lower > RANGE_HIGH`.

Bullish reversal:

- selected FVG must be bullish;
- entire FVG must lie below range:
  `FVG.upper < RANGE_LOW`.

If multiple eligible FVGs exist, select the nearest to the swept boundary.

Tie-breaker:

1. more recently created FVG;
2. lower unique FVG ID.

## 8. Raid/rejection

Bearish:

1. `high > RANGE_HIGH`;
2. `high >= selected_bearish_FVG.lower`;
3. `RANGE_LOW < close < RANGE_HIGH`.

Bullish:

1. `low < RANGE_LOW`;
2. `low <= selected_bullish_FVG.upper`;
3. `RANGE_LOW < close < RANGE_HIGH`.

A bar qualifying both directions is:

`dual_sided_raid_ambiguous`.

All touched pre-existing FVGs are mitigated after the event decision.

## 9. Causal internal M1 pivot

At sweep completion freeze the most recent already-confirmed opposite-side 1m 2-left/2-right pivot whose center lies within the previous 15 market-active M1 ordinals and before sweep-bar open.

Bearish uses the most recent internal swing low.

Bullish uses the most recent internal swing high.

If unavailable:

`no_internal_mss_pivot`.

No later pivot substitution.

## 10. Simplified MSS confirmation

Search from the first market-active M1 bar after sweep completion.

Maximum:

`20 market-active M1 bars`.

Bearish MSS:

`close < frozen_internal_swing_low`.

Bullish MSS:

`close > frozen_internal_swing_high`.

Use the first qualifying close.

If none:

`mss_timeout_20`.

If the 18:00 cutoff occurs first:

`setup_window_closed_before_mss`.

No displacement/body threshold is part of v0.2.

No newly created 1m FVG is required.

## 11. Entry at next market-active M1 open

After MSS confirms, enter at the **open tick of the next market-active M1 bar**.

The entry bar must open before 18:00 UTC.

If no market-active M1 bar opens before 18:00:

`entry_window_closed_1800`.

The synthetic market entry price is exactly that next active M1 `open_tick`; there is no favorable midpoint assumption and no pending limit order.

If multiple still-valid Engine-H-v0.2 setups are scheduled for the same next market-active M1 open while flat, process them in deterministic priority order:

1. earlier sweep-completion timestamp;
2. if tied, lower setup ID.

Each setup is tested against the frozen geometry/risk/room/R:R admission rules using that open. The first setup that passes becomes the open trade. All remaining same-open setups are terminated as `suppressed_one_open`. If an earlier-priority setup fails admission, the next setup may be tested at that same open.

Because entry occurs at the bar open, the full OHLC of that entry bar is post-entry information for hit-testing and MFE/MAE.

## 12. Structural stop

Bearish:

`stop = sweep_5m_high + 1 tick`.

Bullish:

`stop = sweep_5m_low - 1 tick`.

After the next-open entry price is known, require valid geometry:

Bearish: `target < entry < stop`.

Bullish: `stop < entry < target`.

If geometry fails:

`invalid_entry_geometry_at_open`.

Gross structural stop distance:

`abs(entry-stop)`.

At 0.10 lot:

`gross_stop_USD = stop_distance_ticks * 0.01`.

Admission requires:

`gross_stop_USD <= USD 40`.

This is the same gross structural-risk gate as earlier engines, before transaction-cost stress.

Otherwise:

`structural_risk_above_40`.

No stop compression.

## 13. Actual target

Target remains the opposite side of the frozen pre-sweep range.

Bearish:

`TARGET = RANGE_LOW`.

Bullish:

`TARGET = RANGE_HIGH`.

Require:

`target_distance_ticks >= 3000`.

Otherwise:

`insufficient_target_room_3xau`.

Require:

`target_distance_ticks >= 2 * stop_distance_ticks`.

Otherwise:

`reward_risk_below_2`.

Target is frozen and never moves.

## 14. Entry-bar and later same-bar ordering

Entry occurs exactly at the entry bar open.

Therefore target/stop touches during that same M1 bar are eligible.

Conservative ordering:

- if both stop and target are touched on the entry bar: stop wins;
- if only stop is touched: stop;
- if only target is touched: target.

The same stop-first rule applies to every later bar containing both levels.

Because entry occurs at the bar open, fill-bar MFE/MAE are measured from that open and are not censored.

## 15. Counterfactual target ladder

Independently from original next-open entry, unchanged structural stop and unchanged full horizon:

- T30 = 3.000 XAU;
- T40 = 4.000 XAU;
- T50 = 5.000 XAU;
- T70 = 7.000 XAU;
- T100 = 10.000 XAU.

Actual opposite-range target does not censor these labels.

Each receives:

- `target_before_stop`;
- `stop_before_target`;
- `horizon_without_target_or_stop`.

Store actual-trade and counterfactual-potential MFE/MAE separately.

## 16. Exit horizon

Actual trade exits 100% at the earliest of:

1. opposite-range target;
2. structural stop;
3. close of the 120th market-active M1 bar counting entry bar as 1;
4. 20:00 UTC on entry date;
5. final available source bar.

No overnight carry.

No partials or runner.

## 17. One-open rule

Maximum one economically accepted Engine-H-v0.2 XAUUSD trade open.

A new qualifying setup while one is open receives:

`suppressed_one_open`.

It is not queued.

If a trade opens while other Engine-H-v0.2 setup pipelines are already pending from earlier raids, every other pending pipeline is immediately terminated as `suppressed_one_open`. Pending setups may not wait for the open trade to close.

Location-FVG mitigation caused by the raid still occurs.

## 18. Cost stress

Unchanged BID path.

Round-trip stresses:

- 0.00 XAU = USD 0;
- 0.25 XAU = USD 2.50;
- 0.50 XAU = USD 5.00.

Primary economics use 0.50 XAU.

Cost applies once per filled trade.

## 19. Deterministic terminal codes

Location/setup:

- `range_unavailable_12`
- `range_zero_width`
- `no_external_preexisting_fvg`
- `raid_without_rejection_close`
- `dual_sided_raid_ambiguous`
- `outside_setup_window`
- `suppressed_one_open`

Confirmation/entry:

- `no_internal_mss_pivot`
- `mss_timeout_20`
- `setup_window_closed_before_mss`
- `entry_window_closed_1800`
- `invalid_entry_geometry_at_open`
- `structural_risk_above_40`
- `insufficient_target_room_3xau`
- `reward_risk_below_2`

Filled exits:

- `exit_target`
- `exit_stop`
- `exit_stop_entry_bar`
- `exit_timeout_120`
- `exit_session_2000`
- `exit_data_end`

## 20. Frozen data split

The frozen immutable BID manifest remains exactly the EXP-017/EXP-016 manifest.

Warm-up only:

`2023-12-01 through 2023-12-31`.

Development:

`2024-01-01 through 2025-02-28`.

Validation:

`2025-03-01 through 2025-08-31`.

Fresh holdout:

`2025-09-01 through 2026-02-28`.

March 1-August 20, 2026 remains quarantined.

Neither Engine G v0.1 nor Engine H v0.1 inspected H-v0.2 validation/holdout outcomes.

## 21. Required reporting

Per permitted split report:

- full raid/setup funnel and all terminal reasons;
- accepted filled trades;
- target/stop/timeout rates;
- T30/T40/T50/T70/T100 counterfactual rates;
- gross/net expectancy under all cost stresses;
- profit factor;
- total/mean/median daily P&L including zero-trade eligible weekdays;
- <=USD50 and >=USD100/150/200 weekday proportions;
- maximum drawdown from USD500 reference;
- losing-trade and losing-day streaks;
- target/stop distance distributions;
- actual and potential MFE/MAE;
- direction contribution;
- external-FVG age/distance;
- bootstrap uncertainty.

## 22. Bootstrap

5 eligible-weekday moving blocks.

10,000 replications.

Seed:

`18018`.

Percentile 95% interval.

Primary bootstrap statistics:

- net USD expectancy/trade at primary cost;
- mean net USD/eligible weekday at primary cost.

## 23. Minimum evidence

Development >=100 accepted filled trades.

Validation >=50.

Fresh holdout >=50.

Below threshold:

`INSUFFICIENT_EVIDENCE`.

## 24. Historical-edge promotion criteria

All required under primary 0.50-XAU cost:

1. development expectancy/trade >0;
2. validation expectancy/trade >0;
3. holdout expectancy/trade >0;
4. validation PF >=1.10;
5. holdout PF >=1.10;
6. validation bootstrap expectancy lower bound >0;
7. holdout bootstrap expectancy lower bound >0;
8. no expectancy sign reversal;
9. minimum evidence counts satisfied;
10. no causal/provenance defect;
11. no optimistic same-bar dependency.

Drawdown/streak evidence remains mandatory but no new arbitrary hard cutoff is introduced.

## 25. Execution sequence

1. freeze v0.2 and EXP-018 before outcomes;
2. implement and unit-test;
3. run development only;
4. checkpoint development;
5. proceed to validation only if v0.2 remains eligible for promotion;
6. checkpoint validation;
7. proceed to fresh holdout only if still eligible.

If development fails decisively or is below minimum evidence, stop before validation.

No post-outcome v0.2 retuning. Further changes require v0.3/new experiment.

## 26. Relationship to system objective

Engine H v0.2 is one candidate source.

Even if validated, the USD150-200 strong-day objective remains a later multi-engine/ranker/risk-state-machine problem. EXP-015 stays paused until at least one engine validates.
