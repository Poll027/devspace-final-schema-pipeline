import json,copy,re
from pathlib import Path
B=Path(__file__).parent
P=json.loads((B/'tile_plans.json').read_text()); G=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); R=json.loads((B/'scenario_asset_registry.json').read_text())
C={x['context']['concept_id']:x for x in G['bundles']}; A={a['asset_id']:a for a in R['assets']}
# Each entry revoices one source teaching block. Numeric results remain in referenced assets.
TEXT={
 'task_metric_selection':[
 'Few total late-order mistakes can still hide missed positives. Choose the metric for the task’s error consequences and conditioning population, not accuracy alone.',
 'Class balance and false-positive/false-negative costs matter when choosing classification metrics. Precision, TP/(TP+FP), asks how many predicted positives are actual positives. Recall, TP/(TP+FN), asks how many actual positives were detected. For regression, MAE averages absolute errors; MSE averages squared errors, giving larger errors more influence.',
 'Validation prevalence is actual positives divided by the validation population. Use it to interpret cohort metrics. Confusion-table conditional frequencies describe this cohort; they do not demonstrate calibration of individual probability scores.',
 'Read the confusion cells with their actual and predicted labels. Precision uses predicted positives as its denominator; recall uses actual positives. Prevalence uses the whole validation cohort. The separate regression tables show absolute and squared errors and their averages. Keep task consequences beside the numbers: these cohort summaries do not prove that an individual probability score is calibrated.',
 'Precision and recall use different denominators. Neither replaces the other, and cohort frequencies do not prove probability-score calibration.'
 ],
 'model_acceptance_criteria':[
 'Declare quality and operating requirements before inspecting candidate results. The favored candidate must not determine the acceptance contract.',
 'Precommit a measurable predictive-quality requirement and the supplied deployment compatibility requirements. Keep supplied error costs and deployment class probabilities fixed. FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. A rate with an empty conditioning group is undefined.',
 'With zero cost for correct predictions, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Require expected cost <= the predeclared bound. Operating limits are separate eligibility conditions.',
 'The cost-term table keeps the actual-class conditioning counts, supplied deployment probabilities and error costs separate. Add the weighted contributions and compare with the fixed bound in the acceptance contract. Passing that predictive requirement does not override a latency limit. An empty actual-positive group leaves FNR undefined; do not substitute zero or change deployment probabilities to favor a candidate.',
 'Low cost is not blanket acceptance. Keep predictive and operating eligibility separate, and do not change supplied probabilities or costs to favor a candidate.'
 ],
 'reference_baseline':[
 'Establish a simple reference before judging more elaborate predictions. Fit it on training observations and evaluate its frozen predictions on validation.',
 'DummyClassifier offers reference rules such as most_frequent, prior and constant. DummyRegressor(strategy="mean") predicts the training-target mean. Fit on training inputs and targets, freeze the estimator, then predict on separate validation observations. Report the predeclared metric against validation targets, not a training-only result.',
 'Use np.mean(numeric_values) for the selected numeric observations’ arithmetic mean. np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root; use ddof=1 only when an N−1 divisor is required. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty conditioning groups give undefined rates.',
 'With correct predictions costing zero, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations must not fit preprocessing, choose a model or tune settings: that leaks information. For a classification reference, report training target-class count/training total, not validation or protected-test prevalence.',
 'The registered training labels determine the reference rule and training class proportions. Keep those statistics separate from validation prevalence. Freeze the fitted reference before predicting on the corresponding validation inputs. Evaluate those predictions with the declared metric and cost assumptions; retain actual-class denominators and mark empty groups undefined. Training-target mean and spread describe the chosen training observations, not the held-out result.',
 'A reference still needs held-out evaluation. Training proportions are not validation prevalence, and fitting or selecting with protected-test observations leaks information.'
 ],
 'model_approach_decision':[
 'Use supplied matched records to justify an approach choice. Predictive quality, deployment fit and operating evidence all matter before promotion.',
 'Compare alternatives on the same intended task and cohort. Check quality and deployment compatibility. Inference options differ in latency, scale and cost; supplied constraints govern eligibility. Reject records failing precommitted quality or operating limits, then apply the fixed decision rule among eligible alternatives.',
 'FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Do not use protected-test observations to fit preprocessing, choose models or tune settings: that leaks information.',
 'Custom classical or neural models leave task-model implementation and training choices with the model owner. A managed service can supply training/hosting infrastructure. Compare maintenance responsibility alongside predictive and operating evidence. Address classical/neural and custom/managed trade-offs from matched records, without fitting new alternatives to manufacture evidence.',
 'The approach records keep model family, delivery mode, cohort, confusion counts and operating checks together. Use the same supplied deployment probabilities and costs for every row. Exclude an alternative that fails a fixed requirement before applying the selection rule. A lower cost cannot erase an operating failure; maintenance responsibility remains part of the comparison.',
 'Choose only among eligible matched records. A favorable predictive number cannot excuse a failed operating requirement or replace maintenance evidence.'
 ],
 'sklearn_baseline_workflow':[
 'Connect aligned numeric training data to a bounded LogisticRegression baseline, then inspect its held-out predictions under the declared evaluation.',
 'Use from sklearn.linear_model import LogisticRegression, create estimator = LogisticRegression(random_state=0), and call estimator.fit(X_train, y_train). Numeric X_train has shape (n_samples, n_features); aligned class labels y_train have shape (n_samples,). Compare estimator.predict(X_validation) with corresponding y_validation. If fitting used preprocessing, predict through the fitted pipeline to preserve the feature representation.',
 'FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) on actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.',
 'The training and validation tables expose observation identities, numeric features and aligned labels. Fitting establishes estimator state; prediction applies it to validation inputs; evaluation compares outputs with matching held-out labels. Shape agreement alone does not establish observation correspondence. Use the fitted pipeline when preprocessing belongs to it. Inspect conditional error counts and the fixed cost calculation rather than stopping when fit returns.',
 'predict is not a quality verdict. Use matching held-out labels and the fixed evaluation rule; bypassing fitted preprocessing changes the representation.'
 ],
 'decision_threshold_selection':[
 'The same scores can yield different class decisions. Make the threshold explicit, evaluate supplied candidates on validation, and freeze the chosen rule.',
 'A score is not a class decision: comparing it with a threshold produces the decision. Binary scikit-learn probability scores ordinarily use a 0.5 cutoff; decision_function scores use zero. An explicit task threshold changes the decision. For each supplied threshold, form labels and count TP, FP, TN and FN against validation labels.',
 'Choose the eligible threshold minimizing predeclared validation expected cost, then freeze it before protected testing. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups yield undefined rates. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.',
 'Using protected-test observations to fit preprocessing, choose a model or tune settings leaks information into the selected system. Keep them outside those choices.',
 'Compare supplied thresholds against the same scores and labels. A score between two thresholds changes class decision without changing score. Recount errors at each threshold, apply the fixed costs and eligibility limits, then retain the minimum-cost eligible rule. The ordinary probability and decision_function cutoffs belong to different score representations; do not treat them as interchangeable.',
 'A threshold changes the decision, not the score. Choose with fixed validation evidence and freeze it before protected testing; do not tune on protected-test results.'
 ],
 'validation_candidate_comparison':[
 'Start with comparable records and eligibility, not the smallest displayed number. Baseline and candidates must answer the same evaluation question.',
 'Compare baseline and candidates on the same evaluation dataset and predeclared requirements. Compute each cost using identical supplied deployment probabilities and error costs. Exclude records failing fixed limits; rank eligible records by the declared cost rule. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups give undefined rates.',
 'With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose a model or tune settings without leaking information.',
 'Inspect cohort identity before comparing baseline and candidate costs. A lower number from a different cohort is not matched selection evidence. For matching records, retain confusion counts, conditioning totals and the fixed cost contract. Check quality and operating limits before ranking; do not change deployment probabilities after seeing which candidate benefits. Protected-test observations stay outside fitting and selection.',
 'The smallest number need not be the eligible winner. Matched cohorts and fixed requirements are prerequisites, not checks to postpone until after selection.'
 ],
 'prediction_error_analysis':[
 'Investigate the predefined failure group rather than treating personally tried cases as representative of users. Keep its eligible population explicit.',
 'Inspect prediction failures; developer usage does not necessarily represent users. For the predefined group, divide errors by eligible observations. Compare its quality evidence with the same-cohort reference to localize observed failure; an overall score does not describe every segment.',
 'Summarize selected numeric observations with np.mean(numeric_values). Use np.std(numeric_values, ddof=0): squared deviations are divided by N before the square root. Use ddof=1 only when the specified calculation requires N−1.',
 'The supplied observations identify eligibility and long-distance membership alongside model and reference errors and loss. Keep that group boundary when counting errors and eligible observations. Compare with the group’s same-cohort reference, not unrelated traffic. Selected loss mean and spread describe the measured observations; they do not establish a cause of failure or make developer-chosen examples representative of users.',
 'An overall score does not describe every segment. An error count without the eligible count hides the conditional proportion.'
 ],
 'slice_evaluation':[
 'Evaluate predefined delivery zones separately even when the aggregate improves. Keep each slice’s observation count beside its quality result.',
 'Overall improvement can coexist with uneven segment performance. For each predefined slice, report eligible count and errors/eligible count. Retain that conditioning population. Samples may not represent their intended population, so sample slice differences alone do not establish population-level disparity.',
 'Use np.mean(numeric_values) for selected observations’ mean. np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root; use ddof=1 only when the calculation requires N−1.',
 'Read each zone’s eligible count, errors and conditional error probability together. The loss summaries retain their own selected observations and standard-deviation divisor. Compare slice evidence with the matched overall record without letting one replace the other. Unequal observed sample results support a bounded description of these slices, not an unmeasured population conclusion.',
 'Aggregate improvement can coexist with uneven slices. An observed sample difference alone does not prove disparity throughout the intended population.'
 ],
 'subgroup_risk_mitigation':[
 'Before accepting a supplied mitigation, inspect group representation and both subgroup and overall validation evidence. Do not assume the model alone explains the problem.',
 'Check whether data represents intended groups before attributing a subgroup problem solely to the model. Evaluate the supplied mitigation on the affected validation segment and overall cohort. A subgroup’s contribution to total expected harm is its deployment population probability × subgroup-conditional expected harm, using supplied error costs.',
 'FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. An empty conditioning group leaves its rate undefined.',
 'Keep subgroup-conditional harm distinct from its population-weighted contribution. The registered records show reference and mitigation evidence for both affected segment and overall cohort. Apply the supplied deployment subgroup probability, not the validation subgroup prevalence, to weight conditional harm. Inspect representation and the overall result before acceptance; a subgroup improvement alone is insufficient.',
 'A subgroup-only improvement is insufficient. Population probability, conditional harm and representation are distinct; empty conditioning groups do not supply defined rates.'
 ],
 'experiment_metric_logging':[
 'A keyed run connects resolved parameters, validation results, code identity and a diagnostic artifact. A printed metric alone does not retain that connection.',
 'Use import mlflow and with mlflow.start_run() as run; retain run_id as the tracking key. Log resolved configuration with mlflow.log_params(params), validation results with mlflow.log_metric(name, value), and the diagnostic file with mlflow.log_artifact(local_path). Inspect git rev-parse --verify HEAD before recording code identity.',
 'Retrieve recorded = mlflow.get_run(run_id); inspect recorded.data.params, recorded.data.metrics and recorded.info.artifact_uri. For repeated metric logging, RunData gives the most recently logged value at the largest step, not the full history. Define function defaults, accept keyword overrides, and log resolved values. Use os.getcwd() and os.chdir(recorded_directory) when resolving repository/artifact paths; retain the resolved path in lookup.',
 'Use subprocess.run in the intended working directory with captured output to inspect git rev-parse --verify HEAD. Reject a revision mismatch before claiming the keyed artifact belongs to that run.',
 'An explicit keyword override replaces the default value in the resolved configuration to log. Retain the run key and resolved local artifact path, inspect repository identity in the intended directory, then retrieve the keyed run. Compare its parameters, metrics and artifact URI with the intended record. Interpret repeated metrics as the latest value at the largest step, not a history. A revision mismatch or wrongly resolved path prevents the artifact-ownership claim.',
 'A run name or printed metric is not a verified keyed record. Retrieved parameters, actual revision, resolved overrides and artifact path must agree.'
 ],
 'training_randomness':[
 'Control supplied random sources and retain paired trial results. This supports the declared repeated comparison, not universal determinism.',
 'Integer random_state values reset supported scikit-learn generators for repeatable calls; None and shared RandomState instances consume state differently. Control estimator and split randomness without promising every computation or environment is deterministic. Loop over the declared seeds and collect each matched baseline/candidate validation pair.',
 'Empirical win probability is winning paired trials/all completed paired trials; retain the trial count. Summarize selected numeric results with np.mean(numeric_values) and np.std(numeric_values, ddof=0). The latter divides squared deviations by N before the square root; use ddof=1 only if N−1 is required.',
 'Keep each seed with its baseline and candidate results, then judge wins using the declared metric direction and tie policy. Separate averages lose pairing, so calculate wins pair by pair and retain the completed-pair denominator. An incomplete trial is not a win. Mean and spread describe the selected results under the specified divisor. Controlling estimator and split sources does not establish determinism in every environment.',
 'Controlled seeds do not guarantee universal determinism. Empirical wins describe completed paired trials, not certainty that the candidate always wins.'
 ],
 'validation_regularization':[
 'Good training results with worse validation results under the same score interpretation provide overfitting evidence. Investigate declared regularization settings under the fixed validation protocol.',
 'A good-training/poor-validation gap is evidence of overfitting. Compare declared settings under the same scoring interpretation and select by the predeclared validation criterion, not training score alone. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.',
 'Protected-test observations must not fit preprocessing, choose models or tune settings: that leaks information. Regularization penalizes complexity during fitting. Larger Ridge alpha increases the penalty; LogisticRegression C is inverse regularization strength, so larger C weakens regularization.',
 'Read training and validation cost under the same interpretation. A setting with worse training cost can still be the eligible minimum-validation-cost choice. Retain matched cohort, supplied probabilities and error costs. Identify the estimator before interpreting parameter direction: Ridge alpha and LogisticRegression C run in opposite strength directions. The gap supports investigation, not a claim that every validation weakness has the same cause.',
 'Best training cost need not mean best validation choice. Parameter direction is estimator-specific: larger LogisticRegression C weakens regularization.'
 ],
 'bounded_hyperparameter_search':[
 'Resolve a trial budget and scoring protocol before search. Candidate settings alone do not define a stopping boundary.',
 'GridSearchCV enumerates param_grid combinations; RandomizedSearchCV samples configurations bounded by n_iter. Predeclare scoring and evaluation protocol, then inspect validation-selected best_params_ and cv_results_. In a supplied manual search, iterate bounded configuration dictionaries, execute declared trials and record validation results without exceeding the fixed budget.',
 'FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) on actual positives. Empty groups make rates undefined. With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose models or tune settings without leaking information.',
 'Define a default budget parameter and accept explicit keyword overrides. Resolve the budget before iterating the configuration dictionary/list.',
 'The execution contract distinguishes default and overridden budgets. Resolve the override before trials, then retain only completed configurations and their validation results. A supplied third response is not a completed trial when the budget stops earlier. Keep scoring, actual-class denominators, deployment probabilities and costs fixed. Inspect selected parameters and trial results under the declared protocol; protected-test results are not search evidence.',
 'An overridden budget, not the default, governs execution. Validation-selected settings do not authorize protected-test inspection or continued searching to improve that result.'
 ],
 'model_risk_documentation':[
 'Build one bounded risk record from existing policy and supplied evidence. Documentation must not expand permissions or reproduce exposed secrets.',
 'Compare observed grants with existing permitted identities and record out-of-scope grants rather than defining a new policy. Literal credentials in images or metadata are exposure risks: describe the handling limitation without copying the secret. Aggregate improvement can coexist with segment differences; state supported evaluation limitations, not universal suitability.',
 'Preserve existing policy fields, permitted identities, documented task limits and foreseeable misuse cases in the single record. Do not extend permission scope.',
 'Place existing policy beside supplied observations. An observed identity outside the permitted set is a mismatch to record, not a reason to enlarge that set. Describe the redacted credential-exposure location without copying a value. Carry documented task limits, foreseeable misuse and supported aggregate/segment evidence into one record. Keep permission language separate from measured limitations.',
 'Documentation is not authorization. Do not enlarge identity scope, claim universal suitability or disclose the credential being flagged.'
 ],
 'foundation_model_baseline_evaluation':[
 'Evaluate supplied foundation-model outputs for the order task. The bounded target is matched validation evidence, not application construction or model training.',
 'Use the same task-specific labeled validation examples and acceptance requirements as the reference. Compare supplied-output quality with the validation baseline and report observed limitations; this is not application construction or training. FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined.',
 'With zero correct-prediction cost, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN. Protected-test observations cannot fit preprocessing, choose models or tune settings without leaking information.',
 'Align each supplied output to its labeled validation observation and reference output. A different cohort would not support a matched comparison. Use fixed acceptance requirements, deployment probabilities and error costs, retaining actual-class denominators. Report what these supplied task outputs support and their observed limitations; do not generalize to every foundation model or application. Keep protected-test observations outside fitting and setting choice.',
 'Supplied-output evaluation does not demonstrate application-building or model-training competence. Its conclusion stays task-specific and validation-based.'
 ]}
TITLES={
 'task_metric_selection':['Choose the question','Precision, recall and regression loss','Cohort evidence is bounded','Read the denominators','Do not swap the groups'],
 'model_acceptance_criteria':['Precommit acceptance','Keep the inputs fixed','Cost and eligibility','Inspect the acceptance contract','Cost is not blanket acceptance'],
 'reference_baseline':['Start with a reference','Fit, freeze, evaluate','Statistics and conditioning','Keep training and test boundaries','Inspect the frozen reference','A reference needs validation'],
 'model_approach_decision':['Matched approach evidence','Eligibility before choice','Conditioned deployment cost','Who owns the work?','Review the alternatives','Exclude before ranking'],
 'sklearn_baseline_workflow':['A bounded fitted baseline','Aligned fit and prediction','Evaluate conditional errors','Inspect the held-out path','Prediction is not a verdict'],
 'decision_threshold_selection':['Score versus decision','Thresholds depend on representation','Choose and freeze','Protect the test boundary','Compare threshold records','Do not change the score story'],
 'validation_candidate_comparison':['Compare like with like','Filter then rank','Fixed cost and test boundaries','Inspect cohort identity','Smallest is not necessarily eligible'],
 'prediction_error_analysis':['Locate observed failures','Retain the group denominator','Summarize selected observations','Inspect long-distance evidence','Counts need denominators'],
 'slice_evaluation':['Separate the slices','Bound the sample conclusion','Mean and spread','Inspect zone evidence','Uneven does not prove population disparity'],
 'subgroup_risk_mitigation':['Check representation first','Conditional harm versus contribution','Keep actual-class groups separate','Inspect segment and overall evidence','Subgroup-only is insufficient'],
 'experiment_metric_logging':['Keep a keyed record','Start and log the run','Retrieve resolved evidence','Reject revision mismatch','Verify the intended record','A name is not a verified key'],
 'training_randomness':['Control and pair trials','State consumption matters','Wins, mean and spread','Retain each completed pair','Seeds do not promise certainty'],
 'validation_regularization':['Investigate the train–validation gap','Select by validation','Estimator-specific strength','Inspect setting evidence','Training alone cannot choose'],
 'bounded_hyperparameter_search':['Resolve the stopping boundary','Declare the search protocol','Keep costs and boundaries fixed','Resolve keyword overrides','Inspect completed trials','An override replaces the default'],
 'model_risk_documentation':['One bounded risk record','Policy, exposure and limitations','Preserve existing scope','Map evidence into the record','Documentation is not permission'],
 'foundation_model_baseline_evaluation':['Evaluate supplied outputs','Matched task evidence','Cost and protected boundaries','Check alignment before scoring','Evaluation is not construction']}

def lin(cid,tbs=None,facts=None,visual=False):
 out={'concept_ids':[cid],'teaching_block_ids':tbs or [],'fact_ids':facts or []}
 if visual:out['anchors']=[cid+'#visual']
 return out

def prose(cid,tb):
 n=int(tb['id'][2:])-1
 return {'type':'prose','text':TEXT[cid.split('.')[-1]][n],'role':tb['purpose'] if tb['purpose'] in ['intro','definition','mechanism','example','misconception'] else 'mechanism','lineage':lin(cid,[cid+'#'+tb['id']],[cid+'#'+f for f in tb['fact_ids']])}

def table(cid,aid,cols=None,caption=None,visual=True):
 asset=A[aid]; cols=cols or [c['name'] for c in asset['columns']]
 assert set(cols)<=set(c['name'] for c in asset['columns'])
 return {'type':'data_table','asset_ref':{'asset_id':aid,'columns':cols},'caption':caption or asset['title'],'lineage':lin(cid,visual=visual)}

def letter(n):
 s=''
 while n:n,k=divmod(n-1,26);s=chr(65+k)+s
 return s

def grid(cid,aid,cols=None):
 a=A[aid]; cols=cols or [c['name'] for c in a['columns']]
 return {'type':'spreadsheet_grid','asset_ref':{'asset_id':aid,'columns':cols},'range':f'A1:{letter(len(cols))}{len(a["rows"])+1}','show_formula_bar':True,'lineage':lin(cid,visual=True)}

DATA={
 'task_metric_selection':['ds.confusion_counts','ds.metric_summary','ds.regression_errors','ds.regression_error_summary'],
 'model_acceptance_criteria':['ds.acceptance_terms','ds.acceptance_contract'],
 'reference_baseline':['ds.reference_train','ds.regression_targets','ds.acceptance_contract'],
 'model_approach_decision':['ds.approach_records','ds.acceptance_contract'],
 'sklearn_baseline_workflow':['ds.orders_train','ds.orders_validation','ds.acceptance_contract'],
 'decision_threshold_selection':['ds.threshold_records','ds.acceptance_contract'],
 'validation_candidate_comparison':['ds.candidate_records','ds.acceptance_contract'],
 'prediction_error_analysis':['ds.slice_observations','ds.slice_summary'],
 'slice_evaluation':['ds.slice_summary','ds.aggregate_slice_evidence'],
 'subgroup_risk_mitigation':['ds.mitigation_records','ds.acceptance_contract'],
 'experiment_metric_logging':['ds.execution_contract'],
 'training_randomness':['ds.paired_trials','ds.execution_contract'],
 'validation_regularization':['ds.regularization_records','ds.regularization_directions','ds.acceptance_contract'],
 'bounded_hyperparameter_search':['ds.search_trials','ds.execution_contract','ds.acceptance_contract'],
 'model_risk_documentation':['ds.risk_policy_evidence','ds.access_grants','ds.aggregate_slice_evidence','ds.slice_summary'],
 'foundation_model_baseline_evaluation':['ds.foundation_outputs','ds.validation_scores','ds.acceptance_contract']}
# Code is an inspectable workflow; no computed output is authored here.
CODES={
 'reference_baseline':'''import numpy as np
from sklearn.dummy import DummyClassifier, DummyRegressor

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
                 if FPR is not None and FNR is not None else None)''',
 'sklearn_baseline_workflow':'''import numpy as np
from sklearn.linear_model import LogisticRegression

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
                 if FPR is not None and FNR is not None else None)''',
 'experiment_metric_logging':'''import os
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
            "resolved_path": resolved_path}'''
}
# Present the two fitted workflows as bounded functions with inspectable returned evidence.
for key in ['reference_baseline','sklearn_baseline_workflow']:
 lines=CODES[key].splitlines()
 imports=[]
 while lines and (lines[0].startswith('import ') or lines[0].startswith('from ') or not lines[0]):
  line=lines.pop(0)
  if line:imports.append(line)
 params='X_train, y_train, X_validation, y_validation, p_negative, p_positive, cost_FP, cost_FN'
 if key=='reference_baseline':params+=', numeric_values'
 func='evaluate_reference' if key=='reference_baseline' else 'evaluate_baseline'
 returned={
  'training_shape':'X_train.shape','training_label_shape':'y_train.shape',
  'validation_shape':'X_validation.shape','predictions':'predictions',
  'validation_labels':'y_validation','FP':'FP','TN':'TN','FN':'FN','TP':'TP',
  'actual_negative_denominator':'FP + TN','actual_positive_denominator':'FN + TP',
  'FPR':'FPR','FNR':'FNR','expected_cost':'expected_cost'}
 if key=='reference_baseline':returned.update(training_positive_proportion='training_positive_proportion',training_target_mean='training_target_mean',training_target_std_ddof0='training_target_std')
 lines+=['return {']+['    '+repr(k)+': '+v+',' for k,v in returned.items()]+['}']
 CODES[key]='\n'.join(imports)+'\n\ndef '+func+'('+params+'):\n'+'\n'.join('    '+l for l in lines)

# Obtain the default directly from the registered execution contract.
contract=A['ds.execution_contract']; contract_row=dict(zip([c['name'] for c in contract['columns']],contract['rows'][0]))
CODES['experiment_metric_logging']=CODES['experiment_metric_logging'].replace('trial_setting=10','trial_setting='+str(contract_row['default_trial_setting']))

def visuals(cid,typ):
 key=cid.split('.')[-1]; ids=DATA[key]; out=[]
 if typ=='code_walkthrough':
  out.append({'type':'code_walkthrough','language':'python','code':CODES[key],'lineage':lin(cid,visual=True),'reveal':'line_by_line'})
 elif typ=='spreadsheet_grid':out.append(grid(cid,ids[0]))
 elif typ=='side_by_side':
  cols=['configuration_id','estimator','parameter_name','parameter_value','strength_direction','training_expected_error_cost','expected_error_cost','operating_requirements_met']
  out.append({'type':'side_by_side','left':table(cid,ids[0],cols),'right':table(cid,ids[1]),'left_label':'Matched training and validation costs','right_label':'Estimator-specific strength directions','takeaway':'Select by the fixed validation criterion, not training cost alone.','lineage':lin(cid,visual=True)})
 else:
  for aid in ids:
   cols=None
   if key=='task_metric_selection' and aid=='ds.metric_summary':cols=['actual_positive_count','cohort_count','precision','recall','validation_prevalence']
   if key=='prediction_error_analysis' and aid=='ds.slice_observations':cols=['observation_id','cohort_id','eligible','long_distance','error','loss','reference_error','reference_loss']
   out.append(table(cid,aid,cols))
  return out
 for aid in ids[1:] if typ in ['spreadsheet_grid','side_by_side'] else ids:
  if typ=='side_by_side' and aid==ids[1]:continue
  out.append(table(cid,aid))
 return out


def query(cid,sql,mounts,caption):
 return {'type':'data_table','result_of':{'runtime':'sql','sql':sql,'asset_mounts':[{'asset_id':aid,'mount_path':name} for aid,name in mounts]},'caption':caption,'lineage':lin(cid,visual=True)}

base_visuals=visuals
def visuals(cid,typ):
 out=base_visuals(cid,typ); key=cid.split('.')[-1]
 if key=='task_metric_selection':
  counts=A['ds.confusion_counts']; rows=[dict(zip([c['name'] for c in counts['columns']],r)) for r in counts['rows']]
  pred=sum(r['count'] for r in rows if r['predicted_label']==1)
  actual=sum(r['count'] for r in rows if r['actual_label']==1)
  total=sum(r['count'] for r in rows)
  out[0]['caption']=f"Late-order confusion cells: predicted-positive denominator {pred}; actual-positive denominator {actual}; cohort denominator {total}."
 if key=='model_acceptance_criteria':
  out.append(query(cid,"SELECT SUM(t.weighted_contribution) AS expected_cost, c.expected_cost_bound, SUM(t.weighted_contribution) <= c.expected_cost_bound AS predictive_bound_met, c.operating_limit AS separate_operating_limit FROM terms t CROSS JOIN contract c GROUP BY c.expected_cost_bound, c.operating_limit", [('ds.acceptance_terms','terms'),('ds.acceptance_contract','contract')], 'Sum the cost terms; operating eligibility remains separate.'))
 if key in ['model_approach_decision','validation_candidate_comparison','validation_regularization','bounded_hyperparameter_search']:
  aid=DATA[key][0]; asset=A[aid]; names=[c['name'] for c in asset['columns']]
  ident='alternative_id' if key=='model_approach_decision' else 'candidate_id' if key=='validation_candidate_comparison' else 'configuration_id'
  cohort=dict(zip(names,asset['rows'][0]))['cohort_id']
  # Cohort identifiers come from data, not hand-authored values.
  cohort_sql="'"+cohort.replace("'","''")+"'"
  ops=[n for n in names if n.endswith('_requirement_met') or n in ['deployment_compatibility_met','operating_requirements_met']]
  operating=' AND '.join('r.'+n+' = TRUE' for n in ops)
  mounts=[(aid,'records'),('ds.acceptance_contract','contract')]
  budget_join=''; budget_filter='';budget_col='';order_col='r.'+ident
  if key=='bounded_hyperparameter_search':
   mounts.append(('ds.execution_contract','execution'))
   budget_join=' CROSS JOIN execution e';budget_filter=' WHERE r.declared_order < e.override_search_budget';budget_col=', e.override_search_budget AS resolved_budget'; order_col='r.declared_order'
   # Show supplied configuration availability, not unexecuted trial outcomes.
   out=[query(cid,'SELECT r.configuration_id, r.configuration_json, e.override_search_budget AS resolved_budget, r.declared_order < e.override_search_budget AS executed FROM records r CROSS JOIN execution e ORDER BY r.declared_order',mounts,'Budget boundary: supplied configurations are not all completed trials.'),table(cid,'ds.execution_contract'),table(cid,'ds.acceptance_contract')]
  sql=f"""WITH rates AS (
SELECT r.*, 1.0*r.FP/NULLIF(r.FP+r.TN,0) AS conditioned_FPR,
1.0*r.FN/NULLIF(r.FN+r.TP,0) AS conditioned_FNR,
c.deployment_negative_probability, c.deployment_positive_probability, c.cost_FP, c.cost_FN,
c.expected_cost_bound, ({operating}) AS operating_met,
r.cohort_id = {cohort_sql} AS matched_cohort, {order_col} AS tie_order {budget_col}
FROM records r CROSS JOIN contract c {budget_join} {budget_filter}
), costs AS (
SELECT *, deployment_negative_probability*conditioned_FPR*cost_FP + deployment_positive_probability*conditioned_FNR*cost_FN AS computed_cost FROM rates
), eligible AS (
SELECT *, CASE WHEN NOT matched_cohort THEN 'different cohort'
WHEN conditioned_FPR IS NULL OR conditioned_FNR IS NULL THEN 'undefined required rate'
WHEN computed_cost > expected_cost_bound THEN 'quality bound failed'
WHEN NOT operating_met THEN 'operating requirement failed'
ELSE 'eligible' END AS eligibility_reason FROM costs
), ranked AS (
SELECT {ident}, ROW_NUMBER() OVER (ORDER BY computed_cost, tie_order) AS eligible_rank
FROM eligible WHERE eligibility_reason = 'eligible'
)
SELECT a.{ident}, a.cohort_id, a.FP+a.TN AS actual_negative_denominator,
a.FN+a.TP AS actual_positive_denominator, a.conditioned_FPR, a.conditioned_FNR,
a.computed_cost, a.expected_cost_bound, a.eligibility_reason,
b.eligible_rank, CASE WHEN b.eligible_rank=1 THEN TRUE ELSE FALSE END AS retained_selection
FROM eligible a LEFT JOIN ranked b ON a.{ident}=b.{ident} ORDER BY a.tie_order"""
  out.append(query(cid,sql,mounts,'Fixed-contract eligibility and retained validation selection; null rates remain undefined.'))
 if key=='training_randomness':
  out.append(query(cid,"SELECT seed, baseline_result, candidate_result, candidate_result < baseline_result AS candidate_win FROM pairs ORDER BY seed", [('ds.paired_trials','pairs')],'Completed matched pairs; ties are not wins.'))
  out.append(query(cid,"SELECT COUNT(*) AS completed_pairs, SUM(CASE WHEN candidate_result < baseline_result THEN 1 ELSE 0 END) AS wins, 1.0*SUM(CASE WHEN candidate_result < baseline_result THEN 1 ELSE 0 END)/COUNT(*) AS empirical_win_probability, AVG(baseline_result) AS baseline_mean, SQRT(AVG(baseline_result*baseline_result)-AVG(baseline_result)*AVG(baseline_result)) AS baseline_std_ddof0, AVG(candidate_result) AS candidate_mean, SQRT(AVG(candidate_result*candidate_result)-AVG(candidate_result)*AVG(candidate_result)) AS candidate_std_ddof0 FROM pairs", [('ds.paired_trials','pairs')],'Selected-result means and N-divisor standard deviations.'))
 if key=='decision_threshold_selection':
  out.append(query(cid,'SELECT v.observation_id, v.score, t.threshold, v.score >= t.threshold AS predicted_positive FROM scores v CROSS JOIN thresholds t WHERE v.score > (SELECT MIN(threshold) FROM thresholds) AND v.score < (SELECT MAX(threshold) FROM thresholds) ORDER BY v.observation_id, t.declared_order',[('ds.validation_scores','scores'),('ds.thresholds','thresholds')],'Same supplied score, different threshold-dependent decisions.'))
 if key=='foundation_model_baseline_evaluation':
  mounts=[('ds.foundation_outputs','outputs'),('ds.validation_scores','labels'),('ds.acceptance_contract','contract')]
  out=[query(cid,'SELECT v.observation_id, v.cohort_id, v.actual_label, f.foundation_output, v.reference_output FROM labels v LEFT JOIN outputs f ON v.observation_id=f.observation_id AND v.cohort_id=f.cohort_id ORDER BY v.observation_id',mounts,'Aligned validation labels, supplied foundation outputs and reference outputs.'),table(cid,'ds.acceptance_contract')]
  out.append(query(cid,"""WITH counts AS (
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
SELECT *, expected_cost <= expected_cost_bound AS predictive_requirement_met FROM costs""",mounts,'Foundation-output counts, conditioning denominators and fixed-contract cost evidence.'))
 return out

CONTRAST={
 'task_metric_selection':'Contrast predicted positives with actual positives: precision starts with the first group, recall with the second. Neither group ratio demonstrates score calibration.',
 'model_acceptance_criteria':'Contrast passing the predictive-cost bound with being deployment-eligible: a separate operating failure still excludes the candidate.',
 'reference_baseline':'Contrast training class proportions with validation prevalence. Fit the reference on training, but judge its frozen predictions with matching validation targets.',
 'model_approach_decision':'Contrast an attractive cost with an eligible approach. Matched task/cohort and every fixed quality/operating requirement come before selection.',
 'sklearn_baseline_workflow':'Contrast predictions with evaluated predictions: matching held-out labels and the fitted representation are needed before a quality verdict.',
 'decision_threshold_selection':'Contrast a fixed score with its threshold-dependent class decision. Recount validation errors for each supplied threshold before freezing a choice.',
 'validation_candidate_comparison':'Contrast the lowest reported cost with the lowest eligible matched cost. A different-cohort record cannot win this comparison.',
 'prediction_error_analysis':'Contrast error count with conditional error proportion. The predefined eligible population supplies the denominator; an overall score does not locate every failure.',
 'slice_evaluation':'Contrast observed slice evidence with a population claim. Counts and sample conditioning support the former, not automatic generalization to the latter.',
 'subgroup_risk_mitigation':'Contrast subgroup-conditional harm with population-weighted contribution. Weight by supplied deployment probability, then inspect representation and overall evidence too.',
 'experiment_metric_logging':'Contrast a default with the resolved keyword override. Log the value actually used, then verify keyed parameters, revision and resolved artifact path.',
 'training_randomness':'Contrast repeatable supported seeded calls with universal determinism. Empirical wins are measured among completed matched pairs, not guaranteed future wins.',
 'validation_regularization':'Contrast training quality with validation selection. Larger Ridge alpha strengthens its penalty; larger LogisticRegression C weakens regularization.',
 'bounded_hyperparameter_search':'Contrast default budget with resolved overridden budget. Only executed trials belong in the completed-result record.',
 'model_risk_documentation':'Contrast an observed grant with a permitted identity. Record a mismatch without expanding policy or copying an exposed secret.',
 'foundation_model_baseline_evaluation':'Contrast matched supplied-output evaluation with application construction. The verdict is bounded to aligned labeled validation observations and fixed requirements.'}
RECAP=[
 'Choose metrics by task consequences and their denominators. Cohort frequencies do not prove score calibration. Precommit quality, costs and deployment probabilities; keep operating eligibility separate and empty-group rates undefined.',
 'Fit a simple reference on training and evaluate frozen validation predictions. Keep training statistics distinct from held-out evidence. Compare approaches on matched task/cohort records and fixed eligibility rules. Preserve aligned features, labels and fitted preprocessing in the LogisticRegression path.',
 'Scores and threshold-dependent decisions differ. Evaluate supplied thresholds on validation and freeze the eligible minimum-cost choice. Compare candidates only on matched cohorts, with fixed cost inputs and requirements. Keep protected-test observations outside fitting and selection.',
 'Retain eligible denominators in failure groups and predefined slices. Compare with same-cohort references; sample differences alone do not establish population disparity. Check representation, subgroup and overall evidence before accepting a mitigation. Distinguish conditional harm from population-weighted contribution.',
 'Verify keyed runs with resolved overrides, repository revision and artifact paths. Control random sources without claiming universal determinism; retain completed paired trials. Select regularization by validation, with estimator-specific parameter direction. Resolve search budgets before trials and keep protected-test observations outside selection.',
 'Preserve existing permitted identities, task limits and foreseeable misuse in one risk record. Record access mismatches without widening policy. Describe credential exposure without copying secrets. State supported aggregate and segment limitations rather than universal suitability.',
 'Align supplied outputs, labeled validation observations and reference outputs. Apply the same fixed acceptance and cost requirements. Mark empty-group rates undefined and report cohort-bounded limitations. Supplied-output evaluation is not application construction or training; protected-test observations stay outside fitting and selection.'
]
NEXT=['Establish a simple training-fitted reference baseline.','Turn classification scores into explicit threshold-dependent decisions.','Inspect prediction failures in predefined groups.','Keep resolved experiment settings, validation metrics and artifacts in a keyed run.','Document supported limitations under the existing risk policy.','Evaluate supplied foundation-model outputs against matched validation evidence.','Construct PyTorch input tensors with compatible shapes and dtypes.']
OUT={'schema_version':P['schema_version'],'kind':'screens_part','path_id':P['path_id'],'batch_id':P['batch_id'],'tiles':[]}
for ti,t in enumerate(P['tiles']):
 tile={'tile_id':t['tile_id'],'title':['Metrics and acceptance','Establish a modeling baseline','Thresholds and candidate comparison','Failure groups, slices and mitigation','Track, repeat and bound experiments','Document model risks','Evaluate supplied foundation-model outputs'][ti],'steps':[],'remediation_steps':[]}
 for s in t['steps']:
  cid=s['concept_ids'][0];key=cid.split('.')[-1]; bundle=C[cid]
  step={k:copy.deepcopy(s[k]) for k in ['step_id','type','concept_ids']}
  step['lineage']={k:copy.deepcopy(s[k]) for k in ['teaching_block_ids','fact_ids','segment_ids','anchors']}
  if s['type']=='explainer':
   tbs=[tb for q in s['teaching_block_ids'] for tb in bundle['teaching_blocks'] if cid+'#'+tb['id']==q]
   step['title']=TITLES[key][int(tbs[-1]['id'][2:])-1]; step['blocks']=[prose(cid,tb) for tb in tbs]
   if s['planned_visual_block_type']:step['blocks']+=visuals(cid,s['planned_visual_block_type'])
  elif s['type']=='video':
   step['title']='Inspect '+G['names'][cid].lower();step['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(s['segment_ids'])}]
  elif s['type']=='recap':
   step['title']='Keep these distinctions';step['blocks']=[{'type':'prose','role':'takeaway','text':RECAP[ti],'lineage':{'concept_ids':t['concept_ids'],'teaching_block_ids':[c+'#'+tb['id'] for c in t['concept_ids'] for tb in C[c]['teaching_blocks']],'fact_ids':[c+'#'+f['id'] for c in t['concept_ids'] for f in C[c]['coverage']['required_facts']]}},{'type':'up_next','title':'Up next','text':NEXT[ti]}]
  else:
   if s['type']=='check':step['title']='Check the distinction';step['lede']='Read the supplied evidence and choose the response that follows the declared rule.'
   elif s['planned_interaction_type'] in ['choice','classify']:
    step['title']='Review the logging excerpts';step['lede']='Read the supplied excerpts in this step and decide which correctly preserve the resolved configuration and keyed tracking evidence.'
   elif s['planned_interaction_type']=='external_proof':step['title']='Write one bounded risk record';step['lede']='Use the supplied policy and evaluation evidence to record mismatches and limitations without changing permissions or copying secrets.'
   elif s['planned_interaction_type']=='formula_entry':step['title']='Calculate from the supplied evidence';step['lede']='Use the supplied dataset and fixed contract. Keep the conditioning population explicit when entering the requested formula.'
   else:step['title']='Implement the bounded evaluation';step['lede']='Complete the requested function on the supplied fixture using the declared inputs, fixed criteria and observation boundaries.'
   # Separate check/practice routes cover their respective fact sets without reading stage 04.
   measured=set(f for a in bundle['assessment_anchors'] for f in a['fact_ids']) if s['type']=='check' else set(f['id'] for f in bundle['coverage']['required_facts'])
   tbs=[tb for tb in bundle['teaching_blocks'] if tb['purpose'] not in ['example','intro','misconception'] and set(tb['fact_ids'])&measured]
   rid=t['tile_id']+'.r'+str(len(tile['remediation_steps'])+1).zfill(2)
   rem={'step_id':rid,'type':'remediation','required':False,'concept_ids':[cid],'title':'Revisit: '+('the check' if s['type']=='check' else 'the practice')+' — '+TITLES[key][0].lower(),'lineage':lin(cid,[cid+'#'+tb['id'] for tb in tbs],[cid+'#'+f for f in sorted(measured)])}
   rem['blocks']=[{'type':'prose','text':CONTRAST[key],'role':'misconception','lineage':copy.deepcopy(rem['lineage'])}]+[prose(cid,tb) for tb in tbs]
   rem['blocks'].append(table(cid,DATA[key][0],visual=False))
   tile['remediation_steps'].append(rem)
  tile['steps'].append(step)
 OUT['tiles'].append(tile)
(B/'screens.json').write_text(json.dumps(OUT,ensure_ascii=False,indent=2)+'\n')
print('tiles',len(OUT['tiles']),'planned steps',sum(len(t['steps']) for t in OUT['tiles']),'remediation',sum(len(t['remediation_steps']) for t in OUT['tiles']))
