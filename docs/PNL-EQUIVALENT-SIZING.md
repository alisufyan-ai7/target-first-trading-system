# P&L-Equivalent Sizing Method

_Last updated: 2026-09-23_  
**Status:** FROZEN BY EXP-014 PART B

## Purpose

Define the forward non-Gold economic-normalization method for the Target-First Trading System.

XAUUSD 0.10 lot remains the economic anchor. Other markets must **not** copy the 0.10-lot number.

The governing order is:

```text
validated engine candidate
    ->
freeze/use native target distance
    ->
calculate P&L-equivalent lot
    ->
structural-risk / margin / notional / daily-budget / correlation gates
    ->
USD 50 opportunity, justified USD 40/30 fallback, or reject
```

Target distance is chosen **before** position size. Never reverse the order merely to manufacture USD 50.

## Method selection

EXP-014 compared the two already-declared target-distance approaches conceptually against the repository evidence.

### Volatility-burden equivalence

**NOT THE FORWARD GOVERNING METHOD.**

EXP-006 showed that matching Gold's USD 5 move by equal fraction of hourly volatility produced approximately 3–4 pip FX targets and roughly 1.2–2.1 standard-lot-equivalent sizing for a USD 50 gross target.

That created severe notional/margin pressure for the approximately USD 500 reference account.

Keep volatility burden only as a diagnostic/context feature.

### Engine-conditioned native target

**SELECTED FORWARD METHOD.**

Native target distance must come from the validated engine/market behavior, not from a generic cross-market volatility conversion.

Two admissible forms exist.

#### A. Engine-defined structural target

Preferred when the engine naturally defines the destination, for example:

- opposing liquidity;
- session/range boundary;
- statistical mean;
- structural swing;
- predeclared continuation level.

The engine specification must freeze the target function before holdout inspection.

For candidate `c`:

`D_native(c) = absolute(target_price(c) - entry_price(c))`.

The target may vary by candidate if the engine's frozen target function is candidate-specific.

#### B. Engine-conditioned statistical target

Use only when the engine does not have a natural structural target.

The engine experiment must:

1. generate candidates and structural invalidations without using target outcomes;
2. on development data only, measure favorable excursion **before structural invalidation** with conservative same-bar handling;
3. predeclare a tick-aligned native-distance grid and target-selection criterion before validation/holdout;
4. calculate target-first hit rate and per-1-lot expectancy, including estimated costs where available, across the grid;
5. require stability across development subperiods / validation rather than selecting a single historical maximum;
6. freeze one normal native target distance `D_normal(engine, market)` before holdout;
7. run holdout unchanged.

A distance that only works at one isolated parameter point is not acceptable. Sensitivity around the frozen target must remain directionally stable.

## Equivalent-size calculation

For a linear-P&L instrument, define:

- `D` = frozen native target distance in price units;
- `V1` = USD P&L produced by a one-price-unit favorable move at **1.00 lot**, using contemporaneous conversion where required;
- `G1 = D x V1` = gross USD profit at 1.00 lot if the native target is reached.

Raw USD-50-equivalent size:

`lot_50_raw = 50 / G1`.

Then apply the broker lot step **downward**:

`lot_50 = floor_to_legal_step(lot_50_raw)`.

Do not round upward if doing so increases risk beyond the requested economic unit or a feasibility gate.

For instruments with nonlinear/inverse P&L, use the venue/broker's exact P&L function rather than the linear approximation.

## Currency conversion

For instruments whose P&L currency is not USD:

- convert target P&L and stop risk to USD using the contemporaneous conversion rate;
- freeze the conversion convention in the experiment/execution adapter;
- use broker-native tick value where reliable;
- do not assume a fixed USD pip value for JPY-quote or other non-USD-quote markets.

## Broker specification requirement

Before paper/live sizing, record for every symbol:

- contract size;
- tick size;
- tick value;
- P&L currency;
- minimum lot;
- maximum lot;
- lot step;
- margin formula;
- leverage tiers;
- commission;
- spread convention;
- swap/financing where relevant.

Research conventions cannot substitute for actual broker specifications at deployment.

## Feasibility gates

After calculating the proposed equivalent lot, calculate the real economics of the candidate using its unchanged structural stop.

At minimum record:

- native stop distance;
- structural-stop USD loss;
- gross target USD;
- estimated transaction costs;
- required margin;
- notional exposure;
- notional/equity;
- remaining normal daily-loss budget;
- aggregate open-stop risk;
- common-factor/correlation exposure;
- legal broker lot step/minimum/maximum.

The proposed size is executable only if all configured gates pass.

### Daily-loss rule

The approximately **USD 40 normal daily loss stop** is the sizing/risk budget.

The approximately **USD 60 emergency hard ceiling is not permission to size a new trade up to USD 60 risk**. It exists for exceptional slippage/gaps/operational overshoot.

At the start of a normal day, no new candidate may have structural-stop exposure exceeding the available normal loss budget.

Aggregate open-stop exposure must also fit the remaining normal daily-loss budget.

## USD 40 / USD 30 fallback

If the USD-50-equivalent size is unsafe:

### Same-target size fallback

Recalculate:

- `lot_40_raw = 40 / G1`;
- `lot_30_raw = 30 / G1`;

round downward and rerun **all** feasibility gates.

### Nearer-target fallback

A nearer native target may be used only if it was independently predeclared/validated for that engine/market and has materially stronger target-first evidence.

Do not invent a nearer target after seeing that USD 50 sizing is inconvenient.

If neither USD 40 nor USD 30 economics are validated and safe, reject the candidate.

## Continuation / runner economics

USD 70–100+ is allowed only under separately validated continuation/runner logic.

Do not enlarge initial lot size because a runner is possible.

Partials/runners must be declared by the engine/execution-management specification and evaluated after realistic costs.

## Gold anchor

XAUUSD remains the reference economic anchor:

- reference size: 0.10 lot;
- common research convention pending broker verification: 100 oz per 1.00 lot;
- USD 3 move ~= USD 30 gross;
- USD 4 ~= USD 40;
- USD 5 ~= USD 50;
- USD 7 ~= USD 70;
- USD 10 ~= USD 100.

Gold's 0.10-lot number is **not** copied to other symbols.

## Anti-distortion rules

Never:

- shrink a structural stop to fit a dollar budget;
- choose a tiny native target because it permits a larger lot;
- use same 0.10 lot across FX because Gold uses 0.10;
- use the emergency USD 60 ceiling as a normal risk allowance;
- increase size after a loss;
- martingale;
- use a different target-distance method on holdout because the first method performed poorly;
- select whichever feed gives the best sizing/result.

## Candidate-contract outputs

Before ranking/execution, every candidate should expose:

- engine ID/version;
- symbol;
- entry;
- structural stop;
- frozen native target / target function;
- native target distance;
- USD value per native unit at 1 lot;
- raw and rounded USD-50-equivalent lot;
- USD-40 and USD-30 fallback lots;
- structural-stop USD risk at each proposed size;
- margin/notional;
- target ladder in native units;
- estimated target-first probabilities;
- expected net USD value;
- daily-budget impact;
- correlation/common-factor impact;
- rejection/fallback reason.

## Holdout discipline

Sizing calibration is not allowed to consume holdout information.

The sequence is:

```text
engine rules frozen
    ->
development target-distance calibration
    ->
validation/sensitivity check
    ->
freeze D / target function
    ->
freeze broker-economics convention
    ->
holdout
    ->
independent-feed validation
    ->
paper/demo
```

## Relationship to EXP-015

This document freezes the **sizing methodology**, not a generic candidate generator.

EXP-015 remains a ranker of validated-engine candidates.

Actual non-Gold target distances and equivalent lots cannot be frozen globally until a specific reproducible engine/market pair has passed its own validation process.
