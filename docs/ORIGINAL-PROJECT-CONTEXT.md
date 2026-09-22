# Original Project Context

_Last updated: 2026-09-22_

This document preserves the important design context from the originating project conversation so future chats do not reduce the project to a collection of backtests.

## What the user is trying to build

The desired end product is an automated or semi-automated system that can scan multiple markets continuously and take high-quality trades where the expected attainable move is economically useful.

The original mental model was expressed in Gold terms:

- Gold reference size: 0.10 lot;
- look for trades where Gold has a credible path to at least about a USD 5 move;
- a USD 5 Gold move at the common 0.10-lot/10-oz convention is about USD 50 gross;
- ideally find enough qualified opportunities across the day to work toward USD 150–200.

The project then generalized this to other markets:

- do not use 0.10 lot universally;
- determine the market's native target distance;
- calculate the equivalent lot size needed to make a normal successful move economically comparable to the Gold USD 50 unit;
- reject or downsize unsafe sizing.

## Daily consistency preference

The user explicitly does not want aggregate profitability driven by a few huge days with many zero days.

The desired profile is closer to:

~~~text
+170
+125
+190
 +50
+160
~~~

than:

~~~text
   0
   0
+600
   0
 +55
~~~

Therefore low-output-day frequency and rolling consistency are first-class design metrics.

Working preference:

- low-output day = net P&L <= USD 50;
- ideally such days occur around once per five-day week, roughly <=20%;
- this is an aspirational research target, not an assumed achievable fact.

## Trade count

The conversation initially used 3–4 trades/day as a practical reference.

The durable interpretation is:

- 3–4 qualified trades/day is a desirable normal opportunity range;
- there is no forced minimum;
- do not lower quality because fewer trades appeared;
- more than four may be acceptable if several independent qualified smaller-target opportunities exist and aggregate risk remains safe.

## Risk

Working framework:

- normal daily loss stop around -USD 40;
- rare absolute hard ceiling around -USD 60;
- no martingale;
- no doubling after losses;
- no recovery trades;
- no stop compression merely to fit a dollar budget.

The structural stop comes first. Size must adapt or the trade must be rejected.

## Badar's role

Badar Tanveer's public examples were not adopted as the final system.

They provided the first candidate engine and several useful execution concepts:

- liquidity;
- sweep;
- internal MSS;
- displacement;
- FVG;
- retracement entry;
- structural invalidation;
- partial profits;
- variable large-R continuation.

The end system is free to use other independently validated engines.

## “Sure” does not mean certainty

The user described wanting entries where the market is “sure” to move the required distance.

Operationally this means:

- high enough validated target-first probability;
- positive expected value after realistic costs;
- clear structural room;
- acceptable risk and execution feasibility.

No market move is certain.

## Gold-first, not Gold-only

Gold was used as the economic anchor because 0.10 lot maps USD 3–10 price movement naturally to roughly USD 30–100 gross under the common contract convention.

The system should still search metals, FX, indices, and eventually crypto where data, contract economics, and validated strategy engines justify inclusion.

## Development philosophy

The project should move through:

historical detector/backtest -> out-of-sample validation -> independent-feed validation -> live paper/demo scanner -> signal-only mode -> human-approval/semi-auto mode -> full automation only after evidence.

## Non-negotiable design principle

Increase the **opportunity universe**, not the willingness to accept poor trades.
