# Formal Decision Policy — Badar Current-Era v0.1

## 1. Policy scope

This policy formalizes the human decision hierarchy reconstructed from 42 current-era live streams.

It is **outcome blind**.

It is evaluated at a candidate decision timestamp using only information available at that timestamp.

The policy is deliberately ordered. Earlier rules take precedence over later ones.

## 2. Candidate evaluation model

Evaluate a LONG candidate and a SHORT candidate separately.

A candidate consists of:

- proposed direction;
- current environment;
- HTF context;
- candidate location;
- observed interaction;
- decision evidence / confirmation state;
- execution feasibility;
- structural invalidation;
- quality modifiers.

If neither candidate is eligible, output `WAIT` or `NO_TRADE` according to the rules below.

If both directions appear simultaneously eligible but the evidence does not clearly privilege one side, output `WAIT`. Do not resolve ambiguity by inventing a tie-breaker.

---

# PRE-ENTRY POLICY

## Rule P0 — external risk lock

If the account/session risk layer is locked, output:

`NO_TRADE`

Examples of a lock include a frozen daily-loss stop, explicit end-of-session stop, or other independent Target-First risk control.

Badar's exact historical daily trade count is not copied into this rule.

## Rule P1 — market interpretability

If current price action is explicitly classified as `UNINTERPRETABLE` because of abnormal/news/server/manipulation conditions and no source-supported execution branch is active:

`WAIT`

Do not turn news itself into a universal veto. Current-era evidence contains both stand-aside and news-trading behavior.

## Rule P2 — meaningful location

Location state is evaluated before trigger state.

### P2a — absent / middle / wrong extreme

If:

- `location_state = ABSENT`; or
- `location_state = MIDDLE`; or
- `location_state = WRONG_EXTREME`

then:

`NO_TRADE`

This prevents lower-timeframe patterns from manufacturing a trade where location is poor.

### P2b — approaching / unresolved

If:

- `location_state = APPROACHING`; or
- `location_state = UNRESOLVED`

then:

`WAIT`

### P2c — valid

Only `location_state = VALID` may continue.

## Rule P3 — late / chasing gate

If the intended entry has already left the planned execution area:

- if a source-consistent retracement/retest path still exists -> `WAIT`;
- otherwise -> `NO_TRADE`.

Never convert a missed entry into a market chase.

## Rule P4 — HTF close gate

### P4a — invalidation

If the relevant M15/M30/H1/H4 close has explicitly invalidated the candidate:

`NO_TRADE`

### P4b — required close pending

If the trade plan explicitly requires a higher-timeframe close and that close is still pending:

`WAIT`

### P4c — bias flip

If the newest HTF close flips the active directional case:

`WAIT` and rebuild the candidate from the new context.

Do not inherit the old candidate through a bias flip.

## Rule P5 — structural invalidation feasibility

Every trade must define where the idea is wrong **before entry**.

### P5a — undefined invalidation

If `stop_state = UNDEFINED`:

`NO_TRADE`

### P5b — unacceptable stop

If `stop_state = TOO_LARGE_FOR_THIS_SETUP`:

`NO_TRADE`

### P5c — acceptable large stop

If `stop_state = DEFINED_LARGE_BUT_SIZABLE`:

the candidate may continue, but maximum risk class is `REDUCED`.

### P5d — normal structural stop

If `stop_state = DEFINED_ACCEPTABLE`:

continue.

The exact pip threshold separating these states is **not frozen in v0.1**.

## Rule P6 — interaction state

Interaction is not universally a sweep.

Recognized source-supported interaction families are:

- sweep;
- fake break / close back;
- trap;
- retrace to POI;
- rejection;
- continuation retest;
- range-extreme test;
- repeated / second reaction.

If the planned interaction is explicitly required but has not happened yet:

`WAIT`

If the candidate is a continuation/direct-POI setup where no extra interaction was required by the source logic, continue to P7.

## Rule P7 — decision-evidence branch

There are two legal branches.

---

## Branch A — confirmation-based execution

Use Branch A when `confirmation_state` is not `NONE`.

### A1 — failed

If `confirmation_state = FAILED`:

`NO_TRADE`

### A2 — not yet

If `confirmation_state = NOT_YET`:

`WAIT`

### A3 — strong / adequate

If `confirmation_state = STRONG` or `ADEQUATE`:

candidate is execution-eligible and proceeds to risk classification.

Recognized confirmation families include:

- momentum / MSS;
- inverse close;
- close-back-inside;
- two-candle rejection;
- engulfing / strong opposing close;
- wickless momentum close;
- mini-range break;
- OB/FVG retrace after a confirming move;
- double confirmation.

No single family is privileged universally.

### A4 — weak confirmation

A `WEAK` confirmation may not produce a normal-risk trade.

It is eligible only when all are true:

1. location is `VALID`;
2. structural invalidation is `DEFINED_ACCEPTABLE`;
3. entry is not chasing;
4. HTF state is not invalidating;
5. the trade is explicitly treated as a test / low-probability / reduced-risk idea.

If those conditions are not all satisfied:

`WAIT` or `NO_TRADE` according to the earlier failed gate.

If they are satisfied:

maximum risk class = `REDUCED`.

---

## Branch B — direct / aggressive execution

Branch B exists because 20/107 captured trades had no separately coded confirmation family.

It is **not** a general exception.

A direct candidate is eligible only if all are true:

1. `location_state = VALID`;
2. `interaction_family` is either:
   - `SWEEP`; or
   - `RETRACE_TO_POI`;
3. `stop_state` is defined and not `TOO_LARGE_FOR_THIS_SETUP`;
4. entry is not chasing;
5. no relevant HTF close invalidates the candidate;
6. the entry is pre-planned or tied to a clearly identified structural location;
7. the direct-entry reason can be written before entry without referring to future movement.

If any item fails:

`WAIT` or `NO_TRADE` according to the failed gate.

### B1 — direct normal-risk eligibility

A Branch-B trade may be `NORMAL` only when:

- directional context is `ALIGNED`;
- stop state is `DEFINED_ACCEPTABLE`;
- there is no active downgrade modifier;
- location is a pre-identified structural POI / extreme;
- interaction is already complete.

Otherwise Branch B is `REDUCED`.

This keeps the direct branch narrow and prevents “no confirmation” from becoming unrestricted discretion.

---

## Rule P8 — target-path feasibility

If there is an obvious opposing barrier before any plausible first objective and the trade has no source-supported scalp target before that barrier:

`NO_TRADE`

If target-path feasibility is unresolved:

maximum risk class = `REDUCED`.

No universal numeric RR floor is frozen in v0.1.

## Rule P9 — risk classification

After all eligibility gates pass:

### NORMAL

`NORMAL` is allowed only when no downgrade modifier is active.

Typical NORMAL profile:

- direction aligned or clearly supported;
- valid location;
- strong/adequate evidence, or qualified Branch-B direct entry;
- normal market conditions;
- acceptable structural stop;
- no unresolved contradiction.

### REDUCED

Any of the following caps the trade at `REDUCED`:

- countertrend;
- active/recent major news uncertainty;
- defined-but-large stop;
- weak confirmation;
- direct/aggressive branch without full B1 conditions;
- range/chop/low-volume classification;
- test position;
- re-entry/add-on after an earlier trade;
- low-confidence annotation;
- unresolved target-path quality;
- explicit low-probability classification.

The exact percentage reduction is outside this policy.

## Rule P10 — final pre-entry output

If candidate LONG passes all gates:

- `TRADE_LONG_NORMAL`; or
- `TRADE_LONG_REDUCED`.

If candidate SHORT passes all gates:

- `TRADE_SHORT_NORMAL`; or
- `TRADE_SHORT_REDUCED`.

If no candidate passes because an expected event is incomplete:

`WAIT`.

If no candidate passes because a hard veto is present:

`NO_TRADE`.

If LONG and SHORT both survive but neither is clearly privileged:

`WAIT`.

---

# POST-ENTRY POLICY

## Rule M0 — management uses only information available after entry

Management may use new candles and new structure as they occur.

It may not use future maximum excursion or final outcome.

## Rule M1 — premise invalidated

If a relevant opposing close, failed confirmation, HTF close, or new structure explicitly invalidates the entry premise:

`MANUAL_EXIT_INVALIDATED`

The original structural SL is not the only valid exit.

## Rule M2 — premise degraded but not invalidated

If evidence weakens but does not fully invalidate:

- `TIGHTEN_STOP`; or
- `BREAK_EVEN_OR_STRUCTURAL_PROTECTION`

Use structural protection when a new OB/FVG/swing provides a source-consistent protective location.

Exact buffer is unresolved.

## Rule M3 — first objective reached

If the first planned target / opposing liquidity is reached:

`PARTIAL_AND_PROTECT`

Then evaluate the remainder under M4.

No fixed partial percentage is frozen.

## Rule M4 — runner

A runner is permitted only while:

- premise remains valid;
- no opposing close invalidates it;
- next liquidity/objective is still open.

Output:

`RUNNER_TO_LIQUIDITY`

Protection may be BE or structural protection.

## Rule M5 — favorable move before TP1

A favorable move alone does not force BE universally.

If the original premise remains valid and nearby structure is expected to retest:

`HOLD`

If the setup is countertrend, direct/aggressive, news-sensitive, low-probability or otherwise reduced-risk:

prefer `TIGHTEN_STOP` / `BREAK_EVEN_OR_STRUCTURAL_PROTECTION`.

Exact movement threshold remains unresolved.

## Rule M6 — target extension

Do not extend a target merely because price is moving favorably.

Target extension is allowed only if new structure opens a clearly identified next liquidity objective while the premise remains valid.

This remains a rare optional action in v0.1.

---

# Deterministic pseudocode

```text
evaluate(candidate):

    if external_risk_lock:
        return NO_TRADE

    if environment == UNINTERPRETABLE and no authorized event branch:
        return WAIT

    if location in {ABSENT, MIDDLE, WRONG_EXTREME}:
        return NO_TRADE

    if location in {APPROACHING, UNRESOLVED}:
        return WAIT

    if chasing:
        return WAIT if valid_retrace_path_exists else NO_TRADE

    if htf_close == INVALIDATES:
        return NO_TRADE

    if htf_close == REQUIRED_PENDING:
        return WAIT

    if htf_close == FLIPS_BIAS:
        return WAIT

    if stop_state == UNDEFINED:
        return NO_TRADE

    if stop_state == TOO_LARGE_FOR_THIS_SETUP:
        return NO_TRADE

    if required_interaction == NOT_YET:
        return WAIT

    if confirmation == FAILED:
        return NO_TRADE

    if confirmation == NOT_YET:
        return WAIT

    if confirmation in {STRONG, ADEQUATE}:
        branch = CONFIRMED

    else if confirmation == WEAK:
        if not weak_branch_eligible:
            return WAIT
        branch = CONFIRMED_WEAK

    else if confirmation == NONE:
        if interaction not in {SWEEP, RETRACE_TO_POI}:
            return WAIT
        if not direct_branch_eligible:
            return WAIT
        branch = DIRECT

    if target_path == INFEASIBLE:
        return NO_TRADE

    risk = NORMAL

    if any downgrade modifier:
        risk = REDUCED

    if branch == CONFIRMED_WEAK:
        risk = REDUCED

    if branch == DIRECT and not direct_normal_eligible:
        risk = REDUCED

    return TRADE_<direction>_<risk>
```

# What this policy does not decide

v0.1 intentionally does not mechanically derive:

- which raw candle swing defines an MSS;
- how strong a candle body must be;
- exact OB/FVG geometry;
- exact “same zone” distance;
- exact stop-size threshold;
- exact RR threshold;
- exact news blackout window;
- exact BE distance;
- exact partial percentage;
- exact daily trade count.

Those are mechanization questions, not permission to tune after seeing P&L.
