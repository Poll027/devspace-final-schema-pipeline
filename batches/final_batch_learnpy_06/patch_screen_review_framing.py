import json
from pathlib import Path
p = Path('batches/final_batch_learn_python.region.06/screens.json')
raw = p.read_text()
data = json.loads(raw)
replacements = {
 'learn_python.tile.113_115.s03': 'Inspect the supplied help(sorted), interpreter-version and official-documentation excerpts. Judge the API claims against that evidence and the documented interface for the executing version.',
 'learn_python.tile.113_115.s07': 'Inspect the supplied package-index and project-documentation excerpts. Judge each dependency suggestion using the evidence for its distribution identity, installation source and necessity compared with documented standard-library functionality.'
}
changed = []
for tile in data['tiles']:
 for step in tile['steps']:
  if step['step_id'] in replacements:
   old = step['lede']; new = replacements[step['step_id']]
   if old != new:
    # Replace only the named lede inside the existing text; preserve all other bytes.
    start = raw.index('"step_id": ' + json.dumps(step['step_id']))
    pos = raw.index('"lede": ' + json.dumps(old), start)
    old_field = '"lede": ' + json.dumps(old)
    new_field = '"lede": ' + json.dumps(new)
    raw = raw[:pos] + new_field + raw[pos + len(old_field):]
    changed.append(step['step_id'])
patched = json.loads(raw)
expected = json.loads(p.read_text())
for tile in expected['tiles']:
 for step in tile['steps']:
  if step['step_id'] in replacements: step['lede'] = replacements[step['step_id']]
assert patched == expected
p.write_text(raw)
print('Changed ledes:', changed)
print('Tiles:', len(data['tiles']))
print('Steps:', sum(len(t['steps']) for t in data['tiles']))
print('Remediation steps:', sum(len(t.get('remediation_steps', [])) for t in data['tiles']))
