import json, re, copy
from pathlib import Path
P=Path('batches/final_batch_learn_python.region.04')
plan=json.loads((P/'tile_plans.json').read_text())
g=json.loads((P/'inputs/path_glossary_bundle.json').read_text())
reg=json.loads((P/'scenario_asset_registry.json').read_text())
B={b['context']['concept_id']:b for b in g['bundles']}
A={a['asset_id']:a for a in reg['assets']}
# Each entry re-voices exactly one required fact, in the glossary's order.
texts={
'classes_and_instances':[
'An indented body after `class Order:` creates the class object Order. Use `pass` when that body is empty.',
'Calling an ordinary class creates a new instance. Two calls to `Order()` create two distinct instances.',
'Use `is` to test object identity. `first is second` asks whether the names refer to the same object; an alias shares identity, unlike two separate instances.'],
'file_modes':[
'`open(path, "r")` reads an existing file. With no mode argument, `r` is the default.',
'`w` writes: it truncates an existing file or creates a new one.',
'`a` appends to an existing file, or creates it if absent.',
'`x` exclusively creates a new file and fails if the destination already exists.',
'Handle `FileExistsError` when exclusive creation finds an existing report. Do not silently switch to a mode that truncates it.'],
'instance_initialization':[
'When a class defines `__init__`, instantiation automatically calls it on the new instance with the constructor arguments.',
'Define `__init__(self, label, quantity)` inside Order. Assign `self.label = label` and `self.quantity = quantity` to store those arguments as instance attributes.',
'`__init__` initializes the instance already created. It does not return a replacement object.'],
'instance_methods':[
'An instance method receives its target instance as the first argument, conventionally called `self`.',
'Define `add(self, amount)` inside Order. Use `self.quantity` to read or reassign the receiving instance’s state.',
'In `order.add(2)`, order is supplied implicitly as self, and the explicit value is supplied as amount. Do not pass order again.'],
'class_and_static_methods':[
'An ordinary instance method receives the instance implicitly and can use that instance’s state.',
'Put `@classmethod` above `def from_text(cls, text):`. The implicit argument is the class. Returning `cls(int(text))` constructs an instance through an alternative constructor.',
'Put `@staticmethod` above the method definition for an operation such as cost that receives no implicit instance or class argument. Its arguments are explicit.'],
'composition':[
'An instance attribute can hold another object as a collaborator, rather than holding the result of its work.',
'Store the Calculator object as `self.calculator`. Within Report’s method, call `self.calculator.cost(quantity)` to delegate work through the stored object.'],
'encapsulation_conventions':[
'A leading underscore marks a name as conventionally non-public. It is not an access restriction.',
'This naming convention does not make Python instance attributes truly inaccessible.',
'Public attributes are the interface clients are expected to use. Mark implementation details with a leading underscore.',
'Expose a public method such as `add` that operates on the receiving instance’s supporting attributes. Callers need not manage `_quantity` directly.'],
'inheritance_and_super':[
'`class FeeOrder(Order):` inherits from Order. An override replaces the inherited method for ordinary lookup on FeeOrder instances.',
'Inside an ordinary derived instance method, `super().method(arguments)` delegates lookup to the next class in method resolution order, not unconditionally to a fixed named parent.',
'In the derived initializer, use `super().__init__(quantity)` to run inherited initialization before adding the derived fee state where required.'],
'custom_exceptions':[
'Define an application-specific exception with `class InvalidRecordError(Exception):` and an indented `pass` body.',
'`raise InvalidRecordError(message)` signals the custom failure. A surrounding `except InvalidRecordError:` handles that failure at the caller’s recovery boundary.'],
'instance_vs_class_attributes':[
'Class variables hold attributes shared by instances; instance variables hold data unique to an instance.',
'A mutable list assigned in the class body is shared by instances unless an instance attribute shadows it.',
'Assign `self.labels = []` in `__init__` for a new list on each instance. Then updating first’s list does not mutate a shared class list.'],
'json_serialization':[
'`json.dumps(value)` serializes supported Python values to a JSON string.',
'`json.loads(text)` deserializes JSON text into Python values.',
'Default conversions support dictionaries, lists, tuples, strings, numbers, booleans and None. Both lists and tuples encode as arrays, which decode as lists.',
'JSON object keys are strings. A non-string dictionary key need not retain its original Python type after a round trip.'],
'object_introspection':[
'`type(order)` returns the object’s type.',
'`isinstance(order, Order)` checks membership in Order or one of its subclasses.',
'`dir(order)` attempts to list relevant attribute names; completeness is not guaranteed.',
'`getattr(order, name)` retrieves a named attribute. Supply an optional fallback for an absent attribute.',
'Underscore-prefixed names conventionally signal internal use rather than the public interface.'],
'pathlib_filesystem_operations':[
'`mkdir(parents=True, exist_ok=True)` creates the directory and missing parents, allowing an existing directory; both options default to False.',
'`directory.iterdir()` traverses immediate entries in arbitrary order.',
'`source.rename(target)` moves or renames the entry. Relative targets use the working directory, not the source’s parent.',
'Rename can silently replace an existing target file on Unix when permitted; on Windows it raises `FileExistsError`.',
'Build `target = directory / filename` to select the output directory, not a bare relative filename.'],
'special_methods':[
'Define `__repr__(self)` to return a string with an information-rich, unambiguous representation for repr and interactive inspection.',
'Define `__str__(self)` to return a convenient user-facing string for str and print.',
'If `__str__` is absent, the default representation uses `__repr__`. Return strings from these methods; do not replace the return with printing.'],
 'text_file_encodings':[
'Use `open(path, "r", encoding="utf-8")` to decode UTF-8 text and `open(path, "w", encoding="utf-8")` to explicitly encode written text.',
'The encoding argument specifies how text is encoded. Correct decoding requires the selected encoding to match the file’s bytes.',
'`UnicodeDecodeError` signals a decoding failure; bytes invalid for the selected encoding can cause it. A filename does not establish its encoding.'],
'file_and_format_errors':[
'`FileNotFoundError` means the requested file or directory does not exist. Handle it separately from content problems.',
'`UnicodeDecodeError` indicates content could not be decoded using the selected encoding.',
'`csv.Error` reports parser-detected errors; use a matching handler for parsing failures.',
'DictReader fills missing fields with restval and stores excess fields under restkey; both default to None. Validate required fields explicitly, rather than assuming wrong row lengths raise `csv.Error`.',
'At the import boundary, use specific handlers for missing files, decoding failures and parser failures. Report each according to its cause.'],
'with_resource_management':[
'Use `with context_expression as resource:` followed by an indented body. The context manager enters before that body and exits afterward.',
'After entry succeeds, exit runs on normal completion or a raised body exception. A general context manager may suppress an exception.',
'For `with open(path) as f:`, leaving the body closes the file even when the body raises. Keep this file-closing behavior distinct from general exception suppression.'],
'binary_files':[
'Binary mode `b` uses bytes rather than strings: `rb` reads bytes and `wb` writes bytes.',
'`wb` creates or truncates the destination. Choose a destination whose replacement is intended.',
'Assign `source.read()` to payload and pass that bytes value directly to `destination.write(payload)` to copy without text decoding.',
'Manage both openings with `with` so each file closes after its managed body.']}
# Short scenario contrasts used by conditional re-teaching.
contrasts={
'classes_and_instances':'Compare two Order calls with `alias = first`: separate creation versus another name for the same object.',
'file_modes':'For an existing report.txt, exclusive creation fails; switching to w would replace the report instead of preserving it.',
'instance_initialization':'Storing label on self initializes the Order; returning a replacement object is a different operation.',
'instance_methods':'In order.add(2), the receiving order is implicit; amount is explicit.',
'class_and_static_methods':'Order.from_text receives cls implicitly; Order.cost receives only its explicit arguments.',
'composition':'Report stores the Calculator object and calls through it, not through a saved cost result.',
'encapsulation_conventions':'Use order.add to operate on _quantity; the underscore signals internal use, not a locked attribute.',
'inheritance_and_super':'FeeOrder extends inherited initialization and formatting through super rather than treating super as a fixed-parent name.',
'custom_exceptions':'A raised InvalidRecordError reaches its matching handler; printing a failure label alone does not signal that exception.',
'instance_vs_class_attributes':'A class-body labels list is shared; assigning self.labels during initialization creates separate lists.',
'json_serialization':'A successful round trip can preserve values without preserving every Python type: tuples return as lists.',
'object_introspection':'Treat dir(order) as candidate names, not a complete public-interface specification.',
'pathlib_filesystem_operations':'Use directory / filename, not a bare relative filename whose location depends on the working directory.',
'special_methods':'Return a representation string from the method rather than printing it inside the method.',
'text_file_encodings':'Read label.txt with an encoding matching its bytes, not one guessed from its filename.',
'file_and_format_errors':'A missing quantity is row data to validate; it is not automatically a parser exception.',
'with_resource_management':'An opened file closes on either exit path; general managers may also suppress an exception.',
'binary_files':'Pass bytes directly to the destination; do not turn this copy into a text-decoding operation.'}
practice_titles={
'classes_and_instances':'Create separate Order instances','file_modes':'Create a report without replacement',
'instance_initialization':'Store constructor arguments','instance_methods':'Update the receiving Order',
'class_and_static_methods':'Construct through cls','composition':'Replace the collaborator',
'encapsulation_conventions':'Expose the public operation','inheritance_and_super':'Extend Order behavior',
'custom_exceptions':'Signal and handle an invalid record','instance_vs_class_attributes':'Give each Order its own list',
'json_serialization':'Inspect a JSON round trip','object_introspection':'Inspect an Order object',
'pathlib_filesystem_operations':'Move the report to its output directory','special_methods':'Return two representations',
'text_file_encodings':'Preserve the UTF-8 label','file_and_format_errors':'Handle import causes and validate rows',
'with_resource_management':'Manage both file exit paths','binary_files':'Copy the binary payload'}

def short(c):return c.split('.',1)[1]
def name(c):return B[c]['context']['concept_name']
def tbs(c,fids,allowed=None):
 return [c+'#'+t['id'] for t in B[c]['teaching_blocks'] if set(t['fact_ids']) & {f.split('#')[1] for f in fids} and (allowed is None or c+'#'+t['id'] in allowed)]
def lin(c,fids,allowed=None,visual=False):
 d={'concept_ids':[c],'teaching_block_ids':tbs(c,fids,allowed),'fact_ids':fids}
 if visual:d['anchors']=[c+'#visual']
 return d

def prose(c,text,fids,allowed=None,role='definition'):
 return {'type':'prose','text':text,'role':role,'lineage':lin(c,fids,allowed)}
def fact_blocks(c,fids,allowed=None):
 return [prose(c,texts[short(c)][int(f.split('#f')[1])-1],[f],allowed) for f in fids]

def code_example(c):
 b=B[c]
 for t in b['teaching_blocks']:
  m=re.search(r'```python\n(.*?)```',t['content'],re.S)
  if m:return m.group(1).strip()
 raise ValueError(c)

# Reuse source code, replacing only scenario-specific pieces where registry differs.
codes={c:code_example(c) for c in B if any('```python' in t['content'] for t in B[c]['teaching_blocks'])}
# Complete registered scaffolds without authoring results.
for c in ['python.json_serialization','python.object_introspection']:
 starter=A['ws.'+short(c)]['files'][0]['content']
 if short(c)=='json_serialization':
  prefix=starter.split('#')[0].rstrip()
  codes[c]=prefix+'\ntext = json.dumps(record)\nrestored = json.loads(text)\nprint(restored["quantities"])\nprint(type(restored["quantities"][0]))\nprint(restored["active"])'
 else:
  prefix=starter.split('#')[0].rstrip()
  codes[c]=prefix+'\nprint(type(order))\nprint(isinstance(order, Order))\nprint(getattr(order, "quantity"))\nprint(getattr(order, "missing", None))\nprint(dir(order))'
c='python.custom_exceptions'
codes[c]=codes[c].replace('InvalidOrder','InvalidRecordError')
c='python.inheritance_and_super'
base=A['ws.inheritance_and_super']['files'][0]['content'].split('#')[0].rstrip()
codes[c]=base+'\n\nclass FeeOrder(Order):\n    def __init__(self, quantity, fee):\n        super().__init__(quantity)\n        self.fee = fee\n    def format(self):\n        return super().format() + f", fee: {self.fee}"\n\nprint(FeeOrder(3, 2).format())'
c='python.text_file_encodings'
# This concept precedes managed resource blocks; use its permitted explicit close sequence.
codes[c]='source = open("label.txt", "r", encoding="utf-8")\ntext = source.read()\nsource.close()\ndestination = open("label.txt", "w", encoding="utf-8")\ndestination.write(text)\ndestination.close()\nprint(text)'
c='python.file_and_format_errors'
starter=A['ws.file_and_format_errors']['files'][0]['content']
# Retain the registry helper and its cleanup; replace the unfinished row validation and handlers below.
codes[c]=starter.replace(
    '            # Validate missing/empty required fields and excess fields.\n            rows.append(row)',
    '            if row["label"] is None or row["label"] == "" or row["quantity"] is None or row["quantity"] == "" or None in row:\n                return "Invalid row"\n            rows.append(row)'
).replace('    # Add cause-specific exception handlers here.',
    '    except FileNotFoundError:\n        return "Missing source"\n    except UnicodeDecodeError:\n        return "Decoding failure"\n    except csv.Error:\n        return "Parser failure"')
for filename in ['valid.csv','missing.csv','excess.csv']:
    path=next(f['path'] for f in A['ws.file_and_format_errors']['files'] if f['path']==filename)
    codes[c] += '\nprint(import_rows('+repr(path)+'))'
annotations_placeholder = None

annotations={
'file_and_format_errors':[('if row[', 'Validate required fields and excess fields independently of parser failures.'),('except FileNotFoundError', 'Missing source: not a content problem.'),('except UnicodeDecodeError', 'Failure to decode with the selected encoding.'),('except csv.Error', 'Handle errors actually reported by the CSV parser.'),('finally:', 'Close an opened file at this boundary.')],
'instance_initialization':[('def __init__','Instantiation passes the constructor arguments to the new instance’s initializer.'),('self.label =','Store label on the receiving instance.'),('self.quantity =','Store quantity on that same instance.')],
'instance_methods':[('def add','The first argument is the receiving instance, conventionally self.'),('self.quantity = self.quantity','Read and reassign the receiving instance’s quantity.'),('order.add','The target order is implicit self; the explicit argument binds amount.')],
'class_and_static_methods':[('@classmethod','This decorator supplies the class as cls.'),('return cls','Construct through the received class.'),('@staticmethod','No implicit instance or class is supplied.'),('Order.cost','Only quantity and price are explicit arguments.')],
'composition':[('self.calculator =','Keep the collaborator object as instance data.'),('self.calculator.cost','Delegate through the stored Calculator object.')],
'encapsulation_conventions':[('self._quantity = quantity','The underscore signals supporting state, not enforced access protection.'),('def add','Public operation for clients.'),('order.add','The caller uses the public interface.')],
'inheritance_and_super':[('super().__init__','Inherited initialization precedes the added fee state.'),('super().format','Delegate lookup to the next class in method resolution order, then extend its formatting.')],
'custom_exceptions':[('class InvalidRecordError','Exception subclass with an empty body.'),('raise InvalidRecordError','Negative quantity signals the application-specific failure.'),('except InvalidRecordError','The surrounding boundary handles the matching custom failure.')],
'object_introspection':[('print(type','Inspect the object’s type.'),('print(isinstance','Class membership includes subclasses.'),('print(getattr(order, "quantity"','Retrieve the quantity attribute by name.'),('print(getattr(order, "missing"','Use a fallback when the named attribute is absent.'),('print(dir','Candidate relevant names, not a guaranteed complete public API; underscores signal internal use.')],
'special_methods':[('def __repr__','Return an information-rich string for repr and inspection.'),('def __str__','Return a user-facing string for str and print.'),('print(repr','Use __repr__.'),('print(order)','Use __str__; without it the default uses __repr__.')],
 'text_file_encodings':[('source = open','Explicit UTF-8 decoding must match the source bytes.'),('source.close','Close the reader before rewriting the file.'),('destination = open','Explicit UTF-8 encoding for the saved text.')],
'binary_files':[('with open("source.bin"','Managed rb source reads bytes and closes at outer exit.'),('with open("copy.bin"','Managed wb destination creates or truncates; closes at inner exit.'),('payload =','Keep the read value as bytes.'),('destination.write','Write those bytes unchanged, with no text decoding.')]
}
def cw(c,code=None,notes=None):
 code=code or codes[c]
 anns=[]
 for needle,text in (notes if notes is not None else annotations.get(short(c),[])):
  matches=[i for i,l in enumerate(code.splitlines(),1) if needle in l]
  if matches:anns.append({'start_line':matches[0],'end_line':matches[0],'text':text})
 return {'type':'code_walkthrough','language':'python','code':code,'annotations':anns,'reveal':'all'}
def diagram(labels,edges,title):
 return {'type':'diagram','diagram_kind':'mapping','title':title,'nodes':[{'id':i,'label':s} for i,s in labels], 'edges':[{'from':a,'to':b,'label':s,'directed':True} for a,b,s in edges],'alt_text':title}
def flow(labels,edges,title):
 return {'type':'process_flow','title':title,'direction':'LR','nodes':[{'id':i,'label':s} for i,s in labels], 'edges':[{'from':a,'to':b,'label':s} for a,b,s in edges],'alt_text':title}

def visual(c,s):
 k=short(c)
 if k=='classes_and_instances':
  v=diagram([('class','Order: class object'),('one','First Order instance'),('two','Second Order instance'),('first','first'),('second','second'),('alias','alias')],[('class','one','first = Order()'),('class','two','second = Order()'),('first','one','refers to'),('alias','one','alias = first'),('second','two','refers to')],'Two ordinary calls create distinct instances; alias and first share one object')
 elif k=='file_modes':
  initial=next(f['content'] for f in A['ws.file_modes.existing']['files'] if f['path']=='report.txt')
  example=next(t['content'] for t in B[c]['teaching_blocks'] if t['purpose']=='example')
  appended=re.search(r'writing (\w+) appends',example).group(1)
  v={'type':'before_after','before':diagram([('report','report.txt contents: '+initial)],[],'Before each independent mode choice'),'after':diagram([('r','r: prior contents retained'),('a','a: retain contents, then append '+appended),('w','w: remove prior contents before writing'),('x','x: retain contents; raise FileExistsError')],[],'After opening and the described operation'),'change_summary':'Each mode starts from the same existing report. Exclusive creation does not replace it.'}

 elif k=='instance_vs_class_attributes':
  before=A['ws.instance_vs_class_attributes']['files'][0]['content'].strip()
  v={'type':'side_by_side','left_label':'Shared class list','right_label':'Separate instance lists','left':cw(c,before,[('labels = []','Class-body list shared unless shadowed.'),('first.labels.append','Mutates the shared list.')]),'right':cw(c,codes[c],[('self.labels = []','Create a new list for each instance.'),('first.labels.append','Only first’s instance list is changed.')]),'takeaway':'Move labels initialization onto self to isolate each Order’s mutable state.'}
 elif k=='json_serialization':
  v=flow([('record','Python record: quantities and active'),('text','JSON str'),('restored','Reconstructed Python values'),('tuple','Nested tuple becomes a list'),('active','Boolean value retained')],[('record','text','json.dumps(record)'),('text','restored','json.loads(text)'),('restored','tuple','arrays decode as lists'),('restored','active','boolean conversion')],'A JSON round trip preserves supported values, but not every Python type')
  # Include executable value inspection as a second visual block later.
 elif k=='with_resource_management':
  v=flow([('entry','Successful file entry'),('body','Indented read/process body'),('normal','Normal completion'),('raised','Body raises'),('closed','File closes at exit')],[('entry','body','enter before body'),('body','normal','finishes'),('body','raised','exception'),('normal','closed','exit'),('raised','closed','exit')],'After entry succeeds, both body exit paths close the opened file')
 elif k=='pathlib_filesystem_operations':
  # Paths are extracted directly from the registered scaffold.
  src=re.search(r'source = Path\("(.*?)"\)',A['ws.'+k]['files'][0]['content']).group(1)
  directory=re.search(r'directory = Path\("(.*?)"\)',A['ws.'+k]['files'][0]['content']).group(1)
  fn=re.search(r'filename = "(.*?)"',A['ws.'+k]['files'][0]['content']).group(1)
  target=str(Path(directory)/fn)
  v={'type':'before_after','before':diagram([('source',src),('directory',directory),('target',target+' (absent)')],[('directory','target','target = directory / filename')],'Before: destination absent'),'after':diagram([('source',src+' (absent)'),('directory',directory),('target',target)],[('directory','target','contains')],'After successful move'),'change_summary':'target = directory / filename; source.rename(target). Inspect the target before moving.'}
 else:v=cw(c)
 v['lineage']={'concept_ids':[c],'teaching_block_ids':s['teaching_block_ids'],'fact_ids':s['fact_ids'],'anchors':[c+'#visual']}
 for key in ['left','right','before','after']:
  if key in v:v[key]['lineage']=copy.deepcopy(v['lineage'])
 return v

out={'schema_version':plan['schema_version'],'kind':'screens_part','path_id':plan['path_id'],'batch_id':plan['batch_id'],'tiles':[]}
for tile in plan['tiles']:
 cs=tile['concept_ids']
 title=' / '.join(name(c) for c in cs)
 ot={'tile_id':tile['tile_id'],'title':title,'steps':[],'remediation_steps':[]}
 for s in tile['steps']:
  c=s['concept_ids'][0];k=short(c)
  step={'step_id':s['step_id'],'type':s['type'],'concept_ids':s['concept_ids'],'title':name(c),'lineage':{x:copy.deepcopy(s[x]) for x in ['teaching_block_ids','fact_ids','segment_ids','anchors']}}
  if s['type']=='explainer':
   step['eyebrow']='Understand'
   step['blocks']=fact_blocks(c,s['fact_ids'],s['teaching_block_ids'])
   if s['planned_visual_block_type']:
    step['blocks'].append(visual(c,s))
    if k=='json_serialization':
     v=cw(c);v['lineage']=copy.deepcopy(step['blocks'][-1]['lineage']);step['blocks'].append(v)
    if k=='special_methods':
     # Derive the fallback example by removing __str__, never by typing its output.
     fallback=re.sub(r'    def __str__\(self\):\n        return .*?\n', '', codes[c])
     fallback += '\nprint(str(order))'
     v=cw(c,fallback,[('print(str(order))','With __str__ removed, the default uses __repr__.')])
     v['lineage']=lin(c,[c+'#f3'],s['teaching_block_ids'],True)
     step['blocks'].append(v)
   else:
    # The second screen ties the same facts to the local scenario with one contrast.
    if k=='pathlib_filesystem_operations':
     text='For incoming/report.txt, build target from output/reports and filename. Create missing parents while allowing an existing directory. Move with source.rename(target), then inspect immediate entries without assuming order. A bare relative target uses the working directory, not the source’s parent. Check for an existing target before moving: Unix can replace it when permitted; Windows raises FileExistsError. The mkdir options both default to False, so specify the intended behavior.'
    elif k=='file_and_format_errors':
     text='At the CSV import boundary, distinguish a missing source, a decoding failure and a parser-reported error with their specific handlers. With header label,quantity, a notebook-only row has a missing quantity filled by restval, default None. Excess fields go under restkey, also default None. These row lengths do not automatically raise csv.Error: validate required row fields as well as handling parser failures.'
    else:text=contrasts[k]
    step['blocks']=[prose(c,text,s['fact_ids'],s['teaching_block_ids'],'example')]
  elif s['type']=='video':
   step['eyebrow']='Observe';step['title']=B[c]['media']['group_title']
   step['blocks']=[{'type':'media_group','segment_ids':copy.deepcopy(s['segment_ids'])}]
  elif s['type']=='check':
   step['eyebrow']='Check your understanding';step['title']='Check: '+name(c)
   step['lede']='Read the supplied question and choose the answer that follows the rules you have learned.'
  elif s['type']=='hands_on':
   step['eyebrow']='Practice';step['title']=practice_titles[k]
   step['lede']=B[c]['practice_anchor']['objective']
   if s['planned_interaction_type'] in ['classify','choice']:
    step['title']='Review '+name(c);step['lede']='Read the supplied excerpts in this step and decide which are correct, defective or unsafe.'
  elif s['type']=='recap':
   step['eyebrow']='Takeaways';step['title']='Keep these distinctions'
   # One principal takeaway per concept; all already taught in the planned explainers.
   step['blocks']=[]
   for cc in cs:
    fids=[cc+'#'+f['id'] for f in B[cc]['coverage']['required_facts']]
    recap_facts={
     'classes_and_instances':[2,3],'file_modes':[2,4,5],'instance_initialization':[2,3],
     'instance_methods':[1,3],'class_and_static_methods':[2,3],'composition':[1,2],
     'encapsulation_conventions':[1,2,3,4],'inheritance_and_super':[2,3],'custom_exceptions':[1,2],
     'instance_vs_class_attributes':[2,3],'json_serialization':[3],'object_introspection':[3],
     'pathlib_filesystem_operations':[3,5],'special_methods':[1,2],'text_file_encodings':[2],
     'file_and_format_errors':[3,4],'with_resource_management':[2,3],'binary_files':[1,3]}
    fids=[cc+'#f'+str(i) for i in recap_facts[short(cc)]]
    step['blocks'].append(prose(cc,contrasts[short(cc)],fids,role='takeaway'))
   nxt=next((t for t in plan['tiles'] if t['tile_id']==tile['next_tile_id']),None)
   nextname=name(nxt['concept_ids'][0]) if nxt else g['names']['python.datetime_operations']
   step['blocks'].append({'type':'up_next','title':'Up next: '+nextname,'text':'Next, begin '+nextname.lower()+'.'})
  ot['steps'].append(step)
 # A deterministic conditional screen for every distinct fact set tested or practised.
 seen=set()
 for s in tile['steps']:
  if s['type'] not in ['check','hands_on']:continue
  for c in s['concept_ids']:
   fids=[f for f in s['fact_ids'] if f.startswith(c+'#')]
   if not fids:fids=[c+'#'+f['id'] for f in B[c]['coverage']['required_facts']]
   key=(c,tuple(fids))
   if key in seen:continue
   seen.add(key)
   rid=tile['tile_id']+'.r'+str(len(ot['remediation_steps'])+1).zfill(2)
   blocks=fact_blocks(c,fids)
   blocks.append(prose(c,contrasts[short(c)],fids,role='misconception'))
   ot['remediation_steps'].append({'step_id':rid,'type':'remediation','concept_ids':[c],'eyebrow':'Try a clearer contrast','title':'Revisit: '+name(c),'blocks':blocks,'lineage':lin(c,fids)})
 out['tiles'].append(ot)
(P/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Wrote',len(out['tiles']),'tiles;',sum(len(t['steps']) for t in out['tiles']),'planned steps;',sum(len(t['remediation_steps']) for t in out['tiles']),'remediation steps')
