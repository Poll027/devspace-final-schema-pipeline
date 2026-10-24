#!/usr/bin/env python3
"""
Patch interactions.part.c0_canary.json for s05 advisory findings (revised):
1. RESTORE recognize_symmetric_distribution in measures and anchors (tile plan requires it),
   and ADD a task that tests it (task_symmetric_check targeting ORD-104, delivery_minutes=29).
2. KEEP the merge of task_shape_label + task_mean_above_median into one richer task
   (task_mean_above_median removed; task_shape_label gets merged prompt).
"""
import json

SRC = "batches/final_batch_003_da_chunk/interactions.part.c0_canary.json"

with open(SRC) as f:
    data = json.load(f)

tile = data["tiles"][0]
s05_entry = next(e for e in tile["interactions"] if e["step_id"] == "tile_stats_shape_outliers.s05")
ix = s05_entry["interaction"]

# ── Fix 1: RESTORE recognize_symmetric_distribution in measures ───────────────
# Check if it's already there; if not, add it back
caps = [m["capability"] for m in ix["measures"]]
if "recognize_symmetric_distribution" not in caps:
    # Insert after classify_skew_direction
    new_measures = []
    for m in ix["measures"]:
        new_measures.append(m)
        if m["capability"] == "classify_skew_direction":
            new_measures.append({
                "concept_id": "stats.distribution_shape",
                "capability": "recognize_symmetric_distribution",
                "fact_ids": ["f2"]
            })
    ix["measures"] = new_measures

# ── Fix 1: RESTORE recognize_symmetric_distribution in anchors ────────────────
if "stats.distribution_shape#assessment:recognize_symmetric_distribution" not in ix["anchors"]:
    # Insert after classify_skew_direction anchor
    new_anchors = []
    for a in ix["anchors"]:
        new_anchors.append(a)
        if "classify_skew_direction" in a:
            new_anchors.append("stats.distribution_shape#assessment:recognize_symmetric_distribution")
    ix["anchors"] = new_anchors

# ── Fix 1: ADD task_symmetric_check (tests f2 — recognize symmetric distribution)
# Target: ORD-104, delivery_minutes=29 (closest value to the median 29.5,
# the balance point that a symmetric distribution would have).
# Task asks learner to select the value nearest the distribution's center —
# demonstrating they understand symmetry means equal tails around a midpoint.
tasks = ix["public"]["tasks"]
task_ids = [t["task_id"] for t in tasks]

if "task_symmetric_check" not in task_ids:
    # Insert before task_shape_label (which is now the merged skew+mean task)
    new_tasks = []
    for t in tasks:
        if t["task_id"] == "task_shape_label":
            new_tasks.append({
                "task_id": "task_symmetric_check",
                "prompt": (
                    "Select the cell showing the delivery time closest to the median — "
                    "the value that would be the balance point if this distribution were symmetric."
                ),
                "target_kind": "cell"
            })
        new_tasks.append(t)
    ix["public"]["tasks"] = new_tasks

# ── Fix 1: ADD answer for task_symmetric_check ────────────────────────────────
answers = ix["grading"]["answers"]
answer_task_ids = [a["task_id"] for a in answers]
if "task_symmetric_check" not in answer_task_ids:
    # Insert before task_shape_label answer
    new_answers = []
    for a in answers:
        if a["task_id"] == "task_shape_label":
            new_answers.append({
                "task_id": "task_symmetric_check",
                "row": {
                    "where": {"order_id": "ORD-104"},
                    "occurrence": 0
                },
                "column": "delivery_minutes",
                "expect_value": 29
            })
        new_answers.append(a)
    ix["grading"]["answers"] = new_answers

# ── Fix 1: ADD task_feedback for task_symmetric_check ─────────────────────────
tf = ix["grading"]["task_feedback"]
if "task_symmetric_check" not in tf:
    tf["task_symmetric_check"] = {
        "correct": (
            "Correct. 29 minutes (ORD-104) is the closest value to the median of 29.5 min — "
            "the balance point around which a symmetric distribution would trail off equally "
            "in both directions."
        ),
        "incorrect": (
            "Not quite. A symmetric distribution trails off by roughly equal amounts in both "
            "directions from its centre. Look for the value closest to the midpoint of the data."
        )
    }

# ── Fix 2: Merge task_shape_label + task_mean_above_median ────────────────────
# Replace task_shape_label with a richer merged prompt; drop task_mean_above_median.
tasks = ix["public"]["tasks"]
new_tasks = []
for t in tasks:
    if t["task_id"] == "task_shape_label":
        new_tasks.append({
            "task_id": "task_shape_label",
            "prompt": (
                "Select the cell showing the delivery time that makes this distribution "
                "right-skewed — the extreme value in the long tail that also pulls the "
                "mean above the median."
            ),
            "target_kind": "cell"
        })
    elif t["task_id"] == "task_mean_above_median":
        pass  # drop — merged into task_shape_label
    else:
        new_tasks.append(t)
ix["public"]["tasks"] = new_tasks

# ── Fix 2: Drop task_mean_above_median answer ─────────────────────────────────
ix["grading"]["answers"] = [
    a for a in ix["grading"]["answers"] if a["task_id"] != "task_mean_above_median"
]

# ── Fix 2: Drop task_mean_above_median feedback; update task_shape_label ──────
tf = ix["grading"]["task_feedback"]
tf.pop("task_mean_above_median", None)
tf["task_shape_label"] = {
    "correct": (
        "Correct. The 52-minute delivery at ORD-118 is the extreme value in the right "
        "tail that makes this distribution right-skewed and pulls the mean above the median."
    ),
    "incorrect": (
        "Not quite. Look for the value that stretches furthest to the right — the extreme "
        "value that creates the right tail, labels this distribution as right-skewed, and "
        "pulls the mean above the median."
    )
}

with open(SRC, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
