#!/usr/bin/env python3
"""Build interactions.part.c1.json for tiles: tile_pandas_creating_inspecting, tile_pandas_selection_filtering, tile_pandas_sort_rename"""
import json
import sys
from pathlib import Path

def main():
    batch_dir = Path("batches/final_batch_009_da_pandas")
    
    # Load inputs
    with open(batch_dir / "tile_plans.json") as f:
        tile_plans = json.load(f)
    with open(batch_dir / "inputs/path_glossary_bundle.json") as f:
        glossary = json.load(f)
    with open(batch_dir / "screens.json") as f:
        screens = json.load(f)
    
    # Build glossary lookup
    bundles = {b["context"]["concept_id"]: b for b in glossary["bundles"]}
    
    # Build remediation lookup
    remediation_by_concept = {}
    for tile in screens["tiles"]:
        for rem in tile.get("remediation_steps", []):
            for cid in rem.get("concept_ids", []):
                if cid not in remediation_by_concept:
                    remediation_by_concept[cid] = rem["step_id"]
    
    # Target tiles for c1
    target_tiles = [
        "tile_pandas_creating_inspecting",
        "tile_pandas_selection_filtering",
        "tile_pandas_sort_rename"
    ]
    
    tiles_data = []
    
    for tile_id in target_tiles:
        # Find tile plan
        tile_plan = next((t for t in tile_plans["tiles"] if t["tile_id"] == tile_id), None)
        if not tile_plan:
            print(f"ERROR: tile {tile_id} not found in tile_plans")
            sys.exit(1)
        
        interactions = []
        
        for step in tile_plan["steps"]:
            if step["type"] not in ("check", "hands_on"):
                continue
            
            step_id = step["step_id"]
            planned_ix_type = step["planned_interaction_type"]
            concept_ids = step["concept_ids"]
            fact_ids = step["fact_ids"]
            anchors = step["anchors"]
            
            # Build measures from anchors
            measures = []
            for anchor_id in anchors:
                if "#practice" in anchor_id:
                    # Practice anchor doesn't have a capability field
                    continue
                # Parse anchor_id: concept_id#assessment:capability or concept_id#visual
                parts = anchor_id.split("#")
                if len(parts) != 2:
                    continue
                cid = parts[0]
                anchor_part = parts[1]
                if not anchor_part.startswith("assessment:"):
                    continue
                capability = anchor_part.replace("assessment:", "")
                
                # Find the assessment anchor in the glossary
                bundle = bundles.get(cid)
                if not bundle:
                    continue
                assessment_anchors = bundle.get("assessment_anchors", [])
                anchor_obj = next((a for a in assessment_anchors if a.get("capability") == capability), None)
                if not anchor_obj:
                    continue
                
                # Get fact_ids for this anchor (bare ids, not qualified)
                anchor_fact_ids = anchor_obj.get("fact_ids", [])
                
                measures.append({
                    "concept_id": cid,
                    "capability": capability,
                    "fact_ids": anchor_fact_ids
                })
            
            # Build interaction based on type
            if planned_ix_type == "choice":
                interaction = build_choice(step_id, step, concept_ids, measures, anchors, bundles, remediation_by_concept)
            elif planned_ix_type == "code_exercise":
                interaction = build_code_exercise(step_id, step, concept_ids, measures, anchors, bundles, remediation_by_concept)
            else:
                print(f"ERROR: unknown interaction type {planned_ix_type} for {step_id}")
                sys.exit(1)
            
            interactions.append({
                "step_id": step_id,
                "interaction": interaction
            })
        
        tiles_data.append({
            "tile_id": tile_id,
            "interactions": interactions
        })
    
    # Build output
    output = {
        "schema_version": "0.1.0",
        "kind": "interactions_part",
        "path_id": "data_analyst",
        "batch_id": "final_batch_009_da_pandas",
        "tiles": tiles_data
    }
    
    # Write output
    output_path = batch_dir / "interactions.part.c1.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Wrote {output_path}")
    print(f"Tiles: {len(tiles_data)}")
    print(f"Total interactions: {sum(len(t['interactions']) for t in tiles_data)}")


def build_choice(step_id, step, concept_ids, measures, anchors, bundles, remediation_by_concept):
    """Build a choice interaction"""
    interaction_id = f"ix.{step_id}"
    
    # Determine difficulty based on position in tile
    step_num = int(step_id.split(".s")[-1])
    if step_num <= 3:
        difficulty = "intro"
    elif step_num <= 8:
        difficulty = "core"
    else:
        difficulty = "stretch"
    
    # Get first concept for remediation
    first_concept = concept_ids[0] if concept_ids else None
    remediation_step_id = remediation_by_concept.get(first_concept) if first_concept else None
    
    # Build interaction based on step_id
    if step_id == "tile_pandas_creating_inspecting.s03":
        # pandas.creating_dataframes#assessment:build_dataframe_from_list_of_dicts
        # fact: f2 (list of dicts)
        return {
            "type": "choice",
            "interaction_id": interaction_id,
            "difficulty": "intro",
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": "You have this data: `[{'order_id': 1001, 'city': 'Lagos'}, {'order_id': 1002, 'city': 'Abuja'}]`. What does `pd.DataFrame(data)` produce?",
                "options": [
                    {"option_id": "opt_a", "text": "A DataFrame with 2 rows and 2 columns, where each dict becomes one row."},
                    {"option_id": "opt_b", "text": "A DataFrame with 2 columns and 2 rows, where each dict becomes one column."},
                    {"option_id": "opt_c", "text": "A Series with 2 elements, one per dict."},
                    {"option_id": "opt_d", "text": "An error, because DataFrames require a dict of lists, not a list of dicts."}
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_a"],
                "option_feedback": {
                    "opt_a": {"message": "Correct. When you pass a list of dicts to `pd.DataFrame()`, each dict contributes one row. The keys become column names."},
                    "opt_b": {"message": "Not quite. Each dict in the list becomes a row, not a column. The keys of the dicts become the column names."},
                    "opt_c": {"message": "A list of dicts passed to `pd.DataFrame()` creates a DataFrame, not a Series. Each dict becomes a row."},
                    "opt_d": {"message": "DataFrames accept both forms: a dict of lists (keys → columns) and a list of dicts (each dict → one row). Both are valid."}
                }
            },
            "feedback": {
                "correct": {"message": "Exactly right. Each dict in the list maps to one row, with dict keys as column names."},
                "incorrect": {"message": "Review how `pd.DataFrame()` handles a list of dicts: each dict becomes one row."},
                "hints": [
                    "Think about what one dict represents: a single record with multiple fields.",
                    "The keys in each dict become the column names."
                ],
                "remediation_step_id": remediation_step_id
            }
        }
    
    elif step_id == "tile_pandas_creating_inspecting.s08":
        # pandas.inspecting_dataframes#assessment:report_rows_and_columns_with_shape
        # pandas.inspecting_dataframes#assessment:read_info_summary
        # facts: f2 (shape), f4 (info)
        return {
            "type": "choice",
            "interaction_id": interaction_id,
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": "A DataFrame `orders` has `shape` of `(250, 10)`. What does this tell you, and what additional information does `orders.info()` provide that `shape` does not?",
                "options": [
                    {"option_id": "opt_a", "text": "`shape` tells you there are 250 rows and 10 columns. `info()` adds column names, data types, and non-null counts."},
                    {"option_id": "opt_b", "text": "`shape` tells you there are 10 rows and 250 columns. `info()` adds statistical summaries like mean and median."},
                    {"option_id": "opt_c", "text": "`shape` tells you the memory usage. `info()` adds the first and last rows."},
                    {"option_id": "opt_d", "text": "`shape` and `info()` provide the same information; they are interchangeable."}
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_a"],
                "option_feedback": {
                    "opt_a": {"message": "Correct. `shape` returns (rows, columns). `info()` prints a concise summary with column names, dtypes, and non-null counts."},
                    "opt_b": {"message": "`shape` is (rows, columns), so `(250, 10)` means 250 rows and 10 columns, not the reverse. `info()` does not compute statistical summaries; that's `describe()`."},
                    "opt_c": {"message": "`shape` returns the dimensions (rows, columns), not memory usage. `info()` does show memory usage, but it does not show the first and last rows; that's `head()` and `tail()`."},
                    "opt_d": {"message": "`shape` gives only the dimensions. `info()` adds column names, data types, non-null counts, and memory usage."}
                }
            },
            "feedback": {
                "correct": {"message": "Exactly. `shape` gives dimensions; `info()` adds column detail."},
                "incorrect": {"message": "Remember: `shape` is (rows, columns). `info()` adds column names, dtypes, and non-null counts."},
                "hints": [
                    "`shape` is a tuple: (number of rows, number of columns).",
                    "`info()` prints a summary that includes data types and missing-value counts."
                ],
                "remediation_step_id": remediation_step_id
            }
        }
    
    elif step_id == "tile_pandas_creating_inspecting.s09":
        # pandas.inspecting_dataframes#assessment:get_describe_overview
        # fact: f5 (describe)
        return {
            "type": "choice",
            "interaction_id": interaction_id,
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": "You call `orders.describe()` on a DataFrame with columns `order_id`, `city`, `delivery_time_minutes`, and `distance_km`. Which columns appear in the output, and what statistics does `describe()` compute?",
                "options": [
                    {"option_id": "opt_a", "text": "Only numeric columns (`order_id`, `delivery_time_minutes`, `distance_km`) appear, with count, mean, std, min, 25%, 50%, 75%, max."},
                    {"option_id": "opt_b", "text": "All columns appear, with count, mean, std, min, max for numeric columns and unique, top, freq for text columns."},
                    {"option_id": "opt_c", "text": "Only `delivery_time_minutes` and `distance_km` appear, because `order_id` is an identifier, not a quantity."},
                    {"option_id": "opt_d", "text": "All columns appear, but only count and data type are shown."}
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_a"],
                "option_feedback": {
                    "opt_a": {"message": "Correct. `describe()` computes statistics for numeric columns: count, mean, std, min, 25%, 50% (median), 75%, max. Text columns are excluded by default."},
                    "opt_b": {"message": "By default, `describe()` includes only numeric columns. To see text columns, you must pass `include='all'`."},
                    "opt_c": {"message": "`describe()` includes all numeric columns, even identifiers like `order_id`. It does not distinguish between identifiers and quantities."},
                    "opt_d": {"message": "`describe()` computes statistical summaries (count, mean, std, min, percentiles, max) for numeric columns, not just count and data type."}
                }
            },
            "feedback": {
                "correct": {"message": "Exactly. `describe()` gives a statistical overview of numeric columns."},
                "incorrect": {"message": "Remember: `describe()` computes count, mean, std, min, quartiles, and max for numeric columns only (by default)."},
                "hints": [
                    "`describe()` focuses on numeric columns by default.",
                    "The output includes count, mean, std, min, 25%, 50%, 75%, max."
                ],
                "remediation_step_id": remediation_step_id
            }
        }
    
    elif step_id == "tile_pandas_selection_filtering.s04":
        # pandas.loc_iloc_selection#assessment:predict_iloc_slice_with_exclusive_stop
        # fact: f3 (iloc exclusive stop)
        return {
            "type": "choice",
            "interaction_id": interaction_id,
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": "A DataFrame has 10 rows with default integer index (0 through 9). What does `df.iloc[2:5]` return?",
                "options": [
                    {"option_id": "opt_a", "text": "Rows at positions 2, 3, and 4 (three rows)."},
                    {"option_id": "opt_b", "text": "Rows at positions 2, 3, 4, and 5 (four rows)."},
                    {"option_id": "opt_c", "text": "Rows at positions 3, 4, and 5 (three rows)."},
                    {"option_id": "opt_d", "text": "An error, because the stop must be inclusive."}
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_a"],
                "option_feedback": {
                    "opt_a": {"message": "Correct. `iloc` uses Python slicing: the stop is excluded. `iloc[2:5]` returns positions 2, 3, 4."},
                    "opt_b": {"message": "The stop in `iloc` slicing is excluded, just like Python list slicing. `iloc[2:5]` gives positions 2, 3, 4, not 5."},
                    "opt_c": {"message": "The start is included. `iloc[2:5]` begins at position 2, not 3."},
                    "opt_d": {"message": "`iloc` follows Python slicing rules: the stop is excluded. This is not an error; it's the standard behavior."}
                }
            },
            "feedback": {
                "correct": {"message": "Exactly. `iloc` stop is excluded, just like Python list slicing."},
                "incorrect": {"message": "Remember: `iloc[start:stop]` excludes the stop position. It's the same rule as `my_list[2:5]`."},
                "hints": [
                    "`iloc` uses Python's slicing convention: start is included, stop is excluded.",
                    "`iloc[2:5]` means positions 2, 3, 4."
                ],
                "remediation_step_id": remediation_step_id
            }
        }
    
    elif step_id == "tile_pandas_selection_filtering.s08":
        # pandas.boolean_filtering#assessment:write_single_condition_filter
        # pandas.boolean_filtering#assessment:explain_boolean_mask_row_selection
        # facts: f1 (mask), f2 (single condition)
        return {
            "type": "choice",
            "interaction_id": interaction_id,
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": "You write `mask = orders['delivery_time_minutes'] > 25`. What is `mask`, and what happens when you write `orders[mask]`?",
                "options": [
                    {"option_id": "opt_a", "text": "`mask` is a boolean Series (True/False for each row). `orders[mask]` keeps only rows where `mask` is True."},
                    {"option_id": "opt_b", "text": "`mask` is a list of row indices where the condition is True. `orders[mask]` selects those rows by position."},
                    {"option_id": "opt_c", "text": "`mask` is a new DataFrame with only the rows that meet the condition. `orders[mask]` is redundant."},
                    {"option_id": "opt_d", "text": "`mask` is a single boolean value (True or False). `orders[mask]` returns the entire DataFrame if True, or an empty DataFrame if False."}
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_a"],
                "option_feedback": {
                    "opt_a": {"message": "Correct. The comparison produces a boolean Series the same length as the DataFrame. Passing it inside `df[...]` keeps only the True rows."},
                    "opt_b": {"message": "The comparison produces a boolean Series (True/False), not a list of indices. Pandas aligns the Series with the DataFrame's index and keeps True rows."},
                    "opt_c": {"message": "The comparison produces a boolean Series, not a DataFrame. You must pass the mask inside `df[...]` to filter the rows."},
                    "opt_d": {"message": "The comparison is applied element-wise to every row, producing a Series of True/False values, not a single boolean."}
                }
            },
            "feedback": {
                "correct": {"message": "Exactly. A boolean mask is a True/False Series; `df[mask]` keeps the True rows."},
                "incorrect": {"message": "Remember: `df['col'] > value` produces a boolean Series. `df[mask]` filters to rows where the mask is True."},
                "hints": [
                    "The comparison `df['col'] > value` is applied to every row, producing a Series of True/False.",
                    "`df[mask]` keeps only the rows where the mask is True."
                ],
                "remediation_step_id": remediation_step_id
            }
        }
    
    elif step_id == "tile_pandas_selection_filtering.s09":
        # pandas.boolean_filtering#assessment:combine_conditions_with_parentheses
        # fact: f3 (combining conditions)
        return {
            "type": "choice",
            "interaction_id": interaction_id,
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": "You want to filter `orders` to rows where `city == 'Lagos'` AND `delivery_time_minutes > 25`. Which expression is correct?",
                "options": [
                    {"option_id": "opt_a", "text": "`orders[(orders['city'] == 'Lagos') & (orders['delivery_time_minutes'] > 25)]`"},
                    {"option_id": "opt_b", "text": "`orders[orders['city'] == 'Lagos' & orders['delivery_time_minutes'] > 25]`"},
                    {"option_id": "opt_c", "text": "`orders[(orders['city'] == 'Lagos') and (orders['delivery_time_minutes'] > 25)]`"},
                    {"option_id": "opt_d", "text": "`orders[orders['city'] == 'Lagos', orders['delivery_time_minutes'] > 25]`"}
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_a"],
                "option_feedback": {
                    "opt_a": {"message": "Correct. Each condition must be in parentheses, and you join them with `&` (element-wise AND)."},
                    "opt_b": {"message": "Without parentheses around each condition, Python evaluates the operators in the wrong order and raises a `ValueError`. Always wrap each condition."},
                    "opt_c": {"message": "Use `&` (element-wise AND), not `and` (Python's logical AND). `and` does not work with boolean Series."},
                    "opt_d": {"message": "You cannot pass two separate conditions as arguments. Combine them with `&` inside a single set of brackets: `df[(cond1) & (cond2)]`."}
                }
            },
            "feedback": {
                "correct": {"message": "Exactly. Wrap each condition in parentheses and join with `&`."},
                "incorrect": {"message": "Remember: each condition needs parentheses, and you join them with `&` (not `and`)."},
                "hints": [
                    "Each condition must be wrapped in its own parentheses.",
                    "Use `&` for AND, `|` for OR, and `~` for NOT."
                ],
                "remediation_step_id": remediation_step_id
            }
        }
    
    elif step_id == "tile_pandas_sort_rename.s02":
        # pandas.sort_values#assessment:set_ascending_per_column
        # fact: f2 (ascending per column)
        return {
            "type": "choice",
            "interaction_id": interaction_id,
            "difficulty": "intro",
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": "You want to sort `orders` by `city` ascending and then by `delivery_time_minutes` descending. Which call is correct?",
                "options": [
                    {"option_id": "opt_a", "text": "`orders.sort_values(by=['city', 'delivery_time_minutes'], ascending=[True, False])`"},
                    {"option_id": "opt_b", "text": "`orders.sort_values(by=['city', 'delivery_time_minutes'], ascending=False)`"},
                    {"option_id": "opt_c", "text": "`orders.sort_values(by='city', ascending=True).sort_values(by='delivery_time_minutes', ascending=False)`"},
                    {"option_id": "opt_d", "text": "`orders.sort_values(by=['city', 'delivery_time_minutes'], ascending=True)`"}
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_a"],
                "option_feedback": {
                    "opt_a": {"message": "Correct. Pass a list of booleans to `ascending`, matching the order of columns in `by`. The first column sorts ascending, the second descending."},
                    "opt_b": {"message": "A single boolean applies to all columns. To mix directions, pass a list of booleans: `ascending=[True, False]`."},
                    "opt_c": {"message": "Chaining two `sort_values()` calls works, but it's less efficient and harder to read than passing both columns and a list of booleans in one call."},
                    "opt_d": {"message": "A single boolean applies to all columns. To sort the first ascending and the second descending, pass `ascending=[True, False]`."}
                }
            },
            "feedback": {
                "correct": {"message": "Exactly. A list of booleans lets you set the direction for each column."},
                "incorrect": {"message": "Remember: to mix sort directions, pass a list of booleans to `ascending`, one per column."},
                "hints": [
                    "The `ascending` parameter can be a list of booleans, one per column in `by`.",
                    "`ascending=[True, False]` means the first column sorts ascending, the second descending."
                ],
                "remediation_step_id": remediation_step_id
            }
        }
    
    elif step_id == "tile_pandas_sort_rename.s05":
        # pandas.rename_columns_index#assessment:rename_columns_and_index_together
        # fact: f2 (rename columns and index together)
        return {
            "type": "choice",
            "interaction_id": interaction_id,
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": "You want to rename the column `city` to `destination_city` and the index label `0` to `first_order` in one call. Which expression is correct?",
                "options": [
                    {"option_id": "opt_a", "text": "`orders.rename(columns={'city': 'destination_city'}, index={0: 'first_order'})`"},
                    {"option_id": "opt_b", "text": "`orders.rename({'city': 'destination_city', 0: 'first_order'})`"},
                    {"option_id": "opt_c", "text": "`orders.rename(columns={'city': 'destination_city'}).rename(index={0: 'first_order'})`"},
                    {"option_id": "opt_d", "text": "`orders.rename('city', 'destination_city', 0, 'first_order')`"}
                ],
                "selection": "single",
                "shuffle": True
            },
            "grading": {
                "correct_option_ids": ["opt_a"],
                "option_feedback": {
                    "opt_a": {"message": "Correct. Pass both `columns=` and `index=` in the same call, each with a mapping dict."},
                    "opt_b": {"message": "You must specify `columns=` and `index=` explicitly. Without them, pandas does not know which labels are columns and which are index entries."},
                    "opt_c": {"message": "Chaining two `rename()` calls works, but it's less efficient than passing both `columns=` and `index=` in one call."},
                    "opt_d": {"message": "`rename()` takes keyword arguments `columns=` and `index=`, each with a mapping dict. It does not accept positional arguments for labels."}
                }
            },
            "feedback": {
                "correct": {"message": "Exactly. One `rename()` call can handle both columns and index."},
                "incorrect": {"message": "Remember: pass `columns={...}` and `index={...}` in the same `rename()` call."},
                "hints": [
                    "`rename()` accepts both `columns=` and `index=` in one call.",
                    "Each parameter takes a dict mapping old labels to new labels."
                ],
                "remediation_step_id": remediation_step_id
            }
        }
    
    else:
        print(f"ERROR: no choice implementation for {step_id}")
        sys.exit(1)


def build_code_exercise(step_id, step, concept_ids, measures, anchors, bundles, remediation_by_concept):
    """Build a code_exercise interaction"""
    interaction_id = f"ix.{step_id}"
    
    # Get first concept for remediation
    first_concept = concept_ids[0] if concept_ids else None
    remediation_step_id = remediation_by_concept.get(first_concept) if first_concept else None
    
    # Get practice anchor for allowed/blocked syntax
    practice_anchor_id = next((a for a in anchors if "#practice" in a), None)
    if not practice_anchor_id:
        print(f"ERROR: no practice anchor for {step_id}")
        sys.exit(1)
    
    cid = practice_anchor_id.split("#")[0]
    bundle = bundles.get(cid)
    if not bundle:
        print(f"ERROR: bundle not found for {cid}")
        sys.exit(1)
    
    practice_anchor = bundle.get("practice_anchor", {})
    live_code = practice_anchor.get("live_code", {})
    allowed_syntax = live_code.get("allowed_syntax", [])
    blocked_syntax = live_code.get("blocked_syntax", [])
    success_sentence = practice_anchor.get("success", "")
    
    # Build interaction based on step_id
    if step_id == "tile_pandas_creating_inspecting.s04":
        # pandas.creating_dataframes practice
        return {
            "type": "code_exercise",
            "interaction_id": interaction_id,
            "difficulty": "intro",
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": "Build a DataFrame two ways and print each:\n1. From `data_dict` (a dict of lists with keys `order_id`, `city`, `delivery_time_minutes`).\n2. From `data_list` (a list of dicts, each with the same keys).\n\nBoth should produce the same table with 3 rows and 3 columns.",
                "runtime": {
                    "kind": "python",
                    "version": "0.29.5",
                    "packages": ["pandas"]
                },
                "workspace": {
                    "files": [
                        {
                            "path": "solution.py",
                            "role": "editable",
                            "language": "python",
                            "content": "import pandas as pd\n\ndata_dict = {\n    'order_id': [1001, 1002, 1005],\n    'city': ['Lagos', 'Abuja', 'Abuja'],\n    'delivery_time_minutes': [18, 20, 26]\n}\n\ndata_list = [\n    {'order_id': 1001, 'city': 'Lagos', 'delivery_time_minutes': 18},\n    {'order_id': 1002, 'city': 'Abuja', 'delivery_time_minutes': 20},\n    {'order_id': 1005, 'city': 'Abuja', 'delivery_time_minutes': 26},\n]\n\n# TODO: build df1 from data_dict and print it\n# TODO: build df2 from data_list and print it\n"
                        }
                    ],
                    "entry": "solution.py"
                },
                "constraints": {
                    "allowed_syntax": allowed_syntax,
                    "blocked_syntax": blocked_syntax
                }
            },
            "grading": {
                "solution_files": [
                    {
                        "path": "solution.py",
                        "content": "import pandas as pd\n\ndata_dict = {\n    'order_id': [1001, 1002, 1005],\n    'city': ['Lagos', 'Abuja', 'Abuja'],\n    'delivery_time_minutes': [18, 20, 26]\n}\n\ndata_list = [\n    {'order_id': 1001, 'city': 'Lagos', 'delivery_time_minutes': 18},\n    {'order_id': 1002, 'city': 'Abuja', 'delivery_time_minutes': 20},\n    {'order_id': 1005, 'city': 'Abuja', 'delivery_time_minutes': 26},\n]\n\ndf1 = pd.DataFrame(data_dict)\nprint(df1)\n\ndf2 = pd.DataFrame(data_list)\nprint(df2)\n"
                    }
                ],
                "tests": [
                    {
                        "test_id": "t1",
                        "kind": "dataframe_equals",
                        "spec": {
                            "expr": "df1",
                            "expected": {
                                "columns": ["order_id", "city", "delivery_time_minutes"],
                                "rows": [
                                    [1001, "Lagos", 18],
                                    [1002, "Abuja", 20],
                                    [1005, "Abuja", 26]
                                ]
                            }
                        },
                        "visible": True,
                        "message_on_fail": "The DataFrame from `data_dict` does not match the expected structure. Check that you used `pd.DataFrame(data_dict)`."
                    },
                    {
                        "test_id": "t2",
                        "kind": "dataframe_equals",
                        "spec": {
                            "expr": "df2",
                            "expected": {
                                "columns": ["order_id", "city", "delivery_time_minutes"],
                                "rows": [
                                    [1001, "Lagos", 18],
                                    [1002, "Abuja", 20],
                                    [1005, "Abuja", 26]
                                ]
                            }
                        },
                        "visible": True,
                        "message_on_fail": "The DataFrame from `data_list` does not match the expected structure. Check that you used `pd.DataFrame(data_list)`."
                    }
                ]
            },
            "feedback": {
                "correct": {"message": "Perfect! You built DataFrames from both a dict of lists and a list of dicts."},
                "incorrect": {"message": "Review the two forms: `pd.DataFrame(dict_of_lists)` and `pd.DataFrame(list_of_dicts)`."},
                "hints": [
                    "For a dict of lists, each key is a column name, and each list is that column's values.",
                    "For a list of dicts, each dict is one row, with keys as column names."
                ],
                "remediation_step_id": remediation_step_id
            }
        }
    
    elif step_id == "tile_pandas_creating_inspecting.s10":
        # pandas.inspecting_dataframes practice
        return {
            "type": "code_exercise",
            "interaction_id": interaction_id,
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": "Load `orders.csv` and inspect it:\n1. Print the shape (row and column counts).\n2. Print the dtypes (data type of each column).\n3. Print the first 5 rows with `head()`.\n\nYour output should show the dimensions, the data types, and a preview of the data.",
                "runtime": {
                    "kind": "python",
                    "version": "0.29.5",
                    "packages": ["pandas"]
                },
                "workspace": {
                    "files": [
                        {
                            "path": "solution.py",
                            "role": "editable",
                            "language": "python",
                            "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# TODO: print the shape\n# TODO: print the dtypes\n# TODO: print the first 5 rows\n"
                        }
                    ],
                    "entry": "solution.py",
                    "asset_mounts": [
                        {
                            "asset_id": "ds_orders",
                            "mount_path": "orders.csv"
                        }
                    ]
                },
                "constraints": {
                    "allowed_syntax": allowed_syntax,
                    "blocked_syntax": blocked_syntax
                }
            },
            "grading": {
                "solution_files": [
                    {
                        "path": "solution.py",
                        "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\nprint(orders.shape)\nprint(orders.dtypes)\nprint(orders.head())\n"
                    }
                ],
                "tests": [
                    {
                        "test_id": "t1",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "orders.shape",
                            "expected": [14, 10]
                        },
                        "visible": True,
                        "message_on_fail": "The shape should be (14, 10). Check that you loaded the CSV correctly."
                    },
                    {
                        "test_id": "t2",
                        "kind": "dataframe_equals",
                        "spec": {
                            "expr": "orders.head()",
                            "expected": {
                                "columns": ["order_id", "city", "city_code", "courier", "driver_id", "customer_id", "pickup_date", "delivery_time_minutes", "distance_km", "order_value"],
                                "rows": [
                                    [1001, "Lagos", "LOS", "Ada", 201, 301, "2024-03-14", 18, 4.2, 2500],
                                    [1002, "Abuja", "ABJ", "Bayo", 202, 302, "2024-03-14", 20, 6.1, 3100],
                                    [1003, "Kano", "KAN", "Chidi", 203, 303, "2024-03-15", 22, 5.5, 1800],
                                    [1004, "Lagos", "LOS", "Ada", 201, 304, "2024-03-15", 22, 3.8, 2200],
                                    [1005, "Abuja", "ABJ", "Bayo", 202, 305, "2024-03-16", 26, 7.3, 4000]
                                ]
                            }
                        },
                        "visible": True,
                        "message_on_fail": "The first 5 rows do not match. Check that you called `head()` on the loaded DataFrame."
                    }
                ]
            },
            "feedback": {
                "correct": {"message": "Excellent! You inspected the DataFrame's dimensions, data types, and first rows."},
                "incorrect": {"message": "Review the inspection methods: `shape`, `dtypes`, and `head()`."},
                "hints": [
                    "`shape` is an attribute (no parentheses): `df.shape`.",
                    "`dtypes` is also an attribute: `df.dtypes`.",
                    "`head()` is a method: `df.head()`."
                ],
                "remediation_step_id": remediation_step_id
            }
        }
    
    elif step_id == "tile_pandas_selection_filtering.s05":
        # pandas.loc_iloc_selection practice
        return {
            "type": "code_exercise",
            "interaction_id": interaction_id,
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": "Load `orders.csv` and select data two ways:\n1. Use `.loc` to select the `city` column for rows labeled 2 through 4 (inclusive). Store in `loc_result` and print it.\n2. Use `.iloc` to select the same rows (positions 2, 3, 4) and the same column (position 1). Store in `iloc_result` and print it.\n\nBoth should return the same 3 city values: Kano, Lagos, Abuja.",
                "runtime": {
                    "kind": "python",
                    "version": "0.29.5",
                    "packages": ["pandas"]
                },
                "workspace": {
                    "files": [
                        {
                            "path": "solution.py",
                            "role": "editable",
                            "language": "python",
                            "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# TODO: use .loc to select rows 2:4 (inclusive), column 'city'\n# TODO: use .iloc to select rows 2:5 (exclusive stop), column 1\n# TODO: print both results\n"
                        }
                    ],
                    "entry": "solution.py",
                    "asset_mounts": [
                        {
                            "asset_id": "ds_orders",
                            "mount_path": "orders.csv"
                        }
                    ]
                },
                "constraints": {
                    "allowed_syntax": allowed_syntax,
                    "blocked_syntax": blocked_syntax
                }
            },
            "grading": {
                "solution_files": [
                    {
                        "path": "solution.py",
                        "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\nloc_result = orders.loc[2:4, 'city']\nprint(loc_result)\n\niloc_result = orders.iloc[2:5, 1]\nprint(iloc_result)\n"
                    }
                ],
                "tests": [
                    {
                        "test_id": "t1",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "loc_result.tolist()",
                            "expected": ["Kano", "Lagos", "Abuja"]
                        },
                        "visible": True,
                        "message_on_fail": "The `.loc` result should be ['Kano', 'Lagos', 'Abuja']. Check that you used `loc[2:4, 'city']` (inclusive stop)."
                    },
                    {
                        "test_id": "t2",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "iloc_result.tolist()",
                            "expected": ["Kano", "Lagos", "Abuja"]
                        },
                        "visible": True,
                        "message_on_fail": "The `.iloc` result should be ['Kano', 'Lagos', 'Abuja']. Check that you used `iloc[2:5, 1]` (exclusive stop)."
                    }
                ]
            },
            "feedback": {
                "correct": {"message": "Perfect! You selected the same rows and column with both `.loc` and `.iloc`, accounting for the stop difference."},
                "incorrect": {"message": "Remember: `.loc` stop is inclusive, `.iloc` stop is exclusive. To get the same rows, use different stop values."},
                "hints": [
                    "`.loc[2:4, 'city']` includes rows 2, 3, 4.",
                    "`.iloc[2:5, 1]` includes positions 2, 3, 4 (stop 5 is excluded).",
                    "Column `city` is at position 1 (0-indexed)."
                ],
                "remediation_step_id": remediation_step_id
            }
        }
    
    elif step_id == "tile_pandas_selection_filtering.s10":
        # pandas.boolean_filtering practice
        return {
            "type": "code_exercise",
            "interaction_id": interaction_id,
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": "Load `orders.csv` and filter it:\n1. Keep only rows where `delivery_time_minutes > 25`. Store in `slow` and print it.\n\nThe result should contain 7 rows (orders 1005, 1006, 1007, 1008, 1011, 1013, 1014).",
                "runtime": {
                    "kind": "python",
                    "version": "0.29.5",
                    "packages": ["pandas"]
                },
                "workspace": {
                    "files": [
                        {
                            "path": "solution.py",
                            "role": "editable",
                            "language": "python",
                            "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# TODO: filter to rows where delivery_time_minutes > 25\n# TODO: print the result\n"
                        }
                    ],
                    "entry": "solution.py",
                    "asset_mounts": [
                        {
                            "asset_id": "ds_orders",
                            "mount_path": "orders.csv"
                        }
                    ]
                },
                "constraints": {
                    "allowed_syntax": allowed_syntax,
                    "blocked_syntax": blocked_syntax
                }
            },
            "grading": {
                "solution_files": [
                    {
                        "path": "solution.py",
                        "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\nslow = orders[orders['delivery_time_minutes'] > 25]\nprint(slow)\n"
                    }
                ],
                "tests": [
                    {
                        "test_id": "t1",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "slow['order_id'].tolist()",
                            "expected": [1005, 1006, 1007, 1008, 1011, 1013, 1014]
                        },
                        "visible": True,
                        "message_on_fail": "The filtered result should contain order_ids [1005, 1006, 1007, 1008, 1011, 1013, 1014]. Check your filter condition."
                    },
                    {
                        "test_id": "t2",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "len(slow)",
                            "expected": 7
                        },
                        "visible": True,
                        "message_on_fail": "The filtered result should have 7 rows. Check that you used `> 25`, not `>= 25`."
                    }
                ]
            },
            "feedback": {
                "correct": {"message": "Excellent! You filtered to rows where delivery time is above the threshold."},
                "incorrect": {"message": "Review the boolean filtering syntax: `df[df['col'] > value]`."},
                "hints": [
                    "The condition `df['col'] > value` produces a boolean Series.",
                    "Pass the boolean Series inside `df[...]` to filter the rows."
                ],
                "remediation_step_id": remediation_step_id
            }
        }
    
    elif step_id == "tile_pandas_sort_rename.s03":
        # pandas.sort_values practice
        return {
            "type": "code_exercise",
            "interaction_id": interaction_id,
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": "Load `orders.csv` and sort it:\n1. Primary sort: `city` ascending (A→Z).\n2. Tiebreaker: `delivery_time_minutes` descending (largest to smallest).\n\nStore the sorted DataFrame in `sorted_orders` and print it. Within each city, the longest delivery times should appear first.",
                "runtime": {
                    "kind": "python",
                    "version": "0.29.5",
                    "packages": ["pandas"]
                },
                "workspace": {
                    "files": [
                        {
                            "path": "solution.py",
                            "role": "editable",
                            "language": "python",
                            "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# TODO: sort by city ascending, then delivery_time_minutes descending\n# TODO: print the result\n"
                        }
                    ],
                    "entry": "solution.py",
                    "asset_mounts": [
                        {
                            "asset_id": "ds_orders",
                            "mount_path": "orders.csv"
                        }
                    ]
                },
                "constraints": {
                    "allowed_syntax": allowed_syntax,
                    "blocked_syntax": blocked_syntax
                }
            },
            "grading": {
                "solution_files": [
                    {
                        "path": "solution.py",
                        "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\nsorted_orders = orders.sort_values(by=['city', 'delivery_time_minutes'], ascending=[True, False])\nprint(sorted_orders)\n"
                    }
                ],
                "tests": [
                    {
                        "test_id": "t1",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "sorted_orders['order_id'].tolist()",
                            "expected": [1008, 1005, 1002, 1006, 1003, 1007, 1004, 1001]
                        },
                        "visible": True,
                        "message_on_fail": "The sorted order_ids should be [1008, 1005, 1002, 1006, 1003, 1007, 1004, 1001]. Check your sort columns and directions."
                    },
                    {
                        "test_id": "t2",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "sorted_orders['city'].tolist()",
                            "expected": ["Abuja", "Abuja", "Abuja", "Kano", "Kano", "Lagos", "Lagos", "Lagos"]
                        },
                        "visible": True,
                        "message_on_fail": "The cities should be sorted alphabetically. Check that you used `ascending=[True, False]`."
                    }
                ]
            },
            "feedback": {
                "correct": {"message": "Perfect! You sorted by city ascending and delivery time descending."},
                "incorrect": {"message": "Review the `sort_values()` syntax: pass a list of columns to `by=` and a list of booleans to `ascending=`."},
                "hints": [
                    "Pass `by=['city', 'delivery_time_minutes']` to sort by both columns.",
                    "Pass `ascending=[True, False]` to sort the first ascending and the second descending."
                ],
                "remediation_step_id": remediation_step_id
            }
        }
    
    elif step_id == "tile_pandas_sort_rename.s06":
        # pandas.rename_columns_index practice
        return {
            "type": "code_exercise",
            "interaction_id": interaction_id,
            "difficulty": "core",
            "grading_mode": "client",
            "standalone": False,
            "measures": measures,
            "anchors": anchors,
            "public": {
                "prompt": "Load `orders.csv` and rename:\n1. Column `city` → `destination_city`.\n2. Column `delivery_time_minutes` → `delivery_min`.\n3. Index label `0` → `first_order`.\n\nStore the renamed DataFrame in `renamed` and print it. All other labels should remain unchanged.",
                "runtime": {
                    "kind": "python",
                    "version": "0.29.5",
                    "packages": ["pandas"]
                },
                "workspace": {
                    "files": [
                        {
                            "path": "solution.py",
                            "role": "editable",
                            "language": "python",
                            "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# TODO: rename columns and index\n# TODO: print the result\n"
                        }
                    ],
                    "entry": "solution.py",
                    "asset_mounts": [
                        {
                            "asset_id": "ds_orders",
                            "mount_path": "orders.csv"
                        }
                    ]
                },
                "constraints": {
                    "allowed_syntax": allowed_syntax,
                    "blocked_syntax": blocked_syntax
                }
            },
            "grading": {
                "solution_files": [
                    {
                        "path": "solution.py",
                        "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\nrenamed = orders.rename(columns={'city': 'destination_city', 'delivery_time_minutes': 'delivery_min'}, index={0: 'first_order'})\nprint(renamed)\n"
                    }
                ],
                "tests": [
                    {
                        "test_id": "t1",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "'destination_city' in renamed.columns",
                            "expected": True
                        },
                        "visible": True,
                        "message_on_fail": "The column `destination_city` should exist. Check that you renamed `city`."
                    },
                    {
                        "test_id": "t2",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "'delivery_min' in renamed.columns",
                            "expected": True
                        },
                        "visible": True,
                        "message_on_fail": "The column `delivery_min` should exist. Check that you renamed `delivery_time_minutes`."
                    },
                    {
                        "test_id": "t3",
                        "kind": "value_equals",
                        "spec": {
                            "expr": "renamed.index[0]",
                            "expected": "first_order"
                        },
                        "visible": True,
                        "message_on_fail": "The first index label should be `first_order`. Check that you renamed index `0`."
                    }
                ]
            },
            "feedback": {
                "correct": {"message": "Excellent! You renamed two columns and one index label in a single call."},
                "incorrect": {"message": "Review the `rename()` syntax: pass `columns={...}` and `index={...}` in one call."},
                "hints": [
                    "Pass `columns={'old': 'new', ...}` to rename columns.",
                    "Pass `index={0: 'first_order'}` to rename the index label 0."
                ],
                "remediation_step_id": remediation_step_id
            }
        }
    
    else:
        print(f"ERROR: no code_exercise implementation for {step_id}")
        sys.exit(1)


if __name__ == "__main__":
    main()
