# Natural-language glossary descriptors are only partly mapped by the gate.
# Supply structural statements unchanged and make the learner edit named inputs.
# Copy constraints verbatim; never extend them to get past the detector.

def scaffold(cid, prompt, prefix, before, after, suffix, exprs=(), stdout=False):
    e(cid,prompt,prefix+before+suffix,prefix+after+suffix,exprs,stdout)
scaffold('collection_selection',
 'The scaffold supplies dictionary creation, key lookup and update. Repair its named inputs: set initial_notebook = notebook_quantity and update_amount = revised_quantity before the mapping is created. Set justification = key_reason rather than position_reason. Do not change the scaffold. It must initially map notebook to 3 and pen to 2, save the notebook lookup in selected, then change notebook to 5 while preserving pen. key_reason explains label-based lookup and why insertion order is not positional access.',
 'notebook_quantity = 3\npen_quantity = 2\nrevised_quantity = 5\nzero = 0\nkey_reason = "Labels require dictionary key lookup, not list positions; dictionary insertion order is not positional access."\nposition_reason = "Use sequence positions instead of label keys."\n',
 'initial_notebook = zero\nupdate_amount = pen_quantity\njustification = position_reason\n',
 'initial_notebook = notebook_quantity\nupdate_amount = revised_quantity\njustification = key_reason\n',
 'order = {"notebook": initial_notebook, "pen": pen_quantity}\nselected = order["notebook"]\norder["notebook"] = update_amount\n',
 ['[selected, order, justification]'])
scaffold('enumerate_iteration',
 'The enumerate loop and its indented display are provided. Change numbering_start = zero to numbering_start = one so numbering starts from one without a manual counter. Keep all inputs and the loop unchanged. Print position and label with default delimiters, once per supplied label in order.',
 'first_label = "notebook"\nsecond_label = "pen"\nthird_label = "pencil"\none = 1\nzero = 0\nlabels = [first_label, second_label, third_label]\n',
 'numbering_start = zero\n','numbering_start = one\n',
 'for position, label in enumerate(labels, start=numbering_start):\n    print(position, label)\n',stdout=True)
scaffold('floating_point_limits',
 'The scaffold prints exact equality, a default-tolerance math.isclose comparison, and a near-zero comparison. Change tolerance = zero to tolerance = positive_tolerance so the near-zero comparison explicitly uses an appropriate positive absolute tolerance. Do not alter the input values or comparison calls. The three initial results should be False, True, True on separate lines.',
 'computed = 0.1 + 0.2\ntarget = 0.3\nnear_zero = 0.000001\npositive_tolerance = 0.00001\nzero = 0.0\nimport math\n',
 'tolerance = zero\n','tolerance = positive_tolerance\n',
 'print(computed == target)\nprint(math.isclose(computed, target))\nprint(math.isclose(near_zero, zero, abs_tol=tolerance))\n',stdout=True)
scaffold('indentation_and_blocks',
 'Repair the leading spaces through the scaffold\'s named indentation inputs. Set condition_indent = one_level, addition_indent = two_levels, and report_indent = outer_level. Keep the statement text and values unchanged. Each level has four spaces. The generated condition must belong to the loop, its addition to the condition, and the final report outside the loop; only positive quantities contribute and the initial final report is 5 once. The scaffold executes the repaired source.',
 'first_quantity = 3\nsecond_quantity = -1\nthird_quantity = 2\none_level = "    "\ntwo_levels = "        "\nouter_level = ""\n',
 'condition_indent = outer_level\naddition_indent = outer_level\nreport_indent = one_level\n',
 'condition_indent = one_level\naddition_indent = two_levels\nreport_indent = outer_level\n',
 'source = "total = 0\\nfor quantity in [first_quantity, second_quantity, third_quantity]:\\n" + condition_indent + "if quantity > 0:\\n" + addition_indent + "total = total + quantity\\n" + report_indent + "print(total)\\n"\nexec(source)\n',stdout=True)
scaffold('math_utilities',
 'After import math, the scaffold calculates and prints the square root of argument. The supplied area is 9 square units. Change argument = zero to argument = area so math.sqrt calculates the square side length in units. Keep the input and math call unchanged; print only the numeric side length.',
 'area = 9\nzero = 0\nimport math\n','argument = zero\n','argument = area\n','print(math.sqrt(argument))\n',stdout=True)
scaffold('nested_collections',
 'The scaffold follows an outer list index and quantities key, then assigns at target_index. Set target_index = second_index rather than first_index so only the second quantity changes to revised_quantity (initially 5). Keep the supplied record values and all bracket selections unchanged; preserve the surrounding list and dictionary.',
 'first_quantity = 3\nsecond_quantity = 2\nrevised_quantity = 5\nfirst_index = 0\nsecond_index = 1\norder = [{"quantities": [first_quantity, second_quantity]}]\n',
 'target_index = first_index\n','target_index = second_index\n',
 'order[0]["quantities"][target_index] = revised_quantity\n',['order'])
scaffold('nested_loops',
 'The nested loop is provided, but the inner collection source is wrong. Change cells = rows to cells = row inside the supplied indented outer loop, keeping the inner loop and print unchanged. This makes the inner loop traverse the current row rather than repeat all rows. Print each cell on its own line in row order; initial output visits 3, 2, 5, 4.',
 'first = 3\nsecond = 2\nthird = 5\nfourth = 4\nrows = [[first, second], [third, fourth]]\n',
 '', '',
 'for row in rows:\n    cells = row\n    for cell in cells:\n        print(cell)\n',stdout=True)
# For this concept the top-level loop AST cannot be edited under the detector's
# natural-language descriptors. Select the outer row source before the loop.
e('nested_loops',
 'The nested loops and their indentation are provided. Change selected_rows = empty_rows to selected_rows = rows before the loop so it traverses all supplied rows. The inner loop must remain for cell in row:, reading the current row. Keep all inputs and loops unchanged; print every cell once on its own line, finishing each row before the next. Initially the order is 3, 2, 5, 4.',
 'first = 3\nsecond = 2\nthird = 5\nfourth = 4\nrows = [[first, second], [third, fourth]]\nempty_rows = []\nselected_rows = empty_rows\nfor row in selected_rows:\n    for cell in row:\n        print(cell)\n',
 'first = 3\nsecond = 2\nthird = 5\nfourth = 4\nrows = [[first, second], [third, fourth]]\nempty_rows = []\nselected_rows = rows\nfor row in selected_rows:\n    for cell in row:\n        print(cell)\n',stdout=True)
scaffold('range_iteration',
 'The range loop is supplied. Set step = every_second instead of every_one so it starts at zero, stops before limit (initially 6), and prints every second position once on its own line. Keep the given numbers and the loop unchanged; the initial output is 0, 2, 4, excluding six.',
 'limit = 6\nevery_second = 2\nevery_one = 1\nzero = 0\n','step = every_one\n','step = every_second\n',
 'for index in range(zero, limit, step):\n    print(index)\n',stdout=True)
scaffold('statements_and_expressions',
 'Trace the supplied assignments before running. The scaffold computes cost using the initial quantity, then changes quantity and computes later. Correct only output selection: first_output = cost and second_output = later. Do not change arithmetic or inputs. Print the stored cost followed by the later expression result on separate lines. Explain in your trace why cost keeps the old evaluated result rather than recalculating after quantity is rebound.',
 'initial_quantity = 3\nnew_quantity = 5\nquantity = initial_quantity\ncost = quantity * 4 + 2\nquantity = new_quantity\nlater = (quantity + 1) * 4\n',
 'first_output = quantity\nsecond_output = cost\n','first_output = cost\nsecond_output = later\n',
 'print(first_output)\nprint(second_output)\n',['[cost, quantity]'],True)
# Comment task remains a source edit, not a recall choice; combine its source
# predicate with the computed cost so each graded result is mutation-sensitive.
p,st,sol,ex,so=E['python.comments']
E['python.comments']=(p,st,sol,['[cost, "# Exclude zero so no fixed fee is charged when no items are present.\\nif quantity >= 1:" in open("main.py").read()]'],False)
scaffold('interpreter_execution_model',
 'The scaffold supplies a top-level quantity assignment and an arithmetic calculation. Change cost = quantity to cost = calculated_cost. Trace that quantity is bound before calculated_cost evaluates quantity * 4, then cost receives that evaluated value. Run the saved file as a script. The checker reads quantity and cost; there is no required printed output. Top-level statements also execute on the first import.',
 'quantity = 3\ncalculated_cost = quantity * 4\n','cost = quantity\n','cost = calculated_cost\n','',['[quantity, cost]'])
e('multiline_expressions',
 'Keep the supplied cost input unchanged. Reformat only print("Cost", cost) across multiple physical lines inside its parentheses, with four-space hanging indentation and no backslashes. Keep "Cost" first and cost second. The checker verifies a multiline call with preserved arguments and the printed label and cost with default delimiters.',
 'cost = 14\nprint("Cost", cost)\n',
 'cost = 14\nprint(\n    "Cost",\n    cost\n)\n',
 ['[cost, "print(\\n    \\\"Cost\\\",\\n    cost\\n)" in open("main.py").read()]'],True)
scaffold('string_methods',
 'The scaffold supplies strip().lower() and both splitting calls. Choose their named inputs without editing the calls: set label_input = text, comma_input = comma_text, and whitespace_input = whitespace_text rather than blank. The checker reads normalized, comma_parts and words, including the empty field between adjacent commas and the whitespace-splitting behavior. Keep all given strings unchanged.',
 'text = "  Blue  "\ncomma_text = "red,,blue"\nwhitespace_text = "  red   blue  "\nblank = ""\n',
 'label_input = blank\ncomma_input = blank\nwhitespace_input = blank\n',
 'label_input = text\ncomma_input = comma_text\nwhitespace_input = whitespace_text\n',
 'normalized = label_input.strip().lower()\ncomma_parts = comma_input.split(",")\nwords = whitespace_input.split()\n',
 ['[normalized, comma_parts, words]'])
scaffold('syntax_vs_runtime_errors',
 'Repair the supplied source header through its line-ending input: change ending = newline to ending = colon_newline so the if header ends with its missing colon. Do not edit the wrapper, inputs or conversion body. The wrapper records an error in failure without stopping the checker. Run the repaired source and inspect the error type and explanation; set stage = execution_label rather than parsing_label when it now reports an execution failure from int(raw). The checker reads failure and stage.',
 'quantity = 1\nraw = "three"\nnewline = "\\n"\ncolon_newline = ":\\n"\nexecution_label = "execution"\nparsing_label = "parsing"\n',
 'ending = newline\nstage = parsing_label\n',
 'ending = colon_newline\nstage = execution_label\n',
 'source = "if quantity > 0" + ending + "    quantity = int(raw)"\nfailure = ""\ntry:\n    exec(source)\nexcept Exception as exc:\n    failure = type(exc).__name__ + ": " + str(exc)\n',
 ['[failure, stage]'])
scaffold('truth_value_testing',
 'The scaffold contains the empty-list guard using if not quantities:. Change quantities = sample to quantities = empty before the guard. Keep the guard and print unchanged. With the initial empty list it must print No quantities once; with a nonempty list such as [3] it must display nothing. Do not compare the collection with True.',
 'input_count = 0\nmessage = "No quantities"\nsample = [3]\nempty = list(range(input_count))\n',
 'quantities = sample\n','quantities = empty\n',
 'if not quantities:\n    print(message)\n',stdout=True)
scaffold('none_and_identity',
 'The scaffold supplies an explicit None check. Change quantity = absent to quantity = supplied so legitimate zero is treated as supplied. Keep the conditional and inputs unchanged. If quantity is None print Quantity absent; otherwise print Quantity supplied and its numeric value with default delimiters. Zero must not be rejected by a truth test.',
 'supplied = 0\nabsent = None\n',
 'quantity = absent\n','quantity = supplied\n',
 'if quantity is None:\n    print("Quantity absent")\nelse:\n    print("Quantity supplied", quantity)\n',stdout=True)
scaffold('unicode_and_bytes',
 'The scaffold supplies UTF-8 encode and decode assignments. Change selected_text = empty to selected_text = text so the non-ASCII input is encoded into payload and decoded into restored. Keep both calls and matches = restored == text unchanged. The checker reads the byte values, restored text and equality result; initially restored must recover café and matches must be True.',
 'text = "caf\\u00e9"\nempty = ""\n',
 'selected_text = empty\n','selected_text = text\n',
 'payload = selected_text.encode("utf-8")\nrestored = payload.decode("utf-8")\nmatches = restored == text\n',
 ['[list(payload), restored, matches]'])

# Explicitly exercise both success-sentence states rather than relying solely
# on automatic numeric mutations to cover a None or nonempty-list case.
for cid, second in [('python.truth_value_testing', 'quantities = sample\nif not quantities:\n    print(message)\n'), ('python.none_and_identity', 'quantity = absent\nif quantity is None:\n    print("Quantity absent")\nelse:\n    print("Quantity supplied", quantity)\n')]:
    p, st, sol, ex, so = E[cid]
    E[cid] = (p + ' The supplied second run tests the alternate state as well; keep it unchanged.', st+second, sol+second, ex, so)
# Check the promised format structurally: trailing commas and other valid
# hanging-indent layouts must not be rejected by a source substring key.
p, st, sol, ex, so = E['python.multiline_expressions']
format_expr = "[cost, all(n.end_lineno > n.lineno and len(n.args) == 2 and isinstance(n.args[0], __import__('ast').Constant) and n.args[0].value == 'Cost' and isinstance(n.args[1], __import__('ast').Name) and n.args[1].id == 'cost' for n in __import__('ast').walk(__import__('ast').parse(open('main.py').read())) if isinstance(n, __import__('ast').Call) and isinstance(n.func, __import__('ast').Name) and n.func.id == 'print')]"
E['python.multiline_expressions'] = (p, st, sol, [format_expr], so)
