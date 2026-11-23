import json, copy, re
from pathlib import Path
p=Path('batches/final_batch_learn_python.region.03/interactions.json')
d=json.loads(p.read_text()); original=copy.deepcopy(d)
ix={e['step_id']:e['interaction'] for t in d['tiles'] for e in t['interactions']}
changed=[]
def replace_task(tile, step, prompt, start, end, starter, solution):
    sid=f'learn_python.tile.{tile}.{step}'; x=ix[sid]
    x['public']['prompt']=prompt
    for f, new in [(x['public']['workspace']['files'][0],starter),(x['grading']['solution_files'][0],solution)]:
        s=f['content']; a=s.index(start); b=s.index(end,a) if end else len(s)
        f['content']=s[:a]+new+s[b:]
    changed.append(sid)
marker='# Supplied candidate implementations; inspect but do not edit this block.\n'
replace_task('051_053','s10',
 'Complete read_quantity(text) using try and finally. Return int(text.read()) from try and call text.close() in finally. Do not return from finally. Keep the fixtures and harness unchanged.',
 marker,'# Instructor harness:',
 'def read_quantity(text):\n    # Complete the body using try and finally.\n    pass\n\n',
 'def read_quantity(text):\n    try:\n        return int(text.read())\n    finally:\n        text.close()\n\n')
replace_task('054_055','s09',
 'Complete make_counter: initialize count from initial_count, define advance using nonlocal count, increment and return count, then return advance. Keep counter and other’s separate factory calls unchanged.',
 marker,'counter = make_counter()',
 'def make_counter():\n    # Complete the stateful factory and its nested advance function.\n    pass\n\n',
 'def make_counter():\n    count = initial_count\n    def advance():\n        nonlocal count\n        count = count + 1\n        return count\n    return advance\n\n')
replace_task('056_056','s03',
 "Assign output by joining base with the relative child name 'orders.csv' using /. Keep base_directory and base unchanged; do not use an absolute child name or perform filesystem operations.",
 '# Candidate paths;', 'print(output)',
 'output = None\n', 'output = base / "orders.csv"\n')
replace_task('057_059','s04',
 "Complete cost so negative quantities raise ValueError('quantity must be nonnegative') and nonnegative quantities return quantity * 4. Keep all input variables and the harness unchanged.",
 marker,'# Instructor harness;',
 'def cost(quantity):\n    # Complete the argument check and calculation.\n    pass\n\n',
 'def cost(quantity):\n    if quantity < 0:\n        raise ValueError("quantity must be nonnegative")\n    return quantity * 4\n\n')
replace_task('060_060','s05',
 'Complete add_label: create labels = [] only when labels is None, append label, and return labels. Preserve caller-supplied lists and keep the probes unchanged.',
 marker,'# Instructor probes;',
 'def add_label(label, labels=None):\n    # Complete the None guard, append, and return.\n    pass\n\n',
 'def add_label(label, labels=None):\n    if labels is None:\n        labels = []\n    labels.append(label)\n    return labels\n\n')
# Reuse the original try body and recovery statements verbatim.
s=ix['learn_python.tile.063_064.s04']['public']['workspace']['files'][0]['content']
block=s[s.index('    def specific_first():'):s.index('    def broad_first():')]
block='\n'.join(line[4:] if line.startswith('    ') else line for line in block.splitlines()).rstrip()+'\n\n'
block=block.replace('def specific_first():','def recover():')
replace_task('063_064','s04',
 'Complete the two except headers so FileNotFoundError is handled first and OSError second. Do not change either print statement or the raised exception.',
 marker,'recover()\n',
 block.replace('except FileNotFoundError:', 'except ____:').replace('except OSError:', 'except ____:'),block)
# Preserve target's exact supplied definition, including its surrounding block.
s=ix['learn_python.tile.065_065.s06']['public']['workspace']['files'][0]['content']
target=s[s.index('if True:'):s.index('    def pass_through')].rstrip()+'\n\n'
replace_task('065_065','s06',
 'Write wrapper(*args, **kwargs) and return target(*args, **kwargs), without adding a price argument. Preserve target.',
 marker,None,
 '# Supplied target; leave unchanged.\n'+target+'def wrapper(*args, **kwargs):\n    # Complete argument forwarding.\n    pass\n',
 '# Supplied target; leave unchanged.\n'+target+'def wrapper(*args, **kwargs):\n    return target(*args, **kwargs)\n')
# Advisory edits: the solutions keep the same behavior and tests/answer keys.
s=ix['learn_python.tile.054_055.s04']['public']['workspace']['files'][0]['content']
helpers=s[s.index('if True:'):s.index('    def apply_supplied')].rstrip()+'\n\n'
replace_task('054_055','s04',
 'Complete apply(operation, value) with return operation(value). Assign chosen to double without calling it. Keep double, increment, and input_value unchanged. The checker checks chosen identity and apply with both supplied callables.',
 marker,None,
 '# Supplied transformations; leave unchanged.\n'+helpers+'def apply(operation, value):\n    # Return the result of invoking operation with value.\n    pass\n\nchosen = None\n',
 '# Supplied transformations; leave unchanged.\n'+helpers+'def apply(operation, value):\n    return operation(value)\n\nchosen = double\n')
replace_task('061_062','s04',
 'Complete label_key(record) with return record["label"].lower(), then assign ordered = sorted(records, key=label_key). Keep original text, quantities and records unchanged. Equal lowercase labels must retain input order. The checker reads ordered, records, and list identity.',
 marker,None,
 'def label_key(record):\n    # Return the lowercase label as the sorting key.\n    pass\n\nordered = None\n',
 'def label_key(record):\n    return record["label"].lower()\n\nordered = sorted(records, key=label_key)\n')
replace_task('061_062','s07',
 'Write chosen_key = lambda pair: pair[1], followed by ordered = sorted(pairs, key=chosen_key), to sort in ascending quantity order. Keep pairs unchanged. The checker reads ordered.',
 'label_key = lambda pair:',None,
 'chosen_key = None\nordered = None\n',
 'chosen_key = lambda pair: pair[1]\nordered = sorted(pairs, key=chosen_key)\n')
# The s06 introduction lives in screens.json, another stage's frozen artifact:
# do not edit it. Add the requested introductory wording to this interaction only.
sid='learn_python.tile.051_053.s06'
ix[sid]['public']['prompt']='Predict the failure point, skipped statement and resumption point, then run the unchanged demonstration to confirm the flow. '+ix[sid]['public']['prompt']
changed.append(sid)
# Confirm changes are confined to the findings and preserve every test/key,
# measures, constraints, feedback, and unrelated interaction.
for t,old_t in zip(d['tiles'],original['tiles']):
 for e,old_e in zip(t['interactions'],old_t['interactions']):
  x=e['interaction']; old=old_e['interaction']
  if e['step_id'] not in changed: assert e==old_e
  else:
   assert x['grading']['tests']==old['grading']['tests']
   for k in x:
    if k not in ('public','grading'): assert x[k]==old[k]
   assert x['public']['constraints']==old['public']['constraints']
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Patched',len(changed),'interactions; preserved tests/keys and constraints.')
print('Interactions',sum(len(t['interactions']) for t in d['tiles']),'tiles',len(d['tiles']))
