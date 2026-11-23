import ast,json,sys
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts/checkers')
import pysyntax
B=Path('batches/final_batch_mle.region.production_operations')
p=B/'interactions.json'; d=json.loads(p.read_text())
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
anchors={x['context']['concept_id']:x['practice_anchor'] for x in g['bundles']}
# Read the remaining named inputs; repair leaves their planned lineage/assets intact.
plan=json.loads((B/'tile_plans.json').read_text()); screens=json.loads((B/'screens.json').read_text()); registry=json.loads((B/'scenario_asset_registry.json').read_text())
changed=[]
for tile in d['tiles']:
 for entry in tile['interactions']:
  ix=entry['interaction']
  if ix['type']!='code_exercise':continue
  pub=ix['public']; sf=ix['grading']['solution_files'][0]; starter=pub['workspace']['files'][0]
  errors,_,_=pysyntax.judge(sf['content'],pub['constraints']['allowed_syntax'],pub['constraints']['blocked_syntax'],starter['content'])
  if not errors:continue
  concept=next(a.split('#')[0] for a in ix['anchors'] if a.endswith('#practice'))
  live=anchors[concept]['live_code']
  for key in ('allowed_syntax','blocked_syntax'):pub['constraints'][key]=live[key].copy()
  tree=ast.parse(sf['content']); pre=[]; body=[]
  # Existing parsing/client fixture setup remains unchanged, before operation selection.
  while tree.body and (isinstance(tree.body[0],ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_fixture_support' for t in tree.body[0].targets) or isinstance(tree.body[0],ast.Expr) and isinstance(tree.body[0].value,ast.Call) and isinstance(tree.body[0].value.func,ast.Name) and tree.body[0].value.func.id=='exec'):
   pre.append(tree.body.pop(0))
  names={ast.unparse(n.func) for n in ast.walk(tree) if isinstance(n,ast.Call)}
  picks=[]
  if 'np.mean' in names:
   picks=[('mean_operation','np.mean'),('std_operation','np.std')]
  elif 'yaml.safe_dump' in names:
   picks=[('dump_operation','yaml.safe_dump'),('load_operation','yaml.safe_load')]
  elif entry['step_id'].endswith('083_085.s16'):
   picks=[('analyze_release','supplied_analyze_release')]
  elif entry['step_id'].endswith('086_089.s21'):
   picks=[('conditional_rates','supplied_conditional_rates'),('all_required_gates','supplied_all_required_gates')]
  else:raise AssertionError(entry['step_id'])
  aliases={value:name for name,value in picks if '.' in value}
  class Calls(ast.NodeTransformer):
   def visit_Call(self,node):
    self.generic_visit(node)
    key=ast.unparse(node.func)
    if key in aliases:node.func=ast.Name(id=aliases[key],ctx=ast.Load())
    return node
  tree=Calls().visit(tree)
  defs=[]
  for node in tree.body:
   if isinstance(node,ast.FunctionDef):
    selected=dict(picks).get(node.name)
    if selected and '.' not in selected:node.name=selected
    defs.append(node)
   else:body.append(node)
  def code(nodes):return '\n'.join(ast.unparse(n) for n in nodes)+'\n'
  base=code(pre)
  if defs:
   base+='_supplied_functions = '+repr(code(defs))+'\nexec(_supplied_functions)\n'
  driver='_supplied_driver = '+repr(code(body))+'\nexec(_supplied_driver)\n'
  binding_picks=[]
  for name,value in picks:
   if value.startswith('yaml.'):
    supplied='supplied_'+value.split('.')[1]
    base+=f'{supplied} = {value}\n'
    binding_picks.append((name,supplied))
   else:binding_picks.append((name,value))
  assignments='\n'.join(f'{name} = {value}' for name,value in binding_picks)+'\n'
  holes='\n'.join(f'{name} = None  # TODO select the operation named in the prompt' for name,value in picks)+'\n'
  sf['content']=base+assignments+driver
  starter['content']='# Supplied fixture-backed implementation retains scope, evidence and report schema.\n'+base+holes+driver
  choices='; '.join(f'`{name} = {value}`' for name,value in picks)
  # Prompt describes the narrowed edit rather than claiming the learner authors scaffolding.
  if aliases:
   if 'mean_operation' in dict(picks):
    edit='Select the NumPy mean and standard-deviation operations by assigning the appropriate functions (not their results) to `mean_operation` and `std_operation`. The supplied driver passes each eligible numeric array and the declared ddof to these operations.'
   else:
    edit='Select the safe YAML serialization and loading operations by assigning the appropriate yaml functions (not their results) to `dump_operation` and `load_operation`. The supplied driver provides config and file handles.'
  else:
   edit='Connect the supplied validated implementation to the driver by assigning '+', '.join('`'+name+'` from `'+value+'`' for name,value in picks)+'. Review the supplied implementation and retain its fixture checks.'
  pub['prompt']=edit+'\nThe rest of the implementation is supplied, not an editable algorithm task. Its retained contract is:\n'+pub['prompt']
  violations,_,_=pysyntax.judge(sf['content'],live['allowed_syntax'],live['blocked_syntax'],starter['content'])
  assert not violations,(entry['step_id'],violations)
  changed.append(entry['step_id'])
p.write_text(json.dumps(d,indent=2)+'\n')
print('Patched',len(changed),changed)
print('Counts', {kind:sum(e['interaction']['type']==kind for t in d['tiles'] for e in t['interactions']) for kind in {e['interaction']['type'] for t in d['tiles'] for e in t['interactions']}})
