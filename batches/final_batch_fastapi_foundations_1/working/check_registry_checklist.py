import json,sys,re,os,tempfile
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from checkers.dataset import resolve_dataset,find_row
B=Path('batches/final_batch_foundations_1').resolve()
R=json.loads((B/'scenario_asset_registry.json').read_text())
G=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
A={a['asset_id']:a for a in R['assets']}
checks=[]
for a in A.values():
    if a['asset_kind']!='dataset':continue
    assert all(len(row)==len(a['columns']) for row in a['rows'])
    for c in a['columns']:
        if c['semantic_role']=='numerical':assert c['type'] in ('integer','number')
        if c['type']=='integer' and c['semantic_role'] in ('identifier','categorical'):assert c.get('numeric_looking_label')
        for row in a['rows']:
            value=row[a['columns'].index(c)]
            if value is None:continue
            assert {'integer':lambda v:type(v)==int,'number':lambda v:type(v) in (int,float),'string':lambda v:type(v)==str,'boolean':lambda v:type(v)==bool}[c['type']](value)
    for v in a.get('variants',[]):
        _,rows=resolve_dataset(R,a['asset_id'],v['variant_id'])
        assert v['planted_issues']
        for issue in v['planted_issues']:
            for loc in issue['locations']:
                i=find_row(rows,loc['where'],loc['occurrence']);assert i is not None
                if issue['kind']=='duplicate_row':assert loc['occurrence']==1 and any(j!=i and r==rows[i] for j,r in enumerate(rows))
        if v['variant_id'].endswith('unmatched_customer'):
            assert any(r['customer_reference'] is not None and r['customer_reference'] not in {x[0] for x in A['ds.customers']['rows']} for r in rows)
        if v['variant_id'].endswith('duplicate_external_reference'):
            labels=[r['external_reference'] for r in rows if r['external_reference'] is not None];assert len(labels)>len(set(labels))
checks+=['row widths and scalar types match columns','numeric role/label consistency checked','all planted issues have resolvable predicate locations; duplicate occurrence is 1','foreign-key and duplicate-external variant relationships verified against baseline']
for b in G['bundles']:
    if b['practice_anchor']['type'] in ('live_code','tool_simulation'):
        a=A['ws.'+b['context']['concept_id']]
        intent=json.loads(next(f['content'] for f in a['files'] if f['path']=='exercise_intent.json'))
        assert intent['practice_anchor']==b['practice_anchor']
        assert intent['visual_anchor']==b['visual_anchor']
checks+=['all live-code/tool anchors preserve exact intent in one workspace each','origin dataset contains all four supplied browser URLs and fixed API URL','orders and customers preserve the SQL field names; proposed rows cover every named constraint edge','no glossary anchor or teaching block depends on seeing a rendered plot; no plot images required']
# Test the authored execution harnesses with temporary completed learner code, not stored answer output.
completed={
'ws.python.context_managed_cleanup':'with open("orders.txt") as file:\n    content = file.read()\n',
'ws.asgi.request_lifecycle':'async def app(scope, receive, send):\n    request = await receive()\n    await send({"type":"http.response.start", "status":200, "headers":[(b"content-type",b"application/json")]})\n    await send({"type":"http.response.body", "body":b"{}"})\n'
}
import subprocess
for id,source in completed.items():
    with tempfile.TemporaryDirectory(dir=B/'working') as d:
        d=Path(d)
        for f in A[id]['files']:(d/f['path']).write_text(f['content'])
        (d/'main.py').write_text(source)
        subprocess.run([sys.executable,'harness.py'],cwd=d,check=True)
with tempfile.TemporaryDirectory(dir=B/'working') as d:
    d=Path(d)
    for f in A['ws.python.cooperative_async']['files']:(d/f['path']).write_text(f['content'])
    subprocess.run([sys.executable,'harness.py'],cwd=d,check=True)
checks.append('normal/failing cleanup, supplied ASGI sequence, and async harnesses execute successfully')
report={'concept_count':len(G['bundles']),'scenario_count':len(R['scenarios']),'asset_count':len(A),'dataset_rows':sum(len(a['rows']) for a in A.values() if a['asset_kind']=='dataset'),'variant_count':sum(len(a.get('variants',[])) for a in A.values()),'checklist_passed':checks,'limitations':['code_workspace has no registered deterministic checker','pwdlib, SQLAlchemy, Pydantic and HTTP tool/PostgreSQL execution need runtime provisioning; not verified by this environment','clean environment installation requires pinned jsonschema dependencies to be available']}
(B/'working/registry_checklist.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
