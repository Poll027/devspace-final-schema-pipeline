"""Validate an artifact against a pack schema, resolving cross-file $refs (schemas live flat in ../schemas/).

CLI (any agent can run it):  python3 schema_check.py <schema file name> <artifact.json>
Self-check of every schema: python3 schema_check.py --self
Python:                      from schema_check import validate, errors
"""
import json
import sys
from pathlib import Path

SCHEMAS = Path(__file__).resolve().parent.parent / "schemas"


def _registry():
    from referencing import Registry, Resource
    return Registry().with_resources((f.name, Resource.from_contents(json.loads(f.read_text()))) for f in SCHEMAS.glob("*.schema.json"))


def _validator(schema_name):
    import jsonschema
    schema = json.loads((SCHEMAS / schema_name).read_text())
    return jsonschema.Draft202012Validator(schema, registry=_registry())


def errors(obj, schema_name, limit=25):
    """Human-readable problems, most specific first ([] when valid). oneOf failures are narrowed to the branch chosen by `type`."""
    out = []
    for e in sorted(_validator(schema_name).iter_errors(obj), key=lambda e: list(e.absolute_path)):
        where = "/".join(str(p) for p in e.absolute_path) or "<root>"
        msg = e.message
        if e.context:  # oneOf/anyOf: surface the branch whose `type` const matched, else the best-matching one
            sub = [c for c in e.context if c.validator != "const" or c.path]
            msg = "; ".join(sorted({f"{'/'.join(str(p) for p in c.absolute_path)}: {c.message}" for c in sub}, key=len)[:3]) or msg
        out.append(f"{where}: {msg[:300]}")
        if len(out) >= limit:
            break
    return out


def validate(obj, schema_name):
    errs = errors(obj, schema_name)
    if errs:
        raise ValueError(f"{schema_name}: {len(errs)} problem(s):\n  " + "\n  ".join(errs))


def self_check():
    import jsonschema
    bad = 0
    for f in sorted(SCHEMAS.glob("*.schema.json")):
        try:
            jsonschema.Draft202012Validator.check_schema(json.loads(f.read_text()))
            _validator(f.name)
        except Exception as e:  # noqa: BLE001
            bad += 1
            print(f"BAD {f.name}: {e}")
    print(f"{len(list(SCHEMAS.glob('*.schema.json')))} schemas checked, {bad} bad")
    return bad


if __name__ == "__main__":
    if sys.argv[1:] == ["--self"]:
        sys.exit(1 if self_check() else 0)
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    errs = errors(json.loads(Path(sys.argv[2]).read_text()), sys.argv[1])
    if errs:
        print(f"INVALID: {sys.argv[2]} against {sys.argv[1]}\n  " + "\n  ".join(errs))
        sys.exit(1)
    print(f"VALID: {sys.argv[2]} against {sys.argv[1]}")
