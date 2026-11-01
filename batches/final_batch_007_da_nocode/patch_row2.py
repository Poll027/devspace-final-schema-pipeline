"""
Patch ds_finding_statements row 2 precise_finding to use numbers
derivable from the 12-row ds_delivery_orders dataset, resolving the
advisory that 1,240 orders / 18% are not derivable from the sample.

The 12-row dataset has:
  - Lagos rows: 1001,1003,1006,1009,1012 → 5 orders
  - Abuja rows: 1002,1005,1008,1011      → 4 orders
  - Port Harcourt rows: 1004,1007,1010   → 3 orders
  - Total: 12 orders

We reword row 2 to use a Lagos-specific order count (5) and a
delivery-time comparison that IS in the dataset, keeping the
"Sales went up" vague finding as a generic teaching contrast
but making the precise version reference the actual dataset numbers.

Actually, to keep the teaching contrast clear (vague "Sales went up"
vs precise rewrite), we change the precise_finding to reference
delivery orders in the dataset rather than "sales", using real numbers.
"""
import json, pathlib

path = pathlib.Path("batches/final_batch_007_da_nocode/scenario_asset_registry.json")
data = json.loads(path.read_text())

# Find ds_finding_statements asset
for asset in data["assets"]:
    if asset["asset_id"] == "ds_finding_statements":
        rows = asset["rows"]
        # Row index 1 = finding_id 2
        # Current: "Total sales in March 2024 reached 1,240 orders, an increase of 18% compared with February 2024."
        # New: reword to use numbers from the dataset (12 orders total, 5 Lagos orders)
        # Keep vague finding "Sales went up." unchanged — it's a generic teaching example
        # Reword precise finding to reference delivery orders (not "sales") with dataset-derivable numbers
        rows[1][2] = (
            "Kwik Courier completed 12 delivery orders in the sample week, "
            "with Lagos accounting for 5 of those orders — the highest share of any city."
        )
        # has_specific_number: True (12, 5) — unchanged
        # has_comparison: True (highest share vs other cities) — unchanged
        # is_complete_sentence: True — unchanged
        print("Row 2 precise_finding updated.")
        print("New value:", rows[1][2])
        break

path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
print("File written.")
