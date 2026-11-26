# Phase-2 Independent Reproducibility Results v2

**Status:** COMPLETE — REPRODUCIBILITY GATE FAILED  
**Events:** 254  
**Annotators:** 2 independent blind passes  
**Prior exposure:** 0/254 for A; 0/254 for B  
**Badar decision labels revealed:** NO  
**P&L / outcome / MFE / MAE revealed:** NO

## Provenance

Active rebuilt pack hashes:

- Annotator A: `e972eea554b77636021f1a37b9662e47867089bff00960ba33604a52ee883e95`
- Annotator B: `285caff6000667a01758bedf5904bfa01f5862054d4908c9cd7179586063a45d`

Sealed rebuilt crosswalk commitment:

`474572c2e21d6d8f5a770f27ce0b9d5d837bd2c147691bb15b652334672ddbc1`

The local crosswalk used for scoring was hash-verified against this commitment before A/B labels were mapped to the same underlying events.

## Files

- `raw/` — exact returned CSVs, preserved under blind IDs.
- `RETURN-MANIFEST.csv` — row counts, hashes and integrity checks.
- `AGREEMENT-METRICS.csv` — raw agreement, kappa and unresolved rates.
- `BINARY-GATE-AGREEMENT.csv` — positive/negative agreement for selected hard-gate reductions.
- `PHASE2-INDEPENDENT-REPRODUCIBILITY-RESULT.md` — scientific disposition.

## Scientific disposition

`PHASE2_V0_1_INDEPENDENT_REPRODUCIBILITY_FAIL_CLOSE_BEFORE_BEHAVIORAL_FIDELITY`

All seven frozen promotion fields failed their predeclared reproducibility gate.

Therefore:

- v0.1 qualitative state classifiers are not yet reproducible enough for automated policy use;
- no development backtest is authorized;
- Badar's actual TRADE/WAIT/NO_TRADE labels remain sealed;
- P&L remains sealed;
- no post-hoc adjudication is allowed to turn a failed field into a passing automated field.

The next research object must be a new, outcome-blind mechanization version that improves the annotation representation/contract and is retested prospectively.
