"""Build interactions.part.c0_canary.json for tile_viz_figures_layout_plotting."""
import json

CHART_RENDERER_VERSION = "0.29.5"

interactions = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_012_da_viz",
    "tiles": [
        {
            "tile_id": "tile_viz_figures_layout_plotting",
            "interactions": [
                # ── s04: check ── map_plotting_task_to_correct_object ──────────────
                {
                    "step_id": "tile_viz_figures_layout_plotting.s04",
                    "interaction": {
                        "type": "choice",
                        "interaction_id": "ix.tile_viz_figures_layout_plotting.s04",
                        "difficulty": "intro",
                        "grading_mode": "client",
                        "standalone": False,
                        "measures": [
                            {
                                "concept_id": "viz.matplotlib_figure_axes",
                                "capability": "map_plotting_task_to_correct_object",
                                "fact_ids": [
                                    "viz.matplotlib_figure_axes#f1",
                                    "viz.matplotlib_figure_axes#f2",
                                    "viz.matplotlib_figure_axes#f3"
                                ]
                            }
                        ],
                        "anchors": [
                            "viz.matplotlib_figure_axes#assessment:map_plotting_task_to_correct_object"
                        ],
                        "public": {
                            "prompt": "After running `fig, ax = plt.subplots()`, you want to draw a line of QuickDeliver delivery times. Which object do you call `.plot()` on?",
                            "options": [
                                {
                                    "option_id": "opt_ax",
                                    "text": "`ax` — the Axes object"
                                },
                                {
                                    "option_id": "opt_fig",
                                    "text": "`fig` — the Figure object"
                                },
                                {
                                    "option_id": "opt_plt",
                                    "text": "`plt` — the pyplot module directly"
                                },
                                {
                                    "option_id": "opt_either",
                                    "text": "Either `fig` or `ax` — they both hold the same data"
                                }
                            ],
                            "selection": "single",
                            "shuffle": True
                        },
                        "grading": {
                            "correct_option_ids": ["opt_ax"],
                            "option_feedback": {
                                "opt_ax": {
                                    "message": "Correct. Plotting calls such as `ax.plot(x, y)` draw onto the Axes object — the rectangle with its own x- and y-axis where data is actually rendered."
                                },
                                "opt_fig": {
                                    "message": "Not quite. The Figure is the overall canvas — it holds the Axes but never receives plotted data directly. Plotting calls go on `ax`, not `fig`."
                                },
                                "opt_plt": {
                                    "message": "Not quite. `plt.plot()` is a different function from `ax.plot()`. When you have an explicit `ax` variable from `plt.subplots()`, you call `ax.plot()` to draw onto that specific Axes."
                                },
                                "opt_either": {
                                    "message": "Not quite. Only the Axes (`ax`) receives plotted data. The Figure (`fig`) is the canvas that contains the Axes — it does not hold data itself."
                                }
                            }
                        },
                        "feedback": {
                            "correct": {
                                "message": "Exactly right. The Axes is the plotting area — all drawing calls go on `ax`."
                            },
                            "incorrect": {
                                "message": "Remember: `fig, ax = plt.subplots()` gives you two objects. The Figure (`fig`) is the canvas; the Axes (`ax`) is where data is drawn. Plotting calls go on `ax`."
                            },
                            "hints": [
                                "Think about which object is described as 'the rectangle with its own x- and y-axis where data is drawn'.",
                                "`plt.subplots()` returns two values — the first is the canvas, the second is the plotting area."
                            ],
                            "remediation_step_id": "tile_viz_figures_layout_plotting.s01"
                        }
                    }
                },

                # ── s05: hands_on ── code_exercise (chart_renderer) ─────────────
                {
                    "step_id": "tile_viz_figures_layout_plotting.s05",
                    "interaction": {
                        "type": "code_exercise",
                        "interaction_id": "ix.tile_viz_figures_layout_plotting.s05",
                        "difficulty": "intro",
                        "grading_mode": "client",
                        "standalone": False,
                        "measures": [
                            {
                                "concept_id": "viz.matplotlib_figure_axes",
                                "capability": "identify_figure_vs_axes_roles",
                                "fact_ids": ["viz.matplotlib_figure_axes#f1"]
                            },
                            {
                                "concept_id": "viz.matplotlib_figure_axes",
                                "capability": "recognise_subplots_creates_figure_and_axes",
                                "fact_ids": ["viz.matplotlib_figure_axes#f2"]
                            },
                            {
                                "concept_id": "viz.matplotlib_figure_axes",
                                "capability": "identify_axes_as_target_of_plot_calls",
                                "fact_ids": ["viz.matplotlib_figure_axes#f3"]
                            }
                        ],
                        "anchors": [
                            "viz.matplotlib_figure_axes#practice",
                            "viz.matplotlib_figure_axes#assessment:identify_figure_vs_axes_roles",
                            "viz.matplotlib_figure_axes#assessment:recognise_subplots_creates_figure_and_axes",
                            "viz.matplotlib_figure_axes#assessment:identify_axes_as_target_of_plot_calls"
                        ],
                        "public": {
                            "prompt": (
                                "The lists `days` and `delivery_times` are already defined. "
                                "Complete the two steps below:\n\n"
                                "1. Call `plt.subplots()` and assign the result to `fig` and `ax`.\n"
                                "2. Call `ax.plot(days, delivery_times)` to draw the delivery times onto the Axes.\n\n"
                                "The figure should contain exactly one Axes with one line whose x-values are `days` (1–5) "
                                "and y-values are `delivery_times` (18, 22, 26, 19, 30)."
                            ),
                            "runtime": {
                                "kind": "chart_renderer",
                                "version": CHART_RENDERER_VERSION,
                                "packages": ["pandas", "matplotlib"]
                            },
                            "workspace": {
                                "files": [
                                    {
                                        "path": "solution.py",
                                        "role": "editable",
                                        "language": "python",
                                        "content": (
                                            "import matplotlib.pyplot as plt\n"
                                            "\n"
                                            "days = [1, 2, 3, 4, 5]\n"
                                            "delivery_times = [18, 22, 26, 19, 30]\n"
                                            "\n"
                                            "# Step 1: create a Figure and one Axes using plt.subplots()\n"
                                            "# fig, ax = ...\n"
                                            "\n"
                                            "# Step 2: draw delivery_times against days on the Axes\n"
                                            "# ax.plot(...)\n"
                                        )
                                    }
                                ],
                                "entry": "solution.py"
                            },
                            "constraints": {
                                "allowed_syntax": [
                                    "import matplotlib.pyplot as plt",
                                    "fig, ax = plt.subplots()",
                                    "ax.plot(x, y)"
                                ],
                                "blocked_syntax": [
                                    "plt.plot()",
                                    "plt.figure()",
                                    "plt.figsize",
                                    "figsize=",
                                    "tight_layout()",
                                    "ax.set_title()",
                                    "ax.set_xlabel()",
                                    "ax.set_ylabel()",
                                    "plt.legend()",
                                    "plt.show()",
                                    "plt.bar()",
                                    "plt.hist()",
                                    "plt.scatter()",
                                    "plt.boxplot()",
                                    "sns."
                                ]
                            }
                        },
                        "grading": {
                            "solution_files": [
                                {
                                    "path": "solution.py",
                                    "content": (
                                        "import matplotlib.pyplot as plt\n"
                                        "\n"
                                        "days = [1, 2, 3, 4, 5]\n"
                                        "delivery_times = [18, 22, 26, 19, 30]\n"
                                        "\n"
                                        "fig, ax = plt.subplots()\n"
                                        "ax.plot(days, delivery_times)\n"
                                    )
                                }
                            ],
                            "tests": [
                                {
                                    "test_id": "ix.tile_viz_figures_layout_plotting.s05.t01",
                                    "kind": "figure_equals",
                                    "spec": {
                                        "expected": {
                                            "n_axes": 1,
                                            "chart_types": [["line"]]
                                        }
                                    },
                                    "visible": True,
                                    "message_on_fail": "Your figure should contain exactly one Axes with one line. Make sure you called `fig, ax = plt.subplots()` and then `ax.plot(days, delivery_times)`."
                                },
                                {
                                    "test_id": "ix.tile_viz_figures_layout_plotting.s05.t02",
                                    "kind": "plotted_data_equals",
                                    "spec": {
                                        "chart": "line",
                                        "field": "x",
                                        "expected": [1, 2, 3, 4, 5],
                                        "series": 0,
                                        "axes": 0
                                    },
                                    "visible": True,
                                    "message_on_fail": "The x-values of the line should be `days` (1, 2, 3, 4, 5). Pass `days` as the first argument to `ax.plot()`."
                                },
                                {
                                    "test_id": "ix.tile_viz_figures_layout_plotting.s05.t03",
                                    "kind": "plotted_data_equals",
                                    "spec": {
                                        "chart": "line",
                                        "field": "y",
                                        "expected": [18, 22, 26, 19, 30],
                                        "series": 0,
                                        "axes": 0
                                    },
                                    "visible": True,
                                    "message_on_fail": "The y-values of the line should be `delivery_times` (18, 22, 26, 19, 30). Pass `delivery_times` as the second argument to `ax.plot()`."
                                }
                            ]
                        },
                        "feedback": {
                            "correct": {
                                "message": "Well done! You created a Figure and an Axes with `plt.subplots()` and drew the delivery times onto the Axes with `ax.plot(days, delivery_times)`."
                            },
                            "incorrect": {
                                "message": "Check that you called `fig, ax = plt.subplots()` first, then `ax.plot(days, delivery_times)`. The data must be drawn on `ax`, not on `fig`."
                            },
                            "hints": [
                                "`plt.subplots()` returns two values — assign them as `fig, ax = plt.subplots()`.",
                                "Once you have `ax`, call `ax.plot(days, delivery_times)` — the first argument is x, the second is y."
                            ],
                            "remediation_step_id": "tile_viz_figures_layout_plotting.s01"
                        }
                    }
                },

                # ── s07: check ── apply_tight_layout_to_fit_subplots ────────────
                {
                    "step_id": "tile_viz_figures_layout_plotting.s07",
                    "interaction": {
                        "type": "choice",
                        "interaction_id": "ix.tile_viz_figures_layout_plotting.s07",
                        "difficulty": "core",
                        "grading_mode": "client",
                        "standalone": False,
                        "measures": [
                            {
                                "concept_id": "viz.figure_size_layout",
                                "capability": "apply_tight_layout_to_fit_subplots",
                                "fact_ids": [
                                    "viz.figure_size_layout#f2",
                                    "viz.figure_size_layout#f3"
                                ]
                            }
                        ],
                        "anchors": [
                            "viz.figure_size_layout#assessment:apply_tight_layout_to_fit_subplots"
                        ],
                        "public": {
                            "prompt": "You have created a figure with `fig, ax = plt.subplots(figsize=(8, 4))`. Which of the following correctly calls `tight_layout` to adjust the subplot spacing?",
                            "options": [
                                {
                                    "option_id": "opt_fig_tight",
                                    "text": "`fig.tight_layout()`"
                                },
                                {
                                    "option_id": "opt_plt_tight",
                                    "text": "`plt.tight_layout()`"
                                },
                                {
                                    "option_id": "opt_both",
                                    "text": "Both `fig.tight_layout()` and `plt.tight_layout()` are correct"
                                },
                                {
                                    "option_id": "opt_ax_tight",
                                    "text": "`ax.tight_layout()`"
                                }
                            ],
                            "selection": "single",
                            "shuffle": True
                        },
                        "grading": {
                            "correct_option_ids": ["opt_both"],
                            "option_feedback": {
                                "opt_fig_tight": {
                                    "message": "This is one correct form, but not the only one. `tight_layout()` can also be called as `plt.tight_layout()` — both forms adjust the subplot spacing."
                                },
                                "opt_plt_tight": {
                                    "message": "This is one correct form, but not the only one. `tight_layout()` can also be called as `fig.tight_layout()` — both forms adjust the subplot spacing."
                                },
                                "opt_both": {
                                    "message": "Correct. `tight_layout()` can be called as `plt.tight_layout()` or `fig.tight_layout()` — both automatically adjust subplot parameters so the subplot fits into the figure area."
                                },
                                "opt_ax_tight": {
                                    "message": "Incorrect. `tight_layout()` is a Figure-level method, not an Axes method. Call it as `fig.tight_layout()` or `plt.tight_layout()`, not on `ax`."
                                }
                            }
                        },
                        "feedback": {
                            "correct": {
                                "message": "Right! `tight_layout()` can be called on the figure object (`fig.tight_layout()`) or via pyplot (`plt.tight_layout()`) — both work."
                            },
                            "incorrect": {
                                "message": "`tight_layout()` is a Figure-level operation. It can be called as `fig.tight_layout()` or `plt.tight_layout()` — both adjust subplot spacing automatically."
                            },
                            "hints": [
                                "The fact says `tight_layout()` can be called in two ways — one uses the `fig` variable, the other uses `plt` directly.",
                                "`tight_layout()` is not a method on the Axes (`ax`) — it operates on the Figure."
                            ],
                            "remediation_step_id": "tile_viz_figures_layout_plotting.s06"
                        }
                    }
                },

                # ── s08: hands_on ── code_exercise (chart_renderer) ─────────────
                {
                    "step_id": "tile_viz_figures_layout_plotting.s08",
                    "interaction": {
                        "type": "code_exercise",
                        "interaction_id": "ix.tile_viz_figures_layout_plotting.s08",
                        "difficulty": "core",
                        "grading_mode": "client",
                        "standalone": False,
                        "measures": [
                            {
                                "concept_id": "viz.figure_size_layout",
                                "capability": "set_figure_size_with_figsize",
                                "fact_ids": ["viz.figure_size_layout#f1"]
                            },
                            {
                                "concept_id": "viz.figure_size_layout",
                                "capability": "apply_tight_layout_to_fit_subplots",
                                "fact_ids": [
                                    "viz.figure_size_layout#f2",
                                    "viz.figure_size_layout#f3"
                                ]
                            }
                        ],
                        "anchors": [
                            "viz.figure_size_layout#practice",
                            "viz.figure_size_layout#assessment:set_figure_size_with_figsize",
                            "viz.figure_size_layout#assessment:apply_tight_layout_to_fit_subplots"
                        ],
                        "public": {
                            "prompt": (
                                "Create a figure that is **10 inches wide and 5 inches tall**, then call `tight_layout` on it.\n\n"
                                "Steps:\n"
                                "1. Call `plt.subplots(figsize=(10, 5))` and assign the result to `fig` and `ax`.\n"
                                "2. Call `fig.tight_layout()` to adjust the subplot spacing.\n\n"
                                "After running, `fig.get_size_inches()` should return `[10.0, 5.0]`."
                            ),
                            "runtime": {
                                "kind": "chart_renderer",
                                "version": CHART_RENDERER_VERSION,
                                "packages": ["pandas", "matplotlib"]
                            },
                            "workspace": {
                                "files": [
                                    {
                                        "path": "solution.py",
                                        "role": "editable",
                                        "language": "python",
                                        "content": (
                                            "import matplotlib.pyplot as plt\n"
                                            "\n"
                                            "# Step 1: create a figure 10 inches wide and 5 inches tall\n"
                                            "# fig, ax = plt.subplots(figsize=(...))\n"
                                            "\n"
                                            "# Step 2: call tight_layout on the figure\n"
                                            "# fig.tight_layout()\n"
                                        )
                                    }
                                ],
                                "entry": "solution.py"
                            },
                            "constraints": {
                                "allowed_syntax": [
                                    "plt.subplots(figsize=(width, height))",
                                    "fig.tight_layout()",
                                    "plt.tight_layout()",
                                    "tuple literals for figsize",
                                    "variable assignment (fig, ax = ...)"
                                ],
                                "blocked_syntax": [
                                    "plt.plot()",
                                    "ax.plot()",
                                    "ax.bar()",
                                    "ax.hist()",
                                    "ax.set_xlabel()",
                                    "ax.set_ylabel()",
                                    "ax.set_title()",
                                    "ax.legend()",
                                    "plt.show()",
                                    "seaborn",
                                    "plt.subplots(nrows, ncols) with more than one subplot"
                                ]
                            }
                        },
                        "grading": {
                            "solution_files": [
                                {
                                    "path": "solution.py",
                                    "content": (
                                        "import matplotlib.pyplot as plt\n"
                                        "\n"
                                        "fig, ax = plt.subplots(figsize=(10, 5))\n"
                                        "fig.tight_layout()\n"
                                    )
                                }
                            ],
                            "tests": [
                                {
                                    "test_id": "ix.tile_viz_figures_layout_plotting.s08.t01",
                                    "kind": "figure_equals",
                                    "spec": {
                                        "expected": {
                                            "n_axes": 1
                                        }
                                    },
                                    "visible": True,
                                    "message_on_fail": "Your code should create exactly one figure with one Axes. Use `fig, ax = plt.subplots(figsize=(10, 5))`."
                                },
                                {
                                    "test_id": "ix.tile_viz_figures_layout_plotting.s08.t02",
                                    "kind": "value_equals",
                                    "spec": {
                                        "expr": "list(fig.get_size_inches())",
                                        "expected": [10.0, 5.0]
                                    },
                                    "visible": True,
                                    "message_on_fail": "The figure size should be (10, 5) inches. Pass `figsize=(10, 5)` to `plt.subplots()`."
                                }
                            ]
                        },
                        "feedback": {
                            "correct": {
                                "message": "Well done! You created a 10×5-inch figure with `plt.subplots(figsize=(10, 5))` and called `fig.tight_layout()` to fit the layout."
                            },
                            "incorrect": {
                                "message": "Make sure you pass `figsize=(10, 5)` to `plt.subplots()` and then call `fig.tight_layout()` (or `plt.tight_layout()`) on the result."
                            },
                            "hints": [
                                "`figsize` takes a (width, height) tuple in inches — `figsize=(10, 5)` means 10 inches wide, 5 inches tall.",
                                "After creating the figure, call `fig.tight_layout()` — this adjusts the subplot spacing automatically."
                            ],
                            "remediation_step_id": "tile_viz_figures_layout_plotting.s06"
                        }
                    }
                },

                # ── s11: check ── distinguish_one_arg_from_two_arg_pyplot_call ──
                {
                    "step_id": "tile_viz_figures_layout_plotting.s11",
                    "interaction": {
                        "type": "choice",
                        "interaction_id": "ix.tile_viz_figures_layout_plotting.s11",
                        "difficulty": "core",
                        "grading_mode": "client",
                        "standalone": False,
                        "measures": [
                            {
                                "concept_id": "viz.pyplot_basic_plotting",
                                "capability": "distinguish_one_arg_from_two_arg_pyplot_call",
                                "fact_ids": [
                                    "viz.pyplot_basic_plotting#f1",
                                    "viz.pyplot_basic_plotting#f2"
                                ]
                            }
                        ],
                        "anchors": [
                            "viz.pyplot_basic_plotting#assessment:distinguish_one_arg_from_two_arg_pyplot_call"
                        ],
                        "public": {
                            "prompt": "You call `plt.plot([18, 22, 26, 19, 30])` with a single list argument. What x-values does matplotlib use for the plot?",
                            "options": [
                                {
                                    "option_id": "opt_auto_0",
                                    "text": "Automatic positions starting from 0: 0, 1, 2, 3, 4"
                                },
                                {
                                    "option_id": "opt_auto_1",
                                    "text": "Automatic positions starting from 1: 1, 2, 3, 4, 5"
                                },
                                {
                                    "option_id": "opt_values",
                                    "text": "The y-values themselves: 18, 22, 26, 19, 30"
                                },
                                {
                                    "option_id": "opt_none",
                                    "text": "No x-axis is drawn — a single argument produces a bar chart instead"
                                }
                            ],
                            "selection": "single",
                            "shuffle": True
                        },
                        "grading": {
                            "correct_option_ids": ["opt_auto_0"],
                            "option_feedback": {
                                "opt_auto_0": {
                                    "message": "Correct. `plt.plot(y)` with a single argument treats the list as y-values and automatically generates x-positions starting from 0 (0, 1, 2, 3, 4 for five values)."
                                },
                                "opt_auto_1": {
                                    "message": "Not quite. The automatic x-positions start from 0, not 1. For five y-values, matplotlib uses x = 0, 1, 2, 3, 4."
                                },
                                "opt_values": {
                                    "message": "Not quite. The single argument is treated as y-values, not x-values. Matplotlib generates its own x-positions starting from 0."
                                },
                                "opt_none": {
                                    "message": "Not quite. `plt.plot()` always draws a line chart. With a single argument it uses the list as y-values and auto-generates x-positions from 0."
                                }
                            }
                        },
                        "feedback": {
                            "correct": {
                                "message": "Exactly right. `plt.plot(y)` auto-generates x-positions starting at 0 — so five values get x = 0, 1, 2, 3, 4."
                            },
                            "incorrect": {
                                "message": "`plt.plot(y)` treats its single argument as y-values and fills in x-positions automatically starting from 0. To supply your own x-values, use `plt.plot(x, y)` with two arguments."
                            },
                            "hints": [
                                "The fact says: `plt.plot(y)` 'automatically generates the x-values starting from 0'.",
                                "Think about what index position the first element of a Python list has."
                            ],
                            "remediation_step_id": "tile_viz_figures_layout_plotting.s09"
                        }
                    }
                },

                # ── s12: hands_on ── code_exercise (chart_renderer) ─────────────
                {
                    "step_id": "tile_viz_figures_layout_plotting.s12",
                    "interaction": {
                        "type": "code_exercise",
                        "interaction_id": "ix.tile_viz_figures_layout_plotting.s12",
                        "difficulty": "stretch",
                        "grading_mode": "client",
                        "standalone": False,
                        "measures": [
                            {
                                "concept_id": "viz.pyplot_basic_plotting",
                                "capability": "identify_single_arg_plot_auto_x_behavior",
                                "fact_ids": ["viz.pyplot_basic_plotting#f1"]
                            },
                            {
                                "concept_id": "viz.pyplot_basic_plotting",
                                "capability": "produce_two_arg_plot_with_explicit_x_values",
                                "fact_ids": ["viz.pyplot_basic_plotting#f2"]
                            },
                            {
                                "concept_id": "viz.pyplot_basic_plotting",
                                "capability": "distinguish_one_arg_from_two_arg_pyplot_call",
                                "fact_ids": [
                                    "viz.pyplot_basic_plotting#f1",
                                    "viz.pyplot_basic_plotting#f2"
                                ]
                            }
                        ],
                        "anchors": [
                            "viz.pyplot_basic_plotting#practice",
                            "viz.pyplot_basic_plotting#assessment:identify_single_arg_plot_auto_x_behavior",
                            "viz.pyplot_basic_plotting#assessment:produce_two_arg_plot_with_explicit_x_values",
                            "viz.pyplot_basic_plotting#assessment:distinguish_one_arg_from_two_arg_pyplot_call"
                        ],
                        "public": {
                            "prompt": (
                                "The lists `delivery_times` and `days` are already defined. "
                                "Make **two** `plt.plot()` calls in the order shown:\n\n"
                                "1. **One-argument form**: call `plt.plot(delivery_times)` — matplotlib will auto-generate x-positions 0, 1, 2, 3, 4.\n"
                                "2. **Two-argument form**: call `plt.plot(days, delivery_times)` — matplotlib will use `days` (1–5) as the x-values.\n\n"
                                "Both calls draw onto the same axes. The final figure should have one Axes containing "
                                "two lines: the first line has x-values 0–4, the second has x-values 1–5."
                            ),
                            "runtime": {
                                "kind": "chart_renderer",
                                "version": CHART_RENDERER_VERSION,
                                "packages": ["pandas", "matplotlib"]
                            },
                            "workspace": {
                                "files": [
                                    {
                                        "path": "solution.py",
                                        "role": "editable",
                                        "language": "python",
                                        "content": (
                                            "import matplotlib.pyplot as plt\n"
                                            "\n"
                                            "delivery_times = [18, 22, 26, 19, 30]\n"
                                            "days = [1, 2, 3, 4, 5]\n"
                                            "\n"
                                            "# Call 1: one-argument form (auto x-positions from 0)\n"
                                            "# plt.plot(...)\n"
                                            "\n"
                                            "# Call 2: two-argument form (explicit x-values from days)\n"
                                            "# plt.plot(..., ...)\n"
                                        )
                                    }
                                ],
                                "entry": "solution.py"
                            },
                            "constraints": {
                                "allowed_syntax": [
                                    "import matplotlib.pyplot as plt",
                                    "plt.plot(y_list)",
                                    "plt.plot(x_list, y_list)"
                                ],
                                "blocked_syntax": [
                                    "plt.bar()",
                                    "plt.hist()",
                                    "plt.scatter()",
                                    "plt.boxplot()",
                                    "ax.plot()",
                                    "plt.xlabel()",
                                    "plt.ylabel()",
                                    "plt.title()",
                                    "plt.legend()",
                                    "import seaborn",
                                    "import numpy"
                                ]
                            }
                        },
                        "grading": {
                            "solution_files": [
                                {
                                    "path": "solution.py",
                                    "content": (
                                        "import matplotlib.pyplot as plt\n"
                                        "\n"
                                        "delivery_times = [18, 22, 26, 19, 30]\n"
                                        "days = [1, 2, 3, 4, 5]\n"
                                        "\n"
                                        "plt.plot(delivery_times)\n"
                                        "plt.plot(days, delivery_times)\n"
                                    )
                                }
                            ],
                            "tests": [
                                {
                                    "test_id": "ix.tile_viz_figures_layout_plotting.s12.t01",
                                    "kind": "figure_equals",
                                    "spec": {
                                        "expected": {
                                            "n_axes": 1,
                                            "chart_types": [["line", "line"]]
                                        }
                                    },
                                    "visible": True,
                                    "message_on_fail": "The figure should have one Axes with two lines. Make sure you made both `plt.plot()` calls."
                                },
                                {
                                    "test_id": "ix.tile_viz_figures_layout_plotting.s12.t02",
                                    "kind": "plotted_data_equals",
                                    "spec": {
                                        "chart": "line",
                                        "field": "x",
                                        "expected": [0, 1, 2, 3, 4],
                                        "series": 0,
                                        "axes": 0
                                    },
                                    "visible": True,
                                    "message_on_fail": "The first line should have auto-generated x-positions 0, 1, 2, 3, 4. Use `plt.plot(delivery_times)` with only one argument."
                                },
                                {
                                    "test_id": "ix.tile_viz_figures_layout_plotting.s12.t03",
                                    "kind": "plotted_data_equals",
                                    "spec": {
                                        "chart": "line",
                                        "field": "x",
                                        "expected": [1, 2, 3, 4, 5],
                                        "series": 1,
                                        "axes": 0
                                    },
                                    "visible": True,
                                    "message_on_fail": "The second line should have x-values from `days` (1, 2, 3, 4, 5). Use `plt.plot(days, delivery_times)` with two arguments."
                                },
                                {
                                    "test_id": "ix.tile_viz_figures_layout_plotting.s12.t04",
                                    "kind": "plotted_data_equals",
                                    "spec": {
                                        "chart": "line",
                                        "field": "y",
                                        "expected": [18, 22, 26, 19, 30],
                                        "series": 0,
                                        "axes": 0
                                    },
                                    "visible": False,
                                    "message_on_fail": "The y-values of the first line should be `delivery_times` (18, 22, 26, 19, 30)."
                                },
                                {
                                    "test_id": "ix.tile_viz_figures_layout_plotting.s12.t05",
                                    "kind": "plotted_data_equals",
                                    "spec": {
                                        "chart": "line",
                                        "field": "y",
                                        "expected": [18, 22, 26, 19, 30],
                                        "series": 1,
                                        "axes": 0
                                    },
                                    "visible": False,
                                    "message_on_fail": "The y-values of the second line should be `delivery_times` (18, 22, 26, 19, 30)."
                                }
                            ]
                        },
                        "feedback": {
                            "correct": {
                                "message": "Excellent! You used both forms: `plt.plot(delivery_times)` auto-numbered the x-axis from 0, and `plt.plot(days, delivery_times)` used your supplied day numbers."
                            },
                            "incorrect": {
                                "message": "Make sure you made exactly two `plt.plot()` calls: first `plt.plot(delivery_times)` (one argument, auto x from 0), then `plt.plot(days, delivery_times)` (two arguments, explicit x)."
                            },
                            "hints": [
                                "The one-argument form is `plt.plot(delivery_times)` — pass only the y-values list.",
                                "The two-argument form is `plt.plot(days, delivery_times)` — x-values first, y-values second."
                            ],
                            "remediation_step_id": "tile_viz_figures_layout_plotting.s09"
                        }
                    }
                }
            ]
        }
    ]
}

output_path = "batches/final_batch_012_da_viz/interactions.part.c0_canary.json"
with open(output_path, "w") as f:
    json.dump(interactions, f, indent=2)
print(f"Written {output_path}")
print(f"Interactions count: {len(interactions['tiles'][0]['interactions'])}")
