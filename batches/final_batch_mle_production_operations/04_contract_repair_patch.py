import json, ast, copy
from pathlib import Path
B=Path('batches/final_batch_mle.region.production_operations')
p=B/'interactions.json'
d=json.loads(p.read_text()); before=copy.deepcopy(d)
entries={e['step_id']:e['interaction'] for t in d['tiles'] for e in t['interactions']}
def patch_code(ix, fn):
    for f in ix['public']['workspace']['files']:
        if f['role']=='editable': f['content']=fn(f['content'])
    for f in ix['grading']['solution_files']:
        if f['path']==ix['public']['workspace']['entry']:f['content']=fn(f['content'])
# Change only the release distractor body, not the keyed routine or simulator.
ix=entries['mle.tile.086_089.s16']
def release(c):
    lines=c.splitlines(True)
    for i,l in enumerate(lines):
        if l.startswith('exec('):
            src=ast.literal_eval(l.strip()[5:-1])
            if src.startswith('def admission_release('):
                old="coordinator.confirm_terminal_and_release(event['run_key'], claim['job_id'])"
                assert src.count(old)==1
                lines[i]='exec('+repr(src.replace(old,"executor.attach(claim['job_id'])"))+')\n'
    return ''.join(lines)
patch_code(ix,release)
# Preserve the correct callables and evaluator; introduce competing supplied rules.
ix=entries['mle.tile.086_089.s21']
ix['public']['prompt']='Read the supplied rules and bind each rule name to the callable that satisfies the declared conditional-rate, expected-cost and acceptance contract.'
def alternatives(c):
    lines=c.splitlines(True)
    for i,l in enumerate(lines):
        if l.startswith('exec('):
            src=ast.literal_eval(l.strip()[5:-1])
            if src.startswith('def supplied_fpr_rule('):
                tree=ast.parse(src); funcs={n.name:ast.get_source_segment(src,n) for n in tree.body if isinstance(n,ast.FunctionDef)}
                edits=[('supplied_fpr_rule','pooled_fpr_rule',"model['FP'] + model['TN']","model['FP'] + model['TN'] + model['FN'] + model['TP']"),('supplied_fnr_rule','pooled_fnr_rule',"model['FN'] + model['TP']","model['FP'] + model['TN'] + model['FN'] + model['TP']"),('supplied_cost_rule','reversed_cost_rule','false_positive_weight * fpr + false_negative_weight * fnr','false_negative_weight * fpr + false_positive_weight * fnr'),('supplied_quality_rule','strict_quality_rule','<=','<'),('supplied_passed_rule','partial_passed_rule',"quality and candidate['slice_pass'] and candidate['compatibility_pass']",'quality')]
                extras=[]
                for name,new,old,repl in edits:
                    assert old in funcs[name]
                    extras.append(funcs[name].replace(name,new,1).replace(old,repl))
                lines[i]='exec('+repr(src+'\n\n'+'\n\n'.join(extras)+'\n')+')\n'
    return ''.join(lines).replace('# Bind the corresponding supplied rule.','# Select a supplied rule satisfying the contract.')
patch_code(ix,alternatives)
# Remove alias bindings. The config itself is the editable policy artifact.
ix=entries['mle.tile.091_094.s14']
ix['public']['prompt']='Complete `config` from the declared policy, including scope, amount, period, threshold, notification topic, response pipeline, fixed target, approved identity, secret-version reference, `secretEnv` and event binding. Reuse the supplied fixed-target `response_step`; retain serialization, inspection and replay checks.'
def config_patch(c,solution):
    start=c.index('# Complete the required configuration values.')
    end=c.index("\nwith open('guardrail.yaml'",start)
    region=c[start:end]; nodes=ast.parse(region)
    supplied={n.targets[0].id:ast.get_source_segment(region,n.value) for n in nodes.body if isinstance(n,ast.Assign) and n.targets[0].id.startswith('supplied_')}
    config=next(n.value for n in nodes.body if isinstance(n,ast.Assign) and n.targets[0].id=='config')
    fields=[]
    for k,v in zip(config.keys,config.values):
        key=ast.literal_eval(k)
        val='response_step' if key=='response_step' else supplied['supplied_'+key] if solution else 'None'
        fields.append('    '+repr(key)+': '+val+',')
    return c[:start]+'# Complete the required values directly in config.\nconfig = {\n'+'\n'.join(fields)+'\n}\n'+c[end:]
for f in ix['public']['workspace']['files']:
    if f['role']=='editable':f['content']=config_patch(f['content'],False)
for f in ix['grading']['solution_files']:
    if f['path']==ix['public']['workspace']['entry']:f['content']=config_patch(f['content'],True)
# Keep simulator implementation in the already supplied readonly asset only.
ix=entries['mle.tile.090_090.s05']
def simulator(c):
    lines=c.splitlines(True)
    for i,l in enumerate(lines):
        if l.startswith('exec('):
            src=ast.literal_eval(l.strip()[5:-1])
            if src.startswith('def recover('):
                lines[i]='exec("exec(open(\'runbook_simulator.py\').read(), globals())")\n'
    return ''.join(lines).replace('# Supplied in-memory simulator; no external file is needed.','# Load the supplied readonly simulator callable into the runtime.')
patch_code(ix,simulator)
# Requested surrounding instructions are already present; leave them untouched.
changed=[]
for t0,t1 in zip(before['tiles'],d['tiles']):
    for e0,e1 in zip(t0['interactions'],t1['interactions']):
        if e0!=e1:
            changed.append(e1['step_id'])
            assert e0['interaction']['anchors']==e1['interaction']['anchors']
            assert e0['interaction']['grading']['tests']==e1['interaction']['grading']['tests']
            assert e0['interaction']['public']['constraints']==e1['interaction']['public']['constraints']
assert set(changed)=={'mle.tile.086_089.s16','mle.tile.086_089.s21','mle.tile.090_090.s05','mle.tile.091_094.s14'}
p.write_text(json.dumps(d,indent=2)+'\n')
print('Changed:',changed)
print('Interactions:',sum(len(t['interactions']) for t in d['tiles']))
