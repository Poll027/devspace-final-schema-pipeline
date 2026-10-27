"""Build interactions.part.c0_canary.json for tile_stakeholder_prioritizing_framing_context.

Steps with interactions (check/hands_on):
  s03 - check - choice       - prioritizing_findings_by_relevance f1,f2,f3
  s04 - check - choice       - prioritizing_findings_by_relevance f4
  s05 - hands_on - ordering  - prioritizing_findings_by_relevance f1-f4 (practice)
  s07 - check - choice       - actionable_recommendation_framing f2
  s08 - hands_on - table_select - actionable_recommendation_framing f1,f2 (practice)
  s10 - check - choice       - narrative_context_setup f1,f2,f3
  s11 - check - choice       - narrative_context_setup f4
  s12 - hands_on - external_proof - narrative_context_setup f1-f4 (practice)

IMPORTANT: measures.fact_ids must use SHORT form (f1, f2, ...) not qualified form.
The validator does: q = f"{concept_id}#{f}" to build the qualified id.
"""
import json
from pathlib import Path

BATCH = Path("batches/final_batch_004_da_chunk2")
TILE = "tile_stakeholder_prioritizing_framing_context"

# Remediation step ids (first check/hands_on per concept)
REM_PRIORITIZING = f"{TILE}.r01"
REM_RECOMMENDATION = f"{TILE}.r02"
REM_NARRATIVE = f"{TILE}.r03"

interactions = [

    # ─────────────────────────────────────────────────────────────────────────
    # s03: check / choice
    # Tests: f1 (scoping stage establishes decision context),
    #        f2 (big idea = boil to one sentence, exclude non-essential),
    #        f3 (only include info relevant to audience)
    # Anchors: identify_decision_context_from_scoping_stage,
    #          distill_big_idea_and_exclude_irrelevant_findings
    # Difficulty: intro (first check in tile)
    # ─────────────────────────────────────────────────────────────────────────
    {
        "step_id": f"{TILE}.s03",
        "interaction": {
            "type": "choice",
            "interaction_id": f"ix.{TILE}.s03",
            "difficulty": "intro",
            "grading_mode": "client",
            "standalone": False,
            "measures": [
                {
                    "concept_id": "stakeholder.prioritizing_findings_by_relevance",
                    "capability": "identify_decision_context_from_scoping_stage",
                    "fact_ids": ["f1"]
                },
                {
                    "concept_id": "stakeholder.prioritizing_findings_by_relevance",
                    "capability": "distill_big_idea_and_exclude_irrelevant_findings",
                    "fact_ids": ["f2", "f3"]
                }
            ],
            "anchors": [
                "stakeholder.prioritizing_findings_by_relevance#assessment:identify_decision_context_from_scoping_stage",
                "stakeholder.prioritizing_findings_by_relevance#assessment:distill_big_idea_and_exclude_irrelevant_findings"
            ],
            "public": {
                "prompt": "The Head of Operations at QuickShip asked for an analysis to decide whether to add couriers in Lagos. Your analysis surfaces four findings: (1) Lagos average delivery time rose to 30 minutes, (2) Kano has the highest delivery-time variability, (3) one courier is unusually fast, (4) Abuja is on target. Which finding should open the report, and why?",
                "options": [
                    {
                        "option_id": "opt_lagos",
                        "text": "Lagos average delivery time rose to 30 minutes — it is directly relevant to the staffing decision established in scoping."
                    },
                    {
                        "option_id": "opt_kano",
                        "text": "Kano's delivery-time variability — it is the most analytically interesting finding in the dataset."
                    },
                    {
                        "option_id": "opt_courier",
                        "text": "The unusually fast courier — it is a positive finding and stakeholders prefer good news first."
                    },
                    {
                        "option_id": "opt_abuja",
                        "text": "Abuja is on target — it provides useful context before presenting the problem cities."
                    }
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_lagos"],
                "option_feedback": {
                    "opt_lagos": {
                        "message": "Correct. The scoping stage established the decision: whether to add Lagos couriers. The Lagos slowdown is the finding most directly relevant to that decision, so it leads."
                    },
                    "opt_kano": {
                        "message": "Analytical interestingness is not the right criterion. The scoping stage established the decision as whether to add Lagos couriers — Kano's variability does not inform that decision."
                    },
                    "opt_courier": {
                        "message": "Stakeholder preference for good news is not the right criterion. The scoping stage established the decision as whether to add Lagos couriers — the fast courier finding does not inform that decision."
                    },
                    "opt_abuja": {
                        "message": "Context about a city that is on target does not help the operations manager decide about Lagos staffing. Lead with the finding that directly informs the decision."
                    }
                }
            },
            "feedback": {
                "correct": {
                    "message": "Right. The engagement and scoping stage establishes how the analysis will inform decisions. That decision — whether to add Lagos couriers — points to which finding matters most: the Lagos slowdown."
                },
                "incorrect": {
                    "message": "Think about what the operations manager needs to decide. The scoping stage established the decision; the finding that most directly informs that decision should lead."
                },
                "hints": [
                    "What decision did the scoping stage establish for this analysis?",
                    "Which finding most directly tells the operations manager whether to add Lagos couriers?"
                ],
                "remediation_step_id": REM_PRIORITIZING
            }
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # s04: check / choice
    # Tests: f4 (inverted pyramid: most important first)
    # Anchor: rank_findings_using_inverted_pyramid
    # Difficulty: core
    # ─────────────────────────────────────────────────────────────────────────
    {
        "step_id": f"{TILE}.s04",
        "interaction": {
            "type": "choice",
            "interaction_id": f"ix.{TILE}.s04",
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": [
                {
                    "concept_id": "stakeholder.prioritizing_findings_by_relevance",
                    "capability": "rank_findings_using_inverted_pyramid",
                    "fact_ids": ["f4"]
                }
            ],
            "anchors": [
                "stakeholder.prioritizing_findings_by_relevance#assessment:rank_findings_using_inverted_pyramid"
            ],
            "public": {
                "prompt": "You have three findings to include in the QuickShip operations report: (A) Lagos average delivery time is 30 minutes — above the 25-minute target; (B) Kano also misses the target at 26.4 minutes; (C) Abuja is on target at 23.7 minutes. Using the inverted pyramid principle, which ordering is correct?",
                "options": [
                    {
                        "option_id": "opt_abc",
                        "text": "A first, then B, then C — most important to least important."
                    },
                    {
                        "option_id": "opt_cba",
                        "text": "C first, then B, then A — build up to the most important finding."
                    },
                    {
                        "option_id": "opt_bac",
                        "text": "B first, then A, then C — order by how far each city misses the target."
                    },
                    {
                        "option_id": "opt_acb",
                        "text": "A first, then C, then B — lead with the primary finding, then show the on-target city before the secondary miss."
                    }
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_abc"],
                "option_feedback": {
                    "opt_abc": {
                        "message": "Correct. The inverted pyramid puts the most important information first and arranges everything else from most to least important. Lagos (primary finding) leads, then Kano (secondary miss), then Abuja (on target)."
                    },
                    "opt_cba": {
                        "message": "Building up to the most important finding is a narrative technique, not the inverted pyramid. The inverted pyramid puts the most important information first so the reader gets the key message immediately."
                    },
                    "opt_bac": {
                        "message": "Ordering by degree of miss is not the inverted pyramid principle. The inverted pyramid ranks by importance to the decision — Lagos is primary because it directly informs the staffing decision."
                    },
                    "opt_acb": {
                        "message": "Inserting the on-target city between the two misses breaks the most-to-least-important order. The inverted pyramid keeps findings in descending order of importance."
                    }
                }
            },
            "feedback": {
                "correct": {
                    "message": "Correct. The inverted pyramid: most important first, then everything else from most to least important."
                },
                "incorrect": {
                    "message": "The inverted pyramid means the most important information comes first, with everything else arranged from most to least important after that."
                },
                "hints": [
                    "The inverted pyramid is about importance, not narrative build-up.",
                    "Which city's finding is most important to the Lagos staffing decision?"
                ],
                "remediation_step_id": REM_PRIORITIZING
            }
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # s05: hands_on / ordering (practice)
    # Tests: f1-f4 of prioritizing_findings_by_relevance
    # Anchors: practice, prioritize_findings_by_stakeholder_decision_relevance
    # Difficulty: stretch (hands-on = highest difficulty in tile section)
    # Practice success: learner selects the two findings most directly tied to
    #   the Lagos staffing decision, places them first, and justifies by
    #   referencing the stakeholder's decision rather than statistical novelty.
    # ─────────────────────────────────────────────────────────────────────────
    {
        "step_id": f"{TILE}.s05",
        "interaction": {
            "type": "ordering",
            "interaction_id": f"ix.{TILE}.s05",
            "difficulty": "stretch",
            "grading_mode": "client",
            "standalone": False,
            "measures": [
                {
                    "concept_id": "stakeholder.prioritizing_findings_by_relevance",
                    "capability": "prioritize_findings_by_stakeholder_decision_relevance",
                    "fact_ids": ["f1", "f2", "f3", "f4"]
                }
            ],
            "anchors": [
                "stakeholder.prioritizing_findings_by_relevance#practice",
                "stakeholder.prioritizing_findings_by_relevance#assessment:prioritize_findings_by_stakeholder_decision_relevance"
            ],
            "public": {
                "prompt": "The Head of Operations asked: should we add couriers in Lagos? Your analysis produced five findings. Drag them into the order they should appear in the stakeholder summary — most relevant to the decision first, least relevant last.",
                "items": [
                    {
                        "item_id": "item_lagos_avg",
                        "text": "Lagos average delivery time rose to 30 minutes — above the 25-minute target."
                    },
                    {
                        "item_id": "item_kano_miss",
                        "text": "Kano also misses the target at 26.4 minutes."
                    },
                    {
                        "item_id": "item_abuja_ok",
                        "text": "Abuja is on target at 23.7 minutes."
                    },
                    {
                        "item_id": "item_kano_var",
                        "text": "Kano has the highest delivery-time variability across all three cities."
                    },
                    {
                        "item_id": "item_fast_courier",
                        "text": "One Lagos courier completes deliveries 20% faster than the city average."
                    }
                ],
                "follow_up": {
                    "prompt": "Which principle best explains why you placed the first finding at the top?",
                    "options": [
                        {
                            "option_id": "fu_decision",
                            "text": "It is the finding most directly relevant to the staffing decision established in scoping."
                        },
                        {
                            "option_id": "fu_novelty",
                            "text": "It is the most analytically novel finding in the dataset."
                        },
                        {
                            "option_id": "fu_size",
                            "text": "It has the largest numerical deviation from the target."
                        }
                    ]
                }
            },
            "grading": {
                "correct_order": [
                    "item_lagos_avg",
                    "item_kano_miss",
                    "item_abuja_ok",
                    "item_kano_var",
                    "item_fast_courier"
                ],
                "accepted_alternatives": [
                    ["item_lagos_avg", "item_kano_miss", "item_kano_var", "item_abuja_ok", "item_fast_courier"],
                    ["item_lagos_avg", "item_kano_miss", "item_abuja_ok", "item_fast_courier", "item_kano_var"]
                ],
                "loop_back_note": "The Lagos finding must be first (directly informs the staffing decision). The fast-courier finding and Kano variability are analytically interesting but not relevant to the Lagos staffing decision, so they rank last.",
                "follow_up_correct_option_ids": ["fu_decision"]
            },
            "feedback": {
                "correct": {
                    "message": "Well done. You led with the Lagos finding — the one most directly relevant to the staffing decision — and placed analytically interesting but decision-irrelevant findings at the end."
                },
                "incorrect": {
                    "message": "The inverted pyramid puts the finding most relevant to the stakeholder's decision first. The scoping stage established the decision: whether to add Lagos couriers. Lead with the Lagos finding."
                },
                "hints": [
                    "What decision did the scoping stage establish? Which finding most directly informs that decision?",
                    "Analytical interestingness (variability, fast courier) is not the right criterion — relevance to the decision is."
                ],
                "remediation_step_id": REM_PRIORITIZING
            }
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # s07: check / choice
    # Tests: f2 (Big Idea example: clear what audience needs to know and do)
    # Anchor: write_actionable_recommendation_with_explicit_ask
    # Difficulty: intro (first check for this concept)
    # ─────────────────────────────────────────────────────────────────────────
    {
        "step_id": f"{TILE}.s07",
        "interaction": {
            "type": "choice",
            "interaction_id": f"ix.{TILE}.s07",
            "difficulty": "intro",
            "grading_mode": "client",
            "standalone": False,
            "measures": [
                {
                    "concept_id": "stakeholder.actionable_recommendation_framing",
                    "capability": "write_actionable_recommendation_with_explicit_ask",
                    "fact_ids": ["f2"]
                }
            ],
            "anchors": [
                "stakeholder.actionable_recommendation_framing#assessment:write_actionable_recommendation_with_explicit_ask"
            ],
            "public": {
                "prompt": "Which of the following is a properly framed recommendation — one that makes clear to the audience both what they need to know and what they are being asked to do?",
                "options": [
                    {
                        "option_id": "opt_proper",
                        "text": "We recommend adding one Lagos courier; please approve the added headcount."
                    },
                    {
                        "option_id": "opt_finding_only",
                        "text": "Lagos delivery times rose to 30 minutes — above the 25-minute target."
                    },
                    {
                        "option_id": "opt_vague",
                        "text": "Something should be done about Lagos delivery times."
                    },
                    {
                        "option_id": "opt_restate",
                        "text": "Lagos delivery times are significantly above target and this is a serious problem."
                    }
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_proper"],
                "option_feedback": {
                    "opt_proper": {
                        "message": "Correct. This statement names the action (add one Lagos courier) and includes an explicit ask (please approve the added headcount), making clear what the audience needs to know and what they are being asked to do."
                    },
                    "opt_finding_only": {
                        "message": "This is a finding — it describes what the data shows. A recommendation must go further and state what action should be taken and what the reader is being asked to approve."
                    },
                    "opt_vague": {
                        "message": "This statement is too vague to be actionable. A recommendation must name the specific action and include an explicit ask — the audience cannot be assumed to know what 'something' means."
                    },
                    "opt_restate": {
                        "message": "This restates the finding more emphatically but still does not tell the operations manager what to do. A recommendation must name the action and the explicit ask."
                    }
                }
            },
            "feedback": {
                "correct": {
                    "message": "Correct. A well-formed recommendation names the action and includes an explicit ask, so the audience knows exactly what decision is in front of them."
                },
                "incorrect": {
                    "message": "A recommendation must do two things: name the action to take, and include an explicit ask so the audience knows what they are being asked to approve or do."
                },
                "hints": [
                    "Does the statement name a specific action, or does it only describe the data?",
                    "Does the statement include an explicit ask — something the reader is being asked to approve or do?"
                ],
                "remediation_step_id": REM_RECOMMENDATION
            }
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # s08: hands_on / table_select (practice)
    # Tests: f1, f2 of actionable_recommendation_framing
    # Anchors: practice, distinguish_recommendation_from_finding,
    #          write_actionable_recommendation_with_explicit_ask
    # Difficulty: stretch
    # Uses ds_city_delivery_summary: learner selects the row (Lagos) whose
    # finding most needs to be paired with an actionable recommendation,
    # then selects the cell that shows the finding value that exceeds the
    # target — grounding the recommendation in the data.
    # Practice success: learner identifies the finding that needs a
    # recommendation (Lagos) and the specific value that makes the
    # recommendation necessary (avg_delivery_min = 30.1 > target 25).
    # ─────────────────────────────────────────────────────────────────────────
    {
        "step_id": f"{TILE}.s08",
        "interaction": {
            "type": "table_select",
            "interaction_id": f"ix.{TILE}.s08",
            "difficulty": "stretch",
            "grading_mode": "client",
            "standalone": False,
            "measures": [
                {
                    "concept_id": "stakeholder.actionable_recommendation_framing",
                    "capability": "distinguish_recommendation_from_finding",
                    "fact_ids": ["f1", "f2"]
                },
                {
                    "concept_id": "stakeholder.actionable_recommendation_framing",
                    "capability": "write_actionable_recommendation_with_explicit_ask",
                    "fact_ids": ["f2"]
                }
            ],
            "anchors": [
                "stakeholder.actionable_recommendation_framing#practice",
                "stakeholder.actionable_recommendation_framing#assessment:distinguish_recommendation_from_finding",
                "stakeholder.actionable_recommendation_framing#assessment:write_actionable_recommendation_with_explicit_ask"
            ],
            "public": {
                "asset_ref": {
                    "asset_id": "ds_city_delivery_summary",
                    "variant_id": None,
                    "columns": ["city", "avg_delivery_min", "target_min", "finding_priority"]
                },
                "intro": "The Head of Operations needs a recommendation, not just a finding. Use the delivery summary to identify which city's finding should be paired with an actionable recommendation.",
                "tasks": [
                    {
                        "task_id": "task_select_city",
                        "prompt": "Select the row for the city whose finding most directly requires an actionable recommendation to the Head of Operations about Lagos courier staffing.",
                        "target_kind": "row"
                    },
                    {
                        "task_id": "task_select_value",
                        "prompt": "Select the cell that shows the delivery-time value that makes the recommendation necessary — the value that exceeds the target.",
                        "target_kind": "cell"
                    }
                ]
            },
            "grading": {
                "answers": [
                    {
                        "task_id": "task_select_city",
                        "row": {
                            "where": {"city": "Lagos"}
                        }
                    },
                    {
                        "task_id": "task_select_value",
                        "row": {
                            "where": {"city": "Lagos"}
                        },
                        "column": "avg_delivery_min",
                        "expect_value": 30.1
                    }
                ],
                "task_feedback": {
                    "task_select_city": {
                        "correct": "Correct. Lagos is the city whose finding directly informs the staffing decision — it is the finding that needs to be paired with an actionable recommendation.",
                        "incorrect": "The Head of Operations asked about Lagos courier staffing. Which city's finding directly informs that decision?"
                    },
                    "task_select_value": {
                        "correct": "Correct. The average delivery time of 30.1 minutes exceeds the 25-minute target — this is the finding value that makes the recommendation necessary.",
                        "incorrect": "Look for the delivery-time value that exceeds the target. That is the finding that the recommendation must address."
                    }
                }
            },
            "feedback": {
                "correct": {
                    "message": "Correct. You identified the finding (Lagos avg 30.1 min > 25 min target) that needs to be paired with an actionable recommendation. The value of analytical efforts is only realized when insights are acted upon."
                },
                "incorrect": {
                    "message": "Identify the city whose finding directly informs the staffing decision, then find the delivery-time value that exceeds the target — that is the finding that needs a recommendation."
                },
                "hints": [
                    "The Head of Operations asked about Lagos courier staffing — which city's finding is most relevant?",
                    "A recommendation is needed when a finding shows a problem that requires action. Which value exceeds the target?"
                ],
                "remediation_step_id": REM_RECOMMENDATION
            }
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # s10: check / choice
    # Tests: f1 (story beginning = context), f2 (summary has beginning/middle/end),
    #        f3 (short paragraph, not lengthy background)
    # Anchors: identify_context_as_narrative_beginning,
    #          distinguish_short_opener_from_lengthy_background
    # Difficulty: intro (first check for this concept)
    # ─────────────────────────────────────────────────────────────────────────
    {
        "step_id": f"{TILE}.s10",
        "interaction": {
            "type": "choice",
            "interaction_id": f"ix.{TILE}.s10",
            "difficulty": "intro",
            "grading_mode": "client",
            "standalone": False,
            "measures": [
                {
                    "concept_id": "stakeholder.narrative_context_setup",
                    "capability": "identify_context_as_narrative_beginning",
                    "fact_ids": ["f1", "f2"]
                },
                {
                    "concept_id": "stakeholder.narrative_context_setup",
                    "capability": "distinguish_short_opener_from_lengthy_background",
                    "fact_ids": ["f3"]
                }
            ],
            "anchors": [
                "stakeholder.narrative_context_setup#assessment:identify_context_as_narrative_beginning",
                "stakeholder.narrative_context_setup#assessment:distinguish_short_opener_from_lengthy_background"
            ],
            "public": {
                "prompt": "Which of the following best describes the role of the opening section in a findings narrative?",
                "options": [
                    {
                        "option_id": "opt_context",
                        "text": "A short paragraph that establishes what the report covers and why the analysis was done, before presenting any finding."
                    },
                    {
                        "option_id": "opt_methodology",
                        "text": "A detailed explanation of the data sources, SQL queries, and methodology used in the analysis."
                    },
                    {
                        "option_id": "opt_summary",
                        "text": "A summary of all findings, presented upfront so the reader can skip the rest of the report."
                    },
                    {
                        "option_id": "opt_background",
                        "text": "A full background section covering company history, technical definitions, and operational context."
                    }
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_context"],
                "option_feedback": {
                    "opt_context": {
                        "message": "Correct. The opening section is the beginning of the narrative: a short paragraph that level-sets the reader on what the report covers and why the analysis was done, before any finding is presented."
                    },
                    "opt_methodology": {
                        "message": "Detailed methodology belongs in a separate section, not the opener. The opening should be a short paragraph explaining what the publication is about — not technical definitions or data-source details."
                    },
                    "opt_summary": {
                        "message": "A summary of all findings is the middle of the narrative, not the beginning. The beginning establishes context — what is happening and why — before the findings are presented."
                    },
                    "opt_background": {
                        "message": "A full background section is exactly what the opening should avoid. The opening should be short and purposeful — not lengthy background before the reader knows what the report is about."
                    }
                }
            },
            "feedback": {
                "correct": {
                    "message": "Correct. In a story's structure, the beginning establishes context. The opening section level-sets the reader before diving into the analysis."
                },
                "incorrect": {
                    "message": "The opening section is the beginning of the narrative — it establishes context (what the report covers and why) in a short paragraph, not methodology or lengthy background."
                },
                "hints": [
                    "Think about what a story's beginning does: it establishes context before the action begins.",
                    "The opening should be short and purposeful — what does the reader need to know before seeing any finding?"
                ],
                "remediation_step_id": REM_NARRATIVE
            }
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # s11: check / choice
    # Tests: f4 (explaining why statistics collected = policy/operational context)
    # Anchor: include_policy_and_operational_context_in_opening
    # Difficulty: core
    # ─────────────────────────────────────────────────────────────────────────
    {
        "step_id": f"{TILE}.s11",
        "interaction": {
            "type": "choice",
            "interaction_id": f"ix.{TILE}.s11",
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": [
                {
                    "concept_id": "stakeholder.narrative_context_setup",
                    "capability": "include_policy_and_operational_context_in_opening",
                    "fact_ids": ["f4"]
                }
            ],
            "anchors": [
                "stakeholder.narrative_context_setup#assessment:include_policy_and_operational_context_in_opening"
            ],
            "public": {
                "prompt": "You are writing the opening context section for the QuickShip delivery report. Which sentence best fulfils the requirement to explain why the statistics were collected?",
                "options": [
                    {
                        "option_id": "opt_operational",
                        "text": "This analysis was prompted by rising customer complaints about Lagos delivery times last quarter."
                    },
                    {
                        "option_id": "opt_technical",
                        "text": "Delivery times were measured using timestamps from the orders table, joined to the driver roster via courier_id."
                    },
                    {
                        "option_id": "opt_history",
                        "text": "QuickShip was founded in 2019 and has operated across Lagos, Kano, and Abuja since 2021."
                    },
                    {
                        "option_id": "opt_finding",
                        "text": "Lagos average delivery time rose to 30 minutes last month, above the 25-minute target."
                    }
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_operational"],
                "option_feedback": {
                    "opt_operational": {
                        "message": "Correct. Explaining why the statistics were collected means including relevant, factual information about the policy and operational context — here, the rising customer complaints that prompted the review."
                    },
                    "opt_technical": {
                        "message": "Technical measurement details belong in a methodology section, not the opening context. The opening should explain why the analysis was done, not how the data was extracted."
                    },
                    "opt_history": {
                        "message": "Company history is background information, not the reason the statistics were collected. The opening should explain the operational or policy reason that prompted this specific analysis."
                    },
                    "opt_finding": {
                        "message": "A finding belongs in the middle of the narrative, not the opening context section. The opening should explain why the analysis was done — before presenting any result."
                    }
                }
            },
            "feedback": {
                "correct": {
                    "message": "Correct. Explaining why the statistics were collected means including relevant, factual information about the policy and operational context — the reason the analysis exists at all."
                },
                "incorrect": {
                    "message": "The opening context section should explain why the statistics were collected — the policy or operational reason that prompted the analysis, not technical details, history, or findings."
                },
                "hints": [
                    "What prompted this analysis to be done at all? That is what the opening should explain.",
                    "The opening explains why the analysis was done — not how the data was collected or what the results were."
                ],
                "remediation_step_id": REM_NARRATIVE
            }
        }
    },

    # ─────────────────────────────────────────────────────────────────────────
    # s12: hands_on / external_proof (practice)
    # Tests: f1-f4 of narrative_context_setup
    # Anchors: practice, write_opening_context_section_for_findings_narrative
    # Difficulty: stretch
    # Practice success: two sentences that establish what the report is about
    #   and why it exists, use no technical definitions or lengthy background,
    #   and give the reader a factual reason the analysis was conducted —
    #   all without referencing any finding or result.
    # ─────────────────────────────────────────────────────────────────────────
    {
        "step_id": f"{TILE}.s12",
        "interaction": {
            "type": "external_proof",
            "interaction_id": f"ix.{TILE}.s12",
            "difficulty": "stretch",
            "grading_mode": "client",
            "standalone": False,
            "measures": [
                {
                    "concept_id": "stakeholder.narrative_context_setup",
                    "capability": "write_opening_context_section_for_findings_narrative",
                    "fact_ids": ["f1", "f2", "f3", "f4"]
                }
            ],
            "anchors": [
                "stakeholder.narrative_context_setup#practice",
                "stakeholder.narrative_context_setup#assessment:write_opening_context_section_for_findings_narrative"
            ],
            "public": {
                "instruction": "Write a two-sentence opening context section for the QuickShip delivery report. The first sentence should state what the report covers and why the analysis was done. The second sentence should name the specific question the analysis answers. Do not include any findings, results, or technical methodology.",
                "evidence_kinds": ["text"],
                "checklist": [
                    "Sentence 1 states what the report covers (delivery times, cities, time period).",
                    "Sentence 1 includes the operational or policy reason the analysis was done (e.g. rising customer complaints).",
                    "Sentence 2 names the specific question the analysis answers.",
                    "Neither sentence references a finding, result, or technical detail.",
                    "The two sentences together are short — no lengthy background."
                ]
            },
            "grading": {
                "mode": "self_attest",
                "rubric": [
                    {
                        "criterion": "Sentence 1 states what the report covers and includes the operational reason the analysis was done.",
                        "weight": 2
                    },
                    {
                        "criterion": "Sentence 2 names the specific question the analysis answers.",
                        "weight": 2
                    },
                    {
                        "criterion": "Neither sentence references a finding, result, or technical methodology.",
                        "weight": 1
                    }
                ]
            },
            "feedback": {
                "correct": {
                    "message": "Well done. Your two sentences establish what the report covers, why the analysis was done, and what question it answers — without any findings or technical background."
                },
                "incorrect": {
                    "message": "Check your two sentences: the first should state what the report covers and why the analysis was done; the second should name the specific question it answers. Neither should include findings or technical details."
                },
                "hints": [
                    "Sentence 1: 'This report examines [what] across [where] [when], prompted by [why].'",
                    "Sentence 2: 'It answers: [specific question]?' — name the question, not the answer."
                ],
                "remediation_step_id": REM_NARRATIVE
            }
        }
    }
]

output = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_004_da_chunk2",
    "tiles": [
        {
            "tile_id": TILE,
            "interactions": interactions
        }
    ]
}

out_path = BATCH / "interactions.part.c0_canary.json"
out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
print(f"Written {out_path}")
print(f"Interactions: {len(interactions)}")
for ix in interactions:
    print(f"  {ix['step_id']} -> {ix['interaction']['type']}")
