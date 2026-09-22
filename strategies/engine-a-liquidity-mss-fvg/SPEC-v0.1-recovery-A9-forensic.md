# Engine A Original Recovery — Variant A9 Forensic Fill-Bar Diagnostic

**Status:** FROZEN BEFORE OUTCOME INSPECTION — FORENSIC / NON-DEPLOYABLE  
**Version:** 0.1-recovery-A9-forensic  
**Frozen:** 2026-09-23  
**Experiment:** EXP-014 Part A

## Purpose

A9 is a forensic sibling of the A6 recovery baseline.

A6 is the closest causal recovery branch so far on signal frequency, development/holdout balance, and average structural risk, but 163 of its 333 accepted trades are stopped on the midpoint fill bar under conservative same-bar handling.

A9 tests one implementation ambiguity only:

> Did the original exploratory EXP-002 bar-based backtest effectively begin stop/target evaluation on the minute **after** a midpoint fill, rather than treating a stop also touched inside the fill bar as an immediate loss?

This is explicitly an optimistic historical-backtest diagnostic. It is not admissible for live or production validation.

## Inherited baseline

A9 inherits **all A6 mechanics unchanged**, including:

- reusable latest 5m liquidity level;
- 1-left/1-right confirmed 5m pivot;
- 24-bar age convention used by the validated A6 runner;
- 5m wick sweep + close back inside;
- 12-minute confirmed internal 1m pivot;
- first MSS within 10 completed 1m bars after the completed sweep bar;
- displacement on the MSS candle or either of the next two bars;
- displacement >= 1.6x prior-20 mean absolute 1m body;
- first same-direction FVG on displacement or either of the next two bars;
- exact FVG midpoint entry;
- 10-bar fill expiry;
- A3 proportional FVG invalidation: stop buffer = 25% of selected FVG width;
- one-open-trade policy;
- USD 5 primary target;
- 120-bar / 20:00 UTC maximum horizon;
- T2/T3/T4/T5 labels;
- no costs in the historical reproduction comparison.

Reference baseline:

- `strategies/engine-a-liquidity-mss-fvg/SPEC-v0.1-recovery-A6.md`.

## A9 single forensic change: fill-bar stop handling

The fill bar is used only to determine whether the FVG midpoint was touched and therefore whether the limit entry filled.

After that fill is declared:

- **do not evaluate the structural stop on the fill bar**;
- **do not evaluate any profit target on the fill bar**;
- record fill-bar MFE as zero;
- begin both stop and target evaluation with the **next completed 1m bar**.

After the fill bar, same-bar target/stop ambiguity remains conservative: if stop and a target are both touched in the same later 1m bar, stop wins.

No other rule changes.

## Why this is forensic

OHLC data do not reveal whether, inside the fill minute, the stop-side extreme occurred before or after the midpoint entry.

Ignoring the fill-bar stop is therefore optimistic. Even if A9 reproduces EXP-002, it cannot become the deployable recovered Engine A. Instead, such a result would be evidence that the original exploratory screen may have benefited from intrabar ordering bias.

## Reproduction decision

A9 is still compared to the frozen EXP-014 benchmark vector, but interpretation differs:

- if A9 fails, optimistic fill-bar ordering does not explain EXP-002;
- if A9 materially reproduces EXP-002, treat that as evidence of historical backtest bias, **not** as validation of a live strategy;
- in no case may A9 be promoted to production or used to relax the project's conservative same-bar rule.

No A9 outcome may be calculated before this specification is committed.
