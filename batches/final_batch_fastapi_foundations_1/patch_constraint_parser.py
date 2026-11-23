import json
from pathlib import Path
from tempfile import TemporaryDirectory
import os

p = Path('batches/final_batch_foundations_1/interactions.json')
d = json.loads(p.read_text())
i = next(s['interaction'] for t in d['tiles'] for s in t['interactions'] if s['step_id'] == 'tile_017.s05')
old_solution = i['grading']['solution_files'][0]['content']
parser = r'''def parse_declaration(declaration):
    # Restricted grammar: the four supplied columns followed by table constraints.
    invalid = dict.fromkeys(('primary_key', 'foreign_key', 'required_quantity',
                             'positive_quantity', 'default_unique', 'nullable_customer',
                             'nullable_external', 'distinct_null_policy'), False)
    match = re.fullmatch(r'\s*CREATE\s+TABLE\s+orders\s*\((.*)\)\s*;\s*', declaration, re.I | re.S)
    if match is None:
        return False, invalid
    entries = []
    start = depth = 0
    body = match.group(1)
    for position, character in enumerate(body):
        if character == '(':
            depth += 1
        elif character == ')':
            depth -= 1
            if depth < 0:
                return False, invalid
        elif character == ',' and depth == 0:
            entries.append(body[start:position].strip())
            start = position + 1
    entries.append(body[start:].strip())
    if depth != 0 or len(entries) < 4 or any(not entry for entry in entries):
        return False, invalid
    columns = [('identity', 'INTEGER'), ('customer_reference', 'INTEGER'),
               ('quantity', 'INTEGER'), ('external_reference', 'TEXT')]
    required = {}
    for entry, (name, kind) in zip(entries[:4], columns):
        column = re.fullmatch(name + r'\s+' + kind + r'(\s+NOT\s+NULL)?', entry, re.I)
        if column is None:
            return False, invalid
        required[name] = column.group(1) is not None
    patterns = {
        'primary_key': r'PRIMARY\s+KEY\s*\(\s*identity\s*\)',
        'foreign_key': r'FOREIGN\s+KEY\s*\(\s*customer_reference\s*\)\s*REFERENCES\s+customers\s*\(\s*identity\s*\)',
        'positive_quantity': r'CHECK\s*\(\s*quantity\s*>\s*0\s*\)',
        'default_unique': r'UNIQUE\s*\(\s*external_reference\s*\)',
        'non_distinct_unique': r'UNIQUE\s+NULLS\s+NOT\s+DISTINCT\s*\(\s*external_reference\s*\)'
    }
    constraints = set()
    for entry in entries[4:]:
        names = [name for name, pattern in patterns.items() if re.fullmatch(pattern, entry, re.I)]
        if len(names) != 1 or names[0] in constraints:
            return False, invalid
        constraints.add(names[0])
    if 'default_unique' in constraints and 'non_distinct_unique' in constraints:
        return False, invalid
    flags = {
        'primary_key': 'primary_key' in constraints,
        'foreign_key': 'foreign_key' in constraints,
        'required_quantity': required['quantity'],
        'positive_quantity': 'positive_quantity' in constraints,
        'default_unique': 'default_unique' in constraints,
        'nullable_customer': not required['customer_reference'],
        'nullable_external': not required['external_reference'],
        'distinct_null_policy': 'non_distinct_unique' not in constraints
    }
    return True, flags

def inspect_constraint(candidate, declaration=None):
    if declaration is None:
        lines = open('main.py').read().splitlines()
        declaration = '\n'.join(line[len('# SQL '):] for line in lines if line.startswith('# SQL '))
    valid, flags = parse_declaration(declaration)
    if not valid:
        return {'declared_constraints': flags, 'accepted': False}
'''
prefixed = ''.join('# PY ' + line + '\n' for line in parser.splitlines())
for file in (i['public']['workspace']['files'][0], i['grading']['solution_files'][0]):
    source = file['content']
    start = source.index('# PY def inspect_constraint(candidate):')
    end = source.index('# PY     identity, customer, quantity, external = candidate', start)
    file['content'] = source[:start] + prefixed + source[end:]

solution = i['grading']['solution_files'][0]['content']
declaration = '\n'.join(line[len('# SQL '):] for line in solution.splitlines() if line.startswith('# SQL '))
mutations = []
# Each separator is independently required, including between columns and constraints.
for n in range(declaration.count(',')):
    positions = [pos for pos, ch in enumerate(declaration) if ch == ',']
    pos = positions[n]
    mutations.append((f'missing_separator_{n + 1}', declaration[:pos] + declaration[pos + 1:]))
mutations.extend([
    ('unclosed_table', declaration.replace(');', ';')),
    ('unclosed_constraint', declaration.replace('CHECK (quantity > 0)', 'CHECK (quantity > 0')),
    ('constraint_outside', declaration.replace(',\n    UNIQUE (external_reference)', '') + '\nUNIQUE (external_reference)'),
    ('missing_semicolon', declaration.rstrip().removesuffix(';')),
])
candidate = i['grading']['tests'][0]['spec']['args'][0]
with TemporaryDirectory() as folder:
    previous = os.getcwd()
    os.chdir(folder)
    try:
        Path('main.py').write_text(solution)
        namespace = {}
        exec(solution, namespace)
        # Existing expected answers remain unchanged and must still match.
        for test in i['grading']['tests']:
            spec = test['spec']
            assert namespace[spec['function']](*spec['args']) == spec['expected'], test['test_id']
        for name, malformed in mutations:
            expected = namespace['inspect_constraint'](candidate, malformed)
            assert not expected['accepted'] and not any(expected['declared_constraints'].values())
            i['grading']['tests'].append({
                'test_id': name,
                'kind': 'function_call',
                'message_on_fail': 'Reject malformed declarations before evaluating row constraints: check separators, balanced parentheses, and the declaration boundary.',
                'spec': {'function': 'inspect_constraint', 'args': [candidate, malformed], 'expected': expected}
            })
            # Also prove the real editor source path rejects the same malformed SQL.
            malformed_source = '\n'.join('# SQL ' + line for line in malformed.splitlines()) + '\n' + solution[solution.index('# PY '):]
            Path('main.py').write_text(malformed_source)
            assert namespace['inspect_constraint'](candidate) == expected
        Path('main.py').write_text(i['public']['workspace']['files'][0]['content'])
        starter_ns = {}
        exec(Path('main.py').read_text(), starter_ns)
        assert any(starter_ns[test['spec']['function']](*test['spec']['args']) != test['spec']['expected'] for test in i['grading']['tests'][:10])
    finally:
        os.chdir(previous)
p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
print('Patched tile_017.s05 checker in starter and solution; added', len(mutations), 'negative tests; original 10 answers unchanged.')
print('Interaction count:', sum(len(t['interactions']) for t in d['tiles']))
