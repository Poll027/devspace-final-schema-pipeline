import ast
import copy
import json
from pathlib import Path

root = Path('batches/final_batch_learn_python.region.04')
path = root / 'interactions.json'
data = json.loads(path.read_text())
before = copy.deepcopy(data)
entry = next(e for t in data['tiles'] for e in t['interactions'] if e['step_id'] == 'learn_python.tile.080_083.s07')
interaction = entry['interaction']
message_names = ['invalid_row_message', 'missing_source_message', 'decoding_failed_message', 'parsing_failed_message']

def patch(content):
    prefix, region = content.split('# BEGIN LEARNER\n', 1)
    learner, suffix = region.split('# END LEARNER', 1)
    supplied = next(n.value for n in ast.parse(prefix).body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'supplied_invalid_row_message')
    assignments = {}
    lines = learner.splitlines(keepends=True)
    remove = set()
    for n in ast.parse(learner).body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in message_names:
            name = n.targets[0].id
            if name == 'invalid_row_message':
                assignments[name] = f'{name} = {ast.unparse(supplied)}\n'
            else:
                assignments[name] = ''.join(lines[n.lineno-1:n.end_lineno])
            remove.update(range(n.lineno-1, n.end_lineno))
    assert set(assignments) == set(message_names)
    old = f'supplied_invalid_row_message = {ast.unparse(supplied)}\n'
    assert old in prefix
    prefix = prefix.replace(old, ''.join(assignments[n] for n in message_names))
    learner = ''.join(line for index, line in enumerate(lines) if index not in remove).rstrip() + '\n'
    return prefix + '# BEGIN LEARNER\n' + learner + '# END LEARNER' + suffix

interaction['public']['workspace']['files'][0]['content'] = patch(interaction['public']['workspace']['files'][0]['content'])
interaction['grading']['solution_files'][0]['content'] = patch(interaction['grading']['solution_files'][0]['content'])
assert interaction['grading']['tests'] == next(e['interaction']['grading']['tests'] for t in before['tiles'] for e in t['interactions'] if e['step_id'] == entry['step_id'])
changed = [e['step_id'] for old_tile, tile in zip(before['tiles'], data['tiles']) for old_e, e in zip(old_tile['interactions'], tile['interactions']) if old_e != e]
assert changed == [entry['step_id']]
path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
print('Patched only', changed, ': supplied all four messages outside learner work; preserved tests.')
