#!/usr/bin/env python3
"""Build screens.part.c1.json for tiles:
  - tile_stats_sample_size_significance
  - tile_capstone_question_workflow
  - tile_capstone_execution_narration_delivery
"""
import json

out = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_004_da_chunk2",
    "tiles": []
}

# ─────────────────────────────────────────────────────────────────────────────
# TILE 1: tile_stats_sample_size_significance
# ─────────────────────────────────────────────────────────────────────────────
tile_stats = {
    "tile_id": "tile_stats_sample_size_significance",
    "title": "Sample Size, Effect Size, and Statistical Significance",
    "steps": [

        # ── s01: explainer – sample_size_effect_concept (visual: side_by_side) ──
        {
            "step_id": "tile_stats_sample_size_significance.s01",
            "type": "explainer",
            "concept_ids": ["stats.sample_size_effect_concept"],
            "eyebrow": "Sample Size",
            "title": "Why Sample Size Changes How Much You Can Trust a Result",
            "lede": "Two checkout-button tests both show a 10% lift — but one ran with 50 users per group and the other with 5,000. Should you trust them equally?",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_stats_sample_size_significance.s01.p1",
                    "role": "definition",
                    "text": "A bigger sample tends to provide a more precise point estimate than a smaller sample. The more orders or users you observe, the more accurately you can estimate the effect of the explanatory variable — here, which checkout button a user saw — on the response, whether they completed an order. In a single study, precision comes from collecting a sufficiently large sample.",
                    "lineage": {
                        "concept_ids": ["stats.sample_size_effect_concept"],
                        "teaching_block_ids": ["stats.sample_size_effect_concept#tb2"],
                        "fact_ids": ["stats.sample_size_effect_concept#f1", "stats.sample_size_effect_concept#f2"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_stats_sample_size_significance.s01.p2",
                    "role": "example",
                    "text": "So the 5,000-user version of the QuickShip checkout test tends to produce a more precise estimate of the button's effect than the 50-user version — even though both happened to show the same 10% lift. The larger test observed far more completed orders, so its estimate of the button's effect is more accurate.",
                    "lineage": {
                        "concept_ids": ["stats.sample_size_effect_concept"],
                        "teaching_block_ids": ["stats.sample_size_effect_concept#tb3"],
                        "fact_ids": ["stats.sample_size_effect_concept#f1", "stats.sample_size_effect_concept#f2"]
                    }
                },
                {
                    "type": "side_by_side",
                    "block_id": "tile_stats_sample_size_significance.s01.v1",
                    "left_label": "Small sample (n = 50 per group)",
                    "right_label": "Large sample (n = 5,000 per group)",
                    "left": {
                        "type": "diagram",
                        "diagram_kind": "number_line",
                        "title": "Estimated lift — small sample",
                        "nodes": [
                            {"id": "nl_small_axis", "label": "Lift estimate axis (0% – 30%)"},
                            {"id": "nl_small_est1", "label": "−2%", "value": -2},
                            {"id": "nl_small_est2", "label": "5%", "value": 5},
                            {"id": "nl_small_est3", "label": "10%", "value": 10},
                            {"id": "nl_small_est4", "label": "18%", "value": 18},
                            {"id": "nl_small_est5", "label": "25%", "value": 25}
                        ],
                        "edges": [],
                        "alt_text": "Number line showing five hypothetical lift estimates from small-sample runs scattered widely from −2% to 25%, illustrating high variability around the true 10% lift."
                    },
                    "right": {
                        "type": "diagram",
                        "diagram_kind": "number_line",
                        "title": "Estimated lift — large sample",
                        "nodes": [
                            {"id": "nl_large_axis", "label": "Lift estimate axis (0% – 30%)"},
                            {"id": "nl_large_est1", "label": "9%", "value": 9},
                            {"id": "nl_large_est2", "label": "9.5%", "value": 9.5},
                            {"id": "nl_large_est3", "label": "10%", "value": 10},
                            {"id": "nl_large_est4", "label": "10.5%", "value": 10.5},
                            {"id": "nl_large_est5", "label": "11%", "value": 11}
                        ],
                        "edges": [],
                        "alt_text": "Number line showing five hypothetical lift estimates from large-sample runs clustered tightly between 9% and 11%, illustrating low variability around the true 10% lift."
                    },
                    "takeaway": "Same 10% lift, very different precision. The large-sample estimates cluster tightly; the small-sample estimates scatter widely. A bigger sample gives you a more trustworthy point estimate.",
                    "lineage": {
                        "concept_ids": ["stats.sample_size_effect_concept"],
                        "teaching_block_ids": ["stats.sample_size_effect_concept#tb2", "stats.sample_size_effect_concept#tb3"],
                        "fact_ids": ["stats.sample_size_effect_concept#f1", "stats.sample_size_effect_concept#f2"],
                        "anchors": ["stats.sample_size_effect_concept#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["stats.sample_size_effect_concept"],
                "teaching_block_ids": [
                    "stats.sample_size_effect_concept#tb1",
                    "stats.sample_size_effect_concept#tb2",
                    "stats.sample_size_effect_concept#tb3"
                ],
                "fact_ids": [
                    "stats.sample_size_effect_concept#f1",
                    "stats.sample_size_effect_concept#f2"
                ],
                "anchors": ["stats.sample_size_effect_concept#visual"]
            }
        },

        # ── s02: check – sample_size_effect_concept ──
        {
            "step_id": "tile_stats_sample_size_significance.s02",
            "type": "check",
            "concept_ids": ["stats.sample_size_effect_concept"],
            "eyebrow": "Quick Check",
            "title": "Which test result should you trust more?",
            "lede": "Both the 50-user and 5,000-user QuickShip checkout tests showed a 10% lift. Which estimate is more precise, and why?",
            "reward": {"gems": 5, "first_try_bonus": 2},
            "lineage": {
                "concept_ids": ["stats.sample_size_effect_concept"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "stats.sample_size_effect_concept#f1",
                    "stats.sample_size_effect_concept#f2"
                ],
                "anchors": ["stats.sample_size_effect_concept#assessment:compare_trustworthiness_by_sample_size"]
            }
        },

        # ── s03: hands_on – sample_size_effect_concept ──
        {
            "step_id": "tile_stats_sample_size_significance.s03",
            "type": "hands_on",
            "concept_ids": ["stats.sample_size_effect_concept"],
            "eyebrow": "Practice",
            "title": "Explain the Precision Difference",
            "lede": "In your own words, explain why the 5,000-user QuickShip test gives a more precise estimate of the checkout button's effect than the 50-user test, even though both showed the same 10% lift.",
            "reward": {"gems": 10},
            "lineage": {
                "concept_ids": ["stats.sample_size_effect_concept"],
                "teaching_block_ids": [],
                "fact_ids": [],
                "anchors": ["stats.sample_size_effect_concept#practice"]
            }
        },

        # ── s04: explainer – significance_confidence_concept (visual: diagram) ──
        {
            "step_id": "tile_stats_sample_size_significance.s04",
            "type": "explainer",
            "concept_ids": ["stats.significance_confidence_concept"],
            "eyebrow": "Significance & Confidence",
            "title": "Hypotheses, p-Values, and Statistical Significance",
            "lede": "The checkout test showed a 10% lift for the redesigned button. Before recommending it company-wide, you need language for how sure that result actually is.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_stats_sample_size_significance.s04.p1",
                    "role": "definition",
                    "text": "The null hypothesis (H0) often represents a skeptical position — a perspective of 'no difference'. The alternative hypothesis (HA) represents an alternative claim under consideration. For the QuickShip checkout test, H0 is that the redesigned button makes no real difference to completion rate; HA is that it does.",
                    "lineage": {
                        "concept_ids": ["stats.significance_confidence_concept"],
                        "teaching_block_ids": ["stats.significance_confidence_concept#tb2"],
                        "fact_ids": ["stats.significance_confidence_concept#f1"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_stats_sample_size_significance.s04.p2",
                    "role": "mechanism",
                    "text": "The p-value is the probability of observing data at least as favorable to HA as the current data set, if H0 were true. It quantifies the strength of evidence against the null hypothesis. Statistical significance measures how unusual a result would be if there were actually no difference between the variation and the baseline and the discrepancy were due to chance alone.",
                    "lineage": {
                        "concept_ids": ["stats.significance_confidence_concept"],
                        "teaching_block_ids": ["stats.significance_confidence_concept#tb3"],
                        "fact_ids": ["stats.significance_confidence_concept#f2", "stats.significance_confidence_concept#f3"]
                    }
                },
                {
                    "type": "diagram",
                    "block_id": "tile_stats_sample_size_significance.s04.v1",
                    "diagram_kind": "array",
                    "title": "25 confidence intervals built from different samples (around p = 0.88)",
                    "nodes": [
                        {"id": "ci_true_line", "label": "True proportion p = 0.88", "kind": "step"},
                        {"id": "ci_01", "label": "CI 1 — contains p", "kind": "step"},
                        {"id": "ci_02", "label": "CI 2 — contains p", "kind": "step"},
                        {"id": "ci_03", "label": "CI 3 — contains p", "kind": "step"},
                        {"id": "ci_04", "label": "CI 4 — contains p", "kind": "step"},
                        {"id": "ci_05", "label": "CI 5 — contains p", "kind": "step"},
                        {"id": "ci_06", "label": "CI 6 — contains p", "kind": "step"},
                        {"id": "ci_07", "label": "CI 7 — contains p", "kind": "step"},
                        {"id": "ci_08", "label": "CI 8 — contains p", "kind": "step"},
                        {"id": "ci_09", "label": "CI 9 — contains p", "kind": "step"},
                        {"id": "ci_10", "label": "CI 10 — contains p", "kind": "step"},
                        {"id": "ci_11", "label": "CI 11 — contains p", "kind": "step"},
                        {"id": "ci_12", "label": "CI 12 — contains p", "kind": "step"},
                        {"id": "ci_13", "label": "CI 13 — contains p", "kind": "step"},
                        {"id": "ci_14", "label": "CI 14 — contains p", "kind": "step"},
                        {"id": "ci_15", "label": "CI 15 — contains p", "kind": "step"},
                        {"id": "ci_16", "label": "CI 16 — contains p", "kind": "step"},
                        {"id": "ci_17", "label": "CI 17 — contains p", "kind": "step"},
                        {"id": "ci_18", "label": "CI 18 — contains p", "kind": "step"},
                        {"id": "ci_19", "label": "CI 19 — contains p", "kind": "step"},
                        {"id": "ci_20", "label": "CI 20 — contains p", "kind": "step"},
                        {"id": "ci_21", "label": "CI 21 — contains p", "kind": "step"},
                        {"id": "ci_22", "label": "CI 22 — contains p", "kind": "step"},
                        {"id": "ci_23", "label": "CI 23 — contains p", "kind": "step"},
                        {"id": "ci_24", "label": "CI 24 — contains p", "kind": "step"},
                        {"id": "ci_25_miss", "label": "CI 25 — MISSES p", "kind": "decision"}
                    ],
                    "edges": [],
                    "alt_text": "Strip of 25 horizontal 95% confidence intervals built from different samples around p = 0.88. Twenty-four intervals contain the true proportion line; one interval (CI 25) visibly misses it, illustrating that a small fraction of correctly-built intervals will fail to capture the parameter."
                    ,
                    "lineage": {
                        "concept_ids": ["stats.significance_confidence_concept"],
                        "teaching_block_ids": ["stats.significance_confidence_concept#tb2", "stats.significance_confidence_concept#tb3"],
                        "fact_ids": ["stats.significance_confidence_concept#f1", "stats.significance_confidence_concept#f2", "stats.significance_confidence_concept#f3"],
                        "anchors": ["stats.significance_confidence_concept#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["stats.significance_confidence_concept"],
                "teaching_block_ids": [
                    "stats.significance_confidence_concept#tb1",
                    "stats.significance_confidence_concept#tb2",
                    "stats.significance_confidence_concept#tb3"
                ],
                "fact_ids": [
                    "stats.significance_confidence_concept#f1",
                    "stats.significance_confidence_concept#f2",
                    "stats.significance_confidence_concept#f3"
                ],
                "anchors": ["stats.significance_confidence_concept#visual"]
            }
        },

        # ── s05: video – significance_confidence_concept ──
        {
            "step_id": "tile_stats_sample_size_significance.s05",
            "type": "video",
            "concept_ids": ["stats.significance_confidence_concept"],
            "eyebrow": "Watch",
            "title": "p-Values and Sample Size in Action",
            "lede": "See how sample size drives p-values and why a large sample can make a tiny difference look statistically significant.",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": "tile_stats_sample_size_significance.s05.v1",
                    "segment_ids": ["seg_stats.significance_confidence_concept_vemZtEM63GY_17_649"]
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["stats.significance_confidence_concept"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "stats.significance_confidence_concept#f1",
                    "stats.significance_confidence_concept#f3",
                    "stats.significance_confidence_concept#f6"
                ],
                "segment_ids": ["seg_stats.significance_confidence_concept_vemZtEM63GY_17_649"]
            }
        },

        # ── s06: explainer – significance_confidence_concept (CI + misconceptions) ──
        {
            "step_id": "tile_stats_sample_size_significance.s06",
            "type": "explainer",
            "concept_ids": ["stats.significance_confidence_concept"],
            "eyebrow": "Confidence Intervals",
            "title": "What a Confidence Interval Actually Means",
            "lede": "A confidence interval is not a probability statement about a single interval — here is what it does mean, and two common errors to avoid.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_stats_sample_size_significance.s06.p1",
                    "role": "definition",
                    "text": "A confidence interval is a range of plausible values likely to contain the population parameter — the true value you are trying to estimate. If many samples were taken and a 95% interval built from each one, about 95% of those intervals would contain the parameter.",
                    "lineage": {
                        "concept_ids": ["stats.significance_confidence_concept"],
                        "teaching_block_ids": ["stats.significance_confidence_concept#tb4"],
                        "fact_ids": ["stats.significance_confidence_concept#f4"]
                    }
                },
                {
                    "type": "callout",
                    "block_id": "tile_stats_sample_size_significance.s06.c1",
                    "tone": "misconception",
                    "text": "Describing a confidence interval as capturing the population parameter with a certain probability is a common error. The 95% describes how the method behaves across many samples — not the probability attached to this one interval. So it is not quite right to say 'there is a 95% chance the true completion-rate difference is in this interval.'",
                    "lineage": {
                        "concept_ids": ["stats.significance_confidence_concept"],
                        "teaching_block_ids": ["stats.significance_confidence_concept#tb5"],
                        "fact_ids": ["stats.significance_confidence_concept#f5"]
                    }
                },
                {
                    "type": "callout",
                    "block_id": "tile_stats_sample_size_significance.s06.c2",
                    "tone": "misconception",
                    "text": "Not every confidence interval captures the true value, even when the method is followed correctly. In an illustrative set of twenty-five 95% confidence intervals built from different samples around p = 0.88, only one failed to contain the population proportion. A small fraction of correctly-built intervals will miss it.",
                    "lineage": {
                        "concept_ids": ["stats.significance_confidence_concept"],
                        "teaching_block_ids": ["stats.significance_confidence_concept#tb6"],
                        "fact_ids": ["stats.significance_confidence_concept#m1"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_stats_sample_size_significance.s06.p2",
                    "role": "takeaway",
                    "text": "When the sample size becomes large, even a very small, practically unimportant difference can be detected and called statistically significant. A large enough checkout test could detect a tiny, practically unimportant lift and call it statistically significant. Significance tells you how unusual the result would be if there were truly no difference — not that the lift is big enough to matter.",
                    "lineage": {
                        "concept_ids": ["stats.significance_confidence_concept"],
                        "teaching_block_ids": ["stats.significance_confidence_concept#tb7"],
                        "fact_ids": ["stats.significance_confidence_concept#f6"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["stats.significance_confidence_concept"],
                "teaching_block_ids": [
                    "stats.significance_confidence_concept#tb4",
                    "stats.significance_confidence_concept#tb5",
                    "stats.significance_confidence_concept#tb6"
                ],
                "fact_ids": [
                    "stats.significance_confidence_concept#f4",
                    "stats.significance_confidence_concept#f5",
                    "stats.significance_confidence_concept#m1"
                ]
            }
        },

        # ── s07: check – significance_confidence_concept (H0/HA) ──
        {
            "step_id": "tile_stats_sample_size_significance.s07",
            "type": "check",
            "concept_ids": ["stats.significance_confidence_concept"],
            "eyebrow": "Quick Check",
            "title": "Null vs. Alternative Hypothesis",
            "lede": "For the QuickShip checkout A/B test, which statement correctly describes the role of H0?",
            "reward": {"gems": 5, "first_try_bonus": 2},
            "lineage": {
                "concept_ids": ["stats.significance_confidence_concept"],
                "teaching_block_ids": [],
                "fact_ids": ["stats.significance_confidence_concept#f1"],
                "anchors": ["stats.significance_confidence_concept#assessment:identify_null_and_alternative_hypothesis_roles"]
            }
        },

        # ── s08: check – significance_confidence_concept (p-value) ──
        {
            "step_id": "tile_stats_sample_size_significance.s08",
            "type": "check",
            "concept_ids": ["stats.significance_confidence_concept"],
            "eyebrow": "Quick Check",
            "title": "What Does the p-Value Measure?",
            "lede": "The checkout test returns a p-value. What does that p-value tell you?",
            "reward": {"gems": 5, "first_try_bonus": 2},
            "lineage": {
                "concept_ids": ["stats.significance_confidence_concept"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "stats.significance_confidence_concept#f2",
                    "stats.significance_confidence_concept#f3"
                ],
                "anchors": ["stats.significance_confidence_concept#assessment:explain_p_value_as_evidence_against_null"]
            }
        },

        # ── s09: hands_on – significance_confidence_concept ──
        {
            "step_id": "tile_stats_sample_size_significance.s09",
            "type": "hands_on",
            "concept_ids": ["stats.significance_confidence_concept"],
            "eyebrow": "Practice",
            "title": "Interpret the Confidence Interval",
            "lede": "The A/B test results table shows confidence intervals and p-values for the QuickShip checkout test. Select the rows and cells that correctly illustrate the repeated-sampling interpretation of a 95% confidence interval — and flag any that misstate it.",
            "reward": {"gems": 10},
            "lineage": {
                "concept_ids": ["stats.significance_confidence_concept"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "stats.significance_confidence_concept#f4",
                    "stats.significance_confidence_concept#f5",
                    "stats.significance_confidence_concept#f6",
                    "stats.significance_confidence_concept#m1"
                ],
                "anchors": [
                    "stats.significance_confidence_concept#practice",
                    "stats.significance_confidence_concept#assessment:interpret_confidence_interval_correctly",
                    "stats.significance_confidence_concept#assessment:avoid_probability_misinterpretation_of_confidence_interval",
                    "stats.significance_confidence_concept#assessment:distinguish_statistical_significance_from_practical_significance"
                ]
            }
        },

        # ── s10: explainer – business_conclusion_from_experiment (visual: diagram) ──
        {
            "step_id": "tile_stats_sample_size_significance.s10",
            "type": "explainer",
            "concept_ids": ["stats.business_conclusion_from_experiment"],
            "eyebrow": "Drawing Conclusions",
            "title": "From Confidence Interval to Business Decision",
            "lede": "Getting a p-value or confidence interval is not the end of the job — someone still has to decide what to do about the checkout button.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_stats_sample_size_significance.s10.p1",
                    "role": "definition",
                    "text": "H0 often represents a skeptical perspective or a claim to be tested; HA represents an alternative claim under consideration. The value being compared to the parameter in this setup is called the null value. For the two textbook examples, the null value is p0 = 0.333.",
                    "lineage": {
                        "concept_ids": ["stats.business_conclusion_from_experiment"],
                        "teaching_block_ids": ["stats.business_conclusion_from_experiment#tb2"],
                        "fact_ids": ["stats.business_conclusion_from_experiment#f1"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_stats_sample_size_significance.s10.p2",
                    "role": "mechanism",
                    "text": "In one example, the null value (p0 = 0.333) fell within the confidence interval computed from the sample — that value was not implausible, so the data did not provide sufficient evidence to reject H0. In a second example, p0 = 0.333 was not in the 95% confidence interval, so H0 was rejected: the data provided statistically significant evidence that the proportion differed from 0.333, and because the entire interval was below 0.333, it was concluded to be lower.",
                    "lineage": {
                        "concept_ids": ["stats.business_conclusion_from_experiment"],
                        "teaching_block_ids": ["stats.business_conclusion_from_experiment#tb3"],
                        "fact_ids": ["stats.business_conclusion_from_experiment#f2", "stats.business_conclusion_from_experiment#f3"]
                    }
                },
                {
                    "type": "diagram",
                    "block_id": "tile_stats_sample_size_significance.s10.v1",
                    "diagram_kind": "number_line",
                    "title": "Null value inside vs. outside the 95% CI",
                    "nodes": [
                        {"id": "scenario_a_ci_low",  "label": "Scenario A CI lower bound", "value": 0.28},
                        {"id": "scenario_a_null",    "label": "Null value p0 = 0.333 (inside CI)", "value": 0.333},
                        {"id": "scenario_a_ci_high", "label": "Scenario A CI upper bound", "value": 0.39},
                        {"id": "scenario_b_ci_low",  "label": "Scenario B CI lower bound", "value": 0.21},
                        {"id": "scenario_b_ci_high", "label": "Scenario B CI upper bound", "value": 0.31},
                        {"id": "scenario_b_null",    "label": "Null value p0 = 0.333 (outside CI, above)", "value": 0.333}
                    ],
                    "edges": [],
                    "alt_text": "Two number-line scenarios side by side. Scenario A: 95% CI spans roughly 0.28–0.39, with the null value 0.333 falling inside the shaded band — fail to reject. Scenario B: 95% CI spans roughly 0.21–0.31, with the null value 0.333 falling outside and above the band — reject, conclude proportion is lower than 0.333."
                    ,
                    "lineage": {
                        "concept_ids": ["stats.business_conclusion_from_experiment"],
                        "teaching_block_ids": ["stats.business_conclusion_from_experiment#tb2", "stats.business_conclusion_from_experiment#tb3"],
                        "fact_ids": ["stats.business_conclusion_from_experiment#f1", "stats.business_conclusion_from_experiment#f2", "stats.business_conclusion_from_experiment#f3"],
                        "anchors": ["stats.business_conclusion_from_experiment#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["stats.business_conclusion_from_experiment"],
                "teaching_block_ids": [
                    "stats.business_conclusion_from_experiment#tb1",
                    "stats.business_conclusion_from_experiment#tb2",
                    "stats.business_conclusion_from_experiment#tb3"
                ],
                "fact_ids": [
                    "stats.business_conclusion_from_experiment#f1",
                    "stats.business_conclusion_from_experiment#f2",
                    "stats.business_conclusion_from_experiment#f3"
                ],
                "anchors": ["stats.business_conclusion_from_experiment#visual"]
            }
        },

        # ── s11: explainer – business_conclusion_from_experiment (fail-to-reject + practical) ──
        {
            "step_id": "tile_stats_sample_size_significance.s11",
            "type": "explainer",
            "concept_ids": ["stats.business_conclusion_from_experiment"],
            "eyebrow": "Drawing Conclusions",
            "title": "Failing to Reject Is Not the Same as Accepting the Null",
            "lede": "The first example failed to reject H0 — but that does not mean H0 is true.",
            "blocks": [
                {
                    "type": "callout",
                    "block_id": "tile_stats_sample_size_significance.s11.c1",
                    "tone": "misconception",
                    "text": "Failing to reject the null hypothesis is not equivalent to accepting it as true. It only means there was not strong enough evidence for the alternative. In the first textbook example, perhaps there was an actual difference, but it could not be detected with the relatively small sample of 50.",
                    "lineage": {
                        "concept_ids": ["stats.business_conclusion_from_experiment"],
                        "teaching_block_ids": ["stats.business_conclusion_from_experiment#tb4"],
                        "fact_ids": ["stats.business_conclusion_from_experiment#f6", "stats.business_conclusion_from_experiment#m1"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_stats_sample_size_significance.s11.p1",
                    "role": "example",
                    "text": "Analyzing a test's results means stating whether the variation had a positive, negative, or neutral effect versus the baseline (control). For the QuickShip checkout test, that means saying plainly whether the redesigned button did better, worse, or about the same as the original — not just reporting a p-value and stopping.",
                    "lineage": {
                        "concept_ids": ["stats.business_conclusion_from_experiment"],
                        "teaching_block_ids": ["stats.business_conclusion_from_experiment#tb5"],
                        "fact_ids": ["stats.business_conclusion_from_experiment#f4"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_stats_sample_size_significance.s11.p2",
                    "role": "takeaway",
                    "text": "When the sample size becomes large, even a very small, practically unimportant difference can be detected and called statistically significant. An online experiment might find that placing additional ads on a movie review website statistically significantly increases viewership of a TV show by 0.001% — but that increase might not have any practical value. A business conclusion has to weigh the size of the lift, not just whether it was detected.",
                    "lineage": {
                        "concept_ids": ["stats.business_conclusion_from_experiment"],
                        "teaching_block_ids": ["stats.business_conclusion_from_experiment#tb6"],
                        "fact_ids": ["stats.business_conclusion_from_experiment#f5"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["stats.business_conclusion_from_experiment"],
                "teaching_block_ids": [
                    "stats.business_conclusion_from_experiment#tb4",
                    "stats.business_conclusion_from_experiment#tb5"
                ],
                "fact_ids": [
                    "stats.business_conclusion_from_experiment#f4",
                    "stats.business_conclusion_from_experiment#f6",
                    "stats.business_conclusion_from_experiment#m1"
                ]
            }
        },

        # ── s12: video – business_conclusion_from_experiment ──
        {
            "step_id": "tile_stats_sample_size_significance.s12",
            "type": "video",
            "concept_ids": ["stats.business_conclusion_from_experiment"],
            "eyebrow": "Watch",
            "title": "Statistical vs. Practical Significance",
            "lede": "See why a tiny p-value only tells you the observed difference was unlikely under the null — not whether it matters in practice.",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": "tile_stats_sample_size_significance.s12.v1",
                    "segment_ids": ["seg_stats.business_conclusion_from_experiment__k1MQTUCXmU_122_266"]
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["stats.business_conclusion_from_experiment"],
                "teaching_block_ids": [],
                "fact_ids": ["stats.business_conclusion_from_experiment#f5"],
                "segment_ids": ["seg_stats.business_conclusion_from_experiment__k1MQTUCXmU_122_266"]
            }
        },

        # ── s13: check – business_conclusion_from_experiment (H0/HA roles) ──
        {
            "step_id": "tile_stats_sample_size_significance.s13",
            "type": "check",
            "concept_ids": ["stats.business_conclusion_from_experiment"],
            "eyebrow": "Quick Check",
            "title": "Null Value and Hypothesis Roles",
            "lede": "In the textbook proportion test, what is the role of the null value p0 = 0.333?",
            "reward": {"gems": 5, "first_try_bonus": 2},
            "lineage": {
                "concept_ids": ["stats.business_conclusion_from_experiment"],
                "teaching_block_ids": [],
                "fact_ids": ["stats.business_conclusion_from_experiment#f1"],
                "anchors": ["stats.business_conclusion_from_experiment#assessment:identify_null_and_alternative_hypothesis_roles"]
            }
        },

        # ── s14: check – business_conclusion_from_experiment (practical significance) ──
        {
            "step_id": "tile_stats_sample_size_significance.s14",
            "type": "check",
            "concept_ids": ["stats.business_conclusion_from_experiment"],
            "eyebrow": "Quick Check",
            "title": "Statistical vs. Practical Significance",
            "lede": "A large checkout test detects a 0.1% lift with a very small p-value. What should you conclude?",
            "reward": {"gems": 5, "first_try_bonus": 2},
            "lineage": {
                "concept_ids": ["stats.business_conclusion_from_experiment"],
                "teaching_block_ids": [],
                "fact_ids": ["stats.business_conclusion_from_experiment#f5"],
                "anchors": ["stats.business_conclusion_from_experiment#assessment:distinguish_statistical_significance_from_practical_importance"]
            }
        },

        # ── s15: hands_on – business_conclusion_from_experiment ──
        {
            "step_id": "tile_stats_sample_size_significance.s15",
            "type": "hands_on",
            "concept_ids": ["stats.business_conclusion_from_experiment"],
            "eyebrow": "Practice",
            "title": "Order the Steps to a Business Conclusion",
            "lede": "Put the following steps in the correct order for drawing a business conclusion from the QuickShip A/B test: check whether the null value falls inside or outside the CI, state the directional conclusion, assess practical significance, report the recommendation.",
            "reward": {"gems": 10},
            "lineage": {
                "concept_ids": ["stats.business_conclusion_from_experiment"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "stats.business_conclusion_from_experiment#f2",
                    "stats.business_conclusion_from_experiment#f3",
                    "stats.business_conclusion_from_experiment#f4",
                    "stats.business_conclusion_from_experiment#f6",
                    "stats.business_conclusion_from_experiment#m1"
                ],
                "anchors": [
                    "stats.business_conclusion_from_experiment#practice",
                    "stats.business_conclusion_from_experiment#assessment:determine_reject_or_fail_to_reject_from_confidence_interval",
                    "stats.business_conclusion_from_experiment#assessment:state_directional_business_conclusion_from_ab_test",
                    "stats.business_conclusion_from_experiment#assessment:avoid_equating_fail_to_reject_with_null_being_true"
                ]
            }
        },

        # ── s16: recap ──
        {
            "step_id": "tile_stats_sample_size_significance.s16",
            "type": "recap",
            "concept_ids": [
                "stats.sample_size_effect_concept",
                "stats.significance_confidence_concept",
                "stats.business_conclusion_from_experiment"
            ],
            "eyebrow": "Recap",
            "title": "What You Learned",
            "lede": "Three ideas that connect sample size, significance, and business conclusions.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_stats_sample_size_significance.s16.p1",
                    "role": "takeaway",
                    "text": "A bigger sample gives a more precise estimate. Statistical significance tells you how unusual a result would be under the null — not that the lift is large enough to matter. When the sample size becomes large, even a tiny, practically unimportant difference can be called statistically significant. And failing to reject H0 is not the same as accepting it as true.",
                    "lineage": {
                        "concept_ids": [
                            "stats.sample_size_effect_concept",
                            "stats.significance_confidence_concept",
                            "stats.business_conclusion_from_experiment"
                        ],
                        "teaching_block_ids": [
                            "stats.significance_confidence_concept#tb7",
                            "stats.business_conclusion_from_experiment#tb6"
                        ],
                        "fact_ids": [
                            "stats.business_conclusion_from_experiment#f5",
                            "stats.significance_confidence_concept#f6"
                        ]
                    }
                },
                {
                    "type": "up_next",
                    "block_id": "tile_stats_sample_size_significance.s16.un1",
                    "title": "Up next: Prioritizing Findings and Framing Recommendations",
                    "text": "You will learn how to rank findings by relevance to the stakeholder's decision — not by analytical interestingness — and how to frame a recommendation so it states an action, not just a data point."
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": [
                    "stats.sample_size_effect_concept",
                    "stats.significance_confidence_concept",
                    "stats.business_conclusion_from_experiment"
                ],
                "teaching_block_ids": [
                    "stats.significance_confidence_concept#tb7",
                    "stats.business_conclusion_from_experiment#tb6"
                ],
                "fact_ids": [
                    "stats.business_conclusion_from_experiment#f5",
                    "stats.significance_confidence_concept#f6"
                ]
            }
        }
    ],

    # ── remediation steps ──
    "remediation_steps": [
        {
            "step_id": "tile_stats_sample_size_significance.r01",
            "type": "remediation",
            "concept_ids": ["stats.sample_size_effect_concept"],
            "eyebrow": "Let's revisit",
            "title": "Small vs. Large Sample: A Direct Comparison",
            "lede": "Both QuickShip checkout tests showed a 10% lift — but the estimates from the small test scattered widely, while the large test's estimates clustered tightly. That difference in spread is what precision means.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_stats_sample_size_significance.r01.p1",
                    "role": "definition",
                    "text": "A bigger sample tends to provide a more precise point estimate. With 50 users per group, the estimated lift could easily land anywhere from near zero to well above 20% just by chance. With 5,000 users per group, the same estimate stays close to the true value because far more completed orders are observed. Precision comes from sample size, not from the size of the lift itself.",
                    "lineage": {
                        "concept_ids": ["stats.sample_size_effect_concept"],
                        "teaching_block_ids": ["stats.sample_size_effect_concept#tb2"],
                        "fact_ids": ["stats.sample_size_effect_concept#f1", "stats.sample_size_effect_concept#f2"]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["stats.sample_size_effect_concept"],
                "teaching_block_ids": ["stats.sample_size_effect_concept#tb2", "stats.sample_size_effect_concept#tb3"],
                "fact_ids": ["stats.sample_size_effect_concept#f1", "stats.sample_size_effect_concept#f2"]
            }
        },
        {
            "step_id": "tile_stats_sample_size_significance.r02",
            "type": "remediation",
            "concept_ids": ["stats.significance_confidence_concept"],
            "eyebrow": "Let's revisit",
            "title": "H0 vs. HA: The Skeptic and the Claim",
            "lede": "H0 is the skeptic — it says nothing changed. HA is the claim you are trying to find evidence for.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_stats_sample_size_significance.r02.p1",
                    "role": "definition",
                    "text": "For the QuickShip checkout test, H0 says the redesigned button makes no real difference to completion rate. HA says it does. The p-value measures how surprising the observed data would be if H0 were true — a small p-value means the data would be very unusual under H0, giving evidence for HA. A large p-value means the data are not surprising under H0, so there is not enough evidence to reject it.",
                    "lineage": {
                        "concept_ids": ["stats.significance_confidence_concept"],
                        "teaching_block_ids": ["stats.significance_confidence_concept#tb2", "stats.significance_confidence_concept#tb3"],
                        "fact_ids": ["stats.significance_confidence_concept#f1", "stats.significance_confidence_concept#f2", "stats.significance_confidence_concept#f3"]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["stats.significance_confidence_concept"],
                "teaching_block_ids": ["stats.significance_confidence_concept#tb2", "stats.significance_confidence_concept#tb3"],
                "fact_ids": ["stats.significance_confidence_concept#f1", "stats.significance_confidence_concept#f2", "stats.significance_confidence_concept#f3"]
            }
        },
        {
            "step_id": "tile_stats_sample_size_significance.r03",
            "type": "remediation",
            "concept_ids": ["stats.business_conclusion_from_experiment"],
            "eyebrow": "Let's revisit",
            "title": "Null Value Inside vs. Outside the CI",
            "lede": "The decision rule is simple: if the null value sits inside the confidence interval, you cannot reject H0. If it sits outside, you reject.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_stats_sample_size_significance.r03.p1",
                    "role": "mechanism",
                    "text": "In the first textbook example, p0 = 0.333 fell inside the 95% CI — the null value was plausible, so the data did not provide sufficient evidence to reject H0. In the second example, p0 = 0.333 was not in the CI, and the entire interval was below 0.333, so H0 was rejected and the conclusion was that the proportion is lower. Failing to reject in the first example does not mean H0 is true — it may simply mean the sample of 50 was too small to detect a real difference.",
                    "lineage": {
                        "concept_ids": ["stats.business_conclusion_from_experiment"],
                        "teaching_block_ids": ["stats.business_conclusion_from_experiment#tb3", "stats.business_conclusion_from_experiment#tb4"],
                        "fact_ids": ["stats.business_conclusion_from_experiment#f2", "stats.business_conclusion_from_experiment#f3", "stats.business_conclusion_from_experiment#f6"]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["stats.business_conclusion_from_experiment"],
                "teaching_block_ids": ["stats.business_conclusion_from_experiment#tb3", "stats.business_conclusion_from_experiment#tb4"],
                "fact_ids": ["stats.business_conclusion_from_experiment#f2", "stats.business_conclusion_from_experiment#f3", "stats.business_conclusion_from_experiment#f6"]
            }
        }
    ]
}

out["tiles"].append(tile_stats)


# ─────────────────────────────────────────────────────────────────────────────
# TILE 2: tile_capstone_question_workflow
# ─────────────────────────────────────────────────────────────────────────────
tile_capstone_qw = {
    "tile_id": "tile_capstone_question_workflow",
    "title": "Defining the Question and Planning the Workflow",
    "steps": [

        # ── s01: explainer – defining_business_question (visual: before_after) ──
        {
            "step_id": "tile_capstone_question_workflow.s01",
            "type": "explainer",
            "concept_ids": ["capstone.defining_business_question"],
            "eyebrow": "Scoping",
            "title": "From Vague Complaint to Scoped Business Question",
            "lede": "The operations team at QuickShip says deliveries feel slow lately. That is not yet something you can analyze.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_question_workflow.s01.p1",
                    "role": "intro",
                    "text": "Before any analytical work begins, the question to be addressed, its context, and its boundaries should be identified. Turning a vague complaint into a workable target is called scoping. Scoping ensures an appropriate, common understanding of the problem is defined, and that expectations are aligned with what the analysis can produce.",
                    "lineage": {
                        "concept_ids": ["capstone.defining_business_question"],
                        "teaching_block_ids": ["capstone.defining_business_question#tb1", "capstone.defining_business_question#tb2"],
                        "fact_ids": ["capstone.defining_business_question#f1", "capstone.defining_business_question#f2"]
                    }
                },
                {
                    "type": "before_after",
                    "block_id": "tile_capstone_question_workflow.s01.v1",
                    "before": {
                        "type": "diagram",
                        "diagram_kind": "container",
                        "title": "Vague complaint",
                        "nodes": [
                            {"id": "complaint", "label": "Deliveries feel slow lately — can you look into it?", "kind": "step"}
                        ],
                        "edges": [],
                        "alt_text": "A box containing the vague complaint: 'Deliveries feel slow lately — can you look into it?'"
                    },
                    "after": {
                        "type": "diagram",
                        "diagram_kind": "container",
                        "title": "Scoped business question",
                        "nodes": [
                            {"id": "scoped_q", "label": "Which delivery zones are missing the delivery-time target, and by how much, over the last quarter?", "kind": "step"},
                            {"id": "context",  "label": "Context: QuickShip last-quarter orders", "kind": "subprocess"},
                            {"id": "boundary", "label": "Boundary: zones and delivery time vs. target", "kind": "subprocess"}
                        ],
                        "edges": [],
                        "alt_text": "A box containing the scoped question with its context (QuickShip last-quarter orders) and boundaries (zones and delivery time vs. target) made explicit."
                    },
                    "change_summary": "Scoping converts the vague complaint into a specific question with a context (last quarter's orders) and boundaries (zones and delivery time), so the analyst and the operations team share the same understanding of what the analysis will and will not answer.",
                    "lineage": {
                        "concept_ids": ["capstone.defining_business_question"],
                        "teaching_block_ids": ["capstone.defining_business_question#tb1", "capstone.defining_business_question#tb2"],
                        "fact_ids": ["capstone.defining_business_question#f1", "capstone.defining_business_question#f2"],
                        "anchors": ["capstone.defining_business_question#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["capstone.defining_business_question"],
                "teaching_block_ids": [
                    "capstone.defining_business_question#tb1",
                    "capstone.defining_business_question#tb2"
                ],
                "fact_ids": [
                    "capstone.defining_business_question#f1",
                    "capstone.defining_business_question#f2"
                ],
                "anchors": ["capstone.defining_business_question#visual"]
            }
        },

        # ── s02: explainer – defining_business_question (example) ──
        {
            "step_id": "tile_capstone_question_workflow.s02",
            "type": "explainer",
            "concept_ids": ["capstone.defining_business_question"],
            "eyebrow": "Scoping",
            "title": "Why Every Later Step Depends on the Scoped Question",
            "lede": "Every later capstone step — what data to retrieve, how to clean it, what to compute — serves this one sentence.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_question_workflow.s02.p1",
                    "role": "example",
                    "text": "For QuickShip, scoping the vague complaint means settling its context and boundaries: which orders (a specific quarter's deliveries), which measure (delivery time against a target), and which unit of comparison (delivery zone). The result is a specific business question: 'Which delivery zones are missing the delivery-time target, and by how much, over the last quarter?' Scope it loosely, and the rest of the project has nothing precise to aim at.",
                    "lineage": {
                        "concept_ids": ["capstone.defining_business_question"],
                        "teaching_block_ids": ["capstone.defining_business_question#tb3"],
                        "fact_ids": ["capstone.defining_business_question#f1", "capstone.defining_business_question#f2"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["capstone.defining_business_question"],
                "teaching_block_ids": ["capstone.defining_business_question#tb3"],
                "fact_ids": [
                    "capstone.defining_business_question#f1",
                    "capstone.defining_business_question#f2"
                ]
            }
        },

        # ── s03: check – defining_business_question ──
        {
            "step_id": "tile_capstone_question_workflow.s03",
            "type": "check",
            "concept_ids": ["capstone.defining_business_question"],
            "eyebrow": "Quick Check",
            "title": "Scoping the Question",
            "lede": "The operations team says 'deliveries feel slow lately.' Which of the following is the best scoped business question?",
            "reward": {"gems": 5, "first_try_bonus": 2},
            "lineage": {
                "concept_ids": ["capstone.defining_business_question"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "capstone.defining_business_question#f1",
                    "capstone.defining_business_question#f2"
                ],
                "anchors": ["capstone.defining_business_question#assessment:convert_rough_idea_to_scoped_business_question"]
            }
        },

        # ── s04: hands_on – defining_business_question ──
        {
            "step_id": "tile_capstone_question_workflow.s04",
            "type": "hands_on",
            "concept_ids": ["capstone.defining_business_question"],
            "eyebrow": "Practice",
            "title": "Write Your Scoped Business Question",
            "lede": "Using the QuickShip scenario, write the scoped business question in one sentence. Include the context (which orders), the measure (what you will compare), and the boundary (what the analysis will and will not answer).",
            "reward": {"gems": 10},
            "lineage": {
                "concept_ids": ["capstone.defining_business_question"],
                "teaching_block_ids": [],
                "fact_ids": [],
                "anchors": ["capstone.defining_business_question#practice"]
            }
        },

        # ── s05: explainer – data_retrieval_method_selection (visual: side_by_side) ──
        {
            "step_id": "tile_capstone_question_workflow.s05",
            "type": "explainer",
            "concept_ids": ["capstone.data_retrieval_method_selection"],
            "eyebrow": "Data Retrieval",
            "title": "Matching Each Data Source to Its Retrieval Tool",
            "lede": "With the question scoped, the next decision is how to get the data. QuickShip's order records live in a SQL database; the driver roster is kept in an Excel workbook.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_question_workflow.s05.p1",
                    "role": "mechanism",
                    "text": "Data that lives in a SQL database can be retrieved with a SQL query; pandas' SQL query wrappers (pandas.io.sql) facilitate this retrieval. So the orders table, sitting in the company's database, is a SQL-query job.",
                    "lineage": {
                        "concept_ids": ["capstone.data_retrieval_method_selection"],
                        "teaching_block_ids": ["capstone.data_retrieval_method_selection#tb2"],
                        "fact_ids": ["capstone.data_retrieval_method_selection#f1"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_capstone_question_workflow.s05.p2",
                    "role": "mechanism",
                    "text": "read_excel() reads an Excel file directly into a DataFrame. So the driver roster workbook, which never touches a database, is a read_excel() job instead. The capstone ends up using both: a SQL query pulls the last quarter's orders (zone, driver_id, delivery_time_min) from the orders table, and read_excel() pulls the driver roster (driver_id, name, zone, shift) from the spreadsheet.",
                    "lineage": {
                        "concept_ids": ["capstone.data_retrieval_method_selection"],
                        "teaching_block_ids": ["capstone.data_retrieval_method_selection#tb3", "capstone.data_retrieval_method_selection#tb4"],
                        "fact_ids": ["capstone.data_retrieval_method_selection#f2"]
                    }
                },
                {
                    "type": "side_by_side",
                    "block_id": "tile_capstone_question_workflow.s05.v1",
                    "left_label": "SQL database → SQL query (pandas.io.sql)",
                    "right_label": "Excel workbook → read_excel()",
                    "left": {
                        "type": "diagram",
                        "diagram_kind": "mapping",
                        "title": "Database retrieval",
                        "nodes": [
                            {"id": "db_source", "label": "Data source: SQL database (orders table)", "kind": "io"},
                            {"id": "db_tool",   "label": "Retrieval method: SQL query via pandas.io.sql", "kind": "step"},
                            {"id": "db_result", "label": "Result: orders DataFrame (zone, driver_id, delivery_time_min, order_date)", "kind": "io"}
                        ],
                        "edges": [
                            {"from": "db_source", "to": "db_tool"},
                            {"from": "db_tool",   "to": "db_result"}
                        ],
                        "alt_text": "Mapping from SQL database source to SQL query retrieval method to orders DataFrame."
                    },
                    "right": {
                        "type": "diagram",
                        "diagram_kind": "mapping",
                        "title": "Excel retrieval",
                        "nodes": [
                            {"id": "xl_source", "label": "Data source: Excel workbook (driver roster)", "kind": "io"},
                            {"id": "xl_tool",   "label": "Retrieval method: read_excel()", "kind": "step"},
                            {"id": "xl_result", "label": "Result: drivers DataFrame (driver_id, name, zone, shift)", "kind": "io"}
                        ],
                        "edges": [
                            {"from": "xl_source", "to": "xl_tool"},
                            {"from": "xl_tool",   "to": "xl_result"}
                        ],
                        "alt_text": "Mapping from Excel workbook source to read_excel() retrieval method to drivers DataFrame."
                    },
                    "takeaway": "Two different sources, matched to two different retrieval tools. The method follows where each source actually sits — not a personal preference.",
                    "lineage": {
                        "concept_ids": ["capstone.data_retrieval_method_selection"],
                        "teaching_block_ids": [
                            "capstone.data_retrieval_method_selection#tb2",
                            "capstone.data_retrieval_method_selection#tb3",
                            "capstone.data_retrieval_method_selection#tb4",
                            "capstone.data_retrieval_method_selection#tb5"
                        ],
                        "fact_ids": ["capstone.data_retrieval_method_selection#f1", "capstone.data_retrieval_method_selection#f2"],
                        "anchors": ["capstone.data_retrieval_method_selection#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["capstone.data_retrieval_method_selection"],
                "teaching_block_ids": [
                    "capstone.data_retrieval_method_selection#tb1",
                    "capstone.data_retrieval_method_selection#tb2",
                    "capstone.data_retrieval_method_selection#tb3",
                    "capstone.data_retrieval_method_selection#tb4",
                    "capstone.data_retrieval_method_selection#tb5"
                ],
                "fact_ids": [
                    "capstone.data_retrieval_method_selection#f1",
                    "capstone.data_retrieval_method_selection#f2"
                ],
                "anchors": ["capstone.data_retrieval_method_selection#visual"]
            }
        },

        # ── s06: video – data_retrieval_method_selection ──
        {
            "step_id": "tile_capstone_question_workflow.s06",
            "type": "video",
            "concept_ids": ["capstone.data_retrieval_method_selection"],
            "eyebrow": "Watch",
            "title": "read_excel() and SQL Retrieval in pandas",
            "lede": "See both retrieval methods in action: one call to read_excel() and one call to pd.read_sql_query() with a SELECT statement.",
            "blocks": [
                {
                    "type": "media_group",
                    "block_id": "tile_capstone_question_workflow.s06.v1",
                    "segment_ids": [
                        "seg_capstone.data_retrieval_method_selection_P6HCyxSyFpY_162_267",
                        "seg_capstone.data_retrieval_method_selection_N6hyN6BW6ao_1522_1681"
                    ]
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["capstone.data_retrieval_method_selection"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "capstone.data_retrieval_method_selection#f1",
                    "capstone.data_retrieval_method_selection#f2"
                ],
                "segment_ids": [
                    "seg_capstone.data_retrieval_method_selection_P6HCyxSyFpY_162_267",
                    "seg_capstone.data_retrieval_method_selection_N6hyN6BW6ao_1522_1681"
                ]
            }
        },

        # ── s07: check – data_retrieval_method_selection ──
        {
            "step_id": "tile_capstone_question_workflow.s07",
            "type": "check",
            "concept_ids": ["capstone.data_retrieval_method_selection"],
            "eyebrow": "Quick Check",
            "title": "Which Tool for Which Source?",
            "lede": "QuickShip's driver roster is stored in an Excel workbook. Which retrieval method should you use?",
            "reward": {"gems": 5, "first_try_bonus": 2},
            "lineage": {
                "concept_ids": ["capstone.data_retrieval_method_selection"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "capstone.data_retrieval_method_selection#f1",
                    "capstone.data_retrieval_method_selection#f2"
                ],
                "anchors": ["capstone.data_retrieval_method_selection#assessment:match_retrieval_method_to_data_source"]
            }
        },

        # ── s08: hands_on – data_retrieval_method_selection ──
        {
            "step_id": "tile_capstone_question_workflow.s08",
            "type": "hands_on",
            "concept_ids": ["capstone.data_retrieval_method_selection"],
            "eyebrow": "Practice",
            "title": "Classify Each Data Source by Retrieval Method",
            "lede": "For each QuickShip data source below, classify it as 'SQL query via pandas.io.sql' or 'read_excel()'. Drag each source to the correct retrieval method.",
            "reward": {"gems": 10},
            "lineage": {
                "concept_ids": ["capstone.data_retrieval_method_selection"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "capstone.data_retrieval_method_selection#f1",
                    "capstone.data_retrieval_method_selection#f2"
                ],
                "anchors": [
                    "capstone.data_retrieval_method_selection#practice",
                    "capstone.data_retrieval_method_selection#assessment:identify_sql_retrieval_for_database_source",
                    "capstone.data_retrieval_method_selection#assessment:identify_read_excel_for_workbook_source",
                    "capstone.data_retrieval_method_selection#assessment:match_retrieval_method_to_data_source"
                ]
            }
        },

        # ── s09: explainer – end_to_end_workflow_structure (visual: process_flow) ──
        {
            "step_id": "tile_capstone_question_workflow.s09",
            "type": "explainer",
            "concept_ids": ["capstone.end_to_end_workflow_structure"],
            "eyebrow": "Workflow",
            "title": "The Six-Stage Analytical Workflow",
            "lede": "With the question scoped and both retrieval tools chosen, sketch the whole project's shape before touching either one.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_question_workflow.s09.p1",
                    "role": "mechanism",
                    "text": "An analytical project is commonly structured through phases that begin with scoping the question and end with delivering and communicating the results. A phase such as scoping may need to be revisited if a later phase encounters changes or limitations — for example, if cleaning the orders data reveals that 'last quarter' is ambiguous in the source system, that sends you back to re-scope rather than pressing on.",
                    "lineage": {
                        "concept_ids": ["capstone.end_to_end_workflow_structure"],
                        "teaching_block_ids": ["capstone.end_to_end_workflow_structure#tb2"],
                        "fact_ids": ["capstone.end_to_end_workflow_structure#f1"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_capstone_question_workflow.s09.p2",
                    "role": "mechanism",
                    "text": "Within that structure, the source data is retrieved (via a SQL query or a spreadsheet import), and data quality should be assessed at every stage, with quality improvements such as cleaning focused as early as possible. So right after the orders query and the roster import, the capstone checks for problems like missing delivery times — rather than waiting until the final analysis to discover them.",
                    "lineage": {
                        "concept_ids": ["capstone.end_to_end_workflow_structure"],
                        "teaching_block_ids": ["capstone.end_to_end_workflow_structure#tb3"],
                        "fact_ids": ["capstone.end_to_end_workflow_structure#f2"]
                    }
                },
                {
                    "type": "process_flow",
                    "block_id": "tile_capstone_question_workflow.s09.v1",
                    "title": "QuickShip capstone end-to-end workflow",
                    "direction": "LR",
                    "nodes": [
                        {"id": "pf_scope",     "label": "Scope",     "kind": "start",     "detail": "Define the business question, context, and boundaries"},
                        {"id": "pf_retrieve",  "label": "Retrieve",  "kind": "step",      "detail": "SQL query for orders table; read_excel() for driver roster"},
                        {"id": "pf_clean",     "label": "Clean / Model", "kind": "step",  "detail": "Assess quality early; join orders and drivers tables"},
                        {"id": "pf_analyze",   "label": "Analyze",   "kind": "step",      "detail": "Compute zone-level delivery statistics"},
                        {"id": "pf_visualize", "label": "Visualize", "kind": "step",      "detail": "Build charts and summary tables"},
                        {"id": "pf_communicate","label": "Communicate","kind": "end",     "detail": "Deliver findings to the operations team"}
                    ],
                    "edges": [
                        {"from": "pf_scope",     "to": "pf_retrieve",   "kind": "next"},
                        {"from": "pf_retrieve",  "to": "pf_clean",      "kind": "next"},
                        {"from": "pf_clean",     "to": "pf_analyze",    "kind": "next"},
                        {"from": "pf_analyze",   "to": "pf_visualize",  "kind": "next"},
                        {"from": "pf_visualize", "to": "pf_communicate","kind": "next"},
                        {"from": "pf_clean",     "to": "pf_scope",      "kind": "loop_back", "label": "revisit if needed"}
                    ],
                    "alt_text": "Six-stage linear flow: Scope → Retrieve → Clean/Model → Analyze → Visualize → Communicate, with a back-arrow from Clean/Model to Scope labelled 'revisit if needed', and a quality-check note spanning all stages.",
                    "lineage": {
                        "concept_ids": ["capstone.end_to_end_workflow_structure"],
                        "teaching_block_ids": [
                            "capstone.end_to_end_workflow_structure#tb1",
                            "capstone.end_to_end_workflow_structure#tb2",
                            "capstone.end_to_end_workflow_structure#tb3"
                        ],
                        "fact_ids": ["capstone.end_to_end_workflow_structure#f1", "capstone.end_to_end_workflow_structure#f2"],
                        "anchors": ["capstone.end_to_end_workflow_structure#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["capstone.end_to_end_workflow_structure"],
                "teaching_block_ids": [
                    "capstone.end_to_end_workflow_structure#tb1",
                    "capstone.end_to_end_workflow_structure#tb2",
                    "capstone.end_to_end_workflow_structure#tb3"
                ],
                "fact_ids": [
                    "capstone.end_to_end_workflow_structure#f1",
                    "capstone.end_to_end_workflow_structure#f2"
                ],
                "anchors": ["capstone.end_to_end_workflow_structure#visual"]
            }
        },

        # ── s10: explainer – end_to_end_workflow_structure (modeling + delivery) ──
        {
            "step_id": "tile_capstone_question_workflow.s10",
            "type": "explainer",
            "concept_ids": ["capstone.end_to_end_workflow_structure"],
            "eyebrow": "Workflow",
            "title": "Modeling Multi-Table Data and Communicating Results",
            "lede": "Two stages of the workflow deserve special attention: modeling (when data spans more than one table) and delivery.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_question_workflow.s10.p1",
                    "role": "mechanism",
                    "text": "Where the project's data spans more than one table, the modeling stage connects related tables; relationships are what connect related information between tables. The capstone's orders and drivers are two such tables, so a modeling stage links them — using driver_id as the join key — before any deeper analysis relies on both together.",
                    "lineage": {
                        "concept_ids": ["capstone.end_to_end_workflow_structure"],
                        "teaching_block_ids": ["capstone.end_to_end_workflow_structure#tb4"],
                        "fact_ids": ["capstone.end_to_end_workflow_structure#f3"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_capstone_question_workflow.s10.p2",
                    "role": "mechanism",
                    "text": "In the delivery and communication stage, insights are communicated to the commissioner and approver — the people who need them. Activities may include producing summary packs and reports, launching dashboards or websites, and presentations. The capstone's version of this is reporting the zone-delay findings back to the operations team that raised the original complaint.",
                    "lineage": {
                        "concept_ids": ["capstone.end_to_end_workflow_structure"],
                        "teaching_block_ids": ["capstone.end_to_end_workflow_structure#tb5"],
                        "fact_ids": ["capstone.end_to_end_workflow_structure#f4"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["capstone.end_to_end_workflow_structure"],
                "teaching_block_ids": [
                    "capstone.end_to_end_workflow_structure#tb4",
                    "capstone.end_to_end_workflow_structure#tb5"
                ],
                "fact_ids": [
                    "capstone.end_to_end_workflow_structure#f3",
                    "capstone.end_to_end_workflow_structure#f4"
                ]
            }
        },

        # ── s11: check – end_to_end_workflow_structure ──
        {
            "step_id": "tile_capstone_question_workflow.s11",
            "type": "check",
            "concept_ids": ["capstone.end_to_end_workflow_structure"],
            "eyebrow": "Quick Check",
            "title": "Workflow Stage Order",
            "lede": "Which of the following correctly describes the order of the first three stages in the QuickShip capstone workflow?",
            "reward": {"gems": 5, "first_try_bonus": 2},
            "lineage": {
                "concept_ids": ["capstone.end_to_end_workflow_structure"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "capstone.end_to_end_workflow_structure#f1",
                    "capstone.end_to_end_workflow_structure#f2",
                    "capstone.end_to_end_workflow_structure#f3",
                    "capstone.end_to_end_workflow_structure#f4"
                ],
                "anchors": ["capstone.end_to_end_workflow_structure#assessment:sequence_and_structure_end_to_end_workflow_stages"]
            }
        },

        # ── s12: check – end_to_end_workflow_structure (revisiting) ──
        {
            "step_id": "tile_capstone_question_workflow.s12",
            "type": "check",
            "concept_ids": ["capstone.end_to_end_workflow_structure"],
            "eyebrow": "Quick Check",
            "title": "When to Revisit an Earlier Stage",
            "lede": "During the cleaning stage, you discover that 'last quarter' is ambiguous in the orders database. What should you do?",
            "reward": {"gems": 5, "first_try_bonus": 2},
            "lineage": {
                "concept_ids": ["capstone.end_to_end_workflow_structure"],
                "teaching_block_ids": [],
                "fact_ids": ["capstone.end_to_end_workflow_structure#f1"],
                "anchors": ["capstone.end_to_end_workflow_structure#assessment:identify_when_a_later_phase_requires_revisiting_an_earlier_phase"]
            }
        },

        # ── s13: hands_on – end_to_end_workflow_structure ──
        {
            "step_id": "tile_capstone_question_workflow.s13",
            "type": "hands_on",
            "concept_ids": ["capstone.end_to_end_workflow_structure"],
            "eyebrow": "Practice",
            "title": "Sequence the Workflow Stages",
            "lede": "Put the six QuickShip capstone workflow stages in the correct order, then identify which stage connects the orders and drivers tables.",
            "reward": {"gems": 10},
            "lineage": {
                "concept_ids": ["capstone.end_to_end_workflow_structure"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "capstone.end_to_end_workflow_structure#f2",
                    "capstone.end_to_end_workflow_structure#f3",
                    "capstone.end_to_end_workflow_structure#f4"
                ],
                "anchors": [
                    "capstone.end_to_end_workflow_structure#practice",
                    "capstone.end_to_end_workflow_structure#assessment:place_data_retrieval_and_early_quality_assessment_correctly_in_the_workflow",
                    "capstone.end_to_end_workflow_structure#assessment:identify_the_role_of_the_modeling_stage_when_data_spans_multiple_tables",
                    "capstone.end_to_end_workflow_structure#assessment:describe_delivery_and_communication_stage_activities_and_audience"
                ]
            }
        },

        # ── s14: recap ──
        {
            "step_id": "tile_capstone_question_workflow.s14",
            "type": "recap",
            "concept_ids": [
                "capstone.defining_business_question",
                "capstone.data_retrieval_method_selection",
                "capstone.end_to_end_workflow_structure"
            ],
            "eyebrow": "Recap",
            "title": "What You Learned",
            "lede": "Three foundations every remaining capstone step builds on.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_question_workflow.s14.p1",
                    "role": "takeaway",
                    "text": "Scoping converts a vague complaint into a specific question with context and boundaries. The retrieval method follows the source: SQL query for the database, read_excel() for the workbook. The workflow runs Scope → Retrieve → Clean/Model → Analyze → Visualize → Communicate, with quality checked throughout and any stage open to revisiting.",
                    "lineage": {
                        "concept_ids": [
                            "capstone.defining_business_question",
                            "capstone.data_retrieval_method_selection",
                            "capstone.end_to_end_workflow_structure"
                        ],
                        "teaching_block_ids": [
                            "capstone.defining_business_question#tb4",
                            "capstone.data_retrieval_method_selection#tb6",
                            "capstone.end_to_end_workflow_structure#tb6"
                        ],
                        "fact_ids": [
                            "capstone.data_retrieval_method_selection#f1",
                            "capstone.data_retrieval_method_selection#f2",
                            "capstone.defining_business_question#f1",
                            "capstone.defining_business_question#f2",
                            "capstone.end_to_end_workflow_structure#f1",
                            "capstone.end_to_end_workflow_structure#f2",
                            "capstone.end_to_end_workflow_structure#f3",
                            "capstone.end_to_end_workflow_structure#f4"
                        ]
                    }
                },
                {
                    "type": "up_next",
                    "block_id": "tile_capstone_question_workflow.s14.un1",
                    "title": "Up next: Integrating SQL, Spreadsheet, and Python",
                    "text": "You will see how to run the SQL query, import the Excel roster, and begin connecting the two tables in pandas."
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": [
                    "capstone.defining_business_question",
                    "capstone.data_retrieval_method_selection",
                    "capstone.end_to_end_workflow_structure"
                ],
                "teaching_block_ids": [
                    "capstone.defining_business_question#tb4",
                    "capstone.data_retrieval_method_selection#tb6",
                    "capstone.end_to_end_workflow_structure#tb6"
                ],
                "fact_ids": [
                    "capstone.data_retrieval_method_selection#f1",
                    "capstone.data_retrieval_method_selection#f2",
                    "capstone.defining_business_question#f1",
                    "capstone.defining_business_question#f2",
                    "capstone.end_to_end_workflow_structure#f1",
                    "capstone.end_to_end_workflow_structure#f2",
                    "capstone.end_to_end_workflow_structure#f3",
                    "capstone.end_to_end_workflow_structure#f4"
                ]
            }
        }
    ],

    "remediation_steps": [
        {
            "step_id": "tile_capstone_question_workflow.r01",
            "type": "remediation",
            "concept_ids": ["capstone.defining_business_question"],
            "eyebrow": "Let's revisit",
            "title": "Scoping: Context and Boundaries",
            "lede": "A scoped question has three parts: what you will measure, which records you will use, and what the analysis will not answer.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_question_workflow.r01.p1",
                    "role": "definition",
                    "text": "Before any analytical work begins, the question to be addressed, its context, and its boundaries should be identified. For QuickShip, the context is last quarter's orders and the boundary is delivery time by zone — not every possible cause of delay. Scoping ensures you and the operations team share the same understanding of what the analysis will and will not answer.",
                    "lineage": {
                        "concept_ids": ["capstone.defining_business_question"],
                        "teaching_block_ids": ["capstone.defining_business_question#tb1", "capstone.defining_business_question#tb2"],
                        "fact_ids": ["capstone.defining_business_question#f1", "capstone.defining_business_question#f2"]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["capstone.defining_business_question"],
                "teaching_block_ids": ["capstone.defining_business_question#tb1", "capstone.defining_business_question#tb2"],
                "fact_ids": ["capstone.defining_business_question#f1", "capstone.defining_business_question#f2"]
            }
        },
        {
            "step_id": "tile_capstone_question_workflow.r02",
            "type": "remediation",
            "concept_ids": ["capstone.data_retrieval_method_selection"],
            "eyebrow": "Let's revisit",
            "title": "Source Determines Tool",
            "lede": "The retrieval method is not a preference — it follows where the data actually lives.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_question_workflow.r02.p1",
                    "role": "definition",
                    "text": "Data that lives in a SQL database is retrieved with a SQL query via pandas.io.sql. Data stored in an Excel workbook is read with read_excel(). For QuickShip: the orders table lives in the company's database (SQL query), and the driver roster is an Excel workbook (read_excel()). Matching each source to its tool is the first executable step of the workflow.",
                    "lineage": {
                        "concept_ids": ["capstone.data_retrieval_method_selection"],
                        "teaching_block_ids": ["capstone.data_retrieval_method_selection#tb2", "capstone.data_retrieval_method_selection#tb3"],
                        "fact_ids": ["capstone.data_retrieval_method_selection#f1", "capstone.data_retrieval_method_selection#f2"]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["capstone.data_retrieval_method_selection"],
                "teaching_block_ids": ["capstone.data_retrieval_method_selection#tb2", "capstone.data_retrieval_method_selection#tb3"],
                "fact_ids": ["capstone.data_retrieval_method_selection#f1", "capstone.data_retrieval_method_selection#f2"]
            }
        },
        {
            "step_id": "tile_capstone_question_workflow.r03",
            "type": "remediation",
            "concept_ids": ["capstone.end_to_end_workflow_structure"],
            "eyebrow": "Let's revisit",
            "title": "The Workflow Is Not a Straight Line",
            "lede": "Any stage can send you back to an earlier one — that is a feature, not a failure.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_question_workflow.r03.p1",
                    "role": "mechanism",
                    "text": "An analytical project commonly runs Scope → Retrieve → Clean/Model → Analyze → Visualize → Communicate. But a phase such as scoping may need to be revisited if a later phase encounters changes or limitations. If cleaning the orders data reveals that 'last quarter' is ambiguous in the source system, that sends you back to re-scope the question rather than pressing on with a flawed definition.",
                    "lineage": {
                        "concept_ids": ["capstone.end_to_end_workflow_structure"],
                        "teaching_block_ids": ["capstone.end_to_end_workflow_structure#tb2"],
                        "fact_ids": ["capstone.end_to_end_workflow_structure#f1"]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["capstone.end_to_end_workflow_structure"],
                "teaching_block_ids": ["capstone.end_to_end_workflow_structure#tb2"],
                "fact_ids": ["capstone.end_to_end_workflow_structure#f1"]
            }
        }
    ]
}

out["tiles"].append(tile_capstone_qw)


# ─────────────────────────────────────────────────────────────────────────────
# TILE 3: tile_capstone_execution_narration_delivery
# ─────────────────────────────────────────────────────────────────────────────
tile_capstone_end = {
    "tile_id": "tile_capstone_execution_narration_delivery",
    "title": "Narrating and Delivering the Capstone",
    "steps": [

        # ── s01: explainer – independent_execution (visual: process_flow) ──
        {
            "step_id": "tile_capstone_execution_narration_delivery.s01",
            "type": "explainer",
            "concept_ids": ["capstone.independent_execution"],
            "eyebrow": "Independent Execution",
            "title": "Running the Whole Plan Yourself",
            "lede": "With the plan, retrieval, cleaning, modeling, statistics, and visualization steps all defined, what is left is carrying the whole thing out yourself — end to end — without being walked through each step again.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_execution_narration_delivery.s01.p1",
                    "role": "mechanism",
                    "text": "During the design phase, the commission is converted into an analytical plan, with some iteration expected as the solution is developed. For the capstone, the workflow outline from earlier becomes that analytical plan, and it is normal to adjust it once the SQL, spreadsheet, and pandas work actually starts.",
                    "lineage": {
                        "concept_ids": ["capstone.independent_execution"],
                        "teaching_block_ids": ["capstone.independent_execution#tb2"],
                        "fact_ids": ["capstone.independent_execution#f1"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_capstone_execution_narration_delivery.s01.p2",
                    "role": "mechanism",
                    "text": "During the analysis phase, the planned analysis is carried out while progress and relevance are monitored, and appropriate records of the analysis conducted, changes, decisions, and assumptions made are maintained. As the capstone's query, cleaning, modeling, statistics, and figures get built, a decision log captures what changed and why.",
                    "lineage": {
                        "concept_ids": ["capstone.independent_execution"],
                        "teaching_block_ids": ["capstone.independent_execution#tb3"],
                        "fact_ids": ["capstone.independent_execution#f2"]
                    }
                },
                {
                    "type": "process_flow",
                    "block_id": "tile_capstone_execution_narration_delivery.s01.v1",
                    "title": "Two-phase independent execution",
                    "direction": "LR",
                    "nodes": [
                        {"id": "phase_design",   "label": "Design phase",   "kind": "step",  "detail": "Convert commission → analytical plan; iteration expected"},
                        {"id": "plan_output",    "label": "Analytical plan", "kind": "io",   "detail": "Scoped question + workflow outline"},
                        {"id": "phase_analysis", "label": "Analysis phase",  "kind": "step", "detail": "Execute plan; monitor progress and relevance"},
                        {"id": "decision_log",   "label": "Decision log",    "kind": "io",   "detail": "Records of changes, decisions, and assumptions"},
                        {"id": "outputs",        "label": "Analytical outputs","kind": "end","detail": "Query results, cleaned data, statistics, figures"}
                    ],
                    "edges": [
                        {"from": "phase_design",   "to": "plan_output",    "kind": "next"},
                        {"from": "plan_output",    "to": "phase_analysis", "kind": "next"},
                        {"from": "phase_analysis", "to": "decision_log",   "kind": "branch"},
                        {"from": "phase_analysis", "to": "outputs",        "kind": "next"},
                        {"from": "phase_analysis", "to": "phase_design",   "kind": "loop_back", "label": "iterate if needed"}
                    ],
                    "alt_text": "Two-phase flow: Design phase produces an analytical plan (with an iteration arrow back to Design), then Analysis phase produces both a decision log and the analytical outputs.",
                    "lineage": {
                        "concept_ids": ["capstone.independent_execution"],
                        "teaching_block_ids": [
                            "capstone.independent_execution#tb1",
                            "capstone.independent_execution#tb2",
                            "capstone.independent_execution#tb3"
                        ],
                        "fact_ids": ["capstone.independent_execution#f1", "capstone.independent_execution#f2"],
                        "anchors": ["capstone.independent_execution#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["capstone.independent_execution"],
                "teaching_block_ids": [
                    "capstone.independent_execution#tb1",
                    "capstone.independent_execution#tb2",
                    "capstone.independent_execution#tb3"
                ],
                "fact_ids": [
                    "capstone.independent_execution#f1",
                    "capstone.independent_execution#f2"
                ],
                "anchors": ["capstone.independent_execution#visual"]
            }
        },

        # ── s02: check – independent_execution ──
        {
            "step_id": "tile_capstone_execution_narration_delivery.s02",
            "type": "check",
            "concept_ids": ["capstone.independent_execution"],
            "eyebrow": "Quick Check",
            "title": "What Belongs in the Decision Log?",
            "lede": "During the analysis phase of the QuickShip capstone, which of the following should be recorded in the decision log?",
            "reward": {"gems": 5, "first_try_bonus": 2},
            "lineage": {
                "concept_ids": ["capstone.independent_execution"],
                "teaching_block_ids": [],
                "fact_ids": ["capstone.independent_execution#f2"],
                "anchors": ["capstone.independent_execution#assessment:execute_planned_analysis_while_monitoring_and_recording_decisions"]
            }
        },

        # ── s03: hands_on – independent_execution ──
        {
            "step_id": "tile_capstone_execution_narration_delivery.s03",
            "type": "hands_on",
            "concept_ids": ["capstone.independent_execution"],
            "eyebrow": "Practice",
            "title": "Execute the Capstone Plan",
            "lede": "Using the QuickShip orders and driver datasets, carry out the full analytical plan: run the SQL query, import the driver roster, clean and model the data, compute zone-level statistics, and build the summary visualization. Record any decisions or changes you make in a decision log.",
            "reward": {"gems": 15},
            "lineage": {
                "concept_ids": ["capstone.independent_execution"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "capstone.independent_execution#f1",
                    "capstone.independent_execution#f2"
                ],
                "anchors": [
                    "capstone.independent_execution#practice",
                    "capstone.independent_execution#assessment:convert_commission_to_analytical_plan_with_iteration",
                    "capstone.independent_execution#assessment:execute_capstone_independently_across_sql_spreadsheet_python"
                ]
            }
        },

        # ── s04: explainer – narrated_stakeholder_summary (visual: before_after) ──
        {
            "step_id": "tile_capstone_execution_narration_delivery.s04",
            "type": "explainer",
            "concept_ids": ["capstone.narrated_stakeholder_summary"],
            "eyebrow": "Narrated Summary",
            "title": "Turning Findings into a Story for the Operations Team",
            "lede": "The finished analysis now needs to be turned into something the operations team can act on: a narrated stakeholder summary of what was found.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_execution_narration_delivery.s04.p1",
                    "role": "mechanism",
                    "text": "Designing a communication with a specific person in mind — even if that is not always the reality — can help avoid treating a 'mixed audience' as one undifferentiated group. Knowing what motivates that audience lets you frame what you need them to know or do in those terms. So instead of writing for 'the operations team', write for the Head of Operations specifically.",
                    "lineage": {
                        "concept_ids": ["capstone.narrated_stakeholder_summary"],
                        "teaching_block_ids": ["capstone.narrated_stakeholder_summary#tb2"],
                        "fact_ids": ["capstone.narrated_stakeholder_summary#f1"]
                    }
                },
                {
                    "type": "before_after",
                    "block_id": "tile_capstone_execution_narration_delivery.s04.v1",
                    "before": {
                        "type": "diagram",
                        "diagram_kind": "container",
                        "title": "Raw analytical finding",
                        "nodes": [
                            {"id": "raw_finding", "label": "Lagos-North: avg 32.9 min, 0% on time, gap 7.9 min above target\nLagos-South: avg 29.0 min, 0% on time, gap 4.0 min above target\nKano-Central: avg 26.0 min, 33% on time, gap 1.0 min above target\nAbuja-West: avg 22.6 min, 100% on time", "kind": "io"}
                        ],
                        "edges": [],
                        "alt_text": "Table of zone-level delivery statistics: Lagos-North and Lagos-South both miss the 25-minute target; Kano-Central barely misses; Abuja-West is fully on target."
                    },
                    "after": {
                        "type": "diagram",
                        "diagram_kind": "container",
                        "title": "Narrated stakeholder summary",
                        "nodes": [
                            {"id": "summary_para", "label": "Beginning: Last quarter, QuickShip's delivery-time target is 25 minutes across all zones.\nMiddle: Lagos-North and Lagos-South are both missing the target — Lagos-North by an average of 7.9 minutes, with no orders on time.\nEnd: Adding one courier to the Lagos route is the recommended next step.", "kind": "step"}
                        ],
                        "edges": [],
                        "alt_text": "Narrated summary paragraph structured as beginning (context), middle (finding), end (recommendation) for the Head of Operations."
                    },
                    "change_summary": "The same zone-delay data is transformed into an audience-facing story: context first, then the key finding, then a recommended action — framed for the Head of Operations.",
                    "lineage": {
                        "concept_ids": ["capstone.narrated_stakeholder_summary"],
                        "teaching_block_ids": ["capstone.narrated_stakeholder_summary#tb1", "capstone.narrated_stakeholder_summary#tb2"],
                        "fact_ids": ["capstone.narrated_stakeholder_summary#f1"],
                        "anchors": ["capstone.narrated_stakeholder_summary#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["capstone.narrated_stakeholder_summary"],
                "teaching_block_ids": [
                    "capstone.narrated_stakeholder_summary#tb1",
                    "capstone.narrated_stakeholder_summary#tb2"
                ],
                "fact_ids": ["capstone.narrated_stakeholder_summary#f1"],
                "anchors": ["capstone.narrated_stakeholder_summary#visual"]
            }
        },

        # ── s05: explainer – narrated_stakeholder_summary (structure + delivery) ──
        {
            "step_id": "tile_capstone_execution_narration_delivery.s05",
            "type": "explainer",
            "concept_ids": ["capstone.narrated_stakeholder_summary"],
            "eyebrow": "Narrated Summary",
            "title": "Beginning, Middle, End — and What Counts as Sufficient",
            "lede": "A summary can follow a story structure with an obvious beginning, middle, and end.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_execution_narration_delivery.s05.p1",
                    "role": "mechanism",
                    "text": "The beginning level-sets the audience with the big picture and background context. The middle presents what the analysis found. The ending gives the key takeaway — such as a recommended next step. For the QuickShip capstone, the beginning sets the delivery-time target, the middle reports the Lagos slowdown, and the ending recommends adding one courier to the Lagos route.",
                    "lineage": {
                        "concept_ids": ["capstone.narrated_stakeholder_summary"],
                        "teaching_block_ids": ["capstone.narrated_stakeholder_summary#tb3"],
                        "fact_ids": ["capstone.narrated_stakeholder_summary#f3"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_capstone_execution_narration_delivery.s05.p2",
                    "role": "mechanism",
                    "text": "During delivery, insights are communicated to the people who need them, sufficiently for them to determine whether the work meets their requirements. This communication can include summary packs, reports, or presentations. For the capstone, the finished summary pack should let the Head of Operations judge whether the analysis answers the original question.",
                    "lineage": {
                        "concept_ids": ["capstone.narrated_stakeholder_summary"],
                        "teaching_block_ids": ["capstone.narrated_stakeholder_summary#tb4"],
                        "fact_ids": ["capstone.narrated_stakeholder_summary#f2"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_capstone_execution_narration_delivery.s05.p3",
                    "role": "takeaway",
                    "text": "A narrated summary aimed at one specific person, moving through beginning, middle, and end, is what turns the capstone's findings into something its audience can actually use.",
                    "lineage": {
                        "concept_ids": ["capstone.narrated_stakeholder_summary"],
                        "teaching_block_ids": ["capstone.narrated_stakeholder_summary#tb3", "capstone.narrated_stakeholder_summary#tb4"],
                        "fact_ids": ["capstone.narrated_stakeholder_summary#f2", "capstone.narrated_stakeholder_summary#f3", "capstone.narrated_stakeholder_summary#f4"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["capstone.narrated_stakeholder_summary"],
                "teaching_block_ids": [
                    "capstone.narrated_stakeholder_summary#tb3",
                    "capstone.narrated_stakeholder_summary#tb4"
                ],
                "fact_ids": [
                    "capstone.narrated_stakeholder_summary#f2",
                    "capstone.narrated_stakeholder_summary#f3",
                    "capstone.narrated_stakeholder_summary#f4"
                ]
            }
        },

        # ── s06: check – narrated_stakeholder_summary ──
        {
            "step_id": "tile_capstone_execution_narration_delivery.s06",
            "type": "check",
            "concept_ids": ["capstone.narrated_stakeholder_summary"],
            "eyebrow": "Quick Check",
            "title": "What Counts as Sufficient Delivery?",
            "lede": "The Head of Operations receives the capstone summary pack. What is the standard for whether the delivery is sufficient?",
            "reward": {"gems": 5, "first_try_bonus": 2},
            "lineage": {
                "concept_ids": ["capstone.narrated_stakeholder_summary"],
                "teaching_block_ids": [],
                "fact_ids": ["capstone.narrated_stakeholder_summary#f2"],
                "anchors": ["capstone.narrated_stakeholder_summary#assessment:identify_delivery_formats_and_sufficiency_standard"]
            }
        },

        # ── s07: hands_on – narrated_stakeholder_summary ──
        {
            "step_id": "tile_capstone_execution_narration_delivery.s07",
            "type": "hands_on",
            "concept_ids": ["capstone.narrated_stakeholder_summary"],
            "eyebrow": "Practice",
            "title": "Write the Narrated Stakeholder Summary",
            "lede": "Using the QuickShip zone delivery summary, write a narrated stakeholder summary for the Head of Operations. Structure it with a clear beginning (context), middle (findings), and end (recommendation). Submit your summary pack.",
            "reward": {"gems": 15},
            "lineage": {
                "concept_ids": ["capstone.narrated_stakeholder_summary"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "capstone.narrated_stakeholder_summary#f1",
                    "capstone.narrated_stakeholder_summary#f2",
                    "capstone.narrated_stakeholder_summary#f3"
                ],
                "anchors": [
                    "capstone.narrated_stakeholder_summary#practice",
                    "capstone.narrated_stakeholder_summary#assessment:frame_communication_for_specific_audience",
                    "capstone.narrated_stakeholder_summary#assessment:structure_summary_with_beginning_middle_end",
                    "capstone.narrated_stakeholder_summary#assessment:produce_narrated_stakeholder_summary_from_capstone_findings"
                ]
            }
        },

        # ── s08: explainer – documenting_presenting_deliverable (visual: process_flow) ──
        {
            "step_id": "tile_capstone_execution_narration_delivery.s08",
            "type": "explainer",
            "concept_ids": ["capstone.documenting_presenting_deliverable"],
            "eyebrow": "Deliverable",
            "title": "Packaging the Work So Others Can Evaluate It",
            "lede": "The very last capstone step: package the finished work so someone who never watched it get built can understand and evaluate it.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_execution_narration_delivery.s08.p1",
                    "role": "mechanism",
                    "text": "Transparency about the analytical decisions, process, limitations, and changes made at each stage should be clearly shown through documentation of the analysis, assumptions, and data, together with records of the decisions and quality-assurance checks made. For the capstone, that means documenting the decisions made at each stage — from scoping through visualization.",
                    "lineage": {
                        "concept_ids": ["capstone.documenting_presenting_deliverable"],
                        "teaching_block_ids": ["capstone.documenting_presenting_deliverable#tb2"],
                        "fact_ids": ["capstone.documenting_presenting_deliverable#f1"]
                    }
                },
                {
                    "type": "prose",
                    "block_id": "tile_capstone_execution_narration_delivery.s08.p2",
                    "role": "mechanism",
                    "text": "Delivery and communication activities can include producing summary packs and reports, launching dashboards or websites, and giving presentations. The capstone's deliverable is the finished report or summary pack, together with the visualization set already built, presented to the operations team that raised the original complaint.",
                    "lineage": {
                        "concept_ids": ["capstone.documenting_presenting_deliverable"],
                        "teaching_block_ids": ["capstone.documenting_presenting_deliverable#tb3"],
                        "fact_ids": ["capstone.documenting_presenting_deliverable#f2"]
                    }
                },
                {
                    "type": "process_flow",
                    "block_id": "tile_capstone_execution_narration_delivery.s08.v1",
                    "title": "Documentation layer → Delivery layer",
                    "direction": "TB",
                    "nodes": [
                        {"id": "doc_scope",     "label": "Scope decisions",       "kind": "step", "detail": "Question, context, boundaries"},
                        {"id": "doc_retrieve",  "label": "Retrieval decisions",   "kind": "step", "detail": "SQL query, read_excel() choices"},
                        {"id": "doc_clean",     "label": "Cleaning decisions",    "kind": "step", "detail": "Missing values, QA checks"},
                        {"id": "doc_model",     "label": "Modeling decisions",    "kind": "step", "detail": "Join key, assumptions"},
                        {"id": "doc_analyze",   "label": "Analysis decisions",    "kind": "step", "detail": "Statistics chosen, limitations"},
                        {"id": "doc_viz",       "label": "Visualization decisions","kind": "step","detail": "Chart types, design choices"},
                        {"id": "delivery",      "label": "Delivery layer",        "kind": "end",  "detail": "Summary pack + visualizations + presentation to operations team"}
                    ],
                    "edges": [
                        {"from": "doc_scope",    "to": "doc_retrieve",  "kind": "next"},
                        {"from": "doc_retrieve", "to": "doc_clean",     "kind": "next"},
                        {"from": "doc_clean",    "to": "doc_model",     "kind": "next"},
                        {"from": "doc_model",    "to": "doc_analyze",   "kind": "next"},
                        {"from": "doc_analyze",  "to": "doc_viz",       "kind": "next"},
                        {"from": "doc_viz",      "to": "delivery",      "kind": "next"}
                    ],
                    "alt_text": "Two-layer structure: a documentation layer capturing decisions and QA checks at each prior stage (Scope → Retrieve → Clean → Model → Analyze → Visualize), feeding into a delivery layer comprising the summary pack, visualizations, and presentation to the operations team.",
                    "lineage": {
                        "concept_ids": ["capstone.documenting_presenting_deliverable"],
                        "teaching_block_ids": [
                            "capstone.documenting_presenting_deliverable#tb1",
                            "capstone.documenting_presenting_deliverable#tb2",
                            "capstone.documenting_presenting_deliverable#tb3"
                        ],
                        "fact_ids": ["capstone.documenting_presenting_deliverable#f1", "capstone.documenting_presenting_deliverable#f2"],
                        "anchors": ["capstone.documenting_presenting_deliverable#visual"]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": ["capstone.documenting_presenting_deliverable"],
                "teaching_block_ids": [
                    "capstone.documenting_presenting_deliverable#tb1",
                    "capstone.documenting_presenting_deliverable#tb2",
                    "capstone.documenting_presenting_deliverable#tb3"
                ],
                "fact_ids": [
                    "capstone.documenting_presenting_deliverable#f1",
                    "capstone.documenting_presenting_deliverable#f2"
                ],
                "anchors": ["capstone.documenting_presenting_deliverable#visual"]
            }
        },

        # ── s09: check – documenting_presenting_deliverable ──
        {
            "step_id": "tile_capstone_execution_narration_delivery.s09",
            "type": "check",
            "concept_ids": ["capstone.documenting_presenting_deliverable"],
            "eyebrow": "Quick Check",
            "title": "Delivery Formats",
            "lede": "Which of the following is NOT listed as a delivery and communication activity for the capstone?",
            "reward": {"gems": 5, "first_try_bonus": 2},
            "lineage": {
                "concept_ids": ["capstone.documenting_presenting_deliverable"],
                "teaching_block_ids": [],
                "fact_ids": ["capstone.documenting_presenting_deliverable#f2"],
                "anchors": ["capstone.documenting_presenting_deliverable#assessment:identify_and_select_appropriate_delivery_and_communication_formats"]
            }
        },

        # ── s10: hands_on – documenting_presenting_deliverable ──
        {
            "step_id": "tile_capstone_execution_narration_delivery.s10",
            "type": "hands_on",
            "concept_ids": ["capstone.documenting_presenting_deliverable"],
            "eyebrow": "Practice",
            "title": "Assemble the Capstone Deliverable",
            "lede": "Compile your QuickShip capstone work into a complete deliverable: a documentation section covering decisions and QA checks at each stage, plus the summary pack, visualizations, and a short presentation for the operations team.",
            "reward": {"gems": 15},
            "lineage": {
                "concept_ids": ["capstone.documenting_presenting_deliverable"],
                "teaching_block_ids": [],
                "fact_ids": [
                    "capstone.documenting_presenting_deliverable#f1",
                    "capstone.documenting_presenting_deliverable#f2"
                ],
                "anchors": [
                    "capstone.documenting_presenting_deliverable#practice",
                    "capstone.documenting_presenting_deliverable#assessment:produce_transparent_documentation_of_analytical_decisions",
                    "capstone.documenting_presenting_deliverable#assessment:assemble_capstone_work_into_an_evaluable_deliverable"
                ]
            }
        },

        # ── s11: recap ──
        {
            "step_id": "tile_capstone_execution_narration_delivery.s11",
            "type": "recap",
            "concept_ids": [
                "capstone.independent_execution",
                "capstone.narrated_stakeholder_summary",
                "capstone.documenting_presenting_deliverable"
            ],
            "eyebrow": "Recap",
            "title": "What You Learned",
            "lede": "Three ideas that complete the capstone.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_execution_narration_delivery.s11.p1",
                    "role": "takeaway",
                    "text": "Independent execution is running the whole plan yourself, adjusting it as needed, and keeping a decision log along the way. A narrated summary aimed at one specific person — moving through beginning, middle, and end — turns findings into something the audience can act on. Documenting the decisions made and presenting the finished report and visuals together is what makes the capstone a deliverable someone else can evaluate.",
                    "lineage": {
                        "concept_ids": [
                            "capstone.independent_execution",
                            "capstone.narrated_stakeholder_summary",
                            "capstone.documenting_presenting_deliverable"
                        ],
                        "teaching_block_ids": [
                            "capstone.independent_execution#tb4",
                            "capstone.narrated_stakeholder_summary#tb5",
                            "capstone.documenting_presenting_deliverable#tb4"
                        ],
                        "fact_ids": [
                            "capstone.documenting_presenting_deliverable#f1",
                            "capstone.documenting_presenting_deliverable#f2",
                            "capstone.independent_execution#f1",
                            "capstone.independent_execution#f2",
                            "capstone.narrated_stakeholder_summary#f1",
                            "capstone.narrated_stakeholder_summary#f2",
                            "capstone.narrated_stakeholder_summary#f3"
                        ]
                    }
                }
            ],
            "reward": {"gems": 5},
            "lineage": {
                "concept_ids": [
                    "capstone.independent_execution",
                    "capstone.narrated_stakeholder_summary",
                    "capstone.documenting_presenting_deliverable"
                ],
                "teaching_block_ids": [
                    "capstone.independent_execution#tb4",
                    "capstone.narrated_stakeholder_summary#tb5",
                    "capstone.documenting_presenting_deliverable#tb4"
                ],
                "fact_ids": [
                    "capstone.documenting_presenting_deliverable#f1",
                    "capstone.documenting_presenting_deliverable#f2",
                    "capstone.independent_execution#f1",
                    "capstone.independent_execution#f2",
                    "capstone.narrated_stakeholder_summary#f1",
                    "capstone.narrated_stakeholder_summary#f2",
                    "capstone.narrated_stakeholder_summary#f3"
                ]
            }
        }
    ],

    "remediation_steps": [
        {
            "step_id": "tile_capstone_execution_narration_delivery.r01",
            "type": "remediation",
            "concept_ids": ["capstone.independent_execution"],
            "eyebrow": "Let's revisit",
            "title": "Design Phase vs. Analysis Phase",
            "lede": "Independent execution has two distinct phases — and both produce something.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_execution_narration_delivery.r01.p1",
                    "role": "definition",
                    "text": "During the design phase, the commission is converted into an analytical plan, with some iteration expected. During the analysis phase, the planned analysis is carried out while progress and relevance are monitored, and records of the analysis conducted, changes, decisions, and assumptions made are maintained. The design phase produces the plan; the analysis phase produces the outputs and the decision log.",
                    "lineage": {
                        "concept_ids": ["capstone.independent_execution"],
                        "teaching_block_ids": ["capstone.independent_execution#tb2", "capstone.independent_execution#tb3"],
                        "fact_ids": ["capstone.independent_execution#f1", "capstone.independent_execution#f2"]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["capstone.independent_execution"],
                "teaching_block_ids": ["capstone.independent_execution#tb2", "capstone.independent_execution#tb3"],
                "fact_ids": ["capstone.independent_execution#f1", "capstone.independent_execution#f2"]
            }
        },
        {
            "step_id": "tile_capstone_execution_narration_delivery.r02",
            "type": "remediation",
            "concept_ids": ["capstone.narrated_stakeholder_summary"],
            "eyebrow": "Let's revisit",
            "title": "Beginning, Middle, End — Applied",
            "lede": "A story structure makes the summary usable, not just readable.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_execution_narration_delivery.r02.p1",
                    "role": "mechanism",
                    "text": "The beginning level-sets the audience with the big picture and background context. The middle presents what the analysis found. The ending gives the key takeaway, such as a recommended next step. For the QuickShip capstone: beginning — the 25-minute delivery target; middle — Lagos-North and Lagos-South are both missing it; end — add one courier to the Lagos route.",
                    "lineage": {
                        "concept_ids": ["capstone.narrated_stakeholder_summary"],
                        "teaching_block_ids": ["capstone.narrated_stakeholder_summary#tb3"],
                        "fact_ids": ["capstone.narrated_stakeholder_summary#f3"]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["capstone.narrated_stakeholder_summary"],
                "teaching_block_ids": ["capstone.narrated_stakeholder_summary#tb3"],
                "fact_ids": ["capstone.narrated_stakeholder_summary#f3"]
            }
        },
        {
            "step_id": "tile_capstone_execution_narration_delivery.r03",
            "type": "remediation",
            "concept_ids": ["capstone.documenting_presenting_deliverable"],
            "eyebrow": "Let's revisit",
            "title": "Documentation Makes the Work Evaluable",
            "lede": "A deliverable is not just finished work — it is finished work that someone else can understand and evaluate.",
            "blocks": [
                {
                    "type": "prose",
                    "block_id": "tile_capstone_execution_narration_delivery.r03.p1",
                    "role": "definition",
                    "text": "Transparency about the analytical decisions, process, limitations, and changes made at each stage should be clearly shown through documentation of the analysis, assumptions, and data, together with records of the decisions and quality-assurance checks made. Delivery activities can include summary packs, reports, dashboards, and presentations. Together, the documentation and the delivery layer make the capstone a deliverable someone else can evaluate — not just finished work only you understand.",
                    "lineage": {
                        "concept_ids": ["capstone.documenting_presenting_deliverable"],
                        "teaching_block_ids": ["capstone.documenting_presenting_deliverable#tb2", "capstone.documenting_presenting_deliverable#tb3"],
                        "fact_ids": ["capstone.documenting_presenting_deliverable#f1", "capstone.documenting_presenting_deliverable#f2"]
                    }
                }
            ],
            "reward": {"gems": 3},
            "lineage": {
                "concept_ids": ["capstone.documenting_presenting_deliverable"],
                "teaching_block_ids": ["capstone.documenting_presenting_deliverable#tb2", "capstone.documenting_presenting_deliverable#tb3"],
                "fact_ids": ["capstone.documenting_presenting_deliverable#f1", "capstone.documenting_presenting_deliverable#f2"]
            }
        }
    ]
}

out["tiles"].append(tile_capstone_end)

# Write output
with open('batches/final_batch_004_da_chunk2/screens.part.c1.json', 'w') as f:
    json.dump(out, f, indent=2)

print("Written successfully.")
print(f"Tiles: {len(out['tiles'])}")
for t in out['tiles']:
    print(f"  {t['tile_id']}: {len(t['steps'])} steps, {len(t.get('remediation_steps',[]))} remediation steps")
EOF
