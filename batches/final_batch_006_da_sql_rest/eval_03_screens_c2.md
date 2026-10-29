# Evaluation — 03_screens, chunk c2 (scoped re-evaluation after repair)

**Batch:** final_batch_006_da_sql_rest  
**Tiles evaluated:** tile_sql_style_conventions, tile_sql_text_dates_casts, tile_sql_null_fallback_and_union  
**Scope:** Confirm repairs to previously identified defects; verify no regressions.

## Repair Verification

### 1. BLOCKING tile_sql_text_dates_casts/s01 before_after — stray spaces claim vs registry
- **Before caption** now: "Raw city values — inconsistent casing" — no stray-spaces claim. ✓ FIXED  
- **After caption** now: "After LOWER(TRIM(city)) — consistent lowercase, casing standardised" — no stray-spaces claim. ✓ FIXED  
- **change_summary** now: "LOWER(TRIM(city)) standardises city values to consistent lowercase." — no stray-spaces claim. ✓ FIXED  
- Registry `ds_customers_messy` only plants a casing change; text is now consistent.

### 2. ADVISORY tile_sql_style_conventions/s01 before annotation — "column names mixed-case"
- Annotation now reads: "Keywords lowercase, column names lowercase, no line breaks, no spaces around operators" — accurately describes the before code. ✓ FIXED

### 3. ADVISORY tile_sql_text_dates_casts/s01.p2 — f3 NULL-ignoring behaviour
- Block now reads: "CONCAT concatenates the text representations of all its arguments into one string and ignores any NULL arguments" — explicitly states the NULL-ignoring behaviour from f3. ✓ FIXED

### 4. ADVISORY tile_sql_text_dates_casts/s07.p1 — "integer column" vs "numeric column"
- Block now reads: "that numeric column to text" — matches glossary tb1 wording ("numeric column"). ✓ FIXED

### 5. Unparsed BLOCKING — change_summary in tile_sql_style_conventions/s01.ba
- change_summary now reads: "The same query reformatted: keywords uppercased, columns lowercased, each clause on its own right-aligned line, spaces around operators."
- The phrase "columns lowercased" is slightly misleading since the before code already has lowercase columns, but this describes the conventions demonstrated in the after version, not strictly a before→after delta. Residual ADVISORY only.

## Residual Defects

| Severity | Location | Description |
|----------|----------|-------------|
| ADVISORY | tile_sql_style_conventions/s01.ba change_summary | Says "columns lowercased" but the before code already has lowercase columns; the phrase describes conventions applied rather than actual changes. |

## Regression Check
- JSON validity: confirmed (parses without error).
- All three expected tile IDs present.
- No new structural or factual issues introduced by the repair.

VERDICT: PASS
