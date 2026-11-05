#!/usr/bin/env python3
"""Build interactions.part.c3.json for chunk c3 tiles."""
import json

OUT = "batches/final_batch_011_da_spreadsheet/interactions.part.c3.json"

def choice(interaction_id, difficulty, measures, anchors, prompt, options, correct_ids,
           option_feedback, correct_msg, incorrect_msg, hints, remediation_step_id=None,
           standalone=False):
    ix = {
        "type": "choice",
        "interaction_id": interaction_id,
        "difficulty": difficulty,
        "grading_mode": "client",
        "standalone": standalone,
        "measures": measures,
        "anchors": anchors,
        "public": {
            "prompt": prompt,
            "options": options,
            "selection": "single",
            "shuffle": True
        },
        "grading": {
            "correct_option_ids": correct_ids,
            "option_feedback": option_feedback
        },
        "feedback": {
            "correct": {"message": correct_msg},
            "incorrect": {"message": incorrect_msg},
            "hints": hints
        }
    }
    if remediation_step_id:
        ix["feedback"]["remediation_step_id"] = remediation_step_id
    return ix


def formula_entry(interaction_id, difficulty, measures, anchors, prompt,
                  asset_id, sheet_name, target_cell, allowed_functions,
                  expected_value, reference_formula, must_use_functions,
                  correct_msg, incorrect_msg, hints, remediation_step_id=None,
                  tolerance=None, standalone=False):
    pub = {
        "prompt": prompt,
        "asset_ref": {"asset_id": asset_id, "variant_id": None},
        "sheet_name": sheet_name,
        "target_cell": target_cell,
        "allowed_functions": allowed_functions
    }
    grading = {
        "expected_value": expected_value,
        "reference_formula": reference_formula,
        "must_use_functions": must_use_functions,
        "forbid_hardcoded_values": True
    }
    if tolerance is not None:
        grading["tolerance"] = tolerance
    ix = {
        "type": "formula_entry",
        "interaction_id": interaction_id,
        "difficulty": difficulty,
        "grading_mode": "client",
        "standalone": standalone,
        "measures": measures,
        "anchors": anchors,
        "public": pub,
        "grading": grading,
        "feedback": {
            "correct": {"message": correct_msg},
            "incorrect": {"message": incorrect_msg},
            "hints": hints
        }
    }
    if remediation_step_id:
        ix["feedback"]["remediation_step_id"] = remediation_step_id
    return ix


# ─────────────────────────────────────────────────────────────────────────────
# tile_spreadsheet_tables_named_ranges
# ─────────────────────────────────────────────────────────────────────────────

# s04: check — verify_table_auto_expansion_on_new_data (f4)
s04_tables = choice(
    interaction_id="ix.tile_spreadsheet_tables_named_ranges.s04",
    difficulty="intro",
    measures=[{
        "concept_id": "spreadsheet.structured_tables",
        "capability": "verify_table_auto_expansion_on_new_data",
        "fact_ids": ["f4"]
    }],
    anchors=["spreadsheet.structured_tables#assessment:verify_table_auto_expansion_on_new_data"],
    prompt=(
        "The Orders table currently ends at row 21. A new delivery arrives and you type its "
        "order ID in cell A22. What happens to the table?"
    ),
    options=[
        {"option_id": "opt_a", "text": "The table automatically expands to include row 22, applying the table style and structured references to the new row."},
        {"option_id": "opt_b", "text": "Nothing happens; you must manually resize the table by dragging its corner handle to include row 22."},
        {"option_id": "opt_c", "text": "Excel shows an error because the new row is outside the table boundary."},
        {"option_id": "opt_d", "text": "The table expands only if the new row contains data in every column."}
    ],
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": {"message": "Manual resizing is not required. Typing a value in the cell immediately below the last row of a table causes the table to expand automatically to include that new row."},
        "opt_c": {"message": "No error occurs. Excel is designed to grow the table automatically when you type in the cell just below the last row — that is one of the key benefits of using a table."},
        "opt_d": {"message": "The table expands as soon as you type any value in the cell just below the last row, regardless of whether other columns in that row are filled in yet."}
    },
    correct_msg="Correct! Typing a value in the cell immediately below a table's last row causes the table to expand automatically — the style and structured references extend to cover the new row.",
    incorrect_msg="Typing a value in the cell just below a table's last row automatically expands the table to include that row. No manual resizing is needed.",
    hints=[
        "Think about what 'auto-expansion' means: the table grows on its own when new data is added adjacent to it.",
        "The key word is 'immediately below' — the cell must be directly under the last row of the table."
    ],
    remediation_step_id="tile_spreadsheet_tables_named_ranges.r01"
)

# s05: hands_on — structured reference formula =SUM(Orders[Amount])
# SUM(D2:D21) = 99100.0
s05_tables = formula_entry(
    interaction_id="ix.tile_spreadsheet_tables_named_ranges.s05",
    difficulty="core",
    measures=[
        {
            "concept_id": "spreadsheet.structured_tables",
            "capability": "write_formula_using_structured_reference",
            "fact_ids": ["f3"]
        },
        {
            "concept_id": "spreadsheet.structured_tables",
            "capability": "create_table_from_range_and_manage_header",
            "fact_ids": ["f1", "f2"]
        },
        {
            "concept_id": "spreadsheet.structured_tables",
            "capability": "verify_table_auto_expansion_on_new_data",
            "fact_ids": ["f4"]
        }
    ],
    anchors=[
        "spreadsheet.structured_tables#practice",
        "spreadsheet.structured_tables#assessment:create_table_from_range_and_manage_header",
        "spreadsheet.structured_tables#assessment:write_formula_using_structured_reference",
        "spreadsheet.structured_tables#assessment:verify_table_auto_expansion_on_new_data"
    ],
    prompt=(
        "The Orders sheet contains a table named Orders with columns order_id, city, "
        "delivery_minutes, amount, status, driver_id, and order_date. "
        "In cell F1, write a formula using a structured reference that returns the total "
        "of the amount column. Use the table name Orders and the column name amount in square brackets."
    ),
    asset_id="asset_orders_clean",
    sheet_name="Orders",
    target_cell="F1",
    allowed_functions=["SUM"],
    expected_value=99100.0,
    reference_formula="=SUM(Orders[amount])",
    must_use_functions=["SUM"],
    correct_msg="Correct! =SUM(Orders[amount]) uses a structured reference — the table name followed by the column name in square brackets — instead of a raw cell range like D2:D21. The total is 99100.",
    incorrect_msg="A structured reference names the table and column directly: =SUM(Orders[amount]). Use the table name Orders, then the column name amount inside square brackets.",
    hints=[
        "A structured reference has the form =SUM(TableName[ColumnName]). The table is named Orders and the column is amount.",
        "Make sure to include the square brackets around the column name: Orders[amount], not Orders(amount)."
    ],
    remediation_step_id="tile_spreadsheet_tables_named_ranges.r01"
)

# s07: check — replace_cell_reference_with_named_range_in_formula (f1, f2)
s07_tables = choice(
    interaction_id="ix.tile_spreadsheet_tables_named_ranges.s07",
    difficulty="intro",
    measures=[{
        "concept_id": "spreadsheet.named_ranges",
        "capability": "replace_cell_reference_with_named_range_in_formula",
        "fact_ids": ["f1", "f2"]
    }],
    anchors=["spreadsheet.named_ranges#assessment:replace_cell_reference_with_named_range_in_formula"],
    prompt=(
        "You have selected C2:C21 (the delivery_minutes column) and typed DeliveryTimes "
        "into the Name Box, then pressed Enter. Which formula correctly uses that named range "
        "to calculate the average delivery time?"
    ),
    options=[
        {"option_id": "opt_a", "text": "=AVERAGE(DeliveryTimes)"},
        {"option_id": "opt_b", "text": "=AVERAGE(\"DeliveryTimes\")"},
        {"option_id": "opt_c", "text": "=AVERAGE(C2:C21) — named ranges cannot be used in formulas"},
        {"option_id": "opt_d", "text": "=DeliveryTimes.AVERAGE()"}
    ],
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": {"message": "Putting the name in quotes makes it a text string, not a range reference. Excel would return a #VALUE! error. Use the name without quotes: =AVERAGE(DeliveryTimes)."},
        "opt_c": {"message": "Named ranges can absolutely be used in formulas. Once you define a name, you can type it directly in any formula in place of the cell range — for example =AVERAGE(DeliveryTimes)."},
        "opt_d": {"message": "That is not valid Excel syntax. To use a named range in a formula, simply type the name as the argument: =AVERAGE(DeliveryTimes)."}
    },
    correct_msg="Correct! Once a name is defined, you use it directly in a formula as the argument — =AVERAGE(DeliveryTimes) — without quotes and without any special syntax.",
    incorrect_msg="A named range is used in a formula by typing the name directly as the argument, without quotes: =AVERAGE(DeliveryTimes). The name replaces the raw cell range C2:C21.",
    hints=[
        "A named range is used exactly like a cell range in a formula — just type the name where you would normally type the cell address.",
        "No quotes, no dots, no special syntax — just the name: =AVERAGE(DeliveryTimes)."
    ],
    remediation_step_id="tile_spreadsheet_tables_named_ranges.r02"
)

# s08: hands_on — named range usage
# SUM(C2:C21) = 541 (delivery_minutes, non-null values only; SUM ignores nulls)
# Note: SUM ignores null/blank cells, so =SUM(C2:C21) = 541
s08_tables = formula_entry(
    interaction_id="ix.tile_spreadsheet_tables_named_ranges.s08",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.named_ranges",
        "capability": "replace_cell_reference_with_named_range_in_formula",
        "fact_ids": ["f1", "f2"]
    }],
    anchors=[
        "spreadsheet.named_ranges#practice",
        "spreadsheet.named_ranges#assessment:replace_cell_reference_with_named_range_in_formula"
    ],
    prompt=(
        "The Orders sheet has delivery_minutes values in C2:C21. Imagine you have already "
        "named that range DeliveryTimes using the Name Box. "
        "In cell G1, write a formula using SUM and the named range DeliveryTimes to return "
        "the total of all delivery_minutes values. "
        "(The grader evaluates the result; type =SUM(DeliveryTimes) as you would after naming the range.)"
    ),
    asset_id="asset_orders_clean",
    sheet_name="Orders",
    target_cell="G1",
    allowed_functions=["SUM"],
    expected_value=541,
    reference_formula="=SUM(C2:C21)",
    must_use_functions=["SUM"],
    correct_msg="Correct! =SUM(DeliveryTimes) uses the named range in place of the raw address C2:C21. The total of all recorded delivery times is 541 minutes.",
    incorrect_msg="Use SUM with the named range: =SUM(DeliveryTimes). The name DeliveryTimes stands for C2:C21, so the result is the same as =SUM(C2:C21) — 541 minutes.",
    hints=[
        "Type the name exactly as defined — DeliveryTimes — as the argument to SUM.",
        "The formula looks like =SUM(DeliveryTimes), replacing the cell range with the name you defined in the Name Box."
    ],
    remediation_step_id="tile_spreadsheet_tables_named_ranges.r02"
)

# ─────────────────────────────────────────────────────────────────────────────
# tile_spreadsheet_pivot_tables
# ─────────────────────────────────────────────────────────────────────────────

# s04: check — execute_pivot_table_creation_steps + identify_visual_output_of_each_pivot_area (f2, f4)
s04_pivot = choice(
    interaction_id="ix.tile_spreadsheet_pivot_tables.s04",
    difficulty="intro",
    measures=[
        {
            "concept_id": "spreadsheet.pivot_tables",
            "capability": "execute_pivot_table_creation_steps",
            "fact_ids": ["f2"]
        },
        {
            "concept_id": "spreadsheet.pivot_tables",
            "capability": "identify_visual_output_of_each_pivot_area",
            "fact_ids": ["f4"]
        }
    ],
    anchors=[
        "spreadsheet.pivot_tables#assessment:execute_pivot_table_creation_steps",
        "spreadsheet.pivot_tables#assessment:identify_visual_output_of_each_pivot_area"
    ],
    prompt=(
        "You drag the city field into the Rows area of a PivotTable. "
        "Where does city appear in the finished PivotTable?"
    ),
    options=[
        {"option_id": "opt_a", "text": "As Row Labels on the left side of the PivotTable, with one row per city."},
        {"option_id": "opt_b", "text": "As Column Labels across the top of the PivotTable, with one column per city."},
        {"option_id": "opt_c", "text": "As a top-level report filter above the PivotTable."},
        {"option_id": "opt_d", "text": "As summarized numeric values in the body of the PivotTable."}
    ],
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": {"message": "Column Labels appear when a field is placed in the Columns area, not the Rows area. A field in the Rows area appears as Row Labels on the left side."},
        "opt_c": {"message": "A top-level report filter appears when a field is placed in the Filters area. A field in the Rows area appears as Row Labels on the left side of the PivotTable."},
        "opt_d": {"message": "Summarized numeric values appear in the Values area. A field in the Rows area appears as Row Labels — one row per unique value of that field."}
    },
    correct_msg="Correct! A field placed in the Rows area appears as Row Labels on the left side of the PivotTable — one row for each unique value of that field (e.g., one row per city).",
    incorrect_msg="The Rows area produces Row Labels on the left side of the PivotTable. Each unique value of the field (e.g., each city name) gets its own row.",
    hints=[
        "Think about the four areas: Filters (top), Columns (top header), Rows (left side), Values (body numbers).",
        "The Rows area places field values down the left side of the PivotTable as row labels."
    ],
    remediation_step_id="tile_spreadsheet_pivot_tables.r01"
)

# s05: check — build_pivot_table_to_answer_summarization_requirement (f2, f3, f4)
s05_pivot = choice(
    interaction_id="ix.tile_spreadsheet_pivot_tables.s05",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.pivot_tables",
        "capability": "build_pivot_table_to_answer_summarization_requirement",
        "fact_ids": ["f2", "f3", "f4"]
    }],
    anchors=["spreadsheet.pivot_tables#assessment:build_pivot_table_to_answer_summarization_requirement"],
    prompt=(
        "You want a PivotTable that shows the total order amount for each city, "
        "with cities listed down the left and a single column of totals. "
        "Which field placement achieves this?"
    ),
    options=[
        {"option_id": "opt_a", "text": "city in Rows area; amount in Values area."},
        {"option_id": "opt_b", "text": "city in Columns area; amount in Values area."},
        {"option_id": "opt_c", "text": "city in Values area; amount in Rows area."},
        {"option_id": "opt_d", "text": "city in Filters area; amount in Rows area."}
    ],
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": {"message": "Placing city in the Columns area would spread city names across the top as column headers, not down the left as row labels. To list cities down the left, place city in the Rows area."},
        "opt_c": {"message": "The Values area holds numeric summaries, not category labels. city is a text field and should go in the Rows area; amount is numeric and should go in the Values area."},
        "opt_d": {"message": "The Filters area creates a top-level report filter, not row labels. To list cities down the left side, place city in the Rows area."}
    },
    correct_msg="Correct! city in the Rows area creates one row per city on the left side; amount in the Values area fills in the total for each city. That gives you the city-by-total layout you need.",
    incorrect_msg="To list cities down the left with totals beside them, place city in the Rows area and amount in the Values area. Rows area → left-side labels; Values area → numeric summaries.",
    hints=[
        "Rows area = left-side labels (one row per unique value). Values area = numeric summaries in the body.",
        "Match the field type to the area: text/category fields go in Rows or Columns; numeric fields go in Values."
    ],
    remediation_step_id="tile_spreadsheet_pivot_tables.r01"
)

# s06: hands_on — pivot_tables practice (f1, f3)
# Use SUMIF to compute what a pivot table Values area would show for Lagos
# SUMIF(B2:B21,"Lagos",D2:D21) = 28000.0
s06_pivot = formula_entry(
    interaction_id="ix.tile_spreadsheet_pivot_tables.s06",
    difficulty="core",
    measures=[
        {
            "concept_id": "spreadsheet.pivot_tables",
            "capability": "define_pivot_table_purpose",
            "fact_ids": ["f1"]
        },
        {
            "concept_id": "spreadsheet.pivot_tables",
            "capability": "add_and_reposition_fields_in_pivot_areas",
            "fact_ids": ["f3"]
        }
    ],
    anchors=[
        "spreadsheet.pivot_tables#practice",
        "spreadsheet.pivot_tables#assessment:define_pivot_table_purpose",
        "spreadsheet.pivot_tables#assessment:add_and_reposition_fields_in_pivot_areas"
    ],
    prompt=(
        "A PivotTable with city in the Rows area and amount in the Values area would show "
        "the total amount for each city. In cell F1, write a formula that returns the total "
        "amount for Lagos orders — the value that would appear in the Lagos row of that PivotTable. "
        "Use SUMIF with the city range B2:B21, the criterion \"Lagos\", and the amount range D2:D21."
    ),
    asset_id="asset_orders_clean",
    sheet_name="Orders",
    target_cell="F1",
    allowed_functions=["SUMIF"],
    expected_value=28000.0,
    reference_formula='=SUMIF(B2:B21,"Lagos",D2:D21)',
    must_use_functions=["SUMIF"],
    correct_msg="Correct! =SUMIF(B2:B21,\"Lagos\",D2:D21) returns 28000 — the total amount for Lagos orders. In a PivotTable with city in Rows and amount in Values, this is exactly the value that would appear in the Lagos row.",
    incorrect_msg="Use SUMIF with three arguments: the city range (B2:B21), the criterion (\"Lagos\"), and the amount range (D2:D21). The formula is =SUMIF(B2:B21,\"Lagos\",D2:D21).",
    hints=[
        "SUMIF takes three arguments: =SUMIF(range, criteria, sum_range). The range is the city column, the criteria is \"Lagos\", and the sum_range is the amount column.",
        "Make sure to put Lagos in double quotes inside the formula: =SUMIF(B2:B21,\"Lagos\",D2:D21)."
    ],
    remediation_step_id="tile_spreadsheet_pivot_tables.r01"
)

# s09: check — identify_default_summarization_by_data_type (f1)
s09_pivot = choice(
    interaction_id="ix.tile_spreadsheet_pivot_tables.s09",
    difficulty="intro",
    measures=[{
        "concept_id": "spreadsheet.pivot_summarization",
        "capability": "identify_default_summarization_by_data_type",
        "fact_ids": ["f1"]
    }],
    anchors=["spreadsheet.pivot_summarization#assessment:identify_default_summarization_by_data_type"],
    prompt=(
        "You add the status field (which contains text values: Delivered, Pending, Cancelled) "
        "to the Values area of a PivotTable. What summary function does Excel apply by default?"
    ),
    options=[
        {"option_id": "opt_a", "text": "COUNT — because the field contains text values, not numbers."},
        {"option_id": "opt_b", "text": "SUM — because SUM is always the default for any field in the Values area."},
        {"option_id": "opt_c", "text": "AVERAGE — because Excel averages all values by default."},
        {"option_id": "opt_d", "text": "MAX — because Excel picks the largest value by default."}
    ],
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": {"message": "SUM is the default only for numeric fields. When the field contains text values, Excel defaults to COUNT instead, because you cannot add text values together."},
        "opt_c": {"message": "AVERAGE is not the default for any field type. Excel defaults to SUM for numeric fields and COUNT for text fields."},
        "opt_d": {"message": "MAX is not the default. Excel defaults to SUM for numeric fields and COUNT for text fields."}
    },
    correct_msg="Correct! Excel defaults to COUNT for text fields in the Values area, because text values cannot be summed. For numeric fields it defaults to SUM.",
    incorrect_msg="Excel uses COUNT as the default for text fields in the Values area (you cannot sum text), and SUM as the default for numeric fields.",
    hints=[
        "Ask yourself: can you add text values like 'Delivered' and 'Pending' together? If not, what would Excel do instead?",
        "The rule is: numeric field → SUM by default; text field → COUNT by default."
    ],
    remediation_step_id="tile_spreadsheet_pivot_tables.r02"
)

# s10: hands_on — pivot_summarization practice (f2)
# AVERAGE(D2:D21) = 4955.0
s10_pivot = formula_entry(
    interaction_id="ix.tile_spreadsheet_pivot_tables.s10",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.pivot_summarization",
        "capability": "select_correct_value_field_summarization_setting",
        "fact_ids": ["f2"]
    }],
    anchors=[
        "spreadsheet.pivot_summarization#practice",
        "spreadsheet.pivot_summarization#assessment:select_correct_value_field_summarization_setting"
    ],
    prompt=(
        "A PivotTable currently shows the Sum of amount for each city. "
        "You want to change the Values area to show the Average of amount instead. "
        "In cell F1, write a formula that returns the average order amount across all 20 orders — "
        "the overall average that the PivotTable grand total row would show after switching to Average. "
        "Use AVERAGE with the range D2:D21."
    ),
    asset_id="asset_orders_clean",
    sheet_name="Orders",
    target_cell="F1",
    allowed_functions=["AVERAGE"],
    expected_value=4955.0,
    reference_formula="=AVERAGE(D2:D21)",
    must_use_functions=["AVERAGE"],
    correct_msg="Correct! =AVERAGE(D2:D21) returns 4955 — the average order amount. After changing the PivotTable's Values field setting from Sum to Average, the grand total row would show this value.",
    incorrect_msg="Use AVERAGE with the amount range: =AVERAGE(D2:D21). This returns the average order amount across all 20 orders.",
    hints=[
        "The AVERAGE function takes a range as its argument: =AVERAGE(D2:D21).",
        "The amount column is column D, rows 2 through 21 (20 orders)."
    ],
    remediation_step_id="tile_spreadsheet_pivot_tables.r02"
)

# ─────────────────────────────────────────────────────────────────────────────
# tile_spreadsheet_chart_types
# ─────────────────────────────────────────────────────────────────────────────

# s03: check — build_correctly_encoded_bar_chart_from_categorical_summary_data (f1, f2)
s03_chart = choice(
    interaction_id="ix.tile_spreadsheet_chart_types.s03",
    difficulty="intro",
    measures=[{
        "concept_id": "spreadsheet.bar_chart_creation",
        "capability": "build_correctly_encoded_bar_chart_from_categorical_summary_data",
        "fact_ids": ["f1", "f2"]
    }],
    anchors=["spreadsheet.bar_chart_creation#assessment:build_correctly_encoded_bar_chart_from_categorical_summary_data"],
    prompt=(
        "You have a table with two columns: city and total_amount. "
        "You want to create a bar chart to compare total order amounts across cities. "
        "Which axis encoding is correct for a bar chart?"
    ),
    options=[
        {"option_id": "opt_a", "text": "Cities on the category axis; total_amount values represented by bar lengths on the value axis."},
        {"option_id": "opt_b", "text": "total_amount values on the category axis; cities represented by bar lengths on the value axis."},
        {"option_id": "opt_c", "text": "Cities on both axes, with total_amount shown as a colour gradient."},
        {"option_id": "opt_d", "text": "total_amount on both axes, with cities shown as data labels inside the bars."}
    ],
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": {"message": "In a bar chart, categories (like city names) go on the category axis, and numeric values (like total_amount) are represented by bar lengths on the value axis — not the other way around."},
        "opt_c": {"message": "Bar charts do not use colour gradients to encode values. The category axis holds the category labels (cities) and the value axis holds the numeric values (total_amount), shown as bar lengths."},
        "opt_d": {"message": "Both axes cannot hold the same type of data. The category axis holds category labels (cities) and the value axis holds numeric values (total_amount) represented by bar lengths."}
    },
    correct_msg="Correct! In a bar chart, categories (city names) are organised along the category axis and numeric values (total_amount) are represented by bar lengths along the value axis.",
    incorrect_msg="In a bar chart, categories go on the category axis and numeric values are shown as bar lengths on the value axis. Cities are the categories; total_amount is the value.",
    hints=[
        "A bar chart compares items: the items (categories) go on one axis, and their values (shown as bar lengths) go on the other.",
        "Ask yourself: what am I comparing? Those are the categories. What am I measuring? That is the value axis."
    ],
    remediation_step_id="tile_spreadsheet_chart_types.r01"
)

# s04: hands_on — bar_chart practice (f1, f2)
# SUM(B2:B7) on asset_city_totals = 99300.0
s04_chart = formula_entry(
    interaction_id="ix.tile_spreadsheet_chart_types.s04",
    difficulty="core",
    measures=[
        {
            "concept_id": "spreadsheet.bar_chart_creation",
            "capability": "identify_bar_chart_axis_encoding",
            "fact_ids": ["f1"]
        },
        {
            "concept_id": "spreadsheet.bar_chart_creation",
            "capability": "create_bar_chart_via_insert_recommended_charts",
            "fact_ids": ["f2"]
        }
    ],
    anchors=[
        "spreadsheet.bar_chart_creation#practice",
        "spreadsheet.bar_chart_creation#assessment:identify_bar_chart_axis_encoding",
        "spreadsheet.bar_chart_creation#assessment:create_bar_chart_via_insert_recommended_charts"
    ],
    prompt=(
        "The city_totals sheet has city names in column A (A2:A7) and total order amounts "
        "in column B (B2:B7). A bar chart of this data would place cities on the category axis "
        "and total amounts as bar lengths on the value axis. "
        "In cell C1, write a formula that returns the sum of all total_amount values in B2:B7 — "
        "the grand total that would appear in the chart's data range."
    ),
    asset_id="asset_city_totals",
    sheet_name="city_totals",
    target_cell="C1",
    allowed_functions=["SUM"],
    expected_value=99300.0,
    reference_formula="=SUM(B2:B7)",
    must_use_functions=["SUM"],
    correct_msg="Correct! =SUM(B2:B7) returns 99300 — the grand total of all city amounts. The bar chart would use B2:B7 as its value data, with each city's bar length proportional to its share of this total.",
    incorrect_msg="Use SUM with the total_amount range: =SUM(B2:B7). The city_totals sheet has 6 cities in rows 2 through 7.",
    hints=[
        "The total_amount values are in column B, rows 2 through 7 (one row per city).",
        "=SUM(B2:B7) adds up all six city totals."
    ],
    remediation_step_id="tile_spreadsheet_chart_types.r01"
)

# s07: check — identify_axis_roles_and_interval_suitability (f1)
s07_chart = choice(
    interaction_id="ix.tile_spreadsheet_chart_types.s07",
    difficulty="intro",
    measures=[{
        "concept_id": "spreadsheet.line_chart_creation",
        "capability": "identify_axis_roles_and_interval_suitability",
        "fact_ids": ["f1"]
    }],
    anchors=["spreadsheet.line_chart_creation#assessment:identify_axis_roles_and_interval_suitability"],
    prompt=(
        "Which of the following datasets is best suited for a line chart, and why?"
    ),
    options=[
        {"option_id": "opt_a", "text": "Monthly revenue totals for Jan through Jun 2024 — because the data is time-ordered at equal intervals, making a line chart ideal for showing the trend."},
        {"option_id": "opt_b", "text": "Total order amounts by city — because cities are categories and a line chart connects them with a line."},
        {"option_id": "opt_c", "text": "A single order's delivery time — because a line chart can show a single data point."},
        {"option_id": "opt_d", "text": "Driver names and their order counts — because a line chart works for any two-column dataset."}
    ],
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": {"message": "Cities are unordered categories, not time-ordered intervals. A line connecting unordered categories implies a trend that does not exist. A bar chart is better for comparing city totals."},
        "opt_c": {"message": "A single data point cannot show a trend. Line charts are suited to continuous data over time at equal intervals — multiple points that form a meaningful sequence."},
        "opt_d": {"message": "Driver names are unordered categories, not time-ordered intervals. Connecting them with a line would imply a trend that does not exist. A bar chart is more appropriate."}
    },
    correct_msg="Correct! Monthly revenue at equal time intervals (Jan, Feb, Mar…) is exactly the kind of data a line chart is designed for — it shows the trend across evenly spaced time points.",
    incorrect_msg="Line charts are suited to continuous data over time at equal intervals (months, quarters, years). Unordered categories like cities or driver names should use a bar chart instead.",
    hints=[
        "Ask: is the horizontal axis a time sequence with equal spacing? If yes, a line chart works well.",
        "A line connecting unordered categories (like cities) implies a trend that does not exist — that is a misuse of a line chart."
    ],
    remediation_step_id="tile_spreadsheet_chart_types.r02"
)

# s08: check — build_correctly_encoded_line_chart_from_time_ordered_data (f1, f2)
s08_chart = choice(
    interaction_id="ix.tile_spreadsheet_chart_types.s08",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.line_chart_creation",
        "capability": "build_correctly_encoded_line_chart_from_time_ordered_data",
        "fact_ids": ["f1", "f2"]
    }],
    anchors=["spreadsheet.line_chart_creation#assessment:build_correctly_encoded_line_chart_from_time_ordered_data"],
    prompt=(
        "You have monthly revenue data: month labels in column A (Jan-2024 through Jun-2024) "
        "and total amounts in column B. You create a line chart using Insert > Recommended Charts. "
        "Which statement correctly describes the resulting chart?"
    ),
    options=[
        {"option_id": "opt_a", "text": "Month labels are distributed evenly along the horizontal axis; revenue values are plotted on the vertical axis, connected by a line showing the trend over time."},
        {"option_id": "opt_b", "text": "Revenue values are distributed along the horizontal axis; month labels appear on the vertical axis."},
        {"option_id": "opt_c", "text": "Both axes show revenue values; month labels appear as data point labels on the line."},
        {"option_id": "opt_d", "text": "The chart shows bars instead of a line because monthly data always produces a bar chart."}
    ],
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": {"message": "In a line chart, category data (month labels) is distributed along the horizontal axis and value data (revenue) is plotted on the vertical axis — not the other way around."},
        "opt_c": {"message": "The horizontal axis holds category data (month labels), not revenue values. Revenue values are plotted on the vertical axis."},
        "opt_d": {"message": "Monthly data does not automatically produce a bar chart. When you select the data and use Insert > Recommended Charts, Excel recommends a line chart for evenly spaced time-series data."}
    },
    correct_msg="Correct! In a line chart, category data (month labels) is distributed evenly along the horizontal axis and value data (revenue) is plotted on the vertical axis, with points connected by a line.",
    incorrect_msg="In a line chart, the horizontal axis holds the category data (month labels) evenly spaced, and the vertical axis holds the value data (revenue). The line connects the data points to show the trend.",
    hints=[
        "Remember: horizontal axis = category data (months); vertical axis = value data (revenue).",
        "The line connects the data points in order, showing how revenue changes from month to month."
    ],
    remediation_step_id="tile_spreadsheet_chart_types.r02"
)

# s09: hands_on — line_chart practice (f2)
# SUM(B2:B7) on asset_monthly_summary = 1976900.0
s09_chart = formula_entry(
    interaction_id="ix.tile_spreadsheet_chart_types.s09",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.line_chart_creation",
        "capability": "create_line_chart_via_insert_recommended_charts",
        "fact_ids": ["f2"]
    }],
    anchors=[
        "spreadsheet.line_chart_creation#practice",
        "spreadsheet.line_chart_creation#assessment:create_line_chart_via_insert_recommended_charts"
    ],
    prompt=(
        "The monthly_summary sheet has month labels in column A (A2:A7, Jan-2024 through Jun-2024) "
        "and total order amounts in column B (B2:B7). A line chart of this data would place months "
        "evenly along the horizontal axis and revenue values on the vertical axis. "
        "In cell C1, write a formula that returns the sum of all monthly totals in B2:B7 — "
        "the grand total across all six months."
    ),
    asset_id="asset_monthly_summary",
    sheet_name="monthly_summary",
    target_cell="C1",
    allowed_functions=["SUM"],
    expected_value=1976900.0,
    reference_formula="=SUM(B2:B7)",
    must_use_functions=["SUM"],
    correct_msg="Correct! =SUM(B2:B7) returns 1976900 — the total revenue across all six months. The line chart would use B2:B7 as its value data, with each month's point plotted on the vertical axis.",
    incorrect_msg="Use SUM with the total_amount range: =SUM(B2:B7). The monthly_summary sheet has 6 months in rows 2 through 7.",
    hints=[
        "The total_amount values are in column B, rows 2 through 7 (one row per month).",
        "=SUM(B2:B7) adds up all six monthly totals."
    ],
    remediation_step_id="tile_spreadsheet_chart_types.r02"
)

# s12: check — build_correctly_encoded_pie_chart_from_category_totals (f1, f2)
s12_chart = choice(
    interaction_id="ix.tile_spreadsheet_chart_types.s12",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.pie_chart_creation",
        "capability": "build_correctly_encoded_pie_chart_from_category_totals",
        "fact_ids": ["f1", "f2"]
    }],
    anchors=["spreadsheet.pie_chart_creation#assessment:build_correctly_encoded_pie_chart_from_category_totals"],
    prompt=(
        "You have city order totals for 6 cities, all amounts positive. "
        "You select the data and use Insert > Recommended Charts to create a pie chart. "
        "Which statement correctly describes the resulting chart?"
    ),
    options=[
        {"option_id": "opt_a", "text": "Each city appears as a slice; each slice's size is proportional to that city's share of the total amount; all slices together represent 100% of total revenue."},
        {"option_id": "opt_b", "text": "Each city appears as a bar; bar lengths represent the city's total amount; the chart shows absolute values, not proportions."},
        {"option_id": "opt_c", "text": "Each city appears as a point on a line; the line shows how city totals change from city to city."},
        {"option_id": "opt_d", "text": "Each city appears as a slice, but slices are equal in size because pie charts do not encode values."}
    ],
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": {"message": "That describes a bar chart, not a pie chart. A pie chart shows proportions: each slice's size represents that category's share of the whole, and all slices together equal 100%."},
        "opt_c": {"message": "That describes a line chart. A pie chart shows proportions as slices of a circle, not points on a line."},
        "opt_d": {"message": "Pie chart slices are not equal — they are sized proportionally to each category's value. A slice for Lagos (the largest city total) would be larger than a slice for Enugu (the smallest)."}
    },
    correct_msg="Correct! In a pie chart, each category is a slice sized proportionally to its share of the total. All slices together represent 100% of the data series.",
    incorrect_msg="A pie chart shows proportions: each slice represents one category's share of the whole, sized proportionally to its value. All slices together equal 100%.",
    hints=[
        "The key word for pie charts is 'proportional' — each slice's size shows that category's fraction of the total.",
        "All slices together must equal 100% of the data series — that is what makes it a 'pie'."
    ],
    remediation_step_id="tile_spreadsheet_chart_types.r03"
)

# s13: hands_on — pie_chart practice (f1, f2)
# COUNTA(A2:A7) on asset_city_totals = 6
s13_chart = formula_entry(
    interaction_id="ix.tile_spreadsheet_chart_types.s13",
    difficulty="stretch",
    measures=[
        {
            "concept_id": "spreadsheet.pie_chart_creation",
            "capability": "identify_pie_chart_eligibility_conditions",
            "fact_ids": ["f1"]
        },
        {
            "concept_id": "spreadsheet.pie_chart_creation",
            "capability": "build_correctly_encoded_pie_chart_from_category_totals",
            "fact_ids": ["f1", "f2"]
        }
    ],
    anchors=[
        "spreadsheet.pie_chart_creation#practice",
        "spreadsheet.pie_chart_creation#assessment:identify_pie_chart_eligibility_conditions",
        "spreadsheet.pie_chart_creation#assessment:build_correctly_encoded_pie_chart_from_category_totals"
    ],
    prompt=(
        "The city_totals sheet has city names in A2:A7 and total amounts in B2:B7. "
        "A pie chart is appropriate here because there is only one data series, all values are "
        "positive, and the number of categories does not exceed seven. "
        "In cell C1, write a formula that counts the number of city labels in A2:A7 — "
        "confirming that the category count is within the pie chart eligibility limit."
    ),
    asset_id="asset_city_totals",
    sheet_name="city_totals",
    target_cell="C1",
    allowed_functions=["COUNTA"],
    expected_value=6,
    reference_formula="=COUNTA(A2:A7)",
    must_use_functions=["COUNTA"],
    correct_msg="Correct! =COUNTA(A2:A7) returns 6 — there are 6 cities, which is within the seven-category limit for pie charts. With all positive values and a single data series, this dataset meets all pie chart eligibility conditions.",
    incorrect_msg="Use COUNTA to count the city labels in A2:A7: =COUNTA(A2:A7). COUNTA counts non-empty cells, including text labels.",
    hints=[
        "COUNTA counts all non-empty cells, including text. Use it to count the city names in A2:A7.",
        "The pie chart eligibility rule says no more than seven categories. COUNTA(A2:A7) tells you how many categories there are."
    ],
    remediation_step_id="tile_spreadsheet_chart_types.r03"
)

# ─────────────────────────────────────────────────────────────────────────────
# tile_spreadsheet_formatting_validation
# ─────────────────────────────────────────────────────────────────────────────

# s03: check — apply_conditional_formatting_rule_for_given_condition (f1, f2)
s03_fmt = choice(
    interaction_id="ix.tile_spreadsheet_formatting_validation.s03",
    difficulty="intro",
    measures=[{
        "concept_id": "spreadsheet.conditional_formatting",
        "capability": "apply_conditional_formatting_rule_for_given_condition",
        "fact_ids": ["f1", "f2"]
    }],
    anchors=["spreadsheet.conditional_formatting#assessment:apply_conditional_formatting_rule_for_given_condition"],
    prompt=(
        "You want to highlight all cells in the delivery_minutes column (C2:C21) that contain "
        "values below 30, using a red fill. Which sequence of steps achieves this?"
    ),
    options=[
        {"option_id": "opt_a", "text": "Select C2:C21 → Home → Conditional Formatting → Highlight Cells Rules → Less Than → enter 30 → choose a red fill format."},
        {"option_id": "opt_b", "text": "Select C2:C21 → Insert → Conditional Formatting → Less Than → enter 30 → choose a red fill format."},
        {"option_id": "opt_c", "text": "Select C2:C21 → Home → Format Cells → Conditional → Less Than → enter 30 → choose a red fill format."},
        {"option_id": "opt_d", "text": "Select C2:C21 → Data → Conditional Formatting → Highlight Cells Rules → Less Than → enter 30 → choose a red fill format."}
    ],
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": {"message": "Conditional Formatting is not on the Insert tab. It is on the Home tab, in the Styles group. The correct path is Home → Conditional Formatting → Highlight Cells Rules → Less Than."},
        "opt_c": {"message": "There is no Conditional option inside Format Cells. Conditional Formatting is a separate command on the Home tab: Home → Conditional Formatting → Highlight Cells Rules → Less Than."},
        "opt_d": {"message": "Conditional Formatting is not on the Data tab. It is on the Home tab, in the Styles group. The correct path is Home → Conditional Formatting → Highlight Cells Rules → Less Than."}
    },
    correct_msg="Correct! The path is Home → Conditional Formatting → Highlight Cells Rules → Less Than → enter 30 → choose the red fill format. The rule then applies the format automatically to any cell below 30.",
    incorrect_msg="Conditional Formatting is on the Home tab (not Insert or Data). The path is: Home → Conditional Formatting → Highlight Cells Rules → Less Than → enter the threshold → choose the format.",
    hints=[
        "Conditional Formatting lives on the Home tab, in the Styles group — not on Insert or Data.",
        "The Highlight Cells Rules submenu contains comparison commands like Less Than, Greater Than, and Equal To."
    ],
    remediation_step_id="tile_spreadsheet_formatting_validation.r01"
)

# s04: hands_on — conditional_formatting practice (f1, f2)
# COUNTIF(C2:C21,"<30") = 4 (rows where delivery_minutes < 30: 28, 19, 14, 29)
s04_fmt = formula_entry(
    interaction_id="ix.tile_spreadsheet_formatting_validation.s04",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.conditional_formatting",
        "capability": "apply_conditional_formatting_rule_for_given_condition",
        "fact_ids": ["f1", "f2"]
    }],
    anchors=[
        "spreadsheet.conditional_formatting#practice",
        "spreadsheet.conditional_formatting#assessment:apply_conditional_formatting_rule_for_given_condition"
    ],
    prompt=(
        "A conditional formatting rule highlights cells in C2:C21 where delivery_minutes is "
        "less than 30 with a red fill. In cell F1, write a formula that counts how many cells "
        "in C2:C21 satisfy that condition — that is, how many cells would be highlighted red. "
        "Use COUNTIF with the range C2:C21 and the criterion \"<30\"."
    ),
    asset_id="asset_orders_clean",
    sheet_name="Orders",
    target_cell="F1",
    allowed_functions=["COUNTIF"],
    expected_value=4,
    reference_formula='=COUNTIF(C2:C21,"<30")',
    must_use_functions=["COUNTIF"],
    correct_msg="Correct! =COUNTIF(C2:C21,\"<30\") returns 4 — there are 4 orders with delivery times below 30 minutes (28, 19, 14, and 29). Those 4 cells would be highlighted red by the conditional formatting rule.",
    incorrect_msg="Use COUNTIF with the delivery_minutes range and the criterion \"<30\": =COUNTIF(C2:C21,\"<30\"). The criterion must be in double quotes.",
    hints=[
        "COUNTIF takes two arguments: the range and the criterion. The criterion for 'less than 30' is \"<30\" (in double quotes).",
        "The formula is =COUNTIF(C2:C21,\"<30\"). Make sure the criterion is a text string with the comparison operator inside the quotes."
    ],
    remediation_step_id="tile_spreadsheet_formatting_validation.r01"
)

# s08: check — identify_data_validation_purpose + configure_numeric_validation (f1, f3)
s08_fmt = choice(
    interaction_id="ix.tile_spreadsheet_formatting_validation.s08",
    difficulty="intro",
    measures=[
        {
            "concept_id": "spreadsheet.data_validation",
            "capability": "identify_data_validation_purpose_and_error_message_behaviour",
            "fact_ids": ["f1"]
        },
        {
            "concept_id": "spreadsheet.data_validation",
            "capability": "configure_numeric_date_or_text_length_validation_with_condition_and_limits",
            "fact_ids": ["f3"]
        }
    ],
    anchors=[
        "spreadsheet.data_validation#assessment:identify_data_validation_purpose_and_error_message_behaviour",
        "spreadsheet.data_validation#assessment:configure_numeric_date_or_text_length_validation_with_condition_and_limits"
    ],
    prompt=(
        "You want to restrict the delivery_minutes column so that only whole numbers between "
        "1 and 300 can be entered. In the Data Validation dialog, which settings achieve this?"
    ),
    options=[
        {"option_id": "opt_a", "text": "Allow: Whole Number; Data: between; Minimum: 1; Maximum: 300."},
        {"option_id": "opt_b", "text": "Allow: Decimal; Data: between; Minimum: 1; Maximum: 300."},
        {"option_id": "opt_c", "text": "Allow: List; Source: 1,300."},
        {"option_id": "opt_d", "text": "Allow: Text Length; Data: between; Minimum: 1; Maximum: 300."}
    ],
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": {"message": "Decimal allows fractional numbers (e.g., 45.5). To restrict to whole numbers only, choose Whole Number, not Decimal."},
        "opt_c": {"message": "List creates a dropdown with specific values. To allow any whole number in a range, choose Whole Number with a between condition and set the minimum and maximum."},
        "opt_d": {"message": "Text Length restricts the number of characters in a text entry, not the numeric value. To restrict to whole numbers between 1 and 300, choose Whole Number with a between condition."}
    },
    correct_msg="Correct! Allow: Whole Number; Data: between; Minimum: 1; Maximum: 300 restricts the cell to whole numbers in that range. Any entry outside the range triggers the error message.",
    incorrect_msg="To allow only whole numbers between 1 and 300, set Allow to Whole Number, Data to between, Minimum to 1, and Maximum to 300.",
    hints=[
        "The Allow dropdown determines the type of data permitted. For whole numbers, choose Whole Number (not Decimal or Text Length).",
        "The Data dropdown sets the condition (between, greater than, less than, etc.). For a range, choose between and set the minimum and maximum."
    ],
    remediation_step_id="tile_spreadsheet_formatting_validation.r02"
)

# s09: check — select_correct_validation_type (f1, f2, f3)
s09_fmt = choice(
    interaction_id="ix.tile_spreadsheet_formatting_validation.s09",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.data_validation",
        "capability": "select_correct_validation_type_for_a_given_input_restriction_requirement",
        "fact_ids": ["f1", "f2", "f3"]
    }],
    anchors=["spreadsheet.data_validation#assessment:select_correct_validation_type_for_a_given_input_restriction_requirement"],
    prompt=(
        "A colleague wants to restrict the status column so that users can only enter one of "
        "three values: Delivered, Pending, or Cancelled. Which validation type should they choose?"
    ),
    options=[
        {"option_id": "opt_a", "text": "List — because it creates a dropdown with the exact allowed values, preventing any other entry."},
        {"option_id": "opt_b", "text": "Whole Number — because the status values can be coded as numbers (1, 2, 3)."},
        {"option_id": "opt_c", "text": "Text Length — because each status value has a specific character count."},
        {"option_id": "opt_d", "text": "Decimal — because status values can be represented as decimal codes."}
    ],
    correct_ids=["opt_a"],
    option_feedback={
        "opt_b": {"message": "Whole Number restricts entries to numeric values within a range. It cannot enforce specific text values like 'Delivered'. Use List to restrict entries to a fixed set of text options."},
        "opt_c": {"message": "Text Length restricts the number of characters, not the specific text. 'Delivered' (9 chars) and 'Cancelled' (9 chars) have the same length, so Text Length cannot distinguish between them. Use List instead."},
        "opt_d": {"message": "Decimal restricts entries to numeric values. It cannot enforce specific text values like 'Pending'. Use List to create a dropdown with the allowed text values."}
    },
    correct_msg="Correct! List validation creates a dropdown showing the allowed values (Delivered, Pending, Cancelled) and prevents any other entry. It is the right choice when you need to restrict input to a fixed set of text options.",
    incorrect_msg="When you need to restrict input to a fixed set of text values, use List validation. It creates a dropdown with the allowed options and blocks any other entry.",
    hints=[
        "List validation is designed for exactly this scenario: a fixed set of allowed values shown as a dropdown.",
        "Whole Number and Decimal are for numeric ranges; Text Length is for character counts. None of those can enforce specific text values."
    ],
    remediation_step_id="tile_spreadsheet_formatting_validation.r02"
)

# s10: hands_on — data_validation practice (f2)
# COUNTA(E2:E21) = 20 (all 20 rows have a status value)
s10_fmt = formula_entry(
    interaction_id="ix.tile_spreadsheet_formatting_validation.s10",
    difficulty="core",
    measures=[{
        "concept_id": "spreadsheet.data_validation",
        "capability": "configure_dropdown_list_validation_with_source_values",
        "fact_ids": ["f2"]
    }],
    anchors=[
        "spreadsheet.data_validation#practice",
        "spreadsheet.data_validation#assessment:configure_dropdown_list_validation_with_source_values"
    ],
    prompt=(
        "The status column (E2:E21) has a dropdown list validation rule that allows only "
        "Delivered, Pending, or Cancelled. Every cell in E2:E21 currently contains one of "
        "those three values. In cell F1, write a formula that counts how many non-empty cells "
        "are in E2:E21 — confirming that all 20 rows have a valid status entry. "
        "Use COUNTA with the range E2:E21."
    ),
    asset_id="asset_orders_clean",
    sheet_name="Orders",
    target_cell="F1",
    allowed_functions=["COUNTA"],
    expected_value=20,
    reference_formula="=COUNTA(E2:E21)",
    must_use_functions=["COUNTA"],
    correct_msg="Correct! =COUNTA(E2:E21) returns 20 — all 20 rows have a status value. With dropdown list validation applied to E2:E21, each of those values must be one of the three allowed options: Delivered, Pending, or Cancelled.",
    incorrect_msg="Use COUNTA to count non-empty cells in the status range: =COUNTA(E2:E21). COUNTA counts all non-empty cells, including text values.",
    hints=[
        "COUNTA counts all non-empty cells, including text. Use it to count the status values in E2:E21.",
        "The status column is column E, rows 2 through 21 (20 orders)."
    ],
    remediation_step_id="tile_spreadsheet_formatting_validation.r03"
)

# ─────────────────────────────────────────────────────────────────────────────
# Assemble the output
# ─────────────────────────────────────────────────────────────────────────────

doc = {
    "schema_version": "0.1.0",
    "kind": "interactions_part",
    "path_id": "data_analyst",
    "batch_id": "final_batch_011_da_spreadsheet",
    "tiles": [
        {
            "tile_id": "tile_spreadsheet_tables_named_ranges",
            "interactions": [
                {"step_id": "tile_spreadsheet_tables_named_ranges.s04", "interaction": s04_tables},
                {"step_id": "tile_spreadsheet_tables_named_ranges.s05", "interaction": s05_tables},
                {"step_id": "tile_spreadsheet_tables_named_ranges.s07", "interaction": s07_tables},
                {"step_id": "tile_spreadsheet_tables_named_ranges.s08", "interaction": s08_tables},
            ]
        },
        {
            "tile_id": "tile_spreadsheet_pivot_tables",
            "interactions": [
                {"step_id": "tile_spreadsheet_pivot_tables.s04", "interaction": s04_pivot},
                {"step_id": "tile_spreadsheet_pivot_tables.s05", "interaction": s05_pivot},
                {"step_id": "tile_spreadsheet_pivot_tables.s06", "interaction": s06_pivot},
                {"step_id": "tile_spreadsheet_pivot_tables.s09", "interaction": s09_pivot},
                {"step_id": "tile_spreadsheet_pivot_tables.s10", "interaction": s10_pivot},
            ]
        },
        {
            "tile_id": "tile_spreadsheet_chart_types",
            "interactions": [
                {"step_id": "tile_spreadsheet_chart_types.s03", "interaction": s03_chart},
                {"step_id": "tile_spreadsheet_chart_types.s04", "interaction": s04_chart},
                {"step_id": "tile_spreadsheet_chart_types.s07", "interaction": s07_chart},
                {"step_id": "tile_spreadsheet_chart_types.s08", "interaction": s08_chart},
                {"step_id": "tile_spreadsheet_chart_types.s09", "interaction": s09_chart},
                {"step_id": "tile_spreadsheet_chart_types.s12", "interaction": s12_chart},
                {"step_id": "tile_spreadsheet_chart_types.s13", "interaction": s13_chart},
            ]
        },
        {
            "tile_id": "tile_spreadsheet_formatting_validation",
            "interactions": [
                {"step_id": "tile_spreadsheet_formatting_validation.s03", "interaction": s03_fmt},
                {"step_id": "tile_spreadsheet_formatting_validation.s04", "interaction": s04_fmt},
                {"step_id": "tile_spreadsheet_formatting_validation.s08", "interaction": s08_fmt},
                {"step_id": "tile_spreadsheet_formatting_validation.s09", "interaction": s09_fmt},
                {"step_id": "tile_spreadsheet_formatting_validation.s10", "interaction": s10_fmt},
            ]
        }
    ]
}

with open(OUT, "w") as f:
    json.dump(doc, f, indent=2)

print(f"Written {OUT}")
total = sum(len(t["interactions"]) for t in doc["tiles"])
print(f"Total interactions: {total}")
for tile in doc["tiles"]:
    print(f"  {tile['tile_id']}: {len(tile['interactions'])} interactions")
