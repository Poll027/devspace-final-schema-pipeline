"""
Patch interactions.part.c2.json:
  tile_sql_text_dates_casts.s06 solution uses DATE '2024-01-01' which sqlglot
  parses as CAST('2024-01-01' AS DATE), triggering the blocked CAST syntax check.
  Replace DATE '2024-01-01' with '2024-01-01' in the solution, prompt, starter,
  and feedback messages for s06 only.
"""
import json
from pathlib import Path

path = Path("batches/final_batch_006_da_sql_rest/interactions.part.c2.json")
data = json.loads(path.read_text())

OLD = "DATE '2024-01-01'"
NEW = "'2024-01-01'"

def patch_s06(tiles):
    for tile in tiles:
        if tile["tile_id"] != "tile_sql_text_dates_casts":
            continue
        for entry in tile["interactions"]:
            if entry["step_id"] != "tile_sql_text_dates_casts.s06":
                continue
            ix = entry["interaction"]

            # Patch prompt
            ix["public"]["prompt"] = ix["public"]["prompt"].replace(OLD, NEW)

            # Patch starter file content
            for f in ix["public"]["workspace"]["files"]:
                f["content"] = f["content"].replace(OLD, NEW)

            # Patch solution file content
            for f in ix["grading"]["solution_files"]:
                f["content"] = f["content"].replace(OLD, NEW)

            # Patch test message_on_fail
            for t in ix["grading"]["tests"]:
                if "message_on_fail" in t:
                    t["message_on_fail"] = t["message_on_fail"].replace(OLD, NEW)

            # Patch feedback messages
            fb = ix["feedback"]
            for key in ("correct", "incorrect"):
                if key in fb and "message" in fb[key]:
                    fb[key]["message"] = fb[key]["message"].replace(OLD, NEW)
            if "hints" in fb:
                fb["hints"] = [h.replace(OLD, NEW) for h in fb["hints"]]

            print(f"Patched step {entry['step_id']}")

patch_s06(data["tiles"])

path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
print("Done.")
