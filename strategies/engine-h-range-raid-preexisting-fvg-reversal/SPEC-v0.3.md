# Engine H — Range Raid into Pre-existing FVG Reversal v0.3

**Status:** FROZEN PROSPECTIVELY — 2026-09-23  
**Engine ID:** `engine-h-range-raid-preexisting-fvg-reversal`  
**Version:** `0.3`  
**Experiment:** `EXP-019 — Engine H v0.3 Post-Raid Structural Stop + T40 Target`  
**Outcome status at freeze:** ZERO ENGINE-H-v0.3 OUTCOMES CALCULATED

## 1. Identity and rationale

Engine H v0.3 preserves the v0.2 location and confirmation thesis:

```text
recent 5m dealing range
    ->
older unmitigated 5m FVG outside the range
    ->
range-boundary raid into that FVG
    ->
close back inside the range
    ->
causal 1m MSS
    ->
next-active-M1-open entry
```

The prospective redesign is limited to stop/target architecture.

v0.2 showed that confirmation was no longer the main bottleneck: 69 setups reached MSS/next-open admission, but the opposite-range target plus sweep-extreme stop plus 3-XAU/2R geometry admitted only 6 trades.

v0.3 therefore tests:

```text
post-raid 1m structural invalidation stop
+
fixed target-first Gold objective
```

Primary actual target:

`+4.000 XAU / 4000 ticks / approximately USD 40 gross at 0.10 lot`.

Predeclared target diagnostics:

`T30 = 3.000 XAU` and `T50 = 5.000 XAU`.

T70/T100 remain counterfactual reachability labels only.

No v0.3 outcome was inspected before this specification was frozen.

## 2. Market, source and exact price representation

Market: `XAUUSD`.

Primary source: Dukascopy-derived BID M1 OHLC from public repository:

`kevingtlin/Market-Data-Lab`.

Pinned external commit:

`922f83a60cc574e7395fb27397077288055a1ef6`

Pinned root tree:

`6596cd229c736f96bab7d1496656397b31326ca6`

Pinned XAUUSD BID M1 subtree:

`86dd3acd141ffe4b5eb8ad86a04ca42398d0b558`

Source grid:

`τ = 0.001 XAU`.

All structural prices use exact integer ticks:

`price_tick = exact_decimal(source_price) * 1000`.

No binary floating-point equality is permitted for structural comparisons.

At the project's XAU 0.10-lot / 10-oz research convention:

`1 source tick = USD 0.01`.

## 3. Source validity and market-active bars

Use the same source rules as frozen Engine H v0.2:

- exact whole-minute UTC timestamps;
- no duplicate or missing rows in loaded complete-month files;
- exact 0.001-XAU source grid;
- positive valid OHLC geometry;
- carry-forward M1 = valid O=H=L=C equal to prior chronological valid close;
- market-active M1 = valid non-carry-forward minute;
- carry-forward minutes do not increment active-M1 ordinal;
- UTC-aligned 5m bars require all five chronological M1 rows;
- a 5m bar is market-active if at least one constituent M1 is active;
- all-carry-forward 5m bars do not increment active-5m ordinal and cannot create structure/setups.

Missing/invalid rows may never be silently skipped.

## 4. Setup dates and time window

New setups may be created UTC Monday-Friday.

Qualifying 5m raid must complete:

`06:00 <= completion < 18:00 UTC`.

MSS must complete before 18:00.

The next-active-M1-open entry must occur before 18:00.

Filled trades terminate under the frozen horizon in Section 17.

## 5. Frozen recent 5m dealing range

Before candidate market-active 5m sweep bar `B` opens, freeze exactly the previous 12 market-active completed 5m bars.

`RANGE_HIGH = max(high_tick)`

`RANGE_LOW = min(low_tick)`

Require:

`RANGE_HIGH > RANGE_LOW`.

The range stays frozen through the entire setup/trade.

## 6. Pre-existing external 5m FVG

Use three consecutive market-active 5m ordinals.

Bullish FVG:

`low[j] > high[j-2]`

zone:

`[high[j-2], low[j]]`.

Bearish FVG:

`high[j] < low[j-2]`

zone:

`[high[j], low[j-2]]`.

FVG exists after the third bar closes and is eligible beginning with the next active 5m bar.

Eligible age:

`1 <= age_active_5m <= 48`.

A later market-active completed 5m bar mitigates an eligible FVG after event evaluation when:

`bar_high >= FVG.lower AND bar_low <= FVG.upper`.

A mitigated or expired FVG never reactivates.

## 7. External-FVG location relationship

Bearish candidate:

- use an unmitigated bearish FVG;
- entire zone must be above the frozen range:
  `FVG.lower > RANGE_HIGH`.

Bullish candidate:

- use an unmitigated bullish FVG;
- entire zone must be below the frozen range:
  `FVG.upper < RANGE_LOW`.

If multiple FVGs qualify, select nearest to the swept boundary.

Tie-break:

1. most recently created;
2. lower unique FVG ID.

## 8. Raid/rejection

Bearish:

1. `high > RANGE_HIGH`;
2. `high >= selected bearish FVG.lower`;
3. `RANGE_LOW < close < RANGE_HIGH`.

Bullish:

1. `low < RANGE_LOW`;
2. `low <= selected bullish FVG.upper`;
3. `RANGE_LOW < close < RANGE_HIGH`.

A bar qualifying both directions:

`dual_sided_raid_ambiguous`.

All touched eligible FVGs are mitigated after the completed-bar event decision.

## 9. Frozen internal M1 pivot for MSS

At raid completion, freeze the most recent already-confirmed opposite-side 1m 2-left/2-right pivot whose center lies within the previous 15 market-active M1 ordinals and before the sweep 5m bar opens.

Swing high center `t`:

- high[t] > high[t-1];
- high[t] > high[t-2];
- high[t] >= high[t+1];
- high[t] >= high[t+2].

Swing low is the exact mirror.

Bearish setup freezes the most recent internal swing low.

Bullish setup freezes the most recent internal swing high.

If absent:

`no_internal_mss_pivot`.

No pivot substitution.

## 10. MSS

Search from the first market-active M1 bar after the raid completes.

Maximum:

`20 active M1 bars`.

Bearish:

`close < frozen_internal_swing_low`.

Bullish:

`close > frozen_internal_swing_high`.

Use the first qualifying close.

If none:

`mss_timeout_20`.

If 18:00 occurs first:

`setup_window_closed_before_mss`.

## 11. Post-raid invalidation pivot

At the MSS close, freeze a separate post-raid invalidation pivot.

Bearish trade requires the most recent **confirmed 1m swing high** satisfying:

- swing center timestamp >= raid/sweep completion timestamp;
- swing center active ordinal < MSS active ordinal;
- pivot confirmation active ordinal <= MSS active ordinal.

Bullish trade requires the most recent **confirmed 1m swing low** satisfying the same temporal rules.

If no such post-raid invalidation pivot exists at MSS confirmation:

`no_postraid_invalidation_pivot`.

This pivot is not allowed to update later.

## 12. Entry

Entry occurs at the exact open tick of the next market-active M1 bar after MSS confirmation.

The entry bar must open before 18:00.

If not:

`entry_window_closed_1800`.

If several pending v0.3 setups want the same next active M1 open while flat:

1. earlier raid completion timestamp;
2. lower setup ID.

Test each in priority order. The first passing admission opens the trade. Remaining same-open setups are `suppressed_one_open`.

If an earlier-priority setup fails admission, test the next at the same open.

## 13. Post-raid structural stop

Bearish:

`STOP = postraid_swing_high + 1 tick`.

Bullish:

`STOP = postraid_swing_low - 1 tick`.

Require:

Bearish:

`entry < STOP`.

Bullish:

`STOP < entry`.

Otherwise:

`invalid_postraid_stop_geometry`.

Gross stop distance:

`abs(entry - STOP)`.

Gross structural-risk admission remains:

`gross_stop_USD <= USD 40`

equivalent to:

`stop_distance_ticks <= 4000`.

This is before transaction-cost stress.

No stop compression and no fallback to the 5m sweep extreme.

If no valid lower-timeframe stop exists, reject rather than substituting another stop.

## 14. Fixed target-first actual target

Actual v0.3 profit target is fixed at:

`4000 ticks = 4.000 XAU`.

Long:

`TARGET = entry + 4000`.

Short:

`TARGET = entry - 4000`.

This is the **primary execution rule**, chosen prospectively.

No opposing-range target requirement.

No 3-XAU structural-room gate.

No separate 2R gate.

Because gross stop admission is capped at 4000 ticks, the primary target has gross reward/risk >=1.0 by construction.

The frozen recent range and opposite range boundary remain recorded as diagnostics, not target gates.

## 15. Target ladder diagnostics

Independently from the same original entry and unchanged structural stop/horizon:

- T30 = favorable move of 3000 ticks;
- T40 = favorable move of 4000 ticks;
- T50 = favorable move of 5000 ticks;
- T70 = favorable move of 7000 ticks;
- T100 = favorable move of 10000 ticks.

T40 is identical to the actual target threshold but is still stored in the common counterfactual-label schema.

T30/T50 are the primary predeclared target-ladder diagnostics.

T70/T100 remain secondary reachability diagnostics.

No diagnostic rung may replace the primary T40 execution rule because it performs better historically.

## 16. Entry-bar and same-bar ordering

Entry occurs exactly at the next active M1 bar open.

Therefore that bar's full high/low is post-entry information.

On the entry bar:

- if stop and T40 target both touch: stop wins;
- if only stop touches: stop;
- if only T40 touches: target.

For counterfactual labels, if stop and that rung both touch on the same bar:

`stop_before_target`.

The same conservative ordering applies on later bars.

Actual and potential MFE/MAE include the entry bar from the exact open.

## 17. Exit horizon

Actual v0.3 exits 100% at the earliest of:

1. fixed T40 target;
2. post-raid structural stop;
3. close of 120th market-active M1 bar counting entry bar as bar 1;
4. 20:00 UTC on entry date;
5. final available source bar.

No overnight carry.

No partials or runner.

## 18. One-open rule

Maximum one economically accepted Engine-H-v0.3 XAUUSD trade open.

A new qualifying setup while one is open:

`suppressed_one_open`.

If a trade opens while other H-v0.3 pipelines are pending, all other pending pipelines immediately become:

`suppressed_one_open`.

No queueing behind an open trade.

FVG mitigation still occurs independently.

## 19. Cost stress

Unchanged BID path.

Round-trip stress:

- 0.00 XAU = 0 ticks = USD 0;
- 0.25 XAU = 250 ticks = USD 2.50;
- 0.50 XAU = 500 ticks = USD 5.

Primary historical economics use 0.50 XAU.

Cost is deducted exactly once per filled trade.

At the actual T40 target:

- gross winner at 0.10 lot = approximately +USD40;
- primary-cost net winner = approximately +USD35.

A maximum-admitted 4000-tick stop:

- gross loss = approximately -USD40;
- primary-cost net loss = approximately -USD45.

## 20. Deterministic reason codes

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
- `no_postraid_invalidation_pivot`
- `entry_window_closed_1800`
- `invalid_postraid_stop_geometry`
- `structural_risk_above_40`

Filled exits:

- `exit_t40`
- `exit_stop`
- `exit_stop_entry_bar`
- `exit_timeout_120`
- `exit_session_2000`
- `exit_data_end`

## 21. Expanded prospective development data

The v0.3 rule redesign was created from prior development evidence, but validation and holdout remain untouched.

To avoid lowering the >=100 development evidence threshold merely because H is sparse, v0.3 expands the development window backward into previously unused 2023 data.

Warm-up:

`2022-12-01 through 2022-12-31`.

Development:

`2023-01-01 through 2025-02-28`.

This is 26 months.

Predeclared development stability subperiods:

- DEV-A: `2023-01-01 through 2023-12-31`;
- DEV-B: `2024-01-01 through 2025-02-28`.

The combined development trade count must satisfy the minimum evidence rule, and both DEV-A and DEV-B primary-cost expectancy signs are reported separately.

Validation remains:

`2025-03-01 through 2025-08-31`.

Fresh holdout remains:

`2025-09-01 through 2026-02-28`.

March 1-August 20, 2026 remains quarantined.

## 22. Frozen additional development manifest

The pinned BID audit reports complete full-calendar coverage and zero gaps for every file below.

| Role | File | Git blob SHA | Bytes |
|---|---|---|---:|
| Warm-up | `xauusd_bid_m1_2022_12.csv` | `b654f2e8033584ba3aad37a9c197fae3fe044b08` | 2231796 |
| DEV-A | `xauusd_bid_m1_2023_01.csv` | `ad56ac464c6844640a3f7ae4e5d8b3c7c30a4e33` | 2231952 |
| DEV-A | `xauusd_bid_m1_2023_02.csv` | `95d40f88c4200f9163144e108aff0b03eb079a3b` | 2016006 |
| DEV-A | `xauusd_bid_m1_2023_03.csv` | `5f2d85e197a9bf19b9aca7db49ec7dfdb6b466c7` | 2231984 |
| DEV-A | `xauusd_bid_m1_2023_04.csv` | `9a3a8e99038d555880e7d2da7ad9047ba48850ff` | 2159920 |
| DEV-A | `xauusd_bid_m1_2023_05.csv` | `95eadc1e3b8cb9636935e8d80e46384fa5ab3438` | 2231972 |
| DEV-A | `xauusd_bid_m1_2023_06.csv` | `c603c32760c193c90c54906c2b388172c881616f` | 2159976 |
| DEV-A | `xauusd_bid_m1_2023_07.csv` | `a24667621441f3fa400d1c9bcce4f4a32ee30a09` | 2231931 |
| DEV-A | `xauusd_bid_m1_2023_08.csv` | `7f2838f0bb6212bea9aec1aca004d22fecaa141d` | 2231974 |
| DEV-A | `xauusd_bid_m1_2023_09.csv` | `b37bd67b75e3fd59d1e818e0618f26d6929a9042` | 2159931 |
| DEV-A | `xauusd_bid_m1_2023_10.csv` | `93a551f1e7371b7cc3f57ac3c50a2edb1e27c0d3` | 2231917 |
| DEV-A | `xauusd_bid_m1_2023_11.csv` | `e739d6a6cdf868dc83d37406a6a7d068f29d5de4` | 2159884 |
| DEV-A | `xauusd_bid_m1_2023_12.csv` | `56dbf8a5316c48f4ec3300126c0decda03f8325f` | 2231969 |
| DEV-B | `xauusd_bid_m1_2024_01.csv` | `f439cc6e17e39addc1a464eb0ccf8fe2eb71de99` | 2231993 |
| DEV-B | `xauusd_bid_m1_2024_02.csv` | `b3ad49d5e784fb8c879f8e12095640f454f8f5fb` | 2087847 |
| DEV-B | `xauusd_bid_m1_2024_03.csv` | `cdd53e37cc41773cc0d5c9210daefbf5ef6c3535` | 2231983 |
| DEV-B | `xauusd_bid_m1_2024_04.csv` | `f2e7801f91829e9aeeebbd88f9177350cc6ba043` | 2159936 |
| DEV-B | `xauusd_bid_m1_2024_05.csv` | `b49cd640075396bf656578c52e7dac0d9e472a22` | 2232006 |
| DEV-B | `xauusd_bid_m1_2024_06.csv` | `6c4dc31818a7e04d90f165df0930489cdf5e7121` | 2159852 |
| DEV-B | `xauusd_bid_m1_2024_07.csv` | `1a9877d863a7cadcfb47388a2d7b6657b57873ed` | 2231718 |
| DEV-B | `xauusd_bid_m1_2024_08.csv` | `29c3275f68b15d33325a7a989e322565fca4a64e` | 2231775 |
| DEV-B | `xauusd_bid_m1_2024_09.csv` | `075fc0b3c4f01bfebdbdb21af82c66595c2fd6cc` | 2159940 |
| DEV-B | `xauusd_bid_m1_2024_10.csv` | `ab734d9cea86c2441b2592e6aa0537829bd093f5` | 2231815 |
| DEV-B | `xauusd_bid_m1_2024_11.csv` | `4fe07a39a96512d4264202d4817fafedb3b97e79` | 2159626 |
| DEV-B | `xauusd_bid_m1_2024_12.csv` | `a5a219ccee1e3808593f349a56274d6242fe31dd` | 2231444 |
| DEV-B | `xauusd_bid_m1_2025_01.csv` | `f0211e901b6f8b26996ba1a48aeba73f599bd5fe` | 2231746 |
| DEV-B | `xauusd_bid_m1_2025_02.csv` | `e3beb3def6e2502975046d07f43db777604110b2` | 2015844 |

The previously frozen validation/holdout manifest from EXP-017/018 remains unchanged.

## 23. Contamination note

No earlier Target-First strategy-result experiment in the repository used calendar year 2023.

The 2023 period is therefore an unused development extension at v0.3 freeze.

The 2024-Jan through 2025-Feb period has been used as development by H v0.1/v0.2 and remains explicitly development, not validation.

The 2025-Mar through 2026-Feb validation/holdout periods remain untouched by Engine-H outcomes.

## 24. Required metrics

Report for combined development and separately for DEV-A / DEV-B:

- setup funnel and terminal reasons;
- accepted trades;
- T40 target / stop / timeout rates;
- T30/T40/T50/T70/T100 reachability;
- gross and cost-stressed expectancy;
- profit factor;
- total net P&L;
- eligible-weekday mean/median and output bands;
- maximum drawdown;
- losing-trade/day streaks;
- post-raid stop distance/risk distribution;
- actual and potential MFE/MAE;
- direction contribution;
- location-FVG age/distance;
- opposite-range-boundary distance diagnostic;
- bootstrap uncertainty for combined development.

## 25. Bootstrap

Combined development moving-block bootstrap:

- 5 consecutive eligible weekdays;
- 10,000 replications;
- seed `19019`;
- percentile 95%.

Primary statistics:

- net USD expectancy/trade at 0.50-XAU cost;
- mean net USD per eligible weekday at 0.50-XAU cost.

## 26. Minimum development evidence and stability

Combined development accepted filled trades:

`>=100`.

Validation:

`>=50`.

Fresh holdout:

`>=50`.

Below count threshold:

`INSUFFICIENT_EVIDENCE`.

Additionally report DEV-A and DEV-B expectancy separately.

For v0.3 to proceed to validation:

- combined development primary-cost expectancy must be >0;
- combined development must have >=100 accepted trades;
- DEV-A and DEV-B primary-cost expectancy must both be >0.

This subperiod sign rule is frozen before v0.3 outcomes.

## 27. Historical-edge promotion criteria

At primary 0.50-XAU cost:

1. combined development expectancy >0;
2. DEV-A expectancy >0;
3. DEV-B expectancy >0;
4. validation expectancy >0;
5. holdout expectancy >0;
6. validation PF >=1.10;
7. holdout PF >=1.10;
8. validation bootstrap expectancy lower bound >0;
9. holdout bootstrap expectancy lower bound >0;
10. minimum evidence counts satisfied;
11. no causal/provenance defect;
12. no optimistic same-bar dependency.

MDD/streak evidence is mandatory but has no newly invented hard cutoff.

## 28. Execution sequence

1. freeze v0.3 and EXP-019 before outcomes;
2. verify expanded 2022-12/2023 provenance;
3. implement/unit-test;
4. run combined development only;
5. report combined + DEV-A + DEV-B;
6. checkpoint development;
7. proceed to validation only if the frozen development count/expectancy/subperiod-sign gates pass;
8. checkpoint validation;
9. proceed to fresh holdout only if still eligible.

No post-outcome v0.3 retuning.

Any change requires v0.4/new experiment.

## 29. Relationship to system objective

v0.3 tests whether the Video-2-style location plus causal MSS can become an economically usable candidate source once the stop and target are aligned with a target-first Gold objective.

Even if validated, the USD150-200 strong-day objective remains a later portfolio/ranker/risk-state-machine problem. EXP-015 remains paused until at least one engine validates.
