# Reproducibility Audit — Mechanization v0.1 Phase 1

## Status

Outcome blind. No P&L, result R, MFE, MAE or future skipped-trade outcome was used.

Input:

`../decision-trace-corpus/full-pre-entry-events.csv`

N = 347 decisions:

- 107 TRADE;
- 131 WAIT;
- 109 NO_TRADE.

## Important limitation

This is an **internal-consistency audit**, not independent annotation validation.

The original decision-event fields were extracted from Badar source notes/transcripts, so they may reflect his stated decision.

True reproducibility requires the Phase-2 blinded chart replay.

## Hard-gate audit

Six structured gates can be checked directly from the current corpus.

| Gate | Events hit | TRADE contradictions | WAIT | NO_TRADE |
|---|---:|---:|---:|---:|
| location not reached / absent | 84 | 0 | 61 | 23 |
| middle | 18 | 0 | 4 | 14 |
| chasing | 19 | 0 | 1 | 18 |
| no logical stop | 1 | 0 | 0 | 1 |
| confirmation failed | 13 | 0 | 0 | 13 |
| required close pending | 44 | 0 | 42 | 2 |

Because events overlap, the union is:

- **148 distinct WAIT/NO_TRADE events**
- **0 TRADE contradictions**

Thus these six rules explain or temporally defer **148 / 240 = 61.7%** of non-trade decisions without conflicting with any of the 107 recorded trades.

This supports freezing them as Phase-1 hard/pending gates.

## Residual 92 non-trade decisions

After removing events already captured by the six Phase-1 gates, 92 WAIT/NO_TRADE events remain.

Largest unresolved reason families include:

- stop too large: 7;
- confirmation close still desired but not represented in `htf_close_pending`: 5;
- wrong extreme not yet machine-derived from candidate direction: 4;
- generic confirmation desired: 4;
- explicit stop-for-day: 4;
- pre-news stand-aside: 3;
- active-direction conflict: 2;
- discretion unclear: 2;
- retracement desired: 2;
- overtrade stop: 2.

The remainder is spread across lower-frequency reasons.

This identifies the exact fields that need richer state derivation.

## Coverage audit of existing fields

### Location

- `location_present`: 347/347 populated.
- YES: 263
- APPROACHING: 61
- NO: 23

`location_position`:

- known non-UNKNOWN: 200/347 = 57.6%
- UNKNOWN: 147

No TRADE occurs with location not present.

No TRADE occurs with MIDDLE.

### Confirmation

`confirmation_quality` is populated on all events:

- STRONG: 51
- ADEQUATE: 46
- WEAK: 19
- FAILED: 13
- NOT_YET: 218

However `NOT_YET` currently mixes:

- genuinely pending confirmation;
- no-confirmation/direct branch events;
- events where confirmation was not the deciding issue.

Therefore the mechanized schema must separate:

- `confirmation_required`
- `confirmation_state`

rather than relying on one field.

### Stop

`logical_stop_present`:

- YES: 123
- NO: 1
- UNCLEAR: 223

All 107 TRADE decisions are YES.

This strongly supports the structural-stop hard gate but shows that non-trade stop geometry was under-annotated.

### Target path

`barrier_before_target = UNCLEAR` on **347/347** events.

No target-path reproducibility claim is currently possible.

This is the largest missing input in the corpus.

### HTF close pending

- NONE: 303
- named pending close: 44

Of the 44 pending-close events:

- 42 WAIT
- 2 NO_TRADE
- 0 TRADE

This is a clean source-consistent temporal gate.

### Chasing

- 19 events marked late/chasing;
- 18 NO_TRADE;
- 1 WAIT;
- 0 TRADE.

## Phase-1 disposition by classifier

| Classifier | Status after Phase 1 |
|---|---|
| location reached / approaching / absent | MECHANIZED |
| middle | MECHANIZED given frozen active boundaries |
| wrong extreme | PARTIAL — needs candidate direction + continuation exception |
| chasing | MECHANIZED |
| structural stop exists | MECHANIZED |
| stop sizeability | RISK-LAYER DEPENDENT |
| confirmation open/failed | MECHANIZED |
| confirmation strength | PARTIAL |
| target path | CONTRACT DEFINED, NO CORPUS COVERAGE |
| required close pending | MECHANIZED when plan names timeframe |
| choosing required timeframe | PARTIAL |

## Scientific conclusion

The formal policy is more mechanizable than the initial qualitative model suggested.

Several important veto/pending states already behave like hard gates across the full source corpus.

But a fully automated OHLC experiment would still be scientifically premature because:

1. target-path state was never annotated;
2. 223 stop states are unclear in non-trades;
3. candidate direction is missing for many WAIT/NO_TRADE events;
4. major/minor swing and hidden-OB selection remain subjective;
5. confirmation-strength labels were not independently blinded.

## Disposition

`PHASE1_INTERNAL_REPRODUCIBILITY_PASS`

This means:

- the hard-gate contract is coherent enough to freeze;
- it does **not** mean the strategy is profitable;
- it does **not** authorize P&L testing.

Next requirement is the blinded visual reproducibility pass.
