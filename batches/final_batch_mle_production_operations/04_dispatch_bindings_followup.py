import ast
import json
from pathlib import Path
B = Path('batches/final_batch_mle.region.production_operations')
p = B / 'interactions.json'
d = json.loads(p.read_text())
for tile in d['tiles']:
    for item in tile['interactions']:
        sid = item['step_id']
        if sid not in {'mle.tile.086_089.s16', 'mle.tile.086_089.s21'}:
            continue
        ix = item['interaction']
        solution = ix['grading']['solution_files'][0]['content']
        if sid.endswith('s16'):
            old = "    # Supplied coordinator interface; bind the claim operation below.\n    atomic_claim = coordinator.atomic_admit\n    unavailable_claim = None\n    # TODO: bind claim_operation to the durable atomic interface.\n    claim_operation = atomic_claim\n    claim = claim_operation(event['run_key'], event['pipeline'])"
            assert solution.count(old) == 1
            solution = solution.replace(old, "    claim = claim_operation(coordinator, event['run_key'], event['pipeline'])")
            tree = ast.parse(solution)
            func = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'admit')
            source = ast.get_source_segment(solution, func)
            helper = "def atomic_claim(coordinator, run_key, pipeline):\n    return coordinator.atomic_admit(run_key, pipeline)"
            binding = "# Supplied durable operation and admission branches; edit only the binding.\nexec(" + repr(helper) + ")\nunavailable_claim = None\nclaim_operation = atomic_claim\n\nexec(" + repr(source) + ")"
            solution = solution.replace(source, binding)
            starter = solution.replace('claim_operation = atomic_claim', 'claim_operation = unavailable_claim')
            ix['public']['prompt'] = ix['public']['prompt'].replace('single marked binding inside admit', 'single marked top-level binding used by admit')
        else:
            # Supplied callable implementations follow the same explicit fixture-scaffolding
            # form already used for the clients; none of their internals is learner edited.
            tree = ast.parse(solution)
            for func in reversed([n for n in tree.body if isinstance(n, ast.FunctionDef)]):
                source = ast.get_source_segment(solution, func)
                solution = solution.replace(source, '# Supplied callable implementation (leave unchanged).\nexec(' + repr(source) + ')', 1)
            bindings = {'fpr_rule': 'negative_class_error_rate', 'fnr_rule': 'positive_class_error_rate', 'cost_rule': 'prevalence_weighted_error_cost', 'quality_rule': 'declared_quality_limits', 'passed_rule': 'all_required_gates'}
            starter = solution
            for name, supplied in bindings.items():
                starter = starter.replace(name + ' = ' + supplied, name + ' = unavailable_rule')
        ast.parse(solution); ast.parse(starter)
        ix['public']['workspace']['files'][0]['content'] = starter
        ix['grading']['solution_files'][0]['content'] = solution
p.write_text(json.dumps(d, indent=2) + '\n')
