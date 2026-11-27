# Ready-to-Paste Bootstrap Prompt for Chat #11

You are continuing the **Badar Tanveer Strategies / Target-First Trading System** project. This is **Chat #11**.

## Canonical source

GitHub is the durable source of truth.

Main repository:

`alisufyan-ai7/target-first-trading-system`

External Badar evidence feed:

`alisufyan-ai7/unpack-human-trading-strategies-claude`

Before new research, fetch current main HEADs and read:

1. `docs/PROJECT-GOVERNANCE.md`
2. `docs/current-status.md`
3. `docs/decision-log.md`
4. `docs/NEW-CHAT-HANDOFF.md`
5. `docs/CHAT-LEDGER.md`
6. `CHANGELOG.md`
7. `strategies/STATUS.md`
8. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.1/phase2-independent-results-v2/PHASE2-INDEPENDENT-REPRODUCIBILITY-RESULT.md`
9. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.2/README.md`
10. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.2/REPRODUCIBILITY-GATES.md`
11. `research/human-strategy-library/traders/badar/current-era-decision-model-v0.1/mechanization-v0.2/independent-results/REPRODUCIBILITY-RESULT.md`

Also inspect commits/docs newer than this prompt.

## Historical mechanization results

v0.1:

`PHASE2_V0_1_INDEPENDENT_REPRODUCIBILITY_FAIL_CLOSE_BEFORE_BEHAVIORAL_FIDELITY`

v0.2:

`V0_2_REPRODUCIBILITY_FAIL_CLOSE_BEFORE_BEHAVIORAL_FIDELITY`

v0.2 used a genuinely fresh 43-case tranche from evidence boundary:

`bd0037e06a881a066e0cd8070b635cace59240d1`

No v0.1 cases were reused.

## v0.2 formal result

| Field | Raw | Kappa | Result |
|---|---:|---:|---|
| location_state | 51.2% | 0.260 | FAIL |
| structural_stop_visibility | 74.4% | 0.532 | FAIL |
| late_state, applicable N=26 | 73.1% | 0.450 | FAIL |
| confirmation_state, human N=17 | 76.5% | 0.595 | FAIL |
| target_path_state | 95.3% | 0.482 | FAIL |
| HTF packet applicability | 100% | n/a | PASS |

Provenance and crosswalk verification passed. Prior exposure was zero.

## Hard boundary

Do **not** reveal Badar's actual TRADE/WAIT/NO_TRADE decisions for the v0.2 cases.

Do **not** open P&L, result R, MFE/MAE, skipped-trade outcomes, or later management.

Do **not** adjudicate/repair v0.2 labels and rescore the same tranche as independent.

Do **not** tune a successor and reuse these 43 cases as fresh validation.

## If research continues

The only scientifically authorized continuation is a **prospectively new mechanization version/tranche**.

It may use v0.2 aggregate disagreement diagnostics to redesign the representation/contract, but must freeze new definitions and promotion gates before collecting labels on a genuinely fresh evidence set.

No behavior-fidelity or P&L stage is authorized from v0.2.

## Mandatory documentation

After every meaningful execution, update GitHub:

- `docs/current-status.md`
- `docs/decision-log.md`
- `docs/NEW-CHAT-HANDOFF.md`
- `docs/CHAT-LEDGER.md`
- `docs/NEXT-CHAT-PROMPT.md`
- `CHANGELOG.md`
- affected research README/result/freeze/manifest
- relevant GitHub issue(s)

Always leave the exact disposition, next action, evidence boundaries and current Target-First HEAD.
