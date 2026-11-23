import ast,json,sys,pathlib
B=pathlib.Path('batches/final_batch_mle.region.production_operations');sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts');from checkers import sandbox,pysyntax
D=json.load(open(B/'interactions.json'));R=json.load(open(B/'scenario_asset_registry.json'));assets={a['asset_id']:a for a in R['assets']}
# Convert syntax-conflict dependency-order puzzles into bounded input/function binding tasks.
# Infrastructure remains supplied; the editable starter never includes learner bindings.
for tile in D['tiles']:
 for e in tile['interactions']:
  ix=e['interaction'];c=e['interaction']['measures'][0]['concept_id']
  if ix['type']!='code_exercise' or c in ['mle.ml_incident_runbook','mle.retraining_run_idempotency']:continue
  sol=ix['grading']['solution_files'][0]['content'];tree=ast.parse(sol)
  infra=tree.body[0:2] if False else next(n.value.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_fixture_support' for t in n.targets))
  old=sol[sol.index('exec(_fixture_support)')+len('exec(_fixture_support)'):].lstrip()
  # The calculation/report mechanism is supplied, while the learner must map inputs
  # and select mean and population-spread operators.
  mount_names=[m['mount_path'].removesuffix('.csv') for m in ix['public']['workspace']['asset_mounts']]
  data_code=''
  bindings=[]
  params=[]
  for name in mount_names:
   data_code+=name+'_rows = load('+repr(name)+')\n'
   bindings.append((name+'_input',name+'_rows'));params.append(name+'_input')
  mean_std=('np.mean(' in old or 'np.std(' in old)
  if mean_std:bindings += [('mean_function','np.mean'),('spread_function','np.std')];params+=['mean_function','spread_function']
  # The routing dictionary and report assembly are scaffolding, not learner syntax.
  route='{'+','.join(repr(n)+':'+n+'_input' for n in mount_names)+'}'
  replacement='def calculate_contract('+','.join(params)+'):\n    supplied_rows = '+route+'\n    def load(name):\n        return supplied_rows[name]\n'
  if mean_std:old=old.replace('np.mean(','mean_function(').replace('np.std(','spread_function(')
  # Any np functions in the original policy serializer stay in supplied code.
  replacement+='\n'.join('    '+l for l in old.splitlines())+'\n    return report\n'
  policy_node=next((n for n in ast.parse(old).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='policy' for t in n.targets)),None)
  policy_source=ast.get_source_segment(old,policy_node) if policy_node else ''
  infrastructure=infra+'\n'+policy_source+'\n'+replacement
  pre='# Supplied fixture parsing, contract/report mechanism and authorized simulator.\n_fixture_support = '+repr(infrastructure)+'\nexec(_fixture_support)\n'+data_code
  lines='\n'.join(n+' = '+v for n,v in bindings)+'\n'
  starter=pre+'# Bind each contract input to its intended row collection.\n'+'\n'.join(n+' = None' for n,v in bindings)+'\n'
  if mean_std:starter+='# Select the NumPy mean and standard-deviation functions; the supplied contract fixes ddof=0.\n'
  finish='report = calculate_contract('+','.join(params)+')\n'
  starter+=finish;solution=pre+lines+finish
  ix['public']['workspace']['files'][0]['content']=starter;ix['grading']['solution_files'][0]['content']=solution
  # Explicitly frame simplified allowable task rather than asking for an implementation the starter already supplies.
  ix['public']['prompt']=ix['public']['prompt'].split('\nRuntime note:')[0]
  ix['public']['prompt']+='\nThe supplied mechanism handles parsing and report assembly. Your bounded edit is to bind each named input to the intended mounted row collection'+(' and select np.mean and np.std as its mean/spread functions' if mean_std else '')+'. Replace only the None bindings. Do not copy an output or change the fixed contract. Run and inspect the full report described above.'
  violations=pysyntax.judge(solution,ix['public']['constraints']['allowed_syntax'],ix['public']['constraints']['blocked_syntax'],starter)[0]
  if violations:raise RuntimeError((c,violations))
# Specific planned checks must test their actual capability.
def check_change(step,prompt,good,bad,why):
 ix=next(e['interaction'] for t in D['tiles'] for e in t['interactions'] if e['step_id']==step);ix['public']['prompt']=prompt;ix['public']['options']=[{'option_id':'correct','text':good},{'option_id':'misconception','text':bad}];ix['grading']['option_feedback']={k:{'message':why} for k in ['correct','misconception']}
check_change('mle.tile.091_094.s08','You report training unit cost for a declared billing window. Which denominator is aligned with the attributed training expenditure?','Completed training work measured for the corresponding workload and work/billing window.','Completed inference work from a different reporting window.','Unit cost divides attributed expenditure by corresponding completed work, retaining the billing and work-measurement windows.')
check_change('mle.tile.091_094.s13','Which process verifies the resolved workload budget-response YAML before applying it?','Safely dump and reload the configuration, then inspect scope, amount, period, threshold, event binding and fixed approved target.','Apply the serialized text without reloading or inspecting its resolved fields.','The supplied contract requires safe serialization/loading and resolved-field inspection before application.')
# Actual cleanup inspect-and-judge excerpts: derive names/identities/policy from registry.
c='mle.serving_resource_cleanup';ix=next(e['interaction'] for t in D['tiles'] for e in t['interactions'] if e['step_id']=='mle.tile.091_094.s19')
pol=json.loads(next(f['content'] for f in assets['ws.serving_resource_cleanup']['files'] if f['path']=='policy.json'))
a=assets['ds.cleanup_inventory'];names=[co['name'] for co in a['columns']];rr=[dict(zip(names,r)) for r in a['rows']];active=next(r for r in rr if r['approved_inventory']=='active');retired=next(r for r in rr if r['approved_inventory']=='retired');unverified=next(r for r in rr if r['approved_inventory']=='not_authorized')
contract=json.dumps(pol,ensure_ascii=False)
entries=[
 ('Runtime inspection: '+json.dumps(retired)+'\nIdentity='+pol['authorized_identity']+'. Approved inventory and actual owner/release, running/exit state, logs and compute identity agree on exclusive retirement. Captured output contains no credential values. Plan: docker container stop '+retired['NAME']+'; confirm stopped; docker container rm '+retired['NAME']+'; gcloud compute instances delete '+retired['INSTANCE']+' --zone='+retired['ZONE']+' under '+pol['disk_policy']+'. Preserve active '+active['NAME']+' and required artifacts. Then verify readiness, bounded prediction and approved retired-resource absence; record ownership, authorization, inspections, actions, retained artifacts and non-disclosure review.','safe','Runtime verification and explicit scope permit only retired-resource actions; the active release/artifacts and required postchecks/audit are preserved.'),
 ('Runtime inspection: '+json.dumps(unverified)+'\nProposed cleanup: remove this container and delete its instance because it is the oldest release. No approved inventory or permitted owner match is available.','reject','Age does not establish authorization or exclusive retirement; this owner/identity is outside the approved inventory.'),
 ('Runtime inspection: '+json.dumps(retired)+'\nProposed sequence: docker container rm '+retired['NAME']+' while State.Running is true; stop is skipped. No other changes are proposed.','reject','A verified retired running container is stopped before removal; exclusive retirement does not remove the stop-before-rm requirement.'),
 ('Runtime inspection: retired container='+retired['NAME']+', active container='+active['NAME']+'. Both reference '+active['image_ref']+' and '+active['preprocessing_artifact']+'. Proposed action after retired-container removal: delete '+active['image_ref']+' and '+active['preprocessing_artifact']+' as unused retired artifacts.','reject','The active release still references the shared artifacts. Retired-container removal is not authorization to delete them.'),
 ('Post-action audit excerpt: authorized identity='+pol['authorized_identity']+'; inspected actual labels and lifecycle; only '+retired['NAME']+' stopped then removed and '+retired['INSTANCE']+' deleted preserving disks. Active '+active['NAME']+' remains present. Required artifacts remain present. Active readiness and bounded prediction pass; before/after describe confirms approved retired-instance absence; inventory confirms retired-container absence. Captured commands/logs contain references only; non-disclosure review passes. Audit includes owner '+pol['authorized_owner']+', active/retired release identities, permitted scope, inspection evidence, actions and retained artifacts.','safe','This evidence includes active health, approved absence, artifact/disk retention and the complete credential-safe audit.'),
 ('Post-action record: only approved retired targets acted on; no credential values appear and required artifacts are retained. Active instance reports RUNNING, but model readiness and bounded prediction were not checked. The audit declares cleanup verified solely from RUNNING.','reject','Instance RUNNING alone does not prove active-serving readiness and bounded prediction; required health checks remain missing.')]
ix['public']={'prompt':'Inspect these independent cleanup plans/audit excerpts against the supplied lab contract. Classify each as compliant or unsafe/incomplete. Judge actual runtime ownership/release and lifecycle evidence, narrow destructive scope, stop-before-remove, preservation of the active release/artifacts, post-action health/absence and credential-safe audit—not age alone.\nContract: '+contract,'buckets':[{'bucket_id':'safe','label':'Compliant cleanup plan or verification record'},{'bucket_id':'reject','label':'Unsafe or missing required evidence'}],'items':[{'item_id':'i'+str(i),'text':text} for i,(text,key,why) in enumerate(entries)]}
ix['grading']={'assignments':{'i'+str(i):key for i,(text,key,why) in enumerate(entries)},'item_feedback':{'i'+str(i):{'message':why} for i,(text,key,why) in enumerate(entries)}}
# Code tests derive every new expected from the actual pinned solution, preserving one report per task.
for t in D['tiles']:
 for e in t['interactions']:
  ix=e['interaction']
  if ix['type']!='code_exercise':continue
  tables,_=sandbox._tables(R,ix['public']['workspace']['asset_mounts'],{},[])
  result=sandbox.node_run(sandbox._py_job('python',ix['public']['runtime']['packages'],[sandbox._py_script('solution','main.py',ix['grading']['solution_files'][0]['content'],sandbox._py_mounts(tables),[{'id':'report','kind':'expr','expr':'report'}])]),sandbox.RUNTIMES['python']['runner'])['results']['solution']
  if not result['ok']:raise RuntimeError((e['step_id'],result))
  ix['grading']['tests'][0]['spec']['expected']=result['probes']['report']['value']
  print('computed',e['step_id'])
json.dump(D,open(B/'interactions.json','w'),indent=2,ensure_ascii=False)
