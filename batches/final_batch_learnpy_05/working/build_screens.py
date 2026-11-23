import json,re
from pathlib import Path
P=Path('batches/final_batch_learn_python.region.05')
plan=json.loads((P/'tile_plans.json').read_text()); glossary=json.loads((P/'inputs/path_glossary_bundle.json').read_text()); registry=json.loads((P/'scenario_asset_registry.json').read_text())
B={b['context']['concept_id']:b for b in glossary['bundles']}; A={a['asset_id']:a for a in registry['assets']}
# One self-contained idea per paragraph, ordered to match the glossary facts.
texts={
'datetime_operations':[
'Parse date text with datetime.strptime(text, format); .date() then obtains the calendar date.',
'For numeric year-month-day text, the explicit parsing format is %Y-%m-%d.',
'Subtracting one date from another produces a timedelta that represents the difference.',
'For calendar dates, (later_date - earlier_date).days gives a signed day difference. Reversing the subtraction reverses the sign in this example, rather than preserving an absolute distance.'],
'local_modules':[
'A module is a .py file containing Python definitions and statements. Its filename without .py is the module name: helpers.py is imported as helpers, not as a dotted filename.',
'Move the shared cost helper into sibling helpers.py. Use import helpers with helpers.cost(quantity, price), or from helpers import cost with cost(quantity, price). Follow the import binding when choosing the call.',
'In ordinary script invocation, the script directory is included in the module search path, allowing this sibling-module import.'],
'importable_packages':[
'A regular package groups modules in a directory with __init__.py, which may be empty. In the orders layout, costs.py and __init__.py belong inside the orders directory.',
'Where orders is importable, use import orders.costs and orders.costs.cost(quantity, price). Alternatively, from orders.costs import cost gives the direct call cost(quantity, price). Keep package, module and helper distinct.'],
'logging':[
'After import logging, logger = logging.getLogger(__name__) obtains a logger named for the module.',
'Choose the event level by meaning: DEBUG for detailed diagnostics; INFO for expected progress; WARNING for an unexpected condition while continuing; ERROR for inability to perform a function; CRITICAL for a serious failure.',
'Emit events with the corresponding method, such as logger.debug(message) or logger.info(message).',
'logging.basicConfig(level=logging.INFO) includes INFO and higher events. The default root threshold is WARNING. A missing DEBUG message need not mean that its line was never reached.',
'Propagation normally sends events to ancestor handlers. Handlers on both a logger and its ancestors can duplicate output; ordinarily configure a handler at one suitable ancestor.'],
'main_entry_point':[
'When a module runs as the main script, __name__ is "__main__". When imported, __name__ is its module name instead.',
'Place command-interface actions inside if __name__ == "__main__":. Importing the module then does not execute those guarded actions; the guard applies only to its body.',
'Keep reusable helper definitions outside the guarded body so importers can use them. Guard the command actions, not the shared cost definition.'],
'argparse_command_line':[
'After import argparse, create parser = argparse.ArgumentParser() to define the command interface.',
'parser.add_argument("input_path") defines a required positional value. An argument name beginning with -- defines an option.',
'parser.add_argument("--verbose", action="store_true") defines a boolean flag: absent means False; present means True. Its presence selects it, rather than a following text value.',
'args = parser.parse_args() parses command-line arguments into attributes such as args.input_path and args.verbose.',
'Invalid arguments, including missing required arguments, produce an error message and exit status 2 by default.'],
'module_search_paths':[
'An ordinary import checks built-in modules, then searches sys.path. The script directory normally precedes standard-library directories.',
'A same-named local file can shadow a standard-library module. Rename the conflicting local file to remove the ambiguity; a familiar import name alone does not prove its source.',
'Inspect sys.path for the search locations used by the executing interpreter. Exact paths depend on the environment.',
'For a file-backed imported module, inspect module.__file__ to locate its file. In the diagnostic example, inspect json.__file__ rather than guessing from the name json.'],
'os_environment':[
'os.environ maps process environment names to string values. Configuration arrives as text.',
'os.environ.get("SETTING", fallback) returns the configured string or, if absent, the fallback. Without a fallback, absence returns None. An absent name is not the same as a configured empty string.',
'For required configuration, check absence explicitly or use bracket lookup, which raises KeyError for a missing key. Report missing configuration instead of proceeding with an unintended value.'],
'random_vs_secrets':[
'Use random for modelling and simulation. Use secrets for cryptographically strong randomness in security-sensitive values; seeded simulation output is not a substitute.',
'random.seed(seed) initializes the pseudo-random generator. Reusing a seed reproduces a sequence under the documented reproducibility conditions, not a guarantee across every environment.',
'random.random() returns a floating-point value from 0.0 inclusive to 1.0 exclusive.',
'secrets.token_hex(nbytes) generates a random hexadecimal token for security-sensitive use. Choose the module from the requirement, not convenience.'],
'regular_expressions':[
'A regular expression describes a text pattern. [...] selects one character from a set; A-Z is a range; * permits zero or more repetitions.',
'Concatenated elements match in sequence. A raw literal such as r"..." avoids Python string-escape processing of pattern backslashes.',
're.fullmatch(pattern, text) returns a Match for a whole-text match and None otherwise. Test is not None for success.',
're.match checks the beginning; re.search looks anywhere. Neither requires the entire text to match, so a matching prefix or substring does not establish whole-label validity.'],
'sys_runtime_interface':[
'sys.executable identifies the running interpreter’s executable path when available. It may be an empty string or None if Python cannot retrieve it; do not invent a path.',
'sys.version includes the interpreter version plus build and compiler information.',
'After import sys, print(sys.executable) and print(sys.version) display the actual executing runtime. Compare these observations with the interpreter you intended, rather than relying only on a tool label.'],
'virtual_environments':[
'Use the selected Python executable with -m venv .venv to create a project environment. Its interpreter is bin/python on POSIX or Scripts/python.exe on Windows.',
'Activation changes command lookup to the environment executable. It is not required when invoking that executable by its full path.',
'sys.prefix != sys.base_prefix identifies an interpreter running in a virtual environment.',
'Inspect installed packages using the environment’s Python with -m pip list.',
'Virtual environments are isolated from base-environment packages by default; do not assume the base package list applies.'],
'environment_interpreter_selection':[
'Inspect sys.executable in the executed program to identify its actual interpreter. An environment label is not the evidence for this check.',
'A venv interpreter is at bin/python on POSIX or Scripts/python.exe on Windows.',
'If command lookup selects the wrong Python, configure the tool to invoke the intended venv executable explicitly. Explicit invocation does not require activation.',
'After changing the runtime, check the executable path and sys.prefix != sys.base_prefix again in the program that runs. Changing the displayed label is not the final check.'],
'pip_installation':[
'Install a verified distribution using the intended environment interpreter with -m pip install package_name.',
'Through that same interpreter, inspect installation with -m pip show package_name or -m pip list.',
'Check usability by importing the documented import name under the same interpreter that will run the project. Installation with one interpreter does not verify usability in another.',
'A pip distribution name need not equal its Python import-package name. Use documented names rather than guessing the import spelling from the installation name.'],
'requirements_files':[
'A requirements file lists dependencies. package_name==version pins a specific version; replace placeholders only with verified project information.',
'Install the listed requirements using the fresh environment’s Python with -m pip install -r requirements.txt.',
'Inspect installed versions with that same interpreter’s -m pip list.',
'Check required documented imports in the recreated interpreter. An installation report alone does not prove that every required module is importable.']}
contrasts={
'datetime_operations':'Contrast subtraction order: second - first and first - second describe opposite signed differences for these calendar dates.',
'local_modules':'Contrast helpers.py, the file, with helpers, the import name. Match the call to the import binding.',
'importable_packages':'Contrast the orders package directory with its costs module. A regular package includes __init__.py even when that file is empty.',
'logging':'Contrast expected progress with detailed diagnostics: choose the event method, then consider the configured threshold and handler placement.',
'main_entry_point':'Contrast running report.py as the main script with importing report. The guarded actions and the unguarded helper have different roles.',
'argparse_command_line':'Contrast the required input_path value with the presence-only --verbose flag. Missing a required value is invalid.',
'module_search_paths':'Contrast the name json with the file actually imported. A local json.py can conflict with the standard-library module.',
'os_environment':'Contrast an absent ORDER_SOURCE with a configured empty string. Test absence explicitly for a required setting.',
'random_vs_secrets':'Contrast reproducible simulation with a security-sensitive token. A seeded simulation is not a security recipe.',
'regular_expressions':'Contrast a whole-label check with a prefix check. Use the registered labels with fullmatch, not just match.',
'sys_runtime_interface':'Contrast the selected tool label with observations from the running process. Preserve unavailable executable-path values.',
'virtual_environments':'Contrast activation with explicit invocation of the environment executable. Explicit invocation does not depend on activation.',
'environment_interpreter_selection':'Contrast a changed environment label with a rechecked running process. Verify the actual executable and prefixes.',
'pip_installation':'Contrast installation evidence with import evidence. Both checks must use the intended interpreter and documented names.',
'requirements_files':'Contrast a successful installation report with checking required imports in the recreated interpreter.'}
takeaways={
'datetime_operations':'Parse calendar dates with an explicit format; use subtraction and .days for a signed difference.',
'local_modules':'Share helpers through sibling modules and match calls to import bindings.',
'importable_packages':'A regular package contains __init__.py; dotted access separates package, module and helper.',
'logging':'Choose meaningful levels, configure thresholds, and avoid duplicate handlers along propagation.',
'main_entry_point':'Guard command actions while keeping reusable helpers available to importers.',
'argparse_command_line':'Declare required values and presence-only flags; parse attributes and recognise invalid arguments.',
'module_search_paths':'Inspect search locations and imported files; resolve conflicting local filenames.',
'os_environment':'Environment values are strings. Distinguish absence, optional fallbacks and required configuration.',
'random_vs_secrets':'Separate simulation randomness from security-sensitive randomness; preserve reproducibility limits and value bounds.',
'regular_expressions':'Validate complete labels with fullmatch and an explicit success test, not just a prefix or substring.',
'sys_runtime_interface':'Inspect the actual executable and version, preserving the executable-path availability limit.',
'virtual_environments':'Use the environment executable, check prefixes and inspect its packages; activation is not required for explicit invocation.',
'environment_interpreter_selection':'Configure the intended executable and verify the executed process again.',
'pip_installation':'Use one interpreter for installation, inspection and documented imports; distribution and import names may differ.',
'requirements_files':'Record verified version pins, install into a fresh environment, inspect versions and check required imports.'}
def key(c):return c.split('.')[-1]
def lineage(c,fs,tbs=None,anchors=None):
 return dict(concept_ids=[c],fact_ids=[c+'#'+f for f in fs],teaching_block_ids=tbs or [],anchors=anchors or [])
def factblocks(c,fs,tbs):
 out=[]
 for f in fs:
  related=[x for x in tbs if f in next(t for t in B[c]['teaching_blocks'] if c+'#'+t['id']==x)['fact_ids']]
  out.append(dict(type='prose',text=texts[key(c)][int(f[1:])-1],role='mechanism',lineage=lineage(c,[f],related)))
 # Intro and misconception blocks contribute context to the relevant factual teaching.
 missing=[x for x in tbs if not any(x in b['lineage']['teaching_block_ids'] for b in out)]
 if out:out[0]['lineage']['teaching_block_ids']+=missing
 return out

def codeblock(c,code,annotations=None):
 return dict(type='code_walkthrough',language='python',code=code,annotations=annotations or [],reveal='line_by_line',lineage=lineage(c,[f['id'] for f in B[c]['coverage']['required_facts']],[c+'#tb4'],[c+'#visual']))
def fenced(c):
 for t in B[c]['teaching_blocks']:
  m=re.search(r'```python\n(.*?)```',t['content'],re.S)
  if m:return m.group(1).rstrip()+'\n'
def diagram(c,title,labels,edges=None):
 ns=[dict(id='n'+str(i+1),label=x) for i,x in enumerate(labels)]
 return dict(type='diagram',diagram_kind='mapping',title=title,nodes=ns,edges=[dict(**{'from':ns[a]['id'],'to':ns[b]['id']},label=l,directed=True) for a,b,l in (edges or [])],alt_text=title+': '+'; '.join(labels),lineage=lineage(c,[f['id'] for f in B[c]['coverage']['required_facts']],[c+'#tb4'],[c+'#visual']))
def visual(c,v):
 k=key(c)
 if v=='code_walkthrough':
  code=fenced(c)
  if not code and k=='random_vs_secrets':
   starter=A['ws.'+k]['files'][0]['content']; seedline=next(l for l in starter.splitlines() if l.startswith('random.seed'))
   example=next(t['content'] for t in B[c]['teaching_blocks'] if t['id']=='tb4'); token=re.search(r'secrets.token_hex\(\d+\)',example).group()
   code='import random\n'+seedline+'\nfirst = [random.random(), random.random()]\n'+seedline+'\nsecond = [random.random(), random.random()]\nprint(first == second)\nimport secrets\nprint('+token+')\n'
  annotations={
   'datetime_operations':[(2,3,'Parse with an explicit format and obtain calendar dates.'),(4,5,'Display both subtraction orders; .days keeps the sign.')],
   'logging':[(2,2,'Set the application threshold.'),(3,3,'Name the logger for the module.'),(4,5,'Choose diagnostic and progress event methods.')],
   'main_entry_point':[(1,2,'Reusable helper remains outside the guard.'),(4,5,'Only the guarded command action depends on main-script execution.')],
   'os_environment':[(2,3,'Optional fallback versus required configuration.'),(5,6,'Check None explicitly for absence.')],
   'random_vs_secrets':[(2,6,'Reset the seed and compare repeated simulation calls.'),(7,8,'Use secrets for a security-sensitive token.')],
   'regular_expressions':[(2,2,'First character required; later characters may repeat.'),(4,4,'Whole-text match with an explicit success test.')],
   'sys_runtime_interface':[(2,3,'Observe the actual process, not a tool label.')]}
  return codeblock(c,code,[dict(start_line=a,end_line=b,text=t) for a,b,t in annotations[k]])
 if k=='local_modules':
  starter=A['ws.local_modules']['files'][0]['content']; before=starter.split('#')[0]; definition=before[:before.index('\ncost(')].rstrip();call=re.search(r'cost\([^\n]+\)',before[before.index('\ncost('):]).group()
  after='# helpers.py\n'+definition+'\n\n# sibling report.py\nimport helpers\nhelpers.'+call+'\n'
  before_diagram=diagram(c,'Before: definition and call in report.py',['report.py: '+definition,'report.py: '+call],[(0,1,'local call')])
  after_diagram=diagram(c,'After: shared sibling module',['helpers.py: '+definition,'report.py: import helpers','report.py: helpers.'+call,'helpers.py filename → helpers module name'],[(1,0,'imports sibling'),(1,2,'qualified call binding'),(3,1,'import name')])
  return dict(type='before_after',before=before_diagram,after=after_diagram,change_summary='Move the shared definition into helpers.py; import helpers from sibling report.py.',lineage=lineage(c,['f1','f2','f3'],[c+'#tb4'],[c+'#visual']))
 if k=='importable_packages':
  return diagram(c,'Regular package layout',['orders/','orders/__init__.py (may be empty)','orders/costs.py: cost helper','import orders.costs','orders.costs.cost(quantity, price)','from orders.costs import cost','cost(quantity, price)'],[(0,1,'contains'),(0,2,'contains'),(3,4,'qualified call'),(5,6,'direct call')])
 if k=='argparse_command_line':
  return diagram(c,'Command interface and parsed attributes',['Argument declarations: required input_path; --verbose with store_true','Supplied words: orders.csv --verbose','parse_args(): args.input_path; args.verbose','Absent --verbose: default False','Invalid or missing required arguments: error; default exit status 2'],[(0,2,'defines'),(1,2,'parse'),(0,3,'flag absent'),(0,4,'invalid input')])
 if k=='module_search_paths':
  before=diagram(c,'Before: possible local shadowing',['Built-in module check','sys.path: script directory normally before standard library','Local json.py: conflicts with json','Inspect sys.path and json.__file__'],[(0,1,'then search'),(1,2,'can shadow'),(2,3,'inspect actual source')])
  after=diagram(c,'After: conflict removed',['Rename conflicting local json.py','Inspect sys.path and json.__file__','Locate the file-backed imported module'],[(0,1,'remove ambiguity'),(1,2,'verify location')])
  return dict(type='before_after',before=before,after=after,change_summary='Rename the conflicting local file; inspect the actual imported location instead of assuming paths.',lineage=lineage(c,['f1','f2','f3','f4'],[c+'#tb4'],[c+'#visual']))
 if k=='virtual_environments':
  return diagram(c,'Environment executable and inspection',['Selected Python: -m venv .venv','.venv/bin/python (POSIX)','.venv/Scripts/python.exe (Windows)','Explicit full-path invocation: activation not required','Inspect sys.prefix != sys.base_prefix','Environment Python: -m pip list'],[(0,1,'POSIX'),(0,2,'Windows'),(1,3,'explicit invocation'),(2,3,'explicit invocation'),(3,4,'identify environment'),(3,5,'inspect packages')])
 if k=='environment_interpreter_selection':
  before=diagram(c,'Before: label alone is insufficient',['Tool displays project environment label','Inspect sys.executable in the executed program','Compare actual path with intended venv executable'],[(0,1,'verify process'),(1,2,'compare')])
  after=diagram(c,'After: explicit selection and recheck',['Select intended bin/python or Scripts/python.exe explicitly','Activation not required','Recheck sys.executable and sys.prefix != sys.base_prefix in the executed program'],[(0,1,'explicit invocation'),(0,2,'run again and inspect')])
  return dict(type='before_after',before=before,after=after,change_summary='Replace reliance on a displayed label with explicit executable selection and process rechecking.',lineage=lineage(c,['f1','f2','f3','f4'],[c+'#tb4'],[c+'#visual']))
 if k=='pip_installation':
  return diagram(c,'Same interpreter across three checks',['Intended environment executable','-m pip install package_name: verified distribution name','-m pip show package_name or -m pip list','Import documented import name: may differ from distribution name'],[(0,1,'install through'),(0,2,'inspect through'),(0,3,'verify through')])
 if k=='requirements_files':
  labels=['Verified dependency pins: package_name==version','Fresh environment Python: -m pip install -r requirements.txt','Same interpreter: -m pip list','Same interpreter: check required documented imports']
  ns=[dict(id='n'+str(i+1),label=l,kind='step') for i,l in enumerate(labels)]
  return dict(type='process_flow',nodes=ns,edges=[{'from':ns[i]['id'],'to':ns[i+1]['id'],'kind':'next'} for i in range(len(ns)-1)],direction='LR',reveal='stepwise',alt_text='Recreate from verified pins, then inspect installed versions and check imports through the fresh environment interpreter.',lineage=lineage(c,['f1','f2','f3','f4'],[c+'#tb4'],[c+'#visual']))
 raise ValueError((c,v))

out={k:plan[k] for k in ['schema_version','path_id','batch_id']};out.update(kind='screens_part',tiles=[])
for t in plan['tiles']:
 tile=dict(tile_id=t['tile_id'],title=' · '.join(B[c]['context']['concept_name'] for c in t['concept_ids']),steps=[],remediation_steps=[])
 for ps in t['steps']:
  c=ps['concept_ids'][0];k=key(c)
  s=dict(step_id=ps['step_id'],type=ps['type'],concept_ids=ps['concept_ids'],title=B[c]['context']['concept_name'],lineage={x:ps[x] for x in ['concept_ids','teaching_block_ids','fact_ids','segment_ids','anchors']})
  if ps['type']=='explainer':
   s['eyebrow']='Explore';s['blocks']=factblocks(c,[f.split('#')[1] for f in ps['fact_ids']],ps['teaching_block_ids'])
   if ps['planned_visual_block_type']:s['blocks'].append(visual(c,ps['planned_visual_block_type']))
  elif ps['type']=='video':
   s['eyebrow']='Demonstration';s['blocks']=[dict(type='media_group',segment_ids=ps['segment_ids'])]
  elif ps['type']=='check':
   caps=[a.split('#assessment:')[1].replace('_',' ') for a in ps['anchors'] if '#assessment:' in a]
   s['title']='Check: '+(' / '.join(caps) or B[c]['context']['concept_name']);s['eyebrow']='Quick check';s['lede']='Read the supplied question and choose the answer that fits the requirement.'
  elif ps['type']=='hands_on':
   s['eyebrow']='Practice'
   if ps['planned_interaction_type'] in ['classify','choice']:
    s['title']='Review '+B[c]['context']['concept_name'].lower();s['lede']='Read the supplied excerpts in this step and judge which meet the requirement and which are defective.'
   else:
    s['title']='Practise '+B[c]['context']['concept_name'].lower();s['lede']=B[c]['practice_anchor']['objective']
  elif ps['type']=='recap':
   s['title']='Keep these ideas';s['eyebrow']='Recap';s['blocks']=[]
   for cid in ps['concept_ids']:
    s['blocks'].append(dict(type='prose',role='takeaway',text=takeaways[key(cid)],lineage=lineage(cid,[f['id'] for f in B[cid]['coverage']['required_facts']],[cid+'#'+b['id'] for b in B[cid]['teaching_blocks']])))
   nxt=next((nt for nt in plan['tiles'] if nt['tile_id']==t['next_tile_id']),None)
   nc=nxt['concept_ids'][0] if nxt else list(glossary['names'])[list(glossary['names']).index(t['concept_ids'][-1])+1]
   s['blocks'].append(dict(type='up_next',title='Next: '+glossary['names'][nc]))
  tile['steps'].append(s)
 # Every distinct measured fact set has a suitable short retry screen.
 seen=set()
 for ps in t['steps']:
  if ps['type'] not in ['check','hands_on']:continue
  c=ps['concept_ids'][0];fs=[f.split('#')[1] for f in ps['fact_ids']]
  if not fs:
   fs=list(dict.fromkeys(f for a in B[c]['assessment_anchors'] for f in a['fact_ids']))
   # Practice-only facts are also available on retry.
   fs=list(dict.fromkeys(fs+[f['id'] for f in B[c]['coverage']['required_facts']]))
  sig=(c,tuple(fs))
  if sig in seen:continue
  seen.add(sig);tbs=[c+'#'+b['id'] for b in B[c]['teaching_blocks'] if set(b['fact_ids'])&set(fs)]
  blocks=factblocks(c,fs,tbs)
  blocks.append(dict(type='prose',text=contrasts[key(c)],role='misconception',lineage=lineage(c,fs,tbs)))
  tile['remediation_steps'].append(dict(step_id=t['tile_id']+'.r'+str(len(tile['remediation_steps'])+1).zfill(2),type='remediation',concept_ids=[c],title='Try the contrast: '+B[c]['context']['concept_name'],eyebrow='Review',blocks=blocks,lineage=lineage(c,fs,tbs)))
 out['tiles'].append(tile)
(P/'screens.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
# Mistakes-to-avoid self-check: plan order/lineage, budgets, text grounding tags, no authored outputs, and assets.
for t,ot in zip(plan['tiles'],out['tiles']):
 assert [x['step_id'] for x in t['steps']]==[x['step_id'] for x in ot['steps']]
 for ps,s in zip(t['steps'],ot['steps']):
  assert s['type']==ps['type'] and s['concept_ids']==ps['concept_ids']
  assert s['lineage']['fact_ids']==ps['fact_ids'] and s['lineage']['teaching_block_ids']==ps['teaching_block_ids']
  if ps['type'] in ['check','hands_on']:assert 'blocks' not in s
  if ps['word_budget']:
   n=sum(len(re.findall(r'\S+',b.get('text',''))) for b in s.get('blocks',[]))
   assert n<=ps['word_budget'],(s['step_id'],n,ps['word_budget'])
 def inspect(b):
  assert not any(x in b for x in ['output','result','computed_values','execution_provenance'])
  if b['type']=='prose':
   assert len(b['text'].split())<=90 and 'video' not in b['text'].lower()
   assert b['lineage']['concept_ids'] and b['lineage']['teaching_block_ids'] and b['lineage']['fact_ids']
  for f in b.get('lineage',{}).get('fact_ids',[]):assert '#f' in f
  if b['type'] in ['code_walkthrough','diagram','process_flow','before_after']:assert any(a.endswith('#visual') for a in b['lineage']['anchors'])
  for part in ['before','after']:
   if part in b:inspect(b[part])
 for s in ot['steps']+ot['remediation_steps']:
  for b in s.get('blocks',[]):inspect(b)
print('tiles',len(out['tiles']),'steps',sum(len(t['steps']) for t in out['tiles']),'remediation',sum(len(t['remediation_steps']) for t in out['tiles']))
