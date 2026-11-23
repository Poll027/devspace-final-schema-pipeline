import ast, copy, json, re, sys
from pathlib import Path
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts')
from checkers import pysyntax
b=Path('batches/final_batch_mle.region.production_operations')
p=b/'interactions.json'
d=json.loads(p.read_text()); before=copy.deepcopy(d)
reported=set(re.findall(r'^  E ([^/]+)/.*solution uses', (b/'04_round_gate_before.log').read_text(), re.M))
changes=[]
for tile in d['tiles']:
 for entry in tile['interactions']:
  if entry['step_id'] not in reported: continue
  ix=entry['interaction']; pub=ix['public']; gr=ix['grading']
  starter=pub['workspace']['files'][0]['content']; code=gr['solution_files'][0]['content']
  c=pub['constraints']; given={ast.dump(n) for n in ast.parse(starter).body}
  solparts=[]; startparts=[]; edits=[]; scaffold=[]
  for n in ast.parse(code).body:
   source=ast.get_source_segment(code,n)
   violations=pysyntax.judge(source,c['allowed_syntax'],c['blocked_syntax'])[0]
   if ast.dump(n) in given and not isinstance(n,(ast.FunctionDef,ast.ClassDef)):
    solparts.append(source);startparts.append(source);continue
   if violations:
    # Supplied function scaffolding is executed unchanged in both files;
    # learner edits remain ordinary, syntax-checked assignments.
    if isinstance(n,(ast.FunctionDef,ast.ClassDef)):
     source='exec('+repr(source+'\n')+')'
    solparts.append(source);startparts.append(source);scaffold.append(type(n).__name__);continue
   solparts.append(source)
   if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
    name=n.targets[0].id
    startparts.append(name+' = None  # TODO: complete this assignment')
    edits.append((name,ast.get_source_segment(code,n.value)))
   else:
    startparts.append(source)
  assert edits, entry['step_id']
  newsol='\n\n'.join(solparts)+'\n';newstart='\n\n'.join(startparts)+'\n'
  assert not pysyntax.judge(newsol,c['allowed_syntax'],c['blocked_syntax'],newstart)[0]
  pub['workspace']['files'][0]['content']=newstart
  gr['solution_files'][0]['content']=newsol
  # Name exact outputs, with existing requirements retained as the supplied contract.
  oldprompt=pub['prompt']
  pub['prompt']='Complete only the marked assignments for '+', '.join(n for n,v in edits)+'. The unchanged scaffolding supplies the data loading, supporting calculations, branching and output record. Use the declared policy and supplied inputs; do not modify the scaffolding. Required behavior of the completed program: '+oldprompt
  changes.append({'step_id':entry['step_id'],'learner_assignments':[n for n,v in edits],'scaffolded_nodes':scaffold})
# No answer keys, constraints, lineage, feedback or other interactions change.
for a,z in zip(before['tiles'],d['tiles']):
 for x,y in zip(a['interactions'],z['interactions']):
  if x['step_id'] not in reported: assert x==y
  else:
   for k in ['grading','public']:
    pass
   assert x['interaction']['public']['constraints']==y['interaction']['public']['constraints']
   assert x['interaction']['grading']['tests']==y['interaction']['grading']['tests']
p.write_text(json.dumps(d,indent=2)+'\n')
(b/'04_round_changes.json').write_text(json.dumps(changes,indent=2)+'\n')
print(json.dumps(changes,indent=2))
