# Evaluation Report: Stage 04 Interactions — Chunk c3

## Scope
Tiles evaluated: `tile_sql_adv_joining_tables`, `tile_sql_adv_execution_order_subquery_where`, `tile_sql_adv_subquery_from_cte`

Total interactions reviewed: 16 (all interactions in the chunk)

## Methodology
1. Read all glossary bundle facts, teaching blocks, assessment anchors, and practice anchors for all 7 concepts covered.
2. Read all three tile lesson files to verify what was taught.
3. Solved every choice question blind from the lesson text, then compared with the key.
4. Manually computed expected results for all 7 code exercises against the scenario registry data.
5. Checked each code exercise for: alternative correct queries that could be marked wrong, starter completeness, practice anchor alignment, prompt pinning of columns/order/approach.

## Tile: tile_sql_adv_joining_tables

### s04 (choice — INNER JOIN row survival)
- Correct answer opt_b (3 customers) is unambiguous and well-supported by glossary fact sql.inner_join#f1.
- All distractor feedback is factually accurate.
- No issues.

### s05 (code — INNER JOIN on customer_id)
- Expected result verified against registry data (13 rows, ordered by order_id). ✓
- Prompt pins columns (name, order_id, delivery_time_minutes), order (order_id ASC), and approach (JOIN with ON). ✓
- Starter is genuinely incomplete (no query body). ✓
- Practice anchor success: "The query returns one row for each order that has a matching customer, showing columns from both tables." Satisfied. ✓
- USING (customer_id) would also pass the test, but the prompt explicitly says "with an ON clause." Acceptable.

### s07 (choice — composite ON with AND)
- Correct answer opt_b is unambiguous. All feedback accurate per sql.composite_join_conditions#f1.
- No issues.

### s08 (choice — USING shorthand)
- Correct answer opt_a (USING (order_id, product_id)) is unambiguous per sql.composite_join_conditions#f2.
- All distractor feedback is accurate.
- No issues.

### s09 (code — composite join ON with AND)
- Expected result verified (6 rows). ✓
- Prompt pins columns, order, and approach (ON clause with AND). ✓
- Starter genuinely incomplete. ✓
- Practice anchor success: "Rows that match on only one of the two columns are excluded from the result." Satisfied. ✓

### s13 (choice — LEFT JOIN vs others)
- Correct answer opt_b (LEFT JOIN) is unambiguous per sql.outer_joins#f1, f2, f3.
- All feedback accurate. FULL JOIN correctly rejected because it would add unmatched order rows.
- No issues.

### s14 (choice — OUTER is optional)
- Correct answer opt_a is unambiguous per sql.outer_joins#f4.
- All feedback accurate.
- No issues.

### s15 (code — LEFT JOIN)
- Expected result verified (16 rows including 3 unmatched customers). ✓
- Prompt pins columns, order, and approach (LEFT JOIN). ✓
- Starter genuinely incomplete. ✓
- Practice anchor success: "The query returns every customer at least once, with order columns NULL for customers without orders." Satisfied. ✓

## Tile: tile_sql_adv_execution_order_subquery_where

### s04 (choice — clause processing order)
- Correct answer opt_b (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY) matches glossary fact sql.clause_execution_order#f1 exactly.
- All feedback accurate.
- No issues.

### s05 (code — fix alias in WHERE)
- Expected result verified (7 rows with tax > 500). ✓
- Prompt pins columns, order, and approach (write expression in WHERE). ✓
- Starter is genuinely incomplete (missing WHERE clause). ✓
- Practice anchor success: "The learner repairs the query ... and names that WHERE runs before the SELECT output is computed." Satisfied. ✓

### s08 (choice — scalar subquery in WHERE)
- Correct answer opt_b is unambiguous per sql.subquery_in_where#f2.
- Feedback for opt_a correctly notes AVG() can't be used directly in WHERE.
- All feedback accurate.
- No issues.

### s09 (code — IN subquery + scalar subquery)
- Expected results verified for both queries. ✓
- Prompt pins columns, order, and approach for both queries. ✓
- Starter genuinely incomplete (missing WHERE clauses). ✓
- Practice anchor success: "The query returns exactly the rows that satisfy the comparison against the subquery's single value." Satisfied. ✓

## Tile: tile_sql_adv_subquery_from_cte

### s04 (choice — inner column names visible to outer query)
- Correct answer opt_a is unambiguous per sql.subquery_in_from#f2.
- All feedback accurate.
- No issues.

### s05 (code — FROM subquery)
- Expected result verified (2 rows: customer 1 with 6 orders, customer 2 with 4). ✓
- Prompt pins columns, order, alias name, and approach (FROM subquery). ✓
- Starter genuinely incomplete. ✓
- Practice anchor success: "The query runs, the subquery is wrapped in parentheses with an alias, and the outer query filters on a column the inner query produced." Satisfied. ✓

### s08 (choice — CTE rewrite)
- Correct answer opt_a is unambiguous per sql.cte#f1, f2, f3.
- All distractor feedback is accurate (WITH placement, parentheses requirement).
- No issues.

### s09 (code — CTE with WITH clause)
- Expected result verified (same 2 rows as FROM subquery version). ✓
- Prompt pins columns, order, CTE name, and approach (WITH clause). ✓
- Starter genuinely incomplete. ✓
- Practice anchor success: "The query defines the totals in a WITH block, reads it by name in the main query, and returns only the customers that meet the filter." Satisfied. ✓

## Defects Found

None blocking. No advisory issues of note.

## Verdict

VERDICT: PASS
