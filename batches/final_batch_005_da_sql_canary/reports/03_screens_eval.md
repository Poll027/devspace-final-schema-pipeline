# 03_screens Evaluation — final_batch_005_da_sql_canary

## Tiles reviewed
- **tile_sql_fund_relational_select** (canary tile): all 10 steps + 4 remediation steps reviewed
- **tile_sql_fund_alias_distinct**: all 8 steps + 4 remediation steps reviewed

## Sources consulted
- `inputs/path_glossary_bundle.json` — all four concept bundles (sql.relational_model, sql.select_fundamentals, sql.aliasing, sql.distinct)
- `scenario_asset_registry.json` — ds.customers (8 rows, 4 distinct cities), ds.orders (10 rows), ds.products (5 rows)

## Defects

### BLOCKING

1. **tile_sql_fund_alias_distinct/r03.b1**: The text states "The customers table has eight rows with **three** distinct cities: Lagos (3 customers), Abuja (2), Kano (2), Port Harcourt (1)." The registry shows four distinct cities (Lagos, Abuja, Kano, Port Harcourt), and the same sentence lists all four and says DISTINCT returns four rows. The word "three" is a factual error.
   → Fix: replace "three distinct cities" with "four distinct cities".

### ADVISORY

1. **tile_sql_fund_alias_distinct/s08 lineage**: The recap text covers sql.distinct facts (f1: DISTINCT removes duplicates; f2: SELECT ALL is the default) and sql.aliasing#f2 (must use alias, not original name), but the step lineage lists only sql.aliasing#f1 and sql.aliasing#f3. No content error, but lineage is incomplete.

2. **tile_sql_fund_relational_select/s01.b1**: The intro says "each table holds one kind of data" which paraphrases fact f5 ("each table should contain information about one kind of thing only"), but f5 is not listed in the block's lineage fact_ids. Minor lineage gap.

3. **tile_sql_fund_alias_distinct/s01**: The lede "Typing out orders or customers in full every time gets tedious" is a motivational framing rather than a factual claim, but it slightly overstates the burden for short table names. Purely stylistic.

## Verdict

VERDICT: FAIL
BLOCKING tile_sql_fund_alias_distinct/r03.b1: text says "three distinct cities" but the customers table has four distinct cities (Lagos, Abuja, Kano, Port Harcourt) → replace "three distinct cities" with "four distinct cities"
ADVISORY tile_sql_fund_alias_distinct/s08 lineage: recap step lineage omits sql.distinct#f1, sql.distinct#f2, and sql.aliasing#f2 even though the prose covers those facts → add missing fact_ids to lineage
ADVISORY tile_sql_fund_relational_select/s01.b1 lineage: block paraphrases f5 but f5 is not in block lineage → add sql.relational_model#f5 to block lineage
ADVISORY tile_sql_fund_alias_distinct/s01: lede framing slightly overstates tedium of typing short table names → no change required, stylistic only
