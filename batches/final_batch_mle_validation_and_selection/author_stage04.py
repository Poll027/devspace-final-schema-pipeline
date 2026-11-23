import json,re,sys,copy
from pathlib import Path
B=Path('batches/final_batch_mle.region.validation_and_selection')
P=json.loads((B/'tile_plans.json').read_text()); S=json.loads((B/'screens.json').read_text()); G=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); R=json.loads((B/'scenario_asset_registry.json').read_text())
g={x['context']['concept_id']:x for x in G['bundles']}; assets={a['asset_id']:a for a in R['assets']}; screens={t['tile_id']:t for t in S['tiles']}
core=Path('00_FINAL_PIPELINE_CORE'); rt=json.loads((core/'registry/runtimes.json').read_text())['runtimes']
def records(a):
 x=assets[a];return [dict(zip([c['name'] for c in x['columns']],r)) for r in x['rows']]
def base(t,s,j,n):
 cid=s['concept_ids'][0]; measures=[]
 for anchor in s['anchors']:
  if '#assessment:' in anchor:
   cap=anchor.split('#assessment:')[1];a=next(a for a in g[cid]['assessment_anchors'] if a['capability']==cap);measures.append({'concept_id':cid,**a})
 fb={'correct':{'message':'Your result follows the fixed evidence and the declared conditioning populations.'},'incorrect':{'message':'Recheck which observations belong in each denominator and keep the declared decision inputs fixed.'},'hints':['Separate the observations being measured from the fixed decision assumptions.','Check each required field against the supplied evidence before drawing the conclusion.']}
 if s['type']=='check':
  rem=next((r['step_id'] for r in screens[t['tile_id']].get('remediation_steps',[]) if cid in r['concept_ids']),None)
  if rem:fb['remediation_step_id']=rem
 return {'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if j==0 else ('stretch' if j==n-1 else 'core'),'grading_mode':'client','standalone':True,'measures':measures,'anchors':s['anchors'],'feedback':fb}
# Questions are supplied-evidence judgements with mutually exclusive conclusions.
Q={
'mle.task_metric_selection':('Precision in a late-order validation cohort is 0.80. Which interpretation is supported by this confusion-table ratio?', ['Among predicted late orders, 80% are actually late; this does not establish calibration of individual scores.','Among actually late orders, 80% are detected.','Every order with a score of 0.80 has a calibrated 80% chance of being late.'],['Precision conditions on predicted positives, and cohort frequencies alone do not establish score calibration.','This reverses the conditioning population: detection among actual positives is recall.','A confusion-table ratio does not establish calibration of individual probability scores.']),
'mle.model_acceptance_criteria':('A candidate passes the predeclared expected-cost bound but fails a separate supplied operating requirement. What is the acceptance conclusion?', ['Predictive cost passes, but the failed operating requirement excludes deployment eligibility.','The passing predictive cost overrides the operating failure.','Change deployment class probabilities until the operating failure is compensated.'],['Predictive and operating requirements remain separate.','Passing expected cost does not waive an operating condition.','Deployment probabilities are fixed decision inputs, not adjustments made to rescue a candidate.']),
'mle.reference_baseline':('The frozen reference has no actual-positive observations in one validation cohort. How should its FNR and expected error cost be recorded?', ['FNR is undefined; any cost requiring that rate is undefined.','FNR is zero, so the false-negative contribution is zero.','Use the training positive prevalence as the missing validation FNR.'],['FNR requires a nonempty actual-positive conditioning group.','An empty denominator does not define a zero rate.','Training prevalence is not the conditional validation error rate.']),
'mle.model_approach_decision':('Matched classical and neural records satisfy the same predictive-quality requirement. The neural record fails the precommitted latency requirement. Under the fixed minimum-cost-among-eligible rule, what should happen?', ['Exclude the neural record before selecting among eligible alternatives.','Select the neural record whenever its expected cost is lower.','Remove latency from the contract after seeing the neural result.'],['Operating constraints define eligibility before cost ranking.','Lower cost cannot override a fixed operating failure.','Requirements are fixed before comparison, not rewritten after results.']),
'mle.sklearn_baseline_workflow':('Training used fitted preprocessing. Which validation prediction path preserves the fitted feature representation?', ['Call predict through that fitted pipeline on the corresponding validation inputs.','Fit preprocessing again using validation labels before predicting.','Bypass the fitted preprocessing and send raw inputs directly to the final estimator.'],['The fitted pipeline applies the training-fitted representation to validation.','Validation is held out; its labels should not refit training state.','Bypassing the fitted preprocessing changes the feature representation.']),
'mle.decision_threshold_selection':('An order has a fixed probability score of 0.60. Changing the threshold from 0.50 to 0.70 changes its class decision. Which statement is correct?', ['The score is unchanged; comparing it with a different threshold changes the decision.','The score must change to 0.70 when that threshold is selected.','Threshold selection changes the actual validation label.'],['A score and the thresholded class decision are distinct outputs.','The threshold is a decision rule, not a replacement score.','The observed actual label is not altered by choosing a threshold.']),
'mle.validation_candidate_comparison':('A record has a lower expected cost than the baseline but comes from a different validation cohort. What is defensible under a matched-cohort comparison rule?', ['Exclude it from this comparison until matched-cohort evidence is available.','Select it immediately because its cost is lower.','Treat all equally sized cohorts as interchangeable.'],['Comparable candidate evidence uses the same evaluation dataset.','A lower cost on another cohort does not satisfy the matched-evidence rule.','Equal sample counts do not establish observation correspondence.']),
'mle.prediction_error_analysis':('A predefined long-distance group has a higher observed error proportion than its same-cohort reference. Which conclusion stays within the evidence?', ['The supplied group exhibits a recurring error pattern; these observations alone do not establish its cause.','Distance has been proven to cause the errors.','The developer\'s own usage disproves the supplied failure pattern.'],['The finding is descriptive and bounded to comparable supplied evidence.','An observed error pattern alone does not test a causal explanation.','Personal developer usage is not a substitute for supplied failure observations.']),
'mle.slice_evaluation':('Zone B has a higher eligible error proportion than zone A in the supplied validation sample. Which report is justified?', ['Retain both denominators and describe the observed sample gap without asserting a population disparity.','Declare all intended populations unfairly treated from the proportions alone.','Compare raw error counts and discard the eligible denominators.'],['Slice proportions must retain their sample sizes and scope.','Representation beyond the supplied sample is not established.','Raw counts without denominators do not compare conditional error proportions.']),
'mle.subgroup_risk_mitigation':('A supplied mitigation improves overall validation error cost. What further check is required before accepting it for a documented subgroup risk?', ['Check the matched affected segment as well as the overall cohort, and inspect representation limitations.','Overall improvement proves the affected segment is safe.','Replace supplied deployment subgroup probability with its validation prevalence.'],['Affected-segment and overall evidence are both required; representation remains a limitation.','Aggregate improvement does not establish suitability for every segment.','Validation subgroup prevalence and deployment population probability are distinct inputs.']),
'mle.experiment_metric_logging':('A metric was logged repeatedly to an MLflow run. What does recorded.data.metrics expose when you retrieve that keyed run?', ['The most recently logged value at the largest step, not the complete metric history.','Every historical metric value in a list.','Only the first logged value, regardless of later steps.'],['RunData exposes the most recent value at the largest step.','This field is not the entire metric history.','The retrieval rule is not the first logged value.']),
'mle.training_randomness':('A comparison sets both split and estimator random_state to the same declared integer seed for each pair. What can the report claim?', ['The specified random sources were controlled; this does not guarantee identical computation in every environment.','All computations are universally deterministic in every environment.','Controlling estimator randomness makes split randomness irrelevant.'],['Random-source control is bounded, not universal determinism.','Controlled seeds do not guarantee universal deterministic replay.','Both split and estimator random sources matter for a matched comparison.']),
'mle.validation_regularization':('For a LogisticRegression setting, C is reduced while the protocol stays fixed. What does this change mean?', ['Regularization strength increases because C is inverse regularization strength.','Regularization strength decreases because C is the direct penalty strength.','It has the same parameter direction as increasing Ridge alpha in reverse.'],['Smaller C means stronger regularization; Ridge alpha uses the direct penalty direction.','C is inverse, not direct, regularization strength.','Increasing Ridge alpha also increases the penalty, so the proposed reverse direction is wrong.']),
'mle.bounded_hyperparameter_search':('A manual search has three declared configurations, default budget three, and an explicit keyword budget of two. What should the execution record show?', ['Resolve the override first, then execute exactly the first two declared trials.','Execute all three and retain only the best two results.','Ignore the override because the function has a default.'],['The resolved budget limits execution, not just the displayed results.','Discarding a trial result does not undo execution beyond the budget.','Explicit keyword overrides replace the default for that call.']),
'mle.model_risk_documentation':('An existing policy permits identity A; a supplied access-grant record includes A and B. What belongs in the risk record?', ['Preserve permitted scope A and identify B as an out-of-scope grant.','Expand the permitted scope to A and B to match observed grants.','Copy any exposed credential value as evidence of the grant.'],['Record the deviation without redefining the existing authorization policy.','Observed grants do not authorize extending the permitted identity scope.','Describe exposure location and handling limitation without copying secrets.']),
'mle.foundation_model_baseline_evaluation':('A supplied foundation-output file has the right number of rows but different observation identifiers from the labeled validation cohort. What should happen?', ['Reject alignment and do not issue a task-quality acceptance verdict from unmatched observations.','Compare by position because equal row counts prove correspondence.','Fit a new model to make the file align.'],['Matched identifiers establish which labels correspond to supplied outputs.','Equal size alone does not establish observation correspondence.','This task evaluates supplied outputs, not new fitting or construction.'])}
def choice(cid):
 q,opts,fb=Q[cid];ids=['o'+str(i+1) for i in range(len(opts))];return {'prompt':q,'options':[{'option_id':i,'text':x} for i,x in zip(ids,opts)],'selection':'single','shuffle':True},{'correct_option_ids':[ids[0]],'option_feedback':{i:{'message':x} for i,x in zip(ids,fb)}}
def mount(a,name=None):return {'asset_id':a,'mount_path':name or a[3:]+'.csv'}
def code(ix,cid,scaffold,learner,signature,exprs,prompt,mounts,packages=['numpy','pandas']):
 starter=scaffold+'\n# Add the required imports and implement the function.\n'+signature+'\n    return None\n'
 solution=scaffold+'\n'+learner.strip()+'\n'
 live=g[cid]['practice_anchor'].get('live_code');constraints={k:live[k] for k in ['allowed_syntax','blocked_syntax']} if live else {'allowed_syntax':[],'blocked_syntax':[]}
 ix['public']={'prompt':prompt,'runtime':{'kind':'python','version':rt['python']['version'],'packages':packages},'workspace':{'entry':'main.py','files':[{'path':'main.py','role':'editable','language':'python','content':starter}],'asset_mounts':mounts},'constraints':constraints}
 ix['grading']={'solution_files':[{'path':'main.py','content':solution}], 'tests':[{'test_id':'t'+str(i+1),'kind':'value_equals','spec':{'expr':e},'visible':i==0,'message_on_fail':'Check the named result fields, fixed assumptions, and empty-group behavior.'} for i,e in enumerate(exprs)]}
def formula(ix,a,formula,prompt):
 ix['public']={'prompt':prompt,'asset_ref':{'asset_id':a},'sheet_name':'Evidence','target_cell':'AZ1','allowed_functions':sorted(set(re.findall(r'([A-Z]+)\(',formula)))}
 ix['grading']={'reference_formula':formula,'expected_value':None,'forbid_hardcoded_values':True}
def C(i):
 z=''
 while i: i,r=divmod(i-1,26);z=chr(65+r)+z
 return z
def ref(a,name,r):return C([x['name'] for x in assets[a]['columns']].index(name)+1)+str(r)
def text(x):return '"'+x.replace('"','""')+'"'
def cat(parts):return '&'.join(parts)
def fmt(x):return 'TEXT('+x+',"0.00")'
def cost(a,r):
 fp,tn,fn,tp=[ref(a,k,r) for k in ['FP','TN','FN','TP']]
 return f'(0.8*{fp}/({fp}+{tn})+0.2*{fn}/({fn}+{tp})*5)'
def valid(a,r):
 return 'AND('+','.join([f'({ref(a,"FP",r)}+{ref(a,"TN",r)})>0',f'({ref(a,"FN",r)}+{ref(a,"TP",r)})>0'])+')'
# Contract data loading is scaffolding; all graded calculations are learner-written.
load_contract="import pandas as pd\ncontract = pd.read_csv('acceptance_contract.csv').iloc[0]\np_negative = contract['deployment_negative_probability']\np_positive = contract['deployment_positive_probability']\ncost_FP = contract['cost_FP']\ncost_FN = contract['cost_FN']\nbound = contract['expected_cost_bound']\n"
counts='''    FP = np.sum((y == 0) & (predictions == 1))
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
'''
count_return="{'FP': FP, 'TN': TN, 'FN': FN, 'TP': TP, 'actual_negative_count': negative_count, 'actual_positive_count': positive_count, 'FPR': FPR, 'FNR': FNR, 'expected_cost': expected_cost}"
output={'schema_version':P['schema_version'],'kind':'interactions_part','path_id':P['path_id'],'batch_id':P['batch_id'],'tiles':[]}
for t in P['tiles']:
 sts=[s for s in t['steps'] if s['type'] in ['check','hands_on']]; out={'tile_id':t['tile_id'],'interactions':[]}
 for j,s in enumerate(sts):
  cid=s['concept_ids'][0];short=cid[4:];ix=base(t,s,j,len(sts))
  if s['type']=='check':ix['public'],ix['grading']=choice(cid)
  elif short=='task_metric_selection':
   f='='+cat([text('precision=P(actual positive|predicted positive): '),fmt('D2/(D2+D3)'),text('; recall=P(predicted positive|actual positive): '),fmt('D2/(D2+D4)'),text('; prevalence: '),fmt('(D2+D4)/SUM(D2:D5)'),text('; choose recall: missed late orders have the greater consequence; cohort ratios do not establish individual-score calibration; squared-error averaging gives large regression errors more influence than absolute-error averaging.')])
   formula(ix,'ds.confusion_counts',f,'Missed late orders have the greater consequence. In AZ1 enter one concatenating formula that computes precision, recall and actual-positive prevalence from the counts (two decimal places), identifies both conditioning populations, chooses and justifies the metric for this consequence, and states the calibration limitation. Use the output format: precision=P(actual positive|predicted positive): <value>; recall=P(predicted positive|actual positive): <value>; prevalence: <value>; choose recall: missed late orders have the greater consequence; cohort ratios do not establish individual-score calibration; squared-error averaging gives large regression errors more influence than absolute-error averaging. Include that final regression contrast in the same record.')
  elif short=='model_acceptance_criteria':
   starter='// Fixed contract and rates are supplied; complete the formulas on sheet terms.\n'
   sol=starter+'H1: =IF(E2>0,C2,"undefined")\nH2: =IF(E3>0,C3,"undefined")\nH3: =IF(AND(E2>0,E3>0),B2*H1*D2+B3*H2*D3,"undefined")\nH4: =IF(AND(E2>0,E3>0),H3<=contract!F2,FALSE)\nH5: =E2\nH6: =E3\nH7: =contract!E2\nH8: =contract!F2\nH9: =IF(ISBLANK(contract!K2),"no numeric operating limit supplied; predictive acceptance is not overall eligibility",contract!K2)\n'
   ix['public']={'prompt':'The supplied deployment probabilities, costs, rates and permitted bound are fixed before comparison; correct predictions have zero cost. On sheet terms, put guarded FPR in H1 (actual-negative denominator E2), guarded FNR in H2 (actual-positive denominator E3), expected cost in H3, and the predictive inequality result H3 <= the bound in H4. Use "undefined" for rates/cost with empty conditioning groups and FALSE for unresolved predictive acceptance. Put the two conditioning counts in H5/H6, the correct-prediction cost in H7, and bound in H8. In H9 retain the supplied operating limit independently; when none is supplied write "no numeric operating limit supplied; predictive acceptance is not overall eligibility". Do not invent a latency limit.','runtime':{'kind':'spreadsheet','version':rt['spreadsheet']['version']},'workspace':{'entry':'contract.sheet','files':[{'path':'contract.sheet','role':'editable','language':'sheet','content':starter}],'asset_mounts':[mount('ds.acceptance_terms','terms.csv'),mount('ds.acceptance_contract','contract.csv')]},'constraints':{'allowed_syntax':['IF','AND','ISBLANK','relative cell references','cross-sheet references','+ - * /','comparison operators','text in quotes','TRUE / FALSE'],'blocked_syntax':[]}}
   ix['grading']={'solution_files':[{'path':'contract.sheet','content':sol}],'tests':[{'test_id':'t'+str(i),'kind':'cell_equals','spec':{'cell':'H'+str(i)},'message_on_fail':'Keep rates, fixed contract inputs and operating limits separate.'} for i in range(1,10)]}
  elif short in ['reference_baseline','sklearn_baseline_workflow']:
   train='reference_train' if short=='reference_baseline' else 'orders_train';features=['feature_1'] if short=='reference_baseline' else ['feature_1','feature_2'];sc=load_contract+f"train = pd.read_csv('{train}.csv')\nvalidation = pd.read_csv('orders_validation.csv')\nX_train = train[{features!r}].to_numpy()\ny_train = train['y_train'].to_numpy()\nX_validation = validation[{features!r}].to_numpy()\ny_validation = validation['y_validation'].to_numpy()\n"
   sig='def evaluate(X_train, y_train, X_validation, y, p_negative, p_positive, cost_FP, cost_FN):'
   init='from sklearn.dummy import DummyClassifier\nfrom sklearn.metrics import accuracy_score\n' if short=='reference_baseline' else 'from sklearn.linear_model import LogisticRegression\n'
   estimator='DummyClassifier(strategy="most_frequent")' if short=='reference_baseline' else 'LogisticRegression(random_state=0)'
   learner='import numpy as np\n'+init+sig+'\n'
   if short=='sklearn_baseline_workflow':learner+='    assert X_train.ndim == 2\n    assert y_train.ndim == 1\n    assert X_train.shape[0] == y_train.shape[0]\n    assert X_validation.shape[0] == y.shape[0]\n'
   learner+=f'    estimator = {estimator}\n    estimator.fit(X_train, y_train)\n    predictions = estimator.predict(X_validation)\n'+counts
   extra=", 'predictions': predictions, 'training_shape': X_train.shape, 'training_label_shape': y_train.shape"
   if short=='reference_baseline':extra+=", 'rule': 'most_frequent', 'training_mean': np.mean(y_train), 'training_std': np.std(y_train, ddof=0), 'training_positive_prevalence': np.sum(y_train == 1) / len(y_train), 'training_negative_prevalence': np.sum(y_train == 0) / len(y_train), 'validation_accuracy': accuracy_score(y, predictions)"
   learner+='    return '+count_return[:-1]+extra+'}\n'
   expr='evaluate(X_train, y_train, X_validation, y_validation, p_negative, p_positive, cost_FP, cost_FN)'
   fields='FP, TN, FN, TP, actual_negative_count, actual_positive_count, FPR, FNR, expected_cost, predictions, training_shape, training_label_shape'
   if short=='reference_baseline':fields+=', rule, training_mean, training_std, training_positive_prevalence, training_negative_prevalence, validation_accuracy'
   prompt='Write the required NumPy and estimator imports and implement evaluate with the supplied parameters. Fit the '+('most-frequent reference' if short=='reference_baseline' else 'LogisticRegression(random_state=0) baseline')+' once on training only, then predict separate corresponding validation inputs. Return a dictionary with exactly these fields: '+fields+'. Use actual-class denominators; undefined rates and any cost requiring them must be None. '+('Use the binary training targets for mean, ddof=0 standard deviation and both class proportions; accuracy compares validation predictions to validation labels.' if short=='reference_baseline' else 'Verify two-dimensional training inputs, one-dimensional training labels and observation-count alignment. The supplied raw numeric features require no fitted preprocessing; if preprocessing were supplied, predictions would use that fitted pipeline. Original fixture dimensions are (6, 2) and (6,), but derive dimensions for altered fixtures.')+' Preserve the fixed zero-correct-prediction-cost contract and do not access protected test data.'
   code(ix,cid,sc,learner,sig,[expr,expr.replace('X_validation, y_validation','X_validation[y_validation == 0], y_validation[y_validation == 0]'),expr.replace('X_validation, y_validation','X_validation[y_validation == 1], y_validation[y_validation == 1]')],prompt,[mount('ds.'+train),mount('ds.orders_validation'),mount('ds.acceptance_contract')],['numpy','pandas','scikit-learn'])
  elif short in ['model_approach_decision','validation_candidate_comparison']:
   a='ds.approach_records' if short=='model_approach_decision' else 'ds.candidate_records';n=len(assets[a]['rows']);parts=[];eligible=[]
   for r in range(2,n+2):
    flags=[ref(a,k,r) for k in [c['name'] for c in assets[a]['columns'] if c['name'].endswith('_met')]]
    elig='AND('+','.join([valid(a,r),ref(a,'cohort_id',r)+'="orders_100"',cost(a,r)+'<=0.30']+flags)+')';eligible.append(elig)
    ident=ref(a,'alternative_id' if short=='model_approach_decision' else 'candidate_id',r)
    fp,tn,fn,tp=[ref(a,k,r) for k in ['FP','TN','FN','TP']]
    parts += [ident,text(': neg='),str(f'({fp}+{tn})'),text(',pos='),str(f'({fn}+{tp})'),text(',FPR='),f'IF({valid(a,r)},{fmt(fp+"/("+fp+"+"+tn+")")},"undefined")',text(',FNR='),f'IF({valid(a,r)},{fmt(fn+"/("+fn+"+"+tp+")")},"undefined")',text(',cost='),f'IF({valid(a,r)},{fmt(cost(a,r))},"undefined")',text(',eligible='),f'IF({elig},"yes","no")',text('; ')]
    if short=='model_approach_decision':parts.extend([ref(a,'maintenance_responsibility',r),text('; ')])
   scores=[f'IF({e},{cost(a,r)},1000000)' for r,e in enumerate(eligible,2)];minimum='MIN('+','.join(scores)+')'; selection='"none"'
   for r,e in reversed(list(enumerate(eligible,2))):selection=f'IF(AND({e},{cost(a,r)}={minimum}),{ref(a,"alternative_id" if short=="model_approach_decision" else "candidate_id",r)},{selection})'
   parts += [text('selected='),selection,text('; fixed p0=0.80,p1=0.20,costFP=1,costFN=5,correct cost=0,bound=0.30; exclude unmatched cohorts, operating failures and unresolved required rates before cost ranking; ties use declared order; no protected-test evidence.')]
   if short=='model_approach_decision':parts+=[text(' Classical versus neural follows matched quality and operating eligibility; custom versus managed retains the recorded maintenance responsibilities, not an assumption that managed eliminates owner task-model choices.')]
   formula(ix,a,'='+cat(parts),'Read every supplied record. In AZ1 enter one formula returning a semicolon-separated comparison record. For each row, in declared order, output <identity>: neg=<FP+TN>,pos=<FN+TP>,FPR=<two decimals or undefined>,FNR=<two decimals or undefined>,cost=<two decimals or undefined>,eligible=<yes/no>; '+('then the row maintenance_responsibility followed by "; ". ' if short=='model_approach_decision' else '')+'Apply the fixed orders_100 cohort, expected-cost <= 0.30, every supplied operating flag, and defined required rates. Rank eligible records by lowest cost; ties use declared order. Append selected=<identity or none>; fixed p0=0.80,p1=0.20,costFP=1,costFN=5,correct cost=0,bound=0.30; exclude unmatched cohorts, operating failures and unresolved required rates before cost ranking; ties use declared order; no protected-test evidence.'+(' Append: Classical versus neural follows matched quality and operating eligibility; custom versus managed retains the recorded maintenance responsibilities, not an assumption that managed eliminates owner task-model choices.' if short=='model_approach_decision' else ''))
  elif short=='decision_threshold_selection':
   sc=load_contract+"import numpy as np\nobservations = pd.read_csv('validation_scores.csv')\ny = observations['actual_label'].to_numpy()\nscores = observations['score'].to_numpy()\nthresholds = pd.read_csv('thresholds.csv')['threshold'].tolist()\n"
   sig='def evaluate(scores, y, thresholds, p_negative, p_positive, cost_FP, cost_FN, bound):'
   # count_nonzero, not np.sum, is the practice's declared tool.
   body='import numpy as np\n'+sig+'\n    records = []\n    selected = None\n    best_cost = None\n    for threshold in thresholds:\n        predictions = scores >= threshold\n'+''.join('    '+l+'\n' for l in counts.replace('np.sum','np.count_nonzero').splitlines())+'        record = '+count_return[:-1]+", 'threshold': threshold, 'score_representation': 'probability'}\n        records.append(record)\n        if expected_cost is not None:\n            if expected_cost <= bound:\n                if best_cost is None:\n                    best_cost = expected_cost\n                    selected = threshold\n                else:\n                    if expected_cost < best_cost:\n                        best_cost = expected_cost\n                        selected = threshold\n    return {'records': records, 'selected_threshold': selected, 'score_representation': 'probability'}\n"
   expr='evaluate(scores, y, thresholds, p_negative, p_positive, cost_FP, cost_FN, bound)'
   code(ix,cid,sc,body,sig,[expr,expr.replace('scores, y, thresholds','scores[y == 0], y[y == 0], thresholds'),expr.replace(', bound)',', -1)')],'Implement evaluate over the declared probability thresholds; do not alter the scores. Return records in declared order, each with FP,TN,FN,TP,actual_negative_count,actual_positive_count,FPR,FNR,expected_cost,threshold,score_representation. Return selected_threshold (minimum fixed expected cost <= bound; first declared tie; None if none eligible) and score_representation="probability". Undefined rates/cost are None. Retain the selected threshold and unchanged score representation for later testing; no protected-test access.',[mount('ds.validation_scores'),mount('ds.thresholds'),mount('ds.acceptance_contract')])
  elif short=='prediction_error_analysis':
   sc="import pandas as pd\nimport numpy as np\nobservations = pd.read_csv('slice_observations.csv')\neligible = observations['eligible'].to_numpy()\nlong_distance = observations['long_distance'].to_numpy()\nerrors = observations['error'].to_numpy()\nlosses = observations['loss'].to_numpy()\nreference_errors = observations['reference_error'].to_numpy()\nreference_losses = observations['reference_loss'].to_numpy()\n"
   sig='def evaluate(eligible, long_distance, errors, losses, reference_errors, reference_losses):'
   body='import numpy as np\n'+sig+'''\n    group = (eligible == True) & (long_distance == True)
    n = np.count_nonzero(group)
    error_count = np.count_nonzero(errors[group])
    reference_count = np.count_nonzero(reference_errors[group])
    return {'eligible_count': n, 'error_count': error_count, 'error_proportion': error_count / n, 'loss_mean': np.mean(losses[group]), 'loss_std': np.std(losses[group], ddof=0), 'reference_eligible_count': n, 'reference_error_count': reference_count, 'reference_error_proportion': reference_count / n, 'reference_loss_mean': np.mean(reference_losses[group]), 'reference_loss_std': np.std(reference_losses[group], ddof=0), 'finding': 'The supplied long-distance failures form a descriptive pattern; compare the same-cohort reference quantities, not an untested causal claim.'}
'''
   code(ix,cid,sc,body,sig,['evaluate(eligible, long_distance, errors, losses, reference_errors, reference_losses)'],'Implement evaluate for the predefined eligible long-distance group and corresponding same-cohort reference. Return eligible_count,error_count,error_proportion,loss_mean,loss_std (ddof=0), and reference_eligible_count,reference_error_count,reference_error_proportion,reference_loss_mean,reference_loss_std. The supplied group is nonempty. Include finding="The supplied long-distance failures form a descriptive pattern; compare the same-cohort reference quantities, not an untested causal claim." The computed counts and loss summaries are the evidence supporting that bounded finding.',[mount('ds.slice_observations')])
  elif short=='slice_evaluation':
   sc="import pandas as pd\nimport numpy as np\nobservations = pd.read_csv('slice_observations.csv')\nzones = observations['zone'].to_numpy()\neligible = observations['eligible'].to_numpy()\nerrors = observations['error'].to_numpy()\nlosses = observations['loss'].to_numpy()\ndeclared_slices = ['A', 'B']\n"
   sig='def evaluate(zones, eligible, errors, losses, declared_slices):'
   body='import numpy as np\n'+sig+'''\n    records = []
    for zone in declared_slices:
        mask = (zones == zone) & (eligible == True)
        n = np.sum(mask)
        error_count = np.sum(errors[mask])
        record = {'slice': zone, 'eligible_count': n, 'error_count': error_count, 'error_proportion': None, 'loss_mean': None, 'loss_std': None}
        if n > 0:
            record = {'slice': zone, 'eligible_count': n, 'error_count': error_count, 'error_proportion': error_count / n, 'loss_mean': np.mean(losses[mask]), 'loss_std': np.std(losses[mask], ddof=0)}
        records.append(record)
    return {'records': records, 'limitation': 'These are observed eligible validation slices; representation beyond this sample is unresolved, so no population disparity is established.'}
'''
   expr='evaluate(zones, eligible, errors, losses, declared_slices)'
   code(ix,cid,sc,body,sig,[expr,expr.replace('declared_slices)',"['unobserved'])")],'Implement evaluate for the declared slices in order. Return records with slice,eligible_count,error_count,error_proportion,loss_mean,loss_std (ddof=0). Retain both denominators; for an empty slice use None for proportion and both loss summaries. Add limitation="These are observed eligible validation slices; representation beyond this sample is unresolved, so no population disparity is established."',[mount('ds.slice_observations')])
  elif short=='subgroup_risk_mitigation':
   a='ds.mitigation_records';parts=[]
   for r in range(2,6):
    fp,tn,fn,tp=[ref(a,k,r) for k in ['FP','TN','FN','TP']];harm=f'(({fp}+{tn})/({fp}+{tn}+{fn}+{tp})*{fp}/({fp}+{tn})*{ref(a,"cost_FP",r)}+({fn}+{tp})/({fp}+{tn}+{fn}+{tp})*{fn}/({fn}+{tp})*{ref(a,"cost_FN",r)})'
    parts += [ref(a,'system',r),text('/'),ref(a,'scope',r),text(': neg='),f'({fp}+{tn})',text(',pos='),f'({fn}+{tp})',text(',FPR='),f'IF({valid(a,r)},{fmt(fp+"/("+fp+"+"+tn+")")},"undefined")',text(',FNR='),f'IF({valid(a,r)},{fmt(fn+"/("+fn+"+"+tp+")")},"undefined")',text(',harm='),f'IF({valid(a,r)},{fmt(harm)},"undefined")']
    if r in [2,4]:
     overall=3 if r==2 else 5
     parts += [text(',validation_prevalence='),fmt(ref(a,'cohort_count',r)+'/'+ref(a,'cohort_count',overall)),text(',deployment_probability='),fmt(ref(a,'deployment_subgroup_probability',r)),text(',contribution='),f'IF({valid(a,r)},{fmt(harm+"*"+ref(a,"deployment_subgroup_probability",r))},"undefined")']
    parts+=[text('; ')]
   parts += [text('selected=mitigation; precommitted check: defined conditioned rates and lower harm in matched affected segment AND overall cohort; deployment probability is not validation prevalence; representation beyond supplied sample is not established.')]
   formula(ix,a,'='+cat(parts),'In AZ1 return one formula-based risk-check record for all four supplied rows in order. Each row: <system>/<scope>: neg=<FP+TN>,pos=<FN+TP>,FPR=<two decimals or undefined>,FNR=<two decimals or undefined>,harm=<two decimals or undefined>. Harm uses each row\'s actual-class proportions and supplied error costs, with zero correct-prediction cost. For affected_subgroup rows also append ,validation_prevalence=<subgroup count / corresponding overall count>,deployment_probability=<supplied probability>,contribution=<harm times supplied deployment probability> (two decimals). End each row with "; ". Before viewing comparisons, use the check: defined rates and lower harm on both matched scopes. Append selected=mitigation; precommitted check: defined conditioned rates and lower harm in matched affected segment AND overall cohort; deployment probability is not validation prevalence; representation beyond supplied sample is not established. The supplied mitigation addresses the documented affected-segment risk; retain sample representation limits, not a population guarantee.')
  elif short=='experiment_metric_logging':
   v=records('ds.execution_contract')[0];default=v['default_trial_setting'];override=v['override_trial_setting'];metric=records('ds.acceptance_terms');cost_value=sum(r['deployment_class_probability']*r['conditional_error_rate']*r['error_cost'] for r in metric)
   excerpts=[
    ('resolved',f'def record(trial_setting={default}):\n    mlflow.log_params({{"trial_setting": trial_setting}})\nrecord(trial_setting={override})\nretrieved params: trial_setting="{override}"','meets','The recorded parameter retains the resolved keyword override.'),
    ('default',f'def record(trial_setting={default}):\n    mlflow.log_params({{"trial_setting": {default}}})\nrecord(trial_setting={override})\nretrieved params: trial_setting="{default}"','fails','Logging the default ignores the explicit resolved override.'),
    ('identity','cwd = os.getcwd()\nos.chdir(recorded_directory)\ncompleted = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=recorded_directory, capture_output=True, text=True, check=True)\nactual_revision = completed.stdout.strip()\nif actual_revision != expected_revision:\n    raise ValueError("Repository revision mismatch")\nresolved_path = os.path.abspath(local_path)\n# retain actual_revision and resolved_path with run_id','meets','Captured revision is inspected in the intended repository and mismatches are rejected; the resolved local path is retained.'),
    ('unchecked','revision = expected_revision\n# no repository inspection performed\nlookup = {"repository_revision": revision, "diagnostic_path": local_path}','fails','Copying an expected revision does not inspect the actual repository, and an unresolved path does not retain the resolved artifact location.'),
    ('linked',f'with mlflow.start_run() as run:\n    run_id = run.info.run_id\n    mlflow.log_metric("validation_expected_cost", {cost_value!r})\n    mlflow.log_artifact(resolved_path)\nrecorded = mlflow.get_run(run_id)\nlookup = {{"run_id": run_id, "params": recorded.data.params, "metrics": recorded.data.metrics, "artifact_uri": recorded.info.artifact_uri, "resolved_path": resolved_path, "repository_revision": actual_revision}}','meets','A keyed run links the validation metric and diagnostic artifact, and retrieval retains the parameters, metric and artifact URI.'),
    ('history','recorded = mlflow.get_run(run_id)\nreport = {"entire_metric_history": recorded.data.metrics}','fails','RunData metrics are the most recently logged values at the largest step, not the entire history.')]
   ix['public']={'prompt':'Read each supplied logging excerpt and judge whether it meets or violates the named requirement shown by its evidence: resolved configuration, repository/path identity, keyed logging/retrieval, or metric-history interpretation. Other parts of the logging workflow are outside each excerpt\'s judgement.','buckets':[{'bucket_id':'meets','label':'Meets the shown requirement'},{'bucket_id':'fails','label':'Violates the shown requirement'}],'items':[{'item_id':i,'text':x} for i,x,b,f in excerpts]};ix['grading']={'assignments':{i:b for i,x,b,f in excerpts},'item_feedback':{i:{'message':f} for i,x,b,f in excerpts}}
  elif short=='training_randomness':
   sc="import pandas as pd\ntrials = pd.read_csv('paired_trials.csv').to_dict('records')\ndeclared_seed_list = pd.read_csv('paired_trials.csv')['seed'].tolist()\n# Supplied infrastructure adapter: returns paired validation evidence and audits random sources.\ncall_trace = []\ndef run_pair(seed, split_random_state, baseline_random_state, candidate_random_state):\n    assert split_random_state == seed\n    assert baseline_random_state == seed\n    assert candidate_random_state == seed\n    for row in trials:\n        if row['seed'] == seed:\n            call_trace.append({'seed': seed, 'split_random_state': split_random_state, 'baseline_random_state': baseline_random_state, 'candidate_random_state': candidate_random_state})\n            return row\n    raise ValueError('undeclared seed')\n"
   sig='def evaluate(declared_seed_list):'
   body='import numpy as np\n'+sig+'''\n    pairs = []
    baseline_results = []
    candidate_results = []
    wins = 0
    for seed in declared_seed_list:
        pair = run_pair(seed, split_random_state=seed, baseline_random_state=seed, candidate_random_state=seed)
        pairs.append(pair)
        baseline_results.append(pair['baseline_result'])
        candidate_results.append(pair['candidate_result'])
        if pair['candidate_result'] < pair['baseline_result']:
            wins = wins + 1
    n = len(pairs)
    return {'pairs': pairs, 'completed_pair_count': n, 'win_count': wins, 'win_probability': wins / n, 'baseline_mean': np.mean(baseline_results), 'baseline_std': np.std(baseline_results, ddof=0), 'candidate_mean': np.mean(candidate_results), 'candidate_std': np.std(candidate_results, ddof=0), 'limitation': 'Declared split and estimator random sources are controlled; identical computation in every environment is not guaranteed.'}
'''
   code(ix,cid,sc,body,sig,['evaluate(declared_seed_list)',"(evaluate(declared_seed_list), call_trace[-len(declared_seed_list):])"],'Implement evaluate over every declared seed. Use the supplied run_pair adapter, passing that seed explicitly as split_random_state, baseline_random_state and candidate_random_state. Lower expected cost wins; ties are not wins. Return pairs (seed,baseline_result,candidate_result),completed_pair_count,win_count,win_probability,baseline_mean,baseline_std,candidate_mean,candidate_std (both ddof=0). Include limitation="Declared split and estimator random sources are controlled; identical computation in every environment is not guaranteed." The adapter supplies existing paired evidence, not a new training task.',[mount('ds.paired_trials')])
  elif short=='validation_regularization':
   sc=load_contract+"settings = pd.read_csv('regularization_records.csv').to_dict('records')\n# Existing training-fitted workflow supplies the matched training/validation counts.\n"
   sig='def evaluate(settings, p_negative, p_positive, cost_FP, cost_FN, bound):'
   body=sig+'''\n    records = []
    selected = None
    best_cost = None
    for setting in settings:
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
        if expected_cost is not None:
            if expected_cost <= bound:
                if setting['operating_requirements_met']:
                    eligible = True
                    if best_cost is None:
                        best_cost = expected_cost
                        selected = setting['configuration_id']
                    else:
                        if expected_cost < best_cost:
                            best_cost = expected_cost
                            selected = setting['configuration_id']
        records.append({'configuration_id': setting['configuration_id'], 'parameter_value': setting['parameter_value'], 'FPR': FPR, 'FNR': FNR, 'actual_negative_count': FP + TN, 'actual_positive_count': FN + TP, 'training_cost': training_cost, 'validation_cost': expected_cost, 'eligible': eligible})
    return {'records': records, 'selected_configuration': selected, 'direction': 'C is inverse regularization strength; smaller C increases the penalty. Larger Ridge alpha increases the penalty.', 'interpretation': 'Lower expected cost is better; compare training and validation costs under the fixed protocol, not training cost alone.'}
'''
   expr='evaluate(settings, p_negative, p_positive, cost_FP, cost_FN, bound)'
   code(ix,cid,sc,body,sig,[expr,expr.replace(', bound)',', -1)')],'Implement evaluate to compare the declared settings using supplied counts from the existing training-fitted workflow; do not refit preprocessing, alter the held-out protocol, or access protected test data. Return records in declared order with configuration_id,parameter_value,FPR,FNR,actual_negative_count,actual_positive_count,training_cost,validation_cost,eligible. Guard both training and validation denominators; unresolved rates/costs are None and cannot establish eligibility. Apply cost <= bound and supplied operating eligibility, select minimum validation cost, first tie, or None. Include selected_configuration, direction="C is inverse regularization strength; smaller C increases the penalty. Larger Ridge alpha increases the penalty.", and interpretation="Lower expected cost is better; compare training and validation costs under the fixed protocol, not training cost alone."',[mount('ds.regularization_records'),mount('ds.acceptance_contract')])
  elif short=='bounded_hyperparameter_search':
   v=records('ds.execution_contract')[0];default=v['default_search_budget'];override=v['override_search_budget']
   sc=load_contract+f"import json\ntrials = pd.read_csv('search_trials.csv').to_dict('records')\nconfigurations = [json.loads(row['configuration_json']) for row in trials]\n# Supplied authorized trial adapter; execution trace retains actual configurations.\nCALLS = []\ndef run_trial(configuration):\n    for row in trials:\n        if json.loads(row['configuration_json']) == configuration:\n            CALLS.append(configuration.copy())\n            return row\n    raise ValueError('configuration outside declared search space')\n"
   sig=f'def search(configurations, p_negative, p_positive, cost_FP, cost_FN, bound, budget={default}):'
   body=sig+'''\n    records = []
    selected = None
    best_cost = None
    for configuration in configurations[:budget]:
        trial = run_trial(configuration)
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
                expected_cost = p_negative * FPR * cost_FP + p_positive * FNR * cost_FN
        eligible = False
        if expected_cost is not None:
            if expected_cost <= bound:
                if trial['operating_requirements_met']:
                    eligible = True
                    if best_cost is None:
                        best_cost = expected_cost
                        selected = configuration
                    else:
                        if expected_cost < best_cost:
                            best_cost = expected_cost
                            selected = configuration
        records.append({'configuration': configuration, 'cohort_id': trial['cohort_id'], 'FP': FP, 'TN': TN, 'FN': FN, 'TP': TP, 'actual_negative_count': FP + TN, 'actual_positive_count': FN + TP, 'FPR': FPR, 'FNR': FNR, 'expected_cost': expected_cost, 'eligible': eligible})
    return {'resolved_budget': budget, 'completed_trials': len(records), 'records': records, 'selected_configuration': selected}
'''
   expr='search(configurations, p_negative, p_positive, cost_FP, cost_FN, bound)'
   code(ix,cid,sc,body,sig,[expr,expr[:-1]+f', budget={override})',f"(search(configurations, p_negative, p_positive, cost_FP, cost_FN, bound, budget={override}), CALLS[-{override}:])"],'Implement search with the shown default budget and explicit keyword overrides resolved before iteration. Execute only the bounded declared configurations through run_trial; preserve actual configurations and returned validation evidence. Return resolved_budget,completed_trials,records,selected_configuration. Each record has configuration,cohort_id,FP,TN,FN,TP,actual_negative_count,actual_positive_count,FPR,FNR,expected_cost,eligible. Empty conditioning rates and requiring costs are None. Apply the fixed cost bound and operating flag, select lowest eligible validation cost, first declared tie, or None. The override budget of two must execute exactly the first two configurations. No protected-test access.',[mount('ds.search_trials'),mount('ds.acceptance_contract')])
  elif short=='model_risk_documentation':
   evidence=records('ds.risk_policy_evidence');a=records('ds.access_grants');z=records('ds.slice_summary');agg=records('ds.aggregate_slice_evidence')
   instruction='Produce one text risk-and-use record from these supplied existing-policy fields and observations. Preserve permitted scope; do not copy secrets or create an authorization policy.\n'+ '\n'.join(r['field']+': policy='+r['existing_policy']+'; observation='+r['supplied_observation']+'; recording constraint='+r['recording_constraint'] for r in evidence)+'\nAccess grants: '+json.dumps(a)+'\nSupported validation slice evidence: '+json.dumps(z[:2])+'\nAggregate evidence: '+json.dumps(agg)+'\nRetain permitted identities, documented task limits, foreseeable misuse, out-of-scope grants, exposure location/handling limitation and supported sample-only segment limitations in that single record.'
   checklist=['Preserve the existing permitted identity scope A and identify the observed B grant as out of scope.','Document only the redacted credential field location and handling limitation, never a secret value.','Retain permitted use, task/cohort limits and foreseeable misuse fields without expanding permissions.','Cite the supplied zone sample proportions and counts; state representation beyond the sample is unresolved and aggregate improvement is not universal suitability.']
   ix['public']={'instruction':instruction,'evidence_kinds':['text','file'],'checklist':checklist};ix['grading']={'mode':'manual','rubric':[{'criterion':x,'weight':1} for x in checklist]};ix['feedback']={'correct':{'message':'The single record preserves policy scope and cites bounded supplied evidence without exposing secrets.'},'incorrect':{'message':'Retain every existing-policy field, identify scope deviations, and separate sample evidence from universal suitability.'},'hints':['Separate existing permission scope from observed grants.','Describe exposure handling without reproducing credential values.']}
  elif short=='foundation_model_baseline_evaluation':
   sc=load_contract+"import numpy as np\nvalidation = pd.read_csv('validation_scores.csv')\noutputs = pd.read_csv('foundation_outputs.csv')\nids = validation['observation_id'].to_numpy()\noutput_ids = outputs['observation_id'].to_numpy()\ny = validation['actual_label'].to_numpy()\noutputs_y = outputs['foundation_output'].to_numpy()\nreference = validation['reference_output'].to_numpy()\noutput_kind = outputs['output_kind'].to_numpy()\n"
   sig='def evaluate(ids, output_ids, y, outputs_y, reference, output_kind, p_negative, p_positive, cost_FP, cost_FN, bound):'
   helper='''import numpy as np
def quantities(y, predictions, p_negative, p_positive, cost_FP, cost_FN):
'''+counts+'    return '+count_return[:-1]+", 'accuracy': np.sum(y == predictions) / np.sum((y == 0) | (y == 1))}\n"
   body=helper+sig+'''\n    if not np.array_equal(ids, output_ids):
        return {'aligned': False, 'accepted': False, 'reason': 'unmatched observations'}
    if y.shape != outputs_y.shape or y.shape != reference.shape:
        return {'aligned': False, 'accepted': False, 'reason': 'unmatched observations'}
    if np.sum(output_kind != 'foundation-model') > 0:
        return {'aligned': False, 'accepted': False, 'reason': 'candidate is not the supplied foundation-model output kind'}
    candidate = quantities(y, outputs_y, p_negative, p_positive, cost_FP, cost_FN)
    baseline = quantities(y, reference, p_negative, p_positive, cost_FP, cost_FN)
    accepted = False
    if candidate['expected_cost'] is not None:
        if candidate['expected_cost'] <= bound:
            accepted = True
    return {'aligned': True, 'candidate': candidate, 'baseline': baseline, 'accepted': accepted, 'bound': bound, 'limitations': 'Quality verdict is bounded to supplied order-task validation observations; no application construction, fitting or protected-test evidence is implied.'}
'''
   # Boolean OR is not allowed by this practice; denominator is the array shape.
   body=body.replace('np.sum((y == 0) | (y == 1))','y.shape[0]')
   expr='evaluate(ids, output_ids, y, outputs_y, reference, output_kind, p_negative, p_positive, cost_FP, cost_FN, bound)'
   code(ix,cid,sc,body,sig,[expr,expr.replace('ids, output_ids,','ids, output_ids[::-1],'),expr.replace('ids, output_ids, y, outputs_y, reference, output_kind','ids[y == 0], output_ids[y == 0], y[y == 0], outputs_y[y == 0], reference[y == 0], output_kind[y == 0]')],'Write required NumPy imports and implement evaluate plus quantities. Accept only the supplied foundation-model output kind. Verify matched identifiers and aligned label/output shapes. On mismatch return aligned=False,accepted=False,reason="unmatched observations"; on wrong output kind use reason="candidate is not the supplied foundation-model output kind". Otherwise return aligned=True,candidate,baseline,accepted,bound,limitations. Both candidate and baseline dictionaries include FP,TN,FN,TP,actual_negative_count,actual_positive_count,FPR,FNR,expected_cost,accuracy on the matched cohort. Guard rates/costs as None for empty actual groups. Acceptance is only defined candidate cost <= the fixed bound; undefined evidence never passes. Include limitations="Quality verdict is bounded to supplied order-task validation observations; no application construction, fitting or protected-test evidence is implied." Do not fit, change settings, rank approaches or use protected-test observations.',[mount('ds.validation_scores'),mount('ds.foundation_outputs'),mount('ds.acceptance_contract')])
  else:raise ValueError(cid)
  out['interactions'].append({'step_id':s['step_id'],'interaction':ix})
 output['tiles'].append(out)
(B/'interactions.json').write_text(json.dumps(output,indent=2)+'\n')
print('authored',sum(len(t['interactions']) for t in output['tiles']))
