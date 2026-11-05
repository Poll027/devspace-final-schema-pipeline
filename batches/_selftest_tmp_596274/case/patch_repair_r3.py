"""Repair patch r3 — fix all errors reported by validate_tile.py --strict."""
import json, copy

with open('batches/final_batch_012_da_viz/interactions.part.c0_canary.json') as f:
    data = json.load(f)

tile = data['tiles'][0]
assert tile['tile_id'] == 'tile_viz_figures_layout_plotting'

# ── helpers ──────────────────────────────────────────────────────────────────

def strip_concept_prefix(fact_ids):
    """'viz.foo#f1' -> 'f1'  (validator does concept_id + '#' + f)"""
    out = []
    for fid in fact_ids:
        if '#' in fid:
            out.append(fid.split('#', 1)[1])
        else:
            out.append(fid)
    return out

# ── daily_averages mount (used by s05 and s12) ───────────────────────────────
DA_MOUNT = [{"asset_id": "ds.daily_averages", "mount_path": "daily_averages.csv"}]

# ── iterate and patch ────────────────────────────────────────────────────────
for entry in tile['interactions']:
    sid = entry['step_id']
    ix  = entry['interaction']

    # 1. Fix fact_ids format in measures (strip concept prefix)
    for m in ix.get('measures', []):
        m['fact_ids'] = strip_concept_prefix(m['fact_ids'])

    # 2. Remove remediation_step_id (no remediation steps exist in this tile)
    fb = ix.get('feedback', {})
    fb.pop('remediation_step_id', None)

    # ── s05: viz.matplotlib_figure_axes practice ─────────────────────────────
    if sid == 'tile_viz_figures_layout_plotting.s05':
        pub = ix['public']
        gr  = ix['grading']

        # Update prompt
        pub['prompt'] = (
            "The file `daily_averages.csv` is already loaded into a DataFrame `df`. "
            "Complete the two steps below:\n\n"
            "1. Call `plt.subplots()` and assign the result to `fig` and `ax`.\n"
            "2. Call `ax.plot(days, delivery_times)` to draw the data onto the Axes.\n\n"
            "The figure should contain exactly one Axes with one line whose x-values are "
            "the `day` column and y-values are the `lagos_avg` column."
        )

        # Add mount
        pub['workspace']['asset_mounts'] = DA_MOUNT

        # Update starter
        pub['workspace']['files'][0]['content'] = (
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n\n"
            "df = pd.read_csv('daily_averages.csv')\n"
            "days = df['day'].tolist()\n"
            "delivery_times = df['lagos_avg'].tolist()\n\n"
            "# Step 1: create a Figure and one Axes using plt.subplots()\n"
            "# fig, ax = ...\n\n"
            "# Step 2: draw delivery_times against days on the Axes\n"
            "# ax.plot(...)\n"
        )

        # Extend allowed_syntax (keep practice anchor entries, add what solution needs)
        pub['constraints']['allowed_syntax'] = [
            "import matplotlib.pyplot as plt",
            "fig, ax = plt.subplots()",
            "ax.plot(x, y)",
            "import pandas as pd",
            "pd.read_csv(file)",
            "df[col].tolist()",
            "single- or double-quoted strings",
            "tuple literal with commas or parentheses",
        ]

        # Update solution
        gr['solution_files'][0]['content'] = (
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n\n"
            "df = pd.read_csv('daily_averages.csv')\n"
            "days = df['day'].tolist()\n"
            "delivery_times = df['lagos_avg'].tolist()\n\n"
            "fig, ax = plt.subplots()\n"
            "ax.plot(days, delivery_times)\n"
        )

        # Update tests — expected values from ds.daily_averages rows
        # day: [1,2,3]  lagos_avg: [21,23,19]  (serialised as ints by sandbox)
        gr['tests'] = [
            {
                "test_id": "ix.tile_viz_figures_layout_plotting.s05.t01",
                "kind": "figure_equals",
                "spec": {"expected": {"n_axes": 1, "chart_types": [["line"]]}},
                "visible": True,
                "message_on_fail": "Your figure should contain exactly one Axes with one line. Make sure you called `fig, ax = plt.subplots()` and then `ax.plot(days, delivery_times)`."
            },
            {
                "test_id": "ix.tile_viz_figures_layout_plotting.s05.t02",
                "kind": "plotted_data_equals",
                "spec": {"chart": "line", "field": "x", "expected": [1, 2, 3], "series": 0, "axes": 0},
                "visible": True,
                "message_on_fail": "The x-values of the line should be the `day` column (1, 2, 3). Pass `days` as the first argument to `ax.plot()`."
            },
            {
                "test_id": "ix.tile_viz_figures_layout_plotting.s05.t03",
                "kind": "plotted_data_equals",
                "spec": {"chart": "line", "field": "y", "expected": [21, 23, 19], "series": 0, "axes": 0},
                "visible": True,
                "message_on_fail": "The y-values of the line should be the `lagos_avg` column (21, 23, 19). Pass `delivery_times` as the second argument to `ax.plot()`."
            },
        ]

    # ── s08: viz.figure_size_layout practice ─────────────────────────────────
    if sid == 'tile_viz_figures_layout_plotting.s08':
        pub = ix['public']
        gr  = ix['grading']

        # Extend allowed_syntax
        pub['constraints']['allowed_syntax'] = [
            "import matplotlib.pyplot as plt",
            "plt.subplots(figsize=(width, height))",
            "fig.tight_layout()",
            "plt.tight_layout()",
            "tuple literals for figsize",
            "variable assignment (fig, ax = ...)",
            "whole-number literals as in the examples",
        ]

        # Update solution — use scalar variables so py_var_mutations can mutate them
        gr['solution_files'][0]['content'] = (
            "import matplotlib.pyplot as plt\n\n"
            "width = 10\n"
            "height = 5\n"
            "fig, ax = plt.subplots(figsize=(width, height))\n"
            "fig.tight_layout()\n"
        )

        # Update tests — expected from sandbox run: list(fig.get_size_inches()) -> [10, 5]
        gr['tests'] = [
            {
                "test_id": "ix.tile_viz_figures_layout_plotting.s08.t01",
                "kind": "figure_equals",
                "spec": {"expected": {"n_axes": 1}},
                "visible": True,
                "message_on_fail": "Your code should create exactly one figure with one Axes. Use `fig, ax = plt.subplots(figsize=(10, 5))`."
            },
            {
                "test_id": "ix.tile_viz_figures_layout_plotting.s08.t02",
                "kind": "value_equals",
                "spec": {"expr": "list(fig.get_size_inches())", "expected": [10, 5]},
                "visible": True,
                "message_on_fail": "The figure size should be (10, 5) inches. Pass `figsize=(10, 5)` to `plt.subplots()`."
            },
        ]

    # ── s12: viz.pyplot_basic_plotting practice ───────────────────────────────
    if sid == 'tile_viz_figures_layout_plotting.s12':
        pub = ix['public']
        gr  = ix['grading']

        # Update prompt
        pub['prompt'] = (
            "The file `daily_averages.csv` is already loaded into a DataFrame `df`. "
            "Make **two** `plt.plot()` calls in the order shown:\n\n"
            "1. **One-argument form**: call `plt.plot(delivery_times)` — matplotlib will "
            "auto-generate x-positions 0, 1, 2.\n"
            "2. **Two-argument form**: call `plt.plot(days, delivery_times)` — matplotlib "
            "will use `days` (1–3) as the x-values.\n\n"
            "Both calls draw onto the same axes. The final figure should have one Axes "
            "containing two lines: the first line has x-values 0–2, the second has x-values 1–3."
        )

        # Add mount
        pub['workspace']['asset_mounts'] = DA_MOUNT

        # Update starter
        pub['workspace']['files'][0]['content'] = (
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n\n"
            "df = pd.read_csv('daily_averages.csv')\n"
            "delivery_times = df['lagos_avg'].tolist()\n"
            "days = df['day'].tolist()\n\n"
            "# Call 1: one-argument form (auto x-positions from 0)\n"
            "# plt.plot(...)\n\n"
            "# Call 2: two-argument form (explicit x-values from days)\n"
            "# plt.plot(..., ...)\n"
        )

        # Extend allowed_syntax
        pub['constraints']['allowed_syntax'] = [
            "import matplotlib.pyplot as plt",
            "plt.plot(y_list)",
            "plt.plot(x_list, y_list)",
            "import pandas as pd",
            "pd.read_csv(file)",
            "df[col].tolist()",
            "single- or double-quoted strings",
        ]

        # Update solution
        gr['solution_files'][0]['content'] = (
            "import matplotlib.pyplot as plt\n"
            "import pandas as pd\n\n"
            "df = pd.read_csv('daily_averages.csv')\n"
            "delivery_times = df['lagos_avg'].tolist()\n"
            "days = df['day'].tolist()\n\n"
            "plt.plot(delivery_times)\n"
            "plt.plot(days, delivery_times)\n"
        )

        # Update tests
        # sandbox: artist 0 x=[0,1,2] y=[21,23,19]; artist 1 x=[1,2,3] y=[21,23,19]
        # chart_types deduplicated -> ['line']
        gr['tests'] = [
            {
                "test_id": "ix.tile_viz_figures_layout_plotting.s12.t01",
                "kind": "figure_equals",
                "spec": {"expected": {"n_axes": 1, "chart_types": [["line"]]}},
                "visible": True,
                "message_on_fail": "The figure should have one Axes. Make sure you made both `plt.plot()` calls."
            },
            {
                "test_id": "ix.tile_viz_figures_layout_plotting.s12.t02",
                "kind": "plotted_data_equals",
                "spec": {"chart": "line", "field": "x", "expected": [0, 1, 2], "series": 0, "axes": 0},
                "visible": True,
                "message_on_fail": "The first line should have auto-generated x-positions 0, 1, 2. Use `plt.plot(delivery_times)` with only one argument."
            },
            {
                "test_id": "ix.tile_viz_figures_layout_plotting.s12.t03",
                "kind": "plotted_data_equals",
                "spec": {"chart": "line", "field": "x", "expected": [1, 2, 3], "series": 1, "axes": 0},
                "visible": True,
                "message_on_fail": "The second line should have x-values from `days` (1, 2, 3). Use `plt.plot(days, delivery_times)` with two arguments."
            },
            {
                "test_id": "ix.tile_viz_figures_layout_plotting.s12.t04",
                "kind": "plotted_data_equals",
                "spec": {"chart": "line", "field": "y", "expected": [21, 23, 19], "series": 0, "axes": 0},
                "visible": False,
                "message_on_fail": "The y-values of the first line should be the `lagos_avg` column (21, 23, 19)."
            },
            {
                "test_id": "ix.tile_viz_figures_layout_plotting.s12.t05",
                "kind": "plotted_data_equals",
                "spec": {"chart": "line", "field": "y", "expected": [21, 23, 19], "series": 1, "axes": 0},
                "visible": False,
                "message_on_fail": "The y-values of the second line should be the `lagos_avg` column (21, 23, 19)."
            },
        ]

with open('batches/final_batch_012_da_viz/interactions.part.c0_canary.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Patch applied.")
