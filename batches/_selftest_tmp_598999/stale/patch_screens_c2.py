import json, copy

path = "batches/final_batch_009_da_pandas/screens.part.c2.json"
with open(path) as f:
    data = json.load(f)

# Locate tile_pandas_descriptive_stats
tile = next(t for t in data["tiles"] if t["tile_id"] == "tile_pandas_descriptive_stats")

# ── FIX 1: s01.b2 prose ─────────────────────────────────────────────────────
# Change from 7-order batch numbers to full 14-row dataset numbers
s01 = next(s for s in tile["steps"] if s["step_id"] == "tile_pandas_descriptive_stats.s01")
b2 = next(b for b in s01["blocks"] if b["block_id"] == "tile_pandas_descriptive_stats.s01.b2")
b2["text"] = (
    "pandas provides built-in statistical methods for a Series or DataFrame column, "
    "including `mean()` (mean of values), `median()` (arithmetic median), and `std()` "
    "(sample standard deviation): if `delivery_time_minutes` holds all fourteen orders, "
    "`orders[\"delivery_time_minutes\"].mean()`, `.median()`, and `.std()` return "
    "approximately 29.0, 25.0, and 15.6 minutes."
)

# ── FIX 2: s05.b1 recap prose ────────────────────────────────────────────────
# Change from 7-value batch numbers (~30.9, 22) to 14-row dataset numbers (29.0, 25.0)
s05 = next(s for s in tile["steps"] if s["step_id"] == "tile_pandas_descriptive_stats.s05")
b1_s05 = next(b for b in s05["blocks"] if b["block_id"] == "tile_pandas_descriptive_stats.s05.b1")
b1_s05["text"] = (
    "pandas provides `mean()`, `median()`, and `std()` as direct methods on a Series or column. "
    "`describe()` bundles count, mean, std, min, quartiles, and max into one call. "
    "For the SwiftDrop delivery-time column, the mean (29.0 min) sits above the median (25.0 min) "
    "because a single 80-minute outlier pulls the average up \u2014 a pattern describe() makes "
    "immediately visible."
)

# ── FIX 3: r01 remediation ───────────────────────────────────────────────────
# Update prose and before_after code to use full 14-row dataset numbers
r01 = next(s for s in tile["remediation_steps"] if s["step_id"] == "tile_pandas_descriptive_stats.r01")

# r01.b1 prose
b1_r01 = next(b for b in r01["blocks"] if b["block_id"] == "tile_pandas_descriptive_stats.r01.b1")
b1_r01["text"] = (
    "`describe()` computes a set of summary statistics \u2014 count, mean, std, min, quartiles "
    "(25%, 50%, 75%), and max \u2014 for a Series or for each numeric column of a DataFrame in one call. "
    "The `50%` row is the median. For the SwiftDrop delivery-time column (all fourteen orders), "
    "`describe()` shows count 14, mean 29.0, std 15.6, min 18, 25% 21.25, 50% (median) 25.0, "
    "75% 30.25, and max 80."
)

# r01.b2 before_after code
b2_r01 = next(b for b in r01["blocks"] if b["block_id"] == "tile_pandas_descriptive_stats.r01.b2")
b2_r01["before"]["code"] = (
    "# Individual calls \u2014 one statistic at a time\n"
    "print(orders[\"delivery_time_minutes\"].mean())    # 29.0\n"
    "print(orders[\"delivery_time_minutes\"].median())  # 25.0\n"
    "print(orders[\"delivery_time_minutes\"].std())     # 15.6"
)
b2_r01["after"]["code"] = (
    "# describe() \u2014 all summary statistics in one call\n"
    "print(orders[\"delivery_time_minutes\"].describe())\n"
    "# count    14.0\n"
    "# mean     29.0\n"
    "# std      15.6\n"
    "# min      18.0\n"
    "# 25%      21.25\n"
    "# 50%      25.0   <- median\n"
    "# 75%      30.25\n"
    "# max      80.0"
)

with open(path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Patch applied successfully.")
