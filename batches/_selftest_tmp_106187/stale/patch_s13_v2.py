import json

files = [
    'batches/final_batch_008_da_python_core/interactions.part.c1.json',
    'batches/final_batch_008_da_python_core/interactions.json',
]

for fpath in files:
    with open(fpath) as f:
        data = json.load(f)

    patched = False
    for tile in data['tiles']:
        if tile['tile_id'] == 'tile_python_lists_dicts_tuples':
            for step in tile['interactions']:
                if step['step_id'] == 'tile_python_lists_dicts_tuples.s13':
                    ix = step['interaction']
                    caps = [m['capability'] for m in ix['measures']]
                    if 'recognize_tuple_immutability' not in caps:
                        ix['measures'].append({
                            "concept_id": "python.tuples",
                            "capability": "recognize_tuple_immutability",
                            "fact_ids": ["f2"]
                        })
                        ix['anchors'].append("python.tuples#assessment:recognize_tuple_immutability")
                        patched = True
                        print(f"{fpath}: patched s13")
                    else:
                        print(f"{fpath}: s13 already has recognize_tuple_immutability")

    with open(fpath, 'w') as f:
        json.dump(data, f, indent=2)

print("Done.")
