# Model Refinement After Full Decision Corpus

## Status

Badar Current-Era Decision Model v0.1 was created before the 42-stream decision corpus.

The corpus is now complete and refines—but does not replace—the original model.

## Refinement 1 — explicit confirmation is not universal

Original v0.1 language treated confirmation as a core stage.

Full corpus:

- 107 trade decisions;
- 87 include an explicit coded confirmation family;
- 20 do not.

Therefore:

> **Decision evidence is core; one explicit LTF confirmation pattern is not.**

The formal hierarchy becomes:

`location/context + executable invalidation -> confirmation OR deliberate direct/aggressive branch`.

A direct branch must not be interpreted as “no logic.” It normally has strong location/HTF/stop geometry and often lower risk.

## Refinement 2 — sweep is a branch, not the universal root

Only 36/107 trades are coded as simple sweeps.

Other common interactions are POI retracement, trap, continuation retest and rejection.

Therefore the flagship sweep→MSS→FVG model is an important setup family but **not the entire current-era decision process**.

## Refinement 3 — stop feasibility is a stronger universal feature

Every captured trade decision includes a logical stop/invalidation in the extraction.

Conversely, explicit no-trades include cases where:

- stop is too large;
- no logical stop exists;
- price location makes stop geometry poor.

Future formalization should evaluate **execution feasibility before trigger family selection**.

## Refinement 4 — risk class is part of the model, not an afterthought

70/107 trade decisions are coded reduced-risk.

Future formalization must preserve at least:

- NORMAL
- REDUCED
- SKIP

rather than treating all accepted entries equally.

Target-First account-level sizing remains independent from Badar's changing risk percentages.

## Refinement 5 — management must be modeled as premise updates

136 management decisions show frequent:

- BE;
- partials;
- manual exits;
- tightening.

A static fixed-SL/fixed-TP implementation would omit a large part of current live behavior.

## Refined v0.1 hierarchy

```text
environment
-> HTF direction
-> location
-> interaction
-> decision evidence
     -> confirmation branch
     -> direct/aggressive branch
-> execution feasibility / invalidation geometry
-> risk class
-> TRADE / WAIT / NO_TRADE
-> post-entry premise monitoring
-> adaptive risk / exit / partial / runner action
```

## Formalization warning

Do not convert `direct/aggressive branch` into a broad permission.

It requires its own source-derived eligibility criteria. Otherwise it becomes a loophole that recreates unconstrained discretionary trading.

No P&L test is authorized from this refinement alone.
