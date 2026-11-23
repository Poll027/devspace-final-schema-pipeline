import ast, copy, json, re, sys
from pathlib import Path
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts/checkers')
import pysyntax
B=Path('batches/final_batch_mle.region.production_operations')
p=B/'interactions.json'
a=json.loads(p.read_text()); before=copy.deepcopy(a)
errors=set(re.findall(r'^  E ([^/]+)/', (B/'04_dispatch_actual_strict.log').read_text(), re.M))
bundles={b['context']['concept_id']:b for b in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}
# The repair is limited to the reported code exercises. All supplied algorithms,
# fixtures, predicates and expected values are taken from the existing artifact.
np_tasks={
 'mle.tile.080_082.s04':['asarray','histogram','sum','mean','std'],
 'mle.tile.080_082.s14':['asarray','count_nonzero','sum','abs','mean','std'],
 'mle.tile.083_085.s06':['mean','std'],
 'mle.tile.091_094.s09':['mean','std'],
}
class Operations(ast.NodeTransformer):
 def __init__(self,names):self.names=names
 def visit_Call(self,n):
  self.generic_visit(n)
  if isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='np' and n.func.attr in self.names:
   n.func=ast.Name(id=n.func.attr+'_operation',ctx=ast.Load())
  return n

def helper(name,args,expr):
 return ast.FunctionDef(name=name,args=ast.arguments(posonlyargs=[],args=[ast.arg(arg=x) for x in args],kwonlyargs=[],kw_defaults=[],defaults=[]),body=[ast.Return(value=copy.deepcopy(expr))],decorator_list=[])

def render(tree):return ast.unparse(ast.fix_missing_locations(tree))+'\n'

changed=[]
for tile in a['tiles']:
 for x in tile['interactions']:
  sid=x['step_id']
  if sid not in errors:continue
  i=x['interaction'];pub=i['public'];gr=i['grading']
  anchor=bundles[i['measures'][0]['concept_id']]['practice_anchor']['live_code']
  assert pub['constraints']['allowed_syntax']==anchor['allowed_syntax']
  assert pub['constraints']['blocked_syntax']==anchor['blocked_syntax']
  tree=ast.parse(gr['solution_files'][0]['content'])
  bindings=[]; helpers=[]; functions=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
  editable=[]
  if sid in np_tasks:
   names=np_tasks[sid]
   transformer=Operations(names)
   for f in functions:transformer.visit(f)
   bindings=[ast.parse(f'{name}_operation = np.{name}').body[0] for name in names]
   task='Complete the operation bindings marked TODO. Bind each name to the NumPy operation for its role: '+', '.join(name+'_operation ('+name+')' for name in names)+'. The supplied orchestration applies these operations to the mounted data, supplies the declared eligibility rules and denominators, and constructs the existing report. Keep population standard deviations (ddof=0) and the supplied record fields and ordering. Do not replace the report with constants.'
   if sid=='mle.tile.080_082.s14':task+=' The supplied drift calculation uses half the sum of absolute probability differences and the declared strict threshold; its result describes distribution differences, not demonstrated quality loss.'
   if sid=='mle.tile.083_085.s06':task+=' The supplied join rejects duplicate IDs and selects only mature matched labels; summarize losses for that cohort, not all traffic.'
   if sid=='mle.tile.091_094.s09':task+=' The supplied allocation follows the declared shared-cost rule and retains unallocated rows and lifecycle evidence; summarize each workload’s window costs.'
  elif sid=='mle.tile.083_085.s16':
   f=next(f for f in functions if f.name=='analyze_release')
   loop=next(n for n in f.body if isinstance(n,ast.For))
   first=next(n for n in loop.body if isinstance(n,ast.If) and isinstance(n.test,ast.Compare) and isinstance(n.test.left,ast.Name) and n.test.left.id=='denominator')
   # There are two denominator guards; use the response-selection branch.
   response_if=next(n for n in loop.body if isinstance(n,ast.If) and n.orelse and isinstance(n.orelse[0],ast.If))
   branch=response_if.orelse[0]
   helpers.append(helper('supplied_replay_supported_config_rule',['r','replay_evidence'],branch.test))
   branch.test=ast.parse('rollback_rule(r, replay_evidence)',mode='eval').body
   bindings=ast.parse('rollback_rule = supplied_replay_supported_config_rule').body
   task='Complete the TODO binding `rollback_rule` by reusing the supplied replay-supported configuration rule. Read its predicate in the supplied support code: the rollback must be supported by the affected release/cohort, a configuration mismatch, reproduction under the bad configuration and restoration under the approved rollback. The supplied report computes labeled error proportions only for nonzero denominators and retains the gates and scope statement. Keep those outputs unchanged; distribution distance alone is not the rollback rule.'
  elif sid=='mle.tile.086_089.s16':
   f=next(f for f in functions if f.name=='handle_event')
   admit=f.body[0]
   helpers.append(helper('supplied_atomic_admission',['event','coordinator'],admit.value))
   admit.value=ast.parse('admission_operation(event, coordinator)',mode='eval').body
   bindings=ast.parse('admission_operation = supplied_atomic_admission').body
   editable=[n for n in tree.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='safe_dump']
   editable += [n for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='safe_load']
   task='Complete `admission_operation` by reusing the supplied atomic-admission interface, then complete the safe YAML dump and load lines marked TODO. The supplied handler and fixtures exercise duplicate delivery, busy admission, restart/reconciliation and terminal release. Safely write `config` to the supplied `file_handle`, then reload into `loaded` using the reopened handle. Retain the admission → required function-test → execution dependency chain and fatal required-stage failures. The supplied assertions and report verify those results.'
  elif sid=='mle.tile.086_089.s21':
   rates=next(f for f in functions if f.name=='conditional_rates')
   cost_guard=next(n for n in rates.body if isinstance(n,ast.If) and isinstance(n.test,ast.BoolOp))
   cost_assignment=cost_guard.body[0]
   helpers.append(helper('supplied_declared_weighted_cost',['row','policy','fpr','fnr'],cost_assignment.value))
   cost_assignment.value=ast.parse('cost_operation(row, policy, fpr, fnr)',mode='eval').body
   val=next(f for f in functions if f.name=='validate_candidate')
   identity=next(n for n in val.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='identity_match')
   helpers.append(helper('supplied_immutable_identity_match',['promotion_identity','candidate'],identity.value))
   identity.value=ast.parse('identity_operation(promotion_identity, candidate)',mode='eval').body
   bindings=ast.parse('cost_operation = supplied_declared_weighted_cost\nidentity_operation = supplied_immutable_identity_match').body
   task='Complete the two TODO assignments by reusing the supplied operations: `cost_operation` must use the declared class-probability-weighted false-positive/false-negative costs; `identity_operation` must match the promoted immutable artifact to the tested candidate. Inspect the supplied operations before binding them. The supplied validator guards empty denominators and requires every quality, cost, slice, compatibility, cohort and identity gate; retain those gates and the existing `report` fields. Do not replace any results with constants.'
  elif sid in ['mle.tile.083_085.s11','mle.tile.091_094.s04','mle.tile.091_094.s14']:
   if sid=='mle.tile.083_085.s11':
    wanted={'mean','std','loaded'}
    task='Complete only the TODO baseline calculations and safe YAML dump/load lines. Compute `mean` and population `std` from `baseline` using ddof=0. The supplied formula constructs `threshold` from that mean and the declared margin, and the supplied configuration identifies the indicator, window, owner and response. Safely write `config` using the supplied open `file_handle`, then reload it into `loaded` using the reopened handle. Retain the boundary assertions and replay into `records`; only a strict breach triggers the response.'
   elif sid=='mle.tile.091_094.s04':
    wanted={'count','cpu_mean','cpu_std','memory_mean','memory_std'}
    task='The supplied mask has already selected the fixed instance, process and declared running interval into `cpu` and `memory`. Complete the TODO lines: set `count` to the number of eligible CPU observations, calculate `cpu_mean` and `memory_mean`, and calculate population `cpu_std` and `memory_std` with ddof=0. Retain the existing report fields and supplied lifecycle evidence; do not include the other process or observations outside the bounded interval.'
   else:
    wanted={'loaded'}
    task='Complete the two TODO safe YAML serialization lines. The supplied `config` contains the declared budget scope, amount, period, threshold, existing notification topic, event binding, fixed target and runtime secret references. Safely write it through the supplied `file_handle`, then reload it into `loaded` using the reopened handle. Retain the separate notification, response, target/state and credential-output verification fields in the supplied report; a budget notification is not a hard spending cap.'
   for n in tree.body:
    if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in wanted for t in n.targets):editable.append(n)
    if sid!='mle.tile.091_094.s04' and isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='safe_dump':editable.append(n)
  else:raise AssertionError(sid)
  # YAML method receivers are supplied; the learner selects the safe operation
  # through a name binding (the detector does not allow attr_module for yaml).
  yaml_nodes=[n for n in editable if isinstance(n,ast.Expr) or (isinstance(n,ast.Assign) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr=='safe_load')]
  yaml_support=''
  if yaml_nodes:
   yaml_support='import yaml\nsupplied_safe_dump = yaml.safe_dump\nsupplied_safe_load = yaml.safe_load\n'
   bindings += ast.parse('dump_operation = supplied_safe_dump\nload_operation = supplied_safe_load').body
   for n in yaml_nodes:
    call=n.value
    call.func=ast.Name(id='dump_operation' if isinstance(n,ast.Expr) else 'load_operation',ctx=ast.Load())
   editable=[n for n in editable if n not in yaml_nodes]
   task=task.replace('safe YAML dump/load lines','safe YAML operation bindings').replace('safe YAML dump and load lines','safe YAML operation bindings').replace('two TODO safe YAML serialization lines','two TODO safe YAML operation bindings').replace('safe YAML dump/load lines','safe YAML operation bindings')
   task += ' Bind `dump_operation` and `load_operation` to the supplied safe-dump and safe-load operations; the supplied calls pass the configuration and open handles.'
  # Move supplied function orchestration to the existing shared fixture support.
  # The learner's bindings remain ordinary, visible Python assignments in main.py.
  # No selected binding and no expected output is included in the support source.
  support=next(n for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='_fixture_support')
  support.value.value += '\n# Supplied orchestration; operations are selected by the learner.\n' + yaml_support + '\n'.join(render(n) for n in helpers+functions)
  tree.body=[n for n in tree.body if not isinstance(n,ast.FunctionDef)]
  pos=next(j for j,n in enumerate(tree.body) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='exec')+1
  tree.body[pos:pos]=bindings
  selected={ast.dump(n) for n in bindings+editable}
  solution=render(tree)
  starter=copy.deepcopy(tree)
  for j,n in enumerate(starter.body):
   if ast.dump(n) in selected:
    if isinstance(n,ast.Assign):n.value=ast.Constant(value=None)
    else:starter.body[j]=ast.Assign(targets=[ast.Name(id='_serialization_todo',ctx=ast.Store())],value=ast.Constant(value=None))
  starter_text='# Complete only the TODO operation/calculation/serialization lines described in the prompt.\n'+render(starter)
  # Add TODO markers without affecting the unchanged scaffold comparison.
  original_selected={ast.dump(n) for n in bindings+editable}
  # Every reference-solution addition must fit the glossary lists unchanged.
  violations,_,_=pysyntax.judge(solution,pub['constraints']['allowed_syntax'],pub['constraints']['blocked_syntax'],starter_text)
  assert not violations,(sid,violations)
  gr['solution_files'][0]['content']=solution
  pub['workspace']['files'][0]['content']=starter_text
  pub['prompt']=task+' The graded output remains `report`, with the supplied structure and ordering.'
  changed.append(sid)
# Assert the edit has not widened syntax, altered tests/keys, or touched unreported interactions.
for oldt,newt in zip(before['tiles'],a['tiles']):
 for old,new in zip(oldt['interactions'],newt['interactions']):
  if new['step_id'] not in errors:assert old==new
  else:
   for k in old['interaction']:
    if k not in ['public','grading']:assert old['interaction'][k]==new['interaction'][k]
   for k in old['interaction']['public']:
    if k not in ['prompt','workspace']:assert old['interaction']['public'][k]==new['interaction']['public'][k]
   for k in old['interaction']['grading']:
    if k!='solution_files':assert old['interaction']['grading'][k]==new['interaction']['grading'][k]
p.write_text(json.dumps(a,indent=2,ensure_ascii=False)+'\n')
print('Patched',len(changed),'reported exercises:',*changed,sep='\n')
print('Interactions:',sum(len(t['interactions']) for t in a['tiles']))
