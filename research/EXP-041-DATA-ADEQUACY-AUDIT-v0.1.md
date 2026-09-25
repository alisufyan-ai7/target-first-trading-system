# EXP-041 Macro Data-Adequacy Audit v0.1

**Date:** 2026-09-25  
**Outcome labels used:** NO  
**Protected periods used:** NO

## Current evidence

The current repository market sources contain roughly March-September 2026 M1 history, while development is hard-sealed at Jun30.

The curated macro seed before the seal contains only 17 primary event blocks:

- Employment Situation: 3;
- CPI: 3;
- PPI: 3;
- Retail Sales: 3;
- GDP/PCE: 3;
- FOMC: 2.

That is too little independent macro history for a trustworthy surprise-conditioned model.

The danger is pseudo-replication: one CPI release can generate hundreds of candidate rows across markets/directions, but it remains **one economic event**.

A model can appear statistically strong while actually learning from only a few independent news days.

## Decision

**Gate A fails on sample independence.**

Disposition:

`DATA_INSUFFICIENT_EXTEND_EARLIER_HISTORY`.

Do not run a macro outcome model yet.

## Required remedy

Acquire at least 12 months of earlier development history ending Jun30 2026, with matching point-in-time macro calendar/consensus data.

This expands evidence backward rather than consuming the protected future.

## Why this is the useful expert path

A profitable human trader may specialize in CPI/NFP/FOMC behavior after seeing hundreds of releases over years.

Testing “news trading” from three CPI releases and three payroll releases would not reproduce that experience.

The system must learn from enough independent catalysts to distinguish repeatable behavior from one-off market narratives.
