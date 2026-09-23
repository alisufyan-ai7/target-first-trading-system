# EXP-020 — Engine I Session Expansion / Continuation v0.1

**Status:** FROZEN / NOT YET RUN  
**Frozen:** 2026-09-23  
**Engine:** Engine I — Session Expansion / Continuation v0.1  
**Spec:** `strategies/engine-i-session-expansion-continuation/SPEC-v0.1.md`  
**Outcome status at freeze:** ZERO ENGINE-I OUTCOMES CALCULATED

## Why EXP-020 exists

EXP-016 Engine G and EXP-017 through EXP-019 Engine H tested reversal-oriented liquidity/location theses and did not produce a promotable development result.

Engine I intentionally changes causal family:

```text
established intraday direction
    ->
Asian/session boundary cleared
    ->
strong 5m expansion
    ->
controlled pullback
    ->
1m continuation confirmation
    ->
next-open entry
    ->
structural pullback stop
    ->
T40 execution target
```

The goal is fast hypothesis turnover with enough natural opportunity frequency to test >=100 accepted development trades without lowering evidence standards or mining a large parameter grid.

## Frozen v0.1 center rule

- XAUUSD only for first engine proof;
- exact 0.001-XAU integer source ticks;
- daily Asian range = complete 00:00-05:59 UTC interval;
- directional context = latest completed active 15m close vs two active 15m bars earlier, aligned with Asian-range midpoint;
- candidate expansion = first per side/day completed active 5m bar from 06:00 to before 17:00 that closes through the Asian boundary in the context direction;
- expansion bar range >= median prior-12 active 5m ranges;
- body >=60% of range;
- close in directional outer 25% of expansion bar;
- controlled pullback = 25%-60% retracement of expansion range while completed M1 closes continue to hold beyond the cleared Asian boundary;
- pullback/confirmation window = maximum 20 active M1 bars after expansion and before 18:00;
- continuation confirmation = first directional M1 close after the pullback-arm bar that closes beyond the previous three active-M1 highs/lows;
- entry = next active M1 open before 18:00;
- stop = one tick beyond frozen post-expansion pullback extreme through confirmation;
- gross structural risk <=USD40 at the XAU 0.10-lot research convention;
- actual target = fixed T40 / 4.000 XAU;
- counterfactual target-first labels include T30/T40/T50/T70/T100;
- actual horizon = 120 active M1 bars or 20:00 UTC;
- no overnight;
- one open Engine-I trade maximum;
- first qualifying expansion per side/day only;
- conservative stop-first same-bar treatment;
- primary round-trip cost = 0.50 XAU / USD5 per filled trade.

No FVG, reversal MSS, opposing-range target, target-room filter, or separate 2R gate is part of Engine I v0.1.

## Frozen source snapshot

Use the same immutable Dukascopy-derived BID M1 transport already audited in EXP-016 through EXP-019:

- transport repository: `kevingtlin/Market-Data-Lab`;
- pinned commit: `922f83a60cc574e7395fb27397077288055a1ef6`;
- BID M1 subtree: `86dd3acd141ffe4b5eb8ad86a04ca42398d0b558`.

The exact monthly file/blob/byte manifest is frozen in the Engine-I specification and must be re-verified before any outcome calculation.

Development execution must not download validation or holdout files.

## Frozen split

Warm-up:

`2022-12-01 through 2022-12-31`.

Combined development:

`2023-01-01 through 2025-02-28`.

Development stability subperiods:

- DEV-A = calendar 2023;
- DEV-B = Jan-2024 through Feb-2025.

Validation:

`2025-03-01 through 2025-08-31`.

Fresh holdout:

`2025-09-01 through 2026-02-28`.

Quarantined prior-research period:

`2026-03-01 through 2026-08-20`.

## Contamination classification at freeze

Development is not pristine at the project level because G/H results have already been inspected on parts of 2023-Feb-2025. It remains the explicitly reusable project development pool.

This is acceptable for Engine-I hypothesis screening only because:

- zero Engine-I outcomes have been calculated;
- the complete Engine-I rule is frozen before any Engine-I development result;
- no Engine-I parameter search has occurred.

The stronger protection remains validation/holdout:

- G/H validation Mar-Aug 2025 was never inspected;
- G/H fresh holdout Sep 2025-Feb 2026 was never inspected.

These periods remain closed unless Engine-I development/validation gates prospectively permit opening them.

## Why the frequency design should avoid another sparse engine

Unlike H, Engine I does not stack external-FVG location + reversal MSS + displacement + new FVG + midpoint fill + target-room + 2R conditions.

The center rule permits up to:

- one long expansion event per eligible weekday;
- one short expansion event per eligible weekday.

The 26-month development interval therefore has a structurally broad event pool before pullback/confirmation/risk admission.

The required development count remains >=100. If v0.1 produces fewer, the experiment is insufficient and the rule is not loosened post hoc.

## Frozen development gate

Validation is forbidden unless all pass:

1. accepted development trades >=100;
2. combined primary-cost expectancy >0;
3. DEV-A primary-cost expectancy >0;
4. DEV-B primary-cost expectancy >0;
5. combined primary-cost PF >=1.10;
6. combined max drawdown <=USD200 on the standalone USD500 reference curve;
7. combined net-profit / max-drawdown recovery factor >=1.00 when MDD >0;
8. no causal leakage;
9. no optimistic same-bar dependency;
10. no provenance defect.

Below 100 accepted development trades = `INSUFFICIENT_EVIDENCE`.

A failure of any mandatory gate stops v0.1 before validation.

## Frozen validation gate

Only after a passing development checkpoint:

- accepted trades >=50;
- primary-cost expectancy >0;
- primary-cost PF >=1.10;
- 95% moving-block-bootstrap expectancy lower bound >0;
- max drawdown <=USD200;
- no causal/provenance/same-bar defect.

If validation fails, fresh holdout remains untouched.

## Frozen fresh-holdout gate

Only after a passing validation checkpoint:

- accepted trades >=50;
- primary-cost expectancy >0;
- primary-cost PF >=1.10;
- 95% moving-block-bootstrap expectancy lower bound >0;
- max drawdown <=USD200;
- no causal/provenance/same-bar defect.

Final same-feed historical promotion also requires no expectancy sign reversal across development, DEV-A, DEV-B, validation and holdout.

## Bootstrap

Use moving blocks of 5 consecutive eligible weekdays.

- replications: 10,000;
- seed: `20020`;
- interval: percentile 95%.

Development lower-bound positivity is reported but is not a hard gate.

Validation and holdout lower-bound positivity are hard gates.

## Primary cost

Primary historical economics use:

`0.50 XAU round-trip = 500 ticks = USD5 per filled trade`.

The 0.00 and 0.25 XAU cases are diagnostics only.

This cost is included from the first development run.

## No-parameter-mining rule

EXP-020 has one frozen center rule.

Do not rescue a failed result by trying neighboring:

- direction lookbacks;
- session windows;
- expansion thresholds;
- pullback-depth bands;
- confirmation lookbacks;
- stop caps;
- target distances.

No v0.1 sensitivity grid is authorized.

If development fails decisively, preserve validation/holdout and move to the next genuinely different engine family rather than endlessly creating Engine-I variants.

## Required first checkpoint after implementation

Before any development outcome:

1. exact-arithmetic unit tests pass;
2. causal sequencing tests pass;
3. frozen source manifest is re-verified;
4. development-only runner/workflow is confirmed not to download validation/holdout;
5. implementation matches the frozen v0.1 specification;
6. GitHub checkpoint records that zero Engine-I outcomes have yet been calculated.

Only then may combined development Jan-2023 through Feb-2025 run.

## Checkpoint 0 — frozen before outcomes

- Engine-I v0.1 specification frozen: YES;
- EXP-020 frozen: YES;
- source snapshot/manifest frozen: YES;
- split frozen: YES;
- transaction costs frozen: YES;
- development/validation/holdout gates frozen: YES;
- Engine-I outcomes calculated: NO;
- Engine-I development backtest launched: NO.

## Relationship to EXP-015

EXP-015 remains paused.

If Engine I ultimately validates, it becomes a standardized candidate source that can feed the target-first ranker alongside future independently validated engines.

The long-term goal remains several profitable, reproducible strategy engines whose combined opportunity stream can later be ranked and risk-gated toward the USD150-200 strong-day objective under the approximately USD40 normal / USD60 emergency daily loss framework.


## Checkpoint 1 — implementation and preflight verified before outcomes

**Outcome status:** ZERO ENGINE-I OUTCOMES CALCULATED.

Reference implementation:

- `research/code/engine-i-v0.1.js`;
- initial implementation commit: `e4a894b8f4d8c29ccebd209b94e63b77cf2c7295`;
- final pre-outcome reporting/terminal-reason amendment: `060ee9848575516ae06e16c1b17b921b525942f8`.

Execution harnesses:

- preflight verifier: `research/code/run-engine-i-preflight.js`;
- development runner: `research/code/run-engine-i-development.js`;
- preflight workflow: `.github/workflows/exp020-engine-i-preflight.yml`;
- development workflow: `.github/workflows/exp020-engine-i-development.yml`.

The development workflow exists but has **not** been triggered.

### Final preflight

Final successful GitHub Actions run:

- run ID: `35842855789`;
- tested repository SHA: `0fa662744b08c14d7f52709986b5c6dab9ec0e1a`;
- result commit: `61e2e81e95bb01b2ae891b3cb7814cb03efdea60`;
- engine file SHA-256: `2037c20640476b254e3ffb04069f1ab0556e11cd1fb1cf41ffae55d0c4c61ac4`;
- durable result: `research/results/EXP-020-preflight-v0.1.json`.

Preflight verified:

- 27 frozen warm-up/development files only;
- 1,182,240 total M1 rows;
- 59,108,737 total bytes;
- every file matched frozen Git blob SHA and byte size;
- every file matched exact full-month row count;
- every first/last timestamp matched exact calendar-month boundaries;
- one-minute chronology passed;
- exact price-grid/OHLC checks passed;
- validation/holdout filenames were absent from both development runner and workflow;
- validation/holdout data were not loaded;
- strict-before-expansion 15m context path is present;
- conservative same-bar stop-first handling is present;
- first-qualifying-expansion-per-side/day consumption is present.

### Self/causality tests

All 11 frozen tests passed:

1. exact tick parsing;
2. off-grid rejection;
3. 15m context strictly before expansion open;
4. equal-close-time context leakage prevention;
5. exact prior-12 median comparison;
6. expansion shape;
7. 25%-60% pullback arithmetic;
8. strict cleared-boundary hold;
9. previous-three-M1 continuation break;
10. stop-first same-bar handling;
11. 4000-tick structural-risk boundary.

### Pre-outcome implementation clarification

Before any Engine-I outcome, reporting counters were completed for:

- valid Asian weekdays;
- long/short aligned directional-context boundary events;
- explicit `pullback_timeout_20` versus session-close `pullback_not_armed_25`.

This changed no frozen strategy threshold or causal rule.

### Permission to begin next stage

Checkpoint-1 requirements are satisfied.

The **next and only permitted outcome computation** is combined development:

`2023-01-01 through 2025-02-28`

with Dec-2022 warm-up, DEV-A=2023 and DEV-B=Jan-2024 through Feb-2025.

Validation Mar-Aug 2025 and fresh holdout Sep-2025 through Feb-2026 remain uninspected and must not be downloaded or run.

**Development backtest started at this checkpoint: NO.**


## Checkpoint 2 — development failed; validation forbidden

**Development run:** GitHub Actions run `35844194955`  
**Result commit:** `a891dc1aa956151df1b87f6c9e03daae2dabf29b`  
**Result file:** `research/results/EXP-020-development-summary-v0.1.json`  
**Validation/holdout loaded:** NO

### Combined development result

Jan-2023 through Feb-2025:

- accepted filled trades: **197**;
- frozen minimum count: >=100 — **PASS**;
- T40 hit rate: **24.37%**;
- primary-cost expectancy: **-USD5.15/trade** — **FAIL**;
- primary-cost PF: **0.631** — **FAIL**;
- total primary-cost P&L: **-USD1,015.49**;
- max drawdown: **USD1,060.90** — **FAIL** versus <=USD200;
- recovery factor: **-0.957** — **FAIL**;
- bootstrap 95% primary-cost expectancy interval: **[-USD8.38, -USD1.94]**;
- bootstrap 95% mean eligible-weekday P&L interval: **[-USD2.98, -USD0.66]**.

Gross expectancy before transaction cost was already approximately **-USD0.15/trade**, so the development failure is not merely a transaction-cost artifact.

### DEV-A — calendar 2023

- accepted trades: **99**;
- T40 hit rate: **20.20%**;
- primary-cost expectancy: **-USD6.20/trade** — **FAIL**;
- primary-cost PF: **0.550**;
- total net: **-USD614.24**;
- max drawdown: **USD674.77**.

### DEV-B — Jan-2024 through Feb-2025

- accepted trades: **98**;
- T40 hit rate: **28.57%**;
- primary-cost expectancy: **-USD4.09/trade** — **FAIL**;
- primary-cost PF: **0.711**;
- total net: **-USD401.25**;
- max drawdown: **USD458.80**.

DEV-B improved in gross terms to approximately +USD0.91/trade before cost, but still failed decisively at the frozen primary cost and did not provide enough economic headroom for deployment.

### Frozen gate disposition

- accepted >=100: PASS;
- combined expectancy >0: FAIL;
- DEV-A expectancy >0: FAIL;
- DEV-B expectancy >0: FAIL;
- combined PF >=1.10: FAIL;
- max drawdown <=USD200: FAIL;
- recovery factor >=1.0: FAIL;
- causal/provenance defect observed: NO.

**Final EXP-020 development disposition: FAIL.**

Engine I v0.1 is stopped before validation.

Do not:

- run Mar-Aug 2025 validation;
- run Sep-2025 through Feb-2026 fresh holdout;
- switch the actual target from T40 based on the diagnostic ladder;
- create a parameter grid around the same rule;
- loosen the pullback/expansion/context thresholds post hoc to rescue v0.1.

The correct next action is to preserve validation/holdout and move to a genuinely different causal engine family.
