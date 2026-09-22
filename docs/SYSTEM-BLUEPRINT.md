# System Blueprint

_Last updated: 2026-09-22_

## Identity

This project is building a **trading system**. Research, backtesting, video analysis, statistics, and machine learning are validation and selection layers used to build that system; they are not the end product.

## Operational objective

Build a multi-strategy, multi-market system that continuously scans supported liquid markets, identifies the best qualified opportunities, sizes them economically, controls portfolio risk, and works toward approximately **USD 150–200 net on days with sufficient validated opportunity**.

Reference account: approximately USD 500.

Normal successful-trade objective: approximately USD 50, with validated flexibility around USD 30–40 for nearer/high-confidence targets and USD 70–100+ for continuation/runners.

No daily profit is guaranteed.

## Architecture

~~~text
MARKET / NEWS / SESSION DATA
          |
          v
MULTI-MARKET SCANNER
          |
          v
VALIDATED STRATEGY ENGINES
          |
          v
STANDARDIZED CANDIDATE CONTRACT
          |
          v
TARGET-FIRST LABEL / PROBABILITY LAYER
          |
          v
EQUIVALENT POSITION SIZING
          |
          v
FEASIBILITY GATES
  structural risk / margin / leverage
  daily budget / correlation
          |
          v
CROSS-MARKET OPPORTUNITY RANKER
          |
          v
EXECUTION + TRADE MANAGEMENT
          |
          v
DAILY P&L STATE MACHINE
          |
          v
JOURNAL / LEDGER / PERFORMANCE DATABASE
          |
          v
FORWARD VALIDATION -> SEMI-AUTO -> FULL AUTO
~~~

## Critical architecture rule: engines generate candidates

The probability/ranking layer sits **after** validated setup engines.

Default architecture:

~~~text
validated engine -> meaningful candidate -> probability/ranking model
~~~

Do not silently replace this with:

~~~text
every generic pivot / every bar -> ML decides whether to trade
~~~

A broad statistical candidate generator may be researched separately, but it must itself pass an explicit validation gate before being allowed to replace or bypass strategy engines.

## Candidate contract

Every strategy engine should eventually emit a common candidate object containing at minimum:

- engine ID/version;
- market/symbol;
- long/short direction;
- candidate/entry timestamp;
- entry logic;
- structural invalidation / stop;
- native target ladder;
- context/features;
- session and market regime;
- data-source/version metadata.

See docs/STRATEGY-ENGINE-CONTRACT.md.

## Target-first decision principle

The system is not trying only to predict direction.

For each candidate it asks:

> From this exact entry and structural invalidation, what useful favorable move is likely to happen first, and is this opportunity better than the alternatives currently available?

Required outputs eventually include probability/EV for USD 30 / 40 / 50 / 70 / 100+ profit rungs before invalidation.

## Economic normalization

### XAUUSD

Reference execution size: 0.10 lot, subject to broker contract verification.

Under the common 100-oz/lot convention:

- USD 3 Gold move ~= USD 30 gross;
- USD 4 ~= USD 40;
- USD 5 ~= USD 50;
- USD 7 ~= USD 70;
- USD 10 ~= USD 100.

### Other markets

Do not copy the 0.10-lot number.

Freeze a native target distance first, then calculate a symbol-specific economically equivalent lot size for approximately USD 50 gross.

That proposed size must then pass risk, margin, notional, leverage, daily-budget, and correlation gates. If it is unsafe, use a justified smaller USD 30–40 opportunity or reject the trade.

## Daily state philosophy

The daily target is a stopping/selection state, not a quota.

Illustrative behavior:

- around +USD 50: continue only for qualified opportunities;
- around +USD 100: continue only for qualified opportunities;
- around +USD 150–200: normally stop adding exposure;
- around -USD 30: become materially more selective;
- around -USD 40: normally stop adding risk;
- -USD 60: emergency hard ceiling.

Never manufacture a trade because the day is below target.

## Portfolio exposure

Signals can be economically correlated even when symbols differ.

Example: long EURUSD, long GBPUSD, short USDJPY, and long Gold may all express USD weakness.

The system therefore needs common-factor/correlation exposure controls in addition to per-trade stop risk.

## Consistency objective

The system should be evaluated on the **shape of daily outcomes**, not only aggregate return.

Important metrics:

- median daily P&L;
- average daily P&L;
- percentage of days <= USD 50;
- percentage >= USD 100 / 150 / 200;
- losing-day frequency;
- consecutive low-output days;
- consecutive losing days;
- 5-day rolling P&L consistency;
- drawdown;
- trades/day including zero-signal days.

A pattern such as 0 / 0 / +600 / 0 / +55 is not equivalent to a smoother pattern such as +170 / +125 / +190 / +50 / +160 even if longer-run averages are similar.

## Current gate

Before broad scanner/ranker development resumes:

1. recover the original EXP-002 Gold Engine A as faithfully as possible;
2. reproduce its recorded behavior within reasonable tolerance;
3. freeze correct P&L-equivalent sizing for non-Gold markets;
4. define the common strategy-engine candidate contract;
5. only then restart target-first ranker work.
