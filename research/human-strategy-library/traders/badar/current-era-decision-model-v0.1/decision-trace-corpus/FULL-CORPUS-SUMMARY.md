# Full Corpus Summary — Badar Current-Era Decision Trace v0.1

**Evidence cutoff:** external repo commit `d19a43da80ae0e3ab4207a73a35f317120d37c84`  
**Streams:** 42  
**Period:** 2026-07-06 through 2026-09-30  
**P&L / outcome join:** NOT PERFORMED

## Corpus size

### Pre-entry decisions

Total: **347**

| Decision | Count | Share |
|---|---:|---:|
| WAIT | 131 | 37.8% |
| NO_TRADE | 109 | 31.4% |
| TRADE_SHORT | 61 | 17.6% |
| TRADE_LONG | 46 | 13.3% |
| **All TRADE** | **107** | **30.8%** |
| **WAIT + NO_TRADE** | **240** | **69.2%** |

This is a **salient-decision corpus**, not a second-by-second market-frequency estimate. The percentages describe decisions explicitly recoverable from stream notes, not how often the market objectively offered setups.

### Post-entry management decisions

Total: **136**

| Action | Count |
|---|---:|
| BREAK_EVEN | 37 |
| PARTIAL | 35 |
| MANUAL_EXIT | 23 |
| TIGHTEN_STOP | 21 |
| HOLD | 13 |
| STRUCTURAL_PROTECTION | 5 |
| EXTEND_TARGET | 1 |
| REDUCE_RISK | 1 |

Management is therefore a major observable part of Badar's method, not merely a fixed SL/TP afterthought.

## Strongest descriptive findings

### 1. Selection dominates the visible decision process

There are **240 WAIT/NO_TRADE decisions versus 107 entries**.

The most common WAIT families are:

| WAIT reason | Count |
|---|---:|
| confirmation close pending | 17 |
| HTF close pending | 12 |
| retracement pending | 11 |
| sweep pending | 7 |
| sweep + confirmation pending | 5 |
| generic confirmation pending | 4 |

Badar frequently knows the **location** before he is willing to execute. The decision is often temporal: wait for price to interact correctly, wait for a candle to close, or wait for a better retracement.

### 2. Wrong location is a recurring explicit veto

Top explicit NO_TRADE reasons include:

| NO_TRADE reason | Count |
|---|---:|
| wrong extreme | 8 |
| stop too large | 7 |
| middle of range / no edge location | 6 |
| chasing / late entry | 5 |
| stop trading for the day | 4 |
| HTF-close conflict | 3 |
| no meaningful location | 3 |
| required structure missing | 3 |
| pre-news stand-aside | 3 |

This is consistent across July, August and September.

The most repeated location failure is conceptually simple:

- do not sell after price is already extended at the low;
- do not buy at the top merely because price is strong;
- do not trade the middle;
- wait for price to come to a location where invalidation and target logic make sense.

### 3. Location + risk geometry are more stable than any single trigger

Of the **107 captured trade decisions**:

- **105** have a specifically typed location in the corpus;
- the other 2 are post-NFP continuation entries whose source notes still describe a pullback/continuation context but were left with generic `OTHER` location coding;
- **107/107** have a logical stop identified at the decision point.

Stop basis among trade decisions:

| Stop basis | Count |
|---|---:|
| zone / POI boundary | 56 |
| sweep extreme | 30 |
| confirmation candle | 11 |
| outer swing | 8 |
| range low | 1 |
| unknown | 1 |

This is descriptive evidence that **“where am I wrong?” is part of the trade decision itself**, not something added after entry.

### 4. Sweep is important, but clearly not universal

Trade interaction types include:

| Interaction | Count |
|---|---:|
| sweep | 36 |
| retrace to POI | 22 |
| trap | 11 |
| continuation retest | 10 |
| rejection | 10 |
| fake break | 5 |
| other / combined forms | 13 |

Only about one-third of captured trades are coded as a simple sweep interaction.

Therefore a future formalization must not require:

`every trade = liquidity sweep -> MSS -> FVG`

Some current-era trades are continuation/retracement trades, direct zone entries, or trap/rejection entries without a textbook sweep.

### 5. Explicit confirmation is common, but not mandatory

Confirmation coding among 107 trades includes:

- momentum close: 30;
- inverse close: 13;
- close-back-inside: 12;
- rejection / 2CR families: multiple;
- MSS/FVG and other combined confirmations: multiple;
- **no separately coded confirmation: 20**.

Thus **87/107** trade decisions include an explicit confirmation family, while **20/107** are direct/aggressive/location-based decisions.

Those direct decisions are not random. They generally rely on some combination of:

- strong location;
- very small/defined stop;
- pre-existing HTF structure;
- limit/retrace geometry;
- reduced risk.

So v0.1 is refined from:

`location -> mandatory confirmation -> trade`

to:

```text
location + context + executable invalidation
    -> either explicit confirmation
       OR deliberate aggressive/direct execution with risk downgrade
```

### 6. M1 is an execution tool, not a standalone strategy

Execution style:

| Style | Count |
|---|---:|
| market / confirmation close | 88 |
| limit retrace | 13 |
| split entry | 6 |

M1/M3/M5 appears repeatedly for execution, but the corpus also repeatedly records Badar refusing M1 signals when:

- price is in the middle;
- HTF close conflicts;
- stop is too large;
- the move is already late;
- the signal is at the wrong extreme.

Therefore an M1 signal without location/context is not a faithful Badar reconstruction.

### 7. Risk classification is integral to selection

Of 107 trade decisions:

- **70 REDUCED_RISK**
- **37 NORMAL_RISK**

Frequent risk modifiers include:

- news;
- countertrend;
- large stop;
- low-probability classification;
- lower confidence;
- after a prior win;
- second/re-entry position.

Badar does not treat all technically valid setups as equal-sized bets.

### 8. Active invalidation is a recurring management rule

Across 136 management events:

- 37 break-even decisions;
- 35 partials;
- 23 manual exits;
- 21 stop tightenings.

Common management causes include:

- TP1 reached;
- favorable movement;
- opposing candle close;
- new structure;
- confirmation failure.

This strongly supports a post-entry state machine.

The initial structural SL is **not** the only definition of “wrong.” Badar frequently cuts or protects earlier when new candle behavior contradicts the premise.

## Stable decision hierarchy after all 42 streams

The corpus supports the following hierarchy as the current best human-logic reconstruction:

```text
1. ENVIRONMENT
   session / news / volatility / unusual conditions

2. DIRECTIONAL CONTEXT
   D1 / H4 / especially H1 structure and recent close

3. LOCATION
   meaningful extreme / POI / range edge / session liquidity / OB / FVG

4. INTERACTION
   sweep / trap / retrace / rejection / continuation retest

5. DECISION EVIDENCE
   close / MSS / inverse close / 2CR / momentum
   OR intentionally aggressive direct execution

6. EXECUTION FEASIBILITY
   not late, definable structural stop, acceptable geometry

7. RISK CLASS
   normal / reduced / skip

8. PRE-ENTRY OUTPUT
   TRADE / WAIT / NO_TRADE

9. POST-ENTRY PREMISE MONITORING
   expected follow-through / opposing close / new structure / target liquidity

10. MANAGEMENT OUTPUT
   hold / partial / tighten / BE / structural protection / manual exit
```

## Candidate CORE gates after corpus

These are sufficiently recurrent to carry into a formalization stage:

1. **A meaningful location must exist.**
2. **Do not trade the middle as though a lower-timeframe pattern alone creates edge.**
3. **Do not chase a move that has already left the intended execution area.**
4. **A logical structural invalidation must be definable before entry.**
5. **HTF/H1 context and candle closes can confirm, downgrade or invalidate a lower-timeframe idea.**
6. **WAIT is a valid output when location exists but interaction/close/retracement is incomplete.**
7. **Trade quality changes risk size.**
8. **Countertrend / news / large-stop / weak-confidence setups are frequently downgraded.**
9. **Post-entry premise changes can justify risk reduction or manual exit before original SL.**
10. **No single confirmation family is mandatory across all current-era trades.**

## Candidate STRONG but non-universal gates

- sweep before reversal;
- session-high/low liquidity;
- OB/FVG co-location;
- MSS after a sweep;
- double confirmation;
- M15/M30 close before M1 execution;
- partial + runner management.

These should remain optional branches, not universal requirements.

## Remaining discretionary variables

The corpus still does not mechanically define:

- how Badar chooses between several nearby valid POIs;
- how close two levels must be to count as the “same zone”;
- exact swing-selection rule for MSS;
- exact threshold for a “strong” close;
- when a direct no-confirmation trade is acceptable beyond qualitative stop/location quality;
- exact stop-size ceiling by regime;
- precise quality score for normal vs reduced risk;
- exact news policy;
- exact stop-tightening / BE timing;
- when one failed confirmation deserves a second attempt versus abandonment.

These are the highest-value items for formalization.

## Important unresolved decision traces

Do not delete cases that do not fit the clean model.

Examples include:

- `fkZjFHTg3GY` 2026-09-18: a sell POI + rejection + sweep + MSS is recognized, yet Badar does not take it.
- `OCBsHuFhjUQ` 2026-08-05: a strong buy confirmation is explicitly skipped for discipline.
- direct no-confirmation trades such as `C18mm9p2oW4`, `9D7wgJCdP5c`, and `MbUagftbsIw` show that location/stop geometry can sometimes substitute for a textbook trigger.

These are not noise to optimize away. They are evidence that a human discretion variable remains.

## Integrity status

- source commit pinned: **PASS**
- 42 pinned streams represented: **PASS**
- pre-entry decision IDs unique: **PASS**
- management IDs unique: **PASS**
- every management event links to an existing TRADE event: **PASS**
- management events linked to non-trades: **0**
- future outcome/P&L/MFE/MAE columns in pre-entry corpus: **0**
- outcome-conditioned feature selection: **NOT PERFORMED**
- P&L evaluation: **NOT PERFORMED**

## Scientific disposition

**DECISION_TRACE_CORPUS_V0_1_COMPLETE — READY_FOR_OUTCOME_BLIND_RULE_FORMALIZATION**

This does **not** authorize a P&L test yet.

The next stage is to convert only the stable hierarchy into an explicit, reproducible decision policy while preserving:

- optional branches;
- reduced-risk classes;
- `WAIT` and `NO_TRADE`;
- unresolved discretion;
- no outcome-driven threshold selection.

Only after that formal policy is frozen may a development experiment be specified.
