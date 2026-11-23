import json, re, ast, copy
from pathlib import Path
B=Path('batches/final_batch_learn_python.region.01')
P=json.loads((B/'tile_plans.json').read_text())
G={g['context']['concept_id']:g for g in json.loads((B/'inputs/path_glossary_bundle.json').read_text())['bundles']}
R=json.loads((B/'scenario_asset_registry.json').read_text())
A={a['asset_id']:a for a in R['assets']}
# Authored screen voice. Literal examples and fact identifiers are sourced below.
C={
'variables_assignment': {
'intro':'Name the notebook quantity, unit price and cost.',
'facts':[
'Assignment binds a name to the right-hand expression’s value; another assignment can rebind it.',
'Write name = value. A later right-hand expression uses a name’s current value.',
'Names are case-sensitive. ASCII names may contain letters, underscores and digits, but cannot begin with a digit or be a keyword.',
'Combine named numbers with +, -, * or / on the right, then assign the result.'
],
'example':'Read each notebook assignment from right to left: evaluate the expression, then bind its target. Changing quantity and recalculating cost are separate assignments. Use unit_price as a meaningful name; changing quantity to Quantity refers to a different name.',
'contrast':'Changing quantity does not keep the earlier cost expression running. Assign cost again to use the new quantity.',
'annotations':[('cost =','Evaluate the current quantity and unit_price, then bind cost.'),('quantity =','This binds quantity; it does not recalculate an earlier cost.')],
'recap':'Assignment uses current values; recalculation needs a new assignment.'},
'core_data_types': {
'intro':'Inspect notebook quantity, price, label and truth value.',
'facts':[
'An int represents an integer. A numeric literal with a decimal point or exponent produces a float.',
'In mixed int/float arithmetic, the int operand is converted to float.',
'Text has type str. Single or double quotes create string literals; + joins strings.',
'A bool represents truth with True or False.',
'Equality or ordering comparisons between numbers produce a boolean.',
'type(value) returns the type of that value.',
'print(value) displays the value’s string representation.'
],
'example':'Inspect quantity and price with type, then compare numeric multiplication with joining label text. Finally, reassign quantity to a bool and inspect its type again: inspect the current value, not the name’s spelling.',
'contrast':'A quoted number is text. Joining strings with + is not numeric addition; type(value) distinguishes the kinds of value.',
'annotations':[('print(type(quantity))','Inspect quantity’s current type, before and after reassignment.'),('print(label +','The operands are strings, so + joins their text.'),('print(quantity *','This calculation mixes an integer and a float.')],
'recap':'Distinguish int, float, str and bool before combining values.'},
'arithmetic_operators': {
'intro':'Choose the operation that answers the token-grouping question.',
'facts':[
'For numbers, + adds, - subtracts, * multiplies and / divides. Dividing ints produces a float.',
'// gives the floored quotient, % the remainder, and ** a power.',
'Parentheses group calculations. Exponentiation has higher precedence than multiplication, division and remainder; those have higher precedence than addition and subtraction.'
],
'example':'Compare ordinary division, the floored quotient and the remainder on the same token inputs. Then compare the grouped and ungrouped addition-and-multiplication expressions. Trace grouping before calculating.',
'contrast':'// is a floored quotient, not ordinary division displayed differently. Parentheses change grouping, not just appearance.',
'annotations':[('print(17','Compare division, floored quotient and remainder on identical inputs.'),('print((2','The parentheses group addition before multiplication.'),('print(2 +','Without parentheses, multiplication has higher precedence.')],
'recap':'Operators and parentheses determine the calculation.'},
'comparison_operators': {
'intro':'Choose whether a quantity threshold includes its boundary.',
'facts':[
'Use == to test equality and != to test inequality.',
'< and > test strict ordering. <= and >= also include equality.',
'Comparisons between supported scalar values produce True or False.'
],
'example':'Read each quantity comparison as a question. Equality is different from assignment; an inclusive threshold accepts the boundary while a strict threshold does not.',
'contrast':'At the boundary, >= includes equality but > does not. Use == for an equality test, not assignment’s =.',
'annotations':[('print(','Read the operator: strict or inclusive, equality or inequality?')],
'recap':'Strict and inclusive comparisons differ at equality.'},
'logical_operators': {
'intro':'Combine quantity and budget conditions.',
'facts':[
'For boolean conditions, and is true when both are true; or is true when at least one is true; not reverses the truth value.',
'and skips its second operand if the first is false. or skips its second operand if the first is true.',
'not has higher priority than and, and and higher priority than or. Parentheses make grouping explicit.'
],
'example':'Track quantity_ok and budget_ok separately before combining them. Mark whether a second operand is needed, then read any not and parentheses before evaluating the full rule.',
'contrast':'Do not assume both operands are evaluated: and can stop after a false first operand, while or can stop after a true one.',
'annotations':[('print(','Trace grouping and whether the second operand is evaluated.')],
'recap':'Combine boolean conditions and respect short-circuiting and grouping.'},
'type_conversion': {
'intro':'Convert numeric quantity text before using it in a calculation.',
'facts':[
'int(value) constructs an integer from suitable numeric text or a number. A float-to-int conversion truncates toward zero.',
'float(text) constructs a floating-point value from supported numeric text.',
'str(value) constructs a string representation.',
'Invalid numeric text can raise ValueError: the value is unsuitable for that conversion.',
'Assign the converted result to a name for later calculations. The original name changes only if it is the assignment target.'
],
'example':'Keep quantity_text separate from the converted quantity. The price conversion supplies a numeric value for multiplication. Compare suitable numeric text with an arbitrary word, and read float-to-int conversion as truncation toward zero.',
'contrast':'A conversion returns a value; it does not automatically rebind quantity_text. Truncating toward zero is not general rounding.',
'annotations':[('quantity =','The converted result is assigned to quantity, not quantity_text.'),('print(int(','Float-to-int conversion truncates toward zero.')],
'recap':'Store conversion results; distinguish truncation from rounding.'},
'conditional_statements': {
'intro':'Choose one order-size response by testing conditions in order.',
'facts':[
'Write if condition: with an indented body. Align any elif condition: headers and the optional else: header with if; indent their bodies.',
'Test conditions in order. Execute the first true condition’s body; execute else only if none is true.'
],
'example':'Read the size branches top to bottom. Stop at the first true condition; do not run another branch just because its test could also be true.',
'contrast':'An elif chain chooses the first true branch, not every true branch. else is the fallback only when all tests fail.',
'annotations':[('if quantity','Begin with the first condition.'),('elif quantity','Test this only if the earlier condition was false.'),('else:','Use this body only when no condition was true.')],
'recap':'An if/elif chain selects its first true branch.'},
'while_loops': {
'intro':'Keep asking for labels until the response reaches the stopping condition.',
'facts':[
'Write while condition: with an indented body. Test before each repetition; stop when the condition is false.',
'If the initial condition is false, the body never runs.',
'Update values used by the condition inside the body so the loop can reach its stopping condition.',
'input(prompt) displays a prompt and returns the entered line as text without its trailing newline. Assign another input result inside the loop to get a fresh response.'
],
'example':'The first input provides the response tested at entry. The input inside the body replaces it before the next test. A stopping response at the first prompt skips the body entirely.',
'contrast':'Testing before the body means zero repetitions are possible. Reusing the old response without updating it can keep the loop repeating.',
'annotations':[('while response','Test the response before entering or repeating the body.'),('    response =','Get a new text response before the next test.')],
'recap':'A while loop tests first and needs a reachable stopping state.'},
'lists': {
'intro':'Keep the color labels in order, then correct and extend them.',
'facts':[
'[item1, item2, ...] creates a list: an ordered collection that can change.',
'items[0] selects the first item. Negative indices count from the end.',
'items[start:stop] returns a new list from start up to, but excluding, stop.',
'items[index] = value replaces the item at that position.',
'items.append(value) adds a value at the list’s end.'
],
'example':'Track label positions through the replacement and append. Replacement changes an existing position; append extends the end. The slice selects a range into a new list, excluding its stop position.',
'contrast':'A slice’s stop is excluded. A slice returns a new list, unlike a single-index lookup; replacing an item is different from appending.',
'annotations':[('labels[1]','Replace the existing label at this position.'),('labels.append','Append at the end.'),('print(labels[1:3])','Include the start position and exclude the stop position.')],
'recap':'Lists support positional access, replacement, slicing and append.'},
'sets': {
'intro':'Collect distinct color labels rather than repeated occurrences.',
'facts':[
'A set is unordered and contains distinct elements. set(items) constructs it, removing repeated values.',
'{item1, item2, ...} makes a nonempty set. set() makes an empty set; {} makes a dictionary.',
'value in values tests membership in a set.',
'a | b is union: elements in either set. a & b is intersection: elements in both.'
],
'example':'Compare the label sets by membership, not display order. Repeated source labels contribute one distinct element. Union combines membership from either set; intersection keeps only shared members.',
'contrast':'set() is an empty set, whereas {} is a dictionary. Sets do not provide stable first and second sequence positions.',
'annotations':[('first =','Repeated source labels contribute one distinct element.'),('print(first |','Union includes members from either set.'),('print(first &','Intersection includes members shared by both sets.')],
'recap':'Sets represent distinct membership, not sequence positions.'},
'dictionaries': {
'intro':'Retrieve a quantity using its product label as the key.',
'facts':[
'{key: value, ...} creates a dictionary of key-value pairs with unique keys.',
'mapping[key] retrieves the associated value. If the key is absent, lookup raises an error.',
'mapping[key] = value adds a new pair or replaces the existing key’s value.'
],
'example':'Follow the notebook key through its replacement, then distinguish adding the pencil key from updating notebook. An eraser lookup would fail because that key has not been added.',
'contrast':'Updating notebook replaces its value; it does not create a duplicate key. An absent-key bracket lookup raises an error, not a fallback value.',
'annotations':[('quantities["notebook"] =','Replace the value associated with an existing key.'),('quantities["pencil"] =','Add a pair under a new key.')],
'recap':'Dictionary lookup and updates operate on unique keys.'},
'string_basics_formatting': {
'intro':'Build a readable notebook-cost message from text and values.',
'facts':[
'Strings represent text; single or double quotes delimit their literals.',
'Prefix a literal with f and put expressions inside braces to insert their values: f"{expression}".',
'A colon introduces a presentation specification. f"{value:.2f}" displays fixed-point form with two digits after the decimal point.'
],
'example':'Separate the f prefix, literal text, braced expression and colon-led format specification. The expression supplies a value; .2f controls how that value appears in the message.',
'contrast':'Two decimal digits describe the formatted text. Formatting does not change the underlying numeric calculation.',
'annotations':[('message =','f enables insertion; braces hold the expression; :.2f sets fixed-point presentation.')],
'recap':'F-strings insert expression values; format specifications control presentation.'},
'defining_calling_functions': {
'intro':'Name the greeting action, then choose when to call it.',
'facts':[
'Define a function with def name(): and an indented body.',
'The definition binds its name to a function. name() calls the function and executes its body.'
],
'example':'The greeting definition makes the function available. Each call outside the indented body asks that body to execute; the definition itself is not a call.',
'contrast':'def greet(): binds the function name; greet() invokes the body. Defining and calling are different actions.',
'annotations':[('def greet','Define and bind the function name.'),('    print','This indented body executes when the function is called.'),('greet()','A call outside the body invokes the function.')],
'recap':'A definition binds a function; a call executes its body.'},
'parameters_arguments': {
'intro':'Reuse describe with different notebook and pen call values.',
'facts':[
'Parameters are names in a function definition. Arguments are values supplied at a call.',
'Define def name(parameter): with an indented body using parameter; call name(argument) to supply a value.',
'Positional arguments bind to the corresponding parameters in order.'
],
'example':'In describe, label and quantity are parameter names. For each call, connect the first argument to label and the second to quantity before reading the body.',
'contrast':'label is a parameter name, not one particular product label. Each call supplies arguments that bind in positional order.',
'annotations':[('def describe','label and quantity are parameters.'),('describe(','The first argument binds label; the second binds quantity.')],
'recap':'Parameters name inputs; call arguments supply their values.'},
'return_values': {
'intro':'Give the caller an order cost it can use again.',
'facts':[
'return expression ends the current call and supplies the expression’s value to the caller.',
'result = function(arguments) stores the returned value.',
'Reaching the function’s end without return, or using return with no expression, returns None.',
'print displays values; it does not supply the function’s calculated return result.'
],
'example':'Trace the product through return into cost, then into the caller’s addition. Contrast that with a helper that only prints the product: displaying it does not return it.',
'contrast':'A display-only helper reaches its end and returns None. A missing return does not return the last calculation.',
'annotations':[('    return','End this call and supply the product to the caller.'),('cost =','Store the returned value in cost.'),('print(cost','The caller can reuse the stored result.')],
'recap':'Return supplies a reusable result; print only displays.'},
 'tuples': {
'intro':'Return the smallest and largest quantities together as an ordered pair.',
'facts':[
'A tuple is an ordered group whose individual items cannot be reassigned.',
'Comma-separated values form a tuple; (value,) forms a one-item tuple.',
'first, second = pair unpacks a pair. Target and value counts must match.',
'return first, second returns a tuple of the two expression values.',
'For a nonempty collection, min(values) obtains the smallest item and max(values) the largest.'
],
'example':'Trace the first returned expression into smallest and the second into largest. Both targets match the pair’s two values. The separate one-item tuple needs its comma.',
'contrast':'Tuple items cannot be replaced like list items. Unpacking requires matching counts, and a one-item tuple requires the comma.',
'annotations':[('    return','The first expression supplies the lower bound; the second the upper bound.'),('smallest, largest','Unpack the returned pair into the corresponding two names.'),('one_item','The comma forms a one-item tuple.')],
'recap':'Tuples carry ordered values; unpacking requires matching counts.'},
'function_default_keyword_args': {
'intro':'Use the ordinary order fee unless a call overrides it.',
'facts':[
'In def name(required, optional=default):, omitting optional at a call uses its default.',
'Positional arguments bind in order; keyword arguments bind by parameter name. Keywords follow ordinary positional arguments.',
'Supply required arguments. Do not bind a parameter twice or use an unaccepted keyword.'
],
'example':'Identify quantity and price as required parameters and fee as defaulted. Compare omitting fee, naming all arguments, and using keywords after positional arguments. A named fee overrides the default.',
'contrast':'A keyword does not permit a duplicate binding. Supply required parameters once each, and only use accepted keyword names.',
'annotations':[('def cost','quantity and price are required; fee has a default.'),('print(cost','Match arguments by position or parameter name; omitted fee uses the default.')],
'recap':'Defaults fill omissions; keywords bind accepted parameter names.'},
'variable_scope': {
'intro':'Distinguish the module quantity from a helper’s local quantity.',
'facts':[
'Assigned function names are local throughout that function unless declared otherwise. Reading a local before binding it raises UnboundLocalError.',
'Without a local binding, ordinary lookup can read an enclosing or module binding.',
'globals() returns the current module namespace dictionary. globals()["name"] explicitly reads that entry even when a local shadows it.',
'Ordinary local assignment changes the local binding, not a same-named module binding.',
'A global declaration directs assignments to that name’s module binding instead.'
],
'example':'In show, ordinary quantity reads its local binding, while globals()["quantity"] reads the module entry. After the call, the module quantity still refers to its module binding.',
'contrast':'A module quantity cannot rescue a read of an unbound local quantity. Assignment makes that name local throughout the function unless declared otherwise.',
'annotations':[('quantity =','The unindented assignment binds the module name.'),('    quantity =','This assignment binds a separate local quantity.'),('    print(globals','Explicit lookup selects the module namespace entry.')],
'recap':'Local assignment and explicit module lookup refer to different bindings.'},
'error_handling': {
'intro':'Give unsuitable quantity text a defined recovery path.',
'facts':[
'Put the operation in an indented try: body; align except ExceptionType: with try and indent the recovery body.',
'A matching exception skips the rest of try and runs the handler. With no exception, the handler is skipped.',
'An unmatched exception passes to an outer handler, or stops execution if no handler is found.',
'except ValueError: handles an invalid numeric conversion from entered text.'
],
'example':'Read the conversion before the multiplication. Invalid numeric text reaches the matching ValueError handler and skips the remaining try operations. Suitable numeric text takes the success path and skips that handler.',
'contrast':'Handling the failure does not make conversion succeed. The multiplication remaining in try is skipped after the conversion raises.',
'annotations':[('try:','Begin the protected body.'),('    quantity =','A conversion failure transfers control to a matching handler.'),('    print(quantity','This operation is skipped if the preceding conversion raises.'),('except ValueError','The aligned handler matches invalid numeric conversion.')],
'recap':'Matching failures enter the handler and skip the rest of try.'},
'import_statements': {
'intro':'Choose the name that gives access to the math operation.',
'facts':[
'import module binds the module name. Access functionality with module.member.',
'from module import member binds that member directly in the importing namespace.',
'After import math, math.cos(value) accesses a math function.'
],
'example':'Connect import math to math.cos, and from math import cos to the bare cos name. Both call forms access the same member; their name bindings differ.',
'contrast':'import math does not bind every member as a bare name. Use math.cos, or explicitly import cos before using that name.',
'annotations':[('import math','Bind the module name; the following call uses math.cos.'),('from math import','Bind cos directly; the following call uses cos without the module prefix.')],
'recap':'Import form determines whether a call uses a module prefix.'},
'pep8_style': {
'intro':'Reformat the order helper without changing operations.',
'facts':[
'Use four spaces per block indentation level.',
'Use lowercase function and variable names; add underscores between words when that improves readability.',
'Avoid extra spaces inside parentheses, brackets or braces, before commas or colons, or between a function name and its call parentheses.',
'Put one space beside assignment and comparison operators; group arithmetic spacing to reflect priority.',
'PEP 8 recommends code lines of at most 79 characters, and comments or docstrings flowed to 72.'
],
'example':'Compare the same helper before and after reformatting. Notice lowercase underscore-separated names, four-space indentation and punctuation spacing. Keep the recommended line limits in view as the helper grows.',
'contrast':'Recommended line lengths are not a rule that longer lines are invalid syntax. Keep style recommendations distinct from block indentation.',
'annotations':[('def order_cost','Use lowercase words separated with underscores.'),('    cost =','Four-space indentation; spaced assignment and arithmetic.'),('print(order_cost','No extra punctuation spacing.')],
'recap':'Use readable names and spacing; distinguish recommendations from syntax.'},
'for_loops': {
'intro':'Visit the quantities while carrying a running total.',
'facts':[
'Write for item in sequence: with an indented body. Process successive sequence items in their order.',
'Initialize total = 0 before the loop. Inside, use total = total + item to accumulate numeric items.'
],
'example':'Initialize once, then reuse the current total on the right of each update. Each quantity is the next sequence item, so the accumulator carries earlier additions forward.',
'contrast':'Initializing total inside the loop discards the earlier accumulated value. Prepare it once outside, then update it inside.',
'annotations':[('total = 0','Initialize once before the loop.'),('for quantity','Bind the next sequence item.'),('    total =','Reuse the previous total, then assign the updated result.')],
'recap':'Initialize an accumulator once, then update it for each item.'},
'loop_control': {
'intro':'Choose whether a quantity means skip or stop.',
'facts':[
'break exits the innermost enclosing for or while loop.',
'continue skips the rest of the current body and proceeds to the next iteration.',
'Put break or continue inside a loop conditional so it applies only when its condition holds.'
],
'example':'Trace each quantity through the stop and skip conditions before adding it. The stop marker exits the loop; the skip value bypasses addition but permits another iteration.',
'contrast':'continue skips this iteration’s remaining work; break exits the innermost loop. They are not interchangeable.',
'annotations':[('        break','Exit this loop; later quantities are not processed.'),('        continue','Skip addition for this item, then proceed to the next iteration.'),('    total =','Add only when neither control condition applies.')],
'recap':'continue skips remaining work; break exits the innermost loop.'},
'iterating_collections': {
'intro':'Decide whether the order loop needs keys or key-value pairs.',
'facts':[
'Use for item in collection: with an indented body to visit successive elements.',
'Lists and tuples are ordered sequences.',
'Sets are unordered; their traversal is not positional sequence traversal.',
'Direct dictionary iteration visits keys.',
'for key, value in mapping.items(): visits each dictionary key-value pair together.'
],
'example':'In direct quantities traversal, label binds a key. In quantities.items() traversal, label and quantity bind the key and associated value together. Read the collection type before assuming what an item means.',
'contrast':'Direct dictionary iteration does not yield values or key-value pairs. Use quantities.items() when both the label and its quantity are needed.',
'annotations':[('for label in quantities:','Direct traversal binds label to each key.'),('for label, quantity','items() binds the key and associated value together.')],
'recap':'Dictionary iteration visits keys; items() visits key-value pairs.'},
'comprehensions': {
'intro':'Build new collections from accepted source quantities.',
'facts':[
'[expression for item in iterable if condition] builds a new list by evaluating expression for accepted items. The condition is optional.',
'{key_expression: value_expression for item in iterable} builds a dictionary of computed keys and values. An if clause can filter the source items.'
],
'example':'Read each comprehension as source, optional filter and computed result. In the dictionary form, the colon separates key and value expressions. Items failing the filter contribute nothing.',
'contrast':'The condition selects source items; it is not a result value. The result expression computes what each accepted item contributes.',
'annotations':[('doubled =','Source follows in; if selects; the leading expression computes each list item.'),('by_quantity =','The expressions before and after the colon compute keys and values.')],
'recap':'Comprehensions separate source, optional filtering and computed results.'},
'file_io': {
'intro':'Read saved notebook orders with managed file opening.',
'facts':[
'open(path, mode) returns a file object. r reads; w writes and replaces existing contents.',
'with open(path, mode) as f: uses an indented body and closes f after use.',
'f.read() reads remaining contents. f.write(text) writes text through a text-mode file object.',
'Without managed opening, call f.close() when finished.',
'Open CSV input with newline="" for the reader.',
'By default, csv.DictReader(f) uses the first row as dictionary keys, not a result row. list(csv.DictReader(f)) collects the row dictionaries.'
],
'example':'In orders.csv, the header supplies label and quantity keys. DictReader returns CSV field text, including numeric-looking quantity text. The managed body collects rows; the file is closed afterward. For text, read remaining contents or write text through the file object.',
'contrast':'w replaces existing contents; it is not a reading mode. The CSV header supplies keys by default, rather than appearing as a returned data row.',
'annotations':[('with open','Read the CSV with newline handling and managed closure.'),('    rows =','Collect data-row dictionaries using the header keys.'),('print(rows)','Outside the managed body, the file is closed.')],
'recap':'Choose file modes carefully; manage closure and CSV header handling.'}
}

def qual(c, ids): return [c+'#'+i for i in ids]
def lin(c, tbs=(), facts=(), anchors=()):
    return {'concept_ids':[c], 'teaching_block_ids':qual(c,tbs), 'fact_ids':qual(c,facts), **({'anchors':qual(c,anchors)} if anchors else {})}
def prose(text,c,tbs,facts,role): return {'type':'prose','text':text,'role':role,'lineage':lin(c,tbs,facts)}
def cfg(c): return C[c.split('.',1)[1]]
def tb(c, tid): return next(t for t in G[c]['teaching_blocks'] if t['id']==tid)
def fact_voice(c):
    ids=[f['id'] for f in G[c]['coverage']['required_facts']]
    return dict(zip(ids,cfg(c)['facts'],strict=True))
def example_code(c):
    return '\n\n'.join(re.findall(r'```python\s*\n(.*?)```', tb(c,'tb4')['content'],re.S)).rstrip()

def code_block(c,code,visual=False, annotations=True):
    lines=code.splitlines(); anns=[]
    if annotations:
        for match,text in cfg(c)['annotations']:
            # Match indentation exactly where the cue includes it.
            for n,line in enumerate(lines,1):
                if line.startswith(match): anns.append({'start_line':n,'end_line':n,'text':text})
    return {'type':'code_walkthrough','language':'python','code':code,'annotations':anns,'reveal':'line_by_line','lineage':lin(c,['tb4'],tb(c,'tb4')['fact_ids'],['visual'] if visual else [])}

def visual(c):
    code=example_code(c)
    if c=='python.variables_assignment':
        # Show all three cost inspection points; outputs belong to the execution stage.
        out=[]; cost_seen=False
        for line in code.splitlines():
            out.append(line)
            if line.startswith('cost ='): cost_seen=True; out.append('print(cost)')
            elif cost_seen and line.startswith('quantity ='): out.append('print(cost)')
        code='\n'.join(out)
    elif c=='python.core_data_types':
        bool_literal=re.search(r'\bTrue\b',G[c]['coverage']['required_facts'][3]['statement']).group()
        code+='\nquantity = '+bool_literal+'\nprint(type(quantity))'
    elif c=='python.string_basics_formatting':
        # The visual anchor requests this expression rather than tb4's other message.
        expr=re.search(r'(message = f".*?")',G[c]['visual_anchor']['purpose']).group(1)
        tree=ast.parse(code)
        code='\n'.join(ast.unparse(n) for n in tree.body if isinstance(n,ast.Assign) and not any(isinstance(t,ast.Name) and t.id=='message' for t in n.targets))+'\n'+expr+'\nprint(message)'
    elif c=='python.function_default_keyword_args':
        tree=ast.parse(code); func=tree.body[0]; names=[a.arg for a in func.args.args]
        first=tree.body[1].value.args[0]
        allkw=ast.Call(func=copy.deepcopy(first.func),args=[],keywords=[ast.keyword(arg=n,value=copy.deepcopy(v)) for n,v in zip(names,first.args)])
        code+='\nprint('+ast.unparse(allkw)+')'
    elif c=='python.pep8_style':
        # Same fixture values; the before version is only a style mutation.
        bad=code.replace('order_cost','OrderCost').replace('unit_price','UnitPrice').replace('quantity','Quantity').replace('cost','Cost')
        bad=bad.replace('    ','  ').replace(' = ','=').replace(' * ','*').replace(', ', ' , ').replace('):', ' ) :').replace('(', '( ')
        return [{'type':'before_after','before':code_block(c,bad,True,False),'after':code_block(c,code,True),
                 'change_summary':'Same calculation; clearer names, indentation and spacing.','lineage':lin(c,['tb2','tb3','tb4'],[f['id'] for f in G[c]['coverage']['required_facts']],['visual'])}]
    blocks=[]
    if c=='python.file_io':
        blocks.append({'type':'data_table','asset_ref':{'asset_id':A['ds.orders']['asset_id'],'columns':[col['name'] for col in A['ds.orders']['columns']]},'lineage':lin(c,['tb4'],['f5','f6'],['visual'])})
    blocks.append(code_block(c,code,True))
    if c=='python.return_values':
        tree=ast.parse(code)
        fn=tree.body[0]
        for i,n in enumerate(fn.body):
            if isinstance(n,ast.Return): fn.body[i]=ast.Expr(value=ast.Call(func=ast.Name(id='print',ctx=ast.Load()),args=[n.value],keywords=[]))
        # Display-only contrast stores and inspects the call result without trying arithmetic on it.
        code2=ast.unparse(fn)+'\n'+ast.unparse(tree.body[1])+'\nprint(cost)'
        blocks.append(code_block(c,code2,True,False))
    return blocks

def factual_blocks(c,tid):
    voice=fact_voice(c)
    return [prose(voice[f],c,[tid],[f],tb(c,tid)['purpose']) for f in tb(c,tid)['fact_ids']]

def targeted_contrast(c,facts):
    short=c.split('.',1)[1]; fs=set(facts)
    options={
        'variables_assignment': [('f2','Changing quantity does not recalculate cost. Assign cost again to use quantity’s current value.')],
        'core_data_types': [('f3','Quoted numeric text is a string; joining text is different from adding numbers.'),('f5','A numeric comparison produces a bool, not a text label.'),('f6','Inspect the current value with type; the variable name alone does not tell you its type.')],
        'arithmetic_operators': [('f1','Ordinary division of integer inputs produces a float; it is not the floored quotient.'),('f2','The floored quotient counts complete groups; the remainder answers what is left over.')],
        'comparison_operators': [('f2','An inclusive threshold includes equality at the boundary; a strict threshold excludes it.'),('f3','Read a comparison as a question with a boolean result, not an assignment of its right-hand value.')],
        'logical_operators': [('f1','and requires both boolean conditions; or accepts at least one.'),('f2','and can skip after a false first operand; or can skip after a true one.')],
        'type_conversion': [('f1','Float-to-int conversion truncates toward zero; it is not general rounding.'),('f5','Assigning a conversion to quantity does not rebind quantity_text.'),('f4','Suitable numeric text and an arbitrary word are different conversion inputs; an invalid input can raise ValueError.')],
        'conditional_statements': [('f2','The first true branch runs; the chain does not run every branch whose condition could be true.')],
        'while_loops': [('f1','The test comes before the body, so the loop need not run once.')],
        'lists': [('f3','A slice excludes its stop position and returns a new list; it is not a single-index lookup.'),('f4','Replacement changes an existing position; append adds at the end.')],
        'sets': [('f2','set() creates an empty set; empty braces create a dictionary.'),('f4','Union includes labels in either set; intersection requires membership in both.')],
        'dictionaries': [('f2','An absent-key lookup raises an error rather than providing a fallback value.'),('f3','Updating notebook replaces its value; adding pencil creates a new key-value pair.')],
        'string_basics_formatting': [('f2','Braced expressions insert their values; the surrounding literal text supplies the message wording.'),('f3','Fixed-point formatting changes presentation, not the numeric calculation.')],
        'defining_calling_functions': [('f2','The definition binds greet; the later greet() calls execute its body.')],
        'parameters_arguments': [('f1','label is a parameter name in describe; a product label supplied at a call is an argument.')],
        'return_values': [('f4','Printing the product displays it; returning the product supplies it to the caller.'),('f3','A display-only helper reaches its end and returns None, not the displayed product.')],
        'tuples': [('f2','A one-item tuple needs its comma, not just parentheses.'),('f3','A pair requires two unpacking targets, not three.'),('f4','Returning two expressions supplies one tuple to the caller, whose two values can then be unpacked.')],
        'function_default_keyword_args': [('f3','Naming an argument does not allow binding that same parameter twice.'),('f1','Omitting fee uses its default; explicitly supplying fee overrides that default.')],
        'variable_scope': [('f3','Ordinary quantity can refer to a local; globals()["quantity"] explicitly reads the module entry.'),('f4','An ordinary local assignment leaves the module binding alone; a global declaration redirects assignment to the module.'),('f1','A module quantity does not rescue a read of a quantity classified as local but not yet bound.')],
        'error_handling': [('f4','The ValueError handler matches invalid numeric conversion; it is not a handler for every exception type.'),('f2','A failed conversion skips the remaining try work; a successful conversion skips the handler.')],
        'import_statements': [('f2','import math binds math; from math import cos binds cos directly.')],
        'pep8_style': [('f5','Recommended line lengths do not mean every longer line is invalid syntax.'),('f3','Keep spaces around operators, not extra spaces inside call punctuation.')],
        'for_loops': [('f2','Initializing total in the body would discard earlier additions; initialize once before the loop.'),('f1','The body processes each successive sequence item, not the entire sequence as one item.')],
        'loop_control': [('f1','break exits the innermost loop; continue only skips the current body’s remaining work.')],
        'iterating_collections': [('f3','Lists and tuples have sequence order; set traversal is not positional.'),('f4','Direct dictionary traversal visits keys, not associated values.'),('f5','Use items() to bind each label and quantity together; direct traversal binds only keys.')],
        'comprehensions': [('f1','The condition selects quantities; the result expression computes list items. The condition is not itself the result.'),('f3','The colon separates computed keys from computed values; the optional condition only filters source items.')],
        'file_io': [('f1','Reading uses r; w replaces existing contents rather than inspecting them.'),('f6','The CSV header supplies keys by default; it is not returned as a data-row dictionary.')]
    }
    for f,text in options[short]:
        if f in fs:
            return text,[f]
    return cfg(c)['contrast'],tb(c,'tb5')['fact_ids']

out={'schema_version':P['schema_version'],'kind':'screens_part','path_id':P['path_id'],'batch_id':P['batch_id'],'tiles':[]}
for idx,t in enumerate(P['tiles']):
    names=[G[c]['context']['concept_name'] for c in t['concept_ids']]
    tile={'tile_id':t['tile_id'],'title':' / '.join(names),'steps':[],'remediation_steps':[]}
    for s in t['steps']:
        c=s['concept_ids'][0]; q=cfg(c)
        st={'step_id':s['step_id'],'type':s['type'],'concept_ids':s['concept_ids'],
            'title':G[c]['context']['concept_name'],
            'lineage':{'teaching_block_ids':s['teaching_block_ids'],'fact_ids':s['fact_ids'],'segment_ids':s['segment_ids'],'anchors':s['anchors']}}
        if s['type']=='explainer':
            blocks=[]
            for tidq in s['teaching_block_ids']:
                cid,tid=tidq.split('#'); qc=cfg(cid)
                if tid=='tb1': blocks.append(prose(qc['intro'],cid,[tid],[],'intro'))
                elif tid in ('tb2','tb3'): blocks.extend(factual_blocks(cid,tid))
                elif tid=='tb4': blocks.append(prose(qc['example'],cid,[tid],tb(cid,tid)['fact_ids'],'example'))
                elif tid=='tb5': blocks.append(prose(qc['contrast'],cid,[tid],tb(cid,tid)['fact_ids'],'misconception'))
            if s['planned_visual_block_type']: blocks.extend(visual(c))
            st['blocks']=blocks
        elif s['type']=='video':
            st['title']='Explore '+G[c]['context']['concept_name'].lower()
            st['blocks']=[{'type':'media_group','segment_ids':s['segment_ids']}]
        elif s['type'] in ('check','hands_on'):
            st['eyebrow']='Quick check' if s['type']=='check' else 'Practice'
            if s['type']=='hands_on' and s['planned_interaction_type'] in ('choice','classify'):
                st['title']='Review '+G[c]['context']['concept_name'].lower()
                st['lede']='Read the supplied excerpts in this step and judge which follow the rule.'
            elif s['type']=='hands_on':
                st['title']='Practice '+G[c]['context']['concept_name'].lower()
                st['lede']='Apply the rule to the supplied notebook-desk example.'
            else:
                st['title']='Check '+G[c]['context']['concept_name'].lower()
                st['lede']='Read the example and decide which interpretation follows the rule.'
        elif s['type']=='recap':
            st['title']='Takeaways'
            st['blocks']=[prose(cfg(cid)['recap'],cid,['tb2','tb3'],[f['id'] for f in G[cid]['coverage']['required_facts']],'takeaway') for cid in s['concept_ids']]
            if idx+1<len(P['tiles']):
                nc=P['tiles'][idx+1]['concept_ids'][0]
                nextname=G[nc]['context']['concept_name']
                nexttext=cfg(nc)['intro']
            else:
                nextname='Collection selection'
                nexttext='Next, choose a collection for a task.'
            st['blocks'].append({'type':'up_next','title':nextname,'text':nexttext})
        tile['steps'].append(st)
    # A distinct fact-set route for every concept check/practice demand.
    seen=set()
    for s in t['steps']:
        if s['type'] not in ('check','hands_on'): continue
        for c in s['concept_ids']:
            facts=[f.split('#')[1] for f in s['fact_ids'] if f.startswith(c+'#')]
            if not facts:
                facts=list(dict.fromkeys(f for a in G[c]['assessment_anchors'] for f in a['fact_ids']))
            key=(c,tuple(sorted(facts)))
            if key in seen: continue
            seen.add(key)
            tids=[x['id'] for x in G[c]['teaching_blocks'] if set(facts)&set(x['fact_ids'])]
            rid=t['tile_id']+'.r'+str(len(tile['remediation_steps'])+1).zfill(2)
            blocks=[]
            voice=fact_voice(c)
            for f in facts:
                ftids=[tid for tid in tids if f in tb(c,tid)['fact_ids']]
                blocks.append(prose(voice[f],c,ftids,[f],'definition'))
            contrast,cf=targeted_contrast(c,facts)
            ct=[tid for tid in tids if set(cf)&set(tb(c,tid)['fact_ids'])]
            blocks.append(prose(contrast,c,ct,cf,'misconception'))
            # Same authored fixture as the teaching screen; no inline results.
            blocks.append(code_block(c,example_code(c),False,False))
            tile['remediation_steps'].append({'step_id':rid,'type':'remediation','required':False,'concept_ids':[c],
                'eyebrow':'Try the contrast','title':'Revisit '+G[c]['context']['concept_name'].lower(),
                'blocks':blocks,'lineage':lin(c,tids,facts)})
    out['tiles'].append(tile)
(B/'screens.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Wrote',len(out['tiles']),'tiles;',sum(len(t['steps']) for t in out['tiles']),'planned steps;',sum(len(t['remediation_steps']) for t in out['tiles']),'remediation steps')
# Word-budget checklist excludes executable code and framing-only planned steps.
for t,p in zip(out['tiles'],P['tiles'],strict=True):
    for s,ps in zip(t['steps'],p['steps'],strict=True):
        def words(b):
            if b['type']=='prose': return len(b['text'].split())
            if b['type']=='up_next':return len((b['title']+' '+b.get('text','')).split())
            if b['type']=='code_walkthrough':return sum(len(x['text'].split()) for x in b.get('annotations',[]))
            if b['type']=='before_after':return len(b['change_summary'].split())+words(b['before'])+words(b['after'])
            return 0
        n=sum(words(b) for b in s.get('blocks',[]))
        if ps['word_budget'] and n>ps['word_budget']:print('OVER BUDGET',s['step_id'],n,ps['word_budget'])
