# Working Risk Framework

_Last updated: 2026-09-22_

## Daily limits

- normal daily loss stop: approximately **-USD 40**;
- rare absolute hard stop: **-USD 60**;
- desired daily profit zone: approximately **+USD 150 to +USD 200**.

## Position sizing principle

### XAUUSD

Reference size: **0.10 lot**, subject to broker contract verification.

### Other markets

Use **P&L-equivalent sizing**, not identical lot size.

For a frozen native target distance, choose the lot size that would make that target approximately USD 50 gross:

`lot_size ~= 50 / (target_distance × USD value per distance unit at 1 lot)`.

This is the base economic conversion only.

The proposed size must then pass:

- structural-stop dollar-risk gate;
- margin gate;
- notional/leverage gate;
- remaining daily-loss-budget gate;
- correlated-exposure gate.

The project may accept a smaller safe size / USD 30–40 target when the USD-50-equivalent size is not feasible.

Do not enlarge size after losses.

## Important prior evidence

EXP-006 already demonstrated that volatility-normalized USD-50-equivalent FX sizing can require much larger lots than Gold's 0.10-lot reference.

That finding is not discarded. It is a warning that equivalent sizing must be paired with explicit execution-feasibility checks rather than replaced by an arbitrary same-lot rule.

## Structural stop

A valid structural/statistical invalidation remains mandatory.

Never compress a stop solely to fit a dollar amount.

For every proposed trade calculate:

- dollar loss if structural stop is hit;
- target dollar reward;
- reward/risk under the actual proposed size;
- margin required;
- aggregate open-stop exposure.

Reject any trade whose proposed equivalent size creates unacceptable risk.

## Profit management

Normal trade objective: about **USD 50**.

Allowed:

- approximately USD 30–40 when the validated near target is materially more reliable;
- USD 70–100+ when validated continuation/runner logic supports it.

Any partial/runner rule must be predeclared before holdout use.

## Aggregate portfolio gate

1. stop adding risk around -USD 40 realized daily P&L;
2. protect against breaching the -USD 60 emergency ceiling after including credible open-stop exposure;
3. control correlated simultaneous positions;
4. near +USD 150, normally stop adding new exposure unless a predeclared rule says otherwise;
5. never increase size to recover or accelerate the daily target.

## Small-account implication

At USD 500 reference equity, the stated daily limits are aggressive.

Before live deployment the system must verify:

- actual broker leverage and margin;
- liquidation/margin-call thresholds;
- spreads and commissions;
- slippage/gaps;
- drawdown and risk of ruin;
- simultaneous exposure.

No live promotion without independent-feed and forward/paper validation.
