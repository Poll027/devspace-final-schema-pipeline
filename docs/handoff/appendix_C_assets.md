# Appendix C: Datasets, code workspaces and scenarios

65 distinct asset ids across the batches' `scenario_asset_registry.json` files.

## IMPORTANT: asset ids are not globally unique
Each batch has its own registry. **Seven asset ids occur in several batches with different content** (different rows/columns). A lesson refers to an asset by `asset_id` only; the registry it was authored against is identified by `source.scenario_registry_hash` in the lesson. The backend must therefore key assets by `(scenario_registry_hash, asset_id)` (or by a content hash of the asset), never by `asset_id` alone, or lessons will silently read the wrong data.

- `ds_city_delivery_summary`: final_batch_003_da_chunk: 6 rows, columns ['city', 'month', 'avg_delivery_minutes', 'order_count']; final_batch_004_da_chunk2: 3 rows, columns ['city', 'avg_delivery_min', 'target_min', 'pct_on_time', 'variability_rank', 'n_couriers', 'finding_priority']
- `ds_customers`: final_batch_003_da_chunk: 5 rows, columns ['customer_id', 'name', 'city']; final_batch_006_da_sql_rest: 6 rows, columns ['customer_id', 'name', 'city']; final_batch_009_da_pandas: 15 rows, columns ['customer_id', 'customer_name', 'segment', 'signup_date']
- `ds_orders`: final_batch_003_da_chunk: 7 rows, columns ['order_id', 'customer_id', 'delivery_minutes']; final_batch_006_da_sql_rest: 13 rows, columns ['order_id', 'customer_id', 'delivery_time_minutes', 'order_date', 'region', 'amount', 'city']; final_batch_008_da_python_core: 15 rows, columns ['order_id', 'city', 'delivery_minutes', 'is_late', 'driver_id']; final_batch_009_da_pandas: 14 rows, columns ['order_id', 'city', 'city_code', 'courier', 'driver_id', 'customer_id', 'pickup_date', 'delivery_time_minutes', 'distance_km', 'order_value']
- `ds_order_items`: final_batch_003_da_chunk: 8 rows, columns ['order_id', 'product_id']; final_batch_006_da_sql_rest: 10 rows, columns ['order_id', 'product_id', 'quantity', 'unit_price']
- `ds_capstone_orders`: final_batch_004_da_chunk2: 12 rows, columns ['order_id', 'zone', 'driver_id', 'delivery_time_min', 'order_date', 'on_time']; final_batch_010_da_stats_capstone: 34 rows, columns ['order_id', 'driver_id', 'zone', 'order_date', 'delivery_time']
- `ds_capstone_drivers`: final_batch_004_da_chunk2: 6 rows, columns ['driver_id', 'name', 'zone', 'shift']; final_batch_010_da_stats_capstone: 8 rows, columns ['driver_id', 'driver_name']
- `ds.orders`: final_batch_005_da_sql_canary: 10 rows, columns ['order_id', 'customer_id', 'delivery_time_minutes']; final_batch_012_da_viz: 24 rows, columns ['order_id', 'city', 'delivery_time_minutes', 'distance_km', 'order_value', 'num_items']

## Scenarios

- `northstar_store`:  - 
- `scenario_courier_orders`:  - 
- `scen_quickship`:  - 
- `scen_quickship_db`:  - 
- `scen_quickship_ab`:  - 
- `scen_quickship_ops`:  - 
- `scen.sql_delivery_shop`:  - 
- `scen_da_sql_ecommerce`:  - 
- `scenario_delivery_ops`:  - 
- `scenario_stakeholder_comms`:  - 
- `scen_delivery_python`:  - 
- `scen_swiftdrop`:  - 
- `scen_delivery_stats`:  - 
- `scen_ab_test`:  - 
- `scenario_delivery_orders`:  - 
- `scen.da_viz_delivery`:  - 
- `scen.da_viz_theming`:  - 
- `scenario_nga_delivery_ops`:  - 

## Assets

### `asset_city_deliveries` (dataset) - batch `final_batch_013_da_stakeholder_chart` - content `9c4d190756`
Average delivery time and total order count per city (Lagos, Abuja, Kano) for the current reporting period. Used for bar chart (comparison) and pie chart (part-to-whole share of total orders) examples.

Rows: 3, variants: `city_deliveries_messy`
| column | type | role | notes |
|---|---|---|---|
| city | string | categorical | City name (Lagos, Abuja, or Kano) |
| avg_delivery_minutes | number | numerical | Average delivery time in minutes for orders in this city |
| order_count | integer | numerical | Total number of orders fulfilled in this city during the reporting period |

### `asset_city_totals` (dataset) - batch `final_batch_011_da_spreadsheet` - content `3532b4960d`
Aggregated total order amount by city (6 cities, all amounts positive). Used for bar-chart and pie-chart exercises. 6 categories and no negative values satisfy the pie-chart eligibility conditions from the glossary.

Rows: 6
| column | type | role | notes |
|---|---|---|---|
| city | string | categorical | Delivery destination city |
| total_amount | number | numerical | Total order amount for the city |

### `asset_delivery_distance` (dataset) - batch `final_batch_013_da_stakeholder_chart` - content `69caf48956`
Individual order records with distance from depot and actual delivery time, across Lagos, Abuja, and Kano. Used for scatterplot (distance/delivery-time relationship) — an exploratory chart that can be designed to communicate findings to an audience. order_id is a numeric-looking label.

Rows: 15, variants: `delivery_distance_messy`
| column | type | role | notes |
|---|---|---|---|
| order_id | integer | identifier | Unique order identifier (numeric label, not a quantity to aggregate) |
| city | string | categorical | City where the order was fulfilled (Lagos, Abuja, or Kano) |
| distance_km | number | numerical | Distance from depot to delivery address in kilometres |
| delivery_minutes | number | numerical | Actual delivery time in minutes for this order |

### `asset_drivers_index_match` (dataset) - batch `final_batch_011_da_spreadsheet` - content `aff9d24b31`
Driver reference table with driver_name in column A and driver_id in column B — the reversed layout that VLOOKUP cannot handle. Supports =INDEX(Drivers!A:A,MATCH(F2,Drivers!B:B,0)) exercises.

Rows: 5
| column | type | role | notes |
|---|---|---|---|
| driver_name | string | text | Full name of the driver |
| driver_id | string | identifier | Driver identifier string (e.g. D01); used as a label, not a number |

### `asset_drivers_vlookup` (dataset) - batch `final_batch_011_da_spreadsheet` - content `d6ad90b2c0`
Driver reference table with driver_id in the leftmost column and driver_name in the second column. Supports =VLOOKUP(F2,Drivers!A:B,2,FALSE) and =XLOOKUP(F2,Drivers!A:A,Drivers!B:B) exercises.

Rows: 5
| column | type | role | notes |
|---|---|---|---|
| driver_id | string | identifier | Driver identifier string (e.g. D01); used as a label, not a number |
| driver_name | string | text | Full name of the driver |

### `asset_lagos_weekly_deliveries` (dataset) - batch `final_batch_013_da_stakeholder_chart` - content `d0f75256c5`
Average delivery time and order count for Lagos, broken down by week over an 8-week reporting period. Shows a rising trend — the 'Lagos point' communicated via a line graph. week_number is a numeric-looking label (sequential identifier, not a quantity to aggregate).

Rows: 8, variants: `lagos_weekly_messy`
| column | type | role | notes |
|---|---|---|---|
| week_number | integer | identifier | Sequential week number (1 = earliest week in the reporting period) |
| week_label | string | categorical | Human-readable week label (e.g. 'Wk 1', 'Wk 2') |
| avg_delivery_minutes | number | numerical | Average delivery time in minutes for Lagos orders in this week |
| order_count | integer | numerical | Number of Lagos orders fulfilled in this week |

### `asset_monthly_summary` (dataset) - batch `final_batch_011_da_spreadsheet` - content `5108979f22`
Aggregated total order amount by month. Used for line-chart exercises where evenly-spaced time-ordered data is required.

Rows: 6
| column | type | role | notes |
|---|---|---|---|
| month_label | string | categorical | Month label (e.g. Jan-2024) |
| total_amount | number | numerical | Total order amount for the month |

### `asset_orders_clean` (dataset) - batch `final_batch_011_da_spreadsheet` - content `fee7ccd6de`
One row per delivery order. Used for formula syntax, aggregation, logical functions, conditional aggregation, lookups, sorting, filtering, tables, named ranges, pivot tables, and chart exercises. delivery_minutes is NULL for Pending/Cancelled rows (non-delivered orders have no recorded time). Note: teaching-block ranges such as D2:D51 span 50 rows; this dataset has 20 rows — learners should adjust range references to D2:D21 in practice.

Rows: 20, variants: `asset_orders_messy`
| column | type | role | notes |
|---|---|---|---|
| order_id | string | identifier | Unique order identifier in the format LG-NNNN |
| city | string | categorical | Delivery destination city |
| delivery_minutes | integer | numerical | Actual delivery time in minutes; null if not yet delivered |
| amount | number | numerical | Order value in Nigerian Naira |
| status | string | categorical | Order status: Pending, Delivered, or Cancelled |
| driver_id | string | identifier | Driver identifier string (e.g. D01); used as a label, not a number |
| order_date | date | datetime | Date the order was placed (YYYY-MM-DD) |

### `asset_orders_location_combined` (dataset) - batch `final_batch_011_da_spreadsheet` - content `7ccef0971d`
Orders table where city and country are stored as a single 'city,country' string (e.g. 'Lagos,Nigeria'). Used for the Text to Columns exercise.

Rows: 8
| column | type | role | notes |
|---|---|---|---|
| order_id | string | identifier | Unique order identifier |
| location | string | text | City and country combined as 'city,country' |
| delivery_minutes | integer | numerical | Delivery time in minutes |
| amount | number | numerical | Order value in NGN |
| status | string | categorical | Order status |
| driver_id | string | identifier | Driver identifier string |
| order_date | date | datetime | Date the order was placed |

### `cw.viz_starter` (code_workspace) - batch `final_batch_012_da_viz` - content `57621ed05e`


`{"asset_kind": "code_workspace", "scenario_id": "scen.da_viz_delivery", "title": "Matplotlib / seaborn starter workspace", "runtime": "pyodide", "files": [{"path": "orders.csv", "content": "order_id,city,delivery_time_minutes,distance_km,order_value,num_items\n1001,Lagos,18,2.1,1850.0,2\n1002,Lagos,22,3.4,2200.0,3\n1003,Lagos,19,2.8,1600.0,1\n1004,Lagos,26,4.5,3100.0,4\n1005,Lagos,30,5.2,2750.0,3\n1006,Lagos,24,3.9,2400.0,2\n1007,Lagos,28,4.8,3300.0,5\n1008,Lagos,50,9.1,4800.0,6\n1009,Abuja,25,3.2,2100.0,2\n1010,Abuja,28,4.1,2600.0,3\n1011,Abuja,23,3.0,1900.0,1\n1012,Abuja,31,5.5,3400.0,4\n101`

### `cw_boolean_filtering` (code_workspace) - batch `final_batch_009_da_pandas` - content `f9220b7d66`


`{"asset_kind": "code_workspace", "scenario_id": "scen_swiftdrop", "title": "Boolean Filtering Workspace", "runtime": "pyodide", "files": [{"path": "starter.py", "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# Threshold: delivery_time_minutes > 25 means 'slow'\n\n# TODO: filter to keep only orders where delivery_time_minutes > 25\n# TODO: filter to keep Lagos orders where delivery_time_minutes > 25\n#       (remember to wrap each condition in parentheses)\n"}, {"path": "orders.csv", "content": "order_id,city,city_code,courier,driver_id,customer_id,pickup_date,delivery`

### `cw_concat_merge` (code_workspace) - batch `final_batch_009_da_pandas` - content `9b046fd37d`


`{"asset_kind": "code_workspace", "scenario_id": "scen_swiftdrop", "title": "concat and merge Workspace", "runtime": "pyodide", "files": [{"path": "starter.py", "content": "import pandas as pd\n\njan_orders = pd.read_csv('jan_orders.csv')\nfeb_orders = pd.read_csv('feb_orders.csv')\nmar_orders = pd.read_csv('mar_orders.csv')\norders    = pd.read_csv('orders.csv')\ncustomers = pd.read_csv('customers.csv')\n\n# concat: stack monthly tables row-wise\n# TODO: pd.concat([jan_orders, feb_orders, mar_orders])\n\n# merge: join orders with customers on customer_id\n# TODO: orders.merge(customers, on='cu`

### `cw_creating_dataframes` (code_workspace) - batch `final_batch_009_da_pandas` - content `c5603ab9d5`


`{"asset_kind": "code_workspace", "scenario_id": "scen_swiftdrop", "title": "Creating DataFrames Workspace", "runtime": "pyodide", "files": [{"path": "starter.py", "content": "import pandas as pd\n\n# Build the same orders table two ways:\n\n# Way 1 \u2014 dict of equal-length lists\n# data_dict = {\n#     'order_id': [1001, 1002, 1005],\n#     'city': ['Lagos', 'Abuja', 'Abuja'],\n#     'delivery_time_minutes': [18, 20, 26]\n# }\n\n# Way 2 \u2014 list of dicts (one dict per row)\n# data_list = [\n#     {'order_id': 1001, 'city': 'Lagos', 'delivery_time_minutes': 18},\n#     {'order_id': 1002, `

### `cw_descriptive_stats` (code_workspace) - batch `final_batch_009_da_pandas` - content `a57c85c50b`


`{"asset_kind": "code_workspace", "scenario_id": "scen_swiftdrop", "title": "Descriptive Statistics Workspace", "runtime": "pyodide", "files": [{"path": "starter.py", "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# delivery_time_minutes holds [18, 20, 22, 22, 26, 28, 80]\n# mean \u2248 30.9, median = 22, std \u2248 21.9\n\n# TODO: compute mean, median, std of delivery_time_minutes\n# TODO: call describe() on the column\n"}, {"path": "orders.csv", "content": "order_id,city,city_code,courier,driver_id,customer_id,pickup_date,delivery_time_minutes,distance_km,order_value`

### `cw_dtype_datetime` (code_workspace) - batch `final_batch_009_da_pandas` - content `92d89c13c3`


`{"asset_kind": "code_workspace", "scenario_id": "scen_swiftdrop", "title": "dtype Conversion and Datetime Workspace", "runtime": "pyodide", "files": [{"path": "starter.py", "content": "import pandas as pd\n\norders = pd.read_csv('orders_messy_dtype.csv')\n\n# distance_km is loaded as a string \u2014 convert it to float\n# pickup_date is a string \u2014 convert it to datetime\n\n# TODO: print orders.dtypes to see the problem\n# TODO: convert distance_km to float\n# TODO: convert pickup_date to datetime with pd.to_datetime()\n# TODO: extract the month number into a new column 'pickup_month'\n"},`

### `cw_groupby_melt` (code_workspace) - batch `final_batch_009_da_pandas` - content `46fed51e8c`


`{"asset_kind": "code_workspace", "scenario_id": "scen_swiftdrop", "title": "groupby and melt Workspace", "runtime": "pyodide", "files": [{"path": "starter.py", "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\ncity_deliveries = pd.read_csv('city_deliveries.csv')\n\n# groupby: average delivery time per city\n# TODO: orders.groupby('city')['delivery_time_minutes'].mean()\n# TODO: also compute sum and mean together with .agg(['mean', 'sum'])\n\n# melt: wide \u2192 long\n# TODO: city_deliveries.melt(id_vars=['city'],\n#                            var_name='month',\n#          `

### `cw_inspecting_dataframes` (code_workspace) - batch `final_batch_009_da_pandas` - content `ab77cff64e`


`{"asset_kind": "code_workspace", "scenario_id": "scen_swiftdrop", "title": "Inspecting DataFrames Workspace", "runtime": "pyodide", "files": [{"path": "starter.py", "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# TODO: show the first 5 rows\n# TODO: print the shape\n# TODO: print the dtypes\n# TODO: call info()\n# TODO: call describe()\n"}, {"path": "orders.csv", "content": "order_id,city,city_code,courier,driver_id,customer_id,pickup_date,delivery_time_minutes,distance_km,order_value\n1001,Lagos,LOS,Ada,201,301,2024-03-14,18,4.2,2500\n1002,Abuja,ABJ,Bayo,202,302,202`

### `cw_loc_iloc_selection` (code_workspace) - batch `final_batch_009_da_pandas` - content `b552491501`


`{"asset_kind": "code_workspace", "scenario_id": "scen_swiftdrop", "title": "loc and iloc Selection Workspace", "runtime": "pyodide", "files": [{"path": "starter.py", "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# orders has default integer row labels 0, 1, 2, ...\n# Columns: order_id, city, city_code, courier, driver_id,\n#          customer_id, pickup_date, delivery_time_minutes,\n#          distance_km, order_value\n\n# TODO: use .loc to select the 'city' column for rows labeled 2 through 4\n# TODO: use .iloc to select the first 3 rows and first 2 columns\n# TODO:`

### `cw_map_apply` (code_workspace) - batch `final_batch_009_da_pandas` - content `382eb4f3b6`


`{"asset_kind": "code_workspace", "scenario_id": "scen_swiftdrop", "title": "map and apply Workspace", "runtime": "pyodide", "files": [{"path": "starter.py", "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# Lookup dict for city codes\ncity_lookup = {'LOS': 'Lagos', 'ABJ': 'Abuja', 'KAN': 'Kano'}\n\n# TODO: use .map(city_lookup) to replace city_code with full city names\n\n# Labelling rule: delivery_time_minutes > 25 \u2192 'slow', else \u2192 'fast'\n# def label_speed(row):\n#     if row['delivery_time_minutes'] > 25:\n#         return 'slow'\n#     else:\n#         re`

### `cw_orders_csv` (code_workspace) - batch `final_batch_008_da_python_core` - content `5d26171282`


`{"asset_kind": "code_workspace", "scenario_id": "scen_delivery_python", "title": "orders.csv \u2014 delivery order records for file I/O exercises", "runtime": "pyodide", "files": [{"path": "orders.csv", "content": "order_id,city,delivery_minutes\n1042,Lagos,32\n1043,Abuja,45\n1044,Kano,21\n1045,Lagos,60\n1046,Ibadan,18\n1047,Abuja,12\n1048,Kano,55\n1049,Lagos,38\n1050,Ibadan,72\n1051,Lagos,14\n1052,Abuja,29\n1053,Kano,47\n1054,Lagos,33\n1055,Ibadan,9\n1056,Abuja,61\n"}]}`

### `cw_pivot_export` (code_workspace) - batch `final_batch_009_da_pandas` - content `59828aefd8`


`{"asset_kind": "code_workspace", "scenario_id": "scen_swiftdrop", "title": "pivot_table and Export Workspace", "runtime": "pyodide", "files": [{"path": "starter.py", "content": "import pandas as pd\n\nlong_deliveries = pd.read_csv('long_deliveries.csv')\nproduct_sales   = pd.read_csv('product_sales.csv')\n\n# pivot_table: long \u2192 wide (city \u00d7 month)\n# TODO: long_deliveries.pivot_table(index='city',\n#                                   columns='month',\n#                                   values='deliveries')\n\n# pivot_table with aggfunc='sum' (product_sales has duplicate product-mon`

### `cw_reading_data` (code_workspace) - batch `final_batch_009_da_pandas` - content `403b192a27`


`{"asset_kind": "code_workspace", "scenario_id": "scen_swiftdrop", "title": "Reading Data Workspace", "runtime": "pyodide", "files": [{"path": "starter.py", "content": "import pandas as pd\n\n# The orders CSV is available at: 'orders.csv'\n# orders = pd.read_csv('orders.csv')\n\n# TODO: read orders.csv into a DataFrame called orders\n# TODO: print the DataFrame\n"}, {"path": "orders.csv", "content": "order_id,city,city_code,courier,driver_id,customer_id,pickup_date,delivery_time_minutes,distance_km,order_value\n1001,Lagos,LOS,Ada,201,301,2024-03-14,18,4.2,2500\n1002,Abuja,ABJ,Bayo,202,302,2024-`

### `cw_series_dataframe` (code_workspace) - batch `final_batch_009_da_pandas` - content `411025b2da`


`{"asset_kind": "code_workspace", "scenario_id": "scen_swiftdrop", "title": "Series and DataFrame Construction Workspace", "runtime": "pyodide", "files": [{"path": "starter.py", "content": "import pandas as pd\n\n# A list of delivery times (minutes)\n# delivery_times = [18, 20, 22, 22, 26, 28, 80]\n\n# A dict of equal-length lists for an orders table\n# data = {\n#     'order_id': [1001, 1002, 1003],\n#     'city': ['Lagos', 'Abuja', 'Kano'],\n#     'delivery_time_minutes': [18, 20, 26]\n# }\n\n# TODO: build a Series from delivery_times\n# TODO: build a DataFrame from data\n# TODO: pull out the`

### `cw_sort_rename` (code_workspace) - batch `final_batch_009_da_pandas` - content `6a54423b6a`


`{"asset_kind": "code_workspace", "scenario_id": "scen_swiftdrop", "title": "Sort and Rename Workspace", "runtime": "pyodide", "files": [{"path": "starter.py", "content": "import pandas as pd\n\norders = pd.read_csv('orders.csv')\n\n# TODO: sort by city ascending, then delivery_time_minutes descending\n# TODO: rename 'delivery_time_minutes' to 'delivery_min'\n#       and 'city' to 'destination_city'\n"}, {"path": "orders.csv", "content": "order_id,city,city_code,courier,driver_id,customer_id,pickup_date,delivery_time_minutes,distance_km,order_value\n1001,Lagos,LOS,Ada,201,301,2024-03-14,18,4.2,`

### `cw_text_dupes_missing` (code_workspace) - batch `final_batch_009_da_pandas` - content `2a07a79035`


`{"asset_kind": "code_workspace", "scenario_id": "scen_swiftdrop", "title": "String Cleaning, Duplicates, and Missing Values Workspace", "runtime": "pyodide", "files": [{"path": "starter.py", "content": "import pandas as pd\n\norders = pd.read_csv('orders_messy.csv')\n\n# The city column has mixed case and stray spaces\n# Some order_ids are duplicated\n# Some delivery_time_minutes values are missing\n\n# TODO: clean city with .str.strip().str.lower()\n# TODO: remove duplicate order_ids with drop_duplicates()\n# TODO: detect missing delivery times with isna()\n# TODO: fill missing delivery times`

### `ds.chart_selection_mini` (dataset) - batch `final_batch_012_da_viz` - content `3cc174a703`
Six-row dataset with columns distance_km and delivery_minutes, matching the column names used in the chart_type_selection practice anchor. Used for the scatter-vs-bar chart-type selection exercise.

Rows: 6
| column | type | role | notes |
|---|---|---|---|
| distance_km | number | numerical | Delivery distance in kilometres |
| delivery_minutes | integer | numerical | Delivery time in minutes |

### `ds.customers` (dataset) - batch `final_batch_005_da_sql_canary` - content `88a26efe10`
One row per customer. Columns: customer_id (integer PK), name, city. Used in sql.relational_model, sql.select_fundamentals, sql.distinct.

Rows: 8, variants: `customers.messy_v1`
| column | type | role | notes |
|---|---|---|---|
| customer_id | integer | identifier | Unique integer identifier for each customer (used as a label, not a quantity). |
| name | string | text | Full name of the customer. |
| city | string | categorical | City where the customer is located. |

### `ds.daily_averages` (dataset) - batch `final_batch_012_da_viz` - content `407b4df735`
Average delivery time per day (Mon–Fri) for Lagos and Abuja. Used for line-plot exercises (plt.plot(x, y)) and labeling/legend exercises (ax.set_xlabel, ax.set_ylabel, ax.set_title, ax.legend). Lagos values match the glossary example: [21, 23, 19, 25, 20].

Rows: 5
| column | type | role | notes |
|---|---|---|---|
| day | integer | identifier | Day number (1=Monday … 5=Friday) |
| lagos_avg | number | numerical | Average delivery time in Lagos for that day |
| abuja_avg | number | numerical | Average delivery time in Abuja for that day |

### `ds.orders` (dataset) - batch `final_batch_005_da_sql_canary` - content `7823e97702`
One row per delivery order. Columns: order_id (integer PK), customer_id (integer FK), delivery_time_minutes (integer). Used in sql.relational_model, sql.aliasing.

Rows: 10, variants: `orders.messy_v1`
| column | type | role | notes |
|---|---|---|---|
| order_id | integer | identifier | Unique integer identifier for each order (label, not a quantity). |
| customer_id | integer | identifier | Foreign key referencing customers.customer_id. |
| delivery_time_minutes | integer | numerical | Time in minutes from order placement to delivery. |

### `ds.orders` (dataset) - batch `final_batch_012_da_viz` - content `8a7dd38940`
Individual delivery orders for QuickDeliver across Lagos, Abuja, and Kano. Used for bar charts (city comparison), histograms (delivery time distribution), scatter plots (distance vs time), box plots (per-city spread), and seaborn exercises.

Rows: 24, variants: `ds.orders.messy`
| column | type | role | notes |
|---|---|---|---|
| order_id | integer | identifier | Unique order identifier |
| city | string | categorical | Delivery city: Lagos, Abuja, or Kano |
| delivery_time_minutes | integer | numerical | Total delivery time in minutes |
| distance_km | number | numerical | Delivery distance in kilometres |
| order_value | number | numerical | Order value in Nigerian Naira |
| num_items | integer | numerical | Number of items in the order |

### `ds.products` (dataset) - batch `final_batch_005_da_sql_canary` - content `5c9b6ea9de`
One row per product. Columns: product_id (integer PK), name, price (NGN). Introduced in sql.relational_model to complete the three-table database picture.

Rows: 5
| column | type | role | notes |
|---|---|---|---|
| product_id | integer | identifier | Unique integer identifier for each product (label, not a quantity). |
| name | string | text | Name of the product. |
| price | number | numerical | Price of the product in Nigerian Naira. |

### `ds.theming_demo` (dataset) - batch `final_batch_012_da_viz` - content `4a9e10781d`
Minimal three-row dataset with 'category' and 'value' columns, matching the seaborn_themes_palettes practice anchor starter state. Used for sns.set_theme() and sns.set_palette() exercises.

Rows: 3
| column | type | role | notes |
|---|---|---|---|
| category | string | categorical | Delivery city category |
| value | number | numerical | Average delivery time in minutes |

### `ds_ab_test_results` (dataset) - batch `final_batch_004_da_chunk2` - content `cc193855ab`
Summary table of A/B test runs for the QuickShip checkout-button redesign. Includes a small pilot (n=50 per group) and a large run (n=5000 per group), both showing the same 10% lift, plus two textbook proportion tests illustrating null-value-in-CI reasoning (null value 0.333).

Rows: 6, variants: `ds_ab_test_results_messy`
| column | type | role | notes |
|---|---|---|---|
| test_id | string | identifier | Unique identifier for the test run |
| variant | string | categorical | Which group: control or variation |
| n_per_group | integer | numerical | Number of users assigned to each group |
| conversions | integer | numerical | Number of completed orders in this group |
| conversion_rate | number | numerical | Proportion of users who completed an order |
| lift_pct | number | numerical | Percentage lift of variation over control; null for control rows |
| p_value | number | numerical | p-value from the hypothesis test; null for control rows |
| ci_lower | number | numerical | Lower bound of 95% confidence interval for the lift; null for control rows |
| ci_upper | number | numerical | Upper bound of 95% confidence interval for the lift; null for control rows |
| null_value_in_ci | string | categorical | Whether the null value (0% lift) falls inside the confidence interval: yes, no, or n/a |

### `ds_ab_test_summary` (dataset) - batch `final_batch_010_da_stats_capstone` - content `c7f43dc92a`
Summary of the checkout-button A/B test. Control (A): 500 users, 100 converted, rate=0.20. Treatment (B): 500 users, 110 converted, rate=0.22. Absolute difference: 0.02. Lift: 10.0% (positive).

Rows: 2
| column | type | role | notes |
|---|---|---|---|
| group | string | categorical | Test group: control (A) or treatment (B) |
| users | integer | numerical | Number of users in the group |
| conversions | integer | numerical | Number of users who completed an order |
| conversion_rate | number | numerical | Conversions / users; control=0.20, treatment=0.22 |

### `ds_ab_test_users` (dataset) - batch `final_batch_010_da_stats_capstone` - content `25fccd7f1a`
Individual user records for the checkout-button A/B test. 50 rows: 25 control users (5 converted, rate=0.20) and 25 treatment users (6 converted, rate=0.24). Used for field_selection exercises identifying control/treatment groups and the comparison metric.

Rows: 50
| column | type | role | notes |
|---|---|---|---|
| user_id | string | identifier | Unique user identifier |
| group | string | categorical | Test group assignment: 'control' or 'treatment' |
| converted | integer | numerical | 1 if the user completed an order, 0 otherwise |

### `ds_capstone_delivery_sheet` (dataset) - batch `final_batch_010_da_stats_capstone` - content `7e6a34e3c2`
Delivery records with zone, shift, and delivery_time for the spreadsheet PivotTable and COUNTIFS exercise. Each row pairs an order's zone and delivery_time with the driver's shift. COUNTIFS(zone_range, 'Ikeja', delivery_time_range, '>45') returns 2 (rows with 48 and 178 minutes).

Rows: 36
| column | type | role | notes |
|---|---|---|---|
| zone | string | categorical | Delivery zone within Lagos |
| shift | string | categorical | Driver shift: morning, afternoon, or evening |
| delivery_time | integer | numerical | Delivery time in minutes |

### `ds_capstone_drivers` (dataset) - batch `final_batch_004_da_chunk2` - content `2e8ccaf632`
Driver roster for QuickShip, read from an Excel workbook via read_excel(). Columns match the glossary's capstone example: driver_id, name, zone, shift. driver_id is the join key linking this table to the orders table.

Rows: 6
| column | type | role | notes |
|---|---|---|---|
| driver_id | string | identifier | Unique driver identifier; foreign key to orders table |
| name | string | text | Driver full name |
| zone | string | categorical | Primary delivery zone assigned to this driver |
| shift | string | categorical | Shift worked: morning or afternoon |

### `ds_capstone_drivers` (dataset) - batch `final_batch_010_da_stats_capstone` - content `4165e54224`
Driver roster for QuickRide. driver_id is the primary key. Orders.driver_id is a foreign key referencing this table. One driver delivers many orders (one-to-many relationship).

Rows: 8
| column | type | role | notes |
|---|---|---|---|
| driver_id | string | identifier | Primary key — uniquely identifies each driver |
| driver_name | string | text | Driver's full name |

### `ds_capstone_orders` (dataset) - batch `final_batch_004_da_chunk2` - content `37c0b268af`
Last-quarter order records for QuickShip, retrieved via SQL query from the company's orders database. Columns match the glossary's capstone example: zone, driver_id, delivery_time_min, order_date. One row has a null delivery_time_min (missing value — a key data-quality teaching point). Covers four delivery zones: Lagos-North, Lagos-South, Kano-Central, Abuja-West.

Rows: 12
| column | type | role | notes |
|---|---|---|---|
| order_id | string | identifier | Unique order identifier |
| zone | string | categorical | Delivery zone within the city |
| driver_id | string | identifier | Driver assigned to this order; foreign key to driver roster |
| delivery_time_min | number | numerical | Actual delivery time in minutes; null if delivery not yet completed |
| order_date | date | datetime | Date the order was placed (last quarter) |
| on_time | string | categorical | Whether delivery met the 25-minute target: yes, no, or unknown |

### `ds_capstone_orders` (dataset) - batch `final_batch_010_da_stats_capstone` - content `61eb77fbe3`
Last-quarter orders (2026-04-01 to 2026-06-30) for QuickRide. Used for SQL retrieval (INNER JOIN with drivers, WHERE date range, GROUP BY zone), pandas cleaning (NaN delivery_times, groupby zone mean), descriptive statistics (Ikeja mean=52.0, median=38.0), and multi-panel dashboard visualisation.

Rows: 34, variants: `ds_capstone_orders_messy`
| column | type | role | notes |
|---|---|---|---|
| order_id | string | identifier | Unique order identifier |
| driver_id | string | identifier | Foreign key referencing drivers.driver_id |
| zone | string | categorical | Delivery zone within Lagos |
| order_date | date | datetime | Date the order was placed (YYYY-MM-DD) |
| delivery_time | integer | numerical | Delivery time in minutes; NULL where not yet recorded |

### `ds_capstone_zone_summary` (dataset) - batch `final_batch_004_da_chunk2` - content `257f8d1ba0`
Zone-level delivery performance summary produced by the capstone analysis. Answers the scoped question: which delivery zones are missing the 25-minute target, and by how much. Lagos-North and Lagos-South both miss the target; Abuja-West is fully on target. Used in the narrated stakeholder summary and deliverable documentation.

Rows: 4
| column | type | role | notes |
|---|---|---|---|
| zone | string | categorical | Delivery zone |
| n_orders | integer | numerical | Number of orders in the last quarter |
| avg_delivery_min | number | numerical | Average delivery time in minutes, computed over non-null delivery_time_min values only |
| target_min | integer | numerical | Company delivery-time target |
| pct_on_time | number | numerical | Percentage of orders meeting the target |
| gap_min | number | numerical | Average gap above target (positive = missing target); 0.0 if on target |

### `ds_city_delivery_summary` (dataset) - batch `final_batch_003_da_chunk` - content `2108e7f0fc`
Monthly average delivery times and order volumes for Lagos, Abuja, and Kano across two months. Lagos average rose from 22 to 30 minutes. Supports bar chart (city comparison), line chart (trend over time), pie chart (share of total orders), and stakeholder recommendation teaching.

Rows: 6
| column | type | role | notes |
|---|---|---|---|
| city | string | categorical | Delivery city |
| month | string | categorical | Month label (e.g. 'Month 1', 'Month 2') |
| avg_delivery_minutes | number | numerical | Average delivery time in minutes for that city and month |
| order_count | integer | numerical | Total number of orders delivered in that city and month |

### `ds_city_delivery_summary` (dataset) - batch `final_batch_004_da_chunk2` - content `3dad4e7877`
City-level delivery performance summary for QuickShip's three operating cities. Lagos average delivery time rose to 30 minutes against a 25-minute target (primary finding). Kano also misses the target. Abuja is on target. Used to teach finding prioritization (Lagos slowdown is the primary finding) and actionable recommendation framing.

Rows: 3, variants: `ds_city_delivery_summary_messy`
| column | type | role | notes |
|---|---|---|---|
| city | string | categorical | Delivery city: Lagos, Abuja, or Kano |
| avg_delivery_min | number | numerical | Average delivery time in minutes last month |
| target_min | integer | numerical | Company delivery-time target in minutes |
| pct_on_time | number | numerical | Percentage of deliveries meeting the target |
| variability_rank | string | categorical | Relative variability of delivery times: low or medium |
| n_couriers | integer | numerical | Number of active couriers in this city |
| finding_priority | string | categorical | Priority of this city's finding for the operations manager: primary or secondary |

### `ds_correlation_matrix` (dataset) - batch `final_batch_003_da_chunk` - content `c9643ae644`
Pairwise Pearson correlation coefficients for distance_km, package_weight_kg, and delivery_minutes. Values: distance/delivery_minutes=0.82 (strong positive), weight/delivery_minutes=-0.41 (moderate negative), distance/weight=-0.38 (weak negative). Used to teach ranking by magnitude and confounding variable reasoning.

Rows: 3
| column | type | role | notes |
|---|---|---|---|
| variable | string | identifier | Row variable name |
| distance_km | number | numerical | Correlation with distance_km |
| package_weight_kg | number | numerical | Correlation with package_weight_kg |
| delivery_minutes | number | numerical | Correlation with delivery_minutes |

### `ds_courier_orders_base` (dataset) - batch `final_batch_002_da_canary_llm` - content `57db3d1681`
Ten delivery records for Kwik Courier. Covers every column the glossary teaching blocks name: order_id (identifier), city (categorical), delivery_min (numerical), driver (categorical), zone_code (numeric-looking categorical label). Used for the rows-and-columns explainer and the field-selection practice.

Rows: 10, variants: `ds_courier_orders_messy`
| column | type | role | notes |
|---|---|---|---|
| order_id | integer | identifier | Unique order number (e.g. 1042, 1043). A label, not a quantity. |
| city | string | categorical | Destination city for the delivery (Lagos, Abuja, Kano). Values are category labels. |
| delivery_min | integer | numerical | Time taken to complete the delivery in minutes. Arithmetic (sum, difference) is meaningful. |
| driver | string | categorical | Name of the driver who handled the delivery. A category label. |
| zone_code | integer | categorical | Numeric zone code for the delivery area (101, 102, 103). Stored as digits but arithmetic is meaningless — a categorical  |

### `ds_customers` (dataset) - batch `final_batch_003_da_chunk` - content `5c70fcb44c`
The customers entity table: customer_id (primary key), name, city. Used to teach entities/tables, primary keys, entity integrity, one-to-many relationships, normalization, and foreign key referencing.

Rows: 5, variants: `ds_customers.with_duplicate`
| column | type | role | notes |
|---|---|---|---|
| customer_id | integer | identifier | Primary key — unique integer label for each customer (not a quantity) |
| name | string | text | Customer full name |
| city | string | categorical | Customer's city: Lagos, Abuja, or Kano |

### `ds_customers` (dataset) - batch `final_batch_006_da_sql_rest` - content `97c5684655`
One row per registered customer. Used for JOIN, outer join, COALESCE, style conventions, and UNION exercises. Customer 4 has no orders (LEFT JOIN unmatched row demo). Customer 5 has NULL name and city (COALESCE demo). Customer 6 has city='Kano' (sibling for casing rule in messy variant).

Rows: 6, variants: `ds_customers_messy`
| column | type | role | notes |
|---|---|---|---|
| customer_id | integer | identifier | Unique customer identifier |
| name | string | pii | Customer full name; NULL if not recorded |
| city | string | categorical | Customer home city; NULL if not recorded |

### `ds_customers` (dataset) - batch `final_batch_009_da_pandas` - content `5346f62555`
Customer reference table. Shares customer_id with ds_orders. customer_id 315 exists here but not in orders (unmatched on right side). Used in merge_join practice: orders.merge(customers, on='customer_id').

Rows: 15
| column | type | role | notes |
|---|---|---|---|
| customer_id | integer | identifier | Customer identifier — matches customer_id in orders table |
| customer_name | string | categorical | Customer full name |
| segment | string | categorical | Customer segment: Individual or Business |
| signup_date | date | datetime | Date the customer registered |

### `ds_customers_pk_candidates` (dataset) - batch `final_batch_003_da_chunk` - content `b0f0f0ecd3`
A customers table with four candidate columns to evaluate as primary key: customer_id (valid PK: unique, never null), name (fails: two customers share a name), phone (fails: one null), signup_date (fails: two customers signed up on the same date). Used to teach primary key selection and entity integrity.

Rows: 5, variants: `ds_customers_pk_candidates.name_dup_highlighted`, `ds_customers_pk_candidates.phone_null_highlighted`
| column | type | role | notes |
|---|---|---|---|
| customer_id | integer | identifier | Valid primary key candidate: unique integer, never null |
| name | string | text | Customer name — fails as PK because two customers share a name |
| phone | string | text | Phone number — fails as PK because one row has a null value |
| signup_date | date | datetime | Signup date — fails as PK because two customers share the same date |

### `ds_delivery_frequency_table` (dataset) - batch `final_batch_003_da_chunk` - content `df67ec7d3d`
Frequency table of 21 delivery times grouped into 10-minute bins (with a single 50–80 min bin matching the glossary). Bins: 10–20 min: 4 orders, 20–30 min: 9 orders (modal bin), 30–40 min: 5 orders, 40–50 min: 2 orders, 50–80 min: 0 orders, 80–90 min: 1 order. Right-skewed with a single far-out delivery past 80 minutes.

Rows: 6
| column | type | role | notes |
|---|---|---|---|
| bin_label | string | categorical | 10-minute delivery-time bin label (e.g. '10–20 min') |
| bin_lower | integer | numerical | Lower bound of the bin (inclusive) |
| bin_upper | integer | numerical | Upper bound of the bin (exclusive) |
| order_count | integer | numerical | Number of orders whose delivery time falls in this bin |

### `ds_delivery_orders` (dataset) - batch `final_batch_007_da_nocode` - content `b45e7d1006`
One week of delivery orders for Kwik Courier across Lagos, Abuja and Port Harcourt. Used throughout tile_data_quality_and_workflow and tile_stakeholder_framing_requirements. The clean base has 12 rows; the 'messy' variant plants three quality issues (missing value, duplicate row, impossible value) matching the glossary's teaching examples.

Rows: 12, variants: `ds_delivery_orders_messy`
| column | type | role | notes |
|---|---|---|---|
| order_id | integer | identifier | Unique order number — a digit used as a label, not a quantity |
| order_date | date | datetime | Date the order was placed (YYYY-MM-DD) |
| city | string | categorical | Destination city for the delivery |
| delivery_minutes | integer | numerical | Time from order dispatch to delivery confirmation, in minutes |
| driver_id | integer | identifier | Driver identifier — a digit used as a label, not a quantity |
| customer_name | string | pii | Customer full name — personally identifiable information |
| customer_phone | string | pii | Customer phone number including country code — personally identifiable information |

### `ds_delivery_orders_extended` (dataset) - batch `final_batch_003_da_chunk` - content `8460c2b351`
Twenty delivery orders with distance, package weight, city, priority flag, and delivery time. Supports correlation analysis (distance/time ≈ 0.83 strong positive; weight/time ≈ -0.42 moderate negative; distance/weight ≈ -0.37 weak negative) and city-level comparisons (Lagos, Abuja, Kano). Priority toggle illustrates correlation-vs-causation caveat.

Rows: 20
| column | type | role | notes |
|---|---|---|---|
| order_id | string | identifier | Unique order reference |
| city | string | categorical | Delivery city: Lagos, Abuja, or Kano |
| distance_km | number | numerical | Distance from dispatch hub to delivery address in kilometres |
| package_weight_kg | number | numerical | Package weight in kilograms |
| priority | boolean | categorical | Whether the customer selected the priority delivery toggle |
| delivery_minutes | integer | numerical | Actual delivery time in minutes from dispatch to doorstep |

### `ds_delivery_times` (dataset) - batch `final_batch_008_da_python_core` - content `6e8c9dcdd6`
Tabular form of the delivery_times list from the lists teaching block: [32, 45, 21, 60, 18, ...]. Used for list, loop, comprehension and iterating exercises.

Rows: 10
| column | type | role | notes |
|---|---|---|---|
| position | integer | identifier | 0-based index position in the delivery_times list |
| minutes | integer | numerical | Delivery time in minutes (glossary list: [32, 45, 21, 60, 18, ...]) |

### `ds_delivery_times_sample` (dataset) - batch `final_batch_003_da_chunk` - content `f87dc57657`
Nine delivery-time observations used to illustrate distribution shape. Values: 18, 20, 22, 22, 26, 28, 34, 41, 52 minutes. Right-skewed: bulk sits 18–28 min, tail trails right. Mean ≈ 29.2, median = 26.

Rows: 9, variants: `ds_delivery_times_sample.outlier`
| column | type | role | notes |
|---|---|---|---|
| order_id | string | identifier | Unique order reference |
| delivery_minutes | integer | numerical | Actual delivery time in minutes from dispatch to doorstep |

### `ds_drivers` (dataset) - batch `final_batch_009_da_pandas` - content `fb77327f5c`
Driver reference table. Shares driver_id with ds_orders. driver_id 204 exists here but not in orders (unmatched on right side of a left join). Used in merge_join teaching block: orders.merge(drivers, on='driver_id').

Rows: 4
| column | type | role | notes |
|---|---|---|---|
| driver_id | integer | identifier | Driver identifier — matches driver_id in orders table |
| driver_name | string | categorical | Full name of the driver |
| vehicle | string | categorical | Vehicle type: Motorcycle or Van |
| base_city | string | categorical | City where the driver is based |

### `ds_feb_orders` (dataset) - batch `final_batch_009_da_pandas` - content `2960c0c40f`
February delivery orders — identical columns to ds_jan_orders and ds_mar_orders. Used in concat_stacking teaching block as feb_orders.

Rows: 5
| column | type | role | notes |
|---|---|---|---|
| order_id | integer | identifier |  |
| city | string | categorical |  |
| courier | string | categorical |  |
| delivery_time_minutes | integer | numerical |  |
| order_value | number | numerical |  |

### `ds_finding_statements` (dataset) - batch `final_batch_007_da_nocode` - content `c1456ac779`
Five pairs of vague and precise finding statements drawn from the Kwik Courier scenario. The first row matches the glossary's exact teaching example. Used in tile_stakeholder_framing_requirements for the before_after visual anchor and the external_proof practice anchor on stating findings precisely.

Rows: 5
| column | type | role | notes |
|---|---|---|---|
| finding_id | integer | identifier | Row identifier — a digit used as a label, not a quantity |
| vague_finding | string | text | The imprecise finding statement — lacks a specific number or comparison |
| precise_finding | string | text | The rewritten precise finding — names a specific number and includes a comparison |
| has_specific_number | boolean | categorical | True if the precise finding names at least one specific number |
| has_comparison | boolean | categorical | True if the precise finding includes a comparison to a prior period or group |
| is_complete_sentence | boolean | categorical | True if the precise finding is a complete sentence with a subject and verb |

### `ds_jan_orders` (dataset) - batch `final_batch_009_da_pandas` - content `671a99f301`
January delivery orders — identical columns to ds_feb_orders and ds_mar_orders. Used in concat_stacking teaching block as jan_orders.

Rows: 5
| column | type | role | notes |
|---|---|---|---|
| order_id | integer | identifier |  |
| city | string | categorical |  |
| courier | string | categorical |  |
| delivery_time_minutes | integer | numerical |  |
| order_value | number | numerical |  |

### `ds_mar_orders` (dataset) - batch `final_batch_009_da_pandas` - content `86396cb43b`
March delivery orders — identical columns to ds_jan_orders and ds_feb_orders. Used in concat_stacking teaching block as mar_orders.

Rows: 5
| column | type | role | notes |
|---|---|---|---|
| order_id | integer | identifier |  |
| city | string | categorical |  |
| courier | string | categorical |  |
| delivery_time_minutes | integer | numerical |  |
| order_value | number | numerical |  |

### `ds_monthly_long` (dataset) - batch `final_batch_009_da_pandas` - content `51ca2533dc`
One row per city-month combination (city, month, deliveries). Used in pivot_table_reshaping teaching block as long_deliveries. Contains a duplicate Lagos-jan row so that aggfunc='sum' and aggfunc='mean' give different results, preventing a hard-coded answer from passing.

Rows: 10
| column | type | role | notes |
|---|---|---|---|
| city | string | categorical | Destination city |
| month | string | categorical | Month label: jan_deliveries, feb_deliveries, or mar_deliveries |
| deliveries | integer | numerical | Number of deliveries for this city-month combination |

### `ds_monthly_wide` (dataset) - batch `final_batch_009_da_pandas` - content `b2d7f14490`
One row per city, one column per month (jan_deliveries, feb_deliveries, mar_deliveries). Used in melt_reshaping teaching block as city_deliveries. melt(id_vars=['city'], var_name='month', value_name='deliveries') produces ds_monthly_long.

Rows: 3
| column | type | role | notes |
|---|---|---|---|
| city | string | categorical | Destination city |
| jan_deliveries | integer | numerical | Number of deliveries completed in January |
| feb_deliveries | integer | numerical | Number of deliveries completed in February |
| mar_deliveries | integer | numerical | Number of deliveries completed in March |

### `ds_order_city` (dataset) - batch `final_batch_008_da_python_core` - content `bd8fd6a535`
Tabular form of the order_city dictionary from the dictionaries teaching block: {1042: 'Lagos', 1043: 'Abuja', 1044: 'Kano', ...}. Used for dict, iteration and set exercises.

Rows: 8
| column | type | role | notes |
|---|---|---|---|
| order_id | integer | identifier | Order id used as dictionary key (glossary: order_city = {1042: 'Lagos', ...}) |
| city | string | categorical | City value in the order_city dictionary |

### `ds_order_items` (dataset) - batch `final_batch_003_da_chunk` - content `ff14b0b5a3`
Junction table resolving the many-to-many relationship between orders and products. Each row is one (order, product) pairing. Composite primary key: (order_id, product_id). Teaching block pairings: order 101 with rice bag (product 10), order 101 with cooking oil (product 11), order 103 with rice bag (product 10).

Rows: 8
| column | type | role | notes |
|---|---|---|---|
| order_id | integer | identifier | Foreign key referencing orders.order_id — part of composite primary key |
| product_id | integer | identifier | Foreign key referencing products.product_id — part of composite primary key |

### `ds_order_items` (dataset) - batch `final_batch_006_da_sql_rest` - content `d6811f8d3b`
One row per line item within an order. Used for composite join exercises (join to shipments on order_id AND product_id).

Rows: 10
| column | type | role | notes |
|---|---|---|---|
| order_id | integer | identifier | FK to orders.order_id |
| product_id | integer | identifier | FK to a products catalogue |
| quantity | integer | numerical | Number of units ordered |
| unit_price | number | numerical | Price per unit at time of order |

### `ds_orders` (dataset) - batch `final_batch_003_da_chunk` - content `822761d5df`
The orders entity table: order_id (primary key), customer_id (foreign key → customers), delivery_minutes. Used to teach foreign keys, referential integrity, one-to-many relationships, and normalization. Multiple orders per customer demonstrate the 1:M relationship.

Rows: 7, variants: `ds_orders.with_orphan`
| column | type | role | notes |
|---|---|---|---|
| order_id | integer | identifier | Primary key — unique integer label for each order (not a quantity) |
| customer_id | integer | identifier | Foreign key referencing customers.customer_id — identifies which customer placed this order |
| delivery_minutes | integer | numerical | Actual delivery time in minutes |

### `ds_orders` (dataset) - batch `final_batch_006_da_sql_rest` - content `1902b59c9a`
One row per customer order. Used for WHERE, ORDER BY, LIMIT/OFFSET, aggregate functions, GROUP BY, HAVING, CASE, string/date/cast functions, COALESCE, UNION, clause execution order, and subquery exercises.

Rows: 13, variants: `ds_orders_messy`
| column | type | role | notes |
|---|---|---|---|
| order_id | integer | identifier | Unique order identifier |
| customer_id | integer | identifier | FK to customers.customer_id |
| delivery_time_minutes | integer | numerical | Elapsed minutes from order placement to delivery; NULL when not yet delivered |
| order_date | date | datetime | Calendar date the order was placed |
| region | string | categorical | Broad geographic region of the delivery address |
| amount | number | numerical | Total order value in Naira |
| city | string | categorical | City of the delivery address |

### `ds_orders` (dataset) - batch `final_batch_008_da_python_core` - content `4e7aeac4e3`
Flat table of delivery orders. Mirrors the orders.csv file named in the file_io teaching block. Columns match the glossary's csv.DictReader example: order_id, city, delivery_minutes. Extended with is_late and driver_id for richer boolean/identifier exercises.

Rows: 15, variants: `orders_messy`
| column | type | role | notes |
|---|---|---|---|
| order_id | integer | identifier | Unique order identifier (glossary: order_id = 1042) |
| city | string | categorical | Destination city (glossary cities: Lagos, Abuja, Kano, Ibadan) |
| delivery_minutes | number | numerical | Actual delivery time in minutes (glossary: delivery_minutes = 32) |
| is_late | boolean | categorical | True if delivery exceeded the 45-minute SLA (glossary: is_late = True) |
| driver_id | integer | identifier | Driver identifier; numeric label, not a quantity |

### `ds_orders` (dataset) - batch `final_batch_009_da_pandas` - content `967214883b`
One row per delivery order. Columns match the names used in all pandas teaching blocks: order_id, city, city_code, courier, driver_id, customer_id, pickup_date, delivery_time_minutes, distance_km, order_value. The first 7 rows reproduce the exact delivery_time_minutes sequence [18, 20, 22, 22, 26, 28, 80] from the descriptive-stats teaching block.

Rows: 14, variants: `orders_messy`
| column | type | role | notes |
|---|---|---|---|
| order_id | integer | identifier | Unique dispatch order number (1001, 1002, …) — numeric-looking label, not a quantity |
| city | string | categorical | Destination city: Lagos, Abuja, or Kano |
| city_code | string | categorical | Three-letter city code used in map_substitution examples: LOS, ABJ, KAN |
| courier | string | categorical | Courier name (Ada, Bayo, Chidi, …) |
| driver_id | integer | identifier | Driver identifier — numeric-looking label, not a quantity |
| customer_id | integer | identifier | Customer identifier — numeric-looking label, not a quantity |
| pickup_date | date | datetime | ISO date string of order pickup (2024-03-14 style); converted with pd.to_datetime() |
| delivery_time_minutes | integer | numerical | Minutes from pickup to delivery; the 7-value batch [18,20,22,22,26,28,80] is used in descriptive-stats examples |
| distance_km | number | numerical | Route distance in kilometres |
| order_value | number | numerical | Order value in Naira; used in groupby_aggregation examples |

### `ds_pandas_orders` (dataset) - batch `final_batch_010_da_stats_capstone` - content `b22624751f`
Small orders DataFrame for the pandas cleaning exercise. Contains 'zone' and 'delivery_time' columns with NaN delivery_times. After dropna(), groupby('zone')['delivery_time'].mean() returns one mean per zone.

Rows: 15
| column | type | role | notes |
|---|---|---|---|
| zone | string | categorical | Delivery zone within Lagos |
| delivery_time | integer | numerical | Delivery time in minutes; None where not recorded |

### `ds_product_sales` (dataset) - batch `final_batch_009_da_pandas` - content `3d50e07f92`
Long-format sales table with product, month, and sales columns. Several product-month pairs repeat so that pivot_table aggfunc='sum' and aggfunc='mean' give different results. Used in pivot_table_reshaping practice.

Rows: 12
| column | type | role | notes |
|---|---|---|---|
| product | string | categorical | Product name |
| month | string | categorical | Month label (Jan, Feb, Mar) |
| sales | number | numerical | Sales amount in Naira |

### `ds_products` (dataset) - batch `final_batch_003_da_chunk` - content `4426c9e76f`
The products entity table: product_id (primary key), name. An independent entity — a product can exist without any orders. Used to teach many-to-many relationships and junction tables. Includes the rice bag and cooking oil mentioned in teaching blocks.

Rows: 5
| column | type | role | notes |
|---|---|---|---|
| product_id | integer | identifier | Primary key — unique integer label for each product (not a quantity) |
| name | string | text | Product name |

### `ds_seven_delivery_times` (dataset) - batch `final_batch_010_da_stats_capstone` - content `d8447d39b4`
The exact seven delivery times used in the teaching blocks for measures of center and spread: 18, 20, 22, 22, 26, 28, 80 minutes. Mean ≈ 30.9, median = 22, mode = 22, range = 62, variance ≈ 481.1, std ≈ 21.9.

Rows: 7
| column | type | role | notes |
|---|---|---|---|
| order_id | string | identifier | Unique order identifier |
| delivery_time | integer | numerical | Delivery time in minutes from dispatch to drop-off |

### `ds_shipments` (dataset) - batch `final_batch_006_da_sql_rest` - content `a63671969c`
One row per dispatched line item. Used for composite join exercises (join to order_items on order_id AND product_id). Several order_items rows have no matching shipment row, so an inner join drops them while an outer join keeps them.

Rows: 6
| column | type | role | notes |
|---|---|---|---|
| order_id | integer | identifier | FK to orders.order_id |
| product_id | integer | identifier | FK to a products catalogue |
| shipped_date | date | datetime | Date the item was physically dispatched |

### `ds_stakeholder_requests` (dataset) - batch `final_batch_007_da_nocode` - content `45c6aacec4`
A lookup table of six vague stakeholder requests paired with their underlying decision, a rewritten measurable analytical question, and the question's components (variable, group, intent). Used in tile_stakeholder_framing_requirements for practice anchors on identifying decision need, framing the analytical question, and identifying requirements.

Rows: 6
| column | type | role | notes |
|---|---|---|---|
| request_id | integer | identifier | Row identifier — a digit used as a label, not a quantity |
| request_text | string | text | The vague stakeholder request as originally stated |
| decision | string | text | The underlying business decision the analysis is meant to inform |
| vague_question | string | text | The question as first stated — vague, not yet measurable |
| measurable_question | string | text | The rewritten well-formed statistical question naming variable, group, and intent |
| variable_of_interest | string | categorical | The measurable variable the question focuses on |
| group_or_period | string | categorical | The group or time period the question focuses on |
| intent | string | categorical | The statistical intent: comparison, description, or association |

### `northstar_orders` (dataset) - batch `final_batch_001_da_canary` - content `f0a0210df6`
Six delivered orders. Column roles are declared so categorical/numerical answer keys can be checked by script.

Rows: 6, variants: `messy`
| column | type | role | notes |
|---|---|---|---|
| order_id | string | identifier | Unique order number |
| customer_segment | string | categorical | Student, Professional or Business |
| city | string | categorical | Destination city |
| zone_code | integer | categorical | Delivery zone label written as digits: a label, not a quantity |
| items | integer | numerical | Number of items in the order |
| order_value_ngn | number | numerical | Order value in naira |
| payment_method | string | categorical | Transfer, Card or Cash |
| driver | string | categorical | Driver who delivered the order |
| delivery_minutes | integer | numerical | Minutes from dispatch to arrival |
