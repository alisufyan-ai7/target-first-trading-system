# Long-Running Pipeline Workflow Policy

_Last updated: 2026-09-24_  
**Status:** PROJECT OPERATING RULE

## Purpose

Long-running GitHub Actions jobs commonly take 10–30 minutes. Repeatedly polling them from ChatGPT wastes tool calls and conversation time without improving the experiment.

This policy defines how the project operates while a CI/research pipeline is running.

## Core rule

After launching a long-running GitHub pipeline:

1. confirm once that the intended workflow was queued or started;
2. do **not** repeatedly poll it merely to wait for completion;
3. use the remaining turn only for work that is genuinely independent of the pending result;
4. if no useful independent work remains, stop the turn and resume when the user returns or explicitly asks for status;
5. when resuming, inspect the durable workflow result/commit first and continue from the repository state.

This is the default behavior for all future experiments unless the user explicitly requests active monitoring.

## What counts as safe parallel work

Parallel work is allowed only when it does **not** depend on the pending result and cannot alter the frozen experiment being executed.

Examples:

- documentation that records already-frozen rules;
- future-stage scaffolding that is not triggered;
- code review of unrelated modules;
- source-of-truth cleanup;
- provenance documentation;
- designing a later experiment prospectively without using the pending outcome;
- adding tests or operational tooling that does not change the running experiment's code/data/spec.

## What is not safe parallel work

Do not, while an experiment is running:

- edit the code, specification, data manifest, thresholds, features, target rules, costs, gates, or workflow inputs used by that running experiment;
- create a new trigger for the same experiment;
- inspect protected later-period outcomes;
- change a gate because the pending run appears slow, sparse, or likely to fail;
- make outcome-dependent design choices before the result is durably checkpointed;
- repeatedly query Actions status with no new decision to make.

If a correction to the running experiment is discovered, record the issue and let the current run finish or cancel it explicitly if cancellation is necessary. Do not silently mutate the experiment underneath the running SHA.

## Repository-race rule

A long-running workflow may finish by committing generated results back to `main`.

Therefore:

- parallel commits must never change the frozen inputs of the running workflow;
- workflows that commit results should use `git pull --rebase origin main` immediately before pushing;
- generated result commits must be based on, or explicitly identify, the tested repository SHA;
- a push conflict is an operational failure, not an experimental result;
- if duplicate runs race, accept one durable identical result and do not rerun merely because another duplicate failed to push.

Where practical, result files should record:

- tested repository SHA;
- engine/runner fingerprint;
- data/provenance fingerprint;
- whether protected periods were loaded;
- experiment/run ID.

## Trigger discipline

Before triggering:

1. freeze and commit all experiment inputs;
2. verify the intended workflow path/trigger;
3. ensure protected periods are excluded as required;
4. create one trigger;
5. confirm that the correct workflow was queued/running.

Do not create repeated triggers to obtain faster feedback.

## During-pipeline discipline

After the one-time launch confirmation:

```text
pipeline running
    ->
is there independent useful work?
    -> yes: do only that independent work
    -> no: end the turn
```

The assistant must not simulate background monitoring. A later user message resumes the workflow by reading GitHub's durable state.

## Result-resume discipline

When returning after a long-running pipeline:

1. read the workflow/run conclusion or durable result file;
2. verify the result corresponds to the intended tested SHA;
3. check whether the result was successfully committed;
4. apply the experiment's predeclared gate;
5. update experiment/status/decision-log/changelog/handoff as appropriate;
6. only then trigger the next permitted stage.

Do not infer success or failure from elapsed time.

## Exceptions

Active repeated status checking is appropriate only when:

- the user explicitly asks for live monitoring;
- an immediate external dependency makes status materially actionable;
- the run normally completes within a very short period;
- a failure is expected to require prompt intervention and the user has asked to keep the turn open.

Even then, polling should be sparse and purposeful.

## Relationship to experimental integrity

This policy is not merely a convenience rule.

It protects the evidence process by preventing:

- accidental mid-run mutation;
- duplicate triggers;
- result-commit races;
- post-hoc threshold changes while waiting;
- needless consumption of protected state;
- conversational timeouts caused by waiting loops.

The project therefore treats efficient pipeline handling as part of reproducibility and experiment governance.
