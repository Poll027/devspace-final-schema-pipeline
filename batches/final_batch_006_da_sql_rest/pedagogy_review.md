# Pedagogy Review — `final_batch_006_da_sql_rest`

**Reviewer:** Independent evaluator (stage 08)  
**Date:** 2026-10-29  
**Tiles reviewed:** All 10

---

## Summary

All 10 tiles were reviewed for explain → check → apply flow, one-idea-per-step, reading load, difficulty ramp, remediation quality, visual utility, step count, and estimated time. The content is generally well-structured and pedagogically sound. Several tiles fall outside the 8–14 step / 6–12 minute guideline, and one tile has a factual miscount in its lede. No blocking defects were found.

---

## Per-tile findings

### 1. tile_sql_fund_filtering_rows (14 steps, ~16 min)

**Flow:** Explain → check → apply for each of three concepts (where_filtering, logical_operators, null_handling). Correct sequencing throughout.  
**One idea per step:** ✓  
**Difficulty ramp:** Intro → core → stretch, well-paced.  
**Remediation:** Each check has a dedicated remediation step that addresses the specific mistake.  
**Visuals:** before_after and side_by_side tables earn their place.  
**Pacing:** 16 minutes is above the 6–12 minute guideline.

- ADVISORY tile_sql_fund_filtering_rows/pacing: Estimated 16 minutes exceeds the 6–12 minute guideline. Consider splitting into two tiles (WHERE + logical operators, NULL handling).
- ADVISORY tile_sql_fund_filtering_rows/s01.ba: The before table has max_rows=10 but the after result includes order 1013 (row 13), which would not be visible in the before table. This could momentarily confuse a learner scanning the before/after pair.

### 2. tile_sql_fund_sorting_limiting (7 steps, ~6.9 min)

**Flow:** Explain ORDER BY → check → apply → explain LIMIT/OFFSET → check → apply → recap. Correct.  
**One idea per step:** ✓  
**Difficulty ramp:** Appropriate.  
**Remediation:** Present and targeted.  
**Visuals:** before_after data tables are useful.  
**Pacing:** 7 steps is below the 8–14 guideline but close; 6.9 min is within range.

- ADVISORY tile_sql_fund_sorting_limiting/step_count: 7 steps is one below the 8-step minimum guideline.

### 3. tile_sql_fund_aggregating_data (14 steps, ~26.1 min)

**Flow:** Explain aggregates → video → check → check → apply → explain GROUP BY → check → check → apply → explain HAVING → check → check → apply → recap. Correct sequencing.  
**One idea per step:** ✓  
**Difficulty ramp:** Good progression across three concepts.  
**Remediation:** Present for each check step.  
**Visuals:** Diagrams and process flows earn their place.  
**Pacing:** 26.1 minutes is far above the 6–12 minute guideline.

- ADVISORY tile_sql_fund_aggregating_data/pacing: Estimated 26.1 minutes is more than double the 12-minute ceiling. This tile covers three concepts (aggregate_functions, group_by, having) and would benefit from being split into two tiles.

### 4. tile_sql_case_expressions (6 steps, ~4.7 min)

**Flow:** Explain CASE WHEN → explain ELSE + simple form → check → check → apply → recap. Correct.  
**One idea per step:** s02 teaches two ideas (ELSE behavior and simple CASE form) in one step.  
**Difficulty ramp:** Appropriate.  
**Remediation:** Present and targeted.  
**Pacing:** 6 steps / 4.7 min are both below guidelines.

- ADVISORY tile_sql_case_expressions/step_count: 6 steps is below the 8-step minimum; 4.7 minutes is below the 6-minute minimum.
- ADVISORY tile_sql_case_expressions/s02: This step teaches two distinct ideas (ELSE/NULL fallback behavior AND the simple CASE form). Consider splitting into two explainer steps.

### 5. tile_sql_style_conventions (4 steps, ~3.9 min)

**Flow:** Explain all 5 conventions → check → apply → recap. Correct but compressed.  
**One idea per step:** s01 teaches all 5 style facts in one step (keyword casing, column casing, alias naming, river alignment, newline rules). This is a lot for one step.  
**Difficulty ramp:** Flat — only one concept.  
**Remediation:** Present and targeted.  
**Pacing:** 4 steps / 3.9 min are well below guidelines.

- ADVISORY tile_sql_style_conventions/step_count: 4 steps is well below the 8-step minimum; 3.9 minutes is below the 6-minute minimum.
- ADVISORY tile_sql_style_conventions/s01: Five distinct style rules are taught in a single explainer step. Consider splitting into at least two steps (casing rules vs. formatting/layout rules).

### 6. tile_sql_text_dates_casts (10 steps, ~9.9 min)

**Flow:** Explain string functions → check → apply → explain date functions → check → apply → explain type casting → check → apply → recap. Correct.  
**One idea per step:** ✓  
**Difficulty ramp:** Good progression.  
**Remediation:** Present and targeted.  
**Visuals:** before_after tables and side_by_side comparisons earn their place.  
**Pacing:** 10 steps / 9.9 min — within guidelines.

- ADVISORY tile_sql_text_dates_casts/s01: The lede says "Four functions that clean, combine, and measure text values" but the step teaches five functions (LOWER, UPPER, TRIM, CONCAT, LENGTH). Should say "Five functions" or restructure the count.

### 7. tile_sql_null_fallback_and_union (9 steps, ~7.8 min)

**Flow:** Explain COALESCE → check → check → apply → explain UNION → explain UNION ALL + compatibility → check → apply → recap. Correct.  
**One idea per step:** ✓  
**Difficulty ramp:** Appropriate.  
**Remediation:** Present and targeted.  
**Visuals:** before_after tables and diagrams earn their place.  
**Pacing:** 9 steps / 7.8 min — within guidelines.

No defects found.

### 8. tile_sql_adv_joining_tables (16 steps, ~22.3 min)

**Flow:** Explain INNER JOIN → video → check → check → apply → explain composite joins → check → check → apply → explain LEFT JOIN → explain RIGHT/FULL → video → check → check → apply → recap. Correct.  
**One idea per step:** ✓  
**Difficulty ramp:** Good progression across three concepts.  
**Remediation:** Present and targeted.  
**Visuals:** ERD diagrams and code walkthroughs earn their place.  
**Pacing:** 16 steps / 22.3 min are both above guidelines.

- ADVISORY tile_sql_adv_joining_tables/pacing: 16 steps and 22.3 minutes both exceed guidelines. This tile covers three concepts (inner_join, composite_join_conditions, outer_joins) and would benefit from being split.

### 9. tile_sql_adv_execution_order_subquery_where (10 steps, ~21.4 min)

**Flow:** Explain execution order → video → explain alias rules → check → apply → explain subquery in WHERE → check → apply → recap. Correct.  
**One idea per step:** ✓  
**Difficulty ramp:** Appropriate.  
**Remediation:** Present and targeted.  
**Visuals:** Process flow diagram earns its place.  
**Pacing:** 10 steps within range; 21.4 minutes is above the 12-minute ceiling.

- ADVISORY tile_sql_adv_execution_order_subquery_where/pacing: 21.4 minutes exceeds the 12-minute guideline.

### 10. tile_sql_adv_subquery_from_cte (10 steps, ~17.7 min)

**Flow:** Explain subquery in FROM → explain column visibility → video → check → apply → explain CTE → check → apply → recap. Correct.  
**One idea per step:** ✓  
**Difficulty ramp:** Appropriate.  
**Remediation:** Present and targeted.  
**Visuals:** Code walkthroughs earn their place.  
**Pacing:** 10 steps within range; 17.7 minutes is above the 12-minute ceiling.

- ADVISORY tile_sql_adv_subquery_from_cte/pacing: 17.7 minutes exceeds the 12-minute guideline.

---

## Cross-tile observations

1. **Explain → check → apply flow** is consistently followed across all tiles. No check arrives before its idea is taught.
2. **Remediation** steps are present for every check and address the specific wrong-answer pattern.
3. **Visuals** (before_after, side_by_side, diagrams, process_flow) all support the text and are not decorative.
4. **Video steps** add visual demonstrations that complement the text (e.g., Venn diagrams for joins, live SQL execution for aggregates).
5. **Data consistency**: All expected query results verified against the scenario registry data. No contradictions found.
6. **Glossary alignment**: All taught facts match the glossary bundle's required_facts. No unsupported claims found.

---

## Defect list

| Severity | Tile / Step | Problem | Fix |
|----------|-------------|---------|-----|
| ADVISORY | tile_sql_text_dates_casts/s01 | Lede says "Four functions" but step teaches five (LOWER, UPPER, TRIM, CONCAT, LENGTH) | Change lede to "Five functions that clean, combine, and measure text values in a query." |
| ADVISORY | tile_sql_style_conventions/pacing | 4 steps / 3.9 min, well below 8–14 steps / 6–12 min guideline | Consider expanding with additional check or practice steps |
| ADVISORY | tile_sql_case_expressions/pacing | 6 steps / 4.7 min, below 8–14 steps / 6–12 min guideline | Consider splitting s02 and adding a practice step |
| ADVISORY | tile_sql_case_expressions/s02 | Two distinct ideas (ELSE/NULL fallback + simple CASE form) in one step | Split into two explainer steps |
| ADVISORY | tile_sql_fund_sorting_limiting/step_count | 7 steps, one below the 8-step minimum | Consider adding one more check or explainer step |
| ADVISORY | tile_sql_fund_filtering_rows/pacing | 16 min estimated, above 12-min ceiling | Consider splitting into two tiles |
| ADVISORY | tile_sql_fund_aggregating_data/pacing | 26.1 min estimated, far above 12-min ceiling | Consider splitting into two tiles |
| ADVISORY | tile_sql_adv_joining_tables/pacing | 16 steps / 22.3 min, above guidelines | Consider splitting into two tiles |
| ADVISORY | tile_sql_adv_execution_order_subquery_where/pacing | 21.4 min estimated, above 12-min ceiling | Consider splitting into two tiles |
| ADVISORY | tile_sql_adv_subquery_from_cte/pacing | 17.7 min estimated, above 12-min ceiling | Consider splitting into two tiles |
| ADVISORY | tile_sql_fund_filtering_rows/s01.ba | Before table capped at 10 rows but after result includes order 1013 (row 13) not visible in before | Increase max_rows to 13 or add a note |
| ADVISORY | tile_sql_style_conventions/s01 | Five style rules in one explainer step — high reading load | Consider splitting into two steps |

---

## Verdict

No blocking defects found. All tiles follow the explain → check → apply pattern, remediations address specific mistakes, visuals support the text, and all data/facts are accurate. The advisory findings are pacing/length preferences and one minor lede miscount.

**VERDICT: PASS**
