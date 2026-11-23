import json,sys,ast
from pathlib import Path
B=Path('batches/final_batch_learn_python.region.06')
p=B/'interactions.json';d=json.loads(p.read_text())
bundles={x['context']['concept_id']:x for x in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}
changed=[]
for tile in d['tiles']:
 for row in tile['interactions']:
  sid=row['step_id'];i=row['interaction']
  if not any(sid.endswith(x) for x in ['100_103.s06','100_103.s09','104_106.s04','104_106.s12','107_109.s03','107_109.s13','110_112.s12']):continue
  pub=i['public'];old=i['grading']['solution_files'][0]['content'];starter=pub['workspace']['files'][0]['content']
  concept=i['measures'][0]['concept_id'];assert pub['constraints']=={k:bundles[concept]['practice_anchor']['live_code'][k] for k in ['allowed_syntax','blocked_syntax']}
  if sid.endswith('100_103.s06'):
   prefix,body=old.split('def positive_quantities(values):',1)
   scaffold=prefix+'# Supplied generator implementations: leave unchanged.\nif True:\n    def supplied_positive_quantities(values):'+''.join('\n    '+line if line else '\n' for line in body.split('\n')[1:])+'\n    def supplied_empty_generator(values):\n        for value in values:\n            if value > 0:\n                yield value\n                return\n'
   wrong='positive_quantities = supplied_empty_generator\n';right='positive_quantities = supplied_positive_quantities\n'
   prompt='The loop, condition, and yield are supplied as scaffold. Replace only the positive_quantities assignment to select supplied_positive_quantities rather than supplied_empty_generator. Keep the scaffold and inputs unchanged. The selected function must create a generator iterator, yield every positive input in order, and terminate after the finite input (not stop after its first accepted value).'
  elif sid.endswith('100_103.s09'):
   prefix,expression=old.rsplit('total = sum(',1)
   scaffold=prefix+'# Select the aggregation callable; keep the expression below unchanged.\n'
   tail='\n# Supplied lazy transformation and filtering scaffold.\ntotal = aggregate('+expression
   wrong='aggregate = list\n';right='aggregate = sum\n'
   prompt='Replace only aggregate = list with an assignment binding aggregate to sum. Keep inputs and the supplied generator expression unchanged. The expression doubles only entries strictly greater than supplied_minimum and is the sole argument to the aggregation call; total must be the numeric sum, not a materialized collection.'
  elif sid.endswith('104_106.s04'):
   prefix,expression=old.rsplit('stored = sum(',1)
   scaffold=prefix+'# Choose the one-pass aggregation callable.\n'
   tail='\n# Supplied generator expression: leave unchanged.\nstored = aggregate('+expression
   wrong='aggregate = list\n';right='aggregate = sum\n'
   prompt='The supplied expression already uses a generator rather than an intermediate transformed list. Replace only aggregate = list with an assignment binding aggregate to sum, so stored is the numeric total of the doubled input values. Keep all inputs and the generator expression unchanged; the selected callable must consume that generator directly.'
   test=i['grading']['tests'][0]['spec']
   test['expr']=test['expr'].replace("n.value.func.id == 'sum'", "n.value.func.id == 'aggregate' and aggregate is sum")
  elif sid.endswith('104_106.s12'):
   prefix,_=old.split('stored = ',1)
   scaffold=prefix+'# Select the transformation and acceptance callables.\n'
   tail='\n# Supplied equivalent eager and lazy traversal templates: leave unchanged.\nstored = [transform(value) for value in values if accept(value)]\nlazy = (transform(value) for value in values if accept(value))\n'
   wrong='transform = positive\naccept = double\n';right='transform = double\naccept = positive\n'
   prompt='Keep the helpers, inputs, and supplied comprehension/generator templates unchanged. Replace only the transform and accept assignments: bind transform to double and accept to positive, matching map(double, filter(positive, values)). stored must be the materialized transformed positive values in input order; lazy must be a generator yielding the same values without materializing a list at creation.'
  elif sid.endswith('107_109.s03'):
   prefix,cls=old.split('import unittest\n\nclass CostTests',1)
   prefix=prefix.replace('expected_cost = supplied_expected_cost\n','')
   scaffold=prefix+'# Select the expected value for the supplied equality assertion.\n'
   tail='\n# Supplied unittest module scaffold: leave unchanged.\nimport unittest\nif True:\n    class CostTests'+''.join('\n    '+line if line else '\n' for line in cls.split('\n')[1:])
   # Retain the class declaration suffix from the source, not hand-typed.
   tail=tail.replace('class CostTests\n','class CostTests'+cls.split('\n',1)[0]+'\n',1)
   wrong='expected_cost = None\n';right='expected_cost = supplied_expected_cost\n'
   prompt='The unittest import, TestCase subclass, and named equality, truth, and expected-exception checks are supplied as scaffold. Replace only the expected_cost assignment so it uses supplied_expected_cost. Keep the helper, scaffold, and inputs unchanged. The equality check must enforce the supplied normal-case cost; the truth check and the cost(-1) call inside assertRaises must remain intact. Do not add a test runner.'
  elif sid.endswith('107_109.s13'):
   prefix,cls=old.split('# Complete only setUp',1)
   classcode='# Complete only setUp'+cls
   classcode=classcode.replace('self.addCleanup(release)','self.addCleanup(cleanup_action)')
   scaffold=prefix+'# Choose a cleanup callable without calling it.\n'
   tail='\n'+classcode
   wrong='cleanup_action = acquire\n';right='cleanup_action = release\n'
   prompt='The acquisition, setUp initialization, and test methods are supplied as scaffold. Replace only cleanup_action = acquire with an assignment binding cleanup_action to release, without calling release. Keep the scaffold and inputs unchanged. setUp registers that callable immediately after acquisition and creates a fresh quantities list. Release must occur after normal completion, test failure, and setup failure after registration; one test\'s mutation must not affect another\'s list.'
  else:
   prefix,body=old.split('try:\n',1)
   scaffold=prefix+'# Supplied rejecting converter: leave unchanged.\nif True:\n    def supplied_reject(text):\n        return -1\n# Choose the safe numeric converter.\n'
   tail='\n# Supplied validation and conversion-error handling: leave unchanged.\ntry:\n'+body.replace('int(text)','convert_text(text)')
   wrong='convert_text = supplied_reject\n';right='convert_text = int\n'
   prompt='Replace only the convert_text assignment so it refers to int, not supplied_reject. Do not call the converter in this assignment. Keep text, quantity, the rejected proposal, and the supplied validation/try-except scaffold unchanged. The parser must produce a nonnegative integer quantity for valid text, and quantity = None for malformed or negative text, without executing the text.'
  tail=locals().get('tail','') if not sid.endswith('100_103.s06') else ''
  newstarter=scaffold+wrong+tail;solution=scaffold+right+tail
  ast.parse(newstarter);ast.parse(solution)
  pub['workspace']['files'][0]['content']=newstarter
  pub['prompt']=prompt;i['grading']['solution_files'][0]['content']=solution
  changed.append(sid)
  tail=''
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('Patched',len(changed),*changed,sep='\n')
