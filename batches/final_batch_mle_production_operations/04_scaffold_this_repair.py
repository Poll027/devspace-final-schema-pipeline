import ast, copy, json, re, sys
from pathlib import Path
B=Path(__file__).parent
p=B/'interactions.json'
d=json.loads(p.read_text())
original=copy.deepcopy(d)
ids=set(re.findall(r'^  E ([^/]+)/',(B/'04_this_repair_before.log').read_text(),re.M))

def wrap_functions(code):
    # Supplied implementations are scaffolding, not editable learner definitions.
    lines=code.splitlines(True)
    for n in reversed(ast.parse(code).body):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            text=''.join(lines[n.lineno-1:n.end_lineno])
            lines[n.lineno-1:n.end_lineno]=['exec('+repr(text)+')\n']
    return ''.join(lines)

def blank_assignment(code, names):
    lines=code.splitlines(True)
    found=set()
    for n in reversed(ast.parse(code).body):
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id in names:
            name=n.targets[0].id
            lines[n.lineno-1:n.end_lineno]=[name+' = None  # TODO: complete this assignment; leave the supplied implementation unchanged.\n']
            found.add(name)
    assert found == set(names), (found,names)
    return ''.join(lines)

changes=[]
for tile in d['tiles']:
    for e in tile['interactions']:
        sid=e['step_id']
        if sid not in ids: continue
        ix=e['interaction']; pub=ix['public']; solution=ix['grading']['solution_files'][0]['content']
        short=sid.removeprefix('mle.tile.')
        if short in ('080_082.s04','083_085.s06'):
            fname='summarize' if short=='080_082.s04' else 'quality'
            # Retain the supplied full record/cohort implementation, but require the learner
            # to select the mean and standard-deviation operations it calls.
            n=next(n for n in ast.parse(solution).body if isinstance(n,ast.FunctionDef) and n.name==fname)
            lines=solution.splitlines(True)
            body=''.join(lines[n.lineno-1:n.end_lineno]).replace('np.mean(', 'summary_mean(').replace('np.std(', 'summary_std(')
            lines[n.lineno-1:n.end_lineno]=['summary_mean = np.mean\n\nsummary_std = np.std\n\n'+body]
            solution=''.join(lines)
            names=['summary_mean','summary_std']
            prompt=('Complete summary_mean and summary_std by assigning the NumPy functions for the selected observations’ mean and standard deviation. The supplied '+fname+' implementation calls these functions with the declared divisor; leave its eligibility, normalization, identity, boundary and record-handling scaffolding unchanged. The tests inspect the resulting complete report, not just the selected function names.')
        elif short in ('080_082.s14','091_094.s09'):
            names=['ref_mean','cur_mean','ref_std','cur_std'] if short=='080_082.s14' else ['training_mean','training_std','inference_mean','inference_std']
            prompt=('Complete '+', '.join(names)+' using np.mean and np.std with ddof=0 on the corresponding supplied value arrays. Leave the supplied filtering, category alignment, distance decisions and comparison metadata unchanged.' if short=='080_082.s14' else 'Complete '+', '.join(names)+' using np.mean and np.std with ddof=0 on training_values and inference_values respectively. Leave the supplied lifecycle simulation, mapped/shared charge allocation, unmatched-charge handling and reconciliation unchanged. The tests inspect the complete workload report.')
        elif short=='083_085.s16':
            names=['rollback_response']
            prompt='Complete rollback_response by assigning the supplied approved_rollback_response. Leave the supplied matched-count rate calculations and distinguishing-evidence branches unchanged. Run the supplied analysis to retain unavailable groups and choose only the policy-supported response with its readiness and bounded-prediction gates; no recovery is executed.'
        elif short=='086_089.s16':
            names=['busy_response']
            prompt='Complete busy_response by assigning the supplied deferred_response so a busy pipeline claim is deferred. Leave the supplied atomic admission, persisted-identity reconciliation, terminal-only release and fixture assertions unchanged. Run the fixture checks; the returned records must preserve one logical job for duplicate deliveries and no overlapping jobs for different keys.'
        elif short=='086_089.s21':
            names=['validation_cohort']
            prompt='Complete validation_cohort by assigning the supplied required_cohort. Leave the supplied conditional-rate and expected-cost calculations, incumbent-relative checks, identity binding and every quality/slice/compatibility gate unchanged. Run the supplied valid, equality-boundary and failing fixture assertions; the returned verdict must use the declared cohort for both models.'
        elif short=='091_094.s14':
            names=['target_instance','target_zone']
            prompt='Complete target_instance and target_zone by assigning approved_instance and approved_zone respectively. Leave the supplied budget scope, period, threshold, existing topic/event binding, runtime-secret references and safe YAML round-trip unchanged. Run the replay: the below-threshold fixture must not stop an instance, and the breach fixture must authorize a stop only of the approved target. The supplied report checks before/after state and credential non-disclosure and retains the delayed-notification limitation.'
        else: raise AssertionError(sid)
        solution=wrap_functions(solution)
        starter=blank_assignment(solution,names)
        header='# Supplied implementation and fixture scaffolding. Edit only the TODO assignments named in the prompt.\n'
        pub['workspace']['files'][0]['content']=header+starter
        ix['grading']['solution_files'][0]['content']=header+solution
        pub['prompt']=prompt
        changes.append({'step_id':sid,'learner_assignments':names})
# Exact repair scope: prompts and starter/solution source only, no constraints or keys.
for old_t,new_t in zip(original['tiles'],d['tiles']):
    for old,new in zip(old_t['interactions'],new_t['interactions']):
        c=copy.deepcopy(new)
        if new['step_id'] in ids:
            c['interaction']['public']['prompt']=old['interaction']['public']['prompt']
            c['interaction']['public']['workspace']['files']=old['interaction']['public']['workspace']['files']
            c['interaction']['grading']['solution_files']=old['interaction']['grading']['solution_files']
        assert c==old
assert len(changes)==len(ids)
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
(B/'04_this_repair_changes.json').write_text(json.dumps(changes,indent=2)+'\n')
print(json.dumps(changes,indent=2))
