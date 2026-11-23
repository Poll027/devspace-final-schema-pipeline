import ast, json, re, sys
from pathlib import Path
sys.path.insert(0, '00_FINAL_PIPELINE_CORE/scripts/checkers')
from pysyntax import judge
B = Path('batches/final_batch_mle.region.production_operations')
p = B / 'interactions.json'
doc = json.loads(p.read_text())
original = json.loads(p.read_text())
reported = set(re.findall(r' E ([^/]+)/', (B / '04_dispatch_actual.log').read_text()))
bundles = {v['context']['concept_id']: v for v in json.loads((B / 'inputs/path_glossary_bundle.json').read_text())['bundles']}
changes = []
for tile in doc['tiles']:
    for entry in tile['interactions']:
        sid = entry['step_id']
        if sid not in reported:
            continue
        ix = entry['interaction']
        constraints = ix['public']['constraints']
        anchor = bundles[ix['measures'][0]['concept_id']]['practice_anchor']['live_code']
        assert constraints['allowed_syntax'] == anchor['allowed_syntax']
        assert constraints['blocked_syntax'] == anchor['blocked_syntax']
        allowed, blocked = constraints['allowed_syntax'], constraints['blocked_syntax']
        solution_file = ix['grading']['solution_files'][0]
        starter_file = ix['public']['workspace']['files'][0]
        solution, starter = solution_file['content'], starter_file['content']
        so, st = ast.parse(solution).body, ast.parse(starter).body
        assert len(so) == len(st)
        out_so, out_st, edits, supplied = [], [], [], []
        def append_shared(text):
            out_so.append(text)
            out_st.append(text)
        def binding(name, value):
            out_so.append('# Learner edit\n' + name + ' = ' + value)
            out_st.append('# TODO: select the supplied calculation/interface for ' + name + '\n' + name + ' = None')
            edits.append(name + ' = ' + value)
        for sn, tn in zip(so, st):
            text = ast.get_source_segment(solution, sn)
            start_text = ast.get_source_segment(starter, tn)
            if sid == 'mle.tile.083_085.s06' and isinstance(sn, ast.FunctionDef) and sn.name == 'quality':
                binding('loss_mean', 'np.mean')
                binding('loss_std', 'np.std')
                text = text.replace('np.mean(losses)', 'loss_mean(losses)').replace('np.std(losses, ddof=0)', 'loss_std(losses, ddof=0)')
                append_shared('# Supplied identity and maturity join; selected summaries are applied to its mature losses.\nexec(' + repr(text) + ')')
                continue
            if sid in {'mle.tile.086_089.s16', 'mle.tile.086_089.s21'} and isinstance(sn, ast.FunctionDef):
                name = sn.name
                if name in {'admit', 'rates', 'evaluate'}:
                    text = text.replace('def ' + name + '(', 'def supplied_' + name + '(', 1)
                    append_shared('# Supplied implementation: inspect its admission or validation conditions.\nexec(' + repr(text) + ')')
                    binding(name, 'supplied_' + name)
                else:
                    append_shared('# Supplied failure assertion fixture.\nexec(' + repr(text) + ')')
                continue
            # Keep YAML file handling and configuration shape in the scaffold;
            # the learner selects the safe writer and reader by name.
            if sid in {'mle.tile.083_085.s11', 'mle.tile.091_094.s14'} and isinstance(sn, ast.With):
                if any(isinstance(n, ast.Attribute) and n.attr == 'safe_dump' for n in ast.walk(sn)):
                    append_shared('# Supplied safe YAML writer interface.\nsafe_writer = yaml.safe_dump')
                    binding('write_config', 'safe_writer')
                    text = text.replace('yaml.safe_dump(', 'write_config(')
                else:
                    append_shared('# Supplied safe YAML reader interface.\nsafe_reader = yaml.safe_load')
                    binding('read_config', 'safe_reader')
                    text = text.replace('yaml.safe_load(', 'read_config(')
                append_shared('# Supplied file lifecycle; uses the selected safe interface.\n' + text)
                continue
            if sid == 'mle.tile.083_085.s16' and isinstance(sn, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'selected_rates' for t in sn.targets):
                # Build the rates as supplied data, then leave the binding editable.
                append_shared('# Supplied denominator-safe group rates.\n' + text.replace('selected_rates', 'supplied_rates'))
                continue
            if sid == 'mle.tile.083_085.s16' and isinstance(sn, ast.For):
                if 'selected_rates' in text:
                    append_shared('# Supplied denominator-safe group rates.\n' + text.replace('selected_rates', 'supplied_rates'))
                    binding('selected_rates', 'supplied_rates')
                elif 'selected_response' in text:
                    append_shared('# Supplied incident evidence selection.\n' + text.replace('selected_response', 'supported_response'))
                    binding('selected_response', 'supported_response')
                else:
                    append_shared(text)
                continue
            if sid == 'mle.tile.083_085.s16' and isinstance(sn, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'selected_response' for t in sn.targets):
                append_shared(text.replace('selected_response', 'supported_response'))
                continue
            if ast.dump(sn) == ast.dump(tn) and not isinstance(sn, (ast.FunctionDef, ast.ClassDef)):
                append_shared(text)
            elif judge(text, allowed, blocked)[0]:
                append_shared('# Supplied alignment, normalization, configuration or decision rule (unchanged).\n' + text)
                supplied.append(type(sn).__name__)
            else:
                out_so.append('# Learner edit\n' + text)
                out_st.append('# Learner edit\n' + start_text)
                edits.append(text)
        solution_file['content'] = '\n\n'.join(out_so) + '\n'
        starter_file['content'] = '\n\n'.join(out_st) + '\n'
        assert not judge(solution_file['content'], allowed, blocked, starter_file['content'])[0]
        prompts = {
            'mle.tile.080_082.s04': 'Complete ref_mean, cur_mean, ref_std and cur_std with NumPy mean and population standard deviation (ddof=0), and ref_counts and cur_counts with np.histogram using fixed_edges. The supplied code selects each window’s eligible observations, normalizes counts by that window’s total, retains every declared category/class, and emits the single records summary. Do not change that scaffold.',
            'mle.tile.080_082.s14': 'Complete ref_mean, cur_mean, ref_std and cur_std using NumPy and ddof=0 on ref_values and cur_values respectively. The supplied code aligns and normalizes categories and bins, applies the declared distances and thresholds, and constructs result. Retain those rules: its drift verdicts describe distribution differences, not established prediction degradation.',
            'mle.tile.083_085.s06': 'Complete loss_mean and loss_std by selecting the NumPy mean and standard-deviation functions. The supplied quality function applies them to mature matched losses with ddof=0. Inspect its prediction-ID, duplicate, cohort and availability-boundary checks and leave them unchanged. Its result report must retain separate eligible and mature denominators and must describe only mature-cohort quality.',
            'mle.tile.083_085.s11': 'Complete baseline_mean and baseline_std from baseline using NumPy and ddof=0. Select write_config = safe_writer and read_config = safe_reader to safely serialize and reload the supplied alert mapping. The scaffold applies the declared threshold rule, inspects the reloaded owner/response/window fields and replays both fixtures into result. Preserve that configuration and replay code.',
            'mle.tile.083_085.s16': 'Inspect the supplied denominator-safe rate calculation and incident evidence selection. Bind selected_rates to supplied_rates and selected_response to supported_response. Keep the zero-denominator, approved-configuration and permitted-response checks unchanged. The scaffold builds the diagnostic result from these selections without executing recovery.',
            'mle.tile.086_089.s16': 'Inspect supplied_admit and bind admit to that implementation. Its atomic claim must defer a busy event, avoid relaunching a completed claim, launch accepted claims with the persisted job ID, attach duplicates and release only after terminal confirmation. Leave the supplied concurrency/restart replay and durable-state assertions unchanged; they produce result.',
            'mle.tile.086_089.s21': 'Inspect supplied_rates and supplied_evaluate, then bind rates and evaluate to the corresponding implementations. Preserve their undefined-group, incumbent-relative cost, quality, slice, compatibility, cohort and exact-identity gates. The supplied valid, equality-boundary and failure assertions and test_all replay must produce result without weakening any gate.',
            'mle.tile.091_094.s04': 'Complete cpu_mean, cpu_std, memory_mean and memory_std from cpu and memory using NumPy and ddof=0. The supplied workload mask and series selection retain the same instance/process interval and exclude stopped or unrelated observations; leave those selections unchanged. The scaffold constructs result with identities, interval, observation counts and units.',
            'mle.tile.091_094.s09': 'Complete training_values and inference_values from the supplied allocated window totals, then calculate training_mean, training_std, inference_mean and inference_std using NumPy and ddof=0. Complete allocated_total using the supplied workload/window totals. Retain the supplied lifecycle records, direct/shared allocation rules, unusual/unmatched flags and allocated-plus-unallocated reconciliation; the scaffold produces result.',
            'mle.tile.091_094.s14': 'Select write_config = safe_writer and read_config = safe_reader to safely write and reload the supplied guardrail mapping. Retain its workload scope, budget amount, period, threshold, existing event binding, fixed approved instance and runtime secret references. The supplied inspection and replay produce result for the below-threshold and breach fixtures, including target-only stop evidence and the delayed-notification limitation. Do not change that configuration or replay.',
        }
        ix['public']['prompt'] = prompts[sid]
        assert edits, sid
        changes.append({'step_id': sid, 'learner_edits': edits, 'scaffolded_statements': supplied})
# Limit repair to the named steps and the permitted solution/starter/prompt fields.
for ot, nt in zip(original['tiles'], doc['tiles']):
    for oe, ne in zip(ot['interactions'], nt['interactions']):
        if oe['step_id'] not in reported:
            assert oe == ne
        else:
            check = json.loads(json.dumps(ne))
            for field in ['prompt', 'workspace']:
                check['interaction']['public'][field] = oe['interaction']['public'][field]
            check['interaction']['grading']['solution_files'] = oe['interaction']['grading']['solution_files']
            assert check == oe
p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + '\n')
(B / '04_dispatch_changes.json').write_text(json.dumps(changes, indent=2) + '\n')
print('Patched', len(changes), 'reported interactions')
