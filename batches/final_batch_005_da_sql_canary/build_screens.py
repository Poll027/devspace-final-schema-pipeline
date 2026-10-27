#!/usr/bin/env python3
"""Build screens.json for final_batch_005_da_sql_canary."""
import json, pathlib

OUT = pathlib.Path("batches/final_batch_005_da_sql_canary/screens.json")

screens = {
  "schema_version": "0.1.0",
  "kind": "screens_part",
  "path_id": "data_analyst",
  "batch_id": "final_batch_005_da_sql_canary",
  "tiles": [

    # ─────────────────────────────────────────────────────────────────────────
    # TILE 1: tile_sql_fund_relational_select
    # ─────────────────────────────────────────────────────────────────────────
    {
      "tile_id": "tile_sql_fund_relational_select",
      "title": "The Relational Model and SELECT Basics",
      "summary": "Learn how relational databases organise data into named tables of rows and columns, then write your first SELECT statements to pull specific columns from the QuickDeliver dataset.",
      "steps": [

        # ── s01: explainer — relational_model tb1+tb2, visual = data_table ──
        {
          "step_id": "tile_sql_fund_relational_select.s01",
          "type": "explainer",
          "concept_ids": ["sql.relational_model"],
          "eyebrow": "Relational databases",
          "title": "Tables, rows and columns",
          "lede": "A relational database stores data in separate named tables — one for customers, one for orders, one for products.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_relational_select.s01.b1",
              "role": "intro",
              "text": "QuickDeliver keeps its data in three tables: customers, orders, and products. A relational database is built from exactly this kind of piece — each table holds one kind of data, and together they describe the whole business.",
              "lineage": {
                "concept_ids": ["sql.relational_model"],
                "teaching_block_ids": ["sql.relational_model#tb1"],
                "fact_ids": ["sql.relational_model#f1", "sql.relational_model#f4"]
              }
            },
            {
              "type": "prose",
              "block_id": "tile_sql_fund_relational_select.s01.b2",
              "role": "definition",
              "text": "A table (also called a relation) holds data where each row — also called a record or tuple — represents one group of related values. The columns are also called fields or attributes. In the customers table, each row is one customer, and the columns customer_id, name, and city are the attributes recorded about every customer.",
              "lineage": {
                "concept_ids": ["sql.relational_model"],
                "teaching_block_ids": ["sql.relational_model#tb2"],
                "fact_ids": ["sql.relational_model#f1", "sql.relational_model#f2", "sql.relational_model#f4"]
              }
            },
            {
              "type": "data_table",
              "block_id": "tile_sql_fund_relational_select.s01.b3",
              "asset_ref": {
                "asset_id": "ds.customers",
                "variant_id": None,
                "columns": ["customer_id", "name", "city"],
                "max_rows": 4
              },
              "caption": "customers — each row is one customer (record/tuple); each column is an attribute (field).",
              "tag_columns": [
                {"column": "customer_id", "tag": "field / attribute", "tone": "focus"},
                {"column": "name", "tag": "field / attribute", "tone": "focus"},
                {"column": "city", "tag": "field / attribute", "tone": "focus"}
              ],
              "lineage": {
                "concept_ids": ["sql.relational_model"],
                "teaching_block_ids": ["sql.relational_model#tb2"],
                "fact_ids": ["sql.relational_model#f1", "sql.relational_model#f2"],
                "anchors": ["sql.relational_model#visual"]
              }
            }
          ],
          "reward": {"gems": 2},
          "lineage": {
            "concept_ids": ["sql.relational_model"],
            "teaching_block_ids": ["sql.relational_model#tb1", "sql.relational_model#tb2"],
            "fact_ids": ["sql.relational_model#f1", "sql.relational_model#f2", "sql.relational_model#f4"]
          }
        },

        # ── s02: explainer — relational_model tb3, no visual ──
        {
          "step_id": "tile_sql_fund_relational_select.s02",
          "type": "explainer",
          "concept_ids": ["sql.relational_model"],
          "eyebrow": "Relational databases",
          "title": "What makes a table well-formed",
          "lede": "A well-formed table has a unique name, no duplicate rows, and covers exactly one kind of thing.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_relational_select.s02.b1",
              "role": "mechanism",
              "text": "Every table in a database has a name that is distinct from every other table — 'customers' is not reused for anything else. A table contains no duplicate rows, and the order its rows and columns happen to appear in is not meaningful.",
              "lineage": {
                "concept_ids": ["sql.relational_model"],
                "teaching_block_ids": ["sql.relational_model#tb3"],
                "fact_ids": ["sql.relational_model#f3"]
              }
            },
            {
              "type": "prose",
              "block_id": "tile_sql_fund_relational_select.s02.b2",
              "role": "practical_context",
              "text": "Each table should contain information about one kind of thing only — a Customer or an Order, not both mixed together. That is why QuickDeliver keeps customer details and order details in two separate tables rather than one merged one.",
              "lineage": {
                "concept_ids": ["sql.relational_model"],
                "teaching_block_ids": ["sql.relational_model#tb3"],
                "fact_ids": ["sql.relational_model#f5"]
              }
            }
          ],
          "reward": {"gems": 2},
          "lineage": {
            "concept_ids": ["sql.relational_model"],
            "teaching_block_ids": ["sql.relational_model#tb3"],
            "fact_ids": ["sql.relational_model#f3", "sql.relational_model#f5"]
          }
        },

        # ── s03: check — relational_model, framing only ──
        {
          "step_id": "tile_sql_fund_relational_select.s03",
          "type": "check",
          "concept_ids": ["sql.relational_model"],
          "eyebrow": "Quick check",
          "title": "Is this table well-formed?",
          "lede": "Apply the three properties of a well-formed table.",
          "reward": {"gems": 3, "first_try_bonus": 1},
          "lineage": {
            "concept_ids": ["sql.relational_model"],
            "teaching_block_ids": [],
            "fact_ids": ["sql.relational_model#f3", "sql.relational_model#f5"],
            "anchors": ["sql.relational_model#assessment:judge_whether_a_table_design_is_well_formed"]
          }
        },

        # ── s04: hands_on — relational_model, framing only ──
        {
          "step_id": "tile_sql_fund_relational_select.s04",
          "type": "hands_on",
          "concept_ids": ["sql.relational_model"],
          "eyebrow": "Hands-on",
          "title": "Identify rows and columns in the customers table",
          "lede": "Select the parts of the table that match each SQL term.",
          "reward": {"gems": 4, "first_try_bonus": 2},
          "lineage": {
            "concept_ids": ["sql.relational_model"],
            "teaching_block_ids": [],
            "fact_ids": ["sql.relational_model#f1", "sql.relational_model#f2", "sql.relational_model#f4"],
            "anchors": [
              "sql.relational_model#practice",
              "sql.relational_model#assessment:identify_table_rows_columns_in_scenario"
            ]
          }
        },

        # ── s05: explainer — select_fundamentals tb1+tb2+tb3, visual = code_walkthrough ──
        {
          "step_id": "tile_sql_fund_relational_select.s05",
          "type": "explainer",
          "concept_ids": ["sql.select_fundamentals"],
          "eyebrow": "SELECT basics",
          "title": "SELECT, FROM and AS",
          "lede": "A SELECT statement names the columns you want and the table to read them from.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_relational_select.s05.b1",
              "role": "intro",
              "text": "You know the customers table has columns customer_id, name, and city. To pull that data out of the database, you write a SELECT statement.",
              "lineage": {
                "concept_ids": ["sql.select_fundamentals"],
                "teaching_block_ids": ["sql.select_fundamentals#tb1"],
                "fact_ids": ["sql.select_fundamentals#f1"]
              }
            },
            {
              "type": "prose",
              "block_id": "tile_sql_fund_relational_select.s05.b2",
              "role": "definition",
              "text": "The SELECT list — everything between SELECT and FROM — specifies the expressions that form the output rows. The FROM clause names the table the query reads from. So SELECT name, city FROM customers reads the customers table and returns just those two columns for every row.",
              "lineage": {
                "concept_ids": ["sql.select_fundamentals"],
                "teaching_block_ids": ["sql.select_fundamentals#tb2"],
                "fact_ids": ["sql.select_fundamentals#f1", "sql.select_fundamentals#f3"]
              }
            },
            {
              "type": "prose",
              "block_id": "tile_sql_fund_relational_select.s05.b3",
              "role": "syntax",
              "text": "You can rename an output column by writing AS output_name after its expression in the SELECT list. AS can be omitted if the name you want does not collide with a keyword. SELECT name AS customer_name, city FROM customers returns the same data, but the first column is labelled customer_name in the result.",
              "lineage": {
                "concept_ids": ["sql.select_fundamentals"],
                "teaching_block_ids": ["sql.select_fundamentals#tb3"],
                "fact_ids": ["sql.select_fundamentals#f2"]
              }
            },
            {
              "type": "code_walkthrough",
              "block_id": "tile_sql_fund_relational_select.s05.b4",
              "language": "sql",
              "code": "SELECT name AS customer_name,\n       city\nFROM   customers;",
              "annotations": [
                {
                  "start_line": 1,
                  "end_line": 2,
                  "text": "SELECT list: the two expressions that form each output row. AS renames 'name' to 'customer_name' in the result."
                },
                {
                  "start_line": 3,
                  "end_line": 3,
                  "text": "FROM clause: the customers table supplies the rows."
                }
              ],
              "reveal": "line_by_line",
              "lineage": {
                "concept_ids": ["sql.select_fundamentals"],
                "teaching_block_ids": ["sql.select_fundamentals#tb2", "sql.select_fundamentals#tb3"],
                "fact_ids": ["sql.select_fundamentals#f1", "sql.select_fundamentals#f2", "sql.select_fundamentals#f3"],
                "anchors": ["sql.select_fundamentals#visual"]
              }
            }
          ],
          "reward": {"gems": 2},
          "lineage": {
            "concept_ids": ["sql.select_fundamentals"],
            "teaching_block_ids": [
              "sql.select_fundamentals#tb1",
              "sql.select_fundamentals#tb2",
              "sql.select_fundamentals#tb3"
            ],
            "fact_ids": [
              "sql.select_fundamentals#f1",
              "sql.select_fundamentals#f2",
              "sql.select_fundamentals#f3"
            ]
          }
        },

        # ── s06: video — select_fundamentals ──
        {
          "step_id": "tile_sql_fund_relational_select.s06",
          "type": "video",
          "concept_ids": ["sql.select_fundamentals"],
          "eyebrow": "Watch",
          "title": "SELECT and FROM picking just the columns you need",
          "lede": "See SELECT and FROM in action on a customers table.",
          "blocks": [
            {
              "type": "media_group",
              "block_id": "tile_sql_fund_relational_select.s06.b1",
              "group_title": "SELECT and FROM picking just the columns you need",
              "segment_ids": ["seg_sql.select_fundamentals_082lfHzdTe8_326_444"]
            }
          ],
          "reward": {"gems": 1},
          "lineage": {
            "concept_ids": ["sql.select_fundamentals"],
            "teaching_block_ids": [],
            "fact_ids": ["sql.select_fundamentals#f1", "sql.select_fundamentals#f3"],
            "segment_ids": ["seg_sql.select_fundamentals_082lfHzdTe8_326_444"]
          }
        },

        # ── s07: explainer — select_fundamentals tb4 ──
        {
          "step_id": "tile_sql_fund_relational_select.s07",
          "type": "explainer",
          "concept_ids": ["sql.select_fundamentals"],
          "eyebrow": "SELECT basics",
          "title": "Using * to select all columns",
          "lede": "A star in the SELECT list is shorthand for every column.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_relational_select.s07.b1",
              "role": "example",
              "text": "Writing * in the SELECT list returns all columns of every selected row, so SELECT * FROM customers returns customer_id, name, and city without listing them one by one. When a query reads from more than one table, table_name.* narrows the star to just that table's columns.",
              "lineage": {
                "concept_ids": ["sql.select_fundamentals"],
                "teaching_block_ids": ["sql.select_fundamentals#tb4"],
                "fact_ids": ["sql.select_fundamentals#f4"]
              }
            }
          ],
          "reward": {"gems": 1},
          "lineage": {
            "concept_ids": ["sql.select_fundamentals"],
            "teaching_block_ids": ["sql.select_fundamentals#tb4"],
            "fact_ids": ["sql.select_fundamentals#f4"]
          }
        },

        # ── s08: check — select_fundamentals, framing only ──
        {
          "step_id": "tile_sql_fund_relational_select.s08",
          "type": "check",
          "concept_ids": ["sql.select_fundamentals"],
          "eyebrow": "Quick check",
          "title": "Write a SELECT for listed columns",
          "lede": "Choose the correct SELECT statement to return specific columns.",
          "reward": {"gems": 3, "first_try_bonus": 1},
          "lineage": {
            "concept_ids": ["sql.select_fundamentals"],
            "teaching_block_ids": [],
            "fact_ids": ["sql.select_fundamentals#f1", "sql.select_fundamentals#f3"],
            "anchors": ["sql.select_fundamentals#assessment:write_select_for_listed_columns"]
          }
        },

        # ── s09: hands_on — select_fundamentals, framing only ──
        {
          "step_id": "tile_sql_fund_relational_select.s09",
          "type": "hands_on",
          "concept_ids": ["sql.select_fundamentals"],
          "eyebrow": "Hands-on",
          "title": "Rename a column with AS",
          "lede": "Write a SELECT statement that returns three columns from customers, renaming at least one with AS.",
          "reward": {"gems": 5, "first_try_bonus": 2},
          "lineage": {
            "concept_ids": ["sql.select_fundamentals"],
            "teaching_block_ids": [],
            "fact_ids": ["sql.select_fundamentals#f2"],
            "anchors": [
              "sql.select_fundamentals#practice",
              "sql.select_fundamentals#assessment:rename_output_column_with_as"
            ]
          }
        },

        # ── s10: recap ──
        {
          "step_id": "tile_sql_fund_relational_select.s10",
          "type": "recap",
          "concept_ids": ["sql.relational_model", "sql.select_fundamentals"],
          "eyebrow": "Recap",
          "title": "What you've learned",
          "lede": "Two concepts, one foundation.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_relational_select.s10.b1",
              "role": "takeaway",
              "text": "A relational database stores data in named tables. Each row represents one thing — a customer, an order — and each column is an attribute of that thing. A database is composed of multiple tables, each covering one kind of data. SELECT ... FROM is the shape every query builds on: FROM names the table to read, and the SELECT list names the columns — renamed or not — that come back out.",
              "lineage": {
                "concept_ids": ["sql.relational_model", "sql.select_fundamentals"],
                "teaching_block_ids": [
                  "sql.relational_model#tb4",
                  "sql.select_fundamentals#tb5"
                ],
                "fact_ids": [
                  "sql.relational_model#f1",
                  "sql.relational_model#f5",
                  "sql.select_fundamentals#f1",
                  "sql.select_fundamentals#f3"
                ]
              }
            },
            {
              "type": "up_next",
              "block_id": "tile_sql_fund_relational_select.s10.b2",
              "title": "Up next: Aliasing and DISTINCT",
              "text": "In the next tile you will give tables short temporary names with AS and use DISTINCT to list each unique city exactly once."
            }
          ],
          "reward": {"gems": 2},
          "lineage": {
            "concept_ids": ["sql.relational_model", "sql.select_fundamentals"],
            "teaching_block_ids": [
              "sql.relational_model#tb4",
              "sql.select_fundamentals#tb5"
            ],
            "fact_ids": [
              "sql.relational_model#f1",
              "sql.relational_model#f5",
              "sql.select_fundamentals#f1",
              "sql.select_fundamentals#f3"
            ]
          }
        }
      ],

      # ── remediation steps ──
      "remediation_steps": [
        # r01: for s03 (check: judge_whether_a_table_design_is_well_formed) — facts f3, f5
        {
          "step_id": "tile_sql_fund_relational_select.r01",
          "type": "remediation",
          "concept_ids": ["sql.relational_model"],
          "eyebrow": "Let's review",
          "title": "What makes a table well-formed",
          "lede": "A well-formed table has three key properties.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_relational_select.r01.b1",
              "role": "mechanism",
              "text": "A well-formed table has a name that is distinct from every other table in the database. It contains no duplicate rows — every row is unique. And the order its rows and columns appear in is not meaningful.",
              "lineage": {
                "concept_ids": ["sql.relational_model"],
                "teaching_block_ids": ["sql.relational_model#tb3"],
                "fact_ids": ["sql.relational_model#f3"]
              }
            },
            {
              "type": "prose",
              "block_id": "tile_sql_fund_relational_select.r01.b2",
              "role": "practical_context",
              "text": "Each table should cover one kind of thing only. A table that mixes customer details and order details in the same rows is not well-formed — those belong in separate tables. QuickDeliver keeps customers, orders, and products in three distinct tables for exactly this reason.",
              "lineage": {
                "concept_ids": ["sql.relational_model"],
                "teaching_block_ids": ["sql.relational_model#tb3"],
                "fact_ids": ["sql.relational_model#f5"]
              }
            }
          ],
          "lineage": {
            "concept_ids": ["sql.relational_model"],
            "teaching_block_ids": ["sql.relational_model#tb3"],
            "fact_ids": ["sql.relational_model#f3", "sql.relational_model#f5"]
          }
        },

        # r02: for s04 (hands_on: identify_table_rows_columns_in_scenario) — facts f1, f2, f4
        {
          "step_id": "tile_sql_fund_relational_select.r02",
          "type": "remediation",
          "concept_ids": ["sql.relational_model"],
          "eyebrow": "Let's review",
          "title": "Rows, columns and tables",
          "lede": "Each row is one thing; each column is one attribute.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_relational_select.r02.b1",
              "role": "definition",
              "text": "A table holds data where each row — also called a record or tuple — represents one group of related values. The columns are also called fields or attributes. In the customers table, row 1 is Amara Okafor from Lagos; the columns customer_id, name, and city are the attributes recorded for every customer.",
              "lineage": {
                "concept_ids": ["sql.relational_model"],
                "teaching_block_ids": ["sql.relational_model#tb2"],
                "fact_ids": ["sql.relational_model#f1", "sql.relational_model#f2"]
              }
            },
            {
              "type": "prose",
              "block_id": "tile_sql_fund_relational_select.r02.b2",
              "role": "practical_context",
              "text": "A database is composed of multiple tables, each holding its own kind of data. QuickDeliver has a customers table, an orders table, and a products table — three separate tables, each covering one kind of thing.",
              "lineage": {
                "concept_ids": ["sql.relational_model"],
                "teaching_block_ids": ["sql.relational_model#tb2"],
                "fact_ids": ["sql.relational_model#f4"]
              }
            }
          ],
          "lineage": {
            "concept_ids": ["sql.relational_model"],
            "teaching_block_ids": ["sql.relational_model#tb2"],
            "fact_ids": ["sql.relational_model#f1", "sql.relational_model#f2", "sql.relational_model#f4"]
          }
        },

        # r03: for s08 (check: write_select_for_listed_columns) — facts f1, f3
        {
          "step_id": "tile_sql_fund_relational_select.r03",
          "type": "remediation",
          "concept_ids": ["sql.select_fundamentals"],
          "eyebrow": "Let's review",
          "title": "SELECT list and FROM clause",
          "lede": "The SELECT list names the columns; FROM names the table.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_relational_select.r03.b1",
              "role": "definition",
              "text": "The SELECT list — everything between SELECT and FROM — specifies the expressions that form the output rows. The FROM clause names the table the query reads from. SELECT name, city FROM customers returns exactly those two columns for every row in the customers table.",
              "lineage": {
                "concept_ids": ["sql.select_fundamentals"],
                "teaching_block_ids": ["sql.select_fundamentals#tb2"],
                "fact_ids": ["sql.select_fundamentals#f1", "sql.select_fundamentals#f3"]
              }
            }
          ],
          "lineage": {
            "concept_ids": ["sql.select_fundamentals"],
            "teaching_block_ids": ["sql.select_fundamentals#tb2"],
            "fact_ids": ["sql.select_fundamentals#f1", "sql.select_fundamentals#f3"]
          }
        },

        # r04: for s09 (hands_on: rename_output_column_with_as) — fact f2
        {
          "step_id": "tile_sql_fund_relational_select.r04",
          "type": "remediation",
          "concept_ids": ["sql.select_fundamentals"],
          "eyebrow": "Let's review",
          "title": "Renaming a column with AS",
          "lede": "AS output_name after a column expression changes its label in the result.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_relational_select.r04.b1",
              "role": "syntax",
              "text": "Writing AS output_name after a column's expression in the SELECT list names that output column. AS can be omitted if the desired name does not match a keyword. SELECT name AS customer_name FROM customers returns the name column labelled customer_name in the result, not name.",
              "lineage": {
                "concept_ids": ["sql.select_fundamentals"],
                "teaching_block_ids": ["sql.select_fundamentals#tb3"],
                "fact_ids": ["sql.select_fundamentals#f2"]
              }
            }
          ],
          "lineage": {
            "concept_ids": ["sql.select_fundamentals"],
            "teaching_block_ids": ["sql.select_fundamentals#tb3"],
            "fact_ids": ["sql.select_fundamentals#f2"]
          }
        }
      ]
    },

    # ─────────────────────────────────────────────────────────────────────────
    # TILE 2: tile_sql_fund_alias_distinct
    # ─────────────────────────────────────────────────────────────────────────
    {
      "tile_id": "tile_sql_fund_alias_distinct",
      "title": "Aliasing and DISTINCT",
      "summary": "Give tables and columns short temporary names with AS, qualify column references with a table alias, and use SELECT DISTINCT to list each unique value exactly once.",
      "steps": [

        # ── s01: explainer — aliasing tb1+tb2, visual = code_walkthrough ──
        {
          "step_id": "tile_sql_fund_alias_distinct.s01",
          "type": "explainer",
          "concept_ids": ["sql.aliasing"],
          "eyebrow": "Aliasing",
          "title": "Giving a table a short name",
          "lede": "FROM orders AS o gives the orders table the short name o for the rest of that query.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_alias_distinct.s01.b1",
              "role": "intro",
              "text": "Typing out orders or customers in full every time gets tedious, especially once a query refers to a table's columns repeatedly. SQL lets you give a table a short temporary name for the query instead.",
              "lineage": {
                "concept_ids": ["sql.aliasing"],
                "teaching_block_ids": ["sql.aliasing#tb1"],
                "fact_ids": ["sql.aliasing#f1"]
              }
            },
            {
              "type": "prose",
              "block_id": "tile_sql_fund_alias_distinct.s01.b2",
              "role": "definition",
              "text": "A table alias is a temporary name given to a table reference, written FROM table_reference AS alias — AS is optional. FROM orders AS o gives the orders table the short name o for the rest of that query. Once assigned, the table must be referred to by its alias, not its original name — writing FROM orders AS o and then referencing orders again later would be an error.",
              "lineage": {
                "concept_ids": ["sql.aliasing"],
                "teaching_block_ids": ["sql.aliasing#tb2"],
                "fact_ids": ["sql.aliasing#f1", "sql.aliasing#f2"]
              }
            },
            {
              "type": "code_walkthrough",
              "block_id": "tile_sql_fund_alias_distinct.s01.b3",
              "language": "sql",
              "code": "SELECT o.order_id,\n       o.delivery_time_minutes AS delivery_min\nFROM   orders AS o;",
              "annotations": [
                {
                  "start_line": 1,
                  "end_line": 2,
                  "text": "o. qualifies each column with the alias. AS delivery_min renames the output column."
                },
                {
                  "start_line": 3,
                  "end_line": 3,
                  "text": "FROM orders AS o — 'o' is the alias. Use 'o' everywhere in this query; 'orders' is no longer valid here."
                }
              ],
              "reveal": "line_by_line",
              "lineage": {
                "concept_ids": ["sql.aliasing"],
                "teaching_block_ids": ["sql.aliasing#tb2"],
                "fact_ids": ["sql.aliasing#f1", "sql.aliasing#f2"],
                "anchors": ["sql.aliasing#visual"]
              }
            }
          ],
          "reward": {"gems": 2},
          "lineage": {
            "concept_ids": ["sql.aliasing"],
            "teaching_block_ids": ["sql.aliasing#tb1", "sql.aliasing#tb2"],
            "fact_ids": ["sql.aliasing#f1", "sql.aliasing#f2"]
          }
        },

        # ── s02: explainer — aliasing tb3+tb4 ──
        {
          "step_id": "tile_sql_fund_alias_distinct.s02",
          "type": "explainer",
          "concept_ids": ["sql.aliasing"],
          "eyebrow": "Aliasing",
          "title": "Column aliases and qualified references",
          "lede": "Alias a column with AS and reference it as alias.column_name.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_alias_distinct.s02.b1",
              "role": "syntax",
              "text": "A column can be aliased the same way: write AS output_name after the column's expression in the SELECT list. A column can also be referenced as correlation.columnname, where correlation is a table name or an alias defined in the FROM clause. With orders aliased to o, you write o.customer_id instead of orders.customer_id. The correlation name and dot can be left off entirely when the column name is unique across every table used in the query.",
              "lineage": {
                "concept_ids": ["sql.aliasing"],
                "teaching_block_ids": ["sql.aliasing#tb3"],
                "fact_ids": ["sql.aliasing#f3", "sql.aliasing#f4"]
              }
            },
            {
              "type": "prose",
              "block_id": "tile_sql_fund_alias_distinct.s02.b2",
              "role": "practical_context",
              "text": "On a single table like SELECT o.order_id, o.delivery_time_minutes FROM orders AS o, qualifying a column with the alias is optional — the column names are already unique. The alias starts to matter once a query reads from more than one table and two of those tables share a column name; qualifying which table's copy you mean is what keeps the query unambiguous.",
              "lineage": {
                "concept_ids": ["sql.aliasing"],
                "teaching_block_ids": ["sql.aliasing#tb4"],
                "fact_ids": ["sql.aliasing#f4"]
              }
            }
          ],
          "reward": {"gems": 2},
          "lineage": {
            "concept_ids": ["sql.aliasing"],
            "teaching_block_ids": ["sql.aliasing#tb3", "sql.aliasing#tb4"],
            "fact_ids": ["sql.aliasing#f3", "sql.aliasing#f4"]
          }
        },

        # ── s03: check — aliasing, framing only ──
        {
          "step_id": "tile_sql_fund_alias_distinct.s03",
          "type": "check",
          "concept_ids": ["sql.aliasing"],
          "eyebrow": "Quick check",
          "title": "Qualify and alias columns correctly",
          "lede": "Choose the query that correctly uses a table alias and qualifies its columns.",
          "reward": {"gems": 3, "first_try_bonus": 1},
          "lineage": {
            "concept_ids": ["sql.aliasing"],
            "teaching_block_ids": [],
            "fact_ids": ["sql.aliasing#f3", "sql.aliasing#f4"],
            "anchors": ["sql.aliasing#assessment:qualify_and_alias_columns_correctly"]
          }
        },

        # ── s04: hands_on — aliasing, framing only ──
        {
          "step_id": "tile_sql_fund_alias_distinct.s04",
          "type": "hands_on",
          "concept_ids": ["sql.aliasing"],
          "eyebrow": "Hands-on",
          "title": "Alias the orders table and qualify its columns",
          "lede": "Write a query that gives orders a short alias, qualifies every column with that alias, and renames one output column with AS.",
          "reward": {"gems": 5, "first_try_bonus": 2},
          "lineage": {
            "concept_ids": ["sql.aliasing"],
            "teaching_block_ids": [],
            "fact_ids": [
              "sql.aliasing#f1",
              "sql.aliasing#f2",
              "sql.aliasing#f3",
              "sql.aliasing#f4"
            ],
            "anchors": [
              "sql.aliasing#practice",
              "sql.aliasing#assessment:alias_a_table_and_use_the_alias",
              "sql.aliasing#assessment:qualify_and_alias_columns_correctly"
            ]
          }
        },

        # ── s05: explainer — distinct tb1+tb2, visual = before_after ──
        {
          "step_id": "tile_sql_fund_alias_distinct.s05",
          "type": "explainer",
          "concept_ids": ["sql.distinct"],
          "eyebrow": "DISTINCT",
          "title": "Removing duplicate rows with DISTINCT",
          "lede": "SELECT DISTINCT keeps one row from each group of duplicates.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_alias_distinct.s05.b1",
              "role": "definition",
              "text": "SELECT DISTINCT removes duplicate rows from the result, keeping one row from each group of duplicates. SELECT DISTINCT city FROM customers returns each city that appears in the customers table exactly once, no matter how many customers share it.",
              "lineage": {
                "concept_ids": ["sql.distinct"],
                "teaching_block_ids": ["sql.distinct#tb1"],
                "fact_ids": ["sql.distinct#f1"]
              }
            },
            {
              "type": "prose",
              "block_id": "tile_sql_fund_alias_distinct.s05.b2",
              "role": "example",
              "text": "SELECT ALL is the default when DISTINCT is not written — it keeps every row, duplicates included. SELECT city FROM customers lists Lagos once per customer who lives there, while SELECT DISTINCT city FROM customers lists Lagos only once.",
              "lineage": {
                "concept_ids": ["sql.distinct"],
                "teaching_block_ids": ["sql.distinct#tb2"],
                "fact_ids": ["sql.distinct#f2"]
              }
            },
            {
              "type": "before_after",
              "block_id": "tile_sql_fund_alias_distinct.s05.b3",
              "before": {
                "type": "data_table",
                "asset_ref": {
                  "asset_id": "ds.customers",
                  "variant_id": None,
                  "columns": ["city"]
                },
                "caption": "SELECT city FROM customers — all rows, Lagos appears three times."
              },
              "after": {
                "type": "data_table",
                "result_of": {
                  "runtime": "sql",
                  "sql": "SELECT DISTINCT city FROM customers ORDER BY city",
                  "asset_mounts": [
                    {"asset_id": "ds.customers", "mount_path": "customers"}
                  ]
                },
                "caption": "SELECT DISTINCT city FROM customers — each city appears once."
              },
              "change_summary": "Adding DISTINCT collapses the three Lagos rows into one, returning each city exactly once.",
              "lineage": {
                "concept_ids": ["sql.distinct"],
                "teaching_block_ids": ["sql.distinct#tb1", "sql.distinct#tb2"],
                "fact_ids": ["sql.distinct#f1", "sql.distinct#f2"],
                "anchors": ["sql.distinct#visual"]
              }
            }
          ],
          "reward": {"gems": 2},
          "lineage": {
            "concept_ids": ["sql.distinct"],
            "teaching_block_ids": ["sql.distinct#tb1", "sql.distinct#tb2"],
            "fact_ids": ["sql.distinct#f1", "sql.distinct#f2"]
          }
        },

        # ── s06: check — distinct, framing only ──
        {
          "step_id": "tile_sql_fund_alias_distinct.s06",
          "type": "check",
          "concept_ids": ["sql.distinct"],
          "eyebrow": "Quick check",
          "title": "Predict rows with and without DISTINCT",
          "lede": "How many rows does each query return from the customers table?",
          "reward": {"gems": 3, "first_try_bonus": 1},
          "lineage": {
            "concept_ids": ["sql.distinct"],
            "teaching_block_ids": [],
            "fact_ids": ["sql.distinct#f2"],
            "anchors": ["sql.distinct#assessment:predict_rows_with_and_without_distinct"]
          }
        },

        # ── s07: hands_on — distinct, framing only ──
        {
          "step_id": "tile_sql_fund_alias_distinct.s07",
          "type": "hands_on",
          "concept_ids": ["sql.distinct"],
          "eyebrow": "Hands-on",
          "title": "List each distinct city exactly once",
          "lede": "Write a query that returns each unique city from the customers table exactly once.",
          "reward": {"gems": 5, "first_try_bonus": 2},
          "lineage": {
            "concept_ids": ["sql.distinct"],
            "teaching_block_ids": [],
            "fact_ids": ["sql.distinct#f1", "sql.distinct#f2"],
            "anchors": [
              "sql.distinct#practice",
              "sql.distinct#assessment:write_distinct_to_list_unique_values",
              "sql.distinct#assessment:predict_rows_with_and_without_distinct"
            ]
          }
        },

        # ── s08: recap ──
        {
          "step_id": "tile_sql_fund_alias_distinct.s08",
          "type": "recap",
          "concept_ids": ["sql.aliasing", "sql.distinct"],
          "eyebrow": "Recap",
          "title": "What you've learned",
          "lede": "Aliases and DISTINCT — two tools for cleaner queries.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_alias_distinct.s08.b1",
              "role": "takeaway",
              "text": "Whether it's naming a table or a column, an alias is the same idea: a temporary rename that exists only for the current query, chosen to make the query shorter or its output columns clearer. Once a table alias is assigned, use it — not the original name — for the rest of that query. DISTINCT removes duplicate rows from the result, keeping one row from each group; without it, SELECT ALL is the default and every row is returned.",
              "lineage": {
                "concept_ids": ["sql.aliasing", "sql.distinct"],
                "teaching_block_ids": ["sql.aliasing#tb5"],
                "fact_ids": ["sql.aliasing#f1", "sql.aliasing#f3"]
              }
            },
            {
              "type": "up_next",
              "block_id": "tile_sql_fund_alias_distinct.s08.b2",
              "title": "Up next: Filtering rows with WHERE",
              "text": "In the next tile you will use WHERE to return only the rows that match a condition — for example, only orders delivered in under 30 minutes."
            }
          ],
          "reward": {"gems": 2},
          "lineage": {
            "concept_ids": ["sql.aliasing", "sql.distinct"],
            "teaching_block_ids": ["sql.aliasing#tb5"],
            "fact_ids": ["sql.aliasing#f1", "sql.aliasing#f3"]
          }
        }
      ],

      # ── remediation steps ──
      "remediation_steps": [
        # r01: for s03 (check: qualify_and_alias_columns_correctly) — facts f3, f4
        {
          "step_id": "tile_sql_fund_alias_distinct.r01",
          "type": "remediation",
          "concept_ids": ["sql.aliasing"],
          "eyebrow": "Let's review",
          "title": "Column aliases and qualified references",
          "lede": "Use alias.column to reference a column through its table alias.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_alias_distinct.r01.b1",
              "role": "syntax",
              "text": "A column can be aliased by writing AS output_name after its expression in the SELECT list. A column can also be referenced as correlation.columnname, where correlation is a table name or alias from the FROM clause. With orders aliased to o, write o.customer_id — not orders.customer_id. The dot prefix can be dropped when the column name is unique across all tables in the query.",
              "lineage": {
                "concept_ids": ["sql.aliasing"],
                "teaching_block_ids": ["sql.aliasing#tb3"],
                "fact_ids": ["sql.aliasing#f3", "sql.aliasing#f4"]
              }
            }
          ],
          "lineage": {
            "concept_ids": ["sql.aliasing"],
            "teaching_block_ids": ["sql.aliasing#tb3"],
            "fact_ids": ["sql.aliasing#f3", "sql.aliasing#f4"]
          }
        },

        # r02: for s04 (hands_on: alias_a_table_and_use_the_alias + qualify_and_alias_columns_correctly) — facts f1,f2,f3,f4
        {
          "step_id": "tile_sql_fund_alias_distinct.r02",
          "type": "remediation",
          "concept_ids": ["sql.aliasing"],
          "eyebrow": "Let's review",
          "title": "Table aliases — the full picture",
          "lede": "Assign an alias in FROM, then use it everywhere in that query.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_alias_distinct.r02.b1",
              "role": "definition",
              "text": "A table alias is a temporary name written FROM table AS alias. Once assigned, the alias replaces the original table name for the rest of that query — using the original name again is an error. Columns can be qualified as alias.column and renamed with AS output_name in the SELECT list.",
              "lineage": {
                "concept_ids": ["sql.aliasing"],
                "teaching_block_ids": ["sql.aliasing#tb2", "sql.aliasing#tb3"],
                "fact_ids": ["sql.aliasing#f1", "sql.aliasing#f2", "sql.aliasing#f3", "sql.aliasing#f4"]
              }
            }
          ],
          "lineage": {
            "concept_ids": ["sql.aliasing"],
            "teaching_block_ids": ["sql.aliasing#tb2", "sql.aliasing#tb3"],
            "fact_ids": ["sql.aliasing#f1", "sql.aliasing#f2", "sql.aliasing#f3", "sql.aliasing#f4"]
          }
        },

        # r03: for s06 (check: predict_rows_with_and_without_distinct) — fact f2
        {
          "step_id": "tile_sql_fund_alias_distinct.r03",
          "type": "remediation",
          "concept_ids": ["sql.distinct"],
          "eyebrow": "Let's review",
          "title": "SELECT ALL vs SELECT DISTINCT",
          "lede": "Without DISTINCT, every row is returned — duplicates included.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_alias_distinct.r03.b1",
              "role": "example",
              "text": "SELECT ALL is the default when DISTINCT is not written — it keeps every row, duplicates included. The customers table has eight rows with three distinct cities: Lagos (3 customers), Abuja (2), Kano (2), Port Harcourt (1). SELECT city FROM customers returns eight rows; SELECT DISTINCT city FROM customers returns four.",
              "lineage": {
                "concept_ids": ["sql.distinct"],
                "teaching_block_ids": ["sql.distinct#tb2"],
                "fact_ids": ["sql.distinct#f2"]
              }
            }
          ],
          "lineage": {
            "concept_ids": ["sql.distinct"],
            "teaching_block_ids": ["sql.distinct#tb2"],
            "fact_ids": ["sql.distinct#f2"]
          }
        },

        # r04: for s07 (hands_on: write_distinct_to_list_unique_values + predict_rows_with_and_without_distinct) — facts f1, f2
        {
          "step_id": "tile_sql_fund_alias_distinct.r04",
          "type": "remediation",
          "concept_ids": ["sql.distinct"],
          "eyebrow": "Let's review",
          "title": "DISTINCT — one row per unique value",
          "lede": "Place DISTINCT right after SELECT to collapse duplicate rows.",
          "blocks": [
            {
              "type": "prose",
              "block_id": "tile_sql_fund_alias_distinct.r04.b1",
              "role": "definition",
              "text": "SELECT DISTINCT removes duplicate rows from the result, keeping one row from each group of duplicates. SELECT DISTINCT city FROM customers returns each city exactly once. Without DISTINCT, SELECT ALL is in effect and every row is returned — Lagos appears three times because three customers live there.",
              "lineage": {
                "concept_ids": ["sql.distinct"],
                "teaching_block_ids": ["sql.distinct#tb1", "sql.distinct#tb2"],
                "fact_ids": ["sql.distinct#f1", "sql.distinct#f2"]
              }
            }
          ],
          "lineage": {
            "concept_ids": ["sql.distinct"],
            "teaching_block_ids": ["sql.distinct#tb1", "sql.distinct#tb2"],
            "fact_ids": ["sql.distinct#f1", "sql.distinct#f2"]
          }
        }
      ]
    }
  ]
}

OUT.write_text(json.dumps(screens, indent=2, ensure_ascii=False))
print(f"Written {OUT}")

# Count steps
for tile in screens["tiles"]:
    main = len(tile["steps"])
    rem = len(tile.get("remediation_steps", []))
    print(f"  {tile['tile_id']}: {main} steps + {rem} remediation steps")
