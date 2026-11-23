import ast
import copy
import json
from pathlib import Path

B = Path('batches/final_batch_mle.region.production_operations')
p = B / 'interactions.json'
data = json.loads(p.read_text())
before = copy.deepcopy(data)
changes = []
for tile in data['tiles']:
    for item in tile['interactions']:
        sid = item['step_id']
        if sid not in {'mle.tile.086_089.s16', 'mle.tile.086_089.s21', 'mle.tile.091_094.s14'}:
            continue
        ix = item['interaction']
        solution = ix['grading']['solution_files'][0]['content']
        if sid.endswith('086_089.s16'):
            old = "    claim = coordinator.atomic_admit(event['run_key'], event['pipeline'])"
            assert solution.count(old) == 1
            replacement = "    # Supplied coordinator interface; bind the claim operation below.\n    atomic_claim = coordinator.atomic_admit\n    unavailable_claim = None\n    # TODO: bind claim_operation to the durable atomic interface.\n    claim_operation = atomic_claim\n    claim = claim_operation(event['run_key'], event['pipeline'])"
            solution = solution.replace(old, replacement)
            starter = solution.replace('    claim_operation = atomic_claim', '    claim_operation = unavailable_claim')
            prompt = "Complete the single marked binding inside admit: assign claim_operation to the supplied atomic_claim interface, not unavailable_claim. This interface reserves the run key, active pipeline slot and persisted job identity together. The supplied branches perform accepted/duplicate/busy handling, same-token recovery and terminal-only release. Keep that scaffolding, the fatal successful-step pipeline dependencies, safe YAML round trip and durable-state assertions unchanged. Run the existing concurrency, restart, unknown-response and completed-duplicate fixtures; tests inspect result and logical_job_counts. This exercise edits only the interface binding; the simulated clients and remaining implementation are supplied."
        elif sid.endswith('086_089.s21'):
            bindings = {
                'fpr_rule': 'negative_class_error_rate',
                'fnr_rule': 'positive_class_error_rate',
                'cost_rule': 'prevalence_weighted_error_cost',
                'quality_rule': 'declared_quality_limits',
                'passed_rule': 'all_required_gates',
            }
            for name, supplied in bindings.items():
                assert solution.count('def ' + name + '(') == 1
                solution = solution.replace('def ' + name + '(', 'def ' + supplied + '(')
            marker = 'def rates(model):'
            assert solution.count(marker) == 1
            bound = '# Supplied rule interfaces above; complete only these bindings.\nunavailable_rule = None\n' + '\n'.join(name + ' = ' + supplied for name, supplied in bindings.items()) + '\n\n\n'
            solution = solution.replace(marker, bound + marker)
            starter = solution
            for name, supplied in bindings.items():
                starter = starter.replace(name + ' = ' + supplied, name + ' = unavailable_rule')
            prompt = "Complete only the five marked rule-interface assignments. Bind fpr_rule to negative_class_error_rate (FP divided by FP+TN), fnr_rule to positive_class_error_rate (FN divided by FN+TP), cost_rule to prevalence_weighted_error_cost, quality_rule to declared_quality_limits, and passed_rule to all_required_gates. These supplied implementations use the shared cohort, declared probabilities and costs, incumbent-relative limits, required slice and compatibility checks, and exact artifact identity. Keep the supplied evaluator's undefined-empty-group handling, verdict recording and valid/boundary/failing/identity-mismatch assertions unchanged. Run the fixtures to produce result; tests inspect that variable. The learner edits the rule bindings, not the supplied calculations or evaluator."
        else:
            marker = "with open('guardrail.yaml', 'w') as h:\n    yaml.safe_dump(config, h)\n\nwith open('guardrail.yaml') as h:\n    resolved = yaml.safe_load(h)"
            assert solution.count(marker) == 1
            replacement = "# Supplied safe YAML interfaces; complete only the two bindings.\nsafe_serializer = yaml.safe_dump\nsafe_loader = yaml.safe_load\nunavailable_interface = None\nserialize = safe_serializer\ndeserialize = safe_loader\n\nwith open('guardrail.yaml', 'w') as h:\n    serialize(config, h)\n\nwith open('guardrail.yaml') as h:\n    resolved = deserialize(h)"
            solution = solution.replace(marker, replacement)
            starter = solution.replace('serialize = safe_serializer', 'serialize = unavailable_interface').replace('deserialize = safe_loader', 'deserialize = unavailable_interface')
            prompt = "Complete the two marked assignments: bind serialize to safe_serializer and deserialize to safe_loader. These supplied interfaces are yaml.safe_dump and yaml.safe_load. Keep the provided configuration, file-handling blocks, reloaded-field inspections and replay assertions unchanged. The configuration already contains the declared workload budget and period, threshold, existing notification topic and event binding, fixed authorized stop target, and runtime secret references. Run the supplied below-threshold, boundary and breach replay to produce result. Verify the safe round trip, fixed-target authorized response and credential non-disclosure through the existing assertions; budget notifications still do not impose a hard spending cap. Tests inspect result. Only the safe-interface bindings are learner edits."
        assert starter != solution
        ast.parse(starter)
        ast.parse(solution)
        ix['public']['workspace']['files'][0]['content'] = starter
        ix['grading']['solution_files'][0]['content'] = solution
        ix['public']['prompt'] = prompt
        assert ix['public']['constraints'] == next(e['interaction']['public']['constraints'] for t in before['tiles'] for e in t['interactions'] if e['step_id'] == sid)
        changes.append(sid)

# No answer keys, constraints, plan metadata or other interaction fields may change.
for old_tile, new_tile in zip(before['tiles'], data['tiles']):
    for old, new in zip(old_tile['interactions'], new_tile['interactions']):
        if old['step_id'] not in changes:
            assert old == new
        else:
            restored = copy.deepcopy(new)
            oi = old['interaction']; ri = restored['interaction']
            ri['public']['prompt'] = oi['public']['prompt']
            ri['public']['workspace']['files'][0]['content'] = oi['public']['workspace']['files'][0]['content']
            ri['grading']['solution_files'][0]['content'] = oi['grading']['solution_files'][0]['content']
            assert restored == old
p.write_text(json.dumps(data, indent=2) + '\n')
print(json.dumps({'patched_steps': changes, 'interactions': sum(len(t['interactions']) for t in data['tiles'])}))
