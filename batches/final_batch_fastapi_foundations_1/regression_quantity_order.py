"""Require reordered column constraints to match every supplied grader result."""
import io
import json
from pathlib import Path
from unittest.mock import patch

d=json.loads((Path(__file__).parent/'interactions.json').read_text())
i=next(s['interaction'] for t in d['tiles'] for s in t['interactions'] if s['step_id']=='tile_017.s05')
solution=i['grading']['solution_files'][0]['content']
reordered=solution.replace('quantity INTEGER NOT NULL,','quantity INTEGER CHECK (quantity > 0) NOT NULL,').replace('# SQL     CHECK (quantity > 0),\n','')
assert reordered!=solution

def run(source,test):
    def supplied_open(path,*args,**kwargs):
        assert path=='main.py'
        return io.StringIO(source)
    with patch('builtins.open',supplied_open):
        ns={}
        exec(source,ns)
        return ns[test['spec']['function']](*test['spec']['args'])

for test in i['grading']['tests']:
    assert run(solution,test)==test['spec']['expected'],test['test_id']
    assert run(reordered,test)==run(solution,test),test['test_id']
print(f"PASS: {len(i['grading']['tests'])} reordered-column grader regressions")
