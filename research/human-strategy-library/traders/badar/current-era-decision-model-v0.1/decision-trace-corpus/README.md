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
