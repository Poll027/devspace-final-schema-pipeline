# EVALUATOR PACKET — Mapping and Applying Transformations (tile_pandas_map_apply)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.map_substitution — Map substitution
B = pandas.apply_transform — Apply transform

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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

### s03 · hands_on · Map city codes to full names  [reward 5]
Practice — Use .map() with a dict to replace city_code values in the SwiftDrop orders table.

### s04 · explainer · Running a custom function across rows or columns with .apply()  [reward 3]
Apply transform — When you need logic that spans multiple columns — like labelling an order 'fast' or 'slow' based on its delivery time — .apply() runs your function once per row.
(practical_context) Suppose you want to label every SwiftDrop order "fast" or "slow" based on its delivery time, using a rule you write yourself. `Series.map()` works on one column at a time, but this rule needs to read `delivery_time_minutes` and write a new column — that's a row-level operation. ⟦B.f1 B:tb1⟧
(definition) `DataFrame.apply()` applies an arbitrary function along an axis of the DataFrame, operating on each **column** by default (`axis=0`), or on each **row** when `axis=1`. Write `def label_speed(row): return 'slow' if row['delivery_time_minutes'] > 25 else 'fast'`, then `orders.apply(label_speed, axis=1)` runs it once per row and returns one label per order. ⟦B.f1 B:tb2⟧
[PROCESS_FLOW: How .apply() traverses a DataFrame] nodes=['DataFrame\n(orders)', 'axis=?', 'axis=0 (default)\nFunction runs once\nper column', 'axis=1\nFunction runs once\nper row', 'One result\nper column', 'One result\nper row\n(e.g. speed_label)', 'Results collected\ninto a Series'] edges=[('df_in', 'axis_decision', None), ('axis_decision', 'col_path', '0'), ('axis_decision', 'row_path', '1'), ('col_path', 'col_result', None), ('row_path', 'row_result', None), ('col_result', 'combined', None), ('row_result', 'combined', None)] alt: A DataFrame feeds into an axis decision: axis=0 runs the function once per column producing one result per column; axis=1 runs it once per row producing one result per row. Both paths collect results into a Series.

### s05 · video · Applying a function across rows and columns
See it in action — Watch how axis=0 and axis=1 change what the function receives and what it returns.
[VIDEO ] bridge-before:  | bridge-after: 

### s06 · check · Applying a function across rows with axis=1  [reward 2]
Quick check — Confirm you understand what axis=1 does when you call .apply() on a DataFrame.

### s07 · hands_on · Label orders fast or slow with .apply()  [reward 5]
Practice — Write a function and use .apply(axis=1) to add a speed_label column to the SwiftDrop orders table.

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

# EVALUATOR PACKET — Grouping, Aggregating, and Reshaping with melt (tile_pandas_groupby_melt)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.groupby_aggregation — Grouping and aggregation (groupby)
B = pandas.melt_reshaping — Melt reshaping

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · explainer · Calling groupby and choosing an aggregation  [reward 2]
Groupby syntax — One call chains the grouping key with the aggregation method. You can compute one statistic or several at once.
(syntax) Call `df.groupby(key)` then chain an aggregation method such as `.sum()` or `.mean()` on the DataFrame or a selected column. Use `.agg([...])` to compute several aggregations at once. By default, the group keys become the index of the result: `orders.groupby("city")["delivery_time_minutes"].mean()` returns one average per city with city names as the index; `orders.groupby("city")["delivery_time_minutes"].agg(["mean", "sum"])` computes both in one call. ⟦A.f3 A:tb4⟧

### s04 · check · Describing the split-apply-combine process  [reward 2]
Quick check — Confirm you can describe what groupby does in terms of split, apply, and combine.

### s05 · hands_on · Aggregate delivery times and order values by city  [reward 5]
Practice — Use groupby to compute the mean delivery time and total order value per city from the SwiftDrop orders table.

### s06 · explainer · Turning a wide table into a long one with melt()  [reward 3]
Melt reshaping — A wide summary table has one column per month. melt() unpivots those columns into rows — one row per city-month combination.
(practical_context) The SwiftDrop monthly deliveries table has one row per city and separate columns `jan_deliveries`, `feb_deliveries`, `mar_deliveries`. Many analysis tools and visualisation libraries expect one row per city-month combination instead — that's the long format. ⟦B.f1 B:tb1⟧
(definition) `melt()` reshapes a DataFrame from wide to long format: the columns listed as `id_vars` stay as identifier columns, while all other columns are unpivoted into two new columns — one holding the original column names and one holding their values. `city_deliveries.melt(id_vars=["city"])` keeps `city` as an identifier and turns the three month columns into two new columns. ⟦B.f1 B:tb2⟧
(mechanism) The default output column names are `variable` and `value`. Use `var_name` and `value_name` to rename them: `city_deliveries.melt(id_vars=["city"], var_name="month", value_name="deliveries")` gives the two new columns clearer names. ⟦B.f2 B:tb3⟧
[BEFORE_AFTER] Wide table (3 rows × 4 columns) melted to long format (8 rows × 3 columns) with id_vars=['city'], var_name='month', value_name='deliveries'.
  before:
[TABLE ds_monthly_wide cols=['city', 'jan_deliveries', 'feb_deliveries', 'mar_deliveries'] tags=jan_deliveries:will become rows, feb_deliveries:will become rows, mar_deliveries:will become rows] caption: Wide format — one column per month
  after:
[TABLE ds_monthly_long cols=['city', 'month', 'deliveries'] tags=month:former column names, deliveries:former column values] caption: Long format — one row per city-month, month column renamed via var_name='month'

### s07 · video · Reshaping wide to long with melt()
See it in action — Watch melt() unpivot month columns into rows and how var_name and value_name rename the output.
[VIDEO ] bridge-before:  | bridge-after: 

### s08 · check · Renaming melt output columns  [reward 2]
Quick check — Confirm you know which parameters rename the two new columns that melt() produces.

### s09 · hands_on · Melt the monthly deliveries table from wide to long  [reward 5]
Practice — Use melt() with id_vars, var_name, and value_name to reshape the city deliveries table.

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

# EVALUATOR PACKET — Concatenating and Merging DataFrames (tile_pandas_concat_merge)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.concat_stacking — Concat stacking
B = pandas.merge_join — Merge join

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
ds_drivers: SwiftDrop Drivers — columns: driver_id(identifier,digits-as-label), driver_name(categorical), vehicle(categorical), base_city(categorical)
   [201,"Ada Okafor","Motorcycle","Lagos"]
   [202,"Bayo Adeyemi","Van","Abuja"]
   [203,"Chidi Okonkwo","Motorcycle","Kano"]
   [204,"Dami Fashola","Van","Lagos"]
ds_jan_orders: January Orders — columns: order_id(identifier,digits-as-label), city(categorical), courier(categorical), delivery_time_minutes(numerical), order_value(numerical)
   [2001,"Lagos","Ada",18,2500]
   [2002,"Abuja","Bayo",22,3100]
   [2003,"Kano","Chidi",26,1800]
   [2004,"Lagos","Ada",31,2900]
   [2005,"Abuja","Bayo",19,3400]

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
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Choosing the concat axis  [reward 2]
Quick check — Confirm you know what axis=1 does when passed to pd.concat().

### s04 · hands_on · Stack the monthly order tables into one DataFrame  [reward 5]
Practice — Use pd.concat() to combine jan_orders, feb_orders, and mar_orders row-wise.

### s05 · explainer · Joining two DataFrames on a shared key with merge()  [reward 3]
Merge and join — Orders and driver details live in separate tables, linked by driver_id. merge() matches rows on that shared key and combines the columns.
(definition) `merge()` combines two DataFrames by matching values in a shared key column, specified with the `on` parameter: `orders.merge(drivers, on="driver_id")`. The result contains one row for every matched pair — columns from both tables side by side. ⟦B.f1 B:tb1 B:tb2⟧
(mechanism) The `how` parameter controls which keys are kept. `how='inner'` (the default) keeps only key values present in **both** DataFrames — a `driver_id` that appears in orders but not in drivers won't survive an inner merge, and vice versa. ⟦B.f2 B:tb3⟧
(mechanism) When a key value does not appear in one of the two DataFrames, the corresponding values contributed by that DataFrame in the joined result are `NA`. This is what happens once a join type other than the default inner merge is used and unmatched keys are allowed to stay in the result. ⟦B.f3 B:tb4⟧
[DIAGRAM: Join types — which keys survive] nodes=['Left only\n(orders keys\nnot in drivers)', 'Inner\n(keys in both)', 'Right only\n(drivers keys\nnot in orders)', "how='inner'\nkeeps only this", "how='left'\nkeeps left + inner", "how='outer'\nkeeps all three"] edges=[('inner_label', 'inner', None), ('left_label', 'left_only', None), ('left_label', 'inner', None), ('outer_label', 'left_only', None), ('outer_label', 'inner', None), ('outer_label', 'right_only', None)] alt: Venn diagram of two overlapping circles: left circle is orders keys, right circle is drivers keys. The overlap is the inner join. how='inner' keeps only the overlap; how='left' keeps the left circle and overlap; how='outer' keeps everything. Unmatched keys in the result get NA values from the missing side.

### s06 · video · Merging DataFrames on a shared key
See it in action — Watch merge() join orders to drivers and see how changing how= keeps or drops unmatched rows.
[VIDEO ] bridge-before:  | bridge-after: 

### s07 · explainer · Left, right, and outer joins  [reward 2]
Join types — Beyond the default inner join, three other how= values let you keep unmatched rows from one or both sides.
(mechanism) The `how` parameter also accepts `'left'` (keep all keys from the left DataFrame only), `'right'` (keep all keys from the right DataFrame only), and `'outer'` (keep the union of keys from both DataFrames). `orders.merge(drivers, on="driver_id", how="left")` keeps every order, filling in `NA` for driver details on any `driver_id` that merge can't find in the drivers table. ⟦B.f4 B:tb5⟧

### s08 · check · Merging on a shared key and choosing a join type  [reward 2]
Quick check — Confirm you can identify the correct merge call and the effect of the how= parameter.

### s09 · check · NA values for unmatched keys  [reward 2]
Quick check — Confirm you understand what happens to unmatched key values in a non-inner merge.

### s10 · hands_on · Join orders to customers and predict the inner merge result  [reward 5]
Practice — Use merge() to join the orders table to the customers table on customer_id, then explore what an inner join keeps.

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

# EVALUATOR PACKET — Pivot Tables and Exporting to CSV (tile_pandas_pivot_export)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.pivot_table_reshaping — Pivot table reshaping
B = pandas.export_to_csv — Exporting cleaned data (to_csv)

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

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
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · explainer · Controlling how duplicate cells are combined with aggfunc  [reward 2]
Aggregation in pivot_table — When two rows share the same index and column values, pivot_table() must combine them. aggfunc controls how.
(mechanism) `pivot_table()` combines rows that share the same index/column values using `aggfunc`, which defaults to `'mean'`. Passing `aggfunc='sum'` (or another function) changes how those values are combined — so if a city had two rows for the same month, the default call would average them instead of erroring, and adding `aggfunc='sum'` would total them instead. ⟦A.f3 A:tb4⟧

### s04 · check · Changing the pivot aggregation function  [reward 2]
Quick check — Confirm you know which argument to pivot_table() controls how duplicate cells are combined.

### s05 · hands_on · Build a pivot table from the long deliveries data  [reward 5]
Practice — Use pivot_table() with index, columns, and values to reshape long_deliveries into a wide city × month grid.

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

### s08 · hands_on · Write a DataFrame to CSV with and without the index  [reward 5]
Practice — Use to_csv() to save the orders table, then try index=False to see the difference in the output file.

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