# EVALUATOR PACKET — DataFrames, Series, and Reading Data (tile_pandas_dataframe_reading)
Tile summary: Learn the two core pandas data structures — Series and DataFrame — and how to load tabular data from CSV and Excel files into a DataFrame.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.dataframe_series_model — Series and DataFrame data structures
B = pandas.reading_data — Reading data (read_csv, read_excel)

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=0

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
[VIDEO Series and DataFrame from plain Python data] bridge-before: Clip 1 shows a Series from a list; clip 2 builds a DataFrame from a dict of lists and shows that one column is a Series. Neither builds a Series from a dict, and neither adds a column with df['new'] = ... | bridge-after: Devspace fills both gaps: a Series built from a dict takes the dict's keys as its index, and df['new'] = ... adds a column using dict-style assignment.
  - W6WFX_H-AA4 0-161s facts=['f1'] label: A Series built from a Python list: one labelled column of any data type with a default 0, 1, 2 index | summary: Introduces a Series as a one-dimensional labelled array, like a single column in a spreadsheet, using a hallway of numbered apartments as the picture. A short list of three integers becomes a Series with pd.Series. Printing it shows the values in one column, the labels 0, 1, 2 on the left (the index) and the data type underneath. Changing the list to decimals, letters or True/False values changes that type to float, object or bool. It ends by noting the default labels start at 0 and go up by one, and that custom labels can be set.
  - zmdjNSmRXF4 189-668s facts=['f1', 'f2', 'f4'] label: From a dict of lists to a DataFrame: rows, columns, and a single column as a Series | summary: Builds the DataFrame idea in plain Python first: a dict whose keys play the role of columns and whose list values hold the rows. Passing that dict to pd.DataFrame prints a table with an index of 0, 1, 2 on the left. Selecting one column with the same bracket syntax used for a dict key returns a Series, which the presenter describes as one-dimensional, so a DataFrame is a container of several Series that share the index. Working with the index itself is left for a later video.

### s03 · explainer · Building a DataFrame and accessing columns  [reward 5]
Series & DataFrame — Pass a dict of equal-length lists to pd.DataFrame and use bracket notation to get or set columns.
(example) Pass a dict of equal-length lists to `pd.DataFrame()` and each key becomes a column name: `pd.DataFrame({"order_id": [1001, 1002, 1003], "city": ["Lagos", "Abuja", "Kano"], "delivery_time_minutes": [18, 20, 22]})` produces a three-column, three-row orders table. ⟦A.f4 A:tb4⟧
(mechanism) A DataFrame behaves like a dict of like-indexed Series. `orders['city']` returns the city column as a Series. `orders['courier'] = ['Ada', 'Bayo', 'Chidi']` adds a new column — the same bracket syntax you use to read or write a dict entry. ⟦A.f5 A:tb5⟧

### s04 · check · Columns and Series  [reward 5]
Quick check — Test your understanding of how DataFrame columns relate to Series.
QUESTION [choice, core, grading=client] You have a DataFrame called `orders` with columns `order_id`, `city`, and `delivery_time_minutes`. What is the type of `orders['city']`, and how does it relate to the DataFrame?
  ✔ opt_a: It is a pandas Series that shares the same index as the DataFrame.
      why: Correct. `df['col']` returns a Series — the same one-dimensional, indexed structure that a DataFrame is built from. It shares the DataFrame's index.
  ✘ opt_b: It is a Python list extracted from the DataFrame.
      why: Not quite. `df['col']` uses dict-like syntax, but the result is a pandas Series, not a plain Python list. A Series carries index labels alongside its values.
  ✘ opt_c: It is a new DataFrame containing only the `city` column.
      why: A single-column selection with `df['col']` returns a Series, not a DataFrame. To get a one-column DataFrame you would use double brackets: `df[['col']]`.
  ✘ opt_d: It is a dict mapping index labels to city values.
      why: A pandas Series is not a dict, even though a DataFrame can be thought of as a dict of Series. `df['city']` returns a Series with an integer index, not a dict.
  feedback✔: Exactly right. A DataFrame is a collection of like-indexed Series objects, so pulling out a column with `df['col']` gives you back one of those Series.  feedback✘: Remember: a DataFrame can be thought of as a dict of Series that share an index. Selecting a column with `df['col']` returns one of those Series.  hints: ['Think about what a DataFrame is made of at its core.', "The teaching block said: 'A DataFrame can be treated like a dict of like-indexed Series.'"]  remediation→r01
  MEASURES: A:relate_dataframe_columns_to_series(f1,f2,f5)   anchors=['assessment:relate_dataframe_columns_to_series']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f5←s03

### s05 · hands_on · Build a Series and a DataFrame  [reward 10]
Hands-on — Create a Series from a list of delivery times, build a DataFrame from a dict of lists, then pull one column out and confirm it is a Series.
QUESTION [code_exercise, core, grading=client] Complete the script to:
1. `first_time` is already set to `18` (the first delivery time). Build `delivery_times = [first_time, 20, 22, 22, 26, 28, 80]` and a Series `s` from it; print `s`.
2. Build a DataFrame `df` from the `data` dict (keys: `order_id`, `city`, `delivery_time_minutes`) and print it.
3. Pull out the column named by `col_name` from `df` into `col` and print its type.

Use only `pd.Series(list)`, `pd.DataFrame(dict_of_lists)`, `df['col']`, `print()`, and `type()`.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=['import pandas as pd', 'pd.Series(list)', 'pd.DataFrame(dict_of_lists)', "df['col']", 'print()', 'type()'] blocked=7 items
  file starter.py [editable]:
import pandas as pd

# First delivery time (minutes) — change this to test your code
first_time = 18

# Delivery times list — uses first_time as the first element
delivery_times = [first_time, 20, 22, 22, 26, 28, 80]

# Data dict for the DataFrame
data = {
    'order_id': [1001, 1002, 1003],
    'city': ['Lagos', 'Abuja', 'Kano'],
    'delivery_time_minutes': [first_time, 20, 26]
}

# Column to select
col_name = 'delivery_time_minutes'

# TODO: Create a Series from delivery_times and print it

# TODO: Create a DataFrame from data and print it

# TODO: Pull out the col_name column from df and print its type

  SOLUTION starter.py:
import pandas as pd

# First delivery time (minutes) — change this to test your code
first_time = 18

# Delivery times list — uses first_time as the first element
delivery_times = [first_time, 20, 22, 22, 26, 28, 80]

# Data dict for the DataFrame
data = {
    'order_id': [1001, 1002, 1003],
    'city': ['Lagos', 'Abuja', 'Kano'],
    'delivery_time_minutes': [first_time, 20, 26]
}

# Column to select
col_name = 'delivery_time_minutes'

# Create a Series from delivery_times and print it
s = pd.Series(delivery_times)
print(s)

# Create a DataFrame from data and print it
df = pd.DataFrame(data)
print(df)

# Pull out the col_name column from df and print its type
col = df[col_name]
print(type(col))

  test ix.tile_pandas_dataframe_reading.s05.t1 (value_equals, visible=True): {"expr":"s.tolist()","expected":[18,20,22,22,26,28,80]} | on-fail: Make sure `s = pd.Series(delivery_times)` where `delivery_times = [first_time, 20, 22, 22, 26, 28, 80]` and `first_time = 18`.
  test ix.tile_pandas_dataframe_reading.s05.t2 (dataframe_equals, visible=True): {"expr":"df","expected":{"columns":["order_id","city","delivery_time_minutes"],"rows":[[1001,"Lagos",18],[1002,"Abuja",20],[1003,"Kano",26]]},"ordered":true} | on-fail: Make sure `df = pd.DataFrame(data)` where `data` has keys `order_id`, `city`, `delivery_time_minutes` with the given lists.
  test ix.tile_pandas_dataframe_reading.s05.t3 (value_equals, visible=True): {"expr":"col.tolist()","expected":[18,20,26]} | on-fail: Use `col = df['delivery_time_minutes']` to pull out the column. Its values should match `data['delivery_time_minutes']`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"f61d92d95081ac84f0b102389a0bc3a002577f4eeab03ea751513377132a75d4","tests_passed":3}
  feedback✔: Well done! You built a Series from a list, a DataFrame from a dict of lists, and confirmed that a column pulled from a DataFrame is itself a Series.  feedback✘: Check that you used `pd.Series(delivery_times)` for the Series, `pd.DataFrame(data)` for the DataFrame, and `df[col_name]` to select the column.  hints: ['Start with `s = pd.Series(delivery_times)` — pass the list directly.', 'For the DataFrame, pass the whole `data` dict to `pd.DataFrame()`.']  remediation→r02
  MEASURES: A:construct_series_from_list_or_dict(f1,f3); A:construct_dataframe_from_dict_of_lists(f2,f4); A:relate_dataframe_columns_to_series(f1,f2,f5)   anchors=['practice', 'assessment:construct_series_from_list_or_dict', 'assessment:construct_dataframe_from_dict_of_lists', 'assessment:relate_dataframe_columns_to_series']
  taught-before-tested: A.f1←s01; A.f3←s01; A.f2←s01; A.f4←s03; A.f1←s01; A.f2←s01; A.f5←s03

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
[VIDEO Reading a CSV into a DataFrame] bridge-before: Watch the one-line read_csv call with the file path as its first argument. The r before the path string is only a Windows-path workaround, not a read_csv setting. | bridge-after: The clip covers only read_csv with a path. Devspace adds read_excel with sheet_name, and read_csv's sep argument for files that use something other than commas.
  - dUpyC40cF6Q 58-172s facts=['f1'] label: Reading a CSV into a DataFrame with pd.read_csv | summary: Calls pd.read_csv on a countries CSV: the file's path is copied, pasted as the argument and run, which returns a DataFrame rather than a plain string. The first run fails with a Unicode error because of the backslashes in a Windows path, which is fixed by putting r before the string. The result shows country and region columns, with the headers taken from the file and an index added on the left. read_excel, the sep argument and sheet_name do not appear.

### s08 · check · Choosing the right reader  [reward 5]
Quick check — Which pandas function do you call for a CSV file, and which for an Excel workbook?
QUESTION [choice, intro, grading=client] A colleague sends you two files: `deliveries.csv` (a comma-separated text file) and `deliveries.xlsx` (an Excel workbook). Which pandas functions do you use to load each file into a DataFrame?
  ✔ opt_a: `pd.read_csv()` for the CSV and `pd.read_excel()` for the Excel file.
      why: Correct. `pd.read_csv()` reads delimited text files like CSV, and `pd.read_excel()` reads Excel workbooks (.xlsx).
  ✘ opt_b: `pd.read_excel()` for both, because Excel can also open CSV files.
      why: While Excel can open CSV files in the application, `pd.read_excel()` expects a binary Excel workbook format. Use `pd.read_csv()` for `.csv` files.
  ✘ opt_c: `pd.read_csv()` for both, because CSV is the universal format.
      why: `pd.read_csv()` reads delimited text files, not Excel workbooks. Passing an `.xlsx` file to `pd.read_csv()` will raise an error.
  ✘ opt_d: `pd.read_table()` for the CSV and `pd.read_csv()` for the Excel file.
      why: `pd.read_table()` is not the main function taught here, and `pd.read_csv()` does not read Excel workbooks. Use `pd.read_csv()` for CSV and `pd.read_excel()` for `.xlsx`.
  feedback✔: Right. Each file format has its own reader: `read_csv` for delimited text, `read_excel` for Excel workbooks.  feedback✘: Each file format needs its own reader. `pd.read_csv()` is for delimited text files like `.csv`; `pd.read_excel()` is for Excel workbooks like `.xlsx`.  hints: ['The function name matches the file type: `read_csv` for CSV, `read_excel` for Excel.', 'Think about what each function name describes.']  remediation→r03
  MEASURES: B:choose_read_csv_for_delimited_text(f1); B:choose_read_excel_for_workbooks(f2)   anchors=['assessment:choose_read_csv_for_delimited_text', 'assessment:choose_read_excel_for_workbooks']
  taught-before-tested: B.f1←s06; B.f2←s06

### s09 · check · Arguments: path, sheet_name, and sep  [reward 5]
Quick check — Test your knowledge of the key arguments for read_csv and read_excel.
QUESTION [choice, core, grading=client] A delivery export file uses a semicolon (`;`) as its delimiter instead of a comma. Which call correctly reads it into a DataFrame?
  ✔ opt_a: `pd.read_csv("deliveries.csv", sep=";")`
      why: Correct. `sep=";"` tells `read_csv()` to split fields on semicolons instead of the default comma.
  ✘ opt_b: `pd.read_csv("deliveries.csv", delimiter=",")`
      why: The argument name is `sep`, not `delimiter` (though `delimiter` is an alias, the value here is wrong: passing `","` keeps the default comma separator, which won't parse a semicolon-delimited file correctly).
  ✘ opt_c: `pd.read_excel("deliveries.csv", sheet_name="Sheet1")`
      why: `pd.read_excel()` reads Excel workbooks, not CSV files. The `sheet_name` argument is for Excel sheets, not CSV files.
  ✘ opt_d: `pd.read_csv("deliveries.csv")`
      why: Without `sep=";"`, `read_csv()` uses the default comma separator. A semicolon-delimited file would be read as a single column.
  feedback✔: Exactly. `sep` lets you override the default comma delimiter. The file path is always the first argument.  feedback✘: When the delimiter is not a comma, pass `sep=";"` (or whatever character is used) as a keyword argument to `pd.read_csv()`.  hints: ['The default separator for `read_csv` is a comma. What argument changes it?', 'Look at the `sep` parameter of `pd.read_csv()`.']  remediation→r04
  MEASURES: B:set_path_sheet_name_and_sep_arguments(f3,f4)   anchors=['assessment:set_path_sheet_name_and_sep_arguments']
  taught-before-tested: B.f3←s06; B.f4←s06

### s10 · hands_on · Load the SwiftDrop orders CSV  [reward 10]
Hands-on — Load the provided orders CSV into a DataFrame and print it to confirm the expected columns and rows arrived.
QUESTION [code_exercise, intro, grading=client] The file `orders.csv` contains SwiftDrop delivery records. Read it into a DataFrame called `orders` using `pd.read_csv()`, then print the DataFrame.

After running your code, the output should show all 10 columns (`order_id`, `city`, `city_code`, `courier`, `driver_id`, `customer_id`, `pickup_date`, `delivery_time_minutes`, `distance_km`, `order_value`) and all 14 rows.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pandas']} constraints.allowed=['import pandas as pd', 'pd.read_csv(path)', 'pd.read_csv(path, sep=...)', 'pd.read_excel(path, sheet_name=...)', 'print(df)'] blocked=5 items
  file starter.py [editable]:
import pandas as pd

# File path provided for you
file_path = 'orders.csv'

# TODO: Load the CSV file and print the DataFrame

  SOLUTION starter.py:
import pandas as pd

# File path provided for you
file_path = 'orders.csv'

# Load the CSV file and print the DataFrame
orders = pd.read_csv(file_path)
print(orders)

  test ix.tile_pandas_dataframe_reading.s10.t1 (dataframe_equals, visible=True): {"expr":"orders","expected":{"columns":["order_id","city","city_code","courier","driver_id","customer_id","pickup_date","delivery_time_minutes","distance_km","order_value"],"rows":[[1001,"Lagos","LOS","Ada",201,301,"2024-03-14",18,4.2,2500],[1002,"Abuja","ABJ","Bayo",202,302,"2024-03-14",20,6.1,3100],[1003,"Kano","KAN","Chidi",203,303,"2024-03-15",22,5.5,1800],[1004,"Lagos","LOS","Ada",201,304,"2024-03-15",22,3.8,2200],[1005,"Abuja","ABJ","Bayo",202,305,"2024-03-16",26,7.3,4000],[1006,"Kano","KA | on-fail: Make sure you read `orders.csv` with `pd.read_csv('orders.csv')` and assign the result to a variable called `orders`.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"600a7abec1d18efc71841493ba04059793aff976401932efebc1000fb08bf8ca","tests_passed":1}
  feedback✔: Great work! You loaded the CSV into a DataFrame with all 10 columns and 14 rows. That's the first step in every pandas workflow.  feedback✘: Use `orders = pd.read_csv('orders.csv')` to load the file. Make sure the variable is named `orders` and you print it.  hints: ["The file path is the first argument: `pd.read_csv('orders.csv')`.", 'Assign the result to `orders`, then call `print(orders)`.']  remediation→r03
  MEASURES: B:choose_read_csv_for_delimited_text(f1); B:set_path_sheet_name_and_sep_arguments(f3)   anchors=['practice']
  taught-before-tested: B.f1←s06; B.f3←s06

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