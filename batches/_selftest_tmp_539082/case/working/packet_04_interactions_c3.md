# EVALUATOR PACKET — Concatenating and Merging DataFrames (tile_pandas_concat_merge)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.concat_stacking — Concat stacking
B = pandas.merge_join — Merge join

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (pandas.concat_stacking)   objective: Stack multiple DataFrames with the same structure along rows or columns using concat.
A.f1: pd.concat() concatenates multiple Series or DataFrame objects along an axis.   [sources: pandas_docs_merging#concat]
A.f2: By default, pd.concat() stacks the given DataFrames row-wise, appending each one's rows below the previous, producing one combined DataFrame when they share the same columns.   [sources: pandas_docs_merging#concat]
A.f3: pd.concat() takes an axis parameter: by default (no axis argument), it stacks the objects row-wise, while axis=1 places them side by side as columns.   [sources: pandas_docs_merging#concat, pandas_docs_merging#joining-logic-of-the-resulting-axis]
note: Skip the optional join-parameter and ignore_index facts -- not required.
PRACTICE ANCHOR (live_code): Concatenate three monthly sales DataFrames with identical columns into one combined yearly DataFrame.  SUCCESS: The printed result has every row of the first table, then the second, then the third, with the shared columns unchanged.
ASSESSMENT ANCHOR: stack_dataframes_row_wise facts=['f1', 'f2']
ASSESSMENT ANCHOR: choose_concat_axis facts=['f3']

## SOURCE FACTS — B (pandas.merge_join)   objective: Combine two related DataFrames on a shared key column using merge, with the correct join type.
B.f1: merge() combines two DataFrames by matching values in a shared key column, which can be specified with the on parameter.   [sources: pandas_docs_merging#merge]
B.f2: The how parameter to merge() controls which keys are kept in the result; how='inner' (the default) keeps only the key values present in both DataFrames.   [sources: pandas_docs_merging#merge, pandas_docs_merge_api]
B.f3: If a key value does not appear in one of the two DataFrames being merged, the corresponding values contributed by that DataFrame in the joined result are NA.   [sources: pandas_docs_merging#merge]
B.f4: The how parameter also accepts 'left' (keep all keys from the left DataFrame only), 'right' (keep all keys from the right DataFrame only), and 'outer' (keep the union of keys from both DataFrames).   [sources: pandas_docs_merging#merge]
note: TOC conflict: the concept's own objective frames merge as mirroring SQL joins, but SQL hasn't been taught yet and isn't in this concept's allowed knowledge -- this text explains merge purely in pandas terms, without comparing it to SQL.
note: Known TOC conflict (see orchestrator_notes): the objective mirrors SQL joins, but SQL is not yet taught, so neither the teaching text nor the anchors compare merge to SQL.
PRACTICE ANCHOR (live_code): Merge an orders DataFrame with a customers DataFrame on customer_id using an inner merge.  SUCCESS: The printed result has one row per order whose customer_id also appears in customers, with the customer columns attached, and no unmatched order rows.
ASSESSMENT ANCHOR: merge_on_shared_key facts=['f1']
ASSESSMENT ANCHOR: predict_inner_merge_result facts=['f2']
ASSESSMENT ANCHOR: choose_how_join_type facts=['f4']
ASSESSMENT ANCHOR: explain_na_for_unmatched_keys facts=['f3']

## DATA ASSETS USED
ds_customers: SwiftDrop Customers — columns: customer_id(identifier,digits-as-label), customer_name(categorical), segment(categorical), signup_date(datetime)
   [301,"Ngozi Eze","Individual","2023-01-10"]
   [302,"Emeka Obi","Business","2023-02-14"]
   [303,"Fatima Musa","Individual","2023-03-05"]
   [304,"Tunde Bakare","Business","2023-04-20"]
   [305,"Amaka Nwosu","Individual","2023-05-11"]
   [306,"Yusuf Garba","Business","2023-06-01"]
   [307,"Chisom Ike","Individual","2023-07-18"]
   [308,"Bisi Adewale","Business","2023-08-09"]
ds_feb_orders: February Orders — columns: order_id(identifier,digits-as-label), city(categorical), courier(categorical), delivery_time_minutes(numerical), order_value(numerical)
   [2006,"Lagos","Ada",20,2700]
   [2007,"Abuja","Bayo",28,4000]
   [2008,"Kano","Chidi",24,1600]
   [2009,"Lagos","Ada",35,5100]
   [2010,"Kano","Chidi",21,2000]
ds_jan_orders: January Orders — columns: order_id(identifier,digits-as-label), city(categorical), courier(categorical), delivery_time_minutes(numerical), order_value(numerical)
   [2001,"Lagos","Ada",18,2500]
   [2002,"Abuja","Bayo",22,3100]
   [2003,"Kano","Chidi",26,1800]
   [2004,"Lagos","Ada",31,2900]
   [2005,"Abuja","Bayo",19,3400]
ds_mar_orders: March Orders — columns: order_id(identifier,digits-as-label), city(categorical), courier(categorical), delivery_time_minutes(numerical), order_value(numerical)
   [2011,"Lagos","Ada",22,2600]
   [2012,"Abuja","Bayo",30,3700]
   [2013,"Kano","Chidi",27,1900]
   [2014,"Lagos","Ada",80,5500]
   [2015,"Abuja","Bayo",23,3200]
ds_orders: SwiftDrop Orders — columns: order_id(identifier,digits-as-label), city(categorical), city_code(categorical), courier(categorical), driver_id(identifier,digits-as-label), customer_id(identifier,digits-as-label), pickup_date(datetime), delivery_time_minutes(numerical), distance_km(numerical), order_value(numerical)
   [1001,"Lagos","LOS","Ada",201,301,"2024-03-14",18,4.2,2500]
   [1002,"Abuja","ABJ","Bayo",202,302,"2024-03-14",20,6.1,3100]
   [1003,"Kano","KAN","Chidi",203,303,"2024-03-15",22,5.5,1800]
   [1004,"Lagos","LOS","Ada",201,304,"2024-03-15",22,3.8,2200]
   [1005,"Abuja","ABJ","Bayo",202,305,"2024-03-16",26,7.3,4000]
   [1006,"Kano","KAN","Chidi",203,306,"2024-03-16",28,8.0,1500]
   [1007,"Lagos","LOS","Ada",201,307,"2024-03-17",80,12.4,5500]
   [1008,"Abuja","ABJ","Bayo",202,308,"2024-03-17",31,9.2,3800]
   variant orders_messy: 5 ops; planted: iss_city_case_1004(inconsistent_category); iss_city_case_1007(inconsistent_category); iss_dist_string(wrong_type); iss_missing_dt(missing_value); iss_duplicate_1003(duplicate_row)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Aggregate functions (COUNT, SUM, AVG, MIN, MAX); CASE expressions for conditional logic in queries; COALESCE for fallback values and NULL handling; Common SQL string functions for cleaning text; DISTINCT for de-duplication; Entities and tables as models of real-world objects; Exporting cleaned data (to_csv); GROUP BY grouping semantics; Grouping and aggregation (groupby); HAVING clause for filtering aggregated groups; Limiting results (LIMIT/OFFSET); Logical operators (AND, OR, NOT) in filtering; Melt reshaping; Merge join; NULL handling (IS NULL / IS NOT NULL); Pivot table reshaping; Primary keys; Relational database and table structure basics; SELECT statement fundamentals (columns, aliasing); SQL date/time extraction and arithmetic; SQL formatting/naming conventions per style guide; SQL type casting and conversion; Sorting results with ORDER BY (ASC/DESC); Table and column aliasing for readability; UNION and UNION ALL for stacking compatible query results; WHERE clause filtering and comparison operators

## LESSON, in learner order

### s01 · explainer · Stacking DataFrames with pd.concat()  [reward 3]
Concatenation — January, February, and March orders each live in their own table. pd.concat() glues them into one combined DataFrame in a single call.
(definition) `pd.concat()` concatenates multiple Series or DataFrame objects along an axis. Pass a list of DataFrames: `pd.concat([jan_orders, feb_orders, mar_orders])`. By default it stacks them **row-wise**, appending each one's rows below the previous — so the result has every January row, then every February row, then every March row, one after another. ⟦A.f1 A.f2 A:tb2 A:tb3⟧
(mechanism) `pd.concat()` takes an `axis` parameter. By default (no `axis` argument) it stacks row-wise. Passing `axis=1` places the DataFrames side by side as columns: `pd.concat([orders_basic_info, orders_extra_columns], axis=1)` lines the two tables up next to each other, column by column. ⟦A.f3 A:tb4⟧
[BEFORE_AFTER] Three 5-row monthly DataFrames stacked into one 15-row DataFrame using pd.concat() with default axis=0.
  before:
[TABLE ds_jan_orders cols=['order_id', 'city', 'courier', 'delivery_time_minutes', 'order_value'] ] caption: jan_orders — 5 rows; feb_orders and mar_orders have the same columns
  after:
[CODE python]
all_orders = pd.concat([jan_orders, feb_orders, mar_orders])
print(all_orders.shape)  # (15, 5)
print(all_orders.head())
  annotations: ['Three same-column tables stacked row-wise', '15 rows = 5 Jan + 5 Feb + 5 Mar']

### s02 · video · Concatenating DataFrames row-wise and column-wise
See it in action — Watch pd.concat() stack monthly tables and see how axis=1 changes the direction.
[VIDEO Stacking tables with concat] bridge-before: Watch the default top-to-bottom stacking, then axis=1 placing tables side by side. ignore_index=True is an extra here; it only renumbers the rows. | bridge-after: axis=1 lines rows up by position, so it is safe only when the row orders already match. Matching rows by a key value is a different job, taught later.
  - bIiXKpZaJ3U 6-194s facts=['f1', 'f2', 'f3'] label: pd.concat to stack monthly tables, then axis=1 to place tables side by side | summary: Combines three monthly sales DataFrames into a quarter table by passing them as a list to pd.concat, which stacks them one below the other; ignore_index=True renumbers the index into one continuous run. A second example puts a customers table and a regions table side by side with axis=1, so each customer gains a region in the same row. The presenter notes this works when the row order already lines up.

### s03 · check · Choosing the concat axis  [reward 2]
Quick check — Confirm you know what axis=1 does when passed to pd.concat().
QUESTION [choice, core, grading=client] You have three DataFrames with the same columns and want to stack them row-wise (one below the other). Which `pd.concat()` call is correct?
  ✘ opt_a: `pd.concat([df1, df2, df3])`
      why: This is correct, but not the only correct answer. `axis=0` is the default, so `pd.concat([df1, df2, df3])` and `pd.concat([df1, df2, df3], axis=0)` are equivalent.
  ✘ opt_b: `pd.concat([df1, df2, df3], axis=1)`
      why: `axis=1` places the DataFrames side by side as columns, not row-wise. For row-wise stacking, use the default (no axis argument) or `axis=0`.
  ✘ opt_c: `pd.concat([df1, df2, df3], axis=0)`
      why: This is correct, but not the only correct answer. `axis=0` is the default, so `pd.concat([df1, df2, df3])` and `pd.concat([df1, df2, df3], axis=0)` are equivalent.
  ✔ opt_d: Both A and C are correct
      why: Correct. By default, `pd.concat()` stacks row-wise (axis=0), so both calls produce the same result.
  feedback✔: Exactly right. The default axis is 0 (row-wise stacking).  feedback✘: Not quite. Review the default axis for `pd.concat()`.  hints: ['Think about what the default axis is for `pd.concat()` when no axis argument is given.']  remediation→r01
  MEASURES: A:choose_concat_axis(f3)   anchors=['assessment:choose_concat_axis']
  taught-before-tested: A.f3←s01

### s04 · hands_on · Stack the monthly order tables into one DataFrame  [reward 5]
Practice — Use pd.concat() to combine jan_orders, feb_orders, and mar_orders row-wise.
QUESTION [code_exercise, core, grading=client] You have three monthly order tables: `jan_orders`, `feb_orders`, `mar_orders`, all with the same columns. Use `pd.concat()` to stack them row-wise into one DataFrame, then print the result.

Use only `pd.concat([df1, df2, df3])`, `axis=1`, and `print()`.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=['pd.concat([df1, df2, df3])', 'axis=1', 'print()'] blocked=4 items
  file solution.py [editable]:
import pandas as pd

jan_orders = pd.read_csv('jan_orders.csv')
feb_orders = pd.read_csv('feb_orders.csv')
mar_orders = pd.read_csv('mar_orders.csv')

frames = [jan_orders, feb_orders, mar_orders]

# Concatenate the three DataFrames using pd.concat
# Store in result

print(result)

  SOLUTION solution.py:
import pandas as pd

jan_orders = pd.read_csv('jan_orders.csv')
feb_orders = pd.read_csv('feb_orders.csv')
mar_orders = pd.read_csv('mar_orders.csv')

frames = [jan_orders, feb_orders, mar_orders]

result = pd.concat(frames)

print(result)

  test t1 (dataframe_equals, visible=True): {"expr":"pd.concat([jan_orders, feb_orders, mar_orders], ignore_index=True)","expected":{"columns":["order_id","city","courier","delivery_time_minutes","order_value"],"rows":[[2001,"Lagos","Ada",18,2500],[2002,"Abuja","Bayo",22,3100],[2003,"Kano","Chidi",26,1800],[2004,"Lagos","Ada",31,2900],[2005,"Abuja","Bayo",19,3400],[2006,"Lagos","Ada",20,2700],[2007,"Abuja","Bayo",28,4000],[2008,"Kano","Chidi",24,1600],[2009,"Lagos","Ada",35,5100],[2010,"Kano","Chidi",21,2000],[2011,"Lagos","Ada",22,2600], | on-fail: The result should have all rows from jan, feb, and mar orders stacked row-wise.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"743a52eea0e6096f7d37b5fb6d5ac3c71421ce3bcf02860f742d40b59fa36230","tests_passed":1}
  feedback✔: Perfect! You stacked the three tables row-wise.  feedback✘: Not quite. Make sure you use `pd.concat([jan_orders, feb_orders, mar_orders])` to stack them.  hints: ['Use `pd.concat([jan_orders, feb_orders, mar_orders])` to stack the tables row-wise.']  remediation→r01
  MEASURES: A:stack_dataframes_row_wise(f1,f2); A:choose_concat_axis(f3)   anchors=['practice', 'assessment:stack_dataframes_row_wise', 'assessment:choose_concat_axis']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s05 · explainer · Joining two DataFrames on a shared key with merge()  [reward 3]
Merge and join — Orders and driver details live in separate tables, linked by driver_id. merge() matches rows on that shared key and combines the columns.
(definition) `merge()` combines two DataFrames by matching values in a shared key column, specified with the `on` parameter: `orders.merge(drivers, on="driver_id")`. The result contains one row for every matched pair — columns from both tables side by side. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) The `how` parameter controls which keys are kept. `how='inner'` (the default) keeps only key values present in **both** DataFrames — a `driver_id` that appears in orders but not in drivers won't survive an inner merge, and vice versa. ⟦B.f2 B:tb3⟧
(mechanism) When a key value does not appear in one of the two DataFrames, the corresponding values contributed by that DataFrame in the joined result are `NA`. This is what happens once a join type other than the default inner merge is used and unmatched keys are allowed to stay in the result. ⟦B.f3 B:tb4⟧
[DIAGRAM: Join types — which keys survive] nodes=['Left only\n(orders keys\nnot in drivers)', 'Inner\n(keys in both)', 'Right only\n(drivers keys\nnot in orders)', "how='inner'\nkeeps only this", "how='left'\nkeeps left + inner", "how='outer'\nkeeps all three"] edges=[('inner_label', 'inner', None), ('left_label', 'left_only', None), ('left_label', 'inner', None), ('outer_label', 'left_only', None), ('outer_label', 'inner', None), ('outer_label', 'right_only', None)] alt: Venn diagram of two overlapping circles: left circle is orders keys, right circle is drivers keys. The overlap is the inner join. how='inner' keeps only the overlap; how='left' keeps the left circle and overlap; how='outer' keeps everything. Unmatched keys in the result get NA values from the missing side.

### s06 · video · Merging DataFrames on a shared key
See it in action — Watch merge() join orders to drivers and see how changing how= keeps or drops unmatched rows.
[VIDEO Merging on a shared key and the join types] bridge-before: Clip 1 shows the four join types as diagrams and the default inner merge; clip 2 shows left, outer and inner results with NaN gaps. Clip 2 writes pd.merge(df1, df3, ...) where Devspace writes df.merge(...). Clip 1 has a mid-clip sponsor read. | bridge-after: Right is never run in either clip: remember how='right' keeps every key from the right table only. Clip 1 doesn't show NaN for unmatched keys, but clip 2 does.
  - TPivN7tpdwc 0-399s facts=['f1', 'f2', 'f4'] label: Join types in diagrams, then df.merge() with the default inner join and the on= argument | summary: Opens with diagrams of four join types: inner returns only what is in both tables, outer takes everything, left takes everything from the left table plus matches, and right does the reverse. Two small Lord of the Rings tables that overlap on some IDs and names are then loaded (with a short sponsor read in between). df1.merge(df2) with no arguments does an inner join, matching on both shared columns, and how='inner' confirms it is the default. Setting on='fellowship_id' matches on that column alone, so the other shared column appears twice with _x and _y suffixes.
  - XMjSGGej9y8 478-698s facts=['f1', 'f2', 'f3'] label: Merging on a shared Year key and what how=left, outer and inner keep | summary: Merges two small tables on their Year column with pd.merge(df1, df3, on='Year'); the default result is missing the years found in only one table. how='left' keeps the keys of the first table (2001 to 2004), with NaN where the second table has no data. how='outer' keeps the union of all the keys, again with NaN where data is absent. how='inner', the default, keeps only the keys both tables share. A right merge is described aloud but not run.

### s07 · explainer · Left, right, and outer joins  [reward 2]
Join types — Beyond the default inner join, three other how= values let you keep unmatched rows from one or both sides.
(mechanism) The `how` parameter also accepts `'left'` (keep all keys from the left DataFrame only), `'right'` (keep all keys from the right DataFrame only), and `'outer'` (keep the union of keys from both DataFrames). `orders.merge(drivers, on="driver_id", how="left")` keeps every order, filling in `NA` for driver details on any `driver_id` that merge can't find in the drivers table. ⟦B.f4 B:tb5⟧

### s08 · check · Merging on a shared key and choosing a join type  [reward 2]
Quick check — Confirm you can identify the correct merge call and the effect of the how= parameter.
QUESTION [choice, core, grading=client] You have `orders` with `customer_id` and `customers` with `customer_id`. You want to keep all orders and attach customer info where available, filling NaN for unmatched orders. Which `how` parameter is correct?
  ✔ opt_a: `orders.merge(customers, on='customer_id', how='left')`
      why: Correct. `how='left'` keeps all rows from the left DataFrame (orders) and fills NaN for unmatched keys.
  ✘ opt_b: `orders.merge(customers, on='customer_id', how='inner')`
      why: `how='inner'` (the default) keeps only rows where the key appears in both DataFrames, dropping unmatched orders. Use `how='left'` to keep all orders.
  ✘ opt_c: `orders.merge(customers, on='customer_id', how='right')`
      why: `how='right'` keeps all rows from the right DataFrame (customers), not all orders. Use `how='left'` to keep all orders.
  ✘ opt_d: `orders.merge(customers, on='customer_id', how='outer')`
      why: `how='outer'` keeps all keys from both DataFrames, including customers with no orders. Use `how='left'` to keep only all orders.
  feedback✔: Exactly right. `how='left'` keeps all rows from the left DataFrame.  feedback✘: Not quite. Review which `how` parameter keeps all rows from the left DataFrame.  hints: ['Think about which join type keeps all rows from the first (left) DataFrame.']  remediation→r02
  MEASURES: B:merge_on_shared_key(f1); B:choose_how_join_type(f4)   anchors=['assessment:merge_on_shared_key', 'assessment:choose_how_join_type']
  taught-before-tested: B.f1←s05; B.f4←s07

### s09 · check · NA values for unmatched keys  [reward 2]
Quick check — Confirm you understand what happens to unmatched key values in a non-inner merge.
QUESTION [choice, core, grading=client] After a left merge of `orders` and `customers` on `customer_id`, some rows have NaN in the `customer_name` column. What does this mean?
  ✔ opt_a: Those orders have a `customer_id` that does not appear in the `customers` table.
      why: Correct. When a key value does not appear in one DataFrame, the columns from that DataFrame are filled with NaN in the result.
  ✘ opt_b: Those orders have a missing `customer_id` value.
      why: Not quite. The NaN appears in the customer columns because the `customer_id` from orders does not match any row in customers, not because the `customer_id` itself is missing.
  ✘ opt_c: The merge failed for those rows.
      why: The merge did not fail. NaN values are the expected result when a key from the left DataFrame has no match in the right DataFrame.
  ✘ opt_d: Those customers have no orders.
      why: This is a left merge starting from orders, so the NaN means the order's `customer_id` has no match in customers, not that customers have no orders.
  feedback✔: Exactly right. Unmatched keys result in NaN for the columns from the other DataFrame.  feedback✘: Not quite. Review what NaN means in a merge result.  hints: ['Think about what happens when a key value appears in one DataFrame but not the other.']  remediation→r03
  MEASURES: B:explain_na_for_unmatched_keys(f3)   anchors=['assessment:explain_na_for_unmatched_keys']
  taught-before-tested: B.f3←s05

### s10 · hands_on · Join orders to customers and predict the inner merge result  [reward 5]
Practice — Use merge() to join the orders table to the customers table on customer_id, then explore what an inner join keeps.
QUESTION [code_exercise, core, grading=client] The `orders` DataFrame has `customer_id` and the `customers` DataFrame has `customer_id`, `customer_name`, and `segment`. Use `.merge()` to join them on `customer_id` (inner join), then print the result.

The result should have one row per order whose `customer_id` also appears in customers, with the customer columns attached.

Use only `orders.merge(customers, on='customer_id')`, `how='inner'`, `how='left'`, `how='right'`, `how='outer'`, and `print()`.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=["orders.merge(customers, on='customer_id')", "how='inner'", "how='left'", "how='right'", "how='outer'", 'print()'] blocked=5 items
  file solution.py [editable]:
import pandas as pd

orders = pd.read_csv('orders.csv')
customers = pd.read_csv('customers.csv')
df = orders

on_col = 'customer_id'

# Merge df with customers on on_col
# Store in result

print(result)

  SOLUTION solution.py:
import pandas as pd

orders = pd.read_csv('orders.csv')
customers = pd.read_csv('customers.csv')
df = orders

on_col = 'customer_id'

result = df.merge(customers, on=on_col)

print(result)

  test t1 (dataframe_equals, visible=True): {"expr":"orders.merge(customers, on='customer_id')[['customer_id', 'customer_name', 'segment']]","expected":{"columns":["customer_id","customer_name","segment"],"rows":[[301,"Ngozi Eze","Individual"],[302,"Emeka Obi","Business"],[303,"Fatima Musa","Individual"],[304,"Tunde Bakare","Business"],[305,"Amaka Nwosu","Individual"],[306,"Yusuf Garba","Business"],[307,"Chisom Ike","Individual"],[308,"Bisi Adewale","Business"],[309,"Halima Sule","Individual"],[310,"Rotimi Coker","Business"],[311,"Nkechi  | on-fail: The result should have one row per order with matching customer_id, with customer columns attached.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"d99b16522485a791cce8b0acbbb0d916bd540cafb2585ed483c32d887541fd90","tests_passed":1}
  feedback✔: Perfect! You joined the two tables on the shared key.  feedback✘: Not quite. Make sure you use `orders.merge(customers, on='customer_id')` for an inner join.  hints: ["Use `orders.merge(customers, on='customer_id')` to join on the shared key."]
  MEASURES: B:predict_inner_merge_result(f2)   anchors=['practice', 'assessment:predict_inner_merge_result']
  taught-before-tested: B.f2←s05

### s11 · recap · Concatenation and merging — key takeaways  [reward 5]
Recap — concat glues tables end to end; merge matches rows on a shared key. The axis and how parameters control the direction and which rows survive.
(takeaway) `pd.concat()` glues tables end to end — the `axis` argument is just which direction: down for more rows (default), sideways for more columns. `merge()` matches rows on a shared key; setting `how` decides whether unmatched rows on either side get dropped (`inner`) or kept with `NA` gaps (`left`, `right`, `outer`). Use concat when tables share the same columns; use merge when they share a key column. ⟦A.f1 A.f2 A.f3 B.f1 B.f2 B.f3 B.f4 A:tb5 B:tb6⟧
[UP NEXT] Up next: Grouping, Aggregating, and Reshaping with melt: Next you'll use groupby to summarise orders by city, and melt() to reshape a wide monthly deliveries table into the long format that analysis tools commonly expect.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · How the axis parameter changes concat direction — axis=0 stacks rows; axis=1 places tables side by side as columns.
(mechanism) `pd.concat()` takes an `axis` parameter: by default (no `axis` argument) it stacks the objects row-wise, while `axis=1` places them side by side as columns. Think of it as which direction "end to end" points — down for more rows, sideways for more columns. ⟦A.f3 A:tb4⟧
[BEFORE_AFTER] axis=0 (default) appends rows; axis=1 appends columns.
  before:
[CODE python]
# Default axis=0: rows stacked
result = pd.concat([jan_orders, feb_orders, mar_orders])
print(result.shape)  # (15, 5) — more rows
  annotations: ['No axis argument → axis=0 → rows appended below']
  after:
[CODE python]
# axis=1: columns placed side by side
result = pd.concat([orders_basic_info, orders_extra_columns], axis=1)
print(result.shape)  # same rows, more columns
  annotations: ['axis=1 → columns placed side by side']
### r02 · Merging on a key and controlling which rows survive — merge() matches rows on a shared column. The how= parameter decides whether unmatched rows are dropped or kept with NA.
(mechanism) `merge()` combines two DataFrames by matching values in a shared key column specified with `on`. The `how` parameter controls which keys are kept: `how='inner'` (the default) keeps only key values present in both DataFrames. `how='left'` keeps all keys from the left DataFrame, filling `NA` for any driver details that can't be found in the right table. ⟦B.f1 B.f4 B:tb2 B:tb3 B:tb5⟧
[BEFORE_AFTER] Inner merge drops unmatched keys; left merge keeps all left rows and fills NA for missing right-side values.
  before:
[CODE python]
# Inner merge — only matched driver_ids survive
result = orders.merge(drivers, on='driver_id')
# driver_id 204 (in drivers but not orders) is dropped
  annotations: ["how='inner' is the default — unmatched keys dropped"]
  after:
[CODE python]
# Left merge — all orders kept, NA for unmatched drivers
result = orders.merge(drivers, on='driver_id', how='left')
# Every order row is present; driver_name is NA if driver_id not in drivers
  annotations: ["how='left' keeps all left rows; fills NA on right side"]
### r03 · Why unmatched keys produce NA values — When a key value exists on only one side of a merge, the columns from the missing side have nothing to contribute — so they become NA.
(mechanism) If a key value does not appear in one of the two DataFrames being merged, the corresponding values contributed by that DataFrame in the joined result are `NA`. This is what happens once a join type other than the default inner merge is used and unmatched keys are allowed to stay in the result — for example, a `driver_id` that exists in orders but not in drivers will have `NA` in every driver column. ⟦B.f3 B:tb4⟧
[BEFORE_AFTER] Unmatched key values in a non-inner merge produce NA in the columns contributed by the side that lacks that key.
  before:
[TABLE ds_drivers cols=['driver_id', 'driver_name', 'vehicle', 'base_city'] ] caption: drivers table — driver_id 204 (Dami Fashola) exists here but not in orders
  after:
[CODE python]
# Left merge: all orders kept
result = orders.merge(drivers, on='driver_id', how='left')
# Any order whose driver_id is not in drivers
# gets NA in driver_name, vehicle, base_city
  annotations: ['Unmatched driver_id → NA in all driver columns']

## OTHER CONTENT (fields without a dedicated renderer)
· nodes.label: Left only
(orders keys
not in drivers)
· nodes.label: Inner
(keys in both)
· nodes.label: Right only
(drivers keys
not in orders)
· nodes.label: how='inner'
keeps only this
· nodes.label: how='left'
keeps left + inner
· nodes.label: how='outer'
keeps all three

=========

# EVALUATOR PACKET — Grouping, Aggregating, and Reshaping with melt (tile_pandas_groupby_melt)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.groupby_aggregation — Grouping and aggregation (groupby)
B = pandas.melt_reshaping — Melt reshaping

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (pandas.groupby_aggregation)   objective: Split a DataFrame into groups by a key, apply an aggregation, and combine the results into one summarized row per group using groupby.
A.f1: Group by refers to a process involving one or more of the following steps: splitting the data into groups based on some criteria, applying a function to each group independently, and combining the results into a data structure.   [sources: pandas_docs_groupby#group-by-split-apply-combine]
A.f2: An aggregation is a groupby operation that reduces each group to a single summary value per column, such as computing the sum of a column within each group.   [sources: pandas_docs_groupby#aggregation]
A.f3: In practice, you call df.groupby(key) and then an aggregation method such as .sum() or .mean() on the DataFrame or a selected column, or .agg([...]) to compute several aggregations at once; by default the group keys become the index of the result.   [sources: pandas_docs_groupby#aggregation]
PRACTICE ANCHOR (live_code): Compute total and average order value per customer using groupby.  SUCCESS: The printed result has one row per customer with the sum and mean of order value, and the customer IDs form the index.
ASSESSMENT ANCHOR: describe_split_apply_combine facts=['f1']
ASSESSMENT ANCHOR: write_groupby_aggregation facts=['f2', 'f3']
ASSESSMENT ANCHOR: read_group_keys_as_result_index facts=['f3']

## SOURCE FACTS — B (pandas.melt_reshaping)   objective: Reshape a wide-format DataFrame into long format using melt.
B.f1: melt() reshapes a DataFrame from wide to long format: the columns listed as id_vars stay as identifier columns, while all other columns are unpivoted into two columns, one holding the original column names and one holding their values.   [sources: pandas_docs_reshaping#melt-and-wide-to-long]
B.f2: The default 'variable' and 'value' column names produced by melt() can be renamed using its var_name and value_name parameters.   [sources: pandas_docs_reshaping#melt-and-wide-to-long]
PRACTICE ANCHOR (live_code): Melt a wide table of monthly columns into a long table with a single month column and a single value column.  SUCCESS: The printed long table has one row per identifier-and-month pair, with the learner's chosen month and value column names.
ASSESSMENT ANCHOR: melt_wide_to_long_with_id_vars facts=['f1']
ASSESSMENT ANCHOR: rename_melt_output_columns facts=['f2']

## DATA ASSETS USED
ds_monthly_long: Monthly Deliveries by City (Long) — columns: city(categorical), month(categorical), deliveries(numerical)
   ["Lagos","jan_deliveries",142]
   ["Lagos","feb_deliveries",138]
   ["Lagos","mar_deliveries",155]
   ["Abuja","jan_deliveries",98]
   ["Abuja","feb_deliveries",104]
   ["Abuja","mar_deliveries",110]
   ["Kano","jan_deliveries",76]
   ["Kano","feb_deliveries",81]
ds_monthly_wide: Monthly Deliveries by City (Wide) — columns: city(categorical), jan_deliveries(numerical), feb_deliveries(numerical), mar_deliveries(numerical)
   ["Lagos",142,138,155]
   ["Abuja",98,104,110]
   ["Kano",76,81,88]
ds_orders: SwiftDrop Orders — columns: order_id(identifier,digits-as-label), city(categorical), city_code(categorical), courier(categorical), driver_id(identifier,digits-as-label), customer_id(identifier,digits-as-label), pickup_date(datetime), delivery_time_minutes(numerical), distance_km(numerical), order_value(numerical)
   [1001,"Lagos","LOS","Ada",201,301,"2024-03-14",18,4.2,2500]
   [1002,"Abuja","ABJ","Bayo",202,302,"2024-03-14",20,6.1,3100]
   [1003,"Kano","KAN","Chidi",203,303,"2024-03-15",22,5.5,1800]
   [1004,"Lagos","LOS","Ada",201,304,"2024-03-15",22,3.8,2200]
   [1005,"Abuja","ABJ","Bayo",202,305,"2024-03-16",26,7.3,4000]
   [1006,"Kano","KAN","Chidi",203,306,"2024-03-16",28,8.0,1500]
   [1007,"Lagos","LOS","Ada",201,307,"2024-03-17",80,12.4,5500]
   [1008,"Abuja","ABJ","Bayo",202,308,"2024-03-17",31,9.2,3800]
   variant orders_messy: 5 ops; planted: iss_city_case_1004(inconsistent_category); iss_city_case_1007(inconsistent_category); iss_dist_string(wrong_type); iss_missing_dt(missing_value); iss_duplicate_1003(duplicate_row)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Aggregate functions (COUNT, SUM, AVG, MIN, MAX); CASE expressions for conditional logic in queries; COALESCE for fallback values and NULL handling; Common SQL string functions for cleaning text; DISTINCT for de-duplication; Entities and tables as models of real-world objects; Exporting cleaned data (to_csv); Foreign keys and referential integrity; GROUP BY grouping semantics; HAVING clause for filtering aggregated groups; Limiting results (LIMIT/OFFSET); Logical operators (AND, OR, NOT) in filtering; Melt reshaping; NULL handling (IS NULL / IS NOT NULL); One-to-many relationships; Pivot table reshaping; Primary keys; Relational database and table structure basics; SELECT statement fundamentals (columns, aliasing); SQL date/time extraction and arithmetic; SQL formatting/naming conventions per style guide; SQL type casting and conversion; Sorting results with ORDER BY (ASC/DESC); Table and column aliasing for readability; UNION and UNION ALL for stacking compatible query results; WHERE clause filtering and comparison operators

## LESSON, in learner order

### s01 · explainer · Split, apply, combine — groupby in three steps  [reward 3]
Groupby aggregation — To find the average delivery time per city, you don't filter and average three times. groupby does all three steps — split, apply, combine — in one call.
(definition) **Group by** refers to a process involving one or more of the following steps: splitting the data into groups based on some criteria, applying a function to each group independently, and combining the results into a data structure. For SwiftDrop orders, that means splitting every order into its city's group, applying "average" within each group, then combining the per-city averages into one result. ⟦A.f1 A:tb1 A:tb2⟧
(mechanism) An **aggregation** is a groupby operation that reduces each group to a single summary value per column — for example, computing the sum of `order_value` within each city group. The result has one row per group, not one row per original order. ⟦A.f2 A:tb3⟧
[PROCESS_FLOW: Split → Apply → Combine] nodes=['All orders\n(8 rows)', 'Split\nby city', 'Lagos\ngroup', 'Abuja\ngroup', 'Kano\ngroup', 'Apply\naggregation\n(e.g. mean)', 'Combine\ninto one\nsummary table'] edges=[('raw', 'split', None), ('split', 'lagos', None), ('split', 'abuja', None), ('split', 'kano', None), ('lagos', 'apply', None), ('abuja', 'apply', None), ('kano', 'apply', None), ('apply', 'combine', None)] alt: 8 order rows are split into three city groups (Lagos, Abuja, Kano). An aggregation function is applied inside each group. The per-group results are combined into one summary table with one row per city.

### s02 · video · groupby in practice
See it in action — Watch groupby split orders by city and aggregate delivery times and order values.
[VIDEO Grouping and aggregating with groupby] bridge-before: Watch groupby do nothing useful until an aggregation like mean() follows, and the group key become the index. The clip's .mean() skips text columns; in pandas 2.0 and later that raises an error unless you select a numeric column or pass numeric_only=True. | bridge-after: The clip never names the split, apply and combine steps, and it stops before agg() for several aggregations at once. Both come from Devspace's text.
  - VRmXto2YA2I 0-358s facts=['f1', 'f2', 'f3'] label: df.groupby() with mean, count, min, max and sum, giving one row per group | summary: Explains groupby as gathering the values of one column so aggregate functions can be run on each group. On an ice-cream ratings table, grouping by base flavor alone returns only a groupby object. Adding .mean() gives one row per base flavor (chocolate and vanilla), averaging the numeric columns, with base flavor now the index. Then count shows how many rows fed each group (3 and 6), min and max also work on text by picking the alphabetical first or last, and sum totals the numeric columns. A short sponsor read sits in the middle.

### s03 · explainer · Calling groupby and choosing an aggregation  [reward 2]
Groupby syntax — One call chains the grouping key with the aggregation method. You can compute one statistic or several at once.
(syntax) Call `df.groupby(key)` then chain an aggregation method such as `.sum()` or `.mean()` on the DataFrame or a selected column. Use `.agg([...])` to compute several aggregations at once. By default, the group keys become the index of the result: `orders.groupby("city")["delivery_time_minutes"].mean()` returns one average per city with city names as the index; `orders.groupby("city")["delivery_time_minutes"].agg(["mean", "sum"])` computes both in one call. ⟦A.f3 A:tb4⟧

### s04 · check · Describing the split-apply-combine process  [reward 2]
Quick check — Confirm you can describe what groupby does in terms of split, apply, and combine.
QUESTION [choice, intro, grading=client] What does the 'split-apply-combine' pattern describe in the context of `groupby()`?
  ✔ opt_a: Split the data into groups, apply a function to each group independently, and combine the results into a data structure.
      why: Correct. The split-apply-combine pattern is the core of `groupby()`: split by a key, apply a function to each group, and combine the results.
  ✘ opt_b: Split the DataFrame into rows and columns, apply a filter, and combine them back.
      why: Not quite. The pattern is about grouping by a key column, not splitting into rows and columns. Review the three steps: split, apply, combine.
  ✘ opt_c: Split the data by index, apply a sort, and combine the sorted pieces.
      why: The pattern is not about sorting. It's about grouping data by a key, applying a function to each group, and combining the results.
  ✘ opt_d: Split the data into training and test sets, apply a model, and combine predictions.
      why: That describes a machine learning workflow, not `groupby()`. The split-apply-combine pattern groups data by a key, applies a function to each group, and combines the results.
  feedback✔: Exactly right. Split-apply-combine is the foundation of `groupby()` operations.  feedback✘: Not quite. Review the three steps of the split-apply-combine pattern.  hints: ['Think about what happens when you group data by a key and compute a summary for each group.']  remediation→r01
  MEASURES: A:describe_split_apply_combine(f1)   anchors=['assessment:describe_split_apply_combine']
  taught-before-tested: A.f1←s01

### s05 · hands_on · Aggregate delivery times and order values by city  [reward 5]
Practice — Use groupby to compute the mean delivery time and total order value per city from the SwiftDrop orders table.
QUESTION [code_exercise, core, grading=client] The `orders` DataFrame has `customer_id` and `order_value` columns. Use `groupby('customer_id')` to compute both the sum and mean of `order_value` for each customer in one call using `.agg(['sum', 'mean'])`. Print the result.

The customer IDs should form the index of the result.

Use only `df.groupby('key')['col'].sum()`, `df.groupby('key')['col'].mean()`, `df.groupby('key')['col'].agg([...])`, and `print()`.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=["df.groupby('key')['col'].sum()", "df.groupby('key')['col'].mean()", "df.groupby('key')['col'].agg([...])", 'print()'] blocked=4 items
  file solution.py [editable]:
import pandas as pd

orders = pd.read_csv('orders.csv')

df = orders.groupby('customer_id')['order_value']
agg_funcs = ['sum', 'mean']
# Use .agg(agg_funcs) on df to compute both aggregations
# Store in result

print(result)

  SOLUTION solution.py:
import pandas as pd

orders = pd.read_csv('orders.csv')

df = orders.groupby('customer_id')['order_value']
agg_funcs = ['sum', 'mean']
result = df.agg(agg_funcs)

print(result)

  test t1 (dataframe_equals, visible=True): {"expr":"result","expected":{"columns":["sum","mean"],"rows":[[2500.0,2500.0],[3100.0,3100.0],[1800.0,1800.0],[2200.0,2200.0],[4000.0,4000.0],[1500.0,1500.0],[5500.0,5500.0],[3800.0,3800.0],[2100.0,2100.0],[2900.0,2900.0],[4200.0,4200.0],[1700.0,1700.0],[3300.0,3300.0],[4600.0,4600.0]]}} | on-fail: The result should have one row per customer_id with sum and mean of order_value.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"fe20d99535dc3640b55f1e322b7b6d237223cb7bec64242e87cb7d839ef3fd5e","tests_passed":1}
  feedback✔: Perfect! You computed multiple aggregations in one call.  feedback✘: Not quite. Make sure you use `.agg(['sum', 'mean'])` to compute both aggregations.  hints: ["Use `orders.groupby('customer_id')['order_value'].agg(['sum', 'mean'])` to compute both aggregations in one call."]
  MEASURES: A:write_groupby_aggregation(f2,f3); A:read_group_keys_as_result_index(f3)   anchors=['practice', 'assessment:write_groupby_aggregation', 'assessment:read_group_keys_as_result_index']
  taught-before-tested: A.f2←s01; A.f3←s03; A.f3←s03

### s06 · explainer · Turning a wide table into a long one with melt()  [reward 3]
Melt reshaping — A wide summary table has one column per month. melt() unpivots those columns into rows — one row per city-month combination.
(practical_context) The SwiftDrop monthly deliveries table has one row per city and separate columns `jan_deliveries`, `feb_deliveries`, `mar_deliveries`. Many analysis tools and visualisation libraries expect one row per city-month combination instead — that's the long format. ⟦B.f1 B:tb1⟧
(definition) `melt()` reshapes a DataFrame from wide to long format: the columns listed as `id_vars` stay as identifier columns, while all other columns are unpivoted into two new columns — one holding the original column names and one holding their values. `city_deliveries.melt(id_vars=["city"])` keeps `city` as an identifier and turns the three month columns into two new columns. ⟦B.f1 B:tb2⟧
(mechanism) The default output column names are `variable` and `value`. Use `var_name` and `value_name` to rename them: `city_deliveries.melt(id_vars=["city"], var_name="month", value_name="deliveries")` gives the two new columns clearer names. ⟦B.f2 B:tb3⟧
[BEFORE_AFTER] Wide table (3 rows × 4 columns) melted to long format (9 rows × 3 columns) with id_vars=['city'], var_name='month', value_name='deliveries'.
  before:
[TABLE ds_monthly_wide cols=['city', 'jan_deliveries', 'feb_deliveries', 'mar_deliveries'] tags=jan_deliveries:will become rows, feb_deliveries:will become rows, mar_deliveries:will become rows] caption: Wide format — one column per month
  after:
[TABLE ds_monthly_long cols=['city', 'month', 'deliveries'] tags=month:former column names, deliveries:former column values] caption: Long format — one row per city-month, month column renamed via var_name='month'

### s07 · video · Reshaping wide to long with melt()
See it in action — Watch melt() unpivot month columns into rows and how var_name and value_name rename the output.
[VIDEO Wide to long with melt] bridge-before: Watch which column stays fixed (id_vars) and how every other column becomes a variable/value pair. | bridge-after: The clip stops after renaming. Devspace's example melts city delivery counts by month, so you can practise the same two steps: keep the id column, then rename variable and value.
  - ldpDNtPC_mU 0-202s facts=['f1', 'f2'] label: pd.melt with id_vars, then renaming the new columns with var_name and value_name | summary: Starts with wide sales data, one row per store with a separate column for each month, and explains why a long format, with one column for months and one for values, suits analysis. pd.melt with id_vars='Store' keeps Store as it is and turns the Jan, Feb and Mar sales columns into two columns named variable and value. A second call adds var_name='Month' and value_name='Sales' to give those columns clearer names, leaving a tidy table.

### s08 · check · Renaming melt output columns  [reward 2]
Quick check — Confirm you know which parameters rename the two new columns that melt() produces.
QUESTION [choice, core, grading=client] Which single `melt()` call renames them to 'month' and 'deliveries'?
  ✔ opt_a: `df.melt(id_vars=['city'], var_name='month', value_name='deliveries')`
      why: Correct. `var_name` and `value_name` parameters rename the default 'variable' and 'value' columns.
  ✘ opt_b: `df.melt(id_vars=['city']).rename(columns={'variable': 'month', 'value': 'deliveries'})`
      why: `.rename()` is a separate method that renames existing columns after the fact. `melt()` has its own built-in `var_name` and `value_name` parameters specifically for this purpose — use those instead of chaining a second method.
  ✘ opt_c: `df.melt(id_vars=['city'], columns=['month', 'deliveries'])`
      why: There is no `columns` parameter for `melt()`. Use `var_name` and `value_name` to rename the output columns.
  ✘ opt_d: `df.melt(id_vars=['city'], names=['month', 'deliveries'])`
      why: There is no `names` parameter for `melt()`. Use `var_name` and `value_name` to rename the output columns.
  feedback✔: Exactly right. `var_name` and `value_name` control the output column names.  feedback✘: Not quite. Review the parameters that rename the output columns of `melt()`.  hints: ["Think about which parameters `melt()` accepts to rename the 'variable' and 'value' columns."]  remediation→r02
  MEASURES: B:rename_melt_output_columns(f2)   anchors=['assessment:rename_melt_output_columns']
  taught-before-tested: B.f2←s06

### s09 · hands_on · Melt the monthly deliveries table from wide to long  [reward 5]
Practice — Use melt() with id_vars, var_name, and value_name to reshape the city deliveries table.
QUESTION [code_exercise, core, grading=client] The `city_deliveries` DataFrame has a `city` column and three month columns (`jan`, `feb`, `mar`). Use `.melt()` to reshape it to long format with `id_vars='city'`, `var_name='month'`, and `value_name='deliveries'`. Print the result.

The result should have one row per city-month combination.

Use only `df.melt(id_vars=[...])`, `pd.melt(df, id_vars=[...])`, `var_name='month'`, `value_name='value'`, and `print()`.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=['df.melt(id_vars=[...])', 'pd.melt(df, id_vars=[...])', "var_name='month'", "value_name='value'", 'print()'] blocked=3 items
  file solution.py [editable]:
import pandas as pd

city_deliveries = pd.read_csv('city_deliveries.csv')
df = city_deliveries

id_col = 'city'
var = 'month'
val = 'deliveries'

# Melt df using id_col, var, val
# Store in result

print(result)

  SOLUTION solution.py:
import pandas as pd

city_deliveries = pd.read_csv('city_deliveries.csv')
df = city_deliveries

id_col = 'city'
var = 'month'
val = 'deliveries'

result = df.melt(id_vars=id_col, var_name=var, value_name=val)

print(result)

  test t1 (dataframe_equals, visible=True): {"expr":"city_deliveries.melt(id_vars=['city'], var_name='month', value_name='deliveries')","expected":{"columns":["city","month","deliveries"],"rows":[["Lagos","jan_deliveries",142],["Abuja","jan_deliveries",98],["Kano","jan_deliveries",76],["Lagos","feb_deliveries",138],["Abuja","feb_deliveries",104],["Kano","feb_deliveries",81],["Lagos","mar_deliveries",155],["Abuja","mar_deliveries",110],["Kano","mar_deliveries",88]]}} | on-fail: The result should have one row per city-month combination with columns city, month, deliveries.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"b110c0ee6b265998f92d4b762a5f6384eb983630b2712e6f75bc6aceb52df101","tests_passed":1}
  feedback✔: Perfect! You reshaped the wide table to long format.  feedback✘: Not quite. Make sure you use `id_vars=['city']`, `var_name='month'`, and `value_name='deliveries'`.  hints: ["Use `city_deliveries.melt(id_vars=['city'], var_name='month', value_name='deliveries')` to reshape."]  remediation→r02
  MEASURES: B:melt_wide_to_long_with_id_vars(f1); B:rename_melt_output_columns(f2)   anchors=['practice', 'assessment:melt_wide_to_long_with_id_vars', 'assessment:rename_melt_output_columns']
  taught-before-tested: B.f1←s06; B.f2←s06

### s10 · recap · Groupby aggregation and melt — key takeaways  [reward 5]
Recap — groupby summarises data by group; melt reshapes wide tables into the long format that analysis tools commonly expect.
(takeaway) Split, apply, combine is the whole idea — `groupby` gives you one call that does all three steps for whatever key and aggregation you choose. Chain `.mean()`, `.sum()`, or `.agg([...])` after `groupby(key)` to get per-group summaries; the group keys become the result's index by default. `melt()` is the complementary reshape: it unpivots wide columns into rows, keeping `id_vars` fixed and turning the rest into a `variable`/`value` pair that you can rename with `var_name` and `value_name`. ⟦A.f1 A.f2 A.f3 B.f1 B.f2 A:tb5⟧
[UP NEXT] Up next: Pivot Tables and Exporting Data: Next you'll use pivot_table() to spread long data back into a wide grid — aggregating duplicate cells automatically — and then write the result to a CSV file with to_csv().

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · The three steps inside every groupby call — groupby always does the same three things: split the rows into groups, apply a function to each group, then combine the results.
(definition) **Group by** refers to a process involving one or more of the following steps: splitting the data into groups based on some criteria, applying a function to each group independently, and combining the results into a data structure. For SwiftDrop orders: split every order into its city's group, apply "average delivery time" within each group, then combine the per-city averages into one summary table. ⟦A.f1 A:tb2⟧
[BEFORE_AFTER] 8 individual order rows reduced to 3 per-city averages by groupby split-apply-combine.
  before:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] ] caption: All orders mixed together — no per-city summary yet
  after:
[CODE python]
# Split by city, apply mean, combine into one result
result = orders.groupby('city')['delivery_time_minutes'].mean()
print(result)
# city
# Abuja    ...
# Kano     ...
# Lagos    ...
  annotations: ['groupby splits, .mean() applies, result combines', 'One average per city — city names become the index']
### r02 · Renaming the variable and value columns in melt() — melt() always produces two new columns. By default they're called 'variable' and 'value' — var_name and value_name let you rename them.
(mechanism) The default `variable` and `value` column names produced by `melt()` can be renamed using its `var_name` and `value_name` parameters. Passing `var_name="month"` renames the column that holds the original column names; passing `value_name="deliveries"` renames the column that holds their values. ⟦B.f2 B:tb3⟧
[BEFORE_AFTER] Default 'variable' and 'value' column names replaced with 'month' and 'deliveries' using var_name and value_name.
  before:
[CODE python]
# Without renaming — default column names
city_deliveries.melt(id_vars=['city'])
# Columns: city | variable | value
  annotations: ["Default names 'variable' and 'value' are generic"]
  after:
[CODE python]
# With var_name and value_name
city_deliveries.melt(
    id_vars=['city'],
    var_name='month',
    value_name='deliveries'
)
# Columns: city | month | deliveries
  annotations: ["var_name renames 'variable'; value_name renames 'value'"]

## OTHER CONTENT (fields without a dedicated renderer)
· nodes.label: Apply
aggregation
(e.g. mean)
· nodes.label: Combine
into one
summary table

=========

# EVALUATOR PACKET — Mapping and Applying Transformations (tile_pandas_map_apply)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.map_substitution — Map substitution
B = pandas.apply_transform — Apply transform

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: tile_pandas_map_apply.s02: remediation tile_pandas_map_apply.r01 re-teaches ['pandas.map_substitution#f2'] but the check measures ['pandas.map_substitution#f1'] — a learner who fails it is sent to an unrelated fact
  warn: plan: tile_pandas_map_apply.s02 was planned to measure pandas.map_substitution#assessment:recode_values_with_dict_mapping but its interaction does not
  warn: plan: tile_pandas_map_apply.s03 was planned to measure pandas.map_substitution#assessment:map_series_with_function but its interaction does not

## SOURCE FACTS — A (pandas.map_substitution)   objective: Substitute or translate the values of a pandas Series element-wise using .map() with a function or a mapping.
A.f1: Series.map() accepts a Python function taking a single value and returning a single value, and applies it to every element of the Series.   [sources: pandas_docs_basics#applying-elementwise-functions]
A.f2: Series.map() can substitute each value in the Series using a mapping correspondence that may be a function, a dict, or a Series.   [sources: pandas_docs_series_map]
PRACTICE ANCHOR (live_code): Use Series.map() with a lookup dictionary to recode categorical codes into human-readable labels.  SUCCESS: The printed column shows the full label for every code that appears in the lookup dict.
ASSESSMENT ANCHOR: map_series_with_function facts=['f1']
ASSESSMENT ANCHOR: recode_values_with_dict_mapping facts=['f2']

## SOURCE FACTS — B (pandas.apply_transform)   objective: Transform DataFrame or Series values by applying a custom function along an axis using .apply().
B.f1: DataFrame.apply() applies an arbitrary function along an axis of the DataFrame, operating on each column by default, or on each row when axis=1.   [sources: pandas_docs_basics#row-or-column-wise-function-application]
note: Skip the optional note pointing to map() for elementwise work -- not required, and map() is covered separately.
PRACTICE ANCHOR (live_code): Use apply() to compute a new derived column from an existing DataFrame using a custom function.  SUCCESS: The new column holds one value per row computed by the learner's function from that row's existing columns.
ASSESSMENT ANCHOR: apply_function_down_columns facts=['f1']
ASSESSMENT ANCHOR: apply_function_across_rows_with_axis_1 facts=['f1']

## DATA ASSETS USED
ds_orders: SwiftDrop Orders — columns: order_id(identifier,digits-as-label), city(categorical), city_code(categorical), courier(categorical), driver_id(identifier,digits-as-label), customer_id(identifier,digits-as-label), pickup_date(datetime), delivery_time_minutes(numerical), distance_km(numerical), order_value(numerical)
   [1001,"Lagos","LOS","Ada",201,301,"2024-03-14",18,4.2,2500]
   [1002,"Abuja","ABJ","Bayo",202,302,"2024-03-14",20,6.1,3100]
   [1003,"Kano","KAN","Chidi",203,303,"2024-03-15",22,5.5,1800]
   [1004,"Lagos","LOS","Ada",201,304,"2024-03-15",22,3.8,2200]
   [1005,"Abuja","ABJ","Bayo",202,305,"2024-03-16",26,7.3,4000]
   [1006,"Kano","KAN","Chidi",203,306,"2024-03-16",28,8.0,1500]
   [1007,"Lagos","LOS","Ada",201,307,"2024-03-17",80,12.4,5500]
   [1008,"Abuja","ABJ","Bayo",202,308,"2024-03-17",31,9.2,3800]
   variant orders_messy: 5 ops; planted: iss_city_case_1004(inconsistent_category); iss_city_case_1007(inconsistent_category); iss_dist_string(wrong_type); iss_missing_dt(missing_value); iss_duplicate_1003(duplicate_row)

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Aggregate functions (COUNT, SUM, AVG, MIN, MAX); Apply transform; CASE expressions for conditional logic in queries; COALESCE for fallback values and NULL handling; Common SQL string functions for cleaning text; Concat stacking; DISTINCT for de-duplication; Exporting cleaned data (to_csv); GROUP BY grouping semantics; Grouping and aggregation (groupby); HAVING clause for filtering aggregated groups; Limiting results (LIMIT/OFFSET); Logical operators (AND, OR, NOT) in filtering; Melt reshaping; Merge join; NULL handling (IS NULL / IS NOT NULL); Pivot table reshaping; Relational database and table structure basics; SELECT statement fundamentals (columns, aliasing); SQL date/time extraction and arithmetic; SQL formatting/naming conventions per style guide; SQL type casting and conversion; Sorting results with ORDER BY (ASC/DESC); Table and column aliasing for readability; UNION and UNION ALL for stacking compatible query results; WHERE clause filtering and comparison operators

## LESSON, in learner order

### s01 · explainer · Replacing values element-by-element with .map()  [reward 3]
Map substitution — Every order in the SwiftDrop dataset carries a three-letter city code. .map() lets you swap each code for its full city name in one line.
(definition) `Series.map()` accepts a Python function that takes a single value and returns a single value, then applies it to every element of the Series. Define `def to_upper(code): return code.upper()` and call `orders["city_code"].map(to_upper)` — every city code in the column is uppercased in one pass. ⟦A.f1 A:tb1⟧
(mechanism) `Series.map()` also accepts a **dict** or another **Series** as a mapping correspondence. `orders["city_code"].map({"LOS": "Lagos", "ABJ": "Abuja", "KAN": "Kano"})` replaces each three-letter code with its full city name — no loop, no conditional logic. ⟦A.f2 A:tb2⟧
[BEFORE_AFTER] city_code column (LOS/ABJ/KAN) mapped to full city names (Lagos/Abuja/Kano) using a dict lookup.
  before:
[TABLE ds_orders cols=['order_id', 'city_code'] tags=city_code:codes to replace] caption: orders — city_code column holds three-letter codes
  after:
[CODE python]
city_lookup = {"LOS": "Lagos", "ABJ": "Abuja", "KAN": "Kano"}
orders["city_name"] = orders["city_code"].map(city_lookup)
print(orders[["order_id", "city_code", "city_name"]].head())
  annotations: ['Dict maps each code to its full city name', '.map(city_lookup) substitutes every code in one call']

### s02 · check · Recoding values with a dict mapping  [reward 2]
Quick check — Confirm you can identify the correct way to substitute Series values using a dict.
QUESTION [choice, intro, grading=client] You have a Series `names` with values `['alice', 'bob', 'charlie']` and a function `to_upper` that converts a string to uppercase. What does `names.map(to_upper)` return?
  ✔ a: A Series with `['ALICE', 'BOB', 'CHARLIE']`
  ✘ b: A Series with `['alice', 'bob', 'charlie']` (unchanged)
      why: Not quite. `.map(function)` applies the function to each element, transforming the values.
  ✘ c: An error, because `.map()` only accepts dictionaries
      why: Actually, `.map()` accepts both dictionaries and functions. When given a function, it applies that function to each element.
  ✘ d: A single uppercase string `'ALICEBOBCHARLIE'`
      why: No. `.map()` applies the function element-wise, returning a Series of the same length, not a single concatenated string.
  feedback✔: Correct! `.map()` applies the function to each element in the Series.  feedback✘: Not quite. Review how the operation works.  hints: ['Think about what happens when you pass a function to `.map()` - does it apply the function to each element?']  remediation→r01
  MEASURES: A:map_series_with_function(f1)   anchors=[]
  taught-before-tested: A.f1←s01

### s03 · hands_on · Map city codes to full names  [reward 5]
Practice — Use .map() with a dict to replace city_code values in the SwiftDrop orders table.
QUESTION [code_exercise, core, grading=client] The `orders` DataFrame has a `city_code` column with three-letter codes ('LOS', 'ABJ', 'KAN'). Use `.map(city_lookup)` to create a new column `city_name` with the full city names, then print the `city_name` column.

The lookup dict is already defined: `city_lookup = {'LOS': 'Lagos', 'ABJ': 'Abuja', 'KAN': 'Kano'}`.

Use only `df['col'].map(dict)`, `df['new'] = ...`, and `print()`.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=["df['col'].map(function)", "df['col'].map(dict)", "df['new'] = ...", 'print()'] blocked=4 items
  file solution.py [editable]:
import pandas as pd

orders = pd.read_csv('orders.csv')

city_lookup = {'LOS': 'Lagos', 'ABJ': 'Abuja', 'KAN': 'Kano'}
col_in = 'city_code'
col_out = 'city_name'

# Use .map() with city_lookup to create orders[col_out] from orders[col_in]

print(orders[col_out])

  SOLUTION solution.py:
import pandas as pd

orders = pd.read_csv('orders.csv')

city_lookup = {'LOS': 'Lagos', 'ABJ': 'Abuja', 'KAN': 'Kano'}
col_in = 'city_code'
col_out = 'city_name'

orders[col_out] = orders[col_in].map(city_lookup)

print(orders[col_out])

  test t1 (dataframe_equals, visible=True): {"expr":"orders[['city_name']]","expected":{"columns":["city_name"],"rows":[["Lagos"],["Abuja"],["Kano"],["Lagos"],["Abuja"],["Kano"],["Lagos"],["Abuja"],["Kano"],["Lagos"],["Abuja"],["Kano"],["Lagos"],["Abuja"]]}} | on-fail: The city_name column should contain the full city names mapped from city_code.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"add0e4df26bbfc3eb542aa500af2036673dae3da08f0511748c547ff3452e1e0","tests_passed":1}
  feedback✔: Perfect! You used `.map()` to substitute city codes with full names.  feedback✘: Not quite. Make sure you use `.map(city_lookup)` to create the city_name column.  hints: ["Use `orders['city_name'] = orders['city_code'].map(city_lookup)` to create the new column."]  remediation→r01
  MEASURES: A:recode_values_with_dict_mapping(f2)   anchors=['practice', 'assessment:recode_values_with_dict_mapping']
  taught-before-tested: A.f2←s01

### s04 · explainer · Running a custom function across rows or columns with .apply()  [reward 3]
Apply transform — When you need logic that spans multiple columns — like labelling an order 'fast' or 'slow' based on its delivery time — .apply() runs your function once per row.
(practical_context) Suppose you want to label every SwiftDrop order "fast" or "slow" based on its delivery time, using a rule you write yourself. `Series.map()` works on one column at a time, but this rule needs to read `delivery_time_minutes` and write a new column — that's a row-level operation. ⟦B.f1 B:tb1⟧
(definition) `DataFrame.apply()` applies an arbitrary function along an axis of the DataFrame, operating on each **column** by default (`axis=0`), or on each **row** when `axis=1`. Write `def label_speed(row): return 'slow' if row['delivery_time_minutes'] > 25 else 'fast'`, then `orders.apply(label_speed, axis=1)` runs it once per row and returns one label per order. ⟦B.f1 B:tb2⟧
[PROCESS_FLOW: How .apply() traverses a DataFrame] nodes=['DataFrame\n(orders)', 'axis=?', 'axis=0 (default)\nFunction runs once\nper column', 'axis=1\nFunction runs once\nper row', 'One result\nper column', 'One result\nper row\n(e.g. speed_label)', 'Results collected\ninto a Series'] edges=[('df_in', 'axis_decision', None), ('axis_decision', 'col_path', '0'), ('axis_decision', 'row_path', '1'), ('col_path', 'col_result', None), ('row_path', 'row_result', None), ('col_result', 'combined', None), ('row_result', 'combined', None)] alt: A DataFrame feeds into an axis decision: axis=0 runs the function once per column producing one result per column; axis=1 runs it once per row producing one result per row. Both paths collect results into a Series.

### s05 · video · Applying a function across rows and columns
See it in action — Watch how axis=0 and axis=1 change what the function receives and what it returns.
[VIDEO Applying a function down columns or across rows] bridge-before: Watch what axis changes: 0 runs the function on each column, 1 runs it on each row. The clip sets axis=0 explicitly and never calls it the default. | bridge-after: Devspace states the default: apply works column by column unless axis=1. The clip's row-wise example returns one value per row, like the text's fast/slow label.
  - smPLY_5gVv4 190-354s facts=['f1'] label: DataFrame.apply() down columns with axis=0 and across rows with axis=1 | summary: Applies a function to a whole DataFrame rather than a single column. With axis=0, a small function that returns each column's mode runs once per column, so the result is one summary value per column. With axis=1, a different function that finds the longest item in each row (turning numbers into text first) runs once per row, and the results come back as what amounts to a new column.

### s06 · check · Applying a function across rows with axis=1  [reward 2]
Quick check — Confirm you understand what axis=1 does when you call .apply() on a DataFrame.
QUESTION [choice, core, grading=client] You want to create a new column `speed_label` that labels each order as 'slow' if `delivery_time_minutes > 25`, else 'fast'. You have a function `label_speed(row)` that reads `row['delivery_time_minutes']` and returns the label. Which approach is correct?
  ✔ opt_a: `orders['speed_label'] = orders.apply(label_speed, axis=1)`
      why: Correct. `axis=1` tells `.apply()` to pass each row to the function, so `label_speed` receives one row at a time and can read any column.
  ✘ opt_b: `orders['speed_label'] = orders['delivery_time_minutes'].apply(label_speed)`
      why: Not quite. `.apply()` on a Series passes individual values, not rows. To read multiple columns from a row, use `df.apply(function, axis=1)`.
  ✘ opt_c: `orders['speed_label'] = orders.apply(label_speed)`
      why: Without `axis=1`, `.apply()` operates on each column by default, not each row. Use `axis=1` to pass rows to the function.
  ✘ opt_d: `orders['speed_label'] = label_speed(orders)`
      why: The function expects a single row, not the entire DataFrame. Use `df.apply(label_speed, axis=1)` to apply it to each row.
  feedback✔: Exactly right. `axis=1` makes `.apply()` pass each row to the function.  feedback✘: Not quite. Review how `axis=1` changes what `.apply()` passes to the function.  hints: ['Think about which axis argument makes `.apply()` operate on rows instead of columns.']  remediation→r02
  MEASURES: B:apply_function_across_rows_with_axis_1(f1)   anchors=['assessment:apply_function_across_rows_with_axis_1']
  taught-before-tested: B.f1←s04

### s07 · hands_on · Label orders fast or slow with .apply()  [reward 5]
Practice — Write a function and use .apply(axis=1) to add a speed_label column to the SwiftDrop orders table.
QUESTION [code_exercise, core, grading=client] Use `.apply()` with `axis=1` to compute the combined delivery effort (sum of `delivery_time_minutes` and `distance_km`) for each order row-wise. Store the result in a new column `total_effort`, then print it.

`df` already holds only the two numeric columns. Apply the built-in `sum` to `df` with `axis=axis_val` and store the result in `orders[col]`.

Use only `df.apply(function, axis=1)`, `df['new'] = ...`, and `print()`.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=['def function(row): ...', 'df.apply(function, axis=1)', "df['new'] = ...", 'print()'] blocked=4 items
  file solution.py [editable]:
import pandas as pd

orders = pd.read_csv('orders.csv')
df = orders[['delivery_time_minutes', 'distance_km']]

col = 'total_effort'
axis_val = 1

# Apply sum row-wise (axis=axis_val) and store in orders[col]

print(orders[col])

  SOLUTION solution.py:
import pandas as pd

orders = pd.read_csv('orders.csv')
df = orders[['delivery_time_minutes', 'distance_km']]

col = 'total_effort'
axis_val = 1

# Apply sum row-wise (axis=axis_val) and store in orders[col]
orders[col] = df.apply(sum, axis=axis_val)

print(orders[col])

  test t1 (dataframe_equals, visible=True): {"expr":"orders[['total_effort']]","expected":{"columns":["total_effort"],"rows":[[22.2],[26.1],[27.5],[25.8],[33.3],[36.0],[92.4],[40.2],[23.9],[29.1],[43.0],[25.4],[33.6],[46.1]]}} | on-fail: The total_effort column should be the sum of delivery_time_minutes and distance_km for each row.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"5c3c66a329b4510dcd8a8a718edba66fe63c7bf6fafc613f98a5a3d6403dfbd4","tests_passed":1}
  feedback✔: Well done! You used `.apply(sum, axis=1)` to sum two columns row-wise.  feedback✘: Not quite. Make sure you use `df.apply(sum, axis=1)` where `df` holds only the two numeric columns.  hints: ['Pass the built-in `sum` function (no parentheses) as the first argument to `.apply()`.', 'Use `axis=axis_val` (which equals 1) to apply the function row-wise.']  remediation→r02
  MEASURES: B:apply_function_down_columns(f1)   anchors=['practice', 'assessment:apply_function_down_columns']
  taught-before-tested: B.f1←s04

### s08 · recap · Map substitution and apply — key takeaways  [reward 5]
Recap — Two tools for element-wise transformation: .map() for value substitution, .apply() for custom row or column logic.
(takeaway) `Series.map()` substitutes values element-by-element using a function, a dict, or another Series — ideal for recoding categories like city codes. `DataFrame.apply()` runs an arbitrary function along an axis: column-by-column by default, or row-by-row with `axis=1`. Use `apply()` when the logic needs to read across multiple columns of the same row. ⟦B.f1 B:tb3⟧
[UP NEXT] Up next: Concatenating and Merging DataFrames: Next you'll combine separate DataFrames — stacking monthly order tables row-wise with pd.concat(), and joining orders to a customers table on a shared key with merge().

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · How .map() uses a dict to substitute values — A dict passed to .map() acts as a lookup table — each key in the Series is replaced by its matching value in the dict.
(mechanism) `Series.map()` can substitute each value in the Series using a mapping correspondence that may be a function, a dict, or a Series. When you pass a dict, every element whose value matches a key is replaced by the corresponding dict value. Elements with no matching key become `NaN`. ⟦A.f2 A:tb2⟧
[BEFORE_AFTER] city_code values (LOS/ABJ/KAN) replaced with full city names (Lagos/Abuja/Kano) via dict lookup.
  before:
[CODE python]
# city_code column holds: 'LOS', 'ABJ', 'KAN'
print(orders["city_code"].head(3))
# LOS, ABJ, KAN
  annotations: ['Three-letter codes — not human-readable']
  after:
[CODE python]
city_lookup = {"LOS": "Lagos", "ABJ": "Abuja", "KAN": "Kano"}
orders["city_name"] = orders["city_code"].map(city_lookup)
print(orders["city_name"].head(3))
# Lagos, Abuja, Kano
  annotations: ['Dict: each code → full city name', '.map(dict) replaces every code in one call']
### r02 · What axis=1 means for .apply() — The axis argument tells .apply() which direction to travel — down columns or across rows.
(mechanism) `DataFrame.apply()` applies an arbitrary function along an axis of the DataFrame, operating on each column by default (`axis=0`), or on each row when `axis=1`. With `axis=1`, the function receives one row at a time as a Series, so it can read any column of that row. The return value becomes one element in the result Series — one label per order, for example. ⟦B.f1 B:tb2⟧
[BEFORE_AFTER] axis=0 passes each column to the function; axis=1 passes each row, enabling multi-column logic.
  before:
[CODE python]
# axis=0 (default): function receives one column at a time
def col_max(col):
    return col.max()

orders.apply(col_max)  # one max value per column
  annotations: ['axis=0: function sees each column as a Series']
  after:
[CODE python]
# axis=1: function receives one row at a time
def label_speed(row):
    return 'slow' if row['delivery_time_minutes'] > 25 else 'fast'

orders['speed_label'] = orders.apply(label_speed, axis=1)
  annotations: ['axis=1: function sees each row — can read any column']

## OTHER CONTENT (fields without a dedicated renderer)
· nodes.label: axis=0 (default)
Function runs once
per column
· nodes.label: axis=1
Function runs once
per row
· nodes.label: One result
per column
· nodes.label: One result
per row
(e.g. speed_label)
· nodes.label: Results collected
into a Series

=========

# EVALUATOR PACKET — Pivot Tables and Exporting to CSV (tile_pandas_pivot_export)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.pivot_table_reshaping — Pivot table reshaping
B = pandas.export_to_csv — Exporting cleaned data (to_csv)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

## SOURCE FACTS — A (pandas.pivot_table_reshaping)   objective: Reshape long-format data into a wide summary table using pivot_table.
A.f1: pivot_table() reshapes data by turning the distinct values of one column into new columns, and unlike plain pivot(), it can handle duplicate index/column combinations by aggregating the numeric values.   [sources: pandas_docs_reshaping#pivot-table, pandas_docs_reshaping#pivot]
A.f2: pivot_table() takes index, columns, and values arguments: index sets the rows of the output table, columns sets the new columns, and values selects which column(s) to aggregate into the table.   [sources: pandas_docs_reshaping#pivot-table]
A.f3: pivot_table() combines rows that share the same index/column values using aggfunc, which defaults to 'mean'; passing aggfunc='sum' (or another function) changes how those values are combined.   [sources: pandas_docs_pivot_table_api, pandas_docs_reshaping#pivot-table]
PRACTICE ANCHOR (live_code): Pivot a long sales-transactions table into a wide table with products as rows and months as columns.  SUCCESS: The printed wide table has one row per product, one column per month, and each cell holds the aggregated sales for that product and month.
ASSESSMENT ANCHOR: build_pivot_table_from_index_columns_values facts=['f1', 'f2']
ASSESSMENT ANCHOR: change_pivot_aggfunc facts=['f3']

## SOURCE FACTS — B (pandas.export_to_csv)   objective: Export a cleaned DataFrame to a CSV file using to_csv, with or without writing the index column as required.
B.f1: The to_csv() method on a Series or DataFrame writes its contents to a CSV file; the destination path or buffer is its only required argument.   [sources: pandas_docs_io#writing-to-csv-format]
B.f2: to_csv()'s index argument controls whether the row (index) labels are written to the file; it defaults to True, and passing index=False omits them.   [sources: pandas_docs_io#writing-to-csv-format]
PRACTICE ANCHOR (live_code): Export a cleaned DataFrame to a CSV file without writing the index column.  SUCCESS: A CSV file exists at the given path with the DataFrame's columns and rows and no extra column of index numbers.
ASSESSMENT ANCHOR: write_dataframe_to_csv facts=['f1']
ASSESSMENT ANCHOR: control_index_column_in_output facts=['f2']

## DATA ASSETS USED
ds_monthly_long: Monthly Deliveries by City (Long) — columns: city(categorical), month(categorical), deliveries(numerical)
   ["Lagos","jan_deliveries",142]
   ["Lagos","feb_deliveries",138]
   ["Lagos","mar_deliveries",155]
   ["Abuja","jan_deliveries",98]
   ["Abuja","feb_deliveries",104]
   ["Abuja","mar_deliveries",110]
   ["Kano","jan_deliveries",76]
   ["Kano","feb_deliveries",81]
ds_orders: SwiftDrop Orders — columns: order_id(identifier,digits-as-label), city(categorical), city_code(categorical), courier(categorical), driver_id(identifier,digits-as-label), customer_id(identifier,digits-as-label), pickup_date(datetime), delivery_time_minutes(numerical), distance_km(numerical), order_value(numerical)
   [1001,"Lagos","LOS","Ada",201,301,"2024-03-14",18,4.2,2500]
   [1002,"Abuja","ABJ","Bayo",202,302,"2024-03-14",20,6.1,3100]
   [1003,"Kano","KAN","Chidi",203,303,"2024-03-15",22,5.5,1800]
   [1004,"Lagos","LOS","Ada",201,304,"2024-03-15",22,3.8,2200]
   [1005,"Abuja","ABJ","Bayo",202,305,"2024-03-16",26,7.3,4000]
   [1006,"Kano","KAN","Chidi",203,306,"2024-03-16",28,8.0,1500]
   [1007,"Lagos","LOS","Ada",201,307,"2024-03-17",80,12.4,5500]
   [1008,"Abuja","ABJ","Bayo",202,308,"2024-03-17",31,9.2,3800]
   variant orders_messy: 5 ops; planted: iss_city_case_1004(inconsistent_category); iss_city_case_1007(inconsistent_category); iss_dist_string(wrong_type); iss_missing_dt(missing_value); iss_duplicate_1003(duplicate_row)
ds_product_sales: Product Sales by Month (Long) — columns: product(categorical), month(categorical), sales(numerical)
   ["Envelope","Jan",4500]
   ["Envelope","Jan",3200]
   ["Envelope","Feb",5100]
   ["Envelope","Mar",4800]
   ["Parcel","Jan",8200]
   ["Parcel","Feb",7600]
   ["Parcel","Feb",9100]
   ["Parcel","Mar",8800]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Aggregate functions (COUNT, SUM, AVG, MIN, MAX); Basic normalization concepts (avoiding redundancy); CASE expressions for conditional logic in queries; COALESCE for fallback values and NULL handling; Common SQL string functions for cleaning text; DISTINCT for de-duplication; Entities and tables as models of real-world objects; Exporting cleaned data (to_csv); Foreign keys and referential integrity; GROUP BY grouping semantics; HAVING clause for filtering aggregated groups; Limiting results (LIMIT/OFFSET); Logical operators (AND, OR, NOT) in filtering; Many-to-many relationships and junction/bridge tables; NULL handling (IS NULL / IS NOT NULL); One-to-many relationships; Primary keys; Relational database and table structure basics; SELECT statement fundamentals (columns, aliasing); SQL date/time extraction and arithmetic; SQL formatting/naming conventions per style guide; SQL type casting and conversion; Sorting results with ORDER BY (ASC/DESC); Table and column aliasing for readability; UNION and UNION ALL for stacking compatible query results; WHERE clause filtering and comparison operators

## LESSON, in learner order

### s01 · explainer · Spreading long data into a wide grid with pivot_table()  [reward 3]
Pivot table — The long deliveries table has one row per city-month. pivot_table() spreads it back into a wide grid — cities as rows, months as columns — and handles duplicate cells automatically.
(definition) `pivot_table()` reshapes data by turning the distinct values of one column into new columns. Unlike plain `pivot()`, it can handle duplicate index/column combinations by aggregating the numeric values — so it won't raise an error if two rows share the same city and month. ⟦A.f1 A:tb2⟧
(syntax) `pivot_table()` takes `index`, `columns`, and `values` arguments: `index` sets the rows of the output table, `columns` sets the new columns, and `values` selects which column to aggregate. `long_deliveries.pivot_table(index="city", columns="month", values="deliveries")` puts each city on its own row, each month as its own column, and the delivery counts as the values filling the grid. ⟦A.f2 A:tb3⟧
[BEFORE_AFTER] Long table (8 rows × 3 columns) pivoted to wide format (3 rows × 3 month columns) with city as index.
  before:
[TABLE ds_monthly_long cols=['city', 'month', 'deliveries'] ] caption: long_deliveries — one row per city-month combination
  after:
[CODE python]
wide = long_deliveries.pivot_table(
    index='city',
    columns='month',
    values='deliveries'
)
print(wide)
  annotations: ["index='city' → cities become rows", "columns='month' → month values become column headers", "values='deliveries' → delivery counts fill the grid"]

### s02 · video · Building a pivot table from long data
See it in action — Watch pivot_table() spread city-month rows into a wide grid and see how aggfunc changes the result.
[VIDEO Long to wide with pivot_table] bridge-before: Watch the three roles: index sets the rows, columns sets the new columns, values is what gets aggregated. Clip 1 uses sum and clip 2 the default mean. Clip 2 has a fiddly dropna(thresh=...) detour. | bridge-after: Neither clip contrasts pivot_table with plain pivot(). Devspace notes that pivot_table can aggregate duplicate index and column combinations, which pivot() cannot.
  - JnXZz5y1Eco 22-211s facts=['f1', 'f2'] label: pivot_table with index, columns, values and aggfunc='sum' on sales profit | summary: Describes a pivot table as a way to summarize, group and analyze large data with sum, mean or count, in one line. On a store-sales table, pivot_table(index='region', columns='sub_category', values='profit', aggfunc='sum') returns one row per region, one column per sub-category, and the total profit in each region-and-sub-category cell, so groups compare easily. The clip names index, columns and aggfunc as the main parameters.
  - ETQXKwM6YMY 172-475s facts=['f1', 'f2', 'f3'] label: pivot_table of average height by year and team, then aggfunc changed from the mean default to max | summary: Poses the question of the average height of athletes per year and per country. pivot_table(index='year', columns='team', values='height') makes the distinct years the rows and the distinct teams the columns, with average heights in the cells and lots of NaN where a combination doesn't exist. dropna with a thresh argument is used to trim the sparse table, and pivoting by sport instead gives a smaller, easier-to-read table. Asking for aggfunc='max' instead of the default mean gives the tallest height in each cell.

### s03 · explainer · Controlling how duplicate cells are combined with aggfunc  [reward 2]
Aggregation in pivot_table — When two rows share the same index and column values, pivot_table() must combine them. aggfunc controls how.
(mechanism) `pivot_table()` combines rows that share the same index/column values using `aggfunc`, which defaults to `'mean'`. Passing `aggfunc='sum'` (or another function) changes how those values are combined — so if a city had two rows for the same month, the default call would average them instead of erroring, and adding `aggfunc='sum'` would total them instead. ⟦A.f3 A:tb4⟧

### s04 · check · Changing the pivot aggregation function  [reward 2]
Quick check — Confirm you know which argument to pivot_table() controls how duplicate cells are combined.
QUESTION [choice, core, grading=client] You have a long-format table with duplicate product-month combinations. You want to pivot it so each cell shows the total sales (sum) for that product and month. Which `aggfunc` should you use?
  ✔ opt_a: `aggfunc='sum'`
      why: Correct. `aggfunc='sum'` combines duplicate rows by summing their values.
  ✘ opt_b: `aggfunc='mean'`
      why: `aggfunc='mean'` computes the average, not the total. Use `aggfunc='sum'` to get the total sales.
  ✘ opt_c: `aggfunc='count'`
      why: `aggfunc='count'` counts the number of rows, not the sum of sales. Use `aggfunc='sum'` to get the total sales.
  ✘ opt_d: No `aggfunc` needed; `pivot_table()` sums by default
      why: The default `aggfunc` is 'mean', not 'sum'. To get totals, pass `aggfunc='sum'`.
  feedback✔: Exactly right. `aggfunc='sum'` gives you totals.  feedback✘: Not quite. Review which `aggfunc` computes totals.  hints: ['Think about which aggregation function adds up all the values for each group.']  remediation→r01
  MEASURES: A:change_pivot_aggfunc(f3)   anchors=['assessment:change_pivot_aggfunc']
  taught-before-tested: A.f3←s03

### s05 · hands_on · Build a pivot table from the long deliveries data  [reward 5]
Practice — Use pivot_table() with index, columns, and values to reshape long_deliveries into a wide city × month grid.
QUESTION [code_exercise, core, grading=client] The `product_sales` DataFrame has columns `product`, `month`, and `sales`, with some duplicate product-month rows. Use `pivot_table()` to reshape it to wide format with `index='product'`, `columns='month'`, `values='sales'`, and `aggfunc='sum'`. Print the result.

The result should have one row per product, one column per month, and each cell holding the total sales.

Use only `df.pivot_table(index=..., columns=..., values=...)`, `aggfunc='sum'`, `aggfunc='mean'`, and `print()`.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=['df.pivot_table(index=..., columns=..., values=...)', "aggfunc='sum'", "aggfunc='mean'", 'print()'] blocked=5 items
  file solution.py [editable]:
import pandas as pd

product_sales = pd.read_csv('product_sales.csv')
df = product_sales

index_col = 'product'
cols = 'month'
vals = 'sales'
func = 'sum'

# Create a pivot table: index=index_col, columns=cols, values=vals, aggfunc=func
# Store in result

print(result)

  SOLUTION solution.py:
import pandas as pd

product_sales = pd.read_csv('product_sales.csv')
df = product_sales

index_col = 'product'
cols = 'month'
vals = 'sales'
func = 'sum'

result = df.pivot_table(index=index_col, columns=cols, values=vals, aggfunc=func)

print(result)

  test t1 (dataframe_equals, visible=True): {"expr":"df.pivot_table(index='product', columns='month', values='sales', aggfunc='sum').reset_index()","expected":{"columns":["product","Feb","Jan","Mar"],"rows":[["Document",2400,2100,4200],["Envelope",5100,7700,4800],["Parcel",16700,8200,8800]]}} | on-fail: The pivot table should have one row per product, one column per month, with summed sales.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"f57c14d702ed31518a0bc736a62e338fc494d781bf06485f8d97c2a360f6a5bf","tests_passed":1}
  feedback✔: Perfect! You reshaped the long table to wide format with aggregation.  feedback✘: Not quite. Make sure you use `aggfunc='sum'` to total the sales for each product-month.  hints: ["Use `product_sales.pivot_table(index='product', columns='month', values='sales', aggfunc='sum')` to reshape."]
  MEASURES: A:build_pivot_table_from_index_columns_values(f1,f2)   anchors=['practice', 'assessment:build_pivot_table_from_index_columns_values']
  taught-before-tested: A.f1←s01; A.f2←s01

### s06 · explainer · Writing a DataFrame to a CSV file with to_csv()  [reward 3]
Exporting data — Once the data is clean and shaped, to_csv() writes it to a file. One argument controls whether the row index is included.
(definition) The `to_csv()` method on a Series or DataFrame writes its contents to a CSV file; the destination path or buffer is its only required argument: `orders.to_csv("cleaned_orders.csv")` writes the full orders table to a file. ⟦B.f1 B:tb1⟧
(mechanism) `to_csv()`'s `index` argument controls whether the row labels are written to the file; it defaults to `True`. Passing `index=False` omits them: `orders.to_csv("cleaned_orders.csv", index=False)` writes the same file without an extra index column at the start. ⟦B.f2 B:tb2⟧
[SIDE_BY_SIDE] Pass index=False whenever the row index is just a default integer range and you don't want it as a column in the output file. left_label: With index (default) | right_label: Without index (index=False)
  left:
[CODE python]
orders.to_csv('cleaned_orders.csv')
# CSV starts with an extra column:
# ,order_id,city,delivery_time_minutes,...
# 0,1001,Lagos,18,...
# 1,1002,Abuja,20,...
  annotations: ['Leading comma = unnamed index column written to file']
  right:
[CODE python]
orders.to_csv('cleaned_orders.csv', index=False)
# CSV has no extra column:
# order_id,city,delivery_time_minutes,...
# 1001,Lagos,18,...
# 1002,Abuja,20,...
  annotations: ['No leading comma — index omitted from file']

### s07 · check · Controlling the index column in CSV output  [reward 2]
Quick check — Confirm you know which argument to to_csv() omits the row index from the output file.
QUESTION [choice, core, grading=client] You export a DataFrame to CSV with `orders.to_csv('output.csv')`. When you open the file, you see an extra column of row numbers (0, 1, 2, ...). How do you prevent this?
  ✔ opt_a: `orders.to_csv('output.csv', index=False)`
      why: Correct. `index=False` omits the row labels (index) from the output file.
  ✘ opt_b: `orders.to_csv('output.csv', header=False)`
      why: `header=False` omits the column names, not the index. Use `index=False` to omit the row numbers.
  ✘ opt_c: `orders.to_csv('output.csv', columns=False)`
      why: There is no `columns=False` parameter. Use `index=False` to omit the row numbers.
  ✘ opt_d: `orders.to_csv('output.csv', row_numbers=False)`
      why: There is no `row_numbers` parameter. Use `index=False` to omit the index.
  feedback✔: Exactly right. `index=False` omits the index from the CSV.  feedback✘: Not quite. Review which parameter controls whether the index is written.  hints: ['Think about which parameter controls whether the row labels are written to the file.']  remediation→r02
  MEASURES: B:control_index_column_in_output(f2)   anchors=['assessment:control_index_column_in_output']
  taught-before-tested: B.f2←s06

### s08 · hands_on · Write a DataFrame to CSV with and without the index  [reward 5]
Practice — Use to_csv() to save the orders table, then try index=False to see the difference in the output file.
QUESTION [code_exercise, core, grading=client] The `orders` DataFrame is loaded. Export it to a CSV file named `cleaned_orders.csv` with `index=False` (no row numbers), then read it back with `pd.read_csv()` and print it to verify.

Use only `df.to_csv(path)`, `df.to_csv(path, index=False)`, `pd.read_csv(path)`, and `print()`.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=['df.to_csv(path)', 'df.to_csv(path, index=False)', 'pd.read_csv(path) to check', 'print()'] blocked=4 items
  file solution.py [editable]:
import pandas as pd

orders = pd.read_csv('orders.csv')
df = orders

out_path = 'cleaned_orders.csv'
write_index = False

# Export df to out_path with index=write_index
# Then read it back into result and print

print(result)

  SOLUTION solution.py:
import pandas as pd

orders = pd.read_csv('orders.csv')
df = orders

out_path = 'cleaned_orders.csv'
write_index = False

df.to_csv(out_path, index=write_index)

result = pd.read_csv(out_path)

print(result)

  test t1 (value_equals, visible=True): {"expr":"len(pd.read_csv('cleaned_orders.csv'))","expected":14} | on-fail: The CSV should have 14 rows (the same as the original orders DataFrame).
  test t2 (value_equals, visible=True): {"expr":"pd.read_csv('cleaned_orders.csv')['order_id'].iloc[0]","expected":1001} | on-fail: The first order_id should be 1001.
  test t3 (value_equals, visible=None): {"expr":"pd.read_csv('cleaned_orders.csv')['customer_id'].iloc[0]","expected":301} | on-fail: The CSV should preserve the original data values.
  test t4 (value_equals, visible=True): {"expr":"int(pd.read_csv('cleaned_orders.csv')['order_value'].sum())","expected":43200} | on-fail: The total order_value in the exported CSV should be 43200. Make sure you export the full DataFrame with to_csv().
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"0914c941cf516ce3890fbb0c6ac02b15e7c032a7a0f09af8e5fa93a742e27c04","tests_passed":4}
  feedback✔: Perfect! You exported the DataFrame without the index column.  feedback✘: Not quite. Make sure you use `index=False` to omit the row numbers.  hints: ["Use `orders.to_csv('cleaned_orders.csv', index=False)` to export without the index."]  remediation→r02
  MEASURES: B:write_dataframe_to_csv(f1); B:control_index_column_in_output(f2)   anchors=['practice', 'assessment:write_dataframe_to_csv', 'assessment:control_index_column_in_output']
  taught-before-tested: B.f1←s06; B.f2←s06

### s09 · recap · Pivot tables and CSV export — key takeaways  [reward 5]
Recap — pivot_table() spreads long data into a wide grid and handles duplicates; to_csv() writes the result to a file.
(takeaway) `pivot_table()` spreads long data wider by turning one column's values into new column headers, aggregating whenever more than one row lands in the same cell. Pass `index`, `columns`, and `values` to define the shape; use `aggfunc='sum'` (or another function) to control how duplicates are combined. Once the table is ready, `to_csv(path)` writes it to a file — add `index=False` to omit the row labels from the output. ⟦A.f1 A.f2 A.f3 B.f1 B.f2 A:tb5 B:tb1 B:tb2⟧
[UP NEXT] Up next: SQL and Relational Data: Next you'll move from pandas to SQL — querying relational tables with SELECT, WHERE, and GROUP BY to answer the same kinds of questions you've been solving in Python.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · How aggfunc controls duplicate cell values in pivot_table() — When two rows share the same index and column values, pivot_table() must combine them. aggfunc tells it how.
(mechanism) `pivot_table()` combines rows that share the same index/column values using `aggfunc`, which defaults to `'mean'`. Passing `aggfunc='sum'` changes how those values are combined — so if a city had two rows for the same month, the default call would average them instead of erroring, and adding `aggfunc='sum'` would total them instead. ⟦A.f3 A:tb4⟧
[BEFORE_AFTER] Default aggfunc='mean' averages duplicate cells; aggfunc='sum' totals them instead.
  before:
[CODE python]
# Default aggfunc='mean'
wide = long_deliveries.pivot_table(
    index='city', columns='month', values='deliveries'
)
# Duplicate city-month rows are averaged
  annotations: ["aggfunc='mean' is the default — duplicates averaged"]
  after:
[CODE python]
# aggfunc='sum' totals duplicate rows instead
wide = long_deliveries.pivot_table(
    index='city', columns='month', values='deliveries',
    aggfunc='sum'
)
# Duplicate city-month rows are summed
  annotations: ["aggfunc='sum' → duplicates totalled, not averaged"]
### r02 · The index argument in to_csv() — By default to_csv() writes the row index as an extra column. index=False omits it.
(mechanism) `to_csv()`'s `index` argument controls whether the row (index) labels are written to the file; it defaults to `True`, and passing `index=False` omits them. When the index is just a default integer range (0, 1, 2, …), it adds an unnamed column to the CSV that most downstream tools don't expect — `index=False` prevents that. ⟦B.f2 B:tb2⟧
[BEFORE_AFTER] index=True (default) writes row labels as an extra column; index=False omits them.
  before:
[CODE python]
# index=True (default) — row labels written to file
orders.to_csv('cleaned_orders.csv')
# First column in file: 0, 1, 2, ... (the index)
  annotations: ["Extra unnamed column — the DataFrame's row index"]
  after:
[CODE python]
# index=False — row labels omitted
orders.to_csv('cleaned_orders.csv', index=False)
# File starts directly with order_id, city, ...
  annotations: ['No extra column — cleaner output for downstream tools']