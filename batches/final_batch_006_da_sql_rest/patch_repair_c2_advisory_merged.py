"""
Apply the same advisory repair changes to interactions.json (the merged file).
"""
import json

with open("batches/final_batch_006_da_sql_rest/interactions.json") as f:
    data = json.load(f)

def find_interaction(tile_id, step_id):
    for tile in data["tiles"]:
        if tile["tile_id"] == tile_id:
            for ix in tile["interactions"]:
                if ix["step_id"] == step_id:
                    return ix["interaction"]
    raise KeyError(f"{tile_id}/{step_id} not found")

# ── Fix 1 & 2: tile_sql_text_dates_casts/s03 ─────────────────────────────────
ix_s03 = find_interaction("tile_sql_text_dates_casts", "tile_sql_text_dates_casts.s03")

# Fix 1 & 2: update prompt with stray spaces/casing wording + name_length column
ix_s03["public"]["prompt"] = (
    "The `customers` table has columns `customer_id`, `name`, and `city`. "
    "Some city values may have stray spaces or inconsistent casing. "
    "Write a query that returns:\n\n"
    "- **customer_id** \u2014 unchanged\n"
    "- **city_clean** \u2014 the city value trimmed of spaces and converted to lower case\n"
    "- **label** \u2014 a combined string built with CONCAT in the form `'Name (City)'`, "
    "for example `'Amara Okafor (Lagos)'`\n"
    "- **name_length** \u2014 the number of characters in the customer's name (use `LENGTH(name)`)\n\n"
    "Return all rows. Name the columns exactly as shown."
)

# Update starter file comment
ix_s03["public"]["workspace"]["files"][0]["content"] = (
    "-- customers columns: customer_id, name, city\n"
    "-- Return: customer_id, city_clean, label, name_length\n"
    "-- city_clean: trim spaces then convert to lower case\n"
    "-- label: CONCAT(name, ' (', city, ')')\n"
    "-- name_length: LENGTH(name)\n\n"
)

# Update solution to include name_length
ix_s03["grading"]["solution_files"][0]["content"] = (
    "SELECT customer_id,\n"
    "       LOWER(TRIM(city))             AS city_clean,\n"
    "       CONCAT(name, ' (', city, ')') AS label,\n"
    "       LENGTH(name)                  AS name_length\n"
    "  FROM customers AS c\n"
)

# Update expected rows to include name_length
test = ix_s03["grading"]["tests"][0]
test["spec"]["expected"]["columns"] = ["customer_id", "city_clean", "label", "name_length"]
test["spec"]["expected"]["rows"] = [
    [1, "lagos",  "Amara Okafor (Lagos)", 12],
    [2, "kano",   "Emeka Nwosu (Kano)",   11],
    [3, "abuja",  "Fatima Aliyu (Abuja)", 12],
    [4, None,     "Chidi Eze ()",          9],
    [5, None,     " ()",                  None],
    [6, "kano",   "Ngozi Bello (Kano)",   11],
]
test["message_on_fail"] = (
    "Your query should return customer_id, city_clean (trimmed + lower-cased city), "
    "label (CONCAT of name and city), and name_length (LENGTH of name) for all 6 customers."
)

# Update feedback/hints to mention LENGTH
ix_s03["feedback"]["correct"]["message"] = (
    "Your query correctly trims and lower-cases the city column, builds the label with CONCAT, "
    "and measures the name length with LENGTH. Note that CONCAT ignores NULL arguments, "
    "so customers with a NULL city still get a partial label; LENGTH(NULL) returns NULL."
)
ix_s03["feedback"]["incorrect"]["message"] = (
    "Check that city_clean uses LOWER(TRIM(city)), label uses CONCAT(name, ' (', city, ')'), "
    "and name_length uses LENGTH(name). Make sure the column aliases match exactly."
)
ix_s03["feedback"]["hints"] = [
    "Nest TRIM inside LOWER: LOWER(TRIM(city)) trims first, then lower-cases.",
    "LENGTH(name) returns the number of characters; it returns NULL when name is NULL.",
]

# ── Fix 3: tile_sql_null_fallback_and_union/s04 ───────────────────────────────
ix_s04 = find_interaction("tile_sql_null_fallback_and_union", "tile_sql_null_fallback_and_union.s04")

# Add a forbidden_syntax test blocking CASE WHEN so COALESCE is required
# Only add if not already present
existing_ids = {t["test_id"] for t in ix_s04["grading"]["tests"]}
if "t_require_coalesce" not in existing_ids:
    forbidden_test = {
        "test_id": "t_require_coalesce",
        "kind": "forbidden_syntax",
        "spec": {
            "descriptors": ["CASE WHEN ... THEN ... ELSE ... END"]
        },
        "visible": False,
        "message_on_fail": "Use COALESCE to replace NULL city values, not CASE WHEN."
    }
    ix_s04["grading"]["tests"].append(forbidden_test)
    print("Added forbidden_syntax test to s04")
else:
    print("forbidden_syntax test already present in s04")

# Write back
with open("batches/final_batch_006_da_sql_rest/interactions.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("interactions.json patched successfully.")
