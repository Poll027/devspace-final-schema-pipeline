# Helpers imported by build_screens.py through exec; registry and glossary are its only data sources.
def rows(asset_id):
 a=assets[asset_id]; return [dict(zip([c['name'] for c in a['columns']],r)) for r in a['rows']]
contract=rows('ds.acceptance_contract')[0]; execution=rows('ds.execution_contract')[0]
def lin(s,visual=False):
 d={k:copy.deepcopy(s.get(k,[])) for k in ('concept_ids','teaching_block_ids','fact_ids')}
 if visual:d['anchors']=[c+'#visual' for c in s['concept_ids']]
 return d
def table(s,aid,columns=None,caption=None):
 ref={'asset_id':aid}
 if columns:ref['columns']=columns
 return {'type':'data_table','asset_ref':ref,'caption':caption or assets[aid]['title'],'lineage':lin(s,True)}
def query(s,sql,mounts,caption):
 return {'type':'data_table','result_of':{'runtime':'sql','sql':sql,'asset_mounts':[{'asset_id':aid,'mount_path':name} for name,aid in mounts.items()]},'caption':caption,'lineage':lin(s,True)}
def excelcol(n):
 out=''
 while n: n,r=divmod(n-1,26);out=chr(65+r)+out
 return out
def grid(s,aid,columns=None):
 a=assets[aid]; cols=columns or [c['name'] for c in a['columns']]
 return {'type':'spreadsheet_grid','asset_ref':{'asset_id':aid,'columns':cols},'sheet_name':a['title'],'range':f'A1:{excelcol(len(cols))}{len(a["rows"])+1}','show_formula_bar':True,'lineage':lin(s,True)}
def code(s,txt,annotations=()):
 ls=txt.strip().splitlines(); ann=[]
 for match,description in annotations:
  idx=next(i for i,l in enumerate(ls,1) if match in l)
  ann.append({'start_line':idx,'end_line':idx,'text':description})
 return {'type':'code_walkthrough','language':'python','code':'\n'.join(ls),'reveal':'all','annotations':ann,'lineage':lin(s,True)}
COST='a.deployment_negative_probability * FPR * a.cost_FP + a.deployment_positive_probability * FNR * a.cost_FN'
requirements=['latency_requirement_met','scale_requirement_met','training_cost_requirement_met','serving_cost_requirement_met','maintenance_requirement_met','deployment_compatibility_met']
def selection(s,aid,idcol,matched=None,operating=None):
 names=[c['name'] for c in assets[aid]['columns']]
 operating=operating or [c for c in requirements if c in names]
 same=f'cohort_id = {json.dumps(matched)}' if matched is not None else 'TRUE'
 # A quoted SQL literal is produced from an existing record, never an authored scenario value.
 if matched is not None:same='cohort_id = '+"'"+matched.replace("'","''")+"'"
 reason=[f"WHEN NOT ({same}) THEN 'different cohort'", "WHEN actual_negative_count = 0 OR actual_positive_count = 0 THEN 'undefined conditional rate'", "WHEN expected_error_cost > expected_cost_bound THEN 'predictive bound failed'"]
 for c in operating:reason.append(f"WHEN NOT {c} THEN '{c.replace('_requirement_met','').replace('_met','')} failed'")
 eligible=f'({same}) AND actual_negative_count > 0 AND actual_positive_count > 0 AND expected_error_cost <= expected_cost_bound'+''.join(' AND '+c for c in operating)
 order_cases='CASE '+idcol+' '+ ' '.join('WHEN '+"'"+str(r[idcol]).replace("'","''")+"'"+' THEN '+str(i) for i,r in enumerate(rows(aid)))+' END'
 sql=f'''WITH inspected AS (
 SELECT r.*, a.deployment_negative_probability, a.deployment_positive_probability,
 a.cost_FP, a.cost_FN, a.expected_cost_bound, a.operating_limit,
 CASE {' '.join(reason)} ELSE 'eligible' END AS eligibility_reason,
 ({eligible}) AS eligible
 FROM records r CROSS JOIN acceptance a
), ranked AS (
 SELECT {idcol}, ROW_NUMBER() OVER (ORDER BY expected_error_cost, {order_cases}) AS eligible_rank
 FROM inspected WHERE eligible
)
SELECT i.*, ranked.eligible_rank, (ranked.eligible_rank = 1) AS retained_selection
FROM inspected i LEFT JOIN ranked ON i.{idcol} = ranked.{idcol}'''
 return query(s,sql,{'records':aid,'acceptance':'ds.acceptance_contract'},'Fixed inputs, separate exclusions, eligible rank and retained validation choice')
RATECODE='''    TP = int(np.sum((prediction == positive) & (y_validation == positive)))
    FP = int(np.sum((prediction == positive) & (y_validation == negative)))
    FN = int(np.sum((prediction == negative) & (y_validation == positive)))
    TN = int(np.sum((prediction == negative) & (y_validation == negative)))
    actual_negative_count, actual_positive_count = FP + TN, FN + TP
    FPR = FP / actual_negative_count if actual_negative_count else None
    FNR = FN / actual_positive_count if actual_positive_count else None
    expected_cost = None
    if FPR is not None and FNR is not None:
        expected_cost = p_negative * FPR * cost_FP + p_positive * FNR * cost_FN'''
negative=contract['correct_prediction_cost']; positive=contract['cost_FP']
REFERENCE=f'''import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score

def reference(X_train, y_train, X_validation, y_validation,
              p_negative, p_positive, cost_FP, cost_FN):
    negative, positive = {negative!r}, {positive!r}
    estimator = DummyClassifier(strategy="most_frequent")
    estimator.fit(X_train, y_train)
    prediction = estimator.predict(X_validation)
{RATECODE}
    return {{"training_mean": np.mean(y_train),
            "training_std": np.std(y_train, ddof={contract['ddof']!r}),
            "training_class_proportions": {{
                "negative": np.sum(y_train == negative) / len(y_train),
                "positive": np.sum(y_train == positive) / len(y_train)}},
            "prediction": prediction, "validation_accuracy": accuracy_score(y_validation, prediction),
            "TP": TP, "FP": FP, "FN": FN, "TN": TN,
            "actual_negative_count": actual_negative_count,
            "actual_positive_count": actual_positive_count,
            "FPR": FPR, "FNR": FNR, "expected_error_cost": expected_cost}}'''
SKLEARN=f'''import numpy as np
from sklearn.linear_model import LogisticRegression

def baseline(X_train, y_train, X_validation, y_validation,
             p_negative, p_positive, cost_FP, cost_FN, fitted_pipeline=None):
    negative, positive = {negative!r}, {positive!r}
    if fitted_pipeline is None:
        fitted = LogisticRegression(random_state={execution['estimator_random_state']!r})
        fitted.fit(X_train, y_train)
    else:
        fitted = fitted_pipeline
    prediction = fitted.predict(X_validation)
{RATECODE}
    return {{"training_input_shape": X_train.shape, "training_target_shape": y_train.shape,
            "validation_input_shape": X_validation.shape,
            "fitted": fitted, "prediction": prediction, "validation_labels": y_validation,
            "TP": TP, "FP": FP, "FN": FN, "TN": TN,
            "actual_negative_count": actual_negative_count,
            "actual_positive_count": actual_positive_count,
            "FPR": FPR, "FNR": FNR, "expected_error_cost": expected_cost}}'''
LOGGING=f'''import os
import subprocess
import mlflow

def log_and_inspect(recorded_directory, local_path, expected_revision,
                    validation_results, trial_setting={execution['default_trial_setting']!r}):
    original_directory = os.getcwd()
    os.chdir(recorded_directory)
    try:
        resolved_directory = os.getcwd()
        revision = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"], cwd=resolved_directory,
            capture_output=True, text=True, check=True).stdout.strip()
        if revision != expected_revision:
            raise ValueError("repository revision mismatch")
        resolved_path = os.path.abspath(local_path)
        params = {{"trial_setting": trial_setting,
                  "code_revision": revision, "artifact_path": resolved_path}}
        with mlflow.start_run() as run:
            run_id = run.info.run_id
            mlflow.log_params(params)
            for name, value in validation_results.items():
                mlflow.log_metric(name, value)
            mlflow.log_artifact(resolved_path)
        recorded = mlflow.get_run(run_id)
        if recorded.data.params.get("code_revision") != revision:
            raise ValueError("retrieved revision mismatch")
        if recorded.data.params.get("artifact_path") != resolved_path:
            raise ValueError("retrieved artifact path mismatch")
        return {{"run_id": run_id, "resolved_directory": resolved_directory,
                "params": recorded.data.params, "metrics": recorded.data.metrics,
                "artifact_uri": recorded.info.artifact_uri}}
    finally:
        os.chdir(original_directory)

# Invoke within the existing authorized repository/tracking runtime.
# Repository and artifact paths are supplied inputs, not invented locations.
record = log_and_inspect(recorded_directory, local_path, expected_revision,
                         validation_results, trial_setting={execution['override_trial_setting']!r})'''
def visuals(s):
 cid=s['concept_ids'][0].removeprefix('mle.')
 if cid=='task_metric_selection':
  return [table(s,'ds.confusion_counts'),query(s,'SELECT TP, FP, FN, TN, TP+FP AS predicted_positive_count, actual_positive_count, cohort_count, precision, recall, validation_prevalence FROM summary',{'summary':'ds.metric_summary'},'Attach each ratio to its conditioning population'),table(s,'ds.regression_errors'),table(s,'ds.regression_error_summary')]
 if cid=='model_acceptance_criteria':
  return [table(s,'ds.acceptance_terms'),query(s,'SELECT SUM(weighted_contribution) AS expected_error_cost, expected_cost_bound, SUM(weighted_contribution) <= expected_cost_bound AS predictive_requirement_met, operating_limit FROM terms CROSS JOIN acceptance GROUP BY expected_cost_bound, operating_limit',{'terms':'ds.acceptance_terms','acceptance':'ds.acceptance_contract'},'Predictive bound check; an unspecified operating limit remains unresolved'),table(s,'ds.acceptance_contract')]
 if cid=='reference_baseline':
  return [code(s,REFERENCE,[('estimator.fit','Training alone fits the reference.'),('prediction =','Frozen state produces validation predictions.'),('actual_negative_count,','Keep both actual-class denominators; empty groups remain undefined.'),('return {','Return training statistics and held-out evidence together.')]),table(s,'ds.reference_train'),table(s,'ds.orders_validation'),table(s,'ds.regression_targets'),table(s,'ds.acceptance_contract')]
 if cid=='model_approach_decision':
  return [grid(s,'ds.approach_records'),selection(s,'ds.approach_records','alternative_id',rows('ds.approach_records')[0]['cohort_id']),table(s,'ds.acceptance_contract')]
 if cid=='sklearn_baseline_workflow':
  return [code(s,SKLEARN,[('fitted.fit','Fit the declared estimator on aligned training inputs and labels.'),('fitted = fitted_pipeline','If supplied, use the previously fitted pipeline unchanged.'),('prediction =','Predict through the fitted object; compare with corresponding validation labels.'),('return {','Inspect dimensions, fitted state and held-out quantities together.')]),table(s,'ds.orders_train'),table(s,'ds.orders_validation'),table(s,'ds.acceptance_contract')]
 if cid=='decision_threshold_selection':
  # Order comes from the registered threshold list, preserving its tie policy.
  return [table(s,'ds.threshold_records'),query(s,'''WITH inspected AS (
 SELECT r.*, t.score_representation, t.declared_order, a.deployment_negative_probability,
 a.deployment_positive_probability, a.cost_FP, a.cost_FN, a.expected_cost_bound,
 (r.actual_negative_count > 0 AND r.actual_positive_count > 0 AND r.expected_error_cost <= a.expected_cost_bound) AS eligible
 FROM records r JOIN thresholds t ON r.threshold=t.threshold CROSS JOIN acceptance a
), ranked AS (SELECT threshold, ROW_NUMBER() OVER (ORDER BY expected_error_cost,declared_order) AS eligible_rank FROM inspected WHERE eligible)
SELECT i.*, ranked.eligible_rank, ranked.eligible_rank=1 AS retained_selection FROM inspected i LEFT JOIN ranked ON i.threshold=ranked.threshold ORDER BY i.declared_order''',{'records':'ds.threshold_records','thresholds':'ds.thresholds','acceptance':'ds.acceptance_contract'},'Eligible threshold ranking under fixed expected-cost inputs'),query(s,'''SELECT v.observation_id, v.actual_label, v.score, t.threshold, t.score_representation, v.score >= t.threshold AS predicted_positive FROM scores v CROSS JOIN thresholds t WHERE v.score > (SELECT MIN(threshold) FROM thresholds) AND v.score < (SELECT MAX(threshold) FROM thresholds) ORDER BY v.observation_id,t.declared_order''',{'scores':'ds.validation_scores','thresholds':'ds.thresholds'},'Unchanged scores can cross one supplied cutoff but not the other')]
 if cid=='validation_candidate_comparison':
  return [table(s,'ds.candidate_records'),selection(s,'ds.candidate_records','candidate_id',rows('ds.candidate_records')[0]['cohort_id']),table(s,'ds.acceptance_contract')]
 if cid=='prediction_error_analysis':
  return [table(s,'ds.slice_observations',['observation_id','cohort_id','eligible','long_distance','error','loss','reference_error','reference_loss','distance']),query(s,'''SELECT COUNT(*) AS eligible_count, SUM(error) AS error_count, AVG(CAST(error AS DOUBLE)) AS conditional_error_proportion,
 AVG(loss) AS loss_mean, SQRT(AVG(loss*loss)-AVG(loss)*AVG(loss)) AS loss_std,
 SUM(reference_error) AS reference_error_count, AVG(CAST(reference_error AS DOUBLE)) AS reference_error_proportion,
 AVG(reference_loss) AS reference_loss_mean, ddof FROM observations CROSS JOIN acceptance WHERE eligible AND long_distance GROUP BY ddof''',{'observations':'ds.slice_observations','acceptance':'ds.acceptance_contract'},'Predefined eligible long-distance group and same-cohort reference; population loss spread')]
 if cid=='slice_evaluation':
  return [table(s,'ds.slice_summary'),table(s,'ds.aggregate_slice_evidence'),table(s,'ds.slice_observations',['observation_id','cohort_id','zone','eligible','error','loss'])]
 if cid=='subgroup_risk_mitigation':
  return [grid(s,'ds.mitigation_records'),query(s,'''SELECT system,scope,cohort_id,actual_negative_count,actual_positive_count,FPR,FNR,
 deployment_negative_probability, deployment_positive_probability,cost_FP,cost_FN,
 expected_error_cost AS subgroup_or_overall_conditional_harm,
 deployment_subgroup_probability,population_weighted_harm_contribution,validation_subgroup_prevalence,
 representation_limitation,CASE WHEN actual_negative_count=0 OR actual_positive_count=0 THEN 'undefined rate' ELSE 'defined rates' END AS rate_status
 FROM records''',{'records':'ds.mitigation_records'},'Subgroup weighting is distinct from conditional harm and overall validation evidence')]
 if cid=='experiment_metric_logging':
  return [code(s,LOGGING,[('trial_setting=','Default setting; the call below supplies the explicit override.'),('revision =','Capture the actual revision in the intended working directory.'),('revision !=','Reject a mismatch before claiming artifact lineage.'),('params =','Log resolved values, code identity and the resolved local path.'),('recorded =','Look up the keyed run; metrics here are not full history.')]),table(s,'ds.execution_contract')]
 if cid=='training_randomness':
  return [query(s,'SELECT seed,baseline_result,candidate_result,candidate_result < baseline_result AS candidate_win FROM trials',{'trials':'ds.paired_trials'},'Matched completed trials; ties are not wins'),query(s,'''SELECT COUNT(*) AS completed_pair_count,SUM(CASE WHEN candidate_result < baseline_result THEN 1 ELSE 0 END) AS wins,
 AVG(CASE WHEN candidate_result < baseline_result THEN 1.0 ELSE 0.0 END) AS empirical_win_probability,
 AVG(baseline_result) AS baseline_mean,AVG(candidate_result) AS candidate_mean,
 SQRT(AVG(baseline_result*baseline_result)-AVG(baseline_result)*AVG(baseline_result)) AS baseline_std,
 SQRT(AVG(candidate_result*candidate_result)-AVG(candidate_result)*AVG(candidate_result)) AS candidate_std,ddof
 FROM trials CROSS JOIN execution WHERE baseline_result IS NOT NULL AND candidate_result IS NOT NULL GROUP BY ddof''',{'trials':'ds.paired_trials','execution':'ds.execution_contract'},'Completed-pair denominator and selected-result population summaries'),table(s,'ds.execution_contract')]
 if cid=='validation_regularization':
  common=['configuration_id','estimator','parameter_name','parameter_value','strength_direction','cohort_id']
  left=table(s,'ds.regularization_records',common+['training_TP','training_FP','training_FN','training_TN','training_expected_error_cost'])
  right=table(s,'ds.regularization_records',common+['TP','FP','FN','TN','actual_negative_count','actual_positive_count','FPR','FNR','expected_error_cost','operating_requirements_met'])
  return [{'type':'side_by_side','left':left,'right':right,'left_label':'Training expected cost','right_label':'Validation expected cost','takeaway':'Compare the same score interpretation; validation and eligibility select the setting.','lineage':lin(s,True)},selection(s,'ds.regularization_records','configuration_id',operating=['operating_requirements_met']),table(s,'ds.regularization_directions')]
 if cid=='bounded_hyperparameter_search':
  return [query(s,'''WITH bounded AS (
 SELECT t.*, e.default_search_budget,e.override_search_budget AS resolved_budget,
 (declared_order < override_search_budget) AS completed,
 TP+FN AS actual_positive_count,FP+TN AS actual_negative_count,
 CASE WHEN declared_order < override_search_budget THEN CAST(FP AS DOUBLE)/NULLIF(FP+TN,0) END AS FPR,
 CASE WHEN declared_order < override_search_budget THEN CAST(FN AS DOUBLE)/NULLIF(FN+TP,0) END AS FNR
 FROM trials t CROSS JOIN execution e
), inspected AS (
 SELECT b.*,a.deployment_negative_probability,a.deployment_positive_probability,a.cost_FP,a.cost_FN,a.expected_cost_bound,
 CASE WHEN completed THEN a.deployment_negative_probability*FPR*a.cost_FP+a.deployment_positive_probability*FNR*a.cost_FN END AS expected_error_cost
 FROM bounded b CROSS JOIN acceptance a
), eligible AS (
 SELECT *, ROW_NUMBER() OVER (ORDER BY expected_error_cost,declared_order) AS eligible_rank FROM inspected
 WHERE completed AND FPR IS NOT NULL AND FNR IS NOT NULL AND expected_error_cost <= expected_cost_bound AND operating_requirements_met
)
SELECT i.configuration_id,i.declared_order,i.configuration_json,i.cohort_id,i.default_search_budget,i.resolved_budget,i.completed,
 CASE WHEN i.completed THEN i.TP END AS TP,CASE WHEN i.completed THEN i.FP END AS FP,
 CASE WHEN i.completed THEN i.FN END AS FN,CASE WHEN i.completed THEN i.TN END AS TN,
 CASE WHEN i.completed THEN i.actual_negative_count END AS actual_negative_count,
 CASE WHEN i.completed THEN i.actual_positive_count END AS actual_positive_count,
 i.FPR,i.FNR,i.deployment_negative_probability,i.deployment_positive_probability,i.cost_FP,i.cost_FN,i.expected_error_cost,i.expected_cost_bound,
 CASE WHEN NOT i.completed THEN 'unexecuted: budget reached' WHEN i.FPR IS NULL OR i.FNR IS NULL THEN 'undefined rate' WHEN i.expected_error_cost > i.expected_cost_bound THEN 'predictive bound failed' WHEN NOT i.operating_requirements_met THEN 'operating requirement failed' ELSE 'eligible' END AS eligibility_reason,
 e.eligible_rank,e.eligible_rank=1 AS retained_selection FROM inspected i LEFT JOIN eligible e ON i.configuration_id=e.configuration_id ORDER BY i.declared_order''',{'trials':'ds.search_trials','execution':'ds.execution_contract','acceptance':'ds.acceptance_contract'},'Resolved budget, completed evidence and unexecuted configurations')]
 if cid=='model_risk_documentation':
  return [table(s,'ds.risk_policy_evidence'),table(s,'ds.access_grants'),table(s,'ds.aggregate_slice_evidence'),table(s,'ds.slice_summary')]
 if cid=='foundation_model_baseline_evaluation':
  mounts={'outputs':'ds.foundation_outputs','validation':'ds.validation_scores','acceptance':'ds.acceptance_contract'}
  aligned='SELECT v.observation_id,v.cohort_id,v.actual_label,f.output_kind,f.foundation_output,v.reference_output FROM validation v JOIN outputs f ON v.observation_id=f.observation_id AND v.cohort_id=f.cohort_id'
  counts=f'''WITH aligned AS ({aligned}), counts AS (
 SELECT 'foundation outputs' AS system,
 SUM(CASE WHEN actual_label={positive} AND foundation_output={positive} THEN 1 ELSE 0 END) AS TP,
 SUM(CASE WHEN actual_label={negative} AND foundation_output={positive} THEN 1 ELSE 0 END) AS FP,
 SUM(CASE WHEN actual_label={positive} AND foundation_output={negative} THEN 1 ELSE 0 END) AS FN,
 SUM(CASE WHEN actual_label={negative} AND foundation_output={negative} THEN 1 ELSE 0 END) AS TN FROM aligned
 UNION ALL
 SELECT 'reference outputs',
 SUM(CASE WHEN actual_label={positive} AND reference_output={positive} THEN 1 ELSE 0 END),
 SUM(CASE WHEN actual_label={negative} AND reference_output={positive} THEN 1 ELSE 0 END),
 SUM(CASE WHEN actual_label={positive} AND reference_output={negative} THEN 1 ELSE 0 END),
 SUM(CASE WHEN actual_label={negative} AND reference_output={negative} THEN 1 ELSE 0 END) FROM aligned
), rates AS (SELECT *, FP+TN AS actual_negative_count,FN+TP AS actual_positive_count,
 CAST(FP AS DOUBLE)/NULLIF(FP+TN,0) AS FPR,CAST(FN AS DOUBLE)/NULLIF(FN+TP,0) AS FNR FROM counts)
SELECT rates.*,a.deployment_negative_probability,a.deployment_positive_probability,a.cost_FP,a.cost_FN,
 {COST} AS expected_error_cost,a.expected_cost_bound,({COST}) <= a.expected_cost_bound AS predictive_requirement_met,a.operating_limit FROM rates CROSS JOIN acceptance a'''
  return [query(s,aligned,mounts,'Observation-aligned supplied outputs and reference'),query(s,counts,mounts,'Same labeled cohort, actual-class denominators and fixed predictive bound; operating evidence stays separate')]
 raise ValueError(cid)
