import ast
import copy
import json
from pathlib import Path

B = Path(__file__).parent
P = B / 'interactions.json'
d = json.loads(P.read_text())
before = copy.deepcopy(d)
targets = {'mle.tile.086_089.s21', 'mle.tile.090_090.s05', 'mle.tile.091_094.s14'}
for tile in d['tiles']:
    for entry in tile['interactions']:
        sid = entry['step_id']
        if sid not in targets:
            continue
        ix = entry['interaction']
        ws = ix['public']['workspace']
        starter = ws['files'][0]
        solution = ix['grading']['solution_files'][0]
        if sid == 'mle.tile.090_090.s05':
            helper = next(f for f in ws['files'] if f['path'] == 'runbook_simulator.py')['content']
            old = "exec(compile(open('runbook_simulator.py').read(), 'runbook_simulator.py', 'exec'))"
            for f in (starter, solution):
                assert old in f['content']
                f['content'] = f['content'].replace(old, 'exec(' + repr(helper) + ')')
                f['content'] = f['content'].replace('# Load the readonly simulator into the supplied fixture namespace.', '# Supplied in-memory simulator; no external file is needed.')
        elif sid == 'mle.tile.086_089.s21':
            # Bind supplied formula/predicate interfaces with the only detected
            # construct permitted by this anchor: simple variable assignment.
            s = solution['content']
            nodes = ast.parse(s).body
            funcs = [n for n in nodes if isinstance(n, ast.FunctionDef)]
            assert [n.name for n in funcs] == ['rates', 'evaluate']
            original = s.splitlines(True)
            a, z = funcs[0].lineno - 1, funcs[-1].end_lineno
            functions = ''.join(original[a:z])
            rules = []
            replacements = []
            for fn, names in [('rates', ['fpr', 'fnr', 'cost']), ('evaluate', ['quality', 'passed'])]:
                node = next(n for n in funcs if n.name == fn)
                for name in names:
                    assignments = [n for n in ast.walk(node) if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == name]
                    chosen = assignments[-1]
                    expr = ast.get_source_segment(s, chosen.value)
                    args = {'fpr': 'model', 'fnr': 'model', 'cost': 'fpr, fnr', 'quality': 'cand, inc', 'passed': 'quality, candidate, incumbent, requested_identity'}[name]
                    rules.append('def supplied_' + name + '_rule(' + args + '):\n    return ' + expr + '\n')
                    replacements.append((ast.get_source_segment(s, chosen), name + ' = ' + name + '_rule(' + args + ')'))
            for old, new in replacements:
                assert old in functions
                functions = functions.replace(old, new)
            scaffold = 'exec(' + repr('\n'.join(rules) + '\n' + functions) + ')\n\n'
            start_bindings = '\n'.join(name + '_rule = None  # Bind the corresponding supplied rule.' for name in ['fpr','fnr','cost','quality','passed']) + '\n'
            solution_bindings = '\n'.join(name + '_rule = supplied_' + name + '_rule' for name in ['fpr','fnr','cost','quality','passed']) + '\n'
            # The surrounding fixtures, weights, assertions and result are untouched.
            tail = ''.join(original[z:])
            prefix = ''.join(original[:a]).replace('# Complete only the five marked expressions; retain the supplied function scaffold.', '# Supplied conditional-rate and gate interfaces; bind the five rule names below.')
            starter['content'] = prefix + scaffold + start_bindings + tail
            solution['content'] = prefix + scaffold + solution_bindings + tail
            ix['public']['prompt'] = 'Bind `fpr_rule`, `fnr_rule`, `cost_rule`, `quality_rule` and `passed_rule` to their corresponding supplied callable names (`supplied_fpr_rule`, `supplied_fnr_rule`, `supplied_cost_rule`, `supplied_quality_rule`, `supplied_passed_rule`). Read the supplied formulas and predicates: they calculate conditional rates and expected costs, reject undefined groups, enforce all declared gates and bind the verdict to the exact artifact and shared cohort. Keep fixtures, weights, assertions and result unchanged. The fixture checks cover valid, boundary and failing cases, including identity mismatch.'
        else:
            s = solution['content']
            node = next(n for n in ast.parse(s).body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == 'config')
            assert isinstance(node.value, ast.Dict)
            supplied, bindings, fields = [], [], []
            for key, value in zip(node.value.keys, node.value.values):
                name = key.value
                if name == 'response_step':
                    fields.append(repr(name) + ': response_step')
                    continue
                expr = ast.get_source_segment(s, value)
                supplied.append('supplied_' + name + ' = ' + expr)
                bindings.append((name, 'supplied_' + name))
                fields.append(repr(name) + ': ' + name)
            scaffold = '\n'.join(supplied) + '\n\n'
            mapping = 'config = {' + ', '.join(fields) + '}\n'
            original = s.splitlines(True)
            prefix = ''.join(original[:node.lineno-1])
            tail = ''.join(original[node.end_lineno:])
            for f, is_solution in [(starter, False), (solution, True)]:
                assignments = '\n'.join(name + ' = ' + (value if is_solution else 'None  # Complete using the corresponding supplied value.') for name, value in bindings) + '\n\n'
                f['content'] = prefix + scaffold + assignments + mapping + tail
            ix['public']['prompt'] = 'Complete the named configuration-value assignments (`workload_scope`, `budget_amount`, `period`, `threshold_ratio`, `notification_topic`, `response_pipeline`, `INSTANCE`, `ZONE`, `authorized_identity`, `secret_version_reference`, `secretEnv`, `event_binding`) by reusing each corresponding `supplied_` value. Inspect those supplied values against the declared policy. The supplied mapping then forms `config`; keep the fixed-target response step, safe YAML serialization/reload, resolved-field inspection and below-threshold/breach replay checks unchanged.'
# Scope audit: only named interaction workspace contents, solutions and prompts.
changes=[]
for old_tile,new_tile in zip(before['tiles'],d['tiles']):
    for old,new in zip(old_tile['interactions'],new_tile['interactions']):
        if old!=new:
            assert new['step_id'] in targets
            a,b=copy.deepcopy(old),copy.deepcopy(new)
            for e in (a,b):
                i=e['interaction']; i['public'].pop('prompt'); i['public']['workspace'].pop('files'); i['grading'].pop('solution_files')
            assert a==b
            changes.append(new['step_id'])
assert set(changes)==targets
P.write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps({'changed':changes,'interaction_count':sum(len(t['interactions']) for t in d['tiles'])}))
