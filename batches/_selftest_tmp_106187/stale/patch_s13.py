import json

with open('batches/final_batch_008_da_python_core/interactions.part.c1.json') as f:
    data = json.load(f)

for tile in data['tiles']:
    if tile['tile_id'] == 'tile_python_lists_dicts_tuples':
        for step in tile['interactions']:
            if step['step_id'] == 'tile_python_lists_dicts_tuples.s13':
                ix = step['interaction']

                # Add recognize_tuple_immutability to measures
                ix['measures'].append({
                    "concept_id": "python.tuples",
                    "capability": "recognize_tuple_immutability",
                    "fact_ids": ["f2"]
                })

                # Add the assessment anchor
                ix['anchors'].append("python.tuples#assessment:recognize_tuple_immutability")

                print("Patched s13 measures:", [m['capability'] for m in ix['measures']])
                print("Patched s13 anchors:", ix['anchors'])

with open('batches/final_batch_008_da_python_core/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Done.")
