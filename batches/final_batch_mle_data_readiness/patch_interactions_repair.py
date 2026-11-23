import ast, json
from pathlib import Path
B=Path('batches/final_batch_mle.region.data_readiness')
p=B/'interactions.json'
d=json.loads(p.read_text())
prompts={
'001_003.s05': 'Import NumPy and implement inspect(fixture). Construct the array without casting or flattening; inspect rank, shape and dtype; check rank before axis lengths; accept width two and batches of one through three; otherwise raise descriptive ValueError. Return the accepted array. Author assertions for one- and three-order list and tuple inputs and empty, flat, wrong-width and four-order rejections.',
'001_003.s10': "Import NumPy and implement compare(reference, candidates, tolerance, budget). Explicitly cast each candidate from the unchanged reference, compare every scalar against its reference within tolerance, calculate size times itemsize and confirm agreement with nbytes and unchanged element count. Return the existing per-candidate report fields, accepting only value-preserving candidates within budget; use the justification ‘element storage, not total object memory’.",
'001_003.s16': 'Import NumPy and implement transform(fixture). Subtract feature references [1, 5] using array arithmetic. Author an independent list-comprehension reference, assert the intended two-axis result shape, and check agreement with np.testing.assert_allclose using rtol=1e-7 and atol=1e-9. Return the result array.',
'004_006.s11': "Import pandas and implement scan(path, budget, feature_count, element_width, declared_types). Calculate the row limit; iterate read_csv chunks inside an open-file block; materialize each matrix; compute bytes from actual shape and dtype; assert agreement with nbytes and compliance with budget. Return row_limit, largest_element_bytes and memory_scope='single matrix element storage only'. Do not retain previous chunks.",
'004_006.s16': "Import NumPy and implement readiness(columns, numeric_values, ddof=0). Return columns, column_dtypes, observations, features, shape, dtype, element_bytes, means, standard_deviations and memory_scope='element storage, not total process memory'. Summarize each feature over rows using the caller’s divisor and preserve the observation/feature axis meanings.",
'007_008.s05': 'Import pandas and implement validate(table). Require exactly distance: float64 and zone: string; distance 0 through 100 inclusive; zone north or south. Check columns and types before values, raise descriptive ValueError on violations without changing input, and return True on acceptance. Author assertions for valid input, both endpoints, missing and unexpected columns, wrong types, invalid zones and out-of-range distances.',
'007_008.s10': 'Implement clean_orders(records, policy). Use an accepted-key set and add keys only after acceptance. Apply the supplied duplicate, distance and zone-repair policies through conditional branches. Return cleaned observations and affected observation IDs/actions in the existing schema. Author assertions for retain, both distance boundaries, repair, rejection, repeated accepted keys and invalid-then-valid retry; demonstrate detection of a deliberately false expected result.',
'009_011.s06': "Import NumPy and implement evaluate_statistics(fixture). Compute sample shares from the sample total, target shares from the target total and inclusion rates from each category’s target count; return 'unsupported' for a zero category denominator. Compute the selected observations’ mean and population standard deviation. Return the existing ordered fields and a count-supported limitation without asserting an unobserved cause or inevitable prediction failure.",
'009_011.s11': 'Implement audit(observations, labels, boundary) using the supplied predicates. Detect repeated observation and label IDs before mapping; report both unmatched-ID directions; use keyed lookups to report invalid, misaligned and unavailable records, accepting cutoff equality. Return the existing verdict and affected-ID fields. Author assertions for valid, reordered, duplicate, missing, orphaned, invalid, misaligned, unavailable and equality-boundary cases.',
'009_011.s16': 'Implement partition(records, scenario, training_groups, cutoff, end). For groups, assign complete groups and assert disjoint group sets. For time, use training timestamps < cutoff and cutoff <= validation timestamps < end. Return the existing partitions, each partition’s target proportion or None when empty, and the existing scenario-specific justification. Author valid, equality-boundary and deliberately invalid group/time assertions.',
'012_015.s05': 'Import NumPy and SimpleImputer and implement replace_missing(train, validation, single_missing). Fit a mean imputer on training only; compute the observed training column mean and population standard deviation; transform validation and the single-missing boundary without refitting. Return the existing report fields. Author assertions for unchanged statistics_, preserved complete values, correct missing replacements and a deliberately incorrect replacement.',
'012_015.s11': 'Import NumPy and StandardScaler and implement scale(train, validation). Compute training column means and population standard deviations; fit one centered, standardized scaler on training only; transform training and validation with that object. Return the existing report fields. Author assertions for expected values, unchanged mean_ and scale_, constant-feature scale_ of 1 and detection of incorrect results or changed state.',
'012_015.s16': 'Import NumPy and OneHotEncoder and implement encode(training, cases, policy). Fit once with the supplied error or ignore policy and sparse_output=False. Build the zone mapping from categories_, transform aligned cases without refitting and return mapping, width and results in the existing schema. Author assertions for known indicators, unknown and missing behavior, unchanged categories and output width under both policies and both missing-at-fit conditions.',
'016_017.s05': 'Implement corrected(training, held_out, preprocessor, predictor). Select only distance and zone, fit preprocessing only on training inputs and transform held-out inputs without refitting. Author boundary_check assertions for permitted prediction fields, training-only fit rows and held-out transform/prediction inputs. Apply those same checks to leaked and corrected variants, asserting failure for the former and success for the latter.',
'016_017.s11': 'Import datetime and implement feature(records, prediction_time). Select records with a list comprehension using available_at <= prediction_time, initialize total=0, accumulate only accepted values and return total. Author assertions for exact-boundary inclusion, empty input and invariance after adding later observations.',
'018_018.s05': 'Implement permitted_record(identity, sample, permitted_fields). Call the supplied authorized read interface before processing. Construct a fresh dictionary using permitted-field membership checks, preserve permitted values and exclude token and raw_customer_values. Do not print restricted values or retrieve/copy the runtime secret. Return the dictionary and allow authorization denial to propagate.'
}
changed=[]
for tile in d['tiles']:
 for step in tile['interactions']:
  key=step['step_id'].removeprefix('mle.tile.')
  if key not in prompts: continue
  i=step['interaction']; i['public']['prompt']=prompts[key]
  file=i['public']['workspace']['files'][0]
  s=file['content']; lines=s.splitlines(keepends=True)
  targets=[n for n in ast.walk(ast.parse(s)) if isinstance(n,ast.FunctionDef) and (n.name.startswith('supplied_') or n.name in ('learner_checks','boundary_check'))]
  for n in sorted(targets,key=lambda n:n.lineno,reverse=True):
   name=n.name.removeprefix('supplied_').removesuffix('_workflow') if n.name.startswith('supplied_') else n.name
   indent=' '*n.col_offset
   lines[n.lineno-1:n.end_lineno]=[f'{indent}def {name}({ast.unparse(n.args)}):\n',f'{indent}    # TODO: implement the required calculations or assertions.\n',f'{indent}    raise NotImplementedError\n']
  s=''.join(lines)
  s=s.split('# Supplied inactive entry point; activate the workflow below.')[0].rstrip()+'\n'
  ast.parse(s); file['content']=s
  changed.append(key)
  if key=='004_006.s11':
   # Derive element bytes from the evaluator-specified eight-row asset and declared float widths.
   registry=json.loads((B/'scenario_asset_registry.json').read_text())
   asset=next(a for a in registry['assets'] if a['asset_id']=='ds.chunked_orders')
   constants={n.targets[0].id:ast.literal_eval(n.value) for n in ast.walk(ast.parse(file['content'])) if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('FEATURE_COUNT','ELEMENT_WIDTH','DECLARED_TYPES')}
   test=next(t for t in i['grading']['tests'] if t['test_id']=='t1')
   budget=test['spec']['args'][0]
   row_limit=budget//(constants['FEATURE_COUNT']*constants['ELEMENT_WIDTH'])
   widths=[int(dtype.removeprefix('float'))//8 for dtype in constants['DECLARED_TYPES'].values()]
   assert len(widths)==len(asset['columns']) and len(set(widths))==1
   test['spec']['expected']={'row_limit':row_limit,'largest_element_bytes':min(row_limit,8)*len(asset['columns'])*widths[0], 'memory_scope':test['spec']['expected']['memory_scope']}

p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('Patched',len(changed),'interactions:',changed)
print('Total',sum(len(t['interactions']) for t in d['tiles']))
