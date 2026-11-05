# EVALUATOR PACKET — Creating and Inspecting DataFrames (tile_pandas_creating_inspecting)
Tile summary: Build a DataFrame directly from Python data — a dict of lists or a list of dicts — then use head, shape, dtypes, info, and describe to get an immediate overview of what is inside.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.creating_dataframes — Creating DataFrames from dicts/lists/files
B = pandas.inspecting_dataframes — Inspecting data (head, info, describe, shape, dtypes)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

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
[VIDEO Building a DataFrame from a dict of lists] bridge-before: Watch each key become a column and each list fill it, with the 0, 1, 2 index appearing on its own. | bridge-after: The clip shows only the dict-of-lists route. Devspace also teaches the list-of-dicts route, where each dict is one row and the keys name the columns.
  - OUnnuKHbmbU 0-134s facts=['f1'] label: Building a DataFrame from a dict of equal-length lists | summary: Describes a DataFrame as a tabular, two-dimensional structure with rows and columns, similar to a spreadsheet, then builds one. A dict has keys 'name' and 'age', each holding an equal-length list of values, and the dict is passed to pd.DataFrame. Printing the result shows a table with one column per key and an index labelled 0, 1, 2 for the rows, which can be changed to something custom later.

### s03 · check · Building a DataFrame from a list of dicts  [reward 5]
Quick check — Confirm you can identify what each dict contributes when you pass a list of dicts to pd.DataFrame.
QUESTION [choice, intro, grading=client] You have this data: `[{'order_id': 1001, 'city': 'Lagos'}, {'order_id': 1002, 'city': 'Abuja'}]`. What does `pd.DataFrame(data)` produce?
  ✔ opt_a: A DataFrame with 2 rows and 2 columns, where each dict becomes one row.
      why: Correct. When you pass a list of dicts to `pd.DataFrame()`, each dict contributes one row. The keys become column names.
  ✘ opt_b: A DataFrame with 2 columns and 2 rows, where each dict becomes one column.
      why: Not quite. Each dict in the list becomes a row, not a column. The keys of the dicts become the column names.
  ✘ opt_c: A Series with 2 elements, one per dict.
      why: A list of dicts passed to `pd.DataFrame()` creates a DataFrame, not a Series. Each dict becomes a row.
  ✘ opt_d: An error, because DataFrames require a dict of lists, not a list of dicts.
      why: DataFrames accept both forms: a dict of lists (keys → columns) and a list of dicts (each dict → one row). Both are valid.
  feedback✔: Exactly right. Each dict in the list maps to one row, with dict keys as column names.  feedback✘: Review how `pd.DataFrame()` handles a list of dicts: each dict becomes one row.  hints: ['Think about what one dict represents: a single record with multiple fields.', 'The keys in each dict become the column names.']  remediation→r01
  MEASURES: A:build_dataframe_from_list_of_dicts(f2)   anchors=['assessment:build_dataframe_from_list_of_dicts']
  taught-before-tested: A.f2←s01

### s04 · hands_on · Create a DataFrame two ways  [reward 10]
Hands-on — Build the same small orders table once from a dict of lists and once from a list of dicts, then confirm both produce the same result.
QUESTION [code_exercise, intro, grading=client] Two data structures are provided: `dict_of_lists` and `list_of_dicts`. Create two DataFrames:
1. `df1` from `dict_of_lists`
2. `df2` from `list_of_dicts`

Print both. They should produce the same 14×3 DataFrame (14 rows, 3 columns).
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=['import pandas as pd', 'pd.DataFrame(dict_of_lists)', 'pd.DataFrame(list_of_dicts)', 'print(df)'] blocked=4 items
  file solution.py [editable]:
import pandas as pd

# Data loaded from CSV (scaffolding)
_raw = pd.read_csv('orders_sample.csv')
dict_of_lists = {
    'order_id': list(_raw['order_id']),
    'city': list(_raw['city']),
    'delivery_time_minutes': list(_raw['delivery_time_minutes'])
}
list_of_dicts = _raw[['order_id', 'city', 'delivery_time_minutes']].to_dict('records')

# TODO: Create df1 from dict_of_lists using pd.DataFrame()
# TODO: Create df2 from list_of_dicts using pd.DataFrame()
# TODO: Print both

  SOLUTION solution.py:
import pandas as pd

# Data loaded from CSV (scaffolding)
_raw = pd.read_csv('orders_sample.csv')
dict_of_lists = {
    'order_id': list(_raw['order_id']),
    'city': list(_raw['city']),
    'delivery_time_minutes': list(_raw['delivery_time_minutes'])
}
list_of_dicts = _raw[['order_id', 'city', 'delivery_time_minutes']].to_dict('records')

df1 = pd.DataFrame(dict_of_lists)
df2 = pd.DataFrame(list_of_dicts)
print(df1)
print(df2)

  test t1 (value_equals, visible=True): {"expr":"df1.shape","expected":[14,3]} | on-fail: df1 should have 14 rows and 3 columns. Check that you created it from dict_of_lists using pd.DataFrame().
  test t2 (value_equals, visible=True): {"expr":"df2.shape","expected":[14,3]} | on-fail: df2 should have 14 rows and 3 columns. Check that you created it from list_of_dicts using pd.DataFrame().
  test t3 (dataframe_equals, visible=True): {"expr":"df1","expected":{"columns":["order_id","city","delivery_time_minutes"],"rows":[[1001,"Lagos",18],[1002,"Abuja",20],[1003,"Kano",22],[1004,"Lagos",22],[1005,"Abuja",26],[1006,"Kano",28],[1007,"Lagos",80],[1008,"Abuja",31],[1009,"Kano",19],[1010,"Lagos",24],[1011,"Abuja",33],[1012,"Kano",21],[1013,"Lagos",27],[1014,"Abuja",35]]}} | on-fail: df1 does not match the expected data. Check that you used pd.DataFrame(dict_of_lists).
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"ca243afa0c795e51b0a221b5cfa1cab10b8af4878ee13399e25521d2483abb23","tests_passed":3}
  feedback✔: Excellent! You built the same DataFrame from both a dict of lists and a list of dicts.  feedback✘: Review how to load a CSV file with `pd.read_csv()`.  hints: ["Use `pd.DataFrame('orders_sample.csv')` to load the file.", 'Store the result in a variable and print it.']  remediation→r01
  MEASURES: A:build_dataframe_from_dict_of_lists(f1); A:build_dataframe_from_list_of_dicts(f2)   anchors=['practice', 'assessment:build_dataframe_from_dict_of_lists', 'assessment:build_dataframe_from_list_of_dicts']
  taught-before-tested: A.f1←s01; A.f2←s01

### s05 · explainer · Five methods that answer your first questions about a DataFrame  [reward 5]
Inspecting DataFrames — Before doing anything else with a newly loaded or built orders DataFrame, get an overview of what is actually in it.
(mechanism) `orders.head()` shows the first five delivery records by default — a quick sanity check that the data loaded correctly. `orders.shape` returns a tuple of (rows, columns), such as `(250, 10)` for 250 orders across 10 columns. ⟦B.f1 B.f2 B:tb2 B:tb3⟧
(mechanism) `orders.dtypes` returns the data type of each column — for example, that `delivery_time_minutes` holds integers and `city` holds text. `orders.info()` combines that dtype list with a count of non-missing values per column and the DataFrame's memory usage in one concise summary. ⟦B.f3 B.f4 B:tb4 B:tb5⟧
[COMPARISON] cols=['head()', 'shape', 'dtypes', 'info()', 'describe()']
  - What it shows: {"head":"First 5 rows by default","shape":"Tuple of (rows, columns)","dtypes":"Data type of each column","info":"Non-null counts, dtypes, and memory usage","describe":"Statistical summary of numeric columns"}
  - Example output: {"head":"DataFrame with 5 rows × all columns","shape":"(250, 10)","dtypes":"order_id: int64, city: object, ...","info":"250 entries, 10 columns, 19.6+ KB","describe":"count, mean, std, min, max for numeric columns"}
  - Best for: {"head":"Quick sanity check of data","shape":"Confirming dimensions","dtypes":"Checking column types","info":"Finding missing values","describe":"Understanding numeric distributions"}
[DIAGRAM: Five inspection methods and the question each answers] nodes=['head()', 'shape', 'dtypes', 'info()', 'describe()', 'What do the first rows look like?', 'How many rows and columns?', 'What type is each column?', 'Are there missing values?', 'What are the numeric distributions?'] edges=[('n_head', 'q_preview', None), ('n_shape', 'q_size', None), ('n_dtypes', 'q_types', None), ('n_info', 'q_missing', None), ('n_describe', 'q_stats', None)] alt: A mapping diagram showing five pandas inspection methods — head(), shape, dtypes, info(), and describe() — each connected by an arrow to the question it answers: head() → 'What do the first rows look like?'; shape → 'How many rows and columns?'; dtypes → 'What type is each column?'; info() → 'Are there missing values?'; describe() → 'What are the numeric distributions?'.

### s06 · video · head, shape, dtypes, info, and describe in action  [reward 3]
Inspecting DataFrames — Watch each inspection method called on a real table and see what it returns.
[VIDEO Five quick first looks at a DataFrame] bridge-before: Match each method to its question: head and tail show a sample, shape the size, dtypes and info the types, describe the numbers. Skip the short sponsor read in clip 1 and the side trips in clip 3. | bridge-after: Together the clips cover all five methods. Clip 2 leaves out the non-missing counts and memory use that info() also reports; clip 3 covers both.
  - Liv6eeb1VfE 225-366s facts=['f4', 'f5'] label: Running df.info() and df.describe() on a world-population table | summary: On a world-population table, info() is called first as a high-level look. It lists the columns, how many values each has (234 in most columns, fewer in some, with the count marking what is not null) and each column's data type. A short sponsor message sits in the middle of the clip. Then describe() gives, for each numeric column, the count, mean, standard deviation, minimum, maximum and the 25th, 50th and 75th percentiles, a quick overview from which the presenter reads off a few extremes.
  - ZyhVh-qRZPA 677-860s facts=['f2', 'f4'] label: Checking a DataFrame's size with .shape and its columns and types with .info() | summary: Shows shape as an attribute rather than a method, so it takes no parentheses: it returns the number of rows and then columns as a tuple, about 88,000 rows by 85 columns. Then info() is called, with parentheses because it is a method, and its output lists the number of entries, the columns and each column's data type, where object usually means strings, int64 means integers and float means decimal numbers. A short detour restarts the notebook to fix cut-off text. The non-missing counts and memory use in the output are not discussed.
  - BspcRHPiFk4 104-562s facts=['f1', 'f2', 'f3', 'f4'] label: Four quick looks at a sales table: head() and tail(), shape, dtypes and info() | summary: A tour of quick first looks at a loaded sales table. head() and tail() return the first and last five rows, which shows the column names and index positions. shape returns a tuple of rows and then columns (9994 by 20), written without parentheses. dtypes shows how each column is stored (text as object, dates, floats, integers), and info() combines the column types with non-null counts per column and the memory used. Side trips cover len(), columns, chaining and counting the dtypes.

### s07 · explainer · describe() — a statistical overview in one call  [reward 3]
Inspecting DataFrames — One method summarises all numeric columns at once.
(mechanism) `orders.describe()` computes a quick statistical overview of each numeric column — count, mean, std, min, quartiles, and max — in a single call. ⟦B.f5 B:tb6⟧

### s08 · check · shape and info  [reward 5]
Quick check — Test your understanding of what shape and info() each report about a DataFrame.
QUESTION [choice, core, grading=client] A DataFrame `orders` has `shape` of `(250, 10)`. What does this tell you, and what additional information does `orders.info()` provide that `shape` does not?
  ✔ opt_a: `shape` tells you there are 250 rows and 10 columns. `info()` adds column names, data types, and non-null counts.
      why: Correct. `shape` returns (rows, columns). `info()` prints a concise summary with column names, dtypes, and non-null counts.
  ✘ opt_b: `shape` tells you there are 10 rows and 250 columns. `info()` adds statistical summaries like mean and median.
      why: `shape` is (rows, columns), so `(250, 10)` means 250 rows and 10 columns, not the reverse. `info()` does not compute statistical summaries; that's `describe()`.
  ✘ opt_c: `shape` tells you the memory usage. `info()` adds the first and last rows.
      why: `shape` returns the dimensions (rows, columns), not memory usage. `info()` does show memory usage, but it does not show the first and last rows; that's `head()` and `tail()`.
  ✘ opt_d: `shape` and `info()` provide the same information; they are interchangeable.
      why: `shape` gives only the dimensions. `info()` adds column names, data types, non-null counts, and memory usage.
  feedback✔: Exactly. `shape` gives dimensions; `info()` adds column detail.  feedback✘: Remember: `shape` is (rows, columns). `info()` adds column names, dtypes, and non-null counts.  hints: ['`shape` is a tuple: (number of rows, number of columns).', '`info()` prints a summary that includes data types and missing-value counts.']  remediation→r02
  MEASURES: B:report_rows_and_columns_with_shape(f2); B:read_info_summary(f4)   anchors=['assessment:report_rows_and_columns_with_shape', 'assessment:read_info_summary']
  taught-before-tested: B.f2←s05; B.f4←s05

### s09 · check · describe() overview  [reward 5]
Quick check — Confirm what describe() computes and when to reach for it.
QUESTION [choice, core, grading=client] You call `orders.describe()` on a DataFrame with columns `order_id`, `city`, `delivery_time_minutes`, and `distance_km`. Which columns appear in the output, and what statistics does `describe()` compute?
  ✔ opt_a: Only numeric columns (`order_id`, `delivery_time_minutes`, `distance_km`) appear, with count, mean, std, min, 25%, 50%, 75%, max.
      why: Correct. `describe()` computes statistics for numeric columns: count, mean, std, min, 25%, 50% (median), 75%, max. Text columns are excluded by default.
  ✘ opt_b: All columns appear, with count, mean, std, min, max for numeric columns and unique, top, freq for text columns.
      why: By default, `describe()` includes only numeric columns. To see text columns, you must pass `include='all'`.
  ✘ opt_c: Only `delivery_time_minutes` and `distance_km` appear, because `order_id` is an identifier, not a quantity.
      why: `describe()` includes all numeric columns, even identifiers like `order_id`. It does not distinguish between identifiers and quantities.
  ✘ opt_d: All columns appear, but only count and data type are shown.
      why: `describe()` computes statistical summaries (count, mean, std, min, percentiles, max) for numeric columns, not just count and data type.
  feedback✔: Exactly. `describe()` gives a statistical overview of numeric columns.  feedback✘: Remember: `describe()` computes count, mean, std, min, quartiles, and max for numeric columns only (by default).  hints: ['`describe()` focuses on numeric columns by default.', 'The output includes count, mean, std, min, 25%, 50%, 75%, max.']  remediation→r03
  MEASURES: B:get_describe_overview(f5)   anchors=['assessment:get_describe_overview']
  taught-before-tested: B.f5←s07

### s10 · hands_on · Inspect the orders DataFrame  [reward 10]
Hands-on — Call head() to preview the first rows, then use dtypes to read each column's type.
QUESTION [code_exercise, core, grading=client] Load `orders.csv` and inspect it:
1. Print the shape (row and column counts).
2. Print the dtypes (data type of each column).
3. Print the first 5 rows with `head()`.

Your output should show the dimensions, the data types, and a preview of the data.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=['import pandas as pd', 'pd.read_csv(path)', 'df.head()', 'df.tail()', 'df.shape', 'df.dtypes', 'df.info()', 'df.describe()', 'print()'] blocked=7 items
  file solution.py [editable]:
import pandas as pd

path = 'orders.csv'  # scaffolding

# TODO: load the CSV into a DataFrame called df using pd.read_csv(path)
# TODO: print the shape
# TODO: print the dtypes
# TODO: print the first 5 rows

  SOLUTION solution.py:
import pandas as pd

path = 'orders.csv'  # scaffolding

df = pd.read_csv(path)

print(df.shape)
print(df.dtypes)
print(df.head())

  test t1 (value_equals, visible=True): {"expr":"df.shape","expected":[14,10]} | on-fail: df.shape should be (14, 10). Make sure you loaded orders.csv and printed the shape.
  test t2 (dataframe_equals, visible=True): {"expr":"df.head()","expected":{"columns":["order_id","city","city_code","courier","driver_id","customer_id","pickup_date","delivery_time_minutes","distance_km","order_value"],"rows":[[1001,"Lagos","LOS","Ada",201,301,"2024-03-14",18,4.2,2500],[1002,"Abuja","ABJ","Bayo",202,302,"2024-03-14",20,6.1,3100],[1003,"Kano","KAN","Chidi",203,303,"2024-03-15",22,5.5,1800],[1004,"Lagos","LOS","Ada",201,304,"2024-03-15",22,3.8,2200],[1005,"Abuja","ABJ","Bayo",202,305,"2024-03-16",26,7.3,4000]]}} | on-fail: df.head() should return the first 5 rows of orders.csv. Check that you loaded the file correctly.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"8b53cc351d897c52184961b8aa1e78f8cf27a2f06fc43a4b6867e1c30f564295","tests_passed":2}
  feedback✔: Excellent! You inspected the DataFrame's dimensions, data types, and first rows.  feedback✘: Review the inspection methods: `shape`, `dtypes`, and `head()`.  hints: ['`shape` is an attribute (no parentheses): `df.shape`.', '`dtypes` is also an attribute: `df.dtypes`.', '`head()` is a method: `df.head()`.']
  MEASURES: B:preview_rows_with_head(f1); B:read_column_dtypes(f3)   anchors=['practice', 'assessment:preview_rows_with_head', 'assessment:read_column_dtypes']
  taught-before-tested: B.f1←s05; B.f3←s05

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

## OTHER CONTENT (fields without a dedicated renderer)
· blocks.title: Five inspection methods at a glance

=========

# EVALUATOR PACKET — Selecting and Filtering Data (tile_pandas_selection_filtering)
Tile summary: Use .loc and .iloc to select rows and columns by label or position, and apply boolean filters — single conditions or combined with & | ~ — to keep only the rows you need.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.loc_iloc_selection — Selecting rows/columns with loc/iloc
B = pandas.boolean_filtering — Boolean/conditional filtering

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

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
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] highlights=[["row",null,"label 0"],["row",null,"label 1"],["row",null,"label 2 (stop included)"]]] caption: orders.loc[0:2, ['order_id','city','delivery_time_minutes']] — rows labeled 0, 1, 2 (all three included)
  right:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] highlights=[["row",null,"pos 0"],["row",null,"pos 1"],["row",null,"pos 2 (stop excluded at 3)"]]] caption: orders.iloc[0:3, [0,1,7]] — positions 0, 1, 2 (position 3 excluded)

### s02 · video · Selecting rows and columns with .loc and .iloc  [reward 3]
loc & iloc — Watch .loc and .iloc used on real tables to pick rows by label and by position.
[VIDEO Selecting by label with loc and by position with iloc] bridge-before: Watch label-based loc against position-based iloc, and the row selector then column selector pattern. In clip 2, iloc[0:11] returns 11 rows, not the 10 the narrator says. | bridge-after: Neither clip states that a loc label slice includes its stop (clip 2's Charizard-to-Blastoise slice shows it without saying so). Keep Devspace's rule: loc includes the stop label, iloc excludes the stop position.
  - zmdjNSmRXF4 934-1327s facts=['f1', 'f4'] label: iloc by integer position, then loc by label, with a row selector and a column selector | summary: On a small people table with the default 0, 1, 2 index, iloc picks rows by integer location: iloc[0] returns the first row as a Series, and a list such as [0, 1] returns several rows as a DataFrame. A second value after the row selector picks columns, by integer position for iloc (2 for the third column, since counting starts at 0). loc then works by label in the same pattern: loc[0], loc[[0, 1], 'email'], and a list of column names, which come back in the order asked for. With default labels the two look alike, so real label use is left for later.
  - aoNRYtVEhAM 163-438s facts=['f1', 'f3', 'f4'] label: loc by name and iloc by position, including a slice whose stop is excluded | summary: On a Pokemon table, a name column is made the row label when the CSV is read, so loc['Pikachu'] returns that whole row. A list of column names as the second value narrows it to height and weight, and a name-to-name slice returns the rows from Charizard through Blastoise. iloc then works by position: iloc[0:11] with a reminder that the second number is excluded, a step of two for every second row, and 0:3 as the second value for the first three columns. The narrator says 'first 10 rows' for the 0:11 slice, which actually returns 11 rows.

### s03 · explainer · .iloc uses 0-based positions with an exclusive stop  [reward 3]
loc & iloc — iloc follows the same slicing rules as Python lists — the stop position is not included.
(mechanism) `orders.iloc[0:3, 0:2]` selects the first three rows (positions 0, 1, 2) and the first two columns (positions 0, 1) by pure position. The stop position 3 is **excluded**, following ordinary Python slicing rules. So `orders.iloc[0:3]` returns exactly three rows — not four. ⟦A.f3 A:tb6 A:tb7⟧

### s04 · check · Predict an iloc slice  [reward 5]
Quick check — Apply the exclusive-stop rule to predict which rows orders.iloc[1:3] returns.
QUESTION [choice, core, grading=client] A DataFrame has 10 rows with default integer index (0 through 9). What does `df.iloc[2:5]` return?
  ✔ opt_a: Rows at positions 2, 3, and 4 (three rows).
      why: Correct. `iloc` uses Python slicing: the stop is excluded. `iloc[2:5]` returns positions 2, 3, 4.
  ✘ opt_b: Rows at positions 2, 3, 4, and 5 (four rows).
      why: The stop in `iloc` slicing is excluded, just like Python list slicing. `iloc[2:5]` gives positions 2, 3, 4, not 5.
  ✘ opt_c: Rows at positions 3, 4, and 5 (three rows).
      why: The start is included. `iloc[2:5]` begins at position 2, not 3.
  ✘ opt_d: An error, because the stop must be inclusive.
      why: `iloc` follows Python slicing rules: the stop is excluded. This is not an error; it's the standard behavior.
  feedback✔: Exactly. `iloc` stop is excluded, just like Python list slicing.  feedback✘: Remember: `iloc[start:stop]` excludes the stop position. It's the same rule as `my_list[2:5]`.  hints: ["`iloc` uses Python's slicing convention: start is included, stop is excluded.", '`iloc[2:5]` means positions 2, 3, 4.']  remediation→r01
  MEASURES: A:predict_iloc_slice_with_exclusive_stop(f3)   anchors=['assessment:predict_iloc_slice_with_exclusive_stop']
  taught-before-tested: A.f3←s03

### s05 · hands_on · Select rows and columns with .loc and .iloc  [reward 10]
Hands-on — Use .loc to select by label and .iloc to select by position on the SwiftDrop orders table.
QUESTION [code_exercise, core, grading=client] Load `orders.csv` and select data two ways using the provided variables:
1. Use `.loc` with `start_row:end_row_loc` to select rows, then select the `city_col_name` column. Store in `loc_result` and print it.
2. Use `.iloc` with `start_row:end_row_iloc` to select rows, then select the `city_col_name` column. Store in `iloc_result` and print it.

Both should return the same 3 city values: Kano, Lagos, Abuja.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=['df.loc[rows, cols]', 'df.iloc[rows, cols]', 'label slices', 'integer slices', 'list of labels', 'print()'] blocked=5 items
  file solution.py [editable]:
import pandas as pd

df = pd.read_csv('orders.csv')

# Slice bounds and column info provided
start_row = 2
end_row_loc = 4  # loc stop is inclusive
end_row_iloc = 5  # iloc stop is exclusive
city_col_name = 'city'

# TODO: Use .loc to select rows start_row through end_row_loc (inclusive), then select the city column
# TODO: Store in loc_result and print it
# TODO: Use .iloc to select rows start_row through end_row_iloc (exclusive), then select the city column
# TODO: Store in iloc_result and print it

  SOLUTION solution.py:
import pandas as pd

df = pd.read_csv('orders.csv')

# Slice bounds and column info provided
start_row = 2
end_row_loc = 4  # loc stop is inclusive
end_row_iloc = 5  # iloc stop is exclusive
city_col_name = 'city'

# Select rows first, then column using chained selection
loc_result = df.loc[start_row:end_row_loc][city_col_name]
print(loc_result)

iloc_result = df.iloc[start_row:end_row_iloc][city_col_name]
print(iloc_result)

  test t1 (value_equals, visible=True): {"expr":"list(loc_result)","expected":["Kano","Lagos","Abuja"]} | on-fail: The `.loc` result should be ['Kano', 'Lagos', 'Abuja']. Check that you used `loc[2:4]` then selected the 'city' column (inclusive stop).
  test t2 (value_equals, visible=True): {"expr":"list(iloc_result)","expected":["Kano","Lagos","Abuja"]} | on-fail: The `.iloc` result should be ['Kano', 'Lagos', 'Abuja']. Check that you used `iloc[2:5]` then selected the 'city' column (exclusive stop).
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"fdcaa373d133235ea1f2d28e5178f7d26ba0486a3c4c22f5304bcdded936358f","tests_passed":2}
  feedback✔: Perfect! You selected the same rows and column with both `.loc` and `.iloc`, accounting for the stop difference.  feedback✘: Remember: `.loc` stop is inclusive, `.iloc` stop is exclusive. To get the same rows, use different stop values.  hints: ['`.loc[2:4]` includes rows 2, 3, 4. Then select the column by name.', '`.iloc[2:5]` includes positions 2, 3, 4 (stop 5 is excluded). Then select the column by name.', 'Chain the selections: first select rows, then select the column.']  remediation→r01
  MEASURES: A:choose_loc_or_iloc(f1); A:write_row_and_column_selectors(f4); A:predict_loc_slice_with_inclusive_stop(f2); A:predict_iloc_slice_with_exclusive_stop(f3)   anchors=['practice', 'assessment:choose_loc_or_iloc', 'assessment:write_row_and_column_selectors', 'assessment:predict_loc_slice_with_inclusive_stop', 'assessment:predict_iloc_slice_with_exclusive_stop']
  taught-before-tested: A.f1←s01; A.f4←s01; A.f2←s01; A.f3←s03

### s06 · explainer · Filter rows with a True/False mask  [reward 5]
Boolean Filtering — Suppose you only want the delivery orders that took longer than 25 minutes — a boolean filter does exactly that.
(mechanism) Comparing a DataFrame column with a value — such as `orders['delivery_time_minutes'] > 25` — produces a **True/False Series** of the same length as the column. Passing that Series inside `orders[...]` keeps only the rows where the value is `True`. ⟦B.f1 B.f2 B:tb2 B:tb3⟧
(mechanism) When combining multiple conditions, each must be wrapped in parentheses and joined with `&` (and), `|` (or), or `~` (not). For example: `orders[(orders['city'] == 'Lagos') & (orders['delivery_time_minutes'] > 25)]`. Without the parentheses Python evaluates the comparison operators in the wrong order. ⟦B.f3 B:tb4⟧
[BEFORE_AFTER] The boolean mask keeps only rows where delivery_time_minutes > 25; all other rows are dropped.
  before:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] tags=delivery_time_minutes:mask column] caption: All orders — delivery_time_minutes varies
  after:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] highlights=[["row",null,"True"],["row",null,"True"],["row",null,"True"],["row",null,"True"]]] caption: orders[orders['delivery_time_minutes'] > 25] — only rows where mask is True

### s07 · video · Boolean masks in action  [reward 3]
Boolean Filtering — Watch a comparison expression produce a True/False Series and filter a table.
[VIDEO Boolean masks and combined conditions] bridge-before: The Pokemon clip shows filters and combined conditions with | and &; the mask clip explains the True/False Series behind every filter. Neither says why parentheses are needed. | bridge-after: Devspace supplies the reason: without parentheses, Python evaluates the comparison operators in an unintended order and the filter breaks. The Pokemon clip only says to use them.
  - AdR_gx5Y4wE 198-376s facts=['f2', 'f3'] label: Filtering Pokemon rows with a condition, then combining conditions with | and & | summary: Filters a Pokemon table to rows where Type 1 equals 'Water' by putting the comparison inside df[...]. To also include Pokemon whose second type is water, two conditions are combined with the vertical bar for or, each wrapped in parentheses. For fire and flying, the ampersand is used for and, again with parentheses, and not Python's own and. The result keeps only rows that satisfy the combined condition (two rows). The clip sums up filtering as keeping the rows that match a condition.
  - Lw2rlcxScZY 53-285s facts=['f1', 'f2'] label: A comparison produces a True/False mask that df[...] uses to keep rows | summary: Shows that comparing a column with a value, such as last name equal to 'Doe', returns a Series of True and False values rather than a smaller table. Each value lines up with a row of the original frame, with True marking a row that met the condition. The presenter calls this a filter mask, stores it in a variable, and passes it inside df[...] to get back only the matching rows. The same comparison is then written directly inside the brackets.

### s08 · check · Writing a single-condition filter  [reward 5]
Quick check — Confirm you can write a boolean filter and explain what the mask does to the rows.
QUESTION [choice, core, grading=client] You write `mask = orders['delivery_time_minutes'] > 25`. What is `mask`, and what happens when you write `orders[mask]`?
  ✔ opt_a: `mask` is a boolean Series (True/False for each row). `orders[mask]` keeps only rows where `mask` is True.
      why: Correct. The comparison produces a boolean Series the same length as the DataFrame. Passing it inside `df[...]` keeps only the True rows.
  ✘ opt_b: `mask` is a list of row indices where the condition is True. `orders[mask]` selects those rows by position.
      why: The comparison produces a boolean Series (True/False), not a list of indices. Pandas aligns the Series with the DataFrame's index and keeps True rows.
  ✘ opt_c: `mask` is a new DataFrame with only the rows that meet the condition. `orders[mask]` is redundant.
      why: The comparison produces a boolean Series, not a DataFrame. You must pass the mask inside `df[...]` to filter the rows.
  ✘ opt_d: `mask` is a single boolean value (True or False). `orders[mask]` returns the entire DataFrame if True, or an empty DataFrame if False.
      why: The comparison is applied element-wise to every row, producing a Series of True/False values, not a single boolean.
  feedback✔: Exactly. A boolean mask is a True/False Series; `df[mask]` keeps the True rows.  feedback✘: Remember: `df['col'] > value` produces a boolean Series. `df[mask]` filters to rows where the mask is True.  hints: ["The comparison `df['col'] > value` is applied to every row, producing a Series of True/False.", '`df[mask]` keeps only the rows where the mask is True.']  remediation→r02
  MEASURES: B:write_single_condition_filter(f2); B:explain_boolean_mask_row_selection(f1)   anchors=['assessment:write_single_condition_filter', 'assessment:explain_boolean_mask_row_selection']
  taught-before-tested: B.f2←s06; B.f1←s06

### s09 · check · Combining conditions with parentheses  [reward 5]
Quick check — Identify the correct way to combine two boolean conditions in a pandas filter.
QUESTION [choice, core, grading=client] You want to filter `orders` to rows where `city == 'Lagos'` AND `delivery_time_minutes > 25`. Which expression is correct?
  ✔ opt_a: `orders[(orders['city'] == 'Lagos') & (orders['delivery_time_minutes'] > 25)]`
      why: Correct. Each condition must be in parentheses, and you join them with `&` (element-wise AND).
  ✘ opt_b: `orders[orders['city'] == 'Lagos' & orders['delivery_time_minutes'] > 25]`
      why: Without parentheses around each condition, Python evaluates the operators in the wrong order and raises a `ValueError`. Always wrap each condition.
  ✘ opt_c: `orders[(orders['city'] == 'Lagos') and (orders['delivery_time_minutes'] > 25)]`
      why: Use `&` (element-wise AND), not `and` (Python's logical AND). `and` does not work with boolean Series.
  ✘ opt_d: `orders[orders['city'] == 'Lagos', orders['delivery_time_minutes'] > 25]`
      why: You cannot pass two separate conditions as arguments. Combine them with `&` inside a single set of brackets: `df[(cond1) & (cond2)]`.
  feedback✔: Exactly. Wrap each condition in parentheses and join with `&`.  feedback✘: Remember: each condition needs parentheses, and you join them with `&` (not `and`).  hints: ['Each condition must be wrapped in its own parentheses.', 'Use `&` for AND, `|` for OR, and `~` for NOT.']  remediation→r03
  MEASURES: B:combine_conditions_with_parentheses(f3)   anchors=['assessment:combine_conditions_with_parentheses']
  taught-before-tested: B.f3←s06

### s10 · hands_on · Filter the orders DataFrame  [reward 10]
Hands-on — Write a boolean filter to keep only Lagos orders, then combine two conditions to find long Lagos deliveries.
QUESTION [code_exercise, core, grading=client] Load `orders.csv` and filter it using the provided variables:
1. Keep only rows where the column named in `time_col` is greater than `threshold`. Store in `slow` and print it.

The result should contain 7 rows (orders 1005, 1006, 1007, 1008, 1011, 1013, 1014).
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=["df[df['col'] > value]", 'comparison operators', '& | ~ with parenthesised conditions', 'print()'] blocked=5 items
  file solution.py [editable]:
import pandas as pd

df = pd.read_csv('orders.csv')

# Filter criteria provided
time_col = 'delivery_time_minutes'
threshold = 25

# TODO: filter to rows where delivery_time_minutes > 25
# TODO: Store in slow and print it

  SOLUTION solution.py:
import pandas as pd

df = pd.read_csv('orders.csv')

# Filter criteria provided
time_col = 'delivery_time_minutes'
threshold = 25

slow = df[df[time_col] > threshold]
print(slow)

  test t1 (value_equals, visible=True): {"expr":"slow['order_id'].tolist()","expected":[1005,1006,1007,1008,1011,1013,1014]} | on-fail: The filtered result should contain order_ids [1005, 1006, 1007, 1008, 1011, 1013, 1014]. Check your filter condition.
  test t2 (value_equals, visible=True): {"expr":"len(slow)","expected":7} | on-fail: The filtered result should have 7 rows. Check that you used `> 25`, not `>= 25`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"9bae463e9c1f51e78bba6484a7e543ac34fec4b4e0082dc8c86e6da604d06901","tests_passed":2}
  feedback✔: Excellent! You filtered to rows where delivery time is above the threshold.  feedback✘: Review the boolean filtering syntax: `df[df['col'] > value]`.  hints: ["The condition `df['col'] > value` produces a boolean Series.", 'Pass the boolean Series inside `df[...]` to filter the rows.']  remediation→r02
  MEASURES: B:write_single_condition_filter(f2)   anchors=['practice', 'assessment:write_single_condition_filter']
  taught-before-tested: B.f2←s06

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

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

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
QUESTION [choice, intro, grading=client] You want to sort `orders` by `city` ascending and then by `delivery_time_minutes` descending. Which call is correct?
  ✔ opt_a: `orders.sort_values(by=['city', 'delivery_time_minutes'], ascending=[True, False])`
      why: Correct. Pass a list of booleans to `ascending`, matching the order of columns in `by`. The first column sorts ascending, the second descending.
  ✘ opt_b: `orders.sort_values(by=['city', 'delivery_time_minutes'], ascending=False)`
      why: A single boolean applies to all columns. To mix directions, pass a list of booleans: `ascending=[True, False]`.
  ✘ opt_c: `orders.sort_values(by='city', ascending=True).sort_values(by='delivery_time_minutes', ascending=False)`
      why: Chaining two single-column `sort_values()` calls does not produce the same result as one multi-column call. The second sort re-orders all rows by `delivery_time_minutes`, breaking the city grouping from the first sort. Use a single call with `by=[...]` and `ascending=[...]` instead.
  ✘ opt_d: `orders.sort_values(by=['city', 'delivery_time_minutes'], ascending=True)`
      why: A single boolean applies to all columns. To sort the first ascending and the second descending, pass `ascending=[True, False]`.
  feedback✔: Exactly. A list of booleans lets you set the direction for each column.  feedback✘: Remember: to mix sort directions, pass a list of booleans to `ascending`, one per column.  hints: ['The `ascending` parameter can be a list of booleans, one per column in `by`.', '`ascending=[True, False]` means the first column sorts ascending, the second descending.']  remediation→r01
  MEASURES: A:set_ascending_per_column(f2)   anchors=['assessment:set_ascending_per_column']
  taught-before-tested: A.f2←s01

### s03 · hands_on · Sort the orders DataFrame  [reward 10]
Hands-on — Sort orders by city ascending, then by delivery_time_minutes descending within each city.
QUESTION [code_exercise, core, grading=client] Load `orders.csv` and sort it using the provided variables:
1. Sort by the columns in `sort_cols` with the directions in `sort_directions` (True=ascending, False=descending).

Store the sorted DataFrame in `sorted_orders` and print it. Within each city, the longest delivery times should appear first.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=["df.sort_values(by='col')", 'df.sort_values(by=[...])', 'ascending=[True, False]', 'print()'] blocked=5 items
  file solution.py [editable]:
import pandas as pd

df = pd.read_csv('orders.csv')

# Sort criteria provided
sort_cols = ['city', 'delivery_time_minutes']
sort_directions = [True, False]  # True=ascending, False=descending

# TODO: sort by the columns in sort_cols with directions in sort_directions
# TODO: Store in sorted_orders and print it

  SOLUTION solution.py:
import pandas as pd

df = pd.read_csv('orders.csv')

# Sort criteria provided
sort_cols = ['city', 'delivery_time_minutes']
sort_directions = [True, False]  # True=ascending, False=descending

sorted_orders = df.sort_values(by=sort_cols, ascending=sort_directions)
print(sorted_orders)

  test t1 (value_equals, visible=True): {"expr":"sorted_orders['order_id'].tolist()","expected":[1014,1011,1008,1005,1002,1006,1003,1012,1009,1007,1013,1010,1004,1001]} | on-fail: The sorted order_ids should be [1014, 1011, 1008, 1005, 1002, 1006, 1003, 1012, 1009, 1007, 1013, 1010, 1004, 1001]. Check your sort columns and directions.
  test t2 (value_equals, visible=True): {"expr":"sorted_orders['city'].tolist()","expected":["Abuja","Abuja","Abuja","Abuja","Abuja","Kano","Kano","Kano","Kano","Lagos","Lagos","Lagos","Lagos","Lagos"]} | on-fail: The cities should be sorted alphabetically. Check that you used `ascending=[True, False]`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"6a97124557c1b58cd63aaa0668b4663248b1dac25b1b1c93308e565aa4cb03bc","tests_passed":2}
  feedback✔: Perfect! You sorted by city ascending and delivery time descending.  feedback✘: Review the `sort_values()` syntax: pass a list of columns to `by=` and a list of booleans to `ascending=`.  hints: ["Pass `by=['city', 'delivery_time_minutes']` to sort by both columns.", 'Pass `ascending=[True, False]` to sort the first ascending and the second descending.']  remediation→r01
  MEASURES: A:sort_by_one_or_more_columns(f1); A:set_ascending_per_column(f2)   anchors=['practice', 'assessment:sort_by_one_or_more_columns', 'assessment:set_ascending_per_column']
  taught-before-tested: A.f1←s01; A.f2←s01

### s04 · explainer · rename(): relabel columns and index entries with a dict  [reward 5]
Renaming — Clean up column names or row labels without rebuilding the DataFrame.
(definition) `rename()` relabels a DataFrame's axes using a dict mapping (or a function). Pass `columns=` to rename column labels: `orders.rename(columns={'delivery_time_minutes': 'delivery_min'})` renames that one column and leaves every other label unchanged. ⟦B.f1 B:tb1⟧
(mechanism) A single `rename()` call can rename columns and index labels together by passing both `columns=` and `index=` at once: `orders.rename(columns={'city': 'destination_city'}, index={0: 'first_order'})` relabels one column and one row label in one call — any label not in the mapping is left as-is. ⟦B.f2 B:tb2⟧
[BEFORE_AFTER] Two column labels are renamed; order_id and all other labels are unchanged.
  before:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] ] caption: orders — original column names
  after:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] highlights=[["column","city","→ destination_city"],["column","delivery_time_minutes","→ delivery_min"]]] caption: orders.rename(columns={'delivery_time_minutes': 'delivery_min', 'city': 'destination_city'})

### s05 · check · Renaming columns with a mapping  [reward 5]
Quick check — Identify the correct rename() call to relabel a column using a dict.
QUESTION [choice, core, grading=client] You want to rename the column `city` to `destination_city` and the index label `0` to `first_order` in a **single** `rename()` call. Which expression is correct?
  ✔ opt_a: `orders.rename(columns={'city': 'destination_city'}, index={0: 'first_order'})`
      why: Correct. Pass both `columns=` and `index=` in the same call, each with a mapping dict.
  ✘ opt_b: `orders.rename({'city': 'destination_city', 0: 'first_order'})`
      why: You must specify `columns=` and `index=` explicitly. Without them, pandas does not know which labels are columns and which are index entries.
  ✘ opt_c: `orders.rename(columns={'city': 'destination_city'}).rename(index={0: 'first_order'})`
      why: This works but uses two calls. The question asks for a single `rename()` call that handles both at once.
  ✘ opt_d: `orders.rename('city', 'destination_city', 0, 'first_order')`
      why: `rename()` takes keyword arguments `columns=` and `index=`, each with a mapping dict. It does not accept positional arguments for labels.
  feedback✔: Exactly. One `rename()` call can handle both columns and index.  feedback✘: Remember: pass `columns={...}` and `index={...}` in the same `rename()` call.  hints: ['`rename()` accepts both `columns=` and `index=` in one call.', 'Each parameter takes a dict mapping old labels to new labels.']  remediation→r02
  MEASURES: B:rename_columns_and_index_together(f2)   anchors=['assessment:rename_columns_and_index_together']
  taught-before-tested: B.f2←s04

### s06 · hands_on · Rename columns and an index label  [reward 10]
Hands-on — Rename two columns to clearer names and rename one index label in a single rename() call.
QUESTION [code_exercise, core, grading=client] Load `orders.csv` and rename using the provided mappings:
1. Rename columns using the `col_renames` dict.
2. Rename index labels using the `idx_renames` dict.

Store the renamed DataFrame in `renamed` and print it. All other labels should remain unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=['df.rename(columns={...})', 'df.rename(index={...})', 'df.rename(columns={...}, index={...})', 'print()'] blocked=4 items
  file solution.py [editable]:
import pandas as pd

df = pd.read_csv('orders.csv')

# Rename mappings provided
col_renames = {'city': 'destination_city', 'delivery_time_minutes': 'delivery_min'}
idx_renames = {0: 'first_order'}

# TODO: rename columns using col_renames and index using idx_renames
# TODO: Store in renamed and print it

  SOLUTION solution.py:
import pandas as pd

df = pd.read_csv('orders.csv')

# Rename mappings provided
col_renames = {'city': 'destination_city', 'delivery_time_minutes': 'delivery_min'}
idx_renames = {0: 'first_order'}

renamed = df.rename(columns=col_renames, index=idx_renames)
print(renamed)

  test t1 (value_equals, visible=True): {"expr":"renamed['destination_city'].tolist()","expected":["Lagos","Abuja","Kano","Lagos","Abuja","Kano","Lagos","Abuja","Kano","Lagos","Abuja","Kano","Lagos","Abuja"]} | on-fail: The column `destination_city` should contain the renamed city data. Check that you renamed `city`.
  test t2 (value_equals, visible=True): {"expr":"renamed['delivery_min'].tolist()","expected":[18,20,22,22,26,28,80,31,19,24,33,21,27,35]} | on-fail: The column `delivery_min` should contain the renamed delivery time data. Check that you renamed `delivery_time_minutes`.
  test t3 (value_equals, visible=True): {"expr":"renamed.loc['first_order', 'destination_city']","expected":"Lagos"} | on-fail: The first index label should be `first_order` and should point to the Lagos row. Check that you renamed index `0`.
  test t4 (value_equals, visible=None): {"expr":"renamed.loc['first_order', 'destination_city']","expected":"Lagos"} | on-fail: The renamed DataFrame should still contain the original data. Check that you used `rename()` correctly.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"46117440e0d31e926fc6be80bd773039e638efced3204b38f4715d207bf9cb80","tests_passed":4}
  feedback✔: Excellent! You renamed two columns and one index label in a single call.  feedback✘: Review the `rename()` syntax: pass `columns={...}` and `index={...}` in one call.  hints: ["Pass `columns={'old': 'new', ...}` to rename columns.", "Pass `index={0: 'first_order'}` to rename the index label 0."]  remediation→r02
  MEASURES: B:rename_columns_with_mapping(f1); B:rename_columns_and_index_together(f2)   anchors=['practice', 'assessment:rename_columns_with_mapping', 'assessment:rename_columns_and_index_together']
  taught-before-tested: B.f1←s04; B.f2←s04

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