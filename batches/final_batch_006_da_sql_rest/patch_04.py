import json

path = "batches/final_batch_006_da_sql_rest/interactions.part.c1.json"

with open(path) as f:
    data = json.load(f)

# ── BLOCKING: tile_sql_fund_aggregating_data / s13 ──────────────────────────
for tile in data["tiles"]:
    if tile["tile_id"] != "tile_sql_fund_aggregating_data":
        continue
    for entry in tile["interactions"]:
        if entry["step_id"] != "tile_sql_fund_aggregating_data.s13":
            continue
        ix = entry["interaction"]

        # 1. Starter file comment: change 10000 → 20000
        for f_obj in ix["public"]["workspace"]["files"]:
            if f_obj["path"] == "query.sql":
                f_obj["content"] = f_obj["content"].replace(
                    "exceeds 10000", "exceeds 20000"
                )

        # 2. Solution: change HAVING threshold 10000 → 20000
        for sf in ix["grading"]["solution_files"]:
            if sf["path"] == "query.sql":
                sf["content"] = sf["content"].replace(
                    "HAVING SUM(amount) > 10000",
                    "HAVING SUM(amount) > 20000"
                )

        # 3. Expected rows: remove "other" (11150), keep north and south
        for test in ix["grading"]["tests"]:
            if test["test_id"] == "ix.tile_sql_fund_aggregating_data.s13.t1":
                test["spec"]["expected"]["rows"] = [
                    ["north", 24950.0],
                    ["south", 33300.0]
                ]

        # 4. message_on_fail: change 10000 → 20000
        for test in ix["grading"]["tests"]:
            test["message_on_fail"] = test["message_on_fail"].replace(
                "above 10000", "above 20000"
            )

        # 5. feedback messages: change 10000 → 20000 (feedback values are dicts with "message")
        fb = ix["feedback"]
        fb["incorrect"]["message"] = fb["incorrect"]["message"].replace(
            "HAVING SUM(amount) > 10000", "HAVING SUM(amount) > 20000"
        )
        fb["hints"] = [
            h.replace("HAVING SUM(amount) > 10000", "HAVING SUM(amount) > 20000")
            for h in fb["hints"]
        ]

        print("Patched s13 HAVING threshold and expected rows.")

# ── ADVISORY: tile_sql_case_expressions / s05 feedback.correct ──────────────
for tile in data["tiles"]:
    if tile["tile_id"] != "tile_sql_case_expressions":
        continue
    for entry in tile["interactions"]:
        if entry["step_id"] != "tile_sql_case_expressions.s05":
            continue
        ix = entry["interaction"]
        ix["feedback"]["correct"]["message"] = ix["feedback"]["correct"]["message"].replace(
            "ELSE catching everything above 7000",
            "ELSE catching every amount of 7000 or above"
        )
        print("Patched s05 ELSE feedback.")

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Done.")
