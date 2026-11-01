"""
Patch screens.json: add a prose block teaching data.analysis_workflow#f7 to step s10,
so that f7 is taught by text before s11 and s12 test it.
"""
import json, pathlib, copy

B = pathlib.Path("batches/final_batch_007_da_nocode")

with open(B / "screens.json") as fh:
    screens = json.load(fh)

NEW_BLOCK = {
    "type": "prose",
    "block_id": "tile_data_quality_and_workflow.s10.b2",
    "role": "workflow",
    "text": (
        "This process is commonly iterative rather than strictly linear: "
        "earlier stages, such as inspecting or cleaning, may be revisited as "
        "later stages reveal new issues. If analyzing the Kwik Courier delivery "
        "data turns up a value that looks wrong, you go back and inspect or clean "
        "it before continuing, rather than treating each stage as done for good."
    ),
    "lineage": {
        "concept_ids": ["data.analysis_workflow"],
        "fact_ids": ["data.analysis_workflow#f7"],
        "teaching_block_ids": ["data.analysis_workflow#tb6"]
    }
}

patched = False
for tile in screens["tiles"]:
    if tile["tile_id"] != "tile_data_quality_and_workflow":
        continue
    for step in tile["steps"]:
        if step["step_id"] != "tile_data_quality_and_workflow.s10":
            continue
        # Add the new prose block
        step["blocks"].append(NEW_BLOCK)
        # Update step-level lineage fact_ids to include f7
        if "data.analysis_workflow#f7" not in step["lineage"]["fact_ids"]:
            step["lineage"]["fact_ids"].append("data.analysis_workflow#f7")
        # NOTE: do NOT add tb6 to step-level teaching_block_ids — the plan only
        # lists tb5 there, and the plan-conformance check would fail.
        patched = True
        print(f"Patched step {step['step_id']}: added prose block for f7")

if not patched:
    raise RuntimeError("Step s10 not found — nothing patched")

with open(B / "screens.json", "w") as fh:
    json.dump(screens, fh, indent=2, ensure_ascii=False)
    fh.write("\n")

print("screens.json written.")
