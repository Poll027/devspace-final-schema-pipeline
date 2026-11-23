# EVALUATOR PACKET — Metrics and acceptance (mle.tile.019_020)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.task_metric_selection — Select task-appropriate classification or regression metrics
B = mle.model_acceptance_criteria — Define measurable model acceptance criteria from task objectives

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=3
  warn: mle.tile.019_020.s01: prose block without lineage.fact_ids
  warn: mle.tile.019_020.s06: prose block without lineage.fact_ids
  warn: plan: mle.tile.019_020.s05 was planned to measure mle.task_metric_selection#assessment:choose_regression_metric_by_error_consequences but its interaction does not

## SOURCE FACTS — A (mle.task_metric_selection)   objective: Choose an evaluation measure whose conditioning population and error consequences match the task.
A.f1: Select classification metrics in relation to task consequences, class balance and the costs of false positives and false negatives, rather than relying on raw accuracy alone.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f2: Precision = TP/(TP+FP) is the proportion of predicted positives that are actual positives, while recall = TP/(TP+FN) is the proportion of actual positives detected.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f3: For regression, mean absolute error averages absolute prediction errors and mean squared error averages squared errors; the latter increases the influence of large errors.   [sources: scikit_learn_user_guide#modules/model_evaluation.html — 3.4.6 Regression metrics]
A.f4: Class prevalence is the proportion of actual positives in the validation population and helps interpret metrics from that population.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f5: Conditional frequencies from a validation confusion table describe outcomes in that cohort; they do not establish that a model’s individual probability scores are calibrated.   [sources: scikit_learn_user_guide#modules/calibration.html — 1.16 Probability calibration]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Metrics and Acceptance Criteria.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.prediction_task_definition. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (spreadsheet): Use the supplied late-order validation counts TP=12, FP=3, FN=8 and TN=77 to calculate precision, recall and class prevalence. Express precision and recall as conditional probabilities with their conditioning populations identified. Given a task consequence statement that prioritizes catching actual late orders over avoiding unnecessary alerts, select and justify one classification metric without claiming individual probability-score calibration.  SUCCESS: Precision is 12/15 = 0.80, interpreted as P(actual positive | predicted positive); recall is 12/20 = 0.60, interpreted as P(predicted positive | actual positive); class prevalence is 20/100 = 0.20. Recall is selected because missed late orders carry the stated greater consequence, rather than because of raw accuracy. The justification states that these validation-cohort frequencies do not establish calibration of individual probability scores.
ASSESSMENT ANCHOR: choose_classification_metric_by_error_consequences facts=['f1', 'f2', 'f4']
ASSESSMENT ANCHOR: choose_regression_metric_by_error_consequences facts=['f3']
ASSESSMENT ANCHOR: interpret_cohort_metrics_without_claiming_score_calibration facts=['f2', 'f4', 'f5']

## SOURCE FACTS — B (mle.model_acceptance_criteria)   objective: Precommit measurable cost, predictive and operating limits for accepting a model.
B.f1: State a measurable predictive-quality acceptance requirement before comparing candidates, along with the supplied deployment compatibility requirements.   [sources: google_mlops_pipelines#Data and model validation]
B.f2: Use the supplied error costs and deployment class probabilities as fixed decision inputs rather than choosing them after seeing which candidate benefits.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
B.f3: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
B.f4: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
B.f5: An expected-cost requirement can be stated as computed expected cost <= the predeclared permitted bound; operating limits remain separate eligibility conditions.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Metrics and Acceptance Criteria.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.prediction_task_definition, mle.task_metric_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (formula): Write a precommitted acceptance contract for the order prediction task using supplied deployment probabilities, error costs, conditional error probabilities, a permitted expected-cost bound, and operating limits. State the zero-cost assumption for correct predictions, calculate expected error cost, and express predictive acceptance as an inequality separate from each supplied operating requirement.  SUCCESS: The contract fixes all supplied decision inputs before candidate results are compared. Using deployment probabilities 0.80 and 0.20, FPR 0.10, FNR 0.20, and error costs 1 and 5, it calculates expected error cost as 0.28 and states the predeclared requirement expected error cost <= 0.30. It records each supplied operating limit independently, without inventing a latency limit or treating predictive acceptance as overall eligibility. It identifies the conditioning denominators for FPR and FNR and marks a rate unresolved if its conditioning group is empty.
ASSESSMENT ANCHOR: precommit_quality_and_operating_requirements facts=['f1', 'f2']
ASSESSMENT ANCHOR: calculate_conditioned_error_rates_and_identify_undefined_rates facts=['f3']
ASSESSMENT ANCHOR: express_expected_error_cost_acceptance_with_separate_operating_limits facts=['f2', 'f4', 'f5']

## DATA ASSETS USED
ds.acceptance_contract: Precommitted predictive contract — columns: deployment_negative_probability(numerical), deployment_positive_probability(numerical), cost_FP(numerical), cost_FN(numerical), correct_prediction_cost(numerical), expected_cost_bound(numerical), selection_rule(categorical), tie_rule(categorical), empty_group_rule(categorical), ddof(numerical), operating_limit(numerical)
   [0.8,0.2,1,5,0,0.3,"minimum expected cost among matched eligible records","first in declared order","undefined rate; ineligible when required",0,null]
ds.acceptance_terms: Expected-cost contributions by actual class — columns: actual_label(categorical,digits-as-label), deployment_class_probability(numerical), conditional_error_rate(numerical), error_cost(numerical), conditioning_count(numerical), weighted_contribution(numerical)
   [0,0.8,0.1,1,80,0.08000000000000002]
   [1,0.2,0.2,5,20,0.20000000000000004]
   variant v.empty_acceptance_positive: 3 ops; planted: 
ds.confusion_counts: Late-order confusion cells — columns: outcome(categorical), actual_label(categorical,digits-as-label), predicted_label(categorical,digits-as-label), count(numerical)
   ["TP",1,1,12]
   ["FP",0,1,3]
   ["FN",1,0,8]
   ["TN",0,0,77]
ds.metric_summary: Confusion-table denominators and computed metrics — columns: cohort_id(identifier), TP(numerical), FP(numerical), FN(numerical), TN(numerical), actual_positive_count(numerical), actual_negative_count(numerical), cohort_count(numerical), precision(numerical), recall(numerical), validation_prevalence(numerical), FPR(numerical), FNR(numerical), expected_error_cost(numerical)
   ["metric_example",12,3,8,77,20,80,100,0.8,0.6,0.2,0.0375,0.4,0.43000000000000005]
ds.regression_error_summary: Regression error averages — columns: MAE(numerical), MSE(numerical)
   [2.0,5.0]
ds.regression_errors: Two regression residuals — columns: observation_id(identifier), error(numerical), absolute_error(numerical), squared_error(numerical)
   ["reg_error_1",1,1,1]
   ["reg_error_2",3,3,9]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose a task-compatible training loss; Choose practical mitigations for documented subgroup-performance risks; Compare model candidates against a baseline using validation evidence before freezing the choice; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Control random seeds for reproducible training comparisons; Define a neural network with task-compatible layers and activations; Define measurable model acceptance criteria from task objectives; Diagnose training failures from loss and gradient behavior; Document model limitations and foreseeable misuse under an existing risk policy; Establish a simple reference prediction baseline; Evaluate important data slices for subgroup performance gaps; Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline; Fit and predict with a bounded scikit-learn baseline workflow; Implement the minibatch forward, backward and optimizer-step loop; Inspect prediction errors

## LESSON, in learner order

### s01 · explainer · Cohort evidence is bounded
(intro) Few total late-order mistakes can still hide missed positives. Choose the metric for the task’s error consequences and conditioning population, not accuracy alone. ⟦A:tb1⟧
(definition) Class balance and false-positive/false-negative costs matter when choosing classification metrics. Precision, TP/(TP+FP), asks how many predicted positives are actual positives. Recall, TP/(TP+FN), asks how many actual positives were detected. For regression, MAE averages absolute errors; MSE averages squared errors, giving larger errors more influence. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Validation prevalence is actual positives divided by the validation population. Use it to interpret cohort metrics. Confusion-table conditional frequencies describe this cohort; they do not demonstrate calibration of individual probability scores. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.confusion_counts cols=['outcome', 'actual_label', 'predicted_label', 'count'] ] caption: Late-order confusion cells: predicted-positive denominator 15; actual-positive denominator 20; cohort denominator 100.
[TABLE ds.metric_summary cols=['actual_positive_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence'] ] caption: Confusion-table denominators and computed metrics
[TABLE ds.regression_errors cols=['observation_id', 'error', 'absolute_error', 'squared_error'] ] caption: Two regression residuals
[TABLE ds.regression_error_summary cols=['MAE', 'MSE'] ] caption: Regression error averages

### s02 · explainer · Read the denominators
(example) Read the confusion cells with their actual and predicted labels. Precision uses predicted positives as its denominator; recall uses actual positives. Prevalence uses the whole validation cohort. The separate regression tables show absolute and squared errors and their averages. Keep task consequences beside the numbers: these cohort summaries do not prove that an individual probability score is calibrated. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4⟧

### s03 · explainer · Do not swap the groups
(misconception) Precision and recall use different denominators. Neither replaces the other, and cohort frequencies do not prove probability-score calibration. ⟦A.f2 A.f5 A:tb5⟧

### s04 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.
QUESTION [choice, intro, grading=client] Precision is 0.80 in this cohort. A separate regression task gives unusually large prediction errors greater consequence. Which response correctly interprets precision and chooses the regression metric?
  ✔ o1: Among predicted late orders, 80% are actually late; this does not establish individual-score calibration. Choose MSE for the regression task because squaring gives large errors more influence.
      why: Precision conditions on predicted positives; squaring gives large regression errors more influence.
  ✘ o2: Among actually late orders, 80% are detected; this does not establish individual-score calibration. Choose MSE because squaring gives large errors more influence.
      why: Detection among actual positives is recall, not precision.
  ✘ o3: Among predicted late orders, 80% are actually late; this does not establish individual-score calibration. Choose MAE because absolute-error averaging gives large errors more influence than squaring.
      why: For the stated priority, squaring, not absolute-error averaging, increases large errors’ influence.
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r01
  MEASURES: A:interpret_cohort_metrics_without_claiming_score_calibration(f2,f4,f5); A:choose_regression_metric_by_error_consequences(f3)   anchors=['assessment:interpret_cohort_metrics_without_claiming_score_calibration', 'assessment:choose_regression_metric_by_error_consequences']
  taught-before-tested: A.f2←s01; A.f4←s01; A.f5←s01; A.f3←s01

### s05 · hands_on · Calculate from the supplied evidence
 — Use the supplied dataset and fixed contract. Keep the conditioning population explicit when entering the requested formula.
QUESTION [formula_entry, core, grading=client] Missed late orders have the greater consequence. In AZ1 enter one concatenating formula; helper-cell calculations are permitted. Required fields:
- Precision, recall and actual-positive prevalence from the counts (two decimal places).
- Both conditioning populations.
- Chosen metric and justification for the stated consequence.
- Calibration limitation.

Prescribed output format: precision=P(actual positive|predicted positive): <value>; recall=P(predicted positive|actual positive): <value>; prevalence: <value>; choose <metric>: <explanation>; cohort ratios do not establish individual-score calibration. Choose precision or recall. For the explanation field, use exactly ‘missed late orders have the greater consequence’. Retain the numeric fields, conditioning labels and output format.
  [unrendered interaction type formula_entry] public={"prompt":"Missed late orders have the greater consequence. In AZ1 enter one concatenating formula; helper-cell calculations are permitted. Required fields:\n- Precision, recall and actual-positive prevalence from the counts (two decimal places).\n- Both conditioning populations.\n- Chosen metric and justification for the stated consequence.\n- Calibration limitation.\n\nPrescribed output format: precision=P(actual positive|predicted positive): <value>; recall=P(predicted positive|actual positive): <value>; prevalence: <value>; choose <metric>: <explanation>; cohort ratios do not establish individual-score calibration. Choose precision or recall. For the explanation field, use exactly ‘missed late orders have the greater consequence’. Retain the numeric fields, conditioning labels and output format.","asset_ref":{"asset_id":"ds.confusion_counts"},"sheet_name":"Evidence","target_cell":"AZ grading={"reference_formula":"=\"precision=P(actual positive|predicted positive): \"&TEXT(D2/(D2+D3),\"0.00\")&\"; recall=P(predicted positive|actual positive): \"&TEXT(D2/(D2+D4),\"0.00\")&\"; prevalence: \"&TEXT((D2+D4)/SUM(D2:D5),\"0.00\")&\"; choose recall: missed late orders have the greater consequence; cohort ratios do not establish individual-score calibration.\"","expected_value":"precision=P(actual positive|predicted positive): 0.80; recall=P(predicted positive|actual positive): 0.60; prevalence: 0.20; choose recall: missed late orders have the greater consequence; cohort ratios do not establish individual-score calibration.","forbid_hardcoded_values":true}
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Precision conditions on predicted positives: TP+FP. Recall conditions on actual positives: TP+FN. Prevalence uses all four confusion cells.', 'Greater consequences for missed actual positives favor recall; cohort ratios do not establish individual-score calibration.']  remediation→r02
  MEASURES: A:choose_classification_metric_by_error_consequences(f1,f2,f4); A:interpret_cohort_metrics_without_claiming_score_calibration(f2,f4,f5)   anchors=['practice', 'assessment:choose_classification_metric_by_error_consequences', 'assessment:interpret_cohort_metrics_without_claiming_score_calibration']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f4←s01; A.f2←s01; A.f4←s01; A.f5←s01

### s06 · explainer · Cost and eligibility
(intro) Declare quality and operating requirements before inspecting candidate results. The favored candidate must not determine the acceptance contract. ⟦B:tb1⟧
(definition) Precommit a measurable predictive-quality requirement and the supplied deployment compatibility requirements. Keep supplied error costs and deployment class probabilities fixed. FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. A rate with an empty conditioning group is undefined. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) With zero cost for correct predictions, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Require expected cost <= the predeclared bound. Operating limits are separate eligibility conditions. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.acceptance_terms cols=['actual_label', 'deployment_class_probability', 'conditional_error_rate', 'error_cost', 'conditioning_count', 'weighted_contribution'] ] caption: Expected-cost contributions by actual class
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract
[TABLE computed result ] caption: Sum the cost terms; operating eligibility remains separate.
  produced by sql: SELECT SUM(t.weighted_contribution) AS expected_cost, c.expected_cost_bound, SUM(t.weighted_contribution) <= c.expected_cost_bound AS predictive_bound_met, c.operating_limit AS separate_operating_limit FROM terms t CROSS JOIN contract c GROUP BY c.expected_cost_bound, c.operating_limit
  result columns=['expected_cost', 'expected_cost_bound', 'predictive_bound_met', 'separate_operating_limit'] rows(1)=[[0.28,0.3,true,null]]

### s07 · explainer · Inspect the acceptance contract
(example) The cost-term table keeps the actual-class conditioning counts, supplied deployment probabilities and error costs separate. Add the weighted contributions and compare with the fixed bound in the acceptance contract. Passing that predictive requirement does not override a latency limit. An empty actual-positive group leaves FNR undefined; do not substitute zero or change deployment probabilities to favor a candidate. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb4⟧

### s08 · explainer · Cost is not blanket acceptance
(misconception) Low cost is not blanket acceptance. Keep predictive and operating eligibility separate, and do not change supplied probabilities or costs to favor a candidate. ⟦B.f1 B.f2 B.f5 B:tb5⟧

### s09 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.
QUESTION [choice, core, grading=client] A candidate passes the predeclared expected-cost bound but fails a separate supplied operating requirement. What is the acceptance conclusion?
  ✔ o1: Predictive cost passes, but the failed operating requirement excludes deployment eligibility.
      why: Predictive and operating requirements remain separate.
  ✘ o2: The passing predictive cost overrides the operating failure.
      why: Passing expected cost does not waive an operating condition.
  ✘ o3: Change deployment class probabilities until the operating failure is compensated.
      why: Deployment probabilities are fixed decision inputs, not adjustments made to rescue a candidate.
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r03
  MEASURES: B:express_expected_error_cost_acceptance_with_separate_operating_limits(f2,f4,f5)   anchors=['assessment:express_expected_error_cost_acceptance_with_separate_operating_limits']
  taught-before-tested: B.f2←s06; B.f4←s06; B.f5←s06

### s10 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.
QUESTION [code_exercise, stretch, grading=client] Complete the requested spreadsheet formulas using the supplied rates, conditioning counts and fixed acceptance contract.

The supplied deployment probabilities, costs, rates and permitted bound are fixed before comparison; correct predictions have zero cost. On sheet terms, put guarded FPR in H1 (actual-negative denominator E2), guarded FNR in H2 (actual-positive denominator E3), expected cost in H3, and the predictive inequality result H3 <= the bound in H4. Use "undefined" for rates/cost with empty conditioning groups and FALSE for unresolved predictive acceptance. Put the two conditioning counts in H5/H6, the correct-prediction cost in H7, and bound in H8. In H9 retain the supplied operating limit independently; when none is supplied write "no numeric operating limit supplied; predictive acceptance is not overall eligibility". Do not invent a latency limit.
  runtime={'kind': 'spreadsheet', 'version': '3.4.0'} constraints.allowed=['IF', 'AND', 'ISBLANK', 'relative cell references', 'cross-sheet references', '+ - * /', 'comparison operators', 'text in quotes', 'TRUE / FALSE', 'numbers'] blocked=0 items
  file contract.sheet [editable]:
// Fixed contract and rates are supplied; complete the formulas on sheet terms.

  SOLUTION contract.sheet:
// Fixed contract and rates are supplied; complete the formulas on sheet terms.
H1: =IF(E2>0,C2,"undefined")
H2: =IF(E3>0,C3,"undefined")
H3: =IF(AND(E2>0,E3>0),B2*H1*D2+B3*H2*D3,"undefined")
H4: =IF(AND(E2>0,E3>0),H3<=contract!F2,FALSE)
H5: =E2
H6: =E3
H7: =contract!E2
H8: =contract!F2
H9: =IF(ISBLANK(contract!K2),"no numeric operating limit supplied; predictive acceptance is not overall eligibility",contract!K2)

  test t1 (cell_equals, visible=None): {"cell":"H1","expected":0.1} | on-fail: Keep rates, fixed contract inputs and operating limits separate.
  test t2 (cell_equals, visible=None): {"cell":"H2","expected":0.2} | on-fail: Keep rates, fixed contract inputs and operating limits separate.
  test t3 (cell_equals, visible=None): {"cell":"H3","expected":0.28} | on-fail: Keep rates, fixed contract inputs and operating limits separate.
  test t4 (cell_equals, visible=None): {"cell":"H4","expected":true} | on-fail: Keep rates, fixed contract inputs and operating limits separate.
  test t5 (cell_equals, visible=None): {"cell":"H5","expected":80} | on-fail: Keep rates, fixed contract inputs and operating limits separate.
  test t6 (cell_equals, visible=None): {"cell":"H6","expected":20} | on-fail: Keep rates, fixed contract inputs and operating limits separate.
  test t7 (cell_equals, visible=None): {"cell":"H7","expected":0} | on-fail: Keep rates, fixed contract inputs and operating limits separate.
  test t_contract_operating (range_equals, visible=None): {"range":"H8:H9","expected":[[0.3],["no numeric operating limit supplied; predictive acceptance is not overall eligibility"]]} | on-fail: Retain the supplied bound and separate operating-limit conclusion.
  provenance: {"runtime":"hyperformula","runtime_version":"3.4.0","solution_sha256":"7e7e306dcfcdd32beb99dd1dec807d83370f2570ebe26b6e803ce308ec812e92","tests_passed":8}
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r04
  MEASURES: B:precommit_quality_and_operating_requirements(f1,f2); B:calculate_conditioned_error_rates_and_identify_undefined_rates(f3); B:express_expected_error_cost_acceptance_with_separate_operating_limits(f2,f4,f5)   anchors=['practice', 'assessment:precommit_quality_and_operating_requirements', 'assessment:calculate_conditioned_error_rates_and_identify_undefined_rates', 'assessment:express_expected_error_cost_acceptance_with_separate_operating_limits']
  taught-before-tested: B.f1←s06; B.f2←s06; B.f3←s06; B.f2←s06; B.f4←s06; B.f5←s06

### s11 · recap · Keep these distinctions
(takeaway) Choose metrics by task consequences and their denominators. Cohort frequencies do not prove score calibration. Precommit quality, costs and deployment probabilities; keep operating eligibility separate and empty-group rates undefined. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 B.f1 B.f2 B.f3 B.f4 B.f5 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Up next: Establish a simple training-fitted reference baseline.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: the check — choose the question
(misconception) Contrast predicted positives with actual positives: precision starts with the first group, recall with the second. Neither group ratio demonstrates score calibration. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
(definition) Class balance and false-positive/false-negative costs matter when choosing classification metrics. Precision, TP/(TP+FP), asks how many predicted positives are actual positives. Recall, TP/(TP+FN), asks how many actual positives were detected. For regression, MAE averages absolute errors; MSE averages squared errors, giving larger errors more influence. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Validation prevalence is actual positives divided by the validation population. Use it to interpret cohort metrics. Confusion-table conditional frequencies describe this cohort; they do not demonstrate calibration of individual probability scores. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.confusion_counts cols=['outcome', 'actual_label', 'predicted_label', 'count'] ] caption: Late-order confusion cells
### r02 · Revisit: the practice — choose the question
(misconception) Contrast predicted positives with actual positives: precision starts with the first group, recall with the second. Neither group ratio demonstrates score calibration. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
(definition) Class balance and false-positive/false-negative costs matter when choosing classification metrics. Precision, TP/(TP+FP), asks how many predicted positives are actual positives. Recall, TP/(TP+FN), asks how many actual positives were detected. For regression, MAE averages absolute errors; MSE averages squared errors, giving larger errors more influence. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Validation prevalence is actual positives divided by the validation population. Use it to interpret cohort metrics. Confusion-table conditional frequencies describe this cohort; they do not demonstrate calibration of individual probability scores. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.confusion_counts cols=['outcome', 'actual_label', 'predicted_label', 'count'] ] caption: Late-order confusion cells
### r03 · Revisit: the check — precommit acceptance
(misconception) Contrast passing the predictive-cost bound with being deployment-eligible: a separate operating failure still excludes the candidate. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3⟧
(definition) Precommit a measurable predictive-quality requirement and the supplied deployment compatibility requirements. Keep supplied error costs and deployment class probabilities fixed. FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. A rate with an empty conditioning group is undefined. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) With zero cost for correct predictions, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Require expected cost <= the predeclared bound. Operating limits are separate eligibility conditions. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.acceptance_terms cols=['actual_label', 'deployment_class_probability', 'conditional_error_rate', 'error_cost', 'conditioning_count', 'weighted_contribution'] ] caption: Expected-cost contributions by actual class
### r04 · Revisit: the practice — precommit acceptance
(misconception) Contrast passing the predictive-cost bound with being deployment-eligible: a separate operating failure still excludes the candidate. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3⟧
(definition) Precommit a measurable predictive-quality requirement and the supplied deployment compatibility requirements. Keep supplied error costs and deployment class probabilities fixed. FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. A rate with an empty conditioning group is undefined. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) With zero cost for correct predictions, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Require expected cost <= the predeclared bound. Operating limits are separate eligibility conditions. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.acceptance_terms cols=['actual_label', 'deployment_class_probability', 'conditional_error_rate', 'error_cost', 'conditioning_count', 'weighted_contribution'] ] caption: Expected-cost contributions by actual class

## OTHER CONTENT (fields without a dedicated renderer)
· grading.reference_formula: ="precision=P(actual positive|predicted positive): "&TEXT(D2/(D2+D3),"0.00")&"; recall=P(predicted positive|actual positive): "&TEXT(D2/(D2+D4),"0.00")&"; prevalence: "&TEXT((D2+D4)/SUM(D2:D5),"0.00")&"; choose recall: missed late orders have the greater consequence; cohort ratios do not establish individual-score calibration."

=========

# EVALUATOR PACKET — Establish a modeling baseline (mle.tile.021_023)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.reference_baseline — Establish a simple reference prediction baseline
B = mle.model_approach_decision — Justify classical versus neural modeling using validation quality, latency and cost evidence
C = mle.sklearn_baseline_workflow — Fit and predict with a bounded scikit-learn baseline workflow

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=7
  warn: mle.tile.021_023.s01: prose block without lineage.fact_ids
  warn: mle.tile.021_023.s05/ix.mle.tile.021_023.s05: ADVISORY — syntax descriptors with no detector: ['None', 'accuracy_score', 'arithmetic operators', 'array equality comparisons', 'dictionary literals', 'elementwise Boolean &', 'function parameters', 'if and else', 'len', 'numeric and string literals']
  warn: mle.tile.021_023.s06: prose block without lineage.fact_ids
  warn: mle.tile.021_023.s10: prose block without lineage.fact_ids
  warn: mle.tile.021_023.s14/ix.mle.tile.021_023.s14: ADVISORY — syntax descriptors with no detector: ['None for undefined quantities', 'arithmetic operators +, *, and /', 'array comparisons with binary labels 0 and 1', 'assert statements', 'def with parameters and return', 'dictionary construction for returned results', 'elementwise boolean conjunction with &', 'if and else']
  warn: plan: mle.tile.021_023.s08 was planned to measure mle.model_approach_decision#assessment:freeze_supplied_approach_without_new_fitting_or_protected_test_access but its interaction does not
  warn: plan: mle.tile.021_023.s14 was planned to measure mle.sklearn_baseline_workflow#assessment:reuse_fitted_preprocessing_for_validation_predictions but its interaction does not

## SOURCE FACTS — A (mle.reference_baseline)   objective: Train and freeze a simple reference, then evaluate its declared validation quantities.
A.f1: DummyClassifier supplies simple reference rules such as most_frequent, prior and constant; DummyRegressor(strategy="mean") predicts the training-target mean.   [sources: scikit_learn_user_guide#modules/model_evaluation.html — 3.4.8 Dummy estimators]
A.f2: Fit the reference estimator on training inputs and targets, then freeze it and call predict on the separate validation cohort.   [sources: scikit_learn_user_guide#modules/model_evaluation.html — 3.4.8 Dummy estimators]
A.f3: Measure the predeclared validation metric on the baseline’s predictions and actual targets, rather than reporting its training-only result.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f4: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
A.f5: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
A.f6: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f7: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
A.f8: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
A.f9: For a classification reference, report the training target-class count divided by the training total, without replacing it with validation or protected-test prevalence.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Establish a Modeling Baseline.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.prediction_task_definition, mle.task_metric_selection, mle.deployment_matched_splits. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function with learner-written imports that establishes a most-frequent classification reference from the supplied training cohort. Calculate the training target mean, population standard deviation and class proportions. Fit once on training, predict the separate validation cohort, and return its predeclared accuracy, conditional error rates and expected error cost using the supplied deployment probabilities and error costs. Preserve the measured validation reference without accessing protected test data.  SUCCESS: The function reports training positive prevalence 0.20 and negative prevalence 0.80 for the eight-negative, two-positive fixture. Its frozen reference predicts the training majority class for every validation observation. Accuracy uses validation predictions and actual targets; FPR and FNR use their respective actual-class denominators. Empty conditioning groups are reported as undefined, not zero, and any cost requiring an undefined rate is also reported as undefined. The returned record contains the training statistics, fixed reference rule, validation metric and applicable error-cost calculation.
ASSESSMENT ANCHOR: define_task_compatible_reference facts=['f1', 'f9']
ASSESSMENT ANCHOR: fit_training_only_and_freeze_reference facts=['f2', 'f8']
ASSESSMENT ANCHOR: measure_predeclared_validation_metric facts=['f3']
ASSESSMENT ANCHOR: justify_reference_with_training_target_statistics facts=['f4', 'f5', 'f9']
ASSESSMENT ANCHOR: calculate_conditional_error_rates_and_expected_cost facts=['f6', 'f7']

## SOURCE FACTS — B (mle.model_approach_decision)   objective: Select a supplied modeling approach from matched quality, operating and ownership evidence.
B.f1: Compare alternatives on the same intended evaluation task and cohort, and check model quality and deployment compatibility before promotion.   [sources: google_mlops_pipelines#Data and model validation]
B.f2: Different inference options have different latency, scale and cost characteristics, so the supplied operating constraints affect eligibility.   [sources: sagemaker_model_deployment#Deploy models for inference]
B.f3: Reject supplied alternatives violating precommitted quality or operating limits, then choose among eligible alternatives using the fixed decision rule.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
B.f4: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
B.f5: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
B.f6: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
B.f7: A custom classical or neural model leaves task-model implementation and training choices with the model owner, while a managed service can supply training/hosting infrastructure; compare maintenance responsibility as well as predictive and operating evidence.   [sources: sagemaker_developer_guide#how-it-works-mlconcepts.html — The machine learning workflow]
B.f8: Address classical-versus-neural and custom-versus-managed trade-offs from matched records, without fitting new alternatives to manufacture comparison evidence.   [sources: google_mlops_pipelines#Data and model validation]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Establish a Modeling Baseline.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection, mle.model_acceptance_criteria, mle.prediction_task_definition. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (spreadsheet): Use a supplied spreadsheet containing matched validation confusion counts and operating records for a custom classical model, a custom neural model and a managed ML service. Verify the shared task and cohort; derive FPR, FNR and expected error cost using supplied deployment class probabilities and false-positive and false-negative costs, with zero cost for correct predictions. Apply precommitted quality, latency, scale, training-cost, serving-cost, maintenance and deployment-compatibility limits, then freeze one eligible alternative using the supplied fixed decision rule. Justify both classical-versus-neural and custom-versus-managed trade-offs without fitting alternatives or accessing protected test data.  SUCCESS: The completed spreadsheet uses FP/(FP+TN) and FN/(FN+TP), marks rates with empty conditioning groups as undefined rather than zero, and calculates expected error cost as P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN wherever rates are defined. Eligibility decisions follow every supplied limit; no undefined required rate is treated as evidence of passing a limit. The frozen selection follows the fixed decision rule among eligible alternatives, with a rationale citing matched quality, operating evidence and maintenance responsibility across all three records. No new fitting or protected-test observations are used.
ASSESSMENT ANCHOR: verify_matched_task_cohort_and_deployment_compatibility facts=['f1']
ASSESSMENT ANCHOR: derive_conditional_error_rates_and_identify_undefined_rates facts=['f4']
ASSESSMENT ANCHOR: calculate_prevalence_weighted_expected_error_cost facts=['f4', 'f5']
ASSESSMENT ANCHOR: reject_ineligible_alternatives_and_apply_fixed_decision_rule facts=['f2', 'f3']
ASSESSMENT ANCHOR: justify_classical_neural_and_custom_managed_tradeoffs facts=['f7', 'f8']
ASSESSMENT ANCHOR: freeze_supplied_approach_without_new_fitting_or_protected_test_access facts=['f6', 'f8']

## SOURCE FACTS — C (mle.sklearn_baseline_workflow)   objective: Fit a bounded classical estimator and compare its validation predictions with the fixed reference.
C.f1: For the binary classification baseline, use from sklearn.linear_model import LogisticRegression; estimator = LogisticRegression(random_state=0); estimator.fit(X_train, y_train), with numeric X_train of shape (n_samples, n_features) and aligned class-label y_train of shape (n_samples,).   [sources: scikit_learn_user_guide#https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html — Examples; fit; predict]
C.f2: Obtain predictions with estimator.predict(X_validation) and compare them against the corresponding y_validation observations.   [sources: scikit_learn_user_guide#https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html — Examples; fit; predict]
C.f3: When training used fitted preprocessing, predict through the fitted pipeline so validation inputs receive the same feature representation.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.1 Inconsistent preprocessing]
C.f4: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
C.f5: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Establish a Modeling Baseline.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.numpy_shape_dtype, mle.deployment_matched_splits, mle.task_metric_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function and its required imports within the supplied runtime scaffolding. Verify the dimensions and declared observation alignment of the six-order, two-feature training fixture and corresponding validation inputs. Fit the declared LogisticRegression baseline, obtain validation predictions through the fitted pipeline when preprocessing is present, and calculate binary error counts, conditional error rates and expected error cost using supplied deployment probabilities and error costs.  SUCCESS: The function verifies X_train has shape (6, 2), y_train has shape (6,), and validation inputs and labels have corresponding observations. It fits the declared estimator, returns aligned validation predictions, calculates FPR and FNR using the correct conditioning groups, and computes expected error cost when both rates are defined. Empty conditioning groups are reported as undefined rather than assigned a rate or used to produce a numerical expected cost.
ASSESSMENT ANCHOR: fit_baseline_with_aligned_numeric_inputs facts=['f1']
ASSESSMENT ANCHOR: obtain_observation_aligned_validation_predictions facts=['f2']
ASSESSMENT ANCHOR: reuse_fitted_preprocessing_for_validation_predictions facts=['f3']

## DATA ASSETS USED
ds.acceptance_contract: Precommitted predictive contract — columns: deployment_negative_probability(numerical), deployment_positive_probability(numerical), cost_FP(numerical), cost_FN(numerical), correct_prediction_cost(numerical), expected_cost_bound(numerical), selection_rule(categorical), tie_rule(categorical), empty_group_rule(categorical), ddof(numerical), operating_limit(numerical)
   [0.8,0.2,1,5,0,0.3,"minimum expected cost among matched eligible records","first in declared order","undefined rate; ineligible when required",0,null]
ds.approach_records: Classical, neural, and managed operating records — columns: alternative_id(identifier), model_family(categorical), delivery_mode(categorical), cohort_id(identifier), TP(numerical), FP(numerical), FN(numerical), TN(numerical), actual_positive_count(numerical), actual_negative_count(numerical), cohort_count(numerical), precision(numerical), recall(numerical), validation_prevalence(numerical), FPR(numerical), FNR(numerical), expected_error_cost(numerical), latency_requirement_met(categorical), scale_requirement_met(categorical), training_cost_requirement_met(categorical), serving_cost_requirement_met(categorical), maintenance_requirement_met(categorical), deployment_compatibility_met(categorical), maintenance_responsibility(text)
   ["custom_classical","classical","custom","orders_100",16,8,4,72,20,80,100,0.6666666666666666,0.8,0.2,0.1,0.2,0.28,true,true,true,true,true,true,"owner maintains task model and infrastructure"]
   ["custom_neural","neural","custom","orders_100",16,4,4,76,20,80,100,0.8,0.8,0.2,0.05,0.2,0.24000000000000005,false,true,true,true,true,true,"owner maintains task model and infrastructure"]
   ["managed_service","classical","managed","orders_100",16,12,4,68,20,80,100,0.5714285714285714,0.8,0.2,0.15,0.2,0.32000000000000006,true,true,true,true,true,true,"service supplies training or hosting infrastructure; owner retains custom task-model choices"]
ds.orders_train: Six-order estimator training inputs — columns: observation_id(identifier), feature_1(numerical), feature_2(numerical), y_train(categorical,digits-as-label)
   ["train_1",-3.0,0.0,0]
   ["train_2",-2.0,2.0,0]
   ["train_3",-1.0,4.0,0]
   ["train_4",0.0,1.0,1]
   ["train_5",1.0,3.0,1]
   ["train_6",2.0,0.0,1]
ds.orders_validation: Held-out aligned estimator inputs — columns: observation_id(identifier), feature_1(numerical), feature_2(numerical), y_validation(categorical,digits-as-label)
   ["validation_1",-2.75,0.0,0]
   ["validation_2",-1.75,3.0,0]
   ["validation_3",-0.75,1.0,0]
   ["validation_4",0.25,4.0,1]
   ["validation_5",1.25,2.0,1]
   ["validation_6",2.25,0.0,1]
   variant v.validation_no_positives: 1 ops; planted: 
   variant v.validation_no_negatives: 1 ops; planted: 
   variant v.validation_bad_alignment: 1 ops; planted: 
ds.reference_train: Reference-only training cohort — columns: observation_id(identifier), feature_1(numerical), y_train(categorical,digits-as-label)
   ["ref_train_1",0.0,0]
   ["ref_train_2",1.0,0]
   ["ref_train_3",2.0,0]
   ["ref_train_4",3.0,0]
   ["ref_train_5",4.0,0]
   ["ref_train_6",5.0,0]
   ["ref_train_7",6.0,0]
   ["ref_train_8",7.0,0]
ds.regression_targets: Separate mean-reference targets — columns: observation_id(identifier), target(numerical)
   ["reg_train_1",2]
   ["reg_train_2",4]
   ["reg_train_3",6]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose a task-compatible training loss; Choose practical mitigations for documented subgroup-performance risks; Compare model candidates against a baseline using validation evidence before freezing the choice; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Control random seeds for reproducible training comparisons; Define a neural network with task-compatible layers and activations; Diagnose training failures from loss and gradient behavior; Diagnose training memory exhaustion; Document model limitations and foreseeable misuse under an existing risk policy; Evaluate important data slices for subgroup performance gaps; Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline; Fit and predict with a bounded scikit-learn baseline workflow; Implement the minibatch forward, backward and optimizer-step loop; Inspect prediction errors for recurring failure mode

## LESSON, in learner order

### s01 · explainer · Statistics and conditioning
(intro) Establish a simple reference before judging more elaborate predictions. Fit it on training observations and evaluate its frozen predictions on validation. ⟦A:tb1⟧
(mechanism) DummyClassifier offers reference rules such as most_frequent, prior and constant. DummyRegressor(strategy="mean") predicts the training-target mean. Fit on training inputs and targets, freeze the estimator, then predict on separate validation observations. Report the predeclared metric against validation targets, not a training-only result. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Use np.mean(numeric_values) for the selected numeric observations’ arithmetic mean. np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root; use ddof=1 only when an N−1 divisor is required. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty conditioning groups give undefined rates. ⟦A.f4 A.f5 A.f6 A:tb3⟧
[CODE python]
import numpy as np
from sklearn.dummy import DummyClassifier, DummyRegressor

def evaluate_reference(X_train, y_train, X_validation, y_validation, p_negative, p_positive, cost_FP, cost_FN, numeric_values):
    reference = DummyClassifier(strategy="most_frequent")
    reference.fit(X_train, y_train)
    predictions = reference.predict(X_validation)
    training_positive_proportion = np.sum(y_train == 1) / len(y_train)
    training_target_mean = np.mean(numeric_values)
    training_target_std = np.std(numeric_values, ddof=0)
    FP = np.sum((y_validation == 0) & (predictions == 1))
    TN = np.sum((y_validation == 0) & (predictions == 0))
    FN = np.sum((y_validation == 1) & (predictions == 0))
    TP = np.sum((y_validation == 1) & (predictions == 1))
    FPR = FP / (FP + TN) if FP + TN else None
    FNR = FN / (FN + TP) if FN + TP else None
    expected_cost = (p_negative * FPR * cost_FP + p_positive * FNR * cost_FN
                     if FPR is not None and FNR is not None else None)
    return {
        'training_shape': X_train.shape,
        'training_label_shape': y_train.shape,
        'validation_shape': X_validation.shape,
        'predictions': predictions,
        'validation_labels': y_validation,
        'FP': FP,
        'TN': TN,
        'FN': FN,
        'TP': TP,
        'actual_negative_denominator': FP + TN,
        'actual_positive_denominator': FN + TP,
        'FPR': FPR,
        'FNR': FNR,
        'expected_cost': expected_cost,
        'training_positive_proportion': training_positive_proportion,
        'training_target_mean': training_target_mean,
        'training_target_std_ddof0': training_target_std,
    }
  annotations: []
[TABLE ds.reference_train cols=['observation_id', 'feature_1', 'y_train'] ] caption: Reference-only training cohort
[TABLE ds.regression_targets cols=['observation_id', 'target'] ] caption: Separate mean-reference targets
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract

### s02 · explainer · Keep training and test boundaries
(mechanism) With correct predictions costing zero, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations must not fit preprocessing, choose a model or tune settings: that leaks information. For a classification reference, report training target-class count/training total, not validation or protected-test prevalence. ⟦A.f7 A.f8 A.f9 A:tb4⟧

### s03 · explainer · A reference needs validation
(example) The registered training labels determine the reference rule and training class proportions. Keep those statistics separate from validation prevalence. Freeze the fitted reference before predicting on the corresponding validation inputs. Evaluate those predictions with the declared metric and cost assumptions; retain actual-class denominators and mark empty groups undefined. Training-target mean and spread describe the chosen training observations, not the held-out result. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A:tb5⟧
(misconception) A reference still needs held-out evaluation. Training proportions are not validation prevalence, and fitting or selecting with protected-test observations leaks information. ⟦A.f2 A.f3 A.f8 A:tb6⟧

### s04 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.
QUESTION [choice, intro, grading=client] The frozen reference has no actual-positive observations in one validation cohort. How should its FNR and expected error cost be recorded?
  ✔ o1: FNR is undefined; any cost requiring that rate is undefined.
      why: FNR requires a nonempty actual-positive conditioning group.
  ✘ o2: FNR is zero, so the false-negative contribution is zero.
      why: An empty denominator does not define a zero rate.
  ✘ o3: Use the training positive prevalence as the missing validation FNR.
      why: Training prevalence is not the conditional validation error rate.
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r01
  MEASURES: A:calculate_conditional_error_rates_and_expected_cost(f6,f7)   anchors=['assessment:calculate_conditional_error_rates_and_expected_cost']
  taught-before-tested: A.f6←s01; A.f7←s02

### s05 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.
QUESTION [code_exercise, core, grading=client] Select the training-target mean and population-standard-deviation operations for target_mean and target_std, and the validation-accuracy operation for validation_metric. Complete the training-positive-prevalence, training-negative-prevalence and validation-accuracy expressions. Preserve the supplied training-only reference fit, guards and result schema.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy', 'pandas', 'scikit-learn']} constraints.allowed=['import numpy as np', 'from sklearn.dummy import DummyClassifier', 'from sklearn.metrics import accuracy_score', 'def', 'return', 'variable assignment', 'function parameters', 'dictionary literals', 'numeric and string literals', 'None', 'if and else', 'arithmetic operators', 'array equality comparisons', 'elementwise Boolean &', 'np.array', 'np.mean(numeric_values)', 'np.std(numeric_values, ddof=0)', 'np.std(numeric_values, ddof=1) only when explicitly required', 'np.sum', 'len', 'DummyClassifier(strategy="most_frequent")', 'estimator.fit', 'estimator.predict', 'accuracy_score'] blocked=7 items
  file main.py [editable]:
# Supplied input loading and dependencies.
import pandas as pd

contract = pd.read_csv('acceptance_contract.csv').iloc[0]

p_negative = contract['deployment_negative_probability']

p_positive = contract['deployment_positive_probability']

cost_FP = contract['cost_FP']

cost_FN = contract['cost_FN']

bound = contract['expected_cost_bound']

train = pd.read_csv('reference_train.csv')

validation = pd.read_csv('orders_validation.csv')

X_train = train[['feature_1']].to_numpy()

y_train = train['y_train'].to_numpy()

X_validation = validation[['feature_1']].to_numpy()

y_validation = validation['y_validation'].to_numpy()

import numpy as np

from sklearn.dummy import DummyClassifier

from sklearn.metrics import accuracy_score

# Supplied evaluation scaffold. Complete the marked expressions; preserve the rest.
if __name__:
    def evaluate(X_train, y_train, X_validation, y, p_negative, p_positive, cost_FP, cost_FN):
        estimator = reference_factory(strategy="most_frequent")
        estimator.fit(X_train, y_train)
        predictions = estimator.predict(X_validation)
        FP = count_errors((y == 0) & (predictions == 1))
        TN = count_errors((y == 0) & (predictions == 0))
        FN = count_errors((y == 1) & (predictions == 0))
        TP = count_errors((y == 1) & (predictions == 1))
        negative_count = FP + TN
        positive_count = FN + TP
        FPR = None
        FNR = None
        expected_cost = None
        if negative_count > 0:
            FPR = FP / negative_count
        if positive_count > 0:
            FNR = FN / positive_count
        if negative_count > 0:
            if positive_count > 0:
                expected_cost = p_negative * FPR * cost_FP + p_positive * FNR * cost_FN
        training_mean = target_mean(y_train)
        training_std = target_std(y_train, ddof=0)
        training_positive_prevalence = None  # TODO: training positive proportion
        training_negative_prevalence = None  # TODO: training negative proportion
        validation_accuracy = None  # TODO: score validation predictions
        return {'FP': FP, 'TN': TN, 'FN': FN, 'TP': TP, 'actual_negative_count': negative_count, 'actual_positive_count': positive_count, 'FPR': FPR, 'FNR': FNR, 'expected_cost': expected_cost, 'predictions': predictions, 'rule': 'most_frequent', 'training_mean': training_mean, 'training_std': training_std, 'training_positive_prevalence': training_positive_prevalence, 'training_negative_prevalence': training_negative_prevalence, 'validation_accuracy': validation_accuracy}

# Supplied callable operations; keep these assignments unchanged.
supplied_DummyClassifier = DummyClassifier
supplied_np_sum = np.sum
supplied_np_mean = np.mean
supplied_np_std = np.std
supplied_accuracy_score = accuracy_score
reference_factory = supplied_DummyClassifier
count_errors = supplied_np_sum

# Supplied callable/value bindings.
target_mean = None  # TODO: bind the supplied operation/value
target_std = None  # TODO: bind the supplied operation/value
validation_metric = None  # TODO: bind the supplied operation/value

  SOLUTION main.py:
# Supplied input loading and dependencies.
import pandas as pd

contract = pd.read_csv('acceptance_contract.csv').iloc[0]

p_negative = contract['deployment_negative_probability']

p_positive = contract['deployment_positive_probability']

cost_FP = contract['cost_FP']

cost_FN = contract['cost_FN']

bound = contract['expected_cost_bound']

train = pd.read_csv('reference_train.csv')

validation = pd.read_csv('orders_validation.csv')

X_train = train[['feature_1']].to_numpy()

y_train = train['y_train'].to_numpy()

X_validation = validation[['feature_1']].to_numpy()

y_validation = validation['y_validation'].to_numpy()

import numpy as np

from sklearn.dummy import DummyClassifier

from sklearn.metrics import accuracy_score

# Supplied evaluation scaffold. Retain unchanged; complete only the top-level bindings below.
if __name__:
    def evaluate(X_train, y_train, X_validation, y, p_negative, p_positive, cost_FP, cost_FN):
        estimator = reference_factory(strategy="most_frequent")
        estimator.fit(X_train, y_train)
        predictions = estimator.predict(X_validation)
        FP = count_errors((y == 0) & (predictions == 1))
        TN = count_errors((y == 0) & (predictions == 0))
        FN = count_errors((y == 1) & (predictions == 0))
        TP = count_errors((y == 1) & (predictions == 1))
        negative_count = FP + TN
        positive_count = FN + TP
        FPR = None
        FNR = None
        expected_cost = None
        if negative_count > 0:
            FPR = FP / negative_count
        if positive_count > 0:
            FNR = FN / positive_count
        if negative_count > 0:
            if positive_count > 0:
                expected_cost = p_negative * FPR * cost_FP + p_positive * FNR * cost_FN
        training_mean = target_mean(y_train)
        training_std = target_std(y_train, ddof=0)
        training_positive_prevalence = count_errors(y_train == 1) / len(y_train)
        training_negative_prevalence = count_errors(y_train == 0) / len(y_train)
        validation_accuracy = validation_metric(y, predictions)
        return {'FP': FP, 'TN': TN, 'FN': FN, 'TP': TP, 'actual_negative_count': negative_count, 'actual_positive_count': positive_count, 'FPR': FPR, 'FNR': FNR, 'expected_cost': expected_cost, 'predictions': predictions, 'rule': 'most_frequent', 'training_mean': training_mean, 'training_std': training_std, 'training_positive_prevalence': training_positive_prevalence, 'training_negative_prevalence': training_negative_prevalence, 'validation_accuracy': validation_accuracy}

# Supplied callable operations; keep these assignments unchanged.
supplied_DummyClassifier = DummyClassifier
supplied_np_sum = np.sum
supplied_np_mean = np.mean
supplied_np_std = np.std
supplied_accuracy_score = accuracy_score
reference_factory = supplied_DummyClassifier
count_errors = supplied_np_sum

# Complete only these callable/value bindings; preserve the supplied scaffold.
target_mean = supplied_np_mean
target_std = supplied_np_std
validation_metric = supplied_accuracy_score

  test t1 (value_equals, visible=True): {"expr":"evaluate(X_train, y_train, X_validation, y_validation, p_negative, p_positive, cost_FP, cost_FN)","expected":{"FP":0,"TN":3,"FN":3,"TP":0,"actual_negative_count":3,"actual_positive_count":3,"FPR":0,"FNR":1,"expected_cost":1,"predictions":[0,0,0,0,0,0],"rule":"most_frequent","training_mean":0.2,"training_std":0.4,"training_positive_prevalence":0.2,"training_negative_prevalence":0.8,"validation_accuracy":0.5}} | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  test t2 (value_equals, visible=False): {"expr":"evaluate(X_train, y_train, X_validation[y_validation == 0], y_validation[y_validation == 0], p_negative, p_positive, cost_FP, cost_FN)","expected":{"FP":0,"TN":3,"FN":0,"TP":0,"actual_negative_count":3,"actual_positive_count":0,"FPR":0,"FNR":null,"expected_cost":null,"predictions":[0,0,0],"rule":"most_frequent","training_mean":0.2,"training_std":0.4,"training_positive_prevalence":0.2,"training_negative_prevalence":0.8,"validation_accuracy":1}} | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  test t3 (value_equals, visible=False): {"expr":"evaluate(X_train, y_train, X_validation[y_validation == 1], y_validation[y_validation == 1], p_negative, p_positive, cost_FP, cost_FN)","expected":{"FP":0,"TN":0,"FN":3,"TP":0,"actual_negative_count":0,"actual_positive_count":3,"FPR":null,"FNR":1,"expected_cost":null,"predictions":[0,0,0],"rule":"most_frequent","training_mean":0.2,"training_std":0.4,"training_positive_prevalence":0.2,"training_negative_prevalence":0.8,"validation_accuracy":0}} | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"c3d57612ef86ff08d3f5cc469233eabd796278cf45bab6de018de8b58c63c951","tests_passed":3}
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Complete only the indicated expressions using the supplied inputs.', 'Keep guards, structured evidence and result fields unchanged.']  remediation→r02
  MEASURES: A:define_task_compatible_reference(f1,f9); A:fit_training_only_and_freeze_reference(f2,f8); A:measure_predeclared_validation_metric(f3); A:justify_reference_with_training_target_statistics(f4,f5,f9); A:calculate_conditional_error_rates_and_expected_cost(f6,f7)   anchors=['practice', 'assessment:define_task_compatible_reference', 'assessment:fit_training_only_and_freeze_reference', 'assessment:measure_predeclared_validation_metric', 'assessment:justify_reference_with_training_target_statistics', 'assessment:calculate_conditional_error_rates_and_expected_cost']
  taught-before-tested: A.f1←s01; A.f9←s02; A.f2←s01; A.f8←s02; A.f3←s01; A.f4←s01; A.f5←s01; A.f9←s02; A.f6←s01; A.f7←s02

### s06 · explainer · Conditioned deployment cost
(intro) Use supplied matched records to justify an approach choice. Predictive quality, deployment fit and operating evidence all matter before promotion. ⟦B:tb1⟧
(mechanism) Compare alternatives on the same intended task and cohort. Check quality and deployment compatibility. Inference options differ in latency, scale and cost; supplied constraints govern eligibility. Reject records failing precommitted quality or operating limits, then apply the fixed decision rule among eligible alternatives. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Do not use protected-test observations to fit preprocessing, choose models or tune settings: that leaks information. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"ds.approach_records","columns":["alternative_id","model_family","delivery_mode","cohort_id","TP","FP","FN","TN","actual_positive_count","actual_negative_count","cohort_count","precision","recall","validation_prevalence","FPR","FNR","expected_error_cost","latency_requirement_met","scale_requirement_met","training_cost_requirement_met","serving_cost_requirement_met","maintenance_requirement_met","deployment_compatibility_met","maintenance_responsibility"]},"range":"A1:X4","show_formula_bar":true,"lineage":{"concept_ids":["mle.model_approach_decision"],"teaching_block_ids":[],"fact_ids":[],"anchors":["mle.model_approach_decision#visual"]}}
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract
[TABLE computed result ] caption: Fixed-contract eligibility and retained validation selection; null rates remain undefined.
  produced by sql: WITH rates AS (
SELECT r.*, 1.0*r.FP/NULLIF(r.FP+r.TN,0) AS conditioned_FPR,
1.0*r.FN/NULLIF(r.FN+r.TP,0) AS conditioned_FNR,
c.deployment_negative_probability, c.deployment_positive_probability, c.cost_FP, c.cost_FN,
c.expected_cost_bound, (r.latency_requirement_met = TRUE AND r.scale_requirement_met = TRUE AND r.training_cost_requirement_met = TRUE AND r.serving_cost_requirement_met = TRUE AND r.maintenance_requirement_met = TRUE AND r.deployment_compatibility_met = TRUE) AS operating_met,
r.cohort_id = 'orders_100' AS matched_cohort, r.alternative_id AS tie_order 
FROM records r CROSS JOIN contract c  
), costs AS (
SELECT *, deployment_negative_probability*conditioned_FPR*cost_FP + deployment_positive_probability*conditioned_FNR*cost_FN AS computed_cost FROM rates
), eligible AS (
SELECT *, CASE WHEN NOT matched_cohort THEN 'different cohort'
WHEN conditioned_FPR IS NULL OR conditioned_FNR IS NULL THEN 'undefined required rate'
WHEN computed_cost > expected_cost_bound THEN 'quality bound failed'
WHEN NOT operating_met THEN 'operating requirement failed'
ELSE 'eligible' END AS eligibility_reason FROM costs
), ranked AS (
SELECT alternative_id, ROW_NUMBER() OVER (ORDER BY computed_cost, tie_order) AS eligible_rank
FROM eligible WHERE eligibility_reason = 'eligible'
)
SELECT a.alternative_id, a.cohort_id, a.FP+a.TN AS actual_negative_denominator,
a.FN+a.TP AS actual_positive_denominator, a.conditioned_FPR, a.conditioned_FNR,
a.computed_cost, a.expected_cost_bound, a.eligibility_reason,
b.eligible_rank, CASE WHEN b.eligible_rank=1 THEN TRUE ELSE FALSE END AS retained_selection
FROM eligible a LEFT JOIN ranked b ON a.alternative_id=b.alternative_id ORDER BY a.tie_order
  result columns=['alternative_id', 'cohort_id', 'actual_negative_denominator', 'actual_positive_denominator', 'conditioned_FPR', 'conditioned_FNR', 'computed_cost', 'expected_cost_bound', 'eligibility_reason', 'eligible_rank', 'retained_selection'] rows(3)=[["custom_classical","orders_100",80,20,0.1,0.2,0.28,0.3,"eligible",1,true],["custom_neural","orders_100",80,20,0.05,0.2,0.24000000000000005,0.3,"operating requirement failed",null,false],["managed_service","orders_100",80,20,0.15,0.2,0.32000000000000006,0.3,"quality bound failed",null,false]]

### s07 · explainer · Exclude before ranking
(mechanism) Custom classical or neural models leave task-model implementation and training choices with the model owner. A managed service can supply training/hosting infrastructure. Compare maintenance responsibility alongside predictive and operating evidence. Address classical/neural and custom/managed trade-offs from matched records, without fitting new alternatives to manufacture evidence. ⟦B.f7 B.f8 B:tb4⟧
(example) The approach records keep model family, delivery mode, cohort, confusion counts and operating checks together. Use the same supplied deployment probabilities and costs for every row. Exclude an alternative that fails a fixed requirement before applying the selection rule. A lower cost cannot erase an operating failure; maintenance responsibility remains part of the comparison. ⟦B.f1 B.f2 B.f3 B.f5 B.f6 B.f7 B.f8 B:tb5⟧
(misconception) Choose only among eligible matched records. A favorable predictive number cannot excuse a failed operating requirement or replace maintenance evidence. ⟦B.f1 B.f2 B.f7 B:tb6⟧

### s08 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.
QUESTION [choice, core, grading=client] Matched classical and neural records satisfy the same predictive-quality requirement. The neural record fails the precommitted latency requirement. Under the fixed minimum-cost-among-eligible rule, what should happen?
  ✔ o1: Exclude the neural record before selecting among eligible alternatives.
      why: Operating constraints define eligibility before cost ranking.
  ✘ o2: Select the neural record whenever its expected cost is lower.
      why: Lower cost cannot override a fixed operating failure.
  ✘ o3: Remove latency from the contract after seeing the neural result.
      why: Requirements are fixed before comparison, not rewritten after results.
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r03
  MEASURES: B:reject_ineligible_alternatives_and_apply_fixed_decision_rule(f2,f3)   anchors=['assessment:reject_ineligible_alternatives_and_apply_fixed_decision_rule']
  taught-before-tested: B.f2←s06; B.f3←s06

### s09 · hands_on · Calculate from the supplied evidence
 — Use the supplied dataset and fixed contract. Keep the conditioning population explicit when entering the requested formula.
QUESTION [formula_entry, core, grading=client] Row calculations
Read every supplied record. You may use helper-cell calculations for denominators, rates, costs and eligibility; in AZ1 assemble the prescribed semicolon-separated comparison record. For each row, in declared order, output <identity>: neg=<FP+TN>,pos=<FN+TP>,FPR=<two decimals or undefined>,FNR=<two decimals or undefined>,cost=<two decimals or undefined>,eligible=<yes/no>; then the row maintenance_responsibility followed by "; ". 

Eligibility and selection
Apply the fixed orders_100 cohort, expected-cost <= 0.30, every supplied operating flag, and defined required rates. Rank eligible records by lowest cost; ties use declared order. 

Append selected=<identity or none>, then the exact fixed suffix:
; fixed p0=0.80,p1=0.20,costFP=1,costFN=5,correct cost=0,bound=0.30; exclude unmatched cohorts, operating failures and unresolved required rates before cost ranking; ties use declared order; no protected-test evidence. Append: Classical versus neural follows matched quality and operating eligibility; custom versus managed retains the recorded maintenance responsibilities, not an assumption that managed eliminates owner task-model choices. Instruction only—not part of AZ1 output: Freeze the supplied approach without new fitting or protected-test access.
  [unrendered interaction type formula_entry] public={"prompt":"Row calculations\nRead every supplied record. You may use helper-cell calculations for denominators, rates, costs and eligibility; in AZ1 assemble the prescribed semicolon-separated comparison record. For each row, in declared order, output <identity>: neg=<FP+TN>,pos=<FN+TP>,FPR=<two decimals or undefined>,FNR=<two decimals or undefined>,cost=<two decimals or undefined>,eligible=<yes/no>; then the row maintenance_responsibility followed by \"; \". \n\nEligibility and selection\nApply the fixed orders_100 cohort, expected-cost <= 0.30, every supplied operating flag, and defined required rates. Rank eligible records by lowest cost; ties use declared order. \n\nAppend selected=<identity or none>, then the exact fixed suffix:\n; fixed p0=0.80,p1=0.20,costFP=1,costFN=5,correct cost=0,bound=0.30; exclude unmatched cohorts, operating failures and unresolved required rates before cos grading={"reference_formula":"=A2&\": neg=\"&(F2+H2)&\",pos=\"&(G2+E2)&\",FPR=\"&IF((F2+H2)>0,TEXT(F2/(F2+H2),\"0.00\"),\"undefined\")&\",FNR=\"&IF((G2+E2)>0,TEXT(G2/(G2+E2),\"0.00\"),\"undefined\")&\",cost=\"&IF(AND((F2+H2)>0,(G2+E2)>0),TEXT((0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5),\"0.00\"),\"undefined\")&\",eligible=\"&IF(IF(AND((F2+H2)>0,(G2+E2)>0),AND(D2=\"orders_100\",(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5)<=0.30,AND(R2,S2,T2,U2,V2,W2)),FALSE),\"yes\",\"no\")&\"; \"&X2&\"; \"&A3&\": neg=\"&(F3+H3)&\",pos=\"&(G3+E3)&\",FPR=\"&IF((F3+H3)>0,TEXT(F3/(F3+H3),\"0.00\"),\"undefined\")&\",FNR=\"&IF((G3+E3)>0,TEXT(G3/(G3+E3),\"0.00\"),\"undefined\")&\",cost=\"&IF(AND((F3+H3)>0,(G3+E3)>0),TEXT((0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5),\"0.00\"),\"undefined\")&\",eligible=\"&IF(IF(AND((F3+H3)>0,(G3+E3)>0),AND(D3=\"orders_100\",(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5)<=0.30,AND(R3,S3,T3,U3,V3,W3)),FALSE),\"yes\",\"no\")&\"; \"&X
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r04
  MEASURES: B:verify_matched_task_cohort_and_deployment_compatibility(f1); B:derive_conditional_error_rates_and_identify_undefined_rates(f4); B:calculate_prevalence_weighted_expected_error_cost(f4,f5); B:reject_ineligible_alternatives_and_apply_fixed_decision_rule(f2,f3); B:justify_classical_neural_and_custom_managed_tradeoffs(f7,f8); B:freeze_supplied_approach_without_new_fitting_or_protected_test_access(f6,f8)   anchors=['practice', 'assessment:verify_matched_task_cohort_and_deployment_compatibility', 'assessment:derive_conditional_error_rates_and_identify_undefined_rates', 'assessment:calculate_prevalence_weighted_expected_error_cost', 'assessment:reject_ineligible_alternatives_and_apply_fixed_decision_rule', 'assessment:justify_classical_neural_and_custom_managed_tradeoffs', 'assessment:freeze_supplied_approach_without_new_fitting_or_protected_test_access']
  taught-before-tested: B.f1←s06; B.f4←s06; B.f4←s06; B.f5←s06; B.f2←s06; B.f3←s06; B.f7←s07; B.f8←s07; B.f6←s06; B.f8←s07

### s10 · explainer · Evaluate conditional errors
(intro) Connect aligned numeric training data to a bounded LogisticRegression baseline, then inspect its held-out predictions under the declared evaluation. ⟦C:tb1⟧
(mechanism) Use from sklearn.linear_model import LogisticRegression, create estimator = LogisticRegression(random_state=0), and call estimator.fit(X_train, y_train). Numeric X_train has shape (n_samples, n_features); aligned class labels y_train have shape (n_samples,). Compare estimator.predict(X_validation) with corresponding y_validation. If fitting used preprocessing, predict through the fitted pipeline to preserve the feature representation. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) on actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦C.f4 C.f5 C:tb3⟧
[CODE python]
import numpy as np
from sklearn.linear_model import LogisticRegression

def evaluate_baseline(X_train, y_train, X_validation, y_validation, p_negative, p_positive, cost_FP, cost_FN):
    estimator = LogisticRegression(random_state=0)
    estimator.fit(X_train, y_train)
    predictions = estimator.predict(X_validation)
    # If training used preprocessing, use the fitted pipeline's predict instead.
    FP = np.sum((y_validation == 0) & (predictions == 1))
    TN = np.sum((y_validation == 0) & (predictions == 0))
    FN = np.sum((y_validation == 1) & (predictions == 0))
    TP = np.sum((y_validation == 1) & (predictions == 1))
    FPR = FP / (FP + TN) if FP + TN else None
    FNR = FN / (FN + TP) if FN + TP else None
    expected_cost = (p_negative * FPR * cost_FP + p_positive * FNR * cost_FN
                     if FPR is not None and FNR is not None else None)
    return {
        'training_shape': X_train.shape,
        'training_label_shape': y_train.shape,
        'validation_shape': X_validation.shape,
        'predictions': predictions,
        'validation_labels': y_validation,
        'FP': FP,
        'TN': TN,
        'FN': FN,
        'TP': TP,
        'actual_negative_denominator': FP + TN,
        'actual_positive_denominator': FN + TP,
        'FPR': FPR,
        'FNR': FNR,
        'expected_cost': expected_cost,
    }
  annotations: []
[TABLE ds.orders_train cols=['observation_id', 'feature_1', 'feature_2', 'y_train'] ] caption: Six-order estimator training inputs
[TABLE ds.orders_validation cols=['observation_id', 'feature_1', 'feature_2', 'y_validation'] ] caption: Held-out aligned estimator inputs
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract

### s11 · explainer · Inspect the held-out path
(example) The training and validation tables expose observation identities, numeric features and aligned labels. Fitting establishes estimator state; prediction applies it to validation inputs; evaluation compares outputs with matching held-out labels. Shape agreement alone does not establish observation correspondence. Use the fitted pipeline when preprocessing belongs to it. Inspect conditional error counts and the fixed cost calculation rather than stopping when fit returns. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb4⟧

### s12 · explainer · Prediction is not a verdict
(misconception) predict is not a quality verdict. Use matching held-out labels and the fixed evaluation rule; bypassing fitted preprocessing changes the representation. ⟦C.f2 C.f3 C:tb5⟧

### s13 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.
QUESTION [choice, core, grading=client] Training used fitted preprocessing. Which validation prediction path preserves the fitted feature representation?
  ✔ o1: Call predict through that fitted pipeline on the corresponding validation inputs.
      why: The fitted pipeline applies the training-fitted representation to validation.
  ✘ o2: Fit preprocessing again using validation labels before predicting.
      why: Validation is held out; its labels should not refit training state.
  ✘ o3: Bypass the fitted preprocessing and send raw inputs directly to the final estimator.
      why: Bypassing the fitted preprocessing changes the feature representation.
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r05
  MEASURES: C:reuse_fitted_preprocessing_for_validation_predictions(f3)   anchors=['assessment:reuse_fitted_preprocessing_for_validation_predictions']
  taught-before-tested: C.f3←s10

### s14 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.
QUESTION [code_exercise, intro, grading=client] Complete the estimator construction, training-only fit and validation-prediction expressions using LogisticRegression(random_state=0), X_train/y_train and X_validation. Preserve the supplied alignment checks, error-rate guards and result schema.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy', 'pandas', 'scikit-learn']} constraints.allowed=['def with parameters and return', 'from sklearn.linear_model import LogisticRegression', 'import numpy as np', 'variable assignment', 'LogisticRegression(random_state=0)', 'estimator.fit(X_train, y_train)', 'estimator.predict(X_validation)', 'supplied_pipeline.fit(X_train, y_train)', 'supplied_pipeline.predict(X_validation)', 'array.shape and array.ndim', 'assert statements', 'array comparisons with binary labels 0 and 1', 'elementwise boolean conjunction with &', 'np.sum on boolean arrays', 'arithmetic operators +, *, and /', 'if and else', 'None for undefined quantities', 'dictionary construction for returned results'] blocked=9 items
  file main.py [editable]:
# Supplied input loading and dependencies.
import pandas as pd

contract = pd.read_csv('acceptance_contract.csv').iloc[0]

p_negative = contract['deployment_negative_probability']

p_positive = contract['deployment_positive_probability']

cost_FP = contract['cost_FP']

cost_FN = contract['cost_FN']

bound = contract['expected_cost_bound']

train = pd.read_csv('orders_train.csv')

validation = pd.read_csv('orders_validation.csv')

X_train = train[['feature_1', 'feature_2']].to_numpy()

y_train = train['y_train'].to_numpy()

X_validation = validation[['feature_1', 'feature_2']].to_numpy()

y_validation = validation['y_validation'].to_numpy()

import numpy as np

from sklearn.linear_model import LogisticRegression

# Supplied evaluation scaffold. Complete the marked expressions; preserve the rest.
if __name__:
    def evaluate(X_train, y_train, X_validation, y, p_negative, p_positive, cost_FP, cost_FN):
        assert X_train.ndim == 2
        assert y_train.ndim == 1
        assert X_validation.ndim == 2
        assert y.ndim == 1
        assert X_validation.shape[1] == X_train.shape[1]
        assert X_train.shape[0] == y_train.shape[0]
        assert X_validation.shape[0] == y.shape[0]
        estimator = None  # TODO: construct the estimator
        ...  # TODO: fit the estimator on training inputs only
        predictions = None  # TODO: predict validation labels
        FP = np.sum((y == 0) & (predictions == 1))
        TN = np.sum((y == 0) & (predictions == 0))
        FN = np.sum((y == 1) & (predictions == 0))
        TP = np.sum((y == 1) & (predictions == 1))
        negative_count = FP + TN
        positive_count = FN + TP
        FPR = None
        FNR = None
        expected_cost = None
        if negative_count > 0:
            FPR = FP / negative_count
        if positive_count > 0:
            FNR = FN / positive_count
        if negative_count > 0:
            if positive_count > 0:
                expected_cost = p_negative * FPR * cost_FP + p_positive * FNR * cost_FN
        return {'FP': FP, 'TN': TN, 'FN': FN, 'TP': TP, 'actual_negative_count': negative_count, 'actual_positive_count': positive_count, 'FPR': FPR, 'FNR': FNR, 'expected_cost': expected_cost, 'predictions': predictions, 'training_shape': X_train.shape, 'training_label_shape': y_train.shape}


# Supplied constructor; retain unchanged.
supplied_LogisticRegression = LogisticRegression

# Constructor binding.
estimator_factory = supplied_LogisticRegression

  SOLUTION main.py:
# Supplied input loading and dependencies.
import pandas as pd

contract = pd.read_csv('acceptance_contract.csv').iloc[0]

p_negative = contract['deployment_negative_probability']

p_positive = contract['deployment_positive_probability']

cost_FP = contract['cost_FP']

cost_FN = contract['cost_FN']

bound = contract['expected_cost_bound']

train = pd.read_csv('orders_train.csv')

validation = pd.read_csv('orders_validation.csv')

X_train = train[['feature_1', 'feature_2']].to_numpy()

y_train = train['y_train'].to_numpy()

X_validation = validation[['feature_1', 'feature_2']].to_numpy()

y_validation = validation['y_validation'].to_numpy()

import numpy as np

from sklearn.linear_model import LogisticRegression

# Supplied evaluation scaffold. Preserve the scaffold outside the requested TODO expressions.
if __name__:
    def evaluate(X_train, y_train, X_validation, y, p_negative, p_positive, cost_FP, cost_FN):
        assert X_train.ndim == 2
        assert y_train.ndim == 1
        assert X_validation.ndim == 2
        assert y.ndim == 1
        assert X_validation.shape[1] == X_train.shape[1]
        assert X_train.shape[0] == y_train.shape[0]
        assert X_validation.shape[0] == y.shape[0]
        estimator = LogisticRegression(random_state=0)
        estimator.fit(X_train, y_train)
        predictions = estimator.predict(X_validation)
        FP = np.sum((y == 0) & (predictions == 1))
        TN = np.sum((y == 0) & (predictions == 0))
        FN = np.sum((y == 1) & (predictions == 0))
        TP = np.sum((y == 1) & (predictions == 1))
        negative_count = FP + TN
        positive_count = FN + TP
        FPR = None
        FNR = None
        expected_cost = None
        if negative_count > 0:
            FPR = FP / negative_count
        if positive_count > 0:
            FNR = FN / positive_count
        if negative_count > 0:
            if positive_count > 0:
                expected_cost = p_negative * FPR * cost_FP + p_positive * FNR * cost_FN
        return {'FP': FP, 'TN': TN, 'FN': FN, 'TP': TP, 'actual_negative_count': negative_count, 'actual_positive_count': positive_count, 'FPR': FPR, 'FNR': FNR, 'expected_cost': expected_cost, 'predictions': predictions, 'training_shape': X_train.shape, 'training_label_shape': y_train.shape}


# Supplied constructor; retain unchanged.
supplied_LogisticRegression = LogisticRegression

# Constructor binding.
estimator_factory = supplied_LogisticRegression

  test t1 (value_equals, visible=True): {"expr":"evaluate(X_train, y_train, X_validation, y_validation, p_negative, p_positive, cost_FP, cost_FN)","expected":{"FP":1,"TN":2,"FN":0,"TP":3,"actual_negative_count":3,"actual_positive_count":3,"FPR":0.3333333333333333,"FNR":0,"expected_cost":0.26666666666666666,"predictions":[0,0,1,1,1,1],"training_shape":[6,2],"training_label_shape":[6]}} | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  test t2 (value_equals, visible=False): {"expr":"evaluate(X_train, y_train, X_validation[y_validation == 0], y_validation[y_validation == 0], p_negative, p_positive, cost_FP, cost_FN)","expected":{"FP":1,"TN":2,"FN":0,"TP":0,"actual_negative_count":3,"actual_positive_count":0,"FPR":0.3333333333333333,"FNR":null,"expected_cost":null,"predictions":[0,0,1],"training_shape":[6,2],"training_label_shape":[6]}} | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  test t3 (value_equals, visible=False): {"expr":"evaluate(X_train, y_train, X_validation[y_validation == 1], y_validation[y_validation == 1], p_negative, p_positive, cost_FP, cost_FN)","expected":{"FP":0,"TN":0,"FN":0,"TP":3,"actual_negative_count":0,"actual_positive_count":3,"FPR":null,"FNR":0,"expected_cost":null,"predictions":[1,1,1],"training_shape":[6,2],"training_label_shape":[6]}} | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"8909acc81d738bb4524342dab3eb8a44a3ee1f8024189fc6c3de61dde8641b4e","tests_passed":3}
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Complete only the indicated expressions using the supplied inputs.', 'Keep guards, structured evidence and result fields unchanged.']  remediation→r06
  MEASURES: C:fit_baseline_with_aligned_numeric_inputs(f1); C:obtain_observation_aligned_validation_predictions(f2)   anchors=['practice', 'assessment:fit_baseline_with_aligned_numeric_inputs', 'assessment:obtain_observation_aligned_validation_predictions']
  taught-before-tested: C.f1←s10; C.f2←s10

### s15 · recap · Keep these distinctions
(takeaway) Fit a simple reference on training and evaluate frozen validation predictions. Keep training statistics distinct from held-out evidence. Compare approaches on matched task/cohort records and fixed eligibility rules. Preserve aligned features, labels and fitted preprocessing in the LogisticRegression path. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 C.f1 C.f2 C.f3 C.f4 C.f5 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5 B:tb6 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Up next: Turn classification scores into explicit threshold-dependent decisions.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: the check — start with a reference
(misconception) Contrast training class proportions with validation prevalence. Fit the reference on training, but judge its frozen predictions with matching validation targets. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A:tb2 A:tb3 A:tb4⟧
(mechanism) DummyClassifier offers reference rules such as most_frequent, prior and constant. DummyRegressor(strategy="mean") predicts the training-target mean. Fit on training inputs and targets, freeze the estimator, then predict on separate validation observations. Report the predeclared metric against validation targets, not a training-only result. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Use np.mean(numeric_values) for the selected numeric observations’ arithmetic mean. np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root; use ddof=1 only when an N−1 divisor is required. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty conditioning groups give undefined rates. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(mechanism) With correct predictions costing zero, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations must not fit preprocessing, choose a model or tune settings: that leaks information. For a classification reference, report training target-class count/training total, not validation or protected-test prevalence. ⟦A.f7 A.f8 A.f9 A:tb4⟧
[TABLE ds.reference_train cols=['observation_id', 'feature_1', 'y_train'] ] caption: Reference-only training cohort
### r02 · Revisit: the practice — start with a reference
(misconception) Contrast training class proportions with validation prevalence. Fit the reference on training, but judge its frozen predictions with matching validation targets. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A.f8 A.f9 A:tb2 A:tb3 A:tb4⟧
(mechanism) DummyClassifier offers reference rules such as most_frequent, prior and constant. DummyRegressor(strategy="mean") predicts the training-target mean. Fit on training inputs and targets, freeze the estimator, then predict on separate validation observations. Report the predeclared metric against validation targets, not a training-only result. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Use np.mean(numeric_values) for the selected numeric observations’ arithmetic mean. np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root; use ddof=1 only when an N−1 divisor is required. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty conditioning groups give undefined rates. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(mechanism) With correct predictions costing zero, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations must not fit preprocessing, choose a model or tune settings: that leaks information. For a classification reference, report training target-class count/training total, not validation or protected-test prevalence. ⟦A.f7 A.f8 A.f9 A:tb4⟧
[TABLE ds.reference_train cols=['observation_id', 'feature_1', 'y_train'] ] caption: Reference-only training cohort
### r03 · Revisit: the check — matched approach evidence
(misconception) Contrast an attractive cost with an eligible approach. Matched task/cohort and every fixed quality/operating requirement come before selection. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B:tb2 B:tb3 B:tb4⟧
(mechanism) Compare alternatives on the same intended task and cohort. Check quality and deployment compatibility. Inference options differ in latency, scale and cost; supplied constraints govern eligibility. Reject records failing precommitted quality or operating limits, then apply the fixed decision rule among eligible alternatives. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Do not use protected-test observations to fit preprocessing, choose models or tune settings: that leaks information. ⟦B.f4 B.f5 B.f6 B:tb3⟧
(mechanism) Custom classical or neural models leave task-model implementation and training choices with the model owner. A managed service can supply training/hosting infrastructure. Compare maintenance responsibility alongside predictive and operating evidence. Address classical/neural and custom/managed trade-offs from matched records, without fitting new alternatives to manufacture evidence. ⟦B.f7 B.f8 B:tb4⟧
[TABLE ds.approach_records cols=['alternative_id', 'model_family', 'delivery_mode', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'latency_requirement_met', 'scale_requirement_met', 'training_cost_requirement_met', 'serving_cost_requirement_met', 'maintenance_requirement_met', 'deployment_compatibility_met', 'maintenance_responsibility'] ] caption: Classical, neural, and managed operating records
### r04 · Revisit: the practice — matched approach evidence
(misconception) Contrast an attractive cost with an eligible approach. Matched task/cohort and every fixed quality/operating requirement come before selection. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B.f7 B.f8 B:tb2 B:tb3 B:tb4⟧
(mechanism) Compare alternatives on the same intended task and cohort. Check quality and deployment compatibility. Inference options differ in latency, scale and cost; supplied constraints govern eligibility. Reject records failing precommitted quality or operating limits, then apply the fixed decision rule among eligible alternatives. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Do not use protected-test observations to fit preprocessing, choose models or tune settings: that leaks information. ⟦B.f4 B.f5 B.f6 B:tb3⟧
(mechanism) Custom classical or neural models leave task-model implementation and training choices with the model owner. A managed service can supply training/hosting infrastructure. Compare maintenance responsibility alongside predictive and operating evidence. Address classical/neural and custom/managed trade-offs from matched records, without fitting new alternatives to manufacture evidence. ⟦B.f7 B.f8 B:tb4⟧
[TABLE ds.approach_records cols=['alternative_id', 'model_family', 'delivery_mode', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'latency_requirement_met', 'scale_requirement_met', 'training_cost_requirement_met', 'serving_cost_requirement_met', 'maintenance_requirement_met', 'deployment_compatibility_met', 'maintenance_responsibility'] ] caption: Classical, neural, and managed operating records
### r05 · Revisit: the check — a bounded fitted baseline
(misconception) Contrast predictions with evaluated predictions: matching held-out labels and the fitted representation are needed before a quality verdict. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) Use from sklearn.linear_model import LogisticRegression, create estimator = LogisticRegression(random_state=0), and call estimator.fit(X_train, y_train). Numeric X_train has shape (n_samples, n_features); aligned class labels y_train have shape (n_samples,). Compare estimator.predict(X_validation) with corresponding y_validation. If fitting used preprocessing, predict through the fitted pipeline to preserve the feature representation. ⟦C.f1 C.f2 C.f3 C:tb2⟧
[TABLE ds.orders_train cols=['observation_id', 'feature_1', 'feature_2', 'y_train'] ] caption: Six-order estimator training inputs
### r06 · Revisit: the practice — a bounded fitted baseline
(misconception) Contrast predictions with evaluated predictions: matching held-out labels and the fitted representation are needed before a quality verdict. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C:tb2 C:tb3⟧
(mechanism) Use from sklearn.linear_model import LogisticRegression, create estimator = LogisticRegression(random_state=0), and call estimator.fit(X_train, y_train). Numeric X_train has shape (n_samples, n_features); aligned class labels y_train have shape (n_samples,). Compare estimator.predict(X_validation) with corresponding y_validation. If fitting used preprocessing, predict through the fitted pipeline to preserve the feature representation. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) on actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦C.f4 C.f5 C:tb3⟧
[TABLE ds.orders_train cols=['observation_id', 'feature_1', 'feature_2', 'y_train'] ] caption: Six-order estimator training inputs

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: from sklearn.model_selection import GridSearchCV
· constraints.blocked_syntax: from sklearn.model_selection import RandomizedSearchCV
· grading.reference_formula: =A2&": neg="&(F2+H2)&",pos="&(G2+E2)&",FPR="&IF((F2+H2)>0,TEXT(F2/(F2+H2),"0.00"),"undefined")&",FNR="&IF((G2+E2)>0,TEXT(G2/(G2+E2),"0.00"),"undefined")&",cost="&IF(AND((F2+H2)>0,(G2+E2)>0),TEXT((0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5),"0.00"),"undefined")&",eligible="&IF(IF(AND((F2+H2)>0,(G2+E2)>0),AND(D2="orders_100",(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5)<=0.30,AND(R2,S2,T2,U2,V2,W2)),FALSE),"yes","no")&"; "&X2&"; "&A3&": neg="&(F3+H3)&",pos="&(G3+E3)&",FPR="&IF((F3+H3)>0,TEXT(F3/(F3+H3),"0.00"),"undefined")&",FNR="&IF((G3+E3)>0,TEXT(G3/(G3+E3),"0.00"),"undefined")&",cost="&IF(AND((F3+H3)>0,(G3+E3)>0),TEXT((0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5),"0.00"),"undefined")&",eligible="&IF(IF(AND((F3+H3)>0,(G3+E3)>0),AND(D3="orders_100",(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5)<=0.30,AND(R3,S3,T3,U3,V3,W3)),FALSE),"yes","no")&"; "&X3&"; "&A4&": neg="&(F4+H4)&",pos="&(G4+E4)&",FPR="&IF((F4+H4)>0,TEXT(F4/(F4+H4),"0.00"),"undefined")&",FNR="&IF((G4+E4)>0,TEXT(G4/(G4+E4),"0.00"),"undefined")&",cost="&IF(AND((F4+H4)>0,(G4+E4)>0),TEXT((0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5),"0.00"),"undefined")&",eligible="&IF(IF(AND((F4+H4)>0,(G4+E4)>0),AND(D4="orders_100",(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5)<=0.30,AND(R4,S4,T4,U4,V4,W4)),FALSE),"yes","no")&"; "&X4&"; "&"selected="&IF(IF(AND((F2+H2)>0,(G2+E2)>0),AND(D2="orders_100",(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5)<=0.30,AND(R2,S2,T2,U2,V2,W2)),FALSE),IF(IF(AND((F2+H2)>0,(G2+E2)>0),IF(AND(D2="orders_100",(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5)<=0.30,AND(R2,S2,T2,U2,V2,W2)),(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5),1000000),1000000)=MIN(IF(AND((F2+H2)>0,(G2+E2)>0),IF(AND(D2="orders_100",(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5)<=0.30,AND(R2,S2,T2,U2,V2,W2)),(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5),1000000),1000000),IF(AND((F3+H3)>0,(G3+E3)>0),IF(AND(D3="orders_100",(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5)<=0.30,AND(R3,S3,T3,U3,V3,W3)),(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5),1000000),1000000),IF(AND((F4+H4)>0,(G4+E4)>0),IF(AND(D4="orders_100",(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5)<=0.30,AND(R4,S4,T4,U4,V4,W4)),(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5),1000000),1000000)),A2,IF(IF(AND((F3+H3)>0,(G3+E3)>0),AND(D3="orders_100",(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5)<=0.30,AND(R3,S3,T3,U3,V3,W3)),FALSE),IF(IF(AND((F3+H3)>0,(G3+E3)>0),IF(AND(D3="orders_100",(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5)<=0.30,AND(R3,S3,T3,U3,V3,W3)),(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5),1000000),1000000)=MIN(IF(AND((F2+H2)>0,(G2+E2)>0),IF(AND(D2="orders_100",(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5)<=0.30,AND(R2,S2,T2,U2,V2,W2)),(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5),1000000),1000000),IF(AND((F3+H3)>0,(G3+E3)>0),IF(AND(D3="orders_100",(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5)<=0.30,AND(R3,S3,T3,U3,V3,W3)),(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5),1000000),1000000),IF(AND((F4+H4)>0,(G4+E4)>0),IF(AND(D4="orders_100",(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5)<=0.30,AND(R4,S4,T4,U4,V4,W4)),(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5),1000000),1000000)),A3,IF(IF(AND((F4+H4)>0,(G4+E4)>0),AND(D4="orders_100",(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5)<=0.30,AND(R4,S4,T4,U4,V4,W4)),FALSE),IF(IF(AND((F4+H4)>0,(G4+E4)>0),IF(AND(D4="orders_100",(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5)<=0.30,AND(R4,S4,T4,U4,V4,W4)),(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5),1000000),1000000)=MIN(IF(AND((F2+H2)>0,(G2+E2)>0),IF(AND(D2="orders_100",(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5)<=0.30,AND(R2,S2,T2,U2,V2,W2)),(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5),1000000),1000000),IF(AND((F3+H3)>0,(G3+E3)>0),IF(AND(D3="orders_100",(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5)<=0.30,AND(R3,S3,T3,U3,V3,W3)),(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5),1000000),1000000),IF(AND((F4+H4)>0,(G4+E4)>0),IF(AND(D4="orders_100",(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5)<=0.30,AND(R4,S4,T4,U4,V4,W4)),(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5),1000000),1000000)),A4,"none"),"none")),IF(IF(AND((F4+H4)>0,(G4+E4)>0),AND(D4="orders_100",(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5)<=0.30,AND(R4,S4,T4,U4,V4,W4)),FALSE),IF(IF(AND((F4+H4)>0,(G4+E4)>0),IF(AND(D4="orders_100",(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5)<=0.30,AND(R4,S4,T4,U4,V4,W4)),(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5),1000000),1000000)=MIN(IF(AND((F2+H2)>0,(G2+E2)>0),IF(AND(D2="orders_100",(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5)<=0.30,AND(R2,S2,T2,U2,V2,W2)),(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5),1000000),1000000),IF(AND((F3+H3)>0,(G3+E3)>0),IF(AND(D3="orders_100",(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5)<=0.30,AND(R3,S3,T3,U3,V3,W3)),(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5),1000000),1000000),IF(AND((F4+H4)>0,(G4+E4)>0),IF(AND(D4="orders_100",(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5)<=0.30,AND(R4,S4,T4,U4,V4,W4)),(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5),1000000),1000000)),A4,"none"),"none"))),IF(IF(AND((F3+H3)>0,(G3+E3)>0),AND(D3="orders_100",(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5)<=0.30,AND(R3,S3,T3,U3,V3,W3)),FALSE),IF(IF(AND((F3+H3)>0,(G3+E3)>0),IF(AND(D3="orders_100",(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5)<=0.30,AND(R3,S3,T3,U3,V3,W3)),(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5),1000000),1000000)=MIN(IF(AND((F2+H2)>0,(G2+E2)>0),IF(AND(D2="orders_100",(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5)<=0.30,AND(R2,S2,T2,U2,V2,W2)),(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5),1000000),1000000),IF(AND((F3+H3)>0,(G3+E3)>0),IF(AND(D3="orders_100",(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5)<=0.30,AND(R3,S3,T3,U3,V3,W3)),(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5),1000000),1000000),IF(AND((F4+H4)>0,(G4+E4)>0),IF(AND(D4="orders_100",(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5)<=0.30,AND(R4,S4,T4,U4,V4,W4)),(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5),1000000),1000000)),A3,IF(IF(AND((F4+H4)>0,(G4+E4)>0),AND(D4="orders_100",(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5)<=0.30,AND(R4,S4,T4,U4,V4,W4)),FALSE),IF(IF(AND((F4+H4)>0,(G4+E4)>0),IF(AND(D4="orders_100",(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5)<=0.30,AND(R4,S4,T4,U4,V4,W4)),(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5),1000000),1000000)=MIN(IF(AND((F2+H2)>0,(G2+E2)>0),IF(AND(D2="orders_100",(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5)<=0.30,AND(R2,S2,T2,U2,V2,W2)),(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5),1000000),1000000),IF(AND((F3+H3)>0,(G3+E3)>0),IF(AND(D3="orders_100",(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5)<=0.30,AND(R3,S3,T3,U3,V3,W3)),(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5),1000000),1000000),IF(AND((F4+H4)>0,(G4+E4)>0),IF(AND(D4="orders_100",(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5)<=0.30,AND(R4,S4,T4,U4,V4,W4)),(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5),1000000),1000000)),A4,"none"),"none")),IF(IF(AND((F4+H4)>0,(G4+E4)>0),AND(D4="orders_100",(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5)<=0.30,AND(R4,S4,T4,U4,V4,W4)),FALSE),IF(IF(AND((F4+H4)>0,(G4+E4)>0),IF(AND(D4="orders_100",(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5)<=0.30,AND(R4,S4,T4,U4,V4,W4)),(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5),1000000),1000000)=MIN(IF(AND((F2+H2)>0,(G2+E2)>0),IF(AND(D2="orders_100",(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5)<=0.30,AND(R2,S2,T2,U2,V2,W2)),(0.8*F2/(F2+H2)+0.2*G2/(G2+E2)*5),1000000),1000000),IF(AND((F3+H3)>0,(G3+E3)>0),IF(AND(D3="orders_100",(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5)<=0.30,AND(R3,S3,T3,U3,V3,W3)),(0.8*F3/(F3+H3)+0.2*G3/(G3+E3)*5),1000000),1000000),IF(AND((F4+H4)>0,(G4+E4)>0),IF(AND(D4="orders_100",(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5)<=0.30,AND(R4,S4,T4,U4,V4,W4)),(0.8*F4/(F4+H4)+0.2*G4/(G4+E4)*5),1000000),1000000)),A4,"none"),"none")))&"; fixed p0=0.80,p1=0.20,costFP=1,costFN=5,correct cost=0,bound=0.30; exclude unmatched cohorts, operating failures and unresolved required rates before cost ranking; ties use declared order; no protected-test evidence."&" Classical versus neural follows matched quality and operating eligibility; custom versus managed retains the recorded maintenance responsibilities, not an assumption that managed eliminates owner task-model choices."
· grading.expected_value: custom_classical: neg=80,pos=20,FPR=0.10,FNR=0.20,cost=0.28,eligible=yes; owner maintains task model and infrastructure; custom_neural: neg=80,pos=20,FPR=0.05,FNR=0.20,cost=0.24,eligible=no; owner maintains task model and infrastructure; managed_service: neg=80,pos=20,FPR=0.15,FNR=0.20,cost=0.32,eligible=no; service supplies training or hosting infrastructure; owner retains custom task-model choices; selected=custom_classical; fixed p0=0.80,p1=0.20,costFP=1,costFN=5,correct cost=0,bound=0.30; exclude unmatched cohorts, operating failures and unresolved required rates before cost ranking; ties use declared order; no protected-test evidence. Classical versus neural follows matched quality and operating eligibility; custom versus managed retains the recorded maintenance responsibilities, not an assumption that managed eliminates owner task-model choices.
· constraints.blocked_syntax: estimator.predict_proba(...)
· constraints.blocked_syntax: RandomizedSearchCV(...)
· constraints.blocked_syntax: cross_val_score(...)
· constraints.blocked_syntax: mlflow.start_run(...)
· constraints.blocked_syntax: mlflow.log_metric(...)
· constraints.blocked_syntax: torch.optim.Adam(...)

=========

# EVALUATOR PACKET — Thresholds and candidate comparison (mle.tile.024_025)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.decision_threshold_selection — Select a decision threshold using validation data and task costs
B = mle.validation_candidate_comparison — Compare model candidates against a baseline using validation evidence before freezing the choice

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=4
  warn: mle.tile.024_025.s01: prose block without lineage.fact_ids
  warn: mle.tile.024_025.s06/ix.mle.tile.024_025.s06: ADVISORY — syntax descriptors with no detector: ['GridSearchCV or RandomizedSearchCV calls', 'MLflow tracking API calls', 'PyTorch model or training API calls', 'arithmetic expressions with guarded division', 'boolean array operations', 'calibration estimator construction or fitting', 'calls to supplied eligibility and threshold-retention interfaces', 'def with parameters and return statements', 'dictionary and list indexing', 'elementwise binary-label comparisons', 'elementwise score comparisons', 'for loops over supplied candidate thresholds', 'if and else conditionals', 'imports for dependencies required by supplied scaffolding', 'lists and dictionaries', 'local variable assignment', 'model registry or deployment API calls', 'numeric and string literals', 'protected test data loading or evaluation calls']
  warn: mle.tile.024_025.s07: prose block without lineage.fact_ids
  warn: plan: mle.tile.024_025.s10 was planned to measure mle.validation_candidate_comparison#assessment:freeze_validation_choice_without_protected_test_information but its interaction does not

## SOURCE FACTS — A (mle.decision_threshold_selection)   objective: Select and freeze a classification cutoff under precommitted validation cost constraints.
A.f1: A classification score and a class decision are different outputs; the decision is obtained by comparing the score with a threshold.   [sources: scikit_learn_user_guide#modules/classification_threshold.html — 3.3.1 The problem; 3.3.2 Post-tuning the decision threshold]
A.f2: For binary scikit-learn predictions, probability scores ordinarily use a 0.5 cutoff and decision_function scores a zero cutoff; an explicitly chosen task threshold changes that decision.   [sources: scikit_learn_user_guide#modules/classification_threshold.html — 3.3.1 The problem; 3.3.2 Post-tuning the decision threshold]
A.f3: For each supplied candidate threshold, form predicted labels, then count TP, FP, TN and FN against validation labels at that threshold.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f4: Choose the eligible threshold with the minimum predeclared expected cost on validation evidence and freeze it before protected testing.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
A.f5: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f6: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
A.f7: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Threshold and Candidate Selection.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection, mle.model_acceptance_criteria. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function, including required imports, that evaluates supplied candidate thresholds against validation scores and binary labels. Compute TP, FP, TN, FN, conditional FPR and FNR, and expected cost using supplied deployment class probabilities and fixed error costs. Apply supplied eligibility limits and retain the minimum-cost eligible threshold through the existing scaffolding, without fitting a calibration model or accessing protected test observations.  SUCCESS: Each candidate has correct confusion counts, conditional rates and prevalence-weighted expected cost. Empty conditioning groups are identified as undefined rather than assigned a numerical rate. The selected threshold satisfies supplied eligibility limits and minimizes the declared cost among eligible candidates. Its score representation and validation record are retained unchanged for later testing; no eligible candidate produces an explicit no-selection result.
ASSESSMENT ANCHOR: distinguish_scores_from_thresholded_decisions facts=['f1', 'f2']
ASSESSMENT ANCHOR: calculate_threshold_confusion_counts_and_conditional_error_rates facts=['f3', 'f5']
ASSESSMENT ANCHOR: select_minimum_cost_eligible_validation_threshold facts=['f4', 'f6']
ASSESSMENT ANCHOR: freeze_threshold_without_using_protected_test_observations facts=['f4', 'f7']

## SOURCE FACTS — B (mle.validation_candidate_comparison)   objective: Rank eligible candidate records using a common expected-cost and operating-limit rule.
B.f1: Compare candidate predictive metrics with the baseline on the same evaluation dataset and check predeclared requirements rather than selecting from incomparable cohorts.   [sources: google_mlops_pipelines#Data and model validation]
B.f2: Calculate each record’s expected cost under the same supplied deployment class probabilities and error costs, exclude records failing fixed limits, and rank the eligible records by the declared cost rule.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
B.f3: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
B.f4: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
B.f5: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Threshold and Candidate Selection.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection, mle.model_acceptance_criteria. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (spreadsheet): Compare three supplied candidate validation records and baseline A for the same orders cohort. Derive FPR and FNR from each record's supplied confusion counts, flag empty conditioning groups as undefined, and calculate expected error cost using the same supplied deployment class probabilities and fixed error costs. Apply the predeclared quality and operating limits, rank eligible records by the precommitted cost rule, and record one frozen choice without consulting protected test observations.  SUCCESS: The completed comparison retains the cohort identity, confusion counts, rate denominators, fixed probabilities and error costs for every record. Conditional rates and expected costs are correct; undefined rates are not replaced with zero. Eligibility decisions follow the supplied limits, exclusions have explicit reasons, and eligible records are ranked by the declared cost rule. One selected identity is recorded with its supporting quantities and eligibility result, with no protected test information used.
ASSESSMENT ANCHOR: check_matched_cohort_and_fixed_requirement_eligibility facts=['f1', 'f2']
ASSESSMENT ANCHOR: derive_conditional_error_rates_and_identify_undefined_rates facts=['f3']
ASSESSMENT ANCHOR: calculate_expected_error_cost_and_rank_eligible_records facts=['f2', 'f4']
ASSESSMENT ANCHOR: freeze_validation_choice_without_protected_test_information facts=['f5']

## DATA ASSETS USED
ds.acceptance_contract: Precommitted predictive contract — columns: deployment_negative_probability(numerical), deployment_positive_probability(numerical), cost_FP(numerical), cost_FN(numerical), correct_prediction_cost(numerical), expected_cost_bound(numerical), selection_rule(categorical), tie_rule(categorical), empty_group_rule(categorical), ddof(numerical), operating_limit(numerical)
   [0.8,0.2,1,5,0,0.3,"minimum expected cost among matched eligible records","first in declared order","undefined rate; ineligible when required",0,null]
ds.candidate_records: Baseline and three candidate records — columns: candidate_id(identifier), cohort_id(identifier), TP(numerical), FP(numerical), FN(numerical), TN(numerical), actual_positive_count(numerical), actual_negative_count(numerical), cohort_count(numerical), precision(numerical), recall(numerical), validation_prevalence(numerical), FPR(numerical), FNR(numerical), expected_error_cost(numerical), latency_requirement_met(categorical), scale_requirement_met(categorical), training_cost_requirement_met(categorical), serving_cost_requirement_met(categorical), maintenance_requirement_met(categorical), deployment_compatibility_met(categorical)
   ["A","orders_100",16,12,4,68,20,80,100,0.5714285714285714,0.8,0.2,0.15,0.2,0.32000000000000006,true,true,true,true,true,true]
   ["B","orders_100",16,8,4,72,20,80,100,0.6666666666666666,0.8,0.2,0.1,0.2,0.28,true,true,true,true,true,true]
   ["C","other_orders_100",16,0,4,80,20,80,100,1.0,0.8,0.2,0.0,0.2,0.20000000000000004,true,true,true,true,true,true]
   ["D","orders_100",16,8,4,72,20,80,100,0.6666666666666666,0.8,0.2,0.1,0.2,0.28,false,true,true,true,true,true]
   variant v.candidates_none_eligible: 4 ops; planted: 
ds.threshold_records: Computed threshold validation evidence — columns: threshold(numerical), TP(numerical), FP(numerical), FN(numerical), TN(numerical), actual_positive_count(numerical), actual_negative_count(numerical), cohort_count(numerical), precision(numerical), recall(numerical), validation_prevalence(numerical), FPR(numerical), FNR(numerical), expected_error_cost(numerical), predictive_requirement_met(categorical)
   [0.5,16,8,4,72,20,80,100,0.6666666666666666,0.8,0.2,0.1,0.2,0.28,true]
   [0.7,16,5,4,75,20,80,100,0.7619047619047619,0.8,0.2,0.0625,0.2,0.25000000000000006,true]
ds.thresholds: Declared threshold candidates — columns: threshold(numerical), score_representation(categorical), declared_order(numerical)
   [0.5,"probability",0]
   [0.7,"probability",1]
ds.validation_scores: One fixed labeled cohort with unchanged scores — columns: observation_id(identifier), cohort_id(identifier), actual_label(categorical,digits-as-label), score(numerical), reference_output(categorical,digits-as-label)
   ["order_001","orders_100",1,0.8,0]
   ["order_002","orders_100",1,0.8,0]
   ["order_003","orders_100",1,0.8,0]
   ["order_004","orders_100",1,0.8,0]
   ["order_005","orders_100",1,0.8,0]
   ["order_006","orders_100",1,0.8,0]
   ["order_007","orders_100",1,0.8,0]
   ["order_008","orders_100",1,0.8,0]
   variant v.scores_no_positives: 1 ops; planted: 
   variant v.scores_no_negatives: 1 ops; planted: 
   variant v.scores_none_eligible: 100 ops; planted: 

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose CPU or GPU capacity for a bounded training workload; Choose a task-compatible training loss; Choose practical mitigations for documented subgroup-performance risks; Compare model candidates against a baseline using validation evidence before freezing the choice; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Control random seeds for reproducible training comparisons; Define a neural network with task-compatible layers and activations; Diagnose training failures from loss and gradient behavior; Diagnose training memory exhaustion; Document model limitations and foreseeable misuse under an existing risk policy; Evaluate important data slices for subgroup performance gaps; Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline; Implement the minibatch forward, backward and optimizer-step loop; Inspect prediction errors for recurring failure modes; 

## LESSON, in learner order

### s01 · explainer · Choose and freeze
(intro) The same scores can yield different class decisions. Make the threshold explicit, evaluate supplied candidates on validation, and freeze the chosen rule. ⟦A:tb1⟧
(mechanism) A score is not a class decision: comparing it with a threshold produces the decision. Binary scikit-learn probability scores ordinarily use a 0.5 cutoff; decision_function scores use zero. An explicit task threshold changes the decision. For each supplied threshold, form labels and count TP, FP, TN and FN against validation labels. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Choose the eligible threshold minimizing predeclared validation expected cost, then freeze it before protected testing. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups yield undefined rates. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦A.f4 A.f5 A.f6 A:tb3⟧
[TABLE ds.threshold_records cols=['threshold', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'predictive_requirement_met'] ] caption: Computed threshold validation evidence
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract
[TABLE computed result ] caption: Same supplied score, different threshold-dependent decisions.
  produced by sql: SELECT v.observation_id, v.score, t.threshold, v.score >= t.threshold AS predicted_positive FROM scores v CROSS JOIN thresholds t WHERE v.score > (SELECT MIN(threshold) FROM thresholds) AND v.score < (SELECT MAX(threshold) FROM thresholds) ORDER BY v.observation_id, t.declared_order
  result columns=['observation_id', 'score', 'threshold', 'predicted_positive'] rows(6)=[["order_026",0.6,0.5,true],["order_026",0.6,0.7,false],["order_027",0.6,0.5,true],["order_027",0.6,0.7,false],["order_028",0.6,0.5,true],["order_028",0.6,0.7,false]]

### s02 · explainer · Protect the test boundary
(mechanism) Using protected-test observations to fit preprocessing, choose a model or tune settings leaks information into the selected system. Keep them outside those choices. ⟦A.f7 A:tb4⟧

### s03 · explainer · Compare threshold records
(example) Compare supplied thresholds against the same scores and labels. A score between two thresholds changes class decision without changing score. Recount errors at each threshold, apply the fixed costs and eligibility limits, then retain the minimum-cost eligible rule. The ordinary probability and decision_function cutoffs belong to different score representations; do not treat them as interchangeable. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb5⟧

### s04 · explainer · Do not change the score story
(misconception) A threshold changes the decision, not the score. Choose with fixed validation evidence and freeze it before protected testing; do not tune on protected-test results. ⟦A.f1 A.f4 A.f7 A:tb6⟧

### s05 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.
QUESTION [choice, intro, grading=client] An order has a fixed probability score of 0.60. Changing the threshold from 0.50 to 0.70 changes its class decision. Which statement is correct?
  ✔ o1: The score is unchanged; comparing it with a different threshold changes the decision.
      why: A score and the thresholded class decision are distinct outputs.
  ✘ o2: The score must change to 0.70 when that threshold is selected.
      why: The threshold is a decision rule, not a replacement score.
  ✘ o3: Threshold selection changes the actual validation label.
      why: The observed actual label is not altered by choosing a threshold.
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r01
  MEASURES: A:distinguish_scores_from_thresholded_decisions(f1,f2)   anchors=['assessment:distinguish_scores_from_thresholded_decisions']
  taught-before-tested: A.f1←s01; A.f2←s01

### s06 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.
QUESTION [code_exercise, intro, grading=client] Complete the thresholded prediction expression, the four confusion-count masks, and the guarded FPR/FNR division expressions. Use scores >= threshold and compare predictions with y. Preserve the supplied eligibility, retention and return logic.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy', 'pandas']} constraints.allowed=['import numpy as np', 'imports for dependencies required by supplied scaffolding', 'def with parameters and return statements', 'local variable assignment', 'numeric and string literals', 'lists and dictionaries', 'for loops over supplied candidate thresholds', 'if and else conditionals', 'NumPy array conversion and shape checks', 'elementwise score comparisons', 'elementwise binary-label comparisons', 'boolean array operations', 'np.count_nonzero', 'arithmetic expressions with guarded division', 'dictionary and list indexing', 'calls to supplied eligibility and threshold-retention interfaces'] blocked=6 items
  file main.py [editable]:
# Supplied input loading and dependencies.
import pandas as pd

contract = pd.read_csv('acceptance_contract.csv').iloc[0]

p_negative = contract['deployment_negative_probability']

p_positive = contract['deployment_positive_probability']

cost_FP = contract['cost_FP']

cost_FN = contract['cost_FN']

bound = contract['expected_cost_bound']

observations = pd.read_csv('validation_scores.csv')

y = observations['actual_label'].to_numpy()

scores = observations['score'].to_numpy()

thresholds = pd.read_csv('thresholds.csv')['threshold'].tolist()

import numpy as np

count_errors = np.count_nonzero

# Supplied evaluation scaffold. Complete the marked expressions; preserve the rest.
if __name__:
    def evaluate(scores, y, thresholds, p_negative, p_positive, cost_FP, cost_FN, bound):
        records = []
        selected = None
        best_cost = None
        for threshold in thresholds:
            predictions = None  # TODO: threshold the scores
            FP = conditional_count(None)  # TODO: FP mask
            TN = conditional_count(None)  # TODO: TN mask
            FN = conditional_count(None)  # TODO: FN mask
            TP = conditional_count(None)  # TODO: TP mask
            negative_count = FP + TN
            positive_count = FN + TP
            FPR = None
            FNR = None
            expected_cost = None
            if negative_count > 0:
                FPR = None  # TODO: conditioned negative rate
            if positive_count > 0:
                FNR = None  # TODO: conditioned positive rate
            if negative_count > 0:
                if positive_count > 0:
                    expected_cost = p_negative * FPR * cost_FP + p_positive * FNR * cost_FN
            record = {'FP': FP, 'TN': TN, 'FN': FN, 'TP': TP, 'actual_negative_count': negative_count, 'actual_positive_count': positive_count, 'FPR': FPR, 'FNR': FNR, 'expected_cost': expected_cost, 'threshold': threshold, 'score_representation': 'probability'}
            records.append(record)
            if expected_cost is not None:
                if expected_cost <= bound:
                    if best_cost is None:
                        best_cost = expected_cost
                        selected = threshold
                    elif expected_cost < best_cost:
                        best_cost = expected_cost
                        selected = threshold
        return {'records': records, 'selected_threshold': selected, 'score_representation': 'probability'}

# Supplied callable operations; keep these assignments unchanged.
supplied_np_count_nonzero = np.count_nonzero

# Supplied counting callable.
conditional_count = np.count_nonzero

  SOLUTION main.py:
# Supplied input loading and dependencies.
import pandas as pd

contract = pd.read_csv('acceptance_contract.csv').iloc[0]

p_negative = contract['deployment_negative_probability']

p_positive = contract['deployment_positive_probability']

cost_FP = contract['cost_FP']

cost_FN = contract['cost_FN']

bound = contract['expected_cost_bound']

observations = pd.read_csv('validation_scores.csv')

y = observations['actual_label'].to_numpy()

scores = observations['score'].to_numpy()

thresholds = pd.read_csv('thresholds.csv')['threshold'].tolist()

import numpy as np

count_errors = np.count_nonzero

# Supplied evaluation scaffold. Preserve the scaffold outside the requested TODO expressions.
if __name__:
    def evaluate(scores, y, thresholds, p_negative, p_positive, cost_FP, cost_FN, bound):
        records = []
        selected = None
        best_cost = None
        for threshold in thresholds:
            predictions = scores >= threshold
            FP = conditional_count((y == 0) & (predictions == 1))
            TN = conditional_count((y == 0) & (predictions == 0))
            FN = conditional_count((y == 1) & (predictions == 0))
            TP = conditional_count((y == 1) & (predictions == 1))
            negative_count = FP + TN
            positive_count = FN + TP
            FPR = None
            FNR = None
            expected_cost = None
            if negative_count > 0:
                FPR = FP / negative_count
            if positive_count > 0:
                FNR = FN / positive_count
            if negative_count > 0:
                if positive_count > 0:
                    expected_cost = p_negative * FPR * cost_FP + p_positive * FNR * cost_FN
            record = {'FP': FP, 'TN': TN, 'FN': FN, 'TP': TP, 'actual_negative_count': negative_count, 'actual_positive_count': positive_count, 'FPR': FPR, 'FNR': FNR, 'expected_cost': expected_cost, 'threshold': threshold, 'score_representation': 'probability'}
            records.append(record)
            if expected_cost is not None:
                if expected_cost <= bound:
                    if best_cost is None:
                        best_cost = expected_cost
                        selected = threshold
                    elif expected_cost < best_cost:
                        best_cost = expected_cost
                        selected = threshold
        return {'records': records, 'selected_threshold': selected, 'score_representation': 'probability'}

# Supplied callable operations; keep these assignments unchanged.
supplied_np_count_nonzero = np.count_nonzero

# Complete only the final counting-operation binding.
conditional_count = np.count_nonzero

  test t1 (value_equals, visible=True): {"expr":"evaluate(scores, y, thresholds, p_negative, p_positive, cost_FP, cost_FN, bound)","expected":{"records":[{"FP":8,"TN":72,"FN":4,"TP":16,"actual_negative_count":80,"actual_positive_count":20,"FPR":0.1,"FNR":0.2,"expected_cost":0.28,"threshold":0.5,"score_representation":"probability"},{"FP":5,"TN":75,"FN":4,"TP":16,"actual_negative_count":80,"actual_positive_count":20,"FPR":0.0625,"FNR":0.2,"expected_cost":0.25000000000000006,"threshold":0.7,"score_representation":"probability"}],"select | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  test t2 (value_equals, visible=False): {"expr":"evaluate(scores[y == 0], y[y == 0], thresholds, p_negative, p_positive, cost_FP, cost_FN, bound)","expected":{"records":[{"FP":8,"TN":72,"FN":0,"TP":0,"actual_negative_count":80,"actual_positive_count":0,"FPR":0.1,"FNR":null,"expected_cost":null,"threshold":0.5,"score_representation":"probability"},{"FP":5,"TN":75,"FN":0,"TP":0,"actual_negative_count":80,"actual_positive_count":0,"FPR":0.0625,"FNR":null,"expected_cost":null,"threshold":0.7,"score_representation":"probability"}],"selecte | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  test t3 (value_equals, visible=False): {"expr":"evaluate(scores, y, thresholds, p_negative, p_positive, cost_FP, cost_FN, -1)","expected":{"records":[{"FP":8,"TN":72,"FN":4,"TP":16,"actual_negative_count":80,"actual_positive_count":20,"FPR":0.1,"FNR":0.2,"expected_cost":0.28,"threshold":0.5,"score_representation":"probability"},{"FP":5,"TN":75,"FN":4,"TP":16,"actual_negative_count":80,"actual_positive_count":20,"FPR":0.0625,"FNR":0.2,"expected_cost":0.25000000000000006,"threshold":0.7,"score_representation":"probability"}],"selected_ | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"10ae20291a926a0f6acd209e499ba2c2d0c713f6555eb6fa7a3854534e68d56b","tests_passed":3}
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Complete only the indicated expressions using the supplied inputs.', 'Keep guards, structured evidence and result fields unchanged.']  remediation→r02
  MEASURES: A:calculate_threshold_confusion_counts_and_conditional_error_rates(f3,f5); A:select_minimum_cost_eligible_validation_threshold(f4,f6); A:freeze_threshold_without_using_protected_test_observations(f4,f7)   anchors=['practice', 'assessment:calculate_threshold_confusion_counts_and_conditional_error_rates', 'assessment:select_minimum_cost_eligible_validation_threshold', 'assessment:freeze_threshold_without_using_protected_test_observations']
  taught-before-tested: A.f3←s01; A.f5←s01; A.f4←s01; A.f6←s01; A.f4←s01; A.f7←s02

### s07 · explainer · Fixed cost and test boundaries
(intro) Start with comparable records and eligibility, not the smallest displayed number. Baseline and candidates must answer the same evaluation question. ⟦B:tb1⟧
(mechanism) Compare baseline and candidates on the same evaluation dataset and predeclared requirements. Compute each cost using identical supplied deployment probabilities and error costs. Exclude records failing fixed limits; rank eligible records by the declared cost rule. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups give undefined rates. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose a model or tune settings without leaking information. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.candidate_records cols=['candidate_id', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'latency_requirement_met', 'scale_requirement_met', 'training_cost_requirement_met', 'serving_cost_requirement_met', 'maintenance_requirement_met', 'deployment_compatibility_met'] ] caption: Baseline and three candidate records
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract
[TABLE computed result ] caption: Fixed-contract eligibility and retained validation selection; null rates remain undefined.
  produced by sql: WITH rates AS (
SELECT r.*, 1.0*r.FP/NULLIF(r.FP+r.TN,0) AS conditioned_FPR,
1.0*r.FN/NULLIF(r.FN+r.TP,0) AS conditioned_FNR,
c.deployment_negative_probability, c.deployment_positive_probability, c.cost_FP, c.cost_FN,
c.expected_cost_bound, (r.latency_requirement_met = TRUE AND r.scale_requirement_met = TRUE AND r.training_cost_requirement_met = TRUE AND r.serving_cost_requirement_met = TRUE AND r.maintenance_requirement_met = TRUE AND r.deployment_compatibility_met = TRUE) AS operating_met,
r.cohort_id = 'orders_100' AS matched_cohort, r.candidate_id AS tie_order 
FROM records r CROSS JOIN contract c  
), costs AS (
SELECT *, deployment_negative_probability*conditioned_FPR*cost_FP + deployment_positive_probability*conditioned_FNR*cost_FN AS computed_cost FROM rates
), eligible AS (
SELECT *, CASE WHEN NOT matched_cohort THEN 'different cohort'
WHEN conditioned_FPR IS NULL OR conditioned_FNR IS NULL THEN 'undefined required rate'
WHEN computed_cost > expected_cost_bound THEN 'quality bound failed'
WHEN NOT operating_met THEN 'operating requirement failed'
ELSE 'eligible' END AS eligibility_reason FROM costs
), ranked AS (
SELECT candidate_id, ROW_NUMBER() OVER (ORDER BY computed_cost, tie_order) AS eligible_rank
FROM eligible WHERE eligibility_reason = 'eligible'
)
SELECT a.candidate_id, a.cohort_id, a.FP+a.TN AS actual_negative_denominator,
a.FN+a.TP AS actual_positive_denominator, a.conditioned_FPR, a.conditioned_FNR,
a.computed_cost, a.expected_cost_bound, a.eligibility_reason,
b.eligible_rank, CASE WHEN b.eligible_rank=1 THEN TRUE ELSE FALSE END AS retained_selection
FROM eligible a LEFT JOIN ranked b ON a.candidate_id=b.candidate_id ORDER BY a.tie_order
  result columns=['candidate_id', 'cohort_id', 'actual_negative_denominator', 'actual_positive_denominator', 'conditioned_FPR', 'conditioned_FNR', 'computed_cost', 'expected_cost_bound', 'eligibility_reason', 'eligible_rank', 'retained_selection'] rows(4)=[["A","orders_100",80,20,0.15,0.2,0.32000000000000006,0.3,"quality bound failed",null,false],["B","orders_100",80,20,0.1,0.2,0.28,0.3,"eligible",1,true],["C","other_orders_100",80,20,0,0.2,0.20000000000000004,0.3,"different cohort",null,false],["D","orders_100",80,20,0.1,0.2,0.28,0.3,"operating requirement failed",null,false]]

### s08 · explainer · Inspect cohort identity
(example) Inspect cohort identity before comparing baseline and candidate costs. A lower number from a different cohort is not matched selection evidence. For matching records, retain confusion counts, conditioning totals and the fixed cost contract. Check quality and operating limits before ranking; do not change deployment probabilities after seeing which candidate benefits. Protected-test observations stay outside fitting and selection. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb4⟧

### s09 · explainer · Smallest is not necessarily eligible
(misconception) The smallest number need not be the eligible winner. Matched cohorts and fixed requirements are prerequisites, not checks to postpone until after selection. ⟦B.f1 B.f2 B:tb5⟧

### s10 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.
QUESTION [choice, core, grading=client] A record has a lower expected cost than the baseline but comes from a different validation cohort. What is defensible under a matched-cohort comparison rule?
  ✔ o1: Exclude it from this comparison until matched-cohort evidence is available.
      why: Comparable candidate evidence uses the same evaluation dataset.
  ✘ o2: Select it immediately because its cost is lower.
      why: A lower cost on another cohort does not satisfy the matched-evidence rule.
  ✘ o3: Treat all equally sized cohorts as interchangeable.
      why: Equal sample counts do not establish observation correspondence.
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r03
  MEASURES: B:check_matched_cohort_and_fixed_requirement_eligibility(f1,f2)   anchors=['assessment:check_matched_cohort_and_fixed_requirement_eligibility']
  taught-before-tested: B.f1←s07; B.f2←s07

### s11 · hands_on · Calculate from the supplied evidence
 — Use the supplied dataset and fixed contract. Keep the conditioning population explicit when entering the requested formula.
QUESTION [formula_entry, stretch, grading=client] Row template
Read every supplied record. You may use helper-cell calculations for rates, costs, reasons and ranks; in AZ1 assemble the prescribed semicolon-separated comparison record. For each row, in declared order, output <identity>: neg=<FP+TN>,pos=<FN+TP>,FPR=<two decimals or undefined>,FNR=<two decimals or undefined>,cost=<two decimals or undefined>,eligible=<yes/no>,reason=<different cohort|undefined required rate|quality bound failed|operating requirement failed|eligible>,rank=<eligible rank or none>; 

Eligibility and selection
Apply the fixed orders_100 cohort, expected-cost <= 0.30, every supplied operating flag, and defined required rates. Rank eligible records by lowest cost; ties use declared order. When several exclusion conditions hold, assign the first applicable reason in this exact precedence: different cohort, undefined required rate, quality bound failed, operating requirement failed; otherwise eligible. Rank eligible records by unrounded expected cost, then declared order.

Append selected=<identity or none>, then the exact fixed suffix:
; fixed p0=0.80,p1=0.20,costFP=1,costFN=5,correct cost=0,bound=0.30; exclude unmatched cohorts, operating failures and unresolved required rates before cost ranking; ties use declared order; no protected-test evidence. 
  [unrendered interaction type formula_entry] public={"prompt":"Row template\nRead every supplied record. You may use helper-cell calculations for rates, costs, reasons and ranks; in AZ1 assemble the prescribed semicolon-separated comparison record. For each row, in declared order, output <identity>: neg=<FP+TN>,pos=<FN+TP>,FPR=<two decimals or undefined>,FNR=<two decimals or undefined>,cost=<two decimals or undefined>,eligible=<yes/no>,reason=<different cohort|undefined required rate|quality bound failed|operating requirement failed|eligible>,rank=<eligible rank or none>; \n\nEligibility and selection\nApply the fixed orders_100 cohort, expected-cost <= 0.30, every supplied operating flag, and defined required rates. Rank eligible records by lowest cost; ties use declared order. When several exclusion conditions hold, assign the first applicable reason in this exact precedence: different cohort, undefined required rate, quality bound fail grading={"reference_formula":"=A2&\": neg=\"&(D2+F2)&\",pos=\"&(E2+C2)&\",FPR=\"&IF((D2+F2)>0,TEXT(D2/(D2+F2),\"0.00\"),\"undefined\")&\",FNR=\"&IF((E2+C2)>0,TEXT(E2/(E2+C2),\"0.00\"),\"undefined\")&\",cost=\"&IF(AND((D2+F2)>0,(E2+C2)>0),TEXT((0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),\"0.00\"),\"undefined\")&\",eligible=\"&IF(IF(AND((D2+F2)>0,(E2+C2)>0),AND(B2=\"orders_100\",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),FALSE),\"yes\",\"no\")&\",reason=\"&IF(B2<>\"orders_100\",\"different cohort\",IF(AND((D2+F2)>0,(E2+C2)>0),IF((0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)>0.30,\"quality bound failed\",IF(AND(P2,Q2,R2,S2,T2,U2),\"eligible\",\"operating requirement failed\")),\"undefined required rate\"))&\",rank=\"&IF(IF(AND((D2+F2)>0,(E2+C2)>0),AND(B2=\"orders_100\",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),FALSE),1+IF(IF(AND((D3+F3)>0,(E3+C3)>0),AND(B3=\"orders_100\",(0.8*D
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r04
  MEASURES: B:check_matched_cohort_and_fixed_requirement_eligibility(f1,f2); B:derive_conditional_error_rates_and_identify_undefined_rates(f3); B:calculate_expected_error_cost_and_rank_eligible_records(f2,f4); B:freeze_validation_choice_without_protected_test_information(f5)   anchors=['practice', 'assessment:check_matched_cohort_and_fixed_requirement_eligibility', 'assessment:derive_conditional_error_rates_and_identify_undefined_rates', 'assessment:calculate_expected_error_cost_and_rank_eligible_records', 'assessment:freeze_validation_choice_without_protected_test_information']
  taught-before-tested: B.f1←s07; B.f2←s07; B.f3←s07; B.f2←s07; B.f4←s07; B.f5←s07

### s12 · recap · Keep these distinctions
(takeaway) Scores and threshold-dependent decisions differ. Evaluate supplied thresholds on validation and freeze the eligible minimum-cost choice. Compare candidates only on matched cohorts, with fixed cost inputs and requirements. Keep protected-test observations outside fitting and selection. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 B.f1 B.f2 B.f3 B.f4 B.f5 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5⟧
[UP NEXT] Up next: Inspect prediction failures in predefined groups.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: the check — score versus decision
(misconception) Contrast a fixed score with its threshold-dependent class decision. Recount validation errors for each supplied threshold before freezing a choice. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb2 A:tb3 A:tb4⟧
(mechanism) A score is not a class decision: comparing it with a threshold produces the decision. Binary scikit-learn probability scores ordinarily use a 0.5 cutoff; decision_function scores use zero. An explicit task threshold changes the decision. For each supplied threshold, form labels and count TP, FP, TN and FN against validation labels. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Choose the eligible threshold minimizing predeclared validation expected cost, then freeze it before protected testing. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups yield undefined rates. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(mechanism) Using protected-test observations to fit preprocessing, choose a model or tune settings leaks information into the selected system. Keep them outside those choices. ⟦A.f7 A:tb4⟧
[TABLE ds.threshold_records cols=['threshold', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'predictive_requirement_met'] ] caption: Computed threshold validation evidence
### r02 · Revisit: the practice — score versus decision
(misconception) Contrast a fixed score with its threshold-dependent class decision. Recount validation errors for each supplied threshold before freezing a choice. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb2 A:tb3 A:tb4⟧
(mechanism) A score is not a class decision: comparing it with a threshold produces the decision. Binary scikit-learn probability scores ordinarily use a 0.5 cutoff; decision_function scores use zero. An explicit task threshold changes the decision. For each supplied threshold, form labels and count TP, FP, TN and FN against validation labels. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Choose the eligible threshold minimizing predeclared validation expected cost, then freeze it before protected testing. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups yield undefined rates. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(mechanism) Using protected-test observations to fit preprocessing, choose a model or tune settings leaks information into the selected system. Keep them outside those choices. ⟦A.f7 A:tb4⟧
[TABLE ds.threshold_records cols=['threshold', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'predictive_requirement_met'] ] caption: Computed threshold validation evidence
### r03 · Revisit: the check — compare like with like
(misconception) Contrast the lowest reported cost with the lowest eligible matched cost. A different-cohort record cannot win this comparison. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3⟧
(mechanism) Compare baseline and candidates on the same evaluation dataset and predeclared requirements. Compute each cost using identical supplied deployment probabilities and error costs. Exclude records failing fixed limits; rank eligible records by the declared cost rule. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups give undefined rates. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose a model or tune settings without leaking information. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.candidate_records cols=['candidate_id', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'latency_requirement_met', 'scale_requirement_met', 'training_cost_requirement_met', 'serving_cost_requirement_met', 'maintenance_requirement_met', 'deployment_compatibility_met'] ] caption: Baseline and three candidate records
### r04 · Revisit: the practice — compare like with like
(misconception) Contrast the lowest reported cost with the lowest eligible matched cost. A different-cohort record cannot win this comparison. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3⟧
(mechanism) Compare baseline and candidates on the same evaluation dataset and predeclared requirements. Compute each cost using identical supplied deployment probabilities and error costs. Exclude records failing fixed limits; rank eligible records by the declared cost rule. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups give undefined rates. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose a model or tune settings without leaking information. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.candidate_records cols=['candidate_id', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'latency_requirement_met', 'scale_requirement_met', 'training_cost_requirement_met', 'serving_cost_requirement_met', 'maintenance_requirement_met', 'deployment_compatibility_met'] ] caption: Baseline and three candidate records

## OTHER CONTENT (fields without a dedicated renderer)
· grading.reference_formula: =A2&": neg="&(D2+F2)&",pos="&(E2+C2)&",FPR="&IF((D2+F2)>0,TEXT(D2/(D2+F2),"0.00"),"undefined")&",FNR="&IF((E2+C2)>0,TEXT(E2/(E2+C2),"0.00"),"undefined")&",cost="&IF(AND((D2+F2)>0,(E2+C2)>0),TEXT((0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),"0.00"),"undefined")&",eligible="&IF(IF(AND((D2+F2)>0,(E2+C2)>0),AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),FALSE),"yes","no")&",reason="&IF(B2<>"orders_100","different cohort",IF(AND((D2+F2)>0,(E2+C2)>0),IF((0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)>0.30,"quality bound failed",IF(AND(P2,Q2,R2,S2,T2,U2),"eligible","operating requirement failed")),"undefined required rate"))&",rank="&IF(IF(AND((D2+F2)>0,(E2+C2)>0),AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),FALSE),1+IF(IF(AND((D3+F3)>0,(E3+C3)>0),AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),FALSE),IF(IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000)<IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),1,IF(AND(IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000)=IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),3<2),1,0)),0)+IF(IF(AND((D4+F4)>0,(E4+C4)>0),AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),FALSE),IF(IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000)<IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),1,IF(AND(IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000)=IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),4<2),1,0)),0)+IF(IF(AND((D5+F5)>0,(E5+C5)>0),AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),FALSE),IF(IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)<IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),1,IF(AND(IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)=IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),5<2),1,0)),0),"none")&"; "&A3&": neg="&(D3+F3)&",pos="&(E3+C3)&",FPR="&IF((D3+F3)>0,TEXT(D3/(D3+F3),"0.00"),"undefined")&",FNR="&IF((E3+C3)>0,TEXT(E3/(E3+C3),"0.00"),"undefined")&",cost="&IF(AND((D3+F3)>0,(E3+C3)>0),TEXT((0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),"0.00"),"undefined")&",eligible="&IF(IF(AND((D3+F3)>0,(E3+C3)>0),AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),FALSE),"yes","no")&",reason="&IF(B3<>"orders_100","different cohort",IF(AND((D3+F3)>0,(E3+C3)>0),IF((0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)>0.30,"quality bound failed",IF(AND(P3,Q3,R3,S3,T3,U3),"eligible","operating requirement failed")),"undefined required rate"))&",rank="&IF(IF(AND((D3+F3)>0,(E3+C3)>0),AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),FALSE),1+IF(IF(AND((D2+F2)>0,(E2+C2)>0),AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),FALSE),IF(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000)<IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),1,IF(AND(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000)=IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),2<3),1,0)),0)+IF(IF(AND((D4+F4)>0,(E4+C4)>0),AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),FALSE),IF(IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000)<IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),1,IF(AND(IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000)=IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),4<3),1,0)),0)+IF(IF(AND((D5+F5)>0,(E5+C5)>0),AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),FALSE),IF(IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)<IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),1,IF(AND(IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)=IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),5<3),1,0)),0),"none")&"; "&A4&": neg="&(D4+F4)&",pos="&(E4+C4)&",FPR="&IF((D4+F4)>0,TEXT(D4/(D4+F4),"0.00"),"undefined")&",FNR="&IF((E4+C4)>0,TEXT(E4/(E4+C4),"0.00"),"undefined")&",cost="&IF(AND((D4+F4)>0,(E4+C4)>0),TEXT((0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),"0.00"),"undefined")&",eligible="&IF(IF(AND((D4+F4)>0,(E4+C4)>0),AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),FALSE),"yes","no")&",reason="&IF(B4<>"orders_100","different cohort",IF(AND((D4+F4)>0,(E4+C4)>0),IF((0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)>0.30,"quality bound failed",IF(AND(P4,Q4,R4,S4,T4,U4),"eligible","operating requirement failed")),"undefined required rate"))&",rank="&IF(IF(AND((D4+F4)>0,(E4+C4)>0),AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),FALSE),1+IF(IF(AND((D2+F2)>0,(E2+C2)>0),AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),FALSE),IF(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000)<IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),1,IF(AND(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000)=IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),2<4),1,0)),0)+IF(IF(AND((D3+F3)>0,(E3+C3)>0),AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),FALSE),IF(IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000)<IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),1,IF(AND(IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000)=IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),3<4),1,0)),0)+IF(IF(AND((D5+F5)>0,(E5+C5)>0),AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),FALSE),IF(IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)<IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),1,IF(AND(IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)=IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),5<4),1,0)),0),"none")&"; "&A5&": neg="&(D5+F5)&",pos="&(E5+C5)&",FPR="&IF((D5+F5)>0,TEXT(D5/(D5+F5),"0.00"),"undefined")&",FNR="&IF((E5+C5)>0,TEXT(E5/(E5+C5),"0.00"),"undefined")&",cost="&IF(AND((D5+F5)>0,(E5+C5)>0),TEXT((0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),"0.00"),"undefined")&",eligible="&IF(IF(AND((D5+F5)>0,(E5+C5)>0),AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),FALSE),"yes","no")&",reason="&IF(B5<>"orders_100","different cohort",IF(AND((D5+F5)>0,(E5+C5)>0),IF((0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)>0.30,"quality bound failed",IF(AND(P5,Q5,R5,S5,T5,U5),"eligible","operating requirement failed")),"undefined required rate"))&",rank="&IF(IF(AND((D5+F5)>0,(E5+C5)>0),AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),FALSE),1+IF(IF(AND((D2+F2)>0,(E2+C2)>0),AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),FALSE),IF(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000)<IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000),1,IF(AND(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000)=IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000),2<5),1,0)),0)+IF(IF(AND((D3+F3)>0,(E3+C3)>0),AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),FALSE),IF(IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000)<IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000),1,IF(AND(IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000)=IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000),3<5),1,0)),0)+IF(IF(AND((D4+F4)>0,(E4+C4)>0),AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),FALSE),IF(IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000)<IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000),1,IF(AND(IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000)=IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000),4<5),1,0)),0),"none")&"; "&"selected="&IF(IF(AND((D2+F2)>0,(E2+C2)>0),AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),FALSE),IF(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000)=MIN(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)),A2,IF(IF(AND((D3+F3)>0,(E3+C3)>0),AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),FALSE),IF(IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000)=MIN(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)),A3,IF(IF(AND((D4+F4)>0,(E4+C4)>0),AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),FALSE),IF(IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000)=MIN(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)),A4,IF(IF(AND((D5+F5)>0,(E5+C5)>0),AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),FALSE),IF(IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)=MIN(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)),A5,"none"),"none")),IF(IF(AND((D5+F5)>0,(E5+C5)>0),AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),FALSE),IF(IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)=MIN(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)),A5,"none"),"none"))),IF(IF(AND((D4+F4)>0,(E4+C4)>0),AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),FALSE),IF(IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000)=MIN(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)),A4,IF(IF(AND((D5+F5)>0,(E5+C5)>0),AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),FALSE),IF(IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)=MIN(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)),A5,"none"),"none")),IF(IF(AND((D5+F5)>0,(E5+C5)>0),AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),FALSE),IF(IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)=MIN(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)),A5,"none"),"none")))),IF(IF(AND((D3+F3)>0,(E3+C3)>0),AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),FALSE),IF(IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000)=MIN(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)),A3,IF(IF(AND((D4+F4)>0,(E4+C4)>0),AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),FALSE),IF(IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000)=MIN(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)),A4,IF(IF(AND((D5+F5)>0,(E5+C5)>0),AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),FALSE),IF(IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)=MIN(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)),A5,"none"),"none")),IF(IF(AND((D5+F5)>0,(E5+C5)>0),AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),FALSE),IF(IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)=MIN(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)),A5,"none"),"none"))),IF(IF(AND((D4+F4)>0,(E4+C4)>0),AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),FALSE),IF(IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000)=MIN(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)),A4,IF(IF(AND((D5+F5)>0,(E5+C5)>0),AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),FALSE),IF(IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)=MIN(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)),A5,"none"),"none")),IF(IF(AND((D5+F5)>0,(E5+C5)>0),AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),FALSE),IF(IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)=MIN(IF(AND((D2+F2)>0,(E2+C2)>0),IF(AND(B2="orders_100",(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5)<=0.30,AND(P2,Q2,R2,S2,T2,U2)),(0.8*D2/(D2+F2)+0.2*E2/(E2+C2)*5),1000000),1000000),IF(AND((D3+F3)>0,(E3+C3)>0),IF(AND(B3="orders_100",(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5)<=0.30,AND(P3,Q3,R3,S3,T3,U3)),(0.8*D3/(D3+F3)+0.2*E3/(E3+C3)*5),1000000),1000000),IF(AND((D4+F4)>0,(E4+C4)>0),IF(AND(B4="orders_100",(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5)<=0.30,AND(P4,Q4,R4,S4,T4,U4)),(0.8*D4/(D4+F4)+0.2*E4/(E4+C4)*5),1000000),1000000),IF(AND((D5+F5)>0,(E5+C5)>0),IF(AND(B5="orders_100",(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5)<=0.30,AND(P5,Q5,R5,S5,T5,U5)),(0.8*D5/(D5+F5)+0.2*E5/(E5+C5)*5),1000000),1000000)),A5,"none"),"none"))))&"; fixed p0=0.80,p1=0.20,costFP=1,costFN=5,correct cost=0,bound=0.30; exclude unmatched cohorts, operating failures and unresolved required rates before cost ranking; ties use declared order; no protected-test evidence."
· grading.expected_value: A: neg=80,pos=20,FPR=0.15,FNR=0.20,cost=0.32,eligible=no,reason=quality bound failed,rank=none; B: neg=80,pos=20,FPR=0.10,FNR=0.20,cost=0.28,eligible=yes,reason=eligible,rank=1; C: neg=80,pos=20,FPR=0.00,FNR=0.20,cost=0.20,eligible=no,reason=different cohort,rank=none; D: neg=80,pos=20,FPR=0.10,FNR=0.20,cost=0.28,eligible=no,reason=operating requirement failed,rank=none; selected=B; fixed p0=0.80,p1=0.20,costFP=1,costFN=5,correct cost=0,bound=0.30; exclude unmatched cohorts, operating failures and unresolved required rates before cost ranking; ties use declared order; no protected-test evidence.

=========

# EVALUATOR PACKET — Failure groups, slices and mitigation (mle.tile.026_028)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.prediction_error_analysis — Inspect prediction errors for recurring failure modes
B = mle.slice_evaluation — Evaluate important data slices for subgroup performance gaps
C = mle.subgroup_risk_mitigation — Choose practical mitigations for documented subgroup-performance risks

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=8
  warn: mle.tile.026_028.s01: prose block without lineage.fact_ids
  warn: mle.tile.026_028.s05/ix.mle.tile.026_028.s05: ADVISORY — syntax descriptors with no detector: ['Boolean array indexing', 'Boolean masks', 'NumPy arrays', 'arithmetic division', 'array comparisons', 'dictionary literals', 'function parameters', 'numeric and string literals']
  warn: mle.tile.026_028.s06: prose block without lineage.fact_ids
  warn: mle.tile.026_028.s11/ix.mle.tile.026_028.s11: ADVISORY — syntax descriptors with no detector: ['Boolean masks and comparisons', 'GridSearchCV', 'RandomizedSearchCV', 'arithmetic operators', 'array indexing', 'for loops', 'function parameters and calls', 'if statements', 'len', 'lists and dictionaries', 'numeric and string literals']
  warn: mle.tile.026_028.s12: prose block without lineage.fact_ids
  warn: plan: mle.tile.026_028.s04 was planned to measure mle.prediction_error_analysis#assessment:interpret_loss_mean_and_standard_deviation_for_selected_observations but its interaction does not
  warn: plan: mle.tile.026_028.s10 was planned to measure mle.slice_evaluation#assessment:calculate_slice_means_and_standard_deviations_with_the_required_divisor but its interaction does not
  warn: plan: mle.tile.026_028.s15 was planned to measure mle.subgroup_risk_mitigation#assessment:justify_mitigation_with_population_weighted_error_harm but its interaction does not

## SOURCE FACTS — A (mle.prediction_error_analysis)   objective: Explain a localized model failure with conditional error and feature-summary evidence.
A.f1: Inspect prediction failures rather than assuming the developer’s own usage represents the user population.   [sources: google_rules_of_ml#Rule #23: You are not a typical end user.]
A.f2: For a predefined failure group, count its errors and divide by its eligible observation count to obtain its conditional error proportion.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f3: Compare the group’s quality evidence with the same-cohort reference to localize an observed failure instead of assuming an overall score describes every segment.   [sources: google_mlops_pipelines#Data and model validation]
A.f4: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
A.f5: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Errors, Slices and Subgroup Risks.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python analysis function, including the required NumPy import, that inspects supplied order-model validation errors. Preserve the predefined long-distance group, compute its error count divided by its eligible observation count, and compute the mean and population standard deviation of supplied per-example losses. Compare the group's conditional error proportion and loss summaries with the supplied same-cohort reference, then report one recurring failure mode supported by the observations.  SUCCESS: The learner-written function returns the eligible count, error count, conditional error proportion, mean loss, and population standard deviation for the predefined group and its same-cohort reference. A descriptive finding identifies a recurring pattern in supplied failures, cites comparable evidence, and avoids claiming an untested cause.
ASSESSMENT ANCHOR: identify_recurring_failure_with_conditional_error_evidence facts=['f1', 'f2', 'f3']
ASSESSMENT ANCHOR: interpret_loss_mean_and_standard_deviation_for_selected_observations facts=['f4', 'f5']

## SOURCE FACTS — B (mle.slice_evaluation)   objective: Compare predefined validation slices without hiding their counts or representativeness limits.
B.f1: Overall model improvement can coexist with inconsistent performance across data segments, so evaluate the specified slices separately.   [sources: google_mlops_pipelines#Data and model validation]
B.f2: For each predefined slice, report its eligible observation count and errors divided by that count, retaining the conditioning population.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
B.f3: A sample can fail to represent its intended population, so observed sample slice differences do not by themselves establish a population-level disparity.   [sources: google_ml_crash_course#fairness — Types of bias]
B.f4: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
B.f5: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Errors, Slices and Subgroup Risks.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write one Python analysis function, including the required NumPy import, to calculate supplied validation metrics for predefined delivery-zone slices. Report eligible counts, conditional error probabilities, and per-slice loss means and standard deviations. Compare matched validation slices and describe one supported sample gap without claiming population-level disparity.  SUCCESS: The function returns each slice's eligible count, errors divided by that count, and the mean and standard deviation of its supplied loss observations. For the illustrative fixture, zone A reports 2/40 = 0.05 and zone B reports 6/20 = 0.30. The comparison retains both denominators, uses the declared standard-deviation divisor, and limits its conclusion to the observed validation slices.
ASSESSMENT ANCHOR: identify_slice_gaps_with_eligible_counts_and_conditional_error_rates facts=['f1', 'f2']
ASSESSMENT ANCHOR: distinguish_observed_slice_gaps_from_population_disparity facts=['f2', 'f3']
ASSESSMENT ANCHOR: calculate_slice_means_and_standard_deviations_with_the_required_divisor facts=['f4', 'f5']

## SOURCE FACTS — C (mle.subgroup_risk_mitigation)   objective: Choose a supported subgroup mitigation using population-weighted harm and validation evidence.
C.f1: Evaluate whether the data represents the groups for which the model is intended before attributing a subgroup problem solely to the model.   [sources: google_ml_crash_course#fairness — Types of bias]
C.f2: Check the supplied mitigation on the affected validation segment as well as the overall validation cohort before accepting it.   [sources: google_mlops_pipelines#Data and model validation]
C.f3: For a subgroup, its contribution to total expected harm is its deployment population probability multiplied by its subgroup-conditional expected harm; use the supplied error costs for that calculation.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
C.f4: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Errors, Slices and Subgroup Risks.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.slice_evaluation. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (spreadsheet): Using supplied reference and mitigation validation counts for the affected subgroup and overall cohort, calculate FPR and FNR with their respective conditioning denominators. Calculate subgroup prevalence within validation and keep it distinct from the supplied deployment population probability. Use supplied error costs and subgroup actual-class proportions to calculate subgroup-conditional expected harm and its population-weighted contribution. Select one supplied mitigation tied to the documented slice finding, inspect representation evidence, and state a validation check before comparing the mitigation results.  SUCCESS: FPR uses FP/(FP+TN), FNR uses FN/(FN+TP), and empty conditioning groups are marked undefined rather than zero. Validation subgroup prevalence is calculated as subgroup count divided by overall cohort count, without assuming it equals deployment population probability. Subgroup-conditional harm uses the supplied costs and actual-class proportions; its contribution to total expected harm multiplies that harm by the supplied deployment population probability. The selected mitigation addresses the documented risk, and the precommitted check applies supplied acceptance criteria to both the matched affected validation segment and overall cohort, with representation limitations stated.
ASSESSMENT ANCHOR: choose_mitigation_for_documented_subgroup_risk facts=['f1', 'f2']
ASSESSMENT ANCHOR: justify_mitigation_with_population_weighted_error_harm facts=['f3', 'f4']

## DATA ASSETS USED
ds.acceptance_contract: Precommitted predictive contract — columns: deployment_negative_probability(numerical), deployment_positive_probability(numerical), cost_FP(numerical), cost_FN(numerical), correct_prediction_cost(numerical), expected_cost_bound(numerical), selection_rule(categorical), tie_rule(categorical), empty_group_rule(categorical), ddof(numerical), operating_limit(numerical)
   [0.8,0.2,1,5,0,0.3,"minimum expected cost among matched eligible records","first in declared order","undefined rate; ineligible when required",0,null]
ds.aggregate_slice_evidence: Aggregate evidence from the matched slice cohort — columns: system(categorical), cohort_id(identifier), eligible_count(numerical), error_count(numerical), error_probability(numerical)
   ["reference","slices_60",60,12,0.2]
   ["model","slices_60",60,8,0.13333333333333333]
ds.mitigation_records: Matched reference and supplied mitigation harm — columns: system(categorical), scope(categorical), cohort_id(identifier), TP(numerical), FP(numerical), FN(numerical), TN(numerical), actual_positive_count(numerical), actual_negative_count(numerical), cohort_count(numerical), precision(numerical), recall(numerical), validation_prevalence(numerical), FPR(numerical), FNR(numerical), expected_error_cost(numerical), deployment_subgroup_probability(numerical), population_weighted_harm_contribution(numerical), representation_limitation(text), deployment_negative_probability(numerical), deployment_positive_probability(numerical), cost_FP(numerical), cost_FN(numerical), validation_subgroup_prevalence(numerical)
   ["reference","affected_subgroup","mitigation_validation",4,15,1,5,5,20,25,0.21052631578947367,0.8,0.2,0.75,0.2,0.8000000000000002,0.25,0.20000000000000004,"representation beyond supplied sample is not established",0.8,0.2,1,5,0.125]
   ["reference","overall","mitigation_validation",32,24,8,136,40,160,200,0.5714285714285714,0.8,0.2,0.15,0.2,0.32000000000000006,0.25,null,"representation beyond supplied sample is not established",0.8,0.2,1,5,0.125]
   ["mitigation","affected_subgroup","mitigation_validation",4,10,1,10,5,20,25,0.2857142857142857,0.8,0.2,0.5,0.2,0.6000000000000001,0.25,0.15000000000000002,"representation beyond supplied sample is not established",0.8,0.2,1,5,0.125]
   ["mitigation","overall","mitigation_validation",32,16,8,144,40,160,200,0.6666666666666666,0.8,0.2,0.1,0.2,0.28,0.25,null,"representation beyond supplied sample is not established",0.8,0.2,1,5,0.125]
ds.slice_observations: Predefined zones and long-distance observations — columns: observation_id(identifier), cohort_id(identifier), zone(categorical), eligible(categorical), long_distance(categorical), error(categorical), loss(numerical), reference_error(categorical), reference_loss(numerical), distance(numerical)
   ["slice_001","slices_60","A",true,true,true,1.0,true,1.0,5.0]
   ["slice_002","slices_60","A",true,true,true,1.0,true,1.0,7.0]
   ["slice_003","slices_60","A",true,true,false,0.0,true,1.0,9.0]
   ["slice_004","slices_60","A",true,true,false,0.0,true,1.0,11.0]
   ["slice_005","slices_60","A",true,true,false,0.0,false,0.0,13.0]
   ["slice_006","slices_60","A",true,true,false,0.0,false,0.0,15.0]
   ["slice_007","slices_60","A",true,true,false,0.0,false,0.0,17.0]
   ["slice_008","slices_60","A",true,true,false,0.0,false,0.0,19.0]
   variant v.empty_zone_B: 1 ops; planted: 
ds.slice_summary: Computed conditional slice summaries — columns: slice(categorical), eligible_count(numerical), error_count(numerical), error_probability(numerical), loss_mean(numerical), loss_std(numerical), ddof(numerical)
   ["A",40,2,0.05,0.05,0.21794494717703367,0]
   ["B",20,6,0.3,0.3,0.45825756949558394,0]
   ["long-distance",20,8,0.4,0.4,0.48989794855663565,0]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose CPU or GPU capacity for a bounded training workload; Choose a task-compatible training loss; Choose practical mitigations for documented subgroup-performance risks; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Control random seeds for reproducible training comparisons; Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point; Define a neural network with task-compatible layers and activations; Diagnose training failures from loss and gradient behavior; Diagnose training memory exhaustion; Document model limitations and foreseeable misuse under an existing risk policy; Evaluate important data slices for subgroup performance gaps; Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline; Freeze and identify a traceable dataset snapshot for reproducible training; Implement the minibatch forward, bac

## LESSON, in learner order

### s01 · explainer · Summarize selected observations
(intro) Investigate the predefined failure group rather than treating personally tried cases as representative of users. Keep its eligible population explicit. ⟦A:tb1⟧
(mechanism) Inspect prediction failures; developer usage does not necessarily represent users. For the predefined group, divide errors by eligible observations. Compare its quality evidence with the same-cohort reference to localize observed failure; an overall score does not describe every segment. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Summarize selected numeric observations with np.mean(numeric_values). Use np.std(numeric_values, ddof=0): squared deviations are divided by N before the square root. Use ddof=1 only when the specified calculation requires N−1. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.slice_observations cols=['observation_id', 'cohort_id', 'eligible', 'long_distance', 'error', 'loss', 'reference_error', 'reference_loss'] ] caption: Predefined zones and long-distance observations
[TABLE ds.slice_summary cols=['slice', 'eligible_count', 'error_count', 'error_probability', 'loss_mean', 'loss_std', 'ddof'] ] caption: Computed conditional slice summaries

### s02 · explainer · Inspect long-distance evidence
(example) The supplied observations identify eligibility and long-distance membership alongside model and reference errors and loss. Keep that group boundary when counting errors and eligible observations. Compare with the group’s same-cohort reference, not unrelated traffic. Selected loss mean and spread describe the measured observations; they do not establish a cause of failure or make developer-chosen examples representative of users. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4⟧

### s03 · explainer · Counts need denominators
(misconception) An overall score does not describe every segment. An error count without the eligible count hides the conditional proportion. ⟦A.f1 A.f2 A.f3 A:tb5⟧

### s04 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.
QUESTION [choice, intro, grading=client] A predefined long-distance group has a higher observed error proportion than its same-cohort reference. Which conclusion stays within the evidence?
  ✔ o1: The supplied group exhibits a recurring error pattern; these observations alone do not establish its cause.
      why: The finding is descriptive and bounded to comparable supplied evidence.
  ✘ o2: Distance has been proven to cause the errors.
      why: An observed error pattern alone does not test a causal explanation.
  ✘ o3: The developer's own usage disproves the supplied failure pattern.
      why: Personal developer usage is not a substitute for supplied failure observations.
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r01
  MEASURES: A:identify_recurring_failure_with_conditional_error_evidence(f1,f2,f3)   anchors=['assessment:identify_recurring_failure_with_conditional_error_evidence']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01

### s05 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.
QUESTION [code_exercise, core, grading=client] Select the supplied loss-summary operations for loss_mean_fn and loss_std_fn. Write a brief noncausal description comparing the measured long-distance model and reference results; retain the structured numerical evidence and limitation. Put your description in finding_description. Preserve the population standard deviations and supplied evaluator.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy', 'pandas']} constraints.allowed=['import numpy as np', 'def', 'function parameters', 'variable assignment', 'return', 'dictionary literals', 'numeric and string literals', 'NumPy arrays', 'Boolean masks', 'Boolean array indexing', 'array comparisons', 'np.count_nonzero(...)', 'array.size', 'arithmetic division', 'np.mean(numeric_values)', 'np.std(numeric_values, ddof=0)', 'np.std(numeric_values, ddof=1) only when an N−1 divisor is explicitly required'] blocked=9 items
  file main.py [editable]:
# Supplied input loading and dependencies.
import pandas as pd

observations = pd.read_csv('slice_observations.csv')

eligible = observations['eligible'].to_numpy()

long_distance = observations['long_distance'].to_numpy()

errors = observations['error'].to_numpy()

losses = observations['loss'].to_numpy()

reference_errors = observations['reference_error'].to_numpy()

reference_losses = observations['reference_loss'].to_numpy()

import numpy as np

# Supplied evaluation scaffold. Complete the marked expressions; preserve the rest.
if __name__:
    def evaluate(eligible, long_distance, errors, losses, reference_errors, reference_losses):
        group = (eligible == True) & (long_distance == True)
        n = conditional_count(group)
        error_count = conditional_count(errors[group])
        reference_count = conditional_count(reference_errors[group])
        error_proportion = error_count / n
        reference_error_proportion = reference_count / n
        loss_mean = loss_mean_fn(losses[group])
        loss_std = loss_std_fn(losses[group], ddof=0)
        reference_loss_mean = loss_mean_fn(reference_losses[group])
        reference_loss_std = loss_std_fn(reference_losses[group], ddof=0)
        description = finding_description
        return {'eligible_count': n, 'error_count': error_count, 'error_proportion': error_proportion, 'loss_mean': loss_mean, 'loss_std': loss_std, 'reference_eligible_count': n, 'reference_error_count': reference_count, 'reference_error_proportion': reference_error_proportion, 'reference_loss_mean': reference_loss_mean, 'reference_loss_std': reference_loss_std, 'finding': {'description': description, 'model': {'error_count': error_count, 'eligible_count': n, 'loss_mean': loss_mean, 'loss_std': loss_std}, 'reference': {'error_count': reference_count, 'eligible_count': n, 'loss_mean': reference_loss_mean, 'loss_std': reference_loss_std}, 'limitation': 'Observed eligible long-distance validation comparison only; no cause is established.'}}

# Supplied callable operations; keep these assignments unchanged.
supplied_np_count_nonzero = np.count_nonzero
supplied_np_mean = np.mean
supplied_np_std = np.std
conditional_count = supplied_np_count_nonzero
loss_mean_fn = None  # TODO: bind the supplied operation/value
loss_std_fn = None  # TODO: bind the supplied operation/value

# Callable/value bindings.
finding_description = None  # TODO: write your noncausal comparison as a string

  SOLUTION main.py:
# Supplied input loading and dependencies.
import pandas as pd

observations = pd.read_csv('slice_observations.csv')

eligible = observations['eligible'].to_numpy()

long_distance = observations['long_distance'].to_numpy()

errors = observations['error'].to_numpy()

losses = observations['loss'].to_numpy()

reference_errors = observations['reference_error'].to_numpy()

reference_losses = observations['reference_loss'].to_numpy()

import numpy as np

# Supplied evaluation scaffold. Preserve the scaffold outside the requested TODO expressions.
if __name__:
    def evaluate(eligible, long_distance, errors, losses, reference_errors, reference_losses):
        group = (eligible == True) & (long_distance == True)
        n = conditional_count(group)
        error_count = conditional_count(errors[group])
        reference_count = conditional_count(reference_errors[group])
        error_proportion = error_count / n
        reference_error_proportion = reference_count / n
        loss_mean = loss_mean_fn(losses[group])
        loss_std = loss_std_fn(losses[group], ddof=0)
        reference_loss_mean = loss_mean_fn(reference_losses[group])
        reference_loss_std = loss_std_fn(reference_losses[group], ddof=0)
        description = finding_description
        return {'eligible_count': n, 'error_count': error_count, 'error_proportion': error_proportion, 'loss_mean': loss_mean, 'loss_std': loss_std, 'reference_eligible_count': n, 'reference_error_count': reference_count, 'reference_error_proportion': reference_error_proportion, 'reference_loss_mean': reference_loss_mean, 'reference_loss_std': reference_loss_std, 'finding': {'description': description, 'model': {'error_count': error_count, 'eligible_count': n, 'loss_mean': loss_mean, 'loss_std': loss_std}, 'reference': {'error_count': reference_count, 'eligible_count': n, 'loss_mean': reference_loss_mean, 'loss_std': reference_loss_std}, 'limitation': 'Observed eligible long-distance validation comparison only; no cause is established.'}}

# Supplied callable operations; keep these assignments unchanged.
supplied_np_count_nonzero = np.count_nonzero
supplied_np_mean = np.mean
supplied_np_std = np.std
conditional_count = supplied_np_count_nonzero
loss_mean_fn = supplied_np_mean
loss_std_fn = supplied_np_std

# Supplied interpretation of the structured evidence (no causal inference).
supplied_observed_comparison = 'Long-distance validation errors persist. The measured model error proportion and mean loss are both lower than the reference in this sample; no cause is established.'

# Callable/value bindings.
finding_description = supplied_observed_comparison

  test t1 (value_equals, visible=True): {"expr":"{k: v for k, v in (evaluate(eligible, long_distance, errors, losses, reference_errors, reference_losses)).items() if k != \"finding\"}","expected":{"eligible_count":20,"error_count":8,"error_proportion":0.4,"loss_mean":0.4,"loss_std":0.48989794855663565,"reference_eligible_count":20,"reference_error_count":10,"reference_error_proportion":0.5,"reference_loss_mean":0.5,"reference_loss_std":0.5}} | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  test finding_evidence (value_equals, visible=True): {"expr":"({k: v for k, v in (evaluate(eligible, long_distance, errors, losses, reference_errors, reference_losses)).items() if k != \"finding\"}, (lambda r: all(r['finding'][side][key] == r[prefix + key] for side, prefix in [('model',''),('reference','reference_')] for key in ['error_count','eligible_count','loss_mean','loss_std']) and bool(r['finding']['limitation']) and isinstance(r['finding'].get('description'), str) and bool(r['finding']['description'].strip()))(evaluate(eligible, long_dista | on-fail: The finding must cite both measured error counts, denominators and loss summaries, with a noncausal limitation. Include a nonempty descriptive recurring pattern.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"16203702af51cf28068c0a3ee6bca73f75af03754fa29719690999ad5eedfc56","tests_passed":2}
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Complete only the indicated expressions using the supplied inputs.', 'Keep guards, structured evidence and result fields unchanged.']  remediation→r02
  MEASURES: A:identify_recurring_failure_with_conditional_error_evidence(f1,f2,f3); A:interpret_loss_mean_and_standard_deviation_for_selected_observations(f4,f5)   anchors=['practice', 'assessment:identify_recurring_failure_with_conditional_error_evidence', 'assessment:interpret_loss_mean_and_standard_deviation_for_selected_observations']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01; A.f5←s01

### s06 · explainer · Mean and spread
(intro) Evaluate predefined delivery zones separately even when the aggregate improves. Keep each slice’s observation count beside its quality result. ⟦B:tb1⟧
(mechanism) Overall improvement can coexist with uneven segment performance. For each predefined slice, report eligible count and errors/eligible count. Retain that conditioning population. Samples may not represent their intended population, so sample slice differences alone do not establish population-level disparity. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Use np.mean(numeric_values) for selected observations’ mean. np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root; use ddof=1 only when the calculation requires N−1. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.slice_summary cols=['slice', 'eligible_count', 'error_count', 'error_probability', 'loss_mean', 'loss_std', 'ddof'] ] caption: Computed conditional slice summaries
[TABLE ds.aggregate_slice_evidence cols=['system', 'cohort_id', 'eligible_count', 'error_count', 'error_probability'] ] caption: Aggregate evidence from the matched slice cohort

### s07 · explainer · Inspect zone evidence
(example) Read each zone’s eligible count, errors and conditional error probability together. The loss summaries retain their own selected observations and standard-deviation divisor. Compare slice evidence with the matched overall record without letting one replace the other. Unequal observed sample results support a bounded description of these slices, not an unmeasured population conclusion. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb4⟧

### s08 · explainer · Uneven does not prove population disparity
(misconception) Aggregate improvement can coexist with uneven slices. An observed sample difference alone does not prove disparity throughout the intended population. ⟦B.f1 B.f3 B:tb5⟧

### s09 · video · Inspect evaluate important data slices for subgroup performance gaps
[VIDEO Overall improvement and uneven slice performance] bridge-before: Watch how similar regional flag rates conceal different language-specific fraud detection rates. These are distinct measurements in a synthetic example; overall improvement does not guarantee consistent performance across slices. | bridge-after: The clip demonstrates uneven slice performance, but does not provide eligible counts, explain population representativeness, or teach NumPy mean and standard deviation. The text supplies those reporting requirements, limitations, and calculations.
  - SrX4J8lKZfg 32-101s facts=['f1'] label: How overall improvement hides language-slice gaps | summary: In this synthetic example, underlying fraud is equally common across languages. An English-centric description-quality score is lower for Hindi and Hinglish descriptions, and adding it improves overall fraud detection. The highest-scoring 10% of cases are flagged. Regional flag rates look nearly identical because languages are distributed evenly across regions. Language-specific detection tells a different story: the model detects 33.5% of fraud overall, but only about one-fifth of English-language fraud, over 40% of Hindi-language fraud, and more than half of Hinglish-language fraud. Overall improvement therefore coexists with uneven slice performance, including missed English-language fraud and burdens on innocent Hindi- and Hinglish-speaking customers.

### s10 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.
QUESTION [choice, core, grading=client] Zone B has a higher eligible error proportion than zone A in the supplied validation sample. Which report is justified?
  ✔ o1: Retain both denominators and describe the observed sample gap without asserting a population disparity.
      why: Slice proportions must retain their sample sizes and scope.
  ✘ o2: Declare all intended populations unfairly treated from the proportions alone.
      why: Representation beyond the supplied sample is not established.
  ✘ o3: Compare raw error counts and discard the eligible denominators.
      why: Raw counts without denominators do not compare conditional error proportions.
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r03
  MEASURES: B:distinguish_observed_slice_gaps_from_population_disparity(f2,f3)   anchors=['assessment:distinguish_observed_slice_gaps_from_population_disparity']
  taught-before-tested: B.f2←s06; B.f3←s06

### s11 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.
QUESTION [code_exercise, core, grading=client] Complete the eligible-zone mask expression in supplied_eligible_zone_mask and the guarded loss-mean and population-loss-standard-deviation call expressions in each slice record. Preserve empty-slice handling, structured comparisons, limitation and result schema.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy', 'pandas']} constraints.allowed=['import numpy as np', 'def', 'function parameters and calls', 'return', 'variable assignment', 'numeric and string literals', 'lists and dictionaries', 'for loops', 'if statements', 'len', 'array indexing', 'Boolean masks and comparisons', 'arithmetic operators', 'np.asarray', 'np.sum', 'np.mean(numeric_values)', 'np.std(numeric_values, ddof=0)', 'np.std(numeric_values, ddof=1)'] blocked=9 items
  file main.py [editable]:
# Supplied input loading and dependencies.
import pandas as pd

observations = pd.read_csv('slice_observations.csv')

zones = observations['zone'].to_numpy()

eligible = observations['eligible'].to_numpy()

errors = observations['error'].to_numpy()

losses = observations['loss'].to_numpy()

declared_slices = ['A', 'B']

import numpy as np

# Supplied evaluation scaffold. Complete the marked expressions; preserve the rest.
if __name__:
    def supplied_eligible_zone_mask(zones, zone, eligible):
        return None  # TODO: eligible-zone mask
    def evaluate(zones, eligible, errors, losses, declared_slices):
        records = []
        comparison = []
        for zone in declared_slices:
            mask = slice_mask(zones, zone, eligible)
            n = conditional_count(mask)
            error_count = conditional_count(errors[mask])
            record = {'slice': zone, 'eligible_count': n, 'error_count': error_count, 'error_proportion': None, 'loss_mean': None, 'loss_std': None}
            if n > 0:
                record = {'slice': zone, 'eligible_count': n, 'error_count': error_count, 'error_proportion': error_count / n, 'loss_mean': None, 'loss_std': None}
            records.append(record)
            if n > 0:
                comparison.append({'slice': zone, 'error_count': error_count, 'eligible_count': n, 'error_proportion': error_count / n})
        return {'records': records, 'comparison': comparison, 'limitation': 'These are observed eligible validation slices; representation beyond this sample is unresolved, so no population disparity is established.'}

# Supplied callable operations; keep these assignments unchanged.
supplied_np_sum = np.sum
supplied_np_mean = np.mean
supplied_np_std = np.std
conditional_count = supplied_np_sum

# Complete the marked bindings and expression holes; preserve the remaining scaffold.
slice_mask = supplied_eligible_zone_mask
loss_mean_fn = supplied_np_mean
loss_std_fn = supplied_np_std

  SOLUTION main.py:
# Supplied input loading and dependencies.
import pandas as pd

observations = pd.read_csv('slice_observations.csv')

zones = observations['zone'].to_numpy()

eligible = observations['eligible'].to_numpy()

errors = observations['error'].to_numpy()

losses = observations['loss'].to_numpy()

declared_slices = ['A', 'B']

import numpy as np

# Supplied evaluation scaffold. Retain unchanged; complete only the top-level bindings below.
if __name__:
    def supplied_eligible_zone_mask(zones, zone, eligible):
        return (zones == zone) & (eligible == True)
    def evaluate(zones, eligible, errors, losses, declared_slices):
        records = []
        comparison = []
        for zone in declared_slices:
            mask = slice_mask(zones, zone, eligible)
            n = conditional_count(mask)
            error_count = conditional_count(errors[mask])
            record = {'slice': zone, 'eligible_count': n, 'error_count': error_count, 'error_proportion': None, 'loss_mean': None, 'loss_std': None}
            if n > 0:
                record = {'slice': zone, 'eligible_count': n, 'error_count': error_count, 'error_proportion': error_count / n, 'loss_mean': loss_mean_fn(losses[mask]), 'loss_std': loss_std_fn(losses[mask], ddof=0)}
            records.append(record)
            if n > 0:
                comparison.append({'slice': zone, 'error_count': error_count, 'eligible_count': n, 'error_proportion': error_count / n})
        return {'records': records, 'comparison': comparison, 'limitation': 'These are observed eligible validation slices; representation beyond this sample is unresolved, so no population disparity is established.'}

# Supplied callable operations; keep these assignments unchanged.
supplied_np_sum = np.sum
supplied_np_mean = np.mean
supplied_np_std = np.std
conditional_count = supplied_np_sum

# Complete only these callable/value bindings; preserve the supplied scaffold.
slice_mask = supplied_eligible_zone_mask
loss_mean_fn = supplied_np_mean
loss_std_fn = supplied_np_std

  test t1 (value_equals, visible=True): {"expr":"evaluate(zones, eligible, errors, losses, declared_slices)","expected":{"records":[{"slice":"A","eligible_count":40,"error_count":2,"error_proportion":0.05,"loss_mean":0.05,"loss_std":0.21794494717703364},{"slice":"B","eligible_count":20,"error_count":6,"error_proportion":0.3,"loss_mean":0.3,"loss_std":0.45825756949558394}],"comparison":[{"slice":"A","error_count":2,"eligible_count":40,"error_proportion":0.05},{"slice":"B","error_count":6,"eligible_count":20,"error_proportion":0.3}],"li | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  test t2 (value_equals, visible=False): {"expr":"(evaluate(zones, eligible, errors, losses, declared_slices), evaluate(zones, eligible, errors, losses, ['unobserved']))","expected":[{"records":[{"slice":"A","eligible_count":40,"error_count":2,"error_proportion":0.05,"loss_mean":0.05,"loss_std":0.21794494717703364},{"slice":"B","eligible_count":20,"error_count":6,"error_proportion":0.3,"loss_mean":0.3,"loss_std":0.45825756949558394}],"comparison":[{"slice":"A","error_count":2,"eligible_count":40,"error_proportion":0.05},{"slice":"B","e | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"85f5f4665dd990b14be20742c36db4699ef94c0764c16edfe1c5f453a88c9b98","tests_passed":2}
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Complete only the indicated expressions using the supplied inputs.', 'Keep guards, structured evidence and result fields unchanged.']  remediation→r04
  MEASURES: B:identify_slice_gaps_with_eligible_counts_and_conditional_error_rates(f1,f2); B:distinguish_observed_slice_gaps_from_population_disparity(f2,f3); B:calculate_slice_means_and_standard_deviations_with_the_required_divisor(f4,f5)   anchors=['practice', 'assessment:identify_slice_gaps_with_eligible_counts_and_conditional_error_rates', 'assessment:distinguish_observed_slice_gaps_from_population_disparity', 'assessment:calculate_slice_means_and_standard_deviations_with_the_required_divisor']
  taught-before-tested: B.f1←s06; B.f2←s06; B.f2←s06; B.f3←s06; B.f4←s06; B.f5←s06

### s12 · explainer · Keep actual-class groups separate
(intro) Before accepting a supplied mitigation, inspect group representation and both subgroup and overall validation evidence. Do not assume the model alone explains the problem. ⟦C:tb1⟧
(mechanism) Check whether data represents intended groups before attributing a subgroup problem solely to the model. Evaluate the supplied mitigation on the affected validation segment and overall cohort. A subgroup’s contribution to total expected harm is its deployment population probability × subgroup-conditional expected harm, using supplied error costs. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. An empty conditioning group leaves its rate undefined. ⟦C.f4 C:tb3⟧
[SPREADSHEET_GRID — unrendered type, raw] {"type":"spreadsheet_grid","asset_ref":{"asset_id":"ds.mitigation_records","columns":["system","scope","cohort_id","TP","FP","FN","TN","actual_positive_count","actual_negative_count","cohort_count","precision","recall","validation_prevalence","FPR","FNR","expected_error_cost","deployment_subgroup_probability","population_weighted_harm_contribution","representation_limitation","deployment_negative_probability","deployment_positive_probability","cost_FP","cost_FN","validation_subgroup_prevalence"]},"range":"A1:X5","show_formula_bar":true,"lineage":{"concept_ids":["mle.subgroup_risk_mitigation"],"teaching_block_ids":[],"fact_ids":[],"anchors":["mle.subgroup_risk_mitigation#visual"]}}
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract

### s13 · explainer · Inspect segment and overall evidence
(example) Keep subgroup-conditional harm distinct from its population-weighted contribution. The registered records show reference and mitigation evidence for both affected segment and overall cohort. Apply the supplied deployment subgroup probability, not the validation subgroup prevalence, to weight conditional harm. Inspect representation and the overall result before acceptance; a subgroup improvement alone is insufficient. ⟦C.f1 C.f2 C.f3 C.f4 C:tb4⟧

### s14 · explainer · Subgroup-only is insufficient
(misconception) A subgroup-only improvement is insufficient. Population probability, conditional harm and representation are distinct; empty conditioning groups do not supply defined rates. ⟦C.f1 C.f2 C.f4 C:tb5⟧

### s15 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.
QUESTION [choice, core, grading=client] A supplied mitigation improves overall validation error cost. What further check is required before accepting it for a documented subgroup risk?
  ✔ o1: Check the matched affected segment as well as the overall cohort, and inspect representation limitations.
      why: Affected-segment and overall evidence are both required; representation remains a limitation.
  ✘ o2: Overall improvement proves the affected segment is safe.
      why: Aggregate improvement does not establish suitability for every segment.
  ✘ o3: Replace supplied deployment subgroup probability with its validation prevalence.
      why: Validation subgroup prevalence and deployment population probability are distinct inputs.
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r05
  MEASURES: C:choose_mitigation_for_documented_subgroup_risk(f1,f2)   anchors=['assessment:choose_mitigation_for_documented_subgroup_risk']
  taught-before-tested: C.f1←s12; C.f2←s12

### s16 · hands_on · Calculate from the supplied evidence
 — Use the supplied dataset and fixed contract. Keep the conditioning population explicit when entering the requested formula.
QUESTION [formula_entry, stretch, grading=client] Row template
In AZ1 return one formula-based risk-check record for all four supplied rows in order. Each row: <system>/<scope>: neg=<FP+TN>,pos=<FN+TP>,FPR=<two decimals or undefined>,FNR=<two decimals or undefined>,harm=<two decimals or undefined>. Harm uses each row's actual-class proportions and supplied error costs, with zero correct-prediction cost. 

Affected-subgroup additions
For affected_subgroup rows also append ,validation_prevalence=<subgroup count / corresponding overall count>,deployment_probability=<supplied probability>,contribution=<harm times supplied deployment probability> (two decimals). End each row with "; ". 

Matched-scope selection check
Before viewing comparisons, use the check: defined rates and lower harm on both matched scopes. Append selected=mitigation only if both systems have matched scope/cohort records, all required rates are defined, and mitigation harm is lower in both affected_subgroup and overall; otherwise append selected=none. 

Exact suffix
precommitted check: defined conditioned rates and lower harm in matched affected segment AND overall cohort; deployment probability is not validation prevalence; representation beyond supplied sample is not established. The supplied mitigation addresses the documented affected-segment risk; retain sample representation limits, not a population guarantee.
  [unrendered interaction type formula_entry] public={"prompt":"Row template\nIn AZ1 return one formula-based risk-check record for all four supplied rows in order. Each row: <system>/<scope>: neg=<FP+TN>,pos=<FN+TP>,FPR=<two decimals or undefined>,FNR=<two decimals or undefined>,harm=<two decimals or undefined>. Harm uses each row's actual-class proportions and supplied error costs, with zero correct-prediction cost. \n\nAffected-subgroup additions\nFor affected_subgroup rows also append ,validation_prevalence=<subgroup count / corresponding overall count>,deployment_probability=<supplied probability>,contribution=<harm times supplied deployment probability> (two decimals). End each row with \"; \". \n\nMatched-scope selection check\nBefore viewing comparisons, use the check: defined rates and lower harm on both matched scopes. Append selected=mitigation only if both systems have matched scope/cohort records, all required rates are define grading={"reference_formula":"=A2&\"/\"&B2&\": neg=\"&(E2+G2)&\",pos=\"&(F2+D2)&\",FPR=\"&IF((E2+G2)>0,TEXT(E2/(E2+G2),\"0.00\"),\"undefined\")&\",FNR=\"&IF((F2+D2)>0,TEXT(F2/(F2+D2),\"0.00\"),\"undefined\")&\",harm=\"&IF(AND((E2+G2)>0,(F2+D2)>0),TEXT(((E2+G2)/(E2+G2+F2+D2)*E2/(E2+G2)*V2+(F2+D2)/(E2+G2+F2+D2)*F2/(F2+D2)*W2),\"0.00\"),\"undefined\")&\",validation_prevalence=\"&TEXT(J2/J3,\"0.00\")&\",deployment_probability=\"&TEXT(Q2,\"0.00\")&\",contribution=\"&IF(AND((E2+G2)>0,(F2+D2)>0),TEXT(((E2+G2)/(E2+G2+F2+D2)*E2/(E2+G2)*V2+(F2+D2)/(E2+G2+F2+D2)*F2/(F2+D2)*W2)*Q2,\"0.00\"),\"undefined\")&\"; \"&A3&\"/\"&B3&\": neg=\"&(E3+G3)&\",pos=\"&(F3+D3)&\",FPR=\"&IF((E3+G3)>0,TEXT(E3/(E3+G3),\"0.00\"),\"undefined\")&\",FNR=\"&IF((F3+D3)>0,TEXT(F3/(F3+D3),\"0.00\"),\"undefined\")&\",harm=\"&IF(AND((E3+G3)>0,(F3+D3)>0),TEXT(((E3+G3)/(E3+G3+F3+D3)*E3/(E3+G3)*V3+(F3+D3)/(E3+G3+F3+D3)*F3/(F3+D3)*W3),\"0.0
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r06
  MEASURES: C:choose_mitigation_for_documented_subgroup_risk(f1,f2); C:justify_mitigation_with_population_weighted_error_harm(f3,f4)   anchors=['practice', 'assessment:choose_mitigation_for_documented_subgroup_risk', 'assessment:justify_mitigation_with_population_weighted_error_harm']
  taught-before-tested: C.f1←s12; C.f2←s12; C.f3←s12; C.f4←s12

### s17 · recap · Keep these distinctions
(takeaway) Retain eligible denominators in failure groups and predefined slices. Compare with same-cohort references; sample differences alone do not establish population disparity. Check representation, subgroup and overall evidence before accepting a mitigation. Distinguish conditional harm from population-weighted contribution. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 B.f1 B.f2 B.f3 B.f4 B.f5 C.f1 C.f2 C.f3 C.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5⟧
[UP NEXT] Up next: Keep resolved experiment settings, validation metrics and artifacts in a keyed run.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: the check — locate observed failures
(misconception) Contrast error count with conditional error proportion. The predefined eligible population supplies the denominator; an overall score does not locate every failure. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
(mechanism) Inspect prediction failures; developer usage does not necessarily represent users. For the predefined group, divide errors by eligible observations. Compare its quality evidence with the same-cohort reference to localize observed failure; an overall score does not describe every segment. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Summarize selected numeric observations with np.mean(numeric_values). Use np.std(numeric_values, ddof=0): squared deviations are divided by N before the square root. Use ddof=1 only when the specified calculation requires N−1. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.slice_observations cols=['observation_id', 'cohort_id', 'zone', 'eligible', 'long_distance', 'error', 'loss', 'reference_error', 'reference_loss', 'distance'] ] caption: Predefined zones and long-distance observations
### r02 · Revisit: the practice — locate observed failures
(misconception) Contrast error count with conditional error proportion. The predefined eligible population supplies the denominator; an overall score does not locate every failure. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
(mechanism) Inspect prediction failures; developer usage does not necessarily represent users. For the predefined group, divide errors by eligible observations. Compare its quality evidence with the same-cohort reference to localize observed failure; an overall score does not describe every segment. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Summarize selected numeric observations with np.mean(numeric_values). Use np.std(numeric_values, ddof=0): squared deviations are divided by N before the square root. Use ddof=1 only when the specified calculation requires N−1. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.slice_observations cols=['observation_id', 'cohort_id', 'zone', 'eligible', 'long_distance', 'error', 'loss', 'reference_error', 'reference_loss', 'distance'] ] caption: Predefined zones and long-distance observations
### r03 · Revisit: the check — separate the slices
(misconception) Contrast observed slice evidence with a population claim. Counts and sample conditioning support the former, not automatic generalization to the latter. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3⟧
(mechanism) Overall improvement can coexist with uneven segment performance. For each predefined slice, report eligible count and errors/eligible count. Retain that conditioning population. Samples may not represent their intended population, so sample slice differences alone do not establish population-level disparity. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Use np.mean(numeric_values) for selected observations’ mean. np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root; use ddof=1 only when the calculation requires N−1. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.slice_summary cols=['slice', 'eligible_count', 'error_count', 'error_probability', 'loss_mean', 'loss_std', 'ddof'] ] caption: Computed conditional slice summaries
### r04 · Revisit: the practice — separate the slices
(misconception) Contrast observed slice evidence with a population claim. Counts and sample conditioning support the former, not automatic generalization to the latter. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B:tb2 B:tb3⟧
(mechanism) Overall improvement can coexist with uneven segment performance. For each predefined slice, report eligible count and errors/eligible count. Retain that conditioning population. Samples may not represent their intended population, so sample slice differences alone do not establish population-level disparity. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Use np.mean(numeric_values) for selected observations’ mean. np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root; use ddof=1 only when the calculation requires N−1. ⟦B.f4 B.f5 B:tb3⟧
[TABLE ds.slice_summary cols=['slice', 'eligible_count', 'error_count', 'error_probability', 'loss_mean', 'loss_std', 'ddof'] ] caption: Computed conditional slice summaries
### r05 · Revisit: the check — check representation first
(misconception) Contrast subgroup-conditional harm with population-weighted contribution. Weight by supplied deployment probability, then inspect representation and overall evidence too. ⟦C.f1 C.f2 C.f3 C.f4 C:tb2 C:tb3⟧
(mechanism) Check whether data represents intended groups before attributing a subgroup problem solely to the model. Evaluate the supplied mitigation on the affected validation segment and overall cohort. A subgroup’s contribution to total expected harm is its deployment population probability × subgroup-conditional expected harm, using supplied error costs. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. An empty conditioning group leaves its rate undefined. ⟦C.f4 C:tb3⟧
[TABLE ds.mitigation_records cols=['system', 'scope', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'deployment_subgroup_probability', 'population_weighted_harm_contribution', 'representation_limitation', 'deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'validation_subgroup_prevalence'] ] caption: Matched reference and supplied mitigation harm
### r06 · Revisit: the practice — check representation first
(misconception) Contrast subgroup-conditional harm with population-weighted contribution. Weight by supplied deployment probability, then inspect representation and overall evidence too. ⟦C.f1 C.f2 C.f3 C.f4 C:tb2 C:tb3⟧
(mechanism) Check whether data represents intended groups before attributing a subgroup problem solely to the model. Evaluate the supplied mitigation on the affected validation segment and overall cohort. A subgroup’s contribution to total expected harm is its deployment population probability × subgroup-conditional expected harm, using supplied error costs. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. An empty conditioning group leaves its rate undefined. ⟦C.f4 C:tb3⟧
[TABLE ds.mitigation_records cols=['system', 'scope', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'deployment_subgroup_probability', 'population_weighted_harm_contribution', 'representation_limitation', 'deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'validation_subgroup_prevalence'] ] caption: Matched reference and supplied mitigation harm

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: mlflow.start_run(...)
· constraints.blocked_syntax: mlflow.log_metric(...)
· constraints.blocked_syntax: RandomizedSearchCV(...)
· spec.expr: {k: v for k, v in (evaluate(eligible, long_distance, errors, losses, reference_errors, reference_losses)).items() if k != "finding"}
· spec.expr: ({k: v for k, v in (evaluate(eligible, long_distance, errors, losses, reference_errors, reference_losses)).items() if k != "finding"}, (lambda r: all(r['finding'][side][key] == r[prefix + key] for side, prefix in [('model',''),('reference','reference_')] for key in ['error_count','eligible_count','loss_mean','loss_std']) and bool(r['finding']['limitation']) and isinstance(r['finding'].get('description'), str) and bool(r['finding']['description'].strip()))(evaluate(eligible, long_distance, errors, losses, reference_errors, reference_losses)))
· grading.reference_formula: =A2&"/"&B2&": neg="&(E2+G2)&",pos="&(F2+D2)&",FPR="&IF((E2+G2)>0,TEXT(E2/(E2+G2),"0.00"),"undefined")&",FNR="&IF((F2+D2)>0,TEXT(F2/(F2+D2),"0.00"),"undefined")&",harm="&IF(AND((E2+G2)>0,(F2+D2)>0),TEXT(((E2+G2)/(E2+G2+F2+D2)*E2/(E2+G2)*V2+(F2+D2)/(E2+G2+F2+D2)*F2/(F2+D2)*W2),"0.00"),"undefined")&",validation_prevalence="&TEXT(J2/J3,"0.00")&",deployment_probability="&TEXT(Q2,"0.00")&",contribution="&IF(AND((E2+G2)>0,(F2+D2)>0),TEXT(((E2+G2)/(E2+G2+F2+D2)*E2/(E2+G2)*V2+(F2+D2)/(E2+G2+F2+D2)*F2/(F2+D2)*W2)*Q2,"0.00"),"undefined")&"; "&A3&"/"&B3&": neg="&(E3+G3)&",pos="&(F3+D3)&",FPR="&IF((E3+G3)>0,TEXT(E3/(E3+G3),"0.00"),"undefined")&",FNR="&IF((F3+D3)>0,TEXT(F3/(F3+D3),"0.00"),"undefined")&",harm="&IF(AND((E3+G3)>0,(F3+D3)>0),TEXT(((E3+G3)/(E3+G3+F3+D3)*E3/(E3+G3)*V3+(F3+D3)/(E3+G3+F3+D3)*F3/(F3+D3)*W3),"0.00"),"undefined")&"; "&A4&"/"&B4&": neg="&(E4+G4)&",pos="&(F4+D4)&",FPR="&IF((E4+G4)>0,TEXT(E4/(E4+G4),"0.00"),"undefined")&",FNR="&IF((F4+D4)>0,TEXT(F4/(F4+D4),"0.00"),"undefined")&",harm="&IF(AND((E4+G4)>0,(F4+D4)>0),TEXT(((E4+G4)/(E4+G4+F4+D4)*E4/(E4+G4)*V4+(F4+D4)/(E4+G4+F4+D4)*F4/(F4+D4)*W4),"0.00"),"undefined")&",validation_prevalence="&TEXT(J4/J5,"0.00")&",deployment_probability="&TEXT(Q4,"0.00")&",contribution="&IF(AND((E4+G4)>0,(F4+D4)>0),TEXT(((E4+G4)/(E4+G4+F4+D4)*E4/(E4+G4)*V4+(F4+D4)/(E4+G4+F4+D4)*F4/(F4+D4)*W4)*Q4,"0.00"),"undefined")&"; "&A5&"/"&B5&": neg="&(E5+G5)&",pos="&(F5+D5)&",FPR="&IF((E5+G5)>0,TEXT(E5/(E5+G5),"0.00"),"undefined")&",FNR="&IF((F5+D5)>0,TEXT(F5/(F5+D5),"0.00"),"undefined")&",harm="&IF(AND((E5+G5)>0,(F5+D5)>0),TEXT(((E5+G5)/(E5+G5+F5+D5)*E5/(E5+G5)*V5+(F5+D5)/(E5+G5+F5+D5)*F5/(F5+D5)*W5),"0.00"),"undefined")&"; "&"selected="&IF(AND(AND((E2+G2)>0,(F2+D2)>0,(E3+G3)>0,(F3+D3)>0,(E4+G4)>0,(F4+D4)>0,(E5+G5)>0,(F5+D5)>0),AND(A2="reference",A3="reference",A4="mitigation",A5="mitigation",B2="affected_subgroup",B4=B2,B3="overall",B5=B3,C2=C4,C3=C5,C2=C3)),IF(AND(((E4+G4)/(E4+G4+F4+D4)*E4/(E4+G4)*V4+(F4+D4)/(E4+G4+F4+D4)*F4/(F4+D4)*W4)<((E2+G2)/(E2+G2+F2+D2)*E2/(E2+G2)*V2+(F2+D2)/(E2+G2+F2+D2)*F2/(F2+D2)*W2),((E5+G5)/(E5+G5+F5+D5)*E5/(E5+G5)*V5+(F5+D5)/(E5+G5+F5+D5)*F5/(F5+D5)*W5)<((E3+G3)/(E3+G3+F3+D3)*E3/(E3+G3)*V3+(F3+D3)/(E3+G3+F3+D3)*F3/(F3+D3)*W3)),"mitigation","none"),"none")&"; precommitted check: defined conditioned rates and lower harm in matched affected segment AND overall cohort; deployment probability is not validation prevalence; representation beyond supplied sample is not established. The supplied mitigation addresses the documented affected-segment risk; retain sample representation limits, not a population guarantee."
· grading.expected_value: reference/affected_subgroup: neg=20,pos=5,FPR=0.75,FNR=0.20,harm=0.80,validation_prevalence=0.13,deployment_probability=0.25,contribution=0.20; reference/overall: neg=160,pos=40,FPR=0.15,FNR=0.20,harm=0.32; mitigation/affected_subgroup: neg=20,pos=5,FPR=0.50,FNR=0.20,harm=0.60,validation_prevalence=0.13,deployment_probability=0.25,contribution=0.15; mitigation/overall: neg=160,pos=40,FPR=0.10,FNR=0.20,harm=0.28; selected=mitigation; precommitted check: defined conditioned rates and lower harm in matched affected segment AND overall cohort; deployment probability is not validation prevalence; representation beyond supplied sample is not established. The supplied mitigation addresses the documented affected-segment risk; retain sample representation limits, not a population guarantee.

=========

# EVALUATOR PACKET — Track, repeat and bound experiments (mle.tile.029_032)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.experiment_metric_logging — Record an MLflow experiment run with parameters, validation metrics and diagnostic artifacts
B = mle.training_randomness — Control random seeds for reproducible training comparisons
C = mle.validation_regularization — Select regularization in response to validation-observed overfitting
D = mle.bounded_hyperparameter_search — Run bounded hyperparameter search using validation evidence without accessing the protected test set

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=11
  warn: mle.tile.029_032.s01: prose block without lineage.fact_ids
  warn: mle.tile.029_032.s06: prose block without lineage.fact_ids
  warn: mle.tile.029_032.s10/ix.mle.tile.029_032.s10: ADVISORY — syntax descriptors with no detector: ['DataLoader', 'GridSearchCV', 'None', 'RandomizedSearchCV', 'calls to supplied preparation and evaluation helpers', 'def with parameters and return', 'dictionary and list indexing', 'fit and predict', 'for seed in declared_seed_list', 'from supplied dependency modules import required names', "if __name__ == '__main__':", 'if statements', 'integer and floating-point literals', 'len', 'lists and dictionaries', 'numeric comparisons and arithmetic', 'scikit-learn split and estimator calls with random_state', 'torch imports and API calls']
  warn: mle.tile.029_032.s11: prose block without lineage.fact_ids
  warn: mle.tile.029_032.s17/ix.mle.tile.029_032.s17: ADVISORY — syntax descriptors with no detector: ['GridSearchCV', 'NumPy array operations and Boolean masks', 'RandomizedSearchCV', 'arithmetic and comparison operators', 'def with parameters and return', 'for loops over supplied settings', 'if and else branches', 'import and from ... import for required dependencies', 'lists, tuples, and dictionaries', 'local assignments and numeric literals', 'training-fitted preprocessing pipeline fit and predict']
  warn: mle.tile.029_032.s18: prose block without lineage.fact_ids
  warn: mle.tile.029_032.s23/ix.mle.tile.029_032.s23: ADVISORY — syntax descriptors with no detector: ['None for undefined rates', 'arithmetic and comparison operators', 'calls to the supplied trial execution interface', 'def with a default budget parameter', 'dictionary literals and key access', 'for loops over the bounded configuration list', 'from torch import ...', 'function calls with explicit keyword arguments', 'if __name__ == "__main__":', 'if and else conditionals', 'import statements for required supplied library or client dependencies', 'len', 'list literals, indexing, slicing, and append', 'numeric literals', 'return statements']
  warn: plan: mle.tile.029_032.s04 was planned to measure mle.experiment_metric_logging#assessment:verify_run_artifact_path_and_code_identity but its interaction does not
  warn: plan: mle.tile.029_032.s09 was planned to measure mle.training_randomness#assessment:summarize_repeated_results_with_mean_and_specified_standard_deviation but its interaction does not
  warn: plan: mle.tile.029_032.s10 was planned to measure mle.training_randomness#assessment:distinguish_random_state_consumption but its interaction does not
  warn: plan: mle.tile.029_032.s23 was planned to measure mle.bounded_hyperparameter_search#assessment:interpret_validation_selected_search_results but its interaction does not

## SOURCE FACTS — A (mle.experiment_metric_logging)   objective: Create and verify a keyed run record linking parameters, metrics, artifacts and actual code revision.
A.f1: Use import mlflow and with mlflow.start_run() as run to create a run whose run_id identifies its tracking record.   [sources: mlflow_docs#ml/tracking/tracking-api/ — Starting and Managing Runs; Logging Data to Runs; Querying Runs Programmatically]
A.f2: Log the resolved configuration with mlflow.log_params(params), validation results with mlflow.log_metric(name, value), and a diagnostic file with mlflow.log_artifact(local_path).   [sources: mlflow_docs#ml/tracking/tracking-api/ — Starting and Managing Runs; Logging Data to Runs; Querying Runs Programmatically]
A.f3: Inspect the actual repository revision with git rev-parse --verify HEAD before recording the run’s code identity.   [sources: git_docs#git-rev-parse — --verify; git-show — DESCRIPTION]
A.f4: Retrieve the keyed run with recorded = mlflow.get_run(run_id), then read recorded.data.params, recorded.data.metrics and recorded.info.artifact_uri; for a metric logged repeatedly, this RunData exposes the most recently logged value at the largest step, not its entire history.   [sources: mlflow_docs#https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html — mlflow.get_run, mlflow_docs#https://mlflow.org/docs/latest/api_reference/python_api/mlflow.entities.html — Run.data; Run.info; RunData.params; RunData.metrics; RunInfo.artifact_uri]
A.f5: Define the logging function with default parameter values and accept explicit keyword overrides, then log the resolved values rather than only the defaults.   [sources: python_tutorial#controlflow.html — Defining Functions; Default Argument Values; Keyword Arguments]
A.f6: Use os.getcwd() to inspect the current working directory and os.chdir(recorded_directory) when resolving local artifact/repository paths, retaining the resolved path in the run lookup.   [sources: python_tutorial#stdlib.html — Operating System Interface; Command Line Arguments]
A.f7: Use subprocess.run with the intended working directory and captured output to inspect git rev-parse --verify HEAD and reject a revision mismatch before claiming the keyed artifact belongs to that run.   [sources: python_tutorial#../library/subprocess.html — Using the subprocess Module]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Track and Tune Reproducibly.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function with learner-written imports, a default trial setting of 10 and an explicit keyword override of 20. Inspect the working directory and repository revision, then record one MLflow run containing the resolved parameter dictionary, a supplied validation metric and an existing diagnostic file. Retain the run ID, repository directory, resolved local artifact path and code revision; retrieve the same run and reject a revision mismatch before accepting its artifact association.  SUCCESS: The retrieved run contains the resolved trial setting of 20, the supplied validation result and an artifact URI for the logged diagnostic file. The retained lookup identifies the same run, repository directory, local artifact path and actual code revision. A revision-mismatch check rejects an incorrect revision rather than accepting the association.
ASSESSMENT ANCHOR: retrieve_run_by_run_id facts=['f1', 'f4']
ASSESSMENT ANCHOR: retrieve_resolved_parameters_and_validation_metrics facts=['f2', 'f4', 'f5']
ASSESSMENT ANCHOR: interpret_repeated_metric_run_data facts=['f4']
ASSESSMENT ANCHOR: verify_run_artifact_path_and_code_identity facts=['f2', 'f3', 'f6', 'f7']

## SOURCE FACTS — B (mle.training_randomness)   objective: Assess paired-run variability with numeric summaries and an empirical candidate-win proportion.
B.f1: Integer random_state values reset supported scikit-learn random generators for repeatable calls, while None or a shared RandomState instance has different state-consumption behavior.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.3 Controlling randomness]
B.f2: Control the estimator and split random sources for a comparison, but distinguish that control from a guarantee that every computation or environment is deterministic.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.3 Controlling randomness]
B.f3: Use a for loop over the declared seed list to execute the repeated comparison and collect each matched pair of validation results.   [sources: python_tutorial#controlflow.html — Defining Functions; Default Argument Values; Keyword Arguments]
B.f4: Estimate the candidate’s empirical win probability as winning paired trials divided by all completed paired trials, retaining the number of trials.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
B.f5: Compute the arithmetic mean with np.mean(numeric_values) over the selected numeric observations.   [sources: numpy_user_guide#reference/generated/numpy.mean.html — Parameters; Notes]
B.f6: Compute standard deviation with np.std(numeric_values, ddof=0), which divides squared deviations by N before taking the square root; use ddof=1 only when the stated calculation requires the N−1 divisor.   [sources: numpy_user_guide#reference/generated/numpy.std.html — Parameters; Notes]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Track and Tune Reproducibly.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.sklearn_baseline_workflow, mle.deployment_matched_splits. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write the required imports and a learner-defined Python function that repeats the supplied baseline/candidate validation comparison over the declared seed list. Control both split and estimator random sources under the supplied protocol, retain each completed pair with its seed, and report the completed-pair count, candidate win count, empirical win probability, and mean and standard deviation of the selected numeric results. Explain why controlled randomness does not establish universal deterministic replay.  SUCCESS: Every declared seed is processed, both models in each completed trial use the same validation split, and each completed record retains its seed and baseline/candidate results. The reported win probability equals winning completed pairs divided by all completed pairs under the supplied metric direction and tie rule. The report includes the denominator, np.mean results, np.std results with ddof=0, and a bounded reproducibility statement.
ASSESSMENT ANCHOR: distinguish_random_state_consumption facts=['f1']
ASSESSMENT ANCHOR: control_split_and_estimator_randomness_without_overclaiming_determinism facts=['f2']
ASSESSMENT ANCHOR: collect_paired_seed_trials_and_estimate_empirical_win_probability facts=['f3', 'f4']
ASSESSMENT ANCHOR: summarize_repeated_results_with_mean_and_specified_standard_deviation facts=['f5', 'f6']

## SOURCE FACTS — C (mle.validation_regularization)   objective: Select a regularization setting from matched train/validation gaps and expected-cost evidence.
C.f1: A gap between good training performance and poor validation performance provides evidence of overfitting; compare both under the same scoring interpretation.   [sources: scikit_learn_user_guide#modules/learning_curve.html — 3.5.1 Validation curve; 3.5.2 Learning curve]
C.f2: Evaluate the declared regularization settings using the same validation protocol, then select with the predeclared validation criterion rather than the training score alone.   [sources: scikit_learn_user_guide#modules/learning_curve.html — 3.5.1 Validation curve; 3.5.2 Learning curve]
C.f3: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
C.f4: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
C.f5: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
C.f6: Regularization penalizes model complexity during fitting; for Ridge settings larger alpha increases the penalty, while LogisticRegression uses C as inverse regularization strength.   [sources: scikit_learn_user_guide#modules/linear_model.html — Ridge regression; Logistic regression]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Track and Tune Reproducibly.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection, mle.deployment_matched_splits, mle.sklearn_baseline_workflow, mle.validation_candidate_comparison. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function with learner-written imports that compares the supplied order-model regularization settings within existing infrastructure scaffolding. Keep preprocessing training-fitted and the validation protocol, deployment probabilities, error costs, scoring interpretation, and eligibility limits fixed. Calculate validation FPR, FNR, and expected error cost, compare training and validation performance, and select an eligible setting using the predeclared validation criterion without protected-test access.  SUCCESS: The function returns the declared settings' comparable training and validation results, correctly calculated conditional error rates and expected costs, and the eligible selection required by the validation criterion. Empty conditioning groups are explicitly reported as undefined rather than assigned a fabricated rate. The comparison preserves all fixed assumptions and never accesses protected-test observations.
ASSESSMENT ANCHOR: recognize_overfitting_from_comparable_training_validation_scores facts=['f1']
ASSESSMENT ANCHOR: select_regularization_using_fixed_validation_criterion_without_test_access facts=['f2', 'f5']
ASSESSMENT ANCHOR: calculate_conditional_error_rates_and_identify_undefined_rates facts=['f3']
ASSESSMENT ANCHOR: calculate_deployment_weighted_expected_error_cost facts=['f4']
ASSESSMENT ANCHOR: interpret_estimator_specific_regularization_strength facts=['f6']

## SOURCE FACTS — D (mle.bounded_hyperparameter_search)   objective: Execute a budgeted validation search with resolved defaults and protected-test isolation.
D.f1: GridSearchCV enumerates combinations from param_grid, while RandomizedSearchCV samples a bounded number of configurations selected by n_iter.   [sources: scikit_learn_user_guide#modules/grid_search.html — 3.2.1 Exhaustive Grid Search; 3.2.2 Randomized Parameter Optimization]
D.f2: Specify the scoring and evaluation protocol before running the search, and inspect the validation-selected best_params_ and cv_results_.   [sources: scikit_learn_user_guide#modules/grid_search.html — 3.2.1 Exhaustive Grid Search; 3.2.2 Randomized Parameter Optimization]
D.f3: For a supplied manual search, iterate the bounded configuration dictionaries, execute each declared trial and record its validation result without exceeding the fixed trial budget.   [sources: python_tutorial#controlflow.html — Defining Functions; Default Argument Values; Keyword Arguments]
D.f4: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
D.f5: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
D.f6: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
D.f7: Define the search function with a default budget parameter and accept explicit keyword overrides; resolve the budget before iterating the trial dictionary/list.   [sources: python_tutorial#controlflow.html — Defining Functions; Default Argument Values; Keyword Arguments]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Track and Tune Reproducibly.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.sklearn_baseline_workflow, mle.validation_candidate_comparison, mle.training_randomness, mle.task_metric_selection, mle.deployment_matched_splits, mle.model_acceptance_criteria. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Implement a learner-defined Python search function within the supplied infrastructure scaffolding, including imports for its required library or client dependencies. Accept a default budget and explicit keyword overrides, resolve the budget before iterating the supplied configuration dictionaries, and execute only the permitted trials. Record validation counts, calculate conditional error rates and prevalence-weighted expected error cost, and return the validation-selected configuration under the supplied fixed selection rule without accessing protected test observations.  SUCCESS: The function respects both its default budget and an explicit keyword override. With three supplied configurations and a keyword budget of two, it executes exactly the first two declared trials and retains their actual configurations and validation results. Its rates use the correct conditioning groups, empty groups remain undefined, and its expected costs use the supplied deployment probabilities and error costs. Selection follows the fixed eligibility and selection rules using validation evidence alone.
ASSESSMENT ANCHOR: interpret_validation_selected_search_results facts=['f1', 'f2']
ASSESSMENT ANCHOR: execute_trials_within_resolved_budget facts=['f3', 'f7']
ASSESSMENT ANCHOR: select_configuration_by_validation_expected_error_cost facts=['f4', 'f5']
ASSESSMENT ANCHOR: exclude_protected_test_evidence_from_search facts=['f6']

## DATA ASSETS USED
ds.acceptance_contract: Precommitted predictive contract — columns: deployment_negative_probability(numerical), deployment_positive_probability(numerical), cost_FP(numerical), cost_FN(numerical), correct_prediction_cost(numerical), expected_cost_bound(numerical), selection_rule(categorical), tie_rule(categorical), empty_group_rule(categorical), ddof(numerical), operating_limit(numerical)
   [0.8,0.2,1,5,0,0.3,"minimum expected cost among matched eligible records","first in declared order","undefined rate; ineligible when required",0,null]
ds.execution_contract: Fixed execution and reporting contracts — columns: estimator_random_state(identifier,digits-as-label), default_trial_setting(numerical), override_trial_setting(numerical), default_search_budget(numerical), override_search_budget(numerical), metric_direction(categorical), tie_policy(categorical), split_protocol(categorical), ddof(numerical)
   [0,10,20,3,2,"lower expected cost is better","ties are not paired wins; selection uses declared order","use same split per seed for both models; set split and estimator random_state to the seed",0]
ds.paired_trials: Five completed matched seed trials — columns: seed(identifier,digits-as-label), baseline_result(numerical), candidate_result(numerical)
   [0,0.32,0.31]
   [1,0.33,0.32]
   [2,0.34,0.33]
   [3,0.35,0.36]
   [4,0.36,0.37]
   variant v.incomplete_pair: 1 ops; planted: 
ds.regularization_directions: Estimator-specific penalty directions — columns: estimator(categorical), parameter(categorical), direction(text)
   ["Ridge","alpha","larger alpha increases penalty"]
   ["LogisticRegression","C","larger C decreases regularization strength"]
ds.regularization_records: Fixed-criterion regularization evidence — columns: configuration_id(identifier), estimator(categorical), parameter_name(categorical), parameter_value(numerical), strength_direction(text), cohort_id(identifier), training_TP(numerical), training_FP(numerical), training_FN(numerical), training_TN(numerical), training_expected_error_cost(numerical), TP(numerical), FP(numerical), FN(numerical), TN(numerical), actual_positive_count(numerical), actual_negative_count(numerical), cohort_count(numerical), precision(numerical), recall(numerical), validation_prevalence(numerical), FPR(numerical), FNR(numerical), expected_error_cost(numerical), operating_requirements_met(categorical)
   ["weak_penalty","LogisticRegression","C",10.0,"inverse regularization strength","orders_100",18,0,2,80,0.10000000000000002,16,15,4,65,20,80,100,0.5161290322580645,0.8,0.2,0.1875,0.2,0.3500000000000001,true]
   ["stronger_penalty","LogisticRegression","C",1.0,"inverse regularization strength","orders_100",17,3,3,77,0.18,16,8,4,72,20,80,100,0.6666666666666666,0.8,0.2,0.1,0.2,0.28,true]
   variant v.regularization_empty_positive: 13 ops; planted: 
ds.search_trials: Three declared configuration dictionaries — columns: configuration_id(identifier), declared_order(numerical), configuration_json(text), cohort_id(identifier), TP(numerical), FP(numerical), FN(numerical), TN(numerical), operating_requirements_met(categorical)
   ["config_1",0,"{\"C\": 10.0, \"random_state\": 0}","orders_100",16,15,4,65,true]
   ["config_2",1,"{\"C\": 1.0, \"random_state\": 0}","orders_100",16,8,4,72,true]
   ["config_3",2,"{\"C\": 0.1, \"random_state\": 0}","orders_100",16,0,4,80,true]
   variant v.search_empty_positive: 4 ops; planted: 

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose CPU or GPU capacity for a bounded training workload; Choose a task-compatible training loss; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Control random seeds for reproducible training comparisons; Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point; Define a neural network with task-compatible layers and activations; Diagnose training failures from loss and gradient behavior; Diagnose training memory exhaustion; Document model limitations and foreseeable misuse under an existing risk policy; Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline; Freeze and identify a traceable dataset snapshot for reproducible training; Implement the minibatch forward, backward and optimizer-step loop; Package a versioned model with fitted preprocessing and inference dependencies; Place models and tensor

## LESSON, in learner order

### s01 · explainer · Start and log the run
(intro) A keyed run connects resolved parameters, validation results, code identity and a diagnostic artifact. A printed metric alone does not retain that connection. ⟦A:tb1⟧
(mechanism) Use import mlflow and with mlflow.start_run() as run; retain run_id as the tracking key. Log resolved configuration with mlflow.log_params(params), validation results with mlflow.log_metric(name, value), and the diagnostic file with mlflow.log_artifact(local_path). Inspect git rev-parse --verify HEAD before recording code identity. ⟦A.f1 A.f2 A.f3 A:tb2⟧
[CODE python]
import os
import subprocess
import mlflow

def record_trial(recorded_directory, local_path, expected_revision,
                 metric_name, metric_value, trial_setting=10):
    original_directory = os.getcwd()
    os.chdir(recorded_directory)
    revision = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=recorded_directory, capture_output=True, text=True, check=True
    ).stdout.strip()
    if revision != expected_revision:
        raise ValueError("Repository revision mismatch")
    resolved_path = os.path.abspath(local_path)
    with mlflow.start_run() as run:
        run_id = run.info.run_id
        mlflow.log_params({"trial_setting": trial_setting,
                           "repository_revision": revision,
                           "diagnostic_path": resolved_path})
        mlflow.log_metric(metric_name, metric_value)
        mlflow.log_artifact(resolved_path)
    recorded = mlflow.get_run(run_id)
    os.chdir(original_directory)
    return {"run_id": run_id, "params": recorded.data.params,
            "metrics": recorded.data.metrics,
            "artifact_uri": recorded.info.artifact_uri,
            "resolved_path": resolved_path}
  annotations: []
[TABLE ds.execution_contract cols=['estimator_random_state', 'default_trial_setting', 'override_trial_setting', 'default_search_budget', 'override_search_budget', 'metric_direction', 'tie_policy', 'split_protocol', 'ddof'] ] caption: Fixed execution and reporting contracts

### s02 · explainer · Reject revision mismatch
(mechanism) Retrieve recorded = mlflow.get_run(run_id); inspect recorded.data.params, recorded.data.metrics and recorded.info.artifact_uri. For repeated metric logging, RunData gives the most recently logged value at the largest step, not the full history. Define function defaults, accept keyword overrides, and log resolved values. Use os.getcwd() and os.chdir(recorded_directory) when resolving repository/artifact paths; retain the resolved path in lookup. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(mechanism) Use subprocess.run in the intended working directory with captured output to inspect git rev-parse --verify HEAD. Reject a revision mismatch before claiming the keyed artifact belongs to that run. ⟦A.f7 A:tb4⟧

### s03 · explainer · A name is not a verified key
(example) An explicit keyword override replaces the default value in the resolved configuration to log. Retain the run key and resolved local artifact path, inspect repository identity in the intended directory, then retrieve the keyed run. Compare its parameters, metrics and artifact URI with the intended record. Interpret repeated metrics as the latest value at the largest step, not a history. A revision mismatch or wrongly resolved path prevents the artifact-ownership claim. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb5⟧
(misconception) A run name or printed metric is not a verified keyed record. Retrieved parameters, actual revision, resolved overrides and artifact path must agree. ⟦A.f2 A.f3 A.f5 A.f6 A.f7 A:tb6⟧

### s04 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.
QUESTION [choice, intro, grading=client] A metric was logged repeatedly to an MLflow run. What does recorded.data.metrics expose when you retrieve that keyed run?
  ✔ o1: The most recently logged value at the largest step, not the complete metric history.
      why: RunData exposes the most recent value at the largest step.
  ✘ o2: Every historical metric value in a list.
      why: This field is not the entire metric history.
  ✘ o3: Only the first logged value, regardless of later steps.
      why: The retrieval rule is not the first logged value.
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r01
  MEASURES: A:interpret_repeated_metric_run_data(f4)   anchors=['assessment:interpret_repeated_metric_run_data']
  taught-before-tested: A.f4←s02

### s05 · hands_on · Review the logging excerpts
 — Read the supplied excerpts in this step and decide which correctly preserve the resolved configuration and keyed tracking evidence.
QUESTION [classify, core, grading=client] Read each supplied logging excerpt and judge whether it meets or violates the named requirement shown by its evidence: resolved configuration, repository/path identity, keyed logging/retrieval, or metric-history interpretation. Other parts of the logging workflow are outside each excerpt's judgement.
  'def record(trial_setting=10):
    mlflow.log_params({"trial_setting": trial_setting})
record(trial_setting=20)
retrieved params: trial_setting="20"' -> Meets the shown requirement
      feedback: The recorded parameter retains the resolved keyword override.
  'def record(trial_setting=10):
    mlflow.log_params({"trial_setting": 10})
record(trial_setting=20)
retrieved params: trial_setting="10"' -> Violates the shown requirement
      feedback: Logging the default ignores the explicit resolved override.
  'cwd = os.getcwd()
os.chdir(recorded_directory)
completed = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=recorded_directory, capture_output=True, text=True, check=True)
actual_revision = completed.stdout.strip()
if actual_revision != expected_revision:
    raise ValueError("Repository revision mismatch")
resolved_path = os.path.abspath(local_path)
# retain actual_revision and resolved_path with run_id' -> Meets the shown requirement
      feedback: Captured revision is inspected in the intended repository and mismatches are rejected; the resolved local path is retained.
  'revision = expected_revision
# no repository inspection performed
lookup = {"repository_revision": revision, "diagnostic_path": local_path}' -> Violates the shown requirement
      feedback: Copying an expected revision does not inspect the actual repository, and an unresolved path does not retain the resolved artifact location.
  'with mlflow.start_run() as run:
    run_id = run.info.run_id
    mlflow.log_metric("validation_expected_cost", 0.28)
    mlflow.log_artifact(resolved_path)
recorded = mlflow.get_run(run_id)
lookup = {"run_id": run_id, "params": recorded.data.params, "metrics": recorded.data.metrics, "artifact_uri": recorded.info.artifact_uri, "resolved_path": resolved_path, "repository_revision": actual_revision}' -> Meets the shown requirement
      feedback: A keyed run links the validation metric and diagnostic artifact, and retrieval retains the parameters, metric and artifact URI.
  'recorded = mlflow.get_run(run_id)
report = {"entire_metric_history": recorded.data.metrics}' -> Violates the shown requirement
      feedback: RunData metrics are the most recently logged values at the largest step, not the entire history.
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r02
  MEASURES: A:retrieve_run_by_run_id(f1,f4); A:retrieve_resolved_parameters_and_validation_metrics(f2,f4,f5); A:interpret_repeated_metric_run_data(f4); A:verify_run_artifact_path_and_code_identity(f2,f3,f6,f7)   anchors=['practice', 'assessment:retrieve_run_by_run_id', 'assessment:retrieve_resolved_parameters_and_validation_metrics', 'assessment:interpret_repeated_metric_run_data', 'assessment:verify_run_artifact_path_and_code_identity']
  taught-before-tested: A.f1←s01; A.f4←s02; A.f2←s01; A.f4←s02; A.f5←s02; A.f4←s02; A.f2←s01; A.f3←s01; A.f6←s02; A.f7←s02

### s06 · explainer · Wins, mean and spread
(intro) Control supplied random sources and retain paired trial results. This supports the declared repeated comparison, not universal determinism. ⟦B:tb1⟧
(mechanism) Integer random_state values reset supported scikit-learn generators for repeatable calls; None and shared RandomState instances consume state differently. Control estimator and split randomness without promising every computation or environment is deterministic. Loop over the declared seeds and collect each matched baseline/candidate validation pair. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Empirical win probability is winning paired trials/all completed paired trials; retain the trial count. Summarize selected numeric results with np.mean(numeric_values) and np.std(numeric_values, ddof=0). The latter divides squared deviations by N before the square root; use ddof=1 only if N−1 is required. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[TABLE ds.paired_trials cols=['seed', 'baseline_result', 'candidate_result'] ] caption: Five completed matched seed trials
[TABLE ds.execution_contract cols=['estimator_random_state', 'default_trial_setting', 'override_trial_setting', 'default_search_budget', 'override_search_budget', 'metric_direction', 'tie_policy', 'split_protocol', 'ddof'] ] caption: Fixed execution and reporting contracts
[TABLE computed result ] caption: Completed matched pairs; ties are not wins.
  produced by sql: SELECT seed, baseline_result, candidate_result, candidate_result < baseline_result AS candidate_win FROM pairs ORDER BY seed
  result columns=['seed', 'baseline_result', 'candidate_result', 'candidate_win'] rows(5)=[[0,0.32,0.31,true],[1,0.33,0.32,true],[2,0.34,0.33,true],[3,0.35,0.36,false],[4,0.36,0.37,false]]
[TABLE computed result ] caption: Selected-result means and N-divisor standard deviations.
  produced by sql: SELECT COUNT(*) AS completed_pairs, SUM(CASE WHEN candidate_result < baseline_result THEN 1 ELSE 0 END) AS wins, 1.0*SUM(CASE WHEN candidate_result < baseline_result THEN 1 ELSE 0 END)/COUNT(*) AS empirical_win_probability, AVG(baseline_result) AS baseline_mean, SQRT(AVG(baseline_result*baseline_result)-AVG(baseline_result)*AVG(baseline_result)) AS baseline_std_ddof0, AVG(candidate_result) AS candidate_mean, SQRT(AVG(candidate_result*candidate_result)-AVG(candidate_result)*AVG(candidate_result)) AS candidate_std_ddof0 FROM pairs
  result columns=['completed_pairs', 'wins', 'empirical_win_probability', 'baseline_mean', 'baseline_std_ddof0', 'candidate_mean', 'candidate_std_ddof0'] rows(1)=[[5,3,0.6,0.33999999999999997,0.014142135623731154,0.33799999999999997,0.023151673805580638]]

### s07 · explainer · Retain each completed pair
(example) Keep each seed with its baseline and candidate results, then judge wins using the declared metric direction and tie policy. Separate averages lose pairing, so calculate wins pair by pair and retain the completed-pair denominator. An incomplete trial is not a win. Mean and spread describe the selected results under the specified divisor. Controlling estimator and split sources does not establish determinism in every environment. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B:tb4⟧

### s08 · explainer · Seeds do not promise certainty
(misconception) Controlled seeds do not guarantee universal determinism. Empirical wins describe completed paired trials, not certainty that the candidate always wins. ⟦B.f2 B.f4 B:tb5⟧

### s09 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.
QUESTION [choice, core, grading=client] A paired comparison explicitly sets split and estimator random_state to each declared integer seed. Which statement correctly describes control and state consumption?
  ✔ o1: Integer random_state resets supported generators; None and shared RandomState have different state-consumption behavior. Control both split and estimator randomness, without guaranteeing identical computation in every environment.
      why: Integer seeds reset supported generators; None/shared RandomState differ. Control is bounded, not universal determinism.
  ✘ o2: Integer random_state, None and shared RandomState all reset supported generators identically, guaranteeing identical computation in every environment.
      why: The state-consumption behaviors differ, and seed control is not universal determinism.
  ✘ o3: Integer random_state resets supported generators, so controlling the estimator makes split randomness irrelevant.
      why: Split randomness and estimator randomness both affect the matched comparison.
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r03
  MEASURES: B:distinguish_random_state_consumption(f1); B:control_split_and_estimator_randomness_without_overclaiming_determinism(f2)   anchors=['assessment:distinguish_random_state_consumption', 'assessment:control_split_and_estimator_randomness_without_overclaiming_determinism']
  taught-before-tested: B.f1←s06; B.f2←s06

### s10 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.
QUESTION [code_exercise, core, grading=client] Complete the split_random_state, baseline_random_state and candidate_random_state argument expressions in supplied_same_seed_trial using the declared seed, and complete the strict candidate-cost paired-win comparison in supplied_strict_cost_win. Preserve incomplete-pair handling, ties in the denominator, summaries and execution traces.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy', 'pandas']} constraints.allowed=['import numpy as np', 'from supplied dependency modules import required names', 'def with parameters and return', 'variable assignment', 'integer and floating-point literals', 'lists and dictionaries', 'for seed in declared_seed_list', 'if statements', 'list.append', 'dictionary and list indexing', 'len', 'numeric comparisons and arithmetic', 'calls to supplied preparation and evaluation helpers', 'scikit-learn split and estimator calls with random_state', 'fit and predict', 'None', 'np.random.RandomState', 'np.mean(numeric_values)', 'np.std(numeric_values, ddof=0)', 'np.std(numeric_values, ddof=1) when explicitly required by the calculation'] blocked=9 items
  file main.py [editable]:
# Supplied input loading and dependencies.
import pandas as pd

trials = pd.read_csv('paired_trials.csv').to_dict('records')

declared_seed_list = pd.read_csv('paired_trials.csv')['seed'].tolist()

call_trace = []

import numpy as np

# Supplied evaluation scaffold. Complete the marked expressions; preserve the rest.
if __name__:
    def supplied_same_seed_trial(seed):
        return paired_trial(seed, split_random_state=None, baseline_random_state=None, candidate_random_state=None)  # TODO: same-seed arguments

    def supplied_strict_cost_win(pair):
        return None  # TODO: strict candidate-cost paired-win comparison
    def run_pair(seed, split_random_state, baseline_random_state, candidate_random_state):
        assert split_random_state == seed
        assert baseline_random_state == seed
        assert candidate_random_state == seed
        for row in trials:
            if row['seed'] == seed:
                call_trace.append({'seed': seed, 'split_random_state': split_random_state, 'baseline_random_state': baseline_random_state, 'candidate_random_state': candidate_random_state})
                return row
        raise ValueError('undeclared seed')

    def supplied_numeric_pair_present(pair):
        if not isinstance(pair, dict):
            return False
        for name in ('baseline_result', 'candidate_result'):
            value = pair.get(name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return False
            if value != value or value in (float('inf'), -float('inf')):
                return False
        return True

    def evaluate(declared_seed_list):
        pairs = []
        baseline_results = []
        candidate_results = []
        wins = 0
        for seed in declared_seed_list:
            pair = seed_trial(seed)
            if supplied_numeric_pair_present(pair):
                pairs.append(pair)
                baseline_results.append(pair['baseline_result'])
                candidate_results.append(pair['candidate_result'])
                if win_rule(pair):
                    wins = wins + 1
        n = len(pairs)
        win_probability = None
        baseline_mean = None
        baseline_std = None
        candidate_mean = None
        candidate_std = None
        if n > 0:
            win_probability = wins / n
            baseline_mean = trial_mean(baseline_results)
            baseline_std = trial_std(baseline_results, ddof=0)
            candidate_mean = trial_mean(candidate_results)
            candidate_std = trial_std(candidate_results, ddof=0)
        return {'pairs': pairs, 'completed_pair_count': n, 'win_count': wins, 'win_probability': win_probability, 'baseline_mean': baseline_mean, 'baseline_std': baseline_std, 'candidate_mean': candidate_mean, 'candidate_std': candidate_std, 'limitation': 'Declared split and estimator random sources are controlled; identical computation in every environment is not guaranteed.'}

# Supplied callable operations; keep these assignments unchanged.
supplied_run_pair = run_pair
supplied_np_mean = np.mean
supplied_np_std = np.std
paired_trial = supplied_run_pair
trial_mean = supplied_np_mean
trial_std = supplied_np_std

# Complete the marked bindings and expression holes; preserve the remaining scaffold.
seed_trial = supplied_same_seed_trial
win_rule = supplied_strict_cost_win

  SOLUTION main.py:
# Supplied input loading and dependencies.
import pandas as pd

trials = pd.read_csv('paired_trials.csv').to_dict('records')

declared_seed_list = pd.read_csv('paired_trials.csv')['seed'].tolist()

call_trace = []

import numpy as np

# Supplied evaluation scaffold. Retain unchanged; complete only the top-level bindings below.
if __name__:
    def supplied_same_seed_trial(seed):
        return paired_trial(seed, split_random_state=seed, baseline_random_state=seed, candidate_random_state=seed)

    def supplied_strict_cost_win(pair):
        return pair['candidate_result'] < pair['baseline_result']
    def run_pair(seed, split_random_state, baseline_random_state, candidate_random_state):
        assert split_random_state == seed
        assert baseline_random_state == seed
        assert candidate_random_state == seed
        for row in trials:
            if row['seed'] == seed:
                call_trace.append({'seed': seed, 'split_random_state': split_random_state, 'baseline_random_state': baseline_random_state, 'candidate_random_state': candidate_random_state})
                return row
        raise ValueError('undeclared seed')

    def supplied_numeric_pair_present(pair):
        if not isinstance(pair, dict):
            return False
        for name in ('baseline_result', 'candidate_result'):
            value = pair.get(name)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return False
            if value != value or value in (float('inf'), -float('inf')):
                return False
        return True

    def evaluate(declared_seed_list):
        pairs = []
        baseline_results = []
        candidate_results = []
        wins = 0
        for seed in declared_seed_list:
            pair = seed_trial(seed)
            if supplied_numeric_pair_present(pair):
                pairs.append(pair)
                baseline_results.append(pair['baseline_result'])
                candidate_results.append(pair['candidate_result'])
                if win_rule(pair):
                    wins = wins + 1
        n = len(pairs)
        win_probability = None
        baseline_mean = None
        baseline_std = None
        candidate_mean = None
        candidate_std = None
        if n > 0:
            win_probability = wins / n
            baseline_mean = trial_mean(baseline_results)
            baseline_std = trial_std(baseline_results, ddof=0)
            candidate_mean = trial_mean(candidate_results)
            candidate_std = trial_std(candidate_results, ddof=0)
        return {'pairs': pairs, 'completed_pair_count': n, 'win_count': wins, 'win_probability': win_probability, 'baseline_mean': baseline_mean, 'baseline_std': baseline_std, 'candidate_mean': candidate_mean, 'candidate_std': candidate_std, 'limitation': 'Declared split and estimator random sources are controlled; identical computation in every environment is not guaranteed.'}

# Supplied callable operations; keep these assignments unchanged.
supplied_run_pair = run_pair
supplied_np_mean = np.mean
supplied_np_std = np.std
paired_trial = supplied_run_pair
trial_mean = supplied_np_mean
trial_std = supplied_np_std

# Complete only these callable/value bindings; preserve the supplied scaffold.
seed_trial = supplied_same_seed_trial
win_rule = supplied_strict_cost_win

  test t1 (value_equals, visible=True): {"expr":"evaluate(declared_seed_list)","expected":{"pairs":[{"seed":0,"baseline_result":0.32,"candidate_result":0.31},{"seed":1,"baseline_result":0.33,"candidate_result":0.32},{"seed":2,"baseline_result":0.34,"candidate_result":0.33},{"seed":3,"baseline_result":0.35,"candidate_result":0.36},{"seed":4,"baseline_result":0.36,"candidate_result":0.37}],"completed_pair_count":5,"win_count":3,"win_probability":0.6,"baseline_mean":0.33999999999999997,"baseline_std":0.01414213562373094,"candidate_mean": | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  test t2 (value_equals, visible=False): {"expr":"(evaluate(declared_seed_list), call_trace[-len(declared_seed_list):])","expected":[{"pairs":[{"seed":0,"baseline_result":0.32,"candidate_result":0.31},{"seed":1,"baseline_result":0.33,"candidate_result":0.32},{"seed":2,"baseline_result":0.34,"candidate_result":0.33},{"seed":3,"baseline_result":0.35,"candidate_result":0.36},{"seed":4,"baseline_result":0.36,"candidate_result":0.37}],"completed_pair_count":5,"win_count":3,"win_probability":0.6,"baseline_mean":0.33999999999999997,"baseline_ | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  test incomplete_pairs (value_equals, visible=False): {"expr":"(lambda saved: (trials.__setitem__(slice(None), [dict(row, candidate_result=None) if j == 0 else dict(row, baseline_result='missing') if j == 1 else dict(row, candidate_result=row['baseline_result']) if j == 2 else row for j, row in enumerate(saved)]), evaluate(declared_seed_list), trials.__setitem__(slice(None), saved))[1])(trials.copy())","expected":{"pairs":[{"seed":2,"baseline_result":0.34,"candidate_result":0.34},{"seed":3,"baseline_result":0.35,"candidate_result":0.36},{"seed":4," | on-fail: Only complete numeric pairs count; ties are not wins.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"3db0f48e6da3a9bac8297c0e12641f901cb0a68b34d10a6dbce4b3fa60241016","tests_passed":3}
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Complete only the indicated expressions using the supplied inputs.', 'Keep guards, structured evidence and result fields unchanged.']  remediation→r04
  MEASURES: B:control_split_and_estimator_randomness_without_overclaiming_determinism(f2); B:collect_paired_seed_trials_and_estimate_empirical_win_probability(f3,f4); B:summarize_repeated_results_with_mean_and_specified_standard_deviation(f5,f6)   anchors=['practice', 'assessment:control_split_and_estimator_randomness_without_overclaiming_determinism', 'assessment:collect_paired_seed_trials_and_estimate_empirical_win_probability', 'assessment:summarize_repeated_results_with_mean_and_specified_standard_deviation']
  taught-before-tested: B.f2←s06; B.f3←s06; B.f4←s06; B.f5←s06; B.f6←s06

### s11 · explainer · Select by validation
(intro) Good training results with worse validation results under the same score interpretation provide overfitting evidence. Investigate declared regularization settings under the fixed validation protocol. ⟦C:tb1⟧
(mechanism) A good-training/poor-validation gap is evidence of overfitting. Compare declared settings under the same scoring interpretation and select by the predeclared validation criterion, not training score alone. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦C.f1 C.f2 C.f3 C:tb2⟧
[SIDE_BY_SIDE] Select by the fixed validation criterion, not training cost alone. left_label: Matched training and validation costs | right_label: Estimator-specific strength directions
  left:
[TABLE ds.regularization_records cols=['configuration_id', 'estimator', 'parameter_name', 'parameter_value', 'strength_direction', 'training_expected_error_cost', 'TP', 'FP', 'FN', 'TN', 'expected_error_cost', 'operating_requirements_met'] ] caption: Fixed-criterion regularization evidence
  right:
[TABLE ds.regularization_directions cols=['estimator', 'parameter', 'direction'] ] caption: Estimator-specific penalty directions
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract
[TABLE computed result ] caption: Fixed-contract eligibility and retained validation selection; null rates remain undefined.
  produced by sql: WITH rates AS (
SELECT r.*, 1.0*r.FP/NULLIF(r.FP+r.TN,0) AS conditioned_FPR,
1.0*r.FN/NULLIF(r.FN+r.TP,0) AS conditioned_FNR,
c.deployment_negative_probability, c.deployment_positive_probability, c.cost_FP, c.cost_FN,
c.expected_cost_bound, (r.operating_requirements_met = TRUE) AS operating_met,
r.cohort_id = 'orders_100' AS matched_cohort, r.configuration_id AS tie_order 
FROM records r CROSS JOIN contract c  
), costs AS (
SELECT *, deployment_negative_probability*conditioned_FPR*cost_FP + deployment_positive_probability*conditioned_FNR*cost_FN AS computed_cost FROM rates
), eligible AS (
SELECT *, CASE WHEN NOT matched_cohort THEN 'different cohort'
WHEN conditioned_FPR IS NULL OR conditioned_FNR IS NULL THEN 'undefined required rate'
WHEN computed_cost > expected_cost_bound THEN 'quality bound failed'
WHEN NOT operating_met THEN 'operating requirement failed'
ELSE 'eligible' END AS eligibility_reason FROM costs
), ranked AS (
SELECT configuration_id, ROW_NUMBER() OVER (ORDER BY computed_cost, tie_order) AS eligible_rank
FROM eligible WHERE eligibility_reason = 'eligible'
)
SELECT a.configuration_id, a.cohort_id, a.FP+a.TN AS actual_negative_denominator,
a.FN+a.TP AS actual_positive_denominator, a.conditioned_FPR, a.conditioned_FNR,
a.computed_cost, a.expected_cost_bound, a.eligibility_reason,
b.eligible_rank, CASE WHEN b.eligible_rank=1 THEN TRUE ELSE FALSE END AS retained_selection
FROM eligible a LEFT JOIN ranked b ON a.configuration_id=b.configuration_id ORDER BY a.tie_order
  result columns=['configuration_id', 'cohort_id', 'actual_negative_denominator', 'actual_positive_denominator', 'conditioned_FPR', 'conditioned_FNR', 'computed_cost', 'expected_cost_bound', 'eligibility_reason', 'eligible_rank', 'retained_selection'] rows(2)=[["stronger_penalty","orders_100",80,20,0.1,0.2,0.28,0.3,"eligible",1,true],["weak_penalty","orders_100",80,20,0.1875,0.2,0.3500000000000001,0.3,"quality bound failed",null,false]]

### s12 · explainer · Estimator-specific strength
(mechanism) Protected-test observations must not fit preprocessing, choose models or tune settings: that leaks information. Regularization penalizes complexity during fitting. Larger Ridge alpha increases the penalty; LogisticRegression C is inverse regularization strength, so larger C weakens regularization. ⟦C.f4 C.f5 C.f6 C:tb3⟧

### s13 · explainer · Inspect setting evidence
(example) Read training and validation cost under the same interpretation. A setting with worse training cost can still be the eligible minimum-validation-cost choice. Retain matched cohort, supplied probabilities and error costs. Identify the estimator before interpreting parameter direction: Ridge alpha and LogisticRegression C run in opposite strength directions. The gap supports investigation, not a claim that every validation weakness has the same cause. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C:tb4⟧

### s14 · video · Inspect select regularization in response to validation-observed overfitting
[VIDEO Recognize validation evidence of overfitting] bridge-before: Watch for falling training loss alongside rising validation loss. Here, loss is lower-is-better: the useful signal is worsening validation performance despite improving training performance, not simply a numerical difference. | bridge-after: The clip establishes overfitting evidence, not setting selection. The text supplies fixed-protocol validation selection, conditional error rates and undefined-rate handling for empty conditioning groups, deployment-weighted error cost, protected-test safeguards, and the opposite penalty directions of Ridge alpha and LogisticRegression C.
  - EehRcPo1M-Q 35-115s facts=['f1'] label: Compare training and validation loss to recognize overfitting | summary: Overfitting occurs when a model fits training observations closely but generalizes poorly. A one-input, one-output example illustrates a fitted pattern that follows training values too closely. The speaker then describes training loss continuing to fall while validation loss rises as training proceeds. Under this lower-is-better interpretation, the divergence provides evidence of overfitting and motivates considering regularization.

### s15 · explainer · Training alone cannot choose
(misconception) Best training cost need not mean best validation choice. Parameter direction is estimator-specific: larger LogisticRegression C weakens regularization. ⟦C.f2 C.f6 C:tb5⟧

### s16 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.
QUESTION [choice, core, grading=client] For a LogisticRegression setting, C is reduced while the protocol stays fixed. What does this change mean?
  ✔ o1: Regularization strength increases because C is inverse regularization strength.
      why: Smaller C means stronger regularization; Ridge alpha uses the direct penalty direction.
  ✘ o2: Regularization strength decreases because C is the direct penalty strength.
      why: C is inverse, not direct, regularization strength.
  ✘ o3: Reducing LogisticRegression C weakens regularization, unlike increasing Ridge alpha
      why: Both reducing LogisticRegression C and increasing Ridge alpha strengthen their respective penalties; C is inverse regularization strength.
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r05
  MEASURES: C:interpret_estimator_specific_regularization_strength(f6)   anchors=['assessment:interpret_estimator_specific_regularization_strength']
  taught-before-tested: C.f6←s12

### s17 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.
QUESTION [code_exercise, core, grading=client] Complete the FPR and FNR division expressions and the deployment-weighted expected-cost expression. Preserve the existing empty-group guards, training comparison, operating checks, selection logic and returned fields.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy', 'pandas']} constraints.allowed=['import and from ... import for required dependencies', 'def with parameters and return', 'local assignments and numeric literals', 'lists, tuples, and dictionaries', 'for loops over supplied settings', 'if and else branches', 'arithmetic and comparison operators', 'NumPy array operations and Boolean masks', 'Ridge(alpha=...)', 'LogisticRegression(C=...)', 'training-fitted preprocessing pipeline fit and predict', 'confusion_matrix(..., labels=[0, 1])'] blocked=9 items
  file main.py [editable]:
# Supplied input loading and dependencies.
import pandas as pd

contract = pd.read_csv('acceptance_contract.csv').iloc[0]

p_negative = contract['deployment_negative_probability']

p_positive = contract['deployment_positive_probability']

cost_FP = contract['cost_FP']

cost_FN = contract['cost_FN']

bound = contract['expected_cost_bound']

settings = pd.read_csv('regularization_records.csv').to_dict('records')

# Supplied evaluation scaffold. Complete the marked expressions; preserve the rest.
if __name__:
    def deployment_weighted_cost(p_negative, FPR, cost_FP, p_positive, FNR, cost_FN):
        return p_negative * FPR * cost_FP + p_positive * FNR * cost_FN

    def evaluate(settings, p_negative, p_positive, cost_FP, cost_FN, bound):
        records = []
        interpretation = []
        selected = None
        best_cost = None
        for setting in settings:
            if setting['cohort_id'] == 'orders_100':
                FP = setting['FP']
                TN = setting['TN']
                FN = setting['FN']
                TP = setting['TP']
                FPR = None
                FNR = None
                expected_cost = None
                if FP + TN > 0:
                    FPR = None  # TODO: conditioned negative rate
                if FN + TP > 0:
                    FNR = None  # TODO: conditioned positive rate
                if FP + TN > 0:
                    if FN + TP > 0:
                        expected_cost = None  # TODO: deployment-weighted expected cost
                train_FP = setting['training_FP']
                train_TN = setting['training_TN']
                train_FN = setting['training_FN']
                train_TP = setting['training_TP']
                training_cost = None
                if train_FP + train_TN > 0:
                    if train_FN + train_TP > 0:
                        training_cost = p_negative * train_FP / (train_FP + train_TN) * cost_FP + p_positive * train_FN / (train_FN + train_TP) * cost_FN
                eligible = False
                if expected_cost is not None and training_cost is not None:
                    if expected_cost <= bound:
                        if setting['operating_requirements_met']:
                            eligible = True
                            if best_cost is None:
                                best_cost = expected_cost
                                selected = setting['configuration_id']
                            elif expected_cost < best_cost:
                                best_cost = expected_cost
                                selected = setting['configuration_id']
                records.append({'configuration_id': setting['configuration_id'], 'parameter_value': setting['parameter_value'], 'FPR': FPR, 'FNR': FNR, 'actual_negative_count': FP + TN, 'actual_positive_count': FN + TP, 'training_cost': training_cost, 'validation_cost': expected_cost, 'eligible': eligible})
                gap = None
                if training_cost is not None and expected_cost is not None:
                    gap = expected_cost - training_cost
                interpretation.append({'configuration_id': setting['configuration_id'], 'training_cost': training_cost, 'validation_cost': expected_cost, 'validation_minus_training': gap})
        return {'records': records, 'selected_configuration': selected, 'direction': 'C is inverse regularization strength; smaller C increases the penalty. Larger Ridge alpha increases the penalty.', 'interpretation': interpretation}

# Supplied callable operations; keep these assignments unchanged.
supplied_deployment_weighted_cost = deployment_weighted_cost

# Supplied operation binding.
cost_rule = supplied_deployment_weighted_cost

  SOLUTION main.py:
# Supplied input loading and dependencies.
import pandas as pd

contract = pd.read_csv('acceptance_contract.csv').iloc[0]

p_negative = contract['deployment_negative_probability']

p_positive = contract['deployment_positive_probability']

cost_FP = contract['cost_FP']

cost_FN = contract['cost_FN']

bound = contract['expected_cost_bound']

settings = pd.read_csv('regularization_records.csv').to_dict('records')

# Supplied evaluation scaffold. Preserve the scaffold outside the requested TODO expressions.
if __name__:
    def deployment_weighted_cost(p_negative, FPR, cost_FP, p_positive, FNR, cost_FN):
        return p_negative * FPR * cost_FP + p_positive * FNR * cost_FN

    def evaluate(settings, p_negative, p_positive, cost_FP, cost_FN, bound):
        records = []
        interpretation = []
        selected = None
        best_cost = None
        for setting in settings:
            if setting['cohort_id'] == 'orders_100':
                FP = setting['FP']
                TN = setting['TN']
                FN = setting['FN']
                TP = setting['TP']
                FPR = None
                FNR = None
                expected_cost = None
                if FP + TN > 0:
                    FPR = FP / (FP + TN)
                if FN + TP > 0:
                    FNR = FN / (FN + TP)
                if FP + TN > 0:
                    if FN + TP > 0:
                        expected_cost = p_negative * FPR * cost_FP + p_positive * FNR * cost_FN
                train_FP = setting['training_FP']
                train_TN = setting['training_TN']
                train_FN = setting['training_FN']
                train_TP = setting['training_TP']
                training_cost = None
                if train_FP + train_TN > 0:
                    if train_FN + train_TP > 0:
                        training_cost = p_negative * train_FP / (train_FP + train_TN) * cost_FP + p_positive * train_FN / (train_FN + train_TP) * cost_FN
                eligible = False
                if expected_cost is not None and training_cost is not None:
                    if expected_cost <= bound:
                        if setting['operating_requirements_met']:
                            eligible = True
                            if best_cost is None:
                                best_cost = expected_cost
                                selected = setting['configuration_id']
                            elif expected_cost < best_cost:
                                best_cost = expected_cost
                                selected = setting['configuration_id']
                records.append({'configuration_id': setting['configuration_id'], 'parameter_value': setting['parameter_value'], 'FPR': FPR, 'FNR': FNR, 'actual_negative_count': FP + TN, 'actual_positive_count': FN + TP, 'training_cost': training_cost, 'validation_cost': expected_cost, 'eligible': eligible})
                gap = None
                if training_cost is not None and expected_cost is not None:
                    gap = expected_cost - training_cost
                interpretation.append({'configuration_id': setting['configuration_id'], 'training_cost': training_cost, 'validation_cost': expected_cost, 'validation_minus_training': gap})
        return {'records': records, 'selected_configuration': selected, 'direction': 'C is inverse regularization strength; smaller C increases the penalty. Larger Ridge alpha increases the penalty.', 'interpretation': interpretation}

# Supplied callable operations; keep these assignments unchanged.
supplied_deployment_weighted_cost = deployment_weighted_cost

# Complete only the final operation binding.
cost_rule = supplied_deployment_weighted_cost

  test t1 (value_equals, visible=True): {"expr":"evaluate(settings, p_negative, p_positive, cost_FP, cost_FN, bound)","expected":{"records":[{"configuration_id":"weak_penalty","parameter_value":10,"FPR":0.1875,"FNR":0.2,"actual_negative_count":80,"actual_positive_count":20,"training_cost":0.1,"validation_cost":0.3500000000000001,"eligible":false},{"configuration_id":"stronger_penalty","parameter_value":1,"FPR":0.1,"FNR":0.2,"actual_negative_count":80,"actual_positive_count":20,"training_cost":0.18000000000000002,"validation_cost":0.28 | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  test t2 (value_equals, visible=False): {"expr":"evaluate(settings, p_negative, p_positive, cost_FP, cost_FN, -1)","expected":{"records":[{"configuration_id":"weak_penalty","parameter_value":10,"FPR":0.1875,"FNR":0.2,"actual_negative_count":80,"actual_positive_count":20,"training_cost":0.1,"validation_cost":0.3500000000000001,"eligible":false},{"configuration_id":"stronger_penalty","parameter_value":1,"FPR":0.1,"FNR":0.2,"actual_negative_count":80,"actual_positive_count":20,"training_cost":0.18000000000000002,"validation_cost":0.28,"e | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"1b3da87d294ae3d124350d99951d86340e9a21eaf070536b52116757ea30fa3b","tests_passed":2}
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Inspect the supplied callable assignments immediately above the final TODO.', 'Change only the final binding; keep the evaluation scaffold and its fixed evidence guards unchanged.']  remediation→r06
  MEASURES: C:recognize_overfitting_from_comparable_training_validation_scores(f1); C:select_regularization_using_fixed_validation_criterion_without_test_access(f2,f5); C:calculate_conditional_error_rates_and_identify_undefined_rates(f3); C:calculate_deployment_weighted_expected_error_cost(f4)   anchors=['practice', 'assessment:recognize_overfitting_from_comparable_training_validation_scores', 'assessment:select_regularization_using_fixed_validation_criterion_without_test_access', 'assessment:calculate_conditional_error_rates_and_identify_undefined_rates', 'assessment:calculate_deployment_weighted_expected_error_cost']
  taught-before-tested: C.f1←s11; C.f2←s11; C.f5←s12; C.f3←s11; C.f4←s12

### s18 · explainer · Keep costs and boundaries fixed
(intro) Resolve a trial budget and scoring protocol before search. Candidate settings alone do not define a stopping boundary. ⟦D:tb1⟧
(mechanism) GridSearchCV enumerates param_grid combinations; RandomizedSearchCV samples configurations bounded by n_iter. Predeclare scoring and evaluation protocol, then inspect validation-selected best_params_ and cv_results_. In a supplied manual search, iterate bounded configuration dictionaries, execute declared trials and record validation results without exceeding the fixed budget. ⟦D.f1 D.f2 D.f3 D:tb2⟧
(mechanism) FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) on actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose models or tune settings without leaking information. ⟦D.f4 D.f5 D.f6 D:tb3⟧
[TABLE computed result ] caption: Budget boundary: supplied configurations are not all completed trials.
  produced by sql: SELECT r.configuration_id, r.configuration_json, e.override_search_budget AS resolved_budget, r.declared_order < e.override_search_budget AS executed FROM records r CROSS JOIN execution e ORDER BY r.declared_order
  result columns=['configuration_id', 'configuration_json', 'resolved_budget', 'executed'] rows(3)=[["config_1","{\"C\": 10.0, \"random_state\": 0}",2,true],["config_2","{\"C\": 1.0, \"random_state\": 0}",2,true],["config_3","{\"C\": 0.1, \"random_state\": 0}",2,false]]
[TABLE ds.execution_contract cols=['estimator_random_state', 'default_trial_setting', 'override_trial_setting', 'default_search_budget', 'override_search_budget', 'metric_direction', 'tie_policy', 'split_protocol', 'ddof'] ] caption: Fixed execution and reporting contracts
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract
[TABLE computed result ] caption: Fixed-contract eligibility and retained validation selection; null rates remain undefined.
  produced by sql: WITH rates AS (
SELECT r.*, 1.0*r.FP/NULLIF(r.FP+r.TN,0) AS conditioned_FPR,
1.0*r.FN/NULLIF(r.FN+r.TP,0) AS conditioned_FNR,
c.deployment_negative_probability, c.deployment_positive_probability, c.cost_FP, c.cost_FN,
c.expected_cost_bound, (r.operating_requirements_met = TRUE) AS operating_met,
r.cohort_id = 'orders_100' AS matched_cohort, r.declared_order AS tie_order , e.override_search_budget AS resolved_budget
FROM records r CROSS JOIN contract c  CROSS JOIN execution e  WHERE r.declared_order < e.override_search_budget
), costs AS (
SELECT *, deployment_negative_probability*conditioned_FPR*cost_FP + deployment_positive_probability*conditioned_FNR*cost_FN AS computed_cost FROM rates
), eligible AS (
SELECT *, CASE WHEN NOT matched_cohort THEN 'different cohort'
WHEN conditioned_FPR IS NULL OR conditioned_FNR IS NULL THEN 'undefined required rate'
WHEN computed_cost > expected_cost_bound THEN 'quality bound failed'
WHEN NOT operating_met THEN 'operating requirement failed'
ELSE 'eligible' END AS eligibility_reason FROM costs
), ranked AS (
SELECT configuration_id, ROW_NUMBER() OVER (ORDER BY computed_cost, tie_order) AS eligible_rank
FROM eligible WHERE eligibility_reason = 'eligible'
)
SELECT a.configuration_id, a.cohort_id, a.TP, a.FP, a.FN, a.TN, a.FP+a.TN AS actual_negative_denominator,
a.FN+a.TP AS actual_positive_denominator, a.conditioned_FPR, a.conditioned_FNR,
a.computed_cost, a.expected_cost_bound, a.eligibility_reason,
b.eligible_rank, CASE WHEN b.eligible_rank=1 THEN TRUE ELSE FALSE END AS retained_selection
FROM eligible a LEFT JOIN ranked b ON a.configuration_id=b.configuration_id ORDER BY a.tie_order
  result columns=['configuration_id', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'actual_negative_denominator', 'actual_positive_denominator', 'conditioned_FPR', 'conditioned_FNR', 'computed_cost', 'expected_cost_bound', 'eligibility_reason', 'eligible_rank', 'retained_selection'] rows(2)=[["config_1","orders_100",16,15,4,65,80,20,0.1875,0.2,0.3500000000000001,0.3,"quality bound failed",null,false],["config_2","orders_100",16,8,4,72,80,20,0.1,0.2,0.28,0.3,"eligible",1,true]]

### s19 · explainer · Resolve keyword overrides
(mechanism) Define a default budget parameter and accept explicit keyword overrides. Resolve the budget before iterating the configuration dictionary/list. ⟦D.f7 D:tb4⟧

### s20 · explainer · Inspect completed trials
(example) The execution contract distinguishes default and overridden budgets. Resolve the override before trials, then retain only completed configurations and their validation results. A supplied third response is not a completed trial when the budget stops earlier. Keep scoring, actual-class denominators, deployment probabilities and costs fixed. Inspect selected parameters and trial results under the declared protocol; protected-test results are not search evidence. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D:tb5⟧

### s21 · explainer · An override replaces the default
(misconception) An overridden budget, not the default, governs execution. Validation-selected settings do not authorize protected-test inspection or continued searching to improve that result. ⟦D.f2 D.f6 D.f7 D:tb6⟧

### s22 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.
QUESTION [choice, core, grading=client] A manual search has three configurations, default budget 3 and keyword budget=2. Which response correctly applies budget, search semantics and evidence isolation?
  ✔ o1: Resolve the override before executing the first two trials. GridSearchCV enumerates param_grid combinations; RandomizedSearchCV is bounded by n_iter. Inspect validation-selected best_params_ and cv_results_ under the fixed protocol. Use validation evidence only; do not consult protected-test results.
      why: The override bounds execution; grid enumeration differs from randomized n_iter sampling, and selection uses validation only.
  ✘ o2: Execute all three trials, then retain two. GridSearchCV samples n_iter configurations, while RandomizedSearchCV enumerates param_grid combinations.
      why: Retaining fewer outputs does not undo excess execution, and the grid/randomized semantics are reversed.
  ✘ o3: Execute the first two trials, then consult protected-test results to choose configurations and best_params_.
      why: Consulting protected tests to choose configurations leaks evidence into selection.
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r07
  MEASURES: D:exclude_protected_test_evidence_from_search(f6); D:interpret_validation_selected_search_results(f1,f2)   anchors=['assessment:exclude_protected_test_evidence_from_search', 'assessment:interpret_validation_selected_search_results']
  taught-before-tested: D.f6←s18; D.f1←s18; D.f2←s18

### s23 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.
QUESTION [code_exercise, stretch, grading=client] Complete the bounded configuration-slice expression in the search loop and the deployment-weighted cost expression in deployment_weighted_cost. Preserve budget normalization, eligibility, trial tracing and returned fields.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy', 'pandas']} constraints.allowed=['import statements for required supplied library or client dependencies', 'def with a default budget parameter', 'function calls with explicit keyword arguments', 'return statements', 'variable assignment', 'dictionary literals and key access', 'list literals, indexing, slicing, and append', 'for loops over the bounded configuration list', 'if and else conditionals', 'None for undefined rates', 'numeric literals', 'arithmetic and comparison operators', 'len', 'calls to the supplied trial execution interface'] blocked=11 items
  file main.py [editable]:
# Supplied input loading and dependencies.
import pandas as pd

contract = pd.read_csv('acceptance_contract.csv').iloc[0]

p_negative = contract['deployment_negative_probability']

p_positive = contract['deployment_positive_probability']

cost_FP = contract['cost_FP']

cost_FN = contract['cost_FN']

bound = contract['expected_cost_bound']

import json

trials = pd.read_csv('search_trials.csv').to_dict('records')

configurations = [json.loads(row['configuration_json']) for row in trials]

CALLS = []

# Supplied evaluation scaffold. Complete the marked expressions; preserve the rest.
if __name__:
    def supplied_budget_prefix(configurations, budget):
        return configurations[:budget]
    def run_trial(configuration):
        for row in trials:
            if json.loads(row['configuration_json']) == configuration:
                CALLS.append(configuration.copy())
                return row
        raise ValueError('configuration outside declared search space')

    def deployment_weighted_cost(p_negative, FPR, cost_FP, p_positive, FNR, cost_FN):
        return None  # TODO: deployment-weighted expected cost

    def search(configurations, p_negative, p_positive, cost_FP, cost_FN, bound, budget=3):
        if budget < 0:
            budget = 0
        if budget > len(configurations):
            budget = len(configurations)
        records = []
        selected = None
        best_cost = None
        for configuration in (None):  # TODO: bounded configuration slice
            trial = trial_interface(configuration)
            FP = trial['FP']
            TN = trial['TN']
            FN = trial['FN']
            TP = trial['TP']
            FPR = None
            FNR = None
            expected_cost = None
            if FP + TN > 0:
                FPR = FP / (FP + TN)
            if FN + TP > 0:
                FNR = FN / (FN + TP)
            if FP + TN > 0:
                if FN + TP > 0:
                    expected_cost = cost_rule(p_negative, FPR, cost_FP, p_positive, FNR, cost_FN)
            eligible = False
            if expected_cost is not None:
                if expected_cost <= bound:
                    if trial['operating_requirements_met']:
                        eligible = True
                        if best_cost is None:
                            best_cost = expected_cost
                            selected = configuration
                        elif expected_cost < best_cost:
                            best_cost = expected_cost
                            selected = configuration
            records.append({'configuration': configuration, 'cohort_id': trial['cohort_id'], 'FP': FP, 'TN': TN, 'FN': FN, 'TP': TP, 'actual_negative_count': FP + TN, 'actual_positive_count': FN + TP, 'FPR': FPR, 'FNR': FNR, 'expected_cost': expected_cost, 'eligible': eligible})
        return {'resolved_budget': budget, 'completed_trials': len(records), 'records': records, 'selected_configuration': selected}

# Supplied callable operations; keep these assignments unchanged.
supplied_run_trial = run_trial
supplied_deployment_weighted_cost = deployment_weighted_cost
trial_interface = supplied_run_trial
cost_rule = supplied_deployment_weighted_cost

# Callable/value bindings.
budgeted_configurations = supplied_budget_prefix

  SOLUTION main.py:
# Supplied input loading and dependencies.
import pandas as pd

contract = pd.read_csv('acceptance_contract.csv').iloc[0]

p_negative = contract['deployment_negative_probability']

p_positive = contract['deployment_positive_probability']

cost_FP = contract['cost_FP']

cost_FN = contract['cost_FN']

bound = contract['expected_cost_bound']

import json

trials = pd.read_csv('search_trials.csv').to_dict('records')

configurations = [json.loads(row['configuration_json']) for row in trials]

CALLS = []

# Supplied evaluation scaffold. Preserve the scaffold outside the requested TODO expressions.
if __name__:
    def supplied_budget_prefix(configurations, budget):
        return configurations[:budget]
    def run_trial(configuration):
        for row in trials:
            if json.loads(row['configuration_json']) == configuration:
                CALLS.append(configuration.copy())
                return row
        raise ValueError('configuration outside declared search space')

    def deployment_weighted_cost(p_negative, FPR, cost_FP, p_positive, FNR, cost_FN):
        return p_negative * FPR * cost_FP + p_positive * FNR * cost_FN

    def search(configurations, p_negative, p_positive, cost_FP, cost_FN, bound, budget=3):
        if budget < 0:
            budget = 0
        if budget > len(configurations):
            budget = len(configurations)
        records = []
        selected = None
        best_cost = None
        for configuration in configurations[:budget]:
            trial = trial_interface(configuration)
            FP = trial['FP']
            TN = trial['TN']
            FN = trial['FN']
            TP = trial['TP']
            FPR = None
            FNR = None
            expected_cost = None
            if FP + TN > 0:
                FPR = FP / (FP + TN)
            if FN + TP > 0:
                FNR = FN / (FN + TP)
            if FP + TN > 0:
                if FN + TP > 0:
                    expected_cost = cost_rule(p_negative, FPR, cost_FP, p_positive, FNR, cost_FN)
            eligible = False
            if expected_cost is not None:
                if expected_cost <= bound:
                    if trial['operating_requirements_met']:
                        eligible = True
                        if best_cost is None:
                            best_cost = expected_cost
                            selected = configuration
                        elif expected_cost < best_cost:
                            best_cost = expected_cost
                            selected = configuration
            records.append({'configuration': configuration, 'cohort_id': trial['cohort_id'], 'FP': FP, 'TN': TN, 'FN': FN, 'TP': TP, 'actual_negative_count': FP + TN, 'actual_positive_count': FN + TP, 'FPR': FPR, 'FNR': FNR, 'expected_cost': expected_cost, 'eligible': eligible})
        return {'resolved_budget': budget, 'completed_trials': len(records), 'records': records, 'selected_configuration': selected}

# Supplied callable operations; keep these assignments unchanged.
supplied_run_trial = run_trial
supplied_deployment_weighted_cost = deployment_weighted_cost
trial_interface = supplied_run_trial
cost_rule = supplied_deployment_weighted_cost

# Callable/value bindings.
budgeted_configurations = supplied_budget_prefix

  test t1 (value_equals, visible=True): {"expr":"search(configurations, p_negative, p_positive, cost_FP, cost_FN, bound)","expected":{"resolved_budget":3,"completed_trials":3,"records":[{"configuration":{"C":10,"random_state":0},"cohort_id":"orders_100","FP":15,"TN":65,"FN":4,"TP":16,"actual_negative_count":80,"actual_positive_count":20,"FPR":0.1875,"FNR":0.2,"expected_cost":0.3500000000000001,"eligible":false},{"configuration":{"C":1,"random_state":0},"cohort_id":"orders_100","FP":8,"TN":72,"FN":4,"TP":16,"actual_negative_count":80," | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  test t2 (value_equals, visible=False): {"expr":"search(configurations, p_negative, p_positive, cost_FP, cost_FN, bound, budget=2)","expected":{"resolved_budget":2,"completed_trials":2,"records":[{"configuration":{"C":10,"random_state":0},"cohort_id":"orders_100","FP":15,"TN":65,"FN":4,"TP":16,"actual_negative_count":80,"actual_positive_count":20,"FPR":0.1875,"FNR":0.2,"expected_cost":0.3500000000000001,"eligible":false},{"configuration":{"C":1,"random_state":0},"cohort_id":"orders_100","FP":8,"TN":72,"FN":4,"TP":16,"actual_negative_c | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  test t3 (value_equals, visible=False): {"expr":"(search(configurations, p_negative, p_positive, cost_FP, cost_FN, bound, budget=2), CALLS[-2:])","expected":[{"resolved_budget":2,"completed_trials":2,"records":[{"configuration":{"C":10,"random_state":0},"cohort_id":"orders_100","FP":15,"TN":65,"FN":4,"TP":16,"actual_negative_count":80,"actual_positive_count":20,"FPR":0.1875,"FNR":0.2,"expected_cost":0.3500000000000001,"eligible":false},{"configuration":{"C":1,"random_state":0},"cohort_id":"orders_100","FP":8,"TN":72,"FN":4,"TP":16,"ac | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"dcb08d63095bb4a50d6afe3687afc55d13f0d462270b82f20733d29a8f919477","tests_passed":3}
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Complete only the indicated expressions using the supplied inputs.', 'Keep guards, structured evidence and result fields unchanged.']  remediation→r08
  MEASURES: D:execute_trials_within_resolved_budget(f3,f7); D:select_configuration_by_validation_expected_error_cost(f4,f5); D:exclude_protected_test_evidence_from_search(f6)   anchors=['practice', 'assessment:execute_trials_within_resolved_budget', 'assessment:select_configuration_by_validation_expected_error_cost', 'assessment:exclude_protected_test_evidence_from_search']
  taught-before-tested: D.f3←s18; D.f7←s19; D.f4←s18; D.f5←s18; D.f6←s18

### s24 · recap · Keep these distinctions
(takeaway) Verify keyed runs with resolved overrides, repository revision and artifact paths. Control random sources without claiming universal determinism; retain completed paired trials. Select regularization by validation, with estimator-specific parameter direction. Resolve search budgets before trials and keep protected-test observations outside selection. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5 A:tb6 B:tb1 B:tb2 B:tb3 B:tb4 B:tb5 C:tb1 C:tb2 C:tb3 C:tb4 C:tb5 D:tb1 D:tb2 D:tb3 D:tb4 D:tb5 D:tb6⟧
[UP NEXT] Up next: Document supported limitations under the existing risk policy.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: the check — keep a keyed record
(misconception) Contrast a default with the resolved keyword override. Log the value actually used, then verify keyed parameters, revision and resolved artifact path. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb2 A:tb3 A:tb4⟧
(mechanism) Use import mlflow and with mlflow.start_run() as run; retain run_id as the tracking key. Log resolved configuration with mlflow.log_params(params), validation results with mlflow.log_metric(name, value), and the diagnostic file with mlflow.log_artifact(local_path). Inspect git rev-parse --verify HEAD before recording code identity. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Retrieve recorded = mlflow.get_run(run_id); inspect recorded.data.params, recorded.data.metrics and recorded.info.artifact_uri. For repeated metric logging, RunData gives the most recently logged value at the largest step, not the full history. Define function defaults, accept keyword overrides, and log resolved values. Use os.getcwd() and os.chdir(recorded_directory) when resolving repository/artifact paths; retain the resolved path in lookup. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(mechanism) Use subprocess.run in the intended working directory with captured output to inspect git rev-parse --verify HEAD. Reject a revision mismatch before claiming the keyed artifact belongs to that run. ⟦A.f7 A:tb4⟧
[TABLE ds.execution_contract cols=['estimator_random_state', 'default_trial_setting', 'override_trial_setting', 'default_search_budget', 'override_search_budget', 'metric_direction', 'tie_policy', 'split_protocol', 'ddof'] ] caption: Fixed execution and reporting contracts
### r02 · Revisit: the practice — keep a keyed record
(misconception) Contrast a default with the resolved keyword override. Log the value actually used, then verify keyed parameters, revision and resolved artifact path. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A.f6 A.f7 A:tb2 A:tb3 A:tb4⟧
(mechanism) Use import mlflow and with mlflow.start_run() as run; retain run_id as the tracking key. Log resolved configuration with mlflow.log_params(params), validation results with mlflow.log_metric(name, value), and the diagnostic file with mlflow.log_artifact(local_path). Inspect git rev-parse --verify HEAD before recording code identity. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Retrieve recorded = mlflow.get_run(run_id); inspect recorded.data.params, recorded.data.metrics and recorded.info.artifact_uri. For repeated metric logging, RunData gives the most recently logged value at the largest step, not the full history. Define function defaults, accept keyword overrides, and log resolved values. Use os.getcwd() and os.chdir(recorded_directory) when resolving repository/artifact paths; retain the resolved path in lookup. ⟦A.f4 A.f5 A.f6 A:tb3⟧
(mechanism) Use subprocess.run in the intended working directory with captured output to inspect git rev-parse --verify HEAD. Reject a revision mismatch before claiming the keyed artifact belongs to that run. ⟦A.f7 A:tb4⟧
[TABLE ds.execution_contract cols=['estimator_random_state', 'default_trial_setting', 'override_trial_setting', 'default_search_budget', 'override_search_budget', 'metric_direction', 'tie_policy', 'split_protocol', 'ddof'] ] caption: Fixed execution and reporting contracts
### r03 · Revisit: the check — control and pair trials
(misconception) Contrast repeatable supported seeded calls with universal determinism. Empirical wins are measured among completed matched pairs, not guaranteed future wins. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B:tb2 B:tb3⟧
(mechanism) Integer random_state values reset supported scikit-learn generators for repeatable calls; None and shared RandomState instances consume state differently. Control estimator and split randomness without promising every computation or environment is deterministic. Loop over the declared seeds and collect each matched baseline/candidate validation pair. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Empirical win probability is winning paired trials/all completed paired trials; retain the trial count. Summarize selected numeric results with np.mean(numeric_values) and np.std(numeric_values, ddof=0). The latter divides squared deviations by N before the square root; use ddof=1 only if N−1 is required. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[TABLE ds.paired_trials cols=['seed', 'baseline_result', 'candidate_result'] ] caption: Five completed matched seed trials
### r04 · Revisit: the practice — control and pair trials
(misconception) Contrast repeatable supported seeded calls with universal determinism. Empirical wins are measured among completed matched pairs, not guaranteed future wins. ⟦B.f1 B.f2 B.f3 B.f4 B.f5 B.f6 B:tb2 B:tb3⟧
(mechanism) Integer random_state values reset supported scikit-learn generators for repeatable calls; None and shared RandomState instances consume state differently. Control estimator and split randomness without promising every computation or environment is deterministic. Loop over the declared seeds and collect each matched baseline/candidate validation pair. ⟦B.f1 B.f2 B.f3 B:tb2⟧
(mechanism) Empirical win probability is winning paired trials/all completed paired trials; retain the trial count. Summarize selected numeric results with np.mean(numeric_values) and np.std(numeric_values, ddof=0). The latter divides squared deviations by N before the square root; use ddof=1 only if N−1 is required. ⟦B.f4 B.f5 B.f6 B:tb3⟧
[TABLE ds.paired_trials cols=['seed', 'baseline_result', 'candidate_result'] ] caption: Five completed matched seed trials
### r05 · Revisit: the check — investigate the train–validation gap
(misconception) Contrast training quality with validation selection. Larger Ridge alpha strengthens its penalty; larger LogisticRegression C weakens regularization. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C:tb2 C:tb3⟧
(mechanism) A good-training/poor-validation gap is evidence of overfitting. Compare declared settings under the same scoring interpretation and select by the predeclared validation criterion, not training score alone. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) Protected-test observations must not fit preprocessing, choose models or tune settings: that leaks information. Regularization penalizes complexity during fitting. Larger Ridge alpha increases the penalty; LogisticRegression C is inverse regularization strength, so larger C weakens regularization. ⟦C.f4 C.f5 C.f6 C:tb3⟧
[TABLE ds.regularization_records cols=['configuration_id', 'estimator', 'parameter_name', 'parameter_value', 'strength_direction', 'cohort_id', 'training_TP', 'training_FP', 'training_FN', 'training_TN', 'training_expected_error_cost', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'operating_requirements_met'] ] caption: Fixed-criterion regularization evidence
### r06 · Revisit: the practice — investigate the train–validation gap
(misconception) Contrast training quality with validation selection. Larger Ridge alpha strengthens its penalty; larger LogisticRegression C weakens regularization. ⟦C.f1 C.f2 C.f3 C.f4 C.f5 C.f6 C:tb2 C:tb3⟧
(mechanism) A good-training/poor-validation gap is evidence of overfitting. Compare declared settings under the same scoring interpretation and select by the predeclared validation criterion, not training score alone. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. ⟦C.f1 C.f2 C.f3 C:tb2⟧
(mechanism) Protected-test observations must not fit preprocessing, choose models or tune settings: that leaks information. Regularization penalizes complexity during fitting. Larger Ridge alpha increases the penalty; LogisticRegression C is inverse regularization strength, so larger C weakens regularization. ⟦C.f4 C.f5 C.f6 C:tb3⟧
[TABLE ds.regularization_records cols=['configuration_id', 'estimator', 'parameter_name', 'parameter_value', 'strength_direction', 'cohort_id', 'training_TP', 'training_FP', 'training_FN', 'training_TN', 'training_expected_error_cost', 'TP', 'FP', 'FN', 'TN', 'actual_positive_count', 'actual_negative_count', 'cohort_count', 'precision', 'recall', 'validation_prevalence', 'FPR', 'FNR', 'expected_error_cost', 'operating_requirements_met'] ] caption: Fixed-criterion regularization evidence
### r07 · Revisit: the check — resolve the stopping boundary
(misconception) Contrast default budget with resolved overridden budget. Only executed trials belong in the completed-result record. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D:tb2 D:tb3 D:tb4⟧
(mechanism) GridSearchCV enumerates param_grid combinations; RandomizedSearchCV samples configurations bounded by n_iter. Predeclare scoring and evaluation protocol, then inspect validation-selected best_params_ and cv_results_. In a supplied manual search, iterate bounded configuration dictionaries, execute declared trials and record validation results without exceeding the fixed budget. ⟦D.f1 D.f2 D.f3 D:tb2⟧
(mechanism) FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) on actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose models or tune settings without leaking information. ⟦D.f4 D.f5 D.f6 D:tb3⟧
(mechanism) Define a default budget parameter and accept explicit keyword overrides. Resolve the budget before iterating the configuration dictionary/list. ⟦D.f7 D:tb4⟧
[TABLE ds.search_trials cols=['configuration_id', 'declared_order', 'configuration_json', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'operating_requirements_met'] ] caption: Three declared configuration dictionaries
### r08 · Revisit: the practice — resolve the stopping boundary
(misconception) Contrast default budget with resolved overridden budget. Only executed trials belong in the completed-result record. ⟦D.f1 D.f2 D.f3 D.f4 D.f5 D.f6 D.f7 D:tb2 D:tb3 D:tb4⟧
(mechanism) GridSearchCV enumerates param_grid combinations; RandomizedSearchCV samples configurations bounded by n_iter. Predeclare scoring and evaluation protocol, then inspect validation-selected best_params_ and cv_results_. In a supplied manual search, iterate bounded configuration dictionaries, execute declared trials and record validation results without exceeding the fixed budget. ⟦D.f1 D.f2 D.f3 D:tb2⟧
(mechanism) FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) on actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose models or tune settings without leaking information. ⟦D.f4 D.f5 D.f6 D:tb3⟧
(mechanism) Define a default budget parameter and accept explicit keyword overrides. Resolve the budget before iterating the configuration dictionary/list. ⟦D.f7 D:tb4⟧
[TABLE ds.search_trials cols=['configuration_id', 'declared_order', 'configuration_json', 'cohort_id', 'TP', 'FP', 'FN', 'TN', 'operating_requirements_met'] ] caption: Three declared configuration dictionaries

## OTHER CONTENT (fields without a dedicated renderer)
· result.rows: {"C": 10.0, "random_state": 0}
· result.rows: {"C": 1.0, "random_state": 0}
· result.rows: {"C": 0.1, "random_state": 0}

=========

# EVALUATOR PACKET — Document model risks (mle.tile.033_033)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.model_risk_documentation — Document model limitations and foreseeable misuse under an existing risk policy

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=1
  warn: mle.tile.033_033.s01: prose block without lineage.fact_ids

## SOURCE FACTS — A (mle.model_risk_documentation)   objective: Write a model risk record that preserves the existing access policy and supported limitations.
A.f1: Compare supplied access grants against the existing policy’s permitted identity scope, recording any grant outside that scope rather than defining a new authorization policy.   [sources: google_mlops_pipelines#https://docs.cloud.google.com/architecture/blueprints/security-foundations/authentication-authorization — Authentication and authorization]
A.f2: Literal credentials in an image or its metadata are an exposure risk, so a risk record should describe the handling limitation without copying the secret value.   [sources: docker_docs#https://docs.docker.com/reference/build-checks/secrets-used-in-arg-or-env/ — Description]
A.f3: Model performance can differ by segment even when the aggregate result improves; state the supported limitations of the supplied evaluation rather than implying universal suitability.   [sources: google_mlops_pipelines#Data and model validation]
A.f4: Build the single record from the existing policy fields, preserving the supplied permitted identities, documented task limits and foreseeable misuse cases without extending the permission scope.   [sources: python_tutorial#datastructures.html — List Comprehensions; Sets; Dictionaries]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Document Model Risks.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.prediction_task_definition. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (external_proof): Write one risk record using the supplied existing policy fields, task evidence, evaluation evidence, sample access grants and credential-handling record. Preserve the permitted identity scope, document grants outside that scope, include task limits and foreseeable misuse, and describe credential/data exposure limitations without reproducing secret values.  SUCCESS: The single record preserves the supplied policy fields and permitted identities without expanding permissions; identifies any out-of-scope grant; documents credential/data exposure by location or handling limitation without copying secrets; retains documented task limits and foreseeable misuse cases; and cites supported segment limitations without treating aggregate improvement as evidence of universal suitability.
ASSESSMENT ANCHOR: audit_access_grants_against_permitted_identity_scope facts=['f1']
ASSESSMENT ANCHOR: document_credential_exposure_without_disclosing_secrets facts=['f2']
ASSESSMENT ANCHOR: state_evidence_supported_segment_limitations facts=['f3']
ASSESSMENT ANCHOR: document_task_limits_and_foreseeable_misuse_under_existing_policy facts=['f4']

## DATA ASSETS USED
ds.access_grants: Permitted identity versus observed grants — columns: identity(categorical), policy_permitted(categorical), observed_grant(categorical)
   ["A",true,true]
   ["B",false,true]
ds.aggregate_slice_evidence: Aggregate evidence from the matched slice cohort — columns: system(categorical), cohort_id(identifier), eligible_count(numerical), error_count(numerical), error_probability(numerical)
   ["reference","slices_60",60,12,0.2]
   ["model","slices_60",60,8,0.13333333333333333]
ds.risk_policy_evidence: Existing policy and redacted risk evidence — columns: field(identifier), existing_policy(text), supplied_observation(text), recording_constraint(text)
   ["permitted_identities","A","A and B","B is outside the existing permitted identity scope"]
   ["credential_handling","do not reproduce secret values","sample_image.credential_field [REDACTED]","record the location and exposure-handling limitation only"]
   ["permitted_use","evaluate supplied order-task validation evidence","task-specific validation fixture","no universal suitability claim"]
   ["task_limits","supplied order task and validation cohort only","no evidence outside the supplied cohort","retain the task/cohort boundary"]
   ["foreseeable_misuse","aggregate improvement used as universal segment suitability","zone A and B have different observed sample errors","retain segment limitations; no population disparity established"]
   ["segment_evidence","retain supported sample limitations","zone B has higher observed eligible error proportion than zone A","sample-only evidence; representation beyond supplied sample is unresolved"]
ds.slice_summary: Computed conditional slice summaries — columns: slice(categorical), eligible_count(numerical), error_count(numerical), error_probability(numerical), loss_mean(numerical), loss_std(numerical), ddof(numerical)
   ["A",40,2,0.05,0.05,0.21794494717703367,0]
   ["B",20,6,0.3,0.3,0.45825756949558394,0]
   ["long-distance",20,8,0.4,0.4,0.48989794855663565,0]

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose CPU or GPU capacity for a bounded training workload; Choose a task-compatible training loss; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point; Define a neural network with task-compatible layers and activations; Diagnose training failures from loss and gradient behavior; Diagnose training memory exhaustion; Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline; Evaluate the frozen selected model and threshold against the baseline on the protected test set; Freeze and identify a traceable dataset snapshot for reproducible training; Implement the minibatch forward, backward and optimizer-step loop; Package a versioned model with fitted preprocessing and inference dependencies; Place models and tensors on the correct compute device; Profile tra

## LESSON, in learner order

### s01 · explainer · Preserve existing scope
(intro) Build one bounded risk record from existing policy and supplied evidence. Documentation must not expand permissions or reproduce exposed secrets. ⟦A:tb1⟧
(definition) Compare observed grants with existing permitted identities and record out-of-scope grants rather than defining a new policy. Literal credentials in images or metadata are exposure risks: describe the handling limitation without copying the secret. Aggregate improvement can coexist with segment differences; state supported evaluation limitations, not universal suitability. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Preserve existing policy fields, permitted identities, documented task limits and foreseeable misuse cases in the single record. Do not extend permission scope. ⟦A.f4 A:tb3⟧
[TABLE ds.risk_policy_evidence cols=['field', 'existing_policy', 'supplied_observation', 'recording_constraint'] ] caption: Existing policy and redacted risk evidence
[TABLE ds.access_grants cols=['identity', 'policy_permitted', 'observed_grant'] ] caption: Permitted identity versus observed grants
[TABLE ds.aggregate_slice_evidence cols=['system', 'cohort_id', 'eligible_count', 'error_count', 'error_probability'] ] caption: Aggregate evidence from the matched slice cohort
[TABLE ds.slice_summary cols=['slice', 'eligible_count', 'error_count', 'error_probability', 'loss_mean', 'loss_std', 'ddof'] ] caption: Computed conditional slice summaries

### s02 · explainer · Map evidence into the record
(example) Place existing policy beside supplied observations. An observed identity outside the permitted set is a mismatch to record, not a reason to enlarge that set. Describe the redacted credential-exposure location without copying a value. Carry documented task limits, foreseeable misuse and supported aggregate/segment evidence into one record. Keep permission language separate from measured limitations. ⟦A.f1 A.f2 A.f3 A.f4 A:tb4⟧

### s03 · explainer · Documentation is not permission
(misconception) Documentation is not authorization. Do not enlarge identity scope, claim universal suitability or disclose the credential being flagged. ⟦A.f1 A.f2 A.f3 A.f4 A:tb5⟧

### s04 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.
QUESTION [choice, intro, grading=client] An existing policy permits identity A; a supplied access-grant record includes A and B. What belongs in the risk record?
  ✔ o1: Preserve permitted scope A and identify B as an out-of-scope grant.
      why: Record the deviation without redefining the existing authorization policy.
  ✘ o2: Expand the permitted scope to A and B to match observed grants.
      why: Observed grants do not authorize extending the permitted identity scope.
  ✘ o3: Copy any exposed credential value as evidence of the grant.
      why: Describe exposure location and handling limitation without copying secrets.
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Separate the observations being measured from the fixed decision assumptions.', 'Check each required field against the supplied evidence before drawing the conclusion.']  remediation→r01
  MEASURES: A:document_task_limits_and_foreseeable_misuse_under_existing_policy(f4)   anchors=['assessment:document_task_limits_and_foreseeable_misuse_under_existing_policy']
  taught-before-tested: A.f4←s01

### s05 · hands_on · Write one bounded risk record
 — Use the supplied policy and evaluation evidence to record mismatches and limitations without changing permissions or copying secrets.
QUESTION [external_proof, stretch, grading=client] Produce one text risk-and-use record. Preserve existing policy; do not copy secrets or create new permissions.
permitted_identities: permitted=A; observed=A and B.
credential_handling: permitted=do not reproduce secret values; observed=sample_image.credential_field [REDACTED].
permitted_use: permitted=evaluate supplied order-task validation evidence; observed=task-specific validation fixture.
task_limits: permitted=supplied order task and validation cohort only; observed=no evidence outside the supplied cohort.
foreseeable_misuse: documented misuse=aggregate improvement used as universal segment suitability; observed=zone A and B have different observed sample errors.
segment_evidence: permitted=retain supported sample limitations; observed=zone B has higher observed eligible error proportion than zone A.
Access grants: A granted=True, B granted=True.
Slice evidence: A 2/40=0.05, B 6/20=0.3.
Aggregate and segment errors: reference 12/60=0.2, model 8/60=0.13333333333333333. Retain all scope, task, misuse and redacted-exposure limitations; sample evidence is not universal suitability.
  [unrendered interaction type external_proof] public={"instruction":"Produce one text risk-and-use record. Preserve existing policy; do not copy secrets or create new permissions.\npermitted_identities: permitted=A; observed=A and B.\ncredential_handling: permitted=do not reproduce secret values; observed=sample_image.credential_field [REDACTED].\npermitted_use: permitted=evaluate supplied order-task validation evidence; observed=task-specific validation fixture.\ntask_limits: permitted=supplied order task and validation cohort only; observed=no evidence outside the supplied cohort.\nforeseeable_misuse: documented misuse=aggregate improvement used as universal segment suitability; observed=zone A and B have different observed sample errors.\nsegment_evidence: permitted=retain supported sample limitations; observed=zone B has higher observed eligible error proportion than zone A.\nAccess grants: A granted=True, B granted=True.\nSlice eviden grading={"mode":"manual","rubric":[{"criterion":"Preserve the existing permitted identity scope A and identify the observed B grant as out of scope.","weight":1},{"criterion":"Document only the redacted credential field location and handling limitation, never a secret value.","weight":1},{"criterion":"Retain permitted use, task/cohort limits and foreseeable misuse fields without expanding permissions.","weight":1},{"criterion":"Cite the supplied zone sample proportions and counts; state representation beyond the sample is unresolved and aggregate improvement is not universal suitability.","weight":1}]}
  feedback✔: The single record preserves policy scope and cites bounded supplied evidence without exposing secrets.  feedback✘: Retain every existing-policy field, identify scope deviations, and separate sample evidence from universal suitability.  hints: ['Separate existing permission scope from observed grants.', 'Describe exposure handling without reproducing credential values.']  remediation→r02
  MEASURES: A:audit_access_grants_against_permitted_identity_scope(f1); A:document_credential_exposure_without_disclosing_secrets(f2); A:state_evidence_supported_segment_limitations(f3); A:document_task_limits_and_foreseeable_misuse_under_existing_policy(f4)   anchors=['practice', 'assessment:audit_access_grants_against_permitted_identity_scope', 'assessment:document_credential_exposure_without_disclosing_secrets', 'assessment:state_evidence_supported_segment_limitations', 'assessment:document_task_limits_and_foreseeable_misuse_under_existing_policy']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01

### s06 · recap · Keep these distinctions
(takeaway) Preserve existing permitted identities, task limits and foreseeable misuse in one risk record. Record access mismatches without widening policy. Describe credential exposure without copying secrets. State supported aggregate and segment limitations rather than universal suitability. ⟦A.f1 A.f2 A.f3 A.f4 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Evaluate supplied foundation-model outputs against matched validation evidence.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: the check — one bounded risk record
(misconception) Contrast an observed grant with a permitted identity. Record a mismatch without expanding policy or copying an exposed secret. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3⟧
(definition) Compare observed grants with existing permitted identities and record out-of-scope grants rather than defining a new policy. Literal credentials in images or metadata are exposure risks: describe the handling limitation without copying the secret. Aggregate improvement can coexist with segment differences; state supported evaluation limitations, not universal suitability. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Preserve existing policy fields, permitted identities, documented task limits and foreseeable misuse cases in the single record. Do not extend permission scope. ⟦A.f4 A:tb3⟧
[TABLE ds.risk_policy_evidence cols=['field', 'existing_policy', 'supplied_observation', 'recording_constraint'] ] caption: Existing policy and redacted risk evidence
### r02 · Revisit: the practice — one bounded risk record
(misconception) Contrast an observed grant with a permitted identity. Record a mismatch without expanding policy or copying an exposed secret. ⟦A.f1 A.f2 A.f3 A.f4 A:tb2 A:tb3⟧
(definition) Compare observed grants with existing permitted identities and record out-of-scope grants rather than defining a new policy. Literal credentials in images or metadata are exposure risks: describe the handling limitation without copying the secret. Aggregate improvement can coexist with segment differences; state supported evaluation limitations, not universal suitability. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) Preserve existing policy fields, permitted identities, documented task limits and foreseeable misuse cases in the single record. Do not extend permission scope. ⟦A.f4 A:tb3⟧
[TABLE ds.risk_policy_evidence cols=['field', 'existing_policy', 'supplied_observation', 'recording_constraint'] ] caption: Existing policy and redacted risk evidence

=========

# EVALUATOR PACKET — Evaluate supplied foundation-model outputs (mle.tile.034_034)
Tile summary: 
Legend: ⟦A.f1 A:tb2⟧ = this text claims to teach fact f1 of concept A from teaching block tb2. ✔ correct option, ✘ wrong option.
A = mle.foundation_model_baseline_evaluation — Evaluate supplied foundation or pretrained task-model outputs against a task-specific validation baseline

## DETERMINISTIC GATE (already passed — do not re-derive): PASS  errors=0 warnings=2
  warn: mle.tile.034_034.s01: prose block without lineage.fact_ids
  warn: mle.tile.034_034.s05/ix.mle.tile.034_034.s05: ADVISORY — syntax descriptors with no detector: ['Boolean conditions using and, or, not', 'arithmetic using +, -, *, /', 'array comparisons using == and !=', 'assignment', 'dictionary construction and key access', 'elementwise Boolean masks using &', 'function parameters and calls', 'numeric, string, Boolean and None literals', 'scalar comparisons using ==, !=, <, <=, >, >=']

## SOURCE FACTS — A (mle.foundation_model_baseline_evaluation)   objective: Compare supplied pretrained task outputs with the fixed baseline under declared acceptance rules.
A.f1: Evaluate supplied foundation-model task outputs against the same task-specific labeled validation examples and acceptance requirements used for the reference.   [sources: sagemaker_developer_guide#how-it-works-mlconcepts.html — The machine learning workflow]
A.f2: Compare the supplied output quality with the validation baseline and report observed limitations without treating supplied-output evaluation as construction or training of the application.   [sources: google_mlops_pipelines#Data and model validation]
A.f3: For binary validation counts, FPR = FP/(FP+TN) conditions on actual negatives, and FNR = FN/(FN+TP) conditions on actual positives; an empty conditioning group does not yield a defined rate.   [sources: google_ml_crash_course#classification/accuracy-precision-recall — Accuracy; Recall, or true positive rate; False positive rate; Precision]
A.f4: With zero cost for correct predictions and supplied deployment class probabilities, expected error cost is P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.   [sources: scikit_learn_user_guide#auto_examples/model_selection/plot_cost_sensitive_learning.html — Cost-sensitive learning with constant gains and costs]
A.f5: Do not use protected test observations to fit preprocessing, choose a model or tune its settings; doing so leaks information into the chosen system.   [sources: scikit_learn_user_guide#common_pitfalls.html — 12.2 Data leakage]
note: Start with the concrete fixture and the declared contract; keep the explanation within this tile: Evaluate Supplied Foundation-Model Outputs.
note: Use the registered prerequisite preparation rather than reteaching general Python, statistics, software engineering or cloud administration. This path assumes those foundations; ownership remains bounded to the supplied ML task and existing authorized runtime.
note: Declared direct prerequisites: mle.task_metric_selection, mle.model_acceptance_criteria. Use these as preparation, not additional learning targets. No forward-preview concepts are taught.
note: All numeric values and short names in the work example are illustrative fixture data, not observed production results. Retain each source rule, qualifier, declared budget and policy boundary.
PRACTICE ANCHOR (live_code): Write a Python function, including learner-written imports for required dependencies, that evaluates one supplied foundation-model output set for the order task within existing infrastructure scaffolding. Verify alignment with the fixed labeled validation cohort, score the supplied outputs and reference baseline under the same declared criteria, calculate foundation-output FPR, FNR and expected error cost using supplied deployment class probabilities and error costs, and return one evidence-backed task-quality verdict with observed limitations. Accept only foundation-model outputs as the evaluated candidate; do not fit models, change settings or rank approaches.  SUCCESS: The function verifies matched observations, reports comparable validation metrics for the supplied outputs and baseline, uses actual-negative and actual-positive denominators correctly, and calculates expected error cost under the supplied zero-correct-prediction-cost assumption. It marks rates with empty conditioning groups as undefined rather than zero and does not claim acceptance when required evidence is undefined. Its single verdict follows the fixed acceptance requirements, includes cohort-bounded limitations, and uses no protected-test observations.
ASSESSMENT ANCHOR: verify_matched_validation_cohort_and_acceptance_requirements facts=['f1']
ASSESSMENT ANCHOR: issue_bounded_quality_verdict_against_validation_baseline facts=['f2']
ASSESSMENT ANCHOR: calculate_class_conditional_error_rates_with_empty_group_handling facts=['f3']
ASSESSMENT ANCHOR: calculate_expected_error_cost_from_supplied_deployment_assumptions facts=['f4']
ASSESSMENT ANCHOR: preserve_protected_test_boundary_during_supplied_output_evaluation facts=['f5']

## DATA ASSETS USED
ds.acceptance_contract: Precommitted predictive contract — columns: deployment_negative_probability(numerical), deployment_positive_probability(numerical), cost_FP(numerical), cost_FN(numerical), correct_prediction_cost(numerical), expected_cost_bound(numerical), selection_rule(categorical), tie_rule(categorical), empty_group_rule(categorical), ddof(numerical), operating_limit(numerical)
   [0.8,0.2,1,5,0,0.3,"minimum expected cost among matched eligible records","first in declared order","undefined rate; ineligible when required",0,null]
ds.foundation_outputs: Supplied foundation output file aligned to validation — columns: observation_id(identifier), cohort_id(identifier), output_kind(categorical), foundation_output(categorical,digits-as-label)
   ["order_001","orders_100","foundation-model",1]
   ["order_002","orders_100","foundation-model",1]
   ["order_003","orders_100","foundation-model",1]
   ["order_004","orders_100","foundation-model",1]
   ["order_005","orders_100","foundation-model",1]
   ["order_006","orders_100","foundation-model",1]
   ["order_007","orders_100","foundation-model",1]
   ["order_008","orders_100","foundation-model",1]
   variant v.foundation_wrong_cohort: 1 ops; planted: 
   variant v.foundation_missing_observation: 1 ops; planted: 
   variant v.foundation_duplicate: 1 ops; planted: issue.duplicate_foundation(duplicate_row)
ds.validation_scores: One fixed labeled cohort with unchanged scores — columns: observation_id(identifier), cohort_id(identifier), actual_label(categorical,digits-as-label), score(numerical), reference_output(categorical,digits-as-label)
   ["order_001","orders_100",1,0.8,0]
   ["order_002","orders_100",1,0.8,0]
   ["order_003","orders_100",1,0.8,0]
   ["order_004","orders_100",1,0.8,0]
   ["order_005","orders_100",1,0.8,0]
   ["order_006","orders_100",1,0.8,0]
   ["order_007","orders_100",1,0.8,0]
   ["order_008","orders_100",1,0.8,0]
   variant v.scores_no_positives: 1 ops; planted: 
   variant v.scores_no_negatives: 1 ops; planted: 
   variant v.scores_none_eligible: 100 ops; planted: 

## LIKELY LEAKAGE SURFACE (nearest blocked future concepts): Adjust training batch size to fit available memory; Apply correct neural-network training and evaluation modes; Build a dataset and minibatch loader; Choose CPU or GPU capacity for a bounded training workload; Choose a task-compatible training loss; Compute neural-network gradients with automatic differentiation; Configure a baseline optimizer and learning rate; Construct PyTorch input tensors with compatible shapes and dtypes; Convert an ML notebook prototype into a repeatable executable training script with an explicit entry point; Define a neural network with task-compatible layers and activations; Diagnose training failures from loss and gradient behavior; Diagnose training memory exhaustion; Evaluate the frozen selected model and threshold against the baseline on the protected test set; Execute a bounded managed custom-model training job on an existing platform; Freeze and identify a traceable dataset snapshot for reproducible training; Implement the minibatch forward, backward and optimizer-step loop; Package a versioned model with fitted preprocessing and inference dependencies; Place models and tensors on the correct compute device; Profile training compute and data-loading

## LESSON, in learner order

### s01 · explainer · Cost and protected boundaries
(intro) Evaluate supplied foundation-model outputs for the order task. The bounded target is matched validation evidence, not application construction or model training. ⟦A:tb1⟧
(mechanism) Use the same task-specific labeled validation examples and acceptance requirements as the reference. Compare supplied-output quality with the validation baseline and report observed limitations; this is not application construction or training. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose models or tune settings without leaking information. ⟦A.f4 A.f5 A:tb3⟧
[TABLE computed result ] caption: Aligned validation labels, supplied foundation outputs and reference outputs.
  produced by sql: SELECT v.observation_id, v.cohort_id, v.actual_label, f.foundation_output, v.reference_output FROM labels v LEFT JOIN outputs f ON v.observation_id=f.observation_id AND v.cohort_id=f.cohort_id ORDER BY v.observation_id
  result columns=['observation_id', 'cohort_id', 'actual_label', 'foundation_output', 'reference_output'] rows(100)=[["order_001","orders_100",1,1,0],["order_002","orders_100",1,1,0],["order_003","orders_100",1,1,0],["order_004","orders_100",1,1,0],["order_005","orders_100",1,1,0],["order_006","orders_100",1,1,0],["order_007","orders_100",1,1,0],["order_008","orders_100",1,1,0],["order_009","orders_100",1,1,0],["order_010","orders_100",1,1,0]]
[TABLE ds.acceptance_contract cols=['deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'correct_prediction_cost', 'expected_cost_bound', 'selection_rule', 'tie_rule', 'empty_group_rule', 'ddof', 'operating_limit'] ] caption: Precommitted predictive contract
[TABLE computed result ] caption: Foundation-output counts, conditioning denominators and fixed-contract cost evidence.
  produced by sql: WITH counts AS (
SELECT SUM(CASE WHEN v.actual_label=0 AND f.foundation_output=1 THEN 1 ELSE 0 END) AS FP,
SUM(CASE WHEN v.actual_label=0 AND f.foundation_output=0 THEN 1 ELSE 0 END) AS TN,
SUM(CASE WHEN v.actual_label=1 AND f.foundation_output=0 THEN 1 ELSE 0 END) AS FN,
SUM(CASE WHEN v.actual_label=1 AND f.foundation_output=1 THEN 1 ELSE 0 END) AS TP
FROM labels v JOIN outputs f ON v.observation_id=f.observation_id AND v.cohort_id=f.cohort_id
), rates AS (SELECT *, 1.0*FP/NULLIF(FP+TN,0) AS FPR, 1.0*FN/NULLIF(FN+TP,0) AS FNR FROM counts), costs AS (
SELECT r.*, FP+TN AS actual_negative_denominator, FN+TP AS actual_positive_denominator,
c.deployment_negative_probability, c.deployment_positive_probability, c.cost_FP, c.cost_FN,
c.expected_cost_bound, c.deployment_negative_probability*r.FPR*c.cost_FP + c.deployment_positive_probability*r.FNR*c.cost_FN AS expected_cost
FROM rates r CROSS JOIN contract c)
SELECT *, expected_cost <= expected_cost_bound AS predictive_requirement_met FROM costs
  result columns=['FP', 'TN', 'FN', 'TP', 'FPR', 'FNR', 'actual_negative_denominator', 'actual_positive_denominator', 'deployment_negative_probability', 'deployment_positive_probability', 'cost_FP', 'cost_FN', 'expected_cost_bound', 'expected_cost', 'predictive_requirement_met'] rows(1)=[[8,72,4,16,0.1,0.2,80,20,0.8,0.2,1,5,0.3,0.28,true]]

### s02 · explainer · Check alignment before scoring
(example) Align each supplied output to its labeled validation observation and reference output. A different cohort would not support a matched comparison. Use fixed acceptance requirements, deployment probabilities and error costs, retaining actual-class denominators. Report what these supplied task outputs support and their observed limitations; do not generalize to every foundation model or application. Keep protected-test observations outside fitting and setting choice. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb4⟧

### s03 · explainer · Evaluation is not construction
(misconception) Supplied-output evaluation does not demonstrate application-building or model-training competence. Its conclusion stays task-specific and validation-based. ⟦A.f1 A.f2 A.f5 A:tb5⟧

### s04 · check · Check the distinction
 — Read the supplied evidence and choose the response that follows the declared rule.
QUESTION [choice, intro, grading=client] The supplied outputs are aligned with labeled validation observations. A colleague proposes using protected-test labels to choose a threshold before issuing the validation quality verdict. What should happen?
  ✔ o1: Reject protected-test tuning; use only validation evidence and the fixed acceptance requirements for this verdict.
      why: Protected-test observations must remain outside fitting and selection; alignment does not change that boundary.
  ✘ o2: Use protected-test labels to choose the threshold because the supplied output file is already aligned.
      why: Aligned outputs do not make protected-test tuning permissible.
  ✘ o3: Fit preprocessing on protected-test observations before evaluating the validation outputs.
      why: Protected-test observations cannot fit preprocessing without leaking information.
  feedback✔: Protected-test observations must remain outside fitting and selection; alignment does not change that boundary.  feedback✘: Keep protected-test observations outside preprocessing, model choice and threshold tuning.  hints: ['Identify which observations are proposed for tuning.', 'Alignment and permission to use observations are separate checks.']  remediation→r01
  MEASURES: A:preserve_protected_test_boundary_during_supplied_output_evaluation(f5)   anchors=['assessment:preserve_protected_test_boundary_during_supplied_output_evaluation']
  taught-before-tested: A.f5←s01

### s05 · hands_on · Implement the bounded evaluation
 — Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.
QUESTION [code_exercise, stretch, grading=client] Complete the cohort-equality and observation-ID-equality checks using np.array_equal, then complete the guarded FPR, FNR and deployment-weighted expected-cost expressions. Preserve the supplied shape guards, output-kind restriction and verdict schema.
  runtime={'kind': 'python', 'version': '0.29.5', 'packages': ['numpy', 'pandas']} constraints.allowed=['import numpy as np', 'def', 'function parameters and calls', 'assignment', 'return', 'if/elif/else', 'raise ValueError(...)', 'numeric, string, Boolean and None literals', 'dictionary construction and key access', 'np.asarray(...)', 'array.shape', 'array.dtype', 'array comparisons using == and !=', 'elementwise Boolean masks using &', 'np.sum(...)', 'np.array_equal(...)', 'arithmetic using +, -, *, /', 'scalar comparisons using ==, !=, <, <=, >, >=', 'Boolean conditions using and, or, not'] blocked=15 items
  file main.py [editable]:
# Supplied input loading and dependencies.
import pandas as pd

contract = pd.read_csv('acceptance_contract.csv').iloc[0]

p_negative = contract['deployment_negative_probability']

p_positive = contract['deployment_positive_probability']

cost_FP = contract['cost_FP']

cost_FN = contract['cost_FN']

bound = contract['expected_cost_bound']

validation = pd.read_csv('validation_scores.csv')

outputs = pd.read_csv('foundation_outputs.csv')

ids = validation['observation_id'].to_numpy()

output_ids = outputs['observation_id'].to_numpy()

y = validation['actual_label'].to_numpy()

outputs_y = outputs['foundation_output'].to_numpy()

reference = validation['reference_output'].to_numpy()

output_kind = outputs['output_kind'].to_numpy()

cohort_ids = validation['cohort_id'].to_numpy()

output_cohort_ids = outputs['cohort_id'].to_numpy()

import numpy as np

count_errors = np.sum

# Supplied evaluation scaffold. Complete the marked expressions; preserve the rest.
if __name__:
    def deployment_weighted_cost(p_negative, FPR, cost_FP, p_positive, FNR, cost_FN):
        return p_negative * FPR * cost_FP + p_positive * FNR * cost_FN

    def quantities(y, predictions, p_negative, p_positive, cost_FP, cost_FN):
        FP = conditional_count((y == 0) & (predictions == 1))
        TN = conditional_count((y == 0) & (predictions == 0))
        FN = conditional_count((y == 1) & (predictions == 0))
        TP = conditional_count((y == 1) & (predictions == 1))
        negative_count = FP + TN
        positive_count = FN + TP
        FPR = None
        FNR = None
        expected_cost = None
        if negative_count > 0:
            FPR = None  # TODO: conditioned negative rate
        if positive_count > 0:
            FNR = None  # TODO: conditioned positive rate
        if negative_count > 0:
            if positive_count > 0:
                expected_cost = None  # TODO: deployment-weighted expected cost
        return {'FP': FP, 'TN': TN, 'FN': FN, 'TP': TP, 'actual_negative_count': negative_count, 'actual_positive_count': positive_count, 'FPR': FPR, 'FNR': FNR, 'expected_cost': expected_cost, 'accuracy': conditional_count(y == predictions) / y.shape[0]}

    def evaluate(ids, output_ids, y, outputs_y, reference, output_kind, p_negative, p_positive, cost_FP, cost_FN, bound, cohort_ids, output_cohort_ids):
        if not (None):  # TODO: cohort-equality expression
            return {'aligned': False, 'accepted': False, 'reason': 'unmatched cohorts'}
        if ids.shape != y.shape or cohort_ids.shape != y.shape or output_ids.shape != outputs_y.shape or (output_cohort_ids.shape != outputs_y.shape) or (output_kind.shape != outputs_y.shape):
            return {'aligned': False, 'accepted': False, 'reason': 'unmatched observations'}
        if not (None):  # TODO: observation-ID-equality expression
            return {'aligned': False, 'accepted': False, 'reason': 'unmatched observations'}
        if y.shape != outputs_y.shape or y.shape != reference.shape:
            return {'aligned': False, 'accepted': False, 'reason': 'unmatched observations'}
        if conditional_count(output_kind != 'foundation-model') > 0:
            return {'aligned': False, 'accepted': False, 'reason': 'candidate is not the supplied foundation-model output kind'}
        candidate = quantities(y, outputs_y, p_negative, p_positive, cost_FP, cost_FN)
        baseline = quantities(y, reference, p_negative, p_positive, cost_FP, cost_FN)
        accepted = False
        if candidate['expected_cost'] is not None:
            if candidate['expected_cost'] <= bound:
                accepted = True
        return {'aligned': True, 'candidate': candidate, 'baseline': baseline, 'accepted': accepted, 'bound': bound, 'limitations': 'Quality verdict is bounded to supplied order-task validation observations; no application construction, fitting or protected-test evidence is implied.'}

# Supplied callable operations; keep these assignments unchanged.
supplied_np_sum = np.sum
supplied_np_array_equal = np.array_equal
conditional_count = supplied_np_sum

# Supplied operation binding.
alignment_check = supplied_np_array_equal

  SOLUTION main.py:
# Supplied input loading and dependencies.
import pandas as pd

contract = pd.read_csv('acceptance_contract.csv').iloc[0]

p_negative = contract['deployment_negative_probability']

p_positive = contract['deployment_positive_probability']

cost_FP = contract['cost_FP']

cost_FN = contract['cost_FN']

bound = contract['expected_cost_bound']

validation = pd.read_csv('validation_scores.csv')

outputs = pd.read_csv('foundation_outputs.csv')

ids = validation['observation_id'].to_numpy()

output_ids = outputs['observation_id'].to_numpy()

y = validation['actual_label'].to_numpy()

outputs_y = outputs['foundation_output'].to_numpy()

reference = validation['reference_output'].to_numpy()

output_kind = outputs['output_kind'].to_numpy()

cohort_ids = validation['cohort_id'].to_numpy()

output_cohort_ids = outputs['cohort_id'].to_numpy()

import numpy as np

count_errors = np.sum

# Supplied evaluation scaffold. Preserve the scaffold outside the requested TODO expressions.
if __name__:
    def deployment_weighted_cost(p_negative, FPR, cost_FP, p_positive, FNR, cost_FN):
        return p_negative * FPR * cost_FP + p_positive * FNR * cost_FN

    def quantities(y, predictions, p_negative, p_positive, cost_FP, cost_FN):
        FP = conditional_count((y == 0) & (predictions == 1))
        TN = conditional_count((y == 0) & (predictions == 0))
        FN = conditional_count((y == 1) & (predictions == 0))
        TP = conditional_count((y == 1) & (predictions == 1))
        negative_count = FP + TN
        positive_count = FN + TP
        FPR = None
        FNR = None
        expected_cost = None
        if negative_count > 0:
            FPR = FP / negative_count
        if positive_count > 0:
            FNR = FN / positive_count
        if negative_count > 0:
            if positive_count > 0:
                expected_cost = p_negative * FPR * cost_FP + p_positive * FNR * cost_FN
        return {'FP': FP, 'TN': TN, 'FN': FN, 'TP': TP, 'actual_negative_count': negative_count, 'actual_positive_count': positive_count, 'FPR': FPR, 'FNR': FNR, 'expected_cost': expected_cost, 'accuracy': conditional_count(y == predictions) / y.shape[0]}

    def evaluate(ids, output_ids, y, outputs_y, reference, output_kind, p_negative, p_positive, cost_FP, cost_FN, bound, cohort_ids, output_cohort_ids):
        if not np.array_equal(cohort_ids, output_cohort_ids):
            return {'aligned': False, 'accepted': False, 'reason': 'unmatched cohorts'}
        if ids.shape != y.shape or cohort_ids.shape != y.shape or output_ids.shape != outputs_y.shape or (output_cohort_ids.shape != outputs_y.shape) or (output_kind.shape != outputs_y.shape):
            return {'aligned': False, 'accepted': False, 'reason': 'unmatched observations'}
        if not np.array_equal(ids, output_ids):
            return {'aligned': False, 'accepted': False, 'reason': 'unmatched observations'}
        if y.shape != outputs_y.shape or y.shape != reference.shape:
            return {'aligned': False, 'accepted': False, 'reason': 'unmatched observations'}
        if conditional_count(output_kind != 'foundation-model') > 0:
            return {'aligned': False, 'accepted': False, 'reason': 'candidate is not the supplied foundation-model output kind'}
        candidate = quantities(y, outputs_y, p_negative, p_positive, cost_FP, cost_FN)
        baseline = quantities(y, reference, p_negative, p_positive, cost_FP, cost_FN)
        accepted = False
        if candidate['expected_cost'] is not None:
            if candidate['expected_cost'] <= bound:
                accepted = True
        return {'aligned': True, 'candidate': candidate, 'baseline': baseline, 'accepted': accepted, 'bound': bound, 'limitations': 'Quality verdict is bounded to supplied order-task validation observations; no application construction, fitting or protected-test evidence is implied.'}

# Supplied callable operations; keep these assignments unchanged.
supplied_np_sum = np.sum
supplied_np_array_equal = np.array_equal
conditional_count = supplied_np_sum

# Complete only the final operation binding.
alignment_check = supplied_np_array_equal

  test t1 (value_equals, visible=True): {"expr":"evaluate(ids, output_ids, y, outputs_y, reference, output_kind, p_negative, p_positive, cost_FP, cost_FN, bound, cohort_ids, output_cohort_ids)","expected":{"aligned":true,"candidate":{"FP":8,"TN":72,"FN":4,"TP":16,"actual_negative_count":80,"actual_positive_count":20,"FPR":0.1,"FNR":0.2,"expected_cost":0.28,"accuracy":0.88},"baseline":{"FP":0,"TN":80,"FN":20,"TP":0,"actual_negative_count":80,"actual_positive_count":20,"FPR":0,"FNR":1,"expected_cost":1,"accuracy":0.8},"accepted":true,"b | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  test t2 (value_equals, visible=False): {"expr":"(evaluate(ids, output_ids, y, outputs_y, reference, output_kind, p_negative, p_positive, cost_FP, cost_FN, bound, cohort_ids, output_cohort_ids), evaluate(ids, output_ids[::-1], y, outputs_y, reference, output_kind, p_negative, p_positive, cost_FP, cost_FN, bound, cohort_ids, output_cohort_ids))","expected":[{"aligned":true,"candidate":{"FP":8,"TN":72,"FN":4,"TP":16,"actual_negative_count":80,"actual_positive_count":20,"FPR":0.1,"FNR":0.2,"expected_cost":0.28,"accuracy":0.88},"baseline" | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  test t3 (value_equals, visible=False): {"expr":"evaluate(ids[y == 0], output_ids[y == 0], y[y == 0], outputs_y[y == 0], reference[y == 0], output_kind[y == 0], p_negative, p_positive, cost_FP, cost_FN, bound, cohort_ids[y == 0], output_cohort_ids[y == 0])","expected":{"aligned":true,"candidate":{"FP":8,"TN":72,"FN":0,"TP":0,"actual_negative_count":80,"actual_positive_count":0,"FPR":0.1,"FNR":null,"expected_cost":null,"accuracy":0.9},"baseline":{"FP":0,"TN":80,"FN":0,"TP":0,"actual_negative_count":80,"actual_positive_count":0,"FPR":0, | on-fail: Check the named result fields, fixed assumptions, and empty-group behavior.
  test wrong_cohort (value_equals, visible=False): {"expr":"(evaluate(ids, output_ids, y, outputs_y, reference, output_kind, p_negative, p_positive, cost_FP, cost_FN, bound, cohort_ids, output_cohort_ids), evaluate(ids, output_ids, y, outputs_y, reference, output_kind, p_negative, p_positive, cost_FP, cost_FN, bound, cohort_ids, np.asarray([\"wrong_cohort\"] * len(output_cohort_ids))))","expected":[{"aligned":true,"candidate":{"FP":8,"TN":72,"FN":4,"TP":16,"actual_negative_count":80,"actual_positive_count":20,"FPR":0.1,"FNR":0.2,"expected_cost": | on-fail: Matching observation ids alone do not establish a matched cohort.
  provenance: {"runtime":"pyodide","runtime_version":"0.29.5","solution_sha256":"125117bfb55ea62086ade8178c969cd6ff0b66280a099b4f91474c9a32281a57","tests_passed":4}
  feedback✔: Your result follows the fixed evidence and the declared conditioning populations.  feedback✘: Recheck which observations belong in each denominator and keep the declared decision inputs fixed.  hints: ['Inspect the supplied callable assignments immediately above the final TODO.', 'Change only the final binding; keep the evaluation scaffold and its fixed evidence guards unchanged.']  remediation→r02
  MEASURES: A:verify_matched_validation_cohort_and_acceptance_requirements(f1); A:issue_bounded_quality_verdict_against_validation_baseline(f2); A:calculate_class_conditional_error_rates_with_empty_group_handling(f3); A:calculate_expected_error_cost_from_supplied_deployment_assumptions(f4); A:preserve_protected_test_boundary_during_supplied_output_evaluation(f5)   anchors=['practice', 'assessment:verify_matched_validation_cohort_and_acceptance_requirements', 'assessment:issue_bounded_quality_verdict_against_validation_baseline', 'assessment:calculate_class_conditional_error_rates_with_empty_group_handling', 'assessment:calculate_expected_error_cost_from_supplied_deployment_assumptions', 'assessment:preserve_protected_test_boundary_during_supplied_output_evaluation']
  taught-before-tested: A.f1←s01; A.f2←s01; A.f3←s01; A.f4←s01; A.f5←s01

### s06 · recap · Keep these distinctions
(takeaway) Align supplied outputs, labeled validation observations and reference outputs. Apply the same fixed acceptance and cost requirements. Mark empty-group rates undefined and report cohort-bounded limitations. Supplied-output evaluation is not application construction or training; protected-test observations stay outside fitting and selection. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb1 A:tb2 A:tb3 A:tb4 A:tb5⟧
[UP NEXT] Up next: Construct PyTorch input tensors with compatible shapes and dtypes.

## REMEDIATION STEPS (shown only after a wrong answer)
### r01 · Revisit: the check — evaluate supplied outputs
(misconception) Contrast matched supplied-output evaluation with application construction. The verdict is bounded to aligned labeled validation observations and fixed requirements. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
(mechanism) Use the same task-specific labeled validation examples and acceptance requirements as the reference. Compare supplied-output quality with the validation baseline and report observed limitations; this is not application construction or training. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose models or tune settings without leaking information. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.foundation_outputs cols=['observation_id', 'cohort_id', 'output_kind', 'foundation_output'] ] caption: Supplied foundation output file aligned to validation
### r02 · Revisit: the practice — evaluate supplied outputs
(misconception) Contrast matched supplied-output evaluation with application construction. The verdict is bounded to aligned labeled validation observations and fixed requirements. ⟦A.f1 A.f2 A.f3 A.f4 A.f5 A:tb2 A:tb3⟧
(mechanism) Use the same task-specific labeled validation examples and acceptance requirements as the reference. Compare supplied-output quality with the validation baseline and report observed limitations; this is not application construction or training. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined. ⟦A.f1 A.f2 A.f3 A:tb2⟧
(mechanism) With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose models or tune settings without leaking information. ⟦A.f4 A.f5 A:tb3⟧
[TABLE ds.foundation_outputs cols=['observation_id', 'cohort_id', 'output_kind', 'foundation_output'] ] caption: Supplied foundation output file aligned to validation

## OTHER CONTENT (fields without a dedicated renderer)
· constraints.blocked_syntax: torch.utils.data.DataLoader(...)
· constraints.blocked_syntax: torch.nn.Linear(...)
· constraints.blocked_syntax: torch.nn.BCEWithLogitsLoss(...)
· constraints.blocked_syntax: torch.optim.Adam(...)
· spec.expr: (evaluate(ids, output_ids, y, outputs_y, reference, output_kind, p_negative, p_positive, cost_FP, cost_FN, bound, cohort_ids, output_cohort_ids), evaluate(ids, output_ids, y, outputs_y, reference, output_kind, p_negative, p_positive, cost_FP, cost_FN, bound, cohort_ids, np.asarray(["wrong_cohort"] * len(output_cohort_ids))))