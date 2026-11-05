import json, re

with open('batches/final_batch_012_da_viz/interactions.part.c1.json', 'r') as f:
    data = json.load(f)

# Find the s15 interaction in tile_viz_line_scatter_box
for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_line_scatter_box':
        for item in tile['interactions']:
            if item['step_id'] == 'tile_viz_line_scatter_box.s15':
                ix = item['interaction']
                pub = ix['public']

                # 1. Fix prompt
                pub['prompt'] = pub['prompt'].replace('tick_labels', 'labels')

                # 2. Fix starter file content
                for f_item in pub['workspace']['files']:
                    if f_item['path'] == 'solution.py':
                        f_item['content'] = f_item['content'].replace(
                            '# Call plt.boxplot() with all three arrays and tick_labels parameter',
                            '# Call plt.boxplot() with all three arrays and labels parameter'
                        ).replace('tick_labels', 'labels')

                # 3. Fix allowed_syntax list
                pub['constraints']['allowed_syntax'] = [
                    entry.replace('tick_labels=[...]', 'labels=[...]')
                    for entry in pub['constraints']['allowed_syntax']
                ]

                # 4. Fix grading solution_files
                for sf in ix['grading']['solution_files']:
                    sf['content'] = sf['content'].replace('tick_labels', 'labels')

                # 5. Fix test message_on_fail
                for test in ix['grading']['tests']:
                    if 'message_on_fail' in test:
                        test['message_on_fail'] = test['message_on_fail'].replace('tick_labels', 'labels')

                # 6. Fix feedback messages and hints
                fb = ix['feedback']
                fb['correct']['message'] = fb['correct']['message'].replace('tick_labels', 'labels')
                fb['incorrect']['message'] = fb['incorrect']['message'].replace('tick_labels', 'labels')
                fb['hints'] = [h.replace('tick_labels', 'labels') for h in fb['hints']]

                print("Patched s15 interaction successfully.")
                break

with open('batches/final_batch_012_da_viz/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("File written.")
