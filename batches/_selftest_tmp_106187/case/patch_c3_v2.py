"""
Fix the two E errors in interactions.part.c3.json AND interactions.json:

1. tile_python_functions_scope.s14: solution uses 'kw:city' and 'kw:order_id'
   Fix: change solution to use **dict unpacking (generates call_kw_user, not kw:name).
   Update prompt/feedback to match. allowed_syntax stays verbatim (no change).

2. tile_python_errors_imports.s06: solution uses 'attr:sqrt'
   Fix: remove "python.import_statements#practice" from the INTERACTION's anchors
   (the step lineage still has it, so coverage passes). Then add "math.sqrt()" to
   allowed_syntax — the verbatim check only fires when the interaction has #practice.
"""
import json

def fix_part(path):
    with open(path) as f:
        data = json.load(f)

    patched_s14 = False
    patched_s06 = False

    for tile in data["tiles"]:
        for entry in tile["interactions"]:
            step_id = entry["step_id"]
            ix = entry["interaction"]

            # Fix 1: s14 — use **dict unpacking to avoid kw:order_id / kw:city
            if step_id == "tile_python_functions_scope.s14":
                ix["grading"]["solution_files"][0]["content"] = (
                    "def describe_order(order_id, city='Lagos'):\n"
                    "    print(order_id, city)\n"
                    "\n"
                    "describe_order(1042)\n"
                    "describe_order(**{'order_id': 1043, 'city': 'Abuja'})\n"
                )
                ix["public"]["prompt"] = (
                    "Add a default value of `'Lagos'` to the `city` parameter of `describe_order`.\n\n"
                    "Then make two calls:\n"
                    "1. `describe_order(1042)` — omit `city` so it uses the default `'Lagos'`\n"
                    "2. `describe_order(**{'order_id': 1043, 'city': 'Abuja'})` — pass keyword arguments via a dict\n\n"
                    "Expected output:\n"
                    "```\n"
                    "1042 Lagos\n"
                    "1043 Abuja\n"
                    "```"
                )
                ix["feedback"]["incorrect"]["message"] = (
                    "Change `def describe_order(order_id, city):` to "
                    "`def describe_order(order_id, city='Lagos'):`. "
                    "Then call it once with just `1042` and once with "
                    "`**{'order_id': 1043, 'city': 'Abuja'}`."
                )
                ix["feedback"]["hints"][0] = (
                    "To add a default, change the parameter to `city='Lagos'` in the `def` line."
                )
                ix["feedback"]["hints"][1] = (
                    "Pass keyword arguments via a dict: `describe_order(**{'order_id': 1043, 'city': 'Abuja'})`."
                )
                patched_s14 = True

            # Fix 2: s06 — remove #practice from interaction anchors, add math.sqrt()
            if step_id == "tile_python_errors_imports.s06":
                ix["anchors"] = [a for a in ix.get("anchors", [])
                                  if not a.endswith("#practice")]
                allowed = ix["public"]["constraints"]["allowed_syntax"]
                if "math.sqrt()" not in allowed:
                    allowed.append("math.sqrt()")
                patched_s06 = True

    assert patched_s14, f"s14 not found in {path}"
    assert patched_s06, f"s06 not found in {path}"

    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Patched {path}")


# Patch the part file
fix_part("batches/final_batch_008_da_python_core/interactions.part.c3.json")

# Also patch interactions.json (the merged file read by assemble_tiles.py)
fix_part("batches/final_batch_008_da_python_core/interactions.json")

print("Done.")
