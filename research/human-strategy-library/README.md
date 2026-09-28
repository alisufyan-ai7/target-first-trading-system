# Human Strategy Evidence Library

## Purpose

This folder preserves external human-trader material as research evidence before it is translated into engine rules.

The goal is to answer:

> What are experienced human traders actually seeing, deciding, and doing that our mechanical / model-generated OHLC strategies may be missing?

This library is deliberately separate from `research/experiments/` and `strategies/`.

Human-source evidence must be captured first. Formalization and testing come later.

## Current source groups

- `traders/badar/` — Badar videos, posts, examples, explanations, and extracted decision logic.
- `traders/other/` — other traders, grouped by source identity when enough material accumulates.
- `cross-source/` — concepts that recur across multiple independent human sources.
- `templates/` — standard source-analysis and strategy-extraction formats.

## Evidence hierarchy

Every source should move through four distinct layers.

### 1. Raw-source record

Record only verifiable source facts:

- source ID;
- trader/source identity;
- platform;
- title/caption;
- source URL when available;
- upload filename;
- publication date when known;
- duration;
- exact timestamps used as evidence.

Do not silently add trading theory that the source did not state or visibly demonstrate.

### 2. Evidence extraction

Capture what the trader actually says or visibly demonstrates:

- important timestamped observations;
- chart screenshots / frames where legally and practically appropriate;
- marked levels and timeframes;
- stated market context;
- entry logic;
- stop / invalidation logic;
- target logic;
- trade-management statements;
- session/time-of-day considerations;
- discretionary cues;
- examples explicitly rejected or skipped;
- uncertainty / contradictions.

Distinguish:

- `SOURCE_EXPLICIT` — stated directly;
- `SOURCE_VISUAL` — visible in the chart/action;
- `RESEARCHER_INFERENCE` — our interpretation, not directly stated.

### 3. Strategy model

After enough evidence exists, convert recurring source logic into a structured human strategy model:

- context;
- setup;
- trigger;
- entry;
- invalidation;
- target;
- management;
- no-trade conditions;
- hierarchy of signals;
- discretionary judgment points.

Do not force ambiguous human judgment into fake precision.

### 4. Testable hypothesis

Only after the strategy model is documented may we freeze a reproducible experiment.

The rule order remains:

`SOURCE EVIDENCE -> HUMAN LOGIC MODEL -> FROZEN HYPOTHESIS -> DEVELOPMENT TEST -> SEALED VALIDATION`

Never reverse this by looking at profitable historical outcomes first and then rewriting the human strategy to fit them.

## Copyright / source-storage rule

Do not commit full third-party videos to the repository unless the repository owner has the necessary rights and intentionally wants to store them.

Prefer storing:

- metadata;
- source links;
- file hashes / filenames when available;
- timestamp references;
- our own notes;
- small research screenshots or annotated frames only where appropriate;
- derived diagrams / structured descriptions.

The user's original uploaded media can be analyzed during the chat without requiring the entire copyrighted source to become part of the Git repository.

## Evidence quality

A strategy claim becomes stronger when it appears:

1. repeatedly in the same trader's independent examples;
2. across different market regimes;
3. in both winning and losing examples;
4. in explicit no-trade / skip explanations;
5. across multiple independent traders.

One attractive winning chart is not enough to define a strategy.

## Project discipline

Human-source material is evidence, not proof of profitability.

A trader's claimed profitability, screenshots, or social-media presentation must not automatically be treated as verified performance.

The purpose of this library is to reconstruct decision logic faithfully and then test that logic prospectively.
