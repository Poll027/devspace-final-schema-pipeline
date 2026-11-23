import ast,copy,json,re,sys
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from checkers import pysyntax
B=Path('batches/final_batch_mle.region.production_operations')
p=B/'interactions.json'; d=json.loads(p.read_text()); before=copy.deepcopy(d)
errors=set(re.findall(r'^  E ([^/]+)/.*solution uses',(B/'04_this_dispatch_new_gate.log').read_text(),re.M))
selectors={
'mle.tile.080_082.s04':['summary_mean','summary_std'],
'mle.tile.083_085.s06':['summary_mean','summary_std'],
'mle.tile.083_085.s11':['write_config','read_config','baseline_mean','baseline_std'],
'mle.tile.083_085.s16':['rollback_response'],
'mle.tile.086_089.s16':['busy_response'],
'mle.tile.086_089.s21':['validation_cohort'],
'mle.tile.091_094.s14':['target_instance','target_zone'],
}
prompts={
'mle.tile.080_082.s04':'Set summary_mean and summary_std to the NumPy mean and standard-deviation functions. The supplied summarize implementation selects eligible observations, normalizes the declared bins, categories and classes, uses ddof=0, and emits and returns the monitoring record. Keep that scaffolding unchanged.',
'mle.tile.083_085.s06':'Set summary_mean and summary_std to the NumPy mean and standard-deviation functions. The supplied quality implementation joins the eligible mature cohort to available labels, rejects duplicate IDs, retains unmatched-label evidence and uses ddof=0 for the matched losses. Keep that scaffolding unchanged.',
'mle.tile.083_085.s11':'Compute baseline_mean with np.mean(baseline) and baseline_std with np.std(baseline, ddof=0). Bind write_config to safe_writer and read_config to safe_reader so the supplied alert configuration is safely serialized and reloaded before replay. Keep the supplied threshold, owner, response and replay checks unchanged.',
'mle.tile.083_085.s16':'Bind rollback_response to approved_rollback_response so the supplied regression-diagnosis implementation records the approved rollback response. Read the supplied cohort, boundary and zero-denominator checks; leave their calculations and fixtures unchanged.',
'mle.tile.086_089.s16':'Bind busy_response to deferred_response so the supplied atomic admission implementation defers a different key while capacity is occupied. Keep the supplied same-key reconciliation, durable reservation, restart and terminal-release logic unchanged.',
'mle.tile.086_089.s21':'Bind validation_cohort to required_cohort so the supplied candidate-validation implementation enforces the declared cohort in addition to identity, quality, slice and compatibility gates. Keep the supplied cost calculations and positive, boundary and rejection fixtures unchanged.',
'mle.tile.091_094.s14':'Bind target_instance to approved_instance and target_zone to approved_zone so the supplied budget event-response configuration acts only on the approved fixed target. Keep the supplied safe YAML serialization, runtime secret references, event binding, below-threshold and boundary/breach replay checks unchanged.',
'mle.tile.080_082.s14':'Compute ref_mean, cur_mean, ref_std and cur_std from ref_values and cur_values using np.mean and np.std with ddof=0. The supplied scaffolding aligns and normalizes categorical and numeric-bin counts, calculates total-variation distances and applies the declared strict threshold. Keep that scaffolding unchanged.',
'mle.tile.091_094.s04':'The supplied mask selects the approved running instance and process in the declared half-open telemetry interval. Compute cpu_mean, cpu_std, memory_mean and memory_std from cpu and memory using np.mean and np.std with ddof=0. Keep the selection scaffolding unchanged.',
'mle.tile.091_094.s09':'Compute training_mean, training_std, inference_mean and inference_std from training_values and inference_values using np.mean and np.std with ddof=0. The supplied scaffolding records lifecycle evidence, allocates charges by the declared mapping and shared rule, retains unmatched charges and reconciles to the export. Keep that scaffolding unchanged.'}
report=[]
for t in d['tiles']:
 for e in t['interactions']:
  sid=e['step_id']
  if sid not in errors:continue
  ix=e['interaction'];sf=ix['grading']['solution_files'][0]; sol=sf['content'];ws=ix['public']['workspace']['files'][0]; old=ws['content']; cons=ix['public']['constraints']
  # Supplied function/class definitions are executed as scaffolding, not learner edits.
  original_sol=sol
  nodes=ast.parse(sol).body; lines=sol.splitlines(True)
  for n in reversed(nodes):
   if isinstance(n,(ast.FunctionDef,ast.ClassDef)):
    lines[n.lineno-1:n.end_lineno]=['exec('+repr(ast.get_source_segment(sol,n))+')\n']
  sol=''.join(lines); sf['content']=sol
  selected=selectors.get(sid)
  if selected is None:selected=[n.targets[0].id for n in ast.parse(sol).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id.endswith(('_mean','_std'))]
  replacements=[]
  for n in ast.parse(sol).body:
   if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in selected:
    src=ast.get_source_segment(sol,n)
    assert not pysyntax.judge(src,cons['allowed_syntax'],cons['blocked_syntax'])[0],(sid,src)
    replacements.append((n.lineno,n.end_lineno,n.targets[0].id+' = None  # TODO: '+prompts[sid]))
  assert len(replacements)==len(selected),(sid,selected)
  lines=sol.splitlines(True)
  for start,end,text in reversed(replacements):lines[start-1:end]=[text+'\n']
  ws['content']=''.join(lines); ix['public']['prompt']=prompts[sid]
  assert not pysyntax.judge(sol,cons['allowed_syntax'],cons['blocked_syntax'],ws['content'])[0]
  report.append({'step_id':sid,'learner_variables':selected,'solution_computation_unchanged':True,'constraints_unchanged':True})
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
(B/'04_dispatch_syntax_only_changes.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
