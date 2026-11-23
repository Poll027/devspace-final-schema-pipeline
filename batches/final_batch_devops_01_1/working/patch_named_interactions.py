import json, copy
from pathlib import Path
p=Path('batches/final_batch_aws_devops.region.01_1')
f=p/'interactions.json'; d=json.loads(f.read_text()); before=copy.deepcopy(d)
ix={i['step_id']:i['interaction'] for t in d['tiles'] for i in t['interactions']}
r=json.loads((p/'scenario_asset_registry.json').read_text())
def rows(aid):
 a=next(a for a in r['assets'] if a['asset_id']==aid)
 return [dict(zip([c['name'] for c in a['columns']],row)) for row in a['rows']]
a,b,c=rows('ds.subnet_candidates')
msg=f"Choose {a['candidate_id']} for {a['availability_zone']} and {b['candidate_id']} for {b['availability_zone']}: their /{a['subnet_cidr'].split('/')[-1]} ranges are contained, nonoverlapping and provide {a['usable_addresses']} usable addresses each. {c['candidate_id'].capitalize()} overlaps {a['candidate_id']} and provides only {c['usable_addresses']} usable addresses, below the requirement of {c['required_usable_addresses']}."
for tid in ['t1','t2']: ix['aws_devops.tile.001.s04']['grading']['task_feedback'][tid]['incorrect']=msg
a,b,c=rows('ds.recovery_options')
ix['aws_devops.tile.004.s04']['grading']['task_feedback']['t1']['incorrect']=f"{a['approach_id']} meets both limits: restoration is {a['restoration_minutes']} minutes against RTO {a['rto_minutes']}, and data loss is {a['data_loss_minutes']} minutes against RPO {a['rpo_minutes']}. {b['approach_id']} exceeds RPO; {c['approach_id']} exceeds RTO."
ix['aws_devops.tile.001.s03']['feedback']['hints']=['Check whether each individual subnet is assigned entirely to one Availability Zone.']
pub=ix['aws_devops.tile.008.s04']['public']
head,code=pub['prompt'].split('```json\n'); body,tail=code.split('\n```',1)
policy=json.loads(body)
for st in policy['Statement']:
 assert isinstance(st['Condition'],str)
 st['Condition']=json.loads(st['Condition'])
pub['prompt']=head+'Here, the resource ending in `sandbox-orders/*` matches objects under `sandbox-orders/`. `StringEquals` requires the named principal-tag value to equal `yes`.\n```json\n'+json.dumps(policy,indent=2)+'\n```'+tail
# Restrict changes to exactly the five named leaves, with no answer key changes.
def diffs(a,b,path=()):
 if isinstance(a,dict):
  assert a.keys()==b.keys()
  return sum((diffs(a[k],b[k],path+(k,)) for k in a),[])
 if isinstance(a,list):
  assert len(a)==len(b)
  return sum((diffs(x,y,path+(i,)) for i,(x,y) in enumerate(zip(a,b))),[])
 return [path] if a!=b else []
changed=diffs(before,d);assert len(changed)==5,changed
for path in changed: print('/'.join(map(str,path)))
f.write_text(json.dumps(d,indent=2)+'\n')
print('Tiles:',len(d['tiles']),'Interactions:',sum(len(t['interactions']) for t in d['tiles']))
