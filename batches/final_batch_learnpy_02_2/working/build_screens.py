import json,re,ast,copy
from pathlib import Path
B=Path('batches/final_batch_learn_python.region.02_2')
p=json.loads((B/'tile_plans.json').read_text()); g=json.loads((B/'inputs/path_glossary_bundle.json').read_text()); registry=json.loads((B/'scenario_asset_registry.json').read_text())
bundles={x['context']['concept_id']:x for x in g['bundles']}
Z,A,C,D,H=list(bundles)
def example(c):
 return re.search(r'```python\n(.*?)```',bundles[c]['teaching_blocks'][3]['content'],re.S).group(1).rstrip()
codes={c:example(c) for c in bundles}
labels=ast.literal_eval(ast.parse(codes[Z]).body[0].value); quantities=ast.literal_eval(ast.parse(codes[Z]).body[1].value)
colors=ast.literal_eval(ast.parse(codes[C]).body[1].value.args[0]); text=ast.literal_eval(ast.parse(codes[D]).body[0].value)
def lin(c,fs=None,tbs=None,anchors=None):
 return {'concept_ids':[c], 'fact_ids':[c+'#'+f for f in (fs or [])], 'teaching_block_ids':[c+'#'+t for t in (tbs or [])], 'anchors':anchors or []}
def prose(c,text,fs,tbs,role='mechanism'):
 return {'type':'prose','role':role,'text':text,'lineage':lin(c,fs,tbs)}
def walk(c,code=None,annotations=None,visual=True):
 return {'type':'code_walkthrough','language':'python','code':code or codes[c],'annotations':annotations or [],'reveal':'all','lineage':lin(c,[f['id'] for f in bundles[c]['coverage']['required_facts']],['tb4'],[c+'#visual'] if visual else [])}
def ann(code,needle,text):
 lines=code.splitlines(); i=next(i for i,l in enumerate(lines,1) if needle in l);return {'start_line':i,'end_line':i,'text':text}
texts={
 Z:[prose(Z,'zip(left, right) pairs corresponding elements into tuples. In for left_item, right_item in zip(left, right):, the two variables receive each pair; an indented body processes it.',['f1','f2'],['tb1','tb2','tb3']),prose(Z,f'By default, zip stops at the shortest input. Here {labels[-1]} has no corresponding quantity and is omitted, not given a missing value. Account for unmatched trailing entries before treating the pairs as a complete report.',['f3'],['tb3','tb4','tb5'],'misconception')],
 A:[prose(A,'Different names can refer to one object: assignment is not a copy. Mutating a shared list or dictionary can be visible through another name and to a caller.',['f1'],['tb1','tb2']),prose(A,'items.copy() or items[:] makes a shallow list copy: top-level changes are independent, but references to existing elements remain. A nested mutable element can still be shared.',['f2','f3'],['tb3'])],
 C:[prose(C,'After from collections import Counter, Counter(items) counts occurrences of hashable elements, mapping each element to its count. Use it to summarize repeated stationery labels.',['f1'],['tb1','tb2']),prose(C,'counts.most_common(1) returns a list containing the most frequent element/count pair, or an empty list for an empty counter. Check that the list is nonempty before selecting its first pair.',['f2','f3'],['tb3','tb4','tb5']),prose(C,'most_common orders pairs by descending count. Tied counts follow first encounter, not a separate ranking. Compare the repeated-label example with empty input and a tie using the same labels.',['f3'],['tb3','tb4'])],
 D:[prose(D,'Use print(label, value) for a labeled view of the state at an execution point. Observe the text before conversion and the quantity after its binding rather than guessing from a final result.',['f1','f3'],['tb1','tb2','tb3','tb4']),prose(D,'repr(value) returns a printable representation that can expose details ordinary string display obscures. Here it makes surrounding spaces and quotes visible.',['f2'],['tb3','tb4']),prose(D,'Place the diagnostic after the binding or before the operation you are investigating. A print before a later reassignment cannot show the later value. Remove the print call when that diagnostic output is no longer needed.',['f3'],['tb3','tb4','tb5'],'misconception')],
 H:[prose(H,'Document public functions, modules, classes and methods with docstrings so callers can inspect the interface.',['f1'],['tb1','tb2','tb4']),prose(H,'A string literal first in a function body provides its docstring. Start with a concise purpose summary; separate additional calling details with a blank line. A string later in the body is not its first-statement docstring.',['f2'],['tb3','tb4','tb5']),prose(H,'Describe arguments, return values and applicable exceptions accurately. For cost, document the numeric arguments and returned product without inventing exception claims. help(cost) displays the function signature and documentation, including its docstring.',['f3','f4'],['tb3','tb4','tb5'])]
}
alias_example=[prose(A,'alias and original share an outer list, so appending through alias affects original. copied has a separate outer list, so that append does not affect its top level. Updating an existing inner element through copied is visible through original because the inner list is shared. original[:] also makes a shallow copy.',['f1','f2','f3'],['tb4','tb5'],'example')]
# Structural drawing deliberately uses no computed post-mutation values.
alias_diagram={'type':'diagram','diagram_kind':'mapping','title':'Separate outer lists, shared inner list','nodes':[{'id':i,'label':label} for i,label in [('original','original'),('alias','alias'),('copied','copied'),('outer','Shared outer list'),('copy_outer','Copied outer list'),('inner','Existing inner list'),('append','alias.append: outer change'),('update','copied[0][0]: inner change')]],'edges':[{'from':a,'to':b,'label':l,'directed':True} for a,b,l in [('original','outer','refers to'),('alias','outer','refers to'),('copied','copy_outer','refers to'),('outer','inner','element reference'),('copy_outer','inner','same element reference'),('append','outer','changes this list only'),('update','inner','changes shared element')]],'layout':'auto','alt_text':'original and alias point to one outer list. copied points to another outer list. Both outer lists reference the same existing inner list. An append through alias changes the shared outer list; a nested update through copied changes the shared inner list.','lineage':lin(A,['f1','f2','f3'],['tb2','tb3'],[A+'#visual'])}
# Code examples are taken from the glossary; outputs are left to stage 05.
zip_visual=walk(Z,annotations=[ann(codes[Z],'for ', 'Each paired tuple binds the two loop variables.'),ann(codes[Z],'labels =',f'{labels[-1]} is unmatched and omitted by default.')])
counter_code=codes[C].replace('pairs = counts.most_common(1)','print(counts)\npairs = counts.most_common(1)\nprint(pairs)')
empty_code='from collections import Counter\ncounts = Counter([])\npairs = counts.most_common(1)\nprint(counts)\nprint(pairs)\nif pairs:\n    label, count = pairs[0]\n    print(label, count)'
tie_code='from collections import Counter\ncounts = Counter('+repr(list(dict.fromkeys(colors)))+')\nprint(counts)\nprint(counts.most_common(1))'
# Preserve the registered helper's text reassignment, inserting observations from the glossary.
d_asset=next(a for a in registry['assets'] if a['asset_id']=='code.'+D)
d_starter=d_asset['files'][0]['content'].split('\n#')[0].rstrip()
diagnostic_lines=codes[D].splitlines()
d_code=d_starter.replace('    quantity = int(text)','    '+diagnostic_lines[1]+'\n    quantity = int(text)').replace('    return quantity','    '+diagnostic_lines[3]+'\n    return quantity')+'\n\nconvert_quantity('+repr(text)+')'
recaps={Z:'zip forms corresponding tuples, and two loop variables bind each pair. By default, traversal stops at the shortest input and leaves unmatched trailing values unvisited.',A:'Assignment can share an object. A shallow copy separates top-level list changes, but nested mutable elements can remain shared.',C:'Counter maps elements to frequencies. most_common returns a list: guard first-pair access, and interpret ties by first encounter.',D:'Label observations, use repr to expose string details, and place diagnostics at the binding or operation you want to inspect. Remove temporary print calls afterward.',H:'Put the docstring first. Summarize purpose, then give accurate argument, return and applicable exception details after a blank line. Inspect signature and documentation with help.'}
framing={
(Z,'check'):('Predict the stopping point','Choose which entries the supplied zip traversal visits and which it omits.'),(Z,'hands_on'):('Pair stationery labels','Write a two-variable zip loop for the supplied labels and quantities, and identify the unmatched label.'),
(A,'check'):('Trace the shared reference','Read the supplied list changes and choose where each mutation is visible.'),(A,'hands_on'):('Separate the outer list','Repair the helper so appending to its returned list does not change the caller’s outer list.'),
(C,'check'):('Interpret the Counter result','Inspect the supplied labels and decide how counts and most_common results should be interpreted.'),(C,'hands_on'):('Report a frequent label safely','Complete the Counter helper: request the most common pair and report it only if one exists.'),
(D,'check'):('Locate the observation','Inspect the supplied code and choose the diagnostic that reveals the intended current value.'),(D,'hands_on'):('Inspect the conversion','Add labeled observations before and after conversion, use repr for text, then remove the temporary print calls.'),
(H,'check'):('Inspect interface documentation','Choose the call that displays the helper’s signature and documentation.'),(H,'hands_on'):('Document the cost helper','Add an accurate first-statement docstring without changing the calculation, then inspect it with help(cost).')}
out={'schema_version':p['schema_version'],'kind':'screens_part','path_id':p['path_id'],'batch_id':p['batch_id'],'tiles':[]}
for plan in p['tiles']:
 tile={'tile_id':plan['tile_id'],'title': ' / '.join(bundles[c]['context']['concept_name'] for c in plan['concept_ids']), 'steps':[], 'remediation_steps':[]}
 for ps in plan['steps']:
  cs=ps['concept_ids']; c=cs[0]; typ=ps['type']
  s={'step_id':ps['step_id'],'type':typ,'concept_ids':copy.deepcopy(cs),'title':bundles[c]['context']['concept_name'],'lineage':{k:copy.deepcopy(ps[k]) for k in ['concept_ids','fact_ids','teaching_block_ids','segment_ids','anchors']}}
  if typ in ['check','hands_on']:
   s['title'],s['lede']=framing[c,typ]; s['eyebrow']='Check your understanding' if typ=='check' else 'Your turn'
   if c==A and ps['fact_ids']==[A+'#f3']:s['title']='Trace the shared inner list'
   if c==C and ps['fact_ids']==[C+'#f3']:s['title']='Interpret a tie'
   if c==D and ps['fact_ids']==[D+'#f2',D+'#f3']:s['title']='Reveal hidden text details'
  elif typ=='video':
   s['title']='Explore '+bundles[c]['context']['concept_name'].lower();s['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(ps['segment_ids'])}]
  elif typ=='explainer':
   if c==A and ps['planned_visual_block_type'] is None:
    s['title']='Follow outer and inner changes';s['blocks']=copy.deepcopy(alias_example)+[walk(A,visual=False)]
   else:
    s['blocks']=copy.deepcopy(texts[c])
    if c==Z:s['blocks'].append(zip_visual)
    elif c==A:s['blocks'].append(alias_diagram)
    elif c==C:s['blocks'] += [walk(C,counter_code,[ann(counter_code,'if pairs:', 'Guard first-pair access.')]),walk(C,empty_code,[ann(empty_code,'Counter([])','Empty input: inspect the returned list before indexing.')]),walk(C,tie_code,[ann(tie_code,'counts =','Tied counts: first encounter decides the order.')])]
    elif c==D:s['blocks'].append(walk(D,d_code,[ann(d_code,'repr(text)','Observe after the text reassignment, before conversion.'),ann(d_code,'converted quantity','Observe after the quantity binding.')]))
    elif c==H:s['blocks'].append(walk(H,annotations=[ann(codes[H],'"""','First statement: concise purpose summary.'),ann(codes[H],'Arguments','Calling details follow a blank line.'),ann(codes[H],'help(cost)','Inspect the signature and documentation.')]))
  else:
   s['title']='Takeaways';s['blocks']=[]
   for rc in cs:
    fs=[f['id'] for f in bundles[rc]['coverage']['required_facts']];s['blocks'].append(prose(rc,recaps[rc],fs,[tb['id'] for tb in bundles[rc]['teaching_blocks']],'takeaway'))
   idx=g['tile_order'].index(plan['tile_id']); next_tile=g['tile_order'][idx+1]
   next_plan=next((t for t in p['tiles'] if t['tile_id']==next_tile),None)
   next_concept=next_plan['concept_ids'][0] if next_plan else list(g['names'])[list(g['names']).index(cs[-1])+1]
   s['blocks'].append({'type':'up_next','title':g['names'][next_concept]})
  tile['steps'].append(s)
 out['tiles'].append(tile)
# One contrast for each distinct assessed fact set; broad first checks cover hands-on sets already taught there.
remediation={
 Z:[(['f3'],'Shortest input, not missing values',f'The labels list ends with {labels[-1]}, but that entry has no corresponding quantity. By default zip stops at the shortest input: it omits the unmatched tail rather than supplying a missing value.',['tb3','tb4','tb5']),(['f1','f2'],'Pair values, then bind them','zip(labels, quantities) forms tuples from corresponding positions. Use for label, quantity in zip(labels, quantities): with an indented body: label receives the label and quantity receives its corresponding quantity, not the whole tuple in each variable.',['tb2','tb3','tb4'])],
 A:[(['f1'],'New name versus new object','alias = original binds another name to the same list; it does not copy. An append through alias is visible through original and can affect a caller sharing that list. Different names do not imply independent objects.',['tb2','tb4','tb5']),(['f3'],'Separate outer list, shared inner element','copied = original.copy() separates the outer list but retains references to existing elements. A nested update through copied can therefore be visible through original. Separate outer lists do not imply separate nested mutable elements.',['tb3','tb4','tb5']),(['f2'],'Copy before changing the top level','Contrast copied = items with copied = items.copy() or copied = items[:]. The first shares the list; either copy form creates a separate outer list, allowing independent top-level changes. Appending to that copied outer list does not append to the caller’s outer list.',['tb2','tb3','tb4'])],
 C:[(['f1','f2','f3'],'A returned list, not a bare pair','Counter counts hashable elements into an element-to-count mapping. most_common(1) returns a list containing the most frequent pair, not the bare pair. An empty counter returns an empty list: check pairs before pairs[0]. Pairs descend by count; ties follow first encounter.',['tb1','tb2','tb3','tb4','tb5']),(['f3'],'First encounter, not a separate rank','With tied counts among the supplied labels, most_common follows first encounter. It orders by descending count first, not a separate label ranking. Check that the returned list is nonempty before accessing its first pair.',['tb3','tb4','tb5'])],
 D:[(['f1','f3'],'Observe the current binding','print(label, value) reveals state at that execution point. Place it after the binding or before the operation under investigation. A diagnostic before a later reassignment cannot reveal the later value. Remove that print to remove its diagnostic output.',['tb2','tb3','tb4','tb5']),(['f2','f3'],'Represent the text at the right point','Ordinary string display can obscure details; repr(text) returns a printable representation that exposes surrounding spaces and quotes in the supplied text. Observe after the relevant binding and before conversion, not before a later reassignment. Remove the diagnostic print when no longer needed.',['tb3','tb4','tb5'])],
 H:[(['f4'],'Inspect documentation, not the calculation','help(cost) displays the function’s signature and documentation, including its docstring. Contrast inspecting the interface with calling the helper to calculate a product.',['tb3','tb4']),(['f2','f3','f4'],'First-statement documentation','Put a string literal first in cost’s body, not later. Give a concise purpose summary, a blank line, then accurate numeric argument and returned-product details. Document exceptions when applicable, without inventing claims. help(cost) displays the signature and documentation.',['tb3','tb4','tb5'])]
}
for tile,plan in zip(out['tiles'],p['tiles']):
 for c in plan['concept_ids']:
  for fs,title,text_,tbs in remediation[c]:
   rid=tile['tile_id']+'.r'+str(len(tile['remediation_steps'])+1).zfill(2)
   tile['remediation_steps'].append({'step_id':rid,'type':'remediation','required':False,'concept_ids':[c],'title':title,'blocks':[prose(c,text_,fs,tbs)],'lineage':lin(c,fs,tbs)})
(B/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Wrote',B/'screens.json')
