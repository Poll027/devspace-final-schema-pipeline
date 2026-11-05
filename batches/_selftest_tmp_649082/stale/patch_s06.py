import json, pathlib

p = pathlib.Path("batches/final_batch_013_da_stakeholder_chart/screens.part.c0_canary.json")
data = json.loads(p.read_text())

changed = 0
for tile in data["tiles"]:
    for step in tile["steps"]:
        if step["step_id"].endswith(".s06"):
            for block in step.get("blocks", []):
                if block.get("type") == "before_after":
                    before_diag = block.get("before", {})
                    for node in before_diag.get("nodes", []):
                        if node.get("id") == "decimal_labels":
                            old = node["label"]
                            node["label"] = "Y-axis labels with trailing zeros (e.g., 0.00, 10.00, 20.00, 30.00, 40.00)"
                            print(f"Changed: {old!r} -> {node['label']!r}")
                            changed += 1

print(f"Total changes: {changed}")
p.write_text(json.dumps(data, indent=2, ensure_ascii=False))
print("Done.")
