# Stage 08 — Independent pedagogy review

## Scope and method

Reviewed the later-batch risk sample: **tile_022, tile_030, tile_034, tile_037** (4 of 11 tiles, rounding one third upward). These cover core-tier concepts with HIGH video need, both 14-step tiles, early foundational contracts, and the middleware/production-serving boundary. Reviewed each sampled tile's complete assembled lesson, interactions, supplied workspaces, answer-specific feedback and remediation. Inspected tile_024 additionally for configuration pacing, without claiming complete batch coverage.

Sources: `08_pedagogy_review/EVALUATOR.md`; playbook principles and lesson contract (§§2, 5), rollout sampling (§7); `inputs/path_glossary_bundle.json`; `scenario_asset_registry.json`; `tile_plans.json`; and the current `tile_lessons/` artifacts. Re-derived the taught rules and observable exercise expectations from the glossary and registry, not authoring scripts or previous reviews. Did not rerun deterministic gates. No player screenshots were present in the batch; visual judgments concern authored diagrams/code and their accompanying text, not verified rendering. Video judgments concern supplied segment summaries and bridges, not independent playback.

## Learner-journey judgment

- **tile_022 (12 steps; estimated 10.1 minutes):** Resource identity, method semantics and response metadata precede the first check and guided contract representation. FastAPI registration is introduced only afterward. Method/path identity and conflicting declaration order precede dispatch questions. Diagram and registration listing support the intended distinctions. No prerequisite-understanding blocker found.
- **tile_030 (14 steps; estimated 13.9 minutes):** Path/query source, conversion and omission are taught before checking defaults and invalid identifiers. Response-model filtering, priority and the direct-Response bypass are taught before their checks and implementation. Code and textual contrasts agree with the registry. The major opportunity is redundant reading and pacing, not missing teaching.
- **tile_034 (14 steps; estimated 11.4 minutes):** Three concept groups are separated into their own explain/check/apply sequences. Prior dependency knowledge supports the responsibility-refactor exercise. Background-task registration and the process-failure limitation precede suitability judgment and registration practice. Dependency prerequisites and typed query inputs precede the composition exercise. The diagrams make each boundary useful and explicit; their arrows do not contradict the prose.
- **tile_037 (8 steps; estimated 7.2 minutes):** Wrapper ordering precedes both traversal judgment and configuration practice. ASGI import-string meaning and production/reload boundaries precede serving judgment. The startup excerpts carry the evidence needed for inspect-and-judge; native execution is not required. No blocker arises from using authored startup fixtures.

The sampled checks have a defensible taught answer, and wrong-option feedback does not change glossary facts. Multiple facts in a step generally elaborate a single governing distinction rather than conceal a second idea. Remediation usually gives the relevant contrast; some application feedback could be more diagnostic. Video bridges usefully distinguish clip coverage from standalone text, although text/video overlap remains a pacing concern rather than a blocker. No BLOCKING defect found in the reviewed scope.

## Findings

ADVISORY tile_030/s02: The walkthrough repeats the s01 code annotation verbatim, and s03 then restates the same source/conversion/default distinctions; the tile is already estimated at 13.9 minutes → Replace s02 prose with a concrete trace: `For /orders/7?limit=3, the placeholder supplies order_id=7 and the query supplies limit=3, both as integers. For /orders/7, limit uses its declared default of 5. For /orders/not-an-integer, path conversion fails before the handler runs.` Keep s03's required-versus-defaulted contrast and the fixed step skeleton.

ADVISORY tile_030/s09: This walkthrough repeats the s08 annotation verbatim before another closely overlapping explainer → Replace s09 prose with: `The internal dictionary contains order_id, status and private_processing_note. Because read_order returns that dictionary normally through response_model=PublicOrder, the public output contains only order_id and status. The private note remains internal.` Keep s10 for priority and the direct-Response contrast; do not remove those facts.

ADVISORY tile_022/s04: Generic exercise feedback names path/method identity even when the learner's mistake is a creation Location or status, so it gives little help locating the faulty assignment → Replace the generic incorrect message with: `Check the failing section. For identity_and_methods, compare the collection/item paths and the GET, POST, PUT and DELETE assignments. For response details, creation uses 201 with Location /orders/42, while an absent item uses 404. Change the annotated assignments, not the supplied values or inspector.` Where possible, give these two section-specific messages on the corresponding tests.

ADVISORY tile_037/s07: Item c's feedback labels the import failure but then explains reload, which is unrelated to that item's mistake → Replace item c feedback with: `main:missing asks Uvicorn for an object named missing in module main. The supplied module defines app, and the startup excerpt says missing was not found. Use main:app with the specified host and port and without reload.` Retain the existing reload explanation for item b.

## Verdict

**VERDICT: PASS** — completed the independent sampled review; findings are advisory-only. This is not a claim that every tile in the batch or player rendering was reviewed.
