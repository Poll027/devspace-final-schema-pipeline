# 01 scenario + asset registry — EVALUATOR
Fresh context. Re-derive from the glossary bundle and the registry; do not trust the generator's notes. The deterministic gate (`validate_tile.py --registry`) already passed — do not repeat it.

BLOCKING: a column/value the glossary examples depend on is missing or contradicts the taught text; a column's `semantic_role` is arguable (two defensible readings); a dataset/variant cannot support an anchor it must serve; data that would teach a wrong fact; a planted issue that isn't a real instance of its kind. ADVISORY: realism, naming, size, extra columns.
Check at least a third of the concepts' examples against the registry (and no more than about two thirds unless something specific warrants it).
End with `VERDICT: PASS|FAIL`, then one line per defect: `BLOCKING|ADVISORY <asset_id>/<field>: problem → fix`.
