# Research Methodology

## Evidence labels

Use these labels consistently.

### OBSERVED

Directly visible in uploaded video/chart evidence or directly measured in a recorded experiment.

### REPEATED PATTERN

Observed across multiple examples, but not necessarily a complete causal trading rule.

### HYPOTHESIS

Plausible rule that has not yet survived formal validation.

## Backtest discipline

Whenever possible:

1. specify the rule before seeing the result;
2. use a development period;
3. keep a later holdout period untouched;
4. count ambiguous same-bar target/stop cases conservatively;
5. avoid future-looking pivots;
6. record timeouts and unfilled entries;
7. include costs in later-stage validation;
8. perform sensitivity testing around key parameters;
9. validate finalists on an independent data feed;
10. require forward/paper evidence before automation.

## Anti-overfitting rule

Do not keep adding filters until a failed strategy looks good.

A filter that improves development results but deteriorates on holdout is evidence against promotion.

## Daily-distribution testing

Portfolio simulation should include every eligible trading weekday, including days with no signals, because zero days are part of the user's objective.

## Checkpointing rule

Long experiments should be broken into smaller batches.

After each material result:

- create/update an experiment file;
- record the parameters and data period;
- record the raw summary metrics;
- record the conclusion;
- record the next action.

Only then begin the next long-running computation.
