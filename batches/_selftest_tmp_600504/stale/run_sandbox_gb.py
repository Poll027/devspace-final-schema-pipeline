#!/usr/bin/env python3
"""Run sandbox checker for groupby_melt s05."""
import json
import sys
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts')

from checkers import sandbox

with open('batches/final_batch_009_da_pandas/scenario_asset_registry.json') as f:
    registry = json.load(f)

with open('batches/final_batch_009_da_pandas/tile_lessons/tile_pandas_groupby_melt.json') as f:
    lesson = json.load(f)

for step in lesson['steps']:
    if step['step_id'] == 'tile_pandas_groupby_melt.s05':
        print(f"Running sandbox for {step['step_id']}...")
        ix = step['interaction']
        result = sandbox.run_exercise(registry, ix)
        if result.problems:
            print(f"  Problems: {result.problems}")
        if result.provenance:
            ix['grading']['execution_provenance'] = result.provenance
            ix['grading']['hidden_checks'] = result.hidden_checks
            print(f"  Added provenance and {len(result.hidden_checks)} hidden checks")
        else:
            print(f"  No provenance (problems: {result.problems})")

with open('batches/final_batch_009_da_pandas/tile_lessons/tile_pandas_groupby_melt.json', 'w') as f:
    json.dump(lesson, f, indent=2)

print("Done")
