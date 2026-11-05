import json, pathlib

p = pathlib.Path("batches/final_batch_012_da_viz/interactions.part.c0_canary.json")
data = json.loads(p.read_text())

old = "Not quite. `plt.plot()` always draws a line chart. With a single argument it uses the list as y-values and auto-generates x-positions from 0."
new = "Not quite. `plt.plot()` draws a line by default. With a single argument it uses the list as y-values and auto-generates x-positions from 0."

found = False
for tile in data["tiles"]:
    for item in tile["interactions"]:
        ix = item["interaction"]
        fb = ix.get("grading", {}).get("option_feedback", {})
        if "opt_none" in fb and fb["opt_none"]["message"] == old:
            fb["opt_none"]["message"] = new
            found = True

if not found:
    raise RuntimeError("Target string not found — check the artifact.")

p.write_text(json.dumps(data, indent=2, ensure_ascii=False))
print("Patched OK")
