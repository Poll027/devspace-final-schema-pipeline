import json,re,copy
from pathlib import Path
P=Path('batches/final_batch_learn_python.region.02_1')
plan=json.loads((P/'tile_plans.json').read_text())
g=json.loads((P/'inputs/path_glossary_bundle.json').read_text())
reg=json.loads((P/'scenario_asset_registry.json').read_text())
bs={b['context']['concept_id']:b for b in g['bundles']}
assets={a['asset_id']:a for a in reg['assets']}
# Fact-level re-voicing. Numeric defaults and scenario literals are read from the source below.
voices={
'collection_selection':[
'Use a list when ordered positions need updates: it is a mutable sequence.',
'A tuple is an immutable sequence for a fixed, ordered group.',
'Sets hold distinct hashable values, not sequence positions. They support membership tests and set operations.',
'A dictionary maps hashable keys to values and allows updates. It preserves insertion order, but lookup uses keys rather than sequence positions.'],
'console_input_output':[
'input(prompt) can display a prompt. It returns the entered text, leaving off the trailing newline.',
'print separates displayed values with spaces and finishes with a newline by default. Customize the separators with sep and the ending with end.'],
'enumerate_iteration':[
None,
'With an indented body, for position, value in enumerate(sequence, start=1): numbers entries from one. No manual counter update is needed.'],
'floating_point_limits':[
'Many decimal fractions have no exact binary floating-point representation.',
'math.isclose(a, b, rel_tol=..., abs_tol=...) uses relative and absolute tolerances instead of demanding exact equality.',None],
'indentation_and_blocks':[
'End a compound-statement header with a colon. Its multi-line body is indented; a nested body goes deeper.',
'Indentation groups statements. Dedenting ends the deeper group; inconsistent indentation can be invalid.',None],
'math_utilities':[
'Import math, then call math.sqrt(x) for the square root of x.',None],
'nested_collections':[
'Collections can hold other collections. Each successive index or key selects a value one level further inside.',
'To change a nested value, assign to the final selected list index or dictionary key.'],
'nested_loops':[
'Indent an inner for loop inside an outer for loop. The inner collection is traversed for each outer item.',
'With for row in rows: and an inner for cell in row:, finish the current row’s cells before moving to the next row.'],
'range_iteration':[None,
'The stop is excluded. Positive steps keep values below stop; negative steps keep values above stop.',None],
'running_scripts':[
'Choose the Python executable explicitly and pass the script path as its argument.',
'Script print output goes to standard output by default.',
'Zero exit status means successful termination; nonzero means abnormal termination. sys.exit(status) requests the status.'],
'statements_and_expressions':[
'An expression statement evaluates its expression. Interactive mode displays a non-None value.',
'Assignment first evaluates the right-hand expression, then binds its result to the target.',
'Expressions are evaluated left to right. Operator precedence and parentheses still determine how operations group.'],
'comments':[
'Outside a string, # begins a comment through the physical line’s end. Syntax ignores comments.',
'Update comments when code changes. A comment contradicting the code is worse than no comment.',
'Use inline comments sparingly. Explain a useful reason instead of repeating an obvious operation.'],
'interactive_execution':[
'Start the interpreter without a script for interactive mode. >>> marks a new command; ... marks continuation.',
'An entered expression displays its result. Later expressions can use variables assigned earlier in the session.',
'Copy commands without their prompt characters. In tutorial sessions, unprompted lines are output, not commands.'],
'interpreter_execution_model':[
'Source can compile to a code object. Invalid source syntax raises SyntaxError.',
'CPython compiles to bytecode that its interpreter uses. Bytecode is an implementation detail, not a guarantee across Python implementations.',
'Top-level module statements execute on first import or when the file runs as a script.',
'At runtime, assignment evaluates the expression using current values, then binds the result to its target.'],
'multiline_expressions':[
'Parentheses, square brackets and braces allow expressions to continue across physical lines without backslashes.',
'Keep the expression and delimiters intact when splitting a call. Continuation indentation does not group statement blocks.',
'Align continued arguments with the opening delimiter, or use a hanging indent.'],
'string_methods':[
'strip() removes leading and trailing whitespace, not whitespace inside the text.',
'The chars argument to strip describes removable edge characters, not a literal prefix or suffix.',
'lower() returns a copy with cased characters changed to lowercase.',
'With an explicit separator, split separates on that delimiter and keeps empty fields between repeated delimiters.',
'Without a separator, split() groups whitespace runs and omits leading and trailing empty fields.'],
'syntax_vs_runtime_errors':[
'Syntax errors happen during parsing. The report points to the line and location where the parser detected invalid syntax.',
'Valid syntax can still raise an exception during execution. Read the exception type and explanation in its error message.',
'Invalid syntax blocks compilation to an executable code object. Repair it before tracing that source’s runtime behavior.'],
 'truth_value_testing':[
'False, None, numeric zero, and empty built-in strings and collections test false. Nonzero numbers and nonempty built-in strings and collections test true.',
'Use if collection: for a nonempty guard, or if not collection: for an empty guard. No equality comparison to True is required.'],
'none_and_identity':[
'None is a singleton commonly used to mark an absent value.',
'is asks whether two operands are the same object; is not asks whether they are different objects.',
'Test absence with value is None or value is not None. A truth test also rejects legitimate zero or empty values.'],
'unicode_and_bytes':[
'str holds Unicode text; bytes holds binary data. They are distinct kinds of values.',None,
'Decode UTF-8 bytes with payload.decode("utf-8") to get text. Match the decoding encoding to the encoded data to recover that text.',
'Bytes invalid for the chosen decoding cause a decoding failure: UnicodeDecodeError.']}
contrasts={
'collection_selection':'Insertion order does not make dictionary lookup positional: it uses keys. Sets also have no sequence positions, even when a display looks ordered.',
'console_input_output':'The prompt is displayed, but it is not part of the returned input text.',
'enumerate_iteration':'Changing the display counter’s start does not change list indexing.',
'floating_point_limits':'Near zero, the default absolute tolerance supplies no positive allowance.',
'indentation_and_blocks':'Dedenting moves a statement out of a deeper group; indentation is not merely decoration.',
'math_utilities':'A real-valued square-root operation is not a request for a complex result.',
'nested_collections':'Follow the selections inward; update the final selection, not the outer container.',
'nested_loops':'Finish the inner traversal for the current row before advancing the outer loop.',
'range_iteration':'The stop is an excluded boundary, not a guaranteed final value.',
'running_scripts':'A printed message and a process exit status are different signals.',
'statements_and_expressions':'Left-to-right evaluation does not cancel operator precedence.',
'comments':'A comment does not prove that the code implements its description.',
'interactive_execution':'Prompt markers identify input; they are not source to type.',
'interpreter_execution_model':'CPython bytecode is not a universal promise about every implementation.',
'multiline_expressions':'Continuation spacing is not compound-statement block grouping.',
'string_methods':'Removing edge whitespace is not the same operation as splitting fields.',
'syntax_vs_runtime_errors':'Repair invalid syntax before inventing a runtime trace for it.',
'truth_value_testing':'An empty guard uses not; a nonempty guard uses the collection itself.',
'none_and_identity':'False truth is not the same as absence.',
'unicode_and_bytes':'Encoded bytes are not already Unicode text.'}
recaps={
'collection_selection':'Choose lists for editable positions, tuples for fixed ordered groups, sets for distinct membership, and dictionaries for key lookup. Dictionary insertion order does not make lookup positional.',
'console_input_output':'Input returns text without the trailing newline. Print controls displayed separators and endings.',
'enumerate_iteration':'Enumerate pairs a counter with each element; changing its start does not change list indices.',
'floating_point_limits':'Many decimal fractions are approximate as binary floats. Compare with suitable tolerances; near zero, use a positive absolute tolerance when small differences should count as close.',
'indentation_and_blocks':'Colons introduce multi-line bodies. Indentation defines grouping, nested bodies go deeper, and dedenting ends a deeper group. Repair each level with four spaces.',
'math_utilities':'Import math to use math.sqrt. These functions operate on real values; an invalid real-valued operation can raise ValueError.',
'nested_collections':'Follow successive indices and keys inward; assign to the final selection to update a nested value.',
'nested_loops':'The inner loop finishes the current row’s cells before the outer loop advances.',
'range_iteration':'Range excludes stop. Choose start and a nonzero step with the intended direction.',
'running_scripts':'Run a script with the explicitly chosen executable. Printed output and exit status are different signals.',
'statements_and_expressions':'Assignment evaluates before binding. Precedence and parentheses group operations within left-to-right evaluation.',
'comments':'Keep comments accurate and explain useful reasons, not obvious operations.',
'interactive_execution':'Interactive prompts distinguish new commands from continuation; do not type the prompt markers.',
'interpreter_execution_model':'Valid source can compile to a code object. CPython bytecode is implementation-specific; runtime assignments use current values.',
'multiline_expressions':'Continue inside matching delimiters; continuation spacing is not block grouping.',
'string_methods':'Strip cleans edges, lower changes case, and split separates fields. Strip’s chars argument is a character set, not a literal substring. Explicit separators keep empty fields between repeated delimiters; whitespace splitting groups whitespace runs.',
'syntax_vs_runtime_errors':'Syntax errors arise during parsing; runtime exceptions arise during execution. Read the reported location or exception explanation, and fix invalid syntax before tracing runtime behavior.',
'truth_value_testing':'Empty built-in collections test false; nonempty ones test true. Use the collection or not collection as the guard.',
'none_and_identity':'None commonly marks absence. Identity checks distinguish it from legitimate zero or empty values that a truth test rejects.',
'unicode_and_bytes':'Unicode text and binary bytes are distinct. Encode to bytes, then decode with the matching encoding to recover text. Invalid bytes for the decoding raise UnicodeDecodeError.'}

def cidshort(c):return c.split('.')[-1]
def tbmap(c):return {x['id']:x for x in bs[c]['teaching_blocks']}
def facts(c):return bs[c]['coverage']['required_facts']
def ftext(c,fid):
 ix=next(i for i,f in enumerate(facts(c)) if f['id']==fid)
 return voices[cidshort(c)][ix] or facts(c)[ix]['statement']
def line(c,tbs,fids,anchor=False):
 return {'concept_ids':[c], 'teaching_block_ids':[c+'#'+x for x in tbs], 'fact_ids':[c+'#'+x for x in fids], **({'anchors':[c+'#visual']} if anchor else {})}
def prose(c,text,tbs,fids,role='mechanism'):
 return {'type':'prose','text':text,'role':role,'lineage':line(c,tbs,fids)}
def sources_for(c,fids):return [tb['id'] for tb in bs[c]['teaching_blocks'] if set(tb['fact_ids']) & set(fids)]
def fact_blocks(c,fids,allowed=None):
 out=[]
 for fid in fids:
  src=sources_for(c,[fid])
  if allowed is not None:src=[x for x in src if x in allowed]
  out.append(prose(c,ftext(c,fid),src,[fid],'definition'))
 return out

def source_code(c):
 text=tbmap(c)['tb4']['content']
 matches=re.findall(r'```(?:python|text)\n(.*?)```',text,re.S)
 if matches:
  code=matches[0].strip()
  if cidshort(c)=='interactive_execution':
   code='\n'.join(x[4:] for x in code.splitlines() if x.startswith('>>> '))
  return code
 aid='cw.'+cidshort(c)
 if aid in assets:return assets[aid]['files'][0]['content'].strip()
 raise ValueError(c)

def cw(c,code,annotation=None,tbs=None,fids=None):
 fids=fids or [x['id'] for x in facts(c)]
 return {'type':'code_walkthrough','language':'python','code':code,'annotations':[{'start_line':1,'end_line':len(code.splitlines()),'text':annotation or contrasts[cidshort(c)]}], 'lineage':line(c,tbs or ['tb4'],fids,True)}

def visual(c,s):
 short=cidshort(c); typ=s['planned_visual_block_type']; tbs=[x.split('#')[-1] for x in s['teaching_block_ids']];fids=[x.split('#')[-1] for x in s['fact_ids']]
 lin=line(c,tbs,fids,True)
 if short=='collection_selection':
  # Literal examples and their numeric values are lifted from the glossary.
  text=tbmap(c)['tb4']['content']
  literals=re.findall(r'(\[[^\]]+\]|\([^\)]+\)|\{[^\}]+\})',text)[:4]
  labels=['List: editable positions','Tuple: fixed ordered group','Set: distinct membership','Dictionary: key lookup']
  cells=['Mutable sequence; access by position.','Immutable sequence; fixed ordered values.','Distinct hashable values; membership and set operations; no sequence positions.','Hashable keys map to values; updates and insertion order; lookup by key.']
  return [{'type':'comparison','columns':[{'id':'example','label':'Order helper collection'},{'id':'access','label':'Access and updates'}], 'rows':[{'criterion':labels[i], 'cells':{'example':v,'access':cells[i]}} for i,v in enumerate(literals)],'lineage':lin}]
 if short=='running_scripts':
  # There are no rendered images in this registry: draw the terminal state as a diagram.
  text=tbmap(c)['tb4']['content']
  command=re.search(r'form (.*?) runs it',text).group(1)
  script=re.search(r'(report\.py) contains (print\([^)]*\))',text)
  nodes=[{'id':'file','label':script.group(1),'fields':[script.group(2)]}, {'id':'command','label':command,'fields':['Replace the executable placeholder with the actual chosen executable.']}, {'id':'stdout','label':'Standard output','fields':['print sends its message here by default.']}, {'id':'status','label':'Process exit status','fields':[ftext(c,'f3')]}]
  return [{'type':'diagram','diagram_kind':'container','title':'Terminal: invocation and separate signals','nodes':nodes,'edges':[{'from':'file','to':'command'},{'from':'command','to':'stdout'},{'from':'command','to':'status'}],'alt_text':'A saved script is passed to a chosen executable. Standard output and process exit status are shown as separate signals.','lineage':lin}]
 if short=='interpreter_execution_model':
  code=assets['cw.'+short]['files'][0]['content'].strip()
  flow={'type':'process_flow','nodes':[{'id':'source','label':'Source'},{'id':'parse','label':'Parse syntax','kind':'decision'},{'id':'invalid','label':'SyntaxError'},{'id':'compile','label':'Compile to code object','detail':'CPython produces implementation-specific bytecode.'},{'id':'runtime','label':'Execute top-level statements','detail':'First import or script execution; assignment evaluates current values, then binds.'}], 'edges':[{'from':'source','to':'parse'},{'from':'parse','to':'invalid','label':'Invalid syntax'},{'from':'parse','to':'compile','label':'Valid syntax'},{'from':'compile','to':'runtime'}], 'alt_text':'Source is parsed; invalid syntax raises SyntaxError. Valid source can compile to a code object and execute; CPython bytecode is implementation-specific.','lineage':lin}
  return [{'type':'side_by_side','left':flow,'right':cw(c,code,'At runtime, the second assignment uses the value bound by the first.',tbs,fids),'left_label':'From source to execution','right_label':'Runtime bindings','takeaway':'Compilation validity and runtime evaluation are separate stages.','lineage':lin}]
 if short=='syntax_vs_runtime_errors':
  bad=source_code(c); good=bad.replace('if quantity > 0\n','if quantity > 0:\n')
  return [{'type':'before_after','before':cw(c,bad,'The header is missing its colon. Parsing detects invalid syntax; repair it before tracing execution.'),'after':cw(c,good,'The colon repairs syntax. The conversion still raises ValueError during execution; read its exception type and explanation.'),'change_summary':'Repairing source structure is separate from investigating the runtime value.','lineage':lin}]
 code=source_code(c)
 if short=='unicode_and_bytes':
  equality=re.search(r'(restored == text)',s['visual_purpose']).group(1)
  code+='\nprint('+equality+')'
 if short=='multiline_expressions':
  before=assets['cw.'+short]['files'][0]['content'].strip()
  return [{'type':'side_by_side','left':cw(c,before,'The calculation and call occupy single lines.'),'right':cw(c,code,'Matching parentheses preserve the expressions; arguments use a hanging indent.'),'left_label':'Single-line form','right_label':'Continued form','takeaway':contrasts[short],'lineage':lin}]
 if short=='string_methods':
  lines=code.splitlines()
  left='\n'.join(lines[:2]+[lines[-1]])
  right='\n'.join(lines[2:-1])
  return [{'type':'side_by_side','left':cw(c,left,'Strip removes edge whitespace, not interior whitespace. Lower returns a lowercase copy; strip chars are removable characters.'),'right':cw(c,right,'An explicit delimiter preserves empty fields between repeated delimiters; whitespace splitting groups runs and omits edge empty fields.'),'left_label':'Clean edges and change case','right_label':'Separate fields','takeaway':contrasts[short],'lineage':lin}]
 return [cw(c,code)]

out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out['kind']='screens_part';out['tiles']=[]
for ti,t in enumerate(plan['tiles']):
 title=' · '.join(bs[c]['context']['concept_name'] for c in t['concept_ids'])
 tile={'tile_id':t['tile_id'],'title':title,'steps':[],'remediation_steps':[]}
 seen=set()
 for s in t['steps']:
  c=s['concept_ids'][0];short=cidshort(c);typ=s['type']
  slin={k:copy.deepcopy(s[k]) for k in ['fact_ids','teaching_block_ids','segment_ids','anchors']}
  step={'step_id':s['step_id'],'type':typ,'concept_ids':s['concept_ids'],'eyebrow':{'explainer':'Learn','check':'Check your understanding','hands_on':'Try it','video':'Optional walkthrough','recap':'Takeaways'}[typ],'title':bs[c]['context']['concept_name'],'lineage':slin}
  if typ=='explainer':
   tbs=[x.split('#')[-1] for x in s['teaching_block_ids']]
   fids=[x.split('#')[-1] for x in s['fact_ids']]
   # First screen teaches the facts; follow-up screen supplies the contrast and examples.
   if 'tb2' in tbs:
    step['blocks']=fact_blocks(c,fids,tbs)
   else:
    if short=='collection_selection':
     example=tbmap(c)['tb4']['content']
     literals=re.findall(r'(\[[^\]]+\]|\([^\)]+\)|\{[^\}]+\})',example)[:4]
     text='Use '+literals[0]+' for editable quantities, '+literals[1]+' for fixed bounds, '+literals[2]+' for distinct labels, and '+literals[3]+' for quantities by label. Choose by the access and update needed, not literal length.'
    else:
     code=assets['cw.'+short]['files'][0]['content'].strip()
     text='In `'+code.replace('\n','`, then `')+'`, the second assignment uses the current value bound by the first. Top-level statements execute on first import or when the file runs as a script. Invalid source syntax raises SyntaxError when compilation is attempted. CPython produces bytecode for its interpreter, but that is not guaranteed across implementations.'
    step['blocks']=[prose(c,text,[tbs[0]],fids,'example'),prose(c,contrasts[short],[tbs[-1]],[x for x in tbmap(c)[tbs[-1]]['fact_ids']],'misconception')]
   if s['planned_visual_block_type']:
    step['blocks']+=visual(c,s)
  elif typ=='video':step['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(s['segment_ids'])}]
  elif typ=='recap':
   step['title']='Keep these distinctions'
   step['blocks']=[]
   for rc in s['concept_ids']:
    fids=[x['id'] for x in facts(rc)]
    step['blocks'].append(prose(rc,recaps[cidshort(rc)],sources_for(rc,fids),fids,'takeaway'))
   nextid=t['next_tile_id']
   if ti+1<len(plan['tiles']):nextname=bs[plan['tiles'][ti+1]['concept_ids'][0]]['context']['concept_name']
   else:
    # Tile 046's first idea is named by the glossary's ordering and names.
    name_order=list(g['names']); nextconcept=name_order[name_order.index(t['concept_ids'][-1])+1]
    nextname=g['names'][nextconcept]
   step['blocks'].append({'type':'up_next','title':nextname,'text':'Next: '+nextname+'.'})
  elif typ=='hands_on':
   if s['planned_interaction_type'] in ['classify','choice']:
    step['eyebrow']='Review the supplied examples';step['title']='Judge '+bs[c]['context']['concept_name'].lower()
    step['lede']='Read the supplied excerpts in this step and decide which are correct or defective for the stated task.'
   else:
    step['title']='Practice '+bs[c]['context']['concept_name'].lower()
    step['lede']=bs[c]['practice_anchor']['objective']
  else:
   step['title']='Choose the right distinction'
   step['lede']='Use what you learned about '+bs[c]['context']['concept_name'].lower()+' to choose the answer.'
  tile['steps'].append(step)
  if typ in ['check','hands_on']:
   fids=[x.split('#')[-1] for x in s['fact_ids']]
   if not fids:fids=[x['id'] for x in facts(c)]
   key=(c,tuple(fids))
   if key not in seen:
    seen.add(key)
    rlin=line(c,sources_for(c,fids),fids)
    blocks=fact_blocks(c,fids)
    blocks.append(prose(c,contrasts[short],['tb5'],tbmap(c)['tb5']['fact_ids'],'misconception'))
    # Same supplied example, one conceptual contrast; no answer key or computed output.
    if short=='collection_selection':
     sample=re.findall(r'(\[[^\]]+\]|\([^\)]+\)|\{[^\}]+\})',tbmap(c)['tb4']['content'])[:4]
     example='For the order helper, compare positional quantities '+sample[0]+' with quantities by label '+sample[3]+'. One selects positions; the other selects keys.'
    elif short=='running_scripts':example='In the saved report example, inspect printed messages separately from the process status.'
    elif short=='string_methods':example='In the supplied label examples, distinguish cleaning edges from choosing how to split fields.'
    else:example=None
    if example:
     blocks.append(prose(c,example,['tb4'],fids,'example'))
    else:
     blocks.append(cw(c,source_code(c),contrasts[short],sources_for(c,fids),fids))
    tile['remediation_steps'].append({'step_id':t['tile_id']+'.r'+str(len(tile['remediation_steps'])+1).zfill(2),'type':'remediation','concept_ids':[c],'eyebrow':'A second look','title':'Review '+bs[c]['context']['concept_name'].lower(),'blocks':blocks,'lineage':rlin})
 out['tiles'].append(tile)
(P/'screens.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Tiles:',len(out['tiles']),'Planned steps:',sum(len(t['steps']) for t in out['tiles']),'Remediation:',sum(len(t['remediation_steps']) for t in out['tiles']))
