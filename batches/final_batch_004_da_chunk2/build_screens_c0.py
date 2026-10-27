"""Build screens.part.c0_canary.json for tile_stakeholder_prioritizing_framing_context.
Word budgets apply to prose blocks only (not visual block text/takeaway/change_summary).
"""
import json, pathlib

TILE_ID = "tile_stakeholder_prioritizing_framing_context"
BATCH_ID = "final_batch_004_da_chunk2"

def sid(n): return f"{TILE_ID}.s{n:02d}"
def bid(s, b): return f"{TILE_ID}.{s}.b{b}"

# ── word-count helper ─────────────────────────────────────────────────────────
def wc(text): return len(text.split())

# ── s01: explainer — tb1/tb2/tb3, f1/f2/f3, side_by_side visual ──────────────
# Budget: 144 prose words across all prose blocks

P_s01_b1 = (
    "A full look at QuickShip delivery times might surface several findings: "
    "Lagos slowed down, Kano's times are the most variable, one courier is unusually fast. "
    "Not all of them belong at the top of the report to the Head of Operations."
)  # ~38 words

P_s01_b2 = (
    "The engagement and scoping stage of an analytical project should establish an understanding "
    "of how the analysis will inform decisions. "
    "That decision — whether to add Lagos couriers — points to which finding matters most: "
    "the Lagos slowdown, not the courier with the fastest times. "
    "Crafting a communication's big idea requires knowing what is not essential, "
    "and boiling the overall message down to a single sentence that captures its core."
)  # ~72 words

P_s01_b3 = (
    "Writing about data should only include information relevant to the audience. "
    "The operations manager's decision about Lagos staffing does not require the full breakdown "
    "of every city's variability. "
    "Filtering by relevance to the decision — not by analytical novelty — "
    "is what separates a useful report from an exhaustive one."
)  # ~46 words

# Total prose: 38+72+46 = 156 — slightly over 144. Trim b2 and b3.

P_s01_b2 = (
    "The engagement and scoping stage should establish how the analysis will inform decisions. "
    "That decision — whether to add Lagos couriers — points to which finding matters most: "
    "the Lagos slowdown, not the courier with the fastest times. "
    "Crafting a communication's big idea requires knowing what is not essential "
    "and boiling the message down to a single sentence."
)  # ~60 words

P_s01_b3 = (
    "Writing about data should only include information relevant to the audience. "
    "The operations manager's decision about Lagos staffing does not require "
    "the full breakdown of every city's variability. "
    "Relevance to the decision — not analytical novelty — is the right criterion."
)  # ~38 words

# Total: 38+60+38 = 136 ✓

def s01():
    return {
        "step_id": sid(1),
        "type": "explainer",
        "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
        "eyebrow": "Prioritizing Findings",
        "title": "Lead with what the decision-maker needs, not what surprised you most",
        "lede": "A delivery-times analysis can surface many findings. Choosing which one opens the report is a judgment call — and the right criterion is the stakeholder's decision, not analytical novelty.",
        "blocks": [
            {
                "type": "prose",
                "block_id": bid("s01", 1),
                "role": "intro",
                "text": P_s01_b1,
                "lineage": {
                    "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
                    "teaching_block_ids": ["stakeholder.prioritizing_findings_by_relevance#tb1"],
                    "fact_ids": []
                }
            },
            {
                "type": "prose",
                "block_id": bid("s01", 2),
                "role": "mechanism",
                "text": P_s01_b2,
                "lineage": {
                    "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
                    "teaching_block_ids": [
                        "stakeholder.prioritizing_findings_by_relevance#tb2",
                        "stakeholder.prioritizing_findings_by_relevance#tb3"
                    ],
                    "fact_ids": [
                        "stakeholder.prioritizing_findings_by_relevance#f1",
                        "stakeholder.prioritizing_findings_by_relevance#f2"
                    ]
                }
            },
            {
                "type": "prose",
                "block_id": bid("s01", 3),
                "role": "mechanism",
                "text": P_s01_b3,
                "lineage": {
                    "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
                    "teaching_block_ids": ["stakeholder.prioritizing_findings_by_relevance#tb3"],
                    "fact_ids": [
                        "stakeholder.prioritizing_findings_by_relevance#f2",
                        "stakeholder.prioritizing_findings_by_relevance#f3"
                    ]
                }
            },
            {
                "type": "side_by_side",
                "block_id": bid("s01", 4),
                "left_label": "Ordered by analytical interestingness",
                "right_label": "Ordered by relevance to the staffing decision",
                "left": {
                    "type": "data_table",
                    "asset_ref": {
                        "asset_id": "ds_city_delivery_summary",
                        "variant_id": None,
                        "columns": ["city", "avg_delivery_min", "variability_rank", "finding_priority"]
                    },
                    "caption": "Findings ranked by what is most analytically notable",
                    "highlight": [
                        {
                            "target": {"kind": "row", "row": {"where": {"city": "Kano"}}},
                            "label": "Most variable — analytically interesting",
                            "tone": "neutral"
                        }
                    ]
                },
                "right": {
                    "type": "data_table",
                    "asset_ref": {
                        "asset_id": "ds_city_delivery_summary",
                        "variant_id": None,
                        "columns": ["city", "avg_delivery_min", "target_min", "finding_priority"]
                    },
                    "caption": "Findings ranked by relevance to the Lagos staffing decision",
                    "highlight": [
                        {
                            "target": {"kind": "row", "row": {"where": {"city": "Lagos"}}},
                            "label": "Primary — directly informs the staffing decision",
                            "tone": "focus"
                        }
                    ]
                },
                "takeaway": (
                    "Same dataset, two orderings. "
                    "Kano leads when ranked by analytical interestingness; "
                    "Lagos leads when ranked by relevance to the decision. "
                    "The stakeholder's decision is the right criterion."
                ),
                "lineage": {
                    "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
                    "teaching_block_ids": [
                        "stakeholder.prioritizing_findings_by_relevance#tb2",
                        "stakeholder.prioritizing_findings_by_relevance#tb3"
                    ],
                    "fact_ids": [
                        "stakeholder.prioritizing_findings_by_relevance#f1",
                        "stakeholder.prioritizing_findings_by_relevance#f2",
                        "stakeholder.prioritizing_findings_by_relevance#f3"
                    ],
                    "anchors": ["stakeholder.prioritizing_findings_by_relevance#visual"]
                }
            }
        ],
        "reward": {"gems": 5},
        "lineage": {
            "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
            "teaching_block_ids": [
                "stakeholder.prioritizing_findings_by_relevance#tb1",
                "stakeholder.prioritizing_findings_by_relevance#tb2",
                "stakeholder.prioritizing_findings_by_relevance#tb3"
            ],
            "fact_ids": [
                "stakeholder.prioritizing_findings_by_relevance#f1",
                "stakeholder.prioritizing_findings_by_relevance#f2",
                "stakeholder.prioritizing_findings_by_relevance#f3"
            ],
            "anchors": ["stakeholder.prioritizing_findings_by_relevance#visual"]
        }
    }


# ── s02: explainer — tb4, f4 (inverted pyramid) ───────────────────────────────
# Budget: 41 prose words

P_s02_b1 = (
    "Use the inverted pyramid: the most important information should be first, "
    "and everything else arranged from most to least important. "
    "For the QuickShip delivery report, the Lagos slowdown opens the report; "
    "Kano and Abuja follow only if relevant to the reader's decision."
)  # ~42 words — trim slightly

P_s02_b1 = (
    "Use the inverted pyramid: most important information first, "
    "everything else from most to least important. "
    "For the QuickShip delivery report, the Lagos slowdown opens the report; "
    "other findings follow only if relevant to the decision."
)  # ~36 words ✓

def s02():
    return {
        "step_id": sid(2),
        "type": "explainer",
        "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
        "eyebrow": "Prioritizing Findings",
        "title": "Put the most important finding first",
        "lede": "Once you know which finding matters most, the inverted pyramid tells you where to put it.",
        "blocks": [
            {
                "type": "prose",
                "block_id": bid("s02", 1),
                "role": "workflow",
                "text": P_s02_b1,
                "lineage": {
                    "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
                    "teaching_block_ids": ["stakeholder.prioritizing_findings_by_relevance#tb4"],
                    "fact_ids": ["stakeholder.prioritizing_findings_by_relevance#f4"]
                }
            }
        ],
        "reward": {"gems": 3},
        "lineage": {
            "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
            "teaching_block_ids": ["stakeholder.prioritizing_findings_by_relevance#tb4"],
            "fact_ids": ["stakeholder.prioritizing_findings_by_relevance#f4"]
        }
    }


# ── s03: check — f1/f2/f3, framing only ──────────────────────────────────────
def s03():
    return {
        "step_id": sid(3),
        "type": "check",
        "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
        "eyebrow": "Quick Check",
        "title": "Which finding should lead the report?",
        "lede": "Apply the relevance-to-decision criterion to the QuickShip scenario.",
        "reward": {"gems": 5, "first_try_bonus": 2},
        "lineage": {
            "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
            "teaching_block_ids": [],
            "fact_ids": [
                "stakeholder.prioritizing_findings_by_relevance#f1",
                "stakeholder.prioritizing_findings_by_relevance#f2",
                "stakeholder.prioritizing_findings_by_relevance#f3"
            ],
            "anchors": [
                "stakeholder.prioritizing_findings_by_relevance#assessment:identify_decision_context_from_scoping_stage",
                "stakeholder.prioritizing_findings_by_relevance#assessment:distill_big_idea_and_exclude_irrelevant_findings"
            ]
        }
    }


# ── s04: check — f4, framing only ────────────────────────────────────────────
def s04():
    return {
        "step_id": sid(4),
        "type": "check",
        "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
        "eyebrow": "Quick Check",
        "title": "Applying the inverted pyramid",
        "lede": "Use the inverted pyramid rule to order findings in a stakeholder report.",
        "reward": {"gems": 5, "first_try_bonus": 2},
        "lineage": {
            "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
            "teaching_block_ids": [],
            "fact_ids": ["stakeholder.prioritizing_findings_by_relevance#f4"],
            "anchors": [
                "stakeholder.prioritizing_findings_by_relevance#assessment:rank_findings_using_inverted_pyramid"
            ]
        }
    }


# ── s05: hands_on — ordering practice, framing only ──────────────────────────
def s05():
    return {
        "step_id": sid(5),
        "type": "hands_on",
        "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
        "eyebrow": "Practice",
        "title": "Order these findings for the Head of Operations",
        "lede": (
            "Given five findings from the QuickShip delivery analysis, "
            "drag them into the order you would present them to the Head of Operations, "
            "who is deciding whether to add Lagos couriers."
        ),
        "reward": {"gems": 10, "first_try_bonus": 5},
        "lineage": {
            "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
            "teaching_block_ids": [],
            "fact_ids": [
                "stakeholder.prioritizing_findings_by_relevance#f1",
                "stakeholder.prioritizing_findings_by_relevance#f2",
                "stakeholder.prioritizing_findings_by_relevance#f3",
                "stakeholder.prioritizing_findings_by_relevance#f4"
            ],
            "anchors": [
                "stakeholder.prioritizing_findings_by_relevance#practice",
                "stakeholder.prioritizing_findings_by_relevance#assessment:prioritize_findings_by_stakeholder_decision_relevance"
            ]
        }
    }


# ── s06: explainer — tb1/tb2/tb3, f1/f2, before_after visual ─────────────────
# Budget: 160 prose words

P_s06_b1 = (
    "\"Lagos delivery times rose to 30 minutes\" is a finding — it describes what the data shows. "
    "\"We recommend adding one more courier to the Lagos route\" is a recommendation: "
    "it states what should happen next. "
    "The two are easy to confuse, but a stakeholder needs both."
)  # ~44 words

P_s06_b2 = (
    "The value of analytical efforts is only truly realized when the insights discovered are acted upon. "
    "An audience cannot be assumed to find the intended takeaway as obvious as the presenter thinks it is. "
    "Simply restating the Lagos finding more emphatically may not tell the manager what to do — "
    "the recommendation needs to say so explicitly."
)  # ~55 words

P_s06_b3 = (
    "A well-formed recommendation makes clear to the audience what they need to know "
    "and what they are being asked to do. "
    "\"We recommend adding one Lagos courier; please approve the added headcount\" "
    "states the action and names the explicit ask, "
    "so the Head of Operations knows exactly what decision is in front of them."
)  # ~55 words

# Total: 44+55+55 = 154 ✓ (under 160)

def s06():
    return {
        "step_id": sid(6),
        "type": "explainer",
        "concept_ids": ["stakeholder.actionable_recommendation_framing"],
        "eyebrow": "Framing Recommendations",
        "title": "A finding tells you what happened; a recommendation says what to do",
        "lede": "Restating a finding more emphatically is not a recommendation. A recommendation names the action and what the reader is being asked to approve.",
        "blocks": [
            {
                "type": "prose",
                "block_id": bid("s06", 1),
                "role": "intro",
                "text": P_s06_b1,
                "lineage": {
                    "concept_ids": ["stakeholder.actionable_recommendation_framing"],
                    "teaching_block_ids": ["stakeholder.actionable_recommendation_framing#tb1"],
                    "fact_ids": []
                }
            },
            {
                "type": "prose",
                "block_id": bid("s06", 2),
                "role": "mechanism",
                "text": P_s06_b2,
                "lineage": {
                    "concept_ids": ["stakeholder.actionable_recommendation_framing"],
                    "teaching_block_ids": ["stakeholder.actionable_recommendation_framing#tb2"],
                    "fact_ids": ["stakeholder.actionable_recommendation_framing#f1"]
                }
            },
            {
                "type": "prose",
                "block_id": bid("s06", 3),
                "role": "example",
                "text": P_s06_b3,
                "lineage": {
                    "concept_ids": ["stakeholder.actionable_recommendation_framing"],
                    "teaching_block_ids": ["stakeholder.actionable_recommendation_framing#tb3"],
                    "fact_ids": ["stakeholder.actionable_recommendation_framing#f2"]
                }
            },
            {
                "type": "before_after",
                "block_id": bid("s06", 4),
                "before": {
                    "type": "diagram",
                    "diagram_kind": "container",
                    "title": "Finding only (weak)",
                    "nodes": [
                        {
                            "id": "finding_only",
                            "label": "Lagos delivery times rose to 30 minutes — above the 25-minute target.",
                            "kind": "finding"
                        }
                    ],
                    "alt_text": "A text box showing only the finding: 'Lagos delivery times rose to 30 minutes — above the 25-minute target.' No action is stated."
                },
                "after": {
                    "type": "diagram",
                    "diagram_kind": "container",
                    "title": "Finding + recommendation (strong)",
                    "nodes": [
                        {
                            "id": "finding_node",
                            "label": "Finding: Lagos delivery times rose to 30 minutes — above the 25-minute target.",
                            "kind": "finding"
                        },
                        {
                            "id": "recommendation_node",
                            "label": "Recommendation: We recommend adding one Lagos courier; please approve the added headcount.",
                            "kind": "recommendation"
                        }
                    ],
                    "alt_text": "Two text boxes: the finding ('Lagos delivery times rose to 30 minutes — above the 25-minute target') followed by a distinct recommendation ('We recommend adding one Lagos courier; please approve the added headcount'), showing the structural difference between restating data and stating an action."
                },
                "change_summary": (
                    "Adding an explicit recommendation — naming the action and the ask — "
                    "transforms a finding into something the Head of Operations can act on."
                ),
                "lineage": {
                    "concept_ids": ["stakeholder.actionable_recommendation_framing"],
                    "teaching_block_ids": [
                        "stakeholder.actionable_recommendation_framing#tb1",
                        "stakeholder.actionable_recommendation_framing#tb2",
                        "stakeholder.actionable_recommendation_framing#tb3"
                    ],
                    "fact_ids": [
                        "stakeholder.actionable_recommendation_framing#f1",
                        "stakeholder.actionable_recommendation_framing#f2"
                    ],
                    "anchors": ["stakeholder.actionable_recommendation_framing#visual"]
                }
            }
        ],
        "reward": {"gems": 5},
        "lineage": {
            "concept_ids": ["stakeholder.actionable_recommendation_framing"],
            "teaching_block_ids": [
                "stakeholder.actionable_recommendation_framing#tb1",
                "stakeholder.actionable_recommendation_framing#tb2",
                "stakeholder.actionable_recommendation_framing#tb3"
            ],
            "fact_ids": [
                "stakeholder.actionable_recommendation_framing#f1",
                "stakeholder.actionable_recommendation_framing#f2"
            ],
            "anchors": ["stakeholder.actionable_recommendation_framing#visual"]
        }
    }


# ── s07: check — f2, framing only ────────────────────────────────────────────
def s07():
    return {
        "step_id": sid(7),
        "type": "check",
        "concept_ids": ["stakeholder.actionable_recommendation_framing"],
        "eyebrow": "Quick Check",
        "title": "Finding or recommendation?",
        "lede": "Identify which statement is a properly framed recommendation with an explicit ask.",
        "reward": {"gems": 5, "first_try_bonus": 2},
        "lineage": {
            "concept_ids": ["stakeholder.actionable_recommendation_framing"],
            "teaching_block_ids": [],
            "fact_ids": ["stakeholder.actionable_recommendation_framing#f2"],
            "anchors": [
                "stakeholder.actionable_recommendation_framing#assessment:write_actionable_recommendation_with_explicit_ask"
            ]
        }
    }


# ── s08: hands_on — table_select practice, framing only ──────────────────────
def s08():
    return {
        "step_id": sid(8),
        "type": "hands_on",
        "concept_ids": ["stakeholder.actionable_recommendation_framing"],
        "eyebrow": "Practice",
        "title": "Select the correctly framed recommendation",
        "lede": (
            "Below are several statements about the QuickShip delivery data. "
            "Select the one that is a properly framed recommendation — "
            "distinct from the finding and with an explicit ask."
        ),
        "reward": {"gems": 10, "first_try_bonus": 5},
        "lineage": {
            "concept_ids": ["stakeholder.actionable_recommendation_framing"],
            "teaching_block_ids": [],
            "fact_ids": [
                "stakeholder.actionable_recommendation_framing#f1",
                "stakeholder.actionable_recommendation_framing#f2"
            ],
            "anchors": [
                "stakeholder.actionable_recommendation_framing#practice",
                "stakeholder.actionable_recommendation_framing#assessment:distinguish_recommendation_from_finding",
                "stakeholder.actionable_recommendation_framing#assessment:write_actionable_recommendation_with_explicit_ask"
            ]
        }
    }


# ── s09: explainer — tb1/tb2/tb3/tb4, f1/f2/f3/f4, before_after visual ───────
# Budget: 177 prose words

P_s09_b1 = (
    "Before the Head of Operations reads any finding about Lagos delivery times, "
    "they need to know why they are reading this report at all. "
    "Dropping straight into numbers without context leaves the reader to guess "
    "the purpose of the analysis."
)  # ~38 words

P_s09_b2 = (
    "In a story's structure, the beginning establishes the context: "
    "what is happening, or what the situation is, when the story begins. "
    "A summary should have an obvious beginning, middle, and end; "
    "the beginning level-sets the audience before diving into the analysis. "
    "For the delivery report, the beginning answers: what does this report cover, and why was it done?"
)  # ~57 words

P_s09_b3 = (
    "A report should not start with lengthy background information or technical definitions. "
    "Instead, include a short paragraph explaining what the publication is about. "
    "For the delivery report, that means a short opener — "
    "\"This report looks at delivery times across our three cities this quarter\" — "
    "rather than a page of methodology before getting to the point."
)  # ~52 words

P_s09_b4 = (
    "Explaining why the statistics have been collected includes relevant, factual information "
    "about the policy and operational context. "
    "Noting that this review was prompted by rising customer complaints about Lagos deliveries "
    "gives the reader a reason the analysis exists at all."
)  # ~38 words

# Total: 38+57+52+38 = 185 — slightly over 177. Trim b2 and b3.

P_s09_b2 = (
    "In a story's structure, the beginning establishes the context: "
    "what is happening when the story begins. "
    "A summary should have an obvious beginning, middle, and end; "
    "the beginning level-sets the audience before diving into the analysis."
)  # ~42 words

P_s09_b3 = (
    "A report should not start with lengthy background or technical definitions. "
    "Instead, include a short paragraph explaining what the publication is about. "
    "For the delivery report: \"This report looks at delivery times across our three cities this quarter\" — "
    "not a page of methodology before the findings."
)  # ~44 words

# Total: 38+42+44+38 = 162 ✓ (under 177)

def s09():
    return {
        "step_id": sid(9),
        "type": "explainer",
        "concept_ids": ["stakeholder.narrative_context_setup"],
        "eyebrow": "Narrative Context",
        "title": "Start with why: set the context before the findings",
        "lede": "Before the Head of Operations reads any finding about Lagos delivery times, they need to know why they are reading this report at all.",
        "blocks": [
            {
                "type": "prose",
                "block_id": bid("s09", 1),
                "role": "intro",
                "text": P_s09_b1,
                "lineage": {
                    "concept_ids": ["stakeholder.narrative_context_setup"],
                    "teaching_block_ids": ["stakeholder.narrative_context_setup#tb1"],
                    "fact_ids": []
                }
            },
            {
                "type": "prose",
                "block_id": bid("s09", 2),
                "role": "definition",
                "text": P_s09_b2,
                "lineage": {
                    "concept_ids": ["stakeholder.narrative_context_setup"],
                    "teaching_block_ids": ["stakeholder.narrative_context_setup#tb2"],
                    "fact_ids": [
                        "stakeholder.narrative_context_setup#f1",
                        "stakeholder.narrative_context_setup#f2"
                    ]
                }
            },
            {
                "type": "prose",
                "block_id": bid("s09", 3),
                "role": "mechanism",
                "text": P_s09_b3,
                "lineage": {
                    "concept_ids": ["stakeholder.narrative_context_setup"],
                    "teaching_block_ids": ["stakeholder.narrative_context_setup#tb3"],
                    "fact_ids": ["stakeholder.narrative_context_setup#f3"]
                }
            },
            {
                "type": "prose",
                "block_id": bid("s09", 4),
                "role": "practical_context",
                "text": P_s09_b4,
                "lineage": {
                    "concept_ids": ["stakeholder.narrative_context_setup"],
                    "teaching_block_ids": ["stakeholder.narrative_context_setup#tb4"],
                    "fact_ids": ["stakeholder.narrative_context_setup#f4"]
                }
            },
            {
                "type": "before_after",
                "block_id": bid("s09", 5),
                "before": {
                    "type": "diagram",
                    "diagram_kind": "container",
                    "title": "Weak opener (lengthy background)",
                    "nodes": [
                        {
                            "id": "weak_opener",
                            "label": (
                                "QuickShip was founded in 2019 and operates across three Nigerian cities. "
                                "The company uses a proprietary routing algorithm. "
                                "Delivery times are measured from order placement to doorstep arrival. "
                                "This report uses SQL queries on the orders table and an Excel driver roster..."
                            ),
                            "kind": "text_block"
                        }
                    ],
                    "alt_text": "A text block showing a weak opener that buries the purpose in lengthy background: company history, technical definitions, and methodology before stating what the report is about."
                },
                "after": {
                    "type": "diagram",
                    "diagram_kind": "container",
                    "title": "Strong opener (short context section)",
                    "nodes": [
                        {
                            "id": "strong_opener",
                            "label": (
                                "This report examines delivery times across Lagos, Kano, and Abuja last quarter, "
                                "prompted by rising customer complaints about Lagos deliveries. "
                                "It answers: which zones are missing the 25-minute target, and by how much?"
                            ),
                            "kind": "text_block"
                        }
                    ],
                    "alt_text": "A text block showing a strong two-sentence opener: one sentence states what the report covers and why it was done; the second names the specific question it answers — no lengthy background."
                },
                "change_summary": (
                    "Two sentences replace a paragraph of background. "
                    "The strong opener immediately level-sets the reader on what the report covers, "
                    "why the analysis was done, and what question it answers."
                ),
                "lineage": {
                    "concept_ids": ["stakeholder.narrative_context_setup"],
                    "teaching_block_ids": [
                        "stakeholder.narrative_context_setup#tb1",
                        "stakeholder.narrative_context_setup#tb2",
                        "stakeholder.narrative_context_setup#tb3",
                        "stakeholder.narrative_context_setup#tb4"
                    ],
                    "fact_ids": [
                        "stakeholder.narrative_context_setup#f1",
                        "stakeholder.narrative_context_setup#f2",
                        "stakeholder.narrative_context_setup#f3",
                        "stakeholder.narrative_context_setup#f4"
                    ],
                    "anchors": ["stakeholder.narrative_context_setup#visual"]
                }
            }
        ],
        "reward": {"gems": 5},
        "lineage": {
            "concept_ids": ["stakeholder.narrative_context_setup"],
            "teaching_block_ids": [
                "stakeholder.narrative_context_setup#tb1",
                "stakeholder.narrative_context_setup#tb2",
                "stakeholder.narrative_context_setup#tb3",
                "stakeholder.narrative_context_setup#tb4"
            ],
            "fact_ids": [
                "stakeholder.narrative_context_setup#f1",
                "stakeholder.narrative_context_setup#f2",
                "stakeholder.narrative_context_setup#f3",
                "stakeholder.narrative_context_setup#f4"
            ],
            "anchors": ["stakeholder.narrative_context_setup#visual"]
        }
    }


# ── s10: check — f1/f2/f3, framing only ──────────────────────────────────────
def s10():
    return {
        "step_id": sid(10),
        "type": "check",
        "concept_ids": ["stakeholder.narrative_context_setup"],
        "eyebrow": "Quick Check",
        "title": "What belongs in the opening context section?",
        "lede": "Identify the correct role of the context section in a findings narrative.",
        "reward": {"gems": 5, "first_try_bonus": 2},
        "lineage": {
            "concept_ids": ["stakeholder.narrative_context_setup"],
            "teaching_block_ids": [],
            "fact_ids": [
                "stakeholder.narrative_context_setup#f1",
                "stakeholder.narrative_context_setup#f2",
                "stakeholder.narrative_context_setup#f3"
            ],
            "anchors": [
                "stakeholder.narrative_context_setup#assessment:identify_context_as_narrative_beginning",
                "stakeholder.narrative_context_setup#assessment:distinguish_short_opener_from_lengthy_background"
            ]
        }
    }


# ── s11: check — f4, framing only ────────────────────────────────────────────
def s11():
    return {
        "step_id": sid(11),
        "type": "check",
        "concept_ids": ["stakeholder.narrative_context_setup"],
        "eyebrow": "Quick Check",
        "title": "Including operational context in the opener",
        "lede": "Decide what factual context belongs in the opening section of a findings report.",
        "reward": {"gems": 5, "first_try_bonus": 2},
        "lineage": {
            "concept_ids": ["stakeholder.narrative_context_setup"],
            "teaching_block_ids": [],
            "fact_ids": ["stakeholder.narrative_context_setup#f4"],
            "anchors": [
                "stakeholder.narrative_context_setup#assessment:include_policy_and_operational_context_in_opening"
            ]
        }
    }


# ── s12: hands_on — external_proof practice, framing only ────────────────────
def s12():
    return {
        "step_id": sid(12),
        "type": "hands_on",
        "concept_ids": ["stakeholder.narrative_context_setup"],
        "eyebrow": "Practice",
        "title": "Write the opening context section",
        "lede": (
            "Write a two-sentence context section introducing the QuickShip delivery report. "
            "The first sentence should state what the report covers and why the analysis was done; "
            "the second should name the specific question the analysis answers."
        ),
        "reward": {"gems": 10, "first_try_bonus": 5},
        "lineage": {
            "concept_ids": ["stakeholder.narrative_context_setup"],
            "teaching_block_ids": [],
            "fact_ids": [
                "stakeholder.narrative_context_setup#f1",
                "stakeholder.narrative_context_setup#f2",
                "stakeholder.narrative_context_setup#f3",
                "stakeholder.narrative_context_setup#f4"
            ],
            "anchors": [
                "stakeholder.narrative_context_setup#practice",
                "stakeholder.narrative_context_setup#assessment:write_opening_context_section_for_findings_narrative"
            ]
        }
    }


# ── s13: recap — all three concepts, up_next block ───────────────────────────
# Budget: 90 prose words

P_s13_b1 = (
    "Lead with the finding most relevant to the stakeholder's decision, not the most analytically interesting one. "
    "Use the inverted pyramid: most important first, everything else from most to least important. "
    "Pair each finding with a distinct recommendation that names the action and the explicit ask. "
    "Open the report with a short context section that states what it covers, "
    "why the analysis was done, and what question it answers."
)  # ~73 words ✓

def s13():
    return {
        "step_id": sid(13),
        "type": "recap",
        "concept_ids": [
            "stakeholder.prioritizing_findings_by_relevance",
            "stakeholder.actionable_recommendation_framing",
            "stakeholder.narrative_context_setup"
        ],
        "eyebrow": "Recap",
        "title": "What you covered",
        "lede": "Three principles for structuring a findings narrative that a stakeholder can act on.",
        "blocks": [
            {
                "type": "prose",
                "block_id": bid("s13", 1),
                "role": "takeaway",
                "text": P_s13_b1,
                "lineage": {
                    "concept_ids": [
                        "stakeholder.prioritizing_findings_by_relevance",
                        "stakeholder.actionable_recommendation_framing",
                        "stakeholder.narrative_context_setup"
                    ],
                    "teaching_block_ids": [],
                    "fact_ids": []
                }
            },
            {
                "type": "up_next",
                "block_id": bid("s13", 2),
                "title": "Up next: Tailoring your message to the audience",
                "text": (
                    "The next lesson covers how to adjust the level of detail and framing "
                    "to match what different audiences — executives, technical peers, operations managers — "
                    "actually need from a findings report."
                )
            }
        ],
        "reward": {"gems": 5},
        "lineage": {
            "concept_ids": [
                "stakeholder.prioritizing_findings_by_relevance",
                "stakeholder.actionable_recommendation_framing",
                "stakeholder.narrative_context_setup"
            ],
            "teaching_block_ids": [],
            "fact_ids": [],
            "anchors": []
        }
    }


# ── remediation steps ─────────────────────────────────────────────────────────

def r01():
    """Remediation for s03 (first check of prioritizing_findings_by_relevance)"""
    return {
        "step_id": f"{TILE_ID}.r01",
        "type": "remediation",
        "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
        "eyebrow": "Let's revisit",
        "title": "Decision relevance vs. analytical interestingness — a clear contrast",
        "lede": "Two analysts look at the same QuickShip data and choose different findings to lead with. Only one is using the right criterion.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.r01.b1",
                "role": "example",
                "text": (
                    "Analyst A leads with Kano's high delivery-time variability — the most statistically unusual finding. "
                    "Analyst B leads with the Lagos slowdown — the finding most directly tied to the staffing decision. "
                    "The Head of Operations is deciding whether to add Lagos couriers. "
                    "Analyst B is correct: the criterion is relevance to the decision, not analytical novelty."
                ),
                "lineage": {
                    "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
                    "teaching_block_ids": [
                        "stakeholder.prioritizing_findings_by_relevance#tb2",
                        "stakeholder.prioritizing_findings_by_relevance#tb3"
                    ],
                    "fact_ids": [
                        "stakeholder.prioritizing_findings_by_relevance#f1",
                        "stakeholder.prioritizing_findings_by_relevance#f2",
                        "stakeholder.prioritizing_findings_by_relevance#f3"
                    ]
                }
            }
        ],
        "reward": {"gems": 2},
        "lineage": {
            "concept_ids": ["stakeholder.prioritizing_findings_by_relevance"],
            "teaching_block_ids": [
                "stakeholder.prioritizing_findings_by_relevance#tb2",
                "stakeholder.prioritizing_findings_by_relevance#tb3"
            ],
            "fact_ids": [
                "stakeholder.prioritizing_findings_by_relevance#f1",
                "stakeholder.prioritizing_findings_by_relevance#f2",
                "stakeholder.prioritizing_findings_by_relevance#f3"
            ]
        }
    }


def r02():
    """Remediation for s07 (first check of actionable_recommendation_framing)"""
    return {
        "step_id": f"{TILE_ID}.r02",
        "type": "remediation",
        "concept_ids": ["stakeholder.actionable_recommendation_framing"],
        "eyebrow": "Let's revisit",
        "title": "Finding vs. recommendation — the structural difference",
        "lede": "A finding describes what the data shows. A recommendation states what action to take and what the reader is being asked to do.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.r02.b1",
                "role": "example",
                "text": (
                    "Finding: \"Lagos delivery times rose to 30 minutes — above the 25-minute target.\" "
                    "This describes the data. It does not tell the Head of Operations what to do. "
                    "Recommendation: \"We recommend adding one Lagos courier; please approve the added headcount.\" "
                    "This names the action and the explicit ask. "
                    "A recommendation is not a louder restatement of the finding — "
                    "it is a distinct statement of what should happen next."
                ),
                "lineage": {
                    "concept_ids": ["stakeholder.actionable_recommendation_framing"],
                    "teaching_block_ids": [
                        "stakeholder.actionable_recommendation_framing#tb1",
                        "stakeholder.actionable_recommendation_framing#tb3"
                    ],
                    "fact_ids": [
                        "stakeholder.actionable_recommendation_framing#f1",
                        "stakeholder.actionable_recommendation_framing#f2"
                    ]
                }
            }
        ],
        "reward": {"gems": 2},
        "lineage": {
            "concept_ids": ["stakeholder.actionable_recommendation_framing"],
            "teaching_block_ids": [
                "stakeholder.actionable_recommendation_framing#tb1",
                "stakeholder.actionable_recommendation_framing#tb3"
            ],
            "fact_ids": [
                "stakeholder.actionable_recommendation_framing#f1",
                "stakeholder.actionable_recommendation_framing#f2"
            ]
        }
    }


def r03():
    """Remediation for s10 (first check of narrative_context_setup)"""
    return {
        "step_id": f"{TILE_ID}.r03",
        "type": "remediation",
        "concept_ids": ["stakeholder.narrative_context_setup"],
        "eyebrow": "Let's revisit",
        "title": "Short opener vs. lengthy background — the contrast",
        "lede": "The opening context section should be short and purposeful, not a page of background before the findings.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE_ID}.r03.b1",
                "role": "example",
                "text": (
                    "A weak opener spends a paragraph on company history, technical definitions, and methodology "
                    "before the reader knows what the report is about. "
                    "A strong opener uses two sentences: one states what the report covers and why the analysis was done; "
                    "the second names the specific question it answers. "
                    "For the QuickShip delivery report: "
                    "\"This report examines delivery times across Lagos, Kano, and Abuja last quarter, "
                    "prompted by rising customer complaints about Lagos deliveries. "
                    "It answers: which zones are missing the 25-minute target, and by how much?\""
                ),
                "lineage": {
                    "concept_ids": ["stakeholder.narrative_context_setup"],
                    "teaching_block_ids": [
                        "stakeholder.narrative_context_setup#tb2",
                        "stakeholder.narrative_context_setup#tb3"
                    ],
                    "fact_ids": [
                        "stakeholder.narrative_context_setup#f1",
                        "stakeholder.narrative_context_setup#f2",
                        "stakeholder.narrative_context_setup#f3"
                    ]
                }
            }
        ],
        "reward": {"gems": 2},
        "lineage": {
            "concept_ids": ["stakeholder.narrative_context_setup"],
            "teaching_block_ids": [
                "stakeholder.narrative_context_setup#tb2",
                "stakeholder.narrative_context_setup#tb3"
            ],
            "fact_ids": [
                "stakeholder.narrative_context_setup#f1",
                "stakeholder.narrative_context_setup#f2",
                "stakeholder.narrative_context_setup#f3"
            ]
        }
    }


# ── assemble ──────────────────────────────────────────────────────────────────

artifact = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": BATCH_ID,
    "tiles": [
        {
            "tile_id": TILE_ID,
            "title": "Prioritizing Findings and Framing Recommendations",
            "summary": (
                "Learn to lead a stakeholder report with the finding most relevant to the decision, "
                "frame a recommendation that is distinct from the finding itself, "
                "and open the narrative with a short context section that level-sets the reader."
            ),
            "steps": [
                s01(), s02(), s03(), s04(), s05(),
                s06(), s07(), s08(),
                s09(), s10(), s11(), s12(),
                s13()
            ],
            "remediation_steps": [r01(), r02(), r03()]
        }
    ]
}

# ── verify word counts ────────────────────────────────────────────────────────
budgets = {'s01': 144, 's02': 41, 's06': 160, 's09': 177, 's13': 90}
for step in artifact['tiles'][0]['steps']:
    sid_short = step['step_id'].split('.')[-1]
    if sid_short in budgets:
        prose_words = sum(
            len(b.get('text','').split())
            for b in step.get('blocks', [])
            if b.get('type') == 'prose'
        )
        budget = budgets[sid_short]
        status = 'OK' if prose_words <= budget else 'OVER'
        print(f"  {step['step_id']}: prose={prose_words} budget={budget} {status}")

out = pathlib.Path(f"batches/{BATCH_ID}/screens.part.c0_canary.json")
out.write_text(json.dumps(artifact, indent=2, ensure_ascii=False))
print(f"\nWritten: {out}")
print(f"Steps: {len(artifact['tiles'][0]['steps'])}")
print(f"Remediation steps: {len(artifact['tiles'][0]['remediation_steps'])}")
