import ast
import copy
import json
import sys
from pathlib import Path
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts')
from checkers import pysyntax
B = Path('batches/final_batch_mle.region.data_readiness')
p = B / 'interactions.json'
data = json.loads(p.read_text())
glossary = {x['context']['concept_id']: x for x in json.loads((B / 'inputs/path_glossary_bundle.json').read_text())['bundles']}
changes = []
for tile in data['tiles']:
    for entry in tile['interactions']:
        ix = entry['interaction']
        if ix['type'] != 'code_exercise':
            continue
        public = ix['public']
        solution_file = ix['grading']['solution_files'][0]
        starter_file = next(f for f in public['workspace']['files'] if f['path'] == solution_file['path'])
        solution, starter = solution_file['content'], starter_file['content']
        cons = public['constraints']
        violations = pysyntax.judge(solution, cons['allowed_syntax'], cons['blocked_syntax'], starter)[0]
        if not violations:
            continue
        anchor = glossary[ix['measures'][0]['concept_id']]['practice_anchor']
        assert cons['allowed_syntax'] == anchor['live_code']['allowed_syntax']
        assert cons['blocked_syntax'] == anchor['live_code']['blocked_syntax']
        # Unsupported function bodies are supplied, not learner-authored. The
        # learner's edit is an assignment wiring each supplied routine into the
        # existing evaluation harness. No constraints, keys, or tests change.
        tree = ast.parse(solution)
        given = {ast.dump(n) for n in ast.parse(starter).body}
        bindings = []
        for node in tree.body:
            if ast.dump(node) in given:
                continue
            if isinstance(node, ast.If) and len(node.body) == 1 and isinstance(node.body[0], ast.FunctionDef):
                fn = node.body[0]
                original = fn.name
                fn.name = 'supplied_' + original
                bindings.append((original, fn.name))
        assert bindings, entry['step_id']
        # All non-binding statements are identical supplied scaffolding. Keeping
        # constants and imports unchanged preserves execution and mutation inputs.
        shared = ast.unparse(tree) + '\n'
        header = '# Supplied routines and checks below are scaffolding. Edit only the final wiring assignments.\n'
        new_solution = header + shared + '\n# Learner wiring\n' + ''.join(f'{name} = {supplied}\n' for name, supplied in bindings)
        new_starter = header + shared + '\n# Learner wiring: replace each placeholder with the appropriate supplied routine name.\n' + ''.join(f'{name} = ...\n' for name, supplied in bindings)
        # Existing assignment exercises (e.g. the summary operation aliases) must
        # remain incomplete in the starter rather than silently supplying them.
        starter_tree = ast.parse(starter)
        for node in tree.body:
            if isinstance(node, ast.Assign) and ast.dump(node) not in given:
                # Retain the original starter's value for an existing editable binding.
                match = next((n for n in starter_tree.body if isinstance(n, ast.Assign) and ast.dump(ast.Tuple(elts=n.targets, ctx=ast.Load())) == ast.dump(ast.Tuple(elts=node.targets, ctx=ast.Load()))), None)
                if match is not None:
                    old_line = ast.unparse(node)
                    new_starter = new_starter.replace(old_line + '\n', ast.unparse(match) + '\n')
        assert not pysyntax.judge(new_solution, cons['allowed_syntax'], cons['blocked_syntax'], new_starter)[0], entry['step_id']
        starter_file['content'] = new_starter
        solution_file['content'] = new_solution
        previous = public['prompt']
        public['prompt'] = ('The implementation and boundary checks are supplied as scaffolding. Complete only the final wiring assignments: bind ' + ', '.join(name for name, _ in bindings) + ' to the corresponding supplied routine names (use names, not calls). Keep the supplied bodies unchanged. Review their behavior against this requirement: ' + previous)
        changes.append({'step_id': entry['step_id'], 'bindings': [n for n, _ in bindings], 'errors_before': len(violations)})
p.write_text(json.dumps(data, indent=2) + '\n')
(B / 'scratch/patch_reported_syntax_changes.json').write_text(json.dumps(changes, indent=2) + '\n')
print(json.dumps(changes, indent=2))
