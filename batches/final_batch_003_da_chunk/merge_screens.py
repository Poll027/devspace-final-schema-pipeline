#!/usr/bin/env python3
"""Merge screens parts into screens.json"""
import json

# Read all parts
parts = []
for chunk in ['c0_canary', 'c1', 'c2', 'c3']:
    try:
        with open(f'screens.part.{chunk}.json', 'r') as f:
            parts.append(json.load(f))
    except FileNotFoundError:
        print(f"Warning: screens.part.{chunk}.json not found")

# Merge: header from first part, tiles from all parts
out = dict(parts[0])
out['tiles'] = []
for part in parts:
    out['tiles'].extend(part['tiles'])

# Write merged file
with open('screens.json', 'w') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
    f.write('\n')

print(f"Merged {len(parts)} parts into screens.json with {len(out['tiles'])} tiles")
