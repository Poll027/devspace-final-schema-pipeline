"""Build screens.part.c0_canary.json for tile_stakeholder_chart_matching_simplifying."""
import json

# ── helpers ──────────────────────────────────────────────────────────────────
def qid(concept_id, local_id):
    """Return qualified id like stakeholder.chart_type_to_point_matching#f1"""
    return f"{concept_id}#{local_id}"

CTPM = "stakeholder.chart_type_to_point_matching"
SCFA = "stakeholder.simplifying_charts_for_audience"

# ── TILE ─────────────────────────────────────────────────────────────────────
tile = {
    "tile_id": "tile_stakeholder_chart_matching_simplifying",
    "title": "Matching and Simplifying Charts for an Audience",
    "summary": (
        "Learn to choose the right chart type for the specific point you are making "
        "to a stakeholder audience, then simplify that chart by removing visual clutter "
        "so the operations manager can focus on the finding, not on reading the graph."
    ),
    "steps": [],
    "remediation_steps": []
}

# ── STEP s01 — explainer: chart type intro + side_by_side visual ─────────────
# side_by_side: left = bar chart (comparison), right = diagram (pie + line labels)
# The plan says side_by_side; the visual_anchor says "comparison" which maps to side_by_side.
# We need left/right to be from the allowed types: data_table, spreadsheet_grid, chart,
# code_walkthrough, diagram, process_flow.
# We'll use chart for bar (left), and a diagram (mapping) for the right panel
# showing pie + line with their points labelled.
# Actually the plan says "bar chart, pie chart, line plot" — three charts.
# side_by_side only has left/right. We'll put bar on left, and a diagram on right
# that shows pie + line as a mapping diagram with callouts.
# Better: use left=chart(bar), right=diagram(mapping) with nodes for pie and line.

s01 = {
    "step_id": "tile_stakeholder_chart_matching_simplifying.s01",
    "type": "explainer",
    "concept_ids": [CTPM],
    "eyebrow": "Chart Type to Point Matching",
    "title": "The chart must match the point, not just the data",
    "lede": (
        "You have the delivery data. The question is: which chart makes your specific "
        "point land for the operations manager?"
    ),
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stakeholder_chart_matching_simplifying.s01.b1",
            "role": "intro",
            "text": (
                "During your own exploration you might have built a bar chart, a line plot, "
                "and a boxplot of the delivery data. Presenting to the operations manager, "
                "the question changes: which one actually makes the Lagos point, for this audience? "
                "The same dataset can support several chart types — the right choice depends on "
                "the specific point you are communicating, not on the data alone."
            ),
            "lineage": {
                "concept_ids": [CTPM],
                "teaching_block_ids": [qid(CTPM, "tb1")],
                "fact_ids": []
            }
        },
        {
            "type": "prose",
            "block_id": "tile_stakeholder_chart_matching_simplifying.s01.b2",
            "role": "mechanism",
            "text": (
                "A bar chart is used for graphing categorical data and comparing values across "
                "categories — showing average delivery time side by side across Lagos, Abuja, and Kano. "
                "A line graph is best when you want to show how the value of something changes over time "
                "— showing Lagos delivery time rising week over week. "
                "Boxplots offer a condensed display for comparing distributions side by side, "
                "but a boxplot may be unfamiliar to many people and could introduce a learning curve; "
                "for a manager who hasn't seen one before, a bar chart or line plot can often make "
                "the point more directly."
            ),
            "lineage": {
                "concept_ids": [CTPM],
                "teaching_block_ids": [qid(CTPM, "tb2")],
                "fact_ids": [
                    qid(CTPM, "f1"),
                    qid(CTPM, "f2"),
                    qid(CTPM, "f3"),
                    qid(CTPM, "f5")
                ]
            }
        },
        {
            # side_by_side visual: left = bar chart (city comparison), right = diagram
            # showing pie (part-to-whole) and line (trend) with their points labelled.
            # We use a diagram (mapping) on the right to show the two remaining chart types
            # with their stakeholder points.
            # Actually the plan says side_by_side with bar, pie, line — but side_by_side
            # only has left/right. We'll put bar on left, and a diagram on right that
            # represents the pie and line as a mapping diagram.
            "type": "side_by_side",
            "block_id": "tile_stakeholder_chart_matching_simplifying.s01.b3",
            "left_label": "Bar chart — compare values across cities",
            "left": {
                "type": "chart",
                "block_id": "tile_stakeholder_chart_matching_simplifying.s01.b3.left",
                "chart_kind": "bar",
                "asset_ref": {
                    "asset_id": "asset_city_deliveries",
                    "variant_id": None,
                    "columns": ["city", "avg_delivery_minutes"]
                },
                "title": "Average Delivery Time by City",
                "alt_text": "Bar chart showing average delivery time in minutes for Lagos (34), Abuja (22), and Kano (19), illustrating a city-vs-city comparison.",
                "encoding": {
                    "x": {"field": "city", "type": "nominal", "title": "City"},
                    "y": {"field": "avg_delivery_minutes", "type": "quantitative", "title": "Avg Delivery Time (min)"}
                }
            },
            "right_label": "Line graph — show Lagos trend over weeks",
            "right": {
                "type": "chart",
                "block_id": "tile_stakeholder_chart_matching_simplifying.s01.b3.right",
                "chart_kind": "line",
                "asset_ref": {
                    "asset_id": "asset_lagos_weekly_deliveries",
                    "variant_id": None,
                    "columns": ["week_label", "avg_delivery_minutes"]
                },
                "title": "Lagos Average Delivery Time — Week over Week",
                "alt_text": "Line graph showing Lagos average delivery time rising from 28 min in Wk 1 to 38 min in Wk 8, illustrating a week-over-week trend.",
                "encoding": {
                    "x": {"field": "week_label", "type": "ordinal", "title": "Week"},
                    "y": {"field": "avg_delivery_minutes", "type": "quantitative", "title": "Avg Delivery Time (min)"}
                }
            },
            "takeaway": (
                "The same delivery data supports both charts — the bar chart makes a comparison point "
                "(which city is slowest?), the line graph makes a trend point (is Lagos getting slower?). "
                "Choose the chart that matches the point you are making."
            ),
            "lineage": {
                "concept_ids": [CTPM],
                "teaching_block_ids": [qid(CTPM, "tb1"), qid(CTPM, "tb2")],
                "fact_ids": [qid(CTPM, "f1"), qid(CTPM, "f2")],
                "anchors": [qid(CTPM, "visual")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [CTPM],
        "teaching_block_ids": [qid(CTPM, "tb1"), qid(CTPM, "tb2")],
        "fact_ids": [
            qid(CTPM, "f1"),
            qid(CTPM, "f2"),
            qid(CTPM, "f3"),
            qid(CTPM, "f5")
        ],
        "anchors": [qid(CTPM, "visual")]
    }
}
tile["steps"].append(s01)

# ── STEP s02 — video ──────────────────────────────────────────────────────────
s02 = {
    "step_id": "tile_stakeholder_chart_matching_simplifying.s02",
    "type": "video",
    "concept_ids": [CTPM],
    "eyebrow": "Chart Type to Point Matching",
    "title": "Why the chart type must match the point you are making",
    "lede": "Watch how the same data looks different depending on chart type, and notice when a chart makes comparison easy versus hard.",
    "blocks": [
        {
            "type": "media_group",
            "block_id": "tile_stakeholder_chart_matching_simplifying.s02.b1",
            "group_title": "Why the chart type must match the point you are making",
            "segment_ids": [
                "seg_stakeholder.chart_type_to_point_matching_RiEZ_hEf96A_0_101",
                "seg_stakeholder.chart_type_to_point_matching_Z77c53eYtHc_149_201"
            ]
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [CTPM],
        "teaching_block_ids": [],
        "fact_ids": [
            qid(CTPM, "f1"),
            qid(CTPM, "f3"),
            qid(CTPM, "f5")
        ],
        "segment_ids": [
            "seg_stakeholder.chart_type_to_point_matching_RiEZ_hEf96A_0_101",
            "seg_stakeholder.chart_type_to_point_matching_Z77c53eYtHc_149_201"
        ]
    }
}
tile["steps"].append(s02)

# ── STEP s03 — explainer: pie chart, scatterplot, misconception ───────────────
s03 = {
    "step_id": "tile_stakeholder_chart_matching_simplifying.s03",
    "type": "explainer",
    "concept_ids": [CTPM],
    "eyebrow": "Chart Type to Point Matching",
    "title": "Pie charts, scatterplots, and the comparison trap",
    "lede": (
        "Two more chart types complete the toolkit — and one common misconception "
        "about pie charts is worth clearing up."
    ),
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stakeholder_chart_matching_simplifying.s03.b1",
            "role": "practical_context",
            "text": (
                "A pie chart expresses a part-to-whole relationship in the data. It is best used "
                "either for a general sense of how parts relate to the whole, or to highlight that "
                "one segment is notably larger or smaller than the others. The pie must depict a "
                "meaningful whole — values that sum to 100%. If the point is 'Lagos accounts for "
                "most of our total delivery volume,' a pie chart of each city's share of total orders "
                "fits that part-to-whole framing in a way a bar chart of averages would not."
            ),
            "lineage": {
                "concept_ids": [CTPM],
                "teaching_block_ids": [qid(CTPM, "tb3")],
                "fact_ids": [qid(CTPM, "f4")]
            }
        },
        {
            "type": "prose",
            "block_id": "tile_stakeholder_chart_matching_simplifying.s03.b2",
            "role": "practical_context",
            "text": (
                "A scatterplot is often used to understand data rather than to communicate with it, "
                "though it can still be designed to convey findings to an audience. Keep this in mind "
                "if the distance/delivery-time relationship ever needs to go in front of the manager "
                "directly, rather than staying an exploratory chart."
            ),
            "lineage": {
                "concept_ids": [CTPM],
                "teaching_block_ids": [qid(CTPM, "tb4")],
                "fact_ids": [qid(CTPM, "f6")]
            }
        },
        {
            "type": "prose",
            "block_id": "tile_stakeholder_chart_matching_simplifying.s03.b3",
            "role": "misconception",
            "text": (
                "It can look like comparing pie slices is just as easy as comparing bar lengths, "
                "since both show a value at a glance — but it is not. A bar chart's aligned, common "
                "baseline makes length differences easy to judge; two pie slices of similar size are "
                "harder to rank correctly by eye."
            ),
            "lineage": {
                "concept_ids": [CTPM],
                "teaching_block_ids": [qid(CTPM, "tb5")],
                "fact_ids": [qid(CTPM, "m1")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [CTPM],
        "teaching_block_ids": [
            qid(CTPM, "tb3"),
            qid(CTPM, "tb4"),
            qid(CTPM, "tb5")
        ],
        "fact_ids": [
            qid(CTPM, "f4"),
            qid(CTPM, "f6"),
            qid(CTPM, "m1")
        ]
    }
}
tile["steps"].append(s03)

# ── STEP s04 — check (framing only) ──────────────────────────────────────────
s04 = {
    "step_id": "tile_stakeholder_chart_matching_simplifying.s04",
    "type": "check",
    "concept_ids": [CTPM],
    "eyebrow": "Quick Check",
    "title": "Scatterplot: exploratory or communicative?",
    "lede": "Test your understanding of when a scatterplot is the right choice for a stakeholder audience.",
    "reward": {"gems": 10, "first_try_bonus": 5},
    "lineage": {
        "concept_ids": [CTPM],
        "teaching_block_ids": [],
        "fact_ids": [qid(CTPM, "f6")],
        "anchors": [qid(CTPM, "assessment:classify_scatterplot_as_exploratory_vs_communicative")]
    }
}
tile["steps"].append(s04)

# ── STEP s05 — hands_on (framing only) ───────────────────────────────────────
s05 = {
    "step_id": "tile_stakeholder_chart_matching_simplifying.s05",
    "type": "hands_on",
    "concept_ids": [CTPM],
    "eyebrow": "Practice",
    "title": "Match the chart to the stakeholder point",
    "lede": (
        "Given a stakeholder point about the delivery data, choose the chart type that "
        "best communicates it and explain why."
    ),
    "reward": {"gems": 15, "first_try_bonus": 5},
    "lineage": {
        "concept_ids": [CTPM],
        "teaching_block_ids": [],
        "fact_ids": [
            qid(CTPM, "f1"),
            qid(CTPM, "f2"),
            qid(CTPM, "f3"),
            qid(CTPM, "f4"),
            qid(CTPM, "f5"),
            qid(CTPM, "f6"),
            qid(CTPM, "m1")
        ],
        "anchors": [
            qid(CTPM, "practice"),
            qid(CTPM, "assessment:select_chart_type_for_stakeholder_point"),
            qid(CTPM, "assessment:distinguish_part_to_whole_from_comparison_framing"),
            qid(CTPM, "assessment:evaluate_audience_readiness_for_boxplot")
        ]
    }
}
tile["steps"].append(s05)

# ── STEP s06 — explainer: simplifying charts + before_after visual ────────────
s06 = {
    "step_id": "tile_stakeholder_chart_matching_simplifying.s06",
    "type": "explainer",
    "concept_ids": [SCFA],
    "eyebrow": "Simplifying Charts for an Audience",
    "title": "Remove the clutter — not the data",
    "lede": (
        "A chart built for your own exploration carries elements the operations manager "
        "doesn't need. Each removal reduces reading effort without changing the numbers."
    ),
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stakeholder_chart_matching_simplifying.s06.b1",
            "role": "intro",
            "text": (
                "A bar chart of city delivery times built during your own exploration can carry "
                "gridlines, a border, and precise decimal labels that help you double-check the numbers. "
                "The operations manager probably doesn't need any of that to get the point. "
                "Gridlines can be deleted from a chart; if precise values matter to the audience, "
                "label the data point directly instead of relying on gridlines."
            ),
            "lineage": {
                "concept_ids": [SCFA],
                "teaching_block_ids": [qid(SCFA, "tb1"), qid(SCFA, "tb2")],
                "fact_ids": [qid(SCFA, "f1")]
            }
        },
        {
            "type": "prose",
            "block_id": "tile_stakeholder_chart_matching_simplifying.s06.b2",
            "role": "mechanism",
            "text": (
                "A chart's border can be removed, since it is not adding informative value; "
                "white space can differentiate parts of a visual better than a border. "
                "Data labels should be used sparingly, only where the exact values are important "
                "to the audience; otherwise remove them and use the axis instead. "
                "Unnecessary trailing zeroes can be dropped from axis labels — '22.00 minutes' "
                "can become '22 min'. Diagonally rotated axis text is slower to read; "
                "city-name tick labels like Lagos, Abuja, and Kano don't need to be rotated at all."
            ),
            "lineage": {
                "concept_ids": [SCFA],
                "teaching_block_ids": [qid(SCFA, "tb2"), qid(SCFA, "tb3")],
                "fact_ids": [
                    qid(SCFA, "f2"),
                    qid(SCFA, "f3"),
                    qid(SCFA, "f5"),
                    qid(SCFA, "f6")
                ]
            }
        },
        {
            "type": "before_after",
            "block_id": "tile_stakeholder_chart_matching_simplifying.s06.b3",
            "before": {
                "type": "diagram",
                "block_id": "tile_stakeholder_chart_matching_simplifying.s06.b3.before",
                "diagram_kind": "container",
                "title": "Before: cluttered bar chart",
                "nodes": [
                    {"id": "border_box", "label": "Chart border (box around entire chart)", "kind": "clutter"},
                    {"id": "gridlines", "label": "Horizontal gridlines behind bars", "kind": "clutter"},
                    {"id": "decimal_labels", "label": "Y-axis: 34.00, 22.00, 19.00 (trailing zeros)", "kind": "clutter"},
                    {"id": "rotated_labels", "label": "X-axis city names rotated 45°", "kind": "clutter"},
                    {"id": "data_labels_all", "label": "Data label on every bar (34.00, 22.00, 19.00)", "kind": "clutter"},
                    {"id": "bars", "label": "Bars: Lagos 34 min, Abuja 22 min, Kano 19 min", "kind": "data"}
                ],
                "alt_text": "Diagram representing a cluttered bar chart with a border, gridlines, decimal axis labels, rotated city-name tick labels, and data labels on every bar."
            },
            "after": {
                "type": "diagram",
                "block_id": "tile_stakeholder_chart_matching_simplifying.s06.b3.after",
                "diagram_kind": "container",
                "title": "After: simplified bar chart",
                "nodes": [
                    {"id": "bars_clean", "label": "Bars: Lagos 34 min, Abuja 22 min, Kano 19 min", "kind": "data"},
                    {"id": "axis_clean", "label": "Y-axis: 0, 10, 20, 30, 40 (no trailing zeros)", "kind": "data"},
                    {"id": "labels_clean", "label": "X-axis: Lagos, Abuja, Kano (horizontal, no rotation)", "kind": "data"},
                    {"id": "whitespace", "label": "White space separates chart from surrounding content", "kind": "design"}
                ],
                "alt_text": "Diagram representing a simplified bar chart with no border, no gridlines, clean axis labels without trailing zeros, horizontal city-name tick labels, and no per-bar data labels."
            },
            "change_summary": (
                "Border removed — white space does the job of separation. "
                "Gridlines removed — the axis scale is sufficient. "
                "Trailing zeros dropped from axis labels (34.00 → 34). "
                "City-name tick labels un-rotated — short names read fine horizontally. "
                "Per-bar data labels removed — the axis gives approximate values. "
                "None of these changes alter the underlying delivery-time numbers."
            ),
            "lineage": {
                "concept_ids": [SCFA],
                "teaching_block_ids": [qid(SCFA, "tb2"), qid(SCFA, "tb3")],
                "fact_ids": [
                    qid(SCFA, "f1"),
                    qid(SCFA, "f2"),
                    qid(SCFA, "f3"),
                    qid(SCFA, "f5"),
                    qid(SCFA, "f6")
                ],
                "anchors": [qid(SCFA, "visual")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [SCFA],
        "teaching_block_ids": [
            qid(SCFA, "tb1"),
            qid(SCFA, "tb2"),
            qid(SCFA, "tb3")
        ],
        "fact_ids": [
            qid(SCFA, "f1"),
            qid(SCFA, "f2"),
            qid(SCFA, "f3"),
            qid(SCFA, "f5"),
            qid(SCFA, "f6")
        ],
        "anchors": [qid(SCFA, "visual")]
    }
}
tile["steps"].append(s06)

# ── STEP s07 — video ──────────────────────────────────────────────────────────
s07 = {
    "step_id": "tile_stakeholder_chart_matching_simplifying.s07",
    "type": "video",
    "concept_ids": [SCFA],
    "eyebrow": "Simplifying Charts for an Audience",
    "title": "Decluttering a chart for a non-technical audience",
    "lede": "Watch how each removal reduces reading effort. The same design principles apply in any charting tool.",
    "blocks": [
        {
            "type": "media_group",
            "block_id": "tile_stakeholder_chart_matching_simplifying.s07.b1",
            "group_title": "Decluttering a chart for a non-technical audience",
            "segment_ids": [
                "seg_stakeholder.simplifying_charts_for_audience_XgY1-BsZSzM_51_393"
            ]
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [SCFA],
        "teaching_block_ids": [],
        "fact_ids": [
            qid(SCFA, "f2"),
            qid(SCFA, "f3"),
            qid(SCFA, "f4"),
            qid(SCFA, "f5"),
            qid(SCFA, "f6")
        ],
        "segment_ids": [
            "seg_stakeholder.simplifying_charts_for_audience_XgY1-BsZSzM_51_393"
        ]
    }
}
tile["steps"].append(s07)

# ── STEP s08 — check (framing only) ──────────────────────────────────────────
s08 = {
    "step_id": "tile_stakeholder_chart_matching_simplifying.s08",
    "type": "check",
    "concept_ids": [SCFA],
    "eyebrow": "Quick Check",
    "title": "Which elements reduce clutter?",
    "lede": "Identify the chart elements that should be removed to simplify a chart for a non-technical audience.",
    "reward": {"gems": 10, "first_try_bonus": 5},
    "lineage": {
        "concept_ids": [SCFA],
        "teaching_block_ids": [],
        "fact_ids": [
            qid(SCFA, "f1"),
            qid(SCFA, "f2"),
            qid(SCFA, "f3"),
            qid(SCFA, "f4"),
            qid(SCFA, "f5"),
            qid(SCFA, "f6")
        ],
        "anchors": [
            qid(SCFA, "assessment:identify_clutter_elements_to_remove"),
            qid(SCFA, "assessment:explain_cognitive_benefit_of_reducing_chart_clutter")
        ]
    }
}
tile["steps"].append(s08)

# ── STEP s09 — check (framing only) ──────────────────────────────────────────
s09 = {
    "step_id": "tile_stakeholder_chart_matching_simplifying.s09",
    "type": "check",
    "concept_ids": [SCFA],
    "eyebrow": "Quick Check",
    "title": "Why remove the border?",
    "lede": "Explain why removing a chart border improves readability for a non-technical audience.",
    "reward": {"gems": 10, "first_try_bonus": 5},
    "lineage": {
        "concept_ids": [SCFA],
        "teaching_block_ids": [],
        "fact_ids": [qid(SCFA, "f2")],
        "anchors": [qid(SCFA, "assessment:justify_border_removal_using_white_space")]
    }
}
tile["steps"].append(s09)

# ── STEP s10 — hands_on (framing only) ───────────────────────────────────────
s10 = {
    "step_id": "tile_stakeholder_chart_matching_simplifying.s10",
    "type": "hands_on",
    "concept_ids": [SCFA],
    "eyebrow": "Practice",
    "title": "Simplify a chart for the operations manager",
    "lede": (
        "Given a bar chart with a border, gridlines, trailing-zero axis labels, rotated "
        "city-name tick labels, and data labels on every bar — simplify it for a non-technical "
        "operations manager."
    ),
    "reward": {"gems": 15, "first_try_bonus": 5},
    "lineage": {
        "concept_ids": [SCFA],
        "teaching_block_ids": [],
        "fact_ids": [
            qid(SCFA, "f1"),
            qid(SCFA, "f3"),
            qid(SCFA, "f5"),
            qid(SCFA, "f6")
        ],
        "anchors": [
            qid(SCFA, "practice"),
            qid(SCFA, "assessment:choose_between_data_labels_and_axis_for_precision"),
            qid(SCFA, "assessment:simplify_axis_labels_for_readability")
        ]
    }
}
tile["steps"].append(s10)

# ── STEP s11 — recap ──────────────────────────────────────────────────────────
s11 = {
    "step_id": "tile_stakeholder_chart_matching_simplifying.s11",
    "type": "recap",
    "concept_ids": [CTPM, SCFA],
    "eyebrow": "Recap",
    "title": "What you've learned",
    "lede": "Two skills that work together: matching the chart to the point, then clearing the noise.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stakeholder_chart_matching_simplifying.s11.b1",
            "role": "takeaway",
            "text": (
                "Reducing clutter lets the audience use their attention to decide what actions "
                "might be warranted, rather than working out how to read the graph. "
                "None of these changes alter the underlying delivery-time numbers — only how much "
                "visual effort it takes to read them. "
                "Match the chart to the point; then strip everything that doesn't serve that point."
            ),
            "lineage": {
                "concept_ids": [CTPM, SCFA],
                "teaching_block_ids": [qid(SCFA, "tb4")],
                "fact_ids": [qid(SCFA, "f4")]
            }
        },
        {
            "type": "up_next",
            "block_id": "tile_stakeholder_chart_matching_simplifying.s11.b2",
            "title": "Up next: Structuring a Stakeholder Presentation",
            "text": (
                "Now that your charts are matched to their points and stripped of clutter, "
                "the next tile covers how to structure the full presentation — "
                "opening with the finding, not the method."
            )
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [CTPM, SCFA],
        "teaching_block_ids": [qid(SCFA, "tb4")],
        "fact_ids": [qid(SCFA, "f4")]
    }
}
tile["steps"].append(s11)

# ── REMEDIATION STEPS ─────────────────────────────────────────────────────────
# Rule 7: first check/hands_on of each concept gets a remediation step.
# Concept 1 (CTPM): first check = s04 (measures f6), first hands_on = s05 (measures f1-f6,m1)
# s04 measures f6 only; s05 measures f1-f6,m1 — different facts → two remediation steps.
# Concept 2 (SCFA): first check = s08 (measures f1-f6), s09 (measures f2), first hands_on = s10
# s08 and s09 measure different facts → two remediation steps.

# r01: remediation for s04 (f6 — scatterplot exploratory vs communicative)
r01 = {
    "step_id": "tile_stakeholder_chart_matching_simplifying.r01",
    "type": "remediation",
    "concept_ids": [CTPM],
    "eyebrow": "Let's revisit",
    "title": "Scatterplots: exploratory by default, communicative by design",
    "lede": "A scatterplot is a powerful tool for your own analysis — but it needs extra design work to communicate findings to an audience.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stakeholder_chart_matching_simplifying.r01.b1",
            "role": "practical_context",
            "text": (
                "A scatterplot is often used to understand data rather than to communicate with it. "
                "When you plot distance_km against delivery_minutes for orders across Lagos, Abuja, "
                "and Kano, you are exploring a relationship — that is the scatterplot's strength. "
                "It can still be designed to convey findings to an audience, but that requires "
                "deliberate choices: a clear title stating the finding, colour coding by city, "
                "and a trend line if the relationship is the point. "
                "Without those additions, a scatterplot of 15 order records is harder for the "
                "operations manager to read than a bar chart or line graph."
            ),
            "lineage": {
                "concept_ids": [CTPM],
                "teaching_block_ids": [qid(CTPM, "tb4")],
                "fact_ids": [qid(CTPM, "f6")]
            }
        }
    ],
    "lineage": {
        "concept_ids": [CTPM],
        "teaching_block_ids": [qid(CTPM, "tb4")],
        "fact_ids": [qid(CTPM, "f6")]
    }
}
tile["remediation_steps"].append(r01)

# r02: remediation for s05 (f1-f6, m1 — full chart matching)
r02 = {
    "step_id": "tile_stakeholder_chart_matching_simplifying.r02",
    "type": "remediation",
    "concept_ids": [CTPM],
    "eyebrow": "Let's revisit",
    "title": "Matching chart type to the point: a quick contrast",
    "lede": "The same delivery data can be shown as a bar chart, line graph, pie chart, or scatterplot — the right choice depends entirely on the point you are making.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stakeholder_chart_matching_simplifying.r02.b1",
            "role": "mechanism",
            "text": (
                "Bar chart: comparing values across categories — which city has the longest average "
                "delivery time? Use it when the point is a side-by-side comparison (Lagos 34 min, "
                "Abuja 22 min, Kano 19 min). "
                "Line graph: showing change over time — is Lagos delivery time rising week over week? "
                "Pie chart: part-to-whole — does Lagos account for most of total orders? "
                "The pie must sum to 100%. "
                "Boxplot: comparing distributions side by side — but may be unfamiliar to a "
                "non-technical audience, so a bar chart or line plot often makes the point more directly. "
                "Scatterplot: exploring a relationship — distance vs. delivery time — but needs "
                "extra design work to communicate findings clearly."
            ),
            "lineage": {
                "concept_ids": [CTPM],
                "teaching_block_ids": [qid(CTPM, "tb2"), qid(CTPM, "tb3"), qid(CTPM, "tb4")],
                "fact_ids": [
                    qid(CTPM, "f1"),
                    qid(CTPM, "f2"),
                    qid(CTPM, "f3"),
                    qid(CTPM, "f4"),
                    qid(CTPM, "f5"),
                    qid(CTPM, "f6")
                ]
            }
        },
        {
            "type": "prose",
            "block_id": "tile_stakeholder_chart_matching_simplifying.r02.b2",
            "role": "misconception",
            "text": (
                "It can look like comparing pie slices is just as easy as comparing bar lengths — "
                "but it is not. A bar chart's aligned, common baseline makes length differences easy "
                "to judge; two pie slices of similar size are harder to rank correctly by eye. "
                "Use a pie chart only when the part-to-whole relationship is the point, not when "
                "precise comparison between categories is needed."
            ),
            "lineage": {
                "concept_ids": [CTPM],
                "teaching_block_ids": [qid(CTPM, "tb5")],
                "fact_ids": [qid(CTPM, "m1")]
            }
        }
    ],
    "lineage": {
        "concept_ids": [CTPM],
        "teaching_block_ids": [
            qid(CTPM, "tb2"),
            qid(CTPM, "tb3"),
            qid(CTPM, "tb4"),
            qid(CTPM, "tb5")
        ],
        "fact_ids": [
            qid(CTPM, "f1"),
            qid(CTPM, "f2"),
            qid(CTPM, "f3"),
            qid(CTPM, "f4"),
            qid(CTPM, "f5"),
            qid(CTPM, "f6"),
            qid(CTPM, "m1")
        ]
    }
}
tile["remediation_steps"].append(r02)

# r03: remediation for s08 (f1-f6 — clutter elements + cognitive benefit)
r03 = {
    "step_id": "tile_stakeholder_chart_matching_simplifying.r03",
    "type": "remediation",
    "concept_ids": [SCFA],
    "eyebrow": "Let's revisit",
    "title": "What counts as clutter — and why removing it helps",
    "lede": "Each element you remove from a chart reduces the cognitive effort the audience spends reading it.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stakeholder_chart_matching_simplifying.r03.b1",
            "role": "mechanism",
            "text": (
                "Gridlines can be deleted; if precise values matter, label the data point directly "
                "instead. A chart's border can be removed — white space differentiates parts of a "
                "visual better than a border. Data labels should be used sparingly, only where exact "
                "values are important; otherwise use the axis. Unnecessary trailing zeroes can be "
                "dropped from axis labels. Diagonally rotated axis text is slower to read — "
                "abbreviate labels so they render horizontally."
            ),
            "lineage": {
                "concept_ids": [SCFA],
                "teaching_block_ids": [qid(SCFA, "tb2"), qid(SCFA, "tb3")],
                "fact_ids": [
                    qid(SCFA, "f1"),
                    qid(SCFA, "f2"),
                    qid(SCFA, "f3"),
                    qid(SCFA, "f5"),
                    qid(SCFA, "f6")
                ]
            }
        },
        {
            "type": "prose",
            "block_id": "tile_stakeholder_chart_matching_simplifying.r03.b2",
            "role": "takeaway",
            "text": (
                "Reducing clutter lets the audience use their attention to decide what actions "
                "might be warranted, rather than working out how to read the graph. "
                "None of these removals change the underlying delivery-time numbers."
            ),
            "lineage": {
                "concept_ids": [SCFA],
                "teaching_block_ids": [qid(SCFA, "tb4")],
                "fact_ids": [qid(SCFA, "f4")]
            }
        }
    ],
    "lineage": {
        "concept_ids": [SCFA],
        "teaching_block_ids": [qid(SCFA, "tb2"), qid(SCFA, "tb3"), qid(SCFA, "tb4")],
        "fact_ids": [
            qid(SCFA, "f1"),
            qid(SCFA, "f2"),
            qid(SCFA, "f3"),
            qid(SCFA, "f4"),
            qid(SCFA, "f5"),
            qid(SCFA, "f6")
        ]
    }
}
tile["remediation_steps"].append(r03)

# r04: remediation for s09 (f2 — border removal / white space)
r04 = {
    "step_id": "tile_stakeholder_chart_matching_simplifying.r04",
    "type": "remediation",
    "concept_ids": [SCFA],
    "eyebrow": "Let's revisit",
    "title": "Border vs. white space: why the border can go",
    "lede": "A chart border feels like it organises the visual — but white space does that job better.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stakeholder_chart_matching_simplifying.r04.b1",
            "role": "mechanism",
            "text": (
                "A chart's border is not adding informative value — it does not encode any data "
                "and does not help the audience read the bars. White space around the chart "
                "differentiates it from surrounding content just as effectively, without adding "
                "a visual element the eye has to process. Removing the border is one of the "
                "quickest single changes that reduces clutter on a chart built for a non-technical "
                "audience like the operations manager."
            ),
            "lineage": {
                "concept_ids": [SCFA],
                "teaching_block_ids": [qid(SCFA, "tb2")],
                "fact_ids": [qid(SCFA, "f2")]
            }
        }
    ],
    "lineage": {
        "concept_ids": [SCFA],
        "teaching_block_ids": [qid(SCFA, "tb2")],
        "fact_ids": [qid(SCFA, "f2")]
    }
}
tile["remediation_steps"].append(r04)

# ── ASSEMBLE OUTPUT ───────────────────────────────────────────────────────────
output = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_013_da_stakeholder_chart",
    "tiles": [tile]
}

out_path = "batches/final_batch_013_da_stakeholder_chart/screens.part.c0_canary.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"Written: {out_path}")
print(f"Steps: {len(tile['steps'])}")
print(f"Remediation steps: {len(tile['remediation_steps'])}")
for s in tile["steps"]:
    print(f"  {s['step_id']} ({s['type']})")
for r in tile["remediation_steps"]:
    print(f"  {r['step_id']} ({r['type']})")
