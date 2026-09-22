# Badar Tanveer Video Evidence Dossier

_Last updated: 2026-09-22_

This document preserves the project-authorized findings from the supplied Facebook clips and the public Badar Tanveer material analyzed in the originating chat.

## Evidence standard

- **OBSERVED**: directly visible in an uploaded clip/chart or explicitly stated in analyzed material.
- **REPEATED PATTERN**: observed across multiple examples/material.
- **HYPOTHESIS**: plausible rule requiring quantitative validation.

## Uploaded Gold buy example

**OBSERVED**

The supplied clip showed approximately:

~~~text
5:38 PM  Be ready for a trade
5:42 PM  Buy gold now
          SL 4276
5:42 PM  Entry price 4279.800
TP1      4286
Later    around 4291 / TP2 / profit booking
~~~

Implications:

- stop was specified immediately;
- exact entry was specified;
- the execution chart was on a low timeframe, around 1m in this example;
- profit was managed in stages;
- this trade was not simply held as an all-or-nothing 1:9 position.

Approximate visible economics:

- entry 4279.800;
- stop 4276.000;
- risk distance about USD 3.80 Gold;
- TP1 4286, about USD 6.20 favorable, roughly 1.6R;
- around 4291, about USD 11.20 favorable, roughly 3R.

## Uploaded high-R short example

**OBSERVED**

Another screenshot showed approximately:

~~~text
SELL   4292.741
SL     4295.825
TARGET 4264.815
~~~

Approximate distances:

- risk: 3.084;
- reward: 27.926;
- reward/risk: approximately 9.06R.

This supports that some opportunities can genuinely be large-R, but 1:9 is not a fixed target for every trade.

## Explicit sweep -> MSS -> FVG clip

**OBSERVED**

A supplied Facebook clip explicitly annotated:

~~~text
liquidity sweep
      ->
MSS
      ->
FVG
      ->
short position
~~~

Observed details:

1. several similar highs / buy-side liquidity were visible;
2. price traded above the marked liquidity and rejected;
3. the MSS line was below an **internal** local swing low, not necessarily the major low of the entire preceding move;
4. bearish displacement broke that internal structure;
5. the displacement created/left a bearish FVG;
6. the short tool was applied after confirmation, around the retracement/FVG area rather than at the first sweep wick.

This is the strongest direct evidence for the original Engine A causal order.

## Working bearish model

**REPEATED PATTERN / HYPOTHESIS built from observed evidence**

~~~text
important location / buy-side liquidity
            ->
liquidity sweep and rejection
            ->
identify internal swing low
            ->
candle close / MSS below internal structure
            ->
bearish displacement
            ->
bearish FVG
            ->
retracement into entry area
            ->
short
            ->
structural invalidation / tight stop
            ->
partials + opposing-liquidity / continuation target
~~~

Bullish logic is mirrored.

## BOS versus MSS

The wider public teaching uses both BOS and MSS.

Project interpretation:

- higher-timeframe BOS/structure helps establish context or validate a POI/order block;
- lower-timeframe MSS is the execution confirmation after a liquidity event.

This remains a hypothesis until more examples are mechanically catalogued.

## Timeframes

Evidence supported:

- larger-timeframe context/map;
- 5m structure/liquidity;
- 3m/1m lower-timeframe refinement and execution.

Do not interpret “15m context” or “5m context” as one previous candle.

See docs/TIMEFRAME-AND-MARKET-CONTEXT.md.

## FVG selection

Public material distinguishes between correct/incorrect FVGs rather than treating every three-candle gap as tradable.

Working hypothesis:

~~~text
valid FVG =
created by meaningful displacement
AND associated with structure change
AND follows a relevant liquidity event / location
~~~

The exact FVG entry percentage is not established.

Variants to test independently include edge, midpoint/50%, deeper fill, and penetration plus confirmation.

## Stops

Evidence suggests stops are structural, often tight, and can produce large R multiples.

Unresolved possibilities include:

- beyond the swept liquidity high/low;
- beyond retracement swing;
- beyond FVG/invalidation plus buffer.

The “30–35 pips average stop” promotional language should not be encoded as a universal fixed stop.

## Targets and management

- partial TP occurs;
- not every trade targets 1:9;
- some setups/runners can be much larger;
- opposing liquidity and remaining structural room appear relevant.

Reward/risk should usually be an **output** of entry + structural stop + available target path, not a fixed number imposed first.

## Volume / VSA / open interest

Later public material discusses VSA, volume, and open interest.

However, the explicit supplied sweep -> MSS -> FVG clip did not require a volume condition.

Project treatment:

- core Engine A begins as price/liquidity structure;
- volume/VSA/open-interest may be tested as optional context/filter layers;
- do not make them mandatory without direct evidence and validation.

## Failed FVG / secondary entry

Public material discussed failed/inverse FVG concepts and opportunities after missing an initial FVG.

Possible future branches:

~~~text
primary:
sweep -> MSS -> displacement -> fresh FVG -> retracement

secondary:
missed / failed FVG
    -> structure still valid?
    -> IFVG / secondary POI / re-entry
~~~

These branches are not part of the recovered EXP-002 implementation unless explicitly proven.

## Sessions / news / DXY

Public material repeatedly emphasizes London/New York trading, news awareness, and sometimes DXY/fundamental context.

A later system may use these as context filters, but the exact mandatory rules are not yet frozen.

## Promotional probability correction

The claim that 1:9 reward/risk means 10% loss probability and 90% profit probability is mathematically false.

Reward/risk describes payoff size, not win probability.

## Remaining unknowns

- exact liquidity-quality definition;
- equal-high/low tolerance;
- required sweep depth;
- wick vs close conditions;
- exact internal pivot selection;
- minimum displacement;
- exact FVG selection and entry percentage;
- exact stop formula;
- exact target-selection rule;
- mandatory versus optional role of volume;
- news/session exceptions;
- skipped-trade logic.
