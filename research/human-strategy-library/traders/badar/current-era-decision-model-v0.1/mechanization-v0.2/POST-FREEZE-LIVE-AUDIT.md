# Post-v0.1 Live-Stream Audit — Mechanization v0.2

**Evidence cutoff:** `bd0037e06a881a066e0cd8070b635cace59240d1`  
**Outcome use:** NONE  
**v0.1 cases reused:** 0

## Fresh-source inventory

| Stream | Date | Full-res frames | Source note | Transcript | v0.2 use |
|---|---|---:|---|---|---|
| PYPzCJV-YXE | 2026-10-01 | 29 | yes | yes | included |
| PxDGTxs-Cvc | 2026-10-02 | 35 | yes | yes | included |
| EsAa5_T_kbQ | 2026-10-06 | 31 | yes | yes | included |
| D85FC79tI6w | 2026-10-08 | 14 | yes | yes | included |
| 6wwmBYPvmPQ | 2026-10-14 | 26 | yes | yes | included |
| _9vCesQpBtM | 2026-10-15 | 12 | yes | yes | included |
| of0Pv8JP4eE | 2026-10-23 | 30 | yes | yes | included |
| wXbKuO5lVGg | 2026-10-26 | 24 | yes | yes | included |

Total: **8 streams / 201 full-resolution frames**.

## Source-only behavioral themes relevant to packet design

These are used only to decide what metadata a blind packet must expose. They are not outcome claims.

### October 1 — PYPzCJV-YXE

Recurring prospective information:

- sell-side context;
- H1 sell area / swept high;
- M15 close used directly as decision evidence;
- repeated planned retraces into M15/M1 FVG areas;
- explicit refusal to sell after price had already moved too low;
- different risk treatment for direct/early versus post-MSS entries.

v0.2 implication:

the packet must name the candidate side, intended POI, active confirmation timeframe and whether the trade is a direct-close or retrace branch.

### October 2 — PxDGTxs-Cvc

Recurring prospective information:

- no pre-news directional commitment in the middle;
- news-release candle-close branch;
- post-spike retrace branch;
- hidden-OB/FVG candidate area;
- 1m/3m/5m confirmation timing;
- explicit comments that an entry could be late.

v0.2 implication:

the packet must state event/news context, active candle status and intended entry anchor before asking about confirmation or chasing.

### October 6 — EsAa5_T_kbQ

Recurring prospective information:

- sell context after a high sweep;
- later limit/retrace entry from a bearish FVG/zone;
- resting-limit style without new LTF close at the moment of entry.

v0.2 implication:

confirmation cannot be assumed mandatory; the packet must state the intended branch.

### October 8 — D85FC79tI6w

Recurring prospective information:

- range context;
- sell OB / buyer-trap idea;
- lower-timeframe confirmation;
- separate breakout-long condition above a fixed level.

v0.2 implication:

candidate direction and the exact level being evaluated must be explicit.

### October 14 — 6wwmBYPvmPQ

Recurring prospective information:

- strong trend-sell context;
- early lower-timeframe sell close rejected while waiting for M15;
- countertrend buy ideas downgraded;
- repeated sell attempts at FVG/OB areas;
- re-entry / retry logic.

v0.2 implication:

required-HTF-close state must be supplied prospectively rather than inferred by the annotator.

### October 15 — _9vCesQpBtM

Recurring prospective information:

- range uncertainty;
- hidden-OB tap;
- 5m bullish-close evidence;
- explicit concern about stop size;
- later buying-area and 1m breakout conditions.

v0.2 implication:

structural-stop visibility and candidate-side metadata need to be separate from setup quality.

### October 23 — of0Pv8JP4eE

Recurring prospective information:

- daily sell context;
- daily OB/FVG sell area;
- 1m signal rejected because 5m/10m confirmation was preferred;
- later 5m reverse-close market entry;
- explicit second-entry idea skipped because it was already late;
- countertrend buy from support rejected as risky.

v0.2 implication:

this stream directly supports named confirmation reference, candle status and a frozen intended entry area for chasing classification.

### October 26 — wXbKuO5lVGg

Recurring prospective information:

- sell context after Asian-high sweep;
- FVG/OB continuation short;
- higher sell area left pending;
- 1m scalp-close branch;
- countertrend long around the 4000 area;
- explicit acknowledgement that a later long was entered late.

v0.2 implication:

the packet needs candidate side, POI, branch and entry anchor before ON_TIME/CHASING is judged.

## Fresh decision-candidate manifest

A prospective 43-event candidate set is frozen in:

`candidate-events-v0.2.csv`

Selection rules:

- candidate is explicitly identifiable before or at the source timestamp;
- candidate direction is prospectively identifiable;
- intended area/reference can be named without using future outcome;
- source frames exist at/before the event;
- ambiguous pre-stream or unconfirmed-execution events are excluded;
- management-only decisions are excluded from this first v0.2 reproducibility test.

No behavior label is stored in the public manifest.

## Scientific role

The eight-stream tranche is a **fresh reproducibility test**, not a profitability sample.

No P&L use is authorized even if v0.2 reproducibility succeeds.
