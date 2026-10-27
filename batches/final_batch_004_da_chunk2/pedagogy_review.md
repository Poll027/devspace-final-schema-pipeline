# Pedagogy Review — batch `final_batch_004_da_chunk2`

Reviewer: independent evaluator (stage 08)
Date: 2025-01-24

## Tiles reviewed

| Tile | Steps (main) | Remediation | Est. minutes | Concepts |
|------|-------------|-------------|-------------|----------|
| tile_stakeholder_prioritizing_framing_context | 13 | 3 | 13.0 | 3 |
| tile_stats_sample_size_significance | 16 | 3 | 27.1 | 3 |
| tile_capstone_question_workflow | 14 | 3 | 16.2 | 3 |
| tile_capstone_execution_narration_delivery | 11 | 3 | 10.8 | 3 |

---

## Tile-by-tile analysis

### 1. tile_stakeholder_prioritizing_framing_context

**Flow (explain → check → apply):** Correct for all three concepts. Each concept block follows: explainer(s) → check(s) → hands_on. No check arrives before its idea is taught.

**One idea per step:** Each step covers a single concept. No step mixes two concepts (except the recap, which is appropriate).

**Dead text:** None found. All prose blocks serve the teaching purpose.

**Reading load:** Reasonable. Prose blocks are concise and scenario-grounded.

**Difficulty ramp:** Intro checks → core checks → stretch hands_on. Appropriate progression.

**Remediation quality:** All three remediation steps directly address the specific mistake pattern. r01 re-explains the relevance-vs-novelty criterion with a concrete analyst-A vs analyst-B comparison. r02 re-explains finding vs recommendation with the exact structural difference. r03 re-explains short opener vs lengthy background.

**Visuals:** The side_by_side in s01 (analytical interestingness vs decision relevance) and the before_after in s06 (finding-only vs finding+recommendation) and s09 (weak opener vs strong opener) all earn their place — they illustrate the structural contrast the text teaches.

**Pacing:** 13 steps, 13.0 minutes. Steps within guideline (8–14); minutes slightly above guideline (6–12). See advisory below.

**Video step:** None present. No video step in this tile.

**Specific issues:**
- s05 ordering item `item_kano_var` text: "Kano has notable delivery-time variability across all three cities." This reads as if Kano's variability extends across all three cities. Should say "Kano has the most notable delivery-time variability of the three cities" or similar. Does not prevent the learner from succeeding (the item is correctly placed near the bottom regardless). ADVISORY.

### 2. tile_stats_sample_size_significance

**Flow (explain → check → apply):** Correct for all three concepts. sample_size_effect: s01 (explainer) → s02 (check) → s03 (hands_on). significance_confidence: s04 (explainer) → s05 (video) → s06 (explainer) → s07 (check) → s08 (check) → s09 (hands_on). business_conclusion: s10 (explainer) → s11 (explainer) → s12 (video) → s13 (check) → s14 (check) → s15 (hands_on). No check arrives before its idea is taught.

**One idea per step:** Each step covers a single concept. s04 introduces H0/HA and p-value in the same step, but these are tightly coupled components of the same concept (significance_confidence_concept) and are presented as a unified mechanism. Acceptable.

**Dead text:** None found.

**Reading load:** s04 is dense — it introduces H0, HA, p-value, and statistical significance, plus previews confidence intervals. However, the CI preview is explicitly flagged as "a concept covered fully in the next step." The density is at the upper limit but manageable.

**Difficulty ramp:** Appropriate. Intro checks → core checks → stretch hands_on for each concept block.

**Remediation quality:** All three remediation steps directly address the specific mistake. r01 re-explains sample size and precision. r02 re-explains H0/HA and p-value. r03 re-explains null-value-inside-vs-outside-CI and the fail-to-reject misconception.

**Visuals:** The side_by_side number lines in s01 (small vs large sample scatter) effectively illustrate precision. The CI array diagram in s04 (25 intervals, one missing) illustrates the repeated-sampling interpretation. The number-line diagram in s10 (null value inside vs outside CI) illustrates the reject/fail-to-reject decision. All earn their place.

**Pacing:** 16 steps, 27.1 minutes. Both significantly exceed the guideline (8–14 steps, 6–12 minutes). This tile covers three substantial statistical concepts with two video steps. See advisory below.

**Video steps:** s05 (p-values and sample size) and s12 (business conclusions from experiments). Both have bridge text explaining what the video adds vs what the text covers. The video in s05 explicitly does not cover confidence intervals (f4, f5) or the misconception (m1), which are covered in text. The video adds visual demonstration of how sample size drives p-values — something the text alone cannot show as effectively.

**Specific issues:**
- The lesson consistently says "10% lift" while the registry data shows 9.8%. The glossary teaching blocks also use "10% lift" as the narrative framing, so this is a deliberate pedagogical rounding, not a data contradiction. ADVISORY.

### 3. tile_capstone_question_workflow

**Flow (explain → check → apply):** Correct for all three concepts. defining_business_question: s01-s02 (explainers) → s03 (check) → s04 (hands_on). data_retrieval_method_selection: s05 (explainer) → s06 (video) → s07 (check) → s08 (hands_on). end_to_end_workflow_structure: s09-s10 (explainers) → s11-s12 (checks) → s13 (hands_on). No check arrives before its idea is taught.

**One idea per step:** Each step covers a single concept. No overloading.

**Dead text:** None found.

**Reading load:** Reasonable throughout. Prose blocks are concise.

**Difficulty ramp:** Appropriate. Intro → core → stretch progression.

**Remediation quality:** All three remediation steps directly address the specific mistake. r01 re-explains scoping with context and boundaries. r02 re-explains source-determines-tool. r03 re-explains that the workflow is not strictly linear.

**Visuals:** The before_after in s01 (vague complaint → scoped question) is effective. The side_by_side in s05 (database retrieval vs Excel retrieval) clearly maps source to tool. The process_flow in s09 (six-stage workflow) provides the structural overview. All earn their place.

**Pacing:** 14 steps, 16.2 minutes. Steps at the upper boundary of guideline; minutes exceed guideline. See advisory below.

**Video step:** s06 shows both retrieval methods in action (read_excel and pd.read_sql_query). Bridge text explains what the clips show vs what the text covers. The video adds something the text cannot: seeing the actual code execution.

**Specific issues:** None blocking.

### 4. tile_capstone_execution_narration_delivery

**Flow (explain → check → apply):** Correct for all three concepts. independent_execution: s01 (explainer) → s02 (check) → s03 (hands_on). narrated_stakeholder_summary: s04-s05 (explainers) → s06 (check) → s07 (hands_on). documenting_presenting_deliverable: s08 (explainer) → s09 (check) → s10 (hands_on). No check arrives before its idea is taught.

**One idea per step:** Each step covers a single concept. No overloading.

**Dead text:** None found.

**Reading load:** Reasonable. The lightest tile in the batch.

**Difficulty ramp:** Appropriate. Intro checks → stretch hands_on (external_proof).

**Remediation quality:** All three remediation steps directly address the specific mistake. r01 re-explains design phase vs analysis phase. r02 re-explains beginning/middle/end structure. r03 re-explains documentation as what makes work evaluable.

**Visuals:** The process_flow in s01 (two-phase independent execution) and the before_after in s04 (raw zone data → narrated summary) both earn their place.

**Pacing:** 11 steps, 10.8 minutes. Within guideline.

**Video step:** None present. No video step in this tile.

**Specific issues:** None.

---

## Defect list

### BLOCKING

None.

### ADVISORY

1. **ADVISORY tile_stats_sample_size_significance/overall:** 16 steps and 27.1 estimated minutes significantly exceed the 8–14 step / 6–12 minute guideline. The tile covers three substantial statistical concepts with two video steps. Consider splitting into two tiles (e.g., sample size + significance in one, business conclusions in another) to improve pacing.

2. **ADVISORY tile_capstone_question_workflow/overall:** 14 steps and 16.2 estimated minutes exceed the time guideline. Consider tightening or splitting.

3. **ADVISORY tile_stakeholder_prioritizing_framing_context/overall:** 13.0 estimated minutes slightly exceeds the 6–12 minute guideline. Minor.

4. **ADVISORY tile_stakeholder_prioritizing_framing_context/s05:** Ordering item `item_kano_var` text "Kano has notable delivery-time variability across all three cities" is ambiguous — reads as if Kano's variability extends across all three cities. → Reword to "Kano has the most notable delivery-time variability of the three cities" or "Delivery-time variability is highest in Kano among the three cities."

5. **ADVISORY tile_stats_sample_size_significance/s01:** The lesson consistently says "10% lift" while the registry data shows 9.8%. The glossary teaching blocks also use "10% lift," so this is a deliberate pedagogical rounding. Consider adding "roughly 10%" or "about 10%" for precision.

6. **ADVISORY tile_stakeholder_prioritizing_framing_context/overall and tile_capstone_execution_narration_delivery/overall:** Neither tile includes a video step. The evaluator checklist mentions "the video step adds something the text doesn't repeat" — these tiles have no video to evaluate. Not a defect per se, but noted.

---

## Summary

All four tiles follow the explain → check → apply flow correctly. No check arrives before its idea is taught. Each step teaches one idea. Remediation steps address the specific mistake in every case. Visuals support the text and are not decorative. Wrong-option feedback is accurate and addresses the specific error in each case. All facts taught are traceable to the glossary bundle. No learner would be unable to succeed from what was taught.

The primary concern is pacing: the stats tile is roughly 2× the recommended length, and two other tiles also exceed the time guideline. These are advisory issues — they affect learner experience but do not prevent learning.

VERDICT: PASS
