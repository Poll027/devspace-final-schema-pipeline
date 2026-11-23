import ast, copy, json
from pathlib import Path
B = Path('batches/final_batch_mle.region.production_operations')
p = B / 'interactions.json'
d = json.loads(p.read_text())
before = copy.deepcopy(d)
glossary = json.loads((B / 'inputs/path_glossary_bundle.json').read_text())
anchors = {b['context']['concept_id']: b['practice_anchor']['live_code'] for b in glossary['bundles'] if b.get('practice_anchor', {}).get('live_code')}
changed = []
for tile in d['tiles']:
    for entry in tile['interactions']:
        sid = entry['step_id']
        if sid not in {'mle.tile.086_089.s16', 'mle.tile.086_089.s21'}:
            continue
        i = entry['interaction']
        concept = i['anchors'][0].split('#')[0]
        lists = anchors[concept]
        assert i['public']['constraints'] == {k: lists[k] for k in ('allowed_syntax', 'blocked_syntax')}
        solution = i['grading']['solution_files'][0]['content']
        lines = solution.splitlines(keepends=True)
        # Supplied infrastructure functions are identical in starter and solution.
        # Keep their source from the existing solution, not manually recreated.
        for node in reversed(ast.parse(solution).body):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                body = ''.join(lines[node.lineno-1:node.end_lineno])
                lines[node.lineno-1:node.end_lineno] = ['exec(' + repr(body) + ')\n']
        solution = ''.join(lines)
        starter = solution
        if sid.endswith('s16'):
            starter = starter.replace('statuses = loaded_statuses', 'statuses = None', 1)
            prompt = 'The supplied admission function, durable clients, pipeline wiring and invariant assertions are scaffolding. Complete only `statuses = ...`: reuse `loaded_statuses`, the safely loaded response policy, so busy requests defer and completed keys return the completed response. Keep the coordinator, executor, dependencies and assertions unchanged. The supplied fixture runner writes `result`, checking same-key and different-key contention, restart recovery, unknown launch responses, terminal release, completed duplicates, and accepted/rejected fatal gates; build.yaml must survive the supplied safe YAML round trip.'
        else:
            for name in ('false_positive_weight', 'false_negative_weight'):
                starter = starter.replace(name + ' = supplied_' + name, name + ' = None', 1)
            prompt = 'The imports, conditional-rate calculations, incumbent-relative gate, identity-bound decision record and fixture assertions are supplied scaffolding. Complete only the assignments to `false_positive_weight` and `false_negative_weight` by reusing the corresponding supplied weights, which combine deployment class probability and error cost. Do not swap the two weights or hard-code them. Keep the supplied evaluator and assertions unchanged. The fixture runner writes `result`: records contain both models\' rates and expected costs, exact candidate identity, and the conjunctive verdict; it checks valid, inclusive-boundary and failing cases, including undefined empty groups and identity mismatch, without protected test observations.'
        assert starter != solution
        i['public']['workspace']['files'][0]['content'] = '# Complete only the marked policy assignments; the remaining code is supplied scaffolding.\n' + starter
        i['grading']['solution_files'][0]['content'] = '# Complete only the marked policy assignments; the remaining code is supplied scaffolding.\n' + solution
        i['public']['prompt'] = prompt
        changed.append(sid)
for old_t, new_t in zip(before['tiles'], d['tiles']):
    for old, new in zip(old_t['interactions'], new_t['interactions']):
        if old['step_id'] not in changed:
            assert old == new
        else:
            a, b = copy.deepcopy(old), copy.deepcopy(new)
            for e in (a,b):
                e['interaction']['public'].pop('prompt')
                e['interaction']['public']['workspace']['files'][0].pop('content')
                e['interaction']['grading']['solution_files'][0].pop('content')
            assert a == b
p.write_text(json.dumps(d, indent=2) + '\n')
print(json.dumps({'patched_steps': changed, 'interaction_count': sum(len(t['interactions']) for t in d['tiles'])}))
