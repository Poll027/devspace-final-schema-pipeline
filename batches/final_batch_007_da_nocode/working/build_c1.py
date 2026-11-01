#!/usr/bin/env python3
"""Build screens.part.c1.json for tile_stakeholder_framing_requirements."""
import json, re

# ── helpers ──────────────────────────────────────────────────────────────────
def wc(text):
    return len(re.findall(r'\S+', text))

# ── tile plan steps (from tile_plans.json) ───────────────────────────────────
# We only need tile_stakeholder_framing_requirements

# ── build the tile ───────────────────────────────────────────────────────────
tile_id = "tile_stakeholder_framing_requirements"
next_tile_id = "tile_stakeholder_recommendation_translation"

steps = []

# ─────────────────────────────────────────────────────────────────────────────
# s01 – explainer – stakeholder.identifying_decision_need
# tb1, tb2, tb3 | f1, f2 | budget 136 | no visual
# ─────────────────────────────────────────────────────────────────────────────
s01_b1_text = (
    "An operations manager emails you: \"Can you look into our delivery times?\" "
    "Before opening a notebook, the first question worth asking is not what to measure "
    "— it is what decision this analysis is actually meant to inform."
)
s01_b2_text = (
    "Analysis is the collection, manipulation and interpretation of information and data "
    "for use in decision-making. A request for analysis often exists because someone needs "
    "to decide something, even when the request itself does not say so directly."
)
s01_b3_text = (
    "The engagement and scoping stage of an analytical project should establish an "
    "understanding of how the analysis will inform decisions. For the delivery-times request, "
    "that means asking the manager directly: is this about deciding whether to hire more "
    "couriers for the Lagos route, or whether to renegotiate with a courier partner? "
    "The answer changes what you would actually need to measure."
)

print(f"s01 b1 words: {wc(s01_b1_text)}")
print(f"s01 b2 words: {wc(s01_b2_text)}")
print(f"s01 b3 words: {wc(s01_b3_text)}")
print(f"s01 total: {wc(s01_b1_text)+wc(s01_b2_text)+wc(s01_b3_text)}")

steps.append({
    "step_id": f"{tile_id}.s01",
    "type": "explainer",
    "concept_ids": ["stakeholder.identifying_decision_need"],
    "eyebrow": "Decision Need",
    "title": "What decision is this analysis for?",
    "lede": "Every analysis request hides a decision. Finding it first saves you from measuring the wrong thing.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.s01.b1",
            "role": "intro",
            "text": s01_b1_text,
            "lineage": {
                "concept_ids": ["stakeholder.identifying_decision_need"],
                "fact_ids": [],
                "teaching_block_ids": ["stakeholder.identifying_decision_need#tb1"]
            }
        },
        {
            "type": "prose",
            "block_id": f"{tile_id}.s01.b2",
            "role": "definition",
            "text": s01_b2_text,
            "lineage": {
                "concept_ids": ["stakeholder.identifying_decision_need"],
                "fact_ids": ["stakeholder.identifying_decision_need#f1"],
                "teaching_block_ids": ["stakeholder.identifying_decision_need#tb2"]
            }
        },
        {
            "type": "prose",
            "block_id": f"{tile_id}.s01.b3",
            "role": "mechanism",
            "text": s01_b3_text,
            "lineage": {
                "concept_ids": ["stakeholder.identifying_decision_need"],
                "fact_ids": ["stakeholder.identifying_decision_need#f2"],
                "teaching_block_ids": ["stakeholder.identifying_decision_need#tb3"]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": ["stakeholder.identifying_decision_need"],
        "fact_ids": [
            "stakeholder.identifying_decision_need#f1",
            "stakeholder.identifying_decision_need#f2"
        ],
        "teaching_block_ids": [
            "stakeholder.identifying_decision_need#tb1",
            "stakeholder.identifying_decision_need#tb2",
            "stakeholder.identifying_decision_need#tb3"
        ]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s02 – check – stakeholder.identifying_decision_need
# f1, f2 | anchors: identify_decision_behind_stakeholder_request | framing only
# ─────────────────────────────────────────────────────────────────────────────
steps.append({
    "step_id": f"{tile_id}.s02",
    "type": "check",
    "concept_ids": ["stakeholder.identifying_decision_need"],
    "eyebrow": "Quick Check",
    "title": "Spot the decision behind the request",
    "lede": "Apply what you've learned about identifying the decision a stakeholder needs.",
    "reward": {"gems": 5, "first_try_bonus": 2},
    "lineage": {
        "concept_ids": ["stakeholder.identifying_decision_need"],
        "fact_ids": [
            "stakeholder.identifying_decision_need#f1",
            "stakeholder.identifying_decision_need#f2"
        ],
        "teaching_block_ids": [],
        "anchors": [
            "stakeholder.identifying_decision_need#assessment:identify_decision_behind_stakeholder_request"
        ]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s03 – hands_on – stakeholder.identifying_decision_need
# f1, f2 | anchors: practice + identify_decision_behind_stakeholder_request | framing only
# ─────────────────────────────────────────────────────────────────────────────
steps.append({
    "step_id": f"{tile_id}.s03",
    "type": "hands_on",
    "concept_ids": ["stakeholder.identifying_decision_need"],
    "eyebrow": "Hands On",
    "title": "Name the decision",
    "lede": "Given a vague stakeholder request, identify the specific decision it is meant to inform.",
    "reward": {"gems": 10, "first_try_bonus": 3},
    "lineage": {
        "concept_ids": ["stakeholder.identifying_decision_need"],
        "fact_ids": [
            "stakeholder.identifying_decision_need#f1",
            "stakeholder.identifying_decision_need#f2"
        ],
        "teaching_block_ids": [],
        "anchors": [
            "stakeholder.identifying_decision_need#practice",
            "stakeholder.identifying_decision_need#assessment:identify_decision_behind_stakeholder_request"
        ]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s04 – explainer – stakeholder.precise_finding_statement
# tb1, tb2 | f2 | visual: before_after | budget 103
# ─────────────────────────────────────────────────────────────────────────────
s04_b1_text = (
    "Once you have analyzed the delivery data, \"delivery times went up\" is a finding of sorts "
    "— but it does not say by how much, where, or compared to what. A communication's big idea "
    "must articulate a unique point of view, convey what is at stake, and be a complete sentence, "
    "not a fragment or a topic label."
)
print(f"\ns04 b1 words: {wc(s04_b1_text)}")

steps.append({
    "step_id": f"{tile_id}.s04",
    "type": "explainer",
    "concept_ids": ["stakeholder.precise_finding_statement"],
    "eyebrow": "Precise Findings",
    "title": "From vague label to complete finding",
    "lede": "A finding that names a number and a comparison is far more useful than one that only names a topic.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.s04.b1",
            "role": "intro",
            "text": s04_b1_text,
            "lineage": {
                "concept_ids": ["stakeholder.precise_finding_statement"],
                "fact_ids": ["stakeholder.precise_finding_statement#f2"],
                "teaching_block_ids": [
                    "stakeholder.precise_finding_statement#tb1",
                    "stakeholder.precise_finding_statement#tb2"
                ]
            }
        },
        {
            "type": "before_after",
            "block_id": f"{tile_id}.s04.b2",
            "before": {
                "type": "diagram",
                "block_id": f"{tile_id}.s04.b2.before",
                "diagram_kind": "container",
                "title": "Vague finding",
                "nodes": [
                    {
                        "id": "vague_label",
                        "label": "Lagos delivery times",
                        "kind": "topic",
                        "detail": "Topic label only — no position, no number, no comparison"
                    }
                ],
                "alt_text": "A box labelled 'Lagos delivery times' — a topic label with no claim, no number and no comparison."
            },
            "after": {
                "type": "diagram",
                "block_id": f"{tile_id}.s04.b2.after",
                "diagram_kind": "container",
                "title": "Precise finding",
                "nodes": [
                    {
                        "id": "precise_sentence",
                        "label": "Lagos delivery times have risen, so customers on that route are waiting longer for their orders.",
                        "kind": "finding",
                        "detail": "Complete sentence: takes a position (Lagos has slowed down) and states what is at stake (customers waiting longer)"
                    }
                ],
                "alt_text": "A box containing the sentence: 'Lagos delivery times have risen, so customers on that route are waiting longer for their orders.' Annotated as a complete sentence with a unique point of view and a statement of what is at stake."
            },
            "change_summary": "Adding a position and a statement of what is at stake turns a topic label into a complete finding sentence.",
            "lineage": {
                "concept_ids": ["stakeholder.precise_finding_statement"],
                "fact_ids": ["stakeholder.precise_finding_statement#f2"],
                "teaching_block_ids": ["stakeholder.precise_finding_statement#tb2"],
                "anchors": ["stakeholder.precise_finding_statement#visual"]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": ["stakeholder.precise_finding_statement"],
        "fact_ids": ["stakeholder.precise_finding_statement#f2"],
        "teaching_block_ids": [
            "stakeholder.precise_finding_statement#tb1",
            "stakeholder.precise_finding_statement#tb2"
        ],
        "anchors": ["stakeholder.precise_finding_statement#visual"]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s05 – explainer – stakeholder.precise_finding_statement
# tb3, tb4 | f3, f4, f5 | no visual | budget 166
# ─────────────────────────────────────────────────────────────────────────────
s05_b1_text = (
    "A claim about the data should be checked against what the data actually shows, and narrowed "
    "if needed. One example revises the broader claim \"Price has declined for all products\" to "
    "the more precise \"the average retail price of existing products declined\" once the underlying "
    "data was examined more closely. The same check applies to the delivery claim: if only Lagos "
    "routes actually slowed down, the finding should narrow to Lagos, not describe every city."
)
s05_b2_text = (
    "Writing about data should be specific about the point being made, and putting data into "
    "context includes making comparisons. Following that pattern, a precise delivery finding "
    "names the number and the comparison: \"the average Lagos delivery time rose to 30 minutes "
    "this month, up from 22 minutes last month\" — rather than just \"delivery times went up.\""
)
print(f"s05 b1 words: {wc(s05_b1_text)}")
print(f"s05 b2 words: {wc(s05_b2_text)}")
print(f"s05 total: {wc(s05_b1_text)+wc(s05_b2_text)}")

steps.append({
    "step_id": f"{tile_id}.s05",
    "type": "explainer",
    "concept_ids": ["stakeholder.precise_finding_statement"],
    "eyebrow": "Precise Findings",
    "title": "Narrow the claim and add the number",
    "lede": "Check your claim against the data, narrow it if needed, then add the specific number and comparison.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.s05.b1",
            "role": "mechanism",
            "text": s05_b1_text,
            "lineage": {
                "concept_ids": ["stakeholder.precise_finding_statement"],
                "fact_ids": ["stakeholder.precise_finding_statement#f3"],
                "teaching_block_ids": ["stakeholder.precise_finding_statement#tb3"]
            }
        },
        {
            "type": "prose",
            "block_id": f"{tile_id}.s05.b2",
            "role": "example",
            "text": s05_b2_text,
            "lineage": {
                "concept_ids": ["stakeholder.precise_finding_statement"],
                "fact_ids": [
                    "stakeholder.precise_finding_statement#f4",
                    "stakeholder.precise_finding_statement#f5"
                ],
                "teaching_block_ids": ["stakeholder.precise_finding_statement#tb4"]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": ["stakeholder.precise_finding_statement"],
        "fact_ids": [
            "stakeholder.precise_finding_statement#f3",
            "stakeholder.precise_finding_statement#f4",
            "stakeholder.precise_finding_statement#f5"
        ],
        "teaching_block_ids": [
            "stakeholder.precise_finding_statement#tb3",
            "stakeholder.precise_finding_statement#tb4"
        ]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s06 – check – stakeholder.precise_finding_statement
# f3 | anchors: narrow_claim_to_match_data | framing only
# ─────────────────────────────────────────────────────────────────────────────
steps.append({
    "step_id": f"{tile_id}.s06",
    "type": "check",
    "concept_ids": ["stakeholder.precise_finding_statement"],
    "eyebrow": "Quick Check",
    "title": "Narrow the claim to match the data",
    "lede": "Apply what you've learned about checking a claim against what the data actually shows.",
    "reward": {"gems": 5, "first_try_bonus": 2},
    "lineage": {
        "concept_ids": ["stakeholder.precise_finding_statement"],
        "fact_ids": ["stakeholder.precise_finding_statement#f3"],
        "teaching_block_ids": [],
        "anchors": [
            "stakeholder.precise_finding_statement#assessment:narrow_claim_to_match_data"
        ]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s07 – hands_on – stakeholder.precise_finding_statement
# f2, f4, f5 | anchors: practice + identify_complete_sentence_big_idea + state_finding_with_specific_number_and_comparison
# ─────────────────────────────────────────────────────────────────────────────
steps.append({
    "step_id": f"{tile_id}.s07",
    "type": "hands_on",
    "concept_ids": ["stakeholder.precise_finding_statement"],
    "eyebrow": "Hands On",
    "title": "Write a precise finding",
    "lede": "Turn a vague delivery finding into a complete sentence with a specific number and comparison.",
    "reward": {"gems": 10, "first_try_bonus": 3},
    "lineage": {
        "concept_ids": ["stakeholder.precise_finding_statement"],
        "fact_ids": [
            "stakeholder.precise_finding_statement#f2",
            "stakeholder.precise_finding_statement#f4",
            "stakeholder.precise_finding_statement#f5"
        ],
        "teaching_block_ids": [],
        "anchors": [
            "stakeholder.precise_finding_statement#practice",
            "stakeholder.precise_finding_statement#assessment:identify_complete_sentence_big_idea",
            "stakeholder.precise_finding_statement#assessment:state_finding_with_specific_number_and_comparison"
        ]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s08 – explainer – stakeholder.framing_analytical_question
# tb1, tb2, tb3 | f1, f3 | visual: before_after | budget 164
# ─────────────────────────────────────────────────────────────────────────────
s08_b1_text = (
    "\"Are deliveries going well?\" is the kind of question a stakeholder might actually ask "
    "— and it cannot be answered with data as written. In the engagement and scoping stage, "
    "the analyst should engage with the commissioner to identify the question, the context, "
    "and the boundaries of the analysis, as well as constraints such as deadlines and available "
    "resources. That kind of conversation can turn \"are deliveries going well\" into something "
    "answerable: which cities, which time period, compared against what."
)
print(f"\ns08 b1 words: {wc(s08_b1_text)}")

steps.append({
    "step_id": f"{tile_id}.s08",
    "type": "explainer",
    "concept_ids": ["stakeholder.framing_analytical_question"],
    "eyebrow": "Analytical Question",
    "title": "From vague question to measurable question",
    "lede": "A vague business question cannot be answered with data. A scoping conversation turns it into one that can.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.s08.b1",
            "role": "intro",
            "text": s08_b1_text,
            "lineage": {
                "concept_ids": ["stakeholder.framing_analytical_question"],
                "fact_ids": ["stakeholder.framing_analytical_question#f1"],
                "teaching_block_ids": [
                    "stakeholder.framing_analytical_question#tb1",
                    "stakeholder.framing_analytical_question#tb2"
                ]
            }
        },
        {
            "type": "before_after",
            "block_id": f"{tile_id}.s08.b2",
            "before": {
                "type": "diagram",
                "block_id": f"{tile_id}.s08.b2.before",
                "diagram_kind": "container",
                "title": "Vague business question",
                "nodes": [
                    {
                        "id": "vague_q",
                        "label": "Are we doing well?",
                        "detail": "No variable of interest, no group, no intent — cannot be answered with data"
                    }
                ],
                "alt_text": "A box containing the question 'Are we doing well?' with a note that it names no variable, no group, and no intent."
            },
            "after": {
                "type": "diagram",
                "block_id": f"{tile_id}.s08.b2.after",
                "diagram_kind": "container",
                "title": "Well-formed statistical question",
                "nodes": [
                    {
                        "id": "variable",
                        "label": "Variable of interest: average delivery time",
                        "kind": "component"
                    },
                    {
                        "id": "group",
                        "label": "Group: Lagos, this month vs. last month",
                        "kind": "component"
                    },
                    {
                        "id": "intent",
                        "label": "Intent: comparison",
                        "kind": "component"
                    },
                    {
                        "id": "question",
                        "label": "Is average delivery time in Lagos this month higher than last month?",
                        "kind": "result"
                    }
                ],
                "edges": [
                    {"from": "variable", "to": "question"},
                    {"from": "group", "to": "question"},
                    {"from": "intent", "to": "question"}
                ],
                "alt_text": "Three labelled components — variable of interest (average delivery time), group (Lagos, this month vs. last month), and intent (comparison) — combine to form the question: 'Is average delivery time in Lagos this month higher than last month?'"
            },
            "change_summary": "Naming the variable of interest, the group, and the intent turns an unanswerable question into a well-formed statistical question.",
            "lineage": {
                "concept_ids": ["stakeholder.framing_analytical_question"],
                "fact_ids": ["stakeholder.framing_analytical_question#f3"],
                "teaching_block_ids": ["stakeholder.framing_analytical_question#tb3"],
                "anchors": ["stakeholder.framing_analytical_question#visual"]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": ["stakeholder.framing_analytical_question"],
        "fact_ids": [
            "stakeholder.framing_analytical_question#f1",
            "stakeholder.framing_analytical_question#f3"
        ],
        "teaching_block_ids": [
            "stakeholder.framing_analytical_question#tb1",
            "stakeholder.framing_analytical_question#tb2",
            "stakeholder.framing_analytical_question#tb3"
        ],
        "anchors": ["stakeholder.framing_analytical_question#visual"]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s09 – explainer – stakeholder.framing_analytical_question
# tb4 | f2 | no visual | budget 44
# ─────────────────────────────────────────────────────────────────────────────
s09_b1_text = (
    "The engagement and scoping stage should lead to agreement between the analyst and "
    "commissioner about the outputs of the work, including acceptable levels of accuracy, "
    "precision and margins of error, so both sides know in advance what kind of answer will "
    "count as sufficient."
)
print(f"\ns09 b1 words: {wc(s09_b1_text)}")

steps.append({
    "step_id": f"{tile_id}.s09",
    "type": "explainer",
    "concept_ids": ["stakeholder.framing_analytical_question"],
    "eyebrow": "Analytical Question",
    "title": "Agreeing on what a good answer looks like",
    "lede": "Scoping ends with both sides agreeing on the outputs — not just the question.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.s09.b1",
            "role": "practical_context",
            "text": s09_b1_text,
            "lineage": {
                "concept_ids": ["stakeholder.framing_analytical_question"],
                "fact_ids": ["stakeholder.framing_analytical_question#f2"],
                "teaching_block_ids": ["stakeholder.framing_analytical_question#tb4"]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": ["stakeholder.framing_analytical_question"],
        "fact_ids": ["stakeholder.framing_analytical_question#f2"],
        "teaching_block_ids": ["stakeholder.framing_analytical_question#tb4"]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s10 – check – stakeholder.framing_analytical_question
# f3 | anchors: identify_components_of_a_well_formed_statistical_question | framing only
# ─────────────────────────────────────────────────────────────────────────────
steps.append({
    "step_id": f"{tile_id}.s10",
    "type": "check",
    "concept_ids": ["stakeholder.framing_analytical_question"],
    "eyebrow": "Quick Check",
    "title": "Components of a well-formed statistical question",
    "lede": "Apply what you've learned about what makes a statistical question well-formed.",
    "reward": {"gems": 5, "first_try_bonus": 2},
    "lineage": {
        "concept_ids": ["stakeholder.framing_analytical_question"],
        "fact_ids": ["stakeholder.framing_analytical_question#f3"],
        "teaching_block_ids": [],
        "anchors": [
            "stakeholder.framing_analytical_question#assessment:identify_components_of_a_well_formed_statistical_question"
        ]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s11 – check – stakeholder.framing_analytical_question
# f2 | anchors: describe_scoping_stage_agreement_on_outputs | framing only
# ─────────────────────────────────────────────────────────────────────────────
steps.append({
    "step_id": f"{tile_id}.s11",
    "type": "check",
    "concept_ids": ["stakeholder.framing_analytical_question"],
    "eyebrow": "Quick Check",
    "title": "Scoping stage agreement on outputs",
    "lede": "Apply what you've learned about what the scoping stage should produce.",
    "reward": {"gems": 5, "first_try_bonus": 2},
    "lineage": {
        "concept_ids": ["stakeholder.framing_analytical_question"],
        "fact_ids": ["stakeholder.framing_analytical_question#f2"],
        "teaching_block_ids": [],
        "anchors": [
            "stakeholder.framing_analytical_question#assessment:describe_scoping_stage_agreement_on_outputs"
        ]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s12 – hands_on – stakeholder.framing_analytical_question
# f1, f2, f3 | anchors: practice + restate_vague_question + identify_scoping_conversation_elements
# ─────────────────────────────────────────────────────────────────────────────
steps.append({
    "step_id": f"{tile_id}.s12",
    "type": "hands_on",
    "concept_ids": ["stakeholder.framing_analytical_question"],
    "eyebrow": "Hands On",
    "title": "Rewrite the vague question",
    "lede": "Classify each element of a scoping conversation and restate the vague question as a measurable analytical question.",
    "reward": {"gems": 10, "first_try_bonus": 3},
    "lineage": {
        "concept_ids": ["stakeholder.framing_analytical_question"],
        "fact_ids": [
            "stakeholder.framing_analytical_question#f1",
            "stakeholder.framing_analytical_question#f2",
            "stakeholder.framing_analytical_question#f3"
        ],
        "teaching_block_ids": [],
        "anchors": [
            "stakeholder.framing_analytical_question#practice",
            "stakeholder.framing_analytical_question#assessment:restate_vague_question_as_measurable_analytical_question",
            "stakeholder.framing_analytical_question#assessment:identify_scoping_conversation_elements"
        ]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s13 – explainer – stakeholder.identifying_requirements
# tb1, tb2, tb3 | f1, f3, f4 | visual: process_flow | budget 130
# ─────────────────────────────────────────────────────────────────────────────
s13_b1_text = (
    "Agreeing on the decision and the question still leaves open what you actually need from "
    "the operations manager before you can start: what data, by when, in what form. In the "
    "engagement and scoping stage, the commissioner should inform the analyst about the important "
    "aspects of the problem, its scope, and any constraints or issues, and should communicate "
    "any relevant information about data sources and data quality."
)
s13_b2_text = (
    "Constraints around resources and timelines should be clarified and agreed between the "
    "analyst and commissioner during engagement and scoping — for instance, whether the manager "
    "needs an answer this week or can wait for a fuller analysis next month."
)
print(f"\ns13 b1 words: {wc(s13_b1_text)}")
print(f"s13 b2 words: {wc(s13_b2_text)}")
print(f"s13 total: {wc(s13_b1_text)+wc(s13_b2_text)}")

steps.append({
    "step_id": f"{tile_id}.s13",
    "type": "explainer",
    "concept_ids": ["stakeholder.identifying_requirements"],
    "eyebrow": "Requirements",
    "title": "What the commissioner must tell you",
    "lede": "Before analysis begins, the commissioner and analyst must exchange information about scope, data, and constraints.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.s13.b1",
            "role": "mechanism",
            "text": s13_b1_text,
            "lineage": {
                "concept_ids": ["stakeholder.identifying_requirements"],
                "fact_ids": [
                    "stakeholder.identifying_requirements#f1",
                    "stakeholder.identifying_requirements#f3"
                ],
                "teaching_block_ids": [
                    "stakeholder.identifying_requirements#tb1",
                    "stakeholder.identifying_requirements#tb2"
                ]
            }
        },
        {
            "type": "prose",
            "block_id": f"{tile_id}.s13.b2",
            "role": "mechanism",
            "text": s13_b2_text,
            "lineage": {
                "concept_ids": ["stakeholder.identifying_requirements"],
                "fact_ids": ["stakeholder.identifying_requirements#f4"],
                "teaching_block_ids": ["stakeholder.identifying_requirements#tb3"]
            }
        },
        {
            "type": "process_flow",
            "block_id": f"{tile_id}.s13.b3",
            "title": "Engagement and scoping: the two-way exchange",
            "direction": "LR",
            "nodes": [
                {
                    "id": "commissioner_input",
                    "label": "Commissioner provides: problem context, scope, constraints, data-quality information",
                    "kind": "io"
                },
                {
                    "id": "analyst_draft",
                    "label": "Analyst drafts specification document",
                    "kind": "step"
                },
                {
                    "id": "commissioner_signoff",
                    "label": "Commissioner signs off",
                    "kind": "decision"
                },
                {
                    "id": "agreed_outputs",
                    "label": "Both parties agree on outputs before analysis begins",
                    "kind": "end"
                }
            ],
            "edges": [
                {"from": "commissioner_input", "to": "analyst_draft", "kind": "next"},
                {"from": "analyst_draft", "to": "commissioner_signoff", "kind": "next"},
                {"from": "commissioner_signoff", "to": "agreed_outputs", "kind": "yes"},
                {"from": "commissioner_signoff", "to": "analyst_draft", "kind": "no", "label": "Revise"}
            ],
            "reveal": "all",
            "alt_text": "A flow diagram showing the engagement-and-scoping exchange: the commissioner provides problem context, scope, constraints, and data-quality information; the analyst drafts a specification document; the commissioner signs off (or asks for revisions); both parties agree on outputs before analysis begins.",
            "lineage": {
                "concept_ids": ["stakeholder.identifying_requirements"],
                "fact_ids": [
                    "stakeholder.identifying_requirements#f1",
                    "stakeholder.identifying_requirements#f3",
                    "stakeholder.identifying_requirements#f4"
                ],
                "teaching_block_ids": [
                    "stakeholder.identifying_requirements#tb2",
                    "stakeholder.identifying_requirements#tb3"
                ],
                "anchors": ["stakeholder.identifying_requirements#visual"]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": ["stakeholder.identifying_requirements"],
        "fact_ids": [
            "stakeholder.identifying_requirements#f1",
            "stakeholder.identifying_requirements#f3",
            "stakeholder.identifying_requirements#f4"
        ],
        "teaching_block_ids": [
            "stakeholder.identifying_requirements#tb1",
            "stakeholder.identifying_requirements#tb2",
            "stakeholder.identifying_requirements#tb3"
        ],
        "anchors": ["stakeholder.identifying_requirements#visual"]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s14 – explainer – stakeholder.identifying_requirements
# tb4 | f2, f5 | no visual | budget 96
# ─────────────────────────────────────────────────────────────────────────────
s14_b1_text = (
    "The analyst should create a specification document that captures the commissioner's "
    "requirements, providing a definition of the scope and project constraints; the analyst "
    "should share this specification with the commissioner for sign-off. For the delivery "
    "request, that means a short written specification of the routes, time period, data source, "
    "and deadline, which the manager signs off. The engagement and scoping stage should lead to "
    "agreement about the outputs of the work — for instance, agreeing the deliverable is a "
    "one-page summary with a bar chart of average delivery time per city."
)
print(f"\ns14 b1 words: {wc(s14_b1_text)}")

steps.append({
    "step_id": f"{tile_id}.s14",
    "type": "explainer",
    "concept_ids": ["stakeholder.identifying_requirements"],
    "eyebrow": "Requirements",
    "title": "The specification document and output agreement",
    "lede": "The analyst captures requirements in a specification document and gets the commissioner's sign-off before starting.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.s14.b1",
            "role": "workflow",
            "text": s14_b1_text,
            "lineage": {
                "concept_ids": ["stakeholder.identifying_requirements"],
                "fact_ids": [
                    "stakeholder.identifying_requirements#f2",
                    "stakeholder.identifying_requirements#f5"
                ],
                "teaching_block_ids": ["stakeholder.identifying_requirements#tb4"]
            }
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": ["stakeholder.identifying_requirements"],
        "fact_ids": [
            "stakeholder.identifying_requirements#f2",
            "stakeholder.identifying_requirements#f5"
        ],
        "teaching_block_ids": ["stakeholder.identifying_requirements#tb4"]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s15 – check – stakeholder.identifying_requirements
# f1, f2, f3 | anchors: identify_commissioner_inputs_at_scoping + describe_specification_document_and_sign_off
# ─────────────────────────────────────────────────────────────────────────────
steps.append({
    "step_id": f"{tile_id}.s15",
    "type": "check",
    "concept_ids": ["stakeholder.identifying_requirements"],
    "eyebrow": "Quick Check",
    "title": "Commissioner inputs and the specification document",
    "lede": "Apply what you've learned about what the commissioner provides and what the analyst captures.",
    "reward": {"gems": 5, "first_try_bonus": 2},
    "lineage": {
        "concept_ids": ["stakeholder.identifying_requirements"],
        "fact_ids": [
            "stakeholder.identifying_requirements#f1",
            "stakeholder.identifying_requirements#f2",
            "stakeholder.identifying_requirements#f3"
        ],
        "teaching_block_ids": [],
        "anchors": [
            "stakeholder.identifying_requirements#assessment:identify_commissioner_inputs_at_scoping",
            "stakeholder.identifying_requirements#assessment:describe_specification_document_and_sign_off"
        ]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s16 – check – stakeholder.identifying_requirements
# f4, f5 | anchors: identify_resource_and_timeline_constraints + recognise_output_agreement_as_scoping_outcome
# ─────────────────────────────────────────────────────────────────────────────
steps.append({
    "step_id": f"{tile_id}.s16",
    "type": "check",
    "concept_ids": ["stakeholder.identifying_requirements"],
    "eyebrow": "Quick Check",
    "title": "Resource constraints and output agreement",
    "lede": "Apply what you've learned about constraints and the output agreement that closes the scoping stage.",
    "reward": {"gems": 5, "first_try_bonus": 2},
    "lineage": {
        "concept_ids": ["stakeholder.identifying_requirements"],
        "fact_ids": [
            "stakeholder.identifying_requirements#f4",
            "stakeholder.identifying_requirements#f5"
        ],
        "teaching_block_ids": [],
        "anchors": [
            "stakeholder.identifying_requirements#assessment:identify_resource_and_timeline_constraints",
            "stakeholder.identifying_requirements#assessment:recognise_output_agreement_as_scoping_outcome"
        ]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s17 – hands_on – stakeholder.identifying_requirements
# f1, f2, f3, f4, f5 | anchors: practice + extract_data_scope_and_output_requirements
# ─────────────────────────────────────────────────────────────────────────────
steps.append({
    "step_id": f"{tile_id}.s17",
    "type": "hands_on",
    "concept_ids": ["stakeholder.identifying_requirements"],
    "eyebrow": "Hands On",
    "title": "Extract scope and output requirements",
    "lede": "Given a stakeholder request, identify the data scope, constraints, and output requirements.",
    "reward": {"gems": 10, "first_try_bonus": 3},
    "lineage": {
        "concept_ids": ["stakeholder.identifying_requirements"],
        "fact_ids": [
            "stakeholder.identifying_requirements#f1",
            "stakeholder.identifying_requirements#f2",
            "stakeholder.identifying_requirements#f3",
            "stakeholder.identifying_requirements#f4",
            "stakeholder.identifying_requirements#f5"
        ],
        "teaching_block_ids": [],
        "anchors": [
            "stakeholder.identifying_requirements#practice",
            "stakeholder.identifying_requirements#assessment:extract_data_scope_and_output_requirements_from_stakeholder_request"
        ]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# s18 – recap
# tb4 from identifying_decision_need | f1, f2 from identifying_decision_need | budget 90
# up_next: tile_stakeholder_recommendation_translation
# ─────────────────────────────────────────────────────────────────────────────
s18_b1_text = (
    "Every analysis request hides a decision — naming it up front gives the work a target. "
    "A precise finding names a number and a comparison, not just a topic. A well-formed "
    "statistical question names the variable, the group, and the intent. Before analysis "
    "begins, the commissioner and analyst agree on scope, constraints, data sources, and "
    "the expected output, captured in a specification document signed off by both sides."
)
print(f"\ns18 b1 words: {wc(s18_b1_text)}")

steps.append({
    "step_id": f"{tile_id}.s18",
    "type": "recap",
    "concept_ids": [
        "stakeholder.identifying_decision_need",
        "stakeholder.precise_finding_statement",
        "stakeholder.framing_analytical_question",
        "stakeholder.identifying_requirements"
    ],
    "eyebrow": "Recap",
    "title": "What you've learned",
    "lede": "Four habits that shape every stakeholder conversation before analysis begins.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.s18.b1",
            "role": "takeaway",
            "text": s18_b1_text,
            "lineage": {
                "concept_ids": [
                    "stakeholder.identifying_decision_need",
                    "stakeholder.precise_finding_statement",
                    "stakeholder.framing_analytical_question",
                    "stakeholder.identifying_requirements"
                ],
                "fact_ids": [
                    "stakeholder.identifying_decision_need#f1",
                    "stakeholder.identifying_decision_need#f2"
                ],
                "teaching_block_ids": ["stakeholder.identifying_decision_need#tb4"]
            }
        },
        {
            "type": "up_next",
            "block_id": f"{tile_id}.s18.b2",
            "title": "Up next: Making a data-driven recommendation",
            "text": (
                "In the next tile you will learn how to translate an analytical finding into "
                "a clear, actionable recommendation — the step that turns analysis into a decision."
            )
        }
    ],
    "reward": {"gems": 5},
    "lineage": {
        "concept_ids": [
            "stakeholder.identifying_decision_need",
            "stakeholder.precise_finding_statement",
            "stakeholder.framing_analytical_question",
            "stakeholder.identifying_requirements"
        ],
        "fact_ids": [
            "stakeholder.identifying_decision_need#f1",
            "stakeholder.identifying_decision_need#f2"
        ],
        "teaching_block_ids": ["stakeholder.identifying_decision_need#tb4"]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# REMEDIATION STEPS
# Rule: one remediation per first check/hands_on of each concept,
# re-teaching the facts that check measures.
#
# Concepts and their first check/hands_on:
#   stakeholder.identifying_decision_need → s02 (check, f1+f2)
#   stakeholder.precise_finding_statement → s06 (check, f3) — but s04 visual teaches f2
#     Also s07 hands_on measures f2,f4,f5 — different facts from s06 → separate remediation
#   stakeholder.framing_analytical_question → s10 (check, f3)
#     s11 (check, f2) — different fact → separate remediation
#   stakeholder.identifying_requirements → s15 (check, f1+f2+f3)
#     s16 (check, f4+f5) — different facts → separate remediation
# ─────────────────────────────────────────────────────────────────────────────

remediation_steps = []

# r01 – for s02 (check on f1, f2 of identifying_decision_need)
r01_text = (
    "Analysis is the collection, manipulation and interpretation of information and data for "
    "use in decision-making. The engagement and scoping stage of an analytical project should "
    "establish an understanding of how the analysis will inform decisions. "
    "When the operations manager asks you to \"look into delivery times,\" the decision could be "
    "whether to hire more Lagos couriers or whether to renegotiate with a courier partner — "
    "two very different analyses. Naming the decision first tells you what to measure."
)
print(f"\nr01 words: {wc(r01_text)}")

remediation_steps.append({
    "step_id": f"{tile_id}.r01",
    "type": "remediation",
    "concept_ids": ["stakeholder.identifying_decision_need"],
    "eyebrow": "Let's revisit",
    "title": "Analysis serves a decision — a closer look",
    "lede": "Here is a clear contrast to help you see the connection between a request and the decision behind it.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.r01.b1",
            "role": "definition",
            "text": r01_text,
            "lineage": {
                "concept_ids": ["stakeholder.identifying_decision_need"],
                "fact_ids": [
                    "stakeholder.identifying_decision_need#f1",
                    "stakeholder.identifying_decision_need#f2"
                ],
                "teaching_block_ids": [
                    "stakeholder.identifying_decision_need#tb2",
                    "stakeholder.identifying_decision_need#tb3"
                ]
            }
        }
    ],
    "reward": {"gems": 0},
    "lineage": {
        "concept_ids": ["stakeholder.identifying_decision_need"],
        "fact_ids": [
            "stakeholder.identifying_decision_need#f1",
            "stakeholder.identifying_decision_need#f2"
        ],
        "teaching_block_ids": [
            "stakeholder.identifying_decision_need#tb2",
            "stakeholder.identifying_decision_need#tb3"
        ]
    }
})

# r02 – for s06 (check on f3 of precise_finding_statement: narrow_claim_to_match_data)
r02_text = (
    "A claim about the data should be checked against what the data actually shows, and narrowed "
    "if needed. If the delivery data shows only Lagos routes slowed down, the claim "
    "\"delivery times went up\" is too broad — it should narrow to \"Lagos delivery times went up.\" "
    "One published example revised \"Price has declined for all products\" to "
    "\"the average retail price of existing products declined\" once the data was examined. "
    "Always match the scope of the claim to the scope of the evidence."
)
print(f"r02 words: {wc(r02_text)}")

remediation_steps.append({
    "step_id": f"{tile_id}.r02",
    "type": "remediation",
    "concept_ids": ["stakeholder.precise_finding_statement"],
    "eyebrow": "Let's revisit",
    "title": "Narrowing a claim to match the data",
    "lede": "Here is a clear contrast to help you see when a claim is too broad for the evidence.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.r02.b1",
            "role": "mechanism",
            "text": r02_text,
            "lineage": {
                "concept_ids": ["stakeholder.precise_finding_statement"],
                "fact_ids": ["stakeholder.precise_finding_statement#f3"],
                "teaching_block_ids": ["stakeholder.precise_finding_statement#tb3"]
            }
        }
    ],
    "reward": {"gems": 0},
    "lineage": {
        "concept_ids": ["stakeholder.precise_finding_statement"],
        "fact_ids": ["stakeholder.precise_finding_statement#f3"],
        "teaching_block_ids": ["stakeholder.precise_finding_statement#tb3"]
    }
})

# r03 – for s07 (hands_on on f2, f4, f5: complete sentence + specific number + comparison)
r03_text = (
    "A communication's big idea must be a complete sentence — not a fragment or a topic label. "
    "\"Lagos delivery times\" is only a topic label. Writing about data should be specific about "
    "the point being made, and putting data into context includes making comparisons. "
    "\"The average Lagos delivery time rose to 30 minutes this month, up from 22 minutes last month\" "
    "is a complete sentence that names the number (30 minutes) and the comparison (up from 22 minutes). "
    "That is the pattern: position + number + comparison."
)
print(f"r03 words: {wc(r03_text)}")

remediation_steps.append({
    "step_id": f"{tile_id}.r03",
    "type": "remediation",
    "concept_ids": ["stakeholder.precise_finding_statement"],
    "eyebrow": "Let's revisit",
    "title": "Complete sentence, specific number, comparison",
    "lede": "Here is a clear contrast between a topic label and a precise finding sentence.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.r03.b1",
            "role": "example",
            "text": r03_text,
            "lineage": {
                "concept_ids": ["stakeholder.precise_finding_statement"],
                "fact_ids": [
                    "stakeholder.precise_finding_statement#f2",
                    "stakeholder.precise_finding_statement#f4",
                    "stakeholder.precise_finding_statement#f5"
                ],
                "teaching_block_ids": [
                    "stakeholder.precise_finding_statement#tb2",
                    "stakeholder.precise_finding_statement#tb4"
                ]
            }
        }
    ],
    "reward": {"gems": 0},
    "lineage": {
        "concept_ids": ["stakeholder.precise_finding_statement"],
        "fact_ids": [
            "stakeholder.precise_finding_statement#f2",
            "stakeholder.precise_finding_statement#f4",
            "stakeholder.precise_finding_statement#f5"
        ],
        "teaching_block_ids": [
            "stakeholder.precise_finding_statement#tb2",
            "stakeholder.precise_finding_statement#tb4"
        ]
    }
})

# r04 – for s10 (check on f3 of framing_analytical_question: components of well-formed question)
r04_text = (
    "A well-formed statistical question makes clear the variable of interest, the group it "
    "focuses on, and its intent — describing the data, comparing a variable across two or more "
    "groups, or looking at an association between two variables — and can be answered with data "
    "collected or already in hand. \"Is average delivery time in Lagos this month higher than "
    "last month?\" names the variable (delivery time), the group (Lagos, this month vs. last), "
    "and the intent (a comparison). \"Are we doing well?\" names none of these."
)
print(f"r04 words: {wc(r04_text)}")

remediation_steps.append({
    "step_id": f"{tile_id}.r04",
    "type": "remediation",
    "concept_ids": ["stakeholder.framing_analytical_question"],
    "eyebrow": "Let's revisit",
    "title": "The three components of a well-formed statistical question",
    "lede": "Here is a clear contrast between a vague question and a well-formed one.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.r04.b1",
            "role": "definition",
            "text": r04_text,
            "lineage": {
                "concept_ids": ["stakeholder.framing_analytical_question"],
                "fact_ids": ["stakeholder.framing_analytical_question#f3"],
                "teaching_block_ids": ["stakeholder.framing_analytical_question#tb3"]
            }
        }
    ],
    "reward": {"gems": 0},
    "lineage": {
        "concept_ids": ["stakeholder.framing_analytical_question"],
        "fact_ids": ["stakeholder.framing_analytical_question#f3"],
        "teaching_block_ids": ["stakeholder.framing_analytical_question#tb3"]
    }
})

# r05 – for s11 (check on f2 of framing_analytical_question: scoping stage agreement on outputs)
r05_text = (
    "The engagement and scoping stage should lead to agreement between the analyst and "
    "commissioner about the outputs of the work, including acceptable levels of accuracy, "
    "precision and margins of error, so both sides know in advance what kind of answer will "
    "count as sufficient. For the delivery request, that could mean agreeing that a one-page "
    "summary with a bar chart of average delivery time per city is sufficient — rather than "
    "discovering at the end that the manager expected a full statistical report."
)
print(f"r05 words: {wc(r05_text)}")

remediation_steps.append({
    "step_id": f"{tile_id}.r05",
    "type": "remediation",
    "concept_ids": ["stakeholder.framing_analytical_question"],
    "eyebrow": "Let's revisit",
    "title": "Agreeing on outputs during scoping",
    "lede": "Here is a clear contrast to help you see why output agreement matters.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.r05.b1",
            "role": "practical_context",
            "text": r05_text,
            "lineage": {
                "concept_ids": ["stakeholder.framing_analytical_question"],
                "fact_ids": ["stakeholder.framing_analytical_question#f2"],
                "teaching_block_ids": ["stakeholder.framing_analytical_question#tb4"]
            }
        }
    ],
    "reward": {"gems": 0},
    "lineage": {
        "concept_ids": ["stakeholder.framing_analytical_question"],
        "fact_ids": ["stakeholder.framing_analytical_question#f2"],
        "teaching_block_ids": ["stakeholder.framing_analytical_question#tb4"]
    }
})

# r06 – for s15 (check on f1, f2, f3 of identifying_requirements)
r06_text = (
    "In the engagement and scoping stage, the commissioner should inform the analyst about the "
    "important aspects of the problem, its scope, and any constraints or issues, and should "
    "communicate any relevant information about data sources and data quality — for the delivery "
    "request, that could mean telling you which system holds delivery timestamps and whether any "
    "routes are missing GPS data. The analyst should then create a specification document "
    "capturing these requirements and share it with the commissioner for sign-off."
)
print(f"r06 words: {wc(r06_text)}")

remediation_steps.append({
    "step_id": f"{tile_id}.r06",
    "type": "remediation",
    "concept_ids": ["stakeholder.identifying_requirements"],
    "eyebrow": "Let's revisit",
    "title": "Commissioner inputs and the specification document — a closer look",
    "lede": "Here is a clear contrast to help you see what the commissioner provides and what the analyst captures.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.r06.b1",
            "role": "mechanism",
            "text": r06_text,
            "lineage": {
                "concept_ids": ["stakeholder.identifying_requirements"],
                "fact_ids": [
                    "stakeholder.identifying_requirements#f1",
                    "stakeholder.identifying_requirements#f2",
                    "stakeholder.identifying_requirements#f3"
                ],
                "teaching_block_ids": [
                    "stakeholder.identifying_requirements#tb2",
                    "stakeholder.identifying_requirements#tb4"
                ]
            }
        }
    ],
    "reward": {"gems": 0},
    "lineage": {
        "concept_ids": ["stakeholder.identifying_requirements"],
        "fact_ids": [
            "stakeholder.identifying_requirements#f1",
            "stakeholder.identifying_requirements#f2",
            "stakeholder.identifying_requirements#f3"
        ],
        "teaching_block_ids": [
            "stakeholder.identifying_requirements#tb2",
            "stakeholder.identifying_requirements#tb4"
        ]
    }
})

# r07 – for s16 (check on f4, f5 of identifying_requirements)
r07_text = (
    "Constraints around resources and timelines should be clarified and agreed between the "
    "analyst and commissioner during engagement and scoping — for instance, whether the manager "
    "needs an answer this week or can wait for a fuller analysis next month. The engagement and "
    "scoping stage should lead to agreement between the analyst and commissioner about the "
    "outputs of the work — for instance, agreeing the deliverable is a one-page summary with "
    "a bar chart of average delivery time per city."
)
print(f"r07 words: {wc(r07_text)}")

remediation_steps.append({
    "step_id": f"{tile_id}.r07",
    "type": "remediation",
    "concept_ids": ["stakeholder.identifying_requirements"],
    "eyebrow": "Let's revisit",
    "title": "Resource constraints and output agreement — a closer look",
    "lede": "Here is a clear contrast to help you see what constraints and output agreement mean in practice.",
    "blocks": [
        {
            "type": "prose",
            "block_id": f"{tile_id}.r07.b1",
            "role": "mechanism",
            "text": r07_text,
            "lineage": {
                "concept_ids": ["stakeholder.identifying_requirements"],
                "fact_ids": [
                    "stakeholder.identifying_requirements#f4",
                    "stakeholder.identifying_requirements#f5"
                ],
                "teaching_block_ids": [
                    "stakeholder.identifying_requirements#tb3",
                    "stakeholder.identifying_requirements#tb4"
                ]
            }
        }
    ],
    "reward": {"gems": 0},
    "lineage": {
        "concept_ids": ["stakeholder.identifying_requirements"],
        "fact_ids": [
            "stakeholder.identifying_requirements#f4",
            "stakeholder.identifying_requirements#f5"
        ],
        "teaching_block_ids": [
            "stakeholder.identifying_requirements#tb3",
            "stakeholder.identifying_requirements#tb4"
        ]
    }
})

# ─────────────────────────────────────────────────────────────────────────────
# Assemble final document
# ─────────────────────────────────────────────────────────────────────────────
doc = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_007_da_nocode",
    "tiles": [
        {
            "tile_id": tile_id,
            "title": "Identifying Decisions, Findings, and Requirements",
            "steps": steps,
            "remediation_steps": remediation_steps
        }
    ]
}

out_path = "batches/final_batch_007_da_nocode/screens.part.c1.json"
with open(out_path, "w") as f:
    json.dump(doc, f, indent=2)

print(f"\nWrote {out_path}")
print(f"Steps: {len(steps)}")
print(f"Remediation steps: {len(remediation_steps)}")
print("Step ids:", [s['step_id'] for s in steps])
print("Remediation ids:", [r['step_id'] for r in remediation_steps])
