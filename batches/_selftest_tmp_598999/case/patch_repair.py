import json, re

with open('batches/final_batch_009_da_pandas/scenario_asset_registry.json', 'r') as f:
    data = json.load(f)

# ── Fix 1: cw_dtype_datetime starter.py ──────────────────────────────────────
# Remove the pd.to_numeric hint line; keep the TODO to convert distance_km
# (the astype(float) approach is what the glossary teaches)
for asset in data['assets']:
    if asset['asset_id'] == 'cw_dtype_datetime':
        for file in asset['files']:
            if file['path'] == 'starter.py':
                old = file['content']
                # Remove the hint line about pd.to_numeric
                new = old.replace(
                    "\n# Hint: 'unknown' values will cause astype(float) to fail — use pd.to_numeric(errors='coerce') instead",
                    ""
                )
                assert new != old, "Fix 1: no change made — pattern not found"
                file['content'] = new
                print("Fix 1 applied: removed pd.to_numeric hint from cw_dtype_datetime/starter.py")
                break

# ── Fix 2: cw_creating_dataframes starter.py ─────────────────────────────────
# order_id 1003 has delivery_time_minutes=22 in ds_orders, not 26.
# Change the third example row to order_id 1005, city Abuja, delivery_time_minutes=26
# (which matches ds_orders exactly) in both Way 1 and Way 2 comment blocks.
for asset in data['assets']:
    if asset['asset_id'] == 'cw_creating_dataframes':
        for file in asset['files']:
            if file['path'] == 'starter.py':
                old = file['content']
                # Way 1 dict: change order_id list and delivery_time_minutes list
                new = old.replace(
                    "'order_id': [1001, 1002, 1003],\n#     'city': ['Lagos', 'Abuja', 'Kano'],\n#     'delivery_time_minutes': [18, 20, 26]",
                    "'order_id': [1001, 1002, 1005],\n#     'city': ['Lagos', 'Abuja', 'Abuja'],\n#     'delivery_time_minutes': [18, 20, 26]"
                )
                # Way 2 list of dicts: change third dict
                new = new.replace(
                    "{'order_id': 1003, 'city': 'Kano',  'delivery_time_minutes': 26},",
                    "{'order_id': 1005, 'city': 'Abuja', 'delivery_time_minutes': 26},"
                )
                assert new != old, "Fix 2: no change made — pattern not found"
                file['content'] = new
                print("Fix 2 applied: changed order_id 1003/26 → 1005/Abuja/26 in cw_creating_dataframes/starter.py")
                break

with open('batches/final_batch_009_da_pandas/scenario_asset_registry.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Done — file written.")
