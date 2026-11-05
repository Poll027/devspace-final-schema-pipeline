# Pedagogy Review — tile_stakeholder_chart_matching_simplifying

**Reviewer:** Independent Evaluator (Stage 08)  
**Tile:** `tile_stakeholder_chart_matching_simplifying`  
**Concepts:** `stakeholder.chart_type_to_point_matching`, `stakeholder.simplifying_charts_for_audience`  
**Steps:** 11 main + 4 remediation  
**Estimated time:** 17.8 minutes

---

## 1. Explain → Check → Apply Flow

**Concept 1 — chart_type_to_point_matching:**
- s01 (explainer): bar, line, boxplot introduced with scenario context
- s02 (video): two clips — bar vs. pie comparison, boxplot audience risk
- s03 (explainer): pie chart part-to-whole, scatterplot exploratory vs. communicative, pie-slice misconception
- s04 (check): scatterplot exploratory vs. communicative — tests f6, taught in s03
- s05 (hands_on): classify four stakeholder points to chart types — tests f1–f6

✅ Every idea is taught before it is checked. Flow is sound.

**Concept 2 — simplifying_charts_for_audience:**
- s06 (explainer): gridlines, border, data labels, trailing zeros, rotated labels, before/after diagram
- s07 (video): live Excel declutter demo covering f2–f6; bridge notes f1 gap
- s08 (check): which elements to remove — tests f1–f6
- s09 (check): why remove border — tests f2
- s10 (hands_on): classify 6 elements as remove/keep — tests f1, f3, f5, f6
- s11 (recap): both concepts summarised

✅ Every idea is taught before it is checked. Flow is sound.

## 2. One Idea per Step

All steps focus on a single concept. s03 covers three sub-topics (pie, scatterplot, misconception) but they are all facets of the same concept (chart_type_to_point_matching) and are presented in separate prose blocks. Acceptable.

## 3. Dead Text / Reading Load

Prose blocks are concise and scenario-grounded. No filler paragraphs detected. Each block teaches or reinforces a specific fact.

## 4. Difficulty Ramp

Concept 1 ramps from recognition (s04 single-choice on scatterplots) to application (s05 classify four items into four buckets). Concept 2 ramps from recognition (s08 single-choice, s09 single-choice) to application (s10 classify six items into two buckets). Appropriate progression.

## 5. Remediation Quality

- r01 (for s04): re-explains scatterplot exploratory vs. communicative — directly addresses the mistake. ✓
- r02 (for s05): re-explains all chart-type-to-point mappings plus pie-slice misconception — directly addresses the mistake. ✓
- r03 (for s10): re-explains all clutter elements — directly addresses the mistake. ✓
- r04 (for s09): re-explains border removal and white space — directly addresses the mistake. ✓

## 6. Visuals

- s01 side-by-side (bar chart vs. line graph): supports the text, earns its place. ✓
- s03 chart (pie chart of order share): supports part-to-whole teaching. ✓
- s06 before/after diagram: illustrates clutter removal. ✓
- s02 and s07 video segments: add demonstration the text can't replicate. ✓

## 7. Video Steps

- s02: two clips covering bar-vs-pie comparison and boxplot audience risk. Bridge notes what the video covers (f1, f3, f5) and what it doesn't (f4, f6). Adds visual demonstration the text can't replicate. ✓
- s07: one clip covering live Excel declutter. Bridge notes f1 gap. Adds hands-on demonstration. ✓

## 8. Step Count and Pacing

- Steps: 11 (within 8–14 range) ✓
- Estimated minutes: 17.8 (exceeds 6–12 minute guideline by ~50%) ⚠️

---

## Findings

ADVISORY tile_stakeholder_chart_matching_simplifying/s01: The line chart in the side-by-side block (b3) references `ds_weekly_delivery_trend` without a filter, but the title says "Weeks 1–3" and the alt text describes only weeks 1–3. The dataset contains 4 weeks and 3 cities; the chart encoding maps color to city. A renderer would show all 4 weeks for all 3 cities, contradicting the title and alt text. → Add a filter to restrict to city="Lagos" and week_number ≤ 3, or update the title/alt text to reflect the full dataset ("Weeks 1–4, all cities" or similar).

ADVISORY tile_stakeholder_chart_matching_simplifying/s06: The "after" diagram node shows "Axis labels: 22, 27, 38 min" but the actual data values are 22.0, 27.2, 38.4. The glossary fact f5 teaches dropping *trailing zeros* (e.g. 22.00 → 22), not rounding non-zero decimals (27.2 → 27, 38.4 → 38). The diagram implies rounding is part of the simplification, which goes beyond what f5 teaches. → Update the "after" axis labels to values consistent with trailing-zero removal (e.g. "22, 27.2, 38.4 min") or acknowledge that the axis shows approximate values.

ADVISORY tile_stakeholder_chart_matching_simplifying/pacing: Estimated time is 17.8 minutes, exceeding the 6–12 minute guideline. The tile covers two concepts with two video steps, two check steps, and two hands-on steps. → Consider whether the tile could be split or whether the time estimate can be reduced (e.g., shorter video segments).

ADVISORY tile_stakeholder_chart_matching_simplifying/s10: Item 6 ("Axis title showing 'Delivery Time (min)'") is graded as "Keep" but axis titles are never explicitly discussed in the teaching material (s06) or the glossary. The learner must infer that axis titles are essential by reasoning that the glossary only lists what to remove. → Add a brief mention in s06 that axis titles provide essential context and should be kept.

---

## Verdict

No blocking defects found. The explain → check → apply flow is sound for both concepts. All checks arrive after their ideas are taught. Remediation addresses specific mistakes. Visuals support the text. Four advisory items noted above.

**VERDICT: PASS**
