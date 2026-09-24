# EXP-028 — Engine M v0.2 Signal-First Validation

**Status:** FROZEN PROSPECTIVELY — ZERO V0.2 OUTCOMES  
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
