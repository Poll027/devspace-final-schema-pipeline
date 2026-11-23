import ast
import copy
import json
import shlex
from pathlib import Path

batch = Path('batches/final_batch_implementation')
path = batch / 'interactions.json'
data = json.loads(path.read_text())
before = copy.deepcopy(data)
ix = data['tiles'][10]['interactions'][3]['interaction']
assert ix['grading']['tests'] == [] and ix['grading']['solution_files'] == []
command = ' '.join(ix['public']['constraints']['allowed_syntax'][:3])
workspace = ix['public']['workspace']
starter = next(f['content'] for f in workspace['files'] if f['path'] == workspace['entry'])
solution = starter.replace('launch_command = ""', 'launch_command = ' + repr(command))
assert solution != starter
# Execute the supplied command inspector to derive the preparation-only key.
module = ast.parse(solution)
function = next(n for n in module.body if isinstance(n, ast.FunctionDef) and n.name == 'inspect_launch')
namespace = {'shlex': shlex}
exec(compile(ast.Module(body=[function], type_ignores=[]), workspace['entry'], 'exec'), namespace)
expected = namespace['inspect_launch'](command)
assert namespace['inspect_launch']('') != expected
ix['grading']['solution_files'] = [{'path': workspace['entry'], 'content': solution}]
ix['grading']['tests'] = [{
    'test_id': ix['interaction_id'] + '.preparation_command',
    'kind': 'value_equals',
    'spec': {'expr': 'launch_config', 'expected': expected},
    'visible': True,
    'message_on_fail': 'Preparation command does not match the supplied import string and options. Passing this inspection is not evidence of Uvicorn startup; the required practice remains blocked as stated in the prompt.'
}]
# Repair scope: only the two arrays named in the schema finding may change.
comparison = copy.deepcopy(data)
comparison['tiles'][10]['interactions'][3]['interaction']['grading'] = copy.deepcopy(before['tiles'][10]['interactions'][3]['interaction']['grading'])
assert comparison == before
path.write_text(json.dumps(data, indent=2) + '\n')
from collections import Counter
counts = Counter(i['interaction']['type'] for t in data['tiles'] for i in t['interactions'])
print('Tiles:', len(data['tiles']), 'Interactions:', sum(counts.values()), dict(counts))
