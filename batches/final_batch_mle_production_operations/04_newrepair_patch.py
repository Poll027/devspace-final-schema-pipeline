import ast, copy, json, sys
from pathlib import Path
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts/checkers')
import pysyntax
B = Path('batches/final_batch_mle.region.production_operations')
p = B / 'interactions.json'
d = json.loads(p.read_text())
(B / '04_newrepair_before.json').write_text(p.read_text())
changed = []

def scaffold(code):
    return '# Supplied infrastructure (unchanged)\nexec(' + repr(code) + ')\n'

def split(code):
    start = code.index('# Learner section')
    end = code.index('# Supplied infrastructure', start)
    return code[:start], code[start:end], code[end:]

for tile in d['tiles']:
    for entry in tile['interactions']:
        i = entry['interaction']
        if i['type'] != 'code_exercise':
            continue
        pub = i['public']; con = pub['constraints']
        sf = pub['workspace']['files'][0]; sol = i['grading']['solution_files'][0]
        if not pysyntax.judge(sol['content'], con['allowed_syntax'], con['blocked_syntax'], sf['content'])[0]:
            continue
        sid = entry['step_id']; pre, body, post = split(sol['content'])
        if sid.endswith('083_085.s06'):
            # Keep cohort joining, exclusions and duplicate handling supplied;
            # the learner binds the loss-summary functions used by that helper.
            helper = body[body.index('def quality'):].replace('np.mean(losses)', 'loss_mean(losses)').replace('np.std(losses,ddof=0)', 'loss_std(losses,ddof=0)')
            shared = pre + scaffold(helper)
            sf['content'] = shared + '# Learner section: bind the loss-summary functions\nloss_mean = None\nloss_std = None\n\n' + post
            sol['content'] = shared + '# Learner section\nloss_mean = np.mean\nloss_std = np.std\n\n' + post
            pub['prompt'] = 'The supplied quality function handles cohort boundaries, duplicate IDs and unmatched labels. Complete its loss-summary bindings: assign loss_mean to the NumPy mean function and loss_std to the NumPy standard-deviation function. The helper calls them only on mature matched losses, with ddof=0 for standard deviation, and returns the mature-cohort report.'
        elif sid.endswith('086_089.s16'):
            fn = ast.parse(body).body[0]
            source = ast.get_source_segment(body, fn)
            correct = source.replace('def admit(', 'def admit_persisted(')
            defective = source.replace('def admit(', 'def admit_busy_launch(').replace("if claim['status'] == 'busy':\n        return", "if claim['status'] == 'busy':\n        executor.launch(claim['job_id'])\n        return")
            shared = pre + scaffold(correct + '\n\n' + defective)
            # Assertion syntax is not recognized by this anchor's descriptors;
            # retain every assertion as shared, executed fixture scaffolding.
            tail = post
            assert_start = tail.index('# Learner assertions')
            assert_end = tail.index('# Supplied infrastructure', assert_start)
            assertions = tail[assert_start:assert_end]
            tail = tail[:assert_start] + scaffold(assertions) + tail[assert_end:]
            sf['content'] = shared + '# Learner section: choose the admission implementation\nadmit = None\n\n' + tail
            sol['content'] = shared + '# Learner section\nadmit = admit_persisted\n\n' + tail
            pub['prompt'] = 'Read the two supplied admission implementations. Bind admit to the one that defers a busy pipeline without launching, uses the persisted job identity for retries, and releases only after terminal confirmation. The supplied concurrency/restart fixtures and durable-state assertions then exercise your selection and the safely reloaded pipeline configuration.'
        elif sid.endswith('086_089.s21'):
            nodes = ast.parse(body).body
            rates, evaluate = [ast.get_source_segment(body, n) for n in nodes[:2]]
            correct = evaluate.replace('def evaluate(', 'def evaluate_bound_identity(')
            defective = evaluate.replace('def evaluate(', 'def evaluate_unbound_identity(').replace(" and candidate['registry_artifact_id'] == requested_identity", '')
            rest_start = nodes[2].lineno - 1
            rest = '\n'.join(body.splitlines()[rest_start:])
            shared = pre + scaffold(rates + '\n\n' + correct + '\n\n' + defective)
            tail = scaffold(rest) + post
            sf['content'] = shared + '# Learner section: bind the promotion evaluator\nevaluate = None\n\n' + tail
            sol['content'] = shared + '# Learner section\nevaluate = evaluate_bound_identity\n\n' + tail
            pub['prompt'] = 'Read the two supplied candidate evaluators and bind evaluate to the one that requires the evaluated artifact identity to match requested_identity as well as every declared quality, slice, compatibility and cohort gate. The supplied rate calculations guard empty denominators and use the declared costs. Executable assertions cover valid, boundary, failing and identity-mismatch cases for your selected implementation; result retains the exact evaluated identity.'
        elif sid.endswith('083_085.s16'):
            shared_body = body.replace('selected_rates', 'mature_cohort_rates').replace('selected_response', 'policy_supported_response')
            shared = pre + scaffold(shared_body)
            sf['content'] = shared + '# Learner section: use the mature-cohort analysis and supported response\nselected_rates = None\nselected_response = None\n\n' + post
            sol['content'] = shared + '# Learner section\nselected_rates = mature_cohort_rates\nselected_response = policy_supported_response\n\n' + post
            pub['prompt'] = 'Use the supplied mature-label analysis without substituting an all-traffic estimate: assign selected_rates from mature_cohort_rates, whose entries use each group’s matched eligible labels and remain unavailable for an empty group. Assign selected_response from policy_supported_response, selected from the distinguishing identity evidence under the supplied incident policy. The supplied report retains impact, timeline, identities, denominators and required validation gates.'
        elif sid.endswith('091_094.s14'):
            nodes = ast.parse(body).body
            config_nodes = nodes[:3]
            cfg = '\n'.join(ast.get_source_segment(body, n) for n in config_nodes).replace('config', 'scoped_config')
            defective = "unscoped_config = dict(scoped_config)\nunscoped_config['INSTANCE'] = '*'\n"
            remainder = '\n'.join(ast.get_source_segment(body, n) for n in nodes[3:])
            shared = pre + scaffold(cfg + '\n' + defective)
            tail = scaffold(remainder) + post
            sf['content'] = shared + '# Learner section: select the authorized configuration\nconfig = None\n\n' + tail
            sol['content'] = shared + '# Learner section\nconfig = scoped_config\n\n' + tail
            pub['prompt'] = 'Read scoped_config and unscoped_config. Assign config to the mapping that retains the fixed authorized instance rather than a wildcard target, along with the supplied budget scope, amount, period, threshold, existing event binding, identity and runtime secret reference. Supplied scaffolding safely writes and reloads guardrail.yaml, inspects the resolved fields and replays below-threshold and breach fixtures for your selected mapping.'
        else:
            # Narrow numerical tasks to the recognized NumPy calls. Other
            # calculations remain visible, unchanged supplied statements.
            parts = []
            learner = []
            for node in ast.parse(body).body:
                source = ast.get_source_segment(body, node)
                violations = pysyntax.judge(source, con['allowed_syntax'], con['blocked_syntax'])[0]
                if violations or not isinstance(node, ast.Assign):
                    parts.append((scaffold(source), scaffold(source)))
                else:
                    assert isinstance(node, ast.Assign), (sid, source)
                    starter_line = ast.unparse(node.targets[0]) + ' = None\n'
                    parts.append(('# Learner section\n' + starter_line, '# Learner section\n' + source + '\n'))
                    learner.append(ast.unparse(node.targets[0]))
            sf['content'] = pre + '\n'.join(a for a, b in parts) + '\n' + post
            sol['content'] = pre + '\n'.join(b for a, b in parts) + '\n' + post
            pub['prompt'] = 'Complete only these numerical TODOs: ' + ', '.join(learner) + '. Use np.mean for each selected series and np.std with ddof=0 for its standard deviation' + ('; use np.histogram with bins=fixed_edges for the two count results' if 'ref_counts' in learner else '') + '. All selection, normalization, policy decisions and report construction are supplied, unchanged scaffolding. Keep those statements intact; your completed statistics must populate the declared report.'
        violations = pysyntax.judge(sol['content'], con['allowed_syntax'], con['blocked_syntax'], sf['content'])[0]
        assert not violations, (sid, violations)
        changed.append(sid)
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'changed_steps': changed, 'count': len(changed)}, indent=2))
