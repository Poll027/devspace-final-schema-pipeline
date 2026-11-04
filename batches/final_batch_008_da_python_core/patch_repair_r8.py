"""Repair round patch for interactions.part.c2.json.

Changes (advisory fixes only — reword/delete/move/cite, no new claims):

1. tile_python_comprehensions_iterating/s03:
   Remove `write_dict_comprehension(f3)` from MEASURES and its anchor,
   because the exercise only involves a list comprehension.

2. tile_python_comprehensions_iterating/s06:
   Change MEASURES capability from `loop_over_key_value_pairs(f2)` to
   `loop_over_keys_or_sequence_items(f1)` (remove f4 too — tuples not tested),
   and update the anchor accordingly, because the exercise uses direct key
   iteration with d[key] lookup, not .items().

3. tile_python_while_loop_control/s04:
   Remove `remediation_step_id` from feedback because r01 re-teaches f2
   (body must update condition variable) but s04 measures f1
   (write a while loop with a condition) — no available remediation step
   covers f1.

4. tile_python_comprehensions_iterating/s06:
   Remove `remediation_step_id` from feedback because r02 re-teaches f3
   (set ordering) but s06 measures f1/f2/f4 (dict/tuple iteration) —
   no available remediation step covers those facts.
"""
import json
from pathlib import Path

PATH = Path('batches/final_batch_008_da_python_core/interactions.part.c2.json')

with open(PATH) as f:
    d = json.load(f)

for tile in d['tiles']:
    tid = tile['tile_id']

    if tid == 'tile_python_comprehensions_iterating':
        for ix_entry in tile['interactions']:
            sid = ix_entry['step_id']
            ix = ix_entry['interaction']

            # Fix 1: s03 — remove write_dict_comprehension from measures and anchors
            if sid == 'tile_python_comprehensions_iterating.s03':
                ix['measures'] = [
                    m for m in ix['measures']
                    if m['capability'] != 'write_dict_comprehension'
                ]
                ix['anchors'] = [
                    a for a in ix['anchors']
                    if 'write_dict_comprehension' not in a
                ]
                print(f"[s03] measures now: {[m['capability'] for m in ix['measures']]}")
                print(f"[s03] anchors now: {ix['anchors']}")

            # Fix 2 + Fix 4: s06 — change measures to loop_over_keys_or_sequence_items(f1)
            # and remove remediation_step_id
            if sid == 'tile_python_comprehensions_iterating.s06':
                ix['measures'] = [
                    {
                        'concept_id': 'python.iterating_collections',
                        'capability': 'loop_over_keys_or_sequence_items',
                        'fact_ids': ['f1']
                    }
                ]
                ix['anchors'] = [
                    a for a in ix['anchors']
                    if 'loop_over_key_value_pairs' not in a
                ]
                # Remove remediation_step_id (r02 re-teaches f3, not f1)
                if 'remediation_step_id' in ix['feedback']:
                    del ix['feedback']['remediation_step_id']
                print(f"[s06] measures now: {[m['capability'] for m in ix['measures']]}")
                print(f"[s06] anchors now: {ix['anchors']}")
                print(f"[s06] feedback keys: {list(ix['feedback'].keys())}")

    if tid == 'tile_python_while_loop_control':
        for ix_entry in tile['interactions']:
            sid = ix_entry['step_id']
            ix = ix_entry['interaction']

            # Fix 3: s04 — remove remediation_step_id (r01 re-teaches f2, not f1)
            if sid == 'tile_python_while_loop_control.s04':
                if 'remediation_step_id' in ix['feedback']:
                    del ix['feedback']['remediation_step_id']
                print(f"[s04] feedback keys: {list(ix['feedback'].keys())}")

with open(PATH, 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
    f.write('\n')

print("Patch applied.")
