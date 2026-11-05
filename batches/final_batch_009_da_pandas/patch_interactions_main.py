import json

# Patch interactions.json (the file the gate reads) with the same fix
path = "batches/final_batch_009_da_pandas/interactions.json"

with open(path) as f:
    data = json.load(f)

# Verbatim allowed_syntax from glossary practice anchors
ALLOWED_SYNTAX_S05 = [
    "import pandas as pd",
    "pd.Series(list)",
    "pd.DataFrame(dict_of_lists)",
    "df['col']",
    "print()",
    "type()"
]

ALLOWED_SYNTAX_S10 = [
    "import pandas as pd",
    "pd.read_csv(path)",
    "pd.read_csv(path, sep=...)",
    "pd.read_excel(path, sheet_name=...)",
    "print(df)"
]

for tile in data["tiles"]:
    for ix in tile["interactions"]:
        sid = ix["step_id"]
        if sid == "tile_pandas_dataframe_reading.s05":
            ix["interaction"]["public"]["constraints"]["allowed_syntax"] = ALLOWED_SYNTAX_S05
            print(f"Patched {sid} allowed_syntax")
        elif sid == "tile_pandas_dataframe_reading.s10":
            ix["interaction"]["public"]["constraints"]["allowed_syntax"] = ALLOWED_SYNTAX_S10
            print(f"Patched {sid} allowed_syntax")

with open(path, "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print("Done.")
