# Stage 01 – Scenario & Asset Registry Evaluation

**Batch:** `final_batch_009_da_pandas`  
**Artifact:** `scenario_asset_registry.json`  
**Evaluator:** independent (no access to generator reasoning)

---

## 1. Scenario Review

**scen_swiftdrop** — SwiftDrop Delivery Analytics (Lagos / Abuja / Kano, NGN, logistics domain). Locale, currency, domain, and glossary_example_vocab are all consistent with the glossary bundle's teaching blocks and examples. The vocabulary list covers all column names, city names, courier names, city codes, file names, DataFrame variable names, speed labels, and summary statistics referenced in the glossary.

## 2. Dataset Assets

### ds_orders (14 rows, 10 columns)
- First 7 rows reproduce delivery_time_minutes = [18, 20, 22, 22, 26, 28, 80] as claimed. Verified: mean ≈ 30.86, median = 22, std ≈ 21.93 (ddof=1) — matches glossary claims of "~30.9", "22", "~21.9".
- All column semantic_roles are correct: order_id/driver_id/customer_id as identifiers with numeric_looking_label=true; city/city_code/courier as categorical; pickup_date as datetime; delivery_time_minutes/distance_km/order_value as numerical with correct units.
- order_ids are unique (1001–1014); customer_ids (301–314) all present in ds_customers; driver_ids (201–203) all present in ds_drivers.

### ds_drivers (4 rows)
- driver_id 204 (Dami Fashola) exists only here, not in ds_orders — correctly supports unmatched-key merge/join demonstrations.

### ds_customers (15 rows)
- customer_id 315 (Zainab Aliyu) exists only here, not in ds_orders — correctly supports unmatched-key merge/join demonstrations.

### ds_monthly_wide (3 rows × 4 columns)
- Wide format with city + jan/feb/mar_deliveries. Values match the glossary melt example.

### ds_monthly_long (10 rows)
- First 9 rows are the expected melt output of ds_monthly_wide. 10th row is a duplicate Lagos/jan_deliveries/18 — correctly supports pivot_table aggfunc='mean' vs 'sum' demonstration.

### ds_product_sales (12 rows)
- Duplicate product-month pairs (Envelope/Jan, Parcel/Feb, Document/Mar) correctly support pivot_table aggfunc demonstration.

### ds_jan_orders, ds_feb_orders, ds_mar_orders (5 rows each)
- Identical column schemas; distinct order_id ranges (2001–2015). Correctly support pd.concat() stacking demonstration.

### orders_messy variant (on ds_orders)
- 5 planted issues verified:
  - iss_city_case_1004: " lagos" (leading space, lowercase) ✓
  - iss_city_case_1007: "LAGOS " (uppercase, trailing space) ✓
  - iss_dist_string: distance_km = "unknown" for order 1005 ✓
  - iss_missing_dt: delivery_time_minutes null for order 1008 ✓
  - iss_duplicate_1003: order 1003 duplicated ✓
- All are genuine instances of their declared kinds.

## 3. Code Workspace Assets

### cw_series_dataframe
- Uses delivery_times = [18, 20, 22, 22, 26, 28, 80] and dict example with [1001, 1002, 1003] / [Lagos, Abuja, Kano] / [18, 20, 26] — matches glossary `pandas.dataframe_series_model` tb2/tb4.

### cw_reading_data
- CSV matches ds_orders (14 rows). Starter uses pd.read_csv('orders.csv') — matches glossary `pandas.reading_data`.

### cw_creating_dataframes
- Dict-of-lists and list-of-dicts examples match glossary `pandas.creating_dataframes` tb2/tb3.

### cw_inspecting_dataframes
- CSV matches ds_orders (14 rows). Starter exercises head/shape/dtypes/info/describe — matches glossary.

### cw_descriptive_stats
- CSV has exactly the 7-row subset producing [18, 20, 22, 22, 26, 28, 80]. Comments cite mean ≈ 30.9, median = 22, std ≈ 21.9 — all verified correct.

### cw_loc_iloc_selection
- CSV has 10 rows (orders 1001–1010). Starter exercises match glossary examples (loc[2:4, 'city'], iloc[0:3, 0:2]).

### cw_boolean_filtering
- CSV has 14 rows. Threshold > 25 and Lagos filter match glossary `pandas.boolean_filtering` tb2/tb4.

### cw_sort_rename
- CSV has 8 rows. Sort by city + delivery_time_minutes and rename examples match glossary.

### cw_dtype_datetime
- orders_messy_dtype.csv has "unknown" in distance_km for order 1005 and string pickup_date — matches glossary `pandas.dtype_conversion` and `pandas.datetime_handling`.

### cw_text_dupes_missing
- orders_messy.csv has mixed-case cities, duplicate order 1003, missing delivery_time for order 1008 — matches glossary concepts for str_accessor_cleaning, drop_duplicates, missing_data_handling.

### cw_map_apply
- city_lookup dict {LOS→Lagos, ABJ→Abuja, KAN→Kano} and label_speed function (>25 → slow) match glossary exactly.

### cw_groupby_melt
- orders.csv + city_deliveries.csv. groupby('city')['delivery_time_minutes'].mean() and melt(id_vars=['city']) match glossary.

### cw_concat_merge
- jan/feb/mar_orders.csv + orders.csv + customers.csv. concat and merge examples match glossary. Customer 315 in customers.csv but not orders.csv supports unmatched-key demo.

### cw_pivot_export
- long_deliveries.csv matches ds_monthly_long (with duplicate Lagos-jan row). product_sales.csv matches ds_product_sales. pivot_table and to_csv examples match glossary.

## 4. Cross-checks Against Glossary

Checked approximately half of the 22 concepts' examples against the registry data:
- pandas.dataframe_series_model: ✓
- pandas.reading_data: ✓
- pandas.creating_dataframes: ✓
- pandas.inspecting_dataframes: ✓
- stats.pandas_descriptive_stats: ✓ (mean/median/std verified numerically)
- pandas.loc_iloc_selection: ✓
- pandas.boolean_filtering: ✓
- pandas.sort_values + pandas.rename_columns_index: ✓
- pandas.dtype_conversion + pandas.datetime_handling: ✓
- pandas.map_substitution + pandas.apply_transform: ✓
- pandas.groupby_aggregation + pandas.melt_reshaping: ✓
- pandas.concat_stacking + pandas.merge_join: ✓
- pandas.pivot_table_reshaping + pandas.export_to_csv: ✓

## 5. Defects

### ADVISORY

1. **cw_dtype_datetime/starter.py**: The hint `pd.to_numeric(errors='coerce')` introduces a function not taught in the glossary's dtype_conversion concept (which only covers `astype()`). While practical, it goes beyond the taught content. → Consider replacing with a hint that stays within astype() or noting this is an extension.

2. **cw_creating_dataframes/starter.py & cw_series_dataframe/starter.py**: The 3-row example uses delivery_time_minutes=26 for order_id 1003, while ds_orders has delivery_time_minutes=22 for order 1003. The workspace follows the glossary example (which also uses 26), so this is internally consistent with the glossary but inconsistent with the dataset. → Consider using order_id 1005 (which actually has delivery_time_minutes=26 in ds_orders) or adjusting the example values.

---

## VERDICT: PASS

ADVISORY cw_dtype_datetime/starter.py: hint introduces pd.to_numeric(errors='coerce') which is not taught in the glossary's dtype_conversion concept → either remove the pd.to_numeric hint or add a note that this is an extension beyond the taught astype() method
ADVISORY cw_creating_dataframes/starter.py: order_id 1003 shown with delivery_time_minutes=26 but ds_orders has 22 for that order; workspace follows glossary example but contradicts dataset → align the example order_ids/values with ds_orders, e.g. use order_id 1005 (which has 26 in ds_orders) or use 22 for order 1003
