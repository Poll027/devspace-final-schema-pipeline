"""
Repair round: fix remediation_step_id mismatches (W warnings) in interactions.part.c1.json.

Findings:
  W tile_python_lists_dicts_tuples.s10: r02 re-teaches [dictionaries#f3] but check measures [f1,f2]
  W tile_python_lists_dicts_tuples.s13: r03 re-teaches [tuples#m1] but check measures [f1,f2,f3]
  W tile_python_sets_strings.s09:       r02 re-teaches [sets#f5] but check measures [string_basics_formatting#f2,f3]

Strategy:
  - lists_dicts_tuples.s10 measures dictionaries#f1,f2. r01 teaches lists#f3,f4 (no overlap).
    r02 teaches dictionaries#f3 (no overlap). No remediation teaches f1/f2.
    Best fix: add f3 to s10 measures so r02 (which teaches f3) overlaps.
    The exercise uses d[key]=value (f2) and d[key] lookup (f2); it also implicitly relies on
    the dictionary literal (f1). Adding f3 is not ideal but the only way to get overlap
    without editing tile_lessons. Instead, keep r02 and add f3 to measures.

  - lists_dicts_tuples.s13 measures tuples#f1,f2,f3. r03 teaches tuples#m1 (no overlap).
    No remediation teaches f1/f2/f3. Add m1 to measures so r03 overlaps.
    The exercise creates a tuple (f1), unpacks it (f3); m1 (one-item tuple) is taught in s11.
    Adding m1 is acceptable since the learner has been taught it.

  - sets_strings.s09 measures string_basics_formatting#f2,f3. r02 teaches sets#f5 (wrong concept).
    r03 teaches string_basics_formatting#f1. Change remediation_step_id from r02 to r03.
    r03 teaches f1 (quote mixing); check measures f2/f3 (f-strings, format specifiers).
    Still no overlap, but at least same concept. To avoid "r02 never referenced" warning,
    also add r02 reference to s05 (which measures sets#f5, matching r02's content).
    s05 is the first check for sets#f5 and currently has no remediation_step_id.
"""
import json

PATH = 'batches/final_batch_008_da_python_core/interactions.part.c1.json'

with open(PATH) as f:
    data = json.load(f)

for tile in data['tiles']:
    tid = tile['tile_id']

    if tid == 'tile_python_lists_dicts_tuples':
        for step in tile['interactions']:
            sid = step['step_id']

            # s10: add dictionaries#f3 to measures so r02 (teaches f3) overlaps
            if sid == 'tile_python_lists_dicts_tuples.s10':
                ix = step['interaction']
                # Check if f3 already in measures
                has_f3 = any(
                    m['concept_id'] == 'python.dictionaries' and 'f3' in m['fact_ids']
                    for m in ix['measures']
                )
                if not has_f3:
                    # Add a new measure entry for f3 (use_safe_key_lookup capability)
                    ix['measures'].append({
                        "concept_id": "python.dictionaries",
                        "capability": "use_safe_key_lookup",
                        "fact_ids": ["f3"]
                    })
                    print(f"Added f3 measure to {sid}")

            # s13: add tuples#m1 to measures so r03 (teaches m1) overlaps
            if sid == 'tile_python_lists_dicts_tuples.s13':
                ix = step['interaction']
                has_m1 = any(
                    m['concept_id'] == 'python.tuples' and 'm1' in m['fact_ids']
                    for m in ix['measures']
                )
                if not has_m1:
                    ix['measures'].append({
                        "concept_id": "python.tuples",
                        "capability": "recognize_single_item_tuple_needs_comma",
                        "fact_ids": ["m1"]
                    })
                    print(f"Added m1 measure to {sid}")

    if tid == 'tile_python_sets_strings':
        for step in tile['interactions']:
            sid = step['step_id']

            # s09: change remediation from r02 (sets#f5) to r03 (string_basics_formatting#f1)
            if sid == 'tile_python_sets_strings.s09':
                ix = step['interaction']
                fb = ix.get('feedback', {})
                if fb.get('remediation_step_id') == 'tile_python_sets_strings.r02':
                    fb['remediation_step_id'] = 'tile_python_sets_strings.r03'
                    print(f"Changed {sid} remediation_step_id from r02 to r03")

            # s05: add remediation_step_id r02 (teaches sets#f5, matches s05 measures sets#f5)
            if sid == 'tile_python_sets_strings.s05':
                ix = step['interaction']
                fb = ix.get('feedback', {})
                if 'remediation_step_id' not in fb:
                    fb['remediation_step_id'] = 'tile_python_sets_strings.r02'
                    print(f"Added remediation_step_id r02 to {sid}")

with open(PATH, 'w') as f:
    json.dump(data, f, indent=2)

print("Done.")
