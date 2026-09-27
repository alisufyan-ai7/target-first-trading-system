# EXP-043 Microstructure Availability Coverage Diagnostic v0.1

Frozen 2026-09-27. Zero-outcome integrity diagnosis only. EXP-043 v0.1 remains INTEGRITY_FAIL_DO_NOT_INTERPRET.

Purpose: test whether AUDUSD/USDCHF coverage below the frozen 90% gate is already implied by the immutable microstructure source itself.

Use only the frozen EXP-043 microstructure release. Do not load target-market OHLC, labels, predictions, P&L, or protected periods.

Decision grid: weekdays, 2026-03-23 <= date < 2026-06-30, 06:05-17:55 UTC every 5 minutes.

Availability rule is unchanged: recent [t-5m,t) >=4 observed minutes; medium [t-30m,t) >=24; baseline [t-60m,t) >=48; no forward fill.

Report source-only decision coverage by market/hour/date and longest ineligible streak.

Disposition: exact source explanation if AUDUSD and USDCHF are <90% and all other markets >=90%; partial explanation if pattern differs; otherwise source does not explain.

This diagnostic does not repair or reinterpret EXP-043 v0.1. Any future v0.2 must be separately frozen and may not tune features/windows/thresholds using visible v0.1 model metrics.
