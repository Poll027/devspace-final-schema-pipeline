import json, sys, copy
from pathlib import Path
B=Path('batches/final_batch_learn_python.region.05')
sys.path.insert(0,str(Path('00_FINAL_PIPELINE_CORE/scripts').resolve()))
from checkers import sandbox
P=json.load(open(B/'tile_plans.json')); S=json.load(open(B/'screens.json')); G={x['context']['concept_id']:x for x in json.load(open(B/'inputs/path_glossary_bundle.json'))['bundles']}; A=json.load(open(B/'scenario_asset_registry.json'))
R=json.load(open('00_FINAL_PIPELINE_CORE/registry/runtimes.json'))['runtimes']['python']
# Each wrong option has its own fact-grounded explanation.
Q={}
def q(c,n,p,right,wrong1,why1,wrong2,why2,hint): Q[(c,n)]=(p,right,wrong1,why1,wrong2,why2,hint)
q('datetime_operations',0,'Two calendar dates have already been parsed. Which statement correctly interprets (second - first).days and the reversed subtraction?','The result is signed; reversing the subtraction reverses its sign.','Both expressions must give the same positive distance.','Calendar-date subtraction gives a signed difference, not an absolute distance.','Subtraction returns a date, so .days reads its day of month.','Subtraction returns a timedelta, not a calendar date.','Consider what the subtraction order expresses.')
q('local_modules',0,'The shared helper is in helpers.py. What module name belongs in its import?','helpers','helpers.py','The .py suffix is removed to obtain the module name.','cost','cost is the helper name, not the filename-derived module name.','Separate the file name from a definition inside the file.')
q('local_modules',1,'report.py and helpers.py are siblings. In ordinary script invocation, why can report.py import helpers?','The script directory is included in the module search path.','Every directory on the computer is automatically searched.','The fact describes inclusion of the script directory, not every directory.','The helper is copied into report.py before the import.','Importing a sibling module does not require copying its helper definition.','Recall the location associated with ordinary script invocation.')
q('importable_packages',0,'Which layout meets the taught regular-package requirement for the orders modules?','orders/ contains __init__.py and the related .py modules; __init__.py may be empty.','Only orders.py exists, with no directory of modules.','A single module file is not the described directory-based regular package.','orders/ contains the modules but deliberately omits __init__.py.','The taught regular-package layout includes __init__.py, even when empty.','Distinguish the directory from its modules.')
q('logging',0,'Detailed quantity calculation is a DEBUG event and report completion is an INFO event. Application logging is configured at INFO. What should appear?','Report completion, but not the detailed calculation.','Both events, because DEBUG describes more detail.','DEBUG is below the INFO threshold and is excluded.','Neither event, because only WARNING is ever emitted.','WARNING is the default root threshold; configuring INFO changes that threshold.','Compare each event level with the configured threshold.')
q('logging',1,'A module logger propagates events to an ancestor handler. Which arrangement avoids the taught duplicate-output trap?','Configure one suitable ancestor handler without also attaching a redundant module handler.','Attach handlers to both the module logger and its ancestor for the same event.','Propagation can deliver the same event to both handlers, duplicating output.','Replace all logging events with diagnostic prints.','Diagnostic prints do not implement the taught module-logger approach.','Trace which handlers can receive the same propagated event.')
q('main_entry_point',0,'A module must expose cost for imports but prompt for input only during direct execution. Which boundary is correct?','Define cost at module level; guard the prompts and display with if __name__ == "__main__":.','Put cost and all command actions inside the guard.','Import does not execute the guarded body, so the helper would not be defined there.','Leave prompts outside the guard and guard only the print.','Only guarded actions are skipped on import; unguarded prompts would still run.','Check every command-interface action, not just its final output.')
q('argparse_command_line',0,'A parser declares required positional input_path and optional --verbose with store_true. No command-line arguments are supplied. What happens by default?','An argparse error is reported and the process exits with status 2.','input_path becomes an empty string and execution succeeds.','A missing required positional argument is invalid, not an implicit empty value.','--verbose supplies the missing input_path automatically.','The optional boolean flag does not replace the required positional value.','Identify which declaration makes a value required.')
q('module_search_paths',0,'An ordinary script imports a file-backed helper that is not built in. ModuleNotFoundError occurs. What is the relevant first diagnostic?','Inspect sys.path and whether the helper is available in those search locations.','Change the logging threshold instead of inspecting module search locations.','The search locations, not a logging threshold, determine ordinary module discovery.','Assume Python searches every unrelated directory automatically.','Ordinary imports search sys.path, not every directory on the computer.','Focus on where this interpreter searches for the named module.')
q('os_environment',0,'ORDER_LABEL is optional and may be absent. Which expression supplies notebook only when the key is absent?','os.environ.get("ORDER_LABEL", "notebook")','os.environ["ORDER_LABEL"]','Bracket lookup raises KeyError when the key is absent; it does not provide this fallback.','os.environ.get("ORDER_LABEL")','Without a fallback argument, get returns None on absence, not notebook.','Compare optional configuration with required configuration.')
q('os_environment',1,'ORDER_SOURCE is absent. What does os.environ["ORDER_SOURCE"] do?','It raises KeyError.','It returns None.','None on absence is the behavior of get without a fallback, not bracket lookup.','It returns a default directory automatically.','Bracket lookup does not supply a default for a missing key.','The two lookup forms differ on absence.')
q('random_vs_secrets',0,'A simulation needs a repeatable pseudo-random sequence in the same execution environment, with no intervening random calls. Which approach fits?','Use random.seed(7), generate the sequence, reset that seed, and repeat the calls.','Use secrets.token_hex(16) as a seeded simulation sequence.','secrets supplies security-sensitive randomness, not this seeded random simulation workflow.','Call random.random() again without resetting the seed and assume the sequence restarts.','Reproducing the taught sequence requires resetting the seed before repeating the calls.','Separate reproducible modelling from security-sensitive randomness.')
q('random_vs_secrets',1,'Which taught operation fits a security-sensitive random hexadecimal token?','secrets.token_hex(16)','random.seed(7) followed by random.random()','The seeded simulation generator is not the taught cryptographically strong token source.','Reuse the same seeded simulation sequence as the token.','Reproducible modelling behavior is not the security-sensitive randomness supplied by secrets.','Choose based on the purpose of the randomness.')
q('regular_expressions',0,'The requirement is to validate an entire label, not just find an uppercase substring. Which operation matches that scope?','re.fullmatch(pattern, label)','re.search(pattern, label)','search can find a match anywhere without requiring the whole text to match.','re.match(pattern, label)','match checks the beginning rather than imposing the whole-text requirement.','Distinguish whole-text validation from locating a match.')
q('sys_runtime_interface',0,'Which runtime field provides interpreter version, build, and compiler information?','sys.version','sys.executable','executable identifies the executable path when available, not version/build information.','A hard-coded project version string','A fixed string is not an observation of the executing interpreter.','Match the diagnostic field to the information requested.')
q('virtual_environments',0,'A process reports sys.prefix != sys.base_prefix as True. What does the taught diagnostic establish?','The interpreter is running in a virtual environment.','Every documented project import has already succeeded.','The prefix comparison identifies a virtual environment, not import verification.','Activation was necessarily performed before invocation.','Explicit environment-executable invocation does not require activation.','Separate environment identity from dependency checks.')
q('environment_interpreter_selection',0,'An editor shows a .venv label, but the running program reports a system executable path. Which evidence should guide diagnosis?','The running process\'s sys.executable, compared with the intended environment executable.','The label alone proves the intended interpreter ran.','An environment label is not the executed-process evidence used in this check.','Assume any Python executable is the project venv executable.','The actual path must match the intended platform-appropriate environment interpreter.','Inspect the actual process, not only the selection label.')
q('environment_interpreter_selection',1,'After selecting the intended project venv executable in the editor, what is the taught verification?','Rerun and inspect sys.executable plus sys.prefix != sys.base_prefix.','Stop at changing the editor label without rerunning.','Only a rerun reveals which executable the new process actually uses.','Require activation even when the editor invokes the full environment executable path.','Explicit executable invocation does not depend on activation.','Check both process identity and virtual-environment status after the change.')
q('pip_installation',0,'A distribution has been installed. What verifies its documented import is usable in the intended environment?','Run its documented import name using that same environment interpreter.','Guess that the distribution spelling is always the import name.','Distribution and import package names need not be identical.','Rely only on an installation success message.','The documented import under the same interpreter is a separate usability check.','Keep distribution installation and Python import verification separate.')
q('requirements_files',0,'The fresh environment reports successful requirements installation. What is still needed to verify required imports?','Run the documented required imports in the recreated interpreter.','Assume the install report proves every required import works.','The installation report alone is not final evidence of module importability.','Check imports only in the old system interpreter.','Imports must be checked in the recreated interpreter, not another environment.','Which process must demonstrate importability?')

# Inspect-and-judge sets: text excerpts rather than invented registry datasets.
C={}
def cls(c,p,items): C[c]=(p,items)
cls('sys_runtime_interface','Read each diagnostic implementation. Decide whether it displays the actual executable followed by actual version, preserving empty or None executable values.',[
('import sys\nprint(sys.executable)\nprint(sys.version)',True,'Both fields come directly from the running interpreter.'),
('import sys\nprint(sys.executable or "/project/.venv/bin/python")\nprint(sys.version)',False,'The fallback fabricates an executable path when the actual value is empty or None.'),
('print("/project/.venv/bin/python")\nprint("Python 3.13")',False,'Hard-coded text is not the executing runtime\'s diagnostic values.')])
cls('virtual_environments','POSIX order-report project: /project. Selected base interpreter: /usr/bin/python3. Read each independent transcript and decide whether it proves creation and explicit use of the project venv, a True prefix comparison, and successful package listing.',[
('/usr/bin/python3 -m venv .venv -> success\n/project/.venv/bin/python diagnostic.py\nsys.executable: /project/.venv/bin/python\nsys.prefix != sys.base_prefix: True\n/project/.venv/bin/python -m pip list -> success',True,'Creation, explicit venv execution, prefix comparison and listing all meet the criterion.'),
('/usr/bin/python3 -m venv .venv -> success\n/usr/bin/python3 diagnostic.py\nsys.executable: /usr/bin/python3\nsys.prefix != sys.base_prefix: False\n/usr/bin/python3 -m pip list -> success',False,'The later commands use system Python, not the created environment.'),
('/usr/bin/python3 -m venv .venv -> success\n/project/.venv/bin/python diagnostic.py\nsys.executable: /project/.venv/bin/python\nsys.prefix != sys.base_prefix: True\nNo package listing was performed.',False,'The required package-listing evidence is missing.')])
cls('environment_interpreter_selection','Read each editor-change and rerun excerpt. On POSIX the intended existing interpreter is /project/.venv/bin/python. Decide whether the change is verified by the actual rerun.',[
('Editor executable = /project/.venv/bin/python\nRerun sys.executable = /project/.venv/bin/python\nRerun sys.prefix != sys.base_prefix = True',True,'The explicit selection and both rerun observations identify the intended venv.'),
('Editor label = .venv\nRerun sys.executable = /usr/bin/python3\nRerun sys.prefix != sys.base_prefix = False',False,'The label does not override the system-runtime evidence.'),
('Editor executable = /project/.venv/bin/python\nNo rerun has occurred.',False,'The selected executable has not been verified in a new process.')])
cls('pip_installation','Project documentation specifies distribution Pillow and import PIL. The intended existing POSIX interpreter is /project/.venv/bin/python. Read each transcript and decide whether installation, inspection, and documented import are all verified in that same environment.',[
('/project/.venv/bin/python -m pip install Pillow -> success\n/project/.venv/bin/python -m pip show Pillow -> Pillow installed\n/project/.venv/bin/python import_check.py (import PIL) -> no import error',True,'All three checks use the intended executable and the documented names.'),
('/project/.venv/bin/python -m pip install Pillow -> success\n/project/.venv/bin/python -m pip show Pillow -> Pillow installed\n/usr/bin/python3 import_check.py (import PIL) -> no import error',False,'The import check runs in another interpreter and does not verify this environment.'),
('/project/.venv/bin/python -m pip install Pillow -> success\n/project/.venv/bin/python -m pip show Pillow -> Pillow installed\n/project/.venv/bin/python import_check.py (import Pillow) -> ModuleNotFoundError',False,'The script guesses the distribution spelling rather than using documented import PIL.')])
cls('requirements_files','Project documentation: requirements.txt contains Pillow==11.1.0; required import is PIL. Fresh POSIX interpreter: /project/.venv/bin/python. Read each transcript and decide whether pinned installation, version listing, and required import are verified in that interpreter.',[
('/project/.venv/bin/python -m pip install -r requirements.txt -> success\n/project/.venv/bin/python -m pip list -> Pillow 11.1.0\n/project/.venv/bin/python import_check.py (import PIL) -> no import error',True,'The fresh interpreter installs the pinned requirement, confirms its version and imports the documented name.'),
('/project/.venv/bin/python -m pip install -r requirements.txt -> success\n/project/.venv/bin/python -m pip list -> Pillow 11.1.0\nNo import check performed.',False,'Installation and listing do not alone verify the required import.'),
('/project/.venv/bin/python -m pip install -r requirements.txt -> success\n/usr/bin/python3 -m pip list -> Pillow 11.1.0\n/usr/bin/python3 import_check.py (import PIL) -> no import error',False,'Listing and import in system Python are not verification of the recreated interpreter.')])

E={}
def ex(c,p,starter,sol,tests): E[c]=(p,starter,sol,tests)
def val(expr): return ('value_equals',{'expr':expr})
def call(f,args): return ('function_call',{'function':f,'args':args})
ex('datetime_operations','Keep the supplied first and second input strings. Parse each with %Y-%m-%d and .date(), reassigning first and second to calendar dates. Print (second - first).days followed by (first - second).days, one per line.',"from datetime import datetime\nfirst = '2025-03-01'\nsecond = '2025-03-04'\n# Parse and print both signed differences.\n","from datetime import datetime\nfirst = '2025-03-01'\nsecond = '2025-03-04'\nfirst = datetime.strptime(first, '%Y-%m-%d').date()\nsecond = datetime.strptime(second, '%Y-%m-%d').date()\nprint((second - first).days)\nprint((first - second).days)\n",[('stdout_equals',{})])
# The pinned runner executes one entry; fixed scaffolding materializes real sibling/package files from the cost definition above it.
local_scaffold='''
# Fixed workspace adapter: materialize the helper definition in a sibling file.
import inspect as _inspect, pathlib as _pathlib, ast as _ast
_pathlib.Path('helpers.py').write_text(_inspect.getsource(cost))
del cost
'''
local_head='quantity = 3\nprice = 4\ndef cost(quantity, price):\n    return quantity * price\n'
local_tail='''
# Fixed adapter records the report section as report.py for layout verification.
_text = _pathlib.Path(__file__ if '__file__' in globals() else 'main.py').read_text()
_pathlib.Path('report.py').write_text(_text.split('# REPORT SECTION\\n', 1)[1].split('# END REPORT', 1)[0])
'''
ls=local_head+local_scaffold+'# REPORT SECTION\n# Import and call the sibling helper; store result.\n# END REPORT\n'+local_tail
lo=local_head+local_scaffold+'# REPORT SECTION\nimport helpers\nresult = helpers.cost(quantity, price)\n# END REPORT\n'+local_tail
ex('local_modules','The fixed adapter moves the cost definition above it into helpers.py and records your REPORT SECTION as report.py. In that section, import helpers and set result to helpers.cost(quantity, price), using the supplied inputs. Do not redefine cost in the report section. Keep the adapter unchanged.',ls,lo,[val("[result, helpers.cost(quantity, price), not any(isinstance(n, _ast.FunctionDef) and n.name == 'cost' for n in _ast.parse(_pathlib.Path('report.py').read_text()).body)]")])
pkg_scaffold='''
# Fixed workspace adapter groups the helper and a second related module.
import inspect as _inspect, pathlib as _pathlib
_pathlib.Path('orders').mkdir(exist_ok=True)
_pathlib.Path('orders/__init__.py').write_text('')
_pathlib.Path('orders/costs.py').write_text(_inspect.getsource(cost))
_pathlib.Path('orders/reports.py').write_text(_inspect.getsource(report))
del cost, report
'''
ph='quantity = 3\nprice = 4\ndef cost(quantity, price):\n    return quantity * price\ndef report():\n    return quantity\n'
# Second module function is supplied scaffolding; learners group/access the regular package via the adapter.
ex('importable_packages','The fixed adapter groups the supplied cost helper and related report helper into orders/costs.py and orders/reports.py with an empty orders/__init__.py. Complete the code after the adapter: import orders.costs, assign result from orders.costs.cost(quantity, price), and print result. Preserve the helper definitions and adapter.',ph+pkg_scaffold+'# Import the packaged helper and compute result.\n',ph+pkg_scaffold+'import orders.costs\nresult = orders.costs.cost(quantity, price)\nprint(result)\n',[val("[result, orders.costs.cost(quantity, price), _pathlib.Path('orders/__init__.py').read_text(), _pathlib.Path('orders/reports.py').is_file()]")])
logging_setup='''import logging
# Fixed adapter supplies variable messages and captures actual emitted events.
detail = 'Detailed quantity calculation'
completion = 'Report complete'
import io as _io
_stream = _io.StringIO()
logging.root.handlers.clear()
logging.root.setLevel(logging.WARNING)
logging.basicConfig(stream=_stream, format='%(message)s')
'''
ex('logging','Replace both diagnostic prints in report() with logger.debug(detail) and logger.info(completion). Obtain logger with logging.getLogger(__name__) and set application logging at INFO with logging.basicConfig(level=logging.INFO). Keep the fixed capture adapter unchanged. The completion event must appear once and the detail event must be excluded.',logging_setup+'def report():\n    print(detail)\n    print(completion)\nreport()\n',logging_setup+'logging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(__name__)\ndef report():\n    logger.debug(detail)\n    logger.info(completion)\nreport()\n',[val("[_stream.getvalue(), len(logger.handlers)]")])
# Fresh root already has capture handler; basicConfig is a no-op unless we supply a scaffold config wrapper for the requested call.
# Preserve ordinary semantics by removing the initial handler and forwarding stream/format in the scaffold.
old="logging.basicConfig(stream=_stream, format='%(message)s')"
new="_basic = logging.basicConfig\ndef _capture_config(*args, **kwargs):\n    kwargs.setdefault('stream', _stream)\n    kwargs.setdefault('format', '%(message)s')\n    return _basic(*args, **kwargs)\nlogging.basicConfig = _capture_config"
p,st,so,ts=E['logging'];E['logging']=(p,st.replace(old,new),so.replace(old,new),ts)
main_scaffold='''# Fixed adapter supplies interactive input for the direct run, and a separate import-mode check.
quantity_input = 3
price_input = 4
import builtins as _builtins, io as _io, contextlib as _contextlib, pathlib as _pathlib
_inputs = iter([str(quantity_input), str(price_input)])
_builtin_input = _builtins.input
_builtins.input = lambda prompt='': next(_inputs)
'''
main_tail='''
# Fixed adapter checks the same learner section in import mode with prompts forbidden.
_builtins.input = _builtin_input
def import_case(q, p):
    section = _pathlib.Path('main.py').read_text().split('# LEARNER SECTION\\n', 1)[1].split('# END LEARNER', 1)[0]
    out = _io.StringIO()
    def forbidden(prompt=''):
        raise RuntimeError('prompt during import')
    previous = _builtins.input
    _builtins.input = forbidden
    try:
        ns = {'__name__': 'report'}
        with _contextlib.redirect_stdout(out):
            exec(section, ns)
        return [out.getvalue(), ns['cost'](q,p)]
    finally:
        _builtins.input = previous
'''
body='def cost(quantity, price):\n    return quantity * price\n\nquantity = int(input("Quantity: "))\nprice = int(input("Price: "))\nprint(cost(quantity, price))\n'
solbody='def cost(quantity, price):\n    return quantity * price\n\nif __name__ == "__main__":\n    quantity = int(input("Quantity: "))\n    price = int(input("Price: "))\n    print(cost(quantity, price))\n'
ex('main_entry_point','In the LEARNER SECTION, keep cost at module level and place both prompts, conversions, and the calculated-cost print inside if __name__ == "__main__":. The adapter supplies direct-run inputs quantity_input and price_input. Import mode must have no prompts or output and retain a callable cost. Keep all adapter code unchanged.',main_scaffold+'# LEARNER SECTION\n'+body+'# END LEARNER\n'+main_tail,main_scaffold+'# LEARNER SECTION\n'+solbody+'# END LEARNER\n'+main_tail,[('stdout_equals',{}),call('import_case',[3,4]),call('import_case',[4,7])])
args_scaffold='''# Fixed adapter supplies the command line and independently checks fresh invocations.
path_input = 'orders.csv'
import sys as _sys, pathlib as _pathlib, io as _io, contextlib as _contextlib
_old_argv = _sys.argv
_sys.argv = ['report.py', path_input]
'''
args_tail='''
_sys.argv = _old_argv
def command_case(argv):
    code = _pathlib.Path('main.py').read_text().split('# LEARNER SECTION\\n',1)[1].split('# END LEARNER',1)[0]
    out, err = _io.StringIO(), _io.StringIO()
    previous = _sys.argv
    _sys.argv = ['report.py'] + argv
    status = 0
    try:
        with _contextlib.redirect_stdout(out), _contextlib.redirect_stderr(err):
            try:
                exec(code, {'__name__': '__main__'})
            except SystemExit as e:
                status = e.code
        return [out.getvalue().strip(), status, 'input_path' in err.getvalue()]
    finally:
        _sys.argv = previous
'''
ab='import argparse\n# Define the parser and print parsed attributes.\n'
asol='import argparse\nparser = argparse.ArgumentParser()\nparser.add_argument("input_path")\nparser.add_argument("--verbose", action="store_true")\nargs = parser.parse_args()\nprint(args.input_path, args.verbose)\n'
ex('argparse_command_line','Complete the LEARNER SECTION with an ArgumentParser, required positional input_path, and --verbose using action="store_true". Parse the command line into args and print args.input_path, args.verbose. Preserve the adapter, which checks orders.csv without the flag, with the flag, and with no required argument (error and exit 2).',args_scaffold+'# LEARNER SECTION\n'+ab+'# END LEARNER\n'+args_tail,args_scaffold+'# LEARNER SECTION\n'+asol+'# END LEARNER\n'+args_tail,[('stdout_equals',{}),call('command_case',[['orders.csv']]),call('command_case',[['orders.csv','--verbose']]),call('command_case',[[]])])
search_scaffold='''# Workspace filename: json.py
# Fixed adapter materializes the editable local filename and runs a fresh diagnostic import.
project = 'order_project'
import pathlib as _pathlib, sys as _sys
_filename = _pathlib.Path('main.py').read_text().splitlines()[0].split(': ',1)[1]
_pathlib.Path(project).mkdir(exist_ok=True)
_pathlib.Path(project, _filename).write_text('# Local report data module.\\n')
_sys.path.insert(0, str(_pathlib.Path(project).resolve()))
_sys.modules.pop('json', None)
'''
searchbody='import sys\nimport json\nprint(sys.path)\nprint(json.__file__)\n'
ex('module_search_paths','The first-line Workspace filename controls the local file materialized by the fixed adapter. Diagnose the conflicting json.py using sys.path and json.__file__. Rename that first-line filename to report_data.py and retain the diagnostic imports and both prints. In a fresh run json.__file__ must identify the standard library, not the local file. Keep the adapter unchanged.',search_scaffold+searchbody,search_scaffold.replace('# Workspace filename: json.py','# Workspace filename: report_data.py')+searchbody,[val("[sys.path[0], json.__file__, _pathlib.Path(project, 'report_data.py').exists(), not _pathlib.Path(project, 'json.py').exists()]")])
env_scaffold='''# Fixed adapter supplies process configuration and tests separate environment cases.
configured_source = 'orders'
import os, pathlib as _pathlib, io as _io, contextlib as _contextlib
os.environ['ORDER_SOURCE'] = configured_source
'''
env_tail='''
def environment_case(value):
    code = _pathlib.Path('main.py').read_text().split('# LEARNER SECTION\\n',1)[1].split('# END LEARNER',1)[0]
    previous = os.environ.get('ORDER_SOURCE')
    if value is None:
        os.environ.pop('ORDER_SOURCE', None)
    else:
        os.environ['ORDER_SOURCE'] = value
    out = _io.StringIO()
    try:
        with _contextlib.redirect_stdout(out):
            exec(code, {'__name__': '__main__', 'os': os})
        return out.getvalue().strip()
    finally:
        if previous is None:
            os.environ.pop('ORDER_SOURCE', None)
        else:
            os.environ['ORDER_SOURCE'] = previous
'''
eb='required = None\n# Get ORDER_SOURCE and explicitly distinguish absence.\n'
es='required = os.environ.get("ORDER_SOURCE")\nif required is None:\n    print("Missing ORDER_SOURCE configuration")\nelse:\n    print(required)\n'
ex('os_environment','In the LEARNER SECTION assign required using os.environ.get("ORDER_SOURCE"). Use required is None to print Missing ORDER_SOURCE configuration on absence; otherwise print the retrieved string, including an empty string if configured. Preserve the fixed adapter, which supplies separate configured, absent, and empty-string cases.',env_scaffold+'# LEARNER SECTION\n'+eb+'# END LEARNER\n'+env_tail,env_scaffold+'# LEARNER SECTION\n'+es+'# END LEARNER\n'+env_tail,[('stdout_equals',{}),call('environment_case',['orders']),call('environment_case',[None]),call('environment_case',[''])])
rh='import random\nseed = 7\nrandom.seed(seed)\n'
rs='a = random.random()\nb = random.random()\nfirst = [a, b]\nrandom.seed(seed)\nc = random.random()\nd = random.random()\nsecond = [c, d]\nprint(first)\nprint(second)\nprint(first == second)\nprint(a >= 0.0 and a < 1.0 and b >= 0.0 and b < 1.0 and c >= 0.0 and c < 1.0 and d >= 0.0 and d < 1.0)\n'
ex('random_vs_secrets','Using the supplied seed (7), store two successive random.random() values as a and b and list first = [a, b]. Reset the same seed, generate c and d, and store second = [c, d]. Print first, second, their equality, and one boolean confirming each of a, b, c, d is >= 0.0 and < 1.0, in that order. Do not insert other random calls.',rh+'# Generate and repeat the two-value sequence.\n',rh+rs,[('stdout_equals',{})])
rxh="import re\nlabels = ['BLUE', 'A', 'Blue', 'BLUE!', '']\n"
rxb="pattern = None\nfor label in labels:\n    accepted = None\n    print(label, accepted)\n"
rxs='pattern = r"[A-Z][A-Z]*"\nfor label in labels:\n    accepted = re.fullmatch(pattern, label) is not None\n    print(label, accepted)\n'
# Include a string input variable to obtain realistic whole-label mutations.
rxh="import re\nfirst_label = 'BLUE'\nlabels = [first_label, 'A', 'Blue', 'BLUE!', '']\n"
ex('regular_expressions','Use a pattern requiring one uppercase letter followed by zero or more uppercase letters. For each supplied label, set accepted from re.fullmatch(pattern, label) is not None and print label, accepted. BLUE and A must be accepted; Blue, BLUE!, and empty text must be rejected. Keep the input list and loop order.',rxh+rxb,rxh+rxs,[('stdout_equals',{})])

exec((B/'working/simplify_tasks.py').read_text())
exec((B/'working/final_task_adjustments.py').read_text())

out={k:P[k] for k in ['schema_version','path_id','batch_id']};out['kind']='interactions_part';out['tiles']=[]
code_jobs=[];code_refs=[]
for t in P['tiles']:
 tile={'tile_id':t['tile_id'],'interactions':[]};out['tiles'].append(tile)
 checks=[s for s in t['steps'] if s['type'] in ('check','hands_on')]
 seen=set(); counters={}
 rem=next(z for z in S['tiles'] if z['tile_id']==t['tile_id'])['remediation_steps']
 for i,s in enumerate(checks):
  cid=s['concept_ids'][0]; c=cid.split('.',1)[1]; g=G[cid]; typ=s['planned_interaction_type']
  measures=[]
  for anchor in s['anchors']:
   if '#assessment:' in anchor:
    cap=anchor.split('#assessment:')[1]; a=next(a for a in g['assessment_anchors'] if a['capability']==cap);measures.append({'concept_id':cid,'capability':cap,'fact_ids':a['fact_ids']})
  ix={'type':typ,'interaction_id':'ix.'+s['step_id'],'difficulty':'intro' if i==0 else ('stretch' if i==len(checks)-1 else 'core'),'grading_mode':'client','standalone':typ!='code_exercise','measures':measures,'anchors':s['anchors'],'feedback':{'correct':{'message':'Correct: your judgement follows the stated requirement.'},'incorrect':{'message':'Recheck the requirement and the supplied evidence before trying again.'},'hints':['Compare the requested behavior with each step of the supplied code or evidence.']}}
  if cid not in seen:
   candidates=[r for r in rem if cid in r['concept_ids']]
   if candidates: ix['feedback']['remediation_step_id']=candidates[0]['step_id']
   seen.add(cid)
  if typ=='choice':
   n=counters.get(c,0);counters[c]=n+1
   p,right,w1,why1,w2,why2,h=Q[(c,n)]
   options=[{'option_id':'correct','text':right},{'option_id':'trap1','text':w1},{'option_id':'trap2','text':w2}]
   ix['public']={'prompt':p,'options':options,'selection':'single','shuffle':True}
   ix['grading']={'correct_option_ids':['correct'],'option_feedback':{'correct':{'message':'Correct. '+right},'trap1':{'message':why1},'trap2':{'message':why2}}}
   ix['feedback']['correct']['message']='Correct. '+right
   ix['feedback']['incorrect']['message']='Compare the alternatives with the taught distinction; the selected claim does not meet it.'
   ix['feedback']['hints']=[h]
  elif typ=='classify':
   p,items=C[c];ix['public']={'prompt':p,'buckets':[{'bucket_id':'meets','label':'Meets the stated criterion'},{'bucket_id':'fails','label':'Does not meet the stated criterion'}],'items':[]}
   ix['grading']={'assignments':{},'item_feedback':{}}
   for j,(txt,ok,why) in enumerate(items):
    ident='excerpt'+str(j+1);ix['public']['items'].append({'item_id':ident,'text':txt});ix['grading']['assignments'][ident]='meets' if ok else 'fails';ix['grading']['item_feedback'][ident]={'message':why}
  else:
   p,st,so,ts=E[c]
   ix['public']={'prompt':p,'runtime':{'kind':'python','version':R['version'],'packages':[]},'workspace':{'entry':'main.py','files':[{'path':'main.py','role':'editable','language':'python','content':st}],'asset_mounts':[]},'constraints':{k:copy.deepcopy(g['practice_anchor']['live_code'][k]) for k in ['allowed_syntax','blocked_syntax']}}
   ix['grading']={'solution_files':[{'path':'main.py','content':so}],'tests':[]}
   for j,(kind,spec) in enumerate(ts):
    ix['grading']['tests'].append({'test_id':'test'+str(j+1),'kind':kind,'spec':copy.deepcopy(spec),'visible':True,'message_on_fail':'The result or required behavior differs from the prompt. Review the learner section and leave the fixed adapter unchanged.'})
   if not measures: ix['measures']=copy.deepcopy([{'concept_id':cid,**a} for a in g['assessment_anchors']])
   sid=s['step_id'];probes=[sandbox._py_probe(test) for test in ix['grading']['tests'] if test['kind']!='stdout_equals']
   code_jobs.append(sandbox._py_script(sid,'main.py',so,[],probes));code_refs.append((sid,ix))
  tile['interactions'].append({'step_id':s['step_id'],'interaction':ix})
# Compute every Python expected in the pinned runtime, not by typing output values.
res=sandbox.node_run(sandbox._py_job('python',[],code_jobs),R['runner'])['results']
for sid,ix in code_refs:
 r=res[sid]
 if not r['ok']: raise RuntimeError((sid,r))
 for test in ix['grading']['tests']:
  if test['kind']=='stdout_equals': v=r['stdout']
  else:
   probe=r['probes'][test['test_id']]
   if not probe['ok']: raise RuntimeError((sid,probe))
   v=probe['value']
  test['spec']['expected']=v
(B/'interactions.json').write_text(json.dumps(out,indent=2)+'\n')
print('tiles',len(out['tiles']),'interactions',sum(len(t['interactions']) for t in out['tiles']))
