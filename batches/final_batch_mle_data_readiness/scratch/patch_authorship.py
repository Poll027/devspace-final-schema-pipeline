import ast, copy, json
from pathlib import Path
B=Path('batches/final_batch_mle.region.data_readiness')
p=B/'interactions.json'; d=json.loads(p.read_text()); before=copy.deepcopy(d)
openings={
'001_003.s05': 'Write `import numpy as np`, implement `validate(fixture)`, and author the fixture checks below. Accept only rank-two arrays with one through three rows and exactly two features; check rank before indexing shape and raise ValueError for violations. Return the unchanged accepted array. Expose accepted, boundary, rank, shape, dtype, batch, width, rank_ok, batch_ok, width_ok, and the four named rejection booleans.',
'001_003.s10': 'Write the NumPy import and implement `compare(a, candidate_dtypes, tolerance, element_storage_budget)`. Cast each candidate from the unchanged reference, check every scalar difference, calculate size-times-itemsize and nbytes, and return the declared reports and justification. Set result and boundary_result using the supplied fixtures.',
'001_003.s16': 'Write the NumPy import and implement `transform(matrix, feature_references)`. Use array subtraction, independently build the two-feature list-comprehension reference, assert the intended shape, and check agreement with explicit rtol and atol. Return the array and expose result.',
'004_006.s11': 'Write the pandas import and implement `inspect_chunks(path, declared_types, array_budget, feature_count, element_width)`. Calculate the row limit, iterate typed CSV chunks while the file remains open, verify every matrix’s actual element bytes against nbytes and budget, and return the declared summary without retaining prior chunks.',
'004_006.s16': 'Write the NumPy import and implement `inspect(columns, numeric_values, ddof=0)`. Return all declared readiness fields, compute feature-wise means and standard deviations over rows using the supplied divisor, and report observed dtype and element bytes with the stated memory scope. Expose result and boundary_result.',
'007_008.s05': 'Write the pandas import and implement `validate(table, contract)`. Check exact columns, then declared dtypes, then inclusive distance bounds and permitted zones. Raise the specified ValueError message for the first violation and return unchanged valid input. Author assertions for every supplied fixture and expose verdicts and result.',
'007_008.s10': 'Implement `clean(records, policy)` without changing source records. Use an accepted-key set and the supplied policy dictionary to reject invalid distances and repeats, repair approved spellings, and report affected IDs in input order. Author valid, boundary, repair, rejection, repeat, and deliberately false assertion checks; expose result and valid_result.',
'009_011.s06': 'Write the NumPy import and calculate sample_shares, target_shares, and inclusion in zone-A then zone-B order using their respective denominators. Calculate mean and population std from numeric_values, and write the supported coverage limitation.',
'009_011.s11': 'Implement `audit(observations, labels, contract)`. Detect repeated IDs before dictionary replacement, align by ID, compute missing and orphan sets, and report invalid, misaligned, and unavailable IDs under the stated predicates. Return the specified fields and author assertions for valid, reordered, duplicate, missing, orphaned, invalid, misaligned, unavailable, and inclusive-cutoff fixtures.',
'009_011.s16': 'Implement `partition(records, scenario, training_groups, cutoff, evaluation_end)` for both declared scenarios. Preserve source order, calculate each partition’s target proportion, and author group-disjointness and time-inequality assertions, including cutoff equality and the supplied invalid assignment. Expose group_result and time_result.',
'012_015.s05': 'Write the NumPy import and implement `impute(X_train, X_validation, X_boundary, numeric_values)` using the supplied SimpleImputer interface. Fit training only, transform both held-out fixtures, compute observed-training mean and population std, and author the declared output/state and deliberately incorrect replacement assertions.',
'012_015.s11': 'Write the NumPy import and implement `scale(X_train, X_validation)` using the supplied StandardScaler interface. Fit training only, transform both inputs, calculate column means and population std, and author assertions for validation arithmetic, constant-feature scale 1, unchanged state, and the supplied wrong-output case.',
'012_015.s16': 'Implement `encode(X_train, known, unseen, missing, policy)` using the supplied OneHotEncoder interface. Fit once on training, build the zone mapping from categories_, transform all three cases without refitting, and author output, width, and mapping assertions for ignore, error, and missing-seen-at-fit fixtures.',
'016_017.s05': 'Implement `correct(training, held_out, permitted_features)` using the supplied trace interfaces. Project permitted fields, fit only projected training rows, transform and predict held-out inputs once, and author invariant checks applied to both leaked and corrected traces.',
'016_017.s11': 'Write the datetime import and implement `feature(records, prediction_time)`. Filter with a list comprehension using available_at <= prediction_time, initialize total=0, and accumulate only accepted values. Author assertions for the original result, later-record invariance, empty input, and exact-boundary inclusion; expose result and augmented_result.',
'018_018.s05': 'Implement `audit(identity, sample, permitted_fields)` using read_sample and dictionary membership checks. Return only original permitted values without printing restricted values. Set result, invoke use_secret to set secret_used without copying the credential, and author permitted-field and unauthorized-access assertions.'}
funcs=['validate','compare','transform','inspect_chunks','inspect','clean','audit','partition','impute','scale','encode','correct','feature','check_invariants']
imports={k for k in openings if k not in ['007_008.s10','009_011.s11','009_011.s16','012_015.s16','016_017.s05','018_018.s05']}
# Expressions are copied from the existing selected candidate, not newly authored answer keys.
class Inline(ast.NodeTransformer):
 def __init__(self,rule): self.rule=rule
 def visit_Call(self,n):
  self.generic_visit(n)
  if isinstance(n.func,ast.Name) and n.func.id=='selected_rule':
   mapping={a.arg:v for a,v in zip(self.rule.args.args,n.args)}
   class Names(ast.NodeTransformer):
    def visit_Name(self,q): return copy.deepcopy(mapping.get(q.id,q))
   return ast.copy_location(Names().visit(copy.deepcopy(self.rule.body)),n)
  return n

def exec_code(n):
 if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='exec': return ast.literal_eval(n.value.args[0])

def names(n): return [q.id for q in ast.walk(n) if isinstance(q,ast.Name) and isinstance(q.ctx,ast.Store)]

for t in d['tiles']:
 for x in t['interactions']:
  key=x['step_id'].removeprefix('mle.tile.'); i=x['interaction']
  if key=='000_000.s06':
   a,b=i['public']['prompt'].split('Readable output scaffold',1)
   lines=b.splitlines()
   fields=['prediction_unit','eligible_population','target_event','prediction_time','horizon','allowed_inputs','excluded_input']
   lines=[('- '+field+': [selected value]') if (field:=next((f for f in fields if line.startswith('- '+f+':')),None)) else line for line in lines]
   i['public']['prompt']=a+'Readable output scaffold'+'\n'.join(lines);continue
  if key not in openings:continue
  source=i['grading']['solution_files'][0]['content']; tree=ast.parse(source)
  rule_tree=ast.parse(exec_code(tree.body[0])); chosen=tree.body[1].value.id
  rule=next(q.value for q in rule_tree.body if q.targets[0].id==chosen)
  starter=[];solution=[];spec=[];output_names=[];after=False
  for n in tree.body[2:]:
   text=ast.get_source_segment(source,n); code=exec_code(n)
   if code is not None:
    sub=ast.parse(code)
    target=isinstance(sub.body[0],ast.FunctionDef) and sub.body[0].name in funcs
    if target:
     after=True
     transformed=Inline(rule).visit(sub); ast.fix_missing_locations(transformed)
     solution.append(ast.unparse(transformed))
     for f in sub.body:
      if isinstance(f,ast.FunctionDef):
       starter.append(ast.unparse(ast.fix_missing_locations(ast.FunctionDef(name=f.name,args=f.args,body=[ast.Pass()],decorator_list=[]))).replace('    pass','    # TODO: implement the required computation and checks.\n    pass'))
     for q in ast.walk(sub):
      if isinstance(q,ast.Return) and isinstance(q.value,ast.Dict):
       fields=[ast.literal_eval(k) for k in q.value.keys if isinstance(k,ast.Constant)]
       spec.append('Return fields: '+', '.join('`'+str(k)+'`' for k in fields)+'.')
      if isinstance(q,ast.Dict):
       for k,v in zip(q.keys,q.values):
        if isinstance(k,ast.Constant) and k.value in ['scope','axis_meanings']:
         try: spec.append('`'+k.value+'` must be '+repr(ast.literal_eval(v))+'.')
         except:pass
     continue
    # Teaching interfaces stay supplied, but requested learner imports must not be duplicated there.
    if key in imports and sub.body and isinstance(sub.body[0],(ast.Import,ast.ImportFrom)):
     sub.body=[q for q in sub.body if not isinstance(q,(ast.Import,ast.ImportFrom))]
     code=ast.unparse(sub)+'\n'; text='exec('+repr(code)+')'
    solution.append(text);starter.append(text);continue
   solution.append(ast.unparse(Inline(rule).visit(copy.deepcopy(n))))
   if isinstance(n,(ast.Import,ast.ImportFrom)) and key in imports:
    starter.append('# TODO: '+text);continue
   if key=='009_011.s06' and isinstance(n,ast.Assign) and any(v in ['sample_shares','target_shares','inclusion','mean','std','limitation'] for v in names(n)):
    starter.append('# TODO: calculate '+', '.join(names(n))+'.');output_names+=names(n);continue
   if after:
    # Keep execution bindings except the explicitly learner-written output assignments.
    fixed_bindings={'result','boundary_result','valid_result','group_result','time_result','ignore_result','error_result','seen_missing_result','augmented_result'}
    authored_bindings={'001_003.s05','001_003.s10','007_008.s05','018_018.s05'}
    if isinstance(n,ast.Assign) and (set(names(n))<=fixed_bindings and key not in authored_bindings):
     starter.append(text);output_names+=names(n);continue
    if isinstance(n,ast.Assign) and set(names(n))<= {'reordered_labels','boundary_records','leaked_traces'}:
     starter.append(text);continue
    output_names += names(n)
    if isinstance(n,ast.Assert):starter.append('# TODO: author the required fixture assertion.')
    elif isinstance(n,(ast.Try,ast.For)):
     flags=[z for z in names(n) if z.endswith('_caught') or z.endswith('_rejected')]
     starter.append('# TODO: author fixture checks'+ (' and expose '+', '.join(dict.fromkeys(flags)) if flags else '')+'.')
    elif isinstance(n,ast.Assign):starter.append('# TODO: set '+', '.join(names(n))+'.')
    else:starter.append('# TODO: apply the learner-authored invariant checks.')
   else: starter.append(text)
  if key=='001_003.s05':output_names+=['empty_rejected','flat_rejected','wrong_width_rejected','too_many_rejected']
  extra={
   '001_003.s10':'Reports are in candidate_dtypes order. Each report has dtype, count, itemsize, element_bytes, nbytes, preserved, accepted. A candidate is accepted only when every scalar difference is within tolerance and storage is within budget. choice is the last acceptable candidate in this ordering or "neither".',
   '007_008.s05':'ValueError messages are "columns", "dtype", "distance", and "zone", in that check order. verdicts maps each fixture name to "accepted" or its first error message; result is [the valid table, verdicts].',
   '007_008.s10':'Return [cleaned records, report]. Report entries have observation_id and action, with labels "rejected", "repaired", or "removed_repeat"; unchanged accepted rows have no report entry. Catch the deliberately false assertion and expose false_predicate_caught.',
   '009_011.s11':'Repeated IDs retain discovery order (observations before labels); invalid, misaligned and unavailable lists follow first-seen label order. missing and orphan are sets. Invalid labels fall outside label_values; misaligned timestamps differ from the corresponding observation; availability later than the inclusive cutoff is unavailable. case_results maps supplied case names to their audits.',
   '009_011.s16':'Both partitions are nonempty in the supplied fixtures. For group use training_groups; validation contains the other groups. For time, train timestamps are before cutoff and validation timestamps are at or after cutoff but before evaluation_end. Proportions are target sums divided by partition counts.',
   '016_017.s05':'Author check_invariants(traces) containing these required checks:\nassert traces["fit_rows"] == select(training, permitted_features)\nassert traces["transform_rows"] == [select(held_out, permitted_features)]\nassert traces["prediction_rows"] == [select(held_out, permitted_features)]\nApply the same checks to corrected and leaked traces, including each leaked input trace separately; expose leaked_fit_caught and leaked_inputs_caught.',
  }.get(key,'')
  # Preserve the original report labels directly from the source instead of guessing their spelling.
  if key=='007_008.s10':
   clean=next(ast.parse(exec_code(n)) for n in tree.body if exec_code(n) and exec_code(n).startswith('def clean('))
   actions=[v.value for q in ast.walk(clean) if isinstance(q,ast.Dict) for k,v in zip(q.keys,q.values) if isinstance(k,ast.Constant) and k.value=='action' and isinstance(v,ast.Constant)]
   extra='Return [cleaned records, report]. Report entries have observation_id and action. Action labels: '+', '.join(repr(z) for z in dict.fromkeys(actions))+'. Unchanged accepted rows have no report entry. Catch the deliberately false assertion.'
  prompt=openings[key]+'\n\nFixtures, teaching interfaces and execution adapters remain supplied. Replace all TODOs with your own code; implement the computation and fixture assertions rather than selecting a policy. Keep supplied fixture values, adapters and result bindings unchanged. The implementation must also work on changed input fixtures.\n\n'+'\n'.join(dict.fromkeys(spec))
  if output_names:prompt+='\nExpose: '+', '.join('`'+n+'`' for n in dict.fromkeys(output_names) if n not in ['name','field','traces','caught'])+'.'
  if extra:prompt+='\n'+extra
  i['public']['prompt']=prompt.strip()
  i['public']['workspace']['files'][0]['content']='# Editable learner implementation; supplied fixtures and adapters below.\n'+ '\n\n'.join(starter)+'\n'
  i['grading']['solution_files'][0]['content']='# Reference implementation with supplied fixtures and adapters.\n'+'\n\n'.join(solution)+'\n'
  ast.parse(i['public']['workspace']['files'][0]['content']);ast.parse(i['grading']['solution_files'][0]['content'])
# Grading keys, tests, constraints, anchors and all other interactions must remain intact.
for ta,tb in zip(before['tiles'],d['tiles']):
 for xa,xb in zip(ta['interactions'],tb['interactions']):
  if xa!=xb:
   a=copy.deepcopy(xa);b=copy.deepcopy(xb)
   a['interaction']['public'].pop('prompt');b['interaction']['public'].pop('prompt')
   if a['interaction']['type']=='code_exercise':
    a['interaction']['public']['workspace']['files'][0].pop('content');b['interaction']['public']['workspace']['files'][0].pop('content')
    a['interaction']['grading']['solution_files'][0].pop('content');b['interaction']['grading']['solution_files'][0].pop('content')
   assert a==b
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('Patched',len(openings),'code exercises and one formula scaffold; total interactions',sum(len(t['interactions']) for t in d['tiles']))
