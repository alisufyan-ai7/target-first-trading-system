# EXP-028 — Engine M v0.2 Signal-First Validation

**Status:** DEVELOPMENT RUNNER FROZEN — DEVELOPMENT OUTCOMES NEXT  
**Date:** 2026-09-24  
**Strategy:** `strategies/engine-m-mtf-reclaim-limit-entry/SPEC-v0.2.md`

## Purpose

Correct the research-layer ordering exposed by EXP-027.

EXP-027 showed that Engine-M mechanics generated 1,581 limit fills but the USD40-equivalent sizing gate rejected most FX fills because target-size lots exceeded the USD50k / USD100-margin reference-account envelope.

This does not prove the signals lack edge.

EXP-028 separates:

1. **signal validity** — does the MTF/limit setup have target-first edge?
2. **reference-account deployability** — what P&L can the frozen USD500 risk/margin envelope actually support?

## Strategy rules

Unchanged from Engine M v0.1.

No parameter is altered.

## Preflight

Zero-outcome only:

- >=50 mechanically filled valid signals per market;
- both directions every market;
- >=600 total;
- safe-lot overlay for each signal;
- Gold remains capped at 0.10 lot;
- no safety-cap violations;
- utility bands GE40 / GE30 / LT30 reported;
- Jul-Aug/Sep sealed.

## Development

If preflight passes:

- six fixed chronological development slices;
- size-invariant normalized-R signal metrics;
- separate USD500 safe-lot portfolio metrics;
- matched immediate-entry control.

## Protection

At freeze:

- v0.2 outcomes: none;
- Jul-Aug: unopened;
- Sep: unopened.

## Next

Implement the zero-outcome safe-lot/deployability preflight only.


## Zero-outcome preflight — PASS

**Workflow run:** `35997920091`  
**Trigger SHA:** `057871a772d384faa5af67b7e73089d3c2c9d730`  
**Durable result commit:** `68e52188de8abb2c708cacb611e347afb22a086d`

Protection:

- target outcomes: **NO**;
- P&L outcomes: **NO**;
- Jul-Aug secondary: **unopened**;
- Sep final holdout: **unopened**.

Result:

- total filled valid signal paths: **1,581**;
- safe-lot deployable paths >=0.01: **1,581**;
- every market >=50 signals: PASS;
- LONG and SHORT on every market: PASS;
- total >=600: PASS;
- safe overlay never violated USD20 risk / USD50k notional / USD100 margin: PASS.

Utility under the frozen USD500 reference account:

- GE40: **66**;
- GE30: **160**;
- LT30: **1,355**.

Per-market signal counts:

- XAUUSD 196;
- EURUSD 176;
- GBPUSD 212;
- USDJPY 193;
- EURJPY 193;
- AUDUSD 198;
- USDCAD 212;
- USDCHF 201.

All 1,581 are mechanically filled valid signals and all remain safely deployable at some >=0.01 lot size.

**Disposition:** PASS. EXP-028 may proceed to development outcomes while Jul-Aug and Sep remain sealed.


## Final pre-development reporting clarification

Daily USD100/USD150 reporting uses final realized UTC-day primary P&L, with all eligible weekdays including zero-trade days in the denominator. These are descriptive metrics, not pass gates.

No EXP-028 target/P&L outcome existed when this clarification was frozen.


## Development implementation checkpoint — zero outcomes

Frozen before EXP-028 development outcomes:

- six fixed evaluation slices;
- size-invariant normalized-R signal layer;
- separate safe-lot USD500 reference-account portfolio;
- matched immediate-entry control on the same MTF arms;
- one-open portfolio ranking by achievable gross target, then lower stop risk;
- daily stop-adding-risk rules;
- end-of-day USD100/USD150 reporting definition;
- per-market normalized-R diagnostics;
- strict Jul1 seal.

Implementation commits:

- development runner: `033c870660e7a1d58ac7905cc78e107dd4f1aec0`;
- development workflow: `526cdb2234da7f07e23196b60ee0c82b4118a792`;
- per-market reporting hardening: `619e3d3d02bd80ed7182a3ee68b96f18887c64d5`.

At this checkpoint:

- EXP-028 target outcomes: **NO**;
- EXP-028 P&L outcomes: **NO**;
- Jul-Aug loaded/labeled: **NO**;
- Sep loaded/labeled: **NO**.

### Next

Trigger EXP-028 development only. Fail any mandatory development gate -> stop before secondary.
