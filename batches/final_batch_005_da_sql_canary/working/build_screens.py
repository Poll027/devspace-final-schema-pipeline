"""Build screens.json for final_batch_005_da_sql_canary."""
import json

# ── helpers ──────────────────────────────────────────────────────────────────

def qid(concept_id, local):
    """Return a qualified id like sql.relational_model#f1."""
    return f"{concept_id}#{local}"

# ── TILE 1: tile_sql_fund_relational_select ───────────────────────────────────

TILE1_ID = "tile_sql_fund_relational_select"
C_REL  = "sql.relational_model"
C_SEL  = "sql.select_fundamentals"

tile1_steps = [

    # ── s01: explainer – relational model intro + data_table visual ──────────
    {
        "step_id": f"{TILE1_ID}.s01",
        "type": "explainer",
        "concept_ids": [C_REL],
        "eyebrow": "Relational Model",
        "title": "Tables, rows and columns",
        "lede": "Greenleaf Online Shop keeps its data in a relational database — a set of named tables, each holding one kind of thing.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE1_ID}.s01.b01",
                "role": "intro",
                "text": (
                    "Greenleaf Online Shop stores its data in a relational database. "
                    "Instead of one big spreadsheet, the data lives in separate tables — "
                    "a customers table, an orders table — each holding its own kind of data. "
                    "A database is composed of multiple tables like this, each holding data."
                ),
                "lineage": {
                    "concept_ids": [C_REL],
                    "teaching_block_ids": [qid(C_REL, "tb1")],
                    "fact_ids": [qid(C_REL, "f4")]
                }
            },
            {
                "type": "prose",
                "block_id": f"{TILE1_ID}.s01.b02",
                "role": "definition",
                "text": (
                    "A relation — what SQL calls a table — holds data where each row "
                    "(also called a record or tuple) represents one group of related data values. "
                    "The columns are also called fields or attributes. "
                    "In the customers table, each row is one customer; "
                    "customer_id, name and city are its attributes."
                ),
                "lineage": {
                    "concept_ids": [C_REL],
                    "teaching_block_ids": [qid(C_REL, "tb2")],
                    "fact_ids": [qid(C_REL, "f1"), qid(C_REL, "f2")]
                }
            },
            {
                "type": "data_table",
                "block_id": f"{TILE1_ID}.s01.b03",
                "asset_ref": {
                    "asset_id": "ds_customers",
                    "variant_id": None,
                    "columns": ["customer_id", "name", "city"],
                    "max_rows": 4
                },
                "caption": "customers table — each row is one record/tuple; customer_id, name and city are fields/attributes.",
                "tag_columns": [
                    {"column": "customer_id", "tag": "field / attribute", "tone": "focus"},
                    {"column": "name",        "tag": "field / attribute", "tone": "focus"},
                    {"column": "city",        "tag": "field / attribute", "tone": "focus"}
                ],
                "highlight": [
                    {
                        "target": {"kind": "row", "row": {"where": {"customer_id": 1}}},
                        "label": "row / record / tuple",
                        "tone": "focus"
                    }
                ],
                "lineage": {
                    "concept_ids": [C_REL],
                    "teaching_block_ids": [qid(C_REL, "tb2")],
                    "fact_ids": [qid(C_REL, "f1"), qid(C_REL, "f2"), qid(C_REL, "f4")],
                    "anchors": [qid(C_REL, "visual")]
                }
            }
        ],
        "reward": {"gems": 2},
        "lineage": {
            "concept_ids": [C_REL],
            "teaching_block_ids": [qid(C_REL, "tb1"), qid(C_REL, "tb2")],
            "fact_ids": [qid(C_REL, "f1"), qid(C_REL, "f2"), qid(C_REL, "f4")],
            "anchors": [qid(C_REL, "visual")]
        }
    },

    # ── s02: explainer – table properties ────────────────────────────────────
    {
        "step_id": f"{TILE1_ID}.s02",
        "type": "explainer",
        "concept_ids": [C_REL],
        "eyebrow": "Relational Model",
        "title": "What makes a table well-formed",
        "lede": "A well-formed table has a unique name, no duplicate rows, and covers exactly one kind of thing.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE1_ID}.s02.b01",
                "role": "definition",
                "text": (
                    "A table has a name distinct from every other table in the database — "
                    "'customers' is not reused for anything else. "
                    "It contains no duplicate rows, and the order its rows and columns "
                    "happen to be listed in is not meaningful."
                ),
                "lineage": {
                    "concept_ids": [C_REL],
                    "teaching_block_ids": [qid(C_REL, "tb3")],
                    "fact_ids": [qid(C_REL, "f3")]
                }
            },
            {
                "type": "prose",
                "block_id": f"{TILE1_ID}.s02.b02",
                "role": "practical_context",
                "text": (
                    "Each table should contain information about one kind of thing only — "
                    "the Customer or the Order — rather than mixing unrelated things together. "
                    "That is why Greenleaf keeps customer details and order details in two "
                    "separate tables instead of one merged one."
                ),
                "lineage": {
                    "concept_ids": [C_REL],
                    "teaching_block_ids": [qid(C_REL, "tb3")],
                    "fact_ids": [qid(C_REL, "f5")]
                }
            }
        ],
        "reward": {"gems": 2},
        "lineage": {
            "concept_ids": [C_REL],
            "teaching_block_ids": [qid(C_REL, "tb3")],
            "fact_ids": [qid(C_REL, "f3"), qid(C_REL, "f5")]
        }
    },

    # ── s03: check – judge table design (framing only; interaction in stage 04) ─
    {
        "step_id": f"{TILE1_ID}.s03",
        "type": "check",
        "concept_ids": [C_REL],
        "eyebrow": "Quick check",
        "title": "Is this table well-formed?",
        "lede": "Apply the three properties of a well-formed table to a short scenario.",
        "reward": {"gems": 3, "first_try_bonus": 1},
        "lineage": {
            "concept_ids": [C_REL],
            "teaching_block_ids": [],
            "fact_ids": [qid(C_REL, "f3"), qid(C_REL, "f5")],
            "anchors": [qid(C_REL, "assessment:judge_whether_a_table_design_is_well_formed")]
        }
    },

    # ── s04: hands_on – identify rows/columns (framing only) ─────────────────
    {
        "step_id": f"{TILE1_ID}.s04",
        "type": "hands_on",
        "concept_ids": [C_REL],
        "eyebrow": "Hands-on",
        "title": "Find the rows and columns",
        "lede": "Select the parts of the orders table that match the description.",
        "reward": {"gems": 4, "first_try_bonus": 2},
        "lineage": {
            "concept_ids": [C_REL],
            "teaching_block_ids": [],
            "fact_ids": [qid(C_REL, "f1"), qid(C_REL, "f2"), qid(C_REL, "f4")],
            "anchors": [
                qid(C_REL, "practice"),
                qid(C_REL, "assessment:identify_table_rows_columns_in_scenario")
            ]
        }
    },

    # ── s05: explainer – SELECT … FROM + code_walkthrough visual ─────────────
    {
        "step_id": f"{TILE1_ID}.s05",
        "type": "explainer",
        "concept_ids": [C_SEL],
        "eyebrow": "SELECT Basics",
        "title": "SELECT and FROM: pulling columns out of a table",
        "lede": "A SELECT statement names the columns you want and the table to read them from.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE1_ID}.s05.b01",
                "role": "intro",
                "text": (
                    "The customers table has columns customer_id, name and city. "
                    "To pull that data out of the database you write a SELECT statement. "
                    "The SELECT list — everything between SELECT and FROM — specifies the "
                    "expressions that form the output rows, and the FROM clause names the "
                    "table the query reads from."
                ),
                "lineage": {
                    "concept_ids": [C_SEL],
                    "teaching_block_ids": [qid(C_SEL, "tb1"), qid(C_SEL, "tb2")],
                    "fact_ids": [qid(C_SEL, "f1"), qid(C_SEL, "f3")]
                }
            },
            {
                "type": "prose",
                "block_id": f"{TILE1_ID}.s05.b02",
                "role": "syntax",
                "text": (
                    "You can rename an output column by writing AS output_name after its "
                    "expression in the SELECT list — AS can be left out if the name you "
                    "want does not collide with a keyword. "
                    "SELECT name AS customer_name, city FROM customers returns the same "
                    "data, but the first column is labelled customer_name in the result."
                ),
                "lineage": {
                    "concept_ids": [C_SEL],
                    "teaching_block_ids": [qid(C_SEL, "tb3")],
                    "fact_ids": [qid(C_SEL, "f2")]
                }
            },
            {
                "type": "code_walkthrough",
                "block_id": f"{TILE1_ID}.s05.b03",
                "language": "sql",
                "code": (
                    "SELECT name AS customer_name,\n"
                    "       city\n"
                    "FROM   customers;"
                ),
                "annotations": [
                    {
                        "start_line": 1,
                        "end_line": 2,
                        "text": "SELECT list: the expressions that form the output rows — name is renamed to customer_name, city keeps its name."
                    },
                    {
                        "start_line": 3,
                        "end_line": 3,
                        "text": "FROM clause: derives the table the query reads from — here the customers table."
                    }
                ],
                "reveal": "line_by_line",
                "lineage": {
                    "concept_ids": [C_SEL],
                    "teaching_block_ids": [qid(C_SEL, "tb2"), qid(C_SEL, "tb3")],
                    "fact_ids": [qid(C_SEL, "f1"), qid(C_SEL, "f2"), qid(C_SEL, "f3")],
                    "anchors": [qid(C_SEL, "visual")]
                }
            }
        ],
        "reward": {"gems": 2},
        "lineage": {
            "concept_ids": [C_SEL],
            "teaching_block_ids": [qid(C_SEL, "tb1"), qid(C_SEL, "tb2"), qid(C_SEL, "tb3")],
            "fact_ids": [qid(C_SEL, "f1"), qid(C_SEL, "f2"), qid(C_SEL, "f3")],
            "anchors": [qid(C_SEL, "visual")]
        }
    },

    # ── s06: video – media_group ──────────────────────────────────────────────
    {
        "step_id": f"{TILE1_ID}.s06",
        "type": "video",
        "concept_ids": [C_SEL],
        "eyebrow": "Watch",
        "title": "SELECT and FROM picking just the columns you need",
        "lede": "See a SELECT statement run against the customers table and watch the output columns appear.",
        "blocks": [
            {
                "type": "media_group",
                "block_id": f"{TILE1_ID}.s06.b01",
                "group_title": "SELECT and FROM picking just the columns you need",
                "segment_ids": [
                    "seg_sql.select_fundamentals_082lfHzdTe8_326_444"
                ],
                "default_mode": "video"
            }
        ],
        "reward": {"gems": 1},
        "lineage": {
            "concept_ids": [C_SEL],
            "teaching_block_ids": [],
            "fact_ids": [qid(C_SEL, "f1"), qid(C_SEL, "f3")],
            "segment_ids": ["seg_sql.select_fundamentals_082lfHzdTe8_326_444"]
        }
    },

    # ── s07: explainer – SELECT * ─────────────────────────────────────────────
    {
        "step_id": f"{TILE1_ID}.s07",
        "type": "explainer",
        "concept_ids": [C_SEL],
        "eyebrow": "SELECT Basics",
        "title": "SELECT * — all columns at once",
        "lede": "Writing * in the SELECT list is shorthand for every column of the selected rows.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE1_ID}.s07.b01",
                "role": "example",
                "text": (
                    "Writing * in the SELECT list is shorthand for all columns of the "
                    "selected rows — SELECT * FROM customers returns every column of every "
                    "customer row without listing them one by one. "
                    "When a query reads from more than one table, table_name.* narrows "
                    "that to just one table's columns."
                ),
                "lineage": {
                    "concept_ids": [C_SEL],
                    "teaching_block_ids": [qid(C_SEL, "tb4")],
                    "fact_ids": [qid(C_SEL, "f4")]
                }
            }
        ],
        "reward": {"gems": 1},
        "lineage": {
            "concept_ids": [C_SEL],
            "teaching_block_ids": [qid(C_SEL, "tb4")],
            "fact_ids": [qid(C_SEL, "f4")]
        }
    },

    # ── s08: check – write SELECT for listed columns (framing only) ──────────
    {
        "step_id": f"{TILE1_ID}.s08",
        "type": "check",
        "concept_ids": [C_SEL],
        "eyebrow": "Quick check",
        "title": "Which query returns the right columns?",
        "lede": "Choose the SELECT statement that returns exactly the columns described.",
        "reward": {"gems": 3, "first_try_bonus": 1},
        "lineage": {
            "concept_ids": [C_SEL],
            "teaching_block_ids": [],
            "fact_ids": [qid(C_SEL, "f1"), qid(C_SEL, "f3")],
            "anchors": [qid(C_SEL, "assessment:write_select_for_listed_columns")]
        }
    },

    # ── s09: hands_on – rename with AS (framing only) ────────────────────────
    {
        "step_id": f"{TILE1_ID}.s09",
        "type": "hands_on",
        "concept_ids": [C_SEL],
        "eyebrow": "Hands-on",
        "title": "Rename a column with AS",
        "lede": "Write a SELECT statement that returns three columns from customers, renaming at least one with AS.",
        "reward": {"gems": 4, "first_try_bonus": 2},
        "lineage": {
            "concept_ids": [C_SEL],
            "teaching_block_ids": [],
            "fact_ids": [qid(C_SEL, "f2")],
            "anchors": [
                qid(C_SEL, "practice"),
                qid(C_SEL, "assessment:rename_output_column_with_as")
            ]
        }
    },

    # ── s10: recap ────────────────────────────────────────────────────────────
    {
        "step_id": f"{TILE1_ID}.s10",
        "type": "recap",
        "concept_ids": [C_REL, C_SEL],
        "eyebrow": "Recap",
        "title": "What you've learned",
        "lede": "Tables, rows, columns — and the SELECT statement that reads them.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE1_ID}.s10.b01",
                "role": "takeaway",
                "text": (
                    "A relational database stores data in named tables. "
                    "Each row represents one group of related values; "
                    "each table covers one kind of thing only. "
                    "SELECT … FROM is the shape every query builds on: "
                    "FROM names the table to read, and the SELECT list names the columns — "
                    "renamed or not — that come back out."
                ),
                "lineage": {
                    "concept_ids": [C_REL, C_SEL],
                    "teaching_block_ids": [qid(C_REL, "tb4"), qid(C_SEL, "tb5")],
                    "fact_ids": [
                        qid(C_REL, "f1"), qid(C_REL, "f5"),
                        qid(C_SEL, "f1"), qid(C_SEL, "f3")
                    ]
                }
            },
            {
                "type": "up_next",
                "block_id": f"{TILE1_ID}.s10.b02",
                "title": "Up next: Aliasing and DISTINCT",
                "text": (
                    "In the next tile you will give tables short temporary names with AS "
                    "and use DISTINCT to list each unique city in the customers table exactly once."
                )
            }
        ],
        "reward": {"gems": 2},
        "lineage": {
            "concept_ids": [C_REL, C_SEL],
            "teaching_block_ids": [qid(C_REL, "tb4"), qid(C_SEL, "tb5")],
            "fact_ids": [
                qid(C_REL, "f1"), qid(C_REL, "f5"),
                qid(C_SEL, "f1"), qid(C_SEL, "f3")
            ]
        }
    }
]

# ── Remediation steps for tile 1 ─────────────────────────────────────────────
# Rule: one remediation step for the first check/hands-on of each concept.
# Concept 1 (sql.relational_model): first check = s03
# Concept 2 (sql.select_fundamentals): first check = s08

tile1_remediation = [
    {
        "step_id": f"{TILE1_ID}.r01",
        "type": "remediation",
        "concept_ids": [C_REL],
        "eyebrow": "Let's revisit",
        "title": "Well-formed vs. poorly-formed tables — a contrast",
        "lede": "Compare two designs for the same data to see which properties matter.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE1_ID}.r01.b01",
                "role": "misconception",
                "text": (
                    "A poorly-formed table might mix customer details and order details "
                    "in the same rows, or repeat the same customer row twice. "
                    "A well-formed table has a unique name, no duplicate rows, and "
                    "covers exactly one kind of thing — so customers and orders each "
                    "get their own table in Greenleaf's database."
                ),
                "lineage": {
                    "concept_ids": [C_REL],
                    "teaching_block_ids": [qid(C_REL, "tb3")],
                    "fact_ids": [qid(C_REL, "f3"), qid(C_REL, "f5")]
                }
            }
        ],
        "lineage": {
            "concept_ids": [C_REL],
            "teaching_block_ids": [qid(C_REL, "tb3")],
            "fact_ids": [qid(C_REL, "f3"), qid(C_REL, "f5")]
        }
    },
    {
        "step_id": f"{TILE1_ID}.r02",
        "type": "remediation",
        "concept_ids": [C_SEL],
        "eyebrow": "Let's revisit",
        "title": "SELECT list vs. FROM clause — what each part does",
        "lede": "A quick contrast between the two required parts of every SELECT statement.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE1_ID}.r02.b01",
                "role": "misconception",
                "text": (
                    "The FROM clause names the table to read — it does not choose columns. "
                    "The SELECT list names the columns (or expressions) that appear in the "
                    "output — it does not name the table. "
                    "SELECT name, city FROM customers: the SELECT list picks two columns; "
                    "FROM customers supplies all the rows."
                ),
                "lineage": {
                    "concept_ids": [C_SEL],
                    "teaching_block_ids": [qid(C_SEL, "tb2")],
                    "fact_ids": [qid(C_SEL, "f1"), qid(C_SEL, "f3")]
                }
            }
        ],
        "lineage": {
            "concept_ids": [C_SEL],
            "teaching_block_ids": [qid(C_SEL, "tb2")],
            "fact_ids": [qid(C_SEL, "f1"), qid(C_SEL, "f3")]
        }
    }
]

# ── TILE 2: tile_sql_fund_alias_distinct ──────────────────────────────────────

TILE2_ID = "tile_sql_fund_alias_distinct"
C_ALIAS  = "sql.aliasing"
C_DIST   = "sql.distinct"

tile2_steps = [

    # ── s01: explainer – aliasing intro + code_walkthrough visual ────────────
    {
        "step_id": f"{TILE2_ID}.s01",
        "type": "explainer",
        "concept_ids": [C_ALIAS],
        "eyebrow": "Aliasing",
        "title": "Giving tables a short temporary name",
        "lede": "SQL lets you give a table a short alias for the current query so you don't have to type its full name every time.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE2_ID}.s01.b01",
                "role": "intro",
                "text": (
                    "Typing orders or customers in full every time gets tedious, "
                    "especially once a query refers to a table's columns repeatedly. "
                    "SQL lets you give a table a short temporary name for the query instead."
                ),
                "lineage": {
                    "concept_ids": [C_ALIAS],
                    "teaching_block_ids": [qid(C_ALIAS, "tb1")],
                    "fact_ids": [qid(C_ALIAS, "f1")]
                }
            },
            {
                "type": "prose",
                "block_id": f"{TILE2_ID}.s01.b02",
                "role": "definition",
                "text": (
                    "A table alias is a temporary name given to a table reference, "
                    "written FROM table_reference AS alias — AS is optional. "
                    "FROM orders AS o gives the orders table the short name o for the "
                    "rest of that query. Once assigned, the table must be referred to "
                    "by its alias, not its original name — writing FROM orders AS o "
                    "and then referencing orders again later would be an error."
                ),
                "lineage": {
                    "concept_ids": [C_ALIAS],
                    "teaching_block_ids": [qid(C_ALIAS, "tb2")],
                    "fact_ids": [qid(C_ALIAS, "f1"), qid(C_ALIAS, "f2")]
                }
            },
            {
                "type": "code_walkthrough",
                "block_id": f"{TILE2_ID}.s01.b03",
                "language": "sql",
                "code": (
                    "SELECT o.order_id,\n"
                    "       o.delivery_time_minutes AS delivery_min\n"
                    "FROM   orders AS o;"
                ),
                "annotations": [
                    {
                        "start_line": 1,
                        "end_line": 2,
                        "text": "o. qualifies each column with the alias — o is the alias for orders defined in FROM."
                    },
                    {
                        "start_line": 2,
                        "end_line": 2,
                        "text": "AS delivery_min renames the output column — same AS syntax as column aliasing."
                    },
                    {
                        "start_line": 3,
                        "end_line": 3,
                        "text": "FROM orders AS o — assigns the alias o to the orders table for this query."
                    }
                ],
                "reveal": "line_by_line",
                "lineage": {
                    "concept_ids": [C_ALIAS],
                    "teaching_block_ids": [qid(C_ALIAS, "tb2")],
                    "fact_ids": [qid(C_ALIAS, "f1"), qid(C_ALIAS, "f2")],
                    "anchors": [qid(C_ALIAS, "visual")]
                }
            }
        ],
        "reward": {"gems": 2},
        "lineage": {
            "concept_ids": [C_ALIAS],
            "teaching_block_ids": [qid(C_ALIAS, "tb1"), qid(C_ALIAS, "tb2")],
            "fact_ids": [qid(C_ALIAS, "f1"), qid(C_ALIAS, "f2")],
            "anchors": [qid(C_ALIAS, "visual")]
        }
    },

    # ── s02: explainer – column aliasing + qualification ─────────────────────
    {
        "step_id": f"{TILE2_ID}.s02",
        "type": "explainer",
        "concept_ids": [C_ALIAS],
        "eyebrow": "Aliasing",
        "title": "Column aliases and qualified column references",
        "lede": "Columns can be renamed in the SELECT list, and referenced with a table alias prefix to avoid ambiguity.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE2_ID}.s02.b01",
                "role": "syntax",
                "text": (
                    "A column can be aliased by writing AS output_name after its expression "
                    "in the SELECT list, exactly as you already saw with SELECT. "
                    "A column can also be referenced as correlation.columnname, where "
                    "correlation is a table name or an alias defined in the FROM clause — "
                    "so with orders aliased to o, you can write o.customer_id instead of "
                    "orders.customer_id. The correlation name and dot can be left off "
                    "entirely when the column name is unique across every table in the query."
                ),
                "lineage": {
                    "concept_ids": [C_ALIAS],
                    "teaching_block_ids": [qid(C_ALIAS, "tb3")],
                    "fact_ids": [qid(C_ALIAS, "f3"), qid(C_ALIAS, "f4")]
                }
            },
            {
                "type": "prose",
                "block_id": f"{TILE2_ID}.s02.b02",
                "role": "practical_context",
                "text": (
                    "On a single table like SELECT o.order_id FROM orders AS o, "
                    "qualifying a column is optional — the alias starts to matter once "
                    "a query reads from more than one table and two of those tables share "
                    "a column name. Qualifying which table's copy you mean is what keeps "
                    "the query unambiguous."
                ),
                "lineage": {
                    "concept_ids": [C_ALIAS],
                    "teaching_block_ids": [qid(C_ALIAS, "tb4")],
                    "fact_ids": [qid(C_ALIAS, "f4")]
                }
            }
        ],
        "reward": {"gems": 2},
        "lineage": {
            "concept_ids": [C_ALIAS],
            "teaching_block_ids": [qid(C_ALIAS, "tb3"), qid(C_ALIAS, "tb4")],
            "fact_ids": [qid(C_ALIAS, "f3"), qid(C_ALIAS, "f4")]
        }
    },

    # ── s03: check – qualify and alias columns (framing only) ────────────────
    {
        "step_id": f"{TILE2_ID}.s03",
        "type": "check",
        "concept_ids": [C_ALIAS],
        "eyebrow": "Quick check",
        "title": "Which query uses the alias correctly?",
        "lede": "Choose the query that correctly assigns a table alias and uses it to qualify a column.",
        "reward": {"gems": 3, "first_try_bonus": 1},
        "lineage": {
            "concept_ids": [C_ALIAS],
            "teaching_block_ids": [],
            "fact_ids": [qid(C_ALIAS, "f3"), qid(C_ALIAS, "f4")],
            "anchors": [qid(C_ALIAS, "assessment:qualify_and_alias_columns_correctly")]
        }
    },

    # ── s04: hands_on – alias a table and use it (framing only) ──────────────
    {
        "step_id": f"{TILE2_ID}.s04",
        "type": "hands_on",
        "concept_ids": [C_ALIAS],
        "eyebrow": "Hands-on",
        "title": "Alias the orders table and qualify its columns",
        "lede": "Write a SELECT that aliases the orders table as o and uses o. to reference its columns.",
        "reward": {"gems": 4, "first_try_bonus": 2},
        "lineage": {
            "concept_ids": [C_ALIAS],
            "teaching_block_ids": [],
            "fact_ids": [
                qid(C_ALIAS, "f1"), qid(C_ALIAS, "f2"),
                qid(C_ALIAS, "f3"), qid(C_ALIAS, "f4")
            ],
            "anchors": [
                qid(C_ALIAS, "practice"),
                qid(C_ALIAS, "assessment:alias_a_table_and_use_the_alias"),
                qid(C_ALIAS, "assessment:qualify_and_alias_columns_correctly")
            ]
        }
    },

    # ── s05: explainer – DISTINCT + before_after visual ──────────────────────
    {
        "step_id": f"{TILE2_ID}.s05",
        "type": "explainer",
        "concept_ids": [C_DIST],
        "eyebrow": "DISTINCT",
        "title": "DISTINCT: one row per unique value",
        "lede": "Add DISTINCT after SELECT to collapse duplicate rows so each unique value appears exactly once.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE2_ID}.s05.b01",
                "role": "definition",
                "text": (
                    "SELECT DISTINCT removes duplicate rows from the result, keeping one "
                    "row from each group of duplicates. "
                    "SELECT DISTINCT city FROM customers returns each city exactly once, "
                    "no matter how many customers share it. "
                    "SELECT ALL — the default when DISTINCT is not written — keeps every "
                    "row, duplicates included."
                ),
                "lineage": {
                    "concept_ids": [C_DIST],
                    "teaching_block_ids": [qid(C_DIST, "tb1"), qid(C_DIST, "tb2")],
                    "fact_ids": [qid(C_DIST, "f1"), qid(C_DIST, "f2")]
                }
            },
            {
                "type": "before_after",
                "block_id": f"{TILE2_ID}.s05.b02",
                "before": {
                    "type": "data_table",
                    "asset_ref": {
                        "asset_id": "ds_customers",
                        "variant_id": None,
                        "columns": ["city"]
                    },
                    "caption": "SELECT city FROM customers — one row per customer (duplicates kept)"
                },
                "after": {
                    "type": "data_table",
                    "asset_ref": {
                        "asset_id": "ds_customers",
                        "variant_id": None,
                        "columns": ["city"],
                        "max_rows": 3
                    },
                    "caption": "SELECT DISTINCT city FROM customers — one row per unique city"
                },
                "change_summary": "Adding DISTINCT collapses the 8 city rows to 3 unique cities (Lagos, Abuja, Kano).",
                "lineage": {
                    "concept_ids": [C_DIST],
                    "teaching_block_ids": [qid(C_DIST, "tb1"), qid(C_DIST, "tb2")],
                    "fact_ids": [qid(C_DIST, "f1"), qid(C_DIST, "f2")],
                    "anchors": [qid(C_DIST, "visual")]
                }
            }
        ],
        "reward": {"gems": 2},
        "lineage": {
            "concept_ids": [C_DIST],
            "teaching_block_ids": [qid(C_DIST, "tb1"), qid(C_DIST, "tb2")],
            "fact_ids": [qid(C_DIST, "f1"), qid(C_DIST, "f2")],
            "anchors": [qid(C_DIST, "visual")]
        }
    },

    # ── s06: check – predict rows with/without DISTINCT (framing only) ───────
    {
        "step_id": f"{TILE2_ID}.s06",
        "type": "check",
        "concept_ids": [C_DIST],
        "eyebrow": "Quick check",
        "title": "How many rows does DISTINCT return?",
        "lede": "Predict the row count when DISTINCT is added to a query over the customers table.",
        "reward": {"gems": 3, "first_try_bonus": 1},
        "lineage": {
            "concept_ids": [C_DIST],
            "teaching_block_ids": [],
            "fact_ids": [qid(C_DIST, "f2")],
            "anchors": [qid(C_DIST, "assessment:predict_rows_with_and_without_distinct")]
        }
    },

    # ── s07: hands_on – write DISTINCT (framing only) ────────────────────────
    {
        "step_id": f"{TILE2_ID}.s07",
        "type": "hands_on",
        "concept_ids": [C_DIST],
        "eyebrow": "Hands-on",
        "title": "List each city exactly once",
        "lede": "Write a query that returns each distinct city in the customers table exactly once.",
        "reward": {"gems": 4, "first_try_bonus": 2},
        "lineage": {
            "concept_ids": [C_DIST],
            "teaching_block_ids": [],
            "fact_ids": [qid(C_DIST, "f1"), qid(C_DIST, "f2")],
            "anchors": [
                qid(C_DIST, "practice"),
                qid(C_DIST, "assessment:write_distinct_to_list_unique_values"),
                qid(C_DIST, "assessment:predict_rows_with_and_without_distinct")
            ]
        }
    },

    # ── s08: recap ────────────────────────────────────────────────────────────
    {
        "step_id": f"{TILE2_ID}.s08",
        "type": "recap",
        "concept_ids": [C_ALIAS, C_DIST],
        "eyebrow": "Recap",
        "title": "What you've learned",
        "lede": "Aliases shorten queries; DISTINCT removes duplicate rows.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE2_ID}.s08.b01",
                "role": "takeaway",
                "text": (
                    "A table alias — FROM orders AS o — is a temporary rename that exists "
                    "only for the current query. Once assigned, use the alias, not the "
                    "original name. Column aliases work the same way in the SELECT list. "
                    "SELECT DISTINCT collapses duplicate rows so each unique value appears once; "
                    "without it, SELECT ALL is the default and every row is kept."
                ),
                "lineage": {
                    "concept_ids": [C_ALIAS, C_DIST],
                    "teaching_block_ids": [qid(C_ALIAS, "tb5")],
                    "fact_ids": [qid(C_ALIAS, "f1"), qid(C_ALIAS, "f3")]
                }
            },
            {
                "type": "up_next",
                "block_id": f"{TILE2_ID}.s08.b02",
                "title": "Up next: Filtering rows with WHERE",
                "text": (
                    "In the next tile you will add a WHERE clause to return only the rows "
                    "that match a condition — for example, only orders delivered in under "
                    "30 minutes."
                )
            }
        ],
        "reward": {"gems": 2},
        "lineage": {
            "concept_ids": [C_ALIAS, C_DIST],
            "teaching_block_ids": [qid(C_ALIAS, "tb5")],
            "fact_ids": [qid(C_ALIAS, "f1"), qid(C_ALIAS, "f3")]
        }
    }
]

# ── Remediation steps for tile 2 ─────────────────────────────────────────────
# Concept 1 (sql.aliasing): first check = s03
# Concept 2 (sql.distinct): first check = s06

tile2_remediation = [
    {
        "step_id": f"{TILE2_ID}.r01",
        "type": "remediation",
        "concept_ids": [C_ALIAS],
        "eyebrow": "Let's revisit",
        "title": "Alias assigned — must use the alias",
        "lede": "A contrast showing what happens when you mix the alias and the original name.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE2_ID}.r01.b01",
                "role": "misconception",
                "text": (
                    "Once you write FROM orders AS o, the alias o is the only valid name "
                    "for that table in the rest of the query — referencing orders again "
                    "would be an error. "
                    "Think of it as: the alias replaces the original name for the duration "
                    "of the query, not just as an optional shortcut alongside it."
                ),
                "lineage": {
                    "concept_ids": [C_ALIAS],
                    "teaching_block_ids": [qid(C_ALIAS, "tb2")],
                    "fact_ids": [qid(C_ALIAS, "f2")]
                }
            }
        ],
        "lineage": {
            "concept_ids": [C_ALIAS],
            "teaching_block_ids": [qid(C_ALIAS, "tb2")],
            "fact_ids": [qid(C_ALIAS, "f2")]
        }
    },
    {
        "step_id": f"{TILE2_ID}.r02",
        "type": "remediation",
        "concept_ids": [C_DIST],
        "eyebrow": "Let's revisit",
        "title": "DISTINCT vs. ALL — the same column, two row counts",
        "lede": "See the difference in row count between SELECT city and SELECT DISTINCT city on the customers table.",
        "blocks": [
            {
                "type": "prose",
                "block_id": f"{TILE2_ID}.r02.b01",
                "role": "misconception",
                "text": (
                    "SELECT city FROM customers returns one row per customer — 8 rows "
                    "because there are 8 customers, even though only 3 cities appear. "
                    "SELECT DISTINCT city FROM customers returns 3 rows — one per unique "
                    "city. SELECT ALL (the default) keeps duplicates; DISTINCT removes them."
                ),
                "lineage": {
                    "concept_ids": [C_DIST],
                    "teaching_block_ids": [qid(C_DIST, "tb2")],
                    "fact_ids": [qid(C_DIST, "f1"), qid(C_DIST, "f2")]
                }
            }
        ],
        "lineage": {
            "concept_ids": [C_DIST],
            "teaching_block_ids": [qid(C_DIST, "tb2")],
            "fact_ids": [qid(C_DIST, "f1"), qid(C_DIST, "f2")]
        }
    }
]

# ── Assemble final document ───────────────────────────────────────────────────

screens = {
    "schema_version": "0.1.0",
    "kind": "screens_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_005_da_sql_canary",
    "tiles": [
        {
            "tile_id": TILE1_ID,
            "title": "The Relational Model and SELECT Basics",
            "summary": (
                "Introduces the relational model — tables, rows and columns — "
                "and the SELECT … FROM statement that reads named columns from a table."
            ),
            "steps": tile1_steps,
            "remediation_steps": tile1_remediation
        },
        {
            "tile_id": TILE2_ID,
            "title": "Aliasing and DISTINCT",
            "summary": (
                "Covers table and column aliases for readability and DISTINCT "
                "for collapsing duplicate rows in query results."
            ),
            "steps": tile2_steps,
            "remediation_steps": tile2_remediation
        }
    ]
}

out_path = "batches/final_batch_005_da_sql_canary/screens.json"
with open(out_path, "w") as f:
    json.dump(screens, f, indent=2)

print(f"Written: {out_path}")
print(f"Tile 1 steps: {len(tile1_steps)}, remediation: {len(tile1_remediation)}")
print(f"Tile 2 steps: {len(tile2_steps)}, remediation: {len(tile2_remediation)}")
