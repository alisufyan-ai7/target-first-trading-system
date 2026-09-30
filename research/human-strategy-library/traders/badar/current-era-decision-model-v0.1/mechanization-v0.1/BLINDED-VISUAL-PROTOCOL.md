# Blinded Visual Reproducibility Protocol — Mechanization v0.1 Phase 2

## Objective

Measure whether the remaining qualitative Badar decision states can be reproduced from chart information alone before any P&L is visible.

This phase is not a profitability test.

## Required chart snapshot pack

For each decision event, reconstruct the chart state at the frozen event timestamp with **all future bars hidden**.

Preferred synchronized views:

- D1 context;
- H4 context;
- H1 structure and POIs;
- M15;
- M5;
- M1 where the source used it.

Use approximately the most recent 2–3 trading days for intraday levels, consistent with Badar's current teaching.

Each snapshot package must include:

- instrument;
- timezone;
- exact frozen timestamp;
- candidate direction if it was prospectively identifiable before the decision;
- session state;
- current candle status (open/closed);
- no later trade result or management information.

## Blindness rules

Annotators must not see:

- Badar's eventual TRADE / WAIT / NO_TRADE decision;
- trade outcome;
- result R;
- P&L;
- future candles;
- later management actions;
- whether a skipped setup would have won;
- source paraphrases that reveal the eventual decision.

Badar commentary may be used only if it was spoken **before** the frozen decision point and does not reveal the eventual action.

## Scope

Use all 347 events if chart frames can be reconstructed reliably.

Do not sample only executed trades.

If an event lacks a prospectively identifiable candidate direction:

- annotate direction-independent fields;
- mark candidate-direction-dependent fields `NO_CANDIDATE_SIDE`;
- do not force a side from the eventual decision.

## Independent annotation

At least two independent annotation passes are required.

Annotator A and Annotator B must:

- use the same frozen derivation contract;
- not see each other's labels;
- not see Badar's decision label;
- preserve `UNRESOLVED` rather than guessing.

## Fields to compare

Primary reproducibility fields:

1. `location_state`
2. `confirmation_state`
3. `structural_stop_state`
4. `target_path_state`
5. `htf_close_state`

Secondary fields:

- interaction family;
- directional context;
- location family;
- confirmation family;
- late/chasing state;
- direct/aggressive branch eligibility.

## Agreement metrics

For each categorical field compute:

- raw percent agreement;
- Cohen's kappa when class counts permit;
- confusion matrix;
- unresolved rate.

For deterministic binary hard gates also compute:

- positive agreement;
- negative agreement.

## Reproducibility gates

A field is eligible for automated policy use only if:

### Core hard-gate fields

For:

- location state;
- structural stop existence;
- required/pending HTF-close state;
- chasing;

require:

- raw agreement >= 85%;
- Cohen's kappa >= 0.70 where calculable;
- unresolved rate <= 10%.

### Quality fields

For:

- confirmation strength;
- target-path state;
- direct/aggressive eligibility;

require:

- raw agreement >= 80%;
- Cohen's kappa >= 0.60 where calculable;
- unresolved rate <= 15%.

If a field fails its gate:

- it remains human/discretionary;
- it may not be silently converted into an automated threshold;
- no development backtest may use it as though mechanically resolved.

These are reproducibility thresholds, not trading-performance thresholds.

## Adjudication

When annotators disagree:

1. preserve both original labels;
2. flag `ANNOTATION_CONFLICT`;
3. adjudicate using only the frozen chart and derivation contract;
4. record the reason;
5. do not inspect P&L or future bars.

If disagreement exposes a missing rule:

- add it only in a new mechanization version;
- do not retroactively edit v0.1 after outcome access.

## Policy-output replay

After annotation labels are frozen, run Formal Decision Policy v0.1 on each event.

This produces an outcome-blind reconstructed policy output:

- TRADE_LONG_NORMAL
- TRADE_LONG_REDUCED
- TRADE_SHORT_NORMAL
- TRADE_SHORT_REDUCED
- WAIT
- NO_TRADE

## Behavioral-fidelity reveal

Only after all annotations and policy outputs are frozen may Badar's actual decision label be revealed.

Then compute:

- TRADE vs WAIT vs NO_TRADE confusion matrix;
- direction agreement for TRADE events;
- normal-vs-reduced risk agreement where source evidence supports it;
- false-trade rate: policy TRADE when Badar chose WAIT/NO_TRADE;
- missed-trade rate: policy WAIT/NO_TRADE when Badar traded.

This is still **not a P&L test**.

It measures whether the mechanized policy reproduces Badar's behavior.

## Promotion gate to development P&L

A P&L development study may be specified only after:

1. core classifier reproducibility passes;
2. quality fields either pass or are explicitly excluded from the automated subset;
3. policy-output behavior-fidelity report is frozen;
4. broker/instrument risk-sizeability inputs are defined;
5. the exact automated subset and unresolved human-only branches are declared;
6. no rule has been chosen using P&L.

## Current data limitation

The pinned Claude evidence repository contains:

- notes;
- transcripts;
- per-stream CSVs;

but **no persistent chart image/frame assets**.

Therefore Phase 2 cannot be executed faithfully from the current repositories alone.

The required next evidence artifact is a timestamped chart-snapshot pack built from the source streams or independently reconstructed market data.
