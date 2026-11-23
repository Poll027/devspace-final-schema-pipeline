# Execute in generator namespace. Simplify learner edits rather than widening glossary constraints.
# Unmapped prose descriptors in this glossary are not accepted as Python syntax by the pinned gate.
simplified=[]
def simplify(n,inputs,learner,finish,prompt):
 old=specs[n]
 # Separate supplied infrastructure from the learner section. Infrastructure executes AFTER edits where needed.
 scaffold=old['starter'].split('\n# Learner section\n')[0]+'\n'+supplied(inputs)
 names=[line.split(' = ')[0] for line in learner.strip().splitlines() if ' = ' in line]
 starter=''.join(k+' = None\n' for k in names)+'# Complete the documented calculations/assignments.\n'+supplied(finish)
 solution=learner+'\n'+supplied(finish)
 register(n,old['names'],scaffold,starter,solution,prompt,old['exprs'],old['packages']);simplified.append(n)

n='distribution_monitoring'
inputs="ref_values=reference['numeric_values']; ref_values=ref_values[(ref_values>=0)&(ref_values<=10)]\ncur_values=production['numeric_values']; cur_values=cur_values[(cur_values>=0)&(cur_values<=10)]\nfixed_edges=policy['fixed_edges']\n"
learner='''ref_mean = np.mean(ref_values)
cur_mean = np.mean(cur_values)
ref_std = np.std(ref_values,ddof=0)
cur_std = np.std(cur_values,ddof=0)
ref_counts = np.histogram(ref_values,bins=fixed_edges)
cur_counts = np.histogram(cur_values,bins=fixed_edges)
'''
finish='''def complete_summary(data,values,mean,std,hist):
    if mean is None or std is None or hist is None: return None
    return {'eligible_total':len(values),'category_total':len(data['category']),'class_total':len(data['predicted_class']),'bin_proportions':hist[0]/len(values),'mean':mean,'std':std,'categories':{c:np.sum(data['category']==c)/len(data['category']) for c in policy['declared_categories']},'classes':{c:np.sum(data['predicted_class']==c)/len(data['predicted_class']) for c in policy['declared_classes']}}
record={'reference_id':policy['reference_id'],'window':policy['production_window'],'fixed_edges':fixed_edges,'category_definitions':policy['declared_categories'],'class_definitions':policy['declared_classes'],'ddof':policy['ddof'],'reference':complete_summary(reference,ref_values,ref_mean,ref_std,ref_counts),'production':complete_summary(production,cur_values,cur_mean,cur_std,cur_counts)}
emit(record)
'''
simplify(n,inputs,learner,finish,'Complete ref_mean/cur_mean with np.mean on ref_values/cur_values, ref_std/cur_std with np.std(...,ddof=0), and ref_counts/cur_counts with np.histogram(...,bins=fixed_edges). The supplied client infrastructure selects the inclusive eligible numeric range, uses fixed bin edges, normalizes each window by its own total, retains declared categories/classes (including zeros), window/reference definitions and emits one monitoring record. Do not change the infrastructure. This bounded edit focuses on the NumPy calculations; the supplied function and emission client assemble the single deliverable.')

n='data_drift_detection'
inputs="ref_values=ref_values[(ref_values>=0)&(ref_values<=10)]\ncur_values=cur_values[(cur_values>=0)&(cur_values<=10)]\ncategory_deltas=0.5*np.abs(ref_cats/ref_cat_n-cur_cats/cur_cat_n)\nnumeric_deltas=0.5*np.abs(ref_bins/ref_n-cur_bins/cur_n)\n"
learner='''ref_mean = np.mean(ref_values)
cur_mean = np.mean(cur_values)
ref_std = np.std(ref_values,ddof=0)
cur_std = np.std(cur_values,ddof=0)
category_distance = np.sum(category_deltas)
numeric_distance = np.sum(numeric_deltas)
'''
finish='''result={'reference_id':policy['reference_id'],'current_id':policy['current_id'],'window':policy['comparison_window'],'edges':policy['fixed_edges'],'categories':policy['declared_categories'],'eligibility':policy['eligible_numeric_range'],'criterion':policy['criterion'],'quality_claim':policy['quality_claim'],'reference_mean':ref_mean,'current_mean':cur_mean,'reference_std':ref_std,'current_std':cur_std,'reference_categories':ref_cats/ref_cat_n,'current_categories':cur_cats/cur_cat_n,'reference_bins':ref_bins/ref_n,'current_bins':cur_bins/cur_n,'category_distance':category_distance,'numeric_distance':numeric_distance,'category_drift':category_distance>0.20 if category_distance is not None else None,'numeric_drift':numeric_distance>0.20 if numeric_distance is not None else None,'reference_total':ref_n,'current_total':cur_n}
'''
simplify(n,inputs,learner,finish,'Complete ref_mean/cur_mean and ref_std/cur_std on the supplied eligible ref_values/cur_values using np.mean and np.std(...,ddof=0). Complete category_distance=np.sum(category_deltas) and numeric_distance=np.sum(numeric_deltas). Infrastructure has aligned bins/categories and normalized each window by its own total; each delta is 0.5*abs(reference proportion-current proportion). It returns result with the policy comparison definition, proportions, summaries and feature verdicts for distance>0.20, never a claim of increased prediction error. Keep the supplied comparison code unchanged.')

n='delayed_label_quality'
original=specs[n]['solution'].split('\n# Learner section\n')[1]
# Preserve the join and rejection logic as supplied infrastructure; request the two glossary-mapped calculations.
inputs=original.replace('result = quality(prediction_rows,label_rows)','joined = quality(prediction_rows,label_rows)')+"\nmature_losses=[r['loss'] for r in joined.get('matched',{}).values()]\n"
learner='loss_mean = np.mean(mature_losses)\nloss_std = np.std(mature_losses,ddof=0)\n'
finish="result = joined\nif result.get('status')=='mature_cohort_only':\n    result['loss_mean']=loss_mean; result['loss_std']=loss_std\n"
simplify(n,inputs,learner,finish,'The supplied prediction-ID joining interface preserves cohort rows/timestamps, rejects duplicate IDs, excludes unmatched or out-of-boundary labels and exposes mature_losses. Complete loss_mean with np.mean(mature_losses) and loss_std with np.std(mature_losses,ddof=0). The returned result incorporates these values into the mature-cohort report with eligible/matched counts, coverage, error count/proportion and exclusion evidence. Do not change the boundary or cohort policy; these results do not establish quality for all traffic.')

n='actionable_ml_alerts'
inputs="normal_valid=np.mean(windows['normal'])<=np.mean(baseline)+4\nboundary_valid=np.mean(windows['boundary'])<=np.mean(baseline)+4\nbreach_valid=np.mean(windows['breached'])>np.mean(baseline)+4\n"
learner='''baseline_mean = np.mean(baseline)
baseline_std = np.std(baseline,ddof=0)
assert normal_valid
assert boundary_valid
assert breach_valid
'''
finish="""resolved={'indicator':policy['indicator'],'baseline_window':policy['baseline_window'],'threshold':float(baseline_mean+4) if baseline_mean is not None else None,'ddof':policy['ddof'],'owner':policy['owner'],'response':policy['response']}
with open('alert.yaml','w') as h: yaml.safe_dump(resolved,h)
with open('alert.yaml') as h: resolved=yaml.safe_load(h)
result=replay(resolved) if resolved['threshold'] is not None else None
"""
simplify(n,inputs,learner,finish,'Complete baseline_mean=np.mean(baseline) and baseline_std=np.std(baseline,ddof=0). Add assert normal_valid, assert boundary_valid and assert breach_valid for the supplied valid/equality/crossing predicate fixtures. The existing configuration interface sets mean(baseline)+4, preserves policy owner/action, safely writes/reloads alert.yaml and replays result; only a strict crossing emits the owner/action. Keep supplied serialization and replay plumbing unchanged.')

n='production_regression_diagnosis'
original=specs[n]['solution'].split('\n# Learner section\n')[1]
inputs="matched_counts=release_evidence['matched_eligible_labels']\nerror_counts=release_evidence['labeled_errors']\nnonempty=matched_counts>0\n"
# Comparison operators is explicitly mapped but division descriptor is not, so use np count? no np count mapped available and zero denominators guarded.
# The learner chooses the supplied guarded rate vector and tested policy response, not a new response policy.
inputs+="guarded_rates=[float(e/n) if n>0 else None for e,n in zip(error_counts,matched_counts)]\npolicy_supported_response='approved_rollback'\nunsupported_response='gated_retraining'\n"
learner='selected_rates = guarded_rates\nselected_response = policy_supported_response\n'
finish=original.replace("rate = errors/n","rate = selected_rates[len(result)]").replace("response = 'approved_rollback'","response = selected_response")
simplify(n,inputs,learner,finish,'Complete selected_rates by assigning the supplied guarded_rates vector, which keeps separate matched eligible mature-label denominators and None for empty groups. Complete selected_response by assigning policy_supported_response, not unsupported_response. Read the evidence: the active cfg.bad differs from the approved configuration and the distinguishing replay supports the policy-approved rollback. The supplied recording interface preserves each release/cohort timeline, identities, hypothesis evidence, counts and rates, requires readiness/bounded prediction for rollback and leaves quality unresolved for empty groups. No recovery is executed. This bounded configuration edit selects the evidence-supported report inputs.')

n='ml_resource_utilization'
original=specs[n]['solution'].split('\n# Learner section\n')[1]
inputs=original.split('result = ')[0].replace(" & (resource_telemetry['timestamp']", " & (resource_telemetry['running_process'] == policy['process_id']) & (resource_telemetry['timestamp']",1)
learner='''cpu_mean = np.mean(cpu)
cpu_std = np.std(cpu,ddof=0)
memory_mean = np.mean(memory)
memory_std = np.std(memory,ddof=0)
'''
finish='result = '+original.split('result = ')[1].replace('np.mean(cpu)','cpu_mean').replace('np.std(cpu,ddof=0)','cpu_std').replace('np.mean(memory)','memory_mean').replace('np.std(memory,ddof=0)','memory_std')
simplify(n,inputs,learner,finish,'The supplied selection interface retains only the policy instance/process, matching running process, RUNNING lifecycle state and declared half-open interval, using one mask for CPU and memory. Complete cpu_mean/memory_mean with np.mean(cpu)/np.mean(memory) and cpu_std/memory_std with np.std(...,ddof=0). Infrastructure retains identity, interval, counts and units in result. Do not mix stopped or unrelated observations or perform lifecycle actions.')

n='ml_workload_cost_attribution'
original=specs[n]['solution'].split('\n# Learner section\n')[1]
inputs=original.split('summary = {}')[0]+"training_values=np.array([allocated['training']['w1'],allocated['training']['w2']])\ninference_values=np.array([allocated['inference']['w1'],allocated['inference']['w2']])\n"
learner='''training_mean = np.mean(training_values)
training_std = np.std(training_values,ddof=0)
inference_mean = np.mean(inference_values)
inference_std = np.std(inference_values,ddof=0)
'''
finish='summary = {}'+original.split('summary = {}')[1]
finish=finish.replace("'mean':np.mean(values),'std':np.std(values,ddof=0)","'mean':training_mean if workload=='training' else inference_mean,'std':training_std if workload=='training' else inference_std")
simplify(n,inputs,learner,finish,'The supplied authorized workload interface records the two bounded lifecycle windows and stopped states. The attribution interface applies resource_mapping, retains persistent-disk charges, shares charges by policy and records unallocated/unmatched amounts. Complete training_mean/inference_mean from training_values/inference_values with np.mean and training_std/inference_std with np.std(...,ddof=0). Each array is one workload\'s per-window charges. The result retains lifecycle, workload windows, unusual flags, explicit unallocated amounts and reconciled totals. Keep the supplied mapping/interval policy unchanged.')

n='retrained_candidate_validation'
original=specs[n]['solution'].split('\n# Learner section\n')[1]
inputs=original.split('assert evaluate')[0]+"checked_records=test_all(evaluate)\nvalid_pass=evaluate(fixtures['valid']['incumbent'],fixtures['valid']['candidate'],fixtures['valid']['candidate']['registry_artifact_id'])['verdict']\nboundary_pass=evaluate(fixtures['boundary']['incumbent'],fixtures['boundary']['candidate'],fixtures['boundary']['candidate']['registry_artifact_id'])['verdict']\nidentity_rejected=not evaluate(fixtures['valid']['incumbent'],fixtures['valid']['candidate'],'model.unrelated')['verdict']\nfailure_checks_pass=all(not r['record']['verdict'] for r in checked_records if r['fixture'] not in ['valid','boundary'])\n"
learner='''assert valid_pass
assert boundary_pass
assert identity_rejected
assert failure_checks_pass
result = checked_records
'''
simplify(n,inputs,learner,'','Verify the supplied incumbent-relative evaluation implementation using executable assertions: assert valid_pass, assert boundary_pass, assert identity_rejected and assert failure_checks_pass. Assign result=checked_records. The supplied function uses FPR/FNR conditioning counts, shared probabilities/costs, rejects undefined groups, enforces quality AND slice AND compatibility AND exact identity/cohort binding, and records every fixture. No protected test observations are available. This bounded edit focuses on assert predicates; do not replace conjunctive gates or identity binding. A false predicate must raise AssertionError in ordinary execution.')

n='ml_workload_cost_guardrail'
keys=['workload_scope','budget_amount','period','threshold_ratio','notification_topic','response_pipeline','INSTANCE','ZONE','authorized_identity','secret_version_reference']
inputs='approved_config = '+repr({k:policy(n)[k] for k in keys})+"\napproved_config['secretEnv']=['BUDGET_CLIENT']\napproved_config['event_binding']={'topic':policy['notification_topic'],'pipeline':policy['response_pipeline']}\nunapproved_config = dict(approved_config,INSTANCE='other-lab')\n"
learner='config = approved_config\n'
finish="""with open('guardrail.yaml','w') as h: yaml.safe_dump(config,h)
with open('guardrail.yaml') as h: resolved=yaml.safe_load(h)
result=apply_and_replay(resolved) if config is not None else None
"""
simplify(n,inputs,learner,finish,'Complete config by assigning approved_config rather than unapproved_config. Read the two supplied mappings: only approved_config retains policy workload/amount/period/threshold, existing topic/event binding, authorized fixed instance and runtime secret version reference with scoped secretEnv. The existing platform safely dumps/reloads YAML, validates resolved fields before application and exercises below/boundary/breach fixtures, recording notification separately from stop execution, fixed-target before/after descriptions and credential-safe logs in result. The returned limitation states that notification lag permits spending above budget. Keep supplied parsing/replay unchanged.')

n='retraining_run_idempotency'
old=specs[n];helper=old['starter'].split('\n# Learner section\n')[0]
# Supply branch interfaces, but learner must wire accepted/duplicate/busy handling and gate assertions.
inputs='''def accepted_same_token(claim,executor): return executor.launch(claim['job_id'])
def duplicate_same_token(claim,executor): return executor.attach(claim['job_id'])
def no_launch(claim,executor): return None
'''
learner='on_accepted = accepted_same_token\non_duplicate = duplicate_same_token\non_busy = no_launch\n'
original=old['solution'].split('\n# Learner section\n')[1]
finish=original.replace("return {'status':'defer','job_id':claim['job_id']}","on_busy(claim,executor)\n        return {'status':'defer','job_id':claim['job_id']}").replace("executor.launch(claim['job_id'])","on_accepted(claim,executor)").replace("executor.attach(claim['job_id'])","on_duplicate(claim,executor)")
# Starter must not run a missing callable; it instead returns no report, not successful fixtures.
finish="if on_accepted is None or on_duplicate is None or on_busy is None:\n    result=None\nelse:\n"+'\n'.join('    '+line for line in finish.splitlines())+'\n'
specs[n]['starter'] = specs[n]['starter'].replace('\n# Learner section\n', '\nevent_run_key = '+repr(policy(n)['event']['run_key'])+'\n# Learner section\n')
inputs = "policy['event']['run_key']=event_run_key\n" + inputs
simplify(n,inputs,learner,finish,'Wire the supplied durable admission function by assigning on_accepted=accepted_same_token, on_duplicate=duplicate_same_token and on_busy=no_launch. Read their contracts: accepted launches with the atomic coordinator\'s persisted job token, duplicate attaches/reconciles that same token, and busy launches nothing. The supplied shared filesystem coordinator atomically reserves key/slot/job identity; the function handles terminal release while retaining completed keys. Existing assertions and fresh-worker fixtures inspect one logical job, busy deferral, stable restart/unknown-response identity and non-relaunch after completion. The existing build config uses explicit fatal entry/function_test/execute dependencies, safe YAML roundtrip and accepted/rejected trigger evidence. Keep the infrastructure and assertions unchanged. This bounded edit wires the correct branch interfaces rather than adding new coordination state.')

# Any assertions in the learner section are gated against the verbatim glossary list.
for n,s in specs.items():
 cons=G['mle.'+n]['practice_anchor']['live_code']
 violations,unmapped,_=pysyntax.judge(s['solution'],cons['allowed_syntax'],cons['blocked_syntax'],s['starter'])
 if violations: raise RuntimeError(n+': '+str(violations))
exec((B/'stage04_content.py').read_text())

out={'schema_version':P['schema_version'],'kind':'interactions_part','path_id':P['path_id'],'batch_id':P['batch_id'],'tiles':[]}
for t in P['tiles']:
 screen=next(x for x in S['tiles'] if x['tile_id']==t['tile_id']);seen=set(); tile={'tile_id':t['tile_id'],'interactions':[]}; planned=[s for s in t['steps'] if s['type'] in ['check','hands_on']]
 for index,s in enumerate(planned):
  cid=s['concept_ids'][0];n=cid.split('.')[1];g=G[cid]
  measures=[]
  for anchor in s['anchors']:
   if '#assessment:' in anchor:
    cap=anchor.split('#assessment:')[1]; a=next(a for a in g['assessment_anchors'] if a['capability']==cap)
    measures.append({'concept_id':cid,'capability':cap,'fact_ids':a['fact_ids']})
  ix={'type':s['planned_interaction_type'],'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if index==0 else ('stretch' if index>=len(planned)-2 else 'core'),'grading_mode':'client','standalone':True,'anchors':[a for a in s['anchors'] if a.endswith('#practice')],'measures':measures}
  hint='Review the comparison definition and the evidence required for each judgement.'
  feedback={'correct':{'message':'The response follows the declared evidence, calculation or authorization rule.'},'incorrect':{'message':'Recheck the declared observations, denominator, boundary and required gates; do not substitute evidence for a different claim.'},'hints':[hint]}
  if cid not in seen:
   rem=next((r for r in screen.get('remediation_steps',[]) if cid in r['concept_ids']),None)
   if rem: feedback['remediation_step_id']=rem['step_id']
   seen.add(cid)
  if s['type']=='check':
   prompt,choices,hint=checks[n];feedback['hints']=[hint]
   # Correct IDs derive from authored option object marked by its evidence-justified role.
   opts=[{'option_id':'o'+str(i+1),'text':c[0]} for i,c in enumerate(choices)]
   correct=opts[0]
   ix['public']={'prompt':prompt,'options':opts,'selection':'single','shuffle':True}
   ix['grading']={'correct_option_ids':[correct['option_id']],'option_feedback':{o['option_id']:{'message':c[1]} for o,c in zip(opts,choices)}}
  elif ix['type']=='code_exercise':
   sp=specs[n];ix['standalone']=False
   ix['public']={'prompt':sp['prompt'],'runtime':{'kind':'python','version':sandbox.RUNTIMES['python']['version'],'packages':sp['packages']},'workspace':{'entry':'learner.py','files':[{'path':'learner.py','role':'editable','language':'python','content':sp['starter']}],'asset_mounts':[{'asset_id':'ds.'+name,'mount_path':name+'.csv'} for name in sp['names']]},'constraints':{k:copy.deepcopy(g['practice_anchor']['live_code'][k]) for k in ['allowed_syntax','blocked_syntax']}}
   tests=[{'test_id':'t'+str(i+1),'kind':'value_equals','spec':{'expr':expr},'visible':True,'message_on_fail':'The returned record or calculation does not match the declared fixture contract.'} for i,expr in enumerate(sp['exprs'])]
   ix['grading']={'solution_files':[{'path':'learner.py','content':sp['solution']}],'tests':tests}
  elif n=='drift_degradation_distinction':
   asset=assets['ds.evidence_scenarios'];cols=[c['name'] for c in asset['columns']];print('EVIDENCE COLS',cols)
   buckets=[{'bucket_id':'input','label':'Input distribution shift; other changes unsupported'},{'bucket_id':'conditional','label':'Conditional target change; other changes unsupported'},{'bucket_id':'quality','label':'Observed matched-label quality loss; other changes unsupported'}]
   roles={'P(X)':'input','P(Y|X)':'conditional','matched_label_errors':'quality'}
   evidence_col=next(c for c in cols if c in ['evidence_type','evidence_category','evidence_basis','supported_evidence'])
   idcol=cols[0]; rolecol=evidence_col;items=[];assignments={};item_feedback={}
   for i,row in enumerate(asset['rows']):
    d=dict(zip(cols,row));item='item'+str(i+1);role=d[rolecol]
    text='\n'.join(c+': '+str(d[c]) for c in cols if c!=rolecol)
    items.append({'item_id':item,'text':text,'source':{'asset_id':asset['asset_id'],'row':{'where':{idcol:d[idcol]},'occurrence':0},'column':rolecol}});assignments[item]=roles[role];item_feedback[item]={'message':d[cols[-1]]}
   ix['public']={'prompt':'Read each order-prediction scenario. Classify the evidence-supported change and keep the other conclusions unsupported. A quality-loss claim requires matched predictions and labels against the declared quality reference.','buckets':buckets,'items':items}
   ix['grading']={'assignments':assignments,'role_map':roles,'item_feedback':item_feedback}
  else:
   rows=judge_sets[n];ix['public']={'prompt':'Read each supplied excerpt and decide whether it meets or violates the stated operations criterion. Classify the whole excerpt; one unsafe or unsupported step makes it a violation. All targets and identities are fictional nonproduction order-service fixtures.','buckets':[{'bucket_id':'meets','label':'Meets the declared criterion'},{'bucket_id':'violates','label':'Violates the declared criterion'}],'items':[{'item_id':'item'+str(i+1),'text':title+'\n```text\n'+text+'\n```'} for i,(title,text,role,why) in enumerate(rows)]}
   ix['grading']={'assignments':{'item'+str(i+1):row[2] for i,row in enumerate(rows)},'item_feedback':{'item'+str(i+1):{'message':row[3]} for i,row in enumerate(rows)}}
  ix['feedback']=feedback;tile['interactions'].append({'step_id':s['step_id'],'interaction':ix})
 out['tiles'].append(tile)

# Compute all expected values by executing solutions in pinned Pyodide, never by transcription.
scripts=[];code_ix=[]
for tile in out['tiles']:
 for row in tile['interactions']:
  ix=row['interaction']
  if ix['type']!='code_exercise':continue
  code_ix.append(ix);ws=ix['public']['workspace'];mounts=[]
  for m in ws['asset_mounts']:
   a=assets[m['asset_id']];mounts.append({'path':m['mount_path'],'columns':[c['name'] for c in a['columns']],'rows':a['rows']})
  scripts.append({'id':ix['interaction_id'],'entry':ws['entry'],'files':ix['grading']['solution_files'],'mounts':mounts,'probes':[{'id':t['test_id'],'kind':'expr','expr':t['spec']['expr']} for t in ix['grading']['tests']]})
job={'packages':['numpy','pandas','pyyaml'],'scripts':scripts}
results=sandbox.node_run(job,sandbox.RUNTIMES['python']['runner'])['results']
for ix in code_ix:
 r=results[ix['interaction_id']]
 if not r['ok']:raise RuntimeError(ix['interaction_id']+' '+r.get('error','unknown execution error'))
 for t in ix['grading']['tests']:
  p=r['probes'][t['test_id']]
  if not p['ok']:raise RuntimeError(ix['interaction_id']+' '+str(p))
  t['spec']['expected']=p['value']
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
(B/'stage04_expected_execution.json').write_text(json.dumps(results,indent=2)+'\n')
print('WROTE',len(code_ix),'code exercises',sum(len(t['interactions']) for t in out['tiles']),'total')
(B/'stage04_simplifications.json').write_text(json.dumps(simplified,indent=2)+'\n')
