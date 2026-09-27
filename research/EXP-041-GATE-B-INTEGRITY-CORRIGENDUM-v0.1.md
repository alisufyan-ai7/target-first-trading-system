# EXP-041 Gate-B Integrity Corrigendum v0.1

Frozen 2026-09-27. Integrity-only repair. No model rerun and no scientific threshold changes.


## Frozen mechanical diagnosis

The only uncovered Gate-A timestamps in the original Gate-B result are:

- 2025-12-10T19:00:00Z — FOMC;
- 2026-01-28T19:00:00Z — FOMC.

The reused EXP-040 decision grid is weekdays 06:05-17:55 UTC every five minutes. Gate B's event window is [-60,+180] minutes. A 19:00 event therefore has no legal structural decision timestamp in that frozen grid: the pre-event window begins at 18:00, five minutes after the grid has already ended.

All other 63 frozen Gate-A timestamps have candidates.

Frozen original Gate-B result blob SHA:

`d5789f32f7c0e239d7efd4e45dc14e205763b5fd`.

The corrigendum:

- does not rerun Gate B;
- does not alter any metric, feature, model, fold, threshold, candidate time or event window;
- derives geometric eligibility independently;
- requires exactly 63 eligible timestamps;
- requires exactly the two FOMC timestamps above to be ineligible;
- recovers the scientific disposition only from the original unchanged information-advantage gates.

Runner commit: `8c22f18128f1738eb1cc2a54bb43215e549f7562`.  
Workflow commit: `996be120f13f538d05f20dcb945f93739871b639`.
