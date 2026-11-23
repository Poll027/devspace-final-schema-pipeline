import json,sys,re
from pathlib import Path
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox
B=Path('batches/final_batch_mle.region.validation_and_selection')
P=json.loads((B/'tile_plans.json').read_text()); S=json.loads((B/'screens.json').read_text()); G=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); R=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={b['context']['concept_id']:b for b in G['bundles']}; assets={a['asset_id']:a for a in R['assets']}
def rows(a):
 x=assets[a];return [dict(zip([c['name'] for c in x['columns']],r)) for r in x['rows']]
# All tabular values below are loaded from the registry; only pedagogical wording is authored.
Q={
'task_metric_selection':('What can precision, recall and prevalence from a validation confusion table establish?', 'Conditional outcome frequencies in that validation cohort, not calibration of individual scores.', 'Calibration of each individual probability score.', 'Recall conditions on predicted positives, while precision conditions on actual positives.'),
'model_acceptance_criteria':('Which acceptance contract preserves the declared decision inputs?', 'Compare deployment-weighted error cost with the predeclared bound; assess operating limits separately.', 'Choose deployment probabilities after observing which candidate they favor.', 'Treat passing the predictive cost bound as proof of meeting every operating limit.'),
'reference_baseline':('Which reference procedure keeps its statistics and evaluation populations distinct?', 'Fit on training targets, report training class proportions, freeze the rule and measure validation predictions against validation targets.', 'Use validation target prevalence to define the training reference rule.', 'Report training accuracy as the predeclared validation result.'),
'model_approach_decision':('A supplied alternative violates a precommitted operating limit. How should a fixed comparison treat it?', 'Exclude it before ranking eligible alternatives by the declared rule.', 'Select it whenever its predictive cost is the lowest, ignoring the operating failure.', 'Fit new alternatives and use protected-test results to repair its comparison evidence.'),
'sklearn_baseline_workflow':('Which validation procedure preserves training-fitted preprocessing?', 'Reuse the fitted preprocessing with observation-aligned validation inputs and labels.', 'Refit preprocessing using the validation targets before predicting validation observations.', 'Compare validation predictions against training labels instead of corresponding validation labels.'),
'decision_threshold_selection':('When an actual-class conditioning group is empty during threshold evaluation, what is defensible?', 'Keep that required rate undefined and do not treat it as passing eligibility.', 'Assign the missing rate zero and accept it as evidence of no errors.', 'Choose a new threshold by consulting protected-test outcomes.'),
'validation_candidate_comparison':('A record has lower cost but a different validation cohort. What does the fixed comparison permit?', 'Exclude the unmatched record; rank only matched records that satisfy every supplied limit.', 'Rank it first because cost alone overrides cohort identity.', 'Redefine the deployment probabilities to make it comparable.'),
'prediction_error_analysis':('What should a recurring validation failure pattern support?', 'A descriptive finding with an eligible denominator and comparable same-cohort evidence, not an untested cause.', 'A causal explanation established solely by the observed error association.', 'An error proportion with no retained eligible count.'),
'slice_evaluation':('Two predefined validation slices show different error proportions. Which report is bounded?', 'Retain both eligible counts and the declared spread divisor; describe an observed sample gap only.', 'Infer population-level disparity solely from the two sample proportions.', 'Discard the denominators because proportions alone establish representation.'),
'subgroup_risk_mitigation':('Which mitigation check distinguishes observed sampling from deployment weighting?', 'Check matched affected-segment and overall evidence under precommitted criteria; keep validation subgroup prevalence separate from deployment probability.', 'Set deployment subgroup probability equal to its validation sample share automatically.', 'Treat aggregate improvement as proof that every subgroup is suitable.'),
'experiment_metric_logging':('A retrieved run is associated with a different repository revision than the retained actual revision. What should happen?', 'Reject the artifact association despite a matching run ID.', 'Accept it because a matching run ID makes the revision irrelevant.', 'Replace the retained actual revision with the retrieved revision to erase the mismatch.'),
 'training_randomness':('What belongs in a bounded paired-seed report?', 'Completed matched pairs and their seeds, wins divided by completed pairs, and declared-divisor numeric summaries without universal replay claims.', 'Wins divided only by the winning pairs, omitting losses and ties.', 'A universal deterministic replay guarantee merely because random_state was set.'),
'validation_regularization':('Which setting decision avoids using training fit as the selection criterion?', 'Compare declared settings on fixed validation evidence and choose an eligible one by the predeclared criterion.', 'Choose the smallest training cost even if its validation cost is worse.', 'Consult protected-test outcomes to choose the regularization setting.'),
'bounded_hyperparameter_search':('How should an explicit search-budget keyword override be used?', 'Resolve it before iterating, execute only the bounded declared trials and retain actual validation results.', 'Run every configuration first and truncate only the reported results afterward.', 'Choose the budget after seeing protected-test outcomes.'),
'model_risk_documentation':('An existing policy permits identity A, while observed grants include A and B. What should the single record do?', 'Preserve A as the permitted scope and record B as an out-of-scope grant.', 'Expand the policy to A and B so the observed grants appear compliant.', 'Copy any exposed credential secret into the risk record as evidence.'),
'foundation_model_baseline_evaluation':('Which procedure supports a bounded supplied-output verdict?', 'Align the supplied foundation outputs and baseline to the same labeled validation observations and fixed acceptance requirements.', 'Use mismatched labeled cohorts because both systems predict the same task.', 'Fit a new candidate and tune it using protected-test observations during supplied-output evaluation.')}
F={
'task_metric_selection':['Cohort frequencies describe outcomes, not individual-score calibration.','Precision conditions on predicted positives; recall conditions on actual positives.'],
'model_acceptance_criteria':['Deployment probabilities and costs are fixed before comparing candidates.','Predictive acceptance and operating eligibility are separate conditions.'],
'reference_baseline':['Training class proportions must come from training targets, not validation targets.','The declared validation metric uses validation predictions and actual targets.'],
'model_approach_decision':['Precommitted operating limits determine eligibility before ranking.','Use supplied matched records without new fitting or protected-test selection.'],
'sklearn_baseline_workflow':['Validation uses training-fitted preprocessing, not a validation refit.','Predictions must be compared against corresponding validation labels.'],
'decision_threshold_selection':['An empty actual-class denominator yields an undefined rate, not zero.','Threshold selection uses validation evidence, not protected-test outcomes.'],
'validation_candidate_comparison':['Cohort matching and eligibility precede cost ranking.','Supplied deployment probabilities stay fixed across comparisons.'],
'prediction_error_analysis':['A descriptive failure association does not establish an untested cause.','An error proportion must retain its eligible conditioning population.'],
'slice_evaluation':['Observed sample differences alone do not establish population disparity.','Unequal eligible counts and representation limits remain relevant.'],
'subgroup_risk_mitigation':['Validation sample share is not automatically deployment population probability.','Aggregate improvement does not establish universal subgroup suitability.'],
'experiment_metric_logging':['The retained code revision must match before accepting an artifact association.','Changing the retained revision does not verify the actual intended repository revision.'],
 'training_randomness':['The denominator is all completed pairs, including losses and ties.','Controlling random sources does not guarantee every environment or computation is deterministic.'],
'validation_regularization':['Selection follows the fixed validation criterion rather than training score alone.','Protected-test observations cannot be used to choose settings.'],
'bounded_hyperparameter_search':['The resolved budget bounds actual execution, not merely reporting.','Budget resolution and selection use the fixed validation protocol, not protected-test results.'],
'model_risk_documentation':['Document grants outside existing permissions rather than expanding the scope.','Describe credential exposure by location or handling limitation without reproducing secrets.'],
'foundation_model_baseline_evaluation':['Both systems must be compared against the same task-specific labeled observations.','Supplied-output evaluation does not fit or tune new models and excludes protected-test evidence.']}
# Scaffold CSV readers are supplied unchanged and are not learner-authored syntax.
reader='''import csv
import json
def supplied_rows(path):
    with open(path) as f:
        raw = list(csv.DictReader(f))
    def convert(v):
        if v == '': return None
        if v.lower() == 'true': return True
        if v.lower() == 'false': return False
        try: return float(v) if '.' in v or 'e' in v.lower() else int(v)
        except ValueError: return v
    return [{k: convert(v) for k,v in r.items()} for r in raw]
'''
def load(*names):return reader+''.join(f"{n} = supplied_rows('{n}.csv')\n" for n in names)
contract=rows('ds.acceptance_contract')[0]
# A single rate/cost block, specialised to the taught syntax of each function.
def count_code(actual='y',pred='pred',indent='    ',counter='np.sum'):
 return '\n'.join(indent+l for l in [f'TP = {counter}(({actual} == 1) & ({pred} == 1))',f'FP = {counter}(({actual} == 0) & ({pred} == 1))',f'FN = {counter}(({actual} == 1) & ({pred} == 0))',f'TN = {counter}(({actual} == 0) & ({pred} == 0))','if FP + TN == 0:','    FPR = None','else:','    FPR = FP / (FP + TN)','if FN + TP == 0:','    FNR = None','else:','    FNR = FN / (FN + TP)','if FPR == None or FNR == None:','    cost = None','else:','    cost = p0 * FPR * cfp + p1 * FNR * cfn'])+'\n'
code_tasks={}
def task(name,scaf,body,tail,prompt,mounts,exprs,packages=['numpy']):
 code_tasks[name]={'scaf':scaf,'body':body,'tail':tail,'prompt':prompt,'mounts':mounts,'exprs':exprs,'packages':packages}
params=f"p0 = {json.dumps(contract['deployment_negative_probability'])}\np1 = {json.dumps(contract['deployment_positive_probability'])}\ncfp = {json.dumps(contract['cost_FP'])}\ncfn = {json.dumps(contract['cost_FN'])}\nbound = {json.dumps(contract['expected_cost_bound'])}\n"
# Acceptance formula practice is a Python contract calculation (planned runtime Python).
a=rows('ds.acceptance_terms');print('acceptance terms',a)
scaf=load('acceptance_terms','acceptance_contract')+params
body='''def acceptance(terms, requirements):
    negative = terms[0]
    positive = terms[1]
    FPR = negative['conditional_error_rate']
    FNR = positive['conditional_error_rate']
    cost = requirements['deployment_negative_probability'] * FPR * requirements['cost_FP'] + requirements['deployment_positive_probability'] * FNR * requirements['cost_FN']
    return {'FPR': FPR, 'FNR': FNR, 'expected_cost': cost, 'quality_pass': cost <= requirements['expected_cost_bound'], 'operating_limit': requirements['operating_limit'], 'operating_eligibility': 'unresolved: no numerical operating limit supplied', 'denominators': 'FPR: actual negatives; FNR: actual positives; empty conditioning group unresolved', 'contract': requirements}
'''
task('model_acceptance_criteria',scaf,body,"result = acceptance(acceptance_terms, acceptance_contract[0])\n",'Complete acceptance(terms, requirements), using the supplied fixed contract before any candidate comparison. Return result with FPR, FNR, expected_cost, quality_pass, operating_limit, operating_eligibility, denominators and contract. Do not invent an operating limit: leave overall operating eligibility unresolved when no limit is supplied. State both actual-class denominators and that an empty group is unresolved. Preserve every contract field.', ['ds.acceptance_terms','ds.acceptance_contract'],['result'],[])
# Reference baseline: true training-only DummyClassifier, including edge cases.
scaf=load('reference_train','orders_validation')+params
body='''import numpy as np
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
def reference(X_train, y_train, X_validation, y, p0, p1, cfp, cfn):
    estimator = DummyClassifier(strategy="most_frequent")
    estimator.fit(X_train, y_train)
    pred = estimator.predict(X_validation)
    training_positive = np.mean(y_train)
    training_negative = 1 - training_positive
'''+count_code()+'''    return {'training_positive': training_positive, 'training_negative': training_negative, 'rule': 'training most_frequent, frozen', 'predictions': pred, 'accuracy': accuracy_score(y, pred), 'FPR': FPR, 'FNR': FNR, 'expected_cost': cost}
'''
tail="X_train = np.array([[r['feature_1']] for r in reference_train])\ny_train = np.array([r['y_train'] for r in reference_train])\nX_validation = np.array([[r['feature_1']] for r in orders_validation])\ny = np.array([r['y_validation'] for r in orders_validation])\nresult = reference(X_train, y_train, X_validation, y, p0, p1, cfp, cfn)\nempty_negative = reference(X_train, y_train, X_validation[:2], np.array([1,1]), p0,p1,cfp,cfn)\nempty_positive = reference(X_train, y_train, X_validation[:2], np.array([0,0]), p0,p1,cfp,cfn)\n"
task('reference_baseline',scaf,body,tail,'Write the imports and reference function. Fit DummyClassifier(strategy="most_frequent") only on training inputs, freeze it and evaluate corresponding validation labels. Return training_positive, training_negative, rule ("training most_frequent, frozen"), predictions, accuracy, FPR, FNR and expected_cost. Undefined required rates and costs are None. Supplied calls also exercise empty actual-class groups. Do not access protected-test observations. Results are in result, empty_negative and empty_positive.', ['ds.reference_train','ds.orders_validation'],['result','empty_negative','empty_positive'],['numpy','scikit-learn'])
# Scikit-learn baseline.
scaf=load('orders_train','orders_validation')+params
body='''import numpy as np
from sklearn.linear_model import LogisticRegression
def baseline(X_train, y_train, X_validation, y, p0, p1, cfp, cfn):
    assert X_train.ndim == 2
    assert y_train.ndim == 1
    assert X_train.shape[0] == y_train.shape[0]
    assert X_validation.shape[0] == y.shape[0]
    estimator = LogisticRegression(random_state=0)
    estimator.fit(X_train, y_train)
    pred = estimator.predict(X_validation)
'''+count_code()+'''    return {'training_shape': X_train.shape, 'target_shape': y_train.shape, 'predictions': pred, 'FPR': FPR, 'FNR': FNR, 'expected_cost': cost}
'''
tail="X_train = np.array([[r['feature_1'], r['feature_2']] for r in orders_train])\ny_train = np.array([r['y_train'] for r in orders_train])\nX_validation = np.array([[r['feature_1'],r['feature_2']] for r in orders_validation])\ny = np.array([r['y_validation'] for r in orders_validation])\nresult = baseline(X_train,y_train,X_validation,y,p0,p1,cfp,cfn)\nempty_negative = baseline(X_train,y_train,X_validation[:2],np.array([1,1]),p0,p1,cfp,cfn)\nempty_positive = baseline(X_train,y_train,X_validation[:2],np.array([0,0]),p0,p1,cfp,cfn)\n"
task('sklearn_baseline_workflow',scaf,body,tail,'Write imports and baseline(X_train, y_train, X_validation, y, p0, p1, cfp, cfn). Check feature/target dimensions and observation alignment, fit LogisticRegression(random_state=0) on training only and predict validation. Return training_shape, target_shape, predictions, FPR, FNR, expected_cost. Guard both actual-class denominators; use None for undefined rates/costs. Do not refit preprocessing on validation or consult protected test. Supplied result and two empty-class calls are graded.', ['ds.orders_train','ds.orders_validation'],['result','empty_negative','empty_positive'],['numpy','scikit-learn'])
# Threshold selection: supplied interfaces retain representation and eligibility.
scaf=load('validation_scores','thresholds')+params+'''def supplied_eligible(cost, FPR, FNR):
    return cost is not None and cost <= bound

def supplied_retain(threshold, representation, records):
    return {'threshold': threshold, 'score_representation': representation, 'validation_records': records}
'''
body='''import numpy as np
def thresholds_evaluate(scores, y, candidates, p0, p1, cfp, cfn):
    scores = np.asarray(scores)
    y = np.asarray(y)
    records = []
    selected = None
    best = None
    for threshold in candidates:
        pred = scores >= threshold
'''+count_code(indent='        ',counter='np.count_nonzero')+'''        eligible = supplied_eligible(cost, FPR, FNR)
        record = {'threshold': threshold, 'TP': TP, 'FP': FP, 'FN': FN, 'TN': TN, 'FPR': FPR, 'FNR': FNR, 'expected_cost': cost, 'eligible': eligible}
        records = records + [record]
        if eligible:
            if best == None or cost < best:
                best = cost
                selected = threshold
    return supplied_retain(selected, 'probability_score; predicted positive when score >= threshold', records)
'''
tail="scores = [r['score'] for r in validation_scores]\ny = [r['actual_label'] for r in validation_scores]\ncandidates = [r['threshold'] for r in thresholds]\nresult = thresholds_evaluate(scores,y,candidates,p0,p1,cfp,cfn)\nempty = thresholds_evaluate(scores[:2],[1,1],candidates,p0,p1,cfp,cfn)\n"
task('decision_threshold_selection',scaf,body,tail,'Implement thresholds_evaluate and the required NumPy import. Evaluate every supplied threshold with predicted-positive rule score >= threshold. Return through supplied_retain: threshold (None when no eligible candidate), score_representation exactly "probability_score; predicted positive when score >= threshold", validation_records with threshold, TP, FP, FN, TN, FPR, FNR, expected_cost and eligible. Use supplied eligibility and minimum cost, retaining first declared threshold on a tie. Guard actual-class denominators. result and an empty-actual-negative call are graded; retain the frozen validation record and do not consult protected test.', ['ds.validation_scores','ds.thresholds'],['result','empty'])
# Error analysis and slice evaluation.
scaf=load('slice_observations')
body='''import numpy as np
def error_analysis(eligible, long_distance, error, loss, reference_error, reference_loss):
    mask = eligible & long_distance
    count = np.count_nonzero(mask)
    errors = np.count_nonzero(error[mask])
    reference_errors = np.count_nonzero(reference_error[mask])
    return {'eligible_count': count, 'error_count': errors, 'error_probability': errors/count, 'loss_mean': np.mean(loss[mask]), 'loss_std': np.std(loss[mask], ddof=0), 'reference_error_count': reference_errors, 'reference_error_probability': reference_errors/count, 'reference_loss_mean': np.mean(reference_loss[mask]), 'reference_loss_std': np.std(reference_loss[mask], ddof=0), 'finding': 'Long-distance supplied failures recur in this predefined eligible group; comparison is descriptive same-cohort evidence, not an established cause.'}
'''
tail="eligible = np.array([r['eligible'] for r in slice_observations])\nlong_distance = np.array([r['long_distance'] for r in slice_observations])\nerror = np.array([r['error'] for r in slice_observations])\nloss = np.array([r['loss'] for r in slice_observations])\nreference_error = np.array([r['reference_error'] for r in slice_observations])\nreference_loss = np.array([r['reference_loss'] for r in slice_observations])\nresult = error_analysis(eligible,long_distance,error,loss,reference_error,reference_loss)\n"
task('prediction_error_analysis',scaf,body,tail,'Write error_analysis and import NumPy. Restrict to eligible & long_distance. Return eligible_count, error_count, error_probability, loss_mean, loss_std with ddof=0, reference_error_count, reference_error_probability, reference_loss_mean, reference_loss_std from the same selected observations, and finding: "Long-distance supplied failures recur in this predefined eligible group; comparison is descriptive same-cohort evidence, not an established cause." The supplied fixture has a nonempty group; do not claim a cause.', ['ds.slice_observations'],['result'])
body='''import numpy as np
def slices(zone, eligible, error, loss):
    report = {}
    for label in ['A','B']:
        mask = (zone == label) & eligible
        count = np.sum(mask)
        errors = np.sum(error[mask])
        report[label] = {'eligible_count': count, 'error_count': errors, 'error_probability': errors/count, 'loss_mean': np.mean(loss[mask]), 'loss_std': np.std(loss[mask], ddof=0)}
    return {'slices': report, 'error_gap_B_minus_A': report['B']['error_probability'] - report['A']['error_probability'], 'limitation': 'Observed validation-slice gap only; unequal denominators retained; population-level disparity not established.'}
'''
tail="zone = np.asarray([r['zone'] for r in slice_observations])\neligible = np.asarray([r['eligible'] for r in slice_observations])\nerror = np.asarray([r['error'] for r in slice_observations])\nloss = np.asarray([r['loss'] for r in slice_observations])\nresult = slices(zone,eligible,error,loss)\n"
task('slice_evaluation',scaf,body,tail,'Write the NumPy import and slices(zone, eligible, error, loss). For predefined A and B return slices keyed by label, with eligible_count, error_count, error_probability, loss_mean, loss_std (ddof=0); also error_gap_B_minus_A and limitation exactly "Observed validation-slice gap only; unequal denominators retained; population-level disparity not established." Keep the same-cohort conditioning populations and describe only the observed sample gap.', ['ds.slice_observations'],['result'])
# Paired trials use the authorized supplied adapter, not new fitting.
scaf=load('paired_trials')+'''def supplied_pair(seed, split_random_state, estimator_random_state):
    if split_random_state != seed or estimator_random_state != seed:
        raise ValueError('both random sources must match seed')
    return next(r for r in paired_trials if r['seed'] == seed)
'''
body='''import numpy as np
def paired(declared_seed_list):
    records = []
    selected_results = []
    wins = 0
    for seed in declared_seed_list:
        record = supplied_pair(seed, split_random_state=seed, estimator_random_state=seed)
        records.append(record)
        selected_results.append(record['candidate_result'])
        if record['candidate_result'] < record['baseline_result']:
            wins = wins + 1
    count = len(records)
    return {'records': records, 'completed_pairs': count, 'wins': wins, 'win_probability': wins/count, 'candidate_mean': np.mean(selected_results), 'candidate_std': np.std(selected_results, ddof=0), 'limitation': 'Split and estimator randomness controlled; universal deterministic replay not established.'}
'''
tail="declared_seed_list = [r['seed'] for r in paired_trials]\nresult = paired(declared_seed_list)\n"
task('training_randomness',scaf,body,tail,'Write paired(declared_seed_list) and the NumPy import. Call supplied_pair for every declared seed with both split_random_state and estimator_random_state equal to that seed. Lower cost wins; ties are not wins. Return records with only seed, baseline_result and candidate_result; completed_pairs, wins, win_probability, candidate_mean, candidate_std (ddof=0) and limitation exactly "Split and estimator randomness controlled; universal deterministic replay not established."', ['ds.paired_trials'],['result'])
# Regularization uses fixed supplied training/validation records and existing scaffolding.
scaf=load('regularization_records')+params+'''def supplied_result(setting):
    return setting
'''
body='''import numpy as np
def regularization(settings, p0, p1, cfp, cfn, bound):
    records = []
    selected = None
    best = None
    for setting in settings:
        r = supplied_result(setting)
        TP = r['TP']
        FP = r['FP']
        FN = r['FN']
        TN = r['TN']
        if FP + TN == 0:
            FPR = None
        else:
            FPR = FP/(FP+TN)
        if FN + TP == 0:
            FNR = None
        else:
            FNR = FN/(FN+TP)
        if FPR == None or FNR == None:
            cost = None
        else:
            cost = p0*FPR*cfp+p1*FNR*cfn
        eligible = cost != None and cost <= bound and r['operating_requirements_met']
        record = {'configuration_id': r['configuration_id'], 'C': r['parameter_value'], 'training_expected_error_cost': r['training_expected_error_cost'], 'validation_expected_error_cost': cost, 'FPR': FPR, 'FNR': FNR, 'eligible': eligible}
        records = records + [record]
        if eligible:
            if best == None or cost < best:
                best = cost
                selected = r['configuration_id']
    return {'records': records, 'selected': selected, 'parameter_direction': 'LogisticRegression C is inverse regularization strength; larger Ridge alpha increases penalty', 'boundary': 'Fixed training-fitted preprocessing and validation assumptions; no protected-test access'}
'''
task('validation_regularization',scaf,body,"result = regularization(regularization_records,p0,p1,cfp,cfn,bound)\n",'Within the existing supplied workflow, write regularization(settings,p0,p1,cfp,cfn,bound) and required imports. For each declared setting use supplied_result(setting), retain configuration_id, C, training_expected_error_cost and recompute validation_expected_error_cost, FPR, FNR, eligible. Preserve the fixed training-fitted protocol. Return records, selected (minimum eligible validation cost; first on ties; None if none), parameter_direction exactly "LogisticRegression C is inverse regularization strength; larger Ridge alpha increases penalty", and boundary exactly "Fixed training-fitted preprocessing and validation assumptions; no protected-test access". Guard undefined rates and do not choose from training scores alone.', ['ds.regularization_records'],['result'])
# Bounded search with default and keyword override; configurations parsed by supplied scaffold.
scaf=load('search_trials','execution_contract')+params+'''configs = [json.loads(r['configuration_json']) for r in search_trials]
def supplied_trial(configuration):
    return next(r for r in search_trials if json.loads(r['configuration_json']) == configuration)
'''
body='''def search(configurations, p0, p1, cfp, cfn, bound, budget=3):
    records = []
    selected = None
    best = None
    for configuration in configurations[:budget]:
        r = supplied_trial(configuration)
        FP = r['FP']
        TN = r['TN']
        FN = r['FN']
        TP = r['TP']
        if FP + TN == 0:
            FPR = None
        else:
            FPR = FP/(FP+TN)
        if FN + TP == 0:
            FNR = None
        else:
            FNR = FN/(FN+TP)
        if FPR == None or FNR == None:
            cost = None
        else:
            cost = p0*FPR*cfp+p1*FNR*cfn
        eligible = cost != None and cost <= bound and r['operating_requirements_met']
        records.append({'configuration': configuration, 'cohort_id': r['cohort_id'], 'TP': TP, 'FP': FP, 'FN': FN, 'TN': TN, 'FPR': FPR, 'FNR': FNR, 'expected_cost': cost, 'eligible': eligible})
        if eligible:
            if best == None or cost < best:
                best = cost
                selected = configuration
    return {'resolved_budget': budget, 'completed_trials': len(records), 'records': records, 'selected_configuration': selected}
'''
task('bounded_hyperparameter_search',scaf,body,"result = search(configs,p0,p1,cfp,cfn,bound,budget=execution_contract[0]['override_search_budget'])\ndefault_result = search(configs,p0,p1,cfp,cfn,bound)\n",'Write search(configurations,p0,p1,cfp,cfn,bound,budget=3). Resolve the explicit keyword override before iterating configurations[:budget]; execute supplied_trial for each permitted configuration only. Return resolved_budget, completed_trials, records (configuration, cohort_id, TP, FP, FN, TN, FPR, FNR, expected_cost, eligible), selected_configuration. Required undefined rates/costs are None and ineligible; minimum eligible cost wins, ties retain declared order. The supplied calls grade both the default and the keyword override. No protected-test access.', ['ds.search_trials','ds.execution_contract'],['result','default_result'],[])
# Foundation outputs: strict alignment, one bounded verdict, no fit or ranking.
scaf=load('foundation_outputs','validation_scores')+params
body='''import numpy as np
def evaluate(ids, output_ids, y, outputs, reference, p0,p1,cfp,cfn,bound):
    ids = np.asarray(ids)
    output_ids = np.asarray(output_ids)
    y = np.asarray(y)
    pred = np.asarray(outputs)
    reference = np.asarray(reference)
    if not np.array_equal(ids, output_ids):
        raise ValueError('observation mismatch')
    if y.shape != pred.shape or y.shape != reference.shape:
        raise ValueError('shape mismatch')
'''+count_code()+'''    accuracy = np.sum(y == pred)/np.sum((y == 0) | (y == 1))
    baseline_accuracy = np.sum(y == reference)/np.sum((y == 0) | (y == 1))
    baseline_FP = np.sum((y == 0) & (reference == 1))
    baseline_TN = np.sum((y == 0) & (reference == 0))
    baseline_FN = np.sum((y == 1) & (reference == 0))
    baseline_TP = np.sum((y == 1) & (reference == 1))
    if baseline_FP + baseline_TN == 0 or baseline_FN + baseline_TP == 0:
        baseline_cost = None
    else:
        baseline_cost = p0*baseline_FP/(baseline_FP+baseline_TN)*cfp+p1*baseline_FN/(baseline_FN+baseline_TP)*cfn
    if cost == None:
        verdict = 'unresolved'
    elif cost <= bound:
        verdict = 'predictive quality accepted'
    else:
        verdict = 'predictive quality rejected'
    return {'aligned': True, 'accuracy': accuracy, 'baseline_accuracy': baseline_accuracy, 'TP': TP, 'FP': FP, 'FN': FN, 'TN': TN, 'FPR': FPR, 'FNR': FNR, 'expected_cost': cost, 'baseline_expected_cost': baseline_cost, 'verdict': verdict, 'limitations': 'Supplied validation cohort only; operating eligibility separate; no universal suitability or protected-test evidence'}
'''
tail="ids = [r['observation_id'] for r in validation_scores]\noutput_ids = [r['observation_id'] for r in foundation_outputs]\ny = [r['actual_label'] for r in validation_scores]\noutputs = [r['foundation_output'] for r in foundation_outputs]\nreference = [r['reference_output'] for r in validation_scores]\nresult = evaluate(ids,output_ids,y,outputs,reference,p0,p1,cfp,cfn,bound)\nempty = evaluate(ids[:2],output_ids[:2],[1,1],outputs[:2],reference[:2],p0,p1,cfp,cfn,bound)\ndef supplied_mismatch_check():\n    try:\n        evaluate(ids,output_ids[::-1],y,outputs,reference,p0,p1,cfp,cfn,bound)\n    except ValueError:\n        return True\n    return False\nmismatch_rejected = supplied_mismatch_check()\n"
task('foundation_model_baseline_evaluation',scaf,body,tail,'Write evaluate and NumPy import. Verify exact identifier alignment and corresponding shapes, raising ValueError on mismatches. Evaluate only the supplied foundation-model outputs, without fitting or ranking approaches. Return aligned, accuracy, baseline_accuracy, TP, FP, FN, TN, FPR, FNR, expected_cost, baseline_expected_cost, verdict and limitations. Both accuracies and costs use the same validation labels and fixed inputs. Use None for undefined required rates/costs; verdict is "unresolved", "predictive quality accepted" when cost <= bound, otherwise "predictive quality rejected". limitations is "Supplied validation cohort only; operating eligibility separate; no universal suitability or protected-test evidence". result, empty-class behavior and identifier mismatch rejection are graded.', ['ds.foundation_outputs','ds.validation_scores'],['[result, mismatch_rejected]','empty'])
# Inspect-and-judge is intentionally embedded text, with no data source/asset_ref.
logging_items=[
('override','def log_trial(trial_setting=10):\n    params = {"trial_setting": trial_setting}\n    with mlflow.start_run() as run:\n        mlflow.log_params(params)\n        mlflow.log_metric(metric_name, validation_value)\n        mlflow.log_artifact(local_path)\n    return run.info.run_id\nrun_id = log_trial(trial_setting=20)','valid','The resolved override is logged in the parameter dictionary along with supplied metric and diagnostic artifact.'),
('wrong_default','def log_trial(trial_setting=10):\n    params = {"trial_setting": 10}\n    mlflow.log_params(params)\nlog_trial(trial_setting=20)','invalid','The dictionary ignores the resolved keyword override and records the default instead.'),
('association','lookup = {"run_id": run_id, "repository_directory": directory, "local_artifact_path": absolute_path, "code_revision": actual_revision}\nrecorded = mlflow.get_run(lookup["run_id"])\nif intended_revision != lookup["code_revision"]:\n    raise ValueError("revision mismatch")\nartifact_uri = recorded.info.artifact_uri','valid','Retrieval is keyed to the retained run and a mismatching revision is rejected.'),
('wrong_revision','recorded = mlflow.get_run(run_id)\nif intended_revision != actual_revision:\n    artifact_uri = recorded.info.artifact_uri  # accept anyway','invalid','The mismatching revision is accepted instead of rejected.'),
('revision_capture',"directory = os.getcwd()\ncompleted = subprocess.run(['git', 'rev-parse', '--verify', 'HEAD'], cwd=directory, capture_output=True, text=True, check=True)\nactual_revision = completed.stdout.strip()",'valid','The actual repository directory and captured Git revision are retained, rather than guessed.')]
exec((B/'scope_code_tasks.py').read_text())
trial_contract=rows('ds.execution_contract')[0]
logging_items=[(id,txt.replace('=10','=__DEFAULT__').replace('=20','=__OVERRIDE__').replace('=__DEFAULT__','='+str(trial_contract['default_trial_setting'])).replace('=__OVERRIDE__','='+str(trial_contract['override_trial_setting'])),key,fb) for id,txt,key,fb in logging_items]
# Build all planned entries, and only those entries.
O={k:P[k] for k in ['schema_version','path_id','batch_id']};O['kind']='interactions_part';O['tiles']=[]
code_ix=[]; formula_ix=[]
for t in P['tiles']:
 rem=next(x for x in S['tiles'] if x['tile_id']==t['tile_id']).get('remediation_steps',[])
 out={'tile_id':t['tile_id'],'interactions':[]};O['tiles'].append(out)
 steps=[s for s in t['steps'] if s['type'] in ['check','hands_on']]
 for idx,s in enumerate(steps):
  cid=s['concept_ids'][0];name=cid.split('.',1)[1];b=bundles[cid]
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':('intro' if idx==0 else 'stretch' if idx==len(steps)-1 else 'core'),'grading_mode':'client','standalone':False,'anchors':s['anchors'],'measures':[]}
  for anchor in s['anchors']:
   if '#assessment:' in anchor:
    capability=anchor.split('#assessment:')[1];a=next(a for a in b['assessment_anchors'] if a['capability']==capability);ix['measures'].append({'concept_id':cid,'capability':capability,'fact_ids':a['fact_ids']})
  ix['feedback']={'correct':{'message':'The response preserves the stated conditioning populations, fixed inputs and evidence boundaries.'},'incorrect':{'message':'Recheck the fixed contract and distinguish observed validation evidence from unsupported claims.'},'hints':['Identify the population each quantity conditions on.','Keep declared decision inputs and evidence boundaries unchanged.']}
  if not any(e['interaction']['measures'] and any(m['concept_id']==cid for m in e['interaction']['measures']) for e in out['interactions']):
   r=next((r for r in rem if cid in r['concept_ids']),None)
   if r:ix['feedback']['remediation_step_id']=r['step_id']
  if ix['type']=='choice':
   prompt,*options=Q[name];ix['public']={'prompt':prompt,'options':[{'option_id':f'o{i+1}','text':text} for i,text in enumerate(options)],'selection':'single','shuffle':True}
   ix['grading']={'correct_option_ids':['o1'],'option_feedback':{'o1':{'message':options[0]},**{f'o{i+2}':{'message':v} for i,v in enumerate(F[name])}}}
  elif ix['type']=='code_exercise':
   z=code_tasks[name]; z['scaf']='exec('+repr(z['scaf'])+')\n';live=b['practice_anchor'].get('live_code')
   constraints={k:live[k] for k in ['allowed_syntax','blocked_syntax']} if live else {'allowed_syntax':['def','return','variable assignment','{key: value} dictionary literal','d[key] lookup and assignment','int, float, str and bool literals','+ - * / // % **','comparison operators'], 'blocked_syntax':[]}
   starter=z['scaf']+'\n# Write required imports and the requested function here.\n'+z['tail']
   solution=z['scaf']+'\n'+z['body']+'\n'+z['tail']
   mounts=[{'asset_id':a,'mount_path':a[3:]+'.csv'} for a in z['mounts']]
   ix['public']={'prompt':z['prompt'],'runtime':{'kind':'python','version':sandbox.RUNTIMES['python']['version'],'packages':z['packages']},'workspace':{'files':[{'path':'main.py','role':'editable','language':'python','content':starter}],'entry':'main.py','asset_mounts':mounts},'constraints':constraints}
   ix['grading']={'solution_files':[{'path':'main.py','content':solution}],'tests':[{'test_id':f't{i+1}','kind':'value_equals','spec':{'expr':expr,'expected':None,'tolerance':1e-9},'message_on_fail':'Check the requested fields against the fixed supplied inputs.'} for i,expr in enumerate(z['exprs'])]};code_ix.append(ix)
  elif ix['type']=='classify':
   ix['public']={'prompt':'Inspect the supplied MLflow fragments within an existing authorized setup. Treat each fragment as the specified local operation: classify whether it preserves the resolved setting, same-run lookup and revision/artifact association contract. All unspecified paths and metric inputs are already authorized.','buckets':[{'bucket_id':'valid','label':'Preserves the stated local contract'},{'bucket_id':'invalid','label':'Violates the stated local contract'}],'items':[{'item_id':id,'text':txt} for id,txt,key,fb in logging_items]}
   ix['grading']={'assignments':{id:key for id,txt,key,fb in logging_items},'item_feedback':{id:{'message':fb} for id,txt,key,fb in logging_items}}
  elif ix['type']=='external_proof':
   policies=rows('ds.risk_policy_evidence');grants=rows('ds.access_grants');summary=rows('ds.slice_summary')
   instruction='Write one risk record preserving existing policy, without expanding permissions or reproducing secrets. Existing policy / supplied observation / recording constraint:\n'+'\n'.join(r['field']+': '+r['existing_policy']+' / '+r['supplied_observation']+' / '+r['recording_constraint'] for r in policies)
   instruction += '\nObserved grants: '+ '; '.join(r['identity']+' permitted='+str(r['policy_permitted'])+' observed='+str(r['observed_grant']) for r in grants)
   instruction += '\nValidation sample: '+ '; '.join(r['slice']+' errors='+str(r['error_count'])+'/'+str(r['eligible_count']) for r in summary if r['slice'] in ['A','B'])
   instruction += '\nSame-cohort overall evidence: '+ '; '.join(r['system']+' errors='+str(r['error_count'])+'/'+str(r['eligible_count'])+' ('+r['cohort_id']+')' for r in rows('ds.aggregate_slice_evidence'))
   if len(instruction)>1500:
    instruction='Write one risk record preserving every existing policy field, without expanding permissions or copying secrets.\n'+'\n'.join(r['field']+': policy='+r['existing_policy']+'; evidence='+r['supplied_observation'] for r in policies)+'\nGrants: '+ '; '.join(r['identity']+' permitted='+str(r['policy_permitted'])+' observed='+str(r['observed_grant']) for r in grants)+'\nSample: '+ '; '.join(r['slice']+' errors='+str(r['error_count'])+'/'+str(r['eligible_count']) for r in summary if r['slice'] in ['A','B'])+'; representation beyond supplied sample unresolved.'

   criteria=['Preserve all existing policy fields and permitted identity scope; identify every observed out-of-scope grant.','Record the redacted credential location and handling limitation without copying a secret value.','Retain the supplied order-task/cohort limits and foreseeable misuse case.','Cite matched segment sample evidence, denominators and representation limitation; do not infer universal suitability from aggregate improvement.']
   ix['public']={'instruction':instruction,'evidence_kinds':['text','file'],'checklist':criteria};ix['grading']={'mode':'manual','rubric':[{'criterion':c,'weight':1} for c in criteria]}
  elif ix['type']=='formula_entry':
   # One target cell is a compact auditable report. Numerical fields are formulas, not literals.
   if name=='task_metric_selection':
    aid='ds.confusion_counts';formula='="precision="&D2/(D2+D3)&"; recall="&D2/(D2+D4)&"; prevalence="&(D2+D4)/SUM(D2:D5)&"; metric=recall because missed late orders carry greater consequence; precision=P(actual positive|predicted positive); recall=P(predicted positive|actual positive); cohort frequencies do not establish individual-score calibration"'
    prompt='In F1 enter a formula-generated text report with precision, recall and prevalence from count column D (TP row 2, FP row 3, FN row 4, TN row 5). Format as precision=<value>; recall=<value>; prevalence=<value>; metric=recall because missed late orders carry greater consequence; precision=P(actual positive|predicted positive); recall=P(predicted positive|actual positive); cohort frequencies do not establish individual-score calibration. Use cell references for all numeric values.'
   else:
    aid={'model_approach_decision':'ds.approach_records','validation_candidate_comparison':'ds.candidate_records','subgroup_risk_mitigation':'ds.mitigation_records'}[name]
    cols=[c['name'] for c in assets[aid]['columns']]
    def col(n):
     i=cols.index(n)+1;v=''
     while i:i,j=divmod(i-1,26);v=chr(65+j)+v
     return v
    def cell(n,r):return col(n)+str(r)
    if name!='subgroup_risk_mitigation':
     bits=[];costs={};eligible={}
     for r in range(2,len(assets[aid]['rows'])+2):
      fp,tn,fn,tp=[cell(n,r) for n in ['FP','TN','FN','TP']];fpr=f'{fp}/({fp}+{tn})';fnr=f'{fn}/({fn}+{tp})';cost=f"{contract['deployment_negative_probability']}*({fpr})*{contract['cost_FP']}+{contract['deployment_positive_probability']}*({fnr})*{contract['cost_FN']}";costs[r]=cost
      limits=[cell(n,r) for n in ['latency_requirement_met','scale_requirement_met','training_cost_requirement_met','serving_cost_requirement_met','maintenance_requirement_met','deployment_compatibility_met']]
      eligible[r]=f'AND({fp}+{tn}>0,{fn}+{tp}>0,{cell("cohort_id",r)}="orders_100",({cost})<={contract["expected_cost_bound"]},'+','.join(limits)+')'
      bits += [f'{cell(cols[0],r)}&": FPR="&IF({fp}+{tn}=0,"undefined",{fpr})&", FNR="&IF({fn}+{tp}=0,"undefined",{fnr})&", cost="&IF(OR({fp}+{tn}=0,{fn}+{tp}=0),"undefined",{cost})&", eligible="&IF({eligible[r]},"yes","no")']
     best='"no selection"'
     # Compare eligible costs without replacing undefined rates by zero.
     for r in reversed(range(2,len(assets[aid]['rows'])+2)):
      tests=[f'OR(NOT({eligible[j]}),({costs[r]})'+('<=' if r<j else '<')+f'({costs[j]}))' for j in costs if j!=r]
      best=f'IF(AND({eligible[r]},'+','.join(tests)+f'),{cell(cols[0],r)},{best})'
     suffix='; matched counts and denominators retained; fixed deployment probabilities '+str(contract['deployment_negative_probability'])+' and '+str(contract['deployment_positive_probability'])+' and costs '+str(contract['cost_FP'])+' and '+str(contract['cost_FN'])+'; exclude unmatched cohorts or failed supplied limits; frozen validation-only selection, no new fitting or protected-test evidence'
     if name=='model_approach_decision':suffix+='; custom classical and neural alternatives leave task-model and infrastructure maintenance with owner; managed service supplies training or hosting infrastructure but owner retains task-model choices'
     formula='='+('&"; "&'.join(bits))+ '&"; selected="&'+best+'&'+json.dumps(suffix)
     prompt='In '+ 'AA1'+' enter one formula-generated comparison report. For every record retain its identity, calculate FPR=FP/(FP+TN), FNR=FN/(FN+TP), mark empty groups undefined and compute deployment-weighted cost with the fixed probabilities/costs '+json.dumps({k:contract[k] for k in ['deployment_negative_probability','deployment_positive_probability','cost_FP','cost_FN','expected_cost_bound']})+'. Evaluate cohort_id="orders_100", the cost bound and every supplied operating predicate separately before selecting the minimum-cost eligible identity (first declared on a tie; no selection if none). Use the exact format and bounded rationale shown in the reference reporting contract: '+suffix+'. Each row format: <identity>: FPR=<value>, FNR=<value>, cost=<value>, eligible=yes/no; end with selected=<identity> and the stated rationale. Retain all source rows as evidence, including exclusions.'
    else:
     bits=[]
     for r in range(2,6):
      fp,tn,fn,tp=[cell(n,r) for n in ['FP','TN','FN','TP']]; fpr=f'{fp}/({fp}+{tn})';fnr=f'{fn}/({fn}+{tp})';cost=f'{cell("deployment_negative_probability",r)}*({fpr})*{cell("cost_FP",r)}+{cell("deployment_positive_probability",r)}*({fnr})*{cell("cost_FN",r)}'
      bits.append(f'{cell("system",r)}&"/"&{cell("scope",r)}&": FPR="&IF({fp}+{tn}=0,"undefined",{fpr})&", FNR="&IF({fn}+{tp}=0,"undefined",{fnr})&", harm="&IF(OR({fp}+{tn}=0,{fn}+{tp}=0),"undefined",{cost})')
     group=cell('cohort_count',4);overall=cell('cohort_count',5);dp=cell('deployment_subgroup_probability',4)
     subharm=f'{cell("deployment_negative_probability",4)}*{cell("FP",4)}/({cell("FP",4)}+{cell("TN",4)})*{cell("cost_FP",4)}+{cell("deployment_positive_probability",4)}*{cell("FN",4)}/({cell("FN",4)}+{cell("TP",4)})*{cell("cost_FN",4)}'
     def harm(r):
      fp,tn,fn,tp=[cell(n,r) for n in ['FP','TN','FN','TP']]
      return f'{cell("deployment_negative_probability",r)}*{fp}/({fp}+{tn})*{cell("cost_FP",r)}+{cell("deployment_positive_probability",r)}*{fn}/({fn}+{tp})*{cell("cost_FN",r)}'
     tests=[]
     for r in range(2,6):
      tests += [cell('FP',r)+'+'+cell('TN',r)+'>0',cell('FN',r)+'+'+cell('TP',r)+'>0']
     tests += [cell('cohort_id',2)+'='+cell('cohort_id',4),cell('cohort_id',3)+'='+cell('cohort_id',5),'('+harm(4)+')<('+harm(2)+')','('+harm(5)+')<='+str(contract['expected_cost_bound'])]
     check='IF(AND('+','.join(tests)+'),"pass","fail or unresolved")'
     formula='='+('&"; "&'.join(bits))+f'&"; validation subgroup prevalence="&{group}/{overall}&"; deployment subgroup probability="&{dp}&"; mitigation weighted contribution="&({subharm})*{dp}&"; precommitted check="&{check}&"; selected mitigation addresses the documented subgroup false-positive risk; precommitted check: subgroup harm improves against matched reference and overall expected cost <= {contract['expected_cost_bound']:.2f}; representation beyond supplied sample not established; sample prevalence is not deployment probability"'

     prompt='In AA1 enter a formula-generated report for all reference and mitigation rows: <system>/<scope>: FPR=<value>, FNR=<value>, harm=<value>; then validation subgroup prevalence, deployment subgroup probability, mitigation weighted contribution. Compute rates from actual-class denominators (empty groups undefined), subgroup prevalence as subgroup count/overall count, conditional harm from supplied class probabilities and costs, and contribution as subgroup harm times deployment subgroup probability. Then report precommitted check=pass only when subgroup harm improves on its matched reference, overall cost is within the fixed bound, all required conditioning groups are nonempty; otherwise fail or unresolved. End with: selected mitigation addresses the documented subgroup false-positive risk; precommitted check: subgroup harm improves against matched reference and overall expected cost <= 0.30; representation beyond supplied sample not established; sample prevalence is not deployment probability. Apply the fixed check to matched subgroup and overall records, not aggregate improvement alone.'
   ix['public']={'prompt':prompt,'asset_ref':{'asset_id':aid},'sheet_name':'Evidence','target_cell':'F1' if name=='task_metric_selection' else 'AA1','allowed_functions':sorted(set(re.findall(r'([A-Z]+)\(',formula)))}
   ix['grading']={'expected_value':None,'reference_formula':formula,'forbid_hardcoded_values':True};formula_ix.append(ix)
  out['interactions'].append({'step_id':s['step_id'],'interaction':ix})
# Execute solution programs in the pinned engines; obtain full expected values from probes.
if __name__=='__main__':
 scripts=[]
 for ix in code_ix:
  pub=ix['public'];problems=[];tables,_=sandbox._tables(R,pub['workspace']['asset_mounts'],{},problems)
  assert not problems,problems
  scripts.append(sandbox._py_script(ix['interaction_id'],'main.py',ix['grading']['solution_files'][0]['content'],sandbox._py_mounts(tables),[sandbox._py_probe(t) for t in ix['grading']['tests']]))
 # Execute separately to keep sklearn loads isolated and avoid excessive WASM memory.
 for ix,script in zip(code_ix,scripts):
  result=sandbox.node_run(sandbox._py_job('python',ix['public']['runtime']['packages'],[script]),sandbox.RUNTIMES['python']['runner'])['results'][ix['interaction_id']]
  (B/(ix['interaction_id']+'.probe.json')).write_text(json.dumps(result,indent=2))
  if not result['ok']:raise RuntimeError(ix['interaction_id']+' '+result.get('error',''))
  for t in ix['grading']['tests']:
   val,err=sandbox._py_result(t['kind'],t['spec'],result,t['test_id']);assert not err,(ix['interaction_id'],err);t['spec']['expected']=val
  print('computed',ix['interaction_id'],flush=True)
 for ix in formula_ix:
  pub=ix['public'];block={'asset_ref':pub['asset_ref'],'sheet_name':pub['sheet_name'],'cells':[{'ref':pub['target_cell'],'formula':ix['grading']['reference_formula']}]}
  values,problems=sandbox.sheet_cell_values(R,block);assert not problems,problems
  ix['grading']['expected_value']=values[pub['target_cell']];print('computed formula',ix['interaction_id'],flush=True)
 (B/'interactions.json').write_text(json.dumps(O,indent=2)+'\n')
 print('wrote',sum(len(t['interactions']) for t in O['tiles']))
