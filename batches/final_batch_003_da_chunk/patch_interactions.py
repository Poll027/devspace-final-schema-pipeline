"""
Patch interactions.part.c0_canary.json to fix BLOCKING findings 3, 4, 5 and ADVISORY finding 6.

Finding 3 (BLOCKING s05/practice-anchor):
  Add two tasks that make the learner identify the shape label and mean-vs-median relationship.

Finding 4 (BLOCKING s08/category_id):
  Add a third category "Both possible (needs investigation)" and make it the correct answer,
  so neither cat_data_error alone nor cat_genuine alone is accepted.

Finding 5 (BLOCKING s08/practice-anchor):
  Restructure so the learner must acknowledge both explanations by selecting the "both possible" category.

Finding 6 (ADVISORY s05/feedback):
  Remove references to "the median" from correct-feedback message and hint 2.
"""
import json, copy

with open('batches/final_batch_003_da_chunk/interactions.part.c0_canary.json') as f:
    data = json.load(f)

for tile in data['tiles']:
    for entry in tile['interactions']:
        sid = entry['step_id']
        ix = entry['interaction']

        # ── s05 fixes (Findings 3 & 6) ──────────────────────────────────────
        if sid == 'tile_stats_shape_outliers.s05':
            tasks = ix['public']['tasks']
            answers = ix['grading']['answers']
            task_feedback = ix['grading']['task_feedback']

            # Finding 3: add two new tasks
            # Task: identify the shape label (right-skewed)
            tasks.append({
                "task_id": "task_shape_label",
                "prompt": "Select the cell showing the delivery time that makes this distribution right-skewed — the value in the long tail that stretches to the right.",
                "target_kind": "cell"
            })
            # Task: identify the value that places the mean above the median
            tasks.append({
                "task_id": "task_mean_above_median",
                "prompt": "Select the cell showing the delivery time that pulls the mean above the median.",
                "target_kind": "cell"
            })

            # Grading answers for the two new tasks (ORD-118, delivery_minutes = 52)
            answers.append({
                "task_id": "task_shape_label",
                "row": {"where": {"order_id": "ORD-118"}, "occurrence": 0},
                "column": "delivery_minutes",
                "expect_value": 52
            })
            answers.append({
                "task_id": "task_mean_above_median",
                "row": {"where": {"order_id": "ORD-118"}, "occurrence": 0},
                "column": "delivery_minutes",
                "expect_value": 52
            })

            # Task feedback for the two new tasks
            task_feedback["task_shape_label"] = {
                "correct": "Correct. The 52-minute delivery at ORD-118 is the extreme value in the right tail that makes this distribution right-skewed.",
                "incorrect": "Not quite. Look for the value that stretches furthest to the right — the extreme value that creates the right tail and labels this distribution as right-skewed."
            }
            task_feedback["task_mean_above_median"] = {
                "correct": "Correct. The 52-minute extreme value pulls the mean toward the right tail, placing the mean above the median.",
                "incorrect": "Not quite. The mean is pulled toward extreme values. Find the extreme value in the right tail — it is what pulls the mean above the median."
            }

            # Finding 6 (ADVISORY): fix feedback that mentions "the median" without a median task
            ix['feedback']['correct']['message'] = (
                "Well done! You've identified the extreme value in the tail, the bulk of the distribution, "
                "and recognised that this distribution is right-skewed with the mean pulled above the median by that extreme value."
            )
            # Rewrite hint 2 — remove the median-calculation sentence
            ix['feedback']['hints'][1] = (
                "The extreme value in the right tail is what labels this distribution as right-skewed "
                "and pulls the mean toward the tail side."
            )

        # ── s08 fixes (Findings 4 & 5) ──────────────────────────────────────
        if sid == 'tile_stats_shape_outliers.s08':
            pub = ix['public']
            gr = ix['grading']

            # Finding 4 & 5: add a third category "Both possible" and make it the correct answer
            pub['categories'].append({
                "category_id": "cat_both_possible",
                "label": "Both possible — needs investigation"
            })

            # Update the issue to use cat_both_possible
            for iss in gr['issues']:
                if iss['issue_id'] == 'issue_outlier_80min':
                    iss['category_id'] = 'cat_both_possible'
                    iss['explanation'] = (
                        "The 80-minute delivery is extreme relative to the rest of the batch (18–28 min). "
                        "It could be a data-entry error (e.g. 8.0 typed as 80) or a genuine event such as a road closure. "
                        "Both explanations are plausible; the record must be examined before any decision is made."
                    )

            # Update wrong_category_message to explain why single-category answers are wrong
            gr['wrong_category_message'] = (
                "You've identified the outlier, but a single explanation is not enough. "
                "The 80-minute value could be a data-entry error or a genuine event — "
                "both are plausible, so the correct response is to flag it as needing investigation, "
                "not to commit to one explanation without checking the record."
            )

            # Update completion_message
            gr['completion_message'] = (
                "Well done! You've identified the extreme value and recognised that both a data-entry error "
                "and a genuine event are plausible explanations — the record must be examined before deciding."
            )

            # Update instructions to make clear the learner must consider both possibilities
            pub['instructions'] = (
                "The table shows delivery times for seven orders. "
                "Flag any values that appear extreme relative to the rest of the data, "
                "and classify each: if only a data error is plausible choose 'Possible data error'; "
                "if only a genuine event is plausible choose 'Genuine event'; "
                "if both explanations are plausible choose 'Both possible — needs investigation'."
            )

            # Update correct feedback to reflect the both-possible answer
            ix['feedback']['correct']['message'] = (
                "Excellent work. You've identified the extreme value and recognised that both a data-entry error "
                "and a genuine event are plausible explanations — the record needs examination before any action is taken."
            )

with open('batches/final_batch_003_da_chunk/interactions.part.c0_canary.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Patch applied.")
