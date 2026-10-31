# Evaluation — Stage 04 Interactions (chunk c2)

**Batch:** `final_batch_006_da_sql_rest`
**Tiles evaluated:** `tile_sql_style_conventions`, `tile_sql_text_dates_casts`, `tile_sql_null_fallback_and_union`
**Interactions reviewed:** 13 / 13 (all)

## Summary

All choice-question keys are correct and unambiguous. All code-exercise expected results match the registry data when computed by hand. All feedback messages are factually accurate. Practice-anchor success sentences are satisfied by the corresponding exercises. No glossary facts are contradicted.

## Defects

### ADVISORY

1. **tile_sql_text_dates_casts/s03 (prompt wording):** The prompt states "Some city values may have stray spaces" but the exercise mounts the base `ds_customers` dataset, which has no stray spaces. TRIM is effectively a no-op on the test data. → Consider mounting `ds_customers_messy` (which has a lowercase 'kano') or softening the prompt to "may have stray spaces or inconsistent casing."

2. **tile_sql_text_dates_casts/s03 (capability coverage):** The interaction measures capability `build_a_label_with_concat_and_length` (fact_ids f3, f4) but the exercise only uses CONCAT, not LENGTH. LENGTH (f4) is not exercised anywhere in this tile's interactions. → Consider adding a LENGTH column to the exercise or splitting the measurement.

3. **tile_sql_style_conventions/s03 (style enforcement):** The code exercise can only verify the result set, not actual formatting. A learner could submit a query with incorrect formatting (e.g., left-aligned keywords, no alias) and still pass. → Inherent limitation of result-based testing for style exercises; the prompt and hints are clear about expectations.

4. **tile_sql_null_fallback_and_union/s04 (alternative solution):** A learner could use `CASE WHEN city IS NULL THEN 'Unknown' ELSE city END AS city` instead of COALESCE and pass all tests. The starter-code comment mentions COALESCE but no syntax or hidden check enforces it. → Consider adding a hidden check or syntax constraint that requires COALESCE.

## Verdict

VERDICT: PASS
