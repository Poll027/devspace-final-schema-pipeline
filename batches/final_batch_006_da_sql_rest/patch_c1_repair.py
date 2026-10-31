"""
Patch interactions.part.c1.json:
1. Fix fact_ids in measures: strip the concept_id# prefix (e.g. sql.aggregate_functions#f2 -> f2)
2. Fix remediation_step_id: replace invalid step IDs (s01, s06, s10) with valid r-step IDs
"""
import json, re

PATH = "batches/final_batch_006_da_sql_rest/interactions.part.c1.json"

with open(PATH) as f:
    data = json.load(f)

# ---- 1. Fix fact_ids in measures ----
# fact_ids should be just "f1", "f2", etc. not "concept_id#f1"
for tile in data["tiles"]:
    for ix_entry in tile["interactions"]:
        ix = ix_entry["interaction"]
        for m in ix.get("measures", []):
            cid = m["concept_id"]
            prefix = cid + "#"
            fixed = []
            for fid in m.get("fact_ids", []):
                if fid.startswith(prefix):
                    fixed.append(fid[len(prefix):])
                else:
                    fixed.append(fid)
            m["fact_ids"] = fixed

# ---- 2. Fix remediation_step_id ----
# Map from invalid step IDs to valid remediation step IDs
# tile_sql_fund_aggregating_data:
#   r01 teaches sql.aggregate_functions#f2
#   r02 teaches sql.aggregate_functions#f3,f4,f5,f6
#   r03 teaches sql.group_by#f2
#   r04 teaches sql.having#f2
# tile_sql_case_expressions:
#   r01 teaches sql.case_expressions#f1
#   r02 teaches sql.case_expressions#f2

# Build a per-step remediation mapping based on what each step measures
STEP_REMEDIATION = {
    # tile_sql_fund_aggregating_data
    "tile_sql_fund_aggregating_data.s03": "tile_sql_fund_aggregating_data.r01",  # measures agg#f2
    "tile_sql_fund_aggregating_data.s04": "tile_sql_fund_aggregating_data.r02",  # measures agg#f3-f6
    "tile_sql_fund_aggregating_data.s05": "tile_sql_fund_aggregating_data.r01",  # measures agg#f1, closest is r01
    "tile_sql_fund_aggregating_data.s08": "tile_sql_fund_aggregating_data.r03",  # measures group_by#f2
    "tile_sql_fund_aggregating_data.s09": "tile_sql_fund_aggregating_data.r03",  # measures group_by#f1, closest is r03
    "tile_sql_fund_aggregating_data.s12": "tile_sql_fund_aggregating_data.r04",  # measures having#f2
    "tile_sql_fund_aggregating_data.s13": "tile_sql_fund_aggregating_data.r04",  # measures having#f1,f2
    # tile_sql_case_expressions
    "tile_sql_case_expressions.s03": "tile_sql_case_expressions.r01",  # measures case#f1
    "tile_sql_case_expressions.s04": "tile_sql_case_expressions.r02",  # measures case#f3, closest is r02
    "tile_sql_case_expressions.s05": "tile_sql_case_expressions.r02",  # measures case#f2
}

for tile in data["tiles"]:
    for ix_entry in tile["interactions"]:
        sid = ix_entry["step_id"]
        ix = ix_entry["interaction"]
        fb = ix.get("feedback", {})
        if sid in STEP_REMEDIATION:
            fb["remediation_step_id"] = STEP_REMEDIATION[sid]

with open(PATH, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")

# Verify
with open(PATH) as f:
    data2 = json.load(f)

print("\nVerification - measures fact_ids and remediation_step_ids:")
for tile in data2["tiles"]:
    tid = tile["tile_id"]
    if tid in ["tile_sql_fund_aggregating_data", "tile_sql_case_expressions"]:
        print(f"\n=== {tid} ===")
        for ix_entry in tile["interactions"]:
            sid = ix_entry["step_id"]
            ix = ix_entry["interaction"]
            for m in ix.get("measures", []):
                print(f"  {sid}: concept={m['concept_id']}, fact_ids={m['fact_ids']}")
            fb = ix.get("feedback", {})
            rem = fb.get("remediation_step_id")
            if rem:
                print(f"  {sid}: remediation_step_id={rem}")
