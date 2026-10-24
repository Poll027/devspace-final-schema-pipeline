#!/usr/bin/env python3
"""
Patch interactions.part.c0_canary.json for s05 advisory findings:
1. Remove recognize_symmetric_distribution from measures and anchors.
2. Merge task_shape_label + task_mean_above_median into one richer task
   (task_shape_label kept, task_mean_above_median removed; same answer key cell).
"""
import json, copy

SRC = "batches/final_batch_003_da_chunk/interactions.part.c0_canary.json"

with open(SRC) as f:
    data = json.load(f)

# Navigate to s05 interaction
tile = data["tiles"][0]
s05_entry = next(e for e in tile["interactions"] if e["step_id"] == "tile_stats_shape_outliers.s05")
ix = s05_entry["interaction"]

# ── Fix 1: remove recognize_symmetric_distribution from measures ──────────────
ix["measures"] = [
    m for m in ix["measures"]
    if m["capability"] != "recognize_symmetric_distribution"
]

# ── Fix 1: remove recognize_symmetric_distribution from anchors ──────────────
ix["anchors"] = [
    a for a in ix["anchors"]
    if "recognize_symmetric_distribution" not in a
]

# ── Fix 2: merge task_shape_label + task_mean_above_median ───────────────────
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

# ── Fix 2: drop task_mean_above_median answer; keep task_shape_label answer ──
answers = ix["grading"]["answers"]
ix["grading"]["answers"] = [
    a for a in answers if a["task_id"] != "task_mean_above_median"
]

# ── Fix 2: drop task_mean_above_median task_feedback; update task_shape_label ─
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
