import copy, json, shutil
from pathlib import Path
from collections import Counter
b = Path('batches/final_batch_implementation')
p = b / 'interactions.json'
d = json.loads(p.read_text())
before = copy.deepcopy(d)
def target(doc):
    return next(e['interaction'] for t in doc['tiles'] if t['tile_id'] == 'tile_037' for e in t['interactions'] if e['step_id'] == 'tile_037.s07')
ix = target(d)
old_prompt = ix['public']['prompt']
old_feedback = copy.deepcopy(ix['feedback'])
ix['public']['prompt'] = ('PUBLICATION HOLD — required Uvicorn startup is unavailable in this sandbox. Do not publish this tile or award required-practice completion. The supplied python_asgi workspace has no native terminal or verified startup-evidence submission mechanism. The registry describes intended starter assets, not a verified available Uvicorn runtime.\n\nRequired practice remains blocked until a supported native terminal or independently verified external execution mechanism has Uvicorn installed, supplies the registry main.py, and verifies an executed process importing main:app and serving on 0.0.0.0:8000 without --reload. Command parsing, in-process ASGI responses and self-attestation cannot verify that success condition.\n\nOptional preparation only: set launch_command and inspect its import string and options with the supplied harness. Passing the inspection test does not complete the required practice. There is currently no verified run submission to use.')
ix['feedback']['correct']['message'] = 'Preparation inspection passed, not Uvicorn startup verification. Required practice remains blocked and incomplete. Keep this tile unpublished until a supported execution and grading mechanism verifies actual Uvicorn startup; do not award completion for this parsed command.'
ix['feedback']['incorrect']['message'] = 'Command inspection has not passed. This sandbox cannot verify Uvicorn startup, even if the inspection passes. Required practice remains blocked and incomplete; keep the tile unpublished pending supported execution verification.'
ix['feedback']['hints'] = ['This workspace only inspects command options; it cannot execute Uvicorn.', 'Actual startup requires the supplied main.py and a supported run-and-verify mechanism, not a parsed command or self-attestation.']
# Only the named step's prompt and feedback changed. Keys, tests, runtimes,
# constraints, other interactions and all other stage artifacts stay untouched.
check = copy.deepcopy(d)
target(check)['public']['prompt'] = old_prompt
target(check)['feedback'] = old_feedback
assert check == before
bundle = json.loads((b/'inputs/path_glossary_bundle.json').read_text())
g = next(x for x in bundle['bundles'] if x['context']['concept_id'] == 'fastapi.production_asgi_serving')
assert ix['public']['constraints']['allowed_syntax'] == g['practice_anchor']['live_code']['allowed_syntax']
assert ix['public']['constraints']['blocked_syntax'] == g['practice_anchor']['live_code']['blocked_syntax']
# Mistakes review: no answer/expected edits, invented runtime, startup evidence,
# widened syntax, changed anchors or new completion claim. Actual practice is
# still unsatisfiable: this patch is a publication hold, not a runtime repair.
p.write_text(json.dumps(d, indent=2)+'\n')
c = Counter(e['interaction']['type'] for t in d['tiles'] for e in t['interactions'])
print('tiles', len(d['tiles']), 'interactions', sum(c.values()), dict(c))
s = b/'scratch_s07_unavailable_execution_gate'
s.mkdir(exist_ok=True)
for name in ['batch_run_context.json','tile_plans.json','screens.json','scenario_asset_registry.json','interactions.json']:
    shutil.copy2(b/name, s/name)
(s/'inputs').mkdir(exist_ok=True)
shutil.copy2(b/'inputs/path_glossary_bundle.json', s/'inputs/path_glossary_bundle.json')
