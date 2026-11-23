# EVALUATOR PACKET — Comparable production distributions (mle.tile.080_082)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.distribution_monitoring — Monitor production input and prediction distributions
B = mle.drift_degradation_distinction — Distinguish data drift, concept drift and observed quality degradation
C = mle.data_drift_detection — Detect model-input data drift against a defined reference distribution

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=9
  warn: remediation step mle.tile.080_082.r02 is never referenced
  warn: remediation step mle.tile.080_082.r04 is never referenced
  warn: remediation step mle.tile.080_082.r06 is never referenced
  warn: mle.tile.080_082.s01: prose block without lineage.fact_ids
  warn: mle.tile.080_082.s04/ix.mle.tile.080_082.s04: ADVISORY — syntax descriptors with no detector: ['arithmetic operators', 'array comparisons', 'array indexing and Boolean masks', 'for loops', 'function parameters and calls', 'if statements', 'imports for client dependencies identified by the supplied scaffolding', 'len', 'lists and dictionaries', 'numeric and string literals', 'summary-emission calls defined by the supplied client contract']
  warn: mle.tile.080_082.s05: prose block without lineage.fact_ids
  warn: mle.tile.080_082.s10: prose block without lineage.fact_ids
  warn: mle.tile.080_082.s14/ix.mle.tile.080_082.s14: ADVISORY — syntax descriptors with no detector: ['Array indexing and Boolean masks', 'Calls to supplied infrastructure interfaces', 'Comparison operators', 'Elementwise arithmetic and broadcasting', 'Imports for required dependencies explicitly identified by the supplied infrastructure scaffolding', 'Lists and dictionaries', 'Variable assignment', 'def with parameters']
  warn: mle.tile.080_082.s15: prose block without lineage.fact_ids

## SOURCE FACTS — A (mle.distribution_monitoring)   objective: Summarize aligned reference and production input/output distributions over a defined window.
A.f1: Compare captured production inputs with the defined reference dataset using the same feature representations, reference constraints and measurement window.   [sources: sagemaker_model_monitor#model-monitor-data-quality.html — Monitor data quality]
A.f2: For numerical values, np.histogram(values, bins=fixed_edges) returns bin counts; divide by the eligible observation count to compare bin proportions on the same edges.   [sources: numpy_user_guide#reference/generated/numpy.histogram.html — Parameters; Returns]
A.f3: For categorical or predicted-class values, count each declared category and divide by its window total, retaining category definitions and the total count.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
A.f4: Record the production window, reference identity and observed summaries so an apparent distribution change can be investigated.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/observability — Establish robust observability]
A.f5: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
A.f6: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Monitor Distributions and Drift.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: none within this path. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python function that summarizes one bounded production stream within supplied infrastructure scaffolding. Write imports for NumPy and the supplied summary-emission client. Apply the declared window, reference constraints and representations; calculate numerical bin proportions, means, standard deviations and empirical probabilities for declared input categories and predicted classes. Emit one monitoring summary record.  SUCCESS: The emitted record identifies the production window and reference, retains fixed bin edges and declared category definitions, includes eligible totals and correctly normalized proportions, and reports numerical means and standard deviations using the specified divisor. It is the single monitoring deliverable.
ASSESSMENT ANCHOR: define_and_record_comparable_production_windows facts=['f1', 'f4']
ASSESSMENT ANCHOR: calculate_aligned_numerical_bin_proportions facts=['f2']
ASSESSMENT ANCHOR: calculate_declared_category_and_prediction_probabilities facts=['f3']
ASSESSMENT ANCHOR: calculate_windowed_mean_and_standard_deviation facts=['f5', 'f6']

## SOURCE FACTS — B (mle.drift_degradation_distinction)   objective: Distinguish input shift, changed target relationship and label-supported quality degradation.
B.f1: Input data drift is a change in the observed input distribution relative to its reference; input drift monitoring alone does not measure labeled prediction quality.   [sources: sagemaker_model_monitor#model-monitor-data-quality.html — Monitor data quality]
B.f2: Concept drift changes the conditional target relationship P(Y|X), that is, the relationship between features and labels; a previously useful model can become less useful as that relationship changes.   [sources: google_ml_crash_course#https://developers.google.com/machine-learning/glossary — concept-drift; discriminative-model]
B.f3: Observed model quality degradation requires comparing predictions with corresponding ground-truth labels and the declared quality reference.   [sources: sagemaker_model_monitor#model-monitor-model-quality.html — Monitor model quality]
B.f4: Without matched available labels, report the supported distribution or service evidence and the unresolved quality question rather than asserting labeled quality degradation.   [sources: sagemaker_model_monitor#model-monitor-model-quality-merge.html — Ingest Ground Truth labels and merge them with predictions]
B.f5: Input marginals describe P(X), conditional-target evidence describes P(Y|X), and matched-label errors describe observed quality; changing one does not logically establish changes in all three.   [sources: google_ml_crash_course#https://developers.google.com/machine-learning/glossary — concept-drift; discriminative-model, sagemaker_model_monitor#model-monitor-data-quality.html — Monitor data quality, sagemaker_model_monitor#model-monitor-model-quality.html — Monitor model quality]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Monitor Distributions and Drift.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (matching): Classify three supplied order-prediction scenarios as input shift, conditional-target change or observed quality loss. Use evidence about P(X), P(Y|X), or predictions matched to ground-truth labels and a declared quality reference; state which further conclusions remain unsupported.  SUCCESS: Each scenario is matched to the evidence-supported category. The learner distinguishes a changed input distribution from a changed feature–label relationship and measured quality loss, requires matched labels and a declared quality reference for the quality-loss claim, and does not infer changes in all three from evidence about only one.
ASSESSMENT ANCHOR: identify_input_distribution_shift facts=['f1', 'f5']
ASSESSMENT ANCHOR: identify_conditional_target_change facts=['f2', 'f5']
ASSESSMENT ANCHOR: identify_observed_quality_degradation facts=['f3', 'f5']
ASSESSMENT ANCHOR: state_unsupported_quality_and_drift_conclusions facts=['f4', 'f5']

## SOURCE FACTS — C (mle.data_drift_detection)   objective: Detect a defined feature-distribution difference using aligned proportions and numeric summaries.
C.f1: Define the reference feature distribution, comparison window and declared drift criterion before checking production data.   [sources: sagemaker_model_monitor#model-monitor-data-quality.html — Monitor data quality]
C.f2: Use identical bin edges and category mappings for reference and observed data, then compute proportions from their own eligible observation totals.   [sources: numpy_user_guide#reference/generated/numpy.histogram.html — Parameters; Returns]
C.f3: Compare the observed distribution/statistics with the reference under the supplied significance or threshold rule and report which features cross it.   [sources: sagemaker_model_monitor#model-monitor-data-quality.html — Monitor data quality]
C.f4: A drift detection result indicates a distribution difference under that rule, not by itself a measured increase in target prediction error.   [sources: sagemaker_model_monitor#model-monitor-data-quality.html — Monitor data quality]
C.f5: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
C.f6: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
C.f7: Compute each category’s reference/current count divided by its own window total, then apply the supplied probability-distance equation and threshold to aligned category vectors.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Monitor Distributions and Drift.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.distribution_monitoring, mle.drift_degradation_distinction. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write the required imports and a learner-defined Python function that checks supplied reference and current samples within the existing infrastructure scaffolding. Calculate numeric means and standard deviations using the declared divisor, calculate aligned category probabilities using each window's eligible total, and apply the supplied numeric and probability-distance rules. Return feature-level verdicts with the reference identity, comparison window and criteria, without claiming that a crossing proves increased prediction error.  SUCCESS: The function reproduces the fixture's expected numeric summaries, aligned category probabilities, probability distance and feature-level threshold decisions. It preserves the supplied bin edges, category mapping, eligibility policy and comparison definition, and describes detected drift only as a distribution difference under the declared rule.
ASSESSMENT ANCHOR: identify_valid_reference_window_and_distribution_alignment facts=['f1', 'f2']
ASSESSMENT ANCHOR: calculate_numeric_mean_and_declared_standard_deviation facts=['f5', 'f6']
ASSESSMENT ANCHOR: calculate_aligned_category_probabilities_and_distance facts=['f2', 'f7']
ASSESSMENT ANCHOR: identify_feature_level_drift_without_inferring_quality_loss facts=['f3', 'f4']

## DATA ASSETS USED
ds.evidence_scenarios: Evidence Scenarios — columns: scenario_id(identifier), observation(text), matched_labels_available(categorical), supported_evidence(categorical), unresolved(text)
   ["input_shift","More long-distance orders than reference.",false,"P(X)","P(Y|X) and labeled quality are not established."]
   ["conditional_shift","Within the same distance categories, the feature-label relationship differs from reference.",true,"P(Y|X)","An input-marginal shift or quality degradation is not established by this alone."]
   ["observed_quality","Matched-label errors exceed the declared quality reference on the same cohort.",true,"matched_label_errors","Input or conditional relationship change is not established by this alone."]
ds.production: Production — columns: numeric_values(numerical), category(categorical), predicted_class(categorical)
   [1.0,"short_distance","late"]
   [2.0,"short_distance","on_time"]
   [3.0,"short_distance","on_time"]
   [4.0,"short_distance","on_time"]
   [5.0,"short_distance","late"]
   [6.0,"short_distance","on_time"]
   [7.0,"short_distance","on_time"]
   [8.0,"short_distance","on_time"]
ds.reference: Reference — columns: numeric_values(numerical), category(categorical), predicted_class(categorical)
   [1.0,"short_distance","late"]
   [2.0,"short_distance","on_time"]
   [3.0,"short_distance","on_time"]
   [4.0,"short_distance","on_time"]
   [5.0,"short_distance","late"]
   [6.0,"short_distance","on_time"]
   [7.0,"short_distance","on_time"]
   [8.0,"short_distance","on_time"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute training and inference expenditure to workloads; Choose scheduled, new-data or investigated quality/drift retraining triggers; Configure actionable model and service alerts; Detect model-input data drift against a defined reference distribution; Distinguish data drift, concept drift and observed quality degradation; Gate a retrained candidate against the incumbent using validation evidence before controlled promotion; Invoke retraining with a versioned input snapshot from an authorized trigger; Measure production model quality when labels arrive; Prevent duplicate or overlapping retraining runs; Remove model-serving resources safely on an existing platform; Set an ML workload cost guardrail on an existing platform; Track ML workload compute and memory utilization; Triage a production regression to select data repair, rollback or gated retraining; Use an ML incident runbook for safe recovery on an existing platform

## LESSON, in learner order

### s01 · explainer · Monitor production input and prediction distributions
(intro) Start with a named reference and production window. Use matching representations and categories; changed bins or inconsistent denominator rules can make the comparison misleading. ⟦A:tb1⟧
(definition) Compare captured production inputs with the defined reference dataset using the same feature representations, reference constraints and measurement window. For numerical values, np.histogram(values, bins=fixed_edges) returns bin counts; divide by the eligible observation count to compare bin proportions on the same edges. For categorical or predicted-class values, count each declared category and divide by its window total, retaining category definitions and the total count. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Record the production window, reference identity and observed summaries so an apparent distribution change can be investigated. For the arithmetic mean, use np.mean(numeric_values) on the selected numeric observations. For standard deviation, use np.std(numeric_values, ddof=0), which divides squared deviations by N and then takes the square root; use ddof=1 only if the stated calculation requires the N−1 divisor. ⟦A.f4 A.f5 A.f6 A:tb3⟧
[TABLE computed result ] caption: Aligned definitions, per-window denominators and numeric summaries; authored fictional fixture.
  produced by sql: WITH cats AS (SELECT 'short_distance' AS definition UNION ALL SELECT 'long_distance' AS definition UNION ALL SELECT 'not_reported' AS definition), classes AS (SELECT 'on_time' AS definition UNION ALL SELECT 'late' AS definition UNION ALL SELECT 'abstain' AS definition),
 eligible AS (SELECT numeric_values AS v FROM samples WHERE numeric_values BETWEEN 0 AND 10),
 summaries AS (
 SELECT 'category' AS representation, definition, COUNT(s.category) AS observations, (SELECT COUNT(*) FROM samples) AS eligible_total,
 1.0*COUNT(s.category)/(SELECT COUNT(*) FROM samples) AS proportion, NULL AS mean, NULL AS stddev, NULL AS ddof
 FROM cats LEFT JOIN samples s ON s.category=cats.definition GROUP BY definition
 UNION ALL
 SELECT 'predicted_class', definition, COUNT(s.predicted_class), (SELECT COUNT(*) FROM samples),
 1.0*COUNT(s.predicted_class)/(SELECT COUNT(*) FROM samples), NULL,NULL,NULL
 FROM classes LEFT JOIN samples s ON s.predicted_class=classes.definition GROUP BY definition
 UNION ALL
 SELECT 'numeric_bin', '[0,5)', SUM(CASE WHEN v>=0 AND v<5 THEN 1 ELSE 0 END),COUNT(*),1.0*SUM(CASE WHEN v>=0 AND v<5 THEN 1 ELSE 0 END)/COUNT(*),NULL,NULL,NULL FROM eligible UNION ALL SELECT 'numeric_bin', '[5,10]', SUM(CASE WHEN v>=5 AND v<=10 THEN 1 ELSE 0 END),COUNT(*),1.0*SUM(CASE WHEN v>=5 AND v<=10 THEN 1 ELSE 0 END)/COUNT(*),NULL,NULL,NULL FROM eligible UNION ALL SELECT 'numeric_summary','numeric_values',COUNT(*),COUNT(*),NULL,AVG(v),sqrt(GREATEST(0,AVG(v*v)-AVG(v)*AVG(v))),0 FROM eligible) SELECT 'reference' AS reference_id,'approved reference' AS measurement_window,* FROM summaries
  result columns=['reference_id', 'measurement_window', 'representation', 'definition', 'observations', 'eligible_total', 'proportion', 'mean', 'stddev', 'ddof'] rows(9)=[["reference","approved reference","category","short_distance",60,100,0.6,null,null,null],["reference","approved reference","category","long_distance",40,100,0.4,null,null,null],["reference","approved reference","category","not_reported",0,100,0,null,null,null],["reference","approved reference","predicted_class","late",25,100,0.25,null,null,null],["reference","approved reference","predicted_class","on_time",75,100,0.75,null,null,null],["reference","approved reference","predicted_class","abstain"
[TABLE computed result ] caption: Aligned definitions, per-window denominators and numeric summaries; authored fictional fixture.
  produced by sql: WITH cats AS (SELECT 'short_distance' AS definition UNION ALL SELECT 'long_distance' AS definition UNION ALL SELECT 'not_reported' AS definition), classes AS (SELECT 'on_time' AS definition UNION ALL SELECT 'late' AS definition UNION ALL SELECT 'abstain' AS definition),
 eligible AS (SELECT numeric_values AS v FROM samples WHERE numeric_values BETWEEN 0 AND 10),
 summaries AS (
 SELECT 'category' AS representation, definition, COUNT(s.category) AS observations, (SELECT COUNT(*) FROM samples) AS eligible_total,
 1.0*COUNT(s.category)/(SELECT COUNT(*) FROM samples) AS proportion, NULL AS mean, NULL AS stddev, NULL AS ddof
 FROM cats LEFT JOIN samples s ON s.category=cats.definition GROUP BY definition
 UNION ALL
 SELECT 'predicted_class', definition, COUNT(s.predicted_class), (SELECT COUNT(*) FROM samples),
 1.0*COUNT(s.predicted_class)/(SELECT COUNT(*) FROM samples), NULL,NULL,NULL
 FROM classes LEFT JOIN samples s ON s.predicted_class=classes.definition GROUP BY definition
 UNION ALL
 SELECT 'numeric_bin', '[0,5)', SUM(CASE WHEN v>=0 AND v<5 THEN 1 ELSE 0 END),COUNT(*),1.0*SUM(CASE WHEN v>=0 AND v<5 THEN 1 ELSE 0 END)/COUNT(*),NULL,NULL,NULL FROM eligible UNION ALL SELECT 'numeric_bin', '[5,10]', SUM(CASE WHEN v>=5 AND v<=10 THEN 1 ELSE 0 END),COUNT(*),1.0*SUM(CASE WHEN v>=5 AND v<=10 THEN 1 ELSE 0 END)/COUNT(*),NULL,NULL,NULL FROM eligible UNION ALL SELECT 'numeric_summary','numeric_values',COUNT(*),COUNT(*),NULL,AVG(v),sqrt(GREATEST(0,AVG(v*v)-AVG(v)*AVG(v))),0 FROM eligible) SELECT 'reference' AS reference_id,'2026-01-02T10:00:00Z/2026-01-02T11:00:00Z' AS measurement_window,* FROM summaries
  result columns=['reference_id', 'measurement_window', 'representation', 'definition', 'observations', 'eligible_total', 'proportion', 'mean', 'stddev', 'ddof'] rows(9)=[["reference","2026-01-02T10:00:00Z/2026-01-02T11:00:00Z","category","short_distance",30,100,0.3,null,null,null],["reference","2026-01-02T10:00:00Z/2026-01-02T11:00:00Z","category","long_distance",70,100,0.7,null,null,null],["reference","2026-01-02T10:00:00Z/2026-01-02T11:00:00Z","category","not_reported",0,100,0,null,null,null],["reference","2026-01-02T10:00:00Z/2026-01-02T11:00:00Z","predicted_class","late",25,100,0.25,null,null,null],["reference","2026-01-02T10:00:00Z/2026-01-02T11:00:00Z","p

### s02 · explainer · Apply the rule: Monitor production input and prediction distributions
(example) Compare the registered reference and production windows using the declared categories and predicted classes. Keep absent categories in position. Normalize each window with its own eligible total, including the independent larger-window fixture. Keep fixed numerical edges, reference identity, window and the stated standard-deviation divisor with the summaries. This supports investigation of distribution change, not a labeled-error claim. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb4⟧
(misconception) Different bins or category mappings can make distributions incomparable. Keep the same representation and each window's own eligible count instead of comparing raw counts alone. ⟦A.f1 A.f2 A.f3 A:tb5⟧

### s03 · check · Review monitor production input and prediction distributions
Check the distinction — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [choice, intro, grading=client] The selected numeric window uses the N divisor for standard deviation. Which calculation pair follows that declared rule?
  ✔ o1: np.mean(numeric_values) and np.std(numeric_values, ddof=0)
      why: The mean uses the selected observations and ddof=0 uses N.
  ✘ o2: np.mean(numeric_values) and np.std(numeric_values, ddof=1)
      why: ddof=1 uses N-1, not the declared N divisor.
  ✘ o3: Use reference-window mean and standard deviation for the current window
      why: The summaries must be computed over the selected observations, not substituted from the reference.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Check which divisor the window declares.']  remediation→r01
  MEASURES: A:calculate_windowed_mean_and_standard_deviation(f5,f6)   anchors=[]
  taught-before-tested: A.f5←s01; A.f6←s01

### s04 · hands_on · Apply monitor production input and prediction distributions
Practice — Complete the learner-defined function and required imports under the supplied policy; use the declared cases to verify the single deliverable.
QUESTION [code_exercise, core, grading=client] Complete the missing numerical calculations in the supplied monitoring scaffold, then inspect the resulting record.

Complete mean_calculation(values) and std_calculation(values, ddof) using NumPy. Retain the supplied window selection, eligible-count normalization, categorical probabilities, identities and emission scaffold unchanged. The emitted record must report each window’s numerical mean and standard deviation using the declared divisor.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy']} constraints.allowed=['import numpy as np', 'imports for client dependencies identified by the supplied scaffolding', 'def', 'return', 'variable assignment', 'function parameters and calls', 'for loops', 'if statements', 'lists and dictionaries', 'numeric and string literals', 'array indexing and Boolean masks', 'array comparisons', 'arithmetic operators', 'len', 'np.asarray', 'np.histogram(values, bins=fixed_edges)', 'np.mean(numeric_values)', 'np.std(numeric_values, ddof=0)', 'np.std(numeric_values, ddof=1)', 'np.sum', 'summary-emission calls defined by the supplied client contract'] blocked=3 items
  file learner.py [editable]:
# Supplied infrastructure helper (retain unchanged).
exec('def normalize_counts(counts, values):\n    return counts / len(values)\n')

import numpy as np

exec("def summarize(reference, production, policy):\n    fixed_edges = policy['fixed_edges']\n    summaries = []\n    for data in [reference, production]:\n        values = data['numeric_values']\n        values = values[(values >= policy['eligible_numeric_range'][0]) & (values <= policy['eligible_numeric_range'][1])]\n        counts = np.histogram(values, bins=fixed_edges)[0]\n        proportions = normalize_counts(counts, values)\n        categories = {}\n        for category in policy['declared_categories']:\n            categories[category] = np.sum(data['category'] == category) / len(data['category'])\n        classes = {}\n        for predicted_class in policy['declared_classes']:\n            classes[predicted_class] = np.sum(data['predicted_class'] == predicted_class) / len(data['predicted_class'])\n        summaries = summaries + [{'eligible_total': len(values), 'category_total': len(data['category']), 'class_total': len(data['predicted_class']), 'bin_proportions': proportions, 'mean': mean_calculation(values), 'std': std_calculation(values, ddof=0), 'categories': categories, 'classes': classes}]\n    record = {'reference_id': policy['reference_id'], 'window': policy['production_window'], 'fixed_edges': fixed_edges, 'category_definitions': policy['declared_categories'], 'class_definitions': policy['declared_classes'], 'ddof': policy['ddof'], 'reference': summaries[0], 'production': summaries[1]}\n    emit(record)\n    return record\n")

def mean_calculation(values):
    return None

def std_calculation(values, ddof):
    return None

exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"reference_id": "reference", "production_window": {"start": "2026-01-02T10:00:00Z", "end": "2026-01-02T11:00:00Z"}, "fixed_edges": [0, 5, 10], "eligible_numeric_range": [0, 10], "declared_categories": ["short_distance", "long_distance", "not_reported"], "declared_classes": ["on_time", "late", "abstain"], "ddof": 0, "window_membership": "All rows of production.csv are in the declared bounded window; reference.csv is the approved reference. Alternate fixtures are independent windows.", "summary_client": "from summary_client import emit; emit(record) appends a single JSON record to summary.jsonl"}\')')

exec("reference_rows = list(csv.DictReader(open('reference.csv')))")

exec('reference = {}')

exec("reference['numeric_values'] = np.array([float(r['numeric_values'] or 'nan') for r in reference_rows])")

exec("reference['category'] = np.array([r['category'] for r in reference_rows])")

exec("reference['predicted_class'] = np.array([r['predicted_class'] for r in reference_rows])")

exec("production_rows = list(csv.DictReader(open('production.csv')))")

exec('production = {}')

exec("production['numeric_values'] = np.array([float(r['numeric_values'] or 'nan') for r in production_rows])")

exec("production['category'] = np.array([r['category'] for r in production_rows])")

exec("production['predicted_class'] = np.array([r['predicted_class'] for r in production_rows])")

exec('records = []')

exec('def emit(record):\n    records.append(record)')

exec('summarize(reference, production, policy)')

  SOLUTION learner.py:
# Supplied infrastructure helper (retain unchanged).
exec('def normalize_counts(counts, values):\n    return counts / len(values)\n')

import numpy as np

exec("def summarize(reference, production, policy):\n    fixed_edges = policy['fixed_edges']\n    summaries = []\n    for data in [reference, production]:\n        values = data['numeric_values']\n        values = values[(values >= policy['eligible_numeric_range'][0]) & (values <= policy['eligible_numeric_range'][1])]\n        counts = np.histogram(values, bins=fixed_edges)[0]\n        proportions = normalize_counts(counts, values)\n        categories = {}\n        for category in policy['declared_categories']:\n            categories[category] = np.sum(data['category'] == category) / len(data['category'])\n        classes = {}\n        for predicted_class in policy['declared_classes']:\n            classes[predicted_class] = np.sum(data['predicted_class'] == predicted_class) / len(data['predicted_class'])\n        summaries = summaries + [{'eligible_total': len(values), 'category_total': len(data['category']), 'class_total': len(data['predicted_class']), 'bin_proportions': proportions, 'mean': mean_calculation(values), 'std': std_calculation(values, ddof=0), 'categories': categories, 'classes': classes}]\n    record = {'reference_id': policy['reference_id'], 'window': policy['production_window'], 'fixed_edges': fixed_edges, 'category_definitions': policy['declared_categories'], 'class_definitions': policy['declared_classes'], 'ddof': policy['ddof'], 'reference': summaries[0], 'production': summaries[1]}\n    emit(record)\n    return record\n")

def mean_calculation(values):
    return np.mean(values)

def std_calculation(values, ddof):
    return np.std(values, ddof=ddof)

exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"reference_id": "reference", "production_window": {"start": "2026-01-02T10:00:00Z", "end": "2026-01-02T11:00:00Z"}, "fixed_edges": [0, 5, 10], "eligible_numeric_range": [0, 10], "declared_categories": ["short_distance", "long_distance", "not_reported"], "declared_classes": ["on_time", "late", "abstain"], "ddof": 0, "window_membership": "All rows of production.csv are in the declared bounded window; reference.csv is the approved reference. Alternate fixtures are independent windows.", "summary_client": "from summary_client import emit; emit(record) appends a single JSON record to summary.jsonl"}\')')

exec("reference_rows = list(csv.DictReader(open('reference.csv')))")

exec('reference = {}')

exec("reference['numeric_values'] = np.array([float(r['numeric_values'] or 'nan') for r in reference_rows])")

exec("reference['category'] = np.array([r['category'] for r in reference_rows])")

exec("reference['predicted_class'] = np.array([r['predicted_class'] for r in reference_rows])")

exec("production_rows = list(csv.DictReader(open('production.csv')))")

exec('production = {}')

exec("production['numeric_values'] = np.array([float(r['numeric_values'] or 'nan') for r in production_rows])")

exec("production['category'] = np.array([r['category'] for r in production_rows])")

exec("production['predicted_class'] = np.array([r['predicted_class'] for r in production_rows])")

exec('records = []')

exec('def emit(record):\n    records.append(record)')

exec('summarize(reference, production, policy)')

  test t1 (value_equals, visible=True): {"expr":"records","expected":[{"reference_id":"reference","window":{"start":"2026-01-02T10:00:00Z","end":"2026-01-02T11:00:00Z"},"fixed_edges":[0,5,10],"category_definitions":["short_distance","long_distance","not_reported"],"class_definitions":["on_time","late","abstain"],"ddof":0,"reference":{"eligible_total":100,"category_total":100,"class_total":100,"bin_proportions":[0.45,0.55],"mean":4.96,"std":2.5996922894835075,"categories":{"short_distance":0.6,"long_distance":0.4,"not_reported":0},"cla | on-fail: The returned record or calculation does not match the declared fixture contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"cb6cab1929be89c966095a38e068f481fe45c8e9cda50aa0b5daa5721f70523b","tests_passed":1}
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Use policy eligibility and fixed_edges for each window; category and class arrays have their own totals. Check records contains exactly the returned record.']
  MEASURES: A:define_and_record_comparable_production_windows(f1,f4); A:calculate_aligned_numerical_bin_proportions(f2); A:calculate_declared_category_and_prediction_probabilities(f3); A:calculate_windowed_mean_and_standard_deviation(f5,f6)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f4←s01; A.f2←s01; A.f3←s01; A.f5←s01; A.f6←s01

### s05 · explainer · Distinguish data drift, concept drift and observed quality degradation
(intro) Ask three separate questions: did inputs change, did the feature–label relationship change, and did measured prediction quality worsen? With labels unavailable, input evidence cannot answer all three. ⟦B:tb1⟧
(definition) Input data drift is a change in the observed input distribution relative to its reference; input drift monitoring alone does not measure labeled prediction quality. Concept drift changes the conditional target relationship P(Y|X), that is, the relationship between features and labels; a previously useful model can become less useful as that relationship changes. Observed model quality degradation requires comparing predictions with corresponding ground-truth labels and the declared quality reference. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Without matched available labels, report the supported distribution or service evidence and the unresolved quality question rather than asserting labeled quality degradation. Input marginals describe P(X), conditional-target evidence describes P(Y|X), and matched-label errors describe observed quality; changing one does not logically establish changes in all three. ⟦B.f4 B.f5 B:tb3⟧
[DIAGRAM] nodes=['P(X) {More long-distance orders than reference.; P(Y|X) and labeled quality are not established.}', 'P(Y|X) {Within the same distance categories, the feature-label relationship differs from reference.; An input-marginal shift or quality degradation is not established by this alone.}', 'matched_label_errors {Matched-label errors exceed the declared quality reference on the same cohort.; Input or conditional relationship change is not established by this alone.}'] edges=[] alt: Separate evidence for input distribution, conditional target relationship and matched-label quality; none logically establishes the other two.

### s06 · explainer · Apply the rule: Distinguish data drift, concept drift and observed quality degradation
(example) More long-distance orders support an input-distribution observation. They do not establish a changed feature–label relationship or worse labeled quality. Compare corresponding predictions and ground truth against the quality reference for the quality question. If labels are unavailable, retain the useful input or service evidence and mark quality unresolved. Missing labels prove neither stable quality nor degraded quality. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb4⟧

### s07 · explainer · Work the contrast: Distinguish data drift, concept drift and observed quality degradation
(misconception) Input drift alone is not labeled quality degradation. Changes in P(X), P(Y|X) and matched-label errors do not logically establish one another. ⟦B.f1 B.f3 B.f4 B.f5 B:tb5⟧

### s08 · check · Review distinguish data drift, concept drift and observed quality degradation
Check the distinction — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [choice, core, grading=client] Production has more long-distance orders than its reference. Corresponding labels are not yet available. Which conclusion is justified?
  ✔ o1: Inputs differ; labeled quality remains unresolved
      why: Input evidence supports a distribution observation; matched labels are still needed for quality.
  ✘ o2: Input drift proves that prediction quality degraded
      why: A change in P(X) does not logically establish matched-label error degradation.
  ✘ o3: Missing labels establish that quality stayed stable
      why: Unavailable labels establish neither stable nor degraded quality.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Separate the evidence you have from the evidence each claim requires.']  remediation→r03
  MEASURES: B:state_unsupported_quality_and_drift_conclusions(f4,f5)   anchors=[]
  taught-before-tested: B.f4←s05; B.f5←s05

### s09 · hands_on · Review distinguish data drift, concept drift and observed quality degradation
Practice — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [classify, core, grading=client] Read each order-prediction scenario. Classify the evidence-supported change and keep the other conclusions unsupported. A quality-loss claim requires matched predictions and labels against the declared quality reference.
  'scenario_id: input_shift
observation: More long-distance orders than reference.
matched_labels_available: False' -> Input distribution shift; other changes unsupported  (column supported_evidence, role=categorical)
      feedback: P(Y|X) and labeled quality are not established.
  'scenario_id: conditional_shift
observation: Within the same distance categories, the feature-label relationship differs from reference.
matched_labels_available: True' -> Conditional target change; other changes unsupported  (column supported_evidence, role=categorical)
      feedback: An input-marginal shift or quality degradation is not established by this alone.
  'scenario_id: observed_quality
observation: Matched-label errors exceed the declared quality reference on the same cohort.
matched_labels_available: True' -> Observed matched-label quality loss; other changes unsupported  (column supported_evidence, role=categorical)
      feedback: Input or conditional relationship change is not established by this alone.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Review the comparison definition and the evidence required for each judgement.']
  MEASURES: B:identify_input_distribution_shift(f1,f5); B:identify_conditional_target_change(f2,f5); B:identify_observed_quality_degradation(f3,f5); B:state_unsupported_quality_and_drift_conclusions(f4,f5)   anchors=['practice']
  taught-before-tested: B.f1←s05; B.f5←s05; B.f2←s05; B.f5←s05; B.f3←s05; B.f5←s05; B.f4←s05; B.f5←s05

### s10 · explainer · Detect model-input data drift against a defined reference distribution
(intro) Choose the reference, window and comparison rule before inspecting the current data. Do not select a threshold afterward to make the change qualify. ⟦C:tb1⟧
(definition) Define the reference feature distribution, comparison window and declared drift criterion before checking production data. Use identical bin edges and category mappings for reference and observed data, then compute proportions from their own eligible observation totals. Compare the observed distribution/statistics with the reference under the supplied significance or threshold rule and report which features cross it. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) A drift detection result indicates a distribution difference under that rule, not by itself a measured increase in target prediction error. For the arithmetic mean, use np.mean(numeric_values) on the selected numeric observations. For standard deviation, use np.std(numeric_values, ddof=0), which divides squared deviations by N and then takes the square root; use ddof=1 only if the stated calculation requires the N−1 divisor. ⟦C.f4 C.f5 C.f6 C:tb3⟧
(mechanism) Compute each category’s reference/current count divided by its own window total, then apply the supplied probability-distance equation and threshold to aligned category vectors. ⟦C.f7 C:tb4⟧
[SIDE_BY_SIDE] Apply aligned comparisons; a crossing does not measure prediction error. left_label: Reference | right_label: Current
  left:
[TABLE computed result ] caption: Aligned definitions, per-window denominators and numeric summaries; authored fictional fixture.
  produced by sql: WITH cats AS (SELECT 'short_distance' AS definition UNION ALL SELECT 'long_distance' AS definition UNION ALL SELECT 'not_reported' AS definition), classes AS (SELECT 'on_time' AS definition UNION ALL SELECT 'late' AS definition UNION ALL SELECT 'abstain' AS definition),
 eligible AS (SELECT numeric_values AS v FROM samples WHERE numeric_values BETWEEN 0 AND 10),
 summaries AS (
 SELECT 'category' AS representation, definition, COUNT(s.category) AS observations, (SELECT COUNT(*) FROM samples) AS eligible_total,
 1.0*COUNT(s.category)/(SELECT COUNT(*) FROM samples) AS proportion, NULL AS mean, NULL AS stddev, NULL AS ddof
 FROM cats LEFT JOIN samples s ON s.category=cats.definition GROUP BY definition
 UNION ALL
 SELECT 'predicted_class', definition, COUNT(s.predicted_class), (SELECT COUNT(*) FROM samples),
 1.0*COUNT(s.predicted_class)/(SELECT COUNT(*) FROM samples), NULL,NULL,NULL
 FROM classes LEFT JOIN samples s ON s.predicted_class=classes.definition GROUP BY definition
 UNION ALL
 SELECT 'numeric_bin', '[0,5)', SUM(CASE WHEN v>=0 AND v<5 THEN 1 ELSE 0 END),COUNT(*),1.0*SUM(CASE WHEN v>=0 AND v<5 THEN 1 ELSE 0 END)/COUNT(*),NULL,NULL,NULL FROM eligible UNION ALL SELECT 'numeric_bin', '[5,10]', SUM(CASE WHEN v>=5 AND v<=10 THEN 1 ELSE 0 END),COUNT(*),1.0*SUM(CASE WHEN v>=5 AND v<=10 THEN 1 ELSE 0 END)/COUNT(*),NULL,NULL,NULL FROM eligible UNION ALL SELECT 'numeric_summary','numeric_values',COUNT(*),COUNT(*),NULL,AVG(v),sqrt(GREATEST(0,AVG(v*v)-AVG(v)*AVG(v))),0 FROM eligible) SELECT 'reference' AS reference_id,'approved reference' AS measurement_window,* FROM summaries
  result columns=['reference_id', 'measurement_window', 'representation', 'definition', 'observations', 'eligible_total', 'proportion', 'mean', 'stddev', 'ddof'] rows(9)=[["reference","approved reference","category","short_distance",60,100,0.6,null,null,null],["reference","approved reference","category","long_distance",40,100,0.4,null,null,null],["reference","approved reference","category","not_reported",0,100,0,null,null,null],["reference","approved reference","predicted_class","late",25,100,0.25,null,null,null],["reference","approved reference","predicted_class","on_time",75,100,0.75,null,null,null],["reference","approved reference","predicted_class","abstain"
  right:
[TABLE computed result ] caption: Aligned definitions, per-window denominators and numeric summaries; authored fictional fixture.
  produced by sql: WITH cats AS (SELECT 'short_distance' AS definition UNION ALL SELECT 'long_distance' AS definition UNION ALL SELECT 'not_reported' AS definition), classes AS (SELECT 'on_time' AS definition UNION ALL SELECT 'late' AS definition UNION ALL SELECT 'abstain' AS definition),
 eligible AS (SELECT numeric_values AS v FROM samples WHERE numeric_values BETWEEN 0 AND 10),
 summaries AS (
 SELECT 'category' AS representation, definition, COUNT(s.category) AS observations, (SELECT COUNT(*) FROM samples) AS eligible_total,
 1.0*COUNT(s.category)/(SELECT COUNT(*) FROM samples) AS proportion, NULL AS mean, NULL AS stddev, NULL AS ddof
 FROM cats LEFT JOIN samples s ON s.category=cats.definition GROUP BY definition
 UNION ALL
 SELECT 'predicted_class', definition, COUNT(s.predicted_class), (SELECT COUNT(*) FROM samples),
 1.0*COUNT(s.predicted_class)/(SELECT COUNT(*) FROM samples), NULL,NULL,NULL
 FROM classes LEFT JOIN samples s ON s.predicted_class=classes.definition GROUP BY definition
 UNION ALL
 SELECT 'numeric_bin', '[0,5)', SUM(CASE WHEN v>=0 AND v<5 THEN 1 ELSE 0 END),COUNT(*),1.0*SUM(CASE WHEN v>=0 AND v<5 THEN 1 ELSE 0 END)/COUNT(*),NULL,NULL,NULL FROM eligible UNION ALL SELECT 'numeric_bin', '[5,10]', SUM(CASE WHEN v>=5 AND v<=10 THEN 1 ELSE 0 END),COUNT(*),1.0*SUM(CASE WHEN v>=5 AND v<=10 THEN 1 ELSE 0 END)/COUNT(*),NULL,NULL,NULL FROM eligible UNION ALL SELECT 'numeric_summary','numeric_values',COUNT(*),COUNT(*),NULL,AVG(v),sqrt(GREATEST(0,AVG(v*v)-AVG(v)*AVG(v))),0 FROM eligible) SELECT 'reference' AS reference_id,'2026-01-02T10:00:00Z/2026-01-02T11:00:00Z' AS measurement_window,* FROM summaries
  result columns=['reference_id', 'measurement_window', 'representation', 'definition', 'observations', 'eligible_total', 'proportion', 'mean', 'stddev', 'ddof'] rows(9)=[["reference","2026-01-02T10:00:00Z/2026-01-02T11:00:00Z","category","short_distance",30,100,0.3,null,null,null],["reference","2026-01-02T10:00:00Z/2026-01-02T11:00:00Z","category","long_distance",70,100,0.7,null,null,null],["reference","2026-01-02T10:00:00Z/2026-01-02T11:00:00Z","category","not_reported",0,100,0,null,null,null],["reference","2026-01-02T10:00:00Z/2026-01-02T11:00:00Z","predicted_class","late",25,100,0.25,null,null,null],["reference","2026-01-02T10:00:00Z/2026-01-02T11:00:00Z","p
[TABLE computed result ] caption: Feature-level distribution decisions under the supplied rule.
  produced by sql: WITH cats AS (SELECT 'short_distance' AS definition UNION ALL SELECT 'long_distance' AS definition UNION ALL SELECT 'not_reported' AS definition), probabilities AS (SELECT 'category' AS feature,definition,1.0*(SELECT COUNT(*) FROM reference WHERE category=definition)/(SELECT COUNT(*) FROM reference) AS rp,1.0*(SELECT COUNT(*) FROM current WHERE category=definition)/(SELECT COUNT(*) FROM current) AS cp FROM cats UNION ALL SELECT 'numeric_bins','[0,5)',1.0*(SELECT COUNT(*) FROM reference WHERE numeric_values>=0 AND numeric_values<5)/(SELECT COUNT(*) FROM reference WHERE numeric_values BETWEEN 0 AND 10),1.0*(SELECT COUNT(*) FROM current WHERE numeric_values>=0 AND numeric_values<5)/(SELECT COUNT(*) FROM current WHERE numeric_values BETWEEN 0 AND 10) UNION ALL SELECT 'numeric_bins','[5, 10]',1.0*(SELECT COUNT(*) FROM reference WHERE numeric_values>=5 AND numeric_values<=10)/(SELECT COUNT(*) FROM reference WHERE numeric_values BETWEEN 0 AND 10),1.0*(SELECT COUNT(*) FROM current WHERE numeric_values>=5 AND numeric_values<=10)/(SELECT COUNT(*) FROM current WHERE numeric_values BETWEEN 0 AND 10)), distances AS (SELECT feature,0.5*SUM(ABS(rp-cp)) AS distance FROM probabilities GROUP BY feature) SELECT *,'0.5 * sum(abs(reference_probability[i]-current_probability[i])) over all aligned positions' AS equation,'distance > 0.20; equality is not a crossing' AS criterion, distance>0.20 AS crosses,'unresolved without matched labels' AS quality FROM distances
  result columns=['feature', 'distance', 'equation', 'criterion', 'crosses', 'quality'] rows(2)=[["category",0.29999999999999993,"0.5 * sum(abs(reference_probability[i]-current_probability[i])) over all aligned positions","distance > 0.20; equality is not a crossing",true,"unresolved without matched labels"],["numeric_bins",0,"0.5 * sum(abs(reference_probability[i]-current_probability[i])) over all aligned positions","distance > 0.20; equality is not a crossing",false,"unresolved without matched labels"]]

### s11 · explainer · Apply the rule: Detect model-input data drift against a defined reference distribution
(example) Compare the registered windows with aligned category and numerical-bin proportions. Apply the supplied distance equation and threshold, not a newly chosen rule. Keep each window’s eligible total, fixed edges, reference identity, window, mean and stated spread. Name the crossing features. The verdict concerns distribution difference under that criterion, not increased target error. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C:tb5⟧

### s12 · explainer · Work the contrast: Detect model-input data drift against a defined reference distribution
(misconception) A drift threshold crossing is not proof that prediction error increased. Also, different category mappings or reused reference denominators would change the comparison rather than measure the intended distributions. ⟦C.f2 C.f4 C:tb6⟧

### s13 · check · Review detect model-input data drift against a defined reference distribution
Check the distinction — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [choice, stretch, grading=client] An aligned feature comparison crosses its predeclared drift threshold. No matched ground truth is available. What should the verdict say?
  ✔ o1: This feature differs under the declared rule; increased prediction error is not established
      why: The threshold decision describes a distribution difference, not measured target error.
  ✘ o2: The threshold proves prediction error increased
      why: Drift monitoring alone does not measure labeled prediction quality.
  ✘ o3: Change the threshold after looking at current values so this feature no longer crosses
      why: Reference, comparison window and drift criterion are declared before checking data.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Ask what the feature threshold actually measures.']  remediation→r05
  MEASURES: C:identify_feature_level_drift_without_inferring_quality_loss(f3,f4)   anchors=[]
  taught-before-tested: C.f3←s10; C.f4←s10

### s14 · hands_on · Apply detect model-input data drift against a defined reference distribution
Practice — Complete the learner-defined function and required imports under the supplied policy; use the declared cases to verify the single deliverable.
QUESTION [code_exercise, stretch, grading=client] Complete the missing numerical calculations in the supplied monitoring scaffold, then inspect the resulting record.

Complete ref_mean, cur_mean, ref_std and cur_std from ref_values and cur_values using np.mean and np.std with ddof=0. Retain the supplied eligibility, aligned-probability distance and strict threshold decision unchanged. The result reports distribution differences, not established prediction-quality loss.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy']} constraints.allowed=['import numpy as np', 'Imports for required dependencies explicitly identified by the supplied infrastructure scaffolding', 'def with parameters', 'return', 'Variable assignment', 'Lists and dictionaries', 'Array indexing and Boolean masks', 'np.asarray(...)', 'np.mean(numeric_values)', 'np.std(numeric_values, ddof=0)', 'np.std(numeric_values, ddof=1) only when the supplied calculation requires the N−1 divisor', 'np.count_nonzero(...)', 'np.sum(...)', 'np.abs(...)', 'Elementwise arithmetic and broadcasting', 'Comparison operators', 'Calls to supplied infrastructure interfaces'] blocked=0 items
  file learner.py [editable]:
exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"reference_id": "reference", "current_id": "production", "comparison_window": "2026-01-02T10:00:00Z/2026-01-02T11:00:00Z", "fixed_edges": [0, 5, 10], "eligible_numeric_range": [0, 10], "declared_categories": ["short_distance", "long_distance", "not_reported"], "ddof": 0, "distance_equation": "0.5 * sum(abs(reference_probability[i]-current_probability[i])) over all aligned positions", "criterion": "distance > 0.20; equality is not a crossing", "numeric_rule": "Apply the same distance to aligned numerical-bin proportions; retain mean and ddof=0 standard deviation separately", "quality_claim": "unresolved without matched labels"}\')')

exec("reference_rows = list(csv.DictReader(open('reference.csv')))")

exec('reference = {}')

exec("reference['numeric_values'] = np.array([float(r['numeric_values'] or 'nan') for r in reference_rows])")

exec("reference['category'] = np.array([r['category'] for r in reference_rows])")

exec("reference['predicted_class'] = np.array([r['predicted_class'] for r in reference_rows])")

exec("production_rows = list(csv.DictReader(open('production.csv')))")

exec('production = {}')

exec("production['numeric_values'] = np.array([float(r['numeric_values'] or 'nan') for r in production_rows])")

exec("production['category'] = np.array([r['category'] for r in production_rows])")

exec("production['predicted_class'] = np.array([r['predicted_class'] for r in production_rows])")

exec("def counts(data):\n    v = data['numeric_values']\n    v = v[(v >= 0) & (v <= 10)]\n    return (np.histogram(v, bins=policy['fixed_edges'])[0], np.array([np.count_nonzero(data['category'] == c) for c in policy['declared_categories']]), np.count_nonzero(v == v), np.count_nonzero(data['category'] == data['category']))")

exec('ref_bins, ref_cats, ref_n, ref_cat_n = counts(reference)')

exec('cur_bins, cur_cats, cur_n, cur_cat_n = counts(production)')

exec("ref_values = reference['numeric_values']")

exec("cur_values = production['numeric_values']")

exec('ref_values = ref_values[(ref_values >= 0) & (ref_values <= 10)]')

exec('cur_values = cur_values[(cur_values >= 0) & (cur_values <= 10)]')

ref_mean = None

cur_mean = None

ref_std = None

cur_std = None

reference_categories = ref_cats / ref_cat_n

current_categories = cur_cats / cur_cat_n

reference_bins = ref_bins / ref_n

current_bins = cur_bins / cur_n

category_distance = 0.5 * np.sum(np.abs(reference_categories - current_categories))

numeric_distance = 0.5 * np.sum(np.abs(reference_bins - current_bins))

category_drift = category_distance > 0.2

numeric_drift = numeric_distance > 0.2

exec("result = {'reference_id': policy['reference_id'], 'current_id': policy['current_id'], 'window': policy['comparison_window'], 'edges': policy['fixed_edges'], 'categories': policy['declared_categories'], 'eligibility': policy['eligible_numeric_range'], 'criterion': policy['criterion'], 'quality_claim': policy['quality_claim'], 'reference_mean': ref_mean, 'current_mean': cur_mean, 'reference_std': ref_std, 'current_std': cur_std, 'reference_categories': reference_categories, 'current_categories': current_categories, 'reference_bins': reference_bins, 'current_bins': current_bins, 'category_distance': category_distance, 'numeric_distance': numeric_distance, 'category_drift': category_drift, 'numeric_drift': numeric_drift, 'reference_total': ref_n, 'current_total': cur_n}")

  SOLUTION learner.py:
exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"reference_id": "reference", "current_id": "production", "comparison_window": "2026-01-02T10:00:00Z/2026-01-02T11:00:00Z", "fixed_edges": [0, 5, 10], "eligible_numeric_range": [0, 10], "declared_categories": ["short_distance", "long_distance", "not_reported"], "ddof": 0, "distance_equation": "0.5 * sum(abs(reference_probability[i]-current_probability[i])) over all aligned positions", "criterion": "distance > 0.20; equality is not a crossing", "numeric_rule": "Apply the same distance to aligned numerical-bin proportions; retain mean and ddof=0 standard deviation separately", "quality_claim": "unresolved without matched labels"}\')')

exec("reference_rows = list(csv.DictReader(open('reference.csv')))")

exec('reference = {}')

exec("reference['numeric_values'] = np.array([float(r['numeric_values'] or 'nan') for r in reference_rows])")

exec("reference['category'] = np.array([r['category'] for r in reference_rows])")

exec("reference['predicted_class'] = np.array([r['predicted_class'] for r in reference_rows])")

exec("production_rows = list(csv.DictReader(open('production.csv')))")

exec('production = {}')

exec("production['numeric_values'] = np.array([float(r['numeric_values'] or 'nan') for r in production_rows])")

exec("production['category'] = np.array([r['category'] for r in production_rows])")

exec("production['predicted_class'] = np.array([r['predicted_class'] for r in production_rows])")

exec("def counts(data):\n    v = data['numeric_values']\n    v = v[(v >= 0) & (v <= 10)]\n    return (np.histogram(v, bins=policy['fixed_edges'])[0], np.array([np.count_nonzero(data['category'] == c) for c in policy['declared_categories']]), np.count_nonzero(v == v), np.count_nonzero(data['category'] == data['category']))")

exec('ref_bins, ref_cats, ref_n, ref_cat_n = counts(reference)')

exec('cur_bins, cur_cats, cur_n, cur_cat_n = counts(production)')

exec("ref_values = reference['numeric_values']")

exec("cur_values = production['numeric_values']")

exec('ref_values = ref_values[(ref_values >= 0) & (ref_values <= 10)]')

exec('cur_values = cur_values[(cur_values >= 0) & (cur_values <= 10)]')

ref_mean = np.mean(ref_values)

cur_mean = np.mean(cur_values)

ref_std = np.std(ref_values, ddof=0)

cur_std = np.std(cur_values, ddof=0)

reference_categories = ref_cats / ref_cat_n

current_categories = cur_cats / cur_cat_n

reference_bins = ref_bins / ref_n

current_bins = cur_bins / cur_n

category_distance = 0.5 * np.sum(np.abs(reference_categories - current_categories))

numeric_distance = 0.5 * np.sum(np.abs(reference_bins - current_bins))

category_drift = category_distance > 0.2

numeric_drift = numeric_distance > 0.2

exec("result = {'reference_id': policy['reference_id'], 'current_id': policy['current_id'], 'window': policy['comparison_window'], 'edges': policy['fixed_edges'], 'categories': policy['declared_categories'], 'eligibility': policy['eligible_numeric_range'], 'criterion': policy['criterion'], 'quality_claim': policy['quality_claim'], 'reference_mean': ref_mean, 'current_mean': cur_mean, 'reference_std': ref_std, 'current_std': cur_std, 'reference_categories': reference_categories, 'current_categories': current_categories, 'reference_bins': reference_bins, 'current_bins': current_bins, 'category_distance': category_distance, 'numeric_distance': numeric_distance, 'category_drift': category_drift, 'numeric_drift': numeric_drift, 'reference_total': ref_n, 'current_total': cur_n}")

  test t1 (value_equals, visible=True): {"expr":"result","expected":{"reference_id":"reference","current_id":"production","window":"2026-01-02T10:00:00Z/2026-01-02T11:00:00Z","edges":[0,5,10],"categories":["short_distance","long_distance","not_reported"],"eligibility":[0,10],"criterion":"distance > 0.20; equality is not a crossing","quality_claim":"unresolved without matched labels","reference_mean":4.96,"current_mean":4.96,"reference_std":2.5996922894835075,"current_std":2.5996922894835075,"reference_categories":[0.6,0.4,0],"current_ | on-fail: The returned record or calculation does not match the declared fixture contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"f39a0da22ed5d04e1084361fd927ce92d9d132ce0be24f46cb4af3ff14d64717","tests_passed":1}
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['ref_n/cur_n and ref_cat_n/cur_cat_n describe different denominators; retain aligned positions before applying policy distance_equation and criterion.']
  MEASURES: C:identify_valid_reference_window_and_distribution_alignment(f1,f2); C:calculate_numeric_mean_and_declared_standard_deviation(f5,f6); C:calculate_aligned_category_probabilities_and_distance(f2,f7); C:identify_feature_level_drift_without_inferring_quality_loss(f3,f4)   anchors=['practice']
  taught-before-tested: C.f1←s10; C.f2←s10; C.f5←s10; C.f6←s10; C.f2←s10; C.f7←s10; C.f3←s10; C.f4←s10

### s15 · recap · Keep these distinctions
(takeaway) Keep representations, bins and per-window denominators aligned. Separate input distribution, conditional-target and matched-label quality evidence. Apply only the declared drift criterion; a crossing alone does not measure target error.
[UP NEXT] Measure production model quality when labels arrive: Freeze the prediction cohort before labels arrive. Attach ground truth by prediction identity; recent predictions with incomplete labels are not a fully mature quality cohort.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Monitor production input and prediction distributions
(mechanism) Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations. ⟦A.f5 A:tb3⟧
(mechanism) Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor. ⟦A.f6 A:tb3⟧
(misconception) A mean uses the selected observations. For standard deviation, ddof=0 divides by N; ddof=1 uses N−1 only when required. Changing the divisor changes the requested calculation. ⟦A.f5 A.f6 A:tb3⟧
### r02 · Revisit: Monitor production input and prediction distributions
(mechanism) Compare captured production inputs with the defined reference dataset using the same feature representations, reference constraints and measurement window. ⟦A.f1 A:tb2⟧
(mechanism) For numerical values, np.histogram(values, bins=fixed_edges) returns bin counts; divide by the eligible observation count to compare bin proportions on the same edges. ⟦A.f2 A:tb2⟧
(mechanism) For categorical or predicted-class values, count each declared category and divide by its window total, retaining category definitions and the total count. ⟦A.f3 A:tb2⟧
(mechanism) Record the production window, reference identity and observed summaries so an apparent distribution change can be investigated. ⟦A.f4 A:tb3⟧
(mechanism) Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations. ⟦A.f5 A:tb3⟧
(mechanism) Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor. ⟦A.f6 A:tb3⟧
(misconception) Different bins or category mappings can make distributions incomparable. Keep the same representation and each window's own eligible count instead of comparing raw counts alone. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb2 A:tb3⟧
### r03 · Revisit: Distinguish data drift, concept drift and observed quality degradation
(mechanism) Without matched available labels, report the supported distribution or service evidence and the unresolved quality question rather than asserting labeled quality degradation. ⟦B.f4 B:tb3⟧
(mechanism) Input marginals describe P(X), conditional-target evidence describes P(Y|X), and matched-label errors describe observed quality; changing one does not logically establish changes in all three. ⟦B.f5 B:tb3⟧
(misconception) Input or service evidence can be reported with quality unresolved. Without matched available labels, neither “quality worsened” nor “quality stayed constant” follows from the input change. ⟦B.f4 B.f5 B:tb3⟧
### r04 · Revisit: Distinguish data drift, concept drift and observed quality degradation
(mechanism) Input data drift is a change in the observed input distribution relative to its reference; input drift monitoring alone does not measure labeled prediction quality. ⟦B.f1 B:tb2⟧
(mechanism) Concept drift changes the conditional target relationship P(Y|X), that is, the relationship between features and labels; a previously useful model can become less useful as that relationship changes. ⟦B.f2 B:tb2⟧
(mechanism) Observed model quality degradation requires comparing predictions with corresponding ground-truth labels and the declared quality reference. ⟦B.f3 B:tb2⟧
(mechanism) Without matched available labels, report the supported distribution or service evidence and the unresolved quality question rather than asserting labeled quality degradation. ⟦B.f4 B:tb3⟧
(mechanism) Input marginals describe P(X), conditional-target evidence describes P(Y|X), and matched-label errors describe observed quality; changing one does not logically establish changes in all three. ⟦B.f5 B:tb3⟧
(misconception) Input drift alone is not labeled quality degradation. Changes in P(X), P(Y|X) and matched-label errors do not logically establish one another. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3⟧
### r05 · Revisit: Detect model-input data drift against a defined reference distribution
(mechanism) Compare the observed distribution/statistics with the reference under the supplied significance or threshold rule and report which features cross it. ⟦C.f3 C:tb2⟧
(mechanism) A drift detection result indicates a distribution difference under that rule, not by itself a measured increase in target prediction error. ⟦C.f4 C:tb3⟧
(misconception) Crossing the declared rule identifies a feature-level distribution difference. It is not a measured increase in labeled prediction error. ⟦C.f3 C.f4 C:tb2 C:tb3⟧
### r06 · Revisit: Detect model-input data drift against a defined reference distribution
(mechanism) Define the reference feature distribution, comparison window and declared drift criterion before checking production data. ⟦C.f1 C:tb2⟧
(mechanism) Use identical bin edges and category mappings for reference and observed data, then compute proportions from their own eligible observation totals. ⟦C.f2 C:tb2⟧
(mechanism) Compare the observed distribution/statistics with the reference under the supplied significance or threshold rule and report which features cross it. ⟦C.f3 C:tb2⟧
(mechanism) A drift detection result indicates a distribution difference under that rule, not by itself a measured increase in target prediction error. ⟦C.f4 C:tb3⟧
(mechanism) Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations. ⟦C.f5 C:tb3⟧
(mechanism) Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor. ⟦C.f6 C:tb3⟧
(mechanism) Compute each category’s reference/current count divided by its own window total, then apply the supplied probability-distance equation and threshold to aligned category vectors. ⟦C.f7 C:tb4⟧
(misconception) A drift threshold crossing is not proof that prediction error increased. Also, different category mappings or reused reference denominators would change the comparison rather than measure the intended distributions. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C:tb2 C:tb3 C:tb4⟧

=========

# EVALUATOR PACKET — Labels, alerts and regression diagnosis (mle.tile.083_085)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.delayed_label_quality — Measure production model quality when labels arrive
B = mle.actionable_ml_alerts — Configure actionable model and service alerts
C = mle.production_regression_diagnosis — Triage a production regression to select data repair, rollback or gated retraining

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=10
  warn: remediation step mle.tile.083_085.r02 is never referenced
  warn: remediation step mle.tile.083_085.r04 is never referenced
  warn: remediation step mle.tile.083_085.r06 is never referenced
  warn: mle.tile.083_085.s01: prose block without lineage.fact_ids
  warn: mle.tile.083_085.s06/ix.mle.tile.083_085.s06: ADVISORY — syntax descriptors with no detector: ['arithmetic operators', 'dictionary key lookup and assignment', 'dictionary literals', 'for loops', 'if and else', 'import statements for required supplied library or client dependencies', 'len', 'list literals and append', 'membership tests', 'numeric literals', 'string literals', 'sum']
  warn: mle.tile.083_085.s07: prose block without lineage.fact_ids
  warn: mle.tile.083_085.s11/ix.mle.tile.083_085.s11: ADVISORY — syntax descriptors with no detector: ['Boolean operators', 'arithmetic operators', 'assert predicate', 'calls to the supplied existing-runtime replay helper', 'mapping and list indexing', 'mapping and list literals', 'numeric and string literals']
  warn: mle.tile.083_085.s12: prose block without lineage.fact_ids
  warn: mle.tile.083_085.s16/ix.mle.tile.083_085.s16: ADVISORY — syntax descriptors with no detector: ['Boolean mask operators & and |', 'NumPy array indexing with Boolean masks', 'assert statements', 'dictionary indexing', 'division guarded by a nonzero denominator', 'for loops', 'if/elif/else statements', 'lists and dictionaries', 'numeric, string, Boolean and None literals', 'parenthesized expressions']
  warn: mle.tile.083_085.s17: prose block without lineage.fact_ids

## SOURCE FACTS — A (mle.delayed_label_quality)   objective: Evaluate a matured, keyed prediction cohort with explicit label-coverage limits.
A.f1: Use a prediction-ID dictionary to preserve cohort membership and prediction time before attaching delayed labels by key.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
A.f2: Join only labels that belong to those prediction IDs and satisfy the declared availability boundary; unmatched labels and duplicate IDs need explicit handling.   [sources: sagemaker_model_monitor#model-monitor-model-quality-merge.html — Ingest Ground Truth labels and merge them with predictions]
A.f3: Define the prediction cohort and analysis delay so recent incomplete ground truth is not treated as a mature cohort.   [sources: sagemaker_model_monitor#model-monitor-model-quality-schedule.html — Model monitor offsets]
A.f4: Estimate P(label mature | cohort) as mature eligible prediction IDs divided by all eligible prediction IDs in that cohort, retaining the denominator.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f5: Compute the declared quality quantity on the matched mature cohort and report its label coverage; without justified coverage it does not estimate quality for all traffic.   [sources: sagemaker_model_monitor#model-monitor-model-quality.html — Monitor model quality]
A.f6: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
A.f7: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Labels, Alerts and Regression Diagnosis.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.label_integrity, mle.task_metric_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function, including imports for NumPy and any required supplied client dependencies, that preserves one prediction cohort in a prediction-ID dictionary, attaches eligible delayed labels under the declared availability boundary, and reports mature-cohort quality, loss mean, loss standard deviation and label maturity coverage. Use the supplied infrastructure scaffolding without changing its authorization or runtime configuration.  SUCCESS: The function preserves prediction times and cohort membership, explicitly handles duplicate IDs and unmatched labels, and excludes labels outside the declared boundary. For the illustrative cohort, it retains 100 eligible IDs and 60 mature matched IDs, reports maturity coverage of 0.60 and error proportion of 0.10 from six matched errors, and computes np.mean and np.std with ddof=0 on the supplied mature labeled losses. Its returned report identifies these as mature-cohort results, not an established quality estimate for all traffic.
ASSESSMENT ANCHOR: preserve_and_join_a_time_bounded_prediction_cohort facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: compute_label_maturity_and_scope_quality_estimates facts=['f4', 'f5']
ASSESSMENT ANCHOR: compute_mean_and_declared_standard_deviation_of_mature_losses facts=['f6', 'f7']

## SOURCE FACTS — B (mle.actionable_ml_alerts)   objective: Configure and replay an actionable alert against baseline variability and a known breach.
B.f1: Use the baseline measurement window and indicator definition to distinguish normal variability from an actionable breach.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/observability — Establish robust observability]
B.f2: Write the existing alert’s indicator, threshold/window rule, owner and response in its YAML schema, then inspect the parsed configuration before replay.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/ — The Compose Specification]
B.f3: Apply the declared noise-tolerant threshold rule to the computed baseline mean/spread, rather than alerting on every single fluctuation.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/reliability/observability — Establish robust observability]
B.f4: Replay normal and breached windows, checking that only the configured breach produces the intended owner/action record.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/operational-excellence/manage-incidents-and-problems — Manage incidents and problems]
B.f5: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
B.f6: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
B.f7: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
B.f8: With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.   [sources: python_tutorial#https://pyyaml.org/wiki/PyYAMLDocumentation — Reference: safe_load; safe_dump]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Labels, Alerts and Regression Diagnosis.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.service_telemetry, mle.distribution_monitoring. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Compute the supplied baseline window's mean and standard deviation using the declared divisor. Apply the supplied noise-tolerant threshold rule, write the indicator, threshold/window rule, owner and response into the existing YAML schema, reload and inspect it, and replay the declared normal, boundary and breached cases.  SUCCESS: The computed statistics and resolved YAML fields match the supplied contract. Predicate assertions pass for the declared valid, boundary and failure cases. Replay produces no breach owner/action record for normal windows and produces the intended owner/action record for a qualifying breach; boundary behavior matches the declared rule.
ASSESSMENT ANCHOR: select_noise_tolerant_alert_condition facts=['f1', 'f3', 'f5', 'f6']
ASSESSMENT ANCHOR: identify_configured_owner_and_actionable_response facts=['f2', 'f8']
ASSESSMENT ANCHOR: verify_breach_only_owner_action_output facts=['f4', 'f7']

## SOURCE FACTS — C (mle.production_regression_diagnosis)   objective: Reproduce and triage a model-service regression using a tested, evidence-supported hypothesis.
C.f1: Start triage with client-visible impact and the available timeline, deployment, data, service and quality evidence.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/operational-excellence/manage-incidents-and-problems — Manage incidents and problems]
C.f2: A schema/value failure identifies data conditions to investigate, whereas a distribution difference alone does not prove labeled model-quality degradation.   [sources: sagemaker_model_monitor#model-monitor-data-quality.html — Monitor data quality]
C.f3: Compare the active artifact/configuration identities with the approved deployment and run record when investigating a release-correlated regression.   [sources: google_mlops_pipelines#Metadata management]
C.f4: Check matched mature-label evidence before selecting a response justified specifically by prediction-quality degradation.   [sources: sagemaker_model_monitor#model-monitor-model-quality-merge.html — Ingest Ground Truth labels and merge them with predictions]
C.f5: Select the supplied supported action—data repair, approved rollback or gated retraining—under the existing incident policy and preserve the required validation gates.   [sources: google_mlops_pipelines#Data and model validation]
C.f6: Calculate conditional labeled error rates for each release/cohort on matched eligible labels, keeping their conditioning counts distinct.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
C.f7: Reproduce and isolate the regression from the release/telemetry timeline, test one causal hypothesis against the evidence and choose only the supported response.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/operational-excellence/manage-incidents-and-problems — Manage incidents and problems]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Labels, Alerts and Regression Diagnosis.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.data_drift_detection, mle.delayed_label_quality, mle.service_telemetry, mle.drift_degradation_distinction, mle.deployed_model_lineage_audit. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Use supplied release, telemetry, artifact/configuration, schema, distribution and mature-label records to reproduce and isolate one regression. Test one causal hypothesis, calculate conditional labeled error rates for each release/cohort with separate eligible-label counts, and justify the supplied policy-supported data repair, approved rollback or gated retraining response without executing recovery.  SUCCESS: The analysis identifies client-visible impact and its timeline, compares active identities with approved deployment/run records, and tests a hypothesis against distinguishing evidence. Each release/cohort result retains its matched eligible mature-label denominator and error count; groups without eligible labels are reported as unavailable. The selected response follows the supplied incident policy, names the required validation gates, and does not treat distribution shift alone as prediction-quality loss.
ASSESSMENT ANCHOR: localize_regression_and_test_causal_hypothesis facts=['f1', 'f3', 'f7']
ASSESSMENT ANCHOR: distinguish_input_shift_from_matched_labeled_quality_loss facts=['f2', 'f4', 'f6']
ASSESSMENT ANCHOR: select_evidence_supported_response_with_required_gates facts=['f5', 'f7']

## DATA ASSETS USED
ds.alert_observations: Alert Observations — columns: window_id(identifier), numeric_values(numerical)
   ["baseline",2]
   ["baseline",4]
   ["baseline",6]
   ["normal",3]
   ["normal",4]
   ["normal",5]
   ["boundary",7]
   ["boundary",8]
ds.labels: Labels — columns: prediction_id(identifier), label_timestamp(datetime), label(categorical), loss(numerical)
   ["p001","2026-01-03T10:00:00Z","on_time",1.0]
   ["p002","2026-01-03T10:00:00Z","late",1.0]
   ["p003","2026-01-03T10:00:00Z","late",1.0]
   ["p004","2026-01-03T10:00:00Z","on_time",1.0]
   ["p005","2026-01-03T10:00:00Z","late",1.0]
   ["p006","2026-01-03T10:00:00Z","late",1.0]
   ["p007","2026-01-03T10:00:00Z","late",0.0]
   ["p008","2026-01-03T10:00:00Z","on_time",0.0]
   variant duplicate_label: 1 ops; planted: issue.duplicate_label(duplicate_row)
ds.predictions: Predictions — columns: prediction_id(identifier), prediction_timestamp(datetime), prediction(categorical), cohort_id(identifier), eligible(categorical)
   ["p001","2026-01-02T10:00:00Z","late","fixed_100",true]
   ["p002","2026-01-02T10:00:00Z","on_time","fixed_100",true]
   ["p003","2026-01-02T10:00:00Z","on_time","fixed_100",true]
   ["p004","2026-01-02T10:00:00Z","late","fixed_100",true]
   ["p005","2026-01-02T10:00:00Z","on_time","fixed_100",true]
   ["p006","2026-01-02T10:00:00Z","on_time","fixed_100",true]
   ["p007","2026-01-02T10:00:00Z","late","fixed_100",true]
   ["p008","2026-01-02T10:00:00Z","on_time","fixed_100",true]
ds.release_evidence: Release Evidence — columns: release_id(identifier), cohort_id(identifier), timestamp(datetime), active_artifact(identifier), approved_artifact(identifier), active_config(identifier), approved_config(identifier), schema_pass(categorical), distribution_distance(numerical), matched_eligible_labels(numerical), labeled_errors(numerical), client_impact(text), hypothesis_test(text), supported_response(categorical)
   ["r1","before","2026-01-02T09:00:00Z","model.r1","model.r1","cfg.r1","cfg.r1",true,0.0,60,6,"baseline","approved configuration reproduces baseline","none"]
   ["r2","after","2026-01-02T11:00:00Z","model.r2","model.r2","cfg.bad","cfg.r2",true,0.3,40,12,"more incorrect arrival predictions","bad configuration reproduces errors; approved rollback restores baseline","approved_rollback"]
   ["r2","incomplete","2026-01-03T23:00:00Z","model.r2","model.r2","cfg.bad","cfg.r2",true,0.3,0,0,"quality unresolved","no mature labels","investigate"]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute training and inference expenditure to workloads; Choose scheduled, new-data or investigated quality/drift retraining triggers; Configure actionable model and service alerts; Gate a retrained candidate against the incumbent using validation evidence before controlled promotion; Invoke retraining with a versioned input snapshot from an authorized trigger; Prevent duplicate or overlapping retraining runs; Remove model-serving resources safely on an existing platform; Set an ML workload cost guardrail on an existing platform; Track ML workload compute and memory utilization; Triage a production regression to select data repair, rollback or gated retraining; Use an ML incident runbook for safe recovery on an existing platform

## LESSON, in learner order

### s01 · explainer · Measure production model quality when labels arrive
(intro) Freeze the prediction cohort before labels arrive. Attach ground truth by prediction identity; recent predictions with incomplete labels are not a fully mature quality cohort. ⟦A:tb1⟧
(mechanism) Use a prediction-ID dictionary to preserve cohort membership and prediction time before attaching delayed labels by key. Join only labels that belong to those prediction IDs and satisfy the declared availability boundary; unmatched labels and duplicate IDs need explicit handling. Define the prediction cohort and analysis delay so recent incomplete ground truth is not treated as a mature cohort. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Estimate P(label mature | cohort) as mature eligible prediction IDs divided by all eligible prediction IDs in that cohort, retaining the denominator. Compute the declared quality quantity on the matched mature cohort and report its label coverage; without justified coverage it does not estimate quality for all traffic. For the arithmetic mean, use np.mean(numeric_values) on the selected numeric observations. ⟦A.f4 A.f5 A.f6 A:tb3⟧
[CODE python]
import numpy as np
# Reject repeated prediction or label IDs before dictionary construction.
cohort_by_id = {row["prediction_id"]: row for row in eligible_predictions}
# Preserve each prediction_timestamp and the frozen cohort membership.
# Attach only cohort labels within the availability boundary and analysis delay.
# Record unmatched and unavailable labels separately.
maturity = len(matched_mature) / len(cohort_by_id)
error_proportion = sum(errors) / len(matched_mature)
mean_loss = np.mean(mature_losses)
spread_loss = np.std(mature_losses, ddof=0)
  annotations: []
[TABLE computed result ] caption: Mature-cohort quantities for this unique-ID fixture. Reject duplicate prediction and label IDs before running this illustrative query; unmatched/late labels are excluded, not counted as successes.
  produced by sql: WITH cohort AS (SELECT * FROM predictions WHERE cohort_id='fixed_100' AND eligible=1), unique_labels AS (SELECT * FROM labels WHERE prediction_id IN (SELECT prediction_id FROM labels GROUP BY prediction_id HAVING COUNT(*)=1)), mature AS (SELECT c.*,l.label,l.loss,l.label_timestamp FROM cohort c JOIN unique_labels l USING(prediction_id) WHERE l.label_timestamp<='2026-01-04T00:00:00Z' AND (epoch(CAST('2026-01-04T00:00:00Z' AS TIMESTAMP))-epoch(CAST(c.prediction_timestamp AS TIMESTAMP)))/3600>=24) SELECT 'fixed_100' AS cohort_id,(SELECT COUNT(*) FROM cohort) AS eligible_ids,COUNT(*) AS matched_mature_ids,1.0*COUNT(*)/(SELECT COUNT(*) FROM cohort) AS maturity,SUM(CASE WHEN prediction!=label THEN 1 ELSE 0 END) AS matched_errors,1.0*SUM(CASE WHEN prediction!=label THEN 1 ELSE 0 END)/COUNT(*) AS mature_error_proportion,AVG(loss) AS mean_loss,sqrt(GREATEST(0,AVG(loss*loss)-AVG(loss)*AVG(loss))) AS stddev_loss,0 AS ddof FROM mature
  result columns=['cohort_id', 'eligible_ids', 'matched_mature_ids', 'maturity', 'matched_errors', 'mature_error_proportion', 'mean_loss', 'stddev_loss', 'ddof'] rows(1)=[["fixed_100",100,60,0.6,6,0.1,0.1,0.3,0]]
[TABLE computed result ] caption: Identity-preserving mature join with retained timestamps.
  produced by sql: WITH cohort AS (SELECT * FROM predictions WHERE cohort_id='fixed_100' AND eligible=1), unique_labels AS (SELECT * FROM labels WHERE prediction_id IN (SELECT prediction_id FROM labels GROUP BY prediction_id HAVING COUNT(*)=1)), mature AS (SELECT c.*,l.label,l.loss,l.label_timestamp FROM cohort c JOIN unique_labels l USING(prediction_id) WHERE l.label_timestamp<='2026-01-04T00:00:00Z' AND (epoch(CAST('2026-01-04T00:00:00Z' AS TIMESTAMP))-epoch(CAST(c.prediction_timestamp AS TIMESTAMP)))/3600>=24) SELECT prediction_id,prediction_timestamp,label_timestamp,prediction,label,loss FROM mature
  result columns=['prediction_id', 'prediction_timestamp', 'label_timestamp', 'prediction', 'label', 'loss'] rows(60)=[["p001","2026-01-02 10:00:00","2026-01-03 10:00:00","late","on_time",1],["p002","2026-01-02 10:00:00","2026-01-03 10:00:00","on_time","late",1],["p003","2026-01-02 10:00:00","2026-01-03 10:00:00","on_time","late",1],["p004","2026-01-02 10:00:00","2026-01-03 10:00:00","late","on_time",1],["p005","2026-01-02 10:00:00","2026-01-03 10:00:00","on_time","late",1],["p006","2026-01-02 10:00:00","2026-01-03 10:00:00","on_time","late",1],["p007","2026-01-02 10:00:00","2026-01-03 10:00:00","late","late",0

### s02 · explainer · Measure production model quality when labels arrive
(mechanism) For standard deviation, use np.std(numeric_values, ddof=0), which divides squared deviations by N and then takes the square root; use ddof=1 only if the stated calculation requires the N−1 divisor. ⟦A.f7 A:tb4⟧

### s03 · explainer · Apply the rule: Measure production model quality when labels arrive
(example) Keep the fixed cohort separate from newer predictions. Reject duplicate identities before dictionary construction; record unmatched or unavailable labels separately. Maturity uses all eligible prediction IDs as its denominator. Quality uses only matched mature observations, with label coverage reported alongside it. Compute loss summaries on those specified observations. Missing labels are not successful predictions, and the mature subset does not automatically estimate quality for all traffic. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb5⟧

### s04 · explainer · Work the contrast: Measure production model quality when labels arrive
(misconception) An absent label is not a correct prediction. Quality and maturity use different denominators, and a matched mature subset does not automatically represent all production traffic. ⟦A.f3 A.f4 A.f5 A:tb6⟧

### s05 · check · Review measure production model quality when labels arrive
Check the distinction — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [choice, intro, grading=client] For mature labeled losses in the selected cohort, the requested spread uses the N divisor. Which calculations satisfy that request?
  ✔ o1: np.mean(losses) and np.std(losses, ddof=0)
      why: Both calculations use the supplied mature losses; ddof=0 uses N.
  ✘ o2: np.mean(losses) and np.std(losses, ddof=1)
      why: This substitutes the N-1 divisor for the requested N divisor.
  ✘ o3: Compute the mean on mature losses but the spread on all unmatched predictions
      why: The requested statistics are over the same selected numeric observations, not different populations.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Keep the selected observations and divisor together.']  remediation→r01
  MEASURES: A:compute_mean_and_declared_standard_deviation_of_mature_losses(f6,f7)   anchors=[]
  taught-before-tested: A.f6←s01; A.f7←s02

### s06 · hands_on · Apply measure production model quality when labels arrive
Practice — Complete the learner-defined function and required imports under the supplied policy; use the declared cases to verify the single deliverable.
QUESTION [code_exercise, core, grading=client] Complete the missing statistics in the supplied scaffold, then inspect the report or replay results.

Complete loss_mean(losses) and loss_std(losses) using np.mean and np.std with ddof=0. Retain the supplied bounded prediction cohort, label reconciliation, matched-denominator coverage and unresolved-state handling unchanged. Report the matched examples’ loss mean and population standard deviation.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy']} constraints.allowed=['import numpy as np', 'import statements for required supplied library or client dependencies', 'def', 'return', 'variable assignment', 'dictionary literals', 'dictionary key lookup and assignment', 'for loops', 'if and else', 'membership tests', 'comparison operators', 'list literals and append', 'len', 'sum', 'arithmetic operators', 'numeric literals', 'string literals', 'np.mean(numeric_values)', 'np.std(numeric_values, ddof=0)', 'np.std(numeric_values, ddof=1)'] blocked=0 items
  file learner.py [editable]:
# Supplied infrastructure helper (retain unchanged).
exec('def coverage_calculation(matched, cohort):\n    return len(matched) / len(cohort)\n')

def loss_mean(losses):
    return None

def loss_std(losses):
    return None

import numpy as np

exec("def quality(prediction_rows, label_rows):\n    cohort = {}\n    rejected = []\n    seen_prediction_ids = {}\n    seen = {}\n    for row in prediction_rows:\n        key = row['prediction_id']\n        if key in seen_prediction_ids:\n            return {'status': 'duplicate_prediction'}\n        seen_prediction_ids[key] = row\n    for row in label_rows:\n        key = row['prediction_id']\n        if key in seen:\n            return {'status': 'duplicate_label'}\n        seen[key] = row\n    for row in prediction_rows:\n        key = row['prediction_id']\n        if row['eligible'] and row['cohort_id'] == policy['cohort']:\n            cohort[key] = row\n    matched = {}\n    losses = []\n    errors = []\n    for row in label_rows:\n        key = row['prediction_id']\n        if key in cohort and cohort[key]['prediction_timestamp'] <= cutoff and (row['label_timestamp'] <= policy['label_available_through']):\n            matched[key] = row\n            losses.append(row['loss'])\n            errors.append(cohort[key]['prediction'] != row['label'])\n        else:\n            rejected.append(key)\n    if len(matched) == 0:\n        return {'status': 'unavailable', 'cohort': cohort, 'matched': matched, 'eligible_ids': len(cohort), 'mature_ids': len(matched), 'coverage': coverage_calculation(matched, cohort) if len(cohort) > 0 else None, 'errors': None, 'error_proportion': None, 'loss_mean': None, 'loss_std': None, 'excluded_label_ids': rejected}\n    return {'status': 'mature_cohort_only', 'cohort': cohort, 'matched': matched, 'eligible_ids': len(cohort), 'mature_ids': len(matched), 'coverage': coverage_calculation(matched, cohort), 'errors': sum(errors), 'error_proportion': sum(errors) / len(matched), 'loss_mean': loss_mean(losses), 'loss_std': loss_std(losses), 'excluded_label_ids': rejected}\n")

exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"cohort": "fixed_100", "analysis_time": "2026-01-04T00:00:00Z", "minimum_age_hours": 24, "label_available_through": "2026-01-04T00:00:00Z", "duplicate_policy": "reject repeated prediction or label ID before dictionary construction", "unmatched_policy": "exclude and record", "outside_cohort_policy": "exclude and record", "ddof": 0}\')')

exec("predictions_rows = list(csv.DictReader(open('predictions.csv')))")

exec('predictions = {}')

exec("predictions['prediction_id'] = np.array([r['prediction_id'] for r in predictions_rows])")

exec("predictions['prediction_timestamp'] = np.array([r['prediction_timestamp'] for r in predictions_rows])")

exec("predictions['prediction'] = np.array([r['prediction'] for r in predictions_rows])")

exec("predictions['cohort_id'] = np.array([r['cohort_id'] for r in predictions_rows])")

exec("predictions['eligible'] = np.array([r['eligible'] == 'True' for r in predictions_rows])")

exec("labels_rows = list(csv.DictReader(open('labels.csv')))")

exec('labels = {}')

exec("labels['prediction_id'] = np.array([r['prediction_id'] for r in labels_rows])")

exec("labels['label_timestamp'] = np.array([r['label_timestamp'] for r in labels_rows])")

exec("labels['label'] = np.array([r['label'] for r in labels_rows])")

exec("labels['loss'] = np.array([float(r['loss'] or 'nan') for r in labels_rows])")

exec('from datetime import datetime, timedelta')

exec("def typed_rows(columns):\n    return [{k: v[i].item() if hasattr(v[i], 'item') else v[i] for k, v in columns.items()} for i in range(len(next(iter(columns.values()))))]")

exec('prediction_rows = typed_rows(predictions)')

exec('label_rows = typed_rows(labels)')

exec("cutoff = (datetime.fromisoformat(policy['analysis_time'].replace('Z', '+00:00')) - timedelta(hours=policy['minimum_age_hours'])).isoformat().replace('+00:00', 'Z')")

exec('result = quality(prediction_rows, label_rows)')

exec('outside_prediction = dict(prediction_rows[0], eligible=False)')

exec('outside_duplicate_rows = [outside_prediction, dict(outside_prediction)]')

  SOLUTION learner.py:
# Supplied infrastructure helper (retain unchanged).
exec('def coverage_calculation(matched, cohort):\n    return len(matched) / len(cohort)\n')

def loss_mean(losses):
    return np.mean(losses)

def loss_std(losses):
    return np.std(losses, ddof=0)

import numpy as np

exec("def quality(prediction_rows, label_rows):\n    cohort = {}\n    rejected = []\n    seen_prediction_ids = {}\n    seen = {}\n    for row in prediction_rows:\n        key = row['prediction_id']\n        if key in seen_prediction_ids:\n            return {'status': 'duplicate_prediction'}\n        seen_prediction_ids[key] = row\n    for row in label_rows:\n        key = row['prediction_id']\n        if key in seen:\n            return {'status': 'duplicate_label'}\n        seen[key] = row\n    for row in prediction_rows:\n        key = row['prediction_id']\n        if row['eligible'] and row['cohort_id'] == policy['cohort']:\n            cohort[key] = row\n    matched = {}\n    losses = []\n    errors = []\n    for row in label_rows:\n        key = row['prediction_id']\n        if key in cohort and cohort[key]['prediction_timestamp'] <= cutoff and (row['label_timestamp'] <= policy['label_available_through']):\n            matched[key] = row\n            losses.append(row['loss'])\n            errors.append(cohort[key]['prediction'] != row['label'])\n        else:\n            rejected.append(key)\n    if len(matched) == 0:\n        return {'status': 'unavailable', 'cohort': cohort, 'matched': matched, 'eligible_ids': len(cohort), 'mature_ids': len(matched), 'coverage': coverage_calculation(matched, cohort) if len(cohort) > 0 else None, 'errors': None, 'error_proportion': None, 'loss_mean': None, 'loss_std': None, 'excluded_label_ids': rejected}\n    return {'status': 'mature_cohort_only', 'cohort': cohort, 'matched': matched, 'eligible_ids': len(cohort), 'mature_ids': len(matched), 'coverage': coverage_calculation(matched, cohort), 'errors': sum(errors), 'error_proportion': sum(errors) / len(matched), 'loss_mean': loss_mean(losses), 'loss_std': loss_std(losses), 'excluded_label_ids': rejected}\n")

exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"cohort": "fixed_100", "analysis_time": "2026-01-04T00:00:00Z", "minimum_age_hours": 24, "label_available_through": "2026-01-04T00:00:00Z", "duplicate_policy": "reject repeated prediction or label ID before dictionary construction", "unmatched_policy": "exclude and record", "outside_cohort_policy": "exclude and record", "ddof": 0}\')')

exec("predictions_rows = list(csv.DictReader(open('predictions.csv')))")

exec('predictions = {}')

exec("predictions['prediction_id'] = np.array([r['prediction_id'] for r in predictions_rows])")

exec("predictions['prediction_timestamp'] = np.array([r['prediction_timestamp'] for r in predictions_rows])")

exec("predictions['prediction'] = np.array([r['prediction'] for r in predictions_rows])")

exec("predictions['cohort_id'] = np.array([r['cohort_id'] for r in predictions_rows])")

exec("predictions['eligible'] = np.array([r['eligible'] == 'True' for r in predictions_rows])")

exec("labels_rows = list(csv.DictReader(open('labels.csv')))")

exec('labels = {}')

exec("labels['prediction_id'] = np.array([r['prediction_id'] for r in labels_rows])")

exec("labels['label_timestamp'] = np.array([r['label_timestamp'] for r in labels_rows])")

exec("labels['label'] = np.array([r['label'] for r in labels_rows])")

exec("labels['loss'] = np.array([float(r['loss'] or 'nan') for r in labels_rows])")

exec('from datetime import datetime, timedelta')

exec("def typed_rows(columns):\n    return [{k: v[i].item() if hasattr(v[i], 'item') else v[i] for k, v in columns.items()} for i in range(len(next(iter(columns.values()))))]")

exec('prediction_rows = typed_rows(predictions)')

exec('label_rows = typed_rows(labels)')

exec("cutoff = (datetime.fromisoformat(policy['analysis_time'].replace('Z', '+00:00')) - timedelta(hours=policy['minimum_age_hours'])).isoformat().replace('+00:00', 'Z')")

exec('result = quality(prediction_rows, label_rows)')

exec('outside_prediction = dict(prediction_rows[0], eligible=False)')

exec('outside_duplicate_rows = [outside_prediction, dict(outside_prediction)]')

  test t1 (value_equals, visible=True): {"expr":"result","expected":{"status":"mature_cohort_only","cohort":{"p001":{"prediction_id":"p001","prediction_timestamp":"2026-01-02T10:00:00Z","prediction":"late","cohort_id":"fixed_100","eligible":true},"p002":{"prediction_id":"p002","prediction_timestamp":"2026-01-02T10:00:00Z","prediction":"on_time","cohort_id":"fixed_100","eligible":true},"p003":{"prediction_id":"p003","prediction_timestamp":"2026-01-02T10:00:00Z","prediction":"on_time","cohort_id":"fixed_100","eligible":true},"p004":{"pr | on-fail: The returned record or calculation does not match the declared fixture contract.
  test excluded_prediction_duplicates (function_call, visible=True): {"function":"quality","args":[[{"prediction_id":"p001","prediction_timestamp":"2026-01-02T10:00:00Z","prediction":"late","cohort_id":"fixed_100","eligible":false},{"prediction_id":"p001","prediction_timestamp":"2026-01-02T10:00:00Z","prediction":"late","cohort_id":"fixed_100","eligible":false}],[{"prediction_id":"p001","label_timestamp":"2026-01-03T10:00:00Z","label":"on_time","loss":1},{"prediction_id":"p002","label_timestamp":"2026-01-03T10:00:00Z","label":"late","loss":1},{"prediction_id":"p0 | on-fail: The returned record or calculation does not match the declared fixture contract.
  test excluded_prediction_control (function_call, visible=True): {"function":"quality","args":[[{"prediction_id":"p001","prediction_timestamp":"2026-01-02T10:00:00Z","prediction":"late","cohort_id":"fixed_100","eligible":false}],[]],"expected":{"status":"unavailable","cohort":{},"matched":{},"eligible_ids":0,"mature_ids":0,"coverage":null,"errors":null,"error_proportion":null,"loss_mean":null,"loss_std":null,"excluded_label_ids":[]}} | on-fail: The returned record or calculation does not match the declared fixture contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"7779d1a66006df5c0684bfbc0379fafa1488727b8d2bde74f2f7d91847b1f324","tests_passed":3}
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Check duplicate IDs across each complete input before filtering; compare prediction timestamps with cutoff and label timestamps with label_available_through.']
  MEASURES: A:preserve_and_join_a_time_bounded_prediction_cohort(f1,f2,f3); A:compute_label_maturity_and_scope_quality_estimates(f4,f5); A:compute_mean_and_declared_standard_deviation_of_mature_losses(f6,f7)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01; A.f5←s01; A.f6←s01; A.f7←s02

### s07 · explainer · Configure actionable model and service alerts
(intro) An actionable alert needs an indicator, window rule, owner and response. Apply the supplied noise-tolerant rule rather than treating every fluctuation as a breach. ⟦B:tb1⟧
(mechanism) Distinguish, using the baseline measurement window and indicator definition, normal variability from an actionable breach. Write the existing alert’s indicator, threshold/window rule, owner and response in its YAML schema, then inspect the parsed configuration before replay. Apply the declared noise-tolerant threshold rule to the computed baseline mean/spread, rather than alerting on every single fluctuation. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Replay normal and breached windows, checking that only the configured breach produces the intended owner/action record. For the arithmetic mean, use np.mean(numeric_values) on the selected numeric observations. For standard deviation, use np.std(numeric_values, ddof=0), which divides squared deviations by N and then takes the square root; use ddof=1 only if the stated calculation requires the N−1 divisor. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[CODE python]
import numpy as np
import yaml
baseline_mean = np.mean(baseline_values)
baseline_spread = np.std(baseline_values, ddof=0)
with open(config_path, "w") as handle:
    yaml.safe_dump(config, handle)
with open(config_path) as handle:
    resolved = yaml.safe_load(handle)
# Inspect indicator, window rule, owner and response before replay.
assert normal_record is None
assert boundary_record is None
assert breached_record["owner"] == resolved["owner"]
  annotations: []
[TABLE computed result ] caption: Baseline/window statistics and configured breach-only owner/action record; replay assertions still require execution evidence.
  produced by sql: WITH stats AS (SELECT window_id,COUNT(*) AS observations,AVG(numeric_values) AS mean,sqrt(GREATEST(0,AVG(numeric_values*numeric_values)-AVG(numeric_values)*AVG(numeric_values))) AS stddev FROM observations GROUP BY window_id), replay AS (SELECT *,mean>(SELECT mean FROM stats WHERE window_id='baseline')+4 AS breach FROM stats) SELECT *,0 AS ddof,'window_mean' AS indicator,'mean(window)>mean(baseline)+4' AS window_rule,CASE WHEN breach THEN 'order_oncall' END AS owner,CASE WHEN breach THEN 'investigate_window' END AS response FROM replay
  result columns=['window_id', 'observations', 'mean', 'stddev', 'breach', 'ddof', 'indicator', 'window_rule', 'owner', 'response'] rows(4)=[["baseline",3,4,1.6329931618554525,false,0,"window_mean","mean(window)>mean(baseline)+4",null,null],["normal",3,4,0.8164965809277268,false,0,"window_mean","mean(window)>mean(baseline)+4",null,null],["boundary",3,8,0.8164965809277289,false,0,"window_mean","mean(window)>mean(baseline)+4",null,null],["breached",3,10,0.8164965809277289,true,0,"window_mean","mean(window)>mean(baseline)+4","order_oncall","investigate_window"]]

### s08 · explainer · Configure actionable model and service alerts
(mechanism) Use assert predicates for declared valid, boundary and failure cases; a false predicate raises AssertionError in ordinary non-optimized execution. Using the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors. ⟦B.f7 B.f8 B:tb4⟧

### s09 · explainer · Apply the rule: Configure actionable model and service alerts
(example) Use the fixture’s baseline, indicator, window rule, owner and response. Compute the requested mean and spread, then write and reload the existing YAML fields. Inspect what the runtime will read. Replay normal, boundary and breached cases with assertions: an owner/action record belongs only to a qualifying breach. Formatting alone does not verify behavior; a predicate alone does not verify the actionable outcome. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B:tb5⟧
(misconception) An indicator changing slightly is not necessarily an actionable breach. A configured alert also needs a tested owner/action outcome under the stated window and noise rule. ⟦B.f1 B.f3 B.f4 B:tb6⟧

### s10 · check · Review configure actionable model and service alerts
Check the distinction — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [choice, core, grading=client] Replay checks run without Python optimization. The rule is mean(window)>threshold. Which acceptance check covers normal, exact-boundary and breached windows?
  ✔ o1: Assert no owner/action record for normal or equality; assert the configured owner/action only for a crossing
      why: These assertions verify the declared valid, boundary and breach outputs.
  ✘ o2: Assert an owner/action record for every window
      why: Normal and equality windows do not satisfy this breach rule.
  ✘ o3: Record predicates as comments instead of assertions
      why: Comments do not check predicates; a false assert raises AssertionError in ordinary execution.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Trace equality separately from a strict crossing.']  remediation→r03
  MEASURES: B:verify_breach_only_owner_action_output(f4,f7)   anchors=[]
  taught-before-tested: B.f4←s07; B.f7←s08

### s11 · hands_on · Apply configure actionable model and service alerts
Practice — Complete the learner-defined function and required imports under the supplied policy; use the declared cases to verify the single deliverable.
QUESTION [code_exercise, core, grading=client] Complete the missing statistics in the supplied scaffold, then inspect the report or replay results.

Complete baseline_mean and baseline_std using np.mean and np.std with ddof=0. Retain the supplied indicator, baseline window, mean-plus-margin threshold configuration, owner/response binding, safe YAML round trip and replay assertions unchanged. The replay must alert on the violating fixture and remain quiet on the nonviolating fixture.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy', 'pyyaml']} constraints.allowed=['import numpy as np', 'import yaml', 'variable assignment', 'numeric and string literals', 'mapping and list literals', 'mapping and list indexing', 'np.mean(numeric_values)', 'np.std(numeric_values, ddof=0)', 'np.std(numeric_values, ddof=1) only when the declared calculation requires the N−1 divisor', 'arithmetic operators', 'comparison operators', 'Boolean operators', 'with open(...) as file_handle', 'yaml.safe_dump(config, file_handle)', 'yaml.safe_load(file_handle)', 'assert predicate', 'calls to the supplied existing-runtime replay helper'] blocked=5 items
  file learner.py [editable]:
exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"indicator": "window_mean", "baseline_window": "baseline", "window_rule": "mean(window)>mean(baseline)+4", "ddof": 0, "owner": "order_oncall", "response": "investigate_window", "expected_replays": {"normal": false, "boundary": false, "breached": true}}\')')

exec("alert_observations_rows = list(csv.DictReader(open('alert_observations.csv')))")

exec('alert_observations = {}')

exec("alert_observations['window_id'] = np.array([r['window_id'] for r in alert_observations_rows])")

exec("alert_observations['numeric_values'] = np.array([float(r['numeric_values'] or 'nan') for r in alert_observations_rows])")

exec('import yaml')

exec("baseline = alert_observations['numeric_values'][alert_observations['window_id'] == 'baseline']")

exec("windows = {w: alert_observations['numeric_values'][alert_observations['window_id'] == w] for w in ['normal', 'boundary', 'breached']}")

exec("def replay(config):\n    results = []\n    for w, values in windows.items():\n        crossed = np.mean(values) > config['threshold']\n        results.append({'window': w, 'mean': np.mean(values), 'std': np.std(values, ddof=config['ddof']), 'records': [{'owner': config['owner'], 'action': config['response']}] if crossed else []})\n    return results")

exec("def serializable(config):\n    config = dict(config)\n    config['threshold'] = float(config['threshold'])\n    return config")

baseline_mean = None

baseline_std = None

config = {'indicator': policy['indicator'], 'baseline_window': policy['baseline_window'], 'threshold': baseline_mean + 4, 'ddof': policy['ddof'], 'owner': policy['owner'], 'response': policy['response']}

serializable_config = serializable(config)

serialized_config = yaml.safe_dump(serializable_config)

with open('alert.yaml', 'w') as h:
    h.write(serialized_config)

with open('alert.yaml') as h:
    config_text = h.read()

resolved = yaml.safe_load(config_text)

assert resolved == config

result = replay(resolved)

assert result[0]['records'] == []

assert result[1]['records'] == []
assert result[2]['records'] == [{'owner': resolved['owner'], 'action': resolved['response']}]

  SOLUTION learner.py:
exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"indicator": "window_mean", "baseline_window": "baseline", "window_rule": "mean(window)>mean(baseline)+4", "ddof": 0, "owner": "order_oncall", "response": "investigate_window", "expected_replays": {"normal": false, "boundary": false, "breached": true}}\')')

exec("alert_observations_rows = list(csv.DictReader(open('alert_observations.csv')))")

exec('alert_observations = {}')

exec("alert_observations['window_id'] = np.array([r['window_id'] for r in alert_observations_rows])")

exec("alert_observations['numeric_values'] = np.array([float(r['numeric_values'] or 'nan') for r in alert_observations_rows])")

exec('import yaml')

exec("baseline = alert_observations['numeric_values'][alert_observations['window_id'] == 'baseline']")

exec("windows = {w: alert_observations['numeric_values'][alert_observations['window_id'] == w] for w in ['normal', 'boundary', 'breached']}")

exec("def replay(config):\n    results = []\n    for w, values in windows.items():\n        crossed = np.mean(values) > config['threshold']\n        results.append({'window': w, 'mean': np.mean(values), 'std': np.std(values, ddof=config['ddof']), 'records': [{'owner': config['owner'], 'action': config['response']}] if crossed else []})\n    return results")

exec("def serializable(config):\n    config = dict(config)\n    config['threshold'] = float(config['threshold'])\n    return config")

baseline_mean = np.mean(baseline)

baseline_std = np.std(baseline, ddof=0)

config = {'indicator': policy['indicator'], 'baseline_window': policy['baseline_window'], 'threshold': baseline_mean + 4, 'ddof': policy['ddof'], 'owner': policy['owner'], 'response': policy['response']}

serializable_config = serializable(config)

serialized_config = yaml.safe_dump(serializable_config)

with open('alert.yaml', 'w') as h:
    h.write(serialized_config)

with open('alert.yaml') as h:
    config_text = h.read()

resolved = yaml.safe_load(config_text)

assert resolved == config

result = replay(resolved)

assert result[0]['records'] == []

assert result[1]['records'] == []
assert result[2]['records'] == [{'owner': resolved['owner'], 'action': resolved['response']}]

  test t1 (value_equals, visible=True): {"expr":"baseline_mean","expected":4} | on-fail: The returned record or calculation does not match the declared fixture contract.
  test t2 (value_equals, visible=True): {"expr":"baseline_std","expected":1.632993161855452} | on-fail: The returned record or calculation does not match the declared fixture contract.
  test t3 (value_equals, visible=True): {"expr":"resolved","expected":{"baseline_window":"baseline","ddof":0,"indicator":"window_mean","owner":"order_oncall","response":"investigate_window","threshold":8}} | on-fail: The returned record or calculation does not match the declared fixture contract.
  test t4 (value_equals, visible=True): {"expr":"result","expected":[{"window":"normal","mean":4,"std":0.816496580927726,"records":[]},{"window":"boundary","mean":8,"std":0.816496580927726,"records":[]},{"window":"breached","mean":10,"std":0.816496580927726,"records":[{"owner":"order_oncall","action":"investigate_window"}]}]} | on-fail: The returned record or calculation does not match the declared fixture contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"4fda942b6a4058c7a03e839da720393c25897a707860a96d32c61cb17f45a1e4","tests_passed":4}
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['baseline and policy supply the configuration inputs. Compare resolved fields before inspecting each replay window’s records.']
  MEASURES: B:select_noise_tolerant_alert_condition(f1,f3,f5,f6); B:identify_configured_owner_and_actionable_response(f2,f8); B:verify_breach_only_owner_action_output(f4,f7)   anchors=['practice']
  taught-before-tested: B.f1←s07; B.f3←s07; B.f5←s07; B.f6←s07; B.f2←s07; B.f8←s08; B.f4←s07; B.f7←s08

### s12 · explainer · Triage a production regression to select data repair, rollback or gated retraining
(intro) A release preceded worse client outcomes. That timeline is a starting point, not a cause. Gather release, data, service and mature-label evidence, then test one supported hypothesis. ⟦C:tb1⟧
(mechanism) Start triage with client-visible impact and the available timeline, deployment, data, service and quality evidence. A schema/value failure identifies data conditions to investigate, whereas a distribution difference alone does not prove labeled model-quality degradation. Compare the active artifact/configuration identities with the approved deployment and run record when investigating a release-correlated regression. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) Check matched mature-label evidence before selecting a response justified specifically by prediction-quality degradation. Select the supplied supported action—data repair, approved rollback or gated retraining—under the existing incident policy and preserve the required validation gates. Calculate conditional labeled error rates for each release/cohort on matched eligible labels, keeping their conditioning counts distinct. ⟦C.f4 C.f5 C.f6 C:tb3⟧
(mechanism) Reproduce and isolate the regression from the release/telemetry timeline, test one causal hypothesis against the evidence and choose only the supported response. ⟦C.f7 C:tb4⟧
[TABLE computed result ] caption: Timeline, approved-versus-active identities, mature-label denominators and tested hypothesis evidence.
  produced by sql: SELECT *,1.0*labeled_errors/NULLIF(matched_eligible_labels,0) AS conditional_error_rate FROM evidence ORDER BY timestamp
  result columns=['release_id', 'cohort_id', 'timestamp', 'active_artifact', 'approved_artifact', 'active_config', 'approved_config', 'schema_pass', 'distribution_distance', 'matched_eligible_labels', 'labeled_errors', 'client_impact', 'hypothesis_test', 'supported_response', 'conditional_error_rate'] rows(3)=[["r1","before","2026-01-02 09:00:00","model.r1","model.r1","cfg.r1","cfg.r1",true,0,60,6,"baseline","approved configuration reproduces baseline","none",0.1],["r2","after","2026-01-02 11:00:00","model.r2","model.r2","cfg.bad","cfg.r2",true,0.3,40,12,"more incorrect arrival predictions","bad configuration reproduces errors; approved rollback restores baseline","approved_rollback",0.3],["r2","incomplete","2026-01-03 23:00:00","model.r2","model.r2","cfg.bad","cfg.r2",true,0.3,0,0,"quality unresolve

### s13 · explainer · Apply the rule: Triage a production regression to select data repair, rollback or gated retraining
(example) Compare active artifact and configuration identities with the approved run. Investigate a failed schema as a data condition; do not call distribution difference labeled degradation. Keep each release/cohort’s mature matched denominator separate. Reproduce and isolate the regression, then test the configuration-mismatch hypothesis against the fixture evidence. Choose only a supported data repair, approved rollback or gated retraining response, preserving validation. Timing and class mix alone do not establish cause. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C:tb5⟧

### s14 · explainer · Work the contrast: Triage a production regression to select data repair, rollback or gated retraining
(misconception) A release-correlated timeline is not itself a causal diagnosis. Distribution evidence alone does not justify a prediction-quality claim, and any response must preserve the existing gates. ⟦C.f2 C.f4 C.f5 C.f7 C:tb6⟧

### s15 · check · Review triage a production regression to select data repair, rollback or gated retraining
Check the distinction — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [choice, stretch, grading=client] The supplied policy authorizes rollback after a configuration-mismatch hypothesis is reproduced and an approved-configuration replay restores baseline. Readiness and bounded prediction remain required. Which response follows that evidence and policy?
  ✔ o1: Select the approved rollback and retain both validation gates
      why: The hypothesis has distinguishing evidence and the approved action keeps required gates.
  ✘ o2: Rollback but skip readiness because reproduction succeeded
      why: Evidence supporting an action does not remove required post-action validation gates.
  ✘ o3: Select retraining solely because the input distribution changed
      why: Distribution change alone does not establish quality degradation or justify replacing the supplied supported response.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Keep the evidence-supported action and its required gates together.']  remediation→r05
  MEASURES: C:select_evidence_supported_response_with_required_gates(f5,f7)   anchors=[]
  taught-before-tested: C.f5←s12; C.f7←s12

### s16 · hands_on · Apply triage a production regression to select data repair, rollback or gated retraining
Practice — Complete the learner-defined function and required imports under the supplied policy; use the declared cases to verify the single deliverable.
QUESTION [code_exercise, intro, grading=client] Complete has_labels by comparing matched_counts with zero. Retain the supplied group-rate loop and evidence ledger unchanged. Groups with no matched labels must retain an unresolved rate rather than be reported as zero-error.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy']} constraints.allowed=['variable assignment', 'numeric, string, Boolean and None literals', 'lists and dictionaries', 'dictionary indexing', 'for loops', 'if/elif/else statements', 'comparison operators', 'Boolean mask operators & and |', 'parenthesized expressions', 'NumPy array indexing with Boolean masks', 'np.count_nonzero(...)', 'division guarded by a nonzero denominator', 'assert statements'] blocked=3 items
  file learner.py [editable]:
exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"permitted_responses": ["data_repair", "approved_rollback", "gated_retraining"], "selected_fixture_authorization": "approved rollback cfg.bad -> cfg.r1 under lab.operator; readiness and bounded prediction gates required", "quality_denominator": "matched_eligible_labels; zero means undefined", "hypothesis": "configuration mismatch, distinguished by approved-configuration replay"}\')')

exec("release_evidence_rows = list(csv.DictReader(open('release_evidence.csv')))")

exec('release_evidence = {}')

exec("release_evidence['release_id'] = np.array([r['release_id'] for r in release_evidence_rows])")

exec("release_evidence['cohort_id'] = np.array([r['cohort_id'] for r in release_evidence_rows])")

exec("release_evidence['timestamp'] = np.array([r['timestamp'] for r in release_evidence_rows])")

exec("release_evidence['active_artifact'] = np.array([r['active_artifact'] for r in release_evidence_rows])")

exec("release_evidence['approved_artifact'] = np.array([r['approved_artifact'] for r in release_evidence_rows])")

exec("release_evidence['active_config'] = np.array([r['active_config'] for r in release_evidence_rows])")

exec("release_evidence['approved_config'] = np.array([r['approved_config'] for r in release_evidence_rows])")

exec("release_evidence['schema_pass'] = np.array([r['schema_pass'] == 'True' for r in release_evidence_rows])")

exec("release_evidence['distribution_distance'] = np.array([float(r['distribution_distance'] or 'nan') for r in release_evidence_rows])")

exec("release_evidence['matched_eligible_labels'] = np.array([float(r['matched_eligible_labels'] or 'nan') for r in release_evidence_rows])")

exec("release_evidence['labeled_errors'] = np.array([float(r['labeled_errors'] or 'nan') for r in release_evidence_rows])")

exec("release_evidence['client_impact'] = np.array([r['client_impact'] for r in release_evidence_rows])")

exec("release_evidence['hypothesis_test'] = np.array([r['hypothesis_test'] for r in release_evidence_rows])")

exec("release_evidence['supported_response'] = np.array([r['supported_response'] for r in release_evidence_rows])")

exec("evidence = [{k: v[i].item() if hasattr(v[i], 'item') else v[i] for k, v in release_evidence.items()} for i in range(len(release_evidence_rows))]")

exec("matched_counts = release_evidence['matched_eligible_labels']")

exec("error_counts = release_evidence['labeled_errors']")

exec('rate_groups = list(range(len(matched_counts)))')

zero = 0

has_labels = None

selected_rates = []

for group in rate_groups:
    rate = None
    if has_labels[group]:
        rate = error_counts[group] / matched_counts[group]
    selected_rates = selected_rates + [rate]

exec('result = []')

exec("def diagnostic_record(row, rate, response, gates):\n    n = row['matched_eligible_labels']\n    errors = row['labeled_errors']\n    return {'release': row['release_id'], 'cohort': row['cohort_id'], 'timestamp': row['timestamp'], 'impact': row['client_impact'], 'active_artifact': row['active_artifact'], 'approved_artifact': row['approved_artifact'], 'active_config': row['active_config'], 'approved_config': row['approved_config'], 'hypothesis': policy['hypothesis'], 'hypothesis_test': row['hypothesis_test'], 'matched_eligible_labels': n, 'errors': errors, 'error_rate': rate, 'response': response, 'required_gates': gates, 'quality_claim': 'matched mature cohort only; distribution alone does not establish quality loss'}")

label_investigate = 'investigate'

label_approved_rollback = 'approved_rollback'

label_none = 'none'

for row in evidence:
    n = row['matched_eligible_labels']
    rate = selected_rates[len(result)]
    response = label_investigate
    gates = []
    mismatch_replay = row['active_config'] != row['approved_config'] and row['active_artifact'] == row['approved_artifact'] and n > 0 and row['schema_pass'] and row['hypothesis_test'] == 'bad configuration reproduces errors; approved rollback restores baseline' and row['supported_response'] == label_approved_rollback
    if mismatch_replay:
        response = label_approved_rollback
        gates = ['readiness', 'bounded_prediction']
    elif row['client_impact'] == 'baseline':
        response = label_none
    result = result + [diagnostic_record(row, rate, response, gates)]

  SOLUTION learner.py:
exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"permitted_responses": ["data_repair", "approved_rollback", "gated_retraining"], "selected_fixture_authorization": "approved rollback cfg.bad -> cfg.r1 under lab.operator; readiness and bounded prediction gates required", "quality_denominator": "matched_eligible_labels; zero means undefined", "hypothesis": "configuration mismatch, distinguished by approved-configuration replay"}\')')

exec("release_evidence_rows = list(csv.DictReader(open('release_evidence.csv')))")

exec('release_evidence = {}')

exec("release_evidence['release_id'] = np.array([r['release_id'] for r in release_evidence_rows])")

exec("release_evidence['cohort_id'] = np.array([r['cohort_id'] for r in release_evidence_rows])")

exec("release_evidence['timestamp'] = np.array([r['timestamp'] for r in release_evidence_rows])")

exec("release_evidence['active_artifact'] = np.array([r['active_artifact'] for r in release_evidence_rows])")

exec("release_evidence['approved_artifact'] = np.array([r['approved_artifact'] for r in release_evidence_rows])")

exec("release_evidence['active_config'] = np.array([r['active_config'] for r in release_evidence_rows])")

exec("release_evidence['approved_config'] = np.array([r['approved_config'] for r in release_evidence_rows])")

exec("release_evidence['schema_pass'] = np.array([r['schema_pass'] == 'True' for r in release_evidence_rows])")

exec("release_evidence['distribution_distance'] = np.array([float(r['distribution_distance'] or 'nan') for r in release_evidence_rows])")

exec("release_evidence['matched_eligible_labels'] = np.array([float(r['matched_eligible_labels'] or 'nan') for r in release_evidence_rows])")

exec("release_evidence['labeled_errors'] = np.array([float(r['labeled_errors'] or 'nan') for r in release_evidence_rows])")

exec("release_evidence['client_impact'] = np.array([r['client_impact'] for r in release_evidence_rows])")

exec("release_evidence['hypothesis_test'] = np.array([r['hypothesis_test'] for r in release_evidence_rows])")

exec("release_evidence['supported_response'] = np.array([r['supported_response'] for r in release_evidence_rows])")

exec("evidence = [{k: v[i].item() if hasattr(v[i], 'item') else v[i] for k, v in release_evidence.items()} for i in range(len(release_evidence_rows))]")

exec("matched_counts = release_evidence['matched_eligible_labels']")

exec("error_counts = release_evidence['labeled_errors']")

exec('rate_groups = list(range(len(matched_counts)))')

zero = 0

has_labels = matched_counts > zero

selected_rates = []

for group in rate_groups:
    rate = None
    if has_labels[group]:
        rate = error_counts[group] / matched_counts[group]
    selected_rates = selected_rates + [rate]

exec('result = []')

exec("def diagnostic_record(row, rate, response, gates):\n    n = row['matched_eligible_labels']\n    errors = row['labeled_errors']\n    return {'release': row['release_id'], 'cohort': row['cohort_id'], 'timestamp': row['timestamp'], 'impact': row['client_impact'], 'active_artifact': row['active_artifact'], 'approved_artifact': row['approved_artifact'], 'active_config': row['active_config'], 'approved_config': row['approved_config'], 'hypothesis': policy['hypothesis'], 'hypothesis_test': row['hypothesis_test'], 'matched_eligible_labels': n, 'errors': errors, 'error_rate': rate, 'response': response, 'required_gates': gates, 'quality_claim': 'matched mature cohort only; distribution alone does not establish quality loss'}")

label_investigate = 'investigate'

label_approved_rollback = 'approved_rollback'

label_none = 'none'

for row in evidence:
    n = row['matched_eligible_labels']
    rate = selected_rates[len(result)]
    response = label_investigate
    gates = []
    mismatch_replay = row['active_config'] != row['approved_config'] and row['active_artifact'] == row['approved_artifact'] and n > 0 and row['schema_pass'] and row['hypothesis_test'] == 'bad configuration reproduces errors; approved rollback restores baseline' and row['supported_response'] == label_approved_rollback
    if mismatch_replay:
        response = label_approved_rollback
        gates = ['readiness', 'bounded_prediction']
    elif row['client_impact'] == 'baseline':
        response = label_none
    result = result + [diagnostic_record(row, rate, response, gates)]

  test t1 (value_equals, visible=True): {"expr":"result","expected":[{"release":"r1","cohort":"before","timestamp":"2026-01-02T09:00:00Z","impact":"baseline","active_artifact":"model.r1","approved_artifact":"model.r1","active_config":"cfg.r1","approved_config":"cfg.r1","hypothesis":"configuration mismatch, distinguished by approved-configuration replay","hypothesis_test":"approved configuration reproduces baseline","matched_eligible_labels":60,"errors":6,"error_rate":0.1,"response":"none","required_gates":[],"quality_claim":"matched m | on-fail: The returned record or calculation does not match the declared fixture contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"adfe566caf59b92e7a808d33c8fbea863551ade48250da19774c12607c2160d9","tests_passed":1}
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Use `matched_counts > zero`; a zero denominator leaves that group’s rate unresolved.']
  MEASURES: C:localize_regression_and_test_causal_hypothesis(f1,f3,f7); C:distinguish_input_shift_from_matched_labeled_quality_loss(f2,f4,f6); C:select_evidence_supported_response_with_required_gates(f5,f7)   anchors=['practice']
  taught-before-tested: C.f1←s12; C.f3←s12; C.f7←s12; C.f2←s12; C.f4←s12; C.f6←s12; C.f5←s12; C.f7←s12

### s17 · recap · Keep these distinctions
(takeaway) Freeze cohorts before delayed-label joins and keep maturity separate from mature-cohort quality. Inspect alert configuration and verify breach-only owner/action behavior. Diagnose with matched evidence and a tested hypothesis, then preserve gates in the supported response.
[UP NEXT] Choose scheduled, new-data or investigated quality/drift retraining triggers: A schedule, new data or supported operational evidence may trigger retraining. Record the reason and intended dataset; eligibility to execute is not candidate deployment approval.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Measure production model quality when labels arrive
(mechanism) Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations. ⟦A.f6 A:tb3⟧
(mechanism) Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor. ⟦A.f7 A:tb4⟧
(misconception) Summarize only the selected mature matched losses. Keep the requested mean and spread divisor; missing labels are not zero-loss observations. ⟦A.f6 A.f7 A:tb3 A:tb4⟧
### r02 · Revisit: Measure production model quality when labels arrive
(mechanism) Use a prediction-ID dictionary to preserve cohort membership and prediction time before attaching delayed labels by key. ⟦A.f1 A:tb2⟧
(mechanism) Join only labels that belong to those prediction IDs and satisfy the declared availability boundary; unmatched labels and duplicate IDs need explicit handling. ⟦A.f2 A:tb2⟧
(mechanism) Define the prediction cohort and analysis delay so recent incomplete ground truth is not treated as a mature cohort. ⟦A.f3 A:tb2⟧
(mechanism) Estimate P(label mature | cohort) as mature eligible prediction IDs divided by all eligible prediction IDs in that cohort, retaining the denominator. ⟦A.f4 A:tb3⟧
(mechanism) Compute the declared quality quantity on the matched mature cohort and report its label coverage; without justified coverage it does not estimate quality for all traffic. ⟦A.f5 A:tb3⟧
(mechanism) Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations. ⟦A.f6 A:tb3⟧
(mechanism) Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor. ⟦A.f7 A:tb4⟧
(misconception) An absent label is not a correct prediction. Quality and maturity use different denominators, and a matched mature subset does not automatically represent all production traffic. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb2 A:tb3 A:tb4⟧
### r03 · Revisit: Configure actionable model and service alerts
(mechanism) Replay normal and breached windows, checking that only the configured breach produces the intended owner/action record. ⟦B.f4 B:tb3⟧
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦B.f7 B:tb4⟧
(misconception) A normal replay must not emit the breach owner/action record. A qualifying breached replay must emit it. Use assertions for valid, boundary and failure cases, not formatting alone. ⟦B.f4 B.f7 B:tb3 B:tb4⟧
### r04 · Revisit: Configure actionable model and service alerts
(mechanism) Use the baseline measurement window and indicator definition to distinguish normal variability from an actionable breach. ⟦B.f1 B:tb2⟧
(mechanism) Write the existing alert’s indicator, threshold/window rule, owner and response in its YAML schema, then inspect the parsed configuration before replay. ⟦B.f2 B:tb2⟧
(mechanism) Apply the declared noise-tolerant threshold rule to the computed baseline mean/spread, rather than alerting on every single fluctuation. ⟦B.f3 B:tb2⟧
(mechanism) Replay normal and breached windows, checking that only the configured breach produces the intended owner/action record. ⟦B.f4 B:tb3⟧
(mechanism) Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations. ⟦B.f5 B:tb3⟧
(mechanism) Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor. ⟦B.f6 B:tb3⟧
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦B.f7 B:tb4⟧
(mechanism) Import yaml from the declared PyYAML dependency. Write mappings/lists with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python constructors. ⟦B.f8 B:tb4⟧
(misconception) An indicator changing slightly is not necessarily an actionable breach. A configured alert also needs a tested owner/action outcome under the stated window and noise rule. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B:tb2 B:tb3 B:tb4⟧
### r05 · Revisit: Triage a production regression to select data repair, rollback or gated retraining
(mechanism) Select the supplied supported action—data repair, approved rollback or gated retraining—under the existing incident policy and preserve the required validation gates. ⟦C.f5 C:tb3⟧
(mechanism) Reproduce and isolate the regression from the release/telemetry timeline, test one causal hypothesis against the evidence and choose only the supported response. ⟦C.f7 C:tb4⟧
(misconception) A release-correlated timeline is not a causal test. Use the supported policy response only after testing the hypothesis; preserve required validation gates. ⟦C.f5 C.f7 C:tb3 C:tb4⟧
### r06 · Revisit: Triage a production regression to select data repair, rollback or gated retraining
(mechanism) Start triage with client-visible impact and the available timeline, deployment, data, service and quality evidence. ⟦C.f1 C:tb2⟧
(mechanism) A schema/value failure identifies data conditions to investigate, whereas a distribution difference alone does not prove labeled model-quality degradation. ⟦C.f2 C:tb2⟧
(mechanism) Compare the active artifact/configuration identities with the approved deployment and run record when investigating a release-correlated regression. ⟦C.f3 C:tb2⟧
(mechanism) Check matched mature-label evidence before selecting a response justified specifically by prediction-quality degradation. ⟦C.f4 C:tb3⟧
(mechanism) Select the supplied supported action—data repair, approved rollback or gated retraining—under the existing incident policy and preserve the required validation gates. ⟦C.f5 C:tb3⟧
(mechanism) Calculate conditional labeled error rates for each release/cohort on matched eligible labels, keeping their conditioning counts distinct. ⟦C.f6 C:tb3⟧
(mechanism) Reproduce and isolate the regression from the release/telemetry timeline, test one causal hypothesis against the evidence and choose only the supported response. ⟦C.f7 C:tb4⟧
(misconception) A release-correlated timeline is not itself a causal diagnosis. Distribution evidence alone does not justify a prediction-quality claim, and any response must preserve the existing gates. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C:tb2 C:tb3 C:tb4⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: yaml.unsafe_load(...)
· constraints.blocked_syntax: yaml.load(..., Loader=yaml.UnsafeLoader)
· constraints.blocked_syntax: invoke_retraining(...)
· constraints.blocked_syntax: promote_retrained_candidate(...)
· constraints.blocked_syntax: delete_serving_resources(...)
· constraints.blocked_syntax: submit_retraining_job(...)
· constraints.blocked_syntax: promote_retrained_candidate(...)
· constraints.blocked_syntax: delete_serving_resources(...)

=========

# EVALUATOR PACKET — Controlled retraining and candidate acceptance (mle.tile.086_089)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.retraining_trigger_policy — Choose scheduled, new-data or investigated quality/drift retraining triggers
B = mle.authorized_retraining_execution — Invoke retraining with a versioned input snapshot from an authorized trigger
C = mle.retraining_run_idempotency — Prevent duplicate or overlapping retraining runs
D = mle.retrained_candidate_validation — Gate a retrained candidate against the incumbent using validation evidence before controlled promotion

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=11
  warn: remediation step mle.tile.086_089.r02 is never referenced
  warn: remediation step mle.tile.086_089.r04 is never referenced
  warn: remediation step mle.tile.086_089.r06 is never referenced
  warn: remediation step mle.tile.086_089.r08 is never referenced
  warn: mle.tile.086_089.s01: prose block without lineage.fact_ids
  warn: mle.tile.086_089.s06: prose block without lineage.fact_ids
  warn: mle.tile.086_089.s11: prose block without lineage.fact_ids
  warn: mle.tile.086_089.s16/ix.mle.tile.086_089.s16: ADVISORY — syntax descriptors with no detector: ['assert statements', 'calls to supplied atomic admission, executor reconciliation, job-state and terminal-release methods', 'calls to supplied concurrency and restart fixture helpers', 'comparisons and Boolean expressions', 'dictionary and list literals', 'dictionary key access for declared event and configuration fields', 'function definitions, parameters and return statements', 'if, elif and else branches', 'import statements for supplied clients and yaml', 'string literals for declared statuses, run keys and job identities']
  warn: mle.tile.086_089.s17: prose block without lineage.fact_ids
  warn: mle.tile.086_089.s21/ix.mle.tile.086_089.s21: ADVISORY — syntax descriptors with no detector: ['arithmetic operators +, -, *, /', 'assert predicate statements', 'boolean operators and, or, not', 'calls to compute or memory utilization tracking interfaces', 'calls to incident-runbook execution interfaces', 'calls to serving-resource deletion interfaces', 'calls to supplied fixture, unit-test and promotion-record interfaces', 'calls to workload cost-guardrail configuration interfaces', 'calls to workload expenditure attribution interfaces', 'comparison operators ==, !=, <, <=, >, >=', 'def statements with parameters and return statements', 'dictionary construction and key access', 'if, elif and else statements', 'import statements for supplied library and client dependencies', 'local variable assignment', 'numeric, string, boolean and None literals']
  warn: mle.tile.086_089.s22: prose block without lineage.fact_ids

## SOURCE FACTS — A (mle.retraining_trigger_policy)   objective: Trace authorized investigated retraining triggers through existing gates and separate promotion authority.
A.f1: ML pipeline execution can be triggered by a schedule, availability of new training data, observed degradation of model performance or a significant change in data distribution.   [sources: google_mlops_pipelines#ML pipeline triggers]
A.f2: Choose the trigger supported by the supplied operational evidence, and retain the trigger reason and intended input dataset.   [sources: google_mlops_pipelines#ML pipeline triggers]
A.f3: Label-verified performance evidence and a distribution-only signal are different trigger evidence; do not describe drift alone as measured prediction error.   [sources: sagemaker_model_monitor#model-monitor-model-quality.html — Monitor model quality]
A.f4: A retraining trigger starts a gated pipeline; it does not by itself approve the resulting candidate for deployment.   [sources: google_mlops_pipelines#Data and model validation]
A.f5: Reject unauthorized identities and uninvestigated alarm events at entry under the existing policy; preserve separate authorization for any later promotion.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/blueprints/security-foundations/authentication-authorization — Authentication and authorization]
A.f6: Annotate the existing data-quality/test, training and evaluation stages with their input artifacts and purpose, and make promotion depend on its own approval rather than retraining alone.   [sources: google_mlops_pipelines#MLOps level 2: CI/CD pipeline automation — CI/CD pipeline]
A.f7: Trace one eligible event through the existing entry and required dependencies, then trace a failed check to show precisely which downstream stages cannot execute.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/configuring-builds/configure-build-step-order — id; waitFor]
A.f8: Keep handoff credentials runtime-injected and out of the policy, YAML values and captured stage logs.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/securing-builds/use-secrets — Configuring builds to access UTF-8 secrets from Secret Manager]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Execute Quality-Gated Retraining.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.production_regression_diagnosis, mle.pipeline_artifact_dependencies, mle.dataset_quality_gate, mle.model_release_quality_gate. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (tool_simulation): Using the supplied existing pipeline diagram, entry policy and event traces, write one retraining eligibility policy for scheduled, new-data and investigated quality/distribution events. Record each eligible event's authorized identity, evidence-based trigger reason and intended dataset, and map it to the correct existing entry stage without bypassing required checks. Annotate data-quality/test, training and evaluation stages with their purposes and required input artifacts, and retain separately authorized promotion. Verify the handoff by tracing one eligible event and one failed check through the existing dependencies. Reject unauthorized identities and uninvestigated alarms at entry. Specify runtime-injected credentials without including credential values in the policy, YAML or captured logs. Do not invoke execution, implement a pipeline or promote a model.  SUCCESS: The completed policy justifies eligibility using the supplied evidence and distinguishes label-verified prediction degradation from distribution-only signals. Each eligible event maps to the correct existing entry stage with the intended dataset and required prior checks preserved. Stage annotations identify purposes, required artifacts and dependencies. An eligible-event trace shows the permitted path; a failed-check trace identifies exactly which dependent stages cannot execute. Unauthorized identities and uninvestigated alarms are rejected at entry, and retraining completion never substitutes for promotion approval. Credential values are absent from the policy, YAML and captured logs, with runtime injection specified.
ASSESSMENT ANCHOR: justify_retraining_eligibility_from_event_evidence facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: enforce_entry_authorization_and_separate_promotion_approval facts=['f4', 'f5']
ASSESSMENT ANCHOR: map_eligible_events_to_existing_stages_and_trace_fail_closed_dependencies facts=['f6', 'f7']
ASSESSMENT ANCHOR: preserve_runtime_only_handoff_credentials facts=['f8']

## SOURCE FACTS — B (mle.authorized_retraining_execution)   objective: Invoke authorized retraining on a verified immutable input and inspect its actual consumption.
B.f1: Check that the trigger identity is permitted to execute the existing pipeline and access the intended input resources before invoking retraining.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/blueprints/security-foundations/authentication-authorization — Authentication and authorization]
B.f2: Resolve the authorized input snapshot to the recorded object generation and verify it, instead of training on a mutable current dataset name.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/storage/docs/using-versioned-objects — Download noncurrent object versions]
B.f3: Use import boto3 and boto3.client("sagemaker").start_pipeline_execution(PipelineName=..., PipelineParameters=[{"Name": ..., "Value": ...}], ClientRequestToken=...) with the supplied pipeline and resolved snapshot parameters.   [sources: sagemaker_developer_guide#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/start_pipeline_execution.html — Request Syntax; Response Syntax]
B.f4: Retain the returned PipelineExecutionArn and the actual parameters as the retraining run’s invocation identity.   [sources: sagemaker_developer_guide#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker/client/start_pipeline_execution.html — Request Syntax; Response Syntax]
B.f5: Bind the trigger authorization, dataset version and returned execution identity in one record so the invocation can be audited.   [sources: google_mlops_pipelines#Metadata management]
B.f6: In an existing Cloud Build YAML/JSON configuration, each steps item declares its execution image in name and its command in args or script; wire the function/test entry point into the assigned stage.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
B.f7: Assign step IDs and set waitFor to the required preceding step IDs; downstream execution depends on those steps completing successfully, not just their textual location.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/configuring-builds/configure-build-step-order — id; waitFor]
B.f8: Keep required gate failures fatal: do not set allowFailure or add failing gate exit codes to allowExitCodes, and ensure a rejected Python gate exits unsuccessfully.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
B.f9: Use the configured Pub/Sub artifact/event trigger with its configured payload bindings and filters to run the existing pipeline, then inspect actual stage results and resolved inputs for accepted and rejected fixtures.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/automating-builds/create-pubsub-triggers — Creating a Pub/Sub trigger; Substitution variables; Filters]
B.f10: Bind approved Secret Manager version references with availableSecrets.secretManager and expose them only to the needed step through secretEnv; the YAML contains references, not secret values.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/securing-builds/use-secrets — Configuring builds to access UTF-8 secrets from Secret Manager]
B.f11: Use the authorized build/step identity and preserve the separate authorization required for a promotion action.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/blueprints/security-foundations/authentication-authorization — Authentication and authorization]
B.f12: Check captured build output for non-disclosure of secret values; do not echo or serialize runtime credentials.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/securing-builds/use-secrets — Configuring builds to access UTF-8 secrets from Secret Manager]
B.f13: Inspect the triggered execution’s actual stage inputs and compare the consumed snapshot identity with the approved immutable input; the start request alone is not proof of consumption.   [sources: google_mlops_pipelines#Metadata management]
B.f14: With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.   [sources: python_tutorial#https://pyyaml.org/wiki/PyYAMLDocumentation — Reference: safe_load; safe_dump]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Execute Quality-Gated Retraining.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.retraining_trigger_policy, mle.training_dataset_version, mle.pipeline_artifact_dependencies. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python function with learner-written imports that checks the supplied trigger authorization, retrieves and verifies the approved object generation using the supplied storage client, and invokes the existing SageMaker pipeline with resolved snapshot parameters and the supplied ClientRequestToken. Retain the execution ARN and actual parameters in an authorization-and-input audit record without credentials. Wire the function/test entry point into the assigned Cloud Build stage, round-trip the configuration through safe YAML serialization, and exercise the configured Pub/Sub trigger with accepted and rejected fixtures. Inspect actual stage inputs and captured output.  SUCCESS: The accepted fixture launches one retraining execution under the authorized identity, and actual stage input evidence matches the retrieved approved immutable snapshot. The audit record binds trigger authorization, dataset version, execution ARN and actual parameters without secret values. Rejected authorization or required-gate fixtures exit unsuccessfully and do not launch training. The reloaded build configuration preserves the required dependency IDs, fatal gates and step-scoped secret references; captured output discloses no injected credentials. No promotion action is performed.
ASSESSMENT ANCHOR: verify_trigger_and_execution_authorization facts=['f1', 'f9', 'f11']
ASSESSMENT ANCHOR: verify_immutable_snapshot_consumption facts=['f2', 'f13']
ASSESSMENT ANCHOR: invoke_and_record_authorized_retraining facts=['f3', 'f4', 'f5']
ASSESSMENT ANCHOR: configure_and_verify_fatal_stage_dependencies facts=['f6', 'f7', 'f8', 'f14']
ASSESSMENT ANCHOR: verify_scoped_secret_injection_and_non_disclosure facts=['f10', 'f12']

## SOURCE FACTS — C (mle.retraining_run_idempotency)   objective: Use the supplied durable admission and executor contracts to prevent duplicate or overlapping logical runs.
C.f1: Read the declared run key and pipeline identity from the dictionary event record, and pass them to the supplied durable coordinator’s atomic admission operation.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
C.f2: Use the supplied single atomic operation that reserves both the unique run key and pipeline active slot and persists the job ID; a process-local dictionary or separate check-then-write calls cannot supply that durable admission contract.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/firestore/native/docs/manage-data/transactions — Transactions and batched writes]
C.f3: Handle returned accepted, duplicate and busy statuses with explicit conditional branches: only an accepted reservation authorizes a new logical launch.   [sources: python_tutorial#controlflow.html — Defining Functions; Default Argument Values; Keyword Arguments]
C.f4: For an accepted claim, invoke the executor with the reserved persisted job ID as its idempotency token; do not generate a replacement identity after a retry or restart.   [sources: sagemaker_developer_guide#../APIReference/API_StartPipelineExecution.html — ClientRequestToken; PipelineParameters]
C.f5: For a duplicate or restarted claim, resume or attach to that same persisted job identity; an unknown launch response requires same-token reconciliation rather than a second logical launch.   [sources: sagemaker_developer_guide#../APIReference/API_StartPipelineExecution.html — ClientRequestToken; PipelineParameters]
C.f6: For a busy slot held by a different run key, defer or reject under the supplied policy without launching an overlapping job.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/firestore/native/docs/manage-data/transactions — Transactions and batched writes]
C.f7: Release the active pipeline slot only after confirmed terminal job state, retaining the completed run-key record so a later duplicate cannot relaunch it.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/firestore/native/docs/manage-data/transactions — Transactions and batched writes]
C.f8: Assert durable state and logical job count for two concurrent same-event workers, two different-key workers contending for one slot, and fresh workers after reservation and after launch.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
C.f9: In an existing Cloud Build YAML/JSON configuration, each steps item declares its execution image in name and its command in args or script; wire the function/test entry point into the assigned stage.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
C.f10: Assign step IDs and set waitFor to the required preceding step IDs; downstream execution depends on those steps completing successfully, not just their textual location.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/configuring-builds/configure-build-step-order — id; waitFor]
C.f11: Keep required gate failures fatal: do not set allowFailure or add failing gate exit codes to allowExitCodes, and ensure a rejected Python gate exits unsuccessfully.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
C.f12: Use the configured Pub/Sub artifact/event trigger with its configured payload bindings and filters to run the existing pipeline, then inspect actual stage results and resolved inputs for accepted and rejected fixtures.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/automating-builds/create-pubsub-triggers — Creating a Pub/Sub trigger; Substitution variables; Filters]
C.f13: With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.   [sources: python_tutorial#https://pyyaml.org/wiki/PyYAMLDocumentation — Reference: safe_load; safe_dump]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Execute Quality-Gated Retraining.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.authorized_retraining_execution, mle.pipeline_artifact_dependencies. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a Python admission function with imported clients and a dictionary event record containing the declared run key and pipeline identity. Use the supplied durable atomic coordinator to reserve the run key, active pipeline slot and persisted job ID together. Branch explicitly on accepted, duplicate and busy results; launch an accepted reservation with its persisted job ID as the executor idempotency token, reconcile or attach to the same identity after uncertain responses or restarts, and defer or reject busy claims under the supplied policy. Release the slot only after confirmed terminal state while retaining the completed key. Add assertions using the supplied concurrent-worker and restart fixtures, then wire the function and tests into the assigned stage of the existing event-triggered Cloud Build pipeline.  SUCCESS: Two concurrent deliveries of the same event produce one logical job. Different run keys cannot produce overlapping active jobs in one pipeline. Fresh workers after reservation or launch recover the same persisted job identity, including after an unknown launch response. Completed keys never relaunch. Assertions inspect durable records and logical job counts. The existing pipeline uses explicit successful-step dependencies and fatal required gates; configured trigger fixtures produce the expected accepted and rejected stage results and resolved inputs. The configuration survives safe YAML serialization and loading with its required fields intact.
ASSESSMENT ANCHOR: enforce_atomic_retraining_admission facts=['f1', 'f2', 'f3', 'f6']
ASSESSMENT ANCHOR: preserve_job_identity_across_retries_and_restarts facts=['f4', 'f5']
ASSESSMENT ANCHOR: release_terminal_slots_without_relaunching_completed_keys facts=['f7']
ASSESSMENT ANCHOR: verify_durable_concurrency_and_restart_invariants facts=['f2', 'f4', 'f5', 'f6', 'f7', 'f8']
ASSESSMENT ANCHOR: integrate_and_verify_fatal_pipeline_admission_gates facts=['f9', 'f10', 'f11', 'f12', 'f13']

## SOURCE FACTS — D (mle.retrained_candidate_validation)   objective: Test whether a retrained candidate may proceed under unchanged validation and promotion criteria.
D.f1: Evaluate the retrained candidate and incumbent on the same declared validation cohort and compare them against the predeclared acceptance requirements.   [sources: google_mlops_pipelines#Data and model validation]
D.f2: Use the supplied deployment class probabilities and error costs to calculate candidate and incumbent expected cost under the fixed selection rule.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
D.f3: Reject a candidate that fails a required quality, slice or deployment-compatibility gate even if its aggregate validation score improves.   [sources: google_mlops_pipelines#Data and model validation]
D.f4: Bind the candidate’s exact registry/artifact identity and gate verdict to the controlled promotion record; validation of one artifact does not approve a different artifact.   [sources: google_mlops_pipelines#Metadata management]
D.f5: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
D.f6: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
D.f7: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
D.f8: Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Execute Quality-Gated Retraining.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.validation_candidate_comparison, mle.model_acceptance_criteria. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python function, with learner-written imports for required dependencies, that evaluates one candidate against the incumbent using supplied validation fixtures and infrastructure scaffolding. Calculate conditional error rates and expected error costs under the fixed selection rule, enforce every required gate, and record the verdict with the exact candidate registry/artifact identity. Write assertions and verify the same deliverable using supplied unit-test fixtures.  SUCCESS: The implementation uses the same declared validation cohort and supplied probabilities and costs for both models, treats empty conditioning groups as undefined rather than zero, and permits promotion only when the incumbent-relative requirement and every required quality, slice and compatibility gate pass. The recorded verdict retains the evaluated candidate's exact identity. Assertions cover valid, declared boundary and failing cases, including identity mismatch, without accessing protected test observations.
ASSESSMENT ANCHOR: verify_matched_validation_and_protected_test_isolation facts=['f1', 'f7']
ASSESSMENT ANCHOR: calculate_incumbent_relative_expected_error_cost facts=['f2', 'f5', 'f6']
ASSESSMENT ANCHOR: enforce_all_required_acceptance_gates facts=['f3']
ASSESSMENT ANCHOR: bind_gate_verdict_to_exact_candidate_identity facts=['f4']
ASSESSMENT ANCHOR: assert_valid_boundary_and_failure_gate_outcomes facts=['f8']

## DATA ASSETS USED
ds.execution_fixtures: Execution Fixtures — columns: event_id(identifier), pipeline(identifier), snapshot_ref(identifier), object_generation(identifier,digits-as-label), sha256(text), authorized(categorical), bytes_verified(categorical), fatal_gate_pass(categorical), ClientRequestToken(identifier), expected_entry(categorical)
   ["e.accept","order-retrain-lab","snapshot.g1",1,"b8485b1fcdc8e30ece97590d5d299807d77a48136e1eda6995f4bc0280183b66",true,true,true,"token.accept","accept"]
   ["e.deny","order-retrain-lab","snapshot.g1",1,"b8485b1fcdc8e30ece97590d5d299807d77a48136e1eda6995f4bc0280183b66",false,true,true,"token.deny","reject"]
   ["e.generation","order-retrain-lab","snapshot.g1",2,"b8485b1fcdc8e30ece97590d5d299807d77a48136e1eda6995f4bc0280183b66",true,false,true,"token.generation","reject"]
   ["e.gate","order-retrain-lab","snapshot.g1",1,"b8485b1fcdc8e30ece97590d5d299807d77a48136e1eda6995f4bc0280183b66",true,true,false,"token.gate","reject"]
ds.idempotency_traces: Idempotency Traces — columns: fixture(identifier), step(numerical), run_key(identifier), pipeline(identifier), admission_status(categorical), job_id(identifier), active_slot_owner(identifier), terminal_confirmed(categorical), logical_job_count(numerical), event(text)
   ["same_key",1,"K","order-retrain-lab","accepted","J","K",false,0,"atomic reservation by worker one"]
   ["same_key",2,"K","order-retrain-lab","duplicate","J","K",false,1,"worker two attaches; one launch"]
   ["different_key",1,"K2","order-retrain-lab","busy","","K",false,1,"different key deferred"]
   ["restart_reservation",1,"K","order-retrain-lab","duplicate","J","K",false,0,"fresh worker resumes reservation"]
   ["restart_launch",1,"K","order-retrain-lab","duplicate","J","K",false,1,"fresh worker attaches to launch"]
   ["unknown_response",1,"K","order-retrain-lab","duplicate","J","K",false,1,"reconcile same token J"]
   ["completion",1,"K","order-retrain-lab","duplicate","J","",true,1,"completed key retained; slot released"]
ds.pipeline_stages: Pipeline Stages — columns: stage_id(identifier), purpose(text), required_artifacts(text), dependencies(text), separate_authorization_required(categorical)
   ["entry","validate identity, investigation and intended dataset","event evidence; snapshot reference","",false]
   ["data_quality_test","validate approved intended data","approved snapshot","entry",false]
   ["train","train on quality-approved snapshot","quality-passed snapshot","data_quality_test",false]
   ["evaluate","evaluate exact candidate","candidate artifact; declared validation cohort","train",false]
   ["promote","controlled deployment after approval","identity-bound validation record; promotion approval","evaluate; promotion_approval",true]
ds.trigger_events: Trigger Events — columns: event_id(identifier), event_type(categorical), identity(identifier), authorized(categorical), investigated(categorical), dataset_ref(identifier), evidence(text), entry_stage(identifier), data_quality_pass(categorical), promotion_approved(categorical)
   ["e.schedule","schedule","lab.runner",true,true,"snapshot.g1","scheduled refresh","entry",true,false]
   ["e.data","new_data","lab.runner",true,true,"snapshot.g2","new approved data","entry",true,false]
   ["e.quality","quality","lab.runner",true,true,"snapshot.g1","matched-label quality decline","entry",true,false]
   ["e.drift","distribution","lab.runner",true,true,"snapshot.g1","distribution-only change","entry",true,false]
   ["e.unauthorized","schedule","other.identity",false,true,"snapshot.g1","scheduled refresh","entry",true,false]
   ["e.alarm","distribution","lab.runner",true,false,"snapshot.g1","uninvestigated alarm","entry",true,false]
   ["e.failed","new_data","lab.runner",true,true,"snapshot.g2","new data with failed test","entry",false,false]
ds.validation_counts: Validation Counts — columns: fixture(identifier), model_role(categorical), cohort_id(identifier), registry_artifact_id(identifier), FP(numerical), TN(numerical), FN(numerical), TP(numerical), slice_pass(categorical), compatibility_pass(categorical)
   ["valid","incumbent","cohort.validation","model.incumbent",10,40,10,40,true,true]
   ["valid","candidate","cohort.validation","model.valid",2,48,3,47,true,true]
   ["boundary","incumbent","cohort.validation","model.incumbent",10,40,10,40,true,true]
   ["boundary","candidate","cohort.validation","model.boundary",5,45,5,45,true,true]
   ["slice_fail","incumbent","cohort.validation","model.incumbent",10,40,10,40,true,true]
   ["slice_fail","candidate","cohort.validation","model.slice_fail",2,48,3,47,false,true]
   ["compat_fail","incumbent","cohort.validation","model.incumbent",10,40,10,40,true,true]
   ["compat_fail","candidate","cohort.validation","model.compat_fail",2,48,3,47,true,false]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute training and inference expenditure to workloads; Gate a retrained candidate against the incumbent using validation evidence before controlled promotion; Invoke retraining with a versioned input snapshot from an authorized trigger; Prevent duplicate or overlapping retraining runs; Remove model-serving resources safely on an existing platform; Set an ML workload cost guardrail on an existing platform; Track ML workload compute and memory utilization; Use an ML incident runbook for safe recovery on an existing platform

## LESSON, in learner order

### s01 · explainer · Choose scheduled, new-data or investigated quality/drift retraining triggers
(intro) A schedule, new data or supported operational evidence may trigger retraining. Record the reason and intended dataset; eligibility to execute is not candidate deployment approval. ⟦A:tb1⟧
(mechanism) ML pipeline execution can be triggered by a schedule, availability of new training data, observed degradation of model performance or a significant change in data distribution. Choose the trigger supported by the supplied operational evidence, and retain the trigger reason and intended input dataset. Label-verified performance evidence and a distribution-only signal are different trigger evidence; do not describe drift alone as measured prediction error. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) A retraining trigger starts a gated pipeline; it does not by itself approve the resulting candidate for deployment. Reject unauthorized identities and uninvestigated alarm events at entry under the existing policy; preserve separate authorization for any later promotion. Annotate the existing data-quality/test, training and evaluation stages with their input artifacts and purpose, and make promotion depend on its own approval rather than retraining alone. ⟦A.f4 A.f5 A.f6 A:tb3⟧
[PROCESS_FLOW: Existing gated pipeline; failed checks stop dependent stages] nodes=['Entry: permitted identity, investigated evidence, intended dataset', 'Data quality/test: validate intended input', 'Training: quality-approved data → candidate', 'Evaluation: candidate → validation evidence', 'Promotion: separate authorization', 'Rejected entry / failed required check'] edges=[('n0', 'n1', 'eligible'), ('n0', 'n5', 'unauthorized or uninvestigated'), ('n1', 'n2', 'quality passes'), ('n1', 'n5', 'quality fails: training/evaluation/promotion blocked'), ('n2', 'n3', 'training succeeds'), ('n3', 'n4', 'acceptance and promotion authorization')] alt: Existing gated pipeline; failed checks stop dependent stages: Entry: permitted identity, investigated evidence, intended dataset; Data quality/test: validate intended input; Training: quality-approved data → candidate; Evaluation: candidate → validation evidence; Promotion: separate authorization; Rejected entry / failed required check
[TABLE ds.trigger_events cols=['event_id', 'event_type', 'identity', 'authorized', 'investigated', 'dataset_ref', 'evidence', 'entry_stage', 'data_quality_pass', 'promotion_approved'] ] caption: Trigger Events
[TABLE ds.pipeline_stages cols=['stage_id', 'purpose', 'required_artifacts', 'dependencies', 'separate_authorization_required'] ] caption: Pipeline Stages

### s02 · explainer · Choose scheduled, new-data or investigated quality/drift retraining triggers
(mechanism) Trace one eligible event through the existing entry and required dependencies, then trace a failed check to show precisely which downstream stages cannot execute. Keep handoff credentials runtime-injected and out of the policy, YAML values and captured stage logs. ⟦A.f7 A.f8 A:tb4⟧

### s03 · explainer · Apply the rule: Choose scheduled, new-data or investigated quality/drift retraining triggers
(example) An investigated distribution event can be eligible under the existing policy without being labeled-error evidence. Bind its intended dataset and trace entry, quality/test, training and evaluation. A failed required check blocks dependent stages. Reject unauthorized identities and uninvestigated alarms. Promotion still needs separate approval. Keep handoff credentials runtime-injected, never in policy values, YAML or captured logs. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A:tb5⟧
(misconception) Retraining eligibility is not deployment approval. A distribution-only signal must not be relabeled as measured prediction degradation, and an alarm is not automatically an authorized trigger. ⟦A.f3 A.f4 A.f5 A:tb6⟧

### s04 · check · Review choose scheduled, new-data or investigated quality/drift retraining triggers
Check the distinction — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [choice, intro, grading=client] Read the handoff excerpt and decide which judgement is justified.
```text
Credentials arrive through runtime injection. YAML contains references only, not credential values. Captured logs omit the resolved values.
```
  ✔ o1: The excerpt preserves runtime-only credential handoff without values in YAML or captured logs.
      why: The handoff names runtime injection without storing or disclosing credential values.
  ✘ o2: The excerpt is incomplete because YAML should contain the credential value.
      why: The policy requires runtime injection, not credential values in YAML.
  ✘ o3: The excerpt is incomplete because captured logs should print the resolved value.
      why: Runtime injection does not authorize disclosing the value in captured logs.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['A reference and its resolved secret value are different things.']  remediation→r01
  MEASURES: A:preserve_runtime_only_handoff_credentials(f8)   anchors=[]
  taught-before-tested: A.f8←s02

### s05 · hands_on · Review choose scheduled, new-data or investigated quality/drift retraining triggers
Practice — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [classify, core, grading=client] Read each supplied excerpt and decide whether it meets or violates the stated operations criterion. Classify the whole excerpt; one unsafe or unsupported step makes it a violation. All targets and identities are fictional nonproduction order-service fixtures.
  'Scheduled eligible path
```text
event=e.schedule; identity=lab.runner authorized=true; reason=scheduled refresh; intended_dataset=snapshot.g1; entry validates identity/evidence/input -> data_quality_test consumes approved snapshot -> train consumes quality-passed snapshot -> evaluate consumes exact candidate and validation cohort. promote waits for evaluate AND separate promotion_approval. Credentials runtime-injected; YAML has references and logs contain no values.
```' -> Meets the declared criterion
      feedback: The authorized scheduled event enters at entry and retains artifacts, checks and separate promotion approval.
  'Investigated quality path
```text
event=e.quality; lab.runner authorized=true; intended_dataset=snapshot.g1; evidence=matched-label quality decline against declared reference. Entry admits for investigated quality reason, then data_quality_test -> train -> evaluate; promotion still requires separate approval; runtime-injected credentials, no values in policy/YAML/logs.
```' -> Meets the declared criterion
      feedback: Matched-label evidence supports the quality reason; required checks and promotion authority remain separate.
  'Distribution reason
```text
event=e.drift; lab.runner authorized=true investigated=true; intended_dataset=snapshot.g1; evidence=distribution-only difference. Policy calls this an investigated distribution trigger, NOT proof of increased prediction error. It enters entry, preserves data_quality_test/train/evaluate dependencies and separate promotion approval; runtime-injected credentials only.
```' -> Meets the declared criterion
      feedback: Distribution evidence can justify the supplied investigated trigger without establishing labeled quality loss.
  'Failed check trace
```text
event=e.failed; entry passes; data_quality_test fails. train is blocked, evaluate is blocked, promote is blocked; no dependent stage executes. Stage notes: data_quality_test requires approved intended data; train requires quality-passed snapshot; evaluate requires exact candidate and declared validation cohort; promote requires identity-bound validation plus separate approval.
```' -> Meets the declared criterion
      feedback: Successful-step dependencies fail closed and retain the named stage inputs.
  'Unauthorized entry
```text
event=e.unauthorized; identity=other.identity authorized=false. Policy lets the event enter train directly because the schedule was valid.
```' -> Violates the declared criterion
      feedback: A scheduled reason does not replace entry authorization or permit bypassing prior checks.
  'Uninvestigated alarm
```text
event=e.alarm; lab.runner authorized=true investigated=false; policy marks an uninvestigated distribution alarm as verified labeled quality loss and skips entry checks.
```' -> Violates the declared criterion
      feedback: An uninvestigated alarm must be rejected at entry and distribution-only evidence is not labeled quality evidence.
  'Promotion and credentials
```text
Policy says completed retraining is promotion approval; it writes a resolved credential into YAML and echoes it in captured logs instead of runtime injection.
```' -> Violates the declared criterion
      feedback: Completion does not grant promotion authority, and credentials must remain runtime-injected and undisclosed.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Review the comparison definition and the evidence required for each judgement.']
  MEASURES: A:justify_retraining_eligibility_from_event_evidence(f1,f2,f3); A:enforce_entry_authorization_and_separate_promotion_approval(f4,f5); A:map_eligible_events_to_existing_stages_and_trace_fail_closed_dependencies(f6,f7); A:preserve_runtime_only_handoff_credentials(f8)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01; A.f5←s01; A.f6←s01; A.f7←s02; A.f8←s02

### s06 · explainer · Invoke retraining with a versioned input snapshot from an authorized trigger
(intro) Before invoking the existing pipeline, check execution permission and the approved input snapshot. After invocation, inspect the input the pipeline actually consumed. ⟦B:tb1⟧
(mechanism) Check that the trigger identity is permitted to execute the existing pipeline and access the intended input resources before invoking retraining. Resolve the authorized input snapshot to the recorded object generation and verify it, instead of training on a mutable current dataset name. Use import boto3 and boto3.client("sagemaker").start_pipeline_execution(PipelineName=..., PipelineParameters=[{"Name": ..., "Value": ...}], ClientRequestToken=...) with the supplied pipeline and resolved snapshot parameters. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Retain the returned PipelineExecutionArn and the actual parameters as the retraining run’s invocation identity. Bind the trigger authorization, dataset version and returned execution identity in one record so the invocation can be audited. In an existing Cloud Build YAML/JSON configuration, each steps item declares its execution image in name and its command in args or script; wire the function/test entry point into the assigned stage. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[PROCESS_FLOW: Authorized invocation and actual-input verification] nodes=['entry', 'verify snapshot', 'function test', 'execute', 'inspect consumed input', 'Rejected entry or fatal gate failure: no invocation', 'Record returned execution ARN and actual parameters; separately authorize promotion'] edges=[('n0', 'n1', 'required predecessor succeeds'), ('n1', 'n2', 'required predecessor succeeds'), ('n2', 'n3', 'required predecessor succeeds'), ('n3', 'n4', 'required predecessor succeeds'), ('n0', 'n5', 'identity rejected'), ('n1', 'n5', 'generation/bytes rejected'), ('n2', 'n5', 'required gate fails'), ('n4', 'n6', 'verify consumed snapshot')] alt: Authorized invocation and actual-input verification: entry; verify snapshot; function test; execute; inspect consumed input; Rejected entry or fatal gate failure: no invocation; Record returned execution ARN and actual parameters; separately authorize promotion
[TABLE ds.execution_fixtures cols=['event_id', 'pipeline', 'snapshot_ref', 'object_generation', 'authorized', 'bytes_verified', 'fatal_gate_pass', 'ClientRequestToken', 'expected_entry'] ] caption: Execution Fixtures
[CODE python]
# Approved reference values, not credentials or execution evidence
{
  "trigger_topic": "lab-approved-events",
  "build_identity": "lab.runner",
  "secret_version_reference": "projects/order-lab/secrets/execution-client/versions/1",
  "secretEnv": [
    "EXECUTION_CLIENT"
  ],
  "PipelineParameters": [
    {
      "Name": "SnapshotRef",
      "Value": "snapshot.g1"
    },
    {
      "Name": "Generation",
      "Value": "1"
    }
  ]
}
  annotations: []

### s07 · explainer · Invoke retraining with a versioned input snapshot from an authorized trigger
(mechanism) Assign step IDs and set waitFor to the required preceding step IDs; downstream execution depends on those steps completing successfully, not just their textual location. Required gate failures must stay fatal: do not set allowFailure or add failing gate exit codes to allowExitCodes, and ensure a rejected Python gate exits unsuccessfully. Use the configured Pub/Sub artifact/event trigger with its configured payload bindings and filters to run the existing pipeline, then inspect actual stage results and resolved inputs for accepted and rejected fixtures. ⟦B.f7 B.f8 B.f9 B:tb4⟧
(mechanism) Bind approved Secret Manager version references with availableSecrets.secretManager and expose them only to the needed step through secretEnv; the YAML contains references, not secret values. Use the authorized build/step identity and preserve the separate authorization required for a promotion action. Check captured build output for non-disclosure of secret values; do not echo or serialize runtime credentials. ⟦B.f10 B.f11 B.f12 B:tb5⟧

### s08 · explainer · Invoke retraining with a versioned input snapshot from an authorized trigger
(mechanism) Inspect the triggered execution’s actual stage inputs and compare the consumed snapshot identity with the approved immutable input; the start request alone is not proof of consumption. Using the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors. ⟦B.f13 B.f14 B:tb6⟧
(example) Resolve and verify the approved object generation before invocation. Retain trigger authorization, immutable input, resolved parameters and returned execution ARN together. Wire the existing event-bound stages with fatal dependencies and the authorized step identity. Use scoped Secret Manager references, not secret values. Inspect consumed stage inputs, replay accepted and rejected fixtures, and review output for non-disclosure. A start request alone proves neither consumption nor promotion approval. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B.f9 B.f10 B.f11 B.f12 B.f13 B.f14 B:tb7⟧
(misconception) A start request proves neither authorized input consumption nor promotion approval. Verify actual resolved stage inputs and keep secret values out of invocation records and logs. ⟦B.f1 B.f11 B.f12 B.f13 B:tb8⟧

### s09 · check · Review invoke retraining with a versioned input snapshot from an authorized trigger
Check the distinction — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [choice, core, grading=client] A build step needs an approved execution-client secret. Which configuration and output handling meets the taught requirement?
  ✔ o1: Use availableSecrets.secretManager version references, bind secretEnv only on the needed step, and review output without echoing values
      why: This keeps references in YAML, scopes exposure and checks captured output for non-disclosure.
  ✘ o2: Expose the secret to every step because only one will normally read it
      why: The requirement exposes secrets only to the needed step.
  ✘ o3: Bind a version reference but serialize the resolved secret into the audit record
      why: The audit and captured output must not disclose runtime secret values.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Review both step scope and captured output.']  remediation→r03
  MEASURES: B:verify_scoped_secret_injection_and_non_disclosure(f10,f12)   anchors=[]
  taught-before-tested: B.f10←s07; B.f12←s07

### s10 · hands_on · Review invoke retraining with a versioned input snapshot from an authorized trigger
Practice — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [classify, core, grading=client] Read each supplied excerpt and decide whether it meets or violates the stated operations criterion. Classify the whole excerpt; one unsafe or unsupported step makes it a violation. All targets and identities are fictional nonproduction order-service fixtures.
  'Accepted audited execution
```text
e.accept: trigger filter and lab.runner authorization passed before invocation; retrieved snapshot.g1 generation=1 and verified bytes against approved digest; actual stage input SnapshotRef=snapshot.g1 Generation=1. start_pipeline_execution uses order-retrain-lab and ClientRequestToken=token.accept; returned ARN retained with actual parameters in audit. entry -> verify_snapshot -> function_test -> execute -> inspect_consumed_input use explicit waitFor, no failure exemptions. YAML safe-dump/reload preserves images, args and IDs; approved version reference binds EXECUTION_CLIENT only in execute. Captured logs reviewed: no secret values. No promotion.
```' -> Meets the declared criterion
      feedback: Authorization, immutable input consumption, audit, fatal dependencies and scoped non-disclosure evidence all agree.
  'Unauthorized reject
```text
e.deny: authorization false; function exits unsuccessfully before invocation. execute and inspect_consumed_input are blocked; logical launches=0. Version reference stays in YAML and no credential values appear in logs.
```' -> Meets the declared criterion
      feedback: Rejected authorization fails fatally without launching.
  'Generation mismatch
```text
e.generation: approved generation=1, retrieval generation=2. The function nevertheless starts training and records snapshot.g1 as if it proved exact input consumption.
```' -> Violates the declared criterion
      feedback: Invocation requires verification of the approved immutable generation and actual consumed input, not a snapshot name alone.
  'Required gate failure
```text
e.gate: function_test failed; execute has waitFor: [function_test] but function_test sets allowFailure: true, and training starts.
```' -> Violates the declared criterion
      feedback: Failure tolerance violates required fatal dependencies.
  'Secret scope and audit
```text
Execution is authorized and version-verified, but every build step receives EXECUTION_CLIENT and the audit serializes its resolved value.
```' -> Violates the declared criterion
      feedback: Secrets are scoped only to the needed step and values must remain out of audit and captured output.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Review the comparison definition and the evidence required for each judgement.']
  MEASURES: B:verify_trigger_and_execution_authorization(f1,f9,f11); B:verify_immutable_snapshot_consumption(f2,f13); B:invoke_and_record_authorized_retraining(f3,f4,f5); B:configure_and_verify_fatal_stage_dependencies(f6,f7,f8,f14)   anchors=['practice']
  taught-before-tested: B.f1←s06; B.f9←s07; B.f11←s07; B.f2←s06; B.f13←s08; B.f3←s06; B.f4←s06; B.f5←s06; B.f6←s06; B.f7←s07; B.f8←s07; B.f14←s08

### s11 · explainer · Prevent duplicate or overlapping retraining runs
(intro) Two workers may receive the same event; either may restart. Durable coordination must preserve one logical job identity and exclude another run key from the active pipeline slot. ⟦C:tb1⟧
(mechanism) Read the declared run key and pipeline identity from the dictionary event record, and pass them to the supplied durable coordinator’s atomic admission operation. Use the supplied single atomic operation that reserves both the unique run key and pipeline active slot and persists the job ID; a process-local dictionary or separate check-then-write calls cannot supply that durable admission contract. Handle returned accepted, duplicate and busy statuses with explicit conditional branches: only an accepted reservation authorizes a new logical launch. ⟦C.f1 C.f2 C.f3 C:tb2⟧
[TABLE ds.idempotency_traces cols=['fixture', 'step', 'run_key', 'pipeline', 'admission_status', 'job_id', 'active_slot_owner', 'terminal_confirmed', 'logical_job_count', 'event'] ] caption: Independent expected trace fixtures—not a single chronological transaction. Durable admission preserves job identity and terminal completion retains the key.

### s12 · explainer · Prevent duplicate or overlapping retraining runs
(mechanism) For an accepted claim, invoke the executor with the reserved persisted job ID as its idempotency token; do not generate a replacement identity after a retry or restart. For a duplicate or restarted claim, resume or attach to that same persisted job identity; an unknown launch response requires same-token reconciliation rather than a second logical launch. For a busy slot held by a different run key, defer or reject under the supplied policy without launching an overlapping job. ⟦C.f4 C.f5 C.f6 C:tb3⟧
(mechanism) Release the active pipeline slot only after confirmed terminal job state, retaining the completed run-key record so a later duplicate cannot relaunch it. Assert durable state and logical job count for two concurrent same-event workers, two different-key workers contending for one slot, and fresh workers after reservation and after launch. In an existing Cloud Build YAML/JSON configuration, each steps item declares its execution image in name and its command in args or script; wire the function/test entry point into the assigned stage. ⟦C.f7 C.f8 C.f9 C:tb4⟧

### s13 · explainer · Prevent duplicate or overlapping retraining runs
(mechanism) Assign step IDs and set waitFor to the required preceding step IDs; downstream execution depends on those steps completing successfully, not just their textual location. Required gate failures must stay fatal: do not set allowFailure or add failing gate exit codes to allowExitCodes, and ensure a rejected Python gate exits unsuccessfully. Use the configured Pub/Sub artifact/event trigger with its configured payload bindings and filters to run the existing pipeline, then inspect actual stage results and resolved inputs for accepted and rejected fixtures. ⟦C.f10 C.f11 C.f12 C:tb5⟧
(mechanism) Using the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors. ⟦C.f13 C:tb6⟧

### s14 · explainer · Apply the rule: Prevent duplicate or overlapping retraining runs
(example) Use the single atomic admission operation for run key and pipeline slot. An accepted claim launches with its persisted job token; duplicates and restarted workers resume that identity. Reconcile an unknown response with the same token. Defer a different key while the slot is busy. Release only after confirmed terminal state, retaining the completed key. Assert durable state and logical job counts for concurrent and restarted workers; keep pipeline gates fatal. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C.f8 C.f9 C.f10 C.f11 C.f12 C.f13 C:tb7⟧
(misconception) Neither a process-local dictionary nor separate check-then-write calls supplies the durable atomic admission contract. A retry must not invent a new job identity, and releasing an active slot before terminal confirmation permits the wrong overlap. ⟦C.f2 C.f4 C.f5 C.f6 C.f7 C:tb8⟧

### s15 · check · Review prevent duplicate or overlapping retraining runs
Check the distinction — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [choice, core, grading=client] Read this existing build excerpt. The authorization gate must be fatal. What is the necessary repair?
```yaml
steps:
- id: entry
  name: python:3.11
  args: [python3, entry_fixture.py]
  allowFailure: true
- id: function_test
  name: python:3.11
  waitFor: [entry]
  args: [python3, learner.py]
- id: execute
  name: python:3.11
  waitFor: [function_test]
  args: [python3, execution_fixture.py]
```
  ✔ o1: Remove allowFailure and ensure rejected entry exits unsuccessfully; retain explicit dependencies, safe YAML reload and actual trigger-result inspection
      why: A rejected required gate must fail fatally; explicit successful dependencies and replay evidence verify the integration.
  ✘ o2: Retain allowFailure because waitFor alone makes a failed gate fatal
      why: Allowing failure contradicts the required fatal gate even when a dependency is named.
  ✘ o3: Remove waitFor and rely on textual stage order
      why: Downstream success dependencies must be explicit, not inferred from textual position.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Distinguish successful dependencies from failure-tolerance settings.']  remediation→r05
  MEASURES: C:integrate_and_verify_fatal_pipeline_admission_gates(f9,f10,f11,f12,f13)   anchors=[]
  taught-before-tested: C.f9←s12; C.f10←s13; C.f11←s13; C.f12←s13; C.f13←s13

### s16 · hands_on · Apply prevent duplicate or overlapping retraining runs
Practice — Complete the learner-defined function and required imports under the supplied policy; use the declared cases to verify the single deliverable.
QUESTION [code_exercise, core, grading=client] Read the supplied routines and bind `admit` to the one that satisfies the durable admission contract.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['pyyaml']} constraints.allowed=['import statements for supplied clients and yaml', 'function definitions, parameters and return statements', 'variable assignment', 'dictionary and list literals', 'dictionary key access for declared event and configuration fields', 'string literals for declared statuses, run keys and job identities', 'if, elif and else branches', 'comparisons and Boolean expressions', 'calls to supplied atomic admission, executor reconciliation, job-state and terminal-release methods', 'calls to supplied concurrency and restart fixture helpers', 'assert statements', 'with open(...) as file_handle', 'yaml.safe_dump(config, file_handle)', 'yaml.safe_load(file_handle)', 'raise SystemExit(...) for an unsuccessful rejected gate'] blocked=0 items
  file learner.py [editable]:
import numpy as np


exec("def supplied_admission(event, coordinator, executor):\n    claim = coordinator.atomic_admit(event['run_key'], event['pipeline'])\n    if claim['status'] == 'busy':\n        return {'status': statuses['busy_response'], 'job_id': claim['job_id']}\n    elif claim['completed']:\n        return {'status': statuses['completed_response'], 'job_id': claim['job_id']}\n    elif claim['status'] == 'accepted':\n        response = executor.launch(claim['job_id'])\n        if response == None:\n            executor.attach(claim['job_id'])\n    else:\n        executor.attach(claim['job_id'])\n    if executor.status(claim['job_id']) == 'terminal':\n        coordinator.confirm_terminal_and_release(event['run_key'], claim['job_id'])\n    return {'status': claim['status'], 'job_id': claim['job_id']}\n")

exec("def admission_busy(event, coordinator, executor):\n    claim = coordinator.atomic_admit(event['run_key'], event['pipeline'])\n    if claim['status'] == 'busy':\n        return {'status': claim['status'], 'job_id': claim['job_id']}\n    elif claim['completed']:\n        return {'status': statuses['completed_response'], 'job_id': claim['job_id']}\n    elif claim['status'] == 'accepted':\n        response = executor.launch(claim['job_id'])\n        if response == None:\n            executor.attach(claim['job_id'])\n    else:\n        executor.attach(claim['job_id'])\n    if executor.status(claim['job_id']) == 'terminal':\n        coordinator.confirm_terminal_and_release(event['run_key'], claim['job_id'])\n    return {'status': claim['status'], 'job_id': claim['job_id']}\n")

exec("def admission_retry(event, coordinator, executor):\n    claim = coordinator.atomic_admit(event['run_key'], event['pipeline'])\n    if claim['status'] == 'busy':\n        return {'status': statuses['busy_response'], 'job_id': claim['job_id']}\n    elif claim['completed']:\n        return {'status': statuses['completed_response'], 'job_id': claim['job_id']}\n    elif claim['status'] == 'accepted':\n        response = executor.launch(claim['job_id'])\n        if response == None:\n            executor.launch(claim['job_id'] + '-retry')\n    else:\n        executor.launch(claim['job_id'] + '-retry')\n    if executor.status(claim['job_id']) == 'terminal':\n        coordinator.confirm_terminal_and_release(event['run_key'], claim['job_id'])\n    return {'status': claim['status'], 'job_id': claim['job_id']}\n")

exec("def admission_release(event, coordinator, executor):\n    claim = coordinator.atomic_admit(event['run_key'], event['pipeline'])\n    if claim['status'] == 'busy':\n        return {'status': statuses['busy_response'], 'job_id': claim['job_id']}\n    elif claim['completed']:\n        return {'status': statuses['completed_response'], 'job_id': claim['job_id']}\n    elif claim['status'] == 'accepted':\n        response = executor.launch(claim['job_id'])\n        if response == None:\n            executor.attach(claim['job_id'])\n    else:\n        executor.attach(claim['job_id'])\n    if executor.status(claim['job_id']) != None:\n        executor.attach(claim['job_id'])\n    return {'status': claim['status'], 'job_id': claim['job_id']}\n")


# Read the supplied routines and select the durable admission entry point.
admit = None


event_run_key = 'K'

exec('import yaml')

status_config = 'busy_response: defer\ncompleted_response: completed\n'

loaded_statuses = yaml.safe_load(status_config)

statuses = loaded_statuses

exec("policy = {'event': {'run_key': 'K', 'pipeline': 'order-retrain-lab'}, 'busy_policy': 'defer', 'coordinator_contract': {'atomic_admit(run_key,pipeline)': 'Atomically reserve unique run key AND pipeline slot and persist job_id. Return accepted, duplicate or busy plus persisted identity; durable coordinator is external to learner process.', 'inspect(run_key)': 'Read durable record; completed records retained.', 'confirm_terminal_and_release(run_key,job_id)': 'Release active slot only after executor confirms terminal; retain completed key.'}, 'executor_contract': {'launch(job_id)': 'Idempotent executor token; at most one logical job per job_id. Unknown response must be reconciled with same token.', 'attach(job_id)': 'Resume or reconcile existing identity.', 'status(job_id)': 'Return running or confirmed terminal.'}, 'test_scenarios': ['concurrent_same_key', 'concurrent_different_key', 'restart_after_reservation', 'restart_after_launch', 'unknown_launch_response', 'completed_duplicate'], 'fatal_dependencies': ['admission', 'function_test', 'execute']}")

exec('import os, json')

exec("class Coordinator:\n\n    def __init__(self):\n        self.path = 'coordinator.json'\n        if not os.path.exists(self.path):\n            self.write({'claims': {}, 'slots': {}, 'jobs': {}})\n\n    def read(self):\n        with open(self.path) as f:\n            return json.load(f)\n\n    def write(self, state):\n        with open(self.path + '.tmp', 'w') as f:\n            json.dump(state, f)\n        os.replace(self.path + '.tmp', self.path)\n\n    def atomic_admit(self, key, pipeline):\n        try:\n            os.mkdir('coordinator.lock')\n        except FileExistsError:\n            return {'status': 'busy', 'job_id': None, 'completed': False}\n        try:\n            state = self.read()\n            if key in state['claims']:\n                row = state['claims'][key]\n                return {'status': 'duplicate', 'job_id': row['job_id'], 'completed': row['completed']}\n            if pipeline in state['slots']:\n                return {'status': 'busy', 'job_id': None, 'completed': False}\n            job = 'J.' + key\n            state['claims'][key] = {'pipeline': pipeline, 'job_id': job, 'completed': False}\n            state['slots'][pipeline] = key\n            self.write(state)\n            return {'status': 'accepted', 'job_id': job, 'completed': False}\n        finally:\n            os.rmdir('coordinator.lock')\n            hook = getattr(self, 'overlap_hook', None)\n            self.overlap_hook = None\n            if hook is not None:\n                hook()\n\n    def confirm_terminal_and_release(self, key, job):\n        try:\n            os.mkdir('coordinator.lock')\n        except FileExistsError:\n            return False\n        try:\n            state = self.read()\n            if state['jobs'].get(job) != 'terminal':\n                return False\n            row = state['claims'][key]\n            if row['job_id'] != job:\n                return False\n            row['completed'] = True\n            if state['slots'].get(row['pipeline']) == key:\n                del state['slots'][row['pipeline']]\n            self.write(state)\n            return True\n        finally:\n            os.rmdir('coordinator.lock')\n\n    def finish_jobs(self):\n        state = self.read()\n        state['jobs'] = {j: 'terminal' for j in state['jobs']}\n        self.write(state)")

exec("class Executor:\n\n    def __init__(self, coordinator):\n        self.coordinator = coordinator\n\n    def launch(self, job):\n        try:\n            os.mkdir('coordinator.lock')\n        except FileExistsError:\n            return job\n        try:\n            state = self.coordinator.read()\n            state['jobs'].setdefault(job, 'running')\n            self.coordinator.write(state)\n            if getattr(self, 'unknown_once', False):\n                self.unknown_once = False\n                return None\n            return job\n        finally:\n            os.rmdir('coordinator.lock')\n\n    def attach(self, job):\n        return self.launch(job)\n\n    def status(self, job):\n        return self.coordinator.read()['jobs'].get(job, 'unknown')")

exec('def fresh():\n    c = Coordinator()\n    return (c, Executor(c))')

exec("def reset():\n    c, e = fresh()\n    c.write({'claims': {}, 'slots': {}, 'jobs': {}})")

exec('def durable_state():\n    c, e = fresh()\n    return c.read()')

exec("def run_fixtures(admit, config):\n    event = policy['event']\n    key = event['run_key']\n    pipeline = event['pipeline']\n    out = {}\n    reset()\n    c1, e1 = fresh()\n    c2, e2 = fresh()\n    second = []\n    c1.overlap_hook = lambda: second.append(admit(event, c2, e2))\n    a = admit(event, c1, e1)\n    b = second[0]\n    state = durable_state()\n    out['same_key'] = {'results': [a, b], 'state': state}\n    out['same_key']['logical_job_count'] = len(state['jobs'])\n    reset()\n    c1, e1 = fresh()\n    c2, e2 = fresh()\n    second = []\n    c1.overlap_hook = lambda: second.append(admit({'run_key': key + '2', 'pipeline': pipeline}, c2, e2))\n    a = admit(event, c1, e1)\n    b2 = second[0]\n    state = durable_state()\n    out['different_key'] = {'result': b2, 'state': state, 'logical_job_count': len(state['jobs'])}\n    reset()\n    c, e = fresh()\n    reservation = c.atomic_admit(key, pipeline)\n    c2, e2 = fresh()\n    out['restart_reservation'] = {'result': admit(event, c2, e2), 'state': durable_state()}\n    reset()\n    c, e = fresh()\n    r = c.atomic_admit(key, pipeline)\n    e.launch(r['job_id'])\n    c2, e2 = fresh()\n    out['restart_launch'] = {'result': admit(event, c2, e2), 'state': durable_state()}\n    reset()\n    c3, e3 = fresh()\n    e3.unknown_once = True\n    uncertain = admit(event, c3, e3)\n    c4, e4 = fresh()\n    out['unknown_response'] = {'result': admit(event, c4, e4), 'state': durable_state()}\n    c.finish_jobs()\n    out['completion_release'] = admit(event, c3, e3)\n    out['completed_duplicate'] = {'result': admit(event, *fresh()), 'state': durable_state()}\n    fatal = all((not s.get('allowFailure', False) and (not s.get('allowExitCodes')) for s in config['steps']))\n    deps = config['steps'][1]['waitFor'] == ['entry'] and config['steps'][2]['waitFor'] == ['function_test']\n    out['pipeline'] = {'resolved': config, 'accepted': {'entry': 'success', 'function_test': 'success', 'execute': 'success'} if fatal and deps else {}, 'rejected': {'entry': 'failed', 'function_test': 'blocked', 'execute': 'blocked'}, 'resolved_inputs': event}\n    return out")

exec("policy['event']['run_key'] = event_run_key")

exec("config = {'steps': [{'id': 'entry', 'name': 'python:3.11', 'args': ['python3', 'entry_fixture.py']}, {'id': 'function_test', 'name': 'python:3.11', 'waitFor': ['entry'], 'args': ['python3', 'learner.py']}, {'id': 'execute', 'name': 'python:3.11', 'waitFor': ['function_test'], 'args': ['python3', 'execution_fixture.py']}]}")

exec("with open('build.yaml', 'w') as handle:\n    yaml.safe_dump(config, handle)")

exec("with open('build.yaml') as handle:\n    resolved = yaml.safe_load(handle)")

exec('result = run_fixtures(admit, resolved)')

assert result['same_key']['results'][0]['job_id'] == result['same_key']['results'][1]['job_id']

assert result['same_key']['logical_job_count'] == 1

assert result['different_key']['result']['status'] == 'defer'

assert result['different_key']['logical_job_count'] == 1

assert result['restart_reservation']['result']['job_id'] == result['restart_launch']['result']['job_id']

assert result['restart_reservation']['state']['jobs'] == result['restart_launch']['state']['jobs']

assert result['completed_duplicate']['result']['status'] == 'completed'

assert result['completed_duplicate']['state']['slots'] == {}

exec("logical_job_counts = {name: result[name].pop('logical_job_count') for name in ['same_key', 'different_key']}")

assert result['unknown_response']['result']['job_id'] == result['restart_launch']['result']['job_id'] and result['unknown_response']['state']['jobs'] == result['restart_launch']['state']['jobs']

  SOLUTION learner.py:
import numpy as np


exec("def supplied_admission(event, coordinator, executor):\n    claim = coordinator.atomic_admit(event['run_key'], event['pipeline'])\n    if claim['status'] == 'busy':\n        return {'status': statuses['busy_response'], 'job_id': claim['job_id']}\n    elif claim['completed']:\n        return {'status': statuses['completed_response'], 'job_id': claim['job_id']}\n    elif claim['status'] == 'accepted':\n        response = executor.launch(claim['job_id'])\n        if response == None:\n            executor.attach(claim['job_id'])\n    else:\n        executor.attach(claim['job_id'])\n    if executor.status(claim['job_id']) == 'terminal':\n        coordinator.confirm_terminal_and_release(event['run_key'], claim['job_id'])\n    return {'status': claim['status'], 'job_id': claim['job_id']}\n")

exec("def admission_busy(event, coordinator, executor):\n    claim = coordinator.atomic_admit(event['run_key'], event['pipeline'])\n    if claim['status'] == 'busy':\n        return {'status': claim['status'], 'job_id': claim['job_id']}\n    elif claim['completed']:\n        return {'status': statuses['completed_response'], 'job_id': claim['job_id']}\n    elif claim['status'] == 'accepted':\n        response = executor.launch(claim['job_id'])\n        if response == None:\n            executor.attach(claim['job_id'])\n    else:\n        executor.attach(claim['job_id'])\n    if executor.status(claim['job_id']) == 'terminal':\n        coordinator.confirm_terminal_and_release(event['run_key'], claim['job_id'])\n    return {'status': claim['status'], 'job_id': claim['job_id']}\n")

exec("def admission_retry(event, coordinator, executor):\n    claim = coordinator.atomic_admit(event['run_key'], event['pipeline'])\n    if claim['status'] == 'busy':\n        return {'status': statuses['busy_response'], 'job_id': claim['job_id']}\n    elif claim['completed']:\n        return {'status': statuses['completed_response'], 'job_id': claim['job_id']}\n    elif claim['status'] == 'accepted':\n        response = executor.launch(claim['job_id'])\n        if response == None:\n            executor.launch(claim['job_id'] + '-retry')\n    else:\n        executor.launch(claim['job_id'] + '-retry')\n    if executor.status(claim['job_id']) == 'terminal':\n        coordinator.confirm_terminal_and_release(event['run_key'], claim['job_id'])\n    return {'status': claim['status'], 'job_id': claim['job_id']}\n")

exec("def admission_release(event, coordinator, executor):\n    claim = coordinator.atomic_admit(event['run_key'], event['pipeline'])\n    if claim['status'] == 'busy':\n        return {'status': statuses['busy_response'], 'job_id': claim['job_id']}\n    elif claim['completed']:\n        return {'status': statuses['completed_response'], 'job_id': claim['job_id']}\n    elif claim['status'] == 'accepted':\n        response = executor.launch(claim['job_id'])\n        if response == None:\n            executor.attach(claim['job_id'])\n    else:\n        executor.attach(claim['job_id'])\n    if executor.status(claim['job_id']) != None:\n        executor.attach(claim['job_id'])\n    return {'status': claim['status'], 'job_id': claim['job_id']}\n")


# Read the supplied routines and select the durable admission entry point.
admit = supplied_admission


event_run_key = 'K'

exec('import yaml')

status_config = 'busy_response: defer\ncompleted_response: completed\n'

loaded_statuses = yaml.safe_load(status_config)

statuses = loaded_statuses

exec("policy = {'event': {'run_key': 'K', 'pipeline': 'order-retrain-lab'}, 'busy_policy': 'defer', 'coordinator_contract': {'atomic_admit(run_key,pipeline)': 'Atomically reserve unique run key AND pipeline slot and persist job_id. Return accepted, duplicate or busy plus persisted identity; durable coordinator is external to learner process.', 'inspect(run_key)': 'Read durable record; completed records retained.', 'confirm_terminal_and_release(run_key,job_id)': 'Release active slot only after executor confirms terminal; retain completed key.'}, 'executor_contract': {'launch(job_id)': 'Idempotent executor token; at most one logical job per job_id. Unknown response must be reconciled with same token.', 'attach(job_id)': 'Resume or reconcile existing identity.', 'status(job_id)': 'Return running or confirmed terminal.'}, 'test_scenarios': ['concurrent_same_key', 'concurrent_different_key', 'restart_after_reservation', 'restart_after_launch', 'unknown_launch_response', 'completed_duplicate'], 'fatal_dependencies': ['admission', 'function_test', 'execute']}")

exec('import os, json')

exec("class Coordinator:\n\n    def __init__(self):\n        self.path = 'coordinator.json'\n        if not os.path.exists(self.path):\n            self.write({'claims': {}, 'slots': {}, 'jobs': {}})\n\n    def read(self):\n        with open(self.path) as f:\n            return json.load(f)\n\n    def write(self, state):\n        with open(self.path + '.tmp', 'w') as f:\n            json.dump(state, f)\n        os.replace(self.path + '.tmp', self.path)\n\n    def atomic_admit(self, key, pipeline):\n        try:\n            os.mkdir('coordinator.lock')\n        except FileExistsError:\n            return {'status': 'busy', 'job_id': None, 'completed': False}\n        try:\n            state = self.read()\n            if key in state['claims']:\n                row = state['claims'][key]\n                return {'status': 'duplicate', 'job_id': row['job_id'], 'completed': row['completed']}\n            if pipeline in state['slots']:\n                return {'status': 'busy', 'job_id': None, 'completed': False}\n            job = 'J.' + key\n            state['claims'][key] = {'pipeline': pipeline, 'job_id': job, 'completed': False}\n            state['slots'][pipeline] = key\n            self.write(state)\n            return {'status': 'accepted', 'job_id': job, 'completed': False}\n        finally:\n            os.rmdir('coordinator.lock')\n            hook = getattr(self, 'overlap_hook', None)\n            self.overlap_hook = None\n            if hook is not None:\n                hook()\n\n    def confirm_terminal_and_release(self, key, job):\n        try:\n            os.mkdir('coordinator.lock')\n        except FileExistsError:\n            return False\n        try:\n            state = self.read()\n            if state['jobs'].get(job) != 'terminal':\n                return False\n            row = state['claims'][key]\n            if row['job_id'] != job:\n                return False\n            row['completed'] = True\n            if state['slots'].get(row['pipeline']) == key:\n                del state['slots'][row['pipeline']]\n            self.write(state)\n            return True\n        finally:\n            os.rmdir('coordinator.lock')\n\n    def finish_jobs(self):\n        state = self.read()\n        state['jobs'] = {j: 'terminal' for j in state['jobs']}\n        self.write(state)")

exec("class Executor:\n\n    def __init__(self, coordinator):\n        self.coordinator = coordinator\n\n    def launch(self, job):\n        try:\n            os.mkdir('coordinator.lock')\n        except FileExistsError:\n            return job\n        try:\n            state = self.coordinator.read()\n            state['jobs'].setdefault(job, 'running')\n            self.coordinator.write(state)\n            if getattr(self, 'unknown_once', False):\n                self.unknown_once = False\n                return None\n            return job\n        finally:\n            os.rmdir('coordinator.lock')\n\n    def attach(self, job):\n        return self.launch(job)\n\n    def status(self, job):\n        return self.coordinator.read()['jobs'].get(job, 'unknown')")

exec('def fresh():\n    c = Coordinator()\n    return (c, Executor(c))')

exec("def reset():\n    c, e = fresh()\n    c.write({'claims': {}, 'slots': {}, 'jobs': {}})")

exec('def durable_state():\n    c, e = fresh()\n    return c.read()')

exec("def run_fixtures(admit, config):\n    event = policy['event']\n    key = event['run_key']\n    pipeline = event['pipeline']\n    out = {}\n    reset()\n    c1, e1 = fresh()\n    c2, e2 = fresh()\n    second = []\n    c1.overlap_hook = lambda: second.append(admit(event, c2, e2))\n    a = admit(event, c1, e1)\n    b = second[0]\n    state = durable_state()\n    out['same_key'] = {'results': [a, b], 'state': state}\n    out['same_key']['logical_job_count'] = len(state['jobs'])\n    reset()\n    c1, e1 = fresh()\n    c2, e2 = fresh()\n    second = []\n    c1.overlap_hook = lambda: second.append(admit({'run_key': key + '2', 'pipeline': pipeline}, c2, e2))\n    a = admit(event, c1, e1)\n    b2 = second[0]\n    state = durable_state()\n    out['different_key'] = {'result': b2, 'state': state, 'logical_job_count': len(state['jobs'])}\n    reset()\n    c, e = fresh()\n    reservation = c.atomic_admit(key, pipeline)\n    c2, e2 = fresh()\n    out['restart_reservation'] = {'result': admit(event, c2, e2), 'state': durable_state()}\n    reset()\n    c, e = fresh()\n    r = c.atomic_admit(key, pipeline)\n    e.launch(r['job_id'])\n    c2, e2 = fresh()\n    out['restart_launch'] = {'result': admit(event, c2, e2), 'state': durable_state()}\n    reset()\n    c3, e3 = fresh()\n    e3.unknown_once = True\n    uncertain = admit(event, c3, e3)\n    c4, e4 = fresh()\n    out['unknown_response'] = {'result': admit(event, c4, e4), 'state': durable_state()}\n    c.finish_jobs()\n    out['completion_release'] = admit(event, c3, e3)\n    out['completed_duplicate'] = {'result': admit(event, *fresh()), 'state': durable_state()}\n    fatal = all((not s.get('allowFailure', False) and (not s.get('allowExitCodes')) for s in config['steps']))\n    deps = config['steps'][1]['waitFor'] == ['entry'] and config['steps'][2]['waitFor'] == ['function_test']\n    out['pipeline'] = {'resolved': config, 'accepted': {'entry': 'success', 'function_test': 'success', 'execute': 'success'} if fatal and deps else {}, 'rejected': {'entry': 'failed', 'function_test': 'blocked', 'execute': 'blocked'}, 'resolved_inputs': event}\n    return out")

exec("policy['event']['run_key'] = event_run_key")

exec("config = {'steps': [{'id': 'entry', 'name': 'python:3.11', 'args': ['python3', 'entry_fixture.py']}, {'id': 'function_test', 'name': 'python:3.11', 'waitFor': ['entry'], 'args': ['python3', 'learner.py']}, {'id': 'execute', 'name': 'python:3.11', 'waitFor': ['function_test'], 'args': ['python3', 'execution_fixture.py']}]}")

exec("with open('build.yaml', 'w') as handle:\n    yaml.safe_dump(config, handle)")

exec("with open('build.yaml') as handle:\n    resolved = yaml.safe_load(handle)")

exec('result = run_fixtures(admit, resolved)')

assert result['same_key']['results'][0]['job_id'] == result['same_key']['results'][1]['job_id']

assert result['same_key']['logical_job_count'] == 1

assert result['different_key']['result']['status'] == 'defer'

assert result['different_key']['logical_job_count'] == 1

assert result['restart_reservation']['result']['job_id'] == result['restart_launch']['result']['job_id']

assert result['restart_reservation']['state']['jobs'] == result['restart_launch']['state']['jobs']

assert result['completed_duplicate']['result']['status'] == 'completed'

assert result['completed_duplicate']['state']['slots'] == {}

exec("logical_job_counts = {name: result[name].pop('logical_job_count') for name in ['same_key', 'different_key']}")

assert result['unknown_response']['result']['job_id'] == result['restart_launch']['result']['job_id'] and result['unknown_response']['state']['jobs'] == result['restart_launch']['state']['jobs']

  test t1 (value_equals, visible=True): {"expr":"result","expected":{"same_key":{"results":[{"status":"accepted","job_id":"J.K"},{"status":"duplicate","job_id":"J.K"}],"state":{"claims":{"K":{"pipeline":"order-retrain-lab","job_id":"J.K","completed":false}},"slots":{"order-retrain-lab":"K"},"jobs":{"J.K":"running"}}},"different_key":{"result":{"status":"defer","job_id":null},"state":{"claims":{"K":{"pipeline":"order-retrain-lab","job_id":"J.K","completed":false}},"slots":{"order-retrain-lab":"K"},"jobs":{"J.K":"running"}}},"restart_re | on-fail: The returned record or calculation does not match the declared fixture contract.
  test overlap_logical_jobs (value_equals, visible=True): {"expr":"{'counts':logical_job_counts,'run_key':policy['event']['run_key']}","expected":{"counts":{"same_key":1,"different_key":1},"run_key":"K"}} | on-fail: The returned record or calculation does not match the declared fixture contract.
  test unknown_response_durable_job (value_equals, visible=True): {"expr":"{'job_id':result['unknown_response']['result']['job_id'], 'jobs':result['unknown_response']['state']['jobs'], 'single_persisted_job':len(result['unknown_response']['state']['jobs']) == 1 and result['unknown_response']['result']['job_id'] in result['unknown_response']['state']['jobs']}","expected":{"job_id":"J.K","jobs":{"J.K":"running"},"single_persisted_job":true}} | on-fail: Unknown response reconciliation must retain the persisted single logical job.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"eb7f32aef8f3d9285c8ca06ba617bf8ebebd8131cf1b37f72898058aa67b0bb2","tests_passed":3}
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Every attach, launch and terminal-release operation must refer to the claim’s persisted job_id; inspect the same-key, different-key and restart fixture evidence.']
  MEASURES: C:enforce_atomic_retraining_admission(f1,f2,f3,f6); C:preserve_job_identity_across_retries_and_restarts(f4,f5); C:release_terminal_slots_without_relaunching_completed_keys(f7); C:verify_durable_concurrency_and_restart_invariants(f2,f4,f5,f6,f7,f8); C:integrate_and_verify_fatal_pipeline_admission_gates(f9,f10,f11,f12,f13)   anchors=['practice']
  taught-before-tested: C.f1←s11; C.f2←s11; C.f3←s11; C.f6←s12; C.f4←s12; C.f5←s12; C.f7←s12; C.f2←s11; C.f4←s12; C.f5←s12; C.f6←s12; C.f7←s12; C.f8←s12; C.f9←s12; C.f10←s13; C.f11←s13; C.f12←s13; C.f13←s13

### s17 · explainer · Gate a retrained candidate against the incumbent using validation evidence before controlled promotion
(intro) Compare candidate and incumbent on a shared validation cohort. Record every required gate and the exact candidate identity; aggregate improvement alone is not acceptance. ⟦D:tb1⟧
(mechanism) Evaluate the retrained candidate and incumbent on the same declared validation cohort and compare them against the predeclared acceptance requirements. Use the supplied deployment class probabilities and error costs to calculate candidate and incumbent expected cost under the fixed selection rule. Reject a candidate that fails a required quality, slice or deployment-compatibility gate even if its aggregate validation score improves. ⟦D.f1 D.f2 D.f3 D:tb2⟧
(mechanism) Bind the candidate’s exact registry/artifact identity and gate verdict to the controlled promotion record; validation of one artifact does not approve a different artifact. For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate. With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦D.f4 D.f5 D.f6 D:tb3⟧
[CODE python]
negative_count = FP + TN
positive_count = FN + TP
# Empty actual-class groups yield undefined rates; reject explicitly.
FPR = FP / negative_count
FNR = FN / positive_count
expected_cost = P_Y0 * FPR * cost_FP + P_Y1 * FNR * cost_FN
# Acceptance requires cost, quality, slice and compatibility gates.
# Bind the exact registry_artifact_id and cohort_id to the verdict.
assert not accepted_when_required_gate_fails
  annotations: []
[TABLE computed result ] caption: Conditional rates, incumbent-relative costs and identity-bound gates; undefined groups reject.
  produced by sql: WITH rates AS (SELECT *,1.0*FP/NULLIF(FP+TN,0) AS FPR,1.0*FN/NULLIF(FN+TP,0) AS FNR FROM counts), costs AS (SELECT *,0.5*FPR*1+0.5*FNR*2 AS expected_cost FROM rates), gates AS (SELECT *,FPR<=0.1 AND FNR<=0.1 AS quality_pass,expected_cost<=(SELECT i.expected_cost FROM costs i WHERE i.fixture=c.fixture AND i.model_role='incumbent') AS cost_pass FROM costs c) SELECT *, CASE WHEN quality_pass AND cost_pass AND slice_pass AND compatibility_pass THEN 'accept' ELSE 'reject' END AS verdict FROM gates
  result columns=['fixture', 'model_role', 'cohort_id', 'registry_artifact_id', 'FP', 'TN', 'FN', 'TP', 'slice_pass', 'compatibility_pass', 'FPR', 'FNR', 'expected_cost', 'quality_pass', 'cost_pass', 'verdict'] rows(12)=[["valid","incumbent","cohort.validation","model.incumbent",10,40,10,40,true,true,0.2,0.2,0.30000000000000004,false,true,"reject"],["valid","candidate","cohort.validation","model.valid",2,48,3,47,true,true,0.04,0.06,0.08,true,true,"accept"],["boundary","incumbent","cohort.validation","model.incumbent",10,40,10,40,true,true,0.2,0.2,0.30000000000000004,false,true,"reject"],["boundary","candidate","cohort.validation","model.boundary",5,45,5,45,true,true,0.1,0.1,0.15000000000000002,true,true,"accept

### s18 · explainer · Gate a retrained candidate against the incumbent using validation evidence before controlled promotion
(mechanism) Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system. Use assert predicates for declared valid, boundary and failure cases; a false predicate raises AssertionError in ordinary non-optimized execution. ⟦D.f7 D.f8 D:tb4⟧

### s19 · explainer · Apply the rule: Gate a retrained candidate against the incumbent using validation evidence before controlled promotion
(example) Lower expected cost cannot override a failed required slice or compatibility gate. Compare both models under the same deployment probabilities, error costs and actual-class conditional rates. Reject undefined conditioning rates. Keep protected-test observations out of fitting and setting choice. Bind the exact candidate artifact and verdict to the promotion record, and assert valid, boundary and failure cases. Approval for one candidate is not approval for another. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D.f8 D:tb5⟧
(misconception) Retrained does not mean accepted. An aggregate gain cannot bypass a required slice or compatibility gate, and validation of one artifact does not approve another. ⟦D.f3 D.f4 D:tb6⟧

### s20 · check · Review gate a retrained candidate against the incumbent using validation evidence before controlled promotion
Check the distinction — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [choice, stretch, grading=client] The fixed candidate gate accepts equality at its declared maximum. In ordinary non-optimized Python, which unit-test strategy verifies the valid, boundary and failure outcomes?
  ✔ o1: Assert valid and equality cases pass and each declared failure case rejects
      why: Assertions cover the required outcomes; a false predicate raises AssertionError.
  ✘ o2: Assert only one aggregate-improvement case passes
      why: One passing case leaves boundary and failure behavior unverified.
  ✘ o3: Replace assertions with comments describing the desired outcomes
      why: Comments do not check predicates during execution.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['A test needs an executable predicate for each declared outcome.']  remediation→r07
  MEASURES: D:assert_valid_boundary_and_failure_gate_outcomes(f8)   anchors=[]
  taught-before-tested: D.f8←s18

### s21 · hands_on · Apply gate a retrained candidate against the incumbent using validation evidence before controlled promotion
Practice — Complete the learner-defined function and required imports under the supplied policy; use the declared cases to verify the single deliverable.
QUESTION [code_exercise, stretch, grading=client] Read the supplied rules and bind each rule name to the callable that satisfies the declared conditional-rate, expected-cost and acceptance contract.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy']} constraints.allowed=['import statements for supplied library and client dependencies', 'def statements with parameters and return statements', 'local variable assignment', 'numeric, string, boolean and None literals', 'dictionary construction and key access', 'arithmetic operators +, -, *, /', 'comparison operators ==, !=, <, <=, >, >=', 'boolean operators and, or, not', 'if, elif and else statements', 'calls to supplied fixture, unit-test and promotion-record interfaces', 'assert predicate statements'] blocked=5 items
  file learner.py [editable]:
import numpy as np

# Supplied conditional-rate and gate interfaces; bind the five rule names below.
exec("def supplied_fpr_rule(model):\n    return model['FP'] / (model['FP'] + model['TN'])\n\ndef supplied_fnr_rule(model):\n    return model['FN'] / (model['FN'] + model['TP'])\n\ndef supplied_cost_rule(fpr, fnr):\n    return false_positive_weight * fpr + false_negative_weight * fnr\n\ndef supplied_quality_rule(cand, inc):\n    return cand['FPR'] <= policy['acceptance']['maximum_FPR'] and cand['FNR'] <= policy['acceptance']['maximum_FNR'] and (cand['cost'] <= inc['cost'])\n\ndef supplied_passed_rule(quality, candidate, incumbent, requested_identity):\n    return quality and candidate['slice_pass'] and candidate['compatibility_pass'] and (candidate['cohort_id'] == incumbent['cohort_id']) and (candidate['cohort_id'] == policy['cohort']) and (candidate['registry_artifact_id'] == requested_identity)\n\ndef rates(model):\n    if model['FP'] + model['TN'] == 0 or model['FN'] + model['TP'] == 0:\n        return {'FPR': None, 'FNR': None, 'cost': None}\n    fpr = fpr_rule(model)\n    fnr = fnr_rule(model)\n    cost = cost_rule(fpr, fnr)\n    return {'FPR': fpr, 'FNR': fnr, 'cost': cost}\n\ndef evaluate(incumbent, candidate, requested_identity):\n    inc = rates(incumbent)\n    cand = rates(candidate)\n    quality = False\n    if cand['cost'] != None and inc['cost'] != None:\n        quality = quality_rule(cand, inc)\n    passed = passed_rule(quality, candidate, incumbent, requested_identity)\n    return {'registry_artifact_id': candidate['registry_artifact_id'], 'cohort_id': candidate['cohort_id'], 'FPR': cand['FPR'], 'FNR': cand['FNR'], 'expected_cost': cand['cost'], 'incumbent_rates': inc, 'quality_pass': quality, 'slice_pass': candidate['slice_pass'], 'compatibility_pass': candidate['compatibility_pass'], 'verdict': passed}\n\n\ndef pooled_fpr_rule(model):\n    return model['FP'] / (model['FP'] + model['TN'] + model['FN'] + model['TP'])\n\ndef pooled_fnr_rule(model):\n    return model['FN'] / (model['FP'] + model['TN'] + model['FN'] + model['TP'])\n\ndef reversed_cost_rule(fpr, fnr):\n    return false_negative_weight * fpr + false_positive_weight * fnr\n\ndef strict_quality_rule(cand, inc):\n    return cand['FPR'] < policy['acceptance']['maximum_FPR'] and cand['FNR'] < policy['acceptance']['maximum_FNR'] and (cand['cost'] < inc['cost'])\n\ndef partial_passed_rule(quality, candidate, incumbent, requested_identity):\n    return quality and (candidate['cohort_id'] == incumbent['cohort_id']) and (candidate['cohort_id'] == policy['cohort']) and (candidate['registry_artifact_id'] == requested_identity)\n")

fpr_rule = None  # Select a supplied rule satisfying the contract.
fnr_rule = None  # Select a supplied rule satisfying the contract.
cost_rule = None  # Select a supplied rule satisfying the contract.
quality_rule = None  # Select a supplied rule satisfying the contract.
passed_rule = None  # Select a supplied rule satisfying the contract.


exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"P_Y0": 0.5, "P_Y1": 0.5, "cost_FP": 1, "cost_FN": 2, "acceptance": {"maximum_FPR": 0.1, "maximum_FNR": 0.1, "cost_not_above_incumbent": true, "slice_pass_required": true, "compatibility_pass_required": true}, "empty_group": "undefined; reject", "cohort": "cohort.validation", "decision_record_fields": ["registry_artifact_id", "cohort_id", "FPR", "FNR", "expected_cost", "quality_pass", "slice_pass", "compatibility_pass", "verdict"], "protected_test": "not provided; never used for selection"}\')')

exec("validation_counts_rows = list(csv.DictReader(open('validation_counts.csv')))")

exec('validation_counts = {}')

exec("validation_counts['fixture'] = np.array([r['fixture'] for r in validation_counts_rows])")

exec("validation_counts['model_role'] = np.array([r['model_role'] for r in validation_counts_rows])")

exec("validation_counts['cohort_id'] = np.array([r['cohort_id'] for r in validation_counts_rows])")

exec("validation_counts['registry_artifact_id'] = np.array([r['registry_artifact_id'] for r in validation_counts_rows])")

exec("validation_counts['FP'] = np.array([float(r['FP'] or 'nan') for r in validation_counts_rows])")

exec("validation_counts['TN'] = np.array([float(r['TN'] or 'nan') for r in validation_counts_rows])")

exec("validation_counts['FN'] = np.array([float(r['FN'] or 'nan') for r in validation_counts_rows])")

exec("validation_counts['TP'] = np.array([float(r['TP'] or 'nan') for r in validation_counts_rows])")

exec("validation_counts['slice_pass'] = np.array([r['slice_pass'] == 'True' for r in validation_counts_rows])")

exec("validation_counts['compatibility_pass'] = np.array([r['compatibility_pass'] == 'True' for r in validation_counts_rows])")

exec('fixtures = {}')

exec("for i in range(len(validation_counts_rows)):\n    r = {k: v[i].item() if hasattr(v[i], 'item') else v[i] for k, v in validation_counts.items()}\n    fixtures.setdefault(r['fixture'], {})[r['model_role']] = r")

exec("def test_all(evaluate):\n    out = []\n    for name, pair in fixtures.items():\n        c = pair['candidate']\n        inc = pair['incumbent']\n        out.append({'fixture': name, 'record': evaluate(inc, c, c['registry_artifact_id'])})\n    pair = fixtures['valid']\n    out.append({'fixture': 'identity_mismatch', 'record': evaluate(pair['incumbent'], pair['candidate'], 'model.unrelated')})\n    return out")

exec("def assert_failures(check_failure):\n    for name, pair in fixtures.items():\n        if name not in ['valid', 'boundary']:\n            check_failure(pair)")


supplied_false_positive_weight = policy['P_Y0'] * policy['cost_FP']
false_positive_weight = supplied_false_positive_weight


supplied_false_negative_weight = policy['P_Y1'] * policy['cost_FN']
false_negative_weight = supplied_false_negative_weight

assert evaluate(fixtures['valid']['incumbent'], fixtures['valid']['candidate'], fixtures['valid']['candidate']['registry_artifact_id'])['verdict']

assert evaluate(fixtures['boundary']['incumbent'], fixtures['boundary']['candidate'], fixtures['boundary']['candidate']['registry_artifact_id'])['verdict']

assert not evaluate(fixtures['valid']['incumbent'], fixtures['valid']['candidate'], 'model.unrelated')['verdict']

exec("def check_failure(pair):\n    assert not evaluate(pair['incumbent'], pair['candidate'], pair['candidate']['registry_artifact_id'])['verdict']")

exec('assert_failures(check_failure)')

result = test_all(evaluate)

  SOLUTION learner.py:
import numpy as np

# Supplied conditional-rate and gate interfaces; bind the five rule names below.
exec("def supplied_fpr_rule(model):\n    return model['FP'] / (model['FP'] + model['TN'])\n\ndef supplied_fnr_rule(model):\n    return model['FN'] / (model['FN'] + model['TP'])\n\ndef supplied_cost_rule(fpr, fnr):\n    return false_positive_weight * fpr + false_negative_weight * fnr\n\ndef supplied_quality_rule(cand, inc):\n    return cand['FPR'] <= policy['acceptance']['maximum_FPR'] and cand['FNR'] <= policy['acceptance']['maximum_FNR'] and (cand['cost'] <= inc['cost'])\n\ndef supplied_passed_rule(quality, candidate, incumbent, requested_identity):\n    return quality and candidate['slice_pass'] and candidate['compatibility_pass'] and (candidate['cohort_id'] == incumbent['cohort_id']) and (candidate['cohort_id'] == policy['cohort']) and (candidate['registry_artifact_id'] == requested_identity)\n\ndef rates(model):\n    if model['FP'] + model['TN'] == 0 or model['FN'] + model['TP'] == 0:\n        return {'FPR': None, 'FNR': None, 'cost': None}\n    fpr = fpr_rule(model)\n    fnr = fnr_rule(model)\n    cost = cost_rule(fpr, fnr)\n    return {'FPR': fpr, 'FNR': fnr, 'cost': cost}\n\ndef evaluate(incumbent, candidate, requested_identity):\n    inc = rates(incumbent)\n    cand = rates(candidate)\n    quality = False\n    if cand['cost'] != None and inc['cost'] != None:\n        quality = quality_rule(cand, inc)\n    passed = passed_rule(quality, candidate, incumbent, requested_identity)\n    return {'registry_artifact_id': candidate['registry_artifact_id'], 'cohort_id': candidate['cohort_id'], 'FPR': cand['FPR'], 'FNR': cand['FNR'], 'expected_cost': cand['cost'], 'incumbent_rates': inc, 'quality_pass': quality, 'slice_pass': candidate['slice_pass'], 'compatibility_pass': candidate['compatibility_pass'], 'verdict': passed}\n\n\ndef pooled_fpr_rule(model):\n    return model['FP'] / (model['FP'] + model['TN'] + model['FN'] + model['TP'])\n\ndef pooled_fnr_rule(model):\n    return model['FN'] / (model['FP'] + model['TN'] + model['FN'] + model['TP'])\n\ndef reversed_cost_rule(fpr, fnr):\n    return false_negative_weight * fpr + false_positive_weight * fnr\n\ndef strict_quality_rule(cand, inc):\n    return cand['FPR'] < policy['acceptance']['maximum_FPR'] and cand['FNR'] < policy['acceptance']['maximum_FNR'] and (cand['cost'] < inc['cost'])\n\ndef partial_passed_rule(quality, candidate, incumbent, requested_identity):\n    return quality and (candidate['cohort_id'] == incumbent['cohort_id']) and (candidate['cohort_id'] == policy['cohort']) and (candidate['registry_artifact_id'] == requested_identity)\n")

fpr_rule = supplied_fpr_rule
fnr_rule = supplied_fnr_rule
cost_rule = supplied_cost_rule
quality_rule = supplied_quality_rule
passed_rule = supplied_passed_rule


exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"P_Y0": 0.5, "P_Y1": 0.5, "cost_FP": 1, "cost_FN": 2, "acceptance": {"maximum_FPR": 0.1, "maximum_FNR": 0.1, "cost_not_above_incumbent": true, "slice_pass_required": true, "compatibility_pass_required": true}, "empty_group": "undefined; reject", "cohort": "cohort.validation", "decision_record_fields": ["registry_artifact_id", "cohort_id", "FPR", "FNR", "expected_cost", "quality_pass", "slice_pass", "compatibility_pass", "verdict"], "protected_test": "not provided; never used for selection"}\')')

exec("validation_counts_rows = list(csv.DictReader(open('validation_counts.csv')))")

exec('validation_counts = {}')

exec("validation_counts['fixture'] = np.array([r['fixture'] for r in validation_counts_rows])")

exec("validation_counts['model_role'] = np.array([r['model_role'] for r in validation_counts_rows])")

exec("validation_counts['cohort_id'] = np.array([r['cohort_id'] for r in validation_counts_rows])")

exec("validation_counts['registry_artifact_id'] = np.array([r['registry_artifact_id'] for r in validation_counts_rows])")

exec("validation_counts['FP'] = np.array([float(r['FP'] or 'nan') for r in validation_counts_rows])")

exec("validation_counts['TN'] = np.array([float(r['TN'] or 'nan') for r in validation_counts_rows])")

exec("validation_counts['FN'] = np.array([float(r['FN'] or 'nan') for r in validation_counts_rows])")

exec("validation_counts['TP'] = np.array([float(r['TP'] or 'nan') for r in validation_counts_rows])")

exec("validation_counts['slice_pass'] = np.array([r['slice_pass'] == 'True' for r in validation_counts_rows])")

exec("validation_counts['compatibility_pass'] = np.array([r['compatibility_pass'] == 'True' for r in validation_counts_rows])")

exec('fixtures = {}')

exec("for i in range(len(validation_counts_rows)):\n    r = {k: v[i].item() if hasattr(v[i], 'item') else v[i] for k, v in validation_counts.items()}\n    fixtures.setdefault(r['fixture'], {})[r['model_role']] = r")

exec("def test_all(evaluate):\n    out = []\n    for name, pair in fixtures.items():\n        c = pair['candidate']\n        inc = pair['incumbent']\n        out.append({'fixture': name, 'record': evaluate(inc, c, c['registry_artifact_id'])})\n    pair = fixtures['valid']\n    out.append({'fixture': 'identity_mismatch', 'record': evaluate(pair['incumbent'], pair['candidate'], 'model.unrelated')})\n    return out")

exec("def assert_failures(check_failure):\n    for name, pair in fixtures.items():\n        if name not in ['valid', 'boundary']:\n            check_failure(pair)")


supplied_false_positive_weight = policy['P_Y0'] * policy['cost_FP']
false_positive_weight = supplied_false_positive_weight


supplied_false_negative_weight = policy['P_Y1'] * policy['cost_FN']
false_negative_weight = supplied_false_negative_weight

assert evaluate(fixtures['valid']['incumbent'], fixtures['valid']['candidate'], fixtures['valid']['candidate']['registry_artifact_id'])['verdict']

assert evaluate(fixtures['boundary']['incumbent'], fixtures['boundary']['candidate'], fixtures['boundary']['candidate']['registry_artifact_id'])['verdict']

assert not evaluate(fixtures['valid']['incumbent'], fixtures['valid']['candidate'], 'model.unrelated')['verdict']

exec("def check_failure(pair):\n    assert not evaluate(pair['incumbent'], pair['candidate'], pair['candidate']['registry_artifact_id'])['verdict']")

exec('assert_failures(check_failure)')

result = test_all(evaluate)

  test t1 (value_equals, visible=True): {"expr":"result","expected":[{"fixture":"valid","record":{"registry_artifact_id":"model.valid","cohort_id":"cohort.validation","FPR":0.04,"FNR":0.06,"expected_cost":0.08,"incumbent_rates":{"FPR":0.2,"FNR":0.2,"cost":0.30000000000000004},"quality_pass":true,"slice_pass":true,"compatibility_pass":true,"verdict":true}},{"fixture":"boundary","record":{"registry_artifact_id":"model.boundary","cohort_id":"cohort.validation","FPR":0.1,"FNR":0.1,"expected_cost":0.15000000000000002,"incumbent_rates":{"FP | on-fail: The returned record or calculation does not match the declared fixture contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"9cb78417cf0d29e464f1e2b41a302a9caecfceb0a0343a3a9bda3fb37db36356","tests_passed":1}
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['FP/TN and FN/TP are separate conditioning groups. Bind the decision to policy cohort and requested_identity as well as the quality and compatibility gates.']
  MEASURES: D:verify_matched_validation_and_protected_test_isolation(f1,f7); D:calculate_incumbent_relative_expected_error_cost(f2,f5,f6); D:enforce_all_required_acceptance_gates(f3); D:bind_gate_verdict_to_exact_candidate_identity(f4); D:assert_valid_boundary_and_failure_gate_outcomes(f8)   anchors=['practice']
  taught-before-tested: D.f1←s17; D.f7←s18; D.f2←s17; D.f5←s17; D.f6←s17; D.f3←s17; D.f4←s17; D.f8←s18

### s22 · recap · Keep these distinctions
(takeaway) Bind trigger reason and intended dataset without confusing retraining with deployment approval. Verify permitted invocation and actual immutable-input consumption. Preserve durable job identity across retries. Accept only the exact candidate that passes every required gate.
[UP NEXT] Use an ML incident runbook for safe recovery on an existing platform: Recovery is scoped to one authorized nonproduction instance. Reproduce and isolate the injected service fault, then test the supported hypothesis before the lifecycle action.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Choose scheduled, new-data or investigated quality/drift retraining triggers
(mechanism) Keep handoff credentials runtime-injected and out of the policy, YAML values and captured stage logs. ⟦A.f8 A:tb4⟧
(misconception) Runtime injection keeps handoff credentials out of policy, YAML and captured logs. Writing credential values into any of those records violates that boundary. ⟦A.f8 A:tb4⟧
### r02 · Revisit: Choose scheduled, new-data or investigated quality/drift retraining triggers
(mechanism) ML pipeline execution can be triggered by a schedule, availability of new training data, observed degradation of model performance or a significant change in data distribution. ⟦A.f1 A:tb2⟧
(mechanism) Choose the trigger supported by the supplied operational evidence, and retain the trigger reason and intended input dataset. ⟦A.f2 A:tb2⟧
(mechanism) Label-verified performance evidence and a distribution-only signal are different trigger evidence; do not describe drift alone as measured prediction error. ⟦A.f3 A:tb2⟧
(mechanism) A retraining trigger starts a gated pipeline; it does not by itself approve the resulting candidate for deployment. ⟦A.f4 A:tb3⟧
(mechanism) Reject unauthorized identities and uninvestigated alarm events at entry under the existing policy; preserve separate authorization for any later promotion. ⟦A.f5 A:tb3⟧
(mechanism) Annotate the existing data-quality/test, training and evaluation stages with their input artifacts and purpose, and make promotion depend on its own approval rather than retraining alone. ⟦A.f6 A:tb3⟧
(mechanism) Trace one eligible event through the existing entry and required dependencies, then trace a failed check to show precisely which downstream stages cannot execute. ⟦A.f7 A:tb4⟧
(mechanism) Keep handoff credentials runtime-injected and out of the policy, YAML values and captured stage logs. ⟦A.f8 A:tb4⟧
(misconception) Retraining eligibility is not deployment approval. A distribution-only signal must not be relabeled as measured prediction degradation, and an alarm is not automatically an authorized trigger. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A:tb2 A:tb3 A:tb4⟧
### r03 · Revisit: Invoke retraining with a versioned input snapshot from an authorized trigger
(mechanism) Bind approved Secret Manager version references with availableSecrets.secretManager and expose them only to the needed step through secretEnv; the YAML contains references, not secret values. ⟦B.f10 B:tb5⟧
(mechanism) Check captured build output for non-disclosure of secret values; do not echo or serialize runtime credentials. ⟦B.f12 B:tb5⟧
(misconception) Secret Manager versions belong in availableSecrets.secretManager references and scoped secretEnv, not literal credential values. Check captured output too: a reference-only YAML does not excuse leaked logs. ⟦B.f10 B.f12 B:tb5⟧
### r04 · Revisit: Invoke retraining with a versioned input snapshot from an authorized trigger
(mechanism) Check that the trigger identity is permitted to execute the existing pipeline and access the intended input resources before invoking retraining. ⟦B.f1 B:tb2⟧
(mechanism) Use the authorized build/step identity and preserve the separate authorization required for a promotion action. ⟦B.f11 B:tb5⟧
(mechanism) Inspect the triggered execution’s actual stage inputs and compare the consumed snapshot identity with the approved immutable input; the start request alone is not proof of consumption. ⟦B.f13 B:tb6⟧
(mechanism) Import yaml from the declared PyYAML dependency. Write mappings/lists with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python constructors. ⟦B.f14 B:tb6⟧
(mechanism) Resolve the authorized input snapshot to the recorded object generation and verify it, instead of training on a mutable current dataset name. ⟦B.f2 B:tb2⟧
(mechanism) Use import boto3 and boto3.client("sagemaker").start_pipeline_execution(PipelineName=..., PipelineParameters=[{"Name": ..., "Value": ...}], ClientRequestToken=...) with the supplied pipeline and resolved snapshot parameters. ⟦B.f3 B:tb2⟧
(mechanism) Retain the returned PipelineExecutionArn and the actual parameters as the retraining run’s invocation identity. ⟦B.f4 B:tb3⟧
(mechanism) Bind the trigger authorization, dataset version and returned execution identity in one record so the invocation can be audited. ⟦B.f5 B:tb3⟧
(mechanism) In existing Cloud Build YAML/JSON steps, name specifies the execution image; args or script specifies the command. Wire the function/test entry into its assigned stage. ⟦B.f6 B:tb3⟧
(mechanism) Assign step IDs and required predecessor IDs in waitFor. Successful dependencies, not textual order, permit downstream execution. ⟦B.f7 B:tb4⟧
(mechanism) Required failures stay fatal: no allowFailure or failing codes in allowExitCodes; rejected Python gates must exit unsuccessfully. ⟦B.f8 B:tb4⟧
(mechanism) Use the existing Pub/Sub artifact/event trigger, payload bindings and filters. Inspect actual stage results and resolved inputs for accepted and rejected fixtures. ⟦B.f9 B:tb4⟧
(misconception) A start request proves neither authorized input consumption nor promotion approval. Verify actual resolved stage inputs and keep secret values out of invocation records and logs. ⟦B.f1 B.f11 B.f13 B.f14 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B.f9 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6⟧
### r05 · Revisit: Prevent duplicate or overlapping retraining runs
(mechanism) Assign step IDs and required predecessor IDs in waitFor. Successful dependencies, not textual order, permit downstream execution. ⟦C.f10 C:tb5⟧
(mechanism) Required failures stay fatal: no allowFailure or failing codes in allowExitCodes; rejected Python gates must exit unsuccessfully. ⟦C.f11 C:tb5⟧
(mechanism) Use the existing Pub/Sub artifact/event trigger, payload bindings and filters. Inspect actual stage results and resolved inputs for accepted and rejected fixtures. ⟦C.f12 C:tb5⟧
(mechanism) Import yaml from the declared PyYAML dependency. Write mappings/lists with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python constructors. ⟦C.f13 C:tb6⟧
(mechanism) In existing Cloud Build YAML/JSON steps, name specifies the execution image; args or script specifies the command. Wire the function/test entry into its assigned stage. ⟦C.f9 C:tb4⟧
(misconception) A textual stage order is not a successful-dependency gate. Use required waitFor IDs, keep failing gates fatal and inspect actual accepted/rejected stage results and resolved inputs. ⟦C.f10 C.f11 C.f12 C.f13 C.f9 C:tb4 C:tb5 C:tb6⟧
### r06 · Revisit: Prevent duplicate or overlapping retraining runs
(mechanism) Read the declared run key and pipeline identity from the dictionary event record, and pass them to the supplied durable coordinator’s atomic admission operation. ⟦C.f1 C:tb2⟧
(mechanism) Assign step IDs and required predecessor IDs in waitFor. Successful dependencies, not textual order, permit downstream execution. ⟦C.f10 C:tb5⟧
(mechanism) Required failures stay fatal: no allowFailure or failing codes in allowExitCodes; rejected Python gates must exit unsuccessfully. ⟦C.f11 C:tb5⟧
(mechanism) Use the existing Pub/Sub artifact/event trigger, payload bindings and filters. Inspect actual stage results and resolved inputs for accepted and rejected fixtures. ⟦C.f12 C:tb5⟧
(mechanism) Import yaml from the declared PyYAML dependency. Write mappings/lists with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python constructors. ⟦C.f13 C:tb6⟧
(mechanism) One supplied atomic operation reserves both unique run key and pipeline slot and persists job ID. Process-local dictionaries and separate check-then-write calls cannot supply this durable contract. ⟦C.f2 C:tb2⟧
(mechanism) Handle returned accepted, duplicate and busy statuses with explicit conditional branches: only an accepted reservation authorizes a new logical launch. ⟦C.f3 C:tb2⟧
(mechanism) For an accepted claim, invoke the executor with the reserved persisted job ID as its idempotency token; do not generate a replacement identity after a retry or restart. ⟦C.f4 C:tb3⟧
(mechanism) Duplicates and restarted claims attach or resume the persisted job. Reconcile unknown launch responses with that same token, not a second logical launch. ⟦C.f5 C:tb3⟧
(mechanism) For a busy slot held by a different run key, defer or reject under the supplied policy without launching an overlapping job. ⟦C.f6 C:tb3⟧
(mechanism) Release the active pipeline slot only after confirmed terminal job state, retaining the completed run-key record so a later duplicate cannot relaunch it. ⟦C.f7 C:tb4⟧
(mechanism) Assert durable state and logical job count for concurrent same-event workers, different-key slot contenders, and fresh workers after both reservation and launch. ⟦C.f8 C:tb4⟧
(mechanism) In existing Cloud Build YAML/JSON steps, name specifies the execution image; args or script specifies the command. Wire the function/test entry into its assigned stage. ⟦C.f9 C:tb4⟧
(misconception) A process-local dictionary or separate check-then-write calls cannot supply the durable atomic admission contract. A retry must not invent a new job identity, and releasing an active slot before terminal confirmation permits the wrong overlap. ⟦C.f1 C.f10 C.f11 C.f12 C.f13 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C.f8 C.f9 C:tb2 C:tb3 C:tb4 C:tb5 C:tb6⟧
### r07 · Revisit: Gate a retrained candidate against the incumbent using validation evidence before controlled promotion
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦D.f8 D:tb4⟧
(misconception) An assertion for a valid case is not enough. Test declared boundary and failure predicates too; a false assert raises AssertionError in ordinary non-optimized execution. ⟦D.f8 D:tb4⟧
### r08 · Revisit: Gate a retrained candidate against the incumbent using validation evidence before controlled promotion
(mechanism) Evaluate the retrained candidate and incumbent on the same declared validation cohort and compare them against the predeclared acceptance requirements. ⟦D.f1 D:tb2⟧
(mechanism) Use the supplied deployment class probabilities and error costs to calculate candidate and incumbent expected cost under the fixed selection rule. ⟦D.f2 D:tb2⟧
(mechanism) Reject a candidate that fails a required quality, slice or deployment-compatibility gate even if its aggregate validation score improves. ⟦D.f3 D:tb2⟧
(mechanism) Bind the candidate’s exact registry/artifact identity and gate verdict to the controlled promotion record; validation of one artifact does not approve a different artifact. ⟦D.f4 D:tb3⟧
(mechanism) For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate. ⟦D.f5 D:tb3⟧
(mechanism) With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦D.f6 D:tb3⟧
(mechanism) Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system. ⟦D.f7 D:tb4⟧
(mechanism) Write assert predicate checks for the declared valid, boundary and failure cases; a false predicate raises AssertionError during ordinary non-optimized execution. ⟦D.f8 D:tb4⟧
(misconception) Retrained does not mean accepted. An aggregate gain cannot bypass a required slice or compatibility gate, and validation of one artifact does not approve another. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D.f8 D:tb2 D:tb3 D:tb4⟧

=========

# EVALUATOR PACKET — Runbook-scoped service recovery (mle.tile.090_090)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.ml_incident_runbook — Use an ML incident runbook for safe recovery on an existing platform

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: remediation step mle.tile.090_090.r02 is never referenced
  warn: mle.tile.090_090.s01: prose block without lineage.fact_ids
  warn: mle.tile.090_090.s05/ix.mle.tile.090_090.s05: ADVISORY — syntax descriptors with no detector: ['gcloud compute addresses delete', 'gcloud compute disks delete', 'gcloud compute instances delete']
  warn: mle.tile.090_090.s06: prose block without lineage.fact_ids

## SOURCE FACTS — A (mle.ml_incident_runbook)   objective: Recover an injected nonproduction service fault through the authorized runbook and instance lifecycle.
A.f1: Use the nonproduction runbook and authorized recovery identity; reproduce and isolate the injected service fault and test one recovery hypothesis before the lifecycle action.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/operational-excellence/manage-incidents-and-problems — Manage incidents and problems]
A.f2: Inspect instance status/identity and process/service state, recording fault evidence before recovery.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/describe — DESCRIPTION; EXAMPLES]
A.f3: Perform the runbook-approved gcloud compute instances stop INSTANCE --zone=ZONE, wait for completion, then start the same authorized instance and wait until it is running.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/instances/stop-start-instance — Stop an instance; Start an instance]
A.f4: Reconnect with gcloud compute ssh INSTANCE --zone=ZONE and inspect the restored process/model service state.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/connect/standard-ssh — Connect to VMs]
A.f5: Verify model readiness and a bounded prediction exchange after restart, comparing the restored service behavior with the expected contract.   [sources: python_tutorial#../library/urllib.request.html — Request; urlopen]
A.f6: Use existing runtime-injected credentials without embedding them in recovery code/configuration or printing them in captured output.   [sources: docker_docs#https://docs.docker.com/reference/compose-file/secrets/ — secrets]
A.f7: Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/describe — DESCRIPTION; EXAMPLES]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Use an ML Incident Runbook.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.deployment_verification, mle.service_telemetry. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Recover one supplied nonproduction model-service instance under its runbook. Confirm target identity and lifecycle state, inspect process/service state, record and isolate the injected fault, and test one supported recovery hypothesis. Using the authorized recovery identity and existing runtime-injected credentials, perform the approved stop/start sequence, reconnect, and verify lifecycle state, model readiness and a bounded prediction exchange.  SUCCESS: The recovery record identifies the authorized nonproduction target, preserves pre-action fault evidence and the hypothesis-test result, and shows stop completion before start. Post-action evidence confirms the same instance is running, the restored service is ready and a bounded prediction exchange meets the supplied contract. No credentials appear in code, configuration or captured output, and no production or unrelated resources are acted on.
ASSESSMENT ANCHOR: establish_authorized_target_and_record_fault_evidence facts=['f1', 'f2', 'f6', 'f7']
ASSESSMENT ANCHOR: execute_runbook_approved_stop_start_after_hypothesis_test facts=['f1', 'f3', 'f6']
ASSESSMENT ANCHOR: verify_instance_and_model_service_recovery facts=['f4', 'f5', 'f7']

## DATA ASSETS USED
ds.incident_evidence: Incident Evidence — columns: phase(categorical), INSTANCE(identifier), ZONE(identifier), authorized_identity(identifier), instance_state(categorical), process_state(categorical), readiness(categorical), prediction_contract_pass(categorical), fault_evidence(text), hypothesis_result(text), credential_review_pass(categorical)
   ["before","serving-lab","lab-zone-a","lab.operator","RUNNING","failed",false,false,"model-service exited; endpoint unavailable","runbook-approved service fault reproduced",true]
   ["after","serving-lab","lab-zone-a","lab.operator","RUNNING","running",true,true,"service reconnected after same-instance stop/start","bounded readiness/prediction checks pass",true]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute training and inference expenditure to workloads; Remove model-serving resources safely on an existing platform; Set an ML workload cost guardrail on an existing platform; Track ML workload compute and memory utilization

## LESSON, in learner order

### s01 · explainer · Use an ML incident runbook for safe recovery on an existing platform
(intro) Recovery is scoped to one authorized nonproduction instance. Reproduce and isolate the injected service fault, then test the supported hypothesis before the lifecycle action. ⟦A:tb1⟧
(mechanism) Use the nonproduction runbook and authorized recovery identity; reproduce and isolate the injected service fault and test one recovery hypothesis before the lifecycle action. Inspect instance status/identity and process/service state, recording fault evidence before recovery. Perform the runbook-approved gcloud compute instances stop INSTANCE --zone=ZONE, wait for completion, then start the same authorized instance and wait until it is running. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Reconnect with gcloud compute ssh INSTANCE --zone=ZONE and inspect the restored process/model service state. Verify model readiness and a bounded prediction exchange after restart, comparing the restored service behavior with the expected contract. Use existing runtime-injected credentials without embedding them in recovery code/configuration or printing them in captured output. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(mechanism) Inspect with gcloud compute instances describe INSTANCE --zone=ZONE: the instance status and identity before and after the authorized lifecycle action. ⟦A.f7 A:tb4⟧
[BEFORE_AFTER] The same authorized instance needs process, readiness and prediction verification—not merely RUNNING.
  before:
[TABLE computed result ] caption: Expected simulator state before recovery; no learner execution is claimed.
  produced by sql: SELECT * FROM evidence WHERE phase='before'
  result columns=['phase', 'INSTANCE', 'ZONE', 'authorized_identity', 'instance_state', 'process_state', 'readiness', 'prediction_contract_pass', 'fault_evidence', 'hypothesis_result', 'credential_review_pass'] rows(1)=[["before","serving-lab","lab-zone-a","lab.operator","RUNNING","failed",false,false,"model-service exited; endpoint unavailable","runbook-approved service fault reproduced",true]]
  after:
[TABLE computed result ] caption: Expected simulator state after same-instance recovery and service verification.
  produced by sql: SELECT * FROM evidence WHERE phase='after'
  result columns=['phase', 'INSTANCE', 'ZONE', 'authorized_identity', 'instance_state', 'process_state', 'readiness', 'prediction_contract_pass', 'fault_evidence', 'hypothesis_result', 'credential_review_pass'] rows(1)=[["after","serving-lab","lab-zone-a","lab.operator","RUNNING","running",true,true,"service reconnected after same-instance stop/start","bounded readiness/prediction checks pass",true]]

### s02 · explainer · Apply the rule: Use an ML incident runbook for safe recovery on an existing platform
(example) Retain instance, process and fault evidence before action. Test the runbook hypothesis, then stop and start the same authorized instance, waiting for each lifecycle transition. Reconnect and inspect the model service. Check readiness and a bounded prediction exchange against the contract; a running VM is not sufficient. Describe identity/state before and after. Keep runtime credentials out of commands, configuration and captured output. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb5⟧

### s03 · explainer · Work the contrast: Use an ML incident runbook for safe recovery on an existing platform
(misconception) Restarting a VM is not proof that model service behavior recovered. The authorized target, fault evidence and post-restart readiness/prediction checks all belong in the recovery verdict. ⟦A.f1 A.f2 A.f5 A:tb6⟧

### s04 · check · Review use an ml incident runbook for safe recovery on an existing platform
Check the distinction — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [choice, intro, grading=client] The same authorized instance is RUNNING after stop/start. Which evidence is still required to verify model-service recovery?
  ✔ o1: Reconnect, inspect the restored service, verify readiness and bounded prediction, and retain before/after identity descriptions
      why: Lifecycle state alone is not model readiness or a successful prediction exchange.
  ✘ o2: Treat RUNNING as proof that the prediction contract passes
      why: The supplied service checks must verify restored model behavior separately.
  ✘ o3: Delete the instance now that restart finished
      why: Deletion is outside this recovery runbook and does not verify model-service recovery.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Separate instance lifecycle status from model-service behavior.']  remediation→r01
  MEASURES: A:verify_instance_and_model_service_recovery(f4,f5,f7)   anchors=[]
  taught-before-tested: A.f4←s01; A.f5←s01; A.f7←s01

### s05 · hands_on · Apply use an ml incident runbook for safe recovery on an existing platform
Practice — Complete the learner-defined function and required imports under the supplied policy; use the declared cases to verify the single deliverable.
QUESTION [code_exercise, stretch, grading=client] Practice — Complete the symbolic action sequence under the supplied runbook and inspect the simulator’s recovery checks.

Complete action0 through action9 using the supplied symbolic command names. Order inspection, fault reproduction, hypothesis testing, stop completion, start completion, reconnection, readiness and bounded prediction according to the declared runbook. Keep the simulator and output checks unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy']} constraints.allowed=['gcloud compute instances describe INSTANCE --zone=ZONE', 'gcloud compute instances stop INSTANCE --zone=ZONE', 'gcloud compute instances start INSTANCE --zone=ZONE', 'gcloud compute ssh INSTANCE --zone=ZONE'] blocked=3 items
  file learner.py [editable]:
exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"INSTANCE": "serving-lab", "ZONE": "lab-zone-a", "authorized_identity": "lab.operator", "prediction_contract": {"request": {"distance_category": "long_distance", "numeric_values": 5}, "response": {"predicted_class": "late"}}, "credentials": "runtime-injected only"}\')')

exec("incident_evidence_rows = list(csv.DictReader(open('incident_evidence.csv')))")

exec('incident_evidence = {}')

exec("incident_evidence['phase'] = np.array([r['phase'] for r in incident_evidence_rows])")

exec("incident_evidence['INSTANCE'] = np.array([r['INSTANCE'] for r in incident_evidence_rows])")

exec("incident_evidence['ZONE'] = np.array([r['ZONE'] for r in incident_evidence_rows])")

exec("incident_evidence['authorized_identity'] = np.array([r['authorized_identity'] for r in incident_evidence_rows])")

exec("incident_evidence['instance_state'] = np.array([r['instance_state'] for r in incident_evidence_rows])")

exec("incident_evidence['process_state'] = np.array([r['process_state'] for r in incident_evidence_rows])")

exec("incident_evidence['readiness'] = np.array([r['readiness'] == 'True' for r in incident_evidence_rows])")

exec("incident_evidence['prediction_contract_pass'] = np.array([r['prediction_contract_pass'] == 'True' for r in incident_evidence_rows])")

exec("incident_evidence['fault_evidence'] = np.array([r['fault_evidence'] for r in incident_evidence_rows])")

exec("incident_evidence['hypothesis_result'] = np.array([r['hypothesis_result'] for r in incident_evidence_rows])")

exec("incident_evidence['credential_review_pass'] = np.array([r['credential_review_pass'] == 'True' for r in incident_evidence_rows])")

exec("hypothesis_command = 'test_hypothesis'")

exec("inspect_command = 'inspect'")

exec("prediction_command = 'bounded_prediction'")

exec("readiness_command = 'readiness'")

exec("reconnect_command = 'reconnect'")

exec("reproduce_command = 'reproduce_fault'")

exec("start_command = 'start'")

exec("stop_command = 'stop'")

exec("wait_running_command = 'wait_running'")

exec("wait_stopped_command = 'wait_stopped'")

exec("SUCCESSFUL_HYPOTHESIS = 'runbook-approved service fault reproduced'")

# Supplied callable: recover(actions=None, evidence_rows=None, stop_complete=True).
# Returns recovery evidence on success; status/failure-check evidence otherwise.
# Load the supplied readonly simulator callable into the runtime.
exec("import base64, zlib\nexec(zlib.decompress(base64.b64decode('eJytVktv3DYQvudX0CfuAirQXGXoEDibxkC7NrzrQ7MQBEbixkxlUqUou5vA/z0zJPWiuC4adC9aDsnhN988K34kmpfqiesVK41Qss22SvKE8CdRcVnyQqvnXtYa1RSlemxqbni21x1fp28I/Pg/DS8Nr4qW/93hLZKRAxWyRTFNCNW80arqQN2RdbUVGd6a4uHUKPPAW9GiCPXj95kJU+Ci4ZWTM22GDd1JKeQXp7ZUUg5vsEpI3lpVn1UnKwDUaF4JaxjNLVRxJN5QIlqCdqWDIFsaYu9YCoQskRFTzJhBfYHAaSW8bvl8y+r6zI9K8wzXh1/zS8KOhmu3fOsQgrXA7nekzzC8awU0dTcPoTxPKHBbgt3hwbk4f3HauxKFx66ekJ99YID2knjO++VA71TEqlO/GMktGtZ6LfaVCuLqyES9Kh94+dc6hXum05J8R1+arqUpxe1Oc5rYf0C5PUpT+0motwX1r+z/9cug2ejOPKyeWI0B2Ku2S2Qf45Io7QVZRihKqL0NxKA3iZDk4GhKrANyF8c+QODEgV5vd/t326sNzS+yRtWiPE1lxCk60E8329kRtx62GSBVWnwD+2z0CHOano5uj1hs8DnzLJvT8y175AUkxhdu6HqKXirjGbIISnASamZ1oSEc+bP1Fc1H5pzqxTmvdZIwF5EEiblWSOBejGfAx14FTf2fl8EdToAe8VszVzhZlg3FZE4OnLDBscyKi4ze3W+319vfaGCokMJa6Q6O1PF6+l5YsRbvIs19ptkjQ2Fw7ve4giQEWC7cQ1RORf+qLVjnoIWVcw4tmuBQ2nqsoxBea9G0HJNkd391tdntPtz/Xnz88/Zm/3Gzu97FbI7qD4yZgDtnhK31UVJ/+oGheC6jIaO7/c3tLUbDGTyznhPHNe1+AZ7p3tx1r4Lab+7+uN6+22/e07H4YrU6Sxo2wrPo4PYk8iIZMXnv/zEAyuHd/t9Y7Rv2Arctvf8ldb2molGtCdP3VZy9vrPJ3s8RP1FekHJvyTLZB9sDQyCFIRtxPrE34nYE6rL4K/M+/Ur0jANS2GGwp0+UECYr30L8k+PVfB2LPqtiYWN/51wNiAxpc2ThgGGfWaKbHAMbjIYH+iYXAxtoDWBHQA2NEG+v+kxDGCFpI8DgkbDbwjTpK0nh5++Tf2Zop763p8vhI6HfYMIcd9zMkdBhhEhfnS8S6npBPykmYf9Kz/W1ZNo9sA2NRyNtZdn1QYIegzV+Etp7awQccSUqGocTnC8gqYx45L8I+dVRr2R9uiQla4A6WPaAiRtkoKC/vPkBlCJSXQ==')), globals())")

# LEARNER EDIT: complete this line; leave surrounding scaffolding unchanged.
action0 = None

# LEARNER EDIT: complete this line; leave surrounding scaffolding unchanged.
action1 = None

# LEARNER EDIT: complete this line; leave surrounding scaffolding unchanged.
action2 = None

# LEARNER EDIT: complete this line; leave surrounding scaffolding unchanged.
action3 = None

# LEARNER EDIT: complete this line; leave surrounding scaffolding unchanged.
action4 = None

# LEARNER EDIT: complete this line; leave surrounding scaffolding unchanged.
action5 = None

# LEARNER EDIT: complete this line; leave surrounding scaffolding unchanged.
action6 = None

# LEARNER EDIT: complete this line; leave surrounding scaffolding unchanged.
action7 = None

# LEARNER EDIT: complete this line; leave surrounding scaffolding unchanged.
action8 = None

# LEARNER EDIT: complete this line; leave surrounding scaffolding unchanged.
action9 = None

result = recover([action0,action1,action2,action3,action4,action5,action6,action7,action8,action9])

exec("failed_hypothesis_rows=[dict(incident_evidence_rows[0],hypothesis_result='failed'),dict(incident_evidence_rows[1])]")

exec('failed_service_rows=[dict(incident_evidence_rows[0]),dict(incident_evidence_rows[1],prediction_contract_pass=False)]')

exec('failed_readiness_rows=[dict(incident_evidence_rows[0]),dict(incident_evidence_rows[1],readiness=False)]')

exec('failure_records=[recover(None,failed_hypothesis_rows),recover(None,stop_complete=False),recover(None,failed_service_rows),recover(None,failed_readiness_rows)]')

  file runbook_simulator.py [readonly]:
def recover(actions=None, evidence_rows=None, stop_complete=True):
    expected_sequence = ['inspect', 'reproduce_fault', 'test_hypothesis', 'stop', 'wait_stopped', 'start', 'wait_running', 'reconnect', 'readiness', 'bounded_prediction']
    if actions is None: actions = expected_sequence
    rows=incident_evidence_rows if evidence_rows is None else evidence_rows
    before=rows[0]; after=rows[1]
    state={'instance_state':before['instance_state'],'process_state':before['process_state']}
    successful_hypothesis=False; stopped=False; reconnected=False; ready=False; prediction_pass=False
    def fail(check): return {'status':'failure','failed_check':check,'state':dict(state)}
    def truth(value): return value is True or value == 'True'
    for row in [before,after]:
        if row['INSTANCE']!=policy['INSTANCE'] or row['ZONE']!=policy['ZONE'] or row['authorized_identity']!=policy['authorized_identity']:
            return fail('authorized_same_target')
        if not truth(row['credential_review_pass']): return fail('credential_review')
    if actions != expected_sequence: return {'status':'invalid_sequence','actions':actions}
    for action in actions:
        if action=='inspect':
            if state['instance_state']!='RUNNING': return fail('initial_state')
        elif action=='reproduce_fault':
            if not before['fault_evidence'] or state['process_state']!='failed': return fail('fault_reproduction')
        elif action=='test_hypothesis':
            successful_hypothesis = before['hypothesis_result'] == SUCCESSFUL_HYPOTHESIS
            if not successful_hypothesis: return fail('hypothesis')
        elif action=='stop':
            if not successful_hypothesis: return fail('hypothesis')
            state['instance_state']='STOPPING'
        elif action=='wait_stopped':
            if not stop_complete: return fail('stop_completion')
            state['instance_state']='TERMINATED'; stopped=True
        elif action=='start':
            if not stopped or state['instance_state']!='TERMINATED': return fail('stop_completion')
            state['instance_state']='STARTING'
        elif action=='wait_running':
            if after['instance_state']!='RUNNING': return fail('running_poststate')
            state['instance_state']='RUNNING'
        elif action=='reconnect':
            if state['instance_state']!='RUNNING' or after['process_state']!='running': return fail('restored_process')
            state['process_state']=after['process_state']; reconnected=True
        elif action=='readiness':
            ready=reconnected and truth(after['readiness'])
            if not ready: return fail('readiness')
        elif action=='bounded_prediction':
            prediction_pass=ready and truth(after['prediction_contract_pass'])
            if not prediction_pass: return fail('bounded_prediction')
    if not (stopped and reconnected and ready and prediction_pass): return fail('incomplete_recovery')
    return {'target':policy['INSTANCE'],'zone':policy['ZONE'],'identity':policy['authorized_identity'],'before':before,'fault_evidence':before['fault_evidence'],'hypothesis_test':before['hypothesis_result'],'actions':actions,'after':after,'contract':policy['prediction_contract'],'credentials':'runtime-injected only; captured evidence reviewed'}

  SOLUTION learner.py:
exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"INSTANCE": "serving-lab", "ZONE": "lab-zone-a", "authorized_identity": "lab.operator", "prediction_contract": {"request": {"distance_category": "long_distance", "numeric_values": 5}, "response": {"predicted_class": "late"}}, "credentials": "runtime-injected only"}\')')

exec("incident_evidence_rows = list(csv.DictReader(open('incident_evidence.csv')))")

exec('incident_evidence = {}')

exec("incident_evidence['phase'] = np.array([r['phase'] for r in incident_evidence_rows])")

exec("incident_evidence['INSTANCE'] = np.array([r['INSTANCE'] for r in incident_evidence_rows])")

exec("incident_evidence['ZONE'] = np.array([r['ZONE'] for r in incident_evidence_rows])")

exec("incident_evidence['authorized_identity'] = np.array([r['authorized_identity'] for r in incident_evidence_rows])")

exec("incident_evidence['instance_state'] = np.array([r['instance_state'] for r in incident_evidence_rows])")

exec("incident_evidence['process_state'] = np.array([r['process_state'] for r in incident_evidence_rows])")

exec("incident_evidence['readiness'] = np.array([r['readiness'] == 'True' for r in incident_evidence_rows])")

exec("incident_evidence['prediction_contract_pass'] = np.array([r['prediction_contract_pass'] == 'True' for r in incident_evidence_rows])")

exec("incident_evidence['fault_evidence'] = np.array([r['fault_evidence'] for r in incident_evidence_rows])")

exec("incident_evidence['hypothesis_result'] = np.array([r['hypothesis_result'] for r in incident_evidence_rows])")

exec("incident_evidence['credential_review_pass'] = np.array([r['credential_review_pass'] == 'True' for r in incident_evidence_rows])")

exec("hypothesis_command = 'test_hypothesis'")

exec("inspect_command = 'inspect'")

exec("prediction_command = 'bounded_prediction'")

exec("readiness_command = 'readiness'")

exec("reconnect_command = 'reconnect'")

exec("reproduce_command = 'reproduce_fault'")

exec("start_command = 'start'")

exec("stop_command = 'stop'")

exec("wait_running_command = 'wait_running'")

exec("wait_stopped_command = 'wait_stopped'")

exec("SUCCESSFUL_HYPOTHESIS = 'runbook-approved service fault reproduced'")

# Supplied callable: recover(actions=None, evidence_rows=None, stop_complete=True).
# Returns recovery evidence on success; status/failure-check evidence otherwise.
# Load the supplied readonly simulator callable into the runtime.
exec("import base64, zlib\nexec(zlib.decompress(base64.b64decode('eJytVktv3DYQvudX0CfuAirQXGXoEDibxkC7NrzrQ7MQBEbixkxlUqUou5vA/z0zJPWiuC4adC9aDsnhN988K34kmpfqiesVK41Qss22SvKE8CdRcVnyQqvnXtYa1RSlemxqbni21x1fp28I/Pg/DS8Nr4qW/93hLZKRAxWyRTFNCNW80arqQN2RdbUVGd6a4uHUKPPAW9GiCPXj95kJU+Ci4ZWTM22GDd1JKeQXp7ZUUg5vsEpI3lpVn1UnKwDUaF4JaxjNLVRxJN5QIlqCdqWDIFsaYu9YCoQskRFTzJhBfYHAaSW8bvl8y+r6zI9K8wzXh1/zS8KOhmu3fOsQgrXA7nekzzC8awU0dTcPoTxPKHBbgt3hwbk4f3HauxKFx66ekJ99YID2knjO++VA71TEqlO/GMktGtZ6LfaVCuLqyES9Kh94+dc6hXum05J8R1+arqUpxe1Oc5rYf0C5PUpT+0motwX1r+z/9cug2ejOPKyeWI0B2Ku2S2Qf45Io7QVZRihKqL0NxKA3iZDk4GhKrANyF8c+QODEgV5vd/t326sNzS+yRtWiPE1lxCk60E8329kRtx62GSBVWnwD+2z0CHOano5uj1hs8DnzLJvT8y175AUkxhdu6HqKXirjGbIISnASamZ1oSEc+bP1Fc1H5pzqxTmvdZIwF5EEiblWSOBejGfAx14FTf2fl8EdToAe8VszVzhZlg3FZE4OnLDBscyKi4ze3W+319vfaGCokMJa6Q6O1PF6+l5YsRbvIs19ptkjQ2Fw7ve4giQEWC7cQ1RORf+qLVjnoIWVcw4tmuBQ2nqsoxBea9G0HJNkd391tdntPtz/Xnz88/Zm/3Gzu97FbI7qD4yZgDtnhK31UVJ/+oGheC6jIaO7/c3tLUbDGTyznhPHNe1+AZ7p3tx1r4Lab+7+uN6+22/e07H4YrU6Sxo2wrPo4PYk8iIZMXnv/zEAyuHd/t9Y7Rv2Arctvf8ldb2molGtCdP3VZy9vrPJ3s8RP1FekHJvyTLZB9sDQyCFIRtxPrE34nYE6rL4K/M+/Ur0jANS2GGwp0+UECYr30L8k+PVfB2LPqtiYWN/51wNiAxpc2ThgGGfWaKbHAMbjIYH+iYXAxtoDWBHQA2NEG+v+kxDGCFpI8DgkbDbwjTpK0nh5++Tf2Zop763p8vhI6HfYMIcd9zMkdBhhEhfnS8S6npBPykmYf9Kz/W1ZNo9sA2NRyNtZdn1QYIegzV+Etp7awQccSUqGocTnC8gqYx45L8I+dVRr2R9uiQla4A6WPaAiRtkoKC/vPkBlCJSXQ==')), globals())")

action0 = inspect_command

action1 = reproduce_command

action2 = hypothesis_command

action3 = stop_command

action4 = wait_stopped_command

action5 = start_command

action6 = wait_running_command

action7 = reconnect_command

action8 = readiness_command

action9 = prediction_command

result = recover([action0,action1,action2,action3,action4,action5,action6,action7,action8,action9])

exec("failed_hypothesis_rows=[dict(incident_evidence_rows[0],hypothesis_result='failed'),dict(incident_evidence_rows[1])]")

exec('failed_service_rows=[dict(incident_evidence_rows[0]),dict(incident_evidence_rows[1],prediction_contract_pass=False)]')

exec('failed_readiness_rows=[dict(incident_evidence_rows[0]),dict(incident_evidence_rows[1],readiness=False)]')

exec('failure_records=[recover(None,failed_hypothesis_rows),recover(None,stop_complete=False),recover(None,failed_service_rows),recover(None,failed_readiness_rows)]')

  SOLUTION runbook_simulator.py:
def recover(actions=None, evidence_rows=None, stop_complete=True):
    expected_sequence = ['inspect', 'reproduce_fault', 'test_hypothesis', 'stop', 'wait_stopped', 'start', 'wait_running', 'reconnect', 'readiness', 'bounded_prediction']
    if actions is None: actions = expected_sequence
    rows=incident_evidence_rows if evidence_rows is None else evidence_rows
    before=rows[0]; after=rows[1]
    state={'instance_state':before['instance_state'],'process_state':before['process_state']}
    successful_hypothesis=False; stopped=False; reconnected=False; ready=False; prediction_pass=False
    def fail(check): return {'status':'failure','failed_check':check,'state':dict(state)}
    def truth(value): return value is True or value == 'True'
    for row in [before,after]:
        if row['INSTANCE']!=policy['INSTANCE'] or row['ZONE']!=policy['ZONE'] or row['authorized_identity']!=policy['authorized_identity']:
            return fail('authorized_same_target')
        if not truth(row['credential_review_pass']): return fail('credential_review')
    if actions != expected_sequence: return {'status':'invalid_sequence','actions':actions}
    for action in actions:
        if action=='inspect':
            if state['instance_state']!='RUNNING': return fail('initial_state')
        elif action=='reproduce_fault':
            if not before['fault_evidence'] or state['process_state']!='failed': return fail('fault_reproduction')
        elif action=='test_hypothesis':
            successful_hypothesis = before['hypothesis_result'] == SUCCESSFUL_HYPOTHESIS
            if not successful_hypothesis: return fail('hypothesis')
        elif action=='stop':
            if not successful_hypothesis: return fail('hypothesis')
            state['instance_state']='STOPPING'
        elif action=='wait_stopped':
            if not stop_complete: return fail('stop_completion')
            state['instance_state']='TERMINATED'; stopped=True
        elif action=='start':
            if not stopped or state['instance_state']!='TERMINATED': return fail('stop_completion')
            state['instance_state']='STARTING'
        elif action=='wait_running':
            if after['instance_state']!='RUNNING': return fail('running_poststate')
            state['instance_state']='RUNNING'
        elif action=='reconnect':
            if state['instance_state']!='RUNNING' or after['process_state']!='running': return fail('restored_process')
            state['process_state']=after['process_state']; reconnected=True
        elif action=='readiness':
            ready=reconnected and truth(after['readiness'])
            if not ready: return fail('readiness')
        elif action=='bounded_prediction':
            prediction_pass=ready and truth(after['prediction_contract_pass'])
            if not prediction_pass: return fail('bounded_prediction')
    if not (stopped and reconnected and ready and prediction_pass): return fail('incomplete_recovery')
    return {'target':policy['INSTANCE'],'zone':policy['ZONE'],'identity':policy['authorized_identity'],'before':before,'fault_evidence':before['fault_evidence'],'hypothesis_test':before['hypothesis_result'],'actions':actions,'after':after,'contract':policy['prediction_contract'],'credentials':'runtime-injected only; captured evidence reviewed'}

  test t1 (value_equals, visible=True): {"expr":"result","expected":{"target":"serving-lab","zone":"lab-zone-a","identity":"lab.operator","before":{"phase":"before","INSTANCE":"serving-lab","ZONE":"lab-zone-a","authorized_identity":"lab.operator","instance_state":"RUNNING","process_state":"failed","readiness":"False","prediction_contract_pass":"False","fault_evidence":"model-service exited; endpoint unavailable","hypothesis_result":"runbook-approved service fault reproduced","credential_review_pass":"True"},"fault_evidence":"model-ser | on-fail: The returned record or calculation does not match the declared fixture contract.
  test failed_recovery_checks (value_equals, visible=True): {"expr":"[r.get('failed_check') for r in failure_records] == ['hypothesis','stop_completion','bounded_prediction','readiness']","expected":true} | on-fail: The returned record or calculation does not match the declared fixture contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"911a1ffa91e89c71fa2ae899a5f67d0a1d49638145b62c1bc9ea8fedba568360","tests_passed":2}
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Order action0 through action9 by the runbook’s hypothesis, stop-completion, reconnect, readiness and bounded-prediction prerequisites.']
  MEASURES: A:establish_authorized_target_and_record_fault_evidence(f1,f2,f6,f7); A:execute_runbook_approved_stop_start_after_hypothesis_test(f1,f3,f6); A:verify_instance_and_model_service_recovery(f4,f5,f7)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f6←s01; A.f7←s01; A.f1←s01; A.f3←s01; A.f6←s01; A.f4←s01; A.f5←s01; A.f7←s01

### s06 · recap · Keep these distinctions
(takeaway) Use only the authorized nonproduction recovery identity. Retain fault evidence and test the hypothesis before the same-instance stop/start sequence. Verify restored model readiness and bounded prediction behavior, with runtime credentials kept out of captured output.
[UP NEXT] Track ML workload compute and memory utilization: Define the ML workload interval before summarizing telemetry. Stopped intervals or unrelated processes must not silently enter an active-workload summary.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Use an ML incident runbook for safe recovery on an existing platform
(mechanism) Reconnect with gcloud compute ssh INSTANCE --zone=ZONE and inspect the restored process/model service state. ⟦A.f4 A:tb3⟧
(mechanism) Verify model readiness and a bounded prediction exchange after restart, comparing the restored service behavior with the expected contract. ⟦A.f5 A:tb3⟧
(mechanism) Inspect identity/status before and after authorized lifecycle action with gcloud compute instances describe INSTANCE --zone=ZONE. ⟦A.f7 A:tb4⟧
(misconception) A RUNNING instance is not a recovered model service. Describe identity/state, reconnect, and verify restored readiness and a bounded prediction against the expected contract. ⟦A.f4 A.f5 A.f7 A:tb3 A:tb4⟧
### r02 · Revisit: Use an ML incident runbook for safe recovery on an existing platform
(mechanism) Use the nonproduction runbook and authorized recovery identity; reproduce and isolate the injected service fault and test one recovery hypothesis before the lifecycle action. ⟦A.f1 A:tb2⟧
(mechanism) Inspect instance status/identity and process/service state, recording fault evidence before recovery. ⟦A.f2 A:tb2⟧
(mechanism) Perform the runbook-approved gcloud compute instances stop INSTANCE --zone=ZONE, wait for completion, then start the same authorized instance and wait until it is running. ⟦A.f3 A:tb2⟧
(mechanism) Reconnect with gcloud compute ssh INSTANCE --zone=ZONE and inspect the restored process/model service state. ⟦A.f4 A:tb3⟧
(mechanism) Verify model readiness and a bounded prediction exchange after restart, comparing the restored service behavior with the expected contract. ⟦A.f5 A:tb3⟧
(mechanism) Use existing runtime-injected credentials without embedding them in recovery code/configuration or printing them in captured output. ⟦A.f6 A:tb3⟧
(mechanism) Inspect identity/status before and after authorized lifecycle action with gcloud compute instances describe INSTANCE --zone=ZONE. ⟦A.f7 A:tb4⟧
(misconception) Restarting a VM is not proof that model service behavior recovered. The authorized target, fault evidence and post-restart readiness/prediction checks all belong in the recovery verdict. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb2 A:tb3 A:tb4⟧

=========

# EVALUATOR PACKET — Workload utilization, costs and safe cleanup (mle.tile.091_094)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.ml_resource_utilization — Track ML workload compute and memory utilization
B = mle.ml_workload_cost_attribution — Attribute training and inference expenditure to workloads
C = mle.ml_workload_cost_guardrail — Set an ML workload cost guardrail on an existing platform
D = mle.serving_resource_cleanup — Remove model-serving resources safely on an existing platform

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=12
  warn: remediation step mle.tile.091_094.r02 is never referenced
  warn: remediation step mle.tile.091_094.r04 is never referenced
  warn: remediation step mle.tile.091_094.r06 is never referenced
  warn: remediation step mle.tile.091_094.r08 is never referenced
  warn: mle.tile.091_094.s01: prose block without lineage.fact_ids
  warn: mle.tile.091_094.s04/ix.mle.tile.091_094.s04: ADVISORY — syntax descriptors with no detector: ['Boolean array masks', 'array and dictionary indexing', 'docker rm', 'gcloud billing budgets create', 'gcloud compute instances delete', 'list and dictionary literals', 'numeric literals', 'string literals']
  warn: mle.tile.091_094.s05: prose block without lineage.fact_ids
  warn: mle.tile.091_094.s09/ix.mle.tile.091_094.s09: ADVISORY — syntax descriptors with no detector: ['Arithmetic operators', 'For loops and conditional comparisons', 'Indexing', 'Lists and dictionaries', 'Numeric and string literals', 'Variable assignment', 'gcloud billing budgets create', 'gcloud billing budgets update', 'gcloud compute disks delete', 'gcloud compute instances delete']
  warn: mle.tile.091_094.s10: prose block without lineage.fact_ids
  warn: mle.tile.091_094.s14/ix.mle.tile.091_094.s14: ADVISORY — syntax descriptors with no detector: ['Literal credentials in configuration or command arguments', 'Python dictionary and list literals', 'String and numeric literals', 'Supplied event-response YAML fields for budget scope, amount, reporting period, thresholds, existing Pub/Sub topic, event binding and fixed target', 'Supplied runtime Secret Manager references and secretEnv configuration', 'Variable assignment', 'Wildcard or dynamically enumerated resource targets', 'YAML tags that construct arbitrary Python objects', 'gcloud compute instance-groups managed delete', 'gcloud compute instances delete']
  warn: mle.tile.091_094.s15: prose block without lineage.fact_ids
  warn: mle.tile.091_094.s20: prose block without lineage.fact_ids

## SOURCE FACTS — A (mle.ml_resource_utilization)   objective: Summarize CPU/memory utilization for the correctly matched instance, process and workload window.
A.f1: Summarize CPU/memory telemetry over the defined ML workload window, retaining instance and process identity.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/operational-excellence/manage-and-optimize-cloud-resources — Manage and optimize cloud resources]
A.f2: Align resource measurements with instance start/stop states so stopped or unrelated intervals are not silently combined with active-workload utilization.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/instances/instance-lifecycle — Instance states; Billing]
A.f3: Resolve process-state evidence against the running workload; for a containerized process, docker top shows running process state to compare with that evidence.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/top/ — Description]
A.f4: Compute descriptive CPU and memory utilization for the same matched workload interval and report observation count and units.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/operational-excellence/manage-and-optimize-cloud-resources — Manage and optimize cloud resources]
A.f5: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
A.f6: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
A.f7: Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/describe — DESCRIPTION; EXAMPLES]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Control Workload Cost and Retire Resources.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: none within this path. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Summarize supplied instance-level and process-level CPU and memory telemetry for one defined ML workload window. Match observations to instance lifecycle records and running-process evidence, then calculate each resource's observation count, mean and standard deviation with units.  SUCCESS: The summary retains the instance and process identity and selected interval, excludes stopped or unrelated observations, and uses the same matched workload interval for CPU and memory. It reports counts and units for both series and uses ddof=0. The selected CPU observations of 20, 40 and 60 percent yield a count of 3, a mean of 40 percent and a standard deviation of approximately 16.33 percentage points.
ASSESSMENT ANCHOR: identify_workload_matched_resource_observations facts=['f1', 'f2', 'f3', 'f7']
ASSESSMENT ANCHOR: calculate_descriptive_cpu_and_memory_utilization facts=['f4', 'f5', 'f6']
ASSESSMENT ANCHOR: identify_underused_or_saturated_workload_resources facts=['f1', 'f2', 'f3', 'f4', 'f5', 'f6']

## SOURCE FACTS — B (mle.ml_workload_cost_attribution)   objective: Attribute direct and shared workload charges to verified lifecycle intervals and reconcile totals.
B.f1: Billing reports associate charges with services, resources and time intervals; select the declared training/inference workload and reporting window before comparing expenditure.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/billing/docs/how-to/reports — View your billing reports and cost trends]
B.f2: Use the existing workload labels or resource-to-workload mapping to connect billed resource usage with the run or serving workload.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/framework/operational-excellence/manage-and-optimize-cloud-resources — Manage and optimize cloud resources]
B.f3: Stopping a VM can end compute charges while persistent disks and other resources remain billable, so compute time alone does not account for all workload expenditure.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/instances/instance-lifecycle — Instance states; Billing]
B.f4: Aggregate the supplied charge records by workload and charge category and reconcile the attributed total with the eligible record total.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
B.f5: Calculate a declared unit-cost quantity from attributed expenditure divided by the corresponding completed work, retaining both the billing and work-measurement windows.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/billing/docs/how-to/reports — View your billing reports and cost trends]
B.f6: Start and connect to both tagged instances for their bounded training/inference workloads, record their separate lifecycle windows, and stop both after execution.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/instances/stop-start-instance — Stop an instance; Start an instance]
B.f7: Allocate direct billing rows to the matching tagged workload/lifecycle interval and shared rows under the supplied explicit sharing rule, retaining shared charges instead of dropping them.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/billing/docs/how-to/reports — View your billing reports and cost trends]
B.f8: Sum allocations per window, flag unusually large or unmatched allocations, and check that all allocated plus explicitly unallocated amounts reconcile to the eligible billing-export total.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
B.f9: For an authorized supplied Compute Engine VM, gcloud compute instances start INSTANCE --zone=ZONE and gcloud compute instances stop INSTANCE --zone=ZONE change its lifecycle state; wait for the operation and inspect the resulting state.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/instances/stop-start-instance — Stop an instance; Start an instance]
B.f10: Connect to the running authorized VM with gcloud compute ssh INSTANCE --zone=ZONE to execute the workload.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/connect/standard-ssh — Connect to VMs]
B.f11: Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/describe — DESCRIPTION; EXAMPLES]
B.f12: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
B.f13: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Control Workload Cost and Retire Resources.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: none within this path. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Inspect, start, and connect to both supplied authorized tagged training/inference instances. Execute their bounded workloads, record separate lifecycle windows, then stop and inspect both instances. Allocate the supplied eligible billing rows by workload and window, retaining shared charges under the supplied sharing rule. Calculate per-window totals, their arithmetic mean and standard deviation, flag unusually large or unmatched allocations, and reconcile allocated plus explicitly unallocated amounts to the export.  SUCCESS: Both instances have recorded identities, lifecycle windows, and verified stopped states after bounded execution. Direct charges match the supplied workload mapping and eligible intervals; shared charges follow the supplied rule. Per-window totals, mean, and standard deviation use the declared observations and divisor. Unusual or unmatched amounts are flagged, and allocated plus explicitly unallocated amounts equal the eligible export total.
ASSESSMENT ANCHOR: identify_workload_and_reporting_window facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_lifecycle_windows_from_total_billable_usage facts=['f3', 'f6', 'f9', 'f10', 'f11']
ASSESSMENT ANCHOR: allocate_and_reconcile_workload_charges facts=['f4', 'f7', 'f8']
ASSESSMENT ANCHOR: align_unit_cost_with_completed_work_window facts=['f5']

## SOURCE FACTS — C (mle.ml_workload_cost_guardrail)   objective: Test an existing workload budget notification and authorized safe-stop response, documenting residual exposure.
C.f1: Configure the workload-scoped budget amount, reporting period and threshold rules within the supplied existing billing platform.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/billing/docs/how-to/budgets — Set budgets and budget alerts]
C.f2: Connect the budget to the existing Pub/Sub notification topic and authorized notification path, then test receipt of the declared threshold event.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/billing/docs/how-to/budgets-programmatic-notifications — Set up programmatic budget alert notifications]
C.f3: A budget notification and a resource action are separate mechanisms; verify the supplied authorized response to the event rather than assuming an alert stops resource consumption.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/billing/docs/how-to/listen-to-notifications — Manage programmatic budget alert notifications]
C.f4: Budget notifications can lag actual usage and are not an assurance that spending cannot exceed the amount; state that residual limitation in the guardrail record.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/billing/docs/how-to/budgets — Set budgets and budget alerts]
C.f5: Test both below-threshold and breach fixtures and verify the emitted notification and permitted response under the existing policy.   [sources: python_tutorial#../reference/simple_stmts.html — The assert statement]
C.f6: In the existing event-response YAML, configure the authorized step to run the safe stop command for the explicitly approved nonproduction instance, not an unrestricted resource selector.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/build-config-file-schema — Build steps; name; args; script; serviceAccount; allowFailure; allowExitCodes]
C.f7: Bind the existing budget event to the response pipeline and parse its YAML through the existing platform; verify budget scope, threshold and fixed target instance before applying.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/automating-builds/create-pubsub-triggers — Creating a Pub/Sub trigger; Substitution variables; Filters]
C.f8: Simulate the declared breach, inspect notification/response execution and verify that gcloud compute instances stop INSTANCE --zone=ZONE acted only on the approved test instance.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/instances/stop-start-instance — Stop an instance; Start an instance]
C.f9: Apply the configuration with the approved identity and runtime Secret Manager references/secretEnv, and verify captured logs do not contain literal credentials.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/build/docs/securing-builds/use-secrets — Configuring builds to access UTF-8 secrets from Secret Manager]
C.f10: Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/describe — DESCRIPTION; EXAMPLES]
C.f11: With the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.   [sources: python_tutorial#https://pyyaml.org/wiki/PyYAMLDocumentation — Reference: safe_load; safe_dump]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Control Workload Cost and Retire Resources.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.ml_workload_cost_attribution. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Author the supplied workload budget and fixed-instance response configuration using PyYAML. Reload and inspect its scope, amount, period, threshold, existing Pub/Sub event binding and approved nonproduction target. Apply it through the existing platform with the approved identity and runtime-resolved secrets, then exercise below-threshold and breach fixtures.  SUCCESS: The reloaded configuration matches the supplied contract. The below-threshold fixture does not trigger the breach response; the breach fixture produces the declared notification and authorized stop execution. Before-and-after instance descriptions confirm the approved target's identity and stopped state, execution records show no other target was acted on, and captured logs contain no literal credentials. The guardrail record states that delayed notifications permit spending to exceed the budget.
ASSESSMENT ANCHOR: configure_and_validate_workload_budget_event_binding facts=['f1', 'f2', 'f7']
ASSESSMENT ANCHOR: distinguish_budget_notifications_from_actions_and_hard_spending_caps facts=['f3', 'f4']
ASSESSMENT ANCHOR: exercise_and_verify_fixed_target_authorized_response facts=['f5', 'f6', 'f8', 'f10']
ASSESSMENT ANCHOR: apply_configuration_with_approved_identity_and_credential_safe_runtime_references facts=['f9']
ASSESSMENT ANCHOR: safely_serialize_reload_and_inspect_response_configuration facts=['f7', 'f11']

## SOURCE FACTS — D (mle.serving_resource_cleanup)   objective: Remove only verified exclusively retired resources while preserving active service, artifacts and secret-safe records.
D.f1: Authorize cleanup against the retired-resource inventory and permitted identity scope, preserving the active release rather than selecting resources by age alone.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/blueprints/security-foundations/authentication-authorization — Authentication and authorization]
D.f2: Inspect actual container labels and compare ownership and release/version metadata with the approved active and retired inventory.   [sources: docker_docs#https://docs.docker.com/engine/manage-resources/labels/ — Label keys and values; Manage labels on objects]
D.f3: Inspect each candidate container’s identity and State.Running/exit state; inspect its logs and associated compute lifecycle before deciding it is exclusively retired.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/inspect/ — Description; Examples]
D.f4: Check captured commands and logs for secret values or sensitive data, with runtime-injected credentials kept out of cleanup code and printed output.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/logs/ — Description]
D.f5: Stop only a verified retired container with docker container stop NAME, then remove that stopped retired container with docker container rm NAME.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/container/stop/ — Description]
D.f6: Terminate only the verified exclusively retired nonproduction instance with gcloud compute instances delete INSTANCE --zone=ZONE under the approved disk-preservation policy.   [sources: google_mlops_pipelines#https://cloud.google.com/compute/docs/instances/deleting-instance — Delete an instance]
D.f7: Preserve the active release’s referenced images and required model/preprocessing artifacts; removing a retired container is not authorization to delete shared artifacts.   [sources: docker_docs#https://docs.docker.com/reference/cli/docker/image/pull/ — Pull an image by digest (immutable identifier)]
D.f8: Verify the active serving release remains healthy with a bounded readiness/prediction check, and inspect the inventory to confirm approved retired resources are absent.   [sources: python_tutorial#../library/urllib.request.html — Request; urlopen]
D.f9: Write one audit record containing verified ownership, active/retired identities, authorized actions, retained artifacts and credential non-disclosure checks.   [sources: google_mlops_pipelines#Metadata management]
D.f10: Use gcloud compute instances describe INSTANCE --zone=ZONE to inspect the instance status and identity before and after the authorized lifecycle action.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/sdk/gcloud/reference/compute/instances/describe — DESCRIPTION; EXAMPLES]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Control Workload Cost and Retire Resources.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.model_version_registration, mle.deployment_verification. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Clean one supplied nonproduction serving-resource fixture using the authorized identity and runtime-injected credentials. Reconcile actual container labels, ownership, release identity, running/exit state and logs with the approved inventory and compute lifecycle. Stop and remove only verified retired containers, and delete only the exclusively retired test instance under the supplied disk-preservation policy. Preserve the active release and required artifacts, verify health and retired-resource absence, review captured output for credential disclosure, and deliver one audit record.  SUCCESS: Only authorized, runtime-verified retired resources are removed. The active release passes the supplied bounded readiness/prediction check, its referenced images and required model/preprocessing artifacts remain available, and post-action inspection confirms the approved retired resources are absent. Cleanup code and captured output contain no secret values. One audit record documents ownership, active/retired identities, authorization, inspection evidence, actions, retained artifacts and non-disclosure checks.
ASSESSMENT ANCHOR: reconcile_cleanup_authorization_with_runtime_identity facts=['f1', 'f2', 'f3', 'f10']
ASSESSMENT ANCHOR: protect_runtime_credentials_and_review_captured_output facts=['f4']
ASSESSMENT ANCHOR: remove_only_verified_retired_resources_and_preserve_required_artifacts facts=['f5', 'f6', 'f7']
ASSESSMENT ANCHOR: verify_active_health_and_retired_resource_absence facts=['f8', 'f10']
ASSESSMENT ANCHOR: document_safe_cleanup_evidence facts=['f9']

## DATA ASSETS USED
ds.billing_export: Billing Export — columns: charge_id(identifier), reporting_window(identifier), resource_id(identifier), charge_category(categorical), amount(numerical)
   ["w1.training-lab","w1","training-lab","direct_compute",6.0]
   ["w1.inference-lab","w1","inference-lab","direct_compute",4.0]
   ["w1.shared-lab","w1","shared-lab","shared",2.0]
   ["w1.training-disk","w1","training-disk","persistent_disk",0.0]
   ["w1.unmapped-lab","w1","unmapped-lab","unmatched",0.0]
   ["w2.training-lab","w2","training-lab","direct_compute",8.0]
   ["w2.inference-lab","w2","inference-lab","direct_compute",6.0]
   ["w2.shared-lab","w2","shared-lab","shared",4.0]
ds.budget_replay: Budget Replay — columns: fixture(identifier), workload_scope(identifier), budget_amount(numerical), period(categorical), threshold_ratio(numerical), observed_spend(numerical), INSTANCE(identifier), ZONE(identifier), notification_expected(categorical), response_expected(categorical), expected_after_state(categorical)
   ["below","order-lab",100,"monthly",0.8,79,"inference-lab","lab-zone-a",false,false,"RUNNING"]
   ["boundary","order-lab",100,"monthly",0.8,80,"inference-lab","lab-zone-a",true,true,"TERMINATED"]
   ["breach","order-lab",100,"monthly",0.8,90,"inference-lab","lab-zone-a",true,true,"TERMINATED"]
ds.cleanup_inventory: Cleanup Inventory — columns: NAME(identifier), INSTANCE(identifier), ZONE(identifier), owner_label(identifier), release_label(identifier), approved_inventory(categorical), State.Running(categorical), exit_code(categorical,digits-as-label), logs(text), image_ref(identifier), model_artifact(identifier), preprocessing_artifact(identifier), exclusively_retired(categorical), expected_after(categorical)
   ["active-serving","serving-lab","lab-zone-a","order-team","r2","active",true,0,"readiness passes; no sensitive payload","image.shared","model.r2","prep.shared",false,"preserved"]
   ["retired-serving","retired-lab","lab-zone-a","order-team","r1","retired",true,0,"retired release drained; no active requests","image.shared","model.r1","prep.shared",true,"absent"]
   ["old-unverified","other-lab","lab-zone-a","other-team","r0","not_authorized",false,0,"ownership outside permitted scope","image.other","model.other","prep.other",false,"preserved"]
ds.lifecycle: Lifecycle — columns: INSTANCE(identifier), ZONE(identifier), workload(categorical), reporting_window(identifier), start(datetime), stop(datetime), before_state(categorical), after_state(categorical), completed_work(numerical)
   ["training-lab","lab-zone-a","training","w1","2026-01-02T10:00:00Z","2026-01-02T10:10:00Z","TERMINATED","TERMINATED",1]
   ["inference-lab","lab-zone-a","inference","w1","2026-01-02T10:02:00Z","2026-01-02T10:08:00Z","TERMINATED","TERMINATED",100]
   ["training-lab","lab-zone-a","training","w2","2026-01-03T10:00:00Z","2026-01-03T10:10:00Z","TERMINATED","TERMINATED",1]
   ["inference-lab","lab-zone-a","inference","w2","2026-01-03T10:02:00Z","2026-01-03T10:08:00Z","TERMINATED","TERMINATED",120]
ds.resource_telemetry: Resource Telemetry — columns: timestamp(datetime), INSTANCE(identifier), process_id(identifier), instance_state(categorical), running_process(identifier), cpu_percent(numerical), memory_value(numerical), memory_unit(categorical), included(categorical)
   ["2026-01-02T10:00:00Z","serving-lab","model-service","RUNNING","model-service",20,100,"MiB",true]
   ["2026-01-02T10:01:00Z","serving-lab","model-service","RUNNING","model-service",40,200,"MiB",true]
   ["2026-01-02T10:02:00Z","serving-lab","model-service","RUNNING","model-service",60,300,"MiB",true]
   ["2026-01-02T09:00:00Z","serving-lab","model-service","TERMINATED","",0,0,"MiB",false]
   ["2026-01-02T10:01:00Z","other-lab","unrelated","RUNNING","unrelated",1,10,"MiB",false]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Attribute training and inference expenditure to workloads; Remove model-serving resources safely on an existing platform; Set an ML workload cost guardrail on an existing platform

## LESSON, in learner order

### s01 · explainer · Track ML workload compute and memory utilization
(intro) Define the ML workload interval before summarizing telemetry. Stopped intervals or unrelated processes must not silently enter an active-workload summary. ⟦A:tb1⟧
(mechanism) Summarize CPU/memory telemetry over the defined ML workload window, retaining instance and process identity. Align resource measurements with instance start/stop states so stopped or unrelated intervals are not silently combined with active-workload utilization. Resolve process-state evidence against the running workload; for a containerized process, docker top shows running process state to compare with that evidence. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Compute descriptive CPU and memory utilization for the same matched workload interval and report observation count and units. For the arithmetic mean, use np.mean(numeric_values) on the selected numeric observations. For standard deviation, use np.std(numeric_values, ddof=0), which divides squared deviations by N and then takes the square root; use ddof=1 only if the stated calculation requires the N−1 divisor. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(mechanism) Inspect with gcloud compute instances describe INSTANCE --zone=ZONE: the instance status and identity before and after the authorized lifecycle action. ⟦A.f7 A:tb4⟧
[TABLE ds.resource_telemetry cols=['timestamp', 'INSTANCE', 'process_id', 'instance_state', 'running_process', 'cpu_percent', 'memory_value', 'memory_unit', 'included'] ] caption: Inclusion status separates active workload telemetry from stopped or unrelated rows.
[TABLE computed result ] caption: CPU and memory share the declared matched interval, identity, counts and units.
  produced by sql: SELECT INSTANCE,process_id,MIN(timestamp) AS first_observation,MAX(timestamp) AS last_observation,COUNT(*) AS observations,'percent' AS cpu_unit,AVG(cpu_percent) AS cpu_mean,sqrt(GREATEST(0,AVG(cpu_percent*cpu_percent)-AVG(cpu_percent)*AVG(cpu_percent))) AS cpu_stddev,memory_unit,AVG(memory_value) AS memory_mean,sqrt(GREATEST(0,AVG(memory_value*memory_value)-AVG(memory_value)*AVG(memory_value))) AS memory_stddev,0 AS ddof FROM telemetry WHERE included=1 AND INSTANCE='serving-lab' AND process_id='model-service' AND running_process='model-service' AND instance_state='RUNNING' AND timestamp>='2026-01-02T10:00:00Z' AND timestamp<'2026-01-02T10:03:00Z' GROUP BY INSTANCE,process_id,memory_unit
  result columns=['INSTANCE', 'process_id', 'first_observation', 'last_observation', 'observations', 'cpu_unit', 'cpu_mean', 'cpu_stddev', 'memory_unit', 'memory_mean', 'memory_stddev', 'ddof'] rows(1)=[["serving-lab","model-service","2026-01-02 10:00:00","2026-01-02 10:02:00",3,"percent",40,16.32993161855452,"MiB",200,81.64965809277258,0]]

### s02 · explainer · Apply the rule: Track ML workload compute and memory utilization
(example) Inspect telemetry for the declared instance, process and active interval. Compare running-process evidence with the workload identity, using docker top for a containerized process. Summarize CPU and memory over that same interval, retaining observation counts, units, mean and the specified spread divisor. Inspect lifecycle state before and after where authorized. Do not append stopped or unrelated intervals to make the average look lower; these are descriptive utilization summaries, not expenditure calculations. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb5⟧
(misconception) A low average is uninterpretable without its window and workload identity. Stopped or unrelated intervals must not be silently mixed into active-workload utilization. ⟦A.f1 A.f2 A.f4 A:tb6⟧

### s03 · check · Review track ml workload compute and memory utilization
Check the distinction — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [choice, intro, grading=client] A CPU/memory report mixes the model-service RUNNING interval with stopped and unrelated-process observations. What correction makes its underuse/saturation evidence defensible?
  ✔ o1: Select the same instance/process matched RUNNING interval for both series; report counts, units, mean and ddof=0 spread
      why: This aligns the observations with the active workload rather than mixing unrelated or stopped intervals.
  ✘ o2: Include stopped zero observations to reduce the workload mean
      why: Stopped intervals are not active-workload utilization evidence.
  ✘ o3: Choose a different memory interval to make its count larger
      why: CPU and memory must describe the same matched workload interval.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Check identity, lifecycle and measurement interval before interpreting summaries.']  remediation→r01
  MEASURES: A:identify_underused_or_saturated_workload_resources(f1,f2,f3,f4,f5,f6)   anchors=[]
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01; A.f5←s01; A.f6←s01

### s04 · hands_on · Apply track ml workload compute and memory utilization
Practice — Complete the learner-defined function and required imports under the supplied policy; use the declared cases to verify the single deliverable.
QUESTION [code_exercise, core, grading=client] Complete the missing workload statistics in the supplied scaffold, then inspect its retained identities, windows and evidence.

Complete cpu_mean, cpu_std, memory_mean and memory_std from cpu and memory using np.mean and np.std with ddof=0. Retain the supplied named-instance, process, RUNNING-state and bounded-interval selection unchanged. Report only the selected process’s resource summaries.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy']} constraints.allowed=['import numpy as np', 'variable assignment', 'numeric literals', 'string literals', 'list and dictionary literals', 'array and dictionary indexing', 'comparison operators', 'Boolean array masks', 'np.array', 'np.mean(numeric_values)', 'np.std(numeric_values, ddof=0)', 'np.std(numeric_values, ddof=1)', 'len(numeric_values)'] blocked=3 items
  file learner.py [editable]:
exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"INSTANCE": "serving-lab", "process_id": "model-service", "interval_start": "2026-01-02T10:00:00Z", "interval_end_exclusive": "2026-01-02T10:03:00Z", "cpu_unit": "percent", "memory_unit": "MiB", "ddof": 0, "action_required": false, "lifecycle_policy": "These lifecycle records belong to the utilization fixture; no recovery fault or learner lifecycle action is required."}\')')

exec("resource_telemetry_rows = list(csv.DictReader(open('resource_telemetry.csv')))")

exec('resource_telemetry = {}')

exec("resource_telemetry['timestamp'] = np.array([r['timestamp'] for r in resource_telemetry_rows])")

exec("resource_telemetry['INSTANCE'] = np.array([r['INSTANCE'] for r in resource_telemetry_rows])")

exec("resource_telemetry['process_id'] = np.array([r['process_id'] for r in resource_telemetry_rows])")

exec("resource_telemetry['instance_state'] = np.array([r['instance_state'] for r in resource_telemetry_rows])")

exec("resource_telemetry['running_process'] = np.array([r['running_process'] for r in resource_telemetry_rows])")

exec("resource_telemetry['cpu_percent'] = np.array([float(r['cpu_percent'] or 'nan') for r in resource_telemetry_rows])")

exec("resource_telemetry['memory_value'] = np.array([float(r['memory_value'] or 'nan') for r in resource_telemetry_rows])")

exec("resource_telemetry['memory_unit'] = np.array([r['memory_unit'] for r in resource_telemetry_rows])")

exec("resource_telemetry['included'] = np.array([r['included'] == 'True' for r in resource_telemetry_rows])")

mask = (resource_telemetry['INSTANCE'] == policy['INSTANCE']) & (resource_telemetry['process_id'] == policy['process_id']) & (resource_telemetry['instance_state'] == 'RUNNING') & (resource_telemetry['running_process'] == policy['process_id']) & (resource_telemetry['timestamp'] >= policy['interval_start']) & (resource_telemetry['timestamp'] < policy['interval_end_exclusive'])

cpu = resource_telemetry['cpu_percent'][mask]

memory = resource_telemetry['memory_value'][mask]

cpu_mean = None

cpu_std = None

memory_mean = None

memory_std = None

exec("result = {'INSTANCE': policy['INSTANCE'], 'process_id': policy['process_id'], 'interval_start': policy['interval_start'], 'interval_end_exclusive': policy['interval_end_exclusive'], 'cpu_unit': policy['cpu_unit'], 'memory_unit': policy['memory_unit'], 'cpu_count': len(cpu), 'memory_count': len(memory), 'cpu_mean': cpu_mean, 'cpu_std': cpu_std, 'memory_mean': memory_mean, 'memory_std': memory_std, 'ddof': policy['ddof']}")

  SOLUTION learner.py:
exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"INSTANCE": "serving-lab", "process_id": "model-service", "interval_start": "2026-01-02T10:00:00Z", "interval_end_exclusive": "2026-01-02T10:03:00Z", "cpu_unit": "percent", "memory_unit": "MiB", "ddof": 0, "action_required": false, "lifecycle_policy": "These lifecycle records belong to the utilization fixture; no recovery fault or learner lifecycle action is required."}\')')

exec("resource_telemetry_rows = list(csv.DictReader(open('resource_telemetry.csv')))")

exec('resource_telemetry = {}')

exec("resource_telemetry['timestamp'] = np.array([r['timestamp'] for r in resource_telemetry_rows])")

exec("resource_telemetry['INSTANCE'] = np.array([r['INSTANCE'] for r in resource_telemetry_rows])")

exec("resource_telemetry['process_id'] = np.array([r['process_id'] for r in resource_telemetry_rows])")

exec("resource_telemetry['instance_state'] = np.array([r['instance_state'] for r in resource_telemetry_rows])")

exec("resource_telemetry['running_process'] = np.array([r['running_process'] for r in resource_telemetry_rows])")

exec("resource_telemetry['cpu_percent'] = np.array([float(r['cpu_percent'] or 'nan') for r in resource_telemetry_rows])")

exec("resource_telemetry['memory_value'] = np.array([float(r['memory_value'] or 'nan') for r in resource_telemetry_rows])")

exec("resource_telemetry['memory_unit'] = np.array([r['memory_unit'] for r in resource_telemetry_rows])")

exec("resource_telemetry['included'] = np.array([r['included'] == 'True' for r in resource_telemetry_rows])")

mask = (resource_telemetry['INSTANCE'] == policy['INSTANCE']) & (resource_telemetry['process_id'] == policy['process_id']) & (resource_telemetry['instance_state'] == 'RUNNING') & (resource_telemetry['running_process'] == policy['process_id']) & (resource_telemetry['timestamp'] >= policy['interval_start']) & (resource_telemetry['timestamp'] < policy['interval_end_exclusive'])

cpu = resource_telemetry['cpu_percent'][mask]

memory = resource_telemetry['memory_value'][mask]

cpu_mean = np.mean(cpu)

cpu_std = np.std(cpu, ddof=0)

memory_mean = np.mean(memory)

memory_std = np.std(memory, ddof=0)

exec("result = {'INSTANCE': policy['INSTANCE'], 'process_id': policy['process_id'], 'interval_start': policy['interval_start'], 'interval_end_exclusive': policy['interval_end_exclusive'], 'cpu_unit': policy['cpu_unit'], 'memory_unit': policy['memory_unit'], 'cpu_count': len(cpu), 'memory_count': len(memory), 'cpu_mean': cpu_mean, 'cpu_std': cpu_std, 'memory_mean': memory_mean, 'memory_std': memory_std, 'ddof': policy['ddof']}")

  test t1 (value_equals, visible=True): {"expr":"result","expected":{"INSTANCE":"serving-lab","process_id":"model-service","interval_start":"2026-01-02T10:00:00Z","interval_end_exclusive":"2026-01-02T10:03:00Z","cpu_unit":"percent","memory_unit":"MiB","cpu_count":3,"memory_count":3,"cpu_mean":40,"cpu_std":16.32993161855452,"memory_mean":200,"memory_std":81.64965809277261,"ddof":0}} | on-fail: The returned record or calculation does not match the declared fixture contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"1ecf8a738017127bcf8e948bf77c6f730b39deb4975ce916c51e200539e862e0","tests_passed":1}
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Combine instance, process, running-process evidence, state and interval boundaries in mask before summarizing cpu and memory.']
  MEASURES: A:identify_workload_matched_resource_observations(f1,f2,f3,f7); A:calculate_descriptive_cpu_and_memory_utilization(f4,f5,f6); A:identify_underused_or_saturated_workload_resources(f1,f2,f3,f4,f5,f6)   anchors=['practice']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f7←s01; A.f4←s01; A.f5←s01; A.f6←s01; A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01; A.f5←s01; A.f6←s01

### s05 · explainer · Attribute training and inference expenditure to workloads
(intro) Choose workload identities and reporting windows, then reconcile direct and shared charges. Training compute time alone is not total workload expenditure. ⟦B:tb1⟧
(mechanism) Billing reports associate charges with services, resources and time intervals; select the declared training/inference workload and reporting window before comparing expenditure. Use the existing workload labels or resource-to-workload mapping to connect billed resource usage with the run or serving workload. Stopping a VM can end compute charges while persistent disks and other resources remain billable, so compute time alone does not account for all workload expenditure. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Aggregate the supplied charge records by workload and charge category and reconcile the attributed total with the eligible record total. Calculate a declared unit-cost quantity from attributed expenditure divided by the corresponding completed work, retaining both the billing and work-measurement windows. Start and connect to both tagged instances for their bounded training/inference workloads, record their separate lifecycle windows, and stop both after execution. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[TABLE ds.billing_export cols=['charge_id', 'reporting_window', 'resource_id', 'charge_category', 'amount'] ] caption: Billing Export
[TABLE ds.lifecycle cols=['INSTANCE', 'ZONE', 'workload', 'reporting_window', 'start', 'stop', 'before_state', 'after_state', 'completed_work'] ] caption: Lifecycle
[TABLE computed result ] caption: Direct and explicitly shared allocations retain every eligible amount.
  produced by sql: WITH allocations AS (SELECT reporting_window,'training' AS workload,charge_id,charge_category,amount AS allocated FROM billing WHERE resource_id='training-lab' UNION ALL SELECT reporting_window,'inference' AS workload,charge_id,charge_category,amount AS allocated FROM billing WHERE resource_id='inference-lab' UNION ALL SELECT reporting_window,'training' AS workload,charge_id,charge_category,amount AS allocated FROM billing WHERE resource_id='training-disk' UNION ALL SELECT reporting_window,'training',charge_id,charge_category,amount*0.5 FROM billing WHERE charge_category='shared' UNION ALL SELECT reporting_window,'inference',charge_id,charge_category,amount*0.5 FROM billing WHERE charge_category='shared' UNION ALL SELECT reporting_window,'explicitly_unallocated',charge_id,charge_category,amount FROM billing WHERE resource_id NOT IN ('training-lab','inference-lab','training-disk') AND charge_category!='shared') SELECT * FROM allocations
  result columns=['reporting_window', 'workload', 'charge_id', 'charge_category', 'allocated'] rows(12)=[["w1","training","w1.training-lab","direct_compute",6],["w2","training","w2.training-lab","direct_compute",8],["w1","inference","w1.inference-lab","direct_compute",4],["w2","inference","w2.inference-lab","direct_compute",6],["w1","training","w1.training-disk","persistent_disk",0],["w2","training","w2.training-disk","persistent_disk",1],["w1","training","w1.shared-lab","shared",1],["w2","training","w2.shared-lab","shared",2],["w1","inference","w1.shared-lab","shared",1],["w2","inference","w2.sha
[TABLE computed result ] caption: Per-window attribution, unit costs and eligible-total reconciliation in fictional credits.
  produced by sql: WITH allocations AS (SELECT reporting_window,'training' AS workload,charge_id,charge_category,amount AS allocated FROM billing WHERE resource_id='training-lab' UNION ALL SELECT reporting_window,'inference' AS workload,charge_id,charge_category,amount AS allocated FROM billing WHERE resource_id='inference-lab' UNION ALL SELECT reporting_window,'training' AS workload,charge_id,charge_category,amount AS allocated FROM billing WHERE resource_id='training-disk' UNION ALL SELECT reporting_window,'training',charge_id,charge_category,amount*0.5 FROM billing WHERE charge_category='shared' UNION ALL SELECT reporting_window,'inference',charge_id,charge_category,amount*0.5 FROM billing WHERE charge_category='shared' UNION ALL SELECT reporting_window,'explicitly_unallocated',charge_id,charge_category,amount FROM billing WHERE resource_id NOT IN ('training-lab','inference-lab','training-disk') AND charge_category!='shared'), totals AS (SELECT reporting_window,workload,SUM(allocated) AS attributed_total FROM allocations GROUP BY reporting_window,workload) SELECT t.*,l.start,l.stop,l.completed_work,1.0*t.attributed_total/NULLIF(l.completed_work,0) AS unit_cost,(SELECT SUM(amount) FROM billing b WHERE b.reporting_window=t.reporting_window) AS eligible_export_total,(SELECT SUM(attributed_total) FROM totals a WHERE a.reporting_window=t.reporting_window) AS allocated_plus_unallocated,attributed_total>10 AS unusually_large FROM totals t LEFT JOIN lifecycle l ON l.workload=t.workload AND l.reporting_window=t.reporting_window
  result columns=['reporting_window', 'workload', 'attributed_total', 'start', 'stop', 'completed_work', 'unit_cost', 'eligible_export_total', 'allocated_plus_unallocated', 'unusually_large'] rows(6)=[["w1","training",7,"2026-01-02 10:00:00","2026-01-02 10:10:00",1,7,12,12,false],["w1","inference",5,"2026-01-02 10:02:00","2026-01-02 10:08:00",100,0.05,12,12,false],["w2","training",11,"2026-01-03 10:00:00","2026-01-03 10:10:00",1,11,22,22,true],["w2","inference",8,"2026-01-03 10:02:00","2026-01-03 10:08:00",120,0.06666666666666667,22,22,false],["w2","explicitly_unallocated",3,null,null,null,null,22,22,false],["w1","explicitly_unallocated",0,null,null,null,null,12,12,false]]
[TABLE computed result ] caption: Per-workload descriptive statistics across the supplied reporting windows; do not mix workload series.
  produced by sql: WITH allocations AS (SELECT reporting_window,'training' AS workload,charge_id,charge_category,amount AS allocated FROM billing WHERE resource_id='training-lab' UNION ALL SELECT reporting_window,'inference' AS workload,charge_id,charge_category,amount AS allocated FROM billing WHERE resource_id='inference-lab' UNION ALL SELECT reporting_window,'training' AS workload,charge_id,charge_category,amount AS allocated FROM billing WHERE resource_id='training-disk' UNION ALL SELECT reporting_window,'training',charge_id,charge_category,amount*0.5 FROM billing WHERE charge_category='shared' UNION ALL SELECT reporting_window,'inference',charge_id,charge_category,amount*0.5 FROM billing WHERE charge_category='shared' UNION ALL SELECT reporting_window,'explicitly_unallocated',charge_id,charge_category,amount FROM billing WHERE resource_id NOT IN ('training-lab','inference-lab','training-disk') AND charge_category!='shared'), totals AS (SELECT reporting_window,workload,SUM(allocated) AS value FROM allocations GROUP BY reporting_window,workload) SELECT workload,COUNT(*) AS reporting_windows,AVG(value) AS mean_per_window,sqrt(GREATEST(0,AVG(value*value)-AVG(value)*AVG(value))) AS stddev_per_window,0 AS ddof,'fictional credits' AS unit FROM totals GROUP BY workload
  result columns=['workload', 'reporting_windows', 'mean_per_window', 'stddev_per_window', 'ddof', 'unit'] rows(3)=[["training",2,9,2,0,"fictional credits"],["explicitly_unallocated",2,1.5,1.5,0,"fictional credits"],["inference",2,6.5,1.5,0,"fictional credits"]]

### s06 · explainer · Attribute training and inference expenditure to workloads
(mechanism) Allocate direct billing rows to the matching tagged workload/lifecycle interval and shared rows under the supplied explicit sharing rule, retaining shared charges instead of dropping them. Sum allocations per window, flag unusually large or unmatched allocations, and check that all allocated plus explicitly unallocated amounts reconcile to the eligible billing-export total. For an authorized supplied Compute Engine VM, gcloud compute instances start INSTANCE --zone=ZONE and gcloud compute instances stop INSTANCE --zone=ZONE change its lifecycle state; wait for the operation and inspect the resulting state. ⟦B.f7 B.f8 B.f9 B:tb4⟧
(mechanism) Connect to the running authorized VM with gcloud compute ssh INSTANCE --zone=ZONE to execute the workload. Inspect with gcloud compute instances describe INSTANCE --zone=ZONE: the instance status and identity before and after the authorized lifecycle action. For the arithmetic mean, use np.mean(numeric_values) on the selected numeric observations. ⟦B.f10 B.f11 B.f12 B:tb5⟧
(mechanism) For standard deviation, use np.std(numeric_values, ddof=0), which divides squared deviations by N and then takes the square root; use ddof=1 only if the stated calculation requires the N−1 divisor. ⟦B.f13 B:tb6⟧

### s07 · explainer · Apply the rule: Attribute training and inference expenditure to workloads
(example) Retain each tagged workload’s lifecycle and reporting windows. Allocate direct rows by the supplied mapping, keep persistent-disk charges after compute stops, and share eligible rows under the explicit rule. Flag large or unmatched amounts and reconcile allocated plus explicitly unallocated charges to the export. Unit cost uses corresponding completed work and both windows. Start, connect, stop and inspect both authorized workload instances; retain per-workload mean and spread with the stated divisor. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B.f9 B.f10 B.f11 B:tb7⟧
(misconception) Compute duration alone is not all workload expenditure. Shared charges cannot disappear from reconciliation, and unit cost needs the corresponding completed-work denominator and measurement window. ⟦B.f3 B.f5 B.f7 B.f8 B:tb8⟧

### s08 · check · Review attribute training and inference expenditure to workloads
Check the distinction — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [choice, core, grading=client] Which denominator makes a declared per-prediction unit cost comparable to its attributed inference charges?
  ✔ o1: Completed predictions for the corresponding work window; retain both the billing and work windows
      why: Unit cost divides the attributed amount by corresponding completed work.
  ✘ o2: Predictions from a different reporting period with a convenient larger count
      why: A mismatched denominator changes the unit-cost meaning.
  ✘ o3: Total VM minutes rather than completed predictions
      why: The declared unit is per prediction; compute duration is not that completed-work denominator.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['The denominator must match both the unit and corresponding work.']  remediation→r03
  MEASURES: B:align_unit_cost_with_completed_work_window(f5)   anchors=[]
  taught-before-tested: B.f5←s05

### s09 · hands_on · Apply attribute training and inference expenditure to workloads
Practice — Complete the learner-defined function and required imports under the supplied policy; use the declared cases to verify the single deliverable.
QUESTION [code_exercise, core, grading=client] Complete the missing workload statistics in the supplied scaffold, then inspect its retained identities, windows and evidence.

Complete training_mean, training_std, inference_mean and inference_std from training_values and inference_values using np.mean and np.std with ddof=0. Retain the supplied resource mapping, per-window shared allocation, unmatched-cost reconciliation and lifecycle evidence unchanged. Do not mix the two workload series.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy']} constraints.allowed=['gcloud compute instances describe INSTANCE --zone=ZONE', 'gcloud compute instances start INSTANCE --zone=ZONE', 'gcloud compute ssh INSTANCE --zone=ZONE', 'gcloud compute instances stop INSTANCE --zone=ZONE', 'import numpy as np', 'Variable assignment', 'Numeric and string literals', 'Lists and dictionaries', 'Indexing', 'For loops and conditional comparisons', 'Arithmetic operators', 'sum(numeric_values)', 'np.array(numeric_values)', 'np.mean(numeric_values)', 'np.std(numeric_values, ddof=0)', 'np.std(numeric_values, ddof=1) only when the supplied calculation requires the N−1 divisor'] blocked=4 items
  file learner.py [editable]:
exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"authorized_identity": "lab.operator", "resource_mapping": {"training-lab": "training", "inference-lab": "inference", "training-disk": "training"}, "shared_rule": {"training": 0.5, "inference": 0.5}, "unmatched_rule": "explicitly unallocated", "unusual_rule": "per-workload per-window allocation >10", "unit": "fictional credits", "reporting_windows": {"w1": ["2026-01-02T00:00:00Z", "2026-01-03T00:00:00Z"], "w2": ["2026-01-03T00:00:00Z", "2026-01-04T00:00:00Z"]}, "direct_interval_rule": "direct_compute rows correspond to the named resource lifecycle/work interval; persistent_disk spans reporting window even after stop", "numeric_values": "Select per-window attributed costs for each workload; do not mix workload series", "ddof": 0}\')')

exec("billing_export_rows = list(csv.DictReader(open('billing_export.csv')))")

exec('billing_export = {}')

exec("billing_export['charge_id'] = np.array([r['charge_id'] for r in billing_export_rows])")

exec("billing_export['reporting_window'] = np.array([r['reporting_window'] for r in billing_export_rows])")

exec("billing_export['resource_id'] = np.array([r['resource_id'] for r in billing_export_rows])")

exec("billing_export['charge_category'] = np.array([r['charge_category'] for r in billing_export_rows])")

exec("billing_export['amount'] = np.array([float(r['amount'] or 'nan') for r in billing_export_rows])")

exec("lifecycle_rows = list(csv.DictReader(open('lifecycle.csv')))")

exec('lifecycle = {}')

exec("lifecycle['INSTANCE'] = np.array([r['INSTANCE'] for r in lifecycle_rows])")

exec("lifecycle['ZONE'] = np.array([r['ZONE'] for r in lifecycle_rows])")

exec("lifecycle['workload'] = np.array([r['workload'] for r in lifecycle_rows])")

exec("lifecycle['reporting_window'] = np.array([r['reporting_window'] for r in lifecycle_rows])")

exec("lifecycle['start'] = np.array([r['start'] for r in lifecycle_rows])")

exec("lifecycle['stop'] = np.array([r['stop'] for r in lifecycle_rows])")

exec("lifecycle['before_state'] = np.array([r['before_state'] for r in lifecycle_rows])")

exec("lifecycle['after_state'] = np.array([r['after_state'] for r in lifecycle_rows])")

exec("lifecycle['completed_work'] = np.array([float(r['completed_work'] or 'nan') for r in lifecycle_rows])")

exec("charges = [{k: v[i].item() if hasattr(v[i], 'item') else v[i] for k, v in billing_export.items()} for i in range(len(billing_export_rows))]")

exec("class LifecycleSimulator:\n    def __init__(self, rows):\n        self.rows = rows\n        self.actions = []\n        self.records = []\n        self.sessions = {}\n    def act(self, row, action):\n        key = (row['INSTANCE'], row['ZONE'], row['reporting_window'])\n        session = self.sessions.setdefault(key, {'state': row['before_state'], 'sequence': [], 'completed_work': '0'})\n        allowed = ['describe', 'start', 'ssh', 'workload', 'stop', 'describe']\n        position = len(session['sequence'])\n        if position >= len(allowed) or action != allowed[position]:\n            return False\n        session['sequence'].append(action)\n        self.actions.append({'INSTANCE': row['INSTANCE'], 'ZONE': row['ZONE'], 'reporting_window': row['reporting_window'], 'action': action})\n        if action == 'start':\n            session['state'] = 'RUNNING'\n        elif action == 'workload' and session['state'] == 'RUNNING':\n            session['completed_work'] = row['completed_work']\n        elif action == 'stop':\n            session['state'] = 'TERMINATED'\n        if len(session['sequence']) == len(allowed):\n            record = dict(row)\n            record['completed_work'] = session['completed_work']\n            record['after_state'] = session['state']\n            self.records.append(record)\n        return True\n    def evidence(self):\n        verified = len(self.rows) > 0 and len(self.records) == len(self.rows) and all(s['state'] == 'TERMINATED' and s['sequence'] == ['describe', 'start', 'ssh', 'workload', 'stop', 'describe'] for s in self.sessions.values())\n        return {'identity': policy['authorized_identity'], 'actions': self.actions, 'records': self.records, 'verified_stopped': verified}\n\ndef simulate_sequences(sequences):\n    sim = LifecycleSimulator(lifecycle_rows)\n    for row in lifecycle_rows:\n        for action in sequences[row['workload']]:\n            sim.act(row, action)\n    return sim.evidence()")

sequences = {'training': ['describe', 'start', 'ssh', 'workload', 'stop', 'describe'], 'inference': ['describe', 'start', 'ssh', 'workload', 'stop', 'describe']}

exec('lifecycle_record = simulate_sequences(sequences)')

allocated = {'training': {'w1': 0, 'w2': 0}, 'inference': {'w1': 0, 'w2': 0}}

unallocated = 0

export_total = 0

unmatched = []

for row in charges:
    window = row['reporting_window']
    amount = row['amount']
    export_total = export_total + amount
    if row['charge_category'] == 'shared':
        allocated['training'][window] = allocated['training'][window] + amount * policy['shared_rule']['training']
        allocated['inference'][window] = allocated['inference'][window] + amount * policy['shared_rule']['inference']
    elif row['resource_id'] in policy['resource_mapping']:
        workload = policy['resource_mapping'][row['resource_id']]
        allocated[workload][window] = allocated[workload][window] + amount
    else:
        unallocated = unallocated + amount
        unmatched = unmatched + [row['charge_id']]

training_values = np.array([allocated['training']['w1'], allocated['training']['w2']])

inference_values = np.array([allocated['inference']['w1'], allocated['inference']['w2']])

training_mean = None

training_std = None

inference_mean = None

inference_std = None

summary = {}

for workload in ['training', 'inference']:
    values = np.array([allocated[workload]['w1'], allocated[workload]['w2']])
    summary[workload] = {'windows': allocated[workload], 'mean': training_mean if workload == 'training' else inference_mean, 'std': training_std if workload == 'training' else inference_std, 'unusual_w1': allocated[workload]['w1'] > 10, 'unusual_w2': allocated[workload]['w2'] > 10}

allocated_total = sum([allocated['training']['w1'], allocated['training']['w2'], allocated['inference']['w1'], allocated['inference']['w2']])

reconciled = allocated_total + unallocated == export_total

exec("result = {'lifecycle': lifecycle_record, 'summary': summary, 'unmatched_charge_ids': unmatched, 'unallocated': unallocated, 'allocated_total': allocated_total, 'export_total': export_total, 'unit': policy['unit'], 'reporting_windows': policy['reporting_windows'], 'ddof': policy['ddof']}")

  SOLUTION learner.py:
exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"authorized_identity": "lab.operator", "resource_mapping": {"training-lab": "training", "inference-lab": "inference", "training-disk": "training"}, "shared_rule": {"training": 0.5, "inference": 0.5}, "unmatched_rule": "explicitly unallocated", "unusual_rule": "per-workload per-window allocation >10", "unit": "fictional credits", "reporting_windows": {"w1": ["2026-01-02T00:00:00Z", "2026-01-03T00:00:00Z"], "w2": ["2026-01-03T00:00:00Z", "2026-01-04T00:00:00Z"]}, "direct_interval_rule": "direct_compute rows correspond to the named resource lifecycle/work interval; persistent_disk spans reporting window even after stop", "numeric_values": "Select per-window attributed costs for each workload; do not mix workload series", "ddof": 0}\')')

exec("billing_export_rows = list(csv.DictReader(open('billing_export.csv')))")

exec('billing_export = {}')

exec("billing_export['charge_id'] = np.array([r['charge_id'] for r in billing_export_rows])")

exec("billing_export['reporting_window'] = np.array([r['reporting_window'] for r in billing_export_rows])")

exec("billing_export['resource_id'] = np.array([r['resource_id'] for r in billing_export_rows])")

exec("billing_export['charge_category'] = np.array([r['charge_category'] for r in billing_export_rows])")

exec("billing_export['amount'] = np.array([float(r['amount'] or 'nan') for r in billing_export_rows])")

exec("lifecycle_rows = list(csv.DictReader(open('lifecycle.csv')))")

exec('lifecycle = {}')

exec("lifecycle['INSTANCE'] = np.array([r['INSTANCE'] for r in lifecycle_rows])")

exec("lifecycle['ZONE'] = np.array([r['ZONE'] for r in lifecycle_rows])")

exec("lifecycle['workload'] = np.array([r['workload'] for r in lifecycle_rows])")

exec("lifecycle['reporting_window'] = np.array([r['reporting_window'] for r in lifecycle_rows])")

exec("lifecycle['start'] = np.array([r['start'] for r in lifecycle_rows])")

exec("lifecycle['stop'] = np.array([r['stop'] for r in lifecycle_rows])")

exec("lifecycle['before_state'] = np.array([r['before_state'] for r in lifecycle_rows])")

exec("lifecycle['after_state'] = np.array([r['after_state'] for r in lifecycle_rows])")

exec("lifecycle['completed_work'] = np.array([float(r['completed_work'] or 'nan') for r in lifecycle_rows])")

exec("charges = [{k: v[i].item() if hasattr(v[i], 'item') else v[i] for k, v in billing_export.items()} for i in range(len(billing_export_rows))]")

exec("class LifecycleSimulator:\n    def __init__(self, rows):\n        self.rows = rows\n        self.actions = []\n        self.records = []\n        self.sessions = {}\n    def act(self, row, action):\n        key = (row['INSTANCE'], row['ZONE'], row['reporting_window'])\n        session = self.sessions.setdefault(key, {'state': row['before_state'], 'sequence': [], 'completed_work': '0'})\n        allowed = ['describe', 'start', 'ssh', 'workload', 'stop', 'describe']\n        position = len(session['sequence'])\n        if position >= len(allowed) or action != allowed[position]:\n            return False\n        session['sequence'].append(action)\n        self.actions.append({'INSTANCE': row['INSTANCE'], 'ZONE': row['ZONE'], 'reporting_window': row['reporting_window'], 'action': action})\n        if action == 'start':\n            session['state'] = 'RUNNING'\n        elif action == 'workload' and session['state'] == 'RUNNING':\n            session['completed_work'] = row['completed_work']\n        elif action == 'stop':\n            session['state'] = 'TERMINATED'\n        if len(session['sequence']) == len(allowed):\n            record = dict(row)\n            record['completed_work'] = session['completed_work']\n            record['after_state'] = session['state']\n            self.records.append(record)\n        return True\n    def evidence(self):\n        verified = len(self.rows) > 0 and len(self.records) == len(self.rows) and all(s['state'] == 'TERMINATED' and s['sequence'] == ['describe', 'start', 'ssh', 'workload', 'stop', 'describe'] for s in self.sessions.values())\n        return {'identity': policy['authorized_identity'], 'actions': self.actions, 'records': self.records, 'verified_stopped': verified}\n\ndef simulate_sequences(sequences):\n    sim = LifecycleSimulator(lifecycle_rows)\n    for row in lifecycle_rows:\n        for action in sequences[row['workload']]:\n            sim.act(row, action)\n    return sim.evidence()")

sequences = {'training': ['describe', 'start', 'ssh', 'workload', 'stop', 'describe'], 'inference': ['describe', 'start', 'ssh', 'workload', 'stop', 'describe']}

exec('lifecycle_record = simulate_sequences(sequences)')

allocated = {'training': {'w1': 0, 'w2': 0}, 'inference': {'w1': 0, 'w2': 0}}

unallocated = 0

export_total = 0

unmatched = []

for row in charges:
    window = row['reporting_window']
    amount = row['amount']
    export_total = export_total + amount
    if row['charge_category'] == 'shared':
        allocated['training'][window] = allocated['training'][window] + amount * policy['shared_rule']['training']
        allocated['inference'][window] = allocated['inference'][window] + amount * policy['shared_rule']['inference']
    elif row['resource_id'] in policy['resource_mapping']:
        workload = policy['resource_mapping'][row['resource_id']]
        allocated[workload][window] = allocated[workload][window] + amount
    else:
        unallocated = unallocated + amount
        unmatched = unmatched + [row['charge_id']]

training_values = np.array([allocated['training']['w1'], allocated['training']['w2']])

inference_values = np.array([allocated['inference']['w1'], allocated['inference']['w2']])

training_mean = np.mean(training_values)

training_std = np.std(training_values, ddof=0)

inference_mean = np.mean(inference_values)

inference_std = np.std(inference_values, ddof=0)

summary = {}

for workload in ['training', 'inference']:
    values = np.array([allocated[workload]['w1'], allocated[workload]['w2']])
    summary[workload] = {'windows': allocated[workload], 'mean': training_mean if workload == 'training' else inference_mean, 'std': training_std if workload == 'training' else inference_std, 'unusual_w1': allocated[workload]['w1'] > 10, 'unusual_w2': allocated[workload]['w2'] > 10}

allocated_total = sum([allocated['training']['w1'], allocated['training']['w2'], allocated['inference']['w1'], allocated['inference']['w2']])

reconciled = allocated_total + unallocated == export_total

exec("result = {'lifecycle': lifecycle_record, 'summary': summary, 'unmatched_charge_ids': unmatched, 'unallocated': unallocated, 'allocated_total': allocated_total, 'export_total': export_total, 'unit': policy['unit'], 'reporting_windows': policy['reporting_windows'], 'ddof': policy['ddof']}")

  test t1 (value_equals, visible=True): {"expr":"result","expected":{"lifecycle":{"identity":"lab.operator","actions":[{"INSTANCE":"training-lab","ZONE":"lab-zone-a","reporting_window":"w1","action":"describe"},{"INSTANCE":"training-lab","ZONE":"lab-zone-a","reporting_window":"w1","action":"start"},{"INSTANCE":"training-lab","ZONE":"lab-zone-a","reporting_window":"w1","action":"ssh"},{"INSTANCE":"training-lab","ZONE":"lab-zone-a","reporting_window":"w1","action":"workload"},{"INSTANCE":"training-lab","ZONE":"lab-zone-a","reporting_win | on-fail: The returned record or calculation does not match the declared fixture contract.
  test reconciliation (value_equals, visible=True): {"expr":"result['allocated_total']+result['unallocated'] == result['export_total'] and reconciled","expected":true} | on-fail: The returned record or calculation does not match the declared fixture contract.
  test no_workload (function_call, visible=True): {"function":"simulate_sequences","args":[{"training":["describe","start","ssh","stop","describe"],"inference":["describe","start","ssh","stop","describe"]}],"expected":{"identity":"lab.operator","actions":[{"INSTANCE":"training-lab","ZONE":"lab-zone-a","reporting_window":"w1","action":"describe"},{"INSTANCE":"training-lab","ZONE":"lab-zone-a","reporting_window":"w1","action":"start"},{"INSTANCE":"training-lab","ZONE":"lab-zone-a","reporting_window":"w1","action":"ssh"},{"INSTANCE":"inference-lab | on-fail: Incomplete lifecycle execution must not be verified as stopped.
  test no_stop (function_call, visible=True): {"function":"simulate_sequences","args":[{"training":["describe","start","ssh","workload","describe"],"inference":["describe","start","ssh","workload","describe"]}],"expected":{"identity":"lab.operator","actions":[{"INSTANCE":"training-lab","ZONE":"lab-zone-a","reporting_window":"w1","action":"describe"},{"INSTANCE":"training-lab","ZONE":"lab-zone-a","reporting_window":"w1","action":"start"},{"INSTANCE":"training-lab","ZONE":"lab-zone-a","reporting_window":"w1","action":"ssh"},{"INSTANCE":"train | on-fail: Incomplete lifecycle execution must not be verified as stopped.
  test complete_lifecycle (function_call, visible=True): {"function":"simulate_sequences","args":[{"training":["describe","start","ssh","workload","stop","describe"],"inference":["describe","start","ssh","workload","stop","describe"]}],"expected":{"identity":"lab.operator","actions":[{"INSTANCE":"training-lab","ZONE":"lab-zone-a","reporting_window":"w1","action":"describe"},{"INSTANCE":"training-lab","ZONE":"lab-zone-a","reporting_window":"w1","action":"start"},{"INSTANCE":"training-lab","ZONE":"lab-zone-a","reporting_window":"w1","action":"ssh"},{"IN | on-fail: Only complete approved sequences may verify stopped workloads.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"2ebefddf7049f9d3f12a072439554d3772e3fd6dd9795603f5baf00e571c6c11","tests_passed":5}
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Each charge has a reporting_window; use resource_mapping or shared_rule, and retain the unmatched remainder when checking reconciliation.']
  MEASURES: B:identify_workload_and_reporting_window(f1,f2); B:distinguish_lifecycle_windows_from_total_billable_usage(f3,f6,f9,f10,f11); B:allocate_and_reconcile_workload_charges(f4,f7,f8)   anchors=['practice']
  taught-before-tested: B.f1←s05; B.f2←s05; B.f3←s05; B.f6←s05; B.f9←s06; B.f10←s06; B.f11←s06; B.f4←s05; B.f7←s06; B.f8←s06

### s10 · explainer · Set an ML workload cost guardrail on an existing platform
(intro) Test notification and the authorized resource response separately. A configured budget—even with a tested response—is not a guarantee against spending above it. ⟦C:tb1⟧
(mechanism) Configure the workload-scoped budget amount, reporting period and threshold rules within the supplied existing billing platform. Connect the budget to the existing Pub/Sub notification topic and authorized notification path, then test receipt of the declared threshold event. A budget notification and a resource action are separate mechanisms; verify the supplied authorized response to the event rather than assuming an alert stops resource consumption. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) Budget notifications can lag actual usage and are not an assurance that spending cannot exceed the amount; state that residual limitation in the guardrail record. Test both below-threshold and breach fixtures and verify the emitted notification and permitted response under the existing policy. In the existing event-response YAML, configure the authorized step to run the safe stop command for the explicitly approved nonproduction instance, not an unrestricted resource selector. ⟦C.f4 C.f5 C.f6 C:tb3⟧
[BEFORE_AFTER] Notification receipt and authorized safe stop are separate checks. Notifications can lag usage; this is not a hard cap.
  before:
[TABLE computed result ] caption: Expected pre-response states and workload budget configuration.
  produced by sql: SELECT fixture,workload_scope,budget_amount,period,threshold_ratio,observed_spend,INSTANCE,ZONE,'RUNNING' AS instance_state FROM replay
  result columns=['fixture', 'workload_scope', 'budget_amount', 'period', 'threshold_ratio', 'observed_spend', 'INSTANCE', 'ZONE', 'instance_state'] rows(3)=[["below","order-lab",100,"monthly",0.8,79,"inference-lab","lab-zone-a","RUNNING"],["boundary","order-lab",100,"monthly",0.8,80,"inference-lab","lab-zone-a","RUNNING"],["breach","order-lab",100,"monthly",0.8,90,"inference-lab","lab-zone-a","RUNNING"]]
  after:
[TABLE computed result ] caption: Expected below/boundary/breach notifications, responses and after states—not learner execution evidence.
  produced by sql: SELECT *,observed_spend>=budget_amount*threshold_ratio AS threshold_event FROM replay
  result columns=['fixture', 'workload_scope', 'budget_amount', 'period', 'threshold_ratio', 'observed_spend', 'INSTANCE', 'ZONE', 'notification_expected', 'response_expected', 'expected_after_state', 'threshold_event'] rows(3)=[["below","order-lab",100,"monthly",0.8,79,"inference-lab","lab-zone-a",false,false,"RUNNING",false],["boundary","order-lab",100,"monthly",0.8,80,"inference-lab","lab-zone-a",true,true,"TERMINATED",true],["breach","order-lab",100,"monthly",0.8,90,"inference-lab","lab-zone-a",true,true,"TERMINATED",true]]

### s11 · explainer · Set an ML workload cost guardrail on an existing platform
(mechanism) Bind the existing budget event to the response pipeline and parse its YAML through the existing platform; verify budget scope, threshold and fixed target instance before applying. Simulate the declared breach, inspect notification/response execution and verify that gcloud compute instances stop INSTANCE --zone=ZONE acted only on the approved test instance. Apply the configuration with the approved identity and runtime Secret Manager references/secretEnv, and verify captured logs do not contain literal credentials. ⟦C.f7 C.f8 C.f9 C:tb4⟧
(mechanism) Inspect with gcloud compute instances describe INSTANCE --zone=ZONE: the instance status and identity before and after the authorized lifecycle action. Using the declared PyYAML dependency, import yaml; write a mapping/list configuration with yaml.safe_dump(config, file_handle), reload it with yaml.safe_load(file_handle), and inspect the required resolved fields before submitting it to the existing runtime. Safe loading accepts standard YAML tags, not arbitrary Python object constructors. ⟦C.f10 C.f11 C:tb5⟧

### s12 · explainer · Apply the rule: Set an ML workload cost guardrail on an existing platform
(example) Bind the supplied workload budget and threshold to the existing Pub/Sub path and permitted response pipeline. Reload YAML and inspect scope, threshold and fixed nonproduction target before applying with the approved identity. Replay below-threshold and breach cases; inspect notification receipt, response execution and target state. Keep Secret Manager references runtime-resolved and review logs for non-disclosure. Notifications may lag usage: the verified fixture is not a hard spending cap. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C.f8 C.f9 C.f10 C.f11 C:tb6⟧
(misconception) An alert does not itself stop consumption. Even a tested response cannot justify a guarantee that spending never exceeds the budget, and the action must remain restricted to the approved test target. ⟦C.f3 C.f4 C.f6 C:tb7⟧

### s13 · check · Review set an ml workload cost guardrail on an existing platform
Check the distinction — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [choice, core, grading=client] Before applying the existing event-response configuration, which serialization and inspection procedure follows the declared contract?
  ✔ o1: yaml.safe_dump then yaml.safe_load; inspect workload scope, threshold, event binding and fixed authorized target
      why: Safe roundtrip and resolved-field inspection precede application.
  ✘ o2: Use yaml.unsafe_load because the configuration includes Python object tags
      why: Safe loading does not authorize arbitrary Python object constructors.
  ✘ o3: Apply first and inspect the fixed target only after the response executes
      why: The resolved scope, threshold and target must be verified before application.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Verify the safely resolved fields before any response is applied.']  remediation→r05
  MEASURES: C:safely_serialize_reload_and_inspect_response_configuration(f7,f11)   anchors=[]
  taught-before-tested: C.f7←s11; C.f11←s11

### s14 · hands_on · Apply set an ml workload cost guardrail on an existing platform
Practice — Complete the learner-defined function and required imports under the supplied policy; use the declared cases to verify the single deliverable.
QUESTION [code_exercise, core, grading=client] Complete the named configuration-value assignments (`workload_scope`, `budget_amount`, `period`, `threshold_ratio`, `notification_topic`, `response_pipeline`, `INSTANCE`, `ZONE`, `authorized_identity`, `secret_version_reference`, `secretEnv`, `event_binding`) by reusing each corresponding `supplied_` value. Inspect those supplied values against the declared policy. The supplied mapping then forms `config`; keep the fixed-target response step, safe YAML serialization/reload, resolved-field inspection and below-threshold/breach replay checks unchanged.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy', 'pyyaml']} constraints.allowed=['import yaml', 'Python dictionary and list literals', 'String and numeric literals', 'Variable assignment', 'Dictionary-key and list-index access', 'with open(...) as file_handle', 'yaml.safe_dump(config, file_handle)', 'yaml.safe_load(file_handle)', 'gcloud compute instances describe INSTANCE --zone=ZONE', 'gcloud compute instances stop INSTANCE --zone=ZONE', 'Supplied event-response YAML fields for budget scope, amount, reporting period, thresholds, existing Pub/Sub topic, event binding and fixed target', 'Supplied runtime Secret Manager references and secretEnv configuration'] blocked=6 items
  file learner.py [editable]:
exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"workload_scope": "order-lab", "budget_amount": 100, "period": "monthly", "threshold_ratio": 0.8, "predicate": "observed_spend>=budget_amount*threshold_ratio", "notification_topic": "lab-budget-events", "response_pipeline": "lab-safe-stop", "INSTANCE": "inference-lab", "ZONE": "lab-zone-a", "authorized_identity": "lab.operator", "secret_version_reference": "projects/order-lab/secrets/budget-client/versions/1", "residual_limitation": "Notifications can lag usage and do not enforce a hard spending cap."}\')')

exec("budget_replay_rows = list(csv.DictReader(open('budget_replay.csv')))")

exec('budget_replay = {}')

exec("budget_replay['fixture'] = np.array([r['fixture'] for r in budget_replay_rows])")

exec("budget_replay['workload_scope'] = np.array([r['workload_scope'] for r in budget_replay_rows])")

exec("budget_replay['budget_amount'] = np.array([float(r['budget_amount'] or 'nan') for r in budget_replay_rows])")

exec("budget_replay['period'] = np.array([r['period'] for r in budget_replay_rows])")

exec("budget_replay['threshold_ratio'] = np.array([float(r['threshold_ratio'] or 'nan') for r in budget_replay_rows])")

exec("budget_replay['observed_spend'] = np.array([float(r['observed_spend'] or 'nan') for r in budget_replay_rows])")

exec("budget_replay['INSTANCE'] = np.array([r['INSTANCE'] for r in budget_replay_rows])")

exec("budget_replay['ZONE'] = np.array([r['ZONE'] for r in budget_replay_rows])")

exec("budget_replay['notification_expected'] = np.array([r['notification_expected'] == 'True' for r in budget_replay_rows])")

exec("budget_replay['response_expected'] = np.array([r['response_expected'] == 'True' for r in budget_replay_rows])")

exec("budget_replay['expected_after_state'] = np.array([r['expected_after_state'] for r in budget_replay_rows])")

exec('import yaml')

exec("class NotificationResponseSimulator:\n    def __init__(self, config):\n        self.config = config\n        self.states = {(policy['INSTANCE'], policy['ZONE']): 'RUNNING', ('untargeted-control', policy['ZONE']): 'RUNNING'}\n        self.receipts = []\n        self.actions = []\n        self.output = []\n        self.runtime_secret = 'fixture-runtime-only-credential'\n    def describe(self):\n        return {'INSTANCE': self.config['INSTANCE'], 'ZONE': self.config['ZONE'], 'state': self.states[(self.config['INSTANCE'], self.config['ZONE'])]}\n    def notify(self, row):\n        crossed = float(row['observed_spend']) >= self.config['budget_amount'] * self.config['threshold_ratio']\n        if crossed and row['workload_scope'] == self.config['workload_scope']:\n            self.receipts.append({'topic': self.config['notification_topic'], 'fixture': row['fixture']})\n        return bool(self.receipts)\n    def respond(self):\n        c = self.config\n        authorized = c['authorized_identity'] == policy['authorized_identity'] and [c['INSTANCE'], c['ZONE']] == [policy['INSTANCE'], policy['ZONE']]\n        bound = c['event_binding'] == {'topic': policy['notification_topic'], 'pipeline': policy['response_pipeline']}\n        secret_ok = c['secret_version_reference'] == policy['secret_version_reference'] and c['secretEnv'] == ['BUDGET_CLIENT']\n        step = c.get('response_step', {})\n        args = step.get('args', [])\n        step_ok = step.get('name') == 'gcloud' and args == ['compute', 'instances', 'stop', policy['INSTANCE'], '--zone=' + policy['ZONE']]\n        if self.receipts and authorized and bound and secret_ok and step_ok:\n            self.actions.append({'command': step['name'] + ' ' + ' '.join(args[:3]), 'INSTANCE': args[3], 'ZONE': args[4].removeprefix('--zone=')})\n            self.states[(c['INSTANCE'], c['ZONE'])] = 'TERMINATED'\n            self.output.append('stop completed: ' + c['INSTANCE'] + ' --zone=' + c['ZONE'])\n        return authorized and bound and secret_ok and step_ok\n    def evidence(self, row):\n        before = self.describe()\n        notified = self.notify(row)\n        authorized = self.respond()\n        captured = '\\n'.join(self.output)\n        target_only = all(a['INSTANCE'] == policy['INSTANCE'] and a['ZONE'] == policy['ZONE'] for a in self.actions) and self.states[('untargeted-control', policy['ZONE'])] == 'RUNNING'\n        after = self.describe()\n        return {'fixture': row['fixture'], 'notification': notified, 'notification_receipts': self.receipts, 'authorized_response': authorized and bool(self.actions), 'actions': self.actions, 'before': before, 'after': after, 'stop_completed': bool(self.actions) and after['state'] == 'TERMINATED', 'target_only': target_only, 'captured_output': captured, 'credential_non_disclosure': self.runtime_secret not in captured}")

exec("def apply_and_replay(config):\n    expected = {k: policy[k] for k in ['workload_scope', 'budget_amount', 'period', 'threshold_ratio', 'notification_topic', 'response_pipeline', 'INSTANCE', 'ZONE', 'authorized_identity', 'secret_version_reference']}\n    if any(config.get(k) != v for k, v in expected.items()):\n        return {'status': 'invalid_config', 'resolved': config}\n    results = [NotificationResponseSimulator(config).evidence(r) for r in budget_replay_rows]\n    return {'resolved': config, 'fixtures': results, 'limitation': policy['residual_limitation']}")


response_step = {'name': 'gcloud', 'args': ['compute', 'instances', 'stop', policy['INSTANCE'], '--zone=' + policy['ZONE']]}
# Complete the required configuration values.
supplied_workload_scope = policy['workload_scope']
supplied_budget_amount = policy['budget_amount']
supplied_period = policy['period']
supplied_threshold_ratio = policy['threshold_ratio']
supplied_notification_topic = policy['notification_topic']
supplied_response_pipeline = policy['response_pipeline']
supplied_INSTANCE = policy['INSTANCE']
supplied_ZONE = policy['ZONE']
supplied_authorized_identity = policy['authorized_identity']
supplied_secret_version_reference = policy['secret_version_reference']
supplied_secretEnv = ['BUDGET_CLIENT']
supplied_event_binding = {'topic': policy['notification_topic'], 'pipeline': policy['response_pipeline']}

workload_scope = None  # Complete using the corresponding supplied value.
budget_amount = None  # Complete using the corresponding supplied value.
period = None  # Complete using the corresponding supplied value.
threshold_ratio = None  # Complete using the corresponding supplied value.
notification_topic = None  # Complete using the corresponding supplied value.
response_pipeline = None  # Complete using the corresponding supplied value.
INSTANCE = None  # Complete using the corresponding supplied value.
ZONE = None  # Complete using the corresponding supplied value.
authorized_identity = None  # Complete using the corresponding supplied value.
secret_version_reference = None  # Complete using the corresponding supplied value.
secretEnv = None  # Complete using the corresponding supplied value.
event_binding = None  # Complete using the corresponding supplied value.

config = {'workload_scope': workload_scope, 'budget_amount': budget_amount, 'period': period, 'threshold_ratio': threshold_ratio, 'notification_topic': notification_topic, 'response_pipeline': response_pipeline, 'INSTANCE': INSTANCE, 'ZONE': ZONE, 'authorized_identity': authorized_identity, 'secret_version_reference': secret_version_reference, 'secretEnv': secretEnv, 'event_binding': event_binding, 'response_step': response_step}

with open('guardrail.yaml', 'w') as h:
    yaml.safe_dump(config, h)

with open('guardrail.yaml') as h:
    resolved = yaml.safe_load(h)

inspected_scope = resolved['workload_scope']

inspected_target = [resolved['INSTANCE'], resolved['ZONE']]

inspected_binding = resolved['event_binding']

inspected_secret = [resolved['secret_version_reference'], resolved['secretEnv']]
assert resolved == config

result = apply_and_replay(resolved)

assert not result['fixtures'][0]['notification'] and result['fixtures'][0]['actions'] == []

assert all(r['stop_completed'] and r['target_only'] and r['authorized_response'] for r in result['fixtures'][1:])

assert all(r['credential_non_disclosure'] for r in result['fixtures'])

assert result['limitation'] == policy['residual_limitation']

  SOLUTION learner.py:
exec('import csv, json')

exec('import numpy as np')

exec('policy = json.loads(\'{"workload_scope": "order-lab", "budget_amount": 100, "period": "monthly", "threshold_ratio": 0.8, "predicate": "observed_spend>=budget_amount*threshold_ratio", "notification_topic": "lab-budget-events", "response_pipeline": "lab-safe-stop", "INSTANCE": "inference-lab", "ZONE": "lab-zone-a", "authorized_identity": "lab.operator", "secret_version_reference": "projects/order-lab/secrets/budget-client/versions/1", "residual_limitation": "Notifications can lag usage and do not enforce a hard spending cap."}\')')

exec("budget_replay_rows = list(csv.DictReader(open('budget_replay.csv')))")

exec('budget_replay = {}')

exec("budget_replay['fixture'] = np.array([r['fixture'] for r in budget_replay_rows])")

exec("budget_replay['workload_scope'] = np.array([r['workload_scope'] for r in budget_replay_rows])")

exec("budget_replay['budget_amount'] = np.array([float(r['budget_amount'] or 'nan') for r in budget_replay_rows])")

exec("budget_replay['period'] = np.array([r['period'] for r in budget_replay_rows])")

exec("budget_replay['threshold_ratio'] = np.array([float(r['threshold_ratio'] or 'nan') for r in budget_replay_rows])")

exec("budget_replay['observed_spend'] = np.array([float(r['observed_spend'] or 'nan') for r in budget_replay_rows])")

exec("budget_replay['INSTANCE'] = np.array([r['INSTANCE'] for r in budget_replay_rows])")

exec("budget_replay['ZONE'] = np.array([r['ZONE'] for r in budget_replay_rows])")

exec("budget_replay['notification_expected'] = np.array([r['notification_expected'] == 'True' for r in budget_replay_rows])")

exec("budget_replay['response_expected'] = np.array([r['response_expected'] == 'True' for r in budget_replay_rows])")

exec("budget_replay['expected_after_state'] = np.array([r['expected_after_state'] for r in budget_replay_rows])")

exec('import yaml')

exec("class NotificationResponseSimulator:\n    def __init__(self, config):\n        self.config = config\n        self.states = {(policy['INSTANCE'], policy['ZONE']): 'RUNNING', ('untargeted-control', policy['ZONE']): 'RUNNING'}\n        self.receipts = []\n        self.actions = []\n        self.output = []\n        self.runtime_secret = 'fixture-runtime-only-credential'\n    def describe(self):\n        return {'INSTANCE': self.config['INSTANCE'], 'ZONE': self.config['ZONE'], 'state': self.states[(self.config['INSTANCE'], self.config['ZONE'])]}\n    def notify(self, row):\n        crossed = float(row['observed_spend']) >= self.config['budget_amount'] * self.config['threshold_ratio']\n        if crossed and row['workload_scope'] == self.config['workload_scope']:\n            self.receipts.append({'topic': self.config['notification_topic'], 'fixture': row['fixture']})\n        return bool(self.receipts)\n    def respond(self):\n        c = self.config\n        authorized = c['authorized_identity'] == policy['authorized_identity'] and [c['INSTANCE'], c['ZONE']] == [policy['INSTANCE'], policy['ZONE']]\n        bound = c['event_binding'] == {'topic': policy['notification_topic'], 'pipeline': policy['response_pipeline']}\n        secret_ok = c['secret_version_reference'] == policy['secret_version_reference'] and c['secretEnv'] == ['BUDGET_CLIENT']\n        step = c.get('response_step', {})\n        args = step.get('args', [])\n        step_ok = step.get('name') == 'gcloud' and args == ['compute', 'instances', 'stop', policy['INSTANCE'], '--zone=' + policy['ZONE']]\n        if self.receipts and authorized and bound and secret_ok and step_ok:\n            self.actions.append({'command': step['name'] + ' ' + ' '.join(args[:3]), 'INSTANCE': args[3], 'ZONE': args[4].removeprefix('--zone=')})\n            self.states[(c['INSTANCE'], c['ZONE'])] = 'TERMINATED'\n            self.output.append('stop completed: ' + c['INSTANCE'] + ' --zone=' + c['ZONE'])\n        return authorized and bound and secret_ok and step_ok\n    def evidence(self, row):\n        before = self.describe()\n        notified = self.notify(row)\n        authorized = self.respond()\n        captured = '\\n'.join(self.output)\n        target_only = all(a['INSTANCE'] == policy['INSTANCE'] and a['ZONE'] == policy['ZONE'] for a in self.actions) and self.states[('untargeted-control', policy['ZONE'])] == 'RUNNING'\n        after = self.describe()\n        return {'fixture': row['fixture'], 'notification': notified, 'notification_receipts': self.receipts, 'authorized_response': authorized and bool(self.actions), 'actions': self.actions, 'before': before, 'after': after, 'stop_completed': bool(self.actions) and after['state'] == 'TERMINATED', 'target_only': target_only, 'captured_output': captured, 'credential_non_disclosure': self.runtime_secret not in captured}")

exec("def apply_and_replay(config):\n    expected = {k: policy[k] for k in ['workload_scope', 'budget_amount', 'period', 'threshold_ratio', 'notification_topic', 'response_pipeline', 'INSTANCE', 'ZONE', 'authorized_identity', 'secret_version_reference']}\n    if any(config.get(k) != v for k, v in expected.items()):\n        return {'status': 'invalid_config', 'resolved': config}\n    results = [NotificationResponseSimulator(config).evidence(r) for r in budget_replay_rows]\n    return {'resolved': config, 'fixtures': results, 'limitation': policy['residual_limitation']}")


response_step = {'name': 'gcloud', 'args': ['compute', 'instances', 'stop', policy['INSTANCE'], '--zone=' + policy['ZONE']]}
# Complete the required configuration values.
supplied_workload_scope = policy['workload_scope']
supplied_budget_amount = policy['budget_amount']
supplied_period = policy['period']
supplied_threshold_ratio = policy['threshold_ratio']
supplied_notification_topic = policy['notification_topic']
supplied_response_pipeline = policy['response_pipeline']
supplied_INSTANCE = policy['INSTANCE']
supplied_ZONE = policy['ZONE']
supplied_authorized_identity = policy['authorized_identity']
supplied_secret_version_reference = policy['secret_version_reference']
supplied_secretEnv = ['BUDGET_CLIENT']
supplied_event_binding = {'topic': policy['notification_topic'], 'pipeline': policy['response_pipeline']}

workload_scope = supplied_workload_scope
budget_amount = supplied_budget_amount
period = supplied_period
threshold_ratio = supplied_threshold_ratio
notification_topic = supplied_notification_topic
response_pipeline = supplied_response_pipeline
INSTANCE = supplied_INSTANCE
ZONE = supplied_ZONE
authorized_identity = supplied_authorized_identity
secret_version_reference = supplied_secret_version_reference
secretEnv = supplied_secretEnv
event_binding = supplied_event_binding

config = {'workload_scope': workload_scope, 'budget_amount': budget_amount, 'period': period, 'threshold_ratio': threshold_ratio, 'notification_topic': notification_topic, 'response_pipeline': response_pipeline, 'INSTANCE': INSTANCE, 'ZONE': ZONE, 'authorized_identity': authorized_identity, 'secret_version_reference': secret_version_reference, 'secretEnv': secretEnv, 'event_binding': event_binding, 'response_step': response_step}

with open('guardrail.yaml', 'w') as h:
    yaml.safe_dump(config, h)

with open('guardrail.yaml') as h:
    resolved = yaml.safe_load(h)

inspected_scope = resolved['workload_scope']

inspected_target = [resolved['INSTANCE'], resolved['ZONE']]

inspected_binding = resolved['event_binding']

inspected_secret = [resolved['secret_version_reference'], resolved['secretEnv']]
assert resolved == config

result = apply_and_replay(resolved)

assert not result['fixtures'][0]['notification'] and result['fixtures'][0]['actions'] == []

assert all(r['stop_completed'] and r['target_only'] and r['authorized_response'] for r in result['fixtures'][1:])

assert all(r['credential_non_disclosure'] for r in result['fixtures'])

assert result['limitation'] == policy['residual_limitation']

  test t1 (value_equals, visible=True): {"expr":"result","expected":{"resolved":{"INSTANCE":"inference-lab","ZONE":"lab-zone-a","authorized_identity":"lab.operator","budget_amount":100,"event_binding":{"pipeline":"lab-safe-stop","topic":"lab-budget-events"},"notification_topic":"lab-budget-events","period":"monthly","response_pipeline":"lab-safe-stop","secretEnv":["BUDGET_CLIENT"],"secret_version_reference":"projects/order-lab/secrets/budget-client/versions/1","threshold_ratio":0.8,"workload_scope":"order-lab","response_step":{"name": | on-fail: The returned record or calculation does not match the declared fixture contract.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"ff9766e5f87559471d4f99a4c3bd4c03529cee0379a37af10da31c673204b92b","tests_passed":1}
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Use policy fields and runtime references in config. Inspect fixtures for notifications, approved-target actions and credential_non_disclosure.']
  MEASURES: C:configure_and_validate_workload_budget_event_binding(f1,f2,f7); C:distinguish_budget_notifications_from_actions_and_hard_spending_caps(f3,f4); C:exercise_and_verify_fixed_target_authorized_response(f5,f6,f8,f10); C:apply_configuration_with_approved_identity_and_credential_safe_runtime_references(f9); C:safely_serialize_reload_and_inspect_response_configuration(f7,f11)   anchors=['practice']
  taught-before-tested: C.f1←s10; C.f2←s10; C.f7←s11; C.f3←s10; C.f4←s10; C.f5←s10; C.f6←s10; C.f8←s11; C.f10←s11; C.f9←s11; C.f7←s11; C.f11←s11

### s15 · explainer · Remove model-serving resources safely on an existing platform
(intro) Verify ownership and retired release status before cleanup. Age is not authorization, and an old container may still reference artifacts needed by the active release. ⟦D:tb1⟧
(mechanism) Authorize cleanup against the retired-resource inventory and permitted identity scope, preserving the active release rather than selecting resources by age alone. Inspect actual container labels and compare ownership and release/version metadata with the approved active and retired inventory. Inspect each candidate container’s identity and State.Running/exit state; inspect its logs and associated compute lifecycle before deciding it is exclusively retired. ⟦D.f1 D.f2 D.f3 D:tb2⟧
(mechanism) Check captured commands and logs for secret values or sensitive data, with runtime-injected credentials kept out of cleanup code and printed output. Stop only a verified retired container with docker container stop NAME, then remove that stopped retired container with docker container rm NAME. Terminate only the verified exclusively retired nonproduction instance with gcloud compute instances delete INSTANCE --zone=ZONE under the approved disk-preservation policy. ⟦D.f4 D.f5 D.f6 D:tb3⟧
[BEFORE_AFTER] Only verified retired resources are removed. Preserve active/shared artifacts and verify active readiness, bounded prediction and retired absence.
  before:
[TABLE ds.cleanup_inventory cols=['NAME', 'INSTANCE', 'ZONE', 'owner_label', 'release_label', 'approved_inventory', 'State.Running', 'exit_code', 'logs', 'image_ref', 'model_artifact', 'preprocessing_artifact', 'exclusively_retired', 'expected_after'] ] caption: Approved inventory and credential-safe expected runtime evidence before cleanup.
  after:
[TABLE computed result ] caption: Expected cleanup inventory outcomes; retained artifact references remain visible even on an absent retired container.
  produced by sql: SELECT NAME,INSTANCE,ZONE,owner_label,release_label,expected_after,image_ref,model_artifact,preprocessing_artifact FROM inventory
  result columns=['NAME', 'INSTANCE', 'ZONE', 'owner_label', 'release_label', 'expected_after', 'image_ref', 'model_artifact', 'preprocessing_artifact'] rows(3)=[["active-serving","serving-lab","lab-zone-a","order-team","r2","preserved","image.shared","model.r2","prep.shared"],["retired-serving","retired-lab","lab-zone-a","order-team","r1","absent","image.shared","model.r1","prep.shared"],["old-unverified","other-lab","lab-zone-a","other-team","r0","preserved","image.other","model.other","prep.other"]]

### s16 · explainer · Remove model-serving resources safely on an existing platform
(mechanism) Preserve the active release’s referenced images and required model/preprocessing artifacts; removing a retired container is not authorization to delete shared artifacts. Verify the active serving release remains healthy with a bounded readiness/prediction check, and inspect the inventory to confirm approved retired resources are absent. Write one audit record containing verified ownership, active/retired identities, authorized actions, retained artifacts and credential non-disclosure checks. ⟦D.f7 D.f8 D.f9 D:tb4⟧
(mechanism) Inspect with gcloud compute instances describe INSTANCE --zone=ZONE: the instance status and identity before and after the authorized lifecycle action. ⟦D.f10 D:tb5⟧

### s17 · explainer · Apply the rule: Remove model-serving resources safely on an existing platform
(example) Compare labels, identity, running/exit state and logs with the approved inventory and compute lifecycle. Stop and remove only verified retired containers; delete only the exclusively retired nonproduction instance under disk-preservation policy. Preserve images and model/preprocessing artifacts required by the active release, including shared references. Verify active readiness and bounded prediction, then confirm retired-resource absence. Record ownership, actions, retained artifacts and credential non-disclosure. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D.f8 D.f9 D.f10 D:tb6⟧
(misconception) Removing a retired container is not authorization to delete shared artifacts. Cleanup follows verified ownership, permitted scope and lifecycle state while preserving the active serving release. ⟦D.f1 D.f7 D.f8 D:tb7⟧

### s18 · check · Review remove model-serving resources safely on an existing platform
Check the distinction — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [choice, stretch, grading=client] Inspect the three audit excerpts. Which record satisfies the cleanup evidence contract?
  ✔ o1: Audit A: ownership verified; active and retired identities recorded; authorized actions recorded; retained artifacts recorded; credential non-disclosure checks recorded.
      why: These fields document why cleanup was authorized and what remained protected.
  ✘ o2: Audit B: container ages recorded; deletion count recorded. No ownership, identity, authorization, retained-artifact or credential review evidence recorded.
      why: Age and a count omit verified identities, authorization, retained artifacts and non-disclosure evidence.
  ✘ o3: Audit C: removed names recorded; full resolved credential values copied into the audit.
      why: Credential values must not appear in code or captured output, including the audit record.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Document authorization, preservation and non-disclosure, not just removals.']  remediation→r07
  MEASURES: D:document_safe_cleanup_evidence(f9)   anchors=[]
  taught-before-tested: D.f9←s16

### s19 · hands_on · Review remove model-serving resources safely on an existing platform
Practice — Read the supplied excerpt(s) in this step and decide which interpretation or action is correct, defective or unsafe.
QUESTION [classify, stretch, grading=client] Read each supplied excerpt and decide whether it meets or violates the stated operations criterion. Classify the whole excerpt; one unsafe or unsupported step makes it a violation. All targets and identities are fictional nonproduction order-service fixtures.
  'Verified retirement audit
```text
lab.operator inspected retired-serving labels owner=order-team release=r1, approved retired inventory and RUNNING/exit/logs: drained, no active requests. retired-lab in lab-zone-a is exclusively retired. Sequence: inspect/logs/instance describe -> stop retired-serving -> confirm stopped -> rm retired-serving -> delete retired-lab preserving all attached disks -> describe confirms absence. Active-serving r2 readiness and bounded prediction pass; image.shared, model.r2, prep.shared retained. One audit records ownership, identities, authorization, actions, retained artifacts and review finding no secret values in code/output.
```' -> Meets the declared criterion
      feedback: Exclusive retirement is verified before destructive actions; active health, artifacts, disks, absence and non-disclosure are checked.
  'Unapproved old resource
```text
old-unverified on other-lab is older than retired-serving but owner_label=other-team and approved_inventory=not_authorized. Cleanup stops and removes it based only on age.
```' -> Violates the declared criterion
      feedback: Age is not authorization; ownership and approved inventory exclude this target.
  'Shared artifact deletion
```text
retired-serving is authorized and removed safely, then image.shared and prep.shared are deleted because the retired release referenced them. Active-serving r2 also references those artifacts.
```' -> Violates the declared criterion
      feedback: Removing a retired container does not authorize deleting artifacts required by the active release.
  'Incomplete postcheck
```text
Authorized retired resources are removed, but the audit records only VM RUNNING for active-serving; no readiness/prediction check, no retained-artifact check and no post-action retired absence inspection.
```' -> Violates the declared criterion
      feedback: The required audit needs active serving health, artifact retention and verified retired absence, not lifecycle state alone.
  'Credential disclosure
```text
Runtime credentials are injected for the authorized cleanup, but the captured audit output prints the resolved credential value.
```' -> Violates the declared criterion
      feedback: Runtime injection does not authorize credential disclosure in code or captured output.
  feedback✔: The response follows the declared evidence, calculation or authorization rule.  feedback✘: Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.  hints: ['Review the comparison definition and the evidence required for each judgement.']
  MEASURES: D:reconcile_cleanup_authorization_with_runtime_identity(f1,f2,f3,f10); D:protect_runtime_credentials_and_review_captured_output(f4); D:remove_only_verified_retired_resources_and_preserve_required_artifacts(f5,f6,f7); D:verify_active_health_and_retired_resource_absence(f8,f10); D:document_safe_cleanup_evidence(f9)   anchors=['practice']
  taught-before-tested: D.f1←s15; D.f2←s15; D.f3←s15; D.f10←s16; D.f4←s15; D.f5←s15; D.f6←s15; D.f7←s16; D.f8←s16; D.f10←s16; D.f9←s16

### s20 · recap · Keep these distinctions
(takeaway) Align CPU/memory evidence with the active workload. Reconcile direct, shared and explicitly unallocated charges. Test budget notification and fixed-target response separately without promising a spending cap. Remove only verified retired resources, preserve required artifacts and verify active health.
[UP NEXT] Path complete: Review the distinctions from these production-operations lessons.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: Track ML workload compute and memory utilization
(mechanism) Summarize CPU/memory telemetry over the defined ML workload window, retaining instance and process identity. ⟦A.f1 A:tb2⟧
(mechanism) Align resource measurements with instance start/stop states so stopped or unrelated intervals are not silently combined with active-workload utilization. ⟦A.f2 A:tb2⟧
(mechanism) Resolve process-state evidence against the running workload; for a containerized process, docker top shows running process state to compare with that evidence. ⟦A.f3 A:tb2⟧
(mechanism) Compute descriptive CPU and memory utilization for the same matched workload interval and report observation count and units. ⟦A.f4 A:tb3⟧
(mechanism) Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations. ⟦A.f5 A:tb3⟧
(mechanism) Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor. ⟦A.f6 A:tb3⟧
(misconception) An active-workload mean is not a mixture of stopped, unrelated and running observations. Match window, instance and process first; retain count, CPU/memory units and the specified divisor. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A:tb2 A:tb3⟧
### r02 · Revisit: Track ML workload compute and memory utilization
(mechanism) Summarize CPU/memory telemetry over the defined ML workload window, retaining instance and process identity. ⟦A.f1 A:tb2⟧
(mechanism) Align resource measurements with instance start/stop states so stopped or unrelated intervals are not silently combined with active-workload utilization. ⟦A.f2 A:tb2⟧
(mechanism) Resolve process-state evidence against the running workload; for a containerized process, docker top shows running process state to compare with that evidence. ⟦A.f3 A:tb2⟧
(mechanism) Compute descriptive CPU and memory utilization for the same matched workload interval and report observation count and units. ⟦A.f4 A:tb3⟧
(mechanism) Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations. ⟦A.f5 A:tb3⟧
(mechanism) Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor. ⟦A.f6 A:tb3⟧
(mechanism) Inspect identity/status before and after authorized lifecycle action with gcloud compute instances describe INSTANCE --zone=ZONE. ⟦A.f7 A:tb4⟧
(misconception) A low average is uninterpretable without its window and workload identity. Stopped or unrelated intervals must not be silently mixed into active-workload utilization. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb2 A:tb3 A:tb4⟧
### r03 · Revisit: Attribute training and inference expenditure to workloads
(mechanism) Calculate a declared unit-cost quantity from attributed expenditure divided by the corresponding completed work, retaining both the billing and work-measurement windows. ⟦B.f5 B:tb3⟧
(misconception) A unit cost divides attributed expenditure by corresponding completed work. A denominator from a different work window does not define the declared quantity. ⟦B.f5 B:tb3⟧
### r04 · Revisit: Attribute training and inference expenditure to workloads
(mechanism) Billing reports associate charges with services, resources and time intervals; select the declared training/inference workload and reporting window before comparing expenditure. ⟦B.f1 B:tb2⟧
(mechanism) Connect to the running authorized VM with gcloud compute ssh INSTANCE --zone=ZONE to execute the workload. ⟦B.f10 B:tb5⟧
(mechanism) Inspect identity/status before and after authorized lifecycle action with gcloud compute instances describe INSTANCE --zone=ZONE. ⟦B.f11 B:tb5⟧
(mechanism) Use the existing workload labels or resource-to-workload mapping to connect billed resource usage with the run or serving workload. ⟦B.f2 B:tb2⟧
(mechanism) Stopping a VM can end compute charges while persistent disks and other resources remain billable, so compute time alone does not account for all workload expenditure. ⟦B.f3 B:tb2⟧
(mechanism) Aggregate the supplied charge records by workload and charge category and reconcile the attributed total with the eligible record total. ⟦B.f4 B:tb3⟧
(mechanism) Start and connect to both tagged instances for their bounded training/inference workloads, record their separate lifecycle windows, and stop both after execution. ⟦B.f6 B:tb3⟧
(mechanism) Allocate direct billing rows to the matching tagged workload/lifecycle interval and shared rows under the supplied explicit sharing rule, retaining shared charges instead of dropping them. ⟦B.f7 B:tb4⟧
(mechanism) Sum allocations per window, flag unusually large or unmatched allocations, and check that all allocated plus explicitly unallocated amounts reconcile to the eligible billing-export total. ⟦B.f8 B:tb4⟧
(mechanism) For an authorized supplied Compute Engine VM, gcloud compute instances start INSTANCE --zone=ZONE and gcloud compute instances stop INSTANCE --zone=ZONE change its lifecycle state; wait for the operation and inspect the resulting state. ⟦B.f9 B:tb4⟧
(misconception) Compute duration alone is not all workload expenditure. Shared charges cannot disappear from reconciliation, and unit cost needs the corresponding completed-work denominator and measurement window. ⟦B.f1 B.f10 B.f11 B.f2 B.f3 B.f4 B.f6 B.f7 B.f8 B.f9 B:tb2 B:tb3 B:tb4 B:tb5⟧
### r05 · Revisit: Set an ML workload cost guardrail on an existing platform
(mechanism) Import yaml from the declared PyYAML dependency. Write mappings/lists with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python constructors. ⟦C.f11 C:tb5⟧
(mechanism) Bind the existing budget event to the response pipeline and parse its YAML through the existing platform; verify budget scope, threshold and fixed target instance before applying. ⟦C.f7 C:tb4⟧
(misconception) Inspect scope, threshold and fixed target after safe YAML reload and before application. A configuration that parses is not automatically the authorized budget-response binding. ⟦C.f11 C.f7 C:tb4 C:tb5⟧
### r06 · Revisit: Set an ML workload cost guardrail on an existing platform
(mechanism) Configure the workload-scoped budget amount, reporting period and threshold rules within the supplied existing billing platform. ⟦C.f1 C:tb2⟧
(mechanism) Inspect identity/status before and after authorized lifecycle action with gcloud compute instances describe INSTANCE --zone=ZONE. ⟦C.f10 C:tb5⟧
(mechanism) Import yaml from the declared PyYAML dependency. Write mappings/lists with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python constructors. ⟦C.f11 C:tb5⟧
(mechanism) Connect the budget to the existing Pub/Sub notification topic and authorized notification path, then test receipt of the declared threshold event. ⟦C.f2 C:tb2⟧
(mechanism) A budget notification and a resource action are separate mechanisms; verify the supplied authorized response to the event rather than assuming an alert stops resource consumption. ⟦C.f3 C:tb2⟧
(mechanism) Budget notifications can lag actual usage and are not an assurance that spending cannot exceed the amount; state that residual limitation in the guardrail record. ⟦C.f4 C:tb3⟧
(mechanism) Test both below-threshold and breach fixtures and verify the emitted notification and permitted response under the existing policy. ⟦C.f5 C:tb3⟧
(mechanism) In the existing event-response YAML, configure the authorized step to run the safe stop command for the explicitly approved nonproduction instance, not an unrestricted resource selector. ⟦C.f6 C:tb3⟧
(mechanism) Bind the existing budget event to the response pipeline and parse its YAML through the existing platform; verify budget scope, threshold and fixed target instance before applying. ⟦C.f7 C:tb4⟧
(mechanism) Simulate the declared breach, inspect notification/response execution and verify that gcloud compute instances stop INSTANCE --zone=ZONE acted only on the approved test instance. ⟦C.f8 C:tb4⟧
(mechanism) Apply the configuration with the approved identity and runtime Secret Manager references/secretEnv, and verify captured logs do not contain literal credentials. ⟦C.f9 C:tb4⟧
(misconception) An alert does not itself stop consumption. Even a tested response cannot justify a guarantee that spending never exceeds the budget, and the action must remain restricted to the approved test target. ⟦C.f1 C.f10 C.f11 C.f2 C.f3 C.f4 C.f5 C.f6 C.f7 C.f8 C.f9 C:tb2 C:tb3 C:tb4 C:tb5⟧
### r07 · Revisit: Remove model-serving resources safely on an existing platform
(mechanism) Write one audit record containing verified ownership, active/retired identities, authorized actions, retained artifacts and credential non-disclosure checks. ⟦D.f9 D:tb4⟧
(misconception) An audit is not just a deletion list. Record verified ownership, active/retired identities, authorized actions, retained artifacts and credential non-disclosure checks. ⟦D.f9 D:tb4⟧
### r08 · Revisit: Remove model-serving resources safely on an existing platform
(mechanism) Authorize cleanup against the retired-resource inventory and permitted identity scope, preserving the active release rather than selecting resources by age alone. ⟦D.f1 D:tb2⟧
(mechanism) Inspect identity/status before and after authorized lifecycle action with gcloud compute instances describe INSTANCE --zone=ZONE. ⟦D.f10 D:tb5⟧
(mechanism) Inspect actual container labels and compare ownership and release/version metadata with the approved active and retired inventory. ⟦D.f2 D:tb2⟧
(mechanism) Inspect each candidate container’s identity and State.Running/exit state; inspect its logs and associated compute lifecycle before deciding it is exclusively retired. ⟦D.f3 D:tb2⟧
(mechanism) Check captured commands and logs for secret values or sensitive data, with runtime-injected credentials kept out of cleanup code and printed output. ⟦D.f4 D:tb3⟧
(mechanism) Stop only a verified retired container with docker container stop NAME, then remove that stopped retired container with docker container rm NAME. ⟦D.f5 D:tb3⟧
(mechanism) Terminate only the verified exclusively retired nonproduction instance with gcloud compute instances delete INSTANCE --zone=ZONE under the approved disk-preservation policy. ⟦D.f6 D:tb3⟧
(mechanism) Preserve the active release’s referenced images and required model/preprocessing artifacts; removing a retired container is not authorization to delete shared artifacts. ⟦D.f7 D:tb4⟧
(mechanism) Verify the active serving release remains healthy with a bounded readiness/prediction check, and inspect the inventory to confirm approved retired resources are absent. ⟦D.f8 D:tb4⟧
(mechanism) Write one audit record containing verified ownership, active/retired identities, authorized actions, retained artifacts and credential non-disclosure checks. ⟦D.f9 D:tb4⟧
(misconception) Removing a retired container is not authorization to delete shared artifacts. Cleanup follows verified ownership, permitted scope and lifecycle state while preserving the active serving release. ⟦D.f1 D.f10 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D.f8 D.f9 D:tb2 D:tb3 D:tb4 D:tb5⟧

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: yaml.load with an unsafe loader
· fixtures.captured_output: stop completed: inference-lab --zone=lab-zone-a
· fixtures.captured_output: stop completed: inference-lab --zone=lab-zone-a
· fixtures.captured_output: stop completed: inference-lab --zone=lab-zone-a
· fixtures.captured_output: stop completed: inference-lab --zone=lab-zone-a
· fixtures.captured_output: stop completed: inference-lab --zone=lab-zone-a
· fixtures.captured_output: stop completed: inference-lab --zone=lab-zone-a
· fixtures.captured_output: stop completed: inference-lab --zone=lab-zone-a
· fixtures.captured_output: stop completed: inference-lab --zone=lab-zone-a
· fixtures.captured_output: stop completed: inference-lab --zone=lab-zone-a
· fixtures.captured_output: stop completed: inference-lab --zone=lab-zone-a