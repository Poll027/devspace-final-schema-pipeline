# Imported by build_interactions.py. Narrow edits to constructs the fixed syntax gate recognizes;
# all constraints remain copied verbatim. Fixed adapters and skeletons supply the rest.
def fixed(text):
    return 'if True:  # Fixed scaffold; leave this block unchanged.\n' + ''.join('    '+line+'\n' for line in text.rstrip().splitlines())
# Calendar-date task: parsing and arithmetic are prewritten, learner obtains dates and displays timedelta days.
rows=next(a['rows'] for a in A['assets'] if a['asset_id']=='ds.report_dates')
first_day=int(rows[0][0][-2:]);second_day=int(rows[0][1][-2:])
dh=f'first_day = {first_day}\nsecond_day = {second_day}\n'+fixed('from datetime import datetime\nfirst_text = f"2025-03-{first_day:02d}"\nsecond_text = f"2025-03-{second_day:02d}"\nfirst = datetime.strptime(first_text, "%Y-%m-%d")\nsecond = datetime.strptime(second_text, "%Y-%m-%d")')
dtail=fixed('forward = second - first\nreverse = first - second')
ex('datetime_operations','The fixed scaffold builds the two supplied year-month-day strings and parses them with %Y-%m-%d. Complete the editable lines: reassign first and second using their .date() methods. The fixed arithmetic then computes forward = second - first and reverse = first - second. Print forward.days and reverse.days in that order, one per line. Keep the day inputs and fixed blocks unchanged.',dh+'# Obtain calendar dates here.\n'+dtail+'# Print both signed day counts.\n',dh+'first = first.date()\nsecond = second.date()\n'+dtail+'print(forward.days)\nprint(reverse.days)\n',[('stdout_equals',{}),val("[type(first).__name__, type(second).__name__, forward.days, reverse.days]")])
# Sibling/package helper definitions and adapters are fixed, with the learner applying a taught direct import.
local_scaffold=local_scaffold.replace('import inspect as _inspect, pathlib as _pathlib, ast as _ast','import inspect as _inspect, pathlib as _pathlib, ast as _ast, textwrap as _textwrap').replace('_inspect.getsource(cost)','_textwrap.dedent(_inspect.getsource(cost))')
lbase='quantity = 3\nprice = 4\n'+fixed('def cost(quantity, price):\n    return quantity * price\n'+local_scaffold)
ls=lbase+'# REPORT SECTION\nresult = None\n# Import cost from helpers and compute result.\n# END REPORT\n'+fixed(local_tail)
lo=lbase+'# REPORT SECTION\nfrom helpers import cost\nresult = cost(quantity, price)\n# END REPORT\n'+fixed(local_tail)
ex('local_modules','The fixed scaffold extracts the supplied cost definition into sibling helpers.py. Complete the REPORT SECTION using from helpers import cost and assign result = cost(quantity, price). Do not define cost in that report section. The final fixed block records this section as report.py. Keep the inputs and adapters unchanged.',ls,lo,[val("[result, cost(quantity, price), cost.__module__, not any(isinstance(n, _ast.FunctionDef) and n.name == 'cost' for n in _ast.parse(_pathlib.Path('report.py').read_text()).body)]")])
pkg_scaffold=pkg_scaffold.replace('import inspect as _inspect, pathlib as _pathlib','import inspect as _inspect, pathlib as _pathlib, textwrap as _textwrap').replace('_inspect.getsource(cost)','_textwrap.dedent(_inspect.getsource(cost))').replace('_inspect.getsource(report)','_textwrap.dedent(_inspect.getsource(report))')
pbase='quantity = 3\nprice = 4\n'+fixed('def cost(quantity, price):\n    return quantity * price\ndef report(quantity):\n    return quantity\n'+pkg_scaffold+'\nimport orders.costs')
ex('importable_packages','The fixed scaffold creates the orders regular-package layout with empty __init__.py, costs.py, and the related reports.py module. Use the taught direct helper import from orders.costs import cost; assign result = cost(quantity, price) and print result. The helper must come from orders.costs, not a new local definition. Keep the inputs and layout adapter unchanged.',pbase+'result = None\n# Import the packaged helper and compute result.\n',pbase+'from orders.costs import cost\nresult = cost(quantity, price)\nprint(result)\n',[val("[result, orders.costs.cost(quantity, price), cost.__module__, _pathlib.Path('orders/__init__.py').read_text(), _pathlib.Path('orders/reports.py').is_file()]")])
# Logging skeleton provides the report helper; learner obtains the logger and configures the threshold.
logbase="detail = 'Detailed quantity calculation'\ncompletion = 'Report complete'\n"+fixed("import logging, io as _io\n_stream = _io.StringIO()\nlogging.root.handlers.clear()\nlogging.root.setLevel(logging.WARNING)\n_basic = logging.basicConfig\ndef _capture_config(*args, **kwargs):\n    kwargs.setdefault('stream', _stream)\n    kwargs.setdefault('format', '%(message)s')\n    return _basic(*args, **kwargs)\nlogging.basicConfig = _capture_config\ndef report():\n    logger.debug(detail)\n    logger.info(completion)")
ex('logging','The fixed report helper already emits detail with logger.debug and completion with logger.info, without diagnostic prints or a redundant module handler. Complete the editable setup with import logging as logging, logging.basicConfig(level=logging.INFO), and logger = logging.getLogger(__name__). Then the supplied report() call must emit only the completion message, once. Leave the helper and capture adapter unchanged.',logbase+'# Configure application logging and obtain logger.\nreport()\n',logbase+'import logging as logging\nlogging.basicConfig(level=logging.INFO)\nlogger = logging.getLogger(__name__)\nreport()\n',[val("[_stream.getvalue(), len(logger.handlers)]")])
# Main guard is prewritten. Completing the converters preserves the guard and importable helper.
main_start='quantity_input = 3\nprice_input = 4\n'+fixed(main_scaffold.split('import builtins',1)[1].join(['import builtins','']) if False else main_scaffold[main_scaffold.index('import builtins'):])
main_body='''def cost(quantity, price):
    return quantity * price

if __name__ == "__main__":
    quantity = quantity_converter(input("Quantity: "))
    price = price_converter(input("Price: "))
    print(cost(quantity, price))
'''
# In the actual entry, the definition is fixed as a block, while the inspected import section is clean module source.
main_fixed=fixed(main_body)
main_tail2=main_tail.replace("section = _pathlib.Path('main.py').read_text().split('# LEARNER SECTION\\n', 1)[1].split('# END LEARNER', 1)[0]", "section = _pathlib.Path('main.py').read_text().split('# LEARNER SECTION\\n', 1)[1].split('# END LEARNER', 1)[0]")
mbstart=main_start+'# LEARNER SECTION\n'
mbend=main_fixed+'# END LEARNER\n'+fixed(main_tail2)
ex('main_entry_point','The supplied skeleton keeps cost importable and guards both prompts and output with if __name__ == "__main__":. Complete quantity_converter = int and price_converter = int before that fixed guard. Leave all fixed blocks unchanged. Direct execution must convert the supplied interactive inputs and display their calculated cost; importing must neither prompt nor display, and cost must remain callable.',mbstart+'quantity_converter = None\nprice_converter = None\n'+mbend,mbstart+'quantity_converter = int\nprice_converter = int\n'+mbend,[('stdout_equals',{}),call('import_case',[3,4]),call('import_case',[4,7])])
# Command interface retains all learner-authored argparse lines, only the adapter functions are fixed blocks.
p,st,so,ts=E['argparse_command_line']
E['argparse_command_line']=(p, fixed(args_scaffold.replace("path_input = 'orders.csv'\n",''))+"path_input = 'orders.csv'\n" if False else st, so,ts)
arg_start="path_input = 'orders.csv'\n"+fixed(args_scaffold.replace("path_input = 'orders.csv'\n",''))+'# LEARNER SECTION\n'
ex('argparse_command_line',p,arg_start+ab+'# END LEARNER\n'+fixed(args_tail),arg_start+asol+'# END LEARNER\n'+fixed(args_tail),ts)
# Environment skeleton supplies retrieval and the explicit None check; learner completes the absence message.
envstart="configured_source = 'orders'\n"+fixed(env_scaffold.replace("configured_source = 'orders'\n",''))+'# LEARNER SECTION\n'
envbody=fixed('required = os.environ.get("ORDER_SOURCE")\nif required is None:\n    print(missing_message)\nelse:\n    print(required)')
envprefix=fixed('supplied_message = "Missing ORDER_SOURCE configuration"')
ex('os_environment','The fixed skeleton retrieves ORDER_SOURCE using os.environ.get and checks required is None, preserving a configured empty string. Complete missing_message = supplied_message before the skeleton so absence displays Missing ORDER_SOURCE configuration instead of None. The configured run must display its actual directory string. Leave lookup, branching, inputs, and the separate-case adapter unchanged.',envstart+envprefix+'missing_message = None\n'+envbody+'# END LEARNER\n'+fixed(env_tail),envstart+envprefix+'missing_message = supplied_message\n'+envbody+'# END LEARNER\n'+fixed(env_tail),[('stdout_equals',{}),call('environment_case',['orders']),call('environment_case',[None]),call('environment_case',[''])])
# The seeded sequence skeleton handles the draw/reset calls; learner selects the supplied seed and displays the demonstration.
rbase='initial_seed = 7\n'
rblock=fixed('import random\nrandom.seed(seed)\na = random.random()\nb = random.random()\nfirst = [a, b]\nrandom.seed(seed)\nc = random.random()\nd = random.random()\nsecond = [c, d]\nmatching = first == second\nin_bounds = a >= 0.0 and a < 1.0 and b >= 0.0 and b < 1.0 and c >= 0.0 and c < 1.0 and d >= 0.0 and d < 1.0')
ex('random_vs_secrets','The fixed skeleton seeds random, draws two values, resets the same seed, and repeats those draws. Complete seed = initial_seed (the supplied seed is 7), preserving the skeleton without intervening calls. Print first, second, matching, and in_bounds in that order, one per line. The displayed sequences must match and every value must be >= 0.0 and < 1.0.',rbase+'seed = None\n# Choose the supplied seed.\n'+rblock+'# Display the two sequences and checks.\n',rbase+'seed = initial_seed\n'+rblock+'print(first)\nprint(second)\nprint(matching)\nprint(in_bounds)\n',[('stdout_equals',{})])
rxbase="first_label = 'BLUE'\n"+fixed("import re\nlabels = [first_label, 'A', 'Blue', 'BLUE!', '']\nnonempty_uppercase = r'[A-Z][A-Z]*'\npossibly_empty_uppercase = r'[A-Z]*'")
rxblock=fixed('for label in labels:\n    accepted = re.fullmatch(pattern, label) is not None\n    print(label, accepted)')
ex('regular_expressions','Choose the supplied pattern that requires at least one uppercase letter: complete pattern = nonempty_uppercase or pattern = possibly_empty_uppercase as appropriate. The fixed loop uses re.fullmatch and is not None, printing label and accepted for each supplied label. It must accept BLUE and A and reject Blue, BLUE!, and empty text. Leave the input list and validation loop unchanged.',rxbase+'pattern = None\n'+rxblock,rxbase+'pattern = nonempty_uppercase\n'+rxblock,[('stdout_equals',{})])
# Use symbolic documented dependency information, not unsupported real-package/version claims.
for c in ('pip_installation','requirements_files'):
    p,items=C[c]
    p=p.replace('Pillow==11.1.0','package_name==version').replace('Pillow','package_name').replace('PIL','module_name')
    C[c]=(p,[(text.replace('Pillow 11.1.0','package_name version').replace('Pillow','package_name').replace('PIL','module_name'),ok,why.replace('PIL','module_name')) for text,ok,why in items])
