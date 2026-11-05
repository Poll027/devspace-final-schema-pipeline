import json, re

with open('batches/final_batch_012_da_viz/interactions.part.c1.json') as f:
    data = json.load(f)

for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_line_scatter_box':
        for item in tile['interactions']:
            if item['step_id'] == 'tile_viz_line_scatter_box.s15':
                ix = item['interaction']
                for t in ix['grading']['tests']:
                    if 'message_on_fail' in t:
                        t['message_on_fail'] = t['message_on_fail'].replace(
                            "`labels=[city_1, city_2, city_3]`",
                            "`tick_labels=[city_1, city_2, city_3]`"
                        )
                        print(f"Test {t['test_id']} message_on_fail:", t['message_on_fail'])

with open('batches/final_batch_012_da_viz/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("File written.")
