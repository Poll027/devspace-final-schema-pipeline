"""Prints the practice-anchor types and live_code syntax descriptors of the non-SQL concepts in a path glossary bundle.
   python3 practice_survey.py <path_glossary_bundle.json> [prefix,prefix,...]   (default prefixes: python,pandas,stats,viz,spreadsheet)"""
import collections
import json
import sys

b = json.load(open(sys.argv[1]))
want = (sys.argv[2] if len(sys.argv) > 2 else "python,pandas,stats,viz,spreadsheet").split(",")
d, types, ex = collections.Counter(), collections.Counter(), []
for x in b["bundles"]:
    ctx = x["context"]
    cid = next((ctx[k] for k in ("concept_id", "id", "canonical_id") if ctx.get(k)), "?")
    p = x.get("practice_anchor")
    if not p or cid.split(".")[0] not in want:
        continue
    types[(cid.split(".")[0], p["type"])] += 1
    lc = p.get("live_code") or {}
    for k in ("allowed_syntax", "blocked_syntax"):
        for s in lc.get(k, []):
            d[(k[:3], s)] += 1
    if len(ex) < 4:
        ex.append({"id": cid, "type": p["type"], "objective": p["objective"], "success": p["success"], "live_code": lc})
print(json.dumps({"practice_types": {f"{a}/{t}": n for (a, t), n in types.items()}, "examples": ex}, indent=1))
for (k, s), n in sorted(d.items()):
    print(k, n, s)

# descriptors the Python syntax checker cannot map (they would stop a run as UNVERIFIED)
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from checkers import pysyntax  # noqa: E402

bad = sorted({s for (k, s) in d if pysyntax.descriptor_tags(s) is None and s not in pysyntax.NOT_CHECKABLE})
print("\nUNMAPPED by pysyntax:", len(bad))
for s in bad:
    print("  ", s)
