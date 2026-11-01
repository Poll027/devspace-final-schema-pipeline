"""
Build screens.part.c0_canary.json for tile_data_quality_and_workflow.
"""
import json

TILE_ID = "tile_data_quality_and_workflow"
PATH_ID = "data_analyst"
BATCH_ID = "final_batch_007_da_nocode"

# ── helpers ──────────────────────────────────────────────────────────────────

def qid(concept_id, local):
    """Return a qualified id like data.data_quality_basics#f1"""
    return f"{concept_id}#{local}"

# ── concept shorthands ───────────────────────────────────────────────────────
DQ  = "data.data_quality_basics"
AW  = "data.analysis_workflow"
EP  = "data.ethics_privacy_basics"

# ── step builders ────────────────────────────────────────────────────────────

def step_s01():
    """Explainer: data quality intro + data_table visual"""
    return {
        "step_id": f"{TILE_ID}.s01",
        "type": "explainer",
        "concept_ids": [DQ],
        "eyebrow": "Data Quality",
        "title": "Is the data any good?",
        "lede": "Before drawing conclusions from the delivery-orders table, you need to ask one question first: is this data fit for the purpose?",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.s01.b1",
                "role": "intro",
                "text": (
                    "Data quality means whether a dataset is fit for the purpose it will be used for — "
                    "not whether it looks tidy, but whether it can actually support the question you're asking. "
                    "Before trusting any conclusion drawn from the Kwik Courier delivery-orders table, "
                    "you need to check whether the data itself is reliable enough to answer that question."
                ),
                "lineage": {
                    "concept_ids": [DQ],
                    "fact_ids": [qid(DQ, "f1")],
                    "teaching_block_ids": [qid(DQ, "tb1")]
                }
            },
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.s01.b2",
                "role": "mechanism",
                "text": (
                    "Two checks look at what is missing or repeated. "
                    "Completeness checks whether the records and values that should be present actually are — "
                    "for example, an order row with no delivery time recorded at all. "
                    "Uniqueness checks whether a record that should appear only once is duplicated — "
                    "for example, the same order number showing up as two separate rows."
                ),
                "lineage": {
                    "concept_ids": [DQ],
                    "fact_ids": [qid(DQ, "f2"), qid(DQ, "f3")],
                    "teaching_block_ids": [qid(DQ, "tb2")]
                }
            },
            {
                "type": "data_table",
                "block_id": f"{TILE_ID}.s01.b3",
                "asset_ref": {
                    "asset_id": "ds_delivery_orders",
                    "variant_id": "ds_delivery_orders_messy",
                    "columns": ["order_id", "order_date", "city", "delivery_minutes", "driver_id"]
                },
                "caption": "Kwik Courier delivery orders — three quality problems highlighted",
                "highlight": [
                    {
                        "target": {
                            "kind": "cell",
                            "row": {"where": {"order_id": 1009}},
                            "column": "delivery_minutes"
                        },
                        "label": "Completeness failure: delivery time missing",
                        "tone": "bad"
                    },
                    {
                        "target": {
                            "kind": "row",
                            "row": {"where": {"order_id": 1003}, "occurrence": 1}
                        },
                        "label": "Uniqueness failure: duplicate order row",
                        "tone": "bad"
                    },
                    {
                        "target": {
                            "kind": "cell",
                            "row": {"where": {"order_id": 1006}},
                            "column": "delivery_minutes"
                        },
                        "label": "Validity failure: −5 minutes is not a valid delivery time",
                        "tone": "bad"
                    }
                ],
                "lineage": {
                    "concept_ids": [DQ],
                    "fact_ids": [qid(DQ, "f2"), qid(DQ, "f3"), qid(DQ, "f4")],
                    "teaching_block_ids": [qid(DQ, "tb2"), qid(DQ, "tb3")],
                    "anchors": [qid(DQ, "visual")]
                }
            }
        ],
        "reward": {"gems": 0},
        "lineage": {
            "concept_ids": [DQ],
            "fact_ids": [qid(DQ, "f1"), qid(DQ, "f2"), qid(DQ, "f3")],
            "teaching_block_ids": [qid(DQ, "tb1"), qid(DQ, "tb2")],
            "anchors": [qid(DQ, "visual")]
        }
    }


def step_s02():
    """Video: data quality basics"""
    return {
        "step_id": f"{TILE_ID}.s02",
        "type": "video",
        "concept_ids": [DQ],
        "eyebrow": "Data Quality",
        "title": "Data-quality dimensions in action",
        "lede": "Watch how each check is tied to one concrete problem: a missing detail, a repeated entry, a badly formatted value.",
        "blocks": [
            {
                "type": "media_group",
                "block_id": f"{TILE_ID}.s02.b1",
                "segment_ids": [
                    "seg_data.data_quality_basics_f7bAohSl_fo_111_326",
                    "seg_data.data_quality_basics_pncfeOvxamg_0_144"
                ]
            }
        ],
        "reward": {"gems": 0},
        "lineage": {
            "concept_ids": [DQ],
            "fact_ids": [
                qid(DQ, "f1"), qid(DQ, "f2"), qid(DQ, "f3"),
                qid(DQ, "f4"), qid(DQ, "f5")
            ],
            "teaching_block_ids": [],
            "segment_ids": [
                "seg_data.data_quality_basics_f7bAohSl_fo_111_326",
                "seg_data.data_quality_basics_pncfeOvxamg_0_144"
            ]
        }
    }


def step_s03():
    """Explainer: validity, accuracy, good-enough data"""
    return {
        "step_id": f"{TILE_ID}.s03",
        "type": "explainer",
        "concept_ids": [DQ],
        "eyebrow": "Data Quality",
        "title": "Validity, accuracy, and good enough",
        "lede": "Two more checks look at whether the values themselves are trustworthy — and data doesn't have to be perfect to be useful.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.s03.b1",
                "role": "mechanism",
                "text": (
                    "Validity checks whether a column's values are in the range and format expected — "
                    "a delivery time of −5 minutes fails validity because negative time is not a valid delivery time. "
                    "Accuracy checks whether the data correctly matches the real-world thing it describes — "
                    "an order logged as delivered to Lagos when the driver actually delivered it to Abuja "
                    "is complete, unique and validly formatted, but still inaccurate."
                ),
                "lineage": {
                    "concept_ids": [DQ],
                    "fact_ids": [qid(DQ, "f4"), qid(DQ, "f5")],
                    "teaching_block_ids": [qid(DQ, "tb3")]
                }
            },
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.s03.b2",
                "role": "misconception",
                "text": (
                    "Good-quality data does not have to be perfect. "
                    "The goal of these checks is not a flawless dataset; "
                    "it is a dataset good enough to answer the question you actually have, "
                    "using completeness, uniqueness, validity and accuracy as the specific things to look for."
                ),
                "lineage": {
                    "concept_ids": [DQ],
                    "fact_ids": [qid(DQ, "m1")],
                    "teaching_block_ids": [qid(DQ, "tb4")]
                }
            }
        ],
        "reward": {"gems": 0},
        "lineage": {
            "concept_ids": [DQ],
            "fact_ids": [qid(DQ, "f4"), qid(DQ, "f5"), qid(DQ, "m1")],
            "teaching_block_ids": [qid(DQ, "tb3"), qid(DQ, "tb4")]
        }
    }


def step_s04():
    """Check: judge fitness for purpose + spot missing/duplicate"""
    return {
        "step_id": f"{TILE_ID}.s04",
        "type": "check",
        "concept_ids": [DQ],
        "eyebrow": "Quick Check",
        "title": "Fitness for purpose and missing or duplicate records",
        "lede": "Apply what you've learned about completeness and uniqueness.",
        "reward": {"gems": 5, "first_try_bonus": 2},
        "lineage": {
            "concept_ids": [DQ],
            "fact_ids": [qid(DQ, "f1"), qid(DQ, "f2"), qid(DQ, "f3")],
            "teaching_block_ids": [],
            "anchors": [
                qid(DQ, "assessment:judge_fitness_for_purpose"),
                qid(DQ, "assessment:spot_missing_or_duplicate_records")
            ]
        }
    }


def step_s05():
    """Check: distinguish invalid from inaccurate + recognize good enough"""
    return {
        "step_id": f"{TILE_ID}.s05",
        "type": "check",
        "concept_ids": [DQ],
        "eyebrow": "Quick Check",
        "title": "Invalid vs inaccurate values, and good-enough data",
        "lede": "Distinguish validity failures from accuracy failures, and recognise when data is good enough.",
        "reward": {"gems": 5, "first_try_bonus": 2},
        "lineage": {
            "concept_ids": [DQ],
            "fact_ids": [qid(DQ, "f4"), qid(DQ, "f5"), qid(DQ, "m1")],
            "teaching_block_ids": [],
            "anchors": [
                qid(DQ, "assessment:distinguish_invalid_from_inaccurate_values"),
                qid(DQ, "assessment:recognize_good_enough_data")
            ]
        }
    }


def step_s06():
    """Hands-on: find issues in messy delivery table"""
    return {
        "step_id": f"{TILE_ID}.s06",
        "type": "hands_on",
        "concept_ids": [DQ],
        "eyebrow": "Hands On",
        "title": "Flag the quality problems",
        "lede": "The delivery-orders table below has three planted problems. Flag each one and name the check it fails.",
        "reward": {"gems": 10, "first_try_bonus": 5},
        "lineage": {
            "concept_ids": [DQ],
            "fact_ids": [],
            "teaching_block_ids": [],
            "anchors": [qid(DQ, "practice")]
        }
    }


def step_s07():
    """Explainer: analysis workflow intro + process_flow visual"""
    return {
        "step_id": f"{TILE_ID}.s07",
        "type": "explainer",
        "concept_ids": [AW],
        "eyebrow": "Analysis Workflow",
        "title": "A repeatable order for analysis",
        "lede": "Knowing what to check is only half the job — you also need to know what order to do things in.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.s07.b1",
                "role": "intro",
                "text": (
                    "A repeatable analysis process typically begins by clarifying the question or purpose — "
                    "for the Kwik Courier data, that might be 'which cities have unusually slow deliveries?' "
                    "Clarifying this first means both you and whoever asked for the analysis share an understanding "
                    "of what is being analyzed and why, before any work starts."
                ),
                "lineage": {
                    "concept_ids": [AW],
                    "fact_ids": [qid(AW, "f1")],
                    "teaching_block_ids": [qid(AW, "tb1")]
                }
            },
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.s07.b2",
                "role": "workflow",
                "text": (
                    "Next comes inspecting and cleaning. "
                    "Before analysis, the data should be inspected and checked for quality so problems are addressed early — "
                    "this is where the completeness, uniqueness, validity and accuracy checks come in. "
                    "Cleaning then helps reduce quality problems such as duplication and inconsistent values, "
                    "for example removing the duplicate order row found during inspection."
                ),
                "lineage": {
                    "concept_ids": [AW],
                    "fact_ids": [qid(AW, "f2"), qid(AW, "f3")],
                    "teaching_block_ids": [qid(AW, "tb2")]
                }
            },
            {
                "type": "process_flow",
                "block_id": f"{TILE_ID}.s07.b3",
                "title": "The six-stage analysis workflow",
                "direction": "LR",
                "nodes": [
                    {"id": "n_clarify",   "label": "Clarify the question", "kind": "start",  "detail": "Agree on what is being analyzed and why"},
                    {"id": "n_inspect",   "label": "Inspect",              "kind": "step",   "detail": "Check completeness, uniqueness, validity, accuracy"},
                    {"id": "n_clean",     "label": "Clean",                "kind": "step",   "detail": "Remove duplicates, fix inconsistent values"},
                    {"id": "n_analyze",   "label": "Analyze",              "kind": "step",   "detail": "Examine prepared data; spot anomalies"},
                    {"id": "n_visualize", "label": "Visualize",            "kind": "step",   "detail": "Turn data into plots or graphics"},
                    {"id": "n_communicate","label": "Communicate",         "kind": "end",    "detail": "Share findings and their limitations"}
                ],
                "edges": [
                    {"from": "n_clarify",    "to": "n_inspect",    "kind": "next"},
                    {"from": "n_inspect",    "to": "n_clean",      "kind": "next"},
                    {"from": "n_clean",      "to": "n_analyze",    "kind": "next"},
                    {"from": "n_analyze",    "to": "n_visualize",  "kind": "next"},
                    {"from": "n_visualize",  "to": "n_communicate","kind": "next"},
                    {"from": "n_analyze",    "to": "n_inspect",    "kind": "loop_back", "label": "new issue found"},
                    {"from": "n_visualize",  "to": "n_inspect",    "kind": "loop_back", "label": "new issue found"}
                ],
                "reveal": "all",
                "alt_text": (
                    "Six boxes in a row: Clarify the question → Inspect → Clean → Analyze → Visualize → Communicate. "
                    "Two loop-back arrows point from Analyze and Visualize back to Inspect, labelled 'new issue found'."
                ),
                "lineage": {
                    "concept_ids": [AW],
                    "fact_ids": [
                        qid(AW, "f1"), qid(AW, "f2"), qid(AW, "f3"),
                        qid(AW, "f4"), qid(AW, "f5"), qid(AW, "f6"), qid(AW, "f7")
                    ],
                    "teaching_block_ids": [
                        qid(AW, "tb1"), qid(AW, "tb2"), qid(AW, "tb3"),
                        qid(AW, "tb4"), qid(AW, "tb5"), qid(AW, "tb6")
                    ],
                    "anchors": [qid(AW, "visual")]
                }
            }
        ],
        "reward": {"gems": 0},
        "lineage": {
            "concept_ids": [AW],
            "fact_ids": [qid(AW, "f1"), qid(AW, "f2"), qid(AW, "f3")],
            "teaching_block_ids": [qid(AW, "tb1"), qid(AW, "tb2")],
            "anchors": [qid(AW, "visual")]
        }
    }


def step_s08():
    """Video: analysis workflow"""
    return {
        "step_id": f"{TILE_ID}.s08",
        "type": "video",
        "concept_ids": [AW],
        "eyebrow": "Analysis Workflow",
        "title": "One analysis walked through in order",
        "lede": "Watch how ask, prepare, clean, analyze and share play out in a real example.",
        "blocks": [
            {
                "type": "media_group",
                "block_id": f"{TILE_ID}.s08.b1",
                "segment_ids": [
                    "seg_data.analysis_workflow_Jye81eSts2c_4_276"
                ]
            }
        ],
        "reward": {"gems": 0},
        "lineage": {
            "concept_ids": [AW],
            "fact_ids": [
                qid(AW, "f1"), qid(AW, "f2"), qid(AW, "f4"), qid(AW, "f6")
            ],
            "teaching_block_ids": [],
            "segment_ids": ["seg_data.analysis_workflow_Jye81eSts2c_4_276"]
        }
    }


def step_s09():
    """Explainer: analyze vs visualize"""
    return {
        "step_id": f"{TILE_ID}.s09",
        "type": "explainer",
        "concept_ids": [AW],
        "eyebrow": "Analysis Workflow",
        "title": "Analyzing and visualizing are different steps",
        "lede": "Examining the data and turning it into a graphic are two distinct jobs — keeping them separate matters.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.s09.b1",
                "role": "workflow",
                "text": (
                    "Analyzing means examining the prepared data to answer the question. "
                    "Exploratory data analysis looks at the data to uncover its underlying structure and spot anomalies — "
                    "unusual values, like one delivery that took far longer than every other in the batch. "
                    "For the Kwik Courier data, analyzing might mean looking closely at the cleaned rows "
                    "to see which cities' deliveries stand out."
                ),
                "lineage": {
                    "concept_ids": [AW],
                    "fact_ids": [qid(AW, "f4")],
                    "teaching_block_ids": [qid(AW, "tb3")]
                }
            },
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.s09.b2",
                "role": "workflow",
                "text": (
                    "Visualizing is its own step: turning data into plots or other graphics. "
                    "Exploratory data analysis relies mostly on such graphical techniques to gain insight and reveal structure, "
                    "but making the graphic is a different job from examining the data. "
                    "For the delivery data, visualizing might mean turning those delivery times into a graphic "
                    "so the pattern is easy to see at a glance."
                ),
                "lineage": {
                    "concept_ids": [AW],
                    "fact_ids": [qid(AW, "f5")],
                    "teaching_block_ids": [qid(AW, "tb4")]
                }
            }
        ],
        "reward": {"gems": 0},
        "lineage": {
            "concept_ids": [AW],
            "fact_ids": [qid(AW, "f4"), qid(AW, "f5")],
            "teaching_block_ids": [qid(AW, "tb3"), qid(AW, "tb4")]
        }
    }


def step_s10():
    """Explainer: communicate findings"""
    return {
        "step_id": f"{TILE_ID}.s10",
        "type": "explainer",
        "concept_ids": [AW],
        "eyebrow": "Analysis Workflow",
        "title": "Communicating findings is part of the workflow",
        "lede": "The analysis isn't done when the numbers are ready — sharing what they mean, and how far they can be trusted, is the final stage.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.s10.b1",
                "role": "workflow",
                "text": (
                    "The final stage is communicating the findings, and how far they can be trusted, "
                    "to the people who will use them — not merely producing the analysis itself. "
                    "Telling a manager 'Lagos deliveries are running slow, but the sample is small' "
                    "is part of the workflow, not an afterthought."
                ),
                "lineage": {
                    "concept_ids": [AW],
                    "fact_ids": [qid(AW, "f6")],
                    "teaching_block_ids": [qid(AW, "tb5")]
                }
            }
        ],
        "reward": {"gems": 0},
        "lineage": {
            "concept_ids": [AW],
            "fact_ids": [qid(AW, "f6")],
            "teaching_block_ids": [qid(AW, "tb5")]
        }
    }


def step_s11():
    """Check: recognize iterative loop-back"""
    return {
        "step_id": f"{TILE_ID}.s11",
        "type": "check",
        "concept_ids": [AW],
        "eyebrow": "Quick Check",
        "title": "The workflow loops back",
        "lede": "Recognise when and why the process revisits earlier stages.",
        "reward": {"gems": 5, "first_try_bonus": 2},
        "lineage": {
            "concept_ids": [AW],
            "fact_ids": [qid(AW, "f7")],
            "teaching_block_ids": [],
            "anchors": [qid(AW, "assessment:recognize_iterative_loop_back")]
        }
    }


def step_s12():
    """Hands-on: order workflow steps"""
    return {
        "step_id": f"{TILE_ID}.s12",
        "type": "hands_on",
        "concept_ids": [AW],
        "eyebrow": "Hands On",
        "title": "Put the workflow in order",
        "lede": "Arrange the six analysis stages in the correct order, then identify where the process loops back when a suspicious value turns up.",
        "reward": {"gems": 10, "first_try_bonus": 5},
        "lineage": {
            "concept_ids": [AW],
            "fact_ids": [
                qid(AW, "f1"), qid(AW, "f2"), qid(AW, "f3"),
                qid(AW, "f4"), qid(AW, "f5"), qid(AW, "f6"), qid(AW, "f7")
            ],
            "teaching_block_ids": [],
            "anchors": [
                qid(AW, "practice"),
                qid(AW, "assessment:order_workflow_steps"),
                qid(AW, "assessment:separate_analyze_from_visualize"),
                qid(AW, "assessment:recognize_iterative_loop_back")
            ]
        }
    }


def step_s13():
    """Explainer: ethics and privacy intro"""
    return {
        "step_id": f"{TILE_ID}.s13",
        "type": "explainer",
        "concept_ids": [EP],
        "eyebrow": "Data Ethics",
        "title": "The people behind the data",
        "lede": "The delivery-orders table contains information about real people — that changes how you should handle it.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.s13.b1",
                "role": "intro",
                "text": (
                    "The Kwik Courier delivery-orders table almost certainly contains information about real people — "
                    "customers' addresses, drivers' names. "
                    "Data users should respect the privacy and confidentiality of the individuals a dataset describes, "
                    "which means treating that table as more than just numbers to analyze."
                ),
                "lineage": {
                    "concept_ids": [EP],
                    "fact_ids": [qid(EP, "f1")],
                    "teaching_block_ids": [qid(EP, "tb1")]
                }
            },
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.s13.b2",
                "role": "practical_context",
                "text": (
                    "Responsible data handling includes minimizing data collection to what is needed and being accountable "
                    "for how the data is used — if the analysis only needs delivery times and cities, "
                    "there is no reason to collect or keep customers' phone numbers. "
                    "Data work should also consider its potential impact on the people and communities it affects: "
                    "a finding like 'deliveries to this neighborhood are consistently late' "
                    "could affect real customers and drivers, not just look interesting in a report."
                ),
                "lineage": {
                    "concept_ids": [EP],
                    "fact_ids": [qid(EP, "f2"), qid(EP, "f3")],
                    "teaching_block_ids": [qid(EP, "tb2")]
                }
            }
        ],
        "reward": {"gems": 0},
        "lineage": {
            "concept_ids": [EP],
            "fact_ids": [qid(EP, "f1"), qid(EP, "f2"), qid(EP, "f3")],
            "teaching_block_ids": [qid(EP, "tb1"), qid(EP, "tb2")]
        }
    }


def step_s14():
    """Explainer: honest reporting + de-identification misconception"""
    return {
        "step_id": f"{TILE_ID}.s14",
        "type": "explainer",
        "concept_ids": [EP],
        "eyebrow": "Data Ethics",
        "title": "Honest reporting and the limits of removing names",
        "lede": "Sharing findings responsibly means stating what the data can and cannot claim — and knowing that removing a name column is not enough.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.s14.b1",
                "role": "practical_context",
                "text": (
                    "When sharing data and findings, data users should honestly report data limitations and known biases "
                    "rather than overstating certainty — if the delivery data only covers one week, "
                    "or one driver logged times inconsistently, that limitation belongs in the report. "
                    "Identifying information that is not needed for the purpose should be left out or removed, "
                    "especially before data is shared; findings can describe a group without identifying individuals — "
                    "reporting 'the eastern delivery zone runs slow' rather than naming individual customers."
                ),
                "lineage": {
                    "concept_ids": [EP],
                    "fact_ids": [qid(EP, "f4"), qid(EP, "f5")],
                    "teaching_block_ids": [qid(EP, "tb3")]
                }
            },
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.s14.b2",
                "role": "misconception",
                "text": (
                    "Removing identifying information does not by itself remove the risk of re-identification: "
                    "the data, combined with other available data, can still identify people, "
                    "so removing a name column alone is not automatically enough."
                ),
                "lineage": {
                    "concept_ids": [EP],
                    "fact_ids": [qid(EP, "m1")],
                    "teaching_block_ids": [qid(EP, "tb4")]
                }
            }
        ],
        "reward": {"gems": 0},
        "lineage": {
            "concept_ids": [EP],
            "fact_ids": [qid(EP, "f4"), qid(EP, "f5"), qid(EP, "m1")],
            "teaching_block_ids": [qid(EP, "tb3"), qid(EP, "tb4")]
        }
    }


def step_s15():
    """Check: identify unneeded identifying data + minimal collection"""
    return {
        "step_id": f"{TILE_ID}.s15",
        "type": "check",
        "concept_ids": [EP],
        "eyebrow": "Quick Check",
        "title": "Privacy, minimal collection, and impact",
        "lede": "Apply the principles of privacy, minimal collection and impact thinking to the delivery-orders scenario.",
        "reward": {"gems": 5, "first_try_bonus": 2},
        "lineage": {
            "concept_ids": [EP],
            "fact_ids": [
                qid(EP, "f1"), qid(EP, "f2"), qid(EP, "f3"), qid(EP, "f5")
            ],
            "teaching_block_ids": [],
            "anchors": [
                qid(EP, "assessment:identify_unneeded_identifying_data"),
                qid(EP, "assessment:apply_minimal_collection_and_impact_thinking")
            ]
        }
    }


def step_s16():
    """Check: report limitations honestly + recognize re-identification risk"""
    return {
        "step_id": f"{TILE_ID}.s16",
        "type": "check",
        "concept_ids": [EP],
        "eyebrow": "Quick Check",
        "title": "Honest reporting and re-identification risk",
        "lede": "Recognise when a finding overstates certainty, and why removing names is not always enough.",
        "reward": {"gems": 5, "first_try_bonus": 2},
        "lineage": {
            "concept_ids": [EP],
            "fact_ids": [qid(EP, "f4"), qid(EP, "m1")],
            "teaching_block_ids": [],
            "anchors": [
                qid(EP, "assessment:report_limitations_honestly"),
                qid(EP, "assessment:recognize_reidentification_risk")
            ]
        }
    }


def step_s17():
    """Hands-on: table_select — choose columns to keep"""
    return {
        "step_id": f"{TILE_ID}.s17",
        "type": "hands_on",
        "concept_ids": [EP],
        "eyebrow": "Hands On",
        "title": "Which columns should you keep?",
        "lede": "Given the delivery-orders table and a stated analysis purpose, select the columns to keep before sharing — and note one limitation to report.",
        "reward": {"gems": 10, "first_try_bonus": 5},
        "lineage": {
            "concept_ids": [EP],
            "fact_ids": [],
            "teaching_block_ids": [],
            "anchors": [qid(EP, "practice")]
        }
    }


def step_s18():
    """Recap"""
    return {
        "step_id": f"{TILE_ID}.s18",
        "type": "recap",
        "concept_ids": [DQ, AW, EP],
        "eyebrow": "Recap",
        "title": "What you've learned",
        "lede": "Three ideas that will shape every analysis you run.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.s18.b1",
                "role": "takeaway",
                "text": (
                    "Running completeness, uniqueness, validity and accuracy checks on the delivery-orders table "
                    "before analyzing it is what tells you whether you can trust what the numbers say. "
                    "The analysis workflow — clarify, inspect, clean, analyze, visualize, communicate — "
                    "is commonly iterative: earlier stages may be revisited as later stages reveal new issues. "
                    "Treating the people behind the data with care, and being honest about what the analysis "
                    "can and cannot claim, is as much a part of the job as getting the numbers right."
                ),
                "lineage": {
                    "concept_ids": [DQ, AW, EP],
                    "fact_ids": [
                        qid(DQ, "f1"), qid(AW, "f7"), qid(EP, "f1"), qid(EP, "f4")
                    ],
                    "teaching_block_ids": [
                        qid(DQ, "tb5"), qid(AW, "tb6"), qid(EP, "tb5")
                    ]
                }
            },
            {
                "type": "up_next",
                "block_id": f"{TILE_ID}.s18.b2",
                "title": "Up next: Variables and assignment",
                "text": (
                    "In the next tile you will learn how Python stores values in variables — "
                    "the foundation for writing code that processes the delivery-orders data."
                )
            }
        ],
        "reward": {"gems": 5},
        "lineage": {
            "concept_ids": [DQ, AW, EP],
            "fact_ids": [
                qid(AW, "f7"), qid(DQ, "f1"), qid(EP, "f1"), qid(EP, "f4")
            ],
            "teaching_block_ids": [
                qid(DQ, "tb5"), qid(AW, "tb6"), qid(EP, "tb5")
            ]
        }
    }


# ── remediation steps ─────────────────────────────────────────────────────────

def remediation_r01():
    """
    Remediation for s04 (checks f1, f2, f3: fitness for purpose, completeness, uniqueness).
    """
    return {
        "step_id": f"{TILE_ID}.r01",
        "type": "remediation",
        "concept_ids": [DQ],
        "eyebrow": "Let's revisit",
        "title": "Fitness for purpose, completeness and uniqueness — a closer look",
        "lede": "Here is a clear contrast to help you see the difference.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.r01.b1",
                "role": "definition",
                "text": (
                    "Data quality means whether a dataset is fit for the purpose it will be used for. "
                    "A completeness failure means a value that should be present is missing — "
                    "order 1009 in the Kwik Courier table has no delivery time recorded at all. "
                    "A uniqueness failure means a record that should appear once is duplicated — "
                    "order 1003 appears as two identical rows. "
                    "Neither problem means the data is useless; it means you know what to fix before analyzing."
                ),
                "lineage": {
                    "concept_ids": [DQ],
                    "fact_ids": [qid(DQ, "f1"), qid(DQ, "f2"), qid(DQ, "f3")],
                    "teaching_block_ids": [qid(DQ, "tb1"), qid(DQ, "tb2")]
                }
            },
            {
                "type": "data_table",
                "block_id": f"{TILE_ID}.r01.b2",
                "asset_ref": {
                    "asset_id": "ds_delivery_orders",
                    "variant_id": "ds_delivery_orders_messy",
                    "columns": ["order_id", "order_date", "city", "delivery_minutes"]
                },
                "caption": "Completeness failure (order 1009) and uniqueness failure (order 1003 duplicated)",
                "highlight": [
                    {
                        "target": {
                            "kind": "cell",
                            "row": {"where": {"order_id": 1009}},
                            "column": "delivery_minutes"
                        },
                        "label": "Completeness: delivery time missing",
                        "tone": "bad"
                    },
                    {
                        "target": {
                            "kind": "row",
                            "row": {"where": {"order_id": 1003}, "occurrence": 1}
                        },
                        "label": "Uniqueness: duplicate row",
                        "tone": "bad"
                    }
                ],
                "lineage": {
                    "concept_ids": [DQ],
                    "fact_ids": [qid(DQ, "f2"), qid(DQ, "f3")],
                    "teaching_block_ids": [qid(DQ, "tb2")]
                }
            }
        ],
        "reward": {"gems": 0},
        "lineage": {
            "concept_ids": [DQ],
            "fact_ids": [qid(DQ, "f1"), qid(DQ, "f2"), qid(DQ, "f3")],
            "teaching_block_ids": [qid(DQ, "tb1"), qid(DQ, "tb2")]
        }
    }


def remediation_r02():
    """
    Remediation for s05 (checks f4, f5, m1: validity, accuracy, good-enough).
    """
    return {
        "step_id": f"{TILE_ID}.r02",
        "type": "remediation",
        "concept_ids": [DQ],
        "eyebrow": "Let's revisit",
        "title": "Validity vs accuracy — the key contrast",
        "lede": "These two checks are easy to confuse. Here is the clearest way to tell them apart.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.r02.b1",
                "role": "definition",
                "text": (
                    "Validity checks whether a value is in the expected range or format — "
                    "order 1006 has delivery_minutes = −5, which is not a valid delivery time. "
                    "Accuracy checks whether the value correctly matches the real world — "
                    "an order logged as delivered to Lagos when the driver actually delivered it to Abuja "
                    "passes validity (the city name is a real city) but fails accuracy. "
                    "Good-quality data does not have to be perfect; it only has to be good enough "
                    "to answer the question you actually have."
                ),
                "lineage": {
                    "concept_ids": [DQ],
                    "fact_ids": [qid(DQ, "f4"), qid(DQ, "f5"), qid(DQ, "m1")],
                    "teaching_block_ids": [qid(DQ, "tb3"), qid(DQ, "tb4")]
                }
            }
        ],
        "reward": {"gems": 0},
        "lineage": {
            "concept_ids": [DQ],
            "fact_ids": [qid(DQ, "f4"), qid(DQ, "f5"), qid(DQ, "m1")],
            "teaching_block_ids": [qid(DQ, "tb3"), qid(DQ, "tb4")]
        }
    }


def remediation_r03():
    """
    Remediation for s11 (checks f7: iterative loop-back).
    """
    return {
        "step_id": f"{TILE_ID}.r03",
        "type": "remediation",
        "concept_ids": [AW],
        "eyebrow": "Let's revisit",
        "title": "Why the workflow loops back",
        "lede": "The analysis process is not a straight line — here is why earlier stages get revisited.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.r03.b1",
                "role": "mechanism",
                "text": (
                    "This process is commonly iterative rather than strictly linear: "
                    "earlier stages, such as inspecting or cleaning, may be revisited as later stages reveal new issues. "
                    "If analyzing the Kwik Courier delivery data turns up a value that looks wrong, "
                    "you go back and inspect or clean it before continuing, "
                    "rather than treating each stage as done for good."
                ),
                "lineage": {
                    "concept_ids": [AW],
                    "fact_ids": [qid(AW, "f7")],
                    "teaching_block_ids": [qid(AW, "tb6")]
                }
            }
        ],
        "reward": {"gems": 0},
        "lineage": {
            "concept_ids": [AW],
            "fact_ids": [qid(AW, "f7")],
            "teaching_block_ids": [qid(AW, "tb6")]
        }
    }


def remediation_r04():
    """
    Remediation for s15 (checks f1, f2, f3, f5: privacy, minimal collection, impact, unneeded data).
    """
    return {
        "step_id": f"{TILE_ID}.r04",
        "type": "remediation",
        "concept_ids": [EP],
        "eyebrow": "Let's revisit",
        "title": "Privacy, minimal collection and impact — a concrete contrast",
        "lede": "Here is the clearest way to apply these principles to the delivery-orders table.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.r04.b1",
                "role": "practical_context",
                "text": (
                    "Data users should respect the privacy and confidentiality of the individuals a dataset describes. "
                    "Responsible data handling means minimizing collection to what is needed — "
                    "if the analysis only needs delivery times and cities, "
                    "customer phone numbers should not be collected or kept. "
                    "Data work should consider its potential impact on the people it affects: "
                    "a finding about slow deliveries in one area affects real customers and drivers. "
                    "Identifying information that is not needed for the purpose should be left out or removed "
                    "before data is shared; findings can describe a group without identifying individuals."
                ),
                "lineage": {
                    "concept_ids": [EP],
                    "fact_ids": [qid(EP, "f1"), qid(EP, "f2"), qid(EP, "f3"), qid(EP, "f5")],
                    "teaching_block_ids": [qid(EP, "tb1"), qid(EP, "tb2"), qid(EP, "tb3")]
                }
            }
        ],
        "reward": {"gems": 0},
        "lineage": {
            "concept_ids": [EP],
            "fact_ids": [qid(EP, "f1"), qid(EP, "f2"), qid(EP, "f3"), qid(EP, "f5")],
            "teaching_block_ids": [qid(EP, "tb1"), qid(EP, "tb2"), qid(EP, "tb3")]
        }
    }


def remediation_r05():
    """
    Remediation for s16 (checks f4, m1: honest reporting, re-identification risk).
    """
    return {
        "step_id": f"{TILE_ID}.r05",
        "type": "remediation",
        "concept_ids": [EP],
        "eyebrow": "Let's revisit",
        "title": "Honest reporting and re-identification — why removing names is not enough",
        "lede": "Two principles that are easy to underestimate.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.r05.b1",
                "role": "practical_context",
                "text": (
                    "When sharing findings, data users should honestly report data limitations and known biases "
                    "rather than overstating certainty — if the delivery data only covers one week, "
                    "that limitation belongs in the report. "
                    "Removing identifying information does not by itself remove the risk of re-identification: "
                    "the data, combined with other available data, can still identify people, "
                    "so removing a name column alone is not automatically enough."
                ),
                "lineage": {
                    "concept_ids": [EP],
                    "fact_ids": [qid(EP, "f4"), qid(EP, "m1")],
                    "teaching_block_ids": [qid(EP, "tb3"), qid(EP, "tb4")]
                }
            }
        ],
        "reward": {"gems": 0},
        "lineage": {
            "concept_ids": [EP],
            "fact_ids": [qid(EP, "f4"), qid(EP, "m1")],
            "teaching_block_ids": [qid(EP, "tb3"), qid(EP, "tb4")]
        }
    }


# ── assemble ──────────────────────────────────────────────────────────────────

artifact = {
    "schema_version": "1.0.0",
    "kind": "screens_part",
    "path_id": PATH_ID,
    "batch_id": BATCH_ID,
    "tiles": [
        {
            "tile_id": TILE_ID,
            "title": "Data Quality and the Analysis Workflow",
            "summary": (
                "Learn to check whether a dataset is fit for purpose using four quality checks "
                "(completeness, uniqueness, validity, accuracy), follow a six-stage repeatable analysis workflow, "
                "and apply basic data-ethics and privacy principles when handling and sharing data."
            ),
            "steps": [
                step_s01(),
                step_s02(),
                step_s03(),
                step_s04(),
                step_s05(),
                step_s06(),
                step_s07(),
                step_s08(),
                step_s09(),
                step_s10(),
                step_s11(),
                step_s12(),
                step_s13(),
                step_s14(),
                step_s15(),
                step_s16(),
                step_s17(),
                step_s18(),
            ],
            "remediation_steps": [
                remediation_r01(),
                remediation_r02(),
                remediation_r03(),
                remediation_r04(),
                remediation_r05(),
            ]
        }
    ]
}

out_path = "batches/final_batch_007_da_nocode/screens.part.c0_canary.json"
with open(out_path, "w") as f:
    json.dump(artifact, f, indent=2)

print(f"Written to {out_path}")
print(f"Steps: {len(artifact['tiles'][0]['steps'])}")
print(f"Remediation steps: {len(artifact['tiles'][0]['remediation_steps'])}")
