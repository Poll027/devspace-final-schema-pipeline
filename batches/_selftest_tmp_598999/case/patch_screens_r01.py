"""
Patch screens.part.c1.json:
  tile_pandas_creating_inspecting.r01 — update to cover BOTH dict_of_lists (f1)
  and list_of_dicts (f2), since s04 hands-on tests both construction methods.
  The title, lede, prose text, and lineage are updated accordingly.
"""
import json, copy

PATH = "batches/final_batch_009_da_pandas/screens.part.c1.json"

with open(PATH) as f:
    data = json.load(f)

tile = next(t for t in data["tiles"] if t["tile_id"] == "tile_pandas_creating_inspecting")
rem_steps = tile["remediation_steps"]
r01 = next(s for s in rem_steps if s["step_id"] == "tile_pandas_creating_inspecting.r01")

# Update title and lede to cover both construction methods
r01["title"] = "Two ways to build a DataFrame: dict of lists and list of dicts"
r01["lede"] = (
    "Use `pd.DataFrame(dict_of_lists)` to build df1 and "
    "`pd.DataFrame(list_of_dicts)` to build df2, then print both."
)

# Update the prose block to cover both f1 and f2
r01["blocks"][0]["text"] = (
    "Pass a **dict of equal-length lists** to `pd.DataFrame()` and each key becomes a column: "
    "`df1 = pd.DataFrame(dict_of_lists)`. "
    "Pass a **list of dicts** and each dict becomes one row: "
    "`df2 = pd.DataFrame(list_of_dicts)`. "
    "Both calls produce a DataFrame with the same columns \u2014 "
    "the difference is only the shape of the Python data you start with. "
    "After each call, `print(df1)` and `print(df2)` to confirm the result."
)
r01["blocks"][0]["lineage"]["teaching_block_ids"] = [
    "pandas.creating_dataframes#tb2",
    "pandas.creating_dataframes#tb3"
]
r01["blocks"][0]["lineage"]["fact_ids"] = [
    "pandas.creating_dataframes#f1",
    "pandas.creating_dataframes#f2"
]

# Update step-level lineage
r01["lineage"]["teaching_block_ids"] = [
    "pandas.creating_dataframes#tb2",
    "pandas.creating_dataframes#tb3"
]
r01["lineage"]["fact_ids"] = [
    "pandas.creating_dataframes#f1",
    "pandas.creating_dataframes#f2"
]

with open(PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patched r01 successfully.")
