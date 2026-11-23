# Constrained variants: supplied implementations are scaffolding; learner edits only named assignments/calls.
# Keep glossary constraints verbatim, including descriptors the current detector cannot map.
def supplied(body):
 return '# Supplied candidate implementations; inspect but do not edit this block.\nif True:\n'+''.join('    '+line+'\n' for line in body.splitlines())+'\n'

def select(cid,prompt,inputs,body,blanks,bindings,tail,exprs,calls=None):
 common=inputs+supplied(body)
 starter=common+blanks+tail;solution=common+bindings+tail
 code(cid,prompt,starter,solution,exprs,calls)

cid='python.exception_propagation';prompt,st,so,tests=C[cid]
function='def quantity(text):\n    return int(text)\n'
# Function itself is unchanged instructor scaffolding, rather than learner-authored syntax.
st=st.replace(function,supplied(function));so=so.replace(function,supplied(function));C[cid]=(prompt,st,so,tests)

select('finally_cleanup','Inspect release_only and release_and_override. Select the implementation of read_quantity that releases the supplied already-open file in finally without replacing a pending result or exception: bind read_quantity to your chosen candidate. Keep the candidate block and harness unchanged. The checker requires good_result to retain conversion, both files closed, and failure to record ValueError for unsuitable contents.',
'valid_number = 3\ninvalid_text = "three"\n',
'''def release_only(text):
    try:
        return int(text.read())
    finally:
        text.close()

def release_and_override(text):
    try:
        return int(text.read())
    finally:
        text.close()
        return 0''',
'read_quantity = None\n','read_quantity = release_only\n',
'''# Instructor harness: create already-open file fixtures; leave unchanged.
import io
good = io.StringIO(str(valid_number))
bad = io.StringIO(invalid_text)
good_result = read_quantity(good)
try:
    read_quantity(bad)
    failure = "no failure"
except ValueError as exc:
    failure = type(exc).__name__
''', ['[good_result, good.closed, bad.closed, failure]'])

select('functions_as_values','Inspect apply_supplied and apply_fixed. Bind apply to the helper that invokes its supplied operation(value), not a fixed transformation. Bind chosen to double without calling it. Keep the supplied input and implementations. The checker checks chosen identity and apply with both double and another supplied callable.',
'input_value = 3\n',
'''def double(value):
    return value * 2

def increment(value):
    return value + 1

def apply_supplied(operation, value):
    return operation(value)

def apply_fixed(operation, value):
    return double(value)''',
'apply = None\nchosen = None\n','apply = apply_supplied\nchosen = double\n','', ['[chosen is double, apply(chosen, input_value), apply(increment, input_value)]'])

select('closures_and_enclosing_scope','Read the two factory implementations. Bind make_counter to the one returning an advance function that retains and increments its enclosing count using nonlocal. Keep initial_count and the supplied separate factory calls. The checker calls counter twice and other once; for initial_count = 0, the results must be 1, 2, 1 and the functions must retain independent state.',
'initial_count = 0\n',
'''def retained_factory():
    count = initial_count
    def advance():
        nonlocal count
        count = count + 1
        return count
    return advance

def reset_factory():
    def advance():
        count = initial_count
        count = count + 1
        return count
    return advance''',
'make_counter = None\n','make_counter = retained_factory\n',
'counter = make_counter()\nother = make_counter()\n', ['[counter(), counter(), other()]'])

st='''from pathlib import Path
base_directory = "/work/project"
base = Path(base_directory)
# Candidate paths; keep these supplied constructions unchanged.
relative_child = base / "orders.csv"
absolute_replacement = base / "/orders.csv"
output = None
print(output)
'''
code('pathlib_paths','Inspect the two supplied Path constructions. Assign output to the candidate representing the relative orders.csv child beneath the explicit absolute base, rather than an absolute child that replaces base. Keep the path constructions and base_directory unchanged; no filesystem operations are needed. The checker reads str(output).',st,st.replace('output = None','output = relative_child'),['str(output)'])

select('raising_exceptions','Read both cost implementations. Bind cost to the one that raises ValueError("quantity must be nonnegative") for negative numeric arguments and preserves quantity * 4 for zero and positive values. Keep the harness unchanged: it checks the negative error type/message and both valid return values.',
'negative_quantity = -1\nzero_quantity = 0\npositive_quantity = 2\n',
'''def checked_cost(quantity):
    if quantity < 0:
        raise ValueError("quantity must be nonnegative")
    return quantity * 4

def unchecked_cost(quantity):
    return quantity * 4''',
'cost = None\n','cost = checked_cost\n',
'''# Instructor harness; do not edit.
try:
    cost(negative_quantity)
    negative_result = "no failure"
except ValueError as exc:
    negative_result = [type(exc).__name__, str(exc)]
zero_result = cost(zero_quantity)
positive_result = cost(positive_quantity)
''', ['[negative_result, zero_result, positive_result]'])

# The source/real traceback task already requires only assignments to observed evidence names.
# Its capture is top-level unchanged scaffolding.

select('debugger_usage','Inspect the supplied recorded pdb session. It pauses immediately after breakpoint(), before line 5; l lists the branch, p inspects quantity and quantity < 0, b 5 sets the branch breakpoint, n traces the wrong branch, and c resumes. Bind each command variable to the corresponding supplied command string. Then bind quantity_branch to the candidate whose comparison meets the intended behavior: positive quantities return "positive", all others "not positive". This browser task records the diagnosis from a supplied session, not interactive pdb input. Keep quantity and all supplied candidates unchanged.',
'quantity = 3\n',
'''list_cmd = "l"
value_cmd = "p quantity"
condition_cmd = "p quantity < 0"
branch_cmd = "b 5"
next_cmd = "n"
continue_cmd = "c"

def greater_branch(quantity):
    if quantity > 0:
        return "positive"
    else:
        return "not positive"

def lesser_branch(quantity):
    if quantity < 0:
        return "positive"
    else:
        return "not positive"''',
'source_command = None\nvalue_command = None\ncondition_command = None\nbreak_command = None\nnext_command = None\ncontinue_command = None\nquantity_branch = None\n',
'source_command = list_cmd\nvalue_command = value_cmd\ncondition_command = condition_cmd\nbreak_command = branch_cmd\nnext_command = next_cmd\ncontinue_command = continue_cmd\nquantity_branch = greater_branch\n',
'', ['[source_command, value_command, condition_command, break_command, next_command, continue_command, quantity_branch(quantity), quantity_branch(-quantity)]'])
prompt,st,so,tests=C['python.debugger_usage'];C['python.debugger_usage']=(prompt,dh+st,dh+so,tests)

select('safe_mutable_defaults','Inspect fresh_labels and shared_labels. Bind add_label to the implementation that uses a None default, allocates a new list only when labels is None, and preserves an explicitly supplied list. Keep the probes unchanged. first and second must be separate single-label lists; first must not accumulate the second label; explicit must be the same updated object as supplied.',
'first_label = "blue"\nsecond_label = "red"\n',
'''def fresh_labels(label, labels=None):
    if labels is None:
        labels = []
    labels.append(label)
    return labels

def shared_labels(label, labels=[]):
    labels.append(label)
    return labels''',
'add_label = None\n','add_label = fresh_labels\n',
'''# Instructor probes; do not edit.
first = add_label(first_label)
second = add_label(second_label)
supplied = []
explicit = add_label(first_label, supplied)
''', ['[first, second, first is second, explicit, explicit is supplied]'])

# Use registered rows to author top-level fixture variables: mutations can change both labels and quantities.
def records_fixture():
 rows=[list(r) for r in assets['ds.orders']['rows']]
 variant=next(v for v in assets['ds.orders']['variants'] if v['variant_id']=='case_labels')
 for op in variant['ops']:
  col=next(i for i,c in enumerate(assets['ds.orders']['columns']) if c['name']==op['column'])
  where=op['where'];matches=[r for r in rows if all(r[next(i for i,c in enumerate(assets['ds.orders']['columns']) if c['name']==k)]==v for k,v in where.items())]
  matches[op['occurrence']][col]=op['value']
 # First four candidates include changing labels and quantities.
 inputs='';parts=[]
 for i,r in enumerate(rows):
  inputs+=f'label_{i} = {r[0]!r}\nquantity_{i} = {r[1]!r}\n';parts.append('{"label": label_%d, "quantity": quantity_%d}'%(i,i))
 return inputs+'records = ['+', '.join(parts)+']\n'
inputs=records_fixture()
body='''def normalized_key(record):
    return record["label"].lower()

def raw_key(record):
    return record["label"]'''
common=inputs+supplied(body)
st=common+'label_key = None\nordered = None\n'
so=common+'label_key = normalized_key\nordered = sorted(records, key=label_key)\n'
code('sorting_with_key_functions','Inspect the supplied named key functions. Bind label_key to the function that returns the lowercase label, then assign ordered using sorted(records, key=label_key) in ascending order. Keep original text, quantities and records unchanged. Equal lowercase labels must retain input order. The checker reads ordered, records, and list identity.',st,so,['[ordered, records, ordered is records]'])

rows=assets['ds.orders']['rows'][:2]
inputs=''
for i,r in enumerate(rows):inputs+=f'label_{i} = {r[0]!r}\nquantity_{i} = {r[1]!r}\n'
common=inputs+'pairs = [(label_0, quantity_0), (label_1, quantity_1)]\nlabel_key = lambda pair: pair[0]\nquantity_key = lambda pair: pair[1]\n'
st=common+'chosen_key = None\nordered = None\n'
so=common+'chosen_key = quantity_key\nordered = sorted(pairs, key=chosen_key)\n'
code('lambda_expressions','Read the two supplied one-parameter, single-expression lambdas. Bind chosen_key to the lambda returning the quantity (the second item of each pair), then assign ordered using sorted(pairs, key=chosen_key) in ascending quantity order. Keep pairs unchanged. The checker reads ordered.',st,so,['ordered'])

select('specific_exception_handlers','Inspect the two supplied recovery implementations. Bind recover to the one ordering FileNotFoundError before OSError, without changing either recovery action. The supplied harness must print missing_notice exactly once rather than other_notice.',
'missing_notice = "File missing"\nother_notice = "Other file operation failure"\n',
'''def specific_first():
    try:
        raise FileNotFoundError("missing-example.txt")
    except FileNotFoundError:
        print(missing_notice)
    except OSError:
        print(other_notice)

def broad_first():
    try:
        raise FileNotFoundError("missing-example.txt")
    except OSError:
        print(other_notice)
    except FileNotFoundError:
        print(missing_notice)''',
'recover = None\n','recover = specific_first\n','recover()\n',[])
prompt,st,so,tests=C['python.specific_exception_handlers'];out=io.StringIO()
with contextlib.redirect_stdout(out):exec(so,{})
tests.append({'test_id':'t1','kind':'stdout_equals','spec':{'expected':out.getvalue().rstrip()},'visible':True,'message_on_fail':'Select the handler order that reaches the specific recovery action.'})

# Assignment-only diagnostic task: the supplied vocabulary stays unchanged; learner assigns its names.
prompt,st,so,tests=C['python.validation_vs_programming_errors']
vocab={'input_failure':'input failure','implementation_defect':'implementation defect','external_failure':'external operational failure','request_correction':'request corrected numeric text','code_correction':'correct the misspelled name','access_report':'report access failure'}
pre=''.join(name+' = '+repr(value)+'\n' for name,value in vocab.items())
# Keep causal inputs first for mutation sampling (only the first four top-level constants are mutated).
pos=st.index('# Supplied report 1:');st=st[:pos]+pre+st[pos:]
pos=so.index('# Supplied report 1:');so=so[:pos]+pre+so[pos:]
for name,value in vocab.items():
 # Replace only filled report assignments, not the vocabulary statements themselves.
 for target in ['input_category','input_response','implementation_category','implementation_response','access_category','access_response']:
  so=so.replace(target+' = '+repr(value),target+' = '+name)
C['python.validation_vs_programming_errors']=(prompt+' Use the supplied vocabulary variable names on the right side of your assignments instead of typing their text.',st,so,tests)

select('variadic_arguments_and_unpacking','Read the supplied forwarding implementations. Bind wrapper to the one collecting *args and **kwargs and returning target(*args, **kwargs), without adding a price binding. Preserve target. The checker calls wrapper(3, price=5), wrapper(3, 5), and wrapper(3), checking both supplied arguments and the target default.',
'',
'''def target(quantity, price=4):
    return quantity * price

def pass_through(*args, **kwargs):
    return target(*args, **kwargs)

def duplicate_price(*args, **kwargs):
    return target(*args, **kwargs, price=5)''',
'wrapper = None\n','wrapper = pass_through\n','',[],[('wrapper',[3],{'price':5}),('wrapper',[3,5],{}),('wrapper',[3],{})])
# Record the inspected controlling value too, so the diagnostic report depends on the supplied execution state.
prompt,st,so,tests=C['python.debugger_usage']
st+='\ninspected_quantity = None\n'
so+='\ninspected_quantity = quantity\n'
expr=tests[0]['spec']['expr'];expr=expr[:-1]+', inspected_quantity]'
code('debugger_usage',prompt+' Also assign inspected_quantity to the supplied controlling quantity; the checker includes that inspected value in the diagnostic report.',st,so,[expr])
