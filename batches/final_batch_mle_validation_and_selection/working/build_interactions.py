import sys,json,re,copy
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from checkers import sandbox
P=Path('batches/final_batch_mle.region.validation_and_selection')
plans=json.load(open(P/'tile_plans.json')); screens=json.load(open(P/'screens.json')); glossary=json.load(open(P/'inputs/path_glossary_bundle.json')); registry=json.load(open(P/'scenario_asset_registry.json'))
G={b['context']['concept_id']:b for b in glossary['bundles']}; A={a['asset_id']:a for a in registry['assets']}
R=json.load(open('00_FINAL_PIPELINE_CORE/registry/runtimes.json'))['runtimes']
def col_letter(n):
 s=''
 while n:
  n,r=divmod(n-1,26);s=chr(65+r)+s
 return s
def records(a):
 x=A[a];return [dict(zip([c['name'] for c in x['columns']],r)) for r in x['rows']]
def feedback(c,t,first):
 f={'correct':{'message':'Your answer follows the declared validation evidence and its limits.'},'incorrect':{'message':'Check the conditioning population and the fixed evidence boundary; do not substitute a different decision contract.'},'hints':['Identify which observations supply the denominator.','Separate an observed validation result from claims it cannot establish.']}
 if True:
  rs=next(x for x in screens['tiles'] if x['tile_id']==t)['remediation_steps']; matches=[r for r in rs if c in r['concept_ids']];target=matches[min(0 if first else 1,len(matches)-1)] if matches else None
  if target:f['remediation_step_id']=target['step_id']
 return f
# Questions contain only concepts taught in the named check's facts.
Q={
 'task_metric_selection':('What can a validation confusion table establish?', ['Cohort precision, recall and actual-positive prevalence, but not calibration of individual probability scores.','Calibration of each individual score, because precision is a conditional frequency.','Recall conditions on predicted positives, while prevalence counts predictions.'],['These quantities describe the validation cohort, not individual-score calibration.','A cohort conditional frequency does not establish individual probability calibration.','Recall conditions on actual positives; prevalence is the actual-positive fraction.']),
 'model_acceptance_criteria':('Under zero cost for correct predictions, which predictive acceptance contract preserves the supplied fixed inputs and separate operating limits?', ['Require P(Y=0) × FPR × cost_FP + P(Y=1) × FNR × cost_FN <= the predeclared bound, and check operating limits separately.','Replace deployment class probabilities with whichever candidate’s validation prevalence gives the lowest cost.','Once expected cost passes, all operating limits automatically pass.'],['The cost requirement and operating eligibility remain separate.','Deployment probabilities and costs are fixed before comparison.','Predictive acceptance does not imply operating eligibility.']),
 'reference_baseline':('A validation cohort has no actual positives. What should the frozen reference report for FNR and any expected cost requiring it?', ['FNR and that expected cost are undefined.','FNR is zero because no positive errors were counted, so cost is defined.','FNR divides false negatives by all validation observations.'],['The actual-positive conditioning group is empty.','Zero errors do not define a rate with an empty conditioning group.','FNR conditions on actual positives, not the total cohort.']),
 'model_approach_decision':('After choosing among supplied approach records using the fixed validation rule, what preserves the evaluation boundary?', ['Freeze the supplied approach choice without new fitting or protected-test access.','Fit an additional approach on protected-test observations to confirm the choice.','Change the supplied requirements after seeing which approach wins.'],['Retain the bounded supplied-record decision.','Protected test observations must not inform fitting or choice.','The supplied requirements stay fixed during comparison.']),
 'sklearn_baseline_workflow':('How should validation predictions use the supplied preprocessing pipeline?', ['Fit on training observations and reuse the fitted preprocessing for validation prediction.','Refit preprocessing on validation observations before predicting them.','Fit on the combined training and validation observations.'],['Validation uses the training-fitted preprocessing.','Refitting on validation breaks the training-only fitting boundary.','Validation observations must not enter fitting.']),
 'decision_threshold_selection':('Which statement distinguishes a score from its thresholded decision?', ['A threshold converts a score into a class decision; score representation must be retained with the threshold.','Changing the threshold refits the underlying model.','A probability score and a decision_function score always share a meaningful default threshold.'],['Thresholds operate on the recorded score representation.','Threshold selection is a decision rule, not model refitting.','Threshold interpretation depends on score representation.']),
 'validation_candidate_comparison':('What evidence should determine the frozen candidate choice?', ['Matched validation evidence under the fixed rule, without protected-test information.','Protected-test performance used to break a validation tie.','Protected-test observations used to repair the lowest-cost candidate.'],['The choice is bounded to the declared validation evidence.','Using protected-test evidence for selection leaks information.','Protected-test evidence must not inform tuning or selection.']),
 'prediction_error_analysis':('For a predefined group’s supplied losses, what does mean plus population standard deviation describe?', ['The average loss and spread of those selected loss observations, using divisor N.','A causal explanation of the recurring failures.','Population standard deviation computed with divisor N−1.'],['These summaries describe the supplied loss observations.','Descriptive loss summaries do not establish a cause.','Population standard deviation uses N; N−1 is a different divisor.']),
 'slice_evaluation':('The declared slice summary uses ddof=0. Which calculation follows that instruction?', ['Compute the mean of each slice’s supplied losses and its standard deviation with divisor N.','Use N−1 regardless of the declared divisor.','Use the full cohort count as the denominator for every slice’s loss mean.'],['The divisor and selected observations must match the declared slice calculation.','N−1 contradicts ddof=0.','A slice mean uses the losses in that slice.']),
 'subgroup_risk_mitigation':('How is a subgroup’s contribution to deployment expected harm obtained?', ['Multiply subgroup-conditional expected harm by the supplied deployment subgroup probability.','Use the validation subgroup fraction as the deployment probability without further evidence.','Treat aggregate improvement as proof that every subgroup has acceptable harm.'],['Conditional harm and deployment population weighting are distinct quantities.','The validation fraction need not equal deployment probability.','An aggregate result does not establish subgroup suitability.']),
 'experiment_metric_logging':('What must a retained run-to-artifact association verify?', ['The run ID, repository directory, resolved local artifact path and actual code revision; reject a revision mismatch.','Only the artifact URI; a different code revision is acceptable.','Only the run’s display name, even if the run ID differs.'],['The retained lookup ties run, paths and actual revision together.','A revision mismatch must be rejected.','The run ID identifies the run; a display name does not replace it.']),
 'training_randomness':('What does a mean and population standard deviation over completed paired results summarize?', ['The average and spread of the selected numeric results using divisor N.','A guarantee of identical computation in every environment.','The probability of every future candidate win without regard to the supplied trials.'],['The summaries describe the selected completed results.','Controlled seeds do not establish universal deterministic replay.','The empirical summary is bounded to supplied trials.']),
 'validation_regularization':('Which parameter change increases regularization strength for the named estimator?', ['Increase Ridge alpha; decrease LogisticRegression C.','Increase both Ridge alpha and LogisticRegression C.','Decrease Ridge alpha; increase LogisticRegression C.'],['Ridge alpha and LogisticRegression C have opposite strength directions.','Larger C decreases LogisticRegression regularization strength.','Both changes weaken rather than strengthen their respective penalties.']),
 'bounded_hyperparameter_search':('Which evidence is excluded from bounded configuration search?', ['Protected-test observations for fitting preprocessing, tuning or selection.','Validation results under the predeclared protocol.','The declared configuration list and budget.'],['Protected-test evidence must remain outside the search.','Declared validation evidence is the basis of this search.','The supplied configurations and budget define the bounded search.']),
 'model_risk_documentation':('How should the single risk record handle existing policy fields?', ['Preserve permitted identities, task limits and foreseeable misuse without extending permission scope.','Expand permitted identities to match every observed grant.','Drop task limitations whenever aggregate quality improves.'],['The record preserves policy and records evidence-supported limits.','Observed grants do not redefine permitted scope.','Aggregate improvement does not remove documented task limits.']),
 'foundation_model_baseline_evaluation':('Which activity violates the supplied-output evaluation boundary?', ['Using protected-test observations to fit preprocessing or tune the evaluated system.','Scoring supplied outputs on the fixed labeled validation cohort.','Reporting cohort-bounded limitations against the reference.'],['Protected-test information must not enter fitting or tuning.','The fixed validation cohort is the declared evaluation evidence.','Bounded limitations belong in the supplied-output verdict.'])}

def choice(ix,c):
 q,opts,fb=Q[c.split('.')[-1]]
 ix['public']={'prompt':q,'selection':'single','shuffle':True,'options':[{'option_id':f'o{i+1}','text':v} for i,v in enumerate(opts)]}
 # Derive the key from the uniquely designated predicate-preserving option, not from a numeric dataset answer.
 ix['grading']={'correct_option_ids':[ix['public']['options'][0]['option_id']], 'option_feedback':{o['option_id']:{'message':m} for o,m in zip(ix['public']['options'],fb)}}

def formula(ix,asset,formula,prompt):
 cell='AZ2';ix['public']={'asset_ref':{'asset_id':asset},'sheet_name':'Evidence','target_cell':cell,'prompt':prompt+' Put the complete report in AZ2 as one formula; headers are in row 1 and all registry columns are shown in their original order.'}
 vals,err=sandbox.sheet_cell_values(registry,{'asset_ref':{'asset_id':asset},'sheet_name':'Evidence','cells':[{'ref':cell,'formula':formula}]})
 if err:raise RuntimeError(err)
 ix['grading']={'reference_formula':formula,'expected_value':vals[cell],'must_use_functions':sorted(set(re.findall(r'([A-Z][A-Z0-9.]*)\(',formula))),'tolerance':1e-9,'forbid_hardcoded_values':True}

def py(ix,c,starter,solution,mount_ids,expr='result',prompt=''):
 print('Building',c,flush=True)
 live=G[c]['practice_anchor']['live_code']
 ix['public']={'prompt':prompt,'runtime':{'kind':'python','version':R['python']['version'],'packages':['numpy','pandas']},'workspace':{'entry':'learner.py','files':[{'path':'learner.py','role':'editable','language':'python','content':starter}],'asset_mounts':[{'asset_id':a,'mount_path':a[3:]+'.csv'} for a in mount_ids]},'constraints':{k:live[k] for k in ['allowed_syntax','blocked_syntax']}}
 
 if 'sklearn' in solution: ix['public']['runtime']['packages'].append('scikit-learn')
 ix['grading']={'solution_files':[{'path':'learner.py','content':solution}],'tests':[{'test_id':'report','kind':'value_equals','spec':{'expr':expr,'expected':None},'visible':True,'message_on_fail':'The returned evidence record must follow the declared input contract.'}]}
 tables,_=sandbox._tables(registry,ix['public']['workspace']['asset_mounts'],{},[])
 script=sandbox._py_script('solution','learner.py',solution,sandbox._py_mounts(tables),[{'id':'report','kind':'expr','expr':expr}])
 r=sandbox.node_run(sandbox._py_job('python',ix['public']['runtime']['packages'],[script]),R['python']['runner'])['results']['solution']
 if not r['ok']:raise RuntimeError(r['error'])
 if not r['probes']['report']['ok']:raise RuntimeError(r['probes']['report'])
 ix['grading']['tests'][0]['spec']['expected']=r['probes']['report']['value']

# These top-level scaffolds provide the supplied infrastructure. Learners edit the
# named analysis lines; all scaffold statements remain unchanged in the solution.
LOAD='import numpy as np\nimport pandas as pd\n'
def frame(a,n):return f'{n} = pd.read_csv({a[3:]+".csv"!r})\n'
def simple_stat(ix,c,asset,group):
 scaffold=LOAD+frame(asset,'data')
 scaffold+=f"selected = data[data['eligible'].eq(True) & data[{group!r}].eq({True if group=='long_distance' else 'A'!r})].dropna(subset=['error','loss'])\n"
 scaffold+="errors = selected['error'].astype(bool).to_numpy()\nlosses = selected['loss'].to_numpy()\nref_errors = selected['reference_error'].astype(bool).to_numpy()\nref_losses = selected['reference_loss'].to_numpy()\n"
 if c.endswith('prediction_error_analysis'):
  edits="error_count = np.count_nonzero(errors)\nerror_probability = np.mean(errors)\nloss_mean = np.mean(losses)\nloss_std = np.std(losses, ddof=0)\nreference_probability = np.mean(ref_errors)\nreference_mean = np.mean(ref_losses)\nreference_std = np.std(ref_losses, ddof=0)\n"
  end="result = {'eligible_count':len(losses),'error_count':error_count,'error_probability':error_probability,'loss_mean':loss_mean,'loss_std':loss_std,'reference_error_probability':reference_probability,'reference_loss_mean':reference_mean,'reference_loss_std':reference_std,'finding':'Long-distance failures recur in this predefined validation group; this descriptive comparison does not establish a cause.'}\n"
 else:
  scaffold=LOAD+frame(asset,'data')+"a = data[data['eligible'].eq(True) & data['zone'].eq('A')].dropna(subset=['error','loss'])\nb = data[data['eligible'].eq(True) & data['zone'].eq('B')].dropna(subset=['error','loss'])\na_errors = a['error'].astype(bool).to_numpy()\nb_errors = b['error'].astype(bool).to_numpy()\na_losses = a['loss'].to_numpy()\nb_losses = b['loss'].to_numpy()\n"
  edits="a_probability = np.mean(a_errors)\nb_probability = np.mean(b_errors)\na_mean = np.mean(a_losses)\nb_mean = np.mean(b_losses)\na_std = np.std(a_losses, ddof=0)\nb_std = np.std(b_losses, ddof=0)\n"
  end="result = {'A':{'eligible_count':len(a_losses),'error_probability':a_probability,'loss_mean':a_mean,'loss_std':a_std},'B':{'eligible_count':len(b_losses),'error_probability':b_probability,'loss_mean':b_mean,'loss_std':b_std},'limitation':'Observed validation slice gap only; population disparity is not established.'}\n"
 names=re.findall(r'^(\w+) =',edits,re.M)
 starter=scaffold+'# Complete only the following analysis assignments.\n'+''.join(n+' = None\n' for n in names)+end
 prompt='Complete the named analysis assignments using NumPy; retain the supplied loading and result-record scaffolding. Use ddof=0. '+('Analyze the predefined eligible long-distance group and its same-cohort reference. ' if c.endswith('prediction_error_analysis') else 'Analyze eligible zone A and B observations separately. ')+'The result dictionary must retain every scaffold field, counts, conditional error proportions, loss means and population standard deviations, and the bounded finding. Missing eligibility/error/loss observations are excluded by the scaffold.'
 py(ix,c,starter,scaffold+edits+end,[asset],prompt=prompt)

OUT={k:plans[k] for k in ['schema_version','path_id','batch_id']};OUT['kind']='interactions_part';OUT['tiles']=[]
for t in plans['tiles']:
 entries=[];seen=set(); total=sum(s['type'] in ['check','hands_on'] for s in t['steps'])
 for s in t['steps']:
  if s['type'] not in ['check','hands_on']:continue
  c=s['concept_ids'][0];short=c.split('.')[-1];b=G[c]
  anchors=[a for a in s['anchors'] if '#assessment:' in a]
  measures=[]
  for a in anchors:
   cap=a.split('#assessment:')[1];an=next(a for a in b['assessment_anchors'] if a['capability']==cap)
   measures.append({'concept_id':c,'capability':cap,'fact_ids':an['fact_ids']})
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if not entries else ('stretch' if len(entries)==total-1 else 'core'),'grading_mode':'client','standalone':False,'measures':measures,'anchors':s['anchors'],'feedback':feedback(c,t['tile_id'],c not in seen)};seen.add(c)
  if s['type']=='check':choice(ix,c)
  elif ix['type']=='formula_entry':
   if short=='task_metric_selection':
    f='="precision="&TEXT(B2/(B2+C2),"0.00")&"; recall="&TEXT(B2/(B2+D2),"0.00")&"; prevalence="&TEXT((B2+D2)/(B2+C2+D2+E2),"0.00")&"; metric=recall; precision conditions on predicted positives; recall conditions on actual positives; cohort frequencies do not establish individual-score calibration; missed late orders are prioritized"'
    prompt='Create a report with this exact label order: precision (two decimals), recall (two decimals), prevalence (two decimals); then metric=recall and the interpretations shown below. Use the TP, FP, FN and TN count cells, not precomputed metrics. The task prioritizes catching actual late orders over avoiding unnecessary alerts. Report text after the numeric values must be: "; metric=recall; precision conditions on predicted positives; recall conditions on actual positives; cohort frequencies do not establish individual-score calibration; missed late orders are prioritized". Separate the numeric fields with "; ".'
    formula(ix,'ds.metric_summary',f,prompt)
   elif short in ['model_approach_decision','validation_candidate_comparison']:
    asset='ds.approach_records' if short=='model_approach_decision' else 'ds.candidate_records'; cols=[x['name'] for x in A[asset]['columns']]
    def cell(n,r):return col_letter(cols.index(n)+1)+str(r)
    pieces=[];costs=[];eligible=[]
    contract=records('ds.acceptance_contract')[0];sentinel=1+contract['deployment_negative_probability']*contract['cost_FP']+contract['deployment_positive_probability']*contract['cost_FN']
    for i,row in enumerate(A[asset]['rows'],2):
     tp,fp,fn,tn=[cell(n,i) for n in ['TP','FP','FN','TN']];neg=f'({fp}+{tn})';pos=f'({fn}+{tp})';cost=f'({contract["deployment_negative_probability"]}*{fp}/{neg}*{contract["cost_FP"]}+{contract["deployment_positive_probability"]}*{fn}/{pos}*{contract["cost_FN"]})'
     cond='AND('+','.join([f'{neg}>0',f'{pos}>0',f'{cell("cohort_id",i)}="orders_100"',cost+'<='+str(contract['expected_cost_bound'])]+[cell(n,i) for n in cols if n.endswith('_met')])+')'
     eligible.append(cond);costs.append(f'IF({cond},{cost},{sentinel})')
     pieces.append(f'{cell(cols[0],i)}&":negative_count="&{neg}&",positive_count="&{pos}&",FPR="&IF({neg}=0,"undefined",TEXT({fp}/{neg},"0.0000"))&",FNR="&IF({pos}=0,"undefined",TEXT({fn}/{pos},"0.0000"))&",cost="&IF(OR({neg}=0,{pos}=0),"undefined",TEXT({cost},"0.0000"))&",eligible="&IF({cond},"yes","no: unmatched cohort, undefined rate, cost or operating requirement fails")')
    selected='"none"'
    for i in reversed(range(len(costs))):selected=f'IF(AND({eligible[i]},{costs[i]}=MIN('+','.join(costs)+f')),{cell(cols[0],i+2)},{selected})'
    f='='+('&"; "&'.join(pieces))+'&"; selected="&'+selected+'&"; fixed deployment P0=0.80,P1=0.20,cost_FP=1,cost_FN=5; validation-only frozen choice"'
    if short=='model_approach_decision':f+='&"; maintenance="&'+('&" | "&'.join(cell('maintenance_responsibility',r) for r in range(2,5)))
    prompt='Return one semicolon-separated report in declared row order. For each identity output identity:negative_count=N,positive_count=N,FPR=x.xxxx,FNR=x.xxxx,cost=x.xxxx,eligible=yes or eligible=no: unmatched cohort, undefined rate, cost or operating requirement fails. Calculate from confusion counts. Empty conditioning groups must say undefined, not zero. Eligibility requires orders_100, all supplied operating predicates and cost <=0.30. Select minimum cost among eligible records, first declared row on ties, or none. Append "; selected=<identity>; fixed deployment P0=0.80,P1=0.20,cost_FP=1,cost_FN=5; validation-only frozen choice".'
    if short=='model_approach_decision':prompt+=' Append "; maintenance=" followed by each supplied maintenance_responsibility in declared order, separated by " | ". This retains all three alternatives’ matched quality, operating and maintenance evidence without new fitting.'
    formula(ix,asset,f,prompt)
   else:
    asset='ds.mitigation_records';cols=[x['name'] for x in A[asset]['columns']]
    def cell(n,r):return col_letter(cols.index(n)+1)+str(r)
    parts=[];harm={};operating=[]
    for r in range(2,6):
     fp,tn,fn,tp=[cell(n,r) for n in ['FP','TN','FN','TP']];neg=f'({fp}+{tn})';pos=f'({fn}+{tp})';cost=f'({cell("deployment_negative_probability",r)}*{fp}/{neg}*{cell("cost_FP",r)}+{cell("deployment_positive_probability",r)}*{fn}/{pos}*{cell("cost_FN",r)})';prev=f'{cell("cohort_count",r)}/{cell("cohort_count",r+1 if r in [2,4] else r)}';harm[r]=cost

     parts.append(f'{cell("system",r)}&"/"&{cell("scope",r)}&":FPR="&IF({neg}=0,"undefined",TEXT({fp}/{neg},"0.0000"))&",FNR="&IF({pos}=0,"undefined",TEXT({fn}/{pos},"0.0000"))&",harm="&IF(OR({neg}=0,{pos}=0),"undefined",TEXT({cost},"0.0000"))&",validation_fraction="&TEXT({prev},"0.0000")&",deployment_weight="&TEXT({cell("deployment_subgroup_probability",r)},"0.0000")'+(f'&",weighted_harm="&IF(OR({neg}=0,{pos}=0),"undefined",TEXT({cost}*{cell("deployment_subgroup_probability",r)},"0.0000"))' if r in [2,4] else ''))
    bound=records('ds.acceptance_contract')[0]['expected_cost_bound']
    decision=f'IF(AND({harm[4]}<{harm[2]},{harm[5]}<={harm[3]},{harm[5]}<={bound}),"recommend supplied mitigation for measured validation harm reduction, conditional on unsupplied operating requirements","do not retain supplied mitigation under the declared improvement rule")'
    f='='+('&"; "&'.join(parts))+'&"; decision="&'+decision+'&"; representation beyond supplied sample is not established; operating eligibility and subgroup suitability remain unresolved without their separate criteria"'
    prompt='Report each record in declared order as system/scope:FPR=x.xxxx,FNR=x.xxxx,harm=x.xxxx,validation_fraction=x.xxxx,deployment_weight=x.xxxx. Add ,weighted_harm=x.xxxx for affected_subgroup rows only. Compute rates from counts and harm from supplied deployment class probabilities and costs; guard empty groups with undefined. Validation fraction is subgroup count / matched overall count (overall rows report 1.0000); deployment weighting is independent of that fraction. Separate records with "; ". The predeclared improvement rule is: affected-subgroup harm strictly decreases, overall harm does not increase and satisfies the fixed overall cost bound, and overall cost satisfies the fixed bound. Operating requirements are not supplied here; retaining a mitigation remains conditional on checking them separately. Append "; decision=" followed by "recommend supplied mitigation for measured validation harm reduction, conditional on unsupplied operating requirements" if the rule passes, else "do not retain supplied mitigation under the declared improvement rule"; then append "; representation beyond supplied sample is not established; operating eligibility and subgroup suitability remain unresolved without their separate criteria". This improvement verdict does not assert subgroup acceptance or universal suitability.'
    formula(ix,asset,f,prompt)
  elif ix['type']=='external_proof':
   grants=records('ds.access_grants'); permitted=', '.join(r['identity'] for r in grants if r['policy_permitted']);mismatch=', '.join(r['identity'] for r in grants if r['observed_grant'] and not r['policy_permitted'])
   criteria=[f'Preserve all existing policy fields and the permitted identity {permitted}; identify the observed {mismatch} grant as out of scope without expanding permissions.','Record sample_image.credential_field and its exposure-handling limitation without reproducing any credential or secret.','Retain supplied task limits and foreseeable misuse from the policy evidence.','Cite supported segment evidence and explain that aggregate improvement does not establish universal suitability.']
   ix['public']={'instruction':'Submit a single text risk record using the earlier supplied risk-policy evidence and access grants. No secrets may be included. Every checklist item is required; this is documentation under the existing policy, not a new authorization policy.','evidence_kinds':['text'],'checklist':criteria}
   ix['grading']={'mode':'manual','rubric':[{'criterion':x,'weight':1} for x in criteria]}
  elif ix['type']=='table_select':
   asset='ds.execution_contract';row=records(asset)[0]
   tasks=[('override','Select the cell containing the resolved explicit trial-setting override, not the default.','override_trial_setting'),('default','Select the default trial-setting cell, which is distinct from the explicit override.','default_trial_setting')]
   ix['public']={'asset_ref':{'asset_id':asset},'intro':'Inspect the supplied execution contract. This table contains configuration inputs only, not a retrieved MLflow run or artifact evidence.','tasks':[{'task_id':k,'prompt':q,'target_kind':'cell'} for k,q,col in tasks]}
   ix['grading']={'answers':[{'task_id':k,'row':{'where':{'default_trial_setting':row['default_trial_setting']},'occurrence':0},'column':col,'expect_value':row[col]} for k,q,col in tasks]}
  elif short=='model_acceptance_criteria':
   f='="FPR denominator="&E2&"; FNR denominator="&E3&"; expected_cost="&IF(OR(E2=0,E3=0),"undefined",TEXT(B2*C2*D2+B3*C3*D3,"0.00"))&"; predictive_requirement=cost<="&TEXT(Contract!F2,"0.00")&"; predictive_verdict="&IF(OR(E2=0,E3=0),"unresolved",IF(B2*C2*D2+B3*C3*D3<=Contract!F2,"pass","fail"))&"; operating_limits=separate supplied predicates, no numeric latency bound supplied; deployment probabilities and error costs fixed before comparison"'
   vals,err=sandbox.sheet_cell_values(registry,{'asset_ref':{'asset_id':'ds.acceptance_terms'},'sheet_name':'Terms','cells':[]})
   pub={'prompt':'In Terms!AZ2 write a single formula report: FPR denominator=<actual-negative count>; FNR denominator=<actual-positive count>; expected_cost=<two decimals or undefined>; predictive_requirement=cost<=<Contract bound to two decimals>; predictive_verdict=<pass, fail or unresolved>; operating_limits=separate supplied predicates, no numeric latency bound supplied; deployment probabilities and error costs fixed before comparison. Use the supplied class probabilities, conditional rates and error costs from Terms rows 2 and 3. Guard empty conditioning groups. Compare cost to Contract!F2; do not invent operating limits or infer overall eligibility. Retain all contract inputs unchanged.','runtime':{'kind':'spreadsheet','version':R['spreadsheet']['version']},'workspace':{'entry':'book.sheet','files':[{'path':'book.sheet','role':'editable','language':'sheet','content':'// Enter the predictive contract report in Terms!AZ2.\n'}],'asset_mounts':[{'asset_id':'ds.acceptance_terms','mount_path':'Terms.csv'},{'asset_id':'ds.acceptance_contract','mount_path':'Contract.csv'}]},'constraints':{'allowed_syntax':['IF','OR','TEXT','cell references','cross-sheet or sheet reference','+ - * /','comparison operators','& (concatenation)','parentheses','numbers','text in quotes'],'blocked_syntax':[]}}
   ix['public']=pub
   tables,_=sandbox._tables(registry,pub['workspace']['asset_mounts'],{},[])
   code='Terms!AZ2: '+f+'\n'
   rr=sandbox.node_run({'scripts':[sandbox._sheet_script('solution',code,tables,[{'id':'report','kind':'cell','ref':'Terms!AZ2'}])]},R['spreadsheet']['runner'])['results']['solution']
   expected=rr['probes']['report']['value']
   ix['grading']={'solution_files':[{'path':'book.sheet','content':code}],'tests':[{'test_id':'report','kind':'cell_equals','spec':{'cell':'Terms!AZ2','expected':expected},'visible':True,'message_on_fail':'Recheck the fixed expected-cost contract and empty-group handling.'}]}
  elif short in ['prediction_error_analysis','slice_evaluation']:simple_stat(ix,c,'ds.slice_observations','long_distance' if short=='prediction_error_analysis' else 'zone')
  else:
   # Remaining Python exercises are generated below by a task-specific scaffold.
   from task_scaffolds import build
   starter,solution,assets,prompt=build(short,A,G)
   py(ix,c,starter,solution,assets,prompt=prompt)
  entries.append({'step_id':s['step_id'],'interaction':ix})
 OUT['tiles'].append({'tile_id':t['tile_id'],'interactions':entries})
(P/'interactions.json').write_text(json.dumps(OUT,indent=2)+'\n')
print('Wrote',sum(len(t['interactions']) for t in OUT['tiles']),'interactions')
