"""
Patch screens.part.c3.json:
- Update remediation step r01 to cover both f1 (.map(function)) and f2 (.map(dict)),
  so it is a valid remediation for s02 which tests pandas.map_substitution#f1.
- Change ONLY what the finding names; do not touch any other step.
"""
import json, copy

SRC = "batches/final_batch_009_da_pandas/screens.part.c3.json"

with open(SRC) as fh:
    doc = json.load(fh)

tile = next(t for t in doc["tiles"] if t["tile_id"] == "tile_pandas_map_apply")
rem_steps = tile["remediation_steps"]
r01 = next(s for s in rem_steps if s["step_id"] == "tile_pandas_map_apply.r01")

# ── Update title and lede to cover both function and dict ──────────────────
r01["title"] = "How .map() substitutes values — with a function or a dict"
r01["lede"] = (
    ".map() accepts either a Python function or a dict. "
    "When you pass a function it is called on every element; "
    "when you pass a dict each matching key is replaced by its value."
)

# ── Replace blocks: add a function-focused prose block (f1) before the
#    existing dict-focused before_after block (f2) ─────────────────────────
new_prose_f1 = {
    "type": "prose",
    "block_id": "tile_pandas_map_apply.r01.b0",
    "role": "definition",
    "text": (
        "`Series.map()` accepts a Python function that takes a single value "
        "and returns a single value, then applies it to every element of the "
        "Series. Define `def to_upper(code): return code.upper()` and call "
        "`orders[\"city_code\"].map(to_upper)` — every city code is "
        "uppercased in one pass, with no loop."
    ),
    "lineage": {
        "concept_ids": ["pandas.map_substitution"],
        "teaching_block_ids": ["pandas.map_substitution#tb1"],
        "fact_ids": ["pandas.map_substitution#f1"]
    }
}

# Existing b1 prose covers f2 (dict) — keep it, just update its text slightly
# to make the contrast with function explicit.
r01["blocks"][0]["text"] = (
    "`Series.map()` also accepts a **dict** as a mapping correspondence. "
    "Every element whose value matches a key is replaced by the corresponding "
    "dict value; elements with no matching key become `NaN`. "
    "Pass `{\"LOS\": \"Lagos\", \"ABJ\": \"Abuja\", \"KAN\": \"Kano\"}` to "
    "replace three-letter city codes with full names in one call."
)

# Insert the new f1 prose block at position 0
r01["blocks"].insert(0, new_prose_f1)

# ── Update step-level lineage to include both f1 and f2 ───────────────────
r01["lineage"]["teaching_block_ids"] = [
    "pandas.map_substitution#tb1",
    "pandas.map_substitution#tb2"
]
r01["lineage"]["fact_ids"] = [
    "pandas.map_substitution#f1",
    "pandas.map_substitution#f2"
]

with open(SRC, "w") as fh:
    json.dump(doc, fh, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
