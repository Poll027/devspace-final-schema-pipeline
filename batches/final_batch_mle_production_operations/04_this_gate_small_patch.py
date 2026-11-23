import ast,json,re,copy
from pathlib import Path
b=Path('batches/final_batch_mle.region.production_operations')
p=b/'interactions.json';d=json.loads(p.read_text());before=copy.deepcopy(d)
ids=set(re.findall(r'^  E ([^/]+)',(b/'04_repair_current_gate_validate.log').read_text(),re.M))
# Read plan, screen and registry metadata without touching those artifacts.
plan=json.loads((b/'tile_plans.json').read_text());screens=json.loads((b/'screens.json').read_text());registry=json.loads((b/'scenario_asset_registry.json').read_text());gloss=json.loads((b/'inputs/path_glossary_bundle.json').read_text())
changes=[]
for tile in d['tiles']:
 for entry in tile['interactions']:
  sid=entry['step_id']
  if sid not in ids:continue
  ix=entry['interaction'];sol=ix['grading']['solution_files'][0]['content']; nodes=ast.parse(sol).body
  segments=[ast.get_source_segment(sol,n) for n in nodes]; edit={}; prompt=''
  if sid.endswith('083_085.s11'):
   edit={n.lineno:'None' for n in nodes if isinstance(n,ast.Assign) and getattr(n.targets[0],'id','') in ['baseline_mean','baseline_std']}
   prompt='Complete baseline_mean = np.mean(baseline) and baseline_std using np.std with the declared N divisor (ddof=0). The supplied policy configuration, safe YAML round-trip and replay assertions then verify normal, boundary and breached windows and the configured owner/action. Leave that scaffolding unchanged.'
  elif sid.endswith('083_085.s16'):
   # The learner supplies the nonzero-denominator predicate; existing diagnostics are scaffolding.
   pos=next(k for k,n in enumerate(nodes) if isinstance(n,ast.Assign) and getattr(n.targets[0],'id','')=='selected_rates')
   segments.insert(pos,'zero = 0\n\nhas_labels = matched_counts > zero');nodes.insert(pos,None)
   for k,s in enumerate(segments):
    if s.startswith('for group in rate_groups:'):segments[k]=s.replace('if matched_counts[group] > 0:', 'if has_labels[group]:')
   prompt='Complete has_labels as the Boolean array matched_counts > zero. This predicate must exclude zero eligible-label denominators. Leave the supplied guarded rate calculation and evidence-supported diagnostic/rollback selection unchanged; they retain readiness and bounded_prediction gates and are verified by the replay tests.'
  elif sid.endswith('086_089.s16'):
   k=next(k for k,n in enumerate(nodes) if isinstance(n,ast.FunctionDef) and n.name=='admit')
   fn=segments[k].replace('def admit(', 'def persisted_admission(',1)
   segments[k]='exec('+repr(fn)+')\n\nadmit = persisted_admission'
   nodes[k]=None
   prompt='Set admit to the supplied persisted_admission callable (assign the callable itself, without calling it). Its displayed implementation atomically reserves the run key and pipeline slot, defers busy claims, reconciles the persisted job identity and releases only confirmed terminal jobs. Leave the implementation and concurrency/restart assertions unchanged. The fixture tests verify those behaviours.'
  elif sid.endswith('086_089.s21'):
   for k,n in enumerate(nodes):
    if isinstance(n,ast.FunctionDef):
     fn=segments[k]
     if n.name=='evaluate':fn=fn.replace('def evaluate(', 'def evaluate_candidate(',1)
     segments[k]='exec('+repr(fn)+')';nodes[k]=None
   k=next(k for k,s in enumerate(segments) if s.startswith('exec(') and 'def evaluate_candidate' in s)
   segments[k]+='\n\nevaluate = evaluate_candidate'
   prompt='Set evaluate to the supplied evaluate_candidate callable (assign it without calling it). Leave the supplied rate/cost implementation and fixture assertions unchanged. It guards undefined class denominators and checks the policy thresholds, expected cost, slices, compatibility, cohort and exact candidate identity; the valid, boundary and unrelated-identity replays verify the verdicts.'
  elif sid.endswith('091_094.s04'):
   edit={n.lineno:'None' for n in nodes if isinstance(n,ast.Assign) and getattr(n.targets[0],'id','') in ['cpu_mean','cpu_std','memory_mean','memory_std']}
   prompt='Using the supplied fixed-instance/process/running-interval mask and selected cpu and memory arrays, complete cpu_mean, cpu_std, memory_mean and memory_std with np.mean and np.std(..., ddof=0). Leave the selection scaffolding unchanged; do not mix CPU and memory series.'
  elif sid.endswith('091_094.s09'):
   edit={n.lineno:'None' for n in nodes if isinstance(n,ast.Assign) and getattr(n.targets[0],'id','') in ['training_mean','training_std','inference_mean','inference_std']}
   prompt='Complete training_mean, training_std, inference_mean and inference_std from the corresponding supplied training_values and inference_values arrays, using np.mean and np.std(..., ddof=0). Leave lifecycle sequences, direct/shared/unmatched charge allocation, summaries and reconciliation scaffolding unchanged. Do not mix workloads.'
  elif sid.endswith('091_094.s14'):
   k=next(k for k,n in enumerate(nodes) if isinstance(n,ast.Assign) and getattr(n.targets[0],'id','')=='config')
   segments[k]=segments[k].replace('config = ', 'declared_config = ',1)+'\n\nconfig = declared_config';nodes[k]=None
   prompt='Set config to the supplied declared_config mapping. Leave the fixed-target event binding, runtime secret references, safe YAML round-trip and response replays unchanged. The supplied below/boundary/breach fixtures verify notification, authorized target-only stop, credential non-disclosure and the recorded limitation that notifications are not a hard spending cap.'
  starter=[]
  for n,s in zip(nodes,segments):
   if n is not None and n.lineno in edit:
    s=ast.unparse(n.targets[0])+' = '+edit[n.lineno]+' # TODO: complete the calculation'
   elif sid.endswith('083_085.s16') and 'has_labels = matched_counts > zero' in s:s=s.replace('has_labels = matched_counts > zero','has_labels = None # TODO: nonzero-denominator mask')
   elif sid.endswith('086_089.s16') and s.endswith('admit = persisted_admission'):s=s[:-len('admit = persisted_admission')]+'admit = None # TODO: select the supplied admission callable'
   elif sid.endswith('086_089.s21') and s.endswith('evaluate = evaluate_candidate'):s=s[:-len('evaluate = evaluate_candidate')]+'evaluate = None # TODO: select the supplied validation callable'
   elif sid.endswith('091_094.s14') and s.endswith('config = declared_config'):s=s[:-len('config = declared_config')]+'config = None # TODO: select the declared mapping'
   starter.append(s)
  ix['grading']['solution_files'][0]['content']='\n\n'.join(segments)+'\n'
  ix['public']['workspace']['files'][0]['content']='\n\n'.join(starter)+'\n'
  ix['public']['prompt']=prompt
  assert ix['public']['constraints']==next(e['interaction']['public']['constraints'] for t in before['tiles'] for e in t['interactions'] if e['step_id']==sid)
  changes.append(sid)
p.write_text(json.dumps(d,indent=2)+'\n')
(b/'04_this_gate_patch_counts.json').write_text(json.dumps({'changed':changes,'counts':{typ:sum(e['interaction']['type']==typ for t in d['tiles'] for e in t['interactions']) for typ in sorted({e['interaction']['type'] for t in d['tiles'] for e in t['interactions']})}},indent=2)+'\n')
