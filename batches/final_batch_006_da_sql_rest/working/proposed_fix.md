# Proposed Fix — `tile_sql_fund_filtering_rows/s13` missing IS NULL test

## Root cause

The generator repeatedly produces a `grading.tests` array for step `s13` that contains
only one test (`t_is_not_null`, targeting `statement: 1`).  The exercise prompt asks
learners to write **two** queries — IS NULL first, IS NOT NULL second — but statement 0
(the IS NULL query) is never tested.  The evaluator correctly blocks on this every round;
three repair attempts across two pipeline runs have not fixed it.

## Required change

In the generated file
`working/gate_04_interactions_c0_canary/tile_lessons/tile_sql_fund_filtering_rows.json`
(and the corresponding public copy), inside
`steps[s13].interaction.grading.tests`, **add** the following test object
(alongside the existing `t_is_not_null` entry):

```json
{
  "test_id": "t_is_null",
  "kind": "query_result_equals",
  "spec": {
    "statement": 0,
    "expected": {
      "columns": ["order_id", "delivery_time_minutes"],
      "rows": [
        [1011, null],
        [1012, null]
      ]
    },
    "ordered": false
  },
  "visible": true,
  "message_on_fail": "Your first query should return exactly the 2 orders where delivery_time_minutes IS NULL. Use IS NULL."
}
```

Also update `execution_provenance.tests_passed` from `1` to `2` after verifying
both tests pass against the solution.

## Why the generator keeps missing this

The generator prompt or few-shot examples for `code_exercise` grading apparently
do not enforce "one test per statement when multiple statements are required."
Consider adding an explicit rule to the generator system prompt:

> "For every SQL statement slot in a multi-statement exercise, there MUST be at
> least one `query_result_equals` test whose `spec.statement` index matches that
> slot's 0-based position."

## Action for the human operator

1. Manually patch the JSON file as described above (or seed it as a repair hint).
2. Re-run the pipeline — completed stages are skipped, so only `04_interactions`
   will re-execute.
3. Longer term: update the generator prompt/template to enforce the one-test-per-
   statement rule so this cannot recur.
