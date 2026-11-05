"""
Build interactions.part.c1.json for tile_viz_line_scatter_box and tile_viz_bar_histograms.
"""
import json

# ── helpers ──────────────────────────────────────────────────────────────────

def choice(step_id, difficulty, measures, anchors, prompt, options, correct_ids,
           option_feedback, correct_msg, incorrect_msg, hints, remediation_step_id=None):
    fb = {
        "correct": {"message": correct_msg},
        "incorrect": {"message": incorrect_msg},
        "hints": hints,
    }
    if remediation_step_id:
        fb["remediation_step_id"] = remediation_step_id
    return {
        "step_id": step_id,
        "interaction": {
            "type": "choice",
            "interaction_id": f"ix.{step_id}",
            "difficulty": difficulty,
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": prompt,
                "options": options,
                "selection": "single",
                "shuffle": True,
            },
            "grading": {
                "correct_option_ids": correct_ids,
                "option_feedback": option_feedback,
            },
            "feedback": fb,
        }
    }


def code_ex(step_id, difficulty, measures, anchors, prompt, runtime_version,
            packages, starter_content, solution_content, tests,
            allowed_syntax, blocked_syntax,
            correct_msg, incorrect_msg, hints, asset_mounts=None):
    workspace = {
        "files": [
            {
                "path": "solution.py",
                "role": "editable",
                "language": "python",
                "content": starter_content,
            }
        ],
        "entry": "solution.py",
        "asset_mounts": asset_mounts or [],
    }
    return {
        "step_id": step_id,
        "interaction": {
            "type": "code_exercise",
            "interaction_id": f"ix.{step_id}",
            "difficulty": difficulty,
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": prompt,
                "runtime": {
                    "kind": "chart_renderer",
                    "version": runtime_version,
                    "packages": packages,
                },
                "workspace": workspace,
                "constraints": {
                    "allowed_syntax": allowed_syntax,
                    "blocked_syntax": blocked_syntax,
                },
            },
            "grading": {
                "solution_files": [
                    {
                        "path": "solution.py",
                        "content": solution_content,
                    }
                ],
                "tests": tests,
            },
            "feedback": {
                "correct": {"message": correct_msg},
                "incorrect": {"message": incorrect_msg},
                "hints": hints,
            },
        }
    }


RUNTIME_VERSION = "0.29.5"

# ═══════════════════════════════════════════════════════════════════════════
# tile_viz_line_scatter_box
# ═══════════════════════════════════════════════════════════════════════════

# ── s03: check — explain_how_connecting_line_reveals_trend (f3) ──────────
s03 = choice(
    step_id="tile_viz_line_scatter_box.s03",
    difficulty="intro",
    measures=[{
        "concept_id": "viz.line_plots",
        "capability": "explain_how_connecting_line_reveals_trend",
        "fact_ids": ["f3"],
    }],
    anchors=["viz.line_plots#assessment:explain_how_connecting_line_reveals_trend"],
    prompt=(
        "A line graph plots the measured points and then draws a line connecting them. "
        "What does the connecting line make easier to see?"
    ),
    options=[
        {"option_id": "opt_trend",
         "text": "How the values rose, fell, or stayed the same over time"},
        {"option_id": "opt_total",
         "text": "The total sum of all the measured values"},
        {"option_id": "opt_outlier",
         "text": "Which individual point is the highest outlier"},
        {"option_id": "opt_category",
         "text": "How many distinct categories the data contains"},
    ],
    correct_ids=["opt_trend"],
    option_feedback={
        "opt_trend": {
            "message": (
                "Correct. The connecting line makes it easier to see how values rose, "
                "fell, or stayed the same over time — the slope between adjacent points "
                "shows the direction of change at a glance."
            )
        },
        "opt_total": {
            "message": (
                "Not quite. The line connects measured points in order; it does not "
                "accumulate or sum them. A bar chart or a running total would show sums."
            )
        },
        "opt_outlier": {
            "message": (
                "Not quite. The connecting line reveals the trend across all points, "
                "not just the highest one. Outliers are visible as individual points "
                "regardless of whether a line is drawn."
            )
        },
        "opt_category": {
            "message": (
                "Not quite. A line graph is for ordered numeric data over time, not "
                "for counting categories. A bar chart is the right tool for comparing "
                "discrete categories."
            )
        },
    },
    correct_msg=(
        "Right. The line between adjacent points makes rises and falls immediately "
        "readable — that is the whole point of connecting them."
    ),
    incorrect_msg=(
        "A line graph plots measured points and draws a line connecting them in order. "
        "That line makes it easier to see how values rose, fell, or stayed the same "
        "over time."
    ),
    hints=[
        "Think about what you can read from the slope of the line between two adjacent points.",
        "The fact says the line makes it easier to see something 'over time' — what changes over time?",
    ],
    remediation_step_id="tile_viz_line_scatter_box.r01",
)

# ── s04: hands_on — line plot code exercise (f1, f2, f3) ─────────────────
STARTER_S04 = """\
import matplotlib.pyplot as plt

# Data (these values will be changed by the grader to test your code)
day_1 = 1
days = [day_1, 2, 3, 4, 5]
dt_1 = 21
delivery_times = [dt_1, 23, 19, 25, 20]

# Call plt.plot(days, delivery_times) to draw a line chart of delivery times
# plt.plot(...)
"""

SOLUTION_S04 = """\
import matplotlib.pyplot as plt

# Data (these values will be changed by the grader to test your code)
day_1 = 1
days = [day_1, 2, 3, 4, 5]
dt_1 = 21
delivery_times = [dt_1, 23, 19, 25, 20]

plt.plot(days, delivery_times)
"""

TESTS_S04 = [
    {
        "test_id": "ix.tile_viz_line_scatter_box.s04.t01",
        "kind": "figure_equals",
        "spec": {
            "expected": {
                "n_axes": 1,
                "chart_types": [["line"]],
            }
        },
        "visible": True,
        "message_on_fail": (
            "Your figure should contain exactly one Axes with one line. "
            "Call `plt.plot(days, delivery_times)`."
        ),
    },
    {
        "test_id": "ix.tile_viz_line_scatter_box.s04.t02",
        "kind": "plotted_data_equals",
        "spec": {
            "chart": "line",
            "field": "x",
            "expected": [1, 2, 3, 4, 5],
            "series": 0,
            "axes": 0,
        },
        "visible": True,
        "message_on_fail": (
            "The x-values of the line should be the `days` list [1, 2, 3, 4, 5]. "
            "Pass `days` as the first argument to `plt.plot()`."
        ),
    },
    {
        "test_id": "ix.tile_viz_line_scatter_box.s04.t03",
        "kind": "plotted_data_equals",
        "spec": {
            "chart": "line",
            "field": "y",
            "expected": [21, 23, 19, 25, 20],
            "series": 0,
            "axes": 0,
        },
        "visible": True,
        "message_on_fail": (
            "The y-values of the line should be the `delivery_times` list. "
            "Pass `delivery_times` as the second argument to `plt.plot()`."
        ),
    },
]

s04 = code_ex(
    step_id="tile_viz_line_scatter_box.s04",
    difficulty="intro",
    measures=[
        {"concept_id": "viz.line_plots", "capability": "identify_line_plot_appropriate_use_case", "fact_ids": ["f1"]},
        {"concept_id": "viz.line_plots", "capability": "call_plt_plot_with_x_and_y_arguments", "fact_ids": ["f2"]},
        {"concept_id": "viz.line_plots", "capability": "build_line_plot_for_time_ordered_numeric_data", "fact_ids": ["f1", "f2", "f3"]},
    ],
    anchors=[
        "viz.line_plots#practice",
        "viz.line_plots#assessment:identify_line_plot_appropriate_use_case",
        "viz.line_plots#assessment:call_plt_plot_with_x_and_y_arguments",
        "viz.line_plots#assessment:build_line_plot_for_time_ordered_numeric_data",
    ],
    prompt=(
        "Two lists are already defined: `days = [1, 2, 3, 4, 5]` and "
        "`delivery_times = [21, 23, 19, 25, 20]` (Lagos average delivery times for days 1–5).\n\n"
        "Call `plt.plot(days, delivery_times)` to draw a line chart that shows how "
        "the average delivery time changed across the five days.\n\n"
        "The figure should contain one line with x-values from `days` and y-values "
        "from `delivery_times`."
    ),
    runtime_version=RUNTIME_VERSION,
    packages=["matplotlib", "pandas"],
    starter_content=STARTER_S04,
    solution_content=SOLUTION_S04,
    tests=TESTS_S04,
    allowed_syntax=[
        "import matplotlib.pyplot as plt",
        "plt.plot(x, y)",
        "plt.show()",
        "Python list literals",
        "variable assignment",
    ],
    blocked_syntax=[
        "plt.scatter()",
        "plt.boxplot()",
        "ax.set_xlabel()",
        "ax.set_ylabel()",
        "ax.set_title()",
        "plt.legend()",
        "plt.annotate()",
        "seaborn functions",
        "DataFrame.plot()",
        "plt.subplots()",
    ],
    correct_msg=(
        "Well done! `plt.plot(days, delivery_times)` draws a line chart with the day "
        "numbers on the x-axis and the delivery times on the y-axis, making the "
        "day-to-day rise and fall immediately visible."
    ),
    incorrect_msg=(
        "Call `plt.plot(days, delivery_times)` — pass `days` as the first argument "
        "(x-values) and `delivery_times` as the second argument (y-values)."
    ),
    hints=[
        "`plt.plot(x, y)` takes x-values first, then y-values. Pass `days` then `delivery_times`.",
        "The starter already defines `days` and `delivery_times` — you just need to call `plt.plot()` with them.",
    ],
)

# ── s07: check — build_scatter_plot_from_two_numeric_columns (f1, f2) ────
s07 = choice(
    step_id="tile_viz_line_scatter_box.s07",
    difficulty="core",
    measures=[{
        "concept_id": "viz.scatter_plots",
        "capability": "build_scatter_plot_from_two_numeric_columns",
        "fact_ids": ["f1", "f2"],
    }],
    anchors=["viz.scatter_plots#assessment:build_scatter_plot_from_two_numeric_columns"],
    prompt=(
        "You have a DataFrame `orders` with columns `distance_km` and "
        "`delivery_time_minutes`. Which call produces a scatter plot with one point "
        "per order, distance on the x-axis, and delivery time on the y-axis?"
    ),
    options=[
        {"option_id": "opt_scatter",
         "text": "`plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])`"},
        {"option_id": "opt_plot",
         "text": "`plt.plot(orders['distance_km'], orders['delivery_time_minutes'])`"},
        {"option_id": "opt_bar",
         "text": "`plt.bar(orders['distance_km'], orders['delivery_time_minutes'])`"},
        {"option_id": "opt_hist",
         "text": "`plt.hist(orders['distance_km'])`"},
    ],
    correct_ids=["opt_scatter"],
    option_feedback={
        "opt_scatter": {
            "message": (
                "Correct. `plt.scatter(x, y)` places one point per (x, y) pair, "
                "making the relationship between distance and delivery time visible "
                "across all orders."
            )
        },
        "opt_plot": {
            "message": (
                "Not quite. `plt.plot(x, y)` draws a line connecting the points in "
                "the order they appear — it is designed for ordered sequences such as "
                "time series, not for exploring the relationship between two unordered "
                "numeric variables."
            )
        },
        "opt_bar": {
            "message": (
                "Not quite. `plt.bar(x, height)` draws bars for categorical data. "
                "Here both columns are numeric and you want to see the relationship "
                "between them, so `plt.scatter()` is the right choice."
            )
        },
        "opt_hist": {
            "message": (
                "Not quite. `plt.hist()` bins a single numeric variable to show its "
                "distribution. To show the relationship between two numeric variables "
                "you need `plt.scatter(x, y)`."
            )
        },
    },
    correct_msg=(
        "Exactly. `plt.scatter(x, y)` places one point per (x, y) pair — "
        "the right tool for exploring the relationship between two numeric variables."
    ),
    incorrect_msg=(
        "To show the relationship between two numeric variables, use `plt.scatter(x, y)`. "
        "It places one point per (x, y) pair, so the pattern of points reveals whether "
        "the two variables move together."
    ),
    hints=[
        "A scatter plot places one point per (x, y) pair — which function name matches that description?",
        "`plt.plot()` connects points with a line (for time series); `plt.scatter()` places independent points.",
    ],
    remediation_step_id="tile_viz_line_scatter_box.r02",
)

# ── s08: hands_on — scatter plot code exercise (f1, f2) ──────────────────
STARTER_S08 = """\
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv('orders.csv')

# Call plt.scatter() with distance_km on the x-axis and delivery_time_minutes on the y-axis
# plt.scatter(...)
"""

SOLUTION_S08 = """\
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv('orders.csv')

plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])
"""

# Computed from the data above
SCATTER_X = [2.1, 3.4, 2.8, 4.5, 5.2, 3.9, 4.8, 9.1,
             3.2, 4.1, 3.0, 5.5, 4.3, 4.7, 4.0, 5.8,
             4.6, 5.9, 4.2, 6.8, 5.3, 6.1, 5.0, 7.2]
SCATTER_Y = [18.0, 22.0, 19.0, 26.0, 30.0, 24.0, 28.0, 50.0,
             25.0, 28.0, 23.0, 31.0, 27.0, 29.0, 26.0, 32.0,
             28.0, 32.0, 27.0, 35.0, 30.0, 33.0, 29.0, 36.0]

TESTS_S08 = [
    {
        "test_id": "ix.tile_viz_line_scatter_box.s08.t01",
        "kind": "figure_equals",
        "spec": {
            "expected": {
                "n_axes": 1,
                "chart_types": [["scatter"]],
            }
        },
        "visible": True,
        "message_on_fail": (
            "Your figure should contain exactly one Axes with a scatter plot. "
            "Call `plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])`."
        ),
    },
    {
        "test_id": "ix.tile_viz_line_scatter_box.s08.t02",
        "kind": "plotted_data_equals",
        "spec": {
            "chart": "scatter",
            "field": "x",
            "expected": SCATTER_X,
            "series": 0,
            "axes": 0,
        },
        "visible": True,
        "message_on_fail": (
            "The x-values should be `orders['distance_km']`. "
            "Pass that column as the first argument to `plt.scatter()`."
        ),
    },
    {
        "test_id": "ix.tile_viz_line_scatter_box.s08.t03",
        "kind": "plotted_data_equals",
        "spec": {
            "chart": "scatter",
            "field": "y",
            "expected": SCATTER_Y,
            "series": 0,
            "axes": 0,
        },
        "visible": True,
        "message_on_fail": (
            "The y-values should be `orders['delivery_time_minutes']`. "
            "Pass that column as the second argument to `plt.scatter()`."
        ),
    },
]

s08 = code_ex(
    step_id="tile_viz_line_scatter_box.s08",
    difficulty="core",
    measures=[
        {"concept_id": "viz.scatter_plots", "capability": "build_scatter_plot_from_two_numeric_columns", "fact_ids": ["f1", "f2"]},
    ],
    anchors=[
        "viz.scatter_plots#practice",
        "viz.scatter_plots#assessment:build_scatter_plot_from_two_numeric_columns",
    ],
    prompt=(
        "The `orders` DataFrame is already loaded from `orders.csv`. It has columns "
        "`distance_km` and `delivery_time_minutes`.\n\n"
        "Call `plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])` "
        "to produce a scatter plot with one point per order — distance on the x-axis "
        "and delivery time on the y-axis.\n\n"
        "The figure should contain one scatter plot with 24 points."
    ),
    runtime_version=RUNTIME_VERSION,
    packages=["matplotlib", "pandas"],
    starter_content=STARTER_S08,
    solution_content=SOLUTION_S08,
    tests=TESTS_S08,
    allowed_syntax=[
        "plt.scatter(x, y)",
        "ax.scatter(x, y)",
        "plt.show()",
        "fig, ax = plt.subplots()",
        "import matplotlib.pyplot as plt",
        "orders['distance_km']",
        "orders['delivery_time_minutes']",
    ],
    blocked_syntax=[
        "ax.set_xlabel()",
        "ax.set_ylabel()",
        "ax.set_title()",
        "plt.xlabel()",
        "plt.ylabel()",
        "plt.title()",
        "ax.legend()",
        "plt.legend()",
        "sns.scatterplot()",
        "sns.regplot()",
        "plt.scatter(..., s=...)",
        "plt.scatter(..., c=...)",
        "plt.scatter(..., marker=...)",
    ],
    correct_msg=(
        "Well done! `plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])` "
        "places one point per order, making the relationship between distance and "
        "delivery time visible across all 24 orders."
    ),
    incorrect_msg=(
        "Call `plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])` — "
        "the first argument is the x-column (distance_km) and the second is the "
        "y-column (delivery_time_minutes)."
    ),
    hints=[
        "`plt.scatter(x, y)` takes two arguments: the x-column first, then the y-column.",
        "Access the columns with `orders['distance_km']` and `orders['delivery_time_minutes']`.",
    ],
    asset_mounts=[
        {"asset_id": "ds.orders", "mount_path": "orders.csv"},
    ],
)

# ── s13: check — apply_iqr_rule_to_determine_whisker_extent_and_outliers (f2) ──
s13 = choice(
    step_id="tile_viz_line_scatter_box.s13",
    difficulty="core",
    measures=[{
        "concept_id": "viz.box_plots",
        "capability": "apply_iqr_rule_to_determine_whisker_extent_and_outliers",
        "fact_ids": ["f2"],
    }],
    anchors=["viz.box_plots#assessment:apply_iqr_rule_to_determine_whisker_extent_and_outliers"],
    prompt=(
        "A box plot of Lagos delivery times has Q1 = 20 minutes and Q3 = 30 minutes. "
        "The IQR is 10 minutes. A delivery of 50 minutes is recorded. "
        "How will matplotlib draw that 50-minute delivery?"
    ),
    options=[
        {"option_id": "opt_flier",
         "text": "As a flier point (outlier) beyond the upper whisker"},
        {"option_id": "opt_whisker",
         "text": "At the tip of the upper whisker"},
        {"option_id": "opt_box",
         "text": "Inside the box, between Q1 and Q3"},
        {"option_id": "opt_ignored",
         "text": "It is ignored and not drawn"},
    ],
    correct_ids=["opt_flier"],
    option_feedback={
        "opt_flier": {
            "message": (
                "Correct. The upper whisker can reach at most Q3 + 1.5 × IQR = "
                "30 + 15 = 45 minutes. A 50-minute delivery is beyond that limit, "
                "so it is drawn as a separate flier point."
            )
        },
        "opt_whisker": {
            "message": (
                "Not quite. The whisker tip is the farthest data point that still "
                "falls within 1.5 × IQR of the box (at most 45 minutes here). "
                "A 50-minute delivery exceeds that limit and is drawn as a flier point."
            )
        },
        "opt_box": {
            "message": (
                "Not quite. The box spans Q1 to Q3 (20 to 30 minutes). "
                "A 50-minute delivery is far above Q3 and would be drawn as a "
                "flier point beyond the upper whisker."
            )
        },
        "opt_ignored": {
            "message": (
                "Not quite. Matplotlib draws all data points. Values beyond 1.5 × IQR "
                "from the box are shown as individual flier points — they are not ignored."
            )
        },
    },
    correct_msg=(
        "Right. The upper whisker reaches at most Q3 + 1.5 × IQR = 45 minutes. "
        "The 50-minute delivery exceeds that, so it appears as a flier point."
    ),
    incorrect_msg=(
        "The whiskers extend to the farthest point within 1.5 × IQR of the box. "
        "Here that is Q3 + 1.5 × 10 = 45 minutes. A 50-minute delivery is beyond "
        "that limit and is drawn as a separate flier point."
    ),
    hints=[
        "Calculate the upper whisker limit: Q3 + 1.5 × IQR = 30 + 1.5 × 10 = ?",
        "Any point beyond the whisker limit is drawn separately — what is that called?",
    ],
    remediation_step_id="tile_viz_line_scatter_box.r03",
)

# ── s14: check — explain_box_plot_value_for_comparing_multiple_distributions (f3) ──
s14 = choice(
    step_id="tile_viz_line_scatter_box.s14",
    difficulty="core",
    measures=[{
        "concept_id": "viz.box_plots",
        "capability": "explain_box_plot_value_for_comparing_multiple_distributions",
        "fact_ids": ["f3"],
    }],
    anchors=["viz.box_plots#assessment:explain_box_plot_value_for_comparing_multiple_distributions"],
    prompt=(
        "You want to compare the delivery-time distributions of Lagos, Abuja, and Kano "
        "side by side — not just their averages, but how spread out each city's times are. "
        "Which chart type is best suited for this?"
    ),
    options=[
        {"option_id": "opt_box",
         "text": "A box plot, because it gives a condensed display of each distribution side by side"},
        {"option_id": "opt_bar",
         "text": "A bar chart, because it shows the average for each city"},
        {"option_id": "opt_line",
         "text": "A line plot, because it connects the values in order"},
        {"option_id": "opt_hist",
         "text": "A histogram, because it bins all delivery times into ranges"},
    ],
    correct_ids=["opt_box"],
    option_feedback={
        "opt_box": {
            "message": (
                "Correct. Boxplots offer a condensed display for comparing the "
                "distributions of multiple datasets side by side — showing the median, "
                "spread, and outliers for each city in a single figure."
            )
        },
        "opt_bar": {
            "message": (
                "Not quite. A bar chart shows one value per category (such as the mean). "
                "It does not show the spread, quartiles, or outliers of each city's "
                "distribution — a box plot does."
            )
        },
        "opt_line": {
            "message": (
                "Not quite. A line plot is for showing how a value changes over an "
                "ordered sequence (such as time). It is not designed for comparing "
                "distributions across groups."
            )
        },
        "opt_hist": {
            "message": (
                "Not quite. A histogram bins a single numeric variable to show its "
                "distribution shape. To compare distributions across multiple groups "
                "side by side, a box plot is the right choice."
            )
        },
    },
    correct_msg=(
        "Exactly. A box plot gives a condensed display of each group's distribution — "
        "median, quartiles, whiskers, and outliers — all side by side."
    ),
    incorrect_msg=(
        "When you want to compare the full distribution (not just the average) across "
        "multiple groups, use a box plot. It shows the median, spread, and outliers "
        "for each group in a condensed side-by-side display."
    ),
    hints=[
        "The question asks about comparing *distributions* (spread, median, outliers) — not just averages.",
        "Which chart type is described as offering 'a condensed display for comparing the distributions of multiple datasets side by side'?",
    ],
    remediation_step_id="tile_viz_line_scatter_box.r04",
)

# ── s15: hands_on — grouped box plot code exercise (f1, f2, f4) ──────────
STARTER_S15 = """\
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv('orders.csv')

# Filter delivery times by city
lagos_times = orders.loc[orders['city'] == 'Lagos', 'delivery_time_minutes']
abuja_times = orders.loc[orders['city'] == 'Abuja', 'delivery_time_minutes']
kano_times = orders.loc[orders['city'] == 'Kano', 'delivery_time_minutes']

# Call plt.boxplot() with a list of the three arrays and tick_labels for each city
# plt.boxplot([...], tick_labels=[...])
"""

SOLUTION_S15 = """\
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv('orders.csv')

# Filter delivery times by city
lagos_times = orders.loc[orders['city'] == 'Lagos', 'delivery_time_minutes']
abuja_times = orders.loc[orders['city'] == 'Abuja', 'delivery_time_minutes']
kano_times = orders.loc[orders['city'] == 'Kano', 'delivery_time_minutes']

plt.boxplot([lagos_times, abuja_times, kano_times], tick_labels=['Lagos', 'Abuja', 'Kano'])
"""

# Medians computed from data: Lagos=25.0, Abuja=27.5, Kano=31.0
TESTS_S15 = [
    {
        "test_id": "ix.tile_viz_line_scatter_box.s15.t01",
        "kind": "figure_equals",
        "spec": {
            "expected": {
                "n_axes": 1,
                "chart_types": [["box"]],
            }
        },
        "visible": True,
        "message_on_fail": (
            "Your figure should contain exactly one Axes with a box plot. "
            "Call `plt.boxplot([lagos_times, abuja_times, kano_times], "
            "tick_labels=['Lagos', 'Abuja', 'Kano'])`."
        ),
    },
    {
        "test_id": "ix.tile_viz_line_scatter_box.s15.t02",
        "kind": "axes_property",
        "spec": {
            "property": "xticklabels",
            "expected": ["Lagos", "Abuja", "Kano"],
            "axes": 0,
        },
        "visible": True,
        "message_on_fail": (
            "The x-axis tick labels should be ['Lagos', 'Abuja', 'Kano']. "
            "Pass `tick_labels=['Lagos', 'Abuja', 'Kano']` to `plt.boxplot()`."
        ),
    },
    {
        "test_id": "ix.tile_viz_line_scatter_box.s15.t03",
        "kind": "plotted_data_equals",
        "spec": {
            "chart": "box",
            "field": "n",
            "expected": [8, 8, 8],
            "axes": 0,
        },
        "visible": True,
        "message_on_fail": (
            "Each box should contain 8 data points (one per city). "
            "Make sure you filter the orders DataFrame by city before passing to `plt.boxplot()`."
        ),
    },
    {
        "test_id": "ix.tile_viz_line_scatter_box.s15.t04",
        "kind": "plotted_data_equals",
        "spec": {
            "chart": "box",
            "field": "medians",
            "expected": [25.0, 27.5, 31.0],
            "axes": 0,
        },
        "visible": True,
        "message_on_fail": (
            "The medians should be [25.0, 27.5, 31.0] for Lagos, Abuja, and Kano. "
            "Check that you are passing the correct city arrays in the right order."
        ),
    },
]

s15 = code_ex(
    step_id="tile_viz_line_scatter_box.s15",
    difficulty="stretch",
    measures=[
        {"concept_id": "viz.box_plots", "capability": "call_boxplot_function_with_array_like_data", "fact_ids": ["f1"]},
        {"concept_id": "viz.box_plots", "capability": "identify_box_whisker_and_flier_anatomy", "fact_ids": ["f2"]},
        {"concept_id": "viz.box_plots", "capability": "draw_grouped_box_plot_with_labeled_ticks_from_sequence_of_arrays", "fact_ids": ["f4"]},
    ],
    anchors=[
        "viz.box_plots#practice",
        "viz.box_plots#assessment:call_boxplot_function_with_array_like_data",
        "viz.box_plots#assessment:identify_box_whisker_and_flier_anatomy",
        "viz.box_plots#assessment:draw_grouped_box_plot_with_labeled_ticks_from_sequence_of_arrays",
    ],
    prompt=(
        "The `orders` DataFrame is already loaded from `orders.csv` and the three "
        "per-city arrays (`lagos_times`, `abuja_times`, `kano_times`) are already "
        "filtered for you.\n\n"
        "Call `plt.boxplot([lagos_times, abuja_times, kano_times], "
        "tick_labels=['Lagos', 'Abuja', 'Kano'])` to draw three side-by-side boxes, "
        "one per city, each labeled with its city name.\n\n"
        "The figure should show three boxes with x-axis labels Lagos, Abuja, and Kano."
    ),
    runtime_version=RUNTIME_VERSION,
    packages=["matplotlib", "pandas"],
    starter_content=STARTER_S15,
    solution_content=SOLUTION_S15,
    tests=TESTS_S15,
    allowed_syntax=[
        "plt.boxplot(x)",
        "ax.boxplot(x)",
        "tick_labels=[...]",
        "df.loc[df[col] == value, numeric_col]",
        "import matplotlib.pyplot as plt",
        "fig, ax = plt.subplots()",
        "plt.show()",
        "list literals and variable assignment",
    ],
    blocked_syntax=[
        "ax.set_title()",
        "ax.set_xlabel()",
        "ax.set_ylabel()",
        "plt.title()",
        "plt.xlabel()",
        "plt.ylabel()",
        "seaborn",
        "sns.boxplot()",
        "plt.subplots() with nrows/ncols > 1",
    ],
    correct_msg=(
        "Excellent! You passed a list of three arrays to `plt.boxplot()` and used "
        "`tick_labels` to label each box with its city name — showing the full "
        "distribution (median, spread, and outliers) for all three cities side by side."
    ),
    incorrect_msg=(
        "Call `plt.boxplot([lagos_times, abuja_times, kano_times], "
        "tick_labels=['Lagos', 'Abuja', 'Kano'])`. "
        "Pass the three arrays as a list and use `tick_labels` to name each box."
    ),
    hints=[
        "Wrap the three arrays in a list: `plt.boxplot([lagos_times, abuja_times, kano_times], ...)`.",
        "Use `tick_labels=['Lagos', 'Abuja', 'Kano']` to label each box with its city name.",
    ],
    asset_mounts=[
        {"asset_id": "ds.orders", "mount_path": "orders.csv"},
    ],
)

# ═══════════════════════════════════════════════════════════════════════════
# tile_viz_bar_histograms
# ═══════════════════════════════════════════════════════════════════════════

# ── s04: check — identify_bar_chart_as_categorical_comparison_tool (f2) ──
s04_bar = choice(
    step_id="tile_viz_bar_histograms.s04",
    difficulty="intro",
    measures=[{
        "concept_id": "viz.bar_charts",
        "capability": "identify_bar_chart_as_categorical_comparison_tool",
        "fact_ids": ["f2"],
    }],
    anchors=["viz.bar_charts#assessment:identify_bar_chart_as_categorical_comparison_tool"],
    prompt=(
        "Which of the following datasets is a bar chart the right tool to visualise?"
    ),
    options=[
        {"option_id": "opt_city",
         "text": "Average delivery time for each of three cities (Lagos, Abuja, Kano)"},
        {"option_id": "opt_time",
         "text": "Daily average delivery time over five consecutive days"},
        {"option_id": "opt_dist",
         "text": "The distribution of individual delivery times across all orders"},
        {"option_id": "opt_rel",
         "text": "The relationship between delivery distance and delivery time"},
    ],
    correct_ids=["opt_city"],
    option_feedback={
        "opt_city": {
            "message": (
                "Correct. A bar chart is a common chart type for graphing categorical "
                "data or data sorted into groups — here, the three cities are the "
                "categories and the bar heights show each city's average."
            )
        },
        "opt_time": {
            "message": (
                "Not quite. Daily averages over consecutive days form an ordered "
                "time series — a line plot is better suited to show how the value "
                "changes over time."
            )
        },
        "opt_dist": {
            "message": (
                "Not quite. Showing the distribution of a numeric variable across "
                "many values is what a histogram does — it bins the values and draws "
                "one bar per bin."
            )
        },
        "opt_rel": {
            "message": (
                "Not quite. Exploring the relationship between two numeric variables "
                "is what a scatter plot does — it places one point per (x, y) pair."
            )
        },
    },
    correct_msg=(
        "Right. A bar chart is designed for categorical data — comparing a numeric "
        "value across discrete groups such as cities."
    ),
    incorrect_msg=(
        "A bar chart is a common chart type for graphing categorical data or data "
        "sorted into groups. The three cities are categories, so a bar chart is the "
        "right choice for comparing their averages."
    ),
    hints=[
        "Think about which dataset has discrete, named groups rather than a continuous numeric axis.",
        "A bar chart compares a numeric value across categories — which option has categories?",
    ],
    remediation_step_id="tile_viz_bar_histograms.r01",
)

# ── s05: check — explain_why_zero_baseline_is_required_for_valid_length_comparison (f3, m1) ──
s05_bar = choice(
    step_id="tile_viz_bar_histograms.s05",
    difficulty="core",
    measures=[{
        "concept_id": "viz.bar_charts",
        "capability": "explain_why_zero_baseline_is_required_for_valid_length_comparison",
        "fact_ids": ["f3"],
    }],
    anchors=["viz.bar_charts#assessment:explain_why_zero_baseline_is_required_for_valid_length_comparison"],
    prompt=(
        "Kano averages 30 minutes and Lagos averages 25 minutes. "
        "A bar chart is drawn with the baseline starting at 20 minutes instead of 0. "
        "What is wrong with this chart?"
    ),
    options=[
        {"option_id": "opt_distort",
         "text": "Kano's bar looks twice as long as Lagos's even though its average is only 5 minutes higher"},
        {"option_id": "opt_fine",
         "text": "Nothing — starting at 20 makes the difference between cities easier to see"},
        {"option_id": "opt_missing",
         "text": "The chart is missing a title, which makes it unreadable"},
        {"option_id": "opt_wrong_type",
         "text": "Bar charts cannot display averages — only counts"},
    ],
    correct_ids=["opt_distort"],
    option_feedback={
        "opt_distort": {
            "message": (
                "Correct. With a baseline at 20, Kano's bar is 10 units tall and "
                "Lagos's is 5 units tall — Kano looks twice as long even though its "
                "average is only 5 minutes higher. The eye compares bar lengths from "
                "the baseline, so the baseline must be 0."
            )
        },
        "opt_fine": {
            "message": (
                "Not quite. Starting at a non-zero baseline distorts the comparison. "
                "Bar charts are easy to read because the eye compares lengths from a "
                "common baseline — if that baseline is not 0, the lengths no longer "
                "truthfully represent the values."
            )
        },
        "opt_missing": {
            "message": (
                "Not quite. A missing title is a labeling issue, not a baseline issue. "
                "The real problem is that starting bars at 20 instead of 0 makes "
                "Kano's bar look twice as long as Lagos's, distorting the comparison."
            )
        },
        "opt_wrong_type": {
            "message": (
                "Not quite. Bar charts can display any numeric value per category, "
                "including averages. The problem here is the non-zero baseline, which "
                "distorts the visual comparison of bar lengths."
            )
        },
    },
    correct_msg=(
        "Exactly. A non-zero baseline makes bar lengths misleading — Kano's bar "
        "looks twice as long as Lagos's even though the difference is only 5 minutes. "
        "Keep the baseline at 0."
    ),
    incorrect_msg=(
        "Bar charts are easy to read because the eye compares lengths from a common "
        "baseline. If the baseline is not 0, the lengths distort the comparison. "
        "With a baseline at 20, Kano's bar (10 units) looks twice as long as Lagos's "
        "(5 units) even though the difference is only 5 minutes."
    ),
    hints=[
        "Calculate the bar heights when the baseline is 20: Kano = 30 − 20 = ?, Lagos = 25 − 20 = ?",
        "The eye compares bar *lengths* from the baseline — what happens to those lengths when the baseline shifts?",
    ],
    remediation_step_id="tile_viz_bar_histograms.r02",
)

# ── s06: hands_on — bar chart code exercise (f1, f4) ─────────────────────
STARTER_S06 = """\
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv('orders.csv')

# Compute the mean delivery time per city
# city_avg = orders.groupby('city')['delivery_time_minutes'].mean()

# Call plt.bar() with city names as x and the averages as heights
# plt.bar(city_avg.index, city_avg)
"""

SOLUTION_S06 = """\
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv('orders.csv')

city_avg = orders.groupby('city')['delivery_time_minutes'].mean()
plt.bar(city_avg.index, city_avg)
"""

# Bar heights from groupby: Abuja=27.625, Kano=31.25, Lagos=27.125 (alphabetical order)
BAR_HEIGHTS = [27.625, 31.25, 27.125]
BAR_LABELS = ["Abuja", "Kano", "Lagos"]

TESTS_S06 = [
    {
        "test_id": "ix.tile_viz_bar_histograms.s06.t01",
        "kind": "figure_equals",
        "spec": {
            "expected": {
                "n_axes": 1,
                "chart_types": [["bar"]],
            }
        },
        "visible": True,
        "message_on_fail": (
            "Your figure should contain exactly one Axes with a bar chart. "
            "Call `plt.bar(city_avg.index, city_avg)`."
        ),
    },
    {
        "test_id": "ix.tile_viz_bar_histograms.s06.t02",
        "kind": "axes_property",
        "spec": {
            "property": "xticklabels",
            "expected": BAR_LABELS,
            "axes": 0,
        },
        "visible": True,
        "message_on_fail": (
            "The x-axis labels should be the city names ['Abuja', 'Kano', 'Lagos']. "
            "Pass `city_avg.index` as the first argument to `plt.bar()`."
        ),
    },
    {
        "test_id": "ix.tile_viz_bar_histograms.s06.t03",
        "kind": "plotted_data_equals",
        "spec": {
            "chart": "bar",
            "field": "heights",
            "expected": BAR_HEIGHTS,
            "series": 0,
            "axes": 0,
        },
        "visible": True,
        "message_on_fail": (
            "The bar heights should be the per-city mean delivery times "
            "[27.625, 31.25, 27.125] for Abuja, Kano, and Lagos. "
            "Use `orders.groupby('city')['delivery_time_minutes'].mean()` to compute them."
        ),
    },
]

s06_bar = code_ex(
    step_id="tile_viz_bar_histograms.s06",
    difficulty="core",
    measures=[
        {"concept_id": "viz.bar_charts", "capability": "construct_bar_chart_with_plt_bar_using_categorical_x", "fact_ids": ["f1", "f4"]},
    ],
    anchors=[
        "viz.bar_charts#practice",
        "viz.bar_charts#assessment:construct_bar_chart_with_plt_bar_using_categorical_x",
    ],
    prompt=(
        "The `orders` DataFrame is already loaded from `orders.csv`. It has columns "
        "`city` (Lagos, Abuja, Kano) and `delivery_time_minutes`.\n\n"
        "Steps:\n"
        "1. Compute the mean delivery time per city: "
        "`city_avg = orders.groupby('city')['delivery_time_minutes'].mean()`\n"
        "2. Draw a bar chart: `plt.bar(city_avg.index, city_avg)`\n\n"
        "The figure should show three bars — one per city — with city names on the "
        "x-axis and mean delivery times as bar heights, with the baseline at 0."
    ),
    runtime_version=RUNTIME_VERSION,
    packages=["matplotlib", "pandas"],
    starter_content=STARTER_S06,
    solution_content=SOLUTION_S06,
    tests=TESTS_S06,
    allowed_syntax=[
        "import matplotlib.pyplot as plt",
        "orders.groupby('city')['delivery_time_minutes'].mean()",
        "plt.bar(city_avg.index, city_avg)",
        "plt.show()",
        "ax.bar(city_avg.index, city_avg)",
    ],
    blocked_syntax=[
        "plt.title()",
        "plt.xlabel()",
        "plt.ylabel()",
        "ax.set_title()",
        "ax.set_xlabel()",
        "ax.set_ylabel()",
        "plt.hist()",
        "plt.plot()",
        "plt.scatter()",
        "plt.boxplot()",
        "import seaborn",
        "import numpy",
    ],
    correct_msg=(
        "Well done! `orders.groupby('city')['delivery_time_minutes'].mean()` computes "
        "the per-city averages, and `plt.bar(city_avg.index, city_avg)` draws a bar "
        "for each city with the correct height and a baseline at 0."
    ),
    incorrect_msg=(
        "First compute the averages: `city_avg = orders.groupby('city')['delivery_time_minutes'].mean()`. "
        "Then draw the chart: `plt.bar(city_avg.index, city_avg)`. "
        "Pass the city names (index) as x and the averages as heights."
    ),
    hints=[
        "`orders.groupby('city')['delivery_time_minutes'].mean()` returns a Series with city names as the index.",
        "Pass `city_avg.index` as the first argument to `plt.bar()` and `city_avg` as the second.",
    ],
    asset_mounts=[
        {"asset_id": "ds.orders", "mount_path": "orders.csv"},
    ],
)

# ── s09: check — call_plt_hist_and_explain_binning_mechanism (f1) ─────────
s09_hist = choice(
    step_id="tile_viz_bar_histograms.s09",
    difficulty="core",
    measures=[{
        "concept_id": "viz.histograms",
        "capability": "call_plt_hist_and_explain_binning_mechanism",
        "fact_ids": ["f1"],
    }],
    anchors=["viz.histograms#assessment:call_plt_hist_and_explain_binning_mechanism"],
    prompt=(
        "What does `plt.hist(orders['delivery_time_minutes'])` do internally before "
        "drawing the bars?"
    ),
    options=[
        {"option_id": "opt_bin",
         "text": "Uses numpy.histogram to bin the values and count how many fall in each bin"},
        {"option_id": "opt_sort",
         "text": "Sorts the delivery times and draws one bar per unique value"},
        {"option_id": "opt_avg",
         "text": "Computes the average delivery time and draws a single bar"},
        {"option_id": "opt_scatter",
         "text": "Places one point per delivery time along the x-axis"},
    ],
    correct_ids=["opt_bin"],
    option_feedback={
        "opt_bin": {
            "message": (
                "Correct. `plt.hist()` uses `numpy.histogram` to bin the data in x, "
                "count the number of values in each bin, and draw the result as bars — "
                "one bar per bin."
            )
        },
        "opt_sort": {
            "message": (
                "Not quite. `plt.hist()` groups values into bins (ranges), not one bar "
                "per unique value. Drawing one bar per unique value would produce too "
                "many bars for continuous data."
            )
        },
        "opt_avg": {
            "message": (
                "Not quite. `plt.hist()` shows the distribution of all values, not a "
                "single summary. It bins the data and draws one bar per bin, showing "
                "how many values fall in each range."
            )
        },
        "opt_scatter": {
            "message": (
                "Not quite. Placing one point per value is what a scatter plot does. "
                "`plt.hist()` groups values into bins and draws one bar per bin, "
                "showing the count in each range."
            )
        },
    },
    correct_msg=(
        "Right. `plt.hist()` uses `numpy.histogram` to bin the data and count values "
        "per bin, then draws one bar per bin — revealing the distribution shape."
    ),
    incorrect_msg=(
        "`plt.hist(x, bins=...)` uses `numpy.histogram` to bin the data in x, count "
        "the number of values in each bin, and draw the result as bars."
    ),
    hints=[
        "The fact says `plt.hist()` uses a specific numpy function — which one?",
        "Think about what 'binning' means: grouping values into ranges and counting how many fall in each.",
    ],
    remediation_step_id="tile_viz_bar_histograms.r03",
)

# ── s10: check — configure_bins_parameter_with_integer_sequence_or_string (f2) ──
s10_hist = choice(
    step_id="tile_viz_bar_histograms.s10",
    difficulty="core",
    measures=[{
        "concept_id": "viz.histograms",
        "capability": "configure_bins_parameter_with_integer_sequence_or_string",
        "fact_ids": ["f2"],
    }],
    anchors=["viz.histograms#assessment:configure_bins_parameter_with_integer_sequence_or_string"],
    prompt=(
        "Which of the following is a valid way to call `plt.hist()` that sets "
        "explicit bin edges at 10, 20, 30, 40, and 50 minutes?"
    ),
    options=[
        {"option_id": "opt_seq",
         "text": "`plt.hist(orders['delivery_time_minutes'], bins=[10, 20, 30, 40, 50])`"},
        {"option_id": "opt_int",
         "text": "`plt.hist(orders['delivery_time_minutes'], bins=4)`"},
        {"option_id": "opt_auto",
         "text": "`plt.hist(orders['delivery_time_minutes'], bins='auto')`"},
        {"option_id": "opt_default",
         "text": "`plt.hist(orders['delivery_time_minutes'])`"},
    ],
    correct_ids=["opt_seq"],
    option_feedback={
        "opt_seq": {
            "message": (
                "Correct. Passing a sequence sets explicit bin edges — here the four "
                "bins are [10, 20), [20, 30), [30, 40), and [40, 50], exactly as "
                "specified."
            )
        },
        "opt_int": {
            "message": (
                "Not quite. Passing an integer sets that many *equal-width* bins — "
                "the edges are computed automatically from the data range, not set "
                "explicitly. To set explicit edges, pass a sequence."
            )
        },
        "opt_auto": {
            "message": (
                "Not quite. Passing the string `'auto'` selects a binning strategy "
                "automatically — the edges are chosen by the algorithm, not set "
                "explicitly. To set explicit edges, pass a sequence."
            )
        },
        "opt_default": {
            "message": (
                "Not quite. Calling `plt.hist()` without a `bins` argument uses the "
                "default of 10 equal-width bins. To set explicit bin edges, pass a "
                "sequence such as `[10, 20, 30, 40, 50]`."
            )
        },
    },
    correct_msg=(
        "Exactly. Passing a sequence to `bins` sets explicit bin edges — "
        "the four bins are [10, 20), [20, 30), [30, 40), and [40, 50]."
    ),
    incorrect_msg=(
        "The `bins` parameter accepts three forms: an integer (equal-width bins), "
        "a sequence (explicit edges), or a string strategy such as `'auto'`. "
        "To set explicit edges at 10, 20, 30, 40, 50, pass a list."
    ),
    hints=[
        "The question asks for *explicit* bin edges — which form of `bins` sets the edges directly?",
        "An integer sets the *number* of bins; a sequence sets the *edges*.",
    ],
    remediation_step_id="tile_viz_bar_histograms.r04",
)

# ── s11: hands_on — histogram code exercise (f1, f2) ─────────────────────
STARTER_S11 = """\
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv('orders.csv')

# Plot a histogram of delivery_time_minutes with a non-default bin count
# plt.hist(orders['delivery_time_minutes'], bins=...)
"""

SOLUTION_S11 = """\
import matplotlib.pyplot as plt
import pandas as pd

orders = pd.read_csv('orders.csv')

plt.hist(orders['delivery_time_minutes'], bins=20)
"""

# With bins=20 on this data: 20 bars, heights computed above
HIST_HEIGHTS = [2, 0, 1, 2, 1, 4, 5, 2, 3, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]

TESTS_S11 = [
    {
        "test_id": "ix.tile_viz_bar_histograms.s11.t01",
        "kind": "figure_equals",
        "spec": {
            "expected": {
                "n_axes": 1,
                "chart_types": [["hist"]],
            }
        },
        "visible": True,
        "message_on_fail": (
            "Your figure should contain exactly one Axes with a histogram. "
            "Call `plt.hist(orders['delivery_time_minutes'], bins=<integer>)`."
        ),
    },
    {
        "test_id": "ix.tile_viz_bar_histograms.s11.t02",
        "kind": "plotted_data_equals",
        "spec": {
            "chart": "hist",
            "field": "heights",
            "expected": HIST_HEIGHTS,
            "series": 0,
            "axes": 0,
        },
        "visible": True,
        "message_on_fail": (
            "The bar heights should reflect the distribution of delivery_time_minutes "
            "with bins=20. Make sure you pass `orders['delivery_time_minutes']` to "
            "`plt.hist()` and set `bins=20`."
        ),
    },
]

s11_hist = code_ex(
    step_id="tile_viz_bar_histograms.s11",
    difficulty="stretch",
    measures=[
        {"concept_id": "viz.histograms", "capability": "call_plt_hist_and_explain_binning_mechanism", "fact_ids": ["f1"]},
        {"concept_id": "viz.histograms", "capability": "configure_bins_parameter_with_integer_sequence_or_string", "fact_ids": ["f2"]},
    ],
    anchors=[
        "viz.histograms#practice",
        "viz.histograms#assessment:call_plt_hist_and_explain_binning_mechanism",
        "viz.histograms#assessment:configure_bins_parameter_with_integer_sequence_or_string",
    ],
    prompt=(
        "The `orders` DataFrame is already loaded from `orders.csv`. It has a "
        "`delivery_time_minutes` column.\n\n"
        "Call `plt.hist(orders['delivery_time_minutes'], bins=20)` to draw a histogram "
        "of delivery times with 20 equal-width bins.\n\n"
        "The figure should show a histogram whose bar heights reflect the distribution "
        "of delivery times across all 24 orders."
    ),
    runtime_version=RUNTIME_VERSION,
    packages=["matplotlib", "pandas"],
    starter_content=STARTER_S11,
    solution_content=SOLUTION_S11,
    tests=TESTS_S11,
    allowed_syntax=[
        "plt.hist(series, bins=<int>)",
        "plt.hist(series, bins=<list_of_edges>)",
        "plt.hist(series, bins='auto')",
        "plt.hist(series)",
        "plt.show()",
        "orders['delivery_time_minutes']",
    ],
    blocked_syntax=[
        "sns.histplot()",
        "sns.displot()",
        "plt.plot()",
        "plt.scatter()",
        "plt.boxplot()",
        "plt.xlabel()",
        "plt.ylabel()",
        "plt.title()",
        "plt.legend()",
    ],
    correct_msg=(
        "Well done! `plt.hist(orders['delivery_time_minutes'], bins=20)` bins the "
        "delivery times into 20 equal-width ranges and draws one bar per bin, "
        "revealing the distribution shape."
    ),
    incorrect_msg=(
        "Call `plt.hist(orders['delivery_time_minutes'], bins=20)`. "
        "Pass the delivery_time_minutes column as the first argument and set "
        "`bins=20` to use 20 equal-width bins."
    ),
    hints=[
        "`plt.hist()` takes the data column as the first argument: `orders['delivery_time_minutes']`.",
        "Set `bins=20` to use 20 equal-width bins instead of the default 10.",
    ],
    asset_mounts=[
        {"asset_id": "ds.orders", "mount_path": "orders.csv"},
    ],
)

# ═══════════════════════════════════════════════════════════════════════════
# Assemble output
# ═══════════════════════════════════════════════════════════════════════════

output = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_012_da_viz",
    "tiles": [
        {
            "tile_id": "tile_viz_line_scatter_box",
            "interactions": [s03, s04, s07, s08, s13, s14, s15],
        },
        {
            "tile_id": "tile_viz_bar_histograms",
            "interactions": [s04_bar, s05_bar, s06_bar, s09_hist, s10_hist, s11_hist],
        },
    ],
}

with open("batches/final_batch_012_da_viz/interactions.part.c1.json", "w") as f:
    json.dump(output, f, indent=2)

print("Written interactions.part.c1.json")
print(f"tile_viz_line_scatter_box: {len(output['tiles'][0]['interactions'])} interactions")
print(f"tile_viz_bar_histograms: {len(output['tiles'][1]['interactions'])} interactions")
