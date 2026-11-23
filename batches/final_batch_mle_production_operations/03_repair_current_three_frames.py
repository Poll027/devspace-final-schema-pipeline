import json
from pathlib import Path

batch = Path(__file__).resolve().parent
path = batch / 'screens.json'
before = json.loads(path.read_text())
changes = {
    'mle.tile.086_089.s05': (
        'Review retraining eligibility and stage dependencies',
        'Read the supplied policy and stage traces in this step. Judge event eligibility, trigger reasons and intended inputs, stage artifacts and purposes, and the downstream stages blocked by a failed check. Check entry authorization, separate promotion approval and runtime-only handoff credentials.'
    ),
    'mle.tile.086_089.s10': (
        'Review authorized retraining and snapshot consumption',
        'Read the supplied Python, Cloud Build configuration and execution evidence in this step. Judge the imports and invocation logic, authorization, immutable-generation retrieval and verification, fatal stage dependencies, and accepted and rejected event paths. Check the returned execution identity, actual parameters and consumed snapshot, not just the start request.'
    ),
    'mle.tile.091_094.s19': (
        'Review scoped cleanup and verification evidence',
        'Read the supplied inspection, removal and audit evidence in this step. Judge whether ownership, release labels, runtime state, logs and compute identity justify the scoped actions. Check active health, retired-resource absence, retained artifacts and credential non-disclosure, and whether the audit record captures the verified identities and authorized actions.'
    ),
}
after = json.loads(json.dumps(before))
found = set()
for tile in after['tiles']:
    for step in tile['steps']:
        if step['step_id'] in changes:
            step['title'], step['lede'] = changes[step['step_id']]
            found.add(step['step_id'])
assert found == set(changes)
# Scope guard: only title and lede on the three named steps may change.
restored = json.loads(json.dumps(after))
old_steps = {s['step_id']: s for t in before['tiles'] for s in t['steps']}
for tile in restored['tiles']:
    for step in tile['steps']:
        if step['step_id'] in changes:
            for key in ('title', 'lede'):
                step[key] = old_steps[step['step_id']][key]
assert restored == before
path.write_text(json.dumps(after, indent=2) + '\n')
print('Patched title and lede on', len(found), 'named steps; interactions unchanged.')
print('Tiles:', len(after['tiles']))
print('Planned steps:', sum(len(t['steps']) for t in after['tiles']))
print('Remediation steps:', sum(len(t.get('remediation_steps', [])) for t in after['tiles']))
