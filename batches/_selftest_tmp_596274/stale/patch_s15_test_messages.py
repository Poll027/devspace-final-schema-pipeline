"""
Update test messages for s15 to match the new task.
"""
import json

path = 'batches/final_batch_012_da_viz/interactions.part.c1.json'
with open(path) as f:
    data = json.load(f)

for tile in data['tiles']:
    for ix in tile['interactions']:
        if ix['step_id'] == 'tile_viz_line_scatter_box.s15':
            interaction = ix['interaction']
            tests = interaction['grading']['tests']
            
            # Update t01 message
            tests[0]['message_on_fail'] = "Your figure should contain exactly one Axes with a box plot. Call `plt.boxplot([lagos_times, abuja_times, kano_times], labels=[city_1, city_2, city_3])`."
            
            # Update t02 message
            tests[1]['message_on_fail'] = "The tick labels should be ['Lagos', 'Abuja', 'Kano']. Make sure you pass `labels=[city_1, city_2, city_3]` to `plt.boxplot()`."
            
            # Update t04 message
            tests[2]['message_on_fail'] = "The medians should be [25.0, 27.5, 31.0] for Lagos, Abuja, and Kano. Check that you are passing the three arrays in the correct order: `[lagos_times, abuja_times, kano_times]`."
            
            print("Updated test messages for tile_viz_line_scatter_box.s15")
            break

with open(path, 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("Done.")
