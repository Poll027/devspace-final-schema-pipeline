import json, re

# The fix: make plt.boxplot(..., labels=...) identical in starter and solution
# so it's treated as scaffolding and labels= is not judged against allowed_syntax.
# The learner's task: write the correct df.loc filters for abuja_times and kano_times.
# The starter uses placeholder assignments (abuja_times = lagos_times) that produce
# wrong medians, so the starter fails the tests.

STARTER_CONTENT = (
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
    "# Replace the placeholders below with the correct filters for city_2 and city_3\n"
    "abuja_times = lagos_times  # placeholder\n"
    "kano_times = lagos_times   # placeholder\n"
    "\n"
    "plt.boxplot([lagos_times, abuja_times, kano_times], labels=[city_1, city_2, city_3])\n"
)

SOLUTION_CONTENT = (
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
    "plt.boxplot([lagos_times, abuja_times, kano_times], labels=[city_1, city_2, city_3])\n"
)

NEW_PROMPT = (
    "The `orders` DataFrame is already loaded from `orders.csv`. "
    "`lagos_times` is already filtered for you, and the `plt.boxplot()` call is set up.\n\n"
    "Replace the two placeholder assignments with the correct filters:\n"
    "- `abuja_times = orders.loc[orders['city'] == city_2, 'delivery_time_minutes']`\n"
    "- `kano_times = orders.loc[orders['city'] == city_3, 'delivery_time_minutes']`\n\n"
    "The figure should show three boxes, each reflecting the delivery time distribution for its city."
)

def patch_s15(ix):
    # Fix workspace starter file
    for wf in ix['public']['workspace']['files']:
        if wf['path'] == 'solution.py':
            wf['content'] = STARTER_CONTENT

    # Fix prompt
    ix['public']['prompt'] = NEW_PROMPT

    # Fix solution files
    for sf in ix['grading']['solution_files']:
        if sf['path'] == 'solution.py':
            sf['content'] = SOLUTION_CONTENT

    # Fix tests: keep t01 (figure_equals), t02 (xticklabels), t04 (plotted_data_equals)
    # t02 checks xticklabels which will be set by labels= in the scaffolding call
    for t in ix['grading']['tests']:
        if t['test_id'] == 'ix.tile_viz_line_scatter_box.s15.t02':
            t['message_on_fail'] = (
                "The tick labels should be ['Lagos', 'Abuja', 'Kano']. "
                "Check that city_1, city_2, city_3 are correctly assigned."
            )

    # Fix feedback
    ix['feedback']['correct']['message'] = (
        "Excellent! You filtered the delivery times for each city using `orders.loc[orders['city'] == city_2, 'delivery_time_minutes']` "
        "and `orders.loc[orders['city'] == city_3, 'delivery_time_minutes']`, "
        "giving `plt.boxplot()` the correct data to show the full distribution for all three cities side by side."
    )
    ix['feedback']['incorrect']['message'] = (
        "Replace the placeholder assignments: "
        "`abuja_times = orders.loc[orders['city'] == city_2, 'delivery_time_minutes']` and "
        "`kano_times = orders.loc[orders['city'] == city_3, 'delivery_time_minutes']`."
    )
    ix['feedback']['hints'] = [
        "Use `orders.loc[orders['city'] == city_2, 'delivery_time_minutes']` to filter Abuja's delivery times.",
        "The pattern is the same for Kano: replace `city_2` with `city_3`."
    ]

    return ix

# Patch interactions.part.c1.json
print("Patching interactions.part.c1.json...")
with open('batches/final_batch_012_da_viz/interactions.part.c1.json') as f:
    data = json.load(f)

for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_line_scatter_box':
        for item in tile['interactions']:
            if item['step_id'] == 'tile_viz_line_scatter_box.s15':
                item['interaction'] = patch_s15(item['interaction'])
                print("  Patched s15 in interactions.part.c1.json")

with open('batches/final_batch_012_da_viz/interactions.part.c1.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("  Written.")

# Patch interactions.json
print("Patching interactions.json...")
with open('batches/final_batch_012_da_viz/interactions.json') as f:
    data = json.load(f)

for tile in data['tiles']:
    if tile['tile_id'] == 'tile_viz_line_scatter_box':
        for item in tile['interactions']:
            if item['step_id'] == 'tile_viz_line_scatter_box.s15':
                item['interaction'] = patch_s15(item['interaction'])
                print("  Patched s15 in interactions.json")

with open('batches/final_batch_012_da_viz/interactions.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("  Written.")

# Verify: check that plt.boxplot call is identical in starter and solution
import ast
for fname in ['interactions.part.c1.json', 'interactions.json']:
    with open(f'batches/final_batch_012_da_viz/{fname}') as f:
        d = json.load(f)
    for tile in d['tiles']:
        if tile['tile_id'] == 'tile_viz_line_scatter_box':
            for item in tile['interactions']:
                if item['step_id'] == 'tile_viz_line_scatter_box.s15':
                    ix = item['interaction']
                    starter = ix['public']['workspace']['files'][0]['content']
                    solution = ix['grading']['solution_files'][0]['content']
                    
                    # Check that plt.boxplot call is identical
                    s_tree = ast.parse(starter)
                    sol_tree = ast.parse(solution)
                    s_calls = [ast.dump(n) for n in s_tree.body if isinstance(n, ast.Expr)]
                    sol_calls = [ast.dump(n) for n in sol_tree.body if isinstance(n, ast.Expr)]
                    
                    # Find boxplot call
                    s_bp = [c for c in s_calls if 'boxplot' in c]
                    sol_bp = [c for c in sol_calls if 'boxplot' in c]
                    
                    if s_bp and sol_bp and s_bp[0] == sol_bp[0]:
                        print(f"  {fname}: plt.boxplot call is IDENTICAL in starter and solution ✓")
                    else:
                        print(f"  {fname}: plt.boxplot call DIFFERS between starter and solution ✗")
                    
                    # Check no bare labels= in solution (other than in the scaffolding call)
                    bare = re.findall(r'(?<!tick_)labels=', solution)
                    print(f"  {fname}: bare labels= in solution: {bare}")

print("\nDone.")
