# Evaluation Report — Stage 03 Screens, Chunk c1

**Batch:** `final_batch_004_da_chunk2`  
**Tiles evaluated:** `tile_stats_sample_size_significance`, `tile_capstone_question_workflow`, `tile_capstone_execution_narration_delivery`  
**Evaluator approach:** Re-derived all factual claims from the glossary bundle and scenario asset registry. Reviewed every step of all three tiles (all steps, not just a sample, given the chunk scope).

---

## Tile: tile_stats_sample_size_significance

### Steps reviewed: s01–s16, r01–r03

- **s01 (explainer, sample_size_effect_concept):** Prose blocks accurately reflect facts f1 and f2. Side-by-side diagram correctly illustrates precision difference between small and large samples. The axis label on the left panel says "(0% – 30%)" but includes a node at −2%, which is outside the stated range. Advisory only — the concept is still conveyed correctly.
- **s02 (check):** Lede and lineage correctly test f1/f2 via the assessment anchor.
- **s03 (hands_on):** Practice prompt correctly aligned with the practice anchor.
- **s04 (explainer, significance_confidence_concept):** H0/HA definition matches f1. p-value definition matches f2/f3. The 25-CI diagram matches the visual anchor purpose for this concept. Placement in the first explainer for the concept is acceptable.
- **s05 (video):** Segment reference present; lede does not require video to make sense.
- **s06 (explainer, significance_confidence_concept):** CI definition matches f4. Misconception callout (c1) matches f5. Misconception callout (c2) matches m1 (25 CIs, p = 0.88, one miss). Takeaway (p2) matches f6. All accurate.
- **s07 (check):** Tests f1 via assessment anchor. Fine.
- **s08 (check):** Tests f2/f3 via assessment anchor. Fine.
- **s09 (hands_on):** Tests f4/f5/f6/m1 via practice and assessment anchors. Fine.
- **s10 (explainer, business_conclusion_from_experiment):** Definition block accurately reflects f1 (null value concept) and mentions p0 = 0.333 from f2/f3. Mechanism block accurately describes the two textbook examples per f2 and f3. Number-line diagram uses illustrative CI bounds ([0.28, 0.39] and [0.21, 0.31]) that differ from the registry's test_prop_A/B data ([0.22, 0.5] and [0.09, 0.31]), but the diagram is labeled as "Scenario A" and "Scenario B" (not as the registry rows), and the qualitative conclusions (null inside/outside) are correct. Advisory — the diagram could use the registry's actual CI bounds for consistency.
- **s11 (explainer, business_conclusion_from_experiment):** Misconception callout matches f6 and m1. Example block matches f4. Takeaway matches f5 including the 0.001% movie-ad example. All accurate.
- **s12 (video):** Segment reference present; lede standalone.
- **s13 (check):** Tests f1 via assessment anchor. Fine.
- **s14 (check):** Tests f5 via assessment anchor. Fine.
- **s15 (hands_on):** Tests f2/f3/f4/f6/m1 via practice and assessment anchors. Fine.
- **s16 (recap):** Takeaway accurately summarizes key facts from all three concepts. Up-next text references the next tile's topics without requiring understanding of them.
- **r01–r03 (remediation):** All accurately restate the relevant facts for their respective concepts.

**No blocking defects in this tile.**

---

## Tile: tile_capstone_question_workflow

### Steps reviewed: s01–s13, r01–r03

- **s01 (explainer, defining_business_question):** Prose matches f1/f2. Before/after diagram correctly shows vague complaint → scoped question with context and boundaries. Matches visual anchor.
- **s02 (explainer, defining_business_question):** Example block matches f1/f2 via tb3. Accurate.
- **s03 (check):** Tests f1/f2 via assessment anchor. Fine.
- **s04 (hands_on):** Practice prompt aligned with practice anchor. Fine.
- **s05 (explainer, data_retrieval_method_selection):** SQL query for database matches f1. read_excel() for Excel matches f2. Side-by-side diagram correctly maps each source to its tool. Column names in diagram match registry (zone, driver_id, delivery_time_min, order_date for orders; driver_id, name, zone, shift for drivers). All accurate.
- **s06 (video):** Segment references present; lede standalone.
- **s07 (check):** Tests f1/f2 via assessment anchor. Fine.
- **s08 (hands_on):** Tests f1/f2 via practice and assessment anchors. Fine.
- **s09 (explainer, end_to_end_workflow_structure):** Mechanism blocks match f1 (phases, revisiting) and f2 (quality assessment early). Process flow diagram shows six stages with back-arrow from Clean/Model to Scope. Matches visual anchor.
- **s10 (explainer, end_to_end_workflow_structure):** Modeling stage matches f3 (relationships connect related tables, driver_id as join key). Delivery/communication stage matches f4 (commissioner and approver, summary packs/reports/presentations). Accurate.
- **s11 (check):** Tests f1/f2/f3/f4 via assessment anchor. Fine.
- **s12 (check):** Tests f1 via assessment anchor. Fine.
- **s13 (hands_on):** Tests f1/f2/f3/f4 via practice and assessment anchors. Fine.
- **r01–r03 (remediation):** All accurately restate relevant facts.

**No blocking defects in this tile.**

---

## Tile: tile_capstone_execution_narration_delivery

### Steps reviewed: s01–s11, r01–r03

- **s01 (explainer, independent_execution):** Prose blocks match f1 (design phase, commission → analytical plan, iteration) and f2 (analysis phase, monitoring, decision log). Process flow diagram correctly shows two phases with iteration loop. Matches visual anchor.
- **s02 (check):** Tests f2 via assessment anchor. Fine.
- **s03 (hands_on):** Tests f1/f2 via practice and assessment anchors. Fine.
- **s04 (explainer, narrated_stakeholder_summary):** Mechanism block matches f1 (specific person, audience motivation). Before/after diagram uses registry data accurately (Lagos-North: avg 32.9 min, 0% on time, gap 7.9 min; Lagos-South: avg 29.0 min, 0% on time, gap 4.0 min; Kano-Central: avg 26.0 min, 33% on time, gap 1.0 min; Abuja-West: avg 22.6 min, 100% on time). All match ds_capstone_zone_summary. Narrated summary correctly structures beginning/middle/end per f3.
- **s05 (explainer, narrated_stakeholder_summary):** Block p1 matches f3 (beginning/middle/end structure). Block p2 matches f2 (delivery sufficiency standard). **Block p3 lineage references `capstone.narrated_stakeholder_summary#f4`, which does not exist** — the concept only has facts f1, f2, f3. The text content of p3 is accurate (it paraphrases tb5 and reflects f2/f3), but the lineage metadata is broken. **Also, the step-level lineage at line 2567 repeats this non-existent f4 reference.**
- **s06 (check):** Tests f2 via assessment anchor. Fine.
- **s07 (hands_on):** Tests f1/f2/f3 via practice and assessment anchors. Fine.
- **s08 (explainer, documenting_presenting_deliverable):** Block p1 matches f1 (transparency, documentation). Block p2 matches f2 (delivery activities). Process flow diagram matches visual anchor (documentation layer → delivery layer). Accurate.
- **s09 (check):** Tests f1 via assessment anchor. Fine.
- **s10 (hands_on):** Tests f1/f2 via practice and assessment anchors. Fine.
- **s11 (recap):** Takeaway accurately summarizes key facts from all three concepts.
- **r01–r03 (remediation):** All accurately restate relevant facts.

### Defect: Non-existent fact reference in lineage

**Step s05 (block p3 and step-level lineage):** References `capstone.narrated_stakeholder_summary#f4`, but the concept only defines facts f1, f2, f3. This is a data-integrity break in the lineage metadata. The teaching text itself is correct.

---

## Summary of Defects

| # | Severity | Location | Description | Fix |
|---|----------|----------|-------------|-----|
| 1 | BLOCKING | tile_capstone_execution_narration_delivery/s05 | Block p3 lineage and step-level lineage reference `capstone.narrated_stakeholder_summary#f4`, which does not exist (concept has only f1, f2, f3). | Remove `"capstone.narrated_stakeholder_summary#f4"` from the `fact_ids` array in both the block-level lineage (line 2548) and the step-level lineage (line 2567). The text content is correct and already covered by f2 and f3. |
| 2 | ADVISORY | tile_stats_sample_size_significance/s01 | Side-by-side left panel axis label says "(0% – 30%)" but includes a node at −2%, outside the stated range. | Change axis label to "Lift estimate axis (−5% – 30%)" or similar range that encompasses all nodes. |
| 3 | ADVISORY | tile_stats_sample_size_significance/s10 | Number-line diagram uses illustrative CI bounds ([0.28, 0.39] and [0.21, 0.31]) that differ from the registry's test_prop_A/B data ([0.22, 0.5] and [0.09, 0.31]). Qualitative conclusions are correct but values could be more consistent with the registry. | Consider using the registry's actual CI bounds for Scenario A (0.22–0.50) and Scenario B (0.09–0.31) to maintain consistency with the dataset. |
| 4 | ADVISORY | tile_stats_sample_size_significance/s04 | The 25-CI diagram is placed in the H0/HA/p-value step rather than the CI step (s06), which is where the CI content is taught. | Consider moving the 25-CI diagram to s06 where confidence intervals are explained, or adding a brief forward reference. |

---

VERDICT: FAIL

BLOCKING tile_capstone_execution_narration_delivery/s05: Block p3 lineage and step-level lineage reference non-existent `capstone.narrated_stakeholder_summary#f4` (concept only has f1, f2, f3) → Remove `"capstone.narrated_stakeholder_summary#f4"` from the `fact_ids` array in both the block-level lineage (block tile_capstone_execution_narration_delivery.s05.p3) and the step-level lineage of step s05. The existing f2 and f3 references already cover the text content.
ADVISORY tile_stats_sample_size_significance/s01: Left-panel axis label says "(0% – 30%)" but includes a −2% node outside that range → Change label to "Lift estimate axis (−5% – 30%)" or a range encompassing all nodes.
ADVISORY tile_stats_sample_size_significance/s10: Diagram CI bounds differ from registry test_prop_A/B data though qualitative conclusions are correct → Use registry CI bounds [0.22, 0.50] and [0.09, 0.31] for consistency.
ADVISORY tile_stats_sample_size_significance/s04: 25-CI diagram placed in H0/HA step rather than CI step (s06) → Consider relocating to s06 or adding a forward reference.
