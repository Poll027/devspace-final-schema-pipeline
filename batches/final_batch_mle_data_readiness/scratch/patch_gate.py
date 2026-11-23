import json,copy
from pathlib import Path
b=Path('batches/final_batch_mle.region.data_readiness');p=b/'interactions.json';d=json.loads(p.read_text());R=json.loads((b/'scenario_asset_registry.json').read_text());a={x['asset_id']:x for x in R['assets']};S=json.loads((b/'screens.json').read_text())
for t in d['tiles']:
 rems=next(x for x in S['tiles'] if x['tile_id']==t['tile_id'])['remediation_steps']
 for item in t['interactions']:
  ix=item['interaction'];cid=ix['measures'][0]['concept_id'];matching=[r for r in rems if cid in r['concept_ids']]
  if matching:ix['feedback']['remediation_step_id']=matching[-1 if ix['anchors'] else 0]['step_id']
  if ix['type']=='code_exercise':
   short=ix['anchors'][0].split('#')[0].split('.',1)[1];f=json.loads(next(z['content'] for z in a['ws.'+short]['files'] if z['path']=='fixtures.json'))
   if short=='numpy_dtype_selection':
    for code in [ix['public']['workspace']['files'][0],ix['grading']['solution_files'][0]]:code['content']=code['content'].replace("tolerance = FIXTURES['tolerance']","tolerance = "+repr(f['tolerance']))
   if short=='chunked_ingestion':
    ix['grading']['tests']=[{'test_id':'budget'+str(i),'kind':'function_call','spec':{'function':'inspect_chunks','args':[f['path'],f['declared_types'],budget,f['feature_count'],f['element_width']],'expected':None},'visible':i==0,'message_on_fail':'The maximum actual chunk element allocation does not match this budget.'} for i,budget in enumerate([f['array_budget'],f['array_budget']+f['feature_count']*f['element_width']])]
   if short=='categorical_encoding':
    for code in [ix['public']['workspace']['files'][0],ix['grading']['solution_files'][0]]:
     code['content']=code['content'].replace("'missing':[[np.nan]]","'missing':np.array([[np.nan]],dtype=object)")
    code=ix['grading']['solution_files'][0]['content']
    code=code.replace("before = encoder.categories_[0].copy()","before = encoder.categories_[0].tolist()").replace('assert before.tolist() == encoder.categories_[0].tolist()','assert before == encoder.categories_[0].tolist()')
    code=code.replace("error_encoder.fit(X_train)","error_encoder.fit(X_train)\n    assert np.array_equal(error_encoder.transform(cases['known']), known)")
    ix['grading']['solution_files'][0]['content']=code
  elif ix['type']=='classify' and ix['anchors']==['mle.preprocessing_pipeline#practice']:
   for i in ix['public']['items']:i['text']=i['text'].replace('except KeyError:', 'except ValueError:')
p.write_text(json.dumps(d,indent=2)+'\n')
