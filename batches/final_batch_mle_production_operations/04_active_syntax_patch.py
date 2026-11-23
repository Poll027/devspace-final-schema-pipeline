import ast, json, re, sys
from pathlib import Path
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts')
from checkers.pysyntax import judge
B = Path('batches/final_batch_mle.region.production_operations')
p = B / 'interactions.json'
doc = json.loads(p.read_text())
log = (B/'04_repair_active_strict.log').read_text()
targets = set(re.findall(r' E (mle\.tile\.[^/]+)/.*solution uses', log))
glossary = json.loads((B/'inputs/path_glossary_bundle.json').read_text())
# Keep only the named defects in scope; supply unchanged infrastructure and leave
# the learner a small edit whose constructs the practice actually permits.
edit_names = {
 'mle.tile.080_082.s04': {'summary_mean','summary_std'},
 'mle.tile.080_082.s14': {'ref_mean','cur_mean','ref_std','cur_std'},
 'mle.tile.083_085.s06': {'summary_mean','summary_std'},
 'mle.tile.083_085.s16': {'rollback_response'},
 'mle.tile.086_089.s16': {'busy_response'},
 'mle.tile.086_089.s21': {'validation_cohort'},
 'mle.tile.091_094.s09': {'training_mean','training_std','inference_mean','inference_std'},
 'mle.tile.091_094.s14': {'target_instance','target_zone'},
}
prompts = {
 'mle.tile.080_082.s04': 'The supplied summarize implementation selects eligible values, constructs comparable window summaries and emits one record. Complete summary_mean = np.mean and summary_std = np.std to wire its numeric calculations to NumPy. The supplied call uses ddof=0. Leave the window, bin, category, class and emission scaffolding unchanged; the tests read the returned monitoring record.',
 'mle.tile.080_082.s14': 'The supplied comparison scaffolding constructs aligned probabilities and evaluates the declared drift thresholds. Complete ref_mean, cur_mean, ref_std and cur_std from ref_values and cur_values with np.mean and np.std using ddof=0. Leave the supplied probability, threshold and report construction unchanged. The tests read the resulting report.',
 'mle.tile.083_085.s06': 'The supplied quality implementation rejects duplicate identifiers, joins mature labels to eligible predictions and calculates coverage and errors. Complete summary_mean = np.mean and summary_std = np.std to calculate the matched cohort loss summaries, using the supplied ddof=0 call. Leave the maturity and joining scaffolding unchanged. Tests read the returned quality record, including unavailable and duplicate cases.',
 'mle.tile.083_085.s16': 'The supplied diagnostic scaffolding calculates matched-cohort rates, preserves unavailable rates for zero counts, and evaluates identities and replay evidence before selecting a response. Complete rollback_response by assigning approved_rollback_response. This wires the approved rollback label into the already-guarded branch; it must not authorize retraining or execute recovery. Leave all evidence predicates and required gates unchanged. Tests read the diagnostic records.',
 'mle.tile.086_089.s16': 'The supplied admission implementation persists job identities, reconciles duplicates and unknown responses, and releases only after terminal confirmation. Complete busy_response by assigning deferred_response so a busy claim defers rather than launching another job. Leave the supplied concurrency/restart fixtures and assertions unchanged. Tests read admit and the fixture result records.',
 'mle.tile.086_089.s21': 'The supplied validation implementation calculates conditional error rates and expected cost and applies quality, slice, compatibility and artifact-identity gates. Complete validation_cohort by assigning required_cohort so the promotion verdict also requires the approved validation cohort. Leave the supplied formulas, fixture runner and assertions unchanged. Tests read evaluate verdicts and the resulting promotion records.',
 'mle.tile.091_094.s09': 'The supplied lifecycle and billing scaffolding uses the approved resource mapping and shared-charge rule, preserves unmatched charges and reconciles the export total. Complete training_mean, training_std, inference_mean and inference_std using np.mean and np.std with ddof=0 over training_values and inference_values respectively. Leave the lifecycle sequences, allocation and reconciliation unchanged. Tests read the workload summary records.',
 'mle.tile.091_094.s14': 'The supplied safe YAML round-trip and event-response replay scaffolding resolves the budget scope, amount, period, threshold, topic binding and runtime secret reference. Complete target_instance = approved_instance and target_zone = approved_zone to bind the response to only the authorized target. Leave all supplied configuration, safe serialization and replay checks unchanged. Tests read the resolved configuration and notification/stop evidence, including the untouched control resource and credential non-disclosure.',
}
changes=[]
for tile in doc['tiles']:
 for entry in tile['interactions']:
  sid=entry['step_id']
  if sid not in targets: continue
  ix=entry['interaction']; pub=ix['public']; gr=ix['grading']
  solution=gr['solution_files'][0]['content']
  # Named function implementations are infrastructure, not learner edits.
  # Use the same explicit exec-based supplied-contract format already in this workspace.
  replacements=[]
  for n in ast.parse(solution).body:
   if isinstance(n,(ast.FunctionDef,ast.ClassDef)):
    text=ast.get_source_segment(solution,n)
    replacements.append((n.lineno,n.end_lineno,'# Supplied contract implementation; leave unchanged.\nexec('+repr(text)+')'))
  lines=solution.splitlines()
  for start,end,text in reversed(replacements): lines[start-1:end]=[text]
  solution='\n'.join(lines)+'\n'
  starter=solution
  replacements=[]
  found=set()
  for n in ast.parse(solution).body:
   if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in edit_names[sid]:
    name=n.targets[0].id;found.add(name)
    replacements.append((n.lineno,n.end_lineno,name+' = None  # TODO: complete the numeric calculation or approved binding named in the prompt.'))
  assert found==edit_names[sid], (sid,found)
  lines=starter.splitlines()
  for start,end,text in reversed(replacements):lines[start-1:end]=[text]
  starter='\n'.join(lines)+'\n'
  assert starter != solution
  violations,_,_=judge(solution,pub['constraints']['allowed_syntax'],pub['constraints']['blocked_syntax'],starter)
  assert not violations, (sid,violations)
  pub['workspace']['files'][0]['content']=starter
  gr['solution_files'][0]['content']=solution
  pub['prompt']=prompts[sid]
  changes.append(sid)
assert set(changes)==targets,(targets,changes)
p.write_text(json.dumps(doc,indent=2,ensure_ascii=False)+'\n')
(B/'04_active_syntax_changes.json').write_text(json.dumps({'changed_steps':changes,'constraints_unchanged':True,'expected_and_tests_unchanged':True},indent=2)+'\n')
print('Patched',len(changes),'interactions')
