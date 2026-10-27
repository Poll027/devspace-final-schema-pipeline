"""Keep schemas/block_union.schema.json and interaction_union.schema.json in sync with registry/*.json (the pack mechanism).

Adding a block or interaction type for a new domain pack =
  1. write schemas/block.<type>.schema.json (or ix.<type>.schema.json)   2. add one entry to registry/block_registry.json (or interaction_registry.json)
  3. python3 build_unions.py      4. build the matching player component (the registry's `status` goes draft -> stable when the player ships it)
  python3 build_unions.py --check   exits 1 if a union is out of date, a registered schema file is missing, or a schema file is unregistered (CI use)
"""
import json
import sys
from pathlib import Path

from finlib import CORE, load

SCH = CORE / "schemas"
SPEC = [("block_union", "block_registry.json", "blocks", "block", "Union of every registered block type"),
        ("interaction_union", "interaction_registry.json", "interactions", "ix", "Union of every registered interaction type")]


def main():
    check = "--check" in sys.argv
    bad = 0
    for name, regfile, key, prefix, title in SPEC:
        reg = load(CORE / "registry" / regfile)[key]
        want = {"$schema": "https://json-schema.org/draft/2020-12/schema", "$id": f"{name}.schema.json", "title": title,
                "oneOf": [{"$ref": e["schema"]} for e in reg]}
        for e in reg:
            if not (SCH / e["schema"]).exists():
                print(f"MISSING schema file for registered type {e['type']}: {e['schema']}")
                bad += 1
        files = {f.name for f in SCH.glob(f"{prefix}.*.schema.json")}
        for f in sorted(files - {e["schema"] for e in reg}):
            print(f"UNREGISTERED schema file {f} (add it to registry/{regfile})")
            bad += 1
        path = SCH / f"{name}.schema.json"
        if load(path) != want:
            if check:
                print(f"STALE {path.name}")
                bad += 1
            else:
                path.write_text(json.dumps(want, indent=2) + "\n")
                print(f"rebuilt {path.name} ({len(reg)} types)")
    if check:
        print("unions OK" if not bad else f"{bad} problem(s)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
