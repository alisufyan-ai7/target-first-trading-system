# Freeze — Badar Formal Decision Policy v0.1

## Freeze declaration

This policy version is frozen against:

External Badar evidence snapshot:

`d19a43da80ae0e3ab4207a73a35f317120d37c84`

Target-First decision corpus:

- 42 live streams;
- 347 outcome-blind pre-entry decisions;
- 136 linked management decisions.

No future outcome/P&L/MFE/MAE analysis was used to create the policy.

## Frozen principles

1. Location is evaluated before trigger.
2. Middle / wrong-extreme / absent location is not rescued by an LTF signal.
3. Waiting is a valid decision.
4. Chasing is disallowed.
5. HTF closes may confirm, invalidate or force reevaluation.
6. A logical structural invalidation must exist before entry.
7. Sweep is not universal.
8. Explicit confirmation is not universal.
9. Direct/aggressive entries are legal only through the narrow Branch-B contract.
10. Weak/no-confirmation ideas cannot silently become normal-risk without satisfying their branch rules.
11. Countertrend/news/large-stop/low-confidence conditions downgrade risk.
12. Post-entry management responds to premise changes, not only the original SL/TP.
13. Exact raw-price thresholds that Badar did not define remain unresolved.

## Frozen direct-entry branch

Direct/no-confirmation entries require:

- valid structural location;
- sweep or retrace-to-POI interaction;
- defined acceptable/sizable structural stop;
- no chase;
- no invalidating HTF close;
- pre-entry reason that is writable without future information.

Normal risk additionally requires alignment, acceptable stop geometry and no downgrade modifier.

## Forbidden after freeze

Before a future development experiment is specified and sealed, do not:

- add an exception because a historical winner would otherwise be missed;
- remove a veto because a skipped setup later won;
- choose stop/RR/body/MSS thresholds by looking at profitability;
- widen the direct-entry branch using outcome examples;
- silently replace WAIT with TRADE to increase sample count;
- use Claude `derived/**` outputs as source evidence;
- use validation/holdout outcomes.

## Current scientific disposition

`FORMAL_DECISION_POLICY_V0_1_FROZEN_OUTCOME_BLIND`

## Next authorized research step

**Mechanization / reproducibility study — outcome blind.**

Goal:

Convert the remaining human-classified state inputs into explicit prospective chart-label rules and measure inter-annotator / rule reproducibility.

Priority unresolved classifiers:

1. VALID vs MIDDLE vs WRONG_EXTREME location;
2. STRONG/ADEQUATE/WEAK confirmation;
3. DEFINED_ACCEPTABLE vs DEFINED_LARGE_BUT_SIZABLE vs TOO_LARGE stop;
4. FEASIBLE vs INFEASIBLE target path;
5. which HTF close is required for a candidate.

No P&L backtest is authorized until that mechanization contract is frozen.
