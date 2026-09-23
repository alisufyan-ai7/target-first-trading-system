# EXP-019 — Engine H v0.3 Post-Raid Structural Stop + T40 Target

**Status:** FROZEN / NOT YET RUN  
**Frozen:** 2026-09-23  
**Engine:** Engine H v0.3  
**Spec:** `strategies/engine-h-range-raid-preexisting-fvg-reversal/SPEC-v0.3.md`  
**Outcome status at freeze:** ZERO Engine-H-v0.3 outcomes

## Prospective hypothesis

Keep the H v0.2 location and confirmation:

`range raid into pre-existing external 5m FVG -> 1m MSS -> next-active-M1-open entry`.

Replace the v0.2 economic geometry with:

- post-raid confirmed 1m invalidation swing stop;
- no fallback to sweep-extreme stop;
- fixed actual T40 target (+4.000 XAU);
- T30/T50 predeclared target-ladder diagnostics;
- no opposite-range target gate;
- no 3-XAU room gate;
- no explicit 2R gate;
- gross structural stop still <=USD40.

## Expanded development rationale

H v0.2 had only 69 MSS/next-open admission candidates over Jan-2024 through Feb-2025, so keeping a >=100 development minimum on that exact period would make the criterion unreachable even if every economic candidate were admitted.

The evidence standard is therefore **not lowered**.

Instead, development is prospectively expanded backward into previously unused complete 2023 data:

- warm-up: Dec 2022;
- DEV-A: Jan-Dec 2023;
- DEV-B: Jan 2024-Feb 2025;
- combined development: Jan 2023-Feb 2025.

Validation Mar-Aug 2025 and fresh holdout Sep 2025-Feb 2026 remain untouched.

## Frozen development gate

Proceed to validation only if all hold:

- combined accepted trades >=100;
- combined primary-cost expectancy >0;
- DEV-A primary-cost expectancy >0;
- DEV-B primary-cost expectancy >0.

## Promotion gates after development

Validation >=50 trades, expectancy >0, PF >=1.10, bootstrap expectancy lower bound >0.

Holdout same.

## Checkpoint 0

- v0.3 frozen before outcomes: YES;
- expanded 2023 development provenance audited: YES;
- validation/holdout untouched: YES;
- Engine-H-v0.3 outcomes calculated: NO;
- next permitted outcome: combined development only.

## Checkpoint 1 — implementation verified before outcomes

**Engine-H-v0.3 outcomes calculated:** ZERO.

Executable:

- `research/code/engine-h-v0.3.js`
- corrected pre-outcome implementation commit: `a11d4574a6bf500b7a71f8014dbafa8d560e31ce`

Verification passed:

- exact integer tick parsing;
- off-grid price rejection;
- USD40 gross-risk arithmetic;
- USD5 primary transaction-cost arithmetic;
- no v0.2 export remains;
- no `reward_risk_below_2` admission logic remains;
- no `insufficient_target_room_3xau` admission logic remains;
- no sweep-extreme stop admission remains;
- post-raid invalidation-pivot stop logic is present;
- actual target exit/reporting uses `exit_t40`.

No Engine-H-v0.3 development result existed when this checkpoint was committed.

The next permitted computation is combined development only: Jan-2023 through Feb-2025, with Dec-2022 warm-up.

### Development execution harness frozen before outcomes

Development runner:

- `research/code/run-engine-h-v0.3-development.js`
- commit: `b2fc6ee55f4a5cbdb0057857db5f806125fa743c`

Development workflow:

- `.github/workflows/exp019-engine-h-v03-development.yml`
- commit: `01d8ade1469bc52d30856624ee7219a27d6799cc`

The workflow downloads only:

- Dec-2022 warm-up;
- Jan-Dec 2023 DEV-A;
- Jan-2024 through Feb-2025 DEV-B.

It does not download validation or holdout files.

The runner verifies each loaded file's frozen Git blob SHA and byte count before calculating outcomes.

**Engine-H-v0.3 outcomes calculated at this checkpoint: ZERO.**

## Checkpoint 2 — combined development result

**Development result commit:** `dc1d54d8c0b57a8eb56c1cb9efe84dbcdcc45db6`  
**Combined development:** 2023-01-01 through 2025-02-28  
**DEV-A:** calendar 2023  
**DEV-B:** 2024-01-01 through 2025-02-28  
**Validation outcomes inspected:** NO  
**Fresh-holdout outcomes inspected:** NO

Durable result files:

- `research/results/EXP-019-development-summary-v0.3.json`
- `research/results/EXP-019-development-setups-v0.3.jsonl`
- `research/results/EXP-019-development-trades-v0.3.jsonl`

### Combined development funnel

- market-active M1 rows: **795,011**
- active 5m bars: **153,365**
- prior-range boundary breach bars: **46,512**
- external pre-existing FVG touch bars: **2,310**
- qualifying close-back raids: **613**
- in-window qualifying raids: **338**
- accepted filled trades: **58**

Post-raid terminal reasons included:

- MSS timeout after 20 active M1 bars: **168**
- no post-raid invalidation pivot: **55**
- no internal MSS pivot: **42**
- structural risk above USD40: **11**
- session close before MSS: **4**
- one-open suppression: **1**

### Combined filled-trade outcomes

- actual T40 exits: **17 / 58 = 29.31%**
- stops including entry-bar stops: **39 / 58 = 67.24%**
- timeouts: **2 / 58 = 3.45%**

Counterfactual target reachability:

- T30: **21 / 58 = 36.21%**
- T40: **17 / 58 = 29.31%**
- T50: **12 / 58 = 20.69%**
- T70: **11 / 58 = 18.97%**
- T100: **5 / 58 = 8.62%**

### Combined economics

- gross expectancy/trade: **+USD 0.48**
- net expectancy/trade at 0.25-XAU cost: **-USD 2.02**
- net expectancy/trade at primary 0.50-XAU cost: **-USD 4.52**
- primary-cost profit factor: **0.703**
- total primary-cost net P&L: **-USD 261.98**
- mean eligible-weekday P&L: **-USD 0.46**
- median eligible-weekday P&L: **USD 0**
- >=USD100/150/200 weekdays: **0%**

Risk:

- maximum drawdown: **USD 336.05**
- worst losing-trade run: **7 trades / -USD 163.45**
- mean gross structural stop risk: **USD 19.48**
- median gross structural stop risk: **USD 18.16**
- maximum admitted gross stop observed: **USD 39.11**

### Development subperiod stability

DEV-A — calendar 2023:

- accepted trades: **32**
- T40 hit rate: **18.75%**
- primary-cost expectancy: **-USD 7.18/trade**
- primary-cost PF: **0.507**
- total primary-cost P&L: **-USD 229.65**

DEV-B — Jan-2024 through Feb-2025:

- accepted trades: **26**
- T40 hit rate: **42.31%**
- primary-cost expectancy: **-USD 1.24/trade**
- primary-cost PF: **0.923**
- total primary-cost P&L: **-USD 32.33**

Both frozen development subperiod expectancy signs are negative.

### Bootstrap uncertainty

Frozen 10,000-rep, 5-weekday moving-block bootstrap, seed 19019:

- combined primary-cost expectancy point: **-USD 4.52/trade**
- 95% expectancy interval: **[-USD 11.60, +USD 2.69]**
- mean daily point: **-USD 0.46**
- 95% mean-daily interval: **[-USD 1.19, +USD 0.27]**

### Frozen-gate disposition

The frozen development gate required all of:

- combined accepted trades >=100;
- combined primary-cost expectancy >0;
- DEV-A primary-cost expectancy >0;
- DEV-B primary-cost expectancy >0.

Observed:

- accepted trades: **58** -> FAIL;
- combined expectancy: **-USD 4.52** -> FAIL;
- DEV-A expectancy: **-USD 7.18** -> FAIL;
- DEV-B expectancy: **-USD 1.24** -> FAIL.

Therefore Engine H v0.3 is **not eligible for validation**.

### Decision

**STOP EXP-019 / Engine H v0.3 before validation.**

Do not expose the untouched validation or fresh-holdout periods to v0.3.

The post-raid lower-timeframe stop substantially increased admissible trades relative to H v0.2 and reduced median stop risk, but the fixed T40 target did not produce positive cost-adjusted expectancy. The failure is present in both development subperiods rather than being solely a single-period artifact.

Do not retune v0.3. Any further redesign requires a new prospectively frozen version/engine.
