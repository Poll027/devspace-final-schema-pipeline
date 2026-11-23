import ast,csv,hashlib,io,json,re
from pathlib import Path
B=Path('batches/final_batch_learn_python.region.01')
g=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
cs=g['bundles']; by={c['context']['concept_id'].split('.',1)[1]:c for c in cs}
def example(c):
 return '\n'.join(re.findall(r'```python\n(.*?)```','\n'.join(t['content'] for t in c['teaching_blocks']),re.S))
def tree(k): return ast.parse(example(by[k]))
def assignments(k,names):
 return '\n'.join(ast.unparse(n) for n in tree(k).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets))+'\n'
def first_assign(k,name):
 return ast.unparse(next(n for n in tree(k).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets)))+'\n'
vocab=set()
for c in cs:
 texts=[t['content'] for t in c['teaching_blocks']]+[json.dumps(c[k],ensure_ascii=False) for k in ['practice_anchor','visual_anchor','assessment_anchors']]
 for text in texts:
  vocab.update(re.findall(r'(?<!\w)-?\d+(?:\.\d+)?(?!\w)',text))
 for n in ast.walk(ast.parse(example(c))):
  if isinstance(n,ast.Name): vocab.add(n.id)
  elif isinstance(n,ast.arg): vocab.add(n.arg)
  elif isinstance(n,ast.Attribute): vocab.add(n.attr)
  elif isinstance(n,ast.Constant) and n.value is not None: vocab.add(str(n.value))
  elif isinstance(n,ast.Import): vocab.update(a.name for a in n.names)
  elif isinstance(n,ast.ImportFrom): vocab.add(n.module);vocab.update(a.name for a in n.names)
vocab.update(['notebooks','tokens','CSV','PEP 8','OrderCost','Quantity','UnitPrice','Cost'])
sid='scenario.learn_python.notebook_program'
r={'schema_version':'1.0','kind':'scenario_asset_registry','path_id':g['path_id'],'batch_id':B.name,'scenarios':[{'scenario_id':sid,'name':'A notebook-order learning program','summary':'A fictional learner builds small notebook-order programs, with product quantities and prices, colour labels, greetings, token-grouping calculations, and a saved CSV order. Each exercise uses the glossary’s own local example values rather than combining unrelated quantities or treating all prices as one price.','domain':'Small Python learning programs','glossary_example_vocab':sorted(vocab-{''})}],'assets':[]}
# The glossary explicitly supplies the CSV header and authored row.
f=by['file_io']['teaching_blocks']; txt='\n'.join(t['content'] for t in f)
header,row=re.search(r'contents are (\w+,\w+) followed by (\w+,\d+)',txt).groups()
cols=header.split(','); raw=next(csv.reader([row])); values=[raw[0],int(raw[1])]
buf=io.StringIO(newline=''); w=csv.writer(buf,lineterminator='\n');w.writerow(cols);w.writerow(values); csv_text=buf.getvalue()
(B/'assets').mkdir(exist_ok=True); (B/'assets/orders.csv').write_text(csv_text)
data=(B/'assets/orders.csv').read_bytes()
dataset={'asset_id':'ds.orders','asset_kind':'dataset','scenario_id':sid,'title':'orders.csv','provenance':'authored','description':'Authored CSV example: its header becomes dictionary keys, and its one data row is returned by csv.DictReader. Quantities are numeric counts although CSV reading returns text.','columns':[{'name':cols[0],'type':'string','semantic_role':'categorical','description':'Product label, not a quantity or sequence position.','numeric_looking_label':False},{'name':cols[1],'type':'integer','semantic_role':'numerical','unit':'items','description':'Count for the labelled product.','numeric_looking_label':False}],'rows':[values],'data_file':{'uri':'assets/orders.csv','format':'csv','sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)},'variants':[]}
# Additional valid hidden-check CSV rows use the glossary mapping, not outside facts.
mapping=ast.literal_eval(next(n.value for n in tree('dictionaries').body if isinstance(n,ast.Assign)))
new_pair=next(n for n in tree('dictionaries').body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Subscript) and ast.literal_eval(n.targets[0].slice) not in mapping)
pairs=list(mapping.items())[1:]+[(ast.literal_eval(new_pair.targets[0].slice),ast.literal_eval(new_pair.value))]
ops=[]
for i,(label,count) in enumerate(pairs):
 ops.extend([{'op':'duplicate_row','where':{cols[0]:values[0]},'occurrence':0},{'op':'set_cell','where':{cols[0]:values[0]},'occurrence':1,'column':cols[0],'value':label},{'op':'set_cell','where':{cols[0]:label},'occurrence':0,'column':cols[1],'value':count}])
 dataset['variants'].append({'variant_id':'orders.'+('two_products' if i==0 else 'three_products'),'derived_from':'ds.orders','purpose':'Additional valid authored product rows for CSV hidden checks; not the one-row teaching example.','ops':list(ops),'planted_issues':[]})
r['assets'].append(dataset)
starters={k:'' for k in by}
for k,names in {'logical_operators':['quantity_ok','budget_ok'],'string_basics_formatting':['quantity','cost'],'for_loops':['quantities'],'iterating_collections':['quantities'],'comprehensions':['quantities'],'import_statements':[]}.items():
 if names: starters[k]=assignments(k,names)
starters['comparison_operators']=first_assign('comparison_operators','quantity')
starters['while_loops']=first_assign('while_loops','response')
starters['type_conversion']=first_assign('type_conversion','quantity_text')+first_assign('core_data_types','price')
score=re.search(r'quantity = (\d+)',by['conditional_statements']['practice_anchor']['live_code']['starter_state_intent']).group(1)
starters['conditional_statements']='quantity = '+score+'\n'
set_call=next(n.value for n in tree('sets').body if isinstance(n,ast.Assign))
starters['sets']='first = '+ast.unparse(set_call.args[0])+'\n'
starters['variable_scope']=first_assign('variable_scope','quantity')
starters['error_handling']=first_assign('error_handling','text')+'quantity = int(text)\n'
zero=next(n.args[0] for n in ast.walk(tree('import_statements')) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute))
starters['import_statements']='value = '+ast.unparse(zero)+'\n'
# Valid scaffold supplied in the anchor; the header and indentation remain the task.
msg=next(n.value for n in ast.walk(tree('defining_calling_functions')) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='print') if False else None
hello=next(n.args[0] for n in ast.walk(tree('defining_calling_functions')) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='print')
starters['defining_calling_functions']='message = '+ast.unparse(hello)+'\n'
intent=by['parameters_arguments']['practice_anchor']['live_code']['starter_state_intent']
body=re.search(r'body (label = .*?), followed by',intent).group(1)
starters['parameters_arguments']='def describe():\n    '+body+'\n\ndescribe()\n'
# Make the deliberately poorly styled, but working, helper from the reference AST.
style=tree('pep8_style'); fn=style.body[0]; call=style.body[1].value.args[0]
starters['pep8_style']=ast.unparse(fn)+'\n\n'+ast.unparse(call)+'\n'
for old,new in [('order_cost','OrderCost'),('quantity','Quantity'),('unit_price','UnitPrice'),('cost','Cost')]:
 starters['pep8_style']=re.sub(r'\b'+old+r'\b',new,starters['pep8_style'])
starters['pep8_style']=starters['pep8_style'].replace('    ','  ').replace(' = ','=').replace('(Quantity, UnitPrice)','( Quantity , UnitPrice )').replace(ast.unparse(call).split('(',1)[1],ast.unparse(call).split('(',1)[1])
args=', '.join(ast.unparse(a) for a in call.args)
starters['pep8_style']=starters['pep8_style'].replace('OrderCost('+args+')','OrderCost( '+args.replace(',', ' ,')+' )')
for c in cs:
 k=c['context']['concept_id'].split('.',1)[1];a=c['practice_anchor']; files=[{'path':'main.py','content':starters[k]},{'path':'README.md','content':a['objective']+'\n\n'+a['live_code']['starter_state_intent']+'\n\nAllowed syntax:\n'+'\n'.join('- '+v for v in a['live_code']['allowed_syntax'])+'\n\nBlocked syntax:\n'+'\n'.join('- '+v for v in a['live_code']['blocked_syntax'])+'\n'}]
 if k=='file_io': files.append({'path':'orders.csv','content':csv_text})
 r['assets'].append({'asset_id':'ws.'+k,'asset_kind':'code_workspace','scenario_id':sid,'title':c['context']['concept_name']+' practice','runtime':'python','files':files})
(B/'scenario_asset_registry.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
# Stage mistakes-to-avoid and full-scope audit, in addition to the deterministic gate.
assert len(r['assets'])==len(cs)+1
assert all(len(row)==len(dataset['columns']) for row in dataset['rows'])
assert set(starters)==set(by)
assert all(c['practice_anchor']['type']=='live_code' for c in cs) # no planned find_issues
assert not any(c['visual_anchor']['type'] in ('chart','image') for c in cs)
for a in r['assets'][1:]: ast.parse(a['files'][0]['content'])
print('Scenarios:',len(r['scenarios']),'Assets:',len(r['assets']),'Datasets: 1; Workspaces:',len(cs),'Variants:',len(dataset['variants']),'Vocabulary:',len(vocab))
print('Asset ids:',', '.join(a['asset_id'] for a in r['assets']))
