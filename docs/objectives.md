# System Objectives

_Last updated: 2026-09-22_

## Primary objective

Build a multi-market trading system that continuously scans supported liquid markets, receives candidates from validated strategy engines, ranks target-first opportunities, and works toward a relatively consistent **USD 150–200 daily net P&L zone** without forcing trades or unsafe sizing.

Research is the validation layer; the end objective is an operating system.

## Economic anchor

### XAUUSD

Reference size: **0.10 lot**.

Under the common illustrative 100-oz/lot convention:

- USD 3 Gold move ~= USD 30 gross;
- USD 4 ~= USD 40;
- USD 5 ~= USD 50;
- USD 7 ~= USD 70;
- USD 10 ~= USD 100.

### Other markets

Do not copy the 0.10-lot number.

Freeze a native target distance first and calculate a symbol-specific P&L-equivalent lot size for approximately USD 50 gross.

The proposed size must then pass:

- structural-stop dollar risk;
- margin;
- notional/leverage;
- remaining daily budget;
- correlated exposure.

If unsafe, use a justified smaller USD 30–40 opportunity or reject it.

## Profit flexibility

Normal successful-trade objective: about USD 50.

Permitted when validated:

- USD 30–40 nearer capture;
- USD 70–100+ continuation/runner.

Do not increase size after losses.

## Opportunity-driven trade count

- roughly 3–4 qualified trades/day is a desirable normal range, not a quota;
- zero forced minimum;
- more than four may occur if independent validated opportunities exist and aggregate risk remains safe;
- never lower quality because the day is below target.

## Daily objective

- desired net zone: approximately USD 150–200 when sufficient opportunity exists;
- normal daily loss stop: approximately -USD 40;
- rare hard ceiling: approximately -USD 60.

These are objectives, not promised outcomes.

## Consistency objective

Low-output day = net daily P&L <= USD 50.

Working preference: drive low-output days toward roughly 20% or less **if evidence and risk permit**.

The system should prefer a smoother profile such as:

~~~text
+170 +125 +190 +50 +160
~~~

over a highly concentrated profile such as:

~~~text
0 0 +600 0 +55
~~~

even if long-run averages are similar.

## Required acceptance metrics

- T30/T40/T50/T70/T100 target-first probability;
- expectancy after realistic costs;
- probability calibration;
- structural-stop risk at proposed size;
- margin/notional feasibility;
- mean and median daily P&L;
- <= USD 50 day percentage;
- >= USD 100 / 150 / 200 day percentages;
- losing-day percentage;
- 5-day rolling P&L distribution;
- maximum drawdown;
- consecutive losing days;
- consecutive low-output days;
- trades/day including zero-signal days;
- opportunity concentration;
- simultaneous-signal/common-factor correlation;
- realized capture versus MFE.

## Engine A preservation rule

Original EXP-002 XAUUSD Engine A remains an active positive-simplified-expectancy lead.

Engine A v0.2-portable is a separate rewrite and cannot substitute for it.

Recover and reproduce EXP-002 before broad ranker optimization.

## Non-goals

Do not:

- force a trade count;
- force USD 50 when only USD 30–40 is validated;
- manufacture USD 50 with unsafe leverage;
- hide zero/loss days;
- martingale;
- increase size after losses;
- assume reward/risk implies probability;
- present probabilistic signals as certain;
- let a generic ML ranker silently replace validated setup engines.
