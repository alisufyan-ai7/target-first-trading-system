# Research and Validation

Research is the **validation layer for building the trading system**, not the final product.

Every meaningful quantitative test should receive a unique experiment ID under research/experiments/.

Minimum experiment contents:

- question;
- hypothesis;
- frozen strategy/system specification;
- data source and provenance;
- date range;
- parameters;
- development/validation/holdout split;
- execution assumptions;
- results;
- limitations;
- conclusion;
- promotion/rejection/paused status;
- next action.

## Rules

- unique experiment IDs only;
- do not silently revise a frozen experiment after holdout inspection;
- checkpoint material results before another long run;
- do not overfit failed strategies until they look good;
- preserve zero-signal days in daily-distribution metrics;
- keep raw large datasets outside Git and record retrieval/provenance instead;
- finalists require independent-feed and broker-cost validation;
- research conclusions must remain subordinate to the current system architecture in docs/SYSTEM-BLUEPRINT.md.
