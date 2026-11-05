#!/usr/bin/env python3
"""Better assembly for the two tiles using existing tile as template."""

import json
import sys
import copy
from pathlib import Path
import hashlib

sys.path.insert(0, '../../00_FINAL_PIPELINE_CORE/scripts')
from finlib import load

B = Path('.')

# Load data
ctx = load(B / "batch_run_context.json")
bundles_data = load(B / ctx["glossary_bundle_file"])
plans = {t["tile_id"]: t for t in load(B / "tile_plans.json")["tiles"]}
registry = load(B / "scenario_asset_registry.json")
screens = {t["tile_id"]: t for t in load(B / "screens.json")["tiles"]}
inters = {t["tile_id"]: {i["step_id"]: i["interaction"] for i in t["interactions"]} for t in load(B / "interactions.json")["tiles"]}

# Load an existing tile as template
with open(B / "tile_lessons" / "tile_viz_figures_layout_plotting.json", 'r') as f:
    template = json.load(f)

# Tiles to assemble
target_tiles = ['tile_viz_custom_multi_panel', 'tile_viz_seaborn_stats_themes']

def compute_content_hash(tile):
    """Compute content hash for a tile."""
    # Simplified version - just hash the JSON
    content = json.dumps(tile, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(content.encode()).hexdigest()

for tile_id in target_tiles:
    print(f"Assembling {tile_id}...")
    
    plan, sc, ix = plans[tile_id], screens.get(tile_id), inters.get(tile_id, {})
    if not sc:
        print(f"  ERROR: no screens for {tile_id}")
        continue
    
    steps = copy.deepcopy(sc["steps"])
    
    # Add interactions to steps
    for s in steps:
        if s["step_id"] in ix:
            s["interaction"] = copy.deepcopy(ix[s["step_id"]])
            if s["interaction"]["type"] == "code_exercise":
                s["interaction"]["grading"].pop("execution_provenance", None)
                s["interaction"]["grading"].pop("hidden_checks", None)
    
    rem = copy.deepcopy(sc.get("remediation_steps", []))
    
    # Collect used block types and interaction types
    def iter_blocks(blocks):
        for b in blocks:
            yield b
            if b["type"] == "side_by_side":
                for col in b.get("columns", []):
                    yield from iter_blocks(col.get("blocks", []))
    
    used_blocks = sorted({b["type"] for s in steps + rem for b in iter_blocks(s.get("blocks", []))})
    used_ix = sorted({s["interaction"]["type"] for s in steps if "interaction" in s})
    runtimes = sorted({s["interaction"]["public"]["runtime"]["kind"] for s in steps if s.get("interaction", {}).get("type") == "code_exercise"})
    
    # Collect asset IDs
    asset_ids = set()
    for s in steps:
        if s.get("interaction", {}).get("type") == "code_exercise":
            for mount in s["interaction"].get("workspace", {}).get("asset_mounts", []):
                asset_ids.add(mount["asset_ref"]["asset_id"])
    
    # Build glossary bundle hashes
    glossary_bundle_hashes = {}
    for concept_id in plan["concept_ids"]:
        # Find the concept in bundles
        for bundle in bundles_data.get("bundles", []):
            if bundle["context"]["concept_id"] == concept_id:
                # Compute hash
                content = json.dumps(bundle, sort_keys=True, ensure_ascii=False)
                glossary_bundle_hashes[concept_id] = hashlib.sha256(content.encode()).hexdigest()
                break
    
    # Build summary string
    concept_names = []
    for concept_id in plan["concept_ids"]:
        for bundle in bundles_data.get("bundles", []):
            if bundle["context"]["concept_id"] == concept_id:
                concept_names.append(bundle["context"]["concept_name"])
                break
    summary = f"Learn {', '.join(concept_names)}."
    
    # Build tile
    tile = {
        "schema_version": "0.1.0",
        "kind": "tile_lesson",
        "path_id": ctx["path_id"],
        "tile_id": tile_id,
        "title": plan["title"],
        "summary": summary,
        "concept_ids": plan["concept_ids"],
        "steps": steps,
        "remediation_steps": rem,
        "source": {
            "glossary_batch_id": template["source"]["glossary_batch_id"],
            "toc_freeze_hash": template["source"]["toc_freeze_hash"],
            "glossary_bundle_hashes": glossary_bundle_hashes,
            "scenario_registry_hash": template["source"]["scenario_registry_hash"],
        },
        "requires": {
            "min_player_version": "0.1.0",
            "packs": ["core"],
            "block_types": used_blocks,
            "interaction_types": used_ix,
            "runtimes": runtimes,
            "asset_ids": sorted(asset_ids),
        },
        "toc_location": {
            "region_id": plan["region_id"],
            "terrain_id": plan["terrain_id"],
        },
        "completion": {
            "rule": "all_required_steps_complete",
            "reward": {"gems": 100},  # Placeholder
            "next_tile_id": plan.get("next_tile_id"),
        },
        "pacing": {
            "estimated_minutes": 10.0,  # Placeholder
        },
    }
    
    # Compute content hash
    tile["content_hash"] = compute_content_hash(tile)
    
    # Write tile
    (B / "tile_lessons").mkdir(exist_ok=True)
    with open(B / "tile_lessons" / f"{tile_id}.json", 'w') as f:
        json.dump(tile, f, indent=2, ensure_ascii=False)
    
    print(f"  Written to tile_lessons/{tile_id}.json")

print("\nAssembly complete.")
