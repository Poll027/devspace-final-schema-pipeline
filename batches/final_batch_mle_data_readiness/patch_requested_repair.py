import json
from pathlib import Path
B = Path(__file__).parent
p = B / 'interactions.json'
part = json.loads(p.read_text())
screens = json.loads((B / 'screens.json').read_text())
# Only the reported unused remediation reference is safely repairable here.
tile = next(t for t in screens['tiles'] if t['tile_id'] == 'mle.tile.018_018')
remediation = next(r for r in tile['remediation_steps'] if r['step_id'].endswith('.r02'))
entry = next(e for t in part['tiles'] for e in t['interactions']
             if e['step_id'] == 'mle.tile.018_018.s05')
assert set(m['concept_id'] for m in entry['interaction']['measures']) <= set(remediation['concept_ids'])
entry['interaction']['feedback']['remediation_step_id'] = remediation['step_id']
p.write_text(json.dumps(part, indent=2) + '\n')
