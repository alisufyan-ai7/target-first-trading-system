# Engine J — Volatility Compression Breakout v0.1

**Status:** FROZEN PROSPECTIVELY — 2026-09-23  
**Engine ID:** `engine-j-volatility-compression-breakout`  
**Version:** `0.1`  
**Experiment:** `EXP-021 — Engine J Volatility Compression Breakout v0.1`  
**Outcome status at freeze:** ZERO ENGINE-J OUTCOMES CALCULATED

## 1. Identity and causal thesis

Frozen thesis:

```text
same-day intraday volatility baseline
    ->
30m realized-range compression into a compact 5m box
    ->
strong 5m breakout expansion from inside the box
    ->
next-active-M1-open momentum entry
    ->
breakout-bar structural stop
    ->
fixed T40 execution target with target ladder diagnostics
```

Engine J is a **volatility-regime breakout** engine.

It does not require:

- Asian/session liquidity boundaries;
- pre-established long/short direction;
- a sweep/rejection;
- reversal MSS;
- FVG location;
- pullback/retest;
- continuation confirmation after pullback;
- opposing-range target geometry.

This is materially different from Engines G/H and Engine I.

## 2. Market and price representation

Initial market: `XAUUSD`.

Use the same immutable Dukascopy-derived BID M1 source snapshot already frozen for EXP-020:

- transport repository: `kevingtlin/Market-Data-Lab`;
- pinned external commit: `922f83a60cc574e7395fb27397077288055a1ef6`;
- BID M1 subtree: `86dd3acd141ffe4b5eb8ad86a04ca42398d0b558`.

The external repository is research-data transport only, not project context.

Exact source grid:

`tau = 0.001 XAU`.

All prices are integer ticks:

`price_tick = exact_decimal(source_price) * 1000`.

No binary floating-point equality may determine structural logic.

At the frozen XAUUSD 0.10-lot research convention:

- 1 tick ~= USD0.01;
- 3000 ticks ~= USD30 gross;
- 4000 ticks ~= USD40 gross;
- 5000 ticks ~= USD50 gross.

## 3. Source validity

Use the exact source rules already audited in EXP-020:

- whole-minute UTC timestamps;
- no duplicate timestamps;
- no missing chronological minute in required complete-month files;
- valid positive OHLC geometry;
- exact 0.001-XAU price grid;
- carry-forward M1 = O=H=L=C equal to prior chronological close;
- carry-forward bars do not increment active ordinals;
- UTC-aligned 5m bars require all five chronological M1 rows;
- a 5m bar is market-active if at least one constituent M1 is active;
- all-carry-forward 5m bars do not increment active-5m ordinal.

No invalid/missing row may be silently skipped.

## 4. Candidate time window

Candidate breakout bars are completed market-active UTC-aligned 5m bars on eligible UTC weekdays with:

`06:00 <= completion < 18:00 UTC`.

Entry must occur at the next market-active M1 open before 18:00 UTC.

No overnight setup carry.

## 5. Same-day baseline and compression windows

For a candidate breakout bar `B`, use only completed market-active 5m bars whose close is <= the candidate bar's open.

Let the immediately preceding 30 active 5m bars be:

- `BASE[1..24]`: the older 24-bar baseline window;
- `COMP[1..6]`: the immediately preceding six active 5m bars.

Require all 30 bars to have `startTs >= 00:00 UTC` on the candidate breakout date.

If fewer than 30 eligible same-day active 5m bars exist:

`same_day_30_active5_unavailable`.

The candidate breakout bar is excluded from both windows.

## 6. Baseline median range

For each `BASE` bar define integer range:

`r_i = high_i - low_i`.

Sort the 24 ranges ascending.

Let `r12` and `r13` be the 12th and 13th values under one-based indexing.

Freeze:

`MEDIAN_NUM = r12 + r13`.

This equals two times the exact median and avoids floating-point rounding.

Require:

`MEDIAN_NUM > 0`.

Otherwise:

`baseline_zero_range`.

## 7. Compression rule

For the six `COMP` bars define:

- `S = sum(high-low)`;
- `BOX_HIGH = max(high)`;
- `BOX_LOW = min(low)`;
- `BOX_WIDTH = BOX_HIGH - BOX_LOW`.

Require `BOX_WIDTH > 0`.

### 7.1 Realized-range contraction

Require:

`5*S <= 12*MEDIAN_NUM`.

Because `MEDIAN_NUM = 2 * median`, this is exactly equivalent to:

`average COMP range <= 0.80 * BASE median range`.

### 7.2 Compact price containment

Require:

`2*BOX_WIDTH <= 3*MEDIAN_NUM`.

This is exactly equivalent to:

`BOX_WIDTH <= 3.0 * BASE median range`.

Both conditions are required.

No ATR, standard deviation, Bollinger Band, percentile grid, or optimized compression threshold is used in v0.1.

## 8. Breakout expansion bar

Let candidate bar range:

`R = high - low`.

Let:

`BODY = abs(close-open)`.

Require `R > 0`.

### 8.1 Long breakout

All must hold:

1. `open <= BOX_HIGH`;
2. `close > BOX_HIGH`;
3. `8*R >= 5*MEDIAN_NUM` (range >=1.25x baseline median);
4. `5*BODY >= 3*R` (body >=60% of range);
5. `4*(high-close) <= R` (close in upper 25%).

### 8.2 Short breakout

All must hold:

1. `open >= BOX_LOW`;
2. `close < BOX_LOW`;
3. `8*R >= 5*MEDIAN_NUM`;
4. `5*BODY >= 3*R`;
5. `4*(close-low) <= R`.

A bar that closes beyond both sides is impossible under valid OHLC when `BOX_HIGH > BOX_LOW`; no dual-direction fallback exists.

## 9. Event consumption and frequency discipline

At most the **first qualifying long breakout** and the **first qualifying short breakout** per UTC day are eligible.

A side is consumed when its first bar satisfies the full compression + breakout rules, even if entry later fails the risk/geometry gate.

Later same-side qualifying bars receive:

`side_already_consumed_today`.

This prevents repeated same-day same-direction mining while allowing up to two structurally distinct opportunities per eligible weekday.

Across the 26-month development period this produces a broad theoretical opportunity ceiling above the frozen >=100 accepted-trade requirement.

If accepted development trades are below 100, the gate is not relaxed.

## 10. Entry

Entry is the exact open tick of the next market-active M1 bar after the qualifying breakout bar completes.

Require entry open time <18:00 UTC.

If the next active M1 open is at/after 18:00:

`entry_window_closed_1800`.

If multiple setups request the same open while flat, priority:

1. earlier breakout completion;
2. lower setup ID.

The first setup passing admission opens the trade.

Remaining same-open setups become:

`suppressed_one_open`.

## 11. Structural stop

Long:

`STOP = breakout_low - 1 tick`.

Require `STOP < entry`.

Short:

`STOP = breakout_high + 1 tick`.

Require `entry < STOP`.

Invalid geometry:

`invalid_entry_stop_geometry`.

Structural-risk admission:

`abs(entry-STOP) <= 4000 ticks`.

If above:

`structural_risk_above_40`.

No stop compression is permitted.

No box-midpoint, fixed-dollar, Asian-boundary, FVG, swing, or post-entry adaptive stop may replace the frozen breakout-bar structural stop.

## 12. Frozen target ladder

Actual v0.1 execution target:

### T40

Long:

`TARGET40 = entry + 4000 ticks`.

Short:

`TARGET40 = entry - 4000 ticks`.

Exit 100% at T40 if reached before stop/horizon.

Predeclared counterfactual labels from the same entry/stop/horizon:

- T30 = 3000 ticks;
- T40 = 4000 ticks;
- T50 = 5000 ticks;
- T70 = 7000 ticks;
- T100 = 10000 ticks.

No target rung may replace T40 inside v0.1 after observing development.

No partials or runner.

## 13. Same-bar handling

Entry occurs at a known next-active-M1 open.

On entry bar and every later bar:

- if stop and T40 touch, stop wins;
- if only stop touches, stop;
- if only T40 touches, target.

For every diagnostic target rung, same-bar stop + target means:

`stop_before_target`.

No lower-timeframe interpolation or optimistic ordering.

## 14. Exit horizon

Actual trade exits at earliest of:

1. T40;
2. structural stop;
3. close of the 120th market-active M1 bar counting entry bar as 1;
4. 20:00 UTC on entry date;
5. source-data end.

No overnight carry.

Timeout/session-close exit uses final permitted M1 close.

## 15. One-open rule

Maximum one economically accepted Engine-J XAUUSD trade open at a time.

A new qualifying Engine-J setup while an Engine-J trade is open:

`suppressed_one_open`.

When a trade opens, any other pending same-open setup is suppressed.

No queueing.

## 16. Transaction costs

Use unchanged BID path plus explicit round-trip stress:

- 0.00 XAU = USD0;
- 0.25 XAU = USD2.50;
- **0.50 XAU = USD5 primary cost per filled trade**.

Cost is deducted exactly once per filled trade.

Primary development economics use USD5 from the first run.

## 17. Deterministic reason codes

Window/data:

- `outside_breakout_window`
- `same_day_30_active5_unavailable`
- `baseline_zero_range`

Compression:

- `compression_average_failed`
- `compression_box_too_wide`
- `compression_zero_width`

Breakout:

- `breakout_open_already_outside_box`
- `breakout_close_not_beyond_box`
- `breakout_range_below_1_25_median`
- `body_below_60pct`
- `weak_close_location`
- `side_already_consumed_today`

Entry/admission:

- `entry_window_closed_1800`
- `invalid_entry_stop_geometry`
- `structural_risk_above_40`
- `suppressed_one_open`

Exit:

- `exit_t40`
- `exit_stop`
- `exit_stop_entry_bar`
- `exit_timeout_120`
- `exit_session_2000`
- `exit_data_end`

## 18. Frozen data split

Warm-up:

`2022-12-01 through 2022-12-31 UTC`.

Combined development:

`2023-01-01 through 2025-02-28 UTC`.

Development stability subperiods:

- DEV-A: calendar 2023;
- DEV-B: Jan-2024 through Feb-2025.

Validation:

`2025-03-01 through 2025-08-31 UTC`.

Fresh holdout:

`2025-09-01 through 2026-02-28 UTC`.

Quarantined prior-research period:

`2026-03-01 through 2026-08-20 UTC`.

## 19. Contamination/provenance classification

The development pool is not pristine at the project level:

- G/H/I outcomes have been inspected on portions or all of Jan-2023 through Feb-2025.

It remains the designated reusable project development pool.

At Engine-J freeze:

- no Engine-J outcome has been calculated;
- no Engine-J parameter grid has been run;
- the complete center rule is frozen before Engine-J development.

Validation Mar-Aug 2025 and fresh holdout Sep-2025 through Feb-2026 remain untouched by G/H/I validation/holdout outcomes and stay sealed unless prospective gates permit opening them.

Use the exact monthly blob/byte manifest already frozen in Engine-I v0.1. Before any Engine-J outcome, the development-only harness must re-verify the same 27 Dec-2022 through Feb-2025 files.

Development execution may not download validation or holdout files.

## 20. Required development reporting

Report combined development and DEV-A / DEV-B:

- source/provenance verification;
- eligible weekdays;
- candidates with 30-bar same-day history;
- compression-average passes;
- compact-box passes;
- long/short qualifying breakouts;
- accepted trades;
- rejection counts;
- T40 target/stop/timeout rates;
- T30/T40/T50/T70/T100 target-first diagnostics;
- gross and 0/0.25/0.50-XAU expectancy;
- primary-cost PF;
- total primary-cost P&L;
- eligible-weekday P&L distribution;
- max drawdown;
- recovery factor;
- losing-trade/weekday streaks;
- breakout-bar range/body distributions;
- compression baseline median / sum / box-width distributions;
- stop-distance/risk distribution;
- actual and potential MFE/MAE;
- long/short contribution;
- bootstrap uncertainty.

## 21. Bootstrap

Combined development:

- moving blocks of 5 consecutive eligible weekdays;
- 10,000 replications;
- seed `21021`;
- percentile 95% interval.

Development lower-bound positivity is reported but is not a hard gate.

Validation/holdout lower-bound positivity is a hard gate.

## 22. Frozen development gate

Proceed to validation only if all hold:

1. accepted development trades >=100;
2. combined primary-cost expectancy >0;
3. DEV-A primary-cost expectancy >0;
4. DEV-B primary-cost expectancy >0;
5. combined primary-cost PF >=1.10;
6. max drawdown <=USD200 on standalone USD500 reference curve;
7. net-profit / max-drawdown recovery factor >=1.00 when MDD>0;
8. no causal leakage;
9. no optimistic same-bar dependency;
10. no provenance violation.

Below 100 accepted trades = `INSUFFICIENT_EVIDENCE`.

Any failed mandatory development gate stops v0.1 before validation.

## 23. Frozen validation/holdout gates

Validation may run only after development passes every gate.

Validation must have:

- accepted trades >=50;
- primary-cost expectancy >0;
- primary-cost PF >=1.10;
- 95% bootstrap expectancy lower bound >0;
- max drawdown <=USD200;
- no causal/provenance/same-bar defect.

Fresh holdout may run only after validation passes and must satisfy the same conditions.

Final same-feed historical promotion additionally requires no expectancy sign reversal across development, DEV-A, DEV-B, validation and holdout.

## 24. Anti-mining / fast-turnover rule

Engine J v0.1 has **one center configuration**.

No parameter grid is authorized.

Do not run alternate:

- baseline lengths;
- compression lengths;
- contraction ratios;
- box-width multipliers;
- breakout expansion multipliers;
- body/close thresholds;
- session windows;
- stop definitions;
- target distances

to rescue a failed development result.

If v0.1 fails decisively, preserve validation/holdout and move to another genuinely different causal family.

## 25. Implementation sequence

1. freeze this spec and EXP-021 before outcomes;
2. user reviews frozen mechanics;
3. implement exact-arithmetic reference engine;
4. add unit/causality tests;
5. add development-only harness/workflow;
6. verify exact frozen 27-file manifest with zero Engine-J outcomes;
7. checkpoint preflight;
8. only then run Jan-2023 through Feb-2025 combined development;
9. stop before validation on any failed gate.

## 26. Relationship to the system objective

Engine J is a candidate source, not the complete system.

The target architecture remains:

```text
multiple independently profitable validated engines
    ->
common candidate contract
    ->
EXP-015 target-first ranker
    ->
P&L-equivalent sizing
    ->
risk / daily-budget / correlation gates
    ->
cross-market selection
```

EXP-015 remains paused until at least one reproducible engine validates.
