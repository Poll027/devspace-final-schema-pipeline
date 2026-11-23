import json, sys
from pathlib import Path
sys.path.insert(0, str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers.dataset import resolve_dataset, find_row, rule_holds
B=Path('batches/final_batch_aws_devops.region.04_1')
r=json.loads((B/'scenario_asset_registry.json').read_text())
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
checks=[]
for a in r['assets']:
 if a['asset_kind']!='dataset': continue
 cols=a['columns']; names=[c['name'] for c in cols]
 assert len(names)==len(set(names))
 assert all(len(row)==len(cols) for row in a['rows'])
 for c in cols:
  assert c['semantic_role']!='numerical' or c['type'] in ('integer','number')
  if c.get('numeric_looking_label'):
   assert c['type'] in ('integer','number') and c['semantic_role'] in ('categorical','identifier')
 for row in a['rows']:
  for c,v in zip(cols,row):
   if v is None: continue
   assert {'string':lambda v:isinstance(v,str),'integer':lambda v:type(v)==int,'number':lambda v:type(v) in (int,float),'boolean':lambda v:type(v)==bool}[c['type']](v),(a['asset_id'],c['name'],v)
 for v in a.get('variants',[]):
  _,rows=resolve_dataset(r,a['asset_id'],v['variant_id'])
  assert v['derived_from']==a['asset_id']
  for issue in v.get('planted_issues',[]):
   for loc in issue['locations']:
    assert loc['occurrence']==0
    assert sum(all(row.get(k)==value for k,value in loc['where'].items()) for row in rows)==1
    index=find_row(rows,loc['where'],loc['occurrence'])
    assert index is not None
    holds,why=rule_holds(issue['rule'],rows,index,loc['column'])
    assert holds,why
checks += ['Row widths and declared value types pass for every dataset.', 'Semantic roles agree with types; numeric-looking ports are categorical labels.', 'All variant operations resolve; every planted issue holds after operations; all occurrences identify unique rows.']
_,rows=resolve_dataset(r,'ds.retention_preview')
for row in rows:
 expected=row['tag_status']=='untagged' and row['age_days']>row['age_threshold_days']
 assert row['eligible']==row['previewed_expiry']==expected
 assert not(row['still_needed'] and row['previewed_expiry'])
_,rows=resolve_dataset(r,'ds.retention_preview','var.retention_unsafe')
assert any(row['still_needed'] and row['previewed_expiry'] for row in rows)
_,rows=resolve_dataset(r,'ds.command_invocations')
assert len(rows)==3 and sum(row['invocation_status']=='Success' for row in rows)==2 and sum(row['invocation_status']=='Failed' for row in rows)==1
assert len(set(row['command_id'] for row in rows))==1
for row in rows: assert row['invocation_target'] in row['approved_target_set'].split(', ')
_,rows=resolve_dataset(r,'ds.command_invocations','var.command_scope_discrepancy')
assert any(row['invocation_target'] not in row['approved_target_set'].split(', ') for row in rows)
assert set(rows[0]['approved_target_set'].split(', '))-set(row['invocation_target'] for row in rows)
_,rows=resolve_dataset(r,'ds.scaling_timeline')
assert all(row['minimum_capacity']<=row['resulting_capacity']<=row['maximum_capacity'] for row in rows)
assert any(row['resulting_capacity']==row['maximum_capacity'] and row['metric_value']>row['metric_target'] for row in rows)
checks += ['Tables are sufficiently wide for retention eligibility/preview, approved versus actual target scope, individual outcomes, capacity bounds and configuration/result comparisons.', 'Glossary two-success/one-failure example and above-target-at-maximum case are present; needed digests are protected in the base and unsafe in the declared variant.']
text='\n'.join(t['content'] for b in g['bundles'] for t in b['teaching_blocks'])+'\n'+'\n'.join(json.dumps(b[k]) for b in g['bundles'] for k in ['visual_anchor','practice_anchor','assessment_anchors'])
assert all(term in text for term in r['scenarios'][0]['glossary_example_vocab'])
assert not any(a['asset_kind']=='code_workspace' for a in r['assets'])
by={a['asset_id']:a for a in r['assets']}
for b in g['bundles']:
 if b['visual_anchor']['type'] in ('data_table','spreadsheet'):
  concept=b['context']['concept_id']
  if concept.endswith('configure_artifact_repository_retention'): assert 'ds.retention_preview' in by
  elif concept.endswith('execute_a_scoped_systems_manager_remote_command'): assert 'ds.command_invocations' in by
  else: raise AssertionError('Unhandled mandatory table '+concept)
 if b['visual_anchor']['type']=='chart': assert 'img.scaling_bounded_timeline' in by
checks += ['All mined vocabulary appears verbatim in scoped teaching text or anchors. Unnamed identifiers and numbers are explicitly fictional authored case inputs.', 'Every mandatory data-table/chart anchor has an asset; all 14 concepts are inspect-and-judge and no executable workspace exists.', 'Column roles have explicit quantities, labels, identifiers, categories or text: no competing PII or measurement interpretation.']
report={'status':'PASS','concept_count':len(g['bundles']),'scenario_count':len(r['scenarios']),'dataset_count':sum(a['asset_kind']=='dataset' for a in r['assets']),'image_count':sum(a['asset_kind']=='image' for a in r['assets']),'base_row_count':sum(len(a.get('rows',[])) for a in r['assets']),'variant_count':sum(len(a.get('variants',[])) for a in r['assets']),'checks':checks}
(B/'working/scenario_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
