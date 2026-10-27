# Stage 04 Interactions — Scoped Re-evaluation (c1)

## Scope
Re-evaluation after repair of two BLOCKING and four ADVISORY findings.

## Repair 1: tile_capstone_question_workflow/s08 — `item_csv_trap` removal
**Status: RESOLVED.** The `item_csv_trap` item has been completely removed from both the `items` list and `grading.assignments`. The interaction now contains exactly four items (2 SQL database sources, 2 Excel workbook sources), all correctly assigned to their respective buckets. The associated ADVISORY about `pandas.read_csv()` is also resolved since that content is gone.

## Repair 2: tile_stats_sample_size_significance/s09 — CI interpretation task
**Status: PARTIALLY RESOLVED (now ADVISORY).** A third task (`task_ci_interpretation`) has been added. The task prompt contains the correct repeated-sampling interpretation of 95% confidence ("if this procedure were applied to many independent samples, about 95% of the resulting intervals would contain the true parameter — not that there is a 95% probability this specific interval contains it"). The correct/incorrect feedback reinforces this interpretation. The overall feedback and hints also correctly state the long-run behaviour interpretation.

However, the task's mechanical action (selecting the ci_lower cell) does not require the learner to *demonstrate* understanding of the repeated-sampling interpretation — the correct interpretation is given in the prompt itself, and the learner merely clicks a cell. A learner who ignores the interpretation text can still succeed by locating the correct cell. Within the table_select format this is a reasonable best-effort, so I downgrade from BLOCKING to ADVISORY.

## Previously noted ADVISORYs
- tile_stats_sample_size_significance/s02: "9.8% lift" vs "10% lift" discrepancy — unchanged, still advisory.
- tile_capstone_execution_narration_delivery/s02: title mismatch — unchanged, still advisory.
- tile_stats_sample_size_significance/s09 measures metadata: `distinguish_statistical_significance_from_practical_significance` is listed in measures but not tested by any of the three tasks — unchanged, still advisory.

## Structural integrity
- JSON is valid.
- Three tiles present with correct tile_ids.
- Interaction counts: 8 + 7 + 6 = 21 total.
- No unrelated content was altered.

---

VERDICT: PASS

ADVISORY tile_stats_sample_size_significance/s09 (table_select): task_ci_interpretation embeds the correct repeated-sampling interpretation in the prompt but the learner's action (cell selection) does not require demonstrating that understanding; the task reads-and-acknowledges rather than exercises the concept. → Consider converting task 3 to a choice or external_proof that requires the learner to select or produce the correct interpretation of "95% confidence."
ADVISORY tile_stats_sample_size_significance/s09: Measures metadata lists `distinguish_statistical_significance_from_practical_significance` but none of the three table_select tasks test this capability. → Remove this capability from the s09 measures or add a task that exercises it.
ADVISORY tile_stats_sample_size_significance/s02: Prompt uses "9.8% lift" but the preceding explainer (s01) consistently uses "10% lift"; the unexplained change may confuse learners. → Align the lift figure with the registry data (9.8%) or the explainer (10%) consistently.
ADVISORY tile_capstone_execution_narration_delivery/s02: Lesson step title ("What Belongs in the Decision Log?") slightly mismatches the interaction's broader focus on monitoring and recording during the analysis phase; content is sound.
