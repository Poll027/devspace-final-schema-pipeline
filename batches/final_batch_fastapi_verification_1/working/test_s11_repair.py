import ast,json,sys
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from checkers import sandbox
B=Path('batches/final_batch_verification_1')
d=json.loads((B/'interactions.json').read_text())
ix=next(x['interaction'] for t in d['tiles'] for x in t['interactions'] if x['step_id']=='tile_045.s11')
s=ix['grading']['solution_files'][0]['content']
tree=ast.parse(s)
n=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='test_get_order')
lines=s.splitlines(True); test=''.join(lines[n.lineno-1:n.end_lineno])
no_request='def test_get_order():\n    with TestClient(app) as client:\n        assert True\n        assert True\n'
status_line=next(l for l in test.splitlines(True) if 'assert response.status_code' in l)
json_line=next(l for l in test.splitlines(True) if 'assert response.json()' in l)
cases={'solution':s,'no_request':s.replace(test,no_request),'no_status':s.replace(status_line,'        assert True\n'),'no_json':s.replace(json_line,'        assert True\n')}
probes=[sandbox._py_probe(t) for t in ix['grading']['tests']]
scripts=[sandbox._py_script(name,'exercise.py',code,[],probes,chart=False) for name,code in cases.items()]
res=sandbox.node_run(sandbox._py_job('python_asgi',[],scripts),sandbox.RUNTIMES['python_asgi']['runner'])
(B/'working/s11_mutation_results.json').write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2)[:14000])
