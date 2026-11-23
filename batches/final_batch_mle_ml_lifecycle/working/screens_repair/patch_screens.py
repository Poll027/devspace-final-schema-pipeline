import json, copy, hashlib, sys, os, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
B=ROOT.parent.parent
load=lambda p: json.loads(Path(p).read_text())
d=load(B/'screens.json'); original=copy.deepcopy(d); evidence=load(ROOT/'evidence.json')
steps={s['step_id']:s for t in d['tiles'] for s in t['steps']}
def visual(sid): return next(b for b in steps[sid]['blocks'] if b['type'] in ('diagram','side_by_side','before_after','code_walkthrough'))
def fmt(x): return json.dumps(x,ensure_ascii=False,sort_keys=True)
def diagram(title,records,lineage):
 nodes=[]
 for i,(label,fields) in enumerate(records):
  nodes.append({'id':'n'+str(i),'label':label,'fields':[k+': '+fmt(v) for k,v in fields.items()]})
 return {'type':'diagram','diagram_kind':'sequence','title':title,'nodes':nodes,'edges':[{'from':nodes[i]['id'],'to':nodes[i+1]['id'],'directed':True} for i in range(len(nodes)-1)],'alt_text':title+'. '+ '; '.join(n['label']+': '+'; '.join(n['fields']) for n in nodes),'lineage':copy.deepcopy(lineage)}
def state_records(run):
 records=[('Resolved local-run inputs',run['resolved_inputs'])]
 for s in run['steps']:
  records.append((s['id'],{k:v for k,v in s.items() if k!='id'}))
 return records
# 1. Computed quality run-state diagram (missing_feature registry variant uses missing_required_feature workspace fixture).
sid='mle.tile.073_075.s01';old=visual(sid);ln=old['lineage']; runs=evidence['dataset_quality_gate']['computed_local_results']
records=[]
for label,r in zip(['valid — accepted fixture','missing_feature — missing_required_feature workspace fixture'],runs):
 records.append((label,{'event':r['event']}));records+=state_records(r['run'])
new=diagram('Computed local-simulator runs: accepted and missing-feature fixtures',records,ln)
old.clear();old.update(new)
steps[sid]['blocks'].append({'type':'prose','role':'walkthrough','text':'These are executed local-fixture results, not hosted Cloud Build results.','lineage':copy.deepcopy(ln)})
# 2 and 3. Side-by-side computed results.
for sid,name,labels,takeaway in [
 ('mle.tile.073_075.s06','model_behavior_tests',['Accepted local run','Regressed local run'],'Compare executed local-fixture results: a fatal behavior regression prevents dependent execution. These are not hosted Cloud Build results.'),
 ('mle.tile.073_075.s11','model_release_quality_gate',['Accepted candidate','Latency-failing candidate'],'A passing expected-cost check cannot compensate for a failed latency check; inspect the executed local gate and promotion statuses.')]:
 b=visual(sid)
 for side,label,r in zip(['left','right'],labels,evidence[name]['computed_local_results']):
  b[side]=diagram(label,state_records(r['run']),b['lineage']);b[side+'_label']=label
 b['takeaway']=takeaway
# Executable, workspace-specific walkthroughs: display supplied files and the explicit local demonstration wiring.
def walkthrough_code(name,fixture):
 implementation=evidence[name]['entry_point_implementation']
 mode="\n    if step['args'][1] == 'demonstration_entry.py':\n        step['args'].append(step['id'])\n" if name=='staged_ml_promotion' else "\n    if step['args'][1] == 'demonstration_entry.py':\n        step['args'] = ['python', 'demonstration_entry.py', '${_CASE}', step['id']]\n        if step['id'] == 'model_validation':\n            step['args'].append('${_CONSUMED}')\n"
 extra="\n    config['substitutions']['_CONSUMED'] = cases[event['case_id']]['model_validation']['consumed']\n    config['substitutions']['_PRODUCED'] = cases[event['case_id']]['training']['produced']\n    config['steps'][1]['args'][-1] = '${_PRODUCED}'\n" if name=='pipeline_artifact_dependencies' else ''
 checks="" if name=='pipeline_artifact_dependencies' else "\n    run['secret_reference_and_scope'] = {'references':config['availableSecrets']['secretManager'], 'step_scopes':{s['id']:s.get('secretEnv',[]) for s in config['steps']}}\n    # The bounded adapter supplies no credentials; inspect emitted field names, never credential values.\n    run['non_disclosure_check'] = {'adapter_supplies_credentials':False, 'credential_fields_in_emitted_records':any(k.lower() in ('promotion_token','credential','secret_value') for k in recursive_keys(run))}\n"
 recursive='' if name=='pipeline_artifact_dependencies' else "\ndef recursive_keys(x):\n    if isinstance(x, dict):\n        for k, v in x.items():\n            yield k\n            yield from recursive_keys(v)\n    elif isinstance(x, list):\n        for v in x:\n            yield from recursive_keys(v)\n"
 return "import json, copy, yaml\nfrom pathlib import Path\nfrom runtime_sim import run_build\nload = lambda p: json.loads(Path(p).read_text())\ncases = load("+repr('fixtures/'+fixture)+")\nsupplied = yaml.safe_load(Path('cloudbuild.yaml').read_text())\nprint(json.dumps({'supplied_fixtures':cases, 'parsed_supplied_cloudbuild_yaml':supplied}, indent=2))\n# Author a demonstration entry point in an isolated copy; the supplied learner.py remains unwritten.\nPath('demonstration_entry.py').write_text("+repr(implementation)+")\nconfig = copy.deepcopy(supplied)\nfor i, step in enumerate(config['steps']):\n    step['waitFor'] = ['-'] if i == 0 else [config['steps'][i-1]['id']]\n    if 'learner.py' in step['args']:\n        step['args'][1] = 'demonstration_entry.py'"+mode+recursive+"\nfor event in load('triggers.json')['pubsub']['fixtures'][:2]:"+extra+"\n    with open('demonstration.yaml', 'w') as f:\n        yaml.safe_dump(config, f)\n    parsed = yaml.safe_load(Path('demonstration.yaml').read_text())\n    run = run_build('demonstration.yaml', 'pubsub', event)\n    for step in run['steps']:\n        if step['output'].strip():\n            step['computed_evidence'] = json.loads(step['output'])\n        del step['output']"+checks+"\n    print(json.dumps({'event':event, 'parsed_local_demonstration_config':parsed, 'computed_local_run':run}, indent=2))\n"
def executed_block(b,code,root,annotation):
 path=root/'visual_walkthrough.py';path.write_text(code)
 env=dict(os.environ,PYTHONPATH='/usr/lib/python3/dist-packages:/tmp/mle_eval_runtime')
 p=subprocess.run([sys.executable,str(path)],cwd=root,text=True,capture_output=True,env=env)
 assert p.returncode==0,p.stderr
 b['code']=code;b['annotations']=[{'start_line':1,'end_line':len(code.splitlines()),'text':annotation}]
 b['output']={'kind':'text','text':p.stdout}
 b['execution_provenance']={'runtime':'python','runtime_version':sys.version.split()[0],'code_sha256':hashlib.sha256(code.encode()).hexdigest(),'output_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()}
for sid,name,fixture,annotation in [
 ('mle.tile.076_079.s01','pipeline_artifact_dependencies','dependency_cases.json','Check predecessor completion and artifact agreement separately: training output A must match the resolved model-validation input. A completed predecessor does not establish that identity match.'),
 ('mle.tile.076_079.s06','staged_ml_promotion','promotion_cases.json','Keep the artifact unchanged through staging quality and separate authorization. Rejected authorization must leave production unexecuted. Display secret references and non-disclosure results, never credential values.')]:
 executed_block(visual(sid),walkthrough_code(name,fixture),ROOT/('ws.'+name),annotation)
# Recovery comparison includes all three checkpoints and the fatal required-gate contrast.
b=visual('mle.tile.076_079.s12');before=[];after=[]
for r in evidence['pipeline_failure_recovery']['computed_local_results']:
 label=r['event']['case_id']; first=r['run']['steps'][0]['evidence']
 before.append((label+' — before recovery: A retained after injected failure',{'outputs':first['before'],'upload_count':len(first['uploads'])-len([k for k,v in first['before'].items() if not v['exists']])}))
 before+=state_records(r['before_recovery'])
 after.append((label+' — after recovery',{'outputs':first['after'],'upload_count':first['upload_count']}));after+=state_records(r['run'])
 second=r['second_invocation']; after.append((label+' — after second invocation',{'outputs':second['steps'][0]['evidence']['after'],'upload_count':second['steps'][0]['evidence']['upload_count']}));after+=state_records(second)
b['before']=diagram('Computed state before recovery',before,b['lineage']);b['after']=diagram('Computed recovery and repeat states',after,b['lineage'])
b['change_summary']='Executed local-fixture recovery states: retain verified completed uploads, create only missing outputs, and rerun required validation. A second invocation creates no extra generations; a failed required gate still blocks downstream execution.'
# Audit script executes both Git inspections without creating or repairing a repository.
b=visual('mle.tile.076_079.s18');code=(ROOT/'audit_evidence.py').read_text()
# Replace file-only reporting with printed, computed records and verdicts for this visible walkthrough.
code=code.replace("Path('audit_evidence.json').write_text(json.dumps(evidence,indent=2))","print(json.dumps(evidence,indent=2))")
executed_block(b,code,ROOT/'ws.deployed_model_lineage_audit','Verify every recorded identity edge, the exact artifact generation and content, and the existing local commit. Report missing or mismatched links explicitly; similar names cannot supply provenance.')
# Advisory: retain each concept-specific trigger/dependency/configuration requirement, abbreviate repeated setup only.
full_cloud='In each existing Cloud Build steps item, name selects the execution image; args or script supplies the command. Wire the assigned function/test entry point there.'
full_assert='Use assert predicates for valid, boundary and failure fixtures. A false predicate raises AssertionError in ordinary non-optimized execution.'
seen_cloud=False;seen_assert=False;seen_yaml=False
for t in d['tiles']:
 for s in t['steps']:
  for block in s.get('blocks',[]):
   if block['type']!='prose': continue
   text=block['text']
   if full_cloud in text:
    if seen_cloud: text=text.replace(full_cloud,'As before, wire this assigned entry point through the Cloud Build image and command fields.')
    seen_cloud=True
   if full_assert in text:
    if seen_assert: text=text.replace(full_assert,'Assert the valid, boundary and failure predicates; false assertions still raise AssertionError.')
    seen_assert=True
   yaml_full='With declared PyYAML, import yaml; yaml.safe_dump writes the mapping/list config and yaml.safe_load reloads it. Inspect required resolved fields before submission. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.'
   if yaml_full in text:
    if seen_yaml: text=text.replace(yaml_full,'Reuse the PyYAML safe-dump/safe-load round trip and inspect required resolved fields; safe loading still excludes arbitrary Python object constructors.')
    seen_yaml=True
   block['text']=text
# Ensure the repair leaves all step framing, order and lineage untouched.
for oldt,newt in zip(original['tiles'],d['tiles']):
 assert oldt['remediation_steps']==newt['remediation_steps']
 for olds,news in zip(oldt['steps'],newt['steps']):
  assert {k:v for k,v in olds.items() if k!='blocks'}=={k:v for k,v in news.items() if k!='blocks'}
(B/'screens.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('tiles',len(d['tiles']),'steps',sum(len(t['steps']) for t in d['tiles']),'remediation_steps',sum(len(t['remediation_steps']) for t in d['tiles']))
