# Pedagogy Review — tile_data_shape_and_types

**Reviewer:** Independent evaluator (stage 08)
**Tile:** tile_data_shape_and_types — "Datasets and Variable Types"
**Concepts:** data.dataset_rows_columns, data.categorical_numeric_types

---

## 1. Structure & Pacing

| Metric | Value | Target | Status |
|---|---|---|---|
| Main steps | 8 (s01–s08) | 8–14 | ✅ |
| Remediation steps | 2 (r01, r02) | — | ✅ |
| Estimated minutes | 8.6 | 6–12 | ✅ |

## 2. Explain → Check → Apply Flow

**Concept 1 — data.dataset_rows_columns:**
- s01 (explainer): introduces dataset, table/data matrix — facts f1, f2
- s02 (explainer): rows = observations, columns = variables — facts f3, f4
- s03 (check): choice question testing column = variable — fact f4
- s04 (hands_on): table_select identifying a row and two columns — facts f1–f4

✅ Explain precedes check; check precedes apply. No check arrives before its idea.

**Concept 2 — data.categorical_numeric_types:**
- s05 (explainer): categorical vs numerical definitions + misconception (numeric-looking categorical) — facts f1, f2, m1
- s06 (check): choice question on driver column type — facts f1, f2
- s07 (hands_on): classify all columns including zone_code trap — fact m1
- s08 (recap): both concepts summarised

✅ Explain precedes check; check precedes apply. No check arrives before its idea.

## 3. One Idea per Step

- s01: "dataset" + "table/data matrix" — two closely related sub-facts (f1, f2) from the same concept, taught together in the glossary (tb1 + tb2). Acceptable as one idea.
- s02: "row = observation" + "column = variable" — two halves of one structural idea, taught together in glossary tb3. Acceptable.
- s05: categorical definition + numerical definition + misconception about numeric-looking categoricals — three sub-ideas. However, the misconception is a natural extension of the definitions (you can't define the arithmetic test without immediately addressing the trap case), and the glossary bundles tb1/tb2/tb3 in sequence. The step has 4 blocks but each is focused. Acceptable, though on the heavier side.

✅ No step hides a second idea that the learner must grasp independently.

## 4. Reading Load per Step

- s01: ~100 words prose + 1 data table with highlights — light
- s02: ~150 words across 2 prose blocks — light
- s03: ~30 words prompt + 4 short options — light
- s04: ~20 words intro + 3 task prompts — light
- s05: ~200 words across 3 prose blocks + 1 tagged data table — moderate
- s06: ~30 words prompt + 4 options — light
- s07: ~20 words prompt + 4 drag items — light
- s08: ~100 words across 2 takeaway blocks + 1 up_next — light

✅ No step is overloaded.

## 5. Difficulty Ramp

s03 (intro) → s04 (core) → s06 (core) → s07 (stretch)

✅ Monotonically non-decreasing within each concept's assessment sequence.

## 6. Remediation Quality

- **r01** (for s03, s04): Re-explains row vs column with a concrete side-by-side example (order #1042 as a row, city as a column) plus a highlighted data table. Directly addresses the specific confusion between rows and columns. ✅
- **r02** (for s06, s07): Re-explains the arithmetic test with three concrete examples (delivery_min = numerical, city = categorical, zone_code = categorical despite digits). Directly addresses the specific mistake of misclassifying variable types. ✅

## 7. Visual Audit

- **s01 data_table**: Highlights one row (order 1042) and one column (city) — directly supports the text introducing rows and columns. Earns its place. ✅
- **s05 data_table**: Tags each column as identifier/categorical/numerical, with zone_code visibly tagged categorical — directly supports the misconception text. Earns its place. ✅
- **r01 data_table**: Highlights row 1042 and city column for remediation — directly supports the remediation text. Earns its place. ✅

## 8. Data Consistency with Registry

All specific data values mentioned in prose, interactions, and feedback match the scenario asset registry (ds_courier_orders_base):
- Order #1042: Lagos, 32 min, Emeka Obi, zone 101 ✅
- Order #1043: Abuja, 41 min, Fatima Bello, zone 102 ✅
- Zone codes 101, 102, 103 ✅
- Cities: Lagos, Abuja, Kano ✅
- Arithmetic: 41 − 32 = 9 minutes ✅

## 9. Wrong-Option Feedback Accuracy

**s03 (choice — column = variable):**
- opt_a ("One delivery"): feedback correctly says "That describes a row, not a column." ✅
- opt_c ("Entire dataset"): feedback correctly says "The dataset is the whole table, not a single column." ✅
- opt_d ("Summary statistic"): feedback correctly says "Columns hold raw values, not computed summaries." ✅

**s06 (choice — driver is categorical):**
- opt_a ("Numerical — ranked by performance"): feedback correctly says ranking ≠ numerical; the test is arithmetic. ✅
- opt_c ("Numerical — unique identifier"): feedback correctly says uniqueness ≠ numerical. ✅
- opt_d ("Numerical — alphabetical sort"): feedback correctly says sorting ≠ numerical. ✅

All wrong-option feedback is factually accurate and addresses the specific misconception behind each wrong answer.

## 10. Knowledge Boundary Check

No step requires understanding of concepts beyond data.dataset_rows_columns and data.categorical_numeric_types. The up_next block in s08 mentions "data quality" as a forward pointer only — no understanding required.

The s05 data_table tags order_id as "identifier" — this term is not formally defined in the glossary for this tile. However, it appears only as a visual annotation (tone: "neutral") and is never tested. The learner is not required to understand or recall this label.

---

## Findings

| Severity | Location | Issue | Fix |
|---|---|---|---|
| ADVISORY | s05 | The step teaches three sub-ideas (numerical definition, categorical definition, numeric-looking-categorical misconception) across 3 prose blocks + 1 data table. This is the heaviest step in the tile. | Consider splitting the misconception (tb3/m1) into its own short explainer step between s05 and s06, to keep each step to one core idea. |
| ADVISORY | s05/b04 | The data_table tags order_id as "identifier" — a term not formally defined in this tile's glossary entries. The tag is visual-only and never tested, but a learner might wonder what "identifier" means. | Add a one-sentence note in the caption or a brief inline aside explaining that order_id is just a label used to tell rows apart, not a variable type they need to learn here. |

---

## Verdict

No BLOCKING defects found. The explain → check → apply flow is sound for both concepts. Checks never precede their ideas. Remediation directly addresses the specific mistakes. All data matches the registry. Wrong-option feedback is accurate. Reading load and step count are within bounds.

**VERDICT: PASS**
