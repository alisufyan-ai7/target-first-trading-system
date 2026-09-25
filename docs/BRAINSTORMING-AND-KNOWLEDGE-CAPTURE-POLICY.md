# Brainstorming and Knowledge-Capture Policy

_Last updated: 2026-09-25_  
**Status:** GOVERNING PROJECT POLICY

## Purpose

Important project reasoning must not exist only in chat.

The Target-First Trading System is developed across multiple conversations. Material brainstorming, conceptual corrections, research lessons, rejected assumptions, architecture changes, and newly identified risks must be synthesized into the repository so a later chat can reconstruct not only **what was done**, but also **why**.

## Governing rule

After any materially important brainstorming or reasoning session, checkpoint the useful conclusions in GitHub before moving far enough that losing the chat would damage continuity.

Do **not** dump raw conversation transcripts into the repository.

Instead convert the discussion into durable project knowledge.

## What must be captured

Capture when a discussion changes or materially sharpens any of the following:

- project objective or constraints;
- strategy/research architecture;
- interpretation of failed experiments;
- root-cause hypotheses;
- data-source priorities;
- risk/sizing philosophy;
- target/exit philosophy;
- market/timeframe specialization;
- human-trader evidence;
- anti-overfitting rules;
- protected-period policy;
- experimental sequencing;
- go/no-go criteria;
- assumptions that were considered and rejected;
- important user-supplied screenshots/videos/examples and what was actually useful from them.

## How to capture it

Use the smallest durable structure that preserves the reasoning.

Preferred locations:

- `docs/decision-log.md` — durable decisions and why they were made;
- `docs/current-status.md` — authoritative current path / exact next action;
- `docs/NEW-CHAT-HANDOFF.md` — concise current state needed by a new chat;
- dedicated `research/*.md` — deeper research synthesis, audits, matrices, or unresolved hypotheses;
- `strategies/STATUS.md` — strategy-family lifecycle only;
- `CHANGELOG.md` — concise record of material repository changes.

## Evidence labels

When appropriate, distinguish:

- **OBSERVED / VERIFIED** — supported by repository results or directly supplied evidence;
- **EXTERNAL RESEARCH** — supported by cited public research;
- **HYPOTHESIS** — plausible but not yet tested;
- **DECISION** — project rule frozen prospectively;
- **REJECTED / DEFERRED** — considered but not adopted.

Do not silently turn a brainstorming idea into a strategy rule.

## Screenshots / social-media material

Treat user-supplied educational/social-media material as:

- a source of hypotheses, workflow ideas, or human-process clues;
- **not** authoritative trading evidence by itself.

Capture the useful abstraction, not the influencer claim.

Example:

- useful: “separate higher-timeframe context from lower-timeframe execution”;
- not automatically accepted: “this exact pair/session/timeframe always works.”

## Numerical/project facts

When brainstorming depends on experiment results, verify the authoritative durable result before checkpointing numerical claims.

Later dated/checkpoint sections supersede stale earlier wording.

## Anti-overfitting rule

Brainstorming after seeing development outcomes can create researcher-level overfitting.

Therefore:

- post-result ideas must be clearly marked as hypotheses;
- they must not modify a failed experiment in place;
- a future test must be prospectively frozen before outcomes;
- protected periods remain sealed unless the governing gate permits inspection.

## New-chat requirement

A new chat should be able to reconstruct:

1. current objective;
2. current architecture;
3. recent failures and lessons;
4. active research hypothesis;
5. protected data status;
6. exact next action;
7. unresolved high-value questions.

If any of these exists only in chat, knowledge capture is incomplete.

## Practical checkpoint cadence

Checkpoint immediately after:

- a material experiment result;
- a strategy-family closure/opening;
- a root-cause conclusion;
- a major research-direction change;
- a risk/sizing-policy change;
- a substantial user-evidence review;
- a major brainstorming session that changes the next action.

Small conversational details do not require repository updates.

## Bottom line

The repository is the durable project memory.

Chat is the working room; GitHub is the source of truth.
