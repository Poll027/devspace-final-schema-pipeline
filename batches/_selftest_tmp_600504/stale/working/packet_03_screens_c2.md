# EVALUATOR PACKET — Type Conversion and Datetime Handling (tile_pandas_dtype_datetime)
Tile summary: Learn to convert column dtypes with astype and to work with datetime data using pd.to_datetime and the .dt accessor.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.dtype_conversion — Type conversion and dtype management (astype)
B = pandas.datetime_handling — Working with datetime data (to_datetime, date components)

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (pandas.dtype_conversion)   objective: Convert a DataFrame column's dtype to a different, correct dtype using astype.
A.f1: The astype() method explicitly converts a column's (or Series') values from one dtype to another, returning a copy by default, and it raises an exception if the requested conversion is invalid.   [sources: pandas_docs_basics#astype]
A.f2: astype() can convert a single column, a subset of a DataFrame's columns at once, or specific columns to specific dtypes by passing a dict mapping column names to target dtypes.   [sources: pandas_docs_basics#astype]
PRACTICE ANCHOR (live_code): Convert a column of numeric strings to a proper numeric dtype using astype.  SUCCESS: dtypes shows the column as a numeric type after conversion, and a numeric operation on the column now works.
ASSESSMENT ANCHOR: convert_column_dtype_with_astype facts=['f1']
ASSESSMENT ANCHOR: convert_multiple_columns_with_dict facts=['f2']

## SOURCE FACTS — B (pandas.datetime_handling)   objective: Convert a column of date-like text to pandas datetime values with to_datetime, and extract date components using the .dt accessor.
B.f1: The to_datetime() function converts a Series (or list-like) of date-like strings or other date-like values into pandas datetime values; when passed a Series, it returns a Series with the same index.   [sources: pandas_docs_timeseries#converting-to-timestamps]
B.f2: Once a column has a datetime dtype, its .dt accessor exposes date/time component properties, such as year, month, and day, for each value.   [sources: pandas_docs_timeseries#time-date-components]
PRACTICE ANCHOR (live_code): Convert a text date column to datetime and add a new column extracting just the month.  SUCCESS: dtypes shows the date column as a datetime type, and the new column holds the month number for every row.
ASSESSMENT ANCHOR: convert_text_column_with_to_datetime facts=['f1']
ASSESSMENT ANCHOR: extract_date_components_with_dt facts=['f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Aggregate functions (COUNT, SUM, AVG, MIN, MAX); Apply transform; CASE expressions for conditional logic in queries; Concat stacking; DISTINCT for de-duplication; Exporting cleaned data (to_csv); GROUP BY grouping semantics; Grouping and aggregation (groupby); HAVING clause for filtering aggregated groups; Handling missing data (isna, dropna, fillna); Limiting results (LIMIT/OFFSET); Logical operators (AND, OR, NOT) in filtering; Map substitution; Melt reshaping; Merge join; NULL handling (IS NULL / IS NOT NULL); Pivot table reshaping; Relational database and table structure basics; Removing duplicate rows; SELECT statement fundamentals (columns, aliasing); SQL formatting/naming conventions per style guide; Sorting results with ORDER BY (ASC/DESC); String cleaning with the .str accessor; Table and column aliasing for readability; WHERE clause filtering and comparison operators; Working with datetime data (to_datetime, date components)

## LESSON, in learner order

### s01 · explainer · Fixing column types with astype  [reward 5]
Type Conversion — When a CSV loads numbers as text, arithmetic fails. astype() converts a column to the right dtype in one call.
(intro) Suppose the SwiftDrop export loads `distance_km` as text — values like `"12.5"` instead of actual floats. Until the dtype is fixed, pandas treats the column as strings and arithmetic on it will fail. ⟦A:tb1⟧
(definition) The `astype()` method explicitly converts a column's values from one dtype to another, returning a copy by default. It raises an exception if the conversion is invalid — so `orders["distance_km"].astype(float)` converts text values to floats, but a row containing `"unknown"` would raise an error rather than silently guessing. ⟦A.f1 A:tb2⟧
(example) `astype()` can convert multiple columns at once by passing a dict: `orders.astype({"distance_km": float, "order_id": str})` converts two columns to two different target types in a single call. ⟦A.f2 A:tb3⟧
[BEFORE_AFTER] distance_km column converted from object (text) to float64 using astype(float).
  before:
[CODE python]
# distance_km loaded as object (text)
print(orders["distance_km"].dtype)  # object
print(orders["distance_km"].head())  # '4.2', '6.1', '5.5' ...
  annotations: ["dtype is 'object' — pandas stores these as strings", 'Values look numeric but are text; arithmetic would fail']
  after:
[CODE python]
orders["distance_km"] = orders["distance_km"].astype(float)
print(orders["distance_km"].dtype)  # float64
# Now arithmetic works: orders["distance_km"].mean()
  annotations: ['astype(float) converts every text value to a real float', 'dtype is now float64 — arithmetic is possible']

### s02 · video · astype in action  [reward 3]
Type Conversion — Watch a column's dtype change from object to a numeric type with a single astype call.
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Converting multiple columns at once  [reward 5]
Quick check — Test your understanding of how astype handles multiple columns.

### s04 · hands_on · Convert a column's dtype with astype  [reward 10]
Hands-on — Use astype to convert the distance_km column from text to float in the SwiftDrop orders dataset.

### s05 · explainer · Turning date text into real datetimes  [reward 5]
Datetime Handling — A pickup_date column stored as text can't answer date questions. pd.to_datetime converts it, and .dt unlocks its components.
(intro) Suppose the SwiftDrop export records each order's `pickup_date` as plain text — `"2024-03-14"`. Before you can ask which month had the most deliveries, that text needs to become an actual datetime value. ⟦B:tb1⟧
(definition) `pd.to_datetime()` converts a Series of date-like strings into pandas datetime values, returning a Series with the same index: `orders["pickup_date"] = pd.to_datetime(orders["pickup_date"])` replaces the text column with genuine datetime values, one per order, in the same row positions. ⟦B.f1 B:tb2⟧
(mechanism) Once a column has a datetime dtype, its `.dt` accessor exposes date component properties for each value: `orders["pickup_month"] = orders["pickup_date"].dt.month` pulls just the month number out of every pickup date at once. ⟦B.f2 B:tb3⟧
[BEFORE_AFTER] pickup_date converted from object to datetime64 with pd.to_datetime; a new pickup_month column extracted via .dt.month.
  before:
[CODE python]
# pickup_date is object dtype (text)
print(orders["pickup_date"].dtype)   # object
print(orders["pickup_date"].head())  # '2024-03-14', '2024-03-14', '2024-03-15', ...
  annotations: ["dtype is 'object' — dates stored as plain strings", "Values look like dates but pandas can't do date arithmetic yet"]
  after:
[CODE python]
orders["pickup_date"] = pd.to_datetime(orders["pickup_date"])
orders["pickup_month"] = orders["pickup_date"].dt.month
print(orders["pickup_date"].dtype)   # datetime64[ns]
print(orders[["pickup_date", "pickup_month"]].head())
  annotations: ['to_datetime converts text strings to real datetime values', '.dt.month extracts the month number from each datetime', 'dtype is now datetime64[ns]']

### s06 · video · Converting a text date column with pd.to_datetime  [reward 3]
Datetime Handling — Watch a text date column fail, then succeed after pd.to_datetime converts it.
[VIDEO ] bridge-before:  | bridge-after: 

### s07 · check · Extracting date components with .dt  [reward 5]
Quick check — Test your understanding of the .dt accessor and its component properties.

### s08 · hands_on · Convert dates and extract a month column  [reward 10]
Hands-on — Convert the pickup_date column to datetime and add a pickup_month column using the .dt accessor.

### s09 · recap · Type conversion and datetime handling — key takeaways  [reward 5]
Recap — Two tools for fixing column types: astype for general conversions, to_datetime for dates.
(takeaway) `astype()` is the general-purpose dtype converter — pass a target type for one column or a dict for several at once. It raises an exception on invalid conversions rather than guessing. For date columns, `pd.to_datetime()` is the one-time conversion step; after that, `.dt` unlocks pulling out whatever date component the analysis needs. ⟦A.f1 A.f2 B.f1 B.f2 A:tb4 B:tb4⟧
[UP NEXT] Up next: Text Cleaning, Duplicates, and Missing Data: Next you'll clean messy text columns with the .str accessor, remove duplicate rows, and handle missing values — the three most common data-quality fixes after dtype correction.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Converting multiple columns with a dict — astype accepts a dict so you can convert several columns to different types in one call.
(definition) `astype()` can convert a single column or multiple columns at once. Pass a dict mapping column names to target dtypes: `orders.astype({"distance_km": float, "order_id": str})` converts `distance_km` to float and `order_id` to string in one call — no need to call astype twice. ⟦A.f2 A:tb3⟧
[BEFORE_AFTER] Two separate astype calls replaced by one dict-based call.
  before:
[CODE python]
# Two separate astype calls — works but verbose
orders["distance_km"] = orders["distance_km"].astype(float)
orders["order_id"] = orders["order_id"].astype(str)
  annotations: ['Two separate calls — one per column']
  after:
[CODE python]
# One astype call with a dict — converts both columns at once
orders = orders.astype({"distance_km": float, "order_id": str})
  annotations: ['Dict maps each column name to its target dtype']
### r02 · Extracting date components with .dt — After converting a column to datetime, the .dt accessor exposes year, month, day, and more for every row at once.
(mechanism) Once a column has a datetime dtype, its `.dt` accessor exposes date/time component properties — such as `year`, `month`, and `day` — for each value: `orders["pickup_month"] = orders["pickup_date"].dt.month` pulls just the month number out of every pickup date at once. Without the `.dt` accessor, you cannot access these properties on a datetime Series. ⟦B.f2 B:tb3⟧
[BEFORE_AFTER] pickup_date converted to datetime; month and day extracted via .dt accessor.
  before:
[CODE python]
# pickup_date is still text — .dt is not available
# orders["pickup_date"].dt.month  # AttributeError
  annotations: ['Text column has no .dt accessor — must convert first']
  after:
[CODE python]
orders["pickup_date"] = pd.to_datetime(orders["pickup_date"])
orders["pickup_month"] = orders["pickup_date"].dt.month
orders["pickup_day"]   = orders["pickup_date"].dt.day
  annotations: ['Convert once with to_datetime', '.dt.month and .dt.day each extract one component for every row']

=========

# EVALUATOR PACKET — Text Cleaning, Duplicates, and Missing Data (tile_pandas_text_dupes_missing)
Tile summary: Clean text columns with the .str accessor, remove duplicate rows with drop_duplicates, and handle missing values with isna, dropna, and fillna.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = pandas.str_accessor_cleaning — String cleaning with the .str accessor
B = pandas.drop_duplicates — Removing duplicate rows
C = pandas.missing_data_handling — Handling missing data (isna, dropna, fillna)

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (pandas.str_accessor_cleaning)   objective: Clean and transform a text column using the .str accessor's vectorized string methods, such as strip, lower, and replace.
A.f1: A Series' .str accessor lets you call ordinary string-processing methods, matching the names of Python's built-in string methods (such as lower, strip, and replace), on every element of the Series at once.   [sources: pandas_docs_text#string-methods]
note: Skip the optional fact about .str methods excluding missing values automatically -- not required.
PRACTICE ANCHOR (live_code): Use the .str accessor to lowercase and strip whitespace from every value in a text column.  SUCCESS: Every value in the printed column is lowercase with no leading or trailing spaces, and the variants of the same city now match.
ASSESSMENT ANCHOR: apply_string_methods_across_column facts=['f1']

## SOURCE FACTS — B (pandas.drop_duplicates)   objective: Remove duplicate rows from a DataFrame using drop_duplicates, based on the correct columns and the intended occurrence to keep.
B.f1: duplicated() returns a boolean vector indicating which rows are duplicates, and drop_duplicates() removes duplicate rows; both take as an argument the columns used to identify a duplicated row.   [sources: pandas_docs_indexing#duplicate-data]
B.f2: By default, drop_duplicates() keeps the first occurrence of each duplicate set and drops the rest; passing keep='last' keeps the last occurrence instead, and keep=False drops every row that is part of a duplicate set.   [sources: pandas_docs_indexing#duplicate-data]
PRACTICE ANCHOR (live_code): Remove duplicate customer rows based on a customer ID column, keeping the first occurrence.  SUCCESS: The printed DataFrame has one row per customer ID, and for each repeated ID the row that came first in the original data is the one kept.
ASSESSMENT ANCHOR: identify_duplicates_with_subset facts=['f1']
ASSESSMENT ANCHOR: choose_which_occurrence_to_keep facts=['f2']

## SOURCE FACTS — C (pandas.missing_data_handling)   objective: Detect, drop, or fill missing values in a DataFrame using isna, dropna, and fillna.
C.f1: isna() (and its complement notna()) detects which values in a Series or DataFrame are missing.   [sources: pandas_docs_missing_data#values-considered-missing]
C.f2: dropna() removes rows that contain missing values; passing a subset of column labels restricts which columns are checked when deciding whether a row counts as having a missing value.   [sources: pandas_docs_missing_data#dropping-missing-data, pandas_docs_dataframe_dropna]
C.f3: fillna() replaces missing (NA) values with a specified value, such as a scalar (for example, replacing every missing value in a column with 0).   [sources: pandas_docs_missing_data#filling-missing-data]
note: Skip the optional fact that isna() also treats None as missing -- not required.
PRACTICE ANCHOR (live_code): Detect missing values in a DataFrame, drop rows missing a required field, and fill a numeric column's remaining gaps with its median.  SUCCESS: The mask shows the missing cells, no row is missing the required field afterwards, and the numeric column has no gaps, with filled cells equal to that column's median.
ASSESSMENT ANCHOR: detect_missing_values facts=['f1']
ASSESSMENT ANCHOR: drop_rows_missing_required_field facts=['f2']
ASSESSMENT ANCHOR: fill_missing_values_with_value_or_median facts=['f3']
ASSESSMENT ANCHOR: choose_drop_or_fill facts=['f2', 'f3']

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

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Aggregate functions (COUNT, SUM, AVG, MIN, MAX); Apply transform; CASE expressions for conditional logic in queries; Common SQL string functions for cleaning text; Concat stacking; DISTINCT for de-duplication; Exporting cleaned data (to_csv); GROUP BY grouping semantics; Grouping and aggregation (groupby); HAVING clause for filtering aggregated groups; Handling missing data (isna, dropna, fillna); Limiting results (LIMIT/OFFSET); Logical operators (AND, OR, NOT) in filtering; Map substitution; Melt reshaping; Merge join; NULL handling (IS NULL / IS NOT NULL); Pivot table reshaping; Relational database and table structure basics; Removing duplicate rows; SELECT statement fundamentals (columns, aliasing); SQL date/time extraction and arithmetic; SQL formatting/naming conventions per style guide; SQL type casting and conversion; Sorting results with ORDER BY (ASC/DESC); Table and column aliasing for readability; WHERE clause filtering and comparison operators

## LESSON, in learner order

### s01 · explainer · Cleaning a text column with the .str accessor  [reward 5]
Text Cleaning — Mixed-case and padded city names cause mismatches. The .str accessor applies string methods across an entire column at once.
(intro) Suppose the `city` column in a SwiftDrop export has `"Lagos"`, `" lagos"`, and `"LAGOS "` scattered across different rows — the same city, written three inconsistent ways. Grouping or filtering by city will miss rows until the values are standardised. ⟦A:tb1⟧
(definition) A Series' `.str` accessor lets you call ordinary string-processing methods — matching the names of Python's built-in string methods such as `lower`, `strip`, and `replace` — on every element of the Series at once: `orders["city"].str.strip().str.lower()` removes stray whitespace and lowercases every city value in one chained call, turning all three variants into the same `"lagos"`. ⟦A.f1 A:tb2⟧
[BEFORE_AFTER] city column cleaned: stray whitespace stripped and all values lowercased in one chained .str call.
  before:
[TABLE ds_orders cols=['order_id', 'city'] tags=city:inconsistent text] caption: city column before cleaning — mixed case and stray spaces
  after:
[CODE python]
orders["city"] = orders["city"].str.strip().str.lower()
print(orders["city"].unique())  # ['lagos', 'abuja', 'kano']
  annotations: ['.str.strip() removes leading/trailing spaces; .str.lower() lowercases every value', 'All three variants now collapse to the same lowercase form']

### s02 · video · Lowercasing every value in a column at once  [reward 3]
Text Cleaning — Watch a single .str.lower() call change every row in a column.
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Applying string methods across a column  [reward 5]
Quick check — Test your understanding of the .str accessor.

### s04 · hands_on · Clean a text column with .str  [reward 10]
Hands-on — Use the .str accessor to lowercase and strip whitespace from the city column in the SwiftDrop orders dataset.

### s05 · explainer · Removing duplicate rows with drop_duplicates  [reward 5]
Removing Duplicates — A repeated order_id means the same order was logged twice. drop_duplicates removes the extra row, keeping the occurrence you choose.
(intro) Suppose order `#1003` appears twice in the SwiftDrop orders DataFrame, logged the same way both times. Any count or aggregation will be inflated until the duplicate is removed. ⟦B:tb1⟧
(definition) `duplicated()` returns a boolean vector indicating which rows are duplicates, and `drop_duplicates()` removes them; both accept a `subset` argument naming the columns used to identify a duplicated row: `orders.drop_duplicates(subset=["order_id"])` removes rows that repeat the same `order_id`. ⟦B.f1 B:tb2⟧
(mechanism) By default, `drop_duplicates()` keeps the first occurrence of each duplicate set and drops the rest. Passing `keep='last'` keeps the last occurrence instead; `keep=False` drops every row that is part of a duplicate set: `orders.drop_duplicates(subset=["order_id"], keep="last")` would keep order `#1042`'s second logged row instead of its first. ⟦B.f2 B:tb3⟧
[BEFORE_AFTER] Duplicate order rows removed by drop_duplicates(subset=['order_id']); first occurrence kept.
  before:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] highlights=[["row",null,"duplicate row"]]] caption: orders before deduplication — order_id 1003 appears twice
  after:
[CODE python]
orders_clean = orders.drop_duplicates(subset=["order_id"])
print(len(orders_clean))  # one row per order_id
  annotations: ['subset=["order_id"] means two rows with the same order_id count as duplicates', 'Result has one row per unique order_id; first occurrence kept by default']

### s06 · check · Identifying duplicates with a subset  [reward 5]
Quick check — Test your understanding of how drop_duplicates uses the subset argument.

### s07 · hands_on · Remove duplicate rows and choose which to keep  [reward 10]
Hands-on — Use drop_duplicates with the keep parameter to control which occurrence of a duplicate row is retained.

### s08 · explainer · Detecting, dropping, and filling missing values  [reward 5]
Missing Data — Blank cells in a DataFrame are missing values. isna detects them; dropna removes affected rows; fillna replaces them.
(intro) Suppose a handful of SwiftDrop orders never got a `delivery_time_minutes` recorded — those cells are just blank. Any mean or sum on that column will be wrong unless the gaps are handled first. ⟦C:tb1⟧
(definition) `isna()` (and its complement `notna()`) detects which values in a Series or DataFrame are missing: `orders["delivery_time_minutes"].isna()` returns `True` for every order missing that value. ⟦C.f1 C:tb2⟧
(mechanism) `dropna()` removes rows that contain missing values; passing a `subset` of column labels restricts which columns are checked: `orders.dropna(subset=["delivery_time_minutes"])` removes only the orders missing that one column, ignoring gaps elsewhere. ⟦C.f2 C:tb3⟧
(mechanism) `fillna()` replaces missing values with a specified value: `orders["delivery_time_minutes"].fillna(orders["delivery_time_minutes"].median())` replaces each missing delivery time with the column's median instead of dropping the order entirely. ⟦C.f3 C:tb4⟧
[BEFORE_AFTER] Missing delivery_time_minutes handled: either dropped with dropna(subset=...) or filled with the column median via fillna.
  before:
[TABLE ds_orders cols=['order_id', 'city', 'delivery_time_minutes'] highlights=[["column","delivery_time_minutes","may contain missing values"]]] caption: orders before handling missing values — some delivery_time_minutes are blank
  after:
[CODE python]
# Option A: drop rows missing delivery_time_minutes
orders_dropped = orders.dropna(subset=["delivery_time_minutes"])

# Option B: fill missing values with the column median
median_time = orders["delivery_time_minutes"].median()
orders["delivery_time_minutes"] = orders["delivery_time_minutes"].fillna(median_time)
  annotations: ['dropna with subset removes only rows missing this column', "fillna replaces each blank with the column's median value"]

### s09 · video · Spotting and filling missing values  [reward 3]
Missing Data — Watch isna flag blank cells and fillna replace them.
[VIDEO ] bridge-before:  | bridge-after: 

### s10 · check · Choosing between drop and fill  [reward 5]
Quick check — Test your understanding of when to use dropna versus fillna.

### s11 · hands_on · Detect, drop, and fill missing values  [reward 10]
Hands-on — Use isna to detect gaps, dropna to remove rows missing a required field, and fillna to replace remaining gaps with the column median.

### s12 · recap · Text cleaning, duplicates, and missing data — key takeaways  [reward 5]
Recap — Three essential data-quality tools: .str for text, drop_duplicates for repeated rows, and isna/dropna/fillna for gaps.
(takeaway) Whatever string method you'd call on one piece of text, the `.str` accessor applies across an entire column at once. `drop_duplicates(subset=[...])` removes repeated rows by key column, keeping the first occurrence by default. Handling missing data means detecting it first with `isna()`, then deciding: drop the row if the missing field makes it unusable, or fill with a reasonable substitute such as the column's median. ⟦A.f1 C.f1 C.f2 C.f3 B.f1 B.f2 A:tb3 C:tb5 B:tb3⟧
[UP NEXT] Up next: Mapping and Applying Transformations: Next you'll use map substitution to replace values in a column using a lookup dict — a fast way to recode categories without writing loops.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · The .str accessor applies string methods to every row — Instead of looping row by row, the .str accessor vectorises any Python string method across the whole column.
(definition) A Series' `.str` accessor lets you call ordinary string-processing methods — matching the names of Python's built-in string methods such as `lower`, `strip`, and `replace` — on every element of the Series at once. `orders["city"].str.strip().str.lower()` removes stray whitespace and lowercases every city value in one chained call, turning `"Lagos"`, `" lagos"`, and `"LAGOS "` all into `"lagos"`. ⟦A.f1 A:tb2⟧
[BEFORE_AFTER] Row-by-row loop replaced by a single chained .str.strip().str.lower() call.
  before:
[CODE python]
# Without .str — a loop is needed
for i, val in orders["city"].items():
    orders.at[i, "city"] = val.strip().lower()
  annotations: ['Row-by-row loop — slow and verbose']
  after:
[CODE python]
# With .str — one vectorised call
orders["city"] = orders["city"].str.strip().str.lower()
  annotations: ['.str applies strip and lower to every element at once']
### r02 · Using subset to identify duplicate rows — drop_duplicates checks all columns by default. The subset argument limits the check to the columns that define a duplicate.
(definition) `duplicated()` returns a boolean vector indicating which rows are duplicates, and `drop_duplicates()` removes them; both accept a `subset` argument naming the columns used to identify a duplicated row. `orders.drop_duplicates(subset=["order_id"])` removes rows that repeat the same `order_id`, even if other columns differ slightly between the two rows. ⟦B.f1 B:tb2⟧
[BEFORE_AFTER] drop_duplicates called with subset=['order_id'] to catch rows with the same order ID regardless of other column differences.
  before:
[CODE python]
# Without subset — checks ALL columns; rows must be identical
orders.drop_duplicates()
  annotations: ['Only removes rows where every column matches — misses partial duplicates']
  after:
[CODE python]
# With subset — checks only order_id
orders.drop_duplicates(subset=["order_id"])
  annotations: ['Removes any row whose order_id already appeared — correct for this case']
### r03 · Drop or fill — choosing the right approach — dropna removes rows with missing values; fillna replaces them. The right choice depends on whether a reasonable substitute exists.
(mechanism) `dropna()` removes rows that contain missing values; passing a `subset` of column labels restricts which columns are checked. `fillna()` replaces missing values with a specified value. Drop the row if a missing field makes it unusable for the analysis; fill it if a reasonable substitute — such as the column's median — exists instead. ⟦C.f2 C.f3 C:tb3 C:tb4⟧
[BEFORE_AFTER] Missing delivery_time_minutes handled with either dropna (removes rows) or fillna with median (preserves rows).
  before:
[CODE python]
# Missing delivery_time_minutes — two options
print(orders["delivery_time_minutes"].isna().sum())  # count of missing
  annotations: ['isna().sum() counts how many values are missing']
  after:
[CODE python]
# Drop rows where delivery_time_minutes is missing
orders_dropped = orders.dropna(subset=["delivery_time_minutes"])

# OR fill missing values with the column median
orders["delivery_time_minutes"] = orders["delivery_time_minutes"].fillna(
    orders["delivery_time_minutes"].median()
)
  annotations: ['dropna removes rows missing this column', 'fillna replaces each blank with the median — no rows lost']

=========

# EVALUATOR PACKET — Descriptive Statistics with pandas (tile_pandas_descriptive_stats)
Tile summary: Compute mean, median, and standard deviation for a DataFrame column, and use describe() to get a full summary in one call.
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = stats.pandas_descriptive_stats — Computing descriptive statistics with pandas (describe, mean, median, std)

## DETERMINISTIC GATE (already passed — do not re-derive): n/a  errors=0 warnings=0

## SOURCE FACTS — A (stats.pandas_descriptive_stats)   objective: Compute descriptive statistics for a DataFrame column using pandas methods such as describe, mean, median, and std.
A.f1: pandas provides built-in statistical methods for a Series or DataFrame column, including mean() (mean of values), median() (arithmetic median), and std() (sample standard deviation).   [sources: pandas_docs_basics#descriptive-statistics]
A.f2: describe() computes a set of summary statistics, such as count, mean, std, min, quartiles, and max, for a Series or for each numeric column of a DataFrame in one call.   [sources: pandas_docs_basics#summarizing-data-describe]
note: Keep the reproduced figures (~30.9, 22, ~21.9) consistent with the hand-computed values from stats.descriptive_measures_of_center and stats.measures_of_spread.
PRACTICE ANCHOR (live_code): Call describe() on a DataFrame and interpret the reported mean and std for one column.  SUCCESS: The learner finds the mean and std rows for the chosen column, matches them with mean() and std() calls, and states the std in the column's units as a typical distance from the mean.
ASSESSMENT ANCHOR: compute_mean_median_std_with_pandas facts=['f1']
ASSESSMENT ANCHOR: read_describe_summary_table facts=['f2']
ASSESSMENT ANCHOR: interpret_mean_and_std_in_context facts=['f1', 'f2']

## DATA ASSETS USED

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply transform; Boolean/conditional filtering; Concat stacking; DISTINCT for de-duplication; Exporting cleaned data (to_csv); Grouping and aggregation (groupby); Handling missing data (isna, dropna, fillna); Logical operators (AND, OR, NOT) in filtering; Map substitution; Melt reshaping; Merge join; NULL handling (IS NULL / IS NOT NULL); Pivot table reshaping; Relational database and table structure basics; Removing duplicate rows; Renaming columns and index labels; SELECT statement fundamentals (columns, aliasing); Selecting rows/columns with loc/iloc; Sorting results with ORDER BY (ASC/DESC); Sorting values; String cleaning with the .str accessor; Table and column aliasing for readability; Type conversion and dtype management (astype); WHERE clause filtering and comparison operators; Working with datetime data (to_datetime, date components)

## LESSON, in learner order

### s01 · explainer · Computing statistics directly from a column  [reward 5]
Descriptive Statistics — pandas can compute the mean, median, and standard deviation you've calculated by hand — straight from a DataFrame column.
(intro) The mean, median, and standard deviation computed by hand earlier for the seven-value delivery-time batch are exactly what pandas can compute directly from a DataFrame column. ⟦A:tb1⟧
(definition) pandas provides built-in statistical methods for a Series or DataFrame column, including `mean()` (mean of values), `median()` (arithmetic median), and `std()` (sample standard deviation): if `delivery_time_minutes` holds that seven-order batch, `orders["delivery_time_minutes"].mean()`, `.median()`, and `.std()` reproduce the same approximately 30.9, 22, and 21.9-minute figures straight from the column. ⟦A.f1 A:tb2⟧
(definition) `describe()` computes a set of summary statistics — count, mean, std, min, quartiles, and max — for a Series or for each numeric column of a DataFrame in one call: `orders["delivery_time_minutes"].describe()` returns all of those figures at once for the delivery-time column. ⟦A.f2 A:tb3⟧
[CODE python]
orders["delivery_time_minutes"].describe()
  annotations: ['describe() returns count, mean, std, min, quartiles, and max in one call']
  output: count     7.000000
mean     30.857143
std      21.934969
min      18.000000
25%      21.000000
50%      22.000000
75%      27.000000
max      80.000000
Name: delivery_time_minutes, dtype: float64

### s02 · video · describe, mean, median, and std in action  [reward 3]
Descriptive Statistics — Watch describe() and the individual stat methods run on a real DataFrame column.
[VIDEO ] bridge-before:  | bridge-after: 

### s03 · check · Reading a describe() summary table  [reward 5]
Quick check — Test your ability to read the output of describe() and identify the right statistic.

### s04 · hands_on · Compute and interpret descriptive statistics  [reward 10]
Hands-on — Use mean(), median(), std(), and describe() on the delivery_time_minutes column and interpret what the numbers tell you about SwiftDrop's delivery performance.

### s05 · recap · Descriptive statistics with pandas — key takeaways  [reward 5]
Recap — mean, median, std, and describe give you a complete picture of a numeric column in seconds.
(takeaway) pandas provides `mean()`, `median()`, and `std()` as direct methods on a Series or column. `describe()` bundles count, mean, std, min, quartiles, and max into one call. For the SwiftDrop delivery-time column, the mean (~30.9 min) sits well above the median (22 min) because a single 80-minute outlier pulls the average up — a pattern describe() makes immediately visible. ⟦A.f1 A.f2 A:tb4⟧
[UP NEXT] Up next: Selecting and Filtering Data: Next you'll use loc and iloc to select specific rows and columns, and boolean conditions to filter a DataFrame down to just the rows you need.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Reading the describe() output — describe() returns a fixed set of rows. Knowing what each row means lets you read any summary table quickly.
(definition) `describe()` computes a set of summary statistics — count, mean, std, min, quartiles (25%, 50%, 75%), and max — for a Series or for each numeric column of a DataFrame in one call. The `50%` row is the median. For the SwiftDrop delivery-time column, `describe()` shows count 7, mean ~30.9, std ~21.9, min 18, 50% (median) 22, and max 80. ⟦A.f2 A:tb3⟧
[BEFORE_AFTER] Three individual stat calls replaced by a single describe() call showing all summary statistics.
  before:
[CODE python]
# Individual calls — one statistic at a time
print(orders["delivery_time_minutes"].mean())    # ~30.9
print(orders["delivery_time_minutes"].median())  # 22
print(orders["delivery_time_minutes"].std())     # ~21.9
  annotations: ['Three separate calls — each returns one number']
  after:
[CODE python]
# describe() — all summary statistics in one call
print(orders["delivery_time_minutes"].describe())
# count     7.0
# mean     ~30.9
# std      ~21.9
# min      18.0
# 25%      21.0
# 50%      22.0   <- median
# 75%      27.0
# max      80.0
  annotations: ['describe() returns count, mean, std, min, quartiles, and max', '50% row is the median — same as .median()']