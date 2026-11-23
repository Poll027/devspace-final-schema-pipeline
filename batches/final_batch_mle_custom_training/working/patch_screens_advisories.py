import copy, json
from pathlib import Path
p=Path('batches/final_batch_mle.region.custom_training/screens.json')
d=json.loads(p.read_text());before=copy.deepcopy(d)
def step(tid,sid):
 t=next(t for t in d['tiles'] if t['tile_id']==tid)
 return next(s for s in t['steps']+t['remediation_steps'] if s['step_id']==tid+'.'+sid)
def insert(tid,sid,text,source_index,facts):
 s=step(tid,sid);lineage=copy.deepcopy(s['blocks'][source_index]['lineage']);lineage['fact_ids']=[s['concept_ids'][0]+'#'+f for f in facts]
 idx=next(i for i,b in enumerate(s['blocks']) if b['type']=='code_walkthrough')
 s['blocks'].insert(idx,{'type':'prose','text':text,'role':'example','lineage':lineage})
insert('mle.tile.035_037','s01','These fixtures already supply corresponding observation order. Equal batch lengths alone do not prove that each feature row belongs to its target; verify that correspondence using the supplied observation identifiers or pairing reference.',1,['f2','f4'])
insert('mle.tile.035_037','s06','Here, `feature_observations` and `target_observations` are lists whose individual items are tensors, so the loader stacks them into minibatch tensors.',2,['f4'])
old='In the supplied fixture, a fixture has four observations with two features, and the declared model uses widths 2 → 3 → 1.'
new='The supplied fixture has four observations with two features, and the declared model uses widths 2 → 3 → 1.'
for sid in ['s12','r03','r06']:
 s=step('mle.tile.035_037',sid);matches=[b for b in s['blocks'] if old in b.get('text','')];assert len(matches)==1
 matches[0]['text']=matches[0]['text'].replace(old,new)
s=step('mle.tile.038_040','s01');b=next(b for b in s['blocks'] if b['type']=='code_walkthrough');needle='assert torch.allclose(W.grad, reference_W, rtol=rtol, atol=atol)';assert b['code'].count(needle)==1
b['code']=b['code'].replace(needle,'assert W.grad.shape == reference_W.shape\nassert b.grad.shape == reference_b.shape\n'+needle)
changed=[]
for a,t in zip(before['tiles'],d['tiles']):
 for group in ['steps','remediation_steps']:
  for x,y in zip(a[group],t[group]):
   if x!=y: changed.append(y['step_id'])
assert len(changed)==6,changed
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('Changed:',', '.join(changed))
print('Counts:',len(d['tiles']),'tiles;',sum(len(t['steps']) for t in d['tiles']),'planned steps;',sum(len(t['remediation_steps']) for t in d['tiles']),'remediation steps')
