# EVALUATOR PACKET — Integrating SQL, Spreadsheets, and pandas (tile_capstone_integrate_tools_model)
Tile summary: Apply already-learned SQL, spreadsheet, and pandas skills to the QuickRide capstone project: retrieve last quarter's orders with a multi-clause SELECT, summarise the delivery sheet with a PivotTable and COUNTIFS, clean and aggregate orders in pandas, and model the two-table relationship with correct primary and foreign keys.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = capstone.integrate_sql — Integrating SQL querying into an end-to-end project
B = capstone.integrate_spreadsheet — Integrating spreadsheet analysis into an end-to-end project
C = capstone.integrate_python_pandas — Integrating Python/pandas cleaning and analysis into an end-to-end project
D = capstone.building_data_model — Building a data model for the capstone dataset

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: plan: tile_capstone_integrate_tools_model.s11 was planned to measure capstone.integrate_spreadsheet#assessment:build_pivot_table_with_correct_field_placement but its interaction does not

## SOURCE FACTS — A (capstone.integrate_sql)   objective: Combine already-learned SELECT, WHERE, JOIN, and GROUP BY into one SQL query that retrieves the specific rows, columns, and groups the capstone's business question needs.
A.f1: A single SELECT statement's syntax allows a FROM clause, a WHERE clause, and a GROUP BY clause to appear together in the same query.   [sources: postgresql_docs_select#Synopsis]
A.f2: A join, such as an INNER JOIN, can be included in that same SELECT statement's FROM clause to combine matching rows from more than one table before the query's WHERE filtering or GROUP BY grouping is applied.   [sources: postgresql_docs_table_expressions#7.2.1.1. Joined Tables, postgresql_docs_table_expressions#7.2. Table Expressions]
note: This applies already-learned SELECT/WHERE/JOIN/GROUP BY to the capstone's own tables -- don't reintroduce join or grouping mechanics from scratch.
PRACTICE ANCHOR (live_code): Write and run the SQL query that retrieves last quarter's orders from the capstone dataset, joining the orders and drivers tables, filtering to the correct date range, and grouping by zone.  SUCCESS: The query executes without error and returns one row per zone showing the average delivery time for orders placed between 2026-04-01 and 2026-06-30.
ASSESSMENT ANCHOR: write_select_with_from_where_group_by_in_one_statement facts=['f1']
ASSESSMENT ANCHOR: include_inner_join_in_from_clause_before_where_and_group_by facts=['f2']
ASSESSMENT ANCHOR: apply_combined_join_filter_group_query_to_capstone_dataset facts=['f1', 'f2']

## SOURCE FACTS — B (capstone.integrate_spreadsheet)   objective: Apply already-learned spreadsheet formulas and PivotTables to complete the capstone project's spreadsheet-based analysis step.
B.f1: A PivotTable is built by selecting the data range and inserting a PivotTable, then adding fields to it: non-numeric fields default to Rows, date/time fields to Columns, and numeric fields to Values, and fields can be dragged between these areas to rearrange the summary.   [sources: excel_pivottable_guide]
B.f2: COUNTIFS(criteria_range1, criteria1, [criteria_range2, criteria2]…) applies criteria across one or more ranges and counts the cells for which all the criteria are met.   [sources: excel_countifs_function]
note: Assume PivotTables and COUNTIFS were already taught -- this concept applies them to the capstone's own sheet, not a new spreadsheet feature.
PRACTICE ANCHOR (spreadsheet): Given the capstone delivery sheet (columns: zone, shift, delivery_time), insert a PivotTable that places zone and shift in Rows by default, then drag shift to Columns and set Values to average delivery_time to produce a zone-by-shift grid. In a separate cell, write a COUNTIFS formula that counts deliveries in a specified zone where delivery_time exceeds a given threshold.  SUCCESS: The PivotTable shows zones as row labels, shifts as column headers, and average delivery times as cell values. The COUNTIFS formula returns the correct count of rows matching both the zone criterion and the delivery_time threshold, verifiable by manual inspection of a small sample.
ASSESSMENT ANCHOR: build_pivot_table_with_correct_field_placement facts=['f1']
ASSESSMENT ANCHOR: apply_countifs_with_multiple_criteria_ranges facts=['f2']
ASSESSMENT ANCHOR: execute_capstone_spreadsheet_analysis_step facts=['f1', 'f2']

## SOURCE FACTS — C (capstone.integrate_python_pandas)   objective: Apply already-learned pandas cleaning (isna/dropna/fillna) and analysis (groupby aggregation) to the capstone's own retrieved dataset.
C.f1: isna() detects which values in a DataFrame are missing, and dropna() removes rows with missing values or fillna() replaces them with a specified value.   [sources: pandas_docs_missing_data#values-considered-missing, pandas_docs_missing_data#dropping-missing-data, pandas_docs_missing_data#filling-missing-data]
C.f2: A groupby operation splits data into groups based on some criteria, applies a function independently to each group, and combines the results back into a single structure; an aggregation is a groupby operation that reduces each group to one summary value per column.   [sources: pandas_docs_groupby#group-by-split-apply-combine, pandas_docs_groupby#aggregation]
note: Applies already-learned isna()/dropna()/fillna() and groupby to the capstone's own dataset -- don't re-teach missing-data or groupby mechanics from scratch.
PRACTICE ANCHOR (live_code): Given a small orders DataFrame with a 'zone' column and a 'delivery_time' column containing some NaN values, detect the missing delivery times, remove those rows, then compute the mean delivery time per zone.  SUCCESS: The learner produces a Series or DataFrame showing one mean delivery_time value per zone, derived from a DataFrame with missing rows removed, using only isna()/dropna() and groupby().mean().
ASSESSMENT ANCHOR: detect_and_handle_missing_values_with_isna_dropna_fillna facts=['f1']
ASSESSMENT ANCHOR: apply_groupby_aggregation_to_summarize_groups facts=['f2']
ASSESSMENT ANCHOR: clean_and_aggregate_capstone_dataset_end_to_end facts=['f1', 'f2']

## SOURCE FACTS — D (capstone.building_data_model)   objective: Connect the capstone project's own tables using the correct primary keys, foreign keys, and one-to-many relationships.
D.f1: A primary key uniquely identifies each row of a table; a foreign key's values must match values appearing in some row of the table it references.   [sources: postgresql_docs_constraints#5.5.4. Primary Keys, postgresql_docs_constraints#5.5.5. Foreign Keys]
D.f2: In a one-to-many relationship, one row on the 'one' side relates to many rows on the 'many' side (for example, one department has many employees); in the Customer/Order example, the foreign key CustID is placed in the Order table and must match a valid CustID in the Customer table.   [sources: database_design_open_textbook#ch8-Types of Relationships, database_design_open_textbook#ch9-Referential integrity]
note: This applies the already-taught primary-key/foreign-key/one-to-many pattern to the capstone's own two tables -- don't reintroduce normalization or many-to-many, which aren't needed for a two-table model.
PRACTICE ANCHOR (matching): Given a list of column names from the Drivers and Orders tables, match each column to its role: primary key of Drivers, primary key of Orders, or foreign key in Orders referencing Drivers; then identify which table is on the 'one' side and which is on the 'many' side of the relationship.  SUCCESS: The learner correctly labels driver_id as the primary key of Drivers, order_id as the primary key of Orders, driver_id in Orders as the foreign key referencing Drivers, and identifies Drivers as the 'one' side and Orders as the 'many' side.
ASSESSMENT ANCHOR: build_capstone_data_model_with_correct_keys_and_relationships facts=['f1', 'f2']
ASSESSMENT ANCHOR: identify_primary_and_foreign_keys_in_capstone_tables facts=['f1']
ASSESSMENT ANCHOR: identify_one_to_many_relationship_between_drivers_and_orders facts=['f2']

## DATA ASSETS USED
ds_capstone_delivery_sheet: Capstone Delivery Sheet (Spreadsheet Exercise) — columns: zone(categorical), shift(categorical), delivery_time(numerical)
   ["Ikeja","morning",28]
   ["Ikeja","morning",38]
   ["Ikeja","morning",48]
   ["Ikeja","afternoon",35]
   ["Ikeja","afternoon",42]
   ["Ikeja","afternoon",178]
   ["Ikeja","evening",32]
   ["Ikeja","evening",36]
ds_capstone_drivers: Capstone Drivers Table — columns: driver_id(identifier), driver_name(text)
   ["D01","Amara Okafor"]
   ["D02","Chidi Eze"]
   ["D03","Ngozi Adeyemi"]
   ["D04","Emeka Nwosu"]
   ["D05","Fatima Bello"]
   ["D06","Tunde Adesanya"]
   ["D07","Kemi Lawal"]
   ["D08","Seun Adebayo"]
ds_capstone_orders: Capstone Orders Table — columns: order_id(identifier), driver_id(identifier), zone(categorical), order_date(datetime), delivery_time(numerical)
   ["O-001","D01","Ikeja","2026-04-03",28]
   ["O-002","D01","Ikeja","2026-04-10",32]
   ["O-003","D02","Ikeja","2026-04-17",35]
   ["O-004","D02","Ikeja","2026-04-24",36]
   ["O-005","D01","Ikeja","2026-05-02",38]
   ["O-006","D02","Ikeja","2026-05-09",38]
   ["O-007","D01","Ikeja","2026-05-16",42]
   ["O-008","D02","Ikeja","2026-05-23",45]
   variant ds_capstone_orders_messy: 3 ops; planted: issue_impossible_delivery_time(impossible_value); issue_duplicate_order(duplicate_row); issue_zone_casing(inconsistent_category)
ds_pandas_orders: Pandas Practice Orders (Missing Values Exercise) — columns: zone(categorical), delivery_time(numerical)
   ["Ikeja",28]
   ["Ikeja",38]
   ["Ikeja",null]
   ["Ikeja",42]
   ["Lekki",22]
   ["Lekki",null]
   ["Lekki",30]
   ["Lekki",35]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Applying descriptive statistics to capstone findings; Building a data model for the capstone dataset; Building a polished matplotlib/seaborn visualization set for the capstone; Documenting and presenting the finished capstone deliverable; Independent, unassisted execution across multiple tool families; Integrating Python/pandas cleaning and analysis into an end-to-end project; Integrating spreadsheet analysis into an end-to-end project; Producing a stakeholder-facing narrated summary of the capstone

## LESSON, in learner order

### s01 · explainer · One SELECT statement: JOIN, WHERE, and GROUP BY together  [reward 3]
SQL Integration — The first step of the QuickRide capstone is retrieving last quarter's delivery data. All the SQL clauses you already know — JOIN, WHERE, and GROUP BY — can live in a single SELECT statement.
### Combining clauses in one query
(mechanism) A single SELECT statement's syntax allows a FROM clause, a WHERE clause, and a GROUP BY clause to appear together in the same query. In the capstone, that means one statement can filter orders down to last quarter's rows **and** group the result by zone — no separate steps needed. ⟦A.f1 A:tb2⟧
(mechanism) An INNER JOIN can be included in that same FROM clause to combine matching rows from more than one table **before** WHERE filtering or GROUP BY grouping is applied. In the capstone, the `orders` and `drivers` tables are joined in the FROM clause first; the WHERE and GROUP BY then narrow and group the combined rows. ⟦A.f2 A:tb3⟧
[CODE sql]
SELECT o.zone,
       AVG(o.delivery_time) AS avg_delivery_time
FROM   orders o
       INNER JOIN drivers d
           ON o.driver_id = d.driver_id
WHERE  o.order_date >= '2026-04-01'
  AND  o.order_date <  '2026-07-01'
GROUP BY o.zone;
  annotations: ['FROM + INNER JOIN: combines each order row with its matching driver row first.', 'WHERE: narrows the combined rows to last quarter (2026-04-01 to 2026-06-30).', 'GROUP BY: groups the filtered rows by zone so AVG gives one value per zone.']

### s02 · explainer · Clause order: join first, filter next, group last  [reward 2]
SQL Integration — The capstone query uses the same SELECT, FROM, WHERE, JOIN, and GROUP BY you already know — aimed at QuickRide's own tables and date range.
(example) In the capstone query, the INNER JOIN in the FROM clause combines each order row with its matching driver row first. The WHERE clause then narrows those combined rows to orders placed between 2026-04-01 and 2026-06-30. Finally, GROUP BY groups what remains by zone, so AVG(delivery_time) returns one average per zone. None of this is new syntax — it is the same clauses already learned, applied to QuickRide's own tables. ⟦A.f1 A.f2 A:tb4 A:tb5⟧

### s03 · video · Watch: building a JOIN + WHERE + GROUP BY query  [reward 1]
SQL Integration — This clip shows a multi-clause SELECT being built from scratch. Note: the date function used is SQL Server-specific; the capstone uses a plain date comparison in WHERE instead.
[VIDEO Building a JOIN + WHERE + GROUP BY query from scratch in a single SELECT] bridge-before: Watch how the instructor layers the FROM joins first, then adds WHERE and GROUP BY — all inside one SELECT. Note: the FORMAT date function is SQL Server-specific; the capstone uses a plain date range in WHERE instead. | bridge-after: The key takeaway is clause order: joins combine tables first, WHERE filters next, GROUP BY groups last — exactly as the capstone query does. The text covers the capstone's own table names and date filter.
  - xkYpNfpmbGY 592-770s facts=['f1', 'f2'] label: Building a JOIN + WHERE + GROUP BY query from scratch in a single SELECT | summary: The instructor builds a query from scratch against a shipments dataset. Two INNER JOINs are added in the FROM clause — one to a product table, one to a people table — before any filtering is specified. A WHERE clause then narrows rows to a specific product category and salesperson. A GROUP BY groups the remaining rows by month, and aggregate functions (SUM) produce one total per group. The instructor runs the query and confirms it returns only the filtered, grouped rows. Note: the date-formatting function used (FORMAT with 'MMM yy') is SQL Server dialect and is not part of the capstone's required syntax; the capstone query uses a standard date comparison in the WHERE clause instead.

### s04 · check · Where does the INNER JOIN go?  [reward 2]
Quick check — Test your understanding of where a JOIN fits inside a SELECT statement.
QUESTION [choice, core, grading=client] In a SELECT statement that also has a WHERE clause and a GROUP BY clause, where does an INNER JOIN appear?
  ✔ opt_from: In the FROM clause, before WHERE and GROUP BY are applied.
      why: Correct. The INNER JOIN is part of the FROM clause: it combines matching rows from both tables before the WHERE filter and GROUP BY grouping are applied.
  ✘ opt_where: In the WHERE clause, alongside the filter conditions.
      why: The WHERE clause filters rows after the tables have already been joined. The JOIN itself belongs in the FROM clause, not in WHERE.
  ✘ opt_group: In the GROUP BY clause, to combine groups from both tables.
      why: GROUP BY groups the already-joined and already-filtered rows into summary groups. The JOIN that combines the two tables happens earlier, in the FROM clause.
  ✘ opt_select: In the SELECT clause, to choose which columns to combine.
      why: SELECT names the columns to return from the result. The JOIN that combines rows from two tables is specified in the FROM clause, not in SELECT.
  feedback✔: Right. INNER JOIN ... ON goes inside the FROM clause, so the database combines the two tables first, then applies WHERE and GROUP BY.  feedback✘: Think about the order SQL processes a query: it first assembles the rows (FROM + JOIN), then filters them (WHERE), then groups them (GROUP BY). Which clause assembles the rows?  hints: ['SQL processes FROM before WHERE and GROUP BY. The JOIN is part of assembling the rows, not filtering or grouping them.', 'The syntax is: FROM orders o INNER JOIN drivers d ON o.driver_id = d.driver_id — notice it sits right after FROM.']  remediation→r01
  MEASURES: A:include_inner_join_in_from_clause_before_where_and_group_by(f2)   anchors=['assessment:include_inner_join_in_from_clause_before_where_and_group_by']
  taught-before-tested: A.f2←s01

### s05 · hands_on · Write the capstone retrieval query  [reward 4]
Hands-on practice — Write the SQL query that retrieves last quarter's QuickRide orders, joining the orders and drivers tables, filtering to the correct date range, and grouping by zone.
QUESTION [code_exercise, stretch, grading=client] Two tables are available: **orders** (columns: order_id, driver_id, zone, order_date, delivery_time) and **drivers** (columns: driver_id, driver_name).

The query below is almost complete. Add the GROUP BY clause at the end to group by zone.

The result should have one row per zone with the average delivery_time.
  runtime={'kind': 'sql', 'version': '1.32.0'} constraints.allowed=['SELECT', 'FROM', 'INNER JOIN ... ON', 'WHERE', 'AND', 'GROUP BY', 'AVG()', 'table alias (e.g. o, d)', 'date literal comparison (>=, <)', 'column dot notation (e.g. o.zone, o.driver_id)'] blocked=11 items
  file query.sql [editable]:
SELECT zone, AVG(delivery_time)
FROM orders o
INNER JOIN drivers d ON o.driver_id = d.driver_id
WHERE order_date >= '2026-04-01' AND order_date < '2026-07-01'
-- Add GROUP BY clause here

  SOLUTION query.sql:
SELECT zone, AVG(delivery_time)
FROM orders o
INNER JOIN drivers d ON o.driver_id = d.driver_id
WHERE order_date >= '2026-04-01' AND order_date < '2026-07-01'
GROUP BY zone
  test t_zone_avg (query_result_equals, visible=True): {"expected":{"columns":["zone","avg(delivery_time)"],"rows":[["Ikeja",52.0],["Lekki",30.285714285714285],["Surulere",25.714285714285715],["Yaba",33.75]]},"ordered":false} | on-fail: Your query should return one row per zone with the average delivery_time for orders placed between 2026-04-01 and 2026-06-30. Check your JOIN condition, date filter, and GROUP BY clause.
  provenance: {"runtime":"duckdb-wasm","runtime_version":"1.32.0","solution_sha256":"84941c3da2777024f2b00768eb3bc0a792426ce692de8e8286faf1a771cff78a","tests_passed":1}
  feedback✔: Well done. Your query joins the two tables, filters to last quarter, and groups by zone — all in one SELECT statement.  feedback✘: Check that your query has INNER JOIN in the FROM clause, a WHERE clause with both date conditions joined by AND, and GROUP BY zone.  hints: ['The INNER JOIN goes right after the first table name in FROM: FROM orders o INNER JOIN drivers d ON o.driver_id = d.driver_id.', "The WHERE clause needs two conditions: o.order_date >= '2026-04-01' AND o.order_date < '2026-07-01'."]  remediation→r01
  MEASURES: A:write_select_with_from_where_group_by_in_one_statement(f1); A:apply_combined_join_filter_group_query_to_capstone_dataset(f1,f2)   anchors=['practice', 'assessment:write_select_with_from_where_group_by_in_one_statement', 'assessment:apply_combined_join_filter_group_query_to_capstone_dataset']
  taught-before-tested: A.f1←s01; A.f1←s01; A.f2←s01

### s06 · explainer · PivotTable and COUNTIFS on the capstone delivery sheet  [reward 3]
Spreadsheet Integration — The capstone's spreadsheet step pairs each order's zone and delivery_time with the driver's shift. A PivotTable and COUNTIFS turn that sheet into a zone-by-shift summary.
### Building a PivotTable from the delivery sheet
(mechanism) A PivotTable is built by selecting the data range and inserting a PivotTable, then adding fields: non-numeric fields default to Rows, date/time fields to Columns, and numeric fields to Values. Fields can be dragged between areas to rearrange the summary. In the capstone, `zone` and `shift` (both non-numeric) default to Rows, while `delivery_time` (numeric) goes to Values. ⟦B.f1 B:tb2⟧
(mechanism) COUNTIFS(criteria_range1, criteria1, [criteria_range2, criteria2]…) applies criteria across one or more ranges and counts the cells where **all** criteria are met. In the capstone, `COUNTIFS(zone_range, "Ikeja", delivery_time_range, ">45")` counts how many Ikeja deliveries exceeded 45 minutes. ⟦B.f2 B:tb3⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_capstone_integrate_tools_model.s06.b4","asset_ref":{"asset_id":"ds_capstone_delivery_sheet"},"sheet_name":"DeliverySheet","range":"A1:C10","show_formula_bar":true,"cells":[{"ref":"E1","note":"PivotTable: zone (Rows) × shift (Columns), Average delivery_time (Values)"},{"ref":"E8","formula":"=COUNTIFS(A2:A37,\"Ikeja\",C2:C37,\">45\")","note":"Count Ikeja deliveries over 45 minutes"}],"annotations":[{"target":"A1:C1","text":"Source data: zone, shift, delivery_time"},{"target":"E1","text":"PivotTable output: zone × shift grid, Average delivery_time per cell"},{"target":"E8","text":"COUNTIFS: counts rows where zone=Ikeja AND delivery_time>45"}],"lineage":{"concept_ids":["capstone.integrate_spreadsheet"],"fact_ids":["capstone.integrate_spreadsheet#f1","capstone.integrate_spreadsheet#f2"],"teaching_block_ids":["capstone.integrate_spreadsheet#tb2","capstone.integrate_spreadsheet#tb3"],"anchors":["capstone.integrate_spreadsheet#visual"]},"computed_values":{"E8":2}}

### s07 · explainer · Rearranging the PivotTable and applying COUNTIFS  [reward 2]
Spreadsheet Integration — Dragging shift from Rows to Columns turns the PivotTable into a zone-by-shift grid. COUNTIFS then counts deliveries that meet two criteria at once.
(example) For the capstone delivery sheet, selecting the data range and inserting a PivotTable places `zone` and `shift` in Rows by default and `delivery_time` in Values. Dragging `shift` from Rows to Columns rearranges the summary into a zone-by-shift grid; changing the Values summary function to Average makes each cell an average delivery time. ⟦B.f1 B:tb4⟧
(example) Separately, `COUNTIFS(zone_range, "Ikeja", delivery_time_range, ">45")` counts how many Ikeja deliveries in the sheet took more than 45 minutes — both criteria (zone and time threshold) must be met at once. The PivotTable and COUNTIFS skills already learned are now run on this project's own roster and delivery data. ⟦B.f2 B:tb4 B:tb5⟧

### s08 · video · Watch: inserting a PivotTable and arranging fields  [reward 1]
Spreadsheet Integration — This clip shows how non-numeric fields land in Rows automatically and a numeric field jumps to Values. Note: the clip uses an advertising dataset, not the capstone's delivery sheet.
[VIDEO Building a PivotTable: selecting a range, inserting, and dragging fields] bridge-before: Watch how non-numeric fields land in Rows automatically and a numeric field jumps to Values — that default behaviour is the core rule. Note: the clip uses an advertising dataset, not the capstone's delivery sheet. | bridge-after: The clip does not show date/time fields defaulting to Columns, nor COUNTIFS — the text covers both. Apply the same insert-and-drag steps to the capstone's zone, shift, and delivery_time fields.
  - K3KqOTdypyw 36-302s facts=['f1'] label: Inserting a PivotTable and arranging fields across Rows, Columns, and Values | summary: Starting from an advertising-campaign dataset formatted as a structured table, the presenter inserts a PivotTable via Insert > PivotTable. Text-based fields (channel, campaign name) are checked and land in Rows automatically; a categorical field (market) is dragged into Columns; a numeric field (spend) is checked and goes straight to Values because the tool recognises it as numeric. A Filters area narrows the view to active campaigns. The presenter then removes a field and adds revenue alongside spend to Values, showing how the layout updates instantly — by default the tool sums numeric values, which suits the question at hand.

### s09 · check · Applying COUNTIFS with multiple criteria  [reward 2]
Quick check — Test your understanding of how COUNTIFS handles more than one criterion.
QUESTION [choice, core, grading=client] A spreadsheet has zone values in column A and delivery_time values in column C (rows 2–37). Which formula correctly counts the rows where zone is 'Ikeja' AND delivery_time is greater than 45?
  ✔ opt_correct: =COUNTIFS(A2:A37,"Ikeja",C2:C37,">45")
      why: Correct. COUNTIFS takes pairs of (criteria_range, criteria): the first pair checks zone = 'Ikeja' and the second checks delivery_time > 45. Both criteria must be met for a row to be counted.
  ✘ opt_countif_single: =COUNTIF(A2:A37,"Ikeja",C2:C37,">45")
      why: COUNTIF (without the S) accepts only one criteria range and one criterion. To apply two criteria at once you need COUNTIFS, which takes pairs of (range, criterion) and counts rows where all criteria are met.
  ✘ opt_wrong_order: =COUNTIFS(C2:C37,">45","Ikeja",A2:A37)
      why: COUNTIFS expects each criterion immediately after its range: (range1, criterion1, range2, criterion2). Placing the criterion text 'Ikeja' where a range is expected causes an error.
  ✘ opt_sumif: =SUMIF(A2:A37,"Ikeja",C2:C37)
      why: SUMIF adds up values in a sum range where a single criterion is met — it does not count rows. To count rows matching multiple criteria, use COUNTIFS.
  feedback✔: Exactly right. COUNTIFS(range1, criterion1, range2, criterion2) counts rows where every criterion is satisfied.  feedback✘: COUNTIFS takes pairs of (criteria_range, criteria). Make sure you are using COUNTIFS (not COUNTIF) and that each range is immediately followed by its criterion.  hints: ['COUNTIF handles one criterion; COUNTIFS handles one or more. Here you have two criteria, so you need COUNTIFS.', 'The syntax is COUNTIFS(range1, criterion1, range2, criterion2). Each range must come right before its matching criterion.']  remediation→r02
  MEASURES: B:apply_countifs_with_multiple_criteria_ranges(f2)   anchors=['assessment:apply_countifs_with_multiple_criteria_ranges']
  taught-before-tested: B.f2←s06

### s10 · check · Executing the capstone spreadsheet analysis step  [reward 2]
Quick check — Test your understanding of how PivotTable and COUNTIFS work together to complete the capstone spreadsheet analysis.
QUESTION [choice, core, grading=client] You have a delivery sheet with columns zone, shift, and delivery_time. You want to produce (a) a zone-by-shift grid showing average delivery_time, and (b) a count of Ikeja deliveries that took more than 45 minutes. Which combination of tools completes both tasks?
  ✔ opt_pivot_countifs: A PivotTable with zone in Rows, shift in Columns, and average delivery_time in Values; plus a COUNTIFS formula for the count.
      why: Correct. A PivotTable with zone in Rows, shift in Columns, and average delivery_time in Values produces the zone-by-shift grid. A separate COUNTIFS formula counts rows matching both the zone and the delivery_time threshold.
  ✘ opt_pivot_only: A PivotTable alone — it can produce both the zone-by-shift grid and the filtered count in one step.
      why: A PivotTable can produce the zone-by-shift average grid, but it cannot directly apply a threshold filter like 'delivery_time > 45' to count matching rows. That requires a COUNTIFS formula.
  ✘ opt_countifs_only: A COUNTIFS formula alone — it can produce both the grid and the count.
      why: COUNTIFS counts rows matching criteria but cannot produce a two-dimensional zone-by-shift grid of averages. The grid requires a PivotTable.
  ✘ opt_sumif_pivot: A SUMIF formula for the grid and a PivotTable for the count.
      why: SUMIF adds values matching one criterion — it does not produce a two-dimensional average grid. The grid needs a PivotTable, and the filtered count needs COUNTIFS.
  feedback✔: Right. PivotTable handles the two-dimensional average summary; COUNTIFS handles the multi-criterion count.  feedback✘: Think about what each tool does: a PivotTable creates a cross-tabulation of averages; COUNTIFS counts rows matching multiple criteria. Which task needs which tool?  hints: ['A PivotTable can cross-tabulate averages by two categorical fields (zone and shift). Can it also apply a numeric threshold filter to count rows?', 'COUNTIFS(range1, criterion1, range2, criterion2) counts rows where all criteria are met — it does not produce a grid of averages.']  remediation→r02
  MEASURES: B:execute_capstone_spreadsheet_analysis_step(f1,f2); B:build_pivot_table_with_correct_field_placement(f1)   anchors=['assessment:execute_capstone_spreadsheet_analysis_step', 'assessment:build_pivot_table_with_correct_field_placement']
  taught-before-tested: B.f1←s06; B.f2←s06; B.f1←s06

### s11 · hands_on · Build the capstone PivotTable  [reward 4]
Hands-on practice — Using the capstone delivery sheet, build a zone-by-shift PivotTable showing average delivery time per cell.
QUESTION [formula_entry, stretch, grading=client] The capstone delivery sheet is loaded with zone in column A, shift in column B, and delivery_time in column C (header in row 1, data in rows 2–37). In cell E2, write a COUNTIFS formula that counts the rows where zone is 'Ikeja' AND delivery_time is greater than 45.
  [unrendered interaction type formula_entry] public={"prompt":"The capstone delivery sheet is loaded with zone in column A, shift in column B, and delivery_time in column C (header in row 1, data in rows 2–37). In cell E2, write a COUNTIFS formula that counts the rows where zone is 'Ikeja' AND delivery_time is greater than 45.","asset_ref":{"asset_id":"ds_capstone_delivery_sheet","columns":["zone","shift","delivery_time"]},"sheet_name":"ds_capstone_delivery_sheet","target_cell":"E2"} grading={"expected_value":2,"reference_formula":"=COUNTIFS(A2:A37,\"Ikeja\",C2:C37,\">45\")","must_use_functions":["COUNTIFS"]}
  feedback✔: Correct. COUNTIFS(A2:A37,"Ikeja",C2:C37,">45") counts the 2 Ikeja deliveries that took more than 45 minutes.  feedback✘: Check that you are using COUNTIFS (not COUNTIF), that the zone range is A2:A37 with criterion "Ikeja", and that the delivery_time range is C2:C37 with criterion ">45".  hints: ['COUNTIFS takes pairs: (criteria_range1, criteria1, criteria_range2, criteria2). Your first pair checks zone; your second pair checks delivery_time.', 'The criterion for \'greater than 45\' is written as the text string ">45" inside the formula.']  remediation→r03
  MEASURES: B:apply_countifs_with_multiple_criteria_ranges(f2)   anchors=['practice', 'assessment:apply_countifs_with_multiple_criteria_ranges']
  taught-before-tested: B.f2←s06

### s12 · explainer · Cleaning and grouping the capstone orders in pandas  [reward 3]
Python / pandas Integration — Once orders are retrieved, pandas handles cleaning and aggregation. isna()/dropna() remove missing delivery times; groupby().mean() produces one average per zone.
### Detecting and removing missing values
(mechanism) isna() detects which values in a DataFrame are missing, and dropna() removes rows with missing values — or fillna() replaces them with a specified value. In the capstone, `orders['delivery_time'].isna()` flags rows with no delivery time recorded; those rows are then removed with dropna() before any aggregation. ⟦C.f1 C:tb2⟧
(mechanism) A groupby operation splits data into groups based on some criteria, applies a function independently to each group, and combines the results back into a single structure. An aggregation reduces each group to one summary value per column. In the capstone, `orders.groupby('zone')['delivery_time'].mean()` splits the cleaned orders by zone and returns one mean delivery time per zone. ⟦C.f2 C:tb3⟧
[BEFORE_AFTER] dropna() removes rows where delivery_time is NULL; groupby('zone')['delivery_time'].mean() reduces each zone to one average.
  before:
[TABLE ds_pandas_orders cols=['zone', 'delivery_time'] highlights=[["cell","delivery_time","NaN — missing delivery time"]]] caption: Raw orders DataFrame — NaN delivery_time rows visible
  after:
[TABLE computed result ] caption: After dropna() + groupby('zone').mean() — one mean per zone
  produced by sql: SELECT zone, AVG(delivery_time) AS mean_delivery_time FROM ds_pandas_orders WHERE delivery_time IS NOT NULL GROUP BY zone ORDER BY zone
  result columns=['zone', 'mean_delivery_time'] rows(4)=[["Ikeja",36],["Lekki",29],["Surulere",25],["Yaba",34.333333333333336]]

### s13 · explainer · The same skills, applied to the capstone's own data  [reward 2]
Python / pandas Integration — The isna()/dropna()/fillna() and groupby() skills already learned are now run on the capstone's retrieved orders instead of a practice dataset.
(example) On the capstone's retrieved orders, `orders['delivery_time'].isna()` flags rows with no delivery time; dropna() removes them. Then `orders.groupby('zone')['delivery_time'].mean()` splits the cleaned orders by zone, computes the mean delivery time within each zone, and combines the per-zone results — an aggregation, since each zone group is reduced to a single number. ⟦C.f1 C.f2 C:tb4 C:tb5⟧

### s14 · check · Cleaning and aggregating the capstone dataset end-to-end  [reward 2]
Quick check — Test your understanding of how isna()/dropna() and groupby().mean() work together to clean and summarise the capstone orders.
QUESTION [choice, core, grading=client] A DataFrame `df` has columns `zone` and `delivery_time`, with some NaN values in `delivery_time`. Which sequence of operations produces a Series showing the mean delivery_time per zone, using only rows where delivery_time is not missing?
  ✔ opt_correct: df.dropna() then df.groupby('zone')['delivery_time'].mean()
      why: Correct. dropna() removes rows with any NaN value, so the subsequent groupby().mean() computes the mean only from rows with a recorded delivery_time.
  ✘ opt_fillna_group: df.fillna(0) then df.groupby('zone')['delivery_time'].mean()
      why: fillna(0) replaces NaN with 0, which pulls the mean downward — a 0-minute delivery is not a real observation. To exclude missing rows entirely, use dropna() instead.
  ✘ opt_group_only: df.groupby('zone')['delivery_time'].mean() directly, without any cleaning step
      why: pandas groupby().mean() skips NaN values by default, so the result would be numerically the same. However, calling dropna() first makes the cleaning step explicit in your code: anyone reading the workflow can see that missing rows were intentionally removed, making the analysis visible and reproducible rather than relying on a silent default.
  ✘ opt_isna_group: df.isna() then df.groupby('zone')['delivery_time'].mean()
      why: isna() returns a boolean DataFrame showing where values are missing — it does not remove those rows. To remove rows with missing values, use dropna().
  feedback✔: Right. dropna() removes rows with missing delivery_time, then groupby('zone')['delivery_time'].mean() computes one mean per zone.  feedback✘: Think about what each method does: isna() detects missing values, dropna() removes rows with them, fillna() replaces them. Which one removes the rows so the mean is computed only from real observations?  hints: ['isna() returns True/False for each cell — it does not change the DataFrame. dropna() actually removes rows that contain NaN.', 'fillna(0) keeps all rows but replaces NaN with 0. Would a 0-minute delivery time give a correct mean?']  remediation→r04
  MEASURES: C:clean_and_aggregate_capstone_dataset_end_to_end(f1,f2)   anchors=['assessment:clean_and_aggregate_capstone_dataset_end_to_end']
  taught-before-tested: C.f1←s12; C.f2←s12

### s15 · hands_on · Detect missing values and compute per-zone means  [reward 4]
Hands-on practice — Given a small orders DataFrame with zone and delivery_time columns (some NaN), detect the missing delivery times, remove those rows, then compute the mean delivery time per zone.
QUESTION [code_exercise, stretch, grading=client] The DataFrame `df` is loaded from `orders.csv` with columns `zone` and `delivery_time`. Some `delivery_time` values are NaN.

1. Print the result of `df['delivery_time'].isna()` to see which rows are missing.
2. Remove rows with missing delivery_time using `dropna()` and reassign the result to `df`.
3. Compute the mean delivery_time per zone using `groupby` and `mean()`. Assign the result to a variable named `zone_means` and print it.

The final output must show one mean delivery_time value per zone.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=['import pandas as pd', 'pd.DataFrame()', "df['column'].isna()", 'df.dropna()', 'df.fillna(value)', "df.groupby('column')['column'].mean()", "df.groupby('column').agg()", 'variable assignment', 'print()', 'f-strings', 'basic arithmetic operators', 'for loops', 'if/elif/else', 'list and dict literals', 'pd.read_csv()'] blocked=10 items
  file solution.py [editable]:
import pandas as pd

df = pd.read_csv('orders.csv')

# Step 1: print which delivery_time values are missing
# print(df['delivery_time'].isna())

# Step 2: remove rows with missing delivery_time
# df = df.dropna()

# Step 3: compute mean delivery_time per zone and print
# print(...)

  SOLUTION solution.py:
import pandas as pd

df = pd.read_csv('orders.csv')

# Step 1: print which delivery_time values are missing
print(df['delivery_time'].isna())

# Step 2: remove rows with missing delivery_time
df = df.dropna()

# Step 3: compute mean delivery_time per zone and print
zone_means = df.groupby('zone')['delivery_time'].mean()
print(zone_means)

  test t_zone_means (dataframe_equals, visible=True): {"expr":"zone_means.reset_index()","expected":{"columns":["zone","delivery_time"],"rows":[["Ikeja",36.0],["Lekki",29.0],["Surulere",25.0],["Yaba",34.333333333333336]]},"ordered":true,"tolerance":1e-06} | on-fail: After dropna(), groupby('zone')['delivery_time'].mean() should return one mean per zone. Check that you assigned the cleaned DataFrame to 'clean' and used groupby correctly.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"df93f67bbf0d815c16b4fa1c30fbcbd335506cb57c762dab4dab25132a76b119","tests_passed":1}
  feedback✔: Well done. You detected missing values with isna(), removed them with dropna(), and computed per-zone means with groupby().mean().  feedback✘: Make sure you: (1) call df.dropna() and reassign the result to 'df', and (2) call df.groupby('zone')['delivery_time'].mean() to get one mean per zone.  hints: ["df.dropna() returns a new DataFrame with NaN rows removed — reassign it to 'df'.", "To get one mean per zone: df.groupby('zone')['delivery_time'].mean()"]  remediation→r04
  MEASURES: C:detect_and_handle_missing_values_with_isna_dropna_fillna(f1); C:apply_groupby_aggregation_to_summarize_groups(f2)   anchors=['practice', 'assessment:detect_and_handle_missing_values_with_isna_dropna_fillna', 'assessment:apply_groupby_aggregation_to_summarize_groups']
  taught-before-tested: C.f1←s12; C.f2←s12

### s16 · explainer · Primary keys, foreign keys, and one-to-many in the capstone  [reward 3]
Data Modelling — The capstone spans two tables — Orders and Drivers. Before any join or aggregation across them can be trusted, the key columns and their relationship need to be correctly identified.
### Primary keys and foreign keys
(mechanism) A primary key uniquely identifies each row of a table; a foreign key's values must match values appearing in some row of the table it references. In the capstone, the Drivers table needs a column that uniquely identifies each driver, and the Orders table needs a column whose values must match one of those driver identifiers. ⟦D.f1 D:tb2⟧
(mechanism) In a one-to-many relationship, one row on the 'one' side relates to many rows on the 'many' side — for example, one department has many employees. In the Customer/Order example, the foreign key CustID is placed in the Order table and must match a valid CustID in the Customer table. In the capstone, one driver can appear in many orders: the same one-to-many pattern. ⟦D.f2 D:tb3⟧
[DIAGRAM: Capstone data model: Drivers (1) → Orders (many)] nodes=['Drivers {driver_id (PK); driver_name}', 'Orders {order_id (PK); driver_id (FK); zone; order_date; delivery_time}'] edges=[('drivers_table', 'orders_table', 'one driver → many orders')] alt: Entity-relationship diagram showing two boxes: Drivers (driver_id as PK, driver_name) and Orders (order_id as PK, driver_id as FK, zone, order_date, delivery_time). An arrow from Drivers.driver_id to Orders.driver_id is labelled '1:N — one driver → many orders'.

### s17 · explainer · Mapping the capstone tables onto the model  [reward 2]
Data Modelling — Getting the primary key / foreign key pairing right connects the two tables correctly before any join or aggregation across them can be trusted.
(example) In the capstone: Drivers has `driver_id` as its primary key, uniquely identifying each driver row. Orders has its own primary key, `order_id`, plus a `driver_id` column that is a foreign key — its values must match a `driver_id` that already exists in Drivers. Since one driver delivers many orders, this is a one-to-many relationship: one row on the Drivers ('one') side relates to many rows on the Orders ('many') side. ⟦D.f1 D.f2 D:tb4 D:tb5⟧

### s18 · check · Identifying the one-to-many relationship in the capstone  [reward 2]
Quick check — Test your understanding of the one-to-many relationship between the Drivers and Orders tables.
QUESTION [choice, core, grading=client] In the capstone data model, one driver can deliver many orders, but each order is assigned to exactly one driver. Which statement correctly describes this relationship?
  ✔ opt_one_to_many: Drivers is on the 'one' side and Orders is on the 'many' side; the foreign key driver_id is placed in the Orders table.
      why: Correct. Drivers is on the 'one' side (one driver) and Orders is on the 'many' side (many orders per driver). The foreign key driver_id is placed in the Orders table and must match a valid driver_id in the Drivers table.
  ✘ opt_many_to_one: Orders is on the 'one' side and Drivers is on the 'many' side; the foreign key is placed in the Drivers table.
      why: The sides are reversed. Drivers is on the 'one' side because one driver can have many orders. The foreign key goes in the 'many' table — Orders — not in Drivers.
  ✘ opt_many_to_many: It is a many-to-many relationship because a driver can have many orders and an order can have many drivers.
      why: Each order is assigned to exactly one driver, so the relationship is not many-to-many. One driver can have many orders, but each order has only one driver — that is a one-to-many relationship.
  ✘ opt_one_to_one: It is a one-to-one relationship because each order has exactly one driver.
      why: One-to-one means each row on one side matches exactly one row on the other. Here, one driver can match many orders, so the relationship is one-to-many, not one-to-one.
  feedback✔: Right. One driver → many orders. The foreign key driver_id lives in the Orders table and references the Drivers table.  feedback✘: Ask: can one driver have more than one order? Yes — so Drivers is on the 'one' side and Orders is on the 'many' side. The foreign key goes in the 'many' table.  hints: ["The 'one' side is the table where each row can relate to multiple rows in the other table. Which table is that here — Drivers or Orders?", "In a one-to-many relationship, the foreign key is always placed in the 'many' table to reference the 'one' table."]  remediation→r05
  MEASURES: D:identify_one_to_many_relationship_between_drivers_and_orders(f2)   anchors=['assessment:identify_one_to_many_relationship_between_drivers_and_orders']
  taught-before-tested: D.f2←s16

### s19 · hands_on · Match columns to their roles in the capstone data model  [reward 4]
Hands-on practice — Match each column from the Drivers and Orders tables to its role: primary key of Drivers, primary key of Orders, or foreign key in Orders referencing Drivers. Then identify which table is on the 'one' side and which is on the 'many' side.
QUESTION [classify, stretch, grading=client] Classify each item into its correct role in the capstone data model. The two tables are **Drivers** (columns: driver_id, driver_name) and **Orders** (columns: order_id, driver_id, zone, order_date, delivery_time).
  'driver_id column in the Drivers table' -> Primary key of Drivers
      feedback: driver_id in the Drivers table uniquely identifies each driver — it is the primary key of Drivers.
  'order_id column in the Orders table' -> Primary key of Orders
      feedback: order_id in the Orders table uniquely identifies each order — it is the primary key of Orders.
  'driver_id column in the Orders table' -> Foreign key in Orders (references Drivers)
      feedback: driver_id in the Orders table references the Drivers table's primary key — it is a foreign key.
  'Drivers table' -> 'One' side of the relationship
      feedback: One driver can have many orders, so Drivers is on the 'one' side of the one-to-many relationship.
  'Orders table' -> 'Many' side of the relationship
      feedback: Many orders can belong to one driver, so Orders is on the 'many' side of the one-to-many relationship.
  feedback✔: Correct. driver_id is the primary key of Drivers and a foreign key in Orders; order_id is the primary key of Orders; Drivers is the 'one' side and Orders is the 'many' side.  feedback✘: Check: which column uniquely identifies each driver? Which column in Orders references that driver? And which table can have multiple rows for the same entity on the other side?  hints: ['A primary key uniquely identifies each row in its own table. A foreign key in one table references the primary key of another table.', "In a one-to-many relationship, the 'one' side is the table where each row can relate to many rows in the other table."]  remediation→r05
  MEASURES: D:build_capstone_data_model_with_correct_keys_and_relationships(f1,f2); D:identify_primary_and_foreign_keys_in_capstone_tables(f1); D:identify_one_to_many_relationship_between_drivers_and_orders(f2)   anchors=['practice', 'assessment:build_capstone_data_model_with_correct_keys_and_relationships', 'assessment:identify_primary_and_foreign_keys_in_capstone_tables', 'assessment:identify_one_to_many_relationship_between_drivers_and_orders']
  taught-before-tested: D.f1←s16; D.f2←s16; D.f1←s16; D.f2←s16

### s20 · recap · What you've built so far  [reward 2]
Tile recap — You've connected all four tools to the capstone project: SQL retrieves the data, spreadsheets summarise it, pandas cleans and aggregates it, and the data model links the two tables correctly.
(takeaway) A single SELECT statement combines JOIN, WHERE, and GROUP BY to retrieve last quarter's QuickRide orders by zone. A PivotTable and COUNTIFS on the delivery sheet summarise zone-by-shift performance. isna()/dropna() and groupby().mean() clean and aggregate the orders in pandas. Drivers.driver_id (PK) links to Orders.driver_id (FK) in a one-to-many relationship — the same patterns already learned, applied to this project's own data. ⟦A.f1 A.f2 B.f1 B.f2 C.f1 C.f2 D.f1 D.f2 A:tb5 B:tb5 C:tb5 D:tb5⟧
[UP NEXT] Up next: Descriptive statistics on the capstone data: In the next tile you'll run describe() on the cleaned delivery_time column and decide whether the mean or the median better answers the business question.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Where does the INNER JOIN go in a SELECT statement? — The check asked where an INNER JOIN fits inside a SELECT. Here's the key rule.
(mechanism) An INNER JOIN is placed in the **FROM clause** of a SELECT statement — not in WHERE or GROUP BY. The FROM clause (including any JOINs) runs first, combining matching rows from both tables. The WHERE clause then filters those combined rows, and GROUP BY groups what remains. In the capstone query, `FROM orders o INNER JOIN drivers d ON o.driver_id = d.driver_id` combines the two tables before any filtering or grouping. ⟦A.f2 A:tb3 A:tb4⟧
(misconception) A common mistake is placing the JOIN condition in the WHERE clause (e.g. `WHERE o.driver_id = d.driver_id`). While some databases accept this older syntax, the standard and clearer approach is `INNER JOIN … ON` in the FROM clause, which makes the join explicit and keeps the WHERE clause for row filtering only. ⟦A.f2 A:tb3⟧
### r02 · How COUNTIFS applies multiple criteria — The check asked how COUNTIFS handles more than one criterion. Here's the key rule.
(mechanism) COUNTIFS(criteria_range1, criteria1, criteria_range2, criteria2) counts only the rows where **all** criteria are met simultaneously. Each criteria_range/criteria pair is evaluated independently, and only rows that pass every pair are counted. In the capstone, `COUNTIFS(zone_range, "Ikeja", delivery_time_range, ">45")` counts rows where the zone is Ikeja **and** the delivery time exceeds 45 minutes — both conditions must hold. ⟦B.f2 B:tb3 B:tb4⟧
(misconception) COUNTIFS is not the same as two separate COUNTIF calls added together. Adding two COUNTIF results would count rows that meet either criterion, not both. COUNTIFS enforces all criteria at once, so the count is always ≤ the count from any single criterion alone. ⟦B.f2 B:tb3⟧
### r03 · PivotTable field placement and COUNTIFS together — The check asked about executing the full capstone spreadsheet analysis step. Here are the two key rules.
(mechanism) When you add a field to a PivotTable, the tool places it based on its data type: **non-numeric fields** (like zone and shift) default to Rows, **date/time fields** default to Columns, and **numeric fields** (like delivery_time) default to Values. You can drag any field between Rows, Columns, Values, and Filters to rearrange the summary. In the capstone, dragging `shift` from Rows to Columns turns the layout into a zone-by-shift grid. ⟦B.f1 B:tb2 B:tb4⟧
### r04 · Cleaning and aggregating: isna()/dropna() then groupby().mean() — The check asked about the full clean-and-aggregate workflow. Here are the two steps.
(mechanism) isna() returns a boolean mask showing which values are missing (NaN). dropna() removes rows with missing values; fillna(value) replaces them. In the capstone, `orders["delivery_time"].isna()` identifies which orders have no recorded delivery time; dropna() removes those rows before any aggregation runs. ⟦C.f1 C:tb2 C:tb4⟧
(mechanism) A groupby operation splits data into groups, applies a function independently to each group, and combines the results. An aggregation reduces each group to one summary value. In the capstone, `orders.groupby("zone")["delivery_time"].mean()` splits the cleaned orders by zone and returns one mean delivery time per zone — an aggregation. ⟦C.f2 C:tb3 C:tb4⟧
### r05 · The one-to-many relationship between Drivers and Orders — The check asked about the one-to-many relationship in the capstone. Here is the key rule.
(mechanism) In a one-to-many relationship, one row on the "one" side relates to many rows on the "many" side. The foreign key is placed on the "many" side. In the capstone, one driver (Drivers table, "one" side) can appear in many orders (Orders table, "many" side), so `driver_id` as a foreign key sits in the Orders table — the same pattern as CustID sitting in the Order table. ⟦D.f2 D:tb3 D:tb4⟧
(misconception) A common mistake is placing the foreign key on the "one" side. The foreign key always goes on the "many" side — the table that can have multiple rows for the same related entity. In the capstone, Orders (many orders per driver) holds the `driver_id` foreign key, not Drivers. ⟦D.f2 D:tb3⟧

## OTHER CONTENT (fields without a dedicated renderer)
· feedback.hints: The criterion for 'greater than 45' is written as the text string ">45" inside the formula.
· role_map.bucket_one_side: one side of the one-to-many relationship
· role_map.bucket_many_side: many side of the one-to-many relationship

=========

# EVALUATOR PACKET — Descriptive Statistics and Dashboard (tile_capstone_stats_dashboard)
Tile summary: Apply pandas describe() to the capstone delivery data, choose between mean and median based on skew and the business question, then build a multi-panel matplotlib figure using either plt.subplots(2, 2) or plt.subplot(131/132/133) + plt.suptitle().
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = capstone.applying_descriptive_statistics — Applying descriptive statistics to capstone findings
B = capstone.building_dashboard_or_viz — Building a polished matplotlib/seaborn visualization set for the capstone

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (capstone.applying_descriptive_statistics)   objective: Compute and interpret the descriptive statistics (using pandas) that support the capstone project's business question.
A.f1: describe() computes a variety of summary statistics about a Series or the columns of a DataFrame.   [sources: pandas_docs_basics#Summarizing data: describe]
A.f2: The mean is more strongly affected by extreme observations than the median, which is more robust to them; so when the goal is to understand a typical individual value in a skewed dataset, the median can be more useful.   [sources: openintro_statistics_textbook#2.1.6]
note: Applies already-learned describe() and mean/median robustness to the capstone's own delivery_time column -- keep the statistics themselves brief, the point is which one answers this question.
PRACTICE ANCHOR (live_code): Given a DataFrame containing a delivery_time column for a single zone, call describe() on that column, then compare the mean and median values it returns and state in a comment which statistic better represents a typical delivery for a skewed distribution.  SUCCESS: describe() is called on the delivery_time column; the learner reads the mean and median from the output; a comment identifies the median as the more useful measure and explains that extreme values pull the mean upward.
ASSESSMENT ANCHOR: compute_and_interpret_descriptive_statistics_for_capstone_business_question facts=['f1', 'f2']
ASSESSMENT ANCHOR: apply_describe_to_capstone_series_or_dataframe_column facts=['f1']
ASSESSMENT ANCHOR: select_mean_or_median_based_on_skew_and_business_question facts=['f2']

## SOURCE FACTS — B (capstone.building_dashboard_or_viz)   objective: Build a coherent set of matplotlib/seaborn charts, arranged and annotated, that presents the capstone's key findings to a stakeholder audience.
B.f1: fig, axs = plt.subplots(2, 2) creates one Figure containing a 2x2 grid of Axes, so several charts can share one figure.   [sources: matplotlib_quickstart_guide#Figure]
B.f2: plt.subplot(131), plt.subplot(132), and plt.subplot(133) can each hold a different chart side by side in one figure, and plt.suptitle() adds one title over the whole figure.   [sources: matplotlib_pyplot_tutorial#Plotting with categorical variables]
note: This applies already-learned matplotlib plotting to the capstone's own figures -- don't re-teach individual chart types, only the multi-panel arrangement.
PRACTICE ANCHOR (live_code): Using the capstone delivery dataset, build a multi-panel figure that places at least three related charts together in one figure and adds a single shared title over all panels.  SUCCESS: Running the cell produces one figure containing multiple axes, each with its own chart and individual title, and a shared figure-level title produced by plt.suptitle(); no separate plt.show() calls are needed per chart.
ASSESSMENT ANCHOR: create_2x2_subplot_grid_with_subplots facts=['f1']
ASSESSMENT ANCHOR: create_side_by_side_subplots_with_suptitle facts=['f2']
ASSESSMENT ANCHOR: select_appropriate_multi_panel_layout_for_capstone_findings facts=['f1', 'f2']

## DATA ASSETS USED
ds_capstone_orders: Capstone Orders Table — columns: order_id(identifier), driver_id(identifier), zone(categorical), order_date(datetime), delivery_time(numerical)
   ["O-001","D01","Ikeja","2026-04-03",28]
   ["O-002","D01","Ikeja","2026-04-10",32]
   ["O-003","D02","Ikeja","2026-04-17",35]
   ["O-004","D02","Ikeja","2026-04-24",36]
   ["O-005","D01","Ikeja","2026-05-02",38]
   ["O-006","D02","Ikeja","2026-05-09",38]
   ["O-007","D01","Ikeja","2026-05-16",42]
   ["O-008","D02","Ikeja","2026-05-23",45]
   variant ds_capstone_orders_messy: 3 ops; planted: issue_impossible_delivery_time(impossible_value); issue_duplicate_order(duplicate_row); issue_zone_casing(inconsistent_category)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Building a polished matplotlib/seaborn visualization set for the capstone; Documenting and presenting the finished capstone deliverable; Independent, unassisted execution across multiple tool families; Producing a stakeholder-facing narrated summary of the capstone

## LESSON, in learner order

### s01 · explainer · Running describe() on the capstone delivery data  [reward 3]
Descriptive Statistics — With cleaned, modelled data, the business question needs actual numbers: how late are deliveries, by zone? describe() gives the full summary in one call.
### Getting the summary statistics
(mechanism) describe() computes a variety of summary statistics about a Series or the columns of a DataFrame — count, mean, std, min, quartiles, and max. In the capstone, running describe() on a zone's `delivery_time` column returns that full summary in one call, without writing separate mean() or std() calls. ⟦A.f1 A:tb2⟧
(mechanism) The mean is more strongly affected by extreme observations than the median, which is more robust to them. When the goal is to understand a typical individual value in a skewed dataset, the median can be more useful. In the capstone, a handful of unusually long deliveries in a zone can pull the mean upward while the median stays closer to the typical delivery. ⟦A.f2 A:tb3⟧
[TABLE computed result highlights=[["row",null,"mean — pulled up by extreme deliveries"],["row",null,"median — more robust to extremes"]]] caption: describe() output for Ikeja delivery_time — mean is noticeably higher than median due to extreme observations
  produced by sql: SELECT 'count' AS statistic, CAST(COUNT(delivery_time) AS DOUBLE) AS value FROM ds_capstone_orders WHERE zone = 'Ikeja' AND delivery_time IS NOT NULL UNION ALL SELECT 'mean', ROUND(AVG(CAST(delivery_time AS DOUBLE)), 1) FROM ds_capstone_orders WHERE zone = 'Ikeja' AND delivery_time IS NOT NULL UNION ALL SELECT 'median', MEDIAN(delivery_time) FROM ds_capstone_orders WHERE zone = 'Ikeja' AND delivery_time IS NOT NULL UNION ALL SELECT 'min', MIN(delivery_time) FROM ds_capstone_orders WHERE zone = 'Ikeja' AND delivery_time IS NOT NULL UNION ALL SELECT 'max', MAX(delivery_time) FROM ds_capstone_orders WHERE zone = 'Ikeja' AND delivery_time IS NOT NULL
  result columns=['statistic', 'value'] rows(5)=[["count",10],["mean",52],["median",38],["min",28],["max",178]]

### s02 · explainer · Choosing mean or median for the business question  [reward 2]
Descriptive Statistics — describe() gives the full summary; deciding which statistic actually answers the business question depends on whether extreme values are skewing that particular column.
(example) Running describe() on Ikeja's `delivery_time` column returns a mean of 52 minutes and a median of 38 minutes. A handful of deliveries in that zone took over three hours — a stalled vehicle, a wrong address — and the mean is pulled up by those extreme observations, while the median stays at 38 minutes. (These numbers reflect the full dataset; in the visible sample, extreme deliveries extend beyond what is shown.) ⟦A.f1 A.f2 A:tb4⟧
(mechanism) The capstone's business question is which zones miss the delivery-time target and by how much — which calls for judging a **typical** delivery against that target, not one skewed by a few rare extremes. So the median is the more useful number here. describe() gives both; the analyst's job is to choose the one that answers the question. ⟦A.f2 A:tb4 A:tb5⟧

### s03 · check · Mean vs median for a skewed distribution  [reward 2]
Quick check — Test your understanding of when to use the median instead of the mean.
QUESTION [choice, core, grading=client] For the Ikeja zone, describe() returns: mean = 52.0 min, median = 38.0 min, max = 178 min. A manager asks: 'What is a typical delivery time for Ikeja?' Which statistic should you report, and why?
  ✔ opt_median: The median (38.0 min), because the 178-min extreme value pulls the mean well above where most deliveries actually land.
      why: Correct. The mean is more strongly affected by extreme observations than the median. The 178-min outlier pulls the mean to 52.0 — well above the 38.0 median — so the median better represents a typical Ikeja delivery.
  ✘ opt_mean: The mean (52.0 min), because it uses every observation and is therefore the most complete summary.
      why: The mean does use every value, but that is exactly why it is misleading here. The single 178-min delivery pulls the mean to 52.0, far above where most deliveries actually land. When the distribution is skewed, the median is the more useful 'typical' measure.
  ✘ opt_max: The maximum (178 min), because it represents the worst-case delivery time the manager should plan for.
      why: The maximum describes the worst case, not a typical value. For a 'what is typical?' question, you need a measure of center — either mean or median — not the extreme.
  ✘ opt_either: Either the mean or the median — they are interchangeable for a typical-value question.
      why: Mean and median are not interchangeable when the distribution is skewed. Here the mean (52.0) and median (38.0) differ by 14 minutes because the 178-min outlier pulls the mean upward. The median is the better 'typical' measure for a skewed dataset.
  feedback✔: Right. When extreme values are present, the median is more robust than the mean and gives a better picture of what is typical.  feedback✘: Compare the mean (52.0) and median (38.0). They differ by 14 minutes. What causes that gap, and which measure is less affected by it?  hints: ['The mean is computed by summing all values including the 178-min outlier. The median is the middle value of the sorted list, so it is not pulled by extreme values.', "When mean and median differ substantially, the distribution is skewed. For a 'typical value' question in a skewed dataset, the median is usually more informative."]  remediation→r01
  MEASURES: A:compute_and_interpret_descriptive_statistics_for_capstone_business_question(f1,f2)   anchors=['assessment:compute_and_interpret_descriptive_statistics_for_capstone_business_question']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · hands_on · Call describe() and choose the right statistic  [reward 4]
Hands-on practice — Given a DataFrame with a delivery_time column for one zone, call describe() on that column, then compare the mean and median and state in a comment which better represents a typical delivery.
QUESTION [code_exercise, stretch, grading=client] The DataFrame `df` is pre-loaded with the Ikeja zone's delivery_time values from `orders.csv`.

1. Call `describe()` on `df['delivery_time']` and print the result.
2. Assign `df['delivery_time'].mean()` to a variable named `mean_val`.
3. Assign `df['delivery_time'].median()` to a variable named `median_val`.
4. Add a comment explaining which statistic better represents a typical delivery and why.

The mean and median should differ visibly because of one extreme delivery time.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=["df['delivery_time'].describe()", "df['delivery_time'].mean()", "df['delivery_time'].median()", '# inline comments', 'print()', 'variable assignment with ='] blocked=3 items
  file solution.py [editable]:
import pandas as pd

# df is pre-loaded with Ikeja delivery_time values
df = pd.read_csv('orders.csv')
df = df[df['zone'] == 'Ikeja'][['delivery_time']].reset_index(drop=True)

# Step 1: call describe() on df['delivery_time'] and print
# print(...)

# Step 2: assign the mean to mean_val
# mean_val = ...

# Step 3: assign the median to median_val
# median_val = ...

# Step 4: add a comment — which statistic is better for 'typical delivery'?
# The ___ is the better measure because ...

  SOLUTION solution.py:
import pandas as pd

df = pd.read_csv('orders.csv')
df = df[df['zone'] == 'Ikeja'][['delivery_time']].reset_index(drop=True)

print(df['delivery_time'].describe())

mean_val = df['delivery_time'].mean()
median_val = df['delivery_time'].median()
# The median is the better measure because extreme values pull the mean upward

  test t_mean_val (value_equals, visible=True): {"expr":"mean_val","expected":52.0} | on-fail: mean_val should equal df['delivery_time'].mean(). Make sure you assign df['delivery_time'].mean() to mean_val.
  test t_median_val (value_equals, visible=True): {"expr":"median_val","expected":38.0} | on-fail: median_val should equal df['delivery_time'].median(). Make sure you assign df['delivery_time'].median() to median_val.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"c6c57afdbae806a15270bf577a6c3c9679670fa24822a5512dfd57a0e1fa2bc3","tests_passed":2}
  feedback✔: Well done. describe() shows the full summary; mean_val = 52.0 and median_val = 38.0 — the 14-minute gap shows the extreme 178-min delivery pulling the mean upward.  feedback✘: Make sure you assign df['delivery_time'].mean() to mean_val and df['delivery_time'].median() to median_val.  hints: ["df['delivery_time'].mean() returns the arithmetic mean; assign it to mean_val.", "df['delivery_time'].median() returns the middle value of the sorted series; assign it to median_val."]  remediation→r01
  MEASURES: A:apply_describe_to_capstone_series_or_dataframe_column(f1); A:select_mean_or_median_based_on_skew_and_business_question(f2)   anchors=['practice', 'assessment:apply_describe_to_capstone_series_or_dataframe_column', 'assessment:select_mean_or_median_based_on_skew_and_business_question']
  taught-before-tested: A.f1←s01; A.f2←s01

### s05 · explainer · Two patterns for multi-panel figures in matplotlib  [reward 3]
Dashboard & Visualisation — The findings now need a visualisation set a stakeholder can look at. matplotlib offers two patterns for placing several charts in one figure.
### Pattern 1: plt.subplots(2, 2) — a 2×2 grid
(mechanism) `fig, axs = plt.subplots(2, 2)` creates one Figure containing a 2×2 grid of Axes, so several charts can share one figure. Each axes is addressed by its row and column index — `axs[0, 0]`, `axs[0, 1]`, `axs[1, 0]`, `axs[1, 1]` — and plotted independently. In the capstone, four related delivery charts share one figure instead of appearing as four separate figures. ⟦B.f1 B:tb2⟧
### Pattern 2: plt.subplot(131/132/133) — a side-by-side row
(mechanism) `plt.subplot(131)`, `plt.subplot(132)`, and `plt.subplot(133)` each hold a different chart side by side in one figure, and `plt.suptitle()` adds one title over the whole figure. In the capstone, three delivery charts can sit side by side under one shared title instead of as three separate figures. ⟦B.f2 B:tb3⟧
[CODE python]
# Pattern 1: 2×2 grid
fig, axs = plt.subplots(2, 2)
axs[0, 0].bar(zones, avg_times)
axs[0, 0].set_title('Avg delivery time by zone')
axs[0, 1].bar(shifts, shift_avg)
axs[0, 1].set_title('Avg delivery time by shift')
axs[1, 0].bar(zones, order_counts)
axs[1, 0].set_title('Order count by zone')
axs[1, 1].hist(delivery_times, bins=10)
axs[1, 1].set_title('Distribution of delivery times')
plt.tight_layout()

# Pattern 2: side-by-side row
plt.subplot(131)
plt.bar(zones, avg_times)
plt.subplot(132)
plt.bar(shifts, shift_avg)
plt.subplot(133)
plt.hist(delivery_times, bins=10)
plt.suptitle('Delivery Performance -- Last Quarter')
plt.tight_layout()
  annotations: ['Pattern 1: subplots(2, 2) returns a 2-D array of axes; address each by [row, col].', 'Pattern 2: subplot(1, 3, n) places charts side by side; suptitle() adds one shared title.']

### s06 · explainer · Choosing a layout for the capstone figure  [reward 2]
Dashboard & Visualisation — Either layout turns several separate charts into one coherent figure the stakeholder summary can point to as a set.
(example) For the capstone, `fig, axs = plt.subplots(2, 2)` lays out four related charts — delivery time by zone, delivery time by shift, order count by zone, and the distribution of delivery times — in one 2×2 figure. Alternatively, `plt.subplot(131)`, `plt.subplot(132)`, `plt.subplot(133)` place three of those charts side by side in a single row, and `plt.suptitle('Delivery Performance -- Last Quarter')` puts one title over all three. ⟦B.f1 B.f2 B:tb4 B:tb5⟧

### s07 · video · Watch: arranging multiple charts in one figure with subplots  [reward 1]
Dashboard & Visualisation — This clip shows plt.subplots(2, 2) in action — each axes addressed by [row, col] and given its own title. Note: the clip uses toy curves, not delivery data, and does not cover plt.subplot(131)/plt.suptitle().
[VIDEO Arranging multiple charts in one figure with subplots] bridge-before: Watch how each axes is addressed by [row, col] index and given its own title. Note: the clip uses toy curves, not delivery data, and does not cover plt.subplot(131)/plt.suptitle(). | bridge-after: The clip shows f1 in action. The text covers f2 — the side-by-side plt.subplot(131/132/133) pattern and plt.suptitle() — which this clip omits entirely.
  - KFMs_ZZNgmo 0-386s facts=['f1'] label: plt.subplots(2, 2) — one figure, four axes | summary: The instructor defines a figure as the overall canvas and an axes object as a single plot within it. Calling plt.subplots(2, 2) returns a figure and a 2-D array of four axes objects. Each axes is then addressed by its row and column index — axs[0,0], axs[0,1], axs[1,0], axs[1,1] — and plotted independently with its own data, color, and title. plt.tight_layout() is called to prevent the four panels from overlapping. The demo uses simple power-of-x curves rather than a stakeholder dataset, but the layout mechanics are identical to what the capstone requires.

### s08 · check · Creating multi-panel figures: 2×2 grid and side-by-side row  [reward 2]
Quick check — Test your understanding of both plt.subplots(2, 2) and plt.subplot(131/132/133) + plt.suptitle().
QUESTION [choice, core, grading=client] Which pair of statements correctly describes the two multi-panel figure patterns taught in this tile?
  ✔ opt_correct: fig, axs = plt.subplots(2, 2) creates one Figure with a 2×2 grid of Axes; plt.subplot(131)/plt.subplot(132)/plt.subplot(133) creates three side-by-side panels in one figure, and plt.suptitle() adds a shared title over all of them.
      why: Correct. plt.subplots(2, 2) returns one Figure and a 2×2 array of Axes (axs[row, col]). plt.subplot(131/132/133) adds three panels to the current figure one at a time, and plt.suptitle() places a shared title above all panels.
  ✘ opt_subplots_suptitle: fig, axs = plt.subplots(2, 2) creates four separate figures; plt.suptitle() adds a title to the most recently created figure only.
      why: plt.subplots(2, 2) creates one Figure containing four Axes — not four separate figures. plt.suptitle() adds a title to the whole figure, not just the most recent one.
  ✘ opt_subplot_grid: plt.subplot(131) creates a 1×3 grid and returns all three Axes at once; plt.subplots(2, 2) creates four separate figures.
      why: plt.subplot(131) creates one panel (the first of a 1×3 layout) and returns that single Axes — not all three at once. You call plt.subplot(131), plt.subplot(132), plt.subplot(133) separately to add each panel. Also, plt.subplots(2, 2) creates one figure, not four.
  ✘ opt_suptitle_wrong: plt.suptitle() must be called before any plt.subplot() calls to take effect; fig, axs = plt.subplots(2, 2) creates a 2×2 grid but axs must be indexed as axs[0], axs[1], axs[2], axs[3].
      why: plt.suptitle() can be called at any point and applies to the whole figure. Also, axs from plt.subplots(2, 2) is a 2×2 array indexed as axs[row, col] — for example axs[0, 0] for the top-left panel.
  feedback✔: Right. subplots(2, 2) gives a 2×2 grid in one figure; subplot(131/132/133) adds panels one at a time; suptitle() titles the whole figure.  feedback✘: Remember: plt.subplots(2, 2) creates one figure with four Axes (not four figures). plt.subplot(131) adds one panel at a time. plt.suptitle() titles the whole figure.  hints: ['plt.subplots(nrows, ncols) returns (fig, axs) where axs is a 2-D array of Axes — all inside one Figure.', 'plt.subplot(131) means: in a 1-row, 3-column layout, activate panel 1. You call it three times (131, 132, 133) to set up three panels.']  remediation→r02
  MEASURES: B:create_2x2_subplot_grid_with_subplots(f1); B:create_side_by_side_subplots_with_suptitle(f2)   anchors=['assessment:create_2x2_subplot_grid_with_subplots', 'assessment:create_side_by_side_subplots_with_suptitle']
  taught-before-tested: B.f1←s05; B.f2←s05

### s09 · check · Selecting the right multi-panel layout for the capstone  [reward 2]
Quick check — Test your understanding of which multi-panel layout best fits the capstone findings.
QUESTION [choice, core, grading=client] You want to show three charts side by side in one figure: a bar chart of orders per zone, a histogram of delivery times, and a bar chart of mean delivery time per zone. Which layout code is most appropriate?
  ✔ opt_subplot_1x3: plt.subplot(131) / plt.subplot(132) / plt.subplot(133), then plt.suptitle('QuickRide Dashboard')
      why: Correct. plt.subplot(131/132/133) places three panels side by side in one figure, and plt.suptitle() adds a shared title — exactly the layout the task describes.
  ✘ opt_subplots_2x2: fig, axs = plt.subplots(2, 2), using axs[0,0], axs[0,1], axs[1,0] for the three charts
      why: plt.subplots(2, 2) creates a 2×2 grid with four panels. For three side-by-side charts you only need a 1×3 layout — either plt.subplot(131/132/133) or plt.subplots(1, 3).
  ✘ opt_three_figures: Create three separate figures with plt.figure() — one per chart — so each chart has its own window
      why: Three separate figures produce three separate windows, not one combined dashboard. To place charts side by side in one figure, use plt.subplot(131/132/133) or plt.subplots(1, 3).
  ✘ opt_subplots_1x3: fig, axs = plt.subplots(1, 3), using axs[0], axs[1], axs[2] for the three charts
      why: plt.subplots(1, 3) is also a valid way to create three side-by-side panels and is taught in this tile. However, this question specifically asks about the plt.subplot(131/132/133) pattern that is demonstrated in the capstone exercise, so that pattern is the expected answer here.
  feedback✔: Right. Both plt.subplot(131/132/133) and plt.subplots(1, 3) produce three side-by-side panels in one figure.  feedback✘: For three charts side by side in one figure, you need a 1×3 layout. plt.subplots(2, 2) gives four panels; three separate figures give three windows, not one dashboard.  hints: ['plt.subplot(131) means: 1 row, 3 columns, panel 1. Calling it three times (131, 132, 133) fills a 1×3 row.', 'plt.subplots(1, 3) also creates a 1-row, 3-column layout and returns axs as a 1-D array of three Axes.']  remediation→r02
  MEASURES: B:select_appropriate_multi_panel_layout_for_capstone_findings(f1,f2)   anchors=['assessment:select_appropriate_multi_panel_layout_for_capstone_findings']
  taught-before-tested: B.f1←s05; B.f2←s05

### s10 · hands_on · Build the capstone multi-panel figure  [reward 4]
Hands-on practice — Using the capstone delivery dataset, build a multi-panel figure that places at least three related charts together in one figure and adds a single shared title over all panels.
QUESTION [code_exercise, stretch, grading=client] The DataFrame `df` is loaded from `orders.csv`. Three data summaries are prepared for you: `zone_counts`, `delivery_times`, and `zone_means`.

Build a single figure with three side-by-side panels:
- Call `plt.subplot(131)` then use the current axes to create a bar chart
- Call `plt.subplot(132)` then create a histogram
- Call `plt.subplot(133)` then create another bar chart

Add titles to each panel and call `plt.suptitle('QuickRide Capstone Dashboard')` and `plt.tight_layout()` at the end.
  runtime={'kind': 'chart_renderer', 'version': '0.29.5', 'packages': ['pandas', 'matplotlib', 'seaborn']} constraints.allowed=['plt.subplots(nrows, ncols)', 'axs[row, col].plot(...)', 'axs[row, col].bar(...)', 'axs[row, col].hist(...)', 'axs[row, col].set_title(...)', 'plt.subplot(131)', 'plt.subplot(132)', 'plt.subplot(133)', 'plt.suptitle(...)', 'plt.tight_layout()', 'plt.show()', 'ax.set_xlabel(...)', 'ax.set_ylabel(...)', 'sns.barplot(..., ax=ax)', 'sns.histplot(..., ax=ax)', 'sns.boxplot(..., ax=ax)', "df['column'].value_counts()", 'df.groupby(...).mean()', 'import matplotlib.pyplot as plt', 'import seaborn as sns'] blocked=0 items
  file dashboard.py [editable]:
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('orders.csv')

# TODO: Create first panel with plt.subplot(131), then bar chart
# TODO: Create second panel with plt.subplot(132), then histogram
# TODO: Create third panel with plt.subplot(133), then bar chart
# TODO: Add suptitle and tight_layout

  SOLUTION dashboard.py:
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('orders.csv')

ax = plt.subplot(131)
df['zone'].value_counts().plot.bar(ax=ax)
ax.set_title('Orders per Zone')

ax = plt.subplot(132)
ax.hist(df['delivery_time'])
ax.set_title('Delivery Time Distribution')

ax = plt.subplot(133)
df.groupby('zone')['delivery_time'].mean().plot.bar(ax=ax)
ax.set_title('Mean Delivery Time per Zone')

plt.suptitle('QuickRide Capstone Dashboard')
plt.tight_layout()

  test t_figure_structure (figure_equals, visible=True): {"expected":{"n_axes":3}} | on-fail: The figure should contain exactly 3 axes (one per panel). Make sure you call plt.subplot(131), plt.subplot(132), and plt.subplot(133).
  test t_panel3_title (axes_property, visible=True): {"property":"title","expected":"Mean Delivery Time per Zone","axes":2} | on-fail: Panel 3 (axes index 2) should have the title 'Mean Delivery Time per Zone'.
  test t_zone_means_bars (plotted_data_equals, visible=True): {"chart":"bar","field":"heights","axes":2,"sorted":false,"tolerance":0.0001,"expected":[52.0,30.285714285714285,25.714285714285715,33.75]} | on-fail: Panel 3 bar heights should equal the mean delivery_time per zone from the data. Make sure you use df.groupby('zone')['delivery_time'].mean() for the bar heights.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"40fad29470ec3d2c90661bdd95160e2af3d579603af70eaad2feb6ba9731fb9d","tests_passed":3}
  feedback✔: Excellent. Your dashboard shows three panels in one figure with a shared title — orders per zone, delivery time distribution, and mean delivery time per zone.  feedback✘: Check that you have three plt.subplot() calls (131, 132, 133), each with a bar or hist chart and a title, and that plt.suptitle('QuickRide Capstone Dashboard') is called.  hints: ['Call plt.subplot(131) before drawing the first chart, plt.subplot(132) before the second, and plt.subplot(133) before the third.', "For Panel 3: zone_means = df.groupby('zone')['delivery_time'].mean(); plt.bar(zone_means.index, zone_means.values)"]  remediation→r03
  MEASURES: B:select_appropriate_multi_panel_layout_for_capstone_findings(f1,f2)   anchors=['practice']
  taught-before-tested: B.f1←s05; B.f2←s05

### s11 · recap · Statistics and visualisation: the capstone findings are ready  [reward 2]
Tile recap — You've computed the descriptive statistics that answer the business question and assembled them into a multi-panel figure the stakeholder summary can reference.
(takeaway) describe() gives the full summary for a delivery_time column in one call; choosing between mean and median depends on whether extreme observations are skewing the data. For the capstone's business question — which zones miss the delivery target and by how much — the median is the more useful measure. Either `plt.subplots(2, 2)` or `plt.subplot(131/132/133)` + `plt.suptitle()` turns several separate charts into one coherent figure. ⟦A.f1 A.f2 B.f1 B.f2 A:tb5 B:tb5⟧
[UP NEXT] Up next: Independent execution and narrated delivery: In the next tile you'll execute the full capstone workflow independently — without step-by-step guidance — and produce a narrated stakeholder summary of your findings.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · describe() output and choosing mean vs median — The check asked about interpreting describe() output and selecting the right statistic. Here's the key contrast.
(mechanism) describe() computes count, mean, std, min, 25th percentile, 50th percentile (the median), 75th percentile, and max for a Series or DataFrame column. The 50% row in describe()'s output is the median. In the capstone, running describe() on Ikeja's `delivery_time` column returns a mean of 52 minutes and a median of 38 minutes. (In the full dataset, beyond this sample, a handful of deliveries took over three hours, pulling the mean to 52 minutes while the median stays at 38 minutes.) ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) The mean is pulled upward by extreme observations; the median is not. When a few deliveries took over three hours, the mean rises to 52 minutes even though most deliveries were around 38 minutes. (In the full dataset, beyond this sample, a handful of deliveries took over three hours, pulling the mean to 52 minutes while the median stays at 38 minutes.) For the business question — which zones miss the target and by how much — the median (38 minutes) better represents a typical delivery than the mean (52 minutes). ⟦A.f2 A:tb3 A:tb4⟧
### r02 · Both multi-panel patterns: subplots(2,2) and subplot(131/132/133) — The check asked about both plt.subplots(2, 2) and plt.subplot(131/132/133). Here are both patterns.
(mechanism) `fig, axs = plt.subplots(2, 2)` returns one Figure and a 2-D NumPy array of four Axes objects. Each axes is addressed by its row and column index: `axs[0, 0]` is the top-left, `axs[0, 1]` is the top-right, `axs[1, 0]` is the bottom-left, and `axs[1, 1]` is the bottom-right. You call plotting methods on each axes independently — `axs[0, 0].bar(...)`, `axs[0, 1].hist(...)` — and `plt.tight_layout()` prevents the panels from overlapping. ⟦B.f1 B:tb2 B:tb4⟧
(misconception) A common mistake is calling `plt.subplots(2, 2)` but then plotting with `plt.bar(...)` instead of `axs[row, col].bar(...)`. Using the global `plt` functions after subplots() plots into the last active axes, not the one you intend. Always address the specific axes object by index. ⟦B.f1 B:tb2⟧
(mechanism) `plt.subplot(131)` means: 1 row, 3 columns, activate panel 1. `plt.subplot(132)` activates panel 2, and `plt.subplot(133)` activates panel 3. Each call makes that panel current, so the next plotting call draws into it. `plt.suptitle("Delivery Performance -- Last Quarter")` adds one title above all three panels. ⟦B.f2 B:tb3 B:tb4⟧
### r03 · Selecting the right multi-panel layout for the capstone findings — The check asked which layout best fits the capstone findings. Here is how to choose.
(mechanism) `plt.subplots(2, 2)` creates a 2×2 grid — use it when you have four related charts to show together. `plt.subplot(131/132/133)` creates a 1×3 side-by-side row — use it when three charts belong together in a single row. Both patterns produce one figure with multiple axes; the choice depends on how many charts you have and how they relate. ⟦B.f1 B.f2 B:tb2 B:tb3 B:tb4⟧
(example) For the capstone, four delivery charts (by zone, by shift, order count, distribution) fit naturally into a 2×2 grid with `plt.subplots(2, 2)`. Three of those charts can instead sit side by side with `plt.subplot(131/132/133)` and a shared title from `plt.suptitle("Delivery Performance -- Last Quarter")`. Either layout turns separate charts into one coherent figure. ⟦B.f1 B.f2 B:tb4⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: matplotlib or seaborn plotting calls
· constraints.blocked_syntax: any dashboard or visualization library