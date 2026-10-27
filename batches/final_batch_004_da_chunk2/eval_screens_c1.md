# Evaluation Report — 03_screens, chunk c1

**Batch:** `final_batch_004_da_chunk2`  
**Tiles evaluated:** `tile_stats_sample_size_significance`, `tile_capstone_question_workflow`, `tile_capstone_execution_narration_delivery`  
**Steps reviewed:** ~60% across all three tiles (s01–s04, s06, s10–s11, s13–s16, r01–r03 of tile 1; s01–s05, s09–s14, r01–r03 of tile 2; s01–s02, s04–s05, s07–s11, r01–r03 of tile 3)

---

## Findings

### ADVISORY defects

1. **tile_stats_sample_size_significance/s04 (diagram):** The 25-CI strip diagram is placed in a step titled "Hypotheses, p-Values, and Statistical Significance" before confidence intervals are taught (s06). The diagram's lineage claims it teaches tb2 (H0/HA) and tb3 (p-value), but the diagram content illustrates misconception m1 (CI capture). While the visual anchor belongs to the concept as a whole and the learner will encounter the CI explanation two steps later, placing it here before CIs are introduced is pedagogically premature. Consider moving the diagram to s06 or adding a brief forward-reference sentence.

2. **tile_stats_sample_size_significance/s06.c1:** The callout omits the glossary f5 hedge "while it may be useful to think of it that way, the confidence level only quantifies how plausible it is that the parameter is in the given interval." The screen's version is more absolute in rejecting the probability framing. The omission doesn't introduce a false claim but drops a nuance from the source.

3. **tile_stats_sample_size_significance/s06.p2:** The takeaway about statistical vs. practical significance (f6) is placed in a step titled "What a Confidence Interval Actually Means." While f6 belongs to the same concept, the placement feels thematically disconnected from the step's CI focus.

4. **tile_capstone_execution_narration_delivery/s04.v1 (before_after):** Kano-Central's on-time percentage is shown as "33%" while the registry value is 33.3%. Minor rounding, not misleading.

5. **tile_capstone_question_workflow/s14.p1 (recap):** The recap says "any stage open to revisiting" while glossary f1 says "a phase such as scoping or design may need to be revisited." The glossary uses "such as" (implying examples), so the generalization is defensible but slightly broader than the source.

### No BLOCKING defects found

All required facts for each concept are taught in the tile's explainer steps. Prose blocks faithfully reproduce glossary facts with appropriate contextual substitutions (e.g., "cases" → "orders or users"). Registry data (zone summaries, column names, scenario details) is accurately reflected. No step requires understanding of a blocked_future_concept. No remediation teaches anything false. Visual anchors serve their stated purposes within the concept's step sequence. Check and hands_on steps test only taught content.

---

## VERDICT: PASS

ADVISORY tile_stats_sample_size_significance/s04 (diagram): 25-CI diagram placed before CIs are taught in s06; lineage claims tb2/tb3 but content illustrates m1 → move diagram to s06 or add a forward-reference sentence  
ADVISORY tile_stats_sample_size_significance/s06.c1: omits f5 hedge "while it may be useful to think of it that way, the confidence level only quantifies how plausible it is that the parameter is in the given interval" → consider restoring the hedge  
ADVISORY tile_stats_sample_size_significance/s06.p2: statistical-vs-practical-significance takeaway placed in a CI-focused step → consider moving to a separate step or the recap  
ADVISORY tile_capstone_execution_narration_delivery/s04.v1: Kano-Central on-time shown as "33%" vs registry "33.3%" → change to "33.3%"  
ADVISORY tile_capstone_question_workflow/s14.p1: "any stage open to revisiting" slightly broader than glossary's "a phase such as scoping or design may need to be revisited" → consider "stages such as scoping open to revisiting"
