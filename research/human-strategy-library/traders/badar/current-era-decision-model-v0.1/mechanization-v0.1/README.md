# Badar Current-Era Mechanization / Reproducibility Study v0.1

**Status:** PHASE 1 COMPLETE — OUTCOME BLIND  
**Source evidence snapshot:** `d19a43da80ae0e3ab4207a73a35f317120d37c84`  
**Formal policy:** `../formal-policy-v0.1/`  
**P&L / MFE / MAE access:** NOT USED  
**Backtest authorized:** NO

## Purpose

Convert the remaining qualitative inputs in Badar Current-Era Formal Decision Policy v0.1 into prospective chart-state rules without using profitability.

The study has two distinct layers:

1. **Phase 1 — structural mechanization and internal-consistency audit**
   - define source-supported chart primitives;
   - define deterministic derivation rules where evidence allows;
   - audit existing 347 outcome-blind decision events for rule contradictions.

2. **Phase 2 — blinded visual reproducibility**
   - reconstruct chart snapshots at each decision timestamp;
   - hide all future bars and Badar's eventual decision;
   - independently label unresolved states;
   - measure agreement before any P&L is opened.

Phase 1 is complete. Phase 2 cannot yet be executed from the repositories alone because the external evidence repo contains transcripts/notes and per-stream CSVs but **no stored chart-image/frame assets**.

This is a data-availability boundary, not permission to invent labels.

## Phase-1 result

Six mechanically observable hard/pending gates are already internally consistent across the 347-event corpus:

- location not reached / absent;
- middle;
- chasing;
- no logical stop;
- failed confirmation;
- required close still pending.

Together they flag **148 of 240 WAIT/NO_TRADE decisions** and produce **0 contradictions across 107 TRADE decisions**.

This is an **internal consistency result**, not validation, because the original annotations were created from source material that included Badar's decision commentary.

## Major architectural result

The original `stop_state` mixes two different questions and should be implemented as two layers:

1. **strategy-layer structural invalidation**
   - does a source-supported invalidation price exist?
2. **risk-layer sizeability**
   - can that stop be traded within the independent Target-First account-risk budget and broker constraints?

The first is chart-mechanizable. The second belongs to the risk engine and cannot be honestly inferred from chart shape alone.

## Files

- `STATE-DERIVATION-CONTRACT.md` — prospective rules for unresolved policy inputs.
- `state_derivation_contract.yaml` — machine-readable version.
- `REPRODUCIBILITY-AUDIT.md` — Phase-1 corpus audit.
- `BLINDED-VISUAL-PROTOCOL.md` — exact Phase-2 chart replay protocol.
- `phase1-hard-gate-audit.csv` — event-level outcome-blind hard-gate audit.
- `FREEZE.md` — what is frozen now and what remains unresolved.

## Current disposition

`MECHANIZATION_V0_1_PHASE1_FROZEN — VISUAL_REPRODUCIBILITY_PENDING`

No development P&L test is authorized yet.


## Tracking

Target-First issue #1:

`Build blinded Badar chart snapshot pack for 347 decision events`

The issue is the active dependency for Phase 2.

Do not substitute protected Jul–Sep 2026 raw-OHLC reconstruction for the source-frame pack.


## Phase-2 acquisition prepared

Claude's own source-research runbook confirms that the binary media/frame assets live outside Git in the local `badartrader-research/` workspace.

Target-First now contains:

- `source-frame-request.csv` — 347 frozen event requests;
- 345 events marked `READY` for exact in-stream extraction;
- 2 events marked `MANUAL_PRESTREAM`;
- `tools/extract_source_frames.py` — no-download extractor using the existing Claude media cache;
- `SOURCE-FRAME-EXPORT.md` — transfer instructions.

The extractor requests T−120, T−60, T−30 and T−5 seconds only, exports no decision labels or outcomes, and hashes every frame.

Tracking issue #1 has been updated with this acquisition path.

Current dependency is now physical/file access to Claude's existing local `badartrader-research/media/` cache or an archive exported from it.
