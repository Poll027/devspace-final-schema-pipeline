import json
from pathlib import Path

b = Path('batches/final_batch_mle.region.data_readiness')
p = b / 'interactions.json'
doc = json.loads(p.read_text())
item = next(i for t in doc['tiles'] for i in t['interactions'] if i['step_id'] == 'mle.tile.001_003.s05')
ix = item['interaction']
# The practice allows tuples, but not dictionary literals. Preserve the
# validator, boundary assertions, fixture inputs, and every tested value.
solution = ix['grading']['solution_files'][0]
old = "return {'accepted': True, 'array': a, 'rank': a.ndim, 'shape': a.shape, 'dtype': a.dtype}"
assert old in solution['content']
solution['content'] = solution['content'].replace(old, 'return (True, a, a.ndim, a.shape, a.dtype)')
solution['content'] = solution['content'].replace("return {'accepted': False}", 'return (False,)')
solution['content'] = solution['content'].replace("== {'accepted': False}", '== (False,)')
old_prompt = 'Define verify(fixture) to return {accepted, array, rank, shape, dtype} for valid inputs and {accepted: False} for ValueError.'
assert old_prompt in ix['public']['prompt']
ix['public']['prompt'] = ix['public']['prompt'].replace(old_prompt, 'Define verify(fixture) to return a tuple in the order (accepted, array, rank, shape, dtype) for valid inputs and the one-item tuple (False,) for ValueError.')
for test in ix['grading']['tests']:
    expected = test['spec']['expected']
    assert isinstance(expected, dict) and 'accepted' in expected
    test['spec']['expected'] = [expected[k] for k in ('accepted', 'array', 'rank', 'shape', 'dtype')] if expected['accepted'] else [expected['accepted']]
p.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + '\n')
print('Patched one interaction; six expected structures converted from existing keyed values; constraints unchanged.')
