import json, sys

path = "batches/final_batch_006_da_sql_rest/interactions.part.c1.json"

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

changes = []

for tile in data["tiles"]:
    for item in tile["interactions"]:
        step_id = item["step_id"]
        ix = item["interaction"]

        # BLOCKING: tile_sql_fund_aggregating_data/s13
        # Change prompt from "exceeds 10 000 NGN" to "exceeds 20 000 NGN"
        if step_id == "tile_sql_fund_aggregating_data.s13":
            old_prompt = ix["public"]["prompt"]
            new_prompt = old_prompt.replace(
                "exceeds 10 000 NGN",
                "exceeds 20 000 NGN"
            )
            if new_prompt != old_prompt:
                ix["public"]["prompt"] = new_prompt
                changes.append(f"s13 prompt: replaced '10 000 NGN' with '20 000 NGN'")
            else:
                changes.append(f"WARNING: s13 prompt replacement did not match!")

        # ADVISORY: tile_sql_fund_aggregating_data/s05
        # Add "in that column order" to pin column order
        if step_id == "tile_sql_fund_aggregating_data.s05":
            old_prompt = ix["public"]["prompt"]
            # The prompt currently ends with "across all orders in the `orders` table."
            # We need to add a note that total_amount should come first
            new_prompt = old_prompt.replace(
                "the **total order value** (alias `total_amount`) and the **average order value** (alias `avg_amount`) across all orders in the `orders` table.",
                "the **total order value** (alias `total_amount`) and the **average order value** (alias `avg_amount`) across all orders in the `orders` table, in that column order (`total_amount` first)."
            )
            if new_prompt != old_prompt:
                ix["public"]["prompt"] = new_prompt
                changes.append(f"s05 (aggregating_data) prompt: added column order note")
            else:
                changes.append(f"WARNING: s05 aggregating_data prompt replacement did not match!")

        # ADVISORY: tile_sql_case_expressions/s05
        # Rephrase correct feedback about ELSE
        if step_id == "tile_sql_case_expressions.s05":
            old_msg = ix["feedback"]["correct"]["message"]
            new_msg = old_msg.replace(
                "with ELSE catching every amount of 7000 or above.",
                "with ELSE catching every row whose amount did not match any WHEN — here, 7000 and above."
            )
            if new_msg != old_msg:
                ix["feedback"]["correct"]["message"] = new_msg
                changes.append(f"s05 (case_expressions) correct feedback: rephrased ELSE description")
            else:
                changes.append(f"WARNING: s05 case_expressions feedback replacement did not match!")

print("Changes applied:")
for c in changes:
    print(" -", c)

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Done.")
