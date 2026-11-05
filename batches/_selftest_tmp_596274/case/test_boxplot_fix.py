#!/usr/bin/env python3
"""Test that the boxplot solution runs without errors."""

import sys
import json
from pathlib import Path

# Add the scripts directory to the path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "00_FINAL_PIPELINE_CORE" / "scripts"))

from checkers.sandbox import run_exercise

# Load the registry
registry_path = Path("scenario_asset_registry.json")
with open(registry_path) as f:
    registry = json.load(f)

# Load the interactions file
with open("interactions.part.c1.json") as f:
    data = json.load(f)

# Find the boxplot interaction
for tile in data['tiles']:
    for item in tile['interactions']:
        if item['step_id'] == 'tile_viz_line_scatter_box.s15':
            ix = item['interaction']
            print(f"Testing interaction: {item['step_id']}")
            print(f"Type: {ix['type']}")
            
            # Run the exercise
            try:
                outcome = run_exercise(registry, ix)
                
                if outcome.problems:
                    print("\nPROBLEMS:")
                    for p in outcome.problems:
                        print(f"  - {p}")
                    sys.exit(1)
                else:
                    print(f"\nSUCCESS: {outcome.tests_passed}/{outcome.tests_total} tests passed")
                    if outcome.unverified:
                        print(f"  (unverified: {outcome.unverified})")
                    sys.exit(0)
                    
            except Exception as e:
                print(f"\nERROR: {e}")
                import traceback
                traceback.print_exc()
                sys.exit(1)

print("Interaction not found!")
sys.exit(1)
