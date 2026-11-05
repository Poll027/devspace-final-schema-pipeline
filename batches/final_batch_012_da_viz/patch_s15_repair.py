"""
Patch s15 in interactions.part.c1.json:
- Move filter lines (abuja_times, kano_times) from solution-only into the starter as scaffolding
- Change the learner's task to writing the plt.boxplot() call (uses only allowed syntax)
- Update prompt to match new task
- Remove stale execution_provenance and hidden_checks (assemble recomputes them)
"""
import json

path = 'batches/final_batch_012_da_viz/interactions.part.c1.json'
with open(path) as f:
    data = json.load(f)

NEW_STARTER = (
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
    "# Call plt.boxplot() with all three arrays and labels=[city_1, city_2, city_3]\n"
    "# plt.boxplot(...)\n"
)

NEW_SOLUTION = (
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
    "# Call plt.boxplot() with all three arrays and labels=[city_1, city_2, city_3]\n"
    "plt.boxplot([lagos_times, abuja_times, kano_times], labels=[city_1, city_2, city_3])\n"
)

NEW_PROMPT = (
    "The `orders` DataFrame is already loaded from `orders.csv`. "
    "The delivery times for each city are already filtered into `lagos_times`, `abuja_times`, and `kano_times`.\n\n"
    "Call `plt.boxplot()` with all three arrays in order and `labels=[city_1, city_2, city_3]` "
    "to draw a grouped box plot with one labeled box per city.\n\n"
    "The figure should show three boxes, each reflecting the delivery time distribution for its city."
)

for tile in data['tiles']:
    for ix in tile['interactions']:
        if ix['step_id'] == 'tile_viz_line_scatter_box.s15':
            interaction = ix['interaction']
            # Update prompt
            interaction['public']['prompt'] = NEW_PROMPT
            # Update starter
            interaction['public']['workspace']['files'][0]['content'] = NEW_STARTER
            # Update solution
            interaction['grading']['solution_files'][0]['content'] = NEW_SOLUTION
            # Remove stale execution_provenance and hidden_checks (assemble recomputes)
            interaction['grading'].pop('execution_provenance', None)
            interaction['grading'].pop('hidden_checks', None)
            print("Patched tile_viz_line_scatter_box.s15")
            break

with open(path, 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')

print("Done.")
