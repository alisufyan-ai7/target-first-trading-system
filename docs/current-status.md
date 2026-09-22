# Current Status

**Date:** 2026-09-22  
**Phase:** Knowledge recovery / economic-sizing correction before further development

## Source of truth

Authorized project context now includes:

1. this current chat;
2. the explicitly reintroduced prior chat in this same project to the extent its findings are durably recorded/recoverable here;
3. this repository.

No unrelated chats, projects, memories, or repositories may be used.

## User objective — corrected

Build a multi-market scanner/execution system that works toward approximately USD 150–200 net on days with sufficient qualified opportunity.

Normal successful-trade objective: about USD 50.

Allowed flexibility:

- approximately USD 30–40 when the nearer target has materially stronger target-first probability;
- USD 70–100+ when validated continuation evidence supports it.

No forced trade quota.

## Correct sizing interpretation

### XAUUSD

Reference size = **0.10 lot**.

### Other markets

Do **not** use 0.10 lot automatically.

Calculate an economically equivalent lot size so that the market's frozen native target distance is worth approximately USD 50.

Equivalent sizing must then pass structural-stop risk, margin, leverage/notional, correlation, and daily-loss-budget gates.

If the full USD-50-equivalent size is unsafe, use a justified smaller USD 30–40 objective or reject the trade.

## Original Engine A / Gold — retained positive lead

EXP-002 is the original Badar-inspired Gold screen derived from the prior project's video/chart work.

Recorded results:

- 372 signals overall;
- overall USD 5 target-first hit rate: 29.6%;
- average structural risk distance: about USD 1.02 Gold;
- median favorable excursion: about USD 3.30 Gold;
- average simplified expectancy: about **+USD 0.79 Gold/trade before costs**.

Development:

- ~185 trades;
- USD 5 hit: 31.9%;
- simplified expectancy: about **+USD 0.85 Gold/trade**.

Holdout:

- ~187 trades;
- USD 5 hit: 27.3%;
- simplified expectancy: about **+USD 0.72 Gold/trade**;
- target-first sensitivity:
  - USD 2: 48.7%;
  - USD 3: 41.7%;
  - USD 4: 31.6%;
  - USD 5: 27.3%.

At the illustrative 0.10-lot/10-oz convention, +0.72 Gold/trade is roughly +USD 7.20/trade gross simplified expectancy before costs.

**Status:** retain the original EXP-002 Gold Engine A as an active research lead.

## Critical Engine A distinction

Engine A v0.2-portable, used later in EXP-007/012, is **not the same implementation** as EXP-002.

Its own specification states that it was a prospective reconstruction because exact mechanics from EXP-002 were not fully preserved.

Therefore:

- v0.2's poor Gold results do not invalidate EXP-002;
- v0.2 remains useful as a separate failed/limited implementation record;
- original Engine A recovery must precede further conclusions about the Badar-inspired Gold lead.

## Sizing evidence already available

EXP-006 performed a first P&L-equivalent calculation using a volatility-normalized target burden.

Illustrative USD-50 sizes from that method were approximately:

- EURUSD: 1.608 standard lots;
- GBPUSD: 1.163 standard lots;
- USDJPY: 2.146 standard lots.

Those values were rejected previously because of margin/notional pressure, not because the conversion math was invalid.

Under the corrected objective, EXP-006 becomes useful again as a sizing diagnostic. The next sizing method must preserve the USD-50 equivalence idea while enforcing explicit feasibility gates.

## Misframed later branch

EXP-012 and EXP-013 contain useful Gold and volatility diagnostics, but their FX conclusions based on using **0.10 lot on FX** do not represent the user's intended cross-market sizing rule.

Those same-lot FX results are preserved as diagnostics only and must not drive the next scanner universe.

## Immediate plan

No new strategy optimization should begin yet.

First:

1. recover/reconstruct the original EXP-002 Engine A mechanics from the durable video-derived sequence and recorded parameters;
2. require the recovered implementation to reproduce EXP-002 Gold behavior within reasonable tolerance before using it elsewhere;
3. define a prospective P&L-equivalent lot-sizing rule for non-Gold symbols with ~USD 50 normal target and USD 30–40 fallback;
4. apply hard structural-risk/margin/notional gates;
5. only then resume cross-market scanning/ranking.

## Key unresolved question

Can the original positive Gold Engine A be faithfully reproduced and then combined with P&L-equivalent cross-market sizing to create enough qualified USD 30–100 opportunities to approach the USD 150–200 daily objective without unacceptable risk?
