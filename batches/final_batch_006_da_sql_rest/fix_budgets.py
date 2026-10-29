"""Fix word-budget overruns in build_screens_c1.py then regenerate."""
import re

path = "batches/final_batch_006_da_sql_rest/build_screens_c1.py"
content = open(path).read()

# ── Fix 1: s04 misconception (LIMIT/OFFSET) ──────────────────────────────────
old1 = (
    '                "Without ORDER BY, LIMIT and OFFSET can return an unpredictable subset of rows. "\n'
    '                "SQL does not promise any particular sequence unless ORDER BY is present, "\n'
    '                "so always pair LIMIT/OFFSET with an ORDER BY clause.",'
)
new1 = (
    '                "Without ORDER BY, LIMIT and OFFSET return an unpredictable subset. "\n'
    '                "SQL promises no particular sequence unless ORDER BY is present.",'
)
assert old1 in content, "old1 not found"
content = content.replace(old1, new1)

# ── Fix 2: s02 case mechanism (ELSE / NULL fallthrough) ──────────────────────
old2 = (
    '                "If no WHEN condition is true, CASE returns the ELSE result if one is given, or NULL if ELSE is omitted. "\n'
    '                "An order with a NULL delivery_time_minutes also falls through to ELSE, "\n'
    '                "because none of the WHEN conditions evaluate to true for a null value. "\n'
    '                "Omitting ELSE is valid SQL but can produce unexpected NULLs in the output column.",'
)
new2 = (
    '                "If no WHEN condition is true, CASE returns the ELSE result if given, or NULL if ELSE is omitted. "\n'
    '                "A row with a NULL delivery_time_minutes also falls through to ELSE, "\n'
    '                "since no WHEN condition is true for a null. Omitting ELSE can silently produce NULLs.",'
)
assert old2 in content, "old2 not found"
content = content.replace(old2, new2)

open(path, "w").write(content)
print("Patched build script.")
