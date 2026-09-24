# Multi-Timeframe Intraday Guidance

_Last updated: 2026-09-24_  
**Status:** DESIGN GUIDANCE — NOT A FROZEN TRADING RULE

## Why this note exists

User-provided trading examples repeatedly express a common discretionary workflow:

`higher timeframe -> direction/context`  
`middle timeframe -> setup/location`  
`lower timeframe -> execution`

The examples mention combinations such as:

- Daily / 4H / 1H for broader direction and important levels;
- 15m / 30m for intraday setup/location;
- 5m / 1m for entry execution.

Claims such as “15m is the best timeframe” are **not treated as evidence** and are not adopted literally.

The useful design principle is role separation between timeframes.

## Relevance to this project

Engine K made a completed 5m state do too many jobs:

- directional forecast;
- timing;
- immediate entry;
- stop placement.

Engine L v0.1 corrects the entry layer:

`5m forecast -> arm -> M1 pullback/resumption -> fresh stop`.

However, Engine L v0.1 still does not explicitly require a richer multi-timeframe context/location hierarchy before arming.

That is a plausible future design layer.

## Recommended intraday role hierarchy for research

Do **not** use every timeframe for the same purpose.

### 4H / 1H — context and directional regime

Potential causal information:

- higher-timeframe trend / slope;
- higher highs / higher lows versus lower highs / lower lows;
- distance to recent confirmed HTF swing levels;
- prior-day high / low;
- position inside recent 4H / 1H ranges;
- higher-timeframe volatility regime;
- whether current lower-timeframe forecast agrees with or opposes broader flow.

This layer should answer:

> Is LONG, SHORT, or neutral context more plausible here, and is price near a meaningful higher-timeframe location?

It should **not** directly trigger the trade.

### 15m — setup and location

Potential causal information:

- pullback versus expansion state;
- compression / range state;
- location within the current intraday swing/range;
- confirmed structure break / change only if defined exactly and causally;
- distance to 15m support/resistance/swing zones;
- whether price has reached a higher-timeframe area.

This layer should answer:

> Is there an intraday setup worth arming now?

### 5m — tactical forecast / arm

Engine-L-style role:

- score current directional opportunity;
- decide whether to arm LONG or SHORT;
- do not automatically enter.

### 1m — execution

Engine-L-style role:

- wait for favorable price interaction;
- require causal resumption/confirmation;
- derive fresh execution stop;
- fill only after confirmation;
- reject poor geometry/economics.

This layer answers:

> Is there a precise executable entry now?

## Practical candidate architecture

A future prospectively frozen version may follow:

```text
4H / 1H context
      ↓
15m setup + location
      ↓
5m directional arm
      ↓
1m pullback / confirmation
      ↓
fresh execution stop
      ↓
target-first economics
      ↓
cross-market ranking
```

## Important caution

Multi-timeframe analysis is useful only if each layer has a distinct causal purpose.

Adding many highly correlated indicators from many timeframes can make the model more complex without adding real information.

Therefore future MTF research should prefer a **small number of interpretable context variables** rather than hundreds of duplicated features.

## How to use this with Engine L

Do not mutate Engine L v0.1 after its zero-outcome mechanics checkpoint merely because this guidance was supplied.

Engine L v0.1 should first answer the clean question:

> Does forecast-armed pullback/resumption entry with a fresh stop materially outperform the matched immediate-entry control?

If v0.1 shows that execution quality helps but does not fully pass economics, the next prospective version should test an explicit MTF hierarchy using this note.

If v0.1 already passes robustly, MTF context is optional enhancement rather than a rescue requirement.

## Potential future matched experiment

A future Engine-L context experiment should compare, prospectively:

- **Control:** Engine-L entry mechanics without explicit MTF gating;
- **MTF version:** same entry mechanics, but 4H/1H context + 15m setup/location must support the arm.

Keep entry, stop, target, cost and sizing identical so the incremental value of MTF context can be measured.

## Relationship to daily target

Multi-timeframe context cannot guarantee a profitable trade every day.

Its intended value is to:

- avoid trading lower-timeframe noise against stronger context;
- improve location before arming;
- reduce low-quality entries;
- preserve enough multi-market opportunity by scanning all supported symbols;
- improve the probability that the few selected trades have sufficient target-first edge.

The daily USD150–200 objective remains an **opportunity-dependent portfolio goal**, not a quota that forces trades.
