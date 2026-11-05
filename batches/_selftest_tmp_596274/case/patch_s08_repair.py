"""
Patch tile_viz_custom_multi_panel.s08 interaction to fix allowed-syntax violations.

Violations:
  - attr:DataFrame  (pd.DataFrame({...}) in solution)
  - dict_lit        ({...} in pd.DataFrame({...}))
  - lit_str         (df['col_a'] etc.)
  - tuple_lit       (axs[0, 0] subscript is a tuple in AST)
  - unpack          (fig, axs = ... in solution but not starter)

Fix:
  1. Move `fig, axs = plt.subplots(2, 2)` into the starter (scaffolding).
  2. Remove pd.DataFrame usage from solution; use plain lists directly.
  3. Use axs[0][0] double-bracket notation (avoids tuple_lit).
  4. Update prompt to match new notation.
"""
import json, copy

PATH = "batches/final_batch_012_da_viz/interactions.part.c2.json"

with open(PATH) as f:
    data = json.load(f)

# Find the tile and step
target_tile = None
target_ix = None
for tile in data["tiles"]:
    if tile["tile_id"] == "tile_viz_custom_multi_panel":
        target_tile = tile
        for entry in tile["interactions"]:
            if entry["step_id"] == "tile_viz_custom_multi_panel.s08":
                target_ix = entry["interaction"]
                break
        break

assert target_tile is not None, "tile_viz_custom_multi_panel not found"
assert target_ix is not None, "s08 not found"

# New starter: includes fig, axs = plt.subplots(2, 2) as scaffolding
new_starter = (
    "import matplotlib.pyplot as plt\n"
    "\n"
    "# Data (these values will be changed by the grader to test your code)\n"
    "col_a_1 = 23\n"
    "col_a = [col_a_1, 25, 22, 24, 26, 23, 25, 24]\n"
    "col_b = [45, 47, 44, 46, 48, 45, 47, 46]\n"
    "col_c = [56, 58, 55, 57, 59, 56, 58, 57]\n"
    "col_d = [78, 80, 77, 79, 81, 78, 80, 79]\n"
    "\n"
    "fig, axs = plt.subplots(2, 2)\n"
    "# Draw a histogram in each panel below\n"
)

# New solution: uses axs[0][0] notation (no tuple_lit), no pd.DataFrame
new_solution = (
    "import matplotlib.pyplot as plt\n"
    "\n"
    "# Data (these values will be changed by the grader to test your code)\n"
    "col_a_1 = 23\n"
    "col_a = [col_a_1, 25, 22, 24, 26, 23, 25, 24]\n"
    "col_b = [45, 47, 44, 46, 48, 45, 47, 46]\n"
    "col_c = [56, 58, 55, 57, 59, 56, 58, 57]\n"
    "col_d = [78, 80, 77, 79, 81, 78, 80, 79]\n"
    "\n"
    "fig, axs = plt.subplots(2, 2)\n"
    "# Draw a histogram in each panel below\n"
    "axs[0][0].hist(col_a)\n"
    "axs[0][1].hist(col_b)\n"
    "axs[1][0].hist(col_c)\n"
    "axs[1][1].hist(col_d)\n"
)

# New prompt: uses axs[0][0] notation
new_prompt = (
    "A 2\u00d72 subplot grid has already been created for you with "
    "`fig, axs = plt.subplots(2, 2)`. Four lists of data are also provided: "
    "`col_a`, `col_b`, `col_c`, and `col_d`.\n\n"
    "Draw a histogram in each panel:\n"
    "1. Top-left panel: `axs[0][0].hist(col_a)`\n"
    "2. Top-right panel: `axs[0][1].hist(col_b)`\n"
    "3. Bottom-left panel: `axs[1][0].hist(col_c)`\n"
    "4. Bottom-right panel: `axs[1][1].hist(col_d)`\n\n"
    "Each panel will show the distribution of one column."
)

# Update workspace starter file
target_ix["public"]["workspace"]["files"][0]["content"] = new_starter

# Update prompt
target_ix["public"]["prompt"] = new_prompt

# Update solution file
target_ix["grading"]["solution_files"][0]["content"] = new_solution

# Update test messages to use axs[0][0] notation
for test in target_ix["grading"]["tests"]:
    if test["test_id"] == "ix.tile_viz_custom_multi_panel.s08.t01":
        test["message_on_fail"] = (
            "Your figure should contain 4 axes (2\u00d72 grid), each with a histogram. "
            "Use `fig, axs = plt.subplots(2, 2)` and call `.hist()` on each `axs[row][col]`."
        )

# Update feedback hints
target_ix["feedback"]["hints"] = [
    "The grid is already created: `fig, axs = plt.subplots(2, 2)`. Add four `.hist()` calls, one per panel.",
    "Each panel is addressed by `axs[row][col]` \u2014 for example `axs[0][0]` is top-left and `axs[1][1]` is bottom-right."
]

# Update incorrect feedback
target_ix["feedback"]["incorrect"]["message"] = (
    "Make sure you called `.hist()` on each of the four `axs[row][col]` objects "
    "with a different list: `axs[0][0].hist(col_a)`, `axs[0][1].hist(col_b)`, "
    "`axs[1][0].hist(col_c)`, `axs[1][1].hist(col_d)`."
)

with open(PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
