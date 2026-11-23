import json,sys,subprocess,os,hashlib,re
from pathlib import Path
root=Path(__file__).resolve().parent;p=root.parent.parent/'screens.json';d=json.loads(p.read_text())
patterns={
 'With declared PyYAML, import yaml. Write mapping/list configuration with yaml.safe_dump(config, file_handle), reload with yaml.safe_load(file_handle), and inspect required resolved fields before runtime submission. Safe loading accepts standard YAML tags, not arbitrary Python object constructors.': 'Reuse import yaml, yaml.safe_dump and yaml.safe_load to round-trip the configuration and inspect required resolved fields. Safe loading still excludes arbitrary Python object constructors.',
 'Keep required failures fatal: omit allowFailure and failing codes from allowExitCodes; a rejected Python gate must exit unsuccessfully.': 'Retain the fatal-gate settings: no allowFailure or allowed failing exit codes; rejection exits unsuccessfully.',
 'Give steps IDs and set waitFor to required preceding IDs: successful completion, not textual order, controls downstream execution.': 'Reuse explicit step IDs and waitFor predecessors; depend on successful completion, not textual order.'
}
seen=set()
for t in d['tiles']:
 for s in t['steps']:
  for b in s.get('blocks',[]):
   if b['type']=='prose':
    for text,reminder in patterns.items():
     if text in b['text']:
      if text in seen:b['text']=b['text'].replace(text,reminder)
      seen.add(text)
   if s['step_id']=='mle.tile.076_079.s01' and b['type']=='code_walkthrough':
    code=b['code'].replace("        del step['output']", "        del step['output']\n        if step['id'] == 'training' and step['status'] == 'SUCCESS':\n            step['computed_evidence'] = {'produced_identity':load('downstream_invocation.json')['artifact_id']}")
    q=root/'ws.pipeline_artifact_dependencies'/'visual_walkthrough.py';q.write_text(code)
    proc=subprocess.run([sys.executable,str(q)],cwd=q.parent,env=dict(os.environ,PYTHONPATH='/usr/lib/python3/dist-packages:/tmp/mle_eval_runtime'),capture_output=True,text=True)
    assert proc.returncode==0,proc.stderr
    b['code']=code;b['output']['text']=proc.stdout;b['annotations'][0]['end_line']=len(code.splitlines())
    b['execution_provenance']['code_sha256']=hashlib.sha256(code.encode()).hexdigest();b['execution_provenance']['output_sha256']=hashlib.sha256(proc.stdout.encode()).hexdigest()
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
# Self-audit: required lineage, unchanged framing and ordered plan, prose budgets and only named modifications.
original=json.loads((root/'screens_before.json').read_text());plans=json.loads((root.parent.parent/'tile_plans.json').read_text())
changed=[]
for ot,t,pt in zip(original['tiles'],d['tiles'],plans['tiles']):
 assert ot['remediation_steps']==t['remediation_steps']
 for old,s,plan in zip(ot['steps'],t['steps'],pt['steps']):
  assert s['step_id']==plan['step_id'] and s['type']==plan['type']
  assert {k:v for k,v in old.items() if k!='blocks'}=={k:v for k,v in s.items() if k!='blocks'}
  assert s['lineage']['fact_ids']==plan['fact_ids'] and s['lineage']['teaching_block_ids']==plan['teaching_block_ids']
  count=sum(len(re.findall(r'\S+',b['text'])) for b in s.get('blocks',[]) if b['type']=='prose')
  assert count<=plan['word_budget'],(s['step_id'],count,plan['word_budget'])
  for b in s.get('blocks',[]):
   if b['type']!='up_next':assert 'lineage' in b
   if b['type']=='prose':assert len(b['text'].split())<=90
   for f in b.get('lineage',{}).get('fact_ids',[]):assert '#' in f
  if old!=s:changed.append(s['step_id'])
print('Changed steps:',changed)
