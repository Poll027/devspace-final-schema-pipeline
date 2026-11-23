import ast,json,re,copy
from pathlib import Path
B=Path('batches/final_batch_mle.region.data_readiness'); P=B/'interactions.json'
d=json.loads(P.read_text()); old=copy.deepcopy(d)
prompts={
'001_003.s05': 'Implement validate(fixture). Convert the fixture with np.array, assign rank, shape and dtype, reject rank other than two before indexing shape, require two features and one through three orders, and return the accepted array. Write assertions for the supplied list, tuple, empty, flat, wrong-width and excessive-batch fixtures, including expected ValueError rejection.',
'001_003.s10': 'Implement compare(a, candidate_dtypes, tolerance, element_storage_budget). Cast both candidates from the unchanged reference, inspect their dtypes, compare every scalar value against the tolerance, calculate size * itemsize, confirm agreement with nbytes, and return reports, choice and scope using the supplied dictionary fields. Accept only candidates satisfying preservation and budget requirements; report neither otherwise. Evaluate both supplied reference fixtures.',
'001_003.s16': 'Import NumPy and implement transform(matrix, feature_references). Subtract the feature references using array arithmetic, author a list-comprehension reference, assert the intended result shape, and verify agreement with np.testing.assert_allclose using the supplied rtol and atol. Return the result array.',
'004_006.s11': 'Import pandas and implement inspect_chunks(path, declared_types, array_budget, feature_count, element_width). Derive row_limit from the supplied budget, iterate typed CSV chunks while the file handle remains open, materialize each matrix, check actual element bytes against nbytes and the budget, and track the largest single-chunk allocation without retaining earlier matrices. Return row_limit, chunk_rows, total_rows, largest_element_bytes and scope using the supplied field scaffold.',
'004_006.s16': 'Import NumPy and implement inspect(columns, numeric_values, ddof=0). Return columns, column_dtypes, observation_count, feature_count, shape, axis_meanings, means, std, dtype, element_bytes, nbytes and scope. Compute feature-wise means and standard deviations using the supplied ddof, observe dtype and memory from the input array, and identify the axes as observations and features. Evaluate both supplied fixtures.',
'007_008.s05': 'Import pandas and implement validate(table, contract). Check the exact column set, then declared dtypes, then inclusive distance bounds and permitted zone values. Return the unchanged table on acceptance; raise ValueError with columns, dtype, distance or zone respectively on failure. Author acceptance and rejection assertions for all supplied fixtures.',
'007_008.s10': 'Implement clean(records, policy) without modifying records. Use an accepted-key set and the supplied policy to reject invalid distances and repeated accepted keys, repair approved zone spellings, and retain valid observations. Add keys only after acceptance. Return cleaned and report, using report actions repaired, rejected and rejected_repeat for the supplied policy. Author assertions for valid, boundary, repair, rejection and repeated-key cases, including a deliberately false assertion caught as AssertionError.',
'009_011.s06': 'Using the supplied counts, calculate sample_shares, target_shares and inclusion in zone-A, zone-B order. Compute mean and std from numeric_values with ddof=0. Assign limitation to the supplied supported statement only if your calculated counts support it; do not infer a cause or inevitable prediction failure.',
'009_011.s11': 'Implement audit(observations, labels, contract). Detect repeated IDs before dictionary replacement; calculate missing and orphan IDs with set differences; use keyed lookups to check label validity, required timestamp correspondence and the declared inclusive or exclusive availability boundary. Return accepted, repeated, missing, orphan, invalid, misaligned and unavailable. Author assertions for valid, reordered, repeated-observation, repeated-label, missing, orphaned, invalid, misaligned, unavailable and cutoff-boundary cases.',
'009_011.s16': 'Implement partition(records, scenario, training_groups, cutoff, evaluation_end). For group, partition by training-group membership and assert disjoint group sets. For time, select training timestamps strictly before cutoff and validation timestamps in [cutoff, evaluation_end), then assert those inequalities. Return train, validation, train_proportion and validation_proportion, preserving input row order. Author assertions for the supplied valid, cutoff-equality and invalid-group assignments.',
'012_015.s05': 'Import NumPy and implement impute(X_train, X_validation, X_boundary, numeric_values) using the supplied SimpleImputer-compatible runtime dependency. Fit the declared mean strategy on training only, save statistics_, transform validation and boundary inputs without refitting, compute observed-training column means and ddof=0 standard deviations, and write assertions for outputs, unchanged statistics_ and the deliberately incorrect replacement. Return transformed, boundary, statistics, mean and std.',
'012_015.s11': 'Import NumPy and implement scale(X_train, X_validation) using the supplied StandardScaler-compatible runtime dependency with centering and scaling enabled. Fit training only, transform both inputs, compute column means and ddof=0 standard deviations, and author assertions for numerical results, constant-feature scale 1, unchanged mean_ and scale_, and the supplied incorrect result. Return train, validation, mean, std, mean_ and scale_.',
'012_015.s16': 'Implement encode(X_train, known, unseen, missing, policy) using the supplied OneHotEncoder-compatible runtime dependency. Fit training once with explicit handle_unknown, build the zone mapping from categories_, transform each fixture without refitting, record ValueError for rejected cases, and assert unchanged mapping and width. Author expected-output assertions for error and ignore, with missing values both present and absent at fit. Return mapping, outputs and width.',
'016_017.s05': 'Implement correct(training, held_out, permitted_features) using the supplied trace interfaces. Project only permitted fields, fit preprocessing only on designated training rows, transform held-out inputs without refitting, and pass those transformed inputs to prediction. Author invariant assertions for the three returned traces. Apply the same assertions to the supplied leaked traces and verify that each row-boundary and field-boundary violation fails.',
'016_017.s11': 'Import datetime and implement feature(records, prediction_time). Use a list comprehension with available_at <= prediction_time, initialize total to zero, accumulate only accepted values and return total. Author assertions that the supplied values produce 5, adding the later value 7 leaves the result unchanged, equality at the boundary is included, and an empty accepted list produces zero.',
'018_018.s05': 'Implement audit(identity, sample, permitted_fields) using the supplied authorized read_sample interface. Construct a new dictionary with membership checks, retain original permitted values, and never print or return restricted values or credentials. Preserve authorization rejection and leave secret use inside the supplied authorized interface. Write assertions for the authorized record and unauthorized identity.'}
fn_names=['validate','compare','transform','inspect_chunks','inspect','clean','audit','partition','impute','scale','encode','correct','feature','check_invariants']
class Relations(ast.NodeTransformer):
 def __init__(self,relation,summary):self.relation=relation; self.summary=summary
 def visit_Call(self,n):
  self.generic_visit(n)
  if isinstance(n.func,ast.Name) and n.func.id=='contract_relation':
   ops={'equal':ast.Eq,'different':ast.NotEq,'less_than':ast.Lt,'at_most':ast.LtE,'greater_than':ast.Gt,'at_least':ast.GtE,'member':ast.In,'not_member':ast.NotIn}
   return ast.copy_location(ast.Compare(left=n.args[0],ops=[ops[self.relation]()],comparators=[n.args[1]]),n)
  if isinstance(n.func,ast.Name) and n.func.id=='summary_statistic':n.func=ast.Attribute(value=ast.Name(id='np',ctx=ast.Load()),attr='mean',ctx=ast.Load())
  return n

def exec_body(n):
 if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Name) and n.value.func.id=='exec':return ast.literal_eval(n.value.args[0])

def selector(n):
 return isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ['contract_relation','summary_statistic']

def helper(n):
 b=exec_body(n);return b is not None and (b.startswith('import operator') or 'arithmetic_mean = np.mean' in b)

def skeleton(code):
 tree=ast.parse(code);f=tree.body[0]
 signature=ast.unparse(f).split('\n')[0]
 returns=[n for n in ast.walk(f) if isinstance(n,ast.Return) and isinstance(n.value,ast.Dict)]
 lines=[signature,'    # TODO: implement the operations and invariant assertions in the prompt.','    raise NotImplementedError']
 if returns:
  fields=returns[-1].value
  blank=ast.Dict(keys=fields.keys,values=[ast.Constant(value=Ellipsis) for _ in fields.values])
  lines+=['    # Output-field scaffold (replace each ... with your computed value):','    return '+ast.unparse(blank)]
  # keep report field names available, but not completed operations
  nested=[n for n in ast.walk(f) if isinstance(n,ast.Dict) and n is not fields]
  for nd in nested:
   if all(isinstance(k,ast.Constant) and isinstance(k.value,str) for k in nd.keys):
    lines+=['    # Additional dictionary fields: '+', '.join(k.value for k in nd.keys)]
 return '\n'.join(lines)

for t in d['tiles']:
 for s in t['interactions']:
  sid=s['step_id'].removeprefix('mle.tile.');i=s['interaction']
  if sid not in prompts:continue
  i['public']['prompt']=prompts[sid]
  starter=i['public']['workspace']['files'][0]['content'];solution=i['grading']['solution_files'][0]['content']
  st=ast.parse(starter);so=ast.parse(solution)
  relation=next((n.value.id for n in so.body if selector(n) and isinstance(n.value,ast.Name) and n.targets[0].id=='contract_relation'),None)
  out=['# Supplied fixtures and harness; implement the unfinished learner sections.'];sol=['# Reference implementation with the same fixture and output contracts.'];after_fn=False
  for n in st.body:
   if selector(n) or helper(n):continue
   b=exec_body(n)
   learner=b is not None and isinstance(ast.parse(b).body[0],ast.FunctionDef) and ast.parse(b).body[0].name in fn_names
   if learner:
    out.append(skeleton(b));after_fn=True;continue
   if sid=='009_011.s06' and isinstance(n,ast.Assign) and n.targets[0].id in ['sample_total','target_total','sample_shares','target_shares','inclusion','mean','std','limitation']:
    name=n.targets[0].id
    if name=='limitation':out.append('supported_statement = '+ast.unparse(n.value))
    out.append(name+' = None  # TODO: calculate or select from the supported statement.');continue
   # Preserve fixtures, imports, runtime/harness, and fixture evaluation calls; remove learner assertions.
   if after_fn:
    if isinstance(n,(ast.Assert,ast.Try,ast.For)):continue
    if isinstance(n,ast.Expr) and b is None:continue
    if isinstance(n,ast.Assign):
     names=[x.id for x in n.targets if isinstance(x,ast.Name)]
     keep={'accepted','boundary','result','boundary_result','valid_result','group_result','time_result','ignore_result','error_result','seen_missing_result','augmented_result','boundary_records','reordered_labels','leaked_traces','secret_used'}
     if not set(names)&keep:continue
     if names==['result'] and sid=='007_008.s05':out.append('result = None  # TODO: evaluate fixtures and record verdicts.');continue
   out.append(ast.get_source_segment(starter,n))
  out.append('# TODO: author acceptance, rejection, boundary and invariant assertions requested above.')
  for n in so.body:
   if helper(n) or selector(n):continue
   b=exec_body(n)
   if b is not None and isinstance(ast.parse(b).body[0],ast.FunctionDef) and ast.parse(b).body[0].name in fn_names:
    nt=Relations(relation,True).visit(ast.parse(b));ast.fix_missing_locations(nt);sol.append(ast.unparse(nt))
   else:
    nt=Relations(relation,True).visit(copy.deepcopy(n));ast.fix_missing_locations(nt)
    sol.append(ast.unparse(nt) if ast.dump(nt)!=ast.dump(n) else ast.get_source_segment(solution,n))
  i['public']['workspace']['files'][0]['content']='\n\n'.join(out)+'\n'
  i['grading']['solution_files'][0]['content']='\n\n'.join(sol)+'\n'
  # Make the trace fixture independent of the learner's implementation.
  if sid=='016_017.s05':
   content=i['public']['workspace']['files'][0]['content'];tree=ast.parse(content)
   fixture=next(n for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='leaked_traces')
   text=ast.get_source_segment(content,fixture);content=content.replace(text+'\n\n','');index=content.index('def correct(');content=content[:index]+text+'\n\n'+content[index:];i['public']['workspace']['files'][0]['content']=content

# Advisory changes: wording only; derive formula labels and separators from existing reference.
for t in d['tiles']:
 for s in t['interactions']:
  sid=s['step_id'].removeprefix('mle.tile.');i=s['interaction']
  if sid=='000_000.s06':
   formula=i['grading']['reference_formula']
   parts=formula.split('&" | "&')
   for j in range(7):
    label=parts[j].split(':',1)[0];parts[j]=label+': "&[selected_value_'+str(j+1)+']'
   for j in [7,8]:parts[j]=re.sub(r'B\d/C\d','[division_expression_'+str(j-6)+']',parts[j])
   i['public']['prompt']+='\n\nStarter formula (replace the nine bracketed blanks; keep fixed labels and separators):\n'+ '&" | "&'.join(parts)
  if sid=='001_003.s15':
   i['grading']['option_feedback']['b']['message']='a + b adds the references instead of subtracting them.'
   i['grading']['option_feedback']['c']['message']='b - a reverses the subtraction: it subtracts order features from references.'
  if sid=='004_006.s06':
   i['public']['prompt']=i['public']['prompt'].replace('Retrieve approved/orders-b.csv, preserve declared types including text order_key, verify columns/row count/key, write identity via UTF-8 handle, and distinguish complete CSV access from selected-column Parquet.','The contract requires retrieving approved/orders-b.csv, preserving declared types including text order_key, verifying columns/row count/key, writing identity through a UTF-8 handle, and distinguishing complete CSV access from selected-column Parquet. Read each excerpt and decide whether its shown evidence satisfies that contract.')
# Scope checks: unchanged grading tests, constraints, anchors, measures, and all unlisted interactions.
changes=[]
for ot,nt in zip(old['tiles'],d['tiles']):
 for os,ns in zip(ot['interactions'],nt['interactions']):
  if os==ns:continue
  sid=ns['step_id'].removeprefix('mle.tile.');assert sid in prompts or sid in ['000_000.s06','001_003.s15','004_006.s06']
  for key in ['anchors','measures']:assert os['interaction'][key]==ns['interaction'][key]
  if sid in prompts:
   assert os['interaction']['grading']['tests']==ns['interaction']['grading']['tests']
   assert os['interaction']['public']['constraints']==ns['interaction']['public']['constraints']
  changes.append(ns['step_id'])
P.write_text(json.dumps(d,indent=2)+'\n');print('Patched',len(changes),'interactions:',changes)
