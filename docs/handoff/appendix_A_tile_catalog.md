# Appendix A: Tile catalog (all 72 tiles, in learning order)

Source: `tile_lessons/` of the batch named in each row. Order, regions and terrains come from the frozen TOC (`04_data_analyst_V2_WORKSPACE/toc.json`).

## Region: Data Analysis Foundations (`region_data_analysis_foundations`)
Understand the shape, quality, and responsible use of data before learning tools.

### Terrain: How Data Analysis Works (`terrain_data_analysis_foundations`)
Learn the basic language and workflow of analysis.

#### 1. Datasets and Variable Types  (`tile_data_shape_and_types`)
Learn how data is organised into rows and columns, and how to tell categorical variables from numerical ones.

- Concepts: `data.dataset_rows_columns`, `data.categorical_numeric_types`
- Built in: `final_batch_002_da_canary_llm` | content_hash `367a6b98957b…` | steps 8 (3 explainer, 2 check, 2 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 1 table_select, 1 classify | runtimes: none | packs: core, data
- Blocks used: data_table, prose, up_next
- Assets: ds_courier_orders_base | est. minutes: ? | completion reward: {'gems': 24} | next tile: `None`
- Public copy present: yes | step titles: A dataset is a table of observations; Rows are observations; columns are variables; Which part of the table is a variable?; Mark rows and columns in the delivery table; Categorical and numerical variables; Categorical or numerical?; Classify every column in the delivery table; What you've learned

#### 2. Data Quality and the Analysis Workflow  (`tile_data_quality_and_workflow`)
Learn to check whether a dataset is fit for purpose using four quality checks (completeness, uniqueness, validity, accuracy), follow a six-stage repeatable analysis workflow, and apply basic data-ethics and privacy principles when handling and sharing data.

- Concepts: `data.data_quality_basics`, `data.analysis_workflow`, `data.ethics_privacy_basics`
- Built in: `final_batch_007_da_nocode` | content_hash `9c4de6a74846…` | steps 18 (7 explainer, 2 video, 5 check, 3 hands_on, 1 recap) | remediation steps 5
- Interactions: 5 choice, 1 find_issues, 1 ordering, 1 table_select | runtimes: none | packs: core, data
- Blocks used: data_table, media_group, process_flow, prose, up_next
- Assets: ds_delivery_orders | est. minutes: ? | completion reward: {'gems': 60} | next tile: `tile_python_variables_types`
- Public copy present: yes | step titles: Is the data any good?; Data-quality dimensions in action; Validity, accuracy, and good enough; Fitness for purpose and missing or duplicate records; Invalid vs inaccurate values, and good-enough data; Flag the quality problems; A repeatable order for analysis; One analysis walked through in order; Analyzing and visualizing are different steps; Communicating findings is part of the workflow; The workflow loops back; Put the workflow in order; The people behind the data; Honest reporting and the limits of removing names; Privacy, minimal collection, and impact; Honest reporting and re-identification risk; Which columns should you keep?; What you've learned

## Region: Python Fundamentals (`region_python_fundamentals`)
Learn Python from scratch: variables, data types, data structures, control flow, and functions, building the coding foundation for pandas.

### Terrain: Variables, Types, and Data Structures (`terrain_python_variables_types_structures`)
Store and manipulate values with variables, core types, and Python's built-in data structures.

#### 3. Variables and Core Data Types  (`tile_python_variables_types`)
Learn to store values in variables using Python's assignment operator, understand naming rules, and recognise the four core scalar types: int, float, str and bool.

- Concepts: `python.variables_assignment`, `python.core_data_types`
- Built in: `final_batch_008_da_python_core` | content_hash `536f33da71a3…` | steps 9 (4 explainer, 2 check, 2 hands_on, 1 recap) | remediation steps 4
- Interactions: 2 choice, 2 code_exercise | runtimes: python | packs: core
- Blocks used: before_after, code_walkthrough, prose, side_by_side, up_next
- Assets: none | est. minutes: ? | completion reward: {'gems': 80} | next tile: `tile_python_operators_conversion`
- Public copy present: yes | step titles: Storing a value under a name; Naming rules and using stored values; What happens when you use an unassigned name?; Assign and reassign delivery variables; Four kinds of value: int, float, str and bool; Printing values and checking types; Predict print() output and check a type; Create one variable of each core type; What you learned

#### 4. Comparison and Logical Operators  (`tile_python_operators_conversion`)
Learn Python's arithmetic, comparison and logical operators, understand short-circuit evaluation and operator priority, and convert values between int, float and str.

- Concepts: `python.arithmetic_operators`, `python.comparison_operators`, `python.logical_operators`, `python.type_conversion`
- Built in: `final_batch_008_da_python_core` | content_hash `f1a45bdae791…` | steps 17 (5 explainer, 7 check, 4 hands_on, 1 recap) | remediation steps 6
- Interactions: 7 choice, 4 code_exercise | runtimes: python | packs: core
- Blocks used: before_after, code_walkthrough, prose, side_by_side, up_next
- Assets: none | est. minutes: ? | completion reward: {'gems': 160} | next tile: `tile_python_lists_dicts_tuples`
- Public copy present: yes | step titles: Seven operators for numeric work; Predict the result of a grouped, mixed-type expression; Use arithmetic operators on delivery data; Six operators that return True or False; Choose the right comparison operator; Predict the boolean result of a comparison; Write comparison expressions for delivery data; Combining conditions with and, or and not; not, priority and real-world compound conditions; Predict operator priority in a mixed expression; Predict the result of a short-circuit expression; Write compound boolean expressions; Converting between strings and numbers; Convert a value to the target type; Recognise an invalid conversion; Convert delivery data between types; What you learned

#### 5. Lists, Dictionaries, and Tuples  (`tile_python_lists_dicts_tuples`)
Store ordered sequences in lists, map keys to values in dictionaries, and group fixed records in immutable tuples.

- Concepts: `python.lists`, `python.dictionaries`, `python.tuples`
- Built in: `final_batch_008_da_python_core` | content_hash `ce6968912457…` | steps 14 (5 explainer, 2 video, 3 check, 3 hands_on, 1 recap) | remediation steps 3
- Interactions: 3 choice, 3 code_exercise | runtimes: python | packs: core
- Blocks used: before_after, code_walkthrough, diagram, media_group, prose, side_by_side, up_next
- Assets: none | est. minutes: ? | completion reward: {'gems': 105} | next tile: `tile_python_sets_strings`
- Public copy present: yes | step titles: Ordered, mutable sequences; Lists in action; Adding items with append(); Modify and extend a list; Build and work with a list of delivery times; Key-to-value lookup; Dictionaries in action; Testing key membership with in; Predict what happens with a missing key; Build and query an order-city dictionary; Immutable sequences and unpacking; Recognise when a one-item tuple needs a trailing comma; Create, inspect and unpack a tuple; What you learned

#### 6. Sets and Strings  (`tile_python_sets_strings`)
Use sets to collect unique values and test membership, combine sets with union and intersection, and build readable messages with f-strings and format specifiers.

- Concepts: `python.sets`, `python.string_basics_formatting`
- Built in: `final_batch_008_da_python_core` | content_hash `f0d652c33793…` | steps 10 (3 explainer, 1 video, 3 check, 2 hands_on, 1 recap) | remediation steps 3
- Interactions: 3 choice, 2 code_exercise | runtimes: python | packs: core
- Blocks used: before_after, code_walkthrough, media_group, prose, side_by_side, up_next
- Assets: none | est. minutes: ? | completion reward: {'gems': 80} | next tile: `tile_python_conditionals_for_loops`
- Public copy present: yes | step titles: Unique, unordered collections; Sets in action; Union and intersection; Create a set of unique values; Combine sets with union and intersection; Test membership in a set of cities; Embedding values and formatting numbers; Embed a quote without escaping; Write a formatted f-string; What you learned

### Terrain: Control Flow and Comprehensions (`terrain_python_control_flow_comprehensions`)
Branch and repeat code, then build collections concisely with comprehensions.

#### 7. Conditionals and For Loops  (`tile_python_conditionals_for_loops`)


- Concepts: `python.conditional_statements`, `python.for_loops`
- Built in: `final_batch_008_da_python_core` | content_hash `bcd1f7d2e54d…` | steps 9 (2 explainer, 3 check, 2 hands_on, 1 video, 1 recap) | remediation steps 3
- Interactions: 3 choice, 2 code_exercise | runtimes: python | packs: core
- Blocks used: heading, media_group, process_flow, prose, up_next
- Assets: none | est. minutes: ? | completion reward: {'gems': 50} | next tile: `tile_python_while_loop_control`
- Public copy present: yes | step titles: Branching on data: if, elif, else; When does an if block run?; Which branch runs?; Write an if/elif/else chain; Visiting every item: the for loop; Stepping through a list with a for loop; Trace the loop variable; Write a for loop over a collection; What you've learned

#### 8. While Loops and Loop Control  (`tile_python_while_loop_control`)


- Concepts: `python.while_loops`, `python.loop_control`
- Built in: `final_batch_008_da_python_core` | content_hash `3810555d8961…` | steps 8 (2 explainer, 1 video, 2 check, 2 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 2 code_exercise | runtimes: python | packs: core
- Blocks used: heading, media_group, process_flow, prose, up_next
- Assets: none | est. minutes: ? | completion reward: {'gems': 45} | next tile: `tile_python_comprehensions_iterating`
- Public copy present: yes | step titles: Repeating while a condition holds: the while loop; A while loop as a counter; Making a while loop terminate; Write a while loop with a condition; Steering mid-loop: break and continue; Skip an iteration with continue; Use break and continue in a loop; What you've learned

#### 9. Comprehensions and Iterating Collections  (`tile_python_comprehensions_iterating`)


- Concepts: `python.comprehensions`, `python.iterating_collections`
- Built in: `final_batch_008_da_python_core` | content_hash `696e4a5f5756…` | steps 7 (2 explainer, 2 check, 2 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 2 code_exercise | runtimes: python | packs: core
- Blocks used: before_after, code_walkthrough, heading, prose, side_by_side, up_next
- Assets: none | est. minutes: ? | completion reward: {'gems': 45} | next tile: `tile_python_functions_scope`
- Public copy present: yes | step titles: Building lists and dicts in one line: comprehensions; Write a dict comprehension; Write list and dict comprehensions; Looping over any collection: lists, dicts, sets and tuples; Set iteration order; Loop over keys and key-value pairs; What you've learned

### Terrain: Functions, Errors, and Modules (`terrain_python_functions_errors_modules`)
Package logic into reusable functions, handle errors gracefully, and read and write files.

#### 10. Defining Functions, Parameters, and Return Values  (`tile_python_functions_scope`)


- Concepts: `python.defining_calling_functions`, `python.parameters_arguments`, `python.return_values`, `python.function_default_keyword_args`, `python.variable_scope`
- Built in: `final_batch_008_da_python_core` | content_hash `9382c59e292e…` | steps 21 (6 explainer, 6 check, 5 hands_on, 3 video, 1 recap) | remediation steps 6
- Interactions: 6 choice, 5 code_exercise | runtimes: python | packs: core
- Blocks used: before_after, code_walkthrough, diagram, media_group, process_flow, prose, up_next
- Assets: none | est. minutes: ? | completion reward: {'gems': 122} | next tile: `tile_python_errors_imports`
- Public copy present: yes | step titles: Define once, run whenever you need it; Spot the function definition; Call a function to run its body; Give your function the inputs it needs; Match arguments to parameters; Add parameters and call with arguments; Hand a result back to the caller; Return values in action; Return and store a value; Write a function that returns a result; Optional parameters and named arguments; Default values and keyword arguments; Spot the mutable default trap; Call with defaults and keyword arguments; Where Python looks for a name; Local, global, and the global statement; Local shadows global without changing it; Predict name resolution; When do you need global?; Local vs global names; Functions: what you've learned

#### 11. Handling Errors and Importing Modules  (`tile_python_errors_imports`)


- Concepts: `python.error_handling`, `python.import_statements`
- Built in: `final_batch_008_da_python_core` | content_hash `fae52228bde8…` | steps 7 (2 explainer, 2 check, 2 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 2 code_exercise | runtimes: python | packs: core
- Blocks used: code_walkthrough, process_flow, prose, side_by_side, up_next
- Assets: none | est. minutes: ? | completion reward: {'gems': 45} | next tile: `tile_python_file_io`
- Public copy present: yes | step titles: Catch failures before they crash your script; Handle an invalid number conversion; Wrap risky code in try/except; Bring in code from other files; Write the correct import; Import and use a standard module; Errors and imports: what you've learned

#### 12. Reading and Writing Files  (`tile_python_file_io`)


- Concepts: `python.file_io`
- Built in: `final_batch_008_da_python_core` | content_hash `f986ec887954…` | steps 7 (2 explainer, 1 video, 2 check, 1 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 1 code_exercise | runtimes: python | packs: core
- Blocks used: before_after, code_walkthrough, media_group, prose, up_next
- Assets: ds_orders | est. minutes: ? | completion reward: {'gems': 38} | next tile: `tile_python_pep8_style`
- Public copy present: yes | step titles: Open a file and read its contents; Write text and CSV rows to a file; File I/O in Python; Open, read, and write a text file; Manage a file with the with statement; Read and write CSV rows as dicts; File I/O: what you've learned

#### 13. PEP 8 Style Conventions  (`tile_python_pep8_style`)


- Concepts: `python.pep8_style`
- Built in: `final_batch_008_da_python_core` | content_hash `07a6b7cbfc90…` | steps 4 (1 explainer, 1 check, 1 hands_on, 1 recap) | remediation steps 1
- Interactions: 1 choice, 1 code_exercise | runtimes: python | packs: core
- Blocks used: before_after, code_walkthrough, prose, up_next
- Assets: none | est. minutes: ? | completion reward: {'gems': 25} | next tile: `tile_stats_center_spread`
- Public copy present: yes | step titles: Write code others can read; Remove extraneous whitespace; Restyle a function to follow PEP 8; PEP 8: what you've learned

## Region: Descriptive Statistics (`region_descriptive_statistics`)
Compute and interpret measures of center, spread, distribution shape, and correlation to describe a dataset.

### Terrain: Descriptive Statistics for EDA (`terrain_stats_descriptive_eda`)
Summarize a dataset numerically and reason about relationships between variables.

#### 14. Measures of Center and Spread  (`tile_stats_center_spread`)
Introduces the three measures of central tendency (mean, median, mode) and three measures of spread (range, variance, standard deviation) using a seven-order QuickRide delivery dataset. Emphasises when the median is more representative than the mean, and why standard deviation is more interpretable than variance.

- Concepts: `stats.descriptive_measures_of_center`, `stats.measures_of_spread`
- Built in: `final_batch_010_da_stats_capstone` | content_hash `434e6f190127…` | steps 10 (4 explainer, 2 check, 2 hands_on, 1 video, 1 recap) | remediation steps 4
- Interactions: 2 choice, 2 code_exercise | runtimes: python | packs: core, data
- Blocks used: data_table, media_group, process_flow, prose, up_next
- Assets: ds_seven_delivery_times | est. minutes: ? | completion reward: {'gems': 27} | next tile: `tile_stats_shape_outliers`
- Public copy present: yes | step titles: What's a typical delivery time?; Mode and when the mean misleads; Choose the right center; Compute mean, median, and mode; How spread out are the delivery times?; Standard deviation and the range's blind spot; Variance and standard deviation, worked by hand; Why the range can mislead; Compute range, variance, and standard deviation; Center and spread: what you've learned

#### 15. Distribution Shape, Outliers, and Frequency Distributions  (`tile_stats_shape_outliers`)
Learn to read a distribution's shape as right-skewed, left-skewed, or symmetric; reason about outliers; and translate a frequency table into statements about where delivery times cluster and where rare values sit.

- Concepts: `stats.distribution_shape`, `stats.outlier_reasoning`, `stats.frequency_distribution_reading`
- Built in: `final_batch_003_da_chunk` | content_hash `1c19c3386ee6…` | steps 14 (5 explainer, 2 video, 3 check, 3 hands_on, 1 recap) | remediation steps 3
- Interactions: 3 choice, 2 table_select, 1 find_issues | runtimes: none | packs: core, data
- Blocks used: chart, data_table, media_group, prose, up_next
- Assets: ds_delivery_frequency_table, ds_delivery_orders_extended, ds_delivery_times_sample | est. minutes: ? | completion reward: {'gems': 110} | next tile: `tile_stats_correlation`
- Public copy present: yes | step titles: Which way does the tail point?; Symmetric distributions and what skew does to the mean; Symmetric, left-skewed and right-skewed distributions; Skew and the mean vs. median; Classify the shape of a delivery-time distribution; Spotting an outlier and deciding what to do with it; What should you do with an outlier?; Find and reason about the outlier in the delivery dataset; From a list of times to a histogram and frequency table; From stacked measurements to a frequency table and histogram; Reading the modal bin; Reading a frequency table; Read the delivery-time frequency table; What you've learned

#### 16. Correlation Between Two Variables  (`tile_stats_correlation`)
Read a correlation coefficient's sign and magnitude to describe the direction and strength of a linear relationship, rank pairwise correlations by magnitude, and restate correlational findings as associations rather than causal claims.

- Concepts: `stats.correlation`, `stats.correlation_interpretation`, `stats.correlation_vs_causation_caveat`
- Built in: `final_batch_003_da_chunk` | content_hash `8f5c0dfb6c75…` | steps 14 (5 explainer, 1 video, 4 check, 3 hands_on, 1 recap) | remediation steps 3
- Interactions: 4 choice, 3 table_select | runtimes: none | packs: core, data
- Blocks used: chart, data_table, media_group, prose, up_next
- Assets: ds_correlation_matrix, ds_delivery_orders_extended | est. minutes: ? | completion reward: {'gems': 83} | next tile: `tile_pandas_dataframe_reading`
- Public copy present: yes | step titles: Does Distance Predict Delivery Time?; Scatter Patterns and the Correlation Coefficient; Reading Strength — and One Important Limit; Positive or Negative?; What Correlation Can't Tell You; Read Correlation Values in the QuickShip Data; Ranking Relationships by Magnitude; A Strong Correlation Doesn't Rule Out a Third Variable; Could a Third Variable Explain This?; Rank the QuickShip Correlations by Strength; Moving Together Is Not the Same as Causing; Restate as an Association; Flag the Causal Claim; What You've Learned

## Region: Data Wrangling with pandas (`region_pandas_data_wrangling`)
Load, inspect, clean, transform, combine, and reshape real-world datasets using pandas DataFrames and Series.

### Terrain: pandas Basics: DataFrames, Inspection, and Selection (`terrain_pandas_basics_inspection_selection`)
Create and inspect DataFrames, summarize them statistically, and select subsets of data.

#### 17. DataFrames, Series, and Reading Data  (`tile_pandas_dataframe_reading`)
Learn the two core pandas data structures — Series and DataFrame — and how to load tabular data from CSV and Excel files into a DataFrame.

- Concepts: `pandas.dataframe_series_model`, `pandas.reading_data`
- Built in: `final_batch_009_da_pandas` | content_hash `b8210fd9133e…` | steps 11 (3 explainer, 2 video, 3 check, 2 hands_on, 1 recap) | remediation steps 4
- Interactions: 3 choice, 2 code_exercise | runtimes: python | packs: core, data
- Blocks used: before_after, code_walkthrough, data_table, diagram, media_group, prose, up_next
- Assets: ds_orders | est. minutes: ? | completion reward: {'gems': 61} | next tile: `tile_pandas_creating_inspecting`
- Public copy present: yes | step titles: Two building blocks: Series and DataFrame; Series and DataFrame from plain Python data; Building a DataFrame and accessing columns; Columns and Series; Build a Series and a DataFrame; Loading CSV and Excel files into a DataFrame; Reading a CSV into a DataFrame; Choosing the right reader; Arguments: path, sheet_name, and sep; Load the SwiftDrop orders CSV; What you've learned

#### 18. Creating and Inspecting DataFrames  (`tile_pandas_creating_inspecting`)
Build a DataFrame directly from Python data — a dict of lists or a list of dicts — then use head, shape, dtypes, info, and describe to get an immediate overview of what is inside.

- Concepts: `pandas.creating_dataframes`, `pandas.inspecting_dataframes`
- Built in: `final_batch_009_da_pandas` | content_hash `cd46e4fcb131…` | steps 11 (3 explainer, 2 video, 3 check, 2 hands_on, 1 recap) | remediation steps 3
- Interactions: 3 choice, 2 code_exercise | runtimes: python | packs: core
- Blocks used: code_walkthrough, comparison, diagram, media_group, prose, side_by_side, up_next
- Assets: ds_orders | est. minutes: ? | completion reward: {'gems': 59} | next tile: `tile_pandas_descriptive_stats`
- Public copy present: yes | step titles: Two ways to build a DataFrame from Python data; Building a DataFrame from Python data; Building a DataFrame from a list of dicts; Create a DataFrame two ways; Five methods that answer your first questions about a DataFrame; head, shape, dtypes, info, and describe in action; describe() — a statistical overview in one call; shape and info; describe() overview; Inspect the orders DataFrame; What you learned: creating and inspecting DataFrames

#### 19. Descriptive Statistics with pandas  (`tile_pandas_descriptive_stats`)
Compute mean, median, and standard deviation for a DataFrame column, and use describe() to get a full summary in one call.

- Concepts: `stats.pandas_descriptive_stats`
- Built in: `final_batch_009_da_pandas` | content_hash `1e3d1dcb3b17…` | steps 5 (1 explainer, 1 video, 1 check, 1 hands_on, 1 recap) | remediation steps 1
- Interactions: 1 choice, 1 code_exercise | runtimes: python | packs: core
- Blocks used: before_after, code_walkthrough, diagram, media_group, prose, up_next
- Assets: ds_orders | est. minutes: ? | completion reward: {'gems': 28} | next tile: `tile_pandas_selection_filtering`
- Public copy present: yes | step titles: Computing statistics directly from a column; describe, mean, median, and std in action; Reading a describe() summary table; Compute and interpret descriptive statistics; Descriptive statistics with pandas — key takeaways

#### 20. Selecting and Filtering Data  (`tile_pandas_selection_filtering`)
Use .loc and .iloc to select rows and columns by label or position, and apply boolean filters — single conditions or combined with & | ~ — to keep only the rows you need.

- Concepts: `pandas.loc_iloc_selection`, `pandas.boolean_filtering`
- Built in: `final_batch_009_da_pandas` | content_hash `e19d0f20df0a…` | steps 11 (3 explainer, 2 video, 3 check, 2 hands_on, 1 recap) | remediation steps 3
- Interactions: 3 choice, 2 code_exercise | runtimes: python | packs: core, data
- Blocks used: before_after, data_table, media_group, prose, side_by_side, up_next
- Assets: ds_orders | est. minutes: ? | completion reward: {'gems': 59} | next tile: `tile_pandas_sort_rename`
- Public copy present: yes | step titles: Two accessors: .loc for labels, .iloc for positions; Selecting rows and columns with .loc and .iloc; .iloc uses 0-based positions with an exclusive stop; Predict an iloc slice; Select rows and columns with .loc and .iloc; Filter rows with a True/False mask; Boolean masks in action; Writing a single-condition filter; Combining conditions with parentheses; Filter the orders DataFrame; What you learned: selecting and filtering data

### Terrain: Cleaning and Transforming Data (`terrain_pandas_cleaning_transforming`)
Sort, rename, convert types, and clean messy real-world columns.

#### 21. Sorting and Renaming  (`tile_pandas_sort_rename`)
Sort a DataFrame by one or more columns with sort_values, controlling ascending/descending order per column, and rename column and index labels with rename using a dict mapping.

- Concepts: `pandas.sort_values`, `pandas.rename_columns_index`
- Built in: `final_batch_009_da_pandas` | content_hash `64d902dae7fd…` | steps 7 (2 explainer, 2 check, 2 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 2 code_exercise | runtimes: python | packs: core, data
- Blocks used: before_after, data_table, prose, up_next
- Assets: ds_orders | est. minutes: ? | completion reward: {'gems': 45} | next tile: `tile_pandas_dtype_datetime`
- Public copy present: yes | step titles: sort_values: sort by one or more columns; Setting ascending per column; Sort the orders DataFrame; rename(): relabel columns and index entries with a dict; Renaming columns with a mapping; Rename columns and an index label; What you learned: sorting and renaming

#### 22. Type Conversion and Datetime Handling  (`tile_pandas_dtype_datetime`)
Learn to convert column dtypes with astype and to work with datetime data using pd.to_datetime and the .dt accessor.

- Concepts: `pandas.dtype_conversion`, `pandas.datetime_handling`
- Built in: `final_batch_009_da_pandas` | content_hash `dfb9966c6a03…` | steps 9 (2 explainer, 2 video, 2 check, 2 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 2 code_exercise | runtimes: python | packs: core
- Blocks used: before_after, code_walkthrough, media_group, prose, up_next
- Assets: ds_orders | est. minutes: ? | completion reward: {'gems': 51} | next tile: `tile_pandas_text_dupes_missing`
- Public copy present: yes | step titles: Fixing column types with astype; astype in action; Converting multiple columns at once; Convert a column's dtype with astype; Turning date text into real datetimes; Converting a text date column with pd.to_datetime; Extracting date components with .dt; Convert dates and extract a month column; Type conversion and datetime handling — key takeaways

#### 23. Text Cleaning, Duplicates, and Missing Data  (`tile_pandas_text_dupes_missing`)
Clean text columns with the .str accessor, remove duplicate rows with drop_duplicates, and handle missing values with isna, dropna, and fillna.

- Concepts: `pandas.str_accessor_cleaning`, `pandas.drop_duplicates`, `pandas.missing_data_handling`
- Built in: `final_batch_009_da_pandas` | content_hash `16e1d0358e74…` | steps 12 (3 explainer, 2 video, 3 check, 3 hands_on, 1 recap) | remediation steps 3
- Interactions: 3 choice, 3 code_exercise | runtimes: python | packs: core, data
- Blocks used: before_after, code_walkthrough, data_table, media_group, prose, up_next
- Assets: ds_orders | est. minutes: ? | completion reward: {'gems': 71} | next tile: `tile_pandas_map_apply`
- Public copy present: yes | step titles: Cleaning a text column with the .str accessor; Lowercasing every value in a column at once; Applying string methods across a column; Clean a text column with .str; Removing duplicate rows with drop_duplicates; Identifying duplicates with a subset; Remove duplicate rows and choose which to keep; Detecting, dropping, and filling missing values; Spotting and filling missing values; Choosing between drop and fill; Detect, drop, and fill missing values; Text cleaning, duplicates, and missing data — key takeaways

#### 24. Mapping and Applying Transformations  (`tile_pandas_map_apply`)


- Concepts: `pandas.map_substitution`, `pandas.apply_transform`
- Built in: `final_batch_009_da_pandas` | content_hash `ae89ffd3f3dd…` | steps 8 (2 explainer, 2 check, 2 hands_on, 1 video, 1 recap) | remediation steps 2
- Interactions: 2 choice, 2 code_exercise | runtimes: python | packs: core, data
- Blocks used: before_after, code_walkthrough, data_table, media_group, process_flow, prose, up_next
- Assets: ds_orders | est. minutes: ? | completion reward: {'gems': 25} | next tile: `tile_pandas_concat_merge`
- Public copy present: yes | step titles: Replacing values element-by-element with .map(); Recoding values with a dict mapping; Map city codes to full names; Running a custom function across rows or columns with .apply(); Applying a function across rows and columns; Applying a function across rows with axis=1; Label orders fast or slow with .apply(); Map substitution and apply — key takeaways

### Terrain: Combining and Reshaping Data (`terrain_pandas_combining_reshaping`)
Stack, merge, group, reshape, and export DataFrames.

#### 25. Concatenating and Merging DataFrames  (`tile_pandas_concat_merge`)


- Concepts: `pandas.concat_stacking`, `pandas.merge_join`
- Built in: `final_batch_009_da_pandas` | content_hash `f58bba9c7065…` | steps 11 (3 explainer, 2 video, 3 check, 2 hands_on, 1 recap) | remediation steps 3
- Interactions: 3 choice, 2 code_exercise | runtimes: python | packs: core, data
- Blocks used: before_after, code_walkthrough, data_table, diagram, media_group, prose, up_next
- Assets: ds_customers, ds_feb_orders, ds_jan_orders, ds_mar_orders, ds_orders | est. minutes: ? | completion reward: {'gems': 29} | next tile: `tile_pandas_groupby_melt`
- Public copy present: yes | step titles: Stacking DataFrames with pd.concat(); Concatenating DataFrames row-wise and column-wise; Choosing the concat axis; Stack the monthly order tables into one DataFrame; Joining two DataFrames on a shared key with merge(); Merging DataFrames on a shared key; Left, right, and outer joins; Merging on a shared key and choosing a join type; NA values for unmatched keys; Join orders to customers and predict the inner merge result; Concatenation and merging — key takeaways

#### 26. Grouping, Aggregating, and Reshaping with melt  (`tile_pandas_groupby_melt`)


- Concepts: `pandas.groupby_aggregation`, `pandas.melt_reshaping`
- Built in: `final_batch_009_da_pandas` | content_hash `22d4d87c288f…` | steps 10 (3 explainer, 2 video, 2 check, 2 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 2 code_exercise | runtimes: python | packs: core, data
- Blocks used: before_after, code_walkthrough, data_table, media_group, process_flow, prose, up_next
- Assets: ds_monthly_long, ds_monthly_wide, ds_orders | est. minutes: ? | completion reward: {'gems': 27} | next tile: `tile_pandas_pivot_export`
- Public copy present: yes | step titles: Split, apply, combine — groupby in three steps; groupby in practice; Calling groupby and choosing an aggregation; Describing the split-apply-combine process; Aggregate order values by customer; Turning a wide table into a long one with melt(); Reshaping wide to long with melt(); Renaming melt output columns; Melt the monthly deliveries table from wide to long; Groupby aggregation and melt — key takeaways

#### 27. Pivot Tables and Exporting to CSV  (`tile_pandas_pivot_export`)


- Concepts: `pandas.pivot_table_reshaping`, `pandas.export_to_csv`
- Built in: `final_batch_009_da_pandas` | content_hash `a0aaa955a5c7…` | steps 9 (3 explainer, 1 video, 2 check, 2 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 2 code_exercise | runtimes: python | packs: core, data
- Blocks used: before_after, code_walkthrough, data_table, media_group, prose, side_by_side, up_next
- Assets: ds_monthly_long, ds_orders, ds_product_sales | est. minutes: ? | completion reward: {'gems': 27} | next tile: `tile_sql_fund_relational_select`
- Public copy present: yes | step titles: Spreading long data into a wide grid with pivot_table(); Building a pivot table from long data; Controlling how duplicate cells are combined with aggfunc; Changing the pivot aggregation function; Build a pivot table from the long deliveries data; Writing a DataFrame to a CSV file with to_csv(); Controlling the index column in CSV output; Write a DataFrame to CSV with and without the index; Pivot tables and CSV export — key takeaways

## Region: SQL Fundamentals (`region_sql_fundamentals`)
Write correct SQL queries against a PostgreSQL database: filtering, sorting, aggregating, and formatting results with SELECT statements.

### Terrain: Querying and Filtering Data (`terrain_sql_fundamentals_querying_filtering`)
Retrieve rows from a single table, filter them with conditions, and control how results are sorted and limited.

#### 28. The Relational Model and SELECT Basics  (`tile_sql_fund_relational_select`)
Learn how relational databases organise data into named tables of rows and columns, then write your first SELECT statements to pull specific columns from the QuickDeliver dataset.

- Concepts: `sql.relational_model`, `sql.select_fundamentals`
- Built in: `final_batch_005_da_sql_canary` | content_hash `cd36de324bac…` | steps 10 (4 explainer, 2 check, 2 hands_on, 1 video, 1 recap) | remediation steps 4
- Interactions: 2 choice, 1 table_select, 1 code_exercise | runtimes: sql | packs: core, data
- Blocks used: code_walkthrough, data_table, media_group, prose, up_next
- Assets: ds.customers | est. minutes: ? | completion reward: {'gems': 25} | next tile: `tile_sql_fund_alias_distinct`
- Public copy present: yes | step titles: Tables, rows and columns; What makes a table well-formed; Is this table well-formed?; Identify rows and columns in the customers table; SELECT, FROM and AS; SELECT and FROM picking just the columns you need; Using * to select all columns; Write a SELECT for listed columns; Rename a column with AS; What you've learned

#### 29. Aliasing and DISTINCT  (`tile_sql_fund_alias_distinct`)
Give tables and columns short temporary names with AS, qualify column references with a table alias, and use SELECT DISTINCT to list each unique value exactly once.

- Concepts: `sql.aliasing`, `sql.distinct`
- Built in: `final_batch_005_da_sql_canary` | content_hash `0bd4f9cb0fdd…` | steps 8 (3 explainer, 2 check, 2 hands_on, 1 recap) | remediation steps 4
- Interactions: 2 choice, 2 code_exercise | runtimes: sql | packs: core, data
- Blocks used: before_after, code_walkthrough, data_table, prose, up_next
- Assets: ds.customers, ds.orders | est. minutes: ? | completion reward: {'gems': 24} | next tile: `tile_sql_fund_filtering_rows`
- Public copy present: yes | step titles: Giving a table a short name; Column aliases and qualified references; Qualify and alias columns correctly; Alias the orders table and qualify its columns; Removing duplicate rows with DISTINCT; Predict rows with and without DISTINCT; List each distinct city exactly once; What you've learned

#### 30. Filtering Rows with WHERE and Logical Operators  (`tile_sql_fund_filtering_rows`)
Learn to filter query results with WHERE, combine conditions using AND, OR, and NOT, control evaluation order with parentheses, and test for missing values with IS NULL.

- Concepts: `sql.where_filtering`, `sql.logical_operators`, `sql.null_handling`
- Built in: `final_batch_006_da_sql_rest` | content_hash `cb3b86771eb5…` | steps 14 (4 explainer, 5 check, 3 hands_on, 1 video, 1 recap) | remediation steps 8
- Interactions: 5 choice, 3 code_exercise | runtimes: sql | packs: core, data
- Blocks used: before_after, data_table, media_group, prose, side_by_side, up_next
- Assets: ds_orders | est. minutes: ? | completion reward: {'gems': 80} | next tile: `tile_sql_fund_sorting_limiting`
- Public copy present: yes | step titles: Filtering rows with WHERE; Pick the right comparison operator; Write a WHERE clause for a requirement; Write a WHERE filter in SQL; Combining conditions with AND, OR, and NOT; Evaluation order and parentheses; Predict the result of unparenthesized conditions; Use parentheses to force evaluation order; Combine conditions with AND, OR, and parentheses; Testing for missing values with IS NULL; Testing for missing values (video); Why does = NULL never match?; Write IS NULL and IS NOT NULL filters; Recap: Filtering Rows

#### 31. Sorting and Limiting Results  (`tile_sql_fund_sorting_limiting`)


- Concepts: `sql.order_by`, `sql.limit_offset`
- Built in: `final_batch_006_da_sql_rest` | content_hash `3fc776bd7c98…` | steps 7 (2 explainer, 2 check, 2 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 2 code_exercise | runtimes: sql | packs: core, data
- Blocks used: before_after, data_table, process_flow, prose, up_next
- Assets: ds_orders | est. minutes: ? | completion reward: {'gems': 45} | next tile: `tile_sql_fund_aggregating_data`
- Public copy present: yes | step titles: Controlling the order of your results with ORDER BY; Using a second column as a tiebreaker; Sort orders by region, then by delivery time descending; Returning a slice of rows with LIMIT and OFFSET; Predicting rows returned with LIMIT and OFFSET; Return the top 5 orders by amount; Sorting and limiting results

### Terrain: Aggregating and Styling Queries (`terrain_sql_fundamentals_aggregating_styling`)
Summarize rows into groups and write queries that follow shared style conventions.

#### 32. Aggregating Data with GROUP BY  (`tile_sql_fund_aggregating_data`)


- Concepts: `sql.aggregate_functions`, `sql.group_by`, `sql.having`
- Built in: `final_batch_006_da_sql_rest` | content_hash `06f87a3064ac…` | steps 14 (3 explainer, 3 video, 4 check, 3 hands_on, 1 recap) | remediation steps 4
- Interactions: 4 choice, 3 code_exercise | runtimes: sql | packs: core, data
- Blocks used: before_after, data_table, diagram, media_group, process_flow, prose, up_next
- Assets: ds_orders | est. minutes: ? | completion reward: {'gems': 85} | next tile: `tile_sql_case_expressions`
- Public copy present: yes | step titles: Collapsing many rows into one number with aggregate functions; COUNT, SUM, AVG, MIN and MAX in action; COUNT(*) versus COUNT(column); Choosing the right aggregate for a question; Compute the total and average order value; Splitting rows into groups with GROUP BY; GROUP BY: rows collapsing into one per group; Diagnosing an ungrouped column error; Count orders per region; Filtering aggregated groups with HAVING; HAVING: filtering groups after aggregation; Writing HAVING on an aggregate expression; Keep only regions with total amount above a threshold; Aggregating data with GROUP BY

#### 33. CASE Expressions for Conditional Logic  (`tile_sql_case_expressions`)


- Concepts: `sql.case_expressions`
- Built in: `final_batch_006_da_sql_rest` | content_hash `0f223148fea7…` | steps 6 (2 explainer, 2 check, 1 hands_on, 1 recap) | remediation steps 3
- Interactions: 2 choice, 1 code_exercise | runtimes: sql | packs: core
- Blocks used: code_walkthrough, prose, up_next
- Assets: ds_orders | est. minutes: ? | completion reward: {'gems': 35} | next tile: `tile_sql_style_conventions`
- Public copy present: yes | step titles: Labelling rows with CASE WHEN … THEN … END; What happens when no WHEN matches — and the simple CASE form; Writing CASE with ordered WHEN branches; Recognising the simple CASE form; Label each order as small, medium or large; Conditional logic with CASE expressions

#### 34. SQL Style Conventions  (`tile_sql_style_conventions`)
Format SQL queries consistently: uppercase keywords, lowercase columns, meaningful aliases with AS, right-aligned keyword 'river', and one clause per line.

- Concepts: `sql.style_conventions`
- Built in: `final_batch_006_da_sql_rest` | content_hash `75cfc27c1fcd…` | steps 4 (1 explainer, 1 check, 1 hands_on, 1 recap) | remediation steps 3
- Interactions: 1 choice, 1 code_exercise | runtimes: sql | packs: core
- Blocks used: before_after, code_walkthrough, prose, up_next
- Assets: ds_orders | est. minutes: ? | completion reward: {'gems': 25} | next tile: `tile_sql_text_dates_casts`
- Public copy present: yes | step titles: SQL style conventions; Line breaks and the keyword 'river'; Reformat a query to follow the style guide; Recap: SQL Style Conventions

### Terrain: Transforming Values in SQL (`terrain_sql_transforming_values`)
Clean and combine values directly inside queries.

#### 35. Text and Date Functions  (`tile_sql_text_dates_casts`)
Clean and transform text with LOWER, UPPER, TRIM, CONCAT, and LENGTH; extract date parts with EXTRACT and compute elapsed days; convert types with CAST and :: syntax.

- Concepts: `sql.string_functions`, `sql.date_time_functions`, `sql.type_casting`
- Built in: `final_batch_006_da_sql_rest` | content_hash `23612229b41a…` | steps 10 (3 explainer, 3 check, 3 hands_on, 1 recap) | remediation steps 6
- Interactions: 3 choice, 3 code_exercise | runtimes: sql | packs: core, data
- Blocks used: before_after, code_walkthrough, data_table, prose, side_by_side, up_next
- Assets: ds_customers, ds_orders | est. minutes: ? | completion reward: {'gems': 65} | next tile: `tile_sql_null_fallback_and_union`
- Public copy present: yes | step titles: Cleaning text with LOWER, UPPER, TRIM, CONCAT, and LENGTH; LOWER and UPPER: which function to use; Trim, concat, and measure customer city names; Extracting date parts and computing elapsed days; Days between two dates; Extract order month and compute days since order; Type casting: CAST and :: syntax; Will this cast succeed?; Write a cast in both syntaxes; Recap: Text, Dates, and Casts

#### 36. NULL Fallbacks and UNION  (`tile_sql_null_fallback_and_union`)
Replace missing values with a default using COALESCE, and combine the results of two compatible queries into one list using UNION or UNION ALL.

- Concepts: `sql.coalesce`, `sql.union`
- Built in: `final_batch_006_da_sql_rest` | content_hash `a9efefea7643…` | steps 9 (3 explainer, 3 check, 2 hands_on, 1 recap) | remediation steps 4
- Interactions: 3 choice, 2 code_exercise | runtimes: sql | packs: core, data
- Blocks used: before_after, data_table, diagram, prose, up_next
- Assets: ds_customers, ds_orders | est. minutes: ? | completion reward: {'gems': 53} | next tile: `tile_datamodel_entities_keys`
- Public copy present: yes | step titles: Replacing NULL with a default using COALESCE; What does COALESCE return?; Substituting a default for NULL; Replace missing city values with COALESCE; Stacking query results with UNION and UNION ALL; UNION compatibility: matching columns and types; Are these two queries compatible for UNION?; Stack two queries with UNION and UNION ALL; Recap: NULL Fallbacks and UNION

## Region: Relational Data Modeling (`region_relational_data_modeling`)
Understand how tables relate through keys, normalization, and dimensional (fact/dimension) design, and how to read an ER diagram.

### Terrain: Data Modeling Fundamentals (`terrain_datamodel_fundamentals`)
Model entities, keys, relationships, and dimensional shape well enough to query and design correctly.

#### 37. Entities, Tables, and Primary Keys  (`tile_datamodel_entities_keys`)
Recognise that a table models one kind of real-world thing, identify entities and their attributes in a business scenario, and select a valid primary key that is unique and never null.

- Concepts: `datamodel.entities_tables`, `datamodel.primary_keys`
- Built in: `final_batch_003_da_chunk` | content_hash `a3691ed7233e…` | steps 7 (2 explainer, 2 check, 2 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 1 classify, 1 table_select | runtimes: none | packs: core, data
- Blocks used: data_table, diagram, prose, up_next
- Assets: ds_customers, ds_customers_pk_candidates, ds_orders, ds_products | est. minutes: ? | completion reward: {'gems': 45} | next tile: `tile_datamodel_foreign_keys_one_to_many`
- Public copy present: yes | step titles: Every Table Represents One Real Thing; Attributes of an Entity; Identify Entities in the QuickShip Scenario; Picking the Column That Uniquely Identifies Every Row; Entity Integrity; Select the Valid Primary Key; What You've Learned

#### 38. Foreign Keys and One-to-Many Relationships  (`tile_datamodel_foreign_keys_one_to_many`)
Understand how a foreign key links a child table to a parent table, what referential integrity prevents, and how to identify the one side and the many side of a 1:M relationship.

- Concepts: `datamodel.foreign_keys_referential_integrity`, `datamodel.one_to_many`
- Built in: `final_batch_003_da_chunk` | content_hash `e6aa5fff9700…` | steps 9 (2 explainer, 2 video, 2 check, 2 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 2 table_select | runtimes: none | packs: core, data
- Blocks used: diagram, media_group, prose, up_next
- Assets: ds_orders | est. minutes: ? | completion reward: {'gems': 51} | next tile: `tile_datamodel_normalization_many_to_many`
- Public copy present: yes | step titles: Linking Orders Back to the Right Customer; Foreign Keys Build the Parent-Child Link; What Breaks Referential Integrity?; Find the Foreign Key and the Orphan; One Customer, Many Orders; Telling One-to-Many from One-to-One; Where Does the Foreign Key Go?; Identify the One Side and the Many Side; What You've Learned

#### 39. Normalization and Many-to-Many Relationships  (`tile_datamodel_normalization_many_to_many`)
Learn why repeating data in a single table causes update anomalies, how splitting tables into separate entities removes that redundancy, and how a junction table resolves a many-to-many relationship into two ordinary one-to-many links.

- Concepts: `datamodel.normalization_basics`, `datamodel.many_to_many_junction_tables`
- Built in: `final_batch_003_da_chunk` | content_hash `d647a05474d4…` | steps 10 (4 explainer, 2 check, 2 hands_on, 1 video, 1 recap) | remediation steps 2
- Interactions: 2 choice, 1 find_issues, 1 table_select | runtimes: none | packs: core, data
- Blocks used: data_table, diagram, media_group, prose, side_by_side, up_next
- Assets: ds_customers, ds_order_items | est. minutes: ? | completion reward: {'gems': 85} | next tile: `tile_datamodel_dimensional_er`
- Public copy present: yes | step titles: One big table — and its hidden cost; Update anomalies and the fix; Splitting a table to remove redundancy; Find the redundancy and redesign the table; When both sides can have many — the junction table; What goes inside the junction table; Resolving many-to-many with a junction table; Designing the junction table's keys; Design a junction table for students and courses; What you've learned

#### 40. Reading ER Diagrams  (`tile_datamodel_dimensional_er`)
Learn to read an entity-relationship diagram: boxes for entity types, ovals for attributes with underlined primary keys, and marked relationship lines showing cardinality and connectivity.

- Concepts: `datamodel.er_diagram_reading`
- Built in: `final_batch_003_da_chunk` | content_hash `109b53122272…` | steps 5 (1 explainer, 1 video, 1 check, 1 hands_on, 1 recap) | remediation steps 1
- Interactions: 1 choice, 1 classify | runtimes: none | packs: core
- Blocks used: diagram, media_group, prose, up_next
- Assets: none | est. minutes: ? | completion reward: {'gems': 45} | next tile: `tile_sql_adv_joining_tables`
- Public copy present: yes | step titles: Boxes, ovals, and relationship lines; Reading an ER diagram; Reading cardinality markings; Classify ERD elements and read relationships; What you've learned

## Region: SQL Joins and Advanced Querying (`region_sql_joins_advanced`)
Combine data across tables with joins, see how a query actually executes, and use subqueries, CTEs, and window functions.

### Terrain: Joins, Subqueries, and Advanced SQL (`terrain_sql_joins_subqueries_advanced`)
Bring multiple tables together and layer queries on top of each other for more advanced analysis.

#### 41. Joining Tables  (`tile_sql_adv_joining_tables`)


- Concepts: `sql.inner_join`, `sql.composite_join_conditions`, `sql.outer_joins`
- Built in: `final_batch_006_da_sql_rest` | content_hash `38dc2d8ed352…` | steps 16 (5 explainer, 2 video, 5 check, 3 hands_on, 1 recap) | remediation steps 3
- Interactions: 5 choice, 3 code_exercise | runtimes: sql | packs: core
- Blocks used: code_walkthrough, diagram, media_group, prose, up_next
- Assets: ds_customers, ds_order_items, ds_orders, ds_shipments | est. minutes: ? | completion reward: {'gems': 31} | next tile: `tile_sql_adv_execution_order_subquery_where`
- Public copy present: yes | step titles: Combining two tables on a shared key; INNER JOIN in action; Unmatched rows disappear; Which rows survive an INNER JOIN?; Write the JOIN condition; Joining on two columns at once; Extend ON with AND; Rewrite with USING; Join order_items to shipments on two keys; Keeping unmatched rows with LEFT JOIN; RIGHT, FULL, and the optional OUTER keyword; LEFT, RIGHT and FULL joins; LEFT JOIN and choosing RIGHT or FULL; Is OUTER required?; Write a LEFT JOIN to keep all customers; Joins: what you've learned

#### 42. Query Execution Order and Subqueries in WHERE  (`tile_sql_adv_execution_order_subquery_where`)


- Concepts: `sql.clause_execution_order`, `sql.subquery_in_where`
- Built in: `final_batch_006_da_sql_rest` | content_hash `e7b38005c614…` | steps 10 (3 explainer, 2 video, 2 check, 2 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 2 code_exercise | runtimes: sql | packs: core
- Blocks used: code_walkthrough, media_group, process_flow, prose, up_next
- Assets: ds_customers, ds_orders | est. minutes: ? | completion reward: {'gems': 23} | next tile: `tile_sql_adv_subquery_from_cte`
- Public copy present: yes | step titles: SQL clauses run in a different order than you write them; Tracing the processing order; Where an alias can — and cannot — be used; Trace the clause processing order; Fix the alias placement; Using a query result as a filter value; Subqueries inside WHERE; Write a scalar subquery comparison; Filter with IN and a scalar subquery; Execution order and WHERE subqueries

#### 43. Subqueries in FROM and Common Table Expressions  (`tile_sql_adv_subquery_from_cte`)


- Concepts: `sql.subquery_in_from`, `sql.cte`
- Built in: `final_batch_006_da_sql_rest` | content_hash `109689bd94a7…` | steps 10 (3 explainer, 2 video, 2 check, 2 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 2 code_exercise | runtimes: sql | packs: core
- Blocks used: code_walkthrough, media_group, prose, up_next
- Assets: ds_orders | est. minutes: ? | completion reward: {'gems': 23} | next tile: `tile_spreadsheet_grid_references`
- Public copy present: yes | step titles: Treating a query result as a table; Inner column names become the virtual table's columns; Subqueries in FROM; Use inner output columns in the outer query; Write a FROM subquery with an alias; Naming a query once with WITH; WITH: naming a query once, then reading it like a table; Rewrite a nested subquery as a CTE; Write a WITH clause; Subqueries in FROM and CTEs

## Region: Spreadsheet Analysis (`region_spreadsheet_analysis`)
Analyze tabular data directly in a spreadsheet using structured ranges, formulas, lookups, pivot tables, and charts, without writing code.

### Terrain: Spreadsheet Basics and Data Organization (`terrain_spreadsheet_basics_organization`)
Work with the spreadsheet grid, structure ranges as tables, and sort, filter, and clean data.

#### 44. The Spreadsheet Grid and Cell References  (`tile_spreadsheet_grid_references`)
Introduces the spreadsheet grid model (cells, rows, columns, sheets) and A1 cell references and ranges, using the QuickDeliver orders workbook as context.

- Concepts: `spreadsheet.grid_model`, `spreadsheet.cell_references_ranges`
- Built in: `final_batch_011_da_spreadsheet` | content_hash `ae94be0931aa…` | steps 9 (4 explainer, 2 check, 2 hands_on, 1 recap) | remediation steps 4
- Interactions: 2 choice, 2 formula_entry | runtimes: none | packs: core, data
- Blocks used: diagram, prose, spreadsheet_grid, up_next
- Assets: asset_orders_clean | est. minutes: ? | completion reward: {'gems': 55} | next tile: `tile_spreadsheet_tables_named_ranges`
- Public copy present: yes | step titles: Every cell has an address; One workbook, many sheets; Cell address vs. cell contents; Navigate the QuickDeliver workbook; Pointing at one cell or many; Referencing an entire row or column; Whole-row and whole-column references; Write range references for the Orders sheet; The grid, addresses, and ranges

#### 45. Structured Tables and Named Ranges  (`tile_spreadsheet_tables_named_ranges`)
Convert a data range into an Excel table with structured references, and name ranges for readable formulas.

- Concepts: `spreadsheet.structured_tables`, `spreadsheet.named_ranges`
- Built in: `final_batch_011_da_spreadsheet` | content_hash `db87d7c06f0c…` | steps 9 (3 explainer, 1 video, 2 check, 2 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 2 formula_entry | runtimes: none | packs: core, data
- Blocks used: before_after, diagram, media_group, prose, spreadsheet_grid, up_next
- Assets: asset_orders_clean | est. minutes: ? | completion reward: {'gems': 51} | next tile: `tile_spreadsheet_sorting_filtering`
- Public copy present: yes | step titles: From Plain Range to Structured Table; Auto-Expansion and Structured References in Action; Tables Grow With Your Data; Table Auto-Expansion; Create a Table and Confirm Auto-Expansion; Naming a Range for Readable Formulas; Replacing a Cell Reference with a Named Range; Define a Named Range and Use It in a Formula; Structured Tables and Named Ranges — Key Points

#### 46. Sorting and Filtering Data  (`tile_spreadsheet_sorting_filtering`)
Reorder your Orders sheet by one or more columns, and use AutoFilter to show only the rows that meet your criteria.

- Concepts: `spreadsheet.sorting`, `spreadsheet.filtering`
- Built in: `final_batch_011_da_spreadsheet` | content_hash `8c7031d05fe1…` | steps 10 (3 explainer, 2 video, 2 check, 2 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 2 formula_entry | runtimes: none | packs: core, data
- Blocks used: before_after, diagram, media_group, prose, spreadsheet_grid, up_next
- Assets: asset_orders_clean | est. minutes: ? | completion reward: {'gems': 50} | next tile: `tile_spreadsheet_formatting_validation`
- Public copy present: yes | step titles: Putting Your Orders in Order; Single-Column Sort and Multi-Level Sort Dialog; A Two-Level Sort in Practice; Multi-Level Sort with Independent Directions; Sort the Orders Sheet; Showing Only the Rows You Need; AutoFilter: Hiding Rows, Stacking Filters, and Clearing; Applying AutoFilter Criteria; Filter the Orders Sheet; Sorting and Filtering — Key Points

#### 47. Conditional Formatting and Data Validation  (`tile_spreadsheet_formatting_validation`)
Apply automatic cell formatting based on value rules, and restrict what users can enter into a cell.

- Concepts: `spreadsheet.conditional_formatting`, `spreadsheet.data_validation`
- Built in: `final_batch_011_da_spreadsheet` | content_hash `b8eeb7b6e8d7…` | steps 11 (3 explainer, 2 video, 3 check, 2 hands_on, 1 recap) | remediation steps 3
- Interactions: 3 choice, 2 formula_entry | runtimes: none | packs: core, data
- Blocks used: before_after, diagram, media_group, prose, spreadsheet_grid, up_next
- Assets: asset_orders_clean | est. minutes: ? | completion reward: {'gems': 59} | next tile: `tile_spreadsheet_cleaning_cross_sheet`
- Public copy present: yes | step titles: Highlighting Cells Automatically by Value; Applying a Conditional Formatting Rule via Highlight Cells Rules; Applying a Conditional Formatting Rule; Apply a Conditional Formatting Rule; Restricting What Users Can Enter; Numeric, Date, and Text-Length Validation; Restricting Cell Input: Error Alerts and Numeric Rules; Data Validation Purpose and Numeric Rules; Choosing the Right Validation Type; Add a Dropdown Validation Rule to the Status Column; Conditional Formatting and Data Validation — Key Points

#### 48. Removing Duplicates and Splitting Text  (`tile_spreadsheet_cleaning_cross_sheet`)
Clean your Orders data by removing duplicate rows, split combined text into separate columns, and write formulas that reference cells on other sheets.

- Concepts: `spreadsheet.remove_duplicates_cleaning`, `spreadsheet.text_to_columns_split`, `spreadsheet.cross_sheet_references`
- Built in: `final_batch_011_da_spreadsheet` | content_hash `ec5bf2aa89d6…` | steps 13 (3 explainer, 2 video, 4 check, 3 hands_on, 1 recap) | remediation steps 4
- Interactions: 4 choice, 2 formula_entry, 1 code_exercise | runtimes: spreadsheet | packs: core, data
- Blocks used: before_after, diagram, media_group, prose, spreadsheet_grid, up_next
- Assets: asset_drivers_vlookup, asset_orders_clean, asset_orders_location_combined | est. minutes: ? | completion reward: {'gems': 70} | next tile: `tile_spreadsheet_formula_syntax_refs`
- Public copy present: yes | step titles: Removing Duplicate Rows Permanently; Remove Duplicates in Action; Permanent Deletion and the Copy Precaution; Configure and Run Remove Duplicates; Splitting One Column into Two; Text to Columns Wizard Step by Step; Split a Delimited Column; Split the Full Name Column; Referencing Cells on Another Sheet; Same-Workbook and Cross-Workbook References; Choosing the Right Reference Syntax; Write a Cross-Sheet Reference; Cleaning, Splitting, and Linking — Key Points

### Terrain: Formulas and Functions (`terrain_spreadsheet_formulas_functions`)
Write formulas, use relative and absolute references, and apply built-in functions to aggregate, evaluate, and look up data.

#### 49. Writing Formulas and Reference Types  (`tile_spreadsheet_formula_syntax_refs`)


- Concepts: `spreadsheet.formula_syntax`, `spreadsheet.relative_absolute_references`
- Built in: `final_batch_011_da_spreadsheet` | content_hash `124d8a4f81c4…` | steps 12 (4 explainer, 2 video, 3 check, 2 hands_on, 1 recap) | remediation steps 3
- Interactions: 3 choice, 2 code_exercise | runtimes: spreadsheet | packs: core, data
- Blocks used: before_after, media_group, prose, spreadsheet_grid, up_next
- Assets: asset_orders_clean | est. minutes: ? | completion reward: {'gems': 56} | next tile: `tile_spreadsheet_aggregation_logical`
- Public copy present: yes | step titles: Every Formula Starts with =; Formulas in Action; Operator Precedence and Parentheses; The Required Formula Prefix; Writing a Function Formula; Write Formulas on the Orders Sheet; Relative and Absolute References; Watching References Shift (or Stay Fixed); Mixed References: Lock One Dimension; Constructing a Mixed Reference; Apply Reference Types to the Orders Sheet; Formulas and Reference Types — Key Takeaways

#### 50. Aggregation and Logical Functions  (`tile_spreadsheet_aggregation_logical`)


- Concepts: `spreadsheet.aggregation_functions`, `spreadsheet.logical_functions`
- Built in: `final_batch_011_da_spreadsheet` | content_hash `d6711adfa212…` | steps 11 (4 explainer, 2 video, 2 check, 2 hands_on, 1 recap) | remediation steps 3
- Interactions: 2 choice, 1 formula_entry, 1 code_exercise | runtimes: spreadsheet | packs: core, data
- Blocks used: media_group, prose, side_by_side, spreadsheet_grid, up_next
- Assets: asset_orders_clean | est. minutes: ? | completion reward: {'gems': 50} | next tile: `tile_spreadsheet_text_date_conditional_agg`
- Public copy present: yes | step titles: SUM, AVERAGE, COUNT, and COUNTA; Aggregation Functions in Action; COUNT vs COUNTA: What Gets Counted; Choosing the Right Aggregation Function; Summarise the Orders Sheet; IF, Nested IF, AND, and OR; Logical Functions in Action; AND and OR: Testing Multiple Conditions; Reading an IF Formula; AND vs OR; Aggregation and Logical Functions — Key Takeaways

#### 51. Text, Date, and Conditional Aggregation  (`tile_spreadsheet_text_date_conditional_agg`)


- Concepts: `spreadsheet.text_combining`, `spreadsheet.text_extraction`, `spreadsheet.date_functions`, `spreadsheet.conditional_aggregation`
- Built in: `final_batch_011_da_spreadsheet` | content_hash `c6604ae6b46a…` | steps 18 (6 explainer, 6 check, 4 hands_on, 1 video, 1 recap) | remediation steps 5
- Interactions: 6 choice, 3 formula_entry, 1 code_exercise | runtimes: spreadsheet | packs: core, data
- Blocks used: before_after, media_group, prose, spreadsheet_grid, up_next
- Assets: asset_orders_clean | est. minutes: ? | completion reward: {'gems': 105} | next tile: `tile_spreadsheet_lookups_troubleshooting`
- Public copy present: yes | step titles: Combining Text with TEXTJOIN and CONCATENATE; CONCATENATE Syntax and Deprecation; Combine Text Columns on the Orders Sheet; Extracting Text with LEFT, RIGHT, MID, and TRIM; MID and TRIM; Choosing the Right Extraction Function; Extract Characters from Order IDs; TODAY, DATEDIF, and the Date Serial Number; Choosing the Right Date Function; Calculate Days Since Each Order Was Placed; COUNTIF and SUMIF: One Condition; COUNTIFS and SUMIFS: Multiple Conditions; Building Conditional Aggregation Formulas; Criteria Syntax and the Between Pattern; Single vs Multi-Condition Aggregation; The Between Pattern; Write Conditional Aggregation Formulas; Text, Date, and Conditional Aggregation — Key Takeaways

#### 52. VLOOKUP/XLOOKUP and INDEX/MATCH  (`tile_spreadsheet_lookups_troubleshooting`)
Look up values across sheets with VLOOKUP, XLOOKUP, and INDEX/MATCH, and diagnose the three most common formula error codes.

- Concepts: `spreadsheet.vlookup_xlookup`, `spreadsheet.index_match`, `spreadsheet.formula_error_troubleshooting`
- Built in: `final_batch_011_da_spreadsheet` | content_hash `a13829218ba6…` | steps 17 (6 explainer, 3 video, 4 check, 3 hands_on, 1 recap) | remediation steps 4
- Interactions: 4 choice, 3 code_exercise | runtimes: spreadsheet | packs: core, data
- Blocks used: media_group, prose, spreadsheet_grid, up_next
- Assets: asset_drivers_index_match, asset_drivers_vlookup, asset_orders_clean | est. minutes: ? | completion reward: {'gems': 85} | next tile: `tile_spreadsheet_pivot_tables`
- Public copy present: yes | step titles: Finding a Driver Name from an Order Row; VLOOKUP and XLOOKUP in Action; HLOOKUP and XLOOKUP; HLOOKUP: Row Index; Write VLOOKUP and XLOOKUP Formulas; When the Key Column Is Not on the Left; INDEX and MATCH Working Together; Combining INDEX and MATCH; Write an INDEX/MATCH Formula; Build an INDEX/MATCH Lookup; Reading #N/A and #REF! Error Codes; The #VALUE! Error and SUM vs. Arithmetic; Seeing Formula Errors Appear and Propagate; Diagnosing #VALUE! Errors; #VALUE! Propagation Through SUM or AVERAGE; Diagnose Formula Errors; Lookups and Error Codes — Key Points

### Terrain: Pivot Tables and Charts (`terrain_spreadsheet_pivots_charts`)
Summarize data with pivot tables and visualize it with basic chart types.

#### 53. Pivot Tables  (`tile_spreadsheet_pivot_tables`)
Build a PivotTable to summarise Orders data by city and status, then change the value-field summary function.

- Concepts: `spreadsheet.pivot_tables`, `spreadsheet.pivot_summarization`
- Built in: `final_batch_011_da_spreadsheet` | content_hash `3242a3ce41c4…` | steps 11 (3 explainer, 2 video, 3 check, 2 hands_on, 1 recap) | remediation steps 3
- Interactions: 3 choice, 2 formula_entry | runtimes: none | packs: core, data
- Blocks used: before_after, data_table, diagram, media_group, prose, up_next
- Assets: asset_orders_clean | est. minutes: ? | completion reward: {'gems': 59} | next tile: `tile_spreadsheet_chart_types`
- Public copy present: yes | step titles: What a PivotTable Does and How to Build One; Building a PivotTable: Fields, Areas, and Layout; What Each PivotTable Area Displays; Creating a PivotTable and Reading Its Areas; Building a PivotTable to Answer a Question; Build a PivotTable from the Orders Data; Changing How Values Are Summarised; Changing a PivotTable's Value-Field Summary Function; Default Summarisation by Data Type; Switch the Summary Function to Average; Pivot Tables — Key Points

#### 54. Chart Types  (`tile_spreadsheet_chart_types`)
Build bar, line, and pie charts from Orders data to visualise comparisons, trends, and part-of-whole shares.

- Concepts: `spreadsheet.bar_chart_creation`, `spreadsheet.line_chart_creation`, `spreadsheet.pie_chart_creation`
- Built in: `final_batch_011_da_spreadsheet` | content_hash `a89683314ee5…` | steps 14 (3 explainer, 3 video, 4 check, 3 hands_on, 1 recap) | remediation steps 3
- Interactions: 4 choice, 3 formula_entry | runtimes: none | packs: core, data
- Blocks used: chart, data_table, media_group, prose, up_next
- Assets: asset_city_totals, asset_monthly_summary | est. minutes: ? | completion reward: {'gems': 79} | next tile: `tile_viz_figures_layout_plotting`
- Public copy present: yes | step titles: Bar Charts: Comparing Categories; Building a Bar Chart in Excel; Building a Bar Chart from Category Data; Build a Bar Chart from City Totals; Line Charts: Showing Trends Over Time; Building a Line Chart from Monthly Sales Data; Axis Roles and Interval Suitability; Building a Line Chart from Time-Ordered Data; Build a Line Chart from Monthly Totals; Pie Charts: Part-of-Whole Shares; When a Pie Chart Works: Proportional Slices; Building a Pie Chart from Category Totals; Build a Pie Chart from City Totals; Chart Types — Key Points

## Region: Data Visualization (`region_data_visualization`)
Build static charts with matplotlib and seaborn, choosing chart types that match the analytical question.

### Terrain: matplotlib Fundamentals (`terrain_viz_matplotlib_fundamentals`)
Build figures and the core single-plot chart types with matplotlib's pyplot interface.

#### 55. Figures, Layout, and Basic Plotting  (`tile_viz_figures_layout_plotting`)
Learn matplotlib's Figure/Axes object model, how to set figure size and call tight_layout, and how to use plt.plot() in both its one-argument and two-argument forms.

- Concepts: `viz.matplotlib_figure_axes`, `viz.figure_size_layout`, `viz.pyplot_basic_plotting`
- Built in: `final_batch_012_da_viz` | content_hash `27bcd918a3e9…` | steps 13 (4 explainer, 2 video, 3 check, 3 hands_on, 1 recap) | remediation steps 3
- Interactions: 3 choice, 3 code_exercise | runtimes: chart_renderer | packs: core
- Blocks used: code_walkthrough, diagram, media_group, prose, side_by_side, up_next
- Assets: none | est. minutes: ? | completion reward: {'gems': 115} | next tile: `tile_viz_bar_histograms`
- Public copy present: yes | step titles: The Figure and the Axes; Figure and Axes: the container relationship in code; Plotting onto the Axes; Figure or Axes?; Create a Figure and Plot on Its Axes; Setting Figure Size and Fitting the Layout; Fitting the Layout; Custom Figure Size and Tight Layout; Two Ways to Call plt.plot(); Two ways to call plt.plot(): supplying x and y vs. y alone; One Argument or Two?; Plot Delivery Times with plt.plot(); What You've Learned

#### 56. Bar Charts and Histograms  (`tile_viz_bar_histograms`)
Learn to compare categories with plt.bar() and reveal distributions with plt.hist(), understanding the zero-baseline rule and the bins parameter.

- Concepts: `viz.bar_charts`, `viz.histograms`
- Built in: `final_batch_012_da_viz` | content_hash `f664b60f9059…` | steps 12 (3 explainer, 2 video, 4 check, 2 hands_on, 1 recap) | remediation steps 4
- Interactions: 4 choice, 2 code_exercise | runtimes: chart_renderer | packs: core
- Blocks used: before_after, code_walkthrough, media_group, prose, up_next
- Assets: ds.orders | est. minutes: ? | completion reward: {'gems': 105} | next tile: `tile_viz_line_scatter_box`
- Public copy present: yes | step titles: Comparing Cities with a Bar Chart; Bar Charts: Live Code and the Zero-Baseline Rule; Why the Baseline Must Start at Zero; When to Use a Bar Chart; The Zero-Baseline Rule; Plot City Averages with plt.bar(); Seeing the Distribution with a Histogram; Histograms: Binning and Distribution Shape; How plt.hist() Works; Controlling Bin Count; Plot a Delivery-Time Histogram; Bar Charts and Histograms: What You Learned

#### 57. Line Plots, Scatter Plots, and Box Plots  (`tile_viz_line_scatter_box`)
Plot trends over time with plt.plot(), relationships between two numeric variables with plt.scatter(), and per-group distributions with plt.boxplot().

- Concepts: `viz.line_plots`, `viz.scatter_plots`, `viz.box_plots`
- Built in: `final_batch_012_da_viz` | content_hash `1067b5dee0e9…` | steps 16 (5 explainer, 3 video, 4 check, 3 hands_on, 1 recap) | remediation steps 4
- Interactions: 4 choice, 3 code_exercise | runtimes: chart_renderer | packs: core, data
- Blocks used: chart, diagram, media_group, prose, up_next
- Assets: ds.daily_averages, ds.orders | est. minutes: ? | completion reward: {'gems': 135} | next tile: `tile_viz_labeling_chart_selection`
- Public copy present: yes | step titles: Tracking Trends Over Time with a Line Plot; Line Plots: Connecting Points to Reveal Trends; What the Connecting Line Adds; Plot Lagos Delivery Trends with plt.plot(); Exploring Relationships with a Scatter Plot; Scatter Plots: One Point per Pair; Scatter Plot Basics; Plot Distance vs Delivery Time; Reading a Box Plot; The Box, Whiskers, and Flier Points; Box Plots: Distribution and Outliers; Comparing Multiple Cities Side by Side; Box Plot Anatomy; When to Use a Box Plot; Compare City Delivery Spreads with plt.boxplot(); Line, Scatter, and Box Plots: What You Learned

#### 58. Labeling and Chart Selection  (`tile_viz_labeling_chart_selection`)


- Concepts: `viz.labeling_annotation`, `viz.chart_type_selection`
- Built in: `final_batch_012_da_viz` | content_hash `83534f21d57e…` | steps 11 (3 explainer, 4 check, 2 hands_on, 1 video, 1 recap) | remediation steps 2
- Interactions: 4 choice, 2 code_exercise | runtimes: chart_renderer | packs: core, data
- Blocks used: before_after, chart, code_walkthrough, media_group, prose, side_by_side, up_next
- Assets: ds.daily_averages, ds.orders | est. minutes: ? | completion reward: {'gems': 55} | next tile: `tile_viz_seaborn_stats_themes`
- Public copy present: yes | step titles: Making charts readable with labels; pyplot shortcut functions; Check your understanding; Check your understanding; Practice; Choosing the right chart for your question; Video walkthrough; Check your understanding; Check your understanding; Practice; What you learned

### Terrain: Seaborn and Advanced Styling (`terrain_viz_seaborn_styling`)
Plot directly from DataFrames with seaborn, then extend a figure's styling and layout.

#### 59. seaborn for Statistical Visualization  (`tile_viz_seaborn_stats_themes`)


- Concepts: `viz.seaborn_dataframe_plotting`, `viz.seaborn_statistical_functions`, `viz.seaborn_themes_palettes`
- Built in: `final_batch_012_da_viz` | content_hash `b4e54d4ddf7d…` | steps 11 (3 explainer, 4 check, 3 hands_on, 1 recap) | remediation steps 3
- Interactions: 4 choice, 3 code_exercise | runtimes: chart_renderer | packs: core, data
- Blocks used: before_after, chart, code_walkthrough, prose, up_next
- Assets: ds.orders, ds.theming_demo | est. minutes: ? | completion reward: {'gems': 55} | next tile: `tile_viz_custom_multi_panel`
- Public copy present: yes | step titles: seaborn's DataFrame-first interface; Check your understanding; Practice; Automatic statistical estimation; Check your understanding; Check your understanding; Practice; Polishing plots with sns.set_theme(); Check your understanding; Practice; What you learned

#### 60. Multi-Panel Figures and Custom Styling  (`tile_viz_custom_multi_panel`)


- Concepts: `viz.custom_styling_theming`, `viz.multi_panel_figures`
- Built in: `final_batch_012_da_viz` | content_hash `28d06be20bd7…` | steps 9 (2 explainer, 3 check, 2 hands_on, 1 video, 1 recap) | remediation steps 2
- Interactions: 3 choice, 2 code_exercise | runtimes: chart_renderer | packs: core
- Blocks used: before_after, code_walkthrough, diagram, media_group, prose, up_next
- Assets: none | est. minutes: ? | completion reward: {'gems': 45} | next tile: `tile_stats_ab_test_lift`
- Public copy present: yes | step titles: Style sheets, rcParams, and seaborn palettes; Check your understanding; Check your understanding; Practice; A grid of Axes in one Figure; Video walkthrough; Check your understanding; Practice; What you learned

## Region: A/B Testing and Experiment Literacy (`region_experimentation_literacy`)
Read and interpret A/B test results, including lift, sample size, statistical significance, and what they mean for a business decision.

### Terrain: Reading Experiment Results (`terrain_experimentation_reading_results`)
Understand the structure of an A/B test and draw a sound business conclusion from its results.

#### 61. A/B Test Structure and Lift  (`tile_stats_ab_test_lift`)
Introduces the structure of a randomised A/B test (control group, treatment group, metric) and the concept of lift (relative improvement) using QuickRide's checkout-button experiment. Learners identify the parts of an experiment and compute lift from control and treatment conversion rates.

- Concepts: `stats.ab_test_structure`, `stats.lift_interpretation`
- Built in: `final_batch_010_da_stats_capstone` | content_hash `f51b27d8ff85…` | steps 8 (2 explainer, 1 video, 2 check, 2 hands_on, 1 recap) | remediation steps 4
- Interactions: 2 choice, 1 table_select, 1 code_exercise | runtimes: python, sql | packs: core, data
- Blocks used: data_table, diagram, heading, media_group, prose, side_by_side, up_next
- Assets: ds_ab_test_summary, ds_ab_test_users | est. minutes: ? | completion reward: {'gems': 20} | next tile: `tile_stats_sample_size_significance`
- Public copy present: yes | step titles: Two groups, one metric, one baseline; Watch: split testing in practice; Randomised vs non-randomised; Identify the groups and metric; Turning raw rates into a single comparison figure; Positive, negative, or neutral?; Compute lift and classify the outcome; What you've learned

#### 62. Sample Size, Effect Size, and Statistical Significance  (`tile_stats_sample_size_significance`)


- Concepts: `stats.sample_size_effect_concept`, `stats.significance_confidence_concept`, `stats.business_conclusion_from_experiment`
- Built in: `final_batch_004_da_chunk2` | content_hash `a00a808baead…` | steps 16 (5 explainer, 5 check, 3 hands_on, 2 video, 1 recap) | remediation steps 3
- Interactions: 5 choice, 1 external_proof, 1 table_select, 1 ordering | runtimes: none | packs: core, data
- Blocks used: callout, diagram, media_group, prose, side_by_side, up_next
- Assets: ds_ab_test_results | est. minutes: ? | completion reward: {'gems': 95} | next tile: `tile_stakeholder_framing_requirements`
- Public copy present: yes | step titles: Why Sample Size Changes How Much You Can Trust a Result; Which test result should you trust more?; Explain the Precision Difference; Hypotheses, p-Values, and Statistical Significance; p-Values and Sample Size in Action; What a Confidence Interval Actually Means; Null vs. Alternative Hypothesis; What Does the p-Value Measure?; Interpret the Confidence Interval; From Confidence Interval to Business Decision; Failing to Reject Is Not the Same as Accepting the Null; Statistical vs. Practical Significance; Null Value and Hypothesis Roles; Statistical vs. Practical Significance; Order the Steps to a Business Conclusion; What You Learned

## Region: Stakeholder Communication and Data Storytelling (`region_stakeholder_communication`)
Frame a business question, turn findings into a clear narrative and recommendation, and present them to a non-technical audience.

### Terrain: Framing the Business Question (`terrain_stakeholder_framing_question`)
Identify the decision a stakeholder needs to make and translate it into an answerable analytical question.

#### 63. Identifying Decisions, Findings, and Requirements  (`tile_stakeholder_framing_requirements`)


- Concepts: `stakeholder.identifying_decision_need`, `stakeholder.precise_finding_statement`, `stakeholder.framing_analytical_question`, `stakeholder.identifying_requirements`
- Built in: `final_batch_007_da_nocode` | content_hash `5258b474fa07…` | steps 18 (7 explainer, 6 check, 4 hands_on, 1 recap) | remediation steps 7
- Interactions: 6 choice, 2 table_select, 1 external_proof, 1 classify | runtimes: none | packs: core, data
- Blocks used: before_after, diagram, process_flow, prose, up_next
- Assets: ds_stakeholder_requests | est. minutes: ? | completion reward: {'gems': 110} | next tile: `tile_stakeholder_recommendation_translation`
- Public copy present: yes | step titles: What decision is this analysis for?; Spot the decision behind the request; Name the decision; From vague label to complete finding; Narrow the claim and add the number; Narrow the claim to match the data; Write a precise finding; From vague question to measurable question; Agreeing on what a good answer looks like; Components of a well-formed statistical question; Scoping stage agreement on outputs; Rewrite the vague question; What the commissioner must tell you; The specification document and output agreement; Commissioner inputs and the specification document; Resource constraints and output agreement; Extract scope and output requirements; What you've learned

### Terrain: Crafting the Narrative (`terrain_stakeholder_crafting_narrative`)
Turn findings into a prioritized, well-framed, audience-appropriate narrative.

#### 64. Recommendations and Plain-Language Translation  (`tile_stakeholder_recommendation_translation`)
Learn to turn analytical findings into concrete recommendations using the 'because we found X, we recommend Y' pattern, and to rewrite technical results in plain language by glossing specialist terms and replacing formal words with simpler ones.

- Concepts: `stakeholder.data_driven_recommendation`, `stakeholder.plain_language_translation`
- Built in: `final_batch_003_da_chunk` | content_hash `8a24ce3656b9…` | steps 7 (2 explainer, 2 check, 2 hands_on, 1 recap) | remediation steps 2
- Interactions: 2 choice, 1 table_select, 1 classify | runtimes: none | packs: core, data
- Blocks used: before_after, diagram, prose, up_next
- Assets: ds_city_delivery_summary | est. minutes: ? | completion reward: {'gems': 70} | next tile: `tile_stakeholder_prioritizing_framing_context`
- Public copy present: yes | step titles: From finding to action: the 'because X, recommend Y' pattern; Spotting a data-grounded recommendation; Write a data-grounded recommendation; Replacing jargon and formal words; Replacing a formal word with a simpler one; Match technical results to their plain-language rewrites; What you've learned

#### 65. Prioritizing Findings and Framing Recommendations  (`tile_stakeholder_prioritizing_framing_context`)
Learn to lead a stakeholder report with the finding most relevant to the decision, frame a recommendation that is distinct from the finding itself, and open the narrative with a short context section that level-sets the reader.

- Concepts: `stakeholder.prioritizing_findings_by_relevance`, `stakeholder.actionable_recommendation_framing`, `stakeholder.narrative_context_setup`
- Built in: `final_batch_004_da_chunk2` | content_hash `e0a61fcf1ff8…` | steps 13 (4 explainer, 5 check, 3 hands_on, 1 recap) | remediation steps 3
- Interactions: 5 choice, 1 ordering, 1 table_select, 1 external_proof | runtimes: none | packs: core, data
- Blocks used: before_after, data_table, diagram, prose, side_by_side, up_next
- Assets: ds_city_delivery_summary | est. minutes: ? | completion reward: {'gems': 78} | next tile: `tile_stakeholder_tailoring_anticipating`
- Public copy present: yes | step titles: Lead with what the decision-maker needs, not what surprised you most; Put the most important finding first; Which finding should lead the report?; Applying the inverted pyramid; Order these findings for the Head of Operations; A finding tells you what happened; a recommendation says what to do; Finding or recommendation?; Select the correctly framed recommendation; Start with why: set the context before the findings; What belongs in the opening context section?; Including operational context in the opener; Write the opening context section; What you covered

#### 66. Tailoring Detail and Anticipating Questions  (`tile_stakeholder_tailoring_anticipating`)
Learn to adjust information density and presentation order for technical vs. executive audiences, and to anticipate stakeholder questions by answering them in the writing.

- Concepts: `stakeholder.tailoring_detail_to_audience`, `stakeholder.anticipating_questions_objections`
- Built in: `final_batch_003_da_chunk` | content_hash `aebf593cad1a…` | steps 9 (3 explainer, 3 check, 2 hands_on, 1 recap) | remediation steps 1
- Interactions: 3 choice, 1 classify, 1 table_select | runtimes: none | packs: core, data
- Blocks used: before_after, diagram, prose, up_next
- Assets: ds_city_delivery_summary | est. minutes: ? | completion reward: {'gems': 27} | next tile: `tile_stakeholder_chart_matching_simplifying`
- Public copy present: yes | step titles: Same Finding, Different Audiences; Technical vs. Big-Picture Audiences; Adjusting Detail for the Audience; Match the Version to the Audience; Answering Questions Before They Are Asked; Tailoring to Anticipated Questions; Findings Before the Request; Prepare for Stakeholder Questions; Tailoring and Anticipating — Key Takeaways

### Terrain: Presenting Findings Visually (`terrain_stakeholder_presenting_visually`)
Match charts to the point being made and structure the final presentation or summary.

#### 67. Matching and Simplifying Charts for an Audience  (`tile_stakeholder_chart_matching_simplifying`)
Learn to choose the right chart type for the specific point you are making to a stakeholder audience, then simplify that chart by removing visual clutter so the operations manager can focus on the finding, not on reading the graph.

- Concepts: `stakeholder.chart_type_to_point_matching`, `stakeholder.simplifying_charts_for_audience`
- Built in: `final_batch_013_da_stakeholder_chart` | content_hash `abc880a61b53…` | steps 11 (3 explainer, 2 video, 3 check, 2 hands_on, 1 recap) | remediation steps 4
- Interactions: 3 choice, 2 classify | runtimes: none | packs: core, data
- Blocks used: before_after, chart, diagram, media_group, prose, side_by_side, up_next
- Assets: asset_city_deliveries, asset_lagos_weekly_deliveries | est. minutes: ? | completion reward: {'gems': 90} | next tile: `tile_stakeholder_presentation_structure`
- Public copy present: yes | step titles: The chart must match the point, not just the data; Why the chart type must match the point you are making; Pie charts, scatterplots, and the comparison trap; Scatterplot: exploratory or communicative?; Match the chart to the stakeholder point; Remove the clutter — not the data; Decluttering a chart for a non-technical audience; Which elements reduce clutter?; Why remove the border?; Simplify a chart for the operations manager; What you've learned

#### 68. Structuring Presentations and Writing Executive Summaries  (`tile_stakeholder_presentation_structure`)
Learn to structure a short presentation as opening, body, and call to action, and to write an executive summary with a takeaway title and section headers.

- Concepts: `stakeholder.presentation_structure_basics`, `stakeholder.executive_summary_writing`
- Built in: `final_batch_003_da_chunk` | content_hash `7d8d94f8fc25…` | steps 8 (3 explainer, 2 check, 2 hands_on, 1 recap) | remediation steps 1
- Interactions: 2 choice, 1 ordering, 1 external_proof | runtimes: none | packs: core
- Blocks used: before_after, diagram, process_flow, prose, up_next
- Assets: none | est. minutes: ? | completion reward: {'gems': 27} | next tile: `tile_capstone_question_workflow`
- Public copy present: yes | step titles: Opening, Body, Call to Action; Ending with a Call to Action; Beginning, Middle, End; Arrange the Lagos Presentation; The Executive Summary: One Page That Must Stand Alone; What Makes a Good Executive Summary?; Write an Executive Summary; Presentation Structure and Executive Summaries — Key Takeaways

## Region: Capstone Project (`region_capstone_project`)
Complete an end-to-end analysis project that combines data retrieval, cleaning, modeling, statistics, visualization, and stakeholder communication.

### Terrain: Planning the Capstone (`terrain_capstone_planning`)
Define the business question the capstone will answer and plan how the work will flow end to end.

#### 69. Defining the Question and Planning the Workflow  (`tile_capstone_question_workflow`)


- Concepts: `capstone.defining_business_question`, `capstone.data_retrieval_method_selection`, `capstone.end_to_end_workflow_structure`
- Built in: `final_batch_004_da_chunk2` | content_hash `7fbd5abd0b97…` | steps 14 (5 explainer, 4 check, 3 hands_on, 1 video, 1 recap) | remediation steps 3
- Interactions: 4 choice, 1 external_proof, 1 classify, 1 ordering | runtimes: none | packs: core
- Blocks used: before_after, diagram, media_group, process_flow, prose, side_by_side, up_next
- Assets: none | est. minutes: ? | completion reward: {'gems': 85} | next tile: `tile_capstone_integrate_tools_model`
- Public copy present: yes | step titles: From Vague Complaint to Scoped Business Question; Why Every Later Step Depends on the Scoped Question; Scoping the Question; Write Your Scoped Business Question; Matching Each Data Source to Its Retrieval Tool; read_excel() and SQL Retrieval in pandas; Which Tool for Which Source?; Classify Each Data Source by Retrieval Method; The Six-Stage Analytical Workflow; Modeling Multi-Table Data and Communicating Results; Workflow Stage Order; When to Revisit an Earlier Stage; Sequence the Workflow Stages; What You Learned

### Terrain: Integrating Tools (`terrain_capstone_integrating_tools`)
Bring SQL, spreadsheets, pandas, and a data model together in the capstone project.

#### 70. Integrating SQL, Spreadsheets, and pandas  (`tile_capstone_integrate_tools_model`)
Apply already-learned SQL, spreadsheet, and pandas skills to the QuickRide capstone project: retrieve last quarter's orders with a multi-clause SELECT, summarise the delivery sheet with a PivotTable and COUNTIFS, clean and aggregate orders in pandas, and model the two-table relationship with correct primary and foreign keys.

- Concepts: `capstone.integrate_sql`, `capstone.integrate_spreadsheet`, `capstone.integrate_python_pandas`, `capstone.building_data_model`
- Built in: `final_batch_010_da_stats_capstone` | content_hash `1e792da945a0…` | steps 20 (8 explainer, 2 video, 5 check, 4 hands_on, 1 recap) | remediation steps 5
- Interactions: 5 choice, 2 code_exercise, 1 formula_entry, 1 classify | runtimes: python, sql | packs: core, data
- Blocks used: before_after, code_walkthrough, data_table, diagram, heading, media_group, prose, spreadsheet_grid, up_next
- Assets: ds_capstone_delivery_sheet, ds_capstone_drivers, ds_capstone_orders, ds_pandas_orders | est. minutes: ? | completion reward: {'gems': 50} | next tile: `tile_capstone_stats_dashboard`
- Public copy present: yes | step titles: One SELECT statement: JOIN, WHERE, and GROUP BY together; Clause order: join first, filter next, group last; Watch: building a JOIN + WHERE + GROUP BY query; Where does the INNER JOIN go?; Write the capstone retrieval query; PivotTable and COUNTIFS on the capstone delivery sheet; Rearranging the PivotTable and applying COUNTIFS; Watch: inserting a PivotTable and arranging fields; Applying COUNTIFS with multiple criteria; Executing the capstone spreadsheet analysis step; Build the capstone PivotTable; Cleaning and grouping the capstone orders in pandas; The same skills, applied to the capstone's own data; Cleaning and aggregating the capstone dataset end-to-end; Detect missing values and compute per-zone means; Primary keys, foreign keys, and one-to-many in the capstone; Mapping the capstone tables onto the model; Identifying the one-to-many relationship in the capstone; Match columns to their roles in the capstone data model; What you've built so far

### Terrain: Delivering the Capstone (`terrain_capstone_delivering`)
Apply statistics, build the dashboard, and execute and deliver the finished capstone independently.

#### 71. Descriptive Statistics and Dashboard  (`tile_capstone_stats_dashboard`)
Apply pandas describe() to the capstone delivery data, choose between mean and median based on skew and the business question, then build a multi-panel matplotlib figure using either plt.subplots(2, 2) or plt.subplot(131/132/133) + plt.suptitle().

- Concepts: `capstone.applying_descriptive_statistics`, `capstone.building_dashboard_or_viz`
- Built in: `final_batch_010_da_stats_capstone` | content_hash `996408787034…` | steps 11 (4 explainer, 3 check, 2 hands_on, 1 video, 1 recap) | remediation steps 3
- Interactions: 3 choice, 2 code_exercise | runtimes: chart_renderer, python, sql | packs: core, data
- Blocks used: code_walkthrough, data_table, heading, media_group, prose, up_next
- Assets: ds_capstone_orders | est. minutes: ? | completion reward: {'gems': 27} | next tile: `tile_capstone_execution_narration_delivery`
- Public copy present: yes | step titles: Running describe() on the capstone delivery data; Choosing mean or median for the business question; Mean vs median for a skewed distribution; Call describe() and choose the right statistic; Two patterns for multi-panel figures in matplotlib; Choosing a layout for the capstone figure; Watch: arranging multiple charts in one figure with subplots; Creating multi-panel figures: 2×2 grid and side-by-side row; Selecting the right multi-panel layout for the capstone; Build the capstone multi-panel figure; Statistics and visualisation: the capstone findings are ready

#### 72. Narrating and Delivering the Capstone  (`tile_capstone_execution_narration_delivery`)


- Concepts: `capstone.independent_execution`, `capstone.narrated_stakeholder_summary`, `capstone.documenting_presenting_deliverable`
- Built in: `final_batch_004_da_chunk2` | content_hash `399dba58d30d…` | steps 11 (4 explainer, 3 check, 3 hands_on, 1 recap) | remediation steps 3
- Interactions: 3 choice, 3 external_proof | runtimes: none | packs: core
- Blocks used: before_after, diagram, process_flow, prose
- Assets: none | est. minutes: ? | completion reward: {'gems': 85} | next tile: `None`
- Public copy present: yes | step titles: Running the Whole Plan Yourself; What Belongs in the Decision Log?; Execute the Capstone Plan; Turning Findings into a Story for the Operations Team; Beginning, Middle, End — and What Counts as Sufficient; What Counts as Sufficient Delivery?; Write the Narrated Stakeholder Summary; Packaging the Work So Others Can Evaluate It; Delivery Formats; Assemble the Capstone Deliverable; What You Learned
