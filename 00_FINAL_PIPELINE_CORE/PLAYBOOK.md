# Final Schema Pipeline — Playbook (v0.1, draft)

> **TOC = order. Evidence = truth. Glossary = teaching bank. Video = support. Final Schema = arrangement and everything the learner touches.**

This pack turns a path's **Glossary Learning Bundles** into **tile lessons**: ordered screens (explainers, video, checks, hands-on, recap) with every visual, question, answer key, dataset and code exercise authored, validated and stored once. The player renders them; nothing is generated at runtime. (A runtime-generated "custom path" feature is a later, separate product — see §9.)

It is **role-agnostic**: the same scripts, schemas, loop and gates run every one of the 64 paths. What differs per role is *data* (path profile, asset registry, which packs the glossary needs), never code in the core.

## 1. What comes in, what goes out

| In (frozen, never edited) | Out (per path, in `batches/<id>/`) |
|---|---|
| TOC workspace (`freeze_manifest.json`) | `scenario_asset_registry.json` — scenarios + reusable assets (datasets, code workspaces, images) |
| `path_glossary_bundle.<path>.json` — per concept: facts, teaching blocks, media segments, assessment/practice/visual **anchors (intent only)**, clusters | `tile_plans.json` — deterministic step skeleton per tile |
| | `screens.json`, `interactions.json` — authored parts |
| | `tile_lessons/<tile>.json` (full), `tile_lessons_public/` (grading stripped for server-graded items), `grading/` |

The glossary never stores screens, question text, answers, datasets or UI. Everything concrete is authored here.

## 2. Principles (each is enforced by a script, not a request to the model)

1. **Pre-authored, validated offline.** The model writes content; scripts verify it.
2. **Structure by rule, content by model.** `plan_tiles.py` decides which steps exist, their order, lineage, planned interaction and visual block types. The model fills them. The validator rejects deviations.
3. **Outputs are computed, never typed.** Table results, chart data, expected values and code output come from executing on registered assets; media segments, bridge notes, hashes and `requires` are copied/computed by `assemble_tiles.py`.
4. **Answer keys are data predicates** (`{order_id: NS1003, column: delivery_minutes, expect_value: 41}`), checked against the asset, so a key can't silently disagree with the data.
5. **Traceability.** Every question → fact → teaching block (the playbook v3 rule: *if the answer was never taught, reject the question*). A fact may only be tested after a **text** block has taught it (video doesn't count — text must stand alone).
6. **Coverage is checked both ways.** Every required fact is taught; every assessment anchor is measured; every practice anchor has a hands-on step; every visual anchor is realised.
7. **Fail closed.** A block, interaction or asset type with no checker is `UNVERIFIED` (error under `--strict`), never a silent pass.
8. **Mutation-tested gates.** `selftest.py` breaks content in known ways and asserts the validator catches each. Run it after any change to a schema or checker.

## 3. Stages (`pipeline_manifest.json`)

`00 preflight` (script) → `01 scenario_assets` (G/E) → `02 tile_plan` (script) → `03 screens` (G/E) → `04 interactions` (G/E) → `05 code_exercises` (G/E, only where the plan needs them) → `06 assemble` (script) → `07 validate` (script) → `08 pedagogy_review` (E) → `09 leakage_check` (E) → `10 ledger` (script) → `11 final_audit` (E) → `12 publish` (script).

Evaluator findings are `BLOCKING` (fails the round) or `ADVISORY` (fixed once, no re-evaluation) — same rule as the glossary pack. Scripts run before any evaluator so evaluators never pay to rediscover what a script catches.

## 4. Extensibility: packs

A **pack** is a set of block types, interaction types, asset kinds and their checkers.

| Pack | Blocks | Interactions | Asset kinds | Checker |
|---|---|---|---|---|
| `core` (every role) | prose, heading, callout, concept_chips, up_next, media_group, comparison, side_by_side, before_after, process_flow (flowchart), diagram (graph/erd/architecture/network/sequence/venn/tree/layers/mindmap/timeline/number_line/array/mapping/container), code_walkthrough, annotated_image | choice, ordering, match_pairs, field_selection, short_answer, external_proof, diagram_label, code_exercise* | image, code_workspace | `checkers/core.py` |
| `data` | data_table, spreadsheet_grid, chart | table_select, find_issues, classify, formula_entry* | dataset | `checkers/data.py` |
| `software` (future) | file_tree, terminal_session, ui_preview, http_exchange | … | repo | to write |
| `security`, `design`, … (future) | per what each glossary's visual/practice anchors need | | | to write |

`*` declared, **unverified** until the sandbox runner exists.

Adding a type: schema file `block.<t>.schema.json`/`ix.<t>.schema.json` → one entry in `registry/block_registry.json`/`interaction_registry.json` → `build_unions.py` → checker in a pack module → player component (registry `status` draft → stable when shipped). `visual_inventory.py <glossary bundle>` lists, per path, exactly which types/runtimes it needs and which are missing.

**Evidence the data pack is not the model:** for Data Analyst only 27 of 163 visual anchors are data/spreadsheet/chart; 136 are core (before_after 57, diagram 21, comparison 19, flowchart 18, code 11, screenshot 10). Practice: live_code 93, field_selection 21, spreadsheet 20, formula 10, matching 9, external_proof 8, ordering 5.

## 5. Tile lesson contract (what the backend stores and the player renders)

```
tile_lesson { schema_version, path_id, tile_id, toc_location, title, concept_ids,
  source { glossary_batch_id, toc_freeze_hash, glossary_bundle_hashes{concept→sha}, scenario_registry_hash },
  requires { min_player_version, packs[], block_types[], interaction_types[], runtimes[], asset_ids[] },   # capability negotiation
  steps[ step { step_id, type: explainer|video|check|hands_on|recap, concept_ids, eyebrow, title, lede,
                blocks[ …typed visual/text blocks… ], interaction{ type, public, grading, feedback, measures, grading_mode, standalone },
                reward, lineage{ fact_ids, teaching_block_ids, segment_ids, anchors } } ],
  remediation_steps[], completion{ reward, next_tile_id }, content_hash }
```

- **Ids** are deterministic (`<tile>.sNN`, `ix.<tile>.sNN`) so progress survives regeneration where the plan is unchanged; progress rows should also store `content_hash`.
- **Public/grading split:** `grading_mode: client` ships the key for instant feedback (low-stakes checks); `server` strips `grading` into `grading/<tile>.json` and the backend grades on submit. Default: client for checks, server for assessments.
- **Mastery:** each interaction carries `measures [{concept_id, capability, fact_ids}]` (the glossary's capability tags) so the backend computes per-concept/capability mastery. `standalone: true` interactions can be reused for review/spaced repetition.
- **Adaptive:** video-off → render the segment `summary`; hint ladders and `remediation_step_id` give conditional steps; rewards are config (`gems`), computed at runtime.
- **Datasets** are stored once per path (`scenario_asset_registry`), referenced by `asset_ref {asset_id, variant_id, columns}`; "messy" variants are derived by declared ops with planted issues recorded and verified.
- **Shared grader:** one TypeScript `grader-core` (to build) used by the player, the backend and this pipeline's Node checks, so an authored correct answer passes and each distractor yields its intended feedback everywhere.

## 6. Runtimes (code / formulas / charts)

Python+pandas → Pyodide; SQL → DuckDB-WASM; JS/React → sandboxed iframe; spreadsheet → a formula engine whitelisted to the functions the glossary allows (**check licences — HyperFormula is GPL/commercial dual-licensed as far as I recall**); charts → a constrained Vega-Lite-style subset. `practice_anchor.live_code.allowed_syntax/blocked_syntax` from the glossary is copied into `code_exercise.constraints` and enforced by the grader. Non-coding paths (cyber, devops, marketing tools) need a scripted tool-simulation runtime later (`UI_edit`/`tool_simulation` anchors have no interaction type yet).

## 7. Cost and rollout

Anchor: the glossary pilot cost ≈ $216 for 168 concepts (≈ $1.29/concept). Target here ≤ ≈ $0.65/concept by (a) rule-built structure, (b) single-shot schema-constrained generation per tile, (c) scripts before evaluators, (d) blocking/advisory gate, (e) canary-then-sample. Execution mirrors the glossary pack (Bedrock ladders, spend cap, supervisor on EC2); stage instructions are model-agnostic.

## 8. Thesys / OpenUI — decision

Not adopted for core content. OpenUI is an MIT generative-UI framework for LLM-driven chat interfaces (compact DSL, typed component registry, streaming renderer, paid gateway with autofix/monitoring). Its generic components have no answer keys, graded interactions, dataset/spreadsheet/code runtimes or lineage, and runtime generation conflicts with principles 1–5. Ideas worth borrowing are already here: a typed registry that exports JSON Schema to constrain generation. Reconsider for a later AI-tutor side panel where runtime generation is wanted.

## 9. Out of scope now

Runtime-generated custom paths (later; may reuse these schemas as the output contract); per-learner personalisation beyond video-off/remediation; i18n; rewards economy design.
