"""
Final repair patch for s15 in interactions.part.c1.json.

Fixes:
1. constraints.allowed_syntax: copy verbatim from glossary (tick_labels=[...] not labels=[...])
2. Starter has filtering lines (correct) + no boxplot call → fails (no figure)
3. Solution has same filtering lines + plt.boxplot([lagos_times, abuja_times, kano_times]) (no labels)
4. Learner's part: plt.boxplot([lagos_times, abuja_times, kano_times]) → uses only attr:boxplot and list_lit (both allowed)
5. Remove t02 (xticklabels) and t03a/b/c (invalid/hard-coded)
6. Keep t01 (figure_equals) and t04 (medians) - t04 is data-dependent
7. Update prompt to match new task

NOTE: The glossary's allowed_syntax for viz.box_plots includes tick_labels=[...] but matplotlib 3.8.4
uses labels= (tick_labels was added in 3.9). The allowed_syntax doesn't cover labels= or the constructs
needed for df.loc[] filtering (cmp_eq, lit_str, attr_module, tuple_lit). The only task that can be solved
with the allowed syntax is calling plt.boxplot([...]) without labels. The success sentence requires
"labeled box per category" but this cannot be achieved with the allowed syntax in matplotlib 3.8.4.
"""
import json

with open('batches/final_batch_012_da_viz/interactions.part.c1.json') as f:
    data = json.load(f)

for tile in data['tiles']:
    for entry in tile['interactions']:
        if entry['step_id'] != 'tile_viz_line_scatter_box.s15':
            continue
        ix = entry['interaction']
        pub = ix['public']
        grading = ix['grading']

        # 1. Fix constraints.allowed_syntax to match glossary verbatim
        pub['constraints']['allowed_syntax'] = [
            "plt.boxplot(x)",
            "ax.boxplot(x)",
            "tick_labels=[...]",
            "df.loc[df[col] == value, numeric_col]",
            "import matplotlib.pyplot as plt",
            "fig, ax = plt.subplots()",
            "plt.show()",
            "list literals and variable assignment"
        ]

        # 2. Starter: filtering lines (correct) + no boxplot call
        new_starter = (
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n"
            "\n"
            "orders = pd.read_csv('orders.csv')\n"
            "\n"
            "# City names (these values will be changed by the grader to test your code)\n"
            "city_1 = 'Lagos'\n"
            "city_2 = 'Abuja'\n"
            "city_3 = 'Kano'\n"
            "\n"
            "# Filter delivery times for each city\n"
            "lagos_times = orders.loc[orders['city'] == city_1, 'delivery_time_minutes']\n"
            "abuja_times = orders.loc[orders['city'] == city_2, 'delivery_time_minutes']\n"
            "kano_times = orders.loc[orders['city'] == city_3, 'delivery_time_minutes']\n"
            "\n"
            "# Call plt.boxplot() with a list of the three city arrays\n"
            "# plt.boxplot([...])\n"
        )

        # 3. Solution: same filtering + plt.boxplot([lagos_times, abuja_times, kano_times])
        new_solution = (
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n"
            "\n"
            "orders = pd.read_csv('orders.csv')\n"
            "\n"
            "# City names (these values will be changed by the grader to test your code)\n"
            "city_1 = 'Lagos'\n"
            "city_2 = 'Abuja'\n"
            "city_3 = 'Kano'\n"
            "\n"
            "# Filter delivery times for each city\n"
            "lagos_times = orders.loc[orders['city'] == city_1, 'delivery_time_minutes']\n"
            "abuja_times = orders.loc[orders['city'] == city_2, 'delivery_time_minutes']\n"
            "kano_times = orders.loc[orders['city'] == city_3, 'delivery_time_minutes']\n"
            "\n"
            "plt.boxplot([lagos_times, abuja_times, kano_times])\n"
        )

        # Update starter file
        for f in pub['workspace']['files']:
            if f['path'] == 'solution.py':
                f['content'] = new_starter

        # Update solution file in grading
        for sf in grading.get('solution_files', []):
            if sf['path'] == 'solution.py':
                sf['content'] = new_solution

        # 4. Update prompt
        pub['prompt'] = (
            "The `orders` DataFrame is already loaded from `orders.csv`, and the three per-city arrays "
            "(`lagos_times`, `abuja_times`, `kano_times`) are already filtered for you.\n\n"
            "Call `plt.boxplot([lagos_times, abuja_times, kano_times])` to draw three side-by-side boxes, "
            "one per city.\n\n"
            "The figure should show three boxes, each reflecting the delivery time distribution for its city."
        )

        # 5. Remove t02 (xticklabels) and t03a/b/c; keep t01 and t04
        grading['tests'] = [
            t for t in grading['tests']
            if t['test_id'] in (
                'ix.tile_viz_line_scatter_box.s15.t01',
                'ix.tile_viz_line_scatter_box.s15.t04',
            )
        ]

        # 6. Update t01 message_on_fail
        for t in grading['tests']:
            if t['test_id'] == 'ix.tile_viz_line_scatter_box.s15.t01':
                t['message_on_fail'] = (
                    "Your figure should contain exactly one Axes with a box plot. "
                    "Call `plt.boxplot([lagos_times, abuja_times, kano_times])`."
                )

        # Remove stale execution_provenance and hidden_checks
        grading.pop('execution_provenance', None)
        grading.pop('hidden_checks', None)

        print("Patched s15 successfully.")
        break

with open('batches/final_batch_012_da_viz/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Written interactions.part.c1.json")
