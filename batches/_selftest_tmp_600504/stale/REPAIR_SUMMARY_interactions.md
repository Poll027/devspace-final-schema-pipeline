# Repair Summary for interactions.part.c1.json

## Fixes Applied

### 1. tile_pandas_creating_inspecting.s04
**Issue**: Solution uses `dict_lit`, `list_lit`, `lit_int`, `lit_str` which were not in allowed_syntax. Also, t1/t2 tests were hard-coded (no data or starter variables to mutate).

**Fix**:
- Added to allowed_syntax: `'{key: value} dictionary literal'`, `'[...] list literal'`, `'whole-number literals as in the examples'`, `'single- or double-quoted strings'`
- Modified starter to include `data_dict` and `data_list` as pre-defined variables (top-level assignments that the gate can mutate)
- Solution now uses these starter variables, making tests data-dependent

### 2. tile_pandas_creating_inspecting.s10
**Issue**: The solution's dtypes output has wider spacing than the expected value (pandas version difference).

**Fix**:
- Updated `spec.expected` to match the actual pandas output format with wider column alignment (27 chars for column names)

### 3. tile_pandas_selection_filtering.s05
**Issue**: Solution uses `lit_int`, `lit_str`, `tuple_lit` which were not in allowed_syntax.

**Fix**:
- Added to allowed_syntax: `'whole-number literals as in the examples'`, `'single- or double-quoted strings'`, `'tuple literal with commas or parentheses'`

### 4. tile_pandas_selection_filtering.s10
**Issue**: Solution uses `lit_int`, `lit_str` which were not in allowed_syntax.

**Fix**:
- Added to allowed_syntax: `'whole-number literals as in the examples'`, `'single- or double-quoted strings'`
- Note: The descriptor `"df[df['col'] > value]"` already covers `bool_filter`, so no additional fix needed

### 5. tile_pandas_sort_rename.s03
**Issue**: Solution uses `list_lit`, `lit_bool`, `lit_str` which were not in allowed_syntax.

**Fix**:
- Added to allowed_syntax: `'[...] list literal'`, `'True / False'`, `'single- or double-quoted strings'`

### 6. tile_pandas_sort_rename.s06
**Issue**: t1/t2/t3 tests were hard-coded (checking column/index names that don't change when data changes). Solution uses `dict_lit`, `lit_int`, `lit_str` which were not in allowed_syntax.

**Fix**:
- Added to allowed_syntax: `'{key: value} dictionary literal'`, `'whole-number literals as in the examples'`, `'single- or double-quoted strings'`
- Replaced t1/t2/t3 with data-dependent tests:
  - t1: `renamed['destination_city'].tolist()` - checks actual city values
  - t2: `renamed['delivery_min'].tolist()` - checks actual delivery time values
  - t3: `renamed.loc['first_order', 'destination_city']` - checks specific cell value (data-dependent)

## Unresolved Issue (Outside Scope)

**tile_pandas_creating_inspecting.s05**: Plan requires `annotated_image` or `diagram` block, but the screens artifact has a `comparison` block instead. This is a screens artifact issue (stage 03), not an interactions artifact issue (stage 04). Cannot fix from this stage.

## Verification

All syntax violations have been resolved. The tests are now data-dependent where required. The JSON structure is valid.
