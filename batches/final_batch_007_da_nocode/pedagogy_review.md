# Pedagogy Review — `final_batch_007_da_nocode`

**Evaluator:** independent (stage 08)
**Tiles reviewed:** `tile_data_quality_and_workflow`, `tile_stakeholder_framing_requirements`

---

## Tile 1: `tile_data_quality_and_workflow`

### Explain → Check → Apply flow
- **Concept `data.data_quality_basics`:** Explained in s01 (fitness for purpose, completeness, uniqueness) and s03 (validity, accuracy, good-enough data). Checked in s04 (uniqueness/fitness) and s05 (validity vs accuracy). Applied in s06 (find_issues hands-on). ✅ Correct order.
- **Concept `data.analysis_workflow`:** Explained in s07 (six stages + process_flow diagram), s09 (analyze, visualize), s10 (communicate, iterative). Checked in s11 (iterative loop-back). Applied in s12 (ordering). ✅ Correct order.
- **Concept `data.ethics_privacy_basics`:** Explained in s13 (privacy, minimal collection, impact) and s14 (honest reporting, re-identification). Checked in s15 (remove PII) and s16 (limitations + re-identification). Applied in s17 (table_select columns). ✅ Correct order.

### One idea per step
All non-recap steps have a single concept_id. Step s05 tests two capabilities (distinguish_invalid_from_inaccurate + recognize_good_enough_data) in one compound question, but both are within the same concept and were taught in s03. Borderline but acceptable.

### Reading load
All explainer steps are under 800 characters of prose. Reasonable.

### Difficulty ramp
Each concept block follows intro-difficulty checks before core-difficulty hands-on. ✅

### Remediation quality
- r01 (completeness/uniqueness) addresses the specific mistake in s04/s06 with a concrete contrast and data table. ✅
- r02 (validity vs accuracy) addresses the specific mistake in s05 with a clear contrast. ✅
- r03 (iterative workflow) addresses the specific mistake in s11/s12. ✅
- r04 (privacy/minimal collection) addresses the specific mistake in s15/s17. ✅
- r05 (honest reporting/re-identification) addresses the specific mistake in s16. ✅

### Visuals
- s01 data_table with highlighted quality problems earns its place — directly supports the prose. ✅
- s07 process_flow diagram of six stages earns its place. ✅
- s02 and s08 video steps have bridge text that adds value (notes where video differs from Devspace model). ✅

### Step count and pacing
- **18 main steps** (guideline: 8–14). Exceeds guideline.
- **25.0 estimated minutes** (guideline: 6–12). Exceeds guideline significantly.
- The tile covers 3 concepts, each with a full explain→video→explain→check→check→hands_on cycle. The structure is internally consistent but the tile is long.

### Fact coverage
All required facts (f1–f5, m1 for data_quality_basics; f1–f7 for analysis_workflow; f1–f5, m1 for ethics_privacy_basics) are taught in explainer steps before being tested. ✅

---

## Tile 2: `tile_stakeholder_framing_requirements`

### Explain → Check → Apply flow
- **Concept `stakeholder.identifying_decision_need`:** Explained in s01. Checked in s02. Applied in s03 (table_select). ✅
- **Concept `stakeholder.precise_finding_statement`:** Explained in s04 (big idea) and s05 (specific + comparison). Checked in s06 (narrow claim). Applied in s07 (external_proof write). ✅
- **Concept `stakeholder.framing_analytical_question`:** Explained in s08 (scoping conversation) and s09 (output agreement). Checked in s10 (well-formed question) and s11 (output agreement). Applied in s12 (classify). ✅
- **Concept `stakeholder.identifying_requirements`:** Explained in s13 (commissioner inputs, data sources) and s14 (constraints, specification document). Checked in s15 (commissioner vs analyst roles) and s16 (timeline + output). Applied in s17 (table_select). ✅

### One idea per step
All non-recap steps have a single concept_id. ✅

### Reading load
All explainer steps are under 860 characters of prose. Reasonable.

### Difficulty ramp
Each concept block follows intro-difficulty checks before core-difficulty hands-on. ✅

### Remediation quality
- r01 (decision behind request) addresses the specific mistake in s02. ✅
- r02 (narrow claim to match data) addresses the specific mistake in s06. ✅
- r03 (precise finding with number and comparison) addresses the specific mistake in s07. ✅
- r04 (well-formed statistical question) addresses the specific mistake in s10. ✅
- r05 (output agreement) addresses the specific mistake in s11. ✅
- r06 (commissioner inputs + specification) addresses the specific mistake in s15. ✅
- r07 (resource constraints + output agreement) addresses the specific mistake in s16. ✅
- s03, s12, s17 (hands_on) have no remediation_step_id but do have incorrect feedback and hints. Acceptable.

### Visuals
- s04 before_after diagram (vague label → precise finding) earns its place. ✅
- s08 before_after diagram (vague question → measurable question) earns its place. ✅
- s13 process_flow diagram (engagement and scoping exchange) earns its place. ✅

### Step count and pacing
- **18 main steps** (guideline: 8–14). Exceeds guideline.
- **16.8 estimated minutes** (guideline: 6–12). Exceeds guideline.
- The tile covers 4 concepts, each with a full explain→check→hands_on cycle. The structure is internally consistent but the tile is long.

### Fact coverage
All required facts (f1–f2 for identifying_decision_need; f2–f5 for precise_finding_statement; f1–f3 for framing_analytical_question; f1–f5 for identifying_requirements) are taught in explainer steps before being tested. ✅

---

## Summary of findings

### BLOCKING defects
None found. All facts are accurately represented, all checks test ideas that were previously taught, all remediation steps address the specific mistakes, all wrong-option feedback is factually correct, and no visual contradicts the text.

### ADVISORY defects

1. **ADVISORY tile_data_quality_and_workflow/pacing:** 18 steps and 25.0 estimated minutes exceed the 8–14 step / 6–12 minute guideline. Consider splitting into two tiles (e.g., data quality + workflow/ethics) or trimming the double-check pattern per concept. → Reduce to ≤14 steps and ≤12 minutes, or split the tile.

2. **ADVISORY tile_stakeholder_framing_requirements/pacing:** 18 steps and 16.8 estimated minutes exceed the 8–14 step / 6–12 minute guideline. Consider splitting into two tiles (e.g., decision+finding vs question+requirements) or trimming. → Reduce to ≤14 steps and ≤12 minutes, or split the tile.

3. **ADVISORY tile_data_quality_and_workflow/s05:** The check question tests two capabilities (distinguish_invalid_from_inaccurate + recognize_good_enough_data) in a single compound prompt. While both are within the same concept and were taught, the compound structure may confuse a learner who gets one part right and the other wrong. → Consider splitting into two separate check questions.

4. **ADVISORY tile_stakeholder_framing_requirements/summary:** The `summary` field is an empty string. While not structurally breaking, a summary helps with tile discovery and navigation. → Add a one-sentence summary describing the tile's learning objectives.

5. **ADVISORY tile_stakeholder_framing_requirements/s01:** The explainer has three prose blocks (855 chars total) covering both the definition of analysis and the scoping stage. The step is slightly dense for an opening step. → Consider splitting the definition (f1) and the scoping mechanism (f2) into two steps.

---

VERDICT: PASS
