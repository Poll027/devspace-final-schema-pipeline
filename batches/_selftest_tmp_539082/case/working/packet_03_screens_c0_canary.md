# EVALUATOR PACKET — DataFrames, Series, and Reading Data (tile_pandas_dataframe_reading)
Tile summary: Learn the two core pandas data structures — Series and DataFrame — and how to load tabular data from CSV and Excel files into a DataFrame.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.dataframe_series_model — Series and DataFrame data structures
B = pandas.reading_data — Reading data (read_csv, read_excel)

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (pandas.dataframe_series_model)   objective: Describe pandas' Series and DataFrame structures and how they relate, and construct a Series from a list and a DataFrame from a dict of lists.
A.f1: A pandas Series is a one-dimensional labeled array that can hold data of any type; its axis labels are collectively called the index.   [sources: pandas_docs_dsintro#series]
A.f2: A pandas DataFrame is a two-dimensional labeled data structure whose columns can hold different types, and it can be thought of as a dict of Series objects that share an index.   [sources: pandas_docs_dsintro#dataframe]
A.f3: A pandas Series can be constructed from data that is array-like, an Iterable (such as a Python list), a dict, or a scalar value. When built from a list (or other array-like data) with no index passed, the index defaults to 0, 1, ..., len(data) - 1; when built from a dict, the dict's keys become the index.   [sources: pandas_docs_series_api, pandas_docs_dsintro#series]
A.f4: A DataFrame can be constructed from a dict of equal-length lists, where each key becomes a column name and each list becomes that column's values.   [sources: pandas_docs_dsintro#from-dict-of-ndarrays-lists]
A.f5: A DataFrame can be treated like a dict of like-indexed Series: df['col'] gets a column, and df['new'] = ... sets (or adds) a column, using the same syntax as the analogous dict operations.   [sources: pandas_docs_dsintro#column-selection-addition-deletion]
note: Uses the same delivery-time values and city labels that recur across this batch's pandas concepts, for continuity.
PRACTICE ANCHOR (live_code): Create a Series from a list and a DataFrame from a dict of lists, pull one column out of the DataFrame, and say what type it is and how it relates to the DataFrame.  SUCCESS: The printed Series shows the default 0-based index, the printed DataFrame has one column per dict key, and the learner states that the pulled-out column is a Series sharing the DataFrame's index.
ASSESSMENT ANCHOR: construct_series_from_list_or_dict facts=['f1', 'f3']
ASSESSMENT ANCHOR: construct_dataframe_from_dict_of_lists facts=['f2', 'f4']
ASSESSMENT ANCHOR: relate_dataframe_columns_to_series facts=['f1', 'f2', 'f5']

## SOURCE FACTS — B (pandas.reading_data)   objective: Load tabular data from a CSV or Excel file into a DataFrame using read_csv or read_excel.
B.f1: read_csv() is the main pandas function for reading a delimited text file, such as a CSV file, into a DataFrame.   [sources: pandas_docs_io#csv-text-files]
B.f2: read_excel() reads an Excel file (such as a .xlsx workbook) into a DataFrame.   [sources: pandas_docs_io#excel-files]
B.f3: read_csv() takes the file path (or URL) to read as its first argument, and read_excel() additionally takes a sheet_name argument to choose which sheet of the workbook to load.   [sources: pandas_docs_io#csv-text-files, pandas_docs_io#excel-files]
B.f4: read_csv() accepts arguments such as sep to change the field delimiter used to parse the file (the default is a comma).   [sources: pandas_docs_io#csv-text-files]
note: TOC conflict: don't verify the loaded result with shape or head() here -- pandas.inspecting_dataframes, which teaches those, comes later and isn't in this concept's allowed knowledge.
note: Practice anchor confirms the load by printing the DataFrame and counting rows and columns, not shape or head(): those arrive in pandas.inspecting_dataframes (TOC conflict).
PRACTICE ANCHOR (live_code): Load a provided small CSV file into a DataFrame and print it to confirm the expected columns and rows arrived.  SUCCESS: The printed DataFrame shows every column named in the file and the learner's count of printed rows matches the file's record count.
ASSESSMENT ANCHOR: choose_read_csv_for_delimited_text facts=['f1']
ASSESSMENT ANCHOR: choose_read_excel_for_workbooks facts=['f2']
ASSESSMENT ANCHOR: set_path_sheet_name_and_sep_arguments facts=['f3', 'f4']

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

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply transform; Boolean/conditional filtering; Computing descriptive statistics with pandas (describe, mean, median, std); Concat stacking; Creating DataFrames from dicts/lists/files; DISTINCT for de-duplication; Exporting cleaned data (to_csv); Grouping and aggregation (groupby); Handling missing data (isna, dropna, fillna); Inspecting data (head, info, describe, shape, dtypes); Map substitution; Melt reshaping; Merge join; Pivot table reshaping; Reading data (read_csv, read_excel); Relational database and table structure basics; Removing duplicate rows; Renaming columns and index labels; SELECT statement fundamentals (columns, aliasing); Selecting rows/columns with loc/iloc; Sorting values; String cleaning with the .str accessor; Table and column aliasing for readability; Type conversion and dtype management (astype); WHERE clause filtering and comparison operators; Working with datetime data (to_datetime, date components)

## LESSON, in learner order

### s01 · explainer · Two building blocks: Series and DataFrame  [reward 5]
Series & DataFrame — Every pandas table is built from just two structures. Understanding them makes every later operation predictable.
(definition) A pandas **Series** is a one-dimensional labeled array that can hold data of any type. Its axis labels are collectively called the **index**. Think of it as a single column of a spreadsheet: each cell has a value, and each row has a label on the left. ⟦A.f1 A:tb1⟧
(example) A Series can be built from a Python list, a dict, or a scalar. `pd.Series([18, 20, 22, 22, 26, 28, 80])` — SwiftDrop delivery times — gets index labels 0 through 6 by default. `pd.Series({"Lagos": 18, "Abuja": 20, "Kano": 22})` uses the dict keys as the index instead. ⟦A.f3 A:tb2⟧
(definition) A pandas **DataFrame** is a two-dimensional labeled data structure whose columns can hold different types. It can be thought of as a dict of Series objects that all share the same index — one Series per column, all aligned row-by-row. ⟦A.f2 A:tb3⟧
[DIAGRAM: A DataFrame is a collection of Series sharing one index] nodes=['Index\n0\n1\n2', 'order_id\n1001\n1002\n1003', 'city\nLagos\nAbuja\nKano', 'delivery_time_minutes\n18\n20\n22'] edges=[('idx', 'col_order', 'shared index'), ('idx', 'col_city', 'shared index'), ('idx', 'col_dt', 'shared index')] alt: A DataFrame shown as three columns side by side — order_id, city, delivery_time_minutes — each highlighted as a Series, all sharing the same index (0, 1, 2) on the left.

### s02 · video · Series and DataFrame from plain Python data  [reward 3]
Series & DataFrame — Watch how a list becomes a Series and a dict of lists becomes a DataFrame.
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · explainer · Building a DataFrame and accessing columns  [reward 5]
Series & DataFrame — Pass a dict of equal-length lists to pd.DataFrame and use bracket notation to get or set columns.
(example) Pass a dict of equal-length lists to `pd.DataFrame()` and each key becomes a column name: `pd.DataFrame({"order_id": [1001, 1002, 1003], "city": ["Lagos", "Abuja", "Kano"], "delivery_time_minutes": [18, 20, 22]})` produces a three-column, three-row orders table. ⟦A.f4 A:tb4⟧
(mechanism) A DataFrame behaves like a dict of like-indexed Series. `orders['city']` returns the city column as a Series. `orders['courier'] = ['Ada', 'Bayo', 'Chidi']` adds a new column — the same bracket syntax you use to read or write a dict entry. ⟦A.f5 A:tb5⟧

### s04 · check · Columns and Series  [reward 5]
Quick check — Test your understanding of how DataFrame columns relate to Series.

### s05 · hands_on · Build a Series and a DataFrame  [reward 10]
Hands-on — Create a Series from a list of delivery times, build a DataFrame from a dict of lists, then pull one column out and confirm it is a Series.

### s06 · explainer · Loading CSV and Excel files into a DataFrame  [reward 5]
Reading Data — Delivery records often arrive as CSV exports or Excel workbooks. Two pandas functions cover both.
(intro) Before pandas can work with your delivery records, you read the file into a DataFrame. `pd.read_csv("orders.csv")` is the main function for reading a delimited text file — such as a CSV — into a DataFrame. `pd.read_excel("orders.xlsx", sheet_name="January")` reads an Excel workbook instead. ⟦B.f1 B.f2 B:tb1 B:tb2 B:tb3⟧
(mechanism) `read_csv()` takes the file path (or URL) as its first argument. `read_excel()` additionally takes `sheet_name` to choose which sheet to load — that is why the Excel call names `"January"` but the CSV call does not need to. `read_csv()` also accepts `sep` to change the field delimiter: `pd.read_csv("orders.csv", sep=";")` handles a semicolon-delimited export correctly. ⟦B.f3 B.f4 B:tb4 B:tb5⟧
[BEFORE_AFTER] pd.read_csv("orders.csv") turns the plain-text CSV on the left into the labeled DataFrame on the right.
  before:
[CODE python]
# orders.csv — plain text on disk
order_id,city,delivery_time_minutes
1001,Lagos,18
1002,Abuja,20
1003,Kano,22

# Read it into a DataFrame
import pandas as pd
orders = pd.read_csv("orders.csv")
  annotations: ['CSV file: comma-separated plain text with a header row', 'File path is the first argument; pandas infers the header from row 1']
  after:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] tags=order_id:from CSV header, city:from CSV header, delivery_time_minutes:from CSV header] caption: The DataFrame produced by pd.read_csv("orders.csv") — columns taken from the header row, index added automatically.

### s07 · video · Reading a CSV into a DataFrame  [reward 3]
Reading Data — Watch a one-line read_csv call load a file into a DataFrame.
[VIDEO ] bridge-before:  | bridge-after: 

### s08 · check · Choosing the right reader  [reward 5]
Quick check — Which pandas function do you call for a CSV file, and which for an Excel workbook?

### s09 · check · Arguments: path, sheet_name, and sep  [reward 5]
Quick check — Test your knowledge of the key arguments for read_csv and read_excel.

### s10 · hands_on · Load the SwiftDrop orders CSV  [reward 10]
Hands-on — Load the provided orders CSV into a DataFrame and print it to confirm the expected columns and rows arrived.

### s11 · recap · What you've learned  [reward 5]
Recap — Two structures, two readers — the foundation for every pandas operation ahead.
(takeaway) A **Series** is a one-dimensional labeled array; a **DataFrame** is a collection of Series sharing one index. Pull a column with `df['col']` and you get a Series back. `pd.read_csv()` loads a delimited text file; `pd.read_excel()` loads a workbook. Either way, the result is a DataFrame ready to work with. ⟦A.f1 A.f2 B.f1 B.f2 A:tb6 B:tb6⟧
[UP NEXT] Up next: Creating and Inspecting DataFrames: Not every DataFrame starts life as a file — sometimes delivery data already exists as Python data and you build the table directly from it. Next: creating DataFrames from Python objects and using head, shape, dtypes, info, and describe.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Columns are Series — a closer look — A DataFrame column and a Series are the same thing. Here's the contrast that makes it click.
(definition) A **Series** is a one-dimensional labeled array — its labels are the index. A **DataFrame** is a two-dimensional structure you can think of as a dict of Series sharing one index. Every column in a DataFrame is itself a Series. ⟦A.f1 A.f2 A:tb1 A:tb3⟧
(mechanism) Use `orders['delivery_time_minutes']` to pull the delivery-time column out of the SwiftDrop orders table. The result is a Series — the same one-dimensional, indexed structure — sharing the DataFrame's index. `orders['courier'] = ['Ada', 'Bayo', 'Chidi']` adds a new column using the same dict-style syntax. ⟦A.f5 A:tb5⟧
### r02 · Constructing a Series and a DataFrame — Two constructors, two input shapes — here is the contrast.
(example) Pass a Python list to `pd.Series()` and the index defaults to 0, 1, …, n−1. Pass a dict and the dict's keys become the index labels. `pd.Series([18, 20, 22, 22, 26, 28, 80])` gives index 0–6; `pd.Series({"Lagos": 18, "Abuja": 20, "Kano": 22})` gives city-name labels. ⟦A.f3 A:tb2⟧
(example) Pass a dict of equal-length lists to `pd.DataFrame()` and each key becomes a column name. `pd.DataFrame({"order_id": [1001, 1002, 1003], "city": ["Lagos", "Abuja", "Kano"], "delivery_time_minutes": [18, 20, 22]})` builds a three-column, three-row orders table. ⟦A.f4 A:tb4⟧
### r03 · read_csv vs read_excel — which file, which function — The file extension tells you which reader to call.
(definition) `pd.read_csv()` is the main pandas function for reading a delimited text file — such as a CSV — into a DataFrame. `pd.read_excel()` reads an Excel file (such as a .xlsx workbook) into a DataFrame. Use `read_csv` for `orders.csv`; use `read_excel` for `orders.xlsx`. ⟦B.f1 B.f2 B:tb2 B:tb3⟧
### r04 · Key arguments: path, sheet_name, and sep — Three arguments cover the most common reading scenarios.
(mechanism) `read_csv()` takes the file path (or URL) as its first argument. `read_excel()` additionally takes `sheet_name` to choose which sheet to load — that is why `pd.read_excel("orders.xlsx", sheet_name="January")` names the sheet but `pd.read_csv("orders.csv")` does not need to. `read_csv()` also accepts `sep` to change the delimiter: `pd.read_csv("orders.csv", sep=";")` handles a semicolon-delimited export. ⟦B.f3 B.f4 B:tb4 B:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· nodes.label: order_id
1001
1002
1003
· nodes.label: city
Lagos
Abuja
Kano
· nodes.label: delivery_time_minutes
18
20
22