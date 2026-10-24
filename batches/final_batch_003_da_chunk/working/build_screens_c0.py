"""
Build screens.part.c0_canary.json for tile_stats_shape_outliers.
"""
import json

BATCH_ID = "final_batch_003_da_chunk"
PATH_ID = "data_analyst"

# ── helpers ──────────────────────────────────────────────────────────────────

def qid(concept_id, suffix):
    """Qualified id: concept_id#suffix"""
    return f"{concept_id}#{suffix}"


# ── tile ─────────────────────────────────────────────────────────────────────

tile = {
    "tile_id": "tile_stats_shape_outliers",
    "title": "Distribution Shape, Outliers, and Frequency Distributions",
    "summary": (
        "Learn to read a distribution's shape as right-skewed, left-skewed, or symmetric; "
        "reason about outliers; and translate a frequency table into statements about where "
        "delivery times cluster and where rare values sit."
    ),
    "steps": [],
    "remediation_steps": []
}

steps = tile["steps"]
rem   = tile["remediation_steps"]

# ── s01: explainer — distribution_shape tb1+tb2, f1, visual=chart ────────────
steps.append({
    "step_id": "tile_stats_shape_outliers.s01",
    "type": "explainer",
    "concept_ids": ["stats.distribution_shape"],
    "eyebrow": "Distribution Shape",
    "title": "Which way does the tail point?",
    "lede": (
        "Most delivery times cluster in a narrow band — but a few orders take much longer. "
        "The direction that long stretch points is what analysts call the shape of a distribution."
    ),
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stats_shape_outliers.s01.b1",
            "role": "intro",
            "text": (
                "Consider nine QuickShip delivery times: 18, 20, 22, 22, 26, 28, 34, 41, 52 minutes. "
                "Most orders finish between 18 and 28 minutes, but the remaining values climb gradually "
                "toward 52. That overall pattern — where the bulk of the values sit and which direction "
                "the data trails off toward — is what analysts call the shape of a distribution."
            ),
            "lineage": {
                "concept_ids": ["stats.distribution_shape"],
                "teaching_block_ids": [qid("stats.distribution_shape", "tb1")],
                "fact_ids": []
            }
        },
        {
            "type": "prose",
            "block_id": "tile_stats_shape_outliers.s01.b2",
            "role": "definition",
            "text": (
                "A distribution is right-skewed when it has a longer tail trailing off to the right, "
                "and left-skewed when it has a longer tail trailing off to the left. "
                "This delivery-time batch is right-skewed: the bulk of the values sit between 18 and 28 minutes, "
                "and 34, 41, and 52 form a gradually lengthening tail trailing off to the right."
            ),
            "lineage": {
                "concept_ids": ["stats.distribution_shape"],
                "teaching_block_ids": [qid("stats.distribution_shape", "tb2")],
                "fact_ids": [qid("stats.distribution_shape", "f1")]
            }
        },
        {
            # Visual: three side-by-side histograms (right-skewed, left-skewed, symmetric)
            # using ds_delivery_times_sample for the right-skewed panel
            "type": "chart",
            "block_id": "tile_stats_shape_outliers.s01.b3",
            "chart_kind": "bar",
            "asset_ref": {
                "asset_id": "ds_delivery_times_sample",
                "variant_id": None,
                "columns": ["delivery_minutes"]
            },
            "title": "Right-skewed, left-skewed, and symmetric distributions side by side",
            "alt_text": (
                "Three bar charts placed side by side. The left chart shows the QuickShip delivery-time "
                "sample with bars tallest at 18–28 min and a long tail trailing right — labelled "
                "Right-skewed. The centre chart mirrors this with the tail trailing left — labelled "
                "Left-skewed. The right chart shows bars of roughly equal height on both sides of the "
                "centre — labelled Symmetric. Each chart has an arrow marking the long tail."
            ),
            "encoding": {
                "x": {"field": "delivery_minutes", "type": "quantitative", "title": "Delivery time (min)"},
                "y": {"field": "delivery_minutes", "type": "quantitative", "aggregate": "count", "title": "Count"}
            },
            "annotations": [
                {"text": "Long tail → right-skewed", "target": "tail_right"},
                {"text": "Long tail → left-skewed",  "target": "tail_left"},
                {"text": "Roughly equal both sides → symmetric", "target": "symmetric"}
            ],
            "lineage": {
                "concept_ids": ["stats.distribution_shape"],
                "teaching_block_ids": [
                    qid("stats.distribution_shape", "tb1"),
                    qid("stats.distribution_shape", "tb2")
                ],
                "fact_ids": [qid("stats.distribution_shape", "f1")],
                "anchors": [qid("stats.distribution_shape", "visual")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": ["stats.distribution_shape"],
        "teaching_block_ids": [
            qid("stats.distribution_shape", "tb1"),
            qid("stats.distribution_shape", "tb2")
        ],
        "fact_ids": [qid("stats.distribution_shape", "f1")]
    }
})

# ── s02: explainer — distribution_shape tb3+tb4, f2+f3 ───────────────────────
steps.append({
    "step_id": "tile_stats_shape_outliers.s02",
    "type": "explainer",
    "concept_ids": ["stats.distribution_shape"],
    "eyebrow": "Distribution Shape",
    "title": "Symmetric distributions and what skew does to the mean",
    "lede": (
        "When a distribution has no long tail, the mean and median sit close together. "
        "A skewed tail pulls the mean away from the median."
    ),
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stats_shape_outliers.s02.b1",
            "role": "definition",
            "text": (
                "A distribution is symmetric when it trails off by roughly equal amounts in both directions. "
                "If the delivery-time batch had values spread evenly above and below its centre — "
                "some orders a bit faster and some a bit slower than 24 minutes, with no single value "
                "trailing far off in either direction — that would be a symmetric distribution."
            ),
            "lineage": {
                "concept_ids": ["stats.distribution_shape"],
                "teaching_block_ids": [qid("stats.distribution_shape", "tb3")],
                "fact_ids": [qid("stats.distribution_shape", "f2")]
            }
        },
        {
            "type": "prose",
            "block_id": "tile_stats_shape_outliers.s02.b2",
            "role": "mechanism",
            "text": (
                "The mean is more affected by extreme observations — such as those in the long tail of a "
                "skewed distribution — than the median, which is more robust to them. "
                "In the right-skewed delivery-time batch, the mean (about 29.2 minutes) sits above the "
                "median (26 minutes), pulled upward by the gradual right-hand tail."
            ),
            "lineage": {
                "concept_ids": ["stats.distribution_shape"],
                "teaching_block_ids": [qid("stats.distribution_shape", "tb4")],
                "fact_ids": [qid("stats.distribution_shape", "f3")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": ["stats.distribution_shape"],
        "teaching_block_ids": [
            qid("stats.distribution_shape", "tb3"),
            qid("stats.distribution_shape", "tb4")
        ],
        "fact_ids": [
            qid("stats.distribution_shape", "f2"),
            qid("stats.distribution_shape", "f3")
        ]
    }
})

# ── s03: video — distribution_shape ──────────────────────────────────────────
steps.append({
    "step_id": "tile_stats_shape_outliers.s03",
    "type": "video",
    "concept_ids": ["stats.distribution_shape"],
    "eyebrow": "Distribution Shape",
    "title": "Symmetric, left-skewed and right-skewed distributions",
    "lede": "Watch how the direction the long tail points — not where the tall bars sit — names the skew.",
    "blocks": [
        {
            "type": "media_group",
            "block_id": "tile_stats_shape_outliers.s03.b1",
            "group_title": "Telling symmetric, left-skewed and right-skewed apart",
            "segment_ids": ["seg_stats.distribution_shape_Y53_8WRrPzg_0_149"],
            "segments": [
                {
                    "segment_id": "seg_stats.distribution_shape_Y53_8WRrPzg_0_149",
                    "video_id": "Y53_8WRrPzg",
                    "youtube_url": "https://www.youtube.com/watch?v=Y53_8WRrPzg",
                    "review_url": "https://www.youtube.com/watch?v=Y53_8WRrPzg&t=0s",
                    "start_seconds": 0,
                    "end_seconds": 149,
                    "label": "Symmetric, left-skewed and right-skewed distributions told apart by which way the tail trails",
                    "summary": (
                        "Shows three of six example charts and names each shape. Housefly lengths form a "
                        "symmetric distribution: a line down the middle gives two mirror-image halves, and "
                        "real data is usually only roughly symmetric. Dates on pennies have a long tail to "
                        "the left with the high points on the right, so the distribution is left-skewed. "
                        "Representatives per state have most values low and a tail stretching right, so it "
                        "is right-skewed. The narrator reads the bars out loud, so no earlier chart-reading "
                        "is needed. The clip stops before any link between shape and the mean or median."
                    ),
                    "fact_ids": [
                        qid("stats.distribution_shape", "f1"),
                        qid("stats.distribution_shape", "f2")
                    ],
                    "transcript_ref": "Y53_8WRrPzg:0-149"
                }
            ],
            "bridge": {
                "before": "Watch how the side the long tail points to, not where the tall bars sit, names the skew. The clip's examples are bar charts of counts; Devspace's text works from lists of values instead.",
                "after": "The clip never links shape to the mean and median. The text fills that gap: a long tail pulls the mean toward it, away from the median."
            },
            "default_mode": "video"
        }
    ],
    "reward": {"gems": 0},
    "lineage": {
        "concept_ids": ["stats.distribution_shape"],
        "teaching_block_ids": [],
        "fact_ids": [
            qid("stats.distribution_shape", "f1"),
            qid("stats.distribution_shape", "f2")
        ],
        "segment_ids": ["seg_stats.distribution_shape_Y53_8WRrPzg_0_149"]
    }
})

# ── s04: check — distribution_shape, framing only ────────────────────────────
steps.append({
    "step_id": "tile_stats_shape_outliers.s04",
    "type": "check",
    "concept_ids": ["stats.distribution_shape"],
    "eyebrow": "Quick Check",
    "title": "Skew and the mean vs. median",
    "lede": (
        "A delivery-time dataset has a long tail trailing to the right. "
        "How does that affect the mean compared with the median?"
    ),
    "reward": {"gems": 10, "first_try_bonus": 5},
    "lineage": {
        "concept_ids": ["stats.distribution_shape"],
        "teaching_block_ids": [],
        "fact_ids": [
            qid("stats.distribution_shape", "f1"),
            qid("stats.distribution_shape", "f3")
        ],
        "anchors": [qid("stats.distribution_shape", "assessment:relate_skew_to_mean_versus_median")]
    }
})

# ── s05: hands_on — distribution_shape, framing only ─────────────────────────
steps.append({
    "step_id": "tile_stats_shape_outliers.s05",
    "type": "hands_on",
    "concept_ids": ["stats.distribution_shape"],
    "eyebrow": "Hands-On Practice",
    "title": "Classify the shape of a delivery-time distribution",
    "lede": (
        "Look at the QuickShip delivery-time sample. "
        "Decide whether the distribution is right-skewed, left-skewed, or symmetric, "
        "and say whether the mean should sit above or below the median."
    ),
    "reward": {"gems": 15, "first_try_bonus": 5},
    "lineage": {
        "concept_ids": ["stats.distribution_shape"],
        "teaching_block_ids": [],
        "fact_ids": [
            qid("stats.distribution_shape", "f1"),
            qid("stats.distribution_shape", "f2"),
            qid("stats.distribution_shape", "f3")
        ],
        "anchors": [
            qid("stats.distribution_shape", "practice"),
            qid("stats.distribution_shape", "assessment:classify_skew_direction"),
            qid("stats.distribution_shape", "assessment:recognize_symmetric_distribution"),
            qid("stats.distribution_shape", "assessment:relate_skew_to_mean_versus_median")
        ]
    }
})

# ── s06: explainer — outlier_reasoning tb1–tb4, f1+f2+f3+m1, visual=data_table
steps.append({
    "step_id": "tile_stats_shape_outliers.s06",
    "type": "explainer",
    "concept_ids": ["stats.outlier_reasoning"],
    "eyebrow": "Outlier Reasoning",
    "title": "Spotting an outlier and deciding what to do with it",
    "lede": (
        "One delivery in the batch took 80 minutes — far beyond the rest. "
        "Spotting it is only the first step; reasoning about why it's there is what matters."
    ),
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stats_shape_outliers.s06.b1",
            "role": "intro",
            "text": (
                "In a seven-order delivery batch — 18, 20, 22, 22, 26, 28, 80 minutes — "
                "that 80-minute order stands out from the rest. "
                "An outlier is an observation that appears extreme relative to the rest of the data, "
                "and that single delivery clearly qualifies."
            ),
            "lineage": {
                "concept_ids": ["stats.outlier_reasoning"],
                "teaching_block_ids": [qid("stats.outlier_reasoning", "tb1")],
                "fact_ids": [qid("stats.outlier_reasoning", "f1")]
            }
        },
        {
            "type": "prose",
            "block_id": "tile_stats_shape_outliers.s06.b2",
            "role": "mechanism",
            "text": (
                "Examining a dataset for outliers can help identify strong skew in the distribution, "
                "spot possible data collection or data entry errors, and reveal interesting properties "
                "of the data. For that 80-minute order, this could mean noticing the skew it creates, "
                "checking whether someone mistyped \"8.0\" as \"80,\" or discovering something genuinely "
                "unusual — like the delivery being stuck behind a road closure."
            ),
            "lineage": {
                "concept_ids": ["stats.outlier_reasoning"],
                "teaching_block_ids": [qid("stats.outlier_reasoning", "tb2")],
                "fact_ids": [qid("stats.outlier_reasoning", "f2")]
            }
        },
        {
            "type": "prose",
            "block_id": "tile_stats_shape_outliers.s06.b3",
            "role": "mechanism",
            "text": (
                "Examine an outlier to judge whether it is a possible data collection or data entry error "
                "or a genuine observation; a genuine outlier should not be removed without a very good reason. "
                "That means checking the order record itself — was 80 actually logged, or should it have "
                "been 8.0? — before deciding what to do about it."
            ),
            "lineage": {
                "concept_ids": ["stats.outlier_reasoning"],
                "teaching_block_ids": [qid("stats.outlier_reasoning", "tb3")],
                "fact_ids": [qid("stats.outlier_reasoning", "f3")]
            }
        },
        {
            "type": "prose",
            "block_id": "tile_stats_shape_outliers.s06.b4",
            "role": "misconception",
            "text": (
                "An outlier is not automatically a data error: it may instead be a genuine, correct "
                "observation. If the driver really did take 80 minutes because of a road closure, "
                "that is real information about that specific delivery — not something to delete just "
                "because the value looks unusual next to the rest of the batch."
            ),
            "lineage": {
                "concept_ids": ["stats.outlier_reasoning"],
                "teaching_block_ids": [qid("stats.outlier_reasoning", "tb4")],
                "fact_ids": [qid("stats.outlier_reasoning", "m1")]
            }
        },
        {
            # Visual: data_table showing the outlier variant with the 80-min row highlighted
            "type": "data_table",
            "block_id": "tile_stats_shape_outliers.s06.b5",
            "asset_ref": {
                "asset_id": "ds_delivery_times_sample",
                "variant_id": "ds_delivery_times_sample.outlier",
                "columns": ["order_id", "delivery_minutes"]
            },
            "caption": (
                "Seven QuickShip delivery records. The 80-minute order (ORD-009) is highlighted — "
                "it stands out from the 18–28 minute cluster and warrants investigation before any decision."
            ),
            "highlight": [
                {
                    "target": {
                        "kind": "row",
                        "row": {"where": {"order_id": "ORD-009"}}
                    },
                    "label": "Extreme value — investigate before acting",
                    "tone": "focus"
                }
            ],
            "inspect": {
                "enabled": True,
                "id_column": "order_id"
            },
            "lineage": {
                "concept_ids": ["stats.outlier_reasoning"],
                "teaching_block_ids": [
                    qid("stats.outlier_reasoning", "tb1"),
                    qid("stats.outlier_reasoning", "tb2"),
                    qid("stats.outlier_reasoning", "tb3"),
                    qid("stats.outlier_reasoning", "tb4")
                ],
                "fact_ids": [
                    qid("stats.outlier_reasoning", "f1"),
                    qid("stats.outlier_reasoning", "f2"),
                    qid("stats.outlier_reasoning", "f3"),
                    qid("stats.outlier_reasoning", "m1")
                ],
                "anchors": [qid("stats.outlier_reasoning", "visual")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": ["stats.outlier_reasoning"],
        "teaching_block_ids": [
            qid("stats.outlier_reasoning", "tb1"),
            qid("stats.outlier_reasoning", "tb2"),
            qid("stats.outlier_reasoning", "tb3"),
            qid("stats.outlier_reasoning", "tb4")
        ],
        "fact_ids": [
            qid("stats.outlier_reasoning", "f1"),
            qid("stats.outlier_reasoning", "f2"),
            qid("stats.outlier_reasoning", "f3"),
            qid("stats.outlier_reasoning", "m1")
        ]
    }
})

# ── s07: check — outlier_reasoning, framing only ─────────────────────────────
steps.append({
    "step_id": "tile_stats_shape_outliers.s07",
    "type": "check",
    "concept_ids": ["stats.outlier_reasoning"],
    "eyebrow": "Quick Check",
    "title": "What should you do with an outlier?",
    "lede": (
        "A delivery record shows 80 minutes — far beyond the rest of the batch. "
        "What is the right first action?"
    ),
    "reward": {"gems": 10, "first_try_bonus": 5},
    "lineage": {
        "concept_ids": ["stats.outlier_reasoning"],
        "teaching_block_ids": [],
        "fact_ids": [
            qid("stats.outlier_reasoning", "f2"),
            qid("stats.outlier_reasoning", "f3"),
            qid("stats.outlier_reasoning", "m1")
        ],
        "anchors": [qid("stats.outlier_reasoning", "assessment:explain_and_decide_outlier_handling")]
    }
})

# ── s08: hands_on — outlier_reasoning, framing only ──────────────────────────
steps.append({
    "step_id": "tile_stats_shape_outliers.s08",
    "type": "hands_on",
    "concept_ids": ["stats.outlier_reasoning"],
    "eyebrow": "Hands-On Practice",
    "title": "Find and reason about the outlier in the delivery dataset",
    "lede": (
        "Scan the QuickShip delivery records. Mark the extreme value, "
        "then choose whether to keep, investigate, or exclude it — and explain why."
    ),
    "reward": {"gems": 15, "first_try_bonus": 5},
    "lineage": {
        "concept_ids": ["stats.outlier_reasoning"],
        "teaching_block_ids": [],
        "fact_ids": [
            qid("stats.outlier_reasoning", "f1"),
            qid("stats.outlier_reasoning", "f2"),
            qid("stats.outlier_reasoning", "f3"),
            qid("stats.outlier_reasoning", "m1")
        ],
        "anchors": [
            qid("stats.outlier_reasoning", "practice"),
            qid("stats.outlier_reasoning", "assessment:identify_outlier"),
            qid("stats.outlier_reasoning", "assessment:explain_and_decide_outlier_handling")
        ]
    }
})

# ── s09: explainer — frequency_distribution_reading tb1–tb3, f1+f3, visual=chart
steps.append({
    "step_id": "tile_stats_shape_outliers.s09",
    "type": "explainer",
    "concept_ids": ["stats.frequency_distribution_reading"],
    "eyebrow": "Frequency Distributions",
    "title": "From a list of times to a histogram and frequency table",
    "lede": (
        "Instead of listing every delivery time one by one, group them into ranges "
        "and count how many orders fall into each range."
    ),
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stats_shape_outliers.s09.b1",
            "role": "intro",
            "text": (
                "Instead of listing every delivery time one by one, imagine grouping a full day's "
                "21 QuickShip deliveries into 10-minute ranges and counting how many orders fall "
                "into each range. That grouping turns a long list into a compact summary."
            ),
            "lineage": {
                "concept_ids": ["stats.frequency_distribution_reading"],
                "teaching_block_ids": [qid("stats.frequency_distribution_reading", "tb1")],
                "fact_ids": []
            }
        },
        {
            "type": "prose",
            "block_id": "tile_stats_shape_outliers.s09.b2",
            "role": "definition",
            "text": (
                "A histogram groups numerical values into bins and represents the count of observations "
                "in each bin as a bar; taller bars show where the data values are relatively more common. "
                "For the day's 21 deliveries, the tallest bar sits over the 20–30 minute bin, "
                "and a much shorter bar sits far out over the 80–90 minute bin."
            ),
            "lineage": {
                "concept_ids": ["stats.frequency_distribution_reading"],
                "teaching_block_ids": [qid("stats.frequency_distribution_reading", "tb2")],
                "fact_ids": [qid("stats.frequency_distribution_reading", "f1")]
            }
        },
        {
            "type": "prose",
            "block_id": "tile_stats_shape_outliers.s09.b3",
            "role": "mechanism",
            "text": (
                "The table of counts of observations in each bin, which a histogram displays as bars, "
                "is called a frequency table. For that same day: 10–20 min, 4 orders; "
                "20–30 min, 9 orders; 30–40 min, 5 orders; 40–50 min, 2 orders; "
                "50–80 min, 0 orders; 80–90 min, 1 order."
            ),
            "lineage": {
                "concept_ids": ["stats.frequency_distribution_reading"],
                "teaching_block_ids": [qid("stats.frequency_distribution_reading", "tb3")],
                "fact_ids": [qid("stats.frequency_distribution_reading", "f3")]
            }
        },
        {
            # Visual: chart (histogram) from ds_delivery_frequency_table
            "type": "chart",
            "block_id": "tile_stats_shape_outliers.s09.b4",
            "chart_kind": "bar",
            "asset_ref": {
                "asset_id": "ds_delivery_frequency_table",
                "variant_id": None,
                "columns": ["bin_label", "order_count"]
            },
            "title": "Frequency table and histogram of 21 QuickShip delivery times",
            "alt_text": (
                "A bar chart with delivery-time bins on the horizontal axis (10–20 min, 20–30 min, "
                "30–40 min, 40–50 min, 50–80 min, 80–90 min) and order count on the vertical axis. "
                "The tallest bar is 20–30 min with 9 orders, marked as the peak. "
                "The 80–90 min bar is very short (1 order), showing the far-out delivery."
            ),
            "encoding": {
                "x": {"field": "bin_label", "type": "ordinal", "title": "Delivery-time bin"},
                "y": {"field": "order_count", "type": "quantitative", "title": "Number of orders"}
            },
            "annotations": [
                {"text": "Peak: 9 orders (modal bin)", "target": "20–30 min"},
                {"text": "Far-out delivery", "target": "80–90 min"}
            ],
            "lineage": {
                "concept_ids": ["stats.frequency_distribution_reading"],
                "teaching_block_ids": [
                    qid("stats.frequency_distribution_reading", "tb2"),
                    qid("stats.frequency_distribution_reading", "tb3")
                ],
                "fact_ids": [
                    qid("stats.frequency_distribution_reading", "f1"),
                    qid("stats.frequency_distribution_reading", "f3")
                ],
                "anchors": [qid("stats.frequency_distribution_reading", "visual")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": ["stats.frequency_distribution_reading"],
        "teaching_block_ids": [
            qid("stats.frequency_distribution_reading", "tb1"),
            qid("stats.frequency_distribution_reading", "tb2"),
            qid("stats.frequency_distribution_reading", "tb3")
        ],
        "fact_ids": [
            qid("stats.frequency_distribution_reading", "f1"),
            qid("stats.frequency_distribution_reading", "f3")
        ]
    }
})

# ── s10: video — frequency_distribution_reading ───────────────────────────────
steps.append({
    "step_id": "tile_stats_shape_outliers.s10",
    "type": "video",
    "concept_ids": ["stats.frequency_distribution_reading"],
    "eyebrow": "Frequency Distributions",
    "title": "From stacked measurements to a frequency table and histogram",
    "lede": "Watch how measurements are grouped into bins and stacked into bars, then turned into a histogram from a frequency table.",
    "blocks": [
        {
            "type": "media_group",
            "block_id": "tile_stats_shape_outliers.s10.b1",
            "group_title": "From stacked measurements to a frequency table and histogram",
            "segment_ids": [
                "seg_stats.frequency_distribution_reading_qBigTkBLU6g_34_92",
                "seg_stats.frequency_distribution_reading_AndS0RLdxtk_195_417"
            ],
            "segments": [
                {
                    "segment_id": "seg_stats.frequency_distribution_reading_qBigTkBLU6g_34_92",
                    "video_id": "qBigTkBLU6g",
                    "youtube_url": "https://www.youtube.com/watch?v=qBigTkBLU6g",
                    "review_url": "https://www.youtube.com/watch?v=qBigTkBLU6g&t=34s",
                    "start_seconds": 34,
                    "end_seconds": 92,
                    "label": "How a histogram is built: measurements grouped into bins and stacked into bars",
                    "summary": (
                        "An animated explanation of why histograms exist. Measurements of height pile up "
                        "as dots until they overlap and hide each other. Stacking only identical values "
                        "doesn't help much, so the range of values is divided into bins and the measurements "
                        "in each bin are stacked. The result is a histogram, where a taller stack means more "
                        "measurements fell into that bin."
                    ),
                    "fact_ids": [qid("stats.frequency_distribution_reading", "f1")],
                    "transcript_ref": "qBigTkBLU6g:34-92"
                },
                {
                    "segment_id": "seg_stats.frequency_distribution_reading_AndS0RLdxtk_195_417",
                    "video_id": "AndS0RLdxtk",
                    "youtube_url": "https://www.youtube.com/watch?v=AndS0RLdxtk",
                    "review_url": "https://www.youtube.com/watch?v=AndS0RLdxtk&t=195s",
                    "start_seconds": 195,
                    "end_seconds": 417,
                    "label": "From a frequency table to a histogram: drawing the bars and reading the mode",
                    "summary": (
                        "Starts from a finished frequency table of test scores grouped into ranges and turns "
                        "it into a histogram on a whiteboard: score ranges go along the bottom, counts go up "
                        "the side, and the bars touch with no gaps. Bar heights follow the table, from 1 in "
                        "the lowest range up to 5 in the 80s. The presenter then reads the shape, a long tail "
                        "on the left, so skewed left, and says the mode is the range with the highest "
                        "frequency, here 80 to 89. A mix-up over which axis holds what is corrected on the spot."
                    ),
                    "fact_ids": [
                        qid("stats.frequency_distribution_reading", "f1"),
                        qid("stats.frequency_distribution_reading", "f2"),
                        qid("stats.frequency_distribution_reading", "f3")
                    ],
                    "transcript_ref": "AndS0RLdxtk:195-417"
                }
            ],
            "bridge": {
                "before": "Clip 1 shows bins and stacking; clip 2 turns a frequency table into bars and reads the peak. Clip 2 calls the table a 'frequency distribution table' and says 'negative skew' for left-skewed.",
                "after": "Clip 1 covers only bins and bars; clip 2 adds the frequency table and the mode as the highest-count range. Devspace's text also allows a peak that spans several neighbouring bins."
            },
            "default_mode": "video"
        }
    ],
    "reward": {"gems": 0},
    "lineage": {
        "concept_ids": ["stats.frequency_distribution_reading"],
        "teaching_block_ids": [],
        "fact_ids": [
            qid("stats.frequency_distribution_reading", "f1"),
            qid("stats.frequency_distribution_reading", "f2"),
            qid("stats.frequency_distribution_reading", "f3")
        ],
        "segment_ids": [
            "seg_stats.frequency_distribution_reading_qBigTkBLU6g_34_92",
            "seg_stats.frequency_distribution_reading_AndS0RLdxtk_195_417"
        ]
    }
})

# ── s11: explainer — frequency_distribution_reading tb4, f2 ──────────────────
steps.append({
    "step_id": "tile_stats_shape_outliers.s11",
    "type": "explainer",
    "concept_ids": ["stats.frequency_distribution_reading"],
    "eyebrow": "Frequency Distributions",
    "title": "Reading the modal bin",
    "lede": "The tallest bar in a histogram marks the range where observations are most concentrated.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stats_shape_outliers.s11.b1",
            "role": "mechanism",
            "text": (
                "A mode appears in a histogram as a prominent peak: a bin, or region of neighbouring bins, "
                "where observations are noticeably more concentrated than elsewhere. "
                "In the 21-order frequency table, the 20–30 minute bin — with 9 of the 21 orders — is that peak."
            ),
            "lineage": {
                "concept_ids": ["stats.frequency_distribution_reading"],
                "teaching_block_ids": [qid("stats.frequency_distribution_reading", "tb4")],
                "fact_ids": [qid("stats.frequency_distribution_reading", "f2")]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": ["stats.frequency_distribution_reading"],
        "teaching_block_ids": [qid("stats.frequency_distribution_reading", "tb4")],
        "fact_ids": [qid("stats.frequency_distribution_reading", "f2")]
    }
})

# ── s12: check — frequency_distribution_reading, framing only ────────────────
steps.append({
    "step_id": "tile_stats_shape_outliers.s12",
    "type": "check",
    "concept_ids": ["stats.frequency_distribution_reading"],
    "eyebrow": "Quick Check",
    "title": "Reading a frequency table",
    "lede": (
        "A frequency table shows: 10–20 min: 4 orders; 20–30 min: 9 orders; 30–40 min: 5 orders; "
        "40–50 min: 2 orders; 80–90 min: 1 order. "
        "Which bin has the most orders?"
    ),
    "reward": {"gems": 10, "first_try_bonus": 5},
    "lineage": {
        "concept_ids": ["stats.frequency_distribution_reading"],
        "teaching_block_ids": [],
        "fact_ids": [qid("stats.frequency_distribution_reading", "f3")],
        "anchors": [qid("stats.frequency_distribution_reading", "assessment:read_frequency_table")]
    }
})

# ── s13: hands_on — frequency_distribution_reading, framing only ─────────────
steps.append({
    "step_id": "tile_stats_shape_outliers.s13",
    "type": "hands_on",
    "concept_ids": ["stats.frequency_distribution_reading"],
    "eyebrow": "Hands-On Practice",
    "title": "Read the delivery-time frequency table",
    "lede": (
        "Use the QuickShip frequency table to name the modal bin, describe the spread, "
        "and say whether the shape is skewed."
    ),
    "reward": {"gems": 15, "first_try_bonus": 5},
    "lineage": {
        "concept_ids": ["stats.frequency_distribution_reading"],
        "teaching_block_ids": [],
        "fact_ids": [
            qid("stats.frequency_distribution_reading", "f1"),
            qid("stats.frequency_distribution_reading", "f2"),
            qid("stats.frequency_distribution_reading", "f3")
        ],
        "anchors": [
            qid("stats.frequency_distribution_reading", "practice"),
            qid("stats.frequency_distribution_reading", "assessment:read_bar_height_as_count"),
            qid("stats.frequency_distribution_reading", "assessment:identify_modal_range"),
            qid("stats.frequency_distribution_reading", "assessment:read_frequency_table")
        ]
    }
})

# ── s14: recap ────────────────────────────────────────────────────────────────
steps.append({
    "step_id": "tile_stats_shape_outliers.s14",
    "type": "recap",
    "concept_ids": [
        "stats.distribution_shape",
        "stats.outlier_reasoning",
        "stats.frequency_distribution_reading"
    ],
    "eyebrow": "Recap",
    "title": "What you've learned",
    "lede": "Three ideas that let you describe any batch of numbers at a glance.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stats_shape_outliers.s14.b1",
            "role": "takeaway",
            "text": (
                "A distribution's shape — right-skewed, left-skewed, or symmetric — describes which "
                "direction the data trails off. A long tail pulls the mean toward it, away from the "
                "median. An outlier is an extreme observation: investigate it before acting, because "
                "it may be a genuine event rather than an error. A frequency table or histogram "
                "translates raw counts into a picture of where deliveries cluster and where rare "
                "values sit."
            ),
            "lineage": {
                "concept_ids": [
                    "stats.distribution_shape",
                    "stats.outlier_reasoning",
                    "stats.frequency_distribution_reading"
                ],
                "teaching_block_ids": [
                    qid("stats.distribution_shape", "tb5"),
                    qid("stats.outlier_reasoning", "tb5"),
                    qid("stats.frequency_distribution_reading", "tb5")
                ],
                "fact_ids": [
                    qid("stats.distribution_shape", "f1"),
                    qid("stats.distribution_shape", "f2"),
                    qid("stats.distribution_shape", "f3"),
                    qid("stats.frequency_distribution_reading", "f1"),
                    qid("stats.frequency_distribution_reading", "f2"),
                    qid("stats.frequency_distribution_reading", "f3"),
                    qid("stats.outlier_reasoning", "f1"),
                    qid("stats.outlier_reasoning", "f3")
                ]
            }
        },
        {
            "type": "up_next",
            "block_id": "tile_stats_shape_outliers.s14.b2",
            "title": "Up next: Correlation and Its Limits",
            "text": (
                "In the next tile you'll ask whether two numeric columns — like distance and delivery "
                "time — tend to move together, and learn how to measure the strength and direction "
                "of that relationship."
            )
        }
    ],
    "reward": {"gems": 10},
    "lineage": {
        "concept_ids": [
            "stats.distribution_shape",
            "stats.outlier_reasoning",
            "stats.frequency_distribution_reading"
        ],
        "teaching_block_ids": [
            qid("stats.distribution_shape", "tb5"),
            qid("stats.outlier_reasoning", "tb5"),
            qid("stats.frequency_distribution_reading", "tb5")
        ],
        "fact_ids": [
            qid("stats.distribution_shape", "f1"),
            qid("stats.distribution_shape", "f2"),
            qid("stats.distribution_shape", "f3"),
            qid("stats.frequency_distribution_reading", "f1"),
            qid("stats.frequency_distribution_reading", "f2"),
            qid("stats.frequency_distribution_reading", "f3"),
            qid("stats.outlier_reasoning", "f1"),
            qid("stats.outlier_reasoning", "f3")
        ]
    }
})

# ── remediation steps ─────────────────────────────────────────────────────────
# Rule 7: one remediation step for the first check/hands_on of each concept.
# First check for distribution_shape = s04; first check for outlier_reasoning = s07;
# first check for frequency_distribution_reading = s12.

rem.append({
    "step_id": "tile_stats_shape_outliers.r01",
    "type": "remediation",
    "concept_ids": ["stats.distribution_shape"],
    "eyebrow": "Let's revisit",
    "title": "Skew direction: a clear contrast",
    "lede": "Compare two delivery batches — one with a tail trailing right, one with a tail trailing left.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stats_shape_outliers.r01.b1",
            "role": "example",
            "text": (
                "Batch A: 18, 20, 22, 22, 26, 28, 34, 41, 52 minutes. "
                "Most values sit at the low end; the tail trails right — right-skewed. "
                "Batch B: 30, 38, 44, 48, 50, 52, 52, 54, 56 minutes. "
                "Most values sit at the high end; the tail trails left — left-skewed. "
                "The tail direction, not where the tall bars sit, names the skew."
            ),
            "lineage": {
                "concept_ids": ["stats.distribution_shape"],
                "teaching_block_ids": [
                    qid("stats.distribution_shape", "tb1"),
                    qid("stats.distribution_shape", "tb2")
                ],
                "fact_ids": [
                    qid("stats.distribution_shape", "f1"),
                    qid("stats.distribution_shape", "f3")
                ]
            }
        }
    ],
    "lineage": {
        "concept_ids": ["stats.distribution_shape"],
        "teaching_block_ids": [
            qid("stats.distribution_shape", "tb1"),
            qid("stats.distribution_shape", "tb2")
        ],
        "fact_ids": [
            qid("stats.distribution_shape", "f1"),
            qid("stats.distribution_shape", "f3")
        ]
    }
})

rem.append({
    "step_id": "tile_stats_shape_outliers.r02",
    "type": "remediation",
    "concept_ids": ["stats.outlier_reasoning"],
    "eyebrow": "Let's revisit",
    "title": "Error vs. genuine event: a clear contrast",
    "lede": "Two 80-minute deliveries — same number, different explanations.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stats_shape_outliers.r02.b1",
            "role": "example",
            "text": (
                "Case 1: The driver's app logged \"80\" but the actual time was 8 minutes — "
                "a data-entry error. Removing it is justified once confirmed. "
                "Case 2: The driver really did take 80 minutes because of a road closure — "
                "a genuine event. Removing it would hide real information. "
                "The same extreme value can be either; checking the record decides which."
            ),
            "lineage": {
                "concept_ids": ["stats.outlier_reasoning"],
                "teaching_block_ids": [
                    qid("stats.outlier_reasoning", "tb3"),
                    qid("stats.outlier_reasoning", "tb4")
                ],
                "fact_ids": [
                    qid("stats.outlier_reasoning", "f2"),
                    qid("stats.outlier_reasoning", "f3"),
                    qid("stats.outlier_reasoning", "m1")
                ]
            }
        }
    ],
    "lineage": {
        "concept_ids": ["stats.outlier_reasoning"],
        "teaching_block_ids": [
            qid("stats.outlier_reasoning", "tb3"),
            qid("stats.outlier_reasoning", "tb4")
        ],
        "fact_ids": [
            qid("stats.outlier_reasoning", "f2"),
            qid("stats.outlier_reasoning", "f3"),
            qid("stats.outlier_reasoning", "m1")
        ]
    }
})

rem.append({
    "step_id": "tile_stats_shape_outliers.r03",
    "type": "remediation",
    "concept_ids": ["stats.frequency_distribution_reading"],
    "eyebrow": "Let's revisit",
    "title": "Reading a frequency table: bar height = count",
    "lede": "Each row in the frequency table is one bar in the histogram.",
    "blocks": [
        {
            "type": "prose",
            "block_id": "tile_stats_shape_outliers.r03.b1",
            "role": "example",
            "text": (
                "Frequency table: 10–20 min → 4 orders; 20–30 min → 9 orders; 30–40 min → 5 orders. "
                "In the histogram, the 20–30 min bar is the tallest (9 orders), the 10–20 min bar is "
                "shorter (4 orders), and the 30–40 min bar sits in between (5 orders). "
                "Bar height equals the count in that bin — nothing more."
            ),
            "lineage": {
                "concept_ids": ["stats.frequency_distribution_reading"],
                "teaching_block_ids": [
                    qid("stats.frequency_distribution_reading", "tb2"),
                    qid("stats.frequency_distribution_reading", "tb3")
                ],
                "fact_ids": [
                    qid("stats.frequency_distribution_reading", "f1"),
                    qid("stats.frequency_distribution_reading", "f3")
                ]
            }
        }
    ],
    "lineage": {
        "concept_ids": ["stats.frequency_distribution_reading"],
        "teaching_block_ids": [
            qid("stats.frequency_distribution_reading", "tb2"),
            qid("stats.frequency_distribution_reading", "tb3")
        ],
        "fact_ids": [
            qid("stats.frequency_distribution_reading", "f1"),
            qid("stats.frequency_distribution_reading", "f3")
        ]
    }
})

# ── assemble output ───────────────────────────────────────────────────────────
output = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": PATH_ID,
    "batch_id": BATCH_ID,
    "tiles": [tile]
}

out_path = "batches/final_batch_003_da_chunk/screens.part.c0_canary.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Written: {out_path}")
print(f"Steps: {len(steps)}")
print(f"Remediation steps: {len(rem)}")
for s in steps:
    print(f"  {s['step_id']} ({s['type']})")
