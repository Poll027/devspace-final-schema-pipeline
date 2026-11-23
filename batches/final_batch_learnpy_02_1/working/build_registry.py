import ast, json, re
from pathlib import Path
B=Path(__file__).resolve().parents[1]
bundle=json.loads((B/'inputs/path_glossary_bundle.json').read_text())
bs={b['context']['concept_id'].split('.',1)[1]:b for b in bundle['bundles']}
profile=json.loads(Path('00_FINAL_PIPELINE_CORE/registry/path_profiles/learn_python.json').read_text())
inspect=set(profile['practice_type_by_concept'])
def example(k):
    return next(t['content'] for t in bs[k]['teaching_blocks'] if t['purpose']=='example')
def code(k):
    return re.search(r'```python\n(.*?)```',example(k),re.S).group(1)
def line(k,n=0):
    return code(k).splitlines()[n]+'\n'
# Mine the examples and both anchors before constructing any assets.
vocab=['order','label','quantity','quantities','cost','rows','cell','notebook','pen','pencil','Ada','report.py','selected_python','Python','CPython']
for b in bs.values():
    text='\n'.join(t['content'] for t in b['teaching_blocks'])+'\n'+json.dumps(b['practice_anchor'],ensure_ascii=False)+'\n'+json.dumps(b['visual_anchor'],ensure_ascii=False)
    vocab.extend(re.findall(r'(?<![\w])(?:\d+\.\d+(?:e-?\d+)?|\d+)(?![\w])',text))
    for fragment in re.findall(r'```(?:python|text)\n(.*?)```',text,re.S):
        try:
            tree=ast.parse(fragment)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node,ast.Name): vocab.append(node.id)
            elif isinstance(node,ast.Attribute): vocab.append(node.attr)
            elif isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value:
                vocab.append(node.value)
    vocab.extend(re.findall(r'"([^"\n]+)"', '\n'.join(t['content'] for t in b['teaching_blocks'])))
vocab=list(dict.fromkeys(vocab))
sid='scenario.order_helper'
# Read the label list and editable quantity list directly from the glossary.
labels=ast.literal_eval(ast.parse(code('enumerate_iteration')).body[0].value)
quantities=ast.literal_eval(re.search(r'editable quantities in (\[[^\]]+\])',example('collection_selection')).group(1))
assets=[{'asset_id':'ds.orders','asset_kind':'dataset','scenario_id':sid,'title':'Order helper quantities','description':'Authored item quantities for the fictional order helper. Row order supplies the editable quantities example; labels support key lookup and numbered displays.','columns':[{'name':'label','type':'string','semantic_role':'categorical','description':'Item label used for lookup, not a sequence position.'},{'name':'quantity','type':'integer','semantic_role':'numerical','unit':'items','description':'Editable count of items.'}],'rows':[list(x) for x in zip(labels,quantities)],'variants':[],'provenance':'authored'}]
# Starter states only, not answer files. Trace exercises retain the supplied program.
starters={
 'collection_selection':'quantities = '+repr(quantities[:2])+'\n',
 'enumerate_iteration':line('enumerate_iteration'),
 'floating_point_limits':line('floating_point_limits',1),
 'indentation_and_blocks':'\n'.join(('    ' if s.startswith('print(') else '')+s.lstrip() for s in code('indentation_and_blocks').splitlines())+'\n',
 'math_utilities':line('math_utilities'),
 'nested_collections':'order = '+repr([ast.literal_eval(ast.parse(code('nested_collections')).body[0].value)])+'\n',
 'nested_loops':line('nested_loops'),
 'range_iteration':'for index in range():\n    print(index)\n',
 'statements_and_expressions':code('statements_and_expressions'),
 'comments':line('comments')+'cost = 0\nif quantity >= 1:\n    '+code('comments').splitlines()[1].split('  #')[0]+'\n',
 'interpreter_execution_model':re.search(r'containing (.*?) followed by (.*?)\.',example('interpreter_execution_model')).group(1)+'\n'+re.search(r'containing (.*?) followed by (.*?)\.',example('interpreter_execution_model')).group(2)+'\n',
 'multiline_expressions':'cost = (3 * 4 + 2)\nprint("Cost", cost)\n',
 'string_methods':line('string_methods')+'\n'+ '\n'.join(repr(n.value) for n in ast.walk(ast.parse(code('string_methods'))) if isinstance(n,ast.Constant) and isinstance(n.value,str) and ('red' in n.value))+'\n',
 'syntax_vs_runtime_errors':'quantity = 1\nif quantity > 0\n    quantity = int("three")\n',
 'truth_value_testing':line('truth_value_testing'),
 'none_and_identity':line('none_and_identity'),
 'unicode_and_bytes':line('unicode_and_bytes'),
}
for k,b in bs.items():
    if b['context']['concept_id'] in inspect: continue
    assert b['practice_anchor']['type']=='live_code'
    assets.append({'asset_id':'cw.'+k,'asset_kind':'code_workspace','scenario_id':sid,'title':b['context']['concept_name']+' starter','runtime':'python','files':[{'path':'main.py','content':starters[k]}]})
registry={'schema_version':'1.0','kind':'scenario_asset_registry','path_id':bundle['path_id'],'batch_id':B.name,'scenarios':[{'scenario_id':sid,'name':'A small order helper','summary':'A fictional stationery order helper uses notebook, pen and pencil labels and editable quantities. Its small Python examples also explore display, arithmetic, text handling and execution. Ada is an illustrative user name, not a real record.','domain':'stationery order helper','glossary_example_vocab':vocab}],'assets':assets}
(B/'scenario_asset_registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n')
# Stage-specific mistakes checklist, plus full-batch anchor coverage.
for a in assets:
    if a['asset_kind']=='dataset':
        assert all(len(r)==len(a['columns']) for r in a['rows'])
        assert all(isinstance(r[0],str) and isinstance(r[1],int) for r in a['rows'])
        assert a['rows'][:2]==list(map(list,ast.literal_eval(re.search(r'quantities by label in (\{[^}]+\})',example('collection_selection')).group(1)).items()))
assert len(starters)==len(bs)-len([k for k in bs if 'python.'+k in inspect])
assert not any(a['asset_id']=='cw.'+cid.split('.',1)[1] for cid in inspect for a in assets)
assert not any(b['practice_anchor']['type'] in ('field_selection','data_cleanup') for b in bs.values())
assert not any(b['visual_anchor']['type'] in ('data_table','spreadsheet','chart') for b in bs.values())
assert len({a['asset_id'] for a in assets})==len(assets)
print('Checklist PASS; concepts:',len(bs),'scenarios:',len(registry['scenarios']),'assets:',len(assets),'datasets: 1; rows:',len(labels),'variants: 0; workspaces:',len(starters))
print('Asset ids:',', '.join(a['asset_id'] for a in assets))
