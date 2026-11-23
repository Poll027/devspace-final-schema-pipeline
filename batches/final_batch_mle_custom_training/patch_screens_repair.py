import json
from pathlib import Path
b=Path(__file__).parent
p=b/'screens.json'
d=json.loads(p.read_text())
g=json.loads((b/'inputs/path_glossary_bundle.json').read_text())
bundles={x['context']['concept_id']:x for x in g['bundles']}
targets={
 'mle.tile.044_045.s07':('Failing reference: glossary example','Same-fixture correction: verification rule'),
 'mle.tile.046_048.s12':('Memory reference: glossary example','Same-workload correction: verification rule'),
 'mle.tile.049_050.s01':('Profiling attribution: glossary example','Matched timing: verification rule'),
 'mle.tile.051_051.s01':('Frozen reference: glossary example','Task adaptation: verification rule'),
}
# Only the four named visuals; no new fixture measurements can be authored here.
for tile in d['tiles']:
 for step in tile['steps']:
  if step['step_id'] not in targets:continue
  visual=next(x for x in step['blocks'] if x['type']=='side_by_side')
  bundle=bundles[step['concept_ids'][0]]
  example=next(x for x in bundle['teaching_blocks'] if x['purpose']=='example')
  sentences=example['content'].split('\n\n')[0].split('. ')
  # Use source example sentences, not invented failing/corrected measurements.
  split=max(1,len(sentences)//2)
  for side,title,labels in zip(('left','right'),targets[step['step_id']],(sentences[:split],sentences[split:])):
   diagram=visual[side]
   diagram['title']=title
   diagram['nodes']=[{'id':f'node{i}','label':s.rstrip('.')} for i,s in enumerate(labels)]
   diagram['edges']=[{'from':f'node{i}','to':f'node{i+1}','directed':True} for i in range(len(labels)-1)]
   diagram['alt_text']=title+': '+'; '.join(n['label'] for n in diagram['nodes'])
   diagram['lineage']['teaching_block_ids']=[bundle['context']['concept_id']+'#'+example['id']]
  visual['takeaway']='Glossary example only; the supplied registry has no pinned failing/corrected evidence records for this comparison.'
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('Patched',len(targets),'visuals')
print('Tiles',len(d['tiles']),'steps',sum(len(t['steps']) for t in d['tiles']),'remediation steps',sum(len(t.get('remediation_steps',[])) for t in d['tiles']))
