# Badar Current-Era Decision Trace Corpus

## Status

**Pass A complete — newest 10 live streams**  
**Outcome/P&L join: NOT PERFORMED**

Source evidence repository commit:

`d19a43da80ae0e3ab4207a73a35f317120d37c84`

The corpus is built from the external repository's source-layer stream notes and preserves what was stated/visible at the decision timestamp.

## Files

- `pass-a-pre-entry-events.csv` — 107 pre-entry decisions.
- `pass-a-management-events.csv` — 36 post-entry management decisions.
- `PASS-A-SUMMARY.md` — descriptive, outcome-free analysis.

## Streams covered

1. `EOBnMz2Y_9k` — 2026-09-30
2. `CPGcMydNbbQ` — 2026-09-29
3. `WUblCihXgPU` — 2026-09-28
4. `1E65DgTFxe0` — 2026-09-25
5. `U5CphnzaXio` — 2026-09-24
6. `OpMzvMNNrHM` — 2026-09-23
7. `qTSedn6hEp8` — 2026-09-21
8. `fkZjFHTg3GY` — 2026-09-18
9. `6trb-6A2t6Q` — 2026-09-17
10. `y2Oun9g9abk` — 2026-09-16

## Corpus rules

### Included

- Badar's explicit trade decisions.
- Explicit waits.
- Explicit no-trade / skip decisions.
- Explicit management actions.
- Low-confidence decisions only when the ambiguity is important and clearly labelled.

### Excluded

- Future candles after the decision timestamp.
- MFE / MAE.
- Final outcome.
- Result R.
- P&L.
- Whether a skipped setup later would have won.
- Team/VIP/Zain trades unless Badar himself explicitly endorses the decision logic.

## Important caveat

This is a **salient-decision corpus**, not a second-by-second annotation of every stream frame.

The objective is to reconstruct the human decision hierarchy before formalization, not to create artificial precision from noisy machine transcripts.

## Next corpus step

Pass B extends the same schema to the remaining 32 live streams pinned in the source snapshot.

No outcome join is authorized until the decision corpus and subsequent rule formalization are frozen.


## Full-corpus completion

Pass B is complete across the remaining 32 pinned live streams.

Canonical merged files:

- `full-pre-entry-events.csv` — **347** outcome-blind pre-entry decisions across all **42** pinned streams.
- `full-management-events.csv` — **136** linked management decisions.
- `FULL-CORPUS-SUMMARY.md` — descriptive outcome-free analysis.
- `MODEL-REFINEMENT-AFTER-CORPUS.md` — changes to the decision model supported by the complete corpus.

Full pre-entry decisions:

- 61 TRADE_SHORT
- 46 TRADE_LONG
- 131 WAIT
- 109 NO_TRADE

Integrity checks passed:

- all decision IDs unique;
- all management IDs unique;
- every management record points to an existing TRADE event;
- zero management rows point to WAIT/NO_TRADE;
- no P&L/result-R/MFE/MAE/future-outcome columns exist in the pre-entry corpus;
- all rows use the pinned external source commit `d19a43d...`.

Scientific status:

`DECISION_TRACE_CORPUS_V0_1_COMPLETE — READY_FOR_OUTCOME_BLIND_RULE_FORMALIZATION`

No P&L test is authorized yet.
