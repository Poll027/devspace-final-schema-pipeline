"""Build interactions.part.c2.json for chunk c2:
tile_viz_labeling_chart_selection, tile_viz_custom_multi_panel, tile_viz_seaborn_stats_themes
"""
import json

CHART_RENDERER_VERSION = "0.29.5"

# ─────────────────────────────────────────────────────────────────────────────
# TILE: tile_viz_labeling_chart_selection
# Steps: s03 (choice), s04 (choice), s05 (code_exercise), s08 (choice), s09 (choice), s10 (code_exercise)
# ─────────────────────────────────────────────────────────────────────────────

# s03: check — viz.labeling_annotation#f1 — apply_axes_object_labeling_methods
# Taught by s01 (explainer): f1 = ax.set_xlabel/ylabel/set_title
ix_labeling_s03 = {
    "type": "choice",
    "interaction_id": "ix.tile_viz_labeling_chart_selection.s03",
    "difficulty": "intro",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.labeling_annotation",
            "capability": "apply_axes_object_labeling_methods",
            "fact_ids": ["f1"]
        }
    ],
    "anchors": [
        "viz.labeling_annotation#assessment:apply_axes_object_labeling_methods"
    ],
    "public": {
        "prompt": "You have an Axes object called `ax`. Which three method calls correctly add a title, an x-axis label, and a y-axis label to that Axes?",
        "options": [
            {
                "option_id": "opt_correct",
                "text": "`ax.set_title('...')`, `ax.set_xlabel('...')`, `ax.set_ylabel('...')`"
            },
            {
                "option_id": "opt_plt",
                "text": "`plt.title('...')`, `plt.xlabel('...')`, `plt.ylabel('...')`"
            },
            {
                "option_id": "opt_fig",
                "text": "`fig.set_title('...')`, `fig.set_xlabel('...')`, `fig.set_ylabel('...')`"
            },
            {
                "option_id": "opt_mixed",
                "text": "`ax.title('...')`, `ax.xlabel('...')`, `ax.ylabel('...')`"
            }
        ],
        "selection": "single",
        "shuffle": True
    },
    "grading": {
        "correct_option_ids": ["opt_correct"],
        "option_feedback": {
            "opt_correct": {
                "message": "Correct. `ax.set_xlabel()`, `ax.set_ylabel()`, and `ax.set_title()` are the three Axes object methods for labeling."
            },
            "opt_plt": {
                "message": "Those are the pyplot interface functions (`plt.xlabel()`, etc.), not the Axes object methods. The Axes object uses `ax.set_xlabel()`, `ax.set_ylabel()`, and `ax.set_title()`."
            },
            "opt_fig": {
                "message": "The Figure object (`fig`) does not have `set_xlabel()`, `set_ylabel()`, or `set_title()` methods. Labeling calls go on the Axes object (`ax`), not the Figure."
            },
            "opt_mixed": {
                "message": "The Axes methods are `ax.set_xlabel()`, `ax.set_ylabel()`, and `ax.set_title()` — note the `set_` prefix. `ax.xlabel()` and `ax.ylabel()` are not valid method names."
            }
        }
    },
    "feedback": {
        "correct": {
            "message": "Right. The Axes object's labeling methods all start with `set_`: `ax.set_xlabel()`, `ax.set_ylabel()`, and `ax.set_title()`."
        },
        "incorrect": {
            "message": "The Axes object uses `ax.set_xlabel('...')`, `ax.set_ylabel('...')`, and `ax.set_title('...')` — each takes a string argument."
        },
        "hints": [
            "All three Axes labeling methods start with `set_`.",
            "The methods belong to the `ax` object, not to `fig` or `plt`."
        ],
        "remediation_step_id": "tile_viz_labeling_chart_selection.r01"
    }
}

# s04: check — viz.labeling_annotation#f3 — apply_pyplot_interface_labeling_functions
# Taught by s02 (explainer): f3 = plt.xlabel/ylabel/title
ix_labeling_s04 = {
    "type": "choice",
    "interaction_id": "ix.tile_viz_labeling_chart_selection.s04",
    "difficulty": "intro",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.labeling_annotation",
            "capability": "apply_pyplot_interface_labeling_functions",
            "fact_ids": ["f3"]
        }
    ],
    "anchors": [
        "viz.labeling_annotation#assessment:apply_pyplot_interface_labeling_functions"
    ],
    "public": {
        "prompt": "You are using the pyplot interface (no explicit `ax` variable). Which call sets the title of the current Axes?",
        "options": [
            {
                "option_id": "opt_plt_title",
                "text": "`plt.title('Delivery times by day')`"
            },
            {
                "option_id": "opt_ax_title",
                "text": "`ax.set_title('Delivery times by day')`"
            },
            {
                "option_id": "opt_fig_title",
                "text": "`fig.set_title('Delivery times by day')`"
            },
            {
                "option_id": "opt_plt_set",
                "text": "`plt.set_title('Delivery times by day')`"
            }
        ],
        "selection": "single",
        "shuffle": True
    },
    "grading": {
        "correct_option_ids": ["opt_plt_title"],
        "option_feedback": {
            "opt_plt_title": {
                "message": "Correct. In the pyplot interface, `plt.title()` sets the title of the current Axes — the pyplot equivalent of `ax.set_title()`."
            },
            "opt_ax_title": {
                "message": "`ax.set_title()` is the Axes object method, not the pyplot interface function. When using the pyplot interface without an explicit `ax`, use `plt.title()`."
            },
            "opt_fig_title": {
                "message": "The Figure object does not have a `set_title()` method for the Axes title. In the pyplot interface, use `plt.title()` to set the current Axes title."
            },
            "opt_plt_set": {
                "message": "`plt.set_title()` is not a valid pyplot function. The correct pyplot function is `plt.title()` (no `set_` prefix)."
            }
        }
    },
    "feedback": {
        "correct": {
            "message": "Correct. `plt.title()`, `plt.xlabel()`, and `plt.ylabel()` are the pyplot interface equivalents of the Axes `set_` methods."
        },
        "incorrect": {
            "message": "In the pyplot interface, the labeling functions are `plt.title()`, `plt.xlabel()`, and `plt.ylabel()` — they operate on the current Axes without needing an explicit `ax` variable."
        },
        "hints": [
            "The pyplot interface functions mirror the Axes methods but are called on `plt` directly.",
            "Unlike the Axes methods, the pyplot functions do not have a `set_` prefix — it's `plt.title()`, not `plt.set_title()`."
        ],
        "remediation_step_id": "tile_viz_labeling_chart_selection.r02"
    }
}

# s05: hands_on — code_exercise — viz.labeling_annotation f1, f2, f3
# Practice anchor: add title, axis labels, legend to two pre-plotted series
# Dataset: ds.daily_averages (day, lagos_avg, abuja_avg)
# Allowed: ax.set_xlabel, ax.set_ylabel, ax.set_title, ax.plot(x,y,label=), ax.legend(), plt.xlabel, plt.ylabel, plt.title, import matplotlib.pyplot as plt, fig/ax = plt.subplots(), plt.show()
# Blocked: import seaborn, sns.*, ax.set_theme(), plt.style.use(), plt.subplots_adjust(), plt.tight_layout(), ax.annotate(), ax.text()
# Success: non-empty title, non-empty x/y labels, legend with two distinct entries
ix_labeling_s05 = {
    "type": "code_exercise",
    "interaction_id": "ix.tile_viz_labeling_chart_selection.s05",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.labeling_annotation",
            "capability": "add_title_axis_labels_and_legend_to_unlabeled_plot",
            "fact_ids": ["f1", "f2", "f3"]
        },
        {
            "concept_id": "viz.labeling_annotation",
            "capability": "attach_legend_via_label_kwarg_and_legend_call",
            "fact_ids": ["f2"]
        }
    ],
    "anchors": [
        "viz.labeling_annotation#practice",
        "viz.labeling_annotation#assessment:add_title_axis_labels_and_legend_to_unlabeled_plot",
        "viz.labeling_annotation#assessment:attach_legend_via_label_kwarg_and_legend_call"
    ],
    "public": {
        "prompt": (
            "Two series are already plotted on `ax`: Lagos daily averages and Abuja daily averages for days 1–5.\n\n"
            "Complete the code to:\n"
            "1. Set the Axes title to `'Average Delivery Time by Day'`\n"
            "2. Set the x-axis label to `'Day'`\n"
            "3. Set the y-axis label to `'Average delivery time (minutes)'`\n"
            "4. Add a legend that shows two entries — one labelled `'Lagos'` and one labelled `'Abuja'`\n\n"
            "Use `ax.set_title()`, `ax.set_xlabel()`, `ax.set_ylabel()`, and `ax.legend()`. "
            "Pass `label='Lagos'` and `label='Abuja'` to the two `ax.plot()` calls already in the starter."
        ),
        "runtime": {
            "kind": "chart_renderer",
            "version": CHART_RENDERER_VERSION,
            "packages": ["matplotlib", "pandas"]
        },
        "workspace": {
            "files": [
                {
                    "path": "solution.py",
                    "role": "editable",
                    "language": "python",
                    "content": (
                        "import matplotlib.pyplot as plt\n"
                        "import pandas as pd\n\n"
                        "days = [1, 2, 3, 4, 5]\n"
                        "lagos_avg = [21, 23, 19, 25, 20]\n"
                        "abuja_avg = [24, 26, 22, 28, 25]\n\n"
                        "fig, ax = plt.subplots()\n"
                        "ax.plot(days, lagos_avg)  # add label='Lagos' here\n"
                        "ax.plot(days, abuja_avg)  # add label='Abuja' here\n\n"
                        "# Add title, axis labels, and legend below\n"
                    )
                }
            ],
            "entry": "solution.py",
            "asset_mounts": []
        },
        "constraints": {
            "allowed_syntax": [
                "ax.set_xlabel('...')",
                "ax.set_ylabel('...')",
                "ax.set_title('...')",
                "ax.plot(x, y, label='...')",
                "ax.legend()",
                "plt.xlabel('...')",
                "plt.ylabel('...')",
                "plt.title('...')",
                "import matplotlib.pyplot as plt",
                "fig, ax = plt.subplots()",
                "plt.show()"
            ],
            "blocked_syntax": [
                "import seaborn",
                "sns.*",
                "ax.set_theme()",
                "plt.style.use()",
                "plt.subplots_adjust()",
                "plt.tight_layout()",
                "ax.annotate()",
                "ax.text()"
            ]
        }
    },
    "grading": {
        "solution_files": [
            {
                "path": "solution.py",
                "content": (
                    "import matplotlib.pyplot as plt\n"
                    "import pandas as pd\n\n"
                    "days = [1, 2, 3, 4, 5]\n"
                    "lagos_avg = [21, 23, 19, 25, 20]\n"
                    "abuja_avg = [24, 26, 22, 28, 25]\n\n"
                    "fig, ax = plt.subplots()\n"
                    "ax.plot(days, lagos_avg, label='Lagos')\n"
                    "ax.plot(days, abuja_avg, label='Abuja')\n\n"
                    "ax.set_title('Average Delivery Time by Day')\n"
                    "ax.set_xlabel('Day')\n"
                    "ax.set_ylabel('Average delivery time (minutes)')\n"
                    "ax.legend()\n"
                )
            }
        ],
        "tests": [
            {
                "test_id": "ix.tile_viz_labeling_chart_selection.s05.t01",
                "kind": "axes_property",
                "spec": {
                    "property": "title",
                    "expected": "Average Delivery Time by Day"
                },
                "visible": True,
                "message_on_fail": "Set the Axes title to 'Average Delivery Time by Day' using `ax.set_title('Average Delivery Time by Day')`."
            },
            {
                "test_id": "ix.tile_viz_labeling_chart_selection.s05.t02",
                "kind": "axes_property",
                "spec": {
                    "property": "xlabel",
                    "expected": "Day"
                },
                "visible": True,
                "message_on_fail": "Set the x-axis label to 'Day' using `ax.set_xlabel('Day')`."
            },
            {
                "test_id": "ix.tile_viz_labeling_chart_selection.s05.t03",
                "kind": "axes_property",
                "spec": {
                    "property": "ylabel",
                    "expected": "Average delivery time (minutes)"
                },
                "visible": True,
                "message_on_fail": "Set the y-axis label to 'Average delivery time (minutes)' using `ax.set_ylabel('Average delivery time (minutes)')`."
            },
            {
                "test_id": "ix.tile_viz_labeling_chart_selection.s05.t04",
                "kind": "axes_property",
                "spec": {
                    "property": "legend",
                    "expected": ["Lagos", "Abuja"]
                },
                "visible": True,
                "message_on_fail": "Add `label='Lagos'` and `label='Abuja'` to the two `ax.plot()` calls, then call `ax.legend()` to display the legend."
            },
            {
                "test_id": "ix.tile_viz_labeling_chart_selection.s05.t05",
                "kind": "plotted_data_equals",
                "spec": {
                    "chart": "line",
                    "field": "y",
                    "expected": [21, 23, 19, 25, 20],
                    "series": 0,
                    "axes": 0
                },
                "visible": True,
                "message_on_fail": "The first line should plot `lagos_avg` values [21, 23, 19, 25, 20]. Do not change the `ax.plot()` calls — only add the `label=` argument."
            }
        ]
    },
    "feedback": {
        "correct": {
            "message": "Well done! Your plot now has a title, axis labels, and a two-entry legend — everything a reader needs to understand the chart without extra context."
        },
        "incorrect": {
            "message": "Check that you called `ax.set_title()`, `ax.set_xlabel()`, `ax.set_ylabel()`, and `ax.legend()`, and that you added `label='Lagos'` and `label='Abuja'` to the two `ax.plot()` calls."
        },
        "hints": [
            "Add `label='Lagos'` inside the first `ax.plot()` call and `label='Abuja'` inside the second, then call `ax.legend()` at the end.",
            "The three labeling methods are `ax.set_title('...')`, `ax.set_xlabel('...')`, and `ax.set_ylabel('...')` — each takes a string."
        ]
    }
}

# s08: check — viz.chart_type_selection f1-f5 — select_chart_type + identify_histogram
# Taught by s06 (explainer): all five facts
ix_labeling_s08 = {
    "type": "choice",
    "interaction_id": "ix.tile_viz_labeling_chart_selection.s08",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.chart_type_selection",
            "capability": "select_chart_type_for_analytical_question",
            "fact_ids": ["f1", "f2", "f3", "f4", "f5"]
        },
        {
            "concept_id": "viz.chart_type_selection",
            "capability": "identify_histogram_use_case",
            "fact_ids": ["f2"]
        }
    ],
    "anchors": [
        "viz.chart_type_selection#assessment:select_chart_type_for_analytical_question",
        "viz.chart_type_selection#assessment:identify_histogram_use_case"
    ],
    "public": {
        "prompt": "A QuickDeliver analyst wants to answer: 'What is the shape of the distribution of delivery times — are most deliveries fast, or is the spread wide?' Which chart type is best?",
        "options": [
            {
                "option_id": "opt_hist",
                "text": "Histogram"
            },
            {
                "option_id": "opt_bar",
                "text": "Bar chart"
            },
            {
                "option_id": "opt_line",
                "text": "Line graph"
            },
            {
                "option_id": "opt_scatter",
                "text": "Scatter plot"
            }
        ],
        "selection": "single",
        "shuffle": True
    },
    "grading": {
        "correct_option_ids": ["opt_hist"],
        "option_feedback": {
            "opt_hist": {
                "message": "Correct. `plt.hist()` bins a numeric variable, counts values per bin, and draws the distribution as bars — exactly what you need to see the shape of delivery times."
            },
            "opt_bar": {
                "message": "A bar chart compares a numeric value across discrete categories (e.g., average delivery time per city). It does not show the distribution shape of a single numeric variable."
            },
            "opt_line": {
                "message": "A line graph shows how a value changes over time. It does not reveal the distribution shape of a numeric variable like delivery times."
            },
            "opt_scatter": {
                "message": "A scatter plot shows the relationship between two numeric variables. To see the distribution of a single variable, use a histogram."
            }
        }
    },
    "feedback": {
        "correct": {
            "message": "Right. A histogram bins the data and shows how many values fall in each range — perfect for seeing the distribution shape."
        },
        "incorrect": {
            "message": "To see how a numeric variable is distributed (its shape, spread, and concentration), use a histogram (`plt.hist()`). Each bar represents a count of values in a bin."
        },
        "hints": [
            "The question asks about the 'shape of the distribution' of a single numeric variable.",
            "Think about which chart type bins a numeric variable and counts values per bin."
        ],
        "remediation_step_id": "tile_viz_labeling_chart_selection.r03"
    }
}

# s09: check — viz.chart_type_selection f3, f5 — identify_line_graph + identify_boxplot
# Taught by s06 (explainer): f3, f5
ix_labeling_s09 = {
    "type": "choice",
    "interaction_id": "ix.tile_viz_labeling_chart_selection.s09",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.chart_type_selection",
            "capability": "identify_line_graph_use_case",
            "fact_ids": ["f3"]
        },
        {
            "concept_id": "viz.chart_type_selection",
            "capability": "identify_boxplot_use_case",
            "fact_ids": ["f5"]
        }
    ],
    "anchors": [
        "viz.chart_type_selection#assessment:identify_line_graph_use_case",
        "viz.chart_type_selection#assessment:identify_boxplot_use_case"
    ],
    "public": {
        "prompt": "An analyst wants to compare the full spread of delivery times (median, quartiles, and outliers) across Lagos, Abuja, and Kano side by side. Which chart type is best?",
        "options": [
            {
                "option_id": "opt_box",
                "text": "Box plot"
            },
            {
                "option_id": "opt_line",
                "text": "Line graph"
            },
            {
                "option_id": "opt_hist",
                "text": "Histogram"
            },
            {
                "option_id": "opt_bar",
                "text": "Bar chart"
            }
        ],
        "selection": "single",
        "shuffle": True
    },
    "grading": {
        "correct_option_ids": ["opt_box"],
        "option_feedback": {
            "opt_box": {
                "message": "Correct. Box plots offer a condensed display for comparing the distributions of multiple datasets side by side — showing median, quartiles, and outliers per group."
            },
            "opt_line": {
                "message": "A line graph shows how a value changes over time. It does not show the spread (quartiles, outliers) of a distribution across groups."
            },
            "opt_hist": {
                "message": "A histogram shows the distribution of a single numeric variable. To compare distributions across multiple groups side by side, a box plot is more compact and direct."
            },
            "opt_bar": {
                "message": "A bar chart compares a single aggregate value (like the mean) per category. It does not show the full spread — quartiles, median, and outliers — that a box plot provides."
            }
        }
    },
    "feedback": {
        "correct": {
            "message": "Exactly. A box plot condenses each group's distribution into a single visual — median, IQR, whiskers, and outliers — making side-by-side comparison easy."
        },
        "incorrect": {
            "message": "When you need to compare the full spread (median, quartiles, outliers) across multiple groups, a box plot is the right choice. It shows all of that in a compact form per group."
        },
        "hints": [
            "The question asks for 'full spread' across multiple groups — which chart type shows quartiles and outliers per group?",
            "A line graph tracks change over time; a box plot compares distributions across groups."
        ],
        "remediation_step_id": "tile_viz_labeling_chart_selection.r04"
    }
}

# s10: hands_on — code_exercise — viz.chart_type_selection f1, f4
# Practice anchor: scatter plot of distance_km vs delivery_minutes + comment
# Dataset: ds.chart_selection_mini (distance_km, delivery_minutes)
# Allowed: import matplotlib.pyplot as plt, plt.scatter(x,y), plt.xlabel(), plt.ylabel(), plt.title(), plt.show(), Python list literals, variable assignment, single-line comments (#)
# Blocked: import seaborn, sns.*, plt.subplots() with nrows/ncols > 1, plt.style.use(), plt.hist(), plt.bar(), plt.plot(), plt.boxplot()
ix_labeling_s10 = {
    "type": "code_exercise",
    "interaction_id": "ix.tile_viz_labeling_chart_selection.s10",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.chart_type_selection",
            "capability": "identify_bar_chart_use_case",
            "fact_ids": ["f1"]
        },
        {
            "concept_id": "viz.chart_type_selection",
            "capability": "identify_scatter_plot_use_case",
            "fact_ids": ["f4"]
        }
    ],
    "anchors": [
        "viz.chart_type_selection#practice",
        "viz.chart_type_selection#assessment:identify_bar_chart_use_case",
        "viz.chart_type_selection#assessment:identify_scatter_plot_use_case"
    ],
    "public": {
        "prompt": (
            "Two lists are already defined: `distance_km` and `delivery_minutes`, each with six values from QuickDeliver orders.\n\n"
            "1. Call `plt.scatter(distance_km, delivery_minutes)` to produce a scatter plot.\n"
            "2. Add `plt.xlabel('Distance (km)')` and `plt.ylabel('Delivery time (minutes)')`.\n"
            "3. Add a one-line comment (starting with `#`) that explains why a scatter plot — not a bar chart — answers the question 'Do longer distances lead to longer delivery times?'\n\n"
            "The figure should show `distance_km` on the x-axis and `delivery_minutes` on the y-axis."
        ),
        "runtime": {
            "kind": "chart_renderer",
            "version": CHART_RENDERER_VERSION,
            "packages": ["matplotlib", "pandas"]
        },
        "workspace": {
            "files": [
                {
                    "path": "solution.py",
                    "role": "editable",
                    "language": "python",
                    "content": (
                        "import matplotlib.pyplot as plt\n\n"
                        "distance_km = [1.2, 2.5, 3.8, 4.1, 5.6, 6.3]\n"
                        "delivery_minutes = [14, 21, 28, 31, 38, 44]\n\n"
                        "# Create a scatter plot of distance_km vs delivery_minutes\n"
                        "# plt.scatter(...)\n\n"
                        "# Add axis labels\n\n"
                        "# Add a comment explaining why scatter, not bar chart\n"
                    )
                }
            ],
            "entry": "solution.py",
            "asset_mounts": []
        },
        "constraints": {
            "allowed_syntax": [
                "import matplotlib.pyplot as plt",
                "plt.scatter(x, y)",
                "plt.xlabel()",
                "plt.ylabel()",
                "plt.title()",
                "plt.show()",
                "Python list literals",
                "variable assignment",
                "single-line comments (#)"
            ],
            "blocked_syntax": [
                "import seaborn",
                "sns.*",
                "plt.subplots() with nrows/ncols > 1",
                "plt.style.use()",
                "plt.hist()",
                "plt.bar()",
                "plt.plot()",
                "plt.boxplot()"
            ]
        }
    },
    "grading": {
        "solution_files": [
            {
                "path": "solution.py",
                "content": (
                    "import matplotlib.pyplot as plt\n\n"
                    "distance_km = [1.2, 2.5, 3.8, 4.1, 5.6, 6.3]\n"
                    "delivery_minutes = [14, 21, 28, 31, 38, 44]\n\n"
                    "# Scatter plot shows the relationship between two numerical variables;\n"
                    "# a bar chart compares a value across categories, not a relationship.\n"
                    "plt.scatter(distance_km, delivery_minutes)\n"
                    "plt.xlabel('Distance (km)')\n"
                    "plt.ylabel('Delivery time (minutes)')\n"
                )
            }
        ],
        "tests": [
            {
                "test_id": "ix.tile_viz_labeling_chart_selection.s10.t01",
                "kind": "figure_equals",
                "spec": {
                    "expected": {
                        "n_axes": 1,
                        "chart_types": [["scatter"]]
                    }
                },
                "visible": True,
                "message_on_fail": "Your figure should contain exactly one Axes with a scatter plot. Call `plt.scatter(distance_km, delivery_minutes)`."
            },
            {
                "test_id": "ix.tile_viz_labeling_chart_selection.s10.t02",
                "kind": "plotted_data_equals",
                "spec": {
                    "chart": "scatter",
                    "field": "x",
                    "expected": [1.2, 2.5, 3.8, 4.1, 5.6, 6.3],
                    "series": 0,
                    "axes": 0
                },
                "visible": True,
                "message_on_fail": "The scatter plot's x-values should be `distance_km` = [1.2, 2.5, 3.8, 4.1, 5.6, 6.3]. Call `plt.scatter(distance_km, delivery_minutes)`."
            },
            {
                "test_id": "ix.tile_viz_labeling_chart_selection.s10.t03",
                "kind": "plotted_data_equals",
                "spec": {
                    "chart": "scatter",
                    "field": "y",
                    "expected": [14, 21, 28, 31, 38, 44],
                    "series": 0,
                    "axes": 0
                },
                "visible": True,
                "message_on_fail": "The scatter plot's y-values should be `delivery_minutes` = [14, 21, 28, 31, 38, 44]. Call `plt.scatter(distance_km, delivery_minutes)`."
            },
            {
                "test_id": "ix.tile_viz_labeling_chart_selection.s10.t04",
                "kind": "axes_property",
                "spec": {
                    "property": "xlabel",
                    "expected": "Distance (km)"
                },
                "visible": True,
                "message_on_fail": "Add `plt.xlabel('Distance (km)')` to label the x-axis."
            },
            {
                "test_id": "ix.tile_viz_labeling_chart_selection.s10.t05",
                "kind": "axes_property",
                "spec": {
                    "property": "ylabel",
                    "expected": "Delivery time (minutes)"
                },
                "visible": True,
                "message_on_fail": "Add `plt.ylabel('Delivery time (minutes)')` to label the y-axis."
            }
        ]
    },
    "feedback": {
        "correct": {
            "message": "Great work! Your scatter plot shows the relationship between distance and delivery time, and your comment correctly identifies why scatter — not bar — is the right choice here."
        },
        "incorrect": {
            "message": "Make sure you called `plt.scatter(distance_km, delivery_minutes)`, added both axis labels, and included a comment explaining why a scatter plot (relationship between two numerical variables) is better than a bar chart (category comparison) for this question."
        },
        "hints": [
            "A scatter plot is used when you want to see the relationship between two numerical variables — both axes are numeric.",
            "A bar chart compares a value across discrete categories; a scatter plot explores a relationship between two numbers."
        ]
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# TILE: tile_viz_custom_multi_panel
# Steps: s02 (choice), s03 (choice), s04 (code_exercise), s07 (choice), s08 (code_exercise)
# ─────────────────────────────────────────────────────────────────────────────

# s02: check — viz.custom_styling_theming#f1 — apply_matplotlib_style_sheet
# Taught by s01 (explainer): f1 = plt.style.use('style-name')
ix_custom_s02 = {
    "type": "choice",
    "interaction_id": "ix.tile_viz_custom_multi_panel.s02",
    "difficulty": "intro",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.custom_styling_theming",
            "capability": "apply_matplotlib_style_sheet",
            "fact_ids": ["f1"]
        }
    ],
    "anchors": [
        "viz.custom_styling_theming#assessment:apply_matplotlib_style_sheet"
    ],
    "public": {
        "prompt": "Which call applies matplotlib's built-in `'ggplot'` style sheet to all subsequent plots?",
        "options": [
            {
                "option_id": "opt_correct",
                "text": "`plt.style.use('ggplot')`"
            },
            {
                "option_id": "opt_sns",
                "text": "`sns.set_theme(style='ggplot')`"
            },
            {
                "option_id": "opt_rcparams",
                "text": "`mpl.rcParams['style'] = 'ggplot'`"
            },
            {
                "option_id": "opt_apply",
                "text": "`plt.style.apply('ggplot')`"
            }
        ],
        "selection": "single",
        "shuffle": True
    },
    "grading": {
        "correct_option_ids": ["opt_correct"],
        "option_feedback": {
            "opt_correct": {
                "message": "Correct. `plt.style.use('ggplot')` applies one of matplotlib's predefined style sheets; the available styles can be listed with `plt.style.available`."
            },
            "opt_sns": {
                "message": "`sns.set_theme()` applies seaborn's built-in themes, not matplotlib style sheets. To apply a matplotlib style sheet like `'ggplot'`, use `plt.style.use()`."
            },
            "opt_rcparams": {
                "message": "`mpl.rcParams` sets individual style properties (like `'lines.linewidth'`), not a whole style sheet. To apply a named style sheet, use `plt.style.use('ggplot')`."
            },
            "opt_apply": {
                "message": "`plt.style.apply()` is not a valid function. The correct function is `plt.style.use('style-name')`."
            }
        }
    },
    "feedback": {
        "correct": {
            "message": "Right. `plt.style.use('style-name')` applies a predefined style sheet; you can see all available names with `plt.style.available`."
        },
        "incorrect": {
            "message": "`plt.style.use('style-name')` is the function that applies a matplotlib style sheet. Pass the style name as a string, for example `plt.style.use('ggplot')`."
        },
        "hints": [
            "The function lives in the `plt.style` namespace and is called `use`.",
            "Style names are strings — for example `'ggplot'` or `'dark_background'`."
        ],
        "remediation_step_id": "tile_viz_custom_multi_panel.r01"
    }
}

# s03: check — viz.custom_styling_theming f1, f2, f3 — select_appropriate_styling_method
# Taught by s01 (explainer): f1, f2, f3
ix_custom_s03 = {
    "type": "choice",
    "interaction_id": "ix.tile_viz_custom_multi_panel.s03",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.custom_styling_theming",
            "capability": "select_appropriate_styling_method_for_branding_requirement",
            "fact_ids": ["f1", "f2", "f3"]
        }
    ],
    "anchors": [
        "viz.custom_styling_theming#assessment:select_appropriate_styling_method_for_branding_requirement"
    ],
    "public": {
        "prompt": "A team wants all their plots to use a specific brand color palette from seaborn. Which call sets the matplotlib color cycle to that palette for all subsequent plots?",
        "options": [
            {
                "option_id": "opt_set_palette",
                "text": "`sns.set_palette('pastel')`"
            },
            {
                "option_id": "opt_style_use",
                "text": "`plt.style.use('pastel')`"
            },
            {
                "option_id": "opt_rcparams",
                "text": "`mpl.rcParams['axes.prop_cycle'] = 'pastel'`"
            },
            {
                "option_id": "opt_set_theme",
                "text": "`sns.set_theme(palette='pastel')`"
            }
        ],
        "selection": "single",
        "shuffle": True
    },
    "grading": {
        "correct_option_ids": ["opt_set_palette"],
        "option_feedback": {
            "opt_set_palette": {
                "message": "Correct. `sns.set_palette(palette, ...)` sets the matplotlib color cycle from a seaborn palette, applying that color scheme to subsequent plots."
            },
            "opt_style_use": {
                "message": "`plt.style.use()` applies a matplotlib style sheet by name. `'pastel'` is a seaborn palette name, not a matplotlib style sheet name — use `sns.set_palette('pastel')` instead."
            },
            "opt_rcparams": {
                "message": "While `mpl.rcParams` can set individual properties, assigning a palette name string directly to `'axes.prop_cycle'` is not the correct syntax. Use `sns.set_palette('pastel')` to set a seaborn palette."
            },
            "opt_set_theme": {
                "message": "`sns.set_theme(palette='pastel')` would also set the palette, but it also changes the background style. The question asks specifically about setting the color palette — `sns.set_palette()` is the dedicated function for that."
            }
        }
    },
    "feedback": {
        "correct": {
            "message": "Correct. `sns.set_palette()` is the dedicated function for setting the matplotlib color cycle from a seaborn palette."
        },
        "incorrect": {
            "message": "`sns.set_palette('palette-name')` sets the matplotlib color cycle from a seaborn palette, applying that color scheme to all subsequent plots."
        },
        "hints": [
            "The question asks about setting a color palette specifically — there is a dedicated seaborn function for this.",
            "The function is `sns.set_palette()`, not `plt.style.use()` or `mpl.rcParams`."
        ],
        "remediation_step_id": "tile_viz_custom_multi_panel.r02"
    }
}

# s04: hands_on — code_exercise — viz.custom_styling_theming f2, f3
# Practice anchor: set_palette + rcParams change
# Allowed: import matplotlib as mpl, import matplotlib.pyplot as plt, import seaborn as sns,
#   sns.set_palette(palette_name), mpl.rcParams['axes.titlesize']=value, mpl.rcParams['lines.linewidth']=value,
#   plt.style.use('style-name'), plt.style.available, sns.lineplot(data=df,x=col,y=col), sns.barplot(data=df,x=col,y=col),
#   plt.title(str), plt.xlabel(str), plt.ylabel(str), plt.show()
# Blocked: plt.subplots(nrows, ncols), fig.add_subplot(), axes[i], FacetGrid, GridSpec
ix_custom_s04 = {
    "type": "code_exercise",
    "interaction_id": "ix.tile_viz_custom_multi_panel.s04",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.custom_styling_theming",
            "capability": "set_rcparams_globally",
            "fact_ids": ["f2"]
        },
        {
            "concept_id": "viz.custom_styling_theming",
            "capability": "apply_seaborn_custom_palette",
            "fact_ids": ["f3"]
        }
    ],
    "anchors": [
        "viz.custom_styling_theming#practice",
        "viz.custom_styling_theming#assessment:set_rcparams_globally",
        "viz.custom_styling_theming#assessment:apply_seaborn_custom_palette"
    ],
    "public": {
        "prompt": (
            "A small DataFrame `df` is already defined with columns `'category'` and `'value'`.\n\n"
            "1. Call `sns.set_palette('pastel')` to set the color palette.\n"
            "2. Set `mpl.rcParams['axes.titlesize']` to `16` to make titles larger.\n"
            "3. Call `sns.barplot(data=df, x='category', y='value')` to draw the bar chart.\n"
            "4. Add `plt.title('Delivery Times by City')` as the chart title.\n\n"
            "The plot should use the pastel palette and have a title with font size 16."
        ),
        "runtime": {
            "kind": "chart_renderer",
            "version": CHART_RENDERER_VERSION,
            "packages": ["matplotlib", "pandas", "seaborn"]
        },
        "workspace": {
            "files": [
                {
                    "path": "solution.py",
                    "role": "editable",
                    "language": "python",
                    "content": (
                        "import matplotlib as mpl\n"
                        "import matplotlib.pyplot as plt\n"
                        "import seaborn as sns\n"
                        "import pandas as pd\n\n"
                        "df = pd.DataFrame({\n"
                        "    'category': ['Lagos', 'Abuja', 'Kano'],\n"
                        "    'value': [24.0, 27.0, 30.0]\n"
                        "})\n\n"
                        "# 1. Set the seaborn palette\n"
                        "# sns.set_palette(...)\n\n"
                        "# 2. Set the title font size via rcParams\n"
                        "# mpl.rcParams[...] = ...\n\n"
                        "# 3. Draw the bar chart\n"
                        "# sns.barplot(...)\n\n"
                        "# 4. Add the title\n"
                        "# plt.title(...)\n"
                    )
                }
            ],
            "entry": "solution.py",
            "asset_mounts": []
        },
        "constraints": {
            "allowed_syntax": [
                "import matplotlib as mpl",
                "import matplotlib.pyplot as plt",
                "import seaborn as sns",
                "sns.set_palette(palette_name)",
                "mpl.rcParams['axes.titlesize'] = value",
                "mpl.rcParams['lines.linewidth'] = value",
                "plt.style.use('style-name')",
                "plt.style.available",
                "sns.lineplot(data=df, x=col, y=col)",
                "sns.barplot(data=df, x=col, y=col)",
                "plt.title(str)",
                "plt.xlabel(str)",
                "plt.ylabel(str)",
                "plt.show()"
            ],
            "blocked_syntax": [
                "plt.subplots(nrows, ncols)",
                "fig.add_subplot()",
                "axes[i]",
                "FacetGrid",
                "GridSpec"
            ]
        }
    },
    "grading": {
        "solution_files": [
            {
                "path": "solution.py",
                "content": (
                    "import matplotlib as mpl\n"
                    "import matplotlib.pyplot as plt\n"
                    "import seaborn as sns\n"
                    "import pandas as pd\n\n"
                    "df = pd.DataFrame({\n"
                    "    'category': ['Lagos', 'Abuja', 'Kano'],\n"
                    "    'value': [24.0, 27.0, 30.0]\n"
                    "})\n\n"
                    "sns.set_palette('pastel')\n"
                    "mpl.rcParams['axes.titlesize'] = 16\n"
                    "sns.barplot(data=df, x='category', y='value')\n"
                    "plt.title('Delivery Times by City')\n"
                )
            }
        ],
        "tests": [
            {
                "test_id": "ix.tile_viz_custom_multi_panel.s04.t01",
                "kind": "figure_equals",
                "spec": {
                    "expected": {
                        "n_axes": 1,
                        "chart_types": [["bar"]]
                    }
                },
                "visible": True,
                "message_on_fail": "Your figure should contain one Axes with a bar chart. Call `sns.barplot(data=df, x='category', y='value')`."
            },
            {
                "test_id": "ix.tile_viz_custom_multi_panel.s04.t02",
                "kind": "axes_property",
                "spec": {
                    "property": "title",
                    "expected": "Delivery Times by City"
                },
                "visible": True,
                "message_on_fail": "Add `plt.title('Delivery Times by City')` to set the chart title."
            },
            {
                "test_id": "ix.tile_viz_custom_multi_panel.s04.t03",
                "kind": "plotted_data_equals",
                "spec": {
                    "chart": "bar",
                    "field": "heights",
                    "expected": [24.0, 27.0, 30.0],
                    "series": 0,
                    "axes": 0
                },
                "visible": True,
                "message_on_fail": "The bar chart should show values [24.0, 27.0, 30.0] for Lagos, Abuja, Kano. Call `sns.barplot(data=df, x='category', y='value')`."
            }
        ]
    },
    "feedback": {
        "correct": {
            "message": "Well done! You set a custom seaborn palette with `sns.set_palette()` and changed a global rcParam with `mpl.rcParams['axes.titlesize']` — both affect all subsequent plots."
        },
        "incorrect": {
            "message": "Make sure you called `sns.set_palette('pastel')`, set `mpl.rcParams['axes.titlesize'] = 16`, drew the bar chart with `sns.barplot(data=df, x='category', y='value')`, and added `plt.title('Delivery Times by City')`."
        },
        "hints": [
            "Call `sns.set_palette('pastel')` and `mpl.rcParams['axes.titlesize'] = 16` before the plot call so they take effect.",
            "`mpl.rcParams` is a dictionary — set a key like `mpl.rcParams['axes.titlesize'] = 16`."
        ]
    }
}

# s07: check — viz.multi_panel_figures#f2 — index_and_plot_on_individual_axes_independently
# Taught by s05 (explainer): f1, f2
ix_custom_s07 = {
    "type": "choice",
    "interaction_id": "ix.tile_viz_custom_multi_panel.s07",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.multi_panel_figures",
            "capability": "index_and_plot_on_individual_axes_independently",
            "fact_ids": ["f2"]
        }
    ],
    "anchors": [
        "viz.multi_panel_figures#assessment:index_and_plot_on_individual_axes_independently"
    ],
    "public": {
        "prompt": "After `fig, axs = plt.subplots(2, 2)`, you want to draw a histogram in the top-right panel only. Which call is correct?",
        "options": [
            {
                "option_id": "opt_correct",
                "text": "`axs[0, 1].hist(data)`"
            },
            {
                "option_id": "opt_wrong_index",
                "text": "`axs[1, 0].hist(data)`"
            },
            {
                "option_id": "opt_fig",
                "text": "`fig.hist(data, position=(0, 1))`"
            },
            {
                "option_id": "opt_plt",
                "text": "`plt.hist(data)` — it automatically goes to the top-right panel"
            }
        ],
        "selection": "single",
        "shuffle": True
    },
    "grading": {
        "correct_option_ids": ["opt_correct"],
        "option_feedback": {
            "opt_correct": {
                "message": "Correct. `axs[0, 1]` selects row 0 (top), column 1 (right). Calling `.hist()` on that Axes draws only into that panel."
            },
            "opt_wrong_index": {
                "message": "`axs[1, 0]` selects row 1 (bottom), column 0 (left) — that is the bottom-left panel, not the top-right. The top-right is `axs[0, 1]`."
            },
            "opt_fig": {
                "message": "The Figure object does not have a `hist()` method. Plotting calls go on individual Axes objects, indexed as `axs[row, col]`."
            },
            "opt_plt": {
                "message": "`plt.hist()` draws on the current active Axes, not necessarily the top-right panel. To target a specific panel, use `axs[0, 1].hist(data)`."
            }
        }
    },
    "feedback": {
        "correct": {
            "message": "Right. In a 2×2 grid, `axs[0, 1]` is row 0 (top), column 1 (right). Calls on that Axes only affect that panel."
        },
        "incorrect": {
            "message": "In a 2×2 grid, rows and columns are 0-indexed: `axs[0, 0]` is top-left, `axs[0, 1]` is top-right, `axs[1, 0]` is bottom-left, `axs[1, 1]` is bottom-right."
        },
        "hints": [
            "The first index is the row (0 = top, 1 = bottom); the second is the column (0 = left, 1 = right).",
            "Top-right means row 0, column 1 — so `axs[0, 1]`."
        ],
        "remediation_step_id": "tile_viz_custom_multi_panel.r03"
    }
}

# s08: hands_on — code_exercise — viz.multi_panel_figures f1
# Practice anchor: 2×2 grid, each panel a histogram of a different numeric column
# Allowed: plt.subplots(2,2), axs[0,0].hist(...), axs[0,1].hist(...), axs[1,0].hist(...), axs[1,1].hist(...),
#   axs[row,col].set_title(...), axs[row,col].set_xlabel(...), axs[row,col].set_ylabel(...),
#   plt.tight_layout(), plt.show()
# Dataset: ds.orders (delivery_time_minutes, distance_km, order_value, num_items)
ix_custom_s08 = {
    "type": "code_exercise",
    "interaction_id": "ix.tile_viz_custom_multi_panel.s08",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.multi_panel_figures",
            "capability": "create_subplot_grid_with_subplots",
            "fact_ids": ["f1"]
        }
    ],
    "anchors": [
        "viz.multi_panel_figures#practice",
        "viz.multi_panel_figures#assessment:create_subplot_grid_with_subplots"
    ],
    "public": {
        "prompt": (
            "The `orders` DataFrame is already loaded with columns `delivery_time_minutes`, `distance_km`, `order_value`, and `num_items`.\n\n"
            "Create a 2×2 grid of subplots and draw one histogram per panel:\n"
            "- `axs[0, 0]`: histogram of `orders['delivery_time_minutes']`\n"
            "- `axs[0, 1]`: histogram of `orders['distance_km']`\n"
            "- `axs[1, 0]`: histogram of `orders['order_value']`\n"
            "- `axs[1, 1]`: histogram of `orders['num_items']`\n\n"
            "Use `fig, axs = plt.subplots(2, 2)` to create the grid, then call `.hist()` on each `axs[row, col]`."
        ),
        "runtime": {
            "kind": "chart_renderer",
            "version": CHART_RENDERER_VERSION,
            "packages": ["matplotlib", "pandas"]
        },
        "workspace": {
            "files": [
                {
                    "path": "solution.py",
                    "role": "editable",
                    "language": "python",
                    "content": (
                        "import matplotlib.pyplot as plt\n"
                        "import pandas as pd\n\n"
                        "orders = pd.read_csv('orders.csv')\n\n"
                        "# Create a 2x2 grid\n"
                        "# fig, axs = ___\n\n"
                        "# Plot each column in its panel\n"
                        "# axs[0, 0].hist(...)\n"
                        "# axs[0, 1].hist(...)\n"
                        "# axs[1, 0].hist(...)\n"
                        "# axs[1, 1].hist(...)\n\n"
                        "# plt.tight_layout()\n"
                    )
                }
            ],
            "entry": "solution.py",
            "asset_mounts": [
                {
                    "asset_id": "ds.orders",
                    "mount_path": "orders.csv"
                }
            ]
        },
        "constraints": {
            "allowed_syntax": [
                "plt.subplots(2, 2)",
                "axs[0, 0].hist(...)",
                "axs[0, 1].hist(...)",
                "axs[1, 0].hist(...)",
                "axs[1, 1].hist(...)",
                "axs[row, col].set_title(...)",
                "axs[row, col].set_xlabel(...)",
                "axs[row, col].set_ylabel(...)",
                "plt.tight_layout()",
                "plt.show()"
            ],
            "blocked_syntax": []
        }
    },
    "grading": {
        "solution_files": [
            {
                "path": "solution.py",
                "content": (
                    "import matplotlib.pyplot as plt\n"
                    "import pandas as pd\n\n"
                    "orders = pd.read_csv('orders.csv')\n\n"
                    "fig, axs = plt.subplots(2, 2)\n\n"
                    "axs[0, 0].hist(orders['delivery_time_minutes'])\n"
                    "axs[0, 1].hist(orders['distance_km'])\n"
                    "axs[1, 0].hist(orders['order_value'])\n"
                    "axs[1, 1].hist(orders['num_items'])\n\n"
                    "plt.tight_layout()\n"
                )
            }
        ],
        "tests": [
            {
                "test_id": "ix.tile_viz_custom_multi_panel.s08.t01",
                "kind": "figure_equals",
                "spec": {
                    "expected": {
                        "n_axes": 4,
                        "chart_types": [["hist"], ["hist"], ["hist"], ["hist"]]
                    }
                },
                "visible": True,
                "message_on_fail": "Your figure should contain exactly 4 Axes, each with a histogram. Use `fig, axs = plt.subplots(2, 2)` and call `.hist()` on each panel."
            },
            {
                "test_id": "ix.tile_viz_custom_multi_panel.s08.t02",
                "kind": "plotted_data_equals",
                "spec": {
                    "chart": "hist",
                    "field": "n",
                    "expected": 24,
                    "series": 0,
                    "axes": 0
                },
                "visible": True,
                "message_on_fail": "The top-left panel (`axs[0, 0]`) should show a histogram of `delivery_time_minutes` with 24 data points. Call `axs[0, 0].hist(orders['delivery_time_minutes'])`."
            }
        ]
    },
    "feedback": {
        "correct": {
            "message": "Excellent! You created a 2×2 subplot grid and drew a distinct histogram in each panel — each Axes is independent."
        },
        "incorrect": {
            "message": "Make sure you used `fig, axs = plt.subplots(2, 2)` to create the grid, then called `.hist()` on each of the four `axs[row, col]` objects with a different column."
        },
        "hints": [
            "Start with `fig, axs = plt.subplots(2, 2)` to get a 2×2 grid of Axes.",
            "Each panel is addressed by `axs[row, col]` — for example `axs[0, 0]` is top-left and `axs[1, 1]` is bottom-right."
        ]
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# TILE: tile_viz_seaborn_stats_themes
# Steps: s02 (choice), s03 (code_exercise), s05 (choice), s06 (choice), s07 (code_exercise), s09 (choice), s10 (code_exercise)
# ─────────────────────────────────────────────────────────────────────────────

# s02: check — viz.seaborn_dataframe_plotting f1, f2 — build_seaborn_barplot_from_dataframe
# Taught by s01 (explainer): f1, f2
ix_seaborn_s02 = {
    "type": "choice",
    "interaction_id": "ix.tile_viz_seaborn_stats_themes.s02",
    "difficulty": "intro",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.seaborn_dataframe_plotting",
            "capability": "build_seaborn_barplot_from_dataframe_using_column_names",
            "fact_ids": ["f1", "f2"]
        }
    ],
    "anchors": [
        "viz.seaborn_dataframe_plotting#assessment:build_seaborn_barplot_from_dataframe_using_column_names"
    ],
    "public": {
        "prompt": "You have a DataFrame `orders` with columns `'city'` and `'delivery_time_minutes'`. Which seaborn call produces a bar chart of mean delivery time per city, without a separate `.groupby()` call?",
        "options": [
            {
                "option_id": "opt_correct",
                "text": "`sns.barplot(data=orders, x='city', y='delivery_time_minutes')`"
            },
            {
                "option_id": "opt_groupby",
                "text": "`sns.barplot(orders.groupby('city')['delivery_time_minutes'].mean())`"
            },
            {
                "option_id": "opt_arrays",
                "text": "`sns.barplot(x=orders['city'], y=orders['delivery_time_minutes'].mean())`"
            },
            {
                "option_id": "opt_plt",
                "text": "`plt.bar(orders['city'], orders['delivery_time_minutes'])`"
            }
        ],
        "selection": "single",
        "shuffle": True
    },
    "grading": {
        "correct_option_ids": ["opt_correct"],
        "option_feedback": {
            "opt_correct": {
                "message": "Correct. Seaborn takes the DataFrame via `data=` and column names via `x=` and `y=`, then computes the mean per category automatically — no `.groupby()` needed."
            },
            "opt_groupby": {
                "message": "Seaborn does not need a `.groupby()` call first. Pass the full DataFrame to `data=` and the column names to `x=` and `y=` — seaborn computes the mean per category automatically."
            },
            "opt_arrays": {
                "message": "Passing `orders['delivery_time_minutes'].mean()` gives a single scalar, not per-city means. Pass the full DataFrame to `data=` and the column name string to `y=` — seaborn handles the aggregation."
            },
            "opt_plt": {
                "message": "`plt.bar()` is a matplotlib function that requires pre-aggregated data. Seaborn's `sns.barplot()` accepts the raw DataFrame and computes the mean per category automatically."
            }
        }
    },
    "feedback": {
        "correct": {
            "message": "Right. Seaborn's `data=`, `x=`, `y=` interface lets you pass the DataFrame and column names directly — it handles the aggregation for you."
        },
        "incorrect": {
            "message": "Use `sns.barplot(data=orders, x='city', y='delivery_time_minutes')`. Seaborn takes the full DataFrame and column name strings, then computes the mean per category automatically."
        },
        "hints": [
            "Seaborn's plotting functions take `data=` (the DataFrame) and `x=`/`y=` (column name strings), not extracted arrays.",
            "No `.groupby()` is needed — seaborn computes the mean per category automatically."
        ],
        "remediation_step_id": "tile_viz_seaborn_stats_themes.r01"
    }
}

# s03: hands_on — code_exercise — viz.seaborn_dataframe_plotting f1, f2
# Practice anchor: sns.barplot(data=orders, x='city', y='delivery_time_minutes')
# Dataset: ds.orders
# Allowed: import seaborn as sns, sns.barplot(data=...,x=...,y=...), import pandas as pd, pd.DataFrame(...), import matplotlib.pyplot as plt, plt.show()
# Blocked: sns.set_theme(), sns.set_style(), sns.set_palette(), sns.FacetGrid(), sns.catplot(), sns.histplot(), sns.boxplot(), sns.scatterplot(), sns.lineplot(), estimator=, hue=, col=, row=
ix_seaborn_s03 = {
    "type": "code_exercise",
    "interaction_id": "ix.tile_viz_seaborn_stats_themes.s03",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.seaborn_dataframe_plotting",
            "capability": "build_seaborn_barplot_from_dataframe_using_column_names",
            "fact_ids": ["f1", "f2"]
        }
    ],
    "anchors": [
        "viz.seaborn_dataframe_plotting#practice",
        "viz.seaborn_dataframe_plotting#assessment:build_seaborn_barplot_from_dataframe_using_column_names"
    ],
    "public": {
        "prompt": (
            "The `orders` DataFrame is already loaded with columns `'city'` and `'delivery_time_minutes'`.\n\n"
            "Call `sns.barplot(data=orders, x='city', y='delivery_time_minutes')` to produce a bar chart "
            "showing the mean delivery time per city.\n\n"
            "The figure should show one bar per city (Lagos, Abuja, Kano), with error bars drawn automatically by seaborn."
        ),
        "runtime": {
            "kind": "chart_renderer",
            "version": CHART_RENDERER_VERSION,
            "packages": ["matplotlib", "pandas", "seaborn"]
        },
        "workspace": {
            "files": [
                {
                    "path": "solution.py",
                    "role": "editable",
                    "language": "python",
                    "content": (
                        "import seaborn as sns\n"
                        "import pandas as pd\n"
                        "import matplotlib.pyplot as plt\n\n"
                        "orders = pd.read_csv('orders.csv')\n\n"
                        "# Draw a seaborn bar chart: mean delivery_time_minutes per city\n"
                        "# sns.barplot(...)\n"
                    )
                }
            ],
            "entry": "solution.py",
            "asset_mounts": [
                {
                    "asset_id": "ds.orders",
                    "mount_path": "orders.csv"
                }
            ]
        },
        "constraints": {
            "allowed_syntax": [
                "import seaborn as sns",
                "sns.barplot(data=..., x=..., y=...)",
                "import pandas as pd",
                "pd.DataFrame(...)",
                "import matplotlib.pyplot as plt",
                "plt.show()"
            ],
            "blocked_syntax": [
                "sns.set_theme()",
                "sns.set_style()",
                "sns.set_palette()",
                "sns.FacetGrid()",
                "sns.catplot()",
                "sns.histplot()",
                "sns.boxplot()",
                "sns.scatterplot()",
                "sns.lineplot()",
                "estimator=",
                "hue=",
                "col=",
                "row="
            ]
        }
    },
    "grading": {
        "solution_files": [
            {
                "path": "solution.py",
                "content": (
                    "import seaborn as sns\n"
                    "import pandas as pd\n"
                    "import matplotlib.pyplot as plt\n\n"
                    "orders = pd.read_csv('orders.csv')\n\n"
                    "sns.barplot(data=orders, x='city', y='delivery_time_minutes')\n"
                )
            }
        ],
        "tests": [
            {
                "test_id": "ix.tile_viz_seaborn_stats_themes.s03.t01",
                "kind": "figure_equals",
                "spec": {
                    "expected": {
                        "n_axes": 1,
                        "chart_types": [["bar"]]
                    }
                },
                "visible": True,
                "message_on_fail": "Your figure should contain one Axes with a bar chart. Call `sns.barplot(data=orders, x='city', y='delivery_time_minutes')`."
            },
            {
                "test_id": "ix.tile_viz_seaborn_stats_themes.s03.t02",
                "kind": "axes_property",
                "spec": {
                    "property": "xticklabels",
                    "expected": ["Abuja", "Kano", "Lagos"]
                },
                "visible": True,
                "message_on_fail": "The x-axis should show city names (Abuja, Kano, Lagos). Pass `x='city'` to `sns.barplot()`."
            }
        ]
    },
    "feedback": {
        "correct": {
            "message": "Well done! `sns.barplot()` computed the mean per city and drew error bars automatically — no `.groupby()` needed."
        },
        "incorrect": {
            "message": "Call `sns.barplot(data=orders, x='city', y='delivery_time_minutes')`. Pass the DataFrame to `data=` and the column name strings to `x=` and `y=`."
        },
        "hints": [
            "The three keyword arguments are `data=orders`, `x='city'`, and `y='delivery_time_minutes'`.",
            "Seaborn computes the mean per category automatically — you do not need to call `.groupby()` first."
        ]
    }
}

# s05: check — viz.seaborn_statistical_functions#f1 — identify_seaborn_automatic_statistical_estimation
# Taught by s04 (explainer): f1, f2
ix_seaborn_s05 = {
    "type": "choice",
    "interaction_id": "ix.tile_viz_seaborn_stats_themes.s05",
    "difficulty": "intro",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.seaborn_statistical_functions",
            "capability": "identify_seaborn_automatic_statistical_estimation",
            "fact_ids": ["f1"]
        }
    ],
    "anchors": [
        "viz.seaborn_statistical_functions#assessment:identify_seaborn_automatic_statistical_estimation"
    ],
    "public": {
        "prompt": "Which statement best describes what seaborn does when you call `sns.barplot(data=orders, x='city', y='delivery_time_minutes')`?",
        "options": [
            {
                "option_id": "opt_correct",
                "text": "Seaborn automatically computes the mean delivery time per city and draws a bar for each, without a separate aggregation step."
            },
            {
                "option_id": "opt_raw",
                "text": "Seaborn draws one bar per row in the DataFrame, using the raw `delivery_time_minutes` value as the bar height."
            },
            {
                "option_id": "opt_manual",
                "text": "Seaborn requires you to compute the mean per city with `.groupby()` before calling `sns.barplot()`."
            },
            {
                "option_id": "opt_sum",
                "text": "Seaborn automatically computes the sum of delivery times per city and draws a bar for each."
            }
        ],
        "selection": "single",
        "shuffle": True
    },
    "grading": {
        "correct_option_ids": ["opt_correct"],
        "option_feedback": {
            "opt_correct": {
                "message": "Correct. Many seaborn functions automatically perform the statistical estimation necessary to answer questions such as the average value of one variable as a function of other variables."
            },
            "opt_raw": {
                "message": "Seaborn does not draw one bar per row. It aggregates the data — by default computing the mean per category — and draws one bar per category."
            },
            "opt_manual": {
                "message": "Seaborn does not require a `.groupby()` call. It performs the statistical estimation (mean per category) automatically when you pass the full DataFrame and column names."
            },
            "opt_sum": {
                "message": "Seaborn's default estimator is the mean, not the sum. It computes the mean delivery time per city and draws one bar per city."
            }
        }
    },
    "feedback": {
        "correct": {
            "message": "Right. Seaborn automatically performs statistical estimation — `sns.barplot()` computes the mean per category without any manual aggregation."
        },
        "incorrect": {
            "message": "Seaborn automatically performs the statistical estimation (mean per category by default) when you pass the full DataFrame and column names — no `.groupby()` needed."
        },
        "hints": [
            "Think about what 'automatic statistical estimation' means — seaborn does the aggregation for you.",
            "The default estimator in `sns.barplot()` is the mean, not the sum or raw values."
        ],
        "remediation_step_id": "tile_viz_seaborn_stats_themes.r02"
    }
}

# s06: check — viz.seaborn_statistical_functions f1, f2 — select_correct_seaborn_statistical_function
# Taught by s04 (explainer): f1, f2
ix_seaborn_s06 = {
    "type": "choice",
    "interaction_id": "ix.tile_viz_seaborn_stats_themes.s06",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.seaborn_statistical_functions",
            "capability": "select_correct_seaborn_statistical_function_for_given_question",
            "fact_ids": ["f1", "f2"]
        }
    ],
    "anchors": [
        "viz.seaborn_statistical_functions#assessment:select_correct_seaborn_statistical_function_for_given_question"
    ],
    "public": {
        "prompt": "An analyst wants to visualize whether longer delivery distances tend to produce longer delivery times, with a fitted trend line drawn through the scatter points. Which seaborn call is correct?",
        "options": [
            {
                "option_id": "opt_regplot",
                "text": "`sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')`"
            },
            {
                "option_id": "opt_barplot",
                "text": "`sns.barplot(data=orders, x='distance_km', y='delivery_time_minutes')`"
            },
            {
                "option_id": "opt_scatter",
                "text": "`plt.scatter(orders['distance_km'], orders['delivery_time_minutes'])`"
            },
            {
                "option_id": "opt_lineplot",
                "text": "`sns.lineplot(data=orders, x='distance_km', y='delivery_time_minutes')`"
            }
        ],
        "selection": "single",
        "shuffle": True
    },
    "grading": {
        "correct_option_ids": ["opt_regplot"],
        "option_feedback": {
            "opt_regplot": {
                "message": "Correct. `sns.regplot(data=..., x=..., y=...)` plots a scatterplot of the observations together with a fitted linear regression line — exactly what is needed to visualize the trend."
            },
            "opt_barplot": {
                "message": "`sns.barplot()` computes the mean per category and draws bars. `distance_km` is a continuous numeric variable, not a category — use `sns.regplot()` to show the scatter and fitted trend line."
            },
            "opt_scatter": {
                "message": "`plt.scatter()` shows the data points but does not add a fitted trend line. To get both the scatter and the regression line in one call, use `sns.regplot()`."
            },
            "opt_lineplot": {
                "message": "`sns.lineplot()` connects data points with a line in the order they appear. It does not fit a regression line. Use `sns.regplot()` to get a scatter plot with a fitted linear regression line."
            }
        }
    },
    "feedback": {
        "correct": {
            "message": "Right. `sns.regplot()` produces a scatterplot with a fitted linear regression line in a single call."
        },
        "incorrect": {
            "message": "`sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')` plots the scatter points and fits a linear regression line through them automatically."
        },
        "hints": [
            "The question asks for a scatter plot with a fitted trend line — which seaborn function adds both in one call?",
            "`sns.regplot()` stands for 'regression plot' — it adds the fitted line automatically."
        ],
        "remediation_step_id": "tile_viz_seaborn_stats_themes.r02"
    }
}

# s07: hands_on — code_exercise — viz.seaborn_statistical_functions f2
# Practice anchor: sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')
# Dataset: ds.orders
# Allowed: import seaborn as sns, sns.regplot(data=...,x=...,y=...), import pandas as pd, pd.DataFrame(...), sns.barplot(data=...,x=...,y=...)
# Blocked: sns.set_theme(), sns.set_style(), sns.set_palette(), plt.subplots(), fig/axes, sns.FacetGrid(), sns.lmplot()
ix_seaborn_s07 = {
    "type": "code_exercise",
    "interaction_id": "ix.tile_viz_seaborn_stats_themes.s07",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.seaborn_statistical_functions",
            "capability": "apply_regplot_to_visualize_relationship_with_fitted_trend",
            "fact_ids": ["f2"]
        }
    ],
    "anchors": [
        "viz.seaborn_statistical_functions#practice",
        "viz.seaborn_statistical_functions#assessment:apply_regplot_to_visualize_relationship_with_fitted_trend"
    ],
    "public": {
        "prompt": (
            "The `orders` DataFrame is already loaded with columns `'distance_km'` and `'delivery_time_minutes'`.\n\n"
            "Call `sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')` to produce a scatter plot "
            "of the observations with a fitted linear regression line drawn through them.\n\n"
            "The figure should show individual data points and a fitted trend line, produced by a single `sns.regplot()` call."
        ),
        "runtime": {
            "kind": "chart_renderer",
            "version": CHART_RENDERER_VERSION,
            "packages": ["matplotlib", "pandas", "seaborn"]
        },
        "workspace": {
            "files": [
                {
                    "path": "solution.py",
                    "role": "editable",
                    "language": "python",
                    "content": (
                        "import seaborn as sns\n"
                        "import pandas as pd\n\n"
                        "orders = pd.read_csv('orders.csv')\n\n"
                        "# Draw a scatter plot with a fitted regression line\n"
                        "# sns.regplot(...)\n"
                    )
                }
            ],
            "entry": "solution.py",
            "asset_mounts": [
                {
                    "asset_id": "ds.orders",
                    "mount_path": "orders.csv"
                }
            ]
        },
        "constraints": {
            "allowed_syntax": [
                "import seaborn as sns",
                "sns.regplot(data=..., x=..., y=...)",
                "import pandas as pd",
                "pd.DataFrame(...)",
                "sns.barplot(data=..., x=..., y=...)"
            ],
            "blocked_syntax": [
                "sns.set_theme()",
                "sns.set_style()",
                "sns.set_palette()",
                "plt.subplots()",
                "fig, axes",
                "sns.FacetGrid()",
                "sns.lmplot()"
            ]
        }
    },
    "grading": {
        "solution_files": [
            {
                "path": "solution.py",
                "content": (
                    "import seaborn as sns\n"
                    "import pandas as pd\n\n"
                    "orders = pd.read_csv('orders.csv')\n\n"
                    "sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')\n"
                )
            }
        ],
        "tests": [
            {
                "test_id": "ix.tile_viz_seaborn_stats_themes.s07.t01",
                "kind": "figure_equals",
                "spec": {
                    "expected": {
                        "n_axes": 1,
                        "chart_types": [["scatter"]]
                    }
                },
                "visible": True,
                "message_on_fail": "Your figure should contain one Axes with a scatter plot (plus a regression line). Call `sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')`."
            },
            {
                "test_id": "ix.tile_viz_seaborn_stats_themes.s07.t02",
                "kind": "plotted_data_equals",
                "spec": {
                    "chart": "scatter",
                    "field": "x",
                    "expected": [2.1, 3.4, 2.8, 4.5, 5.2, 3.9, 4.8, 9.1,
                                 3.2, 4.1, 3.0, 5.5, 4.3, 4.7, 4.0, 5.8,
                                 4.6, 5.9, 4.2, 6.8, 5.3, 6.1, 5.0, 7.2],
                    "series": 0,
                    "axes": 0,
                    "sorted": False
                },
                "visible": True,
                "message_on_fail": "The scatter plot should use `distance_km` as the x-axis. Pass `x='distance_km'` to `sns.regplot()`."
            }
        ]
    },
    "feedback": {
        "correct": {
            "message": "Well done! `sns.regplot()` drew the scatter points and fitted the regression line automatically in a single call."
        },
        "incorrect": {
            "message": "Call `sns.regplot(data=orders, x='distance_km', y='delivery_time_minutes')`. Pass the DataFrame to `data=` and the column name strings to `x=` and `y=`."
        },
        "hints": [
            "The three keyword arguments are `data=orders`, `x='distance_km'`, and `y='delivery_time_minutes'`.",
            "`sns.regplot()` adds the fitted regression line automatically — you do not need a separate call."
        ]
    }
}

# s09: check — viz.seaborn_themes_palettes#f1 — explain_global_rcparams_effect_on_subsequent_plots
# Taught by s08 (explainer): f1 (tb2), f2 (tb1)
ix_seaborn_s09 = {
    "type": "choice",
    "interaction_id": "ix.tile_viz_seaborn_stats_themes.s09",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.seaborn_themes_palettes",
            "capability": "explain_global_rcparams_effect_on_subsequent_plots",
            "fact_ids": ["f1"]
        }
    ],
    "anchors": [
        "viz.seaborn_themes_palettes#assessment:explain_global_rcparams_effect_on_subsequent_plots"
    ],
    "public": {
        "prompt": "A notebook cell calls `sns.set_theme(style='whitegrid', palette='deep')` and then draws a seaborn bar chart. The next cell draws a plain matplotlib line chart without calling `sns.set_theme()` again. What will the matplotlib line chart look like?",
        "options": [
            {
                "option_id": "opt_correct",
                "text": "It will use the whitegrid style and deep palette, because `sns.set_theme()` changes global matplotlib rcParams that affect all subsequent plots."
            },
            {
                "option_id": "opt_default",
                "text": "It will use default matplotlib styling, because `sns.set_theme()` only affects seaborn plots."
            },
            {
                "option_id": "opt_error",
                "text": "It will raise an error, because `sns.set_theme()` must be called before every plot."
            },
            {
                "option_id": "opt_retroactive",
                "text": "The seaborn bar chart will be restyled to match the matplotlib defaults."
            }
        ],
        "selection": "single",
        "shuffle": True
    },
    "grading": {
        "correct_option_ids": ["opt_correct"],
        "option_feedback": {
            "opt_correct": {
                "message": "Correct. `sns.set_theme()` changes the global defaults for all plots using the matplotlib rcParams system, so it affects matplotlib plots too, even ones not made with seaborn."
            },
            "opt_default": {
                "message": "`sns.set_theme()` does not only affect seaborn plots. It changes the global matplotlib rcParams, so all subsequent plots — including plain matplotlib ones — use the new style."
            },
            "opt_error": {
                "message": "`sns.set_theme()` does not need to be called before every plot. Once called, it changes the global rcParams, which persist for all subsequent plots in the session."
            },
            "opt_retroactive": {
                "message": "`sns.set_theme()` changes defaults for plots drawn after the call — it does not go back and restyle a figure you already drew and displayed earlier."
            }
        }
    },
    "feedback": {
        "correct": {
            "message": "Right. `sns.set_theme()` works by changing matplotlib's global rcParams, so it affects every plot drawn after the call — seaborn or not."
        },
        "incorrect": {
            "message": "`sns.set_theme()` changes the global matplotlib rcParams. Because it changes global defaults, all plots drawn after the call — including plain matplotlib plots — use the new style."
        },
        "hints": [
            "Think about what 'global defaults' means — once changed, they apply to everything drawn afterward.",
            "`sns.set_theme()` works through matplotlib's rcParams system, not a seaborn-only mechanism."
        ],
        "remediation_step_id": "tile_viz_seaborn_stats_themes.r03"
    }
}

# s10: hands_on — code_exercise — viz.seaborn_themes_palettes f1, f2
# Practice anchor: sns.set_theme(style=..., palette=...) before a seaborn plot
# Dataset: ds.theming_demo (category, value)
# Allowed: import seaborn as sns, import pandas as pd, sns.set_theme(style=...,palette=...), sns.barplot(...), sns.scatterplot(...), sns.histplot(...), pd.DataFrame(...), variable assignment, string literals
# Blocked: matplotlib.rcParams direct manipulation, sns.set_style(), sns.set_palette(), plt.style.use(), custom theme dictionaries, subplots/multi-panel figures
ix_seaborn_s10 = {
    "type": "code_exercise",
    "interaction_id": "ix.tile_viz_seaborn_stats_themes.s10",
    "difficulty": "core",
    "grading_mode": "client",
    "standalone": False,
    "measures": [
        {
            "concept_id": "viz.seaborn_themes_palettes",
            "capability": "apply_seaborn_theme_and_palette_to_produce_polished_plot",
            "fact_ids": ["f1", "f2"]
        },
        {
            "concept_id": "viz.seaborn_themes_palettes",
            "capability": "identify_style_and_palette_parameters_and_their_defaults",
            "fact_ids": ["f2"]
        }
    ],
    "anchors": [
        "viz.seaborn_themes_palettes#practice",
        "viz.seaborn_themes_palettes#assessment:apply_seaborn_theme_and_palette_to_produce_polished_plot",
        "viz.seaborn_themes_palettes#assessment:identify_style_and_palette_parameters_and_their_defaults"
    ],
    "public": {
        "prompt": (
            "A small DataFrame `df` is already defined with columns `'category'` and `'value'`.\n\n"
            "1. Call `sns.set_theme(style='whitegrid', palette='deep')` before the plot.\n"
            "2. Call `sns.barplot(data=df, x='category', y='value')` to draw the bar chart.\n\n"
            "The figure should use the whitegrid style (white background with horizontal gridlines) "
            "and the deep color palette, with `sns.set_theme()` called before the plot function."
        ),
        "runtime": {
            "kind": "chart_renderer",
            "version": CHART_RENDERER_VERSION,
            "packages": ["matplotlib", "pandas", "seaborn"]
        },
        "workspace": {
            "files": [
                {
                    "path": "solution.py",
                    "role": "editable",
                    "language": "python",
                    "content": (
                        "import seaborn as sns\n"
                        "import pandas as pd\n\n"
                        "df = pd.DataFrame({\n"
                        "    'category': ['Lagos', 'Abuja', 'Kano'],\n"
                        "    'value': [24.0, 27.0, 30.0]\n"
                        "})\n\n"
                        "# 1. Set the theme before drawing\n"
                        "# sns.set_theme(...)\n\n"
                        "# 2. Draw the bar chart\n"
                        "# sns.barplot(...)\n"
                    )
                }
            ],
            "entry": "solution.py",
            "asset_mounts": []
        },
        "constraints": {
            "allowed_syntax": [
                "import seaborn as sns",
                "import pandas as pd",
                "sns.set_theme(style=..., palette=...)",
                "sns.barplot(...)",
                "sns.scatterplot(...)",
                "sns.histplot(...)",
                "pd.DataFrame(...)",
                "variable assignment",
                "string literals for style and palette names"
            ],
            "blocked_syntax": [
                "matplotlib.rcParams direct manipulation",
                "sns.set_style()",
                "sns.set_palette()",
                "plt.style.use()",
                "custom theme dictionaries",
                "subplots / multi-panel figures"
            ]
        }
    },
    "grading": {
        "solution_files": [
            {
                "path": "solution.py",
                "content": (
                    "import seaborn as sns\n"
                    "import pandas as pd\n\n"
                    "df = pd.DataFrame({\n"
                    "    'category': ['Lagos', 'Abuja', 'Kano'],\n"
                    "    'value': [24.0, 27.0, 30.0]\n"
                    "})\n\n"
                    "sns.set_theme(style='whitegrid', palette='deep')\n"
                    "sns.barplot(data=df, x='category', y='value')\n"
                )
            }
        ],
        "tests": [
            {
                "test_id": "ix.tile_viz_seaborn_stats_themes.s10.t01",
                "kind": "figure_equals",
                "spec": {
                    "expected": {
                        "n_axes": 1,
                        "chart_types": [["bar"]]
                    }
                },
                "visible": True,
                "message_on_fail": "Your figure should contain one Axes with a bar chart. Call `sns.barplot(data=df, x='category', y='value')`."
            },
            {
                "test_id": "ix.tile_viz_seaborn_stats_themes.s10.t02",
                "kind": "plotted_data_equals",
                "spec": {
                    "chart": "bar",
                    "field": "heights",
                    "expected": [24.0, 27.0, 30.0],
                    "series": 0,
                    "axes": 0
                },
                "visible": True,
                "message_on_fail": "The bar chart should show values [24.0, 27.0, 30.0] for Lagos, Abuja, Kano. Call `sns.barplot(data=df, x='category', y='value')`."
            }
        ]
    },
    "feedback": {
        "correct": {
            "message": "Well done! You called `sns.set_theme()` before the plot, applying the whitegrid style and deep palette to the figure."
        },
        "incorrect": {
            "message": "Make sure you called `sns.set_theme(style='whitegrid', palette='deep')` before `sns.barplot(data=df, x='category', y='value')`."
        },
        "hints": [
            "Call `sns.set_theme(style='whitegrid', palette='deep')` first — it must come before the plot call to take effect.",
            "The two parameters are `style=` (background/gridline style) and `palette=` (color scheme)."
        ]
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# Assemble the output
# ─────────────────────────────────────────────────────────────────────────────

output = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_012_da_viz",
    "tiles": [
        {
            "tile_id": "tile_viz_labeling_chart_selection",
            "interactions": [
                {"step_id": "tile_viz_labeling_chart_selection.s03", "interaction": ix_labeling_s03},
                {"step_id": "tile_viz_labeling_chart_selection.s04", "interaction": ix_labeling_s04},
                {"step_id": "tile_viz_labeling_chart_selection.s05", "interaction": ix_labeling_s05},
                {"step_id": "tile_viz_labeling_chart_selection.s08", "interaction": ix_labeling_s08},
                {"step_id": "tile_viz_labeling_chart_selection.s09", "interaction": ix_labeling_s09},
                {"step_id": "tile_viz_labeling_chart_selection.s10", "interaction": ix_labeling_s10},
            ]
        },
        {
            "tile_id": "tile_viz_custom_multi_panel",
            "interactions": [
                {"step_id": "tile_viz_custom_multi_panel.s02", "interaction": ix_custom_s02},
                {"step_id": "tile_viz_custom_multi_panel.s03", "interaction": ix_custom_s03},
                {"step_id": "tile_viz_custom_multi_panel.s04", "interaction": ix_custom_s04},
                {"step_id": "tile_viz_custom_multi_panel.s07", "interaction": ix_custom_s07},
                {"step_id": "tile_viz_custom_multi_panel.s08", "interaction": ix_custom_s08},
            ]
        },
        {
            "tile_id": "tile_viz_seaborn_stats_themes",
            "interactions": [
                {"step_id": "tile_viz_seaborn_stats_themes.s02", "interaction": ix_seaborn_s02},
                {"step_id": "tile_viz_seaborn_stats_themes.s03", "interaction": ix_seaborn_s03},
                {"step_id": "tile_viz_seaborn_stats_themes.s05", "interaction": ix_seaborn_s05},
                {"step_id": "tile_viz_seaborn_stats_themes.s06", "interaction": ix_seaborn_s06},
                {"step_id": "tile_viz_seaborn_stats_themes.s07", "interaction": ix_seaborn_s07},
                {"step_id": "tile_viz_seaborn_stats_themes.s09", "interaction": ix_seaborn_s09},
                {"step_id": "tile_viz_seaborn_stats_themes.s10", "interaction": ix_seaborn_s10},
            ]
        }
    ]
}

with open('batches/final_batch_012_da_viz/interactions.part.c2.json', 'w') as f:
    json.dump(output, f, indent=2)

print("Written interactions.part.c2.json")
print(f"Tiles: {len(output['tiles'])}")
for t in output['tiles']:
    print(f"  {t['tile_id']}: {len(t['interactions'])} interactions")
