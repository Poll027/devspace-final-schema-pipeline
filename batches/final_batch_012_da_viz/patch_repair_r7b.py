"""
Repair patch v2 for s15: make plt.boxplot() call actual scaffolding in starter (not a comment),
so the learner's part is only the df.loc[] filters.
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

        # Starter: plt.boxplot() is actual code (scaffolding), but lagos_times etc. are undefined
        # so the starter fails with NameError (does not pass tests)
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
            "plt.boxplot([lagos_times, abuja_times, kano_times], labels=[city_1, city_2, city_3])\n"
        )

        # Solution: same as starter but with the three df.loc[] lines filled in
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
            "plt.boxplot([lagos_times, abuja_times, kano_times], labels=[city_1, city_2, city_3])\n"
        )

        # Update starter file
        for f in pub['workspace']['files']:
            if f['path'] == 'solution.py':
                f['content'] = new_starter

        # Update solution file in grading
        for sf in grading.get('solution_files', []):
            if sf['path'] == 'solution.py':
                sf['content'] = new_solution

        # Remove stale execution_provenance and hidden_checks
        grading.pop('execution_provenance', None)
        grading.pop('hidden_checks', None)

        print("Patched starter/solution for s15.")
        break

with open('batches/final_batch_012_da_viz/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Written interactions.part.c1.json")
