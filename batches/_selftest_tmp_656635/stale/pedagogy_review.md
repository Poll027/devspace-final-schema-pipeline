# Pedagogy Review — Batch final_batch_010_da_stats_capstone

**Evaluator:** Stage 08 Independent Evaluator  
**Date:** 2024-11-05  
**Tiles reviewed:** 4 (all tiles in batch)

---

## Summary

All four tiles follow the explain → check → apply flow correctly. Concepts are introduced before being tested, and remediation steps address specific mistakes. The data calculations are accurate and consistent with the glossary bundle and scenario registry.

**Pacing concerns:** Three of four tiles exceed the recommended 6–12 minute range, and one tile (tile_capstone_integrate_tools_model) has 20 steps, exceeding the 8–14 step guideline. These are ADVISORY issues as they affect learner experience but do not prevent learning.

---

## Tile-by-Tile Review

### tile_stats_center_spread (10 steps, 14.1 min)

**Flow:** ✓ Correct  
- s01–s02: Explainers introduce mean, median, mode (stats.descriptive_measures_of_center)
- s03: Check tests understanding of when median is better than mean
- s04: Hands-on applies all three calculations
- s05–s06: Explainers introduce range, variance, standard deviation (stats.measures_of_spread)
- s07: Video reinforces variance/std calculation
- s08: Check tests understanding of range limitation
- s09: Hands-on applies all three spread calculations
- s10: Recap consolidates both concepts

**Data accuracy:** ✓ Verified  
- Seven delivery times: 18, 20, 22, 22, 26, 28, 80
- Mean ≈ 30.857, Median = 22, Mode = 22
- Range = 62, Variance ≈ 481.14, Std ≈ 21.93

**Remediation:** ✓ Each wrong-answer feedback addresses the specific mistake

**Pacing:** Slightly over (14.1 min vs 6–12 target)

---

### tile_stats_ab_test_lift (8 steps, 9.1 min)

**Flow:** ✓ Correct  
- s01: Explainer introduces A/B test structure (control, treatment, metric)
- s02: Video reinforces structure
- s03: Check tests randomized vs non-randomized distinction
- s04: Hands-on identifies groups and metric in table
- s05: Explainer introduces lift calculation
- s06: Check tests positive/negative/neutral classification
- s07: Hands-on computes lift and classifies outcome
- s08: Recap consolidates both concepts

**Data accuracy:** ✓ Verified  
- Control: 500 users, 100 conversions, rate = 0.20
- Treatment: 500 users, 110 conversions, rate = 0.22
- Lift = (0.22 - 0.20) / 0.20 × 100 = 10%

**Remediation:** ✓ Each wrong-answer feedback addresses the specific mistake

**Pacing:** ✓ Within range (9.1 min)

---

### tile_capstone_stats_dashboard (11 steps, 15.5 min)

**Flow:** ✓ Correct  
- s01–s02: Explainers introduce describe() and mean vs median choice
- s03: Check tests mean vs median selection
- s04: Hands-on applies describe() and computes both statistics
- s05–s06: Explainers introduce multi-panel figure patterns
- s07: Video reinforces matplotlib subplots
- s08–s09: Checks test understanding of both patterns
- s10: Hands-on builds multi-panel figure
- s11: Recap consolidates both concepts

**Data accuracy:** ✓ Verified  
- Ikeja delivery times: mean = 52.0, median = 38.0 (matches registry)
- The 178-minute outlier pulls mean up, demonstrating the concept

**Remediation:** ✓ Each wrong-answer feedback addresses the specific mistake

**Pacing:** Over range (15.5 min vs 6–12 target)

---

### tile_capstone_integrate_tools_model (20 steps, 23.7 min)

**Flow:** ✓ Correct  
- s01–s05: SQL integration (JOIN + WHERE + GROUP BY)
- s06–s11: Spreadsheet integration (PivotTable + COUNTIFS)
- s12–s15: Python/pandas integration (isna/dropna + groupby)
- s16–s19: Data modelling (PK/FK, one-to-many)
- s20: Recap consolidates all four concepts

**Data accuracy:** ✓ Verified  
- Zone averages match registry data
- COUNTIFS formula correctly counts Ikeja deliveries > 45 min (2 rows)

**Remediation:** ✓ Each wrong-answer feedback addresses the specific mistake

**Pacing:** Significantly over range (20 steps vs 8–14, 23.7 min vs 6–12)

**Note:** This tile covers 4 concepts (capstone.integrate_sql, capstone.integrate_spreadsheet, capstone.integrate_python_pandas, capstone.building_data_model), which explains the higher step count. The flow within each concept section is correct.

---

## Findings

### ADVISORY

1. **ADVISORY tile_stats_center_spread/pacing:** Estimated time 14.1 min exceeds 6–12 min guideline → Consider splitting into two tiles or reducing explainer content

2. **ADVISORY tile_capstone_stats_dashboard/pacing:** Estimated time 15.5 min exceeds 6–12 min guideline → Consider splitting into two tiles or reducing explainer content

3. **ADVISORY tile_capstone_integrate_tools_model/pacing:** 20 steps and 23.7 min significantly exceed guidelines (8–14 steps, 6–12 min) → Consider splitting into two tiles (SQL+Spreadsheet and Pandas+DataModel)

### No BLOCKING defects found

All tiles:
- Follow explain → check → apply flow correctly
- Teach concepts before testing them
- Provide remediation that addresses specific mistakes
- Use accurate data consistent with glossary and registry
- Do not require knowledge from later concepts

---

## Verdict

**VERDICT: PASS**

The pedagogy is sound. All concepts are taught before being tested, remediation addresses specific mistakes, and data is accurate. The pacing advisories are noted but do not prevent learners from succeeding with the material as written.
