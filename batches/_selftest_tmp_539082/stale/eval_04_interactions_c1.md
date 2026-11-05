# Evaluation — stage 04_interactions, chunk c1 (scoped re-evaluation)

## Scope
Checking only the seven findings sent for repair against the repaired artifact `interactions.part.c1.json`.

## Finding-by-finding verification

### 1. BLOCKING tile_pandas_creating_inspecting/s04 — prompt "3×3" → "14×3"
**Status: FIXED.** Prompt now reads "They should produce the same 14×3 DataFrame (14 rows, 3 columns)."

### 2. BLOCKING tile_pandas_sort_rename/s02/opt_c — false feedback about chaining
**Status: FIXED.** Feedback now correctly states: "Chaining two single-column `sort_values()` calls does not produce the same result as one multi-column call. The second sort re-orders all rows by `delivery_time_minutes`, breaking the city grouping from the first sort."

### 3. BLOCKING tile_pandas_sort_rename/s05 — opt_c defensible correct answer
**Status: FIXED.** Prompt now specifies "in a **single** `rename()` call" and opt_c feedback says "This works but uses two calls. The question asks for a single `rename()` call that handles both at once."

### 4. ADVISORY tile_pandas_creating_inspecting/s04 — feedback✔ and hints
**Status: PARTIALLY FIXED.** The feedback✔ message was updated to "Excellent! You built the same DataFrame from both a dict of lists and a list of dicts." However, hint 0 still reads `Use pd.DataFrame('orders_sample.csv') to load the file.` — this is wrong for this exercise (the task is to create DataFrames from `dict_of_lists` and `list_of_dicts`, not load a file). `pd.DataFrame('orders_sample.csv')` would not load a CSV. Remains ADVISORY.

### 5. ADVISORY tile_pandas_selection_filtering/s05 — chained indexing in model solution
**Status: NOT FIXED.** Solution still uses `df.loc[start_row:end_row_loc][city_col_name]` instead of comma form, and does not use `city_col_pos` for iloc. Remains ADVISORY.

### 6. ADVISORY tile_pandas_sort_rename/s03 — t1 on-fail message
**Status: FIXED.** On-fail message now shows the full 14-item expected list.

### 7. ADVISORY tile_pandas_creating_inspecting/s10 — no dtypes test
**Status: NOT FIXED (accepted as-is).** No new test for dtypes. Remains ADVISORY.

## Remaining defects

ADVISORY tile_pandas_creating_inspecting/s04/hints: Hint 0 still says `Use pd.DataFrame('orders_sample.csv') to load the file.` which is factually wrong for this exercise (the task is to wrap `dict_of_lists` / `list_of_dicts` with `pd.DataFrame()`). → Change hint 0 to "Use `pd.DataFrame(dict_of_lists)` and `pd.DataFrame(list_of_dicts)` to create the two DataFrames."

ADVISORY tile_pandas_selection_filtering/s05/solution: Model solution uses chained indexing `df.loc[...][col]` instead of the taught comma form `df.loc[..., col]`. → Update to `loc_result = df.loc[start_row:end_row_loc, city_col_name]` and `iloc_result = df.iloc[start_row:end_row_iloc, city_col_name]`.

ADVISORY tile_pandas_creating_inspecting/s10: No test verifies dtypes was accessed. → Accept as-is or add a test.

## Verdict

All three original BLOCKING defects have been correctly repaired. No new BLOCKING defects introduced.

VERDICT: PASS
