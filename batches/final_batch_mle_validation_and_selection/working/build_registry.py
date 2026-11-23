import json, re, csv, math, hashlib
from pathlib import Path
from datetime import datetime, timezone
B=Path('batches/final_batch_mle.region.validation_and_selection')
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
bs=g['bundles']; by={b['context']['concept_id'].split('.')[-1]:b for b in bs}
def text(k):
 b=by[k]
 return '\n'.join(t['content'] for t in b['teaching_blocks'])+'\n'+json.dumps(b['practice_anchor'],ensure_ascii=False)+'\n'+json.dumps(b['visual_anchor'],ensure_ascii=False)
def ex(k):return '\n'.join(t['content'] for t in by[k]['teaching_blocks'] if t['purpose']=='example')
def grab(k,pattern):
 m=re.search(pattern,text(k)); assert m,(k,pattern)
 return tuple(float(v) if '.' in v else int(v) for v in m.groups())
sid='scn.order_validation'
# Vocabulary is mined only from the supplied teaching blocks and anchors.
alltext='\n'.join(text(k) for k in by)
terms=['late-order','orders','order task','training','validation','protected test','actual positives','actual negatives','predicted positives','TP','FP','FN','TN','precision','recall','accuracy','prevalence','FPR','FNR','MAE','MSE','expected error cost','deployment probabilities','false-positive cost','false-negative cost','latency','scale','training-cost','serving-cost','maintenance','deployment compatibility','classical','neural','managed ML service','most-frequent','LogisticRegression','Ridge','alpha','C','random_state','RandomState','decision_function','X_train','y_train','X_validation','y_validation','long-distance','per-example loss','zone A','zone B','ddof=0','MLflow','mlflow','trial_setting','run_id','artifact_uri','repository revision','diagnostic file','GridSearchCV','RandomizedSearchCV','best_params_','cv_results_','n_iter','foundation-model','identity A','A and B','credential','foreseeable misuse']
vocab=[w for w in terms if w in alltext]
vocab+=sorted(set(re.findall(r'(?<![\w.])\d+(?:\.\d+)?(?![\w.])',alltext)),key=lambda v:(float(v),v))
# Include verbatim fixture sentences so no example domain is lost in keyword mining.
for k in by:
 first=ex(k).split('\n')[0]
 vocab.append(first)
R={'schema_version':'1.0','kind':'scenario_asset_registry','path_id':g['path_id'],'batch_id':B.name,'scenarios':[{'scenario_id':sid,'name':'Fictional order-model validation desk','domain':'order prediction','summary':'A fictional delivery team evaluates supplied late-order predictions on authored training and validation fixtures. Fixed deployment-cost assumptions and separate operating predicates govern validation-only decisions. Small, explicitly separate cohorts support confusion-table arithmetic, descriptive slice analysis, paired trials, and supplied-output evaluation; no protected-test observations or real credentials are included.','glossary_example_vocab':list(dict.fromkeys(vocab))}],'assets':[],'provenance':{'generated_at':datetime.now(timezone.utc).isoformat()}}
assets={}
def col(n,t='number',role=None,desc=None):
 c={'name':n,'type':t,'semantic_role':role or ('numerical' if t in ('number','integer') else 'categorical' if t=='boolean' else 'text')}
 if role in ('identifier','categorical') and t=='integer': c['numeric_looking_label']=True
 if desc:c['description']=desc
 return c
def cat(n):return col(n,'string','categorical')
def ident(n):return col(n,'string','identifier')
def label(n):return col(n,'integer','categorical','Binary class label, not a quantitative measurement.')
def boolean(n):return col(n,'boolean','categorical')
def ds(name,title,columns,rows,description,variants=None):
 a={'asset_id':'ds.'+name,'asset_kind':'dataset','scenario_id':sid,'title':title,'description':description,'columns':columns,'rows':rows,'provenance':'authored','variants':variants or []}
 R['assets'].append(a); assets[name]=a; return a
def edge(a,name,ops,purpose,issues=None):
 a['variants'].append({'variant_id':'v.'+name,'derived_from':a['asset_id'],'purpose':purpose,'ops':ops,'planted_issues':issues or []})
def setcell(where,column,value):return {'op':'set_cell','where':where,'occurrence':0,'column':column,'value':value}
# Numeric examples are extracted; displayed arithmetic and all expected quantities are computed.
TP,FP,FN,TN=grab('task_metric_selection',r'TP=(\d+), FP=(\d+), FN=(\d+) and TN=(\d+)')
n=TP+FP+FN+TN; npos=TP+FN; nneg=FP+TN
p1,p0,c_fp,c_fn=grab('model_acceptance_criteria',r'positive probability of (\d+\.\d+), negative probability (\d+\.\d+), false-positive cost (\d+) and false-negative cost (\d+)')
fpr,fnr=grab('model_acceptance_criteria',r'validation FPR is (\d+\.\d+) and FNR is (\d+\.\d+)')
(bound,)=grab('model_acceptance_criteria',r'predeclared bound of (\d+\.\d+)')
def metrics(tp,fp,fn,tn):
 neg=fp+tn;pos=fn+tp;total=neg+pos
 fpr_=fp/neg if neg else None;fnr_=fn/pos if pos else None
 return [pos,neg,total,tp/(tp+fp) if tp+fp else None,tp/pos if pos else None,pos/total if total else None,fpr_,fnr_,None if fpr_ is None or fnr_ is None else p0*fpr_*c_fp+p1*fnr_*c_fn]
def counts_for(cost):
 # Construct fictional counts with the example's actual-class totals. Prefer FNR from acceptance fixture.
 options=[]
 for fn in range(npos+1):
  for fp in range(nneg+1):
   if math.isclose(p0*fp/nneg*c_fp+p1*fn/npos*c_fn,cost,abs_tol=1e-10):options.append((abs(fn-npos*fnr),fp,fn))
 assert options,cost
 _,fp,fn=min(options);return [npos-fn,fp,fn,nneg-fp]
countcols=[col('TP','integer'),col('FP','integer'),col('FN','integer'),col('TN','integer')]
metriccols=[col('actual_positive_count','integer'),col('actual_negative_count','integer'),col('cohort_count','integer'),col('precision'),col('recall'),col('validation_prevalence'),col('FPR'),col('FNR'),col('expected_error_cost')]
conf=ds('confusion_counts','Late-order confusion cells',[cat('outcome'),label('actual_label'),label('predicted_label'),col('count','integer')],[[k,y,p,c] for k,y,p,c in [('TP',1,1,TP),('FP',0,1,FP),('FN',1,0,FN),('TN',0,0,TN)]],'Exact glossary confusion fixture. The two label columns are categorical even though encoded with digits.')
ds('metric_summary','Confusion-table denominators and computed metrics',[ident('cohort_id')]+countcols+metriccols,[['metric_example',TP,FP,FN,TN]+metrics(TP,FP,FN,TN)],'Calculated from ds.confusion_counts; aggregate outcomes do not establish probability calibration.')
err1,err2=grab('task_metric_selection',r'errors of (\d+) and (\d+) give MAE')
ds('regression_errors','Two regression residuals',[ident('observation_id'),col('error'),col('absolute_error'),col('squared_error')],[[f'reg_error_{i}',e,abs(e),e*e] for i,e in enumerate((err1,err2),1)],'Separate regression example; absolute and squared errors are computed from extracted residuals.')
ds('regression_error_summary','Regression error averages',[col('MAE'),col('MSE')],[[(abs(err1)+abs(err2))/2,(err1**2+err2**2)/2]],'Computed from the two residuals, not a classification score.')
ds('acceptance_contract','Precommitted predictive contract',[col('deployment_negative_probability'),col('deployment_positive_probability'),col('cost_FP'),col('cost_FN'),col('correct_prediction_cost'),col('expected_cost_bound'),cat('selection_rule'),cat('tie_rule'),cat('empty_group_rule'),col('ddof','integer'),col('operating_limit','number',desc='No numeric operating limit is supplied by the glossary; leave unresolved rather than invent one.')],[[p0,p1,c_fp,c_fn,0,bound,'minimum expected cost among matched eligible records','first in declared order','undefined rate; ineligible when required',0,None]],'Fixed decision inputs from the glossary. Training prevalence and validation prevalence are not replacements for the supplied deployment probabilities. Operating predicates are separate; the formula example supplies no numeric latency bound.')
a_tp=npos-round(npos*fnr);a_fp=round(nneg*fpr);a_fn=npos-a_tp;a_tn=nneg-a_fp
acceptrows=[]
for y,prob,rate,cost,count in [(0,p0,fpr,c_fp,nneg),(1,p1,fnr,c_fn,npos)]:acceptrows.append([y,prob,rate,cost,count,prob*rate*cost])
a=ds('acceptance_terms','Expected-cost contributions by actual class',[label('actual_label'),col('deployment_class_probability'),col('conditional_error_rate'),col('error_cost'),col('conditioning_count','integer'),col('weighted_contribution')],acceptrows,'Authored actual-class counts consistent with the exact supplied rates. Sum contributions and compare to the separate contract bound; no latency verdict is implied.')
edge(a,'empty_acceptance_positive',[setcell({'actual_label':1},'conditioning_count',0),setcell({'actual_label':1},'conditional_error_rate',None),setcell({'actual_label':1},'weighted_contribution',None)],'Empty actual-positive evidence leaves FNR and the cost unresolved.')
# Reference training fixture and separate regression targets.
wordnum={'eight':8,'two':2,'six':6,'five':5,'three':3,'ten':10,'first':1}
m=re.search(r'training has (\w+) negative and (\w+) positive labels',ex('reference_baseline'));zeros,ones=[wordnum[v] for v in m.groups()]
ref_train=ds('reference_train','Reference-only training cohort',[ident('observation_id'),col('feature_1'),label('y_train')],[[f'ref_train_{i+1}',float(i),int(i>=zeros)] for i in range(zeros+ones)],'Eight negative and two positive training labels as taught. Feature values are authored; training and validation identifiers are distinct.')
targets=grab('reference_baseline',r'targets (\d+), (\d+) and (\d+)')
ds('regression_targets','Separate mean-reference targets',[ident('observation_id'),col('target')],[[f'reg_train_{i}',v] for i,v in enumerate(targets,1)],'Training targets for the glossary regression reference; derive mean and population standard deviation from these rows.')
# Six-row, two-feature estimator fixture, not the ten-row reference fixture.
shape_n,shape_d=grab('sklearn_baseline_workflow',r'X_train has shape \((\d+), (\d+)\)')
(train_seed,)=grab('sklearn_baseline_workflow',r'random_state=(\d+)')
train=ds('orders_train','Six-order estimator training inputs',[ident('observation_id'),col('feature_1'),col('feature_2'),label('y_train')],[[f'train_{i+1}',float(i-shape_n/2),float((i*2)%5),int(i>=shape_n/2)] for i in range(shape_n)],'Authored numerical features; exact glossary X_train and y_train dimensions. Feature columns alone form X_train.')
val=ds('orders_validation','Held-out aligned estimator inputs',[ident('observation_id'),col('feature_1'),col('feature_2'),label('y_validation')],[[f'validation_{i+1}',float(i-shape_n/2)+0.25,float((i*3)%5),int(i>=shape_n/2)] for i in range(shape_n)],'Separate authored validation inputs and binary targets; observation IDs preserve correspondence. Never used to fit preprocessing.')
edge(val,'validation_no_positives',[{'op':'drop_rows','where':{'y_validation':1}}],'Undefined FNR test; retain negative conditioning group.')
edge(val,'validation_no_negatives',[{'op':'drop_rows','where':{'y_validation':0}}],'Undefined FPR test; retain positive conditioning group.')
edge(val,'validation_bad_alignment',[setcell({'observation_id':val['rows'][0][0]},'observation_id','unmatched_validation')],'Declared validation identifiers do not match the expected cohort.')
# Candidate cost records and separate approach records.
basecost,bcost,ccost=grab('validation_candidate_comparison',r'expected costs are (\d+\.\d+) and (\d+\.\d+).*?C reports (\d+\.\d+)')
classcost,neuralcost=grab('model_approach_decision',r'classical option has cost (\d+\.\d+).*?neural option has cost (\d+\.\d+)')
operating=['latency_requirement_met','scale_requirement_met','training_cost_requirement_met','serving_cost_requirement_met','maintenance_requirement_met','deployment_compatibility_met']
opcols=[boolean(k) for k in operating]
ccols=[ident('candidate_id'),ident('cohort_id')]+countcols+metriccols+opcols
candrows=[]
for name,cohort,cost in [('A','orders_100',basecost),('B','orders_100',bcost),('C','other_orders_100',ccost),('D','orders_100',classcost)]:
 cnt=counts_for(cost);candrows.append([name,cohort]+cnt+metrics(*cnt)+[True]*len(operating))
candidates=ds('candidate_records','Baseline and three candidate records',ccols,candrows,'A and B reproduce the taught 100-order comparison. C has a different cohort and must be excluded despite lower cost. D is an authored third candidate with a latency predicate failure. Predicate verdicts, not invented numeric operating bounds, are supplied separately from cost.')
candidates['rows'][-1][-len(operating)]=False
edge(candidates,'candidates_none_eligible',[setcell({'candidate_id':r[0]},'deployment_compatibility_met',False) for r in candrows],'All candidate operating predicates fail; return no selection rather than forcing a winner.')
approws=[]
for name,kind,delivery,cost,latency,maint in [('custom_classical','classical','custom',classcost,True,'owner maintains task model and infrastructure'),('custom_neural','neural','custom',neuralcost,False,'owner maintains task model and infrastructure'),('managed_service','classical','managed',basecost,True,'service supplies training or hosting infrastructure; owner retains custom task-model choices')]:
 cnt=counts_for(cost);approws.append([name,kind,delivery,'orders_100']+cnt+metrics(*cnt)+[latency]+[True]*(len(operating)-1)+[maint])
ds('approach_records','Classical, neural, and managed operating records',[ident('alternative_id'),cat('model_family'),cat('delivery_mode'),ident('cohort_id')]+countcols+metriccols+opcols+[col('maintenance_responsibility','string','text')],approws,'Authored matched records consistent with the taught classical cost and neural latency failure. Operating predicates are precommitted Boolean requirements, not numeric limits invented after results. Managed infrastructure does not imply ownership of all task-model choices.')
# Threshold scores: produce exact taught eligible costs, monotonically changing decisions.
(score,lo,hi)=grab('decision_threshold_selection',r'score (\d+\.\d+).*?threshold (\d+\.\d+).*?threshold (\d+\.\d+)')
tcost1,tcost2=grab('decision_threshold_selection',r'costs (\d+\.\d+) and (\d+\.\d+)')
c1=counts_for(tcost1);c2=counts_for(tcost2)
assert c1[0]==c2[0] and c1[1]>=c2[1]
scorerows=[]
for y,amt,s in [(1,c1[0],p0),(1,c1[2],lo/2),(0,c2[1],p0),(0,c1[1]-c2[1],score),(0,c1[3],lo/2)]:
 for _ in range(amt):scorerows.append([f'order_{len(scorerows)+1:03}', 'orders_100',y,s,0])
scores=ds('validation_scores','One fixed labeled cohort with unchanged scores',[ident('observation_id'),ident('cohort_id'),label('actual_label'),col('score'),label('reference_output')],scorerows,'Authored probability-score fixture. The glossary score 0.60 changes decision at cutoffs 0.50 and 0.70 without changing the score. Reference outputs are training-majority predictions.')
edge(scores,'scores_no_positives',[{'op':'drop_rows','where':{'actual_label':1}}],'Required FNR is undefined.')
edge(scores,'scores_no_negatives',[{'op':'drop_rows','where':{'actual_label':0}}],'Required FPR is undefined.')
edge(scores,'scores_none_eligible',[setcell({'observation_id':r[0]},'score',p0) for r in scorerows],'All predictions are positive at both cutoffs; neither cost satisfies the fixed bound.')
thresholds=ds('thresholds','Declared threshold candidates',[col('threshold'),cat('score_representation'),col('declared_order','integer')],[[v,'probability',i] for i,v in enumerate((lo,hi))],'Use predicted positive iff score >= threshold; retain the fixed declared-order tie policy.')
trs=[]
for t in (lo,hi):
 pred=[int(r[3]>=t) for r in scorerows];cnt=[sum(r[2]==y and p==z for r,p in zip(scorerows,pred)) for y,z in [(1,1),(0,1),(1,0),(0,0)]];ms=metrics(*cnt)
 trs.append([t]+cnt+ms+[ms[-1]<=bound])
ds('threshold_records','Computed threshold validation evidence',[col('threshold')]+countcols+metriccols+[boolean('predictive_requirement_met')],trs,'All expected counts and cost values calculated from ds.validation_scores; selection logic is left to the learner.')
found=ds('foundation_outputs','Supplied foundation output file aligned to validation',[ident('observation_id'),ident('cohort_id'),cat('output_kind'),label('foundation_output')],[[r[0],r[1],'foundation-model',int(r[3]>=lo)] for r in scorerows],'One supplied foundation-model output set on the same labeled validation IDs. This authored file represents supplied outputs, not model construction or training.')
edge(found,'foundation_wrong_cohort',[setcell({'observation_id':found['rows'][0][0]},'cohort_id','other_orders_100')],'Reject a candidate output from a different cohort.')
edge(found,'foundation_missing_observation',[{'op':'drop_rows','where':{'observation_id':found['rows'][0][0]}}],'Reject incomplete observation correspondence.')
edge(found,'foundation_duplicate',[{'op':'duplicate_row','where':{'observation_id':found['rows'][0][0]},'occurrence':0,'insert':'end'}],'Reject duplicate output identifiers.',[{'issue_id':'issue.duplicate_foundation','kind':'duplicate_row','locations':[{'where':{'observation_id':found['rows'][0][0]},'occurrence':1,'column':'observation_id'}],'description':'Second occurrence duplicates an entire foundation output row.'}])
# Descriptive slices and localized error analysis share a separate 60-order cohort.
m=re.search(r'zone A has (\w+) errors among (\d+) eligible examples and zone B has (\w+) among (\d+)',ex('slice_evaluation'))
aerr,acount,berr,bcount=wordnum[m[1]],int(m[2]),wordnum[m[3]],int(m[4])
m=re.search(r'group contains (\d+) eligible orders and (\w+) errors',ex('prediction_error_analysis'));longcount,longerr=int(m[1]),wordnum[m[2]]
slicerows=[]
for zone,count,errors in [('A',acount,aerr),('B',bcount,berr)]:
 for i in range(count):
  error=i<errors
  # The predefined long-distance set contains both zones' errors and enough nonerrors to total 20.
  long=error or (zone=='A' and errors<=i<errors+longcount-longerr)
  ref_error=i<errors+2
  slicerows.append([f'slice_{len(slicerows)+1:03}','slices_60',zone,True,long,error,float(error),ref_error,float(ref_error),float(5+i*2)])
# Add ineligible examples to distinguish masking from ignoring eligibility; no change to the taught eligible counts.
for zone in ('A','B'):slicerows.append([f'ineligible_{zone}','slices_60',zone,False,True,True,1.0,True,1.0,100.0])
slices=ds('slice_observations','Predefined zones and long-distance observations',[ident('observation_id'),ident('cohort_id'),cat('zone'),boolean('eligible'),boolean('long_distance'),boolean('error'),col('loss'),boolean('reference_error'),col('reference_loss'),col('distance','number',desc='Authored numerical feature for descriptive summaries; no causal interpretation.')],slicerows,'Separate authored cohort with A: 2/40, B: 6/20 and long-distance: 8/20 among eligible observations. Loss is authored zero-one loss; require population divisor ddof=0. Ineligible rows must be excluded. Same-cohort reference evidence is supplied.')
edge(slices,'empty_zone_B',[{'op':'drop_rows','where':{'zone':'B','eligible':True}}],'No eligible B observations: error probability and loss summaries must be undefined.')
summary=[]
for name,predicate in [('A',lambda r:r[2]=='A'),('B',lambda r:r[2]=='B'),('long-distance',lambda r:r[4])]:
 rs=[r for r in slicerows if r[3] and predicate(r)]; losses=[r[6] for r in rs]; mean=sum(losses)/len(losses);std=math.sqrt(sum((v-mean)**2 for v in losses)/len(losses))
 summary.append([name,len(rs),sum(r[5] for r in rs),sum(r[5] for r in rs)/len(rs),mean,std,0])
ds('slice_summary','Computed conditional slice summaries',[cat('slice'),col('eligible_count','integer'),col('error_count','integer'),col('error_probability'),col('loss_mean'),col('loss_std'),col('ddof','integer')],summary,'Computed from ds.slice_observations. Sample differences are not population-disparity or causal evidence.')
# Harm records: use the given subgroup probabilities without substituting validation prevalence.
subp,subharm,mitigharm=grab('subgroup_risk_mitigation',r'probability of the subgroup is (\d+\.\d+).*?harm.*?is (\d+\.\d+).*?changes the subgroup harm to (\d+\.\d+)')
harmrows=[]
for system,sh,ocost in [('reference',subharm,basecost),('mitigation',mitigharm,bcost)]:
 for scope,cost in [('affected_subgroup',sh),('overall',ocost)]:
  cnt=counts_for(cost)
  # Scale exact proportional counts so subgroup is a smaller observed sample, while rates remain exact.
  divisor=math.gcd(*cnt) if scope=='affected_subgroup' else 1
  cnt=[v//divisor if scope=='affected_subgroup' else v*2 for v in cnt];ms=metrics(*cnt)
  harmrows.append([system,scope,'mitigation_validation']+cnt+ms+[subp,subp*ms[-1] if scope=='affected_subgroup' else None,'representation beyond supplied sample is not established'])
ds('mitigation_records','Matched reference and supplied mitigation harm',[cat('system'),cat('scope'),ident('cohort_id')]+countcols+metriccols+[col('deployment_subgroup_probability'),col('population_weighted_harm_contribution'),col('representation_limitation','string','text')],harmrows,'Authored proportional confusion counts produce the glossary subgroup conditional harms 0.80 and 0.60. Class probabilities are fixed at the supplied negative/positive values. Validation subgroup prevalence is computed from subgroup and overall counts and is not assumed to equal 0.25. Check both subgroup and overall evidence before accepting the supplied mitigation.')
# Make validation subgroup representation distinct from the supplied deployment share.
mitigation_asset=assets['mitigation_records']
mitigation_asset['columns'] += [col('deployment_negative_probability'),col('deployment_positive_probability'),col('cost_FP'),col('cost_FN'),col('validation_subgroup_prevalence')]
for row in mitigation_asset['rows']:
 system=row[0]
 subgroup=next(r for r in mitigation_asset['rows'] if r[0]==system and r[1]=='affected_subgroup')
 overall=next(r for r in mitigation_asset['rows'] if r[0]==system and r[1]=='overall')
 row += [p0,p1,c_fp,c_fn,sum(subgroup[3:7])/sum(overall[3:7])]
eligible_slices=[r for r in slicerows if r[3]]
aggregate=[]
for system,index in [('reference',7),('model',5)]:
 count=len(eligible_slices);errors=sum(r[index] for r in eligible_slices)
 aggregate.append([system,'slices_60',count,errors,errors/count])
ds('aggregate_slice_evidence','Aggregate evidence from the matched slice cohort',[cat('system'),ident('cohort_id'),col('eligible_count','integer'),col('error_count','integer'),col('error_probability')],aggregate,'Computed same-cohort overall reference/model errors. Overall improvement does not remove the supported sample segment limitation or establish universal suitability.')

# Paired randomness trials: five matched pairs, three strict lower-cost wins.
m=re.search(r'five completed matched baseline/candidate pairs and the candidate wins three',ex('training_randomness'));assert m
pairn=wordnum['five'];wins=wordnum['three']
seedlist=list(range(pairn));pairrows=[]
for seed in seedlist:
 baseline=basecost+seed/100;candidate=baseline+(-1 if seed<wins else 1)/100
 pairrows.append([seed,baseline,candidate])
paired=ds('paired_trials','Five completed matched seed trials',[col('seed','integer','identifier','Declared integer random-state setting, not a measurement.'),col('baseline_result'),col('candidate_result')],pairrows,'Authored matched expected-cost results with three candidate wins among five completed trials. Trial records contain only the glossary-required seed and baseline/candidate fields. Lower cost wins, ties are not wins, ddof=0; incomplete pairs are not counted.')
edge(paired,'incomplete_pair',[setcell({'seed':seedlist[-1]},'candidate_result',None)],'Keep the completed-pair denominator explicit; do not count an unfinished trial.')
# Regularization and bounded search: preserve all taught train/validation costs.
tcost_a,vcost_a,tcost_b,vcost_b=grab('validation_regularization',r'training cost (\d+\.\d+) and validation cost (\d+\.\d+).*?training cost (\d+\.\d+) and validation cost (\d+\.\d+)')
regrows=[]
for cfg,C,tr,va in [('weak_penalty',10.0,tcost_a,vcost_a),('stronger_penalty',1.0,tcost_b,vcost_b)]:
 tc=counts_for(tr);vc=counts_for(va)
 regrows.append([cfg,'LogisticRegression','C',C,'inverse regularization strength','orders_100']+tc+[metrics(*tc)[-1]]+vc+metrics(*vc)+[True])
regs=ds('regularization_records','Fixed-criterion regularization evidence',[ident('configuration_id'),cat('estimator'),cat('parameter_name'),col('parameter_value'),col('strength_direction','string','text'),ident('cohort_id')]+[col('training_'+c['name'],'integer') for c in countcols]+[col('training_expected_error_cost')]+countcols+metriccols+[boolean('operating_requirements_met')],regrows,'Authored LogisticRegression C settings with exact taught train/validation costs derived from authored counts. Smaller C strengthens the penalty. Pick by validation cost and fixed eligibility, not by training cost; no protected-test data.')
emptycnt=[0,nneg,0,0]
emptyms=metrics(*emptycnt)
emptyops=[setcell({'configuration_id':'stronger_penalty'},c['name'],v) for c,v in zip(countcols,emptycnt)]
emptyops += [setcell({'configuration_id':'stronger_penalty'},c['name'],v) for c,v in zip(metriccols,emptyms)]
edge(regs,'regularization_empty_positive',emptyops,'Undefined required FNR is not evidence of eligibility, even with nonempty negative evidence.')

ds('regularization_directions','Estimator-specific penalty directions',[cat('estimator'),cat('parameter'),col('direction','string','text')],[['Ridge','alpha','larger alpha increases penalty'],['LogisticRegression','C','larger C decreases regularization strength']],'Verbatim estimator-specific distinction in the glossary; not interchangeable parameter meanings.')
searchrows=[]
for i,(C,cost) in enumerate([(10.0,vcost_a),(1.0,vcost_b),(0.1,ccost)]):
 cnt=counts_for(cost); searchrows.append([f'config_{i+1}',i,json.dumps({'C':C,'random_state':train_seed},sort_keys=True),'orders_100']+cnt+[True])
search=ds('search_trials','Three declared configuration dictionaries',[ident('configuration_id'),col('declared_order','integer'),col('configuration_json','string','text'),ident('cohort_id')]+countcols+[boolean('operating_requirements_met')],searchrows,'Authored authorized trial-interface responses. The third response exists for hidden checks but is not a completed trial when budget=2. The learner records only executed configurations.')
edge(search,'search_empty_positive',[setcell({'configuration_id':'config_2'},c['name'],v) for c,v in zip(countcols,emptycnt)],'The trial interface returns no actual positives; the learner must leave FNR and expected cost undefined.')

keyword_budget=wordnum[re.search(r'keyword budget of (\w+)',ex('bounded_hyperparameter_search'))[1]]
(default_setting,override_setting)=grab('experiment_metric_logging',r'trial setting of (\d+).*?override of (\d+)')
ds('execution_contract','Fixed execution and reporting contracts',[col('estimator_random_state','integer','identifier'),col('default_trial_setting','integer'),col('override_trial_setting','integer'),col('default_search_budget','integer'),col('override_search_budget','integer'),cat('metric_direction'),cat('tie_policy'),cat('split_protocol'),col('ddof','integer')],[[train_seed,default_setting,override_setting,len(searchrows),keyword_budget,'lower expected cost is better','ties are not paired wins; selection uses declared order','use same split per seed for both models; set split and estimator random_state to the seed',0]],'Seed, override and spread contracts from the glossary; default search budget is an authored three-trial fixture contract because no default number is specified.')
# Risk documentation: policy fields are authored only within the glossary's stated scope; no literal secret.
riskrows=[['permitted_identities','A','A and B','B is outside the existing permitted identity scope'],['credential_handling','do not reproduce secret values','sample_image.credential_field [REDACTED]','record the location and exposure-handling limitation only'],['permitted_use','evaluate supplied order-task validation evidence','task-specific validation fixture','no universal suitability claim'],['task_limits','supplied order task and validation cohort only','no evidence outside the supplied cohort','retain the task/cohort boundary'],['foreseeable_misuse','aggregate improvement used as universal segment suitability','zone A and B have different observed sample errors','retain segment limitations; no population disparity established'],['segment_evidence','retain supported sample limitations','zone B has higher observed eligible error proportion than zone A','sample-only evidence; representation beyond supplied sample is unresolved']]
ds('risk_policy_evidence','Existing policy and redacted risk evidence',[ident('field'),col('existing_policy','string','text'),col('supplied_observation','string','text'),col('recording_constraint','string','text')],riskrows,'Authored bounded existing-policy fields and supplied observations grounded in glossary examples. Identity A is permitted; B is not. Only a redacted credential location is provided, never a secret value. Segment figures are backed by ds.slice_observations.')
ds('access_grants','Permitted identity versus observed grants',[cat('identity'),boolean('policy_permitted'),boolean('observed_grant')],[['A',True,True],['B',False,True]],'Exact identity vocabulary from the glossary. Record the mismatch without expanding the permitted set.')
# CSV mounts for every dataset. Hashes, byte counts and headers are computed, never typed.
(B/'assets').mkdir(exist_ok=True)
for name,a in assets.items():
 p=B/'assets'/f'{name}.csv'
 with p.open('w',newline='') as f:
  w=csv.writer(f);w.writerow([c['name'] for c in a['columns']]);w.writerows(a['rows'])
 raw=p.read_bytes();a['data_file']={'uri':str(p.relative_to(B)),'format':'csv','sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}
# Workspace assets contain supplied fixture loaders/contracts only, with learner functions left unwritten.
mounts={
 'reference_baseline':['reference_train','orders_validation','regression_targets','acceptance_contract'],
 'sklearn_baseline_workflow':['orders_train','orders_validation','acceptance_contract','execution_contract'],
 'decision_threshold_selection':['validation_scores','thresholds','acceptance_contract'],
 'prediction_error_analysis':['slice_observations','acceptance_contract'],
 'slice_evaluation':['slice_observations','acceptance_contract'],
 'experiment_metric_logging':['execution_contract','metric_summary'],
 'training_randomness':['orders_train','orders_validation','paired_trials','execution_contract'],
 'validation_regularization':['orders_train','orders_validation','regularization_records','regularization_directions','acceptance_contract'],
 'bounded_hyperparameter_search':['search_trials','execution_contract','acceptance_contract'],
 'foundation_model_baseline_evaluation':['validation_scores','foundation_outputs','acceptance_contract']}
for key,names in mounts.items():
 b=by[key]
 fixture={name:[dict(zip([c['name'] for c in assets[name]['columns']],r)) for r in assets[name]['rows']] for name in names}
 contract={'concept_id':b['context']['concept_id'],'datasets':[assets[name]['asset_id'] for name in names],'csv_mounts':{name:f'{name}.csv' for name in names},'objective':b['practice_anchor']['objective'],'starter_state_intent':b['practice_anchor']['live_code']['starter_state_intent'],'allowed_syntax':b['practice_anchor']['live_code']['allowed_syntax'],'observable_success':b['practice_anchor']['live_code']['observable_success']}
 readme='Supplied fictional order-task fixture\n\n'+contract['starter_state_intent']+'\n\n'+contract['objective']+'\n\nThe learner writes all required imports and the analysis/function body in learner.py. fixtures.json is supplied input, not a solution. Dataset CSVs are mounted with the names in contract.json; missing CSV cells denote missing values. No protected-test data or accessor is supplied. The registry variants provide empty-class, alignment and incomplete-pair hidden-check fixtures.\n'
 extra={}
 if key in ('sklearn_baseline_workflow','reference_baseline','validation_regularization','training_randomness'):
  readme+='\nConstruct arrays from the declared feature columns, not observation identifiers. orders_train supplies feature_1 and feature_2 as X_train and y_train as the label; orders_validation supplies feature_1 and feature_2 as X_validation and y_validation. reference_train is a separate ten-row reference-training fixture. Previously fitted preprocessing, if required, is an injected pipeline; do not fit it on validation.\n'
 if key=='training_randomness':
  readme+='\nDeclared seed list: '+json.dumps(seedlist)+'. For each seed, the authorized comparison interface must use the same split for baseline and candidate and control both estimator and split random_state. paired_trials supplies completed result evidence only (seed, baseline_result, candidate_result), not a substitute for executing the seed-control protocol. An incomplete pair is excluded.\n'
 if key=='decision_threshold_selection':
  readme+='\nInfrastructure interfaces: eligibility(record) evaluates defined required rates and expected_error_cost <= expected_cost_bound. retain_threshold(record) stores one unchanged threshold, probability-score representation, validation record and eligibility verdict. Tie policy is first declared candidate; no eligible record means no selection. Implement these decisions in the learner function; no selection code is supplied.\n'
 if key=='bounded_hyperparameter_search':
  readme+='\nAuthorized trial interface run_trial(configuration): returns the corresponding pre-authored validation confusion counts and operating_requirements_met from search_trials. It records the actual passed dictionary and must not be called beyond the resolved budget. Fixtures list three dictionary inputs in declared order, not three completed executions. Default budget is the fixture contract; keyword budget override is in execution_contract.\n'
  extra['supplied_interface.py']='''# Infrastructure-only adapter; no scoring, budget resolution or selection logic.
import json
from pathlib import Path
TRIALS = json.loads(Path(__file__).with_name("fixtures.json").read_text())["search_trials"]
CALLS = []
def run_trial(configuration):
    for row in TRIALS:
        if json.loads(row["configuration_json"]) == configuration:
            CALLS.append(dict(configuration))
            return {k: row[k] for k in ("TP", "FP", "FN", "TN", "cohort_id", "operating_requirements_met")}
    raise ValueError("configuration outside declared search space")
'''
 if key=='experiment_metric_logging':
  readme+='\nThe player must inject an existing authorized MLflow tracking setup and the intended order-training repository directory. Resolve the local diagnostic.txt path at execution time; capture the real repository HEAD with the allowed Git subprocess command. No repository revision, run_id, artifact_uri or infrastructure authorization is fabricated in this fixture. The supplied validation metric is expected_error_cost from metric_summary. The tracking infrastructure is a runtime dependency, not provided by a glossary or registry. Reject deliberately mismatched retrieved revision evidence.\n'
  extra['diagnostic.txt']=json.dumps({'cohort_id':assets['metric_summary']['rows'][0][0],'confusion_counts':dict(zip(['TP','FP','FN','TN'],[TP,FP,FN,TN])),'metric_name':'expected_error_cost','metric_value':metrics(TP,FP,FN,TN)[-1]},indent=2)+'\n'
 if key=='foundation_model_baseline_evaluation':
  readme+='\nJoin supplied foundation_outputs to validation_scores by the fixed observation identifiers, verifying exact matched cohort and unique coverage before scoring. Only the output_kind foundation-model is accepted. Reference outputs come from the same training-majority baseline. No fitting, settings choice, prompt construction or application integration.\n'
 files={'README.md':readme,'contract.json':json.dumps(contract,indent=2)+'\n','fixtures.json':json.dumps(fixture,indent=2)+'\n','learner.py':'# Write the required imports and learner-defined function here.\n'}
 files.update(extra)
 R['assets'].append({'asset_id':'ws.'+key,'asset_kind':'code_workspace','scenario_id':sid,'title':b['context']['concept_name']+' — supplied fixture','runtime':'python','files':[{'path':p,'content':v} for p,v in files.items()]})
# Own mistakes-to-avoid audit: structural, semantic, example arithmetic, edge predicates, and full scope.
assert len({a['asset_id'] for a in R['assets']})==len(R['assets'])
for a in assets.values():
 assert all(len(r)==len(a['columns']) for r in a['rows']),a['asset_id']
 assert len({c['name'] for c in a['columns']})==len(a['columns'])
 for c in a['columns']:
  if c['type'] in ('number','integer') and c['semantic_role']=='categorical':assert c.get('numeric_looking_label') is True
  if c['semantic_role']=='numerical':assert c['type'] in ('number','integer')
  if c['semantic_role']=='identifier':assert c['type'] in ('string','integer')
assert summary[0][1:4]==[acount,aerr,aerr/acount]
assert summary[1][1:4]==[bcount,berr,berr/bcount]
assert summary[2][1:4]==[longcount,longerr,longerr/longcount]
assert sum(r[2]<r[1] for r in pairrows)==wins
assert all(math.isclose(r[1+len(countcols)+len(metriccols)-1],v,abs_tol=1e-10) for r,v in zip(trs,[tcost1,tcost2]))
assert math.isclose(sum(r[-1] for r in acceptrows),p0*fpr*c_fp+p1*fnr*c_fn)
assert all(k in mounts for k in by if by[k]['practice_anchor']['type']=='live_code')
assert not any(re.search(r'plot|chart|palette|axis limit|bin count',json.dumps(b['visual_anchor']),re.I) for b in bs),'Plot dependency needs explicit rendering'
(B/'scenario_asset_registry.json').write_text(json.dumps(R,indent=2,ensure_ascii=False)+'\n')
audit={'concept_count':len(bs),'scenario_count':len(R['scenarios']),'dataset_count':len(assets),'workspace_count':len(mounts),'image_count':0,'variant_count':sum(len(a['variants']) for a in assets.values()),'row_count':sum(len(a['rows']) for a in assets.values()),'asset_ids':[a['asset_id'] for a in R['assets']],'checks':['row widths and column names','unambiguous semantic roles and digit-label traps','glossary numbers extracted and arithmetic computed','eligible slice and long-distance denominators','paired completed-trial denominator','all live-code anchors have supplied workspace fixtures','no glossary plot dependency','no invented numeric latency bound, secret, git revision, run ID or artifact URI','edge ops and planted duplicate occurrence validated by stage gate'],'uncertainties':['Glossary provides no numeric operating limits: Boolean authored operating predicate records remain separate; formula operating limit is null.','Authorized MLflow and actual repository directory are external runtime dependencies; no live tracking setup or Git repository is fabricated.','Default search budget and numerical feature values are explicitly authored fixture choices where glossary gives no values.']}
(B/'working/registry_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
print(json.dumps({k:v for k,v in audit.items() if k not in ('asset_ids','checks','uncertainties')},indent=2))
