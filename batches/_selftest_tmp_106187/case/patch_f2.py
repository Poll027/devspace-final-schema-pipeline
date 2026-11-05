import json

with open('batches/final_batch_008_da_python_core/screens.part.c1.json') as f:
    data = json.load(f)

# Find tile_python_operators_conversion, step s01
tile = next(t for t in data['tiles'] if t['tile_id'] == 'tile_python_operators_conversion')
s01 = next(s for s in tile['steps'] if s['step_id'] == 'tile_python_operators_conversion.s01')

# The new prose block teaching f2 — insert between b01 and b02
new_prose_block = {
    "type": "prose",
    "block_id": "tile_python_operators_conversion.s01.b01b",
    "role": "definition",
    "text": "The // operator performs floor division: it divides and discards the fractional part, so 17 // 5 is 3. The % operator returns the remainder of the division, so 17 % 5 is 2. Together they let you split a quantity into whole units and a leftover — for example, 17 minutes is 3 complete five-minute slots with 2 minutes remaining.",
    "lineage": {
        "concept_ids": ["python.arithmetic_operators"],
        "fact_ids": ["python.arithmetic_operators#f2"],
        "teaching_block_ids": ["python.arithmetic_operators#tb1"],
        "anchors": []
    }
}

# Insert after b01 (index 0), before b02 (index 1)
s01['blocks'].insert(1, new_prose_block)

with open('batches/final_batch_008_da_python_core/screens.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Patch applied: inserted b01b prose block teaching f2 in s01")
print(f"s01 now has {len(s01['blocks'])} blocks")
