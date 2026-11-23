import ast,json,re,textwrap
from pathlib import Path
B=Path('batches/final_batch_mle.region.ml_lifecycle');P=B/'interactions.json';d=json.loads(P.read_text())
targets={'mle.tile.073_075.s05','mle.tile.073_075.s10','mle.tile.073_075.s17','mle.tile.076_079.s05','mle.tile.076_079.s17'}
prompts={
'mle.tile.073_075.s05':'''Implement the editable contract_checks(snapshot), dataset_gate(snapshot, required), and fatal_dataset(args) stubs and write their dependency imports. Read fixtures/dataset_contract.json and fixtures/dataset_cases.json. Author the named schema, feature_values, label_values and unique_sample_id checks; aggregate every required named result into accepted and failed_checks, retaining snapshot_id and sha256 with checks. Missing required checks or invalid fixtures must fail closed. Fill the assertion stubs for valid, boundary, every invalid fixture and the missing-required-feature case, including evidence identity and named failure checks. Wire quality as training's explicit fatal predecessor, write/reload resolved.yaml with PyYAML and inspect the resolved configuration. Implement assertions on configured repository-commit triggered runs proving accepted quality permits training while rejected quality fails and training is SKIPPED. Retain report and its existing field names; do not alter fixture contracts, trigger filters, commands, images or downstream implementation.''',
'mle.tile.073_075.s10':'''Write the dependency imports and implement reusable test_behavior(package, fixture, contract) and fatal_behavior(args). Exercise the supplied FittedPackage.predict inference path with packaged fitted preprocessing. For valid and boundary fixtures, write assertions for output row count, sample correspondence, output shape and numerical values using np.testing.assert_allclose with explicit contract rtol and atol. For malformed fixtures require InputContractError and fail if prediction returns normally. Complete assertions that each declared regression is rejected. Wire behavior_tests as release_gate's fatal predecessor, round-trip resolved.yaml and inspect it. Complete triggered-run assertions proving successful tests permit release_gate and failed assertions cause behavior_tests FAILURE and release_gate SKIPPED. Preserve report's existing fields and fixture expectations, trigger bindings, commands and images.''',
'mle.tile.073_075.s17':'''Write the dependency imports and implement error_rates(evidence), expected_cost(evidence, contract), acceptance(candidate, reference, contract, event_id), and fatal_acceptance(args). Calculate FPR=FP/(FP+TN), FNR=FN/(FN+TP), and expected error cost from the declared deployment probabilities and costs. Reject invalid counts and undefined denominators. Require complete evidence, matching candidate/event identity, fixed latency and operating predicates, the maximum expected cost and accepted-reference comparison; explicitly reject each failed requirement. Complete learner assertions for accepted, boundary, rejected, empty-class and incomplete fixtures, FPR/FNR and cost, and false operating/evidence predicates. Round-trip the configuration and wire release_gate as promotion's fatal predecessor. Complete configured Pub/Sub triggered-run assertions verifying rejected gates and identity disagreement remain FAILURE with promotion SKIPPED. Preserve report and existing fixture keys, trigger filters, commands and images.''',
'mle.tile.076_079.s05':'''Repair training_waits, model_waits and model_input and implement dependency_checks(record) with named data_to_training, training_to_model, data_validation and model_validation predicates. Resolve the supplied stage dependency dictionary and compare upstream produced identities with downstream consumed identities; validation must be True, not merely present. Write assertions that valid and boundary maps pass, rejected_data fails validation and the supplied A-to-B mismatch fails training_to_model before repair. Copy that mismatch record, repair its model consumer from the training producer, then assert all predicates pass afterward. Keep the original mismatch fixture unchanged so triggered execution still rejects it. Write/reload resolved.yaml and complete assertions inspecting the resolved inputs and configured Pub/Sub runs: explicit upstream dependencies, repaired valid execution, rejected validation, consumer mismatch and downstream skipping. Preserve report's existing fields, fixture contracts, trigger bindings, commands and images.''',
'mle.tile.076_079.s17':'''Write the dependency imports and implement verify(context, output, blob) and bounded recover(context). Catch only the declared recoverable failure, record it and apply the supplied recovery action. Reconcile each declared output without overwriting existing content: reload metadata, retain its generation, download that exact generation, check its hash and require output validation. Upload only missing outputs with if_generation_match=0; after PreconditionFailed (412), reload and verify the existing generation/content, rejecting conflicts. Unrelated exceptions and failed validation must remain fatal. Wire recovery then required_validation as fatal explicit predecessors, round-trip resolved.yaml, and complete learner assertions for accepted, boundary-completed, race-412, invalid-existing, conflicting-content, unrelated-failure and rejected-gate cases. Assert A generation/hash preservation, B content/validation, no extra uploads or generations on repeated invocation, repeated validation and actual triggered stage outcomes with rejection blocking downstream execution. Preserve report fields, contracts, trigger bindings, commands and images.'''
}
# Expand the functions formerly wrapped as immutable scaffolding, leaving runtime setup intact.
def editable_solution(s):
 lines=s.splitlines(True);tree=ast.parse(s);patch=[]
 for n in tree.body:
  if isinstance(n,ast.If) and isinstance(n.test,ast.Constant) and n.test.value is True and all(isinstance(x,ast.FunctionDef) for x in n.body):
   patch.append((n.lineno-1,n.end_lineno,textwrap.dedent(''.join(lines[n.lineno:n.end_lineno]))))
 for a,b,v in reversed(patch):lines[a:b]=[v]
 s=''.join(lines)
 s='\n'.join(l for l in s.splitlines() if not (l.startswith('#') and any(w in l for w in ['scaffolding','Supplied fixture','Supplied practice','read-only','leave unchanged','learner edits only','no learner edits','no learner edits required','Edit only'])))+'\n'
 return s
for t in d['tiles']:
 for x in t['interactions']:
  tag=x['step_id']
  if tag not in targets:continue
  i=x['interaction'];ws=i['public']['workspace'];entry=ws['entry'];sf=next(f for f in i['grading']['solution_files'] if f['path']==entry);s=editable_solution(sf['content'])
  if tag.endswith('073_075.s05'):
   s=s.replace("assert 'schema' in results['missing_required_feature']['failed_checks']", "assert 'schema' in results['missing_required_feature']['failed_checks']\nfor name in cases:\n    assert results[name]['snapshot_id'] == cases[name]['snapshot_id']\n    assert results[name]['sha256'] == cases[name]['sha256']\n    assert set(results[name]['checks']) == set(contract['required_checks'])")
  if tag.endswith('073_075.s17'):
   pos=s.index('def expected_cost(')
   s=s[:pos]+'''def error_rates(evidence):
    for name in ['FP', 'TN', 'FN', 'TP']:
        if name not in evidence or not valid_count(evidence[name]):
            raise ValueError('invalid_count:' + name)
    negative = evidence['FP'] + evidence['TN']
    positive = evidence['FN'] + evidence['TP']
    if negative <= 0 or positive <= 0:
        raise ValueError('undefined_actual_class_rate')
    return [evidence['FP'] / negative, evidence['FN'] / positive]

'''+s[pos:]
   s=s.replace("fpr = evidence['FP'] / negative\n    fnr = evidence['FN'] / positive", "fpr, fnr = error_rates(evidence)")
   pos=s.index("\nconfig = read('cloudbuild.yaml')")+1
   s=s[:pos]+'''for name in ['A', 'B', 'boundary']:
    evidence = cases[name]
    fpr, fnr = error_rates(evidence)
    assert fpr == evidence['FP'] / (evidence['FP'] + evidence['TN'])
    assert fnr == evidence['FN'] / (evidence['FN'] + evidence['TP'])
    weighted = contract['probabilities']['P(Y=0)'] * contract['costs']['cost_FP'] * fpr + contract['probabilities']['P(Y=1)'] * contract['costs']['cost_FN'] * fnr
    assert math.isclose(expected_cost(evidence, contract), weighted, rel_tol=0.0, abs_tol=COST_TOLERANCE)
'''+s[pos:]
   cases=json.loads(next(f['content'] for f in ws['files'] if f['path']=='fixtures/release_cases.json'))
   for name in ['A','B']:
    e=cases[name];rates=[e['FP']/(e['FP']+e['TN']),e['FN']/(e['FN']+e['TP'])]
    i['grading']['tests'].append({'test_id':'test.'+tag+'.rates.'+name,'kind':'function_call','spec':{'function':'error_rates','args':[e],'expected':rates},'message_on_fail':'Calculate both class-conditional error rates from the supplied counts.'})
  if tag.endswith('076_079.s05'):
   s=s.replace('from support import read, dependency_suite','from support import read, dependency_suite\nimport copy')
   pos=s.index("\ncases=read(")+1
   s=s[:pos]+'''def dependency_checks(record):
    return {
        'data_to_training': record['data_validation']['produced'] == record['training']['consumed'],
        'training_to_model': record['training']['produced'] == record['model_validation']['consumed'],
        'data_validation': record['data_validation']['validation_ok'] is True,
        'model_validation': record['model_validation']['validation_ok'] is True,
    }

'''+s[pos:]
   s+='''checks = {name: dependency_checks(record) for name, record in cases.items()}
assert all(checks['valid'].values())
assert all(checks['boundary'].values())
assert not checks['rejected_data']['data_validation']
assert not checks['mismatch']['training_to_model']
repaired = copy.deepcopy(cases['mismatch'])
repaired['model_validation']['consumed'] = repaired['training']['produced']
assert all(dependency_checks(repaired).values())
assert cases['mismatch']['model_validation']['consumed'] != cases['mismatch']['training']['produced']
assert report['runs']['valid']['steps'][2]['status'] == 'SUCCESS'
assert report['runs']['mismatch']['steps'][2]['status'] == 'FAILURE'
assert report['runs']['rejected_data']['steps'][1]['status'] == 'SKIPPED'
'''
   cs=json.loads(next(f['content'] for f in ws['files'] if f['path']=='fixtures/dependency_cases.json'))
   for name,r in cs.items():
    expect={'data_to_training':r['data_validation']['produced']==r['training']['consumed'],'training_to_model':r['training']['produced']==r['model_validation']['consumed'],'data_validation':r['data_validation']['validation_ok'] is True,'model_validation':r['model_validation']['validation_ok'] is True}
    i['grading']['tests'].append({'test_id':'test.'+tag+'.map.'+name,'kind':'function_call','spec':{'function':'dependency_checks','args':[r],'expected':expect},'message_on_fail':'Check both immutable artifact identities and required validation predicates.'})
  sf['content']=s
  # Keep fixture loading / execution harness, but leave ALL assessed functions,
  # dependency imports and assertion expressions for the learner to implement.
  lines=s.splitlines(True);tree=ast.parse(s);patch=[]
  for n in ast.walk(tree):
   if isinstance(n,ast.FunctionDef):
    start=n.body[0].lineno-1
    patch.append((start,n.end_lineno,' '*(n.col_offset+4)+'# TODO: implement this contract function.\n'+' '*(n.col_offset+4)+'raise NotImplementedError\n'))
   elif isinstance(n,ast.Assert):
    # Nested assertions are already removed with their function bodies.
    if any(isinstance(f,ast.FunctionDef) and f.lineno <= n.lineno <= f.end_lineno for f in ast.walk(tree)):continue
    patch.append((n.lineno-1,n.end_lineno,' '*n.col_offset+'# TODO: write the required fixture/evidence assertion.\n'+' '*n.col_offset+'assert False\n'))
   elif isinstance(n,(ast.Import,ast.ImportFrom)) and n.lineno>10:
    patch.append((n.lineno-1,n.end_lineno,'# TODO: write the required dependency imports.\n'))
  for a,b,v in sorted(patch,reverse=True):lines[a:b]=[v]
  starter=''.join(lines)
  # The dependency-map repair must also be learner-authored, not a completed copy.
  if tag.endswith('076_079.s05'):
   starter=starter.replace("repaired['model_validation']['consumed'] = repaired['training']['produced']", "# TODO: repair the copied model consumer identity from its producer.\nrepaired['model_validation']['consumed'] = None")
   starter=starter.replace('training_waits = required_training_waits','training_waits = no_waits').replace('model_waits = required_model_waits','model_waits = no_waits').replace('model_input = training_output','model_input = other_input')
  else:
   starter=re.sub(r'(stage_\d+_waits) = required_stage_\d+',r'\1 = no_predecessors',starter)
  starter='# Learner tasks: write imports, implement function stubs and fixture assertions, and wire fatal dependencies.\n# Dependency setup and registered assets below are supplied runtime infrastructure.\n'+starter
  next(f for f in ws['files'] if f['path']==entry)['content']=starter
  i['public']['prompt']=prompts[tag]
  i['feedback']['hints']=['Follow the fixture contract and keep identity evidence attached to the checks.','Inspect both accepted and rejected runs; a required failure must block its dependent stage.']
P.write_text(json.dumps(d,indent=2)+'\n')
print('patched',len(targets),'interactions')
