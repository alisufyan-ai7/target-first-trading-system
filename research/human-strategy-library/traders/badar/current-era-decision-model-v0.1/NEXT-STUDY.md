# Next Study — Current-Era Decision Trace Corpus v0.1

## Status

Methodology authorized by Badar Current-Era Decision Model v0.1.

No P&L evaluation is authorized yet.

## Objective

Build an outcome-blind dataset from current-era live streams that can answer:

> Which observable facts distinguish Badar's TRADE decisions from his WAIT / NO_TRADE decisions at similar-looking chart locations?

## Source boundary

Start from:

`d19a43da80ae0e3ab4207a73a35f317120d37c84`

This includes 42 live streams through 2026-09-30.

The external repo continues updating daily, but this initial corpus is anchored to the pinned commit.

## Sampling rule

Do not sample only executed trades.

For each stream:

1. identify explicit trade decisions;
2. identify explicit `WAIT` decisions;
3. identify explicit `NO_TRADE` / skip decisions;
4. identify important post-entry reduce/exit/partial decisions;
5. label only information visible or stated at that timestamp.

The source notes already contain “Setups considered but NOT taken” sections for many recent streams.

## Priority ordering

### Pass A — newest current-era anchors

Start with the newest 10 streams:

- `EOBnMz2Y_9k` — 2026-09-30
- `CPGcMydNbbQ` — 2026-09-29
- `WUblCihXgPU` — 2026-09-28
- `1E65DgTFxe0` — 2026-09-25
- `U5CphnzaXio` — 2026-09-24
- `OpMzvMNNrHM` — 2026-09-23
- `qTSedn6hEp8` — 2026-09-21
- `fkZjFHTg3GY` — 2026-09-18
- `6trb-6A2t6Q` — 2026-09-17
- `y2Oun9g9abk` — 2026-09-16

### Pass B — all remaining pinned 2026 streams

Extend to all 42 after the schema is shown to capture Pass-A decisions without forcing ambiguous values.

## Extraction philosophy

Unknown values are allowed.

Do not resolve ambiguity merely to make modeling easier.

Examples:

- unknown exact stop distance is acceptable;
- unknown D1 bias is acceptable;
- “wait for M30 close” is meaningful even if the later trade never occurs;
- “no trade because middle” is valuable without a candidate entry price.

## Allowed analysis before P&L

- counts of TRADE / WAIT / NO_TRADE;
- prevalence of location types;
- prevalence of HTF alignment;
- confirmation families;
- reasons for skipping;
- which variables are usually knowable before a trade;
- stability across streams;
- contradictions by date.

## Not allowed yet

- expectancy;
- win rate;
- profit factor;
- outcome-conditioned feature selection;
- “which skip rule makes the most money”;
- threshold optimization.

## Formalization gate

Do not freeze a development engine until the decision corpus demonstrates:

1. repeated TRADE and NO_TRADE examples;
2. comparable cases that expose selection logic;
3. a stable subset of gates;
4. an explicit list of discretionary/unresolved variables;
5. exact evidence cutoff;
6. no outcome use during rule construction.

## Daily evidence updates

New Claude-repo sessions after `d19a43d...` are evidence deltas.

Before future hypothesis freeze:
- assess whether they confirm or contradict v0.1;
- material contradictions require a new model version.

After hypothesis freeze:
- new sessions are prospective evidence for the next version and cannot rewrite tested rules.


## Completion update — 2026-10-01

The decision-trace study described above is complete.

Final corpus:

- 42/42 pinned live streams represented;
- 347 pre-entry decision events;
- 107 TRADE decisions;
- 131 WAIT decisions;
- 109 NO_TRADE decisions;
- 136 linked post-entry management decisions;
- no future-outcome/P&L join.

See:

`decision-trace-corpus/FULL-CORPUS-SUMMARY.md`

Disposition:

`DECISION_TRACE_CORPUS_V0_1_COMPLETE — READY_FOR_OUTCOME_BLIND_RULE_FORMALIZATION`

### Next exact study

Create **Badar Current-Era Formal Decision Policy v0.1** with no P&L access.

The formal policy must:

1. preserve the hierarchy `environment -> direction -> location -> interaction -> decision evidence -> feasibility -> risk -> decision -> management`;
2. keep `TRADE / WAIT / NO_TRADE` as explicit outputs;
3. include separate confirmation-based and direct/aggressive branches;
4. define only source-supported hard gates;
5. leave unresolved human judgments explicitly unresolved rather than inventing thresholds;
6. define a deterministic annotation/execution contract suitable for a later frozen development experiment;
7. remain outcome blind.

Only after that policy is frozen may a development-test protocol be proposed.


## Formal-policy freeze update — 2026-10-01

Badar Current-Era Formal Decision Policy v0.1 has been created and frozen outcome-blind.

Path:

`formal-policy-v0.1/`

Disposition:

`FORMAL_DECISION_POLICY_V0_1_FROZEN_OUTCOME_BLIND`

### Next exact study

**Mechanization / reproducibility study — still outcome blind.**

The study must operationalize only the remaining human-classified state inputs:

1. VALID vs MIDDLE vs WRONG_EXTREME location;
2. STRONG / ADEQUATE / WEAK confirmation;
3. DEFINED_ACCEPTABLE vs DEFINED_LARGE_BUT_SIZABLE vs TOO_LARGE stop;
4. FEASIBLE vs INFEASIBLE target path;
5. which M15/M30/H1/H4 close is required for a candidate.

Required outputs:

- prospective chart-label definitions;
- explicit tie/conflict handling;
- blinded annotation protocol;
- inter-annotator or deterministic-rule reproducibility report;
- a frozen machine-readable state derivation contract.

Do not use P&L, result R, MFE/MAE, or future candles to choose thresholds.

**No development backtest is authorized until the mechanization contract is frozen.**
