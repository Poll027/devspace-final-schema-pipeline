import json, re, copy
from pathlib import Path
B=Path('batches/final_batch_mle.region.validation_and_selection')
P=json.load(open(B/'tile_plans.json')); G=json.load(open(B/'inputs/path_glossary_bundle.json')); R=json.load(open(B/'scenario_asset_registry.json'))
bundles={x['context']['concept_id']:x for x in G['bundles']}; assets={x['asset_id']:x for x in R['assets']}
# Re-voiced, bounded teaching rules. Each entry corresponds to a glossary fact.
F={
 'task_metric_selection':[
 'Choose classification metrics for class balance and the consequences and costs of false positives and false negatives, not accuracy alone.',
 'Precision = TP/(TP+FP) asks how many predicted positives are truly positive. Recall = TP/(TP+FN) asks how many actual positives were detected.',
 'MAE averages absolute regression errors; MSE averages squared errors, giving larger errors more influence.',
 'Validation prevalence is actual positives divided by the validation population; use it to interpret that cohort’s metrics.',
 'Confusion-table frequencies describe this cohort’s outcomes. They do not establish calibration of individual probability scores.'],
 'model_acceptance_criteria':[
 'Declare measurable predictive acceptance and the supplied deployment compatibility requirements before comparing candidates.',
 'Keep supplied deployment class probabilities and error costs fixed; do not choose inputs to favor a result.',
 'FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) conditions on actual positives. Empty groups leave rates undefined.',
 'With correct predictions costing zero, expected error cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN.',
 'Compare expected cost with the predeclared upper bound using <=. Operating limits are separate eligibility requirements.'],
 'reference_baseline':[
 'DummyClassifier offers reference rules such as most_frequent, prior and constant. DummyRegressor(strategy="mean") predicts the training-target mean.',
 'Fit the reference on training inputs and targets, freeze it, then predict on separate validation inputs.',
 'Evaluate baseline predictions against validation targets using the predeclared metric, not a training-only score.',
 'Use np.mean(numeric_values) for the arithmetic mean of the selected numeric observations.',
 'Use np.std(numeric_values, ddof=0): divide squared deviations by N, then take the square root. Use ddof=1 only for a required N−1 divisor.',
 'FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. An empty group has no defined rate.',
 'With zero correct-prediction cost, expected cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN, using supplied deployment probabilities.',
 'Keep protected-test observations out of preprocessing fit, model choice and tuning; otherwise information leaks into the selected system.',
 'Report training target-class count divided by training total. Validation or protected-test prevalence is not a substitute.'],
 'model_approach_decision':[
 'Use the same intended task and cohort to compare quality and deployment compatibility before promotion.',
 'Inference options differ in latency, scale and cost; apply the supplied operating constraints to eligibility.',
 'Exclude alternatives failing precommitted quality or operating limits, then apply the fixed selection rule to eligible records.',
 'FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined.',
 'With correct predictions costing zero, expected cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN, using supplied deployment probabilities.',
 'Protected-test observations cannot guide preprocessing fit, model choice or tuning: that would leak information into the chosen system.',
 'Custom classical or neural task-model implementation and training choices remain with the owner. A managed service can provide training/hosting infrastructure; compare maintenance responsibilities too.',
 'Discuss classical/neural and custom/managed trade-offs from matched supplied records, without fitting new alternatives to manufacture evidence.'],
 'sklearn_baseline_workflow':[
 'Import LogisticRegression from sklearn.linear_model. Fit LogisticRegression(random_state=0) on numeric X_train shaped (n_samples, n_features) and aligned class labels y_train shaped (n_samples,).',
 'Apply estimator.predict(X_validation), then compare outputs with the corresponding y_validation observations.',
 'If preprocessing was fitted in a pipeline, predict through that pipeline to reuse the training feature representation.',
 'FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. An empty group leaves its rate undefined.',
 'With zero cost for correct predictions, expected cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN, using supplied deployment probabilities.'],
 'decision_threshold_selection':[
 'A score becomes a class decision only when compared with a threshold; these are different outputs.',
 'Binary scikit-learn probability scores ordinarily use a 0.5 cutoff; decision_function scores use zero. An explicitly chosen task threshold changes decisions.',
 'Form labels at each supplied threshold, then count TP, FP, TN and FN against the same validation labels.',
 'Select the eligible threshold with minimum predeclared validation expected cost and freeze it before protected testing.',
 'FPR = FP/(FP+TN) conditions on actual negatives; FNR = FN/(FN+TP) on actual positives. Empty groups leave rates undefined.',
 'With correct predictions costing zero, expected cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN, using supplied deployment probabilities.',
 'Do not fit preprocessing, choose models or tune settings using protected-test observations; that leaks information into the chosen system.'],
 'validation_candidate_comparison':[
 'Compare candidates and baseline on the same evaluation dataset and predeclared requirements, not incomparable cohorts.',
 'Use the same supplied deployment probabilities and error costs for every record. Exclude fixed-limit failures, then rank eligible records by the declared cost rule.',
 'FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups do not define rates.',
 'With zero correct-prediction cost, expected cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN, using supplied deployment probabilities.',
 'Protected-test observations stay outside preprocessing fit, model choice and tuning, which would leak information into the chosen system.'],
 'prediction_error_analysis':[
 'Inspect supplied prediction failures; the developer’s own usage is not necessarily representative of users.',
 'For the predefined failure group, divide its error count by its eligible count to get its conditional error proportion.',
 'Compare this group with its same-cohort reference to localize observed failures. An overall score does not describe every segment.',
 'Calculate the selected numeric observations’ arithmetic mean with np.mean(numeric_values).',
 'np.std(numeric_values, ddof=0) divides squared deviations by N before taking the square root. Use ddof=1 only when the required divisor is N−1.'],
 'slice_evaluation':[
 'Evaluate predefined slices separately: overall improvement can coexist with uneven segment performance.',
 'Keep each slice’s eligible count beside errors divided by that count; retain the conditioning population.',
 'A sample may not represent its intended population. Observed slice differences alone do not establish a population-level disparity.',
 'Use np.mean(numeric_values) to average the selected numeric observations.',
 'Use np.std(numeric_values, ddof=0): squared deviations are divided by N before the square root. Use ddof=1 only for a required N−1 divisor.'],
 'subgroup_risk_mitigation':[
 'Check whether the data represents intended groups before blaming a subgroup problem solely on the model.',
 'Evaluate the supplied mitigation on both the affected validation segment and overall validation cohort before accepting it.',
 'Multiply supplied deployment subgroup probability by subgroup-conditional expected harm, using supplied error costs, to obtain its total-harm contribution.',
 'FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined.'],
 'experiment_metric_logging':[
 'Use import mlflow and with mlflow.start_run() as run; retain the run_id identifying the tracking record.',
 'Log resolved parameters with mlflow.log_params(params), validation metrics with mlflow.log_metric(name, value), and a diagnostic file with mlflow.log_artifact(local_path).',
 'Inspect git rev-parse --verify HEAD for the actual repository revision before recording code identity.',
 'Retrieve recorded = mlflow.get_run(run_id). Read recorded.data.params, recorded.data.metrics and recorded.info.artifact_uri. Repeated metrics expose the most recent value at the largest step, not full history.',
 'Give the logging function defaults and explicit keyword overrides; log the resolved values, not merely defaults.',
 'Inspect os.getcwd() and use os.chdir(recorded_directory) to resolve repository/artifact paths. Retain the resolved local path in the lookup.',
 'Capture subprocess.run output in the intended working directory when inspecting git rev-parse --verify HEAD. Reject revision mismatches before claiming artifact/run identity.'],
 'training_randomness':[
 'Supported integer random_state settings reset generators for repeatable calls. None or a shared RandomState consumes state differently.',
 'Control estimator and split randomness, without claiming every environment or computation is deterministic.',
 'Loop over the declared seeds with for, collecting each matched pair of validation results.',
 'Empirical win probability is winning pairs divided by all completed pairs; retain the completed trial count.',
 'Average selected numeric results with np.mean(numeric_values).',
 'np.std(numeric_values, ddof=0) divides squared deviations by N before the square root. Use ddof=1 only when N−1 is the required divisor.'],
 'validation_regularization':[
 'Good training performance alongside poor validation performance, under the same scoring interpretation, is evidence of overfitting.',
 'Compare declared regularization settings under the same validation protocol. Select by the predeclared validation criterion, not training score alone.',
 'FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty conditioning groups leave rates undefined.',
 'With correct predictions costing zero, expected cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN, using supplied deployment probabilities.',
 'Protected-test observations cannot guide preprocessing fit, model choice or tuning; doing so leaks information into the chosen system.',
 'Regularization penalizes complexity during fitting. Larger Ridge alpha increases its penalty; LogisticRegression C is inverse regularization strength.'],
 'bounded_hyperparameter_search':[
 'GridSearchCV enumerates param_grid combinations. RandomizedSearchCV samples configurations within the n_iter bound.',
 'Declare scoring and evaluation protocol before search; inspect validation-selected best_params_ and cv_results_.',
 'For manual search, iterate the supplied bounded configuration dictionaries, run declared trials and record validation results without exceeding the fixed budget.',
 'FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined.',
 'With zero correct-prediction cost, expected cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN, using supplied deployment probabilities.',
 'Keep protected-test observations out of preprocessing fit, model choice and tuning; otherwise information leaks into the chosen system.',
 'Define a default search budget and allow explicit keyword overrides. Resolve the actual budget before iterating trials.'],
 'model_risk_documentation':[
 'Audit supplied grants against the existing permitted identity scope. Record out-of-scope grants rather than inventing a new policy.',
 'Literal credentials in images or metadata are exposure risks. Describe the handling limitation without copying the secret.',
 'Aggregate improvement can hide segment differences. State supported evaluation limitations, not universal suitability.',
 'Build one record from existing policy fields, preserving permitted identities, documented task limits and foreseeable misuse without expanding permissions.'],
 'foundation_model_baseline_evaluation':[
 'Evaluate supplied foundation-model outputs on the same task-specific labeled validation examples and acceptance requirements as the reference.',
 'Compare supplied-output quality with the validation baseline and state observed limitations. This is not application construction or model training.',
 'FPR = FP/(FP+TN) uses actual negatives; FNR = FN/(FN+TP) uses actual positives. Empty groups leave rates undefined.',
 'With correct predictions costing zero, expected cost = P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN, using supplied deployment probabilities.',
 'Protected-test observations cannot guide preprocessing fit, model choice or tuning; doing so leaks information into the chosen system.']}
INTRO=dict(zip(F,[
 'Which errors matter for late orders?', 'Set the contract before results arrive.', 'Give the candidate a comparable reference.', 'Judge supplied alternatives, not their labels.', 'Connect aligned inputs to held-out evidence.', 'Make the score-to-decision rule explicit.', 'Eligibility comes before ranking.', 'Locate failures in the predefined group.', 'Keep delivery-zone evidence separate.', 'Check the supplied mitigation at both scopes.', 'Connect settings, results and artifacts by key.', 'Retain each repeated comparison as a pair.', 'Investigate the training/validation gap.', 'Set the stopping boundary before trials.', 'Record policy and evidence without expanding either.', 'Evaluate the supplied output file, not a new application.']))
EXAMPLES={
 'task_metric_selection':'Read precision from the predicted-positive group and recall from the actual-positive group. The displayed totals expose their different denominators. Prevalence uses the whole cohort. In the separate regression fixture, compare the absolute-error and squared-error averages: squaring gives the larger residual more influence. Choose the task metric for target type and error consequences before comparison. These cohort outcomes do not establish calibration of an individual probability score.',
 'model_acceptance_criteria':'The two actual-class rows separate deployment probability, conditional error rate and error cost. Sum their weighted contributions and compare with the fixed bound. A passing predictive quantity does not resolve latency or other operating requirements. The formula assumes zero cost for correct predictions. Do not substitute validation prevalence for supplied deployment probabilities. Keep actual-class counts: an empty group leaves a required rate unresolved, not perfect.',
 'reference_baseline':'Fit most_frequent on the training labels, then keep that state fixed for validation. Record training positive count divided by training total, not validation prevalence. In the separate regression fixture, the mean reference uses training targets; check their mean and declared spread independently. Evaluate held-out predictions under the fixed metric. For expected cost, retain actual-class denominators and supplied deployment probabilities and costs. Protected-test observations cannot participate in fit or selection.',
 'model_approach_decision':'The neural record’s lower expected cost cannot rescue its failed latency requirement. Inspect the classical and managed records under the same cohort, quality bound and operating predicates. Select only among eligible records with the fixed rule. Keep maintenance responsibility visible: managed infrastructure does not erase owner choices for a custom task model. Use supplied matched evidence rather than fitting extra alternatives. Protected-test observations cannot influence the choice.',
 'sklearn_baseline_workflow':'Check training dimensions and target correspondence before fit. Apply the fitted estimator to aligned validation inputs; if preprocessing was fitted, use its pipeline prediction path. Compare predictions with the corresponding held-out labels, then count errors. Actual negatives condition FPR; actual positives condition FNR. Apply the fixed deployment probabilities and costs only after those rates are defined. Fit returning successfully is not a held-out quality verdict.',
 'decision_threshold_selection':'The same displayed order score can exceed one supplied cutoff and fall below the other. The score stays fixed while labels, confusion counts and conditional rates change. Recompute every threshold’s quantities on the same validation observations. Select the minimum-cost eligible record using unchanged deployment probabilities, costs and limits. Retain the cutoff, score representation and validation evidence before protected testing; do not tune it with protected-test results.',
 'validation_candidate_comparison':'Compare baseline and candidate only where cohort identity matches. A lower number from a different cohort is excluded, not evidence that the candidate won or lost on these orders. Apply fixed quality and operating limits before ranking. Keep confusion counts, actual-class denominators, deployment probabilities and error costs beside the chosen identity. Operating failures are exclusions, not informal score penalties. Freeze the validation selection without using protected-test observations for fitting or tuning.',
 'prediction_error_analysis':'Read the predefined long-distance group’s errors together with its eligible count. The same error count in a larger group would imply a different proportion. Inspect its observations and same-cohort reference without moving the boundary after seeing failures. Selected loss or feature means and spreads describe that evidence; they do not establish a cause. Keep the observation definition and standard-deviation divisor attached to each summary.',
 'slice_evaluation':'Compare zone labels, eligible counts and observed error proportions side by side. Different denominators matter even when only percentages seem convenient. Keep numerical loss summaries tied to their selected slice and declared divisor. Aggregate improvement does not replace this segment evidence. State the observed sample gap and representation limitation together: these examples alone do not prove a disparity throughout the intended population.',
 'subgroup_risk_mitigation':'Compare reference and mitigation at the subgroup and overall scopes. Population weighting changes the subgroup’s contribution, not its conditional harm. Use the same supplied deployment subgroup probability and error costs for both records. Keep actual-positive and actual-negative denominators distinct; an empty denominator leaves a rate undefined. A lower subgroup contribution is not blanket acceptance: inspect overall evidence and representation before extending the result to deployment.',
 'experiment_metric_logging':'The explicit trial-setting override, not its default, belongs in the resolved parameter dictionary. Start the run, retain its key and log the diagnostic file from its resolved path. Inspect repository revision in the intended directory. Retrieve the keyed record and compare parameters, validation metrics and artifact location. Repeated RunData metrics are not full history. A revision mismatch or wrong local artifact path prevents claiming that the artifact belongs to this run.',
 'training_randomness':'Keep seed, baseline result and candidate result together. Count wins among completed pairs rather than comparing two unpaired averages. Retain the denominator and compute selected-result means and the declared standard deviation. A missing trial is not a win. Control both estimator and split sources as required; integer random_state behavior does not justify claims of computation-wide or environment-wide determinism.',
 'validation_regularization':'The setting with the better training cost need not have the better validation cost. Use the same scoring interpretation, cohort, probabilities and costs while comparing supplied settings. Choose by fixed validation evidence and eligibility, not training alone. Keep estimator names beside parameters: larger Ridge alpha increases the penalty, while LogisticRegression C has the inverse-strength interpretation. The gap supports investigation, not an invented cause. Protected-test results cannot become another tuning trial.',
 'bounded_hyperparameter_search':'Resolve the keyword budget override before running any configuration. The displayed third configuration is outside this bounded run, not a completed trial. Retain actual completed configuration dictionaries and validation quantities. Declare scoring and evaluation protocol separately from grid enumeration or randomized sampling. Inspect best_params_ and cv_results_ under that protocol. Apply fixed expected-cost inputs and eligibility requirements; a search’s best label is not automatic acceptance. Protected-test evidence cannot extend the search.',
 'model_risk_documentation':'Compare the permitted identity set with observed grants; an extra grant is a mismatch, not permission to enlarge the set. Describe the supplied credential-exposure location without reproducing a secret. Map documented task limits, foreseeable misuse and supported segment limitations into one existing-policy record. Separate permission language from evidence language. Aggregate improvement cannot justify universal suitability, and documenting a mismatch is not authorization.',
 'foundation_model_baseline_evaluation':'Align every supplied output with its validation identifier and label before counting errors. Compare against the corresponding reference under unchanged acceptance requirements, deployment probabilities and error costs. A different cohort would not be matched evidence. Report only the observed task limitations of this file, not suitability for all foundation-model uses. Keep protected-test observations outside fitting and selection. This bounded evaluation does not require prompts, retrieval infrastructure or application construction.'}
MIS={
 'task_metric_selection':'Precision and recall use different groups; neither proves probability-score calibration.',
 'model_acceptance_criteria':'Low predictive cost is not operating acceptance. Keep supplied probabilities and costs fixed.',
 'reference_baseline':'A training score cannot replace the matched validation reference or bypass the protected-test boundary.',
 'model_approach_decision':'Quality alone is insufficient; managed infrastructure does not erase owner responsibility or repair unmatched evidence.',
 'sklearn_baseline_workflow':'Prediction alone is not quality evidence; use matching held-out labels and fitted preprocessing.',
 'decision_threshold_selection':'Scores are not decisions. Protected-test evidence cannot rescue a threshold choice.',
 'validation_candidate_comparison':'The smallest cost is not necessarily the eligible winner; matched evidence and fixed limits matter.',
 'prediction_error_analysis':'Overall scores hide segments; error counts need eligible denominators.',
 'slice_evaluation':'Overall gains can coexist with slice gaps; sample gaps alone do not prove population disparity.',
 'subgroup_risk_mitigation':'Subgroup gains alone are insufficient; distinguish population probability, conditional harm and representation. Empty groups leave rates undefined.',
 'experiment_metric_logging':'A printed metric is not a verified keyed record; revision, resolved overrides and artifact path must agree.',
 'training_randomness':'Controlled seeds do not guarantee universal determinism; an empirical win fraction describes completed trials only.',
 'validation_regularization':'Training performance alone does not select the setting. Larger C does not mean stronger LogisticRegression regularization.',
 'bounded_hyperparameter_search':'An override replaces the default budget. Protected-test evidence cannot authorize more tuning.',
 'model_risk_documentation':'Documentation grants no permission, proves no universal suitability and must not reproduce secrets.',
 'foundation_model_baseline_evaluation':'Task-specific supplied-output evaluation is not evidence of application-building or model-training competence.'}

def lineage(c,facts=None,tbs=None,anchor=False):
 return {'concept_ids':[c], 'fact_ids':facts or [], 'teaching_block_ids':tbs or [], **({'anchors':[c+'#visual']} if anchor else {})}
def words(t):return len(t.split())
def split_text(t,limit=85):
 # Sentence boundaries preserve each standalone rule and its qualifiers.
 out=[];cur=''
 for sent in re.split(r'(?<=[.!?])\s+(?=[A-ZΑ])',t):
  if cur and words(cur+' '+sent)>limit:out.append(cur);cur=''
  cur=(cur+' '+sent).strip()
 if cur:out.append(cur)
 return out

def prose(text,c,facts,tbs,role='mechanism'):
 return [{'type':'prose','text':t,'role':role,'lineage':lineage(c,facts,tbs)} for t in split_text(text)]
def ref(a,cols=None):
 if cols:
  assert set(cols)<=set(x['name'] for x in assets[a]['columns']), (a,cols)
 return {'asset_id':a,**({'columns':cols} if cols else {})}
def table(a,c,cols=None,caption=None):
 return {'type':'data_table','asset_ref':ref(a,cols),'caption':caption or assets[a]['title'],'lineage':lineage(c,anchor=True)}
def query(c,sql,mounts,caption):
 return {'type':'data_table','result_of':{'runtime':'sql','sql':sql,'asset_mounts':[{'asset_id':a,'mount_path':m} for a,m in mounts]},'caption':caption,'lineage':lineage(c,anchor=True)}
def xl(n):
 out=''
 while n:n,k=divmod(n-1,26);out=chr(65+k)+out
 return out
def grid(a,c,cols,annotations=None):
 return {'type':'spreadsheet_grid','asset_ref':ref(a,cols),'range':f'A1:{xl(len(cols))}{len(assets[a]["rows"])+1}','show_formula_bar':True,'annotations':annotations or [],'lineage':lineage(c,anchor=True)}
contract_cols=['deployment_negative_probability','deployment_positive_probability','cost_FP','cost_FN','correct_prediction_cost','expected_cost_bound','empty_group_rule','operating_limit']
counts=['TP','FP','FN','TN','actual_positive_count','actual_negative_count']
rates=['FPR','FNR','expected_error_cost']
def contract(c):return table('ds.acceptance_contract',c,contract_cols,'Fixed predictive inputs; operating eligibility remains separate.')
def codeblock(c,code):return {'type':'code_walkthrough','language':'python','code':code,'reveal':'line_by_line','lineage':lineage(c,anchor=True)}

# Code demonstrates computation; output and execution provenance are deliberately absent.
RATE_CODE='''    TP = int(np.sum((actual == 1) & (predicted == 1)))
    FP = int(np.sum((actual == 0) & (predicted == 1)))
    FN = int(np.sum((actual == 1) & (predicted == 0)))
    TN = int(np.sum((actual == 0) & (predicted == 0)))
    negatives, positives = FP + TN, FN + TP
    FPR = FP / negatives if negatives else None
    FNR = FN / positives if positives else None
    cost = None if FPR is None or FNR is None else (
        contract["deployment_negative_probability"] * FPR * contract["cost_FP"]
        + contract["deployment_positive_probability"] * FNR * contract["cost_FN"])
    return {"TP": TP, "FP": FP, "FN": FN, "TN": TN,
            "actual_negative_count": negatives, "actual_positive_count": positives,
            "FPR": FPR, "FNR": FNR, "expected_error_cost": cost}
'''
EVIDENCE='import numpy as np\ndef evidence(actual, predicted, contract):\n'+RATE_CODE
REF_CODE=EVIDENCE+'''from sklearn.dummy import DummyClassifier, DummyRegressor

def reference(X_train, y_train, X_validation, y_validation, regression_targets, contract):
    estimator = DummyClassifier(strategy="most_frequent")
    estimator.fit(X_train, y_train)
    predictions = estimator.predict(X_validation)
    result = evidence(np.asarray(y_validation), predictions, contract)
    result.update(training_positive_count=int(np.sum(np.asarray(y_train) == 1)),
                  training_count=len(y_train),
                  training_positive_proportion=float(np.mean(np.asarray(y_train) == 1)),
                  validation_predictions=predictions.tolist(),
                  validation_actual=np.asarray(y_validation).tolist(),
                  target_mean=float(np.mean(regression_targets)),
                  target_std=float(np.std(regression_targets, ddof=0)))
    mean_reference = DummyRegressor(strategy="mean")
    mean_reference.fit(np.arange(len(regression_targets)).reshape(-1, 1), regression_targets)
    result["mean_reference_predictions"] = mean_reference.predict(X_validation[:, :1]).tolist()
    return result
'''
SK_CODE=EVIDENCE+'''from sklearn.linear_model import LogisticRegression

def baseline(X_train, y_train, X_validation, y_validation, contract):
    estimator = LogisticRegression(random_state=0)
    estimator.fit(X_train, y_train)
    # If preprocessing was fitted, use that fitted pipeline's predict instead.
    predicted = estimator.predict(X_validation)
    return {"training_shape": X_train.shape, "target_shape": y_train.shape,
            "validation_shape": X_validation.shape, "estimator": estimator,
            "aligned_predictions": list(zip(y_validation.tolist(), predicted.tolist())),
            "evidence": evidence(y_validation, predicted, contract)}
'''
LOG_CODE='''import os
import subprocess
import mlflow

def log_trial(recorded_directory, diagnostic_file, expected_revision,
              validation_metrics, trial_setting=DEFAULT_TRIAL_SETTING):
    previous_directory = os.getcwd()
    try:
        os.chdir(recorded_directory)
        resolved_directory = os.getcwd()
        local_path = os.path.abspath(diagnostic_file)
        revision = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"], cwd=resolved_directory,
            capture_output=True, text=True, check=True).stdout.strip()
        if revision != expected_revision:
            raise ValueError("repository revision mismatch")
        params = {"trial_setting": trial_setting, "repository_revision": revision,
                  "local_artifact_path": local_path}
        with mlflow.start_run() as run:
            run_id = run.info.run_id
            mlflow.log_params(params)
            for name, value in validation_metrics.items():
                mlflow.log_metric(name, value)
            mlflow.log_artifact(local_path)
        recorded = mlflow.get_run(run_id)
        return {"run_id": run_id, "resolved_local_path": local_path,
                "params": recorded.data.params, "metrics": recorded.data.metrics,
                "artifact_uri": recorded.info.artifact_uri}
    finally:
        os.chdir(previous_directory)

# DEFAULT_TRIAL_SETTING and execution_contract come from the supplied fixture.
# The caller's explicit keyword value overrides the default before logging.
# log_trial(..., trial_setting=execution_contract["override_trial_setting"])
'''
# Substitute default from data rather than typing a fixture value.
ec=assets['ds.execution_contract']; ecrow=dict(zip([x['name'] for x in ec['columns']],ec['rows'][0]))
LOG_CODE=LOG_CODE.replace('trial_setting=DEFAULT_TRIAL_SETTING', 'trial_setting='+repr(ecrow['default_trial_setting']))

# Eligibility and rank are derived in queries, never authored result rows.
def eligibility_query(c,a,idcol):
 cols=[x['name'] for x in assets[a]['columns']]
 operating=[x for x in cols if x.endswith('_requirement_met') or x=='deployment_compatibility_met' or x=='operating_requirements_met']
 ops=' AND '.join('r.'+x+' = 1' for x in operating) or '1=1'
 sql=f'''WITH checked AS (
 SELECT r.*, r.rowid AS declared_order, k.deployment_negative_probability, k.deployment_positive_probability,
 k.cost_FP, k.cost_FN, k.expected_cost_bound,
 CASE WHEN actual_positive_count = 0 OR actual_negative_count = 0 THEN 'undefined required rate'
 WHEN cohort_id != (SELECT cohort_id FROM records LIMIT 1) THEN 'different cohort'
 WHEN expected_error_cost > k.expected_cost_bound THEN 'quality limit'
 WHEN NOT ({ops}) THEN 'operating limit' ELSE 'eligible' END AS eligibility
 FROM records r CROSS JOIN contract k),
 ranked AS (SELECT {idcol}, ROW_NUMBER() OVER (ORDER BY expected_error_cost, declared_order) AS eligible_rank
 FROM checked WHERE eligibility = 'eligible')
 SELECT checked.*, ranked.eligible_rank,
 CASE WHEN ranked.eligible_rank = 1 THEN 'retain selection' ELSE '' END AS selection
 FROM checked LEFT JOIN ranked USING ({idcol})'''
 return query(c,sql,[(a,'records'),('ds.acceptance_contract','contract')],'Matched eligibility before fixed-cost ranking.')

def visuals(c):
 k=c.removeprefix('mle.')
 if k=='task_metric_selection':
  return [table('ds.confusion_counts',c,caption='Actual and predicted classes are separate.'),query(c,"SELECT SUM(CASE WHEN predicted_label=1 THEN count ELSE 0 END) AS predicted_positive_total, SUM(CASE WHEN actual_label=1 THEN count ELSE 0 END) AS actual_positive_total, SUM(count) AS cohort_total FROM counts",[('ds.confusion_counts','counts')],'Denominators: precision, recall, prevalence.'),table('ds.metric_summary',c,['precision','recall','validation_prevalence'],'Cohort frequencies, not score calibration.'),table('ds.regression_errors',c,caption='Separate regression residuals.'),table('ds.regression_error_summary',c,caption='Absolute versus squared averages.')]
 if k=='model_acceptance_criteria':
  v=next(v for v in assets['ds.acceptance_terms']['variants'] if v['variant_id'])
  return [table('ds.acceptance_terms',c,caption='Actual-class weighted contributions.'),query(c,'SELECT SUM(weighted_contribution) AS expected_error_cost, expected_cost_bound, SUM(weighted_contribution) <= expected_cost_bound AS predictive_requirement_met FROM terms CROSS JOIN contract',[('ds.acceptance_terms','terms'),('ds.acceptance_contract','contract')],'Sum versus fixed bound.'),contract(c),{'type':'data_table','asset_ref':{'asset_id':'ds.acceptance_terms','variant_id':v['variant_id']},'caption':'Empty-group contrast: unresolved, not zero.','lineage':lineage(c,anchor=True)}]
 if k=='reference_baseline':return [codeblock(c,REF_CODE),table('ds.reference_train',c,caption='Training-only classification reference.'),table('ds.regression_targets',c,caption='Separate training mean-reference fixture.'),contract(c)]
 if k=='model_approach_decision':
  cols=['alternative_id','model_family','delivery_mode','cohort_id']+counts+rates+['latency_requirement_met','scale_requirement_met','training_cost_requirement_met','serving_cost_requirement_met','maintenance_requirement_met','deployment_compatibility_met','maintenance_responsibility']
  return [grid('ds.approach_records',c,cols),contract(c),eligibility_query(c,'ds.approach_records','alternative_id')]
 if k=='sklearn_baseline_workflow':return [codeblock(c,SK_CODE),table('ds.orders_train',c,caption='Aligned numeric training inputs and labels.'),table('ds.orders_validation',c,caption='Aligned held-out inputs and labels.'),contract(c)]
 if k=='decision_threshold_selection':
  return [table('ds.threshold_records',c,['threshold']+counts+rates+['predictive_requirement_met'],'Threshold-specific validation quantities.'),table('ds.thresholds',c,caption='Retain cutoff and score representation.'),query(c,'SELECT s.observation_id, s.score, t.threshold, CASE WHEN s.score >= t.threshold THEN 1 ELSE 0 END AS decision FROM scores s CROSS JOIN thresholds t WHERE s.score > (SELECT MIN(threshold) FROM thresholds) AND s.score < (SELECT MAX(threshold) FROM thresholds)',[('ds.validation_scores','scores'),('ds.thresholds','thresholds')],'Same score, different supplied decisions.'),query(c,'SELECT threshold, expected_error_cost FROM evidence WHERE predictive_requirement_met=1 ORDER BY expected_error_cost, threshold LIMIT 1',[('ds.threshold_records','evidence')],'Retained minimum-cost eligible cutoff.'),contract(c)]
 if k=='validation_candidate_comparison':return [eligibility_query(c,'ds.candidate_records','candidate_id'),contract(c)]
 if k=='prediction_error_analysis':
  return [query(c,'SELECT observation_id, cohort_id, eligible, long_distance, error, loss, reference_error, reference_loss, distance FROM observations WHERE long_distance=1',[('ds.slice_observations','observations')],'Predefined long-distance observations and same-cohort reference.'),query(c,"SELECT * FROM summaries WHERE slice='long-distance'",[('ds.slice_summary','summaries')],'Fixed-group counts and loss summaries.')]
 if k=='slice_evaluation':return [table('ds.slice_summary',c,caption='Predefined sample slices; counts and ddof stay visible.'),table('ds.aggregate_slice_evidence',c,caption='Matched aggregate evidence does not replace slices.')]
 if k=='subgroup_risk_mitigation':
  cols=['system','scope','cohort_id']+counts+rates+['validation_subgroup_prevalence','deployment_subgroup_probability','population_weighted_harm_contribution','representation_limitation','deployment_negative_probability','deployment_positive_probability','cost_FP','cost_FN']
  return [grid('ds.mitigation_records',c,cols),contract(c)]
 if k=='experiment_metric_logging':return [codeblock(c,LOG_CODE),table('ds.execution_contract',c,['default_trial_setting','override_trial_setting'],'Default versus resolved override.')]
 if k=='training_randomness':
  return [query(c,'SELECT *, candidate_result < baseline_result AS win FROM trials',[('ds.paired_trials','trials')],'Completed seed pairs; lower cost wins.'),query(c,'SELECT COUNT(*) AS completed_pairs, SUM(candidate_result < baseline_result) AS winning_pairs, 1.0*SUM(candidate_result < baseline_result)/COUNT(*) AS empirical_win_probability, AVG(candidate_result) AS candidate_mean, AVG(baseline_result) AS baseline_mean FROM trials',[('ds.paired_trials','trials')],'Paired denominator and selected-result means.'),codeblock(c,'import numpy as np\n# paired_trials is the supplied completed-pair fixture.\ncandidate = np.array([r["candidate_result"] for r in paired_trials])\nbaseline = np.array([r["baseline_result"] for r in paired_trials])\nsummary = {"candidate_std": np.std(candidate, ddof=0),\n           "baseline_std": np.std(baseline, ddof=0)}')]
 if k=='validation_regularization':
  left=query(c,'SELECT configuration_id, estimator, parameter_name, parameter_value, strength_direction, training_expected_error_cost FROM records',[('ds.regularization_records','records')],'Training under the same cost interpretation.')
  right=eligibility_query(c,'ds.regularization_records','configuration_id')
  return [{'type':'side_by_side','left':left,'right':right,'left_label':'Training','right_label':'Validation eligibility and selection','takeaway':'Select by fixed validation evidence, not training alone.','lineage':lineage(c,anchor=True)},table('ds.regularization_directions',c,caption='Estimator-specific penalty directions.'),contract(c)]
 if k=='bounded_hyperparameter_search':
  return [query(c,'''SELECT t.*, e.override_search_budget AS resolved_budget,
 CASE WHEN t.declared_order < e.override_search_budget THEN 'completed' ELSE 'unexecuted' END AS trial_status,
 CASE WHEN t.declared_order < e.override_search_budget AND FP+TN > 0 THEN 1.0*FP/(FP+TN) END AS FPR,
 CASE WHEN t.declared_order < e.override_search_budget AND FN+TP > 0 THEN 1.0*FN/(FN+TP) END AS FNR
 FROM trials t CROSS JOIN execution e ORDER BY declared_order''',[('ds.search_trials','trials'),('ds.execution_contract','execution')],'Resolved budget gates trial evidence.'),query(c,'''WITH costs AS (
 SELECT t.*, 1.0*FP/(FP+TN) AS FPR, 1.0*FN/(FN+TP) AS FNR,
 k.deployment_negative_probability * (1.0*FP/(FP+TN))*k.cost_FP +
 k.deployment_positive_probability * (1.0*FN/(FN+TP))*k.cost_FN AS expected_error_cost,
 k.expected_cost_bound
 FROM trials t CROSS JOIN execution e CROSS JOIN contract k
 WHERE declared_order < e.override_search_budget),
 eligible AS (SELECT *, ROW_NUMBER() OVER (ORDER BY expected_error_cost, declared_order) AS eligible_rank FROM costs
 WHERE expected_error_cost <= expected_cost_bound AND operating_requirements_met=1)
 SELECT costs.*, eligible.eligible_rank,
 CASE WHEN eligible.eligible_rank=1 THEN 'retain selection' ELSE '' END AS selection
 FROM costs LEFT JOIN eligible USING(configuration_id) ORDER BY costs.declared_order''',[('ds.search_trials','trials'),('ds.execution_contract','execution'),('ds.acceptance_contract','contract')],'Completed validation costs and eligible selection.'),contract(c)]
 if k=='model_risk_documentation':return [table('ds.risk_policy_evidence',c,caption='Existing fields, redacted observations, recording constraints.'),table('ds.access_grants',c,caption='Permitted identities versus supplied grants.'),table('ds.aggregate_slice_evidence',c,caption='Aggregate evidence is bounded.'),table('ds.slice_summary',c,caption='Supported segment limitations.')]
 if k=='foundation_model_baseline_evaluation':
  mounts=[('ds.validation_scores','labels'),('ds.foundation_outputs','outputs')]
  alignment='SELECT l.observation_id, l.cohort_id, l.actual_label, o.foundation_output, l.reference_output FROM labels l JOIN outputs o ON l.observation_id=o.observation_id AND l.cohort_id=o.cohort_id'
  sql='''WITH aligned AS ('''+alignment+'''), counts AS (
 SELECT SUM(actual_label=1 AND foundation_output=1) AS TP,
 SUM(actual_label=0 AND foundation_output=1) AS FP,
 SUM(actual_label=1 AND foundation_output=0) AS FN,
 SUM(actual_label=0 AND foundation_output=0) AS TN FROM aligned),
 rates AS (SELECT *, FP+TN AS actual_negative_count, FN+TP AS actual_positive_count,
 1.0*FP/NULLIF(FP+TN,0) AS FPR, 1.0*FN/NULLIF(FN+TP,0) AS FNR FROM counts),
 costs AS (SELECT r.*, k.deployment_negative_probability, k.deployment_positive_probability, k.cost_FP, k.cost_FN,
 k.deployment_negative_probability*r.FPR*k.cost_FP + k.deployment_positive_probability*r.FNR*k.cost_FN AS expected_error_cost,
 k.expected_cost_bound FROM rates r CROSS JOIN contract k)
 SELECT *, expected_error_cost <= expected_cost_bound AS predictive_requirement_met FROM costs'''
  return [query(c,alignment,mounts,'Identifiers align labels, supplied outputs and reference.'),query(c,sql,mounts+[('ds.acceptance_contract','contract')],'Actual-class rates and fixed predictive requirement.'),query(c,sql.replace('o.foundation_output', 'l.reference_output AS foundation_output'),mounts+[('ds.acceptance_contract','contract')],'Corresponding reference counts and fixed predictive requirement.'),contract(c)]
 raise ValueError(c)

TITLES=dict(zip(F,[ 'Choose the metric’s population','Predeclare acceptance','Build a reference','Compare modeling approaches','Fit, predict, evaluate','Choose a task threshold','Compare eligible candidates','Inspect predefined failures','Evaluate delivery-zone slices','Check a supplied mitigation','Retain a keyed experiment','Compare completed seed pairs','Select regularization on validation','Bound the search','Document existing-policy risk','Evaluate supplied task outputs']))
TAKEAWAYS={
 'task_metric_selection':'Match metrics to error consequences; retain their conditioning groups, not calibration claims.',
 'model_acceptance_criteria':'Keep predictive bounds, operating eligibility and supplied decision inputs fixed.',
 'reference_baseline':'Fit on training; evaluate the frozen reference on separate validation.',
 'model_approach_decision':'Compare matched eligible alternatives and their maintenance responsibilities.',
 'sklearn_baseline_workflow':'Aligned held-out predictions need fixed evaluation, through fitted preprocessing when present.',
 'decision_threshold_selection':'Choose and freeze an eligible validation threshold; scores and decisions differ.',
 'validation_candidate_comparison':'Exclude unmatched or ineligible records before fixed-cost ranking.',
 'prediction_error_analysis':'Localize observed failures with predefined groups and eligible denominators, not causal stories.',
 'slice_evaluation':'Retain sample counts and declared spread; sample gaps do not prove population disparity.',
 'subgroup_risk_mitigation':'Check representation, subgroup harm weighting and overall evidence together.',
 'experiment_metric_logging':'Verify resolved overrides, revision, keyed metrics and artifact paths.',
 'training_randomness':'Retain completed pairs and empirical wins without universal determinism claims.',
 'validation_regularization':'Select by fixed validation evidence; penalty direction depends on the estimator.',
 'bounded_hyperparameter_search':'Resolve the budget before trials and keep protected-test evidence outside search.',
 'model_risk_documentation':'Preserve existing permissions and supported limitations without exposing secrets.',
 'foundation_model_baseline_evaluation':'Align supplied outputs with the reference cohort; report bounded validation evidence only.'}

def tbtext(c,tb):
 k=c.removeprefix('mle.');purpose=tb['purpose']
 if purpose=='intro':return INTRO[k]
 if purpose=='example':return EXAMPLES[k]
 if purpose=='misconception':return MIS[k]
 return ' '.join(F[k][int(f[1:])-1] for f in tb['fact_ids'])

out={k:P[k] for k in ('schema_version','path_id','batch_id')};out['kind']='screens_part';out['tiles']=[]
for ti,t in enumerate(P['tiles']):
 names=[TITLES[c.removeprefix('mle.')] for c in t['concept_ids']]
 tile={'tile_id':t['tile_id'],'title':' · '.join(names),'summary':'Validation-only evidence for the supplied order task.','steps':[],'remediation_steps':[]}
 remkeys={}
 for s in t['steps']:
  c=s['concept_ids'][0];k=c.removeprefix('mle.')
  st={'step_id':s['step_id'],'type':s['type'],'concept_ids':copy.deepcopy(s['concept_ids']),'title':TITLES[k],'lineage':{key:copy.deepcopy(s[key]) for key in ('teaching_block_ids','fact_ids','segment_ids','anchors')}}
  if s['type'] in ('check','hands_on'):
   st['title']=('Check: ' if s['type']=='check' else 'Practice: ')+TITLES[k]
   st['eyebrow']='Apply the fixed validation contract'
   # Framing only: stage 04 owns all learner interactions and feedback links.
   tile['steps'].append(st)
   key=(c,tuple(sorted(s['fact_ids'])))
   if key not in remkeys:
    rid=f'{t["tile_id"]}.r{len(remkeys)+1:02d}';remkeys[key]=rid
    relevant=[tb for tb in bundles[c]['teaching_blocks'] if set(c+'#'+f for f in tb['fact_ids'])&set(s['fact_ids']) and tb['purpose'] not in ('example','misconception')]
    tbids=[c+'#'+tb['id'] for tb in relevant]
    rblocks=[]
    for f in s['fact_ids']:
     ftext=F[k][int(f.split('#f')[1])-1]
     related=[c+'#'+tb['id'] for tb in relevant if f.split('#')[1] in tb['fact_ids']]
     rblocks+=prose(ftext,c,[f],related)
    # One explicit contrast, grounded in the same registered fixture.
    mis_tb=next(tb for tb in bundles[c]['teaching_blocks'] if tb['purpose']=='misconception')
    mis_facts=[c+'#'+f for f in mis_tb['fact_ids']]
    rblocks+=prose(MIS[k],c,mis_facts,[c+'#'+mis_tb['id']],'misconception')
    # Same scenario fixture with one visible distinction, not a new example.
    rem_assets={
      'task_metric_selection':('ds.metric_summary',['actual_positive_count','cohort_count','precision','recall','validation_prevalence']),
      'model_acceptance_criteria':('ds.acceptance_terms',None),
      'reference_baseline':('ds.reference_train',None),
      'model_approach_decision':('ds.approach_records',['alternative_id','expected_error_cost','latency_requirement_met']),
      'sklearn_baseline_workflow':('ds.orders_validation',None),
      'decision_threshold_selection':('ds.threshold_records',['threshold','FPR','FNR','expected_error_cost']),
      'validation_candidate_comparison':('ds.candidate_records',['candidate_id','cohort_id','expected_error_cost','latency_requirement_met']),
      'prediction_error_analysis':('ds.slice_summary',['slice','eligible_count','error_count','error_probability']),
      'slice_evaluation':('ds.slice_summary',None),
      'subgroup_risk_mitigation':('ds.mitigation_records',['system','scope','expected_error_cost','deployment_subgroup_probability','population_weighted_harm_contribution','representation_limitation']),
      'experiment_metric_logging':('ds.execution_contract',['default_trial_setting','override_trial_setting']),
      'training_randomness':('ds.paired_trials',None),
      'validation_regularization':('ds.regularization_records',['configuration_id','estimator','parameter_value','training_expected_error_cost','expected_error_cost']),
      'bounded_hyperparameter_search':('ds.execution_contract',['default_search_budget','override_search_budget']),
      'model_risk_documentation':('ds.access_grants',None),
      'foundation_model_baseline_evaluation':('ds.foundation_outputs',['observation_id','cohort_id','output_kind','foundation_output'])}
    ra,rc=rem_assets[k]
    rb=table(ra,c,rc,'Revisit the same supplied fixture.')
    rb['lineage']=lineage(c,s['fact_ids'],tbids)
    rblocks.append(rb)
    tile['remediation_steps'].append({'step_id':rid,'type':'remediation','required':False,'concept_ids':[c],'title':'Review: '+TITLES[k],'blocks':rblocks,'lineage':lineage(c,s['fact_ids'],tbids)})
   continue
  st['blocks']=[]
  if s['type']=='video':
   st['title']='Review the same evaluation idea';st['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(s['segment_ids'])}]
  elif s['type']=='recap':
   st['title']='Keep the decision bounded'
   for cc in s['concept_ids']:
    bs=bundles[cc];facts=[cc+'#'+f['id'] for f in bs['coverage']['required_facts']];tbids=[cc+'#'+tb['id'] for tb in bs['teaching_blocks'] if tb['fact_ids']]
    st['blocks']+=prose(TAKEAWAYS[cc.removeprefix('mle.')],cc,facts,tbids,'takeaway')
   if ti+1<len(P['tiles']):nextc=P['tiles'][ti+1]['steps'][0]['concept_ids'][0]; nxt=G['names'][nextc]
   else:nxt=G['names']['mle.pytorch_input_tensors']
   st['blocks'].append({'type':'up_next','title':'Up next','text':nxt})
  else:
   planned_tbs={tb['id']:tb for tb in bundles[c]['teaching_blocks']}
   for tid in s['teaching_block_ids']:
    tb=planned_tbs[tid.split('#')[1]]
    text=tbtext(c,tb)
    if tb['purpose'] not in ('intro','example','misconception'):
     for f in tb['fact_ids']:
      st['blocks']+=prose(F[k][int(f[1:])-1],c,[c+'#'+f],[tid],tb['purpose'] if tb['purpose'] in ('definition','mechanism') else 'mechanism')
    else:
     st['blocks']+=prose(text,c,[c+'#'+f for f in tb['fact_ids']],[tid],tb['purpose'])
   # Small-budget boundary steps retain a short title.
   if s['word_budget']<40:st['title']='Remember'
   elif all(planned_tbs[x.split('#')[1]]['purpose']=='example' for x in s['teaching_block_ids']):st['title']='Read the supplied evidence'
   if s['planned_visual_block_type']:st['blocks']+=visuals(c)
  tile['steps'].append(st)
 out['tiles'].append(tile)
(B/'screens.json').write_text(json.dumps(out,indent=2)+'\n')
print('Wrote',B/'screens.json')
print('tiles',len(out['tiles']),'main steps',sum(len(t['steps']) for t in out['tiles']),'remediation',sum(len(t['remediation_steps']) for t in out['tiles']))
