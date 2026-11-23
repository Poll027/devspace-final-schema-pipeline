import json
from pathlib import Path
B=Path('batches/final_batch_mle.region.validation_and_selection');p=B/'interactions.json';d=json.loads(p.read_text());s=json.loads((B/'screens.json').read_text());sm={t['tile_id']:t for t in s['tiles']}
for t in d['tiles']:
 for e in t['interactions']:
  ix=e['interaction'];sid=e['step_id']
  if any('#practice' in a for a in ix['anchors']):
   cid=ix['anchors'][0].split('#')[0];rem=[v['step_id'] for v in sm[t['tile_id']]['remediation_steps'] if cid in v['concept_ids']]
   if rem:ix['feedback']['remediation_step_id']=rem[-1]
  if sid=='mle.tile.019_020.s10':
   ix['grading']['tests']=ix['grading']['tests'][:7]+[{'test_id':'t_contract_operating','kind':'range_equals','spec':{'range':'H8:H9'},'message_on_fail':'Retain the supplied bound and separate operating-limit conclusion.'}]
  if sid=='mle.tile.029_032.s23':
   ws=ix['public']['workspace'];helper=next(f['content'] for f in ws['files'] if f['path']=='trial_adapter.py')
   helper=helper.replace('import json\n\n','').replace('def run_trial(configuration, trials):','def run_trial(configuration):')
   ws['files']=[f for f in ws['files'] if f['path']!='trial_adapter.py'];ws['files'][0]['content']=ws['files'][0]['content'].replace('from trial_adapter import CALLS, run_trial\n',helper)
   ix['grading']['solution_files']=[f for f in ix['grading']['solution_files'] if f['path']!='trial_adapter.py'];f=ix['grading']['solution_files'][0];f['content']=f['content'].replace('from trial_adapter import CALLS, run_trial\n',helper).replace('trial = run_trial(configuration, trials)','trial = run_trial(configuration)')
p.write_text(json.dumps(d,indent=2)+'\n')
