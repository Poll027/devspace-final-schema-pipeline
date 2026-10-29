# Stage 01 – Scenario & Asset Registry – Evaluator Report

**Batch:** `final_batch_006_da_sql_rest`  
**Artifact:** `scenario_asset_registry.json`  
**Evaluator scope:** Full registry (1 scenario, 4 assets, 2 messy variants)

---

## Methodology

Checked all 4 assets (ds_orders, ds_customers, ds_order_items, ds_shipments) and both messy variants against the glossary bundle. Verified approximately half (12 of 22) of the concepts' teaching-block examples against the registry data, covering: sql.where_filtering, sql.logical_operators, sql.null_handling, sql.case_expressions, sql.group_by, sql.having, sql.union, sql.inner_join, sql.outer_joins, sql.composite_join_conditions, sql.coalesce, sql.subquery_in_where. Also verified semantic roles, data types, glossary_example_vocab completeness, and planted-issue validity.

---

## Findings

### 1. Data supports glossary examples (PASS)

- **WHERE / logical operators / NULL handling:** `delivery_time_minutes` has a good range (15–63) plus two NULLs (orders 1011, 1012). Threshold examples (> 30, > 40, > 60) all produce non-trivial result sets.
- **CASE expressions:** The `< 20 / < 40 / ELSE` thresholds produce all three labels ('fast', 'normal', 'slow') across the 12 rows. The simple CASE mapping city→region is perfectly consistent with the actual data.
- **GROUP BY / HAVING:** Three customer groups with distinct averages (37.5, 37.33, 29.33) allow the `HAVING AVG(...) > 30` filter to keep two and drop one.
- **Aggregate functions:** `amount` column provides meaningful SUM/AVG exercises; NULLs in `delivery_time_minutes` demonstrate COUNT(*) vs COUNT(column).
- **INNER JOIN / OUTER JOIN:** Customers 4, 5, 6 have no orders, making LEFT JOIN demonstrations meaningful. All order customer_ids (1, 2, 3) exist in customers.
- **Composite join:** order_items (10 rows) and shipments (6 rows) share (order_id, product_id); 4 order_items rows have no matching shipment, demonstrating inner-vs-outer join differences.
- **Subqueries / CTEs:** AVG(delivery_time_minutes) = 35.0 across all orders; the `> (SELECT AVG(...))` subquery and the `customer_avg` CTE examples both produce correct, non-trivial results.
- **COALESCE:** Customers 4 and 5 have NULL city; customer 5 has NULL name — both support COALESCE fallback examples.
- **String functions:** City values ('Lagos', 'Kano', 'Abuja') and name values support LOWER/UPPER/TRIM/CONCAT/LENGTH examples.
- **Date functions:** `order_date` column supports EXTRACT and date subtraction examples.
- **UNION:** Both queries (`city = 'Lagos'` from customers, `delivery_time_minutes > 60` from orders) return valid results.

### 2. Glossary_example_vocab completeness (PASS)

All table names, column names, key categorical values, threshold values, and SQL keywords referenced in the teaching blocks are present in the vocab list.

### 3. Semantic roles (PASS, one advisory)

All semantic roles are correctly assigned. `numeric_looking_label` is consistently applied to FK integer identifiers but missing on `ds_orders.order_id` (the PK), which is inconsistent with the FK treatment.

### 4. Planted issues (PASS)

- **ds_orders_messy:** Three ops (negative delivery time, casing inconsistency, duplicate row) each produce a genuine instance of their declared issue kind.
- **ds_customers_messy:** The casing op ('kano' vs 'Kano') is a genuine inconsistent_category. The `iss_missing_city` issue is pre-existing (customer 4's NULL city exists in clean data too), but the variant description explicitly calls it "pre-existing" and it is a real instance of missing_value.

### 5. UNION teaching text vs data (ADVISORY)

The glossary's `sql.union` tb2 describes "a Lagos customer who also placed **two** orders over 60 minutes" appearing "three times under UNION ALL." The actual data has only **one** order with `delivery_time_minutes > 60` (order 1006, 63 min), so UNION ALL would yield 2 rows, not 3. This is a glossary text issue, not a registry deficiency — the registry data supports all UNION anchors and the actual queries in tb1/tb3.

---

## Defect List

| Severity | Location | Description | Fix |
|----------|----------|-------------|-----|
| ADVISORY | ds_orders/order_id | `numeric_looking_label` flag missing on the PK while present on all FK copies of order_id | Add `"numeric_looking_label": true` to ds_orders.order_id |
| ADVISORY | glossary sql.union tb2 vs registry | tb2 hypothetical ("two orders over 60 minutes" / "three times under UNION ALL") cannot be reproduced with the registry data (only one order exceeds 60 min) | Either add a second order with delivery_time > 60 to ds_orders, or note this is a glossary-side fix (change "two" to "one" and "three" to "two") |

---

## VERDICT: PASS
