import json,textwrap,copy
from pathlib import Path
P=Path('batches/final_batch_mle.region.data_readiness');p=P/'interactions.json';d=json.loads(p.read_text())
ix={e['step_id']:e['interaction'] for t in d['tiles'] for e in t['interactions']}
def get(t,s):return ix['mle.tile.'+t+'.'+s]
# Preserve the named excerpt label and keep its original positive key.
i=get('004_006','s06')
for it in i['public']['items']:
 if it['item_id']=='types':it['text']='Declared CSV types\n```python\n'+it['text']+'\n```'
# Assertion-test result depends on caller's fixture; two distinct calls avoid a constant verdict.
for i in ix.values():
 if i['type']!='code_exercise':continue
 st=i['public']['workspace']['files'][0]['content'];sol=i['grading']['solution_files'][0]['content']
 if 'def run_checks():' in st:
  for f in [i['public']['workspace']['files'][0],i['grading']['solution_files'][0]]:
   f['content']=f['content'].replace('def run_checks():\n    learner_checks()\n    return True','def run_checks(*args):\n    learner_checks()\n    return evaluate(*args)')
  tests=i['grading']['tests'];tests[:]=[t for t in tests if t['test_id']!='learner_assertions']
  for n,source in enumerate([t for t in tests if t['kind']=='function_call'][:2]):
   t=copy.deepcopy(source);t['test_id']='learner_assertions_'+str(n+1);t['spec']['function']='run_checks';t['message_on_fail']='The learner-authored assertions and computed fixture report must agree.';tests.append(t)
# Move deliberately invalid group/time checks from the supplied evaluate to learner checks.
i=get('009_011','s16')
for f in [i['public']['workspace']['files'][0],i['grading']['solution_files'][0]]:
 c=f['content'];c=c.replace('assert not (set(INVALID_GROUP["training_groups"]) & set(INVALID_GROUP["validation_groups"]))','check_groups(INVALID_GROUP["training_groups"],INVALID_GROUP["validation_groups"])')
 c=c.replace('for row in INVALID_TIME["training"]:\n            assert row["observation_timestamp"] < fixture["cutoff"]','check_training_times(INVALID_TIME["training"],fixture["cutoff"])')
 f['content']=c
 if f is i['public']['workspace']['files'][0]:
  f['content']+='\ndef check_groups(training_groups, validation_groups):\n    # TODO: assert disjoint group sets.\n    pass\n\ndef check_training_times(rows, cutoff):\n    # TODO: assert strict training-time boundaries.\n    pass\n'
 else:
  f['content']+='\ndef check_groups(training_groups, validation_groups):\n    assert not (set(training_groups) & set(validation_groups))\n\ndef check_training_times(rows, cutoff):\n    for row in rows:\n        assert row["observation_timestamp"] < cutoff\n'
# Assess descriptive ValueError by exception type plus independently determined category,
# not an exact learner-authored message.
i=get('007_008','s05')
for f in [i['public']['workspace']['files'][0],i['grading']['solution_files'][0]]:
 f['content']=f['content'].replace('return {"accepted":False,"reason":str(error),"unchanged":table.equals(before)}','assert str(error).strip()\n        if set(table.columns) != {"distance","zone"}:\n            category = "columns"\n        elif table.dtypes["distance"] != "float64" or table.dtypes["zone"] != "string":\n            category = "types"\n        elif not ((table["distance"] >= 0) & (table["distance"] <= 100)).all():\n            category = "distance"\n        else:\n            category = "zone"\n        return {"accepted":False,"reason":category,"unchanged":table.equals(before)}')
sol=i['grading']['solution_files'][0];sol['content']=sol['content'].replace('raise ValueError("columns")','raise ValueError("Expected exactly distance and zone columns")').replace('raise ValueError("types")','raise ValueError("Expected distance float64 and zone string dtypes")').replace('raise ValueError("distance")','raise ValueError("Distance must be between 0 and 100 inclusive")').replace('raise ValueError("zone")','raise ValueError("Zone must be north or south")')
# Constant-feature scale assertion is learner-authored, not supplied.
i=get('012_015','s11');f=i['grading']['solution_files'][0];f['content']=f['content'].replace('assert np.allclose(saved_scale,scaler.scale_)','assert np.allclose(saved_scale,scaler.scale_)\n    assert scaler.scale_[1] == 1')
# Preserve the signature imports as supplied; learners still author all implementations.
# Wrapping only the PROVIDED section is necessary for the gate to distinguish identical
# fixture/helper functions from learner-authored functions (top-level defs are not excluded).
for i in ix.values():
 if i['type']!='code_exercise':continue
 for f in [i['public']['workspace']['files'][0],i['grading']['solution_files'][0]]:
  c=f['content']; marker='# Learner implementation and fixture assertions.'
  if marker not in c:continue
  supplied,learner=c.split(marker,1)
  f['content']='# Supplied test interface; leave unchanged.\nif True:\n'+textwrap.indent(supplied,'    ')+'\n'+marker+learner
p.write_text(json.dumps(d,indent=2)+'\n')
