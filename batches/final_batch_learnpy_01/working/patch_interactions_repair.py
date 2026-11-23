import json
from pathlib import Path
B=Path('batches/final_batch_learn_python.region.01')
p=B/'interactions.json'
d=json.loads(p.read_text())
# Patch only the named variable-assignment exercise; preserve all grading values,
# constraints, ids, and all other interactions.
s=next(s for t in d['tiles'] for s in t['interactions'] if s['step_id']=='learn_python.tile.000_002.s04')
i=s['interaction'];pub=i['public'];g=i['grading']
old=pub['workspace']['files'][0]['content']
sol=g['solution_files'][0]['content']
assert sol.startswith(old)
expression=sol[len(old):].strip().split(' = ',1)[1]
scaffold=old+'purchase_cost = '+expression+'\n'
pub['workspace']['files'][0]['content']=scaffold
g['solution_files'][0]['content']=scaffold+'cost = purchase_cost\n'
pub['prompt']='Keep the supplied assignments. purchase_cost already holds quantity multiplied by unit_price using their current values. Reassign cost from purchase_cost. The checker reads quantity, unit_price and cost.'
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
# Audit immutable constraints against the glossary, and check plan fidelity/counts.
bundles=json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']
byid={b['context']['concept_id']:b for b in bundles}
counts={}
for t in d['tiles']:
 for s in t['interactions']:
  ix=s['interaction'];counts[ix['type']]=counts.get(ix['type'],0)+1
  if ix['type']=='code_exercise':
   cid=next(a.split('#')[0] for a in ix['anchors'] if a.endswith('#practice'))
   live=byid[cid]['practice_anchor']['live_code']
   assert ix['public']['constraints']=={k:live[k] for k in ('allowed_syntax','blocked_syntax')}
print(counts)
# Execute the unchanged test expression rather than supplying expected values.
ns={};exec(g['solution_files'][0]['content'],ns)
for test in g['tests']:
 if test['kind']=='value_equals':assert eval(test['spec']['expr'],ns)==test['spec']['expected']
ns={};exec(scaffold,ns)
assert any(eval(test['spec']['expr'],ns)!=test['spec']['expected'] for test in g['tests'] if test['kind']=='value_equals')
print('Patched one interaction; constraints unchanged; solution passes; starter fails.')
