import json, re, copy
from pathlib import Path
b = Path(__file__).parent
p = b / 'interactions.json'
d = json.loads(p.read_text())
before = copy.deepcopy(d)
g = {x['context']['concept_id']: x for x in json.loads((b / 'inputs/path_glossary_bundle.json').read_text())['bundles']}
model_shape = re.search(r'shape (\([^)]*\))', g['mle.neural_model_definition']['practice_anchor']['success']).group(1)
a = g['mle.task_loss_selection']['practice_anchor']
outputs = re.search(r'outputs (\[[^]]*\])', a['objective']).group(1)
targets = re.search(r'targets (\[[^]]*\])', a['objective']).group(1)
loss = re.search(r'loss ([\d.]+)', a['success']).group(1)
derivatives = re.search(r'derivatives (\[[^]]*\])', a['success']).group(1)
early = g['mle.validation_early_stopping']['practice_anchor']['success']
min_delta = re.search(r'min_delta ([\d.]+)', early).group(1)
patience = re.search(r'patience (\d+)', early).group(1)
tasks = {
'mle.tile.035_037.s05': 'Implement `prepare`, return the aligned tensor tuple, and submit your source and assertion results for the valid, boundary and incompatible fixtures.',
'mle.tile.035_037.s10': 'Implement the paired Dataset and loader; submit source and assertions verifying indexed pairings, both drop_last policies and shuffled pair integrity.',
'mle.tile.035_037.s15': f'Implement and return the task-compatible nn.Module; submit source and fixture results verifying registered layers, forward, matching widths and output shape {model_shape}.',
'mle.tile.038_040.s06': 'Implement fresh W/b gradient verification and submit source plus valid, boundary and mismatched-reference assertion results.',
'mle.tile.038_040.s13': f'Implement mean-MSE verification for outputs {outputs} and targets {targets}; submit source and results for equal shapes, loss {loss}, derivatives {derivatives} and their signs.',
'mle.tile.038_040.s18': 'Implement one plain-SGD update; submit source and assertions for the resulting value and signed change, including the zero-rate boundary and rejected incorrect expectation.',
'mle.tile.041_043.s05': 'Implement the minibatch loop; submit source and results verifying each current-gradient update, scalar losses and actual batch counts.',
'mle.tile.041_043.s12': 'Implement the mode and forward-only validation verifier; submit source and assertions for dropout masking/scaling, evaluation identity, no-grad validation and restored training mode.',
'mle.tile.041_043.s17': 'Implement binary-handle state_dict save/reload; submit source and assertion results comparing corresponding state entries and fixed-input evaluation predictions, including valid, boundary and failed-reload fixtures.',
'mle.tile.044_045.s06': f'Implement the bounded early-stopping controller; submit source, the patience/checkpoint trace and restored-state verification for min_delta {min_delta} and patience {patience}, without protected-test access.',
'mle.tile.044_045.s11': 'Reproduce the supplied failure, capture loss and gradients before clearing, apply one evidence-supported correction, and submit source and matched rerun assertions for valid, boundary and failure cases.',
'mle.tile.046_048.s06': 'Implement and execute the placement verifier on the authorized lab; submit source, actual model/input/target device evidence, fixture assertions and verified final VM state.',
'mle.tile.046_048.s11': 'Implement candidate-batch trials; submit source, actual shapes/counts, feature-plus-target estimates, measured CUDA peaks and completed-work timings, then select an eligible setting.',
'mle.tile.046_048.s17': 'Reproduce the memory failure, inventory simultaneous allocations, change one supported factor, and submit source plus failed/corrected completion and allocated/reserved peak evidence for the same task.',
'mle.tile.049_050.s05': 'Profile and reproduce the supplied bottleneck; submit source, labeled attribution and process evidence, one isolated correction, and matched warm unprofiled completed-work timings.',
'mle.tile.049_050.s10': 'Benchmark both authorized options on the same task; submit source and placement, quality, memory, execution/lifecycle cost and verified shutdown evidence, then justify a feasible capacity choice.',
'mle.tile.051_051.s06': 'Implement and run classifier-only adaptation in the attached lab; submit source and results verifying task labels, selected head gradient, changed head weights, unchanged backbone values, and baseline/adapted FPR, FNR and expected error cost on the same validation cohort, explicitly reporting undefined rates or non-improvement.'
}
changed = []
for tile in d['tiles']:
    for e in tile['interactions']:
        if e['step_id'] not in tasks:
            continue
        parts = e['interaction']['public']['prompt'].split('\n\n')
        assert parts[0].startswith('PRACTICE BLOCKED') and parts[2].startswith('Required verified results:')
        parts[1] = 'Requested task once the required authorized lab, fixtures and verified submission route are provisioned:\n' + tasks[e['step_id']]
        e['interaction']['public']['prompt'] = '\n\n'.join(parts)
        changed.append(e['step_id'])
assert set(changed) == set(tasks)
check = copy.deepcopy(d)
for t0, t1 in zip(before['tiles'], check['tiles']):
    for e0, e1 in zip(t0['interactions'], t1['interactions']):
        if e1['step_id'] in tasks:
            e1['interaction']['public']['prompt'] = e0['interaction']['public']['prompt']
assert check == before
p.write_text(json.dumps(d, indent=2) + '\n')
print('Patched prompts:', len(changed))
from collections import Counter
print('Counts:', dict(Counter(e['interaction']['type'] for t in d['tiles'] for e in t['interactions'])))
print('Tiles:', len(d['tiles']))
