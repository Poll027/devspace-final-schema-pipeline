# EVALUATOR PACKET — Integrating SQL, Spreadsheets, and pandas (tile_capstone_integrate_tools_model)
Tile summary: Apply already-learned SQL, spreadsheet, and pandas skills to the QuickRide capstone project: retrieve last quarter's orders with a multi-clause SELECT, summarise the delivery sheet with a PivotTable and COUNTIFS, clean and aggregate orders in pandas, and model the two-table relationship with correct primary and foreign keys.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = capstone.integrate_sql — Integrating SQL querying into an end-to-end project
B = capstone.integrate_spreadsheet — Integrating spreadsheet analysis into an end-to-end project
C = capstone.integrate_python_pandas — Integrating Python/pandas cleaning and analysis into an end-to-end project
D = capstone.building_data_model — Building a data model for the capstone dataset

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO Building a JOIN + WHERE + GROUP BY query from scratch in a single SELECT] bridge-before:  | bridge-after: 

### s04 · check · Where does the INNER JOIN go?  [reward 2]
Quick check — Test your understanding of where a JOIN fits inside a SELECT statement.

### s05 · hands_on · Write the capstone retrieval query  [reward 4]
Hands-on practice — Write the SQL query that retrieves last quarter's QuickRide orders, joining the orders and drivers tables, filtering to the correct date range, and grouping by zone.

### s06 · explainer · PivotTable and COUNTIFS on the capstone delivery sheet  [reward 3]
Spreadsheet Integration — The capstone's spreadsheet step pairs each order's zone and delivery_time with the driver's shift. A PivotTable and COUNTIFS turn that sheet into a zone-by-shift summary.
### Building a PivotTable from the delivery sheet
(mechanism) A PivotTable is built by selecting the data range and inserting a PivotTable, then adding fields: non-numeric fields default to Rows, date/time fields to Columns, and numeric fields to Values. Fields can be dragged between areas to rearrange the summary. In the capstone, `zone` and `shift` (both non-numeric) default to Rows, while `delivery_time` (numeric) goes to Values. ⟦B.f1 B:tb2⟧
(mechanism) COUNTIFS(criteria_range1, criteria1, [criteria_range2, criteria2]…) applies criteria across one or more ranges and counts the cells where **all** criteria are met. In the capstone, `COUNTIFS(zone_range, "Ikeja", delivery_time_range, ">45")` counts how many Ikeja deliveries exceeded 45 minutes. ⟦B.f2 B:tb3⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","block_id":"tile_capstone_integrate_tools_model.s06.b4","asset_ref":{"asset_id":"ds_capstone_delivery_sheet"},"sheet_name":"DeliverySheet","range":"A1:C10","show_formula_bar":true,"cells":[{"ref":"E1","note":"PivotTable: zone (Rows) × shift (Columns), Average delivery_time (Values)"},{"ref":"E8","formula":"=COUNTIFS(A2:A37,\"Ikeja\",C2:C37,\">45\")","note":"Count Ikeja deliveries over 45 minutes"}],"annotations":[{"target":"A1:C1","text":"Source data: zone, shift, delivery_time"},{"target":"E1","text":"PivotTable output: zone × shift grid, Average delivery_time per cell"},{"target":"E8","text":"COUNTIFS: counts rows where zone=Ikeja AND delivery_time>45"}],"lineage":{"concept_ids":["capstone.integrate_spreadsheet"],"fact_ids":["capstone.integrate_spreadsheet#f1","capstone.integrate_spreadsheet#f2"],"teaching_block_ids":["capstone.integrate_spreadsheet#tb2","capstone.integrate_spreadsheet#tb3"],"anchors":["capstone.integrate_spreadsheet#visual"]}}

### s07 · explainer · Rearranging the PivotTable and applying COUNTIFS  [reward 2]
Spreadsheet Integration — Dragging shift from Rows to Columns turns the PivotTable into a zone-by-shift grid. COUNTIFS then counts deliveries that meet two criteria at once.
(example) For the capstone delivery sheet, selecting the data range and inserting a PivotTable places `zone` and `shift` in Rows by default and `delivery_time` in Values. Dragging `shift` from Rows to Columns rearranges the summary into a zone-by-shift grid; changing the Values summary function to Average makes each cell an average delivery time. ⟦B.f1 B:tb4⟧
(example) Separately, `COUNTIFS(zone_range, "Ikeja", delivery_time_range, ">45")` counts how many Ikeja deliveries in the sheet took more than 45 minutes — both criteria (zone and time threshold) must be met at once. The PivotTable and COUNTIFS skills already learned are now run on this project's own roster and delivery data. ⟦B.f2 B:tb4 B:tb5⟧

### s08 · video · Watch: inserting a PivotTable and arranging fields  [reward 1]
Spreadsheet Integration — This clip shows how non-numeric fields land in Rows automatically and a numeric field jumps to Values. Note: the clip uses an advertising dataset, not the capstone's delivery sheet.
[VIDEO Building a PivotTable: selecting a range, inserting, and dragging fields] bridge-before:  | bridge-after: 

### s09 · check · Applying COUNTIFS with multiple criteria  [reward 2]
Quick check — Test your understanding of how COUNTIFS handles more than one criterion.

### s10 · check · Executing the capstone spreadsheet analysis step  [reward 2]
Quick check — Test your understanding of how PivotTable and COUNTIFS work together to complete the capstone spreadsheet analysis.

### s11 · hands_on · Build the capstone PivotTable  [reward 4]
Hands-on practice — Using the capstone delivery sheet, build a zone-by-shift PivotTable showing average delivery time per cell.

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

### s13 · explainer · The same skills, applied to the capstone's own data  [reward 2]
Python / pandas Integration — The isna()/dropna()/fillna() and groupby() skills already learned are now run on the capstone's retrieved orders instead of a practice dataset.
(example) On the capstone's retrieved orders, `orders['delivery_time'].isna()` flags rows with no delivery time; dropna() removes them. Then `orders.groupby('zone')['delivery_time'].mean()` splits the cleaned orders by zone, computes the mean delivery time within each zone, and combines the per-zone results — an aggregation, since each zone group is reduced to a single number. ⟦C.f1 C.f2 C:tb4 C:tb5⟧

### s14 · check · Cleaning and aggregating the capstone dataset end-to-end  [reward 2]
Quick check — Test your understanding of how isna()/dropna() and groupby().mean() work together to clean and summarise the capstone orders.

### s15 · hands_on · Detect missing values and compute per-zone means  [reward 4]
Hands-on practice — Given a small orders DataFrame with zone and delivery_time columns (some NaN), detect the missing delivery times, remove those rows, then compute the mean delivery time per zone.

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

### s19 · hands_on · Match columns to their roles in the capstone data model  [reward 4]
Hands-on practice — Match each column from the Drivers and Orders tables to its role: primary key of Drivers, primary key of Orders, or foreign key in Orders referencing Drivers. Then identify which table is on the 'one' side and which is on the 'many' side.

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
· cells.formula: =COUNTIFS(A2:A37,"Ikeja",C2:C37,">45")

=========

# EVALUATOR PACKET — Descriptive Statistics and Dashboard (tile_capstone_stats_dashboard)
Tile summary: Apply pandas describe() to the capstone delivery data, choose between mean and median based on skew and the business question, then build a multi-panel matplotlib figure using either plt.subplots(2, 2) or plt.subplot(131/132/133) + plt.suptitle().
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = capstone.applying_descriptive_statistics — Applying descriptive statistics to capstone findings
B = capstone.building_dashboard_or_viz — Building a polished matplotlib/seaborn visualization set for the capstone

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s02 · explainer · Choosing mean or median for the business question  [reward 2]
Descriptive Statistics — describe() gives the full summary; deciding which statistic actually answers the business question depends on whether extreme values are skewing that particular column.
(example) Running describe() on Ikeja's `delivery_time` column returns a mean of 52 minutes and a median of 38 minutes. A handful of deliveries in that zone took over three hours — a stalled vehicle, a wrong address — and the mean is pulled up by those extreme observations, while the median stays at 38 minutes. ⟦A.f1 A.f2 A:tb4⟧
(mechanism) The capstone's business question is which zones miss the delivery-time target and by how much — which calls for judging a **typical** delivery against that target, not one skewed by a few rare extremes. So the median is the more useful number here. describe() gives both; the analyst's job is to choose the one that answers the question. ⟦A.f2 A:tb4 A:tb5⟧

### s03 · check · Mean vs median for a skewed distribution  [reward 2]
Quick check — Test your understanding of when to use the median instead of the mean.

### s04 · hands_on · Call describe() and choose the right statistic  [reward 4]
Hands-on practice — Given a DataFrame with a delivery_time column for one zone, call describe() on that column, then compare the mean and median and state in a comment which better represents a typical delivery.

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
[VIDEO Arranging multiple charts in one figure with subplots] bridge-before:  | bridge-after: 

### s08 · check · Creating multi-panel figures: 2×2 grid and side-by-side row  [reward 2]
Quick check — Test your understanding of both plt.subplots(2, 2) and plt.subplot(131/132/133) + plt.suptitle().

### s09 · check · Selecting the right multi-panel layout for the capstone  [reward 2]
Quick check — Test your understanding of which multi-panel layout best fits the capstone findings.

### s10 · hands_on · Build the capstone multi-panel figure  [reward 4]
Hands-on practice — Using the capstone delivery dataset, build a multi-panel figure that places at least three related charts together in one figure and adds a single shared title over all panels.

### s11 · recap · Statistics and visualisation: the capstone findings are ready  [reward 2]
Tile recap — You've computed the descriptive statistics that answer the business question and assembled them into a multi-panel figure the stakeholder summary can reference.
(takeaway) describe() gives the full summary for a delivery_time column in one call; choosing between mean and median depends on whether extreme observations are skewing the data. For the capstone's business question — which zones miss the delivery target and by how much — the median is the more useful measure. Either `plt.subplots(2, 2)` or `plt.subplot(131/132/133)` + `plt.suptitle()` turns several separate charts into one coherent figure. ⟦A.f1 A.f2 B.f1 B.f2 A:tb5 B:tb5⟧
[UP NEXT] Up next: Independent execution and narrated delivery: In the next tile you'll execute the full capstone workflow independently — without step-by-step guidance — and produce a narrated stakeholder summary of your findings.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · describe() output and choosing mean vs median — The check asked about interpreting describe() output and selecting the right statistic. Here's the key contrast.
(mechanism) describe() computes count, mean, std, min, 25th percentile, 50th percentile (the median), 75th percentile, and max for a Series or DataFrame column. The 50% row in describe()'s output is the median. In the capstone, running describe() on Ikeja's `delivery_time` column returns a mean of 52 minutes and a median of 38 minutes. ⟦A.f1 A:tb2 A:tb4⟧
(mechanism) The mean is pulled upward by extreme observations; the median is not. When a few deliveries took over three hours, the mean rises to 52 minutes even though most deliveries were around 38 minutes. For the business question — which zones miss the target and by how much — the median (38 minutes) better represents a typical delivery than the mean (52 minutes). ⟦A.f2 A:tb3 A:tb4⟧
### r02 · Both multi-panel patterns: subplots(2,2) and subplot(131/132/133) — The check asked about both plt.subplots(2, 2) and plt.subplot(131/132/133). Here are both patterns.
(mechanism) `fig, axs = plt.subplots(2, 2)` returns one Figure and a 2-D NumPy array of four Axes objects. Each axes is addressed by its row and column index: `axs[0, 0]` is the top-left, `axs[0, 1]` is the top-right, `axs[1, 0]` is the bottom-left, and `axs[1, 1]` is the bottom-right. You call plotting methods on each axes independently — `axs[0, 0].bar(...)`, `axs[0, 1].hist(...)` — and `plt.tight_layout()` prevents the panels from overlapping. ⟦B.f1 B:tb2 B:tb4⟧
(misconception) A common mistake is calling `plt.subplots(2, 2)` but then plotting with `plt.bar(...)` instead of `axs[row, col].bar(...)`. Using the global `plt` functions after subplots() plots into the last active axes, not the one you intend. Always address the specific axes object by index. ⟦B.f1 B:tb2⟧
(mechanism) `plt.subplot(131)` means: 1 row, 3 columns, activate panel 1. `plt.subplot(132)` activates panel 2, and `plt.subplot(133)` activates panel 3. Each call makes that panel current, so the next plotting call draws into it. `plt.suptitle("Delivery Performance -- Last Quarter")` adds one title above all three panels. ⟦B.f2 B:tb3 B:tb4⟧
### r03 · Selecting the right multi-panel layout for the capstone findings — The check asked which layout best fits the capstone findings. Here is how to choose.
(mechanism) `plt.subplots(2, 2)` creates a 2×2 grid — use it when you have four related charts to show together. `plt.subplot(131/132/133)` creates a 1×3 side-by-side row — use it when three charts belong together in a single row. Both patterns produce one figure with multiple axes; the choice depends on how many charts you have and how they relate. ⟦B.f1 B.f2 B:tb2 B:tb3 B:tb4⟧
(example) For the capstone, four delivery charts (by zone, by shift, order count, distribution) fit naturally into a 2×2 grid with `plt.subplots(2, 2)`. Three of those charts can instead sit side by side with `plt.subplot(131/132/133)` and a shared title from `plt.suptitle("Delivery Performance -- Last Quarter")`. Either layout turns separate charts into one coherent figure. ⟦B.f1 B.f2 B:tb4⟧