import json

path = "batches/final_batch_006_da_sql_rest/interactions.part.c2.json"

with open(path) as f:
    text = f.read()

OLD = "MAKE_DATE(2024, 1, 1)"
NEW = "DATE '2024-01-01'"

count = text.count(OLD)
text = text.replace(OLD, NEW)
print(f"Replaced {count} remaining occurrences of MAKE_DATE")

with open(path, "w") as f:
    f.write(text)

print("Done.")
