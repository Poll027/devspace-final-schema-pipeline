"""
Patch script for screens.part.c1.json repair round.

BLOCKING fix:
  - Remove "capstone.narrated_stakeholder_summary#f4" from:
      1. block-level lineage of tile_capstone_execution_narration_delivery.s05.p3
      2. step-level lineage of tile_capstone_execution_narration_delivery.s05

ADVISORY fixes:
  - s01 left-panel axis label: change "(0% – 30%)" to "(−5% – 30%)"
  - s10 CI bounds: Scenario A [0.28, 0.39] → [0.22, 0.50]; Scenario B [0.21, 0.31] → [0.09, 0.31]
    (Scenario B upper bound 0.31 already matches; lower bound 0.21 → 0.09)
    Also update alt_text to match.
"""

import json, copy

with open("batches/final_batch_004_da_chunk2/screens.part.c1.json", encoding="utf-8") as f:
    data = json.load(f)

BAD_FACT = "capstone.narrated_stakeholder_summary#f4"

for tile in data["tiles"]:
    if tile["tile_id"] == "tile_capstone_execution_narration_delivery":
        for step in tile["steps"]:
            if step["step_id"] == "tile_capstone_execution_narration_delivery.s05":
                # Fix step-level lineage
                if BAD_FACT in step["lineage"]["fact_ids"]:
                    step["lineage"]["fact_ids"].remove(BAD_FACT)
                    print(f"Removed {BAD_FACT} from s05 step-level lineage")
                # Fix block-level lineage for p3
                for block in step.get("blocks", []):
                    if block.get("block_id") == "tile_capstone_execution_narration_delivery.s05.p3":
                        if BAD_FACT in block["lineage"]["fact_ids"]:
                            block["lineage"]["fact_ids"].remove(BAD_FACT)
                            print(f"Removed {BAD_FACT} from s05.p3 block lineage")

    if tile["tile_id"] == "tile_stats_sample_size_significance":
        for step in tile["steps"]:
            # ADVISORY: s01 axis label fix
            if step["step_id"] == "tile_stats_sample_size_significance.s01":
                for block in step.get("blocks", []):
                    if block.get("type") == "side_by_side":
                        left = block.get("left", {})
                        if left.get("type") == "diagram":
                            for node in left.get("nodes", []):
                                if node.get("id") == "nl_small_axis":
                                    old = node["label"]
                                    node["label"] = "Lift estimate axis (\u22125% \u2013 30%)"
                                    print(f"s01 axis label: '{old}' -> '{node['label']}'")

            # ADVISORY: s10 CI bounds fix
            if step["step_id"] == "tile_stats_sample_size_significance.s10":
                for block in step.get("blocks", []):
                    if block.get("type") == "diagram" and block.get("diagram_kind") == "number_line":
                        for node in block.get("nodes", []):
                            if node.get("id") == "scenario_a_ci_low":
                                old = node["value"]
                                node["value"] = 0.22
                                print(f"s10 Scenario A ci_lower: {old} -> 0.22")
                            elif node.get("id") == "scenario_a_ci_high":
                                old = node["value"]
                                node["value"] = 0.50
                                print(f"s10 Scenario A ci_upper: {old} -> 0.50")
                            elif node.get("id") == "scenario_b_ci_low":
                                old = node["value"]
                                node["value"] = 0.09
                                print(f"s10 Scenario B ci_lower: {old} -> 0.09")
                            # scenario_b_ci_high is already 0.31 — no change needed
                        # Update alt_text
                        old_alt = block.get("alt_text", "")
                        new_alt = (
                            "Two number-line scenarios side by side. "
                            "Scenario A: 95% CI spans 0.22\u20130.50, with the null value 0.333 "
                            "falling inside the shaded band \u2014 fail to reject. "
                            "Scenario B: 95% CI spans 0.09\u20130.31, with the null value 0.333 "
                            "falling outside and above the band \u2014 reject, conclude proportion is lower than 0.333."
                        )
                        block["alt_text"] = new_alt
                        print(f"s10 alt_text updated")

with open("batches/final_batch_004_da_chunk2/screens.part.c1.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done.")
