# Decision Log

## 2026-09-22 — Context isolation

**Decision:** Only the originating chat and `alisufyan-ai7/owner-target-first-trading-research` may be used as durable project context.

**Reason:** Other GitHub repositories and other chats belong to separate projects and must not contaminate this research.

## 2026-09-22 — GitHub as durable checkpoint

**Decision:** Material experiment conclusions must be written to GitHub before beginning another long-running computation.

**Reason:** Several long ChatGPT streaming runs timed out, making response recovery unreliable.

## 2026-09-22 — Do not force daily trade count

**Decision:** Treat 3–4 trades/day as an upper/typical opportunity objective, not a mandatory quota.

**Reason:** Lowering signal quality to meet a daily count would undermine expectancy and increase drawdown.

## 2026-09-22 — Target-first evaluation

**Decision:** Evaluate setups by whether the desired favorable move occurs before structural invalidation, not simply by directional correctness.

## 2026-09-22 — Engine A retained but not sufficient

**Decision:** Keep the Badar-inspired liquidity/MSS/FVG strategy as one candidate generator.

**Reason:** The first screen showed simplified positive expectancy but far too many low-output days.

## 2026-09-22 — Reject first Engine B/C formulations

**Decision:** Do not continue hand-tuning the initial breakout/retest and trend-pullback formulations merely to make them fit historical data.

**Next:** Test structurally different strategy families.
