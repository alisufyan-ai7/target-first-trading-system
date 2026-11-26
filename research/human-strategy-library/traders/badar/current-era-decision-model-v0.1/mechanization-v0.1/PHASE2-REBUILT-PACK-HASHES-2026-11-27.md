# Rebuilt Independent Annotator Pack Hashes — 2026-11-27

The original conversation attachment bytes expired and were no longer downloadable.

Fresh equivalent A/B packs were rebuilt from the frozen 254-event core mapping and the preserved Phase-2 panel artifact.

## Replacement pack hashes

- Annotator A aggregate ZIP:
  - SHA-256: `e972eea554b77636021f1a37b9662e47867089bff00960ba33604a52ee883e95`
- Annotator B aggregate ZIP:
  - SHA-256: `285caff6000667a01758bedf5904bfa01f5862054d4908c9cd7179586063a45d`

## Replacement sealed crosswalk commitment

- SHA-256: `474572c2e21d6d8f5a770f27ce0b9d5d837bd2c147691bb15b652334672ddbc1`

The crosswalk itself is not included in either annotator pack.

## Integrity check

Both ZIPs pass archive integrity testing.

Leak scan result for filenames and text metadata:

- original stream IDs exposed: **0**
- original decision-event IDs exposed: **0**

Underlying study composition remains:

- 254 frozen core events
- four paired folds: 64 / 64 / 63 / 63
- A/B use separate blind IDs and independent within-fold ordering
- no decision labels
- no P&L/outcome/MFE/MAE
