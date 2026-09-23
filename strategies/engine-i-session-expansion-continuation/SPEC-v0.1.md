# Engine I — Session Expansion / Continuation v0.1

**Status:** FROZEN PROSPECTIVELY — 2026-09-23  
**Engine ID:** `engine-i-session-expansion-continuation`  
**Version:** `0.1`  
**Experiment:** `EXP-020 — Engine I Session Expansion / Continuation v0.1`  
**Outcome status at freeze:** ZERO ENGINE-I OUTCOMES CALCULATED

## 1. Identity and causal thesis

Engine I is a genuinely different strategy family from Engines G/H.

Frozen causal thesis:

```text
established intraday direction
    ->
Asian/session boundary cleared in the same direction
    ->
strong completed 5m expansion
    ->
controlled 25%-60% pullback that holds the cleared boundary
    ->
1m continuation break
    ->
next-active-M1-open entry
    ->
structural pullback stop
    ->
fixed T40 execution target with T30/T50 diagnostics
```

Engine I is a **continuation** engine. It does not require:

- a liquidity raid followed by rejection;
- reversal MSS;
- pre-existing FVG location;
- displacement-created entry FVG;
- retracement into an FVG;
- opposing-range target;
- a separate 2R admission gate.

The purpose is to test a simpler, higher-frequency continuation hypothesis rather than continue tuning the G/H reversal family.

## 2. Market, source and exact price representation

Initial market: `XAUUSD`.

Primary source is the same immutable Dukascopy-derived BID M1 research transport already audited in EXP-016 through EXP-019:

- external transport repository: `kevingtlin/Market-Data-Lab`;
- pinned external commit: `922f83a60cc574e7395fb27397077288055a1ef6`;
- root tree: `6596cd229c736f96bab7d1496656397b31326ca6`;
- XAUUSD BID M1 subtree: `86dd3acd141ffe4b5eb8ad86a04ca42398d0b558`.

The repository is research-data transport only and is not project context.

Source grid:

`tau = 0.001 XAU`.

All structural prices use exact integer ticks:

`price_tick = exact_decimal(source_price) * 1000`.

Binary floating-point equality must not determine structural conditions.

At the current research convention of XAUUSD 0.10 lot ~= 10 oz:

- 1 tick = 0.001 XAU ~= USD 0.01;
- 3000 ticks = 3.000 XAU ~= USD 30 gross;
- 4000 ticks = 4.000 XAU ~= USD 40 gross;
- 5000 ticks = 5.000 XAU ~= USD 50 gross.

Broker contract details remain a later execution-validation requirement.

## 3. Source validity and market-active bars

Use the already-frozen source rules:

- timestamps are exact whole-minute UTC;
- no duplicate timestamps;
- required complete-month files may contain no missing chronological minutes;
- valid positive OHLC geometry;
- exact 0.001-XAU source grid;
- carry-forward M1 = O=H=L=C equal to prior valid chronological close;
- market-active M1 = valid non-carry-forward minute;
- carry-forward M1 does not increment active-M1 ordinal;
- UTC-aligned 5m/15m bars require all chronological constituent M1 rows;
- a derived 5m/15m bar is market-active if at least one constituent M1 is active;
- all-carry-forward derived bars do not increment their active ordinals.

No missing/invalid row may be silently skipped.

## 4. Daily Asian reference range

For each eligible UTC weekday, define the Asian reference interval:

`00:00:00 through 05:59:59 UTC`.

The interval is available only if all 360 chronological M1 rows are present and valid.

Freeze:

- `ASIA_HIGH = max(high_tick)`;
- `ASIA_LOW = min(low_tick)`;
- require `ASIA_HIGH > ASIA_LOW`.

Midpoint comparisons use exact integer arithmetic:

`2 * price_tick` compared with `ASIA_HIGH + ASIA_LOW`.

No later bar may change the day's frozen Asian range.

## 5. Established intraday directional context

For every candidate 5m expansion bar, use only completed market-active UTC-aligned 15m bars whose close time is strictly before the candidate 5m bar opens.

Let:

- `C0` = close of the latest such active 15m bar;
- `C2` = close two active-15m ordinals earlier.

Require at least three eligible active 15m bars.

Long context:

1. `C0 > C2`;
2. `2*C0 > ASIA_HIGH + ASIA_LOW`.

Short context:

1. `C0 < C2`;
2. `2*C0 < ASIA_HIGH + ASIA_LOW`.

This is the complete v0.1 directional-context rule. No EMA, optimized lookback grid, or higher-timeframe discretionary label is used.

## 6. Session-expansion trigger

Candidate expansion bars are completed market-active UTC-aligned 5m bars with completion time:

`06:00 <= completion < 17:00 UTC`.

At most the **first qualifying expansion per direction per UTC day** is allowed. Once a long or short side has produced its first qualifying expansion event, that side is consumed for the day even if its later setup invalidates. This prevents repeated same-side re-entry mining.

For the completed 5m bar define:

- `R = high - low`;
- `BODY = abs(close-open)`.

Require `R > 0`.

### Prior-range expansion baseline

Use the ranges of the previous 12 completed market-active 5m bars, excluding the candidate bar.

Sort those 12 integer ranges ascending. Let `r6` and `r7` be the 6th and 7th values under one-based indexing.

Require:

`2*R >= r6 + r7`.

This is an exact median-of-12 comparison without floating-point rounding.

### Long expansion

All must hold:

1. long directional context from Section 5;
2. `high > ASIA_HIGH`;
3. `close > ASIA_HIGH`;
4. `5*BODY >= 3*R` (body >=60% of range);
5. `4*(high-close) <= R` (close in upper 25% of the bar).

### Short expansion

All must hold:

1. short directional context from Section 5;
2. `low < ASIA_LOW`;
3. `close < ASIA_LOW`;
4. `5*BODY >= 3*R`;
5. `4*(close-low) <= R` (close in lower 25% of the bar).

The expansion is a breakout/acceptance event, not a sweep-and-rejection event.

## 7. Controlled pullback

After the expansion bar closes, inspect market-active M1 bars only.

Maximum setup life:

- 20 active M1 bars after expansion; or
- 18:00 UTC,
- whichever occurs first.

No entry is allowed on the expansion bar itself.

### Long pullback

Let `EH = expansion_high` and `ER = expansion_range`.

For each post-expansion active M1 bar define depth:

`DEPTH = EH - bar_low`.

The pullback becomes **armed** on the first bar satisfying:

`4*DEPTH >= ER`

which is a retracement of at least 25% of the expansion range.

The setup is invalidated before confirmation if either occurs:

1. `5*DEPTH > 3*ER` (retracement deeper than 60%);
2. `bar_close <= ASIA_HIGH` (completed close fails to hold above the cleared session boundary).

### Short pullback

Let `EL = expansion_low` and `ER = expansion_range`.

`DEPTH = bar_high - EL`.

Arm when:

`4*DEPTH >= ER`.

Invalidate if either:

1. `5*DEPTH > 3*ER`;
2. `bar_close >= ASIA_LOW`.

### Conservative ordering

If a bar both reaches the 25% arm threshold and violates the 60% threshold, invalidation wins.

A bar that first arms the pullback cannot also serve as the continuation-confirmation bar. Confirmation search begins on the next active M1 bar.

## 8. Pullback structural extreme

From the first active M1 bar after the expansion close through the eventual confirmation bar, freeze:

Long:

`PULLBACK_LOW = minimum low_tick`.

Short:

`PULLBACK_HIGH = maximum high_tick`.

The value updates causally while the setup is pending and is frozen when continuation confirmation completes.

## 9. Continuation confirmation

After the pullback is armed, starting with the next active M1 bar, search until the 20-active-M1/18:00 setup deadline.

For each candidate confirmation bar, compare only with the previous three completed market-active M1 bars.

Long confirmation requires:

1. `close > open`;
2. `close > max(high of previous 3 active M1 bars)`;
3. the controlled-pullback invalidation rules in Section 7 have not fired.

Short confirmation requires:

1. `close < open`;
2. `close < min(low of previous 3 active M1 bars)`;
3. no controlled-pullback invalidation.

Use the first qualifying confirmation.

This is a continuation break after a pullback, not a reversal MSS.

## 10. Entry

Entry is the exact open tick of the next market-active M1 bar after confirmation.

The entry bar must open before 18:00 UTC.

If multiple Engine-I setups request the same next-active-M1 open while flat, priority is:

1. earlier expansion completion timestamp;
2. lower setup ID.

Test in that order. The first setup passing the frozen entry/stop-risk checks opens the trade. Remaining same-open setups become `suppressed_one_open`.

If an earlier setup fails admission, the next setup may be tested at that same open.

## 11. Structural pullback stop

Long:

`STOP = PULLBACK_LOW - 1 tick`.

Require `STOP < entry`.

Short:

`STOP = PULLBACK_HIGH + 1 tick`.

Require `entry < STOP`.

If geometry is invalid:

`invalid_entry_stop_geometry`.

Gross structural stop distance:

`abs(entry-STOP)`.

Gross structural-risk admission at the XAU 0.10-lot research convention:

`stop_distance_ticks <= 4000`

equivalent to gross stop risk <= approximately USD 40.

No stop compression is permitted.

No fallback to Asian boundary, expansion-bar extreme, fixed-dollar stop, FVG edge, or sweep extreme is permitted.

There is no additional v0.1 2R gate. Because the actual target is 4000 ticks and admitted stop distance is at most 4000 ticks, primary gross reward/risk is >=1 by construction.

## 12. Frozen target ladder

Primary actual execution target:

### T40

Long:

`TARGET40 = entry + 4000 ticks`.

Short:

`TARGET40 = entry - 4000 ticks`.

Actual strategy exits 100% at T40 if reached before stop/horizon.

Predeclared counterfactual target-first diagnostics from the same entry, same structural stop and same horizon:

- T30 = 3000 ticks / 3.000 XAU;
- T40 = 4000 ticks / 4.000 XAU;
- T50 = 5000 ticks / 5.000 XAU;
- T70 = 7000 ticks / 7.000 XAU;
- T100 = 10000 ticks / 10.000 XAU.

T30/T50 may not replace T40 inside v0.1 because one looks better after outcomes.

No partials or runner are part of v0.1.

## 13. Same-bar handling

Entry occurs at a known next-active-M1 open; the full bar high/low is post-entry information.

On the entry bar and every later bar:

- if stop and actual T40 both touch, stop wins;
- if only stop touches, stop;
- if only T40 touches, target.

For every counterfactual target rung, if the stop and that rung touch in the same bar:

`stop_before_target`.

No lower-timeframe interpolation may be used to rescue an ambiguous same-bar winner.

## 14. Exit horizon

Actual v0.1 exits 100% at the earliest of:

1. T40;
2. structural stop;
3. close of the 120th market-active M1 bar counting entry bar as bar 1;
4. 20:00 UTC on entry date;
5. final available source bar.

No overnight carry.

Timeout/session-close exit price is the close of the final permitted M1 bar.

## 15. One-open rule

Maximum one economically accepted Engine-I XAUUSD trade open at a time.

A new qualifying Engine-I setup while an Engine-I trade is open:

`suppressed_one_open`.

When a trade opens, every other pending Engine-I setup is immediately terminated as `suppressed_one_open`.

No queueing behind an open trade.

The daily first-expansion-per-side consumption rule remains independent of this one-open rule.

## 16. Transaction costs

Use the unchanged BID price path plus explicit round-trip cost stress:

- 0.00 XAU = 0 ticks = USD 0;
- 0.25 XAU = 250 ticks = USD 2.50;
- **0.50 XAU = 500 ticks = USD 5 primary cost per filled trade**.

Cost is deducted exactly once per filled trade, including target, stop and timeout exits.

Primary historical economics use the 0.50-XAU / USD5 round-trip stress from the first development run.

## 17. Deterministic reason codes

Daily/reference:

- `asia_interval_incomplete`
- `asia_zero_width`
- `context_15m_unavailable`
- `direction_context_mismatch`

Expansion:

- `outside_expansion_window`
- `prior_12_5m_unavailable`
- `range_below_prior_median`
- `body_below_60pct`
- `weak_close_location`
- `boundary_not_cleared`
- `side_already_consumed_today`
- `suppressed_one_open`

Pullback/confirmation:

- `pullback_timeout_20`
- `pullback_not_armed_25`
- `pullback_deeper_than_60`
- `boundary_hold_failed`
- `confirmation_timeout_20`
- `entry_window_closed_1800`
- `invalid_entry_stop_geometry`
- `structural_risk_above_40`

Filled exits:

- `exit_t40`
- `exit_stop`
- `exit_stop_entry_bar`
- `exit_timeout_120`
- `exit_session_2000`
- `exit_data_end`

## 18. Frequency design target

Engine I v0.1 is intentionally designed to avoid the sparse G/H confirmation stacks.

Structural opportunity ceiling:

- up to one long expansion event per eligible UTC weekday;
- up to one short expansion event per eligible UTC weekday;
- no FVG-location requirement;
- no reversal MSS;
- no displacement-created entry FVG;
- no opposing-range target-room gate;
- no separate 2R gate.

Across the 26-month development period, this creates a broad enough pre-filter opportunity pool that **>=100 accepted development trades is a realistic design target**, while still preventing repeated same-side same-day mining.

This is a design expectation, not an observed result. If accepted development trades are below 100, the threshold will not be relaxed.

## 19. Frozen data split

Warm-up:

`2022-12-01 through 2022-12-31 UTC`.

Combined development:

`2023-01-01 through 2025-02-28 UTC`.

Predeclared development stability subperiods:

- DEV-A: `2023-01-01 through 2023-12-31`;
- DEV-B: `2024-01-01 through 2025-02-28`.

Validation:

`2025-03-01 through 2025-08-31`.

Fresh holdout:

`2025-09-01 through 2026-02-28`.

Quarantined prior-research period:

`2026-03-01 through 2026-08-20`.

The quarantined period is not part of primary Engine-I selection.

## 20. Contamination and provenance classification

### Development pool

Calendar 2023 and Jan-2024 through Feb-2025 are **not pristine at the project level**:

- 2023 was later used as H-v0.3 development;
- Jan-2024 through Feb-2025 was used by G/H development.

That is acceptable only because these dates are explicitly the project's reusable **development** pool, not validation or holdout.

At Engine-I freeze:

- no Engine-I outcomes have been calculated on any period;
- Engine-I rules were frozen before inspecting Engine-I results;
- no Engine-I parameter grid has been run.

This means development is suitable for hypothesis screening, but repeated project-level development use must be acknowledged as research-selection exposure.

### Validation and fresh holdout

The repository records that G/H were stopped before their validation/holdout outcome runs.

Therefore:

- Mar-Aug 2025 remains untouched by G/H strategy outcomes;
- Sep 2025-Feb 2026 remains untouched by G/H strategy outcomes.

These periods are reserved for Engine I only if frozen development gates pass.

## 21. Frozen source manifest

The loaded monthly files must exactly match the already-audited immutable BID manifest.

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

Before any outcome computation, every loaded file must match:

- pinned repository commit;
- exact path;
- Git blob SHA;
- byte size;
- expected full-calendar row count;
- exact month-start through month-end one-minute chronology.

Development execution must not download validation or holdout files.

## 22. Required development reporting

Report combined development and separately DEV-A / DEV-B:

- data-quality verification;
- eligible weekdays;
- valid Asian ranges;
- long/short directional-context counts;
- qualifying expansion counts;
- pullback-armed counts;
- pullback invalidation counts by reason;
- continuation-confirmation counts;
- accepted filled trades;
- deterministic rejection/cancellation counts;
- T40 target / stop / timeout rates;
- T30/T40/T50/T70/T100 target-first rates;
- gross expectancy;
- net expectancy at 0/0.25/0.50 XAU costs;
- primary-cost profit factor;
- total primary-cost net P&L;
- mean/median eligible-weekday P&L including zero-trade weekdays;
- losing weekday percentage;
- <=USD50 and >=USD100/150/200 weekday percentages;
- maximum drawdown from USD500 reference;
- maximum consecutive losing trades and loss of worst run;
- maximum consecutive losing weekdays;
- maximum consecutive <=USD50 weekdays;
- structural stop distance/risk distribution;
- expansion-range/body distributions;
- pullback-depth distribution;
- time expansion->pullback;
- time pullback->confirmation;
- actual MFE/MAE;
- counterfactual potential MFE/MAE;
- long/short contribution;
- bootstrap uncertainty.

## 23. Bootstrap

Combined development:

- moving blocks of 5 consecutive eligible weekdays;
- 10,000 replications;
- seed `20020`;
- percentile 95% interval.

Primary statistics:

- primary-cost net expectancy/trade;
- primary-cost mean net USD per eligible weekday.

Bootstrap is required reporting in development but its lower bound is not a hard development gate; subperiod sign, PF and drawdown/recovery rules already provide the prospectively frozen screening gate.

Validation/holdout bootstrap lower-bound requirements are hard promotion gates.

## 24. Frozen development gate

Proceed to validation **only if all conditions hold**:

1. accepted filled development trades >=100;
2. combined primary-cost expectancy/trade >0;
3. DEV-A primary-cost expectancy/trade >0;
4. DEV-B primary-cost expectancy/trade >0;
5. combined primary-cost profit factor >=1.10;
6. combined maximum drawdown <=USD200 on the standalone USD500 reference curve;
7. combined primary-cost net profit / maximum drawdown >=1.00 when maximum drawdown >0;
8. no causal leakage;
9. no optimistic same-bar dependency;
10. no source/provenance violation.

If accepted trades are below 100, disposition is `INSUFFICIENT_EVIDENCE` and the threshold is not lowered.

Any failed mandatory development gate stops Engine I v0.1 before validation.

## 25. Frozen validation and holdout promotion gates

Validation may be run only after a passing development checkpoint.

Validation must satisfy:

1. accepted trades >=50;
2. primary-cost expectancy >0;
3. primary-cost PF >=1.10;
4. 95% moving-block-bootstrap expectancy lower bound >0;
5. maximum drawdown <=USD200;
6. no causal/provenance/same-bar defect.

Fresh holdout may be run only after a passing validation checkpoint.

Holdout must satisfy the same six conditions.

Final same-feed historical promotion additionally requires:

- no expectancy sign reversal across development, DEV-A, DEV-B, validation and holdout;
- unchanged v0.1 rules throughout;
- no validation/holdout parameter selection;
- validation and holdout remain minimum-count sufficient.

Passing these gates promotes Engine I only to a historically validated candidate source for later independent-feed / paper validation. It does not authorize live trading.

## 26. Fast-turnover / anti-mining rule

Engine I v0.1 has **one center configuration**.

No predeclared parameter grid exists.

Do not run alternate:

- directional lookbacks;
- Asian windows;
- expansion body thresholds;
- expansion median multipliers;
- pullback percentages;
- confirmation lookbacks;
- session cutoffs;
- target distances;
- stop caps

to rescue a failed development result.

If v0.1 fails development decisively, preserve validation/holdout and move to the next genuinely different engine family. Creating Engine I v0.2 is not the default response.

## 27. Implementation sequence

1. freeze this spec and EXP-020 in GitHub before outcomes;
2. implement exact-arithmetic engine and unit/causality tests;
3. build a development-only runner/workflow that downloads only Dec-2022 through Feb-2025;
4. re-verify every loaded file against the frozen manifest before strategy calculations;
5. run combined development only;
6. checkpoint development result;
7. run validation only if every frozen development gate passes;
8. checkpoint validation;
9. run fresh holdout only if every frozen validation gate passes;
10. checkpoint holdout;
11. independent-feed validation remains separate.

No Engine-I outcome may be calculated before the pre-outcome implementation/provenance checkpoint is durably recorded.

## 28. Candidate-contract mapping

Every accepted Engine-I setup should expose at minimum:

- engine ID/version;
- symbol/source;
- direction;
- expansion timestamp;
- Asian high/low;
- directional-context closes;
- expansion OHLC/range/body;
- pullback arm timestamp and depth;
- confirmation timestamp;
- entry timestamp/rule/price;
- structural pullback stop and native stop distance;
- T30/T40/T50/T70/T100 prices;
- session;
- feature snapshot available at signal time;
- data provenance/version;
- deterministic rejection reason where rejected.

This maps to `docs/STRATEGY-ENGINE-CONTRACT.md`.

## 29. Relationship to the system objective

Engine I is one candidate engine, not the complete USD150-200 strong-day system.

The desired architecture remains:

```text
several independently profitable validated engines
    ->
standardized candidates
    ->
EXP-015 target-first probability / EV selector
    ->
P&L-equivalent sizing
    ->
risk / margin / daily-budget / correlation gates
    ->
cross-market ranking
```

EXP-015 remains paused until at least one engine validates.
