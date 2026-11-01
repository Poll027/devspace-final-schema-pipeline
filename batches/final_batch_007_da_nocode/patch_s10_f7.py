import json, copy

with open('batches/final_batch_007_da_nocode/screens.part.c0_canary.json') as f:
    data = json.load(f)

tile = data['tiles'][0]
assert tile['tile_id'] == 'tile_data_quality_and_workflow'

for step in tile['steps']:
    if step['step_id'] == 'tile_data_quality_and_workflow.s10':
        # Add a prose block teaching f7 (iterative loop-back) via tb6
        new_block = {
            "type": "prose",
            "block_id": "tile_data_quality_and_workflow.s10.b2",
            "role": "workflow",
            "text": (
                "This process is commonly iterative rather than strictly linear. "
                "If analyzing the delivery data turns up a value that looks wrong, "
                "you go back and inspect or clean it before continuing — earlier stages "
                "may be revisited as later stages reveal new issues."
            ),
            "lineage": {
                "concept_ids": ["data.analysis_workflow"],
                "fact_ids": ["data.analysis_workflow#f7"],
                "teaching_block_ids": ["data.analysis_workflow#tb6"]
            }
        }
        step['blocks'].append(new_block)

        # Update step-level lineage to include f7 and tb6
        if "data.analysis_workflow#f7" not in step['lineage']['fact_ids']:
            step['lineage']['fact_ids'].append("data.analysis_workflow#f7")
        if "data.analysis_workflow#tb6" not in step['lineage']['teaching_block_ids']:
            step['lineage']['teaching_block_ids'].append("data.analysis_workflow#tb6")
        break

with open('batches/final_batch_007_da_nocode/screens.part.c0_canary.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Patch applied.")

# Verify
with open('batches/final_batch_007_da_nocode/screens.part.c0_canary.json') as f:
    data2 = json.load(f)
tile2 = data2['tiles'][0]
for step in tile2['steps']:
    if step['step_id'] == 'tile_data_quality_and_workflow.s10':
        print("s10 blocks:", [b['block_id'] for b in step.get('blocks',[])])
        print("s10 lineage fact_ids:", step['lineage']['fact_ids'])
        print("s10 lineage tb_ids:", step['lineage']['teaching_block_ids'])
        for b in step['blocks']:
            if b['type'] == 'prose':
                words = len(b['text'].split())
                print(f"  {b['block_id']}: {words} words")
