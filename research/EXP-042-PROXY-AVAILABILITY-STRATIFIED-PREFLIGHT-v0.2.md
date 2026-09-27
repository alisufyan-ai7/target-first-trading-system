# EXP-042 Proxy Availability-Stratified Preflight v0.2

**Frozen:** 2026-09-27  
**Type:** zero-outcome availability stratification after v0.1 coverage failure  
**Protected periods:** Jul-Aug and Sep 2026 remain sealed

## 1. Why v0.2 exists

v0.1 durable result `e9ddeb68c5a4b6fa2da2b1892892bafdb72b0d32` failed the requirement that **both** proxies cover every one of the 57 geometrically post-release-eligible events.

The immutable proxy snapshot itself passed repeatability and integrity.

Exactly six eligible events failed common coverage because one proxy was inactive around the release:

- DXY unavailable: 2025-08-01, 2026-02-20, 2026-04-09, 2026-04-10;
- US T-Bond proxy unavailable: 2025-08-14, 2026-04-03.

This is a source trading-hours/availability property observed before any target-market outcome was loaded.

v0.1 remains a FAIL. Its thresholds are not weakened.

## 2. v0.2 objective

Freeze availability-defined event subsets before any target/path label or model is loaded.

Two nested subsets are allowed:

### DXY_COMPLETE

An event belongs to DXY_COMPLETE only if DOLLARIDXUSD independently satisfies the original strict availability rule:

- causal baseline = last M1 close strictly before event;
- baseline staleness >0 and <=5 minutes;
- at each legal post-release structural decision timestamp, use last M1 close strictly before decision;
- per-event decision-time coverage >=80%;
- at least one covered decision timestamp.

### DXY_TBOND_COMPLETE

An event belongs to DXY_TBOND_COMPLETE only if **both** DOLLARIDXUSD and USTBONDTRUSD independently satisfy the same rule above.

No imputation, stale-price carry-forward beyond 5 minutes, or synthetic filling is allowed.

## 3. Frozen structural geometry

Use exact v0.1 geometry:

- Gate-A events: 65;
- post-release structurally eligible: 57;
- structurally ineligible: exactly eight late FOMC timestamps already frozen in v0.1.

The 57-event structural-eligibility set itself may not change.

## 4. Adequacy requirements for each subset

A subset is model-eligible only if all hold:

1. >=40 independent event timestamps;
2. recurring family timestamp counts all >=8:
   - EMPLOYMENT;
   - CPI;
   - PPI;
   - RETAIL;
   - GDP_PCE;
3. each of the six frozen Gate-A folds contains >=4 subset events;
4. each fold contains >=2 event families;
5. every included event passes its required proxy availability rule;
6. no excluded event is silently reintroduced later.

The same original Gate-A adequacy minima are reused; no new weaker minima are invented.

## 5. Output

Write exact immutable timestamp lists:

- `DXY_COMPLETE`;
- `DXY_TBOND_COMPLETE`.

For each subset also store:

- event count;
- family timestamp counts;
- fold event counts;
- fold family counts;
- excluded timestamps and reason/proxy.

These exact lists become the only allowed event universes for EXP-042 modeling.

## 6. Modeling authorization

If DXY_COMPLETE passes:

`EXP042_DXY_SUBSET_ADEQUATE`.

If DXY_TBOND_COMPLETE passes:

`EXP042_DXY_TBOND_SUBSET_ADEQUATE`.

If both pass, authorize the nested future study:

- Study A on DXY_COMPLETE:
  `LOCAL_M5 + EVENT_TIME_CONTROL -> +DXY_REACTION`;
- Study B on DXY_TBOND_COMPLETE:
  `LOCAL_M5 + EVENT_TIME_CONTROL + DXY_REACTION -> +DXY_TBOND_INTERPRETATION`.

Each study compares models on the **same rows/event subset within that study**. Do not compare absolute performance across the two different subsets.

If either subset fails adequacy, that corresponding study is prohibited.

## 7. Restrictions

This preflight must not load:

- target-market bars;
- target/path labels;
- model outcomes;
- P&L;
- protected Jul-Aug/Sep 2026 data.

Engine R and EXP-015 remain paused.
