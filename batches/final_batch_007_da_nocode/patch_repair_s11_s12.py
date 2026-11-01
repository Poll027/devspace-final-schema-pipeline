#!/usr/bin/env python3
"""
Repair patch for s11 and s12 in tile_data_quality_and_workflow.
Finding: s11 and s12 test data.analysis_workflow#f7 but no earlier step
has taught it by text.

Fix: The hint in s11 referenced "the workflow diagram" (a visual), not the
text that teaches f7. Update the hint to reference the text teaching from
s10 (the iterative/loop-back prose block). No answer key or measures change
is needed because s10.b2 teaches f7 by text before s11 is reached.
"""
import json, pathlib

path = pathlib.Path("batches/final_batch_007_da_nocode/interactions.part.c0_canary.json")
d = json.loads(path.read_text())

for tile in d["tiles"]:
    if tile["tile_id"] != "tile_data_quality_and_workflow":
        continue
    for entry in tile["interactions"]:
        sid = entry["step_id"]
        ix = entry["interaction"]

        if sid == "tile_data_quality_and_workflow.s11":
            # Replace the hint that pointed at the visual diagram with one
            # that points at the text taught in s10 about the iterative process.
            ix["feedback"]["hints"] = [
                "Recall what you read about the workflow being iterative rather than strictly linear — what does that mean when a suspicious value turns up during analysis?",
                "Earlier stages such as inspecting or cleaning may be revisited when later stages reveal new issues — which stage would you return to?"
            ]

        if sid == "tile_data_quality_and_workflow.s12":
            # The follow-up prompt already tests the loop-back correctly.
            # Update the second hint to reference the text (not the diagram)
            # so it is grounded in the prose teaching of f7.
            ix["feedback"]["hints"] = [
                "Which stage must come first — before any data is touched? And which stage is always last?",
                "Are analyze and visualize the same step, or are they two distinct stages? And what does the workflow do when a suspicious value appears during analysis?"
            ]

path.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
print("Patch applied.")
