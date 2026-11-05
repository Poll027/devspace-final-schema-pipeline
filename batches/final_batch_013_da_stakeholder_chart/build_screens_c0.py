"""Build screens.part.c0_canary.json for tile_stakeholder_chart_matching_simplifying."""
import json

TILE_ID = "tile_stakeholder_chart_matching_simplifying"
C1 = "stakeholder.chart_type_to_point_matching"
C2 = "stakeholder.simplifying_charts_for_audience"

# ── helpers ──────────────────────────────────────────────────────────────────
def qid(concept, fid):
    return f"{concept}#{fid}"

def tb(concept, n):
    return f"{concept}#tb{n}"

def anchor(concept, suffix):
    return f"{concept}#{suffix}"

# ── STEP s01: explainer — chart type intro + side_by_side visual ─────────────
s01 = {
    "step_id": f"{TILE_ID}.s01",
    "type": "explainer",
    "concept_ids": [C1],
    "eyebrow": "Chart Type Matching",
    "title": "The chart you pick should match the point you are making",
    "lede": "The same delivery data can be shown as a bar chart, a pie chart, or a line plot — but only one will make your specific point land for the operations manager.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{TILE_ID}.s01.b1",
            "role": "intro",
            "text": (
                "During your own exploration you might have built several charts of SwiftMove Nigeria's delivery data. "
                "Presenting to the operations manager, the question changes: which chart actually makes the point you need to make, for this audience? "
                "Chart choice is driven by the point, not by the data alone."
            ),
            "lineage": {
                "concept_ids": [C1],
                "teaching_block_ids": [tb(C1, 1)],
                "fact_ids": []
            }
        },
        {
            "type": "prose",
            "block_id": f"{TILE_ID}.s01.b2",
            "role": "mechanism",
            "text": (
                "A bar chart is used for graphing categorical data and comparing values across categories — "
                "showing average delivery time side by side for Lagos, Abuja, and Kano. "
                "A line graph is best when you want to show how a value changes over time — "
                "for example, Lagos delivery time rising week over week. "
                "Boxplots offer a condensed display for comparing distributions side by side, "
                "but they may be unfamiliar to many audiences and could introduce a learning curve; "
                "a bar chart or line plot can often make the same point more directly."
            ),
            "lineage": {
                "concept_ids": [C1],
                "teaching_block_ids": [tb(C1, 2)],
                "fact_ids": [qid(C1, "f1"), qid(C1, "f2"), qid(C1, "f3"), qid(C1, "f5")]
            }
        },
        {
            "type": "side_by_side",
            "block_id": f"{TILE_ID}.s01.b3",
            "left_label": "Bar chart — compare cities",
            "right_label": "Line graph — Lagos trend over weeks",
            "left": {
                "type": "chart",
                "chart_kind": "bar",
                "asset_ref": {
                    "asset_id": "ds_city_delivery_summary",
                    "variant_id": None,
                    "columns": ["city", "avg_delivery_minutes"]
                },
                "title": "Average Delivery Time by City",
                "alt_text": "Bar chart showing average delivery minutes for Lagos (38.4), Abuja (27.2), and Kano (22.0). Point: compare values across cities.",
                "encoding": {
                    "x": {"field": "city", "type": "nominal", "title": "City"},
                    "y": {"field": "avg_delivery_minutes", "type": "quantitative", "title": "Avg Delivery (min)"}
                },
                "annotations": [
                    {"text": "Point: Which city takes longest?"}
                ]
            },
            "right": {
                "type": "chart",
                "chart_kind": "line",
                "asset_ref": {
                    "asset_id": "ds_weekly_delivery_trend",
                    "variant_id": None,
                    "columns": ["week_number", "avg_delivery_minutes", "city"]
                },
                "title": "Lagos Delivery Time — Weeks 1–4",
                "alt_text": "Line graph showing Lagos average delivery time rising from 34.0 min in week 1 to 40.2 min in week 4. Point: show a trend over time.",
                "encoding": {
                    "x": {"field": "week_number", "type": "ordinal", "title": "Week"},
                    "y": {"field": "avg_delivery_minutes", "type": "quantitative", "title": "Avg Delivery (min)"},
                    "color": {"field": "city"}
                },
                "annotations": [
                    {"text": "Point: Is delivery time rising?"}
                ]
            },
            "takeaway": "The same delivery data, two different points — the chart type follows the point, not the other way around.",
            "lineage": {
                "concept_ids": [C1],
                "teaching_block_ids": [tb(C1, 1), tb(C1, 2)],
                "fact_ids": [qid(C1, "f1"), qid(C1, "f2"), qid(C1, "f3"), qid(C1, "f5")],
                "anchors": [anchor(C1, "visual")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [C1],
        "teaching_block_ids": [tb(C1, 1), tb(C1, 2)],
        "fact_ids": [qid(C1, "f1"), qid(C1, "f2"), qid(C1, "f3"), qid(C1, "f5")],
        "anchors": [anchor(C1, "visual")]
    }
}

# ── STEP s02: video ──────────────────────────────────────────────────────────
s02 = {
    "step_id": f"{TILE_ID}.s02",
    "type": "video",
    "concept_ids": [C1],
    "eyebrow": "Video",
    "title": "Why the chart type must match the point you are making",
    "blocks": [
        {
            "type": "media_group",
            "block_id": f"{TILE_ID}.s02.b1",
            "group_title": "Why the chart type must match the point you are making",
            "segment_ids": [
                "seg_stakeholder.chart_type_to_point_matching_RiEZ_hEf96A_0_101",
                "seg_stakeholder.chart_type_to_point_matching_Z77c53eYtHc_149_201"
            ]
        }
    ],
    "lineage": {
        "concept_ids": [C1],
        "teaching_block_ids": [],
        "fact_ids": [qid(C1, "f1"), qid(C1, "f3"), qid(C1, "f5")],
        "segment_ids": [
            "seg_stakeholder.chart_type_to_point_matching_RiEZ_hEf96A_0_101",
            "seg_stakeholder.chart_type_to_point_matching_Z77c53eYtHc_149_201"
        ]
    }
}

# ── STEP s03: explainer — pie chart, scatterplot, misconception ──────────────
# Budget: 200 words. Target: ~65 + ~55 + ~60 = 180
s03 = {
    "step_id": f"{TILE_ID}.s03",
    "type": "explainer",
    "concept_ids": [C1],
    "eyebrow": "Chart Type Matching",
    "title": "Pie charts, scatterplots, and a comparison trap",
    "lede": "Part-to-whole framing calls for a pie chart — but comparing pie slices is harder than it looks.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{TILE_ID}.s03.b1",
            "role": "practical_context",
            "text": (
                "A pie chart expresses a part-to-whole relationship in the data. "
                "It is best used for a general sense of how parts relate to the whole, "
                "or to highlight that one segment is notably larger or smaller than the others — "
                "and the pie must depict a meaningful whole (values that sum to 100%). "
                "If the point is 'Lagos accounts for most of our total delivery volume,' "
                "a pie chart of city order shares fits that framing in a way a bar chart of averages would not."
            ),
            "lineage": {
                "concept_ids": [C1],
                "teaching_block_ids": [tb(C1, 3)],
                "fact_ids": [qid(C1, "f4")]
            }
        },
        {
            "type": "prose",
            "block_id": f"{TILE_ID}.s03.b2",
            "role": "practical_context",
            "text": (
                "A scatterplot is often used to understand data rather than to communicate with it, "
                "though it can still be designed to convey findings to an audience. "
                "It is not the default choice for a non-technical stakeholder presentation, "
                "but if the distance-versus-delivery-time relationship needs to go in front of the operations manager, "
                "a scatterplot can work."
            ),
            "lineage": {
                "concept_ids": [C1],
                "teaching_block_ids": [tb(C1, 4)],
                "fact_ids": [qid(C1, "f6")]
            }
        },
        {
            "type": "prose",
            "block_id": f"{TILE_ID}.s03.b3",
            "role": "misconception",
            "text": (
                "It can look like comparing pie slices is just as easy as comparing bar lengths — but it is not. "
                "A bar chart's aligned, common baseline makes length differences easy to judge; "
                "two pie slices of similar size are harder to rank correctly by eye. "
                "When precise comparison between categories matters, a bar chart is the stronger choice."
            ),
            "lineage": {
                "concept_ids": [C1],
                "teaching_block_ids": [tb(C1, 5)],
                "fact_ids": [qid(C1, "m1")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [C1],
        "teaching_block_ids": [tb(C1, 3), tb(C1, 4), tb(C1, 5)],
        "fact_ids": [qid(C1, "f4"), qid(C1, "f6"), qid(C1, "m1")]
    }
}

# ── STEP s04: check (framing only) ─────────────────────────────────────────
s04 = {
    "step_id": f"{TILE_ID}.s04",
    "type": "check",
    "concept_ids": [C1],
    "eyebrow": "Quick Check",
    "title": "Scatterplot: exploratory or communicative?",
    "lede": "A scatterplot of delivery distance versus delivery time sits on your screen. Is it ready for the operations manager, or is it still an exploratory tool?",
    "reward": {"gems": 10},
    "lineage": {
        "concept_ids": [C1],
        "teaching_block_ids": [],
        "fact_ids": [qid(C1, "f6")],
        "anchors": [anchor(C1, "assessment:classify_scatterplot_as_exploratory_vs_communicative")]
    }
}

# ── STEP s05: hands_on (framing only) ────────────────────────────────────────
s05 = {
    "step_id": f"{TILE_ID}.s05",
    "type": "hands_on",
    "concept_ids": [C1],
    "eyebrow": "Hands-On Practice",
    "title": "Match each stakeholder point to the right chart type",
    "lede": "For each point the operations manager wants to make, choose the chart type that best communicates it — and explain why.",
    "reward": {"gems": 15},
    "lineage": {
        "concept_ids": [C1],
        "teaching_block_ids": [],
        "fact_ids": [
            qid(C1, "f1"), qid(C1, "f2"), qid(C1, "f3"), qid(C1, "f4"),
            qid(C1, "f5"), qid(C1, "f6"), qid(C1, "m1")
        ],
        "anchors": [
            anchor(C1, "practice"),
            anchor(C1, "assessment:select_chart_type_for_stakeholder_point"),
            anchor(C1, "assessment:distinguish_part_to_whole_from_comparison_framing"),
            anchor(C1, "assessment:evaluate_audience_readiness_for_boxplot")
        ]
    }
}

# ── STEP s06: explainer — simplifying charts + before_after visual ───────────
before_diagram = {
    "type": "diagram",
    "diagram_kind": "container",
    "title": "Before: cluttered bar chart",
    "nodes": [
        {"id": "border", "label": "Border: visible frame around chart"},
        {"id": "gridlines", "label": "Gridlines: horizontal lines behind bars"},
        {"id": "decimals", "label": "Axis labels: 22.00, 27.20, 38.40 min"},
        {"id": "rotated", "label": "Tick labels: rotated city names"},
        {"id": "datalabels", "label": "Data labels: value on every bar"}
    ],
    "edges": [
        {"from": "border", "to": "gridlines"},
        {"from": "gridlines", "to": "decimals"},
        {"from": "decimals", "to": "rotated"},
        {"from": "rotated", "to": "datalabels"}
    ],
    "alt_text": "Bar chart with visible border, gridlines, decimal axis labels (22.00, 27.20, 38.40), rotated city-name tick labels, and data labels on every bar — five clutter elements present."
}

after_diagram = {
    "type": "diagram",
    "diagram_kind": "container",
    "title": "After: simplified bar chart",
    "nodes": [
        {"id": "noborder", "label": "Border removed — white space separates"},
        {"id": "nogridlines", "label": "Gridlines removed"},
        {"id": "simplified", "label": "Axis labels: 22, 27, 38 min"},
        {"id": "horizontal", "label": "Tick labels: horizontal city names"},
        {"id": "nodata", "label": "No per-bar data labels — axis used instead"}
    ],
    "edges": [
        {"from": "noborder", "to": "nogridlines"},
        {"from": "nogridlines", "to": "simplified"},
        {"from": "simplified", "to": "horizontal"},
        {"from": "horizontal", "to": "nodata"}
    ],
    "alt_text": "Bar chart with border removed, gridlines removed, axis labels simplified to 22, 27, 38 min, city-name tick labels horizontal, and no per-bar data labels — same data, less visual effort."
}

s06 = {
    "step_id": f"{TILE_ID}.s06",
    "type": "explainer",
    "concept_ids": [C2],
    "eyebrow": "Simplifying Charts",
    "title": "Remove the clutter your audience doesn't need",
    "lede": "A chart built for your own exploration can carry gridlines, a border, and precise decimal labels. The operations manager probably doesn't need any of that to get the point.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{TILE_ID}.s06.b1",
            "role": "intro",
            "text": (
                "A bar chart of city delivery times built during your own exploration can carry gridlines, "
                "a border, and precise decimal labels that help you double-check the numbers. "
                "The operations manager probably doesn't need any of that to get the point. "
                "Each element you remove reduces the visual effort required to read the chart."
            ),
            "lineage": {
                "concept_ids": [C2],
                "teaching_block_ids": [tb(C2, 1)],
                "fact_ids": []
            }
        },
        {
            "type": "prose",
            "block_id": f"{TILE_ID}.s06.b2",
            "role": "mechanism",
            "text": (
                "Gridlines can be deleted from a chart; if precise values matter to the audience, "
                "label the data point directly instead of relying on gridlines. "
                "A chart's border can be removed, since it is not adding informative value — "
                "white space can differentiate parts of a visual better than a border."
            ),
            "lineage": {
                "concept_ids": [C2],
                "teaching_block_ids": [tb(C2, 2)],
                "fact_ids": [qid(C2, "f1"), qid(C2, "f2")]
            }
        },
        {
            "type": "prose",
            "block_id": f"{TILE_ID}.s06.b3",
            "role": "mechanism",
            "text": (
                "Data labels should be used sparingly, only where exact values are important; "
                "otherwise remove them and use the axis instead. "
                "Unnecessary trailing zeroes can be dropped — '22.00' becomes '22 min'. "
                "Diagonally rotated axis text is slower to read; "
                "city names like Lagos, Abuja, and Kano are short enough to render horizontally."
            ),
            "lineage": {
                "concept_ids": [C2],
                "teaching_block_ids": [tb(C2, 3)],
                "fact_ids": [qid(C2, "f3"), qid(C2, "f5"), qid(C2, "f6")]
            }
        },
        {
            "type": "before_after",
            "block_id": f"{TILE_ID}.s06.b4",
            "before": before_diagram,
            "after": after_diagram,
            "change_summary": "Five removals — border, gridlines, trailing zeros, rotated labels, per-bar data labels — reduce visual effort without changing the underlying delivery-time values.",
            "lineage": {
                "concept_ids": [C2],
                "teaching_block_ids": [tb(C2, 1), tb(C2, 2), tb(C2, 3)],
                "fact_ids": [qid(C2, "f1"), qid(C2, "f2"), qid(C2, "f3"), qid(C2, "f5"), qid(C2, "f6")],
                "anchors": [anchor(C2, "visual")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [C2],
        "teaching_block_ids": [tb(C2, 1), tb(C2, 2), tb(C2, 3)],
        "fact_ids": [qid(C2, "f1"), qid(C2, "f2"), qid(C2, "f3"), qid(C2, "f5"), qid(C2, "f6")],
        "anchors": [anchor(C2, "visual")]
    }
}

# ── STEP s07: video ──────────────────────────────────────────────────────────
s07 = {
    "step_id": f"{TILE_ID}.s07",
    "type": "video",
    "concept_ids": [C2],
    "eyebrow": "Video",
    "title": "Decluttering a chart for a non-technical audience",
    "blocks": [
        {
            "type": "media_group",
            "block_id": f"{TILE_ID}.s07.b1",
            "group_title": "Decluttering a chart for a non-technical audience",
            "segment_ids": [
                "seg_stakeholder.simplifying_charts_for_audience_XgY1-BsZSzM_51_393"
            ]
        }
    ],
    "lineage": {
        "concept_ids": [C2],
        "teaching_block_ids": [],
        "fact_ids": [qid(C2, "f2"), qid(C2, "f3"), qid(C2, "f4"), qid(C2, "f5"), qid(C2, "f6")],
        "segment_ids": [
            "seg_stakeholder.simplifying_charts_for_audience_XgY1-BsZSzM_51_393"
        ]
    }
}

# ── STEP s08: check (framing only) ───────────────────────────────────────────
s08 = {
    "step_id": f"{TILE_ID}.s08",
    "type": "check",
    "concept_ids": [C2],
    "eyebrow": "Quick Check",
    "title": "Which elements should you remove to reduce chart clutter?",
    "lede": "The operations manager will see this bar chart in a slide deck. Identify which elements add visual effort without adding information.",
    "reward": {"gems": 10},
    "lineage": {
        "concept_ids": [C2],
        "teaching_block_ids": [],
        "fact_ids": [
            qid(C2, "f1"), qid(C2, "f2"), qid(C2, "f3"),
            qid(C2, "f4"), qid(C2, "f5"), qid(C2, "f6")
        ],
        "anchors": [
            anchor(C2, "assessment:identify_clutter_elements_to_remove"),
            anchor(C2, "assessment:explain_cognitive_benefit_of_reducing_chart_clutter")
        ]
    }
}

# ── STEP s09: check (framing only) ───────────────────────────────────────────
s09 = {
    "step_id": f"{TILE_ID}.s09",
    "type": "check",
    "concept_ids": [C2],
    "eyebrow": "Quick Check",
    "title": "Why remove the chart border?",
    "lede": "A colleague says the border helps separate the chart from the slide background. What is the better alternative, and why?",
    "reward": {"gems": 10},
    "lineage": {
        "concept_ids": [C2],
        "teaching_block_ids": [],
        "fact_ids": [qid(C2, "f2")],
        "anchors": [anchor(C2, "assessment:justify_border_removal_using_white_space")]
    }
}

# ── STEP s10: hands_on (framing only) ────────────────────────────────────────
s10 = {
    "step_id": f"{TILE_ID}.s10",
    "type": "hands_on",
    "concept_ids": [C2],
    "eyebrow": "Hands-On Practice",
    "title": "Simplify a chart for the operations manager",
    "lede": "A bar chart of city delivery times has a border, gridlines, trailing-zero axis labels, rotated city-name tick labels, and data labels on every bar. Simplify it for a non-technical audience.",
    "reward": {"gems": 15},
    "lineage": {
        "concept_ids": [C2],
        "teaching_block_ids": [],
        "fact_ids": [qid(C2, "f1"), qid(C2, "f3"), qid(C2, "f5"), qid(C2, "f6")],
        "anchors": [
            anchor(C2, "practice"),
            anchor(C2, "assessment:choose_between_data_labels_and_axis_for_precision"),
            anchor(C2, "assessment:simplify_axis_labels_for_readability")
        ]
    }
}

# ── STEP s11: recap — budget 90 words ────────────────────────────────────────
# prose: ~55 words; up_next text: ~30 words = ~85 total
s11 = {
    "step_id": f"{TILE_ID}.s11",
    "type": "recap",
    "concept_ids": [C1, C2],
    "eyebrow": "Recap",
    "title": "What you've learned: matching and simplifying charts",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{TILE_ID}.s11.b1",
            "role": "takeaway",
            "text": (
                "Chart choice is driven by the point you are making, not the data alone. "
                "Bar charts compare categories; line graphs show trends; pie charts express part-to-whole relationships. "
                "Once the right chart is chosen, remove every element that adds visual effort without adding information — "
                "border, gridlines, trailing zeros, rotated labels, unnecessary data labels. "
                "Reducing clutter lets the audience focus on the finding."
            ),
            "lineage": {
                "concept_ids": [C1, C2],
                "teaching_block_ids": [tb(C2, 4)],
                "fact_ids": [qid(C2, "f4")]
            }
        },
        {
            "type": "up_next",
            "block_id": f"{TILE_ID}.s11.b2",
            "title": "Up next: Presentation Structure",
            "text": (
                "Next you will learn how to structure a stakeholder presentation — "
                "opening with the business question, building the body around your findings, "
                "and closing with a clear call to action."
            )
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [C1, C2],
        "teaching_block_ids": [tb(C2, 4)],
        "fact_ids": [qid(C2, "f4")]
    }
}

# ── REMEDIATION STEPS ─────────────────────────────────────────────────────────
r01 = {
    "step_id": f"{TILE_ID}.r01",
    "type": "remediation",
    "concept_ids": [C1],
    "eyebrow": "Let's revisit",
    "title": "Scatterplots: exploratory vs. communicative — a closer look",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{TILE_ID}.r01.b1",
            "role": "mechanism",
            "text": (
                "A scatterplot is often used to understand data rather than to communicate with it. "
                "When you plot delivery distance against delivery time for yourself, you are exploring a relationship. "
                "That same chart can be designed to convey a finding to an audience — "
                "but it is not the default choice for a non-technical stakeholder presentation, "
                "because the audience must first understand what a scatterplot shows before they can read the point. "
                "If the relationship needs to go in front of the operations manager, consider whether a simpler chart can make the same point."
            ),
            "lineage": {
                "concept_ids": [C1],
                "teaching_block_ids": [tb(C1, 4)],
                "fact_ids": [qid(C1, "f6")]
            }
        }
    ],
    "lineage": {
        "concept_ids": [C1],
        "teaching_block_ids": [tb(C1, 4)],
        "fact_ids": [qid(C1, "f6")]
    }
}

r02 = {
    "step_id": f"{TILE_ID}.r02",
    "type": "remediation",
    "concept_ids": [C1],
    "eyebrow": "Let's revisit",
    "title": "Matching chart type to stakeholder point — a contrast",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{TILE_ID}.r02.b1",
            "role": "mechanism",
            "text": (
                "Bar charts compare values across categories — use one when the point is 'Lagos takes longer than Abuja.' "
                "Line graphs show how a value changes over time — use one when the point is 'Lagos delivery time has risen each week.' "
                "Pie charts express part-to-whole relationships — use one when the point is 'Lagos accounts for most of our total order volume' "
                "and the values sum to 100% (Lagos 57.1%, Abuja 28.6%, Kano 14.3%). "
                "Boxplots compare distributions but may be unfamiliar to non-technical audiences; "
                "a bar chart or line plot can often make the same point more directly."
            ),
            "lineage": {
                "concept_ids": [C1],
                "teaching_block_ids": [tb(C1, 2), tb(C1, 3)],
                "fact_ids": [qid(C1, "f1"), qid(C1, "f2"), qid(C1, "f3"), qid(C1, "f4"), qid(C1, "f5")]
            }
        },
        {
            "type": "prose",
            "block_id": f"{TILE_ID}.r02.b2",
            "role": "misconception",
            "text": (
                "Comparing pie slices looks easy, but it is not as easy as comparing bar lengths. "
                "A bar chart's common baseline makes differences immediately readable; "
                "two similar-sized pie slices are hard to rank correctly by eye. "
                "When precise comparison between categories matters, a bar chart is the stronger choice."
            ),
            "lineage": {
                "concept_ids": [C1],
                "teaching_block_ids": [tb(C1, 5)],
                "fact_ids": [qid(C1, "m1")]
            }
        }
    ],
    "lineage": {
        "concept_ids": [C1],
        "teaching_block_ids": [tb(C1, 2), tb(C1, 3), tb(C1, 5)],
        "fact_ids": [qid(C1, "f1"), qid(C1, "f2"), qid(C1, "f3"), qid(C1, "f4"), qid(C1, "f5"), qid(C1, "m1")]
    }
}

r03 = {
    "step_id": f"{TILE_ID}.r03",
    "type": "remediation",
    "concept_ids": [C2],
    "eyebrow": "Let's revisit",
    "title": "Clutter elements and why they slow your audience down",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{TILE_ID}.r03.b1",
            "role": "mechanism",
            "text": (
                "Every element in a chart that does not add information adds cognitive effort. "
                "Gridlines can be deleted; if precise values matter, label the data point directly instead. "
                "A chart border is not adding informative value — white space separates parts of a visual better than a border. "
                "Data labels should be used sparingly, only where exact values are important; otherwise use the axis. "
                "Trailing zeroes on axis labels ('22.00') can be dropped ('22 min'). "
                "Diagonally rotated axis text is slower to read; abbreviate labels so they render horizontally."
            ),
            "lineage": {
                "concept_ids": [C2],
                "teaching_block_ids": [tb(C2, 2), tb(C2, 3)],
                "fact_ids": [qid(C2, "f1"), qid(C2, "f2"), qid(C2, "f3"), qid(C2, "f5"), qid(C2, "f6")]
            }
        },
        {
            "type": "prose",
            "block_id": f"{TILE_ID}.r03.b2",
            "role": "takeaway",
            "text": (
                "Reducing clutter lets the audience use their attention to decide what actions might be warranted, "
                "rather than working out how to read the graph. "
                "None of these changes alter the underlying delivery-time values — only how much visual effort it takes to read them."
            ),
            "lineage": {
                "concept_ids": [C2],
                "teaching_block_ids": [tb(C2, 4)],
                "fact_ids": [qid(C2, "f4")]
            }
        }
    ],
    "lineage": {
        "concept_ids": [C2],
        "teaching_block_ids": [tb(C2, 2), tb(C2, 3), tb(C2, 4)],
        "fact_ids": [qid(C2, "f1"), qid(C2, "f2"), qid(C2, "f3"), qid(C2, "f4"), qid(C2, "f5"), qid(C2, "f6")]
    }
}

r04 = {
    "step_id": f"{TILE_ID}.r04",
    "type": "remediation",
    "concept_ids": [C2],
    "eyebrow": "Let's revisit",
    "title": "Border removal and white space — why it works",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{TILE_ID}.r04.b1",
            "role": "mechanism",
            "text": (
                "A chart border might seem to help by visually containing the chart on the slide. "
                "But the border is not adding informative value — it is adding a line the eye must process. "
                "White space around the chart already differentiates it from the surrounding content. "
                "Removing the border reduces one more element the audience must look past to reach the data. "
                "The same principle applies to gridlines: if the audience needs a precise value, "
                "label that data point directly rather than restoring the gridlines."
            ),
            "lineage": {
                "concept_ids": [C2],
                "teaching_block_ids": [tb(C2, 2)],
                "fact_ids": [qid(C2, "f1"), qid(C2, "f2")]
            }
        }
    ],
    "lineage": {
        "concept_ids": [C2],
        "teaching_block_ids": [tb(C2, 2)],
        "fact_ids": [qid(C2, "f1"), qid(C2, "f2")]
    }
}

# ── Assemble tile ─────────────────────────────────────────────────────────────
tile = {
    "tile_id": TILE_ID,
    "title": "Matching and Simplifying Charts for an Audience",
    "summary": (
        "Learn to match chart type to the specific stakeholder point (bar for comparison, "
        "line for trend, pie for part-to-whole, boxplot with caution), then simplify the chosen chart "
        "by removing gridlines, borders, trailing zeros, rotated labels, and unnecessary data labels."
    ),
    "steps": [s01, s02, s03, s04, s05, s06, s07, s08, s09, s10, s11],
    "remediation_steps": [r01, r02, r03, r04]
}

output = {
    "schema_version": "1.0.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_013_da_stakeholder_chart",
    "tiles": [tile]
}

out_path = "batches/final_batch_013_da_stakeholder_chart/screens.part.c0_canary.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)

# Word count check
print(f"Written: {out_path}")
print(f"Steps: {len(tile['steps'])} main + {len(tile['remediation_steps'])} remediation")

budgets = {
    f"{TILE_ID}.s01": 180,
    f"{TILE_ID}.s03": 200,
    f"{TILE_ID}.s06": 178,
    f"{TILE_ID}.s11": 90,
}
all_steps = tile['steps'] + tile['remediation_steps']
for step in all_steps:
    sid = step['step_id']
    if sid in budgets:
        total_words = sum(len(b.get('text','').split()) for b in step.get('blocks', []))
        budget = budgets[sid]
        status = 'OK' if total_words <= budget else f'OVER by {total_words - budget}'
        print(f"  {sid}: {total_words} words / {budget} budget [{status}]")
