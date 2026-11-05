# Devspace Data Analyst content: full handoff for the backend

**Written for:** the engineers who will build Devspace's backend (content store, API, grading service, progress and mastery tracking) and who need the complete context of what the content pipeline produced and why.
**State described:** the Data Analyst path, all 72 tiles generated, validated and committed; the shared grader built. As of 2026-11-05, repository `Poll027/devspace-final-schema-pipeline`, `main`.
**Not covered because it does not exist yet:** the backend, the publish step (pipeline stage 12), the player's integration of the grader. This document is the input for building them.

How to read this: sections 1-3 are context, 4-9 are the contracts and what the pipeline implements, 10 is what the backend has to build (recommendations, clearly marked), 11-14 are limitations, decisions, operations and open items. Five appendices hold the bulk data (listed in section 15).

---

## 1. What exists, in numbers

| Item | Count |
|---|---|
| Career paths in the product (planned) | 64. **Only Data Analyst is built.** The pipeline is role-agnostic; per-role differences are data. |
| Data Analyst: regions / terrains / tiles / concepts | 12 / 25 / **72** / 168 |
| Steps across the 72 tiles | 783 (243 explainer, 215 check, 168 hands_on, 85 video, 72 recap) |
| Remediation steps (conditional, shown after a miss) | 223 |
| Interactions | **383**: 215 choice, 103 code_exercise, 20 formula_entry, 19 table_select, 10 classify, 8 external_proof, 5 ordering, 3 find_issues |
| Code exercises by runtime | python 53, sql 26, chart_renderer 16, spreadsheet 8 (plus 20 formula_entry on the spreadsheet engine) |
| Content blocks | 918 (580 prose, 85 media_group, 71 up_next, 56 before_after, 31 diagram, 20 side_by_side, 18 process_flow, 15 heading, 11 data_table, 11 code_walkthrough, 9 spreadsheet_grid, 7 chart, 3 callout, 1 comparison) |
| Interaction difficulty | 99 intro, 228 core, 56 stretch |
| Reusable ("standalone") interactions, suitable for review/spaced repetition | 43 |
| Total reward configured | 4,314 gems across tiles (rewards are config, computed at runtime) |
| Datasets / code workspaces in the asset registries | 59 / 16 asset records (65 distinct ids; see section 8, ids collide) |
| Video segments referenced by the glossary | 115 segments on 85 concepts |
| Grader tests (answer-key replay) | 1,164 non-code + 27 SQL + 54 Python + 17 chart + 9 sheet + 21 formula = 1,292 tests, all pass |
| Generation cost (Bedrock, batches 002-013) | **$965.74**, about 31,300 model calls |

Cost is above the plan's target. The playbook aimed at roughly $0.65 per concept; this run cost about $5.75 per concept ($965.74 / 168). The first path also paid for building and verifying four code runtimes, the checkers and the unattended driver, and for many repair loops (section 13.4). Expect later paths to be cheaper, but do not budget from the target figure.

---

## 2. Product context: the three layers

Devspace is an AI learning platform with 64 career paths (data analyst, business analyst, software, cyber, devops, marketing, non-coding paths). Every path is taught from three layers, built in this order:

1. **TOC (table of contents).** The frozen, ordered concept sequence per path, produced by a separate upstream pipeline. Hierarchy: **Region -> Terrain -> Tile -> Concept unit**. A *tile* is the unit a learner completes (about 2-3 concepts, 8-16 steps, roughly 6-20 minutes). Frozen workspace for this path: `04_data_analyst_V2_WORKSPACE` (not in this repo; `toc.json`, `ordered_concept_sequence.json`, prerequisite graph, validation reports).
2. **Glossary Learning Bundles (the teaching bank).** Per concept: sourced facts, teaching text, a video-need call, selected YouTube segments (timestamps, with summaries), assessment/practice/visual anchors (intent only) and teaching notes. Built by a sibling project (`UNIVERSAL_GLOSSARY_PIPELINE_PACK`, 19 stages). Text must teach on its own ("never as the video shows"); learners can turn video off.
3. **Final Schema (this pipeline's output).** Everything the learner touches: ordered screens, visuals, questions, answer keys, datasets, code exercises, hints, remediation and rewards. Authored once, validated by scripts, stored. **Nothing is generated at runtime.**

Governing principle (from the spec): *TOC = order. Evidence = truth. Glossary = teaching bank. Video = support. Final Schema = arrangement and everything the learner touches.*

**Rules inherited from the glossary layer that the lessons obey:** a fact may only be tested after a *text* block has taught it (video does not count); every question traces question -> fact -> teaching block; answer keys are data predicates checked against the registered datasets, never typed numbers.

### 2.1 The Data Analyst path (regions and tile counts)

| Region | Tiles |
|---|---|
| Data Analysis Foundations | 2 |
| Python Fundamentals | 11 |
| Descriptive Statistics | 3 |
| Data Wrangling with pandas | 11 |
| SQL Fundamentals | 9 |
| Relational Data Modeling | 4 |
| SQL Joins and Advanced Querying | 3 |
| Spreadsheet Analysis | 11 |
| Data Visualization | 6 |
| A/B Testing and Experiment Literacy | 2 |
| Stakeholder Communication and Data Storytelling | 6 |
| Capstone Project | 4 |

Appendix A lists every tile in learning order with its concepts, step and interaction counts, requirements, assets, reward and `next_tile_id`.

### 2.2 Glossary content and where it is

The glossary bundle for this path has **168 concepts** (42 core, 86 standard, 40 reference depth), 115 video segments on 85 concepts, and the TOC's concept clusters. A bundle holds, per concept:

| Field | Meaning |
|---|---|
| `context` | concept_id, name, depth tier, toc_location (region/terrain/tile), `prerequisites`, `blocked_future_concepts` (concepts the lesson must not mention yet) |
| `coverage` | `learning_objective`, `required_facts[]` (`id`, `statement`, `source_refs` such as `openintro_statistics_textbook#1.2.1`), `misconceptions[]` |
| `teaching_blocks[]` | `id` (tb1...), `purpose` (intro, definition, example, misconception, takeaway...), `content` (the teaching text), `fact_ids` |
| `video_need` | level HIGH/MEDIUM/LOW/NONE, reason, preferred visual modes |
| `media` | group title and `segments[]`: `segment_id`, `video_id`, `youtube_url`, `review_url`, `start_seconds`, `end_seconds`, `fact_ids`, `label`, `summary` (learners see the summary, never the transcript) |
| `assessment_anchors[]` | `capability` + the `fact_ids` it measures. These become the `measures` of interactions (mastery tags) |
| `practice_anchor` | type (live_code, spreadsheet, field_selection, matching, ordering, external_proof, formula, UI_edit...) + objective + success criterion; for code, `live_code.allowed_syntax` / `blocked_syntax` |
| `visual_anchor` | type + purpose (the visual the concept wants) |
| `teaching_notes[]`, `cluster_ref`, `validation` | authoring guidance and readiness flags |

**All 168 concepts are exported in full (facts with sources, every teaching block, segments, anchors, notes) in `appendix_D_glossary_export.md`.** One concept, abbreviated, to show the shape (`blocked_future_concepts` omitted, it lists about 150 ids):

```json
{
 "context": {"concept_id": "data.dataset_rows_columns", "concept_name": "Rows, columns, and datasets", "path_id": "data_analyst", "depth_tier": "core",
   "toc_location": {"region_id": "region_data_analysis_foundations", "terrain_id": "terrain_data_analysis_foundations", "tile_id": "tile_data_shape_and_types"}, "prerequisites": []},
 "coverage": {"learning_objective": "Recognize that a dataset is organized as rows and columns, and identify what a row and a column each represent in a simple dataset.",
   "required_facts": [
     {"id": "f1", "statement": "A dataset is a collection of observations recorded on the same variables.", "source_refs": ["openintro_statistics_textbook#1.2.1"]},
     {"id": "f2", "statement": "Data is commonly organized as a table (data matrix) of rows and columns.", "source_refs": ["openintro_statistics_textbook#1.2.1"]},
     {"id": "f3", "statement": "In a data table (data matrix), each row represents one observation (one record).", "source_refs": ["openintro_statistics_textbook#1.2.1"]},
     {"id": "f4", "statement": "In a data table (data matrix), each column represents one variable: one attribute that is recorded for every observation.", "source_refs": ["openintro_statistics_textbook#1.2.1"]}], "misconceptions": []},
 "teaching_blocks": [{"id": "tb1", "purpose": "intro", "content": "Picture a week's worth of delivery orders for a small courier company ... (teaching text) ...", "fact_ids": ["f1"]}],
 "video_need": {"level": "LOW", "reason": "The row/column structure is a static layout ...", "preferred_visual_modes": ["data_table_demo"]},
 "media": null,
 "assessment_anchors": [{"fact_ids": ["f1", "f2"], "capability": "describe_dataset_structure"}, {"fact_ids": ["f3"], "capability": "identify_row_as_observation"}, {"fact_ids": ["f4"], "capability": "identify_column_as_variable"}],
 "practice_anchor": {"type": "field_selection", "objective": "Given a small table of delivery orders, mark which part answers each question: a whole row for one order, or a whole column for one attribute across all orders.", "success": "..."},
 "visual_anchor": {"type": "data_table", "purpose": "A small labelled table of delivery orders where one row and one column are visibly highlighted as an observation and a variable."},
 "teaching_notes": ["Learners have zero prior data vocabulary here ... establish 'row = one delivery' and 'column = one attribute' before anything else.", "Don't introduce the categorical/numeric distinction here ..."],
 "cluster_ref": "cluster_001", "validation": {"source_supported": true, "prerequisite_safe": true, "media_aligned": true, "ready_for_final_schema": true}
}
```

**The glossary is intellectual property sourced from third-party texts and YouTube segments.** The appendix D file is deliberately **not committed** to the public GitHub repository (it is listed in `.gitignore`); hand it over through a private channel. The repo is public today; decide whether it should stay so before the backend team's material is added.

The original glossary bundle lives at `UNIVERSAL_GLOSSARY_PIPELINE_PACK/batches/glossary_batch_001_data_analyst_pilot/path_glossary_bundle.data_analyst.json` (1.9 MB) on the author's machine and at `/home/ubuntu/inputs/path_glossary_bundle.data_analyst.json` on the generation instance. Every lesson records the sha256 of the bundle entry it was built from (`source.glossary_bundle_hashes`).

---

## 3. How the content is made (pipeline summary)

The pipeline (`00_FINAL_PIPELINE_CORE`, instructions in `01_FINAL_PACK_TEMPLATE`) turns a path's glossary bundle plus its TOC into tile lessons. Principles, each enforced by a script and not by trusting the model:

1. **Pre-authored, validated offline.** Models write content; scripts verify it.
2. **Structure by rule, content by model.** `plan_tiles.py` fixes which steps exist, their order, lineage, the planned interaction type and visual block type. The model fills them; the validator rejects any deviation.
3. **Outputs are computed, never typed.** Table results, chart data, expected values and code output come from executing on registered assets.
4. **Answer keys are data predicates** (`{where: {order_id: "NS1003"}, column: "delivery_minutes", expect_value: 41}`), checked against the dataset.
5. **Traceability.** Every question points to facts and teaching blocks; a question testing an untaught fact is rejected.
6. **Coverage both ways.** Every required fact is taught; every assessment anchor is measured; every practice anchor has a hands-on step; every visual anchor is realised.
7. **Fail closed.** A block, interaction or asset type with no checker is `UNVERIFIED` (an error under `--strict`), never a silent pass.
8. **Mutation-tested gates.** `selftest.py` deliberately breaks content in 13 known ways and asserts the validator catches each ("0 missed"). It must be re-run after any schema or checker change.

### 3.1 Stages (`pipeline_manifest.json`)

| # | Stage | Kind | What it does / produces |
|---|---|---|---|
| 00 | preflight | script | checks inputs, writes `batch_run_context.json`, stages inputs |
| 01 | scenario_assets | generator + evaluator | `scenario_asset_registry.json`: scenarios, datasets, code workspaces |
| 02 | tile_plan | script | `tile_plans.json`: the deterministic step skeleton per tile |
| 03 | screens | generator + evaluator | `screens.json`: explainer/video/recap steps, blocks, hints text, remediation steps |
| 04 | interactions | generator + evaluator | `interactions.json`: every question/exercise with public part, answer key, feedback, measures |
| 05 | code_exercises | planned | not used; code exercises are authored in 04 and executed by its gate |
| 06 | assemble | script | `tile_lessons/`, `tile_lessons_public/`, `grading/`; computes hashes, `requires`, pacing, media segments, execution provenance |
| 07 | validate | script | `validate_tile.py --strict` over every tile |
| 08 | pedagogy_review | evaluator | teaching quality review |
| 09 | leakage_check | evaluator | checks that prompts/hints/feedback do not give away answers |
| 10 | stage_gate_ledger | script | `final_stage_gate_ledger.json`: PASS/FAIL per stage with artifact hashes; `verify` detects any artifact edited after gating |
| 11 | final_audit | evaluator | independent audit |
| 12 | publish | planned | **not built** (needs the backend) |

Generator agents run on Claude Sonnet, evaluators on Opus, through AWS Bedrock (`us-east-1`). Models seen in the cost logs: Sonnet 4.6 and 4.5, Opus 4.6 and 4.5, Haiku 4.5.

Evaluator findings are `BLOCKING` (fails the round; up to 3 repair rounds) or `ADVISORY` (one reword-only repair). **Deterministic gates run before any evaluator**, so evaluators never pay to find what a script catches.

### 3.2 What the validator checks (`validate_tile.py`, `checkers/`)

- **Structure:** ids unique and prefixed by the tile id, remediation targets resolve, `requires` and `content_hash` are recomputed, bundle hashes match the glossary.
- **Lineage:** every fact, teaching-block and anchor id exists in the glossary bundle; media segments are verbatim copies.
- **Coverage / order / plan:** as in principles 5-6 above; steps must follow `tile_plans.json`.
- **Lint:** no "as the video shows", per-step word budget, mentions of blocked future concepts (advisory).
- **Pack checks, per type:** answer keys executed against the registered assets. For `code_exercise` and `formula_entry` the solution is **run in the real engine** (DuckDB-WASM, Pyodide, HyperFormula) and the tests must pass; the starter must not already pass; "hidden checks" (data mutations) must change the result so a hard-coded answer fails; the solution may only use syntax the concept has taught (except capstones, section 12).

### 3.3 Execution of batches

A *batch* is one run over a list of tiles (`batches/<id>/run_config.json`, `chunks.json`). The orchestrator is `run_pipeline.py` (AWS Bedrock, unattended): it walks the manifest, fans tiles out in chunks (a canary chunk first), runs gates, spends against a cap, resumes from the ledger after any stop, and stops with a written reason (`working/DRIVER_STOPPED.md`) after repeated failure or when the cap is hit. Twelve batches built the path:

| Batch | Tiles | Spend |
|---|---|---|
| 001 canary (orchestrator stand-in), 002 canary (LLM) | 1 | $25.00 (002) |
| 003 chunk (data foundations, Python basics, stats) | 9 | $240.87 |
| 004 chunk 2 (stats, capstone scaffolds) | 4 | $26.70 |
| 005 SQL canary | 2 | $14.88 |
| 006 SQL rest | 10 | $89.41 |
| 007 no-code (stakeholder, data quality) | 2 | $28.36 |
| 008 Python core | 11 | $102.48 |
| 009 pandas | 11 | $146.96 |
| 010 stats and capstones | 4 | $40.99 |
| 011 spreadsheet | 11 | $114.04 |
| 012 visualization | 6 | $124.64 |
| 013 stakeholder chart | 1 | $11.41 |

Batches 001-007 predate the unattended driver; their folders contain builder/patch scripts (`build_*.py`, `patch_*.py`) from how they were authored. They passed the same deterministic gates and ledger; check each batch's `final_stage_gate_ledger.json` for which stages had an evaluator. Batches 008-013 ran fully through the driver with evaluators.

---

## 4. The data contract: a tile lesson

A tile lesson is one JSON document (`tile_lessons/<tile_id>.json`). Authoritative definition: `00_FINAL_PIPELINE_CORE/schemas/tile_lesson.schema.json` (Appendix B has a field-by-field reference; Appendix E has real payloads).

```
tile_lesson {
  schema_version, kind: "tile_lesson", path_id, tile_id, title, summary,
  toc_location { region_id, terrain_id },
  concept_ids[],
  source { glossary_batch_id, toc_freeze_hash, glossary_bundle_hashes{concept_id -> sha256}, scenario_registry_hash },
  requires { min_player_version, packs[], block_types[], interaction_types[], runtimes[], asset_ids[] },   # capability negotiation
  pacing { estimated_minutes },
  steps[ step ],
  remediation_steps[ step ],
  completion { rule: "all_required_steps_complete", reward { gems }, next_tile_id },
  content_hash                         # sha256 of the lesson without this field
}
step {
  step_id  ("<tile_id>.sNN"; remediation steps "<tile_id>.rNN"),
  type: explainer | video | check | hands_on | recap,
  concept_ids[], eyebrow, title, lede,
  blocks[ typed block ],               # the visual / text content
  interaction { ... },                 # present on check and hands_on steps
  reward { gems, first_try_bonus? },
  lineage { concept_ids[], teaching_block_ids[], fact_ids[], anchors[] }
}
interaction {
  type, interaction_id ("ix.<tile_id>.sNN"), difficulty: intro|core|stretch,
  grading_mode: client|server, standalone: bool,
  measures[ {concept_id, capability, fact_ids[]} ],   # mastery tags from the glossary
  anchors[], 
  public  { ...what the learner sees... },
  grading { ...the answer key... },
  feedback { correct{message}, incorrect{message}, hints[], remediation_step_id? }
}
```

### 4.1 Stable ids and versioning

- Ids are deterministic (`<tile>.sNN`, `ix.<tile>.sNN`). If the plan for a tile is unchanged, regenerated content keeps the same ids, so **learner progress survives regeneration**. Store `content_hash` with progress rows to detect that a lesson changed under a learner.
- `content_hash` is recomputed by the validator; `source.*_hash` fields let you tell which glossary/TOC/registry version a lesson came from.

### 4.2 Three copies of each tile (`06_assemble` output)

| Path | Contents | Intended audience |
|---|---|---|
| `tile_lessons/<tile>.json` | full lesson including answer keys | internal / backend |
| `tile_lessons_public/<tile>.json` | what the backend serves to the player: `grading` removed from every interaction with `grading_mode: "server"` | player |
| `grading/<tile>.json` | the stripped answer keys for server-graded interactions | backend grading service |

**Fact you must act on:** in the current content **all 383 interactions are `grading_mode: "client"`**. So no answer key has been stripped yet: the "public" copies carry every key, including code solutions and hidden checks. The pipeline supports server grading (it strips and writes `grading/`), but nobody has flipped any assessment to `server`. The backend/product must decide which interactions (presumably the assessments that feed mastery) become server-graded, then either re-assemble with that setting or strip at publish time. The `grading/*.json` files in the batches are therefore empty objects.

### 4.3 Capability negotiation (`requires`)

`requires` is computed, never authored: it lists the block types, interaction types, packs, runtimes and asset ids a tile needs, and `min_player_version`. A player that lacks any of these must not open the tile. Packs: `core` (every role) and `data` (data_table, spreadsheet_grid, chart; table_select, find_issues, classify, formula_entry). Registry statuses are `draft` today; promote to `stable` when the player ships a component.

### 4.4 Blocks

14 block types are used (Appendix B documents all 16 defined). Each carries `block_id` (`<step_id>.bN`), a `role` where relevant, and `lineage`. Types and counts: prose 580, media_group 85 (video: the segments are copied verbatim from the glossary, with `summary` for video-off mode), up_next 71, before_after 56, diagram 31 (graph/erd/architecture/network/sequence/venn/tree/layers/mindmap/timeline/number_line/array/mapping/container; SVG-style structured data, not images), side_by_side 20, process_flow 18, heading 15, data_table 11, code_walkthrough 11, spreadsheet_grid 9, chart 7, callout 3, comparison 1.

- `data_table`, `spreadsheet_grid` and `chart` show **computed** values: the table result or cell values are produced by running the query/formula/dataset through the engines at assembly time (`computed_values`, `result_of`), never typed.
- `annotated_image` exists in the schema but is **unused**: the asset registry has no image assets and none can be generated, so screens use `diagram` or `spreadsheet_grid` instead.

### 4.5 Row and cell references

Lessons point at data with predicates, not row numbers: `{where: {order_id: "NS1003"}, occurrence: 0, column: "delivery_minutes"}` (`occurrence` picks among duplicates; default 0). The grader and player must resolve these the same way (`grader-core/src/data.ts`).

### 4.6 Video segments

`media_group` blocks hold verbatim glossary segments: `video_id`, `youtube_url`, `start_seconds`, `end_seconds`, `label`, `summary`. When a learner turns video off, render the `summary`. Videos are YouTube embeds of third-party content, selected from an allowlist of 43 channels; check embedding terms and availability at ingestion.

---

## 5. Interaction catalog (what the player renders, what the grader checks)

All 12 registered types, with counts in this path. The submission shapes are those `grader-core` accepts.

| Type | Pack | Count | Learner submits | Correct when | Feedback sources |
|---|---|---|---|---|---|
| `choice` | core | 215 | `{selected: [option_id]}` | selected set equals `grading.correct_option_ids` | `grading.option_feedback[option].message` for the first wrong option picked; generic `feedback.incorrect` |
| `ordering` | core | 5 | `{order: [item_id]}` | equals `correct_order` or any of `accepted_alternatives` | `loop_back_note` |
| `classify` | core | 10 | `{assignments: {item_id: bucket_id}}` | every item in its bucket (`grading.assignments`) | `item_feedback[item].message` |
| `match_pairs` | core | 0 | `{pairs: [{left,right}]}` | exact pair set | none authored |
| `short_answer` | core | 0 | `{text}` | in `accepted_answers`, or numeric within tolerance | none |
| `field_selection` | core | 0 | `{selected: [field_id]}` | every `required` picked, no `forbidden`, no `unneeded` | `outcome_messages` |
| `diagram_label` | core | 0 | `{placements: {label_id: target_id}}` | exact | none |
| `external_proof` | core | 8 | free text / file / link per `evidence_kinds` | **cannot be auto-graded**: `grading.mode` is `self_attest`, `rubric_ai` or `manual`; the grader returns `needs: "review"` | rubric `criterion` + `weight` |
| `table_select` | data | 19 | `{answers: {task_id: {row?: row_ref, column?}}}` | each task's row/column/cell matches the data predicate | `task_feedback[task].incorrect` |
| `find_issues` | data | 3 | `{flags: [{location: cell_ref, category_id}]}` | flags exactly the planted issues with the right category; decoy cells must not be flagged | `wrong_category_message`, decoy `message`, `completion_message` |
| `formula_entry` | data | 20 | `{formula: "=..."}` typed into `target_cell` | value equals `expected_value` (tolerance), uses `must_use_functions`, and gives the same result as `reference_formula` on altered data | generic |
| `code_exercise` | core | 103 | `{code: "<entry file text>"}` | see section 6 | per-test `message_on_fail` |

The four types with a count of 0 (`match_pairs`, `short_answer`, `field_selection`, `diagram_label`) are fully specified and implemented in the grader, but no Data Analyst tile uses them, so they have not been tested against real content. They exist for other paths.

Common to all: each interaction declares `measures` (concept + capability + fact ids) for mastery, a `difficulty`, a `hints[]` ladder in `feedback`, and optionally a `remediation_step_id` pointing to a `remediation_steps` entry (the conditional "go back and read this" step shown after a miss).

---

## 6. Code exercises, runtimes and hidden checks

### 6.1 The exercise object

```
interaction.type = "code_exercise"
public {
  prompt, runtime { kind: sql|python|chart_renderer|spreadsheet, version, packages[] },
  workspace { entry, files[ {path, role: editable|readonly, content} ],     # the starter code
              asset_mounts[ {asset_id, variant_id?, mount_path} ] },          # datasets copied into the sandbox
  constraints { allowed_syntax[], blocked_syntax[] }                          # copied verbatim from the glossary practice anchor
}
grading {
  tests[ {test_id, kind, spec, visible, message_on_fail} ],
  solution_files[ {path, content} ],                                          # the authored reference solution
  execution_provenance { runtime, runtime_version, solution_sha256, tests_passed },   # computed by a real run
  hidden_checks[ {check_id, test_id, mutation{table?, ops[]}, expected} ]     # computed by running the solution on mutated data
}
```

### 6.2 Test kinds per runtime

| Runtime | Test kinds | Notes |
|---|---|---|
| sql | `query_result_equals`, `forbidden_syntax` | spec: `expected {columns, rows}`, `ordered`, `tolerance`, `statement` (0-based statement index), `mount_variants` (re-run on another dataset variant). Column names compared case-insensitively. |
| python | `stdout_equals`, `value_equals` (an expression evaluated after the program), `dataframe_equals`, `function_call` (call a learner function with args), `forbidden_syntax` | stdout compared after trimming trailing whitespace per line |
| chart_renderer (matplotlib + seaborn on Pyodide) | `figure_equals`, `axes_property`, `plotted_data_equals`, `value_equals`, `stdout_equals` | graded on figure **structure** (chart types, titles, labels, tick labels, legend, scales, limits, the plotted numbers), never pixels or colours unless the concept teaches them |
| spreadsheet | `cell_equals`, `range_equals`, `formula_uses`, `forbidden_syntax` | the learner's file is lines `[Sheet!]A1: value-or-=formula` laid over the mounted CSVs |

### 6.3 Hidden checks (anti-hard-coding)

For every exercise the pipeline reruns the authored solution on deterministic mutations of the mounted data (drop first row, duplicate last row, drop last row, set a referenced cell to NULL or to another value) or, for Python/sheets, of constants in the starter (`set_variable`). Mutations that change the solution's result are stored as `hidden_checks` with the expected result. The grader reruns the *learner's* code on the same mutations; a typed-in or hard-coded answer fails. These checks are stored in `grading`, so they are part of the answer key and must stay server-side once grading moves server-side.

### 6.4 Pinned runtimes (`registry/runtimes.json`)

| Kind | Engine | Pinned version | Verified |
|---|---|---|---|
| sql | DuckDB-WASM | 1.32.0 | yes |
| python | Pyodide | 0.29.5 (numpy, pandas) | yes |
| chart_renderer | Pyodide + matplotlib 3.8.4 + seaborn 0.13.2 | 0.29.5 | yes |
| spreadsheet | HyperFormula | 3.4.0 | yes, **licence issue, section 12** |

`runtime.version` in each exercise must equal the pin, and the player must load **the same versions**, otherwise an authored correct answer can fail in the player. Packages are fetched at build time by `sandbox/fetch_packages.mjs` and never at runtime in the pipeline.

### 6.5 Engine contracts you will implement in the player

The pipeline's Node runners define the contract. They are in `00_FINAL_PIPELINE_CORE/sandbox/`:

- `run_sql.mjs`: job `{tables:[{name, columns:[{name,type}], rows}], scripts:[{id, statements[], tables?}]}`; each script runs in a **fresh database**; returns the last row-returning statement plus `outputs[i]` per statement. Output normalisation is part of the contract: DECIMAL values are scaled to numbers, DATE as `YYYY-MM-DD`, TIMESTAMP as `YYYY-MM-DD HH:MM:SS` (UTC), booleans, nulls, lists as arrays. External access is disabled and the configuration locked before any learner SQL runs.
- `run_py.mjs`: job `{packages, scripts:[{id, entry, files, mounts, probes, chart?}]}`; a fresh interpreter state per script; mounts are written as CSV files; probes evaluate an expression or call a function after the program runs; `chart` serialises every matplotlib figure to JSON (figures, axes, artists with their data). It contains the Python **harness** (value serialisation, figure serialiser, import blocking of the JS bridge). **Two compatibility patches live here and must be reproduced in the player:** `Axes.boxplot(tick_labels=...)` is aliased to `labels=` (matplotlib 3.8.4 predates the 3.9 name; the glossary teaches `tick_labels`), and `bar`/`hist`/`bxp` are wrapped to tag artists so the figure serialiser can tell bars from histograms and boxplots.
- `run_sheet.mjs`: job `{scripts:[{id, content, sheets:[{name, columns, rows}], probes}]}`; builds a fresh HyperFormula workbook per script (header in row 1, data from row 2; the file's cells are overlaid); probes read cells or ranges; error cells read as their text (`#DIV/0!`), empty cells as null.

All three run under Node's permission model in the pipeline (no filesystem writes, no child processes, network globals removed). The browser sandbox in the player needs equivalent isolation for learner code.

---

## 7. Assets and datasets

Stage 01 writes `scenario_asset_registry.json` per batch: `scenarios[]` (a business story such as the Lagos delivery company) and `assets[]` of kind `dataset` (inline `columns` with type/semantic role/description, and `rows`; optional `variants[]` derived by declared ops such as `set_cell`, `duplicate_row`, `drop_rows`, `drop_columns`, used to plant data-quality issues and to give hidden-test variants) or `code_workspace`. Lessons reference datasets by `asset_ref {asset_id, variant_id, columns}`. Rows are inline JSON (small teaching datasets: 3 to about 40 rows). Full inventory in Appendix C.

### 7.1 CRITICAL: asset ids collide across batches

Each batch has its own registry, and **seven asset ids occur in several batches with different content**:

| asset_id | Appears in | Differences |
|---|---|---|
| `ds_orders` | 003, 006, 008, 009 | 7, 13, 15, 14 rows, different columns |
| `ds_customers` | 003, 006, 009 | 5, 6, 15 rows, 009 has different columns |
| `ds_order_items` | 003, 006 | different columns |
| `ds_city_delivery_summary` | 003, 004 | different columns |
| `ds_capstone_orders` | 004, 010 | 12 vs 34 rows, different columns |
| `ds_capstone_drivers` | 004, 010 | different columns |
| `ds.orders` | 005, 012 | 10 vs 24 rows, different columns |

A lesson names only the `asset_id`; the registry it was validated against is identified by `source.scenario_registry_hash`. **A backend that stores assets keyed by `asset_id` alone will serve the wrong data to some lessons and silently break answer keys.** Key assets by `(scenario_registry_hash, asset_id)` or by a content hash, and resolve a tile's assets through the registry its `source.scenario_registry_hash` names. (A cleaner fix is a later pipeline change to make ids globally unique per path; none was made.)

The scenario names also differ between batches (different fictional companies), which is why this matters for coherence as well: a learner may see different stories for "orders" in different tiles.

---

## 8. The shared grader (`grader-core/`)

A zero-dependency TypeScript package (runs natively on Node 22.18+; no build step) used by the player, the backend and the pipeline's checks, so an authored correct answer passes everywhere and each wrong answer gives its authored feedback.

```ts
import { gradeInteraction } from "grader-core/src/index.ts";
const result = await gradeInteraction(interaction, submission, { registry, sql, py, sheet });
// { correct: boolean | null, score: 0..1, feedback: string | null, parts?: Record<string, boolean>, needs?: "runtime" | "review" }
```

- Non-code types are pure functions. Code types take **injected engines** with the job shapes of section 6.5; a missing engine returns `needs: "runtime"` instead of guessing; `external_proof` returns `needs: "review"`.
- The comparison rules are line-for-line ports of the pipeline's reference graders (`scripts/checkers/sandbox.py`: `grade_learner`, `grade_learner_py`, `grade_learner_sheet`, `formula_entry_outcome`). The player is required to behave identically.
- Verified by replaying every authored answer key through it (`grader-core/test/`, run with `node --test`): the authored solution passes, and the starter code, an empty program and a typed-in constant all fail. Results: 1,164 (non-code, including each wrong choice option yielding its own authored feedback), 27 (SQL, all 26 exercises), 54 (Python, all 53 exercises plus a helper test), 17 (charts, all 16), 9 (sheets, all 8), 21 (formula entries, all 20). Node adapters in `test/node-engines.ts` show how an engine is plugged in.

**Known gaps:**
1. `forbidden_syntax` tests for Python and spreadsheets come back in `unchecked` (they need a Python/formula parser). SQL forbidden syntax is detected for the four descriptors the lessons use (DISTINCT, WHERE, CASE, table alias). No finished tile uses a Python or sheet `forbidden_syntax` test as a graded rule, but the pipeline's gate does check the *authored* solution against `allowed_syntax`/`blocked_syntax`. Whether to enforce the allowed-syntax list on **learner** code is a product decision (the player could parse with Python's `ast` in Pyodide).
2. The Python harness exists only inside `run_py.mjs`. Before the player integration, extract it into one shared file that the pipeline and the player both load (touches the sandbox; needs a selftest).
3. Tested only in Node. The browser (Pyodide, DuckDB-WASM in a worker, HyperFormula) needs its own end-to-end test.

---

## 9. Quality evidence and its limits

- Every tile passed: schema validation, the deterministic `--strict` validator including real execution of every answer key, the pedagogy review, the leakage check, the ledger verification and an independent final audit (batches 008-013 with evaluators; see the caveat in 3.3 for 001-007).
- `selftest.py`: 13 mutations, 0 missed, rerun after every checker change (last: after the capstone exemption).
- Grader replay: all authored answers pass, all starter/empty/constant answers fail.
- **Not done: human review.** No person has read the lessons. LLM evaluators and scripts are strong on structure, lineage, answer correctness and leakage and weak on tone, pedagogy subtleties and cultural fit. A spot check of tiles from every region before launch is strongly recommended.
- Content correctness of facts rests on the glossary's sourced facts (OpenIntro statistics text and other sources listed in `source_refs`); the pipeline checks lessons against the glossary, not against the world.

---

## 10. What the backend needs to build (recommendations)

Everything in this section is a recommendation derived from the contracts above, not something already built or decided.

### 10.1 Entities

| Entity | Key | Notes |
|---|---|---|
| Path | `path_id` | one row per career path |
| Region / Terrain | `region_id`, `terrain_id` | from the TOC, ordered |
| Tile | `tile_id` | ordered; `next_tile_id` is in `completion` |
| TileVersion | `(tile_id, content_hash)` | immutable; the public lesson JSON; `requires`; `source.*` hashes |
| TileGrading | `(tile_id, content_hash)` | server-side answer keys (`grading/<tile>.json`); never returned to clients |
| Concept | `concept_id` | name, depth tier, prerequisites (for mastery graphs and review) |
| Asset | `(scenario_registry_hash, asset_id)` | dataset rows/columns/variants or code workspaces; section 7.1 |
| MediaSegment | `segment_id` | from the lesson blocks; verify availability |
| Learner progress | `(learner, tile_id)` + step completion | store `content_hash` and `step_id` |
| Attempt | `(learner, interaction_id, n)` | submission, result, hints used, time, `content_hash` |
| Mastery | `(learner, concept_id, capability)` | updated from attempts via `measures` |
| Rewards | ledger of gems | amounts are config in the lesson (`reward`, `first_try_bonus`) |

### 10.2 Publish (pipeline stage 12, to be written once the store exists)

For each tile in `tile_lessons/`: validate against `tile_lesson.schema.json`; recompute and compare `content_hash`; resolve and store its assets under `(scenario_registry_hash, asset_id)`; store the public lesson (after deciding which interactions are server-graded and stripping their `grading`); store the grading part privately; register `requires`; write the tile order from the TOC; make publication atomic per path so a learner never sees half an update. `12_publish/RUN.md` holds the original sketch (object storage + DB rows keyed by `tile_id`/`content_hash`; merge reusable assets into a cross-path registry by `concept_id`).

### 10.3 Runtime flow

1. Player asks for the next tile; the backend checks `requires` against the player's capabilities and returns the public lesson (and the assets).
2. For `client`-graded interactions the player calls `grader-core` locally and shows the authored feedback; it reports the attempt to the backend. For `server`-graded ones the player sends the submission and the backend runs `grader-core` with server-side engines (Node versions of DuckDB, Pyodide, HyperFormula work today, see `sandbox/`).
3. The backend updates mastery from `measures` (concept + capability, with the fact ids) and step completion; hints and `remediation_step_id` drive conditional steps; rewards come from the lesson config.
4. Review/spaced repetition: draw from `standalone: true` interactions (43 today).

### 10.4 Security

Anything in `grading` (keys, `solution_files`, `hidden_checks`, `reference_formula`, `expected_value`) lets a learner skip learning. Decide the client/server split deliberately (4.2). Learner-submitted code runs only in an isolated browser sandbox or a locked-down server worker (the pipeline's Node permission flags and the DuckDB `lock_configuration` / `enable_external_access=false` pattern are the reference). Datasets are teaching data with no personal data.

### 10.5 Regeneration

Ids are stable when the plan is unchanged, so a regenerated tile can replace its predecessor. Gate it by comparing `content_hash`; migrate progress rows by `step_id`, and flag attempts recorded against an older hash.

---

## 11. Decisions made on the way, and why (for the backend's awareness)

| Decision | Why / consequence |
|---|---|
| Content is pre-authored; no runtime generation | principle 1; a later "custom path" product may reuse these schemas as its output contract |
| Client-graded checks, server-graded assessments (the intent) | **not implemented in content**: all 383 are `client` today (4.2) |
| Datasets/spreadsheets are a pack, not the core model | for Data Analyst only 27 of 163 visual anchors are data/spreadsheet/chart; most are core visuals |
| `UI_edit` practice anchors (drag-to-edit) mapped to `classify`/`find_issues` | there is no drag-edit interaction type. The stakeholder tile that wanted it, `tile_stakeholder_chart_matching_simplifying`, makes learners sort chart elements into keep/remove. A true drag-edit type can be added later (schema, registry, checker, player component). |
| Capstone exercises skip the allowed-syntax gate | capstone concepts are integration tasks using everything taught before, while the glossary anchor lists almost nothing as allowed; the code must still run, pass its tests and depend on the data (`SYNTAX_EXEMPT_PREFIXES = ("capstone.",)` in `checkers/sandbox.py`) |
| `annotated_image` not used | no image assets exist; replaced by `diagram`/`spreadsheet_grid` |
| matplotlib 3.8.4 with a `boxplot(tick_labels=)` alias | the player's Pyodide must apply the alias (6.5) |
| HyperFormula 3.4.0 for spreadsheets | GPL-3.0 here; **commercial or alternative engine decision needed** (section 12) |
| Pyodide for Python/charts, DuckDB-WASM for SQL | verified end to end; all run in the browser |
| `plan_tiles.py` maps capstone concepts to runtimes by exact concept id | `registry/path_profiles/data_analyst.json` `runtime_by_concept_prefix` now accepts full concept ids |
| Repo is public, `working/` folders are tracked | simplest while unattended; untracking would make a `git pull` on the instance delete run state; see section 13 |

---

## 12. Known limitations and open items

1. **No backend, no publish, no player integration.** This document is their input.
2. **All interactions are client-graded** (4.2). Answer keys, solutions and hidden checks currently ship in the "public" copies.
3. **Asset id collisions** (7.1): required handling in the store.
4. **HyperFormula licence** (GPL-3.0 as used; commercial licence or an alternative engine for a proprietary product). Needs a legal decision.
5. **No human review** of the lessons (9).
6. **Python/sheet `forbidden_syntax` and allowed-syntax enforcement on learner code** are not in the grader (8).
7. **Grader untested in a browser** (8).
8. **Python harness duplication risk**: the player must reproduce the harness and the two matplotlib patches exactly, or extract the harness to a shared file (6.5, 8).
9. **Real drag-edit interaction** (`UI_edit`) and `tool_simulation` types do not exist. Needed for non-coding paths (cyber, devops, marketing tools).
10. **Cost**: $965.74 for this path, above the plan's target (1). Later paths should benefit from the checkers and fixed generator instructions; budget conservatively.
11. **Glossary IP** is in this handoff (Appendix D, not committed). The GitHub repo is public.
12. **The TOC and glossary are upstream and frozen**; problems found in them were not edited, only logged. Re-running a path needs the same frozen inputs.
13. **Other paths**: only a second TOC workspace (`05_react_V2_WORKSPACE`) exists locally; no glossary or lessons for it. Running the pipeline for a new role follows `01_FINAL_PACK_TEMPLATE/NEW_ROLE_RUNBOOK.md` (add a path profile, run `visual_inventory.py` to see which block/runtime types the role needs, build missing runners).

---

## 13. Operations: how this was run, and how to run it again

### 13.1 Repository layout (`github.com/Poll027/devspace-final-schema-pipeline`)

```
00_FINAL_PIPELINE_CORE/   PLAYBOOK.md (the spec)  pipeline_manifest.json
  schemas/   one JSON Schema per block (block.*), interaction (ix.*), plus tile_lesson, step, common, plan, parts, ledger
  registry/  block_registry, interaction_registry, anchor_mapping, runtimes, path_profiles/<path>.json
  scripts/   the stages, run_pipeline.py (driver), bedrock_agent.py, schema_check.py, selftest.py, checkers/{core,data,code,sandbox,pysyntax,sqlsyntax,sheetsyntax,dataset}.py
  sandbox/   run_sql.mjs, run_py.mjs, run_sheet.mjs, fetch_packages.mjs, package.json (DuckDB-WASM, Pyodide, HyperFormula)
01_FINAL_PACK_TEMPLATE/   START_HERE.md  NEW_ROLE_RUNBOOK.md  <stage>/{GENERATOR,EVALUATOR,RUN}.md   # the instructions the model agents read
batches/<batch_id>/       every artifact of one batch (run_config, chunks, registry, screens, interactions, tile_lessons*, grading, ledger, reports, working/)
grader-core/              the shared grader (section 8)
deploy/                   supervisor.py, install_service.sh, install_ops.sh, ops_sync.py, prepare.sh, status.sh, aws_budget_alarms.sh
docs/handoff/             this document, build_appendices.py, appendices A-E
BACKEND_DECISIONS.md      the short list of decisions deferred until the backend starts
```

### 13.2 Running a batch

`01_FINAL_PACK_TEMPLATE/START_HERE.md` is the loop. In short: write `batches/<id>/run_config.json` (path id, glossary bundle path, TOC workspace, tile ids) and `chunks.json`; run `python3 00_FINAL_PIPELINE_CORE/scripts/run_pipeline.py batches/<id> --max-usd <cap> --selftest-batch batches/<a passing batch>` (the selftest must report 0 missed before spending). A stop writes `working/DRIVER_STOPPED.md`; fix the cause and rerun the same command, finished stages are skipped. Never edit a gated artifact or hand-edit the ledger (`update_ledger.py` is the only writer).

### 13.3 The unattended setup used (AWS)

- One EC2 Ubuntu instance (it was scaled to a c6i.2xlarge for parallel batches; it can be downsized now that generation is complete), Bedrock in `us-east-1`. Each batch runs as a `systemd` service (`deploy/install_service.sh`), restarted automatically on crashes, with a spend cap per batch ($125, raised to $175 where needed) and SNS email on stop/done. Concurrency was `CHUNK_WORKERS=2` per batch with up to 3-4 batches in parallel, bounded by Bedrock throttling.
- An ops timer (`deploy/ops_sync.py`, every 5 minutes) publishes a status snapshot (services, log tails, stop reasons, spend) to an `ops-status` branch and restarts a *stopped* service after pulling a newer `main`; it never touches a running service.
- A scheduled cloud routine (hourly) read the `ops-status` branch, diagnosed stops and pushed instruction or checker fixes to `main` (with a selftest for code changes). This is how most overnight stops were repaired without a person.
- Secrets (GitHub token, SNS topic ARN, key pair) live only on the instance and the owner's machine, never in the repo.

### 13.4 What went wrong and what it taught (condensed; the commit log has the details)

- **Generators repair the wrong thing**: told to fix "differs from anchor" errors, they widened `constraints.allowed_syntax`; told to avoid untaught syntax they rewrote constraints. Fixed with explicit generator rules ("never widen constraints; change the solution or the task") and by routing teaching gaps to the stage that owns them.
- **Teaching gaps surfaced in stage 04** (a question tests a fact no text taught): the driver now sends those facts to the screens generator, then re-records the stage-03 gate.
- **Checker false positives** were the largest source of waste: library keywords (`data=`, `x=`, `y=`), literals in example calls, `math.sqrt`, starter-code imports; each was fixed in `pysyntax.py` with a selftest.
- **Spec/syntax conflicts**: a concept can require a construct its anchor does not allow (capstones, a pandas tile needing `def`), the root of several 3-round stops; resolved case by case (section 11).
- **Runtime compatibility**: the glossary taught `tick_labels` (matplotlib 3.9) while Pyodide ships 3.8.4; aliased.
- **Operational**: concurrent self-tests overwriting a shared scratch folder; a code pull under a running sibling tripping the integrity guard (the guard hashes agent-writable paths); a diverged local commit blocking `git pull --ff-only`; Bedrock throttling needing retry/backoff; an instance too small for parallel batches.
- **Driver bug**: after the teaching-gap fix rewrote `screens.json`, the stage-03 gate was not re-recorded, so the final ledger check failed as STALE (fixed in `e65147e`).

### 13.5 Conventions to keep

Scripts before evaluators; deterministic ids; no content authored by the orchestrator; `selftest.py` after any schema/checker change; never edit frozen TOC or glossary inputs; the ledger is written only by `update_ledger.py`.

---

## 14. Suggested order of work for the backend team

1. Read sections 4-8 and skim Appendix E; open one tile in `batches/final_batch_008_da_python_core/tile_lessons_public/`.
2. Decide: client vs server grading (4.2), asset keying (7.1), HyperFormula licence (12.4), whether the repo stays public (12.11).
3. Build the store and the ingestion (10.1-10.2) and ingest all 72 tiles from `batches/*/tile_lessons*/` (latest batch wins; `tile_data_shape_and_types` exists in 001 and 002, take 002; Appendix A names the source batch per tile).
4. Wire `grader-core` into the player with browser engines; run `grader-core/test` as the acceptance test for the player's engines (replay the authored answers through the browser).
5. Add mastery from `measures`, progress with `content_hash`, rewards, and the review flow from `standalone` interactions.
6. Human-review a sample from every region; then publish.

---

## 15. Appendices (in `docs/handoff/`)

| File | Contents | Committed |
|---|---|---|
| `appendix_A_tile_catalog.md` | all 72 tiles in learning order: concepts, steps, interactions, blocks, assets, reward, next tile, source batch, content hash | yes |
| `appendix_B_schema_reference.md` | field-by-field reference of the tile lesson, step, common definitions, all 16 block types and 12 interaction types, with registry status | yes |
| `appendix_C_assets.md` | every dataset and code workspace with columns, row counts, variants, plus the cross-batch collision list | yes |
| `appendix_D_glossary_export.md` | all 168 concepts: sourced facts, teaching text, media segments, anchors, notes, clusters (about 0.8 MB) | **no, IP; share privately** |
| `appendix_E_examples.md` | one real, complete payload per interaction type and runtime, and an example explainer step | yes |
| `build_appendices.py` | regenerates A-E from the repo's artifacts: `python3 docs/handoff/build_appendices.py --toc <toc.json> --glossary <bundle.json>` | yes |

Other primary sources: `00_FINAL_PIPELINE_CORE/PLAYBOOK.md` (the spec), `grader-core/README.md`, `BACKEND_DECISIONS.md`, `01_FINAL_PACK_TEMPLATE/START_HERE.md`.

---

## 16. Glossary of terms

**Region / Terrain / Tile / Concept unit**: the TOC hierarchy; a tile is the learner-facing lesson. **Bundle**: one concept's glossary entry. **Fact**: a sourced statement the lesson must teach (`f1`...). **Teaching block**: a unit of teaching text (`tb1`...). **Anchor**: glossary intent for an assessment, a practice activity or a visual; the pipeline authors the concrete version. **Capability**: a named skill an assessment measures; the unit of mastery. **Pack**: a set of block types, interaction types, asset kinds and their checker. **Batch**: one run of the pipeline over a list of tiles. **Chunk**: a group of tiles processed together; the first is the canary. **Gate**: a deterministic check that must pass before a stage counts. **Ledger**: the per-batch record of gate results with artifact hashes. **Hidden check**: a stored result of the authored solution on mutated data, used to catch hard-coded answers. **Standalone**: an interaction understandable without its tile, reusable for review. **Remediation step**: a conditional step shown after a miss. **Content hash**: sha256 of a lesson, used to version it.
