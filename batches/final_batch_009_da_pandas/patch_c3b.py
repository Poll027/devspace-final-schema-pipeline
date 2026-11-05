path = "batches/final_batch_009_da_pandas/screens.part.c3.json"
with open(path, "r", encoding="utf-8") as f:
    raw = f.read()

# Fix the prose block lineage for s10.b1 (16-space indentation)
old = (
    '                "fact_ids": [\n'
    '                  "pandas.groupby_aggregation#f1",\n'
    '                  "pandas.groupby_aggregation#f2",\n'
    '                  "pandas.groupby_aggregation#f3"\n'
    '                ]\n'
    '              }\n'
    '            },\n'
    '            {\n'
    '              "type": "up_next",'
)
new = (
    '                "fact_ids": [\n'
    '                  "pandas.groupby_aggregation#f1",\n'
    '                  "pandas.groupby_aggregation#f2",\n'
    '                  "pandas.groupby_aggregation#f3",\n'
    '                  "pandas.melt_reshaping#f1",\n'
    '                  "pandas.melt_reshaping#f2"\n'
    '                ]\n'
    '              }\n'
    '            },\n'
    '            {\n'
    '              "type": "up_next",'
)
count = raw.count(old)
assert count == 1, f"Expected 1 occurrence, found {count}"
raw = raw.replace(old, new, 1)

import json
json.loads(raw)  # validate
print("JSON valid.")

with open(path, "w", encoding="utf-8") as f:
    f.write(raw)
print("Block lineage patched.")
