import json, ast, csv, io, hashlib
from pathlib import Path
B=Path('batches/final_batch_mle.region.ml_lifecycle'); r=json.loads((B/'scenario_asset_registry.json').read_text());g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
checks=[]
def check(name,condition):
 assert condition,name
 checks.append(name)
check('Whole batch: one corresponding workspace per glossary concept', {'ws.'+b['context']['concept_id'].split('.')[-1] for b in g['bundles']} == {a['asset_id'] for a in r['assets'] if a['asset_kind']=='code_workspace'})
for a in r['assets']:
 if a['asset_kind']=='dataset':
  check(a['asset_id']+': every row matches column width',all(len(x)==len(a['columns']) for x in a['rows']))
  check(a['asset_id']+': explicit unambiguous roles',all(c['semantic_role'] in ['identifier','numerical','categorical','datetime','text','pii'] and not (c['semantic_role']=='numerical' and c['type'] not in ['number','integer']) for c in a['columns']))
  for c in a['columns']:
   if c.get('numeric_looking_label'):check(a['asset_id']+': numeric label type/role',c['type'] in ['number','integer'] and c['semantic_role'] in ['identifier','categorical'])
 else:
  paths=[f['path'] for f in a['files']];check(a['asset_id']+': unique safe workspace paths',len(paths)==len(set(paths)) and all(not p.startswith('/') and '..' not in Path(p).parts for p in paths))
  for f in a['files']:
   if f['path'].endswith('.py'):ast.parse(f['content'])
   if f['path'].endswith('.json'):json.loads(f['content'])
  check(a['asset_id']+': Python files parse and JSON fixture files load',True)
  check(a['asset_id']+': no completed learner solution', 'NotImplementedError' in next(f['content'] for f in a['files'] if f['path']=='learner.py'))
  cfg=json.loads(next(f['content'] for f in a['files'] if f['path']=='cloudbuild.yaml'))
  check(a['asset_id']+': no gate failure allowances',all(not s.get('allowFailure') and not s.get('allowExitCodes') for s in cfg['steps']))
check('No plots required: all visual anchors are UI_state, comparison, code or before_after and none asks to see a plot',all(b['visual_anchor']['type'] in ['UI_state','comparison','code','before_after'] and 'plot' not in b['visual_anchor']['purpose'].lower() for b in g['bundles']))
# Vocabulary must actually occur in taught blocks or anchors.
text='\n'.join(t['content'] for b in g['bundles'] for t in b['teaching_blocks'])+'\n'+'\n'.join(json.dumps({k:b[k] for k in ['assessment_anchors','practice_anchor','visual_anchor']}) for b in g['bundles'])
check('Mined vocabulary is present in glossary teaching/anchors',all(v.lower() in text.lower() for v in r['scenarios'][0]['glossary_example_vocab']))
check('Authored dataset content, no imported factual observations', all(a.get('provenance')=='authored' for a in r['assets'] if a['asset_kind']=='dataset'))
report={'checks':checks,'passed':len(checks),'planted_issues_and_occurrences':'Validated by deterministic --registry gate after declared ops','scope_concepts':len(g['bundles']),'scenarios':len(r['scenarios']),'assets':len(r['assets']),'datasets':sum(a['asset_kind']=='dataset' for a in r['assets']),'workspace_files':sum(len(a.get('files',[])) for a in r['assets']),'rows':sum(len(a.get('rows',[])) for a in r['assets']),'variants':sum(len(a.get('variants',[])) for a in r['assets']),'uncertainties':['Code workspaces have no deterministic asset checker; static syntax and fixture checks performed here.','Cloud execution and secret injection require the existing authorized hosted runtime; registered fixtures explicitly use a bounded local simulator.','Local repository bootstrap is supplied for runtime execution; it was not executed during registry authoring.']}
(B/'working/registry_checklist.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
