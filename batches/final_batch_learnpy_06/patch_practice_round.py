import json, textwrap
from pathlib import Path
b=Path('batches/final_batch_learn_python.region.06')
p=b/'interactions.json'; d=json.loads(p.read_text()); original=json.loads(p.read_text())
ids=['learn_python.tile.100_103.s09','learn_python.tile.104_106.s04','learn_python.tile.107_109.s03','learn_python.tile.110_112.s12']
for t in d['tiles']:
 for v in t['interactions']:
  sid=v['step_id']
  if sid not in ids: continue
  i=v['interaction']; pub=i['public']; starter=pub['workspace']['files'][0]; sol=i['grading']['solution_files'][0]; old=sol['content']
  if sid==ids[0]:
   prompt='Write the assignment to total using a filtered generator expression as the sole argument to sum. Double only the positive entries in values, using supplied_factor and supplied_minimum as the doubling factor and positive-entry boundary. Do not construct an intermediate collection. Keep the supplied inputs unchanged.'
   prefix=old.split('\n# TODO:')[0]+'\n\n'
   calculation=textwrap.dedent(old.split('if True:\n',1)[1]).replace(' * factor',' * supplied_factor').replace(' > minimum',' > supplied_minimum')
   starter['content']=prefix+'# TODO: '+prompt+'\n';sol['content']=starter['content']+calculation
  elif sid==ids[1]:
   prompt='Rewrite the assignment to stored so it totals the doubled entries in values using a generator expression directly inside sum, without materializing an intermediate transformed list. Use supplied_factor as the doubling factor and keep the supplied inputs unchanged.'
   prefix=old.split('\n# TODO:')[0]+'\n\n'
   calculation=textwrap.dedent(old.split('if True:\n',1)[1]).replace(' * factor',' * supplied_factor')
   eager=calculation.replace('sum(', 'sum([').replace(')\n', '])\n')
   starter['content']=prefix+eager+'# TODO: '+prompt+'\n';sol['content']=prefix+calculation+'# TODO: '+prompt+'\n'
  elif sid==ids[2]:
   prompt='Write the unittest import and a CostTests subclass of unittest.TestCase. In test_cost, check that cost(3) equals supplied_expected_cost and is positive, using equality and truth assertions. In test_invalid_quantity, check that cost(-1) raises ValueError, placing the call inside the expected-exception context. Keep the supplied helper and inputs unchanged. Do not add a test runner; the checker runs the methods and checks detection of changed helper behavior.'
   prefix=old.split('# Supplied cases:')[0]
   tests=textwrap.dedent(old.rsplit('if True:\n',1)[1]).replace('expected_cost)', 'supplied_expected_cost)')
   starter['content']=prefix+'# TODO: '+prompt+'\n';sol['content']=starter['content']+tests
  else:
   prompt='Implement the quantity parser for text without executing the supplied text. Valid nonnegative integer text must produce the integer in quantity. Malformed text and negative integers must leave quantity as None without an uncaught conversion error. Write the conversion-error handler and explicit nonnegative validation yourself. Keep the rejected eval proposal commented and never use eval, exec or shell invocation. Keep the supplied input unchanged.'
   prefix=old.split('\n# TODO:')[0]+'\n\n'
   repair=textwrap.dedent(old.split('if True:\n',1)[1]).replace('parser(text)', 'int(text)')
   starter['content']=prefix+'# TODO: '+prompt+'\n';sol['content']=starter['content']+repair
  pub['prompt']=prompt
  for test in i['grading']['tests']:
   test['message_on_fail']='Match the required behavior and source structure described in the prompt.'
# Enforce repair scope; answer predicates, expected values, constraints untouched.
for t0,t1 in zip(original['tiles'],d['tiles']):
 for v0,v1 in zip(t0['interactions'],t1['interactions']):
  if v0['step_id'] not in ids: assert v0==v1
  else:
   assert v0['interaction']['public']['constraints']==v1['interaction']['public']['constraints']
   for a,c in zip(v0['interaction']['grading']['tests'],v1['interaction']['grading']['tests']): assert a['spec']==c['spec']
p.write_text(json.dumps(d,indent=2)+'\n')
print('Patched',len(ids),'exercises;',sum(len(t['interactions']) for t in d['tiles']),'interactions total')
