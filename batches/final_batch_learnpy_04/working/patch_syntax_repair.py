import json,re,ast,sys
from pathlib import Path
sys.path.insert(0,'00_FINAL_PIPELINE_CORE/scripts')
from checkers import pysyntax
B=Path('batches/final_batch_learn_python.region.04')
p=B/'interactions.json'
d=json.loads(p.read_text())
errors=set(re.findall(r'E ([^/]+)/', (B/'working/repair_gate_before.txt').read_text()))
# Preserve all answer predicates, constraints, tests, feedback, and other interactions.
original=json.loads(p.read_text())
(B/'working/interactions_before_syntax_repair.json').write_text(p.read_text())
def supplied(code):
    # Definitions are visible, immutable scaffolding. exec is already used by the
    # host fixtures; a literal program keeps the supplied definitions separate
    # from the learner's single assignment/call. The learner never edits exec.
    return '# Supplied implementation: leave unchanged.\nexec('+repr(code.rstrip()+'\n')+')\n'
for t in d['tiles']:
 for s in t['interactions']:
  if s['step_id'] not in errors: continue
  i=s['interaction'];solfile=i['grading']['solution_files'][0];starterfile=i['public']['workspace']['files'][0]
  prefix,body=solfile['content'].split('# BEGIN LEARNER\n',1)
  code,suffix=body.split('# END LEARNER',1)
  key=s['step_id'].removeprefix('learn_python.tile.')
  prompt='';sol='';start=''
  if key=='066_066.s04':
   cls,rest=code.split('first =',1)
   base=supplied(cls)
   tail='# Supplied identity observation: leave unchanged.\nprint(first is second)\n'
   sol=base+'first = Order()\nsecond = Order()\n'+tail
   start=base+'first = None\nsecond = None\n'+tail
   prompt='The supplied empty Order class has an indented pass body; leave it unchanged. Replace the two placeholder assignments with separate Order() calls, assigning the instances to first and second. Leave the supplied identity comparison unchanged and observe its result.'
  elif key=='067_067.s05':
   base='# Supplied creation, writing, closure, and conflict handler: leave unchanged.\n'+code.replace('open(path, "x")','open(path, creation_mode)')
   sol='creation_mode = "x"\n'+base
   start='creation_mode = "w"\n'+base
   prompt='Edit only creation_mode to select exclusive creation. The supplied try/except opens path using that mode, writes report_text, closes a successfully opened file, and prints "Destination exists" for FileExistsError. An absent report must receive report_text; an existing report must remain unchanged. Do not change the supplied handler or add a fallback writing mode.'
  elif key in {'068_070.s04','068_070.s08','068_070.s12','071_073.s03','071_073.s06','071_073.s10','075_075.s04','079_079.s04'}:
   tree=ast.parse(code);last_class=max(n.end_lineno for n in tree.body if isinstance(n,ast.ClassDef))
   lines=code.splitlines(True);base=supplied(''.join(lines[:last_class]));tail=''.join(lines[last_class:]).lstrip('\n')
   if key=='068_070.s04':
    sol=base+tail;start=base+tail.replace('order = Order(label, quantity)','order = None')
    prompt='Leave the supplied Order initializer unchanged. Replace order = None with a call to Order using the supplied label and quantity, in that order. The supplied display must print order.label and order.quantity, preserving both inputs.'
   elif key in {'068_070.s08','071_073.s06'}:
    creation,tail=tail.split('\n',1)
    tail=tail.replace('order.add(amount)','order.add(increment)')
    sol=base+creation+'\nincrement = amount\n'+tail
    start=base+creation+'\nincrement = 0\n'+tail
    prompt=('Leave the supplied Order class, construction, method call, and display unchanged. Set increment to the supplied amount so the call to add updates this instance by that amount. '+('The displayed quantity must be the original quantity plus amount.' if key=='068_070.s08' else 'The method must update _quantity and return that updated value as result; the display prints result, without creating a separate quantity attribute.'))
   elif key=='068_070.s12':
    tail=tail.replace('Order.from_text(text)','Order.from_text(input_text)')
    sol=base+'input_text = text\n'+tail;start=base+'input_text = "0"\n'+tail
    prompt='Leave the supplied Order class and class-method call unchanged. Set input_text to the supplied text so Order.from_text receives that input. It must construct an Order with quantity converted to int; the supplied display prints order.quantity.'
   elif key=='071_073.s03':
    sol=base+tail;start=base+tail.replace('report_formatter = formatter','report_formatter = None')
    prompt='The supplied Report delegates to its stored Formatter object; leave both classes and the calls unchanged. Set report_formatter to the supplied formatter instance so Report stores that same object. The supplied total call assigns result and prints the formatted total for quantity.'
   elif key=='071_073.s10':
    sol=base+tail;start=base+tail.replace('order = FeeOrder(quantity, fee)','order = None')
    prompt='Read the supplied Order and FeeOrder implementations, including their super calls; leave them unchanged. Replace order = None with a FeeOrder construction using the supplied quantity and fee, in that order. The supplied display must show the inherited quantity formatting followed by the fee.'
   elif key=='075_075.s04':
    tail=tail.replace('first.labels.append(label)','selected.labels.append(label)')
    a,b=tail.split('selected.labels.append',1)
    sol=base+a+'selected = first\nselected.labels.append'+b
    start=base+a+'selected = second\nselected.labels.append'+b
    prompt='The supplied initializer creates a fresh labels list for every Order instance; leave it and both constructions unchanged. Set selected to first so the supplied append adds label only to first.labels. Leave the displays unchanged: second.labels must remain empty, with no class-level labels list.'
   else:
    sol=base+tail;start=base+tail.replace('order = Order(quantity)','order = None')
    prompt='Read the supplied __repr__ and __str__ methods, which use self.quantity; leave the class unchanged. Replace order = None with an Order construction using the supplied quantity. Leave the displays and fallback observation unchanged: repr(order) must be Order(quantity=...), print(order) must show Quantity: ..., and removing __str__ must reveal the inspection-form fallback.'
  elif key=='074_074.s03':
   definitions,tail=code.split('try:\n',1)
   tail='try:\n'+tail.replace('except InvalidRecordError:','except error_type:')
   base=supplied(definitions)
   sol=base+'error_type = InvalidRecordError\n'+tail
   start=base+'error_type = ValueError\n'+tail
   prompt='The supplied validator raises InvalidRecordError("negative quantity") for a negative quantity and returns other quantities unchanged. Leave that validator and the supplied try block unchanged. Set error_type to the custom InvalidRecordError class so the handler catches that specific failure and prints "Order rejected"; valid quantities must still be printed normally.'
  elif key=='078_078.s04':
   sol=code;start=code.replace('target = Path(directory, filename)','target = None')
   prompt='Leave the supplied import, mkdir(parents=True, exist_ok=True), rename, and immediate-entry inspection unchanged. Replace target = None with a Path construction combining the supplied directory and filename. The supplied operations must create missing parents and move source to target without changing its content; do not assume entry order.'
  elif key=='080_083.s07':
   # Keep the independently validated importer and cause-specific handlers as
   # supplied code; the learner selects the required-field names it validates.
   code=code.replace('"label" not in row','label_key not in row').replace('"quantity" not in row','quantity_key not in row').replace('row["label"]','row[label_key]').replace('row["quantity"]','row[quantity_key]')
   base=supplied(code)
   sol='label_key = "label"\nquantity_key = "quantity"\n'+base
   start='label_key = "unused_label"\nquantity_key = "unused_quantity"\n'+base
   prompt='Read the supplied import_rows implementation and leave it unchanged. Set label_key and quantity_key to the required CSV field names label and quantity. The supplied independent validation must reject missing, None, or empty required values and excess fields under the None key, returning invalid_row_message. Valid rows must be returned. The supplied separate FileNotFoundError, UnicodeDecodeError, and csv.Error handlers and finally-based cleanup must remain intact.'
  elif key=='080_083.s12':
   base='# Supplied managed reads, deliberate exception, handler, and closed-state displays: leave unchanged.\n'+code.replace('open("label.txt",','open(source_path,')
   sol='source_path = "label.txt"\n'+base;start='source_path = "missing.txt"\n'+base
   prompt='Set source_path to label.txt, the supplied UTF-8 text file. Leave the two managed reads and observations unchanged. Both read into text; the second deliberately raises ValueError("Processing failed") with its handler outside the with block. Observe the supplied closed-state displays: the source must close after both normal completion and the exception, without an explicit close call.'
  elif key=='080_083.s16':
   base='# Supplied nested binary copy: leave unchanged.\n'+code.replace('open("source.bin",','open(source_path,').replace('open("copy.bin",','open(destination_path,')
   sol='source_path = "source.bin"\ndestination_path = "copy.bin"\n'+base
   start='source_path = "missing.bin"\ndestination_path = "copy.bin"\n'+base
   prompt='Set source_path to source.bin and destination_path to copy.bin. Leave the supplied nested managed binary openings and direct payload read/write unchanged: read source in rb mode into payload and write those bytes to the destination in wb mode, without decoding. copy.bin must match source.bin byte-for-byte, source.bin must remain unchanged, and both streams must close.'
  else: raise ValueError(key)
  solfile['content']=prefix+'# BEGIN LEARNER\n'+sol+'# END LEARNER'+suffix
  starterfile['content']=prefix+'# BEGIN LEARNER\n'+start+'# END LEARNER'+suffix
  i['public']['prompt']=prompt
  violations,_,_=pysyntax.judge(solfile['content'],i['public']['constraints']['allowed_syntax'],i['public']['constraints']['blocked_syntax'],starterfile['content'])
  if violations: raise ValueError((key,violations))
# Check patch scope explicitly.
for ot,nt in zip(original['tiles'],d['tiles']):
 for os,ns in zip(ot['interactions'],nt['interactions']):
  if os['step_id'] not in errors: assert os==ns
  else:
   assert os['interaction']['grading']['tests']==ns['interaction']['grading']['tests']
   assert os['interaction']['public']['constraints']==ns['interaction']['public']['constraints']
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Patched',len(errors),'interactions; counts',sum(len(t['interactions']) for t in d['tiles']))
