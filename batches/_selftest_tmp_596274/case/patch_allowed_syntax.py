import json

path = "batches/final_batch_012_da_viz/interactions.part.c0_canary.json"

with open(path) as f:
    data = json.load(f)

# Glossary verbatim allowed_syntax values
GLOSSARY = {
    "ix.tile_viz_figures_layout_plotting.s05": [
        "import matplotlib.pyplot as plt",
        "fig, ax = plt.subplots()",
        "ax.plot(x, y)"
    ],
    "ix.tile_viz_figures_layout_plotting.s08": [
        "plt.subplots(figsize=(width, height))",
        "fig.tight_layout()",
        "plt.tight_layout()",
        "tuple literals for figsize",
        "variable assignment (fig, ax = ...)"
    ],
    "ix.tile_viz_figures_layout_plotting.s12": [
        "import matplotlib.pyplot as plt",
        "plt.plot(y_list)",
        "plt.plot(x_list, y_list)"
    ],
}

patched = 0
for tile in data["tiles"]:
    for item in tile["interactions"]:
        iid = item["interaction"].get("interaction_id")
        if iid in GLOSSARY:
            constraints = item["interaction"]["public"]["constraints"]
            old = constraints["allowed_syntax"]
            new = GLOSSARY[iid]
            if old != new:
                constraints["allowed_syntax"] = new
                print(f"Patched {iid}: {old} -> {new}")
                patched += 1

print(f"Total patched: {patched}")

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Done.")
