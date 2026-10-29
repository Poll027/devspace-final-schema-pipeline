# Evaluation Report — Stage 03 screens, chunk c2

**Batch:** `final_batch_006_da_sql_rest`  
**Tiles evaluated:** `tile_sql_style_conventions`, `tile_sql_text_dates_casts`, `tile_sql_null_fallback_and_union`  
**Artifact:** `screens.part.c2.json`

---

## Tile-by-tile review

### tile_sql_style_conventions

**s01 (explainer):** Prose blocks correctly teach all five facts (f1–f5). The before/after code walkthrough demonstrates the river layout well.

- **BLOCKING — change_summary (line 105):** The change_summary states "alias added with AS" but the after code (`SELECT customer_id, city FROM customers WHERE city = 'Lagos' AND customer_id > 1`) contains no alias. The before code also has no alias. The claim is false for the code shown.
- **ADVISORY — before annotation (line 71):** Annotation says "column names mixed-case" but the before code uses all-lowercase column names (`customer_id`, `city`). Should say "Keywords lowercase" only, or note that the *bad* example in the prose block (not this code) has mixed-case.

**s02 (check):** Correctly targets f4/f5 (line breaks and river). Fine.

**s03 (hands_on):** Covers all five facts and all three assessment anchors. Fine.

**s04 (recap):** Accurately summarises all five rules. Up_next teaser is appropriate.

**Remediation steps (r01–r03):** Accurate restatements of the relevant facts. No issues.

---

### tile_sql_text_dates_casts

**s01 (explainer — string functions):**

- **BLOCKING — before_after caption & change_summary (lines 462, 487):** The before caption says "inconsistent casing and stray spaces" and the change_summary says "removes stray spaces," but the `ds_customers_messy` variant (registry) only applies one op: setting customer 2's city to `'kano'` (casing change). No stray spaces are planted anywhere in the variant. The example contradicts the registry data.
- **ADVISORY — s01.p2 (line 430):** Block claims lineage to `sql.string_functions#f3` (CONCAT ignores NULL arguments) but the block text omits the NULL-ignoring behaviour. The fact is covered later in the recap (s10), so it is taught in the tile, but the lineage attribution for this block is inaccurate.

**s04 (explainer — date functions):** Correctly teaches EXTRACT and date subtraction (f1, f2). Code walkthrough annotations are accurate.

**s05 (check — date subtraction):** Correctly targets f2. Fine.

**s06 (hands_on — date functions):** Appropriately scoped. Fine.

**s07 (explainer — type casting):** Correctly teaches both syntaxes (f1) and the conversion-defined rule (f2). Side-by-side code is accurate.

- **ADVISORY — s07.p1 (line 738):** Says "integer column" where the glossary teaching block says "numeric column." Both are defensible since the registry types `delivery_time_minutes` as integer, but it's a minor deviation from glossary wording.

**s08 (check — cast success):** Correctly targets f2. Fine.

**s09 (hands_on — cast syntaxes):** Correctly targets f1. Fine.

**s10 (recap):** Accurately summarises all facts across all three concepts. Mentions CONCAT ignoring NULLs (covering f3's NULL aspect). Up_next teaser is appropriate.

**Remediation steps (r01–r06):** All accurate restatements. r03 date subtraction example (33 days from 2024-01-01 to 2024-02-03) is arithmetically correct.

---

### tile_sql_null_fallback_and_union

**s01 (explainer — COALESCE):** Correctly teaches f1 and f2. Before/after data table uses `ds_customers` (which has NULL cities for customers 4 and 5). Fine.

**s02 (check):** Targets f1 (predict COALESCE result). Fine.

**s03 (check):** Targets f2 (substitute default for NULL). Fine.

**s04 (hands_on — COALESCE):** Appropriately scoped. Fine.

**s05 (explainer — UNION):** Correctly teaches f1 (append rows, no order guarantee) and f2 (UNION deduplicates, UNION ALL keeps all). Diagram accurately illustrates the difference. The "three times under UNION ALL" example faithfully reproduces the glossary teaching block tb2 wording.

**s06 (explainer — UNION compatibility):** Correctly teaches f3. Fine.

**s07 (check — UNION compatibility):** Targets f3. Fine.

**s08 (hands_on — UNION):** Targets f1 and f2 with both practice and assessment anchors. Fine.

**s09 (recap):** Accurately summarises all COALESCE and UNION facts. Up_next teaser appropriately previews JOIN.

**Remediation steps (r01–r04):** All accurate. r03 correctly states the compatibility rule; r04 correctly distinguishes UNION from UNION ALL.

---

## Defect summary

| # | Severity | Location | Description |
|---|----------|----------|-------------|
| 1 | BLOCKING | tile_sql_style_conventions/s01 change_summary | Claims "alias added with AS" but the after code contains no alias |
| 2 | BLOCKING | tile_sql_text_dates_casts/s01 before_after | Caption and change_summary claim "stray spaces" but ds_customers_messy has no stray spaces — contradicts registry |
| 3 | ADVISORY | tile_sql_style_conventions/s01 before annotation | Says "column names mixed-case" but before code has all-lowercase column names |
| 4 | ADVISORY | tile_sql_text_dates_casts/s01.p2 | Block claims lineage to f3 (CONCAT ignores NULL) but omits NULL-ignoring in text; fact is covered in recap |
| 5 | ADVISORY | tile_sql_text_dates_casts/s07.p1 | Says "integer column" where glossary says "numeric column" — minor wording deviation |

---

## Verdict

VERDICT: FAIL

BLOCKING tile_sql_style_conventions/s01 change_summary: change_summary claims "alias added with AS" but the after code contains no alias → Remove "alias added with AS," from the change_summary so it reads: "The same query reformatted: keywords uppercased, columns lowercased, each clause on its own right-aligned line, spaces around operators."

BLOCKING tile_sql_text_dates_casts/s01 before_after: Caption says "inconsistent casing and stray spaces" and change_summary says "removes stray spaces," but ds_customers_messy has no stray spaces (only a casing op) — example contradicts registry data → Change before caption to "Raw city values — inconsistent casing", change after caption to "After LOWER(TRIM(city)) — consistent lowercase, casing standardised", and change change_summary to "LOWER(TRIM(city)) standardises city values to consistent lowercase." (TRIM is still valid to teach but the data description must not claim spaces exist when they don't.)

ADVISORY tile_sql_style_conventions/s01 before annotation: Annotation says "column names mixed-case" but the before code has all-lowercase column names → Change annotation to "Keywords lowercase, no line breaks, no spaces around operators, no commas after spaces"

ADVISORY tile_sql_text_dates_casts/s01.p2: Block claims lineage to sql.string_functions#f3 but omits the NULL-ignoring behaviour of CONCAT → Add "and ignores any NULL arguments" after "CONCAT concatenates the text representations of all its arguments"

ADVISORY tile_sql_text_dates_casts/s07.p1: Says "integer column" where glossary teaching block says "numeric column" → Consider aligning with glossary wording "numeric column" for consistency
