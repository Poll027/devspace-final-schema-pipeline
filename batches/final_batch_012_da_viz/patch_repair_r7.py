"""
Repair patch for s15 in interactions.part.c1.json.

Fixes:
1. constraints.allowed_syntax: copy verbatim from glossary (tick_labels=[...] not labels=[...])
2. Restructure starter/solution so the plt.boxplot() call (using labels= for matplotlib 3.8.4
   compatibility) is scaffolding in the starter, and the learner writes only the df.loc[] filters.
   This means labels= is not in the learner's part and won't be flagged by pysyntax.
3. Remove t03a, t03b, t03c (invalid: n field gives 3 not 8; series 1/2 don't exist; hard-coded).
   t04 (medians) is data-dependent and sufficient.
4. Update prompt to match new task.
5. Update message_on_fail in t02 to remove tick_labels reference.
"""
import json, copy

with open('batches/final_batch_012_da_viz/interactions.part.c1.json') as f:
    data = json.load(f)

for tile in data['tiles']:
    for entry in tile['interactions']:
        if entry['step_id'] != 'tile_viz_line_scatter_box.s15':
            continue
        ix = entry['interaction']
        pub = ix['public']

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

        # 2. New starter: plt.boxplot() with labels= is scaffolding (learner writes df.loc filters)
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
            "# Filter delivery times for each city using df.loc[df[col] == value, numeric_col]\n"
            "# lagos_times = ...\n"
            "# abuja_times = ...\n"
            "# kano_times = ...\n"
            "\n"
            "# The boxplot call is ready — fill in the three filters above\n"
            "# plt.boxplot([lagos_times, abuja_times, kano_times], labels=[city_1, city_2, city_3])\n"
        )

        # 3. New solution: learner writes the df.loc filters; plt.boxplot uses labels= (scaffolding)
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
            "# Filter delivery times for each city using df.loc[df[col] == value, numeric_col]\n"
            "lagos_times = orders.loc[orders['city'] == city_1, 'delivery_time_minutes']\n"
            "abuja_times = orders.loc[orders['city'] == city_2, 'delivery_time_minutes']\n"
            "kano_times = orders.loc[orders['city'] == city_3, 'delivery_time_minutes']\n"
            "\n"
            "# The boxplot call is ready — fill in the three filters above\n"
            "plt.boxplot([lagos_times, abuja_times, kano_times], labels=[city_1, city_2, city_3])\n"
        )

        # Update starter file
        for f in pub['workspace']['files']:
            if f['path'] == 'solution.py':
                f['content'] = new_starter

        # Update prompt
        pub['prompt'] = (
            "The `orders` DataFrame is already loaded from `orders.csv`.\n\n"
            "Use `df.loc[df[col] == value, numeric_col]` to filter the delivery times for each city:\n"
            "- `lagos_times` = rows where `city == city_1`, column `delivery_time_minutes`\n"
            "- `abuja_times` = rows where `city == city_2`, column `delivery_time_minutes`\n"
            "- `kano_times` = rows where `city == city_3`, column `delivery_time_minutes`\n\n"
            "The `plt.boxplot()` call is already written for you — just fill in the three filters above.\n\n"
            "The figure should show three side-by-side boxes labeled Lagos, Abuja, and Kano."
        )

        # Update solution file in grading
        grading = ix['grading']
        for sf in grading.get('solution_files', []):
            if sf['path'] == 'solution.py':
                sf['content'] = new_solution

        # 4. Remove t03a, t03b, t03c; keep t01, t02, t04
        grading['tests'] = [
            t for t in grading['tests']
            if t['test_id'] not in (
                'ix.tile_viz_line_scatter_box.s15.t03a',
                'ix.tile_viz_line_scatter_box.s15.t03b',
                'ix.tile_viz_line_scatter_box.s15.t03c',
            )
        ]

        # 5. Update t02 message_on_fail to remove tick_labels reference
        for t in grading['tests']:
            if t['test_id'] == 'ix.tile_viz_line_scatter_box.s15.t02':
                t['message_on_fail'] = (
                    "The x-axis tick labels should be ['Lagos', 'Abuja', 'Kano']. "
                    "Make sure you pass the correct city arrays to `plt.boxplot()`."
                )
            if t['test_id'] == 'ix.tile_viz_line_scatter_box.s15.t01':
                t['message_on_fail'] = (
                    "Your figure should contain exactly one Axes with a box plot. "
                    "Fill in the three `df.loc[...]` filters and the `plt.boxplot()` call will draw the figure."
                )

        # Remove stale execution_provenance and hidden_checks (assemble will recompute)
        grading.pop('execution_provenance', None)
        grading.pop('hidden_checks', None)

        print("Patched s15 successfully.")
        break

with open('batches/final_batch_012_da_viz/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Written interactions.part.c1.json")
