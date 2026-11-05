# Appendix B: Schema reference

Generated from `00_FINAL_PIPELINE_CORE/schemas/*.json` and `registry/*.json`. The JSON Schemas are the contract: validate every lesson you ingest against them (`scripts/schema_check.py` does, with `jsonschema` Draft 2020-12 and cross-file `$ref`s).

## Tile lesson (the unit the backend stores)
File: `schemas/tile_lesson.schema.json`

- `schema_version` *(required)*: string (min 1 chars)
- `kind` *(required)*: const 'tile_lesson'
- `path_id` *(required)*: id
- `tile_id` *(required)*: id
- `toc_location`: object
  - `region_id` *(required)*: id
  - `terrain_id` *(required)*: id
- `title` *(required)*: string (min 1 chars)
- `summary`: string
- `concept_ids` *(required)*: array of id
- `source` *(required)*: object
  - `glossary_batch_id` *(required)*: string (min 1 chars)
  - `toc_freeze_hash`: sha256
  - `glossary_bundle_hashes` *(required)*: object
  - `scenario_registry_hash` *(required)*: sha256
- `requires` *(required)*: object
  - `min_player_version` *(required)*: string (min 1 chars)
  - `packs`: array of string
  - `block_types` *(required)*: array of string
  - `interaction_types` *(required)*: array of string
  - `runtimes`: array of string
  - `asset_ids` *(required)*: array of id
- `pacing`: object
  - `estimated_minutes`: number
- `steps` *(required)*: array of step.schema.json
- `remediation_steps`: array of step.schema.json
- `completion` *(required)*: object
  - `rule` *(required)*: enum all_required_steps_complete
  - `reward`: reward
  - `next_tile_id`: ['string', 'null']
- `content_hash`: sha256

## Step
File: `schemas/step.schema.json`

- `step_id` *(required)*: id
- `type` *(required)*: enum explainer | video | check | hands_on | recap | remediation
- `required`: boolean
- `concept_ids` *(required)*: array of id
- `eyebrow`: string
- `title` *(required)*: string (min 1 chars)
- `lede`: string
- `blocks`: array of block_union.schema.json
- `interaction`: interaction_union.schema.json
- `reward`: reward
- `lineage` *(required)*: lineage

## Shared definitions (`$defs`)
File: `schemas/common.schema.json`

### `id`
`{"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.:#\\-]*$", "maxLength": 160}`

### `sha256`
`{"type": "string", "pattern": "^[a-f0-9]{64}$"}`

### `text`
`{"type": "string", "minLength": 1, "maxLength": 1500}`

### `scalar`
`{"type": ["string", "number", "boolean", "null"]}`

### `where`
`{"type": "object", "minProperties": 1, "additionalProperties": {"type": ["string", "number", "boolean", "null"]}}`

### `row_ref`
- `where` *(required)*: where
- `occurrence`: integer

### `cell_ref`
- `where` *(required)*: where
- `occurrence`: integer
- `column` *(required)*: string (min 1 chars)

### `target`
- `kind` *(required)*: enum row | column | cell
- `row`: row_ref
- `column`: string (min 1 chars)

### `asset_ref`
- `asset_id` *(required)*: id
- `variant_id`: ['string', 'null']
- `columns`: ['array', 'null']
- `max_rows`: ['integer', 'null']

### `lineage`
- `concept_ids`: array of id
- `fact_ids`: array of id
- `teaching_block_ids`: array of id
- `segment_ids`: array of id
- `anchors`: array of id

### `reward`
- `gems`: integer
- `first_try_bonus`: integer

### `measures`
`{"type": "array", "items": {"type": "object", "properties": {"concept_id": {"$ref": "#/$defs/id"}, "capability": {"type": "string", "minLength": 1}, "fact_ids": {"type": "array", "items": {"$ref": "#/$defs/id"}, "minItems": 1}}, "additionalProperties": false, "required": ["concept_id", "capability",`

### `feedback`
- `correct` *(required)*: object
  - `message` *(required)*: text
  - `coach`: string
- `incorrect` *(required)*: object
  - `message` *(required)*: text
  - `coach`: string
- `hints`: array of text
- `remediation_step_id`: id

## Block types

| type | pack | status | min player |
|---|---|---|---|
| prose | core | draft | 0.1.0 |
| heading | core | draft | 0.1.0 |
| callout | core | draft | 0.1.0 |
| concept_chips | core | draft | 0.1.0 |
| up_next | core | draft | 0.1.0 |
| media_group | core | draft | 0.1.0 |
| comparison | core | draft | 0.1.0 |
| process_flow | core | draft | 0.1.0 |
| diagram | core | draft | 0.1.0 |
| annotated_image | core | draft | 0.1.0 |
| code_walkthrough | core | draft | 0.1.0 |
| data_table | data | draft | 0.1.0 |
| spreadsheet_grid | data | draft | 0.1.0 |
| chart | data | draft | 0.1.0 |
| before_after | core | draft | 0.1.0 |
| side_by_side | core | draft | 0.1.0 |

### Block `prose` (core)
- `type` *(required)*: const 'prose'
- `block_id`: id
- `text` *(required)*: text
- `role`: enum intro | definition | mechanism | example | misconception | takeaway | syntax | workflow | practical_context | mental_model | walkthrough
- `lineage`: lineage

### Block `heading` (core)
- `type` *(required)*: const 'heading'
- `block_id`: id
- `text` *(required)*: string (min 1 chars)
- `level`: enum 2 | 3

### Block `callout` (core)
- `type` *(required)*: const 'callout'
- `block_id`: id
- `tone` *(required)*: enum info | tip | warning | misconception
- `text` *(required)*: text
- `lineage`: lineage

### Block `concept_chips` (core)
- `type` *(required)*: const 'concept_chips'
- `block_id`: id
- `items` *(required)*: array of object
  - `concept_id` *(required)*: id
  - `label` *(required)*: string (min 1 chars)
  - `short_text` *(required)*: text

### Block `up_next` (core)
- `type` *(required)*: const 'up_next'
- `block_id`: id
- `title` *(required)*: string (min 1 chars)
- `text`: string

### Block `media_group` (core)
- `type` *(required)*: const 'media_group'
- `block_id`: id
- `group_title`: string
- `segment_ids` *(required)*: array of id
- `segments`: array of object
  - `segment_id` *(required)*: id
  - `video_id` *(required)*: string (min 1 chars)
  - `youtube_url` *(required)*: string (min 1 chars)
  - `review_url`: string (min 1 chars)
  - `start_seconds` *(required)*: integer
  - `end_seconds` *(required)*: integer
  - `label`: string
  - `summary` *(required)*: text
  - `fact_ids`: array of id
  - `transcript_ref`: string (min 1 chars)
- `bridge`: object
  - `before`: string
  - `after`: string
- `default_mode`: enum video | summary

### Block `comparison` (core)
- `type` *(required)*: const 'comparison'
- `block_id`: id
- `title`: string
- `columns` *(required)*: array of object
  - `id` *(required)*: id
  - `label` *(required)*: string (min 1 chars)
- `rows` *(required)*: array of object
  - `criterion` *(required)*: string (min 1 chars)
  - `cells` *(required)*: object
- `lineage`: lineage

### Block `process_flow` (core)
- `type` *(required)*: const 'process_flow'
- `block_id`: id
- `title`: string
- `direction`: enum TB | LR
- `nodes` *(required)*: array of object
  - `id` *(required)*: id
  - `label` *(required)*: string (min 1 chars)
  - `kind`: enum start | end | step | decision | io | subprocess
  - `detail`: string
- `edges` *(required)*: array of object
  - `from` *(required)*: id
  - `to` *(required)*: id
  - `label`: string
  - `kind`: enum next | yes | no | loop_back | branch
- `reveal`: enum all | stepwise
- `alt_text` *(required)*: string (min 1 chars)
- `lineage`: lineage

### Block `diagram` (core)
- `type` *(required)*: const 'diagram'
- `block_id`: id
- `diagram_kind` *(required)*: enum (14 values)
- `title`: string
- `nodes` *(required)*: array of object
  - `id` *(required)*: id
  - `label` *(required)*: string (min 1 chars)
  - `kind`: string
  - `group`: string
  - `fields`: array of string
  - `value`: number
  - `range`: array of number
- `edges`: array of object
  - `from` *(required)*: id
  - `to` *(required)*: id
  - `label`: string
  - `cardinality`: enum 1:1 | 1:N | N:1 | N:N
  - `order`: integer
  - `directed`: boolean
- `layout`: enum auto | manual
- `positions`: object
- `alt_text` *(required)*: string (min 1 chars)
- `lineage`: lineage

### Block `annotated_image` (core)
- `type` *(required)*: const 'annotated_image'
- `block_id`: id
- `asset_id` *(required)*: id
- `alt_text` *(required)*: string (min 1 chars)
- `hotspots`: array of object
  - `x` *(required)*: number
  - `y` *(required)*: number
  - `w` *(required)*: number
  - `h` *(required)*: number
  - `label` *(required)*: string (min 1 chars)
  - `detail`: string
- `lineage`: lineage

### Block `code_walkthrough` (core)
- `type` *(required)*: const 'code_walkthrough'
- `block_id`: id
- `language` *(required)*: enum python | sql | javascript | typescript | jsx | css | html | bash | r | excel_formula
- `code` *(required)*: string (min 1 chars)
- `annotations`: array of object
  - `start_line` *(required)*: integer
  - `end_line` *(required)*: integer
  - `text` *(required)*: string (min 1 chars)
- `reveal`: enum all | line_by_line
- `output`: object
  - `kind` *(required)*: enum text | table
  - `text`: string
  - `asset_ref`: asset_ref
- `execution_provenance`: object
  - `runtime`: string (min 1 chars)
  - `runtime_version`: string (min 1 chars)
  - `code_sha256`: sha256
  - `output_sha256`: sha256
- `lineage`: lineage

### Block `data_table` (data)
- `type` *(required)*: const 'data_table'
- `block_id`: id
- `asset_ref`: asset_ref
- `caption`: string
- `highlight`: array of object
  - `target` *(required)*: target
  - `label`: string
  - `tone`: enum focus | good | bad | neutral
- `tag_columns`: array of object
  - `column` *(required)*: string (min 1 chars)
  - `tag` *(required)*: string (min 1 chars)
  - `tone`: enum focus | good | bad | neutral
- `inspect`: object
  - `enabled` *(required)*: boolean
  - `caption_template`: string
  - `id_column`: string
- `lineage`: lineage
- `result_of`: object
  - `runtime` *(required)*: enum sql
  - `sql` *(required)*: string (min 1 chars)
  - `asset_mounts` *(required)*: array of object
    - `asset_id` *(required)*: id
    - `variant_id`: ['string', 'null']
    - `mount_path` *(required)*: string (min 1 chars)
- `result`: object
  - `columns` *(required)*: array of string
  - `rows` *(required)*: array of array
  - `execution_provenance`: object
    - `runtime`: string
    - `runtime_version`: string
    - `sql_sha256`: sha256

### Block `spreadsheet_grid` (data)
- `type` *(required)*: const 'spreadsheet_grid'
- `block_id`: id
- `asset_ref` *(required)*: asset_ref
- `sheet_name`: string
- `range` *(required)*: string
- `show_formula_bar`: boolean
- `cells`: array of object
  - `ref` *(required)*: string
  - `formula`: string
  - `note`: string
- `selection`: string
- `annotations`: array of object
  - `target` *(required)*: string (min 1 chars)
  - `text` *(required)*: string (min 1 chars)
- `computed_values`: object
- `lineage`: lineage

### Block `chart` (data)
- `type` *(required)*: const 'chart'
- `block_id`: id
- `chart_kind` *(required)*: enum bar | line | scatter | histogram | box | pie | heatmap
- `asset_ref` *(required)*: asset_ref
- `title` *(required)*: string (min 1 chars)
- `alt_text` *(required)*: string (min 1 chars)
- `encoding` *(required)*: object
  - `x` *(required)*: object
    - `field` *(required)*: string (min 1 chars)
    - `type` *(required)*: enum quantitative | ordinal | nominal | temporal
    - `title`: string
  - `y`: object
    - `field` *(required)*: string (min 1 chars)
    - `type` *(required)*: enum quantitative | ordinal | nominal | temporal
    - `aggregate`: enum sum | mean | median | count | min | max
    - `title`: string
  - `color`: object
    - `field` *(required)*: string (min 1 chars)
- `annotations`: array of object
  - `text` *(required)*: string (min 1 chars)
  - `target`: string
- `lineage`: lineage

### Block `before_after` (core)
- `type` *(required)*: const 'before_after'
- `block_id`: id
- `before` *(required)*: one of several shapes
- `after` *(required)*: one of several shapes
- `change_summary` *(required)*: text
- `lineage`: lineage

### Block `side_by_side` (core)
- `type` *(required)*: const 'side_by_side'
- `block_id`: id
- `left` *(required)*: one of several shapes
- `right` *(required)*: one of several shapes
- `left_label` *(required)*: string (min 1 chars)
- `right_label` *(required)*: string (min 1 chars)
- `takeaway` *(required)*: text
- `lineage`: lineage

## Interaction types

| type | pack | status |
|---|---|---|
| choice | core | draft |
| table_select | data | draft |
| find_issues | data | draft |
| ordering | core | draft |
| classify | core | draft |
| match_pairs | core | draft |
| field_selection | core | draft |
| formula_entry | data | draft |
| code_exercise | core | draft |
| short_answer | core | draft |
| external_proof | core | draft |
| diagram_label | core | draft |

### Interaction `choice` (core)
- `type` *(required)*: const 'choice'
- `interaction_id` *(required)*: id
- `difficulty`: enum intro | core | stretch
- `grading_mode`: enum client | server
- `standalone`: boolean
- `measures` *(required)*: measures
- `anchors`: array of id
- `public` *(required)*: object
  - `prompt` *(required)*: text
  - `options` *(required)*: array of object
    - `option_id` *(required)*: id
    - `text` *(required)*: string (min 1 chars)
  - `selection` *(required)*: enum single | multiple
  - `shuffle`: boolean
- `grading` *(required)*: object
  - `correct_option_ids` *(required)*: array of id
  - `option_feedback`: object
- `feedback` *(required)*: feedback

### Interaction `table_select` (data)
- `type` *(required)*: const 'table_select'
- `interaction_id` *(required)*: id
- `difficulty`: enum intro | core | stretch
- `grading_mode`: enum client | server
- `standalone`: boolean
- `measures` *(required)*: measures
- `anchors`: array of id
- `public` *(required)*: object
  - `asset_ref` *(required)*: asset_ref
  - `intro`: string
  - `tasks` *(required)*: array of object
    - `task_id` *(required)*: id
    - `prompt` *(required)*: text
    - `target_kind` *(required)*: enum row | column | cell
- `grading` *(required)*: object
  - `answers` *(required)*: array of object
    - `task_id` *(required)*: id
    - `row`: row_ref
    - `column`: string (min 1 chars)
    - `expect_value`: ['string', 'number', 'boolean', 'null']
  - `task_feedback`: object
- `feedback` *(required)*: feedback

### Interaction `find_issues` (data)
- `type` *(required)*: const 'find_issues'
- `interaction_id` *(required)*: id
- `difficulty`: enum intro | core | stretch
- `grading_mode`: enum client | server
- `standalone`: boolean
- `measures` *(required)*: measures
- `anchors`: array of id
- `public` *(required)*: object
  - `asset_ref` *(required)*: asset_ref
  - `instructions` *(required)*: text
  - `categories` *(required)*: array of object
    - `category_id` *(required)*: id
    - `label` *(required)*: string (min 1 chars)
  - `goal_count` *(required)*: integer
- `grading` *(required)*: object
  - `issues` *(required)*: array of object
    - `issue_id` *(required)*: id
    - `category_id` *(required)*: id
    - `locations` *(required)*: array of cell_ref
    - `explanation` *(required)*: text
  - `decoys`: array of object
    - `location` *(required)*: cell_ref
    - `message` *(required)*: text
  - `wrong_category_message`: string
  - `completion_message`: string
- `feedback` *(required)*: feedback

### Interaction `ordering` (core)
- `type` *(required)*: const 'ordering'
- `interaction_id` *(required)*: id
- `difficulty`: enum intro | core | stretch
- `grading_mode`: enum client | server
- `standalone`: boolean
- `measures` *(required)*: measures
- `anchors`: array of id
- `public` *(required)*: object
  - `prompt` *(required)*: text
  - `items` *(required)*: array of object
    - `item_id` *(required)*: id
    - `text` *(required)*: string (min 1 chars)
  - `follow_up`: object
    - `prompt` *(required)*: text
    - `options` *(required)*: array of object
- `grading` *(required)*: object
  - `correct_order` *(required)*: array of id
  - `accepted_alternatives`: array of array
  - `loop_back_note`: string
  - `follow_up_correct_option_ids`: array of id
- `feedback` *(required)*: feedback

### Interaction `classify` (core)
- `type` *(required)*: const 'classify'
- `interaction_id` *(required)*: id
- `difficulty`: enum intro | core | stretch
- `grading_mode`: enum client | server
- `standalone`: boolean
- `measures` *(required)*: measures
- `anchors`: array of id
- `public` *(required)*: object
  - `prompt` *(required)*: text
  - `buckets` *(required)*: array of object
    - `bucket_id` *(required)*: id
    - `label` *(required)*: string (min 1 chars)
  - `items` *(required)*: array of object
    - `item_id` *(required)*: id
    - `text` *(required)*: string (min 1 chars)
    - `source`: object
- `grading` *(required)*: object
  - `assignments` *(required)*: object
  - `role_map`: object
  - `item_feedback`: object
- `feedback` *(required)*: feedback

### Interaction `match_pairs` (core)
- `type` *(required)*: const 'match_pairs'
- `interaction_id` *(required)*: id
- `difficulty`: enum intro | core | stretch
- `grading_mode`: enum client | server
- `standalone`: boolean
- `measures` *(required)*: measures
- `anchors`: array of id
- `public` *(required)*: object
  - `prompt` *(required)*: text
  - `left` *(required)*: array of object
    - `id` *(required)*: id
    - `text` *(required)*: string (min 1 chars)
  - `right` *(required)*: array of object
    - `id` *(required)*: id
    - `text` *(required)*: string (min 1 chars)
- `grading` *(required)*: object
  - `pairs` *(required)*: array of object
    - `left` *(required)*: id
    - `right` *(required)*: id
- `feedback` *(required)*: feedback

### Interaction `field_selection` (core)
- `type` *(required)*: const 'field_selection'
- `interaction_id` *(required)*: id
- `difficulty`: enum intro | core | stretch
- `grading_mode`: enum client | server
- `standalone`: boolean
- `measures` *(required)*: measures
- `anchors`: array of id
- `public` *(required)*: object
  - `prompt` *(required)*: text
  - `scenario`: string
  - `fields` *(required)*: array of object
    - `field_id` *(required)*: id
    - `label` *(required)*: string (min 1 chars)
    - `description`: string
- `grading` *(required)*: object
  - `rules` *(required)*: array of object
    - `field_id` *(required)*: id
    - `role` *(required)*: enum required | acceptable | unneeded | forbidden
    - `rationale` *(required)*: text
  - `outcome_messages`: object
    - `missing_required`: string
    - `includes_forbidden`: string
    - `includes_unneeded`: string
    - `ok`: string
- `feedback` *(required)*: feedback

### Interaction `formula_entry` (data)
- `type` *(required)*: const 'formula_entry'
- `interaction_id` *(required)*: id
- `difficulty`: enum intro | core | stretch
- `grading_mode`: enum client | server
- `standalone`: boolean
- `measures` *(required)*: measures
- `anchors`: array of id
- `public` *(required)*: object
  - `prompt` *(required)*: text
  - `asset_ref` *(required)*: asset_ref
  - `sheet_name`: string
  - `target_cell` *(required)*: string
  - `allowed_functions`: array of string
- `grading` *(required)*: object
  - `expected_value` *(required)*: ['string', 'number', 'boolean', 'null']
  - `must_use_functions`: array of string
  - `forbid_hardcoded_values`: boolean
  - `reference_formula`: string
  - `tolerance`: number
- `feedback` *(required)*: feedback

### Interaction `code_exercise` (core)
- `type` *(required)*: const 'code_exercise'
- `interaction_id` *(required)*: id
- `difficulty`: enum intro | core | stretch
- `grading_mode`: enum client | server
- `standalone`: boolean
- `measures` *(required)*: measures
- `anchors`: array of id
- `public` *(required)*: object
  - `prompt` *(required)*: text
  - `runtime` *(required)*: object
    - `kind` *(required)*: enum python | sql | javascript | react_sandbox | spreadsheet | chart_renderer | bash
    - `version` *(required)*: string (min 1 chars)
    - `packages`: array of string
  - `workspace` *(required)*: object
    - `files` *(required)*: array of object
    - `entry`: string
    - `asset_mounts`: array of object
  - `constraints`: object
    - `allowed_syntax`: array of string
    - `blocked_syntax`: array of string
  - `walkthrough`: array of object
    - `step` *(required)*: string (min 1 chars)
    - `focus_lines`: array of integer
    - `instruction` *(required)*: text
    - `action` *(required)*: enum read | edit | run | predict
- `grading` *(required)*: object
  - `tests` *(required)*: array of object
    - `test_id` *(required)*: id
    - `kind` *(required)*: enum stdout_equals | value_equals | dataframe_equals | query_result_equals | function_call | figure_equals | axes_property | plotted_data_equals | forbidden_syntax | cell_equals | range_equals | formula_uses
    - `spec` *(required)*: object
    - `visible`: boolean
    - `message_on_fail` *(required)*: text
  - `solution_files` *(required)*: array of object
    - `path` *(required)*: string (min 1 chars)
    - `content` *(required)*: string
  - `execution_provenance`: object
    - `runtime`: string (min 1 chars)
    - `runtime_version`: string (min 1 chars)
    - `solution_sha256`: sha256
    - `tests_passed`: integer
  - `hidden_checks`: array of object
    - `check_id` *(required)*: id
    - `mutation` *(required)*: object
    - `expected` *(required)*: object
    - `ordered`: boolean
    - `statement`: integer
    - `test_id`: id
- `feedback` *(required)*: feedback

### Interaction `short_answer` (core)
- `type` *(required)*: const 'short_answer'
- `interaction_id` *(required)*: id
- `difficulty`: enum intro | core | stretch
- `grading_mode`: enum client | server
- `standalone`: boolean
- `measures` *(required)*: measures
- `anchors`: array of id
- `public` *(required)*: object
  - `prompt` *(required)*: text
  - `input_kind` *(required)*: enum text | number
- `grading` *(required)*: object
  - `accepted_answers`: array of string
  - `numeric`: object
    - `value` *(required)*: number
    - `tolerance`: number
  - `case_sensitive`: boolean
- `feedback` *(required)*: feedback

### Interaction `external_proof` (core)
- `type` *(required)*: const 'external_proof'
- `interaction_id` *(required)*: id
- `difficulty`: enum intro | core | stretch
- `grading_mode`: enum client | server
- `standalone`: boolean
- `measures` *(required)*: measures
- `anchors`: array of id
- `public` *(required)*: object
  - `instruction` *(required)*: text
  - `evidence_kinds` *(required)*: array of ?
  - `checklist`: array of string
- `grading` *(required)*: object
  - `mode` *(required)*: enum self_attest | rubric_ai | manual
  - `rubric`: array of object
    - `criterion` *(required)*: string (min 1 chars)
    - `weight`: number
- `feedback` *(required)*: feedback

### Interaction `diagram_label` (core)
- `type` *(required)*: const 'diagram_label'
- `interaction_id` *(required)*: id
- `difficulty`: enum intro | core | stretch
- `grading_mode`: enum client | server
- `standalone`: boolean
- `measures` *(required)*: measures
- `anchors`: array of id
- `public` *(required)*: object
  - `prompt` *(required)*: text
  - `diagram` *(required)*: block.diagram.schema.json
  - `labels` *(required)*: array of object
    - `label_id` *(required)*: id
    - `text` *(required)*: string (min 1 chars)
- `grading` *(required)*: object
  - `placements` *(required)*: object
- `feedback` *(required)*: feedback
