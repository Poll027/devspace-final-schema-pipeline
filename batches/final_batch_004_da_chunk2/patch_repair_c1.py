"""
Repair patch for interactions.part.c1.json
Fixes two BLOCKING issues:
1. tile_capstone_question_workflow/s08: Remove item_csv_trap from items and grading.assignments
2. tile_stats_sample_size_significance/s09: Replace task_pvalue_large with a task that
   tests the repeated-sampling interpretation of 95% confidence
"""
import json, copy

with open('batches/final_batch_004_da_chunk2/interactions.part.c1.json') as f:
    data = json.load(f)

# ── FIX 1: tile_capstone_question_workflow/s08 ──────────────────────────────
# Remove item_csv_trap from items list and from grading.assignments + item_feedback
for tile in data['tiles']:
    if tile['tile_id'] != 'tile_capstone_question_workflow':
        continue
    for entry in tile['interactions']:
        if entry['step_id'] != 'tile_capstone_question_workflow.s08':
            continue
        ix = entry['interaction']

        # Remove from public.items
        ix['public']['items'] = [
            item for item in ix['public']['items']
            if item['item_id'] != 'item_csv_trap'
        ]

        # Remove from grading.assignments
        ix['grading']['assignments'].pop('item_csv_trap', None)

        # Remove from grading.item_feedback
        ix['grading']['item_feedback'].pop('item_csv_trap', None)

        # Clean up feedback/hints that mention CSV (advisory fix: reword only)
        ix['feedback']['correct']['message'] = (
            "Well done. SQL databases \u2192 SQL query via pandas.io.sql; "
            "Excel workbooks (.xlsx) \u2192 read_excel(). The retrieval method follows where the data lives."
        )
        ix['feedback']['incorrect']['message'] = (
            "Match the retrieval method to where the data lives. "
            "SQL databases use SQL queries via pandas.io.sql. "
            "Excel workbooks (.xlsx) use read_excel()."
        )
        ix['feedback']['hints'] = [
            "Look at the file extension or storage type: .xlsx = Excel workbook; SQL database = SQL query.",
            "The retrieval method must match where the data lives \u2014 database or file."
        ]
        break

# ── FIX 2: tile_stats_sample_size_significance/s09 ─────────────────────────
# Replace task_pvalue_large with a task that tests the repeated-sampling
# interpretation of 95% confidence (anchored to #practice success criterion).
for tile in data['tiles']:
    if tile['tile_id'] != 'tile_stats_sample_size_significance':
        continue
    for entry in tile['interactions']:
        if entry['step_id'] != 'tile_stats_sample_size_significance.s09':
            continue
        ix = entry['interaction']

        # Replace task_pvalue_large in public.tasks
        new_task = {
            "task_id": "task_ci_interpretation",
            "prompt": (
                "Select the ci_lower cell for the large-sample test (test_checkout_large) "
                "variation row. The 95% confidence interval shown there reflects the "
                "repeated-sampling behaviour of the method: if this procedure were applied "
                "to many independent samples, about 95% of the resulting intervals would "
                "contain the true parameter \u2014 not that there is a 95% probability "
                "this specific interval contains it. Identify the cell that anchors this interval."
            ),
            "target_kind": "cell"
        }
        ix['public']['tasks'] = [
            t if t['task_id'] != 'task_pvalue_large' else new_task
            for t in ix['public']['tasks']
        ]

        # Replace task_pvalue_large answer in grading.answers
        new_answer = {
            "task_id": "task_ci_interpretation",
            "row": {
                "where": {
                    "test_id": "test_checkout_large",
                    "variant": "variation"
                }
            },
            "column": "ci_lower"
        }
        ix['grading']['answers'] = [
            a if a['task_id'] != 'task_pvalue_large' else new_answer
            for a in ix['grading']['answers']
        ]

        # Replace task_pvalue_large feedback in grading.task_feedback
        ix['grading']['task_feedback'].pop('task_pvalue_large', None)
        ix['grading']['task_feedback']['task_ci_interpretation'] = {
            "correct": (
                "Correct. The ci_lower value anchors the 95% confidence interval for the "
                "large-sample test. '95% confidence' describes the long-run behaviour of "
                "the method: if the sampling procedure were repeated many times, about 95% "
                "of the resulting intervals would contain the true parameter. It does not "
                "mean there is a 95% probability that this particular interval contains it."
            ),
            "incorrect": (
                "Select the ci_lower cell in the test_checkout_large variation row. "
                "That cell anchors the 95% confidence interval whose interpretation "
                "is about the long-run behaviour of the method, not a probability "
                "attached to this single interval."
            )
        }

        # Update overall feedback to reflect the new task
        ix['feedback']['correct']['message'] = (
            "Well done. The small-sample test cannot reject H0 because 0% lift falls "
            "inside its wide CI. The large-sample test is statistically significant "
            "(CI excludes 0%). The 95% CI lower bound anchors an interval whose meaning "
            "is about the long-run behaviour of the method: about 95% of such intervals "
            "would contain the true parameter across many repeated samples \u2014 not a "
            "95% probability attached to this one interval."
        )
        ix['feedback']['incorrect']['message'] = (
            "Check each task: (1) find the variation row where the CI contains 0% lift; "
            "(2) find the null_value_in_ci cell for the large-sample test; "
            "(3) find the ci_lower cell for the large-sample test variation row and recall "
            "that '95% confidence' describes the long-run behaviour of the method, not a "
            "probability attached to this single interval."
        )
        ix['feedback']['hints'] = [
            "null_value_in_ci = 'yes' means the CI contains 0% lift \u2014 H0 cannot be rejected.",
            (
                "'95% confidence' means that if the procedure were repeated across many samples, "
                "about 95% of the resulting intervals would contain the true parameter \u2014 "
                "it is not a probability attached to this specific interval."
            )
        ]
        break

with open('batches/final_batch_004_da_chunk2/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
