import ast, copy, json, re, sys
from pathlib import Path
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts/checkers')
from pysyntax import judge
B=Path('batches/final_batch_mle.region.production_operations')
p=B/'interactions.json'; doc=json.loads(p.read_text()); before=copy.deepcopy(doc)
findings=(B/'04_round_target_strict.log').read_text()
ids=set(re.findall(r'^  E (\S+?)/.*solution uses ', findings, re.M))
bundles={x['context']['concept_id']:x for x in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}
changes=[]
for tile in doc['tiles']:
 for entry in tile['interactions']:
  sid=entry['step_id']
  if sid not in ids: continue
  ix=entry['interaction']; pub=ix['public']; gr=ix['grading']; code=gr['solution_files'][0]['content']
  cid=ix['anchors'][0].split('#')[0]
  assert pub['constraints']=={k:bundles[cid]['practice_anchor']['live_code'][k] for k in ('allowed_syntax','blocked_syntax')}
  chunks=[ast.get_source_segment(code,n) for n in ast.parse(code).body]
  pre=[]; edits={}; instructions=''
  if sid.endswith('080_082.s04'):
   pre=['summary_mean = None','summary_std = None']; edits={'summary_mean = None':'summary_mean = np.mean','summary_std = None':'summary_std = np.std'}
   chunks=[c.replace('np.mean(values)', 'summary_mean(values)').replace('np.std(values, ddof=0)', 'summary_std(values, ddof=0)') if c.startswith('def summarize(') else c for c in chunks]
   instructions='Complete the two statistic bindings: bind summary_mean to NumPy’s arithmetic-mean function and summary_std to NumPy’s standard-deviation function. The supplied summary scaffolding selects eligible observations, uses fixed edges and each window’s own totals, calls the bound functions with ddof=0, and emits one record. Keep that scaffolding unchanged. The checker reads records, including the window/reference identity, definitions, totals, proportions, means and standard deviations.'
  elif sid.endswith('080_082.s14'):
   for c in chunks:
    if any(c.startswith(n+' = ') for n in ('ref_mean','cur_mean','ref_std','cur_std')): edits[c]=c
   instructions='Complete ref_mean, cur_mean, ref_std and cur_std using np.mean and np.std on ref_values and cur_values respectively, with ddof=0 for both standard deviations. Leave the supplied normalization, distance and threshold scaffolding unchanged. The checker reads these four statistics and the category/numeric distances and drift decisions produced from them.'
  elif sid.endswith('083_085.s06'):
   pre=['loss_mean_function = None','loss_std_function = None']; edits={'loss_mean_function = None':'loss_mean_function = np.mean','loss_std_function = None':'loss_std_function = np.std'}
   chunks=[c.replace('np.mean(losses)', 'loss_mean_function(losses)').replace('np.std(losses, ddof=0)', 'loss_std_function(losses, ddof=0)') if c.startswith('def quality(') else c for c in chunks]
   instructions='Bind loss_mean_function to NumPy’s arithmetic-mean function and loss_std_function to NumPy’s standard-deviation function. The supplied cohort scaffolding rejects duplicate IDs, joins only available mature-cohort labels, preserves eligible/mature counts and coverage, and handles unavailable labels. It calls your statistic bindings on mature losses with ddof=0. Keep that scaffolding unchanged; the checker reads the complete quality records, including matched error proportion and mature-loss statistics.'
  elif sid.endswith('083_085.s16'):
   original=next(n.value for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Constant) and n.value=='approved_rollback')
   pre=['approved_rollback_response = '+repr(original),'rollback_response = None']; edits={'rollback_response = None':'rollback_response = approved_rollback_response'}
   chunks=[c.replace("response = 'approved_rollback'",'response = rollback_response') for c in chunks]
   instructions='The supplied diagnostic scaffolding calculates each group’s matched-label error rate and checks the configuration-mismatch replay evidence without executing recovery. Complete rollback_response by assigning the supplied approved_rollback_response value. It is used only when the stated evidence supports approved rollback; other cases retain their supplied responses. Keep the evidence checks and required readiness/bounded-prediction gates unchanged. The checker reads result in the supplied diagnostic-record schema.'
  elif sid.endswith('086_089.s16'):
   original=next(n.value for n in ast.walk(ast.parse(code)) if isinstance(n,ast.Constant) and n.value=='defer')
   pre=['deferred_response = '+repr(original),'busy_response = None']; edits={'busy_response = None':'busy_response = deferred_response'}
   chunks=[c.replace("'status': 'defer'", "'status': busy_response") if c.startswith('def admit(') else c for c in chunks]
   instructions='Complete busy_response by assigning the supplied deferred_response value, so a busy admission defers instead of launching another job. Keep the supplied atomic-admission, persisted-identity reconciliation, completed-claim and terminal-release scaffolding and concurrency/restart assertions unchanged. The checker reads the admission fixture results, including deferred busy claims, duplicate/restart identity reuse and release only after terminal confirmation.'
  elif sid.endswith('086_089.s21'):
   pre=["required_cohort = policy['cohort']",'validation_cohort = None']; edits={'validation_cohort = None':'validation_cohort = required_cohort'}
   chunks=[c.replace("candidate['cohort_id'] == policy['cohort']", "candidate['cohort_id'] == validation_cohort") if c.startswith('def evaluate(') else c for c in chunks]
   instructions='Complete validation_cohort by assigning required_cohort, the cohort supplied by the validation policy. The supplied validation scaffold calculates incumbent/candidate FPR, FNR and expected cost, handles empty conditioning groups, applies quality/slice/compatibility gates and binds the requested artifact identity. Keep those calculations and the passing/failing fixture assertions unchanged. The checker reads result and requires cohort identity binding as well as every other declared gate.'
  elif sid.endswith('091_094.s09'):
   for c in chunks:
    if any(c.startswith(n+' = ') for n in ('training_mean','training_std','inference_mean','inference_std')): edits[c]=c
   instructions='Complete training_mean, training_std, inference_mean and inference_std using np.mean and np.std on training_values and inference_values respectively. Use ddof=0 for both standard deviations. Keep the supplied authorized lifecycle simulation, allocation rules, shared/unmatched-charge handling, unusual-allocation flags and reconciliation scaffolding unchanged. The checker reads the four statistics and the complete per-window workload summaries and lifecycle records.'
  elif sid.endswith('091_094.s14'):
   pre=["approved_instance = policy['INSTANCE']", "approved_zone = policy['ZONE']",'target_instance = None','target_zone = None']; edits={'target_instance = None':'target_instance = approved_instance','target_zone = None':'target_zone = approved_zone'}
   chunks=[c.replace("'INSTANCE': policy['INSTANCE']", "'INSTANCE': target_instance").replace("'ZONE': policy['ZONE']", "'ZONE': target_zone") if c.startswith('config = ') else c for c in chunks]
   instructions='Complete target_instance and target_zone by assigning the supplied approved_instance and approved_zone values. These bindings set the fixed approved nonproduction target in the supplied budget-response configuration. Keep the supplied safe YAML writing/reloading, scope/threshold/event binding, runtime secret references, field inspection and fixture replay scaffolding unchanged. The checker reads result: resolved configuration, below/breach notification behavior, authorized target-only stop, before/after descriptions, credential-safe output and the notification-lag limitation.'
  else: raise RuntimeError(sid)
  # Supplied functions are readable multiline scaffolding, identical in starter and solution.
  chunks=[('exec('+repr(c)+')') if c.startswith('def ') else c for c in chunks]
  base=pre+chunks
  solution=[]; starter=[]
  for c in base:
   if c in edits:
    solved=edits[c]; solution.append('# Learner binding/calculation\n'+solved)
    if c==solved:
     name=ast.parse(c).body[0].targets[0].id
     starter.append('# TODO: compute '+name+' as specified in the prompt.\n'+name+' = None')
    else: starter.append('# TODO: complete this binding as specified in the prompt.\n'+c)
   else:
    solution.append(c); starter.append(c)
  sol='\n\n'.join(solution)+'\n'; st='\n\n'.join(starter)+'\n'
  violations,_,_=judge(sol, **{'allowed':pub['constraints']['allowed_syntax'],'blocked':pub['constraints']['blocked_syntax']}, starter=st)
  assert not violations,(sid,violations)
  pub['workspace']['files'][0]['content']=st; gr['solution_files'][0]['content']=sol; pub['prompt']=instructions
  changes.append({'step_id':sid,'learner_edits':len(edits),'constraints_unchanged':True,'tests_unchanged':True})
assert len(changes)==len(ids)
# No interaction other than the gate-named ones, no answer keys or constraints, is changed.
for ot,nt in zip(before['tiles'],doc['tiles']):
 for old,new in zip(ot['interactions'],nt['interactions']):
  if old['step_id'] not in ids: assert old==new
  else:
   assert old['interaction']['grading']['tests']==new['interaction']['grading']['tests']
   assert old['interaction']['public']['constraints']==new['interaction']['public']['constraints']
p.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
(B/'04_targeted_syntax_changes.json').write_text(json.dumps(changes,indent=2)+'\n')
print(json.dumps({'changed':len(changes),'interactions':sum(len(t['interactions']) for t in doc['tiles'])}))
