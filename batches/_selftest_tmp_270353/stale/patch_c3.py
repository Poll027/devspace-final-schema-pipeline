"""
Patch interactions.part.c3.json per evaluator findings.
"""
import json, copy

path = "batches/final_batch_011_da_spreadsheet/interactions.part.c3.json"

with open(path) as f:
    data = json.load(f)

def find_interaction(data, step_id):
    for tile in data["tiles"]:
        for item in tile["interactions"]:
            if item["step_id"] == step_id:
                return item["interaction"]
    raise KeyError(f"step_id not found: {step_id}")

# ─────────────────────────────────────────────────────────────────────────────
# BLOCKING: tile_spreadsheet_tables_named_ranges/s08
# Change prompt and feedback.correct
# ─────────────────────────────────────────────────────────────────────────────
ix_s08 = find_interaction(data, "tile_spreadsheet_tables_named_ranges.s08")

ix_s08["public"]["prompt"] = (
    "In cell G1, write a formula using SUM to return the total of all "
    "delivery_minutes values in C2:C21. After defining a named range, you "
    "could replace C2:C21 with DeliveryTimes \u2014 but for this exercise, "
    "use the cell range directly: =SUM(C2:C21)."
)

ix_s08["feedback"]["correct"]["message"] = (
    "Correct! =SUM(C2:C21) returns 541. Once you define a named range "
    "DeliveryTimes for C2:C21, you could write =SUM(DeliveryTimes) for "
    "the same result."
)

# ─────────────────────────────────────────────────────────────────────────────
# ADVISORY: tile_spreadsheet_tables_named_ranges/s05
# Change hint 1 and hint 2
# ─────────────────────────────────────────────────────────────────────────────
ix_s05 = find_interaction(data, "tile_spreadsheet_tables_named_ranges.s05")

ix_s05["feedback"]["hints"][0] = (
    "The amount values are in column D, rows 2 through 21. Use =SUM(D2:D21)."
)
ix_s05["feedback"]["hints"][1] = (
    "In a structured table, this same formula could be written as "
    "=SUM(Orders[amount]) \u2014 but for this exercise, use the cell range."
)

# ─────────────────────────────────────────────────────────────────────────────
# ADVISORY: tile_spreadsheet_formatting_validation/s04
# Note in prompt that COUNTIF is previewed here and will be covered fully later
# ─────────────────────────────────────────────────────────────────────────────
ix_fv_s04 = find_interaction(data, "tile_spreadsheet_formatting_validation.s04")

ix_fv_s04["public"]["prompt"] = (
    "A conditional formatting rule highlights cells in C2:C21 where "
    "delivery_minutes is less than 30 with a red fill. In cell F1, write a "
    "formula that counts how many cells in C2:C21 satisfy that condition \u2014 "
    "that is, how many cells would be highlighted red. Use COUNTIF with the "
    "range C2:C21 and the criterion \"<30\". (Note: COUNTIF is previewed here "
    "to reinforce the conditional formatting concept; it will be covered fully "
    "in a later lesson on conditional aggregation.)"
)

# ─────────────────────────────────────────────────────────────────────────────
# ADVISORY: tile_spreadsheet_pivot_tables/s06
# Note in prompt that SUMIF is previewed here and will be covered fully later
# ─────────────────────────────────────────────────────────────────────────────
ix_pt_s06 = find_interaction(data, "tile_spreadsheet_pivot_tables.s06")

ix_pt_s06["public"]["prompt"] = (
    "A PivotTable with city in the Rows area and amount in the Values area "
    "would show the total amount for each city. In cell F1, write a formula "
    "that returns the total amount for Lagos orders \u2014 the value that would "
    "appear in the Lagos row of that PivotTable. Use SUMIF with the city range "
    "B2:B21, the criterion \"Lagos\", and the amount range D2:D21. (Note: SUMIF "
    "is previewed here to connect the PivotTable concept to a formula "
    "equivalent; it will be covered fully in a later lesson on conditional "
    "aggregation.)"
)

# ─────────────────────────────────────────────────────────────────────────────
# ADVISORY: tile_spreadsheet_chart_types/s09
# r02 re-teaches B.f1 but s09 measures B.f2 — add B.f2 content to r02 note
# The remediation_step_id points to tile_spreadsheet_chart_types.r02
# We cannot change the registry, but we can add a note in the incorrect
# feedback to address the tested fact (B.f2: create_line_chart_via_insert_recommended_charts)
# The advisory says "consider adding B.f2 content to r02 or changing the remediation pointer"
# Since we cannot edit registry/r02, we add a note in the incorrect feedback
# that covers the tested fact.
# ─────────────────────────────────────────────────────────────────────────────
ix_ct_s09 = find_interaction(data, "tile_spreadsheet_chart_types.s09")

# The advisory says to add B.f2 content to r02 or change the remediation pointer.
# r02 is a remediation step in the tile plan — we can only change what's in this
# artifact. The remediation_step_id field points to a step; we can change it to
# point to a more relevant remediation step if one exists, or add a note.
# Since we can only reword/delete/move/cite (advisory), we update the incorrect
# feedback to include the key fact about inserting a line chart (B.f2).
ix_ct_s09["feedback"]["incorrect"]["message"] = (
    "Use SUM with the total_amount range: =SUM(B2:B7). The monthly_summary "
    "sheet has 6 months in rows 2 through 7. To create a line chart from this "
    "data, select A1:B7, then go to Insert \u2192 Recommended Charts and choose "
    "the Line chart option."
)

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
