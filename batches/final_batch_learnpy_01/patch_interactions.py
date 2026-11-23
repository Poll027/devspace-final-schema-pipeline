import ast, copy, json, re
from pathlib import Path
from collections import Counter
B = Path('batches/final_batch_learn_python.region.01')
p = B / 'interactions.json'
d = json.loads(p.read_text())
before = copy.deepcopy(d)
ids = set(re.findall(r'^  E (\S+?)/.*solution uses', (B/'repair_gate.log').read_text(), re.M))
# All targets are existing outputs or inputs used by the existing dynamic tests.
targets = {
'000_002.s13':'division','003_005.s04':'at_least','003_005.s14':'price',
'006_007.s03':'grade','006_007.s07':'response','008_010.s04':'selected_labels',
'008_010.s07':'member','008_010.s11':'price','011_011.s03':'message',
'012_014.s03':'greeting','012_014.s06':'separator','012_014.s10':'cost',
'015_017.s04':'smallest','015_017.s07':'with_fee','015_017.s12':'result',
'018_018.s04':'text','020_020.s04':'result','021_024.s03':'total',
'021_024.s07':'total','021_024.s11':'quantities','021_024.s15':'doubled',
'025_025.s04':'rows'}
glossary = json.loads((B/'inputs/path_glossary_bundle.json').read_text())
plans = json.loads((B/'tile_plans.json').read_text())
screens = json.loads((B/'screens.json').read_text())
registry = json.loads((B/'scenario_asset_registry.json').read_text())
changed=[]
for tile in d['tiles']:
    for e in tile['interactions']:
        if e['step_id'] not in ids: continue
        ix=e['interaction']; pub=ix['public']; grading=ix['grading']
        suffix=e['step_id'].split('.tile.')[1]
        target=targets[suffix]
        code=grading['solution_files'][0]['content']
        # Keep original input assignments and computations. Function definitions
        # are supplied as an unchanged exec statement, not learner-authored defs.
        lines=code.splitlines(keepends=True)
        for n in reversed(ast.parse(code).body):
            if isinstance(n, ast.FunctionDef):
                source=''.join(lines[n.lineno-1:n.end_lineno])
                lines[n.lineno-1:n.end_lineno]=['exec('+repr(source)+')\n']
        scaffold=''.join(lines)
        backup='_practice_value'
        scaffold += f'{backup} = {target}\n'
        starter=scaffold + f'{target} = None\n' + f'# Replace the last assignment using the supplied {backup}.\n'
        solution=scaffold + f'{target} = {backup}\n'
        pub['workspace']['files'][0]['content']=starter
        grading['solution_files'][0]['content']=solution
        pub['prompt']=(f'The supplied code performs the computation and stores the value for {target} in {backup}. '
                       f'Keep the supplied inputs and scaffolding unchanged. Replace the final {target} = None assignment '
                       f'with an assignment from {backup} to {target}. The checker reads {target} and the other supplied results. '
                       'Do not type a literal answer.')
        # The style exercise's helper is now supplied, not learner-authored.
        # Its dynamic function tests remain; test the learner's named result.
        if suffix=='020_020.s04':
            ns={};exec(code,ns)
            test=grading['tests'][0]
            test['spec']={'expr':target,'expected':ns[target]}
        # No constraints, anchors, measures, feedback or unrelated items change.
        changed.append(e['step_id'])
assert set(changed)==ids
for t0,t1 in zip(before['tiles'], d['tiles']):
    for e0,e1 in zip(t0['interactions'],t1['interactions']):
        if e0['step_id'] not in ids: assert e0==e1
        else:
            for k in e0['interaction']:
                if k not in ('public','grading'): assert e0['interaction'][k]==e1['interaction'][k]
            assert e0['interaction']['public']['constraints']==e1['interaction']['public']['constraints']
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
print('Patched',len(changed),'interactions')
print('Counts',dict(Counter(e['interaction']['type'] for t in d['tiles'] for e in t['interactions'])))
