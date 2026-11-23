import ast, json, re, sys
from pathlib import Path
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts')
from checkers.pysyntax import judge
b = Path('batches/final_batch_mle.region.production_operations')
p = b / 'interactions.json'
d = json.loads(p.read_text())
before = json.loads(p.read_text())
errors = set(re.findall(r'  E ([^/]+)/', (b/'04_gate_repair_live.log').read_text()))
# Only the named syntax failures: retain keys, tests, constraints, and unrelated interactions.
slots = {
'mle.tile.080_082.s04': ['mean_calculation', 'std_calculation'],
'mle.tile.080_082.s14': ['ref_mean', 'cur_mean', 'ref_std', 'cur_std'],
'mle.tile.083_085.s06': ['mean_calculation', 'std_calculation'],
'mle.tile.083_085.s11': ['baseline_mean', 'baseline_std'],
'mle.tile.083_085.s16': ['rollback_response'],
'mle.tile.086_089.s16': ['admit'],
'mle.tile.086_089.s21': ['evaluate'],
'mle.tile.091_094.s04': ['cpu_mean', 'cpu_std', 'memory_mean', 'memory_std'],
'mle.tile.091_094.s09': ['training_mean', 'training_std', 'inference_mean', 'inference_std'],
'mle.tile.091_094.s14': ['dump_config', 'load_config'],
}
prompts = {
'mle.tile.080_082.s04': 'Complete mean_calculation(values) and std_calculation(values, ddof) using the NumPy mean and standard-deviation calls. The supplied summary engine selects eligible values, normalizes bins and declared categories/classes by their own totals, and emits the identity-bound record. Retain that scaffolding; the replay uses the declared ddof=0 divisor.',
'mle.tile.080_082.s14': 'Complete ref_mean, cur_mean, ref_std and cur_std from ref_values and cur_values using NumPy; use ddof=0. Retain the supplied probability normalization, distance calculations, threshold comparisons and separate drift/quality evidence replay.',
'mle.tile.083_085.s06': 'Complete mean_calculation(values) and std_calculation(values, ddof) using NumPy. Retain the supplied mature-cohort matching and coverage engine: its loss summaries must use these callbacks and the declared ddof=0 divisor. Unavailable labels remain unavailable rather than counted as correct.',
'mle.tile.083_085.s11': 'Complete baseline_mean and baseline_std from baseline using NumPy, with ddof=0. Retain the supplied configuration, safe YAML round trip and normal/boundary/breached replay; the alert threshold is derived from your baseline_mean.',
'mle.tile.083_085.s16': 'Complete rollback_response by assigning the supplied label_approved_rollback name. Retain the supplied cohort-rate calculation and diagnostic replay: it uses this response only for the supported approved-configuration rollback, with readiness and bounded-prediction gates.',
'mle.tile.086_089.s16': 'Complete admit by assigning supplied_admit, the supplied durable-admission implementation. Retain the fixture replay and fatal test dependencies. Inspect the supplied implementation: it reserves the run key and pipeline slot atomically, reuses persisted job identity after an unknown response or restart, and releases the slot only after terminal confirmation.',
'mle.tile.086_089.s21': 'Complete evaluate by assigning supplied_evaluate, the supplied validation implementation. Retain its fixture replay. Inspect the supplied calculation: it rejects undefined actual-class conditioning groups and enforces both quality limits, incumbent-relative expected cost, slice and compatibility checks, cohort agreement and exact artifact identity.',
'mle.tile.091_094.s04': 'Complete cpu_mean, cpu_std, memory_mean and memory_std from cpu and memory using NumPy, with ddof=0. Retain the supplied named-instance/process running-interval mask and result fields; summarize only those selected observations.',
'mle.tile.091_094.s09': 'Complete training_mean, training_std, inference_mean and inference_std from training_values and inference_values using NumPy, with ddof=0. Retain the supplied lifecycle sequences, resource mapping, shared-charge allocation and reconciliation. The workload summaries use the complete declared reporting windows, including zero-charge windows.',
'mle.tile.091_094.s14': 'Complete dump_config and load_config by assigning safe_dump_interface and safe_load_interface respectively. Retain the supplied event-response configuration, safe YAML file round trip and bounded notification replay; it checks the fixed target, event binding, runtime secret reference and credential non-disclosure.',
}
changes = []
for t in d['tiles']:
 for e in t['interactions']:
  sid = e['step_id']
  if sid not in errors: continue
  i=e['interaction']; solution=i['grading']['solution_files'][0]['content']
  nodes=ast.parse(solution).body
  source_node=next((n for n in nodes if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='support_source' for x in n.targets)),None)
  if source_node:
   source=source_node.value.value
   # Use the supplied engine directly in the same namespace, without module wiring.
   if sid.endswith('086_089.s16'): source=source.replace('def admit(', 'def supplied_admit(')
   if sid.endswith('086_089.s21'): source=source.replace('def evaluate(', 'def supplied_evaluate(')
   parts=[]
   for n in nodes:
    text=ast.get_source_segment(solution,n)
    if n is source_node:
     parts.append('exec('+repr(source)+')');continue
    if text=='import types' or text.startswith('support =') or text.startswith('support.') or text.startswith('exec(support_source,') or ' = support.' in text:continue
    parts.append(text)
   solution='\n\n'.join(parts)+'\n'
  starter_parts=[]
  for n in ast.parse(solution).body:
   text=ast.get_source_segment(solution,n)
   name=n.name if isinstance(n,ast.FunctionDef) else (n.targets[0].id if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) else None)
   if name in slots[sid]:
    if isinstance(n,ast.FunctionDef):
     n.body=[ast.Return(value=ast.Constant(None))];text=ast.unparse(n)+' # TODO: calculate the requested statistic'
    else: text=name+' = None # TODO: complete this assignment'
   starter_parts.append(text)
  starter='\n\n'.join(starter_parts)+'\n'
  c=i['public']['constraints']
  violations=judge(solution,c['allowed_syntax'],c['blocked_syntax'],starter=starter)[0]
  assert not violations,(sid,violations)
  i['public']['workspace']['files'][0]['content']=starter
  i['grading']['solution_files'][0]['content']=solution
  i['public']['prompt']=prompts[sid]
  changes.append(sid)
# Verify constraints match the immutable practice lists, and no other fields changed.
g=json.loads((b/'inputs/path_glossary_bundle.json').read_text())
anchors={x['context']['concept_id']:x['practice_anchor'] for x in g['bundles']}
for ot,nt in zip(before['tiles'],d['tiles']):
 for oe,ne in zip(ot['interactions'],nt['interactions']):
  if oe['step_id'] not in errors: assert oe==ne
  else:
   oi,ni=oe['interaction'],ne['interaction']
   assert oi['public']['constraints']==ni['public']['constraints']
   assert oi['grading']['tests']==ni['grading']['tests']
   for anchor in ni['anchors']:
    cid=anchor.split('#')[0]
    if cid in anchors:
     lc=anchors[cid].get('live_code',{})
     for k in ('allowed_syntax','blocked_syntax'):
      assert ni['public']['constraints'][k]==lc[k],(cid,k)
p.write_text(json.dumps(d,indent=2)+'\n')
(b/'04_repair_named_gate_changes.json').write_text(json.dumps({'changed':changes,'counts':{typ:sum(e['interaction']['type']==typ for t in d['tiles'] for e in t['interactions']) for typ in sorted({e['interaction']['type'] for t in d['tiles'] for e in t['interactions']})},'constraints_and_tests_unchanged':True,'unrelated_interactions_unchanged':True},indent=2)+'\n')
print('Patched',len(changes),'interactions')
