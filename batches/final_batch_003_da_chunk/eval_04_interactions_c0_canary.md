# Evaluation: 04_interactions — c0_canary (scoped re-evaluation after repair)

## Scope
Tile: `tile_stats_shape_outliers`
Artifact: `interactions.part.c0_canary.json`

## Repair findings checked

### Finding 3 (s05/practice-anchor) — RESOLVED
Two new tasks added: `task_shape_label` (labels the shape as right-skewed) and `task_mean_above_median` (places the mean on the tail side of the median). Both have correct answers (ORD-118, delivery_minutes=52), task feedback, and grading entries. The practice anchor success sentence ("labels the shape" and "places the mean on the tail side of the median") is now exercised.

### Finding 4 (s08/category_id) — RESOLVED
A third category `cat_both_possible` ("Both possible — needs investigation") was added. The correct answer is now `cat_both_possible`. The `wrong_category_message` correctly explains why selecting only one explanation is insufficient. This aligns with glossary fact f3 and misconception m1.

### Finding 5 (s08/practice-anchor) — RESOLVED
The interaction now requires the learner to select "Both possible — needs investigation," acknowledging both error-type and genuine-event explanations. The completion_message confirms both are plausible. The practice anchor success sentence is now exercised.

### Finding 6 (s05/feedback) — RESOLVED
Feedback and hints now reference the mean-vs-median relationship, which is tested by the new `task_mean_above_median` task. No orphaned references remain.

## Nothing-else-changed check
- s04, s07, s12, s13 interactions appear unchanged and structurally intact.
- All task_feedback entries present for all tasks in s05 and s08.
- Grading answers match task definitions.

## New observations

ADVISORY: s05 claims `stats.distribution_shape#assessment:recognize_symmetric_distribution` as an anchor/measure, but no task in s05 asks the learner to recognize a symmetric distribution (all tasks involve right-skewed data). This is a metadata tracking issue, not a learner-facing content error.

ADVISORY: `task_shape_label` and `task_mean_above_median` in s05 both resolve to the same cell (ORD-118, delivery_minutes=52). The prompts frame the selection differently, exercising distinct concepts, but the physical selection is identical.

## Verdict

VERDICT: PASS

ADVISORY s05/anchors: s05 claims assessment anchor `recognize_symmetric_distribution` but no task tests symmetric-distribution recognition → Remove the `recognize_symmetric_distribution` anchor and measure from s05, or add a task that asks the learner to identify whether a distribution is symmetric.
ADVISORY s05/task_overlap: `task_shape_label` and `task_mean_above_median` both target the same cell (ORD-118, 52 min) → Consider differentiating the target cells or merging into one task with a richer prompt.
