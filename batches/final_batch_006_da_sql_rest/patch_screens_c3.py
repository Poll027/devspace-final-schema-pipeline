"""
Patch screens.part.c3.json for repair round findings:
1. s01 diagram: fix customer_id=3 (Fatima Aliyu) from unmatched→matched, add her order edges,
   remove c3_note, update c4_note to correctly describe Chidi Eze as unmatched.
2. r03 prose: fix "Customers 4 and 5" → "Customers 4, 5, and 6" in both places.
   (s04 prompt/feedback belong to stage 04 — not touched here.)
"""
import json, copy

with open("batches/final_batch_006_da_sql_rest/screens.part.c3.json") as f:
    data = json.load(f)

tile = next(t for t in data["tiles"] if t["tile_id"] == "tile_sql_adv_joining_tables")

# ── Fix 1: s01 diagram ──────────────────────────────────────────────────────
s01 = next(s for s in tile["steps"] if s["step_id"] == "tile_sql_adv_joining_tables.s01")
diagram = next(b for b in s01["blocks"] if b.get("type") == "diagram")

# Rebuild nodes:
# c1 matched, c2 matched, c3 matched (Fatima has orders 1004,1007,1010),
# c4 unmatched (Chidi Eze — no orders in registry), c4_note annotation.
# Orders shown: 1001 (cust=1), 1002 (cust=2), 1003 (cust=1),
#               1004 (cust=3), 1007 (cust=3) — show two of Fatima's orders to keep diagram readable.
diagram["nodes"] = [
    {"id": "c1",     "label": "customer_id=1 | Amara Okafor",  "kind": "matched",   "group": "customers"},
    {"id": "c2",     "label": "customer_id=2 | Emeka Nwosu",   "kind": "matched",   "group": "customers"},
    {"id": "c3",     "label": "customer_id=3 | Fatima Aliyu",  "kind": "matched",   "group": "customers"},
    {"id": "c4",     "label": "customer_id=4 | Chidi Eze",     "kind": "unmatched", "group": "customers"},
    {"id": "o1001",  "label": "order_id=1001 | cust=1",        "kind": "matched",   "group": "orders"},
    {"id": "o1002",  "label": "order_id=1002 | cust=2",        "kind": "matched",   "group": "orders"},
    {"id": "o1003",  "label": "order_id=1003 | cust=1",        "kind": "matched",   "group": "orders"},
    {"id": "o1004",  "label": "order_id=1004 | cust=3",        "kind": "matched",   "group": "orders"},
    {"id": "o1007",  "label": "order_id=1007 | cust=3",        "kind": "matched",   "group": "orders"},
    {"id": "c4_note","label": "customer_id=4 (Chidi Eze) has no matching order \u2014 dropped from result",
                     "kind": "annotation", "group": "note"},
]

# Rebuild edges: c1→o1001, c1→o1003, c2→o1002, c3→o1004, c3→o1007
diagram["edges"] = [
    {"from": "c1", "to": "o1001", "label": "match"},
    {"from": "c1", "to": "o1003", "label": "match"},
    {"from": "c2", "to": "o1002", "label": "match"},
    {"from": "c3", "to": "o1004", "label": "match"},
    {"from": "c3", "to": "o1007", "label": "match"},
]

# Update alt_text
diagram["alt_text"] = (
    "customers rows on the left, orders rows on the right. "
    "Rows with matching customer_id are linked. "
    "customer_id=1 (Amara Okafor) matches orders 1001 and 1003; "
    "customer_id=2 (Emeka Nwosu) matches order 1002; "
    "customer_id=3 (Fatima Aliyu) matches orders 1004 and 1007. "
    "customer_id=4 (Chidi Eze) has no matching order and is dropped from the result."
)

# ── Fix 2: r03 prose ────────────────────────────────────────────────────────
r03 = next(s for s in tile["remediation_steps"] if s["step_id"] == "tile_sql_adv_joining_tables.r03")
prose = next(b for b in r03["blocks"] if b.get("type") == "prose")

old = prose["text"]
new = old.replace(
    "Customers 4 and 5 are dropped.",
    "Customers 4, 5, and 6 are dropped."
).replace(
    "Customers 4 and 5 get a row with delivery_time_minutes = NULL.",
    "Customers 4, 5, and 6 get a row with delivery_time_minutes = NULL."
)
assert new != old, "r03 text replacement did not change anything!"
prose["text"] = new

with open("batches/final_batch_006_da_sql_rest/screens.part.c3.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
print("r03 new text:", prose["text"])
