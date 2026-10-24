#!/usr/bin/env python3
"""Generate interactions for tile_stats_shape_outliers"""

import json

# Load the necessary data
with open('tile_plans.json', 'r') as f:
    plans = json.load(f)

with open('inputs/path_glossary_bundle.json', 'r') as f:
    glossary = json.load(f)

with open('scenario_asset_registry.json', 'r') as f:
    registry = json.load(f)

with open('screens.json', 'r') as f:
    screens = json.load(f)

# Find the tile
tile_plan = None
for tile in plans['tiles']:
    if tile['tile_id'] == 'tile_stats_shape_outliers':
        tile_plan = tile
        break

# Find the tile screens
tile_screens = None
for tile in screens['tiles']:
    if tile['tile_id'] == 'tile_stats_shape_outliers':
        tile_screens = tile
        break

# Build concept bundles lookup
concept_bundles = {}
for bundle in glossary['bundles']:
    concept_id = bundle['context']['concept_id']
    concept_bundles[concept_id] = bundle

# Build asset lookup
assets = {}
for asset in registry['assets']:
    assets[asset['asset_id']] = asset

# Helper to get full fact_id
def full_fact_id(concept_id, fact_id):
    return f"{concept_id}#{fact_id}"

# Helper to get full anchor id
def full_anchor_id(concept_id, anchor_type, capability=None):
    if capability:
        return f"{concept_id}#{anchor_type}:{capability}"
    else:
        return f"{concept_id}#{anchor_type}"

# Generate interactions
interactions = []

# Step s04: check - choice - stats.distribution_shape
step_id = "tile_stats_shape_outliers.s04"
step = next(s for s in tile_plan['steps'] if s['step_id'] == step_id)

# Get the assessment anchor
anchor = None
for a in concept_bundles['stats.distribution_shape']['assessment_anchors']:
    if a['capability'] == 'relate_skew_to_mean_versus_median':
        anchor = a
        break

interaction_s04 = {
    "step_id": step_id,
    "interaction": {
        "type": "choice",
        "interaction_id": f"ix.{step_id}",
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "stats.distribution_shape",
                "capability": "relate_skew_to_mean_versus_median",
                "fact_ids": [
                    full_fact_id("stats.distribution_shape", "f1"),
                    full_fact_id("stats.distribution_shape", "f3")
                ]
            }
        ],
        "anchors": [
            full_anchor_id("stats.distribution_shape", "assessment", "relate_skew_to_mean_versus_median")
        ],
        "public": {
            "prompt": "A delivery-time dataset has a long tail trailing to the right. How does that affect the mean compared with the median?",
            "options": [
                {
                    "option_id": "opt_mean_above",
                    "text": "The mean sits above the median"
                },
                {
                    "option_id": "opt_mean_below",
                    "text": "The mean sits below the median"
                },
                {
                    "option_id": "opt_mean_equal",
                    "text": "The mean equals the median"
                },
                {
                    "option_id": "opt_no_effect",
                    "text": "The tail has no effect on the mean or median"
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_mean_above"],
            "option_feedback": {
                "opt_mean_above": {
                    "message": "Correct. The mean is more affected by extreme observations in the long tail, so it gets pulled toward the right tail, sitting above the median."
                },
                "opt_mean_below": {
                    "message": "Not quite. A right-skewed distribution has a tail trailing to the right, which pulls the mean toward the right, not the left. The mean sits above the median, not below it."
                },
                "opt_mean_equal": {
                    "message": "Not quite. The mean and median are equal only in symmetric distributions. In a right-skewed distribution, the mean is pulled toward the long tail, so it sits above the median."
                },
                "opt_no_effect": {
                    "message": "Not quite. The tail does affect the mean: extreme observations in the long tail pull the mean toward them. The median is more robust to these extremes."
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "Exactly right. The mean is pulled toward the long tail, while the median stays more centered."
            },
            "incorrect": {
                "message": "Remember: the mean is more affected by extreme values than the median."
            },
            "hints": [
                "Think about which measure—mean or median—is more affected by extreme values.",
                "The tail trails to the right, meaning there are some unusually high values. Which measure gets pulled toward them?"
            ],
            "remediation_step_id": "tile_stats_shape_outliers.s01"
        }
    }
}
interactions.append(interaction_s04)

# Step s05: hands_on - table_select - stats.distribution_shape
step_id = "tile_stats_shape_outliers.s05"
step = next(s for s in tile_plan['steps'] if s['step_id'] == step_id)

# Use ds_delivery_orders_extended to create scenarios
# We need to create different subsets showing different skew patterns
# For this hands-on, we'll use the full dataset and ask learners to identify characteristics

interaction_s05 = {
    "step_id": step_id,
    "interaction": {
        "type": "table_select",
        "interaction_id": f"ix.{step_id}",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "stats.distribution_shape",
                "capability": "classify_skew_direction",
                "fact_ids": [
                    full_fact_id("stats.distribution_shape", "f1")
                ]
            },
            {
                "concept_id": "stats.distribution_shape",
                "capability": "recognize_symmetric_distribution",
                "fact_ids": [
                    full_fact_id("stats.distribution_shape", "f2")
                ]
            },
            {
                "concept_id": "stats.distribution_shape",
                "capability": "relate_skew_to_mean_versus_median",
                "fact_ids": [
                    full_fact_id("stats.distribution_shape", "f1"),
                    full_fact_id("stats.distribution_shape", "f3")
                ]
            }
        ],
        "anchors": [
            full_anchor_id("stats.distribution_shape", "practice"),
            full_anchor_id("stats.distribution_shape", "assessment", "classify_skew_direction"),
            full_anchor_id("stats.distribution_shape", "assessment", "recognize_symmetric_distribution"),
            full_anchor_id("stats.distribution_shape", "assessment", "relate_skew_to_mean_versus_median")
        ],
        "public": {
            "asset_ref": {
                "asset_id": "ds_delivery_orders_extended",
                "variant_id": None,
                "columns": ["order_id", "delivery_minutes"]
            },
            "intro": "The table shows 20 delivery times in minutes. Examine the spread of values to answer the questions below.",
            "tasks": [
                {
                    "task_id": "task_highest",
                    "prompt": "Select the row with the highest delivery time.",
                    "target_kind": "row"
                },
                {
                    "task_id": "task_lowest",
                    "prompt": "Select the row with the lowest delivery time.",
                    "target_kind": "row"
                },
                {
                    "task_id": "task_median_row",
                    "prompt": "Select the row that contains the median delivery time (the middle value when sorted).",
                    "target_kind": "row"
                }
            ]
        },
        "grading": {
            "answers": [
                {
                    "task_id": "task_highest",
                    "row": {
                        "where": {"order_id": "ORD-118"},
                        "occurrence": 0
                    },
                    "column": "delivery_minutes",
                    "expect_value": 52
                },
                {
                    "task_id": "task_lowest",
                    "row": {
                        "where": {"order_id": "ORD-113"},
                        "occurrence": 0
                    },
                    "column": "delivery_minutes",
                    "expect_value": 17
                },
                {
                    "task_id": "task_median_row",
                    "row": {
                        "where": {"order_id": "ORD-109"},
                        "occurrence": 0
                    },
                    "column": "delivery_minutes",
                    "expect_value": 29
                }
            ],
            "task_feedback": {
                "task_highest": {
                    "correct": "Correct. ORD-118 has 52 minutes, the highest delivery time in the dataset.",
                    "incorrect": "Not quite. Look for the row with the largest value in the delivery_minutes column."
                },
                "task_lowest": {
                    "correct": "Correct. ORD-113 has 17 minutes, the lowest delivery time in the dataset.",
                    "incorrect": "Not quite. Look for the row with the smallest value in the delivery_minutes column."
                },
                "task_median_row": {
                    "correct": "Correct. When the 20 values are sorted, the median is the average of the 10th and 11th values, which are both 29 minutes.",
                    "incorrect": "Not quite. The median is the middle value when all 20 delivery times are sorted. With 20 values, it's the average of the 10th and 11th values."
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "Well done! You've identified the extreme values and the median, which are key to understanding the distribution's shape."
            },
            "incorrect": {
                "message": "Review the values carefully. Sort them mentally to find the extremes and the middle."
            },
            "hints": [
                "Sort the delivery times from smallest to largest to find the extremes and middle values.",
                "The median of 20 values is the average of the 10th and 11th values when sorted."
            ],
            "remediation_step_id": "tile_stats_shape_outliers.s01"
        }
    }
}
interactions.append(interaction_s05)

# Step s07: check - choice - stats.outlier_reasoning
step_id = "tile_stats_shape_outliers.s07"
step = next(s for s in tile_plan['steps'] if s['step_id'] == step_id)

interaction_s07 = {
    "step_id": step_id,
    "interaction": {
        "type": "choice",
        "interaction_id": f"ix.{step_id}",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "stats.outlier_reasoning",
                "capability": "explain_and_decide_outlier_handling",
                "fact_ids": [
                    full_fact_id("stats.outlier_reasoning", "f2"),
                    full_fact_id("stats.outlier_reasoning", "f3"),
                    full_fact_id("stats.outlier_reasoning", "m1")
                ]
            }
        ],
        "anchors": [
            full_anchor_id("stats.outlier_reasoning", "assessment", "explain_and_decide_outlier_handling")
        ],
        "public": {
            "prompt": "You spot a delivery time of 80 minutes in a batch where most deliveries take 18–28 minutes. What should you do first?",
            "options": [
                {
                    "option_id": "opt_examine",
                    "text": "Examine the record to see if it's a data error or a genuine event"
                },
                {
                    "option_id": "opt_delete",
                    "text": "Delete it immediately because it's an outlier"
                },
                {
                    "option_id": "opt_ignore",
                    "text": "Ignore it and calculate statistics without checking"
                },
                {
                    "option_id": "opt_replace",
                    "text": "Replace it with the median value"
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_examine"],
            "option_feedback": {
                "opt_examine": {
                    "message": "Correct. You should examine the outlier to judge whether it's a possible data error or a genuine observation. A genuine outlier should not be removed without a very good reason."
                },
                "opt_delete": {
                    "message": "Not quite. An outlier is not automatically a data error—it may be a genuine, correct observation. You should examine it first before deciding what to do.",
                    "misconception_id": "stats.outlier_reasoning#m1"
                },
                "opt_ignore": {
                    "message": "Not quite. Examining outliers is important: they can reveal data errors, interesting properties, or strong skew in the distribution. You should investigate before proceeding."
                },
                "opt_replace": {
                    "message": "Not quite. Replacing an outlier without examining it first could hide a genuine observation or mask a data error that needs correction. Always investigate first."
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "Exactly. Always examine an outlier before deciding how to handle it."
            },
            "incorrect": {
                "message": "Remember: an outlier might be a genuine observation, not necessarily an error."
            },
            "hints": [
                "Think about what an outlier could represent—is it always an error?",
                "What's the first step before making any decision about unusual data?"
            ],
            "remediation_step_id": "tile_stats_shape_outliers.s06"
        }
    }
}
interactions.append(interaction_s07)

# Step s08: hands_on - find_issues - stats.outlier_reasoning
step_id = "tile_stats_shape_outliers.s08"
step = next(s for s in tile_plan['steps'] if s['step_id'] == step_id)

# Use the outlier variant of ds_delivery_times_sample
interaction_s08 = {
    "step_id": step_id,
    "interaction": {
        "type": "find_issues",
        "interaction_id": f"ix.{step_id}",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "stats.outlier_reasoning",
                "capability": "identify_outlier",
                "fact_ids": [
                    full_fact_id("stats.outlier_reasoning", "f1")
                ]
            },
            {
                "concept_id": "stats.outlier_reasoning",
                "capability": "explain_and_decide_outlier_handling",
                "fact_ids": [
                    full_fact_id("stats.outlier_reasoning", "f2"),
                    full_fact_id("stats.outlier_reasoning", "f3"),
                    full_fact_id("stats.outlier_reasoning", "m1")
                ]
            }
        ],
        "anchors": [
            full_anchor_id("stats.outlier_reasoning", "practice"),
            full_anchor_id("stats.outlier_reasoning", "assessment", "identify_outlier"),
            full_anchor_id("stats.outlier_reasoning", "assessment", "explain_and_decide_outlier_handling")
        ],
        "public": {
            "asset_ref": {
                "asset_id": "ds_delivery_times_sample",
                "variant_id": "ds_delivery_times_sample.outlier",
                "columns": ["order_id", "delivery_minutes"]
            },
            "instructions": "The table shows delivery times for seven orders. Flag any values that appear extreme relative to the rest of the data, and classify each as either a possible data error or a genuine event.",
            "categories": [
                {
                    "category_id": "cat_data_error",
                    "label": "Possible data error"
                },
                {
                    "category_id": "cat_genuine",
                    "label": "Genuine event"
                }
            ],
            "goal_count": 1
        },
        "grading": {
            "issues": [
                {
                    "issue_id": "issue_outlier_80min",
                    "category_id": "cat_data_error",
                    "locations": [
                        {
                            "where": {"order_id": "ORD-009"},
                            "occurrence": 0,
                            "column": "delivery_minutes"
                        }
                    ],
                    "explanation": "The 80-minute delivery is extreme relative to the rest (18–28 minutes). It could be a data-entry error, such as 8.0 typed as 80, or it could be a genuine event like a road closure. You should examine the record to determine which."
                }
            ],
            "decoys": [
                {
                    "location": {
                        "where": {"order_id": "ORD-005"},
                        "occurrence": 0,
                        "column": "delivery_minutes"
                    },
                    "message": "26 minutes is within the typical range (18–28 minutes) and is not an outlier."
                },
                {
                    "location": {
                        "where": {"order_id": "ORD-006"},
                        "occurrence": 0,
                        "column": "delivery_minutes"
                    },
                    "message": "28 minutes is at the upper end of the typical range but is not extreme relative to the rest of the data."
                }
            ],
            "wrong_category_message": "You've identified the outlier, but consider whether it's more likely to be a data error or a genuine event. The explanation should note that both are possible and the record needs examination.",
            "completion_message": "Well done! You've identified the outlier and recognized that it needs examination to determine whether it's an error or a genuine observation."
        },
        "feedback": {
            "correct": {
                "message": "Excellent work. You've identified the extreme value and recognized that it could be either an error or a genuine event."
            },
            "incorrect": {
                "message": "Look for a value that appears extreme relative to the rest of the batch."
            },
            "hints": [
                "An outlier is an observation that appears extreme relative to the rest of the data.",
                "Compare each delivery time to the others. Which one stands out as unusually high or low?"
            ],
            "remediation_step_id": "tile_stats_shape_outliers.s06"
        }
    }
}
interactions.append(interaction_s08)

# Step s12: check - choice - stats.frequency_distribution_reading
step_id = "tile_stats_shape_outliers.s12"
step = next(s for s in tile_plan['steps'] if s['step_id'] == step_id)

interaction_s12 = {
    "step_id": step_id,
    "interaction": {
        "type": "choice",
        "interaction_id": f"ix.{step_id}",
        "difficulty": "intro",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "stats.frequency_distribution_reading",
                "capability": "read_frequency_table",
                "fact_ids": [
                    full_fact_id("stats.frequency_distribution_reading", "f3")
                ]
            }
        ],
        "anchors": [
            full_anchor_id("stats.frequency_distribution_reading", "assessment", "read_frequency_table")
        ],
        "public": {
            "prompt": "What is the table of counts of observations in each bin, which a histogram displays as bars, called?",
            "options": [
                {
                    "option_id": "opt_frequency_table",
                    "text": "A frequency table"
                },
                {
                    "option_id": "opt_distribution_table",
                    "text": "A distribution table"
                },
                {
                    "option_id": "opt_bin_table",
                    "text": "A bin table"
                },
                {
                    "option_id": "opt_count_table",
                    "text": "A count table"
                }
            ],
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": ["opt_frequency_table"],
            "option_feedback": {
                "opt_frequency_table": {
                    "message": "Correct. The table of counts of observations in each bin is called a frequency table."
                },
                "opt_distribution_table": {
                    "message": "Not quite. While the table does show the distribution of values, the specific term for the table of counts in each bin is 'frequency table.'"
                },
                "opt_bin_table": {
                    "message": "Not quite. While the table does organize data into bins, the standard term for the table of counts in each bin is 'frequency table.'"
                },
                "opt_count_table": {
                    "message": "Not quite. While the table does show counts, the standard term for the table of counts in each bin is 'frequency table.'"
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "Exactly right. A frequency table shows the count of observations in each bin."
            },
            "incorrect": {
                "message": "Think about the standard statistical term for a table that shows how frequently values appear in each bin."
            },
            "hints": [
                "The term relates to how frequently observations appear in each bin.",
                "This is a standard term in statistics for tables that show counts by category or bin."
            ],
            "remediation_step_id": "tile_stats_shape_outliers.s09"
        }
    }
}
interactions.append(interaction_s12)

# Step s13: hands_on - table_select - stats.frequency_distribution_reading
step_id = "tile_stats_shape_outliers.s13"
step = next(s for s in tile_plan['steps'] if s['step_id'] == step_id)

interaction_s13 = {
    "step_id": step_id,
    "interaction": {
        "type": "table_select",
        "interaction_id": f"ix.{step_id}",
        "difficulty": "core",
        "grading_mode": "client",
        "standalone": False,
        "measures": [
            {
                "concept_id": "stats.frequency_distribution_reading",
                "capability": "read_bar_height_as_count",
                "fact_ids": [
                    full_fact_id("stats.frequency_distribution_reading", "f1")
                ]
            },
            {
                "concept_id": "stats.frequency_distribution_reading",
                "capability": "identify_modal_range",
                "fact_ids": [
                    full_fact_id("stats.frequency_distribution_reading", "f2")
                ]
            },
            {
                "concept_id": "stats.frequency_distribution_reading",
                "capability": "read_frequency_table",
                "fact_ids": [
                    full_fact_id("stats.frequency_distribution_reading", "f3")
                ]
            }
        ],
        "anchors": [
            full_anchor_id("stats.frequency_distribution_reading", "practice"),
            full_anchor_id("stats.frequency_distribution_reading", "assessment", "read_bar_height_as_count"),
            full_anchor_id("stats.frequency_distribution_reading", "assessment", "identify_modal_range"),
            full_anchor_id("stats.frequency_distribution_reading", "assessment", "read_frequency_table")
        ],
        "public": {
            "asset_ref": {
                "asset_id": "ds_delivery_frequency_table",
                "variant_id": None,
                "columns": ["bin_label", "order_count"]
            },
            "intro": "The frequency table shows delivery times grouped into bins, with the count of orders in each bin.",
            "tasks": [
                {
                    "task_id": "task_modal_bin",
                    "prompt": "Select the row with the modal bin (the bin with the most observations).",
                    "target_kind": "row"
                },
                {
                    "task_id": "task_modal_count",
                    "prompt": "Select the cell showing how many orders are in the modal bin.",
                    "target_kind": "cell"
                },
                {
                    "task_id": "task_empty_bin",
                    "prompt": "Select the row with a bin that has zero orders.",
                    "target_kind": "row"
                }
            ]
        },
        "grading": {
            "answers": [
                {
                    "task_id": "task_modal_bin",
                    "row": {
                        "where": {"bin_label": "20–30 min"},
                        "occurrence": 0
                    },
                    "column": "order_count",
                    "expect_value": 9
                },
                {
                    "task_id": "task_modal_count",
                    "row": {
                        "where": {"bin_label": "20–30 min"},
                        "occurrence": 0
                    },
                    "column": "order_count",
                    "expect_value": 9
                },
                {
                    "task_id": "task_empty_bin",
                    "row": {
                        "where": {"bin_label": "50–80 min"},
                        "occurrence": 0
                    },
                    "column": "order_count",
                    "expect_value": 0
                }
            ],
            "task_feedback": {
                "task_modal_bin": {
                    "correct": "Correct. The 20–30 min bin has 9 orders, the highest count, making it the modal bin.",
                    "incorrect": "Not quite. Look for the bin with the highest order count—that's the mode."
                },
                "task_modal_count": {
                    "correct": "Correct. The modal bin has 9 orders.",
                    "incorrect": "Not quite. Find the bin with the most orders and select the cell showing that count."
                },
                "task_empty_bin": {
                    "correct": "Correct. The 50–80 min bin has zero orders.",
                    "incorrect": "Not quite. Look for a bin where the order count is 0."
                }
            }
        },
        "feedback": {
            "correct": {
                "message": "Excellent! You've read the frequency table correctly and identified the modal bin and the empty bin."
            },
            "incorrect": {
                "message": "Review the order counts in each bin. The mode is where the count is highest."
            },
            "hints": [
                "The modal bin is the one with the tallest bar in a histogram—the highest count in the table.",
                "Look at the order_count column to find the highest value and the zero value."
            ],
            "remediation_step_id": "tile_stats_shape_outliers.s09"
        }
    }
}
interactions.append(interaction_s13)

# Build the output structure
output = {
    "schema_version": "1.0.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_003_da_chunk",
    "tiles": [
        {
            "tile_id": "tile_stats_shape_outliers",
            "interactions": interactions
        }
    ]
}

# Write the output
with open('interactions.part.c0_canary.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"Generated {len(interactions)} interactions for tile_stats_shape_outliers")
print(f"Interactions: {[ix['step_id'] for ix in interactions]}")
