# 03_screens Evaluation — chunk c3

**Tiles evaluated:** tile_sql_adv_joining_tables, tile_sql_adv_execution_order_subquery_where, tile_sql_adv_subquery_from_cte

**Steps sampled (≥ ⅓):**
- tile_sql_adv_joining_tables: s01, s03, s06, s10, s11, s16, r01, r02, r03 (9 of 16 + 3 remediation)
- tile_sql_adv_execution_order_subquery_where: s01, s03, s06, s10, r01, r02 (6 of 10 + 2 remediation)
- tile_sql_adv_subquery_from_cte: s01, s02, s06, s10, r01, r02 (6 of 10 + 2 remediation)

---

## Defects

### BLOCKING

1. **tile_sql_adv_joining_tables/s01.b4 (diagram):** Node c3 (customer_id=3, Fatima Aliyu) is marked `kind: "matched"` but has no edge to any order row. The diagram's orders are for cust=1 and cust=2 only. An INNER JOIN diagram must not label a row "matched" when no matching row exists — this contradicts the concept being taught (matched rows are linked; unmatched rows are dropped).
   → Fix: Either change c3's kind to `"unmatched"` (and remove it or mark it dropped like c4), or add an order node with cust=3 and an edge from c3 to it.

2. **tile_sql_adv_joining_tables/s06.b4 (code_walkthrough, USING form):** The SELECT list reads `SELECT oi.order_id, oi.product_id, s.shipped_date` with `USING (order_id, product_id)`. In PostgreSQL (the source for all facts), USING columns are coalesced and cannot be qualified with a table alias; `oi.order_id` would error. → Fix: Change the USING-form SELECT to `SELECT order_id, product_id, s.shipped_date`.

3. **tile_sql_adv_subquery_from_cte/s10.b1 (recap):** States "A subquery in FROM must be wrapped in parentheses and given an alias." Glossary fact sql.subquery_in_from#f1 says the alias "**may** be given" and explicitly notes PostgreSQL allows omission. The recap drops this hedge and presents the alias as mandatory, changing the fact's meaning. → Fix: Replace with "A subquery in FROM must be wrapped in parentheses and should be given an alias (the SQL standard requires it, though PostgreSQL allows omission); the outer query reads its output columns by name."

### ADVISORY

4. **tile_sql_adv_joining_tables/s01.b4 (diagram edge):** The edge from c4 to o1001 labeled "no match — dropped" is visually misleading because it connects an unmatched customer to a specific order belonging to a different customer. Consider removing the edge and instead annotating c4 as a standalone dropped node, or pointing it to a "no match" placeholder node.

5. **tile_sql_adv_subquery_from_cte/s01.b2 (definition):** Opens with "must be enclosed in parentheses and given a table alias" (stronger than fact f1's "may be given"), though the sentence immediately following restores the hedge. The full block is acceptable but the opening could be softened to "and typically given a table alias" for consistency with the fact.

---

## VERDICT: FAIL

BLOCKING tile_sql_adv_joining_tables/s01.b4: Node c3 marked "matched" with no matching edge → change c3 kind to "unmatched" or add an order row for cust=3 with a match edge.
BLOCKING tile_sql_adv_joining_tables/s06.b4: USING-form SELECT qualifies columns with table aliases (oi.order_id, oi.product_id) which is invalid in PostgreSQL → change to `SELECT order_id, product_id, s.shipped_date`.
BLOCKING tile_sql_adv_subquery_from_cte/s10.b1: Recap says alias "must" be given, dropping the hedge from fact f1 which says "may be given" → rewrite as "A subquery in FROM must be wrapped in parentheses and should be given an alias (the SQL standard requires it, though PostgreSQL allows omission); the outer query reads its output columns by name."
ADVISORY tile_sql_adv_joining_tables/s01.b4: Edge from c4 to o1001 labeled "no match — dropped" is visually confusing → use a standalone annotation or placeholder node instead.
ADVISORY tile_sql_adv_subquery_from_cte/s01.b2: Opening sentence says "must be … given a table alias" before qualifying; could soften to "typically given" for consistency with fact f1.
