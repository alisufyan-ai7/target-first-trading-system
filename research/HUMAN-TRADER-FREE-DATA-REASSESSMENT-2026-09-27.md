# Human-Trader / Free-Data Reassessment — 2026-09-27

**Status:** governing research correction  
**Paid-data policy:** paused unless later explicitly authorized by user

## Why this reassessment exists

The project has now tested multiple broad information families:

- multi-timeframe structural context;
- macro timing / surprise;
- DXY / US-TBond reaction proxies;
- broker quote/tick microstructure.

Those layers did not establish a stable incremental information advantage under frozen development gates.

That does **not** prove day trading is impossible.

It does show that the project's recent question was often too broad:

> can one information layer improve target prediction across a large generic candidate universe?

A profitable discretionary trader usually operates more selectively.

## What the repository already tells us

### 1. EXP-002 historical positive result

EXP-002 reported a positive exploratory Engine-A screen, but EXP-014 proved the exact implementation is not honestly recoverable from surviving evidence.

Therefore EXP-002 is evidence that a selective liquidity/MSS/FVG process can look promising, but it is not a deployable validated engine.

### 2. Engine Q non-chasing clue

EXP-038 showed the 50% retracement entry materially improved economics versus matched immediate entry by about 0.114R gross.

The signal itself still failed.

Lesson:

> selection/context first, non-chasing execution second.

### 3. Broad information studies

EXP-040 through EXP-043 repeatedly showed that adding richer generic features to broad candidates did not create robust edge.

Lesson:

> the missing element may be selective setup definition and skip logic, not another universal feature.

### 4. Existing architecture already says this

EXP-015 is paused because the intended architecture is:

`validated specialized engine -> meaningful candidate -> probability/EV ranker`

not:

`every bar / generic pivot -> universal classifier -> trade`.

## Human-process interpretation

A skilled day trader may behave more like:

1. specialize in a market / session;
2. identify meaningful external liquidity or structural location;
3. wait for price to interact with that location;
4. decide whether the interaction is **rejection** or **acceptance**;
5. require a lower-timeframe trigger consistent with that branch;
6. avoid chasing;
7. define invalidation structurally;
8. verify room to the next meaningful target;
9. skip if the path is crowded or execution is stale;
10. manage the trade with partials / runner only when the path justifies it.

The critical distinction is that the same liquidity level can produce two different trade ideas:

- **rejection / reclaim** -> reversal;
- **acceptance / hold** -> continuation.

Earlier engines frequently hard-coded only one interpretation.

## Active no-paid-data direction

Paid COMEX/EBS/institutional data is not required for the active path.

Use only already-available/free project data:

- canonical Dukascopy M1;
- existing derived M5/15M/1H context;
- frozen macro calendar as awareness/context only when useful;
- frozen Dukascopy tick/quote snapshot as execution-state context only if a future engine specifically needs it.

Do not resume generic information-layer mining.

## Next experiment principle

The next experiment must be **engine-first and selective**.

Gold first because:

- it is the project's economic anchor;
- the original Badar evidence is Gold-centric;
- structural dollar targets and 0.10-lot anchor are already well defined.

The next setup family should be a decision tree around meaningful liquidity:

`meaningful level -> attack -> rejection or acceptance -> lower-timeframe trigger -> non-chasing entry -> structural stop -> target path`.

The first stage must be zero-outcome opportunity-density / causality only.

Do not inspect target/P&L outcomes until:

- the setup rules are frozen;
- the branch rules are mutually exclusive;
- opportunity density is adequate without weakening rules;
- no future information is used;
- the target-path rule is frozen before outcomes.

## Risk / objective correction

The USD150-200 strong-day zone remains an eventual economic objective, not a quota.

On USD500 starting equity it represents an extreme percentage return and cannot be promised or manufactured safely by leverage.

The correct order remains:

1. establish robust positive post-cost edge;
2. prove drawdown control;
3. size from structural risk and current equity;
4. combine validated specialized engines;
5. only then evaluate how often the portfolio reaches USD150-200 strong-day outcomes.

## Anti-loop rule

Do not create another experiment whose only novelty is:

- a new threshold;
- another OHLC transform;
- another generic classifier;
- another market subset chosen after seeing outcomes.

The next engine must differ at the **decision-process level**.
