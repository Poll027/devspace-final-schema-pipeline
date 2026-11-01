"""Build interactions.part.c1.json for tile_stakeholder_framing_requirements."""
import json

# ── helpers ──────────────────────────────────────────────────────────────────
def choice(step_id, difficulty, measures, anchors, prompt, options, correct_ids,
           option_feedback, correct_msg, incorrect_msg, hints,
           remediation_step_id=None, standalone=False, selection="single"):
    ix = {
        "type": "choice",
        "interaction_id": f"ix.{step_id}",
        "difficulty": difficulty,
        "grading_mode": "client",
        "standalone": standalone,
        "measures": measures,
        "anchors": anchors,
        "public": {
            "prompt": prompt,
            "options": [{"option_id": oid, "text": txt} for oid, txt in options],
            "selection": selection,
            "shuffle": True,
        },
        "grading": {
            "correct_option_ids": correct_ids,
            "option_feedback": {oid: {"message": msg} for oid, msg in option_feedback.items()},
        },
        "feedback": {
            "correct": {"message": correct_msg},
            "incorrect": {"message": incorrect_msg},
            "hints": hints,
        },
    }
    if remediation_step_id:
        ix["feedback"]["remediation_step_id"] = remediation_step_id
    return ix


def table_select(step_id, difficulty, measures, anchors, asset_id, variant_id,
                 columns, intro, tasks, answers, task_feedback,
                 correct_msg, incorrect_msg, hints,
                 remediation_step_id=None, standalone=False):
    ix = {
        "type": "table_select",
        "interaction_id": f"ix.{step_id}",
        "difficulty": difficulty,
        "grading_mode": "client",
        "standalone": standalone,
        "measures": measures,
        "anchors": anchors,
        "public": {
            "asset_ref": {"asset_id": asset_id, "variant_id": variant_id, "columns": columns},
            "intro": intro,
            "tasks": tasks,
        },
        "grading": {
            "answers": answers,
            "task_feedback": task_feedback,
        },
        "feedback": {
            "correct": {"message": correct_msg},
            "incorrect": {"message": incorrect_msg},
            "hints": hints,
        },
    }
    if remediation_step_id:
        ix["feedback"]["remediation_step_id"] = remediation_step_id
    return ix


def external_proof(step_id, difficulty, measures, anchors, instruction, evidence_kinds,
                   checklist, grading_mode_val, rubric,
                   correct_msg, incorrect_msg, hints,
                   remediation_step_id=None, standalone=False):
    ix = {
        "type": "external_proof",
        "interaction_id": f"ix.{step_id}",
        "difficulty": difficulty,
        "grading_mode": grading_mode_val,
        "standalone": standalone,
        "measures": measures,
        "anchors": anchors,
        "public": {
            "instruction": instruction,
            "evidence_kinds": evidence_kinds,
            "checklist": checklist,
        },
        "grading": {
            "mode": "self_attest",
            "rubric": rubric,
        },
        "feedback": {
            "correct": {"message": correct_msg},
            "incorrect": {"message": incorrect_msg},
            "hints": hints,
        },
    }
    if remediation_step_id:
        ix["feedback"]["remediation_step_id"] = remediation_step_id
    return ix


def classify(step_id, difficulty, measures, anchors, prompt, buckets, items,
             assignments, role_map, item_feedback,
             correct_msg, incorrect_msg, hints,
             remediation_step_id=None, standalone=False):
    ix = {
        "type": "classify",
        "interaction_id": f"ix.{step_id}",
        "difficulty": difficulty,
        "grading_mode": "client",
        "standalone": standalone,
        "measures": measures,
        "anchors": anchors,
        "public": {
            "prompt": prompt,
            "buckets": [{"bucket_id": bid, "label": lbl} for bid, lbl in buckets],
            "items": items,
        },
        "grading": {
            "assignments": assignments,
            "role_map": role_map,
            "item_feedback": {iid: {"message": msg} for iid, msg in item_feedback.items()},
        },
        "feedback": {
            "correct": {"message": correct_msg},
            "incorrect": {"message": incorrect_msg},
            "hints": hints,
        },
    }
    if remediation_step_id:
        ix["feedback"]["remediation_step_id"] = remediation_step_id
    return ix


# Remediation step IDs (from assembled tile_lessons):
# r01: stakeholder.identifying_decision_need f1, f2
# r02: stakeholder.precise_finding_statement f3
# r03: stakeholder.precise_finding_statement f2, f4, f5
# r04: stakeholder.framing_analytical_question f3
# r05: stakeholder.framing_analytical_question f2
# r06: stakeholder.identifying_requirements f1, f2, f3
# r07: stakeholder.identifying_requirements f4, f5
REM = {
    "idn_first":  "tile_stakeholder_framing_requirements.r01",
    "pfs_f3":     "tile_stakeholder_framing_requirements.r02",
    "pfs_first":  "tile_stakeholder_framing_requirements.r03",
    "faq_f3":     "tile_stakeholder_framing_requirements.r04",
    "faq_f2":     "tile_stakeholder_framing_requirements.r05",
    "ir_first":   "tile_stakeholder_framing_requirements.r06",
    "ir_f4f5":    "tile_stakeholder_framing_requirements.r07",
}

# ── s02: choice — identify_decision_behind_stakeholder_request ───────────────
# Taught by s01 (f1, f2). Tests f1 and f2.
# First check for identifying_decision_need → remediation_step_id = r01
s02 = choice(
    step_id="tile_stakeholder_framing_requirements.s02",
    difficulty="intro",
    measures=[
        {
            "concept_id": "stakeholder.identifying_decision_need",
            "capability": "identify_decision_behind_stakeholder_request",
            "fact_ids": ["f1", "f2"],
        }
    ],
    anchors=["stakeholder.identifying_decision_need#assessment:identify_decision_behind_stakeholder_request"],
    prompt=(
        "The operations manager sends you this message: \"Can you look into our delivery times?\"\n\n"
        "What is the most useful first step before you start any analysis?"
    ),
    options=[
        ("opt_s02_a", "Ask the manager what decision this analysis is meant to inform — for example, whether to add couriers on the Lagos route or renegotiate with a courier partner."),
        ("opt_s02_b", "Open the delivery-orders table and calculate the average delivery time straight away, because that is what the manager asked for."),
        ("opt_s02_c", "Ask the manager to send you a list of metrics they want, so you can measure each one."),
        ("opt_s02_d", "Decide on your own which decision the analysis is for, so you can start without delay."),
    ],
    correct_ids=["opt_s02_a"],
    option_feedback={
        "opt_s02_b": (
            "Starting the analysis immediately risks measuring the wrong thing. "
            "Analysis is for decision-making, and the engagement and scoping stage should establish "
            "how the analysis will inform a decision before any calculation begins."
        ),
        "opt_s02_c": (
            "A list of metrics is not the same as a decision. The goal is to identify what the manager "
            "needs to decide — the metrics follow from that, not the other way around."
        ),
        "opt_s02_d": (
            "Deciding on the manager's behalf skips the engagement and scoping stage. "
            "The scoping stage should establish an understanding of how the analysis will inform decisions "
            "by engaging with the commissioner, not by guessing."
        ),
    },
    correct_msg=(
        "Correct. Analysis is for decision-making, and the engagement and scoping stage should establish "
        "how the analysis will inform a decision. Asking the manager what decision they face — "
        "add couriers? renegotiate a contract? — gives the analysis a clear target."
    ),
    incorrect_msg=(
        "Think about why analysis exists: it is the collection, manipulation and interpretation of "
        "information for use in decision-making. Before measuring anything, the scoping stage should "
        "establish what decision the analysis is meant to inform."
    ),
    hints=[
        "What does the engagement and scoping stage exist to establish?",
        "If the manager's decision turns out to be about renegotiating a contract, would 'average delivery time per city' be the right thing to measure?",
    ],
    remediation_step_id=REM["idn_first"],
)

# ── s03: table_select — identify_decision_behind_stakeholder_request (hands_on) ──
# Practice anchor: field_selection. Taught by s01 (f1, f2).
# ds_stakeholder_requests columns: request_id, request_text, decision, ...
# Task: given request_text for row 2 ("Can you check how our drivers are doing?"),
#       select the cell that names the decision it is meant to inform.
# Answer: row where request_id=2, column "decision"
#   → "Decide whether to renegotiate the contract with the courier partner"
# No remediation_step_id for second check/hands-on of same concept (per GENERATOR rule)
s03 = table_select(
    step_id="tile_stakeholder_framing_requirements.s03",
    difficulty="core",
    measures=[
        {
            "concept_id": "stakeholder.identifying_decision_need",
            "capability": "identify_decision_behind_stakeholder_request",
            "fact_ids": ["f1", "f2"],
        }
    ],
    anchors=[
        "stakeholder.identifying_decision_need#practice",
        "stakeholder.identifying_decision_need#assessment:identify_decision_behind_stakeholder_request",
    ],
    asset_id="ds_stakeholder_requests",
    variant_id=None,
    columns=["request_id", "request_text", "decision"],
    intro=(
        "The table below shows stakeholder requests and the decision each one is meant to inform. "
        "Read the request in row 2, then complete the task."
    ),
    tasks=[
        {
            "task_id": "task_s03_t1",
            "prompt": (
                "The manager says: \"Can you check how our drivers are doing?\" "
                "Click the cell in the table that names the specific decision this request is meant to inform."
            ),
            "target_kind": "cell",
        }
    ],
    answers=[
        {
            "task_id": "task_s03_t1",
            "row": {"where": {"request_id": 2}},
            "column": "decision",
            "expect_value": "Decide whether to renegotiate the contract with the courier partner",
        }
    ],
    task_feedback={
        "task_s03_t1": {
            "correct": "Correct. The request is about driver performance, and the underlying decision is whether to renegotiate the courier partner contract.",
            "incorrect": "Look for the cell that names a specific decision — something the manager would act on — not a restatement of the request or a metric.",
        }
    },
    correct_msg=(
        "Well done. The request 'Can you check how our drivers are doing?' hides the decision: "
        "whether to renegotiate the contract with the courier partner. "
        "Naming the decision before starting analysis keeps the work focused."
    ),
    incorrect_msg=(
        "The decision is not the same as the request. Look for the cell that names what the manager "
        "would actually do with the analysis result — a concrete action or choice."
    ),
    hints=[
        "The decision column names what the manager would do with the result, not what they asked you to measure.",
        "A decision is something you act on: 'renegotiate', 'hire', 'expand' — not 'look into' or 'check'.",
    ],
)

# ── s06: choice — narrow_claim_to_match_data ─────────────────────────────────
# Taught by s04 (f2) and s05 (f3, f4, f5). Tests f3.
# f3: A claim about the data should be checked against what the data actually shows,
#     and narrowed if needed.
# First check for precise_finding_statement → remediation_step_id = r02 (re-teaches f3)
s06 = choice(
    step_id="tile_stakeholder_framing_requirements.s06",
    difficulty="intro",
    measures=[
        {
            "concept_id": "stakeholder.precise_finding_statement",
            "capability": "narrow_claim_to_match_data",
            "fact_ids": ["f3"],
        }
    ],
    anchors=["stakeholder.precise_finding_statement#assessment:narrow_claim_to_match_data"],
    prompt=(
        "An analyst writes this finding after reviewing the Kwik Courier data:\n\n"
        "\"Delivery times have declined for all cities.\"\n\n"
        "The data shows: Lagos average rose from 22 to 30 minutes; Abuja average fell from 23 to 20 minutes; "
        "Port Harcourt average fell from 27 to 25 minutes.\n\n"
        "What should the analyst do?"
    ),
    options=[
        ("opt_s06_a", "Narrow the claim to match what the data actually shows — for example: 'Average delivery times fell in Abuja and Port Harcourt, but rose in Lagos.'"),
        ("opt_s06_b", "Keep the claim as written, because two out of three cities did show a decline."),
        ("opt_s06_c", "Remove the finding entirely, because the data is contradictory."),
        ("opt_s06_d", "Broaden the claim to 'delivery times have changed across all cities' so it is always true."),
    ],
    correct_ids=["opt_s06_a"],
    option_feedback={
        "opt_s06_b": (
            "A claim should be checked against what the data actually shows and narrowed if needed. "
            "Saying 'all cities' when Lagos shows the opposite is a claim the data does not support."
        ),
        "opt_s06_c": (
            "The data is not contradictory — it shows different trends in different cities. "
            "The right response is to narrow the claim to match what the data actually shows, not to remove it."
        ),
        "opt_s06_d": (
            "Broadening the claim makes it vaguer, not more precise. "
            "A precise finding names the specific pattern the data shows, not a statement so general it is always true."
        ),
    },
    correct_msg=(
        "Correct. A claim about the data should be checked against what the data actually shows and narrowed if needed. "
        "The original claim overstates the finding; the narrowed version accurately reflects the city-level pattern."
    ),
    incorrect_msg=(
        "Check the data against the claim: does 'all cities' match what the numbers show? "
        "A precise finding is narrowed to match the data, not stretched to cover cases the data contradicts."
    ),
    hints=[
        "Does the Lagos data support the claim that delivery times declined for all cities?",
        "What would a claim look like that is true for Abuja and Port Harcourt but honest about Lagos?",
    ],
    remediation_step_id=REM["pfs_f3"],
)

# ── s07: external_proof — precise_finding_statement (hands_on) ───────────────
# Practice anchor: external_proof. Taught by s04 (f2) and s05 (f3, f4, f5). Tests f2, f4, f5.
# f2: big idea = unique point of view + what's at stake + complete sentence
# f4: writing about data should be specific about the point being made
# f5: putting data into context includes making comparisons
# Success: complete sentence, specific number, comparison to prior period.
# No remediation_step_id for second check/hands-on of same concept (per GENERATOR rule)
s07 = external_proof(
    step_id="tile_stakeholder_framing_requirements.s07",
    difficulty="core",
    measures=[
        {
            "concept_id": "stakeholder.precise_finding_statement",
            "capability": "identify_complete_sentence_big_idea",
            "fact_ids": ["f2"],
        },
        {
            "concept_id": "stakeholder.precise_finding_statement",
            "capability": "state_finding_with_specific_number_and_comparison",
            "fact_ids": ["f4", "f5"],
        },
    ],
    anchors=[
        "stakeholder.precise_finding_statement#practice",
        "stakeholder.precise_finding_statement#assessment:identify_complete_sentence_big_idea",
        "stakeholder.precise_finding_statement#assessment:state_finding_with_specific_number_and_comparison",
    ],
    instruction=(
        "Rewrite the vague finding below as a precise, quantified statement.\n\n"
        "Vague finding: \"Sales went up.\"\n\n"
        "Use the Kwik Courier delivery-orders data you have seen in this tile. "
        "Your rewritten statement must:\n"
        "1. Be a complete sentence (subject + verb).\n"
        "2. Name at least one specific number from the data.\n"
        "3. Include a comparison — to a previous period, a target, or another group.\n\n"
        "Write your statement in the text box, then check each criterion below before submitting."
    ),
    evidence_kinds=["text"],
    checklist=[
        "My statement is a complete sentence with a subject and a verb.",
        "My statement names at least one specific number (e.g. a count, average, or percentage).",
        "My statement includes a comparison (e.g. 'up from', 'compared with', 'above the target').",
        "My statement contains no vague qualitative language such as 'went up', 'improved', or 'a lot'.",
    ],
    grading_mode_val="client",
    rubric=[
        {"criterion": "The statement is a complete sentence with a subject and a verb.", "weight": 1},
        {"criterion": "The statement names at least one specific number from the Kwik Courier data.", "weight": 1},
        {"criterion": "The statement includes a comparison to a prior period, a target, or another group.", "weight": 1},
        {"criterion": "The statement contains no vague qualitative language.", "weight": 1},
    ],
    correct_msg=(
        "Well done. A precise finding is a complete sentence that names a specific number and puts it in context "
        "with a comparison — for example: 'Kwik Courier completed 12 delivery orders in the sample week, "
        "with Lagos accounting for 5 of those orders — the highest share of any city.' "
        "That is the kind of statement a stakeholder can act on."
    ),
    incorrect_msg=(
        "Review your statement against the checklist. A precise finding must be a complete sentence, "
        "name at least one specific number, and include a comparison. "
        "Vague language like 'went up' or 'improved' should be replaced with the actual figure."
    ),
    hints=[
        "Look at the delivery-orders data: how many orders were there in total, and how many were in Lagos?",
        "A comparison could be 'the highest share of any city' or 'up from last month' — something that gives the number context.",
    ],
)

# ── s10: choice — identify_components_of_a_well_formed_statistical_question ──
# Taught by s08 (f1, f3) and s09 (f2). Tests f3.
# f3: A well-formed statistical question makes clear the variable(s) of interest,
#     the group it focuses on, and its intent.
# First check for framing_analytical_question → remediation_step_id = r04 (re-teaches f3)
s10 = choice(
    step_id="tile_stakeholder_framing_requirements.s10",
    difficulty="intro",
    measures=[
        {
            "concept_id": "stakeholder.framing_analytical_question",
            "capability": "identify_components_of_a_well_formed_statistical_question",
            "fact_ids": ["f3"],
        }
    ],
    anchors=["stakeholder.framing_analytical_question#assessment:identify_components_of_a_well_formed_statistical_question"],
    prompt=(
        "Which of the following is a well-formed statistical question?"
    ),
    options=[
        ("opt_s10_a", "Is the average delivery time in Lagos this month higher than last month? (variable: delivery time; group: Lagos, this month vs last month; intent: comparison)"),
        ("opt_s10_b", "Are deliveries going well? (no variable, no group, no intent specified)"),
        ("opt_s10_c", "What is happening with our drivers? (no measurable variable, no group, no intent)"),
        ("opt_s10_d", "Delivery times. (a topic label, not a question)"),
    ],
    correct_ids=["opt_s10_a"],
    option_feedback={
        "opt_s10_b": (
            "This question cannot be answered with data as written. It names no measurable variable, "
            "no group, and no intent. A well-formed statistical question must make all three clear."
        ),
        "opt_s10_c": (
            "This question names no measurable variable (what about drivers?), no group (which drivers? when?), "
            "and no intent (description, comparison, or association?). It cannot be answered with data as written."
        ),
        "opt_s10_d": (
            "This is a topic label, not a question. A well-formed statistical question must be a question "
            "that names a variable, a group, and an intent, and can be answered with data."
        ),
    },
    correct_msg=(
        "Correct. A well-formed statistical question makes clear the variable of interest (delivery time), "
        "the group it focuses on (Lagos, this month vs last month), and its intent (comparison). "
        "It can be answered with data already in hand."
    ),
    incorrect_msg=(
        "A well-formed statistical question must name three things: the variable of interest, "
        "the group it focuses on, and its intent — describing, comparing, or looking for an association. "
        "Which option does all three?"
    ),
    hints=[
        "Can you identify a measurable variable, a specific group, and a clear intent in each option?",
        "A question that can't be answered with data as written is not yet well-formed.",
    ],
    remediation_step_id=REM["faq_f3"],
)

# ── s11: choice — describe_scoping_stage_agreement_on_outputs ────────────────
# Taught by s09 (f2). Tests f2.
# f2: The engagement and scoping stage should lead to agreement between the analyst
#     and commissioner about the outputs of the work.
# No remediation_step_id for second check/hands-on of same concept (per GENERATOR rule)
s11 = choice(
    step_id="tile_stakeholder_framing_requirements.s11",
    difficulty="core",
    measures=[
        {
            "concept_id": "stakeholder.framing_analytical_question",
            "capability": "describe_scoping_stage_agreement_on_outputs",
            "fact_ids": ["f2"],
        }
    ],
    anchors=["stakeholder.framing_analytical_question#assessment:describe_scoping_stage_agreement_on_outputs"],
    prompt=(
        "At the end of the engagement and scoping stage for the Kwik Courier delivery-times project, "
        "the analyst and the operations manager should agree on which of the following?"
    ),
    options=[
        ("opt_s11_a", "The outputs of the work, including acceptable levels of accuracy, precision and margins of error — for example, agreeing that a one-page summary with a bar chart of average delivery time per city is the deliverable."),
        ("opt_s11_b", "The exact SQL queries the analyst will use to extract the data, so the manager can review the code."),
        ("opt_s11_c", "The final conclusions of the analysis, so the manager knows the answer before the work begins."),
        ("opt_s11_d", "The list of all possible metrics that could be calculated from the delivery-orders table."),
    ],
    correct_ids=["opt_s11_a"],
    option_feedback={
        "opt_s11_b": (
            "The scoping stage is about agreeing on outputs and requirements, not on the technical implementation. "
            "The manager does not need to review SQL queries at this stage."
        ),
        "opt_s11_c": (
            "The conclusions cannot be agreed before the analysis is done — that would mean the analysis is not needed. "
            "The scoping stage agrees on the outputs (what will be delivered), not the findings."
        ),
        "opt_s11_d": (
            "Listing all possible metrics is not the goal of scoping. "
            "The scoping stage should lead to agreement on the specific outputs of this project, "
            "including what level of accuracy is acceptable."
        ),
    },
    correct_msg=(
        "Correct. The engagement and scoping stage should lead to agreement between the analyst and commissioner "
        "about the outputs of the work, including acceptable levels of accuracy, precision and margins of error. "
        "For the delivery-times project, that means agreeing on the deliverable — for example, a one-page summary "
        "with a bar chart of average delivery time per city."
    ),
    incorrect_msg=(
        "The scoping stage is about agreeing on what will be delivered and at what level of accuracy — "
        "not on the technical method, the final conclusions, or an exhaustive list of metrics."
    ),
    hints=[
        "What does the scoping stage produce that both the analyst and commissioner sign off on?",
        "Think about what 'outputs of the work' means: what format, what level of detail, what accuracy?",
    ],
)

# ── s12: classify — framing_analytical_question (hands_on) ───────────────────
# Practice anchor: matching. Taught by s08 (f1, f3) and s09 (f2). Tests f1, f3.
# Buckets: Variable of interest, Group or time period, Intent, Not a component
# Items from ds_stakeholder_requests row 1 (request_id=1):
#   variable_of_interest (categorical) → bucket_variable
#   group_or_period (categorical) → bucket_group
#   intent (categorical) → bucket_intent
#   vague_question (text) → bucket_none  (trap item)
#
# role_map maps bucket_id → semantic_role of the source column.
# All three "correct" buckets use categorical columns; the trap uses a text column.
# role_map must match: bucket_variable→"categorical", bucket_group→"categorical",
#   bucket_intent→"categorical", bucket_none→"text"
s12 = classify(
    step_id="tile_stakeholder_framing_requirements.s12",
    difficulty="core",
    measures=[
        {
            "concept_id": "stakeholder.framing_analytical_question",
            "capability": "restate_vague_question_as_measurable_analytical_question",
            "fact_ids": ["f1", "f3"],
        },
        {
            "concept_id": "stakeholder.framing_analytical_question",
            "capability": "identify_scoping_conversation_elements",
            "fact_ids": ["f1"],
        },
    ],
    anchors=[
        "stakeholder.framing_analytical_question#practice",
        "stakeholder.framing_analytical_question#assessment:restate_vague_question_as_measurable_analytical_question",
        "stakeholder.framing_analytical_question#assessment:identify_scoping_conversation_elements",
    ],
    prompt=(
        "The operations manager asks: \"Can you look into our delivery times?\"\n\n"
        "After a scoping conversation, the analyst frames this as the measurable question: "
        "\"Is the average delivery time in Lagos this month higher than last month?\"\n\n"
        "Classify each phrase below as the Variable of interest, the Group or time period, "
        "or the Intent of that well-formed question. "
        "One item does not belong to any component — drag it to 'Not a component'."
    ),
    buckets=[
        ("bucket_variable", "Variable of interest"),
        ("bucket_group", "Group or time period"),
        ("bucket_intent", "Intent"),
        ("bucket_none", "Not a component"),
    ],
    items=[
        {
            "item_id": "item_s12_var",
            "text": "delivery time",
            "source": {
                "asset_id": "ds_stakeholder_requests",
                "row": {"where": {"request_id": 1}},
                "column": "variable_of_interest",
            },
        },
        {
            "item_id": "item_s12_grp",
            "text": "Lagos, this month vs last month",
            "source": {
                "asset_id": "ds_stakeholder_requests",
                "row": {"where": {"request_id": 1}},
                "column": "group_or_period",
            },
        },
        {
            "item_id": "item_s12_int",
            "text": "comparison",
            "source": {
                "asset_id": "ds_stakeholder_requests",
                "row": {"where": {"request_id": 1}},
                "column": "intent",
            },
        },
        {
            "item_id": "item_s12_trap",
            "text": "Are our delivery times okay?",
            "source": {
                "asset_id": "ds_stakeholder_requests",
                "row": {"where": {"request_id": 1}},
                "column": "vague_question",
            },
        },
    ],
    assignments={
        "item_s12_var": "bucket_variable",
        "item_s12_grp": "bucket_group",
        "item_s12_int": "bucket_intent",
        "item_s12_trap": "bucket_none",
    },
    # role_map: bucket_id → semantic_role of the source column
    # variable_of_interest, group_or_period, intent are all "categorical"
    # vague_question is "text"
    role_map={
        "bucket_variable": "categorical",
        "bucket_group": "categorical",
        "bucket_intent": "categorical",
        "bucket_none": "text",
    },
    item_feedback={
        "item_s12_var": "Correct. 'Delivery time' is the variable of interest — the measurable quantity the question is about.",
        "item_s12_grp": "Correct. 'Lagos, this month vs last month' specifies the group and time period the question focuses on.",
        "item_s12_int": "Correct. 'Comparison' is the intent — the question asks whether one value is higher than another.",
        "item_s12_trap": "This is the vague question the analyst started with, not a component of the well-formed question. A well-formed statistical question is built from a variable, a group, and an intent — not from restating the original vague request.",
    },
    correct_msg=(
        "Well done. A well-formed statistical question names the variable of interest (delivery time), "
        "the group or time period (Lagos, this month vs last month), and the intent (comparison). "
        "The vague question 'Are our delivery times okay?' is what the scoping conversation starts from — "
        "not a component of the well-formed question."
    ),
    incorrect_msg=(
        "A well-formed statistical question has three components: the variable of interest, "
        "the group or time period, and the intent. "
        "The vague question is what you start with — it is not one of those components."
    ),
    hints=[
        "The variable of interest is the thing you would measure — what quantity does the question ask about?",
        "The intent tells you whether the question is describing, comparing, or looking for an association.",
    ],
)

# ── s15: choice — identify_commissioner_inputs_at_scoping + describe_specification_document_and_sign_off ──
# Taught by s13 (f1, f3, f4) and s14 (f2, f5). Tests f1, f2, f3.
# f1: commissioner informs analyst about problem, scope, constraints
# f2: analyst creates specification document, shares for sign-off
# f3: commissioner communicates data sources and data quality info
# First check for identifying_requirements → remediation_step_id = r06 (re-teaches f1, f2, f3)
s15 = choice(
    step_id="tile_stakeholder_framing_requirements.s15",
    difficulty="intro",
    measures=[
        {
            "concept_id": "stakeholder.identifying_requirements",
            "capability": "identify_commissioner_inputs_at_scoping",
            "fact_ids": ["f1", "f3"],
        },
        {
            "concept_id": "stakeholder.identifying_requirements",
            "capability": "describe_specification_document_and_sign_off",
            "fact_ids": ["f2"],
        },
    ],
    anchors=[
        "stakeholder.identifying_requirements#assessment:identify_commissioner_inputs_at_scoping",
        "stakeholder.identifying_requirements#assessment:describe_specification_document_and_sign_off",
    ],
    prompt=(
        "During the engagement and scoping stage for the Kwik Courier delivery-times project, "
        "which of the following correctly describes what the commissioner provides and what the analyst produces?"
    ),
    options=[
        ("opt_s15_a", "The commissioner informs the analyst about the problem, its scope, constraints, and relevant data sources and data quality; the analyst creates a specification document capturing these requirements and shares it with the commissioner for sign-off."),
        ("opt_s15_b", "The analyst decides the scope and constraints independently, then presents a finished report to the commissioner for approval."),
        ("opt_s15_c", "The commissioner writes the specification document and the analyst signs it off before starting work."),
        ("opt_s15_d", "The commissioner provides the final conclusions of the analysis; the analyst checks whether the data supports them."),
    ],
    correct_ids=["opt_s15_a"],
    option_feedback={
        "opt_s15_b": (
            "The analyst does not decide scope and constraints independently. "
            "In the engagement and scoping stage, the commissioner informs the analyst about the problem, "
            "scope, and constraints. The analyst then creates a specification document — not a finished report."
        ),
        "opt_s15_c": (
            "The roles are reversed. The analyst creates the specification document that captures the commissioner's "
            "requirements, and shares it with the commissioner for sign-off — not the other way around."
        ),
        "opt_s15_d": (
            "The commissioner does not provide conclusions. The commissioner provides information about the problem, "
            "scope, constraints, and data quality. The analyst then creates a specification document before any "
            "analysis begins."
        ),
    },
    correct_msg=(
        "Correct. In the engagement and scoping stage, the commissioner informs the analyst about the problem, "
        "scope, constraints, and data sources and quality. The analyst captures these in a specification document "
        "and shares it with the commissioner for sign-off."
    ),
    incorrect_msg=(
        "Think about who provides what: the commissioner brings knowledge of the problem, scope, constraints, "
        "and data quality; the analyst turns that into a specification document and asks the commissioner to sign it off."
    ),
    hints=[
        "Who knows the most about the business problem and its constraints — the analyst or the commissioner?",
        "What does the analyst produce at the end of the scoping stage, and who approves it?",
    ],
    remediation_step_id=REM["ir_first"],
)

# ── s16: choice — identify_resource_and_timeline_constraints + recognise_output_agreement_as_scoping_outcome ──
# Taught by s13 (f1, f3, f4) and s14 (f2, f5). Tests f4, f5.
# f4: constraints around resources and timelines should be clarified and agreed
# f5: scoping stage should lead to agreement about the outputs of the work
# No remediation_step_id for second check/hands-on of same concept (per GENERATOR rule)
s16 = choice(
    step_id="tile_stakeholder_framing_requirements.s16",
    difficulty="core",
    measures=[
        {
            "concept_id": "stakeholder.identifying_requirements",
            "capability": "identify_resource_and_timeline_constraints",
            "fact_ids": ["f4"],
        },
        {
            "concept_id": "stakeholder.identifying_requirements",
            "capability": "recognise_output_agreement_as_scoping_outcome",
            "fact_ids": ["f5"],
        },
    ],
    anchors=[
        "stakeholder.identifying_requirements#assessment:identify_resource_and_timeline_constraints",
        "stakeholder.identifying_requirements#assessment:recognise_output_agreement_as_scoping_outcome",
    ],
    prompt=(
        "The operations manager says: \"I need the delivery-times analysis by end of next week, "
        "and I want a one-page summary with a bar chart of average delivery time per city.\"\n\n"
        "Which statement best describes what the analyst should do with this information during scoping?"
    ),
    options=[
        ("opt_s16_a", "Clarify and agree the timeline constraint (end of next week) and record the agreed output (one-page summary with a bar chart) in the specification document, so both parties have agreed on the deliverable before analysis begins."),
        ("opt_s16_b", "Ignore the timeline for now and focus on the analysis; the deadline can be discussed later if needed."),
        ("opt_s16_c", "Treat the bar chart request as optional, because the analyst decides the output format independently."),
        ("opt_s16_d", "Ask the manager to provide a longer deadline, because resource and timeline constraints are the analyst's responsibility to set."),
    ],
    correct_ids=["opt_s16_a"],
    option_feedback={
        "opt_s16_b": (
            "Constraints around resources and timelines should be clarified and agreed during engagement and scoping — "
            "not deferred. Leaving the deadline unaddressed risks delivering too late or misallocating effort."
        ),
        "opt_s16_c": (
            "The engagement and scoping stage should lead to agreement between the analyst and commissioner "
            "about the outputs of the work. The output format is agreed jointly, not decided by the analyst alone."
        ),
        "opt_s16_d": (
            "Resource and timeline constraints are clarified and agreed between the analyst and commissioner — "
            "not set unilaterally by either party. The analyst should discuss whether the deadline is feasible, "
            "not simply reject it."
        ),
    },
    correct_msg=(
        "Correct. Constraints around resources and timelines should be clarified and agreed during scoping. "
        "The engagement and scoping stage should lead to agreement about the outputs of the work — "
        "here, a one-page summary with a bar chart of average delivery time per city, delivered by end of next week."
    ),
    incorrect_msg=(
        "Both the timeline and the output format are things to agree during scoping. "
        "Constraints around resources and timelines should be clarified and agreed; "
        "the scoping stage should lead to agreement about the outputs of the work."
    ),
    hints=[
        "What should happen to resource and timeline constraints during the engagement and scoping stage?",
        "Who agrees on the output format — the analyst alone, or both the analyst and the commissioner?",
    ],
)

# ── s17: table_select — identifying_requirements (hands_on) ──────────────────
# Practice anchor: field_selection. Taught by s13 (f1, f3, f4) and s14 (f2, f5). Tests f1-f5.
# Task 1: select the cell naming the decision (scope) for request_id=3
#   → row where request_id=3, column "decision"
#   → "Decide whether to expand operations in Port Harcourt or reduce them"
# Task 2: select the cell naming the measurable question (output requirement) for request_id=3
#   → row where request_id=3, column "measurable_question"
#   → "Is the average delivery time in Port Harcourt higher than in Lagos and Abuja over the same period?"
# No remediation_step_id for third check/hands-on of same concept (per GENERATOR rule)
s17 = table_select(
    step_id="tile_stakeholder_framing_requirements.s17",
    difficulty="stretch",
    measures=[
        {
            "concept_id": "stakeholder.identifying_requirements",
            "capability": "extract_data_scope_and_output_requirements_from_stakeholder_request",
            "fact_ids": ["f1", "f2", "f3", "f4", "f5"],
        }
    ],
    anchors=[
        "stakeholder.identifying_requirements#practice",
        "stakeholder.identifying_requirements#assessment:extract_data_scope_and_output_requirements_from_stakeholder_request",
    ],
    asset_id="ds_stakeholder_requests",
    variant_id=None,
    columns=["request_id", "request_text", "decision", "measurable_question"],
    intro=(
        "The table below shows stakeholder requests alongside the decision each is meant to inform "
        "and the measurable question the analyst should frame. "
        "Use row 3 to complete both tasks."
    ),
    tasks=[
        {
            "task_id": "task_s17_t1",
            "prompt": (
                "The manager says: \"Look into whether Port Harcourt is a problem.\" "
                "Click the cell that names the specific decision this request is meant to inform — "
                "this is the scope the analyst must capture in the specification document."
            ),
            "target_kind": "cell",
        },
        {
            "task_id": "task_s17_t2",
            "prompt": (
                "Now click the cell that shows the measurable analytical question the analyst should agree "
                "with the commissioner as the output requirement before starting analysis."
            ),
            "target_kind": "cell",
        },
    ],
    answers=[
        {
            "task_id": "task_s17_t1",
            "row": {"where": {"request_id": 3}},
            "column": "decision",
            "expect_value": "Decide whether to expand operations in Port Harcourt or reduce them",
        },
        {
            "task_id": "task_s17_t2",
            "row": {"where": {"request_id": 3}},
            "column": "measurable_question",
            "expect_value": "Is the average delivery time in Port Harcourt higher than in Lagos and Abuja over the same period?",
        },
    ],
    task_feedback={
        "task_s17_t1": {
            "correct": "Correct. The scope of the analysis is the decision it must inform: whether to expand or reduce operations in Port Harcourt.",
            "incorrect": "Look for the cell that names a concrete decision — something the manager would act on — not a restatement of the request.",
        },
        "task_s17_t2": {
            "correct": "Correct. The measurable question names the variable (delivery time), the group (Port Harcourt vs Lagos and Abuja), and the intent (comparison) — this is what the analyst and commissioner should agree as the output requirement.",
            "incorrect": "The output requirement is the measurable analytical question — the one that names a variable, a group, and an intent, and can be answered with data.",
        },
    },
    correct_msg=(
        "Well done. Before starting analysis, the analyst should capture the scope (the decision to inform) "
        "and the output requirement (the measurable question) in a specification document, "
        "and share it with the commissioner for sign-off."
    ),
    incorrect_msg=(
        "The specification document captures two things: the scope (what decision the analysis informs) "
        "and the output requirement (the measurable question the analysis will answer). "
        "Both must be agreed with the commissioner before analysis begins."
    ),
    hints=[
        "The scope is the decision the manager needs to make — what would they do with the result?",
        "The output requirement is the measurable question: it names a variable, a group, and an intent.",
    ],
)

# ── assemble output ───────────────────────────────────────────────────────────
output = {
    "schema_version": "1.0.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_007_da_nocode",
    "tiles": [
        {
            "tile_id": "tile_stakeholder_framing_requirements",
            "interactions": [
                {"step_id": "tile_stakeholder_framing_requirements.s02", "interaction": s02},
                {"step_id": "tile_stakeholder_framing_requirements.s03", "interaction": s03},
                {"step_id": "tile_stakeholder_framing_requirements.s06", "interaction": s06},
                {"step_id": "tile_stakeholder_framing_requirements.s07", "interaction": s07},
                {"step_id": "tile_stakeholder_framing_requirements.s10", "interaction": s10},
                {"step_id": "tile_stakeholder_framing_requirements.s11", "interaction": s11},
                {"step_id": "tile_stakeholder_framing_requirements.s12", "interaction": s12},
                {"step_id": "tile_stakeholder_framing_requirements.s15", "interaction": s15},
                {"step_id": "tile_stakeholder_framing_requirements.s16", "interaction": s16},
                {"step_id": "tile_stakeholder_framing_requirements.s17", "interaction": s17},
            ],
        }
    ],
}

out_path = "batches/final_batch_007_da_nocode/interactions.part.c1.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)
print(f"Written {out_path}")
print(f"Interactions: {len(output['tiles'][0]['interactions'])}")
