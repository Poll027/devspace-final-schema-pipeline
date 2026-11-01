# Stage 01 — Scenario Asset Registry Evaluation

**Batch:** `final_batch_007_da_nocode`  
**Artifact:** `scenario_asset_registry.json`

## Scope of review

Checked all 2 scenarios, all 3 assets (`ds_delivery_orders` with its messy variant, `ds_stakeholder_requests`, `ds_finding_statements`). Cross-referenced glossary teaching blocks for all 7 concepts in the bundle against the registry data. Verified planted issues, column semantic roles, numeric consistency of example rows, and glossary_example_vocab coverage.

## Findings

### BLOCKING

1. **ds_finding_statements / row 4 (finding_id=4):** The precise finding states "Driver 201 completed all 3 assigned orders in March 2024 with an average delivery time of 29 minutes, the lowest among the five active drivers." Two factual errors when checked against `ds_delivery_orders`:
   - Driver 201's actual average is 29.67 minutes (times: 28, 32, 29), not 29.
   - Driver 201 is **not** the lowest — Driver 202 (avg 21.0) and Driver 205 (avg 22.0) are both substantially lower. Driver 201 ranks 4th out of 5.
   
   This is a data contradiction within the registry: `ds_finding_statements` is described as "drawn from the Kwik Courier scenario" and other rows (1, 3, 5) are numerically consistent with `ds_delivery_orders`. A learner using both assets would encounter a false claim presented as a model "precise" finding.

### ADVISORY

1. **ds_finding_statements / row 2 (finding_id=2):** The precise finding references "1,240 orders" and "18% increase" — numbers not derivable from the 12-row dataset. Not strictly contradictory (the dataset covers one week; the finding could reference the full month from a different source), but unlike rows 1, 3, and 5 which are verifiable against `ds_delivery_orders`, this row introduces unanchored numbers.

2. **ds_stakeholder_requests / row 2 (request_id=2) intent:** Labeled "description" for "Is the average delivery time per driver in March 2024 above the 30-minute target?" Comparing to a fixed target could be read as "comparison." However, the glossary defines comparison as "comparing a variable across two or more groups," and a fixed target is not a group, so "description" is the more defensible reading. Borderline but acceptable.

3. **ds_stakeholder_requests / row 1 measurable_question:** Minor wording difference from glossary — registry has "Is the average delivery time in Lagos this month higher than last month?" while glossary has "Is average delivery time in Lagos this month higher than last month?" (added "the"). Trivial; no semantic change.

## Verified correct

- `ds_delivery_orders` clean base: 12 rows, 7 columns, all column types and semantic roles correct. Lagos avg = 30.0 min matches glossary teaching example exactly.
- Messy variant: three planted issues (missing value on order 1009, duplicate of order 1003, -5 on order 1006) all match glossary examples for completeness, uniqueness, and validity.
- `ds_finding_statements` rows 1, 3, 5: numerically consistent with `ds_delivery_orders`.
- `ds_stakeholder_requests` row 1: decision, vague question, measurable question, variable, group, and intent all align with glossary teaching blocks.
- `glossary_example_vocab` for both scenarios covers all key terms from the glossary teaching blocks.
- `numeric_looking_label` flags correctly applied to `order_id`, `driver_id`, `request_id`, `finding_id`.
- PII columns (`customer_name`, `customer_phone`) correctly tagged with `semantic_role: "pii"`.

---

VERDICT: FAIL

BLOCKING ds_finding_statements/row 4: Precise finding claims Driver 201 has average delivery time of 29 minutes and is the lowest among five drivers, but ds_delivery_orders shows Driver 201 avg = 29.67 min and ranked 4th of 5 (Driver 202 avg = 21.0 is actually lowest) → Fix precise_finding to: "Driver 202 completed both assigned orders in March 2024 with an average delivery time of 21 minutes, the lowest among the five active drivers." and update vague_finding to: "Driver 202 is our best driver."
ADVISORY ds_finding_statements/row 2: Precise finding references 1,240 orders and 18% increase not derivable from the 12-row dataset → Consider aligning numbers with ds_delivery_orders or adding a note that this finding references full-month data beyond the sample
ADVISORY ds_stakeholder_requests/row 2 intent: "description" for a question comparing to a target is borderline; defensible but could confuse learners expecting "comparison" → No change required but consider adding a teaching note
ADVISORY ds_stakeholder_requests/row 1 measurable_question: Minor wording difference from glossary example (added "the") → No change required
