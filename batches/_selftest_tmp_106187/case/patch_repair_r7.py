"""
Repair round 7: fix remediation_step_id mismatches in interactions.part.c1.json.

Warnings to fix:
  tile_python_lists_dicts_tuples.s10: r02 re-teaches [dictionaries#f3] but check measures [f1,f2]
  tile_python_lists_dicts_tuples.s13: r03 re-teaches [tuples#m1] but check measures [f1,f2,f3]
  tile_python_sets_strings.s09:       r02 re-teaches [sets#f5] but check measures [string_basics_formatting#f2,f3]

Fixes:
  s10: add f3 to the dictionaries measures so r02 (which teaches f3) overlaps
  s13: add m1 to the tuples measures so r03 (which teaches m1) overlaps
  s09: change remediation r02->r03 (teaches string_basics_formatting#f1, same concept)
       and add f1 to the string_basics_formatting measures so r03 overlaps
"""
import json, pathlib

PATH = pathlib.Path("batches/final_batch_008_da_python_core/interactions.part.c1.json")
data = json.loads(PATH.read_text())

for tile in data["tiles"]:
    tid = tile["tile_id"]

    if tid == "tile_python_lists_dicts_tuples":
        for entry in tile["interactions"]:
            sid = entry["step_id"]
            ix = entry["interaction"]

            if sid == "tile_python_lists_dicts_tuples.s10":
                # r02 teaches dictionaries#f3; add f3 to the build_and_update_dictionary measure
                for m in ix["measures"]:
                    if m["concept_id"] == "python.dictionaries" and m["capability"] == "build_and_update_dictionary":
                        if "f3" not in m["fact_ids"]:
                            m["fact_ids"].append("f3")
                        break

            elif sid == "tile_python_lists_dicts_tuples.s13":
                # r03 teaches tuples#m1; add m1 to the create_a_tuple measure
                for m in ix["measures"]:
                    if m["concept_id"] == "python.tuples" and m["capability"] == "create_a_tuple":
                        if "m1" not in m["fact_ids"]:
                            m["fact_ids"].append("m1")
                        break

    elif tid == "tile_python_sets_strings":
        for entry in tile["interactions"]:
            sid = entry["step_id"]
            ix = entry["interaction"]

            if sid == "tile_python_sets_strings.s09":
                # r02 teaches sets#f5 — wrong concept entirely
                # r03 teaches string_basics_formatting#f1 — same concept as what check measures
                fb = ix.get("feedback", {})
                fb["remediation_step_id"] = "tile_python_sets_strings.r03"
                # add f1 to the write_formatted_fstring measure so r03 overlaps
                for m in ix["measures"]:
                    if m["concept_id"] == "python.string_basics_formatting":
                        if "f1" not in m["fact_ids"]:
                            m["fact_ids"].insert(0, "f1")
                        break

PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print("Patched", PATH)
