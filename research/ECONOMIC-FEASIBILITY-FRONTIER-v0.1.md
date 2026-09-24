# Economic Feasibility Frontier v0.1

**Date:** 2026-09-25  
**Status:** ROOT-CAUSE RESEARCH — NOT A STRATEGY BACKTEST  
**Reference equity:** USD500  
**Daily state:** stop adding risk at approximately -USD40 or +USD150  
**Purpose:** determine what payoff/skill levels would be required before changing position risk

## Model

This is an intentionally optimistic discrete-state model.

For a structural risk amount D and gross target multiple m:

- primary research cost = 10% of gross target;
- target outcome = `+0.9*m*D`;
- full-stop outcome = `-(1+0.1*m)*D`.

Assumptions:

- identical independent opportunities;
- no slippage/gaps beyond frozen primary cost;
- every opportunity can be filled;
- no common-factor correlation;
- no opportunity scarcity beyond the fixed maximum N;
- stop accepting new trades once realized P&L <= -USD40 or >= +USD150;
- otherwise continue until N opportunities are used.

Real trading is harder when outcomes are correlated, fills are worse, or qualified opportunities are absent.

## Per-trade break-even frontier

`p_break_even = (1 + 0.1m)/(1+m)`.

| Gross target | Net win at D=20 | Net full stop at D=20 | Break-even p |
|---|---:|---:|---:|
| 1.5R | +27 | -23 | 46.0% |
| 2.0R | +36 | -24 | 40.0% |
| 2.5R | +45 | -25 | 35.7% |
| 3.0R | +54 | -26 | 32.5% |
| 4.0R | +72 | -28 | 28.0% |

Break-even is not enough for the project objective. A strategy only slightly above these rates may be profitable but still incapable of producing frequent USD150 strong days.

## Exact sequential daily examples

### USD20 structural risk

| Target | Max opportunities | Hit p | Expected daily P&L | P(day >=100) | P(day >=150) | P(losing day) |
|---|---:|---:|---:|---:|---:|---:|
| 2.5R | 4 | 60% | +62.56 | 47.5% | 13.0% | 23.7% |
| 2.5R | 6 | 60% | +82.67 | 52.4% | 33.7% | 25.5% |
| 2.5R | 6 | 70% | +116.65 | 72.3% | 52.8% | 12.9% |
| 3.0R | 4 | 60% | +76.21 | 47.5% | 21.6% | 23.7% |
| 3.0R | 6 | 60% | +99.57 | 53.7% | 53.7% | 19.1% |
| 3.0R | 6 | 70% | +131.51 | 73.2% | 73.2% | 10.1% |

Even in this optimistic model, six independent 3R opportunities with a 60% hit rate produce expected daily P&L of only about USD100, not USD150.

A 60% hit rate at a genuine 3R payoff after costs is already an exceptionally strong trading edge.

### USD30 structural risk

| Target | Max opportunities | Hit p | Net win | Net stop | Expected daily P&L | P(day >=150) | P(losing day) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2.5R | 4 | 60% | +67.50 | -37.50 | +88.33 | 47.5% | 23.7% |
| 2.5R | 4 | 70% | +67.50 | -37.50 | +125.17 | 65.2% | 12.8% |
| 3.0R | 4 | 60% | +81.00 | -39.00 | +97.68 | 53.3% | 23.7% |
| 3.0R | 4 | 70% | +81.00 | -39.00 | +127.80 | 69.6% | 12.8% |

At D=30, one ordinary full stop nearly consumes the -USD40 normal daily stop-add-risk threshold.

### USD40 structural risk

At 3R:

- target outcome ~= +USD108;
- full stop ~= -USD52.

With at most three opportunities and p=60%:

- expected daily P&L ~= +USD80.96;
- P(day >=150) ~= 50.4%;
- losing-day probability ~= 40.0%.

With p=70%:

- expected daily P&L ~= +USD114.60;
- P(day >=150) ~= 63.7%;
- losing-day probability ~= 30.0%.

But a single full stop is already -USD52, beyond the normal -USD40 stop-adding-risk threshold and close to the -USD60 emergency ceiling.

## Four-trade arithmetic

If exactly four trades are available and no state stop interrupts them, the hit rate required to **average** USD150 is approximately:

| Structural risk | Target | Net win | Net stop | Required p for E[daily]=150 |
|---|---:|---:|---:|---:|
| 20 | 2.0R | +36 | -24 | impossible in four perfect wins to exceed 144 |
| 20 | 2.5R | +45 | -25 | 89.3% |
| 20 | 3.0R | +54 | -26 | 79.4% |
| 30 | 2.5R | +67.5 | -37.5 | 71.4% |
| 30 | 3.0R | +81 | -39 | 63.8% |
| 40 | 3.0R | +108 | -52 | 55.9% |

The lower required hit rate at D=40 is achieved by accepting a stop size that violates the normal daily risk architecture.

## Connection to actual repository results

Recent reference-account development results are nowhere near the skill/payoff frontier needed for routine USD150 days.

Examples:

- Engine Q v0.2: 251 reference-account trades, primary expectancy -USD1.53/trade, zero development weekdays >=USD100 or >=USD150;
- Engine P v0.1: 836 trades, negative expectancy; only about 3.5% of development weekdays >=USD100 and about 1.75% >=USD150;
- M/N/O similarly had negative expectancy and essentially no USD150 development days.

This is not fixed by scaling position size because the expected value is negative.

## Decision

1. Do not increase per-trade risk merely to make the USD150-200 arithmetic possible.
2. First establish a robust positive post-cost edge.
3. Then choose risk from a joint objective:
   - risk of ruin;
   - daily loss probability;
   - maximum drawdown;
   - margin;
   - correlation/common-factor exposure;
   - strong-day probability.
4. Retain USD150-200 as a **conditional strong-day zone**, not a required daily payout.
5. If the user ultimately requires USD150-200 as a routine expectation, the honest levers are:
   - materially more validated independent edge/opportunities;
   - larger account equity;
   - materially higher risk/drawdown tolerance;
   - or some combination.
   Position sizing alone cannot turn a weak/negative predictor into a sustainable earning system.
