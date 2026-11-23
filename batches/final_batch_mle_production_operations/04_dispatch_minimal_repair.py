import ast, copy, json
from pathlib import Path
B=Path('batches/final_batch_mle.region.production_operations')
p=B/'interactions.json'
d=json.loads(p.read_text()); before=copy.deepcopy(d)
ids={'mle.tile.086_089.s16','mle.tile.086_089.s21','mle.tile.090_090.s05','mle.tile.091_094.s14'}
for tile in d['tiles']:
 for entry in tile['interactions']:
  sid=entry['step_id']
  if sid not in ids: continue
  i=entry['interaction']; starter=i['public']['workspace']['files'][0]; solution=i['grading']['solution_files'][0]
  s=starter['content']; v=solution['content']
  if sid.endswith('086_089.s16'):
   # Retain the implemented admission routine as unchanged scaffolding;
   # only wiring the callable is learner-authored.
   tree=ast.parse(v); node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='admit')
   lines=v.splitlines(True); block=''.join(lines[node.lineno-1:node.end_lineno]); supplied=block.replace('def admit(', 'def supplied_admission(',1)
   prefix=''.join(lines[:node.lineno-1])+supplied+'\n\n# Bind the admission entry point to the supplied routine.\nadmit = '
   suffix=''.join(lines[node.end_lineno:])
   starter['content']=prefix+'None\n'+suffix; solution['content']=prefix+'supplied_admission\n'+suffix
   i['public']['prompt']='Inspect the supplied admission routine and bind `admit` to the routine that atomically reserves the key and pipeline, defers busy claims, retains completed keys, reconciles the persisted executor identity, and releases capacity only after terminal confirmation. Edit only the `admit` assignment. Keep the supplied YAML, coordinator, executor and concurrency/restart assertions unchanged; the tests read the status/job-ID record returned by `admit(event, coordinator, executor)`.'
  elif sid.endswith('086_089.s21'):
   tree=ast.parse(v); nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'rates','evaluate'}]
   lines=v.splitlines(True); first=min(n.lineno for n in nodes); last=max(n.end_lineno for n in nodes)
   block=''.join(lines[first-1:last]).replace('def rates(', 'def supplied_rates(',1).replace('def evaluate(', 'def supplied_gate(',1)
   prefix=''.join(lines[:first-1])+block+'\n\n# Bind conditional-rate and validation-gate entry points.\n'
   suffix=''.join(lines[last:])
   starter['content']=prefix+'rates = None\nevaluate = None\n'+suffix
   solution['content']=prefix+'rates = supplied_rates\nevaluate = supplied_gate\n'+suffix
   i['public']['prompt']='Inspect the supplied conditional-rate and candidate-gate routines. Bind `rates` and `evaluate` to their corresponding supplied routines by editing only those two assignments. Preserve undefined rates for empty conditioning groups, the supplied cost weights, every quality/slice/compatibility gate, matched cohort and exact candidate identity. Retain the assertions and fixtures; the checker reads the FPR, FNR, expected_cost and verdict record returned by `evaluate`.'
  elif sid.endswith('090_090.s05'):
   # Only the simulator definition was divergent; keep it identical in both files.
   sl=s.splitlines(True); vl=v.splitlines(True)
   start=next(j for j,l in enumerate(sl) if l.startswith('# Supplied simulator interface:'))
   end=next(j for j,l in enumerate(sl[start:],start) if l.startswith('recover = '))+1
   sim=next(l for l in vl if l.startswith('exec("def recover('))
   starter['content']=''.join(sl[:start])+sim+''.join(sl[end:])
  else:
   # Populate unchanged mapping scaffolding with named input slots. Learner
   # lines select supplied policy values without writing new mapping ASTs.
   tree=ast.parse(v); node=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='config' for t in n.targets))
   lines=v.splitlines(True); mapping=node.value
   declarations=[]; blank=[]; complete=[]; pairs=[]
   for key,value in zip(mapping.keys,mapping.values):
    name=key.value
    if name=='response_step': pairs.append('    '+repr(name)+': response_step,'); continue
    input_name='supplied_'+name; slot='selected_'+name
    declarations.append(input_name+' = '+ast.get_source_segment(v,value)+'\n')
    blank.append(slot+' = None\n'); complete.append(slot+' = '+input_name+'\n')
    pairs.append('    '+repr(name)+': '+slot+',')
   prefix=''.join(lines[:node.lineno-1])+''.join(declarations)+'\n# Fill each selected field from the corresponding supplied value.\n'
   suffix='\nconfig = {\n'+'\n'.join(pairs)+'\n}\n'+''.join(lines[node.end_lineno:])
   starter['content']=prefix+''.join(blank)+suffix; solution['content']=prefix+''.join(complete)+suffix
   i['public']['prompt']='Complete only the `selected_*` assignments using the corresponding supplied policy values and runtime references. The unchanged mapping scaffolding assembles `config`, safely serializes and reloads it, and inspects its scope, target, event binding and secret references before replay. Preserve the below-threshold, boundary and breach assertions; the checker reads `result`, including fixed-target stop evidence, credential non-disclosure and the notification-lag limitation. Do not change the supplied values or serialization/replay scaffolding.'
for old,new in zip(before['tiles'],d['tiles']):
 for a,b in zip(old['interactions'],new['interactions']):
  if a['step_id'] not in ids: assert a==b
  else:
   assert a['interaction']['public']['constraints']==b['interaction']['public']['constraints']
   assert a['interaction']['grading']['tests']==b['interaction']['grading']['tests']
p.write_text(json.dumps(d,indent=2)+'\n')
print('Patched four named interactions; constraints, tests and all other interactions unchanged.')
