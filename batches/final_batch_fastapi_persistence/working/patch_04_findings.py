import ast,copy,json
from pathlib import Path
B=Path('batches/final_batch_persistence');p=B/'interactions.json';d=json.loads(p.read_text());before=copy.deepcopy(d)
ix={s['step_id']:s['interaction'] for t in d['tiles'] for s in t['interactions']}
def patch_scaffold(content,fn):
 tree=ast.parse(content);old=ast.literal_eval(tree.body[0].value);new=fn(old)
 assert new!=old
 return content.replace(repr(old),repr(new),1)
i=ix['tile_065.s04']
def migration(sc):
 a="or proposition(r'(?:must|need|required).{0,50}(?:manual(?:ly)? )?correction')"
 b="or proposition(r'(?:must|need|required).{0,120}(?:verify|testdb)')"
 assert a in sc and b in sc
 return sc.replace(a,a+" or proposition(r'before approval.{0,120}(?:manual(?:ly)? )?correction')").replace(b,b+" or proposition(r'before approval.{0,120}(?:verify|testdb)')")
for f in i['public']['workspace']['files']+i['grading']['solution_files']:f['content']=patch_scaffold(f['content'],migration)
report=json.loads((B/'final_audit_report.json').read_text())
def find(x,step):
 if isinstance(x,dict):
  if x.get('step_id')==step:return x
  for v in x.values():
   r=find(v,step)
   if r:return r
 elif isinstance(x,list):
  for v in x:
   r=find(v,step)
   if r:return r
finding=find(report,'tile_065.s04')
region=finding['problem'].split('this learner region: ',1)[1].split('\n. Both directions',1)[0]
# Preserve the exact report region; derive comment aggregation as check_review does.
import tokenize,io
comments=[t.string[1:] for t in tokenize.generate_tokens(io.StringIO(region).readline) if t.type==tokenize.COMMENT]
review=' '.join(comments)
sc=ast.literal_eval(ast.parse(i['public']['workspace']['files'][0]['content']).body[0].value)
ns={};exec(sc.split('\nimport inspect\n')[0],ns)
for direction in ['upgrade','downgrade']:
 result=ns['review_findings'](review,direction)
 assert result['correction_before_approval'] and result['test_verification_required'] and all(v for k,v in result.items() if k!='direction'),result
 template=copy.deepcopy(next(t for t in i['grading']['tests'] if t['test_id'].endswith('accept_affirmative_'+direction)))
 template['test_id']='tile_065.s04.accept_preposed_approval_'+direction
 template['spec']['requests'][0]['json']['args']=[review,direction]
 template['spec']['expected']['json']=result
 template['message_on_fail']='Accept the exact review with Before approval preceding correction and test-database verification requirements.'
 i['grading']['tests'].append(template)
(B/'working/migration_preposed_approval_regression.py').write_text(region+'\n')
# Run every existing predicate regression, including all negation guards.
for t in i['grading']['tests']:
 payload=t['spec'].get('requests',[{}])[0].get('json',{})
 if payload.get('function')=='review_findings':assert ns['review_findings'](*payload['args'])==t['spec']['expected']['json'],t['test_id']
i=ix['tile_076.s12']
def transaction(sc):
 old="        if fail: assert raised and s.events[-1]=='rollback'"
 new="        transaction_contract_met = (raised and bool(s.events) and s.events[-1]=='rollback') if fail else ('commit' in s.events and 'rollback' not in s.events and not raised)"
 assert old in sc
 return sc.replace(old,new).replace("'events':s.events","'transaction_contract_met':transaction_contract_met")
for f in i['public']['workspace']['files']+i['grading']['solution_files']:f['content']=patch_scaffold(f['content'],transaction)
for t in i['grading']['tests']:
 expected=t['spec']['expected']['json'];assert 'events' in expected
 del expected['events'];expected['transaction_contract_met']=True
contract="Load the intended Order, preserve its original quantity, apply only supplied permitted fields, commit success or roll back failure, and independently verify the stored fields; additional primary-key reads are not an error."
i['public']['prompt']=contract+' '+i['public']['prompt']
# The graded reference now uses the report's two-line alternative, so the normal
# success and failure gates execute that regression rather than just describing it.
f=i['grading']['solution_files'][0]
a='    original_quantity = order.quantity\n';b='    original = await session.get(Order, order_id)\n    original_quantity = original.quantity\n'
assert a in f['content'];f['content']=f['content'].replace(a,b,1)
for old in [i['grading']['tests'][0],i['grading']['tests'][2]]:
 t=copy.deepcopy(old);t['test_id']=old['test_id']+'.additional_primary_key_read';t['message_on_fail']=contract;i['grading']['tests'].append(t)
# Limit edits to the named interactions; no unrelated stage output changes.
for t in d['tiles']:
 for s in t['interactions']:
  if s['step_id'] not in ['tile_065.s04','tile_076.s12']:assert s==next(u for v in before['tiles'] for u in v['interactions'] if u['step_id']==s['step_id'])
p.write_text(json.dumps(d,indent=2)+'\n')
print('Patched 2 interactions; migration predicate regressions pass. Counts:',len(d['tiles']),sum(len(t['interactions']) for t in d['tiles']))
