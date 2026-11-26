# Key Confusion Matrices — Phase-2 v0.1 Independent A/B

Rows = Annotator A. Columns = Annotator B.

These counts are outcome-blind and decision-label-blind.

## location_state

| A \ B | ABSENT | APPROACHING | MIDDLE | UNRESOLVED | VALID | WRONG_EXTREME |
|---|---:|---:|---:|---:|---:|---:|
| ABSENT | 3 | 2 | 1 | 6 | 4 | 3 |
| APPROACHING | 0 | 10 | 7 | 3 | 6 | 3 |
| MIDDLE | 1 | 4 | 24 | 8 | 9 | 5 |
| UNRESOLVED | 2 | 4 | 2 | 16 | 4 | 4 |
| VALID | 3 | 12 | 27 | 4 | 58 | 11 |
| WRONG_EXTREME | 0 | 2 | 2 | 0 | 0 | 4 |

## confirmation_state

| A \ B | ADEQUATE | FAILED | NOT_YET | STRONG | UNRESOLVED | WEAK |
|---|---:|---:|---:|---:|---:|---:|
| ADEQUATE | 17 | 0 | 8 | 16 | 0 | 1 |
| FAILED | 1 | 6 | 2 | 3 | 0 | 1 |
| NONE | 1 | 0 | 3 | 3 | 0 | 0 |
| NOT_YET | 24 | 1 | 46 | 17 | 7 | 4 |
| STRONG | 2 | 1 | 3 | 15 | 2 | 1 |
| UNRESOLVED | 0 | 0 | 5 | 1 | 19 | 1 |
| WEAK | 2 | 3 | 12 | 12 | 12 | 2 |

## structural_stop_state

| A \ B | DEFINED | UNDEFINED | UNRESOLVED |
|---|---:|---:|---:|
| DEFINED | 162 | 0 | 3 |
| UNDEFINED | 1 | 0 | 0 |
| UNRESOLVED | 51 | 1 | 36 |

## target_path_state

| A \ B | FEASIBLE | INFEASIBLE | UNRESOLVED |
|---|---:|---:|---:|
| FEASIBLE | 139 | 22 | 14 |
| INFEASIBLE | 1 | 0 | 1 |
| UNRESOLVED | 38 | 4 | 35 |

## htf_close_state

| A \ B | CONFIRMS | NEUTRAL | NOT_RELEVANT | UNRESOLVED |
|---|---:|---:|---:|---:|
| CONFIRMS | 0 | 22 | 1 | 0 |
| INVALIDATES | 0 | 2 | 0 | 0 |
| NEUTRAL | 3 | 39 | 0 | 2 |
| NOT_RELEVANT | 0 | 49 | 0 | 0 |
| UNRESOLVED | 1 | 120 | 7 | 8 |

## late_state

| A \ B | CHASING | ON_TIME | UNRESOLVED |
|---|---:|---:|---:|
| CHASING | 27 | 15 | 8 |
| ON_TIME | 51 | 98 | 8 |
| UNRESOLVED | 10 | 12 | 25 |

## direct_branch_eligible

| A \ B | NO | UNRESOLVED | YES |
|---|---:|---:|---:|
| NO | 60 | 12 | 17 |
| UNRESOLVED | 42 | 25 | 13 |
| YES | 36 | 1 | 48 |

## Interpretation rule

These matrices are diagnostic inputs for Mechanization v0.2 only.

Do not use them with Badar decision labels or P&L.

Do not adjudicate cells post hoc to make v0.1 pass.
