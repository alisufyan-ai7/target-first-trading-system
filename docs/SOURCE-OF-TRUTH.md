# Source of Truth and Context Isolation

_Last updated: 2026-09-22_

## Authorized context

This project has exactly two authorized context sources:

1. the originating ChatGPT conversation for this project;
2. this GitHub repository: `alisufyan-ai7/target-first-trading-system`.

## Isolation rule

Do **not** use, inspect for project context, copy from, infer from, or merge assumptions/results/code/decisions from:

- any other GitHub repository on this account;
- any other ChatGPT conversation;
- any other ChatGPT project;
- account-level memories or context;
- unrelated local files or connected apps.

An external source may be used only as **research data or public reference material**, and must be explicitly documented as such. External research sources do not become project memory unless their relevant findings are recorded in this repository.

If the user explicitly introduces material from another source into this project, record that introduction and its provenance before using it.

## Conflict rule

When chat history and repository records conflict:

- prefer the most recent explicit user instruction;
- update this repository immediately;
- preserve the prior decision in the decision log where useful.

## Durability rule

Material conclusions should be checkpointed here before beginning another long-running experiment. This is intended to prevent loss of progress when a ChatGPT stream or tool session times out.

## Long-running pipeline rule

The project operating policy in `docs/PIPELINE-WORKFLOW-POLICY.md` is mandatory.

After launching a long-running GitHub pipeline, confirm the intended run once. Do not repeatedly poll merely to wait. Use the turn only for independent work that cannot change the running experiment; otherwise end the turn and resume from GitHub's durable result later.

Do not mutate the running experiment's frozen inputs while its pipeline is active. Result-committing workflows should rebase from current `main` before pushing so unrelated safe parallel commits do not create avoidable result-push failures.

## Sensitive information

Do not store passwords, API keys, broker credentials, account identifiers, or other secrets in this repository.
