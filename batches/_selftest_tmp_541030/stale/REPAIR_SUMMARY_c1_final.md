# REPAIR ROUND SUMMARY - interactions.part.c1.json

## Artifact
`batches/final_batch_009_da_pandas/interactions.part.c1.json`

## Changes Applied

### 1. ADVISORY tile_pandas_creating_inspecting/s04/hints
**Finding**: Hint 0 incorrectly said "Use `pd.DataFrame('orders_sample.csv')` to load the file." which is wrong for this exercise.

**Fix**: Changed hint 0 to: "Use `pd.DataFrame(dict_of_lists)` and `pd.DataFrame(list_of_dicts)` to create the two DataFrames."

**Rationale**: The exercise asks learners to create DataFrames from the provided `dict_of_lists` and `list_of_dicts` variables, not to load a CSV file. The hint now correctly guides learners to use the appropriate constructors.

### 2. ADVISORY tile_pandas_selection_filtering/s05/solution
**Finding**: Model solution used chained indexing `df.loc[...][col]` instead of the taught comma form.

**Fix**: Updated solution to use comma form:
- `loc_result = df.loc[start_row:end_row_loc, city_col_name]`
- `iloc_result = df.iloc[start_row:end_row_iloc, city_col_name]`

**Rationale**: The comma form `df.loc[rows, cols]` is the standard pandas idiom taught in the concept. Chained indexing can trigger SettingWithCopyWarning and is not the recommended approach.

### 3. ADVISORY tile_pandas_creating_inspecting/s10
**Finding**: No test verified that dtypes was accessed.

**Fix**: Added test `t3` of kind `stdout_contains` checking for substring "int64" with message "Your output should include the dtypes. Make sure you printed df.dtypes."

**Rationale**: The exercise measures the capability "read_column_dtypes" and the prompt asks learners to print dtypes. Adding a test ensures the learning objective is verified.

## Validation
- JSON structure is valid
- 3 tiles with 14 total interactions (5 + 5 + 4)
- All three fixes verified correct
- No new defects introduced

## Method
Used a targeted patch script that modified only the three specific findings:
1. Updated feedback.hints[0] for s04
2. Replaced solution content for s05 with comma-form indexing
3. Appended stdout_contains test to s10

No other changes were made to the artifact.
