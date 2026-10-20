"""Dataset helpers for the data pack: variant op chains, predicate row lookup, planted-issue rules (moved out of the role-agnostic core)."""
import copy


def _matches(row, where):
    return all(row.get(k) == v for k, v in where.items())


def find_row(rows, where, occurrence=0):
    hits = [i for i, r in enumerate(rows) if _matches(r, where)]
    return hits[occurrence] if occurrence < len(hits) else None


def asset_by_id(registry, asset_id):
    for a in registry["assets"]:
        if a["asset_id"] == asset_id:
            return a
    return None


def resolve_dataset(registry, asset_id, variant_id=None):
    """Return (columns, rows-as-dicts) of a dataset after applying its variant op chain. Raises KeyError/ValueError on a bad reference."""
    ds = asset_by_id(registry, asset_id)
    if ds is None or ds.get("asset_kind") != "dataset":
        raise KeyError(f"no dataset asset {asset_id!r}")
    if "rows" not in ds:
        raise ValueError(f"{asset_id}: data_file datasets are resolved by the runtime, not inline")
    names = [c["name"] for c in ds["columns"]]
    base = [dict(zip(names, r)) for r in ds["rows"]]
    for r in ds["rows"]:
        if len(r) != len(names):
            raise ValueError(f"{asset_id}: row width {len(r)} != {len(names)} columns")
    if not variant_id:
        return ds["columns"], base
    variants = {v["variant_id"]: v for v in ds.get("variants", [])}
    if variant_id not in variants:
        raise KeyError(f"{asset_id}: no variant {variant_id!r}")
    chain, cur = [], variants[variant_id]
    while True:
        chain.append(cur)
        parent = cur["derived_from"]
        if parent in ("base", asset_id):
            break
        cur = variants[parent]
    cols, rows = copy.deepcopy(ds["columns"]), copy.deepcopy(base)
    for v in reversed(chain):
        for op in v["ops"]:
            k = op["op"]
            if k == "set_cell":
                i = find_row(rows, op["where"], op.get("occurrence", 0))
                if i is None:
                    raise ValueError(f"{variant_id}: set_cell matched no row {op['where']}")
                rows[i][op["column"]] = op["value"]
            elif k == "duplicate_row":
                i = find_row(rows, op["where"], op.get("occurrence", 0))
                if i is None:
                    raise ValueError(f"{variant_id}: duplicate_row matched no row {op['where']}")
                rows.insert(len(rows) if op.get("insert") == "end" else i + 1, dict(rows[i]))
            elif k == "drop_rows":
                rows = [r for r in rows if not _matches(r, op["where"])]
            elif k == "drop_columns":
                cols = [c for c in cols if c["name"] not in op["columns"]]
                rows = [{k2: v2 for k2, v2 in r.items() if k2 not in op["columns"]} for r in rows]
    return cols, rows


def rule_holds(rule, rows, row_idx, column):
    """Evaluate a planted-issue rule against the located cell. Returns (ok, why)."""
    val = rows[row_idx].get(rule.get("column", column))
    op, ref = rule["op"], rule.get("value")
    try:
        if op == "is_null":
            return val is None, f"value={val!r}"
        if op == "lt":
            return val < ref, f"value={val!r}"
        if op == "le":
            return val <= ref, f"value={val!r}"
        if op == "gt":
            return val > ref, f"value={val!r}"
        if op == "ge":
            return val >= ref, f"value={val!r}"
        if op == "eq":
            return val == ref, f"value={val!r}"
        if op == "ne":
            return val != ref, f"value={val!r}"
        if op == "casing_differs_from_siblings":
            sibs = [r.get(column) for i, r in enumerate(rows) if i != row_idx and isinstance(r.get(column), str)]
            return any(s != val and s.lower() == str(val).lower() for s in sibs), f"value={val!r} siblings={sorted(set(sibs))}"
    except TypeError as e:
        return False, f"type error: {e}"
    return False, f"unknown rule op {op}"
