import json, ast, os, contextlib, io
from pathlib import Path
root=Path('batches/final_batch_learn_python.region.04').resolve()
d=json.loads((root/'interactions.json').read_text())
g=json.loads((root/'inputs/path_glossary_bundle.json').read_text())
anchors={b['context']['concept_id']:b['practice_anchor'] for b in g['bundles']}
plan=json.loads((root/'tile_plans.json').read_text())
screens=json.loads((root/'screens.json').read_text())
changed={
'066_066':['s04'],'067_067':['s05'],'068_070':['s04','s08','s12'],
'071_073':['s03','s06','s10'],'074_074':['s03'],'075_075':['s04'],
'078_078':['s04'],'079_079':['s04'],'080_083':['s07','s12','s16']}
passed=0;failures=[];starter_failures=0
for tile in d['tiles']:
 for x in tile['interactions']:
  i=x['interaction'];short=tile['tile_id'].split('.')[-1];step=x['step_id'].split('.')[-1]
  if short not in changed or step not in changed[short]:continue
  anchor=anchors[i['measures'][0]['concept_id']]
  assert i['public']['constraints']['allowed_syntax']==anchor['live_code']['allowed_syntax']
  assert i['public']['constraints']['blocked_syntax']==anchor['live_code']['blocked_syntax']
  folder=root/'working'/'repair_checks'/short/step;folder.mkdir(parents=True,exist_ok=True)
  for is_solution,code in [(True,i['grading']['solution_files'][0]['content']),(False,i['public']['workspace']['files'][0]['content'])]:
   (folder/'main.py').write_text(code)
   os.chdir(folder); ns={}
   try:
    with contextlib.redirect_stdout(io.StringIO()):exec(compile(code,'main.py','exec'),ns)
    if is_solution:
     for t in i['grading']['tests']:
      if t['kind']=='function_call':
       spec=t['spec'];actual=ns[spec['function']](*spec['args'],**spec.get('kwargs',{}))
       assert actual==spec['expected'],(x['step_id'],t['test_id'],actual,spec['expected'])
       passed+=1
    else:
     # At least one visible check must reject the unfinished implementation.
     failed=False
     for t in i['grading']['tests']:
      if t['kind']=='function_call':
       spec=t['spec']
       try:actual=ns[spec['function']](*spec['args'],**spec.get('kwargs',{}))
       except Exception:failed=True;break
       if actual!=spec['expected']:failed=True;break
     assert failed,'starter passes: '+x['step_id']
     starter_failures+=1
   except Exception as e:
    if is_solution:failures.append((x['step_id'],repr(e)))
    else:starter_failures+=1
   finally:os.chdir(root.parent.parent)
print('Solution fixture tests passed:',passed)
print('Unfinished starters rejected:',starter_failures)
print('Solution failures:',failures)
assert not failures
log=(root/'working/repair_validate.log').read_text()
errs=[line for line in log.splitlines() if line.startswith('  E ')]
print('Gate errors:',len(errs))
print('Non-syntax gate errors:',[e for e in errs if ': solution uses ' not in e])
