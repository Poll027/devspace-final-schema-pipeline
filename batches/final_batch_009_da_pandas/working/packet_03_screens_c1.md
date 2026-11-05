# EVALUATOR PACKET — Creating and Inspecting DataFrames (tile_pandas_creating_inspecting)
Tile summary: Build a DataFrame directly from Python data — a dict of lists or a list of dicts — then use head, shape, dtypes, info, and describe to get an immediate overview of what is inside.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.creating_dataframes — Creating DataFrames from dicts/lists/files
B = pandas.inspecting_dataframes — Inspecting data (head, info, describe, shape, dtypes)

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (pandas.creating_dataframes)   objective: Construct a DataFrame directly from Python data, such as a dict of lists or a list of dicts, rather than loading it from a file.
A.f1: A DataFrame can be constructed from a dict of equal-length lists, where each key becomes a column name and each list becomes that column's values; if no index is passed, the result uses a default range index.   [sources: pandas_docs_dsintro#from-dict-of-ndarrays-lists]
A.f2: A DataFrame can also be constructed from a list of dicts, where each dict becomes one row and the dict keys become the column names.   [sources: pandas_docs_dsintro#from-a-list-of-dicts]
note: TOC conflict: don't verify the result's shape here -- pandas.inspecting_dataframes, which teaches that, comes later and isn't in this concept's allowed knowledge.
note: TOC name says 'from dicts/lists/files' but the objective excludes loading from a file: file loading belongs to pandas.reading_data, so this bundle covers dict-of-lists and list-of-dicts only.
note: Practice anchor verifies by printing the table, not shape: shape arrives in pandas.inspecting_dataframes.
PRACTICE ANCHOR (live_code): Build a DataFrame from a dict of lists and print it to check the column names and row values.  SUCCESS: The printed table has one column per dict key, in the order given, with every list's values in its rows.
ASSESSMENT ANCHOR: build_dataframe_from_dict_of_lists facts=['f1']
ASSESSMENT ANCHOR: build_dataframe_from_list_of_dicts facts=['f2']

## SOURCE FACTS — B (pandas.inspecting_dataframes)   objective: Get an initial overview of a newly-loaded DataFrame using head, info, describe, shape, and dtypes.
B.f1: head() (and tail()) shows a small sample of the first (or last) rows of a Series or DataFrame; by default it shows five rows.   [sources: pandas_docs_basics#head-and-tail]
B.f2: The shape attribute reports a DataFrame's axis dimensions: the number of rows and the number of columns.   [sources: pandas_docs_basics#attributes-and-underlying-data]
B.f3: The dtypes attribute returns the data type of each column in a DataFrame.   [sources: pandas_docs_basics#dtypes]
B.f4: info() prints a concise summary of a DataFrame, including its columns and their data types, how many non-missing values each column has, and its memory usage.   [sources: pandas_docs_dataframe_info]
B.f5: describe() computes a quick statistical overview of a Series' values, or of each numeric column of a DataFrame, in a single call.   [sources: pandas_docs_basics#summarizing-data-describe]
note: Load and build examples now have this to build toward -- head/shape/dtypes/info/describe complete the picture that reading_data and creating_dataframes deliberately left open.
PRACTICE ANCHOR (live_code): Load a dataset and report its shape, column dtypes and a five-row preview before doing any analysis.  SUCCESS: The learner's output shows the row and column counts, a data type for each column, and the first five rows.
ASSESSMENT ANCHOR: preview_rows_with_head facts=['f1']
ASSESSMENT ANCHOR: report_rows_and_columns_with_shape facts=['f2']
ASSESSMENT ANCHOR: read_column_dtypes facts=['f3']
ASSESSMENT ANCHOR: read_info_summary facts=['f4']
ASSESSMENT ANCHOR: get_describe_overview facts=['f5']

## DATA ASSETS USED
img_inspect_overview: MISSING

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply transform; Boolean/conditional filtering; Computing descriptive statistics with pandas (describe, mean, median, std); Concat stacking; DISTINCT for de-duplication; Exporting cleaned data (to_csv); Grouping and aggregation (groupby); Handling missing data (isna, dropna, fillna); Inspecting data (head, info, describe, shape, dtypes); Logical operators (AND, OR, NOT) in filtering; Map substitution; Melt reshaping; Merge join; NULL handling (IS NULL / IS NOT NULL); Pivot table reshaping; Relational database and table structure basics; Removing duplicate rows; Renaming columns and index labels; SELECT statement fundamentals (columns, aliasing); Selecting rows/columns with loc/iloc; Sorting values; String cleaning with the .str accessor; Table and column aliasing for readability; Type conversion and dtype management (astype); WHERE clause filtering and comparison operators; Working with datetime data (to_datetime, date components)

## LESSON, in learner order

### s01 · explainer · Two ways to build a DataFrame from Python data  [reward 5]
Creating DataFrames — Not every DataFrame starts life as a file. When delivery data already exists as Python objects, you can build the table directly.
(example) Pass a **dict of equal-length lists** to `pd.DataFrame()` and each key becomes a column name; each list becomes that column's values. With no index argument the result uses a default range index: `orders = pd.DataFrame({"order_id": [1001, 1002, 1003], "city": ["Lagos", "Abuja", "Kano"]})`. ⟦A.f1 A:tb2⟧
(example) Alternatively, pass a **list of dicts** where each dict becomes one row and the dict keys become column names: `orders = pd.DataFrame([{"order_id": 1001, "city": "Lagos"}, {"order_id": 1002, "city": "Abuja"}])`. Both routes produce the same kind of table — pick whichever shape your data is already in. ⟦A.f2 A:tb3 A:tb4⟧
[SIDE_BY_SIDE] Both produce the same orders table — choose the shape that matches your existing Python data. left_label: Dict of lists (one key per column) | right_label: List of dicts (one dict per row)
  left:
[CODE python]
orders = pd.DataFrame({
    "order_id": [1001, 1002, 1003],
    "city":     ["Lagos", "Abuja", "Kano"],
})
  annotations: ['Each key → column name; each list → column values']
  right:
[CODE python]
orders = pd.DataFrame([
    {"order_id": 1001, "city": "Lagos"},
    {"order_id": 1002, "city": "Abuja"},
    {"order_id": 1003, "city": "Kano"},
])
  annotations: ['Each dict → one row; keys → column names']

### s02 · video · Building a DataFrame from Python data  [reward 3]
Creating DataFrames — See how a dict of lists becomes a DataFrame in a live coding session.
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Building a DataFrame from a list of dicts  [reward 5]
Quick check — Confirm you can identify what each dict contributes when you pass a list of dicts to pd.DataFrame.

### s04 · hands_on · Create a DataFrame two ways  [reward 10]
Hands-on — Build the same small orders table once from a dict of lists and once from a list of dicts, then confirm both produce the same result.

### s05 · explainer · Five methods that answer your first questions about a DataFrame  [reward 5]
Inspecting DataFrames — Before doing anything else with a newly loaded or built orders DataFrame, get an overview of what is actually in it.
(mechanism) `orders.head()` shows the first five delivery records by default — a quick sanity check that the data loaded correctly. `orders.shape` returns a tuple of (rows, columns), such as `(250, 10)` for 250 orders across 10 columns. ⟦B.f1 B.f2 B:tb2 B:tb3⟧
(mechanism) `orders.dtypes` returns the data type of each column — for example, that `delivery_time_minutes` holds integers and `city` holds text. `orders.info()` combines that dtype list with a count of non-missing values per column and the DataFrame's memory usage in one concise summary. ⟦B.f3 B.f4 B:tb4 B:tb5⟧
[ANNOTATED_IMAGE — unrendered type, raw] {"type":"annotated_image","block_id":"tile_pandas_creating_inspecting.s05.b3","asset_id":"img_inspect_overview","alt_text":"Five pandas inspection outputs on the SwiftDrop orders DataFrame: head() showing the first five rows, shape returning (250, 10), dtypes listing each column's type, info() showing non-null counts and memory, and describe() showing statistics for numeric columns — each labelled with the question it answers.","hotspots":[{"x":0.05,"y":0.08,"w":0.4,"h":0.18,"label":"head()","detail":"What do the first rows look like?"},{"x":0.55,"y":0.08,"w":0.4,"h":0.08,"label":"shape","detail":"How many rows and columns?"},{"x":0.55,"y":0.2,"w":0.4,"h":0.18,"label":"dtypes","detail":"What type is each column?"},{"x":0.05,"y":0.35,"w":0.4,"h":0.28,"label":"info()","detail":"How many non-missing values? How much memory?"},{"x":0.55,"y":0.35,"w":0.4,"h":0.28,"label":"describe()","detail":"What do the numbers look like statistically?"}],"lineage":{"concept_ids":["pandas.inspecting_dataframes"],"teaching_block_ids":["pandas.inspecting_dataframes#tb1","pandas.inspecting_dataframes#tb2","pandas.inspecting_dataframes#tb3","pandas.inspecting_dataframes#tb4","pandas.inspecting_dataframes#tb5"],"fact_ids":["pandas.inspecting_dataframes#f1","pandas.inspecting_dataframes#f2","pandas.inspecting_dataframes#f3","pandas.inspecting_dataframes#f4"],"anchors":["pandas.inspecting_dataframes#visual"]}}

### s06 · video · head, shape, dtypes, info, and describe in action  [reward 3]
Inspecting DataFrames — Watch each inspection method called on a real table and see what it returns.
[VIDEO ] bridge-before:  | bridge-after: 

### s07 · explainer · describe() — a statistical overview in one call  [reward 3]
Inspecting DataFrames — One method summarises all numeric columns at once.
(mechanism) `orders.describe()` computes a quick statistical overview of each numeric column — count, mean, std, min, quartiles, and max — in a single call. ⟦B.f5 B:tb6⟧

### s08 · check · shape and info  [reward 5]
Quick check — Test your understanding of what shape and info() each report about a DataFrame.

### s09 · check · describe() overview  [reward 5]
Quick check — Confirm what describe() computes and when to reach for it.

### s10 · hands_on · Inspect the orders DataFrame  [reward 10]
Hands-on — Call head() to preview the first rows, then use dtypes to read each column's type.

### s11 · recap · What you learned: creating and inspecting DataFrames  [reward 5]
Recap — Two construction routes, five inspection tools — here is the summary.
(takeaway) A DataFrame can be built from a **dict of equal-length lists** (one key per column) or a **list of dicts** (one dict per row). Both routes produce the same table — pick whichever shape your Python data is already in. ⟦A.f1 A.f2 A:tb4⟧
(takeaway) Five methods answer your first questions: `head()` previews rows, `shape` reports dimensions, `dtypes` lists column types, `info()` adds non-null counts and memory, and `describe()` gives a statistical overview of numeric columns — all in one call each. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb7⟧
[UP NEXT] Up next: Descriptive Statistics: Next you will compute descriptive statistics — mean, median, std, and more — directly on DataFrame columns using pandas methods.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · List of dicts: each dict is one row — When you pass a list of dicts, each dict contributes exactly one row.
(example) In `pd.DataFrame([{"order_id": 1001, "city": "Lagos"}, {"order_id": 1002, "city": "Abuja"}])`, the first dict becomes row 0 and the second becomes row 1. The dict keys — `order_id` and `city` — become the column names. Contrast this with the dict-of-lists form, where each key maps to a whole column. ⟦A.f2 A:tb3⟧
### r02 · shape vs info() — dimensions vs column detail — shape tells you how big the table is; info() tells you what is inside each column.
(mechanism) `orders.shape` returns a tuple of (rows, columns) — for example `(250, 10)`. It answers only: how many rows and how many columns? `orders.info()` prints a concise summary that includes column names, their data types, how many non-missing values each column has, and the DataFrame's memory usage. Use `shape` for a quick size check; use `info()` when you need to see missing-value counts. ⟦B.f2 B.f4 B:tb3 B:tb5⟧
### r03 · describe() — one call, many statistics — describe() computes a statistical overview of numeric columns in a single call.
(example) `orders.describe()` computes a quick statistical overview of each numeric column — count, mean, std, min, 25th percentile, median (50%), 75th percentile, and max — in a single call. It covers all numeric columns at once, so you do not need to call `mean()` and `std()` separately just to get a first look. ⟦B.f5 B:tb6⟧

=========

# EVALUATOR PACKET — Selecting and Filtering Data (tile_pandas_selection_filtering)
Tile summary: Use .loc and .iloc to select rows and columns by label or position, and apply boolean filters — single conditions or combined with & | ~ — to keep only the rows you need.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.loc_iloc_selection — Selecting rows/columns with loc/iloc
B = pandas.boolean_filtering — Boolean/conditional filtering

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (pandas.loc_iloc_selection)   objective: Select rows and columns from a DataFrame by label using loc, or by integer position using iloc.
A.f1: .loc selects data primarily by label (row or column names), while .iloc selects data primarily by integer position, from 0 to length-1 of the axis.   [sources: pandas_docs_indexing#different-choices-for-indexing]
A.f2: .loc slicing with labels (e.g. 'a':'f') includes both the start and the stop labels in the result, unlike ordinary Python slicing where the stop is excluded.   [sources: pandas_docs_indexing#selection-by-label]
A.f3: .iloc uses 0-based positional indexing where, when slicing, the start position is included and the stop position is excluded, following ordinary Python/NumPy slicing rules.   [sources: pandas_docs_indexing#selection-by-position]
A.f4: Both .loc and .iloc select using a row selector and a column selector separated by a comma (e.g. df.loc[rows, cols]); an axis left out of the selection, or given as a colon (:), means 'all of that axis', so df.loc['a'] is equivalent to df.loc['a', :].   [sources: pandas_docs_indexing#different-choices-for-indexing]
note: Keep the .loc-inclusive vs .iloc-exclusive contrast explicit -- it's the single easiest thing to get backwards.
PRACTICE ANCHOR (live_code): Select a named column and a labeled row range with loc, then select the same data by numeric position with iloc.  SUCCESS: Both selections print the same rows and column, and the learner explains why the loc slice and the iloc slice use different stop values for the same rows.
ASSESSMENT ANCHOR: choose_loc_or_iloc facts=['f1']
ASSESSMENT ANCHOR: write_row_and_column_selectors facts=['f4']
ASSESSMENT ANCHOR: predict_loc_slice_with_inclusive_stop facts=['f2']
ASSESSMENT ANCHOR: predict_iloc_slice_with_exclusive_stop facts=['f3']

## SOURCE FACTS — B (pandas.boolean_filtering)   objective: Filter DataFrame rows using a boolean condition on a column.
B.f1: You may select rows from a DataFrame using a boolean vector the same length as the DataFrame's index; only the rows where the vector is True are kept.   [sources: pandas_docs_indexing#boolean-indexing]
B.f2: Comparing a DataFrame column with a value (e.g. df['A'] > 0) produces a True/False Series of the same length as the column, which can be used directly inside the DataFrame's [] to keep only the matching rows (e.g. df[df['A'] > 0]).   [sources: pandas_docs_indexing#boolean-indexing]
B.f3: When combining multiple boolean conditions with the operators | (or), & (and), or ~ (not), each condition must be grouped in parentheses, because Python would otherwise evaluate the comparison operators in an unintended order.   [sources: pandas_docs_indexing#boolean-indexing]
PRACTICE ANCHOR (live_code): Filter a DataFrame to only the rows where a numeric column exceeds a threshold.  SUCCESS: The printed result contains only rows whose column value is above the threshold, and no row at or below it.
ASSESSMENT ANCHOR: write_single_condition_filter facts=['f2']
ASSESSMENT ANCHOR: explain_boolean_mask_row_selection facts=['f1']
ASSESSMENT ANCHOR: combine_conditions_with_parentheses facts=['f3']

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

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Aggregate functions (COUNT, SUM, AVG, MIN, MAX); Apply transform; Boolean/conditional filtering; Concat stacking; DISTINCT for de-duplication; Exporting cleaned data (to_csv); Grouping and aggregation (groupby); Handling missing data (isna, dropna, fillna); Limiting results (LIMIT/OFFSET); Logical operators (AND, OR, NOT) in filtering; Map substitution; Melt reshaping; Merge join; NULL handling (IS NULL / IS NOT NULL); Pivot table reshaping; Relational database and table structure basics; Removing duplicate rows; Renaming columns and index labels; SELECT statement fundamentals (columns, aliasing); Sorting results with ORDER BY (ASC/DESC); Sorting values; String cleaning with the .str accessor; Table and column aliasing for readability; Type conversion and dtype management (astype); WHERE clause filtering and comparison operators; Working with datetime data (to_datetime, date components)

## LESSON, in learner order

### s01 · explainer · Two accessors: .loc for labels, .iloc for positions  [reward 5]
loc & iloc — Pandas gives two different accessors depending on whether you want to address rows by their labels or by their integer positions.
(definition) `.loc` selects data **by label** — row index labels and column names. `.iloc` selects data **by integer position**, from 0 to length−1 of the axis. Both accept a row selector and a column selector separated by a comma: `df.loc[rows, cols]`. A colon (`:`) or omitting an axis means 'all of that axis'. ⟦A.f1 A.f4 A:tb2 A:tb3⟧
(example) `orders.loc[2:4, "city"]` selects the `city` column for the rows **labeled** 2 through 4 — and because `.loc` uses label slicing, **both endpoints are included** in the result. So `orders.loc[2:4]` returns rows labeled 2, 3, and 4. ⟦A.f2 A:tb4 A:tb5⟧
[SIDE_BY_SIDE] .loc includes the stop label; .iloc excludes the stop position — double-check this boundary whenever a slice's last row matters. left_label: .loc — label-based (stop included) | right_label: .iloc — position-based (stop excluded)
  left:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] highlights=[["row",null,"label 0"],["row",null,"label 1"],["row",null,"label 2 (stop included)"]]] caption: orders.loc[0:2, ['order_id','city']] — rows labeled 0, 1, 2 (all three included)
  right:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] highlights=[["row",null,"pos 0"],["row",null,"pos 1"],["row",null,"pos 2 (stop excluded at 3)"]]] caption: orders.iloc[0:3, [0,1]] — positions 0, 1, 2 (position 3 excluded)

### s02 · video · Selecting rows and columns with .loc and .iloc  [reward 3]
loc & iloc — Watch .loc and .iloc used on real tables to pick rows by label and by position.
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · explainer · .iloc uses 0-based positions with an exclusive stop  [reward 3]
loc & iloc — iloc follows the same slicing rules as Python lists — the stop position is not included.
(mechanism) `orders.iloc[0:3, 0:2]` selects the first three rows (positions 0, 1, 2) and the first two columns (positions 0, 1) by pure position. The stop position 3 is **excluded**, following ordinary Python slicing rules. So `orders.iloc[0:3]` returns exactly three rows — not four. ⟦A.f3 A:tb6 A:tb7⟧

### s04 · check · Predict an iloc slice  [reward 5]
Quick check — Apply the exclusive-stop rule to predict which rows orders.iloc[1:3] returns.

### s05 · hands_on · Select rows and columns with .loc and .iloc  [reward 10]
Hands-on — Use .loc to select by label and .iloc to select by position on the SwiftDrop orders table.

### s06 · explainer · Filter rows with a True/False mask  [reward 5]
Boolean Filtering — Suppose you only want the delivery orders that took longer than 25 minutes — a boolean filter does exactly that.
(mechanism) Comparing a DataFrame column with a value — such as `orders['delivery_time_minutes'] > 25` — produces a **True/False Series** of the same length as the column. Passing that Series inside `orders[...]` keeps only the rows where the value is `True`. ⟦B.f1 B.f2 B:tb2 B:tb3⟧
(mechanism) When combining multiple conditions, each must be wrapped in parentheses and joined with `&` (and), `|` (or), or `~` (not). For example: `orders[(orders['city'] == 'Lagos') & (orders['delivery_time_minutes'] > 25)]`. Without the parentheses Python evaluates the comparison operators in the wrong order. ⟦B.f3 B:tb4⟧
[BEFORE_AFTER] The boolean mask keeps only rows where delivery_time_minutes > 25; all other rows are dropped.
  before:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] tags=delivery_time_minutes:mask column] caption: All orders — delivery_time_minutes varies
  after:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] highlights=[["row",null,"True"],["row",null,"True"],["row",null,"True"]]] caption: orders[orders['delivery_time_minutes'] > 25] — only rows where mask is True

### s07 · video · Boolean masks in action  [reward 3]
Boolean Filtering — Watch a comparison expression produce a True/False Series and filter a table.
[VIDEO ] bridge-before:  | bridge-after: 

### s08 · check · Writing a single-condition filter  [reward 5]
Quick check — Confirm you can write a boolean filter and explain what the mask does to the rows.

### s09 · check · Combining conditions with parentheses  [reward 5]
Quick check — Identify the correct way to combine two boolean conditions in a pandas filter.

### s10 · hands_on · Filter the orders DataFrame  [reward 10]
Hands-on — Write a boolean filter to keep only Lagos orders, then combine two conditions to find long Lagos deliveries.

### s11 · recap · What you learned: selecting and filtering data  [reward 5]
Recap — Two accessors and a mask — here is the summary.
(takeaway) `.loc` selects by **label** and includes the stop label in a slice. `.iloc` selects by **integer position** and excludes the stop position, following Python slicing rules. Both accept `[rows, cols]` — a colon means 'all of that axis'. ⟦A.f1 A.f2 A.f3 A:tb8⟧
(takeaway) A boolean filter is a same-length True/False Series you compute first, then pass to `df[...]` to keep only the matching rows. When combining conditions with `&`, `|`, or `~`, each condition must be in parentheses. ⟦B.f1 B.f2 B.f3 B:tb5⟧
[UP NEXT] Up next: Sorting and Renaming: Next you will sort a DataFrame by one or more columns using sort_values, and rename column and index labels with rename.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · .iloc stop position is excluded — iloc follows Python slicing: the stop is not included in the result.
(mechanism) `orders.iloc[0:3]` returns rows at positions 0, 1, and 2 — **not** position 3. This is the same rule as Python list slicing: `my_list[0:3]` gives three items. Contrast with `.loc`: `orders.loc[0:3]` returns rows labeled 0, 1, 2, **and** 3 — the stop label is included. Always double-check which accessor you are using when the last row matters. ⟦A.f3 A:tb7 A:tb8⟧
### r02 · How a boolean mask filters rows — The mask is a True/False Series — only True rows survive.
(mechanism) `orders['delivery_time_minutes'] > 25` produces a True/False Series the same length as the DataFrame. Passing it inside `orders[...]` keeps only the rows where the value is `True` — every row where the condition is `False` is dropped. The mask must be the same length as the DataFrame's index; pandas aligns them row by row. ⟦B.f1 B.f2 B:tb2 B:tb3⟧
### r03 · Parentheses are required when combining conditions — Each condition must be in its own parentheses before you join them with & or |.
(mechanism) When combining conditions, each must be grouped in parentheses: `orders[(orders['city'] == 'Lagos') & (orders['delivery_time_minutes'] > 25)]`. Without the parentheses, Python evaluates the comparison operators in the wrong order and raises a `ValueError`. The `&`, `|`, and `~` operators work element-wise on the boolean Series. ⟦B.f3 B:tb4⟧

=========

# EVALUATOR PACKET — Sorting and Renaming (tile_pandas_sort_rename)
Tile summary: Sort a DataFrame by one or more columns with sort_values, controlling ascending/descending order per column, and rename column and index labels with rename using a dict mapping.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.sort_values — Sorting values
B = pandas.rename_columns_index — Renaming columns and index labels

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (pandas.sort_values)   objective: Sort a DataFrame by the values in one or more columns, in ascending or descending order.
A.f1: DataFrame.sort_values(by=...) sorts rows using the values of the listed column(s); when by is a list of column names, the first column sets the primary sort order and each later column breaks ties among rows that were equal in the previous column(s).   [sources: pandas_docs_basics#by-values]
A.f2: sort_values()'s ascending parameter defaults to True, and can be given as a list of booleans matching the length of by, to sort some columns ascending and others descending in the same call.   [sources: pandas_docs_dataframe_sort_values]
PRACTICE ANCHOR (live_code): Sort a DataFrame by one column ascending and a tiebreaker column descending.  SUCCESS: The printed rows are ordered by the primary column ascending, and rows with equal primary values are ordered by the tiebreaker column from largest to smallest.
ASSESSMENT ANCHOR: sort_by_one_or_more_columns facts=['f1']
ASSESSMENT ANCHOR: set_ascending_per_column facts=['f2']

## SOURCE FACTS — B (pandas.rename_columns_index)   objective: Rename a DataFrame's column labels and/or index labels using rename.
B.f1: The rename() method relabels a DataFrame's axes using a dict or Series mapping (or a function); passing a columns= mapping renames column labels and an index= mapping renames row index labels.   [sources: pandas_docs_basics#renaming-mapping-labels]
B.f2: A single rename() call can rename columns and index labels together by passing both the columns and index arguments at once; any label not included in the mapping is left unchanged.   [sources: pandas_docs_basics#renaming-mapping-labels]
PRACTICE ANCHOR (live_code): Rename two columns to clearer names and rename one index label in a single rename() call.  SUCCESS: The printed DataFrame shows the two new column names and the new index label, with every other label unchanged.
ASSESSMENT ANCHOR: rename_columns_with_mapping facts=['f1']
ASSESSMENT ANCHOR: rename_columns_and_index_together facts=['f2']

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

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Aggregate functions (COUNT, SUM, AVG, MIN, MAX); Apply transform; Concat stacking; DISTINCT for de-duplication; Exporting cleaned data (to_csv); GROUP BY grouping semantics; Grouping and aggregation (groupby); HAVING clause for filtering aggregated groups; Handling missing data (isna, dropna, fillna); Limiting results (LIMIT/OFFSET); Logical operators (AND, OR, NOT) in filtering; Map substitution; Melt reshaping; Merge join; NULL handling (IS NULL / IS NOT NULL); Pivot table reshaping; Relational database and table structure basics; Removing duplicate rows; Renaming columns and index labels; SELECT statement fundamentals (columns, aliasing); Sorting results with ORDER BY (ASC/DESC); String cleaning with the .str accessor; Table and column aliasing for readability; Type conversion and dtype management (astype); WHERE clause filtering and comparison operators; Working with datetime data (to_datetime, date components)

## LESSON, in learner order

### s01 · explainer · sort_values: sort by one or more columns  [reward 5]
Sorting — Reorder the rows of a DataFrame by the values in one or more columns.
(definition) `DataFrame.sort_values(by=...)` sorts rows using the values of the listed column(s). When `by` is a list, the first column sets the primary sort order and each later column breaks ties: `orders.sort_values(by=['city', 'delivery_time_minutes'])` sorts by city first, then by delivery time within each city. ⟦A.f1 A:tb1⟧
(mechanism) The `ascending` parameter defaults to `True`. Pass a list of booleans matching the length of `by` to sort some columns ascending and others descending in the same call: `orders.sort_values(by=['city', 'delivery_time_minutes'], ascending=[True, False])` sorts cities alphabetically but delivery times from slowest to fastest within each city. ⟦A.f2 A:tb2⟧
[BEFORE_AFTER] Rows are reordered: city is the primary sort key; delivery_time_minutes breaks ties within each city.
  before:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] ] caption: orders — original row order
  after:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] highlights=[["column","city","primary sort"],["column","delivery_time_minutes","tie-breaker"]]] caption: orders.sort_values(by=['city','delivery_time_minutes']) — sorted by city, then time

### s02 · check · Setting ascending per column  [reward 5]
Quick check — Identify the correct call to sort one column ascending and another descending in the same sort_values call.

### s03 · hands_on · Sort the orders DataFrame  [reward 10]
Hands-on — Sort orders by city ascending, then by delivery_time_minutes descending within each city.

### s04 · explainer · rename(): relabel columns and index entries with a dict  [reward 5]
Renaming — Clean up column names or row labels without rebuilding the DataFrame.
(definition) `rename()` relabels a DataFrame's axes using a dict mapping. Pass `columns=` to rename column labels: `orders.rename(columns={'delivery_time_minutes': 'delivery_min'})` renames that one column and leaves every other label unchanged. ⟦B.f1 B:tb1⟧
(mechanism) A single `rename()` call can rename columns and index labels together by passing both `columns=` and `index=` at once: `orders.rename(columns={'city': 'destination_city'}, index={0: 'first_order'})` relabels one column and one row label in one call — any label not in the mapping is left as-is. ⟦B.f2 B:tb2⟧
[BEFORE_AFTER] Two column labels are renamed; order_id and all other labels are unchanged.
  before:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] ] caption: orders — original column names
  after:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] highlights=[["column","city","→ destination_city"],["column","delivery_time_minutes","→ delivery_min"]]] caption: orders.rename(columns={'delivery_time_minutes': 'delivery_min', 'city': 'destination_city'})

### s05 · check · Renaming columns with a mapping  [reward 5]
Quick check — Identify the correct rename() call to relabel a column using a dict.

### s06 · hands_on · Rename columns and an index label  [reward 10]
Hands-on — Rename two columns to clearer names and rename one index label in a single rename() call.

### s07 · recap · What you learned: sorting and renaming  [reward 5]
Recap — One method to reorder rows, one method to relabel axes.
(takeaway) `sort_values(by=[...])` reorders rows by the listed columns. The first column is the primary sort key; later columns break ties. `ascending` defaults to `True` and can be a list of booleans to mix directions. ⟦A.f1 A.f2⟧
(takeaway) `rename(columns={...})` relabels column headers using a dict mapping; `rename(index={...})` relabels row index entries. Both can be combined in one call — any label not in the mapping is left unchanged. ⟦B.f1 B.f2⟧
[UP NEXT] Up next: Type Conversion and Datetime Handling: Next you will convert column dtypes with astype and parse date strings into datetime objects so you can extract months, days, and other time components.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · ascending as a list of booleans — To mix sort directions, pass a list of booleans matching the length of by.
(example) `sort_values()`'s `ascending` parameter defaults to `True` (all columns sorted ascending). To sort some columns ascending and others descending in the same call, pass a list of booleans the same length as `by`: `orders.sort_values(by=['city', 'delivery_time_minutes'], ascending=[True, False])` sorts cities A→Z but delivery times from largest to smallest within each city. ⟦A.f2 A:tb2⟧
### r02 · rename() with columns= and index= together — One rename() call can relabel both column headers and row index entries.
(example) `orders.rename(columns={'delivery_time_minutes': 'delivery_min'})` renames one column; every other column label is left unchanged. To rename a column and an index label in the same call: `orders.rename(columns={'city': 'destination_city'}, index={0: 'first_order'})`. Any label not listed in the mapping is untouched. ⟦B.f1 B.f2 B:tb1 B:tb2⟧