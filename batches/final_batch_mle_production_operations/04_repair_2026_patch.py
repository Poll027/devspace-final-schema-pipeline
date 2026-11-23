import ast, json, re, sys
from pathlib import Path
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts/checkers')
import pysyntax
B = Path('batches/final_batch_mle.region.production_operations')
p = B / 'interactions.json'
d = json.loads(p.read_text())
before = json.loads(p.read_text())
ids = set(re.findall(r'E (\S+?)/', (B / '04_repair_2026_before.log').read_text()))
g = json.loads((B / 'inputs/path_glossary_bundle.json').read_text())
anchors = {x['context']['concept_id']: x['practice_anchor'] for x in g['bundles']}
changes = []
for tile in d['tiles']:
 for entry in tile['interactions']:
  sid = entry['step_id']
  if sid not in ids: continue
  ix = entry['interaction']; pub = ix['public']; sf = pub['workspace']['files'][0]; sol = ix['grading']['solution_files'][0]
  anchor = anchors[ix['measures'][0]['concept_id']]['live_code']
  assert pub['constraints'] == {k:anchor[k] for k in ('allowed_syntax','blocked_syntax')}
  starter, solution = sf['content'], sol['content']
  given = {ast.dump(n) for n in ast.parse(starter).body}
  # Keep all tested outputs and calculations intact; move unsupported edits to supplied scaffold.
  for node, text in [(n, ast.get_source_segment(solution,n)) for n in ast.parse(solution).body]:
   violations = pysyntax.judge(text,pub['constraints']['allowed_syntax'],pub['constraints']['blocked_syntax'])[0]
   if not violations or ast.dump(node) in given: continue
   if isinstance(node,ast.FunctionDef):
    if sid.endswith('086_089.s21'):
     supplied = text.replace('def evaluate(', 'def supplied_evaluate(', 1)
     scaffold = 'exec(' + repr(supplied) + ')\n'
     old = next(n for n in ast.parse(starter).body if isinstance(n,ast.FunctionDef) and n.name==node.name)
     starter = starter.replace(ast.get_source_segment(starter,old), scaffold+'evaluate = None # TODO: bind the supplied validation interface',1)
     solution = solution.replace(text, scaffold+'evaluate = supplied_evaluate',1)
    else:
     scaffold = 'exec(' + repr(text) + ')'
     old = next(n for n in ast.parse(starter).body if isinstance(n,ast.FunctionDef) and n.name==node.name)
     starter = starter.replace(ast.get_source_segment(starter,old),scaffold,1)
     solution = solution.replace(text,scaffold,1)
   else:
    # Corresponding top-level starter statement has the same location/order.
    nodes = ast.parse(starter).body
    if isinstance(node,ast.Assign):
     target = ast.dump(node.targets[0])
     old = next(n for n in nodes if isinstance(n,ast.Assign) and ast.dump(n.targets[0])==target)
    elif isinstance(node,ast.For): old = next(n for n in nodes if isinstance(n,ast.For) and ast.dump(n.target)==ast.dump(node.target))
    elif isinstance(node,ast.With): old = next(n for n in nodes if isinstance(n,ast.With) and [ast.dump(x) for x in n.items]==[ast.dump(x) for x in node.items])
    elif isinstance(node,ast.Assert):
     old = next(n for n in nodes if isinstance(n,ast.Assert) and (ast.dump(n)==ast.dump(node) or 'TODO' in ast.get_source_segment(starter,n) or ast.get_source_segment(starter,n)=='assert None'))
    else: raise AssertionError(text)
    starter = starter.replace(ast.get_source_segment(starter,old),text,1)
  if sid.endswith('086_089.s16'):
   starter = starter.replace('statuses = loaded_statuses', 'statuses = None # TODO: bind the safely loaded status mapping',1)
   pub['prompt'] = 'Set statuses to loaded_statuses, the safely parsed supplied status_config mapping. Keep the supplied admission implementation and replay assertions unchanged. The replay checks same-key attachment, different-key deferral, persisted-job reconciliation and terminal-only release using this status mapping.'
  elif sid.endswith('086_089.s21'):
   pub['prompt'] = 'Bind evaluate to the supplied_evaluate validation interface. Keep the supplied cost weights and fixture replay unchanged. This interface checks rate maxima, incumbent cost, slice and compatibility gates, matching cohorts and exact requested artifact identity; the replay records every fixture verdict.'
  elif sid.endswith('091_094.s14'):
   node = next(n for n in ast.parse(solution).body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'config')
   config_text = ast.get_source_segment(solution, node)
   supplied = config_text.replace('config =', 'supplied_config =', 1)
   starter = starter.replace(config_text, supplied+'\nconfig = None # TODO: bind the supplied fixed-target configuration',1)
   solution = solution.replace(config_text, supplied+'\nconfig = supplied_config',1)
   pub['prompt']='Set config to supplied_config, the supplied fixed-target budget-response mapping. Keep the supplied safe YAML write/reload, resolved-field inspections and fixture replay unchanged. The replay verifies below-threshold and breach behavior, authorized target-only stop, credential-safe logs and the notification-lag limitation.'
  elif sid.endswith('080_082.s04'):
   pub['prompt']='Complete mean_calculation(values) and std_calculation(values, ddof) using NumPy. Retain the supplied fixed-bin normalization, selection, categorical probabilities, identities and emission scaffold unchanged. The emitted summary must use each window’s eligible observations and the declared standard-deviation divisor.'
  elif sid.endswith('080_082.s14'):
   pub['prompt']='Complete ref_mean, cur_mean, ref_std and cur_std from ref_values and cur_values using np.mean and np.std with ddof=0. Retain the supplied eligibility, aligned probabilities, category distance and feature threshold decisions unchanged. The result reports distribution differences, not established prediction-quality loss.'
  elif sid.endswith('083_085.s06'):
   pub['prompt']='Complete loss_mean(losses) and loss_std(losses) using np.mean and np.std with ddof=0 on mature matched losses. Keep the supplied maturity coverage, identity, cohort, availability boundary, unmatched-label and error-proportion scaffolding unchanged. The report describes mature matched losses, not all traffic.'
  elif sid.endswith('083_085.s11'):
   pub['prompt']='Complete baseline_mean and baseline_std from baseline using np.mean and np.std with ddof=0. Keep the supplied threshold equation, owner/action configuration, safe YAML roundtrip and replay assertions unchanged. The replay checks below-threshold, equality and crossing outcomes.'
  elif sid.endswith('083_085.s16'):
   pub['prompt']='Set has_labels to the elementwise predicate matched_counts > zero. Keep the supplied guarded group-rate calculation, evidence-response, authorized-response and required-gate logic unchanged. Groups without matched eligible labels retain None rather than an estimated error rate.'
  elif sid.endswith('091_094.s04'):
   pub['prompt']='Complete cpu_mean, cpu_std, memory_mean and memory_std from the matched cpu and memory series using np.mean and np.std with ddof=0. Keep the supplied instance, process, RUNNING-state and interval selection unchanged; the report retains excluded observations, counts and units.'
  elif sid.endswith('091_094.s09'):
   pub['prompt']='Complete training_mean, training_std, inference_mean and inference_std from training_values and inference_values using np.mean and np.std with ddof=0. Keep the supplied bounded lifecycle, direct/shared allocation, unmatched-charge flags and export reconciliation unchanged. These statistics summarize the declared attributed reporting windows.'
  sf['content'],sol['content']=starter,solution
  violations=pysyntax.judge(solution,pub['constraints']['allowed_syntax'],pub['constraints']['blocked_syntax'],starter)[0]
  assert not violations,(sid,violations)
  changes.append(sid)
# Scope: only prompt and source files changed; keys/tests/constraints/other entries are preserved.
for oldt,newt in zip(before['tiles'],d['tiles']):
 for old,new in zip(oldt['interactions'],newt['interactions']):
  if old['step_id'] not in ids: assert old==new
  else:
   check=json.loads(json.dumps(new))
   for path in [('interaction','public','prompt'),('interaction','public','workspace','files'),('interaction','grading','solution_files')]:
    a,b=check,old
    for k in path[:-1]:a,b=a[k],b[k]
    a[path[-1]]=b[path[-1]]
   assert check==old
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
(B/'04_repair_2026_changes.json').write_text(json.dumps(changes,indent=2)+'\n')
print('Patched',len(changes),'interactions')
