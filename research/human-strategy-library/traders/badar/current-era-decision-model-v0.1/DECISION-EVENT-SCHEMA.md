# Outcome-Blind Decision Event Schema v0.1

## Purpose

Build a corpus of **decision moments** from Badar's current-era live sessions. Each event captures what was knowable at the decision timestamp, including accepted and rejected opportunities.

Future outcomes must not be used while labeling the decision.

## Unit of analysis

A `decision_event` is a point where Badar explicitly or visibly chooses:

- `TRADE`
- `WAIT`
- `NO_TRADE`
- `REDUCE_RISK`
- `EXIT / CUT`
- `PARTIAL / PROTECT`

The corpus must not contain only executed trades.

## Required fields

### Provenance
- `source_repo_commit`
- `stream_id`
- `stream_date`
- `stream_timestamp`
- `chart_timestamp_if_known`
- `instrument`
- `decision_event_id`
- `evidence_confidence`

### Observable environment
- `session` — ASIA / LONDON / NY / OTHER / UNKNOWN
- `session_phase` — PRE_OPEN / OPEN / EARLY / MID / LATE / UNKNOWN
- `news_state` — NONE_KNOWN / PRE_NEWS / POST_NEWS / ACTIVE_NEWS / UNKNOWN
- `special_context` — MONTH_END / FRIDAY / LOW_VOLUME / MANIPULATED / NONE / OTHER
- `volume_comment`

### HTF context
- `daily_bias` — BULL / BEAR / MIXED / UNKNOWN
- `h4_bias`
- `h1_bias`
- `bias_alignment` — ALIGNED / MIXED / COUNTERTREND / UNKNOWN
- `htf_close_pending` — NONE / M15 / M30 / H1 / H4 / OTHER
- `htf_close_effect` — CONFIRMS / INVALIDATES / FLIPS_BIAS / NEUTRAL / NOT_YET

### Location
- `location_present` — YES / NO / APPROACHING
- `location_types` — SESSION_HIGH, SESSION_LOW, PDH, PDL, SWING_HIGH, SWING_LOW, EQUAL_HIGH, EQUAL_LOW, RANGE_HIGH, RANGE_LOW, OB, FVG, BREAKER, BOS_ORIGIN, PREMIUM, DISCOUNT, SUPPLY_DEMAND, OTHER
- `location_position` — TOP / BOTTOM / MIDDLE / PREMIUM / DISCOUNT / UNKNOWN
- `location_quality_comment`

### Interaction
- `interaction_type` — SWEEP / FAKE_BREAK / TRAP / RETRACE_TO_POI / TWO_REJECTIONS / RANGE_TEST / CONTINUATION_RETEST / SIMPLE_TOUCH / NONE / OTHER
- `retail_liquidity_taken` — YES / NO / UNCLEAR
- `smart_money_poi_present` — YES / NO / UNCLEAR

### Confirmation
- `confirmation_type` — MSS / INVERSE_CLOSE / TWO_CANDLE_REJECTION / ENGULF / MOMENTUM_CLOSE / CLOSE_BACK_INSIDE / MINI_RANGE_BREAK / FVG_RETRACE / OB_RETRACE / DOUBLE_CONFIRMATION / NONE / OTHER
- `confirmation_tf`
- `confirmation_quality` — STRONG / ADEQUATE / WEAK / FAILED / NOT_YET
- `close_based` — YES / NO / UNCLEAR
- `second_confirmation` — YES / NO

### Execution feasibility
- `late_or_chasing` — YES / NO / UNCLEAR
- `logical_stop_present` — YES / NO / UNCLEAR
- `stop_basis` — SWEEP_EXTREME / OUTER_SWING / ZONE / CONFIRMATION_CANDLE / OTHER / UNKNOWN
- `stop_size_comment`
- `barrier_before_target` — YES / NO / UNCLEAR
- `execution_style` — MARKET_CLOSE / LIMIT_RETRACE / DIRECT_MOMENTUM / SPLIT_ENTRY / NONE / OTHER

### Risk classification
- `risk_class` — NORMAL / REDUCED / SKIP / UNKNOWN
- `risk_modifiers` — COUNTERTREND / LARGE_STOP / NEWS / LOW_CONFIDENCE / WEAK_CONFIRMATION / LATE_SESSION / AFTER_LOSS / AFTER_WIN / CHOP / OTHER

### Pre-entry decision
One of:
- `TRADE_LONG`
- `TRADE_SHORT`
- `WAIT`
- `NO_TRADE`

### Decision reason
Examples:
- `NO_TRADE_MIDDLE`
- `WAIT_HTF_CLOSE`
- `WAIT_SWEEP`
- `WAIT_RETRACE`
- `NO_TRADE_CHASE`
- `NO_TRADE_NO_LOGICAL_STOP`
- `NO_TRADE_WRONG_EXTREME`
- `TRADE_ALIGNED_SWEEP_CONFIRM`
- `TRADE_REDUCED_COUNTERTREND`

## Post-entry management events

A management decision is a separate event linked by `parent_trade_event_id`.

Fields:

- `management_action` — HOLD / TIGHTEN_STOP / BREAK_EVEN / STRUCTURAL_PROTECTION / PARTIAL / EXTEND_TARGET / PULL_TARGET / MANUAL_EXIT
- `management_reason` — CONFIRMATION_FAILED / OPPOSING_CLOSE / TP1_REACHED / NEW_STRUCTURE / TARGET_LIQUIDITY_REACHED / MARKET_MANIPULATED / NEWS / OTHER
- `decision_tf`
- `source_reason_text_paraphrase`

## Forbidden pre-label fields

During decision extraction do **not** include:

- future MFE;
- future MAE;
- result R;
- final P&L;
- eventual TP/SL outcome;
- whether a skipped trade would have won;
- future candles after the decision timestamp.

Those fields may only be joined later after the decision corpus and formalized hypothesis are frozen.

## Why this schema matters

Earlier experiments mostly had:

`pattern exists -> simulate trade`

This corpus must preserve:

`same-looking environment -> TRADE / WAIT / NO_TRADE`

That is what is needed to test whether the human advantage is primarily **selection** rather than the raw pattern itself.
