"""
Repair round 6: fix remediation_step_id mismatches in interactions.part.c1.json.

Warnings to fix:
  tile_python_lists_dicts_tuples.s10: r02 re-teaches [dictionaries#f3] but check measures [f1,f2]
  tile_python_lists_dicts_tuples.s13: r03 re-teaches [tuples#m1] but check measures [f1,f2,f3]
  tile_python_sets_strings.s09:       r02 re-teaches [sets#f5] but check measures [string_basics_formatting#f2,f3]

Fixes:
  s10 (lists_dicts_tuples): remove remediation_step_id  (r02 still referenced by s09)
  s13 (lists_dicts_tuples): remove remediation_step_id  (r03 still referenced by s12)
  s09 (sets_strings):       change r02 -> r03           (r03 teaches string_basics_formatting#f1,
                                                          same concept; r02 moved to s05 which
                                                          measures sets#f5 == what r02 teaches)
"""
import json, pathlib

PATH = pathlib.Path("batches/final_batch_008_da_python_core/interactions.part.c1.json")
data = json.loads(PATH.read_text())

for tile in data["tiles"]:
    tid = tile["tile_id"]

    if tid == "tile_python_lists_dicts_tuples":
        for entry in tile["interactions"]:
            sid = entry["step_id"]
            fb = entry["interaction"].get("feedback", {})
            if sid == "tile_python_lists_dicts_tuples.s10":
                # r02 teaches dictionaries#f3; check measures f1,f2 → no overlap → remove
                fb.pop("remediation_step_id", None)
            elif sid == "tile_python_lists_dicts_tuples.s13":
                # r03 teaches tuples#m1; check measures f1,f2,f3 → no overlap → remove
                fb.pop("remediation_step_id", None)

    elif tid == "tile_python_sets_strings":
        for entry in tile["interactions"]:
            sid = entry["step_id"]
            fb = entry["interaction"].get("feedback", {})
            if sid == "tile_python_sets_strings.s09":
                # r02 teaches sets#f5; check measures string_basics_formatting#f2,f3 → wrong concept
                # r03 teaches string_basics_formatting#f1 → same concept, closest available
                fb["remediation_step_id"] = "tile_python_sets_strings.r03"
            elif sid == "tile_python_sets_strings.s05":
                # s05 measures sets#f5; r02 teaches sets#f5 → perfect overlap
                # add r02 here so it stays referenced after s09 no longer points to it
                fb["remediation_step_id"] = "tile_python_sets_strings.r02"

PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))
print("Patched", PATH)
