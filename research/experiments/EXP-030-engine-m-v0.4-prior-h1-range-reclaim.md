# EXP-030 — Engine M v0.4 Prior-H1 Range Sweep/Reclaim

**Status:** CLOSED — ZERO-OUTCOME PREFLIGHT FREQUENCY FAIL  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-m-mtf-reclaim-limit-entry/SPEC-v0.4.md`

## Purpose

Replace v0.3's over-constrained local-sweep + midpoint conjunction with one coherent completed-H1 range setup while preserving non-chasing execution.

## Frozen center design

- H4/H1 directional alignment;
- M15 strict sweep/reclaim of H1_0 directional boundary;
- unchanged M5 rejection arm;
- unchanged 50% M5 retracement limit;
- unchanged structural stop;
- T40 must fit before opposite H1_0 boundary;
- unchanged signal-first safe-lot overlay.

## Preflight

Zero outcomes only.

Require >=25 filled valid signals per market, both directions, >=300 total, safety caps intact, protected periods sealed.

## Outcome state

- target/P&L outcomes: none;
- Jul-Aug: unopened;
- Sep: unopened.

## Next

Implement and run zero-outcome preflight only.


## Zero-outcome preflight outcome — FAIL

**Workflow run:** `36009110518`  
**Trigger SHA:** `809aef3f0824c788e5156146c8a820a1757afd22`  
**Durable result commit:** `fd9ae55`

Protection:

- target outcomes: **NO**;
- P&L outcomes: **NO**;
- Jul-Aug: unopened;
- Sep: unopened.

Result:

- filled valid signals: **237**;
- deployable signals: **237**;
- required total: >=300;
- 7/8 markets passed the >=25 + both-directions gate;
- GBPUSD: 19 signals, failed per-market count;
- safety overlay passed.

Per-market filled signals:

- XAUUSD 36;
- EURUSD 30;
- GBPUSD 19;
- USDJPY 32;
- EURJPY 30;
- AUDUSD 29;
- USDCAD 36;
- USDCHF 25.

Utility:

- GE40 8;
- GE30 21;
- LT30 208.

Structural diagnosis:

- v0.4 materially recovered opportunity density from v0.3 (237 vs 106);
- the opposite-H1-boundary target-room check rejected relatively few setups;
- the remaining scarcity comes primarily from requiring the sweep/reclaim specifically against only the latest completed H1 range.

**Disposition:** insufficient frequency. Do not calculate v0.4 outcomes.

### Next design implication

Do not lower the frozen preflight gate after seeing the count.

Prospectively broaden the same coherent H1-range idea by allowing the setup to use the **most recent qualifying range among the latest two completed H1 bars**, with deterministic preference for H1_0.

Keep the same >=300 total and >=25-per-market preflight gate in the next version.
