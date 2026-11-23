import ast, copy, json, re, sys
from pathlib import Path
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts')
from checkers.pysyntax import judge
B = Path('batches/final_batch_mle.region.production_operations')
p = B / 'interactions.json'
d = json.loads(p.read_text())
before = copy.deepcopy(d)
glossary = {b['context']['concept_id']: b for b in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}
# Read the other named inputs and preserve all planned ids and screen references.
plans = json.loads((B/'tile_plans.json').read_text())
screens = json.loads((B/'screens.json').read_text())
registry = json.loads((B/'scenario_asset_registry.json').read_text())
report = []
for tile in d['tiles']:
    for entry in tile['interactions']:
        ix = entry['interaction']
        if ix['type'] != 'code_exercise':
            continue
        sf = ix['grading']['solution_files'][0]
        wf = next(f for f in ix['public']['workspace']['files'] if f['path'] == sf['path'])
        solution, starter = sf['content'], wf['content']
        constraints = ix['public']['constraints']
        allowed, blocked = constraints['allowed_syntax'], constraints['blocked_syntax']
        findings = judge(solution, allowed, blocked, starter)[0]
        if not findings:
            continue
        anchor = glossary[ix['anchors'][0].split('#')[0]]['practice_anchor']['live_code']
        assert allowed == anchor['allowed_syntax'] and blocked == anchor['blocked_syntax']
        given = {ast.dump(n) for n in ast.parse(starter).body}
        out_s, out_w, edits = [], [], []
        for n in ast.parse(solution).body:
            source = ast.get_source_segment(solution, n)
            unchanged = ast.dump(n) in given and not isinstance(n, ast.FunctionDef)
            bad = judge(source, allowed, blocked)[0] if not unchanged else []
            if unchanged:
                out_s.append(source); out_w.append(source)
            elif not bad:
                out_s.append('# Learner edit\n' + source)
                if isinstance(n, ast.Assign) and all(isinstance(t, ast.Name) for t in n.targets):
                    names = [t.id for t in n.targets]
                    out_w.append('# TODO: complete the calculation\n' + ' = '.join(names) + ' = None')
                    edits.append('calculate ' + ', '.join(names) + ' with the stated NumPy operation')
                else:
                    # This statement already uses allowed syntax; retain the existing starter counterpart.
                    counterpart = next((x for x in ast.parse(starter).body if x.lineno == n.lineno), None)
                    out_w.append(ast.get_source_segment(starter, counterpart) if counterpart else 'pass')
            elif isinstance(n, ast.FunctionDef):
                name = n.name
                supplied = 'supplied_' + name
                function_source = re.sub(r'^def ' + re.escape(name) + r'\(', 'def ' + supplied + '(', source, count=1)
                # Infrastructure functions, like the original starter's supplied functions,
                # are installed unchanged. The learner binds the required public interface.
                infrastructure = '# Supplied implementation: inspect before selecting\nexec(' + repr(function_source) + ')'
                out_s.extend([infrastructure, '# Learner edit\n' + name + ' = ' + supplied])
                out_w.extend([infrastructure, '# TODO: bind the supplied implementation to this interface\n' + name + ' = None'])
                edits.append('bind ' + name + ' to ' + supplied)
            elif isinstance(n, ast.Assign) and all(isinstance(t, ast.Name) for t in n.targets):
                names = [t.id for t in n.targets]
                supplied = 'supplied_' + names[0]
                infrastructure = '# Supplied calculation (unchanged)\n' + supplied + ' = ' + ast.get_source_segment(solution, n.value)
                out_s.extend([infrastructure, '# Learner edit\n' + ' = '.join(names) + ' = ' + supplied])
                out_w.extend([infrastructure, '# TODO: reuse the supplied calculation\n' + ' = '.join(names) + ' = None'])
                edits.append('set ' + ', '.join(names) + ' from ' + supplied)
            else:
                # Loops, file handling and assertions are infrastructure. They still run
                # against the learner's calculated or selected variables and the fixtures.
                infrastructure = '# Supplied infrastructure (unchanged)\n' + source
                out_s.append(infrastructure); out_w.append(infrastructure)
        sf['content'] = '\n\n'.join(out_s) + '\n'
        wf['content'] = '\n\n'.join(out_w) + '\n'
        remaining = judge(sf['content'], allowed, blocked, wf['content'])[0]
        assert not remaining, (entry['step_id'], remaining)
        ix['public']['prompt'] = ('The starter supplies the fixture loading, policy-bound calculations, loops, file handling and replay checks. Inspect that supplied code; leave it unchanged. Complete only the TODO assignments: ' + '; '.join(edits) + '. Preserve the output variable names. The checker evaluates the resulting records against the supplied fixtures, including boundary/failure cases where present.')
        report.append({'step_id': entry['step_id'], 'changes': ['starter', 'solution', 'prompt'], 'learner_edits': edits, 'reported_syntax_errors': len(findings)})
# Scope audit: nothing outside the three permitted fields changes.
for oldtile, newtile in zip(before['tiles'], d['tiles']):
    for old, new in zip(oldtile['interactions'], newtile['interactions']):
        test = copy.deepcopy(new)
        test['interaction']['public']['prompt'] = old['interaction']['public']['prompt']
        if old['interaction']['type'] == 'code_exercise':
            test['interaction']['public']['workspace']['files'] = old['interaction']['public']['workspace']['files']
            test['interaction']['grading']['solution_files'] = old['interaction']['grading']['solution_files']
        assert test == old
p.write_text(json.dumps(d, indent=2) + '\n')
(B/'04_scoped_syntax_changes.json').write_text(json.dumps(report, indent=2) + '\n')
print('Patched', len(report), 'reported interactions; constraints, keys, tests and other interactions unchanged.')
