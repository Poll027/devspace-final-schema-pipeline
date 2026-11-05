"""Build interactions.part.c0_canary.json for tile_stakeholder_chart_matching_simplifying."""
import json

TILE = "tile_stakeholder_chart_matching_simplifying"
C1 = "stakeholder.chart_type_to_point_matching"
C2 = "stakeholder.simplifying_charts_for_audience"

# ── s04: check / choice ──────────────────────────────────────────────────────
# Tests f6: scatterplot is exploratory by default, can be communicative by design.
# Taught in s03 (tb4). Anchor: classify_scatterplot_as_exploratory_vs_communicative
# Remediation: r01 (first check for this concept that covers f6 specifically)
s04 = {
    "step_id": f"{TILE}.s04",
    "interaction": {
        "type": "choice",
        "interaction_id": f"ix.{TILE}.s04",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": C1,
                "capability": "classify_scatterplot_as_exploratory_vs_communicative",
                "fact_ids": ["f6"]
            }
        ],
        "anchors": [
            f"{C1}#assessment:classify_scatterplot_as_exploratory_vs_communicative"
        ],
        "public": {
            "prompt": "A data analyst plots distance_km against delivery_minutes for all orders across Lagos, Abuja, and Kano. Which statement best describes how a scatterplot is typically used?",
            "options": [
                {
                    "option_id": "opt_a",
                    "text": "A scatterplot is primarily used to understand data during exploration, though it can be designed to communicate findings to an audience."
                },
                {
                    "option_id": "opt_b",
                    "text": "A scatterplot is the clearest chart for communicating findings to a non-technical audience because it shows every individual data point."
                },
                {
                    "option_id": "opt_c",
                    "text": "A scatterplot cannot be used to communicate findings to an audience under any circumstances."
                },
                {
                    "option_id": "opt_d",
                    "text": "A scatterplot is best used to show how a value changes over time."
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {
                    "message": "Correct. A scatterplot is often used to understand data rather than to communicate with it, but it can still be designed to convey findings to an audience."
                },
                "opt_b": {
                    "message": "Incorrect. Showing every individual data point makes a scatterplot harder, not easier, for a non-technical audience to read without extra design work such as a clear title, colour coding, and a trend line."
                },
                "opt_c": {
                    "message": "Incorrect. A scatterplot can be designed to communicate findings to an audience — it just requires deliberate choices such as a clear title and colour coding. The default is exploratory, not the only use."
                },
                "opt_d": {
                    "message": "Incorrect. Showing change over time is the strength of a line graph, not a scatterplot. A scatterplot shows the relationship between two numerical variables."
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "Right. Scatterplots are exploratory by default — they reveal relationships in your own analysis. With deliberate design choices they can communicate findings to an audience, but that extra work is required."
            },
            "incorrect": {
                "message": "A scatterplot is often used to understand data rather than to communicate with it, though it can still be designed to convey findings to an audience."
            },
            "hints": [
                "Think about who typically reads a scatterplot — the analyst building it, or the manager receiving the report?",
                "The fact says 'often used to understand data' — does that mean it can never communicate?"
            ],
            "remediation_step_id": f"{TILE}.r01"
        }
    }
}

# ── s05: hands_on / classify ─────────────────────────────────────────────────
# Practice anchor: matching type — "Given the stakeholder point 'this category dominates the total',
# choose one chart type from {bar chart, line graph, boxplot, pie chart, scatterplot}..."
# Success: learner selects pie chart (or bar chart showing share), invokes part-to-whole requirement.
# Plan says classify. Buckets: chart types. Items: stakeholder points → classify which chart fits.
# Tests f1-f6, m1. Anchors: practice + select_chart_type_for_stakeholder_point +
#   distinguish_part_to_whole_from_comparison_framing + evaluate_audience_readiness_for_boxplot
s05 = {
    "step_id": f"{TILE}.s05",
    "interaction": {
        "type": "classify",
        "interaction_id": f"ix.{TILE}.s05",
        "difficulty": "stretch",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": C1,
                "capability": "select_chart_type_for_stakeholder_point",
                "fact_ids": ["f1", "f2", "f3", "f4", "f5", "f6"]
            },
            {
                "concept_id": C1,
                "capability": "distinguish_part_to_whole_from_comparison_framing",
                "fact_ids": ["f4", "m1"]
            },
            {
                "concept_id": C1,
                "capability": "evaluate_audience_readiness_for_boxplot",
                "fact_ids": ["f3", "f5"]
            }
        ],
        "anchors": [
            f"{C1}#practice",
            f"{C1}#assessment:select_chart_type_for_stakeholder_point",
            f"{C1}#assessment:distinguish_part_to_whole_from_comparison_framing",
            f"{C1}#assessment:evaluate_audience_readiness_for_boxplot"
        ],
        "public": {
            "prompt": "The operations manager needs three separate charts for three different points. Drag each stakeholder point into the bucket for the chart type that best communicates it.",
            "buckets": [
                {"bucket_id": "bucket_bar", "label": "Bar chart"},
                {"bucket_id": "bucket_line", "label": "Line graph"},
                {"bucket_id": "bucket_pie", "label": "Pie chart"},
                {"bucket_id": "bucket_boxplot", "label": "Boxplot — avoid with this audience"},
                {"bucket_id": "bucket_scatter", "label": "Scatterplot — exploratory, needs design work"}
            ],
            "items": [
                {
                    "item_id": "item_comparison",
                    "text": "\"Lagos has the longest average delivery time compared with Abuja and Kano.\""
                },
                {
                    "item_id": "item_trend",
                    "text": "\"Lagos average delivery time has been rising week over week for the past eight weeks.\""
                },
                {
                    "item_id": "item_part_whole",
                    "text": "\"Lagos accounts for most of our total delivery volume across all three cities.\""
                },
                {
                    "item_id": "item_distribution",
                    "text": "\"The spread of individual delivery times differs across cities — some cities have much more variation than others.\""
                },
                {
                    "item_id": "item_relationship",
                    "text": "\"There may be a relationship between distance from the depot and delivery time.\""
                }
            ]
        },
        "grading": {
            "assignments": {
                "item_comparison": "bucket_bar",
                "item_trend": "bucket_line",
                "item_part_whole": "bucket_pie",
                "item_distribution": "bucket_boxplot",
                "item_relationship": "bucket_scatter"
            },
            "item_feedback": {
                "item_comparison": {
                    "message": "A bar chart is used for graphing categorical data and comparing values across categories — perfect for a side-by-side city comparison."
                },
                "item_trend": {
                    "message": "Line graphs are best when you want to show how the value of something changes over time, making the week-over-week rise in Lagos immediately visible."
                },
                "item_part_whole": {
                    "message": "A pie chart expresses a part-to-whole relationship — Lagos's share of total orders sums to 100% with the other cities, making this the right framing."
                },
                "item_distribution": {
                    "message": "Boxplots offer a condensed display for comparing distributions side by side, but may be unfamiliar to many people and could introduce a learning curve — flag this for a non-technical audience."
                },
                "item_relationship": {
                    "message": "A scatterplot is often used to understand data rather than to communicate with it. It can convey the distance/delivery-time relationship, but requires deliberate design choices for a non-technical audience."
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "Well done. Each chart type matches the specific point: bar for comparison, line for trend, pie for part-to-whole, boxplot for distribution (with an audience caveat), and scatterplot for relationships (exploratory by default)."
            },
            "incorrect": {
                "message": "The chart type must match the specific point being made. Bar = comparison across categories; line = change over time; pie = part-to-whole (must sum to 100%); boxplot = distributions (risky with non-technical audiences); scatterplot = relationships (exploratory by default)."
            },
            "hints": [
                "Ask yourself: is the point about comparing categories, showing change over time, or showing how parts add up to a whole?",
                "For the distribution item, think about whether the operations manager has seen a boxplot before."
            ],
            "remediation_step_id": f"{TILE}.r02"
        }
    }
}

# ── s08: check / choice ──────────────────────────────────────────────────────
# Tests simplifying f1, f2, f3, f5, f6 (taught in s06 tb1-tb3).
# NOTE: f4 is only taught in s11 (recap, tb4) — cannot test f4 here.
# Anchor: identify_clutter_elements_to_remove (fact_ids: f1,f2,f3,f5,f6)
# The explain_cognitive_benefit_of_reducing_chart_clutter anchor (fact_ids: [f4]) is
# excluded from measures here because f4 has not been taught by text before s08.
# Remediation: r03 (first check for simplifying concept)
s08 = {
    "step_id": f"{TILE}.s08",
    "interaction": {
        "type": "choice",
        "interaction_id": f"ix.{TILE}.s08",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": C2,
                "capability": "identify_clutter_elements_to_remove",
                "fact_ids": ["f1", "f2", "f3", "f5", "f6"]
            }
        ],
        "anchors": [
            f"{C2}#assessment:identify_clutter_elements_to_remove",
            f"{C2}#assessment:explain_cognitive_benefit_of_reducing_chart_clutter"
        ],
        "public": {
            "prompt": "An analyst has a bar chart with a visible border, gridlines, decimal axis labels (e.g. '34.00'), diagonally rotated city-name tick labels, and a data label on every bar. The operations manager does not need exact values. Which set of changes best simplifies this chart?",
            "options": [
                {
                    "option_id": "opt_a",
                    "text": "Remove the border, gridlines, and data labels; drop trailing zeros from axis labels; display city-name tick labels horizontally."
                },
                {
                    "option_id": "opt_b",
                    "text": "Remove only the gridlines, because they are the main source of visual noise; keep the border, decimal labels, and data labels to maintain precision."
                },
                {
                    "option_id": "opt_c",
                    "text": "Keep all elements — removing any of them risks losing information the audience needs to understand the chart."
                },
                {
                    "option_id": "opt_d",
                    "text": "Remove the data labels and replace them with a table below the chart so the audience can look up exact values."
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {
                    "message": "Correct. Removing the border, gridlines, trailing zeros, diagonal labels, and unnecessary data labels reduces the visual effort the audience must spend before they can act on the finding."
                },
                "opt_b": {
                    "message": "Incorrect. Gridlines are one source of clutter, but the border, decimal trailing zeros, and diagonal tick labels also add visual effort without adding informative value. Data labels should be removed when exact values are not critical."
                },
                "opt_c": {
                    "message": "Incorrect. None of these removals change the underlying data. The border adds no informative value; white space differentiates the chart better. Trailing zeros and diagonal labels slow reading."
                },
                "opt_d": {
                    "message": "Incorrect. Adding a separate table increases the total visual effort. Since the manager does not need exact values, removing data labels and keeping the axis is the simpler solution."
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "Exactly right. Each removal — border, gridlines, trailing zeros, diagonal labels, excess data labels — reduces the visual effort the audience must spend before they can act on the finding."
            },
            "incorrect": {
                "message": "Focus on what each element adds for the audience. The border adds no informative value; white space does the job better. Trailing zeros and diagonal labels slow reading. Data labels are only needed when exact values are critical."
            },
            "hints": [
                "Which elements encode data, and which are just visual decoration?",
                "If the manager does not need exact values, do data labels help or add clutter?"
            ],
            "remediation_step_id": f"{TILE}.r03"
        }
    }
}

# ── s09: check / choice ──────────────────────────────────────────────────────
# Tests simplifying f2: border removal / white space.
# Anchor: justify_border_removal_using_white_space
# Taught in s06 (tb2). Remediation: r04 (first check for this specific fact)
s09 = {
    "step_id": f"{TILE}.s09",
    "interaction": {
        "type": "choice",
        "interaction_id": f"ix.{TILE}.s09",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": C2,
                "capability": "justify_border_removal_using_white_space",
                "fact_ids": ["f2"]
            }
        ],
        "anchors": [
            f"{C2}#assessment:justify_border_removal_using_white_space"
        ],
        "public": {
            "prompt": "Why can a chart's border be removed without losing anything important?",
            "options": [
                {
                    "option_id": "opt_a",
                    "text": "White space can differentiate parts of a visual better than a border, and the border is not adding informative value."
                },
                {
                    "option_id": "opt_b",
                    "text": "The border should only be removed if the chart has no gridlines, because one of the two is needed to frame the chart."
                },
                {
                    "option_id": "opt_c",
                    "text": "Borders are only decorative in pie charts; bar charts need a border to separate the bars from the background."
                },
                {
                    "option_id": "opt_d",
                    "text": "Removing the border makes the chart smaller, which saves space on the slide."
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_a"],
            "option_feedback": {
                "opt_a": {
                    "message": "Correct. A chart's border is not adding informative value; white space can differentiate parts of a visual better than a border."
                },
                "opt_b": {
                    "message": "Incorrect. Neither a border nor gridlines are required to frame a chart. White space alone differentiates the chart from surrounding content."
                },
                "opt_c": {
                    "message": "Incorrect. The principle applies to all chart types: a border is not adding informative value regardless of chart type, and white space does the job of separation better."
                },
                "opt_d": {
                    "message": "Incorrect. Removing a border does not change the chart's dimensions. The reason to remove it is that it adds no informative value, not that it saves space."
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "Right. The border encodes no data and adds no informative value. White space around the chart separates it from surrounding content just as effectively."
            },
            "incorrect": {
                "message": "A chart's border can be removed because it is not adding informative value; white space can differentiate parts of a visual better than a border."
            },
            "hints": [
                "Does the border tell the audience anything about the delivery data?",
                "What does white space do that a border also does?"
            ],
            "remediation_step_id": f"{TILE}.r04"
        }
    }
}

# ── s10: hands_on / classify ─────────────────────────────────────────────────
# Practice anchor: UI_edit type, but plan says classify.
# Success: chart has no border, no gridlines, axis labels without trailing zeros,
#   horizontal city-name tick labels, no per-bar data labels.
# Tests f1, f3, f5, f6. Anchors: practice + choose_between_data_labels_and_axis_for_precision
#   + simplify_axis_labels_for_readability
# Taught in s06 (tb1, tb2, tb3).
s10 = {
    "step_id": f"{TILE}.s10",
    "interaction": {
        "type": "classify",
        "interaction_id": f"ix.{TILE}.s10",
        "difficulty": "stretch",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": C2,
                "capability": "choose_between_data_labels_and_axis_for_precision",
                "fact_ids": ["f1", "f3"]
            },
            {
                "concept_id": C2,
                "capability": "simplify_axis_labels_for_readability",
                "fact_ids": ["f5", "f6"]
            }
        ],
        "anchors": [
            f"{C2}#practice",
            f"{C2}#assessment:choose_between_data_labels_and_axis_for_precision",
            f"{C2}#assessment:simplify_axis_labels_for_readability"
        ],
        "public": {
            "prompt": "The operations manager's bar chart currently has these elements. Classify each one: should it be kept as-is, removed, or changed? (The manager does not need exact delivery-time values.)",
            "buckets": [
                {"bucket_id": "bucket_remove", "label": "Remove"},
                {"bucket_id": "bucket_change", "label": "Change (abbreviate / simplify)"},
                {"bucket_id": "bucket_keep", "label": "Keep as-is"}
            ],
            "items": [
                {
                    "item_id": "item_gridlines",
                    "text": "Gridlines across the chart area"
                },
                {
                    "item_id": "item_data_labels",
                    "text": "Data labels showing '34.00 min', '22.00 min', '19.00 min' on every bar"
                },
                {
                    "item_id": "item_axis_labels",
                    "text": "Y-axis labels showing '10.00', '20.00', '30.00', '40.00'"
                },
                {
                    "item_id": "item_tick_labels",
                    "text": "City-name tick labels 'Lagos', 'Abuja', 'Kano' displayed diagonally at 45°"
                },
                {
                    "item_id": "item_bars",
                    "text": "The bars themselves (the encoded delivery-time data)"
                }
            ]
        },
        "grading": {
            "assignments": {
                "item_gridlines": "bucket_remove",
                "item_data_labels": "bucket_remove",
                "item_axis_labels": "bucket_change",
                "item_tick_labels": "bucket_change",
                "item_bars": "bucket_keep"
            },
            "item_feedback": {
                "item_gridlines": {
                    "message": "Gridlines can be deleted from a chart. If precise values matter, label the data point directly instead — but here the manager does not need exact values, so the axis alone is sufficient."
                },
                "item_data_labels": {
                    "message": "Data labels should be used sparingly, only where exact values are important to the audience. Since the manager does not need exact values, remove the data labels and rely on the axis."
                },
                "item_axis_labels": {
                    "message": "Unnecessary trailing zeros can be dropped — '10.00' becomes '10' or '10 min'. This reduces visual noise without changing the data."
                },
                "item_tick_labels": {
                    "message": "Diagonally rotated axis text is slower to read. Labels can be abbreviated so they render horizontally — 'Lagos', 'Abuja', and 'Kano' are short enough to display horizontally without overlap."
                },
                "item_bars": {
                    "message": "The bars encode the delivery-time data — they are the point of the chart and must be kept."
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "Correct. Remove gridlines and unnecessary data labels; drop trailing zeros from axis labels; display city-name tick labels horizontally. The bars stay — they are the data."
            },
            "incorrect": {
                "message": "Focus on what each element adds for the audience. Gridlines and excess data labels add visual effort without adding value. Trailing zeros and diagonal labels slow reading. The bars are the data and must stay."
            },
            "hints": [
                "Which elements encode the delivery-time data, and which are just formatting?",
                "If the manager does not need exact values, do data labels help or add clutter?"
            ],
            "remediation_step_id": f"{TILE}.r03"
        }
    }
}

# ── Assemble ──────────────────────────────────────────────────────────────────
output = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_013_da_stakeholder_chart",
    "tiles": [
        {
            "tile_id": TILE,
            "interactions": [s04, s05, s08, s09, s10]
        }
    ]
}

with open("batches/final_batch_013_da_stakeholder_chart/interactions.part.c0_canary.json", "w") as f:
    json.dump(output, f, indent=2)

print("Written interactions.part.c0_canary.json")
print(f"Interactions: {len(output['tiles'][0]['interactions'])}")
for ix in output['tiles'][0]['interactions']:
    print(f"  {ix['step_id']} -> {ix['interaction']['type']}")
