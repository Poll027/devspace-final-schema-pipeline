#!/usr/bin/env python3
"""Patch screens.part.c1.json per repair-round findings."""
import json, copy

with open("batches/final_batch_007_da_nocode/screens.part.c1.json", "r") as f:
    data = json.load(f)

tile = data["tiles"][0]
steps = tile["steps"]

# ── Helper: find step by step_id ──────────────────────────────────────────────
def find_step(steps, step_id):
    for s in steps:
        if s["step_id"] == step_id:
            return s
    raise KeyError(f"Step not found: {step_id}")

# ══════════════════════════════════════════════════════════════════════════════
# BLOCKING FIX: s08 — add explicit prose block teaching full C.f3
# (all three intent types + "can be answered with data collected or already in hand")
# ══════════════════════════════════════════════════════════════════════════════
s08 = find_step(steps, "tile_stakeholder_framing_requirements.s08")

new_block = {
    "type": "prose",
    "block_id": "tile_stakeholder_framing_requirements.s08.b3",
    "role": "definition",
    "text": (
        "A well-formed statistical question makes clear the variable of interest, "
        "the group it focuses on, and its intent \u2014 whether that is describing the data, "
        "comparing a variable across two or more groups, or looking at an association "
        "between two variables \u2014 and can be answered with data collected or already in hand."
    ),
    "lineage": {
        "concept_ids": ["stakeholder.framing_analytical_question"],
        "fact_ids": ["stakeholder.framing_analytical_question#f3"],
        "teaching_block_ids": ["stakeholder.framing_analytical_question#tb3"]
    }
}

# Append after the existing blocks (before_after is b2, new prose is b3)
s08["blocks"].append(new_block)

print("✓ s08: added b3 prose block with full C.f3 definition")

# ══════════════════════════════════════════════════════════════════════════════
# ADVISORY FIX: s04/visual — add note to "after" diagram change_summary
# ══════════════════════════════════════════════════════════════════════════════
s04 = find_step(steps, "tile_stakeholder_framing_requirements.s04")

for block in s04["blocks"]:
    if block.get("type") == "before_after" and block.get("block_id") == "tile_stakeholder_framing_requirements.s04.b2":
        old_summary = block.get("change_summary", "")
        block["change_summary"] = (
            old_summary.rstrip(".")
            + ". (This is a first improvement \u2014 the next step adds the specific number and comparison.)"
        )
        print(f"✓ s04/visual: updated change_summary to note this is a first improvement")
        break

# ══════════════════════════════════════════════════════════════════════════════
# ADVISORY FIX: s18 — add lineage tags for concepts B, C, D facts
# ══════════════════════════════════════════════════════════════════════════════
s18 = find_step(steps, "tile_stakeholder_framing_requirements.s18")

# Additional fact_ids and teaching_block_ids to add for concepts B, C, D
extra_fact_ids = [
    "stakeholder.precise_finding_statement#f2",
    "stakeholder.precise_finding_statement#f4",
    "stakeholder.framing_analytical_question#f3",
    "stakeholder.framing_analytical_question#f1",
    "stakeholder.identifying_requirements#f1",
    "stakeholder.identifying_requirements#f2",
    "stakeholder.identifying_requirements#f3",
    "stakeholder.identifying_requirements#f4",
]
extra_tb_ids = [
    "stakeholder.precise_finding_statement#tb2",
    "stakeholder.framing_analytical_question#tb3",
    "stakeholder.identifying_requirements#tb2",
    "stakeholder.identifying_requirements#tb3",
]

# Update the prose block (b1) lineage
for block in s18["blocks"]:
    if block.get("block_id") == "tile_stakeholder_framing_requirements.s18.b1":
        existing_facts = block["lineage"]["fact_ids"]
        existing_tbs = block["lineage"]["teaching_block_ids"]
        for fid in extra_fact_ids:
            if fid not in existing_facts:
                existing_facts.append(fid)
        for tb in extra_tb_ids:
            if tb not in existing_tbs:
                existing_tbs.append(tb)
        print(f"✓ s18.b1: added lineage tags for concepts B, C, D")
        break

# Update the step-level lineage too
existing_step_facts = s18["lineage"]["fact_ids"]
existing_step_tbs = s18["lineage"]["teaching_block_ids"]
for fid in extra_fact_ids:
    if fid not in existing_step_facts:
        existing_step_facts.append(fid)
for tb in extra_tb_ids:
    if tb not in existing_step_tbs:
        existing_step_tbs.append(tb)
print(f"✓ s18 step lineage: added tags for concepts B, C, D")

# ══════════════════════════════════════════════════════════════════════════════
# Write output
# ══════════════════════════════════════════════════════════════════════════════
with open("batches/final_batch_007_da_nocode/screens.part.c1.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n✓ Patch complete — screens.part.c1.json written.")
