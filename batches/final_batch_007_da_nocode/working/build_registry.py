"""Build scenario_asset_registry.json for final_batch_007_da_nocode.

Two tiles in scope:
  tile_data_quality_and_workflow  — concepts: data.data_quality_basics, data.analysis_workflow, data.ethics_privacy_basics
  tile_stakeholder_framing_requirements — concepts: stakeholder.identifying_decision_need, stakeholder.precise_finding_statement,
                                                     stakeholder.framing_analytical_question, stakeholder.identifying_requirements

Glossary vocabulary mined from teaching blocks:
  - delivery-orders table, order_id, delivery_time (minutes), city, driver_id, order_date, customer_phone, customer_name
  - Cities: Lagos, Abuja
  - Negative delivery time (-5 minutes) → validity failure
  - Duplicate order row → uniqueness failure
  - Missing delivery time (NULL) → completeness failure
  - Inaccurate city (Lagos vs Abuja) → accuracy failure
  - Analysis workflow: clarify question, inspect, clean, analyze, visualize, communicate
  - Stakeholder scenario: operations manager, courier partner, delivery times request
  - Precise finding: "average Lagos delivery time rose to 30 minutes this month, up from 22 minutes last month"
  - Vague vs precise: "delivery times went up" → "Lagos delivery times have risen..."
  - Suspensions example: 787,000 in 2022/23 vs 578,300 prior year (gov.uk writing about data)
"""

import json
import sys
from pathlib import Path

OUT = Path("batches/final_batch_007_da_nocode/scenario_asset_registry.json")

registry = {
    "schema_version": "1.0.0",
    "kind": "scenario_asset_registry",
    "path_id": "data_analyst",
    "batch_id": "final_batch_007_da_nocode",
    "scenarios": [
        {
            "scenario_id": "scenario_delivery_ops",
            "name": "Kwik Courier — Delivery Operations",
            "summary": (
                "Kwik Courier is a fictional last-mile delivery company operating in Nigeria. "
                "An operations manager has asked an analyst to investigate delivery times across city routes. "
                "The running example used throughout tile_data_quality_and_workflow and "
                "tile_stakeholder_framing_requirements: the analyst receives a delivery-orders table, "
                "checks its quality, follows the analysis workflow, and then scopes the request with the manager."
            ),
            "locale": "en-NG",
            "currency": "NGN",
            "domain": "logistics / delivery operations",
            "glossary_example_vocab": [
                "delivery-orders table",
                "order_id",
                "order_date",
                "city",
                "delivery_minutes",
                "driver_id",
                "customer_name",
                "customer_phone",
                "Lagos",
                "Abuja",
                "Port Harcourt",
                "completeness",
                "uniqueness",
                "validity",
                "accuracy",
                "negative delivery time (-5 minutes)",
                "duplicate order row",
                "missing delivery time",
                "operations manager",
                "courier partner",
                "analysis workflow",
                "clarify the question",
                "inspect",
                "clean",
                "analyze",
                "visualize",
                "communicate",
                "exploratory data analysis",
                "anomalies",
                "average Lagos delivery time rose to 30 minutes this month, up from 22 minutes last month",
                "specification document",
                "engagement and scoping stage",
                "commissioner",
                "analyst"
            ]
        },
        {
            "scenario_id": "scenario_stakeholder_comms",
            "name": "Kwik Courier — Stakeholder Communication",
            "summary": (
                "The same Kwik Courier context, focused on the stakeholder-communication tile. "
                "The operations manager's vague request ('Can you look into our delivery times?') is used "
                "to teach identifying the decision need, stating findings precisely, framing the analytical "
                "question, and gathering requirements before analysis begins."
            ),
            "locale": "en-NG",
            "currency": "NGN",
            "domain": "stakeholder communication / analytical scoping",
            "glossary_example_vocab": [
                "operations manager",
                "delivery times",
                "decision need",
                "Lagos couriers",
                "renegotiate with courier partner",
                "vague business question",
                "measurable analytical question",
                "variable of interest",
                "group",
                "intent",
                "Is average delivery time in Lagos this month higher than last month?",
                "big idea",
                "complete sentence",
                "unique point of view",
                "what's at stake",
                "Lagos delivery times have risen, so customers on that route are waiting longer",
                "average Lagos delivery time rose to 30 minutes this month, up from 22 minutes last month",
                "787,000 suspensions in the 2022/23 academic year",
                "578,300 suspensions",
                "specification document",
                "sign-off",
                "scope",
                "constraints",
                "data sources",
                "data quality",
                "deadline",
                "output format",
                "bar chart of average delivery time per city"
            ]
        }
    ],
    "assets": []
}

# ─────────────────────────────────────────────────────────────────────────────
# ASSET 1: delivery_orders (clean base)
# Used by: data_quality_basics (visual_anchor data_table, practice_anchor field_selection)
#          analysis_workflow (teaching blocks reference the same table)
#          ethics_privacy_basics (practice: choose columns to keep/drop)
#
# Columns from glossary:
#   order_id (identifier, integer, numeric_looking_label=True — digits used as labels)
#   order_date (datetime, date)
#   city (categorical, string)
#   delivery_minutes (numerical, integer)
#   driver_id (identifier, integer, numeric_looking_label=True)
#   customer_name (pii, string)
#   customer_phone (pii, string)
#
# Rows: 12 clean rows across Lagos, Abuja, Port Harcourt — enough for hidden tests
# to distinguish correct queries from lazy ones (e.g. AVG per city, filter by city).
# ─────────────────────────────────────────────────────────────────────────────

delivery_orders_columns = [
    {
        "name": "order_id",
        "type": "integer",
        "semantic_role": "identifier",
        "description": "Unique order number — a digit used as a label, not a quantity",
        "numeric_looking_label": True
    },
    {
        "name": "order_date",
        "type": "date",
        "semantic_role": "datetime",
        "description": "Date the order was placed (YYYY-MM-DD)"
    },
    {
        "name": "city",
        "type": "string",
        "semantic_role": "categorical",
        "description": "Destination city for the delivery"
    },
    {
        "name": "delivery_minutes",
        "type": "integer",
        "semantic_role": "numerical",
        "unit": "minutes",
        "description": "Time from order dispatch to delivery confirmation, in minutes"
    },
    {
        "name": "driver_id",
        "type": "integer",
        "semantic_role": "identifier",
        "description": "Driver identifier — a digit used as a label, not a quantity",
        "numeric_looking_label": True
    },
    {
        "name": "customer_name",
        "type": "string",
        "semantic_role": "pii",
        "description": "Customer full name — personally identifiable information"
    },
    {
        "name": "customer_phone",
        "type": "string",
        "semantic_role": "pii",
        "description": "Customer phone number including country code — personally identifiable information"
    }
]

# 12 clean rows: 5 Lagos, 4 Abuja, 3 Port Harcourt
# Lagos avg ≈ 30 min (this month), Abuja ≈ 22 min, Port Harcourt ≈ 25 min
# order_id 1001–1012, driver_id 201–205
delivery_orders_rows = [
    # order_id, order_date,    city,            delivery_minutes, driver_id, customer_name,       customer_phone
    [1001, "2024-03-01", "Lagos",         28, 201, "Amara Okafor",    "+2348012345678"],
    [1002, "2024-03-01", "Abuja",         20, 202, "Emeka Nwosu",     "+2348023456789"],
    [1003, "2024-03-02", "Lagos",         32, 201, "Fatima Bello",    "+2348034567890"],
    [1004, "2024-03-02", "Port Harcourt", 25, 203, "Chidi Eze",       "+2348045678901"],
    [1005, "2024-03-03", "Abuja",         22, 202, "Ngozi Adeyemi",   "+2348056789012"],
    [1006, "2024-03-03", "Lagos",         30, 204, "Tunde Afolabi",   "+2348067890123"],
    [1007, "2024-03-04", "Port Harcourt", 24, 203, "Kemi Obi",        "+2348078901234"],
    [1008, "2024-03-04", "Abuja",         21, 205, "Yusuf Musa",      "+2348089012345"],
    [1009, "2024-03-05", "Lagos",         31, 204, "Adaeze Igwe",     "+2348090123456"],
    [1010, "2024-03-05", "Port Harcourt", 26, 203, "Seun Lawal",      "+2348001234567"],
    [1011, "2024-03-06", "Abuja",         23, 205, "Halima Sule",     "+2348012345679"],
    [1012, "2024-03-06", "Lagos",         29, 201, "Bola Martins",    "+2348023456780"],
]

# ─────────────────────────────────────────────────────────────────────────────
# VARIANT 1: delivery_orders_messy
# Plants three issues matching the glossary's exact examples:
#   issue_dq_001  missing_value   — order 1009: delivery_minutes = NULL (completeness failure)
#   issue_dq_002  duplicate_row   — order 1003 duplicated (uniqueness failure)
#   issue_dq_003  impossible_value — order 1006: delivery_minutes = -5 (validity failure)
#
# Op sequence:
#   1. set_cell order_id=1009, delivery_minutes → null   (completeness)
#   2. set_cell order_id=1006, delivery_minutes → -5     (validity)
#   3. duplicate_row order_id=1003                       (uniqueness)
#
# After ops the variant rows (in order) are:
#   1001 Lagos 28, 1002 Abuja 20, 1003 Lagos 32, 1003 Lagos 32 (dup), 1004 PH 25,
#   1005 Abuja 22, 1006 Lagos -5, 1007 PH 24, 1008 Abuja 21,
#   1009 Lagos null, 1010 PH 26, 1011 Abuja 23, 1012 Lagos 29
#
# Planted issue locations use `where` on order_id (unique in base; after dup, order 1003
# appears twice — occurrence=0 and occurrence=1 both point to the duplicate pair).
# ─────────────────────────────────────────────────────────────────────────────

delivery_orders_asset = {
    "asset_id": "ds_delivery_orders",
    "asset_kind": "dataset",
    "scenario_id": "scenario_delivery_ops",
    "title": "Kwik Courier — Delivery Orders",
    "description": (
        "One week of delivery orders for Kwik Courier across Lagos, Abuja and Port Harcourt. "
        "Used throughout tile_data_quality_and_workflow and tile_stakeholder_framing_requirements. "
        "The clean base has 12 rows; the 'messy' variant plants three quality issues "
        "(missing value, duplicate row, impossible value) matching the glossary's teaching examples."
    ),
    "columns": delivery_orders_columns,
    "rows": delivery_orders_rows,
    "variants": [
        {
            "variant_id": "ds_delivery_orders_messy",
            "derived_from": "ds_delivery_orders",
            "purpose": (
                "Messy version for data-quality practice: contains a missing delivery time "
                "(completeness), a duplicate order row (uniqueness), and a negative delivery time "
                "(validity). Used in the field_selection practice anchor and the data_table visual anchor."
            ),
            "ops": [
                # Op 1: set delivery_minutes to null for order 1009 → completeness failure
                {
                    "op": "set_cell",
                    "where": {"order_id": 1009},
                    "occurrence": 0,
                    "column": "delivery_minutes",
                    "value": None
                },
                # Op 2: set delivery_minutes to -5 for order 1006 → validity failure
                {
                    "op": "set_cell",
                    "where": {"order_id": 1006},
                    "occurrence": 0,
                    "column": "delivery_minutes",
                    "value": -5
                },
                # Op 3: duplicate order 1003 → uniqueness failure
                {
                    "op": "duplicate_row",
                    "where": {"order_id": 1003},
                    "occurrence": 0
                }
            ],
            "planted_issues": [
                {
                    "issue_id": "issue_dq_001",
                    "kind": "missing_value",
                    "locations": [
                        {
                            "where": {"order_id": 1009},
                            "occurrence": 0,
                            "column": "delivery_minutes"
                        }
                    ],
                    "description": (
                        "Order 1009 has no delivery time recorded — the cell is null. "
                        "This is a completeness failure: a value that should be present is missing."
                    ),
                    "rule": {
                        "column": "delivery_minutes",
                        "op": "is_null"
                    }
                },
                {
                    "issue_id": "issue_dq_002",
                    "kind": "duplicate_row",
                    "locations": [
                        {
                            "where": {"order_id": 1003},
                            "occurrence": 0,
                            "column": "order_id"
                        },
                        {
                            "where": {"order_id": 1003},
                            "occurrence": 1,
                            "column": "order_id"
                        }
                    ],
                    "description": (
                        "Order 1003 appears as two identical rows. "
                        "This is a uniqueness failure: one entity (one order) should appear as one row."
                    )
                },
                {
                    "issue_id": "issue_dq_003",
                    "kind": "impossible_value",
                    "locations": [
                        {
                            "where": {"order_id": 1006},
                            "occurrence": 0,
                            "column": "delivery_minutes"
                        }
                    ],
                    "description": (
                        "Order 1006 has delivery_minutes = -5. "
                        "A negative delivery time is not a valid delivery time — this is a validity failure."
                    ),
                    "rule": {
                        "column": "delivery_minutes",
                        "op": "lt",
                        "value": 0
                    }
                }
            ]
        }
    ],
    "provenance": "authored"
}

registry["assets"].append(delivery_orders_asset)

# ─────────────────────────────────────────────────────────────────────────────
# ASSET 2: stakeholder_requests
# Used by: stakeholder.identifying_decision_need (practice: given a vague request, name the decision)
#          stakeholder.framing_analytical_question (practice: rewrite as measurable question)
#          stakeholder.identifying_requirements (practice: list four requirement categories)
#
# This is a small lookup table of stakeholder requests and their analytical metadata.
# Columns:
#   request_id   (identifier, integer, numeric_looking_label=True)
#   request_text (text, string)   — the vague stakeholder request
#   decision     (text, string)   — the underlying business decision
#   vague_question (text, string) — the question as first stated
#   measurable_question (text, string) — the rewritten well-formed question
#   variable_of_interest (categorical, string)
#   group_or_period (categorical, string)
#   intent (categorical, string)  — "comparison" | "description" | "association"
#
# 6 rows — enough for hidden tests to distinguish correct answers from lucky guesses.
# ─────────────────────────────────────────────────────────────────────────────

stakeholder_requests_columns = [
    {
        "name": "request_id",
        "type": "integer",
        "semantic_role": "identifier",
        "description": "Row identifier — a digit used as a label, not a quantity",
        "numeric_looking_label": True
    },
    {
        "name": "request_text",
        "type": "string",
        "semantic_role": "text",
        "description": "The vague stakeholder request as originally stated"
    },
    {
        "name": "decision",
        "type": "string",
        "semantic_role": "text",
        "description": "The underlying business decision the analysis is meant to inform"
    },
    {
        "name": "vague_question",
        "type": "string",
        "semantic_role": "text",
        "description": "The question as first stated — vague, not yet measurable"
    },
    {
        "name": "measurable_question",
        "type": "string",
        "semantic_role": "text",
        "description": "The rewritten well-formed statistical question naming variable, group, and intent"
    },
    {
        "name": "variable_of_interest",
        "type": "string",
        "semantic_role": "categorical",
        "description": "The measurable variable the question focuses on"
    },
    {
        "name": "group_or_period",
        "type": "string",
        "semantic_role": "categorical",
        "description": "The group or time period the question focuses on"
    },
    {
        "name": "intent",
        "type": "string",
        "semantic_role": "categorical",
        "description": "The statistical intent: comparison, description, or association"
    }
]

stakeholder_requests_rows = [
    # request_id, request_text, decision, vague_question, measurable_question, variable_of_interest, group_or_period, intent
    [
        1,
        "Can you look into our delivery times?",
        "Decide whether to add more couriers on the Lagos route",
        "Are our delivery times okay?",
        "Is the average delivery time in Lagos this month higher than last month?",
        "delivery time",
        "Lagos, this month vs last month",
        "comparison"
    ],
    [
        2,
        "Can you check how our drivers are doing?",
        "Decide whether to renegotiate the contract with the courier partner",
        "Are our drivers performing well?",
        "Is the average delivery time per driver in March 2024 above the 30-minute target?",
        "delivery time per driver",
        "all drivers, March 2024",
        "description"
    ],
    [
        3,
        "Look into whether Port Harcourt is a problem.",
        "Decide whether to expand operations in Port Harcourt or reduce them",
        "Is Port Harcourt a problem?",
        "Is the average delivery time in Port Harcourt higher than in Lagos and Abuja over the same period?",
        "delivery time",
        "Port Harcourt vs Lagos and Abuja, March 2024",
        "comparison"
    ],
    [
        4,
        "Find out if late deliveries are related to the time of day.",
        "Decide whether to adjust dispatch scheduling to reduce late deliveries",
        "Do late deliveries happen at certain times?",
        "Is there an association between dispatch hour and delivery time across all orders in March 2024?",
        "delivery time",
        "all orders, March 2024",
        "association"
    ],
    [
        5,
        "Tell me about our order volumes.",
        "Decide whether to hire additional operations staff for peak days",
        "How many orders do we get?",
        "What is the average number of orders per day in Lagos during March 2024?",
        "order count per day",
        "Lagos, March 2024",
        "description"
    ],
    [
        6,
        "Are customers happy with us?",
        "Decide whether to invest in a customer-satisfaction improvement programme",
        "Are customers satisfied?",
        "What proportion of orders in March 2024 were delivered within the 30-minute target across all cities?",
        "proportion of on-time deliveries",
        "all cities, March 2024",
        "description"
    ]
]

stakeholder_requests_asset = {
    "asset_id": "ds_stakeholder_requests",
    "asset_kind": "dataset",
    "scenario_id": "scenario_stakeholder_comms",
    "title": "Kwik Courier — Stakeholder Requests and Analytical Questions",
    "description": (
        "A lookup table of six vague stakeholder requests paired with their underlying decision, "
        "a rewritten measurable analytical question, and the question's components (variable, group, intent). "
        "Used in tile_stakeholder_framing_requirements for practice anchors on identifying decision need, "
        "framing the analytical question, and identifying requirements."
    ),
    "columns": stakeholder_requests_columns,
    "rows": stakeholder_requests_rows,
    "provenance": "authored"
}

registry["assets"].append(stakeholder_requests_asset)

# ─────────────────────────────────────────────────────────────────────────────
# ASSET 3: finding_statements
# Used by: stakeholder.precise_finding_statement (before_after visual anchor, external_proof practice)
#
# Columns:
#   finding_id   (identifier, integer, numeric_looking_label=True)
#   vague_finding (text, string)   — the imprecise version
#   precise_finding (text, string) — the rewritten version with number + comparison
#   has_specific_number (boolean)  — True if the precise version names a number
#   has_comparison (boolean)       — True if the precise version includes a comparison
#   is_complete_sentence (boolean) — True if the precise version is a complete sentence
#
# 5 rows — enough for hidden tests.
# The first row matches the glossary's exact example:
#   vague: "delivery times went up"
#   precise: "the average Lagos delivery time rose to 30 minutes this month, up from 22 minutes last month"
# ─────────────────────────────────────────────────────────────────────────────

finding_statements_columns = [
    {
        "name": "finding_id",
        "type": "integer",
        "semantic_role": "identifier",
        "description": "Row identifier — a digit used as a label, not a quantity",
        "numeric_looking_label": True
    },
    {
        "name": "vague_finding",
        "type": "string",
        "semantic_role": "text",
        "description": "The imprecise finding statement — lacks a specific number or comparison"
    },
    {
        "name": "precise_finding",
        "type": "string",
        "semantic_role": "text",
        "description": "The rewritten precise finding — names a specific number and includes a comparison"
    },
    {
        "name": "has_specific_number",
        "type": "boolean",
        "semantic_role": "categorical",
        "description": "True if the precise finding names at least one specific number"
    },
    {
        "name": "has_comparison",
        "type": "boolean",
        "semantic_role": "categorical",
        "description": "True if the precise finding includes a comparison to a prior period or group"
    },
    {
        "name": "is_complete_sentence",
        "type": "boolean",
        "semantic_role": "categorical",
        "description": "True if the precise finding is a complete sentence with a subject and verb"
    }
]

finding_statements_rows = [
    # finding_id, vague_finding, precise_finding, has_specific_number, has_comparison, is_complete_sentence
    [
        1,
        "Delivery times went up.",
        "The average Lagos delivery time rose to 30 minutes this month, up from 22 minutes last month.",
        True, True, True
    ],
    [
        2,
        "Sales went up.",
        "Total sales in March 2024 reached 1,240 orders, an increase of 18% compared with February 2024.",
        True, True, True
    ],
    [
        3,
        "Port Harcourt is slow.",
        "The average delivery time in Port Harcourt was 25 minutes in March 2024, compared with 30 minutes in Lagos over the same period.",
        True, True, True
    ],
    [
        4,
        "Driver 201 is our best driver.",
        "Driver 201 completed all 3 assigned orders in March 2024 with an average delivery time of 29 minutes, the lowest among the five active drivers.",
        True, True, True
    ],
    [
        5,
        "Most orders are on time.",
        "83% of orders in March 2024 were delivered within the 30-minute target, up from 71% in February 2024.",
        True, True, True
    ]
]

finding_statements_asset = {
    "asset_id": "ds_finding_statements",
    "asset_kind": "dataset",
    "scenario_id": "scenario_stakeholder_comms",
    "title": "Kwik Courier — Vague vs Precise Finding Statements",
    "description": (
        "Five pairs of vague and precise finding statements drawn from the Kwik Courier scenario. "
        "The first row matches the glossary's exact teaching example. "
        "Used in tile_stakeholder_framing_requirements for the before_after visual anchor "
        "and the external_proof practice anchor on stating findings precisely."
    ),
    "columns": finding_statements_columns,
    "rows": finding_statements_rows,
    "provenance": "authored"
}

registry["assets"].append(finding_statements_asset)

# ─────────────────────────────────────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────────────────────────────────────

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n")
print(f"Written: {OUT}")
print(f"  scenarios: {len(registry['scenarios'])}")
print(f"  assets:    {len(registry['assets'])}")
for a in registry["assets"]:
    ncols = len(a["columns"])
    nrows = len(a.get("rows", []))
    nvars = len(a.get("variants", []))
    print(f"    {a['asset_id']}: {ncols} cols, {nrows} rows, {nvars} variants")
