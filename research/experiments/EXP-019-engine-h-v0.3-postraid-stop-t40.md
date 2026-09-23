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
