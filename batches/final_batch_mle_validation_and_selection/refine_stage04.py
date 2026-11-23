import json,re,sys
from pathlib import Path
B=Path('batches/final_batch_mle.region.validation_and_selection');p=B/'interactions.json';d=json.loads(p.read_text());r=json.loads((B/'scenario_asset_registry.json').read_text());g=json.loads((B/'inputs/path_glossary_bundle.json').read_text());aa={a['asset_id']:a for a in r['assets']}
def rec(a):
 x=aa[a];return [dict(zip([c['name'] for c in x['columns']],v)) for v in x['rows']]
def col(a,k):
 i=[x['name'] for x in aa[a]['columns']].index(k)+1;v=''
 while i:i,m=divmod(i-1,26);v=chr(65+m)+v
 return v
for t in d['tiles']:
 for e in t['interactions']:
  ix=e['interaction'];sid=e['step_id']
  if ix['type']=='code_exercise':
   if ix['public']['runtime']['kind']=='python':
    tests=ix['grading']['tests']
    # Test exceptional behavior together with matched evidence to retain input-sensitive verification.
    if sid in ['mle.tile.026_028.s11','mle.tile.034_034.s05']:
     tests[1]['spec']['expr']='('+tests[0]['spec']['expr']+', '+tests[1]['spec']['expr']+')'
    if sid=='mle.tile.021_023.s05':
     for f in ix['grading']['solution_files']:f['content']=f['content'].replace(", 'training_shape': X_train.shape, 'training_label_shape': y_train.shape",'')
     ix['public']['prompt']=ix['public']['prompt'].replace(', training_shape, training_label_shape','')
    if sid=='mle.tile.029_032.s23':
     # Existing adapter helper is supplied infrastructure in a readonly module, not learner-defined source.
     starter=ix['public']['workspace']['files'][0]['content'];solution=ix['grading']['solution_files'][0]['content']
     start=starter.index('# Supplied authorized trial adapter');end=starter.index('\n# Add the required imports',start);helper=starter[start:end]
     newhelper='import json\n\n'+helper.replace("def run_trial(configuration):","def run_trial(configuration, trials):")
     ix['public']['workspace']['files'].append({'path':'trial_adapter.py','role':'readonly','language':'python','content':newhelper})
     shared='from trial_adapter import CALLS, run_trial\n'
     ix['public']['workspace']['files'][0]['content']=starter[:start]+shared+starter[end:]
     ix['grading']['solution_files'][0]['content']=solution.replace(helper,shared).replace('trial = run_trial(configuration)','trial = run_trial(configuration, trials)')
     # Copy supplied module into solution execution explicitly.
     ix['grading']['solution_files'].append({'path':'trial_adapter.py','content':newhelper})
   else:
    f=ix['grading']['solution_files'][0];f['content']=f['content'].replace('IF(ISBLANK(contract!K2),"no numeric operating limit supplied; predictive acceptance is not overall eligibility",contract!K2)','IF(contract!J2,contract!K2,"no numeric operating limit supplied; predictive acceptance is not overall eligibility")')
    ix['public']['constraints']['allowed_syntax']+=['numbers']
  elif ix['type']=='external_proof':
   evidence=rec('ds.risk_policy_evidence');access=rec('ds.access_grants');slices=rec('ds.slice_summary');agg=rec('ds.aggregate_slice_evidence')
   parts=['Produce one text risk-and-use record. Preserve existing policy; do not copy secrets or create new permissions.']
   for v in evidence:parts.append(v['field']+': permitted='+v['existing_policy']+'; observed='+v['supplied_observation']+'.')
   parts.append('Access grants: '+', '.join(str(v['identity'])+' granted='+str(v['observed_grant']) for v in access)+'.')
   parts.append('Slice evidence: '+', '.join(v['slice']+' '+str(v['error_count'])+'/'+str(v['eligible_count'])+'='+str(v['error_probability']) for v in slices[:2])+'.')
   parts.append('Aggregate and segment errors: '+', '.join(v['system']+' '+str(v['error_count'])+'/'+str(v['eligible_count'])+'='+str(v['error_probability']) for v in agg)+'. Retain all scope, task, misuse and redacted-exposure limitations; sample evidence is not universal suitability.')
   ix['public']['instruction']='\n'.join(parts);assert len(ix['public']['instruction'])<=1500
p.write_text(json.dumps(d,indent=2)+'\n')
