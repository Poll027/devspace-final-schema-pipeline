"""
Update feedback for s15 to match the new task (writing the boxplot call).
"""
import json

path = 'batches/final_batch_012_da_viz/interactions.part.c1.json'
with open(path) as f:
    data = json.load(f)

NEW_FEEDBACK = {
    "correct": {
        "message": "Excellent! You called `plt.boxplot([lagos_times, abuja_times, kano_times], labels=[city_1, city_2, city_3])` to draw three side-by-side boxes, each labeled with its city name and showing the full distribution of delivery times for that city."
    },
    "incorrect": {
        "message": "Call `plt.boxplot([lagos_times, abuja_times, kano_times], labels=[city_1, city_2, city_3])` — pass all three arrays as a list, and use `labels=` to name each box."
    },
    "hints": [
        "Pass a list of three arrays to `plt.boxplot()`: `[lagos_times, abuja_times, kano_times]`.",
        "Add `labels=[city_1, city_2, city_3]` to label each box with its city name."
    ]
}

for tile in data['tiles']:
    for ix in tile['interactions']:
        if ix['step_id'] == 'tile_viz_line_scatter_box.s15':
            interaction = ix['interaction']
            interaction['feedback'] = NEW_FEEDBACK
            print("Updated feedback for tile_viz_line_scatter_box.s15")
            break

with open(path, 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("Done.")
