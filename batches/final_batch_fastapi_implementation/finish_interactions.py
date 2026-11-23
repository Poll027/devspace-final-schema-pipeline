import json
from pathlib import Path
B=Path(__file__).parent
x=json.loads((B/'interactions.json').read_text());g={b['context']['concept_id']:b for b in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}
for t in x['tiles']:
 for e in t['interactions']:
  i=e['interaction']
  for k in ['correct','incorrect']:
   if isinstance(i['feedback'][k],str):i['feedback'][k]={'message':i['feedback'][k]}
  if not i['measures']:
   c=i['anchors'][0].split('#')[0];a=g[c]['assessment_anchors'][0]
   i['measures']=[{'concept_id':c,'capability':a['capability'],'fact_ids':a['fact_ids']}]
(B/'interactions.json').write_text(json.dumps(x,indent=2)+'\n')
